extends Node2D

# Capitulo 3: Marte (Domenica). Reemplaza al nivel_marte.gd provisional: misma senal "terminado".
#  1. Llegada: los siete minutos de terror (aterrizaje.gd). Se programa el descenso y se prueba.
#  2. Superficie: tres banderas y la base (habitat, paneles, extractor de oxigeno, taladro de hielo, invernadero).
#     El dia avanza con el trabajo: dia -> atardecer -> noche (sin contador de soles).
#  3. Al atardecer llega una tormenta de polvo: hay que limpiar los paneles.
#  4. De noche: frio y lunas. Se levanta la antena y se envia el primer reporte a la Tierra (revisando las unidades).
# Los descubrimientos se guardan en el cuaderno de campo (cuaderno.gd). Nadie muere: el equipo te rescata.

signal terminado

const Personaje := preload("personaje.gd")
const Fondo := preload("fondo_marte.gd")
const Hud := preload("hud.gd")
const Aterrizaje := preload("aterrizaje.gd")
const Cuaderno := preload("cuaderno.gd")

const SUELO_Y := 304.0
const ANCHO := 1600.0
const CAMINAR := 80.0
const GRAVEDAD := 600.0           # Marte: 0,38 de la gravedad terrestre; el salto es mas corto que en la Luna
const SALTO := 158.0
const T_DESPLEGAR := 1.2
const T_LIMPIAR := 2.0
const X_COHETE := 120.0
const BANDERAS := [["bandera_usa", "Estados Unidos", 270.0], ["bandera_ecuador", "Ecuador", 310.0], ["bandera_ieee", "IEEE IAS — ESPOL", 350.0]]
# id, nombre, x, requiere
const MODULOS := [
	["cupula", "el hábitat", 520.0, ""],
	["paneles", "los paneles solares", 680.0, ""],
	["extractor", "el extractor de oxígeno", 845.0, "paneles"],
	["invernadero", "el invernadero", 1000.0, "taladro"],
	["taladro", "el taladro de hielo", 1230.0, "paneles"],
]
const GENTE := [["comandante", 190.0], ["medica", 430.0], ["ingeniero", 770.0], ["geologa", 1150.0]]
const X_ANTENA := 1440.0

var control_externo := false
var dir_externa := 0.0
var saltar_aterrizaje := false     # para probar solo la superficie

var raiz := ""
var datos := {}
var hud
var cuaderno
var aterrizaje
var camara: Camera2D
var jugador
var fondo
var mundo: Node2D
var objetos: Array = []           # {tipo, id, nombre, x, w, nodo, hecho, requiere}
var cerca = null
var dentro = null
var vel := Vector2.ZERO
var en_suelo := true
var barras := {"oxigeno": 100.0, "energia": 100.0, "alimentos": 100.0, "radiacion": 0.0}
var etapa := "llegada"            # llegada, banderas, base, tormenta, noche, reporte, envio, fin
var aterrizaje_resultado := ""
var banderas := 0
var modulos := 0
var hora := 0.0
var tormenta := 0                 # 0 nada, 1 aviso, 2 polvo
var t_tormenta := 0.0
var polvo_paneles := 0.0          # 0..1
var antena_lista := false
var rescates := 0
var saltos := 0
var tiempo := 0.0
var reporte_sel := 0
var reporte_ok := false
var reporte_msg := ""
var t_envio := 0.0

var _clima: Control
var _ui: Control
var _fuente: Font
var _luces: Array = []
var _progreso := 0.0
var _e_antes := false
var _s_antes := false
var _aviso := ""
var _t_aviso := 0.0
var _habla = null
var _linea := 0
var _anim := 0.0
var _rects := {}


