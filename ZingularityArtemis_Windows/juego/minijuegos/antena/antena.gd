extends "res://nucleo/minijuego.gd"

# RASTREO. Juego de accion de salon recreativo: un satelite cruza el arco del cielo sobre el paramo del
# Cotopaxi y la antena parabolica gira con izquierda y derecha. Mientras el haz toca al satelite bajan
# paquetes de datos; si se pierde, estatica. Mision: bajar la meta de paquetes en 3 pasadas.
#
# Lo real que se aprende jugando (sin cifras inventadas):
#   - un satelite parece cruzar mas rapido sobre la cabeza que cerca del horizonte (geometria del paso);
#   - un haz mas fino concentra la senal (baja el doble de paquetes) pero se escapa antes;
#   - la estacion Quito, al pie del Cotopaxi, opero de 1957 a 1981 (ficha estacion_cotopaxi). Las llamas junto a
#     la antena salen de la ficha estacion_llamas. Nunca se relaciona la estacion con el Apolo 11.
# Los numeros del juego (velocidades, anchos del haz, metas) son de juego, no del equipo historico.
#
# Todo se dibuja con _draw() en pixeles gordos: campo logico de 320 x 180 escalado x4 (1280 x 720).
# La simulacion va a paso fijo (1/120 s) alimentada con delta. El piloto (jugar_solo) mueve las mismas dos
# variables que las teclas, "mando" y "fino", y corre el reloj al doble para caber en las pruebas.

const E: int = 4
const ANCHO: int = 320
const ALTO: int = 180
const SUELO_Y: int = 154
const HUD_Y: int = 157
const PIVOTE: Vector2 = Vector2(160.0, 145.0)
const BORDE_Y: float = 130.0
const PASO_SIM: float = 1.0 / 120.0
const VMAX: float = 64.0
const ACEL: float = 150.0
const FRENO: float = 0.16
const LIMITE: float = 86.0
const VEL_PAQUETE: float = 160.0
const GRACIA: float = 0.2
const T_INTRO: float = 3.0
const T_PAUSA: float = 2.5
const T_FIN: float = 1.6
const HAZ: Array[float] = [8.0, 7.0, 6.0]
const HAZ_FINO: Array[float] = [3.0, 2.6, 2.2]
const CUOTAS: Array[int] = [45, 58, 70]
const PICO_VIENTO: Array[float] = [9.0, 13.0, 17.0]
# por dificultad y pasada: [segundos de cruce, y del apice, sentido, rafagas, pajaros, sprite]
const PLAN: Array = [
	[[24.0, 16.0, 1, 0, 0, "sat_a"], [21.0, 30.0, -1, 1, 1, "sat_b"], [18.0, 44.0, 1, 1, 1, "sat_c"]],
	[[22.0, 20.0, -1, 1, 1, "sat_a"], [19.0, 36.0, 1, 2, 1, "sat_b"], [16.0, 48.0, -1, 2, 2, "sat_c"]],
	[[20.0, 26.0, 1, 2, 1, "sat_a"], [17.0, 40.0, -1, 2, 2, "sat_b"], [14.5, 52.0, 1, 3, 2, "sat_c"]],
]

