"""Produce four restrained grief BGM11 auditions without external audio with the local ACE-Step API; keep raw sources."""
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

COMMON = ('Original instrumental grief underscore for a dark fantasy visual novel, 25 seconds. '
    'Two alternative scenes share this cue: discovering a companion dead inside a wooden inn, '
    'and cradling another companion who has died after a forest battle. Their loss is real, '
    'the survivor is numb, helpless and holding back tears. Quiet sorrow, aching absence, '
    'restrained desolation rather than suspense or horror. Intimate musical scale for reading dialogue. '
    'A small memorable minor-key phrase, slow falling gestures, gentle unresolved suspensions, '
    'long natural note tails with breathing room, restrained dynamics and very soft attacks. '
    'Continuous low-key musical presence for the full 25 seconds; no abrupt note cutoff or early ending. '
    'Keep the grief deeply sad and calm. No hopeful major-key lift, sweet romantic mood, cheerful pentatonic tune, '
    'playful rhythm, heroic sacrifice fanfare, victorious resolution or big dramatic swell. '
    'No fast rhythm, marching beat, pounding drums, bright bells, sparkling piano runs or busy arpeggios. '
    'No dissonant horror clusters, jump scares or aggressive low impacts; this is loss and mourning. '
    'Instrumental only, no voice, choir, speech, rain, wind, insects, crackles, footsteps or environmental sound effects. ')

DIRECTIONS = [
    (1,'felt_piano',3801,'微燈已冷',44,
     'A very soft low-to-middle felt piano alone, sparse unhurried descending minor phrases. '
     'Gentle hammer attacks and naturally connected decay, hollow space around a few carefully placed notes, '
     'the shock of absence without sentimental romantic piano chords.'),
    (2,'cello_piano',3802,'弦上餘痛',42,
     'A restrained low cello sings a quiet slow lament above only a few muted piano notes. '
     'Narrow sorrowful melodic movement and soft sustained bowing, a small chamber duet, '
     'little vibrato, no soloist display, no orchestral bloom or emotional climax.'),
    (3,'muted_strings',3803,'未盡的話',40,
     'A tiny muted viola and cello ensemble holds quiet minor suspensions with slow descending sighs. '
     'Long connected bow phrases, minimal inner-voice movement, restrained acoustic chamber strings, '
     'grief held inside rather than a grand funeral procession.'),
    (4,'bamboo_guzheng',3804,'空燈殘影',46,
     'A soft low bamboo flute carries a brief plaintive minor phrase over sparse damped low guzheng plucks. '
     'Quiet East Asian chamber elegy, long natural resonance, simple aching falling intervals, '
     'no ornamented runs, folk dance lilt or festive pentatonic melody.'),
]

def produce(spec):
    number,slug,seed,label,bpm,detail = spec
    stem=f'candidate_{number:02d}_{slug}_seed{seed}_take01'
    record_path=OUT/(stem+'.json')
    if record_path.exists():
        raise FileExistsError(record_path)
    request=dict(prompt=detail+' '+COMMON, lyrics='[Instrumental]', thinking=False,
        use_format=False,use_cot_caption=False,use_cot_language=False,bpm=bpm,
        key_scale='D minor',time_signature='4',vocal_language='unknown',audio_duration=25,
        inference_steps=8,batch_size=1,use_random_seed=False,seed=seed,model='acestep-v15-turbo',
        task_type='text2music',audio_cover_strength=1.0,audio_format='wav')
    record=dict(date=DATE,cue='BGM11_LOSS_AND_REWIND',label=label,revision='take01',
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
        save(OUT/'generation_manifest_take01.json',dict(date=DATE,cue='BGM11_LOSS_AND_REWIND',candidates=records))
    save(OUT/'technical_measurements_take01.json',dict(date=DATE,files=[dict(file=r['ogg']['file'],**r['technical_measurements']) for r in records]))

if __name__=='__main__': main()
