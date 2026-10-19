label after_warp:
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

label _jz_b5_hanami_1:
    if renpy.music.get_playing(channel="music") != "<loop 3.75>audio/music/bgm_silk_under_door.ogg":
        play music "<loop 3.75>audio/music/bgm_silk_under_door.ogg" loop fadeout 1.5 fadein 1.5

    scene bg inn_hall_evening
    with dissolve

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.85
    queue sound "audio/sfx/magic/magic_black_card_pulse.ogg" volume 0.7
    narrator "驚蟄從袖中取出那張黑色卡片，交到花見手裡。"

    show jingzhe stern at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show hanami concerned at zh_far_left
    hanami "只保護我？"

    jingzhe "嗯。"

    show yumemi worried at zh_far_right
    yumemi "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    jingzhe "我會想辦法。"

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.8
    narrator "花見嘆了口氣，接著把卡片收進衣內，像是收下一種承諾。"
    show hanami determined at zh_far_left

    hanami "我會保管好。"


    narrator "驚蟄沒有再多看，轉身走向夜色。"

    narrator "他不想讓自己猶豫。"

    scene bg forest_path_night
    with fade

    play sound "audio/sfx/world/world_footstep_wet.ogg"
    queue sound "audio/sfx/magic/magic_kiseru_ember.ogg" volume 0.75
    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    play sound "audio/sfx/magic/magic_kiseru_blow.ogg"
    narrator "他吹起煙草。"

    play sound "audio/sfx/magic/magic_insect_summon.ogg"
    show cg chapter7_shikigami_summon
    with dissolve
    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "是同伴。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙刃如螳螂的捕捉前足般交錯。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    hide cg
    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_jingzhe_small zorder 3
    show hanami battle_full at zh_battle_hanami_foreground zorder 3
    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg"
    narrator "土蜘蛛先現身，像一堵牆，從樹影中慢慢逼近。"

    queue sound "audio/sfx/battle/battle_tsuchigumo_hiss.ogg"
    narrator "牠每一步都讓地面微震，像在逼近判決。"

    play music "<loop 3.4285625>audio/music/bgm_forest_assault.ogg" loop fadeout 1.5 fadein 0.5

    show cg chapter7_tsuchigumo_assault zorder 100
    with dissolve
    show kamikiri attack at zh_battle_kamikiri_front zorder 5
    play sound "audio/sfx/battle/battle_kamikiri_blades.ogg"
    narrator "髮切先衝上去，鐮刃交錯，逼得牠抬頭防守。"

    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg" volume 0.9
    narrator "牠的節肢拍地，揚起一層灰。"

    show omukade ready at zh_battle_omukade_coiled_back zorder 1
    play sound "audio/sfx/battle/battle_omukade_armor_move.ogg"
    queue sound "audio/sfx/battle/battle_omukade_impact.ogg"
    narrator "大百足自側面猛撞，震得地面一沉。"

    play sound "audio/sfx/battle/battle_naginata_whoosh.ogg"
    queue sound "<silence 0.04>"
    queue sound "audio/sfx/battle/battle_naginata_armor_hit.ogg"
    narrator "花見趁空隙切入，薙刀的刃光在牠的節肢上割出白痕。"

    narrator "她的呼吸短促，卻不退。"

    play sound "audio/sfx/magic/magic_insect_summon.ogg" volume 0.45
    narrator "驚蟄的蟲影纏住牠的視線，逼得土蜘蛛退到樹根間。"

    stop sound fadeout 0.15
    jump _jz_b5_menu

