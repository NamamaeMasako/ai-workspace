# Approved HTML profile draft, integrated 2026-10-22.
# Reader text and portrait selection are kept in character_profiles.json.

init -10 python:
    import json as jz_profile_json

    with renpy.file("character_profiles.json") as jz_profile_file:
        jz_character_profiles = jz_profile_json.loads(jz_profile_file.read().decode("utf-8"))

    def jz_profiles_unlocked():
        # The current ending records completion after credits, at the ending CG.
        # Legacy clears predate jz_ending_flow and only recorded end_game.
        return bool(getattr(persistent, "jz_completed", False) or
            (renpy.seen_label("end_game") and not renpy.seen_label("jz_ending_flow")))

    def jz_profile_select(index):
        return [SetScreenVariable("person_index", index),
            SetScreenVariable("gallery_state", {"index": 0}),
            SetScreenVariable("profile_tab", "intro"),
            SetScreenVariable("reading_adjustment", ui.adjustment())]

    def jz_profile_image(art, width, height):
        return Transform(Image(art["src"]), xysize=(width, height), fit="contain")

    def jz_profile_head(head, width):
        source = Image(head["src"])
        if "crop" in head:
            source = im.Crop(head["src"], tuple(head["crop"]))
        return Transform(source, xysize=(width, width), fit="contain")


screen jz_profile_art(art, width, height, head_width=82):
    fixed:
        xysize (width, height)
        add jz_profile_image(art, width, height) align (0.5, 0.5)
        for head_number, head in enumerate(art.get("variants", [])):
            add jz_profile_head(head, head_width) xpos 4 ypos (6 + head_number * (head_width + 6))


screen jz_character_profiles():
    tag menu

    default person_index = 0
    default gallery_state = {"index": 0}
    default profile_tab = "intro"
    default reading_adjustment = ui.adjustment()

    add Solid("#0b1210")
    add Solid("#a99c7044") xpos 42 ypos 102 xysize (1196, 1)
    add Solid("#a99c7044") xpos 42 ypos 665 xysize (1196, 1)

    text "人物介紹" xpos 42 ypos 28 size 36 color "#eee4cd"
    text "故事之外，還有一些關於他們的事。" xpos 220 ypos 46 size 17 color "#aaa79b"
    textbutton "返回主選單" xpos 1080 ypos 36 style "jz_profile_button" action ShowMenu("main_menu")
    key "game_menu" action ShowMenu("main_menu")

    if jz_profiles_unlocked():
        $ person = jz_character_profiles[person_index]
        $ gallery = person["portraits"]
        $ details_x = 646 if gallery else 296
        $ details_width = 592 if gallery else 942

        viewport:
            style_prefix "jz_profile"
            xpos 42 ypos 123 xysize (190, 526)
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                spacing 4
                for entry_index, entry in enumerate(jz_character_profiles):
                    if entry_index == 0 or entry["group"] != jz_character_profiles[entry_index - 1]["group"]:
                        null height (16 if entry_index else 0)
                        text entry["group"] size 15 color "#a99c70"
                        null height 5
                    textbutton entry["name"]:
                        style "jz_profile_roster_button"
                        selected person_index == entry_index
                        action jz_profile_select(entry_index)

        if gallery:
            $ art_index = gallery_state["index"] % len(gallery)
            $ art = gallery[art_index]

        fixed:
            xpos 258 ypos 125 xysize (354, 524)
            if gallery:
                use jz_profile_art(art, 354, 424)
                text art["label"] xalign 0.5 ypos 430 xmaximum 346 text_align 0.5 size 16 color "#e5ddc9" substitute False
                textbutton "〈" xpos 20 ypos 474 style "jz_profile_button" action SetDict(gallery_state, "index", (art_index - 1) % len(gallery))
                text "%d / %d" % (art_index + 1, len(gallery)) xalign 0.5 ypos 483 size 16 color "#aaa79b"
                textbutton "〉" xpos 296 ypos 474 style "jz_profile_button" action SetDict(gallery_state, "index", (art_index + 1) % len(gallery))
                textbutton "放大檢視" xpos 116 ypos 513 style "jz_profile_small_button" action Show("jz_profile_zoom", person=person, gallery_state=gallery_state)

        fixed:
            xpos details_x ypos 122 xysize (details_width, 532)
            text person["name"] size 34 color "#eee4cd" substitute False
            text person["identity"] ypos 48 size 17 color "#aaa79b" substitute False
            hbox:
                ypos 87 spacing 12
                textbutton "人物介紹" style "jz_profile_tab_button" selected profile_tab == "intro" action [SetScreenVariable("profile_tab", "intro"), SetScreenVariable("reading_adjustment", ui.adjustment())]
                textbutton "人物逸聞" style "jz_profile_tab_button" selected profile_tab == "notes" action [SetScreenVariable("profile_tab", "notes"), SetScreenVariable("reading_adjustment", ui.adjustment())]
            viewport:
                style_prefix "jz_profile"
                id "jz_profile_reading"
                ypos 143 xysize (details_width, 382)
                yadjustment reading_adjustment
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    xsize (details_width - 30)
                    spacing 18
                    if profile_tab == "intro":
                        for paragraph in person["paragraphs"]:
                            text paragraph style "jz_profile_prose" substitute False
                        null height 3
                        add Solid("#a99c7044") xysize (details_width - 40, 1)
                        text person["relation"] style "jz_profile_prose" color "#bcb6a6" substitute False
                    else:
                        for note in person["notes"]:
                            text note[0] size 22 color "#d6c48f" substitute False
                            text note[1] style "jz_profile_prose" substitute False
                            null height 10
                    null height 10

        text "人物誌" xpos 42 ypos 685 size 16 color "#aaa79b"
        text "左右鍵切換人物　・　Esc 返回" xpos 154 ypos 685 size 15 color "#85877d"
        textbutton "〈" xpos 1065 ypos 675 style "jz_profile_button" action jz_profile_select((person_index - 1) % len(jz_character_profiles))
        text "%02d / %02d" % (person_index + 1, len(jz_character_profiles)) xpos 1110 ypos 685 size 16 color "#d5cba8"
        textbutton "〉" xpos 1210 ypos 675 style "jz_profile_button" action jz_profile_select((person_index + 1) % len(jz_character_profiles))
        key "K_LEFT" action jz_profile_select((person_index - 1) % len(jz_character_profiles))
        key "K_RIGHT" action jz_profile_select((person_index + 1) % len(jz_character_profiles))
    else:
        text "通關後開放" align (0.5, 0.48) size 30 color "#eee4cd"
        text "看過一次完整結局後，即可閱讀人物介紹與逸聞。" align (0.5, 0.57) size 20 color "#aaa79b"


