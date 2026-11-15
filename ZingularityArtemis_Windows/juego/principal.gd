extends Node

# Arranque del juego. Sin argumentos abre el menu principal. Con argumentos tras "--" entra directo a una
# zona o a un minijuego, corre las pruebas, guarda capturas o mide fps (ver herramientas/juego_ejecutar.py).

const Pruebas := preload("res://pruebas/pruebas.gd")


func _ready() -> void:
	var a: Dictionary = Juego.args
	await get_tree().process_frame
	if a.has("prueba"):
		var p := Pruebas.new()
		add_child(p)
		await p.correr(a["prueba"])
		Interfaz.salir()
		return
	if a.has("minijuego"):
		if a.has("captura"):
			_capturar_luego(a["captura"], float(a.get("espera", "3")))
		var r: Dictionary = await Interfaz.abrir_minijuego(a["minijuego"], {"dificultad": int(a.get("dificultad", "1")), "fallar": a.has("fallar")})
		print("RESULTADO ", r)
		if not a.has("captura"):
			Interfaz.salir()
		return
	if a.has("zona"):
		Juego.nueva_partida()
		if not a.has("historia"):
			Juego.poner_bandera("visita_libre")
		for b in String(a.get("banderas", "")).split(",", false):
			Juego.poner_bandera(b)
		await Zonas.ir_a(a["zona"], a.get("entrada", "inicio"))
		if a.has("pos") and Zonas.jugador != null:
			var xz := String(a["pos"]).split(",")
			var mira := Vector3(0, 0, 1)
			if a.has("mira"):
				var m := String(a["mira"]).split(",")
				mira = Vector3(float(m[0]), 0.0, float(m[1]))
			var y := float(xz[2]) if xz.size() > 2 else Zonas.jugador.global_position.y
			Zonas.jugador.colocar(Vector3(float(xz[0]), y + 0.05, float(xz[1])), mira)
			Zonas.companero.colocar_junto(Zonas.jugador.global_position, mira)
			await get_tree().create_timer(0.4).timeout
			Zonas.camara.centrar()
		if a.has("encuadre") and Zonas.camara != null:
			Zonas.camara.encuadre = float(a["encuadre"])
			Zonas.camara.centrar()
		if a.has("medir"):
			await _medir(float(a["medir"]))
			Interfaz.salir()
		elif a.has("captura"):
			_capturar_luego(a["captura"], float(a.get("espera", "2")))
		return
	Interfaz.abrir_menu()
	if a.has("mapa"):
		Interfaz.abrir_mapa(true)
	if a.has("captura"):
		_capturar_luego(a["captura"], float(a.get("espera", "1.5")))


func _capturar_luego(ruta: String, espera: float) -> void:
	await get_tree().create_timer(espera, true, false, true).timeout
	if Juego.args.has("sin_hud"):
		Interfaz.mostrar_hud(false)
		await get_tree().process_frame
	await Interfaz.capturar(ruta)
	Interfaz.salir()


func _medir(segundos: float) -> void:
	# sin vsync: fps, ms por cuadro (media y p95), primitivas y llamadas de dibujo
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	var fin := Time.get_ticks_msec() + 2500
	while Time.get_ticks_msec() < fin:      # calentar: compilacion de shaders y sombras
		await get_tree().process_frame
	var tiempos: Array[float] = []
	var anterior := Time.get_ticks_usec()
	fin = Time.get_ticks_msec() + int(segundos * 1000.0)
	var prims := 0.0
	var llamadas := 0.0
	while Time.get_ticks_msec() < fin:
		await get_tree().process_frame
		var ahora := Time.get_ticks_usec()
		tiempos.append((ahora - anterior) / 1000.0)
		anterior = ahora
		prims = Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)
		llamadas = Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	tiempos.sort()
	var suma := 0.0
	for t in tiempos:
		suma += t
	var media := suma / maxf(float(tiempos.size()), 1.0)
	var p95: float = tiempos[int(tiempos.size() * 0.95)] if not tiempos.is_empty() else 0.0
	print("MEDIDA zona=%s cuadros=%d fps_medio=%.1f ms_medio=%.2f ms_p95=%.2f primitivas=%d llamadas=%d carga_ms=%d resolucion=%s" % [
		Zonas.id_actual, tiempos.size(), 1000.0 / maxf(media, 0.001), media, p95, int(prims), int(llamadas),
		Zonas.ultima_carga_ms, str(get_viewport().get_visible_rect().size)])
