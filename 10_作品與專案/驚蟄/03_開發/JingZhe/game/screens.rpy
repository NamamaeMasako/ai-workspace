################################################################################
## Screens
################################################################################

init offset = -1

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties('input', accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties('hyperlink', accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties('interface')

style button:
    properties gui.button_properties('button')

style button_text is gui_text:
    properties gui.text_properties('button')
    yalign 0.5

style label_text is gui_text:
    properties gui.text_properties('label', accent=True)

style prompt_text is gui_text:
    properties gui.text_properties('prompt')

style bar:
    ysize gui.bar_size
    left_bar Frame('gui/bar/left.png', gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame('gui/bar/right.png', gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame('gui/bar/top.png', gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame('gui/bar/bottom.png', gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame('gui/scrollbar/horizontal_[prefix_]bar.png', gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame('gui/scrollbar/horizontal_[prefix_]thumb.png', gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame('gui/scrollbar/vertical_[prefix_]bar.png', gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame('gui/scrollbar/vertical_[prefix_]thumb.png', gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame('gui/slider/horizontal_[prefix_]bar.png', gui.slider_borders, tile=gui.slider_tile)
    thumb 'gui/slider/horizontal_[prefix_]thumb.png'

style vslider:
    xsize gui.slider_size
    base_bar Frame('gui/slider/vertical_[prefix_]bar.png', gui.vslider_borders, tile=gui.slider_tile)
    thumb 'gui/slider/vertical_[prefix_]thumb.png'

style frame:
    padding gui.frame_borders.padding
    background Frame('gui/frame.png', gui.frame_borders, tile=gui.frame_tile)

screen say(who, what):
    window:
        id 'window'

        if who is not None:
            window:
                style 'namebox'
                text who id 'who'

        text what id 'what'

    if not renpy.variant('small'):
        add SideImage() xalign 0.0 yalign 1.0

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue
style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image('gui/textbox.png', xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height
    background Frame('gui/namebox.png', gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties('name', accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties('dialogue')
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False

screen choice(items):
    style_prefix 'choice'
    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text
style choice_vbox:
    xalign 0.5
    ypos 300
    yanchor 0.5
    spacing gui.choice_spacing
style choice_button is default:
    properties gui.button_properties('choice_button')
style choice_button_text is default:
    properties gui.text_properties('choice_button')

screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            style_prefix 'quick'
            xalign 0.5
            yalign 1.0
            textbutton _('返回') action Rollback()
            textbutton _('歷史') action ShowMenu('history')
            textbutton _('快轉') action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _('自動') action Preference('auto-forward', 'toggle')
            textbutton _('存檔') action ShowMenu('save')
            textbutton _('快存') action QuickSave()
            textbutton _('快讀') action QuickLoad()
            textbutton _('設定') action ShowMenu('preferences')

init python:
    config.overlay_screens.append('quick_menu')

default quick_menu = True

style quick_button is default
style quick_button_text is button_text
style quick_button:
    properties gui.button_properties('quick_button')
style quick_button_text:
    properties gui.text_properties('quick_button')

screen navigation():
    vbox:
        style_prefix 'navigation'
        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing
        if main_menu:
            textbutton _('開始遊戲') action Start()
        else:
            textbutton _('歷史紀錄') action ShowMenu('history')
            textbutton _('存檔') action ShowMenu('save')
        textbutton _('讀檔') action ShowMenu('load')
        textbutton _('設定') action ShowMenu('preferences')
        if _in_replay:
            textbutton _('結束回放') action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _('主選單') action MainMenu()
        textbutton _('關於') action ShowMenu('about')
        if renpy.variant('pc') or (renpy.variant('web') and not renpy.variant('mobile')):
            textbutton _('說明') action ShowMenu('help')
        if renpy.variant('pc'):
            if main_menu:
                textbutton _('離開遊戲') action Show('confirm', message='確定要離開遊戲嗎？', yes_action=Quit(confirm=False), no_action=Hide('confirm'))
            else:
                textbutton _('離開遊戲') action Quit(confirm=True)

style navigation_button is gui_button
style navigation_button_text is gui_button_text
style navigation_button:
    size_group 'navigation'
    properties gui.button_properties('navigation_button')
style navigation_button_text:
    properties gui.text_properties('navigation_button')

screen main_menu():
    tag menu
    style_prefix 'main_menu'
    add gui.main_menu_background
    frame:
        pass
    use navigation
    text '[config.name!t]' style 'main_menu_title'

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_frame:
    xsize 320
    yfill True
    background 'gui/overlay/main_menu.png'
style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20
style main_menu_text:
    properties gui.text_properties('main_menu', accent=True)
style main_menu_title:
    properties gui.text_properties('title')
    xpos 60
    ypos 50

screen game_menu(title, scroll=None):
    style_prefix 'game_menu'
    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background
    frame:
        style 'game_menu_outer_frame'
        hbox:
            frame:
                style 'game_menu_navigation_frame'
            frame:
                style 'game_menu_content_frame'
                if scroll == 'viewport':
                    viewport:
                        scrollbars 'vertical'
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        vbox:
                            transclude
                elif scroll == 'vpgrid':
                    vpgrid:
                        cols 1
                        yinitial 1.0
                        scrollbars 'vertical'
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        transclude
                else:
                    transclude
    use navigation
    textbutton _('返回'):
        style 'return_button'
        action Return()
    label title
    if main_menu:
        key 'game_menu' action ShowMenu('main_menu')

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar
style game_menu_label is gui_label
style game_menu_label_text is gui_label_text
style return_button is navigation_button
style return_button_text is navigation_button_text
style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120
    background 'gui/overlay/game_menu.png'
style game_menu_navigation_frame:
    xsize 320
    yfill True
style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10
style game_menu_viewport:
    xsize 880
style game_menu_vscrollbar:
    unscrollable gui.unscrollable
style game_menu_side:
    spacing 10
style game_menu_label:
    xpos 50
    ysize 120
style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5
style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30

screen about():
    tag menu
    use game_menu(_('關於'), scroll='viewport'):
        style_prefix 'about'
        vbox:
            label '[config.name!t]'
            text _('版本 [config.version!t]\n')
            if gui.about:
                text '[gui.about!t]\n'
            text _('使用 Ren\'Py [renpy.version_only] 製作。')

screen save():
    tag menu
    use file_slots(_('存檔'))

screen load():
    tag menu
    use file_slots(_('讀檔'))

screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_('第 {} 頁'), auto=_('自動存檔'), quick=_('快速存檔'))
    use game_menu(title):
        fixed:
            order_reverse True
            button:
                style 'page_label'
                key_events True
                xalign 0.5
                action page_name_value.Toggle()
                input:
                    style 'page_label_text'
                    value page_name_value
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix 'slot'
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        text FileTime(slot, format=_('{#file_time}%Y-%m-%d %H:%M'), empty=_('空白存檔位')):
                            style 'slot_time_text'
                        text FileSaveName(slot):
                            style 'slot_name_text'
                        key 'save_delete' action FileDelete(slot)
            hbox:
                style_prefix 'page'
                xalign 0.5
                yalign 1.0
                spacing gui.page_spacing
                textbutton _('<') action FilePagePrevious()
                key 'save_page_prev' action FilePagePrevious()
                if config.has_autosave:
                    textbutton _('{#auto_page}A') action FilePage('auto')
                if config.has_quicksave:
                    textbutton _('{#quick_page}Q') action FilePage('quick')
                for page in range(1, 10):
                    textbutton '[page]' action FilePage(page)
                textbutton _('>') action FilePageNext()
                key 'save_page_next' action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text
style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

screen preferences():
    tag menu
    use game_menu(_('設定'), scroll='viewport'):
        vbox:
            hbox:
                box_wrap True
                if renpy.variant('pc') or renpy.variant('web'):
                    vbox:
                        spacing 12
                        vbox:
                            style_prefix 'radio'
                            label _('顯示模式')
                            textbutton _('視窗模式') action Preference('display', 'window')
                            textbutton _('全螢幕') action Preference('display', 'fullscreen')
                vbox:
                    style_prefix 'check'
                    label _('快轉')
                    textbutton _('未讀文本') action Preference('skip', 'toggle')
                    textbutton _('選項後繼續') action Preference('after choices', 'toggle')
                    textbutton _('轉場效果') action InvertSelected(Preference('transitions', 'toggle'))
            null height (4 * gui.pref_spacing)
            hbox:
                style_prefix 'slider'
                box_wrap True
                vbox:
                    label _('文字顯示速度')
                    bar value Preference('text speed')
                    label _('自動播放速度')
                    bar value Preference('auto-forward time')

screen history():
    tag menu
    predict False
    use game_menu(_('歷史紀錄'), scroll=('vpgrid' if gui.history_height else 'viewport')):
        style_prefix 'history'
        for h in _history_list:
            window:
                has fixed:
                    yfit True
                if h.who:
                    label h.who:
                        style 'history_name'
                        substitute False
                        if 'color' in h.who_args:
                            text_color h.who_args['color']
                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False
        if not _history_list:
            label _('目前沒有歷史紀錄。')

define gui.history_allow_tags = { 'alt', 'noalt', 'rt', 'rb', 'art' }

style history_window is empty
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text
style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ('subtitle' if gui.history_text_xalign else 'tex')

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

screen help():
    tag menu
    use game_menu(_('操作說明'), scroll='viewport'):
        vbox:
            spacing 15
            text _('滑鼠左鍵 / Enter：前進對話')
            text _('右鍵 / Esc：開啟選單')
            text _('Ctrl / Tab：快轉')
            text _('Page Up：回看')
            text _('H：隱藏介面')

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    style_prefix 'confirm'
    add 'gui/overlay/confirm.png'

    if message in ["Are you sure you want to quit?", "確定要離開遊戲嗎？"]:
        $ message = "確定要離開遊戲嗎？"
    elif message in ["Are you sure you want to return to the main menu?", "確定要回到主選單嗎？"]:
        $ message = "確定要回到主選單嗎？"
    elif message in ["Are you sure you want to end the replay?", "確定要結束回放嗎？"]:
        $ message = "確定要結束回放嗎？"
    elif message in ["Are you sure you want to begin skipping?", "確定要開始快轉嗎？"]:
        $ message = "確定要開始快轉嗎？"
    elif message in ["Are you sure you want to delete this save?", "確定要刪除這個存檔嗎？"]:
        $ message = "確定要刪除這個存檔嗎？"
    elif message in ["Are you sure you want to overwrite your save?", "確定要覆蓋這個存檔嗎？"]:
        $ message = "確定要覆蓋這個存檔嗎？"
    elif message in ["Loading will lose unsaved progress.\nAre you sure you want to do this?", "讀檔會失去尚未儲存的進度。\n確定要繼續嗎？"]:
        $ message = "讀檔會失去尚未儲存的進度。\n確定要繼續嗎？"
    elif message in ["The device for the mouse handle does not exist. Please reconnect a mouse, some keyboards, or a touchpad.", "找不到滑鼠裝置。請重新連接滑鼠、部分鍵盤，或觸控板。"]:
        $ message = "找不到滑鼠裝置。請重新連接滑鼠、部分鍵盤，或觸控板。"

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 30
            label _(message):
                style 'confirm_prompt'
                xalign 0.5
            hbox:
                xalign 0.5
                spacing 100
                textbutton _('是') action yes_action
                textbutton _('否') action no_action
    key 'game_menu' action no_action

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text
style confirm_frame:
    background Frame(['gui/confirm_frame.png', 'gui/frame.png'], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5
style confirm_prompt_text:
    textalign 0.5
    layout 'subtitle'
style confirm_button:
    properties gui.button_properties('confirm_button')
style confirm_button_text:
    properties gui.text_properties('confirm_button')

screen notify(message):
    zorder 100
    style_prefix 'notify'
    frame at notify_appear:
        text '[message!tq]'
    timer 3.25 action Hide('notify')

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

screen nvl(dialogue, items=None):
    window:
        style 'nvl_window'
        has vbox:
            spacing gui.nvl_spacing
        if gui.nvl_height:
            vpgrid:
                cols 1
                yinitial 1.0
                use nvl_dialogue(dialogue)
        else:
            use nvl_dialogue(dialogue)
        for i in items:
            textbutton i.caption:
                action i.action
                style 'nvl_button'
    add SideImage() xalign 0.0 yalign 1.0

screen nvl_dialogue(dialogue):
    for d in dialogue:
        window:
            id d.window_id
            fixed:
                yfit gui.nvl_height is None
                if d.who is not None:
                    text d.who id d.who_id
                text d.what id d.what_id

define config.nvl_list_length = 6
