extends Node

# Pruebas del carril: modelo real, controles y memoria entre reintentos.
const Orbita := preload("res://minijuegos/orbita/orbita.gd")


func _crear(nivel: int) -> Control:
	var m: Control = Orbita.new()
	add_child(m)
	m.preparar({"dificultad": nivel}, Juego.info_minijuego("orbita"))
	m.empezar()
	m.set_process(false)
	return m


func _simular(nivel: int, v: float, delta: float) -> Dictionary:
	var m: Control = _crear(nivel)
	var salida: Dictionary = {}
	m.terminado.connect(func(r: Dictionary): salida.merge(r))
	# El cambio de valor emite la senal real del deslizador.
	m._dial.value = v
	m._lanzar_boton.pressed.emit()
	while m.activo and m.tiempo < 39.0:
		m.tiempo += delta
		m._paso(delta)
	salida["minima"] = m.minima
	salida["maxima"] = m.maxima
	salida["giro"] = m.angulo
	m.free()
	return salida


func correr(p: Node) -> void:
	for nivel in [1, 2, 3]:
		var h: float = 654.0 if nivel == 3 else 627.0
		var r: Dictionary = _simular(nivel, snappedf(sqrt(398600.0 / (6371.0 + h)), 0.001), 0.017)
		p.comprobar(r.get("superado", false) and float(r.get("tiempo", 99.0)) < 40.0 and float(r["giro"]) >= TAU, "orbita.modelo.circular.d%d" % nivel, str(r))
	var elipse: Dictionary = _simular(1, 8.0, 0.05)
	p.comprobar(not elipse.get("superado", true) and String(elipse.get("detalle", "")).contains("elipse") and float(elipse["giro"]) >= TAU, "orbita.modelo.elipse_completa", str(elipse))
	var escape: Dictionary = _simular(1, 11.0, 0.05)
	p.comprobar(not escape.get("superado", true) and String(escape.get("detalle", "")).contains("escapa"), "orbita.modelo.escape", str(escape))
	var larga: Dictionary = _simular(1, 9.0, 0.05)
	p.comprobar(not larga.get("superado", true) and String(larga.get("detalle", "")).contains("9 600"), "orbita.modelo.elipse_larga", str(larga))
	var baja: Dictionary = _simular(1, 5.5, 0.05)
	p.comprobar(not baja.get("superado", true) and String(baja.get("detalle", "")).contains("cae") and float(baja["minima"]) <= 120.0, "orbita.modelo.caida", str(baja))
	var a: Dictionary = _simular(2, 7.547, 0.017)
	var b: Dictionary = _simular(2, 7.547, 0.13)
	p.comprobar(absf(float(a["minima"]) - float(b["minima"])) < 0.001 and absf(float(a["maxima"]) - float(b["maxima"])) < 0.001, "orbita.modelo.independiente_del_cuadro")
	var m: Control = _crear(1)
	p.comprobar(m._anterior.size() > 2 and m._dato_anterior.contains("5.500"), "orbita.reintento.conserva_trazo_y_lectura")
	var inicial: float = m.velocidad
	Input.action_press("mover_derecha")
	m._paso(0.1)
	Input.action_release("mover_derecha")
	p.comprobar(m.velocidad > inicial, "orbita.teclado.ajusta_deslizador")
	var evento: InputEventAction = InputEventAction.new()
	evento.action = "interactuar"
	evento.pressed = true
	m._input(evento)
	p.comprobar(m._volando and not m._dial.editable, "orbita.teclado.lanza_y_bloquea_velocidad")
	m.free()
	m = _crear(1)
	await get_tree().process_frame
	var antes: float = m.velocidad
	var punto: Vector2 = m._dial.global_position + Vector2(300, 16)
	_raton(punto, true)
	_raton(punto, false)
	p.comprobar(absf(m.velocidad - antes) > 0.1, "orbita.raton.ajusta_deslizador")
	punto = m._lanzar_boton.get_global_rect().get_center()
	_raton(punto, true)
	_raton(punto, false)
	p.comprobar(m._volando, "orbita.raton.lanza")
	m.free()
	# Captura opcional con trazo anterior y un cuarto de vuelta actual.
	if Juego.args.has("evidencia_orbita"):
		m = _crear(1)
		m._dial.value = 7.547
		m._lanzar_boton.pressed.emit()
		m.tiempo = 5.0
		m._paso(5.0)
		await get_tree().process_frame
		await Interfaz.capturar(String(Juego.args["evidencia_orbita"]))
		m.free()


func _raton(punto: Vector2, pulsado: bool) -> void:
	var movimiento: InputEventMouseMotion = InputEventMouseMotion.new()
	movimiento.position = punto
	get_viewport().push_input(movimiento, true)
	var evento: InputEventMouseButton = InputEventMouseButton.new()
	evento.button_index = MOUSE_BUTTON_LEFT
	evento.position = punto
	evento.pressed = pulsado
	get_viewport().push_input(evento, true)