label _jz_b5_yumemi_1:
    if renpy.music.get_playing(channel="music") != "<loop 3.75>audio/music/bgm_silk_under_door.ogg":
        play music "<loop 3.75>audio/music/bgm_silk_under_door.ogg" loop fadeout 1.5 fadein 1.5

    scene bg inn_hall_evening
    with dissolve

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.85
    queue sound "audio/sfx/magic/magic_black_card_pulse.ogg" volume 0.7
    narrator "驚蟄從袖中取出那張黑色卡片，交到夢見手裡。"

    show jingzhe stern at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show yumemi worried at zh_far_right
    yumemi "只保護我……嗎？"

    jingzhe "嗯。"

    show hanami concerned at zh_far_left
    hanami "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    jingzhe "我會想辦法。"

    show yumemi determined at zh_far_right
    yumemi "我會小心的。"

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.8
    narrator "她把卡片收進衣內，像是抱著一件不能說的祕密。"

    show jingzhe wary at zh_center
    narrator "驚蟄看著她的手指收緊，又鬆開。"

    narrator "那一瞬間，他差點想把卡抽回來。"

    narrator "但他知道，猶豫會把人推向更壞的選項。"

    narrator "他轉身走向夜色。"

    scene bg forest_path_night
    with fade

    play sound "audio/sfx/world/world_footstep_wet.ogg"
    queue sound "audio/sfx/magic/magic_kiseru_ember.ogg" volume 0.75
    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    play sound "audio/sfx/magic/magic_kiseru_blow.ogg"
    narrator "他吹起煙草。"

    play sound "audio/sfx/magic/magic_insect_summon.ogg"
    show cg chapter7_shikigami_summon
    with dissolve
    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "自己人。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙刃如螳螂的捕捉前足般交錯。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    hide cg
    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_jingzhe_small zorder 3
    show hanami battle_full at zh_battle_hanami_foreground zorder 3
    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg"
    narrator "土蜘蛛先現身，像一座移動的山。"

    queue sound "audio/sfx/battle/battle_tsuchigumo_hiss.ogg"
    narrator "牠的影子蓋下來時，連空氣都變重。"

    play music "<loop 3.4285625>audio/music/bgm_forest_assault.ogg" loop fadeout 1.5 fadein 0.5

    show cg chapter7_tsuchigumo_assault zorder 100
    with dissolve
    show omukade ready at zh_battle_omukade_coiled_back zorder 1
    show kamikiri attack at zh_battle_kamikiri_front zorder 5
    play sound "audio/sfx/battle/battle_kamikiri_blades.ogg"
    queue sound "audio/sfx/battle/battle_omukade_armor_move.ogg"
    queue sound "audio/sfx/battle/battle_omukade_impact.ogg"
    narrator "髮切牽住牠的正面，大百足自側面猛撞。"

    narrator "花見握緊薙刀，步伐大開大合。"

    play sound "audio/sfx/battle/battle_naginata_whoosh.ogg"
    narrator "她的攻勢猛烈，卻也留下空隙。"

    narrator "驚蟄看見了——也來不及提醒。"

    play sound "audio/sfx/battle/battle_silk_whisper.ogg"
    narrator "絡新婦就在那道空隙裡出現。"

    scene cg chapter7_jorogumo_ambush_hanami
    with dissolve

    play sound "audio/sfx/battle/battle_silk_cut.ogg" volume 0.65
    narrator "一抹細影掠過花見的肩。"

    narrator "像蜘蛛絲輕輕擦過皮膚，連痛都來得很晚。"

    scene bg forest_path_night
    with dissolve

    show hanami injured at zh_right
    narrator "花見的身體晃了一下，像被拉住了線。"

    narrator "她咬住一聲喘息，還想把薙刀舉回原位。"

    narrator "驚蟄想回頭，卻被土蜘蛛逼住。"

    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg" volume 0.9
    narrator "牠的節肢拍地，揚起一層灰，把視線切碎。"

    narrator "他只能把那一瞬間記在心裡。"

    play sound "audio/sfx/battle/battle_omukade_impact.ogg" volume 0.55
    narrator "最後，土蜘蛛倒下。"

    narrator "土蜘蛛倒下的瞬間，絡新婦的影子已經往樹梢更深處退。"

    jingzhe "……別想走。"

    show kamikiri attack at zh_center
    play sound "audio/sfx/battle/battle_kamikiri_blades.ogg" volume 0.85
    narrator "髮切像被放出的刀光，追著那道細影竄上去。"

    play sound "audio/sfx/battle/battle_silk_cut.ogg"
    narrator "鐮刃一閃，黑影斷成幾截，落地時只剩一圈散開的絲。"

    stop sound fadeout 0.15
    jump _jz_b5_menu

