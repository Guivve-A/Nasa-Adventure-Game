extends Node

# Cobertura adicional del montaje con entradas reales y de las causas del balance.
const Satelite := preload("res://minijuegos/satelite/satelite.gd")


func _nuevo(nivel: int) -> Control:
	var m: Control = Satelite.new()
	add_child(m)
	m.preparar({"dificultad": nivel}, {})
	m.set_process(false)
	m.empezar()
	return m


func _tecla(m: Control, accion: String) -> void:
	var e: InputEventAction = InputEventAction.new()
	e.action = accion
	e.pressed = true
	m._input(e)


func _raton(m: Control, pos: Vector2, presionado: bool) -> void:
	var e: InputEventMouseButton = InputEventMouseButton.new()
	e.button_index = MOUSE_BUTTON_LEFT
	e.position = pos
	e.pressed = presionado
	m._gui_input(e)


func _montar(m: Control) -> void:
	for i in 4:
		while m.seleccion != i:
			_tecla(m, "mover_abajo")
		_tecla(m, "interactuar")
		while m.hueco != i:
			_tecla(m, "mover_derecha")
		_tecla(m, "interactuar")
	_tecla(m, "saltar")


func _resolver(m: Control, paso: float) -> Dictionary:
	var resultados: Array[Dictionary] = []
	m.terminado.connect(func(r: Dictionary): resultados.append(r))
	var limite: int = int(39.0 / paso) + 1
	for i in limite:
		if not m.activo:
			break
		m._process(paso)
	return resultados[0] if not resultados.is_empty() else {}


func correr(p: Node) -> void:
	var teclado: Control = _nuevo(1)
	_tecla(teclado, "saltar")
	p.comprobar(teclado.fase == 0, "satelite.montaje_incompleto_bloqueado")
	_tecla(teclado, "interactuar")
	_tecla(teclado, "mover_derecha")
	_tecla(teclado, "interactuar")
	p.comprobar(teclado.piezas[1] == -1 and teclado._mensaje.contains("Enviar datos"), "satelite.hueco_ajeno_explica_funcion")
	_montar(teclado)
	p.comprobar(teclado.fase == 1, "satelite.montaje_entero_con_teclado")
	teclado.free()
	var raton: Control = _nuevo(1)
	for i in 4:
		_raton(raton, raton._rect_pieza(i).get_center(), true)
		_raton(raton, raton._rect_hueco(i).get_center(), false)
	_tecla(raton, "saltar")
	p.comprobar(raton.fase == 1, "satelite.montaje_arrastrando_con_raton")
	raton.free()
	for nivel in [1, 2, 3]:
		for paso in [0.016, 0.37]:
			var m: Control = _nuevo(nivel)
			m.jugar_solo(true)
			var r: Dictionary = _resolver(m, paso)
			p.comprobar(r.get("superado", false) and r.get("tiempo", 99.0) < 40.0, "satelite.piloto_d%d_delta%s" % [nivel, str(paso)], str(r))
			m.free()
	# Se conserva un unico defecto cada vez para comprobar la explicacion causal.
	for defecto in ["antena", "computadora", "radio_sol", "paneles", "radio_sombra"]:
		var m: Control = _nuevo(3)
		_montar(m)
		m._cambiar(0, 1)
		m._cambiar(0, 1)
		m._cambiar(1, 1)
		m._cambiar(4, 1)
		var esperado: String = ""
		match defecto:
			"antena":
				m._cambiar(1, 1)
				esperado = "no llega a tierra"
			"computadora":
				m._cambiar(2, 1)
				esperado = "nadie ordena"
			"radio_sol":
				m._cambiar(3, 1)
				esperado = "nadie los envía"
			"paneles":
				m._cambiar(0, 1)
				esperado = "generan 2 u"
			"radio_sombra":
				m._cambiar(4, 1)
				esperado = "batería se agota"
		var resultados: Array[Dictionary] = []
		m.terminado.connect(func(r: Dictionary): resultados.append(r))
		_tecla(m, "saltar")
		for i in 100:
			if m.activo:
				m._process(0.13)
		var r: Dictionary = resultados[0] if not resultados.is_empty() else {}
		p.comprobar(not r.is_empty() and not r.get("superado", true) and String(r.get("detalle", "")).contains(esperado), "satelite.causa_" + defecto, str(r))
		m.free()
