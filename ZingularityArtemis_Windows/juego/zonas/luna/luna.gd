extends "res://nucleo/zona.gd"

# La Luna del sueno (escenas 3.1 a 3.6 de la Fase 2), VERSION 2. PROVISIONAL: no hay concepto validado de la Luna.
# Al acostarse, la protagonista suena que esta en la Luna: camina y salta a 1/6 g, recolecta muestras, mira la
# etapa de descenso sin pisar su sitio y planta JUNTAS las banderas de Estados Unidos y de Ecuador.
#
# Recorrido (cuatro areas enlazadas a pie, con balizas y estacas cian de ruta y las huellas que ella va dejando):
#   llegada (la caja) -> zanja (reto de salto) y baliza -> campo de muestras junto a un crater pequeno
#   -> anillo cian de 75 m alrededor de la etapa de descenso (se mira, no se pisa) -> loma de las dos banderas
#   -> de vuelta a la caja (el regreso).
# Escala del mapa: 1:4 (Fase 2, 4.3). El anillo de 75 m es un circulo de 18,75 m de radio; los objetos van a
# tamano real. Cerca del anillo la camara se abre sola para que se vean ella y la etapa de descenso.
#
# v2 (pedido de Guillermo: «la seccion de la Luna se ve extremadamente sencilla»):
# - color: regolito con gris calido, gris azulado, violeta en los fondos, mares oscuros y rayos claros
#   (terreno.gd); facetas al sol calidas y de espaldas violetas (regolito.gdshader); luz de la Tierra lavanda y
#   relleno azul violeta; acentos dorados, carton y cian. Nunca negro.
#   v2e (2026-11-15): color medido contra el arte de carga pintado (llano al sol crema rosado #C6A8A4, sombras
#   azul violeta #5E5E89 a #908AA5): luz principal crema calida, relleno azul violeta y carton ocre.
# - dinamicas: salto lunar medido (con reto de la zanja), rocas sueltas que se patean (RigidBody3D a 1,624 m/s2),
#   huellas de botas y de gato que se quedan, seis muestras sueltas que se recogen con E, el anillo que reacciona
#   al acercarse, tres puntos de interes con su ficha y la foto con marco.
# - efectos: polvo balistico (sin aire no hace nubes: cae en parabolas), balizas que se encienden en carrera hacia
#   el objetivo, destellos de las muestras, vineta del sueno y amanecer calido al plantar las banderas.
#
# Recursos: LUN-01 terreno (terreno.gd); LUN-02 rocas, LUN-03 etapa de descenso generica, LUN-04 caja-capsula,
# LUN-10 piedras, LUN-11 eyecta, LUN-12 balizas de camino, LUN-13 estacion de medicion, LUN-14 espejo,
# LUN-15 soporte y bolsas, LUN-16 muestras sueltas, LUN-17 instrumento, LUN-18 penascos, LUN-19 camara de carton
# (herramientas/mallas/luna_recursos_v2.py); LUN-20 labio facetado de los crateres (v2f, por codigo en _montar_bordes); LUN-05 baliza y estaca, LUN-06 y LUN-07 banderas, LUN-08 caja de
# herramientas y LUN-09 casco (herramientas/mallas/luna_modelos.py). Sin insignias, logotipos ni textos.
# No aparecen astronautas.

const Terreno := preload("res://zonas/luna/terreno.gd")
const Estilo := preload("res://interfaz/estilo.gd")
const REGOLITO := preload("res://zonas/luna/shaders/regolito.gdshader")
const BRILLO := preload("res://zonas/luna/shaders/brillo.gdshader")
const CASCO := preload("res://zonas/luna/shaders/casco.gdshader")
const PINTURA := preload("res://zonas/luna/shaders/pintura.gdshader")
const VINETA := preload("res://zonas/luna/shaders/vineta.gdshader")
const MODELOS := "res://modelos/luna/"

const ESCALA := 4.0                          # 1:4
const R_ANILLO := 75.0 / ESCALA              # 18,75 m de juego
const MARGEN_ANILLO := 0.25                  # ella se detiene con los pies justo fuera de la linea
const P_CAJA := Vector2(-2.1, -0.9)
const P_BALIZA := Vector2(3.0, -24.0)
const P_MUESTRAS := Vector2(25.0, -39.5)
const P_HERRAMIENTAS := Vector2(26.4, -40.6)
const P_SOPORTE := Vector2(22.3, -41.0)
const P_ETAPA := Vector2(60.0, -36.0)
const P_FOTO := Vector2(60.0, -15.9)         # borde sur del anillo: la etapa queda al fondo
const P_LOMA := Vector2(36.0, -8.0)          # a 37 m de la etapa: el doble del radio del anillo
const P_ESPEJO := Vector2(-5.0, -7.6)        # punto de interes: la Tierra en el espejo
const P_ESTACION := Vector2(15.5, -23.6)     # punto de interes: temperaturas de la superficie
const P_INSTRUMENTO := Vector2(24.5, -9.6)   # punto de interes: la noche en Tranquilidad
const X_ASTA_EEUU := 34.35
const X_ASTA_ECUADOR := 36.25
const Z_ASTAS := -8.9
const PUERTA_A := 11.0                       # x: mas alla hace falta la baliza
const PUERTA_B := 37.0                       # x: mas alla hacen falta las muestras
const R_PUERTA_LOMA := 9.5                   # la loma pide la foto
const ENCUADRE_PANORAMA := 0.052
const ZANJA_A := Vector2(-10.0, -11.2)       # eje de la zanja (reto de salto)
const ZANJA_B := Vector2(11.0, -13.4)
const ZANJA_MEDIO := 1.9

# estacas de ruta (x, z), en orden de recorrido
const RUTA := [
	Vector2(0.9, -6.5), Vector2(1.6, -17.5), Vector2(10.5, -28.6), Vector2(18.0, -34.2), Vector2(32.5, -36.2),
	Vector2(39.0, -36.6), Vector2(40.8, -27.0), Vector2(45.3, -20.7), Vector2(52.5, -16.2),
	Vector2(52.0, -10.6), Vector2(44.0, -7.9), Vector2(27.0, -4.4), Vector2(18.0, -2.2), Vector2(9.0, -0.6),
]
const BALIZAS_CAMINO := [0, 1, 2, 4, 6, 8, 10, 12]     # puntos de RUTA con baliza LUN-12 (el resto, estaca)
# rocas grandes con colision: [x, z, escala, variante]
const PENASCOS := [
	[6.5, -9.0, 1.3, 0], [-4.5, -19.0, 1.6, 2], [9.5, -23.5, 1.1, 1], [20.0, -31.0, 1.5, 4], [29.0, -33.0, 1.2, 3],
	[36.0, -30.0, 1.7, 2], [47.5, -14.5, 1.4, 5], [30.0, -2.0, 1.2, 0], [15.0, -8.0, 1.0, 6], [55.0, -7.0, 1.5, 2],
	[-7.0, 4.0, 1.4, 7], [21.5, -44.0, 1.1, 3], [43.0, -44.0, 1.3, 1], [72.0, -12.0, 1.6, 0],
]
# penascos grandes LUN-18: [x, z, escala, variante (0 = bloque alto, 1 = afloramiento), giro]
const GRANDES := [
	[-6.6, 0.9, 0.95, 0, 25.0], [-14.0, -22.0, 1.2, 1, 80.0], [7.5, -36.5, 0.9, 0, 150.0], [48.0, -50.0, 1.3, 1, 10.0],
	[74.0, -13.0, 1.0, 0, 200.0], [-15.0, -45.0, 1.1, 0, 60.0], [30.0, 5.5, 1.0, 1, 120.0], [82.0, -38.0, 1.2, 1, 0.0],
	[12.0, 4.5, 0.8, 0, 300.0],
]
# rocas sueltas que se patean (RigidBody3D): [x, z, tamano]
const ROCAS_SUELTAS := [
	[1.9, -4.3, 0.34], [-0.8, -8.0, 0.28], [3.9, -16.2, 0.4], [6.1, -21.2, 0.3], [9.2, -27.2, 0.36], [15.5, -33.4, 0.42],
	[21.6, -35.4, 0.3], [29.6, -36.0, 0.38], [44.4, -19.2, 0.34], [51.6, -12.8, 0.4], [22.0, -3.1, 0.32], [5.2, -1.9, 0.3],
]
# muestras sueltas que se recogen con E: [x, z, variante]
const SUELTAS := [
	[5.6, -18.2, 0], [12.9, -31.4, 1], [19.0, -37.6, 2], [32.2, -41.8, 0], [30.0, -17.6, 1], [13.6, -5.4, 2],
]

# v2e: la luz principal se pinta crema calida, como el arte de carga pintado (licencia del sueno: los datos dicen
# que es de noche y que la luz viene de la Tierra); el relleno azul violeta pinta las sombras. Nunca negro.
const NOCHE_SOL := Color("f4dcc8")           # luz principal: crema calida
const NOCHE_ENERGIA := 0.95
const CONTRASTE_NOCHE := 1.12
const ALBA_SOL := Color("ffb877")            # el Sol rasante del amanecer del sueno: mas naranja
const NOCHE_AMB := Color("4a5290")           # relleno azul violeta de la Tierra
const ALBA_AMB := Color("8f7a8c")              # v2d: mas claro, las sombras del alba no bajan del violeta
const DIR_NOCHE := Vector3(0.72, -0.60, -0.20)
const DIR_ALBA := Vector3(-0.80, -0.33, -0.45)
const RELIEVE_NOCHE := Vector3(-0.72, 0.60, 0.20)
const RELIEVE_ALBA := Vector3(0.80, 0.33, 0.45)

