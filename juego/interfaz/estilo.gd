extends RefCounted

# Estilo PROVISIONAL de la interfaz: el cuaderno de ingenieria de la Biblia de arte (seccion 6), con la paleta
# maestra. La Fase 7 (UI/UX, tipografia y accesibilidad) no esta validada por Guillermo: colores, fuentes y
# tamanos esperan su veredicto. Las fuentes son las del sistema (no se descargo ninguna).

const PAPEL := Color("f6e7c8")
const PAPEL_SOMBRA := Color("e6d2a8")
const CREMA := Color("f8c991")
const TINTA := Color("322c1d")
const TINTA_SUAVE := Color("6a5d48")
const PETROLEO := Color("516b7c")
const NOCHE := Color("1c282e")
const CIAN := Color("62e4e0")
const CIAN_MEDIO := Color("36b1b2")
const BRILLO := Color("cef8f5")
const CORAL := Color("e46043")
const DORADO := Color("daaa25")
const NARANJA := Color("f4a159")
const TERRACOTA := Color("924930")
const VERDE := Color("6d6a2b")

static var _fuentes: Dictionary = {}
static var _tema: Theme = null


static func fuente(peso: int = 500, mano: bool = false) -> Font:
	# "mano" = letra manuscrita para sellos y notas del cuaderno
	var clave := "%d%s" % [peso, "m" if mano else ""]
	if not _fuentes.has(clave):
		var f := SystemFont.new()
		if mano:
			f.font_names = PackedStringArray(["Segoe Print", "Ink Free", "Comic Sans MS", "Segoe UI"])
		else:
			f.font_names = PackedStringArray(["Bahnschrift", "Segoe UI", "Trebuchet MS", "Verdana"])
		f.font_weight = peso
		_fuentes[clave] = f
	return _fuentes[clave]


static func caja(color: Color, radio: int = 12, borde: int = 0, color_borde: Color = TINTA, margen: int = 14) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = color
	s.set_corner_radius_all(radio)
	s.set_border_width_all(borde)
	s.border_color = color_borde
	s.set_content_margin_all(margen)
	s.anti_aliasing = true
	return s


static func texto(contenido: String, tam: int = 20, color: Color = TINTA, peso: int = 500, mano: bool = false) -> Label:
	var l := Label.new()
	l.text = contenido
	l.add_theme_font_override("font", fuente(peso, mano))
	l.add_theme_font_size_override("font_size", tam)
	l.add_theme_color_override("font_color", color)
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return l


static func linea(contenido: String, tam: int = 20, color: Color = TINTA, peso: int = 500) -> Label:
	# etiqueta de una sola linea (sin salto automatico): para filas, cabeceras y contadores
	var l := texto(contenido, tam, color, peso)
	l.autowrap_mode = TextServer.AUTOWRAP_OFF
	return l


static func boton(contenido: String, tam: int = 22, principal: bool = false) -> Button:
	var b := Button.new()
	b.text = contenido
	b.add_theme_font_override("font", fuente(600))
	b.add_theme_font_size_override("font_size", tam)
	var fondo := CIAN if principal else PAPEL
	b.add_theme_stylebox_override("normal", caja(fondo, 10, 3, TINTA, 12))
	b.add_theme_stylebox_override("hover", caja(fondo.lightened(0.25), 10, 3, TINTA, 12))
	b.add_theme_stylebox_override("pressed", caja(PETROLEO, 10, 3, TINTA, 12))
	b.add_theme_stylebox_override("focus", caja(Color(0, 0, 0, 0), 10, 4, CIAN_MEDIO, 12))
	b.add_theme_stylebox_override("disabled", caja(PAPEL_SOMBRA.darkened(0.1), 10, 2, TINTA_SUAVE, 12))
	for estado in ["font_color", "font_hover_color", "font_focus_color"]:
		b.add_theme_color_override(estado, TINTA)
	b.add_theme_color_override("font_pressed_color", PAPEL)
	b.add_theme_color_override("font_disabled_color", TINTA_SUAVE)
	b.custom_minimum_size = Vector2(0, tam * 2 + 6)
	b.pressed.connect(func(): Audio.sonar("pulsar"))
	return b


static func panel(color: Color = PAPEL, radio: int = 14, borde: int = 3, margen: int = 18) -> PanelContainer:
	var p := PanelContainer.new()
	p.add_theme_stylebox_override("panel", caja(color, radio, borde, TINTA, margen))
	return p


static func tema() -> Theme:
	if _tema == null:
		_tema = Theme.new()
		_tema.default_font = fuente(500)
		_tema.default_font_size = 20
		_tema.set_color("font_color", "Label", TINTA)
	return _tema


static func separador(alto: int = 10) -> Control:
	var c := Control.new()
	c.custom_minimum_size = Vector2(0, alto)
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return c


static func luna(lienzo: CanvasItem, centro: Vector2, radio: float, fase: float, giro: float = 0.0, lado_luz: Color = CREMA, lado_sombra: Color = Color("3b4a52")) -> void:
	# dibuja la Luna con su fase (0 = nueva, 0,5 = llena, 1 = nueva) dentro de _draw() de "lienzo".
	# "giro" en radianes: con PI/2 el borde iluminado queda abajo, la «Luna sonriente» del ecuador.
	lienzo.draw_set_transform(centro, giro, Vector2.ONE)
	lienzo.draw_circle(Vector2.ZERO, radio, lado_sombra)
	var k := cos(TAU * fase)              # 1 en nueva, -1 en llena
	var signo := 1.0 if fase <= 0.5 else -1.0
	var puntos := PackedVector2Array()
	var pasos := 24
	for i in pasos + 1:
		var t := PI * float(i) / float(pasos)
		puntos.append(Vector2(signo * radio * sin(t), -radio * cos(t)))
	for i in pasos + 1:
		var t := PI * float(pasos - i) / float(pasos)
		puntos.append(Vector2(signo * k * radio * sin(t), -radio * cos(t)))
	if absf(k) < 0.999:
		lienzo.draw_colored_polygon(puntos, lado_luz)
	lienzo.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
