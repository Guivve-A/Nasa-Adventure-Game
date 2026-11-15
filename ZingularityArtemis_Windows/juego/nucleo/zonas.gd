extends Node

# Gestor de zonas (autoload "Zonas"): el mundo es un conjunto de zonas enlazadas por umbrales. Cambiar de zona
# abre la ventana de carga (pagina del cuaderno con el lugar y un dato real), libera la zona anterior, arma la
# nueva y coloca a la protagonista en la entrada pedida.
#
# IMPORTANTE para las zonas: Zonas.ir_a(...) se llama SIN await y como ultima instruccion. La zona que llama se
# libera durante el cambio; lo que deba pasar despues va en al_entrar() de la zona de destino.

signal zona_cambiada(id: String)

const Materiales := preload("res://nucleo/materiales.gd")
const Recursos := preload("res://nucleo/recursos.gd")
const Jugador := preload("res://nucleo/jugador.gd")
const Companero := preload("res://nucleo/companero.gd")
const Camara := preload("res://nucleo/camara_juego.gd")

const CARGA_MINIMA_MS := 1500

var mundo: Node3D
var actual: Node3D = null
var id_actual := ""
var jugador: CharacterBody3D = null
var companero: Node3D = null
var camara: Camera3D = null
var ocupado := false
var ultima_carga_ms := 0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	mundo = Node3D.new()
	mundo.name = "Mundo"
	mundo.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(mundo)


func info(id: String) -> Dictionary:
	var d: Variant = Juego.leer_json("res://zonas/%s/zona.json" % id)
	if d is Dictionary:
		d["id"] = id
		return d
	return {"id": id, "nombre": id}


func catalogo(con_ocultas: bool = false) -> Array:
	var lista: Array = []
	for carpeta in DirAccess.get_directories_at("res://zonas"):
		if not FileAccess.file_exists("res://zonas/%s/%s.gd" % [carpeta, carpeta]):
			continue
		var d := info(carpeta)
		if d.get("oculta", false) and not con_ocultas:
			continue
		lista.append(d)
	lista.sort_custom(func(a, b): return float(a.get("orden", 99)) < float(b.get("orden", 99)))
	return lista


func existe(id: String) -> bool:
	return FileAccess.file_exists("res://zonas/%s/%s.gd" % [id, id])


func ir_a(id: String, entrada: String = "inicio", opciones: Dictionary = {}) -> bool:
	# opciones: {"sin_carga": true} cambia con un fundido corto, sin la ventana de carga
	if ocupado:
		return false
	if not existe(id):
		Interfaz.aviso("Ese lugar todavía no está construido (%s)." % id, 3.0)
		print("AVISO zona inexistente: ", id)
		return false
	ocupado = true
	if id == id_actual and actual != null and is_instance_valid(actual):
		# otra entrada de la misma zona: fundido corto, sin recargar
		get_tree().paused = true
		await Interfaz.fundido(true, 0.25)
		_colocar(actual, entrada)
		await get_tree().process_frame
		await Interfaz.fundido(false, 0.25)
		get_tree().paused = false
		ocupado = false
		actual.al_entrar(entrada)
		return true
	var meta := info(id)
	var inicio := Time.get_ticks_msec()
	get_tree().paused = true
	Interfaz.limpiar_rotulos()
	if opciones.get("sin_carga", false):
		await Interfaz.fundido(true, 0.3)
	else:
		await Interfaz.mostrar_carga(meta)
	_soltar_zona()
	await get_tree().process_frame
	var guion: Variant = load("res://zonas/%s/%s.gd" % [id, id])
	var zona: Node3D = guion.new()
	zona.set("id", id)
	zona.set("meta", meta)
	zona.set("carpeta", "res://zonas/%s" % id)
	zona.name = "Zona_%s" % id
	actual = zona
	id_actual = id
	mundo.add_child(zona)          # aqui corre _construir()
	_preparar_actores(zona)
	await get_tree().process_frame
	await get_tree().physics_frame
	_colocar(zona, entrada)
	Materiales.ajustar_parametro("inclinacion", float(zona.get("cizalla")))
	Juego.estado["zona"] = id
	Juego.estado["entrada"] = entrada
	Juego.poner_bandera("visitada_" + id)
	Juego.guardar()
	ultima_carga_ms = Time.get_ticks_msec() - inicio
	print("ZONA %s entrada=%s carga_ms=%d" % [id, entrada, ultima_carga_ms])
	if opciones.get("sin_carga", false):
		await Interfaz.fundido(false, 0.3)
	else:
		if Juego.args.has("captura_carga"):
			await Interfaz.capturar(Juego.args["captura_carga"])
		var falta := CARGA_MINIMA_MS - ultima_carga_ms
		if falta > 0 and not Juego.modo_prueba:
			await get_tree().create_timer(falta / 1000.0, true, false, true).timeout
		await Interfaz.ocultar_carga()
	get_tree().paused = false
	ocupado = false
	Interfaz.mostrar_hud(true)
	Interfaz.anunciar_zona(meta)
	zona_cambiada.emit(id)
	zona.al_entrar(entrada)
	return true


