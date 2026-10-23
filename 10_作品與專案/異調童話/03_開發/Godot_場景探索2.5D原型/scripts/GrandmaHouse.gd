extends Node2D

const PLAYER_SPEED := 250.0
const INTERACT_DISTANCE := 112.0
const NO_TARGET := Vector2(-10000.0, -10000.0)

var floor_polygon := PackedVector2Array([
	Vector2(255, 350),
	Vector2(1040, 350),
	Vector2(1200, 690),
	Vector2(82, 690),
])

var props: Array[Dictionary] = []
var player_position := Vector2(650, 615)
var move_target := NO_TARGET
var in_room := false
var status_message := "點選奶奶故居，進入無劇情操作測試。"
var ui_font: SystemFont

const HOME_BUTTON := Rect2(410, 290, 390, 116)
const RESET_BUTTON := Rect2(870, 716, 150, 48)
const MAP_BUTTON := Rect2(1036, 716, 204, 48)


func _ready() -> void:
	ui_font = SystemFont.new()
	ui_font.font_names = PackedStringArray([
		"Microsoft JhengHei UI",
		"Microsoft JhengHei",
		"Noto Sans CJK TC",
		"Arial",
	])
	props = [
		{
			"name": "矮桌",
			"kind": "table",
			"foot": Vector2(430, 480),
			"hit_rect": Rect2(335, 384, 190, 112),
			"block_rect": Rect2(365, 435, 130, 54),
			"visits": 0,
		},
		{
			"name": "舊櫃",
			"kind": "cabinet",
			"foot": Vector2(845, 438),
			"hit_rect": Rect2(790, 285, 118, 160),
			"block_rect": Rect2(812, 408, 66, 38),
			"visits": 0,
		},
		{
			"name": "木箱",
			"kind": "crate",
			"foot": Vector2(700, 620),
			"hit_rect": Rect2(642, 545, 120, 82),
			"block_rect": Rect2(660, 595, 82, 34),
			"visits": 0,
		},
	]
	queue_redraw()


func _process(delta: float) -> void:
	if not in_room:
		return

	var direction := Vector2.ZERO
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		direction.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		direction.x += 1.0
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		direction.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		direction.y += 1.0

	if direction != Vector2.ZERO:
		move_target = NO_TARGET
		_move_with_collision(direction.normalized() * PLAYER_SPEED * delta)
	elif move_target != NO_TARGET:
		var distance_vector := move_target - player_position
		if distance_vector.length() < 5.0:
			move_target = NO_TARGET
		else:
			var old_position := player_position
			var step: Vector2 = distance_vector.normalized() * min(PLAYER_SPEED * delta, distance_vector.length())
			_move_with_collision(step)
			if player_position.distance_to(old_position) < 0.1:
				move_target = NO_TARGET

	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_E and in_room:
			_interact_nearby()
		elif event.keycode == KEY_ESCAPE and in_room:
			in_room = false
			move_target = NO_TARGET
			status_message = "已回到城市地圖。"
			queue_redraw()
		return

	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_handle_left_click(event.position)


func _handle_left_click(point: Vector2) -> void:
	if not in_room:
		if HOME_BUTTON.has_point(point):
			in_room = true
			player_position = Vector2(650, 615)
			move_target = NO_TARGET
			status_message = "操作測試開始；場景沒有劇情或線索。"
			queue_redraw()
		return

	if RESET_BUTTON.has_point(point):
		player_position = Vector2(650, 615)
		move_target = NO_TARGET
		status_message = "位置已重設。"
		queue_redraw()
		return
	if MAP_BUTTON.has_point(point):
		in_room = false
		move_target = NO_TARGET
		status_message = "已回到城市地圖。"
		queue_redraw()
		return

	var clicked_prop := _prop_at(point)
	if not clicked_prop.is_empty():
		_interact(clicked_prop)
		return

	if Geometry2D.is_point_in_polygon(point, floor_polygon):
		move_target = point
		status_message = "洛芙正在前往指定位置。"
	else:
		status_message = "請點選地板區域移動。"
	queue_redraw()


