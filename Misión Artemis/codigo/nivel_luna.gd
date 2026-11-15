extends Node2D

# Capitulo 1: la base del polo sur lunar. Vista lateral, un solo eje.
# Objetivo 1: llevar cajas y minerales a la constructora, que arma el cohete en 4 fases.
# Objetivo 2: combustible (hielo del crater) y bateria (paneles orientados) para despegar hacia Marte.
# El mundo (alturas, props, personajes) sale de datos/nivel_luna.json, que escribe herramientas/generar_hojas.js.

signal despegue(resumen)

const Personaje := preload("personaje.gd")
const Fondo := preload("fondo_parallax.gd")
const Hud := preload("hud.gd")

const SUELO_Y := 304.0
const CAMINAR := 70.0
const CORRER := 115.0
const GRAVEDAD := 260.0          # baja: salto alto y lento, como con 1/6 de la gravedad
const SALTO := 158.0             # sube unas 3 casillas
const IMPULSO := 115.0           # segundo salto en el aire, con la mochila
const VEL_ROVER := 150.0
const CAPACIDAD := 4
const CAPACIDAD_ROVER := 10
const T_EXTRAER := 1.1
const T_PANEL := 1.0
const FASES := [{"caja": 4}, {"caja": 4, "ilmenita": 4}, {"caja": 4, "regolito": 4}, {"ilmenita": 4, "regolito": 4}]
const PARTES := ["los motores", "el tanque", "la etapa superior", "la punta"]
const REFUGIOS := {"cupula": "la cúpula", "invernadero": "el invernadero", "refugio": "el refugio"}
const VETAS := {"veta_ilmenita": ["ilmenita", 4], "veta_regolito": ["regolito", 5], "veta_hielo": ["hielo", 3]}
const ORDEN := ["caja", "ilmenita", "regolito", "hielo"]
const NOMBRES := {"caja": "cajas", "ilmenita": "ilmenita", "regolito": "regolito", "hielo": "hielo"}

# para pruebas automaticas: sin teclado ni eventos al azar
var control_externo := false
var eventos_auto := true
var dir_externa := 0.0

var raiz := ""
var datos := {}
var dialogos := {}
var alturas: Array = []
var ancho := 2560.0
var objetos: Array = []
var hud
var camara: Camera2D
var jugador
var vel := Vector2.ZERO
var en_suelo := true
var impulso_listo := true
var montado := false
var dentro = null                # refugio en el que esta el jugador
var cerca = null                 # objeto con el que puede interactuar
var rover = null
var cohete = null
var barras := {"oxigeno": 100.0, "energia": 100.0, "alimentos": 100.0, "radiacion": 0.0}
var mochila := {"caja": 0, "ilmenita": 0, "regolito": 0, "hielo": 0}
var maletero := {"caja": 0, "ilmenita": 0, "regolito": 0, "hielo": 0}
var entregado := {"caja": 0, "ilmenita": 0, "regolito": 0, "hielo": 0}
var fase := 0
var combustible := 0.0
var bateria := 0.0
var paneles_orientados := 0
var rescates := 0
var tiempo := 0.0
var lanzando := -1.0
var estado_lluvia := 0           # 0 calma, 1 aviso, 2 lluvia
var t_lluvia := 70.0
var t_meteoros := 40.0
var t_carga := 100.0
var meteoros: Array = []
var polvos: Array = []

var _fx: Node2D
var _luz_tex: GradientTexture2D
var _aviso := ""
var _t_aviso := 0.0
var _progreso := 0.0
var _e_antes := false
var _s_antes := false
var _habla = null
var _linea := 0


