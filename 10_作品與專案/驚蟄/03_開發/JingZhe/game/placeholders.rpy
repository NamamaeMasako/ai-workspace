# 驚蟄 / placeholders.rpy

init python:
    def zh_placeholder(label, color, width=760, height=920, text_color="#FFFFFF"):
        return Composite(
            (width, height),
            (0, 0), Solid(color, xysize=(width, height)),
            (40, 48), Text(label, size=54, color=text_color, outlines=[(2, "#000000", 0, 0)])
        )

transform zh_far_left:
    xalign 0.10
    yalign 1.0

transform zh_left:
    xalign 0.27
    yalign 1.0

transform zh_center:
    xalign 0.50
    yalign 1.0

transform zh_right:
    xalign 0.73
    yalign 1.0

transform zh_far_right:
    xalign 0.90
    yalign 1.0

define flash = Fade(0.05, 0.0, 0.25, color="#FFFFFF")

image bg road_twilight = Solid("#546A7B")
image bg inn_exterior = Solid("#7B5E57")
image bg inn_morning = Solid("#A88F6A")
image bg inn_dining = Solid("#8D6E63")
image bg inn_backyard = Solid("#5D7A5A")
image bg inn_hall_evening = Solid("#6A4C5A")
image bg inn_room_night = Solid("#2F3B52")
image bg inn_room_late = Solid("#1D2433")
image bg tavern_night = Solid("#5A4638")
image bg inn_exterior_twilight = Solid("#465067")
image bg forest_path = Solid("#2F4A3C")
image bg forest_path_night = Solid("#1D2A24")
image bg forest_clearing_night = Solid("#243128")
image bg inn_corridor_night = Solid("#3E314A")
image bg inn_kitchen = Solid("#7A6852")
image bg inn_corridor_day = Solid("#8B7B66")
image bg inn_room_evening = Solid("#4D445C")
image bg inn_gate_night = Solid("#394152")
image bg inn_exterior_night = Solid("#313B4A")
image bg inn_hall_night = Solid("#30273A")

# 尚無專屬圖的角色狀態暫時映射到同角色最接近的正式透明立繪；
# 專屬圖完成後直接替換對應路徑，不再退回角色色塊 placeholder。
# 驚蟄預設立繪：02_素材/驚蟄/v1.0/驚蟄_日常平靜_四分之三側身大腿構圖_無菸斗.png。
image jingzhe neutral = Transform("images/characters/thigh/jingzhe_daily_calm_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe smoking = Transform("images/characters/thigh/jingzhe_daily_calm_3q_thigh_holding_kiseru_no_smoke.png", zoom=0.44)
image jingzhe pensive = Transform("images/characters/thigh/jingzhe_pensive_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe faint_smile = Transform("images/characters/thigh/jingzhe_faint_smile_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe wary = Transform("images/characters/thigh/jingzhe_wary_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe stern = Transform("images/characters/thigh/jingzhe_stern_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe battle = Transform("images/characters/thigh/jingzhe_battle_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe shocked = Transform("images/characters/thigh/jingzhe_shocked_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe grief = Transform("images/characters/thigh/jingzhe_grief_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe injured = Transform("images/characters/thigh/jingzhe_true_end_injured_3q_full_no_kiseru.png", zoom=0.44)
image jingzhe softened = Transform("images/characters/thigh/jingzhe_softened_3q_full_no_kiseru.png", zoom=0.44)

image hanami bright = Transform("images/characters/thigh/hanami_bright_3q_full_unarmed.png", zoom=0.44)
image hanami curious = Transform("images/characters/thigh/hanami_curious_3q_full_unarmed.png", zoom=0.44)
image hanami concerned = Transform("images/characters/thigh/hanami_concerned_3q_full_unarmed.png", zoom=0.44)
image hanami possessed_sweet = Transform("images/characters/thigh/hanami_possessed_sweet_3q_full_unarmed.png", zoom=0.44)
image hanami possessed_blank = Transform("images/characters/thigh/hanami_possessed_blank_front_full_unarmed.png", zoom=0.44)
image hanami shaken = Transform("images/characters/thigh/hanami_shaken_3q_full_unarmed.png", zoom=0.44)
image hanami determined = Transform("images/characters/thigh/hanami_determined_3q_full_unarmed.png", zoom=0.44)
image hanami battle = Transform("images/characters/thigh/hanami_battle_injured_3q_full_unarmed.png", zoom=0.44)
image hanami injured = Transform("images/characters/thigh/hanami_injured_3q_full_unarmed.png", zoom=0.44)
image hanami grief = Transform("images/characters/thigh/hanami_grief_3q_full_unarmed.png", zoom=0.44)
image hanami surprised = Transform("images/characters/thigh/hanami_revelation_surprised_3q_full_unarmed.png", zoom=0.44)
image hanami angry = Transform("images/characters/thigh/hanami_angry_3q_full_unarmed.png", zoom=0.44)
image hanami tearful = Transform("images/characters/thigh/hanami_true_end_tearful_3q_full_unarmed.png", zoom=0.44)

image yumemi gentle = Transform("images/characters/thigh/yumemi_gentle_3q_full_unarmed.png", zoom=0.44)
image yumemi shy = Transform("images/characters/thigh/yumemi_shy_3q_full_unarmed.png", zoom=0.44)
image yumemi worried = Transform("images/characters/thigh/yumemi_worried_3q_full_unarmed.png", zoom=0.44)
image yumemi possessed_blank = Transform("images/characters/thigh/yumemi_possessed_blank_3q_full_unarmed.png", zoom=0.44)
image yumemi frightened = Transform("images/characters/thigh/yumemi_frightened_3q_full_unarmed.png", zoom=0.44)
image yumemi ashamed = Transform("images/characters/thigh/yumemi_ashamed_3q_full_unarmed.png", zoom=0.44)
image yumemi determined = Transform("images/characters/thigh/yumemi_determined_3q_full_unarmed.png", zoom=0.44)
image yumemi grief = Transform("images/characters/thigh/yumemi_grief_3q_full_unarmed.png", zoom=0.44)
image yumemi surprised = Transform("images/characters/thigh/yumemi_surprised_3q_full_unarmed.png", zoom=0.44)
image yumemi tearful = Transform("images/characters/thigh/yumemi_true_end_tearful_3q_full_unarmed.png", zoom=0.44)

image achirichi calm = Transform("images/characters/thigh/achirichi_first_meeting_calm_3q_full_no_prop.png", zoom=0.44)
image achirichi serious = Transform("images/characters/thigh/achirichi_serious_3q_full_no_prop.png", zoom=0.44)

image tsuchigumo looming = Transform("images/characters/thigh/tsuchigumo_looming_full_no_prop.png", zoom=0.44)
image tsuchigumo attack = Transform("images/characters/thigh/tsuchigumo_frontal_lunge_full_battle_no_prop.png", zoom=0.44)
image jorogumo watchful = Transform("images/characters/thigh/jorogumo_watchful_front_full_no_prop.png", zoom=0.44)
image jorogumo searching = Transform("images/characters/thigh/jorogumo_searching_3q_full_no_prop.png", zoom=0.44)
image jorogumo attack = Transform("images/characters/thigh/jorogumo_attack_3q_full_no_prop.png", zoom=0.44)
image jorogumo enraged = Transform("images/characters/thigh/jorogumo_enraged_3q_full_no_prop.png", zoom=0.44)
image shadow_witch cold = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
image shadow_witch annoyed = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
image shadow_witch concerned = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
