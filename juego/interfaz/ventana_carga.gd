extends Control

# Ventana de carga «lamina en el cuaderno de campo» (lote 08). La ilustracion del destino es una lamina
# pintada a la acuarela y gouache, pegada con cinta en una hoja cuadriculada del cuaderno de ingenieria de
# la protagonista. Alrededor, a tinta: el nombre del lugar con su trazo, el tramo del viaje dibujado como un
# itinerario, la mision en curso con su casilla, la ficha del cuaderno con su fuente y su sello, y el
# indicador de carga: una fila de lunas que se van entintando fase a fase.
# Pedidos de Guillermo (2026-11-14): pantallas con presencia, «en version NASA space», y despues «se ven
# mucho IA-like. Se original. Genera disenos mas como Bravely». Direccion en
# Nasa_Game/Fase_1_Arte/Exploracion/Lote_08/Lote 08 - Carga pintada.md. Estilo provisional (Fase 7 sin validar).
#
# zona.json -> "carga": {"imagen": "res://zonas/<id>/carga.jpg", "fichas": ["id_de_ficha", ...]}
# La lamina propia del lugar (res://interfaz/arte/carga_<id>.jpg) manda sobre la imagen de la zona.

const Estilo := preload("res://interfaz/estilo.gd")
const Recursos := preload("res://nucleo/recursos.gd")

# geometria de la pagina, pensada para 1280 x 720
const LAMINA := Rect2(66, 42, 842, 474)        # rectangulo de la lamina (con su margen de papel)
const MARGEN_LAMINA := 9.0                      # margen blanco de la lamina impresa
const GIRO_LAMINA := -0.012                     # radianes: la lamina esta pegada un poco torcida
const COLUMNA_X := 944.0                        # columna de notas a la derecha
const COLUMNA_ANCHO := 290.0
const CUADRICULA := 26.0
const PAPEL_LAMINA := Color("fbf3e1")
const CINTA := Color(0.93, 0.87, 0.72, 0.82)

var _papel: Control
var _lamina: Control
var _tinta: Control
var _textura: Texture2D = null
var _con_arte := false

var _encabezado_tramo: Label
var _origen: Label
var _destino: Label
var _nombre: Label
var _detalle: Label
var _estado: Label
var _encabezado_mision: Label
var _mision: Label
var _objetivo: Label
var _cuaderno: Label
var _titulo: Label
var _texto: Label
var _fuente: Label
var _cargando: Label
var _sello := ""
var _con_origen := false

var _t := 0.0
var _avance := 0.0
var _entrada := 1.0
var _ultima_ficha := ""


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	modulate.a = 0.0
	clip_contents = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	_papel = _lienzo(_dibujar_papel)
	_vineta()
	_lamina = Control.new()
	_lamina.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_lamina.position = LAMINA.position
	_lamina.size = LAMINA.size
	_lamina.pivot_offset = LAMINA.size * 0.5
	_lamina.rotation = GIRO_LAMINA
	_lamina.draw.connect(_dibujar_lamina)
	add_child(_lamina)
	_tinta = _lienzo(_dibujar_tinta)

	var espaciada := FontVariation.new()
	espaciada.base_font = Estilo.fuente(700)
	espaciada.spacing_glyph = 2
	_encabezado_tramo = _rotulo("DE CAMINO", 13, Estilo.TINTA_SUAVE, espaciada)
	_origen = _rotulo("", 17, Estilo.TINTA_SUAVE, Estilo.fuente(500))
	_destino = _rotulo("", 18, Estilo.TINTA, Estilo.fuente(700))
	_nombre = _rotulo("", 42, Estilo.TINTA, Estilo.fuente(700, true))
	_detalle = _rotulo("", 19, Estilo.TINTA_SUAVE, Estilo.fuente(500))
	_estado = _rotulo("", 16, Estilo.TERRACOTA, Estilo.fuente(500, true))
	_encabezado_mision = _rotulo("MISIÓN EN CURSO", 13, Estilo.TINTA_SUAVE, espaciada)
	_mision = _rotulo("", 19, Estilo.TINTA, Estilo.fuente(700, true), true)
	_objetivo = _rotulo("", 17, Estilo.TINTA, Estilo.fuente(500), true)
	_cuaderno = _rotulo("DEL CUADERNO", 13, Estilo.TINTA_SUAVE, espaciada)
	_titulo = _rotulo("", 21, Estilo.TINTA, Estilo.fuente(700), true)
	_texto = _rotulo("", 18, Estilo.TINTA, Estilo.fuente(500), true)
	_fuente = _rotulo("", 14, Estilo.TINTA_SUAVE, Estilo.fuente(500), true)
	_cargando = _rotulo("cargando", 15, Estilo.TINTA_SUAVE, Estilo.fuente(500, true))
	for l in [_mision, _objetivo, _titulo, _texto, _fuente]:
		l.custom_minimum_size = Vector2(COLUMNA_ANCHO - 26.0, 0)
	_mision.custom_minimum_size.x = COLUMNA_ANCHO
	_titulo.custom_minimum_size.x = COLUMNA_ANCHO
	_texto.custom_minimum_size.x = COLUMNA_ANCHO
	_fuente.custom_minimum_size.x = COLUMNA_ANCHO


