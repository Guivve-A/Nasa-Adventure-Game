extends RefCounted

# LUN-01: terreno lunar de regolito con crateres, generado por script (PROVISIONAL, sin concepto validado).
# Mapa de alturas de 160 x 128 celdas de 0,75 m (120 x 96 m). Parte de la prueba tecnica pruebas/luna_sueno
# (relieve de ruido mas crateres con borde levantado), a la escala de una zona jugable y sin niveles de detalle:
# la camara de juego ve unos 14 m de ancho. La malla va indexada y el shader de regolito saca la normal plana
# de cada cara con derivadas. La colision es la misma malla (triangulos).
# v2: color por vertice con cinco capas (matiz calido o azulado, mares oscuros, fondos violetas, bordes y rayos
# de eyecta claros, brillo); el suelo deja de ser un azul uniforme.
# Ejes: +X derecha, -Z arriba en pantalla, +Y arriba.

const CELDA := 0.75
const BLOQUE := 32                # celdas por lado de cada trozo de malla (24 m)

var x0 := -24.0
var z0 := -72.0
var nx := 161                     # vertices en X
var nz := 129                     # vertices en Z
var alturas := PackedFloat32Array()
var tono := PackedFloat32Array()          # brillo: + claro, - oscuro
var matiz := PackedFloat32Array()         # -1 gris azulado, +1 gris calido
var hondo := PackedFloat32Array()         # 0..1 fondo de crater o zanja: violeta
var claro := PackedFloat32Array()         # 0..1 borde de crater, eyecta y rayos: gris crema
var mar := PackedFloat32Array()           # 0..1 manchas de mar, mas oscuras
var crateres: Array = []          # [x, z, radio, profundidad, fresco]
var rng := RandomNumberGenerator.new()
var triangulos := 0


func generar(semilla: int, d: Dictionary) -> void:
	# d: "lomas" [[x, z, alto, sigma]], "zanjas" [[x0, z0, x1, z1, medio_ancho, prof]],
	#    "crateres" [[x, z, radio, prof, fresco]], "aleatorios" n, "libres" [[x, z, radio]] (sin crateres al azar),
	#    "llanos" [[x, z, radio_llano, radio_fin]], "cero" Vector2 (punto de altura 0)
	rng.seed = semilla
	alturas.resize(nx * nz)
	tono.resize(nx * nz)
	matiz.resize(nx * nz)
	hondo.resize(nx * nz)
	claro.resize(nx * nz)
	mar.resize(nx * nz)
	var tinte := FastNoiseLite.new()
	tinte.seed = semilla + 21
	tinte.frequency = 1.0 / 22.0
	tinte.fractal_octaves = 2
	var mares := FastNoiseLite.new()
	mares.seed = semilla + 31
	mares.frequency = 1.0 / 64.0
	mares.fractal_octaves = 2
	var relieve := FastNoiseLite.new()
	relieve.seed = semilla
	relieve.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	relieve.frequency = 1.0 / 46.0
	relieve.fractal_octaves = 3
	var fino := FastNoiseLite.new()
	fino.seed = semilla + 7
	fino.noise_type = FastNoiseLite.TYPE_SIMPLEX
	fino.frequency = 1.0 / 3.6
	fino.fractal_type = FastNoiseLite.FRACTAL_NONE
	var manchas := FastNoiseLite.new()
	manchas.seed = semilla + 13
	manchas.frequency = 1.0 / 28.0
	manchas.fractal_octaves = 2
	var lomas: Array = d.get("lomas", [])
	var zanjas: Array = d.get("zanjas", [])
	for j in nz:
		var z := z0 + j * CELDA
		for i in nx:
			var x := x0 + i * CELDA
			var k := j * nx + i
			var h := relieve.get_noise_2d(x, z) * 1.0 + fino.get_noise_2d(x, z) * 0.13
			var t := manchas.get_noise_2d(x, z) * 0.10
			var ho := 0.0
			var cl := 0.0
			var ma := smoothstep(-0.05, 0.28, mares.get_noise_2d(x, z))
			for l in lomas:
				var dl := Vector2(x - float(l[0]), z - float(l[1])).length() / float(l[3])
				h += float(l[2]) * exp(-dl * dl)
				t += 0.04 * exp(-dl * dl)
				cl += 0.08 * exp(-dl * dl)
				ma *= 1.0 - exp(-dl * dl)
			for s in zanjas:
				var a := Vector2(float(s[0]), float(s[1]))
				var b := Vector2(float(s[2]), float(s[3]))
				var p := Vector2(x, z)
				var u := clampf((p - a).dot(b - a) / (b - a).length_squared(), 0.0, 1.0)
				var dz := (p - a.lerp(b, u)).length() / float(s[4])
				if dz < 1.6:
					# fondo plano, paredes en cuesta y un labio suave
					h -= float(s[5]) * (1.0 - smoothstep(0.35, 1.0, dz))
					h += float(s[5]) * 0.12 * exp(-(dz - 1.15) * (dz - 1.15) * 9.0)
					t -= 0.11 * (1.0 - smoothstep(0.3, 1.0, dz))
					ho += 0.75 * (1.0 - smoothstep(0.3, 1.0, dz))
					cl += 0.45 * exp(-(dz - 1.15) * (dz - 1.15) * 9.0)
			alturas[k] = h
			tono[k] = t - 0.05 * ma
			matiz[k] = tinte.get_noise_2d(x, z)
			hondo[k] = ho
			claro[k] = cl
			mar[k] = ma
	for c in d.get("crateres", []):
		_crater(float(c[0]), float(c[1]), float(c[2]), float(c[3]), bool(c[4]))
	var libres: Array = d.get("libres", [])
	var colocados := 0
	var intentos := 0
	var total: int = d.get("aleatorios", 0)
	while colocados < total and intentos < 6000:
		intentos += 1
		var r: float = lerpf(1.2, 4.2, pow(rng.randf(), 2.4))
		var x := rng.randf_range(x0 + 3.0, x0 + (nx - 1) * CELDA - 3.0)
		var z := rng.randf_range(z0 + 3.0, z0 + (nz - 1) * CELDA - 3.0)
		var choca := false
		for l in libres:
			if Vector2(x - float(l[0]), z - float(l[1])).length() < r * 1.7 + float(l[2]):
				choca = true
				break
		if choca:
			continue
		# profundidad / diametro de 0,07 a 0,12: paredes de 35 grados como mucho, se sale caminando
		_crater(x, z, r, r * 2.0 * 0.12 * rng.randf_range(0.6, 1.0), rng.randf() < 0.3)
		colocados += 1
	for l in d.get("llanos", []):
		_aplanar(float(l[0]), float(l[1]), float(l[2]), float(l[3]))
	var cero: Vector2 = d.get("cero", Vector2.ZERO)
	var h0 := altura(cero.x, cero.y)
	for k in nx * nz:
		alturas[k] -= h0


