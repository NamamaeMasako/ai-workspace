from pathlib import Path
import hashlib,json,re,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[5]
WAV=Path(__file__).resolve().parent
OUT=ROOT/'02_素材/音訊/候選/BGM10_INN_HUNTED/longform'
NAME='long_01_natural_phrase_piano_dark_pulse_seed3714_loop_intro'
source=WAV/'long_01_natural_phrase_piano_dark_pulse_seed3714.wav'
wav=WAV/(NAME+'.wav');ogg=OUT/(NAME+'.ogg')
assert not any(p.exists() for p in (wav,ogg,OUT/(NAME+'.json')))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ar','48000','-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2)
pcm=original.copy();overlap=3*48000
phase=np.linspace(0,1,overlap,dtype=np.float32);weight=(phase*phase*(3-2*phase))[:,None]
pcm[-overlap:]=pcm[-overlap:]*(1-weight)+pcm[:overlap]*weight
assert np.array_equal(pcm[:-overlap],original[:-overlap])
subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_f32le',str(wav)],input=pcm.astype('<f4').tobytes(),check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',str(ogg)],check=True)
decoded=subprocess.run(['ffmpeg','-v','error','-i',str(ogg),'-f','null','-'],capture_output=True,check=True)
if decoded.stderr.strip():raise RuntimeError(decoded.stderr.decode(errors='replace'))
qa_log=subprocess.run(['ffmpeg','-hide_banner','-i',str(ogg),'-af','silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,check=True).stderr.decode('utf-8',errors='replace')
stats=json.loads(qa_log[qa_log.rfind('{'):qa_log.rfind('}')+1])
r={'date':'2026-10-16','cue':'BGM10_INN_HUNTED','status':'selected for game audition; scene and loop confirmation pending','user_instruction':'套進遊戲試試','source':{'file':source.name,'sha256':digest(source)},'processing':{'new_generation':False,'unchanged_opening_seconds':57,'tail_crossfade_seconds':3,'crossfade_curve':'smoothstep convex','duration_seconds':60,'renpy_loop_start_seconds':3.0,'repeat_period_seconds':57,'period_basis':'Three-second crossfade selected to preserve the first 57 seconds of the audition; no measured beat alignment is claimed.','unchanged_opening_pcm_max_error':float(np.max(np.abs(pcm[:-overlap]-original[:-overlap]))),'pcm_boundary_step':float(np.max(np.abs(pcm[-1]-pcm[overlap])))},'wav':{'file':wav.name,'sha256':digest(wav)},'ogg':{'file':ogg.name,'sha256':digest(ogg),'probe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,sample_rate,channels:format=duration','-of','json',str(ogg)]))},'technical_check':{'decode':'passed without diagnostics','integrated_lufs':stats['input_i'],'true_peak_dbtp':stats['input_tp'],'quiet_events':re.findall(r'silence_(?:start|end):[^\r\n]*',qa_log)},'producer':{'file':Path(__file__).name,'sha256':digest(Path(__file__))}}
(OUT/(NAME+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sha256':r['ogg']['sha256'],'qa':r['technical_check']}))
