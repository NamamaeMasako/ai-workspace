"""Render a precisely scored BGM10 opening using this Windows device's GM piano.

Requires numpy, ffmpeg and ffprobe. The Windows instrument library is read in
place, never copied or included with project assets. No external music or AI.
"""
from pathlib import Path
import hashlib
import json
import os
import struct
import subprocess
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
MOTHERS = Path(__file__).resolve().parent
CUE = ROOT/'02_素材/音訊/候選/BGM10_INN_HUNTED'
OUT = CUE/'longform'
REFERENCE = CUE/'candidate_04_low_piano_sustain_6s_take07.ogg'
RATE = 48000
NAME = 'long_02_varied_dissonant_piano_take07'
DLS = Path(os.environ.get('WINDIR', 'C:/Windows'))/'System32/drivers/gm.dls'
# Each new onset contains a semitone (1) or tritone (6), never a resolved chord.
GROUPS = [
    # start, duration, ((MIDI pitch, name, relative strength), ...)
    (.12, 12.0, ((39,'Eb2',.48),(40,'E2',.26))),
    (6.12, 12.0, ((34,'Bb1',.34),(33,'A1',.20))),
    (12.12,12.0, ((37,'Db2',.30),(38,'D2',.16))),
    (18.65,10.2, ((42,'Gb2',.24),(43,'G2',.13))),
    (22.90, 5.8, ((37,'Db2',.20),(43,'G2',.12))),
    (28.45,11.4, ((32,'Ab1',.28),(33,'A1',.15))),
    (34.10,11.0, ((39,'Eb2',.21),(45,'A2',.11))),
    (38.65, 4.4, ((49,'Db3',.13),(48,'C3',.075))),
    (43.80,10.8, ((42,'Gb2',.18),(48,'C3',.10))),
    (49.95, 6.5, ((34,'Bb1',.23),(35,'B1',.12))),
    (54.20, 8.5, ((39,'Eb2',.19),(38,'D2',.10))),
    (57.70, 6.0, ((44,'Ab2',.11),(50,'D3',.055))),
]
NOTES = [dict(start=start,duration=duration,midi=midi,note=note,strength=strength)
         for start,duration,voices in GROUPS for midi,note,strength in voices]

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def ff(*args):
    return subprocess.run(['ffmpeg', *map(str,args)], capture_output=True, text=True, encoding='utf-8', check=True)

def chunks(blob, start, end):
    result = []
    while start+8 <= end:
        tag = blob[start:start+4]
        size = struct.unpack_from('<I',blob,start+4)[0]
        offset = start+8
        node = dict(tag=tag.decode('ascii'), offset=offset, size=size)
        if tag in (b'LIST', b'RIFF'):
            node['type'] = blob[offset:offset+4].decode('ascii')
            node['children'] = chunks(blob,offset+4,offset+size)
        result.append(node)
        start = offset+size+(size%2)
    return result

def tag(nodes, value):
    return next(n for n in nodes if n['tag']==value)

def typ(nodes, value):
    return next(n for n in nodes if n.get('type')==value)

def piano_regions(blob, nodes):
    for instrument in typ(nodes,'lins')['children']:
        children = instrument.get('children',[])
        info = next((n for n in children if n['tag']=='insh'),None)
        if not info:
            continue
        count,bank,patch = struct.unpack_from('<III',blob,info['offset'])
        if bank==0 and patch==0:
            return typ(children,'lrgn')['children']
    raise RuntimeError('GM acoustic grand piano not found')