const GLIFOS: Dictionary = {
	"A": [".#.", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
	"C": [".##", "#..", "#..", "#..", ".##"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
	"E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
	"G": [".##", "#..", "#.#", "#.#", ".##"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
	"I": ["###", ".#.", ".#.", ".#.", "###"], "J": ["..#", "..#", "..#", "#.#", ".#."],
	"K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
	"M": ["#.#", "###", "###", "#.#", "#.#"], "N": ["##.", "#.#", "#.#", "#.#", "#.#"],
	"O": [".#.", "#.#", "#.#", "#.#", ".#."], "P": ["##.", "#.#", "##.", "#..", "#.."],
	"Q": [".#.", "#.#", "#.#", "###", ".##"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
	"S": [".##", "#..", ".#.", "..#", "##."], "T": ["###", ".#.", ".#.", ".#.", ".#."],
	"U": ["#.#", "#.#", "#.#", "#.#", "###"], "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
	"W": ["#.#", "#.#", "###", "###", "#.#"], "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
	"Y": ["#.#", "#.#", ".#.", ".#.", ".#."], "Z": ["###", "..#", ".#.", "#..", "###"],
	"0": ["###", "#.#", "#.#", "#.#", "###"], "1": [".#.", "##.", ".#.", ".#.", "###"],
	"2": ["###", "..#", "###", "#..", "###"], "3": ["###", "..#", ".##", "..#", "###"],
	"4": ["#.#", "#.#", "###", "..#", "..#"], "5": ["###", "#..", "###", "..#", "###"],
	"6": ["###", "#..", "###", "#.#", "###"], "7": ["###", "..#", "..#", ".#.", ".#."],
	"8": ["###", "#.#", "###", "#.#", "###"], "9": ["###", "#.#", "###", "..#", "###"],
	"/": ["..#", "..#", ".#.", "#..", "#.."], "-": ["...", "...", "###", "...", "..."],
	"+": ["...", ".#.", "###", ".#.", "..."], "!": [".#.", ".#.", ".#.", "...", ".#."],
	"<": ["..#", ".#.", "#..", ".#.", "..#"], ">": ["#..", ".#.", "..#", ".#.", "#.."],
	"x": ["...", "#.#", ".#.", "#.#", "..."], "^": [".#.", "###", "#.#", "...", "..."],
}

# mapas de caracteres: c crema, p papel, h papel en sombra, m cian medio, a cian, b brillo, d dorado,
# n naranja, r coral, e terracota, s tinta suave, t tinta, v verde, o petroleo
const SPRITES: Dictionary = {
	"sat_a": [
		"mmmm.ccc.mmmm",
		"mama.cpc.mama",
		"mmmmhcpchmmmm",
		"mama.cpc.mama",
		"mmmm.ccc.mmmm",
	],
	"sat_b": [
		"h.........h",
		".h..ccc..h.",
		"..hcpppch..",
		"...cpdpc...",
		"..hcpppch..",
		".h..ccc..h.",
		"h.........h",
	],
	"sat_c": [
		"....h....",
		"...ddd...",
		"mamdpdmam",
		"...ddd...",
	],
	"mini": [
		"mm.c.mm",
		"mmcpcmm",
		"mm.c.mm",
	],
	"condor_a": [
		"e.........e",
		"ee.......ee",
		".eee.p.eee.",
		"...eeeee...",
		".....e.....",
	],
	"condor_b": [
		"...........",
		".....p.....",
		".eeeeeeeee.",
		"ee...e...ee",
		"e.........e",
	],
	"llama_a": [
		"c.c......",
		"ccc......",
		".cc......",
		".cccccccc",
		".chcccchc",
		"..ccccccc",
		"..cc...cc",
		"..hc...hc",
	],
	"llama_b": [
		".........",
		".........",
		".........",
		"..ccccccc",
		".chcccchc",
		"cc.cccccc",
		"ccccc..cc",
		"c..hc..hc",
	],
	"caseta": [
		"....eeeeeeee....",
		"...eeeeeeeeee...",
		"..eeeeeeeeeeee..",
		"..hhhhhhhhhhhh..",
		"..hddhhhhhhddh..",
		"..hddhhsshhddh..",
		"..hhhhhsshhhhh..",
		"..hhhhhsshhhhh..",
	],
	"pedestal": [
		"..hhh..",
		"..hsh..",
		"..hsh..",
		"..hsh..",
		".hhshh.",
		".hsssh.",
		"hhssshh",
		"hsssssh",
	],
	"paquete": [
		"aaa",
		"aba",
		"aaa",
	],
	"reloj": [
		".ppp.",
		"p.p.p",
		"p.ppp",
		"p...p",
		".ppp.",
	],
}

# ------------------------------------------------------------------ estado del juego (lo leen las pruebas)
var antena: float = 0.0            # grados; 0 = cenit, positivo = derecha
var vel: float = 0.0               # grados por segundo
var mando: float = 0.0             # -1..1: lo ponen las teclas, el raton o el piloto
var fino: bool = false             # haz fino: lo pone E / Espacio o el piloto
var fase: String = "espera"        # espera, intro, pasada, pausa, fin
var t_fase: float = 0.0
var pasada: int = 0                # 0..2
var sat_pos: Vector2 = Vector2(-20.0, 80.0)
var sat_ang: float = -84.0
var sat_vel: float = 0.0           # grados por segundo, vistos desde la antena
var sat_fuera: bool = true         # true = no hay satelite sobre el horizonte
var lado: int = -1                 # por donde sale el proximo satelite: -1 izquierda, 1 derecha
var enlace: bool = false
var paquetes: int = 0
var cuota: int = 45
var por_pasada: Array[int] = [0, 0, 0]
var perdidos: int = 0
var comidos: int = 0
var t_visible: float = 0.0
var t_enlace: float = 0.0
var haz: float = 8.0
var haz_fino: float = 3.0

var _plan: Array = []
var _auto: int = 0
var _reloj: float = 1.0
var _acum: float = 0.0
var _anim: float = 0.0
var _emision: float = 0.0
var _sin_enlace: float = 0.0
var _estatica: float = 0.0
var _t_radio: float = 0.0
var _t_error: float = 0.0
var _empuje: float = 0.0
var _viento: float = 0.0
var _rafagas: Array = []           # [t0, duracion, pico con signo, avisada]
var _salidas_pajaro: Array = []    # segundos de la pasada en que sale cada pajaro
var _pajaros: Array = []           # [x, y0, velocidad, edad]
var _vuelo: Array = []             # paquetes en vuelo: [Vector2, es_fino]
var _chispas: Array = []           # [x, y, vx, vy, vida, color]
var _sacudida: float = 0.0
var _destello: float = 0.0
var _bote: float = 0.0
var _meta_t: float = -1.0
var _parpadeo_pasada: float = 0.0
var _pasada_floja: bool = false
var _azar: RandomNumberGenerator = RandomNumberGenerator.new()
var _ruido: RandomNumberGenerator = RandomNumberGenerator.new()
var _fondo: ImageTexture = null
var _tiras: Dictionary = {}
var _spr: Dictionary = {}
var _estrellas: Array[Vector2i] = []
var _suelo_oscuro: Color = Color("10181c")


# ------------------------------------------------------------------ contrato

func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	haz = HAZ[dificultad - 1]
	haz_fino = HAZ_FINO[dificultad - 1]
	cuota = int(parametros.get("cuota", CUOTAS[dificultad - 1]))
	_plan = PLAN[dificultad - 1]
	_azar.seed = 1957 + dificultad * 131 + int(parametros.get("semilla", 0))
	_compilar()
	_hornear_fondo()
	var primera: Array = _plan[0]
	lado = -int(primera[2])
	antena = 0.0
	fase = "espera"
	queue_redraw()


func _empezar() -> void:
	fase = "intro"
	t_fase = 0.0
	sonar("pulsar")


func _paso(delta: float) -> void:
	if _auto == 0:
		mando = eje_x()
		fino = Input.is_action_pressed("interactuar") or Input.is_action_pressed("saltar") or Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)
		if is_zero_approx(mando) and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
			# raton opcional: con el boton izquierdo la antena gira hacia el puntero, con la misma inercia
			var m: Vector2 = get_local_mouse_position() / float(E)
			if m.y < float(HUD_Y) and m.x >= 0.0 and m.x < float(ANCHO):
				var hacia: float = clampf(rad_to_deg(atan2(m.x - PIVOTE.x, maxf(PIVOTE.y - m.y, 1.0))), -LIMITE, LIMITE)
				mando = clampf((hacia - antena - vel * FRENO) / 4.0, -1.0, 1.0)
	_acum += delta * _reloj
	var tope: int = 960
	while _acum >= PASO_SIM and activo and tope > 0:
		_acum -= PASO_SIM
		tope -= 1
		_sim(PASO_SIM)
	if tope == 0:
		_acum = 0.0
	queue_redraw()


func jugar_solo(acierta: bool) -> void:
	# El piloto mira lo mismo que una persona (donde esta el satelite y hacia donde apunta el plato) y mueve
	# "mando" y "fino", igual que las teclas. Corre el reloj al doble: mismas reglas, la mitad de espera.
	_auto = 1 if acierta else -1
	_reloj = 2.0


# ------------------------------------------------------------------ simulacion a paso fijo

func _sim(dt: float) -> void:
	t_fase += dt
	_anim += dt
	if _auto != 0:
		_pilotar()
	_mover_antena(dt)
	match fase:
		"intro":
			if t_fase >= T_INTRO:
				_abrir_pasada(0)
		"pasada":
			_mover_satelite(dt)
			_soplar(dt)
			_soltar_pajaros()
			var datos: Array = _plan[pasada]
			var dura: float = datos[0]
			if t_fase >= dura:
				_cerrar_pasada()
		"pausa":
			if t_fase >= T_PAUSA:
				_abrir_pasada(pasada + 1)
		"fin":
			if t_fase >= T_FIN:
				_cerrar()
				return
	_enlazar(dt)
	_mover_paquetes(dt)
	_mover_pajaros(dt)
	_mover_chispas(dt)
	_sacudida = maxf(_sacudida - dt, 0.0)
	_destello = maxf(_destello - dt, 0.0)
	_bote = maxf(_bote - dt, 0.0)
	_t_error = maxf(_t_error - dt, 0.0)
	_parpadeo_pasada = maxf(_parpadeo_pasada - dt, 0.0)
	if _meta_t >= 0.0:
		_meta_t += dt


func _pilotar() -> void:
	var objetivo: float = float(lado) * 82.0
	var seguir: bool = not sat_fuera
	if _auto < 0 and seguir:
		# el piloto que falla solo sigue el principio de cada pasada y luego suelta el mando
		var datos: Array = _plan[pasada]
		var dura: float = datos[0]
		seguir = t_fase < dura * 0.12
		if not seguir:
			mando = 0.0
			fino = false
			return
	if seguir:
		objetivo = sat_ang + sat_vel * 0.10
	var falta: float = objetivo - antena - vel * FRENO
	mando = 0.0
	if absf(falta) > 1.0:
		mando = signf(falta)
	fino = _auto > 0 and not sat_fuera and absf(sat_ang - antena) < haz_fino * 0.9


func _mover_antena(dt: float) -> void:
	if absf(mando) > 0.05:
		vel = move_toward(vel, mando * VMAX, ACEL * dt)
	else:
		vel *= exp(-dt / FRENO)
	antena += (vel + _empuje) * dt
	if antena > LIMITE:
		antena = LIMITE
		vel = minf(vel, 0.0)
	elif antena < -LIMITE:
		antena = -LIMITE
		vel = maxf(vel, 0.0)


func _punto_sat(u: float, apice: float, sentido: int) -> Vector2:
	var recorrido: float = float(ANCHO) + 20.0
	var x: float = -10.0 + recorrido * u if sentido > 0 else float(ANCHO) + 10.0 - recorrido * u
	var k: float = (x - PIVOTE.x) / (float(ANCHO) * 0.5 + 10.0)
	return Vector2(x, (apice * 1.4 + 8.0) + (BORDE_Y - (apice * 1.4 + 8.0)) * k * k)


func _angulo(p: Vector2) -> float:
	return rad_to_deg(atan2(p.x - PIVOTE.x, PIVOTE.y - p.y))


func _abrir_pasada(n: int) -> void:
	pasada = n
	fase = "pasada"
	t_fase = 0.0
	var datos: Array = _plan[n]
	var dura: float = datos[0]
	var apice: float = datos[1]
	var sentido: int = datos[2]
	var n_rafagas: int = datos[3]
	var n_pajaros: int = datos[4]
	sat_pos = _punto_sat(0.0, apice, sentido)
	sat_ang = _angulo(sat_pos)
	sat_vel = 0.0
	sat_fuera = true
	lado = -sentido
	_rafagas.clear()
	for i in n_rafagas:
		var centro: float = dura * (0.25 + 0.55 * (float(i) + 0.5) / float(n_rafagas)) + _azar.randf_range(-0.8, 0.8)
		var signo: float = 1.0 if _azar.randf() < 0.5 else -1.0
		_rafagas.append([centro, 1.0, signo * PICO_VIENTO[dificultad - 1], false])
	_salidas_pajaro.clear()
	for i in n_pajaros:
		_salidas_pajaro.append(dura * (0.15 + 0.6 * (float(i) + 0.5) / float(n_pajaros)) + _azar.randf_range(-1.0, 1.0))
	sonar("salto")


func _mover_satelite(dt: float) -> void:
	var datos: Array = _plan[pasada]
	var dura: float = datos[0]
	var apice: float = datos[1]
	var sentido: int = datos[2]
	var u: float = clampf(t_fase / dura, 0.0, 1.0)
	sat_pos = _punto_sat(u, apice, sentido)
	var nuevo: float = _angulo(sat_pos)
	sat_vel = (nuevo - sat_ang) / dt
	sat_ang = nuevo
	sat_fuera = sat_pos.x < 0.0 or sat_pos.x > float(ANCHO)


func _cerrar_pasada() -> void:
	sat_fuera = true
	sat_vel = 0.0
	_empuje = 0.0
	_viento = 0.0
	_parpadeo_pasada = 1.2
	_pasada_floja = por_pasada[pasada] * 3 < cuota
	sonar("error" if _pasada_floja and paquetes < cuota else "ok")
	if pasada >= _plan.size() - 1:
		fase = "fin"
	else:
		fase = "pausa"
		var siguiente: Array = _plan[pasada + 1]
		lado = -int(siguiente[2])
	t_fase = 0.0


func _cerrar() -> void:
	var porcentaje: int = int(round(100.0 * t_enlace / maxf(t_visible, 0.01)))
	var pasadas: int = _plan.size()
	if paquetes >= cuota:
		terminar(true, float(paquetes), "Bajaste %d paquetes en %d pasadas (meta: %d). La estación Quito, al pie del Cotopaxi, rastreó naves de 1957 a 1981." % [paquetes, pasadas, cuota])
	elif porcentaje < 45:
		terminar(false, float(paquetes), "Bajaron %d de %d paquetes: el haz tocó al satélite solo el %d %% del tiempo. Espéralo donde sale y síguelo sin soltarlo." % [paquetes, cuota, porcentaje])
	else:
		terminar(false, float(paquetes), "Bajaron %d de %d paquetes: el enlace se cortó a ratos y %d se volvieron estática. Con el haz fino (E) bajan el doble." % [paquetes, cuota, perdidos + comidos])


func _soplar(dt: float) -> void:
	# rafagas del paramo: empujan el plato; se anuncian medio segundo antes con rayas de viento
	_empuje = 0.0
	var aviso: float = 0.0
	for r in _rafagas:
		var rafaga: Array = r
		var centro: float = rafaga[0]
		var dura: float = rafaga[1]
		var pico: float = rafaga[2]
		var x: float = (t_fase - centro) / (dura * 0.5)
		if absf(x) < 1.0:
			_empuje += pico * pow(cos(x * PI * 0.5), 2.0)
		var previo: float = (t_fase - (centro - dura * 0.5 - 0.6)) / (dura + 0.6)
		if previo > 0.0 and previo < 1.0:
			aviso = signf(pico) * minf(1.0, sin(previo * PI) * 1.6)
			if not bool(rafaga[3]):
				rafaga[3] = true
				sonar("pagina")
	_viento = move_toward(_viento, aviso, dt * 4.0)


func _soltar_pajaros() -> void:
	while not _salidas_pajaro.is_empty() and t_fase >= float(_salidas_pajaro[0]):
		_salidas_pajaro.pop_front()
		var desde_izquierda: bool = _azar.randf() < 0.5
		var rapidez: float = _azar.randf_range(20.0, 28.0) + float(dificultad) * 2.0
		_pajaros.append([-8.0 if desde_izquierda else float(ANCHO) + 8.0, _azar.randf_range(85.0, 122.0), rapidez if desde_izquierda else -rapidez, 0.0])


func _mover_pajaros(dt: float) -> void:
	var i: int = _pajaros.size() - 1
	while i >= 0:
		var p: Array = _pajaros[i]
		p[0] = float(p[0]) + float(p[2]) * dt
		p[3] = float(p[3]) + dt
		if float(p[0]) < -14.0 or float(p[0]) > float(ANCHO) + 14.0:
			_pajaros.remove_at(i)
		i -= 1


func _pos_pajaro(p: Array) -> Vector2:
	return Vector2(float(p[0]), float(p[1]) + 2.0 * sin(float(p[3]) * 2.2))


func _punta() -> Vector2:
	# extremo del alimentador: de ahi sale el haz y ahi llegan los paquetes
	var a: float = deg_to_rad(antena)
	return PIVOTE + Vector2(sin(a), -cos(a)) * 10.0


func _medio_haz() -> float:
	# el haz «toca» al satelite cuando el cono dibujado roza su cuerpo (3 px de medio ancho)
	var dist: float = maxf(PIVOTE.distance_to(sat_pos), 1.0)
	return (haz_fino if fino else haz) + rad_to_deg(atan(3.0 / dist))


func _enlazar(dt: float) -> void:
	var antes: bool = enlace
	enlace = false
	if not sat_fuera:
		enlace = absf(sat_ang - antena) <= _medio_haz()
		t_visible += dt
	_emision = maxf(_emision - dt, 0.0)
	if enlace:
		t_enlace += dt
		if not antes:
			_emision = maxf(_emision, 0.2)
			if _sin_enlace > 0.5:
				sonar("pulsar")
		_sin_enlace = 0.0
		_estatica = maxf(_estatica - dt * 4.0, 0.0)
		if _emision <= 0.0:
			_vuelo.append([sat_pos + Vector2(0.0, 3.0), fino])
			_emision = 0.25 if fino else 0.5
	elif not sat_fuera:
		_sin_enlace += dt
		_estatica = minf(_estatica + dt * 1.6, 1.0)
		_t_radio -= dt
		if _t_radio <= 0.0:
			_t_radio = 0.6
			sonar("radio")
		if _sin_enlace > GRACIA and not _vuelo.is_empty():
			# sin enlace, lo que venia bajando se vuelve estatica
			for v in _vuelo:
				var paquete: Array = v
				_reventar(paquete[0], Estilo.CORAL, 4)
			perdidos += _vuelo.size()
			_vuelo.clear()
			_sacudida = 0.18
			_quejarse()
	else:
		_estatica = maxf(_estatica - dt * 2.0, 0.0)


func _quejarse() -> void:
	if _t_error <= 0.0:
		_t_error = 0.9
		sonar("error")


func _mover_paquetes(dt: float) -> void:
	var destino: Vector2 = _punta()
	var i: int = _vuelo.size() - 1
	while i >= 0:
		var v: Array = _vuelo[i]
		var p: Vector2 = v[0]
		var falta: Vector2 = destino - p
		var comido: bool = false
		for pj in _pajaros:
			var b: Vector2 = _pos_pajaro(pj)
			if absf(p.x - b.x) < 5.5 and absf(p.y - b.y) < 3.5:
				comido = true
		if comido:
			_vuelo.remove_at(i)
			comidos += 1
			_reventar(p, Estilo.NARANJA, 5)
			_sacudida = 0.22
			_quejarse()
		elif falta.length() <= VEL_PAQUETE * dt + 2.0:
			_vuelo.remove_at(i)
			_recibir(destino)
		else:
			v[0] = p + falta.normalized() * VEL_PAQUETE * dt
		i -= 1


func _recibir(donde: Vector2) -> void:
	paquetes += 1
	por_pasada[pasada] += 1
	_bote = 0.12
	_reventar(donde, Estilo.BRILLO, 2)
	sonar("recoger" if paquetes % 5 == 0 else "tic")
	if paquetes == cuota:
		_meta_t = 0.0
		_destello = 0.3
		_sacudida = 0.25
		sonar("logro")
		for i in 18:
			_chispas.append([donde.x, donde.y, _azar.randf_range(-34.0, 34.0), _azar.randf_range(-70.0, -20.0), _azar.randf_range(0.5, 1.1), Estilo.DORADO if i % 2 == 0 else Estilo.BRILLO])


func _reventar(donde: Vector2, color: Color, cuantas: int) -> void:
	for i in cuantas:
		_chispas.append([donde.x, donde.y, _azar.randf_range(-26.0, 26.0), _azar.randf_range(-30.0, 8.0), _azar.randf_range(0.25, 0.55), color])
	while _chispas.size() > 90:
		_chispas.pop_front()


func _mover_chispas(dt: float) -> void:
	var i: int = _chispas.size() - 1
	while i >= 0:
		var c: Array = _chispas[i]
		c[0] = float(c[0]) + float(c[2]) * dt
		c[1] = float(c[1]) + float(c[3]) * dt
		c[3] = float(c[3]) + 90.0 * dt
		c[4] = float(c[4]) - dt
		if float(c[4]) <= 0.0:
			_chispas.remove_at(i)
		i -= 1


# ------------------------------------------------------------------ preparacion del dibujo

func _tintas() -> Dictionary:
	return {
		"c": Estilo.CREMA, "p": Estilo.PAPEL, "h": Estilo.PAPEL_SOMBRA, "m": Estilo.CIAN_MEDIO, "a": Estilo.CIAN,
		"b": Estilo.BRILLO, "d": Estilo.DORADO, "n": Estilo.NARANJA, "r": Estilo.CORAL, "e": Estilo.TERRACOTA,
		"s": Estilo.TINTA_SUAVE, "t": Estilo.TINTA, "v": Estilo.VERDE, "o": Estilo.PETROLEO,
	}


func _compilar() -> void:
	# letras y sprites pasan a tiras horizontales: menos rectangulos por cuadro
	for clave in GLIFOS:
		var filas: Array = GLIFOS[clave]
		var tiras: Array = []
		for y in filas.size():
			var fila: String = filas[y]
			var x: int = 0
			while x < fila.length():
				if fila[x] == "#":
					var x0: int = x
					while x < fila.length() and fila[x] == "#":
						x += 1
					tiras.append(Vector3i(x0, y, x - x0))
				else:
					x += 1
		_tiras[clave] = tiras
	var tintas: Dictionary = _tintas()
	for nombre in SPRITES:
		var filas: Array = SPRITES[nombre]
		var tiras: Array = []
		for y in filas.size():
			var fila: String = filas[y]
			var x: int = 0
			while x < fila.length():
				var ch: String = fila[x]
				if tintas.has(ch):
					var x0: int = x
					while x < fila.length() and fila[x] == ch:
						x += 1
					var color: Color = tintas[ch]
					tiras.append([x0, y, x - x0, color])
				else:
					x += 1
		var primera: String = filas[0]
		_spr[nombre] = {"tiras": tiras, "ancho": primera.length(), "alto": filas.size()}


func _estampar(img: Image, nombre: String, x: int, y: int) -> void:
	var s: Dictionary = _spr[nombre]
	var tiras: Array = s["tiras"]
	for t in tiras:
		var tira: Array = t
		var color: Color = tira[3]
		img.fill_rect(Rect2i(x + int(tira[0]), y + int(tira[1]), int(tira[2]), 1), color)


func _hornear_fondo() -> void:
	# cielo de atardecer en bandas, la Luna «sonriente» del ecuador, el Cotopaxi nevado, el paramo y la caseta
	var img: Image = Image.create(ANCHO, ALTO, false, Image.FORMAT_RGBA8)
	var bandas: Array[Color] = [
		Color("121a1f"), Color("17222a"), Estilo.NOCHE, Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.22),
		Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.42), Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.66),
		Estilo.PETROLEO.lerp(Estilo.NARANJA, 0.22), Estilo.PETROLEO.lerp(Estilo.NARANJA, 0.5),
	]
	for y in SUELO_Y:
		var t: float = pow(float(y) / float(SUELO_Y), 1.7) * float(bandas.size() - 1)
		for x in ANCHO:
			var idx: int = clampi(int(t + (0.5 if ((x + y) & 1) == 0 else 0.0)), 0, bandas.size() - 1)
			img.set_pixel(x, y, bandas[idx])
	# estrellas fijas (las que titilan se dibujan aparte)
	var azar: RandomNumberGenerator = RandomNumberGenerator.new()
	azar.seed = 3650
	for i in 46:
		var p: Vector2i = Vector2i(azar.randi_range(2, ANCHO - 3), azar.randi_range(12, 112))
		if i < 12:
			_estrellas.append(p)
		else:
			img.set_pixel(p.x, p.y, Estilo.PAPEL.lerp(Estilo.NOCHE, azar.randf_range(0.25, 0.6)))
	# Luna creciente con el borde iluminado hacia abajo y luz cenicienta
	var luna: Vector2 = Vector2(278.0, 34.0)
	for y in range(28, 41):
		for x in range(272, 285):
			var q: Vector2 = Vector2(float(x), float(y))
			if q.distance_to(luna) <= 5.2:
				var iluminada: bool = q.distance_to(luna + Vector2(0.0, -2.6)) > 5.4
				img.set_pixel(x, y, Estilo.CREMA if iluminada else Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.5))
	# sierra lejana a la derecha
	var sierra: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.3)
	for x in range(130, ANCHO):
		var cima: int = int(145.0 + 3.5 * sin(float(x) * 0.07) + 2.0 * sin(float(x) * 0.19 + 1.0))
		for y in range(cima, SUELO_Y):
			img.set_pixel(x, y, sierra)
	# Cotopaxi: cono concavo con crater y nieve
	var monte: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.12)
	var monte_luz: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.3)
	for x in range(0, 150):
		var d: float = maxf(absf(float(x) - 58.0) - 3.0, 0.0) / 86.0
		if d >= 1.0:
			continue
		var cima: int = int(float(SUELO_Y) - 50.0 * pow(1.0 - d, 1.45))
		var nieve: int = 120 + ((x * 7) % 5) - (2 if x < 58 else 0)
		for y in range(cima, SUELO_Y):
			var color: Color = monte_luz if x < 58 else monte
			if y < nieve:
				color = Estilo.CREMA if x < 60 else Estilo.PAPEL_SOMBRA.lerp(Estilo.PETROLEO, 0.35)
				if y == cima and x < 60:
					color = Estilo.PAPEL
			img.set_pixel(x, y, color)
	# paramo
	img.fill_rect(Rect2i(0, SUELO_Y, ANCHO, HUD_Y - SUELO_Y), Estilo.TINTA)
	img.fill_rect(Rect2i(0, SUELO_Y, ANCHO, 1), Estilo.VERDE)
	for i in 70:
		var x: int = azar.randi_range(0, ANCHO - 1)
		var y: int = azar.randi_range(SUELO_Y + 1, HUD_Y - 2)
		img.set_pixel(x, y, Estilo.VERDE.lerp(Estilo.TINTA, azar.randf_range(0.2, 0.6)))
	for i in 26:
		var x: int = azar.randi_range(2, ANCHO - 3)
		if absi(x - int(PIVOTE.x)) < 8:
			continue
		var color: Color = Estilo.DORADO.lerp(Estilo.TINTA, 0.35) if i % 3 == 0 else Estilo.VERDE
		img.set_pixel(x, SUELO_Y - 1, color)
		img.set_pixel(x + 1, SUELO_Y - 2 if i % 2 == 0 else SUELO_Y - 1, color)
	_estampar(img, "caseta", 112, SUELO_Y - 8)
	_estampar(img, "pedestal", int(PIVOTE.x) - 3, SUELO_Y - 8)
	# franja del marcador
	img.fill_rect(Rect2i(0, HUD_Y, ANCHO, ALTO - HUD_Y), _suelo_oscuro)
	img.fill_rect(Rect2i(0, HUD_Y, ANCHO, 1), Estilo.PETROLEO)
	_fondo = ImageTexture.create_from_image(img)


