extends GutTest

const GameScene = preload("res://scenes/GrandmaHouse.tscn")
var game

func before_each() -> void:
	game = add_child_autofree(GameScene.instantiate())

func test_fresh_run_has_independent_initial_state() -> void:
	assert_eq(game.day, 1)
	assert_eq(game.period, 0)
	assert_eq(game.money, 100)
	assert_false(game.noa_worked_today)
	assert_false(game.clue_found)

func test_entering_and_interacting_do_not_advance_time() -> void:
	game._handle_left_click(Vector2(500, 320))
	assert_true(game.in_room)
	game.player_position = Vector2(931, 438)
	game._interact(game.props[1])
	assert_true(game.clue_found)
	assert_eq(game.period, 0)
	assert_eq(game.louve_hunger, 100)

func test_exploration_and_work_settle_together_on_exit() -> void:
	game._handle_left_click(Vector2(700, 470))
	game._handle_left_click(Vector2(500, 320))
	assert_eq(game.money, 100, "打工收入應在行動結束時結算")
	game._handle_left_click(Vector2(1100, 740))
	assert_false(game.in_room)
	assert_eq(game.period, 1)
	assert_eq(game.money, 120)
	assert_eq(game.louve_hunger, 85)
	assert_eq(game.noa_hunger, 85)

func test_noa_cannot_work_twice_in_one_day() -> void:
	game._handle_left_click(Vector2(700, 470))
	game._finish_period(false)
	game._handle_left_click(Vector2(700, 470))
	assert_eq(game.noa_plan, "休息")
	assert_true(game.noa_worked_today)
	game._finish_period(false)
	assert_eq(game.money, 120, "重複安排不可額外領取工資")

func test_clinic_is_closed_at_night_without_previous_work() -> void:
	game._finish_period(false)
	game._finish_period(false)
	assert_false(game.noa_worked_today)
	game._handle_left_click(Vector2(700, 470))
	assert_eq(game.noa_plan, "休息")
	assert_eq(game.money, 100)

func test_day_rollover_reopens_work() -> void:
	game._handle_left_click(Vector2(700, 470))
	for index in range(3):
		game._finish_period(false)
	assert_eq(game.day, 2)
	assert_eq(game.period, 0)
	assert_false(game.noa_worked_today)
	game._handle_left_click(Vector2(700, 470))
	assert_eq(game.noa_plan, "診所打工")

func test_food_restores_satiety_without_advancing_time() -> void:
	game._finish_period(true)
	game._handle_left_click(Vector2(200, 550))
	assert_eq(game.food, 5)
	assert_eq(game.louve_hunger, 100)
	assert_eq(game.period, 1)

func test_full_satiety_and_empty_stock_do_not_consume_food() -> void:
	game._feed(true)
	assert_eq(game.food, 6)
	game.food = 0
	game.louve_hunger = 10
	game._feed(true)
	assert_eq(game.food, 0)
	assert_eq(game.louve_hunger, 10)

func test_companion_clue_requires_noa_and_proximity() -> void:
	game.player_position = Vector2(526, 480)
	game._interact(game.props[0])
	assert_false(game.joint_clue_found)
	game.noa_plan = "同行"
	game.player_position = Vector2(1000, 600)
	game._interact(game.props[0])
	assert_false(game.joint_clue_found)
	game.player_position = Vector2(526, 480)
	game._interact(game.props[0])
	assert_true(game.joint_clue_found)

func test_satiety_remains_nonnegative_after_many_periods() -> void:
	for index in range(30):
		game._finish_period(true)
	assert_eq(game.louve_hunger, 0)
	assert_eq(game.noa_hunger, 0)
	assert_eq(game.day, 11)
	assert_eq(game.period, 0)
