extends Node2D

const Session = preload("res://scripts/DaySession.gd")
const Rules = preload("res://scripts/RelationshipRules.gd")
const Exposure = preload("res://scripts/ExposureRules.gd")
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
var info_dialog: AcceptDialog
var restart_dialog: ConfirmationDialog
var resume_process := false
var resume_input := false

func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei UI", "Microsoft JhengHei", "Noto Sans CJK TC"])
	overlay = CanvasLayer.new()
	add_child(overlay)
	ui = Control.new()
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(ui)
	show_stage()

func modal_open() -> bool:
	return is_instance_valid(info_dialog) or is_instance_valid(restart_dialog) or is_instance_valid(return_dialog)

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_R or event.physical_keycode == KEY_R or event.unicode in [82, 114]:
			get_viewport().set_input_as_handled()
			if not modal_open():
				request_restart()

func _process(_delta: float) -> void:
	if modal_open():
		return
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
	if session.phase == Session.Phase.BREAKTHROUGH and is_instance_valid(active_view):
		if is_instance_valid(exit_button):
			exit_button.disabled = not session.breakthrough_won(active_view.game)
		if session.breakthrough_won(active_view.game):
			active_view.game.message = "看守已清除，按上方「進入據點」繼續原本的下午行動。"
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
	# 僅由新一輪確認或測試呼叫；與 next_day 的保留範圍不同。
	generation += 1
	transition_pending = false
	home_line = 0
	session.reset()
	show_stage()

func next_day() -> void:
	if session.next_day():
		generation += 1
		transition_pending = false
		home_line = 0
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
	info_dialog = null
	restart_dialog = null
	match session.phase:
		Session.Phase.BREAKFAST:
			active_view = BreakfastView.new()
			active_view.game.budget = session.money
		Session.Phase.AFTERNOON, Session.Phase.BREAKTHROUGH:
			active_view = AfternoonView.new()
		Session.Phase.WORK:
			active_view = WorkView.new()
	if is_instance_valid(active_view):
		add_child(active_view)
		if session.phase == Session.Phase.BREAKTHROUGH:
			active_view.game.player = Vector2(15.5, 5.5)
			active_view.game.check_detection()
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
	control.add_theme_font_size_override("font_size", 16)
	var style := StyleBoxFlat.new()
	style.bg_color = Color("#4a6a60")
	style.set_corner_radius_all(8)
	control.add_theme_stylebox_override("normal", style)
	control.add_theme_stylebox_override("hover", style.duplicate())
	control.pressed.connect(callback)
	(parent if parent != null else ui).add_child(control)
	return control

