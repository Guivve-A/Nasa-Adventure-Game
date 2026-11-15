extends Node

# Estado global de la partida (autoload "Juego"): argumentos, controles, banderas, inventario, cuaderno,
# misiones y guardado. Las zonas y los minijuegos solo leen y escriben por las funciones de este guion.

signal bandera_cambiada(nombre: String, valor: Variant)
signal inventario_cambiado(id: String, cantidad: int)
signal cuaderno_cambiado(id: String)
signal misiones_cambiadas

const RUTA_PARTIDA := "user://partida.json"
const RUTA_MISIONES := "res://datos/misiones.json"
const RUTA_FICHAS := "res://datos/datos_espaciales.json"
const VERSION := 1

var estado: Dictionary = {}
var misiones: Array = []       # definicion de las misiones (datos/misiones.json)
var fichas: Dictionary = {}    # fichas del cuaderno por id (datos/datos_espaciales.json)
var args: Dictionary = {}      # argumentos tras "--": --clave=valor o --clave
var modo_prueba := false       # dialogos sin esperas y minijuegos que se juegan solos
var minijuegos_solos := false  # solo los minijuegos se juegan solos (pruebas con teclas simuladas)
var sin_guardar := false       # no escribe la partida (pruebas)
var _revisando := false


func _init() -> void:
	for a in OS.get_cmdline_user_args():
		var limpio: String = a.trim_prefix("--")
		var corte := limpio.find("=")
		if corte >= 0:
			args[limpio.substr(0, corte)] = limpio.substr(corte + 1)
		else:
			args[limpio] = "1"
	modo_prueba = args.has("prueba") or args.has("auto")
	_registrar_acciones()
	_cargar_datos()
	nueva_partida()


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	if args.has("ritmo"):
		Engine.time_scale = float(args["ritmo"])


func _process(delta: float) -> void:
	if not get_tree().paused:
		estado["tiempo"] = float(estado.get("tiempo", 0.0)) + delta


# ---------------------------------------------------------------- controles

func _registrar_acciones() -> void:
	_accion("mover_izquierda", [KEY_A, KEY_LEFT], [JOY_BUTTON_DPAD_LEFT], [[JOY_AXIS_LEFT_X, -1.0]])
	_accion("mover_derecha", [KEY_D, KEY_RIGHT], [JOY_BUTTON_DPAD_RIGHT], [[JOY_AXIS_LEFT_X, 1.0]])
	_accion("mover_arriba", [KEY_W, KEY_UP], [JOY_BUTTON_DPAD_UP], [[JOY_AXIS_LEFT_Y, -1.0]])
	_accion("mover_abajo", [KEY_S, KEY_DOWN], [JOY_BUTTON_DPAD_DOWN], [[JOY_AXIS_LEFT_Y, 1.0]])
	_accion("correr", [KEY_SHIFT], [JOY_BUTTON_B], [[JOY_AXIS_TRIGGER_RIGHT, 1.0]])
	_accion("interactuar", [KEY_E, KEY_ENTER, KEY_KP_ENTER], [JOY_BUTTON_A])
	_accion("saltar", [KEY_SPACE], [JOY_BUTTON_X])
	_accion("pausa", [KEY_ESCAPE, KEY_P], [JOY_BUTTON_START])
	_accion("cuaderno", [KEY_TAB, KEY_C], [JOY_BUTTON_Y])
	_accion("mapa", [KEY_M], [JOY_BUTTON_BACK])
	_accion("minimapa", [KEY_N], [JOY_BUTTON_RIGHT_STICK])
	_accion("acercar", [KEY_Z, KEY_PAGEUP], [JOY_BUTTON_RIGHT_SHOULDER])
	_accion("alejar", [KEY_X, KEY_PAGEDOWN], [JOY_BUTTON_LEFT_SHOULDER])


