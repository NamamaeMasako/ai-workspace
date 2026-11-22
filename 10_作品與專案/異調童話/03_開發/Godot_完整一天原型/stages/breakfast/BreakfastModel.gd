extends RefCounted

enum Phase { READY, QTE, DIALOGUE, ROUND_RESULT, SHOPPING, DONE }
const Rules = preload("res://scripts/RelationshipRules.gd")
const ROUND_COUNT := 2
const ROUND_SECONDS := 10.0
const RESULT_SECONDS := 1.4

var budget := 100
var emotional_topic := false
var phase := Phase.READY
var round_number := 0
var seconds_left := ROUND_SECONDS
var input_buffer := ""
var outcome := ""
var result_seconds := 0.0
var selected := -1
var dialogue_index := 0
var topics: Array[Dictionary] = []
var history: Array[Dictionary] = []
var communicator_known := false
var eggplant_known := false
var extras: Array[String] = []

func reset() -> void:
	phase = Phase.READY
	emotional_topic = false
	round_number = 0
	seconds_left = ROUND_SECONDS
	input_buffer = ""
	outcome = ""
	result_seconds = 0.0
	selected = -1
	dialogue_index = 0
	topics.clear()
	history.clear()
	communicator_known = false
	eggplant_known = false
	extras.clear()

func start() -> void:
	if phase == Phase.READY:
		begin_round()

func begin_round() -> void:
	round_number += 1
	seconds_left = ROUND_SECONDS
	input_buffer = ""
	selected = -1
	dialogue_index = 0
	phase = Phase.QTE
	if round_number == 1:
		topics = [
			{"opening": "記得之前在奶奶家看過……", "code": "UDLR", "effect": "communicator", "lines": [
				["洛芙", "你說看過什麼？"],
				["諾亞", "組織用的通訊器。奶奶家裡有一台。"],
				["洛芙", "拿到它，或許能讓他們晚一點找到我們。我記下了。"],
			]},
			{"opening": "昨天在……", "code": "UUD", "effect": "chat", "lines": [
				["諾亞", "昨天窗邊有隻小鳥，一直盯著我的麵包。"],
				["洛芙", "大概和你一樣，正在等早餐。"],
			]},
			{"opening": "突然很想……", "code": "LR", "effect": "eggplant", "lines": [
				["諾亞", "突然很想吃茄子。帶在便當裡應該也很好吃。"],
				["洛芙", "知道了。等一下列採購清單時記得買。"],
			]},
		]
	else:
		topics = [
			{"opening": "還有那種通訊器……", "code": "DUL", "effect": "communicator", "lines": [
				["洛芙", "關於那台通訊器，你還記得嗎？"],
				["諾亞", "嗯，是奶奶家裡那台組織用的通訊器。"],
				["洛芙", "值得去找找。先把這件事記下。"],
			]},
			{"opening": "今天能一起吃早餐……", "code": "LUD", "effect": "emotional", "lines": [
				["諾亞", "有人一起吃早餐，感覺很好。"],
				["洛芙", "那就慢慢吃，我還在這裡。"],
			]},
			{"opening": "剛才想到的那道菜……", "code": "RDR", "effect": "eggplant", "lines": [
				["諾亞", "我想到的是茄子。今天有點想吃。"],
				["洛芙", "好，列清單時我會記得。"],
			]},
		]

func tick(delta: float) -> void:
	if phase == Phase.QTE:
		seconds_left = maxf(0.0, seconds_left - delta)
		if seconds_left <= 0:
			fail("時間到了，這輪沒有接上話題。")
	elif phase == Phase.ROUND_RESULT:
		result_seconds -= delta
		if result_seconds <= 0:
			if round_number < ROUND_COUNT:
				begin_round()
			else:
				phase = Phase.SHOPPING

func enter_direction(direction: String) -> void:
	if phase != Phase.QTE or not direction in ["U", "D", "L", "R"]:
		return
	input_buffer += direction
	var still_possible := false
	for index in range(topics.size()):
		var code: String = topics[index].code
		if code.begins_with(input_buffer):
			still_possible = true
			if code == input_buffer:
				selected = index
				dialogue_index = 0
				phase = Phase.DIALOGUE
				return
	if not still_possible:
		fail("輸入沒有對應到任何話題，這輪接話失敗。")

func fail(reason: String) -> void:
	if phase != Phase.QTE:
		return
	outcome = reason
	history.append({"round": round_number, "success": false, "topic": "未接上話題"})
	phase = Phase.ROUND_RESULT
	result_seconds = RESULT_SECONDS

func current_line() -> Array:
	if phase != Phase.DIALOGUE:
		return []
	return topics[selected].lines[dialogue_index]

func next_line() -> void:
	if phase != Phase.DIALOGUE:
		return
	dialogue_index += 1
	if dialogue_index < topics[selected].lines.size():
		return
	var effect: String = topics[selected].effect
	if effect == "communicator":
		communicator_known = true
	elif effect == "eggplant":
		eggplant_known = true
	elif effect == "emotional":
		emotional_topic = true
	history.append({"round": round_number, "success": true, "topic": topics[selected].opening})
	outcome = "話題聊完了。" if effect in ["chat", "emotional"] else ("已記下線索：奶奶家可能有組織通訊器。" if effect == "communicator" else "已記下：今天諾亞想吃茄子。")
	phase = Phase.ROUND_RESULT
	result_seconds = RESULT_SECONDS

func toggle_extra(item: String) -> void:
	if phase != Phase.SHOPPING or not item in ["茄子", "蘋果", "茶葉"]:
		return
	if extras.has(item):
		extras.erase(item)
	else:
		extras.append(item)

func shopping_total() -> int:
	var total := Rules.FIXED_COST
	for item in extras:
		total += Rules.EXTRA_COST[item]
	return total

func confirm_shopping() -> void:
	if phase == Phase.SHOPPING:
		if shopping_total() > budget:
			outcome = "金錢不足：取消額外品項，或使用右上測試補款。"
			return
		phase = Phase.DONE

func favorite_remembered() -> bool:
	return eggplant_known and extras.has("茄子")
