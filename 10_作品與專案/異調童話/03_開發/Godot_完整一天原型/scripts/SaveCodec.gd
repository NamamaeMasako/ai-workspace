extends RefCounted

const Session = preload("res://scripts/DaySession.gd")
const SCHEMA := 1
const GAME_ID := "yidiao_daily_prototype"
const PHASE_LABELS := {0: "早餐前", 1: "下午安排", 3: "晚上安排", 6: "當日結算"}
const INT_LIMITS := {"phase": [0,8], "day_number": [1,100000], "money": [0,1000000000],
	"day_start_money": [0,1000000000], "shopping_cost": [0,22], "visit_spent": [0,10],
	"louve_hp": [0,8], "work_pay": [0,40], "work_errors": [0,1000000], "debug_funds": [0,1000000000]}
const BOOL_FIELDS := ["permanent_evidence", "permanent_communicator", "communicator_known", "eggplant_known",
	"evidence_found", "communicator_acquired", "detected", "retreated", "worked", "favorite_lunch"]
const TEXT_FIELDS := ["activity", "visit_site", "visit_kind", "visit_quest", "visit_result"]

static func whole(value, low: int, high: int) -> bool:
	return (typeof(value) == TYPE_INT or typeof(value) == TYPE_FLOAT) and is_finite(float(value)) and float(value) == floorf(float(value)) and value >= low and value <= high

static func text_ok(value, limit: int = 4096) -> bool:
	return value is String and value.length() <= limit

static func normalize(value):
	if value is Dictionary:
		var result := {}
		for key in value:
			result[key] = normalize(value[key])
		return result
	if value is Array:
		var result := []
		for item in value:
			result.append(normalize(item))
		return result
	return int(value) if typeof(value) == TYPE_FLOAT else value

static func value_map(value, ids: Array) -> bool:
	if not value is Dictionary or value.size() != ids.size():
		return false
	for id in ids:
		if not value.has(id) or not whole(value[id], 0, 100):
			return false
	return true

static func losses_ok(value, exposures: Dictionary, relationships: Dictionary) -> bool:
	if not value is Dictionary:
		return false
	for site in value:
		if not Session.Rules.SITES.has(site) or not text_ok(value[site], 256) or value[site].is_empty() or exposures[site] < 80:
			return false
	for site in Session.Rules.SITES:
		if not Session.Exposure.closure_reason(exposures[site], relationships[site]).is_empty() and not value.has(site):
			return false
	return true

static func ids_ok(value, allowed: Array, maximum: int) -> bool:
	if not value is Array or value.size() > maximum:
		return false
	var seen := {}
	for id in value:
		if not id is String or not allowed.has(id) or seen.has(id):
			return false
		seen[id] = true
	return true

static func strings_ok(value) -> bool:
	if not value is Array or value.size() > 128:
		return false
	for item in value:
		if not text_ok(item):
			return false
	return true

static func log_ok(rows, ids: Array, day: int) -> bool:
	if not rows is Array or rows.size() > 100000:
		return false
	for row in rows:
		if not row is Dictionary or row.size() != 7:
			return false
		for key in ["day", "id", "before", "after", "delta", "requested", "reason"]:
			if not row.has(key):
				return false
		if not whole(row.day, 1, day) or not ids.has(row.id) or not text_ok(row.reason):
			return false
		if not whole(row.before, 0, 100) or not whole(row.after, 0, 100) or not whole(row.delta, -100, 100) or not whole(row.requested, -1000000, 1000000):
			return false
		if row.after - row.before != row.delta:
			return false
	return true

static func validate(envelope) -> Dictionary:
	if not envelope is Dictionary:
		return {"ok": false, "error": "存檔內容不是有效的資料物件。"}
	if not whole(envelope.get("schema"), SCHEMA, SCHEMA):
		return {"ok": false, "error": "存檔版本不支援；原檔保留。"}
	if envelope.get("game") != GAME_ID or envelope.get("relationship_rules") != Session.Rules.VERSION or envelope.get("exposure_rules") != Session.Exposure.VERSION:
		return {"ok": false, "error": "存檔的遊戲或數值規則版本不相容。"}
	if not text_ok(envelope.get("saved_at"), 64):
		return {"ok": false, "error": "存檔時間資料不完整。"}
	var issue := validate_run(envelope.get("run"))
	if not issue.is_empty():
		return {"ok": false, "error": "存檔資料不完整或不合理：" + issue}
	return {"ok": true, "snapshot": normalize(envelope.run), "saved_at": envelope.saved_at}

