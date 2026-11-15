extends "res://nucleo/zona.gd"

# La habitacion-taller de la protagonista (Las Escalinatas, Guayaquil).
# Concepto validado por Guillermo: Lote 05, borrador A «Manana calida», version final con entrada y salida
# (Nasa_Game/Fase_1_Arte/Exploracion/Lote_05/L05_A_manana_calida_final.png).
#
# Los modelos los escribe herramientas/mallas/habitacion_modelos.py en modelos/habitacion/ (familias TAL y HAB).
# Todo se coloca en «coordenadas del cuarto»: origen en el centro del suelo, pared del fondo en z = -AZ y pared
# derecha en x = +AX. El cuarto entero va girado GIRO grados, como en el concepto, para que se vean a la vez
# la pared del fondo y la de la derecha: _m() pasa de coordenadas del cuarto a coordenadas del mundo.
#
# Estados, segun las banderas de la partida:
#   a) manana del dia 1 (por defecto)
#   b) noche: mir_luna y mir_linea puestas y luna_regreso no (faroles, lampara y la cama con borde cian)
#   c) manana del dia 2: luna_regreso puesta (el arreglo del seguidor y el cierre del prototipo)

const HAB := "res://modelos/habitacion/"
const ENT := "res://modelos/entorno/"
const GIRO := 20.0               # grados: el extremo derecho de la pared del fondo se aleja de la camara
const AX := 3.3                  # semiancho del suelo (igual que en el generador)
const AZ := 2.7                  # semifondo del suelo
const FUERA := -0.6              # altura del suelo de fuera (BAJO en el generador)
const CALLE := -2.52             # la calle de abajo, al pie de la escalinata (HAB-18)

# puntos del cuarto (coordenadas del cuarto)
const P_INICIO := Vector3(-0.1, 0.0, 0.35)
const P_ESCALERA := Vector3(0.9, 0.0, 1.55)
const P_CAMA := Vector3(-1.6, 0.0, -0.9)
const P_MARCA := Vector3(2.2, 0.0, 1.6)
const P_BANCO := Vector3(2.9, 0.0, -0.45)
const P_TABURETE := Vector3(2.3, 0.0, -0.4)
const P_TELESCOPIO := Vector3(1.95, 0.0, -1.8)
const P_MACETERO := Vector3(2.75, 0.0, -2.2)
const P_CAJA := Vector3(-2.85, 0.0, -1.15)
const P_CAMA_MUEBLE := Vector3(-2.2, 0.0, -2.1)
# donde se para la protagonista para usar cada cosa (ruta de prueba)
const S_CUADERNO := Vector3(2.2, 0.0, 0.3)
const S_SEGUIDOR := Vector3(2.2, 0.0, -1.2)
const S_PASO := Vector3(1.6, 0.0, -0.4)
const S_VENTANA := Vector3(0.1, 0.0, -1.9)
const S_CAMA := Vector3(-1.75, 0.0, -1.0)

# brillo que acompana la inclinacion 2.5D (el emisivo del nucleo no se inclina y quedaria flotando)
const CODIGO_BRILLO := """shader_type spatial;
render_mode world_vertex_coords, unshaded, shadows_disabled;
uniform float inclinacion = 0.45;
uniform vec3 color : source_color = vec3(0.384, 0.894, 0.878);
uniform float energia = 2.5;
void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
}
void fragment() {
	ALBEDO = color * (1.0 + energia);
}
"""

var _cuarto: Node3D
var _base := Basis.IDENTITY
var _noche := false
var _dia2 := false
var _shader_brillo: Shader
var _cian: ShaderMaterial
var _borde_cama: ShaderMaterial
var _t := 0.0


