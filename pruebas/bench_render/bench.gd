extends Node3D

const WARMUP_SECONDS := 3.0
const SCENES := ["base", "hierba", "sprites", "sdfgi"]
const SEED_VALUE := 7200620
const GRASS_COUNT := 40000
const WIND_SHADER := """
shader_type spatial;
render_mode cull_disabled, diffuse_toon, specular_disabled;
uniform float bench_time = 0.0;
void vertex() {
    vec3 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    float wave = sin(bench_time * 1.8 + world_pos.x * 0.65 + world_pos.z * 0.4);
    VERTEX.x += wave * 0.20 * UV.y * UV.y;
    VERTEX.z += wave * 0.08 * UV.y * UV.y;
}
void fragment() {
    if (abs(UV.x - 0.5) > mix(0.48, 0.02, UV.y)) { discard; }
    ALBEDO = mix(vec3(0.08, 0.20, 0.03), vec3(0.38, 0.65, 0.12), UV.y);
    ROUGHNESS = 0.9;
}
"""

var scene_name := "base"
var duration_seconds := 12.0
var output_path := "res://resultado_individual.json"
var orbit: Node3D
var grass_material: ShaderMaterial
var environment: Environment
var warmup_start_usec: int = 0
var measurement_start_usec: int = 0
var last_frame_usec: int = 0
var measuring := false
var finished := false
var frame_times_usec := PackedInt64Array()
var draw_calls_sum: int = 0
var draw_calls_max: int = 0
var primitives_sum: int = 0
var primitives_max: int = 0
var video_memory_sum: int = 0
var video_memory_max: int = 0
var video_memory_last: int = 0
var initial_resolution := Vector2i.ZERO
var resolution_changed := false


func _ready() -> void:
	set_process(false)
	if not _parse_arguments():
		get_tree().quit(2)
		return
	if scene_name == "sdfgi" and RenderingServer.get_current_rendering_method() != "forward_plus":
		push_error("La escena sdfgi requiere forward_plus.")
		get_tree().quit(2)
		return
	Engine.max_fps = 0
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	_build_environment()
	_build_camera()
	# Espera la textura antes de iniciar los tres segundos de calentamiento.
	await _build_ground()
	_build_meshes()
	if scene_name == "hierba":
		_build_grass()
	elif scene_name == "sprites":
		_build_sprites()
	initial_resolution = Vector2i(get_viewport().get_texture().get_size())
	warmup_start_usec = Time.get_ticks_usec()
	set_process(true)


func _parse_arguments() -> bool:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--escena="):
			scene_name = argument.trim_prefix("--escena=")
		elif argument.begins_with("--segundos="):
			var value := argument.trim_prefix("--segundos=")
			if not value.is_valid_float():
				push_error("--segundos debe ser un numero positivo y finito.")
				return false
			duration_seconds = value.to_float()
		elif argument.begins_with("--salida="):
			output_path = argument.trim_prefix("--salida=")
		else:
			push_error("Argumento desconocido: " + argument)
			return false
	if scene_name not in SCENES or not is_finite(duration_seconds) or duration_seconds <= 0.0:
		push_error("Escena o duracion no valida.")
		return false
	if output_path.is_empty():
		push_error("--salida no puede estar vacio.")
		return false
	# Las rutas relativas se resuelven dentro del proyecto.
	if not output_path.is_absolute_path():
		output_path = ProjectSettings.globalize_path("res://").path_join(output_path)
	else:
		output_path = ProjectSettings.globalize_path(output_path)
	return true


func _build_environment() -> void:
	environment = Environment.new()
	environment.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	sky.sky_material = ProceduralSkyMaterial.new()
	environment.sky = sky
	environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.ambient_light_color = Color(0.65, 0.72, 0.85)
	environment.ambient_light_energy = 0.35
	environment.sdfgi_enabled = scene_name == "sdfgi"
	environment.ssao_enabled = scene_name == "sdfgi"
	environment.glow_enabled = scene_name == "sdfgi"
	var world := WorldEnvironment.new()
	world.environment = environment
	add_child(world)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48.0, -35.0, 0.0)
	sun.light_energy = 1.4
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 150.0
	add_child(sun)


func _build_camera() -> void:
	orbit = Node3D.new()
	orbit.position = Vector3(0.0, 1.0, 0.0)
	orbit.rotation_degrees.y = 45.0
	add_child(orbit)
	var camera := Camera3D.new()
	camera.projection = Camera3D.PROJECTION_PERSPECTIVE
	camera.fov = 30.0
	camera.near = 0.1
	camera.far = 250.0
	camera.position = Vector3(0.0, sin(deg_to_rad(55.0)) * 90.0, cos(deg_to_rad(55.0)) * 90.0)
	camera.rotation_degrees.x = -55.0
	orbit.add_child(camera)
	camera.current = true


