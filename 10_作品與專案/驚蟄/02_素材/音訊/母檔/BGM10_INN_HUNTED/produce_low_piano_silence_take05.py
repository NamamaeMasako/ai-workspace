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

ROOT = Path(__file__).resolve().parents[4]
MOTHERS = Path(__file__).resolve().parent
OUT = ROOT/'02_素材/音訊/候選/BGM10_INN_HUNTED'
RATE = 48000
NAME = 'candidate_04_low_piano_silence_take05'
DLS = Path(os.environ.get('WINDIR', 'C:/Windows'))/'System32/drivers/gm.dls'
NOTES = [
    # Each pair begins simultaneously. The stronger pitch is a black key.
    dict(start=.12, midi=39, note='Eb2', strength=.48, duration=4),
    dict(start=.12, midi=40, note='E2', strength=.26, duration=4),
    dict(start=8.40, midi=34, note='Bb1', strength=.34, duration=4),
    dict(start=8.40, midi=33, note='A1', strength=.20, duration=4),
    dict(start=15.40, midi=37, note='Db2', strength=.30, duration=4),
    dict(start=15.40, midi=38, note='D2', strength=.16, duration=4),
]

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
    envelope = np.exp(-seconds/1.1)
    envelope[:round(.045*RATE)] *= np.linspace(0,1,round(.045*RATE))
    release=round(1.4*RATE)
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
    targets=[OUT/(NAME+'.json'),OUT/(NAME+'.ogg'),MOTHERS/(NAME+'_raw.wav'),MOTHERS/(NAME+'.wav')]
    if any(p.exists() for p in targets):
        raise FileExistsError('Existing revision outputs are preserved')
    blob=DLS.read_bytes()
    nodes=chunks(blob,12,len(blob))
    regions=piano_regions(blob,nodes)
    dry=np.zeros((25*RATE,2),dtype=np.float32)
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
    pcm*=10**(-17/20)/max(float(np.max(np.abs(pcm))),1e-12)
    raw=MOTHERS/(NAME+'_raw.wav')
    subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','2','-i','-',
        '-af','lowpass=f=1100:p=2','-c:a','pcm_f32le',str(raw)],input=pcm.astype('<f4').tobytes(),check=True)
    pre=OUT/(NAME+'_premaster.ogg')
    ff('-v','error','-n','-i',raw,'-t','20','-af','afade=t=out:st=19.2:d=0.8',
       '-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',pre)
    before=measure(pre)
    gain=0.0  # Keep the notes quiet; do not normalize gated loudness across rests.
    master=MOTHERS/(NAME+'.wav')
    ff('-v','error','-n','-i',raw,'-t','20','-af',
       f'afade=t=out:st=19.2:d=0.8,volume={gain:.5f}dB,alimiter=limit=0.595662:attack=5:release=50:level=0:latency=1,asetpts=N/SR/TB',
       '-ar','48000','-ac','2','-c:a','pcm_f32le',master)
    audition=OUT/(NAME+'.ogg')
    ff('-v','error','-n','-i',master,'-ar','44100','-ac','2','-c:a','libvorbis','-q:a','5',audition)
    record=dict(date='2026-10-16',cue='BGM10_INN_HUNTED',label='暗間留白',revision='take05',
        status='awaiting user opening-direction audition',method='Explicit original note score rendered from local Windows GM piano; no AI generation or external music reference.',
        review_basis='User accepted take04 pitch character but found no stillness. Preserve all three dyads and relative strengths; soften attacks, let resonance decay away and leave real rests between events.',
        instrument=dict(local_device_library=str(DLS),library_sha256=hashlib.sha256(blob).hexdigest(),
                        library_copied_into_project=False,library_redistributed=False),
        score=note_records,group_onsets_seconds=[.12,8.4,15.4],tempo='Unmetered; no regular pulse or fixed BPM.',
        processing=dict(raw_duration_seconds=25,audition_duration_seconds=20,peak_before_filter_dbfs=-17,level_policy='Fixed quiet peak, no integrated-loudness normalization',
            fixed_gain_db=gain,low_pass_hz=1100,note_decay_time_constant_seconds=1.1,attack_seconds=.045,release_seconds=1.4,
            tail_reflections=reflections,premaster_measurement=before,loop_processed=False),
        technical_measurements=measure(audition),game_integrated=False,formally_adopted=False)
    for key,path in [('raw_wav',raw),('master_wav',master),('premaster_ogg',pre),('ogg',audition)]:
        record[key]=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
            'format=duration:stream=codec_name,sample_rate,channels','-of','json',str(path)])))
    save(OUT/(NAME+'.json'),record)
    save(OUT/'production_manifest_take05.json',dict(date='2026-10-16',cue=record['cue'],candidates=[record]))
    print(json.dumps(dict(file=audition.name,measurements=record['technical_measurements']),ensure_ascii=False))

if __name__=='__main__': main()
