extends GutTest

const Model = preload("res://scripts/DrinkModel.gd")
var game

func before_each() -> void:
	game = Model.new()

func make_current_order() -> void:
	for ingredient in Model.RECIPES[game.current_order()]:
		game.add(ingredient)

func test_all_recipes_accept_materials_in_any_order() -> void:
	game.start()
	for index in range(4):
		var ingredients: Array = Model.RECIPES[game.current_order()].duplicate()
		ingredients.reverse()
		for ingredient in ingredients:
			game.add(ingredient)
		assert_true(game.matches_order())
		assert_true(game.serve())
		game.next_order()
	assert_eq(game.phase, Model.Phase.DONE)
	assert_eq(game.correct, 4)
	assert_eq(game.wrong, 0)
	assert_eq(Model.RECIPES["珍珠奶茶"], ["tea", "milk", "pearls"])

func test_wrong_delivery_keeps_order_for_retry_and_only_counts_once_per_cup() -> void:
	game.start()
	game.add("milk")
	assert_false(game.serve())
	assert_eq(game.order_index, 0)
	assert_eq(game.phase, Model.Phase.MIXING)
	assert_eq(game.wrong, 1)
	assert_false(game.serve())
	assert_eq(game.wrong, 1)
	assert_eq(game.cup, ["milk"])

func test_discard_clears_cup_without_penalty_or_changing_order() -> void:
	game.start()
	game.add("milk")
	game.discard()
	assert_true(game.cup.is_empty())
	assert_eq(game.wrong, 0)
	assert_eq(game.correct, 0)
	assert_eq(game.order_index, 0)
	assert_eq(game.discarded, 1)
	game.add("tea")
	assert_true(game.serve())

func test_missing_or_extra_ingredients_are_wrong() -> void:
	game.start()
	game.order_index = 1
	game.add("tea")
	assert_false(game.matches_order())
	assert_false(game.serve())
	game.add("milk")
	assert_true(game.serve(), "漏加材料仍可補入")
	game.next_order()
	game.add("tea")
	game.add("pearls")
	game.add("milk")
	assert_false(game.matches_order(), "珍珠紅茶不能含牛奶")

func test_repeated_ingredient_and_unknown_ingredient_do_not_change_recipe() -> void:
	game.start()
	game.add("tea")
	game.add("tea")
	game.add("lemon")
	assert_eq(game.cup, ["tea"])
	assert_true(game.matches_order())

func test_empty_cup_is_not_delivered_or_penalized() -> void:
	game.start()
	assert_false(game.serve())
	game.discard()
	assert_eq(game.wrong, 0)
	assert_eq(game.discarded, 0)
	assert_eq(game.phase, Model.Phase.MIXING)

func test_result_screen_cannot_submit_or_change_drink_twice() -> void:
	game.start()
	game.add("tea")
	assert_true(game.serve())
	game.add("milk")
	game.discard()
	assert_false(game.serve())
	assert_eq(game.correct, 1)
	assert_eq(game.cup, ["tea"])
	game.next_order()
	assert_true(game.cup.is_empty())
	assert_eq(game.current_order(), "奶茶")

func test_rewards_are_only_simulated_and_pay_has_floor() -> void:
	game.correct = 4
	assert_eq(game.simulated_pay(), 40)
	assert_eq(game.simulated_relationship_change(), 3)
	game.wrong = 2
	assert_eq(game.simulated_pay(), 36)
	assert_eq(game.simulated_relationship_change(), 1)
	game.wrong = 99
	assert_eq(game.simulated_pay(), 0)
	assert_eq(game.simulated_relationship_change(), -1)

func test_reset_clears_results_and_done_rejects_changes() -> void:
	game.start()
	for index in range(4):
		make_current_order()
		game.serve()
		game.next_order()
	game.add("milk")
	game.next_order()
	assert_true(game.cup.is_empty())
	assert_eq(game.correct, 4)
	game.reset()
	assert_eq(game.phase, Model.Phase.READY)
	assert_eq(game.order_index, 0)
	assert_eq(game.correct, 0)
	assert_eq(game.wrong, 0)
	assert_eq(game.discarded, 0)

func test_view_buttons_allow_wrong_cup_discard_and_correct_retry() -> void:
	var view = add_child_autofree(load("res://Main.tscn").instantiate())
	view.click(Vector2(1000, 715))
	assert_eq(view.game.phase, Model.Phase.MIXING)
	view.click(Vector2(740, 595))
	view.click(Vector2(1000, 715))
	assert_eq(view.game.wrong, 1)
	view.click(Vector2(460, 715))
	assert_true(view.game.cup.is_empty())
	view.click(Vector2(470, 595))
	view.click(Vector2(1000, 715))
	assert_eq(view.game.phase, Model.Phase.ORDER_RESULT)
	assert_eq(view.game.correct, 1)
	view.click(Vector2(1000, 715))
	assert_eq(view.game.current_order(), "奶茶")

func test_unicode_shortcuts_use_same_model_actions() -> void:
	var view = add_child_autofree(load("res://Main.tscn").instantiate())
	var key := InputEventKey.new()
	key.pressed = true
	key.physical_keycode = KEY_F1
	key.unicode = 13
	view._unhandled_input(key)
	assert_eq(view.game.phase, Model.Phase.MIXING)
	key.unicode = 49
	view._unhandled_input(key)
	assert_eq(view.game.cup, ["tea"])
	key.unicode = 8
	view._unhandled_input(key)
	assert_true(view.game.cup.is_empty())
	key.unicode = 114
	view._unhandled_input(key)
	assert_eq(view.game.phase, Model.Phase.READY)
