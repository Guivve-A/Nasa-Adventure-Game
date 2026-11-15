extends CanvasLayer

# Cuaderno de campo de Marte. Un icono pequeno abajo a la derecha; con clic o Tab se abre en grande.
# Las paginas se ganan haciendo cosas (saltar, desplegar, perforar...). Abierto, pausa el juego.
# Uso: cuaderno.desbloquear("gravedad"). Los textos salen de datos/marte.json ("cuaderno").

signal nueva(id)

const CREMA := Color("f6e8c8")
const PAPEL := Color("f3e3c0")
const PAPEL2 := Color("e9d4ab")
const TINTA := Color("4a3322")
const TINTA2 := Color("7a5a40")
const RAYA := Color("9fb8c9")
const MARGEN := Color("d9826b")
const OXIDO := Color("b5532f")
const ICONO := Rect2(606, 318, 26, 30)
const HOJA := Rect2(120, 52, 400, 252)

var paginas: Array = []          # ids en el orden en que se ganaron
var abierto := false
var actual := 0
var auto_abrir := true           # la primera nota abre el cuaderno una sola vez

var _datos := {}
var _orden: Array = []
var _lienzo: Control
var _fuente: Font
var _t := 0.0
var _brillo := 0.0               # pulso del icono cuando hay nota nueva
var _toast := ""
var _t_toast := 0.0
var _ya_abrio := false
var _sin_leer := 0
var _x_rect := Rect2()


func _ready() -> void:
	layer = 12
	process_mode = Node.PROCESS_MODE_ALWAYS
	var raiz: String = (get_script() as Script).resource_path.get_base_dir().get_base_dir()
	var todo: Dictionary = (load(raiz + "/datos/marte.json") as JSON).data
	_datos = todo["cuaderno"]
	_orden = todo["orden_cuaderno"]
	_fuente = preload("fuente_pixel.gd").obtener()
	_lienzo = Control.new()
	_lienzo.set_anchors_preset(Control.PRESET_FULL_RECT)
	_lienzo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_lienzo.draw.connect(_dibujar)
	add_child(_lienzo)


func total() -> int:
	return _orden.size()


func tiene(id: String) -> bool:
	return paginas.has(id)


func desbloquear(id: String) -> void:
	if paginas.has(id) or not _datos.has(id):
		return
	paginas.append(id)
	# se ordenan como en el cuaderno, no como se ganaron
	paginas.sort_custom(func(a, b): return _orden.find(a) < _orden.find(b))
	_brillo = 1.0
	_sin_leer += 1
	_toast = "Nueva nota: " + String(_datos[id]["titulo"])
	_t_toast = 2.4
	nueva.emit(id)
	if auto_abrir and not _ya_abrio:
		_ya_abrio = true
		get_tree().create_timer(0.6, true).timeout.connect(func(): abrir(id))


func abrir(id := "") -> void:
	if paginas.is_empty():
		return
	abierto = true
	actual = maxi(0, paginas.find(id)) if id != "" else clampi(actual, 0, paginas.size() - 1)
	if id == "" and _sin_leer > 0:
		actual = paginas.size() - 1
	_sin_leer = 0
	_brillo = 0.0
	_pausar(true)


func cerrar() -> void:
	abierto = false
	_pausar(false)


# pausa solo el capitulo (el nodo padre), no todo el arbol: asi funciona igual suelto o dentro del juego principal
func _pausar(si: bool) -> void:
	var nivel := get_parent()
	if nivel != null:
		nivel.process_mode = Node.PROCESS_MODE_DISABLED if si else Node.PROCESS_MODE_INHERIT


func pasar(d: int) -> void:
	actual = clampi(actual + d, 0, paginas.size() - 1)


func _process(delta: float) -> void:
	_t += delta
	_t_toast -= delta
	if _brillo > 0.0 and _sin_leer == 0:
		_brillo = maxf(0.0, _brillo - delta)
	_lienzo.queue_redraw()


