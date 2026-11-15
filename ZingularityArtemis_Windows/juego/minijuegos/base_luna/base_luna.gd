extends "res://nucleo/minijuego.gd"

# «Base en la Luna»: el libro de la Luna de la biblioteca del pueblo (Zingularity: Artemis).
# Envuelve el capitulo 2D de Jean y Joel (codigo/nivel_luna.gd: la base del polo sur lunar y el cohete) y su
# viaje animado (codigo/viaje.gd) en una SubViewport de 640 x 360 ampliada al doble (pantalla completa).
# El juego del equipo no se modifica: al despegar pasa al viaje y, al llegar, el libro termina superado.
# Esc lo maneja el anfitrion (salir del libro).

const Luna := preload("res://minijuegos/base_luna/codigo/nivel_luna.gd")
const Viaje := preload("res://minijuegos/base_luna/codigo/viaje.gd")

var nivel                 # el capitulo de la Luna mientras dura
var viaje                 # la animacion del viaje a Marte
var resumen := {}
var _vista: SubViewport
var _auto := 0
var _t_auto := 0.0
var _acierta := true


func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	var marco := SubViewportContainer.new()
	marco.stretch = true
	marco.stretch_shrink = 2
	marco.size = size
	marco.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	marco.focus_mode = Control.FOCUS_NONE
	add_child(marco)
	_vista = SubViewport.new()
	_vista.size = Vector2i(640, 360)
	_vista.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	_vista.handle_input_locally = true
	marco.add_child(_vista)


func _empezar() -> void:
	nivel = Luna.new()
	if _solo != 0:
		nivel.control_externo = true
		nivel.eventos_auto = false
	nivel.despegue.connect(_al_despegar)
	_vista.add_child(nivel)


func _al_despegar(r: Dictionary) -> void:
	resumen = r
	_cambiar_a_viaje.call_deferred()


func _cambiar_a_viaje() -> void:
	if nivel != null:
		nivel.queue_free()
		nivel = null
	viaje = Viaje.new()
	viaje.llegada.connect(_al_llegar)
	_vista.add_child(viaje)


func _al_llegar() -> void:
	var rescates: int = int(resumen.get("rescates", 0))
	var puntos := clampf(100.0 - 15.0 * rescates, 40.0, 100.0)
	terminar(true, puntos, "¡El cohete despegó del polo sur lunar rumbo a Marte! El libro de Marte continúa la historia.")


# ------------------------------------------------------------------ juego automatico para las pruebas

func jugar_solo(acierta: bool) -> void:
	_acierta = acierta
	_auto = 1
	_t_auto = 0.0


func _paso(delta: float) -> void:
	if _auto == 0 or nivel == null:
		return
	_t_auto += delta
	var l = nivel
	for k in l.barras:
		l.barras[k] = 0.0 if k == "radiacion" else 100.0
	if _t_auto < 1.0:
		return
	match _auto:
		1:
			if not _acierta:
				terminar(false, 0.0, "El cohete no pudo despegar: le faltaba combustible. En el polo sur lunar ese combustible sale del hielo de los cráteres en sombra.")
				return
			# atajo de prueba: cohete armado (4 fases), tanque lleno y bateria cargada
			l.fase = 4
			l.combustible = 100.0
			l.bateria = 100.0
			var s: Sprite2D = l.cohete["nodo"]
			s.texture = load("res://minijuegos/base_luna/recursos/props/cohete_4.png")
			l.teletransportar(l.cohete["x"])
			_auto = 2
		2:
			if l.listo_para_despegar():
				l.cerca = l.cohete
				l.interactuar()
				_auto = 3
