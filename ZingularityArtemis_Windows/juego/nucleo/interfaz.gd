extends CanvasLayer

# Interfaz global (autoload "Interfaz"): HUD, dialogos, avisos, ventana de carga, pausa, cuaderno, menu
# principal y anfitrion de minijuegos. Las zonas y los minijuegos solo usan las funciones de este guion.
# ESTILO PROVISIONAL: la Fase 7 (UI/UX) no esta validada.
#
#   await Interfaz.decir([{"quien": "Órbita", "texto": "..."}])       dialogo
#   var i: int = await Interfaz.elegir("¿...?", ["Sí", "No"])          pregunta con opciones
#   Interfaz.aviso("Texto corto", 3.0)                                 aviso que se va solo
#   var r: Dictionary = await Interfaz.abrir_minijuego("seguidor", {"dificultad": 1})
#        r = {"superado": bool, "puntos": float, "detalle": String, "abandonado": bool (si salio)}

const Estilo := preload("res://interfaz/estilo.gd")
const Recursos := preload("res://nucleo/recursos.gd")
const Hud := preload("res://interfaz/hud.gd")
const Dialogo := preload("res://interfaz/dialogo.gd")
const VentanaCarga := preload("res://interfaz/ventana_carga.gd")
const Anfitrion := preload("res://interfaz/anfitrion.gd")
const Pausa := preload("res://interfaz/pausa.gd")
const Cuaderno := preload("res://interfaz/cuaderno.gd")
const Menu := preload("res://interfaz/menu.gd")
const Mapa := preload("res://interfaz/mapa.gd")

var raiz: Control
var hud: Control
var dialogo: Control
var carga: Control
var anfitrion: Control
var pausa: Control
var cuaderno: Control
var menu: Control
var mapa: Control
var velo: ColorRect
var _pausa_previa := false
var _ocupada_hasta := 0
var _mapa_desde_menu := false
var _hablando := false


func _ready() -> void:
	layer = 10
	process_mode = Node.PROCESS_MODE_ALWAYS
	raiz = Control.new()
	raiz.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	raiz.mouse_filter = Control.MOUSE_FILTER_IGNORE
	raiz.theme = Estilo.tema()
	add_child(raiz)
	hud = Hud.new()
	dialogo = Dialogo.new()
	cuaderno = Cuaderno.new()
	pausa = Pausa.new()
	menu = Menu.new()
	mapa = Mapa.new()
	anfitrion = Anfitrion.new()
	carga = VentanaCarga.new()
	for nodo in [hud, dialogo, cuaderno, pausa, menu, mapa, anfitrion, carga]:
		raiz.add_child(nodo)
	hud.visible = false
	velo = ColorRect.new()
	velo.color = Color("12181b")
	velo.modulate.a = 0.0
	velo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	velo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	raiz.add_child(velo)
	pausa.accion.connect(_accion_pausa)
	cuaderno.cerrado.connect(_cuaderno_cerrado)
	menu.elegido.connect(_accion_menu)
	mapa.cerrado.connect(_mapa_cerrado)
	mapa.viajar.connect(_mapa_viajar)


func _abierta() -> bool:
	return _hablando or dialogo.visible or anfitrion.visible or pausa.visible or cuaderno.visible or menu.visible or carga.visible or mapa.visible


func _process(_delta: float) -> void:
	if _abierta():
		_ocupada_hasta = Time.get_ticks_msec() + 300


func ocupada() -> bool:
	# true mientras haya algo abierto que bloquea a la protagonista, y 0,3 s mas: asi la pulsacion que
	# cierra un dialogo o un minijuego (E o Intro) no vuelve a usar el objeto que esta al lado
	return _abierta() or Time.get_ticks_msec() < _ocupada_hasta


# ------------------------------------------------------------------ dialogos y avisos

func decir(lineas: Variant, quien: String = "") -> void:
	while _hablando:
		await get_tree().process_frame
	_hablando = true
	await dialogo.decir(lineas, quien)
	_hablando = false