const LLEGADA := [
	{"quien": "Órbita", "texto": "Probando la radio del casco. ¿Me copias? Tu caja de cartón alunizó en el Mar de la Tranquilidad."},
	{"quien": "Órbita", "texto": "Aquí la gravedad es de 1,624 m/s²: más o menos la sexta parte de la terrestre."},
	{"quien": "Órbita", "texto": "Tu masa sigue contigo. Lo que cambió es tu peso. Por eso cuesta frenar: anticípate."},
	{"quien": "Órbita", "texto": "Es de noche: el Sol está 25,3° bajo el horizonte. Esta luz nos llega de la Tierra."},
	{"quien": "Órbita", "texto": "Salta con Espacio y sigue las balizas cian hasta la baliza grande. Y patea alguna piedra: mira cómo vuela."},
]
const MENSAJES := {
	"anillo": [
		{"quien": "Órbita", "texto": "Alto ahí. Ese anillo marca 75 m alrededor de la etapa de descenso del Apolo 11."},
		{"quien": "Órbita", "texto": "Es la distancia que la NASA recomienda a los robots visitantes. No es una ley: es una buena costumbre."},
		{"quien": "Órbita", "texto": "Se mira, no se pisa. En el sueño el mapa va a escala 1:4, así que rodearlo es un paseo."},
	],
	"baliza": [{"quien": "Órbita", "texto": "Primero la baliza. Aprende a moverte antes de alejarte de la caja."}],
	"muestras": [{"quien": "Órbita", "texto": "Antes de ir al anillo, recojamos las muestras. Están junto al cráter pequeño."}],
	"loma": [{"quien": "Órbita", "texto": "La loma puede esperar. Primero la foto, desde el borde del anillo."}],
}
const CORTOS := {
	"anillo": "Órbita: «Se mira, no se pisa. Rodea el anillo.»",
	"baliza": "Órbita: «Primero la baliza.»",
	"muestras": "Órbita: «Primero las muestras.»",
	"loma": "Órbita: «Primero la foto.»",
}
const DATOS_ORBITA := [
	"Mis huellas son las únicas de gato en la Luna. Que conste en el cuaderno.",
	"Vista desde aquí, la Tierra se queda casi en el mismo punto del cielo. Sus fases van al revés que las de la Luna.",
	"El regolito incluye desde peñascos hasta polvo. Todo lo dejaron los impactos.",
	"En la Luna tu masa no cambia. Tu peso sí, porque la gravedad es menor.",
	"¿Ves el polvo? Cae en parábolas y no forma nubes: aquí no hay aire que lo frene.",
]
const POI := {
	"Espejo": {
		"ficha": "tierra_en_cielo_lunar", "bandera": "luna_poi_espejo", "texto": "Mirar el espejo",
		"lineas": [
			{"quien": "Órbita", "texto": "Asómate al espejo. Desde aquí abajo no vemos el cielo, pero el espejo nos trae a la Tierra."},
			{"quien": "Órbita", "texto": "Vista desde la Luna, la Tierra se queda más o menos en el mismo punto del cielo. Solo oscila un poco."},
			{"quien": "Órbita", "texto": "Y sus fases van al revés que las de la Luna. Esta noche, desde el Mirador, la Luna era una tajada fina: por eso la Tierra se ve casi llena."},
		],
	},
	"Estacion": {
		"ficha": "temperaturas_lunares", "bandera": "luna_poi_estacion", "texto": "Leer la estación",
		"lineas": [
			{"quien": "Órbita", "texto": "Una estación que mide la temperatura del suelo. Mira qué extremos guarda."},
			{"quien": "Órbita", "texto": "La superficie lunar llega a unos 127 °C a pleno Sol y baja a unos −173 °C en la oscuridad."},
			{"quien": "Órbita", "texto": "Son extremos de la superficie. Por eso el traje y el casco importan tanto, aunque esto sea un sueño."},
		],
	},
	"Instrumento": {
		"ficha": "noche_lunar", "bandera": "luna_poi_instrumento", "texto": "Revisar el instrumento",
		"lineas": [
			{"quien": "Órbita", "texto": "Este instrumento está dormido: sus paneles no cargan nada."},
			{"quien": "Órbita", "texto": "Con datos de NASA calculamos que el Sol está a −25,3° en Tranquilidad: bajo el horizonte. Aquí es de noche."},
			{"quien": "Órbita", "texto": "Le toca esperar el amanecer. Nosotros, en el sueño, podemos hacer trampa."},
		],
	},
}

var terreno: RefCounted
var radio_minimapa := 34.0                   # metros que abarca el minimapa (lo lee el HUD)
var _sol: DirectionalLight3D
var _entorno: Environment
var _libre := false
var _mat_brillo: ShaderMaterial
var _mat_anillo: ShaderMaterial
var _mat_baliza: ShaderMaterial
var _mat_casco: ShaderMaterial
var _mat_pintura: ShaderMaterial
var _mat_regolito: ShaderMaterial
var _mat_destello: ShaderMaterial
var _mat_vineta: ShaderMaterial
var _luz_baliza: OmniLight3D
var _banderas: Array[Node3D] = []
var _marcas_loma: Node3D
var _casco_j: Node3D
var _casco_o: Node3D
var _foco := Node3D.new()
var _panorama := false
var _encuadre_jugador := 0.16
var _hablando := false
var _ultimo_aviso := {}
var _avisos_dados := {}
var _dato := 0
var _huellas: MultiMesh
var _patas: MultiMesh
var _n_huellas := 0
var _n_patas := 0
var _ultima_huella := Vector3.INF
var _ultima_pata := Vector3.INF
var _pie := 1.0
var _aabb := AABB(Vector3(-26, -6, -74), Vector3(124, 14, 100))
var _t := 0.0
# rocas sueltas
var _rocas: Array[RigidBody3D] = []
var _patada := {}
# muestras sueltas: [nodo de la muestra, destello, y base]
var _sueltas: Array = []
# salto lunar
var _en_suelo_antes := true
var _t_aire := 0.0
var _despegue := Vector3.INF
var _record := 0.0
var _ultimo_salto_aviso := -9999
# polvo balistico
const POLVO_MAX := 72
var _polvo: MultiMesh
var _p_pos := PackedVector3Array()
var _p_vel := PackedVector3Array()
var _p_vida := PackedFloat32Array()
var _p_max := PackedFloat32Array()
var _p_tam := PackedFloat32Array()
var _p_sig := 0
var _p_vivas := 0
var _anillo_avisado := false


func _construir() -> void:
	gravedad = 1.624
	salto = 2.2
	inercia = 0.35
	factor_velocidad = 1.3
	encuadre = 0.16
	limites = Rect2(-12.0, -58.0, 96.0, 68.0)
	_libre = bool(Juego.bandera("visita_libre"))
	_record = float(Juego.bandera("luna_record_salto", 0.0))

	# noche lunar bajo la luz de la Tierra: lavanda palida y relleno azul violeta; sombras de color, nunca negras.
	# La luz entra baja desde la izquierda (licencia del sueno: sombras largas que dibujan los crateres).
	# v2e: medido contra carga_luna.jpg (llano al sol #C6A8A4, sombras #5E5E89 a #908AA5)
	_sol = luces("luna", {
		"sombra_distancia": 60.0, "sol": NOCHE_SOL.to_html(false), "energia": NOCHE_ENERGIA, "direccion": DIR_NOCHE,
		"ambiente": NOCHE_AMB.to_html(false), "ambiente_energia": 0.75, "saturacion": 1.0, "contraste": CONTRASTE_NOCHE,
		"exposicion": 1.0, "fondo": "1c1c38",
	})
	_entorno = (get_node("Entorno") as WorldEnvironment).environment
	ambiente(0.35)

	_mat_brillo = _material(BRILLO, {"energia": 2.2})
	_mat_brillo.resource_name = "Emisivo"
	_mat_anillo = _material(BRILLO, {"energia": 0.85, "pulso": 0.18})
	_mat_baliza = _material(BRILLO, {"energia": 0.55})
	_mat_casco = _material(CASCO)
	_mat_pintura = _material(PINTURA)
	_mat_destello = _material(BRILLO, {"energia": 1.6, "pulso": 0.45, "color": Color("cef8f5")})
	_foco.name = "FocoCamara"
	add_child(_foco)

	_montar_terreno()
	_montar_bordes()
	_montar_rocas()
	_montar_piedras()
	_montar_eyecta()
	_montar_grandes()
	_montar_ruta()
	_montar_zanja()
	_montar_llegada()
	_montar_baliza()
	_montar_muestras()
	_montar_anillo()
	_montar_loma()
	_montar_puntos_de_interes()
	_montar_sueltas()
	_montar_rocas_sueltas()
	_montar_huellas()
	_montar_polvo()
	_montar_vineta()
	cerco(Rect2(-13.0, -61.0, 98.0, 74.0), 6.0, -2.0)
	if bool(Juego.bandera("luna_banderas")):
		_luz_alba(0.3)


# ------------------------------------------------------------------ construccion

func _material(shader: Shader, valores: Dictionary = {}) -> ShaderMaterial:
	# material propio de la zona con los parametros comunes del estilo (inclinacion, pintado, pinceladas)
	var m := ShaderMaterial.new()
	m.shader = shader
	for nombre in Materiales.parametros:
		m.set_shader_parameter(nombre, Materiales.parametros[nombre])
	for nombre in valores:
		m.set_shader_parameter(nombre, valores[nombre])
	Materiales.creados.append(m)
	return m


func _suelo(p: Vector2, alza: float = 0.0) -> Vector3:
	return Vector3(p.x, terreno.altura(p.x, p.y) + alza, p.y)


func _arreglar_materiales(raiz: Node, brillo: ShaderMaterial = null) -> void:
	# «Emisivo» lleva el brillo con inclinacion 2.5D (el del nucleo no se inclina), «Casco» el cristal y
	# «Pintura» el color sin luz (el reflejo del espejo)
	var lista: Array = raiz.find_children("*", "MeshInstance3D", true, false)
	if raiz is MeshInstance3D:
		lista.append(raiz)
	for n in lista:
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			var original := mi.mesh.surface_get_material(s)
			var nombre: String = original.resource_name if original != null else ""
			if nombre.begins_with("Emisivo"):
				mi.set_surface_override_material(s, brillo if brillo != null else _mat_brillo)
			elif nombre.begins_with("Casco"):
				mi.set_surface_override_material(s, _mat_casco)
			elif nombre.begins_with("Pintura"):
				mi.set_surface_override_material(s, _mat_pintura)


func _poner(ident: String, pos: Vector3, giro_grados: float = 0.0, escala: float = 1.0, brillo: ShaderMaterial = null) -> Node3D:
	var nodo := modelo(MODELOS + ident + ".glb", pos, giro_grados, {"escala": escala})
	if nodo != null:
		_arreglar_materiales(nodo, brillo)
	return nodo


func _mallas_de(ident: String) -> Array:
	# las mallas de un GLB, en el orden de sus nodos, con los materiales de la zona puestos en la propia malla
	var mallas: Array = []
	var plantilla := Recursos.plantilla(MODELOS + ident + ".glb")
	if plantilla == null:
		push_warning("AVISO falta el modelo %s" % ident)
		return mallas
	for n in plantilla.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			var original := mi.mesh.surface_get_material(s)
			var nombre: String = original.resource_name if original != null else ""
			mi.mesh.surface_set_material(s, _mat_brillo if nombre.begins_with("Emisivo") else Materiales.compartido("facetado"))
		mallas.append(mi.mesh)
	return mallas


func _multimalla(malla: Mesh, transformadas: Array, sombra: bool = true, capacidad: int = 0) -> MultiMesh:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.mesh = malla
	mm.instance_count = maxi(transformadas.size(), capacidad)
	for i in transformadas.size():
		mm.set_instance_transform(i, transformadas[i])
	if capacidad > 0:
		mm.visible_instance_count = transformadas.size()
	var nodo := MultiMeshInstance3D.new()
	nodo.multimesh = mm
	nodo.custom_aabb = _aabb
	nodo.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON if sombra else GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(nodo)
	return mm


func _cinta(m: Dictionary, a: Vector2, b: Vector2, ancho: float, alza: float = 0.06) -> void:
	# tira luminosa pegada al suelo entre dos puntos (x, z)
	var lado := (b - a).orthogonal().normalized() * ancho * 0.5
	var p: Array = [_suelo(a - lado, alza), _suelo(a + lado, alza), _suelo(b + lado, alza), _suelo(b - lado, alza)]
	Piezas.cara(m, p, Color("62e4e0"), (p[0] + p[2]) * 0.5 - Vector3.UP)


func _nodo_brillo(m: Dictionary, material: ShaderMaterial, nombre: String) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.name = nombre
	mi.mesh = Piezas.malla(m)
	mi.material_override = material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.extra_cull_margin = 2.5
	add_child(mi)
	return mi


