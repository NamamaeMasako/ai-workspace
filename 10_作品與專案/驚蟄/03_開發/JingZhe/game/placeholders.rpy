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

# 第一章早餐三人同框時，jingzhe softened 要與前一幀的 pensive 維持同一頭部尺度與頭頂高度。
# 只在該幕放大並對齊；下半身自然延伸到對話框後方與畫面外。
transform zh_breakfast_center:
    xalign 0.50
    yalign 1.0
    zoom 1.30
    xoffset 16
    yoffset 195

# 真結局三人同框時，驚蟄 softened 原圖的人物佔比比兩側角色大。
# 只在卡片說明與結尾靠攏兩幕縮小並上移，讓三人的頭部尺度與高度一致。
transform zh_final_center:
    xalign 0.50
    yalign 1.0
    zoom 0.84
    yoffset -105

# 真結局卡片說明改用真正全身素材，但維持一般人物頭身大小。
# 角色從頭頂對齊，讓下半身自然延伸到對話框後方／畫面外，不能把整個人縮成遠景。
transform zh_final_center_full:
    xalign 0.50
    ypos 0.04

transform zh_right:
    xalign 0.73
    yalign 1.0

transform zh_far_right:
    xalign 0.90
    yalign 1.0

# 第一章談到暮春留下的薙刀時，直接顯示持刀輪廓並留出畫面邊界。
transform zh_hanami_naginata_left:
    xalign 0.27
    yalign 1.0
    yoffset -18

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

# 第七章召喚初見：大百足作為後景放大並下沉，讓盤身約一半落入對話框後方；
# 髮切沿用上一版的一般人物顯示尺度；由於她是全身素材、驚蟄是大腿構圖素材，
# 此幕改將髮切整體下移，使頭部落在驚蟄腹部附近。花見向內收並上移，完整保留薙刀輪廓。
transform zh_summon_omukade_back:
    xalign 0.12
    yalign 1.0
    zoom 1.06
    yoffset 125

transform zh_summon_jingzhe:
    xalign 0.39
    yalign 1.0

transform zh_summon_kamikiri:
    xalign 0.59
    yalign 1.0
    zoom 1.05
    yoffset 330

transform zh_summon_hanami:
    xalign 0.94
    yalign 1.0
    yoffset -18

# 第七章土蜘蛛戰：驚蟄與花見先以同倍率退到右側；大百足落在髮切後方，
# 髮切維持前景。輪到花見出手時，再把她恢復一般尺度拉到前景。
transform zh_battle_party_jingzhe_small:
    xalign 0.98
    yalign 1.0
    zoom 0.76

transform zh_battle_party_hanami_small:
    xalign 0.98
    yalign 1.0
    zoom 0.76
    yoffset -18

# 第七章大百足側撞幕：衝撞圖的頭部位於素材下緣，會整顆沉進對話框。
# 改用既有盤身抬首圖作為撞擊後的定格，放大後退到驚蟄與花見後方；
# 髮切與花見並排壓在前景，讓畫面明確分成前排近戰與後排支援。
transform zh_battle_omukade_coiled_back:
    xalign 0.90
    yalign 1.0
    zoom 0.96
    yoffset 60

transform zh_battle_kamikiri_front:
    xalign 0.55
    yalign 1.0
    zoom 0.78
    yoffset 25

transform zh_battle_hanami_foreground:
    xalign 0.74
    yalign 1.0
    zoom 0.76
    yoffset 205

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

# 真結局雙怪同框：絡新婦縮回敵方左側，再向左拉開半個立繪寬度，
# 與右側式神／驚蟄明確分隊。
transform zh_monster_cluster_mid:
    xalign 0.27
    yalign 1.0
    zoom 0.84
    xoffset -125

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

# 第八章強化甦醒：三者共用同一地面線。大百足在後，驚蟄與髮切疊在前，
# 避免大百足直接蓋住驚蟄；髮切仍比驚蟄略小。
transform zh_empowered_omukade_back:
    xalign 0.38
    yalign 1.0
    zoom 0.90
    yoffset 60

transform zh_empowered_jingzhe_front:
    xalign 0.60
    yalign 1.0

transform zh_empowered_kamikiri_front:
    xalign 0.16
    yalign 1.0
    zoom 0.82
    yoffset 32

# 第八章多人戰：反派集中左側，式神與驚蟄集中右側。攻擊幕沿用第七章
# 已確認的水平站位，並保留大百足在後、髮切在前的圖層關係。
transform zh_true_battle_jingzhe_right:
    xalign 0.98
    yalign 1.0
    zoom 0.88

