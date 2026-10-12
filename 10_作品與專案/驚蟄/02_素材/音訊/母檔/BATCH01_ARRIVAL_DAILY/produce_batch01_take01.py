"""Original procedural atmosphere and foley sources for scene batch 01.

Requires numpy, scipy, ffmpeg and ffprobe. Preserve outputs; use a new take for edits.
No recorded sample, external sample library or music model is used.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parents[4]
MOTHER=ROOT/'02_素材/音訊/母檔/BATCH01_ARRIVAL_DAILY'
OUT=ROOT/'02_素材/音訊/候選/BATCH01_ARRIVAL_DAILY'
RATE=48000
DURATION=45

def run(args, **kw): return subprocess.run(args, capture_output=True, check=True, **kw)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def db(v): return float(20*np.log10(max(float(v),1e-12)))
def unit(x): return x/max(float(np.sqrt(np.mean(x*x))),1e-12)

def color(rng,n,lo,hi,slope=.6):
    """Periodic band-limited random noise; samples wrap on the FFT period."""
    f=np.fft.rfftfreq(n,1/RATE)
    spectrum=np.fft.rfft(rng.standard_normal(n))
    weight=np.zeros_like(f)
    active=(f>lo)&(f<hi)
    if active.any():
        z=(f[active]-lo)/(hi-lo)
        edge=np.minimum(1,np.minimum(z*12,(1-z)*12))
        weight[active]=edge*np.maximum(f[active],1)**(-slope)
    return unit(np.fft.irfft(spectrum*weight,n)).astype(np.float32)

def band(rng,n,lo,hi):
    sos=butter(2,[lo,hi],btype='bandpass',fs=RATE,output='sos')
    return unit(sosfilt(sos,rng.standard_normal(n))).astype(np.float32)

def edge(x,attack=.006,release=.025):
    x=x.copy()
    a=min(round(attack*RATE),len(x)); r=min(round(release*RATE),len(x))
    x[:a] *= np.linspace(0,1,a)**2
    x[-r:] *= np.linspace(1,0,r)**2
    return x

def modal(duration,freqs,amps,decays):
    t=np.arange(round(duration*RATE))/RATE
    x=np.zeros_like(t)
    for f,a,d in zip(freqs,amps,decays):
        x += a*np.sin(2*np.pi*f*t)*np.exp(-t/d)
    return edge(x,.002,.035).astype(np.float32)

def put(x,at,chunk,gain=1):
    start=round(at*RATE)
    stop=min(len(x),start+len(chunk))
    if stop>start: x[start:stop] += chunk[:stop-start]*gain

def ambience(kind,seed):
    rng=np.random.default_rng(seed); n=DURATION*RATE; t=np.arange(n)/RATE
    if kind=='road':
        slow=.77+.16*np.sin(2*np.pi*2*t/DURATION+.8)+.08*np.sin(2*np.pi*5*t/DURATION)
        mid=.82+.14*np.sin(2*np.pi*3*t/DURATION+1.7)
        left=.57*color(rng,n,90,1200,.65)*slow+.22*color(rng,n,700,4500,.45)*mid
        right=.57*color(rng,n,90,1200,.65)*slow+.22*color(rng,n,700,4500,.45)*mid
        # Soft foliage movement follows broad, slowly changing gusts.
        leaves=(.03+.10*(.5+.5*np.sin(2*np.pi*7*t/DURATION+2.1))**6)
        left += color(rng,n,1800,7200,.15)*leaves
        right += color(rng,n,1800,7200,.15)*leaves
    elif kind=='room':
        common=color(rng,n,140,1350,.8)
        left=.095*common+.025*color(rng,n,300,2100,.6)
        right=.095*common+.025*color(rng,n,300,2100,.6)
        # Sparse distant wood settling, rather than voices or obvious nearby footsteps.
        for at in [6.7,18.3,31.2,39.6]:
            length=round(.5*RATE); tt=np.arange(length)/RATE
            creak=band(rng,length,190,1600)*np.sin(np.pi*np.linspace(0,1,length))**3
            creak += .3*np.sin(2*np.pi*(230*tt+18*tt*tt))*np.sin(np.pi*np.linspace(0,1,length))**3
            put(left,at,creak,.04); put(right,at+.004,creak,.028)
    else:
        stream=.8+.08*np.sin(2*np.pi*4*t/DURATION+.7)
        wind=.44+.12*np.sin(2*np.pi*2*t/DURATION)
        left=.58*color(rng,n,450,6200,.25)*stream+.18*color(rng,n,130,1700,.7)*wind
        right=.52*color(rng,n,450,6200,.25)*stream+.18*color(rng,n,130,1700,.7)*wind
        # Irregular tiny water bubbles, without a rhythmic fountain pulse.
        for at in rng.uniform(.8,DURATION-.8,80):
            length=rng.uniform(.015,.05); tt=np.arange(round(length*RATE))/RATE
            f=rng.uniform(430,1300)
            bubble=np.sin(2*np.pi*(f*tt-2.5*f*tt*tt))*np.exp(-tt/(length*.22))
            bubble=edge(bubble,.001,.01)
            pan=rng.uniform(.2,.8); gain=rng.uniform(.025,.065)
            put(left,at,bubble,gain*(1-pan));put(right,at,bubble,gain*pan)
    x=np.column_stack([left,right]).astype(np.float32)
    x -= np.mean(x,axis=0)
    # All continuous components are periodic; add a small endpoint correction
    # to remove residual DC/sample mismatch at the circular boundary.
    seam=round(.020*RATE)
    correction=(x[-1]-x[0]).copy()
    x[-seam:] -= np.linspace(0,1,seam)[:,None]**2*correction
    return x

def foley(kind,seed):
    rng=np.random.default_rng(seed)
    durations={'door':.86,'bell':.48,'ignite':.72,'ember':1.15,'writing':1.05,'cloth':.68}
    n=round(durations[kind]*RATE); t=np.arange(n)/RATE; x=np.zeros(n,dtype=np.float32)
    if kind=='door':
        env=np.sin(np.pi*np.clip((t-.035)/.69,0,1))**.8
        x += .36*band(rng,n,130,1800)*env*(.78+.1*np.sin(2*np.pi*19*t))
        x += .11*band(rng,n,1400,4400)*env
        put(x,.025,modal(.25,[190,470,1010],[.9,.3,.09],[.045,.024,.014]),.17)
        put(x,.69,modal(.17,[145,420,890],[1,.35,.1],[.04,.018,.012]),.48)
    elif kind=='bell':
        x += modal(.48,[910,1480,2475],[1,.30,.08],[.075,.04,.018])
        x += .05*band(rng,n,900,6000)*np.exp(-t/.006)
    elif kind=='ignite':
        scratch=np.sin(np.pi*np.clip(t/.28,0,1))**1.2
        x += .3*band(rng,n,550,5600)*scratch
        x += .055*band(rng,n,250,2800)*np.exp(-np.maximum(t-.20,0)/.12)*(t>.20)
        for at in [.19,.26,.35,.48]:
            p=modal(.04,[1200,2800],[1,.2],[.003,.002])
            put(x,at,p,rng.uniform(.03,.06))
    elif kind=='ember':
        x += .015*band(rng,n,900,5000)*np.sin(np.pi*t/durations[kind])**2
        for at in [.11,.34,.52,.81,.96]:
            length=round(rng.uniform(.014,.026)*RATE)
            p=band(rng,length,650,4800)*np.exp(-np.arange(length)/(RATE*.003))
            put(x,at,edge(p,.0005,.004),rng.uniform(.025,.06))
    elif kind=='writing':
        for at,length in [(.05,.14),(.25,.11),(.45,.19),(.72,.16)]:
            count=round(length*RATE)
            stroke=band(rng,count,900,6500)*np.sin(np.pi*np.linspace(0,1,count))**.6
            put(x,at,stroke,rng.uniform(.16,.25))
        x += .01*band(rng,n,200,1400)
    else:
        for at,length in [(.035,.21),(.31,.27)]:
            count=round(length*RATE)
            rub=.28*band(rng,count,320,2800)+.055*band(rng,count,2400,6000)
            rub *= np.sin(np.pi*np.linspace(0,1,count))**1.5
            put(x,at,rub)
    x=edge(x,.004,.035); x-=np.mean(x)
    return edge(x,.003,.020)

SPECS=[
 ('AMB01_ROAD_WIND','amb_road_twilight_wind','road',5101,-29,'舊道暮色、低風與草木'),
 ('AMB02_INN_WOOD_ROOM','amb_inn_wood_room','room',5102,-38,'木造旅店清淡室內底聲與遠處木構'),
 ('AMB03_COURTYARD_WATER_WIND','amb_courtyard_water_wind','water',5103,-31,'後院柔水流與風'),
 ('SFX01_SLIDING_DOOR','world_sliding_door','door',5201,-15,'序章推門入庄'),
 ('SFX03_WOOD_BELL','world_wood_bell','bell',5203,-18,'拉門後稍晚的木鈴'),
 ('SFX13_KISERU_IGNITE','magic_kiseru_ignite','ignite',5213,-19,'序章煙草燃起'),
 ('SFX15_EMBER','magic_kiseru_ember','ember',5215,-25,'第一章前院煙草餘燼'),
 ('SFX07_WRITING','world_writing_pen','writing',5207,-23,'第一章後院寫下與重寫句子'),
 ('SFX08_PAPER_FOLD','world_cloth_wrapped_naginata','cloth',5208,-23,'SFX08 包布摩擦變體；摺紙基礎音仍待第二批'),
]

def export(stem,x):
    wav=MOTHER/(stem+'_take01.wav'); ogg=OUT/(stem+'_take01.ogg')
    channels=1 if x.ndim==1 else x.shape[1]
    run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac',str(channels),'-i','-',
         '-c:a','pcm_s24le',str(wav)],input=x.astype('<f4').tobytes())
    run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac',str(channels),
         '-c:a','libvorbis','-q:a','6',str(ogg)])
    decoded=run(['ffmpeg','-v','error','-i',str(ogg),'-f','null','-'])
    if decoded.stderr.strip(): raise RuntimeError(decoded.stderr.decode(errors='replace'))
    probe=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)]).stdout)
    return {'wav':{'file':wav.name,'sha256':digest(wav)},'ogg':{'file':ogg.name,'sha256':digest(ogg),'probe':probe}}

def main():
    MOTHER.mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=OUT/'generation_manifest_take01.json'
    if manifest.exists():raise FileExistsError(manifest)
    records=[]
    for cue,stem,kind,seed,target,label in SPECS:
        ambient=cue.startswith('AMB')
        x=ambience(kind,seed) if ambient else foley(kind,seed)
        if ambient:
            gain=10**(target/20)/float(np.sqrt(np.mean(x.astype(np.float64)**2)))
        else:
            gain=10**(target/20)/float(np.max(np.abs(x)))
        x=(x*gain).astype(np.float32)
        r={'date':'2026-10-12','cue':cue,'label':label,'name':stem,'seed':seed,
           'status':'batch01 scene audition pending','method':'original procedural synthesis; no recorded source or external model',
           'duration_seconds':len(x)/RATE,'loop':ambient,'target_kind':'RMS dBFS' if ambient else 'sample peak dBFS',
           'target_dbfs':target,'sample_peak_dbfs':db(np.max(np.abs(x))),
           'rms_dbfs':db(np.sqrt(np.mean(x.astype(np.float64)**2))),
           'loop_boundary_pcm_step':float(np.max(np.abs(x[-1]-x[0]))) if ambient else None,
           'editable_source':Path(__file__).name,'editable_source_sha256':digest(Path(__file__)),
           'technical_check':'complete OGG decode without diagnostics',**export(stem,x)}
        save(OUT/(stem+'_take01.json'),r);records.append(r)
        print(f'Completed {stem}: {r["duration_seconds"]:.2f}s',flush=True)
    save(manifest,{'date':'2026-10-12','batch':'BATCH01_ARRIVAL_DAILY','candidates':records})

if __name__=='__main__':main()
