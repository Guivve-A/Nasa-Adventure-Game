extends Node

# Pruebas del modelo; las entradas reales se verifican en prueba_manos.gd.
const Minijuego = preload("res://minijuegos/telescopio/telescopio.gd")


func correr(p: Node) -> void:
	for nivel in [1, 2, 3]:
		var m: Control = Minijuego.new()
		add_child(m)
		m.preparar({"dificultad": nivel}, Juego.info_minijuego("telescopio"))
		var r: Dictionary = {}
		m.terminado.connect(func(final: Dictionary): r.merge(final))
		m.empezar()
		m.jugar_solo(true)
		while m.activo and m.tiempo < 40:
			await get_tree().process_frame
		p.comprobar(bool(r.get("superado", false)) and m.rasgo == 3 and m.tiempo < 40, "telescopio.modelo.d%d.piloto_reglas_reales" % nivel, str(r))
		p.comprobar(m.iluminacion > 0 and m.altura > 0, "telescopio.modelo.d%d.datos_fichas" % nivel)
		m.activo = false
		m.queue_free()
		await get_tree().process_frame
	var m: Control = Minijuego.new()
	add_child(m)
	m.preparar({}, Juego.info_minijuego("telescopio"))
	m.empezar()
	var r: Dictionary = {}
	m.terminado.connect(func(final: Dictionary): r.merge(final))
	m.reloj = m.limite
	m._paso(0.1)
	while m.activo:
		await get_tree().process_frame
	p.comprobar(not bool(r.get("superado", true)) and String(r.get("detalle", "")).contains("ventana"), "telescopio.modelo.reloj_agotado")
	m.queue_free()
