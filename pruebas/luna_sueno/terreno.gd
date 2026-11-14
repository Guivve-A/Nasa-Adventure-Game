extends RefCounted

# Terreno lunar por script: heightmap de 512 x 512 celdas sobre 450 x 450 m (0,88 m por celda), centrado en
# el sitio del Apolo 11 (origen). Relieve suave de ruido mas crateres de varios tamanos.
# Se trocea en 8 x 8 bloques de 64 celdas (56,25 m). Cada bloque tiene 4 niveles de detalle (1, 2, 4 y 8
# celdas por cuadro) que se cambian por distancia con visibility_range. Un faldon vertical en el borde de
# cada bloque tapa las grietas entre bloques de distinto nivel.
# Ejes: +X este, -Z norte, +Y arriba.

const CELDAS := 512
const LADO := 450.0
const BLOQUES := 8
const PASOS := [1, 2, 4, 8]                   # celdas por cuadro en cada nivel de detalle
const RANGOS := [0.0, 70.0, 140.0, 240.0]     # distancia (m) a la que empieza cada nivel
# Sin histeresis: con margen y sin fundido, Godot arranca cada nivel oculto y deja sin dibujar los bloques
# cuyo centro cae en la banda de +-margen (se vio en la primera captura panoramica: faltaban bloques enteros).
const MARGEN := 0.0
const FALDON := 1.5

var n := CELDAS + 1
var celda := LADO / CELDAS
var alturas := PackedFloat32Array()
var colores := PackedColorArray()
var normales := PackedVector3Array()
var crateres: Array = []  # [x, z, radio, profundidad, fresco]
var rng := RandomNumberGenerator.new()
var _indices_cache := {}
var triangulos_detalle_max := 0


func generar(semilla: int) -> void:
	rng.seed = semilla
	alturas.resize(n * n)
	var tono := PackedFloat32Array()
	tono.resize(n * n)
	var relieve := FastNoiseLite.new()
	relieve.seed = semilla
	relieve.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	relieve.frequency = 1.0 / 150.0
	relieve.fractal_octaves = 3
	var fino := FastNoiseLite.new()
	fino.seed = semilla + 7
	fino.noise_type = FastNoiseLite.TYPE_SIMPLEX
	fino.frequency = 1.0 / 9.0
	fino.fractal_type = FastNoiseLite.FRACTAL_NONE
	var manchas := FastNoiseLite.new()
	manchas.seed = semilla + 13
	manchas.frequency = 1.0 / 60.0
	manchas.fractal_octaves = 2
	for j in n:
		var z := _coord(j)
		for i in n:
			var x := _coord(i)
			var k := j * n + i
			alturas[k] = relieve.get_noise_2d(x, z) * 2.6 + fino.get_noise_2d(x, z) * 0.14
			tono[k] = manchas.get_noise_2d(x, z) * 0.05
	_poner_crateres(tono)
	_aplanar_sitio()
	# color de vertice: gris lunar apenas calido; los crateres frescos dejan halos claros (regolito joven)
	colores.resize(n * n)
	for k in n * n:
		var g := clampf(0.47 + tono[k], 0.30, 0.78)
		colores[k] = Color(g, g * 0.975, g * 0.94).srgb_to_linear()  # el shader usa COLOR en lineal
	normales.resize(n * n)
	for j in n:
		for i in n:
			var hl := alturas[j * n + maxi(i - 1, 0)]
			var hr := alturas[j * n + mini(i + 1, n - 1)]
			var hu := alturas[maxi(j - 1, 0) * n + i]
			var hd := alturas[mini(j + 1, n - 1) * n + i]
			normales[j * n + i] = Vector3(hl - hr, 2.0 * celda, hu - hd).normalized()


func _coord(i: int) -> float:
	return -LADO * 0.5 + i * celda


