extends GutTest

const Session = preload("res://scripts/DaySession.gd")
const Store = preload("res://scripts/SaveStore.gd")
const Codec = preload("res://scripts/SaveCodec.gd")
var store
var session
var test_directory: String

func before_each() -> void:
	test_directory = "user://save_tests/" + str(Time.get_ticks_usec())
	store = Store.new(test_directory)
	session = Session.new()

func breakfast(hints: bool = false):
	var meal = Session.Breakfast.new()
	meal.start()
	if hints:
		for code in ["LR", "DUL"]:
			for direction in code:
				meal.enter_direction(direction)
			while meal.phase == Session.Breakfast.Phase.DIALOGUE:
				meal.next_line()
			meal.tick(2)
		meal.toggle_extra("茄子")
	else:
		for index in range(2):
			meal.tick(11)
			meal.tick(2)
	meal.confirm_shopping()
	return meal

func work():
	var drink = Session.Drink.new()
	drink.start()
	for index in range(4):
		for ingredient in Session.Drink.RECIPES[drink.current_order()]:
			drink.add(ingredient)
		drink.serve()
		drink.next_order()
	return drink

func flow_with_store():
	var flow = load("res://Main.tscn").instantiate()
	flow.saves = store
	return add_child_autofree(flow)

func envelope(data: Dictionary) -> Dictionary:
	return {"schema": 1, "game": Codec.GAME_ID, "relationship_rules": Session.Rules.VERSION,
		"exposure_rules": Session.Exposure.VERSION, "saved_at": "2026-11-23T12:00:00", "run": data}

func raw_write(path: String, contents: String) -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(test_directory))
	var file = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(contents)
	file.close()

func test_no_save_title_never_overwrites_or_autostarts() -> void:
	var flow = flow_with_store()
	assert_true(flow.at_title)
	assert_null(flow.active_view)
	assert_false(FileAccess.file_exists(store.path_for("auto")))
	assert_false(flow.slot_data.auto.ok)
	flow.request_new_game()
	assert_false(flow.at_title)
	assert_true(store.load_slot("auto").ok)
	assert_eq(flow.active_view.game.phase, Session.Breakfast.Phase.READY)

func test_four_safe_phase_roundtrips_keep_exact_plain_data() -> void:
	for phase in [Session.Phase.BREAKFAST, Session.Phase.DEPARTURE, Session.Phase.EVENING, Session.Phase.SUMMARY]:
		if phase == Session.Phase.DEPARTURE:
			session.accept_breakfast(breakfast(true))
		elif phase == Session.Phase.EVENING:
			session.begin_visit("tsuru", "quest")
			session.finish_visit()
		elif phase == Session.Phase.SUMMARY:
			session.choose_work()
			session.finish_work(work())
		var expected = session.to_snapshot()
		var result = store.save_slot("manual", session)
		assert_true(result.ok, result.get("error", ""))
		var loaded = store.load_slot("manual")
		assert_true(loaded.ok, loaded.get("error", ""))
		var restored = store.restored_session(loaded)
		assert_eq_deep(restored.to_snapshot(), expected)
		assert_eq(typeof(restored.relationships.ves), TYPE_INT)

func test_manual_departure_does_not_charge_breakfast_again() -> void:
	session.accept_breakfast(breakfast(true))
	assert_true(store.save_slot("manual", session).ok)
	var resumed = store.restored_session(store.load_slot("manual"))
	assert_eq(resumed.money, 85)
	assert_false(resumed.accept_breakfast(breakfast(true)))
	assert_eq(resumed.money, 85)
	assert_eq(resumed.extras, ["茄子"])
	assert_true(resumed.eggplant_known)
	assert_true(resumed.communicator_known)

func test_summary_load_does_not_repeat_pay_quest_or_overnight() -> void:
	session.accept_breakfast(breakfast())
	session.begin_visit("tsuru", "quest")
	session.finish_visit()
	session.choose_work()
	session.finish_work(work())
	var saved = session.to_snapshot()
	assert_true(store.save_slot("manual", session).ok)
	for index in range(2):
		var resumed = store.restored_session(store.load_slot("manual"))
		assert_eq_deep(resumed.to_snapshot(), saved)
		assert_false(resumed.finish_work(work()))
		assert_false(resumed.finish_visit())
		assert_eq(resumed.money, 130)
		assert_eq(resumed.relationships.tsuru, 53)
		assert_eq(resumed.exposures.tsuru, 0)
		assert_true(resumed.next_day())
		assert_false(resumed.next_day())
		assert_eq(resumed.exposures.tsuru, 6)
		assert_eq(resumed.day_history.size(), 1)

