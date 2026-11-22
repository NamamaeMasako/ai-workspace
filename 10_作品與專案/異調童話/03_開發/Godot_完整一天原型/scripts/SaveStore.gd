extends RefCounted

const Session = preload("res://scripts/DaySession.gd")
const Codec = preload("res://scripts/SaveCodec.gd")
const SLOTS := ["auto", "manual"]
var directory := "user://saves"

func _init(save_directory: String = "user://saves") -> void:
	directory = save_directory

func path_for(slot: String) -> String:
	return directory.path_join(slot + ".json")

func read_file(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {"ok": false, "error": "尚無存檔。"}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {"ok": false, "error": "無法開啟存檔。"}
	if file.get_length() > 8 * 1024 * 1024:
		file.close()
		return {"ok": false, "error": "存檔大小超出本版支援範圍。"}
	var raw := file.get_as_text()
	file.close()
	var json := JSON.new()
	if json.parse(raw) != OK:
		return {"ok": false, "error": "存檔內容損壞或不完整。"}
	return Codec.validate(json.data)

func load_slot(slot: String) -> Dictionary:
	if not SLOTS.has(slot):
		return {"ok": false, "error": "未知存檔欄位。"}
	var main := read_file(path_for(slot))
	if main.ok:
		main["recovered"] = false
		return main
	var backup := read_file(path_for(slot) + ".bak")
	if backup.ok:
		backup["recovered"] = true
		backup["notice"] = "主存檔無法讀取，使用上一份完整備份。"
		return backup
	return main

func save_slot(slot: String, session) -> Dictionary:
	if not SLOTS.has(slot) or not Session.SAFE_PHASES.has(session.phase):
		return {"ok": false, "error": "目前不在可保存的時點。"}
	var envelope := {"schema": Codec.SCHEMA, "game": Codec.GAME_ID,
		"relationship_rules": Session.Rules.VERSION, "exposure_rules": Session.Exposure.VERSION,
		"saved_at": Time.get_datetime_string_from_system(), "run": session.to_snapshot()}
	var check := Codec.validate(envelope)
	if not check.ok:
		return check
	var ancestor := directory
	while ancestor != "user://" and not ancestor.is_empty():
		if FileAccess.file_exists(ancestor):
			return {"ok": false, "error": "存檔資料夾路徑被檔案占用；舊檔仍保留。"}
		var parent := ancestor.get_base_dir()
		if parent == ancestor:
			break
		ancestor = parent
	var mkdir_error := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(directory))
	if mkdir_error != OK:
		return {"ok": false, "error": "無法建立存檔資料夾。"}
	var target := path_for(slot)
	var temporary := target + ".tmp"
	var file := FileAccess.open(temporary, FileAccess.WRITE)
	if file == null:
		return {"ok": false, "error": "存檔暫存檔寫入失敗；舊檔仍保留。"}
	file.store_string(JSON.stringify(envelope, "\t"))
	file.flush()
	var write_error := file.get_error()
	file.close()
	if write_error != OK:
		return {"ok": false, "error": "存檔寫入不完整；舊檔仍保留。"}
	if FileAccess.file_exists(target):
		var previous := read_file(target)
		# 好檔保存為上一份備份；壞檔另外封存，不覆蓋既有的好備份。
		var backup := target + ".bak" if previous.ok else target + ".rejected_" + str(Time.get_ticks_usec())
		var copy_error := DirAccess.copy_absolute(ProjectSettings.globalize_path(target), ProjectSettings.globalize_path(backup))
		if copy_error != OK:
			return {"ok": false, "error": "無法保留舊檔，已取消覆寫。"}
	var replace_error := DirAccess.rename_absolute(ProjectSettings.globalize_path(temporary), ProjectSettings.globalize_path(target))
	if replace_error != OK:
		return {"ok": false, "error": "無法替換存檔；舊檔仍保留。"}
	return {"ok": true, "saved_at": envelope.saved_at}

func restored_session(result: Dictionary):
	if not result.get("ok", false):
		return null
	var session := Session.new()
	session.restore_validated(result.snapshot)
	return session
