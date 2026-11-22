extends RefCounted
## 集中保存本輪已確認的關係測試值；經濟值仍為原型佔位。
const VERSION := "relationship-v1"
const SITES := {"ves": "薇斯帕", "tsuru": "津留", "boars": "波爾三兄弟", "sheep": "希普七姊弟"}
const START_NOA := 25
const START_SITE := 45
const THRESHOLDS := [0, 20, 40, 60, 80]
const NPC_GRADES := ["疏遠", "普通", "友好", "信賴", "摯友"]
const NOA_GRADES := ["生疏", "熟悉", "友好", "親密", "深厚羈絆"]
const HOME_GAIN := 4
const FAVORITE_GAIN := 2
const EMOTIONAL_TOPIC_GAIN := 1
const CONSUME_GAIN := 1
const QUEST_GAINS := [8, 8, 10]
const BROKEN_PROMISE := -4
const START_MONEY := 100
const FIXED_COST := 10
const EXTRA_COST := {"茄子": 5, "蘋果": 4, "茶葉": 3}
const CONSUME_COST := 10

static func grade(value: int, is_noa: bool = false) -> String:
	var index := mini(clampi(value, 0, 100) / 20, 4)
	return NOA_GRADES[index] if is_noa else NPC_GRADES[index]

static func next_threshold(value: int) -> int:
	for threshold in THRESHOLDS:
		if value < threshold:
			return threshold
	return 100

static func work_gain(errors: int) -> int:
	if errors == 0:
		return 3
	return 1 if errors <= 2 else -1
