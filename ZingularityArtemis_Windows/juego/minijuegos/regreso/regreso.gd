extends "res://nucleo/minijuego.gd"

# REENTRADA. Juego de accion en pixeles gordos: 320 x 180 logicos, cada pixel mide 4 x 4 en el lienzo.
# La capsula de carton cae hacia la Tierra. Izquierda y derecha la giran, con inercia, y el aire la empuja.
# Inclinada, el aire la desvia hacia ese lado: asi se rodean las zonas de calor. Demasiado inclinada, el
# escudo deja de ir por delante y la temperatura sube. Abajo = caer en picada (mas rapido, puntos dobles,
# mas calor). E o Espacio abre los paracaidas: solo aguantan dentro de la franja. Al final se ameriza
# entre las boyas, con el viento empujando.
# Grados, calor (0 a 100) y distancias son reglas del suenio: no equivalen a una capsula real.
# Dato real (ficha modulo_mando): escudo termico por delante, paracaidas y amerizaje en el Pacifico.
# Todo se dibuja por codigo con mapas de caracteres; no hay imagenes ni insignias.

const ANCHO: int = 320
const ALTO: int = 180
const PIXEL: float = 4.0
const HUD: int = 18                # alto del marcador
const CAMPO: int = 320             # ancho del campo de juego; el altimetro flota sobre el cielo
const DT: float = 1.0 / 60.0

const INTRO: int = 0
const REENTRADA: int = 1
const FRANJA: int = 2
const PARACAIDAS: int = 3
const AMERIZADO: int = 4
const PERDIDO: int = 5

const INTRO_S: float = 3.2
const Y_CAP: float = 72.0          # altura de la capsula en pantalla mientras cae
const X_MIN: float = 10.0
const X_MAX: float = 290.0
const RADIO_CAPSULA: float = 4.5
const LARGO: float = 1400.0        # pixeles de reentrada
const V_CAIDA: float = 34.0        # pixeles por segundo
const V_PICADA: float = 85.0
const V_FRANJA: float = 27.0
const V_PARACAIDAS: Array[float] = [25.0, 25.0, 19.0, 15.0]   # segun cuantos paracaidas abren
const ACEL_CAIDA: float = 150.0
const GIRO_MANDO: float = 260.0    # grados por segundo al cuadrado
const GIRO_ROCE: float = 2.5
const SUSTENTACION: float = 220.0  # empuje lateral del aire sobre la capsula inclinada
const ROCE_X: float = 1.5
const EMPUJE: float = 70.0         # mando lateral colgando de los paracaidas
const ROCE_PARACAIDAS: float = 1.0
const CALOR_INICIAL: float = 18.0
const ENFRIA: float = 7.0
const CALOR_PICADA: float = 3.0
const DIST_FRANJA: float = 95.0
const DIST_MAR: float = 140.0

const CAUSA_LADO: String = "La cápsula entró de lado: sin el escudo por delante, el calor de la reentrada alcanzó el cartón."
const CAUSA_BOLSAS: String = "Atravesaste demasiadas zonas de calor: inclina un poco la cápsula y el aire la desvía hacia ese lado."
const CAUSA_PICADA: String = "Caíste en picada demasiado tiempo: cuanto más rápido entra la cápsula, más se calienta."
const CAUSA_PRONTO: String = "Abriste los tres paracaídas por encima de la franja: a esa velocidad el aire los arrancó."
const CAUSA_TARDE: String = "Pasaste la franja sin abrir los paracaídas: ya no quedaba altura para frenar antes del agua."
const CAUSA_FUERA: String = "La cápsula tocó el agua fuera de las boyas: el viento empuja, corrige antes de llegar."
const LOGRO: String = "Escudo por delante, paracaídas en la franja y amerizaje entre las boyas: así volvió el módulo de mando al Pacífico el 24-07-1969."

const GLIFOS: Dictionary = {
	"A": ".#./#.#/###/#.#/#.#", "B": "##./#.#/##./#.#/##.", "C": ".##/#../#../#../.##",
	"D": "##./#.#/#.#/#.#/##.", "E": "###/#../##./#../###", "F": "###/#../##./#../#..",
	"G": ".##/#../#.#/#.#/.##", "H": "#.#/#.#/###/#.#/#.#", "I": "###/.#./.#./.#./###",
	"J": "..#/..#/..#/#.#/.#.", "K": "#.#/#.#/##./#.#/#.#", "L": "#../#../#../#../###",
	"M": "#.#/###/###/#.#/#.#", "N": "#.#/###/###/###/#.#", "O": "###/#.#/#.#/#.#/###",
	"P": "###/#.#/###/#../#..", "Q": "###/#.#/#.#/###/..#", "R": "##./#.#/##./#.#/#.#",
	"S": ".##/#../.#./..#/##.", "T": "###/.#./.#./.#./.#.", "U": "#.#/#.#/#.#/#.#/###",
	"V": "#.#/#.#/#.#/#.#/.#.", "W": "#.#/#.#/###/###/#.#", "X": "#.#/#.#/.#./#.#/#.#",
	"Y": "#.#/#.#/.#./.#./.#.", "Z": "###/..#/.#./#../###",
	"0": "###/#.#/#.#/#.#/###", "1": ".#./##./.#./.#./###", "2": "###/..#/###/#../###",
	"3": "###/..#/.##/..#/###", "4": "#.#/#.#/###/..#/..#", "5": "###/#../###/..#/###",
	"6": "###/#../###/#.#/###", "7": "###/..#/..#/.#./.#.", "8": "###/#.#/###/#.#/###",
	"9": "###/#.#/###/..#/###",
	".": ".../.../.../.../.#.", ":": ".../.#./.../.#./...", "!": ".#./.#./.#./.../.#.",
	"+": ".../.#./###/.#./...", "-": ".../.../###/.../...",
}
const ACENTOS: Dictionary = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ñ": "N"}

