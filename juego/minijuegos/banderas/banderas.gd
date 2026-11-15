extends "res://nucleo/minijuego.gd"

# BANDERAS · «Dos banderas, un cielo». Juego de salon recreativo en tres fases y un amanecer:
#   0 HINCAR    caminar hasta cada mastil y golpear (E) cuando la marca del compas cruza el centro
#   1 EXTENDER  mantener E para sacar la barra horizontal y soltar con la punta dentro del tope
#   2 IGUALAR   subir y bajar el tramo alto de cada mastil hasta que las dos telas queden a la misma altura
#   3 AMANECE   sale el sol sobre las dos banderas y termina la partida
#
# Campo logico de 320 x 180 pixeles, escalado x4 al lienzo de 1280 x 720. Todo se dibuja con rectangulos
# enteros en _draw(): sprites con mapas de caracteres y letras de 3 x 5. No hay imagenes externas.
#
# Respeto: las banderas de Estados Unidos y de Ecuador nunca caen, no se danan y no tienen animacion de
# caida. Al perder una vida parpadea la astronauta, no las telas. La bandera historica no aparece: esta es
# una instalacion nueva del sueno. Las cifras reales salen de las fichas bandera_lunar y tratado_espacio;
# compas, pixeles, margenes y tiempos son reglas de juego, no medidas lunares.

const ANCHO: int = 320
const ALTO: int = 180
const ESCALA: float = 4.0
const PASO_FIJO: float = 1.0 / 60.0

const MASTIL_X: Array[int] = [100, 202]
const BASE_Y: Array[int] = [142, 137]
const TRAMO_BAJO: float = 32.0
const HUNDIR_TOTAL: float = 12.0
const TELA_ANCHO: int = 40
const TELA_ALTO: int = 26
const TOPE: float = 40.0
const HOLGURA: float = 1.0
const REBOTE_A: float = 10.0
const ALT_MIN: float = 2.0
const ALT_MAX: float = 28.0
const ALT_INICIAL: Array[float] = [8.0, 18.0]
const PUESTO: float = 9.0
const ALCANCE: float = 7.0
const VEL_ASTRO: float = 48.0
const ACEL_ASTRO: float = 190.0
const FRENO_ASTRO: float = 150.0
const VEL_ALT: float = 16.0
const ACEL_ALT: float = 70.0
const ZONA_ROJA: float = 0.36
const CARTEL_S: float = 1.5
const AMANECER_S: float = 3.8

# por dificultad 1, 2 y 3
const PASADA: Array[float] = [0.80, 0.66, 0.55]
const VENTANA: Array[float] = [0.15, 0.12, 0.10]
const GOLPES: Array[int] = [4, 5, 6]
const VEL_BARRA: Array[float] = [22.0, 28.0, 34.0]
const MARGEN_TOPE: Array[float] = [5.0, 4.0, 3.0]
const FRENO_ALT: Array[float] = [40.0, 28.0, 20.0]
const SOSTEN: Array[float] = [0.7, 0.9, 1.1]
const LIMITE: Array[float] = [99.0, 90.0, 80.0]

const MISIONES: Array[String] = ["HINCA LOS MÁSTILES AL COMPÁS", "MANTÉN E Y SUELTA EN EL TOPE", "IGUALA LAS DOS ALTURAS", "DOS BANDERAS, UN CIELO"]
const LINEA_FINAL: String = "Sin viento, la barra horizontal sostiene la tela extendida. Y plantar una bandera no da territorio: es cooperación."

const PERFIL_CERCA: Array[Vector2i] = [Vector2i(0, 147), Vector2i(28, 146), Vector2i(60, 144), Vector2i(82, 142), Vector2i(120, 142), Vector2i(150, 141), Vector2i(182, 137), Vector2i(224, 137), Vector2i(250, 140), Vector2i(280, 144), Vector2i(319, 146)]
const PERFIL_LEJOS: Array[Vector2i] = [Vector2i(0, 125), Vector2i(30, 119), Vector2i(66, 126), Vector2i(110, 129), Vector2i(160, 122), Vector2i(202, 124), Vector2i(245, 116), Vector2i(282, 120), Vector2i(319, 125)]

const ASTRO_A: Array[String] = [
	"..pppp...",
	".pppppp..",
	".ppdddp..",
	".ppdddp..",
	".pppppp..",
	"mmcccc...",
	"mmcncccc.",
	"mmcccc.c.",
	"mmcccc...",
	".scccc...",
	"..cc.cc..",
	"..cc.cc..",
	".sss.sss.",
]
const ASTRO_B: Array[String] = [
	"..pppp...",
	".pppppp..",
	".ppdddp..",
	".ppdddp..",
	".pppppp..",
	"mmcccc...",
	"mmcncccc.",
	"mmcccc.c.",
	"mmcccc...",
	".scccc...",
	"...ccc...",
	"...ccc...",
	"..ssss...",
]
const CASCO: Array[String] = [
	".ppp.",
	"ppppp",
	"pdddp",
	"ppppp",
	".ppp.",
]
const TIERRA: Array[String] = [
	"....ooooo....",
	"..oowwoooo...",
	".oowwwooggo..",
	".owwoooggggo.",
	"ooooooogggooo",
	"oowoooooggooo",
	"owwwooooooooo",
	"oowwwooooowoo",
	"ooooooooowwoo",
	".oogggoooooo.",
	".ooggggoooo..",
	"..oogggooo...",
	"....ooooo....",
]
const ESCUDO: Array[String] = [
	"t..tt..t",
	"tttttttt",
	".tt..tt.",
	"..rrrr..",
	".rwwwwr.",
	".rwddwr.",
	".rggggr.",
	".roooor.",
	"..rrrr..",
]
const GLIFOS: Dictionary = {
	"A": "010101111101101", "B": "110101110101110", "C": "011100100100011", "D": "110101101101110",
	"E": "111100110100111", "F": "111100110100100", "G": "011100101101011", "H": "101101111101101",
	"I": "111010010010111", "J": "001001001101010", "K": "101101110101101", "L": "100100100100111",
	"M": "101111111101101", "N": "101111111111101", "O": "010101101101010", "P": "110101110100100",
	"Q": "010101101111011", "R": "110101110101101", "S": "011100010001110", "T": "111010010010010",
	"U": "101101101101111", "V": "101101101101010", "W": "101101111111101", "X": "101101010101101",
	"Y": "101101010010010", "Z": "111001010100111",
	"0": "111101101101111", "1": "010110010010111", "2": "111001111100111", "3": "111001111001111",
	"4": "101101111001001", "5": "111100111001111", "6": "111100111101111", "7": "111001001001001",
	"8": "111101111101111", "9": "111101111001111",
	"+": "000010111010000", "-": "000000111000000", ":": "000010000010000", ".": "000000000000010",
	",": "000000000010100", "!": "010010010000010", "¡": "010000010010010", "/": "001001010100100",
	"=": "000111000111000", "←": "001011111011001", "→": "100110111110100", "↑": "010111010010010",
	"↓": "010010010111010",
}
const ACENTOS: Dictionary = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}