# ------------------------------------------------------------------ dibujo

func _r(x: int, y: int, w: int, h: int, color: Color) -> void:
	draw_rect(Rect2(x * E, y * E, w * E, h * E), color)


func _px(p: Vector2, color: Color) -> void:
	draw_rect(Rect2(floorf(p.x + 0.5) * E, floorf(p.y + 0.5) * E, E, E), color)


func _sprite(nombre: String, x: int, y: int, plano: Color = Color(0, 0, 0, 0)) -> void:
	var s: Dictionary = _spr[nombre]
	var tiras: Array = s["tiras"]
	for t in tiras:
		var tira: Array = t
		var color: Color = tira[3]
		if plano.a > 0.0:
			color = plano
		draw_rect(Rect2((x + int(tira[0])) * E, (y + int(tira[1])) * E, int(tira[2]) * E, E), color)


func _sprite_centrado(nombre: String, centro: Vector2, plano: Color = Color(0, 0, 0, 0)) -> void:
	var s: Dictionary = _spr[nombre]
	var ancho: int = s["ancho"]
	var alto: int = s["alto"]
	_sprite(nombre, int(floorf(centro.x + 0.5)) - ancho / 2, int(floorf(centro.y + 0.5)) - alto / 2, plano)


func _texto(contenido: String, x: int, y: int, color: Color, esc: int = 1) -> void:
	var cx: int = x
	for i in contenido.length():
		var ch: String = contenido[i]
		if _tiras.has(ch):
			var tiras: Array = _tiras[ch]
			for t in tiras:
				var tira: Vector3i = t
				draw_rect(Rect2((cx + tira.x * esc) * E, (y + tira.y * esc) * E, tira.z * esc * E, esc * E), color)
		cx += 4 * esc


