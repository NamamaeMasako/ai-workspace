extends RefCounted

enum Phase { BREAKFAST, DEPARTURE, AFTERNOON, EVENING, WORK, HOME, SUMMARY, VISIT, BREAKTHROUGH }
const Breakfast = preload("res://stages/breakfast/BreakfastModel.gd")
const Encounter = preload("res://stages/afternoon/EncounterModel.gd")
const Drink = preload("res://stages/work/DrinkModel.gd")
const Rules = preload("res://scripts/RelationshipRules.gd")
const Exposure = preload("res://scripts/ExposureRules.gd")
const EXTRA_COST = Rules.EXTRA_COST
const FIXED_COST = Rules.FIXED_COST

# 本次遊玩狀態的唯一持有者；畫面不直接修改數值。
var phase := Phase.BREAKFAST
var day_number := 1
var money := Rules.START_MONEY
var relationships: Dictionary = {}
var exposures: Dictionary = {}
var lost_sites: Dictionary = {}
var exposure_log: Array[Dictionary] = []
var day_start_exposures: Dictionary = {}
var cleared_routes: Array[String] = []
var exposure_notes: Array[String] = []
var overnight_notes: Array[String] = []
var visit_spent := 0
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
	exposures.clear()
	lost_sites.clear()
	exposure_log.clear()
	overnight_notes.clear()
	for site in Rules.SITES:
		exposures[site] = Exposure.START
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
	day_start_exposures = exposures.duplicate()
	cleared_routes.clear()
	exposure_notes.clear()
	visit_spent = 0
	shopping_cost = 0
	extras.clear()
	communicator_known = false
	eggplant_known = false
	evidence_found = false
	communicator_acquired = false
	detected = false
	retreated = false
	louve_hp = 8
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
	if Rules.SITES.has(id):
		check_site_loss(id)

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
	phase = Phase.EVENING
	return true

func next_quest_index(site: String) -> int:
	for index in range(Rules.QUEST_GAINS.size()):
		if not completed_quests.has("%s_%d" % [site, index]):
			return index
	return -1

func begin_visit(site: String, kind: String) -> bool:
	if phase != Phase.DEPARTURE or not Rules.SITES.has(site) or kind not in ["consume", "quest", "route"]:
		return false
	if not site_open(site):
		return false
	if kind == "route" and not needs_breakthrough(site):
		return false
	if kind == "consume" and (money < Rules.CONSUME_COST or consumed_today.has(site)):
		return false
	if kind == "quest" and next_quest_index(site) < 0:
		return false
	visit_site = site
	visit_kind = kind
	visit_quest = "%s_%d" % [site, next_quest_index(site)] if kind == "quest" else ""
	activity = "%s：%s" % [Rules.SITES[site], {"consume": "店內消費", "quest": "處理追查支線", "route": "清除看守，掩護今晚通行"}[kind]]
	phase = Phase.BREAKTHROUGH if needs_breakthrough(site) else Phase.VISIT
	return true

func finish_visit(fulfilled: bool = true) -> bool:
	if phase != Phase.VISIT or not site_open(visit_site):
		return false
	if visit_kind == "consume":
		if money < Rules.CONSUME_COST or consumed_today.has(visit_site):
			return false
		money -= Rules.CONSUME_COST
		visit_spent = Rules.CONSUME_COST
		consumed_today.append(visit_site)
		change_relationship(visit_site, Rules.CONSUME_GAIN, "店內消費（本日一次）")
		visit_result = "消費 %d，密切度 +%d" % [Rules.CONSUME_COST, Rules.CONSUME_GAIN]
	elif visit_kind == "route":
		visit_result = "看守已清除，該據點今天可通行；不額外加關係或降低暴露度。"
	elif fulfilled:
		var index := next_quest_index(visit_site)
		if index < 0 or visit_quest != "%s_%d" % [visit_site, index]:
			return false
		completed_quests.append(visit_quest)
		var gain: int = Rules.QUEST_GAINS[index]
		change_relationship(visit_site, gain, "佔位%s支線 %d（首次完成）" % ["重要" if index == 2 else "一般", index + 1])
		var reduction: int = Exposure.QUEST_REDUCTIONS[index]
		change_exposure(visit_site, -reduction, "完成%s支線 %d" % ["關鍵" if index == 2 else "一般", index + 1])
		visit_result = "密切度 +%d，暴露度 -%d（最低 0）；每項只能領一次。" % [gain, reduction]
	else:
		change_relationship(visit_site, Rules.BROKEN_PROMISE, "答應協助後失約（佔位測試）")
		visit_result = "放棄已答應的協助，密切度 %d；之後仍可再接。" % Rules.BROKEN_PROMISE
	phase = Phase.EVENING
	return true

func rest_afternoon() -> bool:
	if phase != Phase.DEPARTURE:
		return false
	activity = "洛芙留在安全屋休息；諾亞照常採購"
	phase = Phase.EVENING
	return true

func choose_work() -> bool:
	if phase != Phase.EVENING or not work_block_reason().is_empty():
		return false
	phase = Phase.WORK
	return true

func choose_home() -> bool:
	if phase != Phase.EVENING:
		return false
	phase = Phase.HOME
	return true