# C carton, c canto del carton, t cinta, w ventanilla, h tapa, e escudo (su color cambia con el calor)
const CAPSULA: Array[String] = [
	".....hhh.....",
	"....cCCCc....",
	"....CCtCC....",
	"...cCCtCCc...",
	"...CCwwwCC...",
	"..cCCwwwCCc..",
	"..CCCCtCCCC..",
	".cCCCCtCCCCc.",
	".CCCtCCCtCCC.",
	"cCCCCCCCCCCCc",
	"eeeeeeeeeeeee",
	".eeeeeeeeeee.",
]
const MODULO: Array[String] = [
	"..ppppp..",
	".wwwwwww.",
	".wpwwwpw.",
	".wwwwwww.",
	".wwwwwww.",
	".wpwwwpw.",
	".wwwwwww.",
	"..ww.ww..",
]
const TELA: Array[String] = [
	"...sSSSs...",
	".sSSsSsSSs.",
	"sSSsSSSsSSs",
	"SSsSSSSSsSS",
	"S..S...S..S",
]
const ICONO_PARACAIDAS: Array[String] = [
	".#####.",
	"#######",
	"#######",
	"#.#.#.#",
	".#.#.#.",
	"..#.#..",
	"...#...",
]
const BARCO: Array[String] = [
	".......P.......",
	"......PPp......",
	".....PPPpp.....",
	"....PPPPppp....",
	"...PPPPPpppp...",
	"PPPPPPPPPPPPPPP",
	".PPPPPPPPPPPPP.",
	"..ppppppppppp..",
]
const BOYA: Array[String] = [
	"..k..",
	"..D..",
	".DDD.",
	".DrD.",
	"DDDDD",
]
const TERMOMETRO: Array[String] = [
	".###.",
	".#.#.",
	".#.#.",
	".#.#.",
	".#.#.",
	".#.#.",
	"##.##",
	"#...#",
	"#...#",
	".###.",
]
const RELOJ: Array[String] = [
	".#####.",
	"#..#..#",
	"#..#..#",
	"#..##.#",
	"#.....#",
	"#.....#",
	".#####.",
]
const FLECHA_IZQ: Array[String] = ["..#..", ".#...", "#####", ".#...", "..#.."]
const FLECHA_DER: Array[String] = ["..#..", "...#.", "#####", "...#.", "..#.."]
const FLECHA_ABA: Array[String] = ["..#..", "..#..", "#.#.#", ".###.", "..#.."]
const MARCA: Array[String] = ["#....", "###..", "#####", "###..", "#...."]
const MINI_ESCUDO: Array[String] = ["#...#", "#...#", ".###."]
const MINI_TELA: Array[String] = [".###.", "#####", "#.#.#", ".#.#.", "..#.."]
const MINI_OLA: Array[String] = [".#...", "#.#.#", "...#."]
const VISTO: Array[String] = ["....#", "...#.", "#.#..", ".#..."]
# los seis pasos del regreso (ficha regreso_seis_pasos), como pictogramas de 11 x 11
const PASOS: Array = [
	[
		"....###....", "...#####...", "...#.#.#...", "...#####...", "....#.#....", "...#.#.#...",
		"....#.#....", "...........", "..#.....#..", ".#########.", "###########",
	],
	[
		"...........", "##.......##", "###.....###", "####.#.####", "###.....###", "##.......##",
		"...........", "..#.....#..", "####...####", "..#.....#..", "...........",
	],
	[
		".....#.....", "....###....", "...#####...", "..#######..", "...........", "..#..#..#..",
		"...........", "..#######..", "..#######..", "..#######..", "...#...#...",
	],
	[
		".....#.....", "....###....", "...#####...", "..#######..", ".#########.", ".#########.",
		"...........", "#.........#", "##.......##", ".###...###.", "...#####...",
	],
	[
		"...#####...", ".#########.", "###########", "#..#...#..#", ".#..#.#..#.", "..#.#.#.#..",
		"...#.#.#...", "....###....", "...#####...", "..#######..", "..#######..",
	],
	[
		".....#.....", "....###....", "...#####...", "..#######..", ".#########.", ".#########.",
		"...........", "##..###..##", "..##...##..", "##..###..##", "..##...##..",
	],
]

# ------------------------------------------------------------------ estado que se ve en pantalla

var fase: int = INTRO
var cap_x: float = 160.0           # centro de la capsula, en pixeles logicos
var cap_vx: float = 0.0
var angulo: float = 0.0            # grados; 0 = escudo hacia abajo, que es hacia donde cae
var giro: float = 0.0              # grados por segundo
var rafaga: float = 0.0            # empuje del aire sobre el giro
var calor: float = CALOR_INICIAL   # 0 a 100
var prof: float = 0.0              # pixeles caidos desde el principio
var velocidad: float = V_CAIDA
var margen: float = 26.0           # inclinacion que el escudo aguanta
var bolsas: Array[Dictionary] = [] # zonas de calor: {x, prof, r, vx, viva, contada}
var franja_ini: float = 0.0        # la franja de los paracaidas, en pixeles caidos
var franja_fin: float = 0.0
var paracaidas: int = 3            # los que quedan guardados
var abiertos: int = 0
var mar_prof: float = 0.0
var diana_x: float = 160.0         # centro de la zona marcada entre las boyas
var diana_medio: float = 26.0
var viento: float = 0.0
var puntos: float = 0.0
var vuelo: float = 0.0
var esquivadas: int = 0
var golpes: int = 0
# los mandos: los escriben las teclas o el piloto, y nadie mas
var mando_x: float = 0.0
var mando_abajo: bool = false

var _pulso: bool = false           # E, Espacio o clic, pendiente de atender
var _auto: int = 0
var _acum: float = 0.0
var _t_fase: float = 0.0
var _reloj: float = 0.0
var _azar: RandomNumberGenerator = RandomNumberGenerator.new()
var _fx: RandomNumberGenerator = RandomNumberGenerator.new()
var _f1: float = 0.0
var _f2: float = 0.0
var _rafaga_max: float = 35.0
var _radio: float = 11.0
var _separacion: float = 150.0
var _golpe: float = 22.0
var _ancho_franja: float = 46.0
var _viento_max: float = 12.0
var _viento_dir: float = 1.0
var _sig_bolsa: float = 190.0
var _calor_lado: float = 0.0
var _calor_bolsas: float = 0.0
var _calor_picada: float = 0.0
var _picada_ok: bool = true
var _causa: String = ""
var _tipo_perdida: String = ""
var _caida_extra: float = 0.0
var _prof_abrio: float = 0.0
var _alt_abrio: float = 84.0
var _inmune: float = 0.0
var _sacudida: float = 0.0
var _desvio: Vector2 = Vector2.ZERO
var _destello: float = 0.0
var _destello_color: Color = Estilo.CREMA
var _t_aviso: float = 0.0
var _t_tela: float = 0.0           # parpadeo del icono al perder un paracaidas
var _chispas: Array[Array] = []    # [x, y, vx, vy, vida, vida_total, color]
var _carteles: Array[Array] = []   # [x, y, texto, vida]
var _rasgados: Array[Array] = []   # telas arrancadas: [x, y, vx, vy]
var _estrellas: Array[Vector3] = []
var _vetas: Array[Vector3] = []
var _nubes: Array[Vector3] = []
var _glifos: Dictionary = {}
var _pal: Dictionary = {}
var _c_hud: Color = Estilo.NOCHE.darkened(0.35)
var _c_espacio: Color = Estilo.NOCHE.darkened(0.5)
var _c_aire: Color = Estilo.PETROLEO.darkened(0.55)
var _c_cielo: Color = Estilo.PETROLEO.darkened(0.25)
var _c_mar: Color = Estilo.PETROLEO.darkened(0.05)


func _init() -> void:
	pantalla_completa = true


func _nivel(a: float, b: float, c: float) -> float:
	return a if dificultad <= 1 else (b if dificultad == 2 else c)


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	margen = _nivel(26.0, 21.0, 16.0)
	_rafaga_max = _nivel(35.0, 55.0, 80.0)
	_radio = _nivel(11.0, 13.0, 15.0)
	_separacion = _nivel(150.0, 112.0, 88.0)
	_golpe = _nivel(22.0, 25.0, 28.0)
	_ancho_franja = _nivel(46.0, 36.0, 28.0)
	_viento_max = _nivel(12.0, 20.0, 28.0)
	diana_medio = _nivel(26.0, 20.0, 15.0)
	# cada intento de una persona cambia el recorrido; el piloto de las pruebas juega siempre el mismo
	var semilla: int = int(parametros.get("semilla", -1))
	if semilla < 0:
		var intento: int = 0
		if _solo == 0 and get_parent() != null:
			intento = int(get_parent().get_meta("regreso_intentos", 0))
			get_parent().set_meta("regreso_intentos", intento + 1)
		semilla = 4201 * dificultad + 17 * intento
	_azar.seed = semilla
	_fx.seed = semilla + 99
	_f1 = _azar.randf_range(0.0, TAU)
	_f2 = _azar.randf_range(0.0, TAU)
	for clave in GLIFOS:
		var dibujo: String = GLIFOS[clave]
		_glifos[clave] = dibujo.split("/")
	_pal = {
		"C": Estilo.CREMA, "c": Estilo.NARANJA, "t": Estilo.PAPEL, "w": Estilo.PETROLEO, "h": Estilo.TERRACOTA,
		"e": Estilo.TINTA_SUAVE, "S": Estilo.CORAL, "s": Estilo.CREMA, "P": Estilo.PAPEL, "p": Estilo.PAPEL_SOMBRA,
		"D": Estilo.DORADO, "k": Estilo.CIAN, "r": Estilo.CORAL, "#": Estilo.PAPEL,
	}
	for i in 42:
		_estrellas.append(Vector3(_fx.randf_range(2.0, CAMPO - 2.0), _fx.randf_range(HUD + 2.0, ALTO - 2.0), _fx.randf_range(0.0, TAU)))
	for i in 30:
		_vetas.append(Vector3(_fx.randf_range(2.0, CAMPO - 2.0), _fx.randf_range(0.0, float(ALTO - HUD)), _fx.randf_range(0.7, 1.5)))
	for i in 6:
		_nubes.append(Vector3(_fx.randf_range(0.0, CAMPO), LARGO + 30.0 + i * 62.0 + _fx.randf_range(-12.0, 12.0), _fx.randf_range(14.0, 30.0)))
	queue_redraw()


