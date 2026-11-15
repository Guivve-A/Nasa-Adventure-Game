extends Control

# El cuaderno (Tab): fichas de datos espaciales reales que se van abriendo, con su fuente y su sello, y la
# lista de misiones. Estilo provisional (Fase 7 sin validar).

signal cerrado

const Estilo := preload("res://interfaz/estilo.gd")

var _panel: PanelContainer
var _lista: VBoxContainer
var _detalle: VBoxContainer
var _contador: Label
var _cerrar: Button


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var velo := ColorRect.new()
	velo.color = Color(Estilo.NOCHE, 0.80)
	velo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(velo)
	_panel = Estilo.panel(Estilo.PAPEL, 16, 4, 24)
	_panel.custom_minimum_size = Vector2(1080, 600)
	add_child(_panel)
	var columna := VBoxContainer.new()
	columna.add_theme_constant_override("separation", 10)
	_panel.add_child(columna)
	var cabecera := HBoxContainer.new()
	var titulo := Estilo.texto("Cuaderno de ingeniería", 30, Estilo.TINTA, 700)
	titulo.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	cabecera.add_child(titulo)
	_contador = Estilo.texto("", 18, Estilo.TERRACOTA, 600)
	_contador.autowrap_mode = TextServer.AUTOWRAP_OFF
	_contador.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	cabecera.add_child(_contador)
	_cerrar = Estilo.boton("Cerrar (Tab)", 16)
	_cerrar.custom_minimum_size = Vector2(140, 38)
	_cerrar.pressed.connect(cerrar)
	cabecera.add_child(_cerrar)
	columna.add_child(cabecera)
	var fila := HBoxContainer.new()
	fila.add_theme_constant_override("separation", 20)
	fila.size_flags_vertical = Control.SIZE_EXPAND_FILL
	columna.add_child(fila)
	var desliza := ScrollContainer.new()
	desliza.custom_minimum_size = Vector2(400, 490)
	desliza.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	_lista = VBoxContainer.new()
	_lista.add_theme_constant_override("separation", 6)
	_lista.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	desliza.add_child(_lista)
	fila.add_child(desliza)
	var hoja := Estilo.panel(Color("fffaf0"), 10, 2, 20)
	hoja.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_detalle = VBoxContainer.new()
	_detalle.add_theme_constant_override("separation", 12)
	hoja.add_child(_detalle)
	fila.add_child(hoja)


func _process(_delta: float) -> void:
	if visible:
		_panel.position = (size - _panel.size) * 0.5


func abrir() -> void:
	for hijo in _lista.get_children():
		_lista.remove_child(hijo)
		hijo.queue_free()
	var abiertas: Array = Juego.estado.get("cuaderno", [])
	_contador.text = "%d de %d fichas   " % [abiertas.size(), Juego.fichas.size()]
	var primero: Button = null
	var por_categoria := {}
	for id_ficha in abiertas:
		var f := Juego.ficha(id_ficha)
		if f.is_empty():
			continue
		var cat: String = f.get("categoria", "Otros")
		if not por_categoria.has(cat):
			por_categoria[cat] = []
		por_categoria[cat].append(id_ficha)
	for cat in por_categoria:
		_lista.add_child(Estilo.texto(String(cat).to_upper(), 14, Estilo.PETROLEO, 700))
		for id_ficha in por_categoria[cat]:
			var f := Juego.ficha(id_ficha)
			var b := Estilo.boton(f.get("titulo", id_ficha), 18)
			b.alignment = HORIZONTAL_ALIGNMENT_LEFT
			b.custom_minimum_size = Vector2(380, 40)
			var elegido: String = id_ficha
			b.pressed.connect(func(): _mostrar(elegido))
			b.focus_entered.connect(func(): _mostrar(elegido))
			_lista.add_child(b)
			if primero == null:
				primero = b
	if primero == null:
		_mostrar("")
		_cerrar.grab_focus.call_deferred()
	else:
		primero.grab_focus.call_deferred()
	visible = true


func _mostrar(id_ficha: String) -> void:
	for hijo in _detalle.get_children():
		_detalle.remove_child(hijo)
		hijo.queue_free()
	var f := Juego.ficha(id_ficha)
	if f.is_empty():
		var vacio := Estilo.texto("Todavía no hay fichas. Los datos reales aparecen al explorar, al hablar con Órbita y al resolver cada reto.", 20, Estilo.TINTA_SUAVE, 500)
		vacio.custom_minimum_size = Vector2(560, 0)
		_detalle.add_child(vacio)
		return
	_detalle.add_child(Estilo.texto(String(f.get("categoria", "")).to_upper(), 14, Estilo.PETROLEO, 700))
	var titulo := Estilo.texto(f.get("titulo", ""), 30, Estilo.TINTA, 700)
	titulo.custom_minimum_size = Vector2(560, 0)
	_detalle.add_child(titulo)
	var texto := Estilo.texto(f.get("texto", ""), 22, Estilo.TINTA, 500)
	texto.custom_minimum_size = Vector2(560, 0)
	_detalle.add_child(texto)
	var fuente := Estilo.texto("Fuente: %s" % f.get("fuente", ""), 16, Estilo.TINTA_SUAVE, 500)
	fuente.custom_minimum_size = Vector2(560, 0)
	_detalle.add_child(fuente)
	var sello := Estilo.texto(f.get("sello", ""), 22, Estilo.CORAL, 700, true)
	sello.rotation = deg_to_rad(-3.0)
	_detalle.add_child(sello)


func cerrar() -> void:
	if visible:
		visible = false
		Audio.sonar("pagina")
		cerrado.emit()
