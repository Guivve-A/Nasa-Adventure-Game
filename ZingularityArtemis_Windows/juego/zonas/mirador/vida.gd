extends Node3D

# Vida del Mirador (v2): luciernagas que se apartan de la protagonista y se reunen si se sienta quieta en la
# banca, viento con rachas que mece la guirnalda y los banderines, el haz del faro (apagado) y la pizarra de
# constelaciones: cinco estrellas de tiza, tres de ellas dibujan la Luna de esta noche.
# Lo monta zonas/mirador/mirador.gd con montar(jugable). Todo es PROVISIONAL, como la zona.

const LUCIERNAGA := preload("res://zonas/mirador/luciernaga.gdshader")
const HAZ := preload("res://zonas/mirador/haz.gdshader")
const BRILLO := preload("res://zonas/mirador/brillo.gdshader")
const Piezas := preload("res://nucleo/piezas.gd")
const Materiales := preload("res://nucleo/materiales.gd")

const HUIR := 1.6                  # m: a esta distancia de la protagonista las luciernagas se apartan
# dorado, crema y verde hierba al sol de la paleta: luz de luciernaga calida, nunca cian (Biblia de arte)
const COLORES := ["e8c64a", "f3d27a", "c9c255"]
const FARO_LINTERNA := Vector3(2.9, 5.45, -2.9)
# el haz giratorio del faro, visto desde la camara alta, lavaba la terraza como neblina: queda apagado
const HAZ_ACTIVO := false
const TAM_LUCIERNAGA := 0.07       # m: medio lado del cuadro con halo (el nucleo brillante mide unos 5 px)

var materiales_viento: Array[ShaderMaterial] = []
var viento := 1.0
var reunir := Vector3.INF          # al sentarse en la banca, las luciernagas cercanas se acercan a este punto
var calma := false                 # sentada y quieta: las luciernagas no huyen de ella
var sustos := 0                    # cuantas veces se apartaron (las pruebas lo leen)

var _racha := 0.0
var _proxima_racha := 5.0
var _t := 0.0
var _mm: MultiMesh
var _l: Array = []                 # cada luciernaga: Dictionary
var _grupos: Array = []            # cada grupo: {"centro": Vector3, "pausa": float}
var _haz: Node3D

# pizarra
var _piz: Dictionary = {}
var _tiza: ShaderMaterial
var _estrella_mat: ShaderMaterial
var _error_mat: ShaderMaterial
var _estrellas: Array = []         # MeshInstance3D de las cinco estrellas
var _elegidas: Array = []          # indices de las estrellas unidas, en orden


func _material_brillo(energia: float) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = BRILLO
	m.set_shader_parameter("inclinacion", float(Materiales.parametros.get("inclinacion", 0.45)))
	m.set_shader_parameter("energia", energia)
	Materiales.creados.append(m)
	return m


func montar(j: Dictionary) -> void:
	_luciernagas(j.get("luciernagas", []))
	if HAZ_ACTIVO:
		_haz_del_faro()
	_piz = j.get("pizarra", {})


# ------------------------------------------------------------------ luciernagas

func _luciernagas(grupos: Array) -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 7311
	for g in grupos:
		var d: Array = g
		var centro := Vector3(float(d[0]), float(d[1]), float(d[2]))
		var radio: float = d[3]
		var alto: float = d[4]
		var n: int = int(d[5])
		_grupos.append({"centro": centro, "pausa": 0.0})
		for i in n:
			var ang := rng.randf() * TAU
			var casa := centro + Vector3(cos(ang) * radio * rng.randf_range(0.2, 1.0), rng.randf_range(0.35, 0.35 + alto), sin(ang) * radio * rng.randf_range(0.2, 1.0))
			_l.append({"casa": casa, "pos": casa, "vel": Vector3.ZERO, "fase": rng.randf(), "radio": radio * 0.45,
				"alto": alto * 0.3, "grupo": _grupos.size() - 1, "susto": 0.0, "color": Color(String(COLORES[i % COLORES.size()]))})
	# v2b: cuadro que mira a la camara con un punto redondo y halo suave (el shader lo dibuja), no una bola facetada
	var quad := QuadMesh.new()
	quad.size = Vector2(2.0, 2.0)
	_mm = MultiMesh.new()
	_mm.transform_format = MultiMesh.TRANSFORM_3D
	_mm.use_colors = true
	_mm.use_custom_data = true
	_mm.mesh = quad
	_mm.instance_count = _l.size()
	var mat := ShaderMaterial.new()
	mat.shader = LUCIERNAGA
	mat.set_shader_parameter("inclinacion", float(Materiales.parametros.get("inclinacion", 0.45)))
	mat.set_shader_parameter("tam", TAM_LUCIERNAGA)
	Materiales.creados.append(mat)
	var mmi := MultiMeshInstance3D.new()
	mmi.name = "Luciernagas"
	mmi.multimesh = _mm
	mmi.material_override = mat
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.custom_aabb = AABB(Vector3(-40, -20, -40), Vector3(80, 40, 80))
	add_child(mmi)
	for i in _l.size():
		var f: Dictionary = _l[i]
		var c: Color = f["color"]
		_mm.set_instance_color(i, c.srgb_to_linear())
		_mm.set_instance_custom_data(i, Color(float(f["fase"]), 0.0, 0.0, 0.0))
		_mm.set_instance_transform(i, Transform3D(Basis(), f["pos"]))