func _ancho_texto(contenido: String, esc: int = 1) -> int:
	return contenido.length() * 4 * esc - esc


func _texto_centrado(contenido: String, cx: int, y: int, color: Color, esc: int = 1) -> void:
	_texto(contenido, cx - _ancho_texto(contenido, esc) / 2, y, color, esc)


func _plato(p: Vector2, grados: float, punta: Color) -> void:
	var a: float = deg_to_rad(grados)
	var d: Vector2 = Vector2(sin(a), -cos(a))
	var l: Vector2 = Vector2(cos(a), sin(a))
	for i in 3:
		_px(p + d * float(i), Estilo.TINTA_SUAVE)
	var s: float = -8.0
	while s <= 8.0:
		var f: float = 2.0 + s * s / 13.0
		_px(p + l * s + d * (f - 1.0), Estilo.PAPEL_SOMBRA)
		_px(p + l * s + d * f, Estilo.CREMA)
		s += 0.5
	_px(p + l * 8.0 + d * 6.9, Estilo.PAPEL)
	_px(p - l * 8.0 + d * 6.9, Estilo.PAPEL)
	for i in range(3, 10):
		_px(p + d * float(i), Estilo.PAPEL_SOMBRA)
	_px(p + d * 10.0, punta)


func _rayo(desde: Vector2, grados: float, color: Color, cada: int, corrimiento: int) -> void:
	var a: float = deg_to_rad(grados)
	var d: Vector2 = Vector2(sin(a), -cos(a))
	for r in range(2, ANCHO):
		var q: Vector2 = desde + d * float(r)
		if q.y < 0.0 or q.x < 0.0 or q.x >= float(ANCHO) or q.y >= float(SUELO_Y - 1):
			break
		if (r + corrimiento) % cada == 0:
			_px(q, color)


