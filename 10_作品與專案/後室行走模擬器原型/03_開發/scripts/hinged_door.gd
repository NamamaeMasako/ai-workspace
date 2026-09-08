extends "res://scripts/interactable.gd"
## Opening never moves the player. The leaf remains a physical, visible door.
@export var leaf_path: NodePath
@export var open_angle_degrees := 90.0
@export var opening_seconds := 1.1

func interact() -> String:
	if used:
		return message
	used = true
	set_highlight(false)
	var leaf := get_node(leaf_path) as AnimatableBody3D
	var tween := create_tween().set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
	tween.tween_property(leaf, "rotation:y", deg_to_rad(open_angle_degrees), opening_seconds).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	return message
