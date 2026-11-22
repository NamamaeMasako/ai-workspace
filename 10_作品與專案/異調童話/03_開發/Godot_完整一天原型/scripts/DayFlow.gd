extends Node2D

const Session = preload("res://scripts/DaySession.gd")
const BreakfastView = preload("res://stages/breakfast/BreakfastView.gd")
const AfternoonView = preload("res://stages/afternoon/Main.gd")
const WorkView = preload("res://stages/work/DrinkView.gd")
var session := Session.new()
var active_view
var overlay: CanvasLayer
var ui: Control
var font: SystemFont
var generation := 0
var transition_pending := false
var home_line := 0
var exit_button: Button
var retry_button: Button
var return_dialog: ConfirmationDialog

func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei UI", "Microsoft JhengHei", "Noto Sans CJK TC"])
	overlay = CanvasLayer.new()
	add_child(overlay)
	ui = Control.new()
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(ui)
	show_stage()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_R or event.physical_keycode == KEY_R or event.unicode in [82, 114]:
			get_viewport().set_input_as_handled()
			reset_day()

func _process(_delta: float) -> void:
	if is_instance_valid(active_view) and not transition_pending:
		if session.phase == Session.Phase.BREAKFAST and active_view.game.phase == Session.Breakfast.Phase.DONE:
			transition_pending = true
			call_deferred("transfer_breakfast", generation)
		elif session.phase == Session.Phase.WORK and active_view.game.phase == Session.Drink.Phase.DONE:
			transition_pending = true
			call_deferred("transfer_work", generation)
	if session.phase == Session.Phase.AFTERNOON and is_instance_valid(active_view):
		if is_instance_valid(exit_button):
			exit_button.disabled = active_view.game.mode == Session.Encounter.Mode.COMBAT
		if is_instance_valid(retry_button):
			retry_button.visible = active_view.game.mode == Session.Encounter.Mode.DEFEAT
	queue_redraw()

func transfer_breakfast(expected_generation: int) -> void:
	if expected_generation != generation:
		return
	transition_pending = false
	if is_instance_valid(active_view) and session.accept_breakfast(active_view.game):
		show_stage()

func transfer_work(expected_generation: int) -> void:
	if expected_generation != generation:
		return
	transition_pending = false
	if is_instance_valid(active_view) and session.finish_work(active_view.game):
		show_stage()

func reset_day() -> void:
	generation += 1
	transition_pending = false
	home_line = 0
	session.reset()
	show_stage()

func show_stage() -> void:
	if is_instance_valid(active_view):
		active_view.hide()
		active_view.set_process(false)
		active_view.set_process_unhandled_input(false)
		active_view.queue_free()
	active_view = null
	for child in ui.get_children():
		child.hide()
		child.set_block_signals(true)
		child.queue_free()
	exit_button = null
	retry_button = null
	return_dialog = null
	match session.phase:
		Session.Phase.BREAKFAST:
			active_view = BreakfastView.new()
		Session.Phase.AFTERNOON:
			active_view = AfternoonView.new()
		Session.Phase.WORK:
			active_view = WorkView.new()
	if is_instance_valid(active_view):
		add_child(active_view)
		if session.phase == Session.Phase.WORK:
			active_view.game.start()
			active_view.queue_redraw()
	build_controls()
	queue_redraw()

func button(rect: Rect2, caption: String, callback: Callable, parent: Node = null) -> Button:
	var control := Button.new()
	control.position = rect.position
	control.size = rect.size
	control.text = caption
	control.focus_mode = Control.FOCUS_NONE
	control.add_theme_font_override("font", font)
	control.add_theme_font_size_override("font_size", 17)
	var style := StyleBoxFlat.new()
	style.bg_color = Color("#4a6a60")
	style.set_corner_radius_all(8)
	control.add_theme_stylebox_override("normal", style)
	control.add_theme_stylebox_override("hover", style.duplicate())
	control.pressed.connect(callback)
	(parent if parent != null else ui).add_child(control)
	return control

