extends SceneTree

# Prueba reproducible con tiempo de shader y pose del gato controlados.
var escena: Node3D
var version := "despues"
var fallos := 0
var follaje: Array[ShaderMaterial] = []


func _initialize() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--prueba_version="):
			version = arg.trim_prefix("--prueba_version=")
	call_deferred("_ejecutar")


func _exigir(condicion: bool, mensaje: String) -> void:
	if not condicion:
		fallos += 1
		push_error("PRUEBA_FALLO " + mensaje)


func _ejecutar() -> void:
	var ruta := "res://capturas/multimesh/escena_antes.gd.txt" if version == "antes" else "res://escena.gd"
	var programa := GDScript.new()
	programa.source_code = FileAccess.get_file_as_string(ruta)
	_exigir(programa.reload() == OK, "compilacion")
	escena = programa.new()
	root.add_child(escena)
	escena.set_process(false)
	for hijo in escena.get_children():
		if hijo is CanvasLayer:
			hijo.hide()
	await process_frame
	var gato: Node3D = escena.instancias["PER-09"]
	var reproductor := gato.find_child("AnimationPlayer", true, false) as AnimationPlayer
	_exigir(reproductor.is_playing() and reproductor.current_animation == "caminar", "gato animado")
	reproductor.speed_scale = 0.0
	reproductor.seek(0.25, true)
	if version == "despues":
		_verificar_lotes()
	var base: Node3D = escena.instancias["roca_iguana"]
	_exigir(is_equal_approx(escena.instancias["FAU-01"].position.y, Materiales.caja_mundo(base).end.y - 0.06), "apoyo iguana")
	var shaders := {}
	for material in Materiales.creados:
		var original := material.shader
		if not shaders.has(original):
			var shader := Shader.new()
			var codigo := original.code
			if original.resource_path.ends_with("follaje.gdshader"):
				codigo = codigo.replace("TIME", "tiempo_prueba")
				codigo = codigo.replace("void vertex()", "uniform float tiempo_prueba = 0.25;\n\nvoid vertex()")
			else:
				codigo = codigo.replace("TIME", "float(0.25)")
			shader.code = codigo
			shaders[original] = shader
		if original.resource_path.ends_with("follaje.gdshader"):
			follaje.append(material)
		material.shader = shaders[original]
	for e in ["21", "12"]:
		escena.encuadre = e
		escena._colocar_camara()
		Materiales.ajustar_parametro("inclinacion", 0.45)
		for m in follaje:
			m.set_shader_parameter("tiempo_prueba", 0.25)
		await _capturar("%s_%s_fijo" % [version, e])
		for m in follaje:
			m.set_shader_parameter("tiempo_prueba", 1.25)
		await _capturar("%s_%s_viento" % [version, e])
		for m in follaje:
			m.set_shader_parameter("tiempo_prueba", 0.25)
		Materiales.ajustar_parametro("inclinacion", 0.0)
		await _capturar("%s_%s_sin_inclinacion" % [version, e])
	_verificar_controles()
	print("PRUEBA version=%s fallos=%d materiales_follaje=%d" % [version, fallos, follaje.size()])
	quit(1 if fallos else 0)


func _capturar(nombre: String) -> void:
	for i in range(12):
		await process_frame
	await RenderingServer.frame_post_draw
	escena._guardar(ProjectSettings.globalize_path("res://capturas/multimesh/%s.png" % nombre))


func _verificar_lotes() -> void:
	var grupos := {}
	for r in escena.datos["recursos"]:
		if not escena.instancias.has(r["id"]):
			continue
		var nodo: Node3D = escena.instancias[r["id"]]
		if r.has("animacion") or r.has("variante"):
			for mi in nodo.find_children("*", "MeshInstance3D", true, false):
				_exigir(mi.visible, "excepcion " + r["id"])
			continue
		var clave := JSON.stringify([r["glb"], r.get("nodo", "")])
		if not grupos.has(clave):
			grupos[clave] = []
		grupos[clave].append(nodo)
	var transformaciones := 0
	var lotes := 0
	for grupo in grupos.values():
		var primero: Node3D = grupo[0]
		for mi in primero.find_children("*", "MeshInstance3D", true, false):
			if grupo.size() == 1:
				_exigir(mi.visible, "recurso unico " + primero.name)
				continue
			var lote := escena.get_node("Multimesh_%s_%s" % [primero.name, mi.name]) as MultiMeshInstance3D
			_exigir(lote != null, "lote " + primero.name)
			if lote == null:
				continue
			lotes += 1
			_exigir(lote.multimesh.instance_count == grupo.size(), "cantidad " + lote.name)
			_exigir(lote.cast_shadow == mi.cast_shadow, "sombras " + lote.name)
			for s in mi.mesh.get_surface_count():
				_exigir(lote.multimesh.mesh.surface_get_material(s) == mi.get_active_material(s), "material " + lote.name)
			for i in grupo.size():
				var original := grupo[i].get_node(primero.get_path_to(mi)) as MeshInstance3D
				_exigir(not original.visible, "malla individual oculta")
				_exigir((lote.global_transform * lote.multimesh.get_instance_transform(i)).is_equal_approx(original.global_transform), "transformacion " + grupo[i].name)
				transformaciones += 1
	print("PRUEBA_LOTES lotes=%d transformaciones=%d" % [lotes, transformaciones])


func _verificar_controles() -> void:
	var evento := InputEventKey.new()
	evento.pressed = true
	evento.keycode = KEY_I
	escena._unhandled_input(evento)
	_exigir(is_zero_approx(escena.inclinacion), "tecla I desactiva cizalla")
	escena._unhandled_input(evento)
	_exigir(is_equal_approx(escena.inclinacion, 0.45), "tecla I activa cizalla")
	for material in Materiales.creados:
		_exigir(is_equal_approx(float(material.get_shader_parameter("inclinacion")), 0.45), "parametro compartido")
	var antena: Node3D = escena.instancias["COL-01_tripo"]
	evento.keycode = KEY_A
	escena._unhandled_input(evento)
	_exigir(not antena.visible, "tecla A oculta antena tripo")
	escena._unhandled_input(evento)
	_exigir(antena.visible, "tecla A restaura antena tripo")
	evento.keycode = KEY_1
	escena._unhandled_input(evento)
	_exigir(escena.encuadre == "21", "tecla 1")
	evento.keycode = KEY_2
	escena._unhandled_input(evento)
	_exigir(escena.encuadre == "12", "tecla 2")
	print("PRUEBA_CONTROLES inclinacion=OK antena_tripo=OK encuadres=OK")