func _soltar_zona() -> void:
	if actual != null and is_instance_valid(actual):
		actual.al_salir()
		mundo.remove_child(actual)
		actual.queue_free()
	actual = null
	Materiales.limpiar_zona()
	Recursos.olvidar_zona()


func _preparar_actores(zona: Node3D) -> void:
	if jugador == null:
		jugador = Jugador.new()
		jugador.name = "Protagonista"
		mundo.add_child(jugador)
		camara = Camara.new()
		camara.name = "Camara"
		mundo.add_child(camara)
		camara.objetivo = jugador
		companero = Companero.new()
		companero.name = "Orbita"
		companero.jugador = jugador
		mundo.add_child(companero)
	jugador.gravedad = float(zona.get("gravedad"))
	jugador.salto = float(zona.get("salto"))
	jugador.factor_velocidad = float(zona.get("factor_velocidad"))
	jugador.inercia = float(zona.get("inercia"))
	camara.encuadre = float(zona.get("encuadre"))
	camara.cizalla = float(zona.get("cizalla"))
	camara.limites = zona.get("limites")
	camara.fijo = false
	var con_gato: bool = zona.get("con_companero")
	companero.visible = con_gato
	companero.process_mode = Node.PROCESS_MODE_INHERIT if con_gato else Node.PROCESS_MODE_DISABLED
	companero.hablar.habilitado = con_gato


func _colocar(zona: Node3D, entrada: String) -> void:
	var entradas: Dictionary = zona.get("entradas")
	var punto := {"pos": Vector3.ZERO, "mira": Vector3(0, 0, 1)}
	if entradas.has(entrada):
		punto = entradas[entrada]
	elif entradas.has("inicio"):
		punto = entradas["inicio"]
		print("AVISO la zona %s no tiene la entrada '%s': se usa 'inicio'" % [id_actual, entrada])
	elif not entradas.is_empty():
		punto = entradas.values()[0]
		print("AVISO la zona %s no tiene la entrada '%s' ni 'inicio'" % [id_actual, entrada])
	else:
		print("AVISO la zona %s no define entradas" % id_actual)
	jugador.colocar(punto["pos"], punto["mira"])
	companero.colocar_junto(punto["pos"], punto["mira"])
	camara.centrar()
	for u in get_tree().get_nodes_in_group("umbrales"):
		u.set("armado", false)


func cerrar() -> void:
	# vuelve al menu: suelta la zona y los actores
	_soltar_zona()
	for nodo in [jugador, companero, camara]:
		if nodo != null and is_instance_valid(nodo):
			nodo.queue_free()
	jugador = null
	companero = null
	camara = null
	id_actual = ""
	Interfaz.mostrar_hud(false)
	Interfaz.limpiar_rotulos()