func _ready() -> void:
	raiz = (get_script() as Script).resource_path.get_base_dir().get_base_dir()
	datos = (load(raiz + "/datos/nivel_luna.json") as JSON).data
	dialogos = (load(raiz + "/datos/dialogos.json") as JSON).data
	alturas = datos["alturas"]
	ancho = float(datos["ancho"])
	var fondo = Fondo.new()
	add_child(fondo)
	fondo.armar(raiz + "/recursos/fondos_luna/5_polo_sur_sol_eterno", [], 72.0)
	var suelo := Sprite2D.new()
	suelo.texture = load(raiz + "/recursos/nivel/suelo_luna.png")
	suelo.centered = false
	suelo.position = Vector2(0, SUELO_Y - float(datos["suelo_base"]))
	add_child(suelo)
	_luz_tex = GradientTexture2D.new()
	_luz_tex.fill = GradientTexture2D.FILL_RADIAL
	_luz_tex.fill_from = Vector2(0.5, 0.5)
	_luz_tex.fill_to = Vector2(1.0, 0.5)
	_luz_tex.width = 64
	_luz_tex.height = 64
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 0.55))
	g.set_color(1, Color(1, 1, 1, 0.0))
	_luz_tex.gradient = g
	for p in datos["props"]:
		_crear_prop(p)
	for gnt in datos["gente"]:
		var n = Personaje.new()
		n.personaje = gnt[0]
		var x := float(gnt[1]) + 16.0
		n.position = Vector2(x, suelo_en(x))
		n.z_index = 4
		add_child(n)
		objetos.append({"tipo": "npc", "id": gnt[0], "x": x, "w": 20.0, "nodo": n})
	jugador = Personaje.new()
	jugador.personaje = "jugador"
	jugador.position = Vector2(672.0, suelo_en(672.0))
	jugador.z_index = 6
	add_child(jugador)
	_fx = Node2D.new()
	_fx.z_index = 8
	_fx.draw.connect(_dibujar_fx)
	add_child(_fx)
	var frente := Parallax2D.new()
	frente.scroll_scale = Vector2(1.3, 0.0)
	frente.repeat_size = Vector2(1280.0, 0.0)
	frente.repeat_times = 3
	frente.z_index = 20
	var sf := Sprite2D.new()
	sf.texture = load(raiz + "/recursos/nivel/frente_luna.png")
	sf.centered = false
	sf.position = Vector2(0, 360.0 - 26.0)
	frente.add_child(sf)
	add_child(frente)
	camara = Camera2D.new()
	camara.position = Vector2(jugador.position.x, 180.0)
	add_child(camara)
	camara.make_current()
	hud = Hud.new()
	hud.capitulo = "Capítulo 1 — La Luna"
	hud.pie = "← → / A D: moverse  ·  Mayús: correr  ·  Espacio: saltar (dos veces: impulso)  ·  E: usar / mantener: extraer"
	add_child(hud)
	avisar("Habla con el equipo de la base (E)", 5.0)


func suelo_en(x: float) -> float:
	return SUELO_Y - float(alturas[clampi(int(x) >> 4, 0, alturas.size() - 1)])


func _crear_prop(p: Dictionary) -> void:
	var id: String = p["id"]
	var w := float(p["w"])
	var h := float(p["h"])
	var x := float(p["x"])
	var s := Sprite2D.new()
	s.texture = load(raiz + "/recursos/props/" + ("cohete_0" if id == "cohete" else id) + ".png")
	s.centered = false
	s.position = Vector2(x, suelo_en(x + w * 0.5) - h)
	s.z_index = 2
	add_child(s)
	for l in p["luces"]:
		_luz(s.position + Vector2(float(l[0]), float(l[1])), float(l[2]), Color(String(l[3])))
	var o := {"id": id, "x": x + w * 0.5, "w": w, "nodo": s, "tipo": "adorno"}
	if id == "pila" or id == "caja_a":
		o["tipo"] = "cajas"
		o["unidades"] = 3 if id == "pila" else 1
	elif VETAS.has(id):
		o["tipo"] = "veta"
		o["recurso"] = VETAS[id][0]
		o["unidades"] = VETAS[id][1]
	elif REFUGIOS.has(id):
		o["tipo"] = "refugio"
	elif id == "recarga":
		o["tipo"] = "oxigeno"
	elif id == "estacion":
		o["tipo"] = "carga"
	elif id == "maquina":
		o["tipo"] = "constructora"
	elif id == "deposito":
		o["tipo"] = "deposito"
	elif id == "paneles":
		o["tipo"] = "panel"
		o["orientado"] = false
		s.modulate = Color(0.62, 0.62, 0.72)      # con polvo y sin orientar: apagado
	elif id == "cohete":
		o["tipo"] = "cohete"
		cohete = o
	elif id == "rover":
		o["tipo"] = "rover"
		s.z_index = 5
		rover = o
	objetos.append(o)


func _luz(pos: Vector2, radio: float, color: Color) -> void:
	var s := Sprite2D.new()
	s.texture = _luz_tex
	s.position = pos
	s.scale = Vector2.ONE * radio * 2.4 / 64.0
	s.modulate = color
	s.z_index = 3
	var m := CanvasItemMaterial.new()
	m.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	s.material = m
	add_child(s)


