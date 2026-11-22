extends GutTest

const Session = preload("res://scripts/DaySession.gd")
const Exposure = preload("res://scripts/ExposureRules.gd")
var run

func before_each() -> void:
	run = Session.new()

func breakfast():
	var meal = Session.Breakfast.new()
	meal.start()
	for index in range(2):
		meal.tick(11)
		meal.tick(2)
	meal.confirm_shopping()
	return meal

func prepare_afternoon() -> void:
	if run.money < 10:
		run.add_test_funds()
	assert_true(run.accept_breakfast(breakfast()))

func finish_night() -> void:
	assert_true(run.choose_home())
	assert_true(run.finish_home())
	assert_true(run.next_day())

func cleared_encounter():
	var encounter = Session.Encounter.new()
	for guard in encounter.guards:
		guard.hp = 0
	return encounter

func complete_quest(site: String) -> void:
	assert_true(run.begin_visit(site, "quest"))
	if run.phase == Session.Phase.BREAKTHROUGH:
		assert_true(run.finish_breakthrough(cleared_encounter()))
	assert_true(run.finish_visit())

func test_initial_values_and_all_grade_boundaries() -> void:
	assert_eq(run.exposures.size(), 4)
	for site in Session.Rules.SITES:
		assert_eq(run.exposures[site], 10)
		assert_true(run.site_open(site))
	var cases := {0:"平靜",29:"平靜",30:"警戒",59:"警戒",60:"危險",79:"危險",80:"嚴密",99:"嚴密",100:"失守"}
	for value in cases:
		assert_eq(Exposure.grade(value), cases[value])

func test_cross_day_rise_once_and_history_is_snapshot() -> void:
	prepare_afternoon()
	run.rest_afternoon()
	run.choose_home()
	run.finish_home()
	assert_eq(run.exposures.ves, 10)
	assert_eq(run.projected_exposure("ves"), 16)
	assert_true(run.next_day())
	assert_eq(run.exposures.ves, 16)
	assert_eq(run.exposure_log.size(), 4)
	assert_false(run.next_day())
	assert_eq(run.exposures.ves, 16)
	assert_eq(run.day_history[0].exposures.ves, 16)
	run.change_exposure("ves", 4, "額外事件測試")
	assert_eq(run.day_history[0].exposures.ves, 16)
	assert_eq(run.exposure_delta("ves"), 4)

func test_ten_ignored_days_are_70_and_fourteen_days_are_94() -> void:
	for day in range(1, 16):
		prepare_afternoon()
		run.rest_afternoon()
		finish_night()
		if day == 10:
			assert_eq(run.exposures.ves, 70)
		if day == 14:
			assert_eq(run.exposures.ves, 94)
	for site in Session.Rules.SITES:
		assert_eq(run.exposures[site], 100)
		assert_false(run.site_open(site))
	assert_eq(run.lost_sites.size(), 4)
	assert_eq(run.day_number, 16)
	assert_eq(run.day_history[-1].lost_sites.size(), 4)

func test_one_general_quest_on_day_six_results_in_50_after_ten_days() -> void:
	for day in range(1,11):
		prepare_afternoon()
		if day == 6:
			complete_quest("tsuru")
		else:
			run.rest_afternoon()
		finish_night()
	assert_eq(run.exposures.tsuru, 50)
	assert_eq(run.exposures.ves, 70)
	assert_eq(run.relationships.tsuru, 53)

func test_key_quest_reduces_35_and_is_not_repeatable() -> void:
	for index in range(3):
		prepare_afternoon()
		run.change_exposure("tsuru", 90 - int(run.exposures.tsuru), "設置關鍵支線測試環境")
		complete_quest("tsuru")
		assert_eq(run.exposures.tsuru, 70 if index < 2 else 55)
		assert_false(run.finish_visit())
		finish_night()
	assert_eq(run.next_quest_index("tsuru"), -1)
	prepare_afternoon()
	assert_false(run.begin_visit("tsuru", "quest"))
	assert_eq(run.completed_quests.size(), 3)

func test_minimum_records_actual_reduction_and_consumption_does_not_reduce() -> void:
	prepare_afternoon()
	complete_quest("boars")
	assert_eq(run.exposures.boars, 0)
	assert_eq(run.exposure_log[-1].delta, -10)
	assert_eq(run.exposure_log[-1].requested, -20)
	finish_night()
	prepare_afternoon()
	assert_true(run.begin_visit("sheep", "consume"))
	assert_true(run.finish_visit())
	assert_eq(run.exposures.sheep, 16)
	assert_eq(run.visit_spent, 10)

func test_80_allows_friendly_but_closes_at_39_and_never_reopens() -> void:
	run.change_exposure("ves", 70, "提高到80")
	assert_true(run.site_open("ves"))
	assert_true(run.needs_breakthrough("ves"))
	run.change_relationship("ves", -5, "降到友好界線40")
	assert_true(run.site_open("ves"))
	run.change_relationship("ves", -1, "降到39")
	assert_false(run.site_open("ves"))
	assert_true(run.lost_sites.has("ves"))
	assert_false(run.change_exposure("ves", -60, "不得恢復"))
	run.change_relationship("ves", 50, "關係恢復也不重開")
	assert_false(run.site_open("ves"))
	prepare_afternoon()
	assert_false(run.begin_visit("ves", "quest"))
	assert_false(run.begin_visit("ves", "consume"))
	run.rest_afternoon()
	assert_false(run.choose_work())
	assert_true(run.choose_home())

