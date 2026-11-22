extends RefCounted

enum Phase { READY, MIXING, ORDER_RESULT, DONE }
const INGREDIENTS := ["tea", "milk", "pearls"]
const LABELS := {"tea": "紅茶", "milk": "牛奶", "pearls": "珍珠"}
const RECIPES := {
	"紅茶": ["tea"],
	"奶茶": ["tea", "milk"],
	"珍珠紅茶": ["tea", "pearls"],
	"珍珠奶茶": ["tea", "milk", "pearls"],
}
const ORDERS := ["紅茶", "奶茶", "珍珠紅茶", "珍珠奶茶"]
# Prototype reward values only; no global money or relationship data is mutated.
const BASE_PAY := 20
const CORRECT_PAY := 5
const WRONG_DEDUCTION := 2

var phase := Phase.READY
var order_index := 0
var cup: Array[String] = []
var correct := 0
var wrong := 0
var discarded := 0
var rejected_this_cup := false
var message := "薇斯帕：無酒精飲料這邊，就交給你了。"

func reset() -> void:
	phase = Phase.READY
	order_index = 0
	cup.clear()
	correct = 0
	wrong = 0
	discarded = 0
	rejected_this_cup = false
	message = "薇斯帕：無酒精飲料這邊，就交給你了。"

func start() -> void:
	if phase == Phase.READY:
		phase = Phase.MIXING
		message = "第一位客人點了一杯紅茶。按配方加入材料後送出。"

func current_order() -> String:
	return ORDERS[order_index] if order_index < ORDERS.size() else ""

func add(ingredient: String) -> void:
	if phase != Phase.MIXING or not INGREDIENTS.has(ingredient):
		return
	if cup.has(ingredient):
		message = "杯中已經有%s，不需要重複加入。" % LABELS[ingredient]
		return
	cup.append(ingredient)
	message = "已加入%s。材料順序不影響配方。" % LABELS[ingredient]

func discard() -> void:
	if phase != Phase.MIXING:
		return
	if cup.is_empty():
		message = "杯子是空的，可以直接加入材料。"
		return
	cup.clear()
	discarded += 1
	rejected_this_cup = false
	message = "倒掉重做。這次不扣分，訂單保持不變。"

func matches_order() -> bool:
	if current_order().is_empty():
		return false
	var recipe: Array = RECIPES[current_order()]
	if recipe.size() != cup.size():
		return false
	for ingredient in recipe:
		if not cup.has(ingredient):
			return false
	return true

func serve() -> bool:
	if phase != Phase.MIXING:
		return false
	if cup.is_empty():
		message = "先加入材料，空杯無法送出。"
		return false
	if matches_order():
		correct += 1
		phase = Phase.ORDER_RESULT
		message = "客人：謝謝，正是我要的%s！" % current_order()
		return true
	if not rejected_this_cup:
		wrong += 1
		rejected_this_cup = true
	message = "客人：這杯和我點的不一樣。請修正，或倒掉重做。"
	return false

func next_order() -> void:
	if phase != Phase.ORDER_RESULT:
		return
	order_index += 1
	cup.clear()
	rejected_this_cup = false
	if order_index >= ORDERS.size():
		phase = Phase.DONE
		message = "今晚的飲料都完成了。看看工作結果吧。"
	else:
		phase = Phase.MIXING
		message = "下一位客人要一杯%s。" % current_order()

func simulated_pay() -> int:
	return maxi(0, BASE_PAY + correct * CORRECT_PAY - wrong * WRONG_DEDUCTION)

func simulated_relationship_change() -> int:
	if wrong == 0:
		return 3
	return 1 if wrong <= 2 else -1