# ---------- bucle ----------
func _physics_process(delta: float) -> void:
	if lanzando >= 0.0:
		_animar_despegue(delta)
		return
	tiempo += delta
	var dir := dir_externa
	var correr := false
	if not control_externo:
		dir = Input.get_axis("ui_left", "ui_right")
		if Input.is_key_pressed(KEY_A):
			dir -= 1.0
		if Input.is_key_pressed(KEY_D):
			dir += 1.0
		dir = clampf(dir, -1.0, 1.0)
		correr = Input.is_key_pressed(KEY_SHIFT)
		var e := Input.is_key_pressed(KEY_E) or Input.is_key_pressed(KEY_ENTER)
		if e and not _e_antes:
			interactuar()
		if e:
			mantener(delta)
		else:
			_progreso = 0.0
		_e_antes = e
		var s := Input.is_key_pressed(KEY_SPACE) or Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP)
		if s and not _s_antes:
			saltar()
		_s_antes = s
	if _habla != null:
		dir = 0.0
	if dentro != null:
		if dir != 0.0:
			_salir()
		dir = 0.0
	_mover(delta, dir, correr)
	_medidores(delta, dir, correr)
	_eventos(delta)
	_buscar_cerca()
	camara.position.x = clampf(jugador.position.x, 320.0, ancho - 320.0)
	_t_aviso -= delta
	_actualizar_hud()
	_fx.queue_redraw()


func _mover(delta: float, dir: float, correr: bool) -> void:
	var v := CAMINAR
	if montado:
		v = VEL_ROVER if barras["energia"] > 0.0 else 30.0
	elif correr:
		v = CORRER
	if not montado:
		if barras["alimentos"] <= 0.0:
			v *= 0.6
		if _total(mochila) >= 3:
			v *= 0.85
	vel.x = dir * v
	var pos: Vector2 = jugador.position
	var nx := clampf(pos.x + vel.x * delta, 10.0, ancho - 10.0)
	var ny := suelo_en(nx)
	if en_suelo:
		if ny < pos.y - 8.5:
			nx = pos.x                      # escalon de mas de media casilla: hay que saltar
		elif ny <= pos.y + 8.5:
			pos.y = ny                      # escalon bajo: lo sube o lo baja solo
		else:
			en_suelo = false                # se acabo el suelo: cae
	elif ny < pos.y - 0.5:
		nx = pos.x                          # choca de lado contra el escalon
	pos.x = nx
	if not en_suelo:
		vel.y += GRAVEDAD * delta
		pos.y += vel.y * delta
		if pos.y >= suelo_en(pos.x):
			pos.y = suelo_en(pos.x)
			vel.y = 0.0
			en_suelo = true
			impulso_listo = true
	jugador.position = pos
	if montado:
		var nodo: Sprite2D = rover["nodo"]
		rover["x"] = pos.x
		nodo.position = Vector2(pos.x - 32.0, pos.y - 36.0)
		if dir != 0.0:
			nodo.flip_h = dir < 0.0
		return
	jugador.mirar(dir)
	var anim := "quieto"
	if not en_suelo:
		anim = "saltar"
	elif dir != 0.0:
		anim = "caminar"
	if jugador.animation != anim:
		jugador.play(anim)


func saltar() -> void:
	if _habla != null or dentro != null or montado or lanzando >= 0.0:
		return
	if en_suelo:
		vel.y = -SALTO
		en_suelo = false
	elif impulso_listo and barras["energia"] >= 6.0:
		vel.y = -IMPULSO
		impulso_listo = false
		barras["energia"] -= 6.0
		polvos.append({"x": jugador.position.x, "y": jugador.position.y, "t": 0.0, "color": Color("62e4e0")})


