extends "res://nucleo/minijuego.gd"

# Las fichas son la fuente de los datos; el control es una regla del suenio.
# Grados, calor relativo (no Celsius) y segundos de juego; no simula una capsula real.
const PASOS: Array[String] = [
	"Despegue de la etapa de ascenso",
	"Encuentro en órbita lunar",
	"Separación del módulo de servicio",
	"Reentrada: escudo térmico por delante",
	"Paracaídas",
	"Amerizaje"
]
const CAUSAS: Array[String] = [
	"Primero despega la etapa de ascenso: desde la superficie no puede encontrarse con la nave en órbita.",
	"Sin el encuentro en órbita lunar no hay nave para volver a la Tierra.",
	"El módulo de servicio se separa antes de reentrar: vuelve el módulo de mando con su escudo por delante.",
	"El escudo va antes que los paracaídas: protege durante la reentrada; los paracaídas frenan después.",
	"Los paracaídas van antes del amerizaje: frenan la caída antes de llegar al agua."
]
const DURACION: float = 20.0
const MINIMO_DENTRO: float = 16.0
const LIMITE_ORDEN: float = 150.0
const DT: float = 1.0 / 120.0
const ACELERACION: float = 65.0
const ROZAMIENTO: float = 0.65

var orden: Array[int] = [1, 0, 2, 4, 3, 5]
var seleccion: int = 0
var tomada: bool = false
var fase: int = 0 # 0 tarjetas, 1 reentrada, 2 paracaidas y agua
var angulo: float = 6.0
var giro: float = 0.0
var calor: float = 12.0
var margen: float = 18.0
var rafaga: float = 9.0
var vuelo: float = 0.0
var dentro: float = 0.0
var aire: float = 0.0
var max_desvio: float = 0.0
var comprobaciones: int = 0
var _acumulado: float = 0.0
var _final: float = 0.0
var _pulso: float = 0.0
var _auto: int = 0
var _raton: float = 0.0
var _arrastre: bool = false
var _trazo: PackedVector2Array = PackedVector2Array()
var _anterior: PackedVector2Array = PackedVector2Array()
var _dato_anterior: String = "Anterior: aún no hay reentrada."
var _paneles: Array[Panel] = []
var _tarjetas: Array[Label] = []
var _orden_nodos: Array[Control] = []
var _vuelo_nodos: Array[Control] = []
var _estado: Label
var _mensaje: Label
var _lectura: Label
var _termometro: ProgressBar
var _boton: Button


