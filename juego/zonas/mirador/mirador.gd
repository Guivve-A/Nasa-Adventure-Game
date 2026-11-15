extends "res://nucleo/zona.gd"

# El Mirador del Faro: terraza de piedra con balaustrada curva, el faro, la mesa del club de astronomia,
# el telescopio, el atril y los binoculares. PROVISIONAL: el concepto (Lote_03/L03_mirador_noche_vista_juego.png)
# y la hoja HR_MIR_v1 no tienen todavia el veredicto de Guillermo.
#
# La escena la escribe herramientas/mallas/mirador_escena.py:
#   - layout.json: recursos (formato de nucleo/constructor.gd) y "jugable" (colisiones, puntos, guirnaldas y luces)
#   - modelos/mirador/: MIR-01 a MIR-10, TAL-10, TAL-11, TAL-18, ARQ-09, ARQ-14, URB-07, VEG-08, VEG-15 y TER-15
# Momento: noche con Luna (luz "noche", provisional), guirnalda y faroles calidos sin sombra.
# Lo calido (bombillas, ventanas) se dibuja con brillo.gdshader, que acompana la inclinacion 2.5D.

const LAYOUT := "res://zonas/mirador/layout.json"
const MODELOS := "res://modelos"
const BRILLO := preload("res://zonas/mirador/brillo.gdshader")
const VAIVEN := preload("res://zonas/mirador/vaiven.gdshader")
const VAIVEN_BRILLO := preload("res://zonas/mirador/vaiven_brillo.gdshader")
const CHARCO := preload("res://zonas/mirador/charco.gdshader")
const Vida := preload("res://zonas/mirador/vida.gd")
const CALIDO := Color("ffc98a")
const CABLE := Color("583f22")
const CUERDA := Color("d6a978")    # tierra2 aclarada hacia crema (la cuerda de MIR-07)
const SOMBRA_APROBADA := 0.7       # valor por defecto de shaders/comun.gdshaderinc (D-015)
const MSG_PORTON := "El portón del cerro sigue cerrado. Primero la Luna y las diapositivas del atril."
# v2 (color): noche pintada. Luna fria de borde desde el oeste, sombras azul profundo y violeta, y charcos
# dorados bajo la guirnalda y las lamparas (caida rapida). La luz "noche" del nucleo sigue PROVISIONAL:
# estos cambios son solo de la zona.
# v2b (critica): noche mas honda (ambiente 2c3163 a 0,62 y contraste 1,2) para que los charcos calidos contrasten.
const NOCHE := {
	"direccion": Vector3(-0.60, -0.66, 0.34), "sombra_distancia": 24.0,
	"sol": "b4c6f0", "energia": 0.36,
	"ambiente": "2c3163", "ambiente_energia": 0.62, "fondo": "10122a",
	"contraste": 1.2, "saturacion": 1.0, "exposicion": 0.95,
}
const CAIDA_FAROL := 2.4           # omni_attenuation de los faroles: charco con borde, no luz de dia
const ENERGIA_FAROL := 1.0          # los charcos dorados mandan sobre la noche azul
const DORADO := Color("f4a159")     # bombilla del farol que se enciende a mano (sol de la paleta)
const REFLEJO := Color("b8bbc6")    # reflejo frio de la Luna en el rio (piedra_clara de la paleta)
const CAPA_FAROL := 2               # capa de render del farol nuevo: su propia luz no lo alcanza (no lo quema)
const LUCIERNAGAS_META := 10        # luciernagas reunidas junto a la banca para el regalo

var radio_minimapa := 8.5         # metros que abarca el minimapa en esta zona (lo lee el HUD)

var _j: Dictionary = {}           # layout.json -> "jugable"
var _inst: Dictionary = {}        # id del layout -> nodo
var _brillo: ShaderMaterial
var _cierre: StaticBody3D         # pared que cierra el porton
var _atajo_abierto := false
var _vida: Node3D                 # vida.gd: luciernagas, viento, haz del faro y pizarra
var _farol_luz: OmniLight3D       # el farol que se enciende a mano
var _farol_bombilla: MeshInstance3D
var _farol_charco: MeshInstance3D
var _sentada := false             # en la banca y quieta: las luciernagas se reunen
var _asiento := Vector3.ZERO
var _intentos_pizarra := 0


func _construir() -> void:
	encuadre = 0.19
	var datos: Variant = JSON.parse_string(FileAccess.get_file_as_string(LAYOUT))
	if datos is Dictionary:
		_j = (datos as Dictionary).get("jugable", {})
	else:
		push_warning("AVISO layout del mirador ilegible: %s" % LAYOUT)
	var lim: Dictionary = _j.get("limites", {"x": [-2.4, 5.3], "z": [-2.3, 1.6]})
	limites = Rect2(float(lim["x"][0]), float(lim["z"][0]), float(lim["x"][1]) - float(lim["x"][0]), float(lim["z"][1]) - float(lim["z"][0]))

	# la Luna baja al oeste (+X): la luz llega desde la derecha y el faro tiende su sombra sobre la terraza
	var luna := luces("noche", NOCHE)
	luna.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL    # la terraza cabe en un solo mapa
	# Los shaders aprobados dejan un 30 % de luz en las sombras proyectadas (D-015), y para ellos la caida de
	# un farol con la distancia es una «sombra»: cada OmniLight sumaria ese 30 % a todo lo que alcanza, sin
	# charcos de luz. De noche se pide la sombra completa; al salir vuelve el valor aprobado (ver al_salir).
	Materiales.ajustar_parametro("sombra_proyectada", 1.0)
	var r: Dictionary = montar_layout(LAYOUT, MODELOS)
	_inst = r["instancias"]

	_sombras_solo_cerca()

	_brillo = ShaderMaterial.new()
	_brillo.shader = BRILLO
	_brillo.set_shader_parameter("inclinacion", float(Materiales.parametros.get("inclinacion", cizalla)))
	Materiales.creados.append(_brillo)      # asi recibe los cambios de inclinacion de la zona
	_brillos_de_modelos()
	_vida = Vida.new()
	_vida.name = "Vida"
	add_child(_vida)
	_guirnaldas_y_ventanas()
	_ciudad_de_abajo()
	for l in _j.get("luces", []):
		var luz: Array = l
		farol(Vector3(float(luz[0]), float(luz[1]), float(luz[2])), CALIDO, float(luz[3]) * ENERGIA_FAROL, float(luz[4])).omni_attenuation = CAIDA_FAROL
	_vida.montar(_j)

	_colisiones()
	_entradas_y_umbrales()
	_interactuables()
	_interactuables_v2()
	if _toca_atajo():
		_abrir_atajo(false)
	else:
		var pp := _xz("porton", [6.2, -1.9])
		interactuable("Porton", pp + Vector3(-0.6, 0.0, 0.0), "Mirar el portón", _usar_porton, {"radio": 1.2, "altura_marca": 1.6})


