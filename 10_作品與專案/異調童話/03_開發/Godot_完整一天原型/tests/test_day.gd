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
	assert_eq(day.exposures.ves, 10, "暴露只在跨日自然上升")

func test_communicator_requires_hint_and_collected_object() -> void:
	reach_evening(true)
	assert_true(day.communicator_acquired)
	assert_eq(day.exposures.ves, 10, "通訊器目前只保留線索，不疊加舊示意數值")
	day.reset()
	reach_evening(false)
	assert_true(day.evidence_found)
	assert_false(day.communicator_acquired)
	assert_eq(day.exposures.ves, 10, "暴露只在跨日自然上升")

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
	assert_eq(day.exposures.ves, 10, "偵測不疊加未核可的暴露增量")

func test_work_carries_pay_relationship_and_favorite_lunch_once() -> void:
	reach_evening()
	assert_true(day.choose_work())
	assert_true(day.finish_work(completed_work()))
	assert_eq(day.money, 125)
	assert_eq(day.work_pay, 40)
	assert_eq(day.ves_closeness, 48)
	assert_eq(day.noa_closeness, 27)
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
	assert_eq(day.ves_closeness, 45)
	assert_eq(day.noa_closeness, 29)
	assert_false(day.favorite_lunch)
	assert_false(day.finish_home())
	assert_eq(day.noa_closeness, 29)

func test_buying_without_remembering_does_not_create_lunch_flag() -> void:
	reach_evening(false)
	day.choose_work()
	day.finish_work(completed_work())
	assert_false(day.favorite_lunch)
	assert_eq(day.noa_closeness, 25)

func test_reset_restores_all_day_state() -> void:
	reach_evening()
	day.choose_work()
	day.finish_work(completed_work())
	day.reset()
	assert_eq(day.phase, Session.Phase.BREAKFAST)
	assert_eq(day.money, 100)
	assert_true(day.extras.is_empty())
	assert_eq(day.ves_closeness, 45)
	assert_eq(day.noa_closeness, 25)
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
	assert_eq(flow.session.noa_closeness, 29)
	for index in range(4):
		flow.reset_day()
	await get_tree().process_frame
	assert_eq(flow.get_child_count(), 2, "只保留 overlay 與目前階段畫面")
	assert_eq(flow.ui.get_child_count(), 4, "舊操作按鈕已釋放")

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

func test_next_day_preserves_run_and_clears_only_daily_fields() -> void:
	reach_evening()
	day.choose_work()
	day.finish_work(completed_work())
	assert_true(day.next_day())
	assert_eq(day.day_number, 2)
	assert_eq(day.phase, Session.Phase.BREAKFAST)
	assert_eq(day.money, 125)
	assert_eq(day.noa_closeness, 27)
	assert_eq(day.ves_closeness, 48)
	assert_true(day.permanent_evidence)
	assert_true(day.permanent_communicator)
	assert_eq(day.day_history.size(), 1)
	assert_false(day.eggplant_known)
	assert_true(day.extras.is_empty())
	assert_eq(day.work_pay, 0)
	assert_eq(day.daily_delta("ves"), 0)
	assert_false(day.next_day(), "同一個結算不能連跳兩天")
	day.change_relationship("ves", 3, "次日測試")
	assert_eq(day.day_history[0].relationships.ves, 48, "歷日快照不可跟著 live dictionary 改變")

func breakfast_without_extras():
	var breakfast = prepared_breakfast(false)
	breakfast.extras.clear()
	return breakfast

func test_ten_home_days_reach_intimate_without_passive_npc_decay() -> void:
	for index in range(10):
		if day.money < 10:
			day.add_test_funds()
		assert_true(day.accept_breakfast(breakfast_without_extras()))
		assert_true(day.rest_afternoon())
		assert_true(day.choose_home())
		assert_true(day.finish_home())
		if index < 9:
			assert_true(day.next_day())
	assert_eq(day.noa_closeness, 65)
	assert_eq(Session.Rules.grade(day.noa_closeness, true), "親密")
	for site in Session.Rules.SITES:
		assert_eq(day.relationships[site], 45)
	assert_eq(day.money, 0)
	assert_eq(day.relationship_log.size(), 10)