# ---------------------------------------------------------------- estado de la partida (lo que se ve)
var fase: int = 0
var cartel: float = 0.0           # segundos que quedan del cartel de mision (el juego espera)
var reloj: float = 99.0           # cuenta atras
var limite: float = 99.0
var vidas: int = 3
var puntos: int = 0
var racha: int = 0
var astro_x: float = 56.0
var astro_v: float = 0.0
var mira: int = 1
var necesarios: int = 4
var ventana: float = 0.15
var margen: float = 5.0
var golpes: Array[int] = [0, 0]
var compas: Array[float] = [0.0, 0.31]
var marca: Array[float] = [0.0, 0.62]
var enfriar: float = 0.0
var barra: Array[float] = [0.0, 0.0]
var fijada: Array[bool] = [false, false]
var tirones: Array[int] = [0, 0]
var rebotando: Array[bool] = [false, false]
var tirando: int = -1
var tiron_t: float = 0.0
var alt: Array[float] = [8.0, 18.0]
var alt_v: Array[float] = [0.0, 0.0]
var nivel_t: float = 0.0
var luz: float = 0.0              # 0 = noche con luz cenicienta; 1 = amanecer
var final_t: float = 0.0
var fin_t: float = -1.0           # pausa breve antes de cerrar una partida perdida
var fin_causa: String = ""
var ultima_causa: String = "compas"

# ---------------------------------------------------------------- mandos (teclas o piloto: mismo camino)
var c_x: float = 0.0
var c_y: float = 0.0
var c_e: bool = false
var c_e_antes: bool = false
var _auto: int = 0

# ---------------------------------------------------------------- solo visual
var _azar: RandomNumberGenerator = RandomNumberGenerator.new()
var _paleta: Dictionary = {}
var _suelo: PackedInt32Array = PackedInt32Array()
var _lejos: PackedInt32Array = PackedInt32Array()
var _estrellas: Array[Vector3] = []
var _telas: Array[PackedColorArray] = []
var _telas_tinte: Array[PackedColorArray] = []
var _luz_tinte: float = -1.0
var _chispas: Array[Dictionary] = []
var _rotulos: Array[Dictionary] = []
var _t_vis: float = 0.0
var _sacude_t: float = 0.0
var _sacude_m: float = 0.0
var _desvio: Vector2 = Vector2.ZERO
var _destello: float = 0.0
var _destello_color: Color = Color.WHITE
var _parpadeo: float = 0.0
var _golpe_t: float = 0.0
var _paso_anim: float = 0.0
var _vis_hundir: Array[float] = [12.0, 12.0]


func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	_azar.seed = 20261114
	necesarios = GOLPES[dificultad - 1]
	ventana = VENTANA[dificultad - 1]
	margen = MARGEN_TOPE[dificultad - 1]
	limite = LIMITE[dificultad - 1]
	reloj = limite
	alt = [ALT_INICIAL[0], ALT_INICIAL[1]]
	_paleta = {
		"p": Estilo.PAPEL, "d": Estilo.DORADO, "c": Estilo.CREMA, "m": Estilo.PETROLEO, "n": Estilo.CORAL,
		"s": Estilo.PAPEL_SOMBRA, "t": Estilo.TINTA, "o": Estilo.PETROLEO, "w": Estilo.BRILLO,
		"g": Estilo.VERDE, "r": Estilo.TERRACOTA,
	}
	_suelo = _perfil(PERFIL_CERCA)
	_lejos = _perfil(PERFIL_LEJOS)
	for k in 80:
		_estrellas.append(Vector3(float(_azar.randi_range(2, ANCHO - 3)), float(_azar.randi_range(18, 119)), _azar.randf_range(0.0, TAU)))
	_armar_telas()
	queue_redraw()


func _empezar() -> void:
	fase = 0
	cartel = CARTEL_S
	c_e_antes = true      # el Intro de «Empezar» no cuenta como golpe
	sonar("radio")


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


func _gui_input(evento: InputEvent) -> void:
	# las flechas son del juego: que no muevan el foco de la interfaz
	if activo and evento is InputEventKey:
		for accion in ["mover_izquierda", "mover_derecha", "mover_arriba", "mover_abajo", "interactuar", "saltar"]:
			if evento.is_action(accion):
				accept_event()
				return


# ================================================================== reglas

func _paso(delta: float) -> void:
	var hx: float = 0.0
	var hy: float = 0.0
	var he: bool = false
	if _auto == 0:
		hx = eje_x()
		hy = eje_y()
		he = Input.is_action_pressed("interactuar") or Input.is_action_pressed("saltar")
	# paso fijo: el juego se comporta igual con el reloj acelerado de las pruebas
	var resto: float = delta
	var n: int = 0
	while resto > 0.0001 and activo and n < 90:
		var dt: float = minf(resto, PASO_FIJO)
		resto -= dt
		n += 1
		if _auto != 0:
			_piloto()
		else:
			c_x = hx
			c_y = hy
			c_e = he
		_simular(dt)
	queue_redraw()


func _simular(dt: float) -> void:
	_efectos(dt)
	if fin_t >= 0.0:
		fin_t -= dt
		if fin_t <= 0.0:
			terminar(false, float(puntos), fin_causa)
		return
	if fase == 3:
		final_t += dt
		luz = smoothstep(0.0, 2.6, final_t)
		if _azar.randf() < dt * 5.0:
			_chispa(Vector2(float(_azar.randi_range(MASTIL_X[0], MASTIL_X[1] + TELA_ANCHO)), float(_azar.randi_range(78, 128))), Vector2(0.0, -6.0), 0.9, Estilo.BRILLO, 0.0)
		if final_t >= AMANECER_S:
			terminar(true, float(puntos), LINEA_FINAL)
		return
	if cartel > 0.0:
		cartel -= dt
		c_e_antes = c_e
		return
	reloj -= dt
	if reloj <= 0.0:
		reloj = 0.0
		_perder(_causa_tiempo())
		return
	var pulso: bool = c_e and not c_e_antes
	c_e_antes = c_e
	_mover_astro(dt)
	match fase:
		0:
			_hincar(dt, pulso)
		1:
			_extender(dt, pulso)
		2:
			_igualar(dt)


