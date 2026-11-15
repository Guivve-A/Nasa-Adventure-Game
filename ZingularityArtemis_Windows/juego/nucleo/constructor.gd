extends RefCounted

# Arma una escena a partir de un layout en JSON, con el mismo formato que la escena aprobada del sendero
# (pruebas/escena_exploracion/layout.json, escrito por herramientas/mallas/escena_v1.py):
#   {"ambiente": {"moteado": {...}, "pinceladas": 0.7},
#    "recursos": [{"id", "glb", "pos": [x, y, z], "rot_y", "escala", y opcionales "nodo", "altura", "escala_y",
#                  "variante", "animacion", "sobre", "oculto"}]}
# Las rutas "glb" son relativas a la carpeta "base". Los recursos repetidos se agrupan en MultiMesh
# (252 -> 58 llamadas de dibujo en el sendero). Portado de pruebas/escena_exploracion/escena.gd.

const Materiales := preload("res://nucleo/materiales.gd")
const Recursos := preload("res://nucleo/recursos.gd")


static func montar(padre: Node3D, datos: Dictionary, base: String, omitir: Array = []) -> Dictionary:
	# devuelve {"instancias": {id: Node3D}, "faltan": [rutas], "recursos": n}
	var instancias := {}
	var faltan: Array = []
	var pendientes_sobre: Array = []
	for r in datos.get("recursos", []):
		if omitir.has(r["id"]) or r.get("oculto", false):
			continue
		var ruta: String = base.path_join(r["glb"])
		var plantilla := Recursos.plantilla(ruta)
		if plantilla == null:
			if not faltan.has(r["glb"]):
				faltan.append(r["glb"])
			continue
		var nodo: Node3D = plantilla.duplicate()
		if r.has("nodo"):
			# del GLB con varias variantes se queda solo la pedida
			for hijo in nodo.get_children():
				if hijo.name != r["nodo"] and not String(hijo.name).begins_with(r["nodo"]):
					hijo.queue_free()
		padre.add_child(nodo)
		if r.has("altura"):
			nodo = normalizar_altura(padre, nodo, float(r["altura"]))
		nodo.rotation.y = deg_to_rad(float(r.get("rot_y", 0.0)))
		nodo.scale *= float(r.get("escala", 1.0))
		if r.has("escala_y"):
			nodo.scale.y *= float(r["escala_y"])
		nodo.position = Vector3(r["pos"][0], r["pos"][1], r["pos"][2])
		nodo.name = r["id"]
		if r.has("variante"):
			nodo.set_meta("variante", r["variante"])
		if r.has("animacion"):
			reproducir(nodo, r["animacion"])
		instancias[r["id"]] = nodo
		if r.has("sobre"):
			pendientes_sobre.append([nodo, r["sobre"]])
	for par in pendientes_sobre:
		var apoyo: Node3D = instancias.get(par[1])
		if apoyo != null:
			var caja := Materiales.caja_mundo(apoyo)
			par[0].position.y = caja.end.y - 0.06
	_agrupar_repetidos(padre, datos, instancias, omitir)
	return {"instancias": instancias, "faltan": faltan, "recursos": instancias.size()}


static func normalizar_altura(padre: Node3D, nodo: Node3D, altura: float) -> Node3D:
	# escala la malla a "altura" metros, apoya su base en y = 0 y la centra; devuelve el pivote que la envuelve
	var caja := Materiales.caja_mundo(nodo)
	if caja.size.y > 0.0:
		nodo.scale = Vector3.ONE * altura / caja.size.y
	caja = Materiales.caja_mundo(nodo)
	var origen := padre.global_position
	nodo.position -= Vector3(caja.get_center().x, caja.position.y, caja.get_center().z) - origen
	var pivote := Node3D.new()
	padre.remove_child(nodo)
	pivote.add_child(nodo)
	padre.add_child(pivote)
	return pivote


static func reproducir(nodo: Node3D, animacion: String, velocidad: float = 1.0) -> AnimationPlayer:
	# glTF no guarda la repeticion: se activa aqui
	var reproductor := nodo.find_child("AnimationPlayer", true, false) as AnimationPlayer
	if reproductor != null and reproductor.has_animation(animacion):
		reproductor.get_animation(animacion).loop_mode = Animation.LOOP_LINEAR
		reproductor.play(animacion)
		reproductor.speed_scale = velocidad
	return reproductor


