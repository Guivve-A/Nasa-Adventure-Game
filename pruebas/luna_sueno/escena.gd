extends Node3D

# Luna del sueno: PRUEBA de rendimiento (etapa 7 del plan de auditoria, carril C5). No es el nivel final.
# Terreno lunar de 450 x 450 m (heightmap de 512 x 512 por script, crateres y 4 niveles de detalle) que
# cubre el anillo de 75 m del sitio del Apolo 11; etapa de descenso generica sin insignias en el centro;
# 2000 rocas en MultiMesh; la Tierra en el cielo y sol rasante.
# Argumentos tras "--":
#   --captura=<png>        guarda una captura y sale
#   --medir=<s>            sin vsync: fps medio, ms medio y p95, primitivas y llamadas de dibujo
#   --encuadre=21|12       marcador de 1,05 m al 21 % o al 12,5 % del alto (como en la escena del sendero)
#   --zoom=<f>             aleja (> 1) o acerca (< 1) la camara
#   --objetivo=x,z         centra la camara en un punto del mapa (m; +X este, -Z norte)
#   --vista=juego|cielo    camara alta de juego, o vista baja hacia el oeste para revisar la Tierra
#   --sin_lod              todo el terreno al detalle maximo (para comparar)
#   --sin_rocas            sin las rocas (para comparar)
#   --sin_inclinacion      sin la cizalla 2.5D de los objetos
#   --mapa=<png>           guarda el heightmap como imagen de 513 x 513 (gris = altura)
# Teclas: flechas mueven, rueda aleja, 1 y 2 encuadre, C cielo, F12 captura, Esc sale.

const Terreno := preload("res://terreno.gd")
const Piezas := preload("res://piezas.gd")
const FACETADO := preload("res://shaders/facetado.gdshader")
const REGOLITO := preload("res://shaders/regolito.gdshader")
const TIERRA := preload("res://shaders/tierra.gdshader")

# la misma camara alta de la escena del sendero (pruebas/escena_exploracion/layout.json)
const CAMARA := {"inclinacion_deg": 48.0, "fov_deg": 40.0, "inclinacion_objetos": 0.45,
	"encuadres": {"21": 0.21, "12": 0.125}, "alto_personaje": 1.05}
const SEMILLA := 1969
const ROCAS := 2000
const MARCADOR := Vector2(3.0, 5.4)   # x, z: junto a la zapata sureste de la etapa de descenso
# Sol rasante desde el este (manana lunar). La Tierra a 66 grados de altura hacia el oeste: el sitio esta a
# 23,5 grados de longitud este y la Tierra queda casi fija sobre el punto 0,0 (Fase 2, 03b y calculo con SVS).
const SOL_ALTURA := 10.0
const SOL_AZIMUT := 95.0
const TIERRA_ALTURA := 66.0
const TIERRA_AZIMUT := 268.0
const TIERRA_DISTANCIA := 500.0
const TIERRA_DIAMETRO_DEG := 1.9  # la Tierra vista desde la Luna mide unos 1,9 grados

var terreno := Terreno.new()
var camara := Camera3D.new()
var sol: DirectionalLight3D
var tierra := MeshInstance3D.new()
var materiales: Array[ShaderMaterial] = []
var objetivo := Vector3.ZERO
var encuadre := "21"
var inclinacion := 0.45
var zoom := 1.0
var vista := "juego"
var captura := ""
var medir := 0.0
var sin_lod := false
var sin_rocas := false
var mapa := ""
var etiqueta := Label.new()
var cuenta := {}


