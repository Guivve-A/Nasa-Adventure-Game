extends Node

# Observa el pictograma del marcador, las placas y los animales visibles.
# Todas las acciones pasan por Input.parse_input_event, nunca por el modelo.
var _resultado: Dictionary = {}
var _devuelto: bool = false
var _pulsadas: Dictionary = {}

func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	for nivel in [1, 2, 3]:
		await _manos(pruebas, nivel)
	pruebas.comprobar(not Interfaz.anfitrion.visible, "linea.manos.anfitrion_cerrado")
	pruebas.comprobar(not get_tree().paused, "linea.manos.arbol_sin_pausa")
	Juego.modo_prueba = true

func _abrir(nivel: int) -> void:
	_resultado = await Interfaz.abrir_minijuego("linea_tiempo", {"dificultad": nivel})
	_devuelto = true

func _manos(pruebas: Node, nivel: int) -> void:
	_devuelto = false
	_resultado = {}
	_abrir(nivel)
	for i in 120:
		await get_tree().process_frame
		if Interfaz.anfitrion.visible and Interfaz.anfitrion.get("_capa").visible:
			break
	await _real(0.12)
	var mj: Control = Interfaz.anfitrion.get("_minijuego")
	if not pruebas.comprobar(mj != null, "linea.manos.d%d.abre" % nivel):
		return
	pruebas.comprobar(int(mj.get("_auto")) == 0 and int(mj.get("_solo")) == 0, "linea.manos.d%d.sin_piloto" % nivel)
	pruebas.comprobar(bool(mj.get("pantalla_completa")) and mj.size == Vector2(1280, 720), "linea.manos.d%d.campo_completo" % nivel)
	pruebas.comprobar(not Interfaz.anfitrion.get("_titulo").visible and not Interfaz.anfitrion.get("_controles").visible, "linea.manos.d%d.sin_margenes" % nivel)
	await _toque(KEY_ENTER)
	pruebas.comprobar(bool(mj.get("activo")), "linea.manos.d%d.Empezar_Intro" % nivel)
	var saltos: int = 0
	var max_progreso: int = 0
	var arriba: int = KEY_W if nivel == 2 else KEY_UP
	var abajo: int = KEY_S if nivel == 2 else KEY_DOWN
	var izquierda: int = KEY_A if nivel == 2 else KEY_LEFT
	var derecha: int = KEY_D if nivel == 2 else KEY_RIGHT
	var accion: int = KEY_SPACE if nivel == 2 else KEY_E
	while is_instance_valid(mj) and bool(mj.get("activo")) and float(mj.get("tiempo")) < 110.0:
		var mov: Vector2 = Vector2.ZERO
		var pulsar: bool = false
		if int(mj.get("fase")) == 1 and float(mj.get("descanso")) <= 0.0:
			var siguiente: int = int(mj.get("siguiente"))
			max_progreso = maxi(max_progreso, siguiente)
			var hitos: Array = mj.get("hitos")
			var pendiente: Dictionary = hitos[siguiente]
			var icono_hud: int = int(pendiente["icono"])
			var placas: Array = mj.get("placas")
			var pos: Vector2 = mj.get("jugadora")
			var velocidad: Vector2 = mj.get("velocidad")
			var objetivo: Vector2 = pos
			for placa in placas:
				var hito: Dictionary = hitos[int(placa["hito"])]
				# Compara los dibujos, sin leer anios ni ordenar fichas ocultas.
				if int(placa["fila"]) == siguiente and int(hito["icono"]) == icono_hud:
					objetivo = placa["pos"]
					break
			var diferencia: Vector2 = objetivo - pos - velocidad * 0.09
			mov.x = signf(diferencia.x) if absf(diferencia.x) > 1.0 else 0.0
			mov.y = signf(diferencia.y) if absf(diferencia.y) > 1.0 else 0.0
			if float(mj.get("salto")) <= 0.0:
				pulsar = pos.distance_to(objetivo) < 7.0
				var peligros: Array = mj.get("peligros")
				for peligro in peligros:
					var animal: Vector2 = peligro["pos"]
					var marcha: Vector2 = peligro["vel"]
					if (animal + marcha * 0.24).distance_to(pos) < 13.0:
						pulsar = true
		_tecla(izquierda, mov.x < 0)
		_tecla(derecha, mov.x > 0)
		_tecla(arriba, mov.y > 0)
		_tecla(abajo, mov.y < 0)
		if pulsar and not bool(_pulsadas.get(accion, false)):
			saltos += 1
		_tecla(accion, pulsar)
		await get_tree().process_frame
	_soltar()
	await _real(0.15)
	var resultado: Dictionary = Interfaz.anfitrion.get("_resultado")
	pruebas.comprobar(bool(resultado.get("superado", false)), "linea.manos.d%d.gana_solo_teclas" % nivel, str(resultado))
	pruebas.comprobar(saltos >= 9 and max_progreso >= 8, "linea.manos.d%d.nueve_saltos_reales" % nivel, "saltos=%d progreso=%d" % [saltos, max_progreso])
	print("LINEA_MANOS nivel=%d saltos=%d tiempo=%.2f vidas=%d" % [nivel, saltos, float(mj.get("tiempo")), int(mj.get("vidas"))])
	await _toque(KEY_ENTER)
	for i in 120:
		await get_tree().process_frame
		if _devuelto:
			break
	pruebas.comprobar(_devuelto and not Interfaz.anfitrion.visible, "linea.manos.d%d.Continuar_Intro_cierra" % nivel)
	pruebas.comprobar(bool(_resultado.get("superado", false)) and not get_tree().paused, "linea.manos.d%d.devuelve_victoria_sin_pausa" % nivel, str(_resultado))

func _tecla(codigo: int, abajo: bool) -> void:
	if bool(_pulsadas.get(codigo, false)) == abajo:
		return
	_pulsadas[codigo] = abajo
	var evento: InputEventKey = InputEventKey.new()
	evento.physical_keycode = codigo
	evento.keycode = codigo
	evento.pressed = abajo
	Input.parse_input_event(evento)

func _soltar() -> void:
	for codigo in _pulsadas.keys():
		_tecla(int(codigo), false)

func _toque(codigo: int) -> void:
	_tecla(codigo, true)
	await get_tree().process_frame
	await get_tree().physics_frame
	_tecla(codigo, false)
	await _real(0.08)

func _real(segundos: float) -> void:
	await get_tree().create_timer(segundos, true, false, true).timeout
