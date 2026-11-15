extends "res://nucleo/zona.gd"

# La Plaza de las Iguanas: la plaza del barrio al pie de Las Escalinatas, entre la casa de la protagonista
# (izquierda) y la boca del camino del cerro (derecha). Al fondo, la Biblioteca municipal (ARQ-13): por su
# puerta sale la luz cian de los dos libros de «Tu primera base espacial» (minijuegos base_luna y base_marte).
#
# PROVISIONAL: no hay concepto validado por Guillermo. Se construye con el estilo aprobado (D-011, D-015) y
# las hojas HR_URB_v1, HR_ARQ_v1, HR_VEG_v1 y HR_COL_v1. Las mallas las escriben herramientas/mallas/
# ciudad_mobiliario.py, ciudad_arquitectura.py y ciudad_vida.py en modelos/ciudad/.
#
# Version 2 («color y vida», 2026-11-14):
# - Color: suelo TER-14 en panos de tres tonos con cenefas de mosaico, una onda turquesa, las ocho fases de la
#   Luna alrededor de la fuente y un medallon con una iguana; fachadas vivas con marcos de cal, postigos,
#   zocalos y toldos en contraste; buganvillas, macetas URB-15, cocoteros VEG-04 y guirnaldas de banderines
#   que se mueven con el viento; agua turquesa en la fuente; de noche, ventanas y bombillas calidas.
# - Vida: iguanas que toman el sol, cabecean y se apartan (o se esconden si se corre); palomas FAU-12 que
#   levantan vuelo, se posan en la cornisa y vuelven; la fuente salpica; la banca calma la plaza; puesto de
#   frutas URB-13 (Lidia lo deja «a la confianza»); tablon URB-14 con la convocatoria; mosaico de las lunas;
#   tres recolectables de la familia COL.
#
# Plano (metros; la fuente en el origen; -Z es arriba en pantalla):
#   x -13..13, z -9.3..8.2. Fachadas: arriba z = -9.85, izquierda x = -13.3, derecha x = 13.3.
# Estados: tarde (la luz aprobada) y noche (mir_luna puesta; provisional, con los faroles encendidos).

const MODELOS := "res://modelos"
const C := "ciudad/"
const E := "entorno/"
const VEL_ESPANTA := 2.8          # m/s: por encima de esto la iguana se esconde (caminar son 2,0 y correr 3,6)
const DIST_ESPANTA := 3.0         # m
const DIST_APARTA := 1.05         # m: caminando, mas cerca que esto la iguana se aparta
const DIST_PALOMAS := 1.9         # m: caminando, mas cerca que esto las palomas levantan vuelo
const DIST_PALOMAS_CORRER := 3.8  # m: corriendo

const P_CASA := Vector3(-12.0, 0.0, 0.55)        # umbral ACasa (losa clara del suelo TER-14)
const P_SENDERO := Vector3(12.3, 0.0, 1.2)       # umbral AlSendero
const P_BIBLIO := Vector3(0.0, 0.42, -8.72)      # puerta de la biblioteca, sobre el podio
const Z_FACHADA := -9.85                         # fachadas de la hilera del fondo
const FAROLES_DOBLES := [Vector2(-5.4, -3.4), Vector2(5.4, -3.4), Vector2(-5.4, 4.4), Vector2(5.4, 4.4)]
const FAROLES := [Vector2(-10.9, -1.5), Vector2(10.9, -0.75)]
const BANCAS := [[-3.4, -4.9, 0.0], [3.4, -4.9, 0.0], [-5.1, -1.4, 90.0], [5.1, -1.4, -90.0], [-7.6, 7.35, 180.0], [6.6, 7.35, 180.0]]
const JARDINERAS := [[-4.35, -7.25, 0.0], [4.35, -7.25, 0.0], [-2.6, 5.55, 0.0], [2.6, 5.55, 0.0], [-10.4, 7.6, 0.0], [10.0, 7.6, 0.0], [-0.5, 7.6, 0.0]]
# iguanas al sol (FAU-01): x, z, giro, y. La cuarta toma el sol en el borde de la fuente.
const IGUANAS := [[-5.6, 6.3, 205.0, 0.012], [7.9, 3.1, 130.0, 0.012], [-9.3, -3.1, 60.0, 0.012], [1.06, -1.06, 135.0, 0.445]]
# sitios a los que cada iguana se aparta (el primero es su sitio)
const SITIOS_IGUANA := [
	[Vector2(-5.6, 6.3), Vector2(-4.3, 6.9), Vector2(-5.9, 7.7)],
	[Vector2(7.9, 3.1), Vector2(8.9, 3.9), Vector2(7.1, 4.0)],
	[Vector2(-9.3, -3.1), Vector2(-8.5, -2.2), Vector2(-10.1, -3.7)],
	[Vector2(1.06, -1.06)],
]
const P_PUESTO := Vector3(-10.4, 0.0, -5.9)      # puesto de frutas URB-13
const P_TABLON := Vector3(4.5, 0.0, -6.3)        # tablon de anuncios URB-14
const PALMAS := [[-11.8, -7.3, 20.0], [11.4, 6.9, 200.0], [-11.9, 6.4, 120.0], [12.55, -3.0, 170.0], [-4.05, -9.15, 60.0], [4.05, -9.15, 120.0]]
# setos de cayena VEG-09 (v2.1, masa verde del borde): x, z, giro, escala, variante ("r" roja, "m" magenta), con choque
const SETOS := [
	# pie de las fachadas del fondo (sin tapar puertas) y a los lados del podio de la biblioteca
	[-11.75, -9.1, 10.0, 1.05, "m", true], [-6.35, -9.1, 80.0, 1.0, "r", true], [-5.25, -9.15, 200.0, 1.1, "m", true],
	[-3.45, -8.35, 30.0, 0.95, "r", true], [3.45, -8.35, 150.0, 0.95, "r", true], [5.25, -9.15, 260.0, 1.1, "m", true],
	[6.3, -9.1, 20.0, 0.95, "r", true], [9.95, -9.15, 110.0, 1.0, "m", true], [11.15, -9.1, 300.0, 1.05, "r", true],
	# fachadas de la izquierda (lejos de la puerta de casa) y de la derecha (lejos de la boca del camino)
	[-12.6, -6.4, 50.0, 1.0, "r", true], [-12.6, -4.3, 140.0, 1.05, "m", true], [-12.6, -3.3, 230.0, 0.9, "r", true],
	[-12.6, 4.4, 320.0, 1.0, "m", true], [-12.6, 6.7, 70.0, 1.05, "r", true],
	[12.7, -7.7, 90.0, 1.0, "m", true], [12.7, -6.2, 180.0, 1.05, "r", true], [12.7, -4.1, 270.0, 0.95, "m", true],
	[12.7, 4.3, 10.0, 1.0, "r", true], [12.75, 5.8, 100.0, 0.95, "m", true], [12.7, 8.15, 200.0, 1.0, "r", false],
	# junto a la baranda de abajo (la plaza es una terraza): detras de bancas y entre jardineras
	[-12.3, 8.35, 0.0, 1.0, "m", false], [-11.25, 8.4, 90.0, 0.9, "r", false], [-8.6, 8.35, 180.0, 1.0, "m", false],
	[-7.55, 8.4, 270.0, 1.05, "r", false], [-6.45, 8.35, 30.0, 0.95, "m", false], [-4.4, 8.4, 120.0, 1.0, "r", false],
	[-3.3, 8.35, 210.0, 0.9, "m", false], [-2.15, 8.4, 300.0, 1.0, "r", false], [1.2, 8.35, 60.0, 1.0, "m", false],
	[2.3, 8.4, 150.0, 0.95, "r", false], [3.45, 8.35, 240.0, 1.05, "m", false], [4.55, 8.4, 330.0, 0.9, "r", false],
	[5.65, 8.35, 45.0, 1.0, "m", false], [6.7, 8.4, 135.0, 1.05, "r", false], [7.75, 8.35, 225.0, 0.95, "m", false],
	[8.65, 8.4, 315.0, 1.0, "r", false], [11.35, 8.35, 15.0, 1.0, "m", false],
]
# copas del barrio de abajo, mas alla de la baranda: enmarcan el borde inferior del cuadro (sin choque)
const COPAS_ABAJO := [-12.4, -9.9, -7.3, -4.8, -2.2, 0.4, 3.0, 5.6, 8.2, 10.8, 13.3]
const MACETAS := [[-7.4, -9.3, 0.0, "URB-15_a"], [9.3, -9.3, 0.0, "URB-15_b"], [-12.7, -1.4, 90.0, "URB-15_b"],
	[-12.75, 2.5, 90.0, "URB-15_a"], [12.7, -3.1, -90.0, "URB-15_a"], [-2.2, -9.3, 0.0, "URB-15_b"]]
const PALOMAS_CASA :=Vector3(2.9, 0.0, 3.7)     # donde picotea la bandada
const BANDERINES := ["e46043", "daaa25", "3f97a0", "f8c991", "a3b07f", "f4a159"]
# posaderos de las palomas (cornisa y balaustradas de la biblioteca, plato alto de la fuente y faroles)
const POSADEROS := [Vector3(-1.7, 3.5, -8.05), Vector3(-0.7, 3.5, -8.05), Vector3(0.9, 3.5, -8.05), Vector3(2.1, 3.5, -8.05),
	Vector3(-4.4, 3.42, -9.85), Vector3(-3.6, 3.42, -9.85), Vector3(4.6, 3.42, -9.85), Vector3(3.8, 3.42, -9.85),
	Vector3(0.32, 1.67, 0.18), Vector3(-0.3, 1.67, -0.22), Vector3(4.98, 2.24, -3.4), Vector3(-4.98, 2.24, 4.4)]

var radio_minimapa := 12.0        # lo lee el minimapa (interfaz/minimapa.gd)

var _noche := false
var _rec: Array = []              # recursos del layout que se arma por codigo
var _inst: Dictionary = {}
var _iguanas: Array = []          # [{nodo, escala, pos (Vector3), sitios, escondida, calma, ocupada, cabeceo}]
var _iguana_inter: Node3D
var _palomas: Array = []          # [{nodo, alas, estado, t, desde, hasta, ctrl, dur, espera, posadero, residente}]
var _posaderos_libres: Array = []
var _destellos: Array = []
var _salpicadura: CPUParticles3D
var _fuente_usos := 0
var _banca_usos := 0
var _enc_base := 0.0             # encuadre elegido por el jugador (Z y X)
var _enc_puesto := 0.0           # ultimo encuadre que puso la zona
var _t := 0.0


