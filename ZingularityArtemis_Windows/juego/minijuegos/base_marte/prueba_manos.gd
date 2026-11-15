extends Node

# Prueba con manos de «Base en Marte»: abre el libro y juega solo con teclas y clics fisicos
# (Input.parse_input_event), como una persona: programa el aterrizaje con el teclado, cambia un valor con el
# raton, aterriza, camina, salta, abre y cierra el cuaderno con Tab y sale del libro con Esc.
# Uso: --prueba=guion:res://minijuegos/base_marte/prueba_manos.gd   (con --capturas=<carpeta> guarda imagenes)

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
	pruebas.comprobar(m != null and Interfaz.anfitrion.visible, "base_marte.manos.abierto")
	if m == null:
		Juego.modo_prueba = true
		return
	pruebas.comprobar(m.size == Vector2(1280, 720), "base_marte.manos.pantalla_completa", str(m.size))
	await _foto("01_tarjeta_del_libro")
	await _toque(KEY_ENTER)
	await _real(0.6)
	var n = m.get("nivel")
	pruebas.comprobar(n != null and n.aterrizaje != null, "base_marte.manos.empieza_en_el_aterrizaje")
	var a = n.aterrizaje
	await _foto("02_programa_dentro_del_juego")
	# teclado: paracaidas 18 -> 11 km, cohetes 0,6 -> 2,1 km, navegacion: si
	for i in 7:
		await _toque(KEY_LEFT)
	await _toque(KEY_DOWN)
	for i in 15:
		await _toque(KEY_RIGHT)
	await _toque(KEY_DOWN)
	await _toque(KEY_RIGHT)
	pruebas.comprobar(is_equal_approx(a.alt_paracaidas, 11.0) and is_equal_approx(a.alt_cohetes, 2.1) and a.navegacion, "base_marte.manos.programa_con_teclado", "%s %s %s" % [a.alt_paracaidas, a.alt_cohetes, a.navegacion])
	# raton: la flecha derecha del paracaidas sube a 12 km y la izquierda lo devuelve a 11
	await _clic(m, (a._rects["mas0"] as Rect2).get_center())
	var con_clic: float = a.alt_paracaidas
	await _clic(m, (a._rects["menos0"] as Rect2).get_center())
	pruebas.comprobar(is_equal_approx(con_clic, 12.0) and is_equal_approx(a.alt_paracaidas, 11.0), "base_marte.manos.flechas_con_raton", "%s %s" % [con_clic, a.alt_paracaidas])
	await _toque(KEY_ENTER)
	await _real(6.5)
	await _foto("03_paracaidas")
	limite = 40.0
	while a.estado == "descenso" and limite > 0.0:
		await _real(0.2)
		limite -= 0.2
	await _real(0.6)
	pruebas.comprobar(a.resultado == "suave", "base_marte.manos.aterrizaje_suave", a.resultado)
	# la primera nota abre el cuaderno solo: Tab lo cierra
	if n.cuaderno.abierto:
		await _foto("04_cuaderno")
		await _toque(KEY_TAB)
	pruebas.comprobar(not n.cuaderno.abierto, "base_marte.manos.tab_cierra_el_cuaderno")
	await _toque(KEY_ENTER)
	limite = 30.0
	while n.bajando and limite > 0.0:
		await _real(0.2)
		limite -= 0.2
	await _real(2.5)
	await _foto("05_bajan_de_la_nave")
	pruebas.comprobar(not n.bajando and n.etapa == "banderas", "base_marte.manos.en_la_superficie", n.etapa)
	var x0: float = n.jugador.position.x
	_tecla(KEY_D, true)
	await _real(1.5)
	_tecla(KEY_D, false)
	pruebas.comprobar(n.jugador.position.x > x0 + 40.0, "base_marte.manos.camina_con_D", "%s -> %s" % [x0, n.jugador.position.x])
	await _toque(KEY_SPACE)
	await _real(0.1)
	pruebas.comprobar(not n.en_suelo, "base_marte.manos.salta_con_espacio")
	await _real(1.2)
	await _foto("06_superficie")
	# Esc es del anfitrion: sale del libro y el juego principal sigue sin pausa
	await _toque(KEY_ESCAPE)
	await _real(0.6)
	pruebas.comprobar(devuelto and not Interfaz.anfitrion.visible, "base_marte.manos.esc_sale_del_libro", str(final))
	pruebas.comprobar(not get_tree().paused, "base_marte.manos.arbol_sin_pausa", str(get_tree().paused))
	Juego.modo_prueba = true


func _lanzar() -> void:
	final = await Interfaz.abrir_minijuego("base_marte", {"dificultad": 1})
	devuelto = true


func _foto(nombre: String) -> void:
	if carpeta == "" or DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(carpeta.path_join(nombre + ".png"))


func _clic(m: Control, p: Vector2) -> void:
	# p en pixeles del capitulo (640 x 360); en el juego principal (1280 x 720) es el doble, desde la esquina
	# del minijuego. El evento entra por la ventana principal como un clic de verdad (push_input).
	var pantalla: Vector2 = m.get_global_rect().position + p * 2.0
	var mov := InputEventMouseMotion.new()
	mov.position = pantalla
	mov.global_position = pantalla
	get_viewport().push_input(mov, true)
	await get_tree().process_frame
	for abajo in [true, false]:
		var b := InputEventMouseButton.new()
		b.button_index = MOUSE_BUTTON_LEFT
		b.pressed = abajo
		b.position = pantalla
		b.global_position = pantalla
		get_viewport().push_input(b, true)
		await get_tree().process_frame
	await get_tree().process_frame


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