func _construir() -> void:
	encuadre = 0.20
	_dia2 = bool(Juego.bandera("luna_regreso"))
	_noche = bool(Juego.bandera("mir_luna")) and bool(Juego.bandera("mir_linea")) and not _dia2
	_base = Basis(Vector3.UP, deg_to_rad(GIRO))
	_cuarto = Node3D.new()
	_cuarto.name = "Cuarto"
	add_child(_cuarto)
	_cuarto.basis = _base
	# la camara casi no se mueve: el cuarto entero cabe en el cuadro y fuera esta el barrio (HAB-13)
	limites = Rect2(-0.6, -1.3, 1.6, 1.1)

	_shader_brillo = Shader.new()
	_shader_brillo.code = CODIGO_BRILLO
	_cian = _brillo(Color("62e4e0"), 2.5)

	if _noche:
		meta["momento"] = "Noche"
		# noche provisional del nucleo, mas oscura: la luz la ponen los faroles, la lampara y el borde de la cama
		luces("interior_noche", {"energia": 0.16, "ambiente": "3f4c68", "ambiente_energia": 0.62, "exposicion": 0.86, "saturacion": 0.86})
	else:
		meta["momento"] = "Mañana del día 2" if _dia2 else "Mañana"
		# la luz "interior_manana" del nucleo es provisional: aqui se acerca al concepto (mas color y contraste)
		luces("interior_manana", {"saturacion": 0.96, "contraste": 1.14, "exposicion": 0.93, "ambiente": "94808a", "ambiente_energia": 0.60})
	ambiente(0.6)
	_vineta()

	_casco()
	_muebles()
	_banco()
	_plantas()
	_faroles()
	_colisiones()
	_entradas_y_umbral()
	_interactuables()


# ------------------------------------------------------------------ ayudas

func _m(p: Vector3) -> Vector3:
	# coordenadas del cuarto -> mundo
	return _base * p


func _brillo(color: Color, energia: float) -> ShaderMaterial:
	var m := ShaderMaterial.new()
	m.shader = _shader_brillo
	m.set_shader_parameter("color", color)
	m.set_shader_parameter("energia", energia)
	m.set_shader_parameter("inclinacion", cizalla)
	return m


func _mod(ruta: String, pos: Vector3, giro: float = 0.0, escala: float = 1.0, sombra: bool = true) -> Node3D:
	# coloca un GLB dentro del cuarto (coordenadas del cuarto)
	var nodo: Node3D = Recursos.instancia(ruta)
	if nodo == null:
		push_warning("AVISO falta el modelo %s" % ruta)
		return null
	_cuarto.add_child(nodo)
	nodo.position = pos
	nodo.rotation.y = deg_to_rad(giro)
	nodo.scale = Vector3.ONE * escala
	var lista: Array = nodo.find_children("*", "MeshInstance3D", true, false)
	if nodo is MeshInstance3D:
		lista.append(nodo)
	for hijo in lista:
		var mi := hijo as MeshInstance3D
		if not sombra:
			mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			# la traza y los LED (material Emisivo): brillo cian que se inclina con la escena
			if mi.get_surface_override_material(s) is StandardMaterial3D:
				mi.set_surface_override_material(s, _cian)
	return nodo


func _caja_brillo(centro: Vector3, tam: Vector3, material: ShaderMaterial, giro: float = 0.0) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var caja := BoxMesh.new()
	caja.size = tam
	mi.mesh = caja
	mi.material_override = material
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_cuarto.add_child(mi)
	mi.position = centro
	mi.rotation.y = deg_to_rad(giro)
	return mi


func _muro(centro: Vector3, tam: Vector3) -> void:
	# caja de colision alineada con el cuarto
	pared(_m(centro), tam, GIRO)


func _poste(base: Vector3, radio: float, alto: float = 1.2) -> void:
	columna(_m(base), radio, alto)


func _inter(nombre: String, pos: Vector3, texto: String, al_usar: Callable, opciones: Dictionary = {}) -> Node3D:
	return interactuable(nombre, _m(pos), texto, al_usar, opciones)


