extends Node

# Cobertura adicional: dos modos, cortes, regla de un cambio y paso fijo.
const Seguidor = preload("res://minijuegos/seguidor/seguidor.gd")

func correr(p: Node) -> void:
	for modo in ["normal", "prealimentacion"]:
		for d in [1, 2, 3]:
			for acierta in [true, false]:
				var m: Control = _nuevo(modo, d)
				var resultado: Dictionary = {}
				m.terminado.connect(func(r: Dictionary): resultado.merge(r))
				m.jugar_solo(acierta)
				for cuadro in 4000:
					if not m.activo:
						break
					m.tiempo += 0.01
					m._paso(0.01)
				p.comprobar(not m.activo and m.tiempo < 40 and resultado.get("superado") == acierta, "seguidor.%s.d%d.auto_%s" % [modo, d, acierta], str(resultado))
				m.free()
	var regla: Control = _nuevo("normal", 1)
	regla.diales[0].value = 8
	regla.diales[1].value = 5
	regla._probar()
	p.comprobar(regla.pruebas == 0 and not regla.probando, "seguidor.bloquea_dos_cambios")
	regla._conservar(1)
	regla._probar()
	p.comprobar(regla.pruebas == 1 and regla.usados[0] == 16 and regla.usados[1] == 5, "seguidor.conserva_un_cambio")
	regla.free()
	var finales: Array[float] = []
	for delta in [1.0 / 30.0, 1.0 / 144.0, 0.19]:
		var m: Control = _nuevo("prealimentacion", 3)
		m.diales[2].value = 15
		m._probar()
		while m.probando:
			m._paso(delta)
		finales.append(m.posicion)
		m.free()
	p.comprobar(absf(finales[0] - finales[1]) < 0.000001 and absf(finales[0] - finales[2]) < 0.000001, "seguidor.paso_fijo_independiente_del_cuadro", str(finales))
	# El error de rampa sin anticipacion no desaparece por esperar mas.
	var sin_ff: Control = _nuevo("prealimentacion", 1)
	sin_ff._probar()
	while sin_ff.probando:
		sin_ff._paso(0.02)
	p.comprobar(sin_ff.error_final > 0.12 and sin_ff.error_final < 0.16, "seguidor.rampa_atraso_constante", str(sin_ff.error_final))
	sin_ff.free()
	p.comprobar(Juego.estado.get("cuaderno", []).has("prealimentacion"), "seguidor.anota_prealimentacion")
	var teclado: Control = _nuevo("normal", 1)
	Input.action_press("mover_derecha")
	for i in 60:
		teclado._paso(1.0 / 60.0)
	Input.action_release("mover_derecha")
	p.comprobar(teclado.valores[0] >= 20.5, "seguidor.teclado_acumula_pasos_del_dial", str(teclado.valores))
	teclado.free()
	if Juego.args.has("captura_seguidor"):
		await _captura(String(Juego.args["captura_seguidor"]))


func _nuevo(modo: String, d: int) -> Control:
	var m: Control = Seguidor.new()
	add_child(m)
	m.preparar({"modo": modo, "dificultad": d}, Juego.info_minijuego("seguidor"))
	m.set_process(false)
	m.empezar()
	return m


func _captura(ruta: String) -> void:
	var capa: CanvasLayer = CanvasLayer.new()
	add_child(capa)
	var fondo: ColorRect = ColorRect.new()
	fondo.color = Color("f6e7c8")
	fondo.size = Vector2(1280, 720)
	capa.add_child(fondo)
	var m: Control = _nuevo("prealimentacion", 3)
	m.reparent(capa)
	m.position = Vector2(80, 100)
	m._probar()
	while m.probando:
		m._paso(0.02)
	m.diales[2].value = 15
	m._probar()
	for i in 160:
		m._paso(0.02)
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var imagen: Image = get_viewport().get_texture().get_image()
	var error: Error = imagen.save_png(ruta)
	print("CAPTURA_SEGUIDOR ", ruta, " error=", error)
	capa.queue_free()
