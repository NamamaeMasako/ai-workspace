# Shared UI activation sounds; the audio channel uses the sfx volume mixer.
define gui.ui_confirm_sound = "audio/sfx/ui/ui_confirm.ogg"
define gui.ui_back_sound = "audio/sfx/ui/ui_back.ogg"

init 10 python:
    # Choice and quick buttons explicitly inherit default in screens.rpy,
    # so they need the same activation sound as the other UI button families.
    for _zh_button_style in (
        "button", "gui_button", "gui_medium_button", "navigation_button",
        "quick_button", "choice_button", "slot_button", "page_button",
        "radio_button", "check_button", "confirm_button", "nvl_button",
    ):
        style[_zh_button_style].activate_sound = gui.ui_confirm_sound
        style[_zh_button_style].hover_sound = None
    style.return_button.activate_sound = gui.ui_back_sound