func _lejos_de_lo_importante(p: Vector2, margen: float = 1.6) -> bool:
	# nada de piedras sobre los sitios de juego, la ruta ni la linea del anillo
	for q in [P_BALIZA, P_MUESTRAS, P_FOTO, P_CAJA, P_ESPEJO, P_ESTACION, P_INSTRUMENTO, P_SOPORTE, P_HERRAMIENTAS]:
		if p.distance_to(q) < margen:
			return false
	if p.length() < 3.2 or p.distance_to(P_LOMA) < 3.4 or p.distance_to(P_ETAPA) < 5.5:
		return false
	if absf(p.distance_to(P_ETAPA) - R_ANILLO) < 0.5:
		return false
	for s in SUELTAS:
		if p.distance_to(Vector2(float(s[0]), float(s[1]))) < 0.9:
			return false
	return true


func _montar_terreno() -> void:
	terreno = Terreno.new()
	var libres: Array = [[0.0, 0.0, 4.5], [P_CAJA.x, P_CAJA.y, 2.0], [P_BALIZA.x, P_BALIZA.y, 3.0], [P_MUESTRAS.x, P_MUESTRAS.y, 3.5],
		[P_ETAPA.x, P_ETAPA.y, 9.0], [P_FOTO.x, P_FOTO.y, 3.0], [P_LOMA.x, P_LOMA.y, 7.0],
		[P_ESPEJO.x, P_ESPEJO.y, 2.0], [P_ESTACION.x, P_ESTACION.y, 2.0], [P_INSTRUMENTO.x, P_INSTRUMENTO.y, 2.0],
		[-10.0, -11.2, 2.5], [-3.0, -12.0, 2.5], [4.0, -12.7, 2.5], [11.0, -13.4, 2.5]]
	for p in RUTA:
		libres.append([p.x, p.y, 2.0])
	for p in PENASCOS:
		libres.append([p[0], p[1], 1.5])
	for s in SUELTAS:
		libres.append([s[0], s[1], 1.2])
	terreno.generar(1969, {
		"lomas": [[P_LOMA.x, P_LOMA.y, 1.7, 5.5]],
		"zanjas": [[ZANJA_A.x, ZANJA_A.y, ZANJA_B.x, ZANJA_B.y, ZANJA_MEDIO, 0.85]],
		"crateres": [[30.0, -45.5, 4.5, 1.1, true], [-9.0, -30.0, 5.5, 1.3, false], [14.0, -52.0, 7.0, 1.7, false],
			[47.0, -55.0, 3.2, 0.75, true], [70.0, -4.0, 6.0, 1.5, false], [16.0, 8.0, 3.5, 0.9, false],
			[78.0, -52.0, 4.0, 1.0, true], [-16.0, -4.0, 3.0, 0.7, true]],
		"aleatorios": 130,
		"libres": libres,
		"llanos": [[0.0, 0.0, 2.4, 4.5], [P_ETAPA.x, P_ETAPA.y, 7.0, 12.0], [P_LOMA.x, P_LOMA.y - 0.4, 2.4, 4.2],
			[P_BALIZA.x, P_BALIZA.y, 1.2, 2.6], [P_MUESTRAS.x + 0.6, P_MUESTRAS.y - 0.5, 1.8, 3.2], [P_FOTO.x, P_FOTO.y, 1.2, 2.6],
			[P_ESPEJO.x, P_ESPEJO.y, 1.0, 2.2], [P_ESTACION.x, P_ESTACION.y, 1.2, 2.4], [P_INSTRUMENTO.x, P_INSTRUMENTO.y, 1.2, 2.4]],
		"cero": Vector2.ZERO,
	})
	_mat_regolito = _material(REGOLITO, {"luz_relieve": RELIEVE_NOCHE, "relieve": 0.95})
	var trozos: int = terreno.montar(self, _mat_regolito)
	print("LUNA terreno trozos=%d triangulos=%d crateres=%d" % [trozos, terreno.triangulos, terreno.crateres.size()])


func _montar_bordes() -> void:
	# LUN-20 (v2f): labio facetado de cada crater. Con celdas de 0,75 m el mapa de alturas no dibuja un borde nitido;
	# este anillo de facetas (cara interior, cresta y falda) lo marca como en el arte de carga: cresta crema al sol,
	# pared interior en sombra violeta. Usa el material del regolito (mismo relieve pintado) y no lleva colision
	var m := Piezas.nueva()
	var cresta := Color("b8bbc6").lerp(Color("f8c991"), 0.4).lerp(Color("d09880"), 0.16).darkened(0.12)
	var pared := Color("b8bbc6").lerp(Color("998385"), 0.45).lerp(Color("516b7c"), 0.08)
	var falda := Color("b8bbc6").lerp(Color("f8c991"), 0.3).lerp(Color("d09880"), 0.15)
	var rng := RandomNumberGenerator.new()
	rng.seed = 77
	var n_bordes := 0
	for c in terreno.crateres:
		var centro := Vector2(float(c[0]), float(c[1]))
		var r: float = c[2]
		if r < 1.5:
			continue
		# fuera de la linea del anillo, de la loma y de la llegada
		if absf(centro.distance_to(P_ETAPA) - R_ANILLO) < r * 1.35 + 0.4 or centro.distance_to(P_ETAPA) < r * 1.35 + 6.0:
			continue
		if centro.distance_to(P_LOMA) < r * 1.35 + 4.5 or centro.length() < r * 1.35 + 4.6:
			continue
		var fresco := bool(c[4])
		var lados := clampi(int(r * 4.5), 12, 28)
		var alto := clampf(r * (0.075 if fresco else 0.05), 0.07, 0.38)
		var anillos: Array = []      # por lado: [dentro, cresta, fuera]
		for k in lados:
			var a := TAU * float(k) / float(lados)
			var dir := Vector2(cos(a), sin(a))
			var j := rng.randf_range(0.94, 1.06)
			var p_in := centro + dir * r * 0.8 * j
			var p_top := centro + dir * r * 1.0 * j
			var p_out := centro + dir * r * (1.32 if fresco else 1.22) * j
			anillos.append([
				_suelo(p_in, -0.04),
				_suelo(p_top, alto * rng.randf_range(0.75, 1.2)),
				_suelo(p_out, -0.04),
			])
		var abajo := Vector3(centro.x, terreno.altura(centro.x, centro.y) - 4.0, centro.y)
		for k in lados:
			var a0: Array = anillos[k]
			var a1: Array = anillos[(k + 1) % lados]
			Piezas.cara(m, [a0[0], a1[0], a1[1]], pared, abajo)
			Piezas.cara(m, [a0[0], a1[1], a0[1]], pared.lerp(cresta, 0.25), abajo)
			Piezas.cara(m, [a0[1], a1[1], a1[2]], cresta, abajo)
			Piezas.cara(m, [a0[1], a1[2], a0[2]], falda, abajo)
		n_bordes += 1
	if n_bordes == 0:
		return
	var mi := MeshInstance3D.new()
	mi.name = "LUN-20_bordes"
	mi.mesh = Piezas.malla(m)
	mi.material_override = _mat_regolito
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.extra_cull_margin = 2.5
	add_child(mi)
	print("LUNA bordes de crater=%d triangulos=%d" % [n_bordes, Piezas.triangulos(m)])


func _montar_rocas() -> void:
	# LUN-02: rocas sueltas en MultiMesh (una por variante) y penascos con colision
	var mallas := _mallas_de("LUN-02")
	if mallas.is_empty():
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = 11
	var por_variante: Array = []
	for i in mallas.size():
		por_variante.append([])
	var puestas := 0
	var intentos := 0
	while puestas < 900 and intentos < 14000:
		intentos += 1
		var x := rng.randf_range(-22.0, 94.0)
		var z := rng.randf_range(-70.0, 22.0)
		if puestas % 3 == 0 and not terreno.crateres.is_empty():
			# una de cada tres, en el borde de un crater: los impactos sacan piedras
			var c: Array = terreno.crateres[rng.randi() % terreno.crateres.size()]
			var ang := rng.randf() * TAU
			var q := float(c[2]) * rng.randf_range(0.95, 1.5)
			x = float(c[0]) + cos(ang) * q
			z = float(c[1]) + sin(ang) * q
		var p := Vector2(x, z)
		if not _lejos_de_lo_importante(p):
			continue
		var tam := lerpf(0.12, 0.95, pow(rng.randf(), 2.2))
		var variante := rng.randi() % mallas.size()
		var base := Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3.ONE * tam)
		por_variante[variante].append(Transform3D(base, _suelo(p, -tam * 0.06)))
		puestas += 1
	for r in PENASCOS:
		var tam: float = r[2]
		var p := Vector2(float(r[0]), float(r[1]))
		var base := Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3.ONE * tam)
		por_variante[int(r[3]) % mallas.size()].append(Transform3D(base, _suelo(p, -0.08 * tam)))
		columna(_suelo(p, -0.3), 0.36 * tam, 1.6)
	for i in mallas.size():
		_multimalla(mallas[i], por_variante[i])


func _montar_piedras() -> void:
	# LUN-10: piedras pequenas por todo el campo (sin sombra: son muchas y pequenas), mas densas junto a los crateres
	var mallas := _mallas_de("LUN-10")
	if mallas.is_empty():
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = 23
	var por_variante: Array = []
	for i in mallas.size():
		por_variante.append([])
	for n in 2600:
		var x := rng.randf_range(-22.0, 94.0)
		var z := rng.randf_range(-70.0, 22.0)
		if n % 2 == 0 and not terreno.crateres.is_empty():
			var c: Array = terreno.crateres[rng.randi() % terreno.crateres.size()]
			var ang := rng.randf() * TAU
			var q := float(c[2]) * rng.randf_range(0.7, 2.2)
			x = float(c[0]) + cos(ang) * q
			z = float(c[1]) + sin(ang) * q
		var p := Vector2(x, z)
		if p.length() < 2.0 or absf(p.distance_to(P_ETAPA) - R_ANILLO) < 0.4:
			continue
		var tam := lerpf(0.05, 0.22, pow(rng.randf(), 1.8))
		var base := Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3(tam, tam * rng.randf_range(0.7, 1.2), tam))
		por_variante[rng.randi() % mallas.size()].append(Transform3D(base, _suelo(p, -0.005)))
	for i in mallas.size():
		_multimalla(mallas[i], por_variante[i], false)


func _montar_eyecta() -> void:
	# LUN-11: bloques de eyecta medio enterrados alrededor de los crateres frescos
	var mallas := _mallas_de("LUN-11")
	if mallas.is_empty():
		return
	var rng := RandomNumberGenerator.new()
	rng.seed = 31
	var por_variante: Array = []
	for i in mallas.size():
		por_variante.append([])
	for c in terreno.crateres:
		if not bool(c[4]):
			continue
		var r: float = c[2]
		var cuantos := int(clampf(r * 2.2, 4.0, 12.0))
		for k in cuantos:
			var ang := rng.randf() * TAU
			var q := r * rng.randf_range(1.0, 1.55)
			var p := Vector2(float(c[0]) + cos(ang) * q, float(c[1]) + sin(ang) * q)
			if not _lejos_de_lo_importante(p, 1.4):
				continue
			var tam := rng.randf_range(0.22, 0.62) * clampf(r / 4.0, 0.6, 1.3)
			var base := Basis(Vector3.UP, rng.randf() * TAU).scaled(Vector3.ONE * tam)
			por_variante[rng.randi() % mallas.size()].append(Transform3D(base, _suelo(p)))
	for i in mallas.size():
		_multimalla(mallas[i], por_variante[i])


