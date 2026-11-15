extends Node

# Se mira la aguja dibujada; nunca se escribe en el estado del vuelo.
var pulsadas: Dictionary = {}
var final: Dictionary = {}
var devuelto: bool = false


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	for nivel in [1, 3]:
		await _partida(pruebas, nivel)
	Juego.modo_prueba = true


func _abrir(nivel: int) -> void:
	final = await Interfaz.abrir_minijuego("orbita", {"dificultad": nivel})
	devuelto = true


func _partida(pruebas: Node, nivel: int) -> void:
	final = {}
	devuelto = false
	_abrir(nivel)
	await _real(0.3)
	var m: Control = Interfaz.anfitrion.get("_minijuego")
	var nombre: String = "orbita.manos.d%d" % nivel
	pruebas.comprobar(m != null, nombre + ".abierto")
	if m == null:
		return
	pruebas.comprobar(int(m.get("_auto")) == 0 and int(m.get("_solo")) == 0, nombre + ".sin_piloto")
	pruebas.comprobar(m.size == Vector2(1280, 720), nombre + ".pantalla_completa")
	await _toque(KEY_ENTER)
	var limite: float = 125.0
	var pulsos: int = 0
	var frenadas: int = 0
	while is_instance_valid(m) and bool(m.get("activo")) and limite > 0.0:
		var aguja: float = float(m.get("guia"))
		var jugando: bool = int(m.get("fase")) == 1
		if jugando and aguja > 0.012:
			pulsos += 1
		if jugando and aguja < -0.012:
			frenadas += 1
		_tecla(KEY_E, jugando and aguja > 0.012)
		_tecla(KEY_DOWN, jugando and aguja < -0.012)
		await _real(0.06)
		limite -= 0.06
	_tecla(KEY_E, false)
	_tecla(KEY_DOWN, false)
	await _real(0.3)
	var resultado: Dictionary = Interfaz.anfitrion.get("_resultado")
	pruebas.comprobar(bool(resultado.get("superado", false)), nombre + ".superado", str(resultado))
	pruebas.comprobar(pulsos > 0 and frenadas > 0, nombre + ".motor_y_freno", "%d / %d" % [pulsos, frenadas])
	print("MANOS ", nombre, " ", resultado)
	if bool(resultado.get("superado", false)):
		await _toque(KEY_ENTER)
	else:
		await _toque(KEY_ESCAPE)
	await _real(0.3)
	pruebas.comprobar(devuelto and bool(final.get("superado", false)), nombre + ".resultado_devuelto", str(final))
	pruebas.comprobar(not Interfaz.anfitrion.visible, nombre + ".anfitrion_cerrado")
	pruebas.comprobar(not get_tree().paused, nombre + ".arbol_sin_pausa")


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


func _real(segundos: float) -> void:
	await get_tree().create_timer(segundos, true, false, true).timeout