static func validate_run(data) -> String:
	if not data is Dictionary or data.size() != Session.SNAPSHOT_FIELDS.size():
		return "欄位數量"
	for field in Session.SNAPSHOT_FIELDS:
		if not data.has(field):
			return "缺少 " + field
	for field in INT_LIMITS:
		if not whole(data[field], INT_LIMITS[field][0], INT_LIMITS[field][1]):
			return field
	if not Session.SAFE_PHASES.has(int(data.phase)):
		return "不支援的保存時點"
	for field in BOOL_FIELDS:
		if not data[field] is bool:
			return field
	for field in TEXT_FIELDS:
		if not text_ok(data[field]):
			return field
	var sites: Array = Session.Rules.SITES.keys()
	var people: Array = ["noa"] + sites
	for field in ["relationships", "day_start_relationships"]:
		if not value_map(data[field], people):
			return field
	for field in ["exposures", "day_start_exposures"]:
		if not value_map(data[field], sites):
			return field
	if not losses_ok(data.lost_sites, data.exposures, data.relationships):
		return "據點失去紀錄"
	var quests: Array = []
	for site in sites:
		for index in range(3):
			quests.append("%s_%d" % [site, index])
	if not ids_ok(data.completed_quests, quests, 12):
		return "任務識別"
	for site in sites:
		for index in range(1,3):
			if data.completed_quests.has("%s_%d" % [site,index]) and not data.completed_quests.has("%s_%d" % [site,index-1]):
				return "任務順序"
	for field in ["cleared_routes", "consumed_today"]:
		if not ids_ok(data[field], sites, 4):
			return field
	if not ids_ok(data.extras, Session.EXTRA_COST.keys(), 3):
		return "採購項目"
	for field in ["day_notes", "exposure_notes", "overnight_notes"]:
		if not strings_ok(data[field]):
			return field
	if not data.visit_site.is_empty() and not sites.has(data.visit_site):
		return "據點識別"
	if data.visit_kind not in ["", "quest", "consume", "route"] or (not data.visit_quest.is_empty() and not quests.has(data.visit_quest)):
		return "據點行動"
	if not log_ok(data.relationship_log, people, data.day_number) or not log_ok(data.exposure_log, sites, data.day_number):
		return "變化紀錄"
	if not data.day_history is Array or data.day_history.size() != int(data.day_number) - 1:
		return "跨日次數"
	var index := 1
	for row in data.day_history:
		if not row is Dictionary or row.size() != 6 or not whole(row.get("day"), index, index) or not whole(row.get("money"), 0, 1000000000) or not text_ok(row.get("activity")):
			return "歷日紀錄"
		if not value_map(row.get("relationships"), people) or not value_map(row.get("exposures"), sites):
			return "歷日數值"
		if not losses_ok(row.get("lost_sites"), row.exposures, row.relationships):
			return "歷日失去據點"
		for site in row.lost_sites:
			if not data.lost_sites.has(site):
				return "失去據點不能恢復"
		index += 1
	if data.day_start_money - data.shopping_cost - data.visit_spent + data.work_pay + data.debug_funds != data.money:
		return "金錢收支"
	if data.shopping_cost != 0:
		var expected := Session.FIXED_COST
		for item in data.extras:
			expected += Session.EXTRA_COST[item]
		if expected != data.shopping_cost:
			return "採購扣款"
	if data.phase == Session.Phase.BREAKFAST:
		if data.shopping_cost != 0 or not data.extras.is_empty() or data.worked or data.work_pay != 0 or not data.activity.is_empty() or not data.cleared_routes.is_empty():
			return "早餐前狀態"
	elif data.shopping_cost < Session.FIXED_COST:
		return "尚未完成採購"
	if data.phase != Session.Phase.SUMMARY and (data.worked or data.work_pay != 0 or data.favorite_lunch):
		return "未到結算卻已發薪"
	if data.favorite_lunch and (not data.worked or not data.eggplant_known or not data.extras.has("茄子")):
		return "便當紀錄"
	return ""
