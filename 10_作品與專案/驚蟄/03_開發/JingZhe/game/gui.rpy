################################################################################
## Initialization
################################################################################

init offset = -2

init python:
    gui.init(1280, 720)

################################################################################
## GUI Configuration Variables
################################################################################

define gui.accent_color = '#C65B7C'
define gui.idle_color = '#DDD6CE'
define gui.idle_small_color = '#BFB8B0'
define gui.hover_color = '#FFFFFF'
define gui.selected_color = '#FFD7E2'
define gui.insensitive_color = '#8B86907F'
define gui.muted_color = '#5A5362'
define gui.hover_muted_color = '#7D7486'
define gui.text_color = '#F5F1E8'
define gui.interface_text_color = '#F5F1E8'

define gui.text_font = 'NotoSansTC-VF.ttf'
define gui.name_text_font = 'NotoSansTC-VF.ttf'
define gui.interface_text_font = 'NotoSansTC-VF.ttf'

define gui.text_size = 34
define gui.name_text_size = 40
define gui.interface_text_size = 28
define gui.label_text_size = 32
define gui.notify_text_size = 22
define gui.title_text_size = 56

define gui.main_menu_background = 'gui/main_menu.png'
define gui.game_menu_background = 'gui/game_menu.png'

define gui.textbox_height = 220
define gui.textbox_yalign = 1.0

define gui.name_xpos = 160
define gui.name_ypos = 20
define gui.name_xalign = 0.0
define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(24, 12, 24, 12)
define gui.namebox_tile = False

define gui.dialogue_xpos = 170
define gui.dialogue_ypos = 78
define gui.dialogue_width = 940
define gui.dialogue_text_xalign = 0.0

define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(6, 6, 6, 6)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.0

define gui.radio_button_borders = Borders(27, 6, 6, 6)
define gui.check_button_borders = Borders(27, 6, 6, 6)
define gui.confirm_button_text_xalign = 0.5
define gui.page_button_borders = Borders(12, 6, 12, 6)
define gui.quick_button_borders = Borders(12, 6, 12, 0)
define gui.quick_button_text_size = 18
define gui.quick_button_text_idle_color = gui.idle_small_color
define gui.quick_button_text_selected_color = gui.accent_color

define gui.choice_button_width = 900
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(120, 12, 120, 12)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = 32
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = '#F0E9E2'
define gui.choice_button_text_hover_color = '#FFFFFF'

define gui.slot_button_width = 276
define gui.slot_button_height = 206
define gui.slot_button_borders = Borders(10, 10, 10, 10)
define gui.slot_button_text_size = 14
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color

define config.thumbnail_width = 256
define config.thumbnail_height = 144

define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

define gui.navigation_xpos = 60
define gui.skip_ypos = 15
define gui.notify_ypos = 55
define gui.choice_spacing = 16
define gui.navigation_spacing = 8
define gui.pref_spacing = 12
define gui.pref_button_spacing = 6
define gui.page_spacing = 4
define gui.slot_spacing = 10
define gui.main_menu_text_xalign = 0.0

define gui.frame_borders = Borders(20, 12, 20, 12)
define gui.confirm_frame_borders = Borders(40, 40, 40, 40)
define gui.skip_frame_borders = Borders(16, 8, 50, 8)
define gui.notify_frame_borders = Borders(16, 8, 40, 8)
define gui.frame_tile = False

define gui.bar_size = 36
define gui.scrollbar_size = 18
define gui.slider_size = 36
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False
define gui.bar_borders = Borders(4, 4, 4, 4)
define gui.scrollbar_borders = Borders(4, 4, 4, 4)
define gui.slider_borders = Borders(18, 18, 18, 18)
define gui.vbar_borders = Borders(4, 4, 4, 4)
define gui.vscrollbar_borders = Borders(4, 4, 4, 4)
define gui.vslider_borders = Borders(18, 18, 18, 18)
define gui.unscrollable = 'hide'

define config.history_length = 250
define gui.history_height = 170
define gui.history_name_xpos = 120
define gui.history_name_ypos = 0
define gui.history_name_width = 180
define gui.history_name_xalign = 1.0
define gui.history_text_xpos = 320
define gui.history_text_ypos = 6
define gui.history_text_width = 720
define gui.history_text_xalign = 0.0

define gui.nvl_borders = Borders(0, 15, 0, 30)
define gui.nvl_height = 160
define gui.nvl_spacing = 14
define gui.nvl_name_xpos = 360
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 180
define gui.nvl_name_xalign = 1.0
define gui.nvl_text_xpos = 390
define gui.nvl_text_ypos = 12
define gui.nvl_text_width = 760
define gui.nvl_text_xalign = 0.0
define gui.nvl_thought_xpos = 180
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 920
define gui.nvl_thought_xalign = 0.0
define gui.nvl_button_xpos = 390
define gui.nvl_button_xalign = 0.0

define gui.language = 'unicode'

init python:
    @gui.variant
    def touch():
        gui.quick_button_borders = Borders(40, 14, 40, 0)

    @gui.variant
    def small():
        gui.text_size = 30
        gui.name_text_size = 34
        gui.notify_text_size = 24
        gui.interface_text_size = 32
        gui.button_text_size = 30
        gui.label_text_size = 34
        gui.textbox_height = 240
        gui.name_xpos = 70
        gui.dialogue_xpos = 80
        gui.dialogue_width = 1120
        gui.choice_button_width = 1240
        gui.navigation_spacing = 18
        gui.pref_button_spacing = 10
        gui.history_height = 210
        gui.history_text_width = 690
        gui.file_slot_cols = 2
        gui.file_slot_rows = 2
        gui.nvl_height = 190
        gui.nvl_name_width = 260
        gui.nvl_name_xpos = 280
        gui.nvl_text_width = 930
        gui.nvl_text_xpos = 300
        gui.nvl_text_ypos = 8
        gui.nvl_thought_width = 1220
        gui.nvl_thought_xpos = 20
        gui.nvl_button_width = 1240
        gui.nvl_button_xpos = 20
        gui.quick_button_text_size = 20
