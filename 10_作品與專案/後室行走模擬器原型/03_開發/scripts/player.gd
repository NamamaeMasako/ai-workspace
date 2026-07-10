extends CharacterBody3D

@export var speed := 4.0
@export var mouse_sensitivity := 0.0025
@export var gravity := 9.8
@export var interact_distance := 4.5
@export var interact_close_distance := 1.6
@export var interact_view_angle := 0.45

@onready var head: Node3D = $Head
@onready var interaction_ray: RayCast3D = $Head/InteractionRay
@onready var prompt_label: Label = %PromptLabel
@onready var message_label: Label = %MessageLabel

var current_interactable: Area3D
var previous_interactable: Area3D
var owned_keys := {}

func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	message_label.text = "你醒在一片潮黃色的房間裡。螢光燈在頭頂發出很薄的嗡鳴。"

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * mouse_sensitivity)
		head.rotate_x(-event.relative.y * mouse_sensitivity)
		head.rotation.x = clamp(head.rotation.x, deg_to_rad(-80), deg_to_rad(80))
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE:
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		elif event.keycode == KEY_ENTER and Input.mouse_mode == Input.MOUSE_MODE_VISIBLE:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		elif event.is_action_pressed("interact") and is_instance_valid(current_interactable):
			_use_current_interactable()

func _physics_process(delta: float) -> void:
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	velocity.x = direction.x * speed
	velocity.z = direction.z * speed
	if not is_on_floor():
		velocity.y -= gravity * delta
	else:
		velocity.y = 0.0
	move_and_slide()
	_check_fall_reset()
	_update_interaction_target()

func _use_current_interactable() -> void:
	var target := current_interactable
	if not is_instance_valid(target):
		return
	if bool(target.get("is_key")):
		owned_keys[str(target.get("key_id"))] = true
		target.set_highlight(false)
		message_label.text = target.interact()
		current_interactable = null
		prompt_label.text = ""
		return
	if bool(target.get("is_exit_door")):
		var needed_key := str(target.get("required_key_id"))
		if not owned_keys.has(needed_key):
			message_label.text = "門把沒有反應。你還需要先找到這個區域的通行物。"
			return
		message_label.text = target.interact()
		_go_to_destination(str(target.get("destination")))
		return
	message_label.text = target.interact()

func _check_fall_reset() -> void:
	if global_position.y < -18.0:
		if global_position.x > 42.0:
			global_position = Vector3(48.0, 1.0, 0.0)
			velocity = Vector3.ZERO
			rotation = Vector3.ZERO
			head.rotation = Vector3.ZERO
			message_label.text = "你從粉色邊界外墜落。雲層沒有盡頭；下一秒，你又站回童話區的起點。"
		else:
			global_position = Vector3(0.0, 1.0, 4.0)
			velocity = Vector3.ZERO

func _go_to_destination(destination: String) -> void:
	if destination == "pool":
		global_position = Vector3(28.0, 1.0, 0.0)
		rotation = Vector3.ZERO
		head.rotation = Vector3.ZERO
		var hum := get_node_or_null("../AmbientHum")
		if hum and hum.has_method("stop"):
			hum.stop()
		var fairy_audio := get_node_or_null("../FairyAmbientLoop")
		if fairy_audio and fairy_audio.has_method("stop"):
			fairy_audio.stop()
		var pool_audio := get_node_or_null("../PoolWaterLoop")
		if pool_audio and pool_audio.has_method("play"):
			pool_audio.play()
	elif destination == "fairy_preview":
		global_position = Vector3(48.0, 1.0, 0.0)
		rotation = Vector3.ZERO
		head.rotation = Vector3.ZERO
		var hum := get_node_or_null("../AmbientHum")
		if hum and hum.has_method("stop"):
			hum.stop()
		var pool_audio := get_node_or_null("../PoolWaterLoop")
		if pool_audio and pool_audio.has_method("stop"):
			pool_audio.stop()
		var fairy_audio := get_node_or_null("../FairyAmbientLoop")
		if fairy_audio and fairy_audio.has_method("play"):
			fairy_audio.stop()
			fairy_audio.play()
		message_label.text = "門後是一片粉色的光。你踏進一座蓋在高空上的童話遊樂場。"

func _update_interaction_target() -> void:
	previous_interactable = current_interactable
	current_interactable = _find_best_interactable()
	prompt_label.text = ""
	if is_instance_valid(current_interactable):
		prompt_label.text = str(current_interactable.get("prompt"))
	if previous_interactable != current_interactable and is_instance_valid(previous_interactable) and previous_interactable.has_method("set_highlight"):
		previous_interactable.set_highlight(false)
	if is_instance_valid(current_interactable) and current_interactable.has_method("set_highlight"):
		current_interactable.set_highlight(true)

func _find_best_interactable() -> Area3D:
	var camera_pos := head.global_position
	var forward := -head.global_transform.basis.z.normalized()
	var best: Area3D = null
	var best_score := -9999.0
	for node in get_tree().get_nodes_in_group("interactables"):
		if not (node is Area3D):
			continue
		var item := node as Area3D
		if not item.has_method("interact") or bool(item.get("used")):
			continue
		var to_item: Vector3 = item.global_position - camera_pos
		var distance: float = to_item.length()
		if distance > interact_distance:
			continue
		var direction: Vector3 = to_item.normalized()
		var facing: float = forward.dot(direction)
		if distance > interact_close_distance and facing < interact_view_angle:
			continue
		var score: float = facing * 2.0 - distance * 0.15
		if distance <= interact_close_distance:
			score += 1.0
		if score > best_score:
			best_score = score
			best = item
	return best
