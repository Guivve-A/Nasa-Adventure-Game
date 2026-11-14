extends Node

# Pruebas automaticas del juego (sin ventana). Se corren con:
#   python -I herramientas/juego_ejecutar.py -- --prueba=<nombre> --ritmo=8
# Nombres: nucleo | zonas | zona:<id> | minijuegos | minijuego:<id> | recorrido
# Cada comprobacion imprime PRUEBA_OK o PRUEBA_FALLO; el envoltorio sale con 1 si hay algun fallo.

var fallos := 0
var hechas := 0


func comprobar(condicion: bool, nombre: String, detalle: String = "") -> bool:
	hechas += 1
	if condicion:
		print("PRUEBA_OK ", nombre)
	else:
		fallos += 1
		print("PRUEBA_FALLO ", nombre, (": " + detalle) if detalle != "" else "")
	return condicion


func correr(cual: String) -> void:
	var nombre := cual.get_slice(":", 0)
	var dato := cual.get_slice(":", 1) if cual.contains(":") else ""
	match nombre:
		"nucleo":
			await _nucleo()
		"zonas":
			await _zonas()
		"zona":
			await _zona(dato)
			await _enlaces([dato])
		"minijuegos":
			for m in Juego.catalogo_minijuegos():
				if String(m.get("zona", "")) == "":
					await _minijuego(m["id"])
		"minijuego":
			await _minijuego(dato)
		"recorrido":
			await _recorrido()
		"guion":
			# prueba propia de un carril: un guion con  func correr(pruebas: Node) -> void  que usa
			# pruebas.comprobar(condicion, nombre, detalle). Ejemplo: --prueba=guion:res://base/prueba_base.gd
			var ruta := cual.substr(cual.find(":") + 1)
			var guion: Variant = load(ruta) if ResourceLoader.exists(ruta) else null
			if comprobar(guion != null, "guion_de_prueba_existe", ruta):
				var nodo: Node = guion.new()
				add_child(nodo)
				await nodo.correr(self)
				nodo.queue_free()
		_:
			comprobar(false, "prueba_desconocida", cual)
	print("PRUEBAS hechas=%d fallos=%d" % [hechas, fallos])


func _esperar(segundos: float) -> void:
	await get_tree().create_timer(segundos).timeout


# ------------------------------------------------------------------ nucleo

func _nucleo() -> void:
	comprobar(not Zonas.catalogo(true).is_empty(), "catalogo_de_zonas")
	comprobar(not Juego.catalogo_minijuegos().is_empty(), "catalogo_de_minijuegos")
	comprobar(not Juego.fichas.is_empty(), "fichas_del_cuaderno", "datos/datos_espaciales.json vacio o ilegible")
	comprobar(not Juego.misiones.is_empty(), "misiones", "datos/misiones.json vacio o ilegible")
	Juego.nueva_partida()
	var llego: bool = await Zonas.ir_a("plantilla", "inicio")
	comprobar(llego and Zonas.actual != null, "ir_a_plantilla")
	if Zonas.actual == null:
		return
	await _esperar(0.6)
	var j: CharacterBody3D = Zonas.jugador
	comprobar(j != null and j.is_on_floor(), "protagonista_en_el_suelo", "y=%.2f" % (j.global_position.y if j != null else -99.0))
	comprobar(j.modelo != null, "modelo_de_la_protagonista_cargado")
	comprobar(Zonas.companero.modelo != null, "modelo_de_orbita_cargado")
	var ok: bool = await j.caminar_hasta(Vector3(2.0, 0.0, 1.0))
	comprobar(ok and j.global_position.distance_to(Vector3(2.0, j.global_position.y, 1.0)) < 0.5, "piloto_camina_hasta_un_punto", str(j.global_position))
	await Interfaz.decir(["Prueba de diálogo.", {"quien": "Órbita", "texto": "Miau."}])
	comprobar(not Interfaz.dialogo.visible, "dialogo_se_cierra")
	var elegido: int = await Interfaz.elegir("¿Seguimos?", ["Sí", "No"])
	comprobar(elegido == 0, "pregunta_con_opciones")
	var cartel: Node3D = Zonas.actual.get_node_or_null("Cartel")
	comprobar(cartel != null, "interactuable_existe")
	if cartel != null:
		await cartel.usar(j)
		comprobar(bool(Juego.bandera("plantilla_minijuego")), "minijuego_desde_la_zona", "la zona no puso la bandera tras el minijuego")
	Juego.poner_bandera("plantilla_paso_1")
	Juego.poner_bandera("plantilla_paso_2")
	comprobar(Juego.estado["misiones_hechas"].has("m_plantilla") or Juego.misiones.filter(func(m): return m.get("id") == "m_plantilla").is_empty(), "mision_se_completa")
	# cruza el umbral del fondo y vuelve a entrar por la otra entrada
	ok = await j.caminar_hasta(Vector3(0.0, 0.0, -4.2))
	await _esperar(1.2)
	comprobar(Zonas.id_actual == "plantilla" and j.global_position.z > 2.0, "umbral_cambia_de_entrada", "z=%.2f" % j.global_position.z)
	Zonas.cerrar()
	await _esperar(0.2)
	comprobar(Zonas.actual == null, "zona_cerrada")


