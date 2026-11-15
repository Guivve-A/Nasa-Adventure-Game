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
	_resultado = await Interfaz.abrir_minijuego("antena", {"dificultad": 1})
	_devuelto = true


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	_abrir.call_deferred()
	var limite: float = 5.0
	while not Interfaz.anfitrion.visible and limite > 0.0:
		await _real(0.05)
		limite -= 0.05
	pruebas.comprobar(Interfaz.anfitrion.visible, "antena.manos.abierto", "Apertura por Interfaz")
	await _real(0.3)
	await _toque(KEY_ENTER)
	await _real(0.2)
	var mj: Control = Interfaz.anfitrion.get("_minijuego")
	pruebas.comprobar(mj != null and bool(mj.get("activo")), "antena.manos.empezar_intro", "Intro activa la partida")
	pruebas.comprobar(mj != null and mj.size == Vector2(1280, 720), "antena.manos.campo_completo", "1280 x 720")
	pruebas.comprobar(mj != null and int(mj.get("_auto")) == 0, "antena.manos.sin_piloto", "Solo InputEventKey")
	limite = 90.0
	while limite > 0.0 and is_instance_valid(mj) and bool(mj.get("activo")):
		# Solo lee lo visible: plato, trayectoria, movimiento y flecha de entrada.
		var objetivo: float = float(mj.get("lado")) * 82.0
		if not bool(mj.get("sat_fuera")):
			objetivo = float(mj.get("sat_ang")) + float(mj.get("sat_vel")) * 0.10
		var falta: float = objetivo - float(mj.get("antena")) - float(mj.get("vel")) * 0.16
		_tecla(KEY_D, falta > 1.0)
		_tecla(KEY_A, falta < -1.0)
		# Haz ancho: la dificultad inicial debe admitir ganar sin el extra de E.
		await get_tree().process_frame
		limite -= get_process_delta_time()
	_tecla(KEY_A, false)
	_tecla(KEY_D, false)
	await _real(0.3)
	var resultado: Dictionary = Interfaz.anfitrion.get("_resultado")
	pruebas.comprobar(bool(resultado.get("superado", false)), "antena.manos.superado", str(resultado))
	if is_instance_valid(mj):
		print("ANTENA_MANOS paquetes=%s por_pasada=%s enlace=%.2f visible=%.2f" % [str(mj.get("paquetes")), str(mj.get("por_pasada")), float(mj.get("t_enlace")), float(mj.get("t_visible"))])
	await _toque(KEY_ENTER)
	await _real(0.4)
	pruebas.comprobar(_devuelto and bool(_resultado.get("superado", false)), "antena.manos.resultado_devuelto", str(_resultado))
	pruebas.comprobar(not Interfaz.anfitrion.visible, "antena.manos.anfitrion_cerrado", "Continuar con Intro")
	pruebas.comprobar(not get_tree().paused, "antena.manos.arbol_sin_pausa", "Interfaz devuelve el control")
	Juego.modo_prueba = true
