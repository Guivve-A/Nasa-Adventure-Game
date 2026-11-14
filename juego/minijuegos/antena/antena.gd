extends "res://nucleo/minijuego.gd"

# Modelo didactico; los parametros no describen el equipo historico.
# u = K * error; cola de 0,25 s y actuador de primer orden de 0,12 s.
const PASO: float = 1.0 / 120.0
const RETARDO_PASOS: int = 30
const TAU_MOTOR: float = 0.12
const MAX_VELOCIDAD: float = 95.0
const ANCHO_SENAL: float = 14.0
const UMBRAL: float = 70.0
const FRACCION: float = 0.80
const LIMITE: float = 180.0
const MAX_PRUEBAS: int = 3
const BASE: Vector2 = Vector2(280, 245)
const RADIO: float = 185.0

var ganancia: float = 1.2
var duracion: float = 10.0
var paso_s: float = 0.0
var antena: float = -72.0
var satelite: float = -60.0
var velocidad: float = 0.0
var senal: float = 0.0
var sostenido: float = 0.0
var viento: float = 0.0
var pruebas: int = 0
var cruces: int = 0
var _signo: int = 1
var _cola: Array[float] = []
var _indice: int = 0
var _acumulado: float = 0.0
var _resto_mando: float = 0.0
var _corriendo: bool = false
var _auto: int = 0
var _trazo: PackedVector2Array = PackedVector2Array()
var _anterior: PackedVector2Array = PackedVector2Array()
var _ultimo: Dictionary = {}
var _dato_anterior: String = "Aún no hay prueba."
var _causa: String = "Ajusta la ganancia y pulsa Probar."
var _dial: HSlider
var _boton: Button
var _ganancia_texto: Label
var _estado: Label
var _senal_texto: Label
var _cobertura: Label
var _actual_texto: Label
var _previo_texto: Label
var _mensaje: Label
var _barra: ProgressBar


func _preparar() -> void:
	duracion = [10.0, 8.5, 7.0][dificultad - 1]
	# El hueco del anfitrion conserva la comparacion si se reintenta.
	var clave: String = "antena_anterior_%d" % dificultad
	if get_parent().has_meta(clave):
		var registro: Dictionary = get_parent().get_meta(clave)
		_anterior = registro["trazo"]
		_dato_anterior = registro["dato"]
	_etiqueta("PASO SIMULADO · %.1f s" % duracion, Vector2(32, 22), 490, 20, Estilo.PAPEL)
	_estado = _etiqueta("", Vector2(32, 279), 490, 16, Estilo.PAPEL)
	var ficha: Dictionary = Juego.ficha("estacion_cotopaxi")
	_etiqueta("QUITO · DATO VERIFICADO", Vector2(574, 20), 520, 18)
	_etiqueta(String(ficha.get("texto", "")), Vector2(574, 48), 520, 18)
	_etiqueta("ERROR DE APUNTADO · escala fija ±40°", Vector2(574, 123), 520, 18)
	_etiqueta("ACTUAL · línea continua", Vector2(602, 150), 235, 16)
	_etiqueta("ANTERIOR · línea a trazos", Vector2(861, 150), 235, 16)
	_actual_texto = _etiqueta("", Vector2(602, 391), 227, 18)
	_previo_texto = _etiqueta(_dato_anterior, Vector2(861, 391), 227, 18)
	_senal_texto = _etiqueta("", Vector2(32, 319), 490, 20)
	_barra = ProgressBar.new()
	_barra.position = Vector2(32, 352)
	_barra.size = Vector2(490, 22)
	_barra.max_value = 100.0
	_barra.show_percentage = false
	_barra.add_theme_stylebox_override("background", Estilo.caja(Estilo.PAPEL_SOMBRA, 4, 1))
	_barra.add_theme_stylebox_override("fill", Estilo.caja(Estilo.CIAN_MEDIO, 4))
	add_child(_barra)
	var marca: ColorRect = ColorRect.new()
	marca.color = Estilo.TINTA
	marca.position = Vector2(490 * 0.7, -2)
	marca.size = Vector2(3, 27)
	marca.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_barra.add_child(marca)
	_cobertura = _etiqueta("", Vector2(32, 385), 500, 18)
	_ganancia_texto = _etiqueta("", Vector2(32, 423), 300, 20)
	_dial = HSlider.new()
	_dial.position = Vector2(32, 461)
	_dial.size = Vector2(324, 32)
	_dial.min_value = 0.4
	_dial.max_value = 12.0
	_dial.step = 0.1
	_dial.value = ganancia
	_dial.focus_mode = Control.FOCUS_NONE
	_dial.add_theme_stylebox_override("slider", Estilo.caja(Estilo.PAPEL_SOMBRA, 4, 1))
	_dial.add_theme_stylebox_override("grabber_area", Estilo.caja(Estilo.CIAN_MEDIO, 4))
	_dial.value_changed.connect(_cambiar_ganancia)
	add_child(_dial)
	_boton = Estilo.boton("Probar", 22, true)
	_boton.position = Vector2(382, 449)
	_boton.size = Vector2(140, 48)
	_boton.focus_mode = Control.FOCUS_NONE
	_boton.pressed.connect(_probar)
	add_child(_boton)
	_mensaje = _etiqueta("", Vector2(574, 456), 520, 18)
	_actualizar()