func test_ten_good_work_days_with_lunch_have_expected_rate_and_money() -> void:
	for index in range(10):
		assert_true(day.accept_breakfast(prepared_breakfast(true)))
		if day.needs_breakthrough("ves"):
			assert_true(day.begin_visit("ves", "route"))
			var gate = Session.Encounter.new()
			for guard in gate.guards:
				guard.hp = 0
			assert_true(day.finish_breakthrough(gate))
			assert_true(day.finish_visit())
		else:
			day.rest_afternoon()
		day.choose_work()
		day.finish_work(completed_work())
		if index < 9:
			day.next_day()
	assert_eq(day.noa_closeness, 45)
	assert_eq(day.ves_closeness, 75)
	assert_eq(day.money, 350)

func test_grade_boundaries_and_clamping_report_actual_delta() -> void:
	var expected := {0: "疏遠", 19: "疏遠", 20: "普通", 39: "普通", 40: "友好", 59: "友好", 60: "信賴", 79: "信賴", 80: "摯友", 100: "摯友"}
	for value in expected:
		assert_eq(Session.Rules.grade(value), expected[value])
	assert_eq(Session.Rules.grade(59, true), "友好")
	assert_eq(Session.Rules.grade(60, true), "親密")
	day.change_relationship("ves", 200, "上限測試")
	assert_eq(day.ves_closeness, 100)
	assert_eq(day.relationship_log[-1].delta, 55)
	day.change_relationship("ves", -300, "下限測試")
	assert_eq(day.ves_closeness, 0)
	assert_eq(day.relationship_log[-1].delta, -100)
	var count: int = day.relationship_log.size()
	day.change_relationship("mori", 3, "不應存在密切度")
	assert_eq(day.relationship_log.size(), count)

func test_three_unique_quests_and_four_shifts_reach_best_friend() -> void:
	for index in range(4):
		day.accept_breakfast(breakfast_without_extras())
		if index < 3:
			assert_true(day.begin_visit("ves", "quest"))
			assert_true(day.finish_visit())
			assert_false(day.finish_visit(), "不能重複完成同一任務")
		else:
			assert_false(day.begin_visit("ves", "quest"), "沒有無限刷支線")
			day.rest_afternoon()
		day.choose_work()
		day.finish_work(completed_work())
		if index < 3:
			day.next_day()
	assert_eq(day.ves_closeness, 83)
	assert_eq(day.completed_quests.size(), 3)
	assert_eq(day.relationships.tsuru, 45)
	assert_eq(day.relationships.boars, 45)
	assert_eq(day.relationships.sheep, 45)

func test_shared_site_consume_cost_once_and_failure_penalty() -> void:
	day.accept_breakfast(breakfast_without_extras())
	assert_true(day.begin_visit("sheep", "consume"))
	assert_true(day.finish_visit())
	assert_eq(day.money, 80)
	assert_eq(day.relationships.sheep, 46)
	assert_false(day.finish_visit())
	day.choose_home()
	day.finish_home()
	day.next_day()
	day.accept_breakfast(breakfast_without_extras())
	assert_true(day.begin_visit("boars", "quest"))
	assert_true(day.finish_visit(false))
	assert_eq(day.relationships.boars, 41)
	assert_eq(day.next_quest_index("boars"), 0, "失約不標記任務完成")
	assert_eq(day.relationships.size(), 5, "四組據點加諾亞，不拆兄弟姊妹")