func elegir(pregunta: Variant, opciones: Array) -> int:
	while _hablando:
		await get_tree().process_frame
	_hablando = true
	var indice: int = await dialogo.elegir(pregunta, opciones)
	_hablando = false
	return indice


func aviso(texto: String, segundos: float = 3.0) -> void:
	if hud != null:
		hud.aviso(texto, segundos)


func indicar(texto: String) -> void:
	hud.indicar(texto)


func rotular(origen: Object, texto: String) -> void:
	hud.rotular(origen, texto)


func limpiar_rotulos() -> void:
	hud.limpiar_rotulos()


func mostrar_hud(ver: bool) -> void:
	hud.visible = ver


func anunciar_zona(meta: Dictionary) -> void:
	hud.anunciar_zona(meta)


# ------------------------------------------------------------------ carga y fundidos

func mostrar_carga(meta: Dictionary) -> void:
	await carga.mostrar(meta)


func ocultar_carga() -> void:
	await carga.ocultar()


func fundido(a_oscuro: bool, segundos: float = 0.4) -> void:
	var meta_alfa := 1.0 if a_oscuro else 0.0
	if Juego.modo_prueba:
		velo.modulate.a = meta_alfa
		await get_tree().process_frame
		return
	var t := velo.create_tween()
	t.tween_property(velo, "modulate:a", meta_alfa, segundos)
	await t.finished


# ------------------------------------------------------------------ minijuegos

func abrir_minijuego(id: String, parametros: Dictionary = {}) -> Dictionary:
	if not FileAccess.file_exists("res://minijuegos/%s/%s.gd" % [id, id]):
		# todavia no esta construido: no bloquea la historia, pero queda avisado
		print("AVISO minijuego en construccion: ", id)
		aviso("El reto «%s» todavía está en construcción." % id, 3.0)
		return {"superado": true, "puntos": 0.0, "detalle": "", "en_construccion": true}
	var estaba_en_pausa := get_tree().paused
	get_tree().paused = true
	var resultado: Dictionary = await anfitrion.jugar(id, parametros)
	get_tree().paused = estaba_en_pausa
	Juego.registrar_minijuego(id, resultado)
	return resultado


# ------------------------------------------------------------------ menu, pausa y cuaderno

func abrir_menu() -> void:
	mostrar_hud(false)
	menu.abrir()


func _en_juego() -> bool:
	return Zonas.actual != null and not Zonas.ocupado


func _input(evento: InputEvent) -> void:
	if evento is InputEventKey and evento.pressed and not evento.echo:
		if evento.keycode == KEY_F11:
			var modo := DisplayServer.window_get_mode()
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if modo == DisplayServer.WINDOW_MODE_FULLSCREEN else DisplayServer.WINDOW_MODE_FULLSCREEN)
			return
		if evento.keycode == KEY_F12:
			capturar("res://capturas/captura_%d.png" % int(Time.get_unix_time_from_system()))
			return
	if anfitrion.visible or carga.visible or mapa.visible:
		return
	if menu.visible:
		return
	if evento.is_action_pressed("mapa") and _en_juego() and not ocupada():
		abrir_mapa(false)
		get_viewport().set_input_as_handled()
		return
	if evento.is_action_pressed("pausa"):
		if pausa.visible:
			_accion_pausa("continuar")
		elif cuaderno.visible:
			cuaderno.cerrar()
		elif _en_juego() and not ocupada():
			_abrir_pausa()
		else:
			return
		get_viewport().set_input_as_handled()
	elif evento.is_action_pressed("cuaderno"):
		if cuaderno.visible:
			cuaderno.cerrar()
		elif _en_juego() and not ocupada():
			abrir_cuaderno()
		else:
			return
		get_viewport().set_input_as_handled()


