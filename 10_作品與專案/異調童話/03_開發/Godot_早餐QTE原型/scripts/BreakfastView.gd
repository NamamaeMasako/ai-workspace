extends Node2D

const Model = preload("res://scripts/BreakfastModel.gd")
const RESET := Rect2(1060, 22, 190, 40)
const NEXT := Rect2(825, 541, 390, 48)
const ARROW_BUTTONS := [Rect2(724, 571, 105, 44), Rect2(848, 571, 105, 44), Rect2(972, 571, 105, 44), Rect2(1096, 571, 105, 44)]
const DIRECTIONS := ["U", "D", "L", "R"]
const EXTRA_ITEMS := ["茄子", "蘋果", "茶葉"]
var game := Model.new()
var font: SystemFont
var animation_time := 0.0

func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei UI", "Microsoft JhengHei", "Noto Sans CJK TC"])
	queue_redraw()

func _process(delta: float) -> void:
	animation_time += delta
	game.tick(delta)
	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		var key: int = event.physical_keycode
		if key == 0:
			key = event.keycode
		if key == 0:
			key = event.unicode
		if key == KEY_R or key == 114:
			game.reset()
		elif key in [KEY_SPACE, KEY_ENTER]:
			continue_flow()
		elif key == KEY_UP:
			game.enter_direction("U")
		elif key == KEY_DOWN:
			game.enter_direction("D")
		elif key == KEY_LEFT:
			game.enter_direction("L")
		elif key == KEY_RIGHT:
			game.enter_direction("R")
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		click(event.position)

func continue_flow() -> void:
	if game.phase == Model.Phase.READY:
		game.start()
	elif game.phase == Model.Phase.DIALOGUE:
		game.next_line()

func click(point: Vector2) -> void:
	if RESET.has_point(point):
		game.reset()
	elif game.phase == Model.Phase.QTE:
		for index in range(ARROW_BUTTONS.size()):
			if ARROW_BUTTONS[index].has_point(point):
				game.enter_direction(DIRECTIONS[index])
				return
	elif game.phase == Model.Phase.READY or game.phase == Model.Phase.DIALOGUE:
		if NEXT.has_point(point):
			continue_flow()
	elif game.phase == Model.Phase.SHOPPING:
		for index in range(EXTRA_ITEMS.size()):
			if Rect2(720, 345 + 59 * index, 495, 48).has_point(point):
				game.toggle_extra(EXTRA_ITEMS[index])
		if NEXT.has_point(point):
			game.confirm_shopping()

func label_at(pos: Vector2, text: String, size: int = 18, color: Color = Color("#f0e6d7"), width: float = -1) -> void:
	draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, width, size, color)

func panel(rect: Rect2, color: Color) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.set_corner_radius_all(12)
	draw_style_box(style, rect)

func button(rect: Rect2, text: String) -> void:
	panel(rect, Color("#596e62"))
	label_at(rect.position + Vector2(18, 29), text, 18)

func arrows(code: String) -> String:
	return code.replace("U", "↑").replace("D", "↓").replace("L", "←").replace("R", "→")

func _draw() -> void:
	if font == null:
		return
	draw_rect(Rect2(0, 0, 1280, 800), Color("#252d2c"))
	label_at(Vector2(29, 44), "異調童話  /  早餐時光", 26)
	label_at(Vector2(30, 78), "洛芙的視角 · 兩輪話題 · 劇情與美術皆為測試用", 15, Color("#bec8bc"))
	button(RESET, "R  重新開始")
	draw_breakfast_scene()
	panel(Rect2(685, 100, 568, 521), Color("#333f3b"))
	match game.phase:
		Model.Phase.READY:
			label_at(Vector2(720, 153), "坐下來，聽她說說話。", 25)
			label_at(Vector2(720, 209), "每輪會同時出現三則話題。", 19)
			label_at(Vector2(720, 245), "10 秒內用方向鍵輸入其中一組。", 19)
			label_at(Vector2(720, 299), "成功：接著聊天，對話不限時。", 18, Color("#c5e0bf"))
			label_at(Vector2(720, 338), "錯誤或逾時：本輪失敗，不可重試。", 18)
			label_at(Vector2(720, 389), "兩輪後，看看今天要請諾亞買什麼。", 18)
			label_at(Vector2(720, 459), "按下開始後，才會啟動第一輪倒數。", 16, Color("#c3c5b3"))
			button(NEXT, "開始早餐  /  空白鍵")
		Model.Phase.QTE, Model.Phase.ROUND_RESULT:
			draw_topics()
		Model.Phase.DIALOGUE:
			draw_dialogue()
		Model.Phase.SHOPPING:
			draw_shopping()
		Model.Phase.DONE:
			draw_summary()
	draw_footer()

