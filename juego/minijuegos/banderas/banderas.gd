extends "res://nucleo/minijuego.gd"

# Cifras historicas: solo las cuatro fichas locales indicadas en el encargo.
# Ritmo, pixeles, tolerancias y tiempos son reglas didacticas, no medidas lunares.
const NOMBRES: Array[String] = ["Estados Unidos", "Ecuador"]
const PASOS: Array[String] = ["1 / 5 · ELEGIR EL SITIO", "2 / 5 · ARMAR", "3 / 5 · HINCAR CON RITMO", "4 / 5 · EXTENDER", "5 / 5 · IGUALAR ALTURAS", "UN CIELO COMPARTIDO"]
const SITIOS: Array[Vector2] = [Vector2(270, 240), Vector2(420, 330), Vector2(555, 225)]
const PIEZAS: Array[String] = ["Mástil", "Barra horizontal", "Tela"]
const CICLO: float = 1.5
const LIMITE: float = 180.0
const CONFIRMAR: Rect2 = Rect2(740, 443, 356, 51)
const ANTERIOR: Rect2 = Rect2(740, 246, 170, 48)
const SIGUIENTE: Rect2 = Rect2(926, 246, 170, 48)
const MENOS: Rect2 = Rect2(740, 309, 170, 48)
const MAS: Rect2 = Rect2(926, 309, 170, 48)

var paso: int = 0
var seleccion: int = 0
var conjunto: int = 0
var armado: Array[int] = [0, 0]
var golpes: Array[int] = [0, 0]
var extension: Array[float] = [0.55, 0.55]
var alturas: Array[float] = [204.0, 160.0]
var separacion: float = 140.0
var fase: float = 0.0
var ventana: float = 0.16
var necesarios: int = 3
var fallos_ritmo: int = 0
var revisiones: int = 0
var ultimo_ciclo: int = -1
var reloj_ritmo: float = 0.0
var ceremonia: float = 0.0
var mensaje: String = "Elige A, B o C. Mira el anillo y las huellas."
var _auto: int = 0
var _pulso: float = 0.0


func _preparar() -> void:
	ventana = [0.18, 0.14, 0.11][dificultad - 1]
	necesarios = 4 if dificultad == 3 else 3
	queue_redraw()


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


func _paso(delta: float) -> void:
	if paso == 5:
		ceremonia += delta
		if ceremonia >= 4.5:
			terminar(true, 100.0, "Una bandera no da territorio: artículo II del Tratado del Espacio. Ecuador firmó los Acuerdos Artemisa el 21-06-2023, como país n.º 26. Es cooperación.")
		queue_redraw()
		return
	if paso == 2:
		reloj_ritmo += delta
		fase = fmod(reloj_ritmo, CICLO) / CICLO
	if _auto != 0:
		_piloto(delta)
	else:
		_ajustar(eje_x(), delta)
	if tiempo >= LIMITE:
		terminar(false, 0.0, _causa_tiempo())
	queue_redraw()


func _causa_tiempo() -> String:
	match paso:
		0: return "Falta elegir un sitio libre de huellas y fuera del anillo recomendado de 75 m."
		1: return "Faltan piezas de soporte: cada tela necesita mástil y barra horizontal."
		2: return "Faltan pulsos centrados en el compás para asentar ambos mástiles; más fuerza no sustituye el ritmo."
		3: return "La barra quedó corta: sin viento, la tela necesita todo el soporte horizontal."
	return "Las alturas o la separación aún difieren: ajusta para que las 2 telas se vean completas."


func _cambiar(direccion: int) -> void:
	if paso == 0 or paso == 1 or paso == 4:
		seleccion = posmod(seleccion + direccion, 3)
	elif paso == 3:
		seleccion = posmod(seleccion + direccion, 2)
	queue_redraw()


