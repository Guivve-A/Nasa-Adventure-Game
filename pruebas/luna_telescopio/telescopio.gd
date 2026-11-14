extends Control

# Prueba tecnica del Mirador del Faro: la Luna real de una fecha, vista desde Guayaquil,
# con texturas de NASA (LRO LROC y LOLA) y datos de JPL Horizons.
# Argumentos tras "--":  --captura=<ruta.png>  guarda una captura y sale;  --prueba  dibuja solo la mascara.
# Las texturas son recursos importados (con mipmaps), para que tambien existan en el juego exportado.

const TINTA := Color("2f2a24")
const PAPEL := Color("f3e6cb")
const CIAN := Color("62e4e0")
const DATO := Color("1d6f72")
const CENTRO_UV := Vector2(0.40, 0.5)
const RADIO_BASE := 0.29          # radio del disco con 29,63' de tamano aparente
const DIAMETRO_BASE := 29.63
const RADIO_OCULAR := 0.46
const MESES := ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
const COLOR_LUNA := preload("res://texturas/luna_color_4k.jpg")
const NORMALES_LUNA := preload("res://texturas/luna_normales.png")
const ORBITA := preload("res://texturas/orbita_senalando.png")

var datos: Dictionary = {}
var texturas: Dictionary = {}
var captura := ""
var modo_prueba := false


func _ready() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--captura="):
			captura = arg.trim_prefix("--captura=")
		elif arg == "--prueba":
			modo_prueba = true
	datos = _leer_json("res://datos/luna.json")
	texturas = _leer_json("res://texturas/texturas.json")
	_crear_luna()
	if not modo_prueba:
		_crear_interfaz()
	if captura != "":
		for i in range(8):
			await get_tree().process_frame
		var ruta := captura if captura.is_absolute_path() else OS.get_user_data_dir().path_join(captura)
		DirAccess.make_dir_recursive_absolute(ruta.get_base_dir())
		var imagen := get_viewport().get_texture().get_image()
		if imagen.get_format() != Image.FORMAT_RGBA8 and imagen.get_format() != Image.FORMAT_RGB8:
			imagen = _lineal_a_srgb(imagen)  # con HDR 2D la imagen llega lineal y en coma flotante
		imagen.save_png(ruta)
		print("CAPTURA_OK ", ruta)
		get_tree().quit()


func _lineal_a_srgb(imagen: Image) -> Image:
	# Image.linear_to_srgb() solo acepta RGB8 y RGBA8; pasar antes a 8 bits destruiria las sombras
	imagen.convert(Image.FORMAT_RGBAF)
	for y in imagen.get_height():
		for x in imagen.get_width():
			imagen.set_pixel(x, y, imagen.get_pixel(x, y).linear_to_srgb())
	imagen.convert(Image.FORMAT_RGBA8)
	return imagen


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("ui_cancel"):
		get_tree().quit()


func _leer_json(ruta: String) -> Dictionary:
	var resultado = JSON.parse_string(FileAccess.get_file_as_string(ruta))
	if typeof(resultado) != TYPE_DICTIONARY:
		push_error("No se pudo leer " + ruta)
		return {}
	return resultado


func _direccion(lon_deg: float, lat_deg: float) -> Vector3:
	# Marco del cuerpo: X hacia (lon 0, lat 0), Y hacia (lon 90 E, lat 0), Z hacia el polo norte
	var lon := deg_to_rad(lon_deg)
	var lat := deg_to_rad(lat_deg)
	return Vector3(cos(lat) * cos(lon), cos(lat) * sin(lon), sin(lat))


func _radio() -> float:
	return RADIO_BASE * float(datos["diametro_arcmin"]) / DIAMETRO_BASE


func _visible() -> bool:
	# borde superior con refraccion estandar: centro a mas de -(34' + semidiametro)
	return float(datos["elevacion_deg"]) > -(34.0 + float(datos["diametro_arcmin"]) / 2.0) / 60.0