func _marco(x: int, y: int, w: int, h: int, fondo: Color, borde: Color) -> void:
	_r(x + 1, y, w - 2, h, fondo)
	_r(x, y + 1, w, h - 2, fondo)
	_r(x + 1, y, w - 2, 1, borde)
	_r(x + 1, y + h - 1, w - 2, 1, borde)
	_r(x, y + 1, 1, h - 2, borde)
	_r(x + w - 1, y + 1, 1, h - 2, borde)


func _tecla_dibujada(simbolo: String, x: int, y: int) -> void:
	_marco(x, y, 7, 9, Estilo.PAPEL, Estilo.PAPEL_SOMBRA)
	_texto(simbolo, x + 2, y + 2, Estilo.TINTA)


func _draw() -> void:
	if _fondo == null:
		return
	var corrida: Vector2 = Vector2.ZERO
	if _sacudida > 0.0:
		corrida = Vector2(float(int(_anim * 40.0) % 3 - 1), float(int(_anim * 53.0) % 3 - 1)) * float(E)
	draw_texture_rect(_fondo, Rect2(0, 0, ANCHO * E, ALTO * E), false)
	draw_set_transform(corrida)
	# estrellas que titilan despacio
	for i in _estrellas.size():
		var e: Vector2i = _estrellas[i]
		var fuerza: float = 0.55 + 0.4 * sin(_anim * 0.9 + float(i) * 1.7)
		_r(e.x, e.y, 1, 1, Color(Estilo.PAPEL, fuerza))
	_dibujar_arco()
	_dibujar_viento()
	_dibujar_haz()
	_dibujar_satelite()
	# paquetes que bajan
	for v in _vuelo:
		var paquete: Array = v
		var p: Vector2 = paquete[0]
		var es_fino: bool = paquete[1]
		var px: int = int(floorf(p.x + 0.5))
		var py: int = int(floorf(p.y + 0.5))
		_r(px - 1, py - 1, 3, 3, Estilo.DORADO if es_fino else Estilo.CIAN)
		_r(px, py, 1, 1, Estilo.BRILLO)
	# condores
	for pj in _pajaros:
		var pajaro: Array = pj
		var b: Vector2 = _pos_pajaro(pajaro)
		_sprite_centrado("condor_a" if int(float(pajaro[3]) * 3.0) % 2 == 0 else "condor_b", b)
	# llamas del paramo: levantan la cabeza con la estatica
	var alerta: bool = _estatica > 0.5
	_sprite("llama_a" if alerta or int(_anim / 2.6) % 2 == 0 else "llama_b", 208, SUELO_Y - 7)
	_sprite("llama_a" if alerta or int(_anim / 3.4 + 0.5) % 2 == 1 else "llama_b", 240, SUELO_Y - 6, Color(0, 0, 0, 0))
	# antena
	var punta: Color = Estilo.CIAN_MEDIO
	if enlace:
		punta = Estilo.BRILLO if int(_anim * 8.0) % 2 == 0 else Estilo.CIAN
	_plato(PIVOTE, antena, punta)
	# chispas
	for c in _chispas:
		var chispa: Array = c
		var color: Color = chispa[5]
		_r(int(floorf(float(chispa[0]))), int(floorf(float(chispa[1]))), 1, 1, Color(color, clampf(float(chispa[4]) * 3.0, 0.0, 1.0)))
	_dibujar_estatica()
	_dibujar_carteles()
	draw_set_transform(Vector2.ZERO)
	_dibujar_marcador()
	if _destello > 0.0:
		_r(0, 0, ANCHO, ALTO, Color(Estilo.BRILLO, 0.4 * _destello / 0.3))
	draw_set_transform(Vector2.ZERO)


