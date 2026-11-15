extends Node2D

# Llegada a Marte: "siete minutos de terror".
# La senal tarda varios minutos entre la Tierra y Marte, asi que nadie puede pilotear el descenso en vivo:
# el jugador programa la secuencia (paracaidas, cohetes, navegacion por terreno), la prueba en el simulador
# y ve si la nave aterriza suave, con un golpe fuerte o si se perderia. Nunca hay muerte: se ajusta y se repite.
# Valores reales de referencia (Perseverance, NASA 2021): paracaidas a unos 11 km, cohetes desde unos 2,1 km.
# Las demas cifras de la simulacion son un modelo simplificado.

signal aterrizo(resultado)            # "suave" o "duro"
signal nota(id)                       # pide una pagina del cuaderno

const CREMA := Color("f6e8c8")
const TINTA := Color("4a3322")
const FONDO := Color(0.043, 0.055, 0.102, 0.88)
const BORDE := Color("33405e")
const BLANCO := Color("f2efe6")
const SUAVE := Color("aeb6c8")
const CIAN := Color("62e4e0")
const AMBAR := Color("f2b134")
const ROSA := Color("e0559a")
const NARANJA := Color("f08a5d")
const VERDE := Color("8fd46a")

const PAR_MIN := 2.0
const PAR_MAX := 20.0
const COH_MIN := 0.5
const COH_MAX := 5.0
const T_ENTRADA := 5.0               # segundos reales de cada tramo del descenso
const T_PARACAIDAS := 4.5
const T_COHETES := 4.0

var control_externo := false
var estado := "programa"             # programa, descenso, resultado, llegada
var alt_paracaidas := 18.0           # km
var alt_cohetes := 0.6               # km
var navegacion := false
var fila := 0
var intentos := 0
var resultado := ""                  # suave, duro, perdida
var causa := ""                      # clave de la explicacion
var t := 0.0                         # tiempo real dentro del descenso

var _capa: CanvasLayer
var _lienzo: Control
var _fuente: Font
var _cohete: Texture2D
var _montes: Array = []
var _suelo: Texture2D
var _estrellas: Array = []
var _rects := {}                     # zonas para el raton
var _t_llegada := 0.0
var _anim := 0.0


func _ready() -> void:
	var raiz: String = (get_script() as Script).resource_path.get_base_dir().get_base_dir()
	_cohete = load(raiz + "/recursos/props/cohete_4.png")
	for k in ["capa_1_montanas_lejanas", "capa_2_montanas_medias", "capa_3_colinas_cercanas"]:
		_montes.append(load(raiz + "/recursos/fondos_marte/dia/" + k + ".png"))
	_suelo = load(raiz + "/recursos/nivel/suelo_marte_dia.png")
	var rng := RandomNumberGenerator.new()
	rng.seed = 42
	for i in 140:
		_estrellas.append(Vector3(rng.randf() * 640.0, rng.randf() * 360.0, rng.randf()))
	_fuente = preload("fuente_pixel.gd").obtener()
	_capa = CanvasLayer.new()
	_capa.layer = 5
	add_child(_capa)
	_lienzo = Control.new()
	_lienzo.set_anchors_preset(Control.PRESET_FULL_RECT)
	_lienzo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_lienzo.draw.connect(_dibujar)
	_capa.add_child(_lienzo)


# ---------- programa ----------
func programar(paracaidas: float, cohetes: float, trn: bool) -> void:
	alt_paracaidas = clampf(snappedf(paracaidas, 1.0), PAR_MIN, PAR_MAX)
	alt_cohetes = clampf(snappedf(cohetes, 0.1), COH_MIN, COH_MAX)
	navegacion = trn


func ajustar(d: int) -> void:
	match fila:
		0:
			alt_paracaidas = clampf(alt_paracaidas + d, PAR_MIN, PAR_MAX)
		1:
			alt_cohetes = clampf(snappedf(alt_cohetes + d * 0.1, 0.1), COH_MIN, COH_MAX)
		2:
			navegacion = not navegacion


