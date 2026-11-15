extends Node

const Orbita := preload("res://minijuegos/orbita/orbita.gd")


func _simular(nivel: int, bien: bool, delta: float) -> Dictionary:
	var m: Control = Orbita.new()
	add_child(m)
	m.preparar({"dificultad": nivel}, Juego.info_minijuego("orbita"))
	m.empezar()
	m.set_process(false)
	m.jugar_solo(bien)
	var salida: Dictionary = {}
	m.terminado.connect(func(r: Dictionary): salida.merge(r))
	while m.activo and m.tiempo < 39.0:
		m.tiempo += delta
		m._paso(delta)
	salida["anillos"] = m.anillos
	salida["fuel"] = m.combustible
	salida["min"] = m.minima
	salida["max"] = m.maxima
	salida["reloj"] = m.reloj
	m.free()
	return salida


func correr(p: Node) -> void:
	for nivel in [1, 2, 3]:
		var r: Dictionary = _simular(nivel, true, 1.0 / 60.0)
		p.comprobar(bool(r.get("superado", false)) and float(r.get("tiempo", 99.0)) < 40.0, "orbita.modelo.d%d" % nivel, str(r))
		p.comprobar(int(r["anillos"]) == 5 + nivel and float(r["fuel"]) >= 0.0 and float(r["reloj"]) >= 60.0, "orbita.reglas.d%d" % nivel, str(r))
	var a: Dictionary = _simular(2, true, 0.017)
	var b: Dictionary = _simular(2, true, 0.13)
	p.comprobar(absf(float(a["min"]) - float(b["min"])) < 0.01 and absf(float(a["max"]) - float(b["max"])) < 0.01, "orbita.paso_fijo", str([a, b]))
	var mal: Dictionary = _simular(1, false, 0.05)
	p.comprobar(not bool(mal.get("superado", true)) and str(mal.get("detalle", "")).contains("atm"), "orbita.frenar_cae", str(mal))
	var m: Control = Orbita.new()
	add_child(m)
	m.preparar({}, Juego.info_minijuego("orbita"))
	var g1: Vector2 = m._gravedad(Vector2(7000, 0))
	var g2: Vector2 = m._gravedad(Vector2(14000, 0))
	p.comprobar(g1.x < 0.0 and absf(g1.length() / g2.length() - 4.0) < 0.0001, "orbita.gravedad_inverso_cuadrado")
	p.comprobar(m.pegaso_baja > 0.0 and m.pegaso_alta > m.pegaso_baja, "orbita.alturas_desde_ficha")
	m.free()
