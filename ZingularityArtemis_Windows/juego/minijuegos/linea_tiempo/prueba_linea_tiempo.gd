extends Node

const Minijuego = preload("res://minijuegos/linea_tiempo/linea_tiempo.gd")
var _resultado: Dictionary = {}

func _crear(nivel: int) -> Control:
	var mj: Control = Minijuego.new()
	add_child(mj)
	mj.preparar({"dificultad": nivel}, {})
	mj.terminado.connect(func(r: Dictionary): _resultado = r)
	_resultado = {}
	mj.empezar()
	mj.set_process(false)
	return mj

func correr(pruebas: Node) -> void:
	for nivel in [1, 2, 3]:
		for acierta in [true, false]:
			var mj: Control = _crear(nivel)
			var anios: Array[int] = []
			for hito in mj.hitos:
				anios.append(int(hito["anio"]))
			pruebas.comprobar(anios == [1873, 1957, 1969, 1975, 1981, 1982, 2007, 2013, 2023], "linea.modelo.d%d.anios_de_fichas" % nivel)
			var ocultas: bool = true
			for placa in mj.placas:
				ocultas = ocultas and not bool(placa["revelada"])
			pruebas.comprobar(ocultas, "linea.modelo.d%d.fechas_ocultas" % nivel)
			mj.jugar_solo(acierta)
			for cuadro in 799:
				if not mj.activo:
					break
				mj._process(0.05)
			pruebas.comprobar(not mj.activo and bool(_resultado.get("superado", not acierta)) == acierta and mj.tiempo < 40.0, "linea.modelo.d%d.auto_%s_menos40" % [nivel, str(acierta)], str(_resultado))
			print("LINEA_MODELO nivel=%d acierta=%s tiempo=%.2f vidas=%d" % [nivel, str(acierta), mj.tiempo, mj.vidas])
			mj.free()
	var juego: Control = _crear(1)
	juego.fase = 1
	juego.jugadora = Vector2(160, 65)
	# Estar sobre una placa sin saltar no revela el anio.
	for i in 12:
		juego._tic(1.0 / 120.0)
	pruebas.comprobar(juego.siguiente == 0, "linea.modelo.caminar_no_activa")
	var evento: InputEventAction = InputEventAction.new()
	evento.action = "saltar"
	evento.pressed = true
	juego._input(evento)
	for i in 100:
		juego._tic(1.0 / 120.0)
	pruebas.comprobar(juego.siguiente == 1, "linea.modelo.aterrizar_revela")
	juego.free()
	for volando in [false, true]:
		juego = _crear(1)
		juego.fase = 1
		juego.salto = 0.4 if volando else 0.0
		juego.peligros.append({"pos": juego.jugadora, "vel": Vector2.ZERO, "coco": true})
		juego._tic(1.0 / 120.0)
		pruebas.comprobar(juego.vidas == (3 if volando else 2), "linea.modelo.salto_evade_%s" % str(volando))
		juego.free()
	juego = _crear(3)
	juego.fase = 1
	juego.reloj = juego.limite - 0.001
	juego._tic(0.01)
	for i in 150:
		juego._tic(0.01)
	pruebas.comprobar(not juego.activo and not bool(_resultado.get("superado", true)), "linea.modelo.tiempo_agotado")
	juego.free()