func cerca() -> int:
	# mastil al alcance de la astronauta (-1 si no hay ninguno)
	for i in 2:
		if absf(astro_x - (float(MASTIL_X[i]) - PUESTO)) <= ALCANCE:
			return i
	return -1


func resto_hundir(i: int) -> float:
	return HUNDIR_TOTAL * (1.0 - float(golpes[i]) / float(necesarios))


func tope_y(i: int) -> int:
	# fila de pixeles de la barra: lo que se ve es lo que cuenta
	return roundi(float(BASE_Y[i]) - TRAMO_BAJO - resto_hundir(i) - alt[i])


func telas_integras() -> bool:
	# ninguna tela toca el suelo ni sale de su mastil
	for i in 2:
		if alt[i] < ALT_MIN - 0.001 or alt[i] > ALT_MAX + 0.001:
			return false
		if tope_y(i) + 1 + TELA_ALTO >= BASE_Y[i]:
			return false
	return true


func _mover_astro(dt: float) -> void:
	if tirando >= 0:
		astro_v = 0.0
		return
	if absf(c_x) > 0.2:
		astro_v = move_toward(astro_v, signf(c_x) * VEL_ASTRO, ACEL_ASTRO * dt)
		mira = 1 if c_x > 0.0 else -1
	else:
		astro_v = move_toward(astro_v, 0.0, FRENO_ASTRO * dt)
	astro_x += astro_v * dt
	if astro_x < 8.0 or astro_x > ANCHO - 8.0:
		astro_x = clampf(astro_x, 8.0, ANCHO - 8.0)
		astro_v = 0.0
	_paso_anim += absf(astro_v) * dt


func _hincar(dt: float, pulso: bool) -> void:
	enfriar = maxf(0.0, enfriar - dt)
	var i_cerca: int = cerca()
	for i in 2:
		var antes: float = marca[i]
		compas[i] += dt / (2.0 * PASADA[dificultad - 1] * (1.0 if i == 0 else 0.88))
		var f: float = fposmod(compas[i], 1.0)
		marca[i] = 1.0 - absf(2.0 * f - 1.0)
		if i == i_cerca and golpes[i] < necesarios and (antes - 0.5) * (marca[i] - 0.5) < 0.0:
			sonar("tic")
	if not pulso or enfriar > 0.0 or i_cerca < 0 or golpes[i_cerca] >= necesarios:
		return
	enfriar = 0.28
	_golpe_t = 0.16
	mira = 1
	var d: float = absf(marca[i_cerca] - 0.5)
	var base: Vector2 = Vector2(float(MASTIL_X[i_cerca]), float(BASE_Y[i_cerca]))
	if d <= ventana:
		golpes[i_cerca] += 1
		racha += 1
		var gana: int = 100 * mini(racha, 4)
		if d <= ventana * 0.35:
			gana += 50
			_rotulo("¡JUSTO!", base + Vector2(-14.0, -52.0), Estilo.CIAN)
		puntos += gana
		_rotulo("+%d" % gana, base + Vector2(6.0, -24.0), Estilo.DORADO)
		_polvo(base, 10, Estilo.PAPEL_SOMBRA, 26.0)
		_sacudir(1.0, 0.12)
		sonar("salto")
		if golpes[i_cerca] >= necesarios:
			_rotulo("FIRME", base + Vector2(-10.0, -62.0), Estilo.CIAN)
			_destellar(Estilo.BRILLO, 0.18)
			sonar("recoger")
			if golpes[0] >= necesarios and golpes[1] >= necesarios:
				_pasar_fase(1)
	elif d >= ZONA_ROJA:
		racha = 0
		_polvo(base + Vector2(-3.0, -9.0), 8, Estilo.CORAL, 30.0)
		_rotulo("FUERA", base + Vector2(-10.0, -24.0), Estilo.CORAL)
		_perder_vida("compas")
	else:
		racha = 0
		_rotulo("CASI", base + Vector2(-8.0, -24.0), Estilo.CREMA)
		sonar("tic")


func _extender(dt: float, pulso: bool) -> void:
	for i in 2:
		if rebotando[i]:
			barra[i] = maxf(REBOTE_A, barra[i] - 90.0 * dt)
			if barra[i] <= REBOTE_A:
				rebotando[i] = false
	if tirando >= 0:
		var i: int = tirando
		var punta: Vector2 = Vector2(float(MASTIL_X[i]) + 1.0 + barra[i], float(tope_y(i)))
		if not c_e:
			# se suelta: o queda fijada en el tope o queda corta
			tirando = -1
			if barra[i] >= TOPE - margen:
				fijada[i] = true
				barra[i] = TOPE
				var gana: int = 300 + (200 if tirones[i] == 0 else 0)
				puntos += gana
				_rotulo("+%d" % gana, punta + Vector2(-8.0, -9.0), Estilo.DORADO)
				_polvo(punta, 8, Estilo.CIAN, 18.0)
				_destellar(Estilo.BRILLO, 0.18)
				_sacudir(1.0, 0.1)
				sonar("recoger")
				if fijada[0] and fijada[1]:
					_pasar_fase(2)
			else:
				tirones[i] += 1
				_rotulo("CORTA", punta + Vector2(-6.0, -9.0), Estilo.CREMA)
				sonar("tic")
			return
		tiron_t += dt
		var vmax: float = VEL_BARRA[dificultad - 1]
		var v: float = minf(vmax, 8.0 + (vmax - 8.0) * tiron_t)
		var antes: int = int(barra[i] / 4.0)
		barra[i] += v * dt
		if int(barra[i] / 4.0) != antes:
			sonar("tic")
		if barra[i] > TOPE + HOLGURA:
			# se paso del tope: el seguro salta y la barra se recoge (la tela no sufre: solo se pliega)
			barra[i] = TOPE
			rebotando[i] = true
			tirando = -1
			tirones[i] += 1
			_rotulo("PASADA", punta + Vector2(-10.0, -9.0), Estilo.CORAL)
			_polvo(punta, 6, Estilo.CORAL, 22.0)
			_perder_vida("tope")
		return
	var i_cerca: int = cerca()
	if pulso and i_cerca >= 0 and not fijada[i_cerca] and not rebotando[i_cerca]:
		tirando = i_cerca
		tiron_t = 0.0
		mira = 1
		sonar("pulsar")