func _vineta() -> void:
	# las esquinas del cuadro, oscurecidas hacia el azul petroleo como el follaje en primer plano del concepto
	var capa := CanvasLayer.new()
	capa.name = "Vineta"
	capa.layer = -1
	add_child(capa)
	var degradado := Gradient.new()
	degradado.offsets = PackedFloat32Array([0.0, 0.58, 0.86, 1.0])
	degradado.colors = PackedColorArray([Color(0.11, 0.16, 0.17, 0.0), Color(0.11, 0.16, 0.17, 0.0), Color(0.11, 0.16, 0.17, 0.5), Color(0.11, 0.16, 0.17, 0.66)])
	var textura := GradientTexture2D.new()
	textura.gradient = degradado
	textura.fill = GradientTexture2D.FILL_RADIAL
	textura.fill_from = Vector2(0.5, 0.5)
	textura.fill_to = Vector2(1.1, 1.1)
	textura.width = 256
	textura.height = 256
	var cuadro := TextureRect.new()
	cuadro.texture = textura
	cuadro.stretch_mode = TextureRect.STRETCH_SCALE
	cuadro.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cuadro.set_anchors_preset(Control.PRESET_FULL_RECT)
	capa.add_child(cuadro)


# ------------------------------------------------------------------ geometria

func _casco() -> void:
	# HAB-12: suelo de baldosas, pared del fondo, pared derecha y bordes cortados. De noche, sin haces de sol.
	_mod(HAB + ("HAB-12n.glb" if _noche else "HAB-12.glb"), Vector3.ZERO, 0.0, 1.0, false)
	# HAB-13: el barrio de fuera (casas de colores, escalinata) y el suelo oscuro que tapa el vacio
	# HAB-18 (v2): a la derecha la escalinata baja a la calle entre el vecino y la casa de abajo, con terrazas y
	# mas barrio alrededor; cierra el hueco que se veia detras del descanso y llena el encuadre alejado
	for ruta in [HAB + "HAB-13.glb", HAB + "HAB-18.glb"]:
		var barrio := _mod(ruta, Vector3.ZERO, 0.0, 1.0, false)
		if barrio != null:
			# capa 2: los faroles del cuarto (mascara 1) no alumbran el barrio
			for malla in barrio.find_children("*", "MeshInstance3D", true, false):
				(malla as MeshInstance3D).layers = 2
	if _noche:
		# HAB-19: ventanas encendidas del barrio y faroles de la calle, con un brillo calido que se inclina
		var ventanas := _mod(HAB + "HAB-19.glb", Vector3.ZERO, 0.0, 1.0, false)
		if ventanas != null:
			var calido := _brillo(Color("ffc27a"), 0.55)
			for malla in ventanas.find_children("*", "MeshInstance3D", true, false):
				(malla as MeshInstance3D).material_override = calido
				(malla as MeshInstance3D).layers = 2
	# ventana con postigos y buganvilla
	_mod(HAB + "HAB-02.glb", Vector3(0.1, 0.0, -AZ))
	_mod(HAB + "HAB-14.glb", Vector3(0.1, 0.0, -AZ), 0.0, 1.0, false)
	# descanso de la escalera: baranda con puerta, escalera con arco y felpudo
	_mod(HAB + "HAB-07.glb", Vector3(AX, 0.0, 0.9), -90.0)
	_mod(HAB + "HAB-09.glb", Vector3(AX, 0.0, 1.85))
	_mod(HAB + "HAB-08.glb", Vector3(2.2, 0.0, 2.42), 0.0, 1.0, false)
	# alfombra tejida al centro
	_mod(HAB + "HAB-03.glb", Vector3(-0.1, 0.0, 0.35), 0.0, 1.0, false)


