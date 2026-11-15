extends Node2D

# Fondo con parallax por capas. Sirve para la Luna y para Marte: solo cambia la carpeta.
# Cada capa es un PNG de 640 x 360 que se repite en horizontal, con estos nombres:
#   capa_0_espacio, capa_0b_sol_tierra, capa_1_montanas_lejanas, capa_2_montanas_medias, capa_3_colinas_cercanas
# Si falta un PNG, esa capa se dibuja como una silueta lisa (reserva), para poder jugar antes de tener el arte.

const CAPAS := [["capa_0_espacio", 0.02], ["capa_0b_sol_tierra", 0.06], ["capa_1_montanas_lejanas", 0.18], ["capa_2_montanas_medias", 0.35], ["capa_3_colinas_cercanas", 0.6]]
const ANCHO := 640.0
const ALTO := 360.0


# carpeta: donde estan los PNG. reserva: un color por capa. Devuelve cuantas capas tenian su PNG.
func armar(carpeta: String, reserva: Array = [], corrimiento_astros := 0.0) -> int:
	var cargadas := 0
	for i in CAPAS.size():
		var p := Parallax2D.new()
		p.scroll_scale = Vector2(CAPAS[i][1], 0.0)
		p.repeat_size = Vector2(ANCHO, 0.0)
		p.repeat_times = 3
		if i == 1:
			p.scroll_offset = Vector2(corrimiento_astros, 0.0)
		add_child(p)
		var ruta: String = carpeta + "/" + CAPAS[i][0] + ".png"
		if ResourceLoader.exists(ruta):
			var s := Sprite2D.new()
			s.texture = load(ruta)
			s.centered = false
			p.add_child(s)
			cargadas += 1
		elif i < reserva.size():
			p.add_child(_silueta(i, reserva[i]))
	return cargadas


func _silueta(i: int, color: Color) -> Node2D:
	var pol := Polygon2D.new()
	pol.color = color
	var pts := PackedVector2Array()
	if i == 0:
		pts = PackedVector2Array([Vector2(0, 0), Vector2(ANCHO, 0), Vector2(ANCHO, ALTO), Vector2(0, ALTO)])
	elif i == 1:
		# un sol pequeno: desde Marte el Sol se ve mas chico que desde la Tierra
		for k in 16:
			pts.append(Vector2(110, 120) + Vector2.from_angle(TAU * k / 16.0) * 7.0)
	else:
		var base := [0.0, 0.0, 190.0, 232.0, 268.0][i] as float
		var amp := [0.0, 0.0, 34.0, 24.0, 14.0][i] as float
		for x in range(0, int(ANCHO) + 1, 8):
			var a := TAU * x / ANCHO
			pts.append(Vector2(x, base - amp * (sin(a * (i - 1)) + 0.5 * sin(a * 3.0 * i + i))))
		pts.append(Vector2(ANCHO, ALTO))
		pts.append(Vector2(0, ALTO))
	pol.polygon = pts
	return pol