func _medidores(delta: float, dir: float, correr: bool) -> void:
	var x: float = jugador.position.x
	var b := barras
	b["alimentos"] -= 0.35 * delta
	b["energia"] -= 0.12 * delta
	if montado and dir != 0.0:
		b["energia"] -= 0.7 * delta
	if dentro != null:
		var id: String = dentro["id"]
		b["oxigeno"] += 22.0 * delta
		b["radiacion"] -= (18.0 if id == "refugio" else 8.0) * delta
		b["alimentos"] += (14.0 if id == "invernadero" else 5.0) * delta
		if id == "cupula":
			b["energia"] += 8.0 * delta
	else:
		b["oxigeno"] -= (1.5 if correr and dir != 0.0 and not montado else 0.9) * delta
		if estado_lluvia == 2:
			b["radiacion"] += 5.0 * delta
		elif x < 480.0:
			b["radiacion"] += 0.25 * delta
		elif x < 1680.0:
			b["radiacion"] -= 1.0 * delta
		elif x < 2240.0:
			b["radiacion"] += 0.5 * delta
		else:
			b["radiacion"] += 1.0 * delta
		for o in objetos:
			if absf(o["x"] - x) < o["w"] * 0.5 + 12.0:
				if o["tipo"] == "oxigeno":
					b["oxigeno"] += 30.0 * delta
				elif o["tipo"] == "carga":
					b["energia"] += 32.0 * delta
	for k in b:
		b[k] = clampf(b[k], 0.0, 100.0)
	if fase >= 4 and bateria < 100.0:
		bateria = minf(100.0, bateria + paneles_orientados * 1.7 * delta)
	if b["oxigeno"] <= 0.0:
		rescate("Te quedaste sin oxígeno")
	elif b["radiacion"] >= 100.0:
		rescate("Demasiada radiación")


# nadie muere: el equipo te lleva a la cupula y pierdes la mitad de la carga
func rescate(causa: String) -> void:
	rescates += 1
	if montado:
		_bajar()
	for k in ORDEN:
		mochila[k] = int(mochila[k]) / 2
	barras["oxigeno"] = 60.0
	barras["radiacion"] = 30.0
	barras["energia"] = maxf(barras["energia"], 40.0)
	barras["alimentos"] = maxf(barras["alimentos"], 40.0)
	teletransportar(616.0)
	avisar(causa + ": el equipo te llevó a la cúpula. Perdiste parte de la carga.", 5.0)


func teletransportar(x: float) -> void:
	jugador.position = Vector2(x, suelo_en(x))
	vel = Vector2.ZERO
	en_suelo = true
	if montado:
		rover["x"] = x
		(rover["nodo"] as Sprite2D).position = Vector2(x - 32.0, suelo_en(x) - 36.0)
	camara.position.x = clampf(x, 320.0, ancho - 320.0)
	_buscar_cerca()


func avisar(texto: String, dur := 3.0) -> void:
	_aviso = texto
	_t_aviso = dur


func _total(d: Dictionary) -> int:
	var n := 0
	for k in d:
		n += int(d[k])
	return n


func _capacidad() -> int:
	return CAPACIDAD_ROVER if montado else CAPACIDAD


# ---------- interaccion ----------
func _buscar_cerca() -> void:
	cerca = null
	if dentro != null:
		return
	var mejor := 1e9
	var x: float = jugador.position.x
	for o in objetos:
		var t: String = o["tipo"]
		if t == "adorno" or t == "oxigeno" or t == "carga":
			continue
		if (t == "cajas" or t == "veta") and int(o["unidades"]) <= 0:
			continue
		if t == "rover" and montado:
			continue
		var d := absf(o["x"] - x)
		if d < o["w"] * 0.5 + 14.0 and d < mejor:
			mejor = d
			cerca = o


func interactuar() -> void:
	if lanzando >= 0.0:
		return
	if _habla != null:
		_avanzar_dialogo()
		return
	if dentro != null:
		_salir()
		return
	if cerca == null:
		if montado:
			_bajar()
		return
	match cerca["tipo"]:
		"npc":
			if montado:
				_bajar()
			_habla = cerca
			_linea = -1
			_avanzar_dialogo()
		"cajas":
			if _total(mochila) >= _capacidad():
				avisar("Mochila llena: entrega en la constructora" + ("" if montado else " o usa el rover"))
			else:
				mochila["caja"] += 1
				cerca["unidades"] -= 1
				_refrescar(cerca)
		"refugio":
			if montado:
				_bajar()
			dentro = cerca
			jugador.visible = false
			avisar("Dentro de " + REFUGIOS[cerca["id"]] + ": a salvo. Muévete para salir.", 4.0)
		"rover":
			montado = true
			jugador.visible = false
			for k in ORDEN:
				mochila[k] += maletero[k]
				maletero[k] = 0
			teletransportar(rover["x"])
			avisar("En el rover: más rápido y con espacio para 10. E para bajar.")
		"constructora":
			_entregar()
		"deposito":
			_cargar_combustible()
		"cohete":
			if listo_para_despegar():
				_despegar()
			elif fase < 4:
				avisar("El cohete va en la fase %d de 4. Lleva recursos a la constructora." % fase)
			else:
				avisar("Falta combustible o batería para despegar.")
		_:
			if montado:
				_bajar()


