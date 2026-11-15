extends Node

# Pruebas automaticas del juego (sin ventana). Se corren con:
#   python -I herramientas/juego_ejecutar.py -- --prueba=<nombre> --ritmo=8
# Nombres: nucleo | zonas | zona:<id> | minijuegos | minijuego:<id> | recorrido | manos | recorrido_manos
# (manos y recorrido_manos juegan con teclas simuladas, como una persona: usar --ritmo=2)
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
		"manos":
			await _manos()
		"recorrido_manos":
			await _recorrido_manos()
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
	_minimapa_datos()
	_sonido()
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
	_minimapa_zona(id)
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
	# las secundarias (los libros de la biblioteca) no cuentan para cerrar la historia
	var queda := Juego.mision_activa()
	comprobar(queda.is_empty() or bool(queda.get("secundaria", false)), "recorrido.todas_las_misiones_principales_hechas", "queda activa: %s" % str(queda.get("id", "")))


# ------------------------------------------------------------------ pruebas con el teclado simulado
# Juegan como una persona: las teclas entran por Input.parse_input_event, igual que las de verdad. Asi se
# comprueba el camino real (teclas, avisos [E], dialogos, botones con foco), no un atajo del piloto.

var _pulsadas := {}


func _real(segundos: float) -> void:
	# espera en tiempo real (no le afecta --ritmo)
	await get_tree().create_timer(segundos, true, false, true).timeout


func _tecla(codigo: int, abajo: bool) -> void:
	if bool(_pulsadas.get(codigo, false)) == abajo:
		return
	_pulsadas[codigo] = abajo
	var evento := InputEventKey.new()
	evento.physical_keycode = codigo
	evento.keycode = codigo
	evento.pressed = abajo
	Input.parse_input_event(evento)


func _toque(codigo: int) -> void:
	_tecla(codigo, true)
	await get_tree().process_frame
	await get_tree().physics_frame
	await get_tree().process_frame
	_tecla(codigo, false)
	await get_tree().process_frame


func _soltar_todo() -> void:
	for codigo in _pulsadas.keys():
		_tecla(codigo, false)


func _apuntar(d: Vector3) -> void:
	# pulsa las teclas de movimiento que llevan hacia d (ocho direcciones, como con WASD)
	var umbral := d.length() * 0.38
	_tecla(KEY_D, d.x > umbral)
	_tecla(KEY_A, d.x < -umbral)
	_tecla(KEY_S, d.z > umbral)
	_tecla(KEY_W, d.z < -umbral)


func _caminar_con_teclas(destino: Vector3, limite_s: float = 40.0, radio: float = 0.32) -> bool:
	var j: CharacterBody3D = Zonas.jugador
	var restante := limite_s
	var quieto := 0.0
	var rodeos := 0
	var ultima := j.global_position
	var zona_inicial := Zonas.id_actual
	while restante > 0.0:
		if Zonas.ocupado or Zonas.jugador == null or Zonas.id_actual != zona_inicial:
			_soltar_todo()
			return true      # piso un umbral: el cambio de zona ya empezo
		if Interfaz.ocupada():
			_soltar_todo()
			await _atender_interfaz()
			continue
		var d: Vector3 = destino - j.global_position
		d.y = 0.0
		if d.length() < radio:
			_soltar_todo()
			return true
		_apuntar(d)
		_tecla(KEY_SHIFT, d.length() > 2.5)
		await get_tree().physics_frame
		var paso := get_physics_process_delta_time()
		restante -= paso
		quieto += paso
		if quieto > 0.9:
			if j.global_position.distance_to(ultima) < 0.12:
				# atascada contra algo: lo rodea como una persona, deslizandose a un lado y luego al otro
				rodeos += 1
				if rodeos > 10:
					break
				var lado := Vector3(-d.z, 0.0, d.x).normalized() * (1.0 if rodeos % 2 == 1 else -1.0)
				_soltar_todo()
				_apuntar(lado + d.normalized() * 0.45)
				var rato := 0.3 + 0.12 * float(rodeos)
				while rato > 0.0 and not Zonas.ocupado:
					await get_tree().physics_frame
					rato -= get_physics_process_delta_time()
					restante -= get_physics_process_delta_time()
				_soltar_todo()
			ultima = j.global_position
			quieto = 0.0
	_soltar_todo()
	return false


