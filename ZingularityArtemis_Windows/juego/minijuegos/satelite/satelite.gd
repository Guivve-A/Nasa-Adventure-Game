extends "res://nucleo/minijuego.gd"

# Maqueta arcade original: caras de montaje, no plano de un satelite real.
# Distancias, tiempos y golpes son reglas de juego. Dimensiones: fichas del JSON.
const DT: float = 1.0 / 120.0
const Y_ENCAJE: float = 146.0
const X_MIN: float = 16.0
const X_MAX: float = 256.0
const CENTRO: float = 136.0
const CARRILES: Array[float] = [32.0, 84.0, 136.0, 188.0, 240.0]
const NOMBRES: Array[String] = ["PANEL", "RADIO", "ANTENA", "COMPUTADORA", "BATERIA"]
const ORDEN: Array[int] = [0, 4, 3, 1, 2]
const ICONOS: Array[String] = [
	"###.###/#.#.#.#/###.###/...#.../###.###/#.#.#.#/###.###",
	"..#..../..#..../#######/#.....#/#.#.#.#/#.....#/#######",
	"#.....#/.#...#./..###../...#.../...#.../...#.../..###..",
	".#.#.#./#######/#.....#/##.#.##/#.....#/#######/.#.#.#.",
	"..###../.#####./.#...#./.#.#.#./.#####./.#####./.#####.",
	"#....#./.##.#../..###../###.###/..###../.#.##../#....#."
]
const BASTIDOR: Array[String] = [
	"...cccccccccc", "..cCCCCCCCCcC", ".cCCCCCCCCc.C", "cccccccccc..C",
	"c........c..C", "c........c..C", "c........c..C", "c........c..C",
	"c........c..C", "c........c..C", "c........c.C.", "ccccccccccc.."
]
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
var fase: int = 0 # 0 mision, 1 cinta, 2 enlace, 3 celebracion
var cubo_x: float = CENTRO
var velocidad_x: float = 0.0
var cara: int = 0
var montadas: Array[bool] = [false, false, false, false, false]
var objetos: Array[Dictionary] = []
var vidas: int = 3
var puntos: int = 0
var reloj: float = 0.0
var limite: float = 110.0
var rapidez: float = 10.5
var margen: float = 12.0
var enlace: float = 0.0
var destino: float = CENTRO
var energia: float = 0.0
var mando: float = 0.0
var turbo: bool = false
var accion: bool = false
var _pulso: bool = false
var _auto: int = 0
var _acum: float = 0.0
var _fase_t: float = 0.0
var _giro_t: float = 0.0
var _proxima: float = 0.0
var _basura_t: float = 1.8
var _contador: int = 0
var _inmune: float = 0.0
var _sacudida: float = 0.0
var _flash: float = 0.0
var _aviso: String = ""
var _aviso_t: float = 0.0
var _gana: bool = false
var _causa: String = ""
var _particulas: Array[Dictionary] = []
var _azar: RandomNumberGenerator = RandomNumberGenerator.new()
var _cm_cubo: int = 0
var _cm_panel: int = 0
var _dato: String = ""
var _raton: bool = false
var _raton_x: float = CENTRO


func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	limite = [110.0, 95.0, 80.0][dificultad - 1]
	rapidez = 10.5
	margen = [12.0, 10.0, 8.0][dificultad - 1]
	_azar.seed = int(parametros.get("semilla", 5309 + dificultad * 37))
	var ficha: Dictionary = Juego.ficha("cubesat")
	_dato = str(ficha.get("texto", ""))
	var cifras: RegEx = RegEx.new()
	cifras.compile("(\\d+) cm")
	var medidas: Array[RegExMatch] = cifras.search_all(_dato)
	if medidas.size() >= 2:
		_cm_cubo = int(medidas[0].get_string(1))
		_cm_panel = int(medidas[1].get_string(1))
	queue_redraw()


func _empezar() -> void:
	fase = 0
	sonar("radio")


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0:
		return
	if evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar"):
		_pulso = true
		get_viewport().set_input_as_handled()
	if evento.is_action_pressed("mover_izquierda") or evento.is_action_pressed("mover_derecha"):
		_raton = false