func test_emotional_breakfast_gain_once_and_failed_topics_never_penalize() -> void:
	var breakfast = Session.Breakfast.new()
	breakfast.start()
	breakfast.tick(11)
	breakfast.tick(2)
	for direction in "LUD":
		breakfast.enter_direction(direction)
	while breakfast.phase == Session.Breakfast.Phase.DIALOGUE:
		breakfast.next_line()
	breakfast.tick(2)
	breakfast.confirm_shopping()
	assert_true(breakfast.emotional_topic)
	assert_true(day.accept_breakfast(breakfast))
	assert_eq(day.noa_closeness, 26)
	assert_false(day.accept_breakfast(breakfast))
	assert_eq(day.relationship_log.size(), 1)

func test_work_errors_reduce_relationship_but_discard_is_free() -> void:
	assert_eq(Session.Rules.work_gain(0), 3)
	assert_eq(Session.Rules.work_gain(1), 1)
	assert_eq(Session.Rules.work_gain(2), 1)
	assert_eq(Session.Rules.work_gain(3), -1)
	day.accept_breakfast(breakfast_without_extras())
	day.rest_afternoon()
	day.choose_work()
	var work = completed_work()
	work.wrong = 3
	work.discarded = 50
	assert_true(day.finish_work(work))
	assert_eq(day.ves_closeness, 44)
	assert_eq(day.noa_closeness, 25)
	assert_eq(day.work_pay, 34)

func test_insufficient_funds_can_recover_without_replaying_breakfast() -> void:
	var breakfast = Session.Breakfast.new()
	breakfast.phase = Session.Breakfast.Phase.SHOPPING
	breakfast.budget = 0
	breakfast.confirm_shopping()
	assert_eq(breakfast.phase, Session.Breakfast.Phase.SHOPPING)
	assert_false(day.add_test_funds(), "資金充足不能任意補款")
	for index in range(10):
		day.accept_breakfast(breakfast_without_extras())
		day.rest_afternoon()
		day.choose_home()
		day.finish_home()
		day.next_day()
	assert_eq(day.money, 0)
	assert_true(day.add_test_funds())
	assert_eq(day.money, 50)
	assert_eq(day.debug_funds, 50)
	assert_false(day.add_test_funds())
	breakfast.budget = day.money
	breakfast.confirm_shopping()
	assert_true(day.accept_breakfast(breakfast))
	assert_eq(day.money, 40)

func test_modal_pauses_qte_and_restart_cancel_keeps_run() -> void:
	var flow = add_child_autofree(load("res://Main.tscn").instantiate())
	flow.active_view.game.start()
	flow.show_relationships()
	assert_true(is_instance_valid(flow.info_dialog))
	assert_false(flow.active_view.is_processing())
	assert_false(flow.active_view.is_processing_unhandled_input())
	assert_string_contains(flow.report_text(), "薇斯帕：45")
	flow.close_relationships()
	assert_true(flow.active_view.is_processing())
	flow.request_restart()
	assert_true(is_instance_valid(flow.restart_dialog))
	flow.cancel_restart()
	assert_eq(flow.session.day_number, 1)
	assert_eq(flow.active_view.game.phase, Session.Breakfast.Phase.QTE)
	assert_true(flow.active_view.is_processing())

func test_repeated_next_day_scene_changes_release_old_views() -> void:
	var flow = add_child_autofree(load("res://Main.tscn").instantiate())
	flow.set_process(false)
	for index in range(5):
		flow.active_view.set_process(false)
		flow.active_view.game = breakfast_without_extras()
		flow.transfer_breakfast(flow.generation)
		flow.begin_visit("tsuru", "consume")
		flow.finish_visit(true)
		flow.choose_home()
		flow.continue_home()
		flow.continue_home()
		flow.next_day()
		flow.next_day()
		await get_tree().process_frame
		assert_eq(flow.get_child_count(), 2)
	assert_eq(flow.session.day_number, 6)
	assert_eq(flow.session.noa_closeness, 45)
	assert_eq(flow.session.relationships.tsuru, 50)
	assert_eq(flow.session.day_history.size(), 5)
	flow.reset_day()
	assert_eq(flow.session.day_number, 1)
	assert_eq(flow.session.relationship_log.size(), 0)
	assert_eq(flow.session.noa_closeness, 25)
