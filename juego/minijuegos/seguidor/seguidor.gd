extends "res://nucleo/minijuego.gd"

# El seguidor que tiembla, en version de salon recreativo.
#
# La Luna cruza el cielo y el visor de la camara la persigue con un motor que tiene inercia:
#     v' = EMPUJE * mando - roce * (v - base) + viento          x' = v
# "mando" es la tecla (-1, 0 o 1), "roce" sube con el freno y "base" es 0 o la velocidad del cielo
# (prealimentacion). Quien juega ES el lazo de control: empujar es la ganancia y frenar, la amortiguacion.
# Si empuja de mas, se pasa de la Luna y oscila; si no empuja, el cielo se le escapa.
#
# Mision: tener la Luna dentro del visor hasta llenar la barra REC (60 s de video, comprimidos en 24 s de
# juego). Tres vidas: cada corte de senal (la Luna demasiado tiempo fuera) gasta una. El limite es el amanecer.
#
# Todo se dibuja con _draw() en una rejilla de 320 x 180 pixeles gordos (x4 = 1280 x 720), sin imagenes.
# Coeficientes y umbrales son reglas del juego, no datos de una camara real. El unico dato real es el giro
# aparente del cielo (ficha cielo_15_grados) y las ideas de control de las fichas realimentacion, ganancia,
# amortiguacion y prealimentacion.

const ESCALA := 4
const ANCHO := 320
const ALTO := 180
const PASO := 1.0 / 120.0          # paso fijo de la fisica: el resultado no depende de los fps
const EMPUJE := 80.0               # px/s2 con la tecla a fondo
const ROCE := 1.0                  # 1/s sin freno: el visor sigue deslizando un buen rato
const ROCE_FRENO := 7.0            # 1/s con el freno pulsado
const VIDEO_META := 60.0           # s de video que pide la convocatoria
const VIDEO_RITMO := 2.5           # s de video por cada s de juego con la Luna en el visor
const RADIO := 6                   # radio de la Luna en pixeles del campo
const X_MIN := 6.0
const X_MAX := 314.0
const SUELO_ARCO := 139.0
const ALTO_ARCO := 100.0
const T_MISION := 1.8              # s que se muestra el pictograma de la mision
const T_FINAL := 1.4               # s de celebracion o de corte antes de avisar al anfitrion
const NITIDO := 3.0                # px: la Luna centrada puntua doble

# por dificultad (1, 2, 3)
const T_PASADA := [32.0, 24.0, 19.2]      # s que tarda la Luna en cruzar el cielo
const PASADAS := [3, 4, 5]                # pasadas antes del amanecer (96 s en total)
# D1: margen 13 / deriva 10.625 = 1.22 s por lado (antes 11 / 9.375 = 1.17).
const MEDIO_VISOR := [19, 15, 13]         # medio ancho interior del visor
const FUERZA := [20.0, 30.0, 40.0]        # px/s2 de una racha de viento
const T_CORTE := [5.0, 4.0, 3.0]          # s seguidos sin Luna que cortan la grabacion
const GRACIA := [6.0, 5.0, 4.5]           # s de margen al empezar cada pasada
const PRIMER_VIENTO := [9.0, 6.0, 4.0]
const CALMA := [[6.0, 9.0], [4.5, 7.0], [3.5, 5.5]]
const NUBES := [2, 3, 4]

const C_LUNA_SOMBRA := Color("3b4a52")

