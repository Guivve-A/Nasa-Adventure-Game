extends "res://nucleo/minijuego.gd"

# Fuentes: herramientas_apolo11, regolito, bolsas_numeradas, muestras_apolo11.
# Las cuatro muestras, etiquetas, golpes y tiempos son reglas del suenio.
# No representan un inventario historico ni una profundidad real de hincado.
const MUESTRAS: Array[Dictionary] = [
	{"nombre": "Suelo fino", "lugar": "A", "bolsa": 2, "herramienta": 0},
	{"nombre": "Fragmentos pequeños", "lugar": "B", "bolsa": 4, "herramienta": 0},
	{"nombre": "Roca suelta", "lugar": "C", "bolsa": 1, "herramienta": 1},
	{"nombre": "Columna con capas", "lugar": "D", "bolsa": 3, "herramienta": 2}
]
const GOLPES: int = 4
const PERIODO: float = 1.0
const LIMITE: float = 150.0
const EXTRAER: Rect2 = Rect2(800, 452, 294, 40)
const MARTILLO: Rect2 = Rect2(600, 452, 184, 40)
enum Fase {HERRAMIENTA, RECOGIDA, RITMO, BOLSA, MAPA, REGISTRADA, FALLO}

var fase: int = Fase.HERRAMIENTA
var muestra: int = 0
var seleccion: int = 0
var recogida: bool = false
var bolsa_guardada: int = 0
var registros: Array[Dictionary] = []
var golpes: int = 0
var desajustes: int = 0
var ritmo: float = 0.0
var ventana: float = 0.24
var _ultimo_pulso: int = -1
var _una: bool = false
var _auto: int = 0
var _pulso_auto: float = 0.0
var _transicion: float = 0.0
var _causa: String = ""
var _mensaje: String = ""
var _correcciones: int = 0
var _detalle: Label


func _preparar() -> void:
	var pedida: int = int(parametros.get("muestra", -1))
	_una = pedida >= 0 and pedida <= 3
	muestra = pedida if _una else 0
	ventana = [0.24, 0.17, 0.10][dificultad - 1]
	_detalle = texto("", 19, Estilo.TINTA, 600)
	_detalle.position = Vector2(24, 387)
	_detalle.custom_minimum_size = Vector2(1072, 0)
	_detalle.size = Vector2(1072, 58)
	add_child(_detalle)
	_nueva_muestra()


func _empezar() -> void:
	_actualizar()


func _nueva_muestra() -> void:
	fase = Fase.HERRAMIENTA
	seleccion = 0
	recogida = false
	bolsa_guardada = 0
	golpes = 0
	desajustes = 0
	ritmo = 0.0
	_ultimo_pulso = -1
	_mensaje = "Elige una herramienta para conservar lo que buscas."
	if dificultad == 1:
		_mensaje = ["El cucharón retiene el suelo fino.", "Usa el cucharón para recoger los fragmentos pequeños con el suelo.", "Las pinzas sujetan una roca suelta.", "El tubo conserva la columna de capas; se hinca con martillo."][muestra]
	elif dificultad == 2:
		_mensaje = "Piensa en la forma de la muestra: polvo, roca o capas."
	_actualizar()


func _paso(delta: float) -> void:
	# Pasos pequenos mantienen la misma ventana a ritmo de pruebas x8.
	var restante: float = delta
	while restante > 0.000001 and activo:
		var paso: float = minf(restante, 1.0 / 120.0)
		restante -= paso
		_avanzar(paso)
	if activo and tiempo >= (90.0 if _una else LIMITE):
		var causa: String = "Falta recoger la muestra con una herramienta que la conserve."
		if fase == Fase.BOLSA:
			causa = "La muestra está recogida, pero falta vincularla a su bolsa numerada."
		elif fase == Fase.MAPA:
			causa = "La bolsa está guardada, pero falta marcar su origen en el croquis."
		elif fase == Fase.RITMO:
			causa = "El tubo sigue en el suelo: faltó completar y extraer la columna."
		terminar(false, 0.0, "Se agotó la sesión. " + causa)
	_actualizar()


