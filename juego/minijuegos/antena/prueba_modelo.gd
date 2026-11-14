extends Node

const Antena = preload("res://minijuegos/antena/antena.gd")


func correr(pruebas: Node) -> void:
	for dificultad in [1, 2, 3]:
		for ganancia in [0.4, 1.2, 3.0, 12.0]:
			var nodo: Control = Antena.new()
			add_child(nodo)
			nodo.preparar({"dificultad": dificultad}, {})
			nodo.empezar()
			nodo.set_process(false)
			nodo._dial.value = ganancia
			nodo._probar()
			var cuadros: int = 0
			while nodo._corriendo and cuadros < 2400:
				nodo._process(1.0 / 144.0)
				cuadros += 1
			var util: float = nodo.sostenido / nodo.duracion
			print("BARRIDO d%d K=%.1f util=%.4f cruces=%d" % [dificultad, ganancia, util, nodo.cruces])
			pruebas.comprobar((util >= 0.8) == is_equal_approx(ganancia, 3.0), "antena.modelo.d%d.K%.1f" % [dificultad, ganancia])
			if ganancia == 12.0:
				pruebas.comprobar(nodo.cruces >= 5, "antena.d%d.ganancia_alta_oscila" % dificultad)
			var previo: PackedVector2Array = nodo._trazo.duplicate()
			if nodo.activo:
				nodo._probar()
				pruebas.comprobar(nodo._anterior == previo and nodo._trazo.size() == 1, "antena.d%d.K%.1f.compara_pruebas" % [dificultad, ganancia])
			else:
				var reintento: Control = Antena.new()
				add_child(reintento)
				reintento.preparar({"dificultad": dificultad}, {})
				pruebas.comprobar(reintento._anterior == previo, "antena.d%d.historial_al_reabrir" % dificultad)
				reintento.free()
			nodo.activo = false
			nodo.free()
	# El ajuste acumula fracciones: funciona tambien con cuadros muy cortos.
	var teclado: Control = Antena.new()
	add_child(teclado)
	teclado.preparar({}, {})
	teclado.empezar()
	teclado.set_process(false)
	for i in 144:
		teclado._ajustar(1.0, 1.0 / 144.0)
	pruebas.comprobar(is_equal_approx(teclado.ganancia, 7.2), "antena.teclado_144_cuadros")
	teclado.activo = false
	teclado.free()
	# El piloto completo pasa por el deslizador y las tres pruebas reales al fallar.
	for acierta in [true, false]:
		var piloto: Control = Antena.new()
		add_child(piloto)
		piloto.preparar({"dificultad": 2}, {})
		piloto.empezar()
		piloto.set_process(false)
		piloto.jugar_solo(acierta)
		var resultado: Dictionary = {}
		piloto.terminado.connect(func(r: Dictionary): resultado.merge(r, true))
		while piloto.activo and piloto.tiempo < 40.0:
			piloto._process(0.19)
		pruebas.comprobar(not piloto.activo and bool(resultado.get("superado", not acierta)) == acierta, "antena.d2.piloto_%s" % str(acierta))
		pruebas.comprobar(piloto.tiempo < 40.0, "antena.d2.piloto_limite_%s" % str(acierta))
		print("PILOTO d2 acierta=%s tiempo=%.3f" % [str(acierta), piloto.tiempo])
		piloto.free()