func _ajustar(direccion: float, delta: float) -> void:
	if paso == 3:
		extension[seleccion] = clampf(extension[seleccion] + direccion * delta * 0.5, 0.4, 1.0)
		if extension[seleccion] >= 0.999:
			extension[seleccion] = 1.0
	elif paso == 4:
		if seleccion < 2:
			alturas[seleccion] = clampf(alturas[seleccion] + direccion * delta * 45.0, 130.0, 240.0)
		else:
			separacion = clampf(separacion + direccion * delta * 60.0, 120.0, 300.0)
	queue_redraw()


func _accion() -> void:
	if not activo or paso == 5:
		return
	match paso:
		0:
			if seleccion == 0:
				mensaje = "75 m: recomendación técnica para robots visitantes; no es una ley. Busquemos fuera del anillo."
			elif seleccion == 1:
				mensaje = "Aquí hay huellas históricas. Elige suelo libre para conservarlas."
			else:
				paso = 1
				seleccion = 0
				mensaje = "Sitio libre. Cada conjunto: mástil → barra → tela."
		1:
			if seleccion == armado[conjunto]:
				armado[conjunto] += 1
				if armado[conjunto] == 3:
					conjunto += 1
					seleccion = 0
					if conjunto == 2:
						paso = 2
						conjunto = 0
						mensaje = "Pulsa al centro del compás. Ritmo, sin medir fuerza."
			else:
				mensaje = "Primero el mástil sostiene la barra; después se fija la tela."
		2:
			var ciclo_actual: int = int(reloj_ritmo / CICLO)
			if ultimo_ciclo == ciclo_actual:
				mensaje = "Espera el siguiente compás: 1 pulso por recorrido."
				return
			ultimo_ciclo = ciclo_actual
			if absf(fase - 0.5) <= ventana:
				golpes[conjunto] += 1
				mensaje = "Pulso centrado. El soporte se asienta sin forzar."
				if golpes[conjunto] >= necesarios:
					conjunto += 1
					if conjunto == 2:
						paso = 3
						seleccion = 0
						mensaje = "Sin viento, la barra sostiene la tela. Extiende las 2 al 100 %."
			else:
				fallos_ritmo += 1
				mensaje = "El pulso llegó fuera del centro. Espera la franja marcada."
				if fallos_ritmo >= 5:
					terminar(false, 0.0, "5 pulsos fuera del compás: los soportes aún no están asentados. Pulsa al centro; no hace falta más fuerza.")
		3:
			if extension[0] >= 0.999 and extension[1] >= 0.999:
				paso = 4
				seleccion = 1
				mensaje = "Iguala las alturas y deja un hueco entre las telas."
			else:
				revisiones += 1
				mensaje = "La tela queda ondulada: falta barra y no hay viento que la sostenga."
				if revisiones >= 3:
					terminar(false, 0.0, "Tras 3 comprobaciones, queda una barra corta. La tela se ve ondulada porque no hay viento que la sostenga; extiende ambas al 100 %.")
		4:
			if absf(alturas[0] - alturas[1]) <= 2.0 and separacion >= 190.0 and separacion <= 250.0:
				paso = 5
				ceremonia = 0.0
				mensaje = ""
			else:
				mensaje = "Ajusta: alturas iguales, sin solapamiento y con un hueco pequeño."
	queue_redraw()


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or paso == 5:
		return
	if evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar"):
		_accion()
	elif evento.is_action_pressed("mover_arriba"):
		_cambiar(-1)
	elif evento.is_action_pressed("mover_abajo"):
		_cambiar(1)
	elif paso <= 1 and evento.is_action_pressed("mover_izquierda"):
		_cambiar(-1)
	elif paso <= 1 and evento.is_action_pressed("mover_derecha"):
		_cambiar(1)
	else:
		return
	get_viewport().set_input_as_handled()


func _gui_input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or paso == 5:
		return
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		var p: Vector2 = evento.position
		if CONFIRMAR.has_point(p):
			_accion()
		elif ANTERIOR.has_point(p):
			_cambiar(-1)
		elif SIGUIENTE.has_point(p):
			_cambiar(1)
		elif MENOS.has_point(p):
			_ajustar(-1.0, 0.2)
		elif MAS.has_point(p):
			_ajustar(1.0, 0.2)
		elif paso == 0:
			for i in 3:
				if p.distance_to(SITIOS[i]) <= 35.0:
					seleccion = i
					_accion()
		queue_redraw()