# ------------------------------------------------------------------ zonas

var _entradas_por_zona := {}
var _destinos := []        # [zona origen, nombre del umbral, zona destino, entrada destino]


func _zonas() -> void:
	var ids: Array = []
	for z in Zonas.catalogo(true):
		ids.append(z["id"])
	for id in ids:
		await _zona(id)
	await _enlaces(ids)


func _zona(id: String) -> void:
	var meta := Zonas.info(id)
	for clave in ["nombre", "lugar", "momento", "estado_arte"]:
		comprobar(String(meta.get(clave, "")) != "", "%s.zona_json.%s" % [id, clave])
	Juego.nueva_partida()
	Juego.poner_bandera("visita_libre")
	var llego: bool = await Zonas.ir_a(id, "inicio")
	if not comprobar(llego and Zonas.actual != null, "%s.carga" % id):
		return
	var zona: Node3D = Zonas.actual
	var j: CharacterBody3D = Zonas.jugador
	var entradas: Dictionary = zona.entradas
	_entradas_por_zona[id] = entradas.keys()
	comprobar(entradas.has("inicio"), "%s.entrada_inicio" % id)
	var umbrales: Array = []
	for u in get_tree().get_nodes_in_group("umbrales"):
		if zona.is_ancestor_of(u):
			umbrales.append(u)
			_destinos.append([id, String(u.name), u.destino_zona, u.destino_entrada])
	comprobar(not umbrales.is_empty() or zona.has_method("despertar"), "%s.tiene_salida" % id, "la zona no tiene umbrales ni despertar()")
	# cada entrada: suelo firme, sitio despejado y lejos de caer en un umbral
	for nombre in entradas:
		var punto: Dictionary = entradas[nombre]
		j.colocar(punto["pos"] + Vector3(0.0, 0.05, 0.0), punto["mira"])
		await _esperar(0.5)
		var caida: float = absf(j.global_position.y - punto["pos"].y)
		comprobar(j.is_on_floor() and caida < 0.4, "%s.entrada_%s.suelo" % [id, nombre], "en_suelo=%s y=%.2f (pedida %.2f)" % [str(j.is_on_floor()), j.global_position.y, punto["pos"].y])
		var corrida: float = Vector2(j.global_position.x - punto["pos"].x, j.global_position.z - punto["pos"].z).length()
		comprobar(corrida < 0.25, "%s.entrada_%s.despejada" % [id, nombre], "algo la empuja %.2f m" % corrida)
		for u in umbrales:
			var d: float = Vector2(u.global_position.x - punto["pos"].x, u.global_position.z - punto["pos"].z).length()
			if absf(u.global_position.y - punto["pos"].y) < 1.2:
				comprobar(d > u.radio + 0.5, "%s.entrada_%s.lejos_de_%s" % [id, nombre, u.name], "a %.2f m: volveria a cruzar al llegar" % d)
	# cada umbral: tramo despejado de 2 x 2 m alrededor
	for u in umbrales:
		comprobar(_despejado(u.global_position, 0.85), "%s.umbral_%s.despejado" % [id, u.name], "hay colisiones a menos de 0,85 m de la marca")
	# recorrido de prueba de la zona
	var ruta: Array = zona.ruta_de_prueba()
	if not ruta.is_empty():
		var inicio: Dictionary = entradas.get("inicio", {"pos": Vector3.ZERO, "mira": Vector3(0, 0, 1)})
		j.colocar(inicio["pos"] + Vector3(0.0, 0.05, 0.0), inicio["mira"])
		await _esperar(0.4)
		await _seguir_ruta(id, ruta)
	if Zonas.id_actual == id:
		comprobar(get_tree().get_nodes_in_group("interactuables").size() > 1, "%s.tiene_interactuables" % id)


