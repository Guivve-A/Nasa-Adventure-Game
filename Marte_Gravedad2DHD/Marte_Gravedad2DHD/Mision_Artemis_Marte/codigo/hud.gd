extends CanvasLayer

# Interfaz comun a los tres capitulos: marco de pagina, medidores, objetivo, avisos, alerta, burbuja, dialogo y panel.
# El nivel rellena estas variables en cada cuadro; aqui solo se dibuja. Todo va en unidades de 640 x 360.

const CREMA := Color("f6e8c8")
const TINTA_CAFE := Color("4a3322")
const FONDO := Color(0.043, 0.055, 0.102, 0.8)
const BORDE := Color("33405e")
const BLANCO := Color("f2efe6")
const SUAVE := Color("aeb6c8")
const VACIO := Color("232a40")
const COLORES := {"oxigeno": Color("62e4e0"), "energia": Color("f2b134"), "alimentos": Color("8fd46a"), "radiacion": Color("e0559a"), "alerta": Color("f08a5d")}
const ICONOS := {
	"oxigeno": ["..#....", "..#....", ".###...", ".###...", "#####..", "#####..", ".###..."],
	"energia": ["...##..", "..##...", ".##....", "#####..", "..##...", ".##....", "##....."],
	"alimentos": ["..#.#..", ".#####.", ".#####.", "..###..", "...#...", "...#...", "..###.."],
	"radiacion": ["#..#..#", ".#.#.#.", "..###..", "#######", "..###..", ".#.#.#.", "#..#..#"],
}

var capitulo := ""
var barras: Array = []        # [[clave, nombre, valor 0..1, en_alerta]]
var objetivo := {}            # {titulo, lineas: [..], cuadros: [hechos, total]}
var mochila := ""             # linea bajo los medidores
var aviso := ""               # mensaje corto arriba, al centro
var alerta := {}              # {titulo, texto}: franja grande (lluvia solar)
var burbuja := {}             # {texto, pos, color}: accion disponible, sobre el objeto
var dialogo := {}             # {nombre, texto}
var panel := {}               # {titulo, lineas: [..]}: panel central (final)
var lluvia := 0.0             # 0..1: intensidad de la lluvia solar
var pie := ""                 # controles, abajo a la izquierda
var progreso := -1.0          # 0..1: barra bajo la burbuja (extraer, orientar, desplegar)

var _lienzo: Control
var _fuente: Font
var _t := 0.0


func _ready() -> void:
	layer = 10
	_fuente = ThemeDB.fallback_font
	_lienzo = Control.new()
	_lienzo.set_anchors_preset(Control.PRESET_FULL_RECT)
	_lienzo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_lienzo.draw.connect(_dibujar)
	add_child(_lienzo)


func _process(delta: float) -> void:
	_t += delta
	_lienzo.queue_redraw()


func _txt(pos: Vector2, s: String, color: Color, tam := 8, ancho := -1.0, alin := HORIZONTAL_ALIGNMENT_LEFT) -> void:
	_lienzo.draw_string(_fuente, pos + Vector2(0.5, 0.5), s, alin, ancho, tam, Color(0, 0, 0, 0.7))
	_lienzo.draw_string(_fuente, pos, s, alin, ancho, tam, color)


func _caja(r: Rect2, borde: Color, fondo := FONDO) -> void:
	_lienzo.draw_rect(r, fondo)
	_lienzo.draw_rect(r, borde, false, 1.0)


func _icono(clave: String, pos: Vector2, color: Color) -> void:
	var filas: Array = ICONOS[clave]
	for j in filas.size():
		for i in 7:
			if filas[j][i] == "#":
				_lienzo.draw_rect(Rect2(pos + Vector2(i, j), Vector2.ONE), color)