func _move_with_collision(motion: Vector2) -> void:
	var horizontal := player_position + Vector2(motion.x, 0.0)
	if _can_stand(horizontal):
		player_position.x = horizontal.x

	var vertical := player_position + Vector2(0.0, motion.y)
	if _can_stand(vertical):
		player_position.y = vertical.y


func _can_stand(point: Vector2) -> bool:
	if not Geometry2D.is_point_in_polygon(point, floor_polygon):
		return false
	for prop in props:
		if prop["block_rect"].has_point(point):
			return false
	return true


func _prop_at(point: Vector2) -> Dictionary:
	for index in range(props.size() - 1, -1, -1):
		var prop: Dictionary = props[index]
		if prop["hit_rect"].has_point(point):
			return prop
	return {}


func _nearest_prop() -> Dictionary:
	var nearest: Dictionary = {}
	var shortest := INTERACT_DISTANCE
	for prop in props:
		var distance: float = player_position.distance_to(prop["foot"])
		if distance < shortest:
			shortest = distance
			nearest = prop
	return nearest


func _interact_nearby() -> void:
	var prop := _nearest_prop()
	if prop.is_empty():
		status_message = "先走近一個物件，再按 E。"
	else:
		_interact(prop)
	queue_redraw()


func _interact(prop: Dictionary) -> void:
	prop["visits"] += 1
	status_message = "%s：互動已觸發（測試回饋 %d）" % [prop["name"], prop["visits"]]
	queue_redraw()


func _draw() -> void:
	draw_rect(Rect2(0, 0, 1280, 800), Color("#171b22"))
	if in_room:
		_draw_room()
	else:
		_draw_city_map()
	_draw_hud()


func _draw_city_map() -> void:
	draw_rect(Rect2(0, 0, 1280, 800), Color("#20272a"))
	# Abstract city blocks and roads are visual placeholders, not a map proposal.
	draw_colored_polygon(PackedVector2Array([
		Vector2(0, 435), Vector2(1280, 310), Vector2(1280, 405), Vector2(0, 530),
	]), Color("#645d51"))
	draw_colored_polygon(PackedVector2Array([
		Vector2(530, 85), Vector2(625, 85), Vector2(775, 700), Vector2(680, 700),
	]), Color("#35494b"))

	var blocks := [
		Rect2(95, 190, 190, 135), Rect2(350, 120, 130, 190),
		Rect2(835, 155, 230, 125), Rect2(925, 490, 200, 145),
		Rect2(190, 565, 205, 110),
	]
	for index in range(blocks.size()):
		var color := Color("#3b4d48") if index % 2 == 0 else Color("#514541")
		draw_rect(blocks[index], color)
		draw_rect(blocks[index], Color("#b9ae92"), false, 2.0)

	draw_rect(HOME_BUTTON, Color("#263532"))
	draw_rect(HOME_BUTTON, Color("#b79b6d"), false, 2.0)
	draw_circle(Vector2(HOME_BUTTON.position.x + 36, HOME_BUTTON.position.y + 40), 9, Color("#83aaa3"))
	draw_string(ui_font, Vector2(HOME_BUTTON.position.x + 62, HOME_BUTTON.position.y + 46), "奶奶故居", HORIZONTAL_ALIGNMENT_LEFT, -1, 23, Color("#efe7d8"))
	draw_string(ui_font, Vector2(HOME_BUTTON.position.x + 62, HOME_BUTTON.position.y + 78), "點擊進入 2.5D 場景操作測試", HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color("#bec7c1"))
	draw_string(ui_font, Vector2(70, 620), "城市街區・灰盒地圖", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color("#d7c9aa"))
	draw_string(ui_font, Vector2(70, 650), "地圖與地點只用來串接範例場景。", HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color("#9ba7a3"))