const LETRAS := {
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
const ACENTOS := {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ñ": "N"}

const S_LUNITA := [".###.", "#####", "#####", "#####", ".###."]
const S_LUNITA_HUECA := [".###.", "#...#", "#...#", "#...#", ".###."]
const S_PUNTO := [".###.", "#####", "#####", "#####", ".###."]
const S_SOL := ["#.#.#", ".###.", "#####", ".###.", "#.#.#"]
const S_FLECHA := ["#..", "##.", "###", "##.", "#.."]
const S_TRIPODE := ["...#...", "...#...", "..###..", "..#.#..", ".#...#.", ".#...#.", "#.....#"]
const S_CHICA := [".hhh.", "hhhhh", "hpph.", ".ppp.", ".ccc.", "ccccc", "pcccp", ".jjj.", ".j.j.", ".j.j."]
const S_GATO_A := ["#.#...", "###...", "###..#", ".###.#", ".####.", ".#.#.."]
const S_GATO_B := ["#.#...", "###...", "###...", ".###.#", ".#####", ".#.#.."]
const S_MANGA := ["##c##c", "##c##.", "##c..."]

# casas de las Escalinatas: [x, ancho, y del techo]
const TECHOS := [
	[0, 14, 107], [14, 14, 103], [28, 18, 108], [46, 12, 101], [58, 20, 106], [78, 14, 110], [92, 18, 104],
	[110, 62, 112], [172, 14, 105], [186, 22, 109], [208, 12, 100], [220, 18, 106], [238, 16, 103], [254, 26, 108],
]
const VENTANAS := [
	[3, 110], [8, 113], [32, 111], [39, 114], [49, 104], [52, 109], [62, 109], [70, 112], [96, 107], [101, 111],
	[175, 108], [180, 112], [190, 112], [199, 114], [224, 109], [231, 113], [242, 106], [247, 110], [259, 111], [270, 114],
]

var modo_cielo := false         # existe el boton «velocidad del cielo» (parametros.modo == "prealimentacion")
var cielo := false              # el motor ya sigue solo la deriva del cielo
var fase := 0                   # 0 espera, 1 mision, 2 juego, 3 final
var reloj := 0.0                # s jugados (fase 2)
var t_fase := 0.0
var t_dibujo := 0.0
var acumulado := 0.0
var mando := 0.0                # -1, 0 o 1: lo mismo desde las teclas, el raton o el piloto
var freno := false
var visor_x := 160.0
var visor_v := 0.0
var luna_x := -10.0
var pasada := 1
var n_pasadas := 3
var t_pasada := 0.0
var dur_pasada := 32.0
var vel_cielo := 10.625            # px/s: la deriva de la Luna
var medio := 19
var margen := 13.0              # la Luna cuenta como dentro si su centro dista menos que esto
var t_corte := 5.0
var dentro := false
var nitido := false
var video := 0.0                # s de video grabados (0 a 60)
var puntos := 0.0
var vidas := 3
var senal := 1.0                # 1 = senal plena; a 0 se corta la grabacion
var gracia := 0.0
var racha := 0.0                # s seguidos con la Luna dentro
var viento := 0.0               # px/s2 sobre el visor
var viento_dir := 1
var viento_fase := 0            # 0 calma, 1 aviso, 2 racha
var viento_t := 0.0
var viento_dur := 1.5
var viento_prox := 9.0
var rachas_viento := 0

# para explicar la causa al terminar
var t_dentro := 0.0
var t_con_cielo := 0.0
var t_atras := 0.0
var t_delante := 0.0
var rebotes := 0
var cortes := 0
var _ultimo_lado := 0
var _estancia := 0.0
var _gana := false
var _motivo := ""

# piloto: 0 juega la persona, 1 acierta, -1 falla, 2 mando externo (pruebas del modelo)
var _auto := 0
var _pulso := 0.0
var _lado := 1.0

# adornos
var azar := RandomNumberGenerator.new()      # juego (rachas)
var chispa := RandomNumberGenerator.new()    # solo visual
var estrellas: Array[Vector3] = []
var nubes: Array[Dictionary] = []
var particulas: Array[Dictionary] = []
var rayas: Array[Vector3] = []
var sacudida := 0.0
var destello := 0.0
var color_destello := Color.WHITE
var parpadeo_vida := 0.0
var cartel := ""
var cartel_t := 0.0
var brillo_boton := 0.0
var _ox := 0
var _oy := 0


# ------------------------------------------------------------------ contrato

func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var modo: String = str(parametros.get("modo", Juego.args.get("modo", "")))
	modo_cielo = modo == "prealimentacion"
	var i := dificultad - 1
	dur_pasada = T_PASADA[i]
	n_pasadas = PASADAS[i]
	medio = MEDIO_VISOR[i]
	margen = float(medio - RADIO)
	t_corte = T_CORTE[i]
	vel_cielo = 340.0 / dur_pasada
	azar.seed = 7919 * dificultad + (13 if modo_cielo else 0)
	chispa.seed = 4242
	for n in 64:
		estrellas.append(Vector3(chispa.randf_range(0.0, 340.0), chispa.randf_range(21.0, 136.0), float(chispa.randi_range(0, 3))))
	var cuantas: int = NUBES[i]
	for n in cuantas:
		nubes.append(_nueva_nube(chispa.randf_range(30.0, 300.0)))
	queue_redraw()


func _empezar() -> void:
	if _solo == 0 and not Juego.modo_prueba:
		azar.randomize()
	var i := dificultad - 1
	fase = 1
	t_fase = 0.0
	viento_prox = PRIMER_VIENTO[i]
	gracia = GRACIA[i]
	sonar("pulsar")


func _paso(delta: float) -> void:
	t_dibujo += delta
	_animar(delta)
	match fase:
		1:
			t_fase += delta
			if t_fase >= T_MISION:
				fase = 2
				sonar("salto")
		2:
			if _auto == 0:
				_leer_mandos()
			acumulado = minf(acumulado + delta, 1.0)
			while acumulado >= PASO and fase == 2:
				acumulado -= PASO
				_avanzar()
		3:
			t_fase += delta
			if t_fase >= T_FINAL:
				_cerrar()
	queue_redraw()


func jugar_solo(acierta: bool) -> void:
	# el piloto no toca el visor: decide "mando", "freno" y el boton del cielo, igual que las teclas
	_auto = 1 if acierta else -1


# ------------------------------------------------------------------ mandos

func _leer_mandos() -> void:
	mando = eje_x()
	freno = Input.is_action_pressed("saltar") or (not modo_cielo and Input.is_action_pressed("interactuar"))
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		# raton (opcional): mantener el boton empuja el motor hacia el puntero
		var p: Vector2 = get_local_mouse_position() / float(ESCALA)
		if p.x >= 0.0 and p.x <= float(ANCHO) and p.y >= 15.0 and p.y <= 166.0 and absf(p.x - visor_x) > 3.0:
			mando = signf(p.x - visor_x)
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		freno = true


func _input(evento: InputEvent) -> void:
	if not activo or fase != 2 or _auto != 0 or not modo_cielo:
		return
	if evento.is_action_pressed("interactuar"):
		_pulsar_cielo()
		get_viewport().set_input_as_handled()


func _gui_input(evento: InputEvent) -> void:
	if not activo or fase != 2 or _auto != 0 or not modo_cielo:
		return
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		var p: Vector2 = evento.position / float(ESCALA)
		if Rect2(96, 167, 60, 12).has_point(p):
			_pulsar_cielo()
			accept_event()


func _pulsar_cielo() -> void:
	# el boton «velocidad del cielo»: el motor ya gira al ritmo del cielo y solo queda corregir
	cielo = not cielo
	brillo_boton = 0.6
	sonar("recoger" if cielo else "pulsar")
	if cielo:
		_chispas(125.0, 172.0, 10, Estilo.CIAN, 26.0)
		_poner_cartel("MOTOR AL RITMO DEL CIELO", 1.5)


func _piloto() -> void:
	var e := luna_x - visor_x
	var sobra := visor_v - vel_cielo
	if _auto > 0:
		if modo_cielo and not cielo and reloj > 0.4:
			_pulsar_cielo()
		# acerca el visor y frena antes de llegar: la orden mira el error y tambien la velocidad
		var orden := 6.0 * e - 3.5 * sobra
		mando = 0.0 if absf(orden) < 8.0 else signf(orden)
		var base := vel_cielo if cielo else 0.0
		freno = absf(sobra) > 20.0 and (visor_v - base) * sobra > 0.0 and absf(e) < 0.45 * absf(sobra) + 4.0
	elif _auto < 0:
		# empuja a fondo hacia la Luna y no suelta ni frena: se pasa de largo y oscila
		_pulso -= PASO
		if _pulso <= 0.0:
			_pulso = 1.3
			_lado = 1.0 if e >= 0.0 else -1.0
		mando = _lado
		freno = false


# ------------------------------------------------------------------ fisica y reglas

func _arco(x: float) -> float:
	# la senda de la Luna (y del visor, que va montado sobre ella)
	return SUELO_ARCO - ALTO_ARCO * sin(PI * clampf((x + 10.0) / 340.0, 0.0, 1.0))


func _avanzar() -> void:
	if _auto == 1 or _auto == -1:
		_piloto()
	reloj += PASO
	t_pasada += PASO
	if t_pasada >= dur_pasada:
		if pasada >= n_pasadas:
			_acabar(false, "amanece")
			return
		pasada += 1
		t_pasada = 0.0
		var g: float = GRACIA[dificultad - 1]
		gracia = maxf(gracia, g)
		_poner_cartel("PASADA %d" % pasada, 1.4)
		sonar("salto")
	luna_x = -10.0 + 340.0 * t_pasada / dur_pasada
	_soplar()
	var base := vel_cielo if cielo else 0.0
	var roce := ROCE_FRENO if freno else ROCE
	visor_v += (EMPUJE * mando - roce * (visor_v - base) + viento) * PASO
	visor_x += visor_v * PASO
	if visor_x < X_MIN:
		visor_x = X_MIN
		visor_v = maxf(visor_v, 0.0)
	elif visor_x > X_MAX:
		visor_x = X_MAX
		visor_v = minf(visor_v, 0.0)
	var e := luna_x - visor_x
	var antes := dentro
	dentro = absf(e) <= margen
	nitido = absf(e) <= NITIDO
	var a_la_vista := luna_x >= 8.0 and luna_x <= 312.0
	gracia = maxf(0.0, gracia - PASO)
	if dentro:
		if not antes:
			sonar("recoger")
			_chispas(luna_x, _arco(luna_x), 6, Estilo.BRILLO, 22.0)
		racha += PASO
		_estancia += PASO
		t_dentro += PASO
		if cielo:
			t_con_cielo += PASO
		var tramo := int(video / 4.0)
		video = minf(VIDEO_META, video + VIDEO_RITMO * PASO)
		puntos += VIDEO_RITMO * PASO * 10.0 * float(_multiplicador()) * (2.0 if nitido else 1.0)
		senal = minf(1.0, senal + PASO / (t_corte * 0.5))
		if int(video / 4.0) != tramo:
			sonar("tic")
			_chispas(72.0 + video * 1.5, 7.0, 4, Estilo.DORADO, 14.0)
		if video >= VIDEO_META:
			_acabar(true, "")
			return
	else:
		racha = 0.0
		var lado := 1 if e > 0.0 else -1
		if _ultimo_lado != 0 and lado != _ultimo_lado and _estancia < 1.0 and a_la_vista:
			rebotes += 1          # cruzo la Luna de lado a lado sin quedarse: se paso
		_ultimo_lado = lado
		_estancia = 0.0
		if a_la_vista and gracia <= 0.0:
			senal -= PASO / t_corte
			if e > 0.0:
				t_atras += PASO
			else:
				t_delante += PASO
			if senal <= 0.0:
				_cortar()


func _multiplicador() -> int:
	return 1 + mini(3, int(racha / 4.0))


func _soplar() -> void:
	match viento_fase:
		0:
			viento = 0.0
			if reloj >= viento_prox:
				viento_fase = 1
				viento_t = 0.0
				viento_dir = 1 if azar.randf() < 0.5 else -1
				viento_dur = azar.randf_range(1.2, 2.0)
				sonar("radio")
		1:
			viento_t += PASO
			if viento_t >= 0.8:
				viento_fase = 2
				viento_t = 0.0
				rachas_viento += 1
				sacudida = maxf(sacudida, 0.15)
		2:
			viento_t += PASO
			var k := viento_t / viento_dur
			var forma := minf(1.0, minf(k, 1.0 - k) * 5.0)
			var f: float = FUERZA[dificultad - 1]
			viento = float(viento_dir) * f * (1.0 + 0.12 * float(pasada - 1)) * forma
			if k >= 1.0:
				viento_fase = 0
				viento = 0.0
				var calma: Array = CALMA[dificultad - 1]
				var c0: float = calma[0]
				var c1: float = calma[1]
				viento_prox = reloj + azar.randf_range(c0, c1)


func _cortar() -> void:
	vidas -= 1
	cortes += 1
	senal = 1.0
	gracia = 2.5
	sacudida = 0.4
	destello = 0.5
	color_destello = Estilo.CORAL
	parpadeo_vida = 1.2
	sonar("error")
	_chispas(visor_x, _arco(visor_x), 14, Estilo.CORAL, 40.0)
	if vidas <= 0:
		_acabar(false, "cortes")
	else:
		_poner_cartel("CORTE", 1.0)


func _acabar(gana: bool, motivo: String) -> void:
	fase = 3
	t_fase = 0.0
	_gana = gana
	_motivo = motivo
	mando = 0.0
	freno = false
	viento = 0.0
	if gana:
		puntos += float(vidas) * 200.0 + maxf(0.0, _tiempo_total() - reloj) * 5.0
		_poner_cartel("VIDEO COMPLETO", T_FINAL)
		destello = 0.5
		color_destello = Estilo.BRILLO
		sonar("logro")
		for n in 5:
			_chispas(chispa.randf_range(40.0, 240.0), chispa.randf_range(30.0, 80.0), 12, [Estilo.DORADO, Estilo.CIAN, Estilo.CORAL][n % 3], 46.0)
	else:
		_poner_cartel("AMANECE" if motivo == "amanece" else "SIN SEÑAL", T_FINAL)


func _tiempo_total() -> float:
	return dur_pasada * float(n_pasadas)


func _cerrar() -> void:
	var grabado := int(video)
	if _gana:
		var frase := "Grabaste los 60 s: mides dónde está la Luna y corriges el motor. Empujar acelera; frenar calma."
		if modo_cielo and cielo:
			Juego.anotar("prealimentacion")
			frase = "El cielo gira unos 15° por hora: con ese dato en el motor, solo corregiste el viento."
		elif modo_cielo:
			frase = "Grabaste los 60 s a pulso. Con E, el motor copia el giro del cielo y solo queda corregir."
		terminar(true, roundf(puntos), frase)
		return
	var causa := "El motor se quedó atrás: el cielo no para de girar y hay que seguir empujando."
	if rebotes >= 3 or t_delante > t_atras:
		causa = "El motor se pasó de la Luna y osciló: empujaste más de lo que frenaste."
	elif modo_cielo and t_con_cielo < 3.0:
		causa = "Sin la velocidad del cielo (E), el motor no anticipa el giro y se queda atrás."
	if _motivo == "amanece":
		terminar(false, roundf(puntos), "Amaneció con %d de 60 s grabados. %s" % [grabado, causa])
	else:
		terminar(false, roundf(puntos), "%s Grabaste %d de 60 s." % [causa, grabado])


# ------------------------------------------------------------------ adornos (no cambian las reglas)

func _poner_cartel(mensaje: String, segundos: float) -> void:
	cartel = mensaje
	cartel_t = segundos


func _chispas(x: float, y: float, cuantas: int, color: Color, fuerza: float) -> void:
	for n in cuantas:
		if particulas.size() > 90:
			return
		var angulo := chispa.randf_range(0.0, TAU)
		var rapidez := chispa.randf_range(0.3, 1.0) * fuerza
		particulas.append({"x": x, "y": y, "vx": cos(angulo) * rapidez, "vy": sin(angulo) * rapidez - 8.0, "vida": chispa.randf_range(0.35, 0.8), "color": color})


func _nueva_nube(x: float) -> Dictionary:
	var ancho := chispa.randi_range(26, 44)
	var alto := chispa.randi_range(6, 9)
	var filas: Array[Vector2i] = []
	var joroba := chispa.randf_range(0.25, 0.55)
	for r in alto:
		var t := float(r) / float(alto - 1)
		var izq := int(float(ancho) * 0.30 * pow(1.0 - t, 1.6))
		var der := ancho - int(float(ancho) * 0.24 * pow(1.0 - t, 1.6))
		if r < 2:
			izq = int(float(ancho) * joroba)
			der = izq + int(float(ancho) * 0.28) + r * 3
		filas.append(Vector2i(izq, mini(der, ancho)))
	return {"x": x, "y": chispa.randf_range(40.0, 118.0), "v": chispa.randf_range(5.0, 11.0), "ancho": ancho, "filas": filas}


func _animar(delta: float) -> void:
	sacudida = maxf(0.0, sacudida - delta)
	destello = maxf(0.0, destello - delta)
	parpadeo_vida = maxf(0.0, parpadeo_vida - delta)
	cartel_t = maxf(0.0, cartel_t - delta)
	brillo_boton = maxf(0.0, brillo_boton - delta)
	if fase < 2:
		return
	for nube in nubes:
		var x: float = nube["x"]
		var v: float = nube["v"]
		var ancho: int = nube["ancho"]
		x += (-v + viento * 0.5) * delta
		if x < -float(ancho) - 6.0:
			x = float(ANCHO) + chispa.randf_range(4.0, 40.0)
			nube["y"] = chispa.randf_range(40.0, 118.0)
		elif x > float(ANCHO) + 46.0:
			x = -float(ancho) - 4.0
		nube["x"] = x
	var vivas: Array[Dictionary] = []
	for p in particulas:
		var vida: float = p["vida"]
		vida -= delta
		if vida <= 0.0:
			continue
		var vy: float = p["vy"]
		vy += 60.0 * delta
		var px: float = p["x"]
		var py: float = p["y"]
		var vx: float = p["vx"]
		p["x"] = px + vx * delta
		p["y"] = py + vy * delta
		p["vy"] = vy
		p["vida"] = vida
		vivas.append(p)
	particulas = vivas
	# rayas de viento: x, y, largo
	var intensidad := absf(viento) / 20.0
	if viento_fase == 2 and rayas.size() < 26 and chispa.randf() < intensidad * delta * 30.0:
		var x0 := -8.0 if viento_dir > 0 else float(ANCHO) + 8.0
		rayas.append(Vector3(x0, chispa.randf_range(22.0, 140.0), chispa.randf_range(4.0, 9.0)))
	var quedan: Array[Vector3] = []
	for r in rayas:
		r.x += float(viento_dir) * 170.0 * delta
		if r.x > -12.0 and r.x < float(ANCHO) + 12.0:
			quedan.append(r)
	rayas = quedan


# ------------------------------------------------------------------ dibujo en pixeles gordos

func _px(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2((roundf(x) + float(_ox)) * ESCALA, (roundf(y) + float(_oy)) * ESCALA, w * ESCALA, h * ESCALA), color)


func _sprite(filas: Array, x: float, y: float, colores: Dictionary, espejo: bool = false) -> void:
	for j in filas.size():
		var fila: String = filas[j]
		var n := fila.length()
		var i := 0
		while i < n:
			var c := fila[i]
			if c == ".":
				i += 1
				continue
			var k := i
			while k + 1 < n and fila[k + 1] == c:
				k += 1
			var color: Color = colores.get(c, Estilo.CREMA)
			var col := (n - 1 - k) if espejo else i
			_px(x + float(col), y + float(j), float(k - i + 1), 1.0, color)
			i = k + 1


func _ancho_texto(s: String, esc: int = 1) -> int:
	var total := 0
	for i in s.length():
		var letra := s[i]
		var base: String = ACENTOS.get(letra, letra)
		var filas: Array = LETRAS.get(base, LETRAS["?"])
		var primera: String = filas[0]
		total += (primera.length() + 1) * esc
	return maxi(0, total - esc)


func _escribir(s: String, x: float, y: float, color: Color, esc: int = 1) -> void:
	var cx := roundf(x)
	for i in s.length():
		var letra := s[i]
		var base: String = ACENTOS.get(letra, letra)
		var filas: Array = LETRAS.get(base, LETRAS["?"])
		var primera: String = filas[0]
		var ancho := primera.length()
		for j in filas.size():
			var fila: String = filas[j]
			var a := 0
			while a < ancho:
				if fila[a] != "#":
					a += 1
					continue
				var b := a
				while b + 1 < ancho and fila[b + 1] == "#":
					b += 1
				_px(cx + float(a * esc), y + float(j * esc), float((b - a + 1) * esc), float(esc), color)
				a = b + 1
		if base != letra:
			if letra == "Ñ":
				_px(cx + float(esc), y - float(2 * esc), float(2 * esc), float(esc), color)
			else:
				_px(cx + float(esc), y - float(2 * esc), float(2 * esc), float(esc), color)
		cx += float((ancho + 1) * esc)


func _centrado(s: String, cx: float, y: float, color: Color, esc: int = 1) -> void:
	_escribir(s, cx - float(_ancho_texto(s, esc)) * 0.5, y, color, esc)


func _draw() -> void:
	_ox = 0
	_oy = 0
	draw_rect(Rect2(Vector2.ZERO, size), Estilo.NOCHE)
	if sacudida > 0.0:
		_ox = chispa.randi_range(-1, 1)
		_oy = chispa.randi_range(-1, 1)
	_dibujar_cielo()
	_dibujar_luna()
	_dibujar_nubes()
	for r in rayas:
		_px(r.x, r.y, r.z, 1.0, Color(Estilo.BRILLO, 0.75))
	_dibujar_barrio()
	_dibujar_visor()
	for p in particulas:
		var px: float = p["x"]
		var py: float = p["y"]
		var color: Color = p["color"]
		_px(px, py, 1.0, 1.0, color)
	_ox = 0
	_oy = 0
	_dibujar_marcador()
	_dibujar_leyenda()
	if fase <= 1:
		_dibujar_mision()
	elif cartel_t > 0.0 and cartel != "":
		var ancho := _ancho_texto(cartel, 2)
		_px(160.0 - float(ancho) * 0.5 - 4.0, 22.0, float(ancho) + 8.0, 16.0, Color(Estilo.TINTA, 0.9))
		_centrado(cartel, 160.0, 25.0, Estilo.DORADO if _gana or fase == 2 and cartel != "CORTE" else Estilo.CORAL, 2)
	if destello > 0.0:
		draw_rect(Rect2(Vector2.ZERO, size), Color(color_destello, 0.4 * destello / 0.5))


func _dibujar_cielo() -> void:
	var amanecer := clampf((reloj - (_tiempo_total() - 15.0)) / 15.0, 0.0, 1.0)
	var c0: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.25 * amanecer)
	var c1: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.16 + 0.3 * amanecer)
	var c2: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.34 + 0.2 * amanecer).lerp(Estilo.CORAL, 0.28 * amanecer)
	var c3: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.55).lerp(Estilo.NARANJA, 0.6 * amanecer)
	_px(0, 0, ANCHO, 61, c0)
	_px(0, 61, ANCHO, 34, c1)
	_px(0, 95, ANCHO, 34, c2)
	_px(0, 129, ANCHO, 51, c3)
	var n := 0
	while n < ANCHO:
		_px(n, 60, 2, 1, c1)
		_px(n + 2, 94, 2, 1, c2)
		_px(n, 128, 2, 1, c3)
		n += 4
	# estrellas: giran con el cielo, a la misma velocidad que la Luna
	var corrimiento := vel_cielo * reloj
	for i in estrellas.size():
		var e: Vector3 = estrellas[i]
		var x := fposmod(e.x + corrimiento, 340.0) - 10.0
		var guino := int(t_dibujo * 1.5 + float(i) * 0.7) % 6 == 0
		var color: Color = [Estilo.BRILLO, Estilo.CREMA, Estilo.PETROLEO.lightened(0.25), Estilo.PAPEL][int(e.z)]
		if guino or amanecer > 0.6:
			color = Estilo.PETROLEO.lightened(0.1)
		_px(x, e.y, 1, 1, color)
		if int(e.z) == 0 and not guino and amanecer < 0.5:
			_px(x - 1.0, e.y, 3, 1, Color(Estilo.BRILLO, 0.35))
			_px(x, e.y - 1.0, 1, 3, Color(Estilo.BRILLO, 0.35))
	# la senda de la Luna: puntos que tambien giran con el cielo
	for k in 34:
		var x := fposmod(float(k) * 10.0 + corrimiento, 340.0) - 10.0
		_px(x, _arco(x), 1, 1, Color(Estilo.PETROLEO.lightened(0.2), 0.8))


