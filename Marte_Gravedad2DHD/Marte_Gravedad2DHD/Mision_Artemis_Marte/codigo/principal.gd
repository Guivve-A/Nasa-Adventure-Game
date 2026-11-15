extends Node

# Mision Artemis — seccion de Marte, como proyecto aparte. Encadena: Marte (aterrizaje + superficie) -> Fin.
# Argumentos (tras "--"):
#   --capitulo=superficie         empieza ya aterrizado (salta los siete minutos de terror)
#   --prueba                      juega solo de principio a fin, comprueba cada paso y sale (0 si todo paso)
#   --capturas=<carpeta>          con --prueba, guarda capturas de cada momento

const Marte := preload("nivel_marte.gd")
const Hud := preload("hud.gd")

var actual: Node
var capitulo := ""
var args := {}
var resumen := {}
var _ok := 0
var _mal := 0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for s in OS.get_cmdline_user_args():
		var limpio := s.trim_prefix("--")
		var i := limpio.find("=")
		if i >= 0:
			args[limpio.substr(0, i)] = limpio.substr(i + 1)
		else:
			args[limpio] = "1"
	abrir(String(args.get("capitulo", "marte")))
	if args.has("prueba"):
		_prueba()


func abrir(c: String) -> void:
	get_tree().paused = false
	if actual != null:
		actual.queue_free()
	capitulo = c
	match c:
		"fin":
			actual = Node2D.new()
			var hud = Hud.new()
			hud.capitulo = "Fin"
			var minutos := int(resumen.get("tiempo", 0.0)) / 60
			hud.panel = {"titulo": "Misión cumplida", "lineas": [
				"Aterrizaste, levantaste la base y enviaste el primer reporte a la Tierra.",
				"La protagonista cierra el libro… y mira al cielo.",
				"",
				"Aterrizaje: %s   ·   Notas del cuaderno: %d de %d" % [resumen.get("aterrizaje", ""), resumen.get("notas", 0), resumen.get("total", 0)],
				"Tiempo en Marte: %d min %d s   ·   Rescates: %d" % [minutos, int(resumen.get("tiempo", 0.0)) % 60, resumen.get("rescates", 0)],
				"",
				"R: volver a empezar"]}
			hud.ready.connect(func(): hud._fuente = preload("fuente_pixel.gd").obtener())
			actual.add_child(hud)
		_:
			capitulo = "marte"
			actual = Marte.new()
			actual.saltar_aterrizaje = c == "superficie"
			actual.terminado.connect(_fin)
	actual.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(actual)


func _fin() -> void:
	var m = actual
	resumen = {"tiempo": m.tiempo, "rescates": m.rescates, "aterrizaje": m.aterrizaje_resultado, "notas": m.cuaderno.paginas.size(), "total": m.cuaderno.total()}
	abrir.call_deferred("fin")


func _unhandled_input(evento: InputEvent) -> void:
	var tecla := evento as InputEventKey
	if tecla == null or not tecla.pressed or tecla.echo:
		return
	if tecla.keycode == KEY_R and capitulo == "fin":
		abrir("marte")
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


func _lleno(m) -> void:
	m.barras["oxigeno"] = 100.0
	m.barras["energia"] = 100.0
	m.barras["alimentos"] = 100.0
	m.barras["radiacion"] = 0.0


func _cerrar_cuaderno(m) -> void:
	await _esperar(0.3)
	if m.cuaderno.abierto:
		m.cuaderno.cerrar()


func _desplegar(m, id: String) -> void:
	var o = m._buscar(id)
	m.teletransportar(o["x"])
	_lleno(m)
	for i in 6:
		m.mantener(0.3)
	await _cerrar_cuaderno(m)