func build_controls() -> void:
	# A GUI layer consumes clicks over the old per-stage reset buttons.
	var cap := ColorRect.new()
	cap.position = Vector2(930, 8)
	cap.size = Vector2(340, 95)
	cap.color = Color("#1f3430")
	cap.mouse_filter = Control.MOUSE_FILTER_STOP
	ui.add_child(cap)
	button(Rect2(1110, 18, 145, 40), "R 重玩整天", reset_day)
	var status := Label.new()
	status.position = Vector2(945, 68)
	status.add_theme_font_override("font", font)
	status.add_theme_font_size_override("font_size", 15)
	status.text = "共用金錢：%d  ｜  %s" % [session.money, stage_name()]
	status.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(status)
	match session.phase:
		Session.Phase.DEPARTURE:
			button(Rect2(710, 620, 470, 62), "前往線索地點，開始下午調查", depart)
		Session.Phase.AFTERNOON:
			exit_button = button(Rect2(945, 18, 155, 40), "結束下午／返家", request_return)
			retry_button = button(Rect2(695, 18, 220, 40), "重新調查（測試用）", retry_afternoon)
			retry_button.visible = false
		Session.Phase.EVENING:
			button(Rect2(80, 565, 515, 78), "諾亞去薇斯帕酒館打工", choose_work)
			button(Rect2(685, 565, 515, 78), "諾亞留在安全屋陪洛芙", choose_home)
		Session.Phase.HOME:
			button(Rect2(795, 650, 400, 58), "繼續聊天" if home_line < 1 else "一起度過今晚，查看結算", continue_home)
		Session.Phase.SUMMARY:
			button(Rect2(820, 670, 375, 62), "重新體驗一天（全部重置）", reset_day)

func depart() -> void:
	if session.depart():
		show_stage()

func request_return() -> void:
	if session.phase != Session.Phase.AFTERNOON or not is_instance_valid(active_view):
		return
	if active_view.game.mode == Session.Encounter.Mode.COMBAT or is_instance_valid(return_dialog):
		return
	active_view.walking.clear()
	active_view.set_process(false)
	return_dialog = ConfirmationDialog.new()
	return_dialog.title = "結束下午調查？"
	return_dialog.dialog_text = "離開後會直接進入晚上，今天不能再選另一處調查。\n" + ("已取得調查物品。" if active_view.game.evidence else "尚未取得線索也能離開；本原型只演示一天。")
	return_dialog.ok_button_text = "返家，進入晚上"
	return_dialog.cancel_button_text = "繼續調查"
	return_dialog.add_theme_font_override("font", font)
	return_dialog.confirmed.connect(confirm_return)
	return_dialog.canceled.connect(cancel_return)
	ui.add_child(return_dialog)
	return_dialog.popup_centered(Vector2i(660, 190))

func cancel_return() -> void:
	if is_instance_valid(return_dialog):
		return_dialog.queue_free()
	return_dialog = null
	if is_instance_valid(active_view):
		active_view.set_process(true)

func confirm_return() -> void:
	if session.phase == Session.Phase.AFTERNOON and is_instance_valid(active_view):
		if session.finish_afternoon(active_view.game):
			show_stage()

func retry_afternoon() -> void:
	if session.phase == Session.Phase.AFTERNOON and is_instance_valid(active_view):
		active_view.reset_game()

func choose_work() -> void:
	if session.choose_work():
		show_stage()

func choose_home() -> void:
	if session.choose_home():
		home_line = 0
		show_stage()

func continue_home() -> void:
	if session.phase != Session.Phase.HOME:
		return
	if home_line == 0:
		home_line = 1
		show_stage()
	elif session.finish_home():
		show_stage()

func stage_name() -> String:
	return ["早餐與採購", "準備出發", "下午調查", "晚上", "酒館打工", "安全屋", "當日結算"][session.phase]

func text_at(pos: Vector2, text: String, size: int = 20, color: Color = Color("#e5e5d8")) -> void:
	draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)

func panel(rect: Rect2, color: Color = Color("#30413b")) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.set_corner_radius_all(12)
	draw_style_box(style, rect)

func _draw() -> void:
	if font == null:
		return
	draw_rect(Rect2(0, 0, 1280, 800), Color("#1c2b2b"))
	if is_instance_valid(active_view):
		return
	text_at(Vector2(45, 53), "異調童話  /  完整一天", 28)
	text_at(Vector2(45, 89), "早餐 → 採購 → 下午調查 → 晚間活動 → 當日結算", 17, Color("#b1c9bc"))
	match session.phase:
		Session.Phase.DEPARTURE: draw_departure()
		Session.Phase.EVENING: draw_evening()
		Session.Phase.HOME: draw_home()
		Session.Phase.SUMMARY: draw_summary()
	text_at(Vector2(45, 773), "整合原型 · 場景、對話與數值為測試用 · 尚未存檔或連續遊玩第二天", 14, Color("#94ad9e"))

func draw_departure() -> void:
	panel(Rect2(45, 135, 1190, 575))
	text_at(Vector2(77, 186), "採購安排好了。接下來是洛芙的下午。", 26)
	text_at(Vector2(78, 240), "諾亞：我照清單去買東西，晚點見。", 21)
	text_at(Vector2(78, 293), "固定採購：米、雞蛋、日常蔬菜", 20)
	text_at(Vector2(78, 335), "額外採購：" + ("、".join(session.extras) if not session.extras.is_empty() else "無"), 20)
	text_at(Vector2(78, 377), "已預留採購款 %d，剩餘金錢 %d（測試價格）。" % [session.shopping_cost, session.money], 20)
	text_at(Vector2(78, 442), "可調查方向：主線提供的測試地點，不需要早餐情報也可前往。", 20)
	text_at(Vector2(78, 488), "早餐提示：留意組織通訊器，取得後有助減緩追查。" if session.communicator_known else "早餐沒有記下通訊器情報；仍可正常調查與取得物品。", 19, Color("#e4d5a6"))
	text_at(Vector2(78, 547), "一個下午只前往一個場景，離開就進入晚上。", 19)

