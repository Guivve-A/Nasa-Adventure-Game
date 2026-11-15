extends Node

# Pruebas de reglas propias; no cambia el anfitrion ni el estado global.
const Guion := preload("res://minijuegos/banderas/banderas.gd")
var resultado: Dictionary = {}


func _nuevo(d: int = 1) -> Control:
	var m: Control = Guion.new()
	add_child(m)
	m.preparar({"dificultad": d}, {})
	m.set_process(false)
	m.terminado.connect(func(r: Dictionary): resultado = r)
	m.empezar()
	return m


func correr(p: Node) -> void:
	var m: Control = _nuevo()
	m.seleccion = 0
	m._accion()
	p.comprobar(m.paso == 0 and m.revisiones == 0 and m.activo and m.mensaje.contains("no es una ley"), "banderas.anillo_sin_castigo")
	m.seleccion = 1
	m._accion()
	p.comprobar(m.paso == 0 and m.mensaje.contains("huellas"), "banderas.huellas_se_conservan")
	m.seleccion = 2
	m._accion()
	m.seleccion = 2
	m._accion()
	p.comprobar(m.armado[0] == 0, "banderas.tela_necesita_soporte")
	m.free()
	for d in [1, 2, 3]:
		for acierta in [true, false]:
			resultado = {}
			m = _nuevo(d)
			m.jugar_solo(acierta)
			var segundos: float = 0.0
			var inicio_ceremonia: float = -1.0
			while m.activo and segundos < 39.9:
				var dt: float = 1.0 / 60.0
				segundos += dt
				m.tiempo += dt
				m._paso(dt)
				if m.paso == 5 and inicio_ceremonia < 0.0:
					inicio_ceremonia = segundos
			p.comprobar(not m.activo and resultado.get("superado", false) == acierta, "banderas.piloto_d%d_%s" % [d, str(acierta)])
			print("BANDERAS_TIEMPO d=%d acierta=%s segundos=%.3f" % [d, str(acierta), segundos])
			if acierta:
				p.comprobar(m.armado == [3, 3] and m.golpes[0] >= m.necesarios and m.golpes[1] >= m.necesarios, "banderas.soportes_reales_d%d" % d)
				p.comprobar(m.extension == [1.0, 1.0] and absf(m.alturas[0] - m.alturas[1]) <= 2.0 and m.separacion >= 190.0 and m.separacion <= 250.0, "banderas.ajuste_real_d%d" % d)
				p.comprobar(segundos - inicio_ceremonia >= 4.5, "banderas.amanecer_y_3s_d%d" % d)
			else:
				p.comprobar(m.revisiones == 3 and m.extension[0] < 1.0 and String(resultado.get("detalle", "")).contains("no hay viento"), "banderas.fallo_real_d%d" % d)
			m.free()
