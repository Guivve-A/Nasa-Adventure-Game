extends Node2D

# Capitulo 3: Marte. PROVISIONAL: el arte y el diseno final los trabaja Domenica.
# Fondos: copia los PNG a recursos/fondos_marte/ con los mismos nombres de capa que la Luna y aparecen solos.
# Mientras no esten, cada capa es una silueta de color liso.
# Objetivos: plantar 3 banderas (EE. UU., Ecuador, IEEE IAS) y desplegar los 3 modulos de la base.

signal terminado

const Personaje := preload("personaje.gd")
const Fondo := preload("fondo_parallax.gd")
const Hud := preload("hud.gd")

const SUELO_Y := 304.0
const ANCHO := 1280.0
const CAMINAR := 80.0
const GRAVEDAD := 600.0           # Marte: 0,38 de la gravedad terrestre; el salto es mas corto que en la Luna
const SALTO := 158.0
const T_DESPLEGAR := 1.2
const RESERVA := [Color("1a0f14"), Color("ffe9c4"), Color("4a2018"), Color("6e2f1c"), Color("94441f")]
const BANDERAS := [["bandera_usa", "Estados Unidos", 420.0], ["bandera_ecuador", "Ecuador", 470.0], ["bandera_ieee", "IEEE IAS — ESPOL", 520.0]]
const MODULOS := [["cupula", "el hábitat", 640.0], ["invernadero", "el invernadero", 830.0], ["paneles", "los paneles solares", 1000.0]]

var control_externo := false
var dir_externa := 0.0
var raiz := ""
var jugador
var camara: Camera2D
var hud
var vel := Vector2.ZERO
var en_suelo := true
var puntos: Array = []            # {tipo, id, nombre, x, nodo, hecho}
var cerca = null
var banderas := 0
var modulos := 0
var fondos_reales := 0
var acabado := false

var _suelo: Node2D
var _progreso := 0.0
var _e_antes := false
var _s_antes := false
var _aviso := "Aterrizaste en Marte. Planta las tres banderas."
var _t_aviso := 5.0


func _ready() -> void:
	raiz = (get_script() as Script).resource_path.get_base_dir().get_base_dir()
	var fondo = Fondo.new()
	add_child(fondo)
	fondos_reales = fondo.armar(raiz + "/recursos/fondos_marte", RESERVA)
	_suelo = Node2D.new()             # el suelo va en un nodo propio, por delante del fondo
	_suelo.z_index = 1
	_suelo.draw.connect(_dibujar_suelo)
	add_child(_suelo)
	var cohete := Sprite2D.new()
	cohete.texture = load(raiz + "/recursos/props/cohete_4.png")
	cohete.centered = false
	cohete.position = Vector2(110, SUELO_Y - 160)
	cohete.z_index = 2
	add_child(cohete)
	for b in BANDERAS:
		_punto("bandera", b)
	for m in MODULOS:
		_punto("modulo", m)
	jugador = Personaje.new()
	jugador.personaje = "jugador"
	jugador.position = Vector2(220, SUELO_Y)
	jugador.z_index = 6
	add_child(jugador)
	camara = Camera2D.new()
	camara.position = Vector2(320, 180)
	add_child(camara)
	camara.make_current()
	hud = Hud.new()
	hud.capitulo = "Capítulo 3 — Marte"
	hud.pie = "← → / A D: moverse  ·  Espacio: saltar  ·  E: plantar / mantener: desplegar" + ("   ·   Fondos de Marte: provisionales" if fondos_reales == 0 else "")
	add_child(hud)


func _punto(tipo: String, d: Array) -> void:
	var s := Sprite2D.new()
	s.texture = load(raiz + "/recursos/props/" + String(d[0]) + ".png")
	s.centered = false
	s.position = Vector2(float(d[2]) - s.texture.get_width() * 0.5, SUELO_Y - s.texture.get_height())
	s.modulate = Color(0.38, 0.89, 0.88, 0.3)       # plano cian: todavia no existe
	s.z_index = 2
	add_child(s)
	puntos.append({"tipo": tipo, "id": d[0], "nombre": d[1], "x": float(d[2]), "nodo": s, "hecho": false})


