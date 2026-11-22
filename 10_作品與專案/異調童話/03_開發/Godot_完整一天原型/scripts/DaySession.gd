extends RefCounted

enum Phase { BREAKFAST, DEPARTURE, AFTERNOON, EVENING, WORK, HOME, SUMMARY, VISIT }
const Breakfast = preload("res://stages/breakfast/BreakfastModel.gd")
const Encounter = preload("res://stages/afternoon/EncounterModel.gd")
const Drink = preload("res://stages/work/DrinkModel.gd")
const Rules = preload("res://scripts/RelationshipRules.gd")
const EXTRA_COST = Rules.EXTRA_COST
const FIXED_COST = Rules.FIXED_COST

# 本次遊玩狀態的唯一持有者；畫面不直接修改數值。
var phase := Phase.BREAKFAST
var day_number := 1
var money := Rules.START_MONEY
var relationships: Dictionary = {}
var completed_quests: Array[String] = []
var permanent_evidence := false
var permanent_communicator := false
var relationship_log: Array[Dictionary] = []
var day_history: Array[Dictionary] = []
var day_start_money := 0
var day_start_relationships: Dictionary = {}
var shopping_cost := 0
var extras: Array[String] = []
var communicator_known := false
var eggplant_known := false
var evidence_found := false
var communicator_acquired := false
var detected := false
var retreated := false
var louve_hp := 8
var exposure_increase := 0
var work_pay := 0
var work_errors := 0
var worked := false
var favorite_lunch := false
var activity := ""
var visit_site := ""
var visit_kind := ""
var visit_quest := ""
var visit_result := ""
var consumed_today: Array[String] = []
var day_notes: Array[String] = []
var debug_funds := 0
var noa_closeness: int:
	get: return relationships.get("noa", Rules.START_NOA)
var ves_closeness: int:
	get: return relationships.get("ves", Rules.START_SITE)

func _init() -> void:
	reset()

func reset() -> void:
	day_number = 1
	money = Rules.START_MONEY
	relationships = {"noa": Rules.START_NOA}
	for site in Rules.SITES:
		relationships[site] = Rules.START_SITE
	completed_quests.clear()
	permanent_evidence = false
	permanent_communicator = false
	relationship_log.clear()
	day_history.clear()
	clear_daily_state()

func clear_daily_state() -> void:
	phase = Phase.BREAKFAST
	day_start_money = money
	day_start_relationships = relationships.duplicate()
	shopping_cost = 0
	extras.clear()
	communicator_known = false
	eggplant_known = false
	evidence_found = false
	communicator_acquired = false
	detected = false
	retreated = false
	louve_hp = 8
	exposure_increase = 0
	work_pay = 0
	work_errors = 0
	worked = false
	favorite_lunch = false
	activity = ""
	visit_site = ""
	visit_kind = ""
	visit_quest = ""
	visit_result = ""
	consumed_today.clear()
	day_notes.clear()
	debug_funds = 0

func change_relationship(id: String, amount: int, reason: String) -> void:
	if not relationships.has(id):
		return
	var before: int = relationships[id]
	var after := clampi(before + amount, 0, 100)
	relationships[id] = after
	relationship_log.append({"day": day_number, "id": id, "before": before, "after": after,
		"delta": after - before, "requested": amount, "reason": reason})

func daily_delta(id: String) -> int:
	return int(relationships.get(id, 0)) - int(day_start_relationships.get(id, 0))

func accept_breakfast(breakfast) -> bool:
	if phase != Phase.BREAKFAST or breakfast.phase != Breakfast.Phase.DONE:
		return false
	var cost := FIXED_COST
	for item in breakfast.extras:
		if not EXTRA_COST.has(item):
			return false
		cost += EXTRA_COST[item]
	if cost > money:
		return false
	extras.assign(breakfast.extras)
	communicator_known = breakfast.communicator_known
	eggplant_known = breakfast.eggplant_known
	shopping_cost = cost
	money -= cost
	if breakfast.emotional_topic:
		change_relationship("noa", Rules.EMOTIONAL_TOPIC_GAIN, "早餐：情感交流")
	phase = Phase.DEPARTURE
	return true

func depart() -> bool:
	if phase != Phase.DEPARTURE:
		return false
	activity = "調查奶奶故居"
	phase = Phase.AFTERNOON
	return true