func build_controls() -> void:
	# 覆蓋並消耗舊原型各自的重置按鈕；避免只清空小遊戲。
	var cap := ColorRect.new()
	cap.position = Vector2(930, 8)
	cap.size = Vector2(340, 95)
	cap.color = Color("#1f3430")
	cap.mouse_filter = Control.MOUSE_FILTER_STOP
	ui.add_child(cap)
	button(Rect2(945, 18, 155, 40), "關係／暴露紀錄", show_relationships)
	button(Rect2(1110, 18, 145, 40), "R 新一輪", request_restart)
	var status := Label.new()
	status.position = Vector2(945, 68)
	status.add_theme_font_override("font", font)
	status.add_theme_font_size_override("font_size", 15)
	status.text = "第 %d 天｜$%d｜%s" % [session.day_number, session.money, stage_name()]
	status.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(status)
	match session.phase:
		Session.Phase.BREAKFAST:
			if not session.overnight_notes.is_empty():
				var notice := Label.new()
				notice.position = Vector2(30, 108)
				notice.add_theme_font_override("font", font)
				notice.add_theme_font_size_override("font_size", 16)
				notice.add_theme_color_override("font_color", Color("#6d2424"))
				notice.text = "昨夜：%s%s" % [session.overnight_notes[0], "（共 %d 則，詳見右上紀錄）" % session.overnight_notes.size() if session.overnight_notes.size() > 1 else ""]
				ui.add_child(notice)
			if session.money < Session.FIXED_COST + 12:
				button(Rect2(710, 18, 205, 40), "測試補款 +$50", add_test_funds)
		Session.Phase.DEPARTURE:
			button(Rect2(75, 485, 470, 58), "調查奶奶故居（自由探索／戰鬥）", depart)
			button(Rect2(75, 565, 470, 58), "洛芙休息，諾亞照常採購", rest_afternoon)
			var index := 0
			for site in Rules.SITES:
				var y := 140 + index * 130
				var quest: int = session.next_quest_index(site)
				var title := "支線已完成"
				if quest >= 0:
					title = "%s%d：關係+%d／暴露-%d" % ["關鍵" if quest == 2 else "一般", quest + 1, Rules.QUEST_GAINS[quest], Exposure.QUEST_REDUCTIONS[quest]]
				var quest_button := button(Rect2(625, y + 63, 270, 42), title, begin_visit.bind(site, "quest"))
				quest_button.add_theme_font_size_override("font_size", 14)
				quest_button.disabled = quest < 0 or not session.site_open(site)
				var consume := button(Rect2(905, y + 63, 140, 42), "$10 消費+1", begin_visit.bind(site, "consume"))
				consume.disabled = session.money < Rules.CONSUME_COST or not session.site_open(site)
				var route := button(Rect2(1055, y + 63, 140, 42), "處理看守", begin_visit.bind(site, "route"))
				route.disabled = not session.needs_breakthrough(site)
				index += 1
		Session.Phase.VISIT:
			button(Rect2(730, 620, 450, 60), "完成協助，進入晚上" if session.visit_kind == "quest" else ("結束下午，今晚可通行" if session.visit_kind == "route" else "完成消費，進入晚上"), finish_visit.bind(true))
			if session.visit_kind == "quest":
				button(Rect2(80, 620, 470, 60), "放棄已答應的協助（密切度 -4）", finish_visit.bind(false))
		Session.Phase.BREAKTHROUGH:
			exit_button = button(Rect2(710, 18, 205, 40), "進入據點，繼續行動", finish_breakthrough)
			exit_button.disabled = not session.breakthrough_won(active_view.game)
			button(Rect2(470, 18, 225, 40), "撤退，結束下午", abandon_breakthrough)
			var gate_title := Label.new()
			gate_title.position = Vector2(28, 8)
			gate_title.size = Vector2(430, 90)
			gate_title.add_theme_font_override("font", font)
			gate_title.add_theme_font_size_override("font_size", 19)
			gate_title.text = "突破%s看守\n暴露 %d・%s\n沿用戰鬥測試場景，清除敵人後進入據點" % [Rules.SITES[session.visit_site], session.exposures[session.visit_site], session.site_status(session.visit_site)]
			var gate_background := ColorRect.new()
			gate_background.position = gate_title.position
			gate_background.size = gate_title.size
			gate_background.color = Color("#1a2831")
			gate_background.mouse_filter = Control.MOUSE_FILTER_IGNORE
			ui.add_child(gate_background)
			ui.add_child(gate_title)
		Session.Phase.AFTERNOON:
			exit_button = button(Rect2(710, 18, 205, 40), "結束下午／返家", request_return)
			retry_button = button(Rect2(470, 18, 225, 40), "重新調查（測試用）", retry_afternoon)
			retry_button.visible = false
		Session.Phase.EVENING:
			var work := button(Rect2(80, 565, 515, 78), "諾亞去薇斯帕酒館打工（依表現）", choose_work)
			work.disabled = not session.work_block_reason().is_empty()
			button(Rect2(685, 565, 515, 78), "諾亞留家陪洛芙（+4／無工資）", choose_home)
		Session.Phase.HOME:
			button(Rect2(795, 650, 400, 58), "繼續聊天" if home_line < 1 else "一起度過今晚，查看結算", continue_home)
		Session.Phase.SUMMARY:
			button(Rect2(80, 670, 470, 62), "關係明細與歷日紀錄", show_relationships)
			button(Rect2(720, 670, 475, 62), "睡一覺，開始第 %d 天（保留累積）" % (session.day_number + 1), next_day)