func _dibujar() -> void:
	var c := _lienzo
	# lluvia solar: tinte y trazos que cruzan la pantalla desde el Sol (arriba a la izquierda)
	if lluvia > 0.0:
		c.draw_rect(Rect2(0, 0, 640, 360), Color(0.88, 0.33, 0.6, 0.1 * lluvia))
		for i in 90:
			var x := fposmod(float((i * 7919) % 700) + _t * 240.0, 700.0) - 40.0
			var y := fposmod(float((i * 4391) % 330) + _t * 80.0, 330.0)
			var l := 5.0 + float((i * 31) % 12)
			c.draw_line(Vector2(x, y), Vector2(x + l, y + l * 0.33), (Color("ffa6cf") if i % 2 == 0 else Color("f08a5d")) * Color(1, 1, 1, 0.75 * lluvia), 1.0)
	# marco de pagina y cinta del capitulo
	c.draw_rect(Rect2(0.5, 0.5, 639, 359), CREMA, false, 2.0)
	if capitulo != "":
		var w := _fuente.get_string_size(capitulo, HORIZONTAL_ALIGNMENT_LEFT, -1, 8).x + 14.0
		c.draw_rect(Rect2(320 - w * 0.5, 0, w, 12), CREMA)
		c.draw_string(_fuente, Vector2(320 - w * 0.5, 9), capitulo, HORIZONTAL_ALIGNMENT_CENTER, w, 8, TINTA_CAFE)
	# medidores
	if not barras.is_empty():
		_caja(Rect2(6, 6, 132, 8 + barras.size() * 10 + (10 if mochila != "" else 0)), BORDE)
		for k in barras.size():
			var b: Array = barras[k]
			var col: Color = COLORES[b[0]]
			var y := 10.0 + k * 10.0
			var parpadeo: bool = b[3] and fmod(_t, 0.6) < 0.3
			_icono(b[0], Vector2(10, y), col)
			_txt(Vector2(21, y + 7), b[1], COLORES["alerta"] if b[3] else BLANCO, 7)
			var llenos := int(round(clampf(b[2], 0.0, 1.0) * 13.0))
			for s in 13:
				c.draw_rect(Rect2(66 + s * 4, y + 1, 3, 5), (Color.WHITE if parpadeo else col) if s < llenos else VACIO)
			_txt(Vector2(119, y + 7), "%d%%" % int(round(b[2] * 100.0)), SUAVE, 6)
		if mochila != "":
			_txt(Vector2(10, 17 + barras.size() * 10), mochila, SUAVE, 6)
	# objetivo
	if not objetivo.is_empty():
		var lineas: Array = objetivo.get("lineas", [])
		var alto := 22.0 + lineas.size() * 9.0 + (10.0 if objetivo.has("cuadros") else 0.0)
		_caja(Rect2(446, 6, 188, alto), BORDE)
		_txt(Vector2(452, 16), objetivo.get("titulo", ""), COLORES["oxigeno"], 8)
		var y2 := 27.0
		if objetivo.has("cuadros"):
			var q: Array = objetivo["cuadros"]
			for k in int(q[1]):
				c.draw_rect(Rect2(452 + k * 12, 20, 10, 6), COLORES["energia"] if k < int(q[0]) else VACIO)
			y2 = 37.0
		for k in lineas.size():
			_txt(Vector2(452, y2 + k * 9.0), lineas[k], BLANCO if k == 0 else SUAVE, 7)
	# alerta grande
	if not alerta.is_empty():
		var col2: Color = COLORES["radiacion"]
		_caja(Rect2(196, 22, 248, 26), col2)
		_icono("radiacion", Vector2(204, 26), Color("ffa6cf"))
		_icono("radiacion", Vector2(429, 26), Color("ffa6cf"))
		_txt(Vector2(196, 34), alerta.get("titulo", ""), Color("ffa6cf") if fmod(_t, 0.5) < 0.3 else BLANCO, 10, 248, HORIZONTAL_ALIGNMENT_CENTER)
		_txt(Vector2(196, 44), alerta.get("texto", ""), BLANCO, 7, 248, HORIZONTAL_ALIGNMENT_CENTER)
	elif aviso != "" and dialogo.is_empty():
		# debajo de los paneles de arriba, para no tapar los medidores ni el objetivo
		var wa := _fuente.get_string_size(aviso, HORIZONTAL_ALIGNMENT_LEFT, -1, 8).x + 16.0
		_caja(Rect2(320 - wa * 0.5, 68, wa, 14), COLORES["energia"])
		_txt(Vector2(320 - wa * 0.5, 78), aviso, BLANCO, 8, wa, HORIZONTAL_ALIGNMENT_CENTER)
	# burbuja de accion
	if not burbuja.is_empty() and dialogo.is_empty():
		var s2: String = burbuja["texto"]
		var wb := _fuente.get_string_size(s2, HORIZONTAL_ALIGNMENT_LEFT, -1, 7).x + 10.0
		var p: Vector2 = burbuja["pos"]
		p.x = clampf(p.x, wb * 0.5 + 4, 636 - wb * 0.5)
		p.y = maxf(p.y, 60.0)
		var col3: Color = burbuja.get("color", COLORES["oxigeno"])
		_caja(Rect2(p.x - wb * 0.5, p.y - 12, wb, 12), col3)
		_txt(Vector2(p.x - wb * 0.5, p.y - 3), s2, col3, 7, wb, HORIZONTAL_ALIGNMENT_CENTER)
		if progreso >= 0.0:
			c.draw_rect(Rect2(p.x - wb * 0.5, p.y + 1, wb, 3), VACIO)
			c.draw_rect(Rect2(p.x - wb * 0.5, p.y + 1, wb * clampf(progreso, 0.0, 1.0), 3), COLORES["energia"])
	# dialogo
	if not dialogo.is_empty():
		# arriba, bajo los paneles: asi no tapa a quien habla
		_caja(Rect2(70, 68, 500, 54), COLORES["oxigeno"], Color(0.043, 0.055, 0.102, 0.93))
		_txt(Vector2(78, 80), dialogo.get("nombre", ""), COLORES["oxigeno"], 8)
		_txt(Vector2(492, 80), "E: seguir", SUAVE, 7, 70, HORIZONTAL_ALIGNMENT_RIGHT)
		c.draw_multiline_string(_fuente, Vector2(78, 93), dialogo.get("texto", ""), HORIZONTAL_ALIGNMENT_LEFT, 484, 8, 3, BLANCO)
	if pie != "":
		_txt(Vector2(8, 353), pie, SUAVE, 6)
	# panel central
	if not panel.is_empty():
		var pl: Array = panel.get("lineas", [])
		var ap := 40.0 + pl.size() * 11.0
		_caja(Rect2(140, 180 - ap * 0.5, 360, ap), CREMA, Color(0.043, 0.055, 0.102, 0.94))
		_txt(Vector2(140, 180 - ap * 0.5 + 20), panel.get("titulo", ""), CREMA, 12, 360, HORIZONTAL_ALIGNMENT_CENTER)
		for k in pl.size():
			_txt(Vector2(150, 180 - ap * 0.5 + 38 + k * 11.0), pl[k], BLANCO, 8, 340, HORIZONTAL_ALIGNMENT_CENTER)
