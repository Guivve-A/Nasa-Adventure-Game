extends "res://nucleo/minijuego.gd"

# Motor didactico normalizado: inercia 1, rozamiento viscoso 0.6.
# x'' = K(r-x) - (D+0.6)x' + (D+0.6)v_conocida.
# Derivada de la medida: evita un impulso al cambiar la referencia.
const H: float = 1.0 / 240.0
const DURACION: float = 5.0
const ROCE: float = 0.6
const BANDA: float = 0.04
const SOBRE: float = 0.05
const ERROR_FINAL: float = 0.015
const GIRO: float = 15.0
const RELOJ: float = 720.0

var rampa: bool = false
var valores: Array[float] = [16.0, 1.0, 0.0]
var base: Array[float] = []
var usados: Array[float] = []
var diales: Array[HSlider] = []
var nombres: Array[Label] = []
var seleccion: int = 0
var pruebas: int = 0
var max_pruebas: int = 5
var probando: bool = false
var acumulado: float = 0.0
var reloj: float = 0.0
var posicion: float = 0.0
var velocidad: float = 0.0
var sobrepaso: float = 0.0
var ultimo_fuera: float = 0.0
var error_final: float = 0.0
var asentamiento: float = 0.0
var trazo: Array[Vector3] = []
var anterior: Array[Vector3] = []
var medidas: String = "Sin medir"
var medidas_antes: String = "Sin prueba anterior"
var estado: Label
var contador: Label
var lectura: Label
var lectura_antes: Label
var boton: Button
var elegir: Array[Button] = []
var _auto: int = 0
var _pausa_auto: float = 0.0
var _ajuste_resto: float = 0.0


func _preparar() -> void:
	rampa = parametros.get("modo", "") == "prealimentacion"
	max_pruebas = 7 - dificultad
	if rampa:
		valores = [8.0, 5.0, 0.0]
	elif dificultad > 1:
		valores = [4.0 if dificultad == 2 else 2.0, 1.0, 0.0]
	base = valores.duplicate()
	contador = _label("", Vector2(20, 8), 1080, 20)
	_label("ACTUAL · respuesta continua", Vector2(356, 48), 350)
	_label("ANTERIOR · respuesta discontinua", Vector2(738, 48), 360)
	for i in (3 if rampa else 2):
		var y: float = 66.0 + i * 76.0
		nombres.append(_label("", Vector2(20, y), 320, 18))
		var dial: HSlider = HSlider.new()
		dial.position = Vector2(24, y + 29)
		dial.size = Vector2(300, 28)
		dial.min_value = 1.0 if i == 0 else 0.0
		dial.max_value = 25.0 if i == 0 else (14.0 if i == 1 else GIRO)
		dial.step = 0.5
		dial.value = valores[i]
		dial.focus_mode = Control.FOCUS_NONE
		var id_ficha: String = ["ganancia", "amortiguacion", "prealimentacion"][i]
		dial.tooltip_text = String(Juego.ficha(id_ficha).get("texto", ""))
		dial.value_changed.connect(func(v: float): _cambiar(i, v))
		add_child(dial)
		diales.append(dial)
		var rotulo: String = ["Solo ganancia", "Solo amortiguación", "Solo cielo conocido"][i]
		var conservar: Button = Estilo.boton(rotulo, 16)
		conservar.position = Vector2(356 + i * 246, 426)
		conservar.size = Vector2(238, 38)
		conservar.focus_mode = Control.FOCUS_NONE
		conservar.pressed.connect(func(): _conservar(i))
		add_child(conservar)
		elegir.append(conservar)
	boton = Estilo.boton("Probar · E / Intro", 20, true)
	boton.position = Vector2(20, 306)
	boton.size = Vector2(308, 44)
	boton.focus_mode = Control.FOCUS_NONE
	boton.pressed.connect(_probar)
	add_child(boton)
	_label("↑ ↓ elegir · ← → ajustar\nEspacio: conservar solo el elegido", Vector2(20, 360), 310)
	_label("Modelo didáctico: inercia y roce.\nCrema: luz · cian: motor.\nEn rampa, 1 = 15°.", Vector2(20, 414), 310)
	lectura = _label("", Vector2(356, 365), 360)
	lectura_antes = _label("", Vector2(738, 365), 360)
	estado = _label("Cambia 1 parámetro y compara las curvas.", Vector2(20, 473), 1080, 18)
	_refrescar()