func _dibujar_arco() -> void:
	# el arco punteado anuncia por donde cruza el satelite de esta pasada (o de la siguiente)
	var n: int = pasada
	if fase == "espera" or fase == "intro":
		n = 0
	elif fase == "pausa":
		n = pasada + 1
	elif fase == "fin":
		return
	var datos: Array = _plan[n]
	var apice: float = datos[1]
	var sentido: int = datos[2]
	var color: Color = Color(Estilo.PETROLEO, 0.75 if fase == "pasada" else 0.5)
	for i in 51:
		if (fase != "pasada") and int(_anim * 6.0 + float(i)) % 3 == 0:
			continue
		var q: Vector2 = _punto_sat(float(i) / 50.0, apice, sentido)
		if q.x >= 0.0 and q.x < float(ANCHO):
			_px(q, color)
	if fase == "pausa" or fase == "intro":
		# flecha: por aqui sale
		var x: int = 4 if lado < 0 else ANCHO - 11
		if int(_anim * 3.0) % 2 == 0:
			_texto("^", x, 116, Estilo.CIAN, 2)


func _dibujar_viento() -> void:
	if absf(_viento) < 0.05:
		return
	var alturas: Array[int] = [38, 60, 80, 99, 116, 133, 148]
	for i in alturas.size():
		var x: float = fposmod(float(i) * 47.0 + _anim * 110.0 * signf(_viento), float(ANCHO + 30)) - 15.0
		_r(int(x), alturas[i], 5 + (i % 3) * 2, 1, Color(Estilo.PAPEL, 0.4 * absf(_viento)))


