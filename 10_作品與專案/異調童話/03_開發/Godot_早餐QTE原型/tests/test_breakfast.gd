extends GutTest

const Model = preload("res://scripts/BreakfastModel.gd")
var game

func before_each() -> void:
	game = Model.new()

func enter(code: String) -> void:
	for direction in code:
		game.enter_direction(direction)

func finish_conversation() -> void:
	while game.phase == Model.Phase.DIALOGUE:
		game.next_line()

func test_waiting_for_start_has_no_countdown() -> void:
	game.tick(200.0)
	assert_eq(game.phase, Model.Phase.READY)
	assert_eq(game.round_number, 0)
	game.start()
	assert_eq(game.round_number, 1)
	assert_eq(game.seconds_left, 10.0)

func test_shared_prefix_waits_for_complete_sequence() -> void:
	game.start()
	enter("U")
	assert_eq(game.phase, Model.Phase.QTE)
	assert_eq(game.input_buffer, "U")
	enter("DLR")
	assert_eq(game.phase, Model.Phase.DIALOGUE)
	assert_eq(game.selected, 0)
	assert_eq(game.history.size(), 0, "資訊要在聊完後記錄")

func test_dialogue_does_not_count_down_or_accept_another_topic() -> void:
	game.start()
	game.tick(3.0)
	enter("LR")
	game.tick(100.0)
	assert_eq(game.phase, Model.Phase.DIALOGUE)
	assert_eq(game.seconds_left, 7.0)
	enter("UDLR")
	assert_eq(game.selected, 2)
	assert_eq(game.input_buffer, "LR")

func test_wrong_input_locks_out_round_and_grants_nothing() -> void:
	game.start()
	enter("D")
	assert_eq(game.phase, Model.Phase.ROUND_RESULT)
	enter("LR")
	assert_eq(game.history.size(), 1)
	assert_false(game.history[0].success)
	assert_false(game.eggplant_known)
	game.tick(1.5)
	assert_eq(game.round_number, 2)
	assert_eq(game.input_buffer, "")
	assert_eq(game.seconds_left, 10.0)

func test_timeout_with_partial_input_fails() -> void:
	game.start()
	enter("UD")
	game.tick(10.1)
	assert_eq(game.phase, Model.Phase.ROUND_RESULT)
	assert_false(game.history[0].success)
	assert_false(game.communicator_known)

func test_two_unanswered_rounds_end_at_shopping() -> void:
	game.start()
	for index in range(2):
		game.tick(10.1)
		game.tick(1.5)
	assert_eq(game.phase, Model.Phase.SHOPPING)
	assert_eq(game.round_number, 2)
	assert_eq(game.history.size(), 2)
	assert_false(game.eggplant_known)
	game.tick(100.0)
	assert_eq(game.round_number, 2)

func test_preference_becomes_shopping_hint_after_dialogue() -> void:
	game.start()
	enter("LR")
	assert_false(game.eggplant_known)
	finish_conversation()
	assert_true(game.eggplant_known)
	game.tick(1.5)
	enter("DUL")
	finish_conversation()
	game.tick(1.5)
	assert_eq(game.phase, Model.Phase.SHOPPING)
	assert_true(game.communicator_known)
	assert_eq(game.history.size(), 2)
	game.toggle_extra("茄子")
	assert_true(game.favorite_remembered())
	game.confirm_shopping()
	assert_eq(game.phase, Model.Phase.DONE)

func test_small_talk_has_no_information_or_preference_reward() -> void:
	game.start()
	enter("UUD")
	finish_conversation()
	assert_false(game.communicator_known)
	assert_false(game.eggplant_known)
	assert_true(game.history[0].success)

func test_shopping_toggles_and_ignores_invalid_or_wrong_phase() -> void:
	game.toggle_extra("茄子")
	assert_true(game.extras.is_empty())
	game.phase = Model.Phase.SHOPPING
	game.toggle_extra("茄子")
	game.toggle_extra("蘋果")
	game.toggle_extra("不存在的物品")
	assert_eq(game.extras.size(), 2)
	assert_false(game.favorite_remembered(), "未聽到喜好時不顯示記住喜好的回饋")
	game.toggle_extra("茄子")
	assert_eq(game.extras.size(), 1)
	game.confirm_shopping()
	game.toggle_extra("茶葉")
	assert_eq(game.extras.size(), 1)

func test_reset_removes_all_session_results() -> void:
	game.start()
	enter("LR")
	finish_conversation()
	game.extras.append("茄子")
	game.reset()
	assert_eq(game.phase, Model.Phase.READY)
	assert_eq(game.round_number, 0)
	assert_false(game.eggplant_known)
	assert_true(game.extras.is_empty())
	assert_true(game.history.is_empty())

func test_round_codes_are_unique_and_prefix_free() -> void:
	game.start()
	for round_index in range(2):
		for first in range(game.topics.size()):
			for second in range(game.topics.size()):
				if first != second:
					assert_false(game.topics[first].code.begins_with(game.topics[second].code))
		game.begin_round()

func test_view_buttons_follow_the_same_qte_and_shopping_rules() -> void:
	var view = add_child_autofree(load("res://Main.tscn").instantiate())
	view.set_process(false)
	view.click(Vector2(900, 560))
	assert_eq(view.game.phase, Model.Phase.QTE)
	view.click(Vector2(1000, 590))
	assert_eq(view.game.input_buffer, "L")
	view.click(Vector2(1130, 590))
	assert_eq(view.game.phase, Model.Phase.DIALOGUE)
	view.click(Vector2(900, 560))
	view.click(Vector2(900, 560))
	assert_true(view.game.eggplant_known)
	view.game.tick(1.5)
	view.game.tick(10.1)
	view.game.tick(1.5)
	assert_eq(view.game.phase, Model.Phase.SHOPPING)
	view.click(Vector2(900, 360))
	assert_true(view.game.extras.has("茄子"))
	view.click(Vector2(900, 560))
	assert_eq(view.game.phase, Model.Phase.DONE)
