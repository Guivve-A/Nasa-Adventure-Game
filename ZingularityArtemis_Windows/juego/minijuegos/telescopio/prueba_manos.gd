extends Node

# Solo observa el visor, la aguja y la diana dibujados; solo actua con teclas.
var pulsadas: Dictionary = {}
var resultado: Dictionary = {}
var listo: bool = false


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	for nivel in [1, 2, 3]:
		await _partida(pruebas, nivel)
	_soltar()
	pruebas.comprobar(not get_tree().paused, "telescopio.manos.arbol_sin_pausa")
	Juego.modo_prueba = true


func _abrir(nivel: int) -> void:
	resultado = await Interfaz.abrir_minijuego("telescopio", {"dificultad": nivel})
	listo = true


func _partida(p: Node, nivel: int) -> void:
	listo = false
	resultado = {}
	_abrir(nivel)
	await get_tree().create_timer(0.2, true, false, true).timeout
	var m: Control = Interfaz.anfitrion.get("_minijuego")
	if not p.comprobar(m != null and Interfaz.anfitrion.visible, "telescopio.d%d.abierto" % nivel):
		return
	p.comprobar(bool(m.get("pantalla_completa")) and m.size == Vector2(1280, 720), "telescopio.d%d.campo_completo" % nivel)
	p.comprobar(int(m.get("_auto")) == 0 and int(m.get("_solo")) == 0, "telescopio.d%d.sin_piloto" % nivel)
	await _toque(KEY_ENTER)
	var titulo: Control = Interfaz.anfitrion.get("_titulo")
	var controles: Control = Interfaz.anfitrion.get("_controles")
	p.comprobar(not titulo.visible and not controles.visible, "telescopio.d%d.sin_marco_exterior" % nivel)
	p.comprobar(bool(m.get("activo")), "telescopio.d%d.intro_empieza" % nivel)
	var limite: float = 100.0
	var etapas: Dictionary = {}
	var marcas: int = 0
	while is_instance_valid(m) and bool(m.get("activo")) and limite > 0:
		var etapa: int = int(m.get("etapa"))
		etapas[etapa] = true
		marcas = maxi(marcas, int(m.get("rasgo")))
		var diferencia: Vector2 = Vector2.ZERO
		var velocidad: Vector2 = m.get("velocidad")
		if etapa == 0:
			var luna: Vector2 = m.get("luna_mundo")
			var visor: Vector2 = m.get("visor")
			diferencia = luna - visor
		elif etapa == 2:
			var diana: Vector2 = m.get("diana")
			var mira: Vector2 = m.get("mira")
			diferencia = diana - mira
		var freno: Vector2 = diferencia - velocidad * 0.10
		var izq: int = KEY_A if nivel == 2 else KEY_LEFT
		var der: int = KEY_D if nivel == 2 else KEY_RIGHT
		var arriba: int = KEY_W if nivel == 2 else KEY_UP
		var abajo: int = KEY_S if nivel == 2 else KEY_DOWN
		_tecla(izq, freno.x < -0.8 and etapa in [0, 2])
		_tecla(der, freno.x > 0.8 and etapa in [0, 2])
		_tecla(arriba, freno.y < -0.8 and etapa in [0, 2])
		_tecla(abajo, freno.y > 0.8 and etapa in [0, 2])
		var accion: int = KEY_SPACE if nivel == 3 else KEY_E
		if etapa == 0 and diferencia.length() < 3 and velocidad.length() < 15:
			await _toque(accion)
		elif etapa == 1:
			_tecla(accion, false)
			if float(m.get("t_etapa")) > 1 and absf(float(m.get("enfoque")) - 0.5) < float(m.get("ventana_foco")) * 0.5:
				await _toque(accion)
		elif etapa == 2:
			_tecla(accion, diferencia.length() < float(m.get("margen")) * 0.7)
		else:
			_tecla(accion, false)
		await get_tree().process_frame
		limite -= get_process_delta_time()
	_soltar()
	await get_tree().create_timer(0.15, true, false, true).timeout
	var r: Dictionary = Interfaz.anfitrion.get("_resultado")
	var gano: bool = bool(r.get("superado", false))
	p.comprobar(gano, "telescopio.d%d.gana_con_teclas" % nivel, str(r))
	p.comprobar(etapas.has(0) and etapas.has(1) and etapas.has(2) and marcas == 3, "telescopio.d%d.tres_rasgos_y_enfoque" % nivel)
	print("TELESCOPIO_MANOS d%d %s" % [nivel, str(r)])
	if gano:
		await _toque(KEY_ENTER)
	else:
		await _toque(KEY_ESCAPE)
	for i in 180:
		if listo and not Interfaz.anfitrion.visible:
			break
		await get_tree().process_frame
	p.comprobar(listo and not Interfaz.anfitrion.visible, "telescopio.d%d.anfitrion_cerrado" % nivel)
	p.comprobar(not get_tree().paused, "telescopio.d%d.sin_pausa" % nivel)


func _tecla(codigo: int, abajo: bool) -> void:
	if bool(pulsadas.get(codigo, false)) == abajo:
		return
	pulsadas[codigo] = abajo
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


func _soltar() -> void:
	for codigo in pulsadas.keys():
		_tecla(int(codigo), false)
