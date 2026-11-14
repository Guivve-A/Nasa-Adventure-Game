extends "res://nucleo/minijuego.gd"

# Las dimensiones proceden de pegaso/cubesat. El montaje y la energia son didacticos.
# u = unidades inventadas para el modelo, nunca prestaciones reales de Pegaso.
const LIMITE_S: float = 180.0
const TRAMO_S: float = 4.0
const CAPACIDAD: float = 4.0
const COSTE_PC: int = 2
const COSTE_RADIO: int = 3
const PIEZAS: Array[String] = ["Energía y paneles", "Radio", "Antena", "Computadora"]
const FUNCIONES: Array[String] = ["Captar luz", "Enviar datos", "Enlace a tierra", "Ordenar datos"]

var fase: int = 0 # 0 montaje, 1 ajustes, 2 sol, 3 sombra
var piezas: Array[int] = [-1, -1, -1, -1]
var seleccion: int = 0
var hueco: int = 0
var tomada: bool = false
var paneles: int = 0
var antena: bool = false
var computadora: bool = true
var radio_sol: bool = true
var radio_sombra: bool = true
var bateria: float = 0.0
var carga_al_sol: float = 0.0
var transcurrido: float = 0.0
var _auto: int = 0
var _pulso: float = 0.0
var _arrastrando: bool = false
var _cursor: Vector2 = Vector2.ZERO
var _mensaje: String = "Elige una pieza. Los huecos indican su función."
var _cabecera: Label
var _lectura: Label
var _estado: Label
var _nota: Label
var _accion: Button
var _ajustes: Array[Button] = []


func _preparar() -> void:
	_cabecera = _etiqueta("", Vector2(24, 10), 1072, 22)
	_etiqueta("Pegaso: primer satélite ecuatoriano · Cubo de 10 cm · 2 paneles de 27 cm", Vector2(24, 45), 1072, 18)
	_nota = _etiqueta("", Vector2(650, 86), 418, 20)
	for i in 5:
		var b: Button = Estilo.boton("", 18)
		b.position = Vector2(632, 82 + i * 53)
		b.size = Vector2(464, 46)
		b.focus_mode = Control.FOCUS_NONE
		b.pressed.connect(_pulsar_ajuste.bind(i))
		add_child(b)
		_ajustes.append(b)
	_lectura = _etiqueta("", Vector2(40, 355), 556, 18)
	_estado = _etiqueta("", Vector2(632, 355), 464, 18)
	_accion = Estilo.boton("", 18, true)
	_accion.position = Vector2(790, 466)
	_accion.size = Vector2(306, 44)
	_accion.focus_mode = Control.FOCUS_NONE
	_accion.pressed.connect(_confirmar)
	add_child(_accion)
	_etiqueta("EXA: presentada el 29-08-2007.\nInició actividades el 01-11-2007.", Vector2(24, 466), 726, 16)
	_refrescar()


func _etiqueta(contenido: String, pos: Vector2, ancho: float, tam: int) -> Label:
	var l: Label = texto(contenido, tam, Estilo.TINTA)
	l.position = pos
	l.custom_minimum_size = Vector2(ancho, 0)
	add_child(l)
	return l


func _empezar() -> void:
	_refrescar()


func _rect_pieza(i: int) -> Rect2:
	return Rect2(24, 105 + i * 59, 224, 50)


func _rect_hueco(i: int) -> Rect2:
	return Rect2(337 + (i % 2) * 102, 178 + (i / 2) * 74, 94, 66)


func _mover(direccion: int) -> void:
	if fase == 0:
		if tomada:
			hueco = posmod(hueco + direccion, 4)
		else:
			seleccion = posmod(seleccion + direccion, 4)
	elif fase == 1:
		seleccion = posmod(seleccion + direccion, 5)
	_refrescar()