label _jz_b5_hanami_2:
    if renpy.music.get_playing(channel="music") != "<loop 3.75>audio/music/bgm_silk_under_door.ogg":
        play music "<loop 3.75>audio/music/bgm_silk_under_door.ogg" loop fadeout 1.5 fadein 1.5

    scene bg inn_hall_evening
    with dissolve

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.85
    queue sound "audio/sfx/magic/magic_black_card_pulse.ogg" volume 0.7
    narrator "驚蟄從袖中取出那張黑色卡片，交到花見手裡。"

    show jingzhe wary at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show hanami concerned at zh_far_left
    hanami "只保護我？"

    jingzhe "嗯。"

    show yumemi worried at zh_far_right
    yumemi "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    narrator "明明只是同樣的問題，他胸口卻像被什麼輕輕拽了一下。"

    jingzhe "我會想辦法。"

    hanami "你講這種話的時候，最不可信。"

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.8
    narrator "她低聲說完，還是把卡片收進衣內，像是收下一種承諾。"

    hanami "我會保管好。"

    show jingzhe grief at zh_center
    narrator "驚蟄盯著那個動作。"

    narrator "他說不出原因。"

    narrator "可心口那一下抽緊太真，真得像他已經為這個動作後悔過一次。"

    narrator "只是覺得——這張卡不該離開他的手。"

    jingzhe "……拿好。別逞強。"

    narrator "話出口的瞬間，他自己都愣了一下。"

    narrator "他平常不會用這種語氣說話。"

    narrator "像是有一段不屬於此刻的記憶，正隔著薄霧貼在他皮膚上。"

    narrator "他不去抓那霧裡的畫面，只把煙斗握緊。"

    scene bg forest_path_night
    with fade

    play sound "audio/sfx/world/world_footstep_wet.ogg"
    queue sound "audio/sfx/magic/magic_kiseru_ember.ogg" volume 0.75
    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    play sound "audio/sfx/magic/magic_kiseru_blow.ogg"
    narrator "他吹起煙草。"

    play sound "audio/sfx/magic/magic_insect_summon.ogg"
    show cg chapter7_shikigami_summon
    with dissolve
    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "是同伴。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙刃如螳螂的捕捉前足般交錯。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    hide cg
    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_jingzhe_small zorder 3
    show hanami battle_full at zh_battle_hanami_foreground zorder 3
    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg"
    narrator "土蜘蛛先現身，像一堵牆，從樹影中慢慢逼近。"

    queue sound "audio/sfx/battle/battle_tsuchigumo_hiss.ogg"
    narrator "牠每一步都讓地面微震，像在逼近判決。"

    play music "<loop 3.4285625>audio/music/bgm_forest_assault.ogg" loop fadeout 1.5 fadein 0.5

    show cg chapter7_tsuchigumo_assault zorder 100
    with dissolve
    show kamikiri attack at zh_battle_kamikiri_front zorder 5
    play sound "audio/sfx/battle/battle_kamikiri_blades.ogg"
    narrator "髮切先衝上去，鐮刃交錯，逼得牠抬頭防守。"

    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg" volume 0.9
    narrator "牠的節肢拍地，揚起一層灰。"

    show omukade ready at zh_battle_omukade_coiled_back zorder 1
    play sound "audio/sfx/battle/battle_omukade_armor_move.ogg"
    queue sound "audio/sfx/battle/battle_omukade_impact.ogg"
    narrator "大百足自側面猛撞，震得地面一沉。"

    play sound "audio/sfx/battle/battle_naginata_whoosh.ogg"
    queue sound "<silence 0.04>"
    queue sound "audio/sfx/battle/battle_naginata_armor_hit.ogg"
    narrator "花見趁空隙切入，薙刀的刃光在牠的節肢上割出白痕。"

    narrator "驚蟄下意識往前一步，像要把她往後推。"

    jingzhe "別太前——"

    narrator "他只說出半句。"

    narrator "花見沒有回頭，卻像聽懂了。"

    narrator "她的步伐稍微收了一點，依舊不退。"

    play sound "audio/sfx/magic/magic_insect_summon.ogg" volume 0.45
    narrator "驚蟄的蟲影纏住牠的視線，逼得土蜘蛛退到樹根間。"

    stop sound fadeout 0.15
    jump _jz_b5_menu

