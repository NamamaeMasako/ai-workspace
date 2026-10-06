# 驚蟄 / build.rpy
# 發行包只排除已逐項確認未引用的素材；避免寬泛 glob 誤傷正式圖。

init python:
    # 編輯器與本機備份檔。
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)

    # UI 已統一使用 NotoSansTC-VF.ttf。
    build.classify("game/SourceHanSansLite.ttf", None)

    # 未引用的 Ren'Py 教學範例資產；逐項排除，禁止使用 game/images/*。
    for unused_tutorial_asset in (
        "bar empty hover.png",
        "bar empty idle.png",
        "bar full hover.png",
        "bar full idle.png",
        "bar thumb hover.png",
        "bar thumb idle.png",
        "bg cave.jpg",
        "bg panorama.webp",
        "bg pong field.png",
        "bg washington.jpg",
        "bg whitehouse.jpg",
        "button glossy hover.png",
        "button glossy idle.png",
        "check_foreground.png",
        "check_selected_foreground.png",
        "concert1.png",
        "concert2.png",
        "concert3.png",
        "eileen concerned.png",
        "eileen happy.png",
        "eileen vhappy.png",
        "hover_background.png",
        "idle_background.png",
        "imagedissolve circleiris.png",
        "imagedissolve circlewipe.png",
        "imagedissolve dream.png",
        "imagedissolve teleport.png",
        "imagemap ground.png",
        "imagemap hover.png",
        "imagemap volume hover.png",
        "imagemap volume idle.png",
        "imagemap volume insensitive.png",
        "imagemap volume selected_hover.png",
        "imagemap volume selected_idle.png",
        "launcher distribute.png",
        "launcher step1.webp",
        "launcher step2.webp",
        "launcher step3.webp",
        "launcher step4.webp",
        "launcher step5.webp",
        "launcher translate.png",
        "logo base.png",
        "logo bw.png",
        "logo solid.png",
        "lucy happy.png",
        "lucy mad.png",
        "magic.png",
        "ninepatch paper.png",
        "ninepatch.png",
        "popup hrpprefs.png",
        "popup prefs.png",
        "popup save.png",
        "spotlight.png",
    ):
        build.classify("game/images/" + unused_tutorial_asset, None)

    # 候選背景不進正式包。
    for unused_candidate in (
        "inn_dining_morning_candidate_v0.1.png",
        "inn_lobby_twilight_candidate_v0.1.png",
        "inn_lobby_twilight_candidate_v0.2.png",
    ):
        build.classify("game/images/backgrounds/" + unused_candidate, None)

    # 這四張角色根目錄副本與實際使用的 thigh 圖逐位元相同。
    for duplicate_character_asset in (
        "kamikiri_ready_3q_full_right_sword_left_forearm_blade.png",
        "kamikiri_attack_forward_full_right_sword_left_forearm_blade.png",
        "kamikiri_empowered_ready_3q_full_right_sword_left_forearm_blade.png",
        "kamikiri_empowered_attack_forward_full_right_sword_left_forearm_blade.png",
    ):
        build.classify("game/images/characters/" + duplicate_character_asset, None)