func probar() -> void:
	intentos += 1
	_evaluar()
	estado = "descenso"
	t = 0.0


func _evaluar() -> void:
	resultado = "suave"
	causa = ""
	if alt_paracaidas > 13.0:
		resultado = "perdida"
		causa = "rasgado"
	elif alt_paracaidas < 7.0:
		resultado = "perdida"
		causa = "poco_freno"
	elif alt_cohetes < 1.0:
		resultado = "perdida"
		causa = "cohetes_tarde"
	elif alt_cohetes > 3.0:
		resultado = "duro"
		causa = "cohetes_pronto"
	elif not navegacion:
		resultado = "duro"
		causa = "rocas"


# tiempo real en que la simulacion se corta
func _t_fin() -> float:
	match causa:
		"rasgado":
			return T_ENTRADA + 1.6
		"poco_freno":
			return T_ENTRADA + T_PARACAIDAS + 0.8
		"cohetes_tarde":
			return T_ENTRADA + T_PARACAIDAS + T_COHETES * 0.45
	return T_ENTRADA + T_PARACAIDAS + T_COHETES + 1.2


func aceptar() -> void:
	# el programa probado se envia a la nave real
	if estado == "resultado" and resultado != "perdida":
		estado = "llegada"
		_t_llegada = 0.0
		nota.emit("siete")


func reprogramar() -> void:
	if estado == "resultado":
		estado = "programa"


func _process(delta: float) -> void:
	_anim += delta
	if estado == "descenso":
		t += delta
		if t >= _t_fin():
			estado = "resultado"
			nota.emit("senal")
	elif estado == "llegada":
		_t_llegada += delta
		if _t_llegada >= 4.0:
			estado = "fin"
			aterrizo.emit(resultado)
	_lienzo.queue_redraw()


func _input(evento: InputEvent) -> void:
	if control_externo or get_tree().paused:
		return
	var tecla := evento as InputEventKey
	if tecla != null and tecla.pressed:
		var k := tecla.keycode
		if estado == "programa":
			if k in [KEY_UP, KEY_W]:
				fila = (fila + 2) % 3
			elif k in [KEY_DOWN, KEY_S]:
				fila = (fila + 1) % 3
			elif k in [KEY_LEFT, KEY_A]:
				ajustar(-1)
			elif k in [KEY_RIGHT, KEY_D]:
				ajustar(1)
			elif k in [KEY_ENTER, KEY_KP_ENTER, KEY_SPACE] and not tecla.echo:
				probar()
		elif estado == "resultado" and not tecla.echo:
			if k in [KEY_ENTER, KEY_KP_ENTER, KEY_SPACE]:
				if resultado == "perdida":
					reprogramar()
				else:
					aceptar()
			elif k == KEY_E:
				reprogramar()
	var clic := evento as InputEventMouseButton
	if clic != null and clic.pressed and clic.button_index == MOUSE_BUTTON_LEFT:
		var p: Vector2 = _lienzo.get_local_mouse_position()
		for nombre in _rects:
			if (_rects[nombre] as Rect2).has_point(p):
				_clic(nombre)
				return


func _clic(nombre: String) -> void:
	if estado == "programa":
		if nombre.begins_with("menos") or nombre.begins_with("mas"):
			fila = int(nombre.right(1))
			ajustar(-1 if nombre.begins_with("menos") else 1)
		elif nombre.begins_with("fila"):
			fila = int(nombre.right(1))
		elif nombre == "probar":
			probar()
	elif estado == "resultado":
		if nombre == "aceptar":
			aceptar()
		elif nombre == "ajustar":
			reprogramar()