func _preparar() -> void:
	margen = [18.0, 14.0, 10.0][dificultad - 1]
	rafaga = [9.0, 14.0, 20.0][dificultad - 1]
	if dificultad == 2:
		orden.assign([2, 0, 1, 4, 3, 5])
	elif dificultad == 3:
		orden.assign([3, 1, 0, 5, 4, 2])
	var clave: String = "regreso_anterior_%d" % dificultad
	if get_parent().has_meta(clave):
		var registro: Dictionary = get_parent().get_meta(clave)
		_anterior = registro["trazo"]
		_dato_anterior = registro["dato"]
	_estado = _etiqueta("", Vector2(24, 14), 1072, 22)
	_orden_nodos.append(_etiqueta("SUEÑO · Secuencia didáctica simplificada · 6 pasos", Vector2(24, 52), 670, 18))
	for i in 6:
		var rect: Rect2 = _rect_tarjeta(i)
		var panel: Panel = Panel.new()
		panel.position = rect.position
		panel.size = rect.size
		panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(panel)
		_paneles.append(panel)
		_orden_nodos.append(panel)
		var l: Label = _etiqueta("", rect.position + Vector2(14, 10), rect.size.x - 28, 18)
		_tarjetas.append(l)
		_orden_nodos.append(l)
	_boton = Estilo.boton("Comprobar · Espacio", 18, true)
	_boton.position = Vector2(24, 438)
	_boton.size = Vector2(670, 48)
	_boton.focus_mode = Control.FOCUS_NONE
	_boton.pressed.connect(_comprobar)
	add_child(_boton)
	_orden_nodos.append(_boton)
	_orden_nodos.append(_etiqueta("DATOS DEL CUADERNO", Vector2(736, 62), 352, 18, Estilo.PETROLEO))
	# Texto literal de la ficha, sin atribuir cifras del modelo a una mision.
	var ficha: Dictionary = Juego.ficha("modulo_mando")
	_orden_nodos.append(_etiqueta(String(ficha["texto"]), Vector2(736, 100), 352, 20))
	ficha = Juego.ficha("muestras_apolo11")
	_orden_nodos.append(_etiqueta(String(ficha["texto"]), Vector2(736, 262), 352, 18))
	_mensaje = _etiqueta("", Vector2(24, 490), 1072, 16)
	_lectura = _etiqueta("", Vector2(704, 60), 392, 20)
	_vuelo_nodos.append(_lectura)
	_termometro = ProgressBar.new()
	_termometro.position = Vector2(704, 162)
	_termometro.size = Vector2(392, 22)
	_termometro.max_value = 100.0
	_termometro.show_percentage = false
	_termometro.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_termometro.add_theme_stylebox_override("background", Estilo.caja(Estilo.PAPEL_SOMBRA, 4, 2, Estilo.TINTA, 0))
	_termometro.add_theme_stylebox_override("fill", Estilo.caja(Estilo.TERRACOTA, 4, 0, Estilo.TINTA, 0))
	add_child(_termometro)
	_vuelo_nodos.append(_termometro)
	_vuelo_nodos.append(_etiqueta("Calor del sueño · límite 100 · sin °C\n20 s de vuelo · al menos 16 s en el margen", Vector2(704, 192), 392, 16))
	for lado in [-1, 1]:
		var b: Button = Estilo.boton("← Girar" if lado < 0 else "Girar →", 18, true)
		b.position = Vector2(704 if lado < 0 else 908, 250)
		b.size = Vector2(188, 48)
		b.focus_mode = Control.FOCUS_NONE
		b.button_down.connect(_pulsar_giro.bind(float(lado)))
		b.button_up.connect(_soltar_giro)
		add_child(b)
		_vuelo_nodos.append(b)
	_vuelo_nodos.append(_etiqueta("ÁNGULO · actual — / anterior · · ·", Vector2(704, 310), 392, 16))
	_vuelo_nodos.append(_etiqueta(_dato_anterior, Vector2(704, 444), 392, 16))
	_refrescar()


func _etiqueta(contenido: String, pos: Vector2, ancho: float, tam: int, color: Color = Estilo.TINTA) -> Label:
	var l: Label = texto(contenido, tam, color)
	l.position = pos
	l.custom_minimum_size = Vector2(ancho, 0)
	add_child(l)
	return l


func _rect_tarjeta(i: int) -> Rect2:
	return Rect2(24, 85 + i * 56, 670, 48)


func _empezar() -> void:
	_refrescar()


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or fase != 0:
		return
	if evento.is_action_pressed("interactuar"):
		tomada = not tomada
	elif evento.is_action_pressed("saltar"):
		_comprobar()
	elif evento.is_action_pressed("mover_arriba"):
		_desplazar(-1)
	elif evento.is_action_pressed("mover_abajo"):
		_desplazar(1)
	else:
		return
	_refrescar()
	get_viewport().set_input_as_handled()


func _desplazar(lado: int) -> void:
	if tomada:
		_mover(lado)
	else:
		seleccion = clampi(seleccion + lado, 0, 5)


func _mover(lado: int) -> void:
	var destino: int = seleccion + lado
	if destino < 0 or destino > 5:
		return
	var tarjeta: int = orden[seleccion]
	orden[seleccion] = orden[destino]
	orden[destino] = tarjeta
	seleccion = destino
	_refrescar()