func _ready() -> void:
	var xz := MARCADOR
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--captura="):
			captura = arg.trim_prefix("--captura=")
		elif arg.begins_with("--medir="):
			medir = float(arg.trim_prefix("--medir="))
		elif arg.begins_with("--encuadre="):
			encuadre = arg.trim_prefix("--encuadre=")
		elif arg.begins_with("--zoom="):
			zoom = float(arg.trim_prefix("--zoom="))
		elif arg.begins_with("--objetivo="):
			var p := arg.trim_prefix("--objetivo=").split(",")
			xz = Vector2(float(p[0]), float(p[1]))
		elif arg.begins_with("--vista="):
			vista = arg.trim_prefix("--vista=")
		elif arg == "--sin_lod":
			sin_lod = true
		elif arg == "--sin_rocas":
			sin_rocas = true
		elif arg == "--sin_inclinacion":
			inclinacion = 0.0
		elif arg.begins_with("--mapa="):
			mapa = arg.trim_prefix("--mapa=")
	var t0 := Time.get_ticks_msec()
	terreno.generar(SEMILLA)
	var t1 := Time.get_ticks_msec()
	_montar_luz()
	var mat_terreno := _material(REGOLITO)
	cuenta["nodos_terreno"] = terreno.montar(self, mat_terreno, sin_lod)
	var t2 := Time.get_ticks_msec()
	_montar_etapa()
	cuenta["rocas"] = 0 if sin_rocas else _montar_rocas()
	_montar_tierra()
	var t3 := Time.get_ticks_msec()
	add_child(camara)
	camara.fov = CAMARA["fov_deg"]
	camara.near = 0.05
	objetivo = Vector3(xz.x, terreno.altura(xz.x, xz.y), xz.y)
	_ajustar("inclinacion", inclinacion)
	_colocar_camara()
	_interfaz()
	if mapa != "":
		_guardar_mapa(mapa)
	print("ESCENA terreno=%dx%d celdas lado=%.0f m crateres=%d nodos_terreno=%d triangulos_terreno_detalle_max=%d rocas=%d lotes_rocas=%d triangulos_etapa=%d alto_marcador=%.3f lod=%s gravedad=%.3f tiempos_ms generar=%d mallas=%d piezas=%d tierra_iluminada=%.0f%%" % [
		Terreno.CELDAS, Terreno.CELDAS, Terreno.LADO, terreno.crateres.size(), cuenta["nodos_terreno"],
		terreno.triangulos_detalle_max, cuenta["rocas"], cuenta.get("lotes_rocas", 0), cuenta["triangulos_etapa"],
		cuenta["alto_marcador"], "no" if sin_lod else "si",
		float(ProjectSettings.get_setting("physics/3d/default_gravity")), t1 - t0, t2 - t1, t3 - t2, _fraccion_tierra() * 100.0])
	if medir > 0.0:
		await _medir()
		get_tree().quit()
		return
	if captura != "":
		for i in range(40):
			await get_tree().process_frame
		_guardar(captura)
		get_tree().quit()


func _material(shader: Shader) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = shader
	# luz lunar: sin atmosfera, las caras de espaldas al sol y las sombras quedan casi negras
	m.set_shader_parameter("sombra_cara", 0.22)
	m.set_shader_parameter("sombra_proyectada", 0.88)
	m.set_shader_parameter("borde_luz", 0.25)
	materiales.append(m)
	return m


func _ajustar(nombre: String, valor) -> void:
	for m in materiales:
		m.set_shader_parameter(nombre, valor)


static func direccion(azimut_deg: float, altura_deg: float) -> Vector3:
	# azimut desde el norte (-Z) hacia el este (+X)
	var a := deg_to_rad(azimut_deg)
	var h := deg_to_rad(altura_deg)
	return Vector3(sin(a) * cos(h), sin(h), -cos(a) * cos(h))


func _fraccion_tierra() -> float:
	# fraccion iluminada del disco: el angulo de fase en la Tierra es 180 menos la separacion Sol-Tierra
	var sep := direccion(SOL_AZIMUT, SOL_ALTURA).angle_to(direccion(TIERRA_AZIMUT, TIERRA_ALTURA))
	return (1.0 - cos(sep)) * 0.5


