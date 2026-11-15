extends Node

# Verificacion independiente de la zona "habitacion" (no es un entregable del carril).
# Recorre lo que la prueba zona: no ejecuta: la noche, el dia 2, el umbral cerrado en modo historia,
# el alcance de cada interactuable y los posibles atascos entre muebles.
# Se corre con: python -I herramientas/juego_ejecutar.py -- --prueba=guion:<ruta absoluta de este archivo> --ritmo=6

var p: Node


func _esperar(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _libre() -> void:
	await _esperar(0.4)
	while Zonas.ocupado:
		await get_tree().process_frame
	await _esperar(0.4)


func correr(pruebas: Node) -> void:
	p = pruebas
	await _noche()
	await _dia2()
	await _umbral()
	await _alcance()
	await _atascos()


func _noche() -> void:
	Juego.nueva_partida()
	Juego.poner_bandera("mir_luna")
	Juego.poner_bandera("mir_linea")
	var llego: bool = await Zonas.ir_a("habitacion", "escalera")
	if not p.comprobar(llego and Zonas.id_actual == "habitacion", "v.noche.carga"):
		return
	await _libre()
	var z: Node3D = Zonas.actual
	p.comprobar(bool(z.get("_noche")), "v.noche.estado")
	p.comprobar(bool(Juego.bandera("hab_noche")), "v.noche.bandera_hab_noche")
	p.comprobar(String(z.meta.get("momento", "")) == "Noche", "v.noche.momento", str(z.meta.get("momento", "")))
	var luces: Array = z.find_children("*", "OmniLight3D", true, false)
	p.comprobar(luces.size() >= 3, "v.noche.faroles_y_lampara", "luces=%d" % luces.size())
	print("V_INFO noche luces=", luces.size(), " cama.texto=", z.get_node("Cama").texto)
	await p._seguir_ruta("habitacion", z.ruta_de_prueba())
	await _libre()
	p.comprobar(bool(Juego.bandera("hab_durmio")), "v.noche.bandera_hab_durmio")
	p.comprobar(Zonas.id_actual == "luna", "v.noche.cama_lleva_a_luna", "zona actual: %s" % Zonas.id_actual)


func _dia2() -> void:
	Juego.nueva_partida()
	Juego.poner_bandera("luna_regreso")
	var llego: bool = await Zonas.ir_a("habitacion", "cama")
	if not p.comprobar(llego and Zonas.id_actual == "habitacion", "v.dia2.carga"):
		return
	await _libre()
	var z: Node3D = Zonas.actual
	p.comprobar(bool(z.get("_dia2")) and not bool(z.get("_noche")), "v.dia2.estado")
	print("V_INFO dia2 momento=", z.meta.get("momento", ""))
	var v: Node = z.get_node_or_null("Ventana")
	await v.usar(Zonas.jugador)
	p.comprobar(not bool(Juego.bandera("fin_v0")), "v.dia2.ventana_antes_no_cierra")
	await p._seguir_ruta("habitacion", z.ruta_de_prueba())
	await _libre()
	p.comprobar(bool(Juego.bandera("hab_seguidor_v2")), "v.dia2.bandera_hab_seguidor_v2")
	p.comprobar(bool(Juego.bandera("fin_v0")), "v.dia2.bandera_fin_v0")
	p.comprobar((Juego.estado["cuaderno"] as Array).has("prealimentacion"), "v.dia2.ficha_prealimentacion")
	print("V_INFO dia2 cuaderno=", (Juego.estado["cuaderno"] as Array).size(), " de ", Juego.fichas.size())


func _umbral() -> void:
	# modo historia (sin visita_libre): cerrado hasta hab_seguidor
	Juego.nueva_partida()
	var llego: bool = await Zonas.ir_a("habitacion", "inicio")
	if not p.comprobar(llego, "v.umbral.carga"):
		return
	await _libre()
	var z: Node3D = Zonas.actual
	var j: CharacterBody3D = Zonas.jugador
	var marca: Vector3 = z.get_node("Escalera").global_position
	print("V_INFO umbral marca=", marca, " radio=", z.get_node("Escalera").radio)
	await j.caminar_hasta(marca, false, 10.0)
	await _esperar(1.5)
	p.comprobar(Zonas.id_actual == "habitacion", "v.umbral.cerrado_sin_seguidor", "zona actual: %s" % Zonas.id_actual)
	Juego.poner_bandera("hab_seguidor")
	await j.caminar_hasta(z.entradas["inicio"]["pos"], false, 10.0)
	await _esperar(0.5)
	await j.caminar_hasta(marca, false, 10.0)
	await _esperar(1.0)
	await _libre()
	p.comprobar(Zonas.id_actual == "ciudad", "v.umbral.abre_con_hab_seguidor", "zona actual: %s" % Zonas.id_actual)


func _alcance() -> void:
	Juego.nueva_partida()
	Juego.poner_bandera("hab_saludo")
	var llego: bool = await Zonas.ir_a("habitacion", "inicio")
	if not p.comprobar(llego, "v.alcance.carga"):
		return
	await _libre()
	var z: Node3D = Zonas.actual
	var j: CharacterBody3D = Zonas.jugador
	var centro: Vector3 = z.entradas["inicio"]["pos"]
	for nombre in ["Cuaderno", "Seguidor", "Poster", "Telescopio", "Caja", "Ventana", "Cama"]:
		var n: Node3D = z.get_node_or_null(nombre)
		if not p.comprobar(n != null, "v.alcance.%s.existe" % nombre):
			continue
		j.colocar(centro + Vector3(0.0, 0.05, 0.0), Vector3(0, 0, 1))
		await _esperar(0.3)
		await j.caminar_hasta(n.global_position, false, 5.0)
		await _esperar(0.2)
		var d: float = j.global_position.distance_to(n.global_position)
		var mejor := ""
		var mejor_d := INF
		for o in get_tree().get_nodes_in_group("interactuables"):
			if not z.is_ancestor_of(o):
				continue
			var d2: float = j.global_position.distance_to(o.global_position)
			if d2 < o.radio and d2 < mejor_d:
				mejor = String(o.name)
				mejor_d = d2
		p.comprobar(d < n.radio, "v.alcance.%s.a_tiro" % nombre, "queda a %.2f m (radio %.2f)" % [d, n.radio])
		p.comprobar(mejor == nombre, "v.alcance.%s.es_el_elegido" % nombre, "el nucleo elegiria '%s'" % mejor)
		print("V_INFO alcance ", nombre, " d=%.2f" % d, " radio=", n.radio, " elegido=", mejor)


func _atascos() -> void:
	Juego.nueva_partida()
	Juego.poner_bandera("hab_saludo")
	var llego: bool = await Zonas.ir_a("habitacion", "inicio")
	if not p.comprobar(llego, "v.atasco.carga"):
		return
	await _libre()
	var z: Node3D = Zonas.actual
	var j: CharacterBody3D = Zonas.jugador
	var centro: Vector3 = z.entradas["inicio"]["pos"]
	# rincones y huecos entre muebles, en coordenadas del cuarto
	var puntos := {
		"hueco_banco_macetero": Vector3(2.45, 0.0, -1.75),
		"entre_cama_y_alfeizar": Vector3(-1.0, 0.0, -2.3),
		"junto_a_la_caja": Vector3(-3.0, 0.0, -0.6),
		"entre_banco_y_baranda": Vector3(3.0, 0.0, 0.75),
		"rincon_baranda_frente": Vector3(3.0, 0.0, 2.4),
		"rincon_frente_izquierda": Vector3(-3.0, 0.0, 2.4),
		"entre_alfeizar_y_telescopio": Vector3(1.25, 0.0, -2.3),
		"detras_del_taburete": Vector3(2.35, 0.0, -0.85),
	}
	for nombre in puntos:
		var destino: Vector3 = z._m(puntos[nombre])
		j.colocar(centro + Vector3(0.0, 0.05, 0.0), Vector3(0, 0, 1))
		await _esperar(0.3)
		var fue: bool = await j.caminar_hasta(destino, false, 6.0)
		var parada: Vector3 = j.global_position
		var volvio: bool = await j.caminar_hasta(centro, false, 8.0)
		var d: float = Vector2(j.global_position.x - centro.x, j.global_position.z - centro.z).length()
		p.comprobar(volvio or d < 0.5, "v.atasco.%s.vuelve_al_centro" % nombre, "paro en %s y quedo a %.2f m del centro" % [str(parada), d])
		p.comprobar(absf(j.global_position.y) < 0.4, "v.atasco.%s.sin_caer" % nombre, "y=%.2f" % j.global_position.y)
		print("V_INFO atasco ", nombre, " llego=", fue, " parada=", parada, " volvio=", volvio)