func add_test_funds() -> void:
	if session.add_test_funds() and is_instance_valid(active_view):
		active_view.game.budget = session.money
		# 不重建早餐，避免重新給 QTE 機會。
		for child in ui.get_children():
			child.hide()
			child.queue_free()
		build_controls()
		active_view.queue_redraw()

func suspend_view() -> void:
	if is_instance_valid(active_view):
		resume_process = active_view.is_processing()
		resume_input = active_view.is_processing_unhandled_input()
		active_view.set_process(false)
		active_view.set_process_unhandled_input(false)

func resume_view() -> void:
	if is_instance_valid(active_view):
		active_view.set_process(resume_process)
		active_view.set_process_unhandled_input(resume_input)

func request_restart() -> void:
	if modal_open():
		return
	suspend_view()
	restart_dialog = ConfirmationDialog.new()
	restart_dialog.title = "開始新一輪？"
	restart_dialog.dialog_text = "將清除本輪所有天數、金錢、關係及支線紀錄，回到第 1 天。\n如果只想繼續下一天，請取消並在當日結算選擇睡一覺。"
	restart_dialog.ok_button_text = "清除，開始新一輪"
	restart_dialog.cancel_button_text = "保留，繼續玩"
	restart_dialog.add_theme_font_override("font", font)
	restart_dialog.confirmed.connect(reset_day)
	restart_dialog.canceled.connect(cancel_restart)
	ui.add_child(restart_dialog)
	restart_dialog.popup_centered(Vector2i(700, 200))

func cancel_restart() -> void:
	restart_dialog.hide()
	restart_dialog.queue_free()
	restart_dialog = null
	resume_view()

func report_text() -> String:
	var lines := PackedStringArray(["第 %d 天｜規則 %s｜金錢 $%d" % [session.day_number, Rules.VERSION, session.money], ""])
	for id in session.relationships:
		var value: int = session.relationships[id]
		var name: String = "洛芙與諾亞" if id == "noa" else Rules.SITES[id]
		lines.append("%s：%d／100　%s　今日 %+d" % [name, value, Rules.grade(value, id == "noa"), session.daily_delta(id)])
	lines.append("\n據點暴露（初始 10，每晚 +6，一般支線 -20、關鍵 -35）")
	for site in Rules.SITES:
		lines.append("%s：%d／100　%s　今日 %+d　睡後預計 %d" % [Rules.SITES[site], session.exposures[site], session.site_status(site), session.exposure_delta(site), session.projected_exposure(site)])
		if session.lost_sites.has(site):
			lines.append("　" + session.lost_sites[site] + "；本輪不會因數值下降而恢復。")
	for note in session.overnight_notes:
		lines.append("昨夜：" + note)
	lines.append("\n每日快照（含該日睡前自然上升；不含今天尚未結算的夜間）")
	for row in session.day_history:
		var values := PackedStringArray()
		for id in row.relationships:
			values.append("%s %d" % ["諾亞" if id == "noa" else Rules.SITES[id], row.relationships[id]])
		lines.append("第 %d 天　$%d　%s" % [row.day, row.money, "／".join(values)])
		var exposure_values := PackedStringArray()
		for site in row.exposures:
			exposure_values.append("%s %d%s" % [Rules.SITES[site], row.exposures[site], "（已失去）" if row.lost_sites.has(site) else ""])
		lines.append("　暴露：" + "／".join(exposure_values))
	lines.append("\n逐筆關係紀錄（含上限截斷後的實際變化）")
	if session.relationship_log.is_empty():
		lines.append("尚無變化；固定早餐、普通閒聊與漏接話題不扣分。")
	for row in session.relationship_log:
		var name: String = "諾亞" if row.id == "noa" else Rules.SITES[row.id]
		lines.append("第 %d 天｜%s %+d｜%d → %d｜%s" % [row.day, name, row.delta, row.before, row.after, row.reason])
	lines.append("\n逐筆暴露變化（本輪失去後不可恢復）")
	for row in session.exposure_log:
		lines.append("第 %d 天｜%s %+d｜%d → %d｜%s" % [row.day, Rules.SITES[row.id], row.delta, row.before, row.after, row.reason])
	lines.append("\n金錢與線索跨日保留；每日採購與便當喜好重置。無關係自然衰退。")
	lines.append("本版沒有磁碟存檔；關閉後清除本輪。飽食度、失守後遠端補給與正式劇情尚未接入。")
	return "\n".join(lines)