func _dibujar_luna() -> void:
	if fase < 2:
		return
	var cx := roundf(luna_x)
	var cy := roundf(_arco(luna_x))
	var r2 := (float(RADIO) + 0.5) * (float(RADIO) + 0.5)
	var corrida := 4.0 + 2.5 * float(pasada - 1)       # cada pasada, la Luna crece un poco
	for dy in range(-RADIO, RADIO + 1):
		var medio_ancho := int(sqrt(r2 - float(dy * dy)))
		_px(cx - float(medio_ancho), cy + float(dy), float(2 * medio_ancho + 1), 1, C_LUNA_SOMBRA)
		# parte iluminada: el borde de abajo, la «Luna sonriente» del ecuador
		var resto := r2 - (float(dy) + corrida) * (float(dy) + corrida)
		if resto <= 0.0:
			_px(cx - float(medio_ancho), cy + float(dy), float(2 * medio_ancho + 1), 1, Estilo.CREMA)
		else:
			var hueco := int(sqrt(resto))
			if hueco < medio_ancho:
				_px(cx - float(medio_ancho), cy + float(dy), float(medio_ancho - hueco), 1, Estilo.CREMA)
				_px(cx + float(hueco) + 1.0, cy + float(dy), float(medio_ancho - hueco), 1, Estilo.CREMA)
	_px(cx - 2.0, cy + 3.0, 2, 1, Estilo.PAPEL_SOMBRA)
	_px(cx + 2.0, cy + 4.0, 1, 1, Estilo.PAPEL_SOMBRA)
	if dentro and fase == 2:
		# destellos de grabacion alrededor de la Luna
		var giro := int(t_dibujo * 6.0) % 2
		for k in 4:
			var angulo := float(k) * PI * 0.5 + float(giro) * PI * 0.25
			_px(cx + roundf(cos(angulo) * 9.0), cy + roundf(sin(angulo) * 9.0), 1, 1, Estilo.DORADO if nitido else Estilo.BRILLO)