func _build_ground() -> void:
	var noise := FastNoiseLite.new()
	noise.seed = SEED_VALUE
	noise.frequency = 0.035
	var ramp := Gradient.new()
	ramp.set_color(0, Color(0.14, 0.20, 0.08))
	ramp.set_color(1, Color(0.43, 0.48, 0.24))
	var texture := NoiseTexture2D.new()
	texture.width = 512
	texture.height = 512
	texture.seamless = true
	texture.color_ramp = ramp
	texture.noise = noise
	await texture.changed
	var material := StandardMaterial3D.new()
	material.albedo_texture = texture
	material.uv1_scale = Vector3(8.0, 8.0, 1.0)
	material.roughness = 0.9
	var plane := PlaneMesh.new()
	plane.size = Vector2(60.0, 60.0)
	var ground := MeshInstance3D.new()
	ground.mesh = plane
	ground.material_override = material
	ground.gi_mode = GeometryInstance3D.GI_MODE_STATIC
	add_child(ground)


func _build_meshes() -> void:
	var random := RandomNumberGenerator.new()
	random.seed = SEED_VALUE
	var box := BoxMesh.new()
	box.size = Vector3(1.5, 2.0, 1.5)
	var sphere := SphereMesh.new()
	sphere.radius = 1.0
	sphere.height = 2.0
	sphere.radial_segments = 24
	sphere.rings = 12
	var cylinder := CylinderMesh.new()
	cylinder.top_radius = 0.8
	cylinder.bottom_radius = 0.8
	cylinder.height = 2.0
	cylinder.radial_segments = 24
	var meshes: Array[Mesh] = [box, sphere, cylinder]
	for index in range(150):
		var material := StandardMaterial3D.new()
		material.diffuse_mode = BaseMaterial3D.DIFFUSE_TOON
		material.specular_mode = BaseMaterial3D.SPECULAR_TOON
		material.roughness = 0.65
		material.albedo_color = Color.from_hsv(random.randf(), 0.55, 0.85)
		var instance := MeshInstance3D.new()
		instance.mesh = meshes[index % 3]
		instance.material_override = material
		var height_scale := random.randf_range(0.7, 2.4)
		instance.scale = Vector3(1.0, height_scale, 1.0)
		instance.position = Vector3(
			(float(index % 15) - 7.0) * 3.5,
			height_scale,
			(float(index / 15) - 4.5) * 4.0
		)
		instance.rotation.y = random.randf_range(-PI, PI)
		instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		instance.gi_mode = GeometryInstance3D.GI_MODE_STATIC
		add_child(instance)


func _build_grass() -> void:
	var surface := SurfaceTool.new()
	surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	var corners := PackedVector3Array([
		Vector3(-0.12, 0.0, 0.0), Vector3(0.12, 0.0, 0.0),
		Vector3(-0.12, 0.9, 0.0), Vector3(0.12, 0.9, 0.0)
	])
	var uvs := PackedVector2Array([Vector2(0, 0), Vector2(1, 0), Vector2(0, 1), Vector2(1, 1)])
	for angle in [0.0, PI / 2.0]:
		for index in [0, 2, 1, 1, 2, 3]:
			surface.set_normal(Vector3.BACK.rotated(Vector3.UP, angle))
			surface.set_uv(uvs[index])
			surface.add_vertex(corners[index].rotated(Vector3.UP, angle))
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.mesh = surface.commit()
	multimesh.instance_count = GRASS_COUNT
	var random := RandomNumberGenerator.new()
	random.seed = SEED_VALUE + 1
	for index in range(GRASS_COUNT):
		var scale_value := random.randf_range(0.65, 1.35)
		var basis := Basis(Vector3.UP, random.randf_range(-PI, PI)).scaled(Vector3.ONE * scale_value)
		var origin := Vector3(random.randf_range(-29.5, 29.5), 0.02, random.randf_range(-29.5, 29.5))
		multimesh.set_instance_transform(index, Transform3D(basis, origin))
	var shader := Shader.new()
	shader.code = WIND_SHADER
	grass_material = ShaderMaterial.new()
	grass_material.shader = shader
	var grass := MultiMeshInstance3D.new()
	grass.multimesh = multimesh
	grass.material_override = grass_material
	# Incluye la deformacion del viento en el volumen de descarte.
	grass.custom_aabb = AABB(Vector3(-31, -1, -31), Vector3(62, 4, 62))
	grass.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	add_child(grass)


func _build_sprites() -> void:
	var image := Image.create(64, 96, false, Image.FORMAT_RGBA8)
	image.fill(Color(0, 0, 0, 0))
	for y in range(96):
		for x in range(64):
			var point := Vector2((float(x) - 31.5) / 27.0, (float(y) - 34.0) / 32.0)
			if point.length_squared() <= 1.0:
				image.set_pixel(x, y, Color(0.24, 0.65, 0.20, 1.0))
			elif absi(x - 32) < 5 and y >= 32 and y < 94:
				image.set_pixel(x, y, Color(0.40, 0.24, 0.10, 1.0))
	image.generate_mipmaps()
	var texture := ImageTexture.create_from_image(image)
	var random := RandomNumberGenerator.new()
	random.seed = SEED_VALUE + 2
	for index in range(200):
		var sprite := Sprite3D.new()
		sprite.texture = texture
		sprite.pixel_size = 0.04
		sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		sprite.alpha_scissor_threshold = 0.5
		sprite.shaded = true
		sprite.double_sided = true
		sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
		sprite.position = Vector3(random.randf_range(-28, 28), 1.92, random.randf_range(-28, 28))
		add_child(sprite)


