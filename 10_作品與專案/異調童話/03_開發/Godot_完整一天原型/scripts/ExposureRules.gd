extends RefCounted
## exposure-v1：生前確認的初輪測試數值。
const VERSION := "exposure-v1"
const START := 10
const DAILY_RISE := 6
const QUEST_REDUCTIONS := [20, 20, 35]
const DANGER := 60
const EARLY_CLOSURE := 80
const FRIENDLY := 40

static func grade(value: int) -> String:
	if value >= 100:
		return "失守"
	if value >= 80:
		return "嚴密"
	if value >= 60:
		return "危險"
	if value >= 30:
		return "警戒"
	return "平靜"

static func closure_reason(value: int, closeness: int) -> String:
	if value >= 100:
		return "暴露度到達 100，據點失守"
	if value >= EARLY_CLOSURE and closeness < FRIENDLY:
		return "暴露度達 80 且關係未達友好，據點停止往來"
	return ""
