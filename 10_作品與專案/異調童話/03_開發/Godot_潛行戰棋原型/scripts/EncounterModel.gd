extends RefCounted

# All combat values are prototype values. One encounter owns all mutable state.
enum Mode { EXPLORE, COMBAT, DEFEAT }
const SIZE := Vector2i(20, 14)
const WALL := Rect2(8, 3, 2, 7)
const SIGHT_RANGE := 6.0
const SIGHT_COS := 0.70710678
const KILL_RANGE := 1.25
const MOVE_BUDGET := 5
const ATTACK_RANGE := 5.0
const OBJECTIVE := Vector2(18.5, 2.5)

var mode := Mode.EXPLORE
var player := Vector2(3.5, 11.5)
var hp := 8
var guards: Array[Dictionary] = []
var turn := 1
var player_turn := true
var moves := MOVE_BUDGET
var actions := 1
var evidence := false
var message := "繞到守衛背後，停下後按 E 暗殺；或走進視野測試戰鬥。"
var astar := AStarGrid2D.new()

func _init() -> void:
	reset()

func reset() -> void:
	mode = Mode.EXPLORE
	player = Vector2(3.5, 11.5)
	hp = 8
	guards = [
		{"name": "守衛 A", "pos": Vector2(13.5, 5.5), "facing": Vector2.RIGHT, "hp": 4},
		{"name": "守衛 B", "pos": Vector2(16.5, 10.5), "facing": Vector2.DOWN, "hp": 4},
	]
	turn = 1
	player_turn = true
	moves = MOVE_BUDGET
	actions = 1
	evidence = false
	message = "繞到守衛背後，停下後按 E 暗殺；或走進視野測試戰鬥。"
	astar.region = Rect2i(Vector2i.ZERO, SIZE)
	astar.cell_size = Vector2.ONE
	astar.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
	astar.default_compute_heuristic = AStarGrid2D.HEURISTIC_MANHATTAN
	astar.default_estimate_heuristic = AStarGrid2D.HEURISTIC_MANHATTAN
	astar.update()

func cell(point: Vector2) -> Vector2i:
	return Vector2i(floori(point.x), floori(point.y))

func center(point: Vector2i) -> Vector2:
	return Vector2(point) + Vector2(0.5, 0.5)

func can_stand(point: Vector2, ignore_guard: int = -1) -> bool:
	if point.x < 0.25 or point.y < 0.25 or point.x > 19.75 or point.y > 13.75:
		return false
	if WALL.grow(0.22).has_point(point):
		return false
	for index in range(guards.size()):
		if index != ignore_guard and guards[index].hp > 0 and point.distance_to(guards[index].pos) < 0.52:
			return false
	return true

func line_clear(from: Vector2, to: Vector2) -> bool:
	if WALL.has_point(from) or WALL.has_point(to):
		return false
	var corners := [WALL.position, WALL.position + Vector2(WALL.size.x, 0), WALL.end, WALL.position + Vector2(0, WALL.size.y)]
	for index in range(4):
		if Geometry2D.segment_intersects_segment(from, to, corners[index], corners[(index + 1) % 4]) != null:
			return false
	return true

func sees(index: int, point: Vector2) -> bool:
	var guard: Dictionary = guards[index]
	if guard.hp <= 0:
		return false
	var offset: Vector2 = point - guard.pos
	return offset.length() <= SIGHT_RANGE and (offset.length() < 0.01 or offset.normalized().dot(guard.facing) >= SIGHT_COS) and line_clear(guard.pos, point)

func check_detection() -> bool:
	if mode != Mode.EXPLORE:
		return false
	for index in range(guards.size()):
		if sees(index, player):
			mode = Mode.COMBAT
			player_turn = true
			moves = MOVE_BUDGET
			actions = 1
			message = "%s 發現洛芙！進入戰鬥，洛芙先行。" % guards[index].name
			return true
	return false

func assassination_target() -> int:
	if mode != Mode.EXPLORE:
		return -1
	for index in range(guards.size()):
		var guard: Dictionary = guards[index]
		var offset: Vector2 = player - guard.pos
		if guard.hp > 0 and offset.length() <= KILL_RANGE and offset.length() > 0.01 and offset.normalized().dot(guard.facing) < -0.55 and line_clear(player, guard.pos):
			return index
	return -1

func assassinate(stationary: bool) -> bool:
	if mode != Mode.EXPLORE:
		return false
	if check_detection():
		return false
	if not stationary:
		message = "先停下，再按 E 執行暗殺。"
		return false
	var target := assassination_target()
	if target < 0:
		message = "需要靠近未警戒守衛的背後；綠色提示出現後按 E。"
		return false
	guards[target].hp = 0
	message = "已暗殺%s。其他存活守衛仍會發現洛芙。" % guards[target].name
	check_detection()
	return true

