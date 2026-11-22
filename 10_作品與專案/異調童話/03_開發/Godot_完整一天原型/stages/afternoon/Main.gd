extends Node2D

const Encounter = preload("res://stages/afternoon/EncounterModel.gd")
const BOARD := Transform2D(Vector2(46, -2), Vector2(10, 30), Vector2(105, 155))
const RESET := Rect2(1030, 23, 210, 40)
const END_TURN := Rect2(1010, 681, 225, 48)
var game := Encounter.new()
var font: SystemFont
var walking: Array[Vector2] = []
var show_sight := true
var enemy_index := -1
var enemy_delay := 0.0
var previous_message := ""
var history: Array[String] = []

func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft JhengHei UI", "Microsoft JhengHei", "Noto Sans CJK TC"])
	queue_redraw()

func screen(point: Vector2) -> Vector2:
	return BOARD * point

func world(point: Vector2) -> Vector2:
	return BOARD.affine_inverse() * point

func direction_input() -> Vector2:
	return Vector2(float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT)) - float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT)), float(Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN)) - float(Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP)))

func _process(delta: float) -> void:
	if game.mode == Encounter.Mode.EXPLORE:
		var direction := direction_input()
		if direction != Vector2.ZERO:
			walking.clear()
			var step := direction.normalized() * 3.4 * delta
			var next_x := game.player + Vector2(step.x, 0)
			if game.can_stand(next_x):
				game.player.x = next_x.x
			var next_y := game.player + Vector2(0, step.y)
			if game.can_stand(next_y):
				game.player.y = next_y.y
		walk(delta, 3.4)
		if game.check_detection():
			walking.clear()
	elif game.mode == Encounter.Mode.COMBAT:
		if game.player_turn:
			walk(delta, 6.0)
		else:
			enemy_delay -= delta
			if enemy_delay <= 0:
				if enemy_index < game.guards.size():
					game.enemy_action(enemy_index)
					enemy_index += 1
					enemy_delay = 0.65
				else:
					game.player_turn = true
					game.turn += 1
					game.moves = Encounter.MOVE_BUDGET
					game.actions = 1
					game.message = "輪到洛芙。點擊地面移動，點守衛射擊，空白鍵結束回合。"
	if game.message != previous_message:
		previous_message = game.message
		history.push_front(game.message)
		if history.size() > 3:
			history.resize(3)
	queue_redraw()

func walk(delta: float, speed: float) -> void:
	if walking.is_empty():
		return
	var next := game.player.move_toward(walking[0], speed * delta)
	if game.can_stand(next):
		game.player = next
	else:
		walking.clear()
		return
	if game.player.distance_to(walking[0]) < 0.01:
		walking.pop_front()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		var pressed_key: int = event.physical_keycode
		if pressed_key == 0:
			pressed_key = event.keycode
		if pressed_key == 0 and event.unicode > 0:
			pressed_key = event.unicode
		# Some input methods inject Unicode without a physical key code.
		if event.unicode >= 97 and event.unicode <= 122:
			pressed_key = event.unicode - 32
		match pressed_key:
			KEY_R:
				reset_game()
			KEY_V:
				show_sight = not show_sight
			KEY_SPACE:
				end_turn()
			KEY_E:
				interact()
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		click(event.position)

func reset_game() -> void:
	game.reset()
	walking.clear()
	history.clear()
	previous_message = ""
	enemy_index = -1
	enemy_delay = 0

func interact() -> void:
	if game.mode == Encounter.Mode.EXPLORE:
		if game.player.distance_to(Encounter.OBJECTIVE) < 1.4 and walking.is_empty() and direction_input() == Vector2.ZERO:
			game.collect_evidence()
		else:
			game.assassinate(walking.is_empty() and direction_input() == Vector2.ZERO)

func end_turn() -> void:
	if game.mode != Encounter.Mode.COMBAT or not game.player_turn:
		return
	if not walking.is_empty():
		game.message = "請等洛芙移動完成，再結束回合。"
		return
	game.player_turn = false
	enemy_index = 0
	enemy_delay = 0.35
	game.message = "敵方回合。"