func draw_breakfast_scene() -> void:
	panel(Rect2(24, 100, 640, 521), Color("#aca28e"))
	# Warm room, window and dining table; all artwork is procedural placeholder.
	draw_rect(Rect2(50, 127, 176, 236), Color("#6e8179"))
	draw_rect(Rect2(61, 139, 154, 210), Color("#c3cfbc"))
	draw_line(Vector2(137, 140), Vector2(137, 350), Color("#7a7767"), 7)
	draw_line(Vector2(61, 242), Vector2(215, 242), Color("#7a7767"), 7)
	draw_rect(Rect2(548, 159, 80, 170), Color("#8c8c76"))
	draw_rect(Rect2(555, 166, 66, 152), Color("#c1b494"))
	var bob := sin(animation_time * 1.5) * 2.0
	var head := Vector2(386, 272 + bob)
	# Long red-gold hair, neutral clothing, seated facing the player.
	draw_colored_polygon(PackedVector2Array([head + Vector2(-76, -28), head + Vector2(-73, 217), head + Vector2(83, 217), head + Vector2(74, -31)]), Color("#a7633c"))
	draw_circle(head + Vector2(0, -5), 78, Color("#bd7c45"))
	draw_colored_polygon(PackedVector2Array([Vector2(330, 358 + bob), Vector2(445, 358 + bob), Vector2(479, 505), Vector2(293, 505)]), Color("#e8d9bb"))
	draw_rect(Rect2(370, 320 + bob, 31, 41), Color("#e3b89b"))
	draw_circle(head, 61, Color("#f1cbb0"))
	draw_colored_polygon(PackedVector2Array([head + Vector2(-64, -12), head + Vector2(-56, -58), head + Vector2(23, -70), head + Vector2(65, -31), head + Vector2(66, 14), head + Vector2(18, -28), head + Vector2(-12, -4), head + Vector2(-6, -32)]), Color("#cf8c4d"))
	draw_line(head + Vector2(-72, -10), head + Vector2(-64, 183), Color("#dfaa67"), 12)
	draw_line(head + Vector2(70, -11), head + Vector2(73, 184), Color("#dfaa67"), 12)
	var blinking := fmod(animation_time, 4.5) > 4.3
	for eye_x in [-23, 23]:
		if blinking:
			draw_line(head + Vector2(eye_x - 6, 5), head + Vector2(eye_x + 6, 5), Color("#71533d"), 3)
		else:
			draw_circle(head + Vector2(eye_x, 5), 5, Color("#796641"))
	var talking: bool = game.phase == Model.Phase.QTE or (game.phase == Model.Phase.DIALOGUE and game.current_line()[0] == "諾亞")
	if talking:
		draw_circle(head + Vector2(0, 31), 3 + absf(sin(animation_time * 5)) * 3, Color("#a96153"))
	else:
		draw_line(head + Vector2(-7, 31), head + Vector2(7, 31), Color("#a96153"), 2)
	# Her hand slowly raises a spoon when she is not speaking.
	var hand_y := 434.0 if talking else 427.0 + sin(animation_time * 2) * 9
	draw_line(Vector2(444, 382), Vector2(485, hand_y), Color("#e8d9bb"), 26)
	draw_circle(Vector2(482, hand_y), 12, Color("#f1cbb0"))
	draw_line(Vector2(478, hand_y), Vector2(458, hand_y - 27), Color("#b9c3bb"), 4)
	draw_circle(Vector2(455, hand_y - 31), 6, Color("#cbd2c8"))
	draw_colored_polygon(PackedVector2Array([Vector2(24, 472), Vector2(664, 472), Vector2(664, 621), Vector2(24, 621)]), Color("#84654e"))
	for offset in [0, 36, 82]:
		draw_line(Vector2(25, 510 + offset), Vector2(662, 510 + offset), Color(0.3, 0.2, 0.15, 0.16), 2)
	draw_circle(Vector2(387, 504), 46, Color("#ded6bc"))
	draw_circle(Vector2(387, 504), 34, Color("#c7af82"))
	draw_rect(Rect2(370, 489, 35, 21), Color("#bb8048"))
	draw_circle(Vector2(527, 510), 23, Color("#e5dabe"))
	draw_circle(Vector2(527, 510), 16, Color("#907350"))
	draw_circle(Vector2(205, 582), 45, Color("#d9d8c7"))
	draw_rect(Rect2(181, 564, 49, 25), Color("#d7b56b"))
	draw_circle(Vector2(77, 575), 20, Color("#bdc4b5"))
	label_at(Vector2(52, 406), "諾亞", 18, Color("#424e43"))
	label_at(Vector2(51, 437), "早餐桌的另一側", 14, Color("#535b4e"))

