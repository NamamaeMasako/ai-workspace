"""Produce four weighty consequential decision BGM12 auditions without external audio with the local ACE-Step API; keep raw sources."""
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTHERS = Path(__file__).resolve().parent
OUT = ROOT / '02_素材/音訊/候選/BGM12_CHOOSE_MY_FATE'
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

COMMON = ('Original instrumental psychological drama score, 25 seconds, a grave consequential decision. '
    'Immediately after choosing to keep a dangerous protective card for himself, a man who has '
    'witnessed his companions die in two failed futures decides to bear the cost alone. '
    'His decision has weight, fear and responsibility; he knowingly walks toward possible suffering. '
    'Heavy restrained resolve, pressure held inside, painful certainty and a farewell he cannot say. '
    'Dark low-register harmony from the opening, slow changing bass weight, tense minor ninths '
    'and suspended seconds, an economical motif that strains upward against a descending bass. '
    'Each small forward movement feels resisted, then holds firm without bright harmonic release. '
    'The decision is made but its danger and cost remain present. Serious dramatic tension beneath '
    'dialogue, low soft dynamic level, rounded soft attacks, substantial sustained musical resonance. '
    'Patient deliberate motion, continuous musical presence through all 25 seconds. '
    'No light daily-life mood, cozy warmth, easy optimism, jaunty or swaying rhythm, bouncing '
    'plucks, waltz, lilting ostinato, pleasant pop chord loop or sweet singable melody. '
    'No funeral procession, nostalgic graduation song, romantic ballad, epic heroic fanfare, '
    'battle drums, horror stings, grand crescendo or early ending. '
    'Instrumental only: no voices, choir, speech or environmental sound effects. ')

DIRECTIONS = [
    (1,'piano_bass_weight',3911,'決定的重量',58,
     'Dark soft piano in the low and middle registers, widely spaced weighty minor chords '
     'over a sustained bowed double bass. A restrained upward fourth hangs against a tense '
     'low pedal, then settles on a stern unresolved chord. Connected bass resonance carries '
     'the tension under sparse piano gestures. No high decorative notes or arpeggiated accompaniment.'),
    (2,'low_strings_burden',3912,'由我承受',62,
     'Small viola, cello and double bass ensemble, broad quiet bow strokes with heavy harmonic '
     'friction. A compact upper phrase rises with effort while the bass slowly descends chromatically. '
     'Deep inner pressure and restrained resolve, close chamber texture, connected bow changes. '
     'No light repetitive rhythm, fast tremolo or sweeping lyrical solo.'),
    (3,'muted_horn_cello',3913,'再無退路',66,
     'One low muted French horn joins cello and very sparse dark piano, quiet short held notes '
     'rather than a fanfare. Stern low harmonies support a narrow hesitant motif that becomes '
     'firmer without getting louder. Serious responsibility and danger remain unresolved. '
     'Intimate ensemble, no brass section, epic chord rise, marching pulse or victory cadence.'),
    (4,'cello_piano_cost',3914,'把結局留下',60,
     'A low cello and soft piano duet with close minor-second suspensions over a dark bass anchor. '
     "A short unresolved plea returns more firmly each time, as if choosing to carry another person's "
     'fate despite fear. Low sustained chord weight beneath the phrase, controlled forward movement '
     'without flowing accompaniment. No sweet romantic cello melody, funeral lament or relaxed sway.'),
]

def produce(spec):
    number,slug,seed,label,bpm,detail = spec
    stem=f'candidate_{number:02d}_{slug}_seed{seed}_take02'
    record_path=OUT/(stem+'.json')
    if record_path.exists():
        raise FileExistsError(record_path)
    request=dict(prompt=detail+' '+COMMON, lyrics='[Instrumental]', thinking=False,
        use_format=False,use_cot_caption=False,use_cot_language=False,bpm=bpm,
        key_scale='D minor',time_signature='4',vocal_language='unknown',audio_duration=25,
        inference_steps=8,batch_size=1,use_random_seed=False,seed=seed,model='acestep-v15-turbo',
        task_type='text2music',audio_cover_strength=1.0,audio_format='wav')
    record=dict(date=DATE,cue='BGM12_CHOOSE_MY_FATE',label=label,revision='take02',
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
        save(OUT/'generation_manifest_take02.json',dict(date=DATE,cue='BGM12_CHOOSE_MY_FATE',candidates=records))
    save(OUT/'technical_measurements_take02.json',dict(date=DATE,files=[dict(file=r['ogg']['file'],**r['technical_measurements']) for r in records]))

if __name__=='__main__': main()