func _gui_input(evento: InputEvent) -> void:
	if not activo or _auto != 0:
		return
	if evento is InputEventMouseMotion:
		_raton = true
		_raton_x = clampf(evento.position.x / 4.0, X_MIN, X_MAX)
	elif evento is InputEventMouseButton and evento.button_index == MOUSE_BUTTON_LEFT:
		accion = evento.pressed
		if evento.pressed:
			_pulso = true
		accept_event()


func _paso(delta: float) -> void:
	_acum += delta
	while _acum >= DT and activo:
		_acum -= DT
		if _auto != 0:
			_piloto()
		else:
			mando = eje_x()
			turbo = Input.is_action_pressed("mover_abajo")
			if _raton:
				mando = signf(_raton_x - cubo_x) if absf(_raton_x - cubo_x) > 1.5 else 0.0
			accion = Input.is_action_pressed("interactuar") or Input.is_action_pressed("saltar") or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)
		_tic(DT)
	queue_redraw()


func _tic(dt: float) -> void:
	_fase_t += dt
	_giro_t = maxf(0.0, _giro_t - dt)
	_inmune = maxf(0.0, _inmune - dt)
	_sacudida = maxf(0.0, _sacudida - dt)
	_flash = maxf(0.0, _flash - dt)
	_aviso_t = maxf(0.0, _aviso_t - dt)
	_efectos(dt)
	if fase == 0:
		_pulso = false
		if _fase_t >= 2.0:
			fase = 1
			_fase_t = 0.0
		return
	if fase == 3:
		if _fase_t > 1.4:
			if _gana:
				Juego.anotar("cubesat")
			terminar(_gana, float(puntos), _dato if _gana else _causa)
		return
	reloj += dt
	# Respuesta directa con frenado corto, sin latencia de menus.
	velocidad_x = move_toward(velocidad_x, mando * 95.0, 650.0 * dt)
	cubo_x = clampf(cubo_x + velocidad_x * dt, X_MIN, X_MAX)
	if _pulso and fase == 1 and _giro_t <= 0.0:
		cara = (cara + 1) % 5
		_giro_t = 0.16
		sonar("tic")
	_pulso = false
	if fase == 1:
		_cinta(dt * (2.5 if turbo else 1.0))
	elif fase == 2:
		# El panel carga; la bateria mantiene la radio mientras se busca el enlace.
		energia = minf(1.0, energia + dt * 0.4)
		if accion and absf(cubo_x - destino) <= margen and energia > 0.05:
			enlace = minf(3.0, enlace + dt)
			energia = maxf(0.0, energia - dt * 0.55)
			if int(enlace * 4.0) != int((enlace - dt) * 4.0):
				sonar("radio")
		else:
			enlace = maxf(0.0, enlace - dt * 0.25)
		if enlace >= 3.0:
			_final(true, "")
	if reloj >= limite and fase != 3:
		_final(false, "La cinta se detuvo antes de completar el montaje y encender la señal.")


func _cinta(dt: float) -> void:
	_proxima -= dt
	_basura_t -= dt
	if _proxima <= 0.0 and not _hay_pieza():
		_nueva_pieza()
	if _basura_t <= 0.0:
		_basura_t += [4.8, 3.2, 2.6][dificultad - 1]
		_contador += 1
		var bx: float = CARRILES[(_contador * 2 + dificultad) % 5]
		# Nunca se genera una pared inevitable sobre la pieza.
		for o in objetos:
			if int(o["tipo"]) < 5 and absf(float(o["x"]) - bx) < 26.0:
				bx = CARRILES[(_contador * 2 + dificultad + 2) % 5]
		objetos.append({"x": bx, "y": 28.0, "tipo": 5})
	for i in range(objetos.size() - 1, -1, -1):
		var o: Dictionary = objetos[i]
		var tipo: int = o["tipo"]
		var antes: float = o["y"]
		var y: float = antes + rapidez * (1.25 if tipo == 5 else 1.0) * dt
		o["y"] = y
		if antes < Y_ENCAJE and y >= Y_ENCAJE:
			if absf(float(o["x"]) - cubo_x) <= (margen if tipo < 5 else 12.0):
				if tipo < 5 and cara == tipo:
					montadas[tipo] = true
					puntos += 200
					_estallar(cubo_x, Y_ENCAJE, Estilo.CIAN)
					sonar("recoger")
					_aviso = NOMBRES[tipo] + " +"
					_aviso_t = 1.2
					_proxima = 0.65
					objetos.remove_at(i)
					if _total() == 5:
						fase = 2
						_fase_t = 0.0
						destino = CENTRO
						energia = 1.0
						sonar("ok")
						objetos.clear()
						return
					continue
				elif _inmune <= 0.0:
					_golpe("La chatarra golpeó el bastidor." if tipo == 5 else "La pieza chocó con una cara sin su conector.")
					objetos.remove_at(i)
					_proxima = 0.65
					if fase == 3:
						return
					continue
		if y > 164.0:
			if tipo < 5:
				_aviso = "PIEZA RECIRCULANDO"
				_aviso_t = 1.4
				_proxima = 0.65
			else:
				puntos += 10
			objetos.remove_at(i)


