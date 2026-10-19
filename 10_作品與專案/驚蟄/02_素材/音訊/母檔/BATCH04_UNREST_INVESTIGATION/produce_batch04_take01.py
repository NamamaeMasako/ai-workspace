"""Original procedural short foley for chapters 4 through 6. Requires numpy, scipy and ffmpeg.
Preserve existing takes. No external recording, voice or generative model is used.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parents[4]
MOTHER=Path(__file__).resolve().parent
OUT=ROOT/'02_素材/音訊/候選/BATCH04_UNREST_INVESTIGATION'
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
 ('SFX02_DOOR_KNOCK','world_door_knock_soft','knock',5702,.86,-23,'花見房門外的兩下輕敲'),
 ('SFX06_TABLE_TAP','world_table_tap_double','tap',5706,.63,-23,'驚蟄指尖兩下木桌敲擊'),
 ('SFX11_LAMP_SWAY','world_lamp_sway','lamp',5711,.88,-28,'入夜前燈具實際輕晃的懸掛木結構細響'),
 ('SFX22_SILK_WHISPER','battle_silk_whisper','silk',5722,.80,-29,'袖口細物縮回的低聲纖維張力提示'),
 ('SFX24_SPIDER_STEPS','battle_spider_steps','spider',5724,1.05,-30,'門縫下蛛腳的極輕短促爬動提示；非巨大重步'),
 ('SFX23_SILK_CUT','battle_silk_snap_fine','snap',5823,.32,-27,'窗邊極細裂響變體；戰鬥切絲基礎音仍待第五批'),
 ('SFX01_SLIDING_DOOR','world_window_slide_soft','window',5801,.72,-25,'窗扇在木軌輕移並停住的短變體'),
 ('SFX01_SLIDING_DOOR','world_sliding_door_close_soft','close',5901,.52,-25,'房門輕輕帶上的短變體'),
 ('SFX08_PAPER_FOLD','world_dry_material_rub','dry',5808,.73,-27,'未點燃煙草摩挲／灰殼掃拂／未燃香封味的乾燥細物變體'),
 ('SFX08_PAPER_FOLD','world_notebook_open','book',5908,.69,-24,'攤開筆記的封面與紙頁變體'),
 ('SFX17_MAILBOX_OPEN','world_mailbox_stow','stow',5817,.95,-24,'將完整郵箱收進房梁暗格的木盒接觸與暗格木件移動變體'),
]

def synth(kind,seed,duration):
    rng=np.random.default_rng(seed); n=round(duration*RATE); t=np.arange(n)/RATE; x=np.zeros(n)
    if kind in ('knock','tap'):
        times=[.035,.37] if kind=='knock' else [.025,.255]
        for i,at in enumerate(times):
            freqs=[145,320,670] if kind=='knock' else [255,570,1120]
            y=modal(.25,freqs,[1,.25,.05],[.042,.025,.012])
            tt=np.arange(len(y))/RATE
            y+=.035*band(rng,len(y),250,2600)*np.exp(-tt/.015)
            put(x,at,edge(y,.006,.04),1 if i==0 else .82)
    elif kind=='lamp':
        for at,length,g in [(.04,.24,.10),(.38,.27,.068)]:
            y=rub(rng,length,140,1350,1.8)
            tt=np.arange(len(y))/RATE
            y+=.30*np.sin(2*np.pi*(226*tt-18*tt*tt))*np.sin(np.pi*np.linspace(0,1,len(y)))**2
            put(x,at,y,g)
    elif kind=='silk':
        put(x,.035,rub(rng,.46,1400,5500,1.8),.075)
        y=modal(.36,[620,1080,1840],[1,.10,.025],[.045,.030,.012])
        put(x,.30,y,.006)
    elif kind=='spider':
        for at,g in [(.035,.55),(.16,.30),(.39,.50),(.51,.27),(.72,.32)]:
            y=modal(.13,[880,1630],[1,.07],[.008,.004])
            put(x,at,y,.025*g)
            put(x,at+.014,rub(rng,.07,950,3900,1.7),.025*g)
    elif kind=='snap':
        put(x,.025,modal(.24,[1080,1960,3100],[1,.15,.025],[.012,.007,.003]),.08)
        put(x,.025,rub(rng,.035,1600,6500,1.4),.025)
    elif kind in ('window','close'):
        length=.46 if kind=='window' else .29
        put(x,.025,rub(rng,length,130,1900,1.3),.14)
        put(x,.47 if kind=='window' else .28,modal(.20,[165,405,850],[1,.22,.035],[.035,.018,.009]),.10)
    elif kind=='dry':
        for at,length,g in [(.035,.21,.13),(.30,.25,.10)]:
            y=rub(rng,length,700,4800,1.6); tt=np.arange(len(y))/RATE
            y*=.82+.12*np.sin(2*np.pi*57*tt)
            put(x,at,y,g)
    elif kind=='book':
        put(x,.025,modal(.25,[165,420],[1,.16],[.028,.012]),.07)
        put(x,.08,rub(rng,.26,450,3800,1.1),.14)
        put(x,.39,rub(rng,.15,850,4800,1.5),.10)
    elif kind=='stow':
        put(x,.035,modal(.24,[172,390,760],[1,.23,.035],[.038,.022,.011]),.13)
        put(x,.31,rub(rng,.34,140,1700,1.3),.10)
        put(x,.63,modal(.24,[155,440],[1,.14],[.034,.016]),.07)
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
        r=dict(date='2026-10-19',cue=cue,label=label,name=stem,seed=seed,status='batch04 complete scene audition pending',
            formally_adopted=False,method='original procedural short foley; no recording, external library, voice or model',
            duration_seconds=len(x)/RATE,loop=False,target_sample_peak_dbfs=peak,
            editable_source=Path(__file__).name,editable_source_sha256=digest(Path(__file__)),**export(stem,x))
        save(OUT/(stem+'_take01.json'),r);records.append(r);print('Completed '+stem,flush=True)
    save(manifest,dict(date='2026-10-19',batch='BATCH04_UNREST_INVESTIGATION',primary_cues=5,files=11,candidates=records))

if __name__=='__main__':main()
