"""Insert sound commands only into the original chapter-eight flow."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=ROOT/'02_素材/音訊/候選/BATCH07_TRUE_END'
SCRIPT=ROOT/'03_開發/JingZhe/game/script.rpy'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def play(path,volume=1):return f'play sound "audio/sfx/{path}.ogg"'+(f' volume {volume}' if volume!=1 else '')
def queue(path,volume=1):return play(path,volume).replace('play sound','queue sound',1)


def main():
    destination=OUT/'scene_integration_take01.json'
    if destination.exists():raise FileExistsError(destination)
    raw=SCRIPT.read_bytes();text=raw.decode('utf-8-sig');newline='\r\n' if '\r\n' in text else '\n'
    text=text.replace('\r\n','\n');initial=text
    start=text.index('label chapter_8_choice:');chunk=text[start:];rows=[];inserted=[]
    def add(trigger,commands,label,anchor=None):
        nonlocal chunk
        target=anchor or '    narrator "'+trigger+'"'
        if chunk.count(target)!=1:raise ValueError((trigger,chunk.count(target)))
        chunk=chunk.replace(target,''.join('    '+c+'\n' for c in commands)+target,1)
        inserted.extend('    '+c for c in commands)
        rows.append(dict(label=label,trigger=trigger,commands=commands,anchor=target))
    add('同樣的走廊，同樣的燈。',['stop sound fadeout 0.12'],'選擇前清除殘留短音，保留無BGM')
    add('選下「把卡留給自己」後',[play('magic/magic_black_card_pulse',.7)],'留卡時淡共鳴',
        anchor='    show hanami concerned at zh_far_left')
    add('他把卡收進袖口，像把一把刀藏回鞘裡。',[play('world/world_black_card_stow',.8)],'黑卡收進袖口')
    add('入夜後，驚蟄獨自來到林道。',[play('world/world_footstep_wet',.65)],'獨自進林道')
    add('他點燃煙斗。',[play('magic/magic_kiseru_ignite',.8)],'點燃苦香')
    add('第一口下去，他就覺得喉嚨像被砂紙磨過。',[play('magic/magic_kiseru_draw',.7)],'第一口苦香')
    add('第二口開始，胸腔會慢半拍，像心臟被人用指尖按住。',[play('magic/magic_kiseru_draw',.6)],'第二口苦香')
    add('髮切與大百足在林道兩側的陰影裡醒來。',[play('magic/magic_insect_summon',.8)],'苦香召出式神')
    add('他踏進去時，連呼吸都被濕度磨鈍。',[play('world/world_footstep_wet',.65)],'踏入黑暗林道')
    add('土蜘蛛先現身。',[play('battle/battle_spider_steps_heavy')],'土蜘蛛重步現身')
    add('驚蟄吐出一口煙。',[play('magic/magic_kiseru_blow',.8)],'交戰前吐煙')
    add('髮切的鐮光先到。',[play('battle/battle_kamikiri_blades')],'髮切先攻')
    add('大百足的撞擊緊跟其後。',[play('battle/battle_omukade_armor_move'),queue('battle/battle_omukade_impact')],'百足甲片→撞擊')
    add('土蜘蛛迎上來，節肢拍地，震得泥土翻起。',[play('battle/battle_spider_steps_heavy',.95)],'蛛腳拍地')
    add('絡新婦在移動。',[play('battle/battle_silk_whisper',.7)],'絡新婦移動細絲')
    add('髮切忽然一折，像聽見了另一個命令，鐮刃往樹梢一掃。',[play('battle/battle_kamikiri_blades',.9)],'鐮刃掃向樹梢')
    add('驚蟄的肩一沉。',[play('battle/battle_silk_whisper',.8)],'絲線套住肩頭')
    add('大百足猛地回身，把那道影子撞開。',[play('battle/battle_omukade_armor_move',.85),queue('battle/battle_omukade_impact',.9)],'百足回身撞開黑影')
    add('他趁空隙把煙吸進肺裡。',[play('magic/magic_kiseru_draw',.75)],'空隙吸煙')
    add('土蜘蛛趁機衝撞。',[play('battle/battle_omukade_impact',.85)],'土蜘蛛重物撞擊')
    add('腳跟踩到一塊濕滑的石。',[play('world/world_footstep_wet',.35)],'退步踩濕石')
    add('他把香捏碎。',[play('world/world_herb_crush')],'捏碎苦香')
    add('髮切的鐮刃刺入土蜘蛛節肢的縫。',[play('battle/battle_kamikiri_blades',.9)],'鐮刃刺入節肢縫')
    add('大百足用整個身軀壓上去。',[play('battle/battle_omukade_armor_move'),queue('battle/battle_omukade_impact',.9)],'百足全身壓上')
    add('土蜘蛛的嘶聲像碎木。',[play('battle/battle_tsuchigumo_hiss')],'土蜘蛛短嘶聲')
    add('牠倒下時，地面像沉了一口氣。',[play('battle/battle_omukade_impact',.65)],'巨蛛倒下')
    add('他吐出一口煙，胸口卻像被撕開一條細縫。',[play('magic/magic_kiseru_blow',.65)],'毒性反噬時吐煙')
    add('絡新婦終於現形。',[play('battle/battle_silk_whisper',.8)],'絡新婦現形細絲')
    add('另一半落在他的肋側。',[play('battle/battle_body_hit_dull',.8)],'肋側受傷鈍響')
    add('那一下讓他的手腕也發出一聲鈍響。',[play('battle/battle_body_hit_dull',.6)],'手腕短鈍響')
    add('他吐出最後一口煙。',[play('magic/magic_kiseru_blow',.65)],'最後吐煙')
    add('髮切從她側面切入。',[play('battle/battle_kamikiri_blades',.9)],'髮切側面切入')
    add('黑影碎開，像被剪斷的絲。',[play('battle/battle_silk_cut',.9)],'切斷黑影')
    add('絡新婦倒下時，還在笑。',[play('battle/battle_body_fall_soft',.5)],'絡新婦倒地')
    add('驚蟄跪下去。',['stop sound fadeout 0.12',play('world/world_cloth_soft',.8)],'跪下時衣料')
    add('膝蓋撞到石頭，痛得他眼前發黑。',[play('battle/battle_body_hit_dull',.8)],'膝蓋碰石')
    add('遠處有腳步聲。',[play('world/world_footstep_wet',.45),queue('world/world_footstep_wet',.7)],'兩人由遠而近趕到')
    add('她伸手去摸他的袖口。',[play('world/world_cloth_soft')],'花見摸袖口')
    add('她要撕。',[play('magic/magic_black_card_pulse_hold',.8)],'準備撕卡、延長共鳴')
    add('驚蟄抓住她的手腕。',['stop sound fadeout 0.08'],'抓腕時中止共鳴、不撕卡')
    add('他靠著樹根，眼皮沉下來。',[play('world/world_cloth_soft',.65)],'靠樹根的衣料')
    add('卡片忽然變輕。',[play('magic/magic_black_card_pulse',.45)],'卡片變輕的淡共鳴')
    add('下一瞬，夜色被撕開一條縫。',[play('magic/magic_night_rift')],'夜縫與影之魔女登場')
    add('卻咳出一口血。',[play('battle/battle_cough_blood')],'全段唯一一次咳血')
    add('她把卡片收回袖中。',[play('world/world_black_card_stow',.7)],'影之魔女收卡')
    add('回去吧。',[play('world/world_footstep_wet',.4)],'一起回去的短腳步',anchor='    jingzhe "回去吧。"')
    add('結局淡出',['stop sound fadeout 0.2'],'結局清除短音',anchor='label end_game:')
    # The end-game label needs its statement inside the label, not before it.
    chunk=chunk.replace('    stop sound fadeout 0.2\nlabel end_game:',
                        'label end_game:\n    stop sound fadeout 0.2',1)
    text=text[:start]+chunk
    original_lines=initial.splitlines();new_lines=text.splitlines();it=iter(new_lines)
    for line in original_lines:
        for candidate in it:
            if candidate==line:break
            if not re.match(r'^\s*(?:play|queue|stop) sound\b',candidate):raise RuntimeError('Non-sound addition')
        else:raise RuntimeError('Original line removed')
    # Include the added end-game stop after the final original label.
    count=len(new_lines)-len(original_lines)
    if count!=len(inserted):raise RuntimeError('Line count mismatch')
    updated=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\n',newline).encode('utf-8')
    SCRIPT.write_bytes(updated)
    for row in rows:
        pos=text.index(row.pop('anchor'),start)
        row['script_line']=text[:pos].count('\n')+1
    rows.sort(key=lambda r:r['script_line'])
    entry=next(r['script_line'] for r in rows if r['trigger']=='同樣的走廊，同樣的燈。')
    manifest=json.loads((OUT/'generation_manifest_take01.json').read_text(encoding='utf-8'))
    save(destination,dict(date='2026-10-19',batch='BATCH07_TRUE_END',status='awaiting_user_whole_scene_confirmation',
        formally_adopted=False,primary_cues=2,variants=3,new_files=5,assets=manifest['candidates'],
        ordered_checklist=rows,added_sound_statements=count,
        script_sha256_before=sha(raw),script_sha256_after=sha(updated),text_staging_music_and_branches_unchanged=True,
        review_entry=f'script.rpy:{entry}',review_end='清晨桌上煙斗還留苦味，接原結局黑底',
        silence_preserved=['選項前無BGM','抓腕時中止共鳴、不播放撕卡','不加額外喘息哭聲或笑聲',
                           '咳血只在明寫句子一次','夜縫只用一次、治療與離場不加新魔法聲','風雨返回不加循環底聲'],
        temporary_review_ui=False,release_rebuilt=False,version_changed=False))
    print(json.dumps(dict(added_sound_statements=count,points=len(rows),entry=entry),ensure_ascii=False))


if __name__=='__main__':main()