# ---------- modelo simplificado del descenso ----------
# devuelve [altitud km, velocidad km/h, tiempo simulado s, fase]
func perfil(tr: float) -> Array:
	var hc := alt_paracaidas
	var hr := alt_cohetes
	var vc := 1512.0 + (hc - 11.0) * 260.0 if hc >= 11.0 else 1512.0 - (11.0 - hc) * 70.0
	if tr < T_ENTRADA:
		var k := tr / T_ENTRADA
		var h := lerpf(125.0, hc, 1.0 - pow(1.0 - k, 1.6))
		return [h, lerpf(20000.0, vc, pow(k, 0.7)), lerpf(0.0, 240.0, k), "Entrada"]
	tr -= T_ENTRADA
	if tr < T_PARACAIDAS:
		var k := tr / T_PARACAIDAS
		var vfin := 320.0 if causa != "poco_freno" else 900.0
		if causa == "rasgado":
			vfin = vc
		return [lerpf(hc, hr, k), lerpf(vc, vfin, sqrt(k)), lerpf(240.0, 360.0, k), "Paracaídas"]
	tr -= T_PARACAIDAS
	var k := clampf(tr / T_COHETES, 0.0, 1.0)
	var v := lerpf(320.0, 2.0, k)
	if causa == "cohetes_tarde" or causa == "poco_freno":
		v = lerpf(320.0 if causa == "cohetes_tarde" else 900.0, 260.0, k)
	return [lerpf(hr, 0.0, k), v, lerpf(360.0, 420.0, k), "Cohetes" if k < 1.0 else "En el suelo"]


static func numero(v: float, dec := 0) -> String:
	var s := ("%." + str(dec) + "f") % v
	var partes := s.split(".")
	var ent: String = partes[0]
	var con := ""
	while ent.length() > 3:
		con = " " + ent.right(3) + con
		ent = ent.left(ent.length() - 3)
	con = ent + con
	if dec > 0:
		con += "," + partes[1]
	return con


func explicacion() -> Array:
	match causa:
		"rasgado":
			return ["A %d km la nave todavía iba muy rápido: el paracaídas se abrió" % int(alt_paracaidas),
				"con tanta fuerza que la tela se rasgó. Ábrelo más abajo, cuando ya frenó un poco.",
				"Perseverance lo abrió a unos 11 km de altura."]
		"poco_freno":
			return ["A %d km quedaba muy poco aire por delante: el paracaídas no alcanzó" % int(alt_paracaidas),
				"a frenar la nave y los cohetes no pudieron con tanta velocidad.",
				"Ábrelo más arriba: Perseverance lo abrió a unos 11 km."]
		"cohetes_tarde":
			return ["Los cohetes se encendieron a %s km: demasiado cerca del suelo." % numero(alt_cohetes, 1),
				"No hubo tiempo de frenar la caída. Enciéndelos más arriba;",
				"Perseverance se soltó del paracaídas a unos 2,1 km."]
		"cohetes_pronto":
			return ["Los cohetes se encendieron a %s km: muy pronto." % numero(alt_cohetes, 1),
				"Gastaron el combustible antes de llegar y la nave cayó los últimos metros.",
				"Llegarías, pero con un golpe fuerte. Prueba entre 1 y 3 km."]
		"rocas":
			return ["Sin navegación por terreno, la nave no vio las rocas del valle",
				"y se posó sobre ellas, inclinada. Con la cámara activada elige sola",
				"un lugar plano, como hizo Perseverance en el cráter Jezero."]
	return ["Paracaídas a %d km, cohetes a %s km y navegación por terreno:" % [int(alt_paracaidas), numero(alt_cohetes, 1)],
		"la nave frenó paso a paso y se posó en un lugar plano.",
		"Así aterrizó Perseverance en 2021."]


# ---------- dibujo ----------
func _txt(pos: Vector2, s: String, color: Color, tam := 8, ancho := -1.0, alin := HORIZONTAL_ALIGNMENT_LEFT) -> void:
	_lienzo.draw_string(_fuente, pos + Vector2(0.5, 0.5), s, alin, ancho, tam, Color(0, 0, 0, 0.7))
	_lienzo.draw_string(_fuente, pos, s, alin, ancho, tam, color)


func _caja(r: Rect2, borde: Color, fondo := FONDO) -> void:
	_lienzo.draw_rect(r, fondo)
	_lienzo.draw_rect(r, borde, false, 1.0)