func _montar_grandes() -> void:
	# LUN-18: penascos grandes que dan escala y silueta (como la roca de la izquierda del arte de carga)
	var mallas := _mallas_de("LUN-18")
	if mallas.size() < 2:
		return
	var por_variante: Array = [[], []]
	for g in GRANDES:
		var p := Vector2(float(g[0]), float(g[1]))
		var esc: float = g[2]
		var base := Basis(Vector3.UP, deg_to_rad(float(g[4]))).scaled(Vector3.ONE * esc)
		por_variante[int(g[3])].append(Transform3D(base, _suelo(p, -0.12 * esc)))
		columna(_suelo(p, -0.3), (0.95 if int(g[3]) == 0 else 1.15) * esc, 2.4)
	for i in 2:
		_multimalla(mallas[i], por_variante[i])


func _montar_ruta() -> void:
	# LUN-12: balizas de camino en los puntos clave de la ruta, con un destello que corre en orden hacia el objetivo;
	# LUN-05_estaca: estacas cian en el resto de la ruta y alrededor del anillo
	var lista: Array = []
	for i in RUTA.size():
		var p: Vector2 = RUTA[i]
		if BALIZAS_CAMINO.has(i):
			var orden := BALIZAS_CAMINO.find(i)
			var mat := _material(BRILLO, {"energia": 1.4, "pulso": 0.12, "carrera": 1.0, "retraso": float(orden) * 0.85})
			var b := _poner("LUN-12", _suelo(p), float(i) * 37.0, 1.0, mat)
			if b != null:
				for n in b.find_children("*", "MeshInstance3D", true, false):
					(n as MeshInstance3D).extra_cull_margin = 1.5
		else:
			lista.append(Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 1.15), _suelo(p)))
	# doce estacas alrededor del anillo, una cada 30 grados
	for k in 12:
		var ang := TAU * (float(k) + 0.5) / 12.0
		lista.append(Transform3D(Basis.IDENTITY, _suelo(P_ETAPA + Vector2(cos(ang), sin(ang)) * R_ANILLO)))
	var mallas := _mallas_de("LUN-05_estaca")
	if not mallas.is_empty():
		_multimalla(mallas[0], lista, false)


func _montar_zanja() -> void:
	# la zanja: reto de salto. Dos lineas de trazos cian en los labios, en el tramo que cruza la ruta
	var m := Piezas.nueva()
	var eje := (ZANJA_B - ZANJA_A).normalized()
	var normal := eje.orthogonal()
	for lado in [-1.0, 1.0]:
		for k in 7:
			var u := 0.38 + 0.05 * float(k)
			var c: Vector2 = ZANJA_A.lerp(ZANJA_B, u) + normal * float(lado) * (ZANJA_MEDIO * 1.35)
			_cinta(m, c - eje * 0.32, c + eje * 0.32, 0.09, 0.05)
	_nodo_brillo(m, _mat_anillo, "MarcasZanja")


func _montar_llegada() -> void:
	# LUN-04: la caja-capsula de carton, que es la entrada y la salida. Losa despejada de 2 x 2 m con la marca cian
	entrada("inicio", Vector3(0.0, 0.0, 0.0), Vector3(0, 0, 1))
	_poner("LUN-04", _suelo(P_CAJA), 16.0)
	pared(_suelo(P_CAJA, 0.45), Vector3(1.25, 0.9, 0.95), 16.0)
	# la caja trae su luz calida (practica de noche, Biblia de arte 7): rompe el azul de la llegada
	farol(_suelo(P_CAJA, 1.1) + Vector3(0.9, 0.0, 0.5), Color("ffb47a"), 0.55, 5.0)
	var m := Piezas.nueva()
	for sx in [-1.0, 1.0]:
		for sz in [-1.0, 1.0]:
			var e := Vector2(sx, sz)
			_cinta(m, e, e - Vector2(sx * 0.55, 0.0), 0.07, 0.035)
			_cinta(m, e, e - Vector2(0.0, sz * 0.55), 0.07, 0.035)
	_nodo_brillo(m, _mat_anillo, "MarcaLlegada")
	interactuable("Caja", _suelo(P_CAJA), "Volver a casa en la caja", _usar_caja, {"radio": 1.9, "altura_marca": 1.45})


func _montar_baliza() -> void:
	# LUN-05: la baliza cian del final de la pista de saltos
	var encendida := bool(Juego.bandera("luna_baliza"))
	_poner("LUN-05", _suelo(P_BALIZA), 0.0, 1.0, _mat_baliza)
	columna(_suelo(P_BALIZA), 0.22, 1.4)
	_luz_baliza = farol(_suelo(P_BALIZA, 1.3), Color("62e4e0"), 0.0, 6.0)
	if encendida:
		_encender_baliza()
	interactuable("Baliza", _suelo(P_BALIZA), "Encender la baliza", _usar_baliza, {"radio": 1.7, "altura_marca": 1.85})


func _encender_baliza() -> void:
	_mat_baliza.set_shader_parameter("energia", 2.6)
	_mat_baliza.set_shader_parameter("pulso", 0.3)
	_luz_baliza.light_energy = 1.1


func _montar_muestras() -> void:
	# LUN-08 caja de herramientas y LUN-15 soporte con sus bolsas, junto al crater pequeno; tres puntos marcados
	_poner("LUN-08", _suelo(P_HERRAMIENTAS), -24.0, 1.3)
	pared(_suelo(P_HERRAMIENTAS, 0.3), Vector3(0.9, 0.6, 0.5), -24.0)
	_poner("LUN-15", _suelo(P_SOPORTE), 18.0)
	columna(_suelo(P_SOPORTE), 0.5, 1.0)
	var m := Piezas.nueva()
	for p in [Vector2(27.4, -42.6), Vector2(23.4, -41.6), Vector2(28.3, -39.2)]:
		for k in 6:
			var a0 := TAU * float(k) / 6.0
			var a1 := TAU * (float(k) + 0.7) / 6.0
			_cinta(m, p + Vector2(cos(a0), sin(a0)) * 0.42, p + Vector2(cos(a1), sin(a1)) * 0.42, 0.05, 0.04)
	_nodo_brillo(m, _mat_anillo, "MarcasMuestras")
	interactuable("Muestras", _suelo(P_MUESTRAS), "Recoger muestras", _usar_muestras, {"radio": 1.8, "altura_marca": 1.2})


func _montar_anillo() -> void:
	# LUN-03: etapa de descenso generica en el centro del anillo cian de 75 m (18,75 m a escala 1:4)
	_poner("LUN-03", _suelo(P_ETAPA))
	columna(_suelo(P_ETAPA), 4.8, 3.2)
	var m := Piezas.nueva()
	var tramos := 144
	for k in tramos:
		if k % 3 == 2:
			continue     # anillo de trazos: luz tenue
		var a0 := TAU * float(k) / float(tramos)
		var a1 := TAU * float(k + 1) / float(tramos)
		_cinta(m, P_ETAPA + Vector2(cos(a0), sin(a0)) * R_ANILLO, P_ETAPA + Vector2(cos(a1), sin(a1)) * R_ANILLO, 0.2)
	_nodo_brillo(m, _mat_anillo, "Anillo75m")
	# punto de foto: un visor marcado en el suelo, en el borde sur, y la camara de carton (LUN-19) en su tripode
	var visor := Piezas.nueva()
	for sx in [-1.0, 1.0]:
		for sz in [-1.0, 1.0]:
			var e := P_FOTO + Vector2(sx * 0.7, sz * 0.5)
			_cinta(visor, e, e - Vector2(sx * 0.35, 0.0), 0.06, 0.035)
			_cinta(visor, e, e - Vector2(0.0, sz * 0.3), 0.06, 0.035)
	_nodo_brillo(visor, _mat_anillo, "MarcaFoto")
	var p_camara := P_FOTO + Vector2(1.8, 1.4)
	var hacia := (P_FOTO - p_camara).normalized()
	_poner("LUN-19", _suelo(p_camara), rad_to_deg(atan2(-hacia.x, -hacia.y)))
	columna(_suelo(p_camara), 0.22, 1.0)
	interactuable("PuntoFoto", _suelo(P_FOTO), "Tomar la foto", _usar_foto, {"radio": 1.6, "altura_marca": 1.5})
	# las huellas de 1969 alrededor de la etapa: se ven desde fuera, nadie las pisa
	var huella := Piezas.nueva()
	var borde: Array = []
	for k in 8:
		var a := TAU * float(k) / 8.0
		borde.append(Vector3(cos(a) * 0.075, 0.0, sin(a) * 0.17))
	Piezas.cara(huella, borde, Color("6d6880"), Vector3(0, -1, 0))
	var rng := RandomNumberGenerator.new()
	rng.seed = 69
	var lista: Array = []
	var pie := Vector2(P_ETAPA.x, P_ETAPA.y + 5.2)      # al pie de la escalerilla
	for destino in [Vector2(-9.0, 3.5), Vector2(7.5, 6.0), Vector2(11.0, -4.0), Vector2(-5.0, -9.0), Vector2(2.0, 11.5)]:
		var p := pie
		var fin: Vector2 = P_ETAPA + destino
		var lado := 1.0
		var seguro := 0
		while p.distance_to(fin) > 0.5 and seguro < 80:
			seguro += 1
			var dir := (fin - p).normalized().rotated(rng.randf_range(-0.35, 0.35))
			p += dir * 0.45
			lado = -lado
			var q := p + dir.orthogonal() * 0.11 * lado
			var base := Basis(Vector3.UP, atan2(dir.x, dir.y))
			lista.append(Transform3D(base, _suelo(q, 0.02)))
	var mm := _multimalla(Piezas.malla(huella), lista, false)
	mm.mesh.surface_set_material(0, Materiales.compartido("facetado"))


func _montar_loma() -> void:
	# la Loma de las Dos Banderas (ficcion), fuera del anillo. LUN-06 y LUN-07 aparecen al superar el reto
	_marcas_loma = Node3D.new()
	_marcas_loma.name = "MarcasLoma"
	add_child(_marcas_loma)
	var m := Piezas.nueva()
	for x in [X_ASTA_EEUU, X_ASTA_ECUADOR]:
		var p := Vector2(x, Z_ASTAS)
		for k in 8:
			var a0 := TAU * float(k) / 8.0
			var a1 := TAU * (float(k) + 0.6) / 8.0
			_cinta(m, p + Vector2(cos(a0), sin(a0)) * 0.3, p + Vector2(cos(a1), sin(a1)) * 0.3, 0.05, 0.04)
	var marcas := _nodo_brillo(m, _mat_anillo, "Marcas")
	remove_child(marcas)
	_marcas_loma.add_child(marcas)
	var y := maxf(terreno.altura(X_ASTA_EEUU, Z_ASTAS), terreno.altura(X_ASTA_ECUADOR, Z_ASTAS))
	# las dos a la misma altura: Estados Unidos a la izquierda y Ecuador a la derecha, sin taparse
	_banderas = [_poner("LUN-06", Vector3(X_ASTA_EEUU, y, Z_ASTAS)), _poner("LUN-07", Vector3(X_ASTA_ECUADOR, y, Z_ASTAS))]
	interactuable("Banderas", _suelo(P_LOMA), "Plantar las banderas", _usar_banderas, {"radio": 1.9, "altura_marca": 1.3})
	_mostrar_banderas(bool(Juego.bandera("luna_banderas")), false)