func _ready() -> void:
	raiz = (get_script() as Script).resource_path.get_base_dir().get_base_dir()
	datos = (load(raiz + "/datos/marte.json") as JSON).data
	_fuente = preload("fuente_pixel.gd").obtener()
	fondo = Fondo.new()
	add_child(fondo)
	fondo.armar(raiz + "/recursos/fondos_marte")
	add_child(fondo.armar_suelo(raiz + "/recursos/nivel", ANCHO + 640.0, SUELO_Y))
	mundo = Node2D.new()
	mundo.z_index = 2
	add_child(mundo)
	var cohete := Sprite2D.new()
	cohete.texture = load(raiz + "/recursos/props/cohete_4.png")
	cohete.centered = false
	cohete.position = Vector2(X_COHETE - 28.0, SUELO_Y - 160.0)
	mundo.add_child(cohete)
	objetos.append({"tipo": "cohete", "id": "cohete", "nombre": "la nave", "x": X_COHETE, "w": 40.0, "nodo": cohete, "hecho": true})
	var hielo := Sprite2D.new()
	hielo.texture = load(raiz + "/recursos/props/veta_hielo.png")
	hielo.centered = false
	hielo.position = Vector2(1268.0, SUELO_Y - 20.0)
	mundo.add_child(hielo)
	for b in BANDERAS:
		_plano("bandera", b[0], b[1], b[2], "")
	for m in MODULOS:
		_plano("modulo", m[0], m[1], m[2], m[3])
	_plano("antena", "antena", "la antena", X_ANTENA, "")
	for g in GENTE:
		var n = Personaje.new()
		n.personaje = g[0]
		n.position = Vector2(g[1], SUELO_Y)
		mundo.add_child(n)
		objetos.append({"tipo": "npc", "id": g[0], "nombre": datos["dialogos"][g[0]]["nombre"], "x": g[1], "w": 20.0, "nodo": n, "hecho": false})
	jugador = Personaje.new()
	jugador.personaje = "jugador"
	jugador.position = Vector2(X_COHETE + 70.0, SUELO_Y)
	jugador.z_index = 3
	mundo.add_child(jugador)
	_crear_luces()
	camara = Camera2D.new()
	camara.position = Vector2(320, 180)
	add_child(camara)
	camara.make_current()
	# polvo y frio por encima del mundo, por debajo de la interfaz
	var capa_clima := CanvasLayer.new()
	capa_clima.layer = 4
	add_child(capa_clima)
	_clima = _lienzo_en(capa_clima, _dibujar_clima)
	hud = Hud.new()
	hud.capitulo = "Capítulo 3 — Marte"
	add_child(hud)
	hud._fuente = preload("fuente_pixel.gd").obtener()      # solo en Marte: la fuente pixel propia
	var capa_ui := CanvasLayer.new()
	capa_ui.layer = 11
	add_child(capa_ui)
	_ui = _lienzo_en(capa_ui, _dibujar_ui)
	cuaderno = Cuaderno.new()
	add_child(cuaderno)
	if saltar_aterrizaje:
		_al_aterrizar("suave")
	else:
		aterrizaje = Aterrizaje.new()
		aterrizaje.control_externo = control_externo
		aterrizaje.nota.connect(func(id): cuaderno.desbloquear(id))
		aterrizaje.aterrizo.connect(_al_aterrizar)
		add_child(aterrizaje)


func _lienzo_en(capa: CanvasLayer, f: Callable) -> Control:
	var l := Control.new()
	l.set_anchors_preset(Control.PRESET_FULL_RECT)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	l.draw.connect(f)
	capa.add_child(l)
	return l


func _plano(tipo: String, id: String, nombre: String, x: float, req: String) -> void:
	var s := Sprite2D.new()
	s.texture = load(raiz + "/recursos/props/" + id + ".png")
	s.centered = false
	s.position = Vector2(x - s.texture.get_width() * 0.5, SUELO_Y - s.texture.get_height())
	s.modulate = Color(0.38, 0.89, 0.88, 0.3)       # plano cian: todavia no existe
	mundo.add_child(s)
	objetos.append({"tipo": tipo, "id": id, "nombre": nombre, "x": x, "w": float(s.texture.get_width()), "nodo": s, "hecho": false, "requiere": req})