func _seguir_ruta(id: String, ruta: Array) -> void:
	var j: CharacterBody3D = Zonas.jugador
	var n := 0
	for paso in ruta:
		n += 1
		while Zonas.ocupado:
			await get_tree().process_frame
		if Zonas.id_actual != id:
			break
		if paso.has("ir"):
			var ok: bool = await j.caminar_hasta(paso["ir"], true, 30.0)
			comprobar(ok, "%s.ruta_%d.ir" % [id, n], "no llego a %s (quedo en %s)" % [str(paso["ir"]), str(j.global_position)])
		elif paso.has("usar"):
			var nodo: Node = Zonas.actual.get_node_or_null(String(paso["usar"]))
			if String(paso["usar"]) == "@orbita":
				nodo = Zonas.companero.hablar
				Zonas.jugador.colocar(Zonas.companero.global_position + Vector3(0.5, 0.05, 0.0))
				await _esperar(0.2)
			if comprobar(nodo != null and nodo.has_method("usar"), "%s.ruta_%d.usar_%s" % [id, n, paso["usar"]], "no existe ese interactuable"):
				var cerca: bool = j.global_position.distance_to(nodo.global_position) < nodo.radio + 0.6
				comprobar(cerca, "%s.ruta_%d.alcanza_%s" % [id, n, paso["usar"]], "la protagonista esta a %.2f m" % j.global_position.distance_to(nodo.global_position))
				await nodo.usar(j)
		elif paso.has("esperar"):
			await _esperar(float(paso["esperar"]))
		elif paso.has("bandera"):
			comprobar(bool(Juego.bandera(paso["bandera"])), "%s.ruta_%d.bandera_%s" % [id, n, paso["bandera"]])


func _despejado(punto: Vector3, radio: float) -> bool:
	var espacio := Zonas.mundo.get_world_3d().direct_space_state
	var forma := CylinderShape3D.new()
	forma.radius = radio
	forma.height = 0.8
	var consulta := PhysicsShapeQueryParameters3D.new()
	consulta.shape = forma
	consulta.transform = Transform3D(Basis.IDENTITY, punto + Vector3(0.0, 0.75, 0.0))
	consulta.collision_mask = 1
	return espacio.intersect_shape(consulta, 4).is_empty()


func _enlaces(ids: Array) -> void:
	# cada umbral lleva a una zona que existe y a una entrada que esa zona define
	for d in _destinos:
		if not ids.has(d[0]) or d[2] == "":
			continue
		if not comprobar(Zonas.existe(d[2]), "%s.umbral_%s.destino_existe" % [d[0], d[1]], "la zona '%s' no existe todavia" % d[2]):
			continue
		if not _entradas_por_zona.has(d[2]):
			Juego.nueva_partida()
			await Zonas.ir_a(d[2], "inicio")
			if Zonas.actual != null:
				_entradas_por_zona[d[2]] = Zonas.actual.entradas.keys()
		var entradas: Array = _entradas_por_zona.get(d[2], [])
		comprobar(entradas.has(d[3]), "%s.umbral_%s.entrada_destino" % [d[0], d[1]], "'%s' no tiene la entrada '%s' (tiene %s)" % [d[2], d[3], str(entradas)])


