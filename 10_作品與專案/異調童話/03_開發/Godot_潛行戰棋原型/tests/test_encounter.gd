extends GutTest

const Model = preload("res://scripts/EncounterModel.gd")
var game

func before_each() -> void:
	game = Model.new()

func test_sight_uses_facing_distance_and_wall() -> void:
	assert_true(game.sees(0, Vector2(15.5, 5.5)))
	assert_false(game.sees(0, Vector2(12.5, 5.5)), "背後不在視野內")
	assert_false(game.sees(0, Vector2(19.7, 5.5)), "超出視距")
	game.guards[0].facing = Vector2.LEFT
	assert_false(game.sees(0, Vector2(7.5, 5.5)), "牆壁阻擋視線")

func test_detection_transitions_once_and_keeps_position() -> void:
	game.player = Vector2(15.5, 5.5)
	assert_true(game.check_detection())
	assert_eq(game.mode, Model.Mode.COMBAT)
	assert_eq(game.player, Vector2(15.5, 5.5))
	game.moves = 2
	assert_false(game.check_detection())
	assert_eq(game.moves, 2, "不可每幀重置戰鬥回合")

func test_back_assassination_is_immediate_and_enemy_no_longer_detects() -> void:
	game.player = Vector2(12.5, 5.5)
	assert_eq(game.assassination_target(), 0)
	assert_true(game.assassinate(true))
	assert_eq(game.guards[0].hp, 0)
	assert_eq(game.mode, Model.Mode.EXPLORE)
	assert_false(game.sees(0, Vector2(15.5, 5.5)))

func test_assassination_requires_stationary_and_close() -> void:
	game.player = Vector2(12.5, 5.5)
	assert_false(game.assassinate(false))
	assert_eq(game.guards[0].hp, 4)
	game.player = Vector2(10.5, 5.5)
	assert_false(game.assassinate(true))
	assert_eq(game.guards[0].hp, 4)

func test_front_or_other_guard_detection_prevents_assassination() -> void:
	game.player = Vector2(14.5, 5.5)
	assert_false(game.assassinate(true))
	assert_eq(game.mode, Model.Mode.COMBAT)
	assert_eq(game.guards[0].hp, 4)
	game.reset()
	game.player = Vector2(12.5, 5.5)
	game.guards[1].pos = Vector2(11, 5.5)
	game.guards[1].facing = Vector2.RIGHT
	assert_false(game.assassinate(true), "不能在其他守衛眼前暗殺")
	assert_eq(game.guards[0].hp, 4)

func test_path_routes_around_wall_and_avoids_occupied_guard() -> void:
	var route = game.path(Vector2(7.5, 5.5), Vector2i(11, 5))
	assert_gt(route.size(), 5, "須繞牆")
	for point in route:
		assert_false(Model.WALL.grow(0.22).has_point(game.center(point)))
	assert_true(game.path(game.player, Vector2i(13, 5)).is_empty())
	assert_true(game.path(game.player, Vector2i(-1, 5)).is_empty())

func test_reachable_respects_budget_and_wall() -> void:
	game.player = Vector2(7.5, 5.5)
	game.moves = 2
	var reachable = game.reachable()
	assert_true(reachable.has(Vector2i(7, 7)))
	assert_false(reachable.has(Vector2i(7, 8)))
	assert_false(reachable.has(Vector2i(8, 5)))

func test_shooting_consumes_action_and_rejects_wall_or_range() -> void:
	game.mode = Model.Mode.COMBAT
	game.player = Vector2(7.5, 5.5)
	assert_false(game.attack(0))
	assert_eq(game.actions, 1)
	game.player = Vector2(12.5, 5.5)
	assert_true(game.attack(0))
	assert_eq(game.guards[0].hp, 2)
	assert_eq(game.actions, 0)
	assert_false(game.attack(0))
	assert_eq(game.guards[0].hp, 2)

func test_victory_restores_exploration() -> void:
	game.mode = Model.Mode.COMBAT
	game.player = Vector2(12.5, 5.5)
	game.guards[0].hp = 2
	game.guards[1].hp = 0
	assert_true(game.attack(0))
	assert_eq(game.mode, Model.Mode.EXPLORE)
	game.player = Model.OBJECTIVE
	game.collect_evidence()
	assert_true(game.evidence)

func test_enemy_hit_defeat_and_reset() -> void:
	game.mode = Model.Mode.COMBAT
	game.player = Vector2(15.5, 5.5)
	game.hp = 1
	game.enemy_action(0)
	assert_eq(game.mode, Model.Mode.DEFEAT)
	assert_eq(game.hp, 0)
	game.reset()
	assert_eq(game.mode, Model.Mode.EXPLORE)
	assert_eq(game.hp, 8)
	assert_eq(game.guards[0].hp, 4)
	assert_false(game.evidence)

func test_enemy_movement_does_not_cross_wall_or_overlap_player() -> void:
	game.mode = Model.Mode.COMBAT
	game.player = Vector2(7.5, 5.5)
	var old_position: Vector2 = game.guards[0].pos
	game.enemy_action(0)
	assert_false(Model.WALL.grow(0.22).has_point(game.guards[0].pos))
	assert_ne(game.cell(game.guards[0].pos), game.cell(game.player))
	assert_lte(old_position.distance_to(game.guards[0].pos), 3.0)

func test_view_input_movement_budget_and_busy_guard() -> void:
	var view = add_child_autofree(load("res://Main.tscn").instantiate())
	view.set_process(false)
	view.game.mode = Model.Mode.COMBAT
	view.game.player = Vector2(3.5, 11.5)
	view.click(view.screen(Vector2(5.5, 11.5)))
	assert_eq(view.game.moves, 3)
	assert_eq(view.walking.size(), 2)
	view.end_turn()
	assert_true(view.game.player_turn, "移動中不能結束回合")
	view.walking.clear()
	view.end_turn()
	assert_false(view.game.player_turn)
	view.reset_game()
	assert_true(view.walking.is_empty())
	assert_eq(view.game.mode, Model.Mode.EXPLORE)

func test_unicode_keyboard_supports_interaction_end_turn_and_reset() -> void:
	var view = add_child_autofree(load("res://Main.tscn").instantiate())
	view.set_process(false)
	view.game.player = Vector2(12.5, 5.5)
	var key := InputEventKey.new()
	key.pressed = true
	key.unicode = 101
	view._unhandled_input(key)
	assert_eq(view.game.guards[0].hp, 0)
	view.game.mode = Model.Mode.COMBAT
	key.unicode = 32
	view._unhandled_input(key)
	assert_false(view.game.player_turn)
	key.unicode = 114
	view._unhandled_input(key)
	assert_eq(view.game.mode, Model.Mode.EXPLORE)
	assert_eq(view.game.guards[0].hp, 4)
