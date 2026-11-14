extends Node

# Comprobaciones especificas del carril; no modifican el anfitrion.
const Minijuego = preload("res://minijuegos/telescopio/telescopio.gd")


func _nuevo(dificultad: int) -> Control:
	var m: Control = Minijuego.new()
	add_child(m)
	m.preparar({"dificultad": dificultad}, Juego.info_minijuego("telescopio"))
	m.empezar()
	return m


func _liberar(m: Control) -> void:
	m.activo = false
	m.queue_free()
	await get_tree().process_frame


func correr(p: Node) -> void:
	for nivel in [1, 2, 3]:
		var m: Control = _nuevo(nivel)
		var resultado: Dictionary = {}
		m.terminado.connect(func(r: Dictionary): resultado.merge(r))
		m.jugar_solo(true)
		while m.activo and m.tiempo < 39:
			await get_tree().process_frame
		p.comprobar(bool(resultado.get("superado", false)) and m.marcas.size() == 3 and m.tiempo < 40, "telescopio.piloto_real_d%d" % nivel, str(resultado))
		print("TELESCOPIO_EVIDENCIA nivel=%d tiempo=%.3f marcas=%d" % [nivel, m.tiempo, m.marcas.size()])
		await _liberar(m)
	var m: Control = _nuevo(1)
	p.comprobar(m._causa_marca(m.CENTRO + Vector2(180, 0), 0) != "", "telescopio.fuera_del_disco")
	var terminador: Vector2 = m._objetivo_auto()
	p.comprobar(m._causa_marca(terminador, 0) == "", "telescopio.terminador_geometrico")
	p.comprobar(m._causa_marca(m.CENTRO, 0) != "", "telescopio.noche_no_es_frontera")
	p.comprobar(m._causa_marca(m.CENTRO, 1) == "", "telescopio.tierra_ilumina_noche")
	var brillante: Vector2 = m.CENTRO + (terminador - m.CENTRO).normalized() * m.RADIO * 0.89
	p.comprobar(m._causa_marca(brillante, 1).contains("Sol"), "telescopio.sol_no_es_cenicienta")
	p.comprobar(m._causa_marca(m.CENTRO + m.CRISIUM * m.RADIO, 2) == "", "telescopio.crisium_proyeccion_validada")
	p.comprobar(m._causa_marca(m.CENTRO, 2) != "", "telescopio.crisium_no_es_centro")
	m._confirmar()
	p.comprobar(m.etapa == 0 and m.revisiones == 1 and m._mensaje.text.contains("20,0°"), "telescopio.busqueda_alta_explica")
	m.acimut = m.datos["azimut_deg"]
	m.altura = m.datos["elevacion_deg"]
	m._confirmar()
	p.comprobar(m.etapa == 1, "telescopio.centrar_abre_enfoque")
	m._confirmar()
	p.comprobar(m.etapa == 1 and m._mensaje.text.contains("borroso"), "telescopio.enfoque_borroso_no_avanza")
	m.enfoque = m.FOCO
	m._confirmar()
	p.comprobar(m.etapa == 2, "telescopio.nitidez_abre_marcas")
	await _liberar(m)
	# Raton: centrar el objeto que aparece en el buscador, rueda y mira.
	m = _nuevo(1)
	var clic: InputEventMouseButton = InputEventMouseButton.new()
	clic.pressed = true
	clic.button_index = MOUSE_BUTTON_LEFT
	clic.position = m.CENTRO + Vector2((float(m.datos["azimut_deg"]) - m.acimut) * 6, (m.altura - float(m.datos["elevacion_deg"])) * 6)
	m._gui_input(clic)
	p.comprobar(m._centrada(), "telescopio.raton_centra_luna_visible")
	var confirmar: InputEventAction = InputEventAction.new()
	confirmar.action = "interactuar"
	confirmar.pressed = true
	m._input(confirmar)
	p.comprobar(m.etapa == 1, "telescopio.accion_teclado_confirma")
	clic.button_index = MOUSE_BUTTON_WHEEL_UP
	m._gui_input(clic)
	p.comprobar(is_equal_approx(m.enfoque, 0.145), "telescopio.rueda_raton_enfoca")
	m._dial_foco.value = m.FOCO
	m._input(confirmar)
	m.mira = m._objetivo_auto()
	m._input(confirmar)
	p.comprobar(m.etapa == 2 and m.rasgo == 1, "telescopio.marcar_terminador_real")
	var luz_solar: Vector2 = m.CENTRO + (terminador - m.CENTRO).normalized() * m.RADIO * 0.89
	var mover_raton: InputEventMouseMotion = InputEventMouseMotion.new()
	mover_raton.position = luz_solar
	m._gui_input(mover_raton)
	var fallo_luz: Dictionary = {}
	m.terminado.connect(func(r: Dictionary): fallo_luz.merge(r))
	for i in 5:
		m._input(confirmar)
	p.comprobar(not m.activo and not bool(fallo_luz.get("superado", true)) and String(fallo_luz.get("detalle", "")).contains("Sol"), "telescopio.fallo_real_al_senalar_sol")
	await _liberar(m)
	# El agotamiento de tiempo es real y usa la misma ruta de finalizacion.
	m = _nuevo(3)
	var agotado: Dictionary = {}
	m.terminado.connect(func(r: Dictionary): agotado.merge(r))
	m.tiempo = m.LIMITE
	m._paso(0.01)
	p.comprobar(not m.activo and not bool(agotado.get("superado", true)) and String(agotado.get("detalle", "")).contains("20,0°"), "telescopio.limite_150s_causal")
	await _liberar(m)
	if Juego.args.has("evidencia_telescopio"):
		await _capturas()


func _capturas() -> void:
	var m: Control = _nuevo(1)
	m.position = Vector2(80, 100)
	var base: String = ProjectSettings.globalize_path("res://../Nasa_Game/Construccion/Minijuegos/telescopio/")
	for etapa in [0, 1, 2, 3]:
		if etapa == 1:
			m.acimut = m.datos["azimut_deg"]
			m.altura = m.datos["elevacion_deg"]
			m._confirmar()
		elif etapa == 2:
			m.enfoque = m.FOCO
			m._confirmar()
		elif etapa == 3:
			m.mira = m._objetivo_auto()
			m._confirmar()
			m.mira = m._objetivo_auto()
			m._confirmar()
		m._refrescar()
		for i in 6:
			await get_tree().process_frame
		await Interfaz.capturar(base + "paso_%d.png" % etapa)
	await _liberar(m)