func _muebles() -> void:
	# cama en la esquina del fondo a la izquierda (cabecera contra la pared izquierda) y la caja de carton
	_mod(HAB + "HAB-01.glb", P_CAMA_MUEBLE)
	_mod(HAB + "HAB-06.glb", P_CAJA, 8.0)
	# repisa con libros y la esfera armilar; dos cuadritos debajo
	_mod(HAB + "HAB-04.glb", Vector3(-2.1, 0.0, -AZ))
	_mod(HAB + "TAL-12.glb", Vector3(-2.3, 1.4425, -2.56))
	_mod(HAB + "HAB-10.glb", Vector3(-1.6, 1.4425, -2.55), 25.0)
	_mod(HAB + "HAB-17.glb", Vector3(-2.45, 0.98, -AZ), 0.0, 1.0, false)
	_mod(HAB + "HAB-17.glb", Vector3(-1.88, 1.0, -AZ), 0.0, 1.0, false)
	# telescopio pequeno junto a la ventana, apuntando hacia ella
	_mod(HAB + "TAL-14.glb", P_TELESCOPIO, 40.0)
	# poster del observatorio en la pared derecha
	_mod(HAB + "HAB-05.glb", Vector3(AX, 1.55, -0.45), -90.0, 1.0, false)


func _banco() -> void:
	# banco de trabajo contra la pared derecha (el frente mira al cuarto) y lo que lleva encima
	var y := 0.80
	_mod(HAB + "TAL-01.glb", P_BANCO, -90.0)
	_mod(HAB + "TAL-07.glb", Vector3(2.9, 0.24, -0.75), -90.0)                 # caja de herramientas, en la balda
	_mod(HAB + "TAL-15.glb", Vector3(2.9, y, -1.12), 55.0, 1.3)                     # seguidor lunar
	_mod(HAB + "TAL-06.glb", Vector3(2.74, y, -0.70), -100.0)                  # placa de circuito
	_mod(HAB + "TAL-09.glb", Vector3(3.14, y, -0.72), -90.0)                   # lampara
	_mod(HAB + "TAL-02.glb", Vector3(3.0, y, -0.28), -62.0)                    # osciloscopio
	_mod(HAB + "TAL-16.glb", Vector3(2.8, y, 0.2), -78.0)                      # cuaderno abierto
	_mod(HAB + "TAL-17.glb", Vector3(3.12, y, 0.42))                           # vaso con lapices
	_mod(HAB + "TAL-10.glb", P_TABURETE, 15.0)                                 # taburete


func _plantas() -> void:
	# planta grande en la esquina del fondo a la derecha (ave del paraiso, VEG-07) en su macetero
	_mod(HAB + "HAB-16.glb", P_MACETERO)
	_mod(ENT + "VEG-07.glb", P_MACETERO + Vector3(0.0, 0.36, 0.0), 30.0, 1.55)
	# macetas colgantes: junto a la repisa y en la pared derecha
	_mod(HAB + "HAB-15.glb", Vector3(-3.0, 1.38, -2.4))
	_mod(HAB + "HAB-15.glb", Vector3(3.0, 1.38, 0.55), -90.0)
	# follaje en primer plano y a los lados, fuera del cuarto: viste los bordes del cuadro
	var fuera := [
		[ENT + "VEG-10.glb", Vector3(-4.3, FUERA, 2.6), 20.0, 2.6],
		[ENT + "VEG-12.glb", Vector3(-4.6, FUERA, 0.6), 80.0, 2.0],
		[ENT + "VEG-07.glb", Vector3(-4.4, FUERA, -1.4), 140.0, 2.2],
		[ENT + "VEG-10.glb", Vector3(-2.6, FUERA, 3.9), 200.0, 2.2],
		[ENT + "VEG-12.glb", Vector3(-0.6, FUERA, 4.1), 10.0, 2.0],
		[ENT + "VEG-07.glb", Vector3(1.3, FUERA, 4.0), 250.0, 1.9],
		[ENT + "VEG-10.glb", Vector3(3.0, FUERA, 4.1), 90.0, 2.3],
		# v2: a la derecha baja la escalinata (HAB-18): jardin junto al descanso y matas en la calle de abajo
		[ENT + "VEG-12.glb", Vector3(4.05, FUERA, 4.3), 300.0, 1.9],
		[ENT + "VEG-07.glb", Vector3(4.0, FUERA, 6.6), 200.0, 1.8],
		[ENT + "VEG-10.glb", Vector3(8.75, CALLE, 4.0), 160.0, 2.0],
		[ENT + "VEG-12.glb", Vector3(8.9, CALLE, -1.7), 40.0, 1.8],
	]
	for f in fuera:
		var ruta: String = f[0]
		var pos: Vector3 = f[1]
		var giro: float = f[2]
		var escala: float = f[3]
		var planta := _mod(ruta, pos, giro, escala, false)
		if planta == null:
			continue
		# v3: capa 2, como el barrio: de noche los faroles del cuarto no las encienden (quedaban amarillas, como al sol)
		for malla in planta.find_children("*", "MeshInstance3D", true, false):
			(malla as MeshInstance3D).layers = 2