func _poner_crateres(tono: PackedFloat32Array) -> void:
	# analogo de Little West: unos 33 m de diametro, unos 60 m al este del sitio
	_crater(62.0, -4.0, 16.5, 4.2, true, tono)
	var listas := [
		# cantidad, radio min, radio max, profundidad/diametro, distancia libre al sitio, fraccion fresca
		[6, 18.0, 42.0, 0.10, 45.0, 0.0],
		[60, 4.0, 12.0, 0.13, 14.0, 0.25],
		[650, 0.6, 3.5, 0.17, 7.0, 0.3],
	]
	for l in listas:
		var colocados := 0
		var intentos := 0
		while colocados < int(l[0]) and intentos < 20000:
			intentos += 1
			# reparto de tamanos en ley de potencia: muchos chicos, pocos grandes
			var r: float = lerpf(l[1], l[2], pow(rng.randf(), 2.2))
			var x := rng.randf_range(-LADO * 0.5, LADO * 0.5)
			var z := rng.randf_range(-LADO * 0.5, LADO * 0.5)
			if Vector2(x, z).length() < r + float(l[4]):
				continue
			_crater(x, z, r, r * 2.0 * float(l[3]) * rng.randf_range(0.6, 1.1), rng.randf() < float(l[5]), tono)
			colocados += 1


func _crater(cx: float, cz: float, r: float, prof: float, fresco: bool, tono: PackedFloat32Array) -> void:
	crateres.append([cx, cz, r, prof, fresco])
	var borde := prof * 0.22
	var alcance := r * (2.6 if fresco else 2.0)
	var i0 := maxi(0, int((cx - alcance + LADO * 0.5) / celda))
	var i1 := mini(n - 1, int((cx + alcance + LADO * 0.5) / celda) + 1)
	var j0 := maxi(0, int((cz - alcance + LADO * 0.5) / celda))
	var j1 := mini(n - 1, int((cz + alcance + LADO * 0.5) / celda) + 1)
	for j in range(j0, j1 + 1):
		var dz := _coord(j) - cz
		for i in range(i0, i1 + 1):
			var dx := _coord(i) - cx
			var d := sqrt(dx * dx + dz * dz) / r
			var k := j * n + i
			if d < 2.0:
				var h: float
				if d < 1.0:
					h = prof * (d * d - 1.0) + borde * d * d * d * d
				else:
					h = borde * exp(-(d - 1.0) * 4.0) * (1.0 - smoothstep(1.6, 2.0, d))
				alturas[k] += h
				if d < 0.9:
					tono[k] -= 0.035
			if fresco and d > 0.75 and d < 2.6:
				tono[k] += 0.16 * exp(-(d - 0.95) * 2.2) * (1.0 - smoothstep(2.0, 2.6, d))


func _aplanar_sitio() -> void:
	# el sitio de alunizaje es llano: se suaviza un circulo de 7 a 16 m y la altura del origen pasa a 0
	var h0 := alturas[(n / 2) * n + n / 2]
	for k in n * n:
		var p := Vector2(_coord(k % n), _coord(k / n))
		var w := smoothstep(7.0, 16.0, p.length())
		alturas[k] = lerpf(h0, alturas[k], w) - h0


func altura(x: float, z: float) -> float:
	# altura bilineal en un punto del mundo
	var fx := clampf((x + LADO * 0.5) / celda, 0.0, CELDAS - 0.001)
	var fz := clampf((z + LADO * 0.5) / celda, 0.0, CELDAS - 0.001)
	var i := int(fx)
	var j := int(fz)
	var tx := fx - i
	var tz := fz - j
	var a := lerpf(alturas[j * n + i], alturas[j * n + i + 1], tx)
	var b := lerpf(alturas[(j + 1) * n + i], alturas[(j + 1) * n + i + 1], tx)
	return lerpf(a, b, tz)