func _avanzar(delta: float) -> void:
	if fase in [Fase.RECOGIDA, Fase.REGISTRADA, Fase.FALLO]:
		_transicion -= delta
		if _transicion <= 0.0:
			if fase == Fase.FALLO:
				terminar(false, 0.0, _causa)
			elif fase == Fase.RECOGIDA:
				fase = Fase.BOLSA
				seleccion = 0
				_mensaje = "Muestra conservada. Lee su etiqueta y elige la bolsa numerada."
			else:
				if _una or muestra == 3:
					print("MUESTRAS registros=%s correcciones=%d tiempo=%.3f" % [str(registros), _correcciones, tiempo])
					terminar(true, 100.0, "Registraste %d muestra(s): herramienta, bolsa y lugar vinculados. Referencia histórica: 21,5 kg en 58 muestras." % registros.size())
				else:
					muestra += 1
					_nueva_muestra()
		return
	if fase == Fase.RITMO:
		ritmo += delta
		if _auto != 0 and ritmo >= float(golpes + 1) * PERIODO:
			_golpear()
		if _auto != 0 and golpes == GOLPES and ritmo >= 4.35:
			_activar()
		if fase == Fase.RITMO and ritmo >= 8.0:
			_extraer()
		return
	if _auto == 0:
		return
	_pulso_auto += delta
	if _pulso_auto < 0.32:
		return
	_pulso_auto = 0.0
	var objetivo: int = 0
	match fase:
		Fase.HERRAMIENTA:
			objetivo = int(MUESTRAS[muestra]["herramienta"])
			if _auto < 0:
				objetivo = 0 if objetivo == 2 else 1 if objetivo == 0 else 2
		Fase.BOLSA:
			objetivo = int(MUESTRAS[muestra]["bolsa"]) - 1
		Fase.MAPA:
			objetivo = muestra
	if seleccion != objetivo:
		_mover(1 if objetivo > seleccion else -1)
	else:
		_activar()


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or evento.is_echo():
		return
	if evento.is_action_pressed("mover_izquierda") or evento.is_action_pressed("mover_arriba"):
		_mover(-1)
	elif evento.is_action_pressed("mover_derecha") or evento.is_action_pressed("mover_abajo"):
		_mover(1)
	elif evento.is_action_pressed("saltar"):
		if fase == Fase.RITMO:
			_golpear()
		else:
			_activar()
	elif evento.is_action_pressed("interactuar"):
		_activar()
	else:
		return
	get_viewport().set_input_as_handled()
	_actualizar()


func _gui_input(evento: InputEvent) -> void:
	if not activo or _auto != 0:
		return
	if evento is InputEventMouseButton and evento.button_index == MOUSE_BUTTON_LEFT and evento.pressed:
		grab_focus()
		if EXTRAER.has_point(evento.position):
			_activar()
		elif fase == Fase.RITMO and MARTILLO.has_point(evento.position):
			_golpear()
		else:
			for i in _cantidad_opciones():
				if _rect_opcion(i).has_point(evento.position):
					seleccion = i
					_activar()
					break
		_actualizar()


func _cantidad_opciones() -> int:
	if fase == Fase.HERRAMIENTA:
		return 3
	if fase in [Fase.BOLSA, Fase.MAPA]:
		return 4
	return 0


func _mover(direccion: int) -> void:
	var cantidad: int = _cantidad_opciones()
	if cantidad > 0:
		seleccion = posmod(seleccion + direccion, cantidad)
		sonar("pulsar")