func _crear_luces() -> void:
	var tex := GradientTexture2D.new()
	tex.fill = GradientTexture2D.FILL_RADIAL
	tex.fill_from = Vector2(0.5, 0.5)
	tex.fill_to = Vector2(1.0, 0.5)
	tex.width = 64
	tex.height = 64
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 0.35))
	g.set_color(1, Color(1, 1, 1, 0.0))
	tex.gradient = g
	var mat := CanvasItemMaterial.new()
	mat.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	for l in [[520.0, 270.0, 90.0, Color("ffd08a"), "cupula"], [1000.0, 285.0, 110.0, Color("8fd46a"), "invernadero"], [845.0, 285.0, 50.0, Color("62e4e0"), "extractor"], [X_ANTENA, 222.0, 26.0, Color("f08a5d"), "antena"], [X_COHETE, 230.0, 60.0, Color("ffe08a"), "cohete"]]:
		var s := Sprite2D.new()
		s.texture = tex
		s.material = mat
		s.position = Vector2(l[0], l[1])
		s.scale = Vector2.ONE * float(l[2]) / 32.0
		s.modulate = l[3]
		s.z_index = 5
		s.visible = false
		add_child(s)
		_luces.append({"nodo": s, "id": l[4]})


func _buscar(id: String) -> Variant:
	for o in objetos:
		if o["id"] == id:
			return o
	return null


func _hecho(id: String) -> bool:
	var o = _buscar(id)
	return o != null and o["hecho"]


# ---------- llegada ----------
func _al_aterrizar(res: String) -> void:
	aterrizaje_resultado = res
	if aterrizaje != null:
		aterrizaje.queue_free()
		aterrizaje = null
	etapa = "banderas"
	hud.pie = "← → / A D: moverse  ·  Espacio: saltar  ·  E: usar / mantener: desplegar  ·  Tab: cuaderno"
	if res == "duro":
		barras["energia"] = 55.0
		avisar("Aterrizaje duro: la nave gastó energía. Habla con la comandante (E).", 5.0)
	else:
		avisar("¡Aterrizaje suave! Habla con la comandante (E).", 5.0)


# ---------- ciclo ----------
func _physics_process(delta: float) -> void:
	_anim += delta
	if etapa == "llegada":
		hud.barras = []
		hud.objetivo = {}
		hud.pie = ""
		return
	tiempo += delta
	var dir := dir_externa
	if not control_externo and etapa != "reporte" and etapa != "envio":
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
		if s and not _s_antes:
			saltar()
		_s_antes = s
	if _habla != null or etapa in ["reporte", "envio", "fin"]:
		dir = 0.0
	if dentro != null and dir != 0.0:
		_salir()
	_mover(delta, dir)
	_medidores(delta, dir)
	_eventos(delta)
	_buscar_cerca()
	_actualizar_hud()
	_clima.queue_redraw()
	_ui.queue_redraw()


func _mover(delta: float, dir: float) -> void:
	var pos: Vector2 = jugador.position
	if dentro == null:
		pos.x = clampf(pos.x + dir * CAMINAR * delta, 60.0, ANCHO - 30.0)
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


func saltar() -> void:
	if not en_suelo or dentro != null or _habla != null or etapa in ["llegada", "reporte", "envio", "fin"]:
		return
	vel.y = -SALTO
	en_suelo = false
	saltos += 1
	if saltos == 1:
		cuaderno.desbloquear("gravedad")


func _medidores(delta: float, dir: float) -> void:
	var b := barras
	var x: float = jugador.position.x
	var energia_base := _hecho("paneles") and polvo_paneles < 0.5
	b["alimentos"] -= 0.3 * delta
	b["energia"] -= 0.12 * delta
	if dentro != null:
		b["oxigeno"] += 22.0 * delta
		b["radiacion"] -= 8.0 * delta
		b["alimentos"] += (14.0 if dentro["id"] == "invernadero" else 4.0) * delta
		if energia_base:
			b["energia"] += 8.0 * delta
	else:
		b["oxigeno"] -= (0.9 if dir == 0.0 else 1.1) * delta
		b["radiacion"] += 0.35 * delta
		if hora > 1.2:
			b["energia"] -= 0.5 * delta * clampf(hora - 1.2, 0.0, 0.8) / 0.8      # calefaccion del traje
		var ext = _buscar("extractor")
		if ext["hecho"] and energia_base and absf(ext["x"] - x) < 40.0:
			b["oxigeno"] += 30.0 * delta
		if absf(X_COHETE - x) < 40.0:
			b["energia"] += 6.0 * delta
	for k in b:
		b[k] = clampf(b[k], 0.0, 100.0)
	if b["oxigeno"] <= 0.0:
		rescate("Te quedaste sin oxígeno")
	elif b["radiacion"] >= 100.0:
		rescate("Demasiada radiación")
	elif b["energia"] <= 0.0 and hora > 1.2:
		rescate("El traje se quedó sin energía para calentarse")


