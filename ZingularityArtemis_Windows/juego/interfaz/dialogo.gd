extends Control

# Caja de dialogo: el texto aparece letra a letra; se avanza con E, Intro, Espacio o un clic.
# Tambien muestra preguntas con opciones. Con Juego.modo_prueba no espera.

signal _siguiente
signal _elegida(indice: int)

const Estilo := preload("res://interfaz/estilo.gd")
const LETRAS_POR_SEGUNDO := 48.0

var _panel: PanelContainer
var _nombre: PanelContainer
var _nombre_texto: Label
var _texto: Label
var _flecha: Label
var _opciones: VBoxContainer
var _visibles := 0.0
var _escribiendo := false
var _esperando := false


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	visible = false

	_panel = Estilo.panel(Color(Estilo.PAPEL, 0.97), 16, 3, 22)
	_panel.custom_minimum_size = Vector2(940, 150)
	add_child(_panel)
	var columna := VBoxContainer.new()
	_panel.add_child(columna)
	_texto = Estilo.texto("", 24, Estilo.TINTA, 500)
	_texto.custom_minimum_size = Vector2(880, 96)
	_texto.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	columna.add_child(_texto)
	_flecha = Estilo.texto("▼", 18, Estilo.CIAN_MEDIO, 700)
	_flecha.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	columna.add_child(_flecha)

	_nombre = Estilo.panel(Estilo.PETROLEO, 10, 3, 8)
	_nombre_texto = Estilo.texto("", 19, Estilo.PAPEL, 700)
	_nombre_texto.autowrap_mode = TextServer.AUTOWRAP_OFF
	_nombre.add_child(_nombre_texto)
	add_child(_nombre)

	_opciones = VBoxContainer.new()
	_opciones.add_theme_constant_override("separation", 8)
	add_child(_opciones)


func _process(delta: float) -> void:
	if not visible:
		return
	var tam := size
	_panel.reset_size()
	_panel.position = Vector2((tam.x - _panel.size.x) * 0.5, tam.y - _panel.size.y - 34)
	_nombre.position = _panel.position + Vector2(26, -_nombre.size.y + 8)
	_opciones.position = Vector2(_panel.position.x + _panel.size.x - _opciones.size.x - 10, _panel.position.y - _opciones.size.y - 14)
	if _escribiendo:
		_visibles += delta * LETRAS_POR_SEGUNDO
		_texto.visible_characters = int(_visibles)
		if int(_visibles) >= _texto.text.length():
			_completar()
	_flecha.modulate.a = (0.55 + 0.45 * sin(Time.get_ticks_msec() * 0.006)) if _esperando else 0.0


func _completar() -> void:
	_escribiendo = false
	_texto.visible_characters = -1
	_esperando = true


func _input(evento: InputEvent) -> void:
	if not visible or _opciones.get_child_count() > 0:
		return
	var pulsado := evento.is_action_pressed("interactuar") or evento.is_action_pressed("ui_accept") or evento.is_action_pressed("saltar")
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		pulsado = true
	if not pulsado:
		return
	get_viewport().set_input_as_handled()
	if _escribiendo:
		_completar()
	elif _esperando:
		_esperando = false
		Audio.sonar("pagina")
		_siguiente.emit()


func decir(lineas: Variant, quien_por_defecto: String = "") -> void:
	# lineas: un texto, o una lista de textos o de {"quien": "Órbita", "texto": "..."}
	var lista: Array = lineas if lineas is Array else [lineas]
	visible = true
	for l in lista:
		var quien := quien_por_defecto
		var contenido := ""
		if l is Dictionary:
			quien = l.get("quien", quien_por_defecto)
			contenido = l.get("texto", "")
		else:
			contenido = str(l)
		_nombre.visible = quien != ""
		_nombre_texto.text = quien
		_nombre.reset_size()
		_texto.text = contenido
		_texto.visible_characters = 0
		_visibles = 0.0
		_esperando = false
		_escribiendo = true
		if Juego.modo_prueba:
			_completar()
			await get_tree().process_frame
		else:
			await _siguiente
	visible = false


func elegir(pregunta: Variant, opciones: Array) -> int:
	# muestra la pregunta y devuelve el indice de la opcion elegida
	visible = true
	var quien := ""
	var contenido := ""
	if pregunta is Dictionary:
		quien = pregunta.get("quien", "")
		contenido = pregunta.get("texto", "")
	else:
		contenido = str(pregunta)
	_nombre.visible = quien != ""
	_nombre_texto.text = quien
	_texto.text = contenido
	_texto.visible_characters = -1
	_escribiendo = false
	_esperando = false
	for i in opciones.size():
		var b := Estilo.boton(str(opciones[i]), 21)
		b.custom_minimum_size = Vector2(420, 46)
		b.alignment = HORIZONTAL_ALIGNMENT_LEFT
		b.pressed.connect(func(): _elegida.emit(i))
		_opciones.add_child(b)
	_opciones.reset_size()
	var indice := 0
	if Juego.modo_prueba:
		await get_tree().process_frame
	else:
		(_opciones.get_child(0) as Button).grab_focus()
		indice = await _elegida
	for hijo in _opciones.get_children():
		hijo.queue_free()
	await get_tree().process_frame
	visible = false
	return indice