func _dibujar_nubes() -> void:
	var arriba: Color = Estilo.PETROLEO.lerp(Estilo.PAPEL, 0.35)
	var abajo: Color = Estilo.PETROLEO.lerp(Estilo.NOCHE, 0.15)
	for nube in nubes:
		var x: float = nube["x"]
		var y: float = nube["y"]
		var filas: Array[Vector2i] = nube["filas"]
		for r in filas.size():
			# nubes a rayas: dejan entrever la Luna; con mas dificultad se cierran
			if dificultad == 1 and r % 2 == 1:
				continue
			if dificultad == 2 and r % 3 == 2:
				continue
			var fila: Vector2i = filas[r]
			_px(x + float(fila.x), y + float(r), float(fila.y - fila.x), 1, arriba if r < 3 else abajo)


func _dibujar_barrio() -> void:
	_oy += 40
	var oscuro: Color = Estilo.TINTA
	var claro: Color = Estilo.TINTA.lightened(0.07)
	# faro del cerro
	_px(19, 91, 5, 12, claro)
	_px(18, 88, 7, 3, oscuro)
	_px(20, 86, 3, 2, oscuro)
	var luz_faro := int(t_dibujo * 0.8) % 2 == 0
	_px(20, 89, 3, 1, Estilo.DORADO if luz_faro else Estilo.TERRACOTA)
	if luz_faro:
		_px(25, 89, 4, 1, Color(Estilo.DORADO, 0.5))
	for i in TECHOS.size():
		var t: Array = TECHOS[i]
		var x: int = int(float(t[0]) * 320.0 / 280.0)
		var w: int = int(ceil(float(t[1]) * 320.0 / 280.0))
		var y: int = t[2]
		_px(x, y, w, ALTO - y - 40, oscuro if i % 2 == 0 else claro)
		_px(x, y, w, 1, Estilo.TINTA_SUAVE)
	for i in VENTANAS.size():
		var v: Array = VENTANAS[i]
		var vx: int = int(float(v[0]) * 320.0 / 280.0)
		var vy: int = v[1]
		var encendida := int(t_dibujo * 0.3 + float(i) * 1.7) % 7 != 0
		_px(vx, vy, 1, 2, (Estilo.DORADO if i % 3 else Estilo.NARANJA) if encendida else Estilo.TINTA_SUAVE)
	# manga de viento en una azotea
	_px(213, 90, 1, 10, Estilo.TINTA_SUAVE)
	if viento_fase == 0:
		_px(214, 91, 2, 1, Estilo.CORAL)
		_px(215, 92, 1, 4, Estilo.CORAL)
		_px(215, 94, 1, 1, Estilo.CREMA)
	else:
		_sprite(S_MANGA, 214.0 if viento_dir > 0 else 207.0, 90.0, {"#": Estilo.CORAL, "c": Estilo.CREMA}, viento_dir < 0)
	# la azotea con el seguidor, la protagonista y el gato
	_sprite(S_CHICA, 146, 102, {"h": Estilo.TERRACOTA, "p": Estilo.CREMA, "c": Estilo.DORADO, "j": Estilo.PETROLEO.lightened(0.3)})
	var cola := int(t_dibujo * 2.0) % 2 == 0
	_sprite(S_GATO_A if cola else S_GATO_B, 169, 106, {"#": Estilo.NARANJA})
	var tiembla := 0.0
	if fase == 2 and absf(visor_v - vel_cielo) > 35.0 and int(t_dibujo * 12.0) % 2 == 0:
		tiembla = 1.0          # el seguidor tiembla cuando el motor va muy forzado
	_sprite(S_TRIPODE, 157.0 + tiembla, 105, {"#": Estilo.PAPEL_SOMBRA})
	# el tubo de la camara apunta al visor
	var pivote := Vector2(160.0 + tiembla, 104.0)
	var meta_v := Vector2(visor_x, _arco(visor_x) - 40.0)
	var hacia := (meta_v - pivote).normalized()
	for k in 5:
		var q := pivote + hacia * float(k) * 2.0
		_px(q.x - 1.0, q.y - 1.0, 2, 2, Estilo.CREMA if k < 4 else Estilo.CIAN)
	if cielo:
		# engranaje encendido: el motor gira solo al ritmo del cielo
		var diente := int(t_dibujo * 5.0) % 2
		_px(159.0 + float(diente), 108.0, 1, 1, Estilo.CIAN)
		_px(160.0 - float(diente), 109.0, 1, 1, Estilo.CIAN)
	if fase >= 2:
		var largo := pivote.distance_to(meta_v)
		var d := 14.0 + fposmod(t_dibujo * 10.0, 7.0)
		while d < largo - 12.0:
			var q := pivote + hacia * d
			_px(q.x, q.y, 1, 1, Color(Estilo.CIAN_MEDIO, 0.7))
			d += 7.0
	_oy -= 40