func _crear_luna() -> void:
	var tam := get_viewport_rect().size
	var fase := deg_to_rad(float(datos["angulo_fase_deg"]))
	var material := ShaderMaterial.new()
	material.shader = load("res://luna.gdshader")
	material.set_shader_parameter("color_luna", COLOR_LUNA)
	material.set_shader_parameter("normales_luna", NORMALES_LUNA)
	material.set_shader_parameter("dir_obs", _direccion(datos["subobservador_lon_deg"], datos["subobservador_lat_deg"]))
	material.set_shader_parameter("dir_sol", _direccion(datos["subsolar_lon_deg"], datos["subsolar_lat_deg"]))
	# polo norte lunar respecto del cenit del Mirador: su angulo de posicion menos el angulo paralactico
	material.set_shader_parameter("pa_norte", deg_to_rad(datos["pa_polo_norte_deg"] - datos["angulo_paralactico_deg"]))
	material.set_shader_parameter("lon_centro", deg_to_rad(texturas["lon_centro_deg"]))
	material.set_shader_parameter("centro", CENTRO_UV)
	material.set_shader_parameter("radio", _radio())
	material.set_shader_parameter("radio_ocular", RADIO_OCULAR)
	material.set_shader_parameter("aspecto", tam.x / tam.y)
	# la Tierra vista desde la Luna esta casi llena cuando la Luna es una creciente fina
	material.set_shader_parameter("factor_cenicienta", (1.0 - cos(fase)) / 1.757)
	material.set_shader_parameter("mostrar_luna", _visible())
	material.set_shader_parameter("salida_lineal", get_viewport().use_hdr_2d)
	material.set_shader_parameter("modo_prueba", 1 if modo_prueba else 0)
	var lienzo := ColorRect.new()
	lienzo.set_anchors_preset(Control.PRESET_FULL_RECT)
	lienzo.material = material
	add_child(lienzo)


func _crear_interfaz() -> void:
	var tam := get_viewport_rect().size
	var centro := CENTRO_UV * tam
	var r := _radio() * tam.y
	var titulo := _etiqueta("Mirador del Faro · Telescopio", 28, PAPEL)
	titulo.position = Vector2(24, 14)
	add_child(titulo)
	if _visible():
		_rotulos_luna(centro, r)
	else:
		var aviso := _etiqueta("La Luna está bajo el horizonte", 26, PAPEL)
		aviso.position = centro - Vector2(190, 18)
		add_child(aviso)
	_panel_datos(tam)
	_orbita(tam)
	var pie := _etiqueta("Prueba técnica · Luna real del " + _fecha() + ", vista desde el Mirador del Faro", 14, Color("9fb4b8"))
	pie.position = Vector2(24, tam.y - 30)
	add_child(pie)


func _rotulos_luna(centro: Vector2, r: float) -> void:
	var ilum := float(datos["iluminacion_pct"])
	# Direccion del borde iluminado segun Horizons (angulo desde el cenit, positivo a la izquierda)
	var theta := deg_to_rad(datos["borde_iluminado_desde_cenit_deg"])
	var v := Vector2(-sin(theta), -cos(theta))
	if ilum > 3.0 and ilum < 97.0:
		# El terminador corta ese eje a -cos(angulo de fase) radios del centro
		var fase := deg_to_rad(datos["angulo_fase_deg"])
		_rotulo("Terminador", centro + v * (-cos(fase)) * r, centro + Vector2(r * 1.02, r * 0.66))
	if ilum < 50.0 and datos["cielo"] != "día":
		_rotulo("Luz cenicienta", centro - v * 0.35 * r, centro + Vector2(r * 0.9, -r * 0.82))


func _rotulo(texto: String, punto: Vector2, destino: Vector2) -> void:
	var linea := Line2D.new()
	linea.points = PackedVector2Array([punto, destino, destino + Vector2(118, 0)])
	linea.width = 2.0
	linea.default_color = CIAN
	add_child(linea)
	var marca := Line2D.new()
	marca.points = PackedVector2Array([punto - Vector2(4, 0), punto + Vector2(4, 0)])
	marca.width = 8.0
	marca.default_color = CIAN
	marca.begin_cap_mode = Line2D.LINE_CAP_ROUND
	marca.end_cap_mode = Line2D.LINE_CAP_ROUND
	add_child(marca)
	var etiqueta := _etiqueta(texto, 19, Color("dff7f6"))
	etiqueta.position = destino + Vector2(4, -26)
	add_child(etiqueta)


