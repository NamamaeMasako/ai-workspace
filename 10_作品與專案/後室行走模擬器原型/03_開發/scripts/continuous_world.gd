extends Node3D
## Crossfade by physical position, in both directions; no teleport or camera edits.
const FIRST_ROUTE := [Vector2(7.8, -9.0), Vector2(7.8, -13.0), Vector2(20.0, -13.0), Vector2(20.0, -10.0)]
const SECOND_ROUTE := [Vector2(38.0, 6.6), Vector2(39.25, 6.6), Vector2(39.25, 2.0), Vector2(40.5, 2.0)]
@onready var player: CharacterBody3D = $Player
@onready var layers: Array[AudioStreamPlayer] = [$AmbientHum, $PoolWaterLoop, $FairyAmbientLoop]
var audio_weights := Vector3(1.0, 0.0, 0.0)

func _ready() -> void:
	for layer in layers:
		layer.volume_linear = 0.0
		if not layer.finished.is_connected(layer.play):
			layer.finished.connect(layer.play)
		if not layer.playing:
			layer.play()
	_apply_audio()

func _process(delta: float) -> void:
	var point := Vector2(player.global_position.x, player.global_position.z)
	var target := weights_at(point)
	audio_weights = audio_weights.lerp(target, 1.0 - exp(-delta * 5.0))
	_apply_audio()

func weights_at(point: Vector2) -> Vector3:
	if point.x < 18.0:
		if point.y <= -9.0:
			var amount := _route_progress(point, FIRST_ROUTE)
			return Vector3(1.0 - amount, amount, 0.0)
		return Vector3(1.0, 0.0, 0.0)
	if point.x < 38.0:
		if point.y < -10.0:
			var amount := _route_progress(point, FIRST_ROUTE)
			return Vector3(1.0 - amount, amount, 0.0)
		return Vector3(0.0, 1.0, 0.0)
	if point.x < 40.5:
		var amount := _route_progress(point, SECOND_ROUTE)
		return Vector3(0.0, 1.0 - amount, amount)
	return Vector3(0.0, 0.0, 1.0)

func _route_progress(point: Vector2, route: Array) -> float:
	var total := 0.0
	var walked := 0.0
	var nearest_distance := INF
	var nearest_walked := 0.0
	for index in range(route.size() - 1):
		total += (route[index + 1] as Vector2).distance_to(route[index])
	for index in range(route.size() - 1):
		var start: Vector2 = route[index]
		var end: Vector2 = route[index + 1]
		var closest := Geometry2D.get_closest_point_to_segment(point, start, end)
		var distance := point.distance_squared_to(closest)
		if distance < nearest_distance:
			nearest_distance = distance
			nearest_walked = walked + start.distance_to(closest)
		walked += start.distance_to(end)
	return smoothstep(0.0, 1.0, nearest_walked / total)

func _apply_audio() -> void:
	layers[0].volume_linear = db_to_linear(-12.0) * audio_weights.x
	layers[1].volume_linear = db_to_linear(0.0) * audio_weights.y
	layers[2].volume_linear = db_to_linear(-1.5) * audio_weights.z

func stop_ambience() -> void:
	for layer in layers:
		if is_instance_valid(layer):
			if layer.finished.is_connected(layer.play):
				layer.finished.disconnect(layer.play)
			layer.stop()