func _input(evento: InputEvent) -> void:
	var tecla := evento as InputEventKey
	if tecla != null and tecla.pressed and not tecla.echo:
		if tecla.keycode == KEY_TAB:
			if abierto:
				cerrar()
			else:
				abrir()
			get_viewport().set_input_as_handled()
		elif abierto:
			if tecla.keycode in [KEY_LEFT, KEY_A]:
				pasar(-1)
			elif tecla.keycode in [KEY_RIGHT, KEY_D]:
				pasar(1)
			get_viewport().set_input_as_handled()
	var clic := evento as InputEventMouseButton
	if clic != null and clic.pressed and clic.button_index == MOUSE_BUTTON_LEFT:
		var p: Vector2 = (_lienzo.make_input_local(clic) as InputEventMouseButton).position
		if abierto:
			if _x_rect.has_point(p) or not HOJA.grow(3).has_point(p):
				cerrar()
			elif p.x < HOJA.position.x + 40:
				pasar(-1)
			elif p.x > HOJA.end.x - 40:
				pasar(1)
			get_viewport().set_input_as_handled()
		elif ICONO.grow(4).has_point(p) and not paginas.is_empty():
			abrir()
			get_viewport().set_input_as_handled()


# ---------- dibujo ----------
func _txt(pos: Vector2, s: String, color: Color, tam := 8, ancho := -1.0, alin := HORIZONTAL_ALIGNMENT_LEFT) -> void:
	_lienzo.draw_string(_fuente, pos, s, alin, ancho, tam, color)


func _dibujar() -> void:
	var c := _lienzo
	if paginas.is_empty():
		return
	# icono: libreta con espiral y una estrella de nota nueva
	var r := ICONO
	var sube := sin(_t * 6.0) * 1.5 * _brillo
	r.position.y -= sube
	c.draw_rect(Rect2(r.position + Vector2(2, 2), r.size), Color(0, 0, 0, 0.45))
	c.draw_rect(r, OXIDO)
	c.draw_rect(Rect2(r.position + Vector2(4, 2), r.size - Vector2(6, 4)), PAPEL)
	for k in 5:
		c.draw_rect(Rect2(r.position + Vector2(1, 4 + k * 5), Vector2(5, 2)), Color("3d4252"))
	for k in 4:
		c.draw_rect(Rect2(r.position + Vector2(9, 8 + k * 5), Vector2(13 - (k % 2) * 4, 1)), RAYA)
	if _sin_leer > 0:
		var pulso := 0.6 + 0.4 * sin(_t * 8.0)
		c.draw_circle(r.position + Vector2(r.size.x - 1, 1), 5.0, Color("f2b134", pulso))
		_txt(r.position + Vector2(r.size.x - 4, 4), str(_sin_leer), TINTA, 7)
	if _t_toast > 0.0 and not abierto:
		var w := _fuente.get_string_size(_toast, HORIZONTAL_ALIGNMENT_LEFT, -1, 7).x + 12.0
		var a := clampf(_t_toast * 2.0, 0.0, 1.0)
		var tr := Rect2(600 - w, 324, w, 13)
		c.draw_rect(tr, Color(PAPEL, a))
		c.draw_rect(tr, Color(OXIDO, a), false, 1.0)
		_txt(tr.position + Vector2(6, 10), _toast, Color(TINTA, a), 7)
	if not abierto:
		return
	# hoja abierta
	c.draw_rect(Rect2(0, 0, 640, 360), Color(0.03, 0.03, 0.06, 0.55))
	var h := HOJA
	c.draw_rect(Rect2(h.position + Vector2(4, 4), h.size), Color(0, 0, 0, 0.5))
	c.draw_rect(h.grow(3), OXIDO)
	c.draw_rect(h, PAPEL)
	for y in range(int(h.position.y) + 34, int(h.end.y) - 8, 12):
		c.draw_line(Vector2(h.position.x + 22, y), Vector2(h.end.x - 6, y), Color(RAYA, 0.55), 1.0)
	c.draw_line(Vector2(h.position.x + 30, h.position.y + 4), Vector2(h.position.x + 30, h.end.y - 4), Color(MARGEN, 0.7), 1.0)
	for k in 13:
		var y2 := h.position.y + 10 + k * 18.5
		c.draw_rect(Rect2(h.position.x - 6, y2, 14, 4), Color("3d4252"))
		c.draw_rect(Rect2(h.position.x - 6, y2, 14, 1), Color("a9adb8"))
	var id: String = paginas[actual]
	var d: Dictionary = _datos[id]
	var x0 := h.position.x + 38
	_txt(Vector2(x0, h.position.y + 22), String(d["titulo"]), TINTA, 16)
	_txt(Vector2(h.end.x - 172, h.position.y + 16), "Cuaderno de campo", TINTA2, 6, 150, HORIZONTAL_ALIGNMENT_RIGHT)
	# dibujo de la pagina, arriba a la derecha
	var caja := Rect2(h.end.x - 104, h.position.y + 28, 92, 70)
	c.draw_rect(caja, PAPEL2)
	c.draw_rect(caja, Color(TINTA2, 0.6), false, 1.0)
	_ilustrar(id, caja)
	c.draw_multiline_string(_fuente, Vector2(x0, h.position.y + 44), String(d["texto"]), HORIZONTAL_ALIGNMENT_LEFT, caja.position.x - x0 - 8, 8, 8, TINTA, TextServer.BREAK_MANDATORY | TextServer.BREAK_WORD_BOUND)
	# dato real, como una nota pegada
	var nota := Rect2(x0 - 4, h.position.y + 140, h.end.x - x0 - 8, 76)
	c.draw_rect(nota, Color("fff3c4"))
	c.draw_rect(Rect2(nota.position.x + nota.size.x * 0.5 - 18, nota.position.y - 4, 36, 8), Color(0.85, 0.85, 0.75, 0.7))
	_txt(nota.position + Vector2(6, 12), "Dato real", OXIDO, 8)
	c.draw_multiline_string(_fuente, nota.position + Vector2(6, 25), String(d["dato"]), HORIZONTAL_ALIGNMENT_LEFT, nota.size.x - 12, 8, 4, TINTA, TextServer.BREAK_MANDATORY | TextServer.BREAK_WORD_BOUND)
	_txt(nota.position + Vector2(6, nota.size.y - 5), "Fuente: " + String(d["fuente"]), TINTA2, 6)
	# pie de pagina
	var pie := "%d / %d" % [actual + 1, paginas.size()]
	_txt(Vector2(h.position.x, h.end.y - 6), pie, TINTA2, 7, h.size.x, HORIZONTAL_ALIGNMENT_CENTER)
	if actual > 0:
		_flecha(Vector2(h.position.x + 46, h.end.y - 9), -1)
	if actual < paginas.size() - 1:
		_flecha(Vector2(h.end.x - 46, h.end.y - 9), 1)
	_txt(Vector2(h.end.x - 120, h.end.y - 6), "Tab: cerrar", TINTA2, 6, 110, HORIZONTAL_ALIGNMENT_RIGHT)
	_x_rect = preload("aterrizaje.gd").boton_x(c, Vector2(h.end.x - 8, h.position.y - 8), OXIDO)


