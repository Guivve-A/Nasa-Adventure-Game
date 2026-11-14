extends RefCounted

# Piezas low-poly por script, con caras planas y color de vertice (shader facetado):
# rocas, etapa de descenso generica y marcador de escala de 1,05 m.
# La etapa de descenso es solo volumen: patas, base octogonal dorada y gris. Sin insignias, banderas,
# textos ni logotipos.


class Constructor:
	var v := PackedVector3Array()
	var nr := PackedVector3Array()
	var c := PackedColorArray()

	func tri(a: Vector3, b: Vector3, d: Vector3, color: Color, centro: Vector3) -> void:
		# Godot toma como frente el sentido horario visto desde fuera: (b-a)x(d-a) apunta hacia dentro.
		# Se ordena cada triangulo para que mire hacia fuera del centro de su pieza (piezas convexas).
		var cruz := (b - a).cross(d - a)
		if cruz.length_squared() < 1e-12:
			return
		var cg := (a + b + d) / 3.0
		if (-cruz).dot(cg - centro) < 0.0:
			var t := b
			b = d
			d = t
			cruz = -cruz
		var fuera := (-cruz).normalized()
		color = color.srgb_to_linear()  # el shader usa COLOR tal cual: se guarda en lineal
		v.append_array([a, b, d])
		nr.append_array([fuera, fuera, fuera])
		c.append_array([color, color, color])

	func cuad(a: Vector3, b: Vector3, d: Vector3, e: Vector3, color: Color, centro: Vector3) -> void:
		tri(a, b, d, color, centro)
		tri(a, d, e, color, centro)

	func prisma(puntos: Array, y0: float, y1: float, color_lado: Callable, tapa: Color, fondo: Color) -> void:
		# poligono convexo en XZ (Vector2) extruido de y0 a y1
		var centro := Vector3.ZERO
		for p in puntos:
			centro += Vector3(p.x, 0.0, p.y)
		centro /= puntos.size()
		var medio := centro + Vector3(0.0, (y0 + y1) * 0.5, 0.0)
		for i in puntos.size():
			var p: Vector2 = puntos[i]
			var q: Vector2 = puntos[(i + 1) % puntos.size()]
			cuad(Vector3(p.x, y0, p.y), Vector3(q.x, y0, q.y), Vector3(q.x, y1, q.y), Vector3(p.x, y1, p.y), color_lado.call(i), medio)
			tri(centro + Vector3(0, y1, 0), Vector3(p.x, y1, p.y), Vector3(q.x, y1, q.y), tapa, medio)
			tri(centro + Vector3(0, y0, 0), Vector3(p.x, y0, p.y), Vector3(q.x, y0, q.y), fondo, medio)

	func barra(p0: Vector3, p1: Vector3, grosor: float, color: Color) -> void:
		# prisma de seccion cuadrada entre dos puntos (puntales de las patas)
		var eje := (p1 - p0).normalized()
		var u := eje.cross(Vector3.UP)
		if u.length_squared() < 1e-6:
			u = Vector3.RIGHT
		u = u.normalized() * grosor * 0.5
		var w := eje.cross(u).normalized() * grosor * 0.5
		var esquinas := [u + w, -u + w, -u - w, u - w]
		var medio := (p0 + p1) * 0.5
		for i in 4:
			var a: Vector3 = esquinas[i]
			var b: Vector3 = esquinas[(i + 1) % 4]
			cuad(p0 + a, p0 + b, p1 + b, p1 + a, color, medio)
		cuad(p0 + esquinas[0], p0 + esquinas[1], p0 + esquinas[2], p0 + esquinas[3], color, medio)
		cuad(p1 + esquinas[0], p1 + esquinas[1], p1 + esquinas[2], p1 + esquinas[3], color, medio)

	func malla() -> ArrayMesh:
		var arrays := []
		arrays.resize(Mesh.ARRAY_MAX)
		arrays[Mesh.ARRAY_VERTEX] = v
		arrays[Mesh.ARRAY_NORMAL] = nr
		arrays[Mesh.ARRAY_COLOR] = c
		var m := ArrayMesh.new()
		m.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
		return m