func _mostrar_banderas(plantadas: bool, animar: bool) -> void:
	_marcas_loma.visible = not plantadas
	for b in _banderas:
		if b == null:
			continue
		b.visible = plantadas
		if plantadas and animar:
			b.scale = Vector3(1.0, 0.02, 1.0)
			var t := create_tween()
			t.tween_property(b, "scale", Vector3.ONE, 0.7).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	var inter := get_node_or_null("Banderas")
	if inter != null:
		inter.set("texto", "Mirar las banderas" if plantadas else "Plantar las banderas")


func _montar_puntos_de_interes() -> void:
	# tres puntos opcionales, cada uno con su ficha: el espejo (LUN-14), la estacion (LUN-13) y el instrumento (LUN-17)
	_poner("LUN-14", _suelo(P_ESPEJO, 0.02), -12.0, 1.25)
	columna(_suelo(P_ESPEJO), 0.45, 0.6)
	_poner("LUN-13", _suelo(P_ESTACION), -18.0)
	columna(_suelo(P_ESTACION), 0.45, 1.0)
	_poner("LUN-17", _suelo(P_INSTRUMENTO), 22.0)
	columna(_suelo(P_INSTRUMENTO), 0.55, 0.9)
	interactuable("Espejo", _suelo(P_ESPEJO), String(POI["Espejo"]["texto"]), _usar_poi.bind("Espejo"), {"radio": 1.6, "altura_marca": 0.9})
	interactuable("Estacion", _suelo(P_ESTACION), String(POI["Estacion"]["texto"]), _usar_poi.bind("Estacion"), {"radio": 1.6, "altura_marca": 1.4})
	interactuable("Instrumento", _suelo(P_INSTRUMENTO), String(POI["Instrumento"]["texto"]), _usar_poi.bind("Instrumento"), {"radio": 1.7, "altura_marca": 1.2})


func _montar_sueltas() -> void:
	# LUN-16: seis muestras sueltas por el campo, con un destello que las delata; se recogen con E
	var mallas := _mallas_de("LUN-16")
	var destello := Piezas.nueva()
	Piezas.esfera(destello, Vector3.ZERO, 0.055, Color("cef8f5"), 4, 2, Vector3(1.0, 1.7, 1.0))
	var malla_destello := Piezas.malla(destello)
	for i in SUELTAS.size():
		var s: Array = SUELTAS[i]
		if bool(Juego.bandera("luna_suelta_%d" % i)):
			_sueltas.append([null, null, 0.0])
			continue
		var p := Vector2(float(s[0]), float(s[1]))
		var muestra: MeshInstance3D = null
		if not mallas.is_empty():
			muestra = MeshInstance3D.new()
			muestra.mesh = mallas[int(s[2]) % mallas.size()]
			muestra.scale = Vector3.ONE * 1.6
			add_child(muestra)
			muestra.position = _suelo(p, -0.01)
			muestra.rotation.y = float(i) * 1.3
		var chispa := MeshInstance3D.new()
		chispa.mesh = malla_destello
		chispa.material_override = _mat_destello
		chispa.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		add_child(chispa)
		var y0: float = terreno.altura(p.x, p.y) + 0.42
		chispa.position = Vector3(p.x, y0, p.y)
		_sueltas.append([muestra, chispa, y0])
		interactuable("Suelta%d" % (i + 1), _suelo(p), "Recoger la muestra suelta", _usar_suelta.bind(i), {"radio": 1.2, "altura_marca": 0.75})


func _montar_rocas_sueltas() -> void:
	# rocas que se patean: cuerpos rigidos con la gravedad lunar. Capa 3 (valor 4): no frenan a la protagonista
	# ni confunden el suelo de Orbita; chocan con el mundo y entre ellas
	var mallas := _mallas_de("LUN-02")
	if mallas.is_empty():
		return
	var g_proyecto := float(ProjectSettings.get_setting("physics/3d/default_gravity", 9.8))
	var friccion := PhysicsMaterial.new()
	friccion.friction = 0.9
	friccion.bounce = 0.18
	for i in ROCAS_SUELTAS.size():
		var r: Array = ROCAS_SUELTAS[i]
		var tam: float = r[2]
		var malla: Mesh = mallas[(i * 3) % mallas.size()]
		var cuerpo := RigidBody3D.new()
		cuerpo.name = "RocaSuelta%d" % i
		cuerpo.collision_layer = 4
		cuerpo.collision_mask = 1 | 4
		cuerpo.gravity_scale = 1.624 / g_proyecto
		cuerpo.mass = 4.0 * tam
		cuerpo.angular_damp = 0.6
		cuerpo.physics_material_override = friccion
		cuerpo.can_sleep = true
		var puntos := PackedVector3Array()
		for v in malla.surface_get_arrays(0)[Mesh.ARRAY_VERTEX]:
			puntos.append(v * tam)
		var forma := ConvexPolygonShape3D.new()
		forma.points = puntos
		var cs := CollisionShape3D.new()
		cs.shape = forma
		cuerpo.add_child(cs)
		var mi := MeshInstance3D.new()
		mi.mesh = malla
		mi.scale = Vector3.ONE * tam
		cuerpo.add_child(mi)
		add_child(cuerpo)
		cuerpo.position = _suelo(Vector2(float(r[0]), float(r[1])), 0.04)
		cuerpo.rotation.y = float(i) * 0.9
		_rocas.append(cuerpo)


func _montar_huellas() -> void:
	# las huellas que ella y Orbita van dejando: dos MultiMesh que se llenan al caminar y duran toda la visita.
	# Bota: borde claro de regolito apretado, suela violeta y cuatro barras de la suela
	var bota := Piezas.nueva()
	var borde: Array = []
	var dentro: Array = []
	for k in 10:
		var a := TAU * float(k) / 10.0
		borde.append(Vector3(cos(a) * 0.07, 0.0, sin(a) * 0.145))
		dentro.append(Vector3(cos(a) * 0.052, 0.004, sin(a) * 0.122))
	Piezas.cara(bota, borde, Color("cfc6c6"), Vector3(0, -1, 0))
	Piezas.cara(bota, dentro, Color("6f6a86"), Vector3(0, -1, 0))
	for k in 4:
		var z := -0.085 + 0.057 * float(k)
		Piezas.cara(bota, [Vector3(-0.04, 0.008, z), Vector3(0.04, 0.008, z), Vector3(0.04, 0.008, z + 0.022), Vector3(-0.04, 0.008, z + 0.022)], Color("9a94a8"), Vector3(0, -1, z))
	_huellas = _multimalla(Piezas.malla(bota), [], false, 900)
	_huellas.mesh.surface_set_material(0, Materiales.compartido("facetado"))
	var pata := Piezas.nueva()
	for d in [Vector3(-0.035, 0, 0), Vector3(0.035, 0, 0)]:
		var puntos: Array = []
		for k in 6:
			var a := TAU * float(k) / 6.0
			puntos.append(d + Vector3(cos(a) * 0.017, 0.0, sin(a) * 0.015))
		Piezas.cara(pata, puntos, Color("6f6a86"), d + Vector3(0, -1, 0))
		for dedo in [Vector3(-0.014, 0, 0.024), Vector3(0.0, 0, 0.03), Vector3(0.014, 0, 0.024)]:
			var c: Vector3 = d + dedo
			Piezas.cara(pata, [c + Vector3(-0.006, 0, -0.005), c + Vector3(0.006, 0, -0.005), c + Vector3(0.0, 0, 0.007)], Color("6f6a86"), c + Vector3(0, -1, 0))
	_patas = _multimalla(Piezas.malla(pata), [], false, 700)
	_patas.mesh.surface_set_material(0, Materiales.compartido("facetado"))


func _montar_polvo() -> void:
	# polvo de regolito: tetraedros pequenos en un solo MultiMesh. Vuela en parabolas (no hay aire) y se posa
	var m := Piezas.nueva()
	var a := Vector3(0.0, 0.62, 0.0)
	var b := Vector3(-0.5, -0.3, 0.38)
	var c := Vector3(0.5, -0.3, 0.38)
	var d := Vector3(0.0, -0.3, -0.58)
	var centro := (a + b + c + d) * 0.25
	var color := Color("cdc4c4")
	for cara in [[a, b, c], [a, c, d], [a, d, b], [b, d, c]]:
		Piezas.cara(m, cara, color, centro)
	_p_pos.resize(POLVO_MAX)
	_p_vel.resize(POLVO_MAX)
	_p_vida.resize(POLVO_MAX)
	_p_max.resize(POLVO_MAX)
	_p_tam.resize(POLVO_MAX)
	var ceros: Array = []
	for i in POLVO_MAX:
		ceros.append(Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 0.0001), Vector3(0, -50, 0)))
		_p_max[i] = 0.0
	_polvo = _multimalla(Piezas.malla(m), ceros, false)
	_polvo.mesh.surface_set_material(0, Materiales.compartido("facetado"))


func _montar_vineta() -> void:
	# vineta suave del sueno, debajo de la interfaz (capa 10)
	var capa := CanvasLayer.new()
	capa.name = "VinetaSueno"
	capa.layer = 1
	add_child(capa)
	var rect := ColorRect.new()
	rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_mat_vineta = ShaderMaterial.new()
	_mat_vineta.shader = VINETA
	rect.material = _mat_vineta
	capa.add_child(rect)


# ------------------------------------------------------------------ polvo

func _polvo_emitir(p: Vector3, cuantas: int, fuerza: float, arriba: float, dir: Vector3 = Vector3.ZERO) -> void:
	if _polvo == null:
		return
	for k in cuantas:
		var i := _p_sig
		_p_sig = (_p_sig + 1) % POLVO_MAX
		var ang := randf() * TAU
		var h := Vector3(cos(ang), 0.0, sin(ang)) * fuerza * randf_range(0.35, 1.0) + dir * randf_range(0.5, 1.0)
		var vy := arriba * randf_range(0.45, 1.0)
		_p_pos[i] = p + Vector3(randf_range(-0.12, 0.12), 0.04, randf_range(-0.12, 0.12))
		_p_vel[i] = Vector3(h.x, vy, h.z)
		_p_vida[i] = 0.0
		# vuelo balistico: sube y baja en 2·vy/g; se posa un momento y se apaga
		_p_max[i] = clampf(2.0 * vy / gravedad, 0.25, 2.2) + 0.5
		_p_tam[i] = randf_range(0.025, 0.06)
	_p_vivas = POLVO_MAX