func _faroles() -> void:
	# dos faroles (HAB-11): sobre el poste del frente y colgado en el arco de la escalera
	var p_poste := Vector3(-1.6, 0.88, AZ + 0.125)
	var p_arco := Vector3(AX + 0.86, 0.40, 1.85)
	var calido := _brillo(Color("ffcf8a"), 1.6 if _noche else 0.9)
	for p in [p_poste, p_arco]:
		var pos: Vector3 = p
		_mod(HAB + "HAB-11.glb", pos, 0.0, 1.0, false)
		_caja_brillo(pos + Vector3(0.0, 0.165, 0.0), Vector3(0.12, 0.24, 0.12), calido)
	# luz practica. OJO: con el acabado pintado del nucleo (las sombras conservan el 30 %), un farol nunca cae a
	# cero con la distancia: cada uno suma el 30 % de su energia a todo el casco del cuarto. Por eso van bajos.
	# v2 (rendimiento): el casco es una sola malla, asi que cada luz omni se calcula en todos sus pixeles. Medido en
	# la HD 620: las dos luces de dia (0,25 y 0,3, casi invisibles con el sol) costaban unos 9 fps. De dia el farol
	# solo brilla (caja emisiva); las luces omni quedan para la noche, donde si se ven.
	if not _noche:
		return
	_luz(p_poste + Vector3(0.0, 0.3, -0.25), Color("ffc98a"), 0.6, 3.0)
	_luz(p_arco + Vector3(-0.3, 0.3, 0.0), Color("ffc98a"), 0.6, 2.8)
	# la lampara del banco y la cama con su borde cian (4.1 de la historia: «la cama brilla»)
	_luz(Vector3(2.85, 1.35, -0.6), Color("ffd9a0"), 0.7, 2.6)
	_caja_brillo(Vector3(3.105, 1.065, -0.66), Vector3(0.09, 0.02, 0.09), _brillo(Color("ffe2b0"), 2.0))
	_borde_cama = _brillo(Color("62e4e0"), 1.6)
	var z_frente := -1.47
	var x_pie := -1.12
	_caja_brillo(Vector3((-AX + x_pie) * 0.5, 0.02, z_frente), Vector3(x_pie + AX, 0.02, 0.06), _borde_cama)
	_caja_brillo(Vector3(x_pie, 0.02, (z_frente - 2.66) * 0.5), Vector3(0.06, 0.02, z_frente + 2.66), _borde_cama)
	# la luz cian de la cama se queda: sin ella la protagonista junto a la cama se pierde en la sombra (probado en v2)
	_luz(Vector3(-1.6, 0.5, -1.3), Color("62e4e0"), 0.22, 1.6)


func _luz(pos: Vector3, color: Color, energia: float, alcance: float) -> void:
	var luz := farol(_m(pos), color, energia, alcance)
	luz.light_cull_mask = 1


func _process(delta: float) -> void:
	if _borde_cama != null:
		_t += delta
		_borde_cama.set_shader_parameter("energia", 1.5 + 0.7 * sin(_t * 2.2))


# ------------------------------------------------------------------ colisiones

