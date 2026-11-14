extends Control

# Menu de pausa (Esc): continuar, cuaderno, despertar (solo en el sueno), volver al menu y salir.
# Estilo provisional (Fase 7 sin validar).

signal accion(nombre: String)

const Estilo := preload("res://interfaz/estilo.gd")

var _panel: PanelContainer
var _botones: VBoxContainer


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var velo := ColorRect.new()
	velo.color = Color(Estilo.NOCHE, 0.72)
	velo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(velo)
	_panel = Estilo.panel(Estilo.PAPEL, 16, 4, 26)
	add_child(_panel)
	_botones = VBoxContainer.new()
	_botones.add_theme_constant_override("separation", 10)
	_panel.add_child(_botones)


func _process(_delta: float) -> void:
	if visible:
		_panel.reset_size()
		_panel.position = (size - _panel.size) * 0.5


func abrir(opciones: Array) -> void:
	# opciones: [["Texto del boton", "accion"], ...]
	for hijo in _botones.get_children():
		_botones.remove_child(hijo)
		hijo.queue_free()
	_botones.add_child(Estilo.texto("Pausa", 32, Estilo.TINTA, 700))
	var objetivo := Juego.objetivo()
	if objetivo != "":
		var l := Estilo.texto("Objetivo: %s" % objetivo, 18, Estilo.TINTA_SUAVE, 500)
		l.custom_minimum_size = Vector2(380, 0)
		_botones.add_child(l)
	var primero: Button = null
	for par in opciones:
		var b := Estilo.boton(par[0], 22, primero == null)
		b.custom_minimum_size = Vector2(380, 50)
		var nombre: String = par[1]
		b.pressed.connect(func(): accion.emit(nombre))
		_botones.add_child(b)
		if primero == null:
			primero = b
	visible = true
	_panel.reset_size()
	if primero != null:
		primero.grab_focus.call_deferred()


func cerrar() -> void:
	visible = false
