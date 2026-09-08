extends SceneTree
## Run with: Godot --headless --path <project> --script res://tools/launch-tools/check_continuous_walk.gd
var world: Node3D
var player: CharacterBody3D
var failures := 0

func _initialize() -> void:
	_run.call_deferred()

func check(condition: bool, description: String) -> void:
	if not condition:
		failures += 1
		push_error(description)

func _run() -> void:
	Engine.time_scale = 3.0
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	player = world.get_node("Player")
	player.set_physics_process(false)
	for frame in range(6):
		await physics_frame
	if "--capture-only" in OS.get_cmdline_user_args():
		await capture_views()
		world.stop_ambience()
		await create_timer(0.2).timeout
		world.queue_free()
		await process_frame
		quit()
		return
	player.global_position = Vector3(7.8, 0.86, -7.8)
	player.rotation.y = 0.37
	player.head.rotation.x = -0.1
	var first = world.get_node("FarDoor")
	player.current_interactable = first
	player._use_current_interactable()
	check(not first.used, "First door opened without its key")
	check(player.test_move(player.global_transform, Vector3(0, 0, -2)), "Closed first door does not block passage")
	player.owned_keys["backrooms"] = true
	var before := player.global_transform
	player._use_current_interactable()
	check(player.global_transform == before, "Opening changed player transform")
	check(is_equal_approx(player.head.rotation.x, -0.1), "Opening changed camera pitch")
	await create_timer(0.55).timeout
	var halfway: float = world.get_node("ExitDoor").rotation.y
	check(halfway > 0.1 and halfway < 1.5, "First door did not animate through an intermediate angle")
	await create_timer(0.8).timeout
	check(is_equal_approx(world.get_node("ExitDoor").rotation.y, PI / 2.0), "First door did not finish opening")
	check(not player.test_move(player.global_transform, Vector3(0, 0, -2)), "Open first door still blocks the doorway")
	var route: Array[Vector2] = [
		Vector2(7.8, -10.6), Vector2(7.8, -13),
		Vector2(20, -13), Vector2(20, -8.5),
		Vector2(20, 8), Vector2(36.8, 8), Vector2(36.8, 6.6)]
	for point in route:
		await walk_to(point)
	print("PASS: first corridor walked into pool")
	var second = world.get_node("PoolScene/PoolExit")
	player.current_interactable = second
	player._use_current_interactable()
	check(not second.used, "Pool door opened with only the first key")
	check(player.test_move(player.global_transform, Vector3(2, 0, 0)), "Closed pool door does not block passage")
	player.owned_keys["pool"] = true
	before = player.global_transform
	player._use_current_interactable()
	check(player.global_transform == before, "Pool door teleported or rotated player")
	await create_timer(1.3).timeout
	check(is_equal_approx(world.get_node("PoolScene/PoolExitDoor").rotation.y, -PI / 2.0), "Pool door did not finish opening")
	check(not player.test_move(player.global_transform, Vector3(2, 0, 0)), "Open pool door still blocks passage")
	for point in [Vector2(39.25, 6.6), Vector2(39.25, 2), Vector2(42, 2)]:
		await walk_to(point)
	print("PASS: second corridor walked into fairy area")
	check(world.weights_at(Vector2(42, 2)).is_equal_approx(Vector3(0, 0, 1)), "Wrong fairy ambience")
	for point in [Vector2(39.25, 2), Vector2(39.25, 6.6), Vector2(36.8, 6.6), Vector2(36.8, 8), Vector2(20, 8), Vector2(20, -8.5), Vector2(20, -13), Vector2(7.8, -13), Vector2(7.8, -7.8)]:
		await walk_to(point)
	check(player.owned_keys.has("backrooms") and player.owned_keys.has("pool"), "Return trip lost inventory")
	check(is_equal_approx(player.rotation.y, 0.37) and is_equal_approx(player.head.rotation.x, -0.1), "Walking changed camera orientation")
	check(world.weights_at(Vector2(7.8, -7.8)).is_equal_approx(Vector3(1, 0, 0)), "Return ambience incorrect")
	var blend: Vector3 = world.weights_at(Vector2(14, -13))
	check(blend.x > 0.1 and blend.y > 0.1, "No overlapping ambience in first corridor")
	print("PASS: return walk, camera preservation, inventory and audio crossfade")
	print("CONTINUOUS_WALK_FAILURES=", failures)
	world.stop_ambience()
	await create_timer(0.2).timeout
	world.queue_free()
	await process_frame
	quit.call_deferred(0 if failures == 0 else 1)

func capture_views() -> void:
	world.get_node("FarDoor").interact()
	world.get_node("PoolScene/PoolExit").interact()
	await create_timer(1.4).timeout
	var directory := "user://continuous-walk-preview"
	DirAccess.make_dir_recursive_absolute(directory)
	var views := [
		[Vector3(7.8, 0.86, -7.5), Vector3(7.8, 1.55, -12), "01-open-door"],
		[Vector3(7.8, 0.86, -13), Vector3(20, 1.55, -13), "02-first-corner"],
		[Vector3(20, 0.86, -11.7), Vector3(23, 1.55, -5), "03-pool-entry"],
		[Vector3(36.8, 0.86, 6.6), Vector3(39.25, 1.55, 6.6), "04-pool-door"],
		[Vector3(39.25, 0.86, 2), Vector3(45, 1.55, 2), "05-fairy-entry"]]
	var camera: Camera3D = player.get_node("Head/Camera3D")
	for view in views:
		player.global_position = view[0]
		camera.look_at(view[1])
		for frame in range(8):
			await process_frame
		await RenderingServer.frame_post_draw
		var picture := root.get_texture().get_image()
		picture.save_png(directory + "/" + view[2] + ".png")
	print("CAPTURE_DIRECTORY=", ProjectSettings.globalize_path(directory))

func walk_to(point: Vector2) -> void:
	for frame in range(900):
		await physics_frame
		var offset := point - Vector2(player.global_position.x, player.global_position.z)
		if offset.length() < 0.07:
			check(player.global_position.y > 0.7 and player.global_position.y < 1.1, "Floor height invalid at " + str(point))
			return
		var direction := offset.normalized()
		var step_speed: float = minf(4.0, offset.length() / player.get_physics_process_delta_time())
		player.velocity = Vector3(direction.x * step_speed, -1.0, direction.y * step_speed)
		player.move_and_slide()
	check(false, "Blocked walking to " + str(point) + " at " + str(player.global_position))
