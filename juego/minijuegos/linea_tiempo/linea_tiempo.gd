extends "res://nucleo/minijuego.gd"

# Escalinata cenital: mundo en pixeles logicos, +y sube por el cerro.
# Las fechas se extraen de las fichas; velocidades y distancias son reglas arcade.
const ANCHO: float = 320.0
const ALTO: float = 180.0
const PRIMERA_FILA: float = 65.0
const PASO_FILA: float = 80.0
const DT: float = 1.0 / 120.0
const COLUMNAS: Array[float] = [70.0, 160.0, 250.0]
const FICHAS: Array[String] = ["observatorio_quito", "estacion_cotopaxi", "disco_apolo11", "apolo_soyuz_1975", "sts2_despedida", "estacion_entrega", "exa_2007", "pegaso_lanzamiento", "acuerdos_artemisa"]
const NOMBRES: Array[String] = ["OBSERVATORIO", "ESTACION QUITO", "DISCO LUNAR", "APOLO SOYUZ", "DESPEDIDA STS2", "ENTREGA", "NACE EXA", "PEGASO", "ACUERDOS"]
const ICONOS: Array = [
	["...###...", "..#####..", ".#######.", ".##...##.", ".##...##.", "#########", "#.#.#.#.#"],
	["#........", ".#.....#.", "..#...#..", "...###...", "....#....", "...###...", "..#...#.."],
	["..#####..", ".#######.", "###...###", "###.#.###", "###...###", ".#######.", "..#####.."],
	["##.....##", "###...###", "..##.##..", "...###...", "..##.##..", "###...###", "##.....##"],
	["....#....", "...###...", "...###...", "..#####..", ".#######.", "###.#.###", "...#.#..."],
	["#.......#", "###...###", "..#####..", "...###...", "..#####..", "###...###", "#.......#"],
	["....#....", "..#.#.#..", "...###...", "#########", "...###...", "..#.#.#..", "....#...."],
	["##.....##", "##..#..##", "#########", "##.###.##", "#########", "##..#..##", "##.....##"],
	["..#####..", "..#.#.#..", "..#####..", "..#.#.#..", "..#####..", "..#.#.#..", "..#####.."]
]
const CHICA: Array[String] = ["..hhh..", ".hhhhh.", ".hpph..", "..ppp..", "..ccc..", ".ccccc.", "p.ccc.p", "..jjj..", "..j.j..", ".jj.jj."]
const COCO: Array[String] = ["..###..", ".#####.", "##.#.##", "#######", ".#####.", "..###.."]
const IGUANA: Array[String] = [".....#.....", "....###....", "..#######.#", "###########", "..#.#..#...", ".#..#...#.."]
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


var hitos: Array[Dictionary] = []
var placas: Array[Dictionary] = []
var peligros: Array[Dictionary] = []
var particulas: Array[Dictionary] = []
var jugadora: Vector2 = Vector2(160, 0)
var velocidad: Vector2 = Vector2.ZERO
var mando: Vector2 = Vector2.ZERO
var siguiente: int = 0
var vidas: int = 3
var puntos: int = 0
var fase: int = 0 # 0 pictograma, 1 jugando, 2 final
var reloj: float = 0.0
var limite: float = 90.0
var rapidez: float = 76.0
var radio_placa: float = 14.0
var salto: float = 0.0
var altura: float = 0.0
var inmune: float = 0.0
var destello: float = 0.0
var sacudida: float = 0.0
var descanso: float = 0.0
var aviso: String = ""
var aviso_t: float = 0.0
var final_t: float = 0.0
var gana: bool = false
var causa: String = ""
var _auto: int = 0
var _pulso: bool = false
var _acum: float = 0.0
var _intro: float = 0.0
var _nuevo_peligro: float = 2.7
var _azar: RandomNumberGenerator = RandomNumberGenerator.new()

func _init() -> void:
	pantalla_completa = true