func draw_evening() -> void:
	panel(Rect2(45, 135, 1190, 565))
	text_at(Vector2(77, 184), "傍晚，洛芙回到安全屋。諾亞也帶回了採購品。", 25)
	text_at(Vector2(78, 236), "下午：" + ("取得調查物品" if session.evidence_found else "沒有取得物品，保留調查方向"), 20)
	text_at(Vector2(78, 278), "已辨識並取得通訊器，追查壓力增量減少 2。" if session.communicator_acquired else "沒有取得可辨識的通訊器加成。", 19, Color("#dacba6"))
	if session.retreated:
		text_at(Vector2(78, 319), "本次戰鬥失敗，以撤退返家處理；正式任務後果尚未設定。", 19, Color("#e1b9a5"))
	else:
		text_at(Vector2(78, 319), "洛芙生命 %d / 8。" % session.louve_hp, 19)
	text_at(Vector2(78, 378), "今晚，諾亞要去工作，還是留下來？", 25)
	text_at(Vector2(80, 436), "去工作：接四張調飲訂單，賺取工資。", 19)
	text_at(Vector2(80, 479), "留下來：一起度過晚上，沒有工資。", 19)
	text_at(Vector2(685, 436), "已記得並買下茄子，打工便當會有她想吃的菜。" if session.eggplant_known and session.extras.has("茄子") else "本日沒有記住並安排的便當喜好加分。", 17, Color("#c4d5b7"))

func draw_home() -> void:
	panel(Rect2(45, 140, 1190, 580))
	text_at(Vector2(80, 195), "安全屋  /  今晚一起待著", 27)
	if home_line == 0:
		text_at(Vector2(80, 290), "諾亞：今天跑了一整天，現在可以一起休息了吧？", 24)
		text_at(Vector2(80, 357), "洛芙：嗯，今晚就留在這裡。", 24)
	else:
		text_at(Vector2(80, 290), "兩人吃完晚餐，聊了些今天的瑣事。", 24)
		text_at(Vector2(80, 357), "諾亞：偶爾這樣也很好。", 24)
	text_at(Vector2(80, 478), "這段安全屋對話為串接流程的佔位內容。", 18, Color("#b9c9bb"))
	text_at(Vector2(80, 526), "共度時光：兩人密切度 +3，今晚不獲得工資（測試值）。", 19)

func draw_summary() -> void:
	panel(Rect2(45, 135, 1190, 590))
	text_at(Vector2(78, 185), "這一天結束了。", 29)
	text_at(Vector2(78, 245), "金錢：100 − 採購 %d ＋ 工資 %d ＝ %d" % [session.shopping_cost, session.work_pay, session.money], 23, Color("#ead2a6"))
	text_at(Vector2(78, 302), "早餐通訊器情報：" + ("取得" if session.communicator_known else "未取得"), 20)
	text_at(Vector2(78, 346), "下午調查物品：" + ("取得" if session.evidence_found else "未取得"), 20)
	text_at(Vector2(78, 390), "通訊器幫助：" + ("已生效" if session.communicator_acquired else "未生效，須先得知情報並取得物品"), 19)
	text_at(Vector2(78, 445), "今晚：" + ("薇斯帕酒館打工，送錯 %d 次" % session.work_errors if session.worked else "留在安全屋，沒有工資"), 20)
	text_at(Vector2(78, 491), "便當：" + ("記住喜好並準備了茄子，兩人密切度 +2" if session.favorite_lunch else "本次無打工便當喜好回饋"), 19)
	text_at(Vector2(730, 305), "本日關係變化（測試值）", 21)
	text_at(Vector2(730, 354), "洛芙與諾亞：%+d" % session.noa_closeness, 23)
	text_at(Vector2(730, 404), "薇斯帕：%+d" % session.ves_closeness, 23)
	text_at(Vector2(730, 476), "追查壓力增量：+%d" % session.exposure_increase, 22)
	text_at(Vector2(78, 564), "只演示一天；沒有完整飽食度、暴露封鎖、存檔或正式劇情。", 17, Color("#b0c4b6"))
	text_at(Vector2(78, 605), "壓力示意：基礎 +5、被發現 +3、取得通訊器 −2。", 17, Color("#b0c4b6"))