# ------------------------------------------------------------------ rendimiento

func _sombras_solo_cerca() -> void:
	# en la HD 620 cada triangulo del mapa de sombras cuenta: solo proyecta sombra lo que esta sobre la terraza.
	# El suelo, el muro, la ladera, el barrio, las copas y las plantas de fuera no la necesitan.
	for hijo in get_children():
		if hijo is MultiMeshInstance3D:
			var nombre := String(hijo.name)
			if not (nombre.contains("MIR-07") or nombre.contains("URB-07") or nombre.contains("TAL-10")):
				(hijo as MultiMeshInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for clave in ["TER-15", "MIR-02"]:
		var raiz: Node = _inst.get(clave)
		if raiz == null:
			continue
		for nodo in raiz.find_children("*", "MeshInstance3D", true, false):
			if clave == "TER-15" or not String(nodo.name).contains("balaustrada"):
				(nodo as MeshInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


# ------------------------------------------------------------------ brillo calido y cian

func _brillos_de_modelos() -> void:
	# las superficies «Emisivo» de los GLB (ocular, lentes, pantalla) pasan al brillo inclinado
	for clave in _inst:
		var raiz: Node = _inst[clave]
		for nodo in raiz.find_children("*", "MeshInstance3D", true, false):
			var mi := nodo as MeshInstance3D
			if mi.mesh == null:
				continue
			for s in mi.mesh.get_surface_count():
				if mi.get_surface_override_material(s) is StandardMaterial3D:
					mi.set_surface_override_material(s, _brillo)


func _nodo_brillo(m: Dictionary, nombre: String) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = nombre
	mi.mesh = Piezas.malla(m)
	mi.material_override = _brillo
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	return mi


func _bombillas(m: Dictionary, lista: Array, color: Color) -> void:
	for b in lista:
		var p: Array = b
		Piezas.esfera(m, Vector3(float(p[0]), float(p[1]), float(p[2])), float(p[3]), color, 4, 2)


func _material_zona(shader: Shader, extra: Dictionary = {}) -> ShaderMaterial:
	# material propio de la zona que recibe los parametros comunes del estilo (inclinacion, pintado, sombras)
	var m := ShaderMaterial.new()
	m.shader = shader
	for nombre in Materiales.parametros:
		m.set_shader_parameter(nombre, Materiales.parametros[nombre])
	for nombre in extra:
		m.set_shader_parameter(nombre, extra[nombre])
	Materiales.creados.append(m)
	return m


func _malla_con_peso(m: Dictionary, pesos: Array) -> ArrayMesh:
	# como Piezas.malla, con el peso del vaiven de cada vertice en UV.x
	var mesh := ArrayMesh.new()
	if m["v"].is_empty():
		return mesh
	var uv := PackedVector2Array()
	for w in pesos:
		uv.append(Vector2(float(w), 0.0))
	var arrays: Array = []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = PackedVector3Array(m["v"])
	arrays[Mesh.ARRAY_NORMAL] = PackedVector3Array(m["n"])
	arrays[Mesh.ARRAY_COLOR] = PackedColorArray(m["c"])
	arrays[Mesh.ARRAY_TEX_UV] = uv
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return mesh


func _nodo_viento(m: Dictionary, pesos: Array, material: ShaderMaterial, nombre: String) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = nombre
	mi.mesh = _malla_con_peso(m, pesos)
	mi.material_override = material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	_vida.materiales_viento.append(material)
	return mi


func _cable(m: Dictionary, pesos: Array, linea: Array, color: Color, grosor: float) -> void:
	# dos cintas cruzadas por tramo, visibles desde la camara alta; el peso se reparte a lo largo del tramo
	for i in range(linea.size() - 1):
		var pa: Array = linea[i]
		var pb: Array = linea[i + 1]
		var a := Vector3(float(pa[0]), float(pa[1]), float(pa[2]))
		var b := Vector3(float(pb[0]), float(pb[1]), float(pb[2]))
		var wa: float = float(pa[3]) if pa.size() > 3 else 0.0
		var wb: float = float(pb[3]) if pb.size() > 3 else 0.0
		var lado := (b - a).cross(Vector3.UP).normalized() * grosor
		var alto := Vector3(0.0, grosor, 0.0)
		var medio := (a + b) * 0.5
		var antes: int = m["v"].size()
		for d in [lado, alto]:
			var desvio: Vector3 = d
			var otro: Vector3 = alto if desvio == lado else lado
			Piezas.cara(m, [a - desvio, b - desvio, b + desvio, a + desvio], color, medio + otro)
			Piezas.cara(m, [a - desvio, b - desvio, b + desvio, a + desvio], color, medio - otro)
		var largo2 := maxf((b - a).length_squared(), 0.000001)
		for k in range(antes, m["v"].size()):
			var v: Vector3 = m["v"][k]
			pesos.append(lerpf(wa, wb, clampf((v - a).dot(b - a) / largo2, 0.0, 1.0)))


func _guirnaldas_y_ventanas() -> void:
	# v2: cables, bombillas y banderines se mecen con el viento (vaiven.gdshader, peso en UV.x)
	var cables := Piezas.nueva()
	var pesos_cables: Array = []
	for c in _j.get("cables", []):
		_cable(cables, pesos_cables, c, CABLE, 0.011)
	for c in _j.get("cables_banderines", []):
		_cable(cables, pesos_cables, c, CUERDA, 0.008)
	for b in _j.get("banderines", []):
		var d: Array = b
		var p0 := Vector3(float(d[0]), float(d[1]), float(d[2]))
		var p1 := Vector3(float(d[3]), float(d[4]), float(d[5]))
		var p2 := Vector3(float(d[6]), float(d[7]), float(d[8]))
		var antes: int = cables["v"].size()
		Piezas.cara(cables, [p0, p1, p2], Color(String(d[9])))
		var ws := [float(d[10]), float(d[11]), float(d[12])]
		for k in range(antes, cables["v"].size()):
			var v: Vector3 = cables["v"][k]
			var cerca := 0
			var mejor := INF
			for q in 3:
				var dist: float = v.distance_squared_to([p0, p1, p2][q])
				if dist < mejor:
					mejor = dist
					cerca = q
			pesos_cables.append(ws[cerca])
	_nodo_viento(cables, pesos_cables, _material_zona(VAIVEN), "CablesYBanderines")
	# bombillas de la guirnalda: brillo calido que se mece con su cable y florece (glow) en la noche
	var bombillas := Piezas.nueva()
	var pesos_bombillas: Array = []
	for b in _j.get("bombillas", []):
		var p: Array = b
		var antes: int = bombillas["v"].size()
		Piezas.esfera(bombillas, Vector3(float(p[0]), float(p[1]), float(p[2])), float(p[3]), CALIDO, 4, 2)
		for k in range(antes, bombillas["v"].size()):
			pesos_bombillas.append(float(p[4]) if p.size() > 4 else 0.0)
	_nodo_viento(bombillas, pesos_bombillas, _material_zona(VAIVEN_BRILLO, {"energia": 1.5}), "BombillasGuirnalda")
	# faroles y ventanas encendidas del faro y del barrio
	var luz := Piezas.nueva()
	for q in _j.get("ventanas", []):
		var v: Array = q
		var pts: Array = []
		for p in v:
			pts.append(Vector3(float(p[0]), float(p[1]), float(p[2])))
		Piezas.cara(luz, pts, CALIDO)
	_nodo_brillo(luz, "LucesCalidas")


func _ciudad_de_abajo() -> void:
	# v2: la ciudad del valle como manchas de luces calidas lejanas (puntos de brillo, sin luces reales)
	var m := Piezas.nueva()
	# v2b: el barrio del valle este, dentro del encuadre; una sola malla (una llamada de dibujo), sin luces reales
	var tonos := [CALIDO, Color("f4a159"), Color("f8c991"), Color("daaa25")]
	var i := 0
	for p in _j.get("puntos_ciudad", []):
		var d: Array = p
		Piezas.esfera(m, Vector3(float(d[0]), float(d[1]), float(d[2])), float(d[3]) * 1.25, tonos[i % tonos.size()], 4, 2)
		i += 1
	var mi := MeshInstance3D.new()
	mi.name = "LucesCiudad"
	mi.mesh = Piezas.malla(m)
	mi.material_override = _material_zona(BRILLO, {"energia": 1.35})    # v2c: con 1,9 las lejanas salian blancas
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	# reflejo frio de la Luna en el rio
	var r := Piezas.nueva()
	for q in _j.get("reflejo_luna", []):
		var pts: Array = []
		for p in q:
			pts.append(Vector3(float(p[0]), float(p[1]), float(p[2])))
		Piezas.cara(r, pts, REFLEJO, (pts[0] + pts[2]) * 0.5 - Vector3.UP)
	var ri := MeshInstance3D.new()
	ri.name = "ReflejoLuna"
	ri.mesh = Piezas.malla(r)
	ri.material_override = _material_zona(BRILLO, {"energia": 0.75})
	ri.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(ri)


# ------------------------------------------------------------------ colisiones

func _muro(a: Vector2, b: Vector2, alto: float = 1.6, y: float = 0.0, grosor: float = 0.3) -> StaticBody3D:
	var d := b - a
	if d.length() < 0.01:
		return null
	var c := (a + b) * 0.5
	return pared(Vector3(c.x, y + alto * 0.5, c.y), Vector3(d.length() + grosor, alto, grosor), rad_to_deg(atan2(-d.y, d.x)))


func _colisiones() -> void:
	var p: Dictionary = _j.get("piso", {"centro": [1.6, 0.0], "tam": [16.4, 9.6]})
	piso(Vector3(float(p["centro"][0]), 0.0, float(p["centro"][1])), Vector2(float(p["tam"][0]), float(p["tam"][1])))
	for m in _j.get("muros", []):
		var t: Array = m
		_muro(Vector2(float(t[0]), float(t[1])), Vector2(float(t[2]), float(t[3])), float(t[4]))
	for c in _j.get("columnas", []):
		var col: Array = c
		columna(Vector3(float(col[0]), 0.0, float(col[1])), float(col[2]), float(col[3]))
	for c in _j.get("cajas", []):
		var caja: Array = c
		var alto: float = caja[5]
		pared(Vector3(float(caja[0]), alto * 0.5, float(caja[1])), Vector3(float(caja[2]), alto, float(caja[3])), float(caja[4]))
	var cierre: Array = _j.get("cierre_porton", [6.2, -3.15, 6.2, -0.65, 1.6])
	_cierre = _muro(Vector2(float(cierre[0]), float(cierre[1])), Vector2(float(cierre[2]), float(cierre[3])), float(cierre[4]))


# ------------------------------------------------------------------ entradas, umbrales y el atajo

func _xz(clave: String, defecto: Array) -> Vector3:
	var a: Array = _j.get(clave, defecto)
	return Vector3(float(a[0]), 0.0, float(a[1]))


func _entradas_y_umbrales() -> void:
	var e: Dictionary = _j.get("entrada", {"pos": [-3.55, -1.55], "mira": [0.5, 0.87]})
	var pos := Vector3(float(e["pos"][0]), 0.0, float(e["pos"][1]))
	var mira := Vector3(float(e["mira"][0]), 0.0, float(e["mira"][1])).normalized()
	entrada("inicio", pos, mira)
	entrada("sendero", pos, mira)
	umbral("AlSendero", _xz("umbral_sendero", [-4.2, -3.0]), "sendero", "mirador", "Al sendero del arroyo")


func _toca_atajo() -> bool:
	# en la visita libre (menu Lugares) el atajo se ve abierto, para poder validar el escenario entero
	return (bool(Juego.bandera("mir_luna")) and bool(Juego.bandera("mir_linea"))) or bool(Juego.bandera("visita_libre"))


func _hoja(nombre: String) -> Node3D:
	var porton: Node = _inst.get("MIR-10")
	if porton == null:
		return null
	for hijo in porton.find_children("*", "Node3D", true, false):
		if String(hijo.name).contains(nombre):
			return hijo as Node3D
	return null


func _abrir_atajo(animado: bool) -> void:
	if _atajo_abierto:
		return
	_atajo_abierto = true
	if _cierre != null and is_instance_valid(_cierre):
		_cierre.queue_free()
		_cierre = null
	var marca := get_node_or_null("Porton")
	if marca != null:
		marca.queue_free()
	# las hojas giran hacia dentro de la terraza: asi no tapan la marca del descanso de la bajada
	var giros := {"hoja_n": deg_to_rad(-100.0), "hoja_s": deg_to_rad(100.0)}
	for clave in giros:
		var hoja := _hoja(clave)
		if hoja == null:
			continue
		if animado:
			create_tween().tween_property(hoja, "rotation:y", float(giros[clave]), 1.2).set_trans(Tween.TRANS_SINE)
		else:
			hoja.rotation.y = float(giros[clave])
	# los faroles del porton se encienden
	var luz := Piezas.nueva()
	_bombillas(luz, _j.get("porton_bombillas", []), CALIDO)
	_nodo_brillo(luz, "LucesPorton")
	var lp: Array = _j.get("luz_porton", [6.3, 1.7, -1.9, 1.3, 4.5])
	farol(Vector3(float(lp[0]), float(lp[1]), float(lp[2])), CALIDO, float(lp[3]) * ENERGIA_FAROL, float(lp[4])).omni_attenuation = CAIDA_FAROL
	umbral("AtajoFaroles", _xz("umbral_atajo", [7.35, -1.9]), "habitacion", "escalera", "Bajada de los faroles: a casa")


func _revisar_cierre() -> void:
	# con la Luna vista y la linea de tiempo ordenada, la noche del Mirador termina y se abre el atajo
	if not (bool(Juego.bandera("mir_luna")) and bool(Juego.bandera("mir_linea"))) or bool(Juego.bandera("mir_cierre")):
		return
	Juego.poner_bandera("mir_cierre")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "La Luna ya se puso: hoy se ocultó a las 21:07. Es hora de volver a casa."},
		{"quien": "Órbita", "texto": "Abrieron el portón del cerro, junto al faro. La bajada de los faroles nos deja en casa."},
	])
	if not _atajo_abierto:
		Audio.sonar("logro")
		_abrir_atajo(true)


