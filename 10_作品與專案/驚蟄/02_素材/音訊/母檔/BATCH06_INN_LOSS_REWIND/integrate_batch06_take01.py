"""Add only sound statements to the four original chapter-seven continuations.
Preserve all text, staging, music, branch logic and user preferences.
"""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=ROOT/'02_素材/音訊/候選/BATCH06_INN_LOSS_REWIND'
SCRIPT=ROOT/'03_開發/JingZhe/game/script.rpy'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def play(path,volume=1):return f'play sound "audio/sfx/{path}.ogg"'+(f' volume {volume}' if volume!=1 else '')


def main():
    destination=OUT/'scene_integration_take01.json'
    if destination.exists():raise FileExistsError(destination)
    original=SCRIPT.read_bytes(); text=original.decode('utf-8-sig')
    newline='\r\n' if '\r\n' in text else '\n'
    text=text.replace('\r\n','\n'); initial=text
    routes={}; inserted=[]
    labels=['chapter_7_hanami_1','chapter_7_yumemi_1','chapter_7_hanami_2','chapter_7_yumemi_2']
    for route in labels:
        start=text.index('label '+route+':')
        m=re.search(r'^label ',text[start+1:],re.M)
        end=start+1+m.start() if m else len(text)
        chunk=text[start:end]; rows=[]
        def add(trigger,commands,label):
            nonlocal chunk
            anchor='    narrator "'+trigger+'"'
            if chunk.count(anchor)!=1:raise ValueError((route,trigger,chunk.count(anchor)))
            before=''.join('    '+command+'\n' for command in commands)
            chunk=chunk.replace(anchor,before+anchor,1)
            inserted.extend('    '+command for command in commands)
            rows.append(dict(label=label,trigger=trigger,commands=commands))
        if 'hanami' in route:
            add('木框被推回去時，發出一聲很輕的悶響。',[play('world/world_frame_thud_soft')],'木框輕悶響')
            add('夢見還來不及退後，燈火便猛地一晃。',[play('world/world_lamp_sway',.85)],'燈架晃動（沿用）')
            add('絡新婦將她拖進房裡，手掌覆住她的口鼻。',[play('world/world_cloth_drag_soft')],'拖動衣料')
            add('夢見的指尖抓住她的手腕，細微地掙動著。',[play('world/world_cloth_soft',.7)],'輕微掙動衣料')
            add('燈盞落在地上，火光晃了晃，沒有翻倒。',[play('world/world_lamp_drop')],'燈盞落地、無碎裂')
            add('夢見倒下時，幾乎沒有發出聲音。',[play('battle/battle_body_fall_soft',.18)],'幾乎無聲的倒下')
            add('土蜘蛛終於倒下。',[play('battle/battle_omukade_impact',.55)],'巨蛛倒下（沿用重物撞擊）')
            add('他們趕回月下庄。',[play('world/world_footstep_wet',.7)],'趕回庄門（沿用濕地腳步）')
            if route.endswith('_1'):
                add('花見的動作很大，很急，像把所有痛都甩出去。',[play('battle/battle_naginata_whoosh')],'庄門薙刀揮動')
                add('驚蟄的蟲影從側面纏住她的腳。',[play('magic/magic_insect_summon',.45)],'蟲影纏住退路')
                add('一息之間，黑影碎成兩半。',[play('battle/battle_silk_cut',.8)],'黑影斷裂')
            else:
                add('他的蟲影先一步纏住黑影的退路。',[play('magic/magic_insect_summon',.45)],'蟲影纏住退路')
                add('花見的薙刀落下，乾淨得像切斷一根線。',[play('battle/battle_naginata_whoosh')],'庄門薙刀落下')
                add('黑影碎成兩半。',[play('battle/battle_silk_cut',.8)],'黑影斷裂')
            add('他們衝進屋裡。',[play('world/world_footstep_wood',.65)],'衝進屋裡的短腳步')
            add('花見跪在地上，像被抽走了骨頭。',[play('battle/battle_body_fall_soft',.28)],'跪地輕觸地面')
            add('他把卡片從花見身上取回。',[play('world/world_black_card_stow',.8)],'取回黑卡的紙布聲')
        else:
            if route.endswith('_1'):
                add('花見倒下的聲音很輕。',[play('battle/battle_body_fall_soft',.55)],'花見輕輕倒地')
                add('他沒有多說，只把外衣蓋到她肩上。',[play('world/world_cloth_soft')],'外衣蓋肩')
                add('他抱著她走，木屐聲被雨吞得很低。',[play('world/world_footstep_wet',.35)],'低聲返庄腳步、無雨底聲')
            else:
                add('但這次，他幾乎是衝過去的。',[play('world/world_footstep_wet',.45)],'衝近花見的短腳步')
                # She is already lying on the leaves when seen; do not invent another fall.
                add('他把外衣蓋到她肩上，又替她把臉側的雨抹開。',[play('world/world_cloth_soft')],'外衣蓋肩')
                add('回月下庄的路比想像中更長。',[play('world/world_footstep_wet',.35)],'低聲返庄腳步、無雨底聲')
            add('然後，他把她抱起來。',[play('world/world_cloth_soft',.8)],'抱起時的衣料')
            add('他把花見放在榻榻米上。',[play('battle/battle_body_fall_soft',.22)],'輕放在榻榻米、無重摔')
            add('她跪下去，像是被抽走了力氣。',[play('battle/battle_body_fall_soft',.28)],'夢見跪下的輕觸地面')
            add('夢見抖著手，把卡片遞出去。',[play('world/world_black_card_stow',.8)],'遞出黑卡的紙布聲')
        add('撕開。',[play('magic/magic_black_card_tear')],'撕開黑卡')
        add('風停了一瞬。',['stop sound fadeout 0.10'],'撕卡後停止短音、回退保留安靜')
        text=text[:start]+chunk+text[end:];routes[route]=rows
    # Every original line remains in the same order. New lines are sound commands only.
    oldlines=initial.splitlines();newlines=text.splitlines();it=iter(newlines)
    for line in oldlines:
        for candidate in it:
            if candidate==line:break
            if not re.match(r'^\s*(?:play|queue|stop) sound\b',candidate):
                raise RuntimeError('Non-sound insertion encountered')
        else:raise RuntimeError('An original line was removed')
    additions=len(newlines)-len(oldlines)
    if additions!=len(inserted):raise RuntimeError('Unexpected line count')
    bom=b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b''
    updated=bom+text.replace('\n',newline).encode('utf-8')
    SCRIPT.write_bytes(updated)
    for route,rows in routes.items():
        for row in rows:
            # Find the trigger in its actual route after all insertions.
            pos=text.index('label '+route+':')
            triggerpos=text.index('    narrator "'+row['trigger']+'"',pos)
            row['script_line']=text[:triggerpos].count('\n')+1
        rows.sort(key=lambda r:r['script_line'])
    entry=text[:text.index('    narrator "另一邊，月下庄靜得像沒有住人。"')].count('\n')+1
    manifest=json.loads((OUT/'generation_manifest_take01.json').read_text(encoding='utf-8'))
    save(destination,dict(date='2026-10-19',batch='BATCH06_INN_LOSS_REWIND',
        status='awaiting_user_whole_scene_confirmation',formally_adopted=False,
        primary_cues=3,variants=3,new_files=6,assets=manifest['candidates'],
        routes=routes,added_sound_statements=additions,
        script_sha256_before=sha(original),script_sha256_after=sha(updated),
        text_staging_music_and_branches_unchanged=True,
        silence_preserved=['無聲穿過屋簷與抽屜搜尋','靜止細影與沒有回答','夢見倒下音量0.18',
                           '第二輪花見已倒在葉上、不重播倒地','耳語不製作人聲','回退不加入雨或風底聲'],
        review_entry=f'script.rpy:{entry}',review_end='第一輪撕卡後的黑底記憶倒流；第二輪到第八章留卡選項前',
        temporary_review_ui=False,release_rebuilt=False,version_changed=False))
    print(json.dumps(dict(added_sound_statements=additions,entry=entry,
                         points={k:len(v) for k,v in routes.items()}),ensure_ascii=False))


if __name__=='__main__':main()
