from pathlib import Path
import hashlib,json,re,subprocess
import numpy as np
BASE=Path(__file__).resolve().parent
CAND=BASE.parents[2]/'候選/BGM08_ROAD_TO_MOON_INN/longform'
NAME='long_02_tail_repair_gentle_guzheng_seed3502_loop_intro'
source=BASE/'long_01_phrase_guided_gentle_guzheng_seed3502_loop_intro.wav'
tail=BASE.parent/'candidate_02_gentle_guzheng_seed3502_take01.wav'
wav=BASE/(NAME+'.wav'); ogg=CAND/(NAME+'.ogg')
assert not any(p.exists() for p in (wav,ogg,CAND/(NAME+'.json')))
RATE=48000

def decode(p):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar',str(RATE),'-ac','2','-f','f32le','-'])
    return np.frombuffer(data,dtype='<f4').reshape(-1,2).copy()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=decode(source); natural=decode(tail); edited=original.copy()
a,b,c,d=[round(t*RATE) for t in (19.3,19.55,21.2,21.5)]
match_a,match_b=[round(t*RATE) for t in (19.52,19.72)]
rms=lambda x:float(np.sqrt(np.mean(x.astype(np.float64)**2)))
gain=rms(original[match_a:match_b])/max(rms(natural[match_a:match_b]),1e-12)
peak=float(np.max(np.abs(natural[a:d])))
gain=min(gain,10**(-2.5/20)/max(peak,1e-12))
weight=np.ones((d-a,1),dtype=np.float32)
for left,right,incoming in [(a,b,True),(c,d,False)]:
    t=np.linspace(0,1,right-left,dtype=np.float32)
    curve=t*t*(3-2*t)
    weight[left-a:right-a,0]=curve if incoming else 1-curve
edited[a:d]=original[a:d]*(1-weight)+natural[a:d]*gain*weight
assert np.array_equal(edited[:a],original[:a]) and np.array_equal(edited[d:],original[d:])
subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-','-c:a','pcm_f32le',str(wav)],input=edited.astype('<f4').tobytes(),check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',str(ogg)],check=True)
clips={}
for label,p in [('before',source),('after',wav)]:
    clip=CAND/(NAME+f'_detail_{label}_15to25.ogg')
    subprocess.run(['ffmpeg','-v','error','-n','-ss','15','-i',str(p),'-t','10','-af','afade=t=in:st=0:d=0.03,afade=t=out:st=9.85:d=0.15','-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',str(clip)],check=True)
    clips[label]={'file':clip.name,'sha256':digest(clip),'original_time_seconds':[15,25]}
measure=subprocess.run(['ffmpeg','-hide_banner','-i',str(ogg),'-af','silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,check=True).stderr.decode('utf-8',errors='replace')
stats=json.loads(measure[measure.rfind('{'):measure.rfind('}')+1])
qa={'integrated_lufs':stats['input_i'],'true_peak_dbtp':stats['input_tp'],'silence_intervals':re.findall(r'silence_(?:start|end):[^\r\n]*',measure)}
for p in [wav,ogg]+[CAND/v['file'] for v in clips.values()]:
    decoded=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,check=True)
    if decoded.stderr.strip():raise RuntimeError(decoded.stderr.decode(errors='replace'))
qa['decode']='passed without diagnostics'
r={'date':'2026-10-13','cue':'BGM08_ROAD_TO_MOON_INN','status':'revision awaiting user audition; game remains on long_01','user_feedback':'Around 20 seconds a note sounds cut short and uncomfortable; try one correction','source':{'file':source.name,'sha256':digest(source)},'natural_tail_source':{'file':tail.name,'sha256':digest(tail)},'processing':{'new_generation':False,'method':'Restore the original unfaded source phrase tail in a local patch; no tempo change, pitch shift, synthetic reverb or new instruments','changed_interval_seconds':[19.3,21.5],'fade_in_interval_seconds':[19.3,19.55],'fade_out_interval_seconds':[21.2,21.5],'crossfade_curve':'smoothstep convex','tail_gain_db':float(20*np.log10(gain)),'gain_match_interval_seconds':[19.52,19.72],'outside_patch_pcm_max_error':float(max(np.max(np.abs(edited[:a]-original[:a])),np.max(np.abs(edited[d:]-original[d:])))),'loop_inherited_from_long_01':True,'renpy_loop_start_seconds':3.0,'repeat_period_seconds':57,'first_duration_seconds':60,'game_integrated':False},'wav':{'file':wav.name,'sha256':digest(wav)},'ogg':{'file':ogg.name,'sha256':digest(ogg),'probe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)]))},'detail_clips':clips,'technical_check':qa}
(CAND/(NAME+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'processing':r['processing'],'qa':qa},ensure_ascii=False))
