extends Node

# Regresiones del modelo y de las rutas de entrada, sin modificar el nucleo.
const Minijuego = preload("res://minijuegos/linea_tiempo/linea_tiempo.gd")
var _resultado: Dictionary = {}


func _crear(nivel: int) -> Control:
	var juego: Control = Minijuego.new()
	add_child(juego)
	juego.preparar({"dificultad": nivel}, {})
	juego.terminado.connect(func(r: Dictionary): _resultado = r)
	_resultado = {}
	juego.empezar()
	return juego


func _accion(juego: Control, nombre: String) -> void:
	var evento: InputEventAction = InputEventAction.new()
	evento.action = nombre
	evento.pressed = true
	juego._input(evento)


func correr(pruebas: Node) -> void:
	for nivel in [1, 2, 3]:
		var juego: Control = _crear(nivel)
		var cantidad: int = [5, 7, 9][nivel - 1]
		pruebas.comprobar(juego.orden.size() == cantidad, "linea.n%d.cantidad" % nivel)
		var fechas_ocultas: bool = true
		for etiqueta in juego._fechas:
			fechas_ocultas = fechas_ocultas and etiqueta.text == "Fecha oculta"
		pruebas.comprobar(fechas_ocultas, "linea.n%d.fechas_ocultas" % nivel)
		juego._comprobar()
		var marcas_validas: bool = true
		for i in juego.orden.size():
			var local: bool = (i == 0 or juego.orden[i - 1] < juego.orden[i]) and (i == juego.orden.size() - 1 or juego.orden[i] < juego.orden[i + 1])
			marcas_validas = marcas_validas and juego._marcas[i] == local
		pruebas.comprobar(marcas_validas, "linea.n%d.marcas_vecinas" % nivel)
		# Resuelve por la ruta de acciones de teclado, una permuta adyacente cada vez.
		for pasada in cantidad:
			for i in range(cantidad - 1):
				if juego.orden[i] > juego.orden[i + 1]:
					juego.seleccion = i + 1
					_accion(juego, "interactuar")
					_accion(juego, "mover_izquierda")
					_accion(juego, "interactuar")
		pruebas.comprobar(juego.comprobaciones == 1, "linea.n%d.mover_no_gasta" % nivel)
		_accion(juego, "saltar")
		pruebas.comprobar(bool(_resultado.get("superado", false)), "linea.n%d.teclado_gana" % nivel)
		juego.free()
		# El arrastre cruza varios huecos y conserva todas las tarjetas.
		juego = _crear(nivel)
		var inicial: Array = juego.orden.duplicate()
		var pulsar: InputEventMouseButton = InputEventMouseButton.new()
		pulsar.button_index = MOUSE_BUTTON_LEFT
		pulsar.pressed = true
		pulsar.position = juego._rect_tarjeta(0).get_center()
		juego._gui_input(pulsar)
		var arrastrar: InputEventMouseMotion = InputEventMouseMotion.new()
		arrastrar.button_mask = MOUSE_BUTTON_MASK_LEFT
		arrastrar.position = juego._rect_tarjeta(cantidad - 1).get_center()
		juego._gui_input(arrastrar)
		pulsar.pressed = false
		pulsar.position = arrastrar.position
		juego._gui_input(pulsar)
		pruebas.comprobar(juego.orden.back() == inicial.front() and juego.orden.size() == cantidad and not juego.tomada, "linea.n%d.arrastre" % nivel)
		juego.free()
		for acierta in [true, false]:
			juego = _crear(nivel)
			juego.jugar_solo(acierta)
			for cuadro in 799:
				if not juego.activo:
					break
				juego._process(0.05)
			pruebas.comprobar(not juego.activo and bool(_resultado.get("superado", not acierta)) == acierta and juego.tiempo < 40.0, "linea.n%d.auto_%s_menos_40s" % [nivel, str(acierta)])
			print("LINEA_AUTO nivel=%d acierta=%s segundos=%.2f comprobaciones=%d" % [nivel, str(acierta), juego.tiempo, juego.comprobaciones])
			juego.free()
	# Captura reproducible de la dificultad mayor, con pistas y una tarjeta tomada.
	var vista: Control = _crear(3)
	vista.position = Vector2(80, 100)
	vista._comprobar()
	vista.seleccion = 2
	vista.tomada = true
	vista._refrescar()
	await get_tree().process_frame
	await get_tree().process_frame
	var cabe: bool = true
	for i in vista.orden.size():
		cabe = cabe and vista._titulos[i].size.y <= 104.0 and vista._pistas[i].size.y <= 100.0
	pruebas.comprobar(cabe and vista._detalle.size.y <= 56.0, "linea.textos_caben_nivel3")
	if DisplayServer.get_name() != "headless":
		var ruta: String = ProjectSettings.globalize_path("res://../Nasa_Game/Construccion/Minijuegos/linea_tiempo/captura_nivel3.png")
		var error: Error = get_viewport().get_texture().get_image().save_png(ruta)
		pruebas.comprobar(error == OK, "linea.captura")
	vista.free()
