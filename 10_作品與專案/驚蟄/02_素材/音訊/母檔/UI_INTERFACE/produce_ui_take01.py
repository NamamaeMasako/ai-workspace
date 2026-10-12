"""Create the two original, procedurally synthesized UI audition cues.

Requires Python 3, numpy, ffmpeg and ffprobe. Existing outputs are preserved.
No external sample or music model is used. Run this source from its asset folder.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
MOTHER = ROOT / '02_素材/音訊/母檔/UI_INTERFACE'
OUT = ROOT / '02_素材/音訊/候選/UI_INTERFACE'
RATE = 48000
SPECS = [
    dict(cue='UI01_CONFIRM', name='ui_confirm_take01', label='確認', seed=4101,
         duration=.28, frequencies=[780, 1208, 2070, 3060],
         weights=[1., .44, .16, .055], decays=[.044, .030, .020, .012],
         direction='Higher, clear, soft wood-like tap; no bright metallic ring',
         scene='主選單、設定、存讀檔、劇情選項確認'),
    dict(cue='UI02_BACK', name='ui_back_take01', label='返回', seed=4102,
         duration=.30, frequencies=[470, 825, 1340, 2210],
         weights=[1., .40, .14, .045], decays=[.052, .032, .019, .010],
         direction='Lower, softer wood-like tap with a gently decaying tail',
         scene='返回上一頁、關閉選單'),
]

def run(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, **kwargs)

def write_wav(path, pcm):
    run(['ffmpeg', '-v', 'error', '-n', '-f', 'f32le', '-ar', str(RATE),
         '-ac', '1', '-i', '-', '-c:a', 'pcm_s24le', str(path)],
        input=pcm.astype('<f4').tobytes())

def encode(source, dest):
    run(['ffmpeg', '-v', 'error', '-n', '-i', str(source), '-ar', '44100',
         '-ac', '1', '-c:a', 'libvorbis', '-q:a', '6', str(dest)])

def metadata(path):
    decoded=run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'])
    if decoded.stderr.strip():
        raise RuntimeError(decoded.stderr.decode(errors='replace'))
    return dict(file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                format=json.loads(run(['ffprobe', '-v', 'error', '-show_entries',
                    'stream=codec_name,sample_rate,channels:format=duration',
                    '-of', 'json', str(path)]).stdout))

def synthesize(spec):
    t=np.arange(round(RATE*spec['duration']), dtype=np.float64)/RATE
    pcm=np.zeros_like(t)
    attack=1-np.exp(-t/.0018)
    for freq, weight, decay in zip(spec['frequencies'], spec['weights'], spec['decays']):
        pcm += weight*np.sin(2*np.pi*freq*t)*np.exp(-t/decay)*attack
    noise=np.random.default_rng(spec['seed']).standard_normal(len(t))
    noise=np.convolve(noise, np.ones(9)/9, mode='same')
    pcm += .21*noise*np.exp(-t/.007)*attack
    # Remove DC and smoothly anchor both endpoints, without reverberant padding.
    pcm -= np.mean(pcm)
    fade=round(.012*RATE)
    pcm[-fade:] *= np.linspace(1,0,fade)**2
    pcm[:round(.001*RATE)] *= np.linspace(0,1,round(.001*RATE))
    gain=10**(-10/20)/np.max(np.abs(pcm))
    pcm *= gain
    return pcm.astype(np.float32), float(gain)

def main():
    MOTHER.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest=OUT/'generation_manifest_take01.json'
    if manifest.exists():
        raise FileExistsError(manifest)
    records=[]
    for spec in SPECS:
        pcm,gain=synthesize(spec)
        wav=MOTHER/(spec['name']+'.wav')
        ogg=OUT/(spec['name']+'.ogg')
        preview=np.zeros(3*RATE, dtype=np.float32)
        for offset in [.1,1.1,2.1]:
            start=round(offset*RATE)
            preview[start:start+len(pcm)] = pcm
        preview_wav=MOTHER/(spec['name']+'_preview.wav')
        preview_ogg=OUT/(spec['name']+'_preview.ogg')
        write_wav(wav,pcm); encode(wav,ogg)
        write_wav(preview_wav,preview); encode(preview_wav,preview_ogg)
        record=dict(date='2026-10-12', status='awaiting user audition; not integrated',
                    method='original procedural modal synthesis with deterministic filtered-noise transient',
                    spec=spec, fixed_peak_gain=gain, sample_peak_dbfs=-10,
                    rms_dbfs=float(20*np.log10(np.sqrt(np.mean(pcm.astype(np.float64)**2)))),
                    preview_repeat_starts_seconds=[.1,1.1,2.1],
                    wav=metadata(wav), ogg=metadata(ogg), preview_wav=metadata(preview_wav),
                    preview_ogg=metadata(preview_ogg),
                    editable_source=dict(file=Path(__file__).name,
                        sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
                    technical_check='complete decoding with no diagnostics; musical suitability pending user')
        (OUT/(spec['name']+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        records.append(record)
        print(f"Completed {spec['name']}: {spec['duration']} seconds, peak -10 dBFS", flush=True)
    manifest.write_text(json.dumps(dict(date='2026-10-12',candidates=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