# ------------------------------------------------------------------ interactuables

func _interactuables() -> void:
	var puntos: Dictionary = _j.get("interactuables", {})
	var lista := [
		["MesaClub", "Armar la maqueta de Pegaso", _usar_mesa, 1.15, 1.3, [0.15, -2.24]],
		["Simulador", "Probar el simulador de órbitas", _usar_simulador, 1.0, 1.25, [0.88, -2.22]],
		["Telescopio", "Mirar por el telescopio", _usar_telescopio, 1.3, 1.55, [2.9, 1.38]],
		["Atril", "Ordenar las diapositivas", _usar_atril, 1.4, 1.65, [-4.2, 0.4]],
		["Binoculares", "Mirar el barrio", _usar_binoculares, 1.2, 1.45, [-2.65, 2.55]],
		["Banca", "Sentarse a mirar la Luna", _usar_banca, 1.3, 0.95, [-1.6, -3.85]],
		["Faro", "Mirar el faro", _usar_faro, 1.3, 1.7, [1.78, -0.5]],
	]
	for dato in lista:
		var d: Array = dato
		var xz: Array = puntos.get(d[0], d[5])
		interactuable(String(d[0]), Vector3(float(xz[0]), 0.0, float(xz[1])), String(d[1]), d[2], {"radio": float(d[3]), "altura_marca": float(d[4])})


