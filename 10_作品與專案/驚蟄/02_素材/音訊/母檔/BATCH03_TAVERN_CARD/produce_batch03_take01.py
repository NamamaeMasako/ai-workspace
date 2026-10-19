"""Original procedural short foley for chapter 3. Requires numpy, scipy and ffmpeg.
Preserve existing takes. No external recording, voice or generative model is used.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parents[4]
MOTHER=Path(__file__).resolve().parent
OUT=ROOT/'02_素材/音訊/候選/BATCH03_TAVERN_CARD'
RATE=48000

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def db(x): return float(20*np.log10(max(float(x),1e-12)))
def band(rng,n,lo,hi):
    x=sosfilt(butter(2,[lo,hi],btype='bandpass',fs=RATE,output='sos'),rng.standard_normal(n))
    return x/max(float(np.sqrt(np.mean(x*x))),1e-12)
def edge(x,attack=.008,release=.04):
    x=x.copy(); a=min(round(attack*RATE),len(x)); r=min(round(release*RATE),len(x))
    x[:a]*=np.linspace(0,1,a)**2; x[-r:]*=np.linspace(1,0,r)**2
    return x
def modal(length,freqs,amps,decays):
    t=np.arange(round(length*RATE))/RATE; x=np.zeros(len(t))
    for f,a,d in zip(freqs,amps,decays):x+=a*np.sin(2*np.pi*f*t)*np.exp(-t/d)
    return edge(x,.003,.04)
def put(x,at,y,gain=1):
    start=round(at*RATE); count=min(len(y),len(x)-start)
    if count>0:x[start:start+count]+=y[:count]*gain
def rub(rng,length,lo,hi,power=1.2):
    n=round(length*RATE)
    env=np.sin(np.pi*np.linspace(0,1,n))**power
    return band(rng,n,lo,hi)*env

SPECS=[
 ('SFX09_CARD_PLACE','world_black_card_place','place',5509,.40,-21.5,'厚紙黑卡輕放木桌，一次柔和接觸'),
 ('SFX10_CARD_SLIDE','world_black_card_slide','slide',5510,.66,-22,'黑卡沿木桌推近，短乾紙摩擦與停下'),
 ('SFX18_CARD_PULSE','magic_black_card_pulse','pulse',5518,1.20,-27,'撕開就知道了之後的一次極輕黑卡共鳴；非心跳或警報'),
 ('SFX09_CARD_PLACE','world_black_card_stow','stow',5609,.75,-24,'黑卡拿起、收入袖口；紙與薄布的收卡變體'),
]

def synth(kind,seed,duration):
    rng=np.random.default_rng(seed); n=round(duration*RATE); t=np.arange(n)/RATE; x=np.zeros(n)
    if kind=='place':
        put(x,.025,rub(rng,.075,650,4000,1.1),.045)
        put(x,.085,modal(.25,[184,416,890],[1,.24,.035],[.028,.018,.009]),.22)
        put(x,.082,rub(rng,.065,240,1850,1.6),.034)
    elif kind=='slide':
        y=rub(rng,.46,450,4400,1.1); tt=np.arange(len(y))/RATE
        y*=.82+.11*np.sin(2*np.pi*31*tt)+.05*np.sin(2*np.pi*73*tt)
        put(x,.035,y,.18)
        put(x,.46,modal(.16,[228,550],[1,.11],[.016,.007]),.035)
    elif kind=='pulse':
        env=np.sin(np.pi*np.clip((t-.035)/1.10,0,1))**2.4
        x+=(.25*np.sin(2*np.pi*132*t)+.055*np.sin(2*np.pi*197*t)+.018*np.sin(2*np.pi*281*t))*env
        x+=.009*band(rng,n,190,1400)*env
    elif kind=='stow':
        put(x,.025,rub(rng,.17,650,4300,1.3),.12)
        put(x,.27,rub(rng,.31,210,2450,1.7),.15)
        put(x,.40,rub(rng,.18,750,3100,1.7),.025)
    x-=np.mean(x); return edge(x,.005,.05)

def export(stem,x):
    wav=MOTHER/(stem+'_take01.wav'); ogg=OUT/(stem+'_take01.ogg')
    subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','1','-i','-',
        '-c:a','pcm_s24le',str(wav)],input=x.astype('<f4').tobytes(),check=True)
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','1',
        '-c:a','libvorbis','-q:a','6',str(ogg)],check=True)
    decoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(ogg),'-f','f32le','-']),dtype='<f4')
    return dict(wav=dict(file=wav.name,sha256=digest(wav)),ogg=dict(file=ogg.name,sha256=digest(ogg),
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)])),
        decoded_sample_peak_dbfs=db(np.max(np.abs(decoded))),decoded_rms_dbfs=db(np.sqrt(np.mean(decoded.astype(float)**2)))))

def main():
    OUT.mkdir(parents=True,exist_ok=True); manifest=OUT/'generation_manifest_take01.json'
    if manifest.exists():raise FileExistsError(manifest)
    records=[]
    for cue,stem,kind,seed,duration,peak,label in SPECS:
        x=synth(kind,seed,duration); x*=10**(peak/20)/max(float(np.max(np.abs(x))),1e-12)
        r=dict(date='2026-10-19',cue=cue,label=label,name=stem,seed=seed,status='batch03 complete scene audition pending',
            formally_adopted=False,method='original procedural short foley; no recording, external library, voice or model',
            duration_seconds=len(x)/RATE,loop=False,target_sample_peak_dbfs=peak,
            editable_source=Path(__file__).name,editable_source_sha256=digest(Path(__file__)),**export(stem,x))
        save(OUT/(stem+'_take01.json'),r);records.append(r);print('Completed '+stem,flush=True)
    save(manifest,dict(date='2026-10-19',batch='BATCH03_TAVERN_CARD',primary_cues=3,files=4,candidates=records))

if __name__=='__main__':main()
