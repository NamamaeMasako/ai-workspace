"""Repair quick releases and build a phrase-end loop from preserved BGM13 sources."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import numpy as np

RATE = 48000
BASE = Path(__file__).resolve().parent
OUT = BASE.parents[2] / '候選/BGM13_HOLD_ON/longform'
OLD = 'long_01_natural_phrase_piano_cello_fading_seed4001'
NAME = 'long_02_tail_repair_piano_cello_fading_seed4001_loop_full_attack'


def decode(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
                                   '-ar', str(RATE), '-ac', '2', '-f', 'f32le', '-'])
    return np.frombuffer(data, dtype='<f4').reshape(-1, 2).copy()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rms(x):
    return float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))


def smooth(n):
    t = np.linspace(0, 1, n, dtype=np.float32)
    return (t * t * (3 - 2 * t))[:, None]


def write_wav(path, pcm):
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-f', 'f32le', '-ar', str(RATE),
                    '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', str(path)],
                   input=pcm.astype('<f4').tobytes(), check=True)


def stretch_tail(x, length):
    # Two WSOLA stages retain nominal pitch while extending only the local tail.
    result = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(RATE),
                             '-ac', '2', '-i', '-', '-af', 'atempo=0.5,atempo=0.5',
                             '-f', 'f32le', '-'], input=x.astype('<f4').tobytes(),
                            capture_output=True, check=True)
    y = np.frombuffer(result.stdout, dtype='<f4').reshape(-1, 2).copy()
    if len(y) < length:
        y = np.pad(y, ((0, length - len(y)), (0, 0)))
    return y[:length]


def main():
    wav = BASE / (NAME + '.wav')
    ogg = OUT / (NAME + '.ogg')
    metadata = OUT / (NAME + '.json')
    if any(p.exists() for p in (wav, ogg, metadata)):
        raise FileExistsError('Revision already exists')
    old_path = BASE / (OLD + '.wav')
    raw_path = BASE / (OLD + '_raw.wav')
    natural_path = BASE / (OLD + '_unfaded_leveled_source.wav')
    old_record = json.loads((OUT / (OLD + '.json')).read_text(encoding='utf-8'))
    original, raw, natural = map(decode, (old_path, raw_path, natural_path))
    continuation_gain = 10 ** (old_record['processing']['continuation_gain_db'] / 20)

    # Keep the full last phrase instead of fading the note struck near 59.2 seconds.
    period = 66.75  # Three 22.25-second source-map periods, not a measured bar grid.
    overlap = 1.0
    duration = period + overlap
    n = round(duration * RATE)
    rebuilt = np.zeros((n, 2), dtype=np.float32)
    rebuilt[:len(raw)] = raw * continuation_gain
    rebuilt[:round(59.5 * RATE)] = original[:round(59.5 * RATE)]

    # The 65-second model output ends during another note; restore its unfaded
    # corresponding original phrase tail rather than extending that model fade.
    a, b, shift = 62.75, 63.10, 44.5
    ia, ib = round(a * RATE), round(b * RATE)
    src_a = round((a - shift) * RATE)
    source_tail = natural[src_a:src_a + n - ia].copy()
    if len(source_tail) != n - ia:
        raise RuntimeError('Original tail is too short')
    gain = rms(rebuilt[ia:ia + RATE // 5]) / max(rms(source_tail[:RATE // 5]), 1e-12)
    gain = min(gain, 10 ** (-16 / 20) / max(float(np.max(np.abs(source_tail))), 1e-12))
    source_tail *= gain
    weight = smooth(ib - ia)
    rebuilt[ia:ib] = rebuilt[ia:ib] * (1 - weight) + source_tail[:ib - ia] * weight
    rebuilt[ib:] = source_tail[ib - ia:]

    # Replace the rapid gate with the same local timbre and a gradual release.
    # Existing following note attacks return at unity gain before they arrive.
    before_patches = rebuilt.copy()
    patches = []
    for release in (18.9, 41.15, 63.4):
        start, full, finish = release - .45, release - .10, release + 1.40
        i, j = round(start * RATE), round(finish * RATE)
        src_i, src_j = round((release - .65) * RATE), round((release - .10) * RATE)
        wet = stretch_tail(before_patches[src_i:src_j], j - i)
        local_gain = rms(before_patches[i:i + round(.18 * RATE)]) / max(rms(wet[:round(.18 * RATE)]), 1e-12)
        wet *= local_gain
        t = np.arange(j - i, dtype=np.float32) / RATE + start
        fade_in = np.clip((t - start) / (full - start), 0, 1)
        fade_in = fade_in * fade_in * (3 - 2 * fade_in)
        restore = np.clip((t - (release - .05)) / .25, 0, 1)
        restore = restore * restore * (3 - 2 * restore)
        dry_weight = np.maximum(1 - fade_in, restore)
        decay = np.exp(-np.maximum(t - full, 0) / .60)
        fade_out = np.clip((finish - t) / .25, 0, 1)
        fade_out = fade_out * fade_out * (3 - 2 * fade_out)
        wet_weight = fade_in * decay * fade_out
        rebuilt[i:j] = before_patches[i:j] * dry_weight[:, None] + wet * wet_weight[:, None]
        patches.append({'release_seconds': release, 'changed_interval_seconds': [start, finish],
                        'local_source_interval_seconds': [release - .65, release - .10],
                        'nominal_pitch_preserved': True, 'stretch_factor': 4,
                        'exponential_release_tau_seconds': .60,
                        'following_original_notes_restore_by_seconds': release + .20,
                        'local_tail_gain_db': float(20 * np.log10(local_gain))})

    # This handoff ends after the old phrase has decayed. The incoming first note
    # is introduced at the start of the overlap, keeping its attack and full tail.
    i = round(period * RATE)
    w = smooth(round(overlap * RATE))
    pcm = rebuilt.copy()
    pcm[i:] = rebuilt[i:] * (1 - w) + rebuilt[:len(w)]
    write_wav(wav, pcm)
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(wav), '-ar', '44100',
                    '-ac', '2', '-c:a', 'libvorbis', '-q:a', '5', str(ogg)], check=True)

    details = {}
    for label, source in [('before', old_path), ('after', wav)]:
        clip = OUT / (NAME + '_detail_' + label + '_16to24.ogg')
        subprocess.run(['ffmpeg', '-v', 'error', '-n', '-ss', '16', '-i', str(source),
                        '-t', '8', '-af', 'afade=t=in:st=0:d=0.03,afade=t=out:st=7.85:d=0.15',
                        '-ar', '44100', '-ac', '2', '-c:a', 'libvorbis', '-q:a', '5', str(clip)], check=True)
        details[label] = {'file': clip.name, 'sha256': digest(clip)}

    report = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(ogg), '-af',
                             'silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                             '-f', 'null', '-'], capture_output=True, check=True).stderr.decode('utf-8', errors='replace')
    stats = json.loads(report[report.rfind('{'):report.rfind('}') + 1])
    record = {'date': '2026-10-16', 'cue': 'BGM13_HOLD_ON',
              'status': 'tail repair ready for game audition; user confirmation pending',
              'user_feedback': '曲子中間就有；有幾個音像突然斷掉，循環接得生硬',
              'new_generation': False, 'formally_adopted': False,
              'sources': [{'file': p.name, 'sha256': digest(p)} for p in (old_path, raw_path, natural_path)],
              'processing': {'method': 'Local pitch-preserving tail extension and unfaded original phrase restoration',
                             'patches': patches, 'final_phrase_restoration': {'destination_seconds': [a, duration],
                             'original_source_seconds': [a - shift, duration - shift], 'gain_db': float(20 * np.log10(gain)),
                             'crossfade_seconds': [a, b]},
                             'unchanged_opening_seconds': 18.45, 'uniform_master_gain_db': 0,
                             'duration_seconds': duration, 'renpy_loop_start_seconds': overlap,
                             'repeat_period_seconds': period, 'loop_overlap_seconds': overlap, 'incoming_intro_gain': 1.0,
                             'loop_overlap_method': 'Add the intact incoming intro while fading only the already quiet outgoing tail',
                             'loop_basis': 'Three fixed source-map periods plus natural original phrase decay; not measured bar alignment',
                             'pcm_boundary_step': float(np.max(np.abs(pcm[-1] - pcm[round(overlap * RATE)])))},
              'wav': {'file': wav.name, 'sha256': digest(wav)},
              'ogg': {'file': ogg.name, 'sha256': digest(ogg), 'probe': json.loads(subprocess.check_output([
                  'ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,sample_rate,channels:format=duration',
                  '-of', 'json', str(ogg)]))}, 'detail_clips': details,
              'technical_measurements': {'integrated_lufs': stats['input_i'], 'true_peak_dbtp': stats['input_tp'],
                  'quiet_events': re.findall(r'silence_(?:start|end):[^\r\n]*', report)},
              'hearing_limit': 'Signal inspection locates gates; actual smoothness and musical fit require user audition.',
              'producer': {'file': Path(__file__).name, 'sha256': digest(Path(__file__))}}
    metadata.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'file': ogg.name, 'sha256': record['ogg']['sha256'],
                      'loop': record['processing'], 'measurements': record['technical_measurements']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
