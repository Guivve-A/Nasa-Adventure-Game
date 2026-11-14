extends Node

# Pruebas del carril: orden, entradas y umbrales del modelo compartido con el piloto.
const Regreso := preload("res://minijuegos/regreso/regreso.gd")


func _crear(d: int = 1) -> Control:
	var m: Control = Regreso.new()
	add_child(m)
	m.preparar({"dificultad": d}, Juego.info_minijuego("regreso"))
	m.empezar()
	m.set_process(false)
	return m


func _tecla(m: Control, accion: String) -> void:
	var evento: InputEventAction = InputEventAction.new()
	evento.action = accion
	evento.pressed = true
	m._input(evento)


func _correr(m: Control, dt: float = 1.0 / 60.0) -> Dictionary:
	var resultado: Dictionary = {}
	m.terminado.connect(func(r: Dictionary): resultado.merge(r))
	while m.activo and m.tiempo < 39.0:
		m.tiempo += dt
		m._paso(dt)
	return resultado


func correr(p: Node) -> void:
	var m: Control = _crear()
	_tecla(m, "interactuar")
	_tecla(m, "mover_abajo")
	p.comprobar(m.orden[0] == 0 and m.orden[1] == 1 and m.seleccion == 1, "regreso.teclado_toma_y_mueve")
	_tecla(m, "interactuar")
	_tecla(m, "mover_abajo")
	p.comprobar(m.seleccion == 2 and m.orden[2] == 2, "regreso.teclado_suelta_y_selecciona")
	# Arrastra paracaidas debajo de la reentrada por el mismo gui_input del lienzo.
	var clic: InputEventMouseButton = InputEventMouseButton.new()
	clic.button_index = MOUSE_BUTTON_LEFT
	clic.pressed = true
	clic.position = m._rect_tarjeta(3).get_center()
	m._gui_input(clic)
	var arrastre: InputEventMouseMotion = InputEventMouseMotion.new()
	arrastre.button_mask = MOUSE_BUTTON_MASK_LEFT
	arrastre.position = m._rect_tarjeta(4).get_center()
	m._gui_input(arrastre)
	clic.pressed = false
	clic.position = arrastre.position
	m._gui_input(clic)
	p.comprobar(m.orden == [0, 1, 2, 3, 4, 5] and not m.tomada, "regreso.raton_arrastra_y_suelta")
	m._boton.pressed.emit()
	p.comprobar(m.fase == 1 and m.comprobaciones == 1, "regreso.boton_comprobar_inicia_reentrada")
	m._pulsar_giro(-1.0)
	m._paso(0.5)
	p.comprobar(m.giro < 0.0 and m.angulo < 6.0, "regreso.raton_corrige_con_fisica")
	var previo: float = m.giro
	m._soltar_giro()
	m._paso(0.01)
	p.comprobar(m._raton == 0.0 and m.giro < 0.0 and absf(m.giro - previo) < 3.0, "regreso.soltar_conserva_inercia")
	m.free()
	# Cualquier par consecutivo invertido produce una causa propia.
	for i in 5:
		m = _crear()
		m.orden.assign([0, 1, 2, 3, 4, 5])
		m.seleccion = i
		m._mover(1)
		var r: Dictionary = {}
		m.terminado.connect(func(dato: Dictionary): r.merge(dato))
		_tecla(m, "saltar")
		p.comprobar(not m.activo and not r.get("superado", true) and r.get("detalle", "") == m.CAUSAS[i], "regreso.par_%d_causa_real" % i)
		m.free()
	# Los tres niveles, con pasos normales y cuadros largos del reloj acelerado.
	for d in [1, 2, 3]:
		for dt in [1.0 / 60.0, 0.2]:
			m = _crear(d)
			m.jugar_solo(true)
			var resultado: Dictionary = _correr(m, dt)
			p.comprobar(resultado.get("superado", false) and m.tiempo < 40.0 and m.vuelo >= 20.0 and m.dentro >= 16.0 and m.calor < 100.0, "regreso.piloto_d%d_dt%.3f" % [d, dt])
			print("REGRESO_QA d%d dt=%.3f total=%.3f dentro=%.3f calor=%.2f" % [d, dt, m.tiempo, m.dentro, m.calor])
			m.free()
		m = _crear(d)
		m.jugar_solo(false)
		var fallo: Dictionary = _correr(m)
		p.comprobar(not fallo.get("superado", true) and m.calor >= 100.0 and m.vuelo < 20.0 and m.tiempo < 40.0, "regreso.piloto_falla_por_calor_d%d" % d)
		m.free()
	m = _crear()
	p.comprobar(m._anterior.size() > 2 and m._dato_anterior.contains("calor 100"), "regreso.intento_previo_persistente")
	m.orden.assign([0, 1, 2, 3, 4, 5])
	m._comprobar()
	m.calor = 99.9
	m.angulo = m.margen + 2.0
	m._integrar(0.1, 0.0)
	p.comprobar(not m.activo and m.calor == 100.0, "regreso.umbral_calor_100")
	m.free()
	m = _crear()
	m.orden.assign([0, 1, 2, 3, 4, 5])
	m._comprobar()
	m.vuelo = 19.999
	m.dentro = 15.0
	m.angulo = 0.0
	m._integrar(0.01, 0.0)
	p.comprobar(not m.activo and m.fase == 1, "regreso.exige_16_s_dentro")
	m.free()
	m = _crear()
	m.tiempo = 150.0
	m._paso(0.01)
	p.comprobar(not m.activo, "regreso.limite_orden_150_s")
	m.free()
	# La simulacion sincronica acumula voces: deja acabar el audio antes de cerrar.
	await get_tree().create_timer(0.3, true, false, true).timeout