func _polvo_paso(delta: float) -> void:
	if _p_vivas <= 0 or _polvo == null:
		return
	var vivas := 0
	for i in POLVO_MAX:
		if _p_max[i] <= 0.0:
			continue
		_p_vida[i] += delta
		if _p_vida[i] >= _p_max[i]:
			_p_max[i] = 0.0
			_polvo.set_instance_transform(i, Transform3D(Basis.IDENTITY.scaled(Vector3.ONE * 0.0001), Vector3(0, -50, 0)))
			continue
		vivas += 1
		var v := _p_vel[i]
		var p := _p_pos[i]
		v.y -= gravedad * delta
		p += v * delta
		var suelo := float(terreno.altura(p.x, p.z)) + 0.02
		if p.y < suelo:
			p.y = suelo
			v = Vector3.ZERO
		_p_vel[i] = v
		_p_pos[i] = p
		var k := 1.0 - smoothstep(_p_max[i] - 0.45, _p_max[i], _p_vida[i])
		var giro := Basis(Vector3(0.3, 1.0, 0.2).normalized(), _p_vida[i] * 6.0 + float(i))
		_polvo.set_instance_transform(i, Transform3D(giro.scaled(Vector3.ONE * _p_tam[i] * k), p))
	_p_vivas = vivas


# ------------------------------------------------------------------ cada cuadro

func _marcar(mm: MultiMesh, cuenta: int, p: Vector3, hacia: Vector3) -> void:
	var n: Vector3 = terreno.normal(p.x, p.z)
	var adelante := (hacia - n * hacia.dot(n)).normalized()
	if adelante.length() < 0.5:
		adelante = Vector3(0, 0, 1)
	var base := Basis(n.cross(adelante).normalized(), n, adelante)
	var pos := Vector3(p.x, terreno.altura(p.x, p.z) + 0.022, p.z)
	mm.set_instance_transform(cuenta % mm.instance_count, Transform3D(base, pos))
	mm.visible_instance_count = mini(cuenta + 1, mm.instance_count)


func _process(delta: float) -> void:
	_t += delta
	_polvo_paso(delta)
	# destellos de las muestras sueltas: suben, bajan y giran
	for i in _sueltas.size():
		var chispa: Variant = _sueltas[i][1]
		if chispa != null and is_instance_valid(chispa):
			chispa.position.y = float(_sueltas[i][2]) + 0.07 * sin(_t * 2.4 + float(i))
			chispa.rotation.y = _t * 2.0 + float(i)
	var j: CharacterBody3D = Zonas.jugador
	if j == null or not is_instance_valid(j) or Zonas.actual != self:
		return
	var p := j.global_position
	# huellas de ella (solo cuando pisa) y de Orbita
	if j.is_on_floor() and _ultima_huella.distance_to(p) > 0.44:
		var mira: Vector3 = j.mirando
		_pie = -_pie
		_marcar(_huellas, _n_huellas, p + Vector3(mira.z, 0.0, -mira.x) * 0.08 * _pie, mira)
		_n_huellas += 1
		_ultima_huella = p
		if _n_huellas % 2 == 0:
			Audio.sonar("paso_luna", -6.0)
		if j.velocity.length() > 1.0:
			_polvo_emitir(p, 1, 0.25, 0.5, -j.velocity.normalized() * 0.2)
	var gato: Node3D = Zonas.companero
	if gato != null and is_instance_valid(gato) and gato.visible:
		var g := gato.global_position
		if _ultima_pata.distance_to(g) > 0.26:
			var d := g - _ultima_pata if _ultima_pata != Vector3.INF else Vector3(0, 0, 1)
			d.y = 0.0
			_marcar(_patas, _n_patas, g, d.normalized() if d.length() > 0.01 else Vector3(0, 0, 1))
			_n_patas += 1
			_ultima_pata = g
		# el casco de Orbita acompana a su cabeza (el gato mira hacia donde gira su pivote)
		if _casco_o != null and is_instance_valid(_casco_o):
			var pivote: Variant = gato.get("_pivote")
			var giro: float = (pivote as Node3D).rotation.y if pivote is Node3D else 0.0
			_casco_o.position = Basis(Vector3.UP, giro) * Vector3(0.0, 0.37, 0.15)
	# el anillo reacciona al acercarse: respira mas fuerte cuanto mas cerca
	var d_etapa := Vector2(p.x - P_ETAPA.x, p.z - P_ETAPA.y).length()
	var w_anillo := 1.0 - smoothstep(R_ANILLO + 0.5, R_ANILLO + 9.0, d_etapa)
	_mat_anillo.set_shader_parameter("energia", 0.85 + 0.45 * w_anillo)
	_mat_anillo.set_shader_parameter("pulso", 0.18 + 0.3 * w_anillo)
	if not _anillo_avisado and d_etapa < R_ANILLO + 4.0:
		_anillo_avisado = true
		Audio.sonar("radio")
		Interfaz.aviso("Órbita: «Ese anillo cian marca 75 m. Se mira, no se pisa.»", 4.0)
	# cerca del anillo la camara se abre sola: se ven ella y la etapa de descenso
	var cam: Camera3D = Zonas.camara
	if cam == null:
		return
	var etapa := Vector3(P_ETAPA.x, p.y, P_ETAPA.y)
	var w := 1.0 - smoothstep(R_ANILLO + 2.0, R_ANILLO + 10.0, d_etapa)
	if w > 0.001:
		if not _panorama:
			_panorama = true
			_encuadre_jugador = float(cam.get("encuadre"))
		_foco.global_position = p.lerp(etapa, 0.4 * w)
		cam.set("objetivo", _foco)
		cam.set("encuadre", lerpf(_encuadre_jugador, ENCUADRE_PANORAMA, w))
	elif _panorama:
		_panorama = false
		cam.set("objetivo", j)
		cam.set("encuadre", _encuadre_jugador)


func _physics_process(delta: float) -> void:
	var j: CharacterBody3D = Zonas.jugador
	if j == null or not is_instance_valid(j) or Zonas.actual != self:
		return
	var p := j.global_position
	_saltos(j, delta)
	_patear(j)
	# el anillo de 75 m: se mira, no se pisa. Ella se detiene sola y Orbita explica por que
	if _fuera_de_circulo(j, P_ETAPA, R_ANILLO + MARGEN_ANILLO):
		_avisar("anillo")
	if _libre:
		return
	# cada area se abre cuando la anterior esta hecha: mensajes de Orbita, no muros
	if not bool(Juego.bandera("luna_baliza")) and p.x > PUERTA_A:
		_frenar_en_x(j, PUERTA_A)
		_avisar("baliza")
	elif not bool(Juego.bandera("luna_muestras")) and p.x > PUERTA_B:
		_frenar_en_x(j, PUERTA_B)
		_avisar("muestras")
	if not bool(Juego.bandera("luna_foto")) and _fuera_de_circulo(j, P_LOMA, R_PUERTA_LOMA):
		_avisar("loma")


func _saltos(j: CharacterBody3D, delta: float) -> void:
	# salto lunar: polvo al despegar y al caer, distancia medida y el reto de cruzar la zanja de un salto
	var en_suelo := j.is_on_floor()
	var p := j.global_position
	if _en_suelo_antes and not en_suelo and j.velocity.y > 0.8:
		_despegue = p
		_t_aire = 0.0
		_polvo_emitir(p, 6, 0.8, 0.9)     # el sonido «salto» lo pone nucleo/jugador.gd
	if not en_suelo:
		_t_aire += delta
	elif not _en_suelo_antes:
		if _t_aire > 0.35:
			var caida := clampf(_t_aire, 0.4, 2.8)
			_polvo_emitir(p, 8 + int(caida * 3.0), 0.6 + caida * 0.35, 0.5 + caida * 0.25)
			Audio.sonar("paso_luna", 1.0)
			if _despegue != Vector3.INF:
				_medir_salto(_despegue, p)
		_despegue = Vector3.INF
		_t_aire = 0.0
	_en_suelo_antes = en_suelo


func _lado_zanja(p: Vector2) -> Vector2:
	# x: posicion a lo largo del eje (0..1); y: distancia con signo al eje en metros
	var eje := ZANJA_B - ZANJA_A
	var u := (p - ZANJA_A).dot(eje) / eje.length_squared()
	var s := eje.normalized().cross(p - ZANJA_A)
	return Vector2(u, s)


func _medir_salto(desde: Vector3, hasta: Vector3) -> void:
	var largo := Vector2(hasta.x - desde.x, hasta.z - desde.z).length()
	var a := _lado_zanja(Vector2(desde.x, desde.z))
	var b := _lado_zanja(Vector2(hasta.x, hasta.z))
	var zanja := a.y * b.y < 0.0 and absf(a.y) > ZANJA_MEDIO * 1.05 and absf(b.y) > ZANJA_MEDIO * 1.05 \
		and a.x > 0.0 and a.x < 1.0 and b.x > 0.0 and b.x < 1.0
	if zanja:
		_celebrar_zanja(largo)
		return
	if largo < 3.0:
		return
	var ahora := Time.get_ticks_msec()
	var texto := "Salto lunar: %s m" % _cifra(largo)
	if largo > _record:
		_record = largo
		Juego.poner_bandera("luna_record_salto", snappedf(largo, 0.1))
		texto += " · ¡récord!"
	elif ahora - _ultimo_salto_aviso < 2500:
		return
	_ultimo_salto_aviso = ahora
	Interfaz.aviso(texto, 2.2)
	if not bool(Juego.bandera("luna_salto_explicado")):
		Juego.poner_bandera("luna_salto_explicado")
		Juego.anotar("gravedad_lunar")
		Interfaz.aviso("Órbita: «Con el mismo impulso, en la Tierra saltarías unas seis veces menos: aquí la gravedad es la sexta parte.»", 5.0)


func _celebrar_zanja(largo: float) -> void:
	Audio.sonar("logro")
	if largo > _record:
		_record = largo
		Juego.poner_bandera("luna_record_salto", snappedf(largo, 0.1))
	if bool(Juego.bandera("luna_zanja_saltada")) or _hablando or Interfaz.ocupada():
		Interfaz.aviso("¡La zanja de un salto! %s m" % _cifra(largo), 2.5)
		return
	Juego.poner_bandera("luna_zanja_saltada")
	Juego.anotar("gravedad_lunar")
	_hablando = true
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "¡Cruzaste la zanja de un salto! %s m sin tocar el fondo." % _cifra(largo)},
		{"quien": "Órbita", "texto": "Con 1,624 m/s² el vuelo dura mucho más. En la Tierra, ese mismo salto no pasaría del borde."},
	])
	_hablando = false


func _cifra(x: float) -> String:
	return ("%.1f" % x).replace(".", ",")


func _patear(j: CharacterBody3D) -> void:
	# una roca suelta sale despedida si ella le pasa por encima con impulso: en la Luna rueda y vuela lejos
	var plana := Vector3(j.velocity.x, 0.0, j.velocity.z)
	if plana.length() < 0.6:
		return
	var ahora := Time.get_ticks_msec()
	for roca in _rocas:
		if not is_instance_valid(roca):
			continue
		var d := roca.global_position - j.global_position
		d.y = 0.0
		if d.length() > 0.62 or plana.dot(d) < 0.0:
			continue
		if ahora - int(_patada.get(roca.name, -9999)) < 600:
			continue
		_patada[roca.name] = ahora
		var dir := (plana.normalized() * 0.8 + d.normalized() * 0.2).normalized()
		var fuerza := clampf(plana.length(), 1.0, 4.5)
		roca.sleeping = false
		roca.apply_central_impulse((dir * fuerza * 1.1 + Vector3.UP * 1.3) * roca.mass)
		roca.apply_torque_impulse(Vector3(randf_range(-1, 1), randf_range(-1, 1), randf_range(-1, 1)) * roca.mass * 0.2)
		_polvo_emitir(roca.global_position, 5, 0.6, 0.8, dir * 0.6)
		Audio.sonar("paso_luna", 2.0)