func _usar_mesa() -> void:
	if Juego.bandera("mir_satelite"):
		await Interfaz.decir([{"quien": "Órbita", "texto": "La maqueta de Pegaso quedó armada: un cubo de 10 cm y dos paneles de 27 cm."}])
		return
	if not Juego.bandera("mir_mesa_vista"):
		Juego.poner_bandera("mir_mesa_vista")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "La mesa del club. Están armando una maqueta de Pegaso, el primer satélite ecuatoriano."},
			{"quien": "Órbita", "texto": "Le faltan cuatro partes: energía, radio, antena y computadora."},
		])
	var r: Dictionary = await Interfaz.abrir_minijuego("satelite", {"dificultad": 1})
	if r.get("superado", false):
		Juego.poner_bandera("mir_satelite")
		Juego.anotar("pegaso")
		Juego.anotar("cubesat")
		Audio.sonar("logro")
		await Interfaz.decir([{"quien": "Órbita", "texto": "Maqueta lista. El Pegaso de verdad era así de pequeño: un cubo de 10 cm."}])
	else:
		Interfaz.aviso("La maqueta sigue a medias. Puedes intentarlo otra vez.", 3.0)


func _usar_simulador() -> void:
	if not Juego.bandera("mir_simulador_visto"):
		Juego.poner_bandera("mir_simulador_visto")
		await Interfaz.decir([{"quien": "Órbita", "texto": "El portátil del club tiene un simulador: un satélite ni se cae ni se escapa si lleva la velocidad justa."}])
	var r: Dictionary = await Interfaz.abrir_minijuego("orbita", {"dificultad": 1})
	if r.get("superado", false):
		Juego.poner_bandera("mir_orbita")
		Juego.anotar("pegaso_orbita")
		await Interfaz.decir([{"quien": "Órbita", "texto": "Órbita estable. Pegaso giró entre 627 y 654 km de altura."}])