func _igualar(dt: float) -> void:
	var i_cerca: int = cerca()
	for i in 2:
		var entrada: float = c_y if i == i_cerca else 0.0
		if absf(entrada) > 0.2:
			alt_v[i] = move_toward(alt_v[i], signf(entrada) * VEL_ALT, ACEL_ALT * dt)
		else:
			alt_v[i] = move_toward(alt_v[i], 0.0, FRENO_ALT[dificultad - 1] * dt)
		var antes: int = tope_y(i)
		alt[i] += alt_v[i] * dt
		if alt[i] < ALT_MIN or alt[i] > ALT_MAX:
			alt[i] = clampf(alt[i], ALT_MIN, ALT_MAX)
			alt_v[i] = 0.0
		if tope_y(i) != antes and tope_y(i) % 2 == 0:
			sonar("tic")
	var iguales: bool = tope_y(0) == tope_y(1)
	var quietas: bool = absf(alt_v[0]) < 2.0 and absf(alt_v[1]) < 2.0
	if iguales and quietas:
		if nivel_t <= 0.0:
			sonar("ok")
		nivel_t += dt
		if nivel_t >= SOSTEN[dificultad - 1]:
			_amanecer()
	else:
		nivel_t = 0.0


func _amanecer() -> void:
	var premio: int = 500 + int(reloj) * 10 + vidas * 200
	puntos += premio
	fase = 3
	final_t = 0.0
	alt_v = [0.0, 0.0]
	_rotulo("+%d" % premio, Vector2(144.0, 92.0), Estilo.DORADO)
	_destellar(Estilo.CREMA, 0.35)
	sonar("logro")
	if _auto != 0:
		print("BANDERAS fase=3 t=%.2f puntos=%d vidas=%d" % [tiempo, puntos, vidas])


func _pasar_fase(nueva: int) -> void:
	fase = nueva
	cartel = CARTEL_S
	racha = 0
	sonar("radio")
	if _auto != 0:
		print("BANDERAS fase=%d t=%.2f" % [fase, tiempo])


func _perder_vida(tipo: String) -> void:
	vidas -= 1
	ultima_causa = tipo
	_parpadeo = 0.9
	_sacudir(2.0, 0.25)
	_destellar(Estilo.CORAL, 0.22)
	sonar("error")
	if vidas <= 0:
		if tipo == "tope":
			_perder("El seguro de la barra saltó tres veces: hay que soltar justo cuando la punta llega al tope.")
		else:
			_perder("Tres golpes lejos del centro del compás: el mástil se asienta con ritmo, no con fuerza.")


func _perder(causa: String) -> void:
	# las banderas se quedan como estan, en pie; solo se cierra la partida
	fin_t = 1.0
	fin_causa = causa
	tirando = -1


func _causa_tiempo() -> String:
	match fase:
		0:
			return "Se acabó el tiempo con un mástil sin asentar: golpea cuando la marca cruza el centro."
		1:
			return "Se acabó el tiempo con una barra corta: sin viento, la tela queda ondulada."
	return "Se acabó el tiempo con las banderas a distinta altura: junta las dos líneas."


# ================================================================== piloto (mueve los mismos mandos)

func _piloto() -> void:
	c_x = 0.0
	c_y = 0.0
	var e: bool = false
	if cartel > 0.0 or fase == 3 or fin_t >= 0.0:
		c_e = false
		return
	var obj: int = 0
	match fase:
		0:
			obj = 0 if golpes[0] < necesarios else 1
		1:
			obj = 1 if not fijada[1] else 0
			if not fijada[0] and not fijada[1] and absf(astro_x - float(MASTIL_X[0])) < absf(astro_x - float(MASTIL_X[1])):
				obj = 0
		2:
			obj = 0
			if cerca() == 1:
				obj = 1
	var dx: float = float(MASTIL_X[obj]) - PUESTO - astro_x
	if tirando < 0:
		var deseada: float = clampf(dx * 5.0, -VEL_ASTRO, VEL_ASTRO)
		if absf(dx) > 1.5 and absf(deseada - astro_v) > 4.0:
			c_x = signf(deseada - astro_v)
	var listo: bool = cerca() == obj and absf(dx) < ALCANCE - 2.0
	match fase:
		0:
			if listo and enfriar <= 0.0 and not c_e_antes:
				var d: float = absf(marca[obj] - 0.5)
				if _auto > 0:
					e = d <= ventana * 0.4
				else:
					e = d >= 0.43      # golpea a destiempo: asi se pierde de verdad
		1:
			if tirando == obj:
				e = barra[obj] < TOPE - margen * 0.5
			elif listo and absf(astro_v) < 4.0 and not rebotando[obj] and not c_e_antes:
				e = true
		2:
			var otro: int = 1 - obj
			var objetivo: float = clampf(alt[otro] + float(BASE_Y[obj] - BASE_Y[otro]), ALT_MIN, ALT_MAX)
			var falta: float = objetivo - alt[obj]
			var v_deseada: float = clampf(falta * 4.0, -VEL_ALT, VEL_ALT)
			if listo and absf(falta) > 0.15 and absf(v_deseada - alt_v[obj]) > 1.0:
				c_y = signf(v_deseada - alt_v[obj])
	c_e = e


# ================================================================== efectos

func _efectos(dt: float) -> void:
	_t_vis += dt
	_destello = maxf(0.0, _destello - dt)
	_parpadeo = maxf(0.0, _parpadeo - dt)
	_golpe_t = maxf(0.0, _golpe_t - dt)
	if _sacude_t > 0.0:
		_sacude_t -= dt
		_desvio = Vector2(float(_azar.randi_range(-1, 1)), float(_azar.randi_range(-1, 1))) * _sacude_m
		if _sacude_t <= 0.0:
			_desvio = Vector2.ZERO
	for i in 2:
		_vis_hundir[i] = move_toward(_vis_hundir[i], resto_hundir(i), 40.0 * dt)
	var k: int = _chispas.size() - 1
	while k >= 0:
		var c: Dictionary = _chispas[k]
		var vida: float = c["t"]
		vida -= dt
		if vida <= 0.0:
			_chispas.remove_at(k)
		else:
			var v: Vector2 = c["v"]
			var p: Vector2 = c["p"]
			var g: float = c["g"]
			v.y += g * dt          # sin aire: el polvo vuela en parabola y cae despacio
			c["v"] = v
			c["p"] = p + v * dt
			c["t"] = vida
		k -= 1
	k = _rotulos.size() - 1
	while k >= 0:
		var r: Dictionary = _rotulos[k]
		var queda: float = r["t"]
		queda -= dt
		if queda <= 0.0:
			_rotulos.remove_at(k)
		else:
			var pos: Vector2 = r["p"]
			r["p"] = pos + Vector2(0.0, -9.0 * dt)
			r["t"] = queda
		k -= 1


func _chispa(p: Vector2, v: Vector2, vida: float, color: Color, gravedad: float = 26.0) -> void:
	if _chispas.size() < 90:
		_chispas.append({"p": p, "v": v, "t": vida, "c": color, "g": gravedad})