func _usar_con_teclas(nodo: Node3D) -> bool:
	# se gira hacia el objeto (un toque de movimiento) hasta que el aviso [E] lo senala, y pulsa E
	var j: CharacterBody3D = Zonas.jugador
	var intentos := 24
	while intentos > 0 and j.get("objetivo") != nodo:
		var d: Vector3 = nodo.global_position - j.global_position
		d.y = 0.0
		if d.length() > 0.05:
			_apuntar(d)
		await get_tree().physics_frame
		await get_tree().physics_frame
		_soltar_todo()
		await get_tree().physics_frame
		await get_tree().physics_frame
		intentos -= 1
	if j.get("objetivo") != nodo:
		return false
	await _real(0.35)
	await _toque(KEY_E)
	return true


func _atender_interfaz(limite_s: float = 40.0) -> void:
	# pulsa lo que pulsaria una persona hasta que la interfaz devuelve el control
	var restante := limite_s
	await _real(0.12)
	while restante > 0.0:
		if Zonas.ocupado or Interfaz.carga.visible:
			await _real(0.1)
		elif Interfaz.dialogo.visible:
			if Interfaz.dialogo.get("_opciones").get_child_count() > 0:
				await _toque(KEY_ENTER)      # elige la opcion con foco (la primera)
			else:
				await _toque(KEY_E)
			await _real(0.1)
		elif Interfaz.ocupada():
			await _real(0.1)
		else:
			await _real(0.4)
			if not Interfaz.ocupada() and not Zonas.ocupado:
				return
		restante -= 0.15


func _modo_manos(activo: bool, minijuegos_solos: bool) -> void:
	Juego.modo_prueba = not activo
	Juego.sin_guardar = true
	Juego.minijuegos_solos = minijuegos_solos and activo
	if not activo:
		_soltar_todo()


func _manos() -> void:
	# el nucleo jugado con teclas: moverse, hablar, usar un objeto, jugar un minijuego, menus y umbral
	_modo_manos(true, false)
	Juego.nueva_partida()
	await Zonas.ir_a("plantilla", "inicio")
	await _atender_interfaz()
	var j: CharacterBody3D = Zonas.jugador
	await _real(0.6)
	comprobar(not Interfaz.dialogo.visible, "manos.el_dialogo_se_cierra_con_E_y_no_se_reabre")
	# moverse con D
	var x0 := j.global_position.x
	_tecla(KEY_D, true)
	await _real(0.5)
	_tecla(KEY_D, false)
	await _real(0.2)
	comprobar(j.global_position.x > x0 + 0.3, "manos.moverse_con_teclas", "x paso de %.2f a %.2f" % [x0, j.global_position.x])
	# hablar con Orbita mirandolo de frente
	var gato: Node3D = Zonas.companero.hablar
	var hablo: bool = await _usar_con_teclas(gato)
	comprobar(hablo, "manos.el_aviso_E_senala_a_orbita_al_mirarlo", "aviso en: %s" % str(j.get("objetivo")))
	await _atender_interfaz()
	comprobar(bool(Juego.bandera("hablo_orbita")), "manos.hablar_con_orbita")
	# usar el cartel: abre el minijuego de plantilla, que aqui se juega con teclas de verdad
	var llego: bool = await _caminar_con_teclas(Vector3(2.0, 0.0, 1.2))
	comprobar(llego, "manos.caminar_hasta_el_cartel", str(j.global_position))
	var cartel: Node3D = Zonas.actual.get_node_or_null("Cartel")
	var uso: bool = await _usar_con_teclas(cartel)
	comprobar(uso, "manos.el_aviso_E_senala_al_cartel_y_no_a_orbita", "aviso en: %s" % str(j.get("objetivo")))
	await _real(0.6)
	var anfitrion: Control = Interfaz.anfitrion
	comprobar(anfitrion.visible, "manos.el_minijuego_se_abre_con_E")
	await _toque(KEY_ENTER)                 # boton «Empezar», que tiene el foco
	await _real(0.3)
	var mj: Variant = anfitrion.get("_minijuego")
	var limite := 40.0
	while limite > 0.0 and mj != null and is_instance_valid(mj) and bool(mj.get("activo")):
		var falta: float = float(mj.get("objetivo")) - float(mj.get("dial"))
		_tecla(KEY_D, falta > 0.02)
		_tecla(KEY_A, falta < -0.02)
		await get_tree().process_frame
		limite -= get_process_delta_time()
	_soltar_todo()
	await _real(0.5)
	comprobar(bool(anfitrion.get("_resultado").get("superado", false)), "manos.minijuego_ganado_con_teclas", str(anfitrion.get("_resultado")))
	await _toque(KEY_ENTER)                 # boton «Continuar»
	await _atender_interfaz()
	await _real(0.6)
	comprobar(not anfitrion.visible and not Interfaz.dialogo.visible, "manos.intro_no_reabre_el_minijuego")
	comprobar(bool(Juego.bandera("plantilla_minijuego")), "manos.la_zona_recibe_el_resultado")
	# mapa, cuaderno y pausa
	await _toque(KEY_M)
	await _real(0.3)
	comprobar(Interfaz.mapa.visible, "manos.mapa_con_M")
	await _toque(KEY_ESCAPE)
	await _real(0.5)
	comprobar(not Interfaz.mapa.visible and not get_tree().paused, "manos.mapa_se_cierra_con_Esc")
	await _toque(KEY_TAB)
	await _real(0.3)
	comprobar(Interfaz.cuaderno.visible, "manos.cuaderno_con_Tab")
	await _toque(KEY_TAB)
	await _real(0.5)
	comprobar(not Interfaz.cuaderno.visible and not get_tree().paused, "manos.cuaderno_se_cierra_con_Tab")
	await _toque(KEY_ESCAPE)
	await _real(0.3)
	comprobar(Interfaz.pausa.visible and get_tree().paused, "manos.pausa_con_Esc")
	await _toque(KEY_ENTER)                 # boton «Continuar»
	await _real(0.5)
	comprobar(not Interfaz.pausa.visible and not get_tree().paused, "manos.pausa_continua_con_Intro")
	# cruzar el umbral caminando
	await _caminar_con_teclas(Vector3(0.0, 0.0, -4.2), 30.0, 0.2)
	await _real(1.5)
	comprobar(j.global_position.z > 2.0, "manos.umbral_al_pisarlo", "z=%.2f" % j.global_position.z)
	await _minimapa_manos()
	_modo_manos(false, false)
	Zonas.cerrar()
	await _real(0.2)