func _empezar() -> void:
	fase = INTRO
	_t_fase = 0.0


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


# ------------------------------------------------------------------ entradas

func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0:
		return
	if evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar"):
		_pulso = true
		get_viewport().set_input_as_handled()


func _gui_input(evento: InputEvent) -> void:
	# el raton es opcional: un clic vale por E
	if activo and _auto == 0 and evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		_pulso = true
		accept_event()


func _leer_mandos() -> void:
	if _auto != 0:
		_piloto()
	else:
		mando_x = eje_x()
		mando_abajo = Input.is_action_pressed("mover_abajo")


# ------------------------------------------------------------------ reglas

func _paso(delta: float) -> void:
	_acum += minf(delta, 0.5)
	while _acum >= DT and activo:
		_acum -= DT
		_leer_mandos()
		_tic(DT)
	queue_redraw()


func _tic(dt: float) -> void:
	_t_fase += dt
	_reloj += dt
	var pulso: bool = _pulso
	_pulso = false
	match fase:
		INTRO:
			if (pulso and _t_fase > 0.15) or _t_fase >= INTRO_S:
				_a_fase(REENTRADA)
				sonar("radio")
		REENTRADA:
			_tic_reentrada(dt)
		FRANJA:
			_tic_franja(dt, pulso)
		PARACAIDAS:
			_tic_paracaidas(dt)
		AMERIZADO:
			if _t_fase >= 1.9:
				terminar(true, floorf(puntos), LOGRO)
		PERDIDO:
			if _tipo_perdida != "fuera":
				_caida_extra += (150.0 if _tipo_perdida != "calor" else 20.0) * dt
			if _t_fase >= 1.2:
				terminar(false, floorf(puntos), _causa)
	_tic_efectos(dt)


func _a_fase(nueva: int) -> void:
	fase = nueva
	_t_fase = 0.0


func _girar(dt: float, fuerza: float) -> void:
	# el aire empuja el giro; el mando lo corrige; al soltar, la capsula conserva el giro
	rafaga = _rafaga_max * fuerza * (sin(1.1 * vuelo + _f1) + 0.6 * sin(2.7 * vuelo + _f2))
	giro += (clampf(mando_x, -1.0, 1.0) * GIRO_MANDO + rafaga - GIRO_ROCE * giro) * dt
	angulo += giro * dt
	if absf(angulo) > 80.0:
		angulo = clampf(angulo, -80.0, 80.0)
		giro = 0.0
	# inclinada, el aire que sube la desvia hacia el lado al que apunta su punta
	cap_vx += (SUSTENTACION * sin(deg_to_rad(angulo)) - ROCE_X * cap_vx) * dt
	_mover_x(dt)


func _mover_x(dt: float) -> void:
	cap_x += cap_vx * dt
	if cap_x < X_MIN or cap_x > X_MAX:
		cap_x = clampf(cap_x, X_MIN, X_MAX)
		cap_vx *= -0.3


func _tic_reentrada(dt: float) -> void:
	vuelo += dt
	_girar(dt, 1.0)
	var picada: bool = mando_abajo
	velocidad = move_toward(velocidad, V_PICADA if picada else V_CAIDA, ACEL_CAIDA * dt)
	var antes: float = prof
	prof += velocidad * dt
	var fuera: bool = absf(angulo) > margen
	if fuera:
		var sube: float = minf(14.0 + (absf(angulo) - margen), 45.0) * dt
		calor += sube
		_calor_lado += sube
		_t_aviso -= dt
		if _t_aviso <= 0.0:
			_t_aviso = 0.35
			sonar("tic")
	elif picada:
		calor += CALOR_PICADA * dt
		_calor_picada += CALOR_PICADA * dt
	else:
		calor = maxf(calor - ENFRIA * dt, 0.0)
	if not fuera:
		puntos += (prof - antes) * (0.5 if picada else 0.25)
	_generar_bolsas()
	_chocar_bolsas(dt)
	if calor >= 100.0:
		calor = 100.0
		var causa: String = CAUSA_LADO
		if _calor_bolsas > _calor_lado and _calor_bolsas >= _calor_picada:
			causa = CAUSA_BOLSAS
		elif _calor_picada > _calor_lado:
			causa = CAUSA_PICADA
		_perder(causa, "calor")
	elif prof >= LARGO:
		franja_ini = prof + DIST_FRANJA
		franja_fin = franja_ini + _ancho_franja
		_a_fase(FRANJA)
		sonar("ok")


func _generar_bolsas() -> void:
	while _sig_bolsa <= prof + float(ALTO) - Y_CAP + 20.0 and _sig_bolsa < LARGO - 70.0:
		var bx: float = cap_x + _azar.randf_range(-22.0, 22.0)
		if _azar.randf() > 0.65:
			bx = _azar.randf_range(20.0, CAMPO - 20.0)
		bx = clampf(bx, 18.0, CAMPO - 18.0)
		_nueva_bolsa(bx, _sig_bolsa)
		if dificultad >= 2 and _azar.randf() < (0.3 if dificultad == 2 else 0.5):
			var lado: float = 1.0 if _azar.randf() < 0.5 else -1.0
			var lejos: float = _azar.randf_range(54.0, 82.0)
			var bx2: float = bx + lado * lejos
			if bx2 < 18.0 or bx2 > CAMPO - 18.0:
				bx2 = bx - lado * lejos
			_nueva_bolsa(clampf(bx2, 18.0, CAMPO - 18.0), _sig_bolsa + _azar.randf_range(-8.0, 8.0))
		_sig_bolsa += _separacion * _azar.randf_range(0.8, 1.2)


func _nueva_bolsa(bx: float, bprof: float) -> void:
	var deriva: float = _azar.randf_range(-6.0, 6.0) if dificultad == 3 else 0.0
	bolsas.append({"x": bx, "prof": bprof, "r": _radio, "vx": deriva, "viva": true, "contada": false})


func _chocar_bolsas(dt: float) -> void:
	var i: int = bolsas.size() - 1
	while i >= 0:
		var b: Dictionary = bolsas[i]
		var bx: float = float(b["x"]) + float(b["vx"]) * dt
		var r: float = b["r"]
		if bx < r or bx > CAMPO - r:
			b["vx"] = -float(b["vx"])
		b["x"] = bx
		var by: float = Y_CAP + float(b["prof"]) - prof
		if by < float(HUD) - r - 4.0:
			bolsas.remove_at(i)
		elif bool(b["viva"]):
			var dx: float = bx - cap_x
			var dy: float = by - Y_CAP
			var alcance: float = r + RADIO_CAPSULA
			if _inmune <= 0.0 and dx * dx + dy * dy < alcance * alcance:
				b["viva"] = false
				golpes += 1
				calor += _golpe
				_calor_bolsas += _golpe
				_inmune = 0.7
				_sacudida = 0.3
				_destellar(Estilo.CORAL, 0.5)
				sonar("error")
				_estallar(bx, by, 18, Estilo.NARANJA, 50.0)
			elif by < Y_CAP - r - 8.0 and not bool(b["contada"]):
				b["contada"] = true
				esquivadas += 1
				puntos += 50.0
				sonar("recoger")
				_carteles.append([cap_x - 6.0, Y_CAP - 16.0, "+50", 0.8])
		i -= 1