transform zh_true_battle_omukade_back:
    xalign 0.90
    yalign 1.0
    zoom 0.90
    yoffset 145

# 真結局首輪交鋒同框：盤身大百足放大後置於右側隊伍中央後景，
# 讓髮切與驚蟄分別壓在牠的左右前方；盤身下緣自然沉入對話框。
transform zh_true_battle_omukade_coiled_back:
    xalign 0.90
    yalign 1.0
    zoom 1.02
    yoffset 125

transform zh_true_battle_omukade_ready_back:
    xalign 0.80
    yalign 1.0
    zoom 0.96
    yoffset 0

transform zh_true_battle_kamikiri_front:
    xalign 0.55
    yalign 1.0
    zoom 0.94
    yoffset 130

transform zh_true_battle_kamikiri_attack_right:
    xalign 0.55
    yalign 1.0
    zoom 0.94
    yoffset 20

# 土蜘蛛倒下後改成絡新婦與驚蟄的雙人主軸。絡新婦留在敵方左側，
# 驚蟄沿用右側戰鬥站位，避免兩張立繪互相壓住。
transform zh_true_duel_jorogumo_left:
    xalign 0.20
    yalign 1.0
    zoom 0.84

# 驚蟄瀕危時的主觀視覺：只模糊 master layer，對話框維持清楚。
# 劇本逐句提高級數，並在卡片變輕時以 bare camera 清除。
transform zh_vision_blur_1:
    blur 2.0

transform zh_vision_blur_2:
    blur 4.0

transform zh_vision_blur_3:
    blur 7.0

transform zh_vision_blur_4:
    blur 11.0

transform zh_vision_blur_5:
    blur 16.0

define flash = Fade(0.05, 0.0, 0.25, color="#FFFFFF")

image bg road_twilight = Transform("images/backgrounds/road_twilight.png", size=(1280, 720))
image bg inn_exterior = Transform("images/backgrounds/inn_exterior_twilight.png", size=(1280, 720))
image bg inn_exterior_twilight = Transform("images/backgrounds/inn_exterior_twilight.png", size=(1280, 720))
image bg inn_exterior_night = Transform("images/backgrounds/inn_exterior_night.png", size=(1280, 720))
image bg inn_gate_night = Transform("images/backgrounds/inn_exterior_night.png", size=(1280, 720))
image bg inn_hall_morning = Transform("images/backgrounds/inn_hall_morning.png", size=(1280, 720))
image bg inn_hall_evening = Transform("images/backgrounds/inn_hall_evening.png", size=(1280, 720))
image bg inn_hall_night = Transform("images/backgrounds/inn_hall_night.png", size=(1280, 720))
image bg inn_dining = Transform("images/backgrounds/inn_dining_morning.png", size=(1280, 720))
image bg inn_front_yard = Transform("images/backgrounds/inn_front_yard_day.png", size=(1280, 720))
image bg inn_room_morning = Transform("images/backgrounds/inn_room_morning.png", size=(1280, 720))
image bg inn_backyard = Transform("images/backgrounds/inn_backyard_day.png", size=(1280, 720))
image bg inn_corridor_day = Transform("images/backgrounds/inn_corridor_day.png", size=(1280, 720))
image bg inn_corridor_night = Transform("images/backgrounds/inn_corridor_night.png", size=(1280, 720))
image bg inn_room_evening = Transform("images/backgrounds/inn_room_evening.png", size=(1280, 720))
image bg inn_room_night = Transform("images/backgrounds/inn_room_night.png", size=(1280, 720))
image bg inn_room_late = Transform("images/backgrounds/inn_room_late_night.png", size=(1280, 720))
image bg tavern_night = Transform("images/backgrounds/tavern_night.png", size=(1280, 720))
image bg forest_path = Transform("images/backgrounds/forest_path_twilight.png", size=(1280, 720))
image bg forest_path_night = Transform("images/backgrounds/forest_path_night.png", size=(1280, 720))
image bg forest_clearing_night = Transform("images/backgrounds/forest_clearing_night.png", size=(1280, 720))

# 影之魔女贈予驚蟄的魔法郵箱；依實機標示以 3:2 小事件圖置中展示。
image event magic_mailbox = Transform(
    "images/events/magic_mailbox_closed.png",
    xysize=(554, 369),
    xalign=0.5,
    yalign=0.475,
)

# 亞奇里奇放在桌上的全黑卡片；與郵箱共用小事件圖尺寸與位置。
image event black_card = Transform(
    "images/events/black_card_on_table.png",
    crop=(256, 171, 1024, 682),
    xysize=(554, 369),
    xalign=0.5,
    yalign=0.475,
)

