extends "res://nucleo/minijuego.gd"

# Unidades fisicas: km y s. Constantes del modelo indicadas en el encargo.
# Alturas: ficha pegaso_orbita (627 x 654 km); no reproduce su orbita real.
const MU: float = 398600.0
const RADIO: float = 6371.0
const PASO: float = 2.0
const ACELERACION: float = 300.0
const LIMITE_VUELO: float = 9600.0
const LIMITE_PARTIDA: float = 180.0
# Corte didactico, no espesor medido de la atmosfera. No se simula arrastre.
const CORTE_ATMOSFERA: float = 120.0
const CENTRO: Vector2 = Vector2(345, 246)

var altura: float = 627.0
var margen: float = 150.0
var circular: float = 0.0
var velocidad: float = 7.2
var posicion: Vector2 = Vector2.ZERO
var vector_velocidad: Vector2 = Vector2.ZERO
var minima: float = 0.0
var maxima: float = 0.0
var angulo: float = 0.0
var segundos_fisicos: float = 0.0
var _acumulado: float = 0.0
var _volando: bool = false
var _auto: int = 0
var _trazo: PackedVector2Array = PackedVector2Array()
var _anterior: PackedVector2Array = PackedVector2Array()
var _dato_anterior: String = "Anterior: aún no hay lanzamiento"
var _dial: HSlider
var _lanzar_boton: Button
var _velocidad_texto: Label
var _lecturas: Label
var _estado: Label
var _progreso: ProgressBar


func _preparar() -> void:
	altura = 654.0 if dificultad == 3 else 627.0
	margen = [150.0, 80.0, 40.0][dificultad - 1]
	circular = sqrt(MU / (RADIO + altura))
	posicion = Vector2(RADIO + altura, 0)
	minima = altura
	maxima = altura
	# El hueco del anfitrion sobrevive al nodo que reemplaza al reintentar.
	var clave: String = "orbita_anterior_%d" % dificultad
	if get_parent().has_meta(clave):
		var registro: Dictionary = get_parent().get_meta(clave)
		_anterior = registro["trazo"]
		_dato_anterior = registro["dato"]
	_etiqueta("TIERRA · SIMULADOR 2D", Vector2(44, 26), 600, 18, Estilo.PAPEL)
	_etiqueta("— Actual     · · · Anterior", Vector2(44, 472), 590, 18, Estilo.PAPEL)
	_etiqueta("Altura de partida: %.0f km\nPegaso: 627 × 654 km (ficha)" % altura, Vector2(706, 22), 390, 21)
	_etiqueta("Modelo circular idealizado\nμ = 398 600 km³/s² · R = 6 371 km", Vector2(706, 88), 390, 17)
	_etiqueta("v = √(μ / r) = %.3f km/s\nCálculo propio · tiempo ×300" % circular, Vector2(706, 143), 390, 19)
	_velocidad_texto = _etiqueta("", Vector2(706, 211), 390, 22)
	_dial = HSlider.new()
	_dial.position = Vector2(706, 249)
	_dial.size = Vector2(386, 34)
	_dial.min_value = 5.0
	_dial.max_value = 11.5
	_dial.step = 0.001
	_dial.value = velocidad
	_dial.focus_mode = Control.FOCUS_NONE
	_dial.add_theme_stylebox_override("slider", Estilo.caja(Estilo.PAPEL_SOMBRA, 4, 1))
	_dial.add_theme_stylebox_override("grabber_area", Estilo.caja(Estilo.CIAN_MEDIO, 4))
	_dial.value_changed.connect(_cambiar_velocidad)
	add_child(_dial)
	_lanzar_boton = Estilo.boton("Lanzar", 22, true)
	_lanzar_boton.position = Vector2(706, 294)
	_lanzar_boton.size = Vector2(386, 48)
	_lanzar_boton.focus_mode = Control.FOCUS_NONE
	_lanzar_boton.pressed.connect(_lanzar)
	add_child(_lanzar_boton)
	_lecturas = _etiqueta("", Vector2(706, 356), 390, 20)
	_estado = _etiqueta("", Vector2(44, 400), 590, 18, Estilo.PAPEL)
	_progreso = ProgressBar.new()
	_progreso.position = Vector2(44, 432)
	_progreso.size = Vector2(590, 18)
	_progreso.add_theme_font_size_override("font_size", 16)
	_progreso.show_percentage = false
	_progreso.max_value = TAU
	_progreso.add_theme_stylebox_override("background", Estilo.caja(Estilo.TINTA, 3, 0, Estilo.TINTA, 0))
	_progreso.add_theme_stylebox_override("fill", Estilo.caja(Estilo.CIAN, 3, 0, Estilo.TINTA, 0))
	add_child(_progreso)
	_actualizar()


func _etiqueta(contenido: String, lugar: Vector2, ancho: float, tam: int, color: Color = Estilo.TINTA) -> Label:
	var l: Label = texto(contenido, tam, color)
	l.position = lugar
	l.custom_minimum_size = Vector2(ancho, 0)
	add_child(l)
	return l