func rescate(causa: String) -> void:
	rescates += 1
	barras["oxigeno"] = 60.0
	barras["radiacion"] = 30.0
	barras["energia"] = maxf(barras["energia"], 45.0)
	barras["alimentos"] = maxf(barras["alimentos"], 40.0)
	var refugio := 520.0 if _hecho("cupula") else X_COHETE + 50.0
	teletransportar(refugio)
	avisar(causa + ": el equipo te llevó " + ("al hábitat." if _hecho("cupula") else "a la nave."), 5.0)


func teletransportar(x: float) -> void:
	if dentro != null:
		_salir()
	jugador.position = Vector2(x, SUELO_Y)
	vel = Vector2.ZERO
	en_suelo = true
	camara.position.x = clampf(x, 320.0, ANCHO - 320.0)
	_buscar_cerca()


func avisar(texto: String, dur := 3.5) -> void:
	_aviso = texto
	_t_aviso = dur


# ---------- tiempo, tormenta y noche ----------
func _eventos(delta: float) -> void:
	_t_aviso -= delta
	# el dia avanza con el trabajo hecho
	var meta := 0.0
	if etapa == "base" or etapa == "banderas":
		meta = modulos * 0.2
	elif etapa == "tormenta":
		meta = 1.0
	elif etapa in ["noche", "reporte", "envio", "fin"]:
		meta = 2.0
	hora = move_toward(hora, meta, delta * (0.12 if meta <= 1.0 else 0.18))
	fondo.poner_hora(hora)
	var tinte := Color(1, 1, 1)
	if hora <= 1.0:
		tinte = Color(1, 1, 1).lerp(Color(1.0, 0.86, 0.78), hora)
	else:
		tinte = Color(1.0, 0.86, 0.78).lerp(Color(0.6, 0.6, 0.86), hora - 1.0)
	if tormenta == 2:
		tinte = tinte.lerp(Color(0.85, 0.62, 0.45), 0.45)
	mundo.modulate = tinte
	for l in _luces:
		var s: Sprite2D = l["nodo"]
		var on: bool = _hecho(l["id"]) or l["id"] == "cohete"
		s.visible = on and hora > 1.0
		s.modulate.a = clampf(hora - 1.0, 0.0, 1.0) * (0.6 + 0.4 * absf(sin(_anim * 2.0)) if l["id"] == "antena" else 1.0)
	if hora >= 1.5 and etapa == "noche":
		cuaderno.desbloquear("frio")
	if hora >= 1.95 and etapa == "noche":
		cuaderno.desbloquear("lunas")
	# tormenta: llega cuando la base esta completa y el Sol ya va bajando
	if etapa == "base" and modulos >= MODULOS.size() and hora >= 0.95 and tormenta == 0:
		iniciar_tormenta(6.0)
	if tormenta == 1:
		t_tormenta -= delta
		if t_tormenta <= 0.0:
			tormenta = 2
			t_tormenta = 14.0
			polvo_paneles = 1.0
			cuaderno.desbloquear("polvo")
			avisar("El polvo cubrió los paneles: sin energía, el extractor se detuvo.", 5.0)
	elif tormenta == 2:
		t_tormenta -= delta
		if t_tormenta <= 0.0 and polvo_paneles <= 0.0:
			tormenta = 0
			etapa = "noche"
			avisar("La tormenta pasó. Cae la noche: levanta la antena y llama a la Tierra.", 5.0)


func iniciar_tormenta(aviso_s: float) -> void:
	etapa = "tormenta"
	tormenta = 1 if aviso_s > 0.0 else 2
	t_tormenta = aviso_s
	if tormenta == 2:
		polvo_paneles = 1.0
		t_tormenta = 14.0