# 花見攜帶的包布薙刀刀部；沿用郵箱與卡片的 3:2 小事件圖展示。
image event wrapped_naginata = Transform(
    "images/events/hanami_wrapped_naginata_blade.png",
    xysize=(554, 369),
    xalign=0.5,
    yalign=0.475,
)

# 尚無專屬圖的角色狀態暫時映射到同角色最接近的正式透明立繪；
# 專屬圖完成後直接替換對應路徑，不再退回角色色塊 placeholder。
# 驚蟄預設立繪：02_素材/驚蟄/v1.0/驚蟄_日常平靜_四分之三側身大腿構圖_無菸斗.png。
image jingzhe neutral = Transform("images/characters/thigh/jingzhe_daily_calm_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe smoking = Transform("images/characters/thigh/jingzhe_daily_calm_3q_thigh_holding_kiseru_no_smoke.png", zoom=0.44)
image jingzhe pensive = Transform("images/characters/thigh/jingzhe_pensive_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe faint_smile = Transform("images/characters/thigh/jingzhe_faint_smile_3q_thigh_no_kiseru.png", zoom=0.44, xoffset=-9)
image jingzhe wary = Transform("images/characters/thigh/jingzhe_wary_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe wary_kiseru = Transform("images/characters/thigh/jingzhe_wary_kiseru_3q_thigh_no_smoke.png", zoom=0.44)
image jingzhe stern = Transform("images/characters/thigh/jingzhe_stern_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe stern_kiseru = Transform("images/characters/thigh/jingzhe_stern_kiseru_3q_thigh_no_smoke.png", zoom=0.44)
image jingzhe battle = Transform("images/characters/thigh/jingzhe_battle_3q_thigh_kiseru_smoke.png", zoom=0.44)
image jingzhe pressured = Transform("images/characters/thigh/jingzhe_battle_pressured_3q_thigh_kiseru_smoke.png", zoom=0.44)
image jingzhe shocked = Transform("images/characters/thigh/jingzhe_shocked_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe emotional_impact = Transform("images/characters/thigh/jingzhe_emotional_impact_3q_thigh_kiseru_no_smoke.png", zoom=0.44)
image jingzhe grief = Transform("images/characters/thigh/jingzhe_grief_3q_thigh_no_kiseru.png", zoom=0.44)
image jingzhe injured = Transform("images/characters/thigh/jingzhe_true_end_injured_3q_full_no_kiseru.png", zoom=0.44)
image jingzhe softened = Transform("images/characters/thigh/jingzhe_softened_3q_full_no_kiseru.png", zoom=0.44)
image jingzhe softened_full = Transform("images/characters/jingzhe_softened_3q_full_no_kiseru.png", zoom=0.64)

image hanami bright = Transform("images/characters/thigh/hanami_bright_3q_full_unarmed.png", zoom=0.44)
image hanami curious = Transform("images/characters/thigh/hanami_curious_3q_full_unarmed.png", zoom=0.44)
image hanami concerned = Transform("images/characters/thigh/hanami_concerned_3q_full_unarmed.png", zoom=0.44)
image hanami proud = Transform("images/characters/thigh/hanami_proud_3q_full_unarmed.png", zoom=0.44)
image hanami possessed_sweet = Transform("images/characters/thigh/hanami_possessed_sweet_3q_full_unarmed.png", zoom=0.44)
image hanami possessed_blank = Transform("images/characters/thigh/hanami_possessed_blank_front_full_unarmed.png", zoom=0.44)
image hanami shaken = Transform("images/characters/thigh/hanami_shaken_3q_full_unarmed.png", zoom=0.44)
image hanami determined = Transform("images/characters/thigh/hanami_determined_3q_full_unarmed.png", zoom=0.44)
image hanami battle = Transform("images/characters/thigh/hanami_battle_ready_3q_full_naginata.png", zoom=0.44)
# 第七章土蜘蛛戰前景專用：改用未裁切的全身來源，維持與大腿構圖版相同的
# 頭部尺度，再把腿部自然沉到對話框與視窗外，避免露出衍生圖的硬裁底緣。
image hanami battle_full = Transform("images/characters/hanami_battle_ready_3q_full_naginata.png", zoom=0.60)
image hanami injured = Transform("images/characters/thigh/hanami_battle_injured_3q_full_unarmed.png", zoom=0.44)
image hanami deceased = Transform("images/characters/thigh/hanami_deceased_3q_full_unarmed.png", zoom=0.44)
image hanami grief = Transform("images/characters/thigh/hanami_grief_3q_full_unarmed.png", zoom=0.44)
image hanami surprised = Transform("images/characters/thigh/hanami_revelation_surprised_3q_full_unarmed.png", zoom=0.44)
image hanami angry = Transform("images/characters/thigh/hanami_angry_3q_full_unarmed.png", zoom=0.44)
image hanami tearful = Transform("images/characters/thigh/hanami_true_end_tearful_3q_full_unarmed.png", zoom=0.44)

image yumemi gentle = Transform("images/characters/thigh/yumemi_gentle_3q_full_unarmed.png", zoom=0.44)
image yumemi shy = Transform("images/characters/thigh/yumemi_shy_3q_full_unarmed.png", zoom=0.44)
image yumemi worried = Transform("images/characters/thigh/yumemi_worried_3q_full_unarmed.png", zoom=0.44)
image yumemi possessed_blank = Transform("images/characters/thigh/yumemi_possessed_blank_3q_full_unarmed.png", zoom=0.44)
image yumemi frightened = Transform("images/characters/thigh/yumemi_frightened_3q_full_unarmed.png", zoom=0.44)
image yumemi fearful_confused = Transform("images/characters/thigh/yumemi_fearful_confused_3q_full_unarmed.png", zoom=0.44)
image yumemi ashamed = Transform("images/characters/thigh/yumemi_ashamed_3q_full_unarmed.png", zoom=0.44)
image yumemi determined = Transform("images/characters/thigh/yumemi_determined_3q_full_unarmed.png", zoom=0.44)
image yumemi grief = Transform("images/characters/thigh/yumemi_grief_3q_full_unarmed.png", zoom=0.44)
image yumemi surprised = Transform("images/characters/thigh/yumemi_surprised_3q_full_unarmed.png", zoom=0.44)
image yumemi mild_surprise = Transform("images/characters/thigh/yumemi_mild_surprise_3q_full_unarmed.png", zoom=0.44)
image yumemi tearful = Transform("images/characters/thigh/yumemi_true_end_tearful_3q_full_unarmed.png", zoom=0.44)

image achirichi calm = Transform("images/characters/thigh/achirichi_first_meeting_calm_3q_full_no_prop.png", zoom=0.44)
image achirichi serious = Transform("images/characters/thigh/achirichi_serious_3q_full_no_prop.png", zoom=0.44)

image kamikiri ready = Transform("images/characters/thigh/kamikiri_ready_3q_full_right_sword_left_forearm_blade.png", zoom=0.44)
image kamikiri attack = Transform("images/characters/thigh/kamikiri_attack_forward_full_right_sword_left_forearm_blade.png", zoom=0.44)
image kamikiri empowered = Transform("images/characters/thigh/kamikiri_empowered_ready_3q_full_right_sword_left_forearm_blade.png", zoom=0.44)
image kamikiri empowered_attack = Transform("images/characters/thigh/kamikiri_empowered_attack_forward_full_right_sword_left_forearm_blade.png", zoom=0.44)

# 大百足以完整盤身／衝撞輪廓顯示；頭部已在母圖中置於對話框安全區。
image omukade ready = Transform("images/characters/thigh/omukade_ready_coiled_raised_full_no_prop.png", zoom=0.58)
image omukade charge = Transform("images/characters/thigh/omukade_charge_forward_full_no_prop.png", zoom=0.58)
image omukade empowered = Transform("images/characters/thigh/omukade_empowered_coiled_raised_full_no_prop.png", zoom=0.58)
image omukade empowered_charge = Transform("images/characters/thigh/omukade_empowered_charge_forward_full_no_prop.png", zoom=0.58)

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
image shadow_witch cold = Transform("images/characters/thigh/shadow_witch_cold_3q_full_holding_staff.png", zoom=0.44)
image shadow_witch annoyed = Transform("images/characters/thigh/shadow_witch_annoyed_3q_full_holding_staff.png", zoom=0.44)
image shadow_witch concerned = Transform("images/characters/thigh/shadow_witch_concerned_3q_full_holding_staff.png", zoom=0.44)

image cg chapter7_shikigami_summon = Transform("images/cg/chapter7_shikigami_summon.png", size=(1280, 720))
image cg chapter7_tsuchigumo_assault = Transform("images/cg/chapter7_tsuchigumo_assault.png", size=(1280, 720))
image cg chapter7_jorogumo_ambush_hanami = Transform("images/cg/chapter7_jorogumo_ambush_hanami.png", size=(1280, 720))
image cg chapter8_jingzhe_solo_battle = Transform("images/cg/chapter8_jingzhe_solo_battle.png", size=(1280, 720))
image cg chapter8_jingzhe_stops_hanami_card = Transform("images/cg/chapter8_jingzhe_stops_hanami_card.png", size=(1280, 720))