func _dibujar_haz() -> void:
	if fase == "espera":
		return
	var desde: Vector2 = _punta()
	var medio: float = haz_fino if fino else haz
	var color: Color = Color(Estilo.CIAN_MEDIO, 0.55)
	var cada: int = 5
	var corrimiento: int = 0
	if enlace:
		color = Estilo.BRILLO if fino else Estilo.CIAN
		cada = 3
		corrimiento = int(_anim * 24.0)
	elif fino:
		color = Color(Estilo.BRILLO, 0.6)
	_rayo(desde, antena - medio, color, cada, corrimiento)
	_rayo(desde, antena + medio, color, cada, corrimiento)
	if enlace:
		# linea de enlace hasta el satelite
		var hacia: Vector2 = sat_pos - desde
		var largo: int = int(hacia.length())
		var d: Vector2 = hacia.normalized()
		for r in range(3, largo - 4):
			if (r + corrimiento) % 4 == 0:
				_px(desde + d * float(r), Color(Estilo.CIAN, 0.4))


func _dibujar_satelite() -> void:
	if fase != "pasada" or sat_pos.x < -8.0 or sat_pos.x > float(ANCHO) + 8.0:
		return
	var datos: Array = _plan[pasada]
	var nombre: String = datos[5]
	_sprite_centrado(nombre, sat_pos)
	if enlace:
		# mira de enganche
		var cx: int = int(floorf(sat_pos.x + 0.5))
		var cy: int = int(floorf(sat_pos.y + 0.5))
		var a: int = 9 + (1 if _emision > 0.38 else 0)
		var b: int = 6 + (1 if _emision > 0.38 else 0)
		var color: Color = Estilo.DORADO if fino else Estilo.CIAN
		for sx: int in [-1, 1]:
			for sy: int in [-1, 1]:
				_r(cx + sx * a - (1 if sx > 0 else 0), cy + sy * b, 2, 1, color)
				_r(cx + sx * a, cy + sy * b - (1 if sy > 0 else 0), 1, 2, color)


func _dibujar_estatica() -> void:
	if _estatica <= 0.02:
		return
	_ruido.seed = int(_anim * 10.0) + 77
	for i in int(_estatica * 34.0):
		var x: int = _ruido.randi_range(0, ANCHO - 3)
		var y: int = _ruido.randi_range(0, SUELO_Y - 2)
		_r(x, y, 1 + _ruido.randi_range(0, 2), 1, Color(Estilo.PAPEL, 0.16 + 0.22 * _ruido.randf()))


