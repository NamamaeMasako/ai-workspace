"""Original procedural short foley for chapter 7 forest battles. Requires numpy, scipy and ffmpeg.
Preserve existing takes. No external recording, voice or generative model is used.
"""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parents[4]
MOTHER=Path(__file__).resolve().parent
OUT=ROOT/'02_素材/音訊/候選/BATCH05_FOREST_BATTLE'
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
 ('SFX05_FOOTSTEP_WET','world_footstep_wet','wet',6005,1.62,-22,'林道短段濕葉泥地行走，非循環雨聲'),
 ('SFX21_INSECT_SUMMON','magic_insect_summon','summon',6021,1.72,-20.5,'式神召喚的短促暗色匯聚與離散蟲翼，無人聲或音樂'),
 ('SFX23_SILK_CUT','battle_silk_cut','cut',6023,.48,-21,'細絲繃緊後切斷的短裂聲，非血肉音'),
 ('SFX25_TSUCHIGUMO_HISS','battle_tsuchigumo_hiss','hiss',6025,.86,-23,'土蜘蛛短嘶聲，以氣流與甲殼顫動合成，不使用人聲'),
 ('SFX26_NAGINATA_WHOOSH','battle_naginata_whoosh','whoosh',6026,.50,-20,'薙刀長刃揮過的短氣流'),
 ('SFX27_NAGINATA_HIT','battle_naginata_armor_hit','hit',6027,.59,-18.5,'薙刀命中甲殼，短硬殼撞擊，非血肉濺聲'),
 ('SFX28_KAMIKIRI_BLADES','battle_kamikiri_blades','blades',6028,.70,-19.5,'髮切兩道鐮刃交錯與短刃風'),
 ('SFX29_OMUKADE_ARMOR','battle_omukade_armor_move','armor',6029,.86,-21.5,'大百足厚重甲片移動與蓄力'),
 ('SFX30_OMUKADE_IMPACT','battle_omukade_impact','impact',6030,.88,-18.5,'大百足撞擊的低沉甲殼衝量；可低音量共用於土蜘蛛倒下'),
 ('SFX24_SPIDER_STEPS','battle_spider_steps_heavy','heavy',6124,1.04,-21,'交戰時巨大土蜘蛛兩次節肢落地變體，與門縫小蛛腳分開'),
 ('SFX14_KISERU_DRAW','magic_kiseru_blow','blow',6114,.76,-25,'吹起已燃煙草的短氣流變體，與吸菸分開'),
]

def synth(kind,seed,duration):
    rng=np.random.default_rng(seed); n=round(duration*RATE); t=np.arange(n)/RATE; x=np.zeros(n)
    if kind=='wet':
        for at,g in [(.035,.70),(.52,.85),(1.02,.73)]:
            y=modal(.30,[85,160,305],[1,.30,.035],[.065,.035,.018]);tt=np.arange(len(y))/RATE
            y+=.065*band(rng,len(y),180,2600)*np.exp(-tt/.065)
            put(x,at,edge(y,.012,.05),g)
            put(x,at+.025,rub(rng,.24,550,4200,1.5),.055*g)
    elif kind=='summon':
        env=np.sin(np.pi*np.clip((t-.035)/1.52,0,1))**1.8
        x+=(.20*np.sin(2*np.pi*(99*t+11*t*t))+.05*np.sin(2*np.pi*(151*t+5*t*t)))*env
        x+=.045*band(rng,n,500,4200)*env
        for at in [.17,.32,.56,.81,1.02]:put(x,at,rub(rng,.16,1200,5100,1.8),.025)
    elif kind=='cut':
        put(x,.025,rub(rng,.18,950,5500,1.5),.10)
        put(x,.17,modal(.25,[790,1610,2810],[1,.17,.025],[.018,.009,.004]),.13)
        put(x,.165,rub(rng,.045,1800,7200,1.3),.055)
    elif kind=='hiss':
        env=np.sin(np.pi*np.clip((t-.035)/.72,0,1))**1.5
        x+=.13*band(rng,n,650,4700)*env*(.80+.12*np.sin(2*np.pi*44*t))
        x+=.025*band(rng,n,180,1200)*env
    elif kind=='whoosh':
        y=rub(rng,.40,160,4100,1.5);tt=np.arange(len(y))/RATE
        y*=.85+.10*np.sin(2*np.pi*19*tt)
        put(x,.025,y,.16)
    elif kind in ('hit','impact','heavy'):
        times=[.03,.49] if kind=='heavy' else [.035]
        for i,at in enumerate(times):
            if kind=='hit':f=[230,605,1420];d=[.060,.035,.017];gain=.24
            elif kind=='impact':f=[57,113,246];d=[.14,.085,.040];gain=.34
            else:f=[66,142,302];d=[.10,.065,.028];gain=.24 if i==0 else .19
            y=modal(.45,f,[1,.33,.07],d);tt=np.arange(len(y))/RATE
            y+=.07*band(rng,len(y),250,3300)*np.exp(-tt/(.035 if kind=='hit' else .065))
            put(x,at,edge(y,.006,.06),gain)
            put(x,at+.035,rub(rng,.16,450,3500,1.6),.025)
    elif kind=='blades':
        for at,g in [(.035,.13),(.275,.11)]:
            put(x,at,rub(rng,.17,450,4500,1.5),g)
            put(x,at+.075,modal(.27,[720,1530,2780],[1,.20,.025],[.032,.018,.008]),g*.60)
    elif kind=='armor':
        for at,length,g in [(.035,.22,.13),(.30,.24,.16),(.59,.15,.10)]:
            put(x,at,rub(rng,length,180,2400,1.4),g)
            put(x,at+.055,modal(.19,[143,340,770],[1,.28,.045],[.040,.024,.012]),g*.5)
    elif kind=='blow':
        env=np.sin(np.pi*np.clip((t-.025)/.65,0,1))**1.5
        x+=.12*band(rng,n,250,2600)*env
        put(x,.32,modal(.08,[1050,2100],[1,.08],[.004,.002]),.007)
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
        r=dict(date='2026-10-19',cue=cue,label=label,name=stem,seed=seed,status='batch05 complete scene audition pending',
            formally_adopted=False,method='original procedural short foley; no recording, external library, voice or model',
            duration_seconds=len(x)/RATE,loop=False,target_sample_peak_dbfs=peak,
            editable_source=Path(__file__).name,editable_source_sha256=digest(Path(__file__)),**export(stem,x))
        save(OUT/(stem+'_take01.json'),r);records.append(r);print('Completed '+stem,flush=True)
    save(manifest,dict(date='2026-10-19',batch='BATCH05_FOREST_BATTLE',primary_cues=9,files=11,candidates=records))

if __name__=='__main__':main()
