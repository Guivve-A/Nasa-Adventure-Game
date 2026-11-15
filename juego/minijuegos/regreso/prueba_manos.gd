extends Node

# Solo observa la partida y pulsa teclas fisicas; nunca modifica la simulacion.
var _pulsadas: Dictionary = {}
var _resultado: Dictionary = {}
var _cerrado: bool = false


func _tecla(codigo: int, abajo: bool) -> void:
	if bool(_pulsadas.get(codigo, false)) == abajo:
		return
	_pulsadas[codigo] = abajo
	var evento: InputEventKey = InputEventKey.new()
	evento.physical_keycode = codigo
	evento.keycode = codigo
	evento.pressed = abajo
	Input.parse_input_event(evento)


func _real(segundos: float) -> void:
	await get_tree().create_timer(segundos, true, false, true).timeout


func _toque(codigo: int) -> void:
	_tecla(codigo, true)
	await _real(0.06)
	_tecla(codigo, false)
	await _real(0.06)


func _abrir() -> void:
	_resultado = await Interfaz.abrir_minijuego("regreso", {"dificultad": 1})
	_cerrado = true


func _carril(m: Control) -> float:
	var x: float = m.get("cap_x")
	var prof: float = m.get("prof")
	var mejor: float = x
	var costo_mejor: float = INF
	var bolsas: Array = m.get("bolsas")
	for candidato in range(18, 283, 4):
		var costo: float = absf(candidato - x) + absf(candidato - 160.0) * 0.05
		for dato in bolsas:
			var bolsa: Dictionary = dato
			var distancia: float = float(bolsa["prof"]) - prof
			if not bool(bolsa["viva"]) or distancia < -float(bolsa["r"]) - 6.0:
				continue
			var holgura: float = absf(float(bolsa["x"]) - candidato) - float(bolsa["r"]) - 11.0
			if holgura < 0.0:
				costo += 300.0 + 6000.0 / (distancia + float(bolsa["r"]) + 30.0) - holgura * 4.0
		if costo < costo_mejor:
			costo_mejor = costo
			mejor = candidato
	return mejor


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	_abrir.call_deferred()
	var limite: int = Time.get_ticks_msec() + 10000
	while not Interfaz.anfitrion.visible and Time.get_ticks_msec() < limite:
		await get_tree().process_frame
	await _real(0.2)
	await _toque(KEY_ENTER)
	var m: Control = Interfaz.anfitrion.get("_minijuego")
	pruebas.comprobar(m != null and bool(m.get("activo")), "regreso.manos.empezar_intro", "Intro inicia la partida")
	if m == null:
		Juego.modo_prueba = true
		return
	pruebas.comprobar(m.size == Vector2(1280, 720) and bool(m.get("pantalla_completa")), "regreso.manos.pantalla_completa", str(m.size))
	limite = Time.get_ticks_msec() + 100000
	var calor_max: float = 0.0
	while bool(m.get("activo")) and Time.get_ticks_msec() < limite:
		var fase: int = m.get("fase")
		var x: float = m.get("cap_x")
		var vx: float = m.get("cap_vx")
		var angulo: float = m.get("angulo")
		var giro: float = m.get("giro")
		var mando: float = 0.0
		calor_max = maxf(calor_max, float(m.get("calor")))
		if fase == 1 or fase == 2:
			var destino: float = _carril(m) if fase == 1 else x
			var objetivo: float = clampf((destino - x) * 0.9 - vx * 0.8, -18.0, 18.0)
			var falta: float = objetivo - angulo - giro * 0.16
			mando = signf(falta) if absf(falta) > 1.5 else 0.0
		elif fase == 3:
			var falta: float = float(m.get("diana_x")) - x - vx * 0.6
			mando = signf(falta) if absf(falta) > 1.5 else 0.0
		_tecla(KEY_A, mando < 0.0)
		_tecla(KEY_D, mando > 0.0)
		var abrir: bool = fase == 2 and float(m.get("prof")) >= float(m.get("franja_ini")) + 4.0
		_tecla(KEY_E, abrir)
		await _real(0.04)
	for codigo in _pulsadas.keys():
		_tecla(int(codigo), false)
	var final: Dictionary = Interfaz.anfitrion.get("_resultado")
	print("REGRESO_MANOS calor_max=%.2f golpes=%d esquivadas=%d x=%.2f diana=%.2f tiempo=%.2f" % [calor_max, int(m.get("golpes")), int(m.get("esquivadas")), float(m.get("cap_x")), float(m.get("diana_x")), float(m.get("tiempo"))])
	pruebas.comprobar(bool(final.get("superado", false)), "regreso.manos.superado", str(final))
	await _real(0.25)
	# En victoria el primer boton es Continuar; en fallo se sale con Esc.
	await _toque(KEY_ENTER if bool(final.get("superado", false)) else KEY_ESCAPE)
	limite = Time.get_ticks_msec() + 5000
	while not _cerrado and Time.get_ticks_msec() < limite:
		await get_tree().process_frame
	pruebas.comprobar(_cerrado and not Interfaz.anfitrion.visible, "regreso.manos.anfitrion_cerrado", str(_resultado))
	pruebas.comprobar(not get_tree().paused, "regreso.manos.arbol_sin_pausa", "El mundo recupera su proceso")
	Juego.modo_prueba = true