label _jz_b5_yumemi_2:
    if renpy.music.get_playing(channel="music") != "<loop 3.75>audio/music/bgm_silk_under_door.ogg":
        play music "<loop 3.75>audio/music/bgm_silk_under_door.ogg" loop fadeout 1.5 fadein 1.5

    scene bg inn_hall_evening
    with dissolve

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.85
    queue sound "audio/sfx/magic/magic_black_card_pulse.ogg" volume 0.7
    narrator "驚蟄從袖中取出那張黑色卡片，交到夢見手裡。"

    show jingzhe wary at zh_center
    jingzhe "這是影之魔女的卡片，它會保護你。"

    show yumemi worried at zh_far_right
    yumemi "只保護我……嗎？"

    jingzhe "嗯。"

    show hanami concerned at zh_far_left
    hanami "那你呢？"

    narrator "驚蟄沒有立刻回答。"

    narrator "明明只是同樣的問題，他卻覺得指節在發冷。"

    jingzhe "我會想辦法。"

    show yumemi determined at zh_far_right
    yumemi "我會小心的。"

    play sound "audio/sfx/world/world_black_card_stow.ogg" volume 0.8
    narrator "她把卡片收進衣內，像是抱著一件不能說的祕密。"

    show jingzhe grief at zh_center
    narrator "驚蟄看著她的手指收緊，又鬆開。"

    narrator "像是有一段不屬於此刻的記憶，正隔著薄霧貼在他皮膚上。"

    narrator "他不去想那霧裡是什麼。"

    narrator "可指尖還是先一步收緊，像身體比他更早記得失去是什麼。"

    narrator "那一瞬間，他差點想把卡抽回來。"

    narrator "但他知道，猶豫會把人推向更壞的選項。"

    narrator "他轉身走向夜色。"

    scene bg forest_path_night
    with fade

    play sound "audio/sfx/world/world_footstep_wet.ogg"
    queue sound "audio/sfx/magic/magic_kiseru_ember.ogg" volume 0.75
    narrator "林道很黑，只有煙斗的火光在一點一點前行。"

    show jingzhe battle at zh_left
    play sound "audio/sfx/magic/magic_kiseru_blow.ogg"
    narrator "他吹起煙草。"

    play sound "audio/sfx/magic/magic_insect_summon.ogg"
    show cg chapter7_shikigami_summon
    with dissolve
    narrator "髮切與大百足在黑暗中竄出，像是應召而來的影。"

    narrator "花見下意識抬薙刀，眼神一瞬間變冷。"

    jingzhe "自己人。"

    narrator "他只說了三個字。"

    narrator "花見的手稍稍放鬆，但仍保持戒備。"

    narrator "髮切是披著人形的螳螂妖怪，雙刃如螳螂的捕捉前足般交錯。"

    narrator "大百足的殼厚得像甲，衝撞時帶著低沉的震響。"

    narrator "他們抵達林道盡頭的空地。"

    narrator "風在枯樹間打旋，地面有被翻動過的痕跡。"

    hide cg
    show tsuchigumo attack at zh_battle_monster_left
    show jingzhe battle at zh_battle_party_jingzhe_small zorder 3
    show hanami battle_full at zh_battle_hanami_foreground zorder 3
    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg"
    narrator "土蜘蛛先現身，像一座移動的山。"

    queue sound "audio/sfx/battle/battle_tsuchigumo_hiss.ogg"
    narrator "牠的影子蓋下來時，連空氣都變重。"

    play music "<loop 3.4285625>audio/music/bgm_forest_assault.ogg" loop fadeout 1.5 fadein 0.5

    show cg chapter7_tsuchigumo_assault zorder 100
    with dissolve
    show omukade ready at zh_battle_omukade_coiled_back zorder 1
    show kamikiri attack at zh_battle_kamikiri_front zorder 5
    play sound "audio/sfx/battle/battle_kamikiri_blades.ogg"
    queue sound "audio/sfx/battle/battle_omukade_armor_move.ogg"
    queue sound "audio/sfx/battle/battle_omukade_impact.ogg"
    narrator "髮切牽住牠的正面，大百足自側面猛撞。"

    narrator "花見握緊薙刀，步伐大開大合。"

    play sound "audio/sfx/battle/battle_naginata_whoosh.ogg"
    narrator "她的攻勢猛烈，卻也留下空隙。"

    narrator "驚蟄看見了——也來不及提醒。"

    narrator "他甚至有一瞬間覺得：自己早就知道會發生什麼。"

    narrator "那種預感太真，像是有人把答案塞進他舌根底下。"

    play sound "audio/sfx/battle/battle_silk_whisper.ogg"
    narrator "絡新婦就在那道空隙裡出現。"

    scene cg chapter7_jorogumo_ambush_hanami
    with dissolve

    play sound "audio/sfx/battle/battle_silk_cut.ogg" volume 0.65
    narrator "一抹細影掠過花見的肩。"

    narrator "像蜘蛛絲輕輕擦過皮膚，連痛都來得很晚。"

    scene bg forest_path_night
    with dissolve

    show hanami injured at zh_right
    narrator "花見的身體晃了一下，像被拉住了線。"

    narrator "她咬住一聲喘息，還想把薙刀舉回原位。"

    narrator "驚蟄想回頭，卻被土蜘蛛逼住。"

    play sound "audio/sfx/battle/battle_spider_steps_heavy.ogg" volume 0.9
    narrator "牠的節肢拍地，揚起一層灰，把視線切碎。"

    narrator "他只能把那一瞬間記在心裡。"

    play sound "audio/sfx/battle/battle_omukade_impact.ogg" volume 0.55
    narrator "最後，土蜘蛛倒下。"

    narrator "土蜘蛛倒下的瞬間，絡新婦的影子已經往樹梢更深處退。"

    jingzhe "……別想走。"

    show kamikiri attack at zh_center
    play sound "audio/sfx/battle/battle_kamikiri_blades.ogg" volume 0.85
    narrator "髮切像被放出的刀光，追著那道細影竄上去。"

    play sound "audio/sfx/battle/battle_silk_cut.ogg"
    narrator "鐮刃一閃，黑影斷成幾截，落地時只剩一圈散開的絲。"

    stop sound fadeout 0.15
    jump _jz_b5_menu