func click(point: Vector2) -> void:
	if RESET.has_point(point):
		reset_game()
		return
	if END_TURN.has_point(point):
		if game.mode == Encounter.Mode.EXPLORE:
			interact()
		else:
			end_turn()
		return
	if point.y < 105 or point.y > 610 or game.mode == Encounter.Mode.DEFEAT:
		return
	if game.mode == Encounter.Mode.COMBAT and (not game.player_turn or not walking.is_empty()):
		return
	if game.mode == Encounter.Mode.COMBAT:
		for index in range(game.guards.size()):
			var foot := screen(game.guards[index].pos)
			if game.guards[index].hp > 0 and Rect2(foot - Vector2(22, 64), Vector2(44, 73)).has_point(point):
				game.attack(index)
				return
	var destination := game.cell(world(point))
	var route: Array[Vector2i] = game.path(game.player, destination)
	if route.is_empty():
		game.message = "無法走到該位置；牆壁與存活的守衛會阻擋通行。"
		return
	if game.mode == Encounter.Mode.COMBAT:
		var cost := route.size() - 1
		if cost > game.moves:
			game.message = "超出本回合剩餘移動範圍。"
			return
		game.moves -= cost
	walking.clear()
	# Keep the current position when combat begins; move along the next cells.
	for index in range(1, route.size()):
		walking.append(game.center(route[index]))
	if game.mode == Encounter.Mode.EXPLORE:
		game.message = "正在前往指定位置；再次按方向鍵可取消自動移動。"

func text_at(point: Vector2, text: String, size: int = 16, color: Color = Color("#e4e8e1"), width: float = -1) -> void:
	draw_string(font, point, text, HORIZONTAL_ALIGNMENT_LEFT, width, size, color)

func tile(point: Vector2i, color: Color) -> void:
	var p := Vector2(point)
	draw_colored_polygon(PackedVector2Array([screen(p), screen(p + Vector2.RIGHT), screen(p + Vector2.ONE), screen(p + Vector2.DOWN)]), color)

func _draw() -> void:
	if font == null:
		return
	draw_rect(Rect2(0, 0, 1280, 800), Color("#141d24"))
	# A fixed oblique view with shared world coordinates for both play modes.
	var floor_points := PackedVector2Array([screen(Vector2.ZERO), screen(Vector2(20, 0)), screen(Vector2(20, 14)), screen(Vector2(0, 14))])
	draw_colored_polygon(floor_points, Color("#384345"))
	draw_polyline(PackedVector2Array([floor_points[0], floor_points[1], floor_points[2], floor_points[3], floor_points[0]]), Color("#8d9d91"), 2)
	for x in range(21):
		draw_line(screen(Vector2(x, 0)), screen(Vector2(x, 14)), Color(0.8, 0.85, 0.8, 0.08), 1)
	for y in range(15):
		draw_line(screen(Vector2(0, y)), screen(Vector2(20, y)), Color(0.8, 0.85, 0.8, 0.08), 1)
	if game.mode == Encounter.Mode.EXPLORE and show_sight:
		for index in range(game.guards.size()):
			draw_cone(index)
	if game.mode == Encounter.Mode.COMBAT and game.player_turn and walking.is_empty():
		for point in game.reachable():
			tile(point, Color(0.2, 0.8, 0.76, 0.18))
		var hovered := game.cell(world(get_global_mouse_position()))
		if Rect2i(Vector2i.ZERO, Encounter.SIZE).has_point(hovered):
			var route: Array[Vector2i] = game.path(game.player, hovered)
			if route.size() > 1 and route.size() - 1 <= game.moves:
				for index in range(1, route.size()):
					draw_line(screen(game.center(route[index - 1])), screen(game.center(route[index])), Color("#a4eee3"), 3)
	draw_objective()
	var depth: Array[Dictionary] = [{"type": "wall", "y": screen(Encounter.WALL.end).y}, {"type": "player", "y": screen(game.player).y}]
	for index in range(game.guards.size()):
		depth.append({"type": "guard", "y": screen(game.guards[index].pos).y, "index": index})
	depth.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return a.y < b.y)
	for item in depth:
		match item.type:
			"wall": draw_wall()
			"player": draw_actor(game.player, Color("#b8c3ce"), "洛芙", game.hp, true)
			"guard":
				var guard: Dictionary = game.guards[item.index]
				if guard.hp <= 0:
					var foot := screen(guard.pos)
					draw_line(foot + Vector2(-14, -4), foot + Vector2(14, 4), Color("#865b58"), 9)
					text_at(foot + Vector2(-28, 22), "已解決", 12, Color("#aeb5b0"))
				else:
					draw_actor(guard.pos, Color("#ba8566"), guard.name, guard.hp, false)
					var direction: Vector2 = (screen(guard.pos + guard.facing) - screen(guard.pos)).normalized()
					draw_line(screen(guard.pos) + direction * 17, screen(guard.pos) + direction * 35, Color("#f0ba84"), 3)
	var target: int = game.assassination_target()
	if target >= 0:
		var foot := screen(game.guards[target].pos)
		draw_arc(foot, 25, 0, TAU, 32, Color("#9ce8ac"), 3)
		text_at(foot + Vector2(-45, -83), "停下後 E 暗殺", 15, Color("#b7f1bc"))
	draw_hud()