func test_autosave_at_next_breakfast_and_loading_never_saves_again() -> void:
	var flow = flow_with_store()
	flow.request_new_game()
	flow.active_view.game = breakfast()
	flow.transfer_breakfast(flow.generation)
	flow.rest_afternoon()
	flow.choose_home()
	flow.continue_home()
	flow.continue_home()
	flow.save_manual()
	assert_eq(store.load_slot("manual").snapshot.phase, Session.Phase.SUMMARY)
	flow.next_day()
	var auto_before = FileAccess.get_file_as_string(store.path_for("auto"))
	assert_eq(store.load_slot("auto").snapshot.day_number, 2)
	assert_eq(store.load_slot("auto").snapshot.exposures.ves, 16)
	assert_eq(store.load_slot("manual").snapshot.day_number, 1)
	var generation: int = flow.generation
	flow.load_saved_slot("manual")
	assert_eq(flow.session.day_number, 1)
	assert_eq(flow.session.phase, Session.Phase.SUMMARY)
	assert_eq(flow.session.exposures.ves, 10)
	assert_eq(FileAccess.get_file_as_string(store.path_for("auto")), auto_before)
	flow.transfer_work(generation)
	assert_eq(flow.session.money, 90)

func test_safe_guard_rejects_qte_exploration_work_and_pending_transitions() -> void:
	var flow = flow_with_store()
	flow.request_new_game()
	assert_true(flow.safe_to_save())
	flow.active_view.game.start()
	assert_false(flow.safe_to_save())
	flow.save_manual()
	assert_false(FileAccess.file_exists(store.path_for("manual")))
	flow.active_view.game = breakfast()
	flow.transfer_breakfast(flow.generation)
	assert_true(flow.safe_to_save())
	flow.depart()
	assert_false(flow.safe_to_save())
	assert_false(store.save_slot("manual", flow.session).ok)
	flow.active_view.game.evidence = true
	flow.confirm_return()
	flow.choose_work()
	assert_false(flow.safe_to_save())
	assert_false(store.save_slot("manual", flow.session).ok)

func test_unknown_versions_invalid_types_and_ids_fail_without_live_changes() -> void:
	var good = envelope(session.to_snapshot())
	var unchanged = session.to_snapshot()
	var changes := [
		["schema", 999], ["game", "other-game"], ["relationship_rules", "future"]
	]
	for change in changes:
		var invalid = good.duplicate(true)
		invalid[change[0]] = change[1]
		assert_false(Codec.validate(invalid).ok)
	for change in [["day_number", 1.5], ["money", -1], ["worked", "false"], ["phase", 2], ["completed_quests", ["unknown"]], ["cleared_routes", ["mori"]]]:
		var invalid = good.duplicate(true)
		invalid.run[change[0]] = change[1]
		assert_false(Codec.validate(invalid).ok)
	var missing = good.duplicate(true)
	missing.run.erase("lost_sites")
	assert_false(Codec.validate(missing).ok)
	var wrong_map = good.duplicate(true)
	wrong_map.run.exposures.ves = 100
	assert_false(Codec.validate(wrong_map).ok, "不可遺漏失去據點狀態")
	assert_eq_deep(session.to_snapshot(), unchanged)

func test_corrupt_file_recovers_known_good_backup_and_keeps_bad_file() -> void:
	assert_true(store.save_slot("auto", session).ok)
	session.add_test_funds() # 資金充足，不應變動。
	assert_true(store.save_slot("auto", session).ok)
	var path: String = store.path_for("auto")
	raw_write(path, "{truncated")
	var loaded = store.load_slot("auto")
	assert_true(loaded.ok)
	assert_true(loaded.recovered)
	assert_eq(loaded.snapshot.money, 100)
	assert_eq(FileAccess.get_file_as_string(path), "{truncated")
	assert_true(store.save_slot("auto", session).ok)
	var dir = DirAccess.open(test_directory)
	var preserved := false
	for name in dir.get_files():
		if name.begins_with("auto.json.rejected_"):
			preserved = true
	assert_true(preserved)