func _label(s: String, p: Vector2, ancho: float, tam: int = 16) -> Label:
	var l: Label = texto(s, tam, Estilo.TINTA, 500)
	l.position = p
	l.custom_minimum_size.x = ancho
	add_child(l)
	return l


func _empezar() -> void:
	_refrescar()


func _cambiar(i: int, v: float) -> void:
	if not activo or probando:
		return
	seleccion = i
	valores[i] = v
	_refrescar()


func _cambios() -> int:
	var cantidad: int = 0
	for i in valores.size():
		if absf(valores[i] - base[i]) > 0.01:
			cantidad += 1
	return cantidad


func _conservar(indice: int) -> void:
	if not activo or probando:
		return
	for i in valores.size():
		if i != indice:
			valores[i] = base[i]
			if i < diales.size():
				diales[i].set_value_no_signal(base[i])
	estado.text = "Conservaste 1 cambio. Ahora puedes probar."
	_refrescar()


func _input(e: InputEvent) -> void:
	if not activo or probando or _auto != 0:
		return
	if e.is_action_pressed("mover_arriba"):
		seleccion = posmod(seleccion - 1, diales.size())
	elif e.is_action_pressed("mover_abajo"):
		seleccion = posmod(seleccion + 1, diales.size())
	elif e.is_action_pressed("saltar"):
		_conservar(seleccion)
	elif e.is_action_pressed("interactuar"):
		_probar()
	else:
		return
	_refrescar()
	get_viewport().set_input_as_handled()


func _paso(delta: float) -> void:
	if probando:
		acumulado += delta
		while acumulado >= H and probando and activo:
			acumulado -= H
			_integrar()
	elif _auto != 0:
		_pausa_auto += delta
		if _pausa_auto >= 0.3:
			_pausa_auto = 0.0
			# El piloto mueve un solo dial antes de pulsar el mismo boton.
			if _auto > 0:
				if rampa:
					diales[2].value = GIRO
				elif absf(valores[0] - 16.0) > 0.01:
					diales[0].value = 16.0
				else:
					diales[1].value = 6.5
			_probar()
	else:
		var eje: float = eje_x()
		if is_zero_approx(eje):
			_ajuste_resto = 0.0
		else:
			_ajuste_resto += eje * delta * 5.0
			while absf(_ajuste_resto) >= 0.5:
				var cambio: float = signf(_ajuste_resto) * 0.5
				_ajuste_resto -= cambio
				diales[seleccion].value += cambio
	if activo and tiempo >= 180.0:
		terminar(false, 0, "Pasaron 180 s. El motor necesita una prueba para medir su atraso y sus oscilaciones.")
	_refrescar()


func _probar() -> void:
	if not activo or probando:
		return
	if _cambios() > 1:
		estado.text = "Cambiaste varios parámetros. Elige 1 y pulsa Espacio o «Conservar solo…»."
		_refrescar()
		return
	if not trazo.is_empty():
		anterior = trazo.duplicate()
		medidas_antes = "K %.1f · D %.1f · cielo %.1f°/h\n%s" % [usados[0], usados[1], usados[2], medidas]
	usados = valores.duplicate()
	base = valores.duplicate()
	pruebas += 1
	probando = true
	reloj = 0.0
	acumulado = 0.0
	posicion = 0.0
	velocidad = 0.0
	sobrepaso = 0.0
	ultimo_fuera = 0.0
	trazo.clear()
	medidas = "Midiendo durante 5 s…"
	_refrescar()