func draw_cone(index: int) -> void:
	var guard: Dictionary = game.guards[index]
	if guard.hp <= 0:
		return
	var polygon := PackedVector2Array([screen(guard.pos)])
	for step in range(33):
		var angle: float = guard.facing.angle() - PI / 4 + float(step) / 32 * PI / 2
		var ray := Vector2.from_angle(angle)
		var distance := 0.0
		while distance < Encounter.SIGHT_RANGE:
			var point: Vector2 = guard.pos + ray * (distance + 0.1)
			if point.x < 0 or point.x > 20 or point.y < 0 or point.y > 14 or not game.line_clear(guard.pos, point):
				break
			distance += 0.1
		polygon.append(screen(guard.pos + ray * distance))
	draw_colored_polygon(polygon, Color(0.98, 0.6, 0.36, 0.17))
	draw_polyline(polygon, Color(1.0, 0.68, 0.4, 0.28), 1)

func draw_wall() -> void:
	var wall: Rect2 = Encounter.WALL
	var a := screen(wall.position)
	var b := screen(wall.position + Vector2(wall.size.x, 0))
	var c := screen(wall.end)
	var d := screen(wall.position + Vector2(0, wall.size.y))
	var up := Vector2(0, -62)
	draw_colored_polygon(PackedVector2Array([b, c, c + up, b + up]), Color("#535b62"))
	draw_colored_polygon(PackedVector2Array([d, c, c + up, d + up]), Color("#62717b"))
	draw_colored_polygon(PackedVector2Array([a + up, b + up, c + up, d + up]), Color("#8a999e"))
	draw_polyline(PackedVector2Array([a + up, b + up, c + up, d + up, a + up]), Color("#b0b9b6"), 2)
	text_at((c + d) / 2 + Vector2(-27, -20), "遮擋牆", 13)

func draw_actor(position: Vector2, color: Color, label: String, health: int, wolf: bool) -> void:
	var foot := screen(position)
	draw_circle(foot, 14, Color(0, 0, 0, 0.3))
	if wolf:
		draw_arc(foot, 20, 0, TAU, 32, Color("#9be5d9"), 2)
	draw_line(foot + Vector2(-5, -13), foot + Vector2(-6, -2), Color("#19252e"), 6)
	draw_line(foot + Vector2(5, -13), foot + Vector2(6, -2), Color("#19252e"), 6)
	draw_colored_polygon(PackedVector2Array([foot + Vector2(-10, -37), foot + Vector2(10, -37), foot + Vector2(13, -12), foot + Vector2(-13, -12)]), color)
	draw_circle(foot + Vector2(0, -45), 10, Color("#d8c4ac") if not wolf else Color("#737f88"))
	if wolf:
		draw_colored_polygon(PackedVector2Array([foot + Vector2(-9, -48), foot + Vector2(-10, -62), foot + Vector2(-1, -53)]), color)
		draw_colored_polygon(PackedVector2Array([foot + Vector2(9, -48), foot + Vector2(10, -62), foot + Vector2(1, -53)]), color)
	draw_line(foot + Vector2(7, -29), foot + Vector2(22, -25), Color("#20282d"), 4)
	draw_rect(Rect2(foot + Vector2(-18, -73), Vector2(36, 4)), Color("#263034"))
	draw_rect(Rect2(foot + Vector2(-18, -73), Vector2(36 * float(health) / (8 if wolf else 4), 4)), Color("#a1ded0") if wolf else Color("#dc986e"))
	text_at(foot + Vector2(-23, 30), label, 13)

