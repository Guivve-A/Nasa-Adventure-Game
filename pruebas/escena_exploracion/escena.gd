extends Node3D

# Escena de exploracion v1: arma la vista aprobada del sendero a partir de layout.json.
# Argumentos tras "--":
#   --captura=<png>         guarda una captura y sale
#   --encuadre=21|12        personaje al 21 % (como el ancla) o al 12,5 % (como la biblia) del alto
#   --antena=tripo|script   que version de la antena COL-01 se muestra
#   --sin_inclinacion       sin echar los objetos hacia atras (para comparar)
#   --medir=<s>             sin vsync: mide fps, ms por cuadro (media y p95), triangulos y llamadas de dibujo
#   --objetivo=x,z  --zoom=<f>   centra la camara en un punto y la acerca (zoom < 1)
#   --pintado=<0..1>        acabado 2.5D de los personajes (1, por defecto) o luz 3D celular (0)
#   --rot=<id>:<grados>     gira un recurso del layout (por ejemplo, la protagonista hacia la camara)
# Teclas: 1 y 2 encuadre, I inclinacion, A antena, flechas mueven la camara, rueda acerca, F12 captura, Esc sale.

const LAYOUT := "res://layout.json"

var datos: Dictionary
var camara := Camera3D.new()
var objetivo := Vector3.ZERO
var encuadre := "21"
var antena := "script"  # iteracion 4 del ajuste al ancla: la de script se parece mas (dE 22,1 contra 24,1 en su zona)
var inclinacion := 0.55
var captura := ""
var zoom := 1.0
var instancias := {}
var plantillas := {}
var etiqueta := Label.new()
var cuenta := {"recursos": 0, "faltan": [], "triangulos": 0}
var medir := 0.0
var objetivo_forzado := Vector3.INF
var pintado := 1.0
var giros := {}


func _ready() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--captura="):
			captura = arg.trim_prefix("--captura=")
		elif arg.begins_with("--encuadre="):
			encuadre = arg.trim_prefix("--encuadre=")
		elif arg.begins_with("--antena="):
			antena = arg.trim_prefix("--antena=")
		elif arg == "--sin_inclinacion":
			inclinacion = 0.0
		elif arg.begins_with("--medir="):
			medir = float(arg.trim_prefix("--medir="))
		elif arg.begins_with("--objetivo="):
			var xz := arg.trim_prefix("--objetivo=").split(",")
			objetivo_forzado = Vector3(float(xz[0]), 0.0, float(xz[1]))
		elif arg.begins_with("--zoom="):
			zoom = float(arg.trim_prefix("--zoom="))  # < 1 acerca la camara
		elif arg.begins_with("--pintado="):
			pintado = float(arg.trim_prefix("--pintado="))  # 1 = acabado 2.5D de los personajes, 0 = luz 3D
		elif arg.begins_with("--rot="):
			var par := arg.trim_prefix("--rot=").split(":")  # --rot=PER-01:-120 gira un recurso
			giros[par[0]] = float(par[1])
	datos = JSON.parse_string(FileAccess.get_file_as_string(LAYOUT))
	Iluminacion.montar(self)
	add_child(camara)
	var c: Dictionary = datos["camara"]
	camara.fov = float(c["fov_deg"])
	objetivo = Vector3(c["objetivo"][0], c["objetivo"][1], c["objetivo"][2])
	if objetivo_forzado != Vector3.INF:
		objetivo = objetivo_forzado
	if inclinacion > 0.0:
		inclinacion = float(c.get("inclinacion_objetos", inclinacion))
	_montar_recursos()
	Materiales.ajustar_parametro("inclinacion", inclinacion)
	Materiales.ajustar_parametro("pintado", pintado)
	_aplicar_ambiente()
	_mostrar_antena()
	_colocar_camara()
	_interfaz()
	print("ESCENA recursos=%d triangulos=%d faltan=%s" % [cuenta["recursos"], cuenta["triangulos"], str(cuenta["faltan"])])
	if medir > 0.0:
		await _medir()
		get_tree().quit()
		return
	if captura != "":
		for i in range(40):
			await get_tree().process_frame
		_guardar(captura)
		get_tree().quit()


func _plantilla(ruta: String) -> Node3D:
	if plantillas.has(ruta):
		return plantillas[ruta]
	var completa := "res://" + ruta
	if not FileAccess.file_exists(completa):
		plantillas[ruta] = null
		return null
	var nodo := Materiales.cargar_glb(completa)
	if nodo != null:
		var info := Materiales.aplicar(nodo)
		nodo.set_meta("triangulos", info["triangulos"])
	plantillas[ruta] = nodo
	return nodo