func _referencia(t: float) -> float:
	return GIRO / 3600.0 * RELOJ / GIRO * t if rampa else (1.0 if t >= 0.35 else 0.0)


func _corte(t: float) -> bool:
	return rampa and dificultad == 3 and ((t >= 1.1 and t < 1.2) or (t >= 1.9 and t < 2.0))


func _integrar() -> void:
	reloj += H
	var referencia: float = _referencia(reloj)
	var conocida: float = usados[2] / 3600.0 * RELOJ / GIRO if rampa else 0.0
	var motor: float = usados[0] * (referencia - posicion) - usados[1] * velocidad + (usados[1] + ROCE) * conocida
	if _corte(reloj):
		motor = 0.0
	velocidad += (motor - ROCE * velocidad) * H
	posicion += velocidad * H
	var error: float = referencia - posicion
	if rampa or reloj >= 0.35:
		sobrepaso = maxf(sobrepaso, -error)
		if absf(error) > BANDA:
			ultimo_fuera = reloj
	if trazo.is_empty() or int(round(reloj / H)) % 4 == 0:
		trazo.append(Vector3(reloj, referencia, posicion))
	if reloj + H * 0.1 >= DURACION:
		error_final = absf(error)
		asentamiento = maxf(0.0, ultimo_fuera - (0.0 if rampa else 0.35))
		_evaluar()


func _limite_asentamiento() -> float:
	return 3.8 if rampa else 2.5


func _causa() -> String:
	if rampa and usados[2] < GIRO - 0.1:
		return "La rampa deja atraso constante: falta dar al motor los 15°/h previstos del cielo."
	if sobrepaso > SOBRE:
		return "La ganancia empuja y falta amortiguación: el motor se pasa y oscila."
	if usados[1] > 2.0 * sqrt(usados[0]):
		return "Demasiada amortiguación frena el motor: llega tarde a la referencia."
	return "Con poca ganancia el motor corrige despacio y se atrasa; aumenta la ganancia en 1 prueba."


func _evaluar() -> void:
	probando = false
	medidas = "Asienta %.2f s · sobrepasa %.1f %%\nError final %.2f %%" % [asentamiento, sobrepaso * 100, error_final * 100]
	var gana: bool = asentamiento <= _limite_asentamiento() and sobrepaso <= SOBRE and error_final <= ERROR_FINAL
	print("SEGUIDOR modo=%s d=%d prueba=%d K=%.1f D=%.1f cielo=%.1f asienta=%.3f sobre=%.5f error=%.5f juego=%.2f" % ["rampa" if rampa else "paso", dificultad, pruebas, usados[0], usados[1], usados[2], asentamiento, sobrepaso, error_final, tiempo])
	if gana:
		if rampa:
			Juego.anotar("prealimentacion")
		terminar(true, 100.0, "La respuesta queda en la franja: " + medidas.replace("\n", ". ") + (". La prealimentación anticipa el giro y la realimentación corrige el resto." if rampa else ". Ganancia y amortiguación equilibran rapidez y estabilidad."))
	elif pruebas >= max_pruebas:
		terminar(false, 0.0, _causa() + " " + medidas.replace("\n", ". "))
	else:
		estado.text = _causa()
	_refrescar()


func _refrescar() -> void:
	contador.text = "%s · Prueba %d/%d · %.1f/5 s%s" % ["Rampa · 15°/h · reloj ×720" if rampa else "Punto de luz · salto de referencia", pruebas, max_pruebas, reloj, " · corte de energía" if _corte(reloj) else ""]
	var titulos: Array[String] = ["GANANCIA", "AMORTIGUACIÓN", "Velocidad conocida del cielo"]
	for i in diales.size():
		nombres[i].text = "%s%s: %.1f%s" % ["› " if seleccion == i else "", titulos[i], valores[i], "°/h" if i == 2 else ""]
		if i == 2:
			nombres[i].text = "%sVelocidad conocida del cielo\n%.1f°/h" % ["› " if seleccion == i else "", valores[i]]
			diales[i].position.y = 268
		diales[i].editable = activo and not probando
	for b in elegir:
		b.visible = _cambios() > 1 and not probando
	boton.disabled = not activo or probando
	boton.text = "Midiendo…" if probando else "Probar · E / Intro"
	lectura.text = medidas
	lectura_antes.text = medidas_antes
	queue_redraw()