func test_bad_file_without_backup_leaves_running_scene_and_state_untouched() -> void:
	var flow = flow_with_store()
	flow.request_new_game()
	var current_view = flow.active_view
	var before = flow.session.to_snapshot()
	raw_write(store.path_for("manual"), "[]")
	flow.load_saved_slot("manual")
	assert_eq(flow.active_view, current_view)
	assert_eq_deep(flow.session.to_snapshot(), before)
	assert_true(is_instance_valid(flow.storage_notice))
	flow.close_storage_error()
	assert_true(flow.active_view.is_processing())

func test_disk_write_failure_preserves_live_progress_and_old_file() -> void:
	assert_true(store.save_slot("manual", session).ok)
	var previous := FileAccess.get_file_as_string(store.path_for("manual"))
	var blocked := Store.new(store.path_for("manual").path_join("not_a_directory"))
	var result = blocked.save_slot("auto", session)
	assert_false(result.ok)
	assert_eq(session.money, 100)
	assert_eq(FileAccess.get_file_as_string(store.path_for("manual")), previous)

func test_lost_sites_clues_quests_and_daytime_route_survive_new_store() -> void:
	session.change_exposure("sheep", 90, "測試失守")
	session.change_exposure("ves", 50, "測試看守")
	session.accept_breakfast(breakfast())
	session.begin_visit("ves", "route")
	var encounter = Session.Encounter.new()
	for guard in encounter.guards:
		guard.hp = 0
	session.finish_breakthrough(encounter)
	session.finish_visit()
	session.permanent_evidence = true
	session.permanent_communicator = true
	assert_true(store.save_slot("manual", session).ok)
	var independent = Store.new(test_directory)
	var restored = independent.restored_session(independent.load_slot("manual"))
	assert_false(restored.site_open("sheep"))
	assert_false(restored.needs_breakthrough("ves"))
	assert_true(restored.choose_work())
	assert_true(restored.permanent_evidence)
	assert_true(restored.permanent_communicator)

func test_existing_save_title_is_preserved_and_new_game_keeps_manual_slot() -> void:
	session.accept_breakfast(breakfast())
	session.rest_afternoon()
	session.choose_home()
	session.finish_home()
	assert_true(store.save_slot("manual", session).ok)
	session.next_day()
	assert_true(store.save_slot("auto", session).ok)
	var manual_before := FileAccess.get_file_as_string(store.path_for("manual"))
	var flow = flow_with_store()
	assert_true(flow.at_title)
	assert_eq(flow.slot_data.auto.snapshot.day_number, 2)
	assert_eq(store.load_slot("auto").snapshot.day_number, 2)
	flow.request_new_game()
	assert_true(is_instance_valid(flow.restart_dialog))
	flow.cancel_restart()
	assert_true(flow.at_title)
	flow.reset_day()
	assert_eq(store.load_slot("auto").snapshot.day_number, 1)
	assert_eq(FileAccess.get_file_as_string(store.path_for("manual")), manual_before)

func test_save_menu_refresh_and_cancel_load_restore_input() -> void:
	var flow = flow_with_store()
	flow.request_new_game()
	flow.show_save_menu()
	assert_true(is_instance_valid(flow.save_dialog))
	await get_tree().process_frame
	assert_eq(flow.manual_load_button.size, Vector2(220, 48), "對話框不得把每顆自訂按鈕撐成全版")
	assert_ne(flow.manual_load_button.get_parent(), flow.save_dialog)
	assert_false(flow.active_view.is_processing_unhandled_input())
	flow.save_manual()
	assert_false(flow.manual_load_button.disabled)
	assert_string_contains(flow.save_description.text, "手動檔：第 1 天")
	flow.request_load("manual")
	assert_true(is_instance_valid(flow.load_dialog))
	flow.cancel_load()
	assert_true(flow.active_view.is_processing_unhandled_input())
	assert_true(flow.active_view.is_processing())
