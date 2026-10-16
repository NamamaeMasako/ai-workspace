"""Produce four critical injury and rescue BGM13 auditions without external audio with the local ACE-Step API; keep raw sources."""
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTHERS = Path(__file__).resolve().parent
OUT = ROOT / '02_素材/音訊/候選/BGM13_HOLD_ON'
BASE = 'http://127.0.0.1:8001'
DATE = '2026-10-16'

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def api(path, payload=None):
    req = urllib.request.Request(BASE+path, data=None if payload is None else json.dumps(payload).encode(),
                                 headers={} if payload is None else {'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=45) as response:
        envelope = json.load(response)
    if envelope.get('error') or envelope.get('code',200) != 200:
        raise RuntimeError(str(envelope))
    return envelope.get('data',envelope)

def ff(*args):
    return subprocess.run(['ffmpeg', *map(str,args)], capture_output=True, text=True, encoding='utf-8', check=True)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_name,sample_rate,channels','-of','json',str(path)]))

def measure(path):
    report = ff('-hide_banner','-i',path,'-af',
        'silencedetect=n=-45dB:d=0.5,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-').stderr
    data,_ = json.JSONDecoder().raw_decode(report[report.rfind('{'):])
    return {'integrated_lufs':data['input_i'],'true_peak_dbtp':data['input_tp'],
            'quiet_events':[line.strip() for line in report.splitlines() if 'silence_start:' in line or 'silence_end:' in line]}

COMMON = ('Original instrumental dramatic underscore for a dark fantasy visual novel, 25 seconds. '
    'After battle the protagonist is critically wounded, losing blood and struggling to remain conscious. '
    'His two companions arrive, terrified of losing him, trying to keep him here. '
    'One tries to tear a protective card to save him; he weakly stops her because he refuses another reset. '
    'He is still alive, very fragile and in danger. Exhaustion, pain, restrained urgency and human closeness. '
    'The music holds a thin thread of life: aching suspended minor harmony, a faltering small motif '
    'that keeps trying to answer, a quiet hesitant musical pulse with gentle forward tension. '
    'Small low-to-middle register ensemble, very soft attacks, controlled dynamics, sustained connected '
    'resonance beneath sparse phrases. A fragile possibility of rescue remains unresolved. '
    'Keep wounded vulnerability and danger present from the opening, without announcing death or recovery. '
    'Continuous quiet musical presence for all 25 seconds, natural note tails, no long silent middle. '
    'No funeral march, settled bereavement, warm nostalgic farewell, comforting daily-life mood, '
    'graduation song, sweet romantic melody, major-key hopeful lift, relaxed swaying accompaniment, '
    'heroic climax, battle drums, horror stings or early ending. '
    'Only instrumental music: no voice, choir, literal breathing or heartbeat effects, rain, wind or other sounds. ')

DIRECTIONS = [
    (1,'piano_cello_fading',4001,'還有一口氣',56,
     'Low soft piano and restrained cello, a short wavering two-note question hangs against '
     'a suspended minor chord. The cello keeps a thin sustained line alive under uneven piano '
     'returns. Delicate physical weakness and aching urgency, no flowing arpeggios or broad elegy.'),
    (2,'strings_hold_on',4002,'別閉上眼',62,
     'Small muted viola and cello ensemble, a quiet measured bowed figure falters but keeps '
     'returning. Close unresolved suspensions and a fragile rising answer over slow low harmony. '
     'Intimate anxious insistence, trying to hold someone here, no sweeping mourning solo or epic strings.'),
    (3,'bass_clarinet_piano',4003,'聲音還在',58,
     'Low bass clarinet and sparse soft piano, restrained short phrases lose strength before '
     'finishing, while a very quiet low piano anchor continues underneath. Minor-second appoggiaturas '
     'and an occasional tentative answering note suggest companions still reaching him. '
     'Dark fragile intimacy, no jazz lilt, lyrical ballad or comforting cadence.'),
    (4,'piano_viola_thread',4004,'留住這一刻',66,
     'Soft middle-register piano with a thin viola line, a hesitant compact motif repeats '
     'with slightly changed spacing above sustained minor suspensions. The melody reaches '
     'toward one small open interval then holds unresolved, a tenuous chance of survival. '
     'Quiet restrained tension and vulnerability, no bright high notes, sweet accompaniment or joyful resolution.'),
]

def produce(spec):
    number,slug,seed,label,bpm,detail = spec
    stem=f'candidate_{number:02d}_{slug}_seed{seed}_take01'
    record_path=OUT/(stem+'.json')
    if record_path.exists():
        raise FileExistsError(record_path)
    request=dict(prompt=detail+' '+COMMON, lyrics='[Instrumental]', thinking=False,
        use_format=False,use_cot_caption=False,use_cot_language=False,bpm=bpm,
        key_scale='E minor',time_signature='4',vocal_language='unknown',audio_duration=25,
        inference_steps=8,batch_size=1,use_random_seed=False,seed=seed,model='acestep-v15-turbo',
        task_type='text2music',audio_cover_strength=1.0,audio_format='wav')
    record=dict(date=DATE,cue='BGM13_HOLD_ON',label=label,revision='take01',
        status='awaiting user short selection',request=request,reference_audio=None,
        musical_parameters='BPM, key and instrumentation are generation prompts, not measured or guaranteed.',
        processing=dict(source_seconds=25,excerpt_seconds=20,fade_in_seconds=.03,fade_out_seconds=.5,
                        loop_processed=False),formally_adopted=False,game_integrated=False)
    record['task']=api('/release_task',request)
    save(record_path,record)
    print('Submitted '+label,flush=True)
    deadline=time.monotonic()+1200
    while time.monotonic()<deadline:
        state=api('/query_result',{'task_id_list':[record['task']['task_id']]})[0]
        if state['status']==2:
            raise RuntimeError(str(state))
        if state['status']==1:
            results=state['result']
            results=json.loads(results) if isinstance(results,str) else results
            if len(results)!=1: raise RuntimeError(str(results))
            record['result']=results[0]
            break
        time.sleep(4)
    else: raise TimeoutError(record['task']['task_id'])
    url=record['result']['file']
    url=BASE+url if url.startswith('/') else url
    if not url.startswith(BASE+'/'): raise RuntimeError('Expected local generated audio')
    raw=MOTHERS/(stem+'_raw.wav')
    with urllib.request.urlopen(url,timeout=60) as response, raw.open('xb') as target:
        shutil.copyfileobj(response,target)
    pre=OUT/(stem+'_premaster.ogg')
    ff('-v','error','-n','-i',raw,'-t','20','-af','afade=t=in:st=0:d=0.03,afade=t=out:st=19.5:d=0.5',
       '-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',pre)
    before=measure(pre)
    gain=-27-float(before['integrated_lufs'])
    master=MOTHERS/(stem+'.wav')
    ff('-v','error','-n','-i',raw,'-t','20','-af',
       f'afade=t=in:st=0:d=0.03,afade=t=out:st=19.5:d=0.5,volume={gain:.5f}dB,alimiter=limit=0.158489:attack=10:release=150:level=0:latency=1,asetpts=N/SR/TB',
       '-ar','48000','-ac','2','-c:a','pcm_f32le',master)
    audition=OUT/(stem+'.ogg')
    ff('-v','error','-n','-i',master,'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',audition)
    record['processing'].update(fixed_gain_db=gain,loudness_target_lufs=-27,limiter_dbfs=-16,premaster_measurement=before)
    for key,path in [('raw_wav',raw),('master_wav',master),('premaster_ogg',pre),('ogg',audition)]:
        record[key]=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),probe=probe(path))
    record['technical_measurements']=measure(audition)
    save(record_path,record)
    print('Finished '+label+' '+json.dumps(record['technical_measurements']),flush=True)
    return record

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for attempt in range(300):
        try: api('/health'); break
        except (OSError,TimeoutError): time.sleep(3)
    else: raise TimeoutError('Local ACE-Step startup')
    records=[]
    for spec in DIRECTIONS:
        records.append(produce(spec))
        save(OUT/'generation_manifest_take01.json',dict(date=DATE,cue='BGM13_HOLD_ON',candidates=records))
    save(OUT/'technical_measurements_take01.json',dict(date=DATE,files=[dict(file=r['ogg']['file'],**r['technical_measurements']) for r in records]))

if __name__=='__main__': main()