func _colisiones() -> void:
	piso(Vector3.ZERO, Vector2(16.0, 16.0))
	# paredes: fondo, izquierda (cortada), derecha con la baranda y murete del frente
	_muro(Vector3(0.0, 1.2, -AZ - 0.3), Vector3(2.0 * AX + 1.2, 2.4, 0.6))
	_muro(Vector3(-AX - 0.3, 1.2, 0.0), Vector3(0.6, 2.4, 2.0 * AZ + 1.2))
	_muro(Vector3(AX + 0.3, 1.2, 0.0), Vector3(0.6, 2.4, 2.0 * AZ + 1.2))
	_muro(Vector3(0.0, 1.2, AZ + 0.3), Vector3(2.0 * AX + 1.2, 2.4, 0.6))
	_muro(Vector3(AX, 0.6, 1.9), Vector3(0.2, 1.2, 2.0))                      # baranda y puerta
	_muro(Vector3(0.1, 0.6, -2.56), Vector3(1.7, 1.2, 0.28))                  # alfeizar
	# muebles
	_muro(P_CAMA_MUEBLE + Vector3(0.0, 0.4, 0.0), Vector3(2.0, 0.8, 1.12))
	_muro(P_CAJA + Vector3(0.0, 0.25, 0.0), Vector3(0.62, 0.5, 0.5))
	_muro(P_BANCO + Vector3(0.0, 0.5, 0.0), Vector3(0.8, 1.0, 2.02))
	_poste(P_TABURETE, 0.2, 0.5)
	# v3: columnas mas altas que el rayo de suelo del companero (sale a 1,6 m): si no, Orbita se subia encima
	# del macetero o del telescopio y parecia flotar
	_poste(P_TELESCOPIO, 0.25, 2.0)
	_poste(P_MACETERO, 0.36, 2.0)


# ------------------------------------------------------------------ entradas, umbral e interactuables

func _entradas_y_umbral() -> void:
	entrada("inicio", _m(P_INICIO), Vector3(0, 0, 1))
	entrada("escalera", _m(P_ESCALERA), _m(Vector3(-0.75, 0.0, -0.65)))
	entrada("cama", _m(P_CAMA), Vector3(0, 0, 1))
	# la marca cian del descanso, frente a la puerta de la baranda, con 2 x 2 m despejados
	umbral("Escalera", _m(P_MARCA), "ciudad", "casa", "A la plaza", {
		"requiere": "hab_seguidor",
		"mensaje_cerrado": "Primero el seguidor: sin él no hay Luna que grabar.",
	})


func _interactuables() -> void:
	_inter("Cuaderno", Vector3(2.75, 0.0, 0.25), "Leer el cuaderno", _usar_cuaderno, {"radio": 1.1, "altura_marca": 1.2})
	_inter("Seguidor", Vector3(2.85, 0.0, -1.1), "Ajustar el seguidor", _usar_seguidor, {"radio": 1.1, "altura_marca": 1.5})
	_inter("Poster", Vector3(2.45, 0.0, -0.4), "Mirar el póster", _usar_poster, {"radio": 1.0, "altura_marca": 1.35})
	_inter("Telescopio", P_TELESCOPIO, "Mirar el telescopio", _usar_telescopio, {"radio": 1.0, "altura_marca": 1.5})
	_inter("Caja", P_CAJA, "Mirar la caja", _usar_caja, {"radio": 1.1, "altura_marca": 0.8})
	_inter("Ventana", Vector3(0.1, 0.0, -2.45), "Asomarse a la ventana", _usar_ventana, {"radio": 1.1, "altura_marca": 1.2})
	_inter("Cama", Vector3(-1.95, 0.0, -1.6), "Dormir" if _noche else "Mirar la cama", _usar_cama, {"radio": 1.1, "altura_marca": 0.95})


func _usar_cuaderno() -> void:
	Audio.sonar("pagina")
	await Interfaz.decir([
		"La convocatoria, copiada a mano: «Graba 60 s de la Luna con un instrumento construido por ti».",
		"«Plazo: antes de la medianoche de mañana.» Debajo, mi dibujo de la Luna, con tres cráteres.",
		{"quien": "Yo", "texto": "Sesenta segundos. Y mi seguidor tiembla a los dos."},
		{"quien": "Órbita", "texto": "Entonces primero el seguidor. Está en el banco, junto al osciloscopio."},
	])
	Juego.poner_bandera("hab_convocatoria")


