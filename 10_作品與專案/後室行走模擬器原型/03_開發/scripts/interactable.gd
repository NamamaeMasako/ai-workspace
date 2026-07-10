extends Area3D

@export var prompt := "按 E 互動"
@export_multiline var message := "這裡有些不對勁。"
@export var highlight_path: NodePath
@export var is_key := false
@export var key_id := "backrooms"
@export var is_exit_door := false
@export var required_key_id := "backrooms"
@export var destination := "pool"
@export var consume_on_interact := false
@export var consume_visual_paths: Array[NodePath] = []

var highlight_node: Node3D
var used := false

func _ready() -> void:
	add_to_group("interactables")
	if highlight_path != NodePath(""):
		highlight_node = get_node_or_null(highlight_path)
		if highlight_node:
			highlight_node.visible = false

func interact() -> String:
	used = true
	if consume_on_interact:
		call_deferred("_consume")
	return message

func set_highlight(enabled: bool) -> void:
	if used:
		enabled = false
	if highlight_node:
		highlight_node.visible = enabled

func _consume() -> void:
	set_highlight(false)
	visible = false
	monitoring = false
	monitorable = false
	for path in consume_visual_paths:
		var visual := get_node_or_null(path)
		if visual:
			visual.visible = false
	for child in get_children():
		if child is CollisionShape3D:
			child.disabled = true
