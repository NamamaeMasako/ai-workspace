"""Produce four sudden-loss shock and denial BGM11 auditions without external audio with the local ACE-Step API; keep raw sources."""
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTHERS = Path(__file__).resolve().parent
OUT = ROOT / '02_素材/音訊/候選/BGM11_LOSS_AND_REWIND'
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

COMMON = ('Original instrumental dramatic underscore, 25 seconds, the immediate moment of sudden tragic death. '
    'Someone loved has just collapsed and cannot answer. Shock, disbelief, desperate refusal to accept it, '
    'then helpless pain while still trying to reach her. The wound is happening NOW, raw and unfinished. '
    'Quiet intensity and grief with nervous inner movement, suspended breath and aching minor harmony. '
    'Fragile short rising questions repeatedly fail to resolve, break off, then sink a semitone; '
    'the melody tries again against a bass that cannot move forward. Uneven hesitant phrasing, '
    'unresolved appoggiaturas, restrained dynamic tension, intimate close musical space. '
    'An unsettled moderate pulse inside the music, neither a stately slow procession nor a driving beat. '
    'Soft attacks, controlled volume, small ensemble. Keep emotionally wounded and human throughout. '
    'Continue with unresolved tension through 25 seconds, natural connected note tails. '
    'No funeral march, ceremonial elegy, peaceful remembrance, nostalgic farewell, comforting resolution, '
    'graduation song, sweet ballad, hopeful lift, horror sting, jump scare, battle drums or large crescendo. '
    'Instrumental only: no voices, choir, speech, heartbeats, rain, wind or sound effects. ')

DIRECTIONS = [
    (1,'piano_strings_denial',3821,'不可能是妳',68,
     'Soft middle-register piano repeats a short rising two-note question at uneven intervals, '
     'each attempt breaks against a suspended minor chord. A thin tense viola and cello line '
     'emerges beneath it, narrowly moving and trembling very softly. Small surges of refusal '
     'immediately collapse into empty space. Raw tragic scene underscore with aching sadness.'),
    (2,'broken_piano',3822,'再回答一次',72,
     'Intimate solo piano, a broken interrupted motif reaching upward and failing, '
     'unanswered call-and-response between middle and low registers, irregular rests and '
     'quiet repeated notes suggesting a hand still trying to wake someone. Painful unresolved '
     'minor-second suspensions. Sparse fragments, no flowing arpeggios or regular song chords.'),
    (3,'trembling_strings',3823,'停在那一刻',64,
     'Small viola and cello ensemble with very soft measured tremolo under an exposed, '
     'fragile aching string fragment. The upper voice reaches upward in disbelief, holds '
     'a strained suspension and falls back without release. Internal agitation held at low volume, '
     'stunned grief and powerlessness. No grand orchestral lament or broad singing solo.'),
    (4,'cello_piano_plea',3824,'還不能放手',76,
     'Piano and close dry cello duet, an insistent but quiet three-note plea returns '
     'with uneven spacing, each time slightly altered and left hanging. A soft low piano '
     'pulse hesitates and drops out while cello sustains a painful unresolved minor ninth. '
     'Desperate grief held inside, wanting to act but unable to save her; no cello virtuoso melody.'),
]

def produce(spec):
    number,slug,seed,label,bpm,detail = spec
    stem=f'candidate_{number:02d}_{slug}_seed{seed}_take03'
    record_path=OUT/(stem+'.json')
    if record_path.exists():
        raise FileExistsError(record_path)
    request=dict(prompt=detail+' '+COMMON, lyrics='[Instrumental]', thinking=False,
        use_format=False,use_cot_caption=False,use_cot_language=False,bpm=bpm,
        key_scale='F minor',time_signature='4',vocal_language='unknown',audio_duration=25,
        inference_steps=8,batch_size=1,use_random_seed=False,seed=seed,model='acestep-v15-turbo',
        task_type='text2music',audio_cover_strength=1.0,audio_format='wav')
    record=dict(date=DATE,cue='BGM11_LOSS_AND_REWIND',label=label,revision='take03',
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
        save(OUT/'generation_manifest_take03.json',dict(date=DATE,cue='BGM11_LOSS_AND_REWIND',candidates=records))
    save(OUT/'technical_measurements_take03.json',dict(date=DATE,files=[dict(file=r['ogg']['file'],**r['technical_measurements']) for r in records]))

if __name__=='__main__': main()