func _montar_luz() -> void:
	sol = DirectionalLight3D.new()
	sol.name = "Sol"
	sol.light_color = Color("fff8ee")  # sin atmosfera: blanco, apenas calido
	sol.light_energy = 1.45
	sol.shadow_enabled = true
	sol.shadow_blur = 1.0
	sol.shadow_bias = 0.06
	sol.shadow_normal_bias = 1.4
	sol.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sol.directional_shadow_max_distance = 40.0
	add_child(sol)
	sol.look_at_from_position(Vector3.ZERO, -direccion(SOL_AZIMUT, SOL_ALTURA), Vector3.UP)
	var entorno := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color("05070c")  # cielo negro (con sol no se ven estrellas)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color("8d97ab")  # luz de relleno fria: suelo iluminado y luz de la Tierra
	e.ambient_light_energy = 0.32
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	e.tonemap_exposure = 1.0
	e.glow_enabled = true
	e.glow_intensity = 0.3
	e.glow_hdr_threshold = 1.2
	e.adjustment_enabled = true
	e.adjustment_contrast = 1.08
	e.adjustment_saturation = 0.9
	entorno.environment = e
	add_child(entorno)


func _montar_etapa() -> void:
	var mat := _material(FACETADO)
	var etapa := MeshInstance3D.new()
	etapa.name = "Etapa_descenso"
	etapa.mesh = Piezas.etapa_descenso()
	etapa.material_override = mat
	etapa.position = Vector3(0.0, terreno.altura(0.0, 0.0), 0.0)
	add_child(etapa)
	var poste := MeshInstance3D.new()
	poste.name = "Marcador_1_05m"
	poste.mesh = Piezas.marcador()
	poste.material_override = mat
	poste.position = Vector3(MARCADOR.x, terreno.altura(MARCADOR.x, MARCADOR.y), MARCADOR.y)
	add_child(poste)
	cuenta["triangulos_etapa"] = etapa.mesh.get_faces().size() / 3
	cuenta["alto_marcador"] = poste.mesh.get_aabb().size.y


func _montar_rocas() -> int:
	# 3 formas de roca; cada forma se reparte en un MultiMesh por bloque del terreno (8 x 8) para que la
	# camara descarte los bloques que no ve
	var rng := RandomNumberGenerator.new()
	rng.seed = SEMILLA + 3
	var formas := [Piezas.roca(rng, 0.50), Piezas.roca(rng, 0.44), Piezas.roca(rng, 0.56)]
	var mat := _material(FACETADO)
	for f in formas:
		f.surface_set_material(0, mat)
	var grandes := []
	for cr in terreno.crateres:
		if cr[2] >= 4.0:
			grandes.append(cr)
	var grupos := {}
	var puestas := 0
	var intentos := 0
	while puestas < ROCAS and intentos < ROCAS * 20:
		intentos += 1
		var p: Vector2
		var tirada := rng.randf()
		if tirada < 0.5:
			# 50 %: cerca del sitio, hasta 40 m (donde mas se mira)
			p = Vector2.from_angle(rng.randf() * TAU) * sqrt(rng.randf()) * 40.0
		elif tirada < 0.65:
			# 15 %: de 40 a 90 m, cubre el anillo de 75 m
			p = Vector2.from_angle(rng.randf() * TAU) * sqrt(lerpf(0.2, 1.0, rng.randf())) * 90.0
		else:
			# 35 %: eyecta en el borde de los crateres de 4 m de radio o mas
			var cr: Array = grandes[rng.randi() % grandes.size()]
			p = Vector2(cr[0], cr[1]) + Vector2.from_angle(rng.randf() * TAU) * float(cr[2]) * rng.randf_range(0.85, 1.8)
		if absf(p.x) > Terreno.LADO * 0.5 - 1.0 or absf(p.y) > Terreno.LADO * 0.5 - 1.0:
			continue
		if p.length() < 5.6 or p.distance_to(MARCADOR) < 0.8:
			continue  # sin rocas bajo la etapa de descenso ni pegadas al marcador
		# tamanos en ley de potencia: mediana de unos 0,17 m, las mayores de 1,4 m
		var s := 0.1 * pow(1.0 - rng.randf() * 0.97, -0.75)
		var base := Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3(s, s * rng.randf_range(0.6, 1.0), s))
		var xf := Transform3D(base, Vector3(p.x, terreno.altura(p.x, p.y) - 0.08 * s, p.y))
		var bloque := Terreno.LADO / Terreno.BLOQUES
		var clave := Vector3i(int((p.x + Terreno.LADO * 0.5) / bloque), int((p.y + Terreno.LADO * 0.5) / bloque), rng.randi() % formas.size())
		if not grupos.has(clave):
			grupos[clave] = []
		grupos[clave].append(xf)
		puestas += 1
	for clave in grupos:
		var lista: Array = grupos[clave]
		var mm := MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.mesh = formas[clave.z]
		mm.instance_count = lista.size()
		for i in lista.size():
			mm.set_instance_transform(i, lista[i])
		var mmi := MultiMeshInstance3D.new()
		mmi.name = "Rocas_%d_%d_%d" % [clave.x, clave.y, clave.z]
		mmi.multimesh = mm
		mmi.extra_cull_margin = 2.0
		add_child(mmi)
	cuenta["lotes_rocas"] = grupos.size()
	return puestas