func _usar_seguidor() -> void:
	if _noche:
		await Interfaz.decir([{"quien": "Yo", "texto": "Hoy ya trabajó bastante. Mañana lo reviso con la cabeza fresca."}])
		return
	if _dia2:
		if not Juego.bandera("hab_seguidor_v2"):
			await Interfaz.decir([
				{"quien": "Yo", "texto": "El cielo gira unos 15° por hora. Eso ya lo sé: no hace falta que el motor lo adivine."},
				{"quien": "Órbita", "texto": "Dale la velocidad conocida y deja que el control corrija solo el resto."},
			])
		var r2: Dictionary = await Interfaz.abrir_minijuego("seguidor", {"dificultad": 2, "modo": "prealimentacion"})
		if r2.get("superado", false) and not Juego.bandera("hab_seguidor_v2"):
			Juego.poner_bandera("hab_seguidor_v2")
			Juego.anotar("prealimentacion")
			await Interfaz.decir([
				{"quien": "Yo", "texto": "Sigue solo. Sin temblar y sin atrasarse."},
				{"quien": "Órbita", "texto": "Asómate a la ventana. Hay que ver por dónde pasará la Luna."},
			])
		return
	if not Juego.bandera("hab_seguidor"):
		await Interfaz.decir([
			{"quien": "Yo", "texto": "Dos motores, una cámara y un control que tiembla. Un parámetro a la vez."},
		])
	var r: Dictionary = await Interfaz.abrir_minijuego("seguidor", {"dificultad": 1})
	if r.get("superado", false) and not Juego.bandera("hab_seguidor"):
		Juego.poner_bandera("hab_seguidor")
		await Interfaz.decir([
			{"quien": "Yo", "texto": "Mide, compara y corrige. Ya no tiembla."},
			{"quien": "Órbita", "texto": "Falta probarlo con el cielo de verdad. La escalera está abierta."},
		])


func _usar_poster() -> void:
	var nueva: bool = Juego.anotar("observatorio_quito")
	await Interfaz.decir([
		"El Observatorio Astronómico de Quito: una cúpula blanca sobre la loma. Fundado en 1873.",
		{"quien": "Yo", "texto": "Más de 150 años mirando el mismo cielo que yo. Algún día subo a saludar."},
	])
	if nueva:
		Interfaz.aviso("Ficha nueva en el cuaderno: El Observatorio de Quito", 3.0)


func _usar_telescopio() -> void:
	if _noche:
		await Interfaz.decir([{"quien": "Yo", "texto": "La Luna ya se puso. Buenas noches, telescopio."}])
	else:
		await Interfaz.decir([
			{"quien": "Yo", "texto": "Mi telescopio pequeño. De día solo sirve para espiar las buganvillas."},
			{"quien": "Órbita", "texto": "Y a mí. Te he visto."},
		])


func _usar_caja() -> void:
	if _noche:
		await Interfaz.decir([
			"La caja de cartón de los adornos, junto a la cama.",
			{"quien": "Yo", "texto": "Cabe una persona sentada. No es que lo haya medido."},
		])
	else:
		await Interfaz.decir([
			"La caja de cartón de los adornos. Papá la dejó aquí «por si necesitas guardar algo».",
			{"quien": "Yo", "texto": "Por ahora guarda aire y un poco de escarcha."},
		])


