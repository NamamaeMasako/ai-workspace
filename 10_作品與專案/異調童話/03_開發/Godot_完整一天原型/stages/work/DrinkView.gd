extends Node2D

const Model = preload("res://stages/work/DrinkModel.gd")
const RESET := Rect2(1050, 22, 200, 42)
const DISCARD := Rect2(385, 690, 270, 58)
const ACTION := Rect2(900, 690, 330, 58)
const MATERIAL_BUTTONS := [Rect2(385, 557, 260, 78), Rect2(675, 557, 260, 78), Rect2(965, 557, 265, 78)]
var game := Model.new()
var font: SystemFont

func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei UI", "Microsoft JhengHei", "Noto Sans CJK TC"])
	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		var key: int = event.physical_keycode
		if key == 0:
			key = event.keycode
		if key == 0:
			key = event.unicode
		# Unicode-injected keys may carry a placeholder physical key code.
		if event.unicode >= 32 and event.unicode <= 126:
			key = event.unicode
		elif event.unicode == 13:
			key = KEY_ENTER
		elif event.unicode == 8:
			key = KEY_BACKSPACE
		if key == KEY_R or key == 114:
			game.reset()
		elif key in [KEY_ENTER, KEY_KP_ENTER, KEY_SPACE]:
			main_action()
		elif key == KEY_BACKSPACE:
			game.discard()
		elif key >= KEY_1 and key <= KEY_3:
			game.add(Model.INGREDIENTS[key - KEY_1])
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		click(event.position)
	queue_redraw()

func click(point: Vector2) -> void:
	if RESET.has_point(point):
		game.reset()
	elif ACTION.has_point(point):
		main_action()
	elif DISCARD.has_point(point):
		game.discard()
	elif game.phase == Model.Phase.MIXING:
		for index in range(MATERIAL_BUTTONS.size()):
			if MATERIAL_BUTTONS[index].has_point(point):
				game.add(Model.INGREDIENTS[index])
	queue_redraw()

func main_action() -> void:
	match game.phase:
		Model.Phase.READY: game.start()
		Model.Phase.MIXING: game.serve()
		Model.Phase.ORDER_RESULT: game.next_order()
		Model.Phase.DONE: game.reset()

func text_at(pos: Vector2, text: String, size: int = 18, color: Color = Color("#f3e5d2"), width: float = -1) -> void:
	draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, width, size, color)

func panel(rect: Rect2, color: Color) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.set_corner_radius_all(12)
	draw_style_box(style, rect)

func button(rect: Rect2, title: String, enabled: bool = true) -> void:
	panel(rect, Color("#6b806b") if enabled else Color("#454a43"))
	text_at(rect.position + Vector2(21, 36), title, 19, Color("#fff4db") if enabled else Color("#a3a99a"))

func _draw() -> void:
	if font == null:
		return
	draw_rect(Rect2(0, 0, 1280, 800), Color("#202c30"))
	draw_rect(Rect2(0, 88, 1280, 712), Color("#322c2a"))
	text_at(Vector2(30, 43), "薇斯帕的酒館  /  諾亞的調飲工作", 26)
	text_at(Vector2(31, 75), "無酒精飲料 · 選對材料即可 · 不計份量與時間", 15, Color("#b7c8ba"))
	button(RESET, "R  重新開始")
	draw_recipe_book()
	panel(Rect2(366, 115, 885, 420), Color("#41483f"))
	if game.phase == Model.Phase.READY:
		draw_welcome()
	elif game.phase == Model.Phase.DONE:
		draw_results()
	else:
		draw_cup()
		draw_order()
	draw_materials()
	text_at(Vector2(386, 670), game.message, 17, Color("#edc897"), 840)
	button(DISCARD, "倒掉重做  /  Backspace", game.phase == Model.Phase.MIXING)
	var action_text := "開始工作"
	match game.phase:
		Model.Phase.MIXING: action_text = "送出飲料  /  Enter"
		Model.Phase.ORDER_RESULT: action_text = "下一位客人" if game.order_index < Model.ORDERS.size() - 1 else "完成工作，查看結算"
		Model.Phase.DONE: action_text = "再做一晚"
	button(ACTION, action_text)
	text_at(Vector2(386, 781), "1／2／3 加材料 · 材料順序不限 · 倒掉不扣分 · 所有配方與結算值皆為測試用", 14, Color("#bdc3b5"))

func draw_recipe_book() -> void:
	panel(Rect2(25, 115, 320, 633), Color("#dbc9a6"))
	text_at(Vector2(51, 157), "吧檯配方本", 24, Color("#423f32"))
	text_at(Vector2(51, 186), "配方可隨時參考", 14, Color("#68644d"))
	var names := ["紅茶", "奶茶", "珍珠紅茶", "珍珠奶茶"]
	for index in range(names.size()):
		var y := 232 + 100 * index
		text_at(Vector2(51, y), names[index], 22, Color("#4c4534"))
		var ingredient_names: Array[String] = []
		for ingredient in Model.RECIPES[names[index]]:
			ingredient_names.append(Model.LABELS[ingredient])
		text_at(Vector2(51, y + 33), "＋".join(ingredient_names), 17, Color("#6c5b43"))
		draw_line(Vector2(49, y + 55), Vector2(317, y + 55), Color("#bca780"), 1)
	text_at(Vector2(51, 663), "每晚先做四張固定訂單", 17, Color("#514c3b"))
	text_at(Vector2(51, 697), "送錯會退回，可以再做。", 16, Color("#68644d"))
	text_at(Vector2(51, 724), "不用搶時間，慢慢試。", 16, Color("#68644d"))