func montar(padre: Node3D, material: Material, sin_lod: bool) -> int:
	# crea los MeshInstance3D; devuelve cuantos nodos de malla hay
	var nodos := 0
	var celdas_bloque := CELDAS / BLOQUES
	for bz in BLOQUES:
		for bx in BLOQUES:
			var niveles := [0] if sin_lod else range(PASOS.size())
			for nivel in niveles:
				var mi := MeshInstance3D.new()
				mi.name = "Bloque_%d_%d_L%d" % [bx, bz, nivel]
				mi.mesh = _malla_bloque(bx * celdas_bloque, bz * celdas_bloque, celdas_bloque, PASOS[nivel])
				mi.material_override = material
				mi.extra_cull_margin = 3.0  # la cizalla 2.5D del shader mueve el terreno hasta 2 m
				if not sin_lod:
					mi.visibility_range_begin = RANGOS[nivel]
					mi.visibility_range_begin_margin = MARGEN if nivel > 0 else 0.0
					if nivel < PASOS.size() - 1:
						mi.visibility_range_end = RANGOS[nivel + 1]
						mi.visibility_range_end_margin = MARGEN
				padre.add_child(mi)
				nodos += 1
				if nivel == 0:
					triangulos_detalle_max += _indices(celdas_bloque / PASOS[0]).size() / 3
	return nodos


func _malla_bloque(i_base: int, j_base: int, celdas_bloque: int, paso: int) -> ArrayMesh:
	var m := celdas_bloque / paso
	var lado := m + 1
	var total := lado * lado + 4 * lado
	var v := PackedVector3Array()
	var nr := PackedVector3Array()
	var c := PackedColorArray()
	v.resize(total)
	nr.resize(total)
	c.resize(total)
	var q := 0
	for jj in lado:
		var j := j_base + jj * paso
		for ii in lado:
			var i := i_base + ii * paso
			var k := j * n + i
			v[q] = Vector3(_coord(i), alturas[k], _coord(j))
			nr[q] = normales[k]
			c[q] = colores[k]
			q += 1
	# faldones: copia de los 4 bordes, bajada FALDON metros
	for borde in _bordes(lado):
		for g in borde:
			v[q] = v[g] - Vector3(0.0, FALDON, 0.0)
			nr[q] = nr[g]
			c[q] = c[g]
			q += 1
	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = v
	arrays[Mesh.ARRAY_NORMAL] = nr
	arrays[Mesh.ARRAY_COLOR] = c
	arrays[Mesh.ARRAY_INDEX] = _indices(m)
	var malla := ArrayMesh.new()
	malla.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return malla


func _bordes(lado: int) -> Array:
	var norte := []
	var sur := []
	var oeste := []
	var este := []
	for t in lado:
		norte.append(t)
		sur.append((lado - 1) * lado + t)
		oeste.append(t * lado)
		este.append(t * lado + lado - 1)
	return [norte, sur, oeste, este]


func _indices(m: int) -> PackedInt32Array:
	# el patron de indices es igual en todos los bloques del mismo nivel: se calcula una vez
	if _indices_cache.has(m):
		return _indices_cache[m]
	var lado := m + 1
	var idx := PackedInt32Array()
	for jj in m:
		for ii in m:
			var a := jj * lado + ii
			var b := a + 1
			var d := a + lado
			var e := d + 1
			# diagonal alterna: facetas en rombo, mas organicas que todas iguales
			if (ii + jj) % 2 == 0:
				idx.append_array([a, b, e, a, e, d])
			else:
				idx.append_array([a, b, d, b, e, d])
	# faldones en las dos caras (asi no importa el sentido del borde)
	var base := lado * lado
	for borde in _bordes(lado):
		for t in lado - 1:
			var g0: int = borde[t]
			var g1: int = borde[t + 1]
			var s0 := base + t
			var s1 := base + t + 1
			idx.append_array([g0, g1, s1, g0, s1, s0, g0, s1, g1, g0, s0, s1])
		base += lado
	_indices_cache[m] = idx
	return idx