func _ruta_manos(id: String, ruta: Array) -> void:
	var j: CharacterBody3D = Zonas.jugador
	var n := 0
	for paso in ruta:
		n += 1
		while Zonas.ocupado:
			await get_tree().process_frame
		if Zonas.id_actual != id:
			break
		await _atender_interfaz()
		while Zonas.ocupado:
			await get_tree().process_frame
		if Zonas.id_actual != id:
			break      # mientras se atendia la interfaz ya cruzo un umbral (venia con impulso)
		if paso.has("ir"):
			var ok: bool = await _caminar_con_teclas(paso["ir"])
			comprobar(ok, "manos.%s.paso_%d.caminar" % [id, n], "no llego a %s; quedo en %s | %s" % [str(paso["ir"]), str(j.global_position), _diagnostico()])
			if not ok and Zonas.id_actual == id:
				await j.caminar_hasta(paso["ir"], true, 30.0)     # sigue con el piloto para no cortar la prueba
		elif paso.has("usar"):
			var nodo: Node3D = Zonas.actual.get_node_or_null(String(paso["usar"]))
			if String(paso["usar"]) == "@orbita":
				nodo = Zonas.companero.hablar
			if not comprobar(nodo != null, "manos.%s.paso_%d.existe_%s" % [id, n, paso["usar"]]):
				continue
			var usado: bool = await _usar_con_teclas(nodo)
			var senala := "nada"
			if j.get("objetivo") != null:
				senala = String(j.get("objetivo").name)
			comprobar(usado, "manos.%s.paso_%d.usar_%s_con_E" % [id, n, paso["usar"]], "el aviso [E] senala a: %s; distancia %.2f" % [senala, j.global_position.distance_to(nodo.global_position)])
			if not usado:
				await nodo.usar(j)
			await _atender_interfaz()
		elif paso.has("esperar"):
			await _esperar(float(paso["esperar"]))
		elif paso.has("bandera"):
			comprobar(bool(Juego.bandera(paso["bandera"])), "manos.%s.paso_%d.bandera_%s" % [id, n, paso["bandera"]])