func _gui_input(evento: InputEvent) -> void:
	if not activo or fase != 0 or _auto != 0:
		return
	if evento is InputEventMouseButton and evento.button_index == MOUSE_BUTTON_LEFT:
		if evento.pressed:
			for i in 6:
				if _rect_tarjeta(i).has_point(evento.position):
					seleccion = i
					tomada = true
					_arrastre = true
					grab_focus()
		else:
			tomada = false
			_arrastre = false
		_refrescar()
	elif evento is InputEventMouseMotion and _arrastre:
		if (evento.button_mask & MOUSE_BUTTON_MASK_LEFT) == 0:
			_arrastre = false
			tomada = false
		else:
			var destino: int = clampi(int((evento.position.y - 85.0) / 56.0), 0, 5)
			while seleccion != destino:
				_mover(1 if destino > seleccion else -1)
		_refrescar()


func _causa_orden() -> String:
	for paso in 5:
		if orden.find(paso) > orden.find(paso + 1):
			return CAUSAS[paso]
	return ""


func _comprobar() -> void:
	if not activo or fase != 0:
		return
	tomada = false
	_arrastre = false
	comprobaciones += 1
	var causa: String = _causa_orden()
	if causa != "":
		terminar(false, 0, causa)
		return
	fase = 1
	_trazo.append(Vector2(0, angulo))
	sonar("pagina")
	_refrescar()


func _pulsar_giro(lado: float) -> void:
	if activo and fase == 1:
		_raton = lado


func _soltar_giro() -> void:
	_raton = 0.0


func _paso(delta: float) -> void:
	if fase == 0:
		if _auto != 0:
			_pulso += delta
			while _pulso >= 0.22 and fase == 0:
				_pulso -= 0.22
				_paso_orden_auto()
		if fase == 0 and tiempo >= LIMITE_ORDEN:
			var causa: String = _causa_orden()
			terminar(false, 0, causa if causa != "" else "Los 6 pasos están ordenados, pero faltó comprobarlos para iniciar el regreso.")
	elif fase == 1:
		_acumulado += delta
		while _acumulado >= DT and activo and fase == 1:
			_acumulado -= DT
			var mando: float = eje_x() if _raton == 0.0 else _raton
			if _auto != 0:
				mando = _mando_auto()
			_integrar(DT, mando)
	elif fase == 2:
		_final += delta
		if _final >= 3.0:
			terminar(true, maxf(100.0 - calor * 0.3, 1.0), "Ordenaste los 6 pasos y mantuviste el escudo dentro del margen %.1f de 20 s. Los paracaídas frenaron antes del amerizaje." % dentro)
	_refrescar()


func _paso_orden_auto() -> void:
	# Intercambios adyacentes: las mismas operaciones que al tomar una tarjeta.
	for i in 5:
		if orden[i] > orden[i + 1]:
			seleccion = i + 1
			tomada = true
			_mover(-1)
			return
	_comprobar()


func _mando_auto() -> float:
	if _auto < 0:
		# Sostener derecha de forma continua deja el escudo de lado y calienta.
		return 1.0
	# Solo usa angulo y giro visibles. Pulsos digitales como las teclas de una persona.
	var error: float = -angulo * 4.0 - giro * 2.8
	return signf(error) if absf(error) > 3.0 else 0.0


func _integrar(dt: float, mando: float) -> void:
	vuelo += dt
	aire = rafaga * (sin(vuelo * 1.4) + 0.55 * sin(vuelo * 3.2 + 0.7))
	giro += (clampf(mando, -1.0, 1.0) * ACELERACION + aire - ROZAMIENTO * giro) * dt
	angulo += giro * dt
	if absf(angulo) > 85.0:
		angulo = clampf(angulo, -85.0, 85.0)
		giro = 0.0
	max_desvio = maxf(max_desvio, absf(angulo))
	if absf(angulo) <= margen:
		dentro += dt
		calor = maxf(calor - 6.0 * dt, 0.0)
	else:
		calor = minf(100.0, calor + minf(14.0 + (absf(angulo) - margen) * 1.1, 45.0) * dt)
	if _trazo.is_empty() or vuelo - _trazo[-1].x >= 0.1:
		_trazo.append(Vector2(vuelo, angulo))
	if calor >= 100.0:
		_guardar_intento()
		terminar(false, 0, "El escudo quedó de lado demasiado tiempo: el calor llegó a 100. Las correcciones tardías y grandes hacen oscilar; usa pulsos cortos y frena antes del centro.")
	elif vuelo >= DURACION:
		_guardar_intento()
		if dentro + 0.001 < MINIMO_DENTRO:
			terminar(false, 0, "El escudo estuvo dentro del margen %.1f s; hacían falta 16 de 20 s. Las correcciones tardías y grandes hacen oscilar: frena el giro antes del centro." % dentro)
		else:
			fase = 2
			_raton = 0.0
			sonar("ok")