func _montar_tierra() -> void:
	var esfera := SphereMesh.new()
	var radio := TIERRA_DISTANCIA * tan(deg_to_rad(TIERRA_DIAMETRO_DEG * 0.5))
	esfera.radius = radio
	esfera.height = radio * 2.0
	esfera.radial_segments = 48
	esfera.rings = 24
	var mat := ShaderMaterial.new()
	mat.shader = TIERRA
	esfera.material = mat
	tierra.name = "Tierra"
	tierra.mesh = esfera
	tierra.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(tierra)


func _colocar_camara() -> void:
	if vista == "cielo":
		# vista baja desde el este de la etapa de descenso, mirando al oeste: la Tierra sobre el sitio
		_ajustar("inclinacion", 0.0)
		camara.fov = 72.0
		var pos := Vector3(24.0, terreno.altura(24.0, 6.0) + 1.6, 6.0)
		var mira := direccion(TIERRA_AZIMUT, 33.0)
		camara.look_at_from_position(pos, pos + mira, Vector3.UP)
		camara.far = 2000.0
		sol.directional_shadow_max_distance = 120.0
	else:
		_ajustar("inclinacion", inclinacion)
		camara.fov = CAMARA["fov_deg"]
		var inclinacion_cam := deg_to_rad(CAMARA["inclinacion_deg"])
		var fraccion := float(CAMARA["encuadres"][encuadre])
		var alto := float(CAMARA["alto_personaje"])
		var factor := cos(inclinacion_cam) + inclinacion * sin(inclinacion_cam)
		var distancia := alto * factor / (2.0 * fraccion * tan(deg_to_rad(camara.fov * 0.5))) * zoom
		var foco := objetivo + Vector3(0.0, alto * 0.5, -inclinacion * alto * 0.5)
		var dir := Vector3(0.0, sin(inclinacion_cam), cos(inclinacion_cam))
		camara.look_at_from_position(foco + dir * distancia, foco, Vector3.UP)
		camara.far = maxf(distancia * 4.0, TIERRA_DISTANCIA + 50.0)
		sol.directional_shadow_max_distance = clampf(distancia * 4.0, 40.0, 300.0)
	# la Tierra acompana a la camara: esta tan lejos que no debe cambiar de lugar al caminar
	tierra.global_position = camara.global_position + direccion(TIERRA_AZIMUT, TIERRA_ALTURA) * TIERRA_DISTANCIA


func _interfaz() -> void:
	if captura != "" or medir > 0.0:
		return
	var capa := CanvasLayer.new()
	add_child(capa)
	etiqueta.position = Vector2(12, 8)
	etiqueta.add_theme_color_override("font_color", Color("f3e6cb"))
	etiqueta.add_theme_color_override("font_outline_color", Color("2f2a24"))
	etiqueta.add_theme_constant_override("outline_size", 6)
	capa.add_child(etiqueta)


