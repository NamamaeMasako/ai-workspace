"""Original short foley for the final battle and rescue, not dialogue voice-over.
Preserve all takes; requires numpy, scipy and ffmpeg.
"""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=ROOT/'02_素材/音訊/候選/BATCH07_TRUE_END'
spec=importlib.util.spec_from_file_location('foley_base',HERE.parent/'BATCH05_FOREST_BATTLE/produce_batch05_take01.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
RATE=base.RATE
SPECS=[
 ('SFX20_MAGIC_RIFT','magic_night_rift','magic',8020,1.16,-25,'夜色短暫撕開：暗色壓力、短裂響及收束氣流，非爆炸或音樂'),
 ('SFX32_COUGH_BLOOD','battle_cough_blood','battle',8032,.74,-26,'一次壓抑咳血近似：合成喉部粗糙氣流與短弱餘咳，無語句、無真人錄音及血肉濺聲'),
 ('SFX08_HERB_VARIANT','world_herb_crush','world',8108,.43,-26.5,'指間捏碎乾燥苦香的短纖維裂聲'),
 ('SFX31_HIT_VARIANT','battle_body_hit_dull','battle',8131,.39,-25,'肋側、手腕、膝蓋的低聲鈍響變體，不作骨裂或重爆點'),
 ('SFX18_HOLD_VARIANT','magic_black_card_pulse_hold','magic',8118,1.85,-27,'依已採用黑卡共鳴同頻率配比延長，準備撕卡時起、抓腕時中止；非循環心跳'),
]


def synth(stem,seed,duration):
    rng=np.random.default_rng(seed);n=round(duration*RATE);t=np.arange(n)/RATE;x=np.zeros(n)
    if stem=='magic_night_rift':
        env=np.sin(np.pi*np.clip((t-.025)/1.06,0,1))**1.8
        x+=.10*base.band(rng,n,90,700)*env
        x+=.025*base.band(rng,n,900,3900)*env
        base.put(x,.24,base.rub(rng,.085,1400,5800,1.1),.13)
        base.put(x,.28,base.modal(.62,[69,143,311],[1,.13,.025],[.11,.055,.025]),.09)
    elif stem=='battle_cough_blood':
        # Non-verbal synthetic approximation only; user listening decides realism.
        for at,length,g in [(.035,.235,.21),(.323,.175,.095)]:
            tt=np.arange(round(length*RATE))/RATE
            env=(1-np.exp(-tt/.003))*np.exp(-tt/.052)
            rough=base.band(rng,len(tt),340,3500)
            throat=base.band(rng,len(tt),120,730)
            gate=.66+.19*np.sin(2*np.pi*97*tt)+.10*np.sin(2*np.pi*143*tt)
            y=(rough*gate+.48*throat)*env
            base.put(x,at,base.edge(y,.0015,.035),g)
        base.put(x,.46,base.rub(rng,.17,180,1500,1.8),.007)
    elif stem=='world_herb_crush':
        for at,length,g in [(.025,.08,.13),(.081,.105,.16),(.152,.12,.10),(.229,.11,.05)]:
            base.put(x,at,base.rub(rng,length,800,6000,1.1),g)
        base.put(x,.03,base.rub(rng,.31,230,1700,1.6),.04)
    elif stem=='battle_body_hit_dull':
        tt=np.arange(round(.34*RATE))/RATE
        y=.42*base.band(rng,len(tt),75,330)*np.exp(-tt/.035)
        y+=.15*base.band(rng,len(tt),300,1500)*np.exp(-tt/.014)
        base.put(x,.02,base.edge(y,.0025,.045))
    else:
        env=np.sin(np.pi*np.clip((t-.035)/1.74,0,1))**1.6
        x+=(.25*np.sin(2*np.pi*132*t)+.055*np.sin(2*np.pi*197*t)+.018*np.sin(2*np.pi*281*t))*env
        x+=.009*base.band(rng,n,190,1400)*env
    return base.edge(x-np.mean(x),.006,.05)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'generation_manifest_take01.json').exists():raise FileExistsError('take01 already exists')
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
        r=dict(date='2026-10-19',cue=cue,name=stem,seed=seed,intention=intention,
               status='scene_audition_pending',formally_adopted=False,loop=False,
               method='original procedural synthesis; no external recordings or generative model; non-verbal cough approximation',
               duration_seconds=duration,target_peak_dbfs=peak,
               decoded_peak_dbfs=base.db(np.max(np.abs(pcm))),
               decoded_rms_dbfs=base.db(np.sqrt(np.mean(pcm.astype(float)**2))),
               editable_source=Path(__file__).name,source_sha256=base.digest(Path(__file__)),
               wav=dict(file=wav.name,sha256=base.digest(wav),sample_rate=RATE,bits=24,channels=1),
               ogg=dict(file=ogg.name,sha256=base.digest(ogg),sample_rate=44100,channels=1),
               game_file=target.relative_to(ROOT).as_posix())
        base.save(OUT/(stem+'_take01.json'),r);records.append(r)
    for r in records:shutil.copy2(OUT/r['ogg']['file'],ROOT/r['game_file'])
    base.save(OUT/'generation_manifest_take01.json',dict(date='2026-10-19',batch='BATCH07_TRUE_END',
              primary_cues=2,variants=3,files=5,candidates=records,
              pulse_formula_source='../BATCH03_TAVERN_CARD/produce_batch03_take01.py'))
    print(json.dumps([dict(name=r['name'],peak=r['decoded_peak_dbfs']) for r in records],ensure_ascii=False))


if __name__=='__main__':main()