static func poligono(lados: int, radio: float, giro_deg: float) -> Array:
	var p := []
	for i in lados:
		var a := deg_to_rad(giro_deg + 360.0 * i / lados)
		p.append(Vector2(cos(a), sin(a)) * radio)
	return p


static func roca(rng: RandomNumberGenerator, gris: float) -> ArrayMesh:
	# icosaedro deformado de 20 caras, aplastado y con la base plana; mide unos 1 m de ancho
	var t := (1.0 + sqrt(5.0)) / 2.0
	var base := [Vector3(-1, t, 0), Vector3(1, t, 0), Vector3(-1, -t, 0), Vector3(1, -t, 0),
		Vector3(0, -1, t), Vector3(0, 1, t), Vector3(0, -1, -t), Vector3(0, 1, -t),
		Vector3(t, 0, -1), Vector3(t, 0, 1), Vector3(-t, 0, -1), Vector3(-t, 0, 1)]
	var caras := [[0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11], [1, 5, 9], [5, 11, 4],
		[11, 10, 2], [10, 7, 6], [7, 1, 8], [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
		[4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]]
	var pts := []
	for p in base:
		var q: Vector3 = p.normalized() * rng.randf_range(0.78, 1.15) * 0.5
		q.y = maxf(q.y * 0.72, -0.2)
		pts.append(q)
	var k := Constructor.new()
	for f in caras:
		var a: Vector3 = pts[f[0]]
		var b: Vector3 = pts[f[1]]
		var d: Vector3 = pts[f[2]]
		var arriba := ((a + b + d) / 3.0).normalized().y
		var g := gris * rng.randf_range(0.9, 1.08) * lerpf(0.82, 1.0, arriba * 0.5 + 0.5)
		k.tri(a, b, d, Color(g, g * 0.98, g * 0.95), Vector3.ZERO)
	return k.malla()


static func etapa_descenso() -> ArrayMesh:
	# Proporciones aproximadas de una etapa de descenso: cuerpo octogonal de 4,2 m entre caras planas,
	# patas abiertas hasta unos 9,2 m entre zapatas opuestas, altura total cercana a 3 m.
	var k := Constructor.new()
	var oro := [Color("d4a537"), Color("c18f2a"), Color("e3bd57"), Color("b07f22")]
	var gris := [Color("9a9b9e"), Color("8a8b8e"), Color("adaeb0"), Color("7e7f82")]
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	var radio := 2.1 / cos(deg_to_rad(22.5))
	var y0 := 1.05
	var y1 := 2.7
	var oct := poligono(8, radio, 22.5)  # caras planas hacia los ejes y las diagonales
	var centro_cuerpo := Vector3(0.0, (y0 + y1) * 0.5, 0.0)
	# paneles laterales: oro y gris alternos, cada uno en 2 x 2 facetas con el centro abombado (lamina arrugada)
	for i in 8:
		var p: Vector2 = oct[i]
		var q: Vector2 = oct[(i + 1) % 8]
		var paleta: Array = oro if i % 2 == 0 else gris
		var normal := Vector3((p.x + q.x) * 0.5, 0.0, (p.y + q.y) * 0.5).normalized()
		for fila in 2:
			for col in 2:
				var a0 := Vector3(lerpf(p.x, q.x, col * 0.5), lerpf(y0, y1, fila * 0.5), lerpf(p.y, q.y, col * 0.5))
				var a1 := Vector3(lerpf(p.x, q.x, (col + 1) * 0.5), lerpf(y0, y1, fila * 0.5), lerpf(p.y, q.y, (col + 1) * 0.5))
				var a2 := Vector3(a1.x, lerpf(y0, y1, (fila + 1) * 0.5), a1.z)
				var a3 := Vector3(a0.x, a2.y, a0.z)
				var m := (a0 + a1 + a2 + a3) * 0.25 + normal * rng.randf_range(0.02, 0.07)
				var lados := [a0, a1, a2, a3]
				for s in 4:
					k.tri(lados[s], lados[(s + 1) % 4], m, paleta[rng.randi() % 4], centro_cuerpo)
	# cubierta superior y fondo
	for i in 8:
		var p: Vector2 = oct[i]
		var q: Vector2 = oct[(i + 1) % 8]
		k.tri(Vector3(0, y1, 0), Vector3(p.x, y1, p.y), Vector3(q.x, y1, q.y), Color("a3a19c"), centro_cuerpo)
		k.tri(Vector3(0, y0, 0), Vector3(p.x, y0, p.y), Vector3(q.x, y0, q.y), Color("55534f"), centro_cuerpo)
	# bloque central sobre la cubierta (volumen, sin detalle)
	k.prisma(poligono(4, 0.95, 45.0), y1, y1 + 0.28, func(_i): return Color("86847f"), Color("97958f"), Color("6d6b66"))
	# tobera del motor bajo el cuerpo: tronco de cono de 8 lados
	var arriba := poligono(8, 0.42, 0.0)
	var abajo := poligono(8, 0.78, 0.0)
	var yb := y0 - 0.6
	var centro_tobera := Vector3(0, (y0 + yb) * 0.5, 0)
	for i in 8:
		var a: Vector2 = arriba[i]
		var b: Vector2 = arriba[(i + 1) % 8]
		var d: Vector2 = abajo[(i + 1) % 8]
		var e: Vector2 = abajo[i]
		k.cuad(Vector3(a.x, y0, a.y), Vector3(b.x, y0, b.y), Vector3(d.x, yb, d.y), Vector3(e.x, yb, e.y), Color("4d4c49") if i % 2 == 0 else Color("5a5955"), centro_tobera)
		k.tri(Vector3(0, yb, 0), Vector3(e.x, yb, e.y), Vector3(d.x, yb, d.y), Color("2f2e2c"), centro_tobera)
	# cuatro patas en las diagonales: puntal principal, dos puntales secundarios y zapata
	for pata in 4:
		var ang := deg_to_rad(45.0 + 90.0 * pata)
		var dir := Vector3(cos(ang), 0.0, sin(ang))
		var lateral := Vector3(-dir.z, 0.0, dir.x)
		var arriba_pata := dir * 2.05 + Vector3(0, 2.35, 0)
		var zapata := dir * 4.6
		var tobillo := zapata + Vector3(0, 0.22, 0)
		k.barra(arriba_pata, tobillo, 0.17, Color("b8902f"))
		var union := arriba_pata.lerp(tobillo, 0.72)
		for lado in [-1.0, 1.0]:
			k.barra(dir * 1.95 + lateral * 0.9 * lado + Vector3(0, 1.12, 0), union, 0.09, Color("a9a8a3"))
		var disco := []
		for p in poligono(8, 0.46, 0.0):
			disco.append(p + Vector2(zapata.x, zapata.z))
		k.prisma(disco, 0.0, 0.22, func(i): return Color("b9b6ae") if i % 2 == 0 else Color("a7a49c"), Color("c4c1b9"), Color("6e6c67"))
	return k.malla()


static func marcador() -> ArrayMesh:
	# poste de escala de 1,05 m (alto del personaje en la escena del sendero): 5 franjas de 0,21 m
	var k := Constructor.new()
	var seccion := poligono(4, 0.07, 45.0)
	for f in 5:
		var color := Color("e8743b") if f % 2 == 0 else Color("f3e6cb")
		k.prisma(seccion, f * 0.21, (f + 1) * 0.21, func(_i): return color, color, color)
	k.prisma(poligono(8, 0.16, 0.0), 0.0, 0.02, func(_i): return Color("4a4844"), Color("5a5853"), Color("3a3936"))
	return k.malla()
