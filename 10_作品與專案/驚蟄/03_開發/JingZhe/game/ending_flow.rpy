# 結局收束：原清晨末句 → 黑底製作名單 → 專屬結局CG與「完」。
# 2026-10-19 生前指定；章名與原劇本文字不在此改寫。

image cg ending_dawn_companions = Transform(
    "images/cg/ending_dawn_companions.png", size=(1280, 720))

define jz_ending_credit_roles = (
    ("故事原案／企劃／監修", "生前"),
    ("角色／世界觀設定・劇本統籌", "生前"),
    ("劇本協作", "澪（AI）・汐（AI）・沐晴（AI）・凜（AI）"),
    ("視覺製作", "澪（AI）・凜（AI）"),
    ("Ren'Py 開發／演出", "沐晴（AI）・凜（AI）"),
    ("短引", "汐（AI）"),
    ("主選單視覺", "凜（AI）"),
    ("音樂／音效製作", "澪（AI）"),
    ("遊戲引擎", "Ren'Py"),
    ("字型", "Noto Sans TC"),
)

transform jz_ending_credit_roll:
    xpos 0.5
    xanchor 0.5
    ypos 740
    linear 36.0 ypos -1130

screen jz_ending_credits():
    modal True
    zorder 200

    add Solid("#000000")

    vbox:
        at jz_ending_credit_roll
        xsize 1000
        spacing 28

        text "驚蟄":
            xalign 0.5
            size 64
            color "#F5F1E8"
            kerning 12
        text "製作名單":
            xalign 0.5
            size 26
            color "#C9B79A"
        null height 28

        for role, names in jz_ending_credit_roles:
            vbox:
                xalign 0.5
                xsize 960
                spacing 8
                text role:
                    xalign 0.5
                    text_align 0.5
                    size 23
                    color "#BFAF98"
                text names:
                    xalign 0.5
                    text_align 0.5
                    size 30
                    color "#F5F1E8"

    timer 37.0 action Return()

    textbutton "略過製作名單":
        xpos 1226
        ypos 680
        xanchor 1.0
        yanchor 1.0
        text_size 20
        text_idle_color "#8F8981"
        text_hover_color "#F5F1E8"
        action Return()

screen jz_ending_complete():
    modal True
    zorder 200

    vbox:
        xpos 72
        ypos 190
        xsize 360
        spacing 24

        text "驚蟄":
            size 82
            kerning 12
            color "#F5E8CC"
            outlines [(2, "#201812", 0, 1)]

        null height 4
        text "— 完 —":
            size 46
            kerning 5
            color "#F5E8CC"
            outlines [(2, "#201812", 0, 1)]

        text "感謝遊玩":
            size 28
            kerning 4
            color "#EADBC1"
            outlines [(2, "#201812", 0, 1)]

    textbutton "返回主選單":
        xpos 72
        ypos 602
        padding (20, 12)
        background Solid("#1B1510B8")
        hover_background Solid("#48372ACA")
        text_size 25
        text_idle_color "#EADBC1"
        text_hover_color "#FFFFFF"
        action Return()

label jz_ending_flow:
    $ _jz_ending_previous_quick_menu = quick_menu
    $ quick_menu = False
    window hide
    stop sound fadeout 0.2

    scene black
    with Fade(1.0, 0.6, 0.0)
    call screen jz_ending_credits

    scene cg ending_dawn_companions
    with Dissolve(1.5)
    call screen jz_ending_complete

    stop music fadeout 1.5
    scene black
    with Dissolve(1.0)
    $ quick_menu = _jz_ending_previous_quick_menu
    return
