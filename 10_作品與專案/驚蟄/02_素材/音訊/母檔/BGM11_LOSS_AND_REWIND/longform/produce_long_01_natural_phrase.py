"""Reproduce BGM11 natural-tail long audition. Requires numpy, ffmpeg, ffprobe and an already running local ACE-Step API. Existing outputs are never overwritten."""
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
import uuid
from pathlib import Path
import numpy as np
FFMPEG='ffmpeg'
BASE='http://127.0.0.1:8001'
RATE=48000

def write_json(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def api(path,payload=None):
    request=urllib.request.Request(BASE+path,data=None if payload is None else json.dumps(payload).encode('utf-8'))
    if payload is not None: request.add_header('Content-Type','application/json')
    with urllib.request.urlopen(request,timeout=30) as response: envelope=json.load(response)
    if envelope.get('error') or envelope.get('code',200)!=200: raise RuntimeError(str(envelope))
    return envelope.get('data',envelope)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,sample_rate,channels','-of','json',str(path)]))

def wait_ready():
    for attempt in range(300):
        try:
            api('/health')
            return
        except (OSError,TimeoutError): time.sleep(3)
    raise TimeoutError('Local API startup')

def decode(path):
    data=subprocess.check_output([FFMPEG,'-v','error','-i',str(path),'-ar',str(RATE),'-ac','2','-f','f32le','-'])
    return np.frombuffer(data,dtype='<f4').reshape(-1,2)


ROOT = Path(__file__).resolve().parents[5]
CUE = ROOT / '02_素材/音訊/候選/BGM11_LOSS_AND_REWIND'
OUT = CUE / 'longform'
WAV = ROOT / '02_素材/音訊/母檔/BGM11_LOSS_AND_REWIND/longform'
NAME = ''
REFERENCE = None

def template(path):
    phrase = decode(NATURAL_LEVELED)[:round(21.75*RATE)].copy()
    reference = decode(REFERENCE)
    gain = float(np.sqrt(np.mean(reference[:18*RATE].astype(np.float64)**2)) / max(np.sqrt(np.mean(phrase[:18*RATE].astype(np.float64)**2)),1e-12))
    phrase *= gain
    period = round(21*RATE)
    overlap = len(phrase)-period
    signal = np.zeros((65*RATE,2),dtype=np.float32)
    starts=[]
    for offset in range(0,len(signal),period):
        chunk=phrase.copy()
        t=np.linspace(0,1,overlap,dtype=np.float32)
        weight=(t*t*(3-2*t))[:,None]
        if offset: chunk[:overlap]*=weight
        chunk[-overlap:] *= 1-weight
        length=min(len(chunk),len(signal)-offset)
        signal[offset:offset+length]+=chunk[:length]
        starts.append(offset/RATE)
    peak_gain=min(1.,10**(-2.5/20)/max(float(np.max(np.abs(signal))),1e-12))
    signal*=peak_gain
    subprocess.run([FFMPEG,'-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-','-c:a','pcm_f32le',str(path)],input=signal.astype('<f4').tobytes(),check=True)
    return {'duration_seconds':65,'phrase_starts_seconds':starts,'phrase_period_seconds':21,'source_excerpt_seconds':21.75,'overlap_seconds':.75,'source_level_match_db':float(20*np.log10(gain)),'peak_gain_db':float(20*np.log10(peak_gain)),'period_basis':'Unfaded BGM11 source tail: RMS at 20.0/20.5/21.0/21.5s is -24.2/-26.7/-33.0/-58.6 dBFS before mastering. Fixed 21s period with 0.75s overlap, not a measured beat alignment.'}

def assemble_natural(reference,generated,mother,audition):
    ref=decode(reference);natural=decode(NATURAL_LEVELED);raw=decode(generated)
    end=60*RATE
    assert len(raw)>=end and len(natural)>=round(21.75*RATE)
    rms=lambda x:float(np.sqrt(np.mean(x.astype(np.float64)**2)))
    natural_gain=rms(ref[:18*RATE])/max(rms(natural[:18*RATE]),1e-12)
    opening=natural*natural_gain
    opening[:18*RATE]=ref[:18*RATE]
    t=np.linspace(0,1,RATE,dtype=np.float32);w=(t*t*(3-2*t))[:,None]
    opening[18*RATE:19*RATE]=ref[18*RATE:19*RATE]*(1-w)+opening[18*RATE:19*RATE]*w
    start=round(20.5*RATE);finish=round(21.75*RATE)
    tail_gain=rms(ref[:18*RATE])/max(rms(raw[finish:end]),1e-12)
    tail_gain=min(tail_gain,10**(-16/20)/max(float(np.max(np.abs(raw[finish:end]))),1e-12))
    mixed=raw[:end].copy()*tail_gain
    mixed[:start]=opening[:start]
    t=np.linspace(0,1,finish-start,dtype=np.float32);w=(t*t*(3-2*t))[:,None]
    mixed[start:finish]=opening[start:finish]*(1-w)+raw[start:finish]*tail_gain*w
    mixed[-RATE//2:]*=np.linspace(1,0,RATE//2,dtype=np.float32)[:,None]
    master_gain=1.0
    mixed*=master_gain
    assert np.array_equal(mixed[:18*RATE],ref[:18*RATE]*master_gain)
    subprocess.run([FFMPEG,'-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-','-c:a','pcm_f32le',str(mother)],input=mixed.astype('<f4').tobytes(),check=True)
    subprocess.run([FFMPEG,'-v','error','-n','-i',str(mother),'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',str(audition)],check=True)
    return {'preserved_selected_short_opening_seconds':18,'natural_unfaded_handoff_interval_seconds':[18,19],'generated_continuation_crossfade_seconds':[20.5,21.75],'natural_source_gain_db':float(20*np.log10(natural_gain)),'continuation_gain_db':float(20*np.log10(tail_gain)),'uniform_master_gain_db':float(20*np.log10(master_gain)),'opening_pcm_verified_before_mastering':True,'fade_out_seconds':.5,'loop_processed':False,'method':'Carry unfaded mother tail through 20s and join at its natural ending, instead of repeating the faded audition clip.'}

def submit(request, source):
    boundary='codex-bgm09-'+uuid.uuid4().hex
    parts=[]
    for key,value in request.items():
        value=str(value).lower() if isinstance(value,bool) else str(value)
        parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n').encode())
    for field,path in [('reference_audio',REFERENCE),('src_audio',source)]:
        mime='audio/ogg' if path.suffix=='.ogg' else 'audio/wav'
        parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"; filename="{path.name}"\r\nContent-Type: {mime}\r\n\r\n').encode())
        parts.extend([path.read_bytes(),b'\r\n'])
    parts.append(f'--{boundary}--\r\n'.encode())
    req=urllib.request.Request(BASE+'/release_task',data=b''.join(parts),
                              headers={'Content-Type':f'multipart/form-data; boundary={boundary}'})
    with urllib.request.urlopen(req,timeout=60) as response:
        envelope=json.load(response)
    if envelope.get('error') or envelope.get('code',200)!=200:
        raise RuntimeError(str(envelope))
    return envelope['data']

def measure(path):
    result=subprocess.run([FFMPEG,'-hide_banner','-i',str(path),'-af',
        'silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
        '-f','null','-'],capture_output=True,text=True,encoding='utf-8',check=True)
    loudness,_=json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):])
    return {'integrated_lufs':loudness['input_i'],'true_peak_dbtp':loudness['input_tp'],
            'quiet_events':[line.strip() for line in result.stderr.splitlines() if 'silence_start:' in line or 'silence_end:' in line]}