func _tic_franja(dt: float, pulso: bool) -> void:
	vuelo += dt
	_girar(dt, 0.5)
	velocidad = move_toward(velocidad, V_FRANJA, ACEL_CAIDA * dt)
	prof += velocidad * dt
	calor = maxf(calor - 12.0 * dt, 0.0)
	_chocar_bolsas(dt)
	if pulso:
		if prof < franja_ini:
			# todavia va demasiado rapido: el aire arranca la tela
			paracaidas -= 1
			_t_tela = 0.8
			_sacudida = 0.25
			sonar("error")
			_rasgados.append([cap_x - 5.0, Y_CAP - 18.0, _fx.randf_range(-14.0, 14.0), -70.0])
			if paracaidas <= 0:
				_perder(CAUSA_PRONTO, "caida")
		else:
			_abrir_paracaidas()
	elif prof > franja_fin + 4.0:
		_perder(CAUSA_TARDE, "caida")


func _abrir_paracaidas() -> void:
	abiertos = paracaidas
	_prof_abrio = prof
	_alt_abrio = _y_altimetro()
	mar_prof = prof + DIST_MAR
	var lejos: float = _azar.randf_range(_nivel(45.0, 55.0, 65.0), _nivel(85.0, 100.0, 115.0))
	var lado: float = 1.0 if _azar.randf() < 0.5 else -1.0
	diana_x = cap_x + lado * lejos
	if diana_x < 36.0 or diana_x > CAMPO - 36.0:
		diana_x = cap_x - lado * lejos
	diana_x = clampf(diana_x, 36.0, CAMPO - 36.0)
	_viento_dir = 1.0 if _azar.randf() < 0.5 else -1.0
	puntos += 100.0 * abiertos
	_a_fase(PARACAIDAS)
	_sacudida = 0.2
	_destellar(Estilo.PAPEL, 0.45)
	sonar("salto")
	_estallar(cap_x, Y_CAP - 12.0, 10, Estilo.PAPEL, 30.0)


func _tic_paracaidas(dt: float) -> void:
	vuelo += dt
	velocidad = move_toward(velocidad, V_PARACAIDAS[abiertos], 90.0 * dt)
	prof += velocidad * dt
	viento = _viento_max * _viento_dir * (0.55 + 0.45 * sin(0.8 * _t_fase + _f1))
	cap_vx += (clampf(mando_x, -1.0, 1.0) * EMPUJE + viento - ROCE_PARACAIDAS * cap_vx) * dt
	_mover_x(dt)
	# colgada de las telas, la capsula se endereza sola y se mece
	angulo = lerpf(angulo, clampf(cap_vx * 0.4, -20.0, 20.0), minf(6.0 * dt, 1.0))
	giro = 0.0
	calor = maxf(calor - 12.0 * dt, 0.0)
	if prof >= mar_prof - 6.0:
		prof = mar_prof - 6.0
		var lejos: float = absf(cap_x - diana_x)
		_estallar(cap_x, _y_capsula() + 5.0, 22, Estilo.PAPEL, 45.0)
		if lejos <= diana_medio:
			puntos += 100.0 + 300.0 * (1.0 - lejos / diana_medio)
			_a_fase(AMERIZADO)
			_destellar(Estilo.PAPEL, 0.4)
			sonar("logro")
		else:
			_sacudida = 0.3
			_perder(CAUSA_FUERA, "fuera")


func _perder(causa: String, tipo: String) -> void:
	_causa = causa
	_tipo_perdida = tipo
	_a_fase(PERDIDO)
	_sacudida = maxf(_sacudida, 0.4)
	if tipo == "calor":
		_destellar(Estilo.CORAL, 0.7)
		_estallar(cap_x, Y_CAP, 30, Estilo.CORAL, 70.0)


# ------------------------------------------------------------------ piloto de las pruebas

func _piloto() -> void:
	# juega con las mismas reglas: solo escribe mando_x, mando_abajo y _pulso, como las teclas
	mando_x = 0.0
	mando_abajo = false
	if fase == INTRO:
		_pulso = _t_fase > 0.2
		return
	if _auto < 0:
		# gira sin soltar: el escudo queda de lado y el calor sube
		mando_x = 1.0
		return
	if fase == REENTRADA:
		var destino: float = _carril_libre()
		var inclinacion: float = clampf((destino - cap_x) * 0.9 - cap_vx * 0.8, -margen * 0.72, margen * 0.72)
		mando_x = _mando_giro(inclinacion)
		var despejado: bool = absf(destino - cap_x) < 3.0
		for b in bolsas:
			if bool(b["viva"]) and Y_CAP + float(b["prof"]) - prof > Y_CAP - 14.0 and absf(float(b["x"]) - cap_x) < float(b["r"]) + 22.0:
				despejado = false
		if calor > 50.0:
			_picada_ok = false
		elif calor < 28.0:
			_picada_ok = true
		mando_abajo = despejado and _picada_ok and absf(angulo) < margen * 0.6 and prof < LARGO - 30.0
	elif fase == FRANJA:
		mando_x = _mando_giro(clampf(-cap_vx * 0.8, -margen * 0.5, margen * 0.5))
		if prof >= franja_ini + 4.0:
			_pulso = true
	elif fase == PARACAIDAS:
		var falta: float = (diana_x - cap_x) - cap_vx * 0.6
		mando_x = signf(falta) if absf(falta) > 1.5 else 0.0


func _mando_giro(objetivo: float) -> float:
	# pulsos de tecla: frena antes de llegar, porque la capsula conserva el giro
	var falta: float = (objetivo - angulo) - giro * 0.16
	return signf(falta) if absf(falta) > 1.5 else 0.0


func _carril_libre() -> float:
	var mejor: float = cap_x
	var costo_mejor: float = _costo_carril(cap_x)
	var c: float = X_MIN + 8.0
	while c <= X_MAX - 8.0:
		var costo: float = _costo_carril(c)
		if costo < costo_mejor - 0.01:
			costo_mejor = costo
			mejor = c
		c += 4.0
	return mejor


func _costo_carril(c: float) -> float:
	var costo: float = absf(c - cap_x) + absf(c - 160.0) * 0.05
	for b in bolsas:
		if not bool(b["viva"]):
			continue
		var r: float = b["r"]
		var by: float = Y_CAP + float(b["prof"]) - prof
		if by < Y_CAP - r - 6.0:
			continue
		var llegada: float = maxf(by - Y_CAP, 0.0) / maxf(velocidad, 1.0)
		var bx: float = float(b["x"]) + float(b["vx"]) * llegada
		var holgura: float = minf(absf(bx - c), absf(float(b["x"]) - c)) - (r + 11.0)
		if holgura < 0.0:
			costo += 300.0 + 6000.0 / (by - Y_CAP + r + 30.0) - holgura * 4.0
	return costo


# ------------------------------------------------------------------ efectos

func _destellar(color: Color, fuerza: float) -> void:
	_destello = fuerza
	_destello_color = color


func _estallar(x: float, y: float, cuantas: int, color: Color, fuerza: float) -> void:
	for i in cuantas:
		var a: float = _fx.randf_range(0.0, TAU)
		var v: float = _fx.randf_range(fuerza * 0.3, fuerza)
		_chispa(x, y, cos(a) * v, sin(a) * v, _fx.randf_range(0.35, 0.8), color)


func _chispa(x: float, y: float, vx: float, vy: float, vida: float, color: Color) -> void:
	if _chispas.size() < 110:
		_chispas.append([x, y, vx, vy, vida, vida, color])


