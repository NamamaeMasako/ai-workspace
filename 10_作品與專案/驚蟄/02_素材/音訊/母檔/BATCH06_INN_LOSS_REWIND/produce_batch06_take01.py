"""Original short foley for chapter 7 inn attack, loss and card rewind.
No external recordings, voice, music model or continuous ambience.
Keep all takes. Requires numpy, scipy and ffmpeg.
"""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT/'02_素材/音訊/候選/BATCH06_INN_LOSS_REWIND'
spec = importlib.util.spec_from_file_location('foley_base', HERE.parent/'BATCH05_FOREST_BATTLE/produce_batch05_take01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
RATE = base.RATE
SPECS = [
 ('SFX12_LAMP_DROP','world_lamp_drop','world',7012,.69,-23,'燈盞穩落木地板：短鈍接觸、燈架輕顫；沒有破裂或翻滾'),
 ('SFX19_CARD_TEAR','magic_black_card_tear','magic',7019,.78,-21,'厚卡片單次拉裂，短纖維斷裂與極淡尾響；不帶人聲或回退音樂'),
 ('SFX31_BODY_FALL','battle_body_fall_soft','battle',7031,.72,-24,'柔和人體落地：衣料先擦過，身體短悶觸地，沒有骨裂或血肉聲'),
 ('SFX06_FRAME_VARIANT','world_frame_thud_soft','world',7106,.36,-26,'木框推回的一聲輕悶響，與無聲抽屜搜尋分開'),
 ('SFX08_DRAG_VARIANT','world_cloth_drag_soft','world',7108,.79,-25,'衣料被短促拖動與掙動，不加入人聲或攻擊尖叫'),
 ('SFX08_CLOTH_VARIANT','world_cloth_soft','world',7208,.62,-29,'外衣蓋肩、抱起時柔軟衣料聲，低聲而短促'),
]


def synth(stem,seed,duration):
    rng=np.random.default_rng(seed); x=np.zeros(round(duration*RATE))
    if stem=='world_lamp_drop':
        y=base.modal(.56,[170,430,1180],[1,.16,.05],[.042,.028,.045])
        t=np.arange(len(y))/RATE
        y+=.12*base.band(rng,len(y),300,2400)*np.exp(-t/.018)
        base.put(x,.035,y)
        for at,g in [(.091,.025),(.151,.010)]:
            base.put(x,at,base.modal(.18,[1250,2640],[1,.19],[.025,.012]),g)
    elif stem=='magic_black_card_tear':
        base.put(x,.025,base.rub(rng,.105,550,3000,1.2),.11)
        for i,at in enumerate([.12,.151,.18,.214,.251,.284,.323,.366,.407,.449,.486]):
            dur=.025+.007*(i%3)
            base.put(x,at,base.rub(rng,dur,900,7700,1.05),.20 if i<5 else .14)
        base.put(x,.13,base.rub(rng,.40,180,2200,1.6),.08)
        base.put(x,.51,base.modal(.22,[213,497],[1,.09],[.035,.015]),.035)
    elif stem=='battle_body_fall_soft':
        base.put(x,.020,base.rub(rng,.32,180,2000,1.6),.11)
        t=np.arange(round(.47*RATE))/RATE
        y=.46*base.band(rng,len(t),45,210)*np.exp(-t/.059)
        y+=.22*base.band(rng,len(t),130,670)*np.exp(-t/.031)
        y+=.05*base.band(rng,len(t),600,1900)*np.exp(-t/.013)
        base.put(x,.13,base.edge(y,.006,.05))
    elif stem=='world_frame_thud_soft':
        base.put(x,.02,base.modal(.31,[139,296,712],[1,.27,.055],[.036,.019,.009]))
        base.put(x,.02,base.rub(rng,.037,350,1800,1.6),.07)
    elif stem=='world_cloth_drag_soft':
        for at,length,g in [(.02,.25,.16),(.17,.32,.22),(.47,.22,.12)]:
            base.put(x,at,base.rub(rng,length,170,2500,1.7),g)
    else:
        base.put(x,.025,base.rub(rng,.48,180,2200,1.5),.18)
    return base.edge(x-np.mean(x),.007,.055)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'generation_manifest_take01.json').exists(): raise FileExistsError('take01 already exists')
    records=[]
    for cue,stem,folder,seed,duration,peak,intention in SPECS:
        x=synth(stem,seed,duration);x*=10**(peak/20)/np.max(np.abs(x))
        wav=HERE/(stem+'_take01.wav');ogg=OUT/(stem+'_take01.ogg')
        subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','1','-i','-',
                        '-c:a','pcm_s24le',str(wav)],input=x.astype('<f4').tobytes(),check=True)
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','1',
                        '-c:a','libvorbis','-q:a','6',str(ogg)],check=True)
        pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(ogg),'-f','f32le','-']),dtype='<f4')
        target=ROOT/'03_開發/JingZhe/game/audio/sfx'/folder/(stem+'.ogg')
        if target.exists():raise FileExistsError(target)
        rec=dict(date='2026-10-19',cue=cue,name=stem,seed=seed,intention=intention,
                 status='scene_audition_pending',formally_adopted=False,loop=False,
                 method='original procedural synthesis; no external recordings, voice or model',
                 duration_seconds=duration,target_peak_dbfs=peak,
                 decoded_peak_dbfs=base.db(np.max(np.abs(pcm))),
                 decoded_rms_dbfs=base.db(np.sqrt(np.mean(pcm.astype(float)**2))),
                 editable_source=Path(__file__).name,source_sha256=base.digest(Path(__file__)),
                 wav=dict(file=wav.name,sha256=base.digest(wav),sample_rate=RATE,bits=24,channels=1),
                 ogg=dict(file=ogg.name,sha256=base.digest(ogg),sample_rate=44100,channels=1),
                 game_file=target.relative_to(ROOT).as_posix())
        base.save(OUT/(stem+'_take01.json'),rec);records.append(rec)
    for r in records:shutil.copy2(OUT/r['ogg']['file'],ROOT/r['game_file'])
    base.save(OUT/'generation_manifest_take01.json',dict(date='2026-10-19',batch='BATCH06_INN_LOSS_REWIND',
              primary_cues=3,variants=3,files=6,candidates=records))
    print(json.dumps([dict(name=r['name'],peak=r['decoded_peak_dbfs']) for r in records],ensure_ascii=False))


if __name__=='__main__':main()
