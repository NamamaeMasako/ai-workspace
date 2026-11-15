extends SceneTree

func _initialize() -> void:
	call_deferred("run_checks")

func run_checks() -> void:
	var game = load("res://scenes/GrandmaHouse.tscn").instantiate()
	root.add_child(game)
	_check(game.day == 1 and game.period == 0, "初始日期")
	game._handle_left_click(Vector2(700, 470))
	_check(game.noa_plan == "診所打工", "早上可安排打工")
	game._handle_left_click(Vector2(500, 320))
	_check(game.in_room and game.period == 0, "進場不推進")
	game.player_position = Vector2(931, 438)
	game._interact(game.props[1])
	_check(game.clue_found, "調查取得線索")
	game._finish_period(true)
	_check(game.period == 1 and game.money == 120 and game.noa_worked_today, "探索後打工結算")
	_check(game.louve_hunger == 85 and game.noa_hunger == 85, "探索與打工消耗")
	var old_food = game.food
	game._feed(true)
	_check(game.food == old_food - 1 and game.louve_hunger == 100 and game.period == 1, "進食不推進時間")
	game._handle_left_click(Vector2(700, 470))
	_check(game.noa_plan == "休息", "每天只能打工一次")
	game._handle_left_click(Vector2(400, 470))
	game._handle_left_click(Vector2(500, 320))
	game.player_position = Vector2(526, 480)
	game._interact(game.props[0])
	_check(game.joint_clue_found, "同行可取得線索")
	game._finish_period(true)
	_check(game.period == 2, "下午進入晚上")
	game._handle_left_click(Vector2(700, 470))
	_check(game.noa_plan == "休息", "晚上不能診所打工")
	game._finish_period(false)
	_check(game.day == 2 and game.period == 0 and not game.noa_worked_today, "跨日重置打工")
	game._handle_left_click(Vector2(700, 470))
	_check(game.noa_plan == "診所打工", "隔日可再打工")
	game.queue_free()
	print("PASS: core loop")
	quit(0)

func _check(condition: bool, description: String) -> void:
	if not condition:
		push_error("FAILED: " + description)
		quit(1)
		assert(condition, description)
