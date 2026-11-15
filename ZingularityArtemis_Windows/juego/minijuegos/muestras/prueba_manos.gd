extends Node

# Observa posiciones, sombras, herramienta y bolsas. Solo juega con teclas fisicas.
var p: Node
var final: Dictionary = {}
var devuelto: bool = false
var pulsadas: Dictionary = {}


func correr(pruebas: Node) -> void:
	p = pruebas
	process_mode = Node.PROCESS_MODE_ALWAYS
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	for d in [1, 2, 3]:
		await _partida({"dificultad": d})
	for i in 4:
		await _partida({"dificultad": 1, "muestra": i})
	p.comprobar(not Interfaz.anfitrion.visible, "muestras.manos.anfitrion_cerrado")
	p.comprobar(not get_tree().paused, "muestras.manos.arbol_sin_pausa")
	_soltar()
	Juego.modo_prueba = true


func _lanzar(parametros: Dictionary) -> void:
	final = await Interfaz.abrir_minijuego("muestras", parametros)
	devuelto = true


func _partida(parametros: Dictionary) -> void:
	devuelto = false
	final = {}
	_lanzar(parametros)
	await _real(0.15)
	var m: Control = Interfaz.anfitrion.get("_minijuego")
	var nombre: String = "muestras.manos.d%d.m%d" % [int(parametros.get("dificultad", 1)), int(parametros.get("muestra", -1))]
	if not p.comprobar(m != null and Interfaz.anfitrion.visible, nombre + ".abre"):
		return
	p.comprobar(bool(m.get("pantalla_completa")) and m.size == Vector2(1280, 720), nombre + ".campo_completo")
	p.comprobar(not (Interfaz.anfitrion.get("_titulo") as Control).visible and not (Interfaz.anfitrion.get("_controles") as Control).visible, nombre + ".sin_bordes_del_anfitrion")
	p.comprobar(int(m.get("_auto")) == 0 and int(m.get("_solo")) == 0, nombre + ".sin_piloto")
	await _toque(KEY_ENTER)
	p.comprobar(bool(m.get("activo")), nombre + ".intro_empieza")
	var espera: float = 0.0
	while bool(m.get("activo")) and espera < 115.0:
		if int(m.get("fase")) != 1:
			_soltar()
			await get_tree().process_frame
			espera += get_process_delta_time()
			continue
		var carga: int = m.get("carga")
		var destino: Vector2 = Vector2(32, 108)
		var muestra: Dictionary = {}
		if carga < 0:
			var muestras: Array = m.get("muestras")
			for candidata in muestras:
				var dato: Dictionary = candidata
				if int(dato["estado"]) == 0:
					muestra = dato
					break
			if muestra.is_empty():
				break
			destino = muestra["pos"]
			var id: int = muestra["id"]
			var util: int = 0 if id < 2 else (1 if id == 2 else 2)
			if int(m.get("herramienta")) != util:
				await _toque(KEY_E)
				continue
		var posicion: Vector2 = m.get("posicion")
		var velocidad: Vector2 = m.get("velocidad")
		var diferencia: Vector2 = destino - posicion
		if carga < 0 and diferencia.length() < 9.0:
			_direccion(Vector2.ZERO)
			_tecla(KEY_SPACE, true)
		else:
			_tecla(KEY_SPACE, false)
			# Lee los crateres dibujados, anticipa la deriva y pasa por su borde.
			var constantes: Dictionary = m.get_script().get_script_constant_map()
			var crateres: Array = constantes["CRATERES"]
			var radio: float = [6.0, 8.0, 10.0][int(m.get("dificultad")) - 1]
			var cantidad: int = [3, 4, 5][int(m.get("dificultad")) - 1]
			var rumbo: Vector2 = diferencia.normalized()
			for i in cantidad:
				var centro: Vector2 = crateres[i]
				var offset: Vector2 = centro - posicion
				var frente: float = offset.dot(rumbo)
				var lateral: float = offset.cross(rumbo)
				if frente > 0.0 and frente < minf(42.0, diferencia.length()) and absf(lateral) < radio + 9.0:
					var lado: float = 1.0 if lateral >= 0.0 else -1.0
					diferencia = rumbo * 10.0 + Vector2(-rumbo.y, rumbo.x) * lado * 24.0
					break
			_direccion(diferencia - velocidad * 0.23)
		await get_tree().process_frame
		espera += get_process_delta_time()
	_soltar()
	await _real(0.15)
	var resultado: Dictionary = Interfaz.anfitrion.get("_resultado")
	p.comprobar(bool(resultado.get("superado", false)), nombre + ".superado_con_teclas", str(resultado))
	p.comprobar(int(m.get("vidas")) > 0 and (m.get("entregadas") as Array).size() == int(m.get("objetivo_total")), nombre + ".carga_entregada", "tiempo=%.2f sellos=%d" % [float(m.get("tiempo")), int(m.get("vidas"))])
	if bool(resultado.get("superado", false)):
		await _toque(KEY_ENTER)
	else:
		await _toque(KEY_ESCAPE)
	await _real(0.12)
	p.comprobar(devuelto and not Interfaz.anfitrion.visible, nombre + ".intro_cierra", str(final))
	p.comprobar(not get_tree().paused, nombre + ".sin_pausa")


func _direccion(d: Vector2) -> void:
	_tecla(KEY_RIGHT, d.x > 2.5)
	_tecla(KEY_LEFT, d.x < -2.5)
	_tecla(KEY_DOWN, d.y > 2.5)
	_tecla(KEY_UP, d.y < -2.5)


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


func _real(segundos: float) -> void:
	await get_tree().create_timer(segundos, true, false, true).timeout
