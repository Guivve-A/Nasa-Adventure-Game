extends Node

# Mide que parte del barrio se ve por la ventana del fondo con la camara real (y la inclinacion 2.5D):
# proyecta las esquinas del vano a la pantalla y lanza el rayo de cada esquina hasta varias alturas del suelo
# de fuera. Escribe la huella en coordenadas del cuarto.
# Uso: python -I herramientas/juego_ejecutar.py -- --prueba=guion:<ruta de este archivo>

const PUNTOS := {
	"descanso": Vector3(3.0, 0.0, 2.2),
	"ventana": Vector3(0.1, 0.0, -1.9),
	"centro": Vector3(0.0, 0.0, 0.3),
	"esq_fondo_izq": Vector3(-2.6, 0.0, -0.6),
	"esq_frente_der": Vector3(2.0, 0.0, 2.3),
}
const ESQUINAS := [Vector3(-0.55, 0.85, -2.95), Vector3(0.75, 0.85, -2.95), Vector3(-0.55, 1.62, -2.7),
	Vector3(0.75, 1.62, -2.7), Vector3(0.1, 2.02, -2.7)]
const ALTURAS := [-0.91, -1.29, -2.03, -3.0]


func _esperar(s: float) -> void:
	await get_tree().create_timer(s).timeout


func correr(p: Node) -> void:
	Juego.nueva_partida()
	Juego.poner_bandera("visita_libre")
	Juego.poner_bandera("hab_saludo")
	Zonas.id_actual = ""
	var llego: bool = await Zonas.ir_a("habitacion", "inicio")
	p.comprobar(llego, "medir.carga")
	await _esperar(1.0)
	var z: Node3D = Zonas.actual
	var cam: Camera3D = Zonas.camara
	var inc: float = float(z.cizalla)
	var inv: Basis = z._base.inverse()
	for e in [0.20, 0.125]:
		for n in PUNTOS.keys():
			Zonas.jugador.colocar(z._m(PUNTOS[n]) + Vector3(0, 0.05, 0), Vector3(0, 0, 1))
			await _esperar(0.2)
			cam.encuadre = e
			cam.centrar()
			await _esperar(0.3)
			for i in ESQUINAS.size():
				var w: Vector3 = z._m(ESQUINAS[i])
				var s := Vector3(w.x, w.y, w.z - inc * w.y)
				var px: Vector2 = cam.unproject_position(s)
				var o: Vector3 = cam.project_ray_origin(px)
				var d: Vector3 = cam.project_ray_normal(px)
				var linea := "VISTA e=%.3f punto=%s esq=%d px=%d,%d" % [e, n, i, int(px.x), int(px.y)]
				for y in ALTURAS:
					var t: float = (float(y) - o.y) / d.y
					var q: Vector3 = o + d * t
					var real := Vector3(q.x, q.y, q.z + inc * q.y)
					var c: Vector3 = inv * real
					linea += " Y%.2f=(%.2f,%.2f)" % [y, c.x, c.z]
				print(linea)
	p.comprobar(true, "medir.hecho")
