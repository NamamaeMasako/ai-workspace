extends GutTest

const Session = preload("res://scripts/DaySession.gd")
var day

func before_each() -> void:
	day = Session.new()

func prepared_breakfast(with_hints: bool):
	var breakfast = Session.Breakfast.new()
	breakfast.start()
	if with_hints:
		for code in ["LR", "DUL"]:
			for direction in code:
				breakfast.enter_direction(direction)
			while breakfast.phase == Session.Breakfast.Phase.DIALOGUE:
				breakfast.next_line()
			breakfast.tick(2)
	else:
		for index in range(2):
			breakfast.tick(11)
			breakfast.tick(2)
	breakfast.toggle_extra("茄子")
	breakfast.confirm_shopping()
	return breakfast

func completed_work():
	var work = Session.Drink.new()
	work.start()
	for index in range(4):
		for ingredient in Session.Drink.RECIPES[work.current_order()]:
			work.add(ingredient)
		work.serve()
		work.next_order()
	return work

func reach_evening(with_hints: bool = true) -> void:
	day.accept_breakfast(prepared_breakfast(with_hints))
	day.depart()
	var encounter = Session.Encounter.new()
	encounter.evidence = true
	day.finish_afternoon(encounter)

func test_breakfast_transfer_is_snapshot_and_only_charged_once() -> void:
	var breakfast = prepared_breakfast(true)
	assert_true(day.accept_breakfast(breakfast))
	assert_eq(day.money, 85)
	assert_true(day.eggplant_known)
	assert_true(day.communicator_known)
	breakfast.extras.clear()
	assert_eq(day.extras, ["茄子"])
	assert_false(day.accept_breakfast(breakfast))
	assert_eq(day.money, 85)

func test_failed_breakfast_still_allows_main_afternoon() -> void:
	assert_true(day.accept_breakfast(prepared_breakfast(false)))
	assert_false(day.communicator_known)
	assert_false(day.eggplant_known)
	assert_true(day.depart())
	assert_eq(day.phase, Session.Phase.AFTERNOON)

func test_information_alone_never_applies_communicator_bonus() -> void:
	day.accept_breakfast(prepared_breakfast(true))
	day.depart()
	var encounter = Session.Encounter.new()
	assert_true(day.finish_afternoon(encounter))
	assert_false(day.communicator_acquired)
	assert_eq(day.exposure_increase, 5)

func test_communicator_requires_hint_and_collected_object() -> void:
	reach_evening(true)
	assert_true(day.communicator_acquired)
	assert_eq(day.exposure_increase, 3)
	day.reset()
	reach_evening(false)
	assert_true(day.evidence_found)
	assert_false(day.communicator_acquired)
	assert_eq(day.exposure_increase, 5)

func test_combat_blocks_exit_and_detection_is_retained_after_victory() -> void:
	day.accept_breakfast(prepared_breakfast(true))
	day.depart()
	var encounter = Session.Encounter.new()
	encounter.player = Vector2(15.5, 5.5)
	encounter.check_detection()
	assert_false(day.finish_afternoon(encounter))
	assert_eq(day.phase, Session.Phase.AFTERNOON)
	for guard in encounter.guards:
		guard.hp = 0
	encounter.finish_if_clear()
	assert_true(day.finish_afternoon(encounter))
	assert_true(day.detected)
	assert_eq(day.exposure_increase, 8)

func test_work_carries_pay_relationship_and_favorite_lunch_once() -> void:
	reach_evening()
	assert_true(day.choose_work())
	assert_true(day.finish_work(completed_work()))
	assert_eq(day.money, 125)
	assert_eq(day.work_pay, 40)
	assert_eq(day.ves_closeness, 3)
	assert_eq(day.noa_closeness, 2)
	assert_true(day.favorite_lunch)
	assert_eq(day.phase, Session.Phase.SUMMARY)
	assert_false(day.finish_work(completed_work()))
	assert_eq(day.money, 125)

func test_home_branch_has_no_pay_or_ves_reward() -> void:
	reach_evening()
	assert_true(day.choose_home())
	assert_true(day.finish_home())
	assert_eq(day.money, 85)
	assert_eq(day.work_pay, 0)
	assert_eq(day.ves_closeness, 0)
	assert_eq(day.noa_closeness, 3)
	assert_false(day.favorite_lunch)
	assert_false(day.finish_home())
	assert_eq(day.noa_closeness, 3)

