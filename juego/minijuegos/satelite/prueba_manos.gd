extends Node

# Observa piezas y conectores y juega exclusivamente por Input.parse_input_event.
var _resultado: Dictionary = {}
var _devuelto: bool = false
var _pulsadas: Dictionary = {}
var _nivel: int = 1


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	for nivel in [1, 2, 3]:
		_nivel = nivel
		_resultado = {}
		_devuelto = false
		_abrir()
		await _esperar(0.25)
		var mj: Control = Interfaz.anfitrion.get("_minijuego")
		pruebas.comprobar(mj != null and Interfaz.anfitrion.visible, "satelite.manos.d%d.abre" % nivel)
		if mj == null:
			continue
		pruebas.comprobar(bool(mj.get("pantalla_completa")) and mj.size == Vector2(1280, 720), "satelite.manos.d%d.lienzo_completo" % nivel)
		await _toque(KEY_ENTER)
		pruebas.comprobar(bool(mj.get("activo")) and int(mj.get("_auto")) == 0, "satelite.manos.d%d.Empezar_Intro_sin_piloto" % nivel)
		var t: float = 0.0
		var giro: float = 0.0
		var x_inicial: float = float(mj.get("cubo_x"))
		var movido: bool = false
		var giro_visto: bool = false
		var ultima_cara: int = 0
		while bool(mj.get("activo")) and t < 65.0:
			var fase: int = int(mj.get("fase"))
			var x: float = float(mj.get("cubo_x"))
			movido = movido or absf(x - x_inicial) > 10.0
			giro_visto = giro_visto or int(mj.get("cara")) != ultima_cara
			ultima_cara = int(mj.get("cara"))
			var objetivo: float = x
			var tipo_objetivo: int = -1
			var objetos: Array = mj.get("objetos")
			for objeto in objetos:
				var o: Dictionary = objeto
				if int(o["tipo"]) < 5:
					objetivo = float(o["x"])
					tipo_objetivo = int(o["tipo"])
					break
			# Reacciona a la basura visible antes de que alcance el carro.
			for objeto in objetos:
				var o: Dictionary = objeto
				if int(o["tipo"]) == 5 and float(o["y"]) > 125.0 and float(o["y"]) < 150.0 and absf(float(o["x"]) - objetivo) < 22.0:
					objetivo = clampf(float(o["x"]) + (30.0 if x > 136.0 else -30.0), 16.0, 256.0)
			if fase == 2:
				objetivo = float(mj.get("destino"))
			_tecla(KEY_A, fase in [1, 2] and objetivo < x - 1.7)
			_tecla(KEY_D, fase in [1, 2] and objetivo > x + 1.7)
			_tecla(KEY_S, fase == 1)
			if fase == 1 and tipo_objetivo >= 0 and int(mj.get("cara")) != tipo_objetivo and giro <= 0.0:
				_tecla(KEY_E, true)
				giro = 0.22
			else:
				_tecla(KEY_E, fase == 2)
			giro -= 0.035
			await _esperar(0.035)
			t += 0.035
		_soltar()
		await _esperar(0.2)
		var r: Dictionary = Interfaz.anfitrion.get("_resultado")
		pruebas.comprobar(movido and giro_visto, "satelite.manos.d%d.movimiento_y_giro_reales" % nivel)
		pruebas.comprobar(bool(r.get("superado", false)), "satelite.manos.d%d.superado_solo_teclas" % nivel, str(r))
		pruebas.comprobar(_cinco(mj), "satelite.manos.d%d.cinco_subsistemas" % nivel)
		pruebas.comprobar(float(mj.get("enlace")) >= 3.0, "satelite.manos.d%d.senal_encendida" % nivel)
		await _toque(KEY_ENTER)
		await _esperar(0.25)
		pruebas.comprobar(_devuelto and not Interfaz.anfitrion.visible, "satelite.manos.d%d.anfitrion_cerrado" % nivel)
		pruebas.comprobar(not get_tree().paused, "satelite.manos.d%d.arbol_sin_pausa" % nivel)
		if Interfaz.anfitrion.visible:
			await _toque(KEY_ESCAPE)
			await _esperar(0.1)
	Juego.modo_prueba = true


func _cinco(mj: Control) -> bool:
	var montadas: Array = mj.get("montadas")
	return montadas.count(true) == 5


func _abrir() -> void:
	_resultado = await Interfaz.abrir_minijuego("satelite", {"dificultad": _nivel})
	_devuelto = true


func _esperar(s: float) -> void:
	await get_tree().create_timer(s, true, false, true).timeout


func _tecla(codigo: int, pulsada: bool) -> void:
	if bool(_pulsadas.get(codigo, false)) == pulsada:
		return
	_pulsadas[codigo] = pulsada
	var e: InputEventKey = InputEventKey.new()
	e.physical_keycode = codigo
	e.keycode = codigo
	e.pressed = pulsada
	Input.parse_input_event(e)


func _toque(codigo: int) -> void:
	_tecla(codigo, true)
	await _esperar(0.04)
	_tecla(codigo, false)
	await _esperar(0.04)


func _soltar() -> void:
	for codigo in _pulsadas.keys():
		_tecla(int(codigo), false)