func _tomar_o_colocar() -> void:
	if fase != 0:
		if fase == 1:
			_cambiar(seleccion, 1)
		return
	if not tomada:
		tomada = true
		_mensaje = "Llevas %s. Elige un hueco y pulsa E." % PIEZAS[seleccion]
	else:
		_colocar()
	_refrescar()


func _colocar() -> void:
	if not tomada:
		return
	if seleccion != hueco:
		_mensaje = "%s no cumple «%s». Busca el hueco de su función." % [PIEZAS[seleccion], FUNCIONES[hueco]]
		sonar("pagina")
	else:
		piezas[hueco] = seleccion
		_mensaje = "%s instalada: %s." % [PIEZAS[seleccion], FUNCIONES[hueco].to_lower()]
		sonar("tic")
	tomada = false
	_arrastrando = false


func _pulsar_ajuste(i: int) -> void:
	if activo and fase == 1:
		seleccion = i
		_cambiar(i, 1)


func _cambiar(i: int, direccion: int) -> void:
	if fase != 1:
		return
	match i:
		0: paneles = posmod(paneles + direccion, 3)
		1: antena = not antena
		2: computadora = not computadora
		3: radio_sol = not radio_sol
		4: radio_sombra = not radio_sombra
	_refrescar()


func _generado() -> int:
	if paneles == 0:
		return 2
	if paneles == 1:
		return 5 if dificultad == 1 else 4
	return 11 - dificultad


func _consumo(sombra: bool) -> int:
	var radio: bool = radio_sombra if sombra else radio_sol
	return (COSTE_PC if computadora else 0) + (COSTE_RADIO if radio else 0)


func _confirmar() -> void:
	if not activo:
		return
	if fase == 0:
		for i in 4:
			if piezas[i] != i:
				_mensaje = "Falta %s: sin esta pieza no puedes %s." % [PIEZAS[i].to_lower(), FUNCIONES[i].to_lower()]
				_refrescar()
				return
		fase = 1
		seleccion = 0
		tomada = false
		_mensaje = "Ajusta una fila cada vez. Después prueba el ciclo."
	elif fase == 1:
		if not computadora:
			_final(false, "Sin computadora encendida nadie ordena los datos ni dirige los equipos.")
			return
		if not antena:
			_final(false, "Sin antena desplegada la radio no llega a tierra: falta el enlace para enviar datos.")
			return
		if not radio_sol:
			_final(false, "La radio está apagada al sol: la computadora prepara datos, pero nadie los envía a tierra.")
			return
		fase = 2
		transcurrido = 0.0
		bateria = 0.0
	_refrescar()


func _paso(delta: float) -> void:
	if fase >= 2:
		_simular(delta)
	elif _auto != 0:
		_pulso += delta
		if _pulso >= 0.28:
			_pulso = 0.0
			_piloto()
	if activo and tiempo >= LIMITE_S:
		var causa: String = "Faltan piezas: el kit aún no puede captar luz, ordenar y transmitir datos." if fase == 0 else "El ciclo no se probó en 180 s: hay que comprobar la carga al sol y el gasto en sombra."
		_final(false, causa)
	_refrescar()


func _simular(delta: float) -> void:
	# Cada tramo dura 4 s de juego. Integra solo el tiempo restante de cada fase.
	var restante: float = delta
	while restante > 0.0 and activo and fase >= 2:
		var paso: float = minf(restante, TRAMO_S - transcurrido)
		var saldo: int = _generado() - _consumo(false) if fase == 2 else -_consumo(true)
		if fase == 2:
			bateria = clampf(bateria + float(saldo) * paso / TRAMO_S, 0.0, CAPACIDAD)
		else:
			bateria += float(saldo) * paso / TRAMO_S
		transcurrido += paso
		restante -= paso
		if fase == 3 and bateria < -0.001:
			_final(false, "La sombra exige %d u y solo guardaste %.0f u: la batería se agota. Apaga la radio en sombra." % [_consumo(true), carga_al_sol])
		elif transcurrido >= TRAMO_S - 0.00001:
			if fase == 2:
				if _generado() < _consumo(false):
					_final(false, "Consumes %d u al sol y los paneles generan %d u: falta energía para operar y cargar. Despliega más paneles." % [_consumo(false), _generado()])
				else:
					carga_al_sol = bateria
					fase = 3
					transcurrido = 0.0
			else:
				_final(true, "Las 4 piezas funcionan: generas %d u, consumes %d u al sol y guardas %.0f u; en sombra gastas %d u. Modelo simplificado." % [_generado(), _consumo(false), carga_al_sol, _consumo(true)])