func _hay_pieza() -> bool:
	for o in objetos:
		if int(o["tipo"]) < 5:
			return true
	return false


func _nueva_pieza() -> void:
	for tipo in ORDEN:
		if not montadas[tipo]:
			var carril: int = (tipo * 2 + _contador + dificultad) % 5
			objetos.append({"x": CARRILES[carril], "y": 28.0, "tipo": tipo})
			sonar("salto")
			return


func _total() -> int:
	var n: int = 0
	for m in montadas:
		if m:
			n += 1
	return n


func _golpe(causa: String) -> void:
	vidas -= 1
	_inmune = 1.5
	_sacudida = 0.24
	_flash = 0.22
	_aviso = "GOLPE"
	_aviso_t = 1.0
	_estallar(cubo_x, Y_ENCAJE, Estilo.CORAL)
	sonar("error")
	if vidas <= 0:
		_final(false, causa + " El cubo perdió sus tres protecciones.")


func _final(gana: bool, causa: String) -> void:
	fase = 3
	_fase_t = 0.0
	_gana = gana
	_causa = causa
	if gana:
		puntos += vidas * 100 + int(limite - reloj)
		_estallar(cubo_x, 139.0, Estilo.DORADO)
		sonar("logro")


func _piloto() -> void:
	# Solo manda movimiento, accion y palanca rapida: nunca instala ni teletransporta.
	mando = 0.0
	turbo = true
	accion = false
	if fase == 2:
		mando = signf(destino - cubo_x) if absf(destino - cubo_x) > 1.0 else 0.0
		accion = true
		return
	var objetivo: float = cubo_x
	var pieza: Dictionary = {}
	for o in objetos:
		if int(o["tipo"]) < 5:
			pieza = o
			break
	if not pieza.is_empty():
		var tipo: int = pieza["tipo"]
		objetivo = float(pieza["x"])
		if _giro_t <= 0.0 and cara != (tipo if _auto > 0 else (tipo + 1) % 5):
			_pulso = true
	# Esquiva la basura a su altura; vuelve al conector despues.
	for o in objetos:
		if int(o["tipo"]) == 5 and float(o["y"]) > Y_ENCAJE - 21.0 and float(o["y"]) < Y_ENCAJE + 4.0 and absf(float(o["x"]) - objetivo) < 22.0:
			objetivo = clampf(float(o["x"]) + (30.0 if cubo_x > CENTRO else -30.0), X_MIN, X_MAX)
	mando = signf(objetivo - cubo_x) if absf(objetivo - cubo_x) > 1.2 else 0.0


func _estallar(x: float, y: float, color: Color) -> void:
	for i in 18:
		var a: float = _azar.randf_range(0.0, TAU)
		var v: float = _azar.randf_range(10.0, 36.0)
		_particulas.append({"p": Vector2(x, y), "v": Vector2(cos(a), sin(a)) * v, "t": 0.65, "c": color})


func _efectos(dt: float) -> void:
	for i in range(_particulas.size() - 1, -1, -1):
		var p: Dictionary = _particulas[i]
		var t: float = float(p["t"]) - dt
		p["t"] = t
		var pos: Vector2 = p["p"]
		var v: Vector2 = p["v"]
		p["p"] = pos + v * dt
		p["v"] = v + Vector2(0.0, 28.0) * dt
		if t <= 0.0:
			_particulas.remove_at(i)


func _r(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2(roundf(x) * 4.0, roundf(y) * 4.0, w * 4.0, h * 4.0), color)


func _mapa(mapa: String, x: float, y: float, color: Color, e: int = 1) -> void:
	var filas: PackedStringArray = mapa.split("/")
	for j in filas.size():
		var fila: String = filas[j]
		for i in fila.length():
			if fila[i] != ".":
				_r(x + i * e, y + j * e, e, e, color)