func _dibujar() -> void:
	_rects.clear()
	if estado == "fin":
		return
	if estado == "programa":
		_cielo(125.0)
		_programa()
	elif estado == "llegada":
		_llegada()
	else:
		var tr := minf(t, _t_fin())
		var p := perfil(tr)
		_escena(tr, p)
		if estado == "resultado":
			_resultado()
		else:
			_telemetria(p)


func _cielo(h: float) -> void:
	var c := _lienzo
	# del negro del espacio al cielo polvoriento, segun la altura
	var k := clampf((60.0 - h) / 52.0, 0.0, 1.0)
	var arriba := Color("0b0e1a").lerp(Color("b65a2e"), k)
	var abajo := Color("1b1530").lerp(Color("f2be82"), k)
	for i in 24:
		c.draw_rect(Rect2(0, i * 15, 640, 15), arriba.lerp(abajo, i / 23.0))
	for e in _estrellas:
		var s: Vector3 = e
		var a := (1.0 - k) * (0.4 + 0.6 * s.z)
		if a > 0.05:
			c.draw_rect(Rect2(s.x, s.y, 1, 1), Color(1, 0.95, 0.85, a))
	# Marte visto desde arriba: una curva naranja que crece al bajar
	if h > 8.0:
		var r := lerpf(900.0, 3000.0, clampf((125.0 - h) / 117.0, 0.0, 1.0))
		var centro := Vector2(320, 360 + r - lerpf(40.0, 150.0, clampf((125.0 - h) / 117.0, 0.0, 1.0)))
		c.draw_circle(centro, r + 6.0, Color(0.95, 0.6, 0.35, 0.25))
		c.draw_circle(centro, r, Color("c2683a"))
		c.draw_circle(centro + Vector2(0, 30), r, Color("a8502e"))