func _dibujar_carteles() -> void:
	var fondo: Color = Color(_suelo_oscuro, 0.94)
	if fase == "intro":
		# la mision: pictograma y una linea
		_marco(66, 24, 188, 60, fondo, Estilo.CIAN_MEDIO)
		_sprite("sat_a", 98, 30)
		for i in 4:
			var t: float = fposmod(_anim * 0.9 + float(i) * 0.25, 1.0)
			var q: Vector2 = Vector2(116.0, 34.0).lerp(Vector2(194.0, 41.0), t)
			_r(int(q.x) - 1, int(q.y) - 1, 3, 3, Estilo.CIAN)
			_r(int(q.x), int(q.y), 1, 1, Estilo.BRILLO)
		_plato(Vector2(210.0, 46.0), -66.0, Estilo.BRILLO)
		_texto_centrado("BAJA %d PAQUETES EN %d PASADAS" % [cuota, _plan.size()], 160, 54, Estilo.PAPEL)
		var x: int = 102
		_tecla_dibujada("<", x, 66)
		_tecla_dibujada(">", x + 9, 66)
		_texto("GIRA", x + 19, 68, Estilo.CREMA)
		_tecla_dibujada("E", x + 44, 66)
		_texto("HAZ FINO x2", x + 54, 68, Estilo.DORADO)
	elif fase == "pasada" and t_fase < 1.6:
		_texto_centrado("PASADA %d" % (pasada + 1), 160, 20, Estilo.CREMA, 2)
	elif fase == "pausa":
		_texto_centrado("+%d" % por_pasada[pasada], 160, 22, Estilo.CORAL if _pasada_floja and paquetes < cuota else Estilo.CIAN, 3)
		_texto_centrado("PASADA %d" % (pasada + 2), 160, 44, Estilo.CREMA, 2)
	elif fase == "fin":
		_marco(82, 32, 156, 40, fondo, Estilo.DORADO if paquetes >= cuota else Estilo.CORAL)
		if paquetes >= cuota:
			_texto_centrado("META CUMPLIDA", 160, 39, Estilo.DORADO, 2)
			_texto_centrado("%d PAQUETES" % paquetes, 160, 57, Estilo.PAPEL)
		else:
			_texto_centrado("FALTARON %d" % (cuota - paquetes), 160, 39, Estilo.CORAL, 2)
			_texto_centrado("%d DE %d PAQUETES" % [paquetes, cuota], 160, 57, Estilo.PAPEL)
	if _meta_t >= 0.0 and _meta_t < 1.6 and fase != "fin" and int(_meta_t * 6.0) % 2 == 0:
		_texto_centrado("META!", 160, 26, Estilo.DORADO, 3)


func _dibujar_marcador() -> void:
	var y0: int = HUD_Y + 4
	_sprite("paquete", 4, 5)
	_texto("BAJA %d PAQUETES EN 3 PASADAS" % cuota, 10, 5, Estilo.PAPEL)
	_tecla_dibujada("<", 218, 4)
	_tecla_dibujada(">", 227, 4)
	_tecla_dibujada("E", 246, 4)
	_texto("x2", 256, 6, Estilo.DORADO)
	_texto("ESC", 300, 6, Estilo.PAPEL_SOMBRA)
	# paquetes: cuenta grande y meta pequena
	_sprite("paquete", 4, y0 + 3)
	var sube: int = 1 if _bote > 0.0 else 0
	_texto("%03d" % paquetes, 10, y0 - sube, Estilo.BRILLO if _bote > 0.0 else Estilo.PAPEL, 2)
	var logrado: bool = paquetes >= cuota
	_texto("/%03d" % cuota, 35, y0 + 5, Estilo.DORADO if logrado else Estilo.PAPEL_SOMBRA)
	# barra de avance hacia la meta
	_r(53, y0 + 1, 34, 3, Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.5))
	_r(53, y0 + 1, int(34.0 * clampf(float(paquetes) / float(maxi(cuota, 1)), 0.0, 1.0)), 3, Estilo.DORADO if logrado else Estilo.CIAN_MEDIO)
	# las pasadas: tres satelites con lo que bajo cada una
	for i in _plan.size():
		var x: int = 112 + i * 24
		var color: Color = Estilo.PAPEL_SOMBRA
		var hecha: bool = i < pasada or (i == pasada and (fase == "pausa" or fase == "fin"))
		var actual: bool = i == pasada and fase == "pasada"
		if hecha:
			color = Estilo.TINTA_SUAVE
			if i == pasada and _parpadeo_pasada > 0.0 and int(_parpadeo_pasada * 5.0) % 2 == 1:
				color = Estilo.CORAL if _pasada_floja else Estilo.BRILLO
		if actual:
			_sprite("mini", x, y0)
			_r(x, y0 + 4, 7, 1, Estilo.CIAN)
		else:
			_sprite("mini", x, y0, color)
		if hecha or actual:
			_texto("%02d" % mini(por_pasada[i], 99), x, y0 + 6, Estilo.PAPEL if actual else Estilo.PAPEL_SOMBRA)
	# senal: cinco barras
	var nivel: int = 0
	if enlace:
		nivel = 3 + int(round(2.0 * (1.0 - absf(sat_ang - antena) / maxf(_medio_haz(), 0.1))))
	for i in 5:
		var alto: int = 2 + i * 2
		var color: Color = Estilo.NOCHE.lerp(Estilo.PETROLEO, 0.5)
		if i < nivel:
			color = Estilo.DORADO if fino else Estilo.CIAN
		elif not sat_fuera and not enlace and _ruido.randf() < 0.3:
			color = Estilo.CORAL
		_r(198 + i * 4, y0 + 10 - alto, 3, alto, color)
	# haz ancho o fino
	var claro: Color = Estilo.DORADO if fino else Estilo.CIAN_MEDIO
	var abre: int = 1 if fino else 3
	for i in 5:
		var mitad: int = int(round(float(abre) * float(4 - i) / 4.0))
		_r(242 - mitad, y0 + 2 + i * 2, 1, 2, claro)
		_r(242 + mitad, y0 + 2 + i * 2, 1, 2, claro)
	_texto("x2" if fino else "x1", 248, y0 + 5, claro)
	# reloj de la pasada
	_sprite("reloj", 284, y0 + 3)
	var segundos: int = 0
	if fase == "pasada":
		var datos: Array = _plan[pasada]
		var dura: float = datos[0]
		segundos = int(ceil(dura - t_fase))
	elif fase == "intro" or fase == "espera":
		var primera: Array = _plan[0]
		segundos = int(ceil(float(primera[0])))
	elif fase == "pausa":
		var siguiente: Array = _plan[pasada + 1]
		segundos = int(ceil(float(siguiente[0])))
	var urgente: bool = fase == "pasada" and segundos <= 5 and paquetes < cuota
	_texto("%02d" % segundos, 292, y0, Estilo.CORAL if urgente else Estilo.PAPEL, 2)