func _etiqueta(contenido: String, pos: Vector2, ancho: float, tam: int, color: Color = Estilo.TINTA) -> Label:
	var etiqueta: Label = texto(contenido, tam, color)
	etiqueta.position = pos
	etiqueta.custom_minimum_size = Vector2(ancho, 0)
	add_child(etiqueta)
	return etiqueta


func _empezar() -> void:
	_actualizar()


func _cambiar_ganancia(valor: float) -> void:
	if not _corriendo:
		ganancia = valor
		_actualizar()


func _ajustar(mando: float, delta: float) -> void:
	if is_zero_approx(mando):
		_resto_mando = 0.0
		return
	_resto_mando += mando * delta * 6.0
	var pasos: int = int((absf(_resto_mando) + 0.000001) / 0.1)
	if pasos > 0:
		var cambio: float = signf(_resto_mando) * float(pasos) * 0.1
		_dial.value = clampf(ganancia + cambio, 0.4, 12.0)
		_resto_mando -= cambio


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or _corriendo:
		return
	if evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar"):
		_probar()
		get_viewport().set_input_as_handled()


func _paso(delta: float) -> void:
	if not _corriendo:
		var mando: float = eje_x()
		if _auto != 0:
			var objetivo: float = 3.0 if _auto > 0 else 12.0
			mando = clampf((objetivo - ganancia) / maxf(delta * 6.0, 0.0001), -1.0, 1.0)
			_ajustar(mando, delta)
			if absf(ganancia - objetivo) < 0.051:
				_probar()
		else:
			_ajustar(mando, delta)
	else:
		_acumulado += delta
		while _acumulado >= PASO and activo and _corriendo:
			_acumulado -= PASO
			_integrar()
	if activo and tiempo >= LIMITE:
		terminar(false, 0.0, "Pasaron 180 s sin sostener el enlace: el haz debe seguir al satélite. " + _causa)
	_actualizar()


func _probar() -> void:
	if not activo or _corriendo:
		return
	if not _ultimo.is_empty():
		_anterior = _ultimo["trazo"]
		_dato_anterior = _ultimo["dato"]
	pruebas += 1
	paso_s = 0.0
	antena = -72.0
	satelite = -60.0
	velocidad = 0.0
	sostenido = 0.0
	viento = 0.0
	cruces = 0
	_signo = 1
	_cola.resize(RETARDO_PASOS)
	_cola.fill(0.0)
	_indice = 0
	_acumulado = 0.0
	_trazo.clear()
	_trazo.append(Vector2(0, satelite - antena))
	_corriendo = true
	_dial.editable = false
	_boton.disabled = true
	_boton.text = "En paso…"
	_causa = "Observa el haz y el error; la ganancia queda fija."
	sonar("tic")
	_actualizar()


func _rafaga(t: float) -> float:
	if dificultad == 1:
		return 0.0
	var fuerza: float = 8.0 if dificultad == 2 else 14.0
	var total: float = 0.0
	for i in 2:
		var centro: float = duracion * (0.32 if i == 0 else 0.65)
		var x: float = (t - centro) / 0.32
		if absf(x) < 1.0:
			total += fuerza * (1.0 if i == 0 else -1.0) * pow(cos(x * PI * 0.5), 2.0)
	return total