func _draw_room() -> void:
	# Fixed oblique room: painted-style planes with a perspective floor.
	draw_colored_polygon(PackedVector2Array([
		Vector2(92, 74), Vector2(1188, 74), Vector2(1080, 357), Vector2(242, 357),
	]), Color("#3b3030"))
	draw_colored_polygon(PackedVector2Array([
		Vector2(92, 74), Vector2(242, 357), Vector2(242, 385), Vector2(91, 190),
	]), Color("#2b292b"))
	draw_colored_polygon(PackedVector2Array([
		Vector2(1188, 74), Vector2(1080, 357), Vector2(1080, 385), Vector2(1190, 190),
	]), Color("#30292a"))
	draw_line(Vector2(242, 357), Vector2(1080, 357), Color("#ab9070"), 5.0)

	# Back-wall beams and a window establish a deeper room silhouette.
	draw_line(Vector2(132, 112), Vector2(1145, 112), Color("#69514a"), 8.0)
	draw_line(Vector2(154, 166), Vector2(1125, 166), Color("#574440"), 3.0)
	draw_rect(Rect2(515, 153, 190, 150), Color("#252f34"))
	draw_rect(Rect2(523, 161, 174, 134), Color("#4d6665"))
	draw_line(Vector2(610, 161), Vector2(610, 295), Color("#c2ac85"), 5.0)
	draw_line(Vector2(523, 228), Vector2(697, 228), Color("#c2ac85"), 5.0)
	draw_rect(Rect2(508, 147, 204, 162), Color("#c2ac85"), false, 5.0)

	draw_colored_polygon(PackedVector2Array([
		Vector2(255, 350), Vector2(1040, 350), Vector2(1200, 690), Vector2(82, 690),
	]), Color("#665744"))
	# Perspective floor guides converge toward the rear wall.
	for index in range(1, 10):
		var amount := float(index) / 10.0
		var back_point := Vector2(255, 350).lerp(Vector2(1040, 350), amount)
		var front_point := Vector2(82, 690).lerp(Vector2(1200, 690), amount)
		draw_line(back_point, front_point, Color(0.86, 0.78, 0.63, 0.12), 1.0)
	for index in range(1, 6):
		var amount := float(index) / 6.0
		var left_point := Vector2(255, 350).lerp(Vector2(82, 690), amount)
		var right_point := Vector2(1040, 350).lerp(Vector2(1200, 690), amount)
		draw_line(left_point, right_point, Color(0.86, 0.78, 0.63, 0.14), 1.0)
	draw_polyline(floor_polygon, Color("#b29a72"), 3.0, true)

	# A door is only a visual landmark; it is not interactive in this test.
	draw_colored_polygon(PackedVector2Array([
		Vector2(916, 193), Vector2(1005, 187), Vector2(1005, 348), Vector2(916, 348),
	]), Color("#292426"))
	draw_rect(Rect2(916, 193, 89, 155), Color("#a98e67"), false, 4.0)
	draw_circle(Vector2(987, 280), 4.0, Color("#d4ba84"))

	var depth_items: Array[Dictionary] = []
	for prop in props:
		depth_items.append({"type": "prop", "y": prop["foot"].y, "prop": prop})
	depth_items.append({"type": "player", "y": player_position.y})
	depth_items.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return a["y"] < b["y"])
	for item in depth_items:
		if item["type"] == "player":
			_draw_player()
		else:
			_draw_prop(item["prop"])

	if move_target != NO_TARGET:
		draw_arc(move_target, 14.0, 0.0, TAU, 28, Color("#e7ce96"), 2.0, true)