func _crater(cx: float, cz: float, r: float, prof: float, fresco: bool) -> void:
	crateres.append([cx, cz, r, prof, fresco])
	# v2f: labio mas alto y mas claro, fondo menos violeta: el crater se lee por su borde, como en el arte de carga
	var borde := prof * 0.34
	var alcance := r * (2.6 if fresco else 2.0)
	# rayos de eyecta de los crateres frescos: 5 a 9 lenguas claras con fase al azar
	var n_rayos := rng.randi_range(5, 9)
	var fase := rng.randf() * TAU
	var i0 := maxi(0, int((cx - alcance - x0) / CELDA))
	var i1 := mini(nx - 1, int((cx + alcance - x0) / CELDA) + 1)
	var j0 := maxi(0, int((cz - alcance - z0) / CELDA))
	var j1 := mini(nz - 1, int((cz + alcance - z0) / CELDA) + 1)
	for j in range(j0, j1 + 1):
		var dz := z0 + j * CELDA - cz
		for i in range(i0, i1 + 1):
			var dx := x0 + i * CELDA - cx
			var q := sqrt(dx * dx + dz * dz) / r
			var k := j * nx + i
			if q < 2.0:
				var h: float
				if q < 1.0:
					h = prof * (q * q - 1.0) + borde * q * q * q * q
				else:
					h = borde * exp(-(q - 1.0) * 4.0) * (1.0 - smoothstep(1.6, 2.0, q))
				alturas[k] += h
				if q < 0.9:
					tono[k] -= 0.06
					hondo[k] += 0.38 * (1.0 - smoothstep(0.55, 0.9, q)) + 0.12
				# labio claro del borde, en todos los crateres
				claro[k] += (0.8 if fresco else 0.55) * exp(-pow((q - 1.02) / 0.17, 2.0))
			if fresco and q > 0.75 and q < 2.6:
				tono[k] += 0.13 * exp(-(q - 0.95) * 2.2) * (1.0 - smoothstep(2.0, 2.6, q))
				var ang := atan2(dz, dx)
				var rayo := pow(0.5 + 0.5 * cos(ang * float(n_rayos) + fase + 0.6 * sin(ang * 3.0)), 5.0)
				var caida := exp(-(q - 1.0) * 1.3) * (1.0 - smoothstep(2.0, 2.6, q))
				if q > 1.0:
					claro[k] += (0.18 + 0.5 * rayo) * caida
					mar[k] *= 1.0 - 0.8 * caida