func _polvo(p: Vector2, cuantas: int, color: Color, fuerza: float) -> void:
	for k in cuantas:
		var a: float = _azar.randf_range(-PI, 0.0)
		_chispa(p, Vector2(cos(a), sin(a)) * _azar.randf_range(0.35, 1.0) * fuerza, _azar.randf_range(0.4, 0.9), color)


func _rotulo(s: String, p: Vector2, color: Color) -> void:
	_rotulos.append({"s": s, "p": p, "t": 0.9, "c": color})


func _sacudir(magnitud: float, segundos: float) -> void:
	_sacude_m = magnitud
	_sacude_t = segundos


func _destellar(color: Color, segundos: float) -> void:
	_destello_color = color
	_destello = segundos


# ================================================================== preparacion del dibujo

func _perfil(claves: Array[Vector2i]) -> PackedInt32Array:
	var r: PackedInt32Array = PackedInt32Array()
	r.resize(ANCHO)
	for k in claves.size() - 1:
		var a: Vector2i = claves[k]
		var b: Vector2i = claves[k + 1]
		for x in range(a.x, b.x + 1):
			if x < ANCHO:
				r[x] = roundi(lerpf(float(a.y), float(b.y), float(x - a.x) / float(maxi(1, b.x - a.x))))
	return r


func _armar_telas() -> void:
	var azul: Color = Estilo.PETROLEO.darkened(0.12)
	# Estados Unidos: 13 franjas de 2 px y canton con estrellas sugeridas
	var a: PackedColorArray = PackedColorArray()
	a.resize(TELA_ANCHO * TELA_ALTO)
	for cy in TELA_ALTO:
		for cx in TELA_ANCHO:
			var franja: int = cy >> 1
			var c: Color = Estilo.CORAL if franja % 2 == 0 else Estilo.PAPEL
			if cx < 18 and cy < 14:
				c = azul
				if cy % 2 == 1 and cy <= 11:
					var fila: int = cy >> 1
					if (fila % 2 == 0 and cx % 3 == 1) or (fila % 2 == 1 and cx % 3 == 2 and cx < 15):
						c = Estilo.BRILLO
			a[cy * TELA_ANCHO + cx] = c
	# Ecuador: amarillo doble, azul y rojo, con el escudo simplificado al centro
	var b: PackedColorArray = PackedColorArray()
	b.resize(TELA_ANCHO * TELA_ALTO)
	for cy in TELA_ALTO:
		for cx in TELA_ANCHO:
			var c: Color = Estilo.DORADO
			if cy >= 20:
				c = Estilo.CORAL
			elif cy >= 13:
				c = azul
			b[cy * TELA_ANCHO + cx] = c
	for fy in ESCUDO.size():
		var linea: String = ESCUDO[fy]
		for fx in linea.length():
			var ch: String = linea[fx]
			if ch != ".":
				var color: Color = _paleta[ch]
				b[(8 + fy) * TELA_ANCHO + 16 + fx] = color
	_telas = [a, b]
	_telas_tinte = [a.duplicate(), b.duplicate()]
	_luz_tinte = -1.0


func _t(c: Color) -> Color:
	# de noche el mundo se ve con la luz tenue de la Tierra
	return c.lerp(Estilo.NOCHE, 0.42 * (1.0 - luz))


func _r(x: int, y: int, w: int, h: int, c: Color) -> void:
	draw_rect(Rect2(float(x), float(y), float(w), float(h)), c)


func _sprite(filas: Array[String], x: int, y: int, espejo: bool = false, noche: bool = true) -> void:
	for fy in filas.size():
		var fila: String = filas[fy]
		var n: int = fila.length()
		var fx: int = 0
		while fx < n:
			var ch: String = fila[fx]
			var largo: int = 1
			while fx + largo < n and fila[fx + largo] == ch:
				largo += 1
			if ch != ".":
				var c: Color = _paleta[ch]
				var px: int = x + (n - fx - largo if espejo else fx)
				_r(px, y + fy, largo, 1, _t(c) if noche else c)
			fx += largo


func _ancho_letras(s: String, escala: int = 1) -> int:
	return s.length() * 4 * escala - escala


func _letras(s: String, x: int, y: int, color: Color, escala: int = 1) -> void:
	var cursor: int = x
	for k in s.length():
		var ch: String = s[k]
		var acento: bool = ACENTOS.has(ch)
		var tilde: bool = ch == "Ñ"
		if acento:
			ch = ACENTOS[ch]
		elif tilde:
			ch = "N"
		if GLIFOS.has(ch):
			var bits: String = GLIFOS[ch]
			for b in 15:
				if bits[b] == "1":
					_r(cursor + (b % 3) * escala, y + (b / 3) * escala, escala, escala, color)
			if acento:
				_r(cursor + escala, y - 2 * escala, escala, escala, color)
				_r(cursor + 2 * escala, y - 3 * escala, escala, escala, color)
			elif tilde:
				_r(cursor, y - 2 * escala, 3 * escala, escala, color)
		cursor += 4 * escala


func _numero(valor: int, cifras: int, x: int, y: int, color: Color, escala: int = 2) -> void:
	_letras(str(maxi(valor, 0)).pad_zeros(cifras), x, y, color, escala)