func _recorrido_manos() -> void:
	# la historia de punta a punta con teclas simuladas; los minijuegos se juegan solos (cada uno tiene su prueba)
	_modo_manos(true, true)
	Juego.nueva_partida()
	var orden: Array = Juego.leer_json("res://datos/misiones.json").get("recorrido_de_prueba", [])
	var primero := true
	for tramo in orden:
		var id: String = tramo["zona"]
		await _real(0.3)
		while Zonas.ocupado:
			await get_tree().process_frame
		if Zonas.id_actual != id:
			var llego: bool = await Zonas.ir_a(id, tramo.get("entrada", "inicio"))
			if not primero:
				comprobar(false, "manos.se_llega_a_%s_jugando" % id, "hubo que saltar a la zona: el paso anterior no llevo hasta aqui")
			if not llego:
				break
		else:
			comprobar(true, "manos.se_llega_a_%s_jugando" % id)
		primero = false
		await _atender_interfaz()
		var ruta: Array = Zonas.actual.ruta_de_prueba()
		await _ruta_manos(id, ruta)
		await _real(0.4)
		while Zonas.ocupado:
			await get_tree().process_frame
		await _atender_interfaz()
		for b in tramo.get("banderas", []):
			comprobar(bool(Juego.bandera(b)), "manos.%s.bandera_%s" % [id, b])
	_modo_manos(false, false)


func _diagnostico() -> String:
	# estado de la interfaz y de los umbrales cercanos, para entender un atasco
	var j: Node3D = Zonas.jugador
	var partes: Array = ["ocupada=%s hablando=%s dialogo=%s anfitrion=%s carga=%s zonas_ocupado=%s suelo=%s" % [
		str(Interfaz.ocupada()), str(Interfaz.get("_hablando")), str(Interfaz.dialogo.visible), str(Interfaz.anfitrion.visible),
		str(Interfaz.carga.visible), str(Zonas.ocupado), str(j.call("is_on_floor"))]]
	for u in get_tree().get_nodes_in_group("umbrales"):
		var d := Vector2(j.global_position.x - u.global_position.x, j.global_position.z - u.global_position.z).length()
		if d < 2.5:
			partes.append("umbral %s d=%.2f dy=%.2f radio=%.2f armado=%s abierto=%s cruzando=%s" % [u.name, d, j.global_position.y - u.global_position.y, float(u.radio), str(u.armado), str(u.abierto()), str(u.get("_cruzando"))])
	return " ; ".join(PackedStringArray(partes))


# ------------------------------------------------------------------ minimapa («donde estoy y a donde voy»)

func _minimapa_datos() -> void:
	# cada paso de mision dice en que zona se cumple y a que nodo lleva (lo usa el minimapa)
	var sin_dato: Array = []
	for m in Juego.misiones:
		for p in m.get("pasos", []):
			var paso: Dictionary = p
			if not paso.has("zona") or not paso.has("destino"):
				sin_dato.append(String(paso.get("bandera", "?")))
			elif not Zonas.existe(String(paso["zona"])):
				sin_dato.append("%s (zona %s)" % [String(paso.get("bandera", "?")), String(paso["zona"])])
	comprobar(sin_dato.is_empty(), "minimapa.cada_paso_tiene_zona_y_destino", str(sin_dato))
	Juego.nueva_partida()
	var d: Dictionary = Juego.destino_actual()
	comprobar(String(d.get("zona", "")) == "habitacion" and String(d.get("destino", "")) == "@orbita", "minimapa.destino_del_primer_paso", str(d))


func _minimapa_zona(id: String) -> void:
	var mm: Control = Interfaz.hud.get("minimapa")
	if not comprobar(mm != null, "%s.minimapa_existe" % id):
		return
	mm.actualizar_ahora()
	# los destinos de los pasos que se cumplen aqui existen en la zona
	for m in Juego.misiones:
		for p in m.get("pasos", []):
			var paso: Dictionary = p
			var nombre := String(paso.get("destino", ""))
			if String(paso.get("zona", "")) != id or nombre == "" or nombre == "@orbita":
				continue
			comprobar(mm._buscar(nombre) != null, "%s.minimapa_destino_%s" % [id, nombre], "el paso '%s' senala un nodo que la zona no tiene" % String(paso.get("bandera", "")))
	# desde cada lugar del mapa del mundo hay una salida que acerca a cualquier otro
	var mapa: Variant = Juego.leer_json("res://datos/mapa.json")
	var ids: Array = []
	if mapa is Dictionary:
		for n in mapa.get("nodos", []):
			ids.append(String(n.get("id", "")))
	if not ids.has(id) and String(Juego.destino_actual().get("zona", "")) != id:
		return      # zona fuera del mapa del mundo (plantilla): no hay ruta que senalar
	comprobar(mm.get("tiene_objetivo"), "%s.minimapa_senala_un_objetivo" % id, "destino=%s" % str(Juego.destino_actual()))
	if not ids.has(id):
		return
	for otro in ids:
		if otro == id or not Zonas.existe(otro):
			continue
		var siguiente: String = mm._siguiente_zona(id, otro)
		comprobar(siguiente != "" and mm._salida_hacia(id, siguiente) != null, "%s.minimapa_camino_a_%s" % [id, otro], "siguiente=%s" % siguiente)


