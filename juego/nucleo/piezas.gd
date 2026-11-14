extends RefCounted

# Mallas low-poly hechas por codigo, con color de vertice y caras planas, para los shaders pintados
# (facetado, follaje). Cada cara lleva un tono propio: mas claro si mira hacia arriba, mas oscuro si mira
# hacia abajo (el «degradado por faceta» de la Biblia de arte). Las caras se orientan solas hacia fuera.
#
# Uso:
#   var m := Piezas.nueva()
#   Piezas.caja(m, Vector3(0, 0.4, 0), Vector3(1.2, 0.8, 0.6), Color("836258"))
#   Piezas.prisma(m, Vector3(0, 0.8, 0), 0.3, 0.5, 6, Color("d09880"))
#   var nodo := Piezas.nodo(m)        # MeshInstance3D con el material facetado de la zona
#
# Para mallas con mas detalle (muebles finos, vegetacion) se pueden generar GLB con herramientas/mallas/nucleo.py.

const Materiales := preload("res://nucleo/materiales.gd")


static func nueva() -> Dictionary:
	return {"v": [], "n": [], "c": []}


static func _tono(color: Color, normal: Vector3) -> Color:
	# los colores se escriben en sRGB (los hex de la paleta maestra) y el shader los quiere en lineal,
	# igual que los GLB de herramientas/mallas/nucleo.py
	var f := 1.0 + 0.10 * normal.y + 0.035 * normal.x - 0.02 * normal.z
	var lineal := Color(clampf(color.r * f, 0.0, 1.0), clampf(color.g * f, 0.0, 1.0), clampf(color.b * f, 0.0, 1.0), color.a).srgb_to_linear()
	return lineal


static func cara(m: Dictionary, puntos: Array, color: Color, interior: Vector3 = Vector3.INF) -> void:
	# poligono plano y convexo. "interior" es un punto de dentro de la pieza: la cara se orienta al lado contrario.
	# Sin "interior", vale el orden de los puntos (regla de la mano derecha: sentido antihorario visto desde fuera).
	if puntos.size() < 3:
		return
	var a: Vector3 = puntos[0]
	var b: Vector3 = puntos[1]
	var c: Vector3 = puntos[2]
	var n := (b - a).cross(c - a)
	if n.length() < 0.0000001:
		return
	n = n.normalized()
	var orden := puntos
	if interior != Vector3.INF:
		var centro := Vector3.ZERO
		for p in puntos:
			centro += p
		centro /= float(puntos.size())
		if n.dot(centro - interior) < 0.0:
			n = -n
			orden = puntos.duplicate()
			orden.reverse()
	var tono := _tono(color, n)
	for i in range(1, orden.size() - 1):
		# en Godot la cara frontal va en sentido horario
		for p in [orden[0], orden[i + 1], orden[i]]:
			m["v"].append(p)
			m["n"].append(n)
			m["c"].append(tono)


static func caja(m: Dictionary, centro: Vector3, tam: Vector3, color: Color, giro_grados: float = 0.0, color_arriba: Variant = null) -> void:
	var h := tam * 0.5
	var base := Basis(Vector3.UP, deg_to_rad(giro_grados))
	var p: Array = []
	for sx in [-1.0, 1.0]:
		for sy in [-1.0, 1.0]:
			for sz in [-1.0, 1.0]:
				p.append(centro + base * Vector3(sx * h.x, sy * h.y, sz * h.z))
	var caras := [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]]
	for i in caras.size():
		var q: Array = caras[i]
		var tinte := color
		if i == 3 and color_arriba != null:
			tinte = color_arriba
		cara(m, [p[q[0]], p[q[1]], p[q[2]], p[q[3]]], tinte, centro)