# ---------- interaccion ----------
func _buscar_cerca() -> void:
	cerca = null
	if dentro != null or etapa == "llegada":
		return
	var x: float = jugador.position.x
	var mejor := 1e9
	for o in objetos:
		var tp: String = o["tipo"]
		var util := false
		match tp:
			"bandera":
				util = not o["hecho"]
			"modulo":
				util = (not o["hecho"] and banderas >= 3) or (o["hecho"] and o["id"] in ["cupula", "invernadero"]) or (o["id"] == "paneles" and polvo_paneles > 0.0)
			"npc":
				util = true
			"antena":
				util = etapa == "noche"
			"cohete":
				util = false
		if not util:
			continue
		var d := absf(o["x"] - x)
		if d < o["w"] * 0.5 + 12.0 and d < mejor:
			mejor = d
			cerca = o


func interactuar() -> void:
	if etapa == "reporte":
		_confirmar_reporte()
		return
	if _habla != null:
		_avanzar_dialogo()
		return
	if dentro != null:
		_salir()
		return
	if cerca == null:
		return
	var o: Dictionary = cerca
	match o["tipo"]:
		"npc":
			_habla = o
			_linea = -1
			_avanzar_dialogo()
		"bandera":
			_construir(o)
			banderas += 1
			if banderas < 3:
				avisar("Bandera de %s plantada (%d de 3)." % [o["nombre"], banderas])
			else:
				etapa = "base"
				avisar("¡Las tres banderas ondean en Marte! Ahora, la base.")
		"modulo":
			if o["hecho"] and o["id"] in ["cupula", "invernadero"]:
				_entrar(o)
		"antena":
			if antena_lista:
				abrir_reporte()


func mantener(delta: float) -> void:
	if cerca == null or _habla != null or dentro != null:
		_progreso = 0.0
		return
	var o: Dictionary = cerca
	if o["tipo"] == "modulo" and o["id"] == "paneles" and o["hecho"] and polvo_paneles > 0.0:
		polvo_paneles = maxf(0.0, polvo_paneles - delta / T_LIMPIAR)
		_progreso = 1.0 - polvo_paneles
		if polvo_paneles <= 0.0:
			_progreso = 0.0
			avisar("Paneles limpios: vuelve la energía.")
		return
	var desplegable: bool = (o["tipo"] == "modulo" and not o["hecho"]) or (o["tipo"] == "antena" and not antena_lista)
	if not desplegable or not _puede(o):
		_progreso = 0.0
		return
	_progreso += delta
	if _progreso >= T_DESPLEGAR:
		_progreso = 0.0
		_construir(o)
		if o["tipo"] == "antena":
			antena_lista = true
			avisar("Antena lista. Pulsa E para escribir el reporte.")
			return
		modulos += 1
		avisar("Desplegaste %s (%d de %d)." % [o["nombre"], modulos, MODULOS.size()])
		match o["id"]:
			"paneles":
				cuaderno.desbloquear("sol")
			"extractor":
				cuaderno.desbloquear("aire")
				cuaderno.desbloquear("moxie")
			"taladro":
				cuaderno.desbloquear("hielo")


func _puede(o: Dictionary) -> bool:
	if o["tipo"] == "modulo":
		return banderas >= 3 and (String(o["requiere"]) == "" or _hecho(o["requiere"]))
	return true


func _construir(o: Dictionary) -> void:
	o["hecho"] = true
	var s: Sprite2D = o["nodo"]
	s.modulate = Color(3, 3, 3, 1)
	create_tween().tween_property(s, "modulate", Color.WHITE, 0.6)


func _entrar(o: Dictionary) -> void:
	dentro = o
	jugador.visible = false
	jugador.position.x = o["x"]


func _salir() -> void:
	dentro = null
	jugador.visible = true


func _avanzar_dialogo() -> void:
	_linea += 1
	var d: Dictionary = datos["dialogos"][_habla["id"]]
	var lineas: Array = d["lineas"]
	var n: Node = _habla["nodo"]
	if _linea < lineas.size():
		hud.dialogo = {"nombre": d["nombre"], "texto": lineas[_linea]}
		n.play("hablar")
		n.mirar(jugador.position.x - n.position.x)
	else:
		hud.dialogo = {}
		n.play("quieto")
		if d.has("nota"):
			cuaderno.desbloquear(d["nota"])
		_habla = null