func _tic_efectos(dt: float) -> void:
	_inmune = maxf(_inmune - dt, 0.0)
	_t_tela = maxf(_t_tela - dt, 0.0)
	_destello = maxf(_destello - dt * 1.6, 0.0)
	if _sacudida > 0.0:
		_sacudida = maxf(_sacudida - dt, 0.0)
		_desvio = Vector2(roundf(_fx.randf_range(-1.6, 1.6)), roundf(_fx.randf_range(-1.6, 1.6))) if _sacudida > 0.0 else Vector2.ZERO
	var cy: float = _y_capsula()
	if fase == REENTRADA:
		# estela: el aire caliente queda arriba, porque la capsula cae
		var lado: float = -6.0 if _fx.randf() < 0.5 else 6.0
		_chispa(cap_x + lado + _fx.randf_range(-1.0, 1.0), cy + 1.0, _fx.randf_range(-4.0, 4.0), -velocidad * 1.3, 0.35, Estilo.NARANJA if calor < 60.0 else Estilo.CORAL)
		if mando_abajo:
			_chispa(cap_x + _fx.randf_range(-5.0, 5.0), cy + 6.0, _fx.randf_range(-10.0, 10.0), -velocidad * 1.6, 0.3, Estilo.DORADO)
		if absf(angulo) > margen:
			var costado: float = signf(angulo)
			_chispa(cap_x - costado * 5.0, cy + 2.0, -costado * _fx.randf_range(10.0, 40.0), _fx.randf_range(-60.0, -20.0), 0.4, Estilo.CORAL)
	elif fase == PERDIDO and _tipo_perdida == "calor":
		_chispa(cap_x + _fx.randf_range(-6.0, 6.0), cy + _fx.randf_range(-6.0, 6.0), _fx.randf_range(-30.0, 30.0), _fx.randf_range(-60.0, -10.0), 0.5, Estilo.CORAL)
	elif fase == AMERIZADO and _fx.randf() < 0.3:
		_chispa(cap_x + _fx.randf_range(-9.0, 9.0), cy + 6.0, _fx.randf_range(-12.0, 12.0), _fx.randf_range(-26.0, -8.0), 0.5, Estilo.PAPEL)
	var i: int = _chispas.size() - 1
	while i >= 0:
		var c: Array = _chispas[i]
		c[4] = float(c[4]) - dt
		if float(c[4]) <= 0.0:
			_chispas.remove_at(i)
		else:
			c[0] = float(c[0]) + float(c[2]) * dt
			c[1] = float(c[1]) + float(c[3]) * dt
		i -= 1
	i = _carteles.size() - 1
	while i >= 0:
		var cartel: Array = _carteles[i]
		cartel[3] = float(cartel[3]) - dt
		cartel[1] = float(cartel[1]) - 14.0 * dt
		if float(cartel[3]) <= 0.0:
			_carteles.remove_at(i)
		i -= 1
	i = _rasgados.size() - 1
	while i >= 0:
		var tela: Array = _rasgados[i]
		tela[0] = float(tela[0]) + float(tela[2]) * dt
		tela[1] = float(tela[1]) + float(tela[3]) * dt
		if float(tela[1]) < -10.0:
			_rasgados.remove_at(i)
		i -= 1


# ------------------------------------------------------------------ geometria de la pantalla

func _camara() -> float:
	# la camara sigue a la capsula hasta que el mar queda a la vista
	if mar_prof > 0.0:
		return minf(prof, mar_prof - 78.0)
	return prof


func _y_capsula() -> float:
	return Y_CAP + prof - _camara() + _caida_extra


func _y_altimetro() -> float:
	if prof <= LARGO or franja_ini <= 0.0:
		return 26.0 + 90.0 * clampf(prof / LARGO, 0.0, 1.0)
	if abiertos > 0:
		return _alt_abrio + (162.0 - _alt_abrio) * clampf((prof - _prof_abrio) / (mar_prof - 6.0 - _prof_abrio), 0.0, 1.0)
	if prof < franja_ini:
		return 116.0 + 4.0 * (prof - LARGO) / (franja_ini - LARGO)
	return 120.0 + minf(12.0 * (prof - franja_ini) / (franja_fin - franja_ini), 30.0)


# ------------------------------------------------------------------ dibujo

func _draw() -> void:
	var escala: Vector2 = Vector2(PIXEL, PIXEL)
	draw_set_transform(Vector2.ZERO, 0.0, escala)
	var t1: float = clampf(prof / LARGO, 0.0, 1.0)
	var t2: float = clampf((prof - LARGO) / 240.0, 0.0, 1.0)
	draw_rect(Rect2(0, 0, ANCHO, ALTO), _c_espacio.lerp(_c_aire, t1).lerp(_c_cielo, t2))
	draw_set_transform(_desvio * PIXEL, 0.0, escala)
	_dibujar_fondo(t1, t2)
	_dibujar_mar()
	_dibujar_franja()
	_dibujar_bolsas()
	_dibujar_chispas()
	_dibujar_capsula()
	_dibujar_carteles()
	draw_set_transform(Vector2.ZERO, 0.0, escala)
	if _destello > 0.0:
		draw_rect(Rect2(0, HUD, CAMPO, ALTO - HUD), Color(_destello_color, minf(_destello, 0.5)))
	_dibujar_avisos()
	if fase == INTRO:
		_dibujar_mision()
	_dibujar_altimetro()
	_dibujar_marcador()


func _r(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2(floorf(x), floorf(y), w, h), color)


func _sprite(mapa: Array, x: float, y: float, e: int = 1, tinte: Color = Color(0, 0, 0, 0)) -> void:
	var ox: float = floorf(x)
	var oy: float = floorf(y)
	for fy in mapa.size():
		var fila: String = mapa[fy]
		for fx in fila.length():
			var c: String = fila[fx]
			if c != ".":
				var color: Color = tinte
				if tinte.a <= 0.0:
					color = _pal[c]
				draw_rect(Rect2(ox + fx * e, oy + fy * e, e, e), color)


func _escribir(t: String, x: float, y: float, color: Color, e: int = 1) -> void:
	var cx: float = floorf(x)
	var oy: float = floorf(y)
	for i in t.length():
		var c: String = t[i]
		var base: String = c
		if ACENTOS.has(c):
			base = ACENTOS[c]
			if c == "Ñ":
				draw_rect(Rect2(cx, oy - 2 * e, 3 * e, e), color)
			else:
				draw_rect(Rect2(cx + e, oy - 2 * e, e, e), color)
		if _glifos.has(base):
			var filas: PackedStringArray = _glifos[base]
			for fy in 5:
				var fila: String = filas[fy]
				for fx in 3:
					if fila[fx] == "#":
						draw_rect(Rect2(cx + fx * e, oy + fy * e, e, e), color)
		cx += 4 * e


func _ancho(t: String, e: int = 1) -> float:
	return float(t.length() * 4 * e - e)


func _centrado(t: String, y: float, color: Color, e: int = 1) -> void:
	_escribir(t, (CAMPO - _ancho(t, e)) * 0.5, y, color, e)


func _tecla(x: float, y: float, dibujo: Variant, encendida: bool = true) -> void:
	# tecla de 9 x 9 con una flecha (mapa) o una letra
	_r(x, y, 9, 9, Estilo.PAPEL if encendida else Estilo.TINTA_SUAVE)
	_r(x + 1, y + 1, 7, 7, _c_hud)
	var tinta: Color = Estilo.CIAN if encendida else Estilo.TINTA_SUAVE
	if dibujo is String:
		_escribir(dibujo, x + 3, y + 2, tinta)
	else:
		_sprite(dibujo, x + 2, y + 2, 1, tinta)


func _rayo(cx: float, cy: float, grados: float, r0: float, r1: float, paso: float, color: Color) -> void:
	# puntos sueltos desde la capsula; 0 grados = hacia abajo
	var a: float = deg_to_rad(grados)
	var r: float = r0
	while r <= r1:
		_r(roundf(cx + sin(a) * r), roundf(cy + cos(a) * r), 1, 1, color)
		r += paso


func _linea(x0: int, y0: int, x1: int, y1: int, color: Color) -> void:
	var dx: int = absi(x1 - x0)
	var dy: int = -absi(y1 - y0)
	var sx: int = 1 if x0 < x1 else -1
	var sy: int = 1 if y0 < y1 else -1
	var err: int = dx + dy
	for paso in 200:
		draw_rect(Rect2(x0, y0, 1, 1), color)
		if x0 == x1 and y0 == y1:
			break
		var e2: int = 2 * err
		if e2 >= dy:
			err += dy
			x0 += sx
		if e2 <= dx:
			err += dx
			y0 += sy