func _piloto(delta: float) -> void:
	_pulso += delta
	if paso == 2:
		if absf(fase - 0.5) < ventana * 0.65:
			_accion()
		return
	if paso == 3 and _auto > 0:
		_ajustar(1.0, delta)
		if extension[seleccion] >= 0.999:
			if seleccion == 0:
				_cambiar(1)
			else:
				_accion()
		return
	if paso == 4:
		if absf(alturas[1] - alturas[0]) > 1.0:
			seleccion = 1
			_ajustar(signf(alturas[0] - alturas[1]), minf(delta, absf(alturas[0] - alturas[1]) / 45.0))
		elif separacion < 210.0:
			seleccion = 2
			_ajustar(1.0, delta)
		else:
			_accion()
		return
	if _pulso < 0.35:
		return
	_pulso = 0.0
	if paso == 0:
		if seleccion < 2:
			_cambiar(1)
		else:
			_accion()
	elif paso == 1:
		if seleccion != armado[conjunto]:
			_cambiar(1)
		else:
			_accion()
	elif paso == 3:
		# El camino de fallo comprueba de verdad dos barras aun cortas.
		_accion()


func _letra(s: String, p: Vector2, tam: int = 18, color: Color = Estilo.PAPEL) -> void:
	draw_string(Estilo.fuente(600), p, s, HORIZONTAL_ALIGNMENT_LEFT, -1, tam, color)


func _boton(r: Rect2, s: String) -> void:
	draw_style_box(Estilo.caja(Estilo.PAPEL, 7, 2, Estilo.CIAN_MEDIO, 0), r)
	_letra(s, r.position + Vector2(14, 31), 18, Estilo.TINTA)


func _draw() -> void:
	var luz: float = clampf(ceremonia / 1.5, 0.0, 1.0)
	draw_rect(Rect2(0, 0, 1120, 520), Estilo.PETROLEO.lerp(Estilo.TERRACOTA, luz))
	draw_colored_polygon(PackedVector2Array([Vector2(0, 350), Vector2(130, 322), Vector2(285, 360), Vector2(480, 316), Vector2(720, 350), Vector2(720, 520), Vector2(0, 520)]), Estilo.TINTA_SUAVE.lerp(Estilo.CREMA, luz))
	for i in 13:
		var p: Vector2 = Vector2(34 + i * 53, 405 + (i % 3) * 27)
		draw_colored_polygon(PackedVector2Array([p, p + Vector2(20, -8), p + Vector2(35, 4), p + Vector2(8, 8)]), Estilo.PETROLEO.lerp(Estilo.PAPEL_SOMBRA, luz))
	_letra(PASOS[paso], Vector2(24, 34), 24)
	_letra("SUEÑO · Instalación nueva", Vector2(24, 63), 16)
	if paso == 0:
		_mapa()
	else:
		for i in 2:
			_bandera(i, 140.0 + float(i) * separacion, 390.0, alturas[i])
			_letra(NOMBRES[i], Vector2(128 + float(i) * separacion, 423), 18, Estilo.TINTA if luz > 0.7 else Estilo.PAPEL)
		if paso == 1:
			_letra("Soportes de montaje · las telas siguen sujetas", Vector2(24, 470), 18)
	if paso == 5:
		_letra("Amanecer del sueño", Vector2(745, 158), 24)
		_letra("2 banderas · 1 cielo", Vector2(745, 200), 22)
		_letra("Cooperar y conservar", Vector2(745, 242), 20)
		return
	draw_rect(Rect2(720, 0, 400, 520), Estilo.PAPEL)
	_panel()


