extends Node3D

@export var rotate_speed := 1.2
@export var bob_height := 0.08
@export var bob_speed := 2.0

var start_y := 0.0

func _ready() -> void:
	start_y = position.y

func _process(delta: float) -> void:
	rotate_y(rotate_speed * delta)
	position.y = start_y + sin(Time.get_ticks_msec() / 1000.0 * bob_speed) * bob_height