func _dibujar_fondo(t1: float, t2: float) -> void:
	# estrellas arriba, vetas de aire que suben y nubes al final
	if t1 < 0.75:
		for e in _estrellas:
			var brillo: float = (0.45 + 0.35 * sin(_reloj * 2.0 + e.z)) * (1.0 - t1 / 0.75)
			_r(e.x, e.y, 1, 1, Color(Estilo.PAPEL, brillo))
	var cam: float = _camara()
	var largo: float = 3.0 + velocidad * 0.09
	var sesgo: float = clampf(rafaga / maxf(_rafaga_max, 1.0), -1.6, 1.6) if fase <= FRANJA else clampf(viento / 14.0, -2.0, 2.0)
	var alfa: float = 0.10 + 0.22 * t1
	for v in _vetas:
		var y: float = float(HUD) + fposmod(v.y - cam * v.z, float(ALTO - HUD))
		if fase >= PARACAIDAS:
			# con las telas abiertas el aire ya no corre hacia arriba: lo que se ve es el viento
			var x: float = fposmod(v.x + _reloj * viento * 1.5 * v.z, float(CAMPO))
			_r(x, y, 4, 1, Color(Estilo.PAPEL, 0.22))
		else:
			for k in int(largo):
				_r(v.x + roundf(sesgo * k * 0.4), y + k, 1, 1, Color(Estilo.PAPEL, alfa))
	if t2 > 0.0:
		for n in _nubes:
			var ny: float = Y_CAP + (n.y - cam) * 0.7
			if ny > float(HUD) - 8.0 and ny < float(ALTO):
				var nx: float = fposmod(n.x + _reloj * viento * 0.4, float(CAMPO) + 40.0) - 20.0
				var tono: Color = Color(Estilo.PAPEL, 0.20)
				_r(nx, ny, n.z, 3, tono)
				_r(nx + 3.0, ny - 2.0, n.z - 8.0, 2, tono)
				_r(nx + 5.0, ny + 3.0, n.z - 11.0, 1, tono)


func _dibujar_mar() -> void:
	if mar_prof <= 0.0:
		return
	var y_mar: float = Y_CAP + mar_prof - _camara()
	var x0: float = diana_x - diana_medio
	var x1: float = diana_x + diana_medio
	var guinio: bool = fmod(_reloj, 0.6) < 0.36
	if y_mar >= float(ALTO):
		# el mar aun no se ve: dos marcas en el borde senalan la zona
		for x in [x0, x1]:
			_r(x - 2.0, ALTO - 7.0, 5, 1, Estilo.CIAN)
			_r(x - 1.0, ALTO - 6.0, 3, 1, Estilo.CIAN)
			_r(x, ALTO - 5.0, 1, 1, Estilo.CIAN)
		var px: float = x0 + 4.0
		while px < x1 - 2.0:
			_r(px, ALTO - 2.0, 2, 1, Color(Estilo.CIAN, 0.9 if guinio else 0.5))
			px += 5.0
		return
	_r(0, y_mar, CAMPO, ALTO - y_mar, _c_mar)
	var fila: int = 0
	var y: float = y_mar
	while y < float(ALTO):
		var corrido: float = fposmod(_reloj * (6.0 + fila * 2.0) + fila * 7.0, 16.0)
		var x: float = -16.0 + corrido
		while x < float(CAMPO):
			_r(x, y, 5 if fila == 0 else 3, 1, Color(Estilo.PAPEL, 0.55 if fila == 0 else 0.22))
			x += 16.0
		y += 3.0 + fila
		fila += 1
	# la zona marcada: linea cian entre dos boyas
	var px2: float = x0 + 3.0
	while px2 < x1 - 2.0:
		_r(px2, y_mar, 3, 1, Estilo.CIAN)
		px2 += 5.0
	for x in [x0, x1]:
		_sprite(BOYA, x - 2.0, y_mar - 4.0 + roundf(sin(_reloj * 3.0 + x) * 0.6))
		if not guinio:
			_r(x, y_mar - 4.0, 1, 1, Estilo.NOCHE)
	if fase == AMERIZADO:
		# el barco de papel viene a buscar la caja
		var desde: float = -18.0 if cap_x < CAMPO * 0.5 else float(CAMPO) + 4.0
		var hasta: float = cap_x + (-26.0 if cap_x < CAMPO * 0.5 else 12.0)
		var bx: float = lerpf(desde, hasta, clampf(_t_fase / 1.6, 0.0, 1.0))
		_sprite(BARCO, bx, y_mar - 7.0 + roundf(sin(_reloj * 4.0) * 0.6))


func _dibujar_franja() -> void:
	if franja_ini <= 0.0 or fase >= AMERIZADO and abiertos > 0:
		return
	var cam: float = _camara()
	var y0: float = floorf(Y_CAP + franja_ini - cam)
	var y1: float = floorf(Y_CAP + franja_fin - cam)
	if y0 >= float(ALTO) or y1 < float(HUD):
		return
	var dentro: bool = fase == FRANJA and prof >= franja_ini and prof <= franja_fin
	var y: float = maxf(y0, float(HUD))
	while y < minf(y1, float(ALTO)):
		_r(0, y, CAMPO, 1, Color(Estilo.CIAN, 0.26 if dentro else 0.10))
		y += 2.0
	var corrido: float = fposmod(_reloj * 10.0, 8.0)
	var x: float = -8.0 + corrido
	while x < float(CAMPO):
		_r(x, y0, 5, 1, Estilo.CIAN)
		_r(x, y1, 5, 1, Estilo.CIAN)
		x += 8.0
	var medio: float = (y0 + y1) * 0.5
	for lado in [10.0, float(CAMPO) - 30.0]:
		_tecla(lado, medio - 4.0, "E")
		_sprite(ICONO_PARACAIDAS, lado + 11.0, medio - 3.0, 1, Estilo.CIAN)


func _dibujar_bolsas() -> void:
	var cam: float = _camara()
	for b in bolsas:
		if not bool(b["viva"]):
			continue
		var r: float = b["r"]
		var ox: float = roundf(float(b["x"]))
		var oy: float = roundf(Y_CAP + float(b["prof"]) - cam)
		var ri: int = int(r)
		for dy in range(-ri, ri + 1):
			var yy: float = oy + dy
			if yy < float(HUD) or yy >= float(ALTO):
				continue
			var w: float = sqrt(r * r - float(dy * dy))
			var onda: float = sin(_reloj * 7.0 + dy * 0.9 + ox) * 1.3
			var w0: int = int(w + onda)
			if w0 > 0:
				draw_rect(Rect2(ox - w0, yy, w0 * 2 + 1, 1), Estilo.CORAL)
			var w1: int = int(w * 0.66 - onda * 0.6)
			if w1 > 0 and absi(dy) < ri - 2:
				draw_rect(Rect2(ox - w1, yy, w1 * 2 + 1, 1), Estilo.NARANJA)
			var w2: int = int(w * 0.34 + onda * 0.4)
			if w2 > 0 and absi(dy) < ri - 5:
				draw_rect(Rect2(ox - w2, yy, w2 * 2 + 1, 1), Estilo.DORADO)
		# lenguas de calor: se reconoce por la forma, no solo por el color
		for k in 4:
			var lx: float = ox + (k - 1.5) * r * 0.5
			var alto: float = 2.0 + fposmod(_reloj * 9.0 + k * 1.7, 4.0)
			var ly: float = oy - r - alto
			if ly >= float(HUD):
				_r(lx, ly, 1, alto, Estilo.NARANJA)