func _bajar() -> void:
	montado = false
	jugador.visible = true
	var sobra := _total(mochila) - CAPACIDAD
	for k in ["hielo", "regolito", "ilmenita", "caja"]:
		while sobra > 0 and int(mochila[k]) > 0:
			mochila[k] -= 1
			maletero[k] += 1
			sobra -= 1
	if _total(maletero) > 0:
		avisar("Dejaste %d cosas en el maletero del rover." % _total(maletero))


func _salir() -> void:
	dentro = null
	jugador.visible = true


func _refrescar(o: Dictionary) -> void:
	var n: Sprite2D = o["nodo"]
	if int(o["unidades"]) <= 0:
		n.visible = false
	elif o["tipo"] == "veta":
		n.modulate = Color(1, 1, 1).lerp(Color(0.6, 0.6, 0.7), 1.0 - float(o["unidades"]) / float(VETAS.get(o["id"], ["", 2])[1]))


func mantener(delta: float) -> void:
	if cerca == null or _habla != null or lanzando >= 0.0:
		_progreso = 0.0
		return
	var t: String = cerca["tipo"]
	if t == "veta":
		if montado:
			avisar("Baja del rover para extraer (E lejos de la veta).")
			return
		if barras["energia"] <= 3.0:
			avisar("Sin energía: recarga el traje en una estación de carga.")
			return
		if _total(mochila) >= _capacidad():
			avisar("Mochila llena: entrega en la constructora o usa el rover.")
			return
		_progreso += delta
		if _progreso >= T_EXTRAER:
			_progreso = 0.0
			mochila[cerca["recurso"]] += 1
			cerca["unidades"] -= 1
			barras["energia"] -= 3.0
			polvos.append({"x": cerca["x"], "y": suelo_en(cerca["x"]) - 6.0, "t": 0.0, "color": Color("c4c9de")})
			_refrescar(cerca)
	elif t == "panel" and not cerca["orientado"]:
		_progreso += delta
		if _progreso >= T_PANEL:
			_progreso = 0.0
			cerca["orientado"] = true
			paneles_orientados += 1
			(cerca["nodo"] as Sprite2D).modulate = Color.WHITE
			avisar("Panel limpio y orientado al Sol (%d de 3)." % paneles_orientados)
	else:
		_progreso = 0.0


func _disponible(k: String, destino_x: float) -> int:
	var n := int(mochila[k])
	if not montado and rover != null and absf(rover["x"] - destino_x) < 110.0:
		n += int(maletero[k])
	return n


func _gastar(k: String, n: int) -> void:
	var de_mochila := mini(n, int(mochila[k]))
	mochila[k] -= de_mochila
	maletero[k] -= n - de_mochila


func _entregar() -> void:
	if fase >= 4:
		avisar("El cohete ya está armado. Ahora necesita combustible y batería.")
		return
	var req: Dictionary = FASES[fase]
	var dado := 0
	for k in req:
		var falta := int(req[k]) - int(entregado[k])
		var n := mini(falta, _disponible(k, cerca["x"]))
		if n > 0:
			_gastar(k, n)
			entregado[k] += n
			dado += n
	var completa := true
	for k in req:
		if int(entregado[k]) < int(req[k]):
			completa = false
	if completa:
		fase += 1
		for k in ORDEN:
			entregado[k] = 0
		var s: Sprite2D = cohete["nodo"]
		s.texture = load(raiz + "/recursos/props/cohete_%d.png" % fase)
		s.modulate = Color(3, 3, 3)
		create_tween().tween_property(s, "modulate", Color.WHITE, 0.8)
		for i in 10:
			polvos.append({"x": cohete["x"] + randf_range(-24, 24), "y": s.position.y + randf_range(20, 150), "t": -i * 0.05, "color": Color("f2b134")})
		if fase < 4:
			avisar("¡Fase %d de 4 lista! La constructora armó %s." % [fase, PARTES[fase - 1]], 4.5)
		else:
			avisar("¡Cohete armado! Ahora: hielo al depósito y paneles al Sol.", 6.0)
	elif dado > 0:
		avisar("Entregaste %d. Falta: %s." % [dado, _texto_falta()])
	else:
		avisar("Falta: %s." % _texto_falta())