func _montar_recursos() -> void:
	var pendientes_sobre := []
	for r in datos["recursos"]:
		var plantilla := _plantilla(r["glb"])
		if plantilla == null:
			if not cuenta["faltan"].has(r["glb"]):
				cuenta["faltan"].append(r["glb"])
			continue
		var nodo: Node3D = plantilla.duplicate()
		if r.has("nodo"):
			# del GLB con varias variantes se queda solo la pedida
			for hijo in nodo.get_children():
				if hijo.name != r["nodo"] and not String(hijo.name).begins_with(r["nodo"]):
					hijo.queue_free()
		add_child(nodo)
		if r.has("altura"):
			var caja := Materiales.caja_mundo(nodo)
			if caja.size.y > 0.0:
				nodo.scale = Vector3.ONE * float(r["altura"]) / caja.size.y
			caja = Materiales.caja_mundo(nodo)
			nodo.position -= Vector3(caja.get_center().x, caja.position.y, caja.get_center().z)
			var pivote := Node3D.new()
			remove_child(nodo)
			pivote.add_child(nodo)
			add_child(pivote)
			nodo = pivote
		nodo.rotation.y = deg_to_rad(float(giros.get(r["id"], r["rot_y"])))
		nodo.scale *= float(r["escala"])
		if r.has("escala_y"):
			nodo.scale.y *= float(r["escala_y"])  # p. ej. el flamboyan en paraguas, mas bajo que el modelo
		nodo.position = Vector3(r["pos"][0], r["pos"][1], r["pos"][2])
		nodo.name = r["id"]
		if r.has("variante"):
			nodo.set_meta("variante", r["variante"])
		if r.has("animacion"):
			# glTF no guarda la repeticion: se activa aqui
			var reproductor := nodo.find_child("AnimationPlayer", true, false) as AnimationPlayer
			if reproductor != null and reproductor.has_animation(r["animacion"]):
				reproductor.get_animation(r["animacion"]).loop_mode = Animation.LOOP_LINEAR
				reproductor.play(r["animacion"])
		instancias[r["id"]] = nodo
		cuenta["recursos"] += 1
		cuenta["triangulos"] += int(plantilla.get_meta("triangulos", 0))
		if r.has("sobre"):
			pendientes_sobre.append([nodo, r["sobre"]])
	for par in pendientes_sobre:
		var base: Node3D = instancias.get(par[1])
		if base != null:
			var caja := Materiales.caja_mundo(base)
			par[0].position.y = caja.end.y - 0.06
	_agrupar_repetidos()


func _agrupar_repetidos() -> void:
	var grupos := {}
	for r in datos["recursos"]:
		if r.has("animacion") or r.has("variante") or not instancias.has(r["id"]):
			continue
		var clave := JSON.stringify([r["glb"], r.get("nodo", "")])
		if not grupos.has(clave):
			grupos[clave] = []
		grupos[clave].append(instancias[r["id"]])
	var recursos := 0
	var lotes := 0
	for grupo in grupos.values():
		if grupo.size() < 2:
			continue
		recursos += grupo.size()
		var primero: Node3D = grupo[0]
		for hijo in primero.find_children("*", "MeshInstance3D", true, false):
			var origen := hijo as MeshInstance3D
			# Las variantes descartadas con queue_free aun existen durante este cuadro.
			var rama: Node = origen
			while rama != primero and not rama.is_queued_for_deletion():
				rama = rama.get_parent()
			if rama != primero or origen.mesh == null:
				continue
			_crear_multimesh(grupo, origen)
			lotes += 1
	print("MULTIMESH recursos=%d lotes=%d" % [recursos, lotes])


func _crear_multimesh(grupo: Array, origen: MeshInstance3D) -> void:
	# MultiMesh usa los materiales de la malla, no los overrides de MeshInstance3D.
	# Se copia solo la malla y se comparten los ShaderMaterial ya registrados.
	var malla := origen.mesh.duplicate() as Mesh
	for superficie in malla.get_surface_count():
		malla.surface_set_material(superficie, origen.get_active_material(superficie))
	var multiples := MultiMesh.new()
	multiples.transform_format = MultiMesh.TRANSFORM_3D
	multiples.mesh = malla
	multiples.instance_count = grupo.size()
	var primero: Node3D = grupo[0]
	var ruta := primero.get_path_to(origen)
	var inversa := global_transform.affine_inverse()
	var cizalla := maxf(inclinacion, float(datos["camara"].get("inclinacion_objetos", 0.45)))
	var inclinar := Transform3D(Basis(Vector3.RIGHT, Vector3(0.0, 1.0, -cizalla), Vector3.BACK), Vector3.ZERO)
	var caja := AABB()
	for i in grupo.size():
		var original := grupo[i].get_node(ruta) as MeshInstance3D
		# Incluye pivotes, altura normalizada, escala, rotacion y apoyo ya resuelto.
		multiples.set_instance_transform(i, inversa * original.global_transform)
		# Cubre ambas posiciones de la tecla I y el viento del shader de follaje.
		var limite := original.global_transform * malla.get_aabb()
		limite = limite.merge(inclinar * limite)
		var balanceo := Vector3(0.035, 0.0, 0.0175) * maxf(limite.end.y, 0.0)
		limite.position -= balanceo
		limite.size += balanceo * 2.0
		limite = inversa * limite
		caja = limite if i == 0 else caja.merge(limite)
		# Se conservan los nodos y sus cajas para las referencias de instancias.
		original.visible = false
	multiples.custom_aabb = caja
	var lote := MultiMeshInstance3D.new()
	lote.name = "Multimesh_%s_%s" % [primero.name, origen.name]
	lote.multimesh = multiples
	lote.cast_shadow = origen.cast_shadow
	lote.layers = origen.layers
	lote.material_overlay = origen.material_overlay
	lote.extra_cull_margin = origen.extra_cull_margin
	add_child(lote)