func _construir() -> void:
	encuadre = 0.17
	limites = Rect2(-9.5, -7.6, 19.0, 13.6)      # el foco de la camara: nunca asoma el borde del decorado
	_noche = bool(Juego.bandera("mir_luna"))
	if _noche:
		# noche provisional: azul profundo, para que se lean los charcos calidos de los faroles y el cian
		# Todos los valores van aqui, completos: la noche de la plaza no depende de como quede el preset del nucleo.
		luces("noche", {"sombra_distancia": 30.0, "sol": "8fa9d8", "energia": 0.4, "ambiente_energia": 0.5, "ambiente": "283a6c",
			"fondo": "0c121b", "contraste": 1.10, "saturacion": 0.80, "exposicion": 1.0})
	else:
		luces("tarde", {"sombra_distancia": 30.0})      # la luz aprobada (D-015)
	# pinceladas 2D-HD y sombra moteada bajo el flamboyan (como en el sendero aprobado)
	ambiente(0.7, {"centro": [6.4, -4.3], "radios": [3.6, 2.2], "fuerza": 1.0, "sombra": 0.45})
	if _noche:
		meta["momento"] = "Noche (provisional)"
		Materiales.ajustar_parametro("moteado_fuerza", 0.0)

	_fondo()
	_edificios()
	_mobiliario()
	_vegetacion()
	var r: Dictionary = Constructor.montar(self, {"recursos": _rec}, MODELOS)
	_inst = r["instancias"]
	if not r["faltan"].is_empty():
		push_warning("AVISO faltan modelos de la plaza: %s" % str(r["faltan"]))
	_sin_sombra(["TER-14", "flor_", "_flor_", "VEG-02_petalos", "VEG-14", "VEG-13", "casa_coral", "casa_crema", "TER-11",
		"URB-15", "FAU-01", "casa_prota", "casa_zinc", "casa_verde",      # las casas de la izquierda dan sombra hacia fuera
		"VEG-09_seto", "casa_azul_der", "URB-09"])     # v2.1: setos y piezas del borde, para no bajar de 40 fps
	_agua_turquesa()
	_carteles()
	_guirnaldas()
	_luces_de_la_plaza()
	_colisiones()
	_entradas_y_umbrales()
	_interactuables()
	_vida()


# ------------------------------------------------------------------ armado

func _r(nombre: String, glb: String, x: float, z: float, giro: float = 0.0, extra: Dictionary = {}) -> void:
	# un recurso del layout (mismo formato que layout.json del sendero): los repetidos van en MultiMesh
	var d := {"id": nombre, "glb": glb, "pos": [x, float(extra.get("y", 0.0)), z], "rot_y": giro, "escala": float(extra.get("escala", 1.0))}
	for clave in extra:
		if clave != "y" and clave != "escala":
			d[clave] = extra[clave]
	_rec.append(d)