static func prisma(m: Dictionary, base: Vector3, radio: float, alto: float, lados: int, color: Color, radio_arriba: float = -1.0, giro_grados: float = 0.0, tapas: bool = true) -> void:
	# cilindro facetado; con radio_arriba distinto, tronco de cono; con radio_arriba = 0, cono
	var r2 := radio if radio_arriba < 0.0 else radio_arriba
	var abajo: Array = []
	var arriba: Array = []
	for i in lados:
		var ang := TAU * (float(i) + 0.5) / float(lados) + deg_to_rad(giro_grados)
		var d := Vector3(cos(ang), 0.0, sin(ang))
		abajo.append(base + d * radio)
		arriba.append(base + Vector3(0.0, alto, 0.0) + d * r2)
	var eje := base + Vector3(0.0, alto * 0.5, 0.0)
	for i in lados:
		var j := (i + 1) % lados
		if r2 <= 0.0001:
			cara(m, [abajo[i], abajo[j], base + Vector3(0.0, alto, 0.0)], color, eje)
		elif radio <= 0.0001:
			cara(m, [base, arriba[j], arriba[i]], color, eje)
		else:
			cara(m, [abajo[i], abajo[j], arriba[j], arriba[i]], color, eje)
	if tapas:
		if radio > 0.0001:
			cara(m, abajo, color, eje)
		if r2 > 0.0001:
			cara(m, arriba, color, eje)


static func esfera(m: Dictionary, centro: Vector3, radio: float, color: Color, gajos: int = 7, anillos: int = 4, escala: Vector3 = Vector3.ONE) -> void:
	# esfera facetada (o elipsoide con "escala")
	for a in anillos:
		var t0 := PI * float(a) / float(anillos)
		var t1 := PI * float(a + 1) / float(anillos)
		for g in gajos:
			var f0 := TAU * float(g) / float(gajos)
			var f1 := TAU * float(g + 1) / float(gajos)
			var p00 := centro + Vector3(sin(t0) * cos(f0), cos(t0), sin(t0) * sin(f0)) * radio * escala
			var p01 := centro + Vector3(sin(t0) * cos(f1), cos(t0), sin(t0) * sin(f1)) * radio * escala
			var p10 := centro + Vector3(sin(t1) * cos(f0), cos(t1), sin(t1) * sin(f0)) * radio * escala
			var p11 := centro + Vector3(sin(t1) * cos(f1), cos(t1), sin(t1) * sin(f1)) * radio * escala
			if a == 0:
				cara(m, [p00, p10, p11], color, centro)
			elif a == anillos - 1:
				cara(m, [p00, p10, p01], color, centro)
			else:
				cara(m, [p00, p10, p11, p01], color, centro)


static func plano(m: Dictionary, centro: Vector3, tam: Vector2, color: Color, giro_grados: float = 0.0) -> void:
	# rectangulo horizontal que mira hacia arriba (suelos, alfombras, tableros)
	var base := Basis(Vector3.UP, deg_to_rad(giro_grados))
	var h := tam * 0.5
	var p: Array = [
		centro + base * Vector3(-h.x, 0.0, -h.y), centro + base * Vector3(-h.x, 0.0, h.y),
		centro + base * Vector3(h.x, 0.0, h.y), centro + base * Vector3(h.x, 0.0, -h.y)]
	cara(m, p, color, centro - Vector3.UP)


static func cuadro(m: Dictionary, a: Vector3, b: Vector3, c: Vector3, d: Vector3, color: Color, interior: Vector3 = Vector3.INF) -> void:
	# cuadrilatero libre (paredes, tejados, rampas)
	cara(m, [a, b, c, d], color, interior)


static func malla(m: Dictionary) -> ArrayMesh:
	var mesh := ArrayMesh.new()
	if m["v"].is_empty():
		return mesh
	var arrays: Array = []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = PackedVector3Array(m["v"])
	arrays[Mesh.ARRAY_NORMAL] = PackedVector3Array(m["n"])
	arrays[Mesh.ARRAY_COLOR] = PackedColorArray(m["c"])
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return mesh


static func nodo(m: Dictionary, material: String = "facetado", sombra: bool = true) -> MeshInstance3D:
	# MeshInstance3D con el material compartido de la zona: "facetado", "follaje", "agua",
	# o "emisivo" (brillo cian sin sombra; el color de vertice lo tine)
	var mi := MeshInstance3D.new()
	mi.mesh = malla(m)
	if material == "emisivo":
		var promedio := Color(0, 0, 0)
		for c in m["c"]:
			promedio += c
		if not m["c"].is_empty():
			promedio /= float(m["c"].size())
		promedio.a = 1.0
		promedio = promedio.linear_to_srgb()   # StandardMaterial3D espera el color en sRGB
		mi.material_override = Materiales.emisivo(promedio, 1.8)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	else:
		mi.material_override = Materiales.compartido(material)
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if sombra else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return mi


static func triangulos(m: Dictionary) -> int:
	return m["v"].size() / 3