func _final(gana: bool, causa: String) -> void:
	print("SATELITE d%d fase=%d paneles=%d bateria=%.3f juego=%.3f" % [dificultad, fase, paneles, bateria, tiempo])
	terminar(gana, 100.0 if gana else 0.0, causa)


func _piloto() -> void:
	# Usa las mismas operaciones de cursor, toma, colocacion y ajuste que la persona.
	if fase == 0:
		if tomada:
			if hueco != seleccion:
				_mover(1)
			else:
				_tomar_o_colocar()
		else:
			for i in 4:
				if piezas[i] != i:
					if seleccion != i:
						_mover(1)
					else:
						_tomar_o_colocar()
					return
			_confirmar()
	elif fase == 1:
		if paneles < 2:
			_cambiar(0, 1)
		elif not antena and _auto > 0:
			_cambiar(1, 1)
		elif radio_sombra:
			_cambiar(4, 1)
		else:
			# El camino de fallo conserva plegada la antena y prueba de verdad.
			_confirmar()


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1
	_pulso = 0.0


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or fase >= 2:
		return
	if evento.is_action_pressed("saltar"):
		_confirmar()
	elif evento.is_action_pressed("interactuar"):
		_tomar_o_colocar()
	elif evento.is_action_pressed("mover_arriba"):
		_mover(-2 if fase == 0 and tomada else -1)
	elif evento.is_action_pressed("mover_abajo"):
		_mover(2 if fase == 0 and tomada else 1)
	elif evento.is_action_pressed("mover_izquierda"):
		if fase == 1:
			_cambiar(seleccion, -1)
		else:
			_mover(-1)
	elif evento.is_action_pressed("mover_derecha"):
		if fase == 1:
			_cambiar(seleccion, 1)
		else:
			_mover(1)
	else:
		return
	get_viewport().set_input_as_handled()


func _gui_input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or fase != 0:
		return
	if evento is InputEventMouseButton and evento.button_index == MOUSE_BUTTON_LEFT:
		_cursor = evento.position
		if evento.pressed:
			for i in 4:
				if _rect_pieza(i).has_point(_cursor):
					seleccion = i
					tomada = true
					_arrastrando = true
					grab_focus()
					break
			for i in 4:
				if tomada and _rect_hueco(i).has_point(_cursor):
					hueco = i
					_colocar()
		else:
			if _arrastrando:
				for i in 4:
					if _rect_hueco(i).has_point(_cursor):
						hueco = i
						_colocar()
						break
			_arrastrando = false
			# Fuera de un hueco la pieza queda tomada para colocar con clic o teclado.
	elif evento is InputEventMouseMotion:
		_cursor = evento.position
	_refrescar()