func _process(delta: float) -> void:
	if captura != "" or medir > 0.0:
		return
	var mover := Vector3.ZERO
	if Input.is_action_pressed("ui_left"):
		mover.x -= 1
	if Input.is_action_pressed("ui_right"):
		mover.x += 1
	if Input.is_action_pressed("ui_up"):
		mover.z -= 1
	if Input.is_action_pressed("ui_down"):
		mover.z += 1
	if mover != Vector3.ZERO:
		objetivo += mover.normalized() * delta * 6.0 * zoom
		objetivo.y = terreno.altura(objetivo.x, objetivo.z)
		_colocar_camara()
	etiqueta.text = "Luna (prueba)  ·  encuadre %s %%  ·  zoom %.2f  ·  vista %s  ·  %d fps  ·  %d prim  ·  %d llamadas\nflechas mover · rueda alejar · 1/2 encuadre · C cielo · F12 captura · Esc salir" % [
		"21" if encuadre == "21" else "12,5", zoom, vista, Engine.get_frames_per_second(),
		Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME),
		Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)]


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("ui_cancel"):
		get_tree().quit()
	elif evento is InputEventKey and evento.pressed and not evento.echo:
		match evento.keycode:
			KEY_1:
				encuadre = "21"
				_colocar_camara()
			KEY_2:
				encuadre = "12"
				_colocar_camara()
			KEY_C:
				vista = "juego" if vista == "cielo" else "cielo"
				_colocar_camara()
			KEY_F12:
				var ruta := ProjectSettings.globalize_path("res://capturas/captura_%d.png" % Time.get_unix_time_from_system())
				_guardar(ruta)
	elif evento is InputEventMouseButton and evento.pressed:
		if evento.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom = maxf(zoom * 0.9, 0.35)
			_colocar_camara()
		elif evento.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom = minf(zoom * 1.1, 40.0)
			_colocar_camara()


func _medir() -> void:
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	var fin := Time.get_ticks_msec() + 2000
	while Time.get_ticks_msec() < fin:  # calentar: compilacion de shaders y sombras
		await get_tree().process_frame
	var tiempos: Array[float] = []
	var anterior := Time.get_ticks_usec()
	fin = Time.get_ticks_msec() + int(medir * 1000.0)
	var prims := 0.0
	var llamadas := 0.0
	while Time.get_ticks_msec() < fin:
		await get_tree().process_frame
		var ahora := Time.get_ticks_usec()
		tiempos.append((ahora - anterior) / 1000.0)
		anterior = ahora
		prims = Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)
		llamadas = Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	tiempos.sort()
	var suma := 0.0
	for t in tiempos:
		suma += t
	var media := suma / tiempos.size()
	var p95: float = tiempos[int(tiempos.size() * 0.95)]
	print("MEDIDA vista=%s encuadre=%s zoom=%.2f lod=%s rocas=%d cuadros=%d fps_medio=%.1f ms_medio=%.2f ms_p95=%.2f primitivas=%d llamadas=%d resolucion=%s" % [
		vista, encuadre, zoom, "no" if sin_lod else "si", cuenta["rocas"], tiempos.size(), 1000.0 / media, media, p95,
		int(prims), int(llamadas), str(get_viewport().get_visible_rect().size)])


func _guardar_mapa(ruta: String) -> void:
	var minimo := INF
	var maximo := -INF
	for h in terreno.alturas:
		minimo = minf(minimo, h)
		maximo = maxf(maximo, h)
	var datos := PackedByteArray()
	datos.resize(terreno.alturas.size())
	for k in terreno.alturas.size():
		datos[k] = int(255.0 * (terreno.alturas[k] - minimo) / (maximo - minimo))
	var imagen := Image.create_from_data(terreno.n, terreno.n, false, Image.FORMAT_L8, datos)
	imagen.save_png(ruta)
	print("ESCENA mapa=%s altura_min=%.2f altura_max=%.2f" % [ruta, minimo, maximo])


func _guardar(ruta: String) -> void:
	var imagen := get_viewport().get_texture().get_image()
	imagen.save_png(ruta)
	print("CAPTURA_OK ", ruta)
