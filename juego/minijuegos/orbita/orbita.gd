extends "res://nucleo/minijuego.gd"

# Gravedad newtoniana en km y s; Verlet con paso fijo. R y mu son constantes del modelo.
# Solo la altura de Pegaso procede de la ficha verificada. Motor, anillos, combustible,
# corte atmosferico y escala de tiempo son reglas didacticas, no datos de Pegaso.
const MU: float = 398600.0
const RADIO: float = 6371.0
const DT: float = 1.0 / 120.0
const RITMO_FISICO: float = 210.0
const MOTOR: float = 0.09
const CORTE_ATMOSFERA: float = 120.0
const CENTRO: Vector2 = Vector2(160, 96)
const LETRAS: Dictionary = {
	"A": ["###", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
	"C": ["###", "#..", "#..", "#..", "###"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
	"E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
	"G": ["###", "#..", "#.#", "#.#", "###"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
	"I": ["###", ".#.", ".#.", ".#.", "###"], "J": ["..#", "..#", "..#", "#.#", "###"],
	"K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
	"M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"], "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
	"O": ["###", "#.#", "#.#", "#.#", "###"], "P": ["###", "#.#", "###", "#..", "#.."],
	"Q": ["###", "#.#", "#.#", "###", "..#"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
	"S": ["###", "#..", "###", "..#", "###"], "T": ["###", ".#.", ".#.", ".#.", ".#."],
	"U": ["#.#", "#.#", "#.#", "#.#", "###"], "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
	"W": ["#...#", "#...#", "#.#.#", "##.##", "#...#"], "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
	"Y": ["#.#", "#.#", ".#.", ".#.", ".#."], "Z": ["###", "..#", ".#.", "#..", "###"],
	"0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
	"2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", "###", "..#", "###"],
	"4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
	"6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", "..#", "..#", "..#"],
	"8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
	" ": ["..", "..", "..", "..", ".."], "/": ["..#", "..#", ".#.", "#..", "#.."],
	":": [".", "#", ".", "#", "."], ".": [".", ".", ".", ".", "#"], "!": ["#", "#", "#", ".", "#"],
	"-": ["...", "...", "###", "...", "..."], "+": ["...", ".#.", "###", ".#.", "..."],
	"x": ["...", "#.#", ".#.", "#.#", "..."], "<": ["..#", ".#.", "#..", ".#.", "..#"],
	">": ["#..", ".#.", "..#", ".#.", "#.."], "?": ["###", "..#", ".#.", "...", ".#."],
}
const SAT: Array[String] = ["....c....", "pp..c..pp", "ppCCCCCpp", "ppCCkCCpp", "ppCCCCCpp", "pp..c..pp", "....c...."]
const ANILLO: Array[String] = ["..###..", ".#...#.", "#.....#", "#.....#", "#.....#", ".#...#.", "..###.."]
const OFFSETS: Array[float] = [160.0, -160.0, 160.0, -160.0, 80.0, 0.0, 0.0, 0.0]

var posicion: Vector2 = Vector2.ZERO
var vector_velocidad: Vector2 = Vector2.ZERO
var altura: float = 640.5
var pegaso_baja: float = 0.0
var pegaso_alta: float = 0.0
var minima: float = 0.0
var maxima: float = 0.0
var margen: float = 140.0
var margen_anillo: float = 170.0
var combustible: float = 28.0
var tanque: float = 28.0
var limite: float = 105.0
var reloj: float = 0.0
var angulo: float = 0.0
var proximo: float = 2.5
var anillos: int = 0
var exigidos: int = 6
var intentados: int = 0
var vidas: int = 3
var puntos: float = 0.0
var estable: float = 0.0
var mando: float = 0.0
var guia: float = 0.0
var fase: int = 0
var _fase_t: float = 0.0
var _acum: float = 0.0
var _auto: int = 0
var _destello: float = 0.0
var _sacudida: float = 0.0
var _inmune: float = 0.0
var _sonido: float = 0.0
var _trazo_t: float = 0.0
var _gana: bool = false
var _causa: String = ""
var _cartel: String = ""
var _cartel_t: float = 0.0
var _trazo: PackedVector2Array = PackedVector2Array()
var _particulas: Array[Dictionary] = []
var _estrellas: Array[Vector2] = []
var _fx: RandomNumberGenerator = RandomNumberGenerator.new()
var _letras: Dictionary = {}
var _pal: Dictionary = {}


func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	# Extraer las cifras de la ficha; no duplicar las alturas en el codigo.
	var ficha: Dictionary = Juego.ficha("pegaso_orbita")
	var texto_ficha: String = str(ficha.get("texto", ""))
	var patron: RegEx = RegEx.new()
	patron.compile("([0-9]+) . ([0-9]+) km")
	var hallazgo: RegExMatch = patron.search(texto_ficha)
	if hallazgo != null:
		pegaso_baja = float(hallazgo.get_string(1))
		pegaso_alta = float(hallazgo.get_string(2))
	altura = (pegaso_baja + pegaso_alta) * 0.5
	margen = [140.0, 90.0, 55.0][dificultad - 1]
	margen_anillo = [170.0, 120.0, 85.0][dificultad - 1]
	tanque = [28.0, 25.0, 23.0][dificultad - 1]
	combustible = tanque
	limite = [105.0, 110.0, 115.0][dificultad - 1]
	exigidos = 5 + dificultad
	posicion = Vector2(RADIO + altura, 0)
	vector_velocidad = Vector2(0.045 * dificultad, -sqrt(MU / posicion.length()) + 0.10 + 0.03 * dificultad)
	_fx.seed = 4813
	for i in 100:
		_estrellas.append(Vector2(_fx.randi_range(0, 319), _fx.randi_range(20, 160)))
	_pal = {"p": Estilo.PETROLEO.lightened(0.3), "C": Estilo.CREMA, "c": Estilo.DORADO, "k": Estilo.CIAN, "#": Estilo.CIAN}
	_letras = LETRAS
	_lecturas()
	queue_redraw()


func _empezar() -> void:
	fase = 0
	_fase_t = 0.0
	sonar("radio")


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


func objetivo_altura() -> float:
	if anillos >= exigidos:
		return altura
	return altura + OFFSETS[mini(anillos, OFFSETS.size() - 1)]


func orden_motor() -> float:
	var r: float = posicion.length()
	var radial: Vector2 = posicion / r
	var tangente: Vector2 = Vector2(radial.y, -radial.x)
	var vr: float = vector_velocidad.dot(radial)
	var vt: float = vector_velocidad.dot(tangente)
	return sqrt(MU / r) - 0.0008 * (r - RADIO - objetivo_altura()) - 0.8 * vr - vt


func _paso(delta: float) -> void:
	# El piloto comprime el tiempo, pero recorre exactamente los mismos pasos y reglas.
	_acum += delta * (3.5 if _auto != 0 else 1.0)
	while _acum >= DT and activo:
		_acum -= DT
		_tic(DT)
	queue_redraw()


func _tic(dt: float) -> void:
	_fase_t += dt
	_efectos(dt)
	if fase == 0:
		if _fase_t >= 2.4:
			fase = 1
			_fase_t = 0.0
		return
	if fase == 2:
		if _fase_t >= 1.6:
			terminar(_gana, roundf(puntos), _causa)
		return
	reloj += dt
	guia = orden_motor()
	if _auto != 0:
		mando = signf(guia) if absf(guia) > 0.007 else 0.0
		if _auto < 0:
			mando = -1.0
	else:
		mando = 0.0
		if Input.is_action_pressed("mover_arriba") or Input.is_action_pressed("interactuar") or Input.is_action_pressed("saltar"):
			mando = 1.0
		if Input.is_action_pressed("mover_abajo"):
			mando = -1.0
		if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
			mando = 1.0
		if Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
			mando = -1.0
	if combustible <= 0.0:
		mando = 0.0
	var gasto: float = minf(combustible, absf(mando) * dt)
	vector_velocidad += vector_velocidad.normalized() * signf(mando) * MOTOR * gasto
	combustible -= gasto
	var paso_fisico: float = dt * RITMO_FISICO
	var previa: Vector2 = posicion
	var a: Vector2 = _gravedad(posicion)
	posicion += vector_velocidad * paso_fisico + a * (0.5 * paso_fisico * paso_fisico)
	vector_velocidad += (a + _gravedad(posicion)) * (0.5 * paso_fisico)
	angulo += absf(previa.angle_to(posicion))
	_lecturas()
	_trazo_t += dt
	if _trazo_t >= 1.0 / 12.0:
		_trazo_t -= 1.0 / 12.0
		_trazo.append(posicion)
		if _trazo.size() > 180:
			_trazo.remove_at(0)
	if mando != 0.0:
		_sonido -= dt
		if _sonido <= 0.0:
			_sonido = 0.18
			sonar("tic")
	if posicion.length() - RADIO <= CORTE_ATMOSFERA:
		_acabar(false, "La órbita rozó la atmósfera: al frenar demasiado, baja el lado opuesto de la trayectoria.")
		return
	if maxima > 6000.0 or vector_velocidad.length_squared() * 0.5 - MU / posicion.length() >= 0.0:
		_acabar(false, "El exceso de impulso abrió la trayectoria: el satélite se escapa del campo de control.")
		return
	if anillos < exigidos and angulo >= proximo:
		intentados += 1
		if absf(posicion.length() - RADIO - objetivo_altura()) <= margen_anillo:
			anillos += 1
			puntos += 150.0
			_cartel = "+150  ENLACE"
			_cartel_t = 1.3
			_destello = 0.16
			sonar("recoger")
			_estallar(_pantalla(posicion), Estilo.CIAN)
		else:
			vidas -= 1
			_sacudida = 0.35
			_destello = 0.28
			_inmune = 1.2
			_cartel = "ANILLO PERDIDO"
			_cartel_t = 1.5
			sonar("error")
			_estallar(_pantalla(posicion), Estilo.CORAL)
			if vidas <= 0:
				_acabar(false, "Se perdieron tres enlaces: los impulsos deben anticipar la altura del siguiente anillo.")
				return
		proximo += 2.4
	if anillos >= exigidos:
		var circular: bool = absf((maxima + minima) * 0.5 - altura) <= margen * 0.5 and maxima - minima <= margen
		estable = estable + dt if circular and mando == 0.0 else 0.0
		if estable >= 4.0 and reloj >= 60.0:
			puntos += combustible * 50.0 + vidas * 100.0
			_acabar(true, "Impulsar eleva el lado opuesto; frenar lo baja: Pegaso fue registrado a %.0f × %.0f km." % [pegaso_baja, pegaso_alta])
	elif combustible <= 0.0 and (minima < CORTE_ATMOSFERA or maxima > 6000.0):
		_acabar(false, "Se agotó el combustible con una trayectoria peligrosa: ya no queda impulso para corregirla.")
	if reloj >= limite and fase == 1:
		_acabar(false, "Terminó la ventana de control antes de reunir los enlaces y dejar una órbita circular sin motor.")


func _gravedad(p: Vector2) -> Vector2:
	return -MU * p / pow(p.length(), 3.0)


func _lecturas() -> void:
	var r: float = posicion.length()
	var energia: float = vector_velocidad.length_squared() * 0.5 - MU / r
	var h: float = absf(posicion.cross(vector_velocidad))
	if energia >= 0.0:
		minima = r - RADIO
		maxima = 99999.0
		return
	var eje: float = -MU / (2.0 * energia)
	var exc: float = sqrt(maxf(0.0, 1.0 + 2.0 * energia * h * h / (MU * MU)))
	minima = eje * (1.0 - exc) - RADIO
	maxima = eje * (1.0 + exc) - RADIO


func _acabar(gana: bool, causa: String) -> void:
	if fase == 2:
		return
	fase = 2
	_fase_t = 0.0
	_gana = gana
	_causa = causa
	_cartel = "ORBITA SELLADA" if gana else "ENLACE PERDIDO"
	_cartel_t = 2.0
	_destello = 0.3
	_sacudida = 0.2
	sonar("logro" if gana else "error")
	_estallar(_pantalla(posicion), Estilo.DORADO if gana else Estilo.CORAL)
	print("ORBITA d%d anillos=%d/%d vidas=%d fuel=%.2f min=%.1f max=%.1f vuelo=%.2f" % [dificultad, anillos, exigidos, vidas, combustible, minima, maxima, reloj])


func _estallar(p: Vector2, color: Color) -> void:
	for i in 22:
		var v: Vector2 = Vector2.from_angle(_fx.randf_range(0.0, TAU)) * _fx.randf_range(8.0, 36.0)
		_particulas.append({"p": p, "v": v, "t": 0.7, "c": color})


func _efectos(dt: float) -> void:
	_destello = maxf(0.0, _destello - dt)
	_sacudida = maxf(0.0, _sacudida - dt)
	_inmune = maxf(0.0, _inmune - dt)
	_cartel_t = maxf(0.0, _cartel_t - dt)
	for i in range(_particulas.size() - 1, -1, -1):
		var p: Dictionary = _particulas[i]
		var lugar: Vector2 = p["p"]
		var v: Vector2 = p["v"]
		p["p"] = lugar + v * dt
		p["t"] = float(p["t"]) - dt
		if float(p["t"]) <= 0.0:
			_particulas.remove_at(i)


func _pantalla(p: Vector2) -> Vector2:
	# Alturas ampliadas para ver la maniobra; la fisica no usa esta proyeccion.
	var radio_visual: float = clampf(35.0 + (p.length() - RADIO) * 0.04, 34.0, 74.0)
	return (CENTRO + p.normalized() * radio_visual).round()


func _r(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2(roundf(x), roundf(y), roundf(w), roundf(h)), color)


func _punto(p: Vector2, color: Color, e: int = 1) -> void:
	_r(p.x, p.y, e, e, color)


func _sprite(mapa: Array, p: Vector2, e: int = 1) -> void:
	for y in mapa.size():
		var fila: String = mapa[y]
		for x in fila.length():
			var c: String = fila[x]
			if c != ".":
				var color: Color = _pal.get(c, Estilo.CREMA)
				_r(p.x + x * e, p.y + y * e, e, e, color)


func _texto(s: String, x: float, y: float, color: Color, e: int = 1) -> void:
	var cx: float = x
	for c in s:
		var filas: Array = _letras.get(c, _letras.get("?", []))
		var ancho: int = 3
		if not filas.is_empty():
			var primera: String = filas[0]
			ancho = primera.length()
		for j in filas.size():
			var fila: String = filas[j]
			for i in fila.length():
				if fila[i] == "#":
					_r(cx + i * e, y + j * e, e, e, color)
		cx += (ancho + 1) * e


func _circulo(p: Vector2, radio: float, color: Color, discontinuo: bool = false) -> void:
	for i in 360:
		if discontinuo and i % 12 > 5:
			continue
		_punto(p + Vector2.from_angle(float(i) * TAU / 360.0) * radio, color)


func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(4, 4))
	_r(0, 0, 320, 180, Estilo.NOCHE)
	var desvio: Vector2 = Vector2(roundf(sin(_fase_t * 81.0)), roundf(cos(_fase_t * 69.0))) if _sacudida > 0.0 else Vector2.ZERO
	draw_set_transform(desvio * 4.0, 0.0, Vector2(4, 4))
	for i in _estrellas.size():
		_punto(_estrellas[i], Color(Estilo.CREMA if i % 4 == 0 else Estilo.PETROLEO, 0.5))
	_circulo(CENTRO, 35.0 + CORTE_ATMOSFERA * 0.04, Estilo.CORAL, true)
	_circulo(CENTRO, 35.0 + altura * 0.04, Color(Estilo.CIAN, 0.35), true)
	_tierra()
	for i in _trazo.size():
		if i % 2 == 0:
			_punto(_pantalla(_trazo[i]), Color(Estilo.CIAN, 0.15 + 0.6 * float(i) / maxf(1.0, _trazo.size())))
	# Prediccion con los elementos osculadores: cambia inmediatamente al pulsar motor.
	var h: float = absf(posicion.cross(vector_velocidad))
	var ex: Vector2 = ((vector_velocidad.length_squared() - MU / posicion.length()) * posicion - posicion.dot(vector_velocidad) * vector_velocidad) / MU
	for i in 120:
		if i % 3 == 0:
			var u: Vector2 = Vector2.from_angle(TAU * i / 120.0)
			var rr: float = h * h / MU / maxf(0.01, 1.0 + ex.dot(u))
			_punto(_pantalla(u * rr), Color(Estilo.CREMA, 0.4))
	if anillos < exigidos:
		_dibujar_anillo()
	var sat: Vector2 = _pantalla(posicion)
	if _inmune <= 0.0 or fmod(_inmune, 0.24) > 0.12:
		_sprite(SAT, sat - Vector2(4, 3))
	var v: Vector2 = vector_velocidad.normalized()
	for i in range(7, 15):
		_punto(sat + v * i, Estilo.CIAN)
	if mando != 0.0 and fase == 1:
		for i in range(5, 10 + int(_fase_t * 20.0) % 4):
			_punto(sat - v * i * mando, Estilo.NARANJA if i % 2 == 0 else Estilo.DORADO, 2)
	for par in _particulas:
		var p: Vector2 = par["p"]
		var c: Color = par["c"]
		_punto(p, c, 2 if float(par["t"]) > 0.4 else 1)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(4, 4))
	_hud()
	if _cartel_t > 0.0:
		_texto(_cartel, 102, 24, Estilo.DORADO if _gana or vidas == 3 else Estilo.CORAL)
	if fase == 0:
		_r(56, 54, 208, 83, Color(Estilo.NOCHE, 0.96))
		_sprite(ANILLO, Vector2(112, 69), 3)
		_sprite(SAT, Vector2(157, 75), 2)
		_texto(">", 141, 76, Estilo.CIAN, 2)
		_texto("CRUZA ANILLOS. SELLA LA ORBITA.", 72, 108, Estilo.CREMA)
		_r(72, 124, 176 * maxf(0.0, 1.0 - _fase_t / 2.4), 2, Estilo.DORADO)
	if _destello > 0.0:
		_r(0, 19, 320, 141, Color(Estilo.DORADO if _gana else Estilo.CORAL, _destello * 0.55))