func _sin_sombra(claves: Array) -> void:
	# rendimiento (HD 620): el suelo, las flores y lo que queda fuera de la plaza no proyectan sombra
	for hijo in get_children():
		var nombre := String(hijo.name)
		var toca := false
		for c in claves:
			if nombre.contains(String(c)):
				toca = true
				break
		if not toca:
			continue
		if hijo is GeometryInstance3D:
			(hijo as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		for malla in hijo.find_children("*", "GeometryInstance3D", true, false):
			(malla as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _fondo() -> void:
	# lo que queda detras de las casas y mas alla del camino: ladera pintada, nunca el vacio
	var m := Piezas.nueva()
	Piezas.plano(m, Vector3(0.0, -0.03, -2.0), Vector2(90.0, 70.0), Color("4f5a34"))
	# manchas de hierba y tierra de la ladera (pintura a mano)
	var manchas := [[-21.0, -12.0, 9.0, 6.0, "6d6a2b"], [20.0, -13.0, 10.0, 7.0, "5c6230"], [22.0, 7.0, 8.0, 9.0, "6d6a2b"],
		[-22.0, 6.0, 8.0, 10.0, "5c6230"], [0.0, -19.0, 16.0, 6.0, "5f6a3a"], [0.0, 14.5, 40.0, 7.0, "5c6230"]]
	for d in manchas:
		var dato: Array = d
		Piezas.plano(m, Vector3(float(dato[0]), -0.02, float(dato[1])), Vector2(float(dato[2]), float(dato[3])), Color(String(dato[4])), 12.0)
	# el camino del cerro sigue en tierra mas alla de la boca
	Piezas.plano(m, Vector3(19.5, -0.01, 1.2), Vector2(9.0, 3.3), Color("af795e"), -4.0)
	Piezas.plano(m, Vector3(20.5, -0.005, 1.25), Vector2(7.0, 1.9), Color("c08a6c"), -4.0)
	pieza(m, "facetado", Vector3.ZERO, 0.0, false)
	_r("TER-14", C + "TER-14.glb", 0.0, 0.0)


func _edificios() -> void:
	# hilera del fondo: la biblioteca en el centro y casas de colores a los lados
	_r("ARQ-13", C + "ARQ-13.glb", 0.0, Z_FACHADA, 0.0, {"suelto": true})
	_r("casa_azul", C + "ARQ-02.glb", -8.3, Z_FACHADA)
	_r("casa_coral", C + "ARQ-02_coral.glb", -14.3, Z_FACHADA)
	_r("casa_rosa", C + "ARQ-01_rosa.glb", 8.1, Z_FACHADA)
	_r("casa_crema", C + "ARQ-02_crema.glb", 13.3, Z_FACHADA)
	# lado izquierdo (las fachadas miran a +X): la casa amarilla es la de la protagonista
	_r("casa_prota", C + "ARQ-01.glb", -13.3, P_CASA.z, 90.0)
	_r("casa_zinc", C + "ARQ-02_zinc.glb", -13.3, -5.2, 90.0)
	_r("casa_verde", C + "ARQ-02_verde.glb", -13.3, 6.2, 90.0)
	# lado derecho (miran a -X), a cada lado de la boca del camino
	_r("casa_azul_der", C + "ARQ-02.glb", 13.3, -4.7, -90.0)
	_r("casa_coral_der", C + "ARQ-02_coral.glb", 13.3, 6.3, -90.0)


func _mobiliario() -> void:
	_r("URB-02", C + "URB-02.glb", 0.0, 0.0, 0.0, {"suelto": true})
	for i in BANCAS.size():
		var b: Array = BANCAS[i]
		_r("URB-01_%d" % i, C + "URB-01.glb", float(b[0]), float(b[1]), float(b[2]))
	for i in JARDINERAS.size():
		var j: Array = JARDINERAS[i]
		_r("URB-07_%d" % i, C + "URB-07.glb", float(j[0]), float(j[1]), float(j[2]))
	for i in FAROLES_DOBLES.size():
		var f: Vector2 = FAROLES_DOBLES[i]
		_r("URB-05_%d" % i, C + "URB-05.glb", f.x, f.y)
	for i in FAROLES.size():
		var f2: Vector2 = FAROLES[i]
		_r("ARQ-09_%d" % i, C + "ARQ-09.glb", f2.x, f2.y)
	_r("URB-03", C + "URB-03.glb", -7.4, -5.3)                      # kiosco de jugos de Lidia (cerrado)
	_r("URB-13", C + "URB-13.glb", P_PUESTO.x, P_PUESTO.z)          # puesto de frutas, a la confianza
	_r("URB-14", C + "URB-14.glb", P_TABLON.x, P_TABLON.z)          # tablon con la convocatoria
	_r("URB-12", C + "URB-12.glb", 7.0, -5.2, 0.0, {"suelto": true})  # puesto de electronica (lleva brillo ya inclinado)
	_r("URB-08", C + "URB-08.glb", -7.6, 4.9, 15.0)                  # estatua de la iguana
	_r("URB-10", C + "URB-10.glb", 0.0, 5.3)                         # poste indicador
	_r("URB-11", C + "URB-11.glb", 11.9, 5.0, -90.0)                 # bicicletero
	_r("URB-06_0", C + "URB-06.glb", -5.5, -5.9)
	_r("URB-06_1", C + "URB-06.glb", 9.1, -4.3)
	_r("URB-06_2", C + "URB-06.glb", -9.2, 7.5)
	_r("ARQ-08_0", C + "ARQ-08.glb", -12.1, -8.3)
	_r("ARQ-08_1", C + "ARQ-08.glb", 12.2, 8.0)
	_r("ARQ-10_0", C + "ARQ-10.glb", -10.6, -8.75)                   # tendederos entre las casas
	_r("ARQ-10_1", C + "ARQ-10.glb", 14.7, -1.25, 8.0)
	_r("ARQ-10_2", C + "ARQ-10.glb", 10.7, -9.0, 0.0)
	for i in MACETAS.size():
		var mc: Array = MACETAS[i]
		_r("URB-15_%d" % i, C + "URB-15.glb", float(mc[0]), float(mc[1]), float(mc[2]), {"nodo": String(mc[3])})
	# baranda del borde de abajo: la plaza es una terraza sobre el barrio
	for i in 8:
		_r("URB-09_%d" % i, E + "URB-09.glb", -10.71 + 3.06 * i, 8.6)
	# iguanas al sol (FAU-01): de noche no estan
	for i in (0 if _noche else IGUANAS.size()):
		var g: Array = IGUANAS[i]
		_r("FAU-01_%d" % i, "personajes/FAU-01.glb", float(g[0]), float(g[1]), float(g[2]), {"y": float(g[3]), "altura": 0.34, "suelto": true})


func _vegetacion() -> void:
	# flamboyan del sendero aprobado, en la esquina del fondo a la derecha: da sombra al puesto
	_r("VEG-02", E + "VEG-02.glb", 9.3, -6.9, 180.0, {"escala": 0.95, "escala_y": 0.84, "suelto": true})
	_r("VEG-02_petalos", E + "VEG-02_petalos.glb", 8.2, -5.0, 180.0, {"escala": 0.7, "y": 0.012})
	# cocoteros VEG-04 en las esquinas: uno da sombra al puesto de frutas; dos flanquean la biblioteca
	for i in PALMAS.size():
		var p: Array = PALMAS[i]
		_r("VEG-04_%d" % i, C + "VEG-04.glb", float(p[0]), float(p[1]), float(p[2]), {"escala": 1.0 - 0.06 * (i % 4)})
	# setos de cayena VEG-09 (un MultiMesh por variante, sin sombra): la masa verde que enmarca la plaza
	for i in SETOS.size():
		var s0: Array = SETOS[i]
		var variante: String = "VEG-09_seto_roja" if String(s0[4]) == "r" else "VEG-09_seto_magenta"
		_r("VEG-09_seto_%d" % i, C + "VEG-09_seto.glb", float(s0[0]), float(s0[1]), float(s0[2]), {"escala": float(s0[3]), "nodo": variante})
	for i in COPAS_ABAJO.size():
		var x: float = COPAS_ABAJO[i]
		var variante2: String = "VEG-09_seto_roja" if i % 3 == 0 else "VEG-09_seto_magenta"
		_r("VEG-09_seto_bajo_%d" % i, C + "VEG-09_seto.glb", x, 9.35 + 0.25 * float(i % 2), 37.0 * i,
			{"escala": 1.55 + 0.15 * float(i % 3), "y": -0.25, "nodo": variante2})
	# buganvillas en cascada (VEG-08 del Mirador) colgando de los balcones y los muros
	for d in [[-13.25, -1.7, 90.0, 2.3], [-13.25, 7.6, 90.0, 2.2], [10.0, -9.8, 0.0, 2.25], [-6.0, -9.8, 0.0, 2.35], [13.25, 4.6, -90.0, 2.2]]:
		var b: Array = d
		_r("VEG-08_%d_%d" % [int(b[0]), int(b[1])], "mirador/VEG-08.glb", float(b[0]), float(b[1]), float(b[2]), {"y": float(b[3]), "escala": 0.9})
	# boca del camino del cerro: rocas, plantas y el arranque de la escalinata de mosaico
	_r("TER-11", E + "TER-11.glb", 16.6, 1.2, -90.0)
	var sueltas := [
		["TER-01_a", 14.0, -1.2, 20.0, 0.9], ["TER-02_a", 13.4, -0.75, 140.0, 1.0], ["TER-01_b", 14.3, 3.5, 250.0, 0.85],
		["TER-02_b", 13.35, 3.05, 40.0, 1.0], ["VEG-10", 14.9, -0.8, 0.0, 1.0], ["VEG-07", 13.6, -1.75, 30.0, 1.0],
		["VEG-12", 15.1, 3.1, 0.0, 1.0], ["VEG-07", 13.7, 3.75, 200.0, 1.0], ["VEG-10", 15.6, -1.6, 90.0, 1.1],
		["VEG-12", 12.3, -8.4, 0.0, 1.0], ["VEG-10", 11.9, -7.3, 60.0, 1.0], ["VEG-07", -12.3, -8.9, 0.0, 1.0],
		["VEG-10", -12.35, 3.45, 0.0, 0.9], ["VEG-07", -12.4, -2.45, 120.0, 0.9], ["VEG-12", -12.3, 8.0, 0.0, 0.9],
		["VEG-12", 12.5, 8.6, 0.0, 0.9], ["VEG-10", 12.45, -1.6, 200.0, 0.9],
	]
	for i in sueltas.size():
		var s: Array = sueltas[i]
		_r("%s_c%d" % [String(s[0]), i], E + String(s[0]) + ".glb", float(s[1]), float(s[2]), float(s[3]), {"escala": float(s[4])})
	# las jardineras URB-07 traen la tierra lista: encima van las plantas de la hoja HR_VEG
	var colores := ["VEG-14_rosa", "VEG-14_amarilla", "VEG-14_blanca"]
	for i in JARDINERAS.size():
		var jar: Array = JARDINERAS[i]
		var jx: float = jar[0]
		var jz: float = jar[1]
		var mata: String = "VEG-10" if i % 2 == 0 else "VEG-07"
		_r("jar_%d_mata" % i, E + mata + ".glb", jx, jz - 0.05, 40.0 * i, {"y": 0.39, "escala": 0.78})
		_r("jar_%d_flor_a" % i, E + "VEG-14.glb", jx - 0.47, jz + 0.13, 25.0 * i, {"y": 0.4, "escala": 1.25, "nodo": String(colores[i % 3])})
		_r("jar_%d_flor_b" % i, E + "VEG-14.glb", jx + 0.47, jz + 0.1, 70.0 * i, {"y": 0.4, "escala": 1.25, "nodo": String(colores[(i + 1) % 3])})
	# flores al pie del flamboyan y en la boca del camino
	var flores := [["VEG-14", "VEG-14_rosa", 10.4, -5.6], ["VEG-14", "VEG-14_amarilla", 11.6, -5.9], ["VEG-14", "VEG-14_blanca", 10.0, -7.4],
		["VEG-13", "VEG-13_g", 11.9, -6.9], ["VEG-13", "VEG-13_m", 10.2, -6.0], ["VEG-14", "VEG-14_amarilla", 13.9, 2.95],
		["VEG-14", "VEG-14_rosa", 14.8, -0.3], ["VEG-13", "VEG-13_g", 15.4, 2.8], ["VEG-14", "VEG-14_blanca", 14.4, 3.0]]
	for i in flores.size():
		var fl: Array = flores[i]
		_r("flor_%d" % i, E + String(fl[0]) + ".glb", float(fl[2]), float(fl[3]), 37.0 * i, {"nodo": String(fl[1])})


func _agua_turquesa() -> void:
	# la fuente de la plaza lleva el agua mas clara y turquesa que el arroyo (solo su material, no el comun)
	var fuente: Node3D = _inst.get("URB-02")
	if fuente == null:
		return
	for nodo in fuente.find_children("*", "MeshInstance3D", true, false):
		var mi := nodo as MeshInstance3D
		for s in mi.mesh.get_surface_count():
			var mat := mi.get_surface_override_material(s) as ShaderMaterial
			if mat != null and mat.shader != null and mat.shader.resource_path.ends_with("agua.gdshader"):
				mat.set_shader_parameter("agua_honda", Color("2f8f98"))
				mat.set_shader_parameter("agua_clara", Color("72cdc4"))


func _carteles() -> void:
	# carteles dibujados, sin letras (el texto lo pone la interfaz)
	var m := Piezas.nueva()
	# kiosco cerrado: tablilla crema con una banda coral cruzada
	var k := Vector3(-6.1, 0.0, -3.95)
	Piezas.caja(m, k + Vector3(0.0, 0.42, 0.0), Vector3(0.05, 0.84, 0.05), Color("583f22"))
	Piezas.caja(m, k + Vector3(0.0, 0.92, 0.02), Vector3(0.56, 0.4, 0.04), Color("f8c991"))
	Piezas.cara(m, [k + Vector3(-0.26, 0.76, 0.045), k + Vector3(-0.18, 0.76, 0.045), k + Vector3(0.26, 1.08, 0.045), k + Vector3(0.18, 1.08, 0.045)], Color("e46043"))
	# puesto de electronica: «Vuelvo enseguida», un reloj dibujado
	var p := Vector3(8.5, 0.0, -4.05)
	Piezas.caja(m, p + Vector3(0.0, 0.42, 0.0), Vector3(0.05, 0.84, 0.05), Color("583f22"))
	Piezas.caja(m, p + Vector3(0.0, 0.92, 0.02), Vector3(0.5, 0.44, 0.04), Color("f8c991"))
	var esfera: Array = []
	for i in 8:
		var a := TAU * (i + 0.5) / 8.0
		esfera.append(p + Vector3(cos(a) * 0.15, 0.92 + sin(a) * 0.15, 0.045))
	Piezas.cara(m, esfera, Color("516b7c"))
	Piezas.cara(m, [p + Vector3(-0.012, 0.92, 0.05), p + Vector3(0.012, 0.92, 0.05), p + Vector3(0.012, 1.03, 0.05), p + Vector3(-0.012, 1.03, 0.05)], Color("f8c991"))
	Piezas.cara(m, [p + Vector3(0.0, 0.908, 0.05), p + Vector3(0.08, 0.908, 0.05), p + Vector3(0.08, 0.932, 0.05), p + Vector3(0.0, 0.932, 0.05)], Color("f8c991"))
	pieza(m)
	columna(k, 0.2, 1.2)
	columna(p, 0.2, 1.2)
	# la luz de los libros se derrama por el podio de la biblioteca: abanico cian palido delante de la puerta
	var luz := Piezas.nueva()
	var zp := -9.22
	Piezas.cara(luz, [Vector3(-0.2, 0.428, zp), Vector3(0.2, 0.428, zp), Vector3(1.0, 0.428, -7.87), Vector3(-1.0, 0.428, -7.87)], Color("a4dcd2"))
	Piezas.cara(luz, [Vector3(-0.14, 0.432, zp), Vector3(0.14, 0.432, zp), Vector3(0.5, 0.432, -8.25), Vector3(-0.5, 0.432, -8.25)], Color("86e2da"))
	# ...y baja por las dos gradas, cada vez mas tenue
	Piezas.cara(luz, [Vector3(-1.0, 0.288, -7.84), Vector3(1.0, 0.288, -7.84), Vector3(1.12, 0.288, -7.61), Vector3(-1.12, 0.288, -7.61)], Color("b4dccf"))
	Piezas.cara(luz, [Vector3(-1.12, 0.148, -7.59), Vector3(1.12, 0.148, -7.59), Vector3(1.38, 0.148, -7.12), Vector3(-1.38, 0.148, -7.12)], Color("c4dccb"))
	pieza(luz, "facetado", Vector3.ZERO, 0.0, false)


func _guirnaldas() -> void:
	# guirnaldas de banderines entre fachadas y faroles: material de follaje, asi el viento las mueve.
	# De noche llevan bombillas calidas (Biblia de arte, seccion 7).
	var m := Piezas.nueva()
	var focos: Array = []
	var tramos := [
		[Vector3(-12.95, 3.0, -4.1), Vector3(-5.4, 2.3, -3.4), 0.55],
		[Vector3(5.4, 2.3, -3.4), Vector3(12.95, 3.0, -2.6), 0.55],
		[Vector3(-12.95, 2.9, 4.7), Vector3(-5.4, 2.3, 4.4), 0.5],
		[Vector3(5.4, 2.3, 4.4), Vector3(12.95, 2.9, 3.9), 0.5],
		[Vector3(-10.9, 3.3, -9.75), Vector3(-5.5, 3.2, -9.75), 0.45],
		[Vector3(5.5, 3.2, -9.75), Vector3(10.4, 4.3, -9.75), 0.45],
	]
	for i in tramos.size():
		var t: Array = tramos[i]
		_guirnalda(m, t[0], t[1], float(t[2]), i, focos)
	pieza(m, "follaje", Vector3.ZERO, 0.0, false)
	if _noche and not focos.is_empty():
		var b := Piezas.nueva()
		for f in focos:
			var c: Vector3 = f
			c.z -= cizalla * c.y      # el emisivo no pasa por los shaders: se inclina aqui
			Piezas.cara(b, [c + Vector3(-0.045, 0.0, 0.0), c + Vector3(0.0, -0.06, 0.0), c + Vector3(0.045, 0.0, 0.0), c + Vector3(0.0, 0.05, 0.0)], Color("ffd9a0"))
		var nodo := Piezas.nodo(b, "emisivo", false)
		var mat := Materiales.emisivo(Color("ffd9a0"), 2.2)
		mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		nodo.material_override = mat
		add_child(nodo)


func _guirnalda(m: Dictionary, a: Vector3, b: Vector3, comba: float, semilla: int, focos: Array) -> void:
	var largo := a.distance_to(b)
	var n := maxi(4, int(largo / 0.34))
	var lado := Vector3(0.0, 0.0, 1.0)
	var curva := func(t: float) -> Vector3:
		return a.lerp(b, t) - Vector3(0.0, comba * 4.0 * t * (1.0 - t), 0.0)
	for i in n:
		var t0 := float(i) / float(n)
		var t1 := float(i + 1) / float(n)
		var p0: Vector3 = curva.call(t0)
		var p1: Vector3 = curva.call(t1)
		# cordel
		Piezas.cara(m, [p0, p1, p1 + Vector3(0.0, 0.018, 0.0), p0 + Vector3(0.0, 0.018, 0.0)], Color("583f22"))
		# banderin triangular que cuelga
		var q0: Vector3 = curva.call(t0 + 0.12 / float(n))
		var q1: Vector3 = curva.call(t0 + 0.82 / float(n))
		var punta := (q0 + q1) * 0.5 - Vector3(0.0, 0.27, 0.0) + lado * 0.01
		var color := Color(String(BANDERINES[(i + semilla * 2) % BANDERINES.size()]))
		Piezas.cara(m, [q0, punta, q1], color)
		if i % 2 == 0:
			focos.append(p0 - Vector3(0.0, 0.05, 0.0))


func _luces_de_la_plaza() -> void:
	# De dia la luz cian de la puerta va pintada en el podio y las gradas (_carteles).
	# Noche PROVISIONAL sin luces reales: siete OmniLight bajaban la plaza a 27 fps en la HD 620 y quemaban el
	# adoquin claro. Van el brillo en los vidrios de los faroles, charcos de luz sumados sobre el suelo y
	# ventanas calidas en las casas.
	# v2.1: la puerta de ARQ-13 queda entreabierta (58 cm) y la luz cian se derrama por el podio y las gradas
	# tambien de tarde (mas tenue que de noche): es el gancho hacia los libros de la base.
	var f_dia := 1.0 if _noche else 0.55
	_abanico(Vector3(0.0, 0.437, -9.2), 0.62, Vector3(0.0, 0.437, -7.9), 2.1, Color("62e4e0"), 0.62 * f_dia)
	_abanico(Vector3(0.0, 0.298, -7.86), 2.1, Vector3(0.0, 0.298, -7.6), 2.25, Color("36b1b2"), 0.42 * f_dia)
	_abanico(Vector3(0.0, 0.158, -7.6), 2.25, Vector3(0.0, 0.158, -7.1), 2.5, Color("36b1b2"), 0.3 * f_dia)
	_charco(Vector3(0.0, 0.03, -6.4), 2.4, Color("36b1b2"), 0.4 * f_dia)
	if not _noche:
		return
	var calido := Materiales.emisivo(Color("ffd9a0"), 1.8)
	var vidrio := SphereMesh.new()
	vidrio.radius = 0.1
	vidrio.height = 0.22
	vidrio.radial_segments = 6
	vidrio.rings = 3
	for f in FAROLES_DOBLES:
		var p: Vector2 = f
		_brillo(vidrio, calido, Vector3(p.x - 0.42, 2.06, p.y))
		_brillo(vidrio, calido, Vector3(p.x + 0.42, 2.06, p.y))
		# v2.1: charcos con borde (alcance -20 %, mas vivos) y suelo azul entre ellos
		_charco(Vector3(p.x, 0.02, p.y + 0.35), 3.2, Color("f4a159"), 1.3)
	for f in FAROLES:
		var p2: Vector2 = f
		_brillo(vidrio, calido, Vector3(p2.x, 2.0, p2.y))
		_charco(Vector3(p2.x, 0.02, p2.y + 0.3), 2.6, Color("f4a159"), 1.15)
	# la luz de los libros, mas viva de noche
	_charco(Vector3(0.0, 0.445, -8.55), 1.1, Color("62e4e0"), 0.7)
	# ventanas encendidas: [x, z, giro de la casa, x local de la ventana, y0, alto, ancho]
	var v := Piezas.nueva()
	var ventanas := [[-8.3, Z_FACHADA, 0.0, 1.3, 0.95, 0.92, 0.72], [8.1, Z_FACHADA, 0.0, 0.9, 0.95, 0.92, 0.72],
		[8.1, Z_FACHADA, 0.0, 1.35, 2.8, 0.86, 0.6], [-13.3, P_CASA.z, 90.0, -1.6, 0.95, 0.92, 0.72],
		[-13.3, P_CASA.z, 90.0, 1.55, 2.8, 0.86, 0.6], [-13.3, 6.2, 90.0, -0.2, 0.95, 0.92, 0.72],
		[13.3, 6.3, -90.0, 1.95, 0.95, 0.92, 0.72], [13.3, -4.7, -90.0, -1.8, 0.95, 0.92, 0.72]]
	for d in ventanas:
		var w: Array = d
		var base := Basis(Vector3.UP, deg_to_rad(float(w[2])))
		var o := Vector3(float(w[0]), 0.0, float(w[1]))
		var lx: float = w[3]
		var y0: float = w[4]
		var h: float = w[5]
		var an: float = w[6]
		var pts: Array = []
		for esq in [Vector2(-0.5, 0.0), Vector2(0.5, 0.0), Vector2(0.5, 1.0), Vector2(-0.5, 1.0)]:
			var e: Vector2 = esq
			var q := o + base * Vector3(lx + e.x * an, y0 + e.y * h, 0.03)
			q.z -= cizalla * q.y
			pts.append(q)
		Piezas.cara(v, pts, Color("ffc98a"))
		_charco(o + base * Vector3(lx, 0.02, 0.9), 1.4, Color("f4a159"), 0.7)
	var nodo := Piezas.nodo(v, "emisivo", false)
	var mat := Materiales.emisivo(Color("ffc98a"), 1.3)
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	nodo.material_override = mat
	add_child(nodo)


func _brillo(malla: Mesh, material: Material, pos: Vector3) -> void:
	# el material emisivo no pasa por los shaders del proyecto: se coloca ya inclinado (z -= cizalla * y)
	var mi := MeshInstance3D.new()
	mi.mesh = malla
	mi.material_override = material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	mi.position = Vector3(pos.x, pos.y, pos.z - cizalla * pos.y)


func _charco(centro: Vector3, radio: float, color: Color, fuerza: float) -> void:
	# charco de luz pintado: disco que se suma al suelo, vivo en el centro y apagado en el borde
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var vivo := Color(color.r * fuerza, color.g * fuerza, color.b * fuerza, 1.0)
	var medio := Color(vivo.r * 0.4, vivo.g * 0.4, vivo.b * 0.4, 1.0)
	var negro := Color(0.0, 0.0, 0.0, 1.0)
	var lados := 20
	for i in lados:
		var a0 := TAU * float(i) / float(lados)
		var a1 := TAU * float(i + 1) / float(lados)
		var d0 := Vector3(cos(a0), 0.0, sin(a0))
		var d1 := Vector3(cos(a1), 0.0, sin(a1))
		var puntos := [[Vector3.ZERO, vivo], [d1 * radio * 0.5, medio], [d0 * radio * 0.5, medio],
			[d0 * radio * 0.5, medio], [d1 * radio * 0.5, medio], [d1 * radio, negro],
			[d0 * radio * 0.5, medio], [d1 * radio, negro], [d0 * radio, negro]]
		for par in puntos:
			var dato: Array = par
			st.set_color(dato[1])
			st.add_vertex(dato[0])
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.vertex_color_use_as_albedo = true
	material.vertex_color_is_srgb = true      # el color pintado es sRGB: sin esto el charco sale casi blanco
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	mi.position = Vector3(centro.x, centro.y, centro.z - cizalla * centro.y)


func _abanico(a: Vector3, ancho_a: float, b: Vector3, ancho_b: float, color: Color, fuerza: float) -> void:
	# haz de luz pintado sobre el suelo (trapecio que se suma): vivo junto a la puerta (a) y apagado al llegar a b
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var vivo := Color(color.r * fuerza, color.g * fuerza, color.b * fuerza, 1.0)
	var medio := Color(vivo.r * 0.45, vivo.g * 0.45, vivo.b * 0.45, 1.0)
	var negro := Color(0.0, 0.0, 0.0, 1.0)
	var filas := [[a, ancho_a, vivo], [a.lerp(b, 0.5), lerpf(ancho_a, ancho_b, 0.5), medio], [b, ancho_b, negro]]
	for k in 2:
		var f0: Array = filas[k]
		var f1: Array = filas[k + 1]
		var c0: Vector3 = f0[0]
		var c1: Vector3 = f1[0]
		var w0: float = f0[1]
		var w1: float = f1[1]
		# en cada fila el borde lateral se apaga: centro vivo, lados negros (tres tiras)
		var xs := [-0.5, -0.22, 0.22, 0.5]
		for t in 3:
			var col0: Color = f0[2]
			var col1: Color = f1[2]
			var izq0: Color = negro if t == 0 else col0
			var izq1: Color = negro if t == 0 else col1
			var der0: Color = negro if t == 2 else col0
			var der1: Color = negro if t == 2 else col1
			var p00 := c0 + Vector3(float(xs[t]) * w0, 0.0, 0.0)
			var p01 := c0 + Vector3(float(xs[t + 1]) * w0, 0.0, 0.0)
			var p10 := c1 + Vector3(float(xs[t]) * w1, 0.0, 0.0)
			var p11 := c1 + Vector3(float(xs[t + 1]) * w1, 0.0, 0.0)
			for par in [[p00, izq0], [p01, der0], [p11, der1], [p00, izq0], [p11, der1], [p10, izq1]]:
				var dato: Array = par
				var q: Vector3 = dato[0]
				q.z -= cizalla * q.y        # el material sin sombreado no pasa por los shaders: se inclina aqui
				st.set_color(dato[1])
				st.add_vertex(q)
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.vertex_color_use_as_albedo = true
	material.vertex_color_is_srgb = true
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)


# ------------------------------------------------------------------ colisiones

func _colisiones() -> void:
	piso(Vector3.ZERO, Vector2(40.0, 30.0))
	# nadie se sale de la plaza: fachadas de la izquierda y del fondo, y la baranda de abajo
	cerco(Rect2(-12.95, -9.35, 27.35, 17.55))
	# lado derecho: fachadas a cada lado de la boca del camino
	pared(Vector3(13.95, 1.5, -5.25), Vector3(2.0, 3.0, 8.6))
	pared(Vector3(13.95, 1.5, 5.85), Vector3(2.0, 3.0, 5.0))
	# biblioteca: podio (se pisa), gradas con rampa, zancas, columnas y muro del cuerpo central
	pared(Vector3(0.0, 0.21, -8.85), Vector3(6.3, 0.42, 2.0))
	rampa(Vector3(0.0, 0.0, -7.04), Vector3(0.0, 0.42, -7.86), 5.2)
	pared(Vector3(0.0, 1.5, -9.6), Vector3(5.8, 3.0, 0.7))
	for lado in [-1.0, 1.0]:
		var sx: float = lado
		pared(Vector3(sx * 2.875, 0.5, -7.45), Vector3(0.55, 1.0, 0.8))
		columna(Vector3(sx * 1.33, 0.42, -8.3), 0.2, 2.6)
		columna(Vector3(sx * 2.62, 0.42, -8.3), 0.2, 2.6)
	# mobiliario
	columna(Vector3.ZERO, 1.62, 1.4)
	for b in BANCAS:
		var banca: Array = b
		pared(Vector3(float(banca[0]), 0.35, float(banca[1])), Vector3(1.32, 0.7, 0.5), float(banca[2]))
	for j in JARDINERAS:
		var jar: Array = j
		pared(Vector3(float(jar[0]), 0.3, float(jar[1])), Vector3(1.68, 0.6, 0.98), float(jar[2]))
	for f in FAROLES_DOBLES:
		var p: Vector2 = f
		columna(Vector3(p.x, 0.0, p.y), 0.15, 2.2)
	for f in FAROLES:
		var p2: Vector2 = f
		columna(Vector3(p2.x, 0.0, p2.y), 0.14, 2.0)
	pared(Vector3(-7.48, 1.0, -5.14), Vector3(2.66, 2.0, 1.9))        # kiosco
	pared(Vector3(7.04, 1.0, -5.17), Vector3(2.42, 2.0, 1.45))        # puesto de electronica
	pared(P_PUESTO + Vector3(-0.02, 0.5, -0.02), Vector3(2.1, 1.0, 0.98))   # puesto de frutas
	pared(P_TABLON + Vector3(0.0, 1.0, 0.0), Vector3(1.85, 2.0, 0.3))      # tablon
	columna(Vector3(-7.6, 0.0, 4.9), 0.62, 1.5)                        # estatua
	columna(Vector3(0.0, 0.0, 5.3), 0.16, 1.8)                         # poste indicador
	pared(Vector3(11.8, 0.4, 5.0), Vector3(1.15, 0.8, 1.5))            # bicicletero
	columna(Vector3(-5.5, 0.0, -5.9), 0.26, 0.9)
	columna(Vector3(9.1, 0.0, -4.3), 0.26, 0.9)
	columna(Vector3(-9.2, 0.0, 7.5), 0.26, 0.9)
	columna(Vector3(-12.1, 0.0, -8.3), 0.14, 2.0)
	columna(Vector3(12.2, 0.0, 8.0), 0.14, 2.0)
	pared(Vector3(-10.5, 0.8, -8.72), Vector3(3.1, 1.6, 0.16))         # tendedero
	columna(Vector3(11.05, 0.0, -6.55), 0.5, 2.0)                      # tronco del flamboyan
	columna(Vector3(14.0, 0.0, -1.2), 0.6, 1.2)                        # rocas de la boca del camino
	columna(Vector3(14.3, 0.0, 3.5), 0.5, 1.2)
	for d in PALMAS:
		var pal: Array = d
		columna(Vector3(float(pal[0]), 0.0, float(pal[1])), 0.22, 2.0)
	for d in SETOS:
		var seto: Array = d
		if bool(seto[5]):
			columna(Vector3(float(seto[0]), 0.0, float(seto[1])), 0.36 * float(seto[3]), 0.9)
	for d in MACETAS:
		var mc: Array = d
		columna(Vector3(float(mc[0]), 0.0, float(mc[1])), 0.38, 0.8)


# ------------------------------------------------------------------ entradas, umbrales e interactuables

func _entradas_y_umbrales() -> void:
	var casa := P_CASA + Vector3(1.45, 0.0, 0.0)
	entrada("inicio", casa, Vector3(1, 0, 0))
	entrada("casa", casa, Vector3(1, 0, 0))
	entrada("sendero", P_SENDERO - Vector3(1.6, 0.0, 0.0), Vector3(-1, 0, 0))
	entrada("biblioteca", Vector3(0.0, 0.0, -6.3), Vector3(0, 0, 1))
	umbral("ACasa", P_CASA, "habitacion", "escalera", "A casa")
	umbral("AlSendero", P_SENDERO, "sendero", "casa", "Al sendero del arroyo")


func _interactuables() -> void:
	interactuable("Biblioteca", P_BIBLIO, "Entrar a la biblioteca", _usar_biblioteca, {"radio": 1.4, "altura_marca": 1.35})
	interactuable("Fuente", Vector3.ZERO, "Tocar el agua", _usar_fuente, {"radio": 2.45, "altura_marca": 2.3})
	interactuable("Kiosco", Vector3(-7.3, 0.0, -4.5), "Mirar el kiosco", _usar_kiosco, {"radio": 1.6, "altura_marca": 2.0})
	interactuable("PuestoElectronica", Vector3(7.0, 0.0, -4.6), "Mirar el puesto", _usar_puesto, {"radio": 1.6, "altura_marca": 1.9})
	interactuable("EstatuaIguana", Vector3(-7.6, 0.0, 4.9), "Mirar la estatua", _usar_estatua, {"radio": 1.6, "altura_marca": 1.75})
	interactuable("PosteIndicador", Vector3(0.0, 0.0, 5.3), "Leer el poste", _usar_poste, {"radio": 1.3, "altura_marca": 2.05})
	interactuable("Banca", Vector3(5.1, 0.0, -1.4), "Sentarse a mirar", _usar_banca, {"radio": 1.35, "altura_marca": 1.05})
	interactuable("PuestoFrutas", P_PUESTO + Vector3(0.0, 0.0, 0.95), "Mirar la fruta", _usar_frutas, {"radio": 1.3, "altura_marca": 2.35})
	interactuable("Tablon", P_TABLON + Vector3(0.0, 0.0, 0.75), "Leer el tablón", _usar_tablon, {"radio": 1.2, "altura_marca": 2.3})
	interactuable("MosaicoLunas", Vector3(-3.54, 0.0, 0.0), "Mirar las lunas del suelo", _usar_mosaico, {"radio": 1.0, "altura_marca": 0.6})
	# la iguana que se deja observar (las otras solo toman el sol)
	if not _noche and _inst.has("FAU-01_0"):
		var g: Array = IGUANAS[0]
		_iguana_inter = interactuable("Iguana", Vector3(float(g[0]), 0.0, float(g[1])), "Observar la iguana", _usar_iguana, {"radio": 1.75, "altura_marca": 0.8})
	# recolectables de la familia COL (hoja HR_COL_v1), con su destello FX-01
	_col("ColPlaca", "COL-03", Vector3(8.35, 0.0, -3.9), 30.0, "placa_de_circuito", "Recoger la placa de circuito")
	_col("ColCable", "COL-06", Vector3(11.0, 0.0, 7.3), -20.0, "cable_de_cobre", "Recoger el cable de cobre")
	_col("ColCarta", "COL-12", Vector3(-6.55, 0.0, 6.7), 15.0, "carta_estelar", "Recoger la carta estelar")


func _col(nombre: String, id_col: String, pos: Vector3, giro: float, id_objeto: String, texto: String) -> void:
	var visual := Node3D.new()
	visual.name = nombre + "_visual"
	add_child(visual)
	var pieza_col := Recursos.instancia("%s/%s%s.glb" % [MODELOS, C, id_col])
	if pieza_col != null:
		visual.add_child(pieza_col)
		pieza_col.position = pos
		pieza_col.rotation.y = deg_to_rad(giro)
		for mi in pieza_col.find_children("*", "GeometryInstance3D", true, false):
			(mi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var destello := Recursos.instancia(MODELOS + "/entorno/FX-01.glb")
	if destello != null:
		visual.add_child(destello)
		destello.position = Vector3(pos.x, 0.42, pos.z - cizalla * 0.42)
		destello.scale = Vector3.ONE * 0.8
		_destellos.append(destello)
	recolectable(nombre, pos, id_objeto, visual, texto)


func _usar_biblioteca() -> void:
	if not Juego.bandera("base_visitada"):
		await Interfaz.decir([
			"La puerta está entreabierta. De la sala de lectura sale una luz cian.",
			"Dentro hay dos libros abiertos. Sobre sus páginas flota una maqueta de luz: «Tu primera base espacial».",
			{"quien": "Órbita", "texto": "Un libro muestra la Luna y el otro, Marte. Acércate."},
		])
		Juego.poner_bandera("base_visitada")
	var i: int = await Interfaz.elegir("¿Qué libro abres?", ["Base en la Luna", "Base en Marte", "Ahora no"])
	if i < 0 or i > 1:
		return
	var reto: String = "base_luna" if i == 0 else "base_marte"
	# Marte despues de la Luna: alla se construye el cohete. Solo cuando el libro de la Luna ya esta hecho.
	if reto == "base_marte" and FileAccess.file_exists("res://minijuegos/base_luna/base_luna.gd") and not Juego.bandera("base_luna_hecha"):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Primero la Luna: allá se construye el cohete que nos lleva a Marte."}])
		return
	var r: Dictionary = await Interfaz.abrir_minijuego(reto)
	if r.get("superado", false) and not r.get("en_construccion", false):
		Juego.poner_bandera(reto + "_hecha")
		Audio.sonar("logro")


func _usar_fuente() -> void:
	_fuente_usos += 1
	_salpicar()
	if _fuente_usos == 1:
		Juego.anotar("chimborazo")
		await Interfaz.decir([
			"Metes la mano en el agua y salpica. Sube, se abre y vuelve a caer: todo cae hacia el centro de la Tierra.",
			{"quien": "Órbita", "texto": "La cumbre del Chimborazo es el punto más alejado de ese centro: 6 384 418,505 m."},
		])
		return
	var frases := ["Órbita da un salto atrás. No le gusta mojarse.", "Las gotas brillan al sol antes de caer.",
		"Órbita te mira muy seria desde lejos.", "Una paloma se acerca a beber al borde."]
	Interfaz.aviso(String(frases[(_fuente_usos - 2) % frases.size()]), 2.5)


func _salpicar() -> void:
	# gotas de agua turquesa (shader agua: se inclinan como todo lo demas) del lado de la protagonista
	Audio.sonar("pagina", -1.0)
	Audio.sonar("tic", -6.0)
	var j: CharacterBody3D = Zonas.jugador
	var dir := Vector3(0.0, 0.0, 1.0)
	if j != null and is_instance_valid(j):
		var d := Vector3(j.global_position.x, 0.0, j.global_position.z)
		if d.length() > 0.1:
			dir = d.normalized()
	if _salpicadura == null:
		_salpicadura = CPUParticles3D.new()
		var gota := SphereMesh.new()
		gota.radius = 0.045
		gota.height = 0.09
		gota.radial_segments = 6
		gota.rings = 3
		_salpicadura.mesh = gota
		_salpicadura.material_override = Materiales.compartido("agua")
		_salpicadura.amount = 36
		_salpicadura.lifetime = 0.9
		_salpicadura.one_shot = true
		_salpicadura.explosiveness = 0.85
		_salpicadura.direction = Vector3(0.0, 1.0, 0.0)
		_salpicadura.spread = 38.0
		_salpicadura.initial_velocity_min = 2.0
		_salpicadura.initial_velocity_max = 3.6
		_salpicadura.gravity = Vector3(0.0, -9.8, 0.0)
		_salpicadura.scale_amount_min = 0.6
		_salpicadura.scale_amount_max = 1.3
		_salpicadura.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
		_salpicadura.emission_sphere_radius = 0.25
		_salpicadura.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		add_child(_salpicadura)
	_salpicadura.position = dir * 1.25 + Vector3(0.0, 0.46, 0.0)
	_salpicadura.restart()
	# Orbita se aparta del agua (es un gato)
	var gato: Node3D = Zonas.companero
	if gato != null and is_instance_valid(gato) and gato.has_method("colocar_junto"):
		var lejos := Vector3(gato.global_position.x, 0.0, gato.global_position.z)
		if lejos.length() < 3.2 and lejos.length() > 0.1:
			var a := create_tween()
			a.tween_property(gato, "global_position", lejos.normalized() * 3.4 + Vector3(0.0, gato.global_position.y, 0.0), 0.25)


func _usar_kiosco() -> void:
	await Interfaz.decir([
		"El kiosco de jugos de Lidia está cerrado. En el cartel hay una banda roja pintada a mano.",
		{"quien": "Órbita", "texto": "Huele a naranja y a piña. Hoy dejó la fruta en el puesto de al lado, a la confianza."},
	])


func _usar_puesto() -> void:
	Juego.anotar("cubesat")
	await Interfaz.decir([
		"No hay nadie. Un cartel con un reloj dibujado dice: «Vuelvo enseguida».",
		"Sobre la mesa, un osciloscopio dibuja una onda cian.",
		{"quien": "Órbita", "texto": "El cuerpo de Pegaso, el primer satélite ecuatoriano, era un cubo de 10 cm. Cabría en esta mesa."},
	])


func _usar_estatua() -> void:
	await Interfaz.decir([
		"Una iguana de piedra toma el sol en su pedestal. A sus pies, otra de mosaico. La plaza lleva su nombre.",
		{"quien": "Órbita", "texto": "Las de verdad andan cerca. Regla del barrio: mirar sin espantar."},
	])


func _usar_poste() -> void:
	await Interfaz.decir([
		"Izquierda: a casa. Al fondo: Biblioteca municipal. Derecha: sendero del arroyo y Mirador del Faro.",
	])


func _usar_banca() -> void:
	# sentarse calma la plaza: la bandada vuelve, la iguana sale y Orbita comenta
	_banca_usos += 1
	await Interfaz.fundido(true, 0.35)
	var j: CharacterBody3D = Zonas.jugador
	if j != null and is_instance_valid(j):
		# junto a la banca, mirando a la fuente. PENDIENTE del rig: no hay clip de sentarse (jugador.gd vuelve a
		# «reposo» en cada cuadro), asi que no se finge hundiendo la malla en el suelo.
		j.colocar(Vector3(4.5, 0.0, -1.4), Vector3(-1, 0, 0))
	var gato: Node3D = Zonas.companero
	if gato != null and is_instance_valid(gato) and gato.has_method("colocar_junto"):
		gato.call("colocar_junto", Vector3(4.5, 0.0, -1.4), Vector3(-1, 0, 0))
	_palomas_vuelven(Vector3(2.9, 0.0, -1.6))
	for ig in _iguanas:
		var dato: Dictionary = ig
		if dato["escondida"]:
			_mostrar_iguana(dato)
	Audio.sonar("pulsar", -4.0)
	await Interfaz.fundido(false, 0.5)
	if _banca_usos == 1:
		Juego.anotar("observatorio_quito")
		await Interfaz.decir([
			"Te sientas un momento. Suena la fuente, el sol calienta los adoquines y las palomas vuelven a picotear.",
			{"quien": "Órbita", "texto": "Buen sitio para esperar la noche. El Observatorio Astronómico de Quito mira el cielo desde 1873."},
		])
		return
	var frases := [
		{"quien": "Órbita", "texto": "Si nadie corre, las palomas bajan solas. Con la Luna pasa igual: hay que saber esperar."},
		{"quien": "Órbita", "texto": "Desde aquí se ve la luz cian de la biblioteca. Esos libros nos esperan."},
		{"quien": "Órbita", "texto": "Mira las iguanas: se ponen al sol para calentarse. Nosotros, a la sombra."},
	]
	await Interfaz.decir([frases[(_banca_usos - 2) % frases.size()]])


func _usar_frutas() -> void:
	if not Juego.bandera("ciu_frutas_vistas"):
		Juego.poner_bandera("ciu_frutas_vistas")
		await Interfaz.decir([
			"Fruta del día en cajones de colores. Un cartel de Lidia: «Deje lo que pueda en la lata».",
			{"quien": "Órbita", "texto": "Lidia confía en el barrio. Y el barrio, en Lidia."},
		])
	var i: int = await Interfaz.elegir("¿Qué fruta tomas?", ["Mango", "Maracuyá", "Pitahaya", "Nada, gracias"])
	if i < 0 or i > 2:
		return
	Audio.sonar("tic", -2.0)
	Audio.sonar("recoger", -3.0)
	Juego.poner_bandera("ciu_fruta")
	var dichos := [
		["Dejas una moneda en la lata. El mango está tan maduro que se pela con la mano.", "Para mí no, gracias. Yo espero algo con escamas."],
		["Dejas una moneda en la lata. El maracuyá es tan ácido que cierras un ojo.", "Así se mira por el telescopio: con un ojo cerrado."],
		["Dejas una moneda en la lata. La pitahaya es blanca por dentro, con puntitos negros.", "Como un cielo al revés: estrellas oscuras sobre fondo claro."],
	]
	var d: Array = dichos[i]
	await Interfaz.decir([String(d[0]), {"quien": "Órbita", "texto": String(d[1])}])


func _usar_tablon() -> void:
	Juego.anotar("luna_sonriente")
	Audio.sonar("pagina", -3.0)
	await Interfaz.decir([
		"El tablón del barrio. En el centro, la convocatoria, con una Luna dibujada: «Graba 60 s de la Luna con un instrumento construido por ti».",
		"Alrededor: clases de guitarra, un gato naranja perdido (no es Órbita) y la feria del sábado.",
		{"quien": "Órbita", "texto": "La Luna del cartel sonríe: cuando es creciente y el borde iluminado apunta hacia abajo, parece una sonrisa."},
	])


func _usar_mosaico() -> void:
	Juego.anotar("terminador")
	await Interfaz.decir([
		"Alrededor de la fuente hay ocho lunas de mosaico: de la nueva a la llena y de vuelta, como un mes en el suelo.",
		{"quien": "Órbita", "texto": "La raya entre la parte clara y la oscura es el terminador: la frontera entre el día y la noche lunar."},
	])


func _usar_iguana() -> void:
	var ig: Dictionary = _iguanas[0] if not _iguanas.is_empty() else {}
	if ig.is_empty() or ig["escondida"]:
		return
	if Juego.bandera("ciu_iguana"):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Sigue al sol sobre los adoquines. No la molestemos."}])
		return
	Juego.poner_bandera("ciu_iguana")
	Audio.sonar("ok")
	_cabecear(ig)
	Interfaz.aviso("Observación anotada: iguana al sol en la plaza.", 3.0)
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Llegaste caminando y no se asustó. Mira: cabecea, es su forma de decir «esta piedra es mía»."},
	])