func _empezar() -> void:
	_estado.text = "Preparado · 0 vueltas"


func _cambiar_velocidad(valor: float) -> void:
	if not _volando:
		velocidad = valor
		_actualizar()


func _ajustar(mando: float, delta: float) -> void:
	_dial.value = clampf(velocidad + mando * delta * 0.6, 5.0, 11.5)


func _input(evento: InputEvent) -> void:
	if not activo or _volando or _auto != 0:
		return
	if evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar"):
		_lanzar()
		get_viewport().set_input_as_handled()


func _paso(delta: float) -> void:
	if not _volando:
		var mando: float = eje_x()
		if _auto != 0:
			var objetivo: float = snappedf(circular, 0.001) if _auto > 0 else 5.5
			mando = clampf((objetivo - velocidad) / maxf(delta * 0.6, 0.0001), -1.0, 1.0)
			_ajustar(mando, delta)
			if absf(velocidad - objetivo) <= 0.0011:
				_lanzar()
		else:
			_ajustar(mando, delta)
	else:
		_acumulado += delta * ACELERACION
		while _acumulado >= PASO and activo:
			_acumulado -= PASO
			_integrar()
	if activo and tiempo >= LIMITE_PARTIDA:
		var causa: String = "Pasaron 180 s sin lanzar: el satélite necesita velocidad tangencial para rodear la Tierra." if not _volando else "La sesión llegó a 180 s antes de completar la vuelta. Lanza antes para poder observarla completa."
		terminar(false, 0, causa)
	_actualizar()
	queue_redraw()


func _lanzar() -> void:
	if not activo or _volando:
		return
	_volando = true
	_dial.editable = false
	_lanzar_boton.disabled = true
	_lanzar_boton.text = "En vuelo…"
	vector_velocidad = Vector2(0, -velocidad)
	_trazo.append(posicion)
	sonar("tic")


func _gravedad(punto: Vector2) -> Vector2:
	var radio: float = punto.length()
	return -MU * punto / (radio * radio * radio)


func _integrar() -> void:
	# Velocity Verlet: dos evaluaciones de gravedad, paso fijo, sin reloj externo.
	var previa: Vector2 = posicion
	var aceleracion: Vector2 = _gravedad(posicion)
	posicion += vector_velocidad * PASO + aceleracion * (0.5 * PASO * PASO)
	vector_velocidad += (aceleracion + _gravedad(posicion)) * (0.5 * PASO)
	segundos_fisicos += PASO
	angulo += absf(previa.angle_to(posicion))
	var h: float = posicion.length() - RADIO
	minima = minf(minima, h)
	maxima = maxf(maxima, h)
	if int(segundos_fisicos) % 8 == 0:
		_trazo.append(posicion)
	if h <= CORTE_ATMOSFERA:
		_finalizar(false, "Con %.3f km/s falta velocidad: roza la atmósfera y cae. Corte del modelo: 120 km; sin arrastre." % velocidad)
	elif angulo >= TAU:
		if maxima - minima < margen:
			_finalizar(true, "Una vuelta completa: altura mínima %.1f km y máxima %.1f km. Diferencia %.1f km < %.0f km." % [minima, maxima, maxima - minima, margen])
		else:
			var causa: String = "Sobra velocidad: la órbita se alarga en una elipse." if velocidad > circular else "Falta velocidad: la órbita baja y se alarga en una elipse."
			_finalizar(false, "%s Diferencia %.1f km; debe ser menor que %.0f km." % [causa, maxima - minima, margen])
	elif posicion.length() >= 2.0 * (RADIO + altura) and vector_velocidad.length_squared() * 0.5 - MU / posicion.length() >= 0.0:
		_finalizar(false, "Con %.3f km/s sobra velocidad: la energía orbital no es negativa y el satélite se escapa." % velocidad)
	elif segundos_fisicos >= LIMITE_VUELO:
		_finalizar(false, "Sobra velocidad: la elipse se alarga y no cierra una vuelta en 9 600 s simulados. Reduce la velocidad.")


func _finalizar(gana: bool, causa: String) -> void:
	_trazo.append(posicion)
	get_parent().set_meta("orbita_anterior_%d" % dificultad, {"trazo": _trazo.duplicate(), "dato": "Anterior: %.3f km/s · mín. %.0f / máx. %.0f km" % [velocidad, minima, maxima]})
	print("ORBITA d%d v=%.3f min=%.3f max=%.3f giro=%.6f fisica=%.0f juego=%.3f" % [dificultad, velocidad, minima, maxima, angulo, segundos_fisicos, tiempo])
	terminar(gana, 100.0 if gana else 0.0, causa)


func _actualizar() -> void:
	_velocidad_texto.text = "Velocidad tangencial: %.3f km/s" % velocidad
	_lecturas.text = "Mínima: %.1f km · Máxima: %.1f km\nDiferencia: %.1f / < %.0f km\n\n%s" % [minima, maxima, maxima - minima, margen, _dato_anterior]
	_progreso.value = minf(angulo, TAU)
	if _volando:
		_estado.text = "Vuelta: %.0f %% · Tiempo simulado: %.0f s" % [minf(100.0, angulo / TAU * 100.0), segundos_fisicos]
	queue_redraw()