# ---------- reporte a la Tierra ----------
func abrir_reporte() -> void:
	etapa = "reporte"
	_t_aviso = 0.0
	reporte_sel = 0
	reporte_ok = false
	reporte_msg = "Una línea no está en sistema métrico. Elígela con ↑ ↓ y pulsa E."


func elegir_reporte(i: int) -> void:
	if etapa == "reporte" and not reporte_ok:
		reporte_sel = clampi(i, 0, 3)


func _confirmar_reporte() -> void:
	var r: Dictionary = datos["reporte"]
	if reporte_ok:
		enviar()
		return
	if reporte_sel == int(r["correcta"]):
		reporte_ok = true
		reporte_msg = String(r["explicacion"])
		cuaderno.desbloquear("unidades")
	else:
		reporte_msg = String(r["lineas"][reporte_sel][1])


func enviar() -> void:
	if etapa == "reporte" and reporte_ok:
		etapa = "envio"
		t_envio = 0.0


func _process(delta: float) -> void:
	if etapa == "envio":
		t_envio += delta
		if t_envio >= 7.0:
			etapa = "fin"
			terminado.emit()


func _input(evento: InputEvent) -> void:
	if control_externo or get_tree().paused or etapa != "reporte":
		return
	var tecla := evento as InputEventKey
	if tecla != null and tecla.pressed and not tecla.echo:
		if tecla.keycode in [KEY_UP, KEY_W]:
			elegir_reporte(reporte_sel - 1)
		elif tecla.keycode in [KEY_DOWN, KEY_S]:
			elegir_reporte(reporte_sel + 1)
	var clic := evento as InputEventMouseButton
	if clic != null and clic.pressed and clic.button_index == MOUSE_BUTTON_LEFT:
		var p: Vector2 = _ui.get_local_mouse_position()
		for k in _rects:
			if (_rects[k] as Rect2).has_point(p):
				if k == "enviar":
					enviar()
				else:
					elegir_reporte(int(k))
					_confirmar_reporte()


# ---------- interfaz ----------
func temperatura() -> int:
	if hora <= 1.0:
		return int(round(lerpf(-31.0, -55.0, hora)))
	return int(round(lerpf(-55.0, -89.0, hora - 1.0)))


func _actualizar_hud() -> void:
	var b := barras
	hud.barras = [
		["oxigeno", "Oxígeno", b["oxigeno"] / 100.0, b["oxigeno"] < 25.0],
		["energia", "Energía", b["energia"] / 100.0, b["energia"] < 20.0],
		["alimentos", "Alimentos", b["alimentos"] / 100.0, b["alimentos"] < 20.0],
		["radiacion", "Radiación", b["radiacion"] / 100.0, b["radiacion"] > 70.0],
	]
	hud.mochila = "Temperatura exterior: %d °C" % temperatura()
	match etapa:
		"banderas":
			hud.objetivo = {"titulo": "Objetivo 3: planta las banderas", "cuadros": [banderas, 3], "lineas": ["Estados Unidos, Ecuador e IEEE IAS"]}
		"base":
			hud.objetivo = {"titulo": "Objetivo 4: levanta la base", "cuadros": [modulos, MODULOS.size()], "lineas": [_siguiente_modulo(), "Mantén E junto a cada plano"]}
		"tormenta":
			if polvo_paneles > 0.0 and tormenta == 2:
				hud.objetivo = {"titulo": "¡Tormenta de polvo!", "lineas": ["Limpia los paneles (mantén E)", "Polvo: %d %%" % int(polvo_paneles * 100.0)]}
			else:
				hud.objetivo = {"titulo": "¡Tormenta de polvo!", "lineas": ["Espera a que pase en el hábitat"]}
		"noche", "reporte", "envio":
			hud.objetivo = {"titulo": "Objetivo final: llama a la Tierra", "lineas": ["Levanta la antena y envía el reporte" if not antena_lista else "Antena lista: pulsa E junto a ella"]}
		_:
			hud.objetivo = {}
	if tormenta == 1:
		hud.alerta = {"titulo": "TORMENTA DE POLVO", "texto": "Llega en %d s: protege los paneles" % int(ceil(t_tormenta))}
	else:
		hud.alerta = {}
	hud.aviso = _aviso if _t_aviso > 0.0 else ""
	hud.progreso = -1.0
	if cerca != null and _habla == null and etapa != "reporte":
		var o: Dictionary = cerca
		var alto := 46.0
		if o["tipo"] != "npc":
			alto = float((o["nodo"] as Sprite2D).texture.get_height()) + 10.0
		var pos := Vector2(o["x"] - (camara.position.x - 320.0), SUELO_Y - minf(alto, 150.0))
		var texto := _texto_accion(o)
		var bloqueado: bool = (o["tipo"] == "modulo" and not o["hecho"] and not _puede(o))
		hud.burbuja = {"texto": texto, "pos": pos, "color": Color("f08a5d") if bloqueado else (Color("f2b134") if o["tipo"] in ["antena", "bandera"] else Color("62e4e0"))}
		if _progreso > 0.0:
			hud.progreso = _progreso if o["id"] == "paneles" and polvo_paneles > 0.0 else _progreso / T_DESPLEGAR
	else:
		hud.burbuja = {}