func _physics_process(delta: float) -> void:
	var dir := dir_externa
	if not control_externo:
		dir = Input.get_axis("ui_left", "ui_right")
		if Input.is_key_pressed(KEY_A):
			dir -= 1.0
		if Input.is_key_pressed(KEY_D):
			dir += 1.0
		dir = clampf(dir, -1.0, 1.0)
		var e := Input.is_key_pressed(KEY_E) or Input.is_key_pressed(KEY_ENTER)
		if e and not _e_antes:
			interactuar()
		if e:
			mantener(delta)
		else:
			_progreso = 0.0
		_e_antes = e
		var s := Input.is_key_pressed(KEY_SPACE) or Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP)
		if s and not _s_antes and en_suelo:
			vel.y = -SALTO
			en_suelo = false
		_s_antes = s
	var pos: Vector2 = jugador.position
	pos.x = clampf(pos.x + dir * CAMINAR * delta, 180.0, ANCHO - 20.0)
	if not en_suelo:
		vel.y += GRAVEDAD * delta
		pos.y += vel.y * delta
		if pos.y >= SUELO_Y:
			pos.y = SUELO_Y
			en_suelo = true
	jugador.position = pos
	jugador.mirar(dir)
	var anim := "quieto" if dir == 0.0 else "caminar"
	if not en_suelo:
		anim = "saltar"
	if jugador.animation != anim:
		jugador.play(anim)
	camara.position.x = clampf(pos.x, 320.0, ANCHO - 320.0)
	cerca = null
	for p in puntos:
		if not p["hecho"] and absf(p["x"] - pos.x) < 26.0 and (p["tipo"] == "bandera" or banderas >= 3):
			cerca = p
			break
	_t_aviso -= delta
	hud.aviso = _aviso if _t_aviso > 0.0 else ""
	if banderas < 3:
		hud.objetivo = {"titulo": "Objetivo 3: planta las banderas", "cuadros": [banderas, 3], "lineas": ["Estados Unidos, Ecuador e IEEE IAS"]}
	else:
		hud.objetivo = {"titulo": "Objetivo final: la base marciana", "cuadros": [modulos, 3], "lineas": ["Despliega los módulos (mantén E)"]}
	hud.progreso = -1.0
	if cerca != null:
		var texto: String = ("E: plantar la bandera de " if cerca["tipo"] == "bandera" else "Mantén E: desplegar ") + String(cerca["nombre"])
		hud.burbuja = {"texto": texto, "pos": Vector2(cerca["x"] - (camara.position.x - 320.0), SUELO_Y - 84.0)}
		if _progreso > 0.0:
			hud.progreso = _progreso / T_DESPLEGAR
	else:
		hud.burbuja = {}
	_suelo.queue_redraw()


func teletransportar(x: float) -> void:
	jugador.position = Vector2(x, SUELO_Y)
	camara.position.x = clampf(x, 320.0, ANCHO - 320.0)
	cerca = null
	for p in puntos:
		if not p["hecho"] and absf(p["x"] - x) < 26.0 and (p["tipo"] == "bandera" or banderas >= 3):
			cerca = p
			break


func interactuar() -> void:
	if cerca != null and cerca["tipo"] == "bandera":
		_hacer(cerca)
		banderas += 1
		_avisar("Bandera de %s plantada (%d de 3)." % [cerca["nombre"], banderas] if banderas < 3 else "¡Las tres banderas ondean en Marte! Ahora, la base.")
		cerca = null


func mantener(delta: float) -> void:
	if cerca == null or cerca["tipo"] != "modulo":
		_progreso = 0.0
		return
	_progreso += delta
	if _progreso >= T_DESPLEGAR:
		_progreso = 0.0
		_hacer(cerca)
		modulos += 1
		_avisar("Desplegaste %s (%d de 3)." % [cerca["nombre"], modulos])
		cerca = null
		if modulos >= 3 and not acabado:
			acabado = true
			get_tree().create_timer(2.0).timeout.connect(func(): terminado.emit())


func _hacer(p: Dictionary) -> void:
	p["hecho"] = true
	var s: Sprite2D = p["nodo"]
	s.modulate = Color(3, 3, 3, 1)
	create_tween().tween_property(s, "modulate", Color.WHITE, 0.6)


func _avisar(texto: String) -> void:
	_aviso = texto
	_t_aviso = 4.0


# suelo provisional: bloques de color oxido
func _dibujar_suelo() -> void:
	var x0 := int(camara.position.x - 336.0) >> 4
	for t in range(x0, x0 + 43):
		for f in 4:
			var h := (t * 374761393 + f * 668265263) & 0x7fffffff
			h = ((h ^ (h >> 13)) * 1274126177) & 0x7fffffff
			var v := float(h & 0xffff) / 65535.0
			var c := Color("d98a52") if f == 0 else (Color("8a4424") if v < 0.3 else (Color("a0522d") if v < 0.7 else Color("b5633a")))
			_suelo.draw_rect(Rect2(t * 16, SUELO_Y + f * 16, 16, 16), c)
			_suelo.draw_rect(Rect2(t * 16, SUELO_Y + f * 16 + 14, 16, 2), Color(0, 0, 0, 0.2))
		_suelo.draw_rect(Rect2(t * 16, SUELO_Y, 16, 2), Color("f0b07a"))