# ------------------------------------------------------------------ vida de la zona

func _vida() -> void:
	# iguanas
	for i in IGUANAS.size():
		var nodo: Node3D = _inst.get("FAU-01_%d" % i)
		if nodo == null:
			continue
		var g: Array = IGUANAS[i]
		var sitios: Array = SITIOS_IGUANA[i]
		_iguanas.append({"i": i, "nodo": nodo, "escala": nodo.scale, "y": float(g[3]), "sitios": sitios, "escondida": false,
			"calma": 0.0, "ocupada": false, "cabeceo": randf_range(3.0, 8.0)})
	# palomas: siete picotean junto a la fuente y tres viven en la cornisa de la biblioteca
	_posaderos_libres = POSADEROS.duplicate()
	var n_suelo := 7
	for i in n_suelo + 3:
		var nodo := modelo("%s/%sFAU-12.glb" % [MODELOS, C], Vector3.ZERO, randf_range(0.0, 360.0))
		if nodo == null:
			break
		for mi in nodo.find_children("*", "GeometryInstance3D", true, false):
			(mi as GeometryInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		nodo.scale = Vector3.ONE * randf_range(0.92, 1.08)
		var alas := [nodo.find_child("FAU-12_ala_i", true, false), nodo.find_child("FAU-12_ala_d", true, false)]
		var p := {"nodo": nodo, "alas": alas, "estado": "suelo", "t": randf() * 3.0, "desde": Vector3.ZERO, "hasta": Vector3.ZERO,
			"ctrl": Vector3.ZERO, "dur": 1.0, "espera": randf_range(1.0, 3.0), "posadero": Vector3.ZERO, "residente": i >= n_suelo,
			"paso": Vector3.ZERO, "centro": PALOMAS_CASA}
		if i < n_suelo:
			var a := randf() * TAU
			nodo.position = PALOMAS_CASA + Vector3(cos(a), 0.0, sin(a)) * randf_range(0.2, 1.1)
		else:
			var k := randi() % mini(4, _posaderos_libres.size())
			var pos: Vector3 = _posaderos_libres[k]
			_posaderos_libres.remove_at(k)
			p["estado"] = "posada"
			p["posadero"] = pos
			nodo.position = pos
			p["espera"] = 9999.0
		if _noche:
			nodo.visible = i >= n_suelo      # de noche solo duermen las de la cornisa
			if i < n_suelo:
				p["estado"] = "fuera"
		_plegar(p, 1.0)
		_palomas.append(p)


func _physics_process(delta: float) -> void:
	_t += delta
	var j: CharacterBody3D = Zonas.jugador
	if j == null or not is_instance_valid(j):
		return
	_encuadrar_biblioteca(j.global_position.z)
	var rapidez := Vector2(j.velocity.x, j.velocity.z).length()
	var libre: bool = not Interfaz.ocupada()
	for i in _iguanas.size():
		var ig: Dictionary = _iguanas[i]
		var nodo: Node3D = ig["nodo"]
		var lejos := Vector2(j.global_position.x - nodo.position.x, j.global_position.z - nodo.position.z).length()
		if not ig["escondida"]:
			if lejos < DIST_ESPANTA and rapidez > VEL_ESPANTA and libre:
				_esconder_iguana(ig, int(ig["i"]) == 0)
			elif lejos < DIST_APARTA and not ig["ocupada"] and (ig["sitios"] as Array).size() > 1 and libre:
				_apartar_iguana(ig, j.global_position)
			else:
				ig["cabeceo"] = float(ig["cabeceo"]) - delta
				if float(ig["cabeceo"]) <= 0.0:
					ig["cabeceo"] = randf_range(5.0, 11.0)
					_cabecear(ig)
		elif lejos > DIST_ESPANTA + 1.5:
			ig["calma"] = float(ig["calma"]) + delta
			if float(ig["calma"]) > 2.0:
				_mostrar_iguana(ig)
		else:
			ig["calma"] = 0.0
	# palomas: levantan vuelo si alguien se acerca caminando o corre hacia ellas
	var espantar := false
	for p in _palomas:
		var dato: Dictionary = p
		if dato["estado"] != "suelo":
			continue
		var n: Node3D = dato["nodo"]
		var d := Vector2(j.global_position.x - n.position.x, j.global_position.z - n.position.z).length()
		if d < DIST_PALOMAS or (d < DIST_PALOMAS_CORRER and rapidez > VEL_ESPANTA):
			espantar = true
			break
	if espantar:
		_espantar_palomas()


func _process(delta: float) -> void:
	for d in _destellos:
		if not is_instance_valid(d):
			continue
		var nodo: Node3D = d
		if nodo.is_inside_tree():
			nodo.scale = Vector3.ONE * 0.8 * (1.0 + 0.14 * sin(_t * 3.2))
			nodo.rotation.y += delta * 0.8
	var j: CharacterBody3D = Zonas.jugador
	for p in _palomas:
		_paloma(p, delta, j)


func _paloma(p: Dictionary, delta: float, j: CharacterBody3D) -> void:
	var n: Node3D = p["nodo"]
	if not is_instance_valid(n) or p["estado"] == "fuera":
		return
	p["t"] = float(p["t"]) + delta
	match String(p["estado"]):
		"suelo":
			# picotea y da pasitos
			var picoteo := maxf(0.0, sin(float(p["t"]) * 7.0)) * 0.5
			n.rotation.x = picoteo
			var paso: Vector3 = p["paso"]
			if paso.length() > 0.01:
				var avance := minf(delta * 0.45, paso.length())
				n.position += paso.normalized() * avance
				p["paso"] = paso - paso.normalized() * avance
				n.position.y = absf(sin(float(p["t"]) * 16.0)) * 0.025
			else:
				n.position.y = 0.0
			p["espera"] = float(p["espera"]) - delta
			if float(p["espera"]) <= 0.0:
				p["espera"] = randf_range(1.2, 3.5)
				var centro: Vector3 = p["centro"]
				var hacia := centro if Vector2(n.position.x - centro.x, n.position.z - centro.z).length() > 1.3 else n.position
				var a := randf() * TAU
				var meta := hacia + Vector3(cos(a), 0.0, sin(a)) * randf_range(0.15, 0.5)
				meta.y = 0.0
				p["paso"] = meta - Vector3(n.position.x, 0.0, n.position.z)
				var dir: Vector3 = p["paso"]
				if dir.length() > 0.01:
					n.rotation.y = atan2(dir.x, dir.z)
		"vuelo":
			var u := clampf(float(p["t"]) / float(p["dur"]), 0.0, 1.0)
			var a0: Vector3 = p["desde"]
			var c: Vector3 = p["ctrl"]
			var b: Vector3 = p["hasta"]
			var pos := a0.lerp(c, u).lerp(c.lerp(b, u), u)
			var tan := (c - a0).lerp(b - c, u)
			n.position = pos
			if Vector2(tan.x, tan.z).length() > 0.01:
				n.rotation.y = atan2(tan.x, tan.z)
			n.rotation.x = -clampf(tan.y * 0.15, -0.5, 0.5)
			var aleteo := sin(float(p["t"]) * 22.0) * (0.9 if u < 0.85 else 0.35)
			_aletear(p, aleteo)
			if u >= 1.0:
				n.rotation.x = 0.0
				_plegar(p, 1.0)
				if b.y > 0.05:
					p["estado"] = "posada"
					p["espera"] = randf_range(5.0, 9.0)
				else:
					p["estado"] = "suelo"
					p["espera"] = randf_range(0.5, 2.0)
					p["paso"] = Vector3.ZERO
				p["t"] = 0.0
		"posada":
			n.rotation.x = maxf(0.0, sin(float(p["t"]) * 2.0)) * 0.15
			if p["residente"]:
				return
			p["espera"] = float(p["espera"]) - delta
			if float(p["espera"]) <= 0.0:
				var cerca := j != null and is_instance_valid(j) and Vector2(j.global_position.x - PALOMAS_CASA.x, j.global_position.z - PALOMAS_CASA.z).length() < 4.0
				if cerca:
					p["espera"] = randf_range(2.0, 4.0)
				else:
					var a := randf() * TAU
					p["centro"] = PALOMAS_CASA
					_volar(p, PALOMAS_CASA + Vector3(cos(a), 0.0, sin(a)) * randf_range(0.2, 1.2))


func _volar(p: Dictionary, destino: Vector3) -> void:
	var n: Node3D = p["nodo"]
	var desde := n.position
	var posadero: Vector3 = p["posadero"]
	if posadero != Vector3.ZERO and String(p["estado"]) == "posada":
		_posaderos_libres.append(posadero)
		p["posadero"] = Vector3.ZERO
	p["desde"] = desde
	p["hasta"] = destino
	p["ctrl"] = (desde + destino) * 0.5 + Vector3(0.0, 1.6 + desde.distance_to(destino) * 0.15, 0.0)
	p["dur"] = clampf(desde.distance_to(destino) / 4.5, 1.1, 3.2)
	p["t"] = 0.0
	p["estado"] = "vuelo"
	_plegar(p, 0.0)


func _espantar_palomas() -> void:
	var primera: bool = not Juego.bandera("ciu_palomas")
	var n := 0
	for p in _palomas:
		var dato: Dictionary = p
		if dato["estado"] != "suelo":
			continue
		var destino := Vector3(randf_range(-2.0, 2.0), 3.5, -8.05)
		if not _posaderos_libres.is_empty():
			var k := randi() % _posaderos_libres.size()
			destino = _posaderos_libres[k]
			_posaderos_libres.remove_at(k)
			dato["posadero"] = destino
		_volar(dato, destino)
		dato["t"] = -0.05 * n        # salen escalonadas
		n += 1
	if n == 0:
		return
	Audio.sonar("pagina", 1.0)
	var eco := create_tween()
	eco.tween_interval(0.09)
	eco.tween_callback(func() -> void: Audio.sonar("pagina", -4.0))
	eco.tween_interval(0.12)
	eco.tween_callback(func() -> void: Audio.sonar("pagina", -8.0))
	if primera:
		Juego.poner_bandera("ciu_palomas")
		Interfaz.aviso("¡Fsss! Las palomas levantan vuelo. Órbita las sigue con la mirada.", 3.0)


func _palomas_vuelven(centro: Vector3) -> void:
	# al sentarse en la banca: las que estan fuera vuelven a picotear delante (sin vuelo: ocurre tras el fundido)
	for p in _palomas:
		var dato: Dictionary = p
		if dato["residente"] or dato["estado"] == "fuera":
			continue
		var posadero: Vector3 = dato["posadero"]
		if posadero != Vector3.ZERO:
			_posaderos_libres.append(posadero)
			dato["posadero"] = Vector3.ZERO
		var a := randf() * TAU
		var n: Node3D = dato["nodo"]
		n.position = centro + Vector3(cos(a), 0.0, sin(a)) * randf_range(0.3, 1.1)
		n.position.y = 0.0
		n.rotation = Vector3(0.0, randf() * TAU, 0.0)
		dato["estado"] = "suelo"
		dato["paso"] = Vector3.ZERO
		dato["centro"] = centro
		dato["espera"] = randf_range(0.5, 2.0)
		_plegar(dato, 1.0)


func _aletear(p: Dictionary, a: float) -> void:
	var alas: Array = p["alas"]
	if alas.size() < 2 or alas[0] == null or alas[1] == null:
		return
	(alas[0] as Node3D).rotation = Vector3(0.0, -0.1, -a)
	(alas[1] as Node3D).rotation = Vector3(0.0, 0.1, a)


func _plegar(p: Dictionary, plegado: float) -> void:
	var alas: Array = p["alas"]
	if alas.size() < 2 or alas[0] == null or alas[1] == null:
		return
	(alas[0] as Node3D).rotation = Vector3(0.0, -1.35 * plegado, -0.25 * plegado)
	(alas[1] as Node3D).rotation = Vector3(0.0, 1.35 * plegado, 0.25 * plegado)


func _cabecear(ig: Dictionary) -> void:
	# las iguanas hacen «flexiones» con la cabeza: tres cabeceos rapidos
	var nodo: Node3D = ig["nodo"]
	if ig["ocupada"] or not is_instance_valid(nodo):
		return
	var e: Vector3 = ig["escala"]
	var t := create_tween()
	for k in 3:
		t.tween_property(nodo, "scale", Vector3(e.x, e.y * 1.12, e.z), 0.12)
		t.tween_property(nodo, "scale", e, 0.14)


func _apartar_iguana(ig: Dictionary, desde: Vector3) -> void:
	var nodo: Node3D = ig["nodo"]
	var mejor: Vector2 = Vector2(nodo.position.x, nodo.position.z)
	var lejos := -1.0
	for s in ig["sitios"]:
		var sitio: Vector2 = s
		var d := sitio.distance_to(Vector2(desde.x, desde.z))
		if d > lejos:
			lejos = d
			mejor = sitio
	if mejor.distance_to(Vector2(nodo.position.x, nodo.position.z)) < 0.2:
		return
	ig["ocupada"] = true
	var destino := Vector3(mejor.x, float(ig["y"]), mejor.y)
	var dir := destino - nodo.position
	var t := create_tween()
	t.tween_property(nodo, "rotation:y", atan2(dir.x, dir.z), 0.08)
	t.tween_property(nodo, "position", destino, 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	t.tween_callback(func() -> void:
		ig["ocupada"] = false
		if int(ig["i"]) == 0 and _iguana_inter != null and is_instance_valid(_iguana_inter):
			_iguana_inter.position = Vector3(nodo.position.x, 0.0, nodo.position.z))
	Audio.sonar("paso", 2.0)
	var otro := create_tween()
	otro.tween_interval(0.16)
	otro.tween_callback(func() -> void: Audio.sonar("paso", -2.0))


func _encuadrar_biblioteca(z: float) -> void:
	# la camara aprobada queda a menos de 7 m de altura y la fachada mide 5 m: de cerca solo se verian las
	# columnas. Al acercarse a las gradas la camara se aleja (de 0,17 a 0,105) y deja ver el fronton con el libro.
	# Se respeta lo que el jugador cambie con Z y X.
	var cam: Camera3D = Zonas.camara
	if cam == null or not is_instance_valid(cam):
		return
	var actual: float = cam.get("encuadre")
	if _enc_base <= 0.0:
		_enc_base = actual
	elif absf(actual - _enc_puesto) > 0.0002:
		_enc_base = clampf(_enc_base + (actual - _enc_puesto), 0.10, 0.24)
	var cerca := smoothstep(-2.6, -6.4, z)
	_enc_puesto = maxf(_enc_base * lerpf(1.0, 0.6, cerca), 0.10)
	cam.set("encuadre", _enc_puesto)


func _esconder_iguana(ig: Dictionary, avisar: bool) -> void:
	ig["escondida"] = true
	if avisar:
		Juego.poner_bandera("ciu_iguana_espantada")
	ig["calma"] = 0.0
	var nodo: Node3D = ig["nodo"]
	if avisar and _iguana_inter != null and is_instance_valid(_iguana_inter):
		_iguana_inter.set("habilitado", false)
	Audio.sonar("paso", 3.0)
	var giro := create_tween()
	giro.tween_property(nodo, "scale", (ig["escala"] as Vector3) * 0.05, 0.22)
	giro.tween_callback(func() -> void: nodo.visible = false)
	if avisar and not Juego.bandera("ciu_iguana"):
		Interfaz.aviso("La iguana se escondió bajo la banca. Aléjate y vuelve caminando.", 3.5)


func _mostrar_iguana(ig: Dictionary) -> void:
	ig["escondida"] = false
	var nodo: Node3D = ig["nodo"]
	nodo.visible = true
	var giro := create_tween()
	giro.tween_property(nodo, "scale", ig["escala"], 0.4)
	if int(ig["i"]) == 0 and _iguana_inter != null and is_instance_valid(_iguana_inter):
		_iguana_inter.set("habilitado", true)


func al_entrar(nombre_entrada: String) -> void:
	if not Juego.bandera("ciudad_visitada"):
		Juego.poner_bandera("ciudad_visitada")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "La Plaza de las Iguanas. A la derecha sale el sendero del arroyo, hacia el cerro."},
			{"quien": "Órbita", "texto": "Al fondo está la biblioteca municipal. ¿Ves la luz cian de la puerta?"},
		])
	elif _noche and nombre_entrada == "sendero" and not Juego.bandera("ciudad_noche_vista"):
		Juego.poner_bandera("ciudad_noche_vista")
		await Interfaz.decir([{"quien": "Órbita", "texto": "Ya encendieron los faroles. Tu casa es la amarilla, al otro lado de la plaza."}])