func _accion(nombre: String, teclas: Array, botones: Array = [], ejes: Array = []) -> void:
	if InputMap.has_action(nombre):
		return
	InputMap.add_action(nombre, 0.35)
	for t in teclas:
		var tecla := InputEventKey.new()
		tecla.physical_keycode = t
		InputMap.action_add_event(nombre, tecla)
	for b in botones:
		var boton := InputEventJoypadButton.new()
		boton.button_index = b
		InputMap.action_add_event(nombre, boton)
	for par in ejes:
		var eje := InputEventJoypadMotion.new()
		eje.axis = par[0]
		eje.axis_value = par[1]
		InputMap.action_add_event(nombre, eje)


# ---------------------------------------------------------------- datos

static func leer_json(ruta: String) -> Variant:
	if not FileAccess.file_exists(ruta):
		return null
	return JSON.parse_string(FileAccess.get_file_as_string(ruta))


func _cargar_datos() -> void:
	var m: Variant = leer_json(RUTA_MISIONES)
	if m is Dictionary:
		misiones = m.get("misiones", [])
	var f: Variant = leer_json(RUTA_FICHAS)
	if f is Dictionary:
		fichas = f.get("fichas", {})
	# fichas propias de otros modos (misma forma): la base espacial trae las suyas
	for ruta in ["res://base/datos_base.json"]:
		var extra: Variant = leer_json(ruta)
		if extra is Dictionary:
			var mas: Dictionary = extra.get("fichas", {})
			for clave in mas:
				fichas[clave] = mas[clave]


func info_minijuego(id: String) -> Dictionary:
	# un minijuego con "zona" en su json es un modo que vive en una zona (p. ej. la base espacial)
	var d: Variant = leer_json("res://minijuegos/%s/minijuego.json" % id)
	if d is Dictionary:
		d["id"] = id
		return d
	return {}


func catalogo_minijuegos() -> Array:
	var lista: Array = []
	for carpeta in DirAccess.get_directories_at("res://minijuegos"):
		var d := info_minijuego(carpeta)
		if not d.is_empty():
			lista.append(d)
	lista.sort_custom(func(a, b): return float(a.get("orden", 99)) < float(b.get("orden", 99)))
	return lista


func ficha(id: String) -> Dictionary:
	var d: Variant = fichas.get(id, {})
	if d is Dictionary:
		return d
	return {}


# ---------------------------------------------------------------- partida

func nueva_partida() -> void:
	estado = {
		"version": VERSION,
		"banderas": {},
		"inventario": {},
		"cuaderno": [],
		"misiones_hechas": [],
		"minijuegos": {},
		"zona": "habitacion",
		"entrada": "inicio",
		"tiempo": 0.0,
	}
	misiones_cambiadas.emit()


func hay_partida() -> bool:
	return FileAccess.file_exists(RUTA_PARTIDA)


func guardar() -> void:
	if modo_prueba or sin_guardar:
		return
	var archivo := FileAccess.open(RUTA_PARTIDA, FileAccess.WRITE)
	if archivo != null:
		archivo.store_string(JSON.stringify(estado, "\t"))


func cargar() -> bool:
	var d: Variant = leer_json(RUTA_PARTIDA)
	if not (d is Dictionary) or int(d.get("version", 0)) != VERSION:
		return false
	nueva_partida()
	for clave in d:
		estado[clave] = d[clave]
	misiones_cambiadas.emit()
	return true


# ---------------------------------------------------------------- banderas e inventario

func bandera(nombre: String, defecto: Variant = false) -> Variant:
	return estado["banderas"].get(nombre, defecto)


func poner_bandera(nombre: String, valor: Variant = true) -> void:
	if estado["banderas"].get(nombre) == valor:
		return
	estado["banderas"][nombre] = valor
	bandera_cambiada.emit(nombre, valor)
	_revisar_misiones()


func cantidad(id: String) -> int:
	return int(estado["inventario"].get(id, 0))