screen jz_profile_zoom(person, gallery_state):
    modal True
    zorder 200
    add Solid("#080d0bfa")
    if jz_profiles_unlocked() and person["portraits"]:
        $ gallery = person["portraits"]
        $ art_index = gallery_state["index"] % len(gallery)
        $ art = gallery[art_index]
        text person["name"] xpos 46 ypos 22 size 26 color "#eee4cd" substitute False
        textbutton "關閉 ×" xpos 1135 ypos 18 style "jz_profile_button" action Hide("jz_profile_zoom")
        fixed:
            xpos 420 ypos 67 xysize (440, 565)
            use jz_profile_art(art, 440, 565, head_width=107)
        text art["label"] xalign 0.5 ypos 647 size 18 color "#eee4cd" substitute False
        text "%d / %d" % (art_index + 1, len(gallery)) xalign 0.5 ypos 682 size 16 color "#aaa79b"
        textbutton "〈" xpos 340 ypos 659 style "jz_profile_button" action SetDict(gallery_state, "index", (art_index - 1) % len(gallery))
        textbutton "〉" xpos 900 ypos 659 style "jz_profile_button" action SetDict(gallery_state, "index", (art_index + 1) % len(gallery))
        key "K_LEFT" action SetDict(gallery_state, "index", (art_index - 1) % len(gallery))
        key "K_RIGHT" action SetDict(gallery_state, "index", (art_index + 1) % len(gallery))
    key "game_menu" action Hide("jz_profile_zoom")


style jz_profile_button is button:
    background None
    hover_background Solid("#d9c58d16")
    padding (10, 5)

style jz_profile_button_text is text:
    font "NotoSansTC-VF.ttf"
    size 20
    color "#c3bdad"
    hover_color "#fff0c8"

style jz_profile_small_button is jz_profile_button
style jz_profile_small_button_text is jz_profile_button_text:
    size 15

style jz_profile_roster_button is jz_profile_button:
    xsize 174
    ysize 36
    padding (12, 5)
    selected_background Frame(Solid("#b7a576"), 1, 1)

style jz_profile_roster_button_text is jz_profile_button_text:
    size 19
    selected_color "#101710"
    selected_hover_color "#101710"

style jz_profile_tab_button is jz_profile_button:
    padding (18, 8)
    selected_background Solid("#b7a57628")

style jz_profile_tab_button_text is jz_profile_button_text:
    size 19
    selected_color "#f2dfab"

style jz_profile_prose is text:
    font "NotoSansTC-VF.ttf"
    size 20
    color "#dbd7ca"
    line_spacing 13

style jz_profile_viewport is viewport
style jz_profile_vscrollbar is vscrollbar:
    xsize 6
    top_bar Solid("#263128")
    bottom_bar Solid("#263128")
    thumb Solid("#a99c70")
    unscrollable "hide"

