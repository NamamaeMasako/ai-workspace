extends GutTest

const Model = preload("res://stages/afternoon/EncounterModel.gd")
const View = preload("res://stages/afternoon/Main.gd")
var game

func before_each() -> void:
	game = Model.new()

func test_range_is_ground_distance_with_inclusive_boundary() -> void:
	game.player = Vector2(12.5, 5.5)
	assert_true(game.in_attack_area(Vector2(17.5, 5.5)))
	assert_true(game.in_attack_area(Vector2(15.5, 9.5)), "3-4-5 對角也是射程邊界")
	assert_false(game.in_attack_area(Vector2(17.501, 5.5)))
	assert_false(game.in_attack_area(Vector2(15.501, 9.501)))

func test_wall_and_map_bounds_clip_attack_area() -> void:
	game.player = Vector2(7.5, 5.5)
	assert_false(game.in_attack_area(Vector2(10.5, 5.5)), "射程內但穿牆不能攻擊")
	assert_false(game.in_attack_area(Vector2(8.5, 5.5)), "牆內不能顯示為可射擊")
	assert_true(game.in_attack_area(Vector2(7.5, 10.5)))
	game.player = Vector2(1.5, 1.5)
	assert_false(game.in_attack_area(Vector2(-0.5, 1.5)))
	assert_false(game.in_attack_area(Vector2(1.5, -0.5)))

func test_target_preview_and_real_attack_agree_without_preview_side_effects() -> void:
	game.mode = Model.Mode.COMBAT
	game.player = Vector2(12.5, 5.5)
	var message: String = game.message
	assert_eq(game.attack_status(0), "可攻擊")
	assert_true(game.can_attack(0))
	assert_eq(game.actions, 1)
	assert_eq(game.guards[0].hp, 4)
	assert_eq(game.message, message)
	assert_true(game.attack(0))
	assert_eq(game.actions, 0)
	assert_eq(game.guards[0].hp, 2)
	assert_false(game.can_attack(0))
	assert_eq(game.attack_status(0), "本回合攻擊已用完")
	assert_false(game.attack(0))

func test_unavailable_target_reasons_and_noncombat_queries() -> void:
	game.player = Vector2(12.5, 5.5)
	assert_false(game.can_attack(0))
	game.mode = Model.Mode.COMBAT
	game.player_turn = false
	assert_eq(game.attack_status(0), "敵方回合")
	game.player_turn = true
	game.player = Vector2(7.5, 5.5)
	game.guards[0].pos = Vector2(10.5, 5.5)
	assert_eq(game.attack_status(0), "牆壁遮擋")
	assert_false(game.attack(0))
	assert_eq(game.actions, 1)
	game.guards[0].pos = Vector2(17.5, 5.5)
	assert_eq(game.attack_status(0), "超出射程")
	game.guards[0].hp = 0
	assert_eq(game.attack_status(0), "無有效目標")
	assert_false(game.can_attack(-1))
	assert_false(game.can_attack(100))

func test_projected_area_clips_wall_and_refreshes_after_move() -> void:
	var view = add_child_autofree(View.new())
	view.set_process(false)
	view.game.player = Vector2(7.5, 5.5)
	var polygon: PackedVector2Array = view.attack_area_polygon()
	assert_gt(polygon.size(), 100)
	assert_true(Geometry2D.is_point_in_polygon(view.screen(Vector2(6.5, 5.5)), polygon))
	assert_false(Geometry2D.is_point_in_polygon(view.screen(Vector2(10.5, 5.5)), polygon))
	assert_false(Geometry2D.is_point_in_polygon(view.screen(Vector2(8.5, 5.5)), polygon))
	var all_valid := true
	for vertex in polygon:
		if not view.game.in_attack_area(view.world(vertex)):
			all_valid = false
	assert_true(all_valid, "所有輪廓頂點均符合實際攻擊範圍")
	view.game.player = Vector2(15.5, 5.5)
	var moved: PackedVector2Array = view.attack_area_polygon()
	assert_ne(moved, polygon)
	assert_eq(view.range_origin, Vector2(15.5, 5.5))
	assert_true(Geometry2D.is_point_in_polygon(view.screen(Vector2(16.5, 5.5)), moved))
