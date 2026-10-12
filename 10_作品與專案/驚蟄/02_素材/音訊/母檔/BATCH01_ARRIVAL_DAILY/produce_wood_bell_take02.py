"""Five irregular, fading wood-bell strikes caused by a moving door."""
from pathlib import Path
import json, hashlib, subprocess
import numpy as np
from produce_batch01_take01 import RATE, modal, band, edge, put, run, digest

ROOT=Path(__file__).resolve().parents[4]
MOTHER=ROOT/'02_素材/音訊/母檔/BATCH01_ARRIVAL_DAILY'
OUT=ROOT/'02_素材/音訊/候選/BATCH01_ARRIVAL_DAILY'
STEM='world_wood_bell_take02'

def main():
    wav=MOTHER/(STEM+'.wav'); ogg=OUT/(STEM+'.ogg')
    if wav.exists() or ogg.exists():raise FileExistsError(STEM)
    rng=np.random.default_rng(5303)
    pcm=np.zeros(round(1.55*RATE),dtype=np.float32)
    strikes=[(0.,1.),(.19,.86),(.43,.63),(.74,.40),(1.04,.23)]
    for at,gain in strikes:
        ratio=rng.uniform(.983,1.016)
        tone=modal(.48,[820*ratio,1345*ratio,2170*ratio],
                   [1,.31,.09],[.085,.042,.019])
        t=np.arange(len(tone))/RATE
        tone += .045*band(rng,len(tone),900,5200)*np.exp(-t/.006)
        put(pcm,at,edge(tone,.0015,.04),gain)
    pcm=edge(pcm,.002,.035)
    pcm *= 10**(-14/20)/np.max(np.abs(pcm))
    run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','1','-i','-',
         '-c:a','pcm_s24le',str(wav)],input=pcm.astype('<f4').tobytes())
    run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','1',
         '-c:a','libvorbis','-q:a','6',str(ogg)])
    decoded=run(['ffmpeg','-v','error','-i',str(ogg),'-f','null','-'])
    if decoded.stderr.strip():raise RuntimeError(decoded.stderr.decode(errors='replace'))
    probe=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)]).stdout)
    record={'date':'2026-10-12','cue':'SFX03_WOOD_BELL','label':'門扇帶動的五下漸弱木鈴',
            'name':STEM,'seed':5303,'status':'batch01 revision pending scene audition',
            'method':'original procedural modal synthesis; five irregular fading impacts',
            'duration_seconds':len(pcm)/RATE,'loop':False,
            'strike_starts_seconds':[x[0] for x in strikes],
            'strike_relative_gains':[x[1] for x in strikes],
            'sample_peak_dbfs':-14,'rms_dbfs':float(20*np.log10(np.sqrt(np.mean(pcm.astype(np.float64)**2)))),
            'source_files':[{'file':Path(__file__).name,'sha256':digest(Path(__file__))},
                            {'file':'produce_batch01_take01.py','sha256':digest(MOTHER/'produce_batch01_take01.py')}],
            'wav':{'file':wav.name,'sha256':digest(wav)},
            'ogg':{'file':ogg.name,'sha256':digest(ogg),'probe':probe},
            'technical_check':'complete decode without diagnostics',
            'user_feedback':'木鈴不要只有一聲，太不明顯，實際上的門鈴也部會只響一聲'}
    (OUT/(STEM+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Completed five-strike wood bell: 1.55 seconds, peak -14 dBFS')

if __name__=='__main__':main()