func _aplanar(cx: float, cz: float, r_llano: float, r_fin: float) -> void:
	var h0 := altura(cx, cz)
	var i0 := maxi(0, int((cx - r_fin - x0) / CELDA))
	var i1 := mini(nx - 1, int((cx + r_fin - x0) / CELDA) + 1)
	var j0 := maxi(0, int((cz - r_fin - z0) / CELDA))
	var j1 := mini(nz - 1, int((cz + r_fin - z0) / CELDA) + 1)
	for j in range(j0, j1 + 1):
		for i in range(i0, i1 + 1):
			var q := Vector2(x0 + i * CELDA - cx, z0 + j * CELDA - cz).length()
			var k := j * nx + i
			alturas[k] = lerpf(h0, alturas[k], smoothstep(r_llano, r_fin, q))


func altura(x: float, z: float) -> float:
	# altura bilineal en un punto del mundo
	var fx := clampf((x - x0) / CELDA, 0.0, nx - 1.001)
	var fz := clampf((z - z0) / CELDA, 0.0, nz - 1.001)
	var i := int(fx)
	var j := int(fz)
	var tx := fx - i
	var tz := fz - j
	var a := lerpf(alturas[j * nx + i], alturas[j * nx + i + 1], tx)
	var b := lerpf(alturas[(j + 1) * nx + i], alturas[(j + 1) * nx + i + 1], tx)
	return lerpf(a, b, tz)


func normal(x: float, z: float) -> Vector3:
	var e := CELDA * 0.6
	return Vector3(altura(x - e, z) - altura(x + e, z), 2.0 * e, altura(x, z - e) - altura(x, z + e)).normalized()


func en_suelo(x: float, z: float, alza: float = 0.0) -> Vector3:
	return Vector3(x, altura(x, z) + alza, z)


func rect() -> Rect2:
	return Rect2(x0, z0, (nx - 1) * CELDA, (nz - 1) * CELDA)