func draw_topics() -> void:
	var active := game.phase == Model.Phase.QTE
	label_at(Vector2(718, 137), "第 %d / 2 輪" % game.round_number, 20)
	label_at(Vector2(1075, 137), "%04.1f 秒" % game.seconds_left if active else "本輪結束", 19, Color("#eed3a4"))
	panel(Rect2(720, 148, 495, 5), Color("#26302d"))
	if active:
		draw_rect(Rect2(720, 148, 495 * game.seconds_left / Model.ROUND_SECONDS, 5), Color("#c9bd83"))
	for index in range(game.topics.size()):
		var topic: Dictionary = game.topics[index]
		var y := 172.0 + index * 111.0
		var matches: bool = topic.code.begins_with(game.input_buffer)
		panel(Rect2(716, y, 503, 96), Color("#4e6055") if matches and active else Color("#3f4941"))
		label_at(Vector2(735, y + 31), topic.opening, 19, Color("#f1e7d3") if matches else Color("#929d91"))
		var code: String = topic.code
		for letter in range(code.length()):
			var accepted := matches and letter < game.input_buffer.length()
			panel(Rect2(738 + letter * 55, y + 45, 43, 35), Color("#9eb78f") if accepted else Color("#2f3b34"))
			label_at(Vector2(751 + letter * 55, y + 70), arrows(code[letter]), 25, Color("#203329") if accepted else Color("#e1d7bd"))
	label_at(Vector2(724, 538), "目前輸入： " + (arrows(game.input_buffer) if not game.input_buffer.is_empty() else "—"), 22, Color("#e8c397") if not active else Color("#c6e2be"))
	if active:
		for index in range(ARROW_BUTTONS.size()):
			button(ARROW_BUTTONS[index], "    " + arrows(DIRECTIONS[index]))
	else:
		label_at(Vector2(724, 587), "即將進入下一輪……" if game.round_number < 2 else "早餐結束，準備採購清單……", 17, Color("#c4cbb8"))

func draw_dialogue() -> void:
	label_at(Vector2(720, 143), "接住了話題  /  聊天不限時", 22, Color("#c4e5bd"))
	var lines: Array = game.topics[game.selected].lines
	var first := maxi(0, game.dialogue_index - 1)
	for index in range(first, game.dialogue_index + 1):
		var y := 185 + (index - first) * 160
		var current := index == game.dialogue_index
		panel(Rect2(717, y, 502, 137), Color("#58695a") if current else Color("#414e44"))
		label_at(Vector2(739, y + 32), lines[index][0], 19, Color("#eed0a1"))
		var body: String = lines[index][1]
		# The placeholder lines are short; split long ones at a safe character boundary.
		label_at(Vector2(739, y + 70), body.substr(0, 23), 19)
		if body.length() > 23:
			label_at(Vector2(739, y + 103), body.substr(23), 19)
	button(NEXT, "繼續  /  空白鍵")