# ================================================================== dibujo

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(ESCALA, ESCALA))
	_r(-4, -4, ANCHO + 8, ALTO + 8, Estilo.NOCHE)
	_dibujar_cielo()
	_dibujar_suelo()
	if fase == 0:
		_dibujar_compases()
	elif fase == 2:
		_dibujar_guias()
	_dibujar_astronauta()
	for i in 2:
		_dibujar_mastil(i)
	_dibujar_avisos()
	for c in _chispas:
		var p: Vector2 = c["p"]
		var color: Color = c["c"]
		_r(roundi(p.x), roundi(p.y), 1, 1, color)
	for r in _rotulos:
		var pos: Vector2 = r["p"]
		var tono: Color = r["c"]
		var s: String = r["s"]
		_letras(s, roundi(pos.x), roundi(pos.y), tono)
	_dibujar_marcador()
	if cartel > 0.0 and fase < 3:
		_dibujar_cartel()
	if _destello > 0.0:
		_r(-4, -4, ANCHO + 8, ALTO + 8, Color(_destello_color, clampf(_destello * 1.6, 0.0, 0.35)))
	if fin_t >= 0.0:
		_r(0, 14, ANCHO, ALTO - 25, Color(Estilo.NOCHE, 0.35))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _dibujar_cielo() -> void:
	for e in _estrellas:
		var brillo: float = 0.55 + 0.45 * sin(_t_vis * 1.2 + e.z)
		_r(int(e.x), int(e.y), 1, 1, Estilo.NOCHE.lerp(Estilo.PAPEL, brillo * (1.0 - 0.35 * luz)))
	# la Tierra, casi llena, alumbra la noche lunar
	for fy in TIERRA.size():
		var fila: String = TIERRA[fy]
		for fx in fila.length():
			var ch: String = fila[fx]
			if ch != ".":
				var c: Color = _paleta[ch]
				if fx >= 9:
					c = c.lerp(Estilo.NOCHE, 0.62)
				_r(270 + fx, 35 + fy, 1, 1, c)
	if luz > 0.0:
		# el sol asoma tras la loma: en la Luna el cielo sigue oscuro, solo cambia la luz del suelo
		var cx: int = 30
		var cy: int = roundi(lerpf(158.0, 123.0, luz))
		for dy in range(-21, 22):
			for dx in range(-21, 22):
				var d2: int = dx * dx + dy * dy
				if d2 > 196 and d2 <= 441:
					var cerca_sol: bool = d2 <= 289
					if (cerca_sol and (dx + dy) % 2 == 0) or (not cerca_sol and (dx + dy * 2) % 4 == 0):
						_r(cx + dx, cy + dy, 1, 1, Estilo.NOCHE.lerp(Estilo.NARANJA if cerca_sol else Estilo.TERRACOTA, 0.75 * luz))
		for dy in range(-14, 15):
			var medio: int = int(sqrt(float(196 - dy * dy)))
			var banda: Color = Estilo.CREMA if dy < -8 else (Estilo.DORADO if dy < 0 else Estilo.NARANJA)
			_r(cx - medio, cy + dy, medio * 2 + 1, 1, banda)


func _dibujar_suelo() -> void:
	var lejos: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.22).lerp(Estilo.TERRACOTA.lerp(Estilo.NARANJA, 0.35), luz)
	var cerca_c: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.5).lerp(Estilo.PAPEL_SOMBRA, luz)
	var borde: Color = Estilo.PETROLEO.lerp(Estilo.BRILLO, 0.3).lerp(Estilo.PAPEL, luz)
	var hondo: Color = cerca_c.lerp(Estilo.NOCHE, 0.3)
	_tramos(_lejos, lejos, lejos.lerp(Estilo.CREMA, 0.25 + 0.3 * luz))
	_tramos(_suelo, cerca_c, borde)
	# crateres y piedras
	for c in [Vector3i(18, 157, 9), Vector3i(244, 153, 12), Vector3i(290, 162, 7), Vector3i(148, 161, 6)]:
		_r(c.x, c.y, c.z, 1, hondo)
		_r(c.x + 1, c.y + 1, c.z - 2, 1, hondo)
		_r(c.x + 1, c.y + 2, c.z - 2, 1, borde.lerp(cerca_c, 0.5))
	for p in [Vector2i(44, 150), Vector2i(67, 163), Vector2i(226, 148), Vector2i(276, 155), Vector2i(174, 147), Vector2i(120, 151)]:
		_r(p.x, p.y, 2, 1, hondo)
	if luz > 0.0:
		# sombras largas del amanecer
		var largo: int = roundi(46.0 * luz)
		for i in 2:
			_r(MASTIL_X[i] + 2, BASE_Y[i] + 1, largo, 1, Color(Estilo.TINTA, 0.55 * luz))
		_r(roundi(astro_x) + 4, _suelo[clampi(roundi(astro_x), 0, ANCHO - 1)] + 1, roundi(18.0 * luz), 1, Color(Estilo.TINTA, 0.55 * luz))


func _tramos(perfil: PackedInt32Array, relleno: Color, borde: Color) -> void:
	var x: int = 0
	while x < ANCHO:
		var y: int = perfil[x]
		var n: int = 1
		while x + n < ANCHO and perfil[x + n] == y:
			n += 1
		_r(x, y, n, ALTO - y, relleno)
		_r(x, y, n, 1, borde)
		x += n


func _dibujar_compases() -> void:
	var i_cerca: int = cerca()
	for i in 2:
		if golpes[i] >= necesarios:
			continue
		var apaga: float = 0.0 if i == i_cerca else 0.5
		var tx: int = MASTIL_X[i] - 22
		var ty: int = BASE_Y[i] + 8
		_r(tx - 1, ty - 1, 46, 7, Estilo.TINTA)
		_r(tx, ty, 44, 5, Estilo.NOCHE)
		var rojo: int = roundi(44.0 * (0.5 - ZONA_ROJA))
		_r(tx, ty, rojo, 5, Estilo.CORAL.lerp(Estilo.NOCHE, apaga))
		_r(tx + 44 - rojo, ty, rojo, 5, Estilo.CORAL.lerp(Estilo.NOCHE, apaga))
		var medio: int = roundi(44.0 * ventana * 2.0)
		_r(tx + 22 - medio / 2, ty, medio, 5, Estilo.CIAN.lerp(Estilo.NOCHE, apaga))
		_r(tx + 21, ty, 2, 5, Estilo.BRILLO.lerp(Estilo.NOCHE, apaga))
		var mx: int = tx + roundi(marca[i] * 43.0)
		_r(mx - 1, ty - 2, 3, 9, Estilo.TINTA)
		_r(mx, ty - 2, 1, 9, Estilo.DORADO.lerp(Estilo.NOCHE, apaga))
		_r(mx - 1, ty + 1, 3, 3, Estilo.PAPEL.lerp(Estilo.NOCHE, apaga))
		for k in necesarios:
			_r(tx + 47, ty + 4 - k * 2 + (necesarios - 4), 2, 1, Estilo.DORADO if k < golpes[i] else Estilo.TINTA_SUAVE)


func _dibujar_guias() -> void:
	var y0: int = tope_y(0)
	var y1: int = tope_y(1)
	var x0: int = MASTIL_X[0] - 8
	var x1: int = MASTIL_X[1] + TELA_ANCHO + 10
	if y0 == y1:
		_r(x0, y0, x1 - x0, 1, Estilo.CIAN)
	else:
		var x: int = x0
		while x < x1:
			_r(x, y0, 2, 1, Estilo.CREMA.lerp(Estilo.NOCHE, 0.35))
			_r(x + 2, y1, 2, 1, Estilo.DORADO.lerp(Estilo.NOCHE, 0.25))
			x += 5
	# nivel de burbuja entre los dos mastiles
	var nx: int = 140
	var ny: int = 153
	_r(nx - 1, ny - 1, 35, 7, Estilo.TINTA)
	_r(nx, ny, 33, 5, Estilo.NOCHE)
	_r(nx + 13, ny, 1, 5, Estilo.PAPEL_SOMBRA)
	_r(nx + 19, ny, 1, 5, Estilo.PAPEL_SOMBRA)
	var corre: int = clampi((y0 - y1) * 2, -13, 13)
	_r(nx + 14 + corre, ny + 1, 5, 3, Estilo.CIAN if y0 == y1 else Estilo.DORADO)
	if nivel_t > 0.0:
		_r(nx, ny + 7, roundi(33.0 * clampf(nivel_t / SOSTEN[dificultad - 1], 0.0, 1.0)), 1, Estilo.CIAN)