func _activar() -> void:
	if not activo:
		return
	var ficha: Dictionary = MUESTRAS[muestra]
	match fase:
		Fase.HERRAMIENTA:
			if seleccion != int(ficha["herramienta"]):
				var causa: String
				if muestra <= 1 and seleccion == 1:
					causa = "Las pinzas no retienen el polvo ni el suelo entre los fragmentos; el material se escapa. Usa el cucharón de caja."
				elif muestra <= 1:
					causa = "El tubo conserva una columna, pero aquí buscas suelo superficial y fragmentos pequeños juntos. Recógelos con el cucharón de caja."
				elif muestra == 3 and seleccion == 0:
					causa = "El cucharón revuelve las capas: ya no conserva su orden. Usa el tubo de núcleo de 2 cm con martillo."
				elif muestra == 3:
					causa = "Las pinzas no encierran una columna de suelo: se escapan los granos y las capas. Usa el tubo de núcleo de 2 cm con martillo."
				elif seleccion == 0:
					causa = "El cucharón recoge suelo junto a la roca; aquí necesitas sujetar solo la roca suelta. Usa las pinzas pequeñas."
				else:
					causa = "El tubo extrae una columna del suelo; no sujeta la roca suelta. Usa las pinzas pequeñas."
				_fallar(causa)
			elif seleccion == 2:
				fase = Fase.RITMO
				ritmo = 0.0
				_mensaje = "Da 4 golpes en el centro (Espacio) y luego extrae (E). No mantengas la tecla."
			else:
				_recoger()
		Fase.RITMO:
			_extraer()
		Fase.BOLSA:
			if seleccion + 1 != int(ficha["bolsa"]):
				_correcciones += 1
				_mensaje = "La bolsa %d no coincide con la etiqueta %d. La muestra se conserva: corrige el número para vincular su registro." % [seleccion + 1, int(ficha["bolsa"])]
				sonar("pagina")
			else:
				bolsa_guardada = seleccion + 1
				fase = Fase.MAPA
				seleccion = 0
				_mensaje = "Bolsa %d guardada. Marca el lugar %s: el número y el origen deben quedar unidos." % [bolsa_guardada, ficha["lugar"]]
		Fase.MAPA:
			if seleccion != muestra:
				_correcciones += 1
				_mensaje = "La muestra vino de %s. Marcar %s perdería su origen; conserva la bolsa %d y corrige el croquis." % [ficha["lugar"], MUESTRAS[seleccion]["lugar"], bolsa_guardada]
				sonar("pagina")
			else:
				registros.append({"muestra": muestra, "bolsa": bolsa_guardada, "lugar": ficha["lugar"], "herramienta": ficha["herramienta"]})
				fase = Fase.REGISTRADA
				_transicion = 1.6
				_mensaje = "Registro completo: %s → bolsa %d → lugar %s. La bolsa numerada conserva el vínculo con el registro." % [ficha["nombre"], bolsa_guardada, ficha["lugar"]]
				sonar("recoger")
	_actualizar()


func _recoger() -> void:
	recogida = true
	fase = Fase.RECOGIDA
	_transicion = 0.9
	_mensaje = "Muestra recogida. Ahora hay que conservar su número y su origen."
	sonar("recoger")


func _golpear() -> void:
	if not activo or fase != Fase.RITMO:
		return
	var pulso: int = int(roundf(ritmo / PERIODO))
	var distancia: float = absf(ritmo - float(pulso) * PERIODO)
	if pulso < 1 or pulso == _ultimo_pulso or distancia > ventana:
		desajustes += 1
		_mensaje = "El golpe cayó fuera del pulso; espera al centro. Desajustes: %d / 2." % desajustes
		if desajustes >= 2:
			_fallar("Dos golpes fuera del pulso rompieron el ritmo. Espera al centro de la barra antes de golpear.")
		return
	_ultimo_pulso = pulso
	golpes += 1
	sonar("tic")
	_mensaje = "Golpes: %d / 4. %s" % [golpes, "Ya puedes extraer con E." if golpes == 4 else "Espera al siguiente pulso."]
	if golpes == GOLPES + 1:
		_mensaje = "Sobra 1 golpe: había que extraer tras 4. Otro golpe romperá el ritmo."
	elif golpes >= GOLPES + 2:
		_fallar("Diste 6 golpes: 2 de más rompieron el ritmo. El modelo pide 4 y luego extraer; no es una cifra histórica.")
	_actualizar()


func _extraer() -> void:
	if golpes < GOLPES:
		_fallar("Con %d de 4 golpes el tubo quedó corto en el modelo: no recogió la columna completa. Completa los 4 pulsos antes de extraer." % golpes)
	elif golpes > GOLPES:
		_fallar("Sobra 1 golpe: se perdió la secuencia de 4 pulsos y extracción. Detente al llegar a 4; es una regla del sueño.")
	else:
		_recoger()


func _fallar(causa: String) -> void:
	_causa = causa
	_mensaje = causa
	fase = Fase.FALLO
	_transicion = 2.2
	sonar("error")
	_actualizar()


func _actualizar() -> void:
	_detalle.text = _mensaje
	queue_redraw()


func _rect_opcion(i: int) -> Rect2:
	if fase == Fase.HERRAMIENTA:
		return Rect2(610 + i * 164, 112, 156, 213)
	if fase == Fase.BOLSA:
		return Rect2(610 + i * 124, 122, 114, 196)
	return Rect2(644 + (i % 2) * 224, 136 + (i / 2) * 92, 192, 70)