func draw_welcome() -> void:
	text_at(Vector2(407, 174), "今晚，先從無酒精飲料開始。", 28)
	text_at(Vector2(408, 231), "紅茶、牛奶、珍珠，選擇訂單需要的材料。", 21)
	text_at(Vector2(408, 276), "左側配方本可以隨時看；按材料後，杯中會顯示內容。", 19)
	text_at(Vector2(408, 323), "做錯可以倒掉重來，再把做好的飲料送給客人。", 19)
	text_at(Vector2(408, 394), "本版沒有倒入份量、計時或材料庫存限制。", 18, Color("#c5d2bb"))
	text_at(Vector2(408, 437), "完成四張訂單後，查看模擬報酬與薇斯帕密切度變化。", 18, Color("#c5d2bb"))
	text_at(Vector2(408, 493), "按右下「開始工作」，或按 Enter。", 19)

func draw_cup() -> void:
	text_at(Vector2(402, 155), "調製區", 20, Color("#c6d7bc"))
	draw_line(Vector2(390, 487), Vector2(800, 487), Color("#9b876b"), 4)
	var cup_outline := PackedVector2Array([Vector2(492, 238), Vector2(716, 238), Vector2(690, 481), Vector2(518, 481)])
	draw_colored_polygon(cup_outline, Color(0.9, 0.95, 0.9, 0.09))
	if game.cup.has("tea") or game.cup.has("milk"):
		var liquid := Color("#9e652f")
		if game.cup.has("milk"):
			liquid = Color("#d4b68b") if game.cup.has("tea") else Color("#ebe5d4")
		draw_colored_polygon(PackedVector2Array([Vector2(506, 290), Vector2(702, 290), Vector2(682, 470), Vector2(526, 470)]), liquid)
		draw_line(Vector2(506, 290), Vector2(702, 290), liquid.lightened(0.2), 4)
	if game.cup.has("pearls"):
		for offset in [Vector2(-59, 0), Vector2(-29, 3), Vector2(1, -1), Vector2(32, 3), Vector2(61, 0), Vector2(-43, -26), Vector2(-11, -27), Vector2(23, -25), Vector2(48, -25)]:
			draw_circle(Vector2(604, 452) + offset, 12, Color("#332b27"))
	draw_polyline(PackedVector2Array([Vector2(492, 238), Vector2(518, 481), Vector2(690, 481), Vector2(716, 238)]), Color("#cbd8c8"), 3, true)
	draw_line(Vector2(492, 238), Vector2(716, 238), Color("#e1e7d5"), 3)
	var labels: Array[String] = []
	for ingredient in game.cup:
		labels.append(Model.LABELS[ingredient])
	text_at(Vector2(405, 518), "杯中：" + ("、".join(labels) if not labels.is_empty() else "空杯"), 18)

func draw_order() -> void:
	panel(Rect2(829, 140, 397, 367), Color("#e9dec5"))
	text_at(Vector2(853, 180), "訂單 %d / 4" % (game.order_index + 1), 19, Color("#797251"))
	text_at(Vector2(853, 236), game.current_order(), 34, Color("#453e32"))
	text_at(Vector2(853, 280), "「一杯%s，謝謝。」" % game.current_order(), 19, Color("#756548"))
	draw_line(Vector2(853, 310), Vector2(1200, 310), Color("#c9b999"), 1)
	if game.phase == Model.Phase.ORDER_RESULT:
		text_at(Vector2(853, 361), "✓  客人收到正確飲料", 23, Color("#5a7651"))
		text_at(Vector2(853, 406), "按右下按鈕接下一張訂單。", 17, Color("#68604a"))
	else:
		text_at(Vector2(853, 355), "請按照左側配方選擇材料。", 18, Color("#68604a"))
		text_at(Vector2(853, 395), "不需要控制份量或加入順序。", 17, Color("#68604a"))
	text_at(Vector2(853, 464), "完成 %d　送錯 %d　倒掉 %d" % [game.correct, game.wrong, game.discarded], 17, Color("#6b654c"))

func draw_materials() -> void:
	for index in range(Model.INGREDIENTS.size()):
		var ingredient: String = Model.INGREDIENTS[index]
		var selected := game.cup.has(ingredient)
		var rect: Rect2 = MATERIAL_BUTTONS[index]
		var enabled := game.phase == Model.Phase.MIXING
		panel(rect, Color("#748461") if selected else (Color("#596754") if enabled else Color("#414b42")))
		text_at(rect.position + Vector2(19, 33), "%d  %s" % [index + 1, Model.LABELS[ingredient]], 23)
		text_at(rect.position + Vector2(20, 60), "已加入" if selected else "點擊加入杯中", 15, Color("#d3dac7") if enabled else Color("#909c8a"))

func draw_results() -> void:
	text_at(Vector2(407, 170), "今晚的工作結算", 28)
	text_at(Vector2(408, 223), "完成飲料：%d / 4　　送錯：%d 次" % [game.correct, game.wrong], 22)
	text_at(Vector2(408, 272), "倒掉重做：%d 次（不扣分）" % game.discarded, 19)
	text_at(Vector2(408, 337), "模擬報酬：%d" % game.simulated_pay(), 28, Color("#eed0a1"))
	var change: int = game.simulated_relationship_change()
	text_at(Vector2(408, 384), "薇斯帕密切度：%+d（測試值）" % change, 23, Color("#c0ddaa"))
	text_at(Vector2(408, 438), "結算僅顯示於此，尚未寫入每日流程或正式關係系統。", 17, Color("#bdcdb4"))
	text_at(Vector2(408, 478), "可以再做一晚，或稍後調整配方與工作規則。", 18)