func _usar_telescopio() -> void:
	if not Juego.bandera("mir_telescopio_visto"):
		Juego.poner_bandera("mir_telescopio_visto")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "La Luna está baja, al oeste: a 20,0° de altura y a 403 151 km."},
			{"quien": "Órbita", "texto": "Hoy solo tiene iluminado el 12,2 %. Búscala y enfócala."},
		])
	var r: Dictionary = await Interfaz.abrir_minijuego("telescopio", {"dificultad": 1})
	if r.get("superado", false):
		var primera := not bool(Juego.bandera("mir_luna"))
		Juego.poner_bandera("mir_luna")
		Juego.anotar("luna_12_noviembre")
		Juego.anotar("luz_cenicienta")
		if primera:
			Audio.sonar("logro")
			await Interfaz.decir([{"quien": "Órbita", "texto": "La parte oscura se alcanza a ver: es la luz cenicienta, luz que la Tierra le refleja a la Luna."}])
		await _revisar_cierre()
	else:
		Interfaz.aviso("La Luna se salió del ocular. Puedes intentarlo otra vez.", 3.0)


func _usar_atril() -> void:
	if not Juego.bandera("mir_atril_visto"):
		Juego.poner_bandera("mir_atril_visto")
		await Interfaz.decir([{"quien": "Órbita", "texto": "El atril del club, con su carta estelar. Alguien dejó las diapositivas desordenadas."}])
	var r: Dictionary = await Interfaz.abrir_minijuego("linea_tiempo", {"dificultad": 1})
	if r.get("superado", false):
		var primera := not bool(Juego.bandera("mir_linea"))
		Juego.poner_bandera("mir_linea")
		Juego.anotar("disco_apolo11")
		if primera:
			Audio.sonar("logro")
			await Interfaz.decir([{"quien": "Órbita", "texto": "En orden. El disco del Apolo 11 llevó mensajes de 73 países, y uno era de Ecuador."}])
		await _revisar_cierre()
	else:
		Interfaz.aviso("Las diapositivas siguen desordenadas. Puedes intentarlo otra vez.", 3.0)


func _usar_binoculares() -> void:
	Juego.anotar("luna_sonriente")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Las Escalinatas de noche: cada ventana encendida es una casa del barrio."},
		{"quien": "Órbita", "texto": "Y sobre los techos, la Luna sonriente: su borde iluminado apunta hacia abajo."},
	])


func _usar_porton() -> void:
	await Interfaz.decir([{"quien": "Órbita", "texto": MSG_PORTON}])


func _usar_banca() -> void:
	# v2: la protagonista se sienta frente a la banca, Orbita se sube a ella y las luciernagas se acercan
	var asiento: Array = _j.get("banca_asiento", [-1.25, -3.23])
	var pos := Vector3(float(asiento[0]), 0.05, float(asiento[1]))
	var mira := Vector3(0.75, 0.0, 0.66).normalized()      # hacia el oeste y la ciudad: alli baja la Luna
	Zonas.jugador.colocar(pos, mira)
	if Zonas.companero != null and is_instance_valid(Zonas.companero):
		Zonas.companero.global_position = Vector3(pos.x + 0.45, 0.62, -3.85)
	Audio.sonar("pulsar")
	# v2b: sentada y quieta, las luciernagas dejan de huir y se reunen; si llegan 10, hay regalo (ver _process)
	_vida.reunir = pos + Vector3(0.3, 0.0, 0.4)
	_vida.calma = true
	_sentada = true
	_asiento = pos
	var vez: int = int(Juego.bandera("mir_banca_veces", 0))
	Juego.poner_bandera("mir_banca_veces", vez + 1)
	var lineas: Array = []
	match vez % 3:
		0:
			lineas = [
				{"quien": "Órbita", "texto": "Buen sitio. Desde la banca se ve la Luna bajando al oeste, sobre los techos del barrio."},
				{"quien": "Órbita", "texto": "Esta noche tiene iluminado el 12,2 %. Está a 20,0° de altura y a 403 151 km."},
				{"quien": "Órbita", "texto": "Mira: las luciérnagas también vinieron a verla."},
			]
			Juego.anotar("luna_12_noviembre")
		1:
			lineas = [
				{"quien": "Órbita", "texto": "La parte oscura de la Luna no está negra del todo: la alumbra la luz que refleja la Tierra."},
				{"quien": "Órbita", "texto": "Se llama luz cenicienta. Con tan poca Luna iluminada, hoy se nota bien."},
			]
			Juego.anotar("luz_cenicienta")
		_:
			lineas = [
				{"quien": "Órbita", "texto": "Mañana a esta hora la Luna estará más alta: a 31,0°, y con el 19,0 % iluminado."},
				{"quien": "Órbita", "texto": "Cada noche crece un poco. Por eso hay que mirarla hoy, antes de que se ponga."},
			]
			Juego.anotar("luna_13_noviembre")
	await Interfaz.decir(lineas)
	if not bool(Juego.bandera("mir_luciernagas")):
		Interfaz.aviso("Quédate quieta en la banca: las luciérnagas se acercan.", 3.0)


func _levantarse() -> void:
	_sentada = false
	_vida.calma = false
	_vida.reunir = Vector3.INF


