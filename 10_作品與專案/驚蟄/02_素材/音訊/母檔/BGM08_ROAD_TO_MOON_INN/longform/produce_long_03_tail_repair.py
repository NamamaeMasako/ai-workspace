from pathlib import Path
import hashlib,json,re,subprocess
import numpy as np
BASE=Path(__file__).resolve().parent
CAND=BASE.parents[2]/'候選/BGM08_ROAD_TO_MOON_INN/longform'
NAME='long_03_tail_repair_gentle_guzheng_seed3502_loop_intro'
source=BASE/'long_02_tail_repair_gentle_guzheng_seed3502_loop_intro.wav'
tail=BASE.parent/'candidate_02_gentle_guzheng_seed3502_take01.wav'
wav=BASE/(NAME+'.wav');ogg=CAND/(NAME+'.ogg')
assert not any(p.exists() for p in [wav,ogg,CAND/(NAME+'.json')])
RATE=48000

def decode(p):
    x=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar',str(RATE),'-ac','2','-f','f32le','-'])
    return np.frombuffer(x,dtype='<f4').reshape(-1,2).copy()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=decode(source);natural=decode(tail);edited=original.copy()
a,b,c,d=[round(t*RATE) for t in (19.3,19.55,21.2,21.5)]
ma,mb=[round(t*RATE) for t in (19.52,19.72)]
rms=lambda x:float(np.sqrt(np.mean(x.astype(np.float64)**2)))
mask=np.zeros(len(edited),dtype=bool); patches=[]
for shift_seconds in [19,38]:
    shift=shift_seconds*RATE
    gain=rms(original[ma+shift:mb+shift])/max(rms(natural[ma:mb]),1e-12)
    gain=min(gain,10**(-2.5/20)/max(float(np.max(np.abs(natural[a:d]))),1e-12))
    weight=np.ones((d-a,1),dtype=np.float32)
    for left,right,incoming in [(a,b,True),(c,d,False)]:
        t=np.linspace(0,1,right-left,dtype=np.float32);curve=t*t*(3-2*t)
        weight[left-a:right-a,0]=curve if incoming else 1-curve
    edited[a+shift:d+shift]=original[a+shift:d+shift]*(1-weight)+natural[a:d]*gain*weight
    mask[a+shift:d+shift]=True
    patches.append({'changed_interval_seconds':[19.3+shift_seconds,21.5+shift_seconds],'natural_source_interval_seconds':[19.3,21.5],'fade_in_interval_seconds':[19.3+shift_seconds,19.55+shift_seconds],'fade_out_interval_seconds':[21.2+shift_seconds,21.5+shift_seconds],'tail_gain_db':float(20*np.log10(gain)),'gain_match_interval_seconds':[19.52+shift_seconds,19.72+shift_seconds]})
assert np.array_equal(edited[~mask],original[~mask])
assert np.array_equal(edited[round(19.3*RATE):round(21.5*RATE)],original[round(19.3*RATE):round(21.5*RATE)])
assert np.array_equal(edited[-RATE//2:],original[-RATE//2:])
subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-','-c:a','pcm_f32le',str(wav)],input=edited.astype('<f4').tobytes(),check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',str(ogg)],check=True)
clips={}
for label,p in [('before',source),('after',wav)]:
    clip=CAND/(NAME+f'_detail_{label}_35to45.ogg')
    subprocess.run(['ffmpeg','-v','error','-n','-ss','35','-i',str(p),'-t','10','-af','afade=t=in:st=0:d=0.03,afade=t=out:st=9.85:d=0.15','-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',str(clip)],check=True)
    clips[label]={'file':clip.name,'sha256':digest(clip),'original_time_seconds':[35,45]}
qa_log=subprocess.run(['ffmpeg','-hide_banner','-i',str(ogg),'-af','silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,check=True).stderr.decode('utf-8',errors='replace')
stats=json.loads(qa_log[qa_log.rfind('{'):qa_log.rfind('}')+1])
qa={'integrated_lufs':stats['input_i'],'true_peak_dbtp':stats['input_tp'],'silence_intervals':re.findall(r'silence_(?:start|end):[^\r\n]*',qa_log)}
for p in [wav,ogg]+[CAND/v['file'] for v in clips.values()]:
    decoded=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,check=True)
    if decoded.stderr.strip():raise RuntimeError(decoded.stderr.decode(errors='replace'))
qa['decode']='passed without diagnostics'
energy={}
for t in [39.,58.]:
    i,j=[round(v*RATE) for v in [t,t+.25]]
    energy[str(t)]={'window_seconds':.25,'before_dbfs':20*np.log10(max(rms(original[i:j]),1e-12)),'after_dbfs':20*np.log10(max(rms(edited[i:j]),1e-12))}
r={'date':'2026-10-13','cue':'BGM08_ROAD_TO_MOON_INN','status':'long_03 awaiting user audition; deployed game remains long_01','user_feedback':'The corrected version still has the same short release around 39 seconds; try again','source':{'file':source.name,'sha256':digest(source)},'natural_tail_source':{'file':tail.name,'sha256':digest(tail)},'processing':{'new_generation':False,'method':'Restore the unfaded original phrase tail at the later two 19-second template recurrences, inheriting the earlier 20-second repair','patches':patches,'crossfade_curve':'smoothstep convex','outside_patches_pcm_max_error':float(np.max(np.abs(edited[~mask]-original[~mask]))),'previous_20_second_repair_pcm_max_error':0.0,'last_half_second_pcm_max_error':0.0,'loop_inherited':True,'renpy_loop_start_seconds':3.,'repeat_period_seconds':57,'first_duration_seconds':60,'game_integrated':False},'diagnostic_energy':energy,'wav':{'file':wav.name,'sha256':digest(wav)},'ogg':{'file':ogg.name,'sha256':digest(ogg),'probe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)]))},'detail_clips':clips,'technical_check':qa,'producer':{'file':Path(__file__).name,'sha256':digest(Path(__file__))}}
(CAND/(NAME+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'patches':patches,'qa':qa,'energy':energy},ensure_ascii=False))
