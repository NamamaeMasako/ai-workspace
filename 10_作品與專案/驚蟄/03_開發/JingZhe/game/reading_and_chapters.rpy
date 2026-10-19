# 2026-10-19 生前核可：黑底章名、通關後回看、閱讀設定。
# 現有對話字級34為上限；回看使用Ren'Py的獨立Replay上下文。

default persistent.jz_completed = False
default persistent.jz_reading_size = 34
default persistent.jz_textbox_opacity = 1.0
default jz_replay_stop_key = None

define jz_chapter_entries = (
    ("prologue", "序章", "月下庄", "prologue", "chapter_1"),
    ("chapter_1", "第一章", "留宿", "chapter_1", "chapter_2"),
    ("chapter_2", "第二章", "煙與孤影", "chapter_2", "chapter_3"),
    ("chapter_3", "第三章", "黑卡", "chapter_3", "chapter_4"),
    ("chapter_4", "第四章", "蛛影", "chapter_4", "chapter_5"),
    ("chapter_5", "第五章", "牽絲", "chapter_5", "chapter_6"),
    ("chapter_6", "第六章", "先手", "chapter_6", "chapter_7"),
    ("chapter_7", "第七章", "錯路", "chapter_7_choice_1", "chapter_8"),
    ("chapter_8", "第八章", "春雷", "chapter_8_choice", None),
)

init python:
    def jz_dialogue_size():
        return min(34, max(26, int(persistent.jz_reading_size or 34)))

    def jz_textbox_alpha():
        value = persistent.jz_textbox_opacity
        return min(1.0, max(0.2, float(1.0 if value is None else value)))

    def jz_textbox_background():
        # 正文與預覽共用底圖、對齊及透明度，避免預覽另有不透明墊底。
        return Transform(Image("gui/textbox.png", xalign=0.5, yalign=1.0),
                         alpha=jz_textbox_alpha())

    def jz_replay_unlocked():
        # 舊版已通關玩家可承接原結局標籤記錄，不需重新跑一遍。
        return bool(persistent.jz_completed or
                    renpy.seen_label("jz_ending_flow") or
                    renpy.seen_label("end_game"))

    def jz_start_chapter_replay(chapter_key):
        if not jz_replay_unlocked():
            return
        entry = next(e for e in jz_chapter_entries if e[0] == chapter_key)
        renpy.music.stop(channel="music", fadeout=0.3)
        renpy.music.set_volume(1.0, channel="music")
        try:
            Replay(entry[3], scope={
                "jz_replay_stop_key": entry[4],
                "first_route": None,
                "second_route": None,
                "quick_menu": True,
            }, locked=False)()
        finally:
            # 入口只在主選單；回看結束後恢復主選單音樂與正常通道音量。
            renpy.music.stop(channel="sound", fadeout=0.15)
            renpy.music.set_volume(1.0, channel="music")
            renpy.music.play(config.main_menu_music, channel="music",
                             loop=True, fadeout=0.3, fadein=0.5)

transform jz_chapter_title_reveal:
    alpha 0.0
    linear 0.35 alpha 1.0
    pause 1.5
    linear 0.35 alpha 0.0

screen jz_chapter_title(chapter_number, chapter_name):
    modal True
    zorder 200
    add Solid("#000000")

    vbox:
        at jz_chapter_title_reveal
        align (0.5, 0.46)
        spacing 26
        text chapter_number:
            xalign 0.5
            size 26
            kerning 6
            color "#C8BEAE"
        text chapter_name:
            xalign 0.5
            size 60
            kerning 10
            color "#F4ECDE"

    timer 2.25 action Return()
    key "dismiss" action Return()

label jz_chapter_gate(chapter_key):
    if _in_replay and jz_replay_stop_key == chapter_key:
        $ renpy.end_replay()

    $ _jz_chapter_entry = next(e for e in jz_chapter_entries if e[0] == chapter_key)
    $ _jz_chapter_previous_quick_menu = quick_menu
    $ quick_menu = False
    window hide
    scene black
    with Dissolve(0.2)
    call screen jz_chapter_title(_jz_chapter_entry[1], _jz_chapter_entry[2])
    $ quick_menu = _jz_chapter_previous_quick_menu
    return

screen jz_chapter_replay():
    tag menu

    use game_menu("章節回看", scroll="viewport"):
        vbox:
            spacing 18
            if jz_replay_unlocked():
                text "選擇要重看的章節":
                    size 26
                    color "#E8DDCC"
                grid 2 5:
                    spacing 14
                    for key, number, name, target, stop_key in jz_chapter_entries:
                        button:
                            xsize 398
                            ysize 82
                            padding (20, 12)
                            background Solid("#25202BD9")
                            hover_background Solid("#574052E8")
                            action Function(jz_start_chapter_replay, key)
                            vbox:
                                spacing 4
                                text number:
                                    size 19
                                    color "#CBBCA7"
                                text name:
                                    size 29
                                    color "#F5F1E8"
                    null
                text "第七章保留兩輪選擇；每章播完會回到這裡。":
                    size 20
                    color "#BFB8B0"
            else:
                text "通關後開放章節回看。":
                    size 26
                    color "#CBBCA7"

screen jz_reading_preferences():
    vbox:
        spacing 12
        label "閱讀設定"
        text "字級大小":
            size 24
            color gui.text_color
        hbox:
            spacing 18
            for caption, value, width in (("小", 26, 122), ("中", 30, 122), ("大（原始字級）", 34, 280)):
                $ chosen = jz_dialogue_size() == value
                button:
                    xsize width
                    padding (2, 2)
                    background Solid("#E6C48C" if chosen else "#554853")
                    hover_background Solid("#F3D9AA")
                    action SetField(persistent, "jz_reading_size", value)
                    selected chosen
                    frame:
                        xfill True
                        padding (16, 11)
                        background Solid("#684551" if chosen else "#231D26")
                        text caption:
                            xalign 0.5
                            size 26
                            bold chosen
                            color ("#FFF2CC" if chosen else "#C9C0C7")

        text "目前原始字級為最大值。":
            size 19
            color gui.idle_small_color

        hbox:
            spacing 18
            text "文字框不透明度":
                size 24
                color gui.text_color
            text ("%d%%" % round(jz_textbox_alpha() * 100)):
                size 24
                color gui.idle_small_color

        bar:
            style "slider"
            xsize 640
            value FieldValue(persistent, "jz_textbox_opacity", min=0.2, max=1.0, step=0.05)

        text "閱讀效果預覽":
            size 24
            color "#DCC59D"
        text "以下為縮小的場景示意；字級與透明度會同步更新。":
            size 19
            color gui.idle_small_color
        frame:
            xsize 780
            padding (2, 2)
            background None
            fixed:
                xysize (776, 219)
                fixed:
                    xysize (1280, 360)
                    at Transform(zoom=0.60625)
                    # 保留場景下半部與原尺寸文字框，再一起等比例縮小。
                    add Transform("bg inn_hall_morning", crop=(0, 360, 1280, 360))
                    window:
                        style "window"
                        background jz_textbox_background()
                        text "清晨的風很淡。":
                            style "say_dialogue"
                            size jz_dialogue_size()

        textbutton "恢復閱讀預設":
            action [SetField(persistent, "jz_reading_size", 34),
                    SetField(persistent, "jz_textbox_opacity", 1.0)]
