extends Node

# Bordes del modelo aparte de la prueba de teclado por el anfitrion.
const Minijuego := preload("res://minijuegos/muestras/muestras.gd")
var resultado: Dictionary = {}


func _crear(parametros: Dictionary) -> Control:
	var m: Control = Minijuego.new()
	add_child(m)
	resultado = {}
	m.terminado.connect(func(r: Dictionary): resultado = r)
	m.preparar(parametros, Juego.info_minijuego("muestras"))
	m.empezar()
	m.set_process(false)
	return m


func _avanzar(m: Control, segundos: float) -> void:
	var restante: float = segundos
	while restante > 0.000001 and m.activo:
		var dt: float = minf(1.0 / 60.0, restante)
		restante -= dt
		m.tiempo += dt
		m._paso(dt)


func correr(pruebas: Node) -> void:
	for d in [1, 2, 3]:
		for indice in [-1, 0, 1, 2, 3]:
			for acierta in [true, false]:
				var m: Control = _crear({"dificultad": d, "muestra": indice})
				m.jugar_solo(acierta)
				_avanzar(m, 39.9)
				pruebas.comprobar(not m.activo and bool(resultado.get("superado", false)) == acierta, "muestras.modelo.d%d.m%d.%s" % [d, indice, str(acierta)], "t=%.2f %s" % [m.tiempo, str(resultado)])
				if acierta:
					pruebas.comprobar(m.entregadas.size() == (4 if indice == -1 else 1), "muestras.modelo.entregadas.d%d.m%d" % [d, indice])
				m.free()
	for indice in 4:
		var m: Control = _crear({"muestra": indice})
		m.fase = 1
		m.posicion = Minijuego.SITIOS[indice]
		m.herramienta = (Minijuego.UTILES[indice] + 1) % 3
		m._cercania()
		var muestra: Dictionary = m.muestras[0]
		m._escapar(muestra)
		pruebas.comprobar(m.vidas == 2 and m.carga == -1 and Vector2(muestra["v"]).length() > 0.0 and float(muestra["espera"]) > 0, "muestras.modelo.herramienta_deja_escapar_%d" % indice)
		m.jugar_solo(true)
		_avanzar(m, 39.9)
		pruebas.comprobar(bool(resultado.get("superado", false)), "muestras.modelo.recupera_muestra_%d" % indice, str(resultado))
		m.free()
	var m: Control = _crear({})
	_avanzar(m, 109.0)
	pruebas.comprobar(not m.activo and not bool(resultado.get("superado", true)) and str(resultado.get("detalle", "")).contains("oxígeno"), "muestras.modelo.oxigeno_agotado", str(resultado))
	m.free()
	m = _crear({})
	pruebas.comprobar(is_equal_approx(m.gravedad, 1.624 * 40.0) and m.fraccion == "1/6", "muestras.modelo.gravedad_desde_ficha")
	m.fase = 1
	m.mando = Vector2.RIGHT
	m._tic(0.1)
	var antes: Vector2 = m.posicion
	m.mando = Vector2.ZERO
	m._tic(0.01)
	pruebas.comprobar(m.posicion.x > antes.x and m.altura > 0.0, "muestras.modelo.salto_con_inercia")
	m.free()
	await get_tree().create_timer(1.0, true, false, true).timeout