func _usar_ventana() -> void:
	if _dia2 and Juego.bandera("hab_seguidor_v2"):
		var abiertas: int = (Juego.estado["cuaderno"] as Array).size()
		var total: int = Juego.fichas.size()
		Juego.poner_bandera("fin_v0")
		Audio.sonar("logro")
		await Interfaz.decir([
			{"quien": "Yo", "texto": "El seguidor ya apunta solo. Esta noche, 60 s de Luna sin un temblor."},
			{"quien": "Órbita", "texto": "Y yo en primera fila, en el alféizar."},
			"Fin del prototipo v0. Abriste %d de %d fichas del cuaderno." % [abiertas, total],
			"Gracias por jugar. Puedes seguir explorando: el barrio no se va a ningún lado.",
		])
		return
	if _noche:
		await Interfaz.decir([{"quien": "Yo", "texto": "Las Escalinatas con los faroles encendidos. Hasta mañana, barrio."}])
		return
	await Interfaz.decir([
		"Las Escalinatas de mañana: techos de colores, 16 escalones a la vista y olor a verde frito.",
		{"quien": "Órbita", "texto": "El alféizar es mío. Puesto de observación número uno."},
	])


func _usar_cama() -> void:
	if not _noche:
		if _dia2:
			await Interfaz.decir([{"quien": "Yo", "texto": "Con el sueño de anoche tengo para toda la semana."}])
		else:
			await Interfaz.decir([{"quien": "Yo", "texto": "Todavía no tengo sueño."}])
		return
	var i: int = await Interfaz.elegir("¿Dormir?", ["Sí", "Todavía no"])
	if i != 0:
		return
	Juego.poner_bandera("hab_durmio")
	# sin await y al final: esta zona se libera durante el cambio
	Zonas.ir_a("luna", "inicio")


# ------------------------------------------------------------------ llegada, pistas y ruta de prueba

func al_entrar(_nombre_entrada: String) -> void:
	if _noche:
		var primera: bool = not Juego.bandera("hab_noche")
		Juego.poner_bandera("hab_noche")
		if primera:
			await Interfaz.decir([
				{"quien": "Yo", "texto": "Qué día. La Luna, la línea de tiempo y como mil escalones."},
				{"quien": "Órbita", "texto": "La cama tiene un brillo raro. Yo que tú, dormía."},
			])
		return
	if _dia2:
		if not Juego.bandera("hab_dia2"):
			Juego.poner_bandera("hab_dia2")
			await Interfaz.decir([
				{"quien": "Yo", "texto": "¿Fue un sueño? Todavía siento el polvo gris en las botas."},
				{"quien": "Órbita", "texto": "Dormida dijiste «quince grados por hora». Dos veces."},
				{"quien": "Yo", "texto": "¡Eso! El cielo gira a una velocidad conocida. Al banco, Órbita."},
			])
		return
	if not Juego.bandera("hab_saludo"):
		Juego.poner_bandera("hab_saludo")
		await Interfaz.decir([
			"Buenos días, taller. Buenos días, sol que entra sin pedir permiso.",
			{"quien": "Órbita", "texto": "Miau. Tu cuaderno sigue abierto en el banco. Anoche copiaste algo importante."},
			{"quien": "Yo", "texto": "La convocatoria. Hoy sí la leo despierta."},
		])


func ruta_de_prueba() -> Array:
	if _noche:
		return [
			{"bandera": "hab_noche"},
			{"ir": _m(S_CAMA)},
			{"usar": "Cama"},
			{"bandera": "hab_durmio"},
		]
	if _dia2:
		return [
			{"ir": _m(S_SEGUIDOR)},
			{"usar": "Seguidor"},
			{"bandera": "hab_seguidor_v2"},
			{"ir": _m(Vector3(1.2, 0.0, -0.9))},
			{"ir": _m(S_VENTANA)},
			{"usar": "Ventana"},
			{"bandera": "fin_v0"},
		]
	return [
		{"usar": "@orbita"},
		{"ir": _m(S_CUADERNO)},
		{"usar": "Cuaderno"},
		{"bandera": "hab_convocatoria"},
		{"ir": _m(S_PASO)},
		{"ir": _m(S_SEGUIDOR)},
		{"usar": "Seguidor"},
		{"bandera": "hab_seguidor"},
		{"ir": _m(S_PASO)},
		{"ir": _m(P_MARCA)},
	]