def instrument_note(blob, nodes, regions, midi, duration):
    region = None
    for candidate in regions:
        header = tag(candidate['children'],'rgnh')
        low,high = struct.unpack_from('<HH',blob,header['offset'])
        if low <= midi <= high:
            region = candidate
            break
    if region is None:
        raise RuntimeError('No piano region for note '+str(midi))
    children = region['children']
    link = tag(children,'wlnk')
    index = struct.unpack_from('<I',blob,link['offset']+8)[0]
    pool = typ(nodes,'wvpl')
    table = tag(nodes,'ptbl')
    table_size = struct.unpack_from('<I',blob,table['offset'])[0]
    relative = struct.unpack_from('<I',blob,table['offset']+table_size+index*4)[0]
    wave = next(n for n in pool['children'] if n['offset']-8==pool['offset']+4+relative)
    fmt = tag(wave['children'],'fmt ')
    codec,channels,rate,byte_rate,align,bits = struct.unpack_from('<HHIIHH',blob,fmt['offset'])
    if (codec,channels,bits)!=(1,1,16):
        raise RuntimeError('Expected mono PCM16 piano sample')
    data = tag(wave['children'],'data')
    sample = np.frombuffer(blob,dtype='<i2',count=data['size']//2,offset=data['offset']).astype(np.float64)/32768
    tuning = tag(children,'wsmp')
    size,root,fine,attenuation,options,loop_count = struct.unpack_from('<IHhiII',blob,tuning['offset'])
    if not loop_count:
        raise RuntimeError('Piano sustain loop missing')
    loop_size,loop_type,loop_start,loop_length = struct.unpack_from('<IIII',blob,tuning['offset']+size)
    n = round(duration*RATE)
    positions = np.arange(n)*rate/RATE*2**((midi-root-fine/100)/12)
    loop_end = loop_start+loop_length
    positions = np.where(positions>=loop_end,loop_start+(positions-loop_start)%loop_length,positions)
    signal = np.interp(positions,np.arange(len(sample)),sample)
    seconds = np.arange(n)/RATE
    # Additional soft decay for a hushed long resonance; no new attacks in a tail.
    envelope = np.exp(-np.minimum(seconds,.9)/1.1) * np.exp(-np.maximum(seconds-.9,0)/12.0)
    envelope[:round(.045*RATE)] *= np.linspace(0,1,round(.045*RATE))
    release=round(2.0*RATE)
    phase=np.linspace(0,1,release)
    envelope[-release:] *= 1-phase*phase*(3-2*phase)
    signal *= envelope
    return signal.astype(np.float32), dict(bank=0,program_zero_based=0,
        wave_table_index=index,sample_rate=rate,sample_root_midi=root,fine_tune_cents=fine,
        sustain_loop_start_frames=loop_start,sustain_loop_length_frames=loop_length)

def measure(path):
    report = ff('-hide_banner','-i',path,'-af',
        'silencedetect=n=-45dB:d=0.5,loudnorm=I=-22:TP=-2.5:LRA=11:print_format=json','-f','null','-').stderr
    values,_ = json.JSONDecoder().raw_decode(report[report.rfind('{'):])
    return dict(integrated_lufs=values['input_i'],true_peak_dbtp=values['input_tp'],
        quiet_events=[s.strip() for s in report.splitlines() if 'silence_start:' in s or 'silence_end:' in s])

def main():
    OUT.mkdir(exist_ok=True)
    targets=[OUT/(NAME+'.json'),OUT/(NAME+'.ogg'),MOTHERS/(NAME+'_raw.wav'),MOTHERS/(NAME+'.wav')]
    if any(p.exists() for p in targets):
        raise FileExistsError('Existing revision outputs are preserved')
    blob=DLS.read_bytes()
    nodes=chunks(blob,12,len(blob))
    regions=piano_regions(blob,nodes)
    dry=np.zeros((65*RATE,2),dtype=np.float32)
    note_records=[]
    for event in NOTES:
        tone,source=instrument_note(blob,nodes,regions,event['midi'],event['duration'])
        offset=round(event['start']*RATE)
        length=min(len(tone),len(dry)-offset)
        # A narrow stereo image keeps the two pitches together.
        pan=-.07 if event['midi']%2 else .07
        dry[offset:offset+length,0]+=tone[:length]*event['strength']*np.sqrt((1-pan)/2)
        dry[offset:offset+length,1]+=tone[:length]*event['strength']*np.sqrt((1+pan)/2)
        note_records.append(dict(**event,instrument_source=source))
    # Quiet deterministic room reflections of the played notes, without noise.
    wet=np.zeros_like(dry)
    reflections=[(.073,.04),(.137,.02)]
    for i,(delay,amplitude) in enumerate(reflections):
        offset=round(delay*RATE)
        wet[offset:]+=dry[:-offset,::-1 if i%2 else 1]*amplitude
    pcm=dry+wet
    pcm*=10**(-17/20)/max(float(np.max(np.abs(pcm[:round(.9*RATE)]))),1e-12)
    raw=MOTHERS/(NAME+'_raw.wav')
    subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-',
        '-af','lowpass=f=1100:p=2','-c:a','pcm_f32le',str(raw)],input=pcm.astype('<f4').tobytes(),check=True)
    ref_bytes=REFERENCE.read_bytes()
    reference_sha256=hashlib.sha256(ref_bytes).hexdigest()
    reference_record=json.loads(REFERENCE.with_suffix('.json').read_text(encoding='utf-8'))
    if reference_sha256 != reference_record['ogg']['sha256']:
        raise RuntimeError('Selected reference audio changed')
    def decode(path):
        return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
            '-ar',str(RATE),'-ac','2','-f','f32le','-']),dtype='<f4').reshape(-1,2)
    reference_pcm=decode(REFERENCE)
    music=decode(raw)[:60*RATE].copy()
    preserved=round(17.5*RATE);join=round(18*RATE)
    music[:preserved]=reference_pcm[:preserved]
    phase=np.linspace(0,1,join-preserved,dtype=np.float32)
    weight=(phase*phase*(3-2*phase))[:,None]
    music[preserved:join]=reference_pcm[preserved:join]*(1-weight)+music[preserved:join]*weight
    preserved_difference=float(np.max(np.abs(music[:preserved]-reference_pcm[:preserved])))
    premaster=MOTHERS/(NAME+'_premaster.wav')
    subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-',
        '-af','afade=t=out:st=59.2:d=0.8','-c:a','pcm_f32le',str(premaster)],
        input=music.astype('<f4').tobytes(),check=True)
    pre=OUT/(NAME+'_premaster.ogg')
    ff('-v','error','-n','-i',premaster,'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',pre)
    before=measure(pre)
    gain=0.0  # Keep the selected quiet scale; no LUFS gain increase.
    master=MOTHERS/(NAME+'.wav')
    ff('-v','error','-n','-i',premaster,'-af',
       'alimiter=limit=0.595662:attack=5:release=50:level=0:latency=1,asetpts=N/SR/TB',
       '-ar','48000','-ac','2','-c:a','pcm_f32le',master)
    audition=OUT/(NAME+'.ogg')
    ff('-v','error','-n','-i',master,'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',audition)
    record=dict(date='2026-10-16',cue='BGM10_INN_HUNTED',label='低聲懸響・變化長版',revision='long_02',
        status='awaiting user 60-second long audition',method='New explicit original score rendered with local Windows GM piano. Actual selected short OGG provides the preserved opening; no AI model request or external music.',
        review_basis='User requests a long cue with new dissonant material, varied note lengths and onset intervals, not repetition of the three short dyads or a strict six-second grid.',
        instrument=dict(local_device_library=str(DLS),library_sha256=hashlib.sha256(blob).hexdigest(),
                        library_copied_into_project=False,library_redistributed=False),
        reference_audio=dict(file=REFERENCE.name,sha256=reference_sha256,
            method='Actual OGG read and decoded into the long arrangement, no model upload.',
            preserved_seconds=17.5,clean_score_crossfade_seconds=[17.5,18.0],
            preserved_pcm_max_difference=preserved_difference),
        score=note_records,group_onsets_seconds=[g[0] for g in GROUPS],
        composition=dict(new_dyads_after_opening=True,repeat_short_as_loop=False,
            onset_intervals_seconds=[round(GROUPS[i][0]-GROUPS[i-1][0],2) for i in range(1,len(GROUPS))],
            dyad_semitone_distances=[abs(g[2][0][0]-g[2][1][0]) for g in GROUPS],
            note_durations_seconds=[g[1] for g in GROUPS],
            character='Quiet unresolved semitones and tritones, no consonant resolution or action build.'),
        processing=dict(raw_duration_seconds=65,audition_duration_seconds=60,
            level_policy='Selected short opening scale retained; no integrated-loudness normalization',
            fixed_gain_db=gain,low_pass_hz=1100,initial_decay_time_constant_seconds=1.1,
            sustain_transition_seconds=.9,sustain_decay_time_constant_seconds=12.0,
            attack_seconds=.045,release_seconds=2.0,tail_reflections=reflections,
            fade_out_seconds=.8,premaster_measurement=before,loop_processed=False),
        technical_measurements=measure(audition),game_integrated=False,formally_adopted=False)
    for key,path in [('raw_wav',raw),('premaster_wav',premaster),('master_wav',master),('premaster_ogg',pre),('ogg',audition)]:
        record[key]=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
            'format=duration:stream=codec_name,sample_rate,channels','-of','json',str(path)])))
    save(OUT/(NAME+'.json'),record)
    save(OUT/'production_manifest_long_02.json',dict(date='2026-10-16',cue=record['cue'],candidates=[record]))
    print(json.dumps(dict(file=audition.name,measurements=record['technical_measurements']),ensure_ascii=False))

if __name__=='__main__': main()