static func aplicar_ambiente(datos: Dictionary) -> void:
	# sombra moteada del arbol y pinceladas (layout.json -> ambiente), en todos los shaders de la zona
	var amb: Dictionary = datos.get("ambiente", {})
	if amb.has("pinceladas"):
		Materiales.ajustar_parametro("pinceladas", float(amb["pinceladas"]))
	if amb.has("moteado"):
		var m: Dictionary = amb["moteado"]
		Materiales.ajustar_parametro("moteado_centro", Vector2(m["centro"][0], m["centro"][1]))
		Materiales.ajustar_parametro("moteado_radios", Vector2(m["radios"][0], m["radios"][1]))
		Materiales.ajustar_parametro("moteado_fuerza", float(m.get("fuerza", 1.0)))
		Materiales.ajustar_parametro("moteado_sombra", float(m.get("sombra", 0.4)))


static func _agrupar_repetidos(padre: Node3D, datos: Dictionary, instancias: Dictionary, omitir: Array) -> void:
	var grupos := {}
	for r in datos.get("recursos", []):
		if r.has("animacion") or r.has("variante") or r.get("suelto", false) or not instancias.has(r["id"]) or omitir.has(r["id"]):
			continue
		var clave := JSON.stringify([r["glb"], r.get("nodo", "")])
		if not grupos.has(clave):
			grupos[clave] = []
		grupos[clave].append(instancias[r["id"]])
	for grupo in grupos.values():
		if grupo.size() < 2:
			continue
		var primero: Node3D = grupo[0]
		for hijo in primero.find_children("*", "MeshInstance3D", true, false):
			var origen := hijo as MeshInstance3D
			# las variantes descartadas con queue_free aun existen durante este cuadro
			var rama: Node = origen
			while rama != primero and not rama.is_queued_for_deletion():
				rama = rama.get_parent()
			if rama != primero or origen.mesh == null:
				continue
			_crear_multimesh(padre, grupo, origen)


static func _crear_multimesh(padre: Node3D, grupo: Array, origen: MeshInstance3D) -> void:
	# MultiMesh usa los materiales de la malla, no los overrides de MeshInstance3D:
	# se copia la malla y se comparten los ShaderMaterial ya registrados
	var malla := origen.mesh.duplicate() as Mesh
	for superficie in malla.get_surface_count():
		malla.surface_set_material(superficie, origen.get_active_material(superficie))
	var multiples := MultiMesh.new()
	multiples.transform_format = MultiMesh.TRANSFORM_3D
	multiples.mesh = malla
	multiples.instance_count = grupo.size()
	var primero: Node3D = grupo[0]
	var ruta := primero.get_path_to(origen)
	var inversa := padre.global_transform.affine_inverse()
	var cizalla := float(Materiales.parametros.get("inclinacion", 0.45))
	var inclinar := Transform3D(Basis(Vector3.RIGHT, Vector3(0.0, 1.0, -cizalla), Vector3.BACK), Vector3.ZERO)
	var caja := AABB()
	for i in grupo.size():
		var original := grupo[i].get_node(ruta) as MeshInstance3D
		multiples.set_instance_transform(i, inversa * original.global_transform)
		# la caja cubre la inclinacion del shader y el viento del follaje
		var limite := original.global_transform * malla.get_aabb()
		limite = limite.merge(inclinar * limite)
		var balanceo := Vector3(0.035, 0.0, 0.0175) * maxf(limite.end.y, 0.0)
		limite.position -= balanceo
		limite.size += balanceo * 2.0
		limite = inversa * limite
		caja = limite if i == 0 else caja.merge(limite)
		# los nodos originales se conservan (invisibles) para colisiones y referencias
		original.visible = false
	multiples.custom_aabb = caja
	var lote := MultiMeshInstance3D.new()
	lote.name = "Multimesh_%s_%s" % [primero.name, origen.name]
	lote.multimesh = multiples
	lote.cast_shadow = origen.cast_shadow
	padre.add_child(lote)