func _minimapa_manos() -> void:
	var j: CharacterBody3D = Zonas.jugador
	var mm: Control = Interfaz.hud.get("minimapa")
	await _real(0.4)
	if not comprobar(mm != null and mm.visible, "manos.minimapa_visible", "mm=%s" % str(mm)):
		return
	var r0: float = mm.radio_px()
	await _toque(KEY_N)
	await _real(0.2)
	comprobar(mm.get("grande") and mm.radio_px() > r0, "manos.minimapa_grande_con_N")
	await _toque(KEY_N)
	await _real(0.2)
	comprobar(not mm.get("grande"), "manos.minimapa_normal_con_N")
	# lleva la historia hasta la mision de prueba de esta zona: el paso 2 senala el umbral del fondo
	for m in Juego.misiones:
		if m.get("secundaria", false) or String(m.get("id", "")) == "m_plantilla":
			continue
		for p in m.get("pasos", []):
			Juego.poner_bandera(String(p.get("bandera", "")))
	Juego.poner_bandera("plantilla_saludo")
	Juego.poner_bandera("plantilla_paso_1")
	await _atender_interfaz()
	mm.actualizar_ahora()
	await _real(0.3)
	var umbral_fondo: Node3D = Zonas.actual.get_node_or_null("AlFondo")
	comprobar(mm.get("tiene_objetivo") and umbral_fondo != null and String(mm.get("objetivo_nombre")) == String(umbral_fondo.get("etiqueta")),
		"manos.minimapa_muestra_el_objetivo", "objetivo=%s destino=%s" % [str(mm.get("objetivo_nombre")), str(Juego.destino_actual())])
	var marca: Variant = mm.get("_marca")
	comprobar(marca != null and (marca as Node3D).visible, "manos.minimapa_marca_dorada_en_el_mundo")
	var d0: float = mm.get("objetivo_distancia")
	await _caminar_con_teclas(Vector3(0.0, 0.0, -2.3), 20.0, 0.3)
	await _real(0.3)
	var d1: float = mm.get("objetivo_distancia")
	comprobar(d1 < d0 - 1.5, "manos.minimapa_la_distancia_baja_al_acercarse", "de %.2f m a %.2f m (z=%.2f)" % [d0, d1, j.global_position.z])


func _sonido() -> void:
	# los efectos del lote A1 se cargan como recursos importados (no con load_from_file) y el ambiente se enciende y apaga
	var faltan: Array = []
	for nombre in ["paso", "paso_luna", "salto", "recoger", "umbral", "logro", "pagina", "radio", "golpe_mastil"]:
		if Audio._cargar("res://audio/%s.ogg" % nombre) == null:
			faltan.append(nombre)
	comprobar(faltan.is_empty(), "sonido.efectos_importados", "faltan: %s (correr con --importar)" % str(faltan))
	comprobar(Audio.tiene_archivo("paso") and not Audio.tiene_archivo("no_existe"), "sonido.archivo_o_sintesis")
	Audio.sonar("ok")
	Audio.sonar("recoger")
	Audio.paso()
	if not Juego.args.has("sin_sonido"):
		# el paso de la protagonista tiene intervalo minimo; el de la iguana (sonar("paso", x)) suena entero y seguido
		var n0: int = Audio.reproducidos
		Audio.sonar("paso", 2.0)
		Audio.sonar("paso", -2.0)
		comprobar(Audio.reproducidos - n0 == 2, "sonido.paso_ajeno_sin_limite", "sonaron %d de 2" % (Audio.reproducidos - n0))
		var n1: int = Audio.reproducidos
		Audio.sonar("paso", -26.0)
		Audio.sonar("paso", -26.0)
		comprobar(Audio.reproducidos - n1 <= 1, "sonido.paso_propio_con_intervalo", "sonaron %d" % (Audio.reproducidos - n1))
	Audio.ambiente("luna")
	comprobar(Audio.ambiente_actual() == "luna", "sonido.ambiente_enciende")
	Audio.ambiente("sin_archivo")
	comprobar(Audio.ambiente_actual() == "", "sonido.ambiente_sin_archivo_se_apaga")