func draw_objective() -> void:
	var point := screen(Encounter.OBJECTIVE)
	draw_circle(point, 18, Color("#527f74"))
	draw_rect(Rect2(point + Vector2(-9, -17), Vector2(18, 24)), Color("#e1d8b6"))
	text_at(point + Vector2(-40, -35), "測試文件", 14, Color("#c4e5c5"))
	if game.evidence:
		text_at(point + Vector2(-26, 34), "已取得", 13)
	elif game.mode == Encounter.Mode.EXPLORE and game.player.distance_to(Encounter.OBJECTIVE) < 1.4:
		text_at(point + Vector2(-35, 34), "E 調查", 16, Color("#a9efcf"))

func button(rect: Rect2, label: String, active: bool = true) -> void:
	draw_style_box(make_panel(Color("#344f54") if active else Color("#293439")), rect)
	text_at(rect.position + Vector2(16, 27), label, 16)

func make_panel(color: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.corner_radius_top_left = 7
	style.corner_radius_top_right = 7
	style.corner_radius_bottom_left = 7
	style.corner_radius_bottom_right = 7
	return style

func draw_hud() -> void:
	draw_rect(Rect2(0, 0, 1280, 104), Color("#1a2831"))
	var state := "自由探索" if game.mode == Encounter.Mode.EXPLORE else ("戰鬥失敗" if game.mode == Encounter.Mode.DEFEAT else ("洛芙回合" if game.player_turn else "敵方回合"))
	text_at(Vector2(30, 39), "異調童話  /  潛行與戰棋", 24)
	text_at(Vector2(30, 73), "%s　｜　洛芙生命 %d / 8　｜　文件：%s" % [state, game.hp, "已取得" if game.evidence else "未取得"], 17, Color("#a8ddd3"))
	button(RESET, "R  重新測試")
	text_at(Vector2(680, 84), "測試數值與佔位美術 · V 切換視野顯示", 14, Color("#b3bebc"))
	draw_rect(Rect2(18, 610, 1244, 174), Color("#1a2831"))
	if game.mode == Encounter.Mode.COMBAT:
		text_at(Vector2(36, 643), "第 %d 回合　移動剩餘 %d 格　攻擊剩餘 %d 次　｜　射程 5 格距離，命中固定傷害 2" % [game.turn, game.moves, game.actions], 17, Color("#abeee0"))
		button(END_TURN, "空白鍵  結束回合", game.player_turn)
	else:
		text_at(Vector2(36, 643), "目標：取得右上方文件。可避開守衛、背後暗殺，或正面戰鬥。", 17, Color("#c2e4d8"))
		if game.mode == Encounter.Mode.EXPLORE:
			button(END_TURN, "E  暗殺／調查")
	text_at(Vector2(36, 674), game.message, 16, Color("#f1d2a8"), 1170)
	text_at(Vector2(36, 708), "探索：WASD／方向鍵移動，左鍵點地面尋路；靠近背後停下後 E 暗殺。", 14, Color("#b6c4c6"), 950)
	text_at(Vector2(36, 733), "戰鬥：左鍵地面移動，左鍵守衛射擊；綠色區域為可移動範圍。", 14, Color("#b6c4c6"), 950)
	if history.size() > 1:
		text_at(Vector2(36, 765), "上一則：" + history[1], 13, Color("#8e9fa6"), 1170)