func _texto_falta() -> String:
	var partes: Array = []
	var req: Dictionary = FASES[fase]
	for k in req:
		var f := int(req[k]) - int(entregado[k])
		if f > 0:
			partes.append("%d de %s" % [f, NOMBRES[k]])
	return ", ".join(partes)


func _cargar_combustible() -> void:
	if fase < 4:
		avisar("Primero hay que armar el cohete.")
	elif combustible >= 100.0:
		avisar("El depósito está lleno.")
	else:
		var n := mini(int(ceil((100.0 - combustible) / 25.0)), _disponible("hielo", cerca["x"]))
		if n <= 0:
			avisar("Trae hielo del cráter en sombra, al final del mapa.")
		else:
			_gastar("hielo", n)
			combustible = minf(100.0, combustible + 25.0 * n)
			avisar("El hielo se convirtió en combustible: %d %%." % int(combustible))


func listo_para_despegar() -> bool:
	return fase >= 4 and combustible >= 100.0 and bateria >= 100.0


func _despegar() -> void:
	if montado:
		_bajar()
	lanzando = 0.0
	jugador.visible = false
	hud.burbuja = {}
	hud.aviso = "¡Despegue hacia Marte!"
	hud.objetivo = {}
	hud.pie = ""
	hud.alerta = {}
	hud.lluvia = 0.0


func _animar_despegue(delta: float) -> void:
	lanzando += delta
	var s: Sprite2D = cohete["nodo"]
	s.position.y -= (8.0 + 90.0 * lanzando * lanzando) * delta
	camara.position.x = cohete["x"] + randf_range(-1.5, 1.5)
	camara.position.y = 180.0 + randf_range(-1.5, 1.5)
	_fx.queue_redraw()
	if lanzando >= 3.4:
		lanzando = -2.0
		set_physics_process(false)
		despegue.emit({"tiempo": tiempo, "rescates": rescates})


# ---------- dialogos ----------
func _avanzar_dialogo() -> void:
	_linea += 1
	var d: Dictionary = dialogos.get(_habla["id"], {})
	var lineas: Array = d.get("lineas", [])
	var n: Node = _habla["nodo"]
	if _linea < lineas.size():
		hud.dialogo = {"nombre": d.get("nombre", ""), "texto": lineas[_linea]}
		n.play("hablar")
		n.mirar(jugador.position.x - n.position.x)
	elif _linea == lineas.size() and d.has("dato"):
		hud.dialogo = {"nombre": "Dato real", "texto": "%s\nFuente: %s" % [d["dato"], d.get("fuente", "")]}
	else:
		hud.dialogo = {}
		n.play("quieto")
		_habla = null


# ---------- eventos ----------
func _eventos(delta: float) -> void:
	if eventos_auto:
		t_lluvia -= delta
		if estado_lluvia == 0 and t_lluvia <= 0.0:
			iniciar_lluvia(12.0)
		t_meteoros -= delta
		if t_meteoros <= 0.0:
			t_meteoros = randf_range(45.0, 70.0)
			for i in randi_range(3, 4):
				var x := randf_range(40.0, ancho - 40.0)
				if i == 0:
					x = clampf(jugador.position.x + randf_range(-140.0, 140.0), 40.0, ancho - 40.0)
				if x > 500.0 and x < 1660.0:
					x = 1700.0 + randf() * 500.0      # la base queda fuera de la zona de impactos
				lanzar_meteorito(x, 2.0 + i * 0.5)
			avisar("¡Meteoritos! Aléjate de las marcas naranjas.", 3.5)
		t_carga -= delta
		if t_carga <= 0.0:
			t_carga = 110.0
			llegar_carga()
	elif estado_lluvia != 0:
		t_lluvia -= delta
	if estado_lluvia == 1 and t_lluvia <= 0.0:
		estado_lluvia = 2
		t_lluvia = 15.0
	elif estado_lluvia == 2 and t_lluvia <= 0.0:
		estado_lluvia = 0
		t_lluvia = randf_range(75.0, 100.0)
		avisar("La lluvia solar pasó.")
	for m in meteoros:
		m["t"] -= delta
		if m["t"] <= 0.0 and not m["cae"]:
			m["cae"] = true
			m["t"] = 0.7
			var s := Sprite2D.new()
			s.texture = load(raiz + "/recursos/props/meteorito.png")
			s.centered = false
			s.z_index = 9
			add_child(s)
			m["nodo"] = s
		if m["cae"]:
			var k := clampf(1.0 - m["t"] / 0.7, 0.0, 1.0)
			var fin := Vector2(m["x"], suelo_en(m["x"]))
			(m["nodo"] as Sprite2D).position = (fin - Vector2(260, 190)).lerp(fin, k) - Vector2(35, 19)
			if m["t"] <= 0.0:
				_impacto(m)
	meteoros = meteoros.filter(func(m): return not m.get("fin", false))
	for p in polvos:
		p["t"] += delta
	polvos = polvos.filter(func(p): return p["t"] < 0.6)