func _dibujar_astronauta() -> void:
	if _parpadeo > 0.0 and int(_parpadeo * 10.0) % 2 == 0:
		return
	var ax: int = roundi(astro_x)
	var ay: int = _suelo[clampi(ax, 0, ANCHO - 1)]
	var bote: int = 0
	var cuadro: Array[String] = ASTRO_A
	if absf(astro_v) > 6.0:
		bote = -int(absf(sin(_paso_anim * 0.4)) * 2.2)
		if int(_paso_anim / 6.0) % 2 == 1:
			cuadro = ASTRO_B
	elif fase == 3:
		bote = -int(absf(sin(_t_vis * 4.0)) * 3.0)      # salta de alegria con la gravedad lunar
	var espejo: bool = mira < 0
	_sprite(cuadro, ax - 4, ay - 13 + bote, espejo)
	if fase == 0:
		# el mazo: en alto mientras espera, contra el mastil cuando golpea
		var lado: int = -1 if espejo else 1
		if _golpe_t > 0.0:
			_r(ax + (3 if lado > 0 else -6), ay - 8 + bote, 4, 1, _t(Estilo.CREMA))
			_r(ax + (6 if lado > 0 else -7), ay - 10 + bote, 2, 5, _t(Estilo.PAPEL))
		else:
			_r(ax + 4 * lado, ay - 12 + bote, 1, 5, _t(Estilo.CREMA))
			_r(ax + 4 * lado - 1, ay - 14 + bote, 3, 2, _t(Estilo.PAPEL))
	elif fase == 1 and tirando >= 0:
		_r(ax + 4, ay - 10, 1, 3, _t(Estilo.CREMA))


func _dibujar_mastil(i: int) -> void:
	var x: int = MASTIL_X[i]
	var base: int = BASE_Y[i]
	var bajo: int = roundi(float(base) - TRAMO_BAJO - _vis_hundir[i])
	var arriba: int = roundi(float(base) - TRAMO_BAJO - _vis_hundir[i] - alt[i])
	# tramo bajo, con la punta rayada que aun falta hincar
	_r(x - 1, bajo, 3, base - bajo + 1, _t(Estilo.PAPEL_SOMBRA))
	_r(x - 1, bajo, 1, base - bajo + 1, _t(Estilo.PAPEL))
	var raya: int = bajo + int(TRAMO_BAJO)
	while raya < base:
		_r(x - 1, raya, 3, 1, _t(Estilo.CORAL if (raya - bajo) % 2 == 0 else Estilo.DORADO))
		raya += 1
	_r(x - 2, bajo, 5, 1, _t(Estilo.TINTA_SUAVE))
	# tramo alto y remate
	_r(x, arriba, 1, bajo - arriba, _t(Estilo.PAPEL))
	_r(x, arriba - 1, 1, 1, _t(Estilo.DORADO))
	var largo: int = roundi(barra[i])
	if fase == 1 and not fijada[i]:
		# la barra completa en punteado, el corchete del tope y el limite
		var apaga: float = 0.0 if cerca() == i else 0.45
		var k: int = x + 2
		while k <= x + 1 + int(TOPE):
			_r(k, arriba, 1, 1, Estilo.PETROLEO)
			k += 2
		var zona: int = roundi(margen)
		var zx: int = x + 1 + int(TOPE) - zona
		_r(zx, arriba - 3, zona + 1, 1, Estilo.CIAN.lerp(Estilo.NOCHE, apaga))
		_r(zx, arriba - 3, 1, 3, Estilo.CIAN.lerp(Estilo.NOCHE, apaga))
		_r(zx + zona, arriba - 3, 1, 3, Estilo.CIAN.lerp(Estilo.NOCHE, apaga))
		_r(zx + zona + 2, arriba - 2, 2, 5, Estilo.CORAL.lerp(Estilo.NOCHE, apaga))
	if largo > 0:
		_r(x + 1, arriba, largo + 1, 1, _t(Estilo.PAPEL))
		if fase == 1 and not fijada[i]:
			_r(x + 1 + largo, arriba - 1, 1, 3, Estilo.DORADO)
		elif fijada[i]:
			_r(x + 1 + largo, arriba - 1, 1, 3, _t(Estilo.CIAN_MEDIO))
	_dibujar_tela(i, x + 2, arriba + 1, largo)


func _dibujar_tela(i: int, x: int, y: int, largo: int) -> void:
	if not is_equal_approx(_luz_tinte, luz):
		_luz_tinte = luz
		for j in 2:
			var origen: PackedColorArray = _telas[j]
			var destino: PackedColorArray = _telas_tinte[j]
			for k in origen.size():
				destino[k] = _t(origen[k])
			_telas_tinte[j] = destino
	var colores: PackedColorArray = _telas_tinte[i]
	if largo < 3:
		# enrollada y atada al mastil
		for cy in TELA_ALTO:
			_r(x, y + cy, 2, 1, colores[cy * TELA_ANCHO + 1])
		_r(x, y + 6, 2, 1, _t(Estilo.TINTA))
		_r(x, y + 19, 2, 1, _t(Estilo.TINTA))
		return
	# con la barra corta la tela cuelga en pliegues QUIETOS: no hay viento que la mueva ni la estire
	var corta: float = 0.0 if fijada[i] else clampf(1.0 - float(largo) / TOPE, 0.0, 1.0)
	for sx in largo:
		var cx: int = mini(TELA_ANCHO - 1, int(float(sx) * float(TELA_ANCHO) / float(largo)))
		var cae: int = roundi(absf(sin(float(sx) * 0.95 + float(i) * 1.7)) * corta * 3.2)
		var sombra: bool = cae >= 2
		var cy: int = 0
		while cy < TELA_ALTO:
			var c: Color = colores[cy * TELA_ANCHO + cx]
			var n: int = 1
			while cy + n < TELA_ALTO and colores[(cy + n) * TELA_ANCHO + cx] == c:
				n += 1
			_r(x + sx, y + cy + cae, 1, n, c.darkened(0.18) if sombra else c)
			cy += n