# ------------------------------------------------------------------ minijuegos

var _resultado_mj := {}
var _listo_mj := false


func _lanzar(id: String, parametros: Dictionary) -> void:
	_resultado_mj = await Interfaz.abrir_minijuego(id, parametros)
	_listo_mj = true


func _jugar_con_limite(id: String, parametros: Dictionary, limite_s: float) -> Dictionary:
	_listo_mj = false
	_resultado_mj = {}
	_lanzar(id, parametros)
	var restante := limite_s
	while not _listo_mj and restante > 0.0:
		await get_tree().process_frame
		restante -= get_process_delta_time()
	if not _listo_mj:
		Interfaz.anfitrion._abandonar()
		await _esperar(0.3)
		return {"superado": false, "colgado": true}
	return _resultado_mj


func _minijuego(id: String) -> void:
	var meta := Juego.info_minijuego(id)
	if not comprobar(not meta.is_empty(), "%s.minijuego_json" % id):
		return
	for clave in ["titulo", "resumen", "controles"]:
		comprobar(String(meta.get(clave, "")) != "", "%s.json.%s" % [id, clave])
	comprobar((meta.get("instrucciones", []) as Array).size() >= 2, "%s.json.instrucciones" % id, "faltan al menos 2 pasos")
	comprobar((meta.get("pistas", []) as Array).size() >= 3, "%s.json.pistas" % id, "faltan las 3 pistas de Orbita")
	var ficha: String = meta.get("ficha", "")
	comprobar(ficha == "" or not Juego.ficha(ficha).is_empty(), "%s.json.ficha" % id, "la ficha '%s' no esta en datos_espaciales.json" % ficha)
	for dificultad in [1, 3]:
		var r: Dictionary = await _jugar_con_limite(id, {"dificultad": dificultad}, 60.0)
		comprobar(not r.get("colgado", false), "%s.d%d.termina_solo" % [id, dificultad], "no termino en 60 s de juego")
		comprobar(bool(r.get("superado", false)), "%s.d%d.se_puede_superar" % [id, dificultad], str(r.get("detalle", "")))
	var mal: Dictionary = await _jugar_con_limite(id, {"dificultad": 1, "fallar": true}, 60.0)
	comprobar(not mal.get("colgado", false) and not bool(mal.get("superado", true)), "%s.se_puede_fallar" % id, "jugar_solo(false) debe terminar sin superar")
	comprobar(String(mal.get("detalle", "")).length() > 12, "%s.el_fallo_explica_la_causa" % id, "detalle vacio o muy corto: '%s'" % str(mal.get("detalle", "")))


# ------------------------------------------------------------------ recorrido completo

func _recorrido() -> void:
	# historia de punta a punta con el piloto automatico: cada zona aporta su ruta_de_prueba()
	Juego.nueva_partida()
	var orden: Array = Juego.leer_json("res://datos/misiones.json").get("recorrido_de_prueba", [])
	if not comprobar(not orden.is_empty(), "recorrido.definido", "falta 'recorrido_de_prueba' en datos/misiones.json"):
		return
	for tramo in orden:
		var id: String = tramo["zona"]
		await _esperar(0.3)
		while Zonas.ocupado:
			await get_tree().process_frame
		if Zonas.id_actual != id:
			var llego: bool = await Zonas.ir_a(id, tramo.get("entrada", "inicio"))
			if not comprobar(llego, "recorrido.%s.carga" % id):
				return
		await _esperar(0.5)
		var ruta: Array = Zonas.actual.ruta_de_prueba()
		await _seguir_ruta(id, ruta)
		await _esperar(0.3)
		while Zonas.ocupado:
			await get_tree().process_frame
		for b in tramo.get("banderas", []):
			comprobar(bool(Juego.bandera(b)), "recorrido.%s.bandera_%s" % [id, b])
	comprobar(Juego.mision_activa().is_empty(), "recorrido.todas_las_misiones_hechas", "queda activa: %s" % str(Juego.mision_activa().get("id", "")))