func iniciar_lluvia(aviso_s: float) -> void:
	estado_lluvia = 1 if aviso_s > 0.0 else 2
	t_lluvia = aviso_s if aviso_s > 0.0 else 15.0


func lanzar_meteorito(x: float, espera := 2.0) -> void:
	meteoros.append({"x": x, "t": espera, "cae": false})


func _impacto(m: Dictionary) -> void:
	m["fin"] = true
	(m["nodo"] as Node).queue_free()
	var x: float = m["x"]
	for i in 8:
		polvos.append({"x": x + randf_range(-14, 14), "y": suelo_en(x) - randf_range(0, 12), "t": -i * 0.02, "color": Color("f08a5d")})
	if dentro == null and absf(jugador.position.x - x) < 30.0 and jugador.position.y > suelo_en(x) - 50.0:
		barras["oxigeno"] -= 18.0
		barras["energia"] -= 10.0
		vel.y = -90.0
		en_suelo = false
		avisar("¡Un meteorito golpeó cerca! El traje perdió oxígeno.", 3.5)
	# el impacto deja a la vista una veta nueva, si hay sitio
	if x < 470.0 or x > 1690.0:
		for o in objetos:
			if absf(o["x"] - x) < o["w"] * 0.5 + 22.0:
				return
		var id := "veta_ilmenita" if randf() < 0.5 else "veta_regolito"
		var s := Sprite2D.new()
		s.texture = load(raiz + "/recursos/props/" + id + ".png")
		s.centered = false
		s.position = Vector2(x - 16.0, suelo_en(x) - 20.0)
		s.z_index = 2
		add_child(s)
		objetos.append({"id": id, "x": x, "w": 32.0, "nodo": s, "tipo": "veta", "recurso": VETAS[id][0], "unidades": 2})