func draw_shopping() -> void:
	label_at(Vector2(720, 145), "早餐結束  /  採購安排", 24)
	panel(Rect2(718, 165, 503, 67), Color("#58664e"))
	label_at(Vector2(735, 193), "今天諾亞想吃茄子。" if game.eggplant_known else "沒有記下特別想吃的東西。", 20)
	label_at(Vector2(735, 217), "從剛才成功聊過的內容留下的提示", 13, Color("#c3cbb5"))
	label_at(Vector2(720, 270), "固定採購：米、雞蛋、日常蔬菜", 18)
	label_at(Vector2(720, 300), "以上為佔位清單；本版不計價格或庫存。", 14, Color("#bdc7b7"))
	label_at(Vector2(720, 331), "額外要買：", 18)
	for index in range(EXTRA_ITEMS.size()):
		var item: String = EXTRA_ITEMS[index]
		var chosen := game.extras.has(item)
		panel(Rect2(720, 345 + 59 * index, 495, 48), Color("#6b7c59") if chosen else Color("#48564b"))
		label_at(Vector2(740, 376 + 59 * index), ("☑  " if chosen else "☐  ") + item, 20)
	button(NEXT, "確認採購清單")

func draw_summary() -> void:
	label_at(Vector2(720, 148), "採購清單已記下", 25, Color("#cfdfbb"))
	label_at(Vector2(720, 202), "額外購買：" + ("、".join(game.extras) if not game.extras.is_empty() else "無"), 19)
	label_at(Vector2(720, 260), "喜好提示：" + ("今天諾亞想吃茄子" if game.eggplant_known else "未取得"), 18)
	if game.favorite_remembered():
		label_at(Vector2(720, 308), "洛芙記住了，也安排買茄子。", 20, Color("#d1e4b3"))
		label_at(Vector2(720, 343), "後續便當與密切度回饋預留於此。", 17)
	else:
		label_at(Vector2(720, 308), "今天的採購安排完成。", 20)
	label_at(Vector2(720, 408), "通訊器線索：" + ("已記下" if game.communicator_known else "未取得"), 18)
	if game.communicator_known:
		label_at(Vector2(720, 442), "仍須之後取得物品，本版不套用加成。", 16)
	label_at(Vector2(720, 552), "原型到此結束。按 R 可再測另一種選擇。", 16, Color("#d3ccb9"))

func draw_footer() -> void:
	panel(Rect2(24, 640, 1229, 138), Color("#313d37"))
	var message := "準備好了，再開始。測試兩輪接話與採購提示是否順暢。"
	if game.phase == Model.Phase.QTE:
		message = "用方向鍵輸入其中一組，或點右側方向按鈕。每輪只能接一個話題。"
	elif game.phase == Model.Phase.DIALOGUE:
		message = "現在不計時。按空白鍵或「繼續」閱讀對話。"
	elif game.phase == Model.Phase.ROUND_RESULT:
		message = game.outcome
	elif game.phase == Model.Phase.SHOPPING:
		message = "固定採購會照常安排；點選額外食材，再確認清單。"
	elif game.phase == Model.Phase.DONE:
		message = "此版只驗證早餐與清單，沒有接續下午、實際採購或晚間打工。"
	label_at(Vector2(48, 678), message, 19)
	label_at(Vector2(48, 717), "輸入進度會顯示在話題與下方。按錯或逾時，直接失去本輪機會。", 16, Color("#bdc9b9"))
	label_at(Vector2(48, 750), "美術、台詞、固定品項皆為佔位 · 沒有每日總倒數 · R 隨時重置", 14, Color("#a8b4a3"))