func _texto(t: String, x: float, y: float, color: Color, e: int = 1) -> void:
	for i in t.length():
		var glifo: String = GLIFOS.get(t[i], ".../.../.../.../...")
		_mapa(glifo, x + i * 4 * e, y, color, e)


func _icono(tipo: int, x: float, y: float, color: Color, e: int = 1) -> void:
	_mapa(ICONOS[tipo], x, y, color, e)


func _draw() -> void:
	_r(0, 0, 320, 180, Estilo.NOCHE)
	var desplazamiento: Vector2 = Vector2.ZERO
	if _sacudida > 0.0:
		desplazamiento = Vector2(4.0 if int(_sacudida * 30.0) % 2 == 0 else -4.0, 0)
	draw_set_transform(desplazamiento)
	_dibujar_taller()
	for o in objetos:
		var x: float = o["x"]
		var y: float = o["y"]
		var tipo: int = o["tipo"]
		_r(x - 6, y - 6, 13, 13, Estilo.CORAL if tipo == 5 else Estilo.NARANJA)
		_r(x - 5, y - 5, 11, 11, Estilo.TINTA)
		_icono(tipo, x - 3, y - 3, Estilo.CORAL if tipo == 5 else Estilo.CREMA)
		if tipo < 5:
			_texto(str(tipo + 1), x + 8, y - 2, Estilo.CREMA)
			for k in 3:
				_r(x, y + 10 + k * 4, 1, 1, Estilo.CIAN_MEDIO)
	_dibujar_cubo()
	for p in _particulas:
		var pos: Vector2 = p["p"]
		var color: Color = p["c"]
		_r(pos.x, pos.y, 1, 1, color)
	if fase == 2 or (fase == 3 and _gana):
		_dibujar_enlace()
	draw_set_transform(Vector2.ZERO)
	_dibujar_hud()
	if _aviso_t > 0.0 and fase == 1:
		_texto(_aviso, CENTRO - _aviso.length() * 2.0, 24, Estilo.CREMA)
	if fase == 0:
		_r(44, 59, 185, 37, Estilo.CREMA)
		_r(45, 60, 183, 35, Estilo.TINTA)
		_icono(0, 79, 67, Estilo.CIAN, 2)
		_texto("+", 100, 71, Estilo.DORADO, 2)
		_icono(3, 114, 67, Estilo.CIAN, 2)
		_texto("ARMA EL CUBO. ENCIENDE SU SENAL.", 76, 86, Estilo.CREMA)
	if _flash > 0.0:
		_r(0, 18, 268, 146, Color(Estilo.CORAL, _flash * 0.6))
	if fase == 3:
		_r(72, 77, 127, 18, Estilo.TINTA)
		_texto("SENAL VIVA" if _gana else "CUBO DETENIDO", 82, 81, Estilo.CIAN if _gana else Estilo.CORAL, 2)


func _dibujar_taller() -> void:
	# Las guias atraviesan el campo abierto; el suelo llega a ambos bordes.
	_r(0, 18, 268, 146, Estilo.NOCHE)
	for i in 36:
		_r((i * 73 + 11) % 268, 21 + (i * 37) % 112, 1, 1, Estilo.TINTA_SUAVE)
	for x in CARRILES:
		_r(x - 20, 18, 1, 146, Color(Estilo.PETROLEO, 0.45))
		for j in 14:
			var y: float = 18.0 + fposmod(j * 11.0 + reloj * rapidez * (2.5 if turbo else 1.0), 146.0)
			_r(x - 16, y, 33, 1, Color(Estilo.PETROLEO, 0.22))
	_r(0, 164, 320, 16, Estilo.PETROLEO)
	_r(0, 164, 320, 2, Estilo.NARANJA)
	for k in 32:
		_r(k * 10, 166, 5, 2, Estilo.TINTA_SUAVE)
	# La sexta cara soporta el carro; cinco conectores didacticos a la derecha.
	_r(268, 18, 52, 146, Estilo.TINTA)
	_texto("CARAS", 280, 24, Estilo.CREMA)
	for i in 5:
		var y: float = 38.0 + i * 22.0
		_r(276, y, 36, 17, Estilo.CIAN if cara == i else Estilo.TINTA_SUAVE)
		_r(277, y + 1, 34, 15, Estilo.NOCHE)
		_icono(i, 280, y + 5, Estilo.CIAN if montadas[i] else Estilo.CREMA)
		_texto(str(i + 1), 292, y + 6, Estilo.CREMA)
		if montadas[i]:
			_mapa("....#/...#./#.#../.#...", 300, y + 6, Estilo.CIAN)
	_r(276, 151, 9, 9, Estilo.NARANJA)
	_texto("E", 279, 153, Estilo.NOCHE)
	_texto("GIRA", 290, 153, Estilo.NARANJA)
	_texto("A D MOVER   E GIRAR   S RAPIDA   ESC SALIR", 4, 171, Estilo.CREMA)