func _dibujar_chispas() -> void:
	for c in _chispas:
		var y: float = c[1]
		if y >= float(HUD) and y < float(ALTO):
			var color: Color = c[6]
			_r(float(c[0]), y, 1, 1, Color(color, clampf(float(c[4]) / float(c[5]), 0.0, 1.0)))
	for tela in _rasgados:
		_sprite(TELA, float(tela[0]), float(tela[1]))


func _dibujar_capsula() -> void:
	var cx: float = cap_x
	var cy: float = _y_capsula()
	if cy > float(ALTO) + 12.0:
		return
	if fase == REENTRADA:
		# modulo de servicio: se separa al empezar y queda atras
		if _t_fase < 1.6:
			_sprite(MODULO, cx - 4.0 + _t_fase * 5.0, cy - 16.0 - _t_fase * 26.0)
		var fuera: bool = absf(angulo) > margen
		var guia: Color = Color(Estilo.CREMA, 0.5)
		if fuera:
			guia = Color(Estilo.CORAL, 0.95 if fmod(_reloj, 0.3) < 0.18 else 0.55)
		_rayo(cx, cy, margen, 12.0, 27.0, 3.0, guia)
		_rayo(cx, cy, -margen, 12.0, 27.0, 3.0, guia)
		# onda de choque: el aire caliente siempre viene de abajo
		var fuerte: float = clampf(velocidad / V_PICADA, 0.3, 1.0)
		for k in range(-4, 5):
			var a: float = deg_to_rad(k * 14.0)
			var temblor: float = 1.0 if fmod(_reloj * 12.0 + k, 2.0) < 1.0 else 0.0
			_r(roundf(cx + sin(a) * 11.0), roundf(cy + cos(a) * (10.0 + temblor)), 1, 1, Color(Estilo.NARANJA if absi(k) > 1 else Estilo.DORADO, 0.35 + 0.6 * fuerte))
		# aguja cian: hacia donde mira el escudo
		_rayo(cx, cy, -angulo, 9.0, 21.0, 2.0, Estilo.CIAN)
		if _t_fase < 3.5 and _auto == 0:
			_tecla(cx - 26.0, cy - 5.0, FLECHA_IZQ, mando_x < -0.1 or fmod(_reloj, 0.8) < 0.5)
			_tecla(cx + 18.0, cy - 5.0, FLECHA_DER, mando_x > 0.1 or fmod(_reloj, 0.8) < 0.5)
		elif _t_fase >= 4.0 and _t_fase < 7.0 and _auto == 0:
			_tecla(cx - 4.0, cy + 30.0, FLECHA_ABA, fmod(_reloj, 0.8) < 0.5)
			_escribir("X2", cx + 8.0, cy + 32.0, Estilo.DORADO)
	if abiertos > 0 and fase != PERDIDO or (fase == PERDIDO and _tipo_perdida == "fuera"):
		_dibujar_telas(cx, cy)
	if fase == FRANJA and prof >= franja_ini and prof <= franja_fin and fmod(_reloj, 0.4) < 0.26:
		_tecla(cx + 12.0, cy - 16.0, "E")
	if _inmune > 0.0 and fmod(_inmune, 0.16) < 0.08:
		return
	var tibio: float = clampf(calor / 100.0, 0.0, 1.0)
	var escudo: Color = Estilo.TINTA_SUAVE.lerp(Estilo.NARANJA, minf(tibio * 1.6, 1.0)).lerp(Estilo.CORAL, clampf(tibio * 2.0 - 1.0, 0.0, 1.0))
	if fase == PERDIDO and _tipo_perdida == "calor":
		escudo = Estilo.CORAL
		_pal["C"] = Estilo.NARANJA if fmod(_reloj, 0.2) < 0.1 else Estilo.CORAL
	_pal["e"] = escudo
	var flota: float = roundf(sin(_reloj * 3.0) * 0.7) if fase == AMERIZADO else 0.0
	_capsula(cx, cy + flota, angulo)
	_pal["C"] = Estilo.CREMA


func _capsula(cx: float, cy: float, grados: float, e: int = 1) -> void:
	# giro por pixeles: cada punto de destino busca su punto en el mapa
	var a: float = deg_to_rad(grados)
	var ca: float = cos(a)
	var sa: float = sin(a)
	var ox: float = roundf(cx)
	var oy: float = roundf(cy)
	for dy in range(-9, 10):
		for dx in range(-9, 10):
			var ix: int = floori(ca * dx + sa * dy + 6.5)
			var iy: int = floori(-sa * dx + ca * dy + 6.5)
			if ix < 0 or ix > 12 or iy < 0 or iy > 11:
				continue
			var c: String = CAPSULA[iy][ix]
			if c != ".":
				var color: Color = _pal[c]
				draw_rect(Rect2(ox + dx * e, oy + dy * e, e, e), color)


func _dibujar_telas(cx: float, cy: float) -> void:
	var puestos: Array[Vector2] = [Vector2(0, -22)]
	if abiertos == 2:
		puestos = [Vector2(-7, -21), Vector2(7, -21)]
	elif abiertos >= 3:
		puestos = [Vector2(-11, -19), Vector2(0, -24), Vector2(11, -19)]
	var caida: float = 0.0
	if fase == AMERIZADO or fase == PERDIDO:
		caida = minf(_t_fase * 22.0, 21.0)
	var abre: float = clampf(_t_fase / 0.25, 0.3, 1.0) if fase == PARACAIDAS else 1.0
	var mece: float = roundf(sin(_reloj * 2.2) * 1.2 - cap_vx * 0.05)
	for p in puestos:
		var tx: float = roundf(cx + p.x * abre * (1.0 + caida * 0.05) + mece)
		var ty: float = roundf(cy + p.y * abre + caida)
		if caida < 12.0:
			_linea(int(tx) - 4, int(ty) + 3, int(roundf(cx)) - 1, int(roundf(cy)) - 6, Color(Estilo.PAPEL, 0.55))
			_linea(int(tx) + 4, int(ty) + 3, int(roundf(cx)) + 1, int(roundf(cy)) - 6, Color(Estilo.PAPEL, 0.55))
		_sprite(TELA, tx - 5.0, ty - 2.0)


func _dibujar_carteles() -> void:
	for cartel in _carteles:
		var y: float = cartel[1]
		if y > float(HUD) + 1.0:
			_escribir(str(cartel[2]), float(cartel[0]), y, Estilo.DORADO)


func _dibujar_avisos() -> void:
	# una linea corta al cambiar de etapa; lo demas se entiende mirando
	var linea: String = ""
	if fase == REENTRADA:
		linea = "ESCUDO ABAJO. ESQUIVA EL CALOR."
	elif fase == FRANJA and abiertos == 0:
		linea = "E: PARACAÍDAS EN LA FRANJA"
	elif fase == PARACAIDAS:
		linea = "AMERIZA ENTRE LAS BOYAS"
	if linea != "":
		var w: float = _ancho(linea)
		var x: float = (CAMPO - w) * 0.5
		_r(x - 4.0, HUD + 2.0, w + 8.0, 11, Color(_c_hud, 0.85))
		_escribir(linea, x, HUD + 6.0, Estilo.PAPEL)
		var icono: Array = MINI_ESCUDO if fase == REENTRADA else (MINI_TELA if fase == FRANJA else MINI_OLA)
		_sprite(icono, x - 12.0, HUD + 5.0, 1, Estilo.CIAN)
	if fase == PARACAIDAS:
		# manga de viento: hacia donde empuja y cuanto
		var fuerza: int = clampi(int(absf(viento) / 4.0) + 1, 1, 7)
		var sentido: float = signf(viento)
		var base: float = 12.0 if sentido > 0.0 else 44.0
		_r(base, HUD + 18.0, 1, 7, Estilo.PAPEL)
		for k in fuerza:
			_r(base + sentido * (1.0 + k * 3.0) - (2.0 if sentido < 0.0 else 0.0), HUD + 18.0 + (k % 2), 3, 3, Estilo.CORAL if k % 2 == 0 else Estilo.CREMA)