func _lienzo(dibujo: Callable) -> Control:
	var c := Control.new()
	c.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.draw.connect(dibujo)
	add_child(c)
	return c


func _vineta() -> void:
	# el papel se oscurece un poco hacia los bordes, como una hoja bajo una lampara
	var degradado := Gradient.new()
	degradado.offsets = PackedFloat32Array([0.0, 0.55, 1.0])
	var sombra := Estilo.PAPEL_SOMBRA.darkened(0.25)
	degradado.colors = PackedColorArray([Color(sombra, 0.0), Color(sombra, 0.05), Color(sombra, 0.34)])
	var textura := GradientTexture2D.new()
	textura.gradient = degradado
	textura.fill = GradientTexture2D.FILL_RADIAL
	textura.fill_from = Vector2(0.5, 0.5)
	textura.fill_to = Vector2(1.08, 1.08)
	textura.width = 128
	textura.height = 72
	var r := TextureRect.new()
	r.texture = textura
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.stretch_mode = TextureRect.STRETCH_SCALE
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	r.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(r)


func _rotulo(contenido: String, tam: int, color: Color, fuente: Font, envolver: bool = false) -> Label:
	var l := Estilo.texto(contenido, tam, color) if envolver else Estilo.linea(contenido, tam, color)
	l.add_theme_font_override("font", fuente)
	add_child(l)
	return l


func _process(delta: float) -> void:
	if not visible:
		return
	_t += delta
	_avance = fmod(_avance + delta * 0.45, 1.0)
	# la lamina se asienta sobre la hoja al aparecer
	_lamina.position = LAMINA.position + Vector2(0, 10.0 * (1.0 - _entrada))
	_lamina.rotation = GIRO_LAMINA - 0.01 * (1.0 - _entrada)
	_colocar()
	_lamina.queue_redraw()
	_tinta.queue_redraw()


func _colocar() -> void:
	# las etiquetas con salto de linea informan al principio una altura enorme: se recalcula cada cuadro
	for l: Label in [_mision, _objetivo, _titulo, _texto, _fuente]:
		l.reset_size()
	# rotulos de la izquierda: bajo la lamina
	var x0 := LAMINA.position.x + 10.0
	var y0 := LAMINA.end.y + 18.0
	_nombre.position = Vector2(x0, y0 - 6.0)
	_detalle.position = Vector2(x0 + 2.0, _nombre.position.y + _nombre.size.y + 2.0)
	_estado.position = Vector2(x0 + 2.0, _detalle.position.y + _detalle.size.y + 8.0)
	# columna de notas
	var cx := COLUMNA_X
	var y := 50.0
	_encabezado_tramo.position = Vector2(cx, y)
	y += 30.0
	if _con_origen:
		_origen.position = Vector2(cx + 30.0, y - _origen.size.y * 0.5)
		y += 46.0
	_destino.position = Vector2(cx + 30.0, y - _destino.size.y * 0.5)
	y += 40.0
	if _mision.text != "":
		_encabezado_mision.position = Vector2(cx, y)
		_mision.position = Vector2(cx, y + 20.0)
		_objetivo.position = Vector2(cx + 26.0, _mision.position.y + _mision.size.y + 4.0)
		y = _objetivo.position.y + _objetivo.size.y + 22.0
	_cuaderno.position = Vector2(cx, y)
	_titulo.position = Vector2(cx, y + 20.0)
	_texto.position = Vector2(cx, _titulo.position.y + _titulo.size.y + 4.0)
	_fuente.position = Vector2(cx, _texto.position.y + _texto.size.y + 6.0)
	_cargando.position = Vector2(cx, size.y - 62.0)