func _mostrar_antena() -> void:
	for nodo in instancias.values():
		if nodo.has_meta("variante"):
			nodo.visible = nodo.get_meta("variante") == antena


func _aplicar_ambiente() -> void:
	# sombra moteada del flamboyan (layout.json -> ambiente.moteado), en todos los shaders de la escena
	var amb: Dictionary = datos.get("ambiente", {})
	if pintado <= 0.0:
		return
	if amb.has("pinceladas"):
		Materiales.ajustar_parametro("pinceladas", float(amb["pinceladas"]))  # textura pintada 2D-HD
	if not amb.has("moteado"):
		return
	var m: Dictionary = amb["moteado"]
	Materiales.ajustar_parametro("moteado_centro", Vector2(m["centro"][0], m["centro"][1]))
	Materiales.ajustar_parametro("moteado_radios", Vector2(m["radios"][0], m["radios"][1]))
	Materiales.ajustar_parametro("moteado_fuerza", float(m["fuerza"]))
	Materiales.ajustar_parametro("moteado_sombra", float(m["sombra"]))


func _colocar_camara() -> void:
	var c: Dictionary = datos["camara"]
	var inclinacion_cam := deg_to_rad(float(c["inclinacion_deg"]))
	var fraccion := float(c["encuadres"][encuadre])
	var alto := float(c["alto_personaje"])
	# con la inclinacion del shader, la vertical se ve casi a su altura real
	var factor := cos(inclinacion_cam) + inclinacion * sin(inclinacion_cam)
	var distancia := alto * factor / (2.0 * fraccion * tan(deg_to_rad(camara.fov * 0.5))) * zoom
	var foco := objetivo + Vector3(0.0, alto * 0.5, -inclinacion * alto * 0.5)
	var dir := Vector3(0.0, sin(inclinacion_cam), cos(inclinacion_cam))
	camara.look_at_from_position(foco + dir * distancia, foco, Vector3.UP)
	camara.far = distancia * 4.0


func _interfaz() -> void:
	if captura != "":
		return
	var capa := CanvasLayer.new()
	add_child(capa)
	etiqueta.position = Vector2(12, 8)
	etiqueta.add_theme_color_override("font_color", Color("f8c991"))
	etiqueta.add_theme_color_override("font_outline_color", Color("322c1d"))
	etiqueta.add_theme_constant_override("outline_size", 6)
	capa.add_child(etiqueta)


func _process(delta: float) -> void:
	if captura != "":
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
		objetivo += mover.normalized() * delta * 3.0
		_colocar_camara()
	etiqueta.text = "Encuadre %s %%  ·  inclinacion %s  ·  antena %s  ·  %d fps\n1/2 encuadre · I inclinacion · A antena · flechas mover · rueda acercar · F12 captura" % [
		"21" if encuadre == "21" else "12,5", "si" if inclinacion > 0.0 else "no", antena, Engine.get_frames_per_second()]


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
			KEY_I:
				inclinacion = 0.0 if inclinacion > 0.0 else float(datos["camara"].get("inclinacion_objetos", 0.45))
				Materiales.ajustar_parametro("inclinacion", inclinacion)
				_colocar_camara()
			KEY_A:
				antena = "script" if antena == "tripo" else "tripo"
				_mostrar_antena()
			KEY_F12:
				var ruta := ProjectSettings.globalize_path("res://capturas/captura_%d.png" % Time.get_unix_time_from_system())
				_guardar(ruta)
	elif evento is InputEventMouseButton and evento.pressed:
		if evento.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom = maxf(zoom * 0.9, 0.35)
			_colocar_camara()
		elif evento.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom = minf(zoom * 1.1, 3.0)
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
	print("MEDIDA encuadre=%s cuadros=%d fps_medio=%.1f ms_medio=%.2f ms_p95=%.2f primitivas=%d llamadas=%d resolucion=%s" % [
		encuadre, tiempos.size(), 1000.0 / media, media, p95, int(prims), int(llamadas), str(get_viewport().get_visible_rect().size)])


func _exit_tree() -> void:
	# las plantillas nunca entran al arbol: se liberan a mano para no dejar fugas al salir
	for p in plantillas.values():
		if p != null and is_instance_valid(p):
			p.free()
	plantillas.clear()
	Materiales.creados.clear()


func _guardar(ruta: String) -> void:
	var imagen := get_viewport().get_texture().get_image()
	imagen.save_png(ruta)
	print("CAPTURA_OK ", ruta)
