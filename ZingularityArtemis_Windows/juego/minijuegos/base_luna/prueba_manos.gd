extends Node

# Prueba con manos de «Base en la Luna»: abre el libro y lo juega con teclas fisicas (Input.parse_input_event):
# empieza con Intro, camina con D, corre con Mayus, salta con Espacio y sale del libro con Esc.
# Uso: --prueba=guion:res://minijuegos/base_luna/prueba_manos.gd   (con --capturas=<carpeta> guarda imagenes)

var pulsadas: Dictionary = {}
var final: Dictionary = {}
var devuelto := false
var carpeta := ""


func correr(pruebas: Node) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	carpeta = String(Juego.args.get("capturas", ""))
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = false
	_lanzar()
	var limite := 5.0
	while not Interfaz.anfitrion.visible and limite > 0.0:
		await _real(0.1)
		limite -= 0.1
	await _real(0.3)
	var m: Control = Interfaz.anfitrion.get("_minijuego")
	pruebas.comprobar(m != null and Interfaz.anfitrion.visible, "base_luna.manos.abierto")
	if m == null:
		Juego.modo_prueba = true
		return
	pruebas.comprobar(m.size == Vector2(1280, 720), "base_luna.manos.pantalla_completa", str(m.size))
	await _foto("L1_tarjeta_del_libro")
	await _toque(KEY_ENTER)
	await _real(1.0)
	var l = m.get("nivel")
	pruebas.comprobar(l != null and l.objetos.size() >= 30, "base_luna.manos.carga_la_base")
	await _foto("L2_base_lunar")
	var x0: float = l.jugador.position.x
	_tecla(KEY_D, true)
	await _real(1.2)
	_tecla(KEY_SHIFT, true)
	await _real(0.8)
	_tecla(KEY_SHIFT, false)
	_tecla(KEY_D, false)
	pruebas.comprobar(l.jugador.position.x > x0 + 60.0, "base_luna.manos.camina_y_corre", "%s -> %s" % [x0, l.jugador.position.x])
	await _toque(KEY_SPACE)
	await _real(0.2)
	pruebas.comprobar(not l.en_suelo, "base_luna.manos.salta")
	await _foto("L3_salto_lunar")
	await _real(2.5)
	await _toque(KEY_ESCAPE)
	await _real(0.6)
	pruebas.comprobar(devuelto and not Interfaz.anfitrion.visible, "base_luna.manos.esc_sale_del_libro", str(final))
	pruebas.comprobar(not get_tree().paused, "base_luna.manos.arbol_sin_pausa", str(get_tree().paused))
	Juego.modo_prueba = true


func _lanzar() -> void:
	final = await Interfaz.abrir_minijuego("base_luna", {"dificultad": 1})
	devuelto = true


func _foto(nombre: String) -> void:
	if carpeta == "" or DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(carpeta.path_join(nombre + ".png"))


func _tecla(codigo: int, abajo: bool) -> void:
	if bool(pulsadas.get(codigo, false)) == abajo:
		return
	pulsadas[codigo] = abajo
	var evento := InputEventKey.new()
	evento.physical_keycode = codigo
	evento.keycode = codigo
	evento.pressed = abajo
	Input.parse_input_event(evento)


func _toque(codigo: int) -> void:
	_tecla(codigo, true)
	await get_tree().process_frame
	await get_tree().physics_frame
	await get_tree().process_frame
	_tecla(codigo, false)
	await get_tree().process_frame


func _real(segundos: float) -> void:
	await get_tree().create_timer(segundos, true, false, true).timeout