func _guardar_intento() -> void:
	var dato: String = "Anterior: %.1f s en margen · calor %.0f\nDesvío máximo: %.1f°" % [dentro, calor, max_desvio]
	get_parent().set_meta("regreso_anterior_%d" % dificultad, {"trazo": _trazo.duplicate(), "dato": dato})
	print("REGRESO d%d vuelo=%.3f dentro=%.3f calor=%.2f desvio=%.2f juego=%.3f" % [dificultad, vuelo, dentro, calor, max_desvio, tiempo])


func _refrescar() -> void:
	for nodo in _orden_nodos:
		nodo.visible = fase == 0
	for nodo in _vuelo_nodos:
		nodo.visible = fase != 0
	if fase == 0:
		_estado.text = "1 / 2 · Prepara el regreso · De arriba abajo"
		for i in 6:
			_paneles[i].add_theme_stylebox_override("panel", Estilo.caja(Estilo.CREMA if i == seleccion and tomada else Estilo.PAPEL, 6, 3 if i == seleccion else 1, Estilo.CIAN_MEDIO if i == seleccion else Estilo.TINTA_SUAVE, 0))
			_tarjetas[i].text = "%d   %s%s" % [i + 1, "↕  " if i == seleccion and tomada else "", PASOS[orden[i]]]
		_mensaje.text = "Tarjeta %d %s · E: tomar / soltar · ↑ ↓: elegir / mover · Espacio: comprobar" % [seleccion + 1, "tomada" if tomada else "seleccionada"]
	else:
		_estado.text = "2 / 2 · Escudo por delante · %.1f / 20 s" % minf(vuelo, DURACION) if fase == 1 else "Paracaídas → amerizaje · La caja vuelve del sueño"
		_lectura.text = "Ángulo: %+.1f° · margen ±%.0f°\nGiro: %+.1f°/s · calor: %.0f / 100\nEn margen: %.1f / 16 s · %s" % [angulo, margen, giro, calor, minf(dentro, DURACION), "DENTRO" if absf(angulo) <= margen else "FUERA"]
		_termometro.value = calor
		_mensaje.text = "← →: pulsos cortos · Suelta y frena al lado opuesto antes del centro · Ángulos y calor: reglas del sueño"
	queue_redraw()


func _draw() -> void:
	if fase == 0:
		draw_style_box(Estilo.caja(Estilo.PAPEL_SOMBRA, 10, 1, Estilo.TINTA_SUAVE), Rect2(718, 48, 386, 428))
		return
	draw_style_box(Estilo.caja(Estilo.PETROLEO, 12, 2), Rect2(24, 52, 650, 432))
	# El suelo sube y las vetas del aire pasan: descenso sin recursos externos.
	for i in 11:
		var x: float = 60.0 + float(i) * 53.0
		var y: float = 90.0 + fposmod(float(i) * 47.0 - vuelo * 90.0, 300.0)
		draw_line(Vector2(x, y), Vector2(x - aire * 0.8, y - 25), Color(Estilo.PAPEL, 0.24), 2, true)
	var suelo: float = 510.0 - minf(vuelo / DURACION, 1.0) * 40.0
	draw_rect(Rect2(26, suelo, 646, 40), Estilo.PAPEL_SOMBRA)
	var centro: Vector2 = Vector2(345, 218 + minf(vuelo / DURACION, 1.0) * 55.0)
	if fase == 2:
		centro.y += minf(_final / 2.4, 1.0) * 115.0
	else:
		# Margen referido a la direccion de caida (hacia abajo), nunca a la horizontal.
		var cuña: PackedVector2Array = PackedVector2Array([centro, centro + Vector2.DOWN.rotated(deg_to_rad(-margen)) * 154.0, centro + Vector2.DOWN.rotated(deg_to_rad(margen)) * 154.0])
		draw_colored_polygon(cuña, Color(Estilo.CREMA, 0.24))
		draw_line(centro, centro + Vector2(0, 162), Estilo.PAPEL, 2, true)
		draw_line(centro + Vector2(0, 162), centro + Vector2(-8, 149), Estilo.PAPEL, 2, true)
		draw_line(centro + Vector2(0, 162), centro + Vector2(8, 149), Estilo.PAPEL, 2, true)
	_dibujar_caja(centro, deg_to_rad(angulo) if fase == 1 else 0.0)
	if fase == 2:
		var copa: Vector2 = centro + Vector2(0, -145)
		draw_colored_polygon(PackedVector2Array([copa + Vector2(-105, 25), copa + Vector2(-70, -24), copa + Vector2(0, -47), copa + Vector2(70, -24), copa + Vector2(105, 25)]), Estilo.CREMA)
		for x in [-105, -35, 35, 105]:
			draw_line(copa + Vector2(x, 25), centro + Vector2(x * 0.4, -40), Estilo.PAPEL, 2, true)
		for i in 4:
			draw_arc(Vector2(345, 473), 35 + i * 20, PI, TAU, 24, Color(Estilo.PAPEL, minf(_final / 3.0, 0.8)), 2, true)
	_dibujar_grafica()