# ------------------------------------------------------------------ dibujo

func _dibujar_papel() -> void:
	var tam := size
	_papel.draw_rect(Rect2(Vector2.ZERO, tam), Estilo.PAPEL)
	# manchas de agua muy suaves: el papel se uso
	var manchas := [[Vector2(0.86, 0.12), 190.0, Estilo.CREMA, 0.16], [Vector2(0.10, 0.92), 230.0, Estilo.PETROLEO, 0.035],
		[Vector2(0.55, 0.96), 160.0, Estilo.NARANJA, 0.07], [Vector2(0.97, 0.78), 150.0, Estilo.PETROLEO, 0.03]]
	for m in manchas:
		var centro: Vector2 = m[0] * tam
		var radio: float = m[1]
		var color: Color = m[2]
		var alfa: float = m[3]
		for k in 5:
			var f := 1.0 - float(k) * 0.17
			_papel.draw_circle(centro + Vector2(k * 7.0, -k * 4.0), radio * f, Color(color, alfa * 0.4))
	# cuadricula del cuaderno de ingenieria
	var color_linea := Color(Estilo.PETROLEO, 0.07)
	var x := fmod(tam.x * 0.5, CUADRICULA)
	while x < tam.x:
		_papel.draw_line(Vector2(x, 0), Vector2(x, tam.y), color_linea, 1.0)
		x += CUADRICULA
	var y := fmod(tam.y * 0.5, CUADRICULA)
	while y < tam.y:
		_papel.draw_line(Vector2(0, y), Vector2(tam.x, y), color_linea, 1.0)
		y += CUADRICULA
	# margen del cuaderno y la costura del lomo
	_papel.draw_line(Vector2(38, 0), Vector2(38, tam.y), Color(Estilo.CORAL, 0.28), 1.5)
	for i in 14:
		var c := Vector2(16, 30.0 + float(i) * (tam.y - 60.0) / 13.0)
		_papel.draw_circle(c, 5.0, Color(Estilo.PAPEL_SOMBRA.darkened(0.2), 0.7))
		_papel.draw_circle(c + Vector2(0.6, 0.6), 3.2, Color(Estilo.TINTA, 0.25))


func _dibujar_lamina() -> void:
	var tam := _lamina.size
	# sombra de la lamina sobre la hoja
	for k in 4:
		var d := 2.0 + float(k) * 2.5
		_lamina.draw_rect(Rect2(Vector2(d * 0.6, d), tam), Color(Estilo.TINTA, 0.055))
	_lamina.draw_rect(Rect2(Vector2.ZERO, tam), PAPEL_LAMINA)
	var dentro := Rect2(Vector2(MARGEN_LAMINA, MARGEN_LAMINA), tam - Vector2(MARGEN_LAMINA, MARGEN_LAMINA) * 2.0)
	if _con_arte and _textura != null:
		_lamina.draw_texture_rect_region(_textura, dentro, _region(dentro.size))
	else:
		_lamina_sin_arte(dentro)
	# borde fino de la lamina y dos tiras de cinta de papel
	_lamina.draw_rect(Rect2(Vector2.ZERO, tam), Color(Estilo.TINTA, 0.12), false, 1.0)
	_cinta(Vector2(18, 8), -0.62)
	_cinta(Vector2(tam.x - 18, 8), 0.62)
	_cinta(Vector2(tam.x - 26, tam.y - 4), -0.5)