func _integrar() -> void:
	paso_s += PASO
	var fase: float = minf(paso_s / duracion, 1.0)
	satelite = -60.0 + 120.0 * (fase - 0.1 * sin(TAU * fase) / TAU)
	var orden: float = clampf(ganancia * (satelite - antena), -MAX_VELOCIDAD, MAX_VELOCIDAD)
	var retardada: float = _cola[_indice]
	_cola[_indice] = orden
	_indice = (_indice + 1) % RETARDO_PASOS
	velocidad += (retardada - velocidad) * PASO / TAU_MOTOR
	viento = _rafaga(paso_s)
	antena += (velocidad + viento) * PASO
	var error: float = satelite - antena
	senal = 100.0 * exp(-pow(error / ANCHO_SENAL, 2.0))
	if senal > UMBRAL:
		sostenido += PASO
	var signo: int = 1 if error > 1.0 else (-1 if error < -1.0 else 0)
	if signo != 0:
		if signo != _signo:
			cruces += 1
		_signo = signo
	# Un punto cada cuatro pasos mantiene pequeno el coste de dibujado.
	if _indice % 4 == 0:
		_trazo.append(Vector2(paso_s, error))
	if paso_s >= duracion - PASO * 0.5:
		_cerrar_prueba()


func _cerrar_prueba() -> void:
	_corriendo = false
	_trazo.append(Vector2(duracion, satelite - antena))
	var porcentaje: float = 100.0 * sostenido / duracion
	var gana: bool = sostenido + 0.000001 >= duracion * FRACCION
	var dato: String = "K %.1f · %.1f %% útil\n%d cruces de 0°" % [ganancia, porcentaje, cruces]
	_ultimo = {"trazo": _trazo.duplicate(), "dato": dato}
	get_parent().set_meta("antena_anterior_%d" % dificultad, _ultimo.duplicate(true))
	if gana:
		_causa = "La ganancia sostiene el haz sobre el satélite."
	elif cruces >= 5 or ganancia > 3.2:
		_causa = "El motor recibe tarde correcciones grandes: el haz se pasa y oscila. Baja la ganancia."
	else:
		_causa = "El motor corrige poco y el haz se atrasa. Sube la ganancia hacia 3,0."
	print("ANTENA d%d K=%.1f paso=%.1f util=%.3f porcentaje=%.3f cruces=%d prueba=%d" % [dificultad, ganancia, duracion, sostenido, porcentaje, cruces, pruebas])
	_dial.editable = true
	_boton.disabled = false
	_boton.text = "Probar"
	if gana or pruebas >= MAX_PRUEBAS:
		terminar(gana, porcentaje if gana else 0.0, "Señal > 70 %% durante %.1f %% del paso; meta: 80 %%. %s" % [porcentaje, _causa])
	else:
		sonar("radio")
	_actualizar()


func _actualizar() -> void:
	_ganancia_texto.text = "GANANCIA  %.1f" % ganancia
	_senal_texto.text = "Señal recibida: %.0f %% · umbral > 70 %%" % senal
	_barra.value = senal
	_cobertura.text = "Tiempo útil: %.1f / %.1f s · meta: 80 %% del paso" % [sostenido, duracion * FRACCION]
	_estado.text = "%.1f / %.1f s · %s · prueba %d de 3" % [paso_s, duracion, "ráfaga de viento" if absf(viento) > 0.1 else ("sin viento" if dificultad == 1 else "2 ráfagas por paso"), pruebas]
	_actual_texto.text = "K %.1f · %.1f %% útil\nError: %+.1f°" % [ganancia, sostenido / duracion * 100.0, satelite - antena]
	_previo_texto.text = _dato_anterior
	_mensaje.text = _causa
	queue_redraw()


func _direccion(grados: float) -> Vector2:
	return Vector2(sin(deg_to_rad(grados)), -cos(deg_to_rad(grados)))