func _letra(s: String, punto: Vector2, tam: int = 18, color: Color = Estilo.TINTA) -> void:
	draw_string(Estilo.fuente(600), punto, s, HORIZONTAL_ALIGNMENT_LEFT, -1, tam, color)


func _caja(rect: Rect2, elegido: bool = false, fondo: Color = Estilo.PAPEL) -> void:
	draw_style_box(Estilo.caja(fondo, 8, 3 if elegido else 2, Estilo.CIAN_MEDIO if elegido else Estilo.TINTA_SUAVE, 0), rect)


func _draw() -> void:
	var ficha: Dictionary = MUESTRAS[muestra]
	_letra("%s · %s" % [ficha["lugar"], ficha["nombre"]], Vector2(24, 30), 25)
	_letra("Registros: %d / %d   ·   Sesión: %d s" % [registros.size(), 1 if _una else 4, maxi(0, int((90.0 if _una else LIMITE) - tiempo))], Vector2(681, 30), 18)
	var paso: String = "1 · ELEGIR Y RECOGER" if fase in [Fase.HERRAMIENTA, Fase.RITMO, Fase.RECOGIDA, Fase.FALLO] else "2 · REGISTRAR: BOLSA + CROQUIS"
	_letra(paso, Vector2(24, 68), 18, Estilo.PETROLEO)
	_terreno()
	if fase == Fase.HERRAMIENTA:
		for i in 3:
			var rect: Rect2 = _rect_opcion(i)
			_caja(rect, seleccion == i)
			_herramienta(i, rect.position + Vector2(78, 72), 0.8)
			var titulos: Array[String] = ["Cucharón", "Pinzas", "Tubo de núcleo"]
			_letra(titulos[i], rect.position + Vector2(10, 146), 18)
			_letra(["de caja", "pequeñas", "2 cm + martillo"][i], rect.position + Vector2(10, 174), 16)
		_letra("¿Qué conserva esta muestra?", Vector2(610, 92), 19)
	elif fase == Fase.BOLSA:
		_letra("Etiqueta: bolsa %d · lugar %s" % [int(ficha["bolsa"]), ficha["lugar"]], Vector2(610, 92), 21)
		for i in 4:
			var rect: Rect2 = _rect_opcion(i)
			_caja(rect, seleccion == i)
			_bolsa(rect.position + Vector2(57, 77), i + 1)
			_letra("Bolsa %d" % (i + 1), rect.position + Vector2(17, 171), 18)
	elif fase in [Fase.MAPA, Fase.REGISTRADA]:
		_letra("CROQUIS DEL SUEÑO · sin escala", Vector2(610, 92), 19)
		_caja(Rect2(610, 108, 484, 223), false, Estilo.PAPEL_SOMBRA)
		draw_line(Vector2(638, 270), Vector2(1045, 143), Estilo.TINTA_SUAVE, 2)
		for i in 4:
			var rect: Rect2 = _rect_opcion(i)
			_caja(rect, seleccion == i and fase == Fase.MAPA)
			_letra("%s · %s" % [MUESTRAS[i]["lugar"], ["suelo fino", "fragmentos", "roca", "columna"][i]], rect.position + Vector2(12, 29), 18)
			for registro in registros:
				if int(registro["muestra"]) == i:
					_letra("✓ Bolsa %d" % int(registro["bolsa"]), rect.position + Vector2(12, 55), 16, Estilo.PETROLEO)
	elif fase == Fase.RITMO:
		_dibujar_ritmo()
	else:
		_herramienta(int(ficha["herramienta"]) if fase != Fase.FALLO else seleccion, Vector2(827, 203), 1.4)
		_letra("Conserva la muestra y su origen", Vector2(610, 320), 19)
	_letra("Origen %s → bolsa %d" % [ficha["lugar"], int(ficha["bolsa"])], Vector2(24, 364), 21)
	_letra("Etiquetas y croquis: ejercicio del sueño.", Vector2(610, 364), 16, Estilo.TINTA_SUAVE)
	if fase == Fase.RITMO:
		_caja(MARTILLO, false, Estilo.CIAN)
		_letra("Golpear · Espacio", MARTILLO.position + Vector2(10, 27), 18)
	if _cantidad_opciones() > 0 or fase == Fase.RITMO:
		_caja(EXTRAER, true, Estilo.CIAN)
		_letra("Extraer · E" if fase == Fase.RITMO else "Confirmar selección · E", EXTRAER.position + Vector2(16, 27), 18)
	_letra("← ↑ ↓ →  Elegir   ·   E / Intro  Confirmar", Vector2(24, 478), 17)
	_letra("Referencia histórica: 21,5 kg en 58 muestras. Aquí recogemos 4 muestras del sueño.", Vector2(24, 511), 16, Estilo.TINTA_SUAVE)