func _fuera_de_circulo(j: CharacterBody3D, centro: Vector2, radio: float) -> bool:
	# si ella esta dentro del circulo, la deja en el borde y le quita la velocidad hacia dentro
	var d := Vector2(j.global_position.x - centro.x, j.global_position.z - centro.y)
	if d.length() >= radio:
		return false
	var n := d.normalized() if d.length() > 0.001 else Vector2(0, 1)
	var borde := centro + n * radio
	j.global_position.x = borde.x
	j.global_position.z = borde.y
	var hacia_dentro := j.velocity.x * n.x + j.velocity.z * n.y
	if hacia_dentro < 0.0:
		j.velocity.x -= hacia_dentro * n.x
		j.velocity.z -= hacia_dentro * n.y
	return true


func _frenar_en_x(j: CharacterBody3D, limite: float) -> void:
	j.global_position.x = limite
	if j.velocity.x > 0.0:
		j.velocity.x = 0.0


func _avisar(cual: String) -> void:
	if _hablando or Interfaz.ocupada():
		return
	var ahora := Time.get_ticks_msec()
	if ahora - int(_ultimo_aviso.get(cual, -99999)) < 7000:
		return
	_ultimo_aviso[cual] = ahora
	var primera := not _avisos_dados.has(cual)
	if cual == "anillo":
		primera = not bool(Juego.bandera("luna_anillo_visto"))
		Juego.poner_bandera("luna_anillo_visto")
		Juego.anotar("zona_75_m")
	_avisos_dados[cual] = true
	if primera:
		_hablando = true
		Audio.sonar("radio")
		await Interfaz.decir(MENSAJES[cual])
		_hablando = false
	else:
		Interfaz.aviso(String(CORTOS[cual]), 3.5)


# ------------------------------------------------------------------ entrar y salir

func al_entrar(_nombre_entrada: String) -> void:
	_poner_cascos()
	if Audio.has_method("ambiente"):
		Audio.call("ambiente", "luna")
	var demo := String(Juego.args.get("luna_demo", ""))
	if demo != "":
		# tomas de evidencia: --luna_demo=foto (la foto con su marco), alba (amanecer en la loma) o polvo
		await get_tree().create_timer(1.3).timeout
		if demo == "foto":
			await _foto()
		elif demo == "alba":
			_mostrar_banderas(true, false)
			_luz_alba(1.0)
		elif demo == "polvo" and Zonas.jugador != null:
			var pj: Vector3 = Zonas.jugador.global_position
			_polvo_emitir(pj + Vector3(0.0, 0.0, -0.4), 18, 1.4, 1.2)
			for roca in _rocas:
				if roca.global_position.distance_to(pj) < 6.0:
					roca.apply_central_impulse((Vector3(0.6, 1.0, -0.8)) * roca.mass * 1.6)
		return
	if not bool(Juego.bandera("luna_llegada")):
		Juego.poner_bandera("luna_llegada")
		Juego.anotar("mar_tranquilidad")
		Audio.sonar("radio")
		await Interfaz.decir(LLEGADA)


func al_salir() -> void:
	for casco in [_casco_j, _casco_o]:
		if casco != null and is_instance_valid(casco):
			casco.queue_free()
	_casco_j = null
	_casco_o = null
	var cam: Camera3D = Zonas.camara
	if cam != null and is_instance_valid(cam) and Zonas.jugador != null and is_instance_valid(Zonas.jugador):
		cam.set("objetivo", Zonas.jugador)
		if _panorama:
			cam.set("encuadre", _encuadre_jugador)


func despertar() -> void:
	# la usa el menu de pausa: en el sueno siempre se puede despertar
	Zonas.ir_a("habitacion", "cama")


func _poner_cascos() -> void:
	# LUN-09: un casco de burbuja para ella y otro, mas pequeno, para Orbita
	if _casco_j == null or not is_instance_valid(_casco_j):
		_casco_j = _casco_nuevo()
		if _casco_j != null and Zonas.jugador != null:
			Zonas.jugador.add_child(_casco_j)
			_casco_j.position = Vector3(0.0, 0.87, 0.0)
	if _casco_o == null or not is_instance_valid(_casco_o):
		_casco_o = _casco_nuevo()
		if _casco_o != null and Zonas.companero != null:
			Zonas.companero.add_child(_casco_o)
			_casco_o.scale = Vector3.ONE * 0.62
			_casco_o.position = Vector3(0.0, 0.37, 0.15)


func _casco_nuevo() -> Node3D:
	var nodo := Recursos.instancia(MODELOS + "LUN-09.glb")
	if nodo == null:
		push_warning("AVISO falta el modelo LUN-09")
		return null
	nodo.name = "CascoDeBurbuja"
	_arreglar_materiales(nodo)
	for n in nodo.find_children("*", "MeshInstance3D", true, false):
		(n as MeshInstance3D).cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return nodo


# ------------------------------------------------------------------ luz del amanecer

func _luz_alba(k: float) -> void:
	# 0 = noche lunar bajo la luz de la Tierra; 1 = el Sol entra rasante y calido, con sombras largas
	_sol.light_color = NOCHE_SOL.lerp(ALBA_SOL, k)
	_sol.light_energy = lerpf(NOCHE_ENERGIA, 1.35, k)
	_sol.look_at_from_position(Vector3.ZERO, DIR_NOCHE.lerp(DIR_ALBA, k).normalized(), Vector3.UP)
	_entorno.ambient_light_color = NOCHE_AMB.lerp(ALBA_AMB, k)
	_entorno.adjustment_contrast = lerpf(CONTRASTE_NOCHE, 1.12, k)
	_mat_regolito.set_shader_parameter("luz_relieve", RELIEVE_NOCHE.lerp(RELIEVE_ALBA, k).normalized())
	_mat_regolito.set_shader_parameter("calidez", k * 0.8)
	if _mat_vineta != null:
		_mat_vineta.set_shader_parameter("calidez", k)


func _amanecer() -> void:
	# sube la luz calida unos segundos y se queda en un alba suave
	var silencio := not Juego.args.has("prueba")
	var t := create_tween()
	t.tween_method(_luz_alba, 0.0, 1.0, 3.5).set_trans(Tween.TRANS_SINE)
	t.tween_interval(6.0)
	if silencio:
		# unos segundos en silencio, sin interfaz
		Interfaz.mostrar_hud(false)
		t.tween_callback(func() -> void: Interfaz.mostrar_hud(true))
	t.tween_method(_luz_alba, 1.0, 0.3, 4.0).set_trans(Tween.TRANS_SINE)


# ------------------------------------------------------------------ interacciones

func _usar_baliza() -> void:
	if bool(Juego.bandera("luna_baliza")):
		Audio.sonar("radio")
		await Interfaz.decir([{"quien": "Órbita", "texto": "La baliza sigue encendida. Con ella siempre sabremos volver a la caja."}])
		return
	_encender_baliza()
	Audio.sonar("logro")
	_polvo_emitir(_suelo(P_BALIZA), 10, 1.0, 0.9)
	Juego.poner_bandera("luna_baliza")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Baliza encendida. Llegaste a saltos, como se camina cuando pesas la sexta parte."},
		{"quien": "Órbita", "texto": "Con ella ya sabemos volver a la caja. Ahora sigue las balizas: el campo de muestras está junto al cráter pequeño."},
	])


func _usar_muestras() -> void:
	if not _libre and not bool(Juego.bandera("luna_baliza")):
		await Interfaz.decir(MENSAJES["baliza"])
		return
	Audio.sonar("radio")
	if not bool(Juego.bandera("luna_muestras")):
		Juego.anotar("regolito")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "Esto que pisas es regolito: polvo y escombros de roca que dejaron los impactos durante miles de millones de años."},
			{"quien": "Órbita", "texto": "En la caja hay cucharón, pinzas y tubo de núcleo. Cada muestra pide su herramienta."},
		])
	var r: Dictionary = await Interfaz.abrir_minijuego("muestras", {"dificultad": 1})
	if not r.get("superado", false):
		await Interfaz.decir([{"quien": "Órbita", "texto": "No pasa nada: la muestra se conserva. Probamos otra vez cuando quieras."}])
		return
	if bool(Juego.bandera("luna_muestras")):
		return
	Juego.poner_bandera("luna_muestras")
	if Zonas.jugador != null:
		Zonas.jugador.reproducir("recoger")
	Audio.sonar("recoger")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Cada muestra en su bolsa y con su lugar anotado. Así una roca sirve para algo."},
		{"quien": "Órbita", "texto": "Ahora sigue las balizas hasta el anillo cian. Hay algo que quiero que veas."},
	])


func _usar_suelta(i: int) -> void:
	# una muestra suelta: se recoge con E, se guarda en su bolsa (bandera) y se anota en el cuaderno al final
	if bool(Juego.bandera("luna_suelta_%d" % i)):
		return
	Juego.poner_bandera("luna_suelta_%d" % i)
	Audio.sonar("recoger")
	var datos: Array = _sueltas[i]
	_sueltas[i] = [null, null, 0.0]          # _process ya no las toca: se liberan al final del tween
	var p := Vector3(float(SUELTAS[i][0]), 0.0, float(SUELTAS[i][1]))
	p.y = terreno.altura(p.x, p.z)
	_polvo_emitir(p, 6, 0.5, 0.7)
	for nodo in [datos[0], datos[1]]:
		if nodo != null and is_instance_valid(nodo):
			var t := create_tween()
			t.tween_property(nodo, "scale", Vector3.ONE * 0.01, 0.25)
			t.tween_callback(nodo.queue_free)
	# el interactuable no se libera: su corrutina usar() sigue esperando esta funcion. Se apaga y ya
	var yo := get_node_or_null("Suelta%d" % (i + 1))
	if yo != null:
		yo.set("habilitado", false)
	if Zonas.jugador != null:
		Zonas.jugador.reproducir("recoger")
	var n := 0
	for k in SUELTAS.size():
		if bool(Juego.bandera("luna_suelta_%d" % k)):
			n += 1
	Interfaz.aviso("Muestra suelta en su bolsa: %d de %d" % [n, SUELTAS.size()], 2.5)
	if n == 1:
		await Interfaz.decir([{"quien": "Órbita", "texto": "Muestra suelta. Va en una bolsa con número, ligada a su registro: así sabremos de dónde salió."}])
	elif n == SUELTAS.size():
		Juego.anotar("bolsas_numeradas")
		Audio.sonar("logro")
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "¡Las seis! Cada una en su bolsa y con su lugar anotado."},
			{"quien": "Órbita", "texto": "Al despertar no traerás rocas: traerás las páginas del cuaderno. Eso pesa cero y vale mucho."},
		])