func _refrescar() -> void:
	if _cabecera == null:
		return
	_cabecera.text = "%s · Nivel %d · %.0f s disponibles" % ["1 / 2 · Montaje" if fase == 0 else "2 / 2 · Balance de energía", dificultad, maxf(0.0, LIMITE_S - tiempo)]
	for i in 5:
		_ajustes[i].visible = fase != 0
		_ajustes[i].disabled = fase >= 2
		_ajustes[i].add_theme_stylebox_override("normal", Estilo.caja(Estilo.CREMA if seleccion == i else Estilo.PAPEL, 8, 3 if seleccion == i else 1))
	_nota.visible = fase == 0
	if fase == 0:
		_nota.text = "KIT DEL CLUB\n\n4 subsistemas, 4 funciones.\n\nMontaje didáctico, no un plano real de Pegaso.\n\nE: tomar / colocar\nFlechas: elegir"
		_lectura.text = _mensaje
		_estado.text = "Maqueta didáctica · Sin escala\n\nComprueba el montaje para pasar al balance."
		_accion.text = "Comprobar · Espacio"
	else:
		var estados: Array[String] = ["Paneles: %s · %d u al sol" % [["plegados", "1 abierto", "2 abiertos"][paneles], _generado()], "Antena: %s · 0 u" % ("desplegada" if antena else "plegada"), "Computadora: %s · %d u / tramo" % ["sí" if computadora else "no", COSTE_PC if computadora else 0], "Radio al sol: %s · %d u" % ["sí" if radio_sol else "no", COSTE_RADIO if radio_sol else 0], "Radio en sombra: %s · %d u" % ["sí" if radio_sombra else "no", COSTE_RADIO if radio_sombra else 0]]
		for i in 5:
			_ajustes[i].text = ("› " if seleccion == i else "") + estados[i]
		var carga: float = clampf(float(_generado() - _consumo(false)), 0.0, CAPACIDAD)
		_lectura.text = "MODELO SIMPLIFICADO · u = energía de juego\nSol: %d u generadas − %d u de consumo\nBatería vacía → %.0f / 4 u; sombra pide %d u\nCiclo: 4 s de sol + 4 s de sombra. Sin escala real." % [_generado(), _consumo(false), carga, _consumo(true)]
		if fase == 1:
			_estado.text = "Objetivo: transmitir al sol y ordenar en sombra.\n\n↑ ↓: fila · ← → / E: cambiar una opción"
		else:
			_estado.text = "%s · %.1f / 4 s\nBatería: %.1f / 4 u\n%s" % ["AL SOL · cargando" if fase == 2 else "EN SOMBRA · gastando", transcurrido, maxf(0.0, bateria), "Generación en sombra: 0 u. La batería sostiene los equipos." if fase == 3 else "El sobrante carga hasta 4 u; el resto no se almacena."]
		_accion.text = "Probar ciclo · Espacio" if fase == 1 else "Ciclo en marcha…"
	_accion.disabled = fase >= 2
	queue_redraw()


func _letra(contenido: String, pos: Vector2, tam: int = 16, color: Color = Estilo.TINTA) -> void:
	draw_string(Estilo.fuente(600), pos, contenido, HORIZONTAL_ALIGNMENT_LEFT, -1, tam, color)


