"""Original procedural revisions requested on 2026-10-19.

Only replace the two pending battle assets. Preserve take01 and all game text.
Requires numpy, scipy, ffmpeg. No external recording or generated music.
"""
from pathlib import Path
import importlib.util
import hashlib
import json
import shutil
import subprocess
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("batch05_source", HERE / "produce_batch05_take01.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
RATE = base.RATE
OUT = base.OUT
GAME = base.ROOT / "03_開發/JingZhe/game"


def heavy(seed=6224):
    rng = np.random.default_rng(seed)
    x = np.zeros(round(1.04 * RATE))
    for at, gain in [(0.025, 1.0), (0.49, 0.88)]:
        t = np.arange(round(0.51 * RATE)) / RATE
        # A broad, damped impact rather than a sustained pitched bass note.
        low = base.band(rng, len(t), 32, 175) * np.exp(-t / 0.105)
        body = base.band(rng, len(t), 110, 550) * np.exp(-t / 0.049)
        crush = base.band(rng, len(t), 750, 4200) * np.exp(-t / 0.013)
        phase = 2 * np.pi * (43 * t + 24 * 0.025 * (1 - np.exp(-t / 0.025)))
        mass = np.sin(phase) * np.exp(-t / 0.105)
        modes = base.modal(0.51, [109, 173, 287], [.25, .14, .065], [.065, .045, .025])
        hit = .62 * low + .27 * body + .065 * crush + .40 * mass + modes
        hit *= 1 - np.exp(-t / .0018)
        base.put(x, at, base.edge(hit, .001, .055), gain)
        # Small, scattered earth particles decay under the main thud.
        for delay, level in [(.028, .030), (.057, .018), (.095, .009)]:
            base.put(x, at + delay, base.rub(rng, .055, 350, 2500, 1.8), level * gain)
    return base.edge(x - np.mean(x), .003, .045)


def blades(seed=6228):
    rng = np.random.default_rng(seed)
    x = np.zeros(round(.70 * RATE))
    for at, gain, tune in [(.025, 1.0, 1.0), (.276, .86, 1.037)]:
        t = np.arange(round(.395 * RATE)) / RATE
        # Inharmonic steel modes with an immediate hard contact and short ring.
        freqs = np.array([583, 973, 1549, 2383, 3491, 5039, 6947]) * tune
        amps = [.52, .66, .47, .31, .20, .105, .045]
        decays = [.115, .165, .130, .100, .070, .043, .025]
        ring = np.zeros(len(t))
        for f, amp, decay in zip(freqs, amps, decays):
            ring += amp * np.sin(2 * np.pi * f * t) * np.exp(-t / decay)
        contact = base.band(rng, len(t), 1700, 10500) * np.exp(-t / .0038)
        body = base.band(rng, len(t), 450, 1800) * np.exp(-t / .010)
        hit = ring + .20 * contact + .10 * body
        base.put(x, at, base.edge(hit, .0008, .045), gain)
    return base.edge(x - np.mean(x), .003, .030)


def main():
    manifest = OUT / "revision_manifest_take02.json"
    if manifest.exists():
        raise FileExistsError(manifest)
    script = GAME / "script.rpy"
    script_sha = base.digest(script)
    records = []
    for stem, cue, synth, peak, intention in [
        ("battle_spider_steps_heavy", "SFX24_HEAVY_VARIANT", heavy, -17.0,
         "巨物落地：寬頻低沉撞擊、短地面共振與碎土，保留兩次落地與原長度。"),
        ("battle_kamikiri_blades", "SFX28_KAMIKIRI_BLADES", blades, -18.5,
         "鐮刃交錯：兩次硬金屬接觸、不等間距金屬共鳴及短尾音，移除原布面般長摩擦。"),
    ]:
        target = GAME / "audio/sfx/battle" / (stem + ".ogg")
        prior = OUT / (stem + "_take01.ogg")
        if base.digest(target) != base.digest(prior):
            raise RuntimeError("Game asset no longer matches take01: " + stem)
        x = synth()
        x *= 10 ** (peak / 20) / np.max(np.abs(x))
        wav = HERE / (stem + "_take02.wav")
        ogg = OUT / (stem + "_take02.ogg")
        subprocess.run(["ffmpeg", "-v", "error", "-n", "-f", "f32le", "-ar", str(RATE),
                        "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", str(wav)],
                       input=x.astype("<f4").tobytes(), check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-n", "-i", str(wav), "-ar", "44100",
                        "-ac", "1", "-c:a", "libvorbis", "-q:a", "6", str(ogg)], check=True)
        pcm = np.frombuffer(subprocess.check_output([
            "ffmpeg", "-v", "error", "-i", str(ogg), "-f", "f32le", "-" ]), dtype="<f4")
        rec = dict(date="2026-10-19", cue=cue, name=stem, take="take02", intention=intention,
                   method="original procedural synthesis; no external recording, voice or model",
                   seed=6224 if synth is heavy else 6228,
                   status="integrated_scene_audition_pending", formally_adopted=False,
                   duration_seconds=len(x)/RATE, sample_peak_target_dbfs=peak,
                   decoded_peak_dbfs=base.db(np.max(np.abs(pcm))),
                   decoded_rms_dbfs=base.db(np.sqrt(np.mean(pcm.astype(float)**2))),
                   source=Path(__file__).name, source_sha256=base.digest(Path(__file__)),
                   wav=dict(file=wav.name, sha256=base.digest(wav), sample_rate=RATE, channels=1, bits=24),
                   ogg=dict(file=ogg.name, sha256=base.digest(ogg), sample_rate=44100, channels=1),
                   previous_ogg_sha256=base.digest(prior),
                   game_file=target.relative_to(base.ROOT).as_posix())
        base.save(OUT / (stem + "_take02.json"), rec)
        records.append(rec)
    # Export both revisions before changing the active development assets.
    for rec in records:
        shutil.copy2(OUT / rec["ogg"]["file"], base.ROOT / rec["game_file"])
    base.save(manifest, dict(date="2026-10-19", batch="BATCH05_FOREST_BATTLE",
                            user_feedback=["土蜘蛛重步不夠像重物落地、不夠重", "鐮刀交錯應該是金屬碰撞，目前像布面摩擦"],
                            candidates=records, script_sha256_before=script_sha,
                            script_sha256_after=base.digest(script),
                            game_text_or_trigger_changed=False,
                            review_entry="script.rpy:1114", formally_adopted=False))
    print(json.dumps([dict(name=r["name"], duration=r["duration_seconds"],
                           peak=r["decoded_peak_dbfs"]) for r in records], ensure_ascii=False))


if __name__ == "__main__":
    main()