func _programa() -> void:
	var c := _lienzo
	_caja(Rect2(70, 16, 500, 52), CREMA)
	_txt(Vector2(70, 33), "Siete minutos de terror", CREMA, 16, 500, HORIZONTAL_ALIGNMENT_CENTER)
	_txt(Vector2(70, 50), "La señal tarda unos 11 minutos en llegar a la Tierra y el descenso dura 7: nadie puede", BLANCO, 7, 500, HORIZONTAL_ALIGNMENT_CENTER)
	_txt(Vector2(70, 61), "ayudarte en vivo. Programa la secuencia y pruébala en el simulador antes de enviarla.", BLANCO, 7, 500, HORIZONTAL_ALIGNMENT_CENTER)
	# regla de altura
	var x := 84.0
	var y0 := 86.0
	var y1 := 304.0
	_caja(Rect2(40, 78, 96, 236), BORDE)
	c.draw_line(Vector2(x, y0), Vector2(x, y1), SUAVE, 1.0)
	for km in range(2, 21, 2):
		var y := lerpf(y1, y0, km / 20.0)
		c.draw_line(Vector2(x - 3, y), Vector2(x + (4 if km % 10 == 0 else 2), y), SUAVE, 1.0)
		_txt(Vector2(x - 36, y + 3), "%d km" % km, SUAVE, 6)
	var yp := lerpf(y1, y0, alt_paracaidas / 20.0)
	var yc := lerpf(y1, y0, alt_cohetes / 20.0)
	c.draw_rect(Rect2(x + 1, lerpf(y1, y0, 13.0 / 20.0), 3, lerpf(y1, y0, 7.0 / 20.0) - lerpf(y1, y0, 13.0 / 20.0)), Color(CIAN, 0.15))
	c.draw_arc(Vector2(x + 18, yp - 4), 7, PI, TAU, 8, CIAN, 2.0)
	c.draw_line(Vector2(x + 4, yp), Vector2(x + 30, yp), CIAN, 1.0)
	c.draw_rect(Rect2(x + 14, yc - 3, 8, 6), AMBAR)
	c.draw_line(Vector2(x + 4, yc), Vector2(x + 30, yc), AMBAR, 1.0)
	c.draw_rect(Rect2(46, y1, 84, 6), Color("b5633a"))
	# filas del programa
	var filas := [
		["Abrir el paracaídas a", "%d km" % int(alt_paracaidas), CIAN,
			"El paracaídas frena mucho, pero si va demasiado rápido se rasga."],
		["Encender los cohetes a", "%s km" % numero(alt_cohetes, 1), AMBAR,
			"Los cohetes frenan los últimos metros. Tienen poco combustible."],
		["Navegación por terreno", "Sí" if navegacion else "No", VERDE if navegacion else NARANJA,
			"Una cámara compara el suelo con un mapa y busca un lugar plano."],
	]
	for i in 3:
		var f: Array = filas[i]
		var r := Rect2(150, 80 + i * 56, 420, 48)
		var sel := i == fila
		_caja(r, f[2] if sel else BORDE, Color(0.043, 0.055, 0.102, 0.92 if sel else 0.8))
		_rects["fila" + str(i)] = r
		_txt(r.position + Vector2(10, 16), "%d. %s" % [i + 1, f[0]], BLANCO, 8)
		var caja_v := Rect2(r.end.x - 120, r.position.y + 6, 110, 16)
		c.draw_rect(caja_v, Color("232a40"))
		_txt(caja_v.position + Vector2(0, 12), f[1], f[2], 9, caja_v.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		_flecha(caja_v.position + Vector2(8, 8), -1, f[2] if sel else SUAVE)
		_flecha(caja_v.position + Vector2(caja_v.size.x - 8, 8), 1, f[2] if sel else SUAVE)
		_rects["menos" + str(i)] = Rect2(caja_v.position, Vector2(22, 16))
		_rects["mas" + str(i)] = Rect2(caja_v.end.x - 22, caja_v.position.y, 22, 16)
		_txt(r.position + Vector2(10, 38), f[3], SUAVE if not sel else BLANCO, 7)
	var b := Rect2(250, 252, 220, 22)
	var pulso := 0.75 + 0.25 * sin(_anim * 4.0)
	_caja(b, AMBAR, Color(0.3, 0.2, 0.05, 0.9 * pulso))
	_txt(b.position + Vector2(0, 15), "Probar en el simulador  (Enter)", AMBAR, 8, b.size.x, HORIZONTAL_ALIGNMENT_CENTER)
	_rects["probar"] = b
	var ayuda := "↑ ↓: elegir   ← →: cambiar" + ("" if intentos == 0 else "   ·   Intentos: %d" % intentos)
	_txt(Vector2(150, 290), ayuda, SUAVE, 6)


func _flecha(p: Vector2, d: int, col: Color) -> void:
	_lienzo.draw_colored_polygon(PackedVector2Array([p + Vector2(d * 4, 0), p + Vector2(-d * 3, -4), p + Vector2(-d * 3, 4)]), col)


func _escena(tr: float, p: Array) -> void:
	var c := _lienzo
	var h: float = p[0]
	var v: float = p[1]
	_cielo(h)
	# las montanas suben a medida que la nave baja
	var desp := [0.0, 0.0, 0.0]
	for i in 3:
		var tope := [8.0, 4.0, 2.0][i] as float
		var dy := clampf(h / tope, 0.0, 1.0) * 320.0
		if dy < 319.0:
			var tex: Texture2D = _montes[i]
			var xo := -fposmod(tr * (6.0 + i * 8.0), 640.0)
			for n in 2:
				c.draw_texture(tex, Vector2(xo + n * 640.0, dy))
			desp[i] = dy
	var dy_suelo := clampf(h / 0.5, 0.0, 1.0) * 120.0
	if dy_suelo < 119.0:
		for n in 2:
			c.draw_texture(_suelo, Vector2(n * 640.0 - fposmod(tr * 30.0, 640.0), 304.0 + dy_suelo))
	# rocas sueltas si no hay navegacion por terreno
	var rocas := causa == "rocas"
	if rocas and dy_suelo < 119.0:
		for k in 4:
			var rx := 270.0 + k * 30.0
			var ry := 304.0 + dy_suelo
			c.draw_colored_polygon(PackedVector2Array([Vector2(rx - 9, ry + 2), Vector2(rx - 5, ry - 7 - k % 2 * 3), Vector2(rx + 6, ry - 6), Vector2(rx + 10, ry + 2)]), Color("6e2e2e"))
			c.draw_line(Vector2(rx - 5, ry - 7 - k % 2 * 3), Vector2(rx + 6, ry - 6), Color("d47a45"), 1.0)
	# estelas de velocidad
	var rapidez := clampf(v / 2500.0, 0.0, 1.0)
	for i in 30:
		var sx := float((i * 97) % 640)
		var sy := fposmod(float((i * 53) % 360) - tr * (80.0 + 600.0 * rapidez), 360.0)
		c.draw_line(Vector2(sx, sy), Vector2(sx, sy + 4.0 + 16.0 * rapidez), Color(1, 0.95, 0.85, 0.25 + 0.3 * rapidez), 1.0)
	# la nave
	var w := 28.0
	var alto := 80.0
	var base_y := 200.0
	var suelo_y := 304.0 + dy_suelo
	var px := 320.0
	if navegacion and h < 1.6 and causa != "cohetes_tarde":
		px = 320.0 + clampf((1.6 - h) / 1.4, 0.0, 1.0) * 70.0          # se desvia hacia un lugar plano
	var pie_y := lerpf(304.0, base_y, clampf(h / 0.5, 0.0, 1.0))
	var tiembla := Vector2(sin(tr * 47.0), cos(tr * 39.0)) * 1.5 * rapidez
	var ang := 0.0
	if rocas and h <= 0.0:
		ang = 0.22
	var nave := Rect2(px - w * 0.5, pie_y - alto, w, alto)
	var en_entrada := tr < T_ENTRADA
	var tp := tr - T_ENTRADA
	var tc := tr - T_ENTRADA - T_PARACAIDAS
	# plasma de la entrada: la nave baja de cola con el escudo termico adelante
	if en_entrada:
		var fuerza := sin(clampf(tr / T_ENTRADA, 0.0, 1.0) * PI) * 0.9 + 0.1
		for i in 22:
			var lado := -1.0 if i % 2 == 0 else 1.0
			var lx := px + lado * (8.0 + (i * 7 % 13))
			var largo := (20.0 + (i * 13 % 40)) * fuerza + sin(_anim * 30.0 + i) * 5.0
			c.draw_line(Vector2(lx, pie_y + 2), Vector2(lx + lado * 4.0, pie_y - largo), (Color("ffe08a") if i % 3 == 0 else NARANJA) * Color(1, 1, 1, 0.8 * fuerza), 2.0)
		c.draw_circle(Vector2(px, pie_y + 4), 18.0 * fuerza + 6.0, Color(1, 0.6, 0.3, 0.35 * fuerza))
	# escudo termico: plato bajo la nave hasta poco despues de abrir el paracaidas
	var escudo_y := pie_y + 4.0
	if tp > 0.8:
		escudo_y += (tp - 0.8) * (tp - 0.8) * 160.0
	if escudo_y < 380.0 and causa != "rasgado":
		c.draw_colored_polygon(PackedVector2Array([Vector2(px - 20, escudo_y - 2), Vector2(px + 20, escudo_y - 2), Vector2(px + 12, escudo_y + 5), Vector2(px - 12, escudo_y + 5)]), Color("7d5210"))
		c.draw_line(Vector2(px - 20, escudo_y - 2), Vector2(px + 20, escudo_y - 2), Color("d39528"), 2.0)
	elif causa == "rasgado" or tp <= 0.8:
		c.draw_colored_polygon(PackedVector2Array([Vector2(px - 20, pie_y + 2), Vector2(px + 20, pie_y + 2), Vector2(px + 12, pie_y + 9), Vector2(px - 12, pie_y + 9)]), Color("7d5210"))
	# paracaidas
	if tp >= 0.0 and tc < 0.3:
		var abre := clampf(tp / 0.5, 0.0, 1.0)
		var cima := Vector2(px, nave.position.y - 70.0)
		if tc >= 0.0:
			cima += Vector2(tc * 60.0, -tc * 400.0)          # se suelta y se va hacia arriba
		var ancho := 52.0 * abre
		if causa == "rasgado":
			var vuela := maxf(0.0, tp - 0.6)
			for k in 4:
				var trozo := cima + Vector2((k - 1.5) * 18.0 + (k - 1.5) * vuela * 50.0, -vuela * 90.0 - k * 6.0 * vuela)
				c.draw_arc(trozo, 9.0, PI, TAU, 6, Color("f6f1e4") if k % 2 == 0 else ROSA, 3.0)
			if vuela < 0.2:
				c.draw_arc(cima, ancho, PI, TAU, 20, ROSA, 6.0)
		else:
			c.draw_arc(cima, ancho, PI, TAU, 24, Color("f6f1e4"), 7.0)
			for k in 6:
				var a := PI + PI * k / 5.0
				c.draw_arc(cima, ancho, a, a + PI / 10.0, 4, ROSA, 7.0)
			for k in 5:
				var bx := cima.x - ancho + k * ancho * 0.5
				c.draw_line(Vector2(bx, cima.y), Vector2(px - 4 + k * 2, nave.position.y), Color(0.9, 0.9, 0.85, 0.7), 1.0)
	# cohetes encendidos
	var llama := tc >= 0.0 and h > 0.0
	if causa == "cohetes_pronto" and h < 0.05:
		llama = false
	if causa == "poco_freno" or causa == "rasgado":
		llama = false
	if llama:
		for i in 10:
			var largo := randf_range(8.0, 22.0)
			c.draw_rect(Rect2(px - 9 + i * 2, pie_y, 2, largo), Color("ffe08a") if i % 3 == 0 else NARANJA)
	# cuerpo de la nave (el cohete que despego de la Luna)
	if ang == 0.0:
		c.draw_texture_rect(_cohete, Rect2(nave.position + tiembla, nave.size), false)
	else:
		c.draw_set_transform(Vector2(px, pie_y), ang, Vector2.ONE)
		c.draw_texture_rect(_cohete, Rect2(Vector2(-w * 0.5, -alto), nave.size), false)
		c.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	# polvo al tocar el suelo
	if h <= 0.0 and resultado != "perdida":
		var tt := tr - (T_ENTRADA + T_PARACAIDAS + T_COHETES)
		for i in 16:
			var a := PI + PI * i / 15.0
			var r := 6.0 + tt * 60.0
			c.draw_rect(Rect2(Vector2(px, suelo_y - 2) + Vector2(cos(a) * r * 1.4, sin(a) * r * 0.35), Vector2(3, 2)), Color("d47a45", clampf(1.0 - tt, 0.0, 1.0)))
	# la simulacion se corta: senal perdida
	if resultado == "perdida" and t >= _t_fin() - 0.25:
		c.draw_rect(Rect2(0, 0, 640, 360), Color(0.06, 0.06, 0.08, 0.92))
		for i in 2200:
			var q := Vector2(randf() * 640.0, randf() * 360.0)
			c.draw_rect(Rect2(q, Vector2(2, 1)), Color(1, 1, 1, randf() * 0.5))
		_txt(Vector2(0, 230), "SEÑAL PERDIDA", ROSA, 16, 640, HORIZONTAL_ALIGNMENT_CENTER)


func _telemetria(p: Array) -> void:
	var c := _lienzo
	var r := Rect2(470, 70, 160, 92)
	_caja(r, CIAN)
	_txt(r.position + Vector2(8, 13), "Simulador de descenso", CIAN, 8)
	_txt(r.position + Vector2(8, 29), "Altitud", SUAVE, 7)
	_txt(r.position + Vector2(70, 29), (numero(p[0], 1) + " km") if p[0] >= 1.0 else ("%d m" % int(p[0] * 1000.0)), BLANCO, 8)
	_txt(r.position + Vector2(8, 42), "Velocidad", SUAVE, 7)
	_txt(r.position + Vector2(70, 42), numero(p[1]) + " km/h", BLANCO, 8)
	var s := int(p[2])
	_txt(r.position + Vector2(8, 55), "Tiempo", SUAVE, 7)
	_txt(r.position + Vector2(70, 55), "%d:%02d de 7:00" % [s / 60, s % 60], BLANCO, 8)
	_txt(r.position + Vector2(8, 68), "Fase", SUAVE, 7)
	_txt(r.position + Vector2(70, 68), p[3], AMBAR, 8)
	# lo que sabe la Tierra en ese momento: nada todavia
	var rt := Rect2(10, 70, 170, 50)
	_caja(rt, BORDE)
	_txt(rt.position + Vector2(8, 13), "Centro de control (Tierra)", SUAVE, 7)
	var espera := int(ceil(11.0 - float(s) / 60.0))
	_txt(rt.position + Vector2(8, 28), "Esperando señal…", BLANCO, 8)
	_txt(rt.position + Vector2(8, 41), "llegará en unos %d min" % maxi(espera, 4), SUAVE, 7)
	if fmod(_anim, 1.0) < 0.5:
		c.draw_circle(rt.position + Vector2(160, 10), 2.5, NARANJA)


func _resultado() -> void:
	var lineas := explicacion()
	var titulo := {"suave": "Aterrizaje suave", "duro": "Aterrizaje duro", "perdida": "La nave se perdería"}[resultado] as String
	var col := {"suave": VERDE, "duro": AMBAR, "perdida": ROSA}[resultado] as Color
	var r := Rect2(70, 30, 500, 114)
	_caja(r, col, Color(0.043, 0.055, 0.102, 0.95))
	_txt(r.position + Vector2(0, 20), titulo, col, 16, r.size.x, HORIZONTAL_ALIGNMENT_CENTER)
	for i in lineas.size():
		_txt(r.position + Vector2(0, 38 + i * 12), lineas[i], BLANCO, 7, r.size.x, HORIZONTAL_ALIGNMENT_CENTER)
	if resultado == "perdida":
		var b := Rect2(r.position.x + 120, r.end.y - 24, 180, 16)
		_caja(b, AMBAR)
		_txt(b.position + Vector2(0, 11), "Ajustar el programa  (Enter)", AMBAR, 7, b.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		_rects["ajustar"] = b
	else:
		var b1 := Rect2(r.position.x + 30, r.end.y - 24, 170, 16)
		var b2 := Rect2(r.position.x + 220, r.end.y - 24, 170, 16)
		_caja(b1, col)
		_txt(b1.position + Vector2(0, 11), "Enviar y aterrizar  (Enter)", col, 7, b1.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		_caja(b2, SUAVE)
		_txt(b2.position + Vector2(0, 11), "Ajustar el programa  (E)", SUAVE, 7, b2.size.x, HORIZONTAL_ALIGNMENT_CENTER)
		_rects["aceptar"] = b1
		_rects["ajustar"] = b2


func _llegada() -> void:
	var c := _lienzo
	var k := clampf(_t_llegada / 4.0, 0.0, 1.0)
	c.draw_rect(Rect2(0, 0, 640, 360), Color(0.02, 0.02, 0.04, 1.0))
	var a := clampf(_t_llegada * 1.5, 0.0, 1.0) * clampf((4.0 - _t_llegada) * 1.5, 0.0, 1.0)
	_txt(Vector2(0, 160), "El programa viaja a la nave… y la nave baja sola.", Color(BLANCO, a), 9, 640, HORIZONTAL_ALIGNMENT_CENTER)
	_txt(Vector2(0, 180), "Once minutos después, la Tierra recibe la señal:", Color(SUAVE, a), 8, 640, HORIZONTAL_ALIGNMENT_CENTER)
	_txt(Vector2(0, 202), "¡Estamos en Marte!", Color(AMBAR, a * clampf((k - 0.35) * 4.0, 0.0, 1.0)), 16, 640, HORIZONTAL_ALIGNMENT_CENTER)