func _tierra() -> void:
	for y in range(-34, 35):
		var w: int = int(sqrt(maxf(0.0, 34.5 * 34.5 - y * y)))
		_r(CENTRO.x - w, CENTRO.y + y, w * 2, 1, Estilo.PETROLEO)
		for x in range(-w, w):
			var costa: float = sin((x + 0.35 * y) * 0.16) + cos(y * 0.19) + sin((x - y) * 0.22)
			if costa > 0.9 and x > -26 and x < 20:
				_r(CENTRO.x + x, CENTRO.y + y, 1, 1, Estilo.CREMA if x < -8 else Estilo.TINTA_SUAVE)
			if x > 14 + y * 0.15:
				_r(CENTRO.x + x, CENTRO.y + y, 1, 1, Color(Estilo.NOCHE, 0.5))
	_circulo(CENTRO, 35.0, Estilo.PETROLEO.lightened(0.25))
	_texto("TIERRA", 148, 94, Estilo.PAPEL)
	# Faro ecuatorial: una estacion envia los enlaces al satelite.
	_r(143, 107, 3, 3, Estilo.DORADO)
	if fmod(reloj, 2.0) < 1.0:
		_circulo(Vector2(144, 108), 5 + fmod(reloj, 1.0) * 7, Color(Estilo.DORADO, 0.6), true)