func montar(padre: Node3D, material: Material) -> int:
	# trozos de malla indexada de BLOQUE x BLOQUE celdas y un solo cuerpo de colision. Devuelve los trozos.
	# v2: el regolito ya no es un azul uniforme. Solo mezclas de la paleta maestra:
	# gris calido (piedra + piedra clara + crema), gris azulado (piedra clara + petroleo), violeta en los
	# fondos (piedra + petroleo), mares mas oscuros y bordes, eyecta y rayos en gris crema.
	# v2e: medido contra el arte de carga pintado (carga_luna.jpg del 2026-11-15): llano al sol crema rosado
	# (#C6A8A4), lejos lavanda (#AEA4B7), fondos y sombras azul violeta (#5E5E89). El violeta lo pone la luz de
	# relleno azul sobre estos grises; el albedo sigue siendo mezcla de la paleta maestra
	var calido := Color("b8bbc6").lerp(Color("f8c991"), 0.30).lerp(Color("d09880"), 0.18)
	var frio := Color("b8bbc6").lerp(Color("998385"), 0.25)
	var violeta := Color("998385").lerp(Color("516b7c"), 0.40)
	var mar_c := Color("b8bbc6").lerp(Color("516b7c"), 0.22).lerp(Color("998385"), 0.22)
	var claro_c := Color("b8bbc6").lerp(Color("f8c991"), 0.45)
	var colores := PackedColorArray()
	colores.resize(nx * nz)
	var normales := PackedVector3Array()
	normales.resize(nx * nz)
	for j in nz:
		for i in nx:
			var k := j * nx + i
			var t := tono[k]
			var c := frio.lerp(calido, clampf(matiz[k] * 2.6 + 0.45, 0.0, 1.0))
			c = c.lerp(mar_c, clampf(mar[k], 0.0, 1.0) * 0.75)
			c = c.lerp(violeta, clampf(hondo[k], 0.0, 0.85))
			c = c.lerp(claro_c, clampf(claro[k], 0.0, 0.85))
			c *= clampf(0.9 + t * 1.6, 0.6, 1.1)
			c.a = 1.0
			colores[k] = Color(clampf(c.r, 0.0, 1.0), clampf(c.g, 0.0, 1.0), clampf(c.b, 0.0, 1.0)).srgb_to_linear()
			var hl := alturas[j * nx + maxi(i - 1, 0)]
			var hr := alturas[j * nx + mini(i + 1, nx - 1)]
			var hu := alturas[maxi(j - 1, 0) * nx + i]
			var hd := alturas[mini(j + 1, nz - 1) * nx + i]
			normales[k] = Vector3(hl - hr, 2.0 * CELDA, hu - hd).normalized()
	var trozos := 0
	var j_base := 0
	while j_base < nz - 1:
		var mj := mini(BLOQUE, nz - 1 - j_base)
		var i_base := 0
		while i_base < nx - 1:
			var mi_celdas := mini(BLOQUE, nx - 1 - i_base)
			var nodo := MeshInstance3D.new()
			nodo.name = "LUN-01_%d_%d" % [i_base / BLOQUE, j_base / BLOQUE]
			nodo.mesh = _malla(i_base, j_base, mi_celdas, mj, colores, normales)
			nodo.material_override = material
			nodo.extra_cull_margin = 2.5       # la inclinacion 2.5D del shader desplaza el terreno
			nodo.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
			padre.add_child(nodo)
			trozos += 1
			i_base += BLOQUE
		j_base += BLOQUE
	# colision: los mismos triangulos, con la misma diagonal alterna
	var caras := PackedVector3Array()
	caras.resize((nx - 1) * (nz - 1) * 6)
	var q := 0
	for j in nz - 1:
		for i in nx - 1:
			var a := _v(i, j)
			var b := _v(i + 1, j)
			var c := _v(i, j + 1)
			var e := _v(i + 1, j + 1)
			if (i + j) % 2 == 0:
				caras[q] = a; caras[q + 1] = b; caras[q + 2] = e
				caras[q + 3] = a; caras[q + 4] = e; caras[q + 5] = c
			else:
				caras[q] = a; caras[q + 1] = b; caras[q + 2] = c
				caras[q + 3] = b; caras[q + 4] = e; caras[q + 5] = c
			q += 6
	var forma := ConcavePolygonShape3D.new()
	forma.backface_collision = true
	forma.set_faces(caras)
	var cuerpo := StaticBody3D.new()
	cuerpo.name = "LUN-01_colision"
	cuerpo.collision_layer = 1
	cuerpo.collision_mask = 0
	var cs := CollisionShape3D.new()
	cs.shape = forma
	cuerpo.add_child(cs)
	padre.add_child(cuerpo)
	return trozos


func _v(i: int, j: int) -> Vector3:
	return Vector3(x0 + i * CELDA, alturas[j * nx + i], z0 + j * CELDA)


func _malla(i_base: int, j_base: int, mi_celdas: int, mj: int, colores: PackedColorArray, normales: PackedVector3Array) -> ArrayMesh:
	var lado := mi_celdas + 1
	var v := PackedVector3Array()
	var nr := PackedVector3Array()
	var c := PackedColorArray()
	v.resize(lado * (mj + 1))
	nr.resize(v.size())
	c.resize(v.size())
	var q := 0
	for jj in mj + 1:
		for ii in lado:
			var k := (j_base + jj) * nx + i_base + ii
			v[q] = _v(i_base + ii, j_base + jj)
			nr[q] = normales[k]
			c[q] = colores[k]
			q += 1
	var idx := PackedInt32Array()
	idx.resize(mi_celdas * mj * 6)
	q = 0
	for jj in mj:
		for ii in mi_celdas:
			var a := jj * lado + ii
			var b := a + 1
			var d := a + lado
			var e := d + 1
			# diagonal alterna (en coordenadas globales, igual que la colision): facetas en rombo
			if (i_base + ii + j_base + jj) % 2 == 0:
				idx[q] = a; idx[q + 1] = b; idx[q + 2] = e
				idx[q + 3] = a; idx[q + 4] = e; idx[q + 5] = d
			else:
				idx[q] = a; idx[q + 1] = b; idx[q + 2] = d
				idx[q + 3] = b; idx[q + 4] = e; idx[q + 5] = d
			q += 6
	triangulos += mi_celdas * mj * 2
	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = v
	arrays[Mesh.ARRAY_NORMAL] = nr
	arrays[Mesh.ARRAY_COLOR] = c
	arrays[Mesh.ARRAY_INDEX] = idx
	var malla := ArrayMesh.new()
	malla.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return malla