func sumar(id: String, n: int = 1) -> int:
	var total := cantidad(id) + n
	estado["inventario"][id] = total
	inventario_cambiado.emit(id, total)
	return total


func anotar(id_ficha: String) -> bool:
	# abre una ficha del cuaderno; devuelve true si era nueva
	if id_ficha == "" or estado["cuaderno"].has(id_ficha):
		return false
	estado["cuaderno"].append(id_ficha)
	cuaderno_cambiado.emit(id_ficha)
	return true


func registrar_minijuego(id: String, resultado: Dictionary) -> void:
	var r: Dictionary = estado["minijuegos"].get(id, {"veces": 0, "superado": false, "mejor": 0.0})
	r["veces"] = int(r["veces"]) + 1
	if resultado.get("superado", false):
		r["superado"] = true
		r["mejor"] = maxf(float(r["mejor"]), float(resultado.get("puntos", 0.0)))
	estado["minijuegos"][id] = r


# ---------------------------------------------------------------- misiones

func _mision_hecha(m: Dictionary) -> bool:
	return estado["misiones_hechas"].has(m.get("id", ""))


func _pasos_completos(m: Dictionary) -> bool:
	for p in m.get("pasos", []):
		if not bandera(p.get("bandera", "")):
			return false
	return true


func _mision_abierta(m: Dictionary) -> bool:
	if _mision_hecha(m):
		return false
	for r in m.get("requiere", []):
		if not bandera(r):
			return false
	return true


func mision_activa() -> Dictionary:
	# la primera mision principal sin terminar cuyas banderas requeridas ya estan puestas;
	# si no queda ninguna principal, la primera secundaria ("secundaria": true)
	for m in misiones:
		if not m.get("secundaria", false) and _mision_abierta(m):
			return m
	for m in misiones:
		if m.get("secundaria", false) and _mision_abierta(m):
			return m
	return {}


func misiones_abiertas() -> Array:
	# todas las misiones abiertas (principal y secundarias), para listas y el cuaderno
	var lista: Array = []
	for m in misiones:
		if _mision_abierta(m):
			lista.append(m)
	return lista


func paso_actual() -> Dictionary:
	var m := mision_activa()
	for p in m.get("pasos", []):
		if not bandera(p.get("bandera", "")):
			return p
	return {}


func objetivo() -> String:
	return paso_actual().get("texto", "")


func destino_actual() -> Dictionary:
	# a donde lleva el paso en curso (lo usa el minimapa): {"zona", "destino", "texto"}.
	#   zona    = id de la zona donde se cumple el paso (si el paso no la trae, la de su mision)
	#   destino = nombre del nodo dentro de esa zona; "@orbita" = el gato; "" = basta con llegar a la zona
	#   texto   = el objetivo tal como sale en la tarjeta
	# Vacio si no queda ningun paso.
	var paso := paso_actual()
	if paso.is_empty():
		return {}
	var mision := mision_activa()
	return {
		"zona": String(paso.get("zona", mision.get("zona", ""))),
		"destino": String(paso.get("destino", "")),
		"texto": String(paso.get("texto", "")),
	}


func _revisar_misiones() -> void:
	if _revisando:
		return
	_revisando = true
	var cambio := true
	while cambio:
		cambio = false
		for m in misiones:
			if _mision_hecha(m) or not _pasos_completos(m):
				continue
			var abierta := true
			for r in m.get("requiere", []):
				if not bandera(r):
					abierta = false
			if not abierta:
				continue
			estado["misiones_hechas"].append(m.get("id", ""))
			var premio: Dictionary = m.get("recompensa", {})
			for f in premio.get("fichas", []):
				anotar(f)
			for b in premio.get("banderas", []):
				estado["banderas"][b] = true
				bandera_cambiada.emit(b, true)
			Interfaz.aviso("Misión cumplida: %s" % m.get("titulo", ""), 4.0)
			Audio.sonar("logro")
			cambio = true
	_revisando = false
	misiones_cambiadas.emit()