func _mapa() -> void:
	draw_rect(Rect2(30, 95, 660, 310), Estilo.TINTA_SUAVE)
	draw_circle(Vector2(230, 220), 112.5, Estilo.PETROLEO)
	draw_arc(Vector2(230, 220), 112.5, 0, TAU, 64, Estilo.PAPEL, 2, true)
	draw_rect(Rect2(213, 203, 34, 34), Estilo.CREMA)
	_letra("Etapa de descenso", Vector2(60, 127), 18)
	_letra("75 m", Vector2(100, 300), 20)
	for j in 9:
		var p: Vector2 = Vector2(348 + j * 10, 270 + j * 7)
		draw_line(p, p + Vector2(6, 7), Estilo.PAPEL, 4)
	_letra("Huellas", Vector2(440, 365), 18)
	for i in 3:
		draw_circle(SITIOS[i], 26, Estilo.PAPEL)
		if seleccion == i:
			draw_arc(SITIOS[i], 31, 0, TAU, 32, Estilo.CIAN, 4, true)
		_letra(["A", "B", "C"][i], SITIOS[i] + Vector2(-7, 7), 22, Estilo.TINTA)
	_letra("Mapa esquemático · 75 m desde la etapa", Vector2(30, 445), 18)
	_letra("Conservar las huellas es parte de la exploración.", Vector2(30, 477), 18)


func _panel() -> void:
	var lineas: Array[String] = []
	match paso:
		0:
			lineas = ["Sitio " + ["A · dentro del anillo", "B · sobre huellas", "C · suelo libre"][seleccion], "75 m: recomendación técnica", "para robots visitantes.", "No es un requisito legal."]
		1:
			lineas = [NOMBRES[conjunto], "Piezas fijadas: %d / 3" % armado[conjunto], "Elegida: " + PIEZAS[seleccion], "Mástil → barra → tela"]
		2:
			lineas = [NOMBRES[conjunto], "Pulsos: %d / %d" % [golpes[conjunto], necesarios], "Fuera de compás: %d / 5" % fallos_ritmo, "Pulsa en la franja central."]
		3:
			lineas = [NOMBRES[seleccion], "Barra: %d %% / 100 %%" % roundi(extension[seleccion] * 100), "Comprobaciones: %d / 3" % revisiones, "La ondulación no es viento."]
		4:
			lineas = [["Altura · Estados Unidos", "Altura · Ecuador", "Separación"][seleccion], "Alturas: %d / %d" % [roundi(alturas[0]), roundi(alturas[1])], "Hueco: %d" % roundi(separacion - 180), "Escala de ajuste del juego"]
	for i in lineas.size():
		_letra(lineas[i], Vector2(740, 52 + i * 30), 19, Estilo.TINTA)
	if paso == 2:
		draw_rect(Rect2(740, 176, 356, 30), Estilo.TINTA_SUAVE)
		draw_rect(Rect2(740 + (0.5 - ventana) * 356, 176, ventana * 712, 30), Estilo.CIAN_MEDIO)
		draw_line(Vector2(740 + fase * 356, 170), Vector2(740 + fase * 356, 213), Estilo.TINTA, 4)
		_letra("CENTRO", Vector2(881, 233), 16, Estilo.TINTA)
	else:
		_boton(ANTERIOR, "↑ Anterior")
		_boton(SIGUIENTE, "↓ Siguiente")
	if paso == 3 or paso == 4:
		_boton(MENOS, "− Reducir")
		_boton(MAS, "+ Aumentar")
	# Mensaje envuelto con la fuente del proyecto, sin nodos ni recortes.
	var palabras: PackedStringArray = mensaje.split(" ")
	var linea: String = ""
	var y: float = 380.0 if paso >= 3 else 319.0
	for palabra in palabras:
		if Estilo.fuente(600).get_string_size(linea + palabra, HORIZONTAL_ALIGNMENT_LEFT, -1, 16).x > 350:
			_letra(linea, Vector2(740, y), 16, Estilo.TINTA)
			y += 20
			linea = ""
		linea += palabra + " "
	_letra(linea, Vector2(740, y), 16, Estilo.TINTA)
	_boton(CONFIRMAR, "Pulsar compás · E / Espacio" if paso == 2 else "Confirmar · E / Espacio")


