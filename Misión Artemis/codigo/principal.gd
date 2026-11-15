extends Node

# Mision Artemis: Mas alla de las paginas. Encadena los capitulos: Luna -> Viaje -> Marte -> Fin.
# Argumentos (tras "--"):
#   --capitulo=luna|viaje|marte   empieza en ese capitulo
#   --prueba                      juega solo de principio a fin, comprueba cada paso y sale (0 si todo paso)
#   --capturas=<carpeta>          con --prueba, guarda capturas de cada momento

const Luna := preload("nivel_luna.gd")
const Viaje := preload("viaje.gd")
const Marte := preload("nivel_marte.gd")
const Hud := preload("hud.gd")

var actual: Node
var capitulo := ""
var args := {}
var resumen := {"tiempo": 0.0, "rescates": 0}
var _ok := 0
var _mal := 0


func _ready() -> void:
	for s in OS.get_cmdline_user_args():
		var limpio := s.trim_prefix("--")
		var i := limpio.find("=")
		if i >= 0:
			args[limpio.substr(0, i)] = limpio.substr(i + 1)
		else:
			args[limpio] = "1"
	abrir(String(args.get("capitulo", "luna")))
	if args.has("prueba"):
		_prueba()


func abrir(c: String) -> void:
	if actual != null:
		actual.queue_free()
	capitulo = c
	match c:
		"viaje":
			actual = Viaje.new()
			actual.llegada.connect(func(): abrir.call_deferred("marte"))
		"marte":
			actual = Marte.new()
			actual.terminado.connect(func(): abrir.call_deferred("fin"))
		"fin":
			actual = Node2D.new()
			var hud = Hud.new()
			hud.capitulo = "Fin"
			var minutos := int(resumen["tiempo"]) / 60
			hud.panel = {"titulo": "Misión cumplida", "lineas": [
				"Construiste el cohete, cruzaste el espacio y levantaste la base marciana.",
				"La protagonista cierra el libro… y mira al cielo.",
				"",
				"Tiempo en la Luna: %d min %d s   ·   Rescates: %d" % [minutos, int(resumen["tiempo"]) % 60, resumen["rescates"]],
				"",
				"R: volver a empezar"]}
			actual.add_child(hud)
		_:
			capitulo = "luna"
			actual = Luna.new()
			actual.despegue.connect(func(r): resumen = r; abrir.call_deferred("viaje"))
	add_child(actual)


func _unhandled_input(evento: InputEvent) -> void:
	var tecla := evento as InputEventKey
	if tecla == null or not tecla.pressed or tecla.echo:
		return
	if tecla.keycode == KEY_R and capitulo == "fin":
		abrir("luna")
	elif tecla.keycode == KEY_F11:
		var w := get_window()
		w.mode = Window.MODE_WINDOWED if w.mode == Window.MODE_FULLSCREEN else Window.MODE_FULLSCREEN


# ---------- prueba automatica ----------
func _ver(nombre: String, cond: bool) -> void:
	if cond:
		_ok += 1
	else:
		_mal += 1
	print(("  ok    " if cond else "  FALLA ") + nombre)


func _esperar(s: float) -> void:
	await get_tree().create_timer(s).timeout


func _captura(nombre: String) -> void:
	if not args.has("capturas"):
		return
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(String(args["capturas"]).path_join(nombre + ".png"))


func _lleno(l) -> void:
	l.barras["oxigeno"] = 100.0
	l.barras["energia"] = 100.0
	l.barras["alimentos"] = 100.0
	l.barras["radiacion"] = 0.0


func _reunir(l, recurso: String, n: int) -> void:
	# recoge n unidades de un recurso con las acciones reales del jugador
	var intentos := 0
	while int(l.mochila[recurso]) < n and intentos < 200:
		intentos += 1
		var hallado = null
		for o in l.objetos:
			if (recurso == "caja" and o["tipo"] == "cajas" or o["tipo"] == "veta" and o.get("recurso", "") == recurso) and int(o["unidades"]) > 0:
				hallado = o
				break
		if hallado == null:
			return
		l.teletransportar(hallado["x"])
		_lleno(l)
		if recurso == "caja":
			l.interactuar()
		else:
			l.mantener(0.4)
		await get_tree().physics_frame


