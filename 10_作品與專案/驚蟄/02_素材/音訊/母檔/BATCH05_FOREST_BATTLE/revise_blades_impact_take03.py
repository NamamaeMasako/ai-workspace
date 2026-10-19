"""2026-10-19: dry blade contact and two massive bodies colliding.

Original procedural synthesis; preserve all earlier takes and game script.
Only two existing battle audio files are replaced, pending scene acceptance.
"""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("batch05_source", HERE / "produce_batch05_take01.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
RATE, OUT = base.RATE, base.OUT
GAME = base.ROOT / "03_開發/JingZhe/game"


def blades():
    rng = np.random.default_rng(6328)
    x = np.zeros(round(.70 * RATE))
    for at, gain, tune in [(.025, 1.0, 1.0), (.276, .88, 1.045)]:
        t = np.arange(round(.27 * RATE)) / RATE
        # Remove low bowl-like modes; the onset dominates the short high ring.
        contact = base.band(rng, len(t), 2000, 13500) * np.exp(-t / .0028)
        hard = base.band(rng, len(t), 1100, 6000) * np.exp(-t / .007)
        ring = np.zeros(len(t))
        for f, a, d in [(2117, .19, .023), (3371, .23, .036), (4789, .18, .041),
                        (6413, .10, .024), (8933, .055, .013)]:
            # Small close partials broaden the steel rather than a single bell note.
            for offset in [-.008, .006]:
                ring += a * .5 * np.sin(2*np.pi*f*tune*(1+offset)*t) * np.exp(-t/d)
        hit = .65*contact + .30*hard + ring
        base.put(x, at, base.edge(hit, .00035, .03), gain)
        base.put(x, at+.007, base.rub(rng, .022, 3700, 11500, 1.5), .040*gain)
    return base.edge(x-np.mean(x), .003, .03)


def impact():
    rng = np.random.default_rng(6330)
    x = np.zeros(round(.88 * RATE))
    t = np.arange(round(.80 * RATE)) / RATE
    # A thick pressure body and damped armor deformation, not two pebble clicks.
    low = base.band(rng, len(t), 30, 165) * np.exp(-t/.13)
    mass = base.band(rng, len(t), 95, 420) * np.exp(-t/.080)
    crush = base.band(rng, len(t), 260, 1800) * np.exp(-t/.031)
    attack = base.band(rng, len(t), 700, 3500) * np.exp(-t/.007)
    phase = 2*np.pi*(43*t + 29*.018*(1-np.exp(-t/.018)))
    pressure = np.sin(phase)*np.exp(-t/.102)
    hit = .68*low + .52*mass + .22*crush + .055*attack + .44*pressure
    hit *= 1-np.exp(-t/.0014)
    hit = np.tanh(1.12*hit)/1.12
    base.put(x, .025, base.edge(hit, .001, .065))
    # Brief residual compression and shell movement stay under the initial blow.
    for at, dur, gain in [(.052, .14, .052), (.096, .16, .032), (.154, .17, .015)]:
        base.put(x, at, base.rub(rng, dur, 170, 1200, 1.6), gain)
    return base.edge(x-np.mean(x), .003, .05)


def main():
    manifest = OUT/'revision_manifest_take03.json'
    if manifest.exists():
        raise FileExistsError(manifest)
    script = GAME/'script.rpy'
    before = base.digest(script)
    records = []
    for stem, cue, fn, seed, prior_take, peak, intention in [
        ('battle_kamikiri_blades', 'SFX28_KAMIKIRI_BLADES', blades, 6328, 'take02', -18.5,
         '去除低中頻鍋具般空腔共鳴，短硬刃口接觸為主，極短高頻金屬尾音；保留兩次交錯。'),
        ('battle_omukade_impact', 'SFX30_OMUKADE_IMPACT', impact, 6330, 'take01', -15.5,
         '兩個重物互撞：厚實寬頻低沉壓力、短甲殼受力與震動尾勁，降低小石塊尖敲感。'),
    ]:
        target = GAME/'audio/sfx/battle'/(stem+'.ogg')
        prior = OUT/(stem+'_'+prior_take+'.ogg')
        if base.digest(target) != base.digest(prior):
            raise RuntimeError('Unexpected active asset: '+stem)
        x = fn(); x *= 10**(peak/20)/np.max(np.abs(x))
        wav = HERE/(stem+'_take03.wav'); ogg = OUT/(stem+'_take03.ogg')
        subprocess.run(['ffmpeg','-v','error','-n','-f','f32le','-ar',str(RATE),'-ac','1',
                        '-i','-','-c:a','pcm_s24le',str(wav)],input=x.astype('<f4').tobytes(),check=True)
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(wav),'-ar','44100','-ac','1',
                        '-c:a','libvorbis','-q:a','6',str(ogg)],check=True)
        pcm = np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(ogg),
                                                   '-f','f32le','-']),dtype='<f4')
        rec = dict(date='2026-10-19',cue=cue,name=stem,take='take03',intention=intention,
                   method='original procedural synthesis; no external recording, voice or model',seed=seed,
                   status='integrated_scene_audition_pending',formally_adopted=False,
                   duration_seconds=len(x)/RATE,sample_peak_target_dbfs=peak,
                   decoded_peak_dbfs=base.db(np.max(np.abs(pcm))),
                   decoded_rms_dbfs=base.db(np.sqrt(np.mean(pcm.astype(float)**2))),
                   source=Path(__file__).name,source_sha256=base.digest(Path(__file__)),
                   wav=dict(file=wav.name,sha256=base.digest(wav),sample_rate=RATE,channels=1,bits=24),
                   ogg=dict(file=ogg.name,sha256=base.digest(ogg),sample_rate=44100,channels=1),
                   previous_take=prior_take,previous_ogg_sha256=base.digest(prior),
                   game_file=target.relative_to(base.ROOT).as_posix())
        base.save(OUT/(stem+'_take03.json'),rec); records.append(rec)
    for rec in records:
        shutil.copy2(OUT/rec['ogg']['file'],base.ROOT/rec['game_file'])
    base.save(manifest,dict(date='2026-10-19',batch='BATCH05_FOREST_BATTLE',
                            user_feedback=['金屬交錯像兩個鍋子在敲，不像刀刃',
                                           '大百足撞擊像小石頭互敲，應像兩個重物互撞'],
                            candidates=records,script_sha256_before=before,
                            script_sha256_after=base.digest(script),game_text_or_trigger_changed=False,
                            retained_heavy_steps='battle_spider_steps_heavy_take02.ogg',
                            review_entry='script.rpy:1114',formally_adopted=False))
    print(json.dumps([dict(name=r['name'],duration=r['duration_seconds'],peak=r['decoded_peak_dbfs'])
                      for r in records],ensure_ascii=False))


if __name__ == '__main__':
    main()