func _punto(t: float, v: float, x: float) -> Vector2:
	return Vector2(x + t / DURACION * 340.0, 337.0 - clampf(v, -0.2, 1.6) * 130.0)


func _draw() -> void:
	for panel in 2:
		var x: float = 356.0 + panel * 382.0
		draw_style_box(Estilo.caja(Estilo.PETROLEO, 8, 2), Rect2(x - 8, 80, 360, 276))
		var datos: Array[Vector3] = trazo if panel == 0 else anterior
		# Franja de error y linea vertical: limites didacticos del modelo.
		var banda: PackedVector2Array = PackedVector2Array()
		for i in 101:
			var t: float = i * DURACION / 100.0
			banda.append(_punto(t, _referencia(t) + BANDA, x))
		for i in range(100, -1, -1):
			var t: float = i * DURACION / 100.0
			banda.append(_punto(t, _referencia(t) - BANDA, x))
		draw_colored_polygon(banda, Color(Estilo.CREMA, 0.32))
		var final: PackedVector2Array = PackedVector2Array([
			_punto(4.5, _referencia(4.5) + ERROR_FINAL, x),
			_punto(5.0, _referencia(5.0) + ERROR_FINAL, x),
			_punto(5.0, _referencia(5.0) - ERROR_FINAL, x),
			_punto(4.5, _referencia(4.5) - ERROR_FINAL, x)])
		draw_colored_polygon(final, Color(Estilo.DORADO, 0.6))
		for i in 100:
			if i % 2 == 0:
				var t: float = i * DURACION / 100.0
				draw_line(_punto(t, _referencia(t) + SOBRE, x), _punto(t + 0.05, _referencia(t + 0.05) + SOBRE, x), Color(Estilo.CREMA, 0.7), 1)
		for i in 6:
			var gx: float = x + i * 68.0
			draw_line(Vector2(gx, 100), Vector2(gx, 340), Color(Estilo.PAPEL, 0.16))
			draw_string(Estilo.fuente(), Vector2(gx, 352), str(i), HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Estilo.PAPEL)
		var limite: float = _limite_asentamiento() + (0.0 if rampa else 0.35)
		draw_line(_punto(limite, -0.1, x), _punto(limite, 1.7, x), Estilo.CREMA, 1)
		var ref: PackedVector2Array = PackedVector2Array()
		var respuesta: PackedVector2Array = PackedVector2Array()
		for dato in datos:
			ref.append(_punto(dato.x, dato.y, x))
			respuesta.append(_punto(dato.x, dato.z, x))
		if ref.size() > 1:
			draw_polyline(ref, Estilo.PAPEL, 2, true)
			if panel == 0:
				draw_polyline(respuesta, Estilo.CIAN, 3, true)
				draw_circle(ref[-1], 5, Estilo.CREMA)
			else:
				for i in range(1, respuesta.size()):
					if i % 6 < 3:
						draw_line(respuesta[i - 1], respuesta[i], Color(Estilo.CIAN, 0.5), 2, true)
		if rampa and dificultad == 3:
			for corte in [1.1, 1.9]:
				draw_rect(Rect2(x + corte / 5.0 * 340, 100, 6.8, 238), Color(Estilo.CORAL, 0.2))
		draw_string(Estilo.fuente(), Vector2(x, 101), "Franja ±4 % · final ≤1,5 %", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Estilo.PAPEL)
		draw_string(Estilo.fuente(), Vector2(x, 123), "Asienta ≤%.1f s · sobrepaso ≤5 %%" % _limite_asentamiento(), HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Estilo.PAPEL)


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1