func _dibujar_visor() -> void:
	var cx := roundf(visor_x)
	var cy := roundf(_arco(visor_x))
	if fase == 2 and absf(visor_v - vel_cielo) > 45.0 and int(t_dibujo * 14.0) % 2 == 0:
		cx += 1.0
	var color: Color = Estilo.CIAN
	if dentro and fase == 2:
		color = Estilo.BRILLO
	elif fase == 2 and gracia <= 0.0 and senal < 0.4 and int(t_dibujo * 3.0) % 2 == 0:
		color = Estilo.CORAL
	var m := float(medio)
	var alto := 10.0
	var brazo := 4.0
	# cuatro esquinas
	for sx in [-1.0, 1.0]:
		for sy in [-1.0, 1.0]:
			var ex: float = cx + sx * m
			var ey: float = cy + sy * alto
			_px(minf(ex, ex - sx * (brazo - 1.0)), ey, brazo, 1, color)
			_px(ex, minf(ey, ey - sy * (brazo - 1.0)), 1, brazo, color)
	# marcas de centro
	_px(cx, cy - alto, 1, 2, color)
	_px(cx, cy + alto - 1.0, 1, 2, color)
	if dentro and fase == 2:
		# enganchado: el visor se cierra con dos marcas laterales (no depende solo del color)
		_px(cx - m, cy, 2, 1, color)
		_px(cx + m - 1.0, cy, 2, 1, color)
		var mult := _multiplicador()
		if mult > 1:
			_escribir("x%d" % mult, cx + m + 3.0, cy - alto, Estilo.DORADO)
	# barra de senal bajo el visor: se vacia mientras la Luna esta fuera
	if fase == 2 and senal < 0.995:
		var ancho := m * 2.0 + 1.0
		_px(cx - m, cy + alto + 3.0, ancho, 2, Estilo.TINTA)
		var lleno := maxf(0.0, roundf(ancho * senal))
		var c_senal: Color = Estilo.DORADO if senal > 0.4 else Estilo.CORAL
		_px(cx - m, cy + alto + 3.0, lleno, 2, c_senal)
	# empuje del motor: una flecha del lado hacia el que acelera
	if fase == 2 and mando != 0.0:
		_sprite(S_FLECHA, cx + (m + 3.0 if mando > 0.0 else -m - 5.0), cy - 2.0, {"#": Estilo.CIAN}, mando < 0.0)
	if fase == 2 and freno:
		_px(cx - 3.0, cy + alto + 1.0, 7, 1, Estilo.NARANJA)


