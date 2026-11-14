extends "res://nucleo/minijuego.gd"

# Minijuego de plantilla: «Sintoniza la señal». El ejemplo minimo de un minijuego completo.
# Se mueve un dial con izquierda y derecha (o con el raton) hasta que la onda propia coincide con la de
# referencia y se mantiene asi 1,5 s. Copia este archivo para empezar un minijuego nuevo.

const TOLERANCIA := 0.06      # diferencia de frecuencia aceptada
const SOSTENER_S := 1.5
const LIMITE_S := 30.0

var objetivo := 1.0           # frecuencia de la senal de referencia
var dial := 0.4               # frecuencia elegida por el jugador
var sostenido := 0.0
var _auto := 0                # 0 = juega la persona; 1 = solo y acierta; -1 = solo y falla
var _barra: ProgressBar
var _lectura: Label


func _preparar() -> void:
	objetivo = [1.3, 1.7, 2.3][dificultad - 1]
	dial = 0.5
	_lectura = texto("", 20, Estilo.TINTA, 600)
	_lectura.position = Vector2(24, 16)
	_lectura.custom_minimum_size = Vector2(700, 0)
	add_child(_lectura)
	_barra = ProgressBar.new()
	_barra.position = Vector2(24, size.y - 44)
	_barra.size = Vector2(size.x - 48, 22)
	_barra.max_value = SOSTENER_S
	_barra.show_percentage = false
	add_child(_barra)


func _empezar() -> void:
	sostenido = 0.0


func _paso(delta: float) -> void:
	# entrada: teclado o mando; el piloto de pruebas mueve el dial solo
	var mando := eje_x()
	if _auto == 1:
		mando = clampf((objetivo - dial) * 6.0, -1.0, 1.0)
	elif _auto == -1:
		mando = -1.0
	dial = clampf(dial + mando * delta * 0.8, 0.2, 3.0)
	var error := absf(dial - objetivo)
	if error < TOLERANCIA:
		sostenido += delta
	else:
		sostenido = maxf(sostenido - delta * 2.0, 0.0)
	_barra.value = sostenido
	_lectura.text = "Tu señal: %.2f Hz   ·   Referencia: %.2f Hz   ·   Tiempo: %d s" % [dial, objetivo, int(LIMITE_S - tiempo)]
	queue_redraw()
	if sostenido >= SOSTENER_S:
		sonar("ok")
		terminar(true, maxf(100.0 - tiempo * 2.0, 10.0), "Las dos ondas quedaron en fase a %.2f Hz." % objetivo)
	elif tiempo >= LIMITE_S:
		var causa := "Tu señal quedó por debajo: gira el dial a la derecha." if dial < objetivo else "Tu señal quedó por encima: gira el dial a la izquierda."
		terminar(false, 0.0, "Se acabó el tiempo. " + causa)
	elif _auto == -1 and tiempo > 3.0:
		terminar(false, 0.0, "Tu señal quedó por debajo de la referencia: gira el dial a la derecha.")


func _gui_input(evento: InputEvent) -> void:
	# raton: arrastrar mueve el dial
	if activo and evento is InputEventMouseMotion and (evento.button_mask & MOUSE_BUTTON_MASK_LEFT) != 0:
		dial = clampf(dial + evento.relative.x * 0.004, 0.2, 3.0)


func _draw() -> void:
	var medio := size.y * 0.5
	var ancho := size.x - 48.0
	draw_rect(Rect2(24, 70, ancho, size.y - 140), Color("1c282e"), true)
	for capa in 2:
		var frecuencia := objetivo if capa == 0 else dial
		var color := Color(Estilo.CREMA, 0.55) if capa == 0 else Estilo.CIAN
		var puntos := PackedVector2Array()
		for i in 160:
			var x := float(i) / 159.0
			puntos.append(Vector2(24.0 + x * ancho, medio + sin(x * TAU * 3.0 * frecuencia + tiempo * 2.0) * 110.0))
		draw_polyline(puntos, color, 3.0 if capa == 1 else 5.0, true)


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1
