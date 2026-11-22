extends SceneTree
## 兩個獨立 Godot 程序的磁碟還原驗證。僅允許隔離測試目錄。
const Session = preload("res://scripts/DaySession.gd")
const Store = preload("res://scripts/SaveStore.gd")

func _initialize() -> void:
	call_deferred("probe")

func meal(hints: bool):
	var breakfast = Session.Breakfast.new()
	breakfast.start()
	if hints:
		for code in ["LR", "DUL"]:
			for direction in code:
				breakfast.enter_direction(direction)
			while breakfast.phase == Session.Breakfast.Phase.DIALOGUE:
				breakfast.next_line()
			breakfast.tick(2)
		breakfast.toggle_extra("茄子")
	else:
		for index in range(2):
			breakfast.tick(11)
			breakfast.tick(2)
	breakfast.confirm_shopping()
	return breakfast

func probe() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 2 or args[0] not in ["write", "read"] or not args[1].begins_with("user://save_tests/"):
		print("Usage: -- write|read user://save_tests/<unique-directory>")
		quit(2)
		return
	var store := Store.new(args[1])
	if args[0] == "write":
		var session := Session.new()
		session.accept_breakfast(meal(false))
		session.begin_visit("tsuru", "quest")
		session.finish_visit()
		session.choose_work()
		var drink := Session.Drink.new()
		drink.start()
		for index in range(4):
			for ingredient in Session.Drink.RECIPES[drink.current_order()]:
				drink.add(ingredient)
			drink.serve()
			drink.next_order()
		session.finish_work(drink)
		session.next_day()
		session.accept_breakfast(meal(true))
		session.depart()
		var encounter := Session.Encounter.new()
		encounter.evidence = true
		session.finish_afternoon(encounter)
		session.choose_home()
		session.finish_home()
		if not store.save_slot("manual", session).ok:
			quit(3)
			return
		session.next_day()
		if not store.save_slot("auto", session).ok:
			quit(4)
			return
	var loaded := store.load_slot("auto")
	if not loaded.ok:
		print(loaded)
		quit(5)
		return
	var resumed = store.restored_session(loaded)
	var manual := store.load_slot("manual")
	var ok: bool = resumed.day_number == 3 and resumed.money == 115 and resumed.exposures.ves == 22 and resumed.exposures.tsuru == 12 and resumed.noa_closeness == 29 and resumed.relationships.tsuru == 53 and resumed.completed_quests == ["tsuru_0"] and resumed.permanent_evidence and resumed.permanent_communicator and not resumed.next_day() and manual.ok and manual.snapshot.day_number == 2 and manual.snapshot.phase == Session.Phase.SUMMARY
	print(JSON.stringify({"probe": args[0], "ok": ok, "day": resumed.day_number, "money": resumed.money,
		"ves_exposure": resumed.exposures.ves, "tsuru_exposure": resumed.exposures.tsuru,
		"noa": resumed.noa_closeness, "quest_ids": resumed.completed_quests, "clue": resumed.permanent_communicator}))
	quit(0 if ok else 6)
