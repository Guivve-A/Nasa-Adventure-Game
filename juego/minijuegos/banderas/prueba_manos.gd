extends Node

var _pulsadas: Dictionary = {}
var _resultado: Dictionary = {}
var _devuelto: bool = false


func _real(segundos: float) -> void:
	await get_tree().create_timer(segundos, true, false, true).timeout


func _tecla(codigo: int, abajo: bool) -> void:
	if bool(_pulsadas.get(codigo, false)) == abajo:
		return
	_pulsadas[codigo] = abajo
	var evento: InputEventKey = InputEventKey.new()
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


func _abrir() -> void:
	_resultado = await Interfaz.abrir_minijuego("banderas", {"dificultad": 1})
	_devuelto = true


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	_abrir.call_deferred()
	var espera: float = 5.0
	while not Interfaz.anfitrion.visible and espera > 0.0:
		await _real(0.05)
		espera -= 0.05
	pruebas.comprobar(Interfaz.anfitrion.visible, "banderas.manos.abierto", "Apertura por Interfaz")
	await _real(0.3)
	await _toque(KEY_ENTER)
	await _real(0.2)
	var mj: Control = Interfaz.anfitrion.get("_minijuego")
	pruebas.comprobar(mj != null and bool(mj.get("activo")), "banderas.manos.empezar_intro", "Intro empieza la partida")
	pruebas.comprobar(mj != null and mj.size == Vector2(1280, 720), "banderas.manos.campo_completo", "320 x 180 pixeles x4")
	pruebas.comprobar(mj != null and int(mj.get("_auto")) == 0, "banderas.manos.sin_piloto", "Solo teclas fisicas")
	var limite: float = 110.0
	var visto: Array[bool] = [false, false, false, false]
	var integras: bool = true
	while limite > 0.0 and is_instance_valid(mj) and bool(mj.get("activo")):
		var fase: int = int(mj.get("fase"))
		visto[fase] = true
		var bases: Array[int] = mj.MASTIL_X
		var suelo: Array[int] = mj.BASE_Y
		var golpes: Array[int] = mj.get("golpes")
		var fijadas: Array[bool] = mj.get("fijada")
		var alturas: Array[float] = mj.get("alt")
		var velocidad_alt: Array[float] = mj.get("alt_v")
		integras = integras and bool(mj.telas_integras())
		var obj: int = 0
		if fase == 0:
			obj = 0 if golpes[0] < int(mj.get("necesarios")) else 1
		elif fase == 1:
			obj = 1 if not fijadas[1] else 0
		# En nivelacion volvemos al mastil izquierdo y miramos las dos lineas.
		var dx: float = float(bases[obj]) - float(mj.PUESTO) - float(mj.get("astro_x"))
		var vx: float = float(mj.get("astro_v"))
		var deseada: float = clampf(dx * 5.0, -48.0, 48.0)
		var mover: float = 0.0
		if absf(dx) > 1.5 and absf(deseada - vx) > 4.0:
			mover = signf(deseada - vx)
		var listo: bool = absf(dx) < 5.0
		var e: bool = false
		var vertical: float = 0.0
		if float(mj.get("cartel")) <= 0.0 and fase < 3:
			if fase == 0:
				var marcas: Array[float] = mj.get("marca")
				e = listo and float(mj.get("enfriar")) <= 0.0 and not bool(mj.get("c_e_antes")) and absf(marcas[obj] - 0.5) < 0.06
			elif fase == 1:
				var barras: Array[float] = mj.get("barra")
				if int(mj.get("tirando")) == obj:
					e = barras[obj] < 37.5
					mover = 0.0
				elif listo and absf(vx) < 4.0 and not fijadas[obj]:
					e = not bool(mj.get("c_e_antes"))
			elif fase == 2 and listo:
				var falta: float = alturas[1] + float(suelo[0] - suelo[1]) - alturas[0]
				var deseada_y: float = clampf(falta * 4.0, -16.0, 16.0)
				if absf(falta) > 0.15 and absf(deseada_y - velocidad_alt[0]) > 1.0:
					vertical = signf(deseada_y - velocidad_alt[0])
		else:
			mover = 0.0
		_tecla(KEY_D, mover > 0.0)
		_tecla(KEY_A, mover < 0.0)
		_tecla(KEY_W, vertical > 0.0)
		_tecla(KEY_S, vertical < 0.0)
		# Alterna las dos teclas anunciadas sin acceder a los mandos internos.
		_tecla(KEY_E, e and obj == 0)
		_tecla(KEY_SPACE, e and obj == 1)
		await get_tree().process_frame
		limite -= get_process_delta_time()
	for codigo in _pulsadas.keys():
		_tecla(int(codigo), false)
	await _real(0.3)
	var resultado: Dictionary = Interfaz.anfitrion.get("_resultado")
	pruebas.comprobar(bool(resultado.get("superado", false)), "banderas.manos.superado", str(resultado))
	pruebas.comprobar(visto == [true, true, true, true], "banderas.manos.tres_misiones_y_amanecer", str(visto))
	pruebas.comprobar(integras, "banderas.manos.banderas_integras", "Siempre en pie y sin tocar el suelo")
	if is_instance_valid(mj):
		print("BANDERAS_MANOS tiempo=%.2f vidas=%d golpes=%s barras=%s alturas=%s" % [float(mj.get("tiempo")), int(mj.get("vidas")), str(mj.get("golpes")), str(mj.get("barra")), str(mj.get("alt"))])
	await _toque(KEY_ENTER)
	await _real(0.4)
	pruebas.comprobar(_devuelto and bool(_resultado.get("superado", false)), "banderas.manos.resultado_devuelto", str(_resultado))
	pruebas.comprobar(not Interfaz.anfitrion.visible, "banderas.manos.anfitrion_cerrado", "Continuar con Intro")
	pruebas.comprobar(not get_tree().paused, "banderas.manos.arbol_sin_pausa", "Control devuelto al juego")
	Juego.modo_prueba = true
