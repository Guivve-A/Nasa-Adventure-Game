extends "res://nucleo/minijuego.gd"

# «Base en Marte»: el libro de Marte de la biblioteca del pueblo (Zingularity: Artemis).
# Envuelve el capitulo 2D de Marte de Domenica (codigo/nivel_marte.gd, 640 x 360 pixeles) en una
# SubViewport ampliada al doble: ocupa toda la pantalla (pantalla_completa) como los otros minijuegos.
# El capitulo trae su propio HUD, cuaderno de campo y controles; al enviar el reporte a la Tierra termina
# y el anfitrion muestra el resultado. Esc lo maneja el anfitrion (salir del libro).

const Nivel := preload("res://minijuegos/base_marte/codigo/nivel_marte.gd")

var nivel
var _vista: SubViewport
var _auto := 0              # paso del juego automatico (pruebas)
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
	_vista.audio_listener_enable_2d = true
	marco.add_child(_vista)


func _empezar() -> void:
	nivel = Nivel.new()
	nivel.saltar_aterrizaje = _solo != 0           # en las pruebas automaticas empieza ya aterrizado
	nivel.terminado.connect(_al_terminar)
	_vista.add_child(nivel)
	# cada nota del cuaderno de Marte tambien se anota en el cuaderno del juego, si su ficha existe
	nivel.cuaderno.nueva.connect(func(id): if not Juego.ficha("marte_" + str(id)).is_empty(): Juego.anotar("marte_" + str(id)))
	if _solo != 0:
		nivel.cuaderno.auto_abrir = false


func _input(evento: InputEvent) -> void:
	# Tab es del cuaderno de Marte: si no, el juego principal lo usa para mover el foco entre botones
	var tecla := evento as InputEventKey
	if tecla != null and tecla.pressed and not tecla.echo and tecla.keycode == KEY_TAB and nivel != null and activo:
		if nivel.cuaderno.abierto:
			nivel.cuaderno.cerrar()
		else:
			nivel.cuaderno.abrir()
		get_viewport().set_input_as_handled()


func _al_terminar() -> void:
	var notas: int = nivel.cuaderno.paginas.size()
	var total: int = nivel.cuaderno.total()
	var puntos := 100.0 * notas / maxf(1.0, total)
	terminar(true, puntos, "Aterrizaste, levantaste la base y el primer reporte llegó a la Tierra. Cuaderno: %d de %d notas." % [notas, total])


# ------------------------------------------------------------------ juego automatico para las pruebas

func jugar_solo(acierta: bool) -> void:
	_acierta = acierta
	_auto = 1
	_t_auto = 0.0
	if nivel != null:
		nivel.control_externo = true


func _paso(delta: float) -> void:
	if _auto == 0 or nivel == null:
		return
	_t_auto += delta
	var m = nivel
	if m.etapa == "llegada" or m.bajando:
		return
	for k in m.barras:
		m.barras[k] = 0.0 if k == "radiacion" else 100.0
	match _auto:
		1:
			if not _acierta:
				terminar(false, 0.0, "Sin levantar el hábitat ni el extractor, el oxígeno del traje se acabó: en Marte el aire es casi todo dióxido de carbono.")
				return
			for o in m.objetos:
				if o["tipo"] == "bandera" and not o["hecho"]:
					m.teletransportar(o["x"])
					m.interactuar()
			_auto = 2
		2:
			for id in ["cupula", "paneles", "extractor", "taladro", "invernadero"]:
				var o = m._buscar(id)
				if not o["hecho"]:
					m.teletransportar(o["x"])
					for i in 4:
						m.mantener(0.4)
			if m.modulos >= 5:
				m.iniciar_tormenta(0.0)
				_auto = 3
		3:
			m.polvo_paneles = 0.0
			m.t_tormenta = 0.0
			if m.etapa == "noche":
				m.teletransportar(m.X_ANTENA)
				for i in 4:
					m.mantener(0.4)
				_auto = 4
		4:
			if m.antena_lista and m.etapa == "noche":
				m.interactuar()
			elif m.etapa == "reporte":
				m.elegir_reporte(int(m.datos["reporte"]["correcta"]))
				m.interactuar()
				m.interactuar()
				_auto = 5