func orbita_dice() -> Array:
	if _noche:
		return [{"quien": "Órbita", "texto": "Es tarde. Tu casa es la amarilla, a la izquierda de la plaza."}]
	if not Juego.bandera("base_visitada"):
		return [{"quien": "Órbita", "texto": "De la puerta de la biblioteca sale una luz cian. Sube las gradas y mira."}]
	return []


func ruta_de_prueba() -> Array:
	if _noche:
		# de noche se vuelve del sendero a casa, pasando junto a la fuente
		return [
			{"ir": Vector3(8.0, 0.0, 2.6)}, {"ir": Vector3(0.0, 0.0, 2.7)}, {"ir": Vector3(-6.0, 0.0, 2.4)},
			{"ir": Vector3(-10.4, 0.0, 0.55)}, {"ir": P_CASA},
		]
	var pasos: Array = [{"bandera": "ciudad_visitada"}, {"ir": Vector3(-6.0, 0.0, 2.4)}, {"ir": Vector3(0.0, 0.0, 2.7)}, {"usar": "Fuente"}]
	if Juego.bandera("visita_libre"):
		# en la visita libre (prueba de la zona) se usa todo lo nuevo y se sube a la puerta de la biblioteca
		pasos.append_array([
			{"usar": "Fuente"}, {"ir": Vector3(-3.0, 0.0, 1.0)}, {"usar": "MosaicoLunas"},
			# el piloto de la prueba siempre corre (3,6 m/s): al acercarse a la iguana 0 la espanta y se esconde.
			# Observarla caminando (sin Mayus) solo se demuestra con teclas: recorrido_manos o el director jugando.
			# (la espera deja pasar los 0,3 s reales en que la interfaz sigue ocupada tras el dialogo, a ritmo 6)
			{"esperar": 2.4}, {"ir": Vector3(-3.0, 0.0, 2.7)}, {"ir": Vector3(-4.3, 0.0, 5.65)}, {"bandera": "ciu_iguana_espantada"},
			{"ir": Vector3(-6.4, 0.0, 6.2)}, {"usar": "ColCarta"}, {"usar": "EstatuaIguana"},
			{"ir": Vector3(-3.0, 0.0, 2.7)}, {"ir": Vector3(0.0, 0.0, 4.1)}, {"usar": "PosteIndicador"},
			{"ir": Vector3(3.8, 0.0, 2.6)}, {"ir": Vector3(3.9, 0.0, -1.4)}, {"usar": "Banca"},
			{"ir": Vector3(4.6, 0.0, -2.6)}, {"ir": Vector3(4.6, 0.0, -5.45)}, {"usar": "Tablon"},
			{"ir": Vector3(4.6, 0.0, -2.6)}, {"ir": Vector3(8.2, 0.0, -3.0)}, {"usar": "ColPlaca"}, {"usar": "PuestoElectronica"},
			{"ir": Vector3(4.6, 0.0, -2.6)}, {"ir": Vector3(0.6, 0.0, -6.2)}, {"ir": Vector3(0.0, 0.42, -8.2)},
			{"usar": "Biblioteca"}, {"bandera": "base_visitada"},
			{"ir": Vector3(0.6, 0.0, -6.2)}, {"ir": Vector3(-4.6, 0.0, -2.6)}, {"ir": Vector3(-7.3, 0.0, -3.2)}, {"usar": "Kiosco"},
			{"ir": Vector3(-9.4, 0.0, -3.0)},
			{"ir": Vector3(-10.4, 0.0, -4.6)}, {"usar": "PuestoFrutas"}, {"bandera": "ciu_fruta"},
			{"ir": Vector3(-9.4, 0.0, -3.0)}, {"ir": Vector3(-4.6, 0.0, 2.0)}, {"ir": Vector3(3.8, 0.0, 2.6)},
			{"ir": Vector3(9.0, 0.0, 2.6)}, {"ir": Vector3(10.4, 0.0, 6.3)}, {"usar": "ColCable"},
		])
	pasos.append_array([{"ir": Vector3(9.0, 0.0, 2.0)}, {"ir": P_SENDERO}])
	return pasos