func _process(_delta: float) -> void:
	if not _sentada or _vida == null:
		return
	var j: Node3D = Zonas.jugador
	if j == null or not is_instance_valid(j):
		return
	if Vector2(j.global_position.x - _asiento.x, j.global_position.z - _asiento.z).length() > 0.35:
		_levantarse()
		return
	if bool(Juego.bandera("mir_luciernagas")) or Interfaz.ocupada():
		return
	if _vida.luciernagas_cerca(_vida.reunir, 1.0) >= LUCIERNAGAS_META:
		_regalo_luciernagas()


func _regalo_luciernagas() -> void:
	# diez luciernagas reunidas alumbran algo bajo la banca: una placa de circuito (COL-03) y un dato real
	Juego.poner_bandera("mir_luciernagas")
	Audio.sonar("logro")
	_poner_regalo()
	Juego.anotar("cielo_15_grados")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Diez luciérnagas juntas. Su luz alumbra algo bajo la banca: ¡una placa de circuito!"},
		{"quien": "Órbita", "texto": "Mientras esperabas quieta, el cielo siguió girando: unos 15° por hora. Por eso la Luna baja al oeste."},
	])


func _poner_regalo() -> void:
	if get_node_or_null("PlacaLuciernagas") != null or bool(Juego.bandera("tomo_mirador_PlacaLuciernagas")):
		return
	var p: Array = _j.get("regalo_luciernagas", [-2.0, -2.95])
	var pos := Vector3(float(p[0]), 0.0, float(p[1]))
	var visual := modelo("res://modelos/ciudad/COL-03.glb", pos, 30.0, {"escala": 1.4})
	recolectable("PlacaLuciernagas", pos, "placa_de_circuito", visual, "Recoger la placa de circuito")


# ------------------------------------------------------------------ v2: farol, pizarra y recolectables

func _interactuables_v2() -> void:
	var puntos: Dictionary = _j.get("interactuables", {})
	# farol apagado junto a la balaustrada sur
	var fp: Array = puntos.get("Farol", [-1.7, 2.65])
	var texto_farol := "Apagar el farol" if bool(Juego.bandera("mir_farol")) else "Encender el farol"
	interactuable("Farol", Vector3(float(fp[0]), 0.0, float(fp[1])), texto_farol, _usar_farol, {"radio": 1.1, "altura_marca": 1.5})
	if bool(Juego.bandera("mir_farol")):
		_farol(true, false)
	# pizarra de constelaciones
	var pp: Array = puntos.get("Pizarra", [-0.35, 2.85])
	interactuable("Pizarra", Vector3(float(pp[0]), 0.0, float(pp[1])), _texto_pizarra(), _usar_pizarra, {"radio": 1.2, "altura_marca": 1.7})
	_vida.pizarra_preparar(_pizarra_elegidas())
	if bool(Juego.bandera("mir_luciernagas")):
		_poner_regalo()
	# recolectables de la familia COL (cada uno, una vez por partida)
	var recs: Dictionary = _j.get("recolectables", {})
	for nombre in recs:
		var r: Array = recs[nombre]
		var visual: Node3D = _inst.get("%s_rec" % String(r[3]))
		recolectable(String(nombre), Vector3(float(r[0]), 0.0, float(r[1])), String(r[2]), visual, "Recoger")


func _charco(centro: Vector3, radio: float) -> MeshInstance3D:
	# disco de 24 lados con UV de 0 a 1 (el shader pinta la caida desde el centro)
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var lados := 24
	for k in lados:
		var a0 := TAU * float(k) / float(lados)
		var a1 := TAU * float(k + 1) / float(lados)
		for par in [[0.0, 0.0], [cos(a0), sin(a0)], [cos(a1), sin(a1)]]:
			var q: Array = par
			st.set_uv(Vector2(0.5 + 0.5 * float(q[0]), 0.5 + 0.5 * float(q[1])))
			st.add_vertex(centro + Vector3(float(q[0]) * radio, 0.0, float(q[1]) * radio))
	var mi := MeshInstance3D.new()
	mi.name = "FarolCharco"
	mi.mesh = st.commit()
	mi.material_override = _material_zona(CHARCO)
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	return mi


func _farol(encender: bool, animado: bool) -> void:
	var datos: Dictionary = _j.get("farol_nuevo", {})
	if encender:
		if _farol_luz == null:
			var l: Array = datos.get("luz", [-1.95, 2.0, 3.0, 3.0, 3.6])
			_farol_luz = farol(Vector3(float(l[0]), float(l[1]), float(l[2])), CALIDO, float(l[3]) * ENERGIA_FAROL, float(l[4]))
			_farol_luz.omni_attenuation = CAIDA_FAROL
			# v2b: el poste del farol va en su propia capa y esta luz no la alcanza: antes lo quemaba como un neon
			_farol_luz.light_cull_mask = 1
			# v2c: tampoco alcanza la balaustrada (el pilar de al lado se quemaba): el charco queda en las losas
			for clave in ["ARQ-09_nuevo", "MIR-02"]:
				var raiz: Node = _inst.get(clave)
				if raiz == null:
					continue
				for nodo in raiz.find_children("*", "MeshInstance3D", true, false):
					if clave == "MIR-02" and not String(nodo.name).contains("balaustrada"):
						continue
					(nodo as MeshInstance3D).layers = 1 << (CAPA_FAROL - 1)
			var m := Piezas.nueva()
			var b: Array = datos.get("bombilla", [-1.95, 2.25, 3.0, 0.11])
			Piezas.esfera(m, Vector3(float(b[0]), float(b[1]), float(b[2])), float(b[3]), DORADO, 6, 3)
			_farol_bombilla = _nodo_brillo(m, "FarolBombilla")
			_farol_bombilla.material_override = _material_zona(BRILLO, {"energia": 1.6})
			# v2c: el charco dorado se pinta (charco.gdshader): en el acabado pintado la OmniLight sola apenas calienta las losas
			var c: Array = datos.get("charco", [-1.85, 2.35, 1.5])
			_farol_charco = _charco(Vector3(float(c[0]), 0.012, float(c[1])), float(c[2]))
		_farol_luz.visible = true
		_farol_bombilla.visible = true
		_farol_charco.visible = true
		if animado:
			# chispa al prender: sube, titila y se asienta
			var energia := _farol_luz.light_energy
			var t := create_tween()
			_farol_luz.light_energy = 0.0
			t.tween_property(_farol_luz, "light_energy", energia * 1.35, 0.18)
			t.tween_property(_farol_luz, "light_energy", energia * 0.6, 0.10)
			t.tween_property(_farol_luz, "light_energy", energia, 0.35)
	elif _farol_luz != null:
		_farol_luz.visible = false
		_farol_bombilla.visible = false
		_farol_charco.visible = false