func _draw() -> void:
	draw_style_box(Estilo.caja(Estilo.PAPEL_SOMBRA, 12, 1), Rect2(16, 78, 594, 377))
	# Pinceladas discretas de la mesa, sin texturas ni recursos externos.
	for i in 12:
		draw_line(Vector2(30, 96 + i * 29), Vector2(595, 100 + i * 29), Color(Estilo.CREMA, 0.23), 3.0)
	if fase == 0:
		_cubo(Vector2(330, 170), Vector2(210, 160))
		for i in 4:
			var r: Rect2 = _rect_pieza(i)
			draw_style_box(Estilo.caja(Estilo.PAPEL, 7, 3 if seleccion == i else 1, Estilo.CIAN_MEDIO if seleccion == i else Estilo.TINTA_SUAVE, 0), r)
			_letra("%s %s" % ["✓" if piezas.has(i) else str(i + 1) + ".", PIEZAS[i]], r.position + Vector2(10, 31), 18)
			var h: Rect2 = _rect_hueco(i)
			draw_style_box(Estilo.caja(Estilo.CREMA if piezas[i] == i else Estilo.PAPEL, 4, 3 if tomada and hueco == i else 1, Estilo.CIAN_MEDIO if tomada and hueco == i else Estilo.TINTA_SUAVE, 0), h)
			_letra("%d %s" % [i + 1, "✓" if piezas[i] == i else "○"], h.position + Vector2(6, 20))
			var palabras: PackedStringArray = FUNCIONES[i].split(" ", true, 1)
			_letra(palabras[0], h.position + Vector2(6, 40))
			_letra(palabras[1], h.position + Vector2(6, 58))
		_letra("Cuerpo: 10 cm", Vector2(346, 120), 18)
		if tomada and _arrastrando:
			draw_style_box(Estilo.caja(Estilo.CIAN, 6, 2), Rect2(_cursor + Vector2(10, -40), Vector2(224, 42)))
			_letra(PIEZAS[seleccion], _cursor + Vector2(20, -13), 18)
	else:
		for i in 2:
			var abierto: bool = paneles > i
			var r: Rect2 = Rect2(54 if i == 0 else 424, 205, 168 if abierto else 18, 88)
			if not abierto and i == 0:
				r.position.x = 222
			draw_line(Vector2(210, 247), Vector2(445, 247), Estilo.TINTA, 8)
			_panel(r)
		_cubo(Vector2(240, 185), Vector2(150, 130))
		_letra("10 cm", Vector2(280, 341), 18)
		_letra("2 paneles de 27 cm", Vector2(40, 170), 18)
		_letra("Sin escala", Vector2(464, 170))
		draw_line(Vector2(316, 160), Vector2(350, 103) if antena else Vector2(347, 161), Estilo.TINTA, 4, true)
		if antena:
			draw_arc(Vector2(350, 103), 14, -1.4, 0.3, 12, Estilo.CIAN_MEDIO, 2, true)
		_letra("PC: %s" % ("sí" if computadora else "no"), Vector2(251, 229))
		_letra("Radio: %s" % ("sí" if (radio_sombra if fase == 3 else radio_sol) else "no"), Vector2(251, 258))
		if fase >= 2:
			draw_rect(Rect2(70, 94, 480 * transcurrido / TRAMO_S, 6), Estilo.DORADO if fase == 2 else Estilo.PETROLEO)


func _cubo(pos: Vector2, medida: Vector2) -> void:
	var sesgo: Vector2 = Vector2(34, -32)
	draw_colored_polygon(PackedVector2Array([pos, pos + sesgo, pos + Vector2(medida.x, 0) + sesgo, pos + Vector2(medida.x, 0)]), Estilo.CREMA)
	draw_colored_polygon(PackedVector2Array([pos + Vector2(medida.x, 0), pos + Vector2(medida.x, 0) + sesgo, pos + medida + sesgo, pos + medida]), Estilo.PETROLEO)
	draw_rect(Rect2(pos, medida), Estilo.PAPEL)
	draw_rect(Rect2(pos, medida), Estilo.TINTA, false, 3)
	draw_line(pos + sesgo, pos + Vector2(medida.x, 0) + sesgo, Estilo.TINTA, 2, true)
	draw_line(pos, pos + sesgo, Estilo.TINTA, 2, true)
	draw_line(pos + Vector2(medida.x, 0) + sesgo, pos + medida + sesgo, Estilo.TINTA, 2, true)
	draw_line(pos + medida, pos + medida + sesgo, Estilo.TINTA, 2, true)


func _panel(r: Rect2) -> void:
	draw_rect(r, Estilo.PETROLEO)
	draw_colored_polygon(PackedVector2Array([r.position, r.position + Vector2(r.size.x, 0), r.end]), Estilo.TINTA_SUAVE)
	for i in range(1, 6):
		var x: float = r.position.x + r.size.x * float(i) / 6.0
		draw_line(Vector2(x, r.position.y), Vector2(x, r.end.y), Estilo.CREMA, 1)
	draw_line(Vector2(r.position.x, r.get_center().y), Vector2(r.end.x, r.get_center().y), Estilo.CREMA, 1)
	draw_rect(r, Estilo.TINTA, false, 2)
