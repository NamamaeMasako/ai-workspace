"""Produce four shadow witch character BGM14 auditions without external audio with the local ACE-Step API; keep raw sources."""
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTHERS = Path(__file__).resolve().parent
OUT = ROOT / '02_素材/音訊/候選/BGM14_SHADOW_WITCH'
BASE = 'http://127.0.0.1:8001'
DATE = '2026-10-17'

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

COMMON = ('Original instrumental character theme for a dark fantasy visual novel, 25 seconds. '
    'A powerful shadow witch steps into a forest clearing and quietly takes control of a crisis. '
    'She is an ancient high-ranking being with a young adult appearance, outwardly cold, '
    'composed, intelligent, elegant and slightly irritated by the trouble. Her power is effortless. '
    'She heals the wounded protagonist while scolding him, then asks for his next written chapter: '
    'a tiny concealed kindness beneath detached authority. Mysterious presence, restrained dignity, '
    'unreadable thoughts and the faint possibility of trust. A memorable compact musical identity, '
    'ambiguous minor harmony with suspended added tones, graceful measured phrases, low-to-middle '
    'register, small intimate chamber scale, quiet continuous musical resonance. '
    'Soft rounded attacks, gentle controlled dynamics, spacious connected note tails and understated '
    'forward movement. Remain cool and mysterious through the whole excerpt; any warmth stays subtle '
    'and unresolved. Leave room for dialogue. Continue naturally past 20 seconds, no early ending. '
    'No cheerful daily-life music, cute magical girl, whimsical comedy, bouncy staccato, dancing waltz, '
    'jazzy swing, sweet romance, sunny major cadence, epic orchestral entrance, heroic victory, '
    'funeral lament, horror villain menace, piercing high chimes, busy arpeggios, loud percussion or climax. '
    'Only instrumental music: no vocals, choir, spoken words, wind, rain, ambient noise or sound effects. ')

DIRECTIONS = [
    (1,'piano_viola_sovereign',4101,'夜幕的主人',64,
     'Soft dark piano and a restrained low viola, a deliberate three-note motif above sustained '
     'low open fifths with a quiet suspended minor second. Slow stately harmonic changes and '
     'an elegant low answering phrase suggest someone who needs no display of force. '
     'Cool controlled authority, no fragile dying motif or sorrowful piano ballad.'),
    (2,'bass_clarinet_cello',4102,'影中的來客',68,
     'Velvety bass clarinet carries an economical questioning motif over very soft cello and '
     'occasional low piano chords. Measured asymmetrical phrases, dark transparent chamber texture '
     'and subtle chromatic neighboring notes suggest intelligence and unreadable intent. '
     'Reserved elegance, no playful bassoon gestures, jazz rhythm or threatening horror drone.'),
    (3,'muted_harp_shadow',4103,'命運在指間',72,
     'Muted low harp with soft viola and a sustained cello foundation. A small deliberate '
     'plucked motif returns at varied intervals, surrounded by dusky suspended harmony; '
     'one restrained answering phrase suggests she understands more than she says. '
     'Fine dark filigree and calm precision, no sparkling fairy harp, runs, jaunty plucking or dance.'),
    (4,'strings_hidden_care',4104,'冷語之下',60,
     'Intimate muted viola and cello with occasional rounded low piano notes. A composed '
     'descending three-note signature rests above a slow unresolved minor harmony, then '
     'an inner voice answers gently without changing into a sentimental melody. '
     'Quiet dignity, distance and guarded care; keep the mystical character present from the '
     'opening. No broad grieving strings, romantic swell, rescue triumph or comforting resolution.'),
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
    record=dict(date=DATE,cue='BGM14_SHADOW_WITCH',label=label,revision='take01',
        status='awaiting user short selection',request=request,reference_audio=None,
        musical_parameters='BPM, key and instrumentation are generation prompts, not measured or guaranteed.',
        setting_sources=['00_共用參考/世界觀/伊洛_Elo/02_角色與勢力/角色設定.txt',
                         '10_作品與專案/驚蟄/02_素材/視覺鎖定清單/影之魔女.txt',
                         '10_作品與專案/驚蟄/03_開發/JingZhe/game/script.rpy'],
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
        save(OUT/'generation_manifest_take01.json',dict(date=DATE,cue='BGM14_SHADOW_WITCH',candidates=records))
    save(OUT/'technical_measurements_take01.json',dict(date=DATE,files=[dict(file=r['ogg']['file'],**r['technical_measurements']) for r in records]))

if __name__=='__main__': main()
