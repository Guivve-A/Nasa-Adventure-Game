extends Node

# Pruebas de bordes del modelo y entradas reales; no cambian el nucleo.
const Minijuego := preload("res://minijuegos/muestras/muestras.gd")
const EVIDENCIA: String = "res://../Nasa_Game/Construccion/Minijuegos/muestras/"
var resultado: Dictionary = {}


func _crear(p: Dictionary) -> Control:
	var m: Control = Minijuego.new()
	add_child(m)
	m.position = Vector2(80, 100)
	m.terminado.connect(func(r: Dictionary): resultado = r)
	resultado = {}
	m.preparar(p, Juego.info_minijuego("muestras"))
	# Fondo del lienzo que normalmente pone el anfitrion.
	var fondo: ColorRect = ColorRect.new()
	fondo.color = Minijuego.Estilo.PAPEL
	fondo.size = Vector2(1120, 520)
	fondo.show_behind_parent = true
	fondo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	m.add_child(fondo)
	m.empezar()
	m.set_process(false)
	return m


func _avanzar(m: Control, segundos: float) -> void:
	var falta: float = segundos
	while falta > 0.000001 and m.activo:
		var delta: float = minf(falta, 1.0 / 120.0)
		falta -= delta
		m.tiempo += delta
		m._paso(delta)


func _tecla(m: Control, accion: String) -> void:
	var e: InputEventAction = InputEventAction.new()
	e.action = accion
	e.pressed = true
	m._input(e)


func _clic(m: Control, punto: Vector2) -> void:
	var e: InputEventMouseButton = InputEventMouseButton.new()
	e.button_index = MOUSE_BUTTON_LEFT
	e.pressed = true
	e.position = punto
	m._gui_input(e)


func _golpes(m: Control, cantidad: int) -> void:
	_tecla(m, "mover_derecha")
	_tecla(m, "mover_derecha")
	_tecla(m, "interactuar")
	for i in cantidad:
		_avanzar(m, 1.0)
		_tecla(m, "saltar")


func _foto(nombre: String) -> void:
	if DisplayServer.get_name() != "headless":
		await get_tree().process_frame
		await Interfaz.capturar(EVIDENCIA + nombre + ".png")


func correr(p: Node) -> void:
	for d in [1, 2, 3]:
		for indice in [-1, 0, 1, 2, 3]:
			for acierta in [true, false]:
				var m: Control = _crear({"muestra": indice, "dificultad": d})
				m.jugar_solo(acierta)
				_avanzar(m, 39.0)
				p.comprobar(not m.activo and bool(resultado.get("superado", false)) == acierta and m.tiempo < 40.0, "muestras.piloto.d%d.m%d.%s" % [d, indice, str(acierta)], str(resultado))
				if acierta:
					p.comprobar(m.registros.size() == (4 if indice == -1 else 1), "muestras.registros.d%d.m%d" % [d, indice])
				m.free()
	var m: Control = _crear({"muestra": 0})
	await _foto("01_herramientas")
	_tecla(m, "interactuar")
	_avanzar(m, 1.0)
	# Bolsa 1 no corresponde; debe conservarse el suelo y permitir corregir.
	_tecla(m, "interactuar")
	p.comprobar(m.activo and m.recogida and m.fase == Minijuego.Fase.BOLSA and m._mensaje.contains("corrige"), "muestras.bolsa_se_corrige_sin_perdida")
	await _foto("02_corregir_bolsa")
	_tecla(m, "mover_derecha")
	_tecla(m, "interactuar")
	_tecla(m, "mover_derecha")
	_tecla(m, "interactuar")
	p.comprobar(m.fase == Minijuego.Fase.MAPA and m.bolsa_guardada == 2 and m.registros.is_empty(), "muestras.mapa_se_corrige_sin_perdida")
	await _foto("03_croquis")
	_tecla(m, "mover_izquierda")
	_tecla(m, "interactuar")
	_avanzar(m, 2.0)
	p.comprobar(bool(resultado.get("superado", false)) and m._correcciones == 2, "muestras.correcciones_luego_victoria")
	m.free()
	# La ruta completa con raton recoge, elige bolsa y marca lugar.
	m = _crear({"muestra": 2})
	_clic(m, Vector2(850, 160))
	_avanzar(m, 1.0)
	_clic(m, Vector2(650, 200))
	_clic(m, Vector2(720, 260))
	_avanzar(m, 2.0)
	p.comprobar(bool(resultado.get("superado", false)), "muestras.raton_completa_roca")
	m.free()
	for cantidad in [3, 4, 5, 6]:
		m = _crear({"muestra": 3, "dificultad": 3})
		_golpes(m, cantidad)
		if cantidad == 4:
			await _foto("04_ritmo")
		_tecla(m, "interactuar")
		_avanzar(m, 2.3)
		p.comprobar((m.activo and m.recogida and m.fase == Minijuego.Fase.BOLSA) if cantidad == 4 else (not m.activo and not bool(resultado.get("superado", true))), "muestras.golpes_%d" % cantidad, str(resultado))
		if cantidad == 3:
			p.comprobar(String(resultado.get("detalle", "")).contains("corto"), "muestras.menos_deja_tubo_corto")
		if cantidad == 6:
			p.comprobar(String(resultado.get("detalle", "")).contains("2 de más"), "muestras.dos_de_mas_rompen_ritmo")
		m.free()
	m = _crear({"muestra": 3})
	_golpes(m, 0)
	_avanzar(m, 0.4)
	_tecla(m, "saltar")
	_tecla(m, "saltar")
	_avanzar(m, 2.3)
	p.comprobar(not bool(resultado.get("superado", true)) and String(resultado.get("detalle", "")).contains("fuera del pulso"), "muestras.dos_golpes_fuera_de_pulso")
	m.free()
	for d in [1, 3]:
		m = _crear({"muestra": 3, "dificultad": d})
		_golpes(m, 0)
		_avanzar(m, 1.18)
		_tecla(m, "saltar")
		p.comprobar((m.golpes == 1) if d == 1 else (m.golpes == 0 and m.desajustes == 1), "muestras.ventana_d%d" % d)
		m.free()
	m = _crear({"muestra": 3})
	_tecla(m, "interactuar")
	await _foto("05_capas_revueltas")
	_avanzar(m, 2.3)
	p.comprobar(String(resultado.get("detalle", "")).contains("revuelve las capas"), "muestras.cucharon_mezcla_capas")
	m.free()
	m = _crear({"muestra": 0})
	_avanzar(m, 91.0)
	p.comprobar(not m.activo and String(resultado.get("detalle", "")).contains("Falta recoger"), "muestras.limite_sesion_causal")
	m.free()
	# Deja terminar los sonidos transitorios antes de que cierre el motor.
	await get_tree().create_timer(1.0, true, false, true).timeout
