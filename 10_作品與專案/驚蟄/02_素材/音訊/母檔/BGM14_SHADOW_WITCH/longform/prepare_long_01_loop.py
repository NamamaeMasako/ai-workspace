"""Prepare selected BGM14 candidate 04 for game audition; preserve the approved opening."""
from pathlib import Path
import hashlib, json, re, subprocess
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
WAV = Path(__file__).resolve().parent
OUT = ROOT / '02_素材/音訊/候選/BGM14_SHADOW_WITCH/longform'
BASE = 'long_01_natural_phrase_strings_hidden_care_seed4104'
NAME = BASE + '_loop_full_attack'
RATE = 48000
source = WAV / (BASE + '.wav')
wav = WAV / (NAME + '.wav')
ogg = OUT / (NAME + '.ogg')
metadata = OUT / (NAME + '.json')
if any(p.exists() for p in (wav, ogg, metadata)):
    raise FileExistsError('Existing loop outputs must be preserved')
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
long_record = json.loads((OUT / (BASE + '.json')).read_text(encoding='utf-8'))
if digest(source) != long_record['assembled_wav']['sha256']:
    raise RuntimeError('Approved long mother hash differs')
original = np.frombuffer(subprocess.check_output([
    'ffmpeg','-v','error','-i',str(source),'-ar',str(RATE),'-ac','2','-f','f32le','-'
]), dtype='<f4').reshape(-1, 2)
pcm = original.copy()
overlap = RATE
phase = np.linspace(0, 1, overlap, dtype=np.float32)
weight = (phase * phase * (3 - 2 * phase))[:, None]
# Preserve the entire incoming attack. Only the outgoing low tail fades away.
pcm[-overlap:] = original[-overlap:] * (1 - weight) + original[:overlap]
duration = len(pcm) / RATE
subprocess.run([
    'ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-',
    '-c:a','pcm_f32le',str(wav)
], input=pcm.astype('<f4').tobytes(), check=True)
subprocess.run([
    'ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','2',
    '-c:a','libvorbis','-q:a','5',str(ogg)
], check=True)
log = subprocess.run([
    'ffmpeg','-hide_banner','-i',str(ogg),'-af',
    'silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
    '-f','null','-'
], capture_output=True, text=True, encoding='utf-8', check=True).stderr
stats = json.loads(log[log.rfind('{'):log.rfind('}')+1])
r = dict(date='2026-10-19', cue='BGM14_SHADOW_WITCH', label='冷語之下',
    status='selected for game audition; scene and loop confirmation pending',
    user_instruction='用第四版', formally_adopted=False,
    source=dict(file=source.name, sha256=digest(source)),
    processing=dict(new_generation=False, uniform_gain_db=0,
        unchanged_opening_seconds=duration-1, tail_overlap_seconds=1,
        incoming_attack_gain=1, outgoing_tail_curve='smoothstep fade',
        duration_seconds=duration, renpy_loop_start_seconds=1.0,
        repeat_period_seconds=duration-1,
        unchanged_opening_pcm_max_error=float(np.max(np.abs(pcm[:-overlap]-original[:-overlap]))),
        boundary_matches_original_opening_transition=bool(np.array_equal(pcm[-1], original[overlap-1])),
        outgoing_last_second_rms_dbfs=float(20*np.log10(max(float(np.sqrt(np.mean(original[-overlap:].astype(float)**2))),1e-12))),
        basis='Overlay the full first second onto the approved low tail; resume at 1s. No measured beat alignment or human listening approval is claimed.'),
    wav=dict(file=wav.name, sha256=digest(wav)),
    ogg=dict(file=ogg.name, sha256=digest(ogg), probe=json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)]))),
    technical_measurements=dict(integrated_lufs=stats['input_i'], true_peak_dbtp=stats['input_tp'],
        quiet_events=re.findall(r'silence_(?:start|end):[^\r\n]*',log)),
    producer=dict(file=Path(__file__).name, sha256=digest(Path(__file__))))
metadata.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(r,ensure_ascii=False,indent=2))