func _mover_luciernagas(delta: float) -> void:
	var jugadora := Vector3.INF
	if Zonas.jugador != null and is_instance_valid(Zonas.jugador):
		jugadora = Zonas.jugador.global_position
	for g in _grupos:
		g["pausa"] = maxf(0.0, float(g["pausa"]) - delta)
	var empuje_viento := Vector3(0.55, 0.0, 0.25) * maxf(0.0, viento - 1.0) * 0.7
	for i in _l.size():
		var f: Dictionary = _l[i]
		var fase: float = float(f["fase"]) * TAU
		var radio: float = f["radio"]
		var casa: Vector3 = f["casa"]
		var objetivo := casa + Vector3(sin(_t * 0.5 + fase) * radio, sin(_t * 0.8 + fase * 2.0) * float(f["alto"]), cos(_t * 0.43 + fase * 1.3) * radio)
		var pos: Vector3 = f["pos"]
		var reunida := reunir != Vector3.INF and Vector2(casa.x - reunir.x, casa.z - reunir.z).length() < 4.0
		if reunida:
			objetivo = reunir + Vector3(sin(_t * 0.7 + fase) * 0.55, 0.55 + 0.3 * sin(_t + fase), cos(_t * 0.6 + fase) * 0.45)
		var acel := (objetivo - pos) * 1.3 + empuje_viento
		var susto: float = maxf(0.0, float(f["susto"]) - delta * 0.8)
		if jugadora != Vector3.INF and not (calma and reunida):
			var d := Vector3(pos.x - jugadora.x, 0.0, pos.z - jugadora.z)
			var dist := d.length()
			if dist < HUIR and absf(pos.y - jugadora.y) < 2.5:
				var fuerza := (HUIR - dist) / HUIR
				acel += (d.normalized() if dist > 0.01 else Vector3.RIGHT) * fuerza * 16.0 + Vector3(0.0, 4.0 * fuerza, 0.0)
				if susto < 0.2:
					var g: Dictionary = _grupos[int(f["grupo"])]
					if float(g["pausa"]) <= 0.0:
						g["pausa"] = 3.5
						sustos += 1
						Audio.sonar("tic", -14.0)
						if not bool(Juego.bandera("mir_luciernagas_susto")):
							Juego.poner_bandera("mir_luciernagas_susto")
				susto = maxf(susto, 0.9 * fuerza + 0.3)
		var vel: Vector3 = f["vel"]
		vel = (vel + acel * delta) * exp(-2.0 * delta)
		pos += vel * delta
		f["vel"] = vel
		f["pos"] = pos
		f["susto"] = susto
		_mm.set_instance_transform(i, Transform3D(Basis(), pos))
		_mm.set_instance_custom_data(i, Color(float(f["fase"]), susto + (0.35 if reunida and calma else 0.0), 0.0, 0.0))


func luciernagas_cerca(punto: Vector3, radio: float = 2.0) -> int:
	var n := 0
	for f in _l:
		var p: Vector3 = f["pos"]
		if Vector2(p.x - punto.x, p.z - punto.z).length() < radio:
			n += 1
	return n


# ------------------------------------------------------------------ viento y faro

