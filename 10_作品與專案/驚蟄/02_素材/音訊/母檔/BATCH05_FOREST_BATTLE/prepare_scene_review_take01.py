"""Build temporary route audition excerpts from the integrated chapter 7 source.
The deployed game keeps its original story flow. This review launch uses Ren'Py's
after_warp hook through a temporary search path, with copied battle prefixes only.
"""
from pathlib import Path
import hashlib, json, os, shutil

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'02_素材/音訊/候選/BATCH05_FOREST_BATTLE'
SCRIPT=ROOT/'03_開發/JingZhe/game/script.rpy'
TEMP=Path(os.environ['TEMP'])/'jz_batch05_probe_20261019'
TEMP.mkdir(exist_ok=True)
source=SCRIPT.read_text(encoding='utf-8')
review='''label after_warp:
    jump _jz_b5_menu

label _jz_b5_menu:
    stop sound fadeout 0.15
    stop music fadeout 0.5
    scene black
    with dissolve
    menu:
        "第七章林間交戰｜選擇試聽段落"
        "第一輪：交給花見":
            jump _jz_b5_hanami_1
        "第一輪：交給夢見":
            jump _jz_b5_yumemi_1
        "第二輪：交給花見":
            jump _jz_b5_hanami_2
        "第二輪：交給夢見":
            jump _jz_b5_yumemi_2
        "結束試聽":
            $ renpy.quit()

'''
manifest=[]
for short in ['hanami_1','yumemi_1','hanami_2','yumemi_2']:
    label='chapter_7_'+short
    start=source.index('label '+label+':')
    end=source.find('\nlabel ',start+1)
    body=source[start:end]
    marker='    play music "<loop 3.0>audio/music/bgm_inn_hunted.ogg"' if short.startswith('hanami') else '    stop music fadeout 1.5'
    prefix=body[:body.index(marker)]
    review+=prefix.replace('label '+label+':','label _jz_b5_'+short+':',1)
    review+='    jump _jz_b5_menu\n\n'
    manifest.append(dict(route=label,review_label='_jz_b5_'+short,
        source_first_line=source[:start].count('\n')+1,
        source_last_line=source[:start+len(prefix)].count('\n'),
        original_excerpt_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),
        source_dialogue_and_audio_unchanged=True))
target=OUT/'scene_review_take01.rpy'
with target.open('x',encoding='utf-8',newline='\n') as fp:fp.write(review)
shutil.copyfile(target,TEMP/'_jz_batch05_review.rpy')
record=dict(date='2026-10-19',batch='BATCH05_FOREST_BATTLE',
    method='Temporary after_warp route menu; actual integrated battle prefixes copied without changing dialogue or audio commands.',
    excludes='Inn attack, death, return, rewind and chapter 8 scenes remain for batches 06 and 07.',
    source_script_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
    review_file=target.name,review_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),routes=manifest,
    producer=Path(__file__).name)
(OUT/'scene_review_manifest_take01.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(TEMP)