func show_relationships() -> void:
	if modal_open():
		return
	suspend_view()
	info_dialog = AcceptDialog.new()
	info_dialog.title = "關係與據點暴露｜可捲動查看；關閉後繼續"
	info_dialog.ok_button_text = "回到遊戲"
	info_dialog.add_theme_font_override("font", font)
	var report := RichTextLabel.new()
	report.position = Vector2(20, 20)
	report.size = Vector2(960, 510)
	report.add_theme_font_override("normal_font", font)
	report.add_theme_font_size_override("normal_font_size", 18)
	report.text = report_text()
	report.selection_enabled = true
	info_dialog.add_child(report)
	info_dialog.confirmed.connect(close_relationships)
	info_dialog.canceled.connect(close_relationships)
	ui.add_child(info_dialog)
	info_dialog.popup_centered(Vector2i(1000, 600))

func close_relationships() -> void:
	info_dialog.hide()
	info_dialog.queue_free()
	info_dialog = null
	resume_view()

func depart() -> void:
	if session.depart():
		show_stage()

func begin_visit(site: String, kind: String) -> void:
	if session.begin_visit(site, kind):
		show_stage()

func finish_visit(fulfilled: bool) -> void:
	if session.finish_visit(fulfilled):
		show_stage()

func finish_breakthrough() -> void:
	if is_instance_valid(active_view) and session.finish_breakthrough(active_view.game):
		show_stage()

func abandon_breakthrough() -> void:
	if session.abandon_breakthrough():
		show_stage()

func rest_afternoon() -> void:
	if session.rest_afternoon():
		show_stage()

func request_return() -> void:
	if session.phase != Session.Phase.AFTERNOON or not is_instance_valid(active_view) or modal_open():
		return
	if active_view.game.mode == Session.Encounter.Mode.COMBAT:
		return
	active_view.walking.clear()
	suspend_view()
	return_dialog = ConfirmationDialog.new()
	return_dialog.title = "結束下午調查？"
	return_dialog.dialog_text = "離開後直接進入晚上，今天不能再選另一處調查。\n" + ("已取得調查物品。" if active_view.game.evidence else "尚未取得線索；可以隔天再來。")
	return_dialog.ok_button_text = "返家，進入晚上"
	return_dialog.cancel_button_text = "繼續調查"
	return_dialog.add_theme_font_override("font", font)
	return_dialog.confirmed.connect(confirm_return)
	return_dialog.canceled.connect(cancel_return)
	ui.add_child(return_dialog)
	return_dialog.popup_centered(Vector2i(660, 190))

func cancel_return() -> void:
	return_dialog.hide()
	return_dialog.queue_free()
	return_dialog = null
	resume_view()

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
	return ["早餐採購", "下午安排", "下午調查", "晚上", "酒館打工", "安全屋", "當日結算", "據點協助", "突破看守"][session.phase]

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
	text_at(Vector2(45, 53), "異調童話 / 第 %d 天" % session.day_number, 28)
	text_at(Vector2(45, 89), "早餐 → 採購 → 下午行動 → 晚間活動 → 結算 → 下一天", 17, Color("#b1c9bc"))
	match session.phase:
		Session.Phase.DEPARTURE: draw_departure()
		Session.Phase.VISIT: draw_visit()
		Session.Phase.EVENING: draw_evening()
		Session.Phase.HOME: draw_home()
		Session.Phase.SUMMARY: draw_summary()
	text_at(Vector2(45, 773), "關係與暴露測試 · 每晚暴露+6 · 60起需突破／100失守 · 關閉後本輪不保留", 14, Color("#94ad9e"))