func _haz_del_faro() -> void:
	# dos cunas opuestas, largas y tenues, que giran desde la linterna
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for l in [1.0, -1.0]:
		var lado: float = l
		var fin := 9.0 * lado
		var a := Vector3(0.25 * lado, 0.0, 0.0)
		var b := Vector3(fin, -0.6, -0.8)
		var c := Vector3(fin, -0.6, 0.8)
		var cen := Vector3(fin, -0.6, 0.0)
		for tri in [[a, b, cen, Vector2(0, 0), Vector2(1, -1), Vector2(1, 0)], [a, cen, c, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)]]:
			var t: Array = tri
			for k in 3:
				st.set_uv(t[3 + k])
				st.add_vertex(t[k])
	var mi := MeshInstance3D.new()
	mi.name = "HazFaro"
	mi.mesh = st.commit()
	var mat := ShaderMaterial.new()
	mat.shader = HAZ
	mat.set_shader_parameter("inclinacion", float(Materiales.parametros.get("inclinacion", 0.45)))
	Materiales.creados.append(mat)
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_haz = Node3D.new()
	_haz.name = "Haz"
	add_child(_haz)
	_haz.position = FARO_LINTERNA
	_haz.add_child(mi)


func _process(delta: float) -> void:
	_t += delta
	# rachas de viento cada 8 a 14 s: suben rapido y se calman en unos 3 s
	_proxima_racha -= delta
	if _proxima_racha <= 0.0:
		_racha = 1.0
		_proxima_racha = randf_range(8.0, 14.0)
	_racha = maxf(0.0, _racha - delta * 0.33)
	viento = 0.85 + 0.2 * sin(_t * 0.37) + 1.7 * sin(PI * _racha)
	for m in materiales_viento:
		m.set_shader_parameter("viento", viento)
	if _haz != null:
		_haz.rotation.y += delta * TAU / 16.0
	if _mm != null:
		_mover_luciernagas(delta)
	# las estrellas que aun se pueden unir laten despacio
	for i in _estrellas.size():
		if _elegidas.has(i):
			continue
		var e: MeshInstance3D = _estrellas[i]
		e.scale = Vector3.ONE * (1.0 + 0.25 * (0.5 + 0.5 * sin(_t * 3.0 + float(i) * 1.3)))


# ------------------------------------------------------------------ pizarra de constelaciones

func _punto(u: float, v: float, despegue: float = 0.006) -> Vector3:
	var c: Array = _piz.get("centro", [0, 1, 0])
	var de: Array = _piz.get("der", [1, 0, 0])
	var ar: Array = _piz.get("arr", [0, 1, 0])
	var nn: Array = _piz.get("n", [0, 0, 1])
	return Vector3(float(c[0]), float(c[1]), float(c[2])) + Vector3(float(de[0]), float(de[1]), float(de[2])) * u \
		+ Vector3(float(ar[0]), float(ar[1]), float(ar[2])) * v + Vector3(float(nn[0]), float(nn[1]), float(nn[2])) * despegue


func cuantas_estrellas() -> int:
	var e: Array = _piz.get("estrellas", [])
	return e.size()


func _estrella_uv(i: int) -> Vector2:
	var e: Array = _piz.get("estrellas", [[-0.24, 0.10], [0.0, -0.12], [0.24, 0.10]])
	var p: Array = e[i]
	return Vector2(float(p[0]), float(p[1]))


func pizarra_preparar(elegidas: Array) -> void:
	# las cinco estrellas: tiza las libres (laten) y doradas las ya unidas
	if _piz.is_empty():
		return
	_tiza = _material_brillo(0.95)
	_estrella_mat = _material_brillo(2.2)
	_error_mat = _material_brillo(1.6)
	for i in cuantas_estrellas():
		var uv := _estrella_uv(i)
		var m := Piezas.nueva()
		var c := _punto(uv.x, uv.y, 0.0)
		var r := 0.03
		var nn := (_punto(0, 0, 1.0) - _punto(0, 0, 0.0)).normalized()
		var de := (_punto(1, 0, 0) - _punto(0, 0, 0)).normalized()
		var ar := (_punto(0, 1, 0) - _punto(0, 0, 0)).normalized()
		Piezas.cara(m, [c - de * r, c - ar * r, c + de * r, c + ar * r], Color("f8c991"), c - nn)
		var mi := MeshInstance3D.new()
		mi.name = "Estrella%d" % i
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		add_child(mi)
		# el centro de la malla es "c": se escala alrededor de el
		mi.position = c
		mi.mesh = _recentrar(m, c)
		_estrellas.append(mi)
	pizarra_dibujar(elegidas, false)


func _recentrar(m: Dictionary, c: Vector3) -> ArrayMesh:
	var v: Array = []
	for p in m["v"]:
		v.append(p - c)
	return Piezas.malla({"v": v, "n": m["n"], "c": m["c"]})