func test_100_closes_even_best_friends_and_reset_reopens() -> void:
	run.change_relationship("sheep", 55, "摯友")
	run.change_exposure("sheep", 1000, "失守測試")
	assert_eq(run.exposures.sheep, 100)
	assert_eq(run.exposure_log[-1].delta, 90)
	assert_false(run.site_open("sheep"))
	run.reset()
	assert_true(run.site_open("sheep"))
	assert_eq(run.exposures.sheep, 10)
	assert_eq(run.exposure_log.size(), 0)
	assert_eq(run.lost_sites.size(), 0)

func test_danger_gate_requires_victory_before_quest_or_spending() -> void:
	run.change_exposure("ves", 50, "達到危險60")
	prepare_afternoon()
	assert_true(run.begin_visit("ves", "quest"))
	assert_eq(run.phase, Session.Phase.BREAKTHROUGH)
	assert_false(run.finish_visit())
	var uncleared = Session.Encounter.new()
	assert_false(run.finish_breakthrough(uncleared))
	var combat = cleared_encounter()
	combat.mode = Session.Encounter.Mode.COMBAT
	assert_false(run.finish_breakthrough(combat))
	combat.mode = Session.Encounter.Mode.EXPLORE
	assert_true(run.finish_breakthrough(combat))
	assert_false(run.finish_breakthrough(combat))
	assert_eq(run.relationships.ves, 45)
	assert_true(run.finish_visit())
	assert_eq(run.exposures.ves, 40)
	assert_eq(run.relationships.ves, 53)
	assert_false(run.finish_visit())

func test_work_requires_daytime_route_and_route_expires_next_day() -> void:
	run.change_exposure("ves", 50, "危險60")
	prepare_afternoon()
	assert_true(run.begin_visit("ves", "route"))
	assert_true(run.finish_breakthrough(cleared_encounter()))
	assert_true(run.finish_visit())
	assert_eq(run.exposures.ves, 60)
	assert_eq(run.relationships.ves, 45)
	assert_eq(run.visit_spent, 0)
	assert_true(run.work_block_reason().is_empty())
	assert_true(run.choose_work())
	var work = Session.Drink.new()
	work.start()
	for index in range(4):
		for ingredient in Session.Drink.RECIPES[work.current_order()]:
			work.add(ingredient)
		work.serve()
		work.next_order()
	assert_true(run.finish_work(work))
	assert_true(run.next_day())
	prepare_afternoon()
	run.rest_afternoon()
	assert_false(run.choose_work())
	assert_string_contains(run.work_block_reason(), "下午先突破")

func test_retreat_does_not_charge_or_reward_or_complete_quest() -> void:
	run.change_exposure("boars", 50, "危險60")
	prepare_afternoon()
	var funds: int = run.money
	assert_true(run.begin_visit("boars", "consume"))
	assert_true(run.abandon_breakthrough())
	assert_eq(run.phase, Session.Phase.EVENING)
	assert_eq(run.money, funds)
	assert_eq(run.visit_spent, 0)
	assert_eq(run.relationships.boars, 45)
	assert_eq(run.exposures.boars, 60)
	assert_eq(run.completed_quests.size(), 0)
	assert_false(run.abandon_breakthrough())

func test_no_unapproved_extra_rise_or_permanent_communicator_discount() -> void:
	prepare_afternoon()
	run.depart()
	var encounter = Session.Encounter.new()
	encounter.evidence = true
	encounter.detected = true
	encounter.mode = Session.Encounter.Mode.DEFEAT
	run.finish_afternoon(encounter)
	assert_eq(run.exposures.ves, 10)
	run.permanent_communicator = true
	finish_night()
	assert_eq(run.exposures.ves, 16)

func test_gate_scene_flow_returns_to_original_action_and_cleans_up() -> void:
	var flow = new_flow()
	flow.set_process(false)
	flow.active_view.set_process(false)
	flow.active_view.game = breakfast()
	flow.transfer_breakfast(flow.generation)
	flow.session.change_exposure("ves", 50, "危險測試")
	flow.begin_visit("ves", "route")
	assert_eq(flow.session.phase, Session.Phase.BREAKTHROUGH)
	flow.active_view.set_process(false)
	assert_eq(flow.active_view.game.mode, Session.Encounter.Mode.COMBAT)
	assert_true(flow.exit_button.disabled)
	for guard in flow.active_view.game.guards:
		guard.hp = 0
	flow.active_view.game.finish_if_clear()
	flow.finish_breakthrough()
	assert_eq(flow.session.phase, Session.Phase.VISIT)
	flow.finish_visit(true)
	flow.choose_work()
	assert_eq(flow.session.phase, Session.Phase.WORK)
	assert_eq(flow.active_view.game.phase, Session.Drink.Phase.MIXING)
	assert_string_contains(flow.report_text(), "暴露")
	await get_tree().process_frame
	assert_eq(flow.get_child_count(), 2)

func new_flow():
	var flow = load("res://Main.tscn").instantiate()
	flow.persistence_enabled = false
	return add_child_autofree(flow)
