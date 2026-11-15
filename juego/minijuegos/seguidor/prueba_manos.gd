extends Node

# Lee posicion y deslizamiento; solo actua mediante teclas fisicas.
var pulsadas: Dictionary = {}
var final: Dictionary = {}
var devuelto: bool = false


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	await _partida(pruebas, false)
	await _partida(pruebas, true)
	Juego.modo_prueba = true


func _lanzar(parametros: Dictionary) -> void:
	final = await Interfaz.abrir_minijuego("seguidor", parametros)
	devuelto = true


func _partida(pruebas: Node, ayuda: bool) -> void:
	final = {}
	devuelto = false
	var parametros: Dictionary = {"dificultad": 1}
	if ayuda:
		parametros["modo"] = "prealimentacion"
	_lanzar(parametros)
	var limite := 5.0
	while not Interfaz.anfitrion.visible and limite > 0.0:
		await _real(0.1)
		limite -= 0.1
	await _real(0.15)
	var m: Control = Interfaz.anfitrion.get("_minijuego")
	var nombre := "seguidor.manos.cielo" if ayuda else "seguidor.manos.normal"
	pruebas.comprobar(m != null and Interfaz.anfitrion.visible, nombre + ".abierto", str(parametros))
	if m == null:
		return
	pruebas.comprobar(int(m.get("_auto")) == 0 and int(m.get("_solo")) == 0, nombre + ".sin_piloto", "Entrada fisica")
	pruebas.comprobar(m.size == Vector2(1280, 720), nombre + ".pantalla_completa", str(m.size))
	await _toque(KEY_ENTER)
	limite = 110.0
	while is_instance_valid(m) and bool(m.get("activo")) and limite > 0.0:
		if int(m.get("fase")) == 2:
			if ayuda and not bool(m.get("cielo")):
				await _toque(KEY_E)
			var error: float = float(m.get("luna_x")) - float(m.get("visor_x"))
			var velocidad: float = float(m.get("visor_v"))
			var deriva: float = float(m.get("vel_cielo"))
			# Impulsos de una decima; anticipa el frenado mirando el deslizamiento.
			var sobra := velocidad - deriva
			var orden := 6.0 * error - 3.5 * sobra
			_tecla(KEY_D, orden > 8.0)
			_tecla(KEY_A, orden < -8.0)
			var base: float = deriva if bool(m.get("cielo")) else 0.0
			_tecla(KEY_SPACE, absf(sobra) > 20.0 and (velocidad - base) * sobra > 0.0 and absf(error) < 0.45 * absf(sobra) + 4.0)
		await _real(0.1)
		limite -= 0.1
	for codigo in pulsadas.keys():
		_tecla(int(codigo), false)
	await _real(0.3)
	var resultado: Dictionary = Interfaz.anfitrion.get("_resultado")
	pruebas.comprobar(bool(resultado.get("superado", false)), nombre + ".superado", str(resultado))
	print("MANOS ", nombre, " ", resultado)
	await _toque(KEY_ENTER)
	await _real(0.3)
	pruebas.comprobar(devuelto and bool(final.get("superado", false)), nombre + ".resultado_devuelto", str(final))
	pruebas.comprobar(not Interfaz.anfitrion.visible, nombre + ".anfitrion_cerrado", str(Interfaz.anfitrion.visible))
	pruebas.comprobar(not get_tree().paused, nombre + ".arbol_sin_pausa", str(get_tree().paused))
	if ayuda:
		var cuaderno: Array = Juego.estado.get("cuaderno", [])
		pruebas.comprobar(cuaderno.has("prealimentacion"), nombre + ".ficha_anotada", str(cuaderno))


func _tecla(codigo: int, abajo: bool) -> void:
	if bool(pulsadas.get(codigo, false)) == abajo:
		return
	pulsadas[codigo] = abajo
	var evento := InputEventKey.new()
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