func llegar_carga() -> void:
	var x := randf_range(130.0, 430.0)
	for o in objetos:
		if absf(o["x"] - x) < o["w"] * 0.5 + 26.0:
			return
	var s := Sprite2D.new()
	s.texture = load(raiz + "/recursos/props/pila.png")
	s.centered = false
	s.z_index = 2
	var fin := Vector2(x - 20.0, suelo_en(x) - 30.0)
	s.position = fin - Vector2(0, 240)
	add_child(s)
	create_tween().tween_property(s, "position", fin, 1.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	objetos.append({"id": "pila", "x": x, "w": 40.0, "nodo": s, "tipo": "cajas", "unidades": 3})
	avisar("Llegó carga de la Tierra a la pista (a la izquierda).", 4.0)


# ---------- dibujo ----------
func _dibujar_fx() -> void:
	for m in meteoros:
		if not m["cae"] and fmod(m["t"], 0.3) < 0.18:
			var y := suelo_en(m["x"])
			_fx.draw_rect(Rect2(m["x"] - 12, y - 2, 24, 2), Color("f08a5d"))
			_fx.draw_rect(Rect2(m["x"] - 1, y - 12, 2, 7), Color("f08a5d"))
			_fx.draw_rect(Rect2(m["x"] - 1, y - 4, 2, 2), Color("f08a5d"))
	for p in polvos:
		if p["t"] < 0.0:
			continue
		var r: float = 2.0 + float(p["t"]) * 22.0
		var c: Color = p["color"]
		c.a = 1.0 - float(p["t"]) / 0.6
		for i in 6:
			var a := -PI * (0.15 + 0.7 * i / 5.0)
			_fx.draw_rect(Rect2(Vector2(p["x"], p["y"]) + Vector2.from_angle(a) * r, Vector2(2, 2)), c)
	if lanzando >= 0.0 and cohete != null:
		var s: Sprite2D = cohete["nodo"]
		var base := s.position + Vector2(28, 152)
		for i in 14:
			var largo := randf_range(10.0, 26.0 + lanzando * 16.0)
			_fx.draw_rect(Rect2(base.x - 10 + i * 1.5, base.y, 2, largo), Color("ffe08a") if i % 3 == 0 else Color("f08a5d"))


func _actualizar_hud() -> void:
	var b := barras
	hud.barras = [
		["oxigeno", "Oxígeno", b["oxigeno"] / 100.0, b["oxigeno"] < 25.0],
		["energia", "Energía", b["energia"] / 100.0, b["energia"] < 20.0],
		["alimentos", "Alimentos", b["alimentos"] / 100.0, b["alimentos"] < 20.0],
		["radiacion", "Radiación", b["radiacion"] / 100.0, b["radiacion"] > 70.0],
	]
	var partes: Array = []
	for k in ORDEN:
		if int(mochila[k]) > 0:
			partes.append("%d %s" % [mochila[k], NOMBRES[k]])
	hud.mochila = ("Rover" if montado else "Mochila") + " %d/%d: %s" % [_total(mochila), _capacidad(), ", ".join(partes) if not partes.is_empty() else "vacía"]
	if fase < 4:
		var req: Dictionary = FASES[fase]
		var lineas: Array = ["Lleva a la constructora:"]
		for k in req:
			lineas.append("  %s %d/%d" % [NOMBRES[k].capitalize(), entregado[k], req[k]])
		hud.objetivo = {"titulo": "Objetivo 1: construye el cohete", "cuadros": [fase, 4], "lineas": lineas}
	elif not listo_para_despegar():
		hud.objetivo = {"titulo": "Objetivo 2: prepara el despegue", "lineas": [
			"Combustible %d %% (hielo al depósito)" % int(combustible),
			"Batería %d %% (paneles al Sol: %d/3)" % [int(bateria), paneles_orientados]]}
	else:
		hud.objetivo = {"titulo": "¡Todo listo!", "lineas": ["Ve al cohete y pulsa E para despegar."]}
	if estado_lluvia == 1:
		hud.alerta = {"titulo": "LLUVIA SOLAR", "texto": "Refúgiate en una cúpula: llega en %d s" % int(ceil(t_lluvia))}
		hud.lluvia = 0.0
	elif estado_lluvia == 2:
		hud.alerta = {"titulo": "LLUVIA SOLAR", "texto": ("A salvo. Faltan %d s" if dentro != null else "¡Entra en una cúpula! Faltan %d s") % int(ceil(t_lluvia))}
		hud.lluvia = 1.0
	else:
		hud.alerta = {}
		hud.lluvia = 0.0
	hud.aviso = _aviso if _t_aviso > 0.0 else ""
	hud.progreso = -1.0
	if cerca != null:
		var texto := _texto_accion(cerca)
		var alto := 46.0
		if cerca["tipo"] != "npc":
			alto = float((cerca["nodo"] as Sprite2D).texture.get_height()) + 10.0
		var ox: float = cerca["x"]
		var pos := Vector2(ox - (camara.position.x - 320.0), suelo_en(ox) - minf(alto, 150.0))
		hud.burbuja = {"texto": texto, "pos": pos, "color": Color("f2b134") if cerca["tipo"] in ["constructora", "deposito", "cohete"] else Color("62e4e0")}
		if _progreso > 0.0:
			hud.progreso = _progreso / (T_EXTRAER if cerca["tipo"] == "veta" else T_PANEL)
	else:
		hud.burbuja = {}


func _texto_accion(o: Dictionary) -> String:
	match o["tipo"]:
		"npc":
			return "E: hablar con " + String(dialogos.get(o["id"], {}).get("nombre", ""))
		"cajas":
			return "E: recoger caja (%d)" % o["unidades"]
		"veta":
			return "Mantén E: extraer %s (%d)" % [o["recurso"], o["unidades"]]
		"refugio":
			return "E: entrar a " + REFUGIOS[o["id"]]
		"rover":
			return "E: subir al rover"
		"constructora":
			return "E: entregar recursos" if fase < 4 else "Cohete armado"
		"deposito":
			return "E: cargar hielo (%d %%)" % int(combustible) if fase >= 4 else "Depósito de combustible"
		"panel":
			return "Panel orientado al Sol" if o["orientado"] else "Mantén E: orientar el panel"
		"cohete":
			return "E: ¡DESPEGAR!" if listo_para_despegar() else "Cohete: fase %d/4" % fase
	return ""