func _prueba() -> void:
	Engine.time_scale = 4.0
	var m = actual
	m.control_externo = true
	await _esperar(0.3)
	print("PRUEBA Mision Artemis — Marte")
	var a = m.aterrizaje
	_ver("empieza en el aterrizaje", a != null and a.estado == "programa")
	a.control_externo = true
	await _captura("01_programa")
	# intento 1: paracaidas demasiado alto
	a.programar(18.0, 0.6, false)
	a.probar()
	await _esperar(2.5)
	await _captura("02_entrada")
	while a.estado == "descenso":
		await _esperar(0.2)
	_ver("paracaidas a 18 km: la nave se perderia", a.resultado == "perdida" and a.causa == "rasgado")
	await _esperar(0.4)
	_ver("la primera prueba abre el cuaderno (pagina de la senal)", m.cuaderno.abierto and m.cuaderno.tiene("senal"))
	await _captura("03_cuaderno_senal")
	m.cuaderno.cerrar()
	await _esperar(0.2)
	await _captura("04_resultado_rasgado")
	# intento 2: bien, pero sin navegacion por terreno
	a.reprogramar()
	a.programar(11.0, 2.1, false)
	a.probar()
	while a.estado == "descenso":
		await _esperar(0.2)
	_ver("sin navegacion por terreno: aterrizaje duro", a.resultado == "duro" and a.causa == "rocas")
	await _captura("05_resultado_rocas")
	# intento 3: como Perseverance
	a.reprogramar()
	a.programar(11.0, 2.1, true)
	a.probar()
	await _esperar(6.4)
	await _captura("06_paracaidas")
	await _esperar(4.5)
	await _captura("07_cohetes")
	while a.estado == "descenso":
		await _esperar(0.2)
	_ver("paracaidas a 11 km, cohetes a 2,1 km y navegacion: suave", a.resultado == "suave")
	await _captura("08_resultado_suave")
	a.aceptar()
	await _esperar(5.0)
	_ver("aterriza y empieza la superficie", m.etapa == "banderas" and m.aterrizaje_resultado == "suave")
	_ver("el cuaderno guarda los siete minutos de terror", m.cuaderno.tiene("siete"))
	await _captura("09_superficie_dia")
	# moverse y saltar
	var x0: float = m.jugador.position.x
	m.dir_externa = 1.0
	await _esperar(1.0)
	m.dir_externa = 0.0
	_ver("camina a la derecha", m.jugador.position.x > x0 + 40.0)
	m.saltar()
	await _esperar(0.15)
	_ver("salta", not m.en_suelo)
	_ver("el primer salto anota la gravedad", m.cuaderno.tiene("gravedad"))
	await _esperar(1.0)
	_ver("vuelve al suelo", m.en_suelo)
	# medidores y rescate
	m.teletransportar(1500.0)
	_lleno(m)
	await _esperar(2.0)
	_ver("fuera baja el oxigeno", m.barras["oxigeno"] < 99.5)
	_ver("fuera sube la radiacion", m.barras["radiacion"] > 0.3)
	m.barras["oxigeno"] = 0.0
	await _esperar(0.2)
	_ver("sin oxigeno, rescate en la nave", m.rescates == 1 and absf(m.jugador.position.x - (m.X_COHETE + 50.0)) < 5.0)
	# dialogo
	m.teletransportar(190.0)
	m.interactuar()
	_ver("habla con la comandante", not m.hud.dialogo.is_empty())
	await _esperar(0.3)
	await _captura("10_dialogo")
	for i in 3:
		m.interactuar()
	_ver("el dialogo se cierra", m.hud.dialogo.is_empty())
	# banderas
	for o in m.objetos:
		if o["tipo"] == "bandera":
			m.teletransportar(o["x"])
			m.interactuar()
	_ver("planta las tres banderas", m.banderas == 3 and m.etapa == "base")
	await _esperar(0.6)
	await _captura("11_banderas")
	# dependencias
	var ext = m._buscar("extractor")
	m.teletransportar(ext["x"])
	for i in 6:
		m.mantener(0.3)
	_ver("sin paneles no se despliega el extractor", not ext["hecho"])
	await _esperar(0.2)
	await _captura("12_necesita_energia")
	for id in ["cupula", "paneles", "extractor", "taladro", "invernadero"]:
		await _desplegar(m, id)
		await _esperar(0.3)
		if id == "paneles":
			await _esperar(1.2)
			await _captura("13_paneles_tarde")
	_ver("despliega los cinco modulos", m.modulos == 5)
	_ver("anota aire, MOXIE, sol e hielo", m.cuaderno.tiene("aire") and m.cuaderno.tiene("moxie") and m.cuaderno.tiene("sol") and m.cuaderno.tiene("hielo"))
	m.teletransportar(1000.0)
	m.interactuar()
	_ver("entra al invernadero", m.dentro != null and m.dentro["id"] == "invernadero")
	m.barras["alimentos"] = 40.0
	await _esperar(1.0)
	_ver("en el invernadero se recuperan los alimentos", m.barras["alimentos"] > 50.0)
	m.interactuar()
	_ver("sale del invernadero", m.dentro == null)
	# atardecer y tormenta
	var espera := 0
	while m.tormenta == 0 and espera < 80:
		espera += 1
		_lleno(m)
		await _esperar(0.25)
	_ver("al atardecer llega la tormenta", m.tormenta >= 1 and m.hora >= 0.95)
	await _esperar(0.3)
	await _captura("14_atardecer_alerta")
	espera = 0
	while m.tormenta != 2 and espera < 60:
		espera += 1
		_lleno(m)
		await _esperar(0.25)
	await _cerrar_cuaderno(m)
	_ver("el polvo cubre los paneles", m.polvo_paneles >= 1.0 and m.cuaderno.tiene("polvo"))
	m.teletransportar(m._buscar("paneles")["x"])
	m.mantener(0.6)
	await _esperar(0.3)
	await _captura("15_tormenta")
	for i in 6:
		m.mantener(0.4)
	_ver("limpia los paneles", m.polvo_paneles <= 0.0)
	espera = 0
	while m.etapa != "noche" and espera < 80:
		espera += 1
		_lleno(m)
		await _esperar(0.25)
	_ver("la tormenta pasa y cae la noche", m.etapa == "noche")
	espera = 0
	while m.hora < 2.0 and espera < 80:
		espera += 1
		_lleno(m)
		await _esperar(0.25)
		if m.cuaderno.abierto:
			m.cuaderno.cerrar()
	_ver("es de noche", m.hora >= 2.0 and m.temperatura() == -89)
	_ver("anota el frio y las lunas", m.cuaderno.tiene("frio") and m.cuaderno.tiene("lunas"))
	m.teletransportar(520.0)
	await _esperar(0.3)
	await _captura("16_noche_base")
	m.cuaderno.abrir("lunas")
	await _esperar(0.2)
	await _captura("16b_cuaderno_lunas")
	m.cuaderno.cerrar()
	# antena y reporte
	m.teletransportar(m.X_ANTENA)
	_lleno(m)
	for i in 6:
		m.mantener(0.3)
	_ver("levanta la antena", m.antena_lista)
	m.interactuar()
	_ver("abre el reporte", m.etapa == "reporte")
	m.elegir_reporte(0)
	m.interactuar()
	_ver("una linea correcta no se marca como error", not m.reporte_ok)
	await _esperar(0.2)
	await _captura("17_reporte_pista")
	m.elegir_reporte(2)
	m.interactuar()
	_ver("encuentra las millas", m.reporte_ok and m.cuaderno.tiene("unidades"))
	await _cerrar_cuaderno(m)
	await _captura("18_reporte_corregido")
	m.interactuar()
	_ver("envia el reporte", m.etapa == "envio")
	await _esperar(5.5)
	await _captura("19_senal_a_la_tierra")
	await _esperar(3.0)
	_ver("termina el capitulo", capitulo == "fin")
	_ver("el cuaderno quedo completo", int(resumen.get("notas", 0)) == 11)
	await _esperar(0.4)
	await _captura("20_fin")
	print("PRUEBA: %d de %d" % [_ok, _ok + _mal])
	get_tree().quit(0 if _mal == 0 else 1)