func _dibujar_marcador() -> void:
	_oy = 2
	_px(0, 0, ANCHO, 14, Estilo.TINTA)
	_px(0, 14, ANCHO, 1, Estilo.PETROLEO)
	_escribir("%05d" % int(puntos), 4, 2, Estilo.CREMA, 2)
	var graba := dentro and fase == 2
	var luz: Color = Estilo.TINTA_SUAVE
	if graba and fmod(t_dibujo, 0.9) < 0.55:
		luz = Estilo.CORAL
	_sprite(S_PUNTO, 50, 5, {"#": luz})
	_escribir("REC", 57, 5, Estilo.CREMA if graba else Estilo.TINTA_SUAVE)
	# barra de grabacion: 30 tramos de 2 s de video
	_px(70, 2, 93, 1, Estilo.CREMA)
	_px(70, 11, 93, 1, Estilo.CREMA)
	_px(70, 2, 1, 10, Estilo.CREMA)
	_px(162, 2, 1, 10, Estilo.CREMA)
	var llenos := int(video / 2.0)
	for s in 30:
		var color: Color = Estilo.NOCHE
		if s < llenos:
			color = Estilo.DORADO if s % 5 == 4 else Estilo.CORAL
			if s == llenos - 1 and graba and int(t_dibujo * 4.0) % 2 == 0:
				color = Estilo.BRILLO
		_px(72 + s * 3, 4, 2, 6, color)
	_escribir("%02d" % int(video), 167, 2, Estilo.CREMA, 2)
	_escribir("/60", 183, 7, Estilo.PAPEL_SOMBRA)
	# vidas: tres lunas
	for v in 3:
		var viva := v < vidas
		if not viva and v == vidas and parpadeo_vida > 0.0 and int(parpadeo_vida * 6.0) % 2 == 0:
			_sprite(S_LUNITA, 242 + v * 7, 5, {"#": Estilo.CORAL})
		else:
			_sprite(S_LUNITA if viva else S_LUNITA_HUECA, 242 + v * 7, 5, {"#": Estilo.CREMA if viva else Estilo.TINTA_SUAVE})
	# tiempo hasta el amanecer
	var queda := int(ceil(maxf(0.0, _tiempo_total() - reloj)))
	var apuro := queda <= 15 and fase == 2
	_sprite(S_SOL, 285, 5, {"#": Estilo.NARANJA if apuro else Estilo.DORADO})
	_escribir("%02d" % mini(queda, 99), 294, 2, Estilo.CORAL if apuro and int(t_dibujo * 2.0) % 2 == 0 else Estilo.CREMA, 2)
	# aviso de viento, bajo el marcador
	if viento_fase > 0 and fase == 2:
		if viento_fase == 2 or int(t_dibujo * 5.0) % 2 == 0:
			var flechas := ">>>" if viento_dir > 0 else "<<<"
			_centrado("%s VIENTO %s" % [flechas, flechas], 160, 19, Estilo.BRILLO)
	_oy = 0