func finish_work(drink) -> bool:
	if phase != Phase.WORK or drink.phase != Drink.Phase.DONE or not site_open("ves"):
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
	overnight_notes.clear()
	for site in Rules.SITES:
		if not site_open(site):
			continue
		var old_grade: String = Exposure.grade(exposures[site])
		change_exposure(site, Exposure.DAILY_RISE, "睡前自然上升 +6")
		if lost_sites.has(site):
			overnight_notes.append("%s：%s" % [Rules.SITES[site], lost_sites[site]])
		elif Exposure.grade(exposures[site]) != old_grade:
			overnight_notes.append("%s進入%s（%d）" % [Rules.SITES[site], Exposure.grade(exposures[site]), exposures[site]])
	day_history.append({"day": day_number, "money": money, "relationships": relationships.duplicate(),
		"exposures": exposures.duplicate(), "lost_sites": lost_sites.duplicate(), "activity": activity})
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

func check_site_loss(site: String) -> void:
	if not exposures.has(site) or lost_sites.has(site):
		return
	var reason: String = Exposure.closure_reason(exposures[site], relationships[site])
	if not reason.is_empty():
		lost_sites[site] = reason
		exposure_notes.append("%s：%s" % [Rules.SITES[site], reason])

func site_open(site: String) -> bool:
	return exposures.has(site) and not lost_sites.has(site) and Exposure.closure_reason(exposures[site], relationships[site]).is_empty()

func change_exposure(site: String, amount: int, reason: String) -> bool:
	if not exposures.has(site) or lost_sites.has(site):
		return false
	var before: int = exposures[site]
	var after := clampi(before + amount, 0, 100)
	exposures[site] = after
	exposure_log.append({"day": day_number, "id": site, "before": before, "after": after,
		"delta": after - before, "requested": amount, "reason": reason})
	check_site_loss(site)
	return true

func exposure_delta(site: String) -> int:
	return int(exposures[site]) - int(day_start_exposures[site])

func projected_exposure(site: String) -> int:
	return mini(100, int(exposures[site]) + Exposure.DAILY_RISE) if site_open(site) else int(exposures[site])

func site_status(site: String) -> String:
	if not site_open(site):
		return "已失去據點"
	return Exposure.grade(exposures[site]) + ("・今天已突破" if cleared_routes.has(site) and exposures[site] >= Exposure.DANGER else "")

func needs_breakthrough(site: String) -> bool:
	return site_open(site) and exposures[site] >= Exposure.DANGER and not cleared_routes.has(site)

func work_block_reason() -> String:
	if not site_open("ves"):
		return "酒館已失去，諾亞無法前往打工。"
	if needs_breakthrough("ves"):
		return "酒館處於危險：需洛芙下午先突破看守，今晚才能打工。"
	return ""

func breakthrough_won(encounter) -> bool:
	if encounter.mode == Encounter.Mode.COMBAT or encounter.mode == Encounter.Mode.DEFEAT:
		return false
	for guard in encounter.guards:
		if guard.hp > 0:
			return false
	return true

func finish_breakthrough(encounter) -> bool:
	if phase != Phase.BREAKTHROUGH or not site_open(visit_site) or not breakthrough_won(encounter):
		return false
	cleared_routes.append(visit_site)
	louve_hp = encounter.hp
	phase = Phase.VISIT
	return true

func abandon_breakthrough() -> bool:
	if phase != Phase.BREAKTHROUGH:
		return false
	# 未能進入據點，不算承諾後失約；耗掉本次下午，沒有支線／消費獎勵。
	activity += "（未突破，撤退）"
	visit_result = "沒有進入據點，未收取費用、未領取獎勵；額外戰敗暴露數值尚未設定。"
	phase = Phase.EVENING
	return true

# 存檔只包含可重建流程的純資料，不包含畫面、Node 或回呼。
const SAFE_PHASES := [Phase.BREAKFAST, Phase.DEPARTURE, Phase.EVENING, Phase.SUMMARY]
const SNAPSHOT_FIELDS := [
	"phase", "day_number", "money", "relationships", "exposures", "lost_sites", "exposure_log",
	"day_start_exposures", "cleared_routes", "exposure_notes", "overnight_notes", "visit_spent",
	"completed_quests", "permanent_evidence", "permanent_communicator", "relationship_log", "day_history",
	"day_start_money", "day_start_relationships", "shopping_cost", "extras", "communicator_known",
	"eggplant_known", "evidence_found", "communicator_acquired", "detected", "retreated", "louve_hp",
	"work_pay", "work_errors", "worked", "favorite_lunch", "activity", "visit_site", "visit_kind",
	"visit_quest", "visit_result", "consumed_today", "day_notes", "debug_funds"
]

func to_snapshot() -> Dictionary:
	var snapshot := {}
	for field in SNAPSHOT_FIELDS:
		var value = get(field)
		snapshot[field] = value.duplicate(true) if value is Array or value is Dictionary else value
	return snapshot

func restore_validated(snapshot: Dictionary) -> void:
	# 只由 SaveCodec 完整驗證後的新 Session 使用；不呼叫結算／獎勵方法。
	for field in SNAPSHOT_FIELDS:
		var value = snapshot[field]
		if get(field) is Array:
			get(field).assign(value.duplicate(true))
		else:
			set(field, value.duplicate(true) if value is Dictionary else value)