func draw_departure() -> void:
	panel(Rect2(45, 135, 530, 575))
	text_at(Vector2(75, 181), "諾亞去採購，洛芙選擇下午的行動。", 22)
	text_at(Vector2(75, 230), "額外品項：" + ("、".join(session.extras) if not session.extras.is_empty() else "無"), 19)
	text_at(Vector2(75, 273), "採購款 $%d 已扣，剩餘 $%d。" % [session.shopping_cost, session.money], 19)
	text_at(Vector2(75, 326), "一次只能選一項；完成或離開就到晚上。", 18)
	text_at(Vector2(75, 370), "也可直接休息，加快觀察晚間關係累積。", 18)
	text_at(Vector2(75, 417), "調查線索跨日保留；重訪不會重複加關係。", 17)
	text_at(Vector2(75, 670), "右側任務是關係測試佔位，沒有正式情節。", 17, Color("#d5cba5"))
	var index := 0
	for site in Rules.SITES:
		var y := 140 + index * 130
		panel(Rect2(605, y, 610, 118))
		text_at(Vector2(625, y + 25), "%s　關係 %d · %s" % [Rules.SITES[site], session.relationships[site], Rules.grade(session.relationships[site])], 18)
		text_at(Vector2(625, y + 50), "暴露 %d／100 · %s　睡後預計 %d" % [session.exposures[site], session.site_status(site), session.projected_exposure(site)], 17, exposure_color(session.exposures[site]))
		index += 1
	text_at(Vector2(625, 684), "60 起先突破再執行行動；80 且未友好提前失去據點。", 16, Color("#d5cba5"))

func draw_visit() -> void:
	panel(Rect2(45, 135, 1190, 575))
	text_at(Vector2(80, 195), session.activity, 28)
	text_at(Vector2(80, 260), "據點內的兄弟姊妹共用這條密切度，不另外拆分。", 22)
	if session.visit_kind == "quest":
		var index: int = session.next_quest_index(session.visit_site)
		text_at(Vector2(80, 330), "佔位支線 %d：處理據點周遭的追查。" % (index + 1), 24)
		text_at(Vector2(80, 390), "完成後關係 +%d、暴露 -%d；每項只可領取一次。" % [Rules.QUEST_GAINS[index], Exposure.QUEST_REDUCTIONS[index]], 21)
		text_at(Vector2(80, 450), "此畫面只測試任務的時間成本與關係獎勵，不代表正式故事。", 19, Color("#d5cba5"))
		text_at(Vector2(80, 510), "選放棄代表已經答應後失約（-4）；單純沒選任務不扣分。", 19)
	elif session.visit_kind == "route":
		text_at(Vector2(80, 330), "洛芙已清除路線上的看守。", 24)
		text_at(Vector2(80, 390), "今天這個據點可以通行；諾亞晚上可以安全抵達酒館。", 21)
		text_at(Vector2(80, 450), "單純清除看守不降低暴露、不加關係；明天需要重新判斷。", 19)
	else:
		text_at(Vector2(80, 330), "正常消費 $10，密切度 +1。", 24)
		text_at(Vector2(80, 390), "消費完成後，這個下午就結束。", 21)
		text_at(Vector2(80, 450), "測試價格；每組據點每天最多獲得一次消費加分。", 19)