func _dibujar_cubo() -> void:
	if _inmune > 0.0 and fmod(_inmune, 0.35) < 0.16:
		return
	var x: float = roundf(cubo_x)
	_r(x - 12, 155, 25, 3, Estilo.NARANJA)
	_r(x - 9, 158, 4, 3, Estilo.TINTA_SUAVE)
	_r(x + 6, 158, 4, 3, Estilo.TINTA_SUAVE)
	for j in BASTIDOR.size():
		var fila: String = BASTIDOR[j]
		for i in fila.length():
			if fila[i] != ".":
				_r(x - 6 + i, 143 + j, 1, 1, Estilo.CREMA if fila[i] == "c" else Estilo.PETROLEO)
	_icono(cara, x - 3, 147, Estilo.CIAN if montadas[cara] else Estilo.CREMA)
	# Conector activo encima del bastidor: forma y numero coinciden con la pieza.
	_r(x - 7, 133, 15, 10, Estilo.CIAN)
	_r(x - 6, 134, 13, 8, Estilo.NOCHE)
	_icono(cara, x - 3, 134, Estilo.CIAN)
	_texto(str(cara + 1), x + 9, 136, Estilo.CIAN)
	if fase >= 2:
		# Un pixel representa un centimetro: proporciones tomadas del JSON.
		for lado in [-1, 1]:
			var px: float = x - 5 - _cm_panel if lado < 0 else x + 5
			_r(px, 144, _cm_panel, 8, Estilo.PETROLEO)
			for j in range(0, _cm_panel, 4):
				_r(px + j, 144, 1, 8, Estilo.CREMA)
			_r(px, 148, _cm_panel, 1, Estilo.CREMA)
		_texto("%d CM" % _cm_cubo, x - 9, 163, Estilo.CREMA)
		_texto("%d CM" % _cm_panel, x - _cm_panel - 4, 135, Estilo.DORADO)
		_r(x, 141, 1, 5, Estilo.CIAN)
		_icono(2, x - 3, 135, Estilo.CIAN)


func _dibujar_enlace() -> void:
	_r(destino - margen, 38, margen * 2, 1, Estilo.CIAN)
	_r(destino - margen, 38, 1, 6, Estilo.CIAN)
	_r(destino + margen - 1, 38, 1, 6, Estilo.CIAN)
	_icono(1, destino - 3, 23, Estilo.CIAN, 2)
	_texto("MANTEN E: ENCIENDE LA SENAL", 88, 58, Estilo.CREMA)
	if accion and absf(cubo_x - destino) <= margen:
		for i in 18:
			var y: float = 44.0 + fposmod(i * 5.0 - reloj * 28.0, 88.0)
			_r(cubo_x, y, 1, 2, Estilo.CIAN)
	_r(100, 79, 74, 7, Estilo.PETROLEO)
	_r(101, 80, floorf(72.0 * enlace / 3.0), 5, Estilo.CIAN)
	_icono(4, 180, 78, Estilo.DORADO)
	_r(191, 79, floorf(20 * energia), 6, Estilo.DORADO)


func _dibujar_hud() -> void:
	_r(0, 0, 320, 18, Estilo.TINTA)
	_texto("%04d" % puntos, 4, 4, Estilo.CREMA, 2)
	_texto("%d:5" % _total(), 65, 4, Estilo.CIAN, 2)
	for i in 3:
		_mapa("###/#.#/###", 116 + i * 10, 5, Estilo.CREMA if i < vidas else Estilo.TINTA_SUAVE, 2)
	_texto("%03d" % int(ceil(maxf(0.0, limite - reloj))), 190, 4, Estilo.CORAL if limite - reloj < 15.0 else Estilo.CREMA, 2)
	_texto("N%d" % dificultad, 300, 6, Estilo.NARANJA)