func _abrir_pausa() -> void:
	_pausa_previa = get_tree().paused
	get_tree().paused = true
	var opciones: Array = [["Continuar", "continuar"], ["Mapa", "mapa"], ["Cuaderno", "cuaderno"]]
	if Zonas.actual != null and Zonas.actual.has_method("despertar"):
		opciones.append(["Despertar", "despertar"])
	opciones.append(["Menú principal", "menu"])
	opciones.append(["Salir del juego", "salir"])
	pausa.abrir(opciones)


func _accion_pausa(nombre: String) -> void:
	pausa.cerrar()
	match nombre:
		"cuaderno":
			cuaderno.abrir()
		"mapa":
			_mapa_desde_menu = false
			mapa.abrir(false)
		"despertar":
			get_tree().paused = false
			Zonas.actual.call("despertar")
		"menu":
			get_tree().paused = false
			Juego.guardar()
			Zonas.cerrar()
			abrir_menu()
		"salir":
			Juego.guardar()
			salir()
		_:
			get_tree().paused = _pausa_previa


func abrir_cuaderno() -> void:
	_pausa_previa = get_tree().paused
	get_tree().paused = true
	Audio.sonar("pagina")
	cuaderno.abrir()


func _cuaderno_cerrado() -> void:
	get_tree().paused = _pausa_previa


func abrir_mapa(viaje: bool = false) -> void:
	# el mapa del mundo: lugares, conexiones y donde esta la protagonista
	_mapa_desde_menu = menu.visible
	if not _mapa_desde_menu:
		_pausa_previa = get_tree().paused
		get_tree().paused = true
	Audio.sonar("pagina")
	mapa.abrir(viaje)


func _mapa_cerrado() -> void:
	if not _mapa_desde_menu:
		get_tree().paused = _pausa_previa


func _mapa_viajar(id_zona: String) -> void:
	if _mapa_desde_menu:
		# visita libre desde el menu principal: todo abierto, para recorrer y validar cada escenario
		Juego.nueva_partida()
		Juego.poner_bandera("visita_libre")
		menu.cerrar()
	else:
		get_tree().paused = _pausa_previa
	Zonas.ir_a(id_zona, "inicio")


func _accion_menu(accion: String, dato: String) -> void:
	match accion:
		"nueva":
			Juego.nueva_partida()
			menu.cerrar()
			Zonas.ir_a(_zona_inicial(), "inicio")
		"continuar":
			if not Juego.cargar():
				Juego.nueva_partida()
			menu.cerrar()
			var zona: String = Juego.estado.get("zona", _zona_inicial())
			if not Zonas.existe(zona):
				zona = _zona_inicial()
			Zonas.ir_a(zona, Juego.estado.get("entrada", "inicio"))
		"minijuegos":
			menu.mostrar_minijuegos()
		"lugares":
			menu.mostrar_lugares()
		"mapa":
			abrir_mapa(true)
		"inicio":
			menu.mostrar_inicio()
		"minijuego":
			await abrir_minijuego(dato, {"dificultad": 1, "desde_menu": true})
			menu.mostrar_minijuegos()
		"lugar":
			# visita libre: los umbrales con requisito quedan abiertos para poder validar cada escenario
			Juego.nueva_partida()
			Juego.poner_bandera("visita_libre")
			menu.cerrar()
			Zonas.ir_a(dato, "inicio")
		"salir":
			salir()


func _zona_inicial() -> String:
	if Zonas.existe("habitacion"):
		return "habitacion"
	var lista := Zonas.catalogo(true)
	return lista[0]["id"] if not lista.is_empty() else ""


func capturar(ruta: String) -> void:
	await RenderingServer.frame_post_draw
	var imagen := get_viewport().get_texture().get_image()
	var destino := ProjectSettings.globalize_path(ruta) if ruta.begins_with("res://") else ruta
	imagen.save_png(destino)
	print("CAPTURA_OK ", destino)


func salir() -> void:
	print("FIN")
	Recursos.liberar()
	get_tree().quit()