func _region(destino: Vector2) -> Rect2:
	# encuadre lento dentro de la lamina: un acercamiento y una deriva muy suaves
	var origen := _textura.get_size()
	var aspecto := destino.x / destino.y
	var base := Vector2(origen.x, origen.x / aspecto)
	if base.y > origen.y:
		base = Vector2(origen.y * aspecto, origen.y)
	# el acercamiento minimo deja fuera el borde sin pintar de la acuarela
	var zoom := 1.09 + 0.02 * sin(_t * 0.21)
	var parte := base / zoom
	var holgura := origen - parte
	var u := 0.5 + 0.30 * sin(_t * 0.13)
	var v := 0.5 + 0.25 * cos(_t * 0.11)
	return Rect2(holgura * Vector2(u, v), parte)


func _cinta(centro: Vector2, giro: float) -> void:
	_lamina.draw_set_transform(centro, giro, Vector2.ONE)
	var r := Rect2(-46, -12, 92, 24)
	_lamina.draw_rect(r, CINTA)
	# bordes rasgados de la cinta: pequenos dientes
	var dientes := PackedVector2Array()
	for i in 7:
		dientes.append(Vector2(r.position.x - (2.0 if i % 2 == 0 else 0.0), r.position.y + r.size.y * float(i) / 6.0))
	_lamina.draw_polyline(dientes, Color(Estilo.TINTA, 0.1), 1.0)
	_lamina.draw_line(r.position, r.position + Vector2(r.size.x, 0), Color(1, 1, 1, 0.25), 1.0)
	_lamina.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _lamina_sin_arte(dentro: Rect2) -> void:
	# sin ilustracion: una aguada de noche con la Luna y algunas estrellas a tinta
	_lamina.draw_rect(dentro, Estilo.NOCHE.lightened(0.08))
	_lamina.draw_rect(Rect2(dentro.position + Vector2(0, dentro.size.y * 0.62), Vector2(dentro.size.x, dentro.size.y * 0.38)), Color(Estilo.PETROLEO, 0.5))
	var semilla := 7
	for i in 70:
		semilla = (semilla * 1103515245 + 12345) & 0x7fffffff
		var x := dentro.position.x + float(semilla % 1000) / 1000.0 * dentro.size.x
		semilla = (semilla * 1103515245 + 12345) & 0x7fffffff
		var y := dentro.position.y + float(semilla % 1000) / 1000.0 * dentro.size.y * 0.6
		_lamina.draw_circle(Vector2(x, y), 1.2, Color(Estilo.PAPEL, 0.5))
	var c := dentro.position + dentro.size * Vector2(0.7, 0.32)
	Estilo.luna(_lamina, c, 54.0, 0.12, PI * 0.5 + 0.22, Estilo.CREMA, Color("2a3a42"))


