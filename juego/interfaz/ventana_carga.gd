extends Control

# Ventana de carga: una pagina del cuaderno con el lugar al que se llega, su ilustracion y un dato real con su
# fuente (pedido de Guillermo: cada escena con su entrada, su salida y su ventana de carga). La Luna gira de
# fase mientras carga. Si el arte de la zona es provisional, lo dice.
#
# zona.json -> "carga": {"imagen": "res://zonas/<id>/carga.jpg", "fichas": ["id_de_ficha", ...]}

const Estilo := preload("res://interfaz/estilo.gd")
const Recursos := preload("res://nucleo/recursos.gd")

var _pagina: PanelContainer
var _imagen: TextureRect
var _marco: PanelContainer
var _nombre: Label
var _detalle: Label
var _titulo: Label
var _texto: Label
var _fuente: Label
var _sello: Label
var _estado: Label
var _luna: Control
var _fase := 0.0
var _ultima_ficha := ""


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	modulate.a = 0.0
	var fondo := ColorRect.new()
	fondo.color = Estilo.NOCHE
	fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(fondo)

	_pagina = Estilo.panel(Estilo.PAPEL, 18, 4, 30)
	_pagina.custom_minimum_size = Vector2(1060, 560)
	add_child(_pagina)
	var fila := HBoxContainer.new()
	fila.add_theme_constant_override("separation", 34)
	_pagina.add_child(fila)

	# izquierda: la ilustracion y el lugar
	var izquierda := VBoxContainer.new()
	izquierda.add_theme_constant_override("separation", 10)
	izquierda.custom_minimum_size = Vector2(470, 0)
	fila.add_child(izquierda)
	_marco = Estilo.panel(Color("fffaf0"), 6, 3, 8)
	_imagen = TextureRect.new()
	_imagen.custom_minimum_size = Vector2(452, 254)
	_imagen.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_imagen.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_marco.add_child(_imagen)
	izquierda.add_child(_marco)
	_nombre = Estilo.texto("", 36, Estilo.TINTA, 700)
	_detalle = Estilo.texto("", 19, Estilo.TERRACOTA, 600)
	_estado = Estilo.texto("", 15, Estilo.TINTA_SUAVE, 500)
	izquierda.add_child(_nombre)
	izquierda.add_child(_detalle)
	izquierda.add_child(_estado)

	# derecha: el dato del cuaderno
	var derecha := VBoxContainer.new()
	derecha.add_theme_constant_override("separation", 12)
	derecha.custom_minimum_size = Vector2(470, 0)
	fila.add_child(derecha)
	derecha.add_child(Estilo.texto("DEL CUADERNO", 15, Estilo.PETROLEO, 700))
	_titulo = Estilo.texto("", 28, Estilo.TINTA, 700)
	_texto = Estilo.texto("", 21, Estilo.TINTA, 500)
	_fuente = Estilo.texto("", 15, Estilo.TINTA_SUAVE, 500)
	_sello = Estilo.texto("", 20, Estilo.CORAL, 700, true)
	_sello.rotation = deg_to_rad(-4.0)
	derecha.add_child(_titulo)
	derecha.add_child(_texto)
	derecha.add_child(_fuente)
	derecha.add_child(Estilo.separador(6))
	derecha.add_child(_sello)
	var relleno := Control.new()
	relleno.size_flags_vertical = Control.SIZE_EXPAND_FILL
	derecha.add_child(relleno)
	var pie := HBoxContainer.new()
	pie.add_theme_constant_override("separation", 14)
	_luna = Control.new()
	_luna.custom_minimum_size = Vector2(46, 46)
	_luna.draw.connect(_dibujar_luna)
	pie.add_child(_luna)
	var cargando := Estilo.linea("Cargando…", 18, Estilo.TINTA_SUAVE, 600)
	cargando.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	pie.add_child(cargando)
	derecha.add_child(pie)


func _process(delta: float) -> void:
	if not visible:
		return
	_pagina.reset_size()
	_pagina.position = (size - _pagina.size) * 0.5
	_fase = fmod(_fase + delta * 0.35, 1.0)
	_luna.queue_redraw()


func _dibujar_luna() -> void:
	Estilo.luna(_luna, Vector2(23, 23), 20.0, _fase, PI * 0.5, Estilo.CREMA, Estilo.PETROLEO)


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
	# no repite la ultima si hay mas de una
	var eleccion: String = validas[randi() % validas.size()]
	if validas.size() > 1 and eleccion == _ultima_ficha:
		eleccion = validas[(validas.find(eleccion) + 1) % validas.size()]
	_ultima_ficha = eleccion
	return eleccion


func preparar(meta: Dictionary) -> void:
	_nombre.text = meta.get("nombre", "")
	var detalle: Array = []
	for clave in ["lugar", "momento"]:
		if meta.get(clave, "") != "":
			detalle.append(meta[clave])
	_detalle.text = " · ".join(PackedStringArray(detalle))
	var estado: String = meta.get("estado_arte", "")
	_estado.text = ("Escenario provisional: el arte espera la validación de Guillermo." if estado.begins_with("provisional") else "")
	var carga: Dictionary = meta.get("carga", {})
	var textura: Texture2D = null
	if carga.get("imagen", "") != "":
		textura = Recursos.textura(carga["imagen"])
	_imagen.texture = textura
	_marco.visible = textura != null
	var id_ficha := _elegir_ficha(meta)
	var f := Juego.ficha(id_ficha)
	_titulo.text = f.get("titulo", "")
	_texto.text = f.get("texto", "")
	_fuente.text = ("Fuente: %s" % f["fuente"]) if f.has("fuente") else ""
	_sello.text = f.get("sello", "")
	if id_ficha != "":
		Juego.anotar(id_ficha)


func mostrar(meta: Dictionary) -> void:
	preparar(meta)
	visible = true
	_pagina.reset_size()
	if Juego.modo_prueba:
		modulate.a = 1.0
		await get_tree().process_frame
		return
	var t := create_tween()
	t.tween_property(self, "modulate:a", 1.0, 0.35)
	await t.finished


func ocultar() -> void:
	if Juego.modo_prueba:
		modulate.a = 0.0
		visible = false
		await get_tree().process_frame
		return
	var t := create_tween()
	t.tween_property(self, "modulate:a", 0.0, 0.45)
	await t.finished
	visible = false