func finish_afternoon(encounter) -> bool:
	if phase != Phase.AFTERNOON or encounter.mode == Encounter.Mode.COMBAT:
		return false
	evidence_found = encounter.evidence
	communicator_acquired = (communicator_known or permanent_communicator) and evidence_found
	permanent_evidence = permanent_evidence or evidence_found
	permanent_communicator = permanent_communicator or communicator_acquired
	detected = encounter.detected
	retreated = encounter.mode == Encounter.Mode.DEFEAT
	louve_hp = encounter.hp
	exposure_increase = maxi(0, 5 + (3 if detected else 0) - (2 if permanent_communicator else 0))
	phase = Phase.EVENING
	return true

func next_quest_index(site: String) -> int:
	for index in range(Rules.QUEST_GAINS.size()):
		if not completed_quests.has("%s_%d" % [site, index]):
			return index
	return -1

func begin_visit(site: String, kind: String) -> bool:
	if phase != Phase.DEPARTURE or not Rules.SITES.has(site) or kind not in ["consume", "quest"]:
		return false
	if kind == "consume" and (money < Rules.CONSUME_COST or consumed_today.has(site)):
		return false
	if kind == "quest" and next_quest_index(site) < 0:
		return false
	visit_site = site
	visit_kind = kind
	visit_quest = "%s_%d" % [site, next_quest_index(site)] if kind == "quest" else ""
	activity = "%s：%s" % [Rules.SITES[site], "店內消費" if kind == "consume" else "支線協助"]
	phase = Phase.VISIT
	return true

func finish_visit(fulfilled: bool = true) -> bool:
	if phase != Phase.VISIT:
		return false
	if visit_kind == "consume":
		if money < Rules.CONSUME_COST or consumed_today.has(visit_site):
			return false
		money -= Rules.CONSUME_COST
		consumed_today.append(visit_site)
		change_relationship(visit_site, Rules.CONSUME_GAIN, "店內消費（本日一次）")
		visit_result = "消費 %d，密切度 +%d" % [Rules.CONSUME_COST, Rules.CONSUME_GAIN]
	elif fulfilled:
		var index := next_quest_index(visit_site)
		if index < 0 or visit_quest != "%s_%d" % [visit_site, index]:
			return false
		completed_quests.append(visit_quest)
		var gain: int = Rules.QUEST_GAINS[index]
		change_relationship(visit_site, gain, "佔位%s支線 %d（首次完成）" % ["重要" if index == 2 else "一般", index + 1])
		visit_result = "協助完成，密切度 +%d；這項支線不能重複領取。" % gain
	else:
		change_relationship(visit_site, Rules.BROKEN_PROMISE, "答應協助後失約（佔位測試）")
		visit_result = "放棄已答應的協助，密切度 %d；之後仍可再接。" % Rules.BROKEN_PROMISE
	exposure_increase = 3 if permanent_communicator else 5
	phase = Phase.EVENING
	return true

func rest_afternoon() -> bool:
	if phase != Phase.DEPARTURE:
		return false
	activity = "洛芙留在安全屋休息；諾亞照常採購"
	exposure_increase = 3 if permanent_communicator else 5
	phase = Phase.EVENING
	return true

func choose_work() -> bool:
	if phase != Phase.EVENING:
		return false
	phase = Phase.WORK
	return true

func choose_home() -> bool:
	if phase != Phase.EVENING:
		return false
	phase = Phase.HOME
	return true

func finish_work(drink) -> bool:
	if phase != Phase.WORK or drink.phase != Drink.Phase.DONE:
		return false
	worked = true
	work_pay = drink.simulated_pay()
	work_errors = drink.wrong
	change_relationship("ves", Rules.work_gain(work_errors), "酒館打工：送錯 %d 次" % work_errors)
	money += work_pay
	favorite_lunch = eggplant_known and extras.has("茄子")
	if favorite_lunch:
		change_relationship("noa", Rules.FAVORITE_GAIN, "記住喜好並準備茄子便當")
	phase = Phase.SUMMARY
	return true

func finish_home() -> bool:
	if phase != Phase.HOME:
		return false
	change_relationship("noa", Rules.HOME_GAIN, "晚上一起留在安全屋")
	phase = Phase.SUMMARY
	return true

func next_day() -> bool:
	if phase != Phase.SUMMARY:
		return false
	day_history.append({"day": day_number, "money": money, "relationships": relationships.duplicate(), "activity": activity})
	day_number += 1
	clear_daily_state()
	return true

func add_test_funds() -> bool:
	# 防止本輪尚未完成的食物經濟阻塞關係試玩；不是正式收入。
	if phase != Phase.BREAKFAST or money >= FIXED_COST + 12:
		return false
	money += 50
	debug_funds += 50
	day_notes.append("測試補款 +50（非正式收入）")
	return true