func _dibujar_tinta() -> void:
	var cx := COLUMNA_X
	var tinta := Estilo.TINTA
	# trazo de pincel bajo el nombre del lugar
	if _nombre.text != "":
		var x0 := _nombre.position.x + 2.0
		var y0 := _nombre.position.y + _nombre.size.y - 2.0
		var largo := minf(_nombre.size.x + 24.0, LAMINA.size.x - 20.0)
		_trazo(Vector2(x0, y0), Vector2(x0 + largo, y0 - 3.0), Color(Estilo.TERRACOTA, 0.75), 4.0)
	# itinerario del tramo: un punto de origen, un camino punteado y el destino en un circulo
	var yd := _destino.position.y + _destino.size.y * 0.5
	var pd := Vector2(cx + 11.0, yd)
	if _con_origen:
		var po := Vector2(cx + 11.0, _origen.position.y + _origen.size.y * 0.5)
		_tinta.draw_circle(po, 4.0, Color(tinta, 0.7))
		_punteado(po + Vector2(0, 7), pd - Vector2(0, 11), Color(Estilo.PETROLEO, 0.9))
	_tinta.draw_arc(pd, 8.5, 0.0, TAU, 28, tinta, 2.0, true)
	_tinta.draw_circle(pd, 3.2, Estilo.TERRACOTA)
	# casilla de la mision
	if _mision.text != "" and _objetivo.text != "":
		var caja := Rect2(cx + 2.0, _objetivo.position.y + 4.0, 15.0, 15.0)
		_tinta.draw_rect(caja, Color(tinta, 0.85), false, 1.6)
	# linea bajo las cabeceras
	for l: Label in [_encabezado_tramo, _encabezado_mision, _cuaderno]:
		if l.visible and l.text != "" and (l != _encabezado_mision or _mision.text != ""):
			var y: float = l.position.y + l.size.y + 1.0
			_tinta.draw_line(Vector2(l.position.x, y), Vector2(l.position.x + COLUMNA_ANCHO, y), Color(tinta, 0.22), 1.0)
	# sello de la ficha: un tampon torcido en coral
	if _sello != "":
		var fuente := Estilo.fuente(700, true)
		var tam_letra := 15
		var ancho := fuente.get_string_size(_sello, HORIZONTAL_ALIGNMENT_LEFT, -1, tam_letra).x
		var pos := Vector2(cx + COLUMNA_ANCHO - ancho - 22.0, _fuente.position.y + _fuente.size.y + 32.0)
		_tinta.draw_set_transform(pos, -0.07, Vector2.ONE)
		var marco := Rect2(-9, -21, ancho + 18, 30)
		_tinta.draw_rect(marco, Color(Estilo.CORAL, 0.75), false, 2.0)
		_tinta.draw_rect(marco.grow(-3.0), Color(Estilo.CORAL, 0.35), false, 1.0)
		_tinta.draw_string(fuente, Vector2.ZERO, _sello, HORIZONTAL_ALIGNMENT_LEFT, -1, tam_letra, Color(Estilo.CORAL, 0.9))
		_tinta.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	_dibujar_lunas()


func _dibujar_lunas() -> void:
	# indicador de carga: ocho fases de la Luna dibujadas a tinta; se van entintando una a una
	var n := 8
	var radio := 11.0
	var x0 := COLUMNA_X + 100.0
	var paso := (COLUMNA_ANCHO - 100.0 - radio) / float(n - 1)
	var y := _cargando.position.y + _cargando.size.y * 0.5 + 2.0
	var hechas := _avance * float(n)
	for i in n:
		var c := Vector2(x0 + paso * float(i), y)
		var fase := float(i) / float(n)
		var tinta_i := clampf(hechas - float(i), 0.0, 1.0)
		if tinta_i > 0.0:
			var sombra := Color(Estilo.PETROLEO, 0.75 * tinta_i)
			Estilo.luna(_tinta, c, radio, fase, PI * 0.5, Estilo.PAPEL, sombra)
			_tinta.draw_arc(c, radio, 0.0, TAU, 32, Color(Estilo.TINTA, 0.35 + 0.55 * tinta_i), 1.6, true)
		else:
			_tinta.draw_arc(c, radio, 0.0, TAU, 32, Color(Estilo.TINTA, 0.22), 1.0, true)


func _trazo(a: Vector2, b: Vector2, color: Color, grosor: float) -> void:
	# trazo de pincel: varias pasadas que adelgazan hacia la punta
	for k in 3:
		var d := Vector2(0, float(k) - 1.0) * grosor * 0.35
		var fin := a.lerp(b, 1.0 - float(k) * 0.08)
		_tinta.draw_line(a + d + Vector2(float(k) * 4.0, 0), fin + d, Color(color, color.a * (1.0 - float(k) * 0.25)), grosor * (1.0 - float(k) * 0.3), true)


func _punteado(a: Vector2, b: Vector2, color: Color) -> void:
	# camino de tinta: una curva suave punteada
	var control := (a + b) * 0.5 + Vector2(16, 0)
	var previo := a
	var pasos := 14
	for i in range(1, pasos + 1):
		var t := float(i) / float(pasos)
		var p := a.lerp(control, t).lerp(control.lerp(b, t), t)
		if i % 2 == 1:
			_tinta.draw_line(previo, p, color, 2.0, true)
		previo = p