func test_buying_without_remembering_does_not_create_lunch_flag() -> void:
	reach_evening(false)
	day.choose_work()
	day.finish_work(completed_work())
	assert_false(day.favorite_lunch)
	assert_eq(day.noa_closeness, 0)

func test_reset_restores_all_day_state() -> void:
	reach_evening()
	day.choose_work()
	day.finish_work(completed_work())
	day.reset()
	assert_eq(day.phase, Session.Phase.BREAKFAST)
	assert_eq(day.money, 100)
	assert_true(day.extras.is_empty())
	assert_eq(day.ves_closeness, 0)
	assert_eq(day.noa_closeness, 0)
	assert_false(day.evidence_found)
	assert_false(day.favorite_lunch)

func test_scene_flow_replaces_view_and_preserves_session() -> void:
	var flow = add_child_autofree(load("res://Main.tscn").instantiate())
	flow.set_process(false)
	flow.active_view.set_process(false)
	flow.active_view.game = prepared_breakfast(true)
	var breakfast_view = flow.active_view
	flow.transfer_breakfast(flow.generation)
	assert_eq(flow.session.phase, Session.Phase.DEPARTURE)
	assert_null(flow.active_view)
	await get_tree().process_frame
	assert_false(is_instance_valid(breakfast_view))
	flow.depart()
	flow.active_view.set_process(false)
	flow.active_view.game.evidence = true
	flow.confirm_return()
	assert_eq(flow.session.phase, Session.Phase.EVENING)
	flow.choose_work()
	assert_eq(flow.active_view.game.phase, Session.Drink.Phase.MIXING)
	flow.active_view.game = completed_work()
	flow.transfer_work(flow.generation)
	assert_eq(flow.session.phase, Session.Phase.SUMMARY)
	assert_eq(flow.session.money, 125)
	assert_null(flow.active_view)

func test_return_confirmation_can_cancel_without_advancing_day() -> void:
	var flow = add_child_autofree(load("res://Main.tscn").instantiate())
	flow.set_process(false)
	flow.active_view.game = prepared_breakfast(false)
	flow.transfer_breakfast(flow.generation)
	flow.depart()
	flow.request_return()
	assert_true(is_instance_valid(flow.return_dialog))
	assert_false(flow.active_view.is_processing())
	flow.cancel_return()
	assert_true(flow.active_view.is_processing())
	assert_eq(flow.session.phase, Session.Phase.AFTERNOON)

func test_reset_during_pending_transition_ignores_old_generation() -> void:
	var flow = add_child_autofree(load("res://Main.tscn").instantiate())
	flow.set_process(false)
	var old_generation: int = flow.generation
	flow.reset_day()
	flow.transfer_breakfast(old_generation)
	assert_eq(flow.session.phase, Session.Phase.BREAKFAST)
	assert_eq(flow.session.money, 100)
	assert_true(is_instance_valid(flow.active_view))

func test_home_scene_flow_and_repeated_restart_cleanup() -> void:
	var flow = add_child_autofree(load("res://Main.tscn").instantiate())
	flow.set_process(false)
	flow.active_view.game = prepared_breakfast(false)
	flow.transfer_breakfast(flow.generation)
	flow.depart()
	flow.confirm_return()
	flow.choose_home()
	flow.continue_home()
	assert_eq(flow.session.phase, Session.Phase.HOME)
	flow.continue_home()
	assert_eq(flow.session.phase, Session.Phase.SUMMARY)
	assert_eq(flow.session.work_pay, 0)
	assert_eq(flow.session.noa_closeness, 3)
	for index in range(4):
		flow.reset_day()
	await get_tree().process_frame
	assert_eq(flow.get_child_count(), 2, "只保留 overlay 與目前階段畫面")
	assert_eq(flow.ui.get_child_count(), 3, "舊操作按鈕已釋放")

func test_invalid_or_incomplete_stage_cannot_pay_or_skip() -> void:
	assert_false(day.depart())
	assert_false(day.choose_work())
	assert_false(day.finish_home())
	assert_false(day.accept_breakfast(Session.Breakfast.new()))
	reach_evening()
	day.choose_work()
	assert_false(day.finish_work(Session.Drink.new()))
	assert_eq(day.money, 85)
	assert_eq(day.work_pay, 0)