func _siguiente_modulo() -> String:
	for m in MODULOS:
		var o = _buscar(m[0])
		if not o["hecho"] and _puede(o):
			return "Sigue: " + String(m[1])
	return "Despliega los módulos"


func _texto_accion(o: Dictionary) -> String:
	match o["tipo"]:
		"npc":
			return "E: hablar con " + String(o["nombre"])
		"bandera":
			return "E: plantar la bandera de " + String(o["nombre"])
		"modulo":
			if o["id"] == "paneles" and o["hecho"] and polvo_paneles > 0.0:
				return "Mantén E: limpiar el polvo de los paneles"
			if o["hecho"]:
				return "E: entrar " + String(o["nombre"]).replace("el ", "al ")
			if not _puede(o):
				var req = _buscar(o["requiere"])
				return "Necesita " + String(req["nombre"]) + (": aún no hay energía" if o["requiere"] == "paneles" else ": aún no hay agua")
			return "Mantén E: desplegar " + String(o["nombre"])
		"antena":
			return "E: escribir el reporte para la Tierra" if antena_lista else "Mantén E: levantar la antena"
	return ""


func _txt(c: Control, pos: Vector2, s: String, color: Color, tam := 8, ancho := -1.0, alin := HORIZONTAL_ALIGNMENT_LEFT) -> void:
	c.draw_string(_fuente, pos + Vector2(0.5, 0.5), s, alin, ancho, tam, Color(0, 0, 0, 0.7))
	c.draw_string(_fuente, pos, s, alin, ancho, tam, color)


func _dibujar_clima() -> void:
	var c := _clima
	var ox := camara.position.x - 320.0 if camara != null else 0.0
	# polvo sobre los paneles (en el mundo, convertido a pantalla)
	var pan = _buscar("paneles")
	if pan != null and pan["hecho"] and polvo_paneles > 0.0:
		var s: Sprite2D = pan["nodo"]
		var r := Rect2(s.position - Vector2(ox, 0), s.texture.get_size())
		for k in 90:
			if float(k) / 90.0 < polvo_paneles:
				var q := r.position + Vector2(float((k * 37) % int(r.size.x)), float((k * 23) % 26) + 2.0)
				c.draw_rect(Rect2(q, Vector2(3, 2)), Color("c99a6b", 0.95))
	if tormenta == 2:
		c.draw_rect(Rect2(0, 0, 640, 360), Color(0.78, 0.45, 0.25, 0.38))
		for i in 160:
			var x := fposmod(float((i * 7919) % 760) - _anim * (260.0 + (i % 5) * 40.0), 760.0) - 60.0
			var y := float((i * 4391) % 340) + sin(_anim * 3.0 + i) * 4.0
			c.draw_line(Vector2(x, y), Vector2(x + 6.0 + (i % 7), y + 1.0), Color("e8b07a", 0.55), 1.0)
	elif tormenta == 1:
		c.draw_rect(Rect2(0, 0, 640, 360), Color(0.78, 0.45, 0.25, 0.1 * (1.0 - t_tormenta / 6.0)))