func _pantalla(punto: Vector2, escala: float) -> Vector2:
	return CENTRO + punto * escala


func _draw() -> void:
	draw_style_box(Estilo.caja(Estilo.PETROLEO, 12, 2), Rect2(24, 16, 650, 484))
	var alcance: float = RADIO + altura
	for trazo in [_trazo, _anterior]:
		for punto in trazo:
			alcance = maxf(alcance, punto.length())
	var escala: float = 148.0 / alcance
	_dibujar_tierra(escala)
	draw_arc(CENTRO, (RADIO + CORTE_ATMOSFERA) * escala, 0, TAU, 64, Color(Estilo.PAPEL, 0.45), 1.0, true)
	for i in range(1, _anterior.size()):
		if i % 4 < 2:
			draw_line(_pantalla(_anterior[i - 1], escala), _pantalla(_anterior[i], escala), Color(Estilo.PAPEL, 0.38), 2.0, true)
	if _trazo.size() > 1:
		var linea: PackedVector2Array = PackedVector2Array()
		for punto in _trazo:
			linea.append(_pantalla(punto, escala))
		draw_polyline(linea, Estilo.CIAN, 2.5, true)
	var sat: Vector2 = _pantalla(posicion, escala)
	draw_line(sat + Vector2(-17, 0), sat + Vector2(17, 0), Estilo.TINTA, 5)
	draw_rect(Rect2(sat - Vector2(20, 6), Vector2(12, 12)), Estilo.CREMA)
	draw_rect(Rect2(sat + Vector2(8, -6), Vector2(12, 12)), Estilo.CREMA)
	draw_rect(Rect2(sat - Vector2(6, 6), Vector2(12, 12)), Estilo.CIAN)
	if not _volando:
		draw_line(sat + Vector2(0, -14), sat + Vector2(0, -48), Estilo.CIAN, 3, true)
		draw_line(sat + Vector2(0, -48), sat + Vector2(-6, -38), Estilo.CIAN, 3, true)
		draw_line(sat + Vector2(0, -48), sat + Vector2(6, -38), Estilo.CIAN, 3, true)


func _dibujar_tierra(escala: float) -> void:
	# Siluetas esquematicas; los triangulos suaves dan volumen al disco.
	var radio: float = RADIO * escala
	var borde: PackedVector2Array = PackedVector2Array()
	for i in 32:
		borde.append(CENTRO + Vector2.from_angle(TAU * i / 32.0) * radio)
	draw_colored_polygon(borde, Estilo.PETROLEO)
	for i in 12:
		var a: float = TAU * float(i) / 12.0
		var b: float = a + TAU / 12.0
		var triangulo: PackedVector2Array = PackedVector2Array([CENTRO + Vector2(-0.2, -0.15) * radio, CENTRO + Vector2.from_angle(a) * radio, CENTRO + Vector2.from_angle(b) * radio])
		draw_colored_polygon(triangulo, Color(Estilo.PAPEL if i > 5 else Estilo.TINTA, 0.08 + 0.02 * (i % 3)))
	var america: PackedVector2Array = PackedVector2Array([Vector2(-0.60, -0.67), Vector2(-0.2, -0.82), Vector2(0.02, -0.65), Vector2(-0.11, -0.3), Vector2(-0.25, -0.22), Vector2(-0.22, 0.02), Vector2(-0.06, 0.13), Vector2(0.04, 0.43), Vector2(-0.18, 0.77), Vector2(-0.31, 0.50), Vector2(-0.32, 0.22), Vector2(-0.50, 0.08), Vector2(-0.43, -0.16), Vector2(-0.7, -0.29)])
	var africa: PackedVector2Array = PackedVector2Array([Vector2(0.15, -0.62), Vector2(0.42, -0.78), Vector2(0.68, -0.62), Vector2(0.82, -0.3), Vector2(0.54, -0.12), Vector2(0.32, -0.12), Vector2(0.37, 0.1), Vector2(0.55, 0.22), Vector2(0.43, 0.58), Vector2(0.2, 0.45), Vector2(0.09, 0.17), Vector2(0.15, -0.05), Vector2(0.0, -0.19), Vector2(0.04, -0.37)])
	for tierra in [america, africa]:
		var puntos: PackedVector2Array = PackedVector2Array()
		for punto in tierra:
			puntos.append(CENTRO + punto * radio)
		draw_colored_polygon(puntos, Estilo.VERDE)
		draw_polyline(puntos, Estilo.CREMA, 1, true)
	draw_polyline(borde, Estilo.PAPEL_SOMBRA, 1.5, true)


func jugar_solo(acierta: bool) -> void:
	# Mueve el mismo deslizador y pulsa el mismo lanzamiento; no fuerza resultados.
	_auto = 1 if acierta else -1