func _bandera(i: int, x: float, suelo: float, alto: float) -> void:
	var tope: Vector2 = Vector2(x, suelo - alto)
	var piezas: int = armado[i]
	if piezas == 0:
		return
	draw_line(Vector2(x, suelo), tope + Vector2(0, -8), Estilo.PAPEL_SOMBRA, 5)
	if piezas < 2:
		return
	var ancho: float = 180.0 * extension[i]
	draw_line(tope, tope + Vector2(ancho, 0), Estilo.PAPEL_SOMBRA, 5)
	if piezas < 3:
		return
	# Pliegues estaticos por soporte corto; nunca una animacion de viento o caida.
	for banda in (13 if i == 0 else 4):
		var total: int = 13 if i == 0 else 4
		var color: Color = (Estilo.CORAL if banda % 2 == 0 else Estilo.PAPEL) if i == 0 else ([Estilo.DORADO, Estilo.DORADO, Estilo.PETROLEO, Estilo.CORAL][banda] as Color)
		var puntos: PackedVector2Array = PackedVector2Array()
		for borde in 2:
			for j in 25:
				var t: float = float(j if borde == 0 else 24 - j) / 24.0
				var pliegue: float = sin(t * PI * 6) * (1.0 - extension[i]) * 12.0
				puntos.append(tope + Vector2(t * ancho, float(banda + borde) * 90.0 / total + pliegue))
		draw_colored_polygon(puntos, color)
	if i == 0:
		draw_rect(Rect2(tope, Vector2(ancho * 0.42, 90.0 * 7.0 / 13.0)), Estilo.PETROLEO)
		for fila in 9:
			for col in (6 if fila % 2 == 0 else 5):
				_estrella(tope + Vector2((float(col) + 0.65 + 0.5 * (fila % 2)) * ancho * 0.064, 3.5 + fila * 4.8), 1.8, Estilo.PAPEL)
	else:
		var centro: Vector2 = tope + Vector2(ancho * 0.5, 45)
		# Escudo simplificado: condor, ovalo, montana, rio y haces laterales.
		draw_colored_polygon(PackedVector2Array([centro + Vector2(-22, -17), centro + Vector2(-5, -19), centro + Vector2(0, -25), centro + Vector2(5, -19), centro + Vector2(22, -17), centro + Vector2(8, -13), centro + Vector2(0, -16), centro + Vector2(-8, -13)]), Estilo.TINTA)
		draw_line(centro + Vector2(-15, -6), centro + Vector2(-13, 19), Estilo.DORADO, 5)
		draw_line(centro + Vector2(15, -6), centro + Vector2(13, 19), Estilo.DORADO, 5)
		draw_set_transform(centro, 0, Vector2(0.72, 1))
		draw_circle(Vector2.ZERO, 17, Estilo.DORADO)
		draw_circle(Vector2.ZERO, 14, Estilo.PAPEL)
		draw_colored_polygon(PackedVector2Array([Vector2(-13, 4), Vector2(0, -8), Vector2(13, 4)]), Estilo.PETROLEO)
		draw_line(Vector2(-8, 7), Vector2(9, 10), Estilo.PETROLEO, 3)
		draw_set_transform(Vector2.ZERO)
	if extension[i] < 0.999:
		for j in 5:
			var xx: float = x + (j + 0.5) * ancho / 5.0
			draw_line(Vector2(xx, tope.y + 2), Vector2(xx, tope.y + 87), Color(Estilo.TINTA, 0.2), 3)


func _estrella(centro: Vector2, radio: float, color: Color) -> void:
	var puntos: PackedVector2Array = PackedVector2Array()
	for j in 10:
		var angulo: float = -PI / 2.0 + j * PI / 5.0
		puntos.append(centro + Vector2(cos(angulo), sin(angulo)) * radio * (1.0 if j % 2 == 0 else 0.4))
	draw_colored_polygon(puntos, color)
