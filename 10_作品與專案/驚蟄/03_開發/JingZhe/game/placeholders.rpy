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

# 三人戰鬥／怪物同框使用較寬的舞台。縮小後再分散站位，避免中央角色
# 把兩側角色整張壓住；這些 transform 是演出排版，不是劇情上的遠近變化。
transform zh_group_left:
    xalign 0.04
    yalign 1.0
    zoom 0.74

transform zh_group_center:
    xalign 0.50
    yalign 1.0
    zoom 0.78

transform zh_group_right:
    xalign 0.96
    yalign 1.0
    zoom 0.74

# 四人同框再退一級，保留每張臉與主要動作的閱讀空間。
transform zh_quad_far_left:
    xalign 0.00
    yalign 1.0
    zoom 0.62

transform zh_quad_left:
    xalign 0.32
    yalign 1.0
    zoom 0.66

transform zh_quad_right:
    xalign 0.68
    yalign 1.0
    zoom 0.66

transform zh_quad_far_right:
    xalign 1.00
    yalign 1.0
    zoom 0.62

# 巨型敵人與一般角色同框時，不再把全員一起縮成遠景。敵人可由畫面邊界
# 自然遮掉外側肢體；驚蟄與花見則集中在另一側，保留正常的人物尺度。
transform zh_battle_monster_left:
    xalign 0.00
    yalign 1.0

transform zh_battle_party_mid:
    xalign 0.68
    yalign 1.0

transform zh_battle_party_right:
    xalign 1.00
    yalign 1.0

# 雙怪同框時集中在左側，讓右側的驚蟄維持正常比例與清楚輪廓。
transform zh_monster_cluster_mid:
    xalign 0.34
    yalign 1.0

# 影之魔女獨立留在左側；其餘三人以正常大小靠攏在右側。
transform zh_shadow_left:
    xalign 0.00
    yalign 1.0

transform zh_party_cluster_left:
    xalign 0.64
    yalign 1.0

transform zh_party_cluster_center:
    xalign 0.82
    yalign 1.0

transform zh_party_cluster_right:
    xalign 1.00
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

# 土蜘蛛衍生圖保留完整輪廓；放大後只由遊戲畫面邊界自然遮擋。looming
# 原圖的可見主體較扁，因此需要較大的顯示倍率；attack 則下移，優先遮腳而非身體。
image tsuchigumo looming = Transform("images/characters/thigh/tsuchigumo_looming_full_no_prop.png", zoom=0.72)
image tsuchigumo attack = Transform("images/characters/thigh/tsuchigumo_frontal_lunge_full_battle_no_prop.png", zoom=0.56, yoffset=140)
# 絡新婦以人形頭身對齊一般角色；完整蜘蛛輪廓仍保留在素材內，畫面只允許
# 大腿以下自然超出底邊，避免為了塞進全身而把人形軀幹縮成遠景。
image jorogumo watchful = Transform("images/characters/thigh/jorogumo_watchful_front_full_no_prop.png", zoom=0.60, yoffset=190)
image jorogumo searching = Transform("images/characters/thigh/jorogumo_searching_3q_full_no_prop.png", zoom=0.60, yoffset=190)
image jorogumo attack = Transform("images/characters/thigh/jorogumo_attack_3q_full_no_prop.png", zoom=0.60, yoffset=190)
image jorogumo enraged = Transform("images/characters/thigh/jorogumo_enraged_3q_full_no_prop.png", zoom=0.60, yoffset=190)
image shadow_witch cold = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
image shadow_witch annoyed = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
image shadow_witch concerned = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_card.png", zoom=0.44)