func _dibujar_avisos() -> void:
	# flecha cian sobre el mastil que espera a la astronauta
	if cartel > 0.0 or fase >= 3 or fin_t >= 0.0:
		return
	var i_cerca: int = cerca()
	var bote: int = int(sin(_t_vis * 4.0) * 1.6)
	for i in 2:
		var pendiente: bool = (fase == 0 and golpes[i] < necesarios) or (fase == 1 and not fijada[i])
		if fase == 2:
			pendiente = true
		var ax: int = MASTIL_X[i]
		var ay: int = roundi(float(BASE_Y[i]) - TRAMO_BAJO - _vis_hundir[i] - alt[i]) - 9
		if fase == 2 and i == i_cerca:
			# flechas de subir y bajar junto al mastil activo
			_letras("↑", ax - 6, ay + 5, Estilo.CIAN)
			_letras("↓", ax - 6, ay + 12, Estilo.CIAN)
		elif pendiente and i != i_cerca:
			_r(ax - 2, ay + bote, 1, 1, Estilo.CIAN)
			_r(ax + 2, ay + bote, 1, 1, Estilo.CIAN)
			_r(ax - 1, ay + 1 + bote, 1, 1, Estilo.CIAN)
			_r(ax + 1, ay + 1 + bote, 1, 1, Estilo.CIAN)
			_r(ax, ay + 2 + bote, 1, 1, Estilo.CIAN)


func _dibujar_marcador() -> void:
	# franja de arriba: puntos, vidas, fase y tiempo
	_r(-4, -4, ANCHO + 8, 20, Estilo.TINTA)
	_r(-4, 15, ANCHO + 8, 1, Estilo.PETROLEO)
	_numero(puntos, 5, 5, 4, Estilo.CREMA, 2)
	for k in 3:
		if k < vidas:
			_sprite(CASCO, 54 + k * 8, 4, false, false)
		else:
			_r(55 + k * 8, 6, 3, 1, Estilo.TINTA_SUAVE)
	for k in 3:
		var bx: int = 142 + k * 13
		var hecho: bool = fase > k
		var actual: bool = fase == k
		_r(bx, 4, 9, 9, Estilo.CIAN_MEDIO if hecho else (Estilo.DORADO if actual else Estilo.TINTA_SUAVE))
		if not hecho and not actual:
			_r(bx + 1, 5, 7, 7, Estilo.TINTA)
		_letras(str(k + 1), bx + 3, 6, Estilo.TINTA if (hecho or actual) else Estilo.TINTA_SUAVE)
	# reloj
	var urge: bool = reloj <= 15.0 and fase < 3
	var c_reloj: Color = Estilo.CORAL if urge else Estilo.CREMA
	_r(290, 4, 5, 1, c_reloj)
	_r(289, 4, 1, 5, c_reloj)
	_r(295, 4, 1, 5, c_reloj)
	_r(290, 9, 5, 1, c_reloj)
	_r(292, 5, 1, 2, c_reloj)
	_r(293, 6, 1, 1, c_reloj)
	_numero(int(ceilf(reloj)), 2, 300, 4, c_reloj, 2)
	# franja de abajo: la mision en una linea, con sus teclas
	_r(-4, 166, ANCHO + 8, 18, Estilo.TINTA)
	_r(-4, 166, ANCHO + 8, 1, Estilo.PETROLEO)
	# La mision conserva su pictograma cuando desaparece el cartel inicial.
	var x: int = 18
	match fase:
		0:
			_r(6, 168, 5, 2, Estilo.DORADO)
			_r(8, 170, 1, 4, Estilo.CREMA)
			_r(13, 168, 1, 7, Estilo.PAPEL)
		1:
			_r(6, 168, 1, 7, Estilo.PAPEL)
			_r(7, 168, 7, 1, Estilo.PAPEL)
			_letras("→", 9, 170, Estilo.CIAN)
		2:
			_r(6, 171, 9, 1, Estilo.CIAN)
			_r(6, 168, 1, 7, Estilo.PAPEL)
			_r(14, 168, 1, 7, Estilo.PAPEL)
	if fase < 3:
		x = _tecla("←→", x, 167)
		x = _tecla("↑↓" if fase == 2 else "E", x, 167)
		_letras(MISIONES[fase], x + 3, 169, Estilo.PAPEL)
	else:
		_letras(MISIONES[3], (ANCHO - _ancho_letras(MISIONES[3])) / 2, 169, Estilo.CREMA)
	_tecla("ESC", ANCHO - 22, 167)


func _tecla(s: String, x: int, y: int) -> int:
	var ancho: int = _ancho_letras(s) + 4
	_r(x, y, ancho, 9, Estilo.CIAN)
	_r(x + 1, y + 1, ancho - 2, 7, Estilo.TINTA)
	_letras(s, x + 2, y + 2, Estilo.CIAN)
	return x + ancho + 3


func _dibujar_cartel() -> void:
	# pictograma y una linea: la mision se entiende mirando
	var ancho: int = 176
	var x: int = (ANCHO - ancho) / 2
	var y: int = 38
	_r(x - 1, y - 1, ancho + 2, 40, Estilo.DORADO)
	_r(x, y, ancho, 38, Estilo.TINTA)
	_letras("FASE %d/3" % (fase + 1), x + 34, y + 6, Estilo.DORADO)
	_letras(MISIONES[fase], x + 34, y + 19, Estilo.PAPEL)
	_tecla("↑↓" if fase == 2 else "E", x + 34 + _ancho_letras("FASE 1/3") + 8, y + 4)
	var px: int = x + 6
	var py: int = y + 8
	_r(px, py + 20, 24, 1, Estilo.PAPEL_SOMBRA)
	match fase:
		0:
			_r(px + 15, py + 4, 2, 16, Estilo.PAPEL)
			_r(px + 3, py + 1, 8, 5, Estilo.DORADO)
			_r(px + 6, py + 6, 2, 9, Estilo.CREMA)
			_letras("↓", px + 19, py + 9, Estilo.CIAN)
		1:
			_r(px + 3, py + 1, 2, 19, Estilo.PAPEL)
			_r(px + 5, py + 2, 12, 1, Estilo.PAPEL)
			_r(px + 5, py + 3, 12, 3, Estilo.CORAL)
			_r(px + 5, py + 6, 12, 3, Estilo.PAPEL)
			_letras("→", px + 18, py, Estilo.CIAN)
			_r(px + 22, py - 1, 1, 7, Estilo.CIAN)
		2:
			_r(px + 2, py + 7, 1, 13, Estilo.PAPEL)
			_r(px + 3, py + 7, 7, 5, Estilo.CORAL)
			_r(px + 14, py + 1, 1, 19, Estilo.PAPEL)
			_r(px + 15, py + 1, 7, 5, Estilo.DORADO)
			_letras("↑", px + 5, py, Estilo.CIAN)
			_letras("=", px + 9, py + 14, Estilo.CIAN)
