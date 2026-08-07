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

# 驚蟄預設立繪：02_素材/驚蟄/v1.0/驚蟄_日常平靜_四分之三側身大腿構圖_無菸斗.png。
image jingzhe neutral = Transform("images/characters/jingzhe_daily_calm_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe smoking = Transform("images/characters/jingzhe_daily_calm_3q_thigh_holding_kiseru_no_smoke.png", zoom=0.44)
image jingzhe pensive = Transform("images/characters/jingzhe_pensive_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe faint_smile = zh_placeholder("驚蟄\n淡笑", "#65758B")
image jingzhe wary = Transform("images/characters/jingzhe_wary_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe stern = Transform("images/characters/jingzhe_stern_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe battle = Transform("images/characters/jingzhe_battle_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe shocked = zh_placeholder("驚蟄\n錯愕", "#6B7280")
image jingzhe grief = Transform("images/characters/jingzhe_grief_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe injured = Transform("images/characters/jingzhe_true_end_injured_3q_full_no_kiseru.png", zoom=0.44)
image jingzhe softened = Transform("images/characters/jingzhe_softened_3q_full_no_kiseru.png", zoom=0.44)

image hanami bright = zh_placeholder("花見\n開朗", "#C65B7C")
image hanami curious = zh_placeholder("花見\n好奇", "#CF6C88")
image hanami concerned = zh_placeholder("花見\n擔心", "#AA526C")
image hanami possessed_sweet = Transform("images/characters/hanami_possessed_sweet_3q_full_unarmed.png", zoom=0.44)
image hanami possessed_blank = Transform("images/characters/hanami_possessed_blank_front_full_unarmed.png", zoom=0.44)
image hanami shaken = zh_placeholder("花見\n驚魂未定", "#8E4A5F")
image hanami determined = zh_placeholder("花見\n堅定", "#B94A68")
image hanami battle = zh_placeholder("花見\n持薙刀戰鬥", "#9A314F")
image hanami injured = Transform("images/characters/hanami_battle_injured_3q_full_unarmed.png", zoom=0.44)
image hanami grief = Transform("images/characters/hanami_grief_3q_full_unarmed.png", zoom=0.44)
image hanami surprised = Transform("images/characters/hanami_revelation_surprised_3q_full_unarmed.png", zoom=0.44)
image hanami angry = zh_placeholder("花見\n生氣", "#8E2F4A")
image hanami tearful = Transform("images/characters/hanami_true_end_tearful_3q_full_unarmed.png", zoom=0.44)

image yumemi gentle = zh_placeholder("夢見\n溫柔", "#8C78D4")
image yumemi shy = zh_placeholder("夢見\n害羞", "#7E6BCB")
image yumemi worried = zh_placeholder("夢見\n擔心", "#6D5BB1")
image yumemi possessed_blank = Transform("images/characters/yumemi_possessed_blank_3q_full_unarmed.png", zoom=0.44)
image yumemi frightened = Transform("images/characters/yumemi_frightened_3q_full_unarmed.png", zoom=0.44)
image yumemi ashamed = zh_placeholder("夢見\n羞愧", "#745FAE")
image yumemi determined = zh_placeholder("夢見\n堅定", "#6854A8")
image yumemi grief = Transform("images/characters/yumemi_grief_3q_full_unarmed.png", zoom=0.44)
image yumemi surprised = zh_placeholder("夢見\n驚訝", "#9988E0")
image yumemi tearful = Transform("images/characters/yumemi_true_end_tearful_3q_full_unarmed.png", zoom=0.44)

image achirichi calm = Transform("images/characters/achirichi_first_meeting_calm_3q_full_no_prop.png", zoom=0.44)
image achirichi serious = zh_placeholder("亞奇里奇\n嚴肅", "#2F7C55")

image tsuchigumo looming = zh_placeholder("土蜘蛛\n逼近", "#1A1A1A")
image tsuchigumo attack = Transform("images/characters/tsuchigumo_frontal_lunge_full_battle_no_prop.png", zoom=0.44)
image jorogumo watchful = Transform("images/characters/jorogumo_watchful_front_full_no_prop.png", zoom=0.44)
image jorogumo searching = Transform("images/characters/jorogumo_searching_3q_full_no_prop.png", zoom=0.44)
image jorogumo attack = Transform("images/characters/jorogumo_attack_3q_full_no_prop.png", zoom=0.44)
image jorogumo enraged = Transform("images/characters/jorogumo_enraged_3q_full_no_prop.png", zoom=0.44)
image shadow_witch cold = zh_placeholder("影之魔女\n冷淡", "#4C2F6B")
image shadow_witch annoyed = Transform("images/characters/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
image shadow_witch concerned = zh_placeholder("影之魔女\n隱晦關切", "#66408A")