func _dibujar_mision() -> void:
	# la mision, de un vistazo: una linea, la capsula de muestra y los seis pasos con sus teclas
	_r(0, HUD, CAMPO, ALTO - HUD, Color(_c_espacio, 0.88))
	_centrado("ESCUDO ABAJO. ESQUIVA EL CALOR.", 20.0, Estilo.CREMA, 2)
	var cx: float = 160.0
	var cy: float = 78.0
	var mece: float = sin(_reloj * 2.4) * 22.0
	_rayo(cx, cy, margen, 14.0, 30.0, 3.0, Color(Estilo.CREMA, 0.6))
	_rayo(cx, cy, -margen, 14.0, 30.0, 3.0, Color(Estilo.CREMA, 0.6))
	_rayo(cx, cy, -mece, 10.0, 24.0, 2.0, Estilo.CIAN)
	_pal["e"] = Estilo.NARANJA
	_capsula(cx, cy, mece)
	_tecla(cx - 36.0, cy - 4.0, FLECHA_IZQ, mece < -4.0)
	_tecla(cx + 28.0, cy - 4.0, FLECHA_DER, mece > 4.0)
	_tecla(34.0, cy - 4.0, FLECHA_ABA)
	_escribir("X2", 46.0, cy - 2.0, Estilo.DORADO)
	for k in 3:
		_r(38.0, cy + 8.0 + k * 3.0 + fposmod(_reloj * 8.0, 3.0), 1, 2, Estilo.DORADO)
	# una zona de calor de muestra, con su rodeo
	var bx: float = 258.0
	for dy in range(-7, 8):
		var w: int = int(sqrt(49.0 - float(dy * dy)) + sin(_reloj * 7.0 + dy) * 1.0)
		if w > 0:
			_r(bx - w, cy + 4.0 + dy, w * 2 + 1, 1, Estilo.CORAL)
		var w1: int = int(w * 0.55)
		if w1 > 0 and absi(dy) < 5:
			_r(bx - w1, cy + 4.0 + dy, w1 * 2 + 1, 1, Estilo.NARANJA)
	for k in 6:
		var a: float = PI * 0.5 + PI * float(k) / 5.0
		_r(roundf(bx + cos(a) * 12.0), roundf(cy + 4.0 - sin(a) * 12.0 * (1.0 if k < 3 else -1.0) * 0.0 + sin(a) * 0.0 + (k - 2.5) * 5.0), 1, 1, Estilo.CIAN)
	# los seis pasos: tres ya pasaron, tres se juegan
	var teclas: Array = [null, null, null, [FLECHA_IZQ, FLECHA_DER], ["E"], [FLECHA_IZQ, FLECHA_DER]]
	for i in 6:
		var px: float = 35.0 + i * 46.0
		var py: float = 120.0
		var juega: bool = i >= 3
		_r(px, py, 15, 15, Estilo.CIAN if juega else Estilo.TINTA_SUAVE)
		_r(px + 1.0, py + 1.0, 13, 13, _c_hud)
		_sprite(PASOS[i], px + 2.0, py + 2.0, 1, Estilo.CREMA if juega else Estilo.TINTA_SUAVE)
		if i < 5:
			_r(px + 22.0, py + 7.0, 6, 1, Estilo.TINTA_SUAVE)
			_r(px + 26.0, py + 6.0, 1, 3, Estilo.TINTA_SUAVE)
		if not juega:
			_sprite(VISTO, px + 10.0, py + 16.0, 1, Estilo.PAPEL_SOMBRA)
		else:
			var lista: Array = teclas[i]
			var tx: float = px + 7.5 - lista.size() * 5.0
			for dibujo in lista:
				_tecla(tx, py + 18.0, dibujo)
				tx += 10.0
	# cuenta atras: la mision empieza sola, o ya mismo con E
	var queda: float = clampf(1.0 - _t_fase / INTRO_S, 0.0, 1.0)
	_r(20.0, ALTO - 7.0, 245.0, 2, Estilo.TINTA_SUAVE)
	_r(20.0, ALTO - 5.0, floorf(245.0 * queda), 2, Estilo.CREMA)
	_tecla(280.0, ALTO - 15.0, "E", fmod(_reloj, 0.7) < 0.45)


func _dibujar_altimetro() -> void:
	# el camino entero de un vistazo: calor, franja de los paracaidas y mar
	var x: float = 304.0
	_r(x, 26, 3, 94, Color(Estilo.TERRACOTA, 0.6))
	for y in range(28, 118, 6):
		_r(x + 1.0, y, 1, 2, Estilo.CORAL)
	_r(x - 1.0, 120, 5, 12, Estilo.CIAN)
	_r(x, 132, 3, 30, Estilo.PETROLEO.lightened(0.25))
	_r(x - 1.0, 162, 5, 8, _c_mar.lightened(0.15))
	_r(x - 1.0, 162, 5, 1, Estilo.PAPEL)
	_sprite(MINI_ESCUDO, x + 5.0, 64, 1, Estilo.NARANJA)
	_sprite(MINI_TELA, x + 5.0, 142, 1, Estilo.CREMA)
	_sprite(MINI_OLA, x + 5.0, 164, 1, Estilo.PAPEL)
	_escribir("E", x + 6.0, 124, Estilo.CIAN)
	var ym: float = clampf(_y_altimetro(), 26.0, 168.0)
	_sprite(MARCA, x - 6.0, ym - 2.0, 1, Estilo.CREMA)



func _dibujar_marcador() -> void:
	_r(0, 0, CAMPO, HUD, _c_hud)
	_r(0, HUD - 1, CAMPO, 1, Estilo.PETROLEO)
	draw_set_transform(Vector2(4, 2) * PIXEL, 0.0, Vector2(PIXEL, PIXEL))
	_escribir(str(mini(int(puntos), 9999)).pad_zeros(4), 3, 2, Estilo.CREMA, 2)
	# temperatura: un pixel por punto de calor
	var peligro: bool = calor >= 75.0 and fmod(_reloj, 0.5) < 0.3
	_sprite(TERMOMETRO, 40, 2, 1, Estilo.CORAL if peligro else Estilo.PAPEL)
	_r(42, 5 if calor > 50.0 else 8, 1, 6 if calor > 50.0 else 3, Estilo.CORAL)
	_r(47, 3, 102, 8, Estilo.CORAL if peligro else Estilo.PAPEL_SOMBRA)
	_r(48, 4, 100, 6, _c_hud)
	var lleno: Color = Estilo.DORADO
	if calor >= 75.0:
		lleno = Estilo.CORAL
	elif calor >= 50.0:
		lleno = Estilo.NARANJA
	_r(48, 4, floorf(clampf(calor, 0.0, 100.0)), 6, lleno)
	for k in [25, 50, 75]:
		_r(48 + k, 3, 1, 2, _c_hud)
		_r(48 + k, 9, 1, 2, _c_hud)
	# los tres paracaidas: apagados hasta que sirven, huecos cuando se pierden
	for i in 3:
		var tinta: Color = Estilo.TINTA_SUAVE
		if i < paracaidas:
			tinta = Estilo.CREMA if fase >= FRANJA else Estilo.PETROLEO
		elif _t_tela > 0.0 and i == paracaidas and fmod(_t_tela, 0.2) < 0.1:
			tinta = Estilo.CORAL
		if i < paracaidas or _t_tela > 0.0 and i == paracaidas:
			_sprite(ICONO_PARACAIDAS, 176 + i * 10, 3, 1, tinta)
		else:
			_r(178 + i * 10, 9, 3, 1, tinta)
	_sprite(RELOJ, 234, 3, 1, Estilo.PAPEL)
	_escribir(str(mini(int(tiempo), 999)).pad_zeros(3), 245, 2, Estilo.CREMA, 2)
	if fase == REENTRADA and mando_abajo:
		_escribir("X2", 282, 2, Estilo.DORADO, 2)