func _tecla_dibujada(rotulo: String, x: float, y: float, encendida: bool, color: Color) -> float:
	# una tecla en pictograma; devuelve su ancho
	var ancho := float(_ancho_texto(rotulo) + 4)
	_px(x, y, ancho, 9, color if encendida else Estilo.TINTA_SUAVE)
	_px(x + 1.0, y + 1.0, ancho - 2.0, 7, Estilo.TINTA if not encendida else color)
	_escribir(rotulo, x + 2.0, y + 2.0, Estilo.TINTA if encendida else Estilo.CREMA)
	return ancho


func _dibujar_leyenda() -> void:
	# leyenda de mandos en pictogramas, sobre las casas
	var y := 167.0
	var izq := fase == 2 and mando < 0.0
	var der := fase == 2 and mando > 0.0
	_sprite(S_FLECHA, 4, y + 2.0, {"#": Estilo.CIAN if izq else Estilo.CREMA}, true)
	_sprite(S_FLECHA, 9, y + 2.0, {"#": Estilo.CIAN if der else Estilo.CREMA})
	_escribir("MOTOR", 15, y + 2.0, Estilo.CIAN if izq or der else Estilo.PAPEL_SOMBRA)
	var frenando := fase == 2 and freno
	var w := _tecla_dibujada("ESP", 45, y, frenando, Estilo.NARANJA)
	_escribir("FRENO", 47.0 + w, y + 2.0, Estilo.NARANJA if frenando else Estilo.PAPEL_SOMBRA)
	if modo_cielo:
		var llama := not cielo and int(t_dibujo * 2.0) % 2 == 0
		var w2 := _tecla_dibujada("E", 98, y, cielo or llama or brillo_boton > 0.0, Estilo.CIAN)
		_escribir("CIELO", 100.0 + w2, y + 2.0, Estilo.CIAN if cielo else Estilo.PAPEL_SOMBRA)
		# estrellita que avanza: el motor copia el giro del cielo
		var avance := fposmod(t_dibujo * 4.0, 6.0) if cielo else 0.0
		_px(129.0 + avance, y + 4.0, 1, 1, Estilo.BRILLO if cielo else Estilo.TINTA_SUAVE)

	_tecla_dibujada("ESC", 292, y, false, Estilo.CREMA)