func _arco(u0: float, u1: float, centro_v: float, radio: float, pasos: int = 10) -> Array:
	# arco de circunferencia de centro (0, centro_v) entre las abscisas u0 y u1, por debajo del centro
	var puntos: Array = []
	for k in pasos + 1:
		var u := lerpf(u0, u1, float(k) / float(pasos))
		var v := centro_v - sqrt(maxf(0.0, radio * radio - u * u))
		puntos.append(Vector2(u, v))
	return puntos


func _linea(puntos: Array, grosor: float, mat: ShaderMaterial, nombre: String, hasta: float = 1.0) -> MeshInstance3D:
	var m := Piezas.nueva()
	var nn := (_punto(0, 0, 1.0) - _punto(0, 0, 0.0)).normalized()
	var total := int(ceil((puntos.size() - 1) * clampf(hasta, 0.0, 1.0)))
	for k in total:
		var a2: Vector2 = puntos[k]
		var b2: Vector2 = puntos[k + 1]
		var a := _punto(a2.x, a2.y)
		var b := _punto(b2.x, b2.y)
		var lado := nn.cross(b - a).normalized() * grosor
		Piezas.cara(m, [a - lado, b - lado, b + lado, a + lado], Color("f8c991"), (a + b) * 0.5 - nn)
	var mi := get_node_or_null(nombre) as MeshInstance3D
	if mi == null:
		mi = MeshInstance3D.new()
		mi.name = nombre
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.material_override = mat
		add_child(mi)
	mi.mesh = Piezas.malla(m)
	mi.visible = true
	return mi


func _tramo(nombre: String, puntos: Array, animado: bool) -> void:
	if animado:
		_linea(puntos, 0.008, _tiza, nombre, 0.0)
		create_tween().tween_method(func(p: float) -> void: _linea(puntos, 0.008, _tiza, nombre, p), 0.0, 1.0, 0.6)
	else:
		_linea(puntos, 0.008, _tiza, nombre)


func pizarra_dibujar(elegidas: Array, animado: bool = true) -> void:
	# tiza segun las estrellas unidas: de una punta al borde iluminado (abajo) y de ahi a la otra punta;
	# completa, se cierra con el terminador y queda la creciente como una sonrisa
	if _piz.is_empty() or _tiza == null:
		return
	var nuevas := elegidas.size() > _elegidas.size()
	_elegidas = elegidas.duplicate()
	for i in _estrellas.size():
		var mi: MeshInstance3D = _estrellas[i]
		mi.material_override = _estrella_mat if _elegidas.has(i) else _tiza
		mi.scale = Vector3.ONE
	# circunferencia por las tres estrellas de la creciente (simetrica): centro (0, cv) y radio r
	var s0 := _estrella_uv(0)
	var s1 := _estrella_uv(1)
	var cv := (s0.x * s0.x + s0.y * s0.y - s1.y * s1.y) / (2.0 * (s0.y - s1.y))
	var r := absf(cv - s1.y)
	for nombre in ["Tiza1", "Tiza2", "Tiza3"]:
		var t := get_node_or_null(nombre)
		var hace_falta := 2 if nombre == "Tiza1" else 3
		if t != null and _elegidas.size() < hace_falta:
			t.visible = false
	if _elegidas.size() >= 2:
		var u0 := _estrella_uv(int(_elegidas[0])).x
		_tramo("Tiza1", _arco(u0, 0.0, cv, r), animado and nuevas and _elegidas.size() == 2)
	if _elegidas.size() >= 3:
		var u2 := _estrella_uv(int(_elegidas[2])).x
		_tramo("Tiza2", _arco(0.0, u2, cv, r), animado and nuevas)
		# terminador: arco mas abierto que pasa a 0,08 m sobre el borde iluminado
		var abajo := s1.y + 0.08
		var cv2 := (s0.x * s0.x + s0.y * s0.y - abajo * abajo) / (2.0 * (s0.y - abajo))
		_tramo("Tiza3", _arco(s0.x, -s0.x, cv2, absf(cv2 - abajo), 14), animado and nuevas)


func pizarra_error(estrella: int) -> void:
	# la estrella equivocada se enciende coral un instante y la tiza se borra
	if estrella >= 0 and estrella < _estrellas.size():
		var mi: MeshInstance3D = _estrellas[estrella]
		_error_mat.set_shader_parameter("energia", 1.6)
		mi.material_override = _error_mat
		mi.scale = Vector3.ONE * 1.6
	await get_tree().create_timer(0.45).timeout
	pizarra_dibujar([], false)