func _terreno() -> void:
	_caja(Rect2(24, 90, 554, 248), false, Estilo.PETROLEO)
	# Facetas y pinceladas geometricas originales, sin texturas ni recursos externos.
	draw_colored_polygon(PackedVector2Array([Vector2(25, 205), Vector2(197, 122), Vector2(375, 181), Vector2(577, 136), Vector2(577, 337), Vector2(25, 337)]), Estilo.PAPEL_SOMBRA)
	draw_colored_polygon(PackedVector2Array([Vector2(25, 205), Vector2(197, 122), Vector2(232, 259), Vector2(25, 337)]), Estilo.CREMA)
	draw_colored_polygon(PackedVector2Array([Vector2(232, 259), Vector2(375, 181), Vector2(577, 337)]), Estilo.TINTA_SUAVE)
	for i in 26:
		var p: Vector2 = Vector2(46 + (i * 73) % 500, 239 + (i * 37) % 77)
		draw_line(p, p + Vector2(9, -3), Estilo.TINTA_SUAVE, 2)
	if muestra in [0, 1]:
		for i in 38:
			var p: Vector2 = Vector2(160 + (i * 41) % 245, 224 + (i * 17) % 58)
			if fase == Fase.FALLO and seleccion == 1:
				p.y += (2.2 - _transicion) * 25.0
			draw_circle(p, 2.0 if muestra == 0 else 4.0, Estilo.TINTA_SUAVE)
	elif muestra == 2:
		draw_colored_polygon(PackedVector2Array([Vector2(207, 275), Vector2(229, 209), Vector2(294, 187), Vector2(349, 229), Vector2(333, 282)]), Estilo.TINTA_SUAVE)
		draw_colored_polygon(PackedVector2Array([Vector2(229, 209), Vector2(294, 187), Vector2(282, 247), Vector2(207, 275)]), Estilo.PAPEL)
		draw_colored_polygon(PackedVector2Array([Vector2(294, 187), Vector2(349, 229), Vector2(282, 247)]), Estilo.CREMA)
	else:
		for i in 5:
			var rect: Rect2 = Rect2(148, 194 + i * 23, 300, 23)
			draw_rect(rect, [Estilo.PAPEL, Estilo.TINTA_SUAVE, Estilo.CREMA, Estilo.PETROLEO, Estilo.PAPEL_SOMBRA][i])
			if fase == Fase.FALLO and seleccion == 0:
				draw_line(Vector2(170 + i * 31, 193), Vector2(300 + i * 29, 307), Estilo.TINTA_SUAVE, 10)
		if fase == Fase.RITMO or recogida:
			var h: float = 30.0 + minf(float(golpes) / GOLPES, 1.0) * 85.0
			draw_rect(Rect2(288, 186, 24, h), Color(Estilo.PAPEL, 0.7))
			draw_rect(Rect2(288, 186, 24, h), Estilo.TINTA, false, 3)
			_herramienta(3, Vector2(348, 145 + (8.0 if fmod(ritmo, 1.0) < 0.15 else 0.0)), 0.7)
	if recogida and fase not in [Fase.RECOGIDA, Fase.RITMO]:
		_bolsa(Vector2(490, 191), int(MUESTRAS[muestra]["bolsa"]) if bolsa_guardada > 0 else 0)
	_letra("Regolito: polvo y escombros de impactos", Vector2(40, 115), 16, Estilo.PAPEL)


