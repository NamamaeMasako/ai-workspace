# 驚蟄 / placeholders.rpy

init python:
    def zh_placeholder(label, color, width=760, height=920, text_color="#FFFFFF"):
        return Composite(
            (width, height),
            (0, 0), Solid(color, xysize=(width, height)),
            (40, 48), Text(label, size=54, color=text_color, outlines=[(2, "#000000", 0, 0)])
        )

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

image jingzhe neutral = zh_placeholder("驚蟄\n預設", "#3B4252")
image jingzhe neutral_smoke = zh_placeholder("驚蟄\n抽菸", "#4C566A")
image hanami smile = zh_placeholder("花見\n微笑", "#C65B7C")
image hanami sad = zh_placeholder("花見\n難過", "#9E3F5D")
image hanami determined = zh_placeholder("花見\n堅定", "#B94A68")
image hanami surprised = zh_placeholder("花見\n驚訝", "#D47A96")
image hanami angry = zh_placeholder("花見\n生氣", "#8E2F4A")
image yumemi shy = zh_placeholder("夢見\n害羞", "#7E6BCB")
image yumemi sad = zh_placeholder("夢見\n難過", "#5B4A9A")
image yumemi surprised = zh_placeholder("夢見\n驚訝", "#9988E0")
image achirichi calm = zh_placeholder("亞奇里奇\n平靜", "#3FA16F")
image tsuchigumo shadow = zh_placeholder("土蜘蛛\n陰影", "#1A1A1A")
image jorogumo shadow = zh_placeholder("絡新婦\n陰影", "#2A2028")
image shadow_witch neutral = zh_placeholder("影之魔女\n預設", "#4C2F6B")
