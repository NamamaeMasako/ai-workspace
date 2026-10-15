"""Produce four revised BGM10 auditions without uploading external audio with the local ACE-Step API; keep raw sources."""
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTHERS = Path(__file__).resolve().parent
OUT = ROOT / '02_素材/音訊/候選/BGM10_INN_HUNTED'
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

COMMON = ('Original instrumental dark exploration BGM for a supernatural visual novel, 25 seconds of continuous music. '
    'A spider-like intruder is already inside a small wooden inn at night, quietly searching the rooms. '
    'The listener senses an abnormal presence in a familiar place. Restrained eerie suspense, patient lurking menace, '
    'low dark musical foundation, sparse small pitched details, cold unresolved harmony, minimal foreground melody. '
    'A calm slow pulse keeps moving beneath the surface without becoming an action beat. '
    "Also support a woman's persistent uneasy premonition after battle while returning to the inn. "
    'Close enclosed scale rather than a vast dungeon, subtly East Asian supernatural setting rather than modern detective jazz. '
    'Use naturally connected note tails and short evolving musical phrases; no big build, no final cadence, no long silent gaps. '
    'No cheerful or bouncy tune, no romantic sadness, no lamenting cello melody, no lush orchestral strings, '
    'no busy arpeggios, no fast battle ostinato, no epic brass or loud percussion, no jump-scare stings. '
    'Music only: no singing, speech, vocal choir, wind, rain, insects, static, footsteps, wood creaks or other real-world sound effects. ')

DIRECTIONS = [
    (1,'low_pad_mallet',3711,'闇室潛影',58,
     'Soft low synthesized bass pad forms an ominous continuous tonal bed; sparse muted wooden mallet notes '
     'answer a slow three-note original chromatic figure. Hollow intimate resonance, very few notes, '
     'a faint regular low pitched pulse, mostly bass and low-mid register, tiny high notes only as brief glints.'),
    (2,'low_reed_shadow',3712,'空廊異兆',60,
     'Dark low reed-like synthesizer sustains soft narrow unresolved intervals over a subdued bass pulse. '
     'Occasional short low bamboo-flute notes and muted metal harmonics create a quiet uncanny Japanese inn atmosphere. '
     'Understated melodic fragments, dry restrained texture with natural resonance, no flute solo or sweeping phrases.'),
    (3,'muted_koto_bass',3713,'絲影盤伏',56,
     'Damped low koto notes make a slow broken asymmetrical original motif over a smooth quiet low synth foundation. '
     'A distant single glassy struck note occasionally suspends above it, long dark pitched undertones, '
     'small chromatic shifts, few foreground notes, lurking predatory patience rather than folk melody.'),
    (4,'piano_dark_pulse',3714,'返路不安',62,
     'Very soft low felt piano repeats a restrained original unresolved cell with subtle timing gaps '
     'above an ominous low organ-like pad and muted string harmonics. A consistent slow low musical pulse '
     'suggests growing apprehension on the walk home. Keep the piano cold and sparse, no lyrical or sentimental tune.'),
]

def produce(spec):
    number,slug,seed,label,bpm,detail = spec
    stem=f'candidate_{number:02d}_{slug}_seed{seed}_take02'
    record_path=OUT/(stem+'.json')
    if record_path.exists():
        raise FileExistsError(record_path)
    request=dict(prompt=detail+' '+COMMON, lyrics='[Instrumental]', thinking=False,
        use_format=False,use_cot_caption=False,use_cot_language=False,bpm=bpm,
        key_scale='E minor',time_signature='4',vocal_language='unknown',audio_duration=25,
        inference_steps=8,batch_size=1,use_random_seed=False,seed=seed,model='acestep-v15-turbo',
        task_type='text2music',audio_cover_strength=1.0,audio_format='wav')
    record=dict(date=DATE,cue='BGM10_INN_HUNTED',label=label,revision='take02',
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
    gain=-16-float(before['integrated_lufs'])
    master=MOTHERS/(stem+'.wav')
    ff('-v','error','-n','-i',raw,'-t','20','-af',
       f'afade=t=in:st=0:d=0.03,afade=t=out:st=19.5:d=0.5,volume={gain:.5f}dB,alimiter=limit=0.749894:attack=5:release=50:level=0:latency=1,asetpts=N/SR/TB',
       '-ar','48000','-ac','2','-c:a','pcm_f32le',master)
    audition=OUT/(stem+'.ogg')
    ff('-v','error','-n','-i',master,'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',audition)
    record['processing'].update(fixed_gain_db=gain,limiter_dbfs=-2.5,premaster_measurement=before)
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
        save(OUT/'generation_manifest_take02.json',dict(date=DATE,cue='BGM10_INN_HUNTED',candidates=records))
    save(OUT/'technical_measurements_take02.json',dict(date=DATE,files=[dict(file=r['ogg']['file'],**r['technical_measurements']) for r in records]))

if __name__=='__main__': main()