func _draw_prop(prop: Dictionary) -> void:
	var foot: Vector2 = prop["foot"]
	var highlighted: bool = _nearest_prop().get("name", "") == prop["name"]
	var outline := Color("#f0d394") if highlighted else Color("#9e8970")
	draw_ellipse_placeholder(Vector2(foot.x, foot.y - 2.0), Vector2(74, 15), Color(0.02, 0.03, 0.03, 0.28))

	match prop["kind"]:
		"table":
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x - 62, foot.y - 75), Vector2(foot.x + 62, foot.y - 75),
				Vector2(foot.x + 62, foot.y - 17), Vector2(foot.x - 62, foot.y - 17),
			]), Color("#584033"))
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x - 80, foot.y - 82), Vector2(foot.x, foot.y - 107),
				Vector2(foot.x + 80, foot.y - 82), Vector2(foot.x, foot.y - 56),
			]), Color("#987457"))
			draw_polyline(PackedVector2Array([
				Vector2(foot.x - 80, foot.y - 82), Vector2(foot.x, foot.y - 107),
				Vector2(foot.x + 80, foot.y - 82), Vector2(foot.x, foot.y - 56),
				Vector2(foot.x - 80, foot.y - 82),
			]), outline, 2.0, true)
		"cabinet":
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x - 42, foot.y - 142), Vector2(foot.x + 22, foot.y - 142),
				Vector2(foot.x + 22, foot.y), Vector2(foot.x - 42, foot.y),
			]), Color("#665046"))
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x + 22, foot.y - 142), Vector2(foot.x + 45, foot.y - 155),
				Vector2(foot.x + 45, foot.y - 13), Vector2(foot.x + 22, foot.y),
			]), Color("#493a35"))
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x - 42, foot.y - 142), Vector2(foot.x - 19, foot.y - 157),
				Vector2(foot.x + 45, foot.y - 155), Vector2(foot.x + 22, foot.y - 142),
			]), Color("#8d6d52"))
			draw_rect(Rect2(foot.x - 31, foot.y - 121, 44, 48), Color("#8b6b52"), false, 2.0)
			draw_circle(Vector2(foot.x + 8, foot.y - 99), 3.0, Color("#d1b783"))
		"crate":
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x - 39, foot.y - 55), Vector2(foot.x + 39, foot.y - 55),
				Vector2(foot.x + 39, foot.y), Vector2(foot.x - 39, foot.y),
			]), Color("#72533d"))
			draw_colored_polygon(PackedVector2Array([
				Vector2(foot.x - 39, foot.y - 55), Vector2(foot.x, foot.y - 70),
				Vector2(foot.x + 51, foot.y - 55), Vector2(foot.x + 39, foot.y - 48),
			]), Color("#987253"))
			draw_line(Vector2(foot.x - 23, foot.y - 48), Vector2(foot.x + 23, foot.y - 7), Color("#b18a5e"), 3.0)
			draw_line(Vector2(foot.x + 23, foot.y - 48), Vector2(foot.x - 23, foot.y - 7), Color("#b18a5e"), 3.0)

	if highlighted:
		draw_string(ui_font, Vector2(foot.x - 38, foot.y - 118), "E / 左鍵", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color("#f2d89e"))
	if prop["visits"] > 0:
		draw_circle(Vector2(foot.x + 60, foot.y - 94), 11.0, Color("#83aaa3"))
		draw_string(ui_font, Vector2(foot.x + 56, foot.y - 90), str(prop["visits"]), HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color("#14201e"))