def generate(number, slug, seed, label, detail):
    global NAME, REFERENCE, NATURAL_SOURCE, NATURAL_LEVELED
    NAME = f'long_01_natural_phrase_{slug}_seed{seed}'
    REFERENCE = CUE / f'candidate_{number:02d}_{slug}_seed{seed}_take03.ogg'
    NATURAL_SOURCE = WAV.parent / f'candidate_{number:02d}_{slug}_seed{seed}_take03_raw.wav'
    OUT.mkdir(exist_ok=True); WAV.mkdir(exist_ok=True)
    metadata=OUT/(NAME+'.json')
    if metadata.exists():
        raise FileExistsError(metadata)
    source=WAV/(NAME+'_source_template.wav')
    short=json.loads(REFERENCE.with_suffix('.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest()==short['ogg']['sha256']
    assert hashlib.sha256(NATURAL_SOURCE.read_bytes()).hexdigest()==short['raw_wav']['sha256']
    NATURAL_LEVELED=WAV/(NAME+'_unfaded_leveled_source.wav')
    selected_gain=short['processing']['fixed_gain_db']
    subprocess.run([FFMPEG,'-v','error','-n','-i',str(NATURAL_SOURCE),'-af',
        f'afade=t=in:st=0:d=0.03,volume={selected_gain:.5f}dB,alimiter=limit=0.158489:attack=10:release=150:level=0:latency=1,asetpts=N/SR/TB',
        '-ar','48000','-ac','2','-c:a','pcm_f32le',str(NATURAL_LEVELED)],check=True)
    assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest()==short['ogg']['sha256']
    assert hashlib.sha256(NATURAL_SOURCE.read_bytes()).hexdigest()==short['raw_wav']['sha256']
    request=dict(short['request'])
    request.update(task_type='cover',audio_duration=65,audio_cover_strength=1.,cover_noise_strength=.55)
    request['prompt'] += (' Extend this exact selected original short faithfully into a continuous 65-second cue. '
        'Keep its piano and cello interplay, quiet three-note plea, unsettled internal movement, '
        'soft attacks and unresolved harmonic pain. The 76 BPM value is a prompt, not a measured tempo. '
        'Maintain the immediate shock of sudden death, refusing to accept it and trying helplessly to reach her. '
        'Preserve this emotional state through the full cue with small phrase variations, without '
        'developing into ceremonial mourning, a warm memory, a hopeful recovery or a large climax. '
        'The supplied source map uses the unfaded original note tail. Continue connected musical tension '
        'under the hesitant questions; no long silent middle, no early fade, no added drums or sound effects. ' + detail)
    record={'date':'2026-10-16','cue':'BGM11_LOSS_AND_REWIND','label':label,
            'status':'awaiting user long audition','formally_adopted':False,'game_integrated':False,'request':request,
            'reference':{'file':REFERENCE.name,'sha256':hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
                         'submission_method':'multipart reference_audio upload'},
            'natural_source':{'file':NATURAL_SOURCE.name,'sha256':hashlib.sha256(NATURAL_SOURCE.read_bytes()).hexdigest()},
            'source_template':{'file':source.name,'structure':template(source),
                               'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},
            'review_basis':'User selected take03 candidate 04. Actual selected OGG is uploaded as reference_audio; corresponding unfaded raw mother supplies src_audio, not a repeated faded preview.',
            'leveled_source':{'file':NATURAL_LEVELED.name,'sha256':hashlib.sha256(NATURAL_LEVELED.read_bytes()).hexdigest(),'same_short_gain_db':selected_gain,'limiter_dbfs':-16}}
    write_json(metadata,record)
    wait_ready()
    record['task']=submit(request,source); write_json(metadata,record)
    print('Submitted '+label,flush=True)
    started=time.monotonic()
    while time.monotonic()-started<1200:
        state=api('/query_result',{'task_id_list':[record['task']['task_id']]})[0]
        if state['status']==2:
            raise RuntimeError(str(state))
        if state['status']==1:
            results=state['result']; results=json.loads(results) if isinstance(results,str) else results
            if len(results)!=1: raise RuntimeError('Expected one output')
            record['result']=results[0]; break
        time.sleep(5)
    else: raise TimeoutError(record['task']['task_id'])
    url=record['result']['file']; url=BASE+url if url.startswith('/') else url
    if not url.startswith(BASE+'/'): raise RuntimeError('Not local output')
    raw=WAV/(NAME+'_raw.wav')
    with urllib.request.urlopen(url,timeout=60) as response,raw.open('xb') as target:
        shutil.copyfileobj(response,target)
    premaster=WAV/(NAME+'_premaster.wav'); preogg=OUT/(NAME+'_premaster.ogg')
    record['processing']=assemble_natural(REFERENCE,raw,premaster,preogg)
    before=measure(preogg); gain=0.0
    mother=WAV/(NAME+'.wav'); audition=OUT/(NAME+'.ogg')
    subprocess.run([FFMPEG,'-v','error','-n','-i',str(premaster),'-af',
        'asetpts=N/SR/TB',
        '-t','60','-ar','48000','-ac','2','-c:a','pcm_f32le',str(mother)],check=True)
    subprocess.run([FFMPEG,'-v','error','-n','-i',str(mother),'-t','60','-ar','44100',
        '-ac','2','-c:a','libvorbis','-q:a','5',str(audition)],check=True)
    record['processing']['audition_mastering']={'fixed_gain_db':gain,'limiter_dbfs':None,'continuation_peak_ceiling_dbfs':-16,'preserve_selected_short_level':True,
        'latency_compensation':True,'timestamps_rebuilt':True,'composition_changed':False,'premaster_measurement':before}
    for key,path,duration in [('source_wav',source,65),('raw_wav',raw,65),
        ('premaster_wav',premaster,60),('premaster_ogg',preogg,60),('assembled_wav',mother,60),('ogg',audition,60)]:
        info=probe(path)
        if abs(float(info['format']['duration'])-duration)>.1: raise RuntimeError(f'Bad duration {path}')
        decoded=subprocess.run([FFMPEG,'-v','error','-i',str(path),'-f','null','-'],capture_output=True,text=True,encoding='utf-8',check=True)
        if decoded.stderr.strip(): raise RuntimeError('Decode diagnostics '+str(path)+': '+decoded.stderr)
        record[key]={'file':path.name,'probe':info,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    record['technical_check']={'decode':'passed',**measure(audition)}
    write_json(metadata,record)
    write_json(OUT/(NAME+'_manifest.json'),{'date':'2026-10-16','cue':record['cue'],'candidates':[record]})
    write_json(OUT/(NAME+'_technical_check.json'),record['technical_check'])
    print(json.dumps(record['technical_check'],ensure_ascii=False),flush=True)
    print('Finished '+str(audition),flush=True)
    return record

def main():
    record=generate(4,'cello_piano_plea',3824,'還不能放手・長版','Keep the quiet plea and helpless refusal emotionally consistent through the continuation.')
    write_json(OUT/'generation_manifest_long_01.json',{'date':'2026-10-16','cue':'BGM11_LOSS_AND_REWIND','candidates':[record]})
    write_json(OUT/'technical_measurements_long_01.json',{'date':'2026-10-16','files':[{'file':record['ogg']['file'],**record['technical_check']}]})

if __name__=='__main__': main()