func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	limite = [100.0, 90.0, 80.0][dificultad - 1]
	radio_placa = [16.0, 13.0, 10.0][dificultad - 1]
	_azar.seed = int(parametros.get("semilla", 7319 + dificultad))
	# Busca el primer anio de cuatro cifras en texto, luego en fuente (disco).
	var expresion: RegEx = RegEx.new()
	expresion.compile("(?:18|19|20)[0-9]{2}")
	for id in FICHAS:
		var ficha: Dictionary = Juego.ficha(id)
		if ficha.is_empty():
			continue
		var resultado: RegExMatch = expresion.search(str(ficha.get("texto", "")))
		if resultado == null:
			resultado = expresion.search(str(ficha.get("fuente", "")))
		if id == "estacion_entrega":
			var fechas: Array[RegExMatch] = expresion.search_all(str(ficha.get("texto", "")))
			if not fechas.is_empty():
				resultado = fechas.back()
		if resultado != null:
			hitos.append({"id": id, "anio": int(resultado.get_string()), "icono": FICHAS.find(id)})
	hitos.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return int(a["anio"]) < int(b["anio"]))
	for fila in hitos.size():
		var columna: int = (fila * 2 + 1) % 3
		for c in 3:
			var indice: int = fila if c == columna else (fila + 1 + (c if c < columna else c - 1)) % hitos.size()
			placas.append({"fila": fila, "columna": c, "hito": indice, "pos": Vector2(COLUMNAS[c], PRIMERA_FILA + fila * PASO_FILA), "revelada": false})
	queue_redraw()

func _empezar() -> void:
	fase = 0
	sonar("radio")

func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1