func _flecha(p: Vector2, d: int) -> void:
	var pts := PackedVector2Array([p + Vector2(d * 5, 0), p + Vector2(-d * 3, -4), p + Vector2(-d * 3, 4)])
	_lienzo.draw_colored_polygon(pts, OXIDO)


# pequenos dibujos a lapiz para cada pagina (todo con formas simples)
func _ilustrar(id: String, r: Rect2) -> void:
	var c := _lienzo
	var o := r.position
	var cx := r.get_center()
	var piso := o.y + r.size.y - 12
	match id:
		"senal":
			c.draw_circle(o + Vector2(16, 36), 9, Color("3f86a8"))
			c.draw_circle(o + Vector2(14, 33), 3, Color("8fd46a"))
			c.draw_circle(o + Vector2(78, 36), 7, Color("c9653a"))
			for k in 7:
				var x := o.x + 28 + k * 6.5
				c.draw_line(Vector2(x, o.y + 36 + (2 if k % 2 else -2)), Vector2(x + 4, o.y + 36 + (-2 if k % 2 else 2)), TINTA, 1.0)
			_txt(o + Vector2(24, 60), "4 – 24 min", TINTA2, 7)
		"siete":
			c.draw_arc(cx + Vector2(0, -6), 22, PI, TAU, 16, MARGEN, 5.0)
			for k in 5:
				c.draw_line(cx + Vector2(-22 + k * 11, -6), cx + Vector2(-3 + k * 1.5, 18), TINTA2, 1.0)
			c.draw_rect(Rect2(cx + Vector2(-5, 16), Vector2(10, 12)), Color("f6f1e4"))
			c.draw_rect(Rect2(cx + Vector2(-5, 16), Vector2(10, 12)), TINTA, false, 1.0)
		"gravedad":
			c.draw_line(Vector2(o.x + 6, piso), Vector2(r.end.x - 6, piso), TINTA2, 1.0)
			var prev := Vector2.ZERO
			for k in 13:
				var t := k / 12.0
				var p := Vector2(o.x + 14 + t * 64, piso - 44 * 4.0 * t * (1.0 - t))
				if k > 0:
					c.draw_dashed_line(prev, p, TINTA2, 1.0, 2.0)
				prev = p
			c.draw_rect(Rect2(cx + Vector2(-4, -36), Vector2(8, 10)), Color("f6f1e4"))
			c.draw_rect(Rect2(cx + Vector2(-4, -36), Vector2(8, 10)), TINTA, false, 1.0)
			_txt(o + Vector2(58, 14), "0,38 g", OXIDO, 8)
		"sol":
			c.draw_arc(Vector2(cx.x, piso), 34, PI, TAU, 24, TINTA2, 1.0)
			c.draw_circle(Vector2(cx.x - 24, piso - 24), 6, Color("f2b134"))
			c.draw_line(Vector2(o.x + 6, piso), Vector2(r.end.x - 6, piso), TINTA2, 1.0)
			_txt(o + Vector2(20, r.size.y - 2), "24 h 39 min", TINTA, 7)
		"aire":
			for k in 4:
				var p := o + Vector2(18 + (k % 2) * 40, 18 + (k / 2) * 28)
				c.draw_circle(p, 5, Color("6a6f7d"))
				c.draw_circle(p + Vector2(-9, 0), 4, Color("d9826b"))
				c.draw_circle(p + Vector2(9, 0), 4, Color("d9826b"))
			_txt(o + Vector2(30, 64), "CO₂", TINTA, 8)
		"moxie":
			c.draw_rect(Rect2(cx + Vector2(-20, -16), Vector2(40, 30)), Color("d39528"))
			for k in 6:
				c.draw_line(cx + Vector2(-20, -12 + k * 5), cx + Vector2(20, -12 + k * 5), Color("f6d277"), 1.0)
			c.draw_rect(Rect2(cx + Vector2(-20, -16), Vector2(40, 30)), TINTA, false, 1.0)
			_txt(o + Vector2(18, r.size.y - 4), "CO₂ → O₂", TINTA, 7)
		"hielo":
			c.draw_rect(Rect2(o + Vector2(4, 18), Vector2(r.size.x - 8, 14)), Color("c9653a"))
			c.draw_rect(Rect2(o + Vector2(4, 32), Vector2(r.size.x - 8, 20)), Color("a8e4f0"))
			c.draw_rect(Rect2(o + Vector2(4, 52), Vector2(r.size.x - 8, 10)), Color("8f4a2c"))
			c.draw_line(o + Vector2(46, 8), o + Vector2(46, 44), TINTA, 2.0)
			_txt(o + Vector2(52, 30), "2,5 cm", TINTA, 7)
		"polvo":
			c.draw_rect(Rect2(cx + Vector2(-26, 4), Vector2(36, 14)), Color("2f62c4"))
			for k in 40:
				var p := o + Vector2(fposmod(k * 37.0 + _t * 30.0, r.size.x), 6 + (k * 13) % 46)
				c.draw_rect(Rect2(p, Vector2(2, 1)), Color("c9653a", 0.8))
			c.draw_rect(Rect2(cx + Vector2(-26, 4), Vector2(36, 5)), Color("c99a6b", 0.9))
		"frio":
			c.draw_rect(Rect2(cx + Vector2(-3, -26), Vector2(6, 38)), Color("f6f1e4"))
			c.draw_rect(Rect2(cx + Vector2(-3, -26), Vector2(6, 38)), TINTA, false, 1.0)
			c.draw_circle(cx + Vector2(0, 16), 6, Color("62a8e4"))
			c.draw_rect(Rect2(cx + Vector2(-1, 0), Vector2(2, 14)), Color("62a8e4"))
			_txt(cx + Vector2(8, -18), "−31 °C", TINTA2, 7)
			_txt(cx + Vector2(8, 10), "−89 °C", TINTA, 7)
		"lunas":
			c.draw_rect(r.grow(-1), Color("1b1b3d"))
			c.draw_circle(cx + Vector2(-12, -4), 14, Color("b0806a"))
			c.draw_circle(cx + Vector2(-16, -8), 4, Color("8c5048"))
			c.draw_circle(cx + Vector2(26, -18), 4, Color("c9a891"))
			_txt(o + Vector2(6, r.size.y - 4), "Fobos", CREMA, 7)
			_txt(o + Vector2(44, 38), "Deimos", CREMA, 6)
		"unidades":
			c.draw_rect(Rect2(o + Vector2(6, 20), Vector2(r.size.x - 12, 14)), Color("f2b134"))
			for k in 16:
				c.draw_line(o + Vector2(10 + k * 5, 20), o + Vector2(10 + k * 5, 24 + (k % 2) * 4), TINTA, 1.0)
			_txt(o + Vector2(8, 50), "lbf·s ≠ N·s", OXIDO, 9)