func _dibujar_ui() -> void:
	var c := _ui
	_rects.clear()
	if etapa == "reporte":
		var r: Dictionary = datos["reporte"]
		var caja := Rect2(120, 96, 400, 176)
		c.draw_rect(caja, Color(0.043, 0.055, 0.102, 0.95))
		c.draw_rect(caja, Color("f2b134"), false, 1.0)
		_txt(c, caja.position + Vector2(0, 18), "Primer reporte para la Tierra", Color("f2b134"), 16, caja.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		_txt(c, caja.position + Vector2(0, 32), "El centro de control trabaja en sistema métrico. Revisa antes de enviar.", Color("aeb6c8"), 7, caja.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		for i in 4:
			var fila := Rect2(caja.position.x + 40, caja.position.y + 42 + i * 20, 320, 16)
			var sel := i == reporte_sel
			var texto: String = r["lineas"][i][0]
			if reporte_ok and i == int(r["correcta"]):
				texto = r["corregida"]
			c.draw_rect(fila, Color("232a40") if not sel else Color(0.38, 0.89, 0.88, 0.18))
			if sel:
				c.draw_rect(fila, Color("62e4e0"), false, 1.0)
			_txt(c, fila.position + Vector2(10, 12), texto, Color("8fd46a") if reporte_ok and i == int(r["correcta"]) else Color("f2efe6"), 8)
			_rects[str(i)] = fila
		c.draw_multiline_string(_fuente, caja.position + Vector2(24, 136), reporte_msg, HORIZONTAL_ALIGNMENT_CENTER, caja.size.x - 48, 8, 2, Color("f2efe6"))
		if reporte_ok:
			var b := Rect2(caja.position.x + 130, caja.end.y - 20, 140, 15)
			c.draw_rect(b, Color(0.3, 0.2, 0.05, 0.9))
			c.draw_rect(b, Color("f2b134"), false, 1.0)
			_txt(c, b.position + Vector2(0, 11), "Enviar a la Tierra  (E)", Color("f2b134"), 7, b.size.x, HORIZONTAL_ALIGNMENT_CENTER)
			_rects["enviar"] = b
	elif etapa == "envio" or etapa == "fin":
		var k := clampf(t_envio / 4.5, 0.0, 1.0)
		var caja := Rect2(100, 110, 440, 120)
		c.draw_rect(caja, Color(0.02, 0.025, 0.05, 0.95))
		c.draw_rect(caja, Color("62e4e0"), false, 1.0)
		var m := caja.position + Vector2(50, 52)
		var t := caja.position + Vector2(390, 52)
		c.draw_circle(m, 14, Color("c2683a"))
		c.draw_circle(m + Vector2(-4, -4), 4, Color("d9864f"))
		c.draw_circle(t, 12, Color("3f86a8"))
		c.draw_circle(t + Vector2(-3, -3), 4, Color("8fd46a"))
		_txt(c, m + Vector2(-30, 30), "Marte", Color("aeb6c8"), 7, 60, HORIZONTAL_ALIGNMENT_CENTER)
		_txt(c, t + Vector2(-30, 30), "Tierra", Color("aeb6c8"), 7, 60, HORIZONTAL_ALIGNMENT_CENTER)
		for i in 30:
			var x := lerpf(m.x + 18, t.x - 16, i / 29.0)
			if i / 29.0 <= k:
				c.draw_rect(Rect2(x, m.y - 1, 4, 2), Color("62e4e0", 0.5))
		var punto := m.lerp(t, k) + Vector2(lerpf(18, -16, k), 0)
		c.draw_circle(punto, 3.0, Color("ffffff"))
		var minutos := int(round(lerpf(0.0, 11.0, k)))
		_txt(c, caja.position + Vector2(0, 18), "La señal viaja a la velocidad de la luz…", Color("f2efe6"), 9, caja.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		_txt(c, caja.position + Vector2(0, 94), "%d de 11 minutos" % minutos, Color("aeb6c8"), 7, caja.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		if t_envio > 4.8:
			_txt(c, caja.position + Vector2(0, 110), "Centro de control: «Recibido. Bienvenidos a Marte, equipo.»", Color("8fd46a"), 8, caja.size.x, HORIZONTAL_ALIGNMENT_CENTER)