func path(from: Vector2, destination: Vector2i, moving_guard: int = -1) -> Array[Vector2i]:
	if not Rect2i(Vector2i.ZERO, SIZE).has_point(destination):
		return []
	for x in range(SIZE.x):
		for y in range(SIZE.y):
			var point := Vector2i(x, y)
			var blocked := WALL.grow(0.22).has_point(center(point))
			for index in range(guards.size()):
				if index != moving_guard and guards[index].hp > 0 and cell(guards[index].pos) == point:
					blocked = true
			if moving_guard >= 0 and cell(player) == point:
				blocked = true
			astar.set_point_solid(point, blocked)
	astar.set_point_solid(cell(from), false)
	if astar.is_point_solid(destination):
		return []
	return astar.get_id_path(cell(from), destination)

func reachable() -> Dictionary:
	var found := {cell(player): 0}
	var queue: Array[Vector2i] = [cell(player)]
	while not queue.is_empty():
		var current: Vector2i = queue.pop_front()
		if found[current] >= moves:
			continue
		for direction in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var next: Vector2i = current + direction
			if not found.has(next) and can_stand(center(next)):
				found[next] = found[current] + 1
				queue.append(next)
	return found

func in_attack_area(point: Vector2) -> bool:
	# 顯示區域與實際射擊共用此判定，不額外計算第二套射程。
	return Rect2(Vector2.ZERO, Vector2(SIZE)).has_point(point) and player.distance_to(point) <= ATTACK_RANGE and line_clear(player, point)

func attack_status(target: int) -> String:
	# 純查詢：游標預覽不消耗攻擊次數，也不覆寫戰鬥訊息。
	if target < 0 or target >= guards.size() or guards[target].hp <= 0:
		return "無有效目標"
	if mode != Mode.COMBAT:
		return "尚未進入戰鬥"
	if not player_turn:
		return "敵方回合"
	if actions <= 0:
		return "本回合攻擊已用完"
	if player.distance_to(guards[target].pos) > ATTACK_RANGE:
		return "超出射程"
	if not line_clear(player, guards[target].pos):
		return "牆壁遮擋"
	return "可攻擊" if in_attack_area(guards[target].pos) else "超出場景"

func can_attack(target: int) -> bool:
	return attack_status(target) == "可攻擊"

func attack(target: int) -> bool:
	if mode != Mode.COMBAT or not player_turn or actions <= 0:
		message = "本回合沒有攻擊次數，按空白鍵結束回合。"
		return false
	if target < 0 or target >= guards.size() or guards[target].hp <= 0:
		return false
	if not in_attack_area(guards[target].pos):
		message = "目標超出射程或被牆擋住；先移動到可攻擊位置。"
		return false
	actions -= 1
	guards[target].hp = maxi(0, guards[target].hp - 2)
	message = "命中%s，造成 2 傷害。可繼續移動或按空白鍵結束回合。" % guards[target].name
	finish_if_clear()
	return true

func finish_if_clear() -> bool:
	for guard in guards:
		if guard.hp > 0:
			return false
	mode = Mode.EXPLORE
	message = "敵人已全部解決，恢復自由探索。可去右上角取得測試文件。"
	return true

func enemy_action(index: int) -> void:
	if mode != Mode.COMBAT or guards[index].hp <= 0:
		return
	var guard: Dictionary = guards[index]
	guard.facing = (player - guard.pos).normalized()
	# Select a reachable firing position; each enemy may move at most 3 cells.
	if player.distance_to(guard.pos) > 4.0 or not line_clear(guard.pos, player):
		var best_path: Array[Vector2i] = []
		var best_score := INF
		for x in range(SIZE.x):
			for y in range(SIZE.y):
				var candidate := Vector2i(x, y)
				var distance := center(candidate).distance_to(player)
				if distance < 0.8 or distance > 4.0 or not line_clear(center(candidate), player):
					continue
				var route := path(guard.pos, candidate, index)
				if not route.is_empty() and route.size() < best_score:
					best_score = route.size()
					best_path = route
		if not best_path.is_empty():
			guard.pos = center(best_path[mini(3, best_path.size() - 1)])
	guard.facing = (player - guard.pos).normalized()
	if player.distance_to(guard.pos) <= 4.0 and line_clear(guard.pos, player):
		hp = maxi(0, hp - 1)
		message = "%s 命中洛芙，造成 1 傷害。" % guard.name
	else:
		message = "%s 移動接近，尚無法射擊。" % guard.name
	if hp <= 0:
		mode = Mode.DEFEAT
		message = "洛芙失去戰鬥能力。按 R 或右上角重新測試。"

func collect_evidence() -> void:
	if mode == Mode.EXPLORE and player.distance_to(OBJECTIVE) < 1.4:
		evidence = true
		message = "取得測試文件！這不是正式劇情；可繼續探索或按 R 重來。"