func _usar_poi(cual: String) -> void:
	var poi: Dictionary = POI[cual]
	Audio.sonar("radio")
	var primera := not bool(Juego.bandera(String(poi["bandera"])))
	if primera:
		Juego.poner_bandera(String(poi["bandera"]))
		Juego.anotar(String(poi["ficha"]))
	await Interfaz.decir(poi["lineas"])
	if primera:
		var n := 0
		for clave in POI:
			if bool(Juego.bandera(String(POI[clave]["bandera"]))):
				n += 1
		Audio.sonar("logro")
		Interfaz.aviso("Punto de interés %d de %d · ficha nueva en el cuaderno" % [n, POI.size()], 3.0)


func _usar_foto() -> void:
	if not _libre and not bool(Juego.bandera("luna_muestras")):
		await Interfaz.decir(MENSAJES["muestras"])
		return
	Audio.sonar("radio")
	var primera := not bool(Juego.bandera("luna_foto"))
	if primera:
		await Interfaz.decir([
			{"quien": "Órbita", "texto": "Ahí está la etapa de descenso. Sirvió de plataforma de lanzamiento y se quedó en la Luna, con su placa conmemorativa."},
			{"quien": "Órbita", "texto": "La bandera llevaba una barra horizontal para sostenerse sin viento. Según Aldrin, el despegue la derribó: se presume que ya no está en pie."},
			{"quien": "Órbita", "texto": "El disco del Apolo 11 llevó mensajes de 73 países. El de Ecuador viajó hasta aquí."},
			{"quien": "Órbita", "texto": "Mi cámara de cartón ya está lista. Ponte derecha. Mira a la cámara… ¡ya!"},
		])
	await _foto()
	if not primera:
		return
	Juego.poner_bandera("luna_foto")
	Juego.anotar("etapa_descenso")
	Juego.anotar("zona_75_m")
	Juego.anotar("tierra_en_cielo_lunar")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Foto guardada: tú, yo y la etapa de descenso al fondo."},
		{"quien": "Órbita", "texto": "La Tierra queda arriba, casi en el mismo punto del cielo. No cabe en la foto, pero nos está alumbrando."},
		{"quien": "Órbita", "texto": "Ahora, la loma. Está fuera del anillo, sin huellas que borrar."},
	])


func _foto() -> void:
	# un destello y un marco con la imagen congelada 2 s
	var j: CharacterBody3D = Zonas.jugador
	if j != null:
		j.set("mirando", Vector3(0, 0, 1))
	var corta := Juego.args.has("prueba")
	var imagen: Image = null
	if DisplayServer.get_name() != "headless":
		Interfaz.mostrar_hud(false)
		await get_tree().process_frame
		await get_tree().process_frame
		await RenderingServer.frame_post_draw
		imagen = get_viewport().get_texture().get_image()
		Interfaz.mostrar_hud(true)
	Audio.sonar("logro")
	var capa := CanvasLayer.new()
	capa.name = "Foto"
	capa.layer = 30
	add_child(capa)
	var raiz := Control.new()
	raiz.set_anchors_preset(Control.PRESET_FULL_RECT)
	raiz.mouse_filter = Control.MOUSE_FILTER_IGNORE
	capa.add_child(raiz)
	if imagen != null and not imagen.is_empty():
		var tam := Vector2(imagen.get_size()) * 0.62
		imagen.resize(int(tam.x), int(tam.y), Image.INTERPOLATE_BILINEAR)
		var centro := CenterContainer.new()
		centro.set_anchors_preset(Control.PRESET_FULL_RECT)
		centro.mouse_filter = Control.MOUSE_FILTER_IGNORE
		raiz.add_child(centro)
		var marco := Estilo.panel(Estilo.PAPEL, 6, 3, 14)
		marco.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var columna_foto := VBoxContainer.new()
		columna_foto.add_theme_constant_override("separation", 8)
		marco.add_child(columna_foto)
		var cuadro := TextureRect.new()
		cuadro.texture = ImageTexture.create_from_image(imagen)
		cuadro.custom_minimum_size = tam
		cuadro.stretch_mode = TextureRect.STRETCH_SCALE
		columna_foto.add_child(cuadro)
		var pie := Estilo.linea("Mirar sin borrar · Mar de la Tranquilidad", 20, Estilo.TINTA_SUAVE)
		pie.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		columna_foto.add_child(pie)
		centro.add_child(marco)
		marco.pivot_offset = (tam + Vector2(28, 60)) * 0.5
		marco.rotation = deg_to_rad(-2.0)
	var destello := ColorRect.new()
	destello.color = Color("cef8f5")
	destello.set_anchors_preset(Control.PRESET_FULL_RECT)
	destello.mouse_filter = Control.MOUSE_FILTER_IGNORE
	raiz.add_child(destello)
	var t := create_tween()
	t.tween_property(destello, "modulate:a", 0.0, 0.45)
	await get_tree().create_timer(0.1 if corta else 2.4).timeout
	var fin := create_tween()
	fin.tween_property(raiz, "modulate:a", 0.0, 0.05 if corta else 0.35)
	await fin.finished
	capa.queue_free()


func _usar_banderas() -> void:
	Audio.sonar("radio")
	if bool(Juego.bandera("luna_banderas")):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Ahí siguen, juntas y a la misma altura. Representan nuestros sueños. No nos hacen dueños."}])
		return
	if not _libre and not bool(Juego.bandera("luna_foto")):
		await Interfaz.decir(MENSAJES["loma"])
		return
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Esta loma queda fuera del anillo: aquí no borramos ninguna huella."},
		{"quien": "Órbita", "texto": "Dos banderas, la de Estados Unidos y la de Ecuador. Aquí no hay viento: cada una necesita su barra horizontal."},
	])
	var r: Dictionary = await Interfaz.abrir_minijuego("banderas", {"dificultad": 1})
	if not r.get("superado", false):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Todavía no quedan parejas. Sin prisa: lo intentamos de nuevo cuando quieras."}])
		return
	Juego.poner_bandera("luna_banderas")
	_mostrar_banderas(true, true)
	# dos golpes de mastil, con su polvo, y luego el logro
	for x in [X_ASTA_EEUU, X_ASTA_ECUADOR]:
		Audio.sonar("golpe_mastil")
		_polvo_emitir(Vector3(x, terreno.altura(x, Z_ASTAS), Z_ASTAS), 8, 0.7, 0.9)
		await get_tree().create_timer(0.35).timeout
	Audio.sonar("logro")
	if Zonas.jugador != null:
		Zonas.jugador.reproducir("celebrar")
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Juntas y a la misma altura. Representan nuestros sueños. No nos hacen dueños."},
		{"quien": "Órbita", "texto": "El artículo II del Tratado del Espacio prohíbe que un país se apropie de la Luna. Una bandera no da territorio."},
		{"quien": "Órbita", "texto": "Mira: en el sueño amanece cuando tú quieres. En la Luna de verdad, esta noche seguiría. Después, volvemos a la caja."},
	])
	_amanecer()


func _usar_caja() -> void:
	Audio.sonar("radio")
	if bool(Juego.bandera("luna_regreso")):
		var otra: int = await Interfaz.elegir("¿Despertar?", ["Seguir en la Luna", "Despertar"])
		if otra == 1:
			despertar()
		return
	if not _libre and not bool(Juego.bandera("luna_banderas")):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Todavía nos falta algo aquí arriba. " + _pista()}])
		var cual: int = await Interfaz.elegir("¿Qué hacemos?", ["Seguir en la Luna", "Despertar ya"])
		if cual == 1:
			despertar()
		return
	await Interfaz.decir([
		{"quien": "Órbita", "texto": "Solo una parte de la nave volvió a la Tierra. Nuestra caja hará lo mismo: con el escudo por delante."},
	])
	var r: Dictionary = await Interfaz.abrir_minijuego("regreso", {"dificultad": 1})
	if not r.get("superado", false):
		await Interfaz.decir([{"quien": "Órbita", "texto": "La caja se calentó de más. Respira: probamos otra vez cuando quieras."}])
		return
	Juego.poner_bandera("luna_regreso")
	await Interfaz.decir([{"quien": "Órbita", "texto": "Nos llevamos cuatro bolsas que pesan cero, y una idea. ¡A casa!"}])
	Zonas.ir_a("habitacion", "cama")


func _pista() -> String:
	if not bool(Juego.bandera("luna_baliza")):
		return "Sigue las balizas cian hasta la baliza grande. Salta con Espacio: la zanja se cruza de un brinco."
	if not bool(Juego.bandera("luna_muestras")):
		return "El campo de muestras está junto al cráter pequeño, pasada la baliza."
	if not bool(Juego.bandera("luna_foto")):
		return "Rodea el anillo cian hasta el punto de foto. Se mira, no se pisa."
	if not bool(Juego.bandera("luna_banderas")):
		return "La loma queda fuera del anillo. Allí van las dos banderas."
	if not bool(Juego.bandera("luna_regreso")):
		return "Volvamos a la caja de cartón. Es hora de regresar."
	return "Puedes quedarte a pasear. La caja te espera."


func orbita_dice() -> Array:
	_dato += 1
	var lineas: Array = [{"quien": "Órbita", "texto": _pista()}]
	# si quedan cosas opcionales, una pista de ellas; si no, un dato
	var faltan := 0
	for k in SUELTAS.size():
		if not bool(Juego.bandera("luna_suelta_%d" % k)):
			faltan += 1
	if faltan > 0 and _dato % 3 == 1:
		lineas.append({"quien": "Órbita", "texto": "Quedan %d muestras sueltas brillando por ahí. Se recogen con E." % faltan})
	else:
		lineas.append({"quien": "Órbita", "texto": String(DATOS_ORBITA[_dato % DATOS_ORBITA.size()])})
	return lineas


func ruta_de_prueba() -> Array:
	# de punta a punta: espejo, una muestra suelta, baliza, muestras, foto, banderas y regreso en la caja
	return [
		{"usar": "@orbita"},
		{"ir": Vector3(-0.8, 0, -4.6)}, {"ir": Vector3(-3.7, 0, -6.6)}, {"usar": "Espejo"}, {"bandera": "luna_poi_espejo"},
		{"ir": Vector3(0.6, 0, -9.0)}, {"ir": Vector3(4.6, 0, -17.8)}, {"usar": "Suelta1"}, {"bandera": "luna_suelta_0"},
		{"ir": Vector3(2.6, 0, -22.6)}, {"usar": "Baliza"}, {"bandera": "luna_baliza"},
		{"ir": Vector3(12.0, 0, -30.0)}, {"ir": Vector3(23.8, 0, -38.2)}, {"usar": "Muestras"}, {"bandera": "luna_muestras"},
		{"ir": Vector3(33.0, 0, -37.5)}, {"ir": Vector3(40.2, 0, -33.0)}, {"ir": Vector3(45.5, 0, -21.5)},
		{"ir": Vector3(53.0, 0, -16.5)}, {"ir": Vector3(59.6, 0, -15.6)}, {"usar": "PuntoFoto"}, {"bandera": "luna_foto"},
		{"ir": Vector3(50.0, 0, -11.0)}, {"ir": Vector3(41.0, 0, -8.6)}, {"ir": Vector3(36.4, 0, -7.0)},
		{"usar": "Banderas"}, {"bandera": "luna_banderas"},
		{"ir": Vector3(24.0, 0, -4.5)}, {"ir": Vector3(10.0, 0, -1.5)}, {"ir": Vector3(-0.6, 0, -0.3)},
		{"usar": "Caja"}, {"bandera": "luna_regreso"},
	]
