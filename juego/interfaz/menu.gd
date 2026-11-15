extends Control

# Menu principal: nueva partida, continuar, minijuegos (galeria para jugarlos sueltos), lugares (para visitar
# y validar cada escenario) y salir. Estilo y titulo PROVISIONALES: «Luz cenicienta» es el nombre de trabajo
# del capitulo en el borrador de la Fase 2, sin aprobar; el titulo comercial no puede llevar «NASA».

signal elegido(accion: String, dato: String)

const Estilo := preload("res://interfaz/estilo.gd")

var _columna: VBoxContainer
var _fase := 0.12


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var fondo := ColorRect.new()
	fondo.color = Estilo.NOCHE
	fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fondo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fondo)
	var cielo := Control.new()
	cielo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	cielo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cielo.draw.connect(func(): _dibujar_cielo(cielo))
	add_child(cielo)
	_columna = VBoxContainer.new()
	_columna.add_theme_constant_override("separation", 10)
	_columna.position = Vector2(90, 70)
	add_child(_columna)
	var pie := Estilo.texto("Prototipo jugable v0 · arte y textos en validación · datos espaciales reales con su fuente", 14, Estilo.PETROLEO, 500)
	pie.autowrap_mode = TextServer.AUTOWRAP_OFF
	pie.position = Vector2(90, 680)
	add_child(pie)


func _dibujar_cielo(lienzo: Control) -> void:
	# estrellas fijas y la «Luna sonriente» del 12-11-2026 vista desde Guayaquil: 12,2 % iluminada
	var semilla := 7
	for i in 90:
		semilla = (semilla * 1103515245 + 12345) & 0x7fffffff
		var x := float(semilla % 1280)
		semilla = (semilla * 1103515245 + 12345) & 0x7fffffff
		var y := float(semilla % 720)
		semilla = (semilla * 1103515245 + 12345) & 0x7fffffff
		var brillo := 0.25 + float(semilla % 100) / 160.0
		lienzo.draw_circle(Vector2(x, y), 1.0 + float(semilla % 3) * 0.5, Color(Estilo.BRILLO, brillo))
	Estilo.luna(lienzo, Vector2(930, 300), 150.0, _fase, PI * 0.5 + 0.22, Estilo.CREMA, Color("2b3b44"))


func _titulo(texto: String, sub: String) -> void:
	for hijo in _columna.get_children():
		_columna.remove_child(hijo)
		hijo.queue_free()
	var t := Estilo.texto(texto, 62, Estilo.CREMA, 700)
	t.autowrap_mode = TextServer.AUTOWRAP_OFF
	_columna.add_child(t)
	var s := Estilo.texto(sub, 21, Estilo.CIAN, 500)
	s.custom_minimum_size = Vector2(560, 0)
	_columna.add_child(s)
	_columna.add_child(Estilo.separador(14))


func _boton(texto: String, accion: String, dato: String = "", principal: bool = false, detalle: String = "") -> Button:
	var b := Estilo.boton(texto, 23, principal)
	b.custom_minimum_size = Vector2(430, 50)
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.pressed.connect(func(): elegido.emit(accion, dato))
	if detalle != "":
		b.tooltip_text = detalle
	_columna.add_child(b)
	return b


func abrir() -> void:
	visible = true
	mostrar_inicio()


func cerrar() -> void:
	visible = false


func mostrar_inicio() -> void:
	_titulo("Luz cenicienta", "Una estudiante de ingeniería de control de Guayaquil, su gato Órbita y la Luna de esta noche.")
	var primero: Button = null
	if Juego.hay_partida():
		primero = _boton("Continuar", "continuar", "", true)
		_boton("Nueva partida", "nueva")
	else:
		primero = _boton("Nueva partida", "nueva", "", true)
	_boton("Mapa del mundo", "mapa")
	_boton("Minijuegos", "minijuegos")
	_boton("Lugares", "lugares")
	_boton("Salir", "salir")
	primero.grab_focus.call_deferred()


func mostrar_minijuegos() -> void:
	_titulo("Minijuegos", "Cada reto enseña un dato espacial real o una idea de control. Aquí se juegan sueltos.")
	var primero: Button = null
	var cuadricula := GridContainer.new()
	cuadricula.columns = 2
	cuadricula.add_theme_constant_override("h_separation", 10)
	cuadricula.add_theme_constant_override("v_separation", 8)
	_columna.add_child(cuadricula)
	for m in Juego.catalogo_minijuegos():
		if m.get("oculto", false):
			continue
		var hecho: Dictionary = Juego.estado["minijuegos"].get(m["id"], {})
		var marca := "✓ " if hecho.get("superado", false) else ""
		var b := Estilo.boton(marca + String(m.get("titulo", m["id"])), 20)
		b.custom_minimum_size = Vector2(330, 46)
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.tooltip_text = m.get("resumen", "")
		var id_mj: String = m["id"]
		var zona_mj: String = m.get("zona", "")
		if zona_mj != "":
			b.pressed.connect(func(): elegido.emit("lugar", zona_mj))
		else:
			b.pressed.connect(func(): elegido.emit("minijuego", id_mj))
		cuadricula.add_child(b)
		if primero == null:
			primero = b
	var volver := _boton("Volver", "inicio")
	(primero if primero != null else volver).grab_focus.call_deferred()


func mostrar_lugares() -> void:
	_titulo("Lugares", "Visita cada escenario por separado. Los marcados como provisionales esperan la validación del arte.")
	var primero: Button = null
	for z in Zonas.catalogo():
		var provisional: bool = String(z.get("estado_arte", "")).begins_with("provisional")
		var texto := String(z.get("nombre", z["id"])) + ("  (provisional)" if provisional else "")
		var b := _boton(texto, "lugar", z["id"])
		if primero == null:
			primero = b
	var volver := _boton("Volver", "inicio")
	(primero if primero != null else volver).grab_focus.call_deferred()