func _process(_delta: float) -> void:
	if finished:
		return
	var now_usec := Time.get_ticks_usec()
	var elapsed := float(now_usec - warmup_start_usec) / 1000000.0
	orbit.rotation.y = deg_to_rad(45.0) + elapsed * 0.025
	if grass_material != null:
		grass_material.set_shader_parameter("bench_time", elapsed)
	if Vector2i(get_viewport().get_texture().get_size()) != initial_resolution:
		resolution_changed = true
	if not measuring:
		if elapsed >= WARMUP_SECONDS:
			measuring = true
			measurement_start_usec = now_usec
			last_frame_usec = now_usec
		return
	# Intervalo real entre callbacks, sin usar delta suavizado ni FPS del motor.
	var frame_usec := now_usec - last_frame_usec
	last_frame_usec = now_usec
	frame_times_usec.append(frame_usec)
	var calls := RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)
	var primitives := RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME)
	video_memory_last = RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_VIDEO_MEM_USED)
	draw_calls_sum += calls
	draw_calls_max = maxi(draw_calls_max, calls)
	primitives_sum += primitives
	primitives_max = maxi(primitives_max, primitives)
	video_memory_sum += video_memory_last
	video_memory_max = maxi(video_memory_max, video_memory_last)
	if float(now_usec - measurement_start_usec) / 1000000.0 >= duration_seconds:
		finished = true
		set_process(false)
		_write_result(now_usec)


func _write_result(end_usec: int) -> void:
	var sorted_times := frame_times_usec.duplicate()
	sorted_times.sort()
	var count := sorted_times.size()
	var measured_seconds := float(end_usec - measurement_start_usec) / 1000000.0
	var slow_count := maxi(1, ceili(float(count) * 0.01))
	var slow_total: int = 0
	for index in range(count - slow_count, count):
		slow_total += sorted_times[index]
	var result := {
		"schema_version": 1,
		"scene": scene_name,
		"seed": SEED_VALUE,
		"godot_version": Engine.get_version_info(),
		"warmup_seconds": WARMUP_SECONDS,
		"requested_seconds": duration_seconds,
		"measured_seconds": measured_seconds,
		"frames": count,
		"fps_mean": float(count) / measured_seconds,
		"fps_1pct_low": 1000000.0 * float(slow_count) / float(slow_total),
		"slowest_1pct_frames": slow_count,
		"frame_time_mean_ms": measured_seconds * 1000.0 / float(count),
		"frame_time_max_ms": float(sorted_times[count - 1]) / 1000.0,
		"draw_calls_mean": float(draw_calls_sum) / float(count),
		"draw_calls_max": draw_calls_max,
		"primitives_mean": float(primitives_sum) / float(count),
		"primitives_max": primitives_max,
		"video_memory_mean_bytes": float(video_memory_sum) / float(count),
		"video_memory_max_bytes": video_memory_max,
		"video_memory_last_bytes": video_memory_last,
		"adapter_name": RenderingServer.get_video_adapter_name(),
		"graphics_api_version": RenderingServer.get_video_adapter_api_version(),
		"rendering_method": RenderingServer.get_current_rendering_method(),
		"rendering_driver": RenderingServer.get_current_rendering_driver_name(),
		"resolution": {"width": initial_resolution.x, "height": initial_resolution.y},
		"resolution_changed": resolution_changed,
		"vsync_mode": DisplayServer.window_get_vsync_mode(),
		"effects": {"sdfgi": environment.sdfgi_enabled, "ssao": environment.ssao_enabled, "glow": environment.glow_enabled},
		"measurement_notes": "CPU wall-clock frame intervals; 1% low = reciprocal mean of slowest ceil(frames*0.01); rendering counters may be 0 when unavailable; video memory is engine accounting, not dedicated VRAM."
	}
	var error := DirAccess.make_dir_recursive_absolute(output_path.get_base_dir())
	if error != OK:
		push_error("No se pudo crear la carpeta de salida: " + error_string(error))
		get_tree().quit(3)
		return
	var file := FileAccess.open(output_path, FileAccess.WRITE)
	if file == null:
		push_error("No se pudo abrir el JSON: " + error_string(FileAccess.get_open_error()))
		get_tree().quit(3)
		return
	file.store_string(JSON.stringify(result, "\t") + "\n")
	file.flush()
	var write_error := file.get_error()
	file.close()
	if write_error != OK:
		push_error("Error al escribir el JSON: " + error_string(write_error))
		get_tree().quit(3)
		return
	print("BENCH_OK " + output_path)
	get_tree().quit()