func _prueba() -> void:
	Engine.time_scale = 6.0
	var l = actual
	l.control_externo = true
	l.eventos_auto = false
	await _esperar(0.5)
	print("PRUEBA Mision Artemis")
	_ver("el nivel carga sus objetos", l.objetos.size() >= 30)
	await _captura("01_inicio")
	# movimiento
	var x0: float = l.jugador.position.x
	l.dir_externa = 1.0
	await _esperar(1.0)
	_ver("camina a la derecha", l.jugador.position.x > x0 + 40.0)
	l.dir_externa = 0.0
	l.saltar()
	await _esperar(0.25)
	var y_salto: float = l.jugador.position.y
	_ver("salta", not l.en_suelo and y_salto < l.suelo_en(l.jugador.position.x) - 15.0)
	var e0: float = l.barras["energia"]
	l.saltar()
	await _esperar(0.3)
	_ver("el impulso de mochila gasta energia", l.barras["energia"] < e0 - 5.0)
	await _esperar(2.5)
	_ver("vuelve al suelo", l.en_suelo)
	# medidores
	l.teletransportar(2000.0)
	_lleno(l)
	await _esperar(3.0)
	_ver("fuera de la base baja el oxigeno", l.barras["oxigeno"] < 99.0)
	_ver("lejos de la base sube la radiacion", l.barras["radiacion"] > 0.5)
	var cupula = null
	for o in l.objetos:
		if o["id"] == "cupula":
			cupula = o
	l.teletransportar(cupula["x"])
	l.barras["oxigeno"] = 40.0
	l.interactuar()
	_ver("entra a la cupula", l.dentro != null)
	await _esperar(1.5)
	_ver("dentro sube el oxigeno", l.barras["oxigeno"] > 55.0)
	# lluvia solar
	l.dir_externa = 1.0
	await _esperar(0.2)
	l.dir_externa = 0.0
	_ver("sale al moverse", l.dentro == null)
	l.teletransportar(300.0)
	_lleno(l)
	l.iniciar_lluvia(0.0)
	await _esperar(2.0)
	_ver("la lluvia solar sube la radiacion", l.barras["radiacion"] > 8.0)
	await _captura("02_lluvia_solar")
	l.estado_lluvia = 0
	# meteorito
	var antes: int = l.objetos.size()
	l.teletransportar(330.0)
	_lleno(l)
	l.lanzar_meteorito(370.0, 0.6)      # un hueco libre de la pista: junto a un prop no deja veta
	await _esperar(0.4)
	await _captura("03_aviso_meteorito")
	await _esperar(1.2)
	_ver("el meteorito deja una veta nueva", l.objetos.size() == antes + 1)
	# rescate
	l.barras["oxigeno"] = 0.0
	await _esperar(0.2)
	_ver("sin oxigeno hay rescate en la cupula", l.rescates == 1 and absf(l.jugador.position.x - 616.0) < 5.0)
	# dialogo
	for o in l.objetos:
		if o["tipo"] == "npc" and o["id"] == "comandante":
			l.teletransportar(o["x"] - 10.0)
	l.interactuar()
	_ver("abre el dialogo de la comandante", not l.hud.dialogo.is_empty())
	await _esperar(0.3)
	await _captura("04_dialogo")
	for i in 4:
		l.interactuar()
	_ver("el dialogo se cierra", l.hud.dialogo.is_empty())
	# rover
	l.teletransportar(l.rover["x"])
	l.interactuar()
	_ver("sube al rover", l.montado)
	var xr: float = l.jugador.position.x
	l.dir_externa = -1.0
	await _esperar(1.0)
	l.dir_externa = 0.0
	_ver("el rover es mas rapido que caminar", xr - l.jugador.position.x > 100.0)
	await _captura("05_rover")
	l.teletransportar(1720.0)
	l.cerca = null
	l.interactuar()
	_ver("baja del rover", not l.montado)
	# fases del cohete
	for f in 4:
		var req: Dictionary = l.FASES[f]
		for k in req:
			var falta := int(req[k])
			while falta > 0:
				var lote := mini(falta, 4)
				await _reunir(l, k, lote)
				for o in l.objetos:
					if o["tipo"] == "constructora":
						l.teletransportar(o["x"])
				l.interactuar()
				falta -= lote
		_ver("fase %d del cohete" % (f + 1), l.fase == f + 1)
		if f == 1:
			await _esperar(0.5)
			await _captura("06_cohete_fase_2")
	# despegue
	_ver("armado, aun no puede despegar", not l.listo_para_despegar())
	for o in l.objetos:
		if o["tipo"] == "panel":
			l.teletransportar(o["x"])
			for i in 4:
				l.mantener(0.3)
	_ver("orienta los tres paneles", l.paneles_orientados == 3)
	await _reunir(l, "hielo", 4)
	await _captura("07_crater_hielo")
	for o in l.objetos:
		if o["tipo"] == "deposito":
			l.teletransportar(o["x"])
	l.interactuar()
	_ver("el hielo llena el combustible", l.combustible >= 100.0)
	var espera := 0
	while l.bateria < 100.0 and espera < 60:
		espera += 1
		_lleno(l)
		await _esperar(1.0)
	_ver("los paneles cargan la bateria", l.bateria >= 100.0)
	l.teletransportar(l.cohete["x"])
	await _esperar(0.3)
	await _captura("08_listo_para_despegar")
	l.interactuar()
	await _esperar(1.5)
	await _captura("09_despegue")
	await _esperar(3.0)
	_ver("pasa al viaje", capitulo == "viaje")
	await _esperar(4.0)
	await _captura("10_viaje")
	await _esperar(7.0)
	_ver("llega a Marte", capitulo == "marte")
	var m = actual
	m.control_externo = true
	await _esperar(0.5)
	await _captura("11_marte_llegada")
	for p in m.puntos:
		if p["tipo"] == "bandera":
			m.teletransportar(p["x"])
			m.interactuar()
	_ver("planta las tres banderas", m.banderas == 3)
	await _esperar(0.8)
	await _captura("12_marte_banderas")
	for p in m.puntos:
		if p["tipo"] == "modulo":
			m.teletransportar(p["x"])
			for i in 5:
				m.mantener(0.3)
	_ver("despliega los tres modulos", m.modulos == 3)
	await _esperar(1.0)
	await _captura("13_marte_base")
	await _esperar(2.5)
	_ver("llega al final", capitulo == "fin")
	await _esperar(0.5)
	await _captura("14_fin")
	print("PRUEBA: %d de %d" % [_ok, _ok + _mal])
	get_tree().quit(0 if _mal == 0 else 1)