func _panel_datos(tam: Vector2) -> void:
	var panel := PanelContainer.new()
	panel.position = Vector2(tam.x - 388, 54)
	panel.custom_minimum_size = Vector2(360, 0)
	panel.add_theme_stylebox_override("panel", _estilo_papel())
	var caja := VBoxContainer.new()
	caja.add_theme_constant_override("separation", 9)
	panel.add_child(caja)
	caja.add_child(_etiqueta("Luna · esta noche", 30, TINTA))
	var puesta = datos.get("puesta_guayaquil")
	var filas := [
		["Hora", datos["guayaquil"].substr(11, 5)],
		["Fase", datos["fase"]],
		["Iluminada", "%d %%" % roundi(datos["iluminacion_pct"])],
		["Distancia", _miles(int(datos["distancia_km"])) + " km"],
		["Tamaño aparente", ("%.1f′" % datos["diametro_arcmin"]).replace(".", ",")],
		["Altura", "%d°" % roundi(datos["elevacion_deg"])],
		["Se pone", str(puesta) if puesta != null else "—"],
	]
	for fila in filas:
		var renglon := HBoxContainer.new()
		var clave := _etiqueta(fila[0] + ":", 21, TINTA)
		clave.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		renglon.add_child(clave)
		renglon.add_child(_etiqueta(fila[1], 21, DATO))
		caja.add_child(renglon)
	var fuente := _etiqueta("Fuente: " + datos["fuente"] + " · " + _fecha() + " · Guayaquil", 13, TINTA)
	fuente.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	fuente.custom_minimum_size = Vector2(324, 0)
	caja.add_child(fuente)
	add_child(panel)


func _frase_orbita() -> String:
	if not _visible():
		# bajo el horizonte: por el oeste ya se puso; por el este todavia no sale
		if float(datos.get("azimut_deg", 270.0)) < 180.0:
			return "La Luna todavía no sale. Vuelve más tarde."
		return "La Luna ya se ocultó. Vuelve otra noche."
	var ilum := float(datos["iluminacion_pct"])
	var borde := float(datos["borde_iluminado_desde_cenit_deg"])
	var acostada := absf(borde - 180.0) < 30.0
	if ilum < 50.0 and acostada:
		return "¿Ves la sonrisa? Cerca del ecuador, la Luna %s se ve acostada." % datos["fase"]
	if ilum > 99.0:
		return "¡Luna llena! Toda la cara que vemos recibe luz del Sol."
	return "Hoy la Luna está iluminada al %d %%, a %s km de nosotros." % [roundi(ilum), _miles(int(datos["distancia_km"]))]


func _orbita(tam: Vector2) -> void:
	var gato := TextureRect.new()
	gato.texture = ORBITA
	gato.position = Vector2(4, tam.y - 360)
	add_child(gato)
	var globo := PanelContainer.new()
	globo.position = Vector2(14, 118)
	globo.custom_minimum_size = Vector2(236, 0)
	globo.add_theme_stylebox_override("panel", _estilo_papel())
	var texto := _etiqueta(_frase_orbita(), 19, TINTA)
	texto.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	texto.custom_minimum_size = Vector2(204, 0)
	globo.add_child(texto)
	add_child(globo)


func _estilo_papel() -> StyleBoxFlat:
	var estilo := StyleBoxFlat.new()
	estilo.bg_color = PAPEL
	estilo.border_color = TINTA
	estilo.set_border_width_all(2)
	estilo.set_corner_radius_all(6)
	estilo.set_content_margin_all(16)
	return estilo


func _etiqueta(texto: String, tamano: int, color: Color) -> Label:
	var etiqueta := Label.new()
	etiqueta.text = texto
	etiqueta.add_theme_font_size_override("font_size", tamano)
	etiqueta.add_theme_color_override("font_color", color)
	return etiqueta


func _fecha() -> String:
	var t: String = datos["guayaquil"]
	return "%d %s %s, %s" % [int(t.substr(8, 2)), MESES[int(t.substr(5, 2)) - 1], t.substr(0, 4), t.substr(11, 5)]


func _miles(n: int) -> String:
	var s := str(n)
	var salida := ""
	while s.length() > 3:
		salida = " " + s.substr(s.length() - 3) + salida
		s = s.substr(0, s.length() - 3)
	return s + salida
