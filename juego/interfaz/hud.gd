extends Control

# HUD de exploracion: objetivo actual (arriba a la izquierda), nombre del lugar al llegar, avisos, inventario
# y el rotulo de interaccion ("[E] Examinar"). Estilo provisional (Fase 7 sin validar).

const Estilo := preload("res://interfaz/estilo.gd")

var _tarjeta: PanelContainer
var _mision: Label
var _objetivo: Label
var _rotulo: PanelContainer
var _rotulo_texto: Label
var _avisos: VBoxContainer
var _lugar: VBoxContainer
var _lugar_nombre: Label
var _lugar_detalle: Label
var _inventario: Label
var _ayuda: Label
var _indicacion := ""
var _rotulos := {}


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	_tarjeta = Estilo.panel(Color(Estilo.PAPEL, 0.94), 12, 3, 12)
	_tarjeta.position = Vector2(18, 16)
	_tarjeta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var columna := VBoxContainer.new()
	columna.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_mision = Estilo.texto("", 14, Estilo.TERRACOTA, 700)
	_objetivo = Estilo.texto("", 19, Estilo.TINTA, 600)
	_objetivo.custom_minimum_size = Vector2(330, 0)
	columna.add_child(_mision)
	columna.add_child(_objetivo)
	_tarjeta.add_child(columna)
	add_child(_tarjeta)

	_inventario = Estilo.texto("", 17, Estilo.PAPEL, 600)
	_inventario.add_theme_color_override("font_outline_color", Estilo.TINTA)
	_inventario.add_theme_constant_override("outline_size", 6)
	_inventario.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_inventario.autowrap_mode = TextServer.AUTOWRAP_OFF
	add_child(_inventario)

	_avisos = VBoxContainer.new()
	_avisos.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_avisos.alignment = BoxContainer.ALIGNMENT_BEGIN
	_avisos.add_theme_constant_override("separation", 6)
	add_child(_avisos)

	_lugar = VBoxContainer.new()
	_lugar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_lugar.modulate.a = 0.0
	_lugar_nombre = Estilo.texto("", 40, Estilo.PAPEL, 700)
	_lugar_detalle = Estilo.texto("", 20, Estilo.CREMA, 500)
	for l in [_lugar_nombre, _lugar_detalle]:
		l.add_theme_color_override("font_outline_color", Estilo.TINTA)
		l.add_theme_constant_override("outline_size", 8)
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.autowrap_mode = TextServer.AUTOWRAP_OFF
		_lugar.add_child(l)
	add_child(_lugar)

	_rotulo = Estilo.panel(Color(Estilo.NOCHE, 0.92), 10, 2, 10)
	_rotulo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_rotulo_texto = Estilo.texto("", 20, Estilo.BRILLO, 600)
	_rotulo_texto.autowrap_mode = TextServer.AUTOWRAP_OFF
	_rotulo.add_child(_rotulo_texto)
	_rotulo.visible = false
	add_child(_rotulo)

	_ayuda = Estilo.texto("WASD o flechas: moverse · Mayús: correr · E: interactuar · Tab: cuaderno · Esc: pausa · Z/X: acercar y alejar", 14, Estilo.PAPEL, 500)
	_ayuda.add_theme_color_override("font_outline_color", Estilo.TINTA)
	_ayuda.add_theme_constant_override("outline_size", 5)
	_ayuda.autowrap_mode = TextServer.AUTOWRAP_OFF
	add_child(_ayuda)

	Juego.misiones_cambiadas.connect(actualizar)
	Juego.inventario_cambiado.connect(func(_a, _b): actualizar())
	actualizar()


func _process(_delta: float) -> void:
	var tam := size
	_tarjeta.reset_size()
	_inventario.position = Vector2(tam.x - _inventario.size.x - 20, 18)
	_avisos.position = Vector2((tam.x - _avisos.size.x) * 0.5, 84)
	_lugar.position = Vector2((tam.x - _lugar.size.x) * 0.5, tam.y * 0.20)
	_rotulo.position = Vector2((tam.x - _rotulo.size.x) * 0.5, tam.y - _rotulo.size.y - 54)
	_ayuda.position = Vector2(18, tam.y - 30)
	var mostrado := _indicacion
	if mostrado == "":
		for v in _rotulos.values():
			mostrado = v
			break
	_rotulo.visible = mostrado != ""
	if mostrado != _rotulo_texto.text:
		_rotulo_texto.text = mostrado
		_rotulo.reset_size()


func actualizar() -> void:
	var m := Juego.mision_activa()
	var texto := Juego.objetivo()
	_tarjeta.visible = texto != ""
	_mision.text = String(m.get("titulo", "")).to_upper()
	_objetivo.text = texto
	_tarjeta.reset_size()
	var partes: Array = []
	var inv: Dictionary = Juego.estado.get("inventario", {})
	for clave in inv:
		if int(inv[clave]) > 0:
			partes.append("%s × %d" % [String(clave).replace("_", " "), int(inv[clave])])
	_inventario.text = "   ".join(PackedStringArray(partes))
	_inventario.reset_size()


func indicar(texto: String) -> void:
	_indicacion = texto


func rotular(origen: Object, texto: String) -> void:
	var clave := origen.get_instance_id()
	if texto == "":
		_rotulos.erase(clave)
	else:
		_rotulos[clave] = texto


func limpiar_rotulos() -> void:
	_rotulos.clear()
	_indicacion = ""


func aviso(texto: String, segundos: float = 3.0) -> void:
	var caja := Estilo.panel(Color(Estilo.NOCHE, 0.92), 10, 2, 10)
	caja.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var l := Estilo.texto(texto, 19, Estilo.BRILLO, 600)
	l.autowrap_mode = TextServer.AUTOWRAP_OFF
	caja.add_child(l)
	caja.modulate.a = 0.0
	_avisos.add_child(caja)
	_avisos.reset_size()
	var t := caja.create_tween()
	t.tween_property(caja, "modulate:a", 1.0, 0.2)
	t.tween_interval(segundos)
	t.tween_property(caja, "modulate:a", 0.0, 0.4)
	t.tween_callback(caja.queue_free)


func anunciar_zona(meta: Dictionary) -> void:
	_lugar_nombre.text = meta.get("nombre", "")
	var detalle: Array = []
	for clave in ["lugar", "momento"]:
		if meta.get(clave, "") != "":
			detalle.append(meta[clave])
	_lugar_detalle.text = " · ".join(PackedStringArray(detalle))
	_lugar.reset_size()
	var t := _lugar.create_tween()
	t.tween_property(_lugar, "modulate:a", 1.0, 0.5)
	t.tween_interval(2.6)
	t.tween_property(_lugar, "modulate:a", 0.0, 0.9)
	_ayuda.visible = float(Juego.estado.get("tiempo", 0.0)) < 240.0
