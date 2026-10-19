"""Original procedural short foley for chapter 2. Requires numpy, scipy and ffmpeg.
Preserve existing takes. No external recording, voice or generative model is used.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parents[4]
MOTHER=Path(__file__).resolve().parent
OUT=ROOT/'02_素材/音訊/候選/BATCH02_ROOM_MAILBOX'
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
 ('SFX04_FOOTSTEP_WOOD','world_footstep_wood','steps',5304,1.95,-22,'門外四步漸近、停住；隔門的柔和木板落腳'),
 ('SFX08_PAPER_FOLD','world_paper_fold','paper',5308,.90,-21,'一頁稿紙拿起、折起、壓平'),
 ('SFX14_KISERU_DRAW','magic_kiseru_draw','draw',5314,.95,-27,'點火後一口克制的菸斗抽吸，無人聲'),
 ('SFX16_MAILBOX_REVEAL','magic_mailbox_reveal','reveal',5316,1.18,-23,'黑色小盒子特寫的低聲魔法共鳴，無尖銳提示鈴'),
 ('SFX17_MAILBOX_OPEN','magic_mailbox_open','open',5317,.48,-22,'小木盒蓋抬起、極輕鉸鏈與木材摩擦'),
 ('SFX17_MAILBOX_OPEN','magic_mailbox_close','close',5417,.58,-23,'盒蓋闔上、輕木質接觸與短共鳴；同 cue 關蓋變體'),
 ('SFX08_PAPER_FOLD','world_notebook_close','notebook',5408,.55,-24,'筆記本闔起的紙頁與柔和封面接觸；同 cue 變體'),
]

def synth(kind,seed,duration):
    rng=np.random.default_rng(seed); n=round(duration*RATE); t=np.arange(n)/RATE; x=np.zeros(n)
    if kind=='steps':
        for at,gain in [(0.035,.60),(.49,.74),(.97,.87),(1.46,.78)]:
            step=modal(.30,[82,157,296],[1,.36,.09],[.055,.040,.025])
            tt=np.arange(len(step))/RATE
            step+=.10*band(rng,len(step),180,1450)*np.exp(-tt/.035)
            put(x,at,edge(step,.009,.05),gain)
            put(x,at+.045,rub(rng,.17,100,850,1.6),.025*gain)
    elif kind=='paper':
        for at,length,gain in [(.025,.20,.16),(.26,.29,.24),(.61,.19,.17)]:
            y=rub(rng,length,700,6200,.9)
            tt=np.arange(len(y))/RATE
            y*=.78+.12*np.sin(2*np.pi*43*tt)+.07*np.sin(2*np.pi*71*tt)
            put(x,at,y,gain)
        put(x,.66,modal(.18,[410,970],[1,.19],[.014,.008]),.018)
    elif kind=='draw':
        env=np.sin(np.pi*np.clip((t-.04)/.76,0,1))**1.6
        x+=.16*band(rng,n,220,2200)*env
        x+=.018*band(rng,n,900,3400)*env*(.7+.2*np.sin(2*np.pi*17*t))
        # A small ember crackle belongs to the same finite inhalation.
        put(x,.41,modal(.07,[860,1710],[1,.12],[.004,.002]),.009)
    elif kind=='reveal':
        env=np.sin(np.pi*np.clip(t/.98,0,1))**2
        phase=2*np.pi*(132*t+2.5*t*t)
        x+=(.26*np.sin(phase)+.08*np.sin(phase*1.51)+.025*np.sin(phase*2.08))*env
        x+=.022*band(rng,n,300,1900)*env
        put(x,.30,modal(.75,[196,294,407],[1,.27,.07],[.21,.16,.10]),.045)
    elif kind=='open':
        put(x,.025,rub(rng,.29,180,1800,1.1),.15)
        tt=np.arange(round(.24*RATE))/RATE
        hinge=np.sin(2*np.pi*(245*tt+32*tt*tt))*np.sin(np.pi*np.linspace(0,1,len(tt)))**2
        put(x,.08,hinge,.032)
        put(x,.30,modal(.16,[230,620],[1,.16],[.022,.012]),.07)
    elif kind=='close':
        put(x,.025,rub(rng,.12,240,1850,1.4),.055)
        put(x,.17,modal(.33,[185,435,880],[1,.27,.06],[.040,.026,.013]),.20)
        # Short soft resonance, not a new magical flourish or ambient layer.
        put(x,.20,modal(.35,[131,198],[1,.13],[.095,.065]),.012)
    elif kind=='notebook':
        put(x,.025,rub(rng,.17,550,4400,1.3),.12)
        put(x,.20,modal(.26,[155,390],[1,.14],[.027,.015]),.15)
        put(x,.21,rub(rng,.07,300,1800,1.5),.025)
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
        r=dict(date='2026-10-19',cue=cue,label=label,name=stem,seed=seed,status='batch02 complete scene audition pending',
            formally_adopted=False,method='original procedural short foley; no recording, external library, voice or model',
            duration_seconds=len(x)/RATE,loop=False,target_sample_peak_dbfs=peak,
            editable_source=Path(__file__).name,editable_source_sha256=digest(Path(__file__)),**export(stem,x))
        save(OUT/(stem+'_take01.json'),r);records.append(r);print('Completed '+stem,flush=True)
    save(manifest,dict(date='2026-10-19',batch='BATCH02_ROOM_MAILBOX',primary_cues=5,files=7,candidates=records))

if __name__=='__main__':main()