func _draw() -> void:
	draw_style_box(Estilo.caja(Estilo.PETROLEO, 12, 2), Rect2(16, 12, 528, 294))
	# Relieve facetado y cielo esquematico, sin dimensiones historicas.
	draw_colored_polygon(PackedVector2Array([Vector2(18, 272), Vector2(18, 235), Vector2(94, 213), Vector2(146, 244), Vector2(198, 226), Vector2(287, 274)]), Estilo.VERDE)
	draw_colored_polygon(PackedVector2Array([Vector2(310, 274), Vector2(412, 220), Vector2(448, 240), Vector2(542, 222), Vector2(542, 274)]), Estilo.TINTA_SUAVE)
	var arco: PackedVector2Array = PackedVector2Array()
	for i in 61:
		arco.append(BASE + _direccion(-60.0 + float(i) * 2.0) * RADIO)
	draw_polyline(arco, Color(Estilo.PAPEL, 0.65), 2.0, true)
	var dir: Vector2 = _direccion(antena)
	var lateral: Vector2 = dir.orthogonal()
	draw_colored_polygon(PackedVector2Array([BASE, BASE + _direccion(antena - 8.36) * RADIO, BASE + _direccion(antena + 8.36) * RADIO]), Color(Estilo.CIAN, 0.14))
	draw_line(BASE, BASE + dir * RADIO, Estilo.CIAN, 2.0, true)
	draw_line(BASE + Vector2(0, -4), BASE + Vector2(-18, 10), Estilo.TINTA, 7.0, true)
	draw_line(BASE + Vector2(0, -4), BASE + Vector2(18, 10), Estilo.TINTA, 7.0, true)
	var plato: PackedVector2Array = PackedVector2Array()
	for i in 17:
		var x: float = -32.0 + float(i) * 4.0
		plato.append(BASE + lateral * x + dir * (x * x / 70.0 - 10.0))
	var silueta: PackedVector2Array = plato.duplicate()
	silueta.append(BASE + lateral * 32.0 + dir * -14.0)
	silueta.append(BASE - lateral * 32.0 + dir * -14.0)
	draw_colored_polygon(silueta, Estilo.CREMA)
	draw_polyline(plato, Estilo.PAPEL, 4.0, true)
	draw_line(BASE, BASE + dir * 24.0, Estilo.TINTA, 3.0, true)
	draw_circle(BASE + dir * 24.0, 4, Estilo.CIAN)
	var sat: Vector2 = BASE + _direccion(satelite) * RADIO
	draw_line(sat - Vector2(20, 0), sat + Vector2(20, 0), Estilo.TINTA, 4.0)
	draw_rect(Rect2(sat - Vector2(23, 7), Vector2(14, 14)), Estilo.CREMA)
	draw_rect(Rect2(sat + Vector2(9, -7), Vector2(14, 14)), Estilo.CREMA)
	draw_rect(Rect2(sat - Vector2(7, 8), Vector2(14, 16)), Estilo.PAPEL)
	_grafica(Rect2(602, 178, 211, 185), _trazo, false)
	_grafica(Rect2(861, 178, 211, 185), _anterior, true)


func _grafica(rect: Rect2, trazo: PackedVector2Array, anterior: bool) -> void:
	draw_style_box(Estilo.caja(Estilo.PAPEL_SOMBRA, 4, 1), rect)
	var centro_y: float = rect.get_center().y
	var banda: float = 8.36 / 40.0 * rect.size.y * 0.5
	draw_rect(Rect2(rect.position.x, centro_y - banda, rect.size.x, banda * 2.0), Color(Estilo.PETROLEO, 0.13))
	draw_line(Vector2(rect.position.x, centro_y), Vector2(rect.end.x, centro_y), Estilo.TINTA_SUAVE, 1.0)
	var fuente: Font = Estilo.fuente()
	for y in [-40, 0, 40]:
		var pos: Vector2 = Vector2(rect.position.x - 30, centro_y - float(y) / 40.0 * rect.size.y * 0.5 + 6)
		draw_string(fuente, pos, "%d" % y, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Estilo.TINTA_SUAVE)
	draw_string(fuente, Vector2(rect.position.x, rect.end.y + 21), "0", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Estilo.TINTA_SUAVE)
	draw_string(fuente, Vector2(rect.end.x - 42, rect.end.y + 21), "%.1f s" % duracion, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Estilo.TINTA_SUAVE)
	for i in range(1, trazo.size()):
		if anterior and i % 6 >= 3:
			continue
		var a: Vector2 = Vector2(rect.position.x + trazo[i - 1].x / duracion * rect.size.x, centro_y - clampf(trazo[i - 1].y, -40, 40) / 40.0 * rect.size.y * 0.5)
		var b: Vector2 = Vector2(rect.position.x + trazo[i].x / duracion * rect.size.x, centro_y - clampf(trazo[i].y, -40, 40) / 40.0 * rect.size.y * 0.5)
		draw_line(a, b, Estilo.TERRACOTA if anterior else Estilo.CIAN_MEDIO, 2.5, true)


func jugar_solo(acierta: bool) -> void:
	# Usa el mismo ajuste y el mismo boton; solo el modelo decide el resultado.
	_auto = 1 if acierta else -1
