extends Node

# Barrido del modelo de RASTREO sin anfitrion: el piloto juega las tres dificultades con cuadros cortos y
# largos, y se mide cuanto baja, cuanto dura y que el paso fijo no dependa de los cuadros por segundo.
#   python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/antena/prueba_modelo.gd --ritmo=8

const Antena = preload("res://minijuegos/antena/antena.gd")


func correr(pruebas: Node) -> void:
	for dificultad in [1, 2, 3]:
		var bajados: Array[int] = []
		for cuadro in [1.0 / 144.0, 1.0 / 30.0, 0.27]:
			var r: Dictionary = _partida(dificultad, true, cuadro)
			var nodo_paquetes: int = r["paquetes"]
			bajados.append(nodo_paquetes)
			print("RASTREO d%d cuadro=%.4f paquetes=%d meta=%d enlace=%.0f%% perdidos=%d comidos=%d reloj=%.1f s" % [dificultad, cuadro, nodo_paquetes, r["cuota"], r["enlace"], r["perdidos"], r["comidos"], r["tiempo"]])
			pruebas.comprobar(bool(r["superado"]), "antena.modelo.d%d.piloto_supera_cuadro_%.4f" % [dificultad, cuadro], str(r))
			pruebas.comprobar(float(r["tiempo"]) < 40.0, "antena.modelo.d%d.piloto_menos_de_40_s" % dificultad, "%.1f s" % float(r["tiempo"]))
		pruebas.comprobar(absi(bajados[0] - bajados[2]) <= 3, "antena.modelo.d%d.paso_fijo_no_depende_de_los_cuadros" % dificultad, str(bajados))
		var mal: Dictionary = _partida(dificultad, false, 1.0 / 30.0)
		print("RASTREO d%d piloto que suelta: paquetes=%d meta=%d enlace=%.0f%% detalle=%s" % [dificultad, mal["paquetes"], mal["cuota"], mal["enlace"], mal["detalle"]])
		pruebas.comprobar(not bool(mal["superado"]) and int(mal["paquetes"]) < int(mal["cuota"]), "antena.modelo.d%d.soltar_el_mando_no_alcanza" % dificultad, str(mal))
		pruebas.comprobar(not String(mal["detalle"]).to_lower().contains("incorrect"), "antena.modelo.d%d.el_fallo_explica_la_causa" % dificultad, String(mal["detalle"]))
	# sin tocar nada no baja la meta: el plato quieto solo roza al satelite cuando pasa por el cenit
	var quieto: Control = Antena.new()
	add_child(quieto)
	quieto.preparar({"dificultad": 1}, {})
	quieto.empezar()
	quieto.set_process(false)
	quieto._auto = 2      # ni teclas ni piloto: mando queda en 0
	var resultado: Dictionary = {}
	quieto.terminado.connect(func(r: Dictionary): resultado.merge(r, true))
	var vueltas: int = 0
	while quieto.activo and vueltas < 20000:
		quieto._paso(1.0 / 30.0)
		vueltas += 1
	print("RASTREO d1 plato quieto: paquetes=%d meta=%d" % [quieto.paquetes, quieto.cuota])
	pruebas.comprobar(not quieto.activo and not bool(resultado.get("superado", true)), "antena.modelo.plato_quieto_no_gana", str(resultado))
	quieto.free()


func _partida(dificultad: int, acierta: bool, cuadro: float) -> Dictionary:
	var nodo: Control = Antena.new()
	add_child(nodo)
	nodo.preparar({"dificultad": dificultad}, {})
	nodo.empezar()
	nodo.set_process(false)
	nodo.jugar_solo(acierta)
	var resultado: Dictionary = {}
	nodo.terminado.connect(func(r: Dictionary): resultado.merge(r, true))
	var reloj: float = 0.0
	while nodo.activo and reloj < 200.0:
		nodo._paso(cuadro)
		reloj += cuadro
	var salida: Dictionary = {
		"superado": bool(resultado.get("superado", false)), "paquetes": int(nodo.paquetes), "cuota": int(nodo.cuota),
		"enlace": 100.0 * float(nodo.t_enlace) / maxf(float(nodo.t_visible), 0.01), "perdidos": int(nodo.perdidos),
		"comidos": int(nodo.comidos), "tiempo": reloj, "detalle": String(resultado.get("detalle", "")),
	}
	nodo.free()
	return salida
