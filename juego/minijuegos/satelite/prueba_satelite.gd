extends Node

# Regresion arcade: delta variable, ciclo normal y perdida causal.
const Satelite := preload("res://minijuegos/satelite/satelite.gd")


func _nuevo(nivel: int) -> Control:
	var m: Control = Satelite.new()
	add_child(m)
	m.preparar({"dificultad": nivel, "semilla": 5346}, {})
	m.set_process(false)
	m.empezar()
	return m


func correr(p: Node) -> void:
	for nivel in [1, 2, 3]:
		var tiempos: Array[float] = []
		for delta in [0.016, 0.37]:
			var m: Control = _nuevo(nivel)
			var resultados: Array[Dictionary] = []
			m.terminado.connect(func(r: Dictionary): resultados.append(r))
			m.jugar_solo(true)
			while m.activo and m.tiempo < 40.0:
				m._process(delta)
			var r: Dictionary = resultados[0] if not resultados.is_empty() else {}
			p.comprobar(bool(r.get("superado", false)), "satelite.modelo.d%d.delta_%s" % [nivel, str(delta)], str(r))
			p.comprobar(m._cm_cubo == 10 and m._cm_panel == 27 and not m._dato.is_empty(), "satelite.modelo.dimensiones_desde_json")
			tiempos.append(float(r.get("tiempo", 99.0)))
			m.free()
		p.comprobar(absf(tiempos[0] - tiempos[1]) < 0.4, "satelite.modelo.d%d.delta_estable" % nivel, str(tiempos))
	# Una partida normal usa exactamente la misma cinta sin accionar la palanca rapida.
	for nivel in [1, 2, 3]:
		var normal: Control = _nuevo(nivel)
		normal._auto = 1
		var resultados: Array[Dictionary] = []
		normal.terminado.connect(func(r: Dictionary): resultados.append(r))
		for i in 14000:
			if not normal.activo:
				break
			normal.tiempo += normal.DT
			normal._piloto()
			normal.turbo = false
			normal._tic(normal.DT)
		var r: Dictionary = resultados[0] if not resultados.is_empty() else {}
		p.comprobar(bool(r.get("superado", false)) and normal.tiempo >= 60.0 and normal.tiempo <= 120.0, "satelite.modelo.d%d.partida_normal_60_a_120s" % nivel, str(r))
		print("SATELITE_NORMAL d%d segundos=%.3f" % [nivel, normal.tiempo])
		normal.free()
	# Quedarse quieto pierde por golpes o tiempo; las piezas no desaparecen para siempre.
	var quieto: Control = _nuevo(2)
	var perdidas: Array[Dictionary] = []
	quieto.terminado.connect(func(resultado: Dictionary): perdidas.append(resultado))
	var recircula: bool = false
	while quieto.activo and quieto.tiempo < 110.0:
		quieto._process(0.1)
		recircula = recircula or quieto._aviso == "PIEZA RECIRCULANDO"
	p.comprobar(recircula, "satelite.modelo.pieza_perdida_recircula")
	var perdida: Dictionary = perdidas[0] if not perdidas.is_empty() else {}
	p.comprobar(not perdida.is_empty() and not bool(perdida.get("superado", true)) and str(perdida.get("detalle", "")).length() > 20, "satelite.modelo.inaccion_pierde_con_causa", str(perdida))
	quieto.free()
