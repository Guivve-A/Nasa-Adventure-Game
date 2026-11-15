extends "res://pruebas/demo_captura.gd"

# Tomas extra del video demo (2026-11-15), con las mismas utilidades de demo_captura.gd.
# No es una prueba del juego: solo juega con teclas simuladas para grabar.
#   --toma=mirador_telescopio  Mirador de noche con HUD: camina hasta el telescopio, pulsa E y se abre el ocular
#   --toma=carga_mirador       del Sendero al Mirador por el umbral: pantalla de carga pintada
#   --toma=mirador_quieto      ella y Orbita quietos junto al telescopio, mirando la Luna sobre la ciudad
#   --toma=mirador_alejar      igual, y la camara se aleja con X (ultima imagen)
#   --toma=luna_lenta          Luna del sueno: saltos a paso lento con Orbita, sin HUD
#   --toma=mapa_tecla_m        en el Sendero, tecla M: el mapa del mundo y el cursor recorre los lugares

const TELESCOPIO_JUNTO := Vector3(2.35, 0.0, 0.55)


func correr(pruebas: Node) -> void:
	p = pruebas
	Juego.modo_prueba = false
	Juego.sin_guardar = true
	Juego.minijuegos_solos = true
	var toma := String(Juego.args.get("toma", ""))
	var seg := float(Juego.args.get("segundos", "0"))
	match toma:
		"mirador_telescopio":
			await _mirador_telescopio(seg if seg > 0.0 else 14.0)
		"carga_mirador":
			await _carga_mirador(seg if seg > 0.0 else 10.0)
		"mirador_quieto":
			await _mirador_quieto(seg if seg > 0.0 else 8.0, false)
		"mirador_alejar":
			await _mirador_quieto(seg if seg > 0.0 else 6.0, true)
		"luna_lenta":
			await _zona("luna", "inicio", [Vector3(6.0, 0, -0.5), Vector3(14.0, 0, -2.5)], seg if seg > 0.0 else 6.0,
				{"hud": false, "saltar": true, "correr": false})
		"mapa_tecla_m":
			await _mapa_tecla_m(seg if seg > 0.0 else 6.0)
		_:
			p.comprobar(false, "demo.toma_desconocida", toma)


func _nodo(nombre: String) -> Node3D:
	return Zonas.actual.find_child(nombre, true, false) as Node3D


func _mirador_telescopio(segundos: float) -> void:
	await _entrar("mirador", "inicio", {"hud": true})
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	var tel := _nodo("Telescopio")
	if tel == null:
		p.comprobar(false, "demo.sin_telescopio", "")
		_marca("fin")
		return
	var destino := tel.global_position + (Zonas.jugador.global_position - tel.global_position).normalized() * 0.9
	destino.y = 0.0
	await p._caminar_con_teclas(destino, 8.0, 0.35)
	await p._usar_con_teclas(tel)
	# dialogo de Orbita (se pasa con E como al jugar) y despues el ocular, que se juega solo
	var con_dialogo := 0.0
	while Engine.get_frames_drawn() < fin:
		await get_tree().process_frame
		con_dialogo = con_dialogo + get_process_delta_time() if Interfaz.dialogo.visible else 0.0
		if con_dialogo > 2.2:
			await _pulsar(KEY_E)
			con_dialogo = 0.0
	p._soltar_todo()
	_marca("fin")


func _carga_mirador(segundos: float) -> void:
	await _entrar("sendero", "mirador", {"hud": true})
	var umbral: Node3D = null
	for u in get_tree().get_nodes_in_group("umbrales"):
		if Zonas.actual.is_ancestor_of(u) and String(u.get("destino_zona")) == "mirador":
			umbral = u
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	await _seg(0.4)
	if umbral != null:
		var d: Vector3 = umbral.global_position
		_caminar([Vector3(d.x, 0.0, d.z)], false, false)
	var con_dialogo := 0.0
	while Engine.get_frames_drawn() < fin:
		await get_tree().process_frame
		con_dialogo = con_dialogo + get_process_delta_time() if Interfaz.dialogo.visible else 0.0
		if con_dialogo > 2.8:
			await _pulsar(KEY_E)
			con_dialogo = 0.0
	p._soltar_todo()
	_marca("fin")


func _mirador_quieto(segundos: float, alejar: bool) -> void:
	await _entrar("mirador", "inicio", {"hud": false})
	var tel := _nodo("Telescopio")
	var junto := TELESCOPIO_JUNTO
	if tel != null:
		junto = tel.global_position + Vector3(-0.55, 0.0, -0.75)
	var mira := Vector3(0.75, 0.0, 0.66).normalized()      # hacia el oeste y la ciudad, donde baja la Luna
	Zonas.jugador.colocar(Vector3(junto.x, 0.3, junto.z), mira)
	Zonas.companero.colocar_junto(Zonas.jugador.global_position, mira)
	await _seg(0.8)
	Zonas.camara.centrar()
	if alejar:
		# empieza cerca (Z) y en la toma se aleja con X
		p._tecla(KEY_Z, true)
		await _seg(2.4)
		p._tecla(KEY_Z, false)
	await _seg(0.6)
	_marca("inicio")
	if alejar:
		await _seg(0.5)
		p._tecla(KEY_X, true)
		await _seg(segundos - 0.5)
		p._tecla(KEY_X, false)
	else:
		await _seg(segundos)
	p._soltar_todo()
	_marca("fin")


func _mapa_tecla_m(segundos: float) -> void:
	await _entrar("sendero", "inicio", {"hud": true})
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	await _seg(0.5)
	await _pulsar(KEY_M)
	await _seg(1.0)
	var teclas := [KEY_D, KEY_W, KEY_D, KEY_A, KEY_S, KEY_A]
	var n := 0
	while Engine.get_frames_drawn() < fin:
		await _pulsar(teclas[n % teclas.size()])
		await _seg(0.8)
		n += 1
	_marca("fin")