func _dibujar_caja(centro: Vector2, rotacion: float) -> void:
	draw_set_transform(centro, rotacion)
	draw_colored_polygon(PackedVector2Array([Vector2(-64, -48), Vector2(44, -48), Vector2(64, -30), Vector2(64, 47), Vector2(-64, 47)]), Estilo.CREMA)
	draw_colored_polygon(PackedVector2Array([Vector2(44, -48), Vector2(64, -30), Vector2(64, 47), Vector2(44, 30)]), Estilo.TERRACOTA)
	draw_rect(Rect2(-11, -48, 22, 92), Estilo.PAPEL_SOMBRA)
	draw_line(Vector2(-64, -48), Vector2(44, -48), Estilo.TINTA_SUAVE, 3, true)
	draw_line(Vector2(-64, -48), Vector2(-64, 47), Estilo.TINTA_SUAVE, 3, true)
	draw_line(Vector2(-48, -18), Vector2(-31, 4), Estilo.TINTA_SUAVE, 1, true)
	draw_line(Vector2(16, 13), Vector2(31, 20), Estilo.TINTA_SUAVE, 1, true)
	# Escudo propio, ancho y plano bajo la caja: ninguna capsula ni insignia real.
	draw_colored_polygon(PackedVector2Array([Vector2(-79, 39), Vector2(79, 39), Vector2(66, 62), Vector2(-66, 62)]), Estilo.TINTA)
	draw_line(Vector2(-66, 61), Vector2(66, 61), Estilo.NARANJA if calor > 50.0 else Estilo.PAPEL_SOMBRA, 5, true)
	draw_set_transform(Vector2.ZERO)


func _dibujar_grafica() -> void:
	var rect: Rect2 = Rect2(704, 342, 392, 92)
	draw_rect(rect, Estilo.PAPEL_SOMBRA)
	var centro_y: float = rect.get_center().y
	var escala: float = 0.5
	draw_rect(Rect2(rect.position.x, centro_y - margen * escala, rect.size.x, margen * escala * 2.0), Color(Estilo.CREMA, 0.8))
	draw_line(Vector2(rect.position.x, centro_y), Vector2(rect.end.x, centro_y), Estilo.TINTA_SUAVE, 1)
	for linea in [_anterior, _trazo]:
		var puntos: PackedVector2Array = PackedVector2Array()
		for p in linea:
			puntos.append(Vector2(rect.position.x + p.x / DURACION * rect.size.x, centro_y - p.y * escala))
		if puntos.size() > 1:
			if linea == _anterior:
				for i in range(1, puntos.size()):
					if i % 4 < 2:
						draw_line(puntos[i - 1], puntos[i], Estilo.TINTA_SUAVE, 2, true)
			else:
				draw_polyline(puntos, Estilo.CIAN_MEDIO, 3, true)


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1