func _estrella(c: Vector2, r: float, color: Color) -> void:
	for k in 4:
		var a := PI * 0.25 * float(k)
		_tinta.draw_line(c - Vector2(cos(a), sin(a)) * r, c + Vector2(cos(a), sin(a)) * r, color, 1.5, true)


# ------------------------------------------------------------------ contenido

func _elegir_ficha(meta: Dictionary) -> String:
	var carga: Dictionary = meta.get("carga", {})
	var candidatas: Array = carga.get("fichas", [])
	var validas: Array = []
	for id_ficha in candidatas:
		if not Juego.ficha(id_ficha).is_empty():
			validas.append(id_ficha)
	if validas.is_empty():
		validas = Juego.fichas.keys()
	if validas.is_empty():
		return ""
	var eleccion: String = validas[randi() % validas.size()]
	if validas.size() > 1 and eleccion == _ultima_ficha:
		eleccion = validas[(validas.find(eleccion) + 1) % validas.size()]
	_ultima_ficha = eleccion
	return eleccion


func preparar(meta: Dictionary) -> void:
	_t = 0.0
	_avance = 0.0
	_nombre.text = meta.get("nombre", "")
	var detalle: Array = []
	for clave in ["lugar", "momento"]:
		if meta.get(clave, "") != "":
			detalle.append(meta[clave])
	_detalle.text = " · ".join(PackedStringArray(detalle))
	var estado: String = meta.get("estado_arte", "")
	_estado.text = "Escenario provisional: el arte espera validación" if estado.begins_with("provisional") else ""
	# de donde a donde
	var origen := ""
	if Zonas.id_actual != "" and Zonas.id_actual != meta.get("id", ""):
		origen = Zonas.info(Zonas.id_actual).get("nombre", "")
	_con_origen = origen != ""
	_origen.text = origen
	_origen.visible = _con_origen
	_destino.text = meta.get("nombre", "") if _con_origen else "Inicio de la expedición"
	# mision en curso
	var m := Juego.mision_activa()
	_mision.text = String(m.get("titulo", "")) if not m.is_empty() else ""
	_objetivo.text = Juego.objetivo() if _mision.text != "" else ""
	_encabezado_mision.visible = _mision.text != ""
	# ilustracion
	var carga: Dictionary = meta.get("carga", {})
	var textura: Texture2D = null
	var propia := "res://interfaz/arte/carga_%s.jpg" % String(meta.get("id", ""))
	if FileAccess.file_exists(propia):
		textura = Recursos.textura(propia)
	elif carga.get("imagen", "") != "":
		textura = Recursos.textura(carga["imagen"])
	_textura = textura
	_con_arte = textura != null
	# dato del cuaderno
	var id_ficha := _elegir_ficha(meta)
	var f := Juego.ficha(id_ficha)
	_cuaderno.visible = not f.is_empty()
	_titulo.text = f.get("titulo", "")
	_texto.text = f.get("texto", "")
	_fuente.text = ("Fuente: %s" % f["fuente"]) if f.has("fuente") else ""
	_sello = f.get("sello", "")
	for l in [_origen, _destino, _nombre, _detalle, _estado, _mision, _objetivo, _titulo, _texto, _fuente]:
		l.reset_size()
	_colocar()
	_papel.queue_redraw()
	_lamina.queue_redraw()
	_tinta.queue_redraw()
	if id_ficha != "":
		Juego.anotar(id_ficha)


func mostrar(meta: Dictionary) -> void:
	preparar(meta)
	visible = true
	if Juego.modo_prueba:
		_entrada = 1.0
		modulate.a = 1.0
		await get_tree().process_frame
		return
	_entrada = 0.0
	var t := create_tween().set_parallel(true)
	t.tween_property(self, "modulate:a", 1.0, 0.4)
	t.tween_property(self, "_entrada", 1.0, 0.7).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	await t.finished


func ocultar() -> void:
	if Juego.modo_prueba:
		modulate.a = 0.0
		visible = false
		await get_tree().process_frame
		return
	var t := create_tween()
	t.tween_property(self, "modulate:a", 0.0, 0.5)
	await t.finished
	visible = false