func _input(evento: InputEvent) -> void:
	if activo and _auto == 0 and (evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar")):
		_pulso = true
		get_viewport().set_input_as_handled()

func _paso(delta: float) -> void:
	_acum += delta
	while _acum >= DT and activo:
		_acum -= DT
		if _auto != 0:
			_piloto()
		else:
			mando = Vector2(eje_x(), eje_y()).limit_length()
		_tic(DT)
	queue_redraw()

func _tic(dt: float) -> void:
	_animar(dt)
	if fase == 0:
		_intro += dt
		_pulso = false
		if _intro >= 2.0:
			fase = 1
		return
	if fase == 2:
		final_t += dt
		if final_t >= 1.3:
			terminar(gana, puntos, causa)
		return
	reloj += dt
	if reloj >= limite:
		_final(false, "Se acabó el tiempo antes de completar los nueve hitos en orden.")
		return
	if descanso > 0.0:
		descanso -= dt
		_pulso = false
		return
	var pulsado: bool = _pulso
	_pulso = false
	if pulsado and salto <= 0.0:
		salto = 0.75
		sonar("salto")
	velocidad = velocidad.move_toward(mando * rapidez, dt * 320.0)
	jugadora += velocidad * dt
	jugadora.x = clampf(jugadora.x, 12.0, ANCHO - 12.0)
	var cima: float = PRIMERA_FILA + siguiente * PASO_FILA
	jugadora.y = clampf(jugadora.y, maxf(-8.0, cima - 100.0), cima + 12.0)
	if salto > 0.0:
		salto = maxf(0.0, salto - dt)
		altura = sin(PI * salto / 0.75) * 14.0
		if salto <= 0.0:
			altura = 0.0
			_aterrizar()
	if fase != 1 or descanso > 0.0:
		return
	_nuevo_peligro -= dt
	if _nuevo_peligro <= 0.0:
		_nuevo_peligro = [4.2, 3.1, 2.4][dificultad - 1]
		var coco: bool = _azar.randf() < 0.6
		var lado: int = -1 if _azar.randf() < 0.5 else 1
		peligros.append({"pos": Vector2(_azar.randf_range(20, 300), cima + 65.0) if coco else Vector2(0 if lado > 0 else 320, cima - 25.0), "vel": Vector2(10.0 * lado, -[24.0, 32.0, 42.0][dificultad - 1]) if coco else Vector2(lado * [28.0, 39.0, 51.0][dificultad - 1], 0), "coco": coco})
	for i in range(peligros.size() - 1, -1, -1):
		var peligro: Dictionary = peligros[i]
		var pos: Vector2 = peligro["pos"]
		var vel: Vector2 = peligro["vel"]
		pos += vel * dt
		peligro["pos"] = pos
		if inmune <= 0.0 and altura < 5.0 and pos.distance_to(jugadora) < (8.0 if bool(peligro["coco"]) else 10.0):
			peligros.remove_at(i)
			_golpe("Los cocos y las iguanas te alcanzaron a ras del mosaico; salta para pasarlos.")
		elif pos.y < cima - 160.0 or pos.x < -12.0 or pos.x > ANCHO + 12.0:
			peligros.remove_at(i)

func _aterrizar() -> void:
	for placa in placas:
		if int(placa["fila"]) != siguiente:
			continue
		var p: Vector2 = placa["pos"]
		if absf(jugadora.x - p.x) <= radio_placa and absf(jugadora.y - p.y) <= 9.0:
			if int(placa["hito"]) != siguiente:
				_golpe("Esa placa pertenece a otro momento: sigue el pictograma pendiente antes de subir.")
				return
			placa["revelada"] = true
			var hito: Dictionary = hitos[siguiente]
			aviso = "%s %d" % [NOMBRES[int(hito["icono"])], int(hito["anio"])]
			aviso_t = 2.3
			puntos += 100 + 25 * vidas
			_estallar(p, Estilo.DORADO)
			destello = 0.12
			descanso = 0.85
			velocidad = Vector2.ZERO
			siguiente += 1
			sonar("recoger")
			if siguiente == hitos.size():
				_final(true, "Del observatorio de %d a los Acuerdos de %d: cada hito ocupa su lugar en el tiempo." % [int(hitos[0]["anio"]), int(hitos.back()["anio"])])
			return

func _golpe(motivo: String) -> void:
	if inmune > 0.0:
		return
	vidas -= 1
	inmune = 2.0
	destello = 0.25
	sacudida = 0.3
	_estallar(jugadora, Estilo.CORAL)
	sonar("error")
	jugadora.y = PRIMERA_FILA + siguiente * PASO_FILA - 25.0
	velocidad = Vector2.ZERO
	salto = 0.0
	altura = 0.0
	if vidas <= 0:
		_final(false, motivo)

func _final(superado: bool, motivo: String) -> void:
	fase = 2
	gana = superado
	causa = motivo
	sonar("logro" if superado else "error")

func _piloto() -> void:
	# Solo manda direcciones y salto; no escribe placas, vidas ni progreso.
	mando = Vector2.ZERO
	if fase != 1 or descanso > 0.0:
		return
	var objetivo: Vector2 = jugadora
	for placa in placas:
		if int(placa["fila"]) == siguiente and ((int(placa["hito"]) == siguiente) == (_auto > 0)):
			objetivo = placa["pos"]
			break
	var diferencia: Vector2 = objetivo - jugadora - velocidad * 0.09
	mando.x = signf(diferencia.x) if absf(diferencia.x) > 1.0 else 0.0
	mando.y = signf(diferencia.y) if absf(diferencia.y) > 1.0 else 0.0
	mando = mando.limit_length()
	if salto <= 0.0:
		if jugadora.distance_to(objetivo) < 7.0:
			_pulso = true
		for peligro in peligros:
			var pos: Vector2 = peligro["pos"]
			var vel: Vector2 = peligro["vel"]
			if (pos + vel * 0.24).distance_to(jugadora) < 13.0:
				_pulso = true

func _animar(dt: float) -> void:
	inmune = maxf(0.0, inmune - dt)
	destello = maxf(0.0, destello - dt)
	sacudida = maxf(0.0, sacudida - dt)
	aviso_t = maxf(0.0, aviso_t - dt)
	for i in range(particulas.size() - 1, -1, -1):
		var p: Dictionary = particulas[i]
		p["vida"] = float(p["vida"]) - dt
		var pos: Vector2 = p["pos"]
		var vel: Vector2 = p["vel"]
		p["pos"] = pos + vel * dt
		p["vel"] = vel + Vector2(0, -45) * dt
		if float(p["vida"]) <= 0.0:
			particulas.remove_at(i)

func _estallar(pos: Vector2, color: Color) -> void:
	for i in 18:
		particulas.append({"pos": pos, "vel": Vector2.from_angle(_azar.randf() * TAU) * _azar.randf_range(9, 30), "vida": 0.7, "color": color})

func _camara() -> float:
	return maxf(0.0, jugadora.y - 32.0)

func _pantalla(pos: Vector2) -> Vector2:
	return Vector2(pos.x, 160.0 - pos.y + _camara())

func _r(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2(floorf(x), floorf(y), w, h), color)

func _sprite(mapa: Array, pos: Vector2, color: Color, escala: int = 1) -> void:
	var pal: Dictionary = {"h": Estilo.TERRACOTA, "p": Estilo.CREMA, "c": Estilo.DORADO, "j": Estilo.PETROLEO}
	for y in mapa.size():
		var fila: String = mapa[y]
		for x in fila.length():
			var c: String = fila[x]
			if c != ".":
				var tinta: Color = pal.get(c, color)
				_r(pos.x + x * escala, pos.y + y * escala, escala, escala, tinta)

func _escribir(t: String, x: float, y: float, color: Color, escala: int = 1) -> void:
	var cx: float = x
	for i in t.length():
		var c: String = t[i]
		var mapa: Array = LETRAS.get(c, LETRAS[" "])
		_sprite(mapa, Vector2(cx, y), color, escala)
		var fila: String = mapa[0]
		cx += (fila.length() + 1) * escala

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(4, 4))
	_r(0, 0, ANCHO, ALTO, Estilo.NOCHE)
	var desvio: Vector2 = Vector2(roundf(sin(reloj * 83.0)), roundf(cos(reloj * 91.0))) if sacudida > 0.0 else Vector2.ZERO
	draw_set_transform(desvio * 4, 0.0, Vector2(4, 4))
	# Cielo y lomas cubren el horizonte; el mosaico llega al pie de pantalla.
	_r(0, 29, ANCHO, 25, Estilo.PETROLEO.darkened(0.55))
	for i in 24:
		_r((i * 47 + 11) % 320, 32 + (i * 7) % 17, 1, 1, Estilo.CREMA)
	for i in 16:
		_r(i * 22, 46 + (i % 4) * 2, 24, 9, Estilo.TINTA)
	for i in range(-4, 65):
		var y: float = _pantalla(Vector2(0, i * 14.0)).y
		if y < 53 or y > ALTO:
			continue
		_r(0, y, ANCHO, 13, Estilo.TINTA_SUAVE if i % 5 == 0 else Estilo.TINTA)
		_r(0, y, ANCHO, 1, Estilo.NARANJA if i % 5 == 0 else Estilo.PETROLEO)
		for x in range(2, 320, 9):
			_r(x + (4 if i % 2 else 0), y + 5, 3, 2, Estilo.PETROLEO if i % 3 else Estilo.TERRACOTA)
	# Casas a ambos lados, sin marco alrededor del campo.
	for i in 14:
		var y: float = fposmod(i * 15.0 + _camara() * 0.5, 180.0)
		for x in [0, 299]:
			_r(x, y, 21, 13, Estilo.TINTA if i % 2 == 0 else Estilo.PETROLEO.darkened(0.5))
			_r(x + 3, y + 4, 3, 3, Estilo.NARANJA)
			_r(x + 11, y + 4, 3, 3, Estilo.DORADO)
	for placa in placas:
		var p: Vector2 = _pantalla(placa["pos"])
		if p.y < 65.0 or p.y > 166.0:
			continue
		var fila: int = placa["fila"]
		var indice: int = placa["hito"]
		var hito: Dictionary = hitos[indice]
		var revelada: bool = placa["revelada"]
		var borde: Color = Estilo.DORADO if revelada else Estilo.PETROLEO
		if dificultad == 1 and fila == siguiente and indice == siguiente:
			borde = Estilo.CIAN
		_r(p.x - 19, p.y - 12, 38, 25, borde)
		_r(p.x - 18, p.y - 11, 36, 22, Estilo.NOCHE)
		_sprite(ICONOS[int(hito["icono"])], p + Vector2(-4, -9), Estilo.CREMA if fila <= siguiente else Estilo.TINTA_SUAVE)
		if revelada:
			_escribir(str(hito["anio"]), p.x - 15, p.y + 1, Estilo.DORADO, 2)
		else:
			_escribir("E", p.x - 1, p.y + 3, Estilo.CIAN if fila == siguiente else Estilo.PETROLEO)
	for peligro in peligros:
		var p: Vector2 = _pantalla(peligro["pos"])
		if p.y > 54 and p.y < 180:
			_sprite(COCO if bool(peligro["coco"]) else IGUANA, p - Vector2(4, 4), Estilo.NARANJA if bool(peligro["coco"]) else Estilo.CORAL)
	for particula in particulas:
		var p: Vector2 = _pantalla(particula["pos"])
		var color: Color = particula["color"]
		_r(p.x, p.y, 1, 1, color)
	var chica: Vector2 = _pantalla(jugadora)
	_r(chica.x - 3, chica.y, 7, 2, Estilo.PETROLEO)
	if inmune <= 0.0 or fmod(inmune, 0.3) > 0.15:
		_sprite(CHICA, chica - Vector2(3, 10 + altura), Estilo.CREMA)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(4, 4))
	_r(0, 0, ANCHO, 29, Estilo.NOCHE)
	_r(0, 28, ANCHO, 1, Estilo.PETROLEO)
	_escribir(str(puntos).pad_zeros(4), 4, 4, Estilo.CREMA, 2)
	_escribir("%d/9" % siguiente, 114, 4, Estilo.DORADO, 2)
	for i in 3:
		_sprite(["#.#", "###", ".#."], Vector2(189 + 12 * i, 4), Estilo.CREMA if i < vidas else Estilo.TINTA_SUAVE, 2)
	_escribir(str(int(ceil(maxf(0, limite - reloj)))).pad_zeros(3), 289, 4, Estilo.CREMA, 2)
	if siguiente < hitos.size():
		var hito: Dictionary = hitos[siguiente]
		_escribir("SIGUE", 4, 19, Estilo.CIAN)
		_sprite(ICONOS[int(hito["icono"])], Vector2(28, 17), Estilo.CREMA)
		_escribir(NOMBRES[int(hito["icono"])], 43, 19, Estilo.PAPEL)
	_r(200, 20, 116, 3, Estilo.PETROLEO)
	_r(200, 20, 116 * clampf(1.0 - reloj / limite, 0.0, 1.0), 3, Estilo.CIAN)
	_escribir("< > WASD", 4, 170, Estilo.CREMA)
	_escribir("E SALTA", 223, 170, Estilo.CIAN)
	_escribir("ESC", 301, 170, Estilo.CREMA)
	if aviso_t > 0.0:
		_r(0, 151, ANCHO, 11, Estilo.NOCHE)
		_escribir(aviso, 7, 154, Estilo.DORADO)
	if destello > 0.0:
		_r(0, 53, ANCHO, 127, Color(Estilo.CREMA if descanso > 0 else Estilo.CORAL, destello))
	if fase == 0:
		_r(54, 65, 212, 62, Estilo.NOCHE)
		for i in 3:
			_r(128 + i * 20, 101 - i * 9, 20, 4, Estilo.CIAN)
		_sprite(CHICA, Vector2(132, 88), Estilo.CREMA)
		_escribir("SUBE LOS HITOS EN ORDEN", 64, 112, Estilo.CREMA, 2)
	if fase == 2:
		_r(67, 69, 186, 29, Estilo.NOCHE)
		_escribir("CIMA DEL TIEMPO" if gana else "OTRO INTENTO", 82, 78, Estilo.DORADO if gana else Estilo.CORAL, 2)