func _usar_farol() -> void:
	var encendido := not bool(Juego.bandera("mir_farol"))
	Juego.poner_bandera("mir_farol", encendido)
	_farol(encendido, true)
	Audio.sonar("ok" if encendido else "pulsar")
	var nodo := get_node_or_null("Farol")
	if nodo != null:
		nodo.set("texto", "Apagar el farol" if encendido else "Encender el farol")
	if encendido and not bool(Juego.bandera("mir_farol_visto")):
		Juego.poner_bandera("mir_farol_visto")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "Con luz se lee mejor la pizarra del club."},
			{"quien": "Órbita", "texto": "Pero para mirar el cielo conviene apagarla: los ojos tardan unos minutos en acostumbrarse a la oscuridad."},
		])


# Pizarra (v2b): cinco estrellas de tiza; tres dibujan la Luna de esta noche. Se unen en orden una punta, el borde
# iluminado (abajo) y la otra punta. Una estrella equivocada (dos son senuelo) borra la tiza y hay que empezar.
# Estrellas (layout "pizarra"): 0 punta izquierda, 1 borde de abajo, 2 punta derecha, 3 y 4 senuelos.
const NOMBRES_ESTRELLA := ["La de la izquierda", "La de abajo", "La de la derecha", "La de arriba", "La del centro"]
const ORDEN_LECTURA := [0, 3, 4, 1, 2]     # como se leen en la pizarra, de izquierda a derecha


func _pizarra_elegidas() -> Array:
	var e: Variant = Juego.bandera("mir_pizarra_estrellas", [])
	return (e as Array).duplicate() if e is Array else []


func _texto_pizarra() -> String:
	var n := _pizarra_elegidas().size()
	if n >= 3:
		return "Mirar la Luna de tiza"
	return "Unir las estrellas de la Luna (%d de 3)" % n


func _pizarra_correcta(elegidas: Array, estrella: int) -> bool:
	match elegidas.size():
		0:
			return estrella == 0 or estrella == 2
		1:
			return estrella == 1
		2:
			return estrella == 2 - int(elegidas[0])
	return false


func _opciones_pizarra(elegidas: Array) -> Array:
	# las estrellas libres en orden de lectura; en modo prueba el dialogo elige siempre la primera opcion, asi que
	# el primer intento de la prueba empieza por un senuelo (comprueba el borrado) y los siguientes por la buena
	var libres: Array = []
	for i in ORDEN_LECTURA:
		if not elegidas.has(i):
			libres.append(i)
	if Juego.modo_prueba:
		var buena := -1
		for i in libres:
			if _pizarra_correcta(elegidas, int(i)):
				buena = int(i)
				break
		var primera := buena
		if _intentos_pizarra == 1 and elegidas.is_empty():
			primera = 3
		libres.erase(primera)
		libres.push_front(primera)
	return libres


func _usar_pizarra() -> void:
	var elegidas := _pizarra_elegidas()
	if elegidas.size() >= 3:
		await Interfaz.decir([{"quien": "Órbita", "texto": "La Luna de esta noche, en tiza: una creciente fina con el borde iluminado hacia abajo, como una sonrisa."}])
		return
	_intentos_pizarra += 1
	if not bool(Juego.bandera("mir_pizarra_vista")):
		Juego.poner_bandera("mir_pizarra_vista")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "La pizarra del club. Hay cinco estrellas de tiza, pero solo tres dibujan la Luna de esta noche."},
			{"quien": "Órbita", "texto": "Únelas en orden: una punta, el borde iluminado y la otra punta. Pista: esta noche la Luna sonríe."},
		])
	var nodo := get_node_or_null("Pizarra")
	while elegidas.size() < 3:
		var libres := _opciones_pizarra(elegidas)
		var textos: Array = []
		for i in libres:
			textos.append(String(NOMBRES_ESTRELLA[int(i)]))
		textos.append("Dejarlo para después")
		var preguntas := ["¿Por qué estrella empiezas?", "¿Y ahora?", "¿Cuál cierra la Luna?"]
		var paso: String = preguntas[elegidas.size()]
		var k: int = await Interfaz.elegir({"quien": "Órbita", "texto": paso}, textos)
		if k >= libres.size():
			return
		var estrella: int = int(libres[k])
		if not _pizarra_correcta(elegidas, estrella):
			Audio.sonar("error")
			Juego.poner_bandera("mir_pizarra_estrellas", [])
			await _vida.pizarra_error(estrella)
			if nodo != null:
				nodo.set("texto", _texto_pizarra())
			var pista := "Esa no es de la Luna: el borrador se llevó la tiza. Empieza por una punta de la creciente."
			if elegidas.size() == 1:
				pista = "Esa no: después de la punta va el borde iluminado, que esta noche queda abajo. La tiza se borró."
			elif elegidas.size() == 2:
				pista = "Esa no: la Luna se cierra en la otra punta, a la misma altura que la primera. La tiza se borró."
			await Interfaz.decir([{"quien": "Órbita", "texto": pista}])
			return
		elegidas.append(estrella)
		Juego.poner_bandera("mir_pizarra_estrellas", elegidas.duplicate())
		_vida.pizarra_dibujar(elegidas, true)
		Audio.sonar("pagina" if elegidas.size() > 1 else "tic")
		if nodo != null:
			nodo.set("texto", _texto_pizarra())
	Juego.poner_bandera("mir_pizarra", 3)
	Audio.sonar("logro")
	var i: int = await Interfaz.elegir({"quien": "Órbita", "texto": "¡Una Luna! ¿Hacia dónde apunta su borde iluminado?"}, ["Hacia arriba", "Hacia abajo, como una sonrisa"])
	var lineas: Array = []
	if i == 1:
		lineas.append({"quien": "Órbita", "texto": "Eso es. Cuando la creciente tiene el borde iluminado abajo, parece una sonrisa."})
	else:
		lineas.append({"quien": "Órbita", "texto": "Mira la tiza otra vez: la curva gruesa está abajo. Ese es el borde que alumbra el Sol."})
	lineas.append({"quien": "Órbita", "texto": "Así la vemos esta noche desde el Mirador, baja y al oeste. Con los binoculares se ve igual sobre los techos."})
	Juego.anotar("luna_sonriente")
	await Interfaz.decir(lineas)


