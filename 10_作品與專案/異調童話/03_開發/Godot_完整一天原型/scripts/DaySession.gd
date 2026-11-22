extends RefCounted

enum Phase { BREAKFAST, DEPARTURE, AFTERNOON, EVENING, WORK, HOME, SUMMARY }
const Breakfast = preload("res://stages/breakfast/BreakfastModel.gd")
const Encounter = preload("res://stages/afternoon/EncounterModel.gd")
const Drink = preload("res://stages/work/DrinkModel.gd")
const EXTRA_COST := {"茄子": 5, "蘋果": 4, "茶葉": 3}
const FIXED_COST := 10

var phase := Phase.BREAKFAST
var money := 100
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
var noa_closeness := 0
var ves_closeness := 0
var work_pay := 0
var work_errors := 0
var worked := false
var favorite_lunch := false

func reset() -> void:
	phase = Phase.BREAKFAST
	money = 100
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
	noa_closeness = 0
	ves_closeness = 0
	work_pay = 0
	work_errors = 0
	worked = false
	favorite_lunch = false

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
	phase = Phase.DEPARTURE
	return true

func depart() -> bool:
	if phase != Phase.DEPARTURE:
		return false
	phase = Phase.AFTERNOON
	return true

func finish_afternoon(encounter) -> bool:
	if phase != Phase.AFTERNOON or encounter.mode == Encounter.Mode.COMBAT:
		return false
	evidence_found = encounter.evidence
	communicator_acquired = communicator_known and evidence_found
	detected = encounter.detected
	retreated = encounter.mode == Encounter.Mode.DEFEAT
	louve_hp = encounter.hp
	exposure_increase = maxi(0, 5 + (3 if detected else 0) - (2 if communicator_acquired else 0))
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
	ves_closeness += drink.simulated_relationship_change()
	money += work_pay
	favorite_lunch = eggplant_known and extras.has("茄子")
	if favorite_lunch:
		noa_closeness += 2
	phase = Phase.SUMMARY
	return true

func finish_home() -> bool:
	if phase != Phase.HOME:
		return false
	noa_closeness += 3
	phase = Phase.SUMMARY
	return true