func _dibujar_mision() -> void:
	_ox = 20
	_oy = 20
	# la mision, en un pictograma y una linea
	_px(54, 34, 172, 52, Estilo.CREMA)
	_px(55, 35, 170, 50, Estilo.TINTA)
	var cx := 140.0
	var cy := 53.0
	# visor con la Luna dentro
	for sx in [-1.0, 1.0]:
		for sy in [-1.0, 1.0]:
			var ex: float = cx + sx * 13.0
			var ey: float = cy + sy * 9.0
			_px(minf(ex, ex - sx * 3.0), ey, 4, 1, Estilo.CIAN)
			_px(ex, minf(ey, ey - sy * 3.0), 1, 4, Estilo.CIAN)
	for dy in range(-5, 6):
		var medio_ancho := int(sqrt(30.25 - float(dy * dy)))
		_px(cx - float(medio_ancho), cy + float(dy), float(2 * medio_ancho + 1), 1, C_LUNA_SOMBRA if dy < 1 else Estilo.CREMA)
	var pulso := int(t_dibujo * 2.5) % 2 == 0
	# teclas a los lados
	_tecla_dibujada("<", 96, 49, pulso and fase == 1, Estilo.CIAN)
	_tecla_dibujada(">", 177, 49, not pulso and fase == 1, Estilo.CIAN)
	if modo_cielo:
		_tecla_dibujada("E", 66, 49, pulso, Estilo.CIAN)
		_centrado("PULSA E: EL MOTOR SIGUE AL CIELO", cx, 72, Estilo.CREMA)
	else:
		_centrado("MANTÉN LA LUNA EN EL VISOR", cx, 72, Estilo.CREMA)
	# la barra que hay que llenar
	_px(206, 48, 12, 1, Estilo.CREMA)
	_px(206, 58, 12, 1, Estilo.CREMA)
	_px(206, 48, 1, 11, Estilo.CREMA)
	_px(217, 48, 1, 11, Estilo.CREMA)
	var sube := int(fposmod(t_dibujo * 4.0, 5.0))
	for s in 4:
		_px(208, 56 - s * 2, 8, 1, Estilo.CORAL if s <= sube else Estilo.NOCHE)
	_ox = 0
	_oy = 0