func _usar_faro() -> void:
	Juego.anotar("polo_sur_celeste")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "El faro del cerro. Su linterna se ve desde todo el barrio."},
		{"quien": "Órbita", "texto": "Desde aquí, a 2,18° S, el polo sur celeste queda a unos 2,2° sobre el horizonte."},
	])


# ------------------------------------------------------------------ vida de la zona

func al_entrar(_nombre_entrada: String) -> void:
	if not Juego.bandera("mirador_visitado"):
		Juego.poner_bandera("mirador_visitado")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "El Mirador del Faro. El club de astronomía dejó su mesa junto al faro."},
			{"quien": "Órbita", "texto": "La Luna está baja, al oeste. Hay que verla antes de que se ponga."},
		])
	else:
		await _revisar_cierre()


func al_salir() -> void:
	Materiales.ajustar_parametro("sombra_proyectada", SOMBRA_APROBADA)


func orbita_dice() -> Array:
	if _atajo_abierto and bool(Juego.bandera("mir_luna")) and bool(Juego.bandera("mir_linea")):
		return [{"quien": "Órbita", "texto": "El portón del cerro está abierto, junto al faro. La bajada de los faroles nos deja en casa."}]
	if bool(Juego.bandera("mir_satelite")) and not bool(Juego.bandera("mir_luna")):
		return [{"quien": "Órbita", "texto": "El telescopio apunta al oeste, sobre el barrio. La Luna de hoy es una sonrisa fina y baja."}]
	return []


func ruta_de_prueba() -> Array:
	# v2: la ruta pasa tambien por la banca, los tres recolectables, el farol y la pizarra
	var ruta: Dictionary = _j.get("ruta", {})
	var pasos: Array = []
	var ir := func(clave: String, defecto: Array) -> void:
		var xz: Array = ruta.get(clave, defecto)
		pasos.append({"ir": Vector3(float(xz[0]), 0.0, float(xz[1]))})
	var recoger := func(nombre: String, defecto: Array) -> void:
		if not bool(Juego.bandera("tomo_mirador_%s" % nombre)) and get_node_or_null(nombre) != null:
			ir.call(nombre, defecto)
			pasos.append({"usar": nombre})
	ir.call("banca", [-1.6, -3.1])
	# de camino a la banca pasa junto a las luciernagas de la maceta: se apartan
	pasos.append({"bandera": "mir_luciernagas_susto"})
	if not bool(Juego.bandera("mir_luciernagas")):
		pasos.append({"usar": "Banca"})
		# sentada y quieta: las luciernagas se reunen (10 o mas) y aparece la placa bajo la banca
		pasos.append({"esperar": 6.0})
		pasos.append({"bandera": "mir_luciernagas"})
		pasos.append({"esperar": 0.5})
		var rg: Array = _j.get("regalo_luciernagas", [-2.0, -2.95])
		pasos.append({"ir": Vector3(float(rg[0]) + 0.35, 0.0, float(rg[1]) + 0.3)})
		pasos.append({"usar": "PlacaLuciernagas"})
	ir.call("tras_banca", [-1.9, -1.95])
	var tramos := [["mesa", "MesaClub", "mir_satelite", [-0.1, -1.34]], ["telescopio", "Telescopio", "mir_luna", [2.33, 1.63]], ["atril", "Atril", "mir_linea", [-3.75, 1.35]]]
	for tramo in tramos:
		var t: Array = tramo
		if String(t[0]) == "telescopio":
			recoger.call("AntenaVarilla", [1.3, -0.85])
		if String(t[0]) == "atril":
			pasos.append({"ir": Vector3(0.5, 0.0, 1.0)})
		ir.call(String(t[0]), t[3])
		if not Juego.bandera(String(t[2])):
			pasos.append({"usar": String(t[1])})
		pasos.append({"bandera": String(t[2])})
	recoger.call("CartaEstelar", [-3.05, 1.55])
	if not bool(Juego.bandera("mir_farol")):
		ir.call("Farol", [-1.7, 2.45])
		pasos.append({"usar": "Farol"})
		pasos.append({"bandera": "mir_farol"})
	if _pizarra_elegidas().size() < 3:
		ir.call("Pizarra", [-0.35, 3.05])
		# primer intento: un senuelo borra la tiza; segundo intento: punta, borde y punta
		pasos.append({"usar": "Pizarra"})
		pasos.append({"usar": "Pizarra"})
		pasos.append({"bandera": "mir_pizarra"})
		ir.call("tras_pizarra", [0.65, 2.9])
	pasos.append({"esperar": 0.5})
	ir.call("paso_1", [1.0, 0.3])
	recoger.call("CableCobre", [4.6, 0.8])
	for clave in ["paso_2", "paso_3"]:
		if ruta.has(clave):
			var xz: Array = ruta[clave]
			pasos.append({"ir": Vector3(float(xz[0]), 0.0, float(xz[1]))})
	pasos.append({"ir": _xz("umbral_atajo", [7.35, -1.9])})
	# el piloto llega mientras la zona cambia: este paso espera a que el cambio termine antes de seguir
	pasos.append({"esperar": 0.5})
	return pasos