func _herramienta(tipo: int, centro: Vector2, escala: float) -> void:
	draw_set_transform(centro, -0.18 if tipo == 3 else 0.0, Vector2.ONE * escala)
	if tipo == 0:
		draw_line(Vector2(25, -65), Vector2(-8, 23), Estilo.TINTA, 13)
		draw_line(Vector2(25, -65), Vector2(-8, 23), Estilo.CREMA, 7)
		draw_colored_polygon(PackedVector2Array([Vector2(-40, 8), Vector2(11, 16), Vector2(31, 52), Vector2(-39, 49)]), Estilo.PETROLEO)
		draw_polyline(PackedVector2Array([Vector2(-40, 8), Vector2(11, 16), Vector2(31, 52), Vector2(-39, 49), Vector2(-40, 8)]), Estilo.TINTA, 4)
		draw_line(Vector2(-32, 20), Vector2(8, 26), Estilo.PAPEL, 4)
	elif tipo == 1:
		draw_polyline(PackedVector2Array([Vector2(-31, 52), Vector2(-9, -55), Vector2(9, -55), Vector2(31, 52)]), Estilo.TINTA, 12)
		draw_polyline(PackedVector2Array([Vector2(-31, 52), Vector2(-9, -55), Vector2(9, -55), Vector2(31, 52)]), Estilo.PAPEL_SOMBRA, 6)
		draw_line(Vector2(-31, 52), Vector2(-16, 46), Estilo.PAPEL, 6)
		draw_line(Vector2(31, 52), Vector2(16, 46), Estilo.PAPEL, 6)
	elif tipo == 2:
		draw_rect(Rect2(-34, -56, 25, 111), Estilo.PAPEL_SOMBRA)
		draw_rect(Rect2(-34, -56, 25, 111), Estilo.TINTA, false, 4)
		draw_line(Vector2(-28, -47), Vector2(-28, 44), Estilo.PAPEL, 4)
		draw_line(Vector2(28, 51), Vector2(28, -27), Estilo.CREMA, 9)
		draw_rect(Rect2(4, -45, 54, 24), Estilo.PETROLEO)
		draw_rect(Rect2(4, -45, 54, 24), Estilo.TINTA, false, 3)
	else:
		draw_line(Vector2(0, 45), Vector2(0, -20), Estilo.TINTA, 12)
		draw_line(Vector2(0, 45), Vector2(0, -20), Estilo.CREMA, 7)
		draw_rect(Rect2(-30, -44, 60, 28), Estilo.PAPEL_SOMBRA)
		draw_rect(Rect2(-30, -44, 60, 28), Estilo.TINTA, false, 3)
	draw_set_transform(Vector2.ZERO)


func _bolsa(centro: Vector2, numero: int) -> void:
	var puntos: PackedVector2Array = PackedVector2Array([centro + Vector2(-31, -40), centro + Vector2(31, -40), centro + Vector2(40, 43), centro + Vector2(-38, 43), centro + Vector2(-31, -40)])
	draw_colored_polygon(puntos, Estilo.CREMA)
	draw_polyline(puntos, Estilo.TINTA, 3)
	draw_line(centro + Vector2(-32, -28), centro + Vector2(32, -28), Estilo.TINTA_SUAVE, 3)
	draw_rect(Rect2(centro + Vector2(-21, -12), Vector2(42, 37)), Estilo.PAPEL)
	_letra(str(numero) if numero > 0 else "?", centro + Vector2(-9, 15), 26)


func _dibujar_ritmo() -> void:
	_letra("Tubo de 2 cm · %d / 4 golpes" % golpes, Vector2(610, 111), 23)
	_letra("Ritmo del sueño: 1 pulso/s", Vector2(610, 151), 18)
	_letra("Regla didáctica, sin profundidad real", Vector2(610, 178), 16, Estilo.TINTA_SUAVE)
	var barra: Rect2 = Rect2(622, 212, 460, 54)
	_caja(barra, false, Estilo.PAPEL_SOMBRA)
	var margen: float = ventana * 460.0 / PERIODO
	draw_rect(Rect2(852 - margen, 212, margen * 2.0, 54), Estilo.CIAN)
	draw_line(Vector2(852, 207), Vector2(852, 274), Estilo.TINTA, 2)
	# Antes del primer barrido la aguja espera al borde, no invita a golpear en t=0.
	var fase_pulso: float = fposmod(ritmo / PERIODO + 0.5, 1.0) if ritmo >= 0.5 else 0.0
	var x: float = 622.0 + fase_pulso * 460.0
	draw_line(Vector2(x, 207), Vector2(x, 274), Estilo.TINTA, 5)
	_letra("Golpea en el centro · margen ±%.2f s" % ventana, Vector2(610, 302), 18)
	_letra("4 golpes, luego E · Desajustes %d / 2" % desajustes, Vector2(610, 329), 18)


func jugar_solo(acierta: bool) -> void:
	# Solo elige, confirma y golpea mediante las mismas operaciones de la persona.
	_auto = 1 if acierta else -1
	_pulso_auto = 0.0