func _dibujar_anillo() -> void:
	var a: float = -proximo
	var u: Vector2 = Vector2.from_angle(a)
	var t: Vector2 = u.orthogonal()
	var r: float = 35.0 + objetivo_altura() * 0.04
	var p: Vector2 = CENTRO + u * r
	var medio: float = maxf(3.0, margen_anillo * 0.04)
	for lado in [-1.0, 1.0]:
		for k in range(-4, 5):
			_punto(p + u * medio * lado + t * k, Estilo.CIAN, 1)
		for k in 3:
			_punto(p + u * (medio - k) * lado + t * 4, Estilo.CIAN)
			_punto(p + u * (medio - k) * lado - t * 4, Estilo.CIAN)
	_texto(str(anillos + 1), p.x - 1 + u.x * 12, p.y - 2 + u.y * 12, Estilo.CREMA)


func _hud() -> void:
	_r(0, 0, 320, 19, Estilo.TINTA)
	_texto("%04d" % int(puntos), 4, 5, Estilo.CREMA, 2)
	_texto("FUEL", 43, 6, Estilo.PAPEL)
	_r(63, 5, 87, 9, Estilo.PETROLEO)
	_r(64, 6, floorf(85.0 * combustible / tanque), 7, Estilo.NARANJA if combustible > tanque * 0.25 else Estilo.CORAL)
	for i in 3:
		_r(162 + i * 9, 6, 6, 7, Estilo.CREMA if i < vidas else Estilo.TINTA_SUAVE)
		_r(164 + i * 9, 4, 2, 11, Estilo.CREMA if i < vidas else Estilo.TINTA_SUAVE)
	_texto("%02d/%02d" % [anillos, exigidos], 201, 5, Estilo.CIAN, 2)
	_texto("%03d" % int(ceil(maxf(0.0, limite - reloj))), 290, 5, Estilo.CREMA, 2)
	_texto("ALT", 6, 41, Estilo.PAPEL)
	_texto("%04d" % maxi(0, int(posicion.length() - RADIO)), 6, 50, Estilo.CREMA, 2)
	_texto("KM", 6, 63, Estilo.PAPEL)
	_texto("ANILLO", 6, 84, Estilo.CIAN)
	_texto("%04d" % int(objetivo_altura()), 6, 94, Estilo.CIAN, 2)
	_texto("ALTURAS", 255, 41, Estilo.PAPEL)
	_texto("PREVISTAS", 255, 49, Estilo.PAPEL)
	_texto("MAX", 255, 64, Estilo.CREMA)
	_texto("%04d" % clampi(int(maxima), 0, 9999), 255, 73, Estilo.CREMA, 2)
	_texto("MIN", 255, 90, Estilo.CREMA)
	_texto("%04d" % maxi(0, int(minima)), 255, 99, Estilo.CREMA, 2)
	_texto("SELLADO", 255, 124, Estilo.DORADO)
	for i in 8:
		_r(255 + i * 7, 135, 5, 6, Estilo.DORADO if estable >= float(i + 1) * 0.5 else Estilo.PETROLEO)
	# Aguja de compensacion: en el centro se puede soltar el motor.
	_texto("-", 109, 147, Estilo.CORAL)
	_texto("+", 204, 147, Estilo.CIAN)
	_r(119, 149, 78, 1, Estilo.PETROLEO)
	_r(153, 146, 10, 7, Estilo.TINTA_SUAVE)
	_r(158 + clampf(guia * 150.0, -37.0, 37.0), 146, 2, 7, Estilo.CREMA)
	_r(0, 161, 320, 19, Estilo.TINTA)
	_texto("E/W: MOTOR", 4, 166, Estilo.CIAN if mando > 0 else Estilo.PAPEL)
	_texto("S: FRENO", 62, 166, Estilo.NARANJA if mando < 0 else Estilo.PAPEL)
	_texto("SUELTA: INERCIA", 105, 166, Estilo.CREMA)
	_texto("ALTURA AMPLIADA", 246, 172, Estilo.PETROLEO.lightened(0.25))
	_texto("PEGASO %.0f x %.0f KM" % [pegaso_baja, pegaso_alta], 230, 162, Estilo.DORADO)