func _draw_player() -> void:
	var depth := clampf(inverse_lerp(350.0, 690.0, player_position.y), 0.0, 1.0)
	var scale_factor := lerpf(0.74, 1.13, depth)
	var p := player_position
	draw_ellipse_placeholder(p + Vector2(0, 1), Vector2(19, 8) * scale_factor, Color(0.02, 0.03, 0.03, 0.36))
	draw_colored_polygon(PackedVector2Array([
		p + Vector2(-13, -33) * scale_factor,
		p + Vector2(13, -33) * scale_factor,
		p + Vector2(20, -8) * scale_factor,
		p + Vector2(0, -2) * scale_factor,
		p + Vector2(-20, -8) * scale_factor,
	]), Color("#769b94"))
	draw_colored_polygon(PackedVector2Array([
		p + Vector2(-9, -36) * scale_factor,
		p + Vector2(0, -48) * scale_factor,
		p + Vector2(10, -36) * scale_factor,
		p + Vector2(8, -27) * scale_factor,
		p + Vector2(-8, -27) * scale_factor,
	]), Color("#d5b69a"))
	draw_line(p + Vector2(-13, -32) * scale_factor, p + Vector2(0, -19) * scale_factor, Color("#d7c9aa"), 2.0)
	draw_line(p + Vector2(13, -32) * scale_factor, p + Vector2(0, -19) * scale_factor, Color("#d7c9aa"), 2.0)
	draw_string(ui_font, p + Vector2(-39, 22) * scale_factor, "洛芙（佔位）", HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color("#f0e8d8"))


func draw_ellipse_placeholder(center: Vector2, radius: Vector2, color: Color) -> void:
	var points := PackedVector2Array()
	for index in range(25):
		var angle := TAU * float(index) / 24.0
		points.append(center + Vector2(cos(angle) * radius.x, sin(angle) * radius.y))
	draw_colored_polygon(points, color)


func _draw_hud() -> void:
	draw_rect(Rect2(14, 14, 1252, 74), Color(0.08, 0.10, 0.12, 0.94))
	draw_rect(Rect2(14, 14, 1252, 74), Color("#59635e"), false, 1.5)
	var title := "奶奶故居｜2.5D 場景探索" if in_room else "異調童話｜城市地圖"
	draw_string(ui_font, Vector2(36, 47), title, HORIZONTAL_ALIGNMENT_LEFT, -1, 22, Color("#f0e8d8"))
	draw_string(ui_font, Vector2(36, 72), "Godot 4 灰盒・無劇情操作測試", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color("#aeb9b4"))
	draw_string(ui_font, Vector2(1080, 58), "2.5D 視角草案", HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color("#dfc38f"))

	draw_rect(Rect2(14, 680, 1252, 106), Color(0.08, 0.10, 0.12, 0.96))
	draw_rect(Rect2(14, 680, 1252, 106), Color("#59635e"), false, 1.5)
	if in_room:
		var nearby := _nearest_prop()
		var prompt := "附近：%s　（E 或左鍵互動）" % nearby["name"] if not nearby.is_empty() else "附近沒有可調查物件"
		draw_string(ui_font, Vector2(34, 715), prompt, HORIZONTAL_ALIGNMENT_LEFT, 760, 16, Color("#e3d2a9"))
		draw_string(ui_font, Vector2(34, 750), status_message, HORIZONTAL_ALIGNMENT_LEFT, 790, 14, Color("#c2cbc5"))
		_draw_button(RESET_BUTTON, "重設位置")
		_draw_button(MAP_BUTTON, "回到城市地圖")
		draw_string(ui_font, Vector2(34, 774), "WASD／方向鍵移動・點擊地板前往・點物件直接互動", HORIZONTAL_ALIGNMENT_LEFT, 790, 12, Color("#929d98"))
	else:
		draw_string(ui_font, Vector2(34, 728), status_message, HORIZONTAL_ALIGNMENT_LEFT, 900, 15, Color("#d2c6a6"))
		draw_string(ui_font, Vector2(34, 760), "點選地圖上的奶奶故居，進入可操作的 2.5D 測試室。", HORIZONTAL_ALIGNMENT_LEFT, 900, 13, Color("#aeb9b4"))


func _draw_button(rect: Rect2, label: String) -> void:
	draw_rect(rect, Color("#263330"))
	draw_rect(rect, Color("#8d8067"), false, 1.5)
	draw_string(ui_font, rect.position + Vector2(14, 30), label, HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 20, 14, Color("#eee4d2"))