func draw_evening() -> void:
	panel(Rect2(45, 135, 1190, 565))
	text_at(Vector2(77, 184), "傍晚，兩人回到安全屋。今晚要怎麼過？", 25)
	text_at(Vector2(78, 242), "下午：" + session.activity, 20)
	text_at(Vector2(78, 286), session.visit_result if not session.visit_result.is_empty() else ("調查物品已記錄。" if session.evidence_found else "今天沒有新的調查收穫。"), 19)
	text_at(Vector2(78, 336), "諾亞 %d · %s　｜　薇斯帕 %d · %s" % [session.noa_closeness, Rules.grade(session.noa_closeness, true), session.ves_closeness, Rules.grade(session.ves_closeness)], 22)
	text_at(Vector2(80, 411), "打工：四張訂單；零失誤 +3，1～2 次 +1，更多 -1。", 19)
	text_at(Vector2(80, 454), "留家：洛芙與諾亞 +4，今晚沒有收入。", 19)
	text_at(Vector2(80, 501), "記住並買下茄子：今晚的打工便當會額外使兩人 +2。" if session.eggplant_known and session.extras.has("茄子") else "今天沒有安排符合早餐喜好的打工便當；不扣分。", 19, Color("#c4d5b7"))
	var block: String = session.work_block_reason()
	if not block.is_empty():
		text_at(Vector2(80, 540), block, 16, Color("#f1ac91"))
	else:
		text_at(Vector2(80, 540), "酒館暴露 %d · %s" % [session.exposures.ves, session.site_status("ves")], 16, exposure_color(session.exposures.ves))

func draw_home() -> void:
	panel(Rect2(45, 140, 1190, 580))
	text_at(Vector2(80, 195), "安全屋 / 今晚一起待著", 27)
	if home_line == 0:
		text_at(Vector2(80, 290), "諾亞：現在可以一起休息了吧？", 24)
		text_at(Vector2(80, 357), "洛芙：嗯，今晚就留在這裡。", 24)
	else:
		text_at(Vector2(80, 290), "兩人吃完晚餐，聊了些今天的瑣事。", 24)
		text_at(Vector2(80, 357), "諾亞：偶爾這樣也很好。", 24)
	text_at(Vector2(80, 478), "不限時的佔位對話；讀完才結算，不會每按一次就加分。", 18)
	text_at(Vector2(80, 526), "共度時光：兩人密切度 +4，今晚不獲得工資。", 19)

func draw_summary() -> void:
	panel(Rect2(45, 135, 1190, 610))
	text_at(Vector2(78, 183), "第 %d 天結束了。" % session.day_number, 29)
	text_at(Vector2(78, 230), "金錢 $%d → $%d　採購 -%d／消費 -%d／工資 +%d／測試補款 +%d" % [session.day_start_money, session.money, session.shopping_cost, session.visit_spent, session.work_pay, session.debug_funds], 19, Color("#ead2a6"))
	var index := 0
	for id in session.relationships:
		var y := 287 + index * 57
		var value: int = session.relationships[id]
		var name: String = "洛芙與諾亞" if id == "noa" else Rules.SITES[id]
		text_at(Vector2(78, y), "%s　%d／100 · %s　今日 %+d" % [name, value, Rules.grade(value, id == "noa"), session.daily_delta(id)], 21)
		draw_rect(Rect2(80, y + 12, 520, 6), Color("#20322e"))
		draw_rect(Rect2(80, y + 12, 520 * value / 100.0, 6), Color("#a2bc89"))
		index += 1
	text_at(Vector2(710, 275), "據點暴露　目前 → 睡後預計", 21)
	var site_index := 0
	for site in Rules.SITES:
		var y := 320 + site_index * 57
		var value: int = session.exposures[site]
		text_at(Vector2(710, y), "%s　%d → %d · %s" % [Rules.SITES[site], value, session.projected_exposure(site), session.site_status(site)], 17, exposure_color(value))
		text_at(Vector2(710, y + 22), "今天 %+d；%s" % [session.exposure_delta(site), "本輪已失去" if not session.site_open(site) else "睡前自然 +6"], 14)
		site_index += 1
	text_at(Vector2(710, 575), "支線立即降低；按睡一覺才結算自然上升。", 16)
	text_at(Vector2(78, 600), "線索：%s　通訊器：%s（跨日保留）" % ["已取得" if session.permanent_evidence else "未取得", "已取得" if session.permanent_communicator else "未取得"], 18)
	text_at(Vector2(78, 638), "關係不自然衰退；暴露會上升。右上可看逐筆原因與歷日快照。", 17)

func exposure_color(value: int) -> Color:
	if value >= 80:
		return Color("#f28c85")
	if value >= 60:
		return Color("#efb075")
	if value >= 30:
		return Color("#e3d698")
	return Color("#b6d4b0")
