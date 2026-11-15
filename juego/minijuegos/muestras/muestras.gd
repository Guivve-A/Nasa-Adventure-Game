extends "res://nucleo/minijuego.gd"

# Distancias, oxigeno, tiempos y sellos son reglas del suenio, no cifras de una EVA.
# La gravedad se lee de la ficha; la altura balistica se ve respecto a la sombra.
const DT: float = 1.0 / 120.0
const CAJA: Vector2 = Vector2(32, 108)
const SITIOS: Array[Vector2] = [Vector2(108, 68), Vector2(220, 64), Vector2(284, 146), Vector2(126, 148)]
const UTILES: Array[int] = [0, 0, 1, 2]
const HERRAMIENTAS: Array[String] = ["CUCHARON", "PINZAS", "TUBO"]
const LIMITES: Array[float] = [105.0, 90.0, 75.0]
const RADIOS: Array[float] = [6.0, 8.0, 10.0]
const CANTIDADES: Array[int] = [3, 4, 5]
const CRATERES: Array[Vector2] = [Vector2(73, 81), Vector2(165, 91), Vector2(205, 149), Vector2(96, 145), Vector2(263, 94)]
const ASTRONAUTA: Array[String] = ["...PPP...", "..PPPPP..", "..PkkkP..", "..PwwwP..", "...PPP...", ".cPPPPP..", ".cPPtPPc.", "..PPtPP..", "..P...P..", ".PP...PP."]
const CAJON: Array[String] = [".kkkkkkkkkkkkk.", "kPPPPPPPPPPPPPk", "kPwwwwwwwwwwwPk", "kPwwwwwwwwwwwPk", "kPPPPPPPPPPPPPk", "kcccccPtPccccck", "kcccccPtPccccck", "kPPPPPPPPPPPPPk", ".kkkkkkkkkkkkk."]
const CUCHARON: Array[String] = ["...P...", "...P...", "...P...", ".PPPPP.", ".PcccP.", ".PPPPP."]
const PINZAS: Array[String] = ["...P...", "..P.P..", "..P.P..", ".P...P.", ".P...P.", ".PP.PP."]
const TUBO: Array[String] = [".PPP.P.", ".PkP.P.", ".PcP.P.", ".PwPPPP", ".PcP...", ".PPP..."]
const ROCA: Array[String] = ["..PPP..", ".PPccP.", "PPccwwP", ".PwwwP.", "..PPP.."]
const LETRAS: Dictionary = {
	"A":".#./#.#/###/#.#/#.#", "B":"##./#.#/##./#.#/##.", "C":"###/#../#../#../###",
	"D":"##./#.#/#.#/#.#/##.", "E":"###/#../##./#../###", "F":"###/#../##./#../#..",
	"G":"###/#../#.#/#.#/###", "H":"#.#/#.#/###/#.#/#.#", "I":"###/.#./.#./.#./###",
	"J":"..#/..#/..#/#.#/###", "K":"#.#/#.#/##./#.#/#.#", "L":"#../#../#../#../###",
	"M":"#.#/###/###/#.#/#.#", "N":"#.#/###/###/###/#.#", "O":"###/#.#/#.#/#.#/###",
	"P":"###/#.#/###/#../#..", "Q":"###/#.#/#.#/###/..#", "R":"##./#.#/##./#.#/#.#",
	"S":"###/#../###/..#/###", "T":"###/.#./.#./.#./.#.", "U":"#.#/#.#/#.#/#.#/###",
	"V":"#.#/#.#/#.#/#.#/.#.", "W":"#.#/#.#/###/###/#.#", "X":"#.#/#.#/.#./#.#/#.#",
	"Y":"#.#/#.#/.#./.#./.#.", "Z":"###/..#/.#./#../###",
	"0":"###/#.#/#.#/#.#/###", "1":".#./##./.#./.#./###", "2":"###/..#/###/#../###",
	"3":"###/..#/###/..#/###", "4":"#.#/#.#/###/..#/..#", "5":"###/#../###/..#/###",
	"6":"###/#../###/#.#/###", "7":"###/..#/..#/..#/..#", "8":"###/#.#/###/#.#/###",
	"9":"###/#.#/###/..#/###", "/":"..#/..#/.#./#../#..", ":":".../.#./.../.#./...",
	"+":".../.#./###/.#./...", "-":".../.../###/.../...", ".":".../.../.../.../.#.",
}
var posicion: Vector2 = CAJA + Vector2(14, 0)
var velocidad: Vector2 = Vector2.ZERO
var altura: float = 0.0
var vertical: float = 0.0
var gravedad: float = 0.0
var fraccion: String = ""
var herramienta: int = 0
var carga: int = -1
var entregadas: Array[int] = []
var muestras: Array[Dictionary] = []
var vidas: int = 3
var oxigeno: float = 105.0
var puntos: float = 0.0
var progreso: float = 0.0
var cercana: int = -1
var fase: int = 0 # 0 mision, 1 campo, 2 celebracion, 3 perdida
var reloj: float = 0.0
var fase_t: float = 0.0
var objetivo_total: int = 4
var causa: String = ""
var mando: Vector2 = Vector2.ZERO
var accion: bool = false
var _auto: int = 0
var _acum: float = 0.0
var _inmune: float = 0.0
var _pausa_muestra: float = 0.0
var _destello: float = 0.0
var _sacudida: float = 0.0
var _aviso: String = ""
var _aviso_t: float = 0.0
var _huellas: Array[Vector2] = []
var _particulas: Array[Dictionary] = []
var _azar: RandomNumberGenerator = RandomNumberGenerator.new()
var _pal: Dictionary = {}
var _glifos: Dictionary = {}


func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	oxigeno = LIMITES[dificultad - 1]
	_azar.seed = 331
	_pal = {"P": Estilo.CREMA, "c": Estilo.NARANJA, "w": Estilo.PETROLEO, "k": Estilo.CIAN, "t": Estilo.CORAL}
	for clave in LETRAS:
		var dibujo: String = LETRAS[clave]
		_glifos[clave] = dibujo.split("/")
	var ficha: Dictionary = Juego.ficha("gravedad_lunar")
	var texto_gravedad: String = str(ficha.get("texto", ""))
	var numero: RegEx = RegEx.new()
	numero.compile("[0-9]+,[0-9]+")
	var dato: RegExMatch = numero.search(texto_gravedad)
	if dato != null:
		gravedad = float(dato.get_string().replace(",", ".")) * 40.0
	numero.compile("[0-9]+/[0-9]+")
	dato = numero.search(texto_gravedad)
	if dato != null:
		fraccion = dato.get_string()
	var pedida: int = int(parametros.get("muestra", -1))
	objetivo_total = 1 if pedida >= 0 and pedida <= 3 else 4
	for i in 4:
		if objetivo_total == 1 and i != pedida:
			continue
		muestras.append({"id": i, "pos": SITIOS[i], "v": Vector2.ZERO, "espera": 0.0, "estado": 0})
	queue_redraw()


func _empezar() -> void:
	fase = 0
	fase_t = 0.0
	sonar("radio")


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or evento.is_echo():
		return
	if evento.is_action_pressed("interactuar"):
		_cambiar()
		get_viewport().set_input_as_handled()


func _cambiar() -> void:
	herramienta = (herramienta + 1) % 3
	progreso = 0.0
	sonar("tic")


func _paso(delta: float) -> void:
	_acum += delta
	while _acum >= DT and activo:
		_acum -= DT
		if _auto != 0:
			_piloto()
		else:
			mando = Vector2(eje_x(), -eje_y()).limit_length()
			accion = Input.is_action_pressed("saltar")
		_tic(DT)
	queue_redraw()


func _tic(dt: float) -> void:
	reloj += dt
	fase_t += dt
	_efectos(dt)
	if fase == 0:
		if fase_t >= 1.8:
			fase = 1
			fase_t = 0.0
		return
	if fase >= 2:
		if fase_t >= 1.2:
			var aprendizaje: String = "Cucharón para suelo, pinzas para roca, tubo para capas."
			terminar(fase == 2, puntos, aprendizaje if fase == 2 else causa)
		return
	oxigeno = maxf(0.0, oxigeno - dt)
	_inmune = maxf(0.0, _inmune - dt)
	_pausa_muestra = maxf(0.0, _pausa_muestra - dt)
	for m in muestras:
		var espera: float = m["espera"]
		m["espera"] = maxf(0.0, espera - dt)
		var p: Vector2 = m["pos"]
		var v: Vector2 = m["v"]
		p += v * dt
		m["pos"] = Vector2(clampf(p.x, 12, 302), clampf(p.y, 60, 157))
		m["v"] = v.move_toward(Vector2.ZERO, 22.0 * dt)
	_cercania()
	# Espacio planta los pies; recoger no requiere acertar un cuadro de aterrizaje.
	var trabajando: bool = accion and carga < 0 and cercana >= 0 and mando.length() < 0.1
	if trabajando:
		velocidad = velocidad.move_toward(Vector2.ZERO, 180.0 * dt)
		altura = move_toward(altura, 0.0, 32.0 * dt)
		vertical = 0.0
	else:
		var empuje: float = 120.0 if altura <= 0.0 else 80.0
		velocidad = velocidad.move_toward(mando * 62.0, empuje * dt)
		if altura <= 0.0 and mando.length() > 0.1:
			vertical = 30.0
			altura = 0.01
			_huellas.append(posicion)
			if _huellas.size() > 65:
				_huellas.pop_front()
			sonar("salto")
		if altura > 0.0:
			vertical -= gravedad * dt
			altura = maxf(0.0, altura + vertical * dt)
	posicion += velocidad * dt
	posicion = Vector2(clampf(posicion.x, 10, 306), clampf(posicion.y, 60, 158))
	for i in CANTIDADES[dificultad - 1]:
		var centro: Vector2 = CRATERES[i]
		if posicion.distance_to(centro) < RADIOS[dificultad - 1] and altura < 2.0 and _inmune <= 0.0:
			var fuera: Vector2 = (posicion - centro).normalized()
			if fuera == Vector2.ZERO:
				fuera = Vector2.LEFT
			posicion = centro + fuera * (RADIOS[dificultad - 1] + 4.0)
			velocidad = fuera * 30.0
			_dano("Un aterrizaje dentro del cráter rompió el último sello del traje.")
			_aviso = "ATERRIZA FUERA DEL CRATER"
			_aviso_t = 2.0
	if trabajando and _pausa_muestra <= 0.0 and altura <= 0.1:
		var m: Dictionary = muestras[cercana]
		var id: int = m["id"]
		if herramienta != UTILES[id]:
			_escapar(m)
		else:
			progreso += dt
			if int(progreso * 4.0) != int((progreso - dt) * 4.0):
				sonar("tic")
				var sitio: Vector2 = m["pos"]
				_estallar(sitio, Estilo.CREMA, 3)
			if progreso >= (1.7 if id == 3 else 0.7):
				carga = id
				m["estado"] = 1
				progreso = 0.0
				_destello = 0.16
				_estallar(posicion, Estilo.CIAN, 12)
				sonar("recoger")
	else:
		progreso = maxf(0.0, progreso - dt)
	if carga >= 0 and posicion.distance_to(CAJA) < 14.0:
		entregadas.append(carga)
		for m in muestras:
			if int(m["id"]) == carga:
				m["estado"] = 2
		carga = -1
		puntos += 250.0
		_destello = 0.2
		_estallar(CAJA, Estilo.DORADO, 20)
		sonar("ok")
		if entregadas.size() == objetivo_total:
			puntos += floorf(oxigeno) * 2.0
			fase = 2
			fase_t = 0.0
			sonar("logro")
	if oxigeno <= 0.0 and fase == 1:
		_perder("El oxígeno se agotó antes de llevar todas las muestras a la caja.")


func _cercania() -> void:
	cercana = -1
	var distancia: float = 12.0
	for i in muestras.size():
		var m: Dictionary = muestras[i]
		if int(m["estado"]) != 0 or float(m["espera"]) > 0.0:
			continue
		var p: Vector2 = m["pos"]
		var d: float = posicion.distance_to(p)
		if d < distancia:
			cercana = i
			distancia = d


func _escapar(m: Dictionary) -> void:
	var id: int = m["id"]
	var p: Vector2 = m["pos"]
	var direccion: Vector2 = (p - posicion).normalized()
	if direccion.length() < 0.1:
		direccion = Vector2.RIGHT
	m["v"] = direccion * (42.0 if id == 2 else 23.0)
	m["espera"] = 1.6
	_pausa_muestra = 1.7
	progreso = 0.0
	if id < 2:
		_aviso = "EL POLVO CAE ENTRE LAS PUNTAS" if herramienta == 1 else "EL TUBO NO BARRE EL SUELO"
		for k in 14:
			_particulas.append({"p": posicion + Vector2(8, -3), "v": Vector2(_azar.randf_range(-9, 9), _azar.randf_range(12, 22)), "t": 1.0, "c": Estilo.CREMA})
	elif id == 2:
		_aviso = "LA ROCA RUEDA DEL CUCHARON" if herramienta == 0 else "EL TUBO EMPUJA LA ROCA"
	else:
		_aviso = "EL CUCHARON MEZCLA LAS CAPAS" if herramienta == 0 else "LAS PINZAS ROMPEN LAS CAPAS"
	_aviso_t = 2.4
	_estallar(p, Estilo.NARANJA, 24)
	_dano(_aviso.capitalize() + "; la muestra escapó y se perdió el último sello del traje.")


func _dano(motivo: String) -> void:
	vidas -= 1
	oxigeno = maxf(0.0, oxigeno - 6.0)
	_inmune = 1.6
	_destello = 0.18
	_sacudida = 0.3
	_estallar(posicion, Estilo.CORAL, 16)
	sonar("error")
	if vidas <= 0:
		_perder(motivo)


func _perder(motivo: String) -> void:
	causa = motivo
	fase = 3
	fase_t = 0.0
	sonar("error")


func _piloto() -> void:
	# Solo escribe los mismos mandos que las teclas. Nunca entrega ni mueve muestras.
	mando = Vector2.ZERO
	accion = false
	if fase != 1:
		return
	var destino: Vector2 = CAJA
	var elegida: Dictionary = {}
	if carga < 0:
		for m in muestras:
			if int(m["estado"]) == 0:
				elegida = m
				break
		if elegida.is_empty():
			return
		destino = elegida["pos"]
		var id: int = elegida["id"]
		var util: int = UTILES[id] if _auto > 0 else (UTILES[id] + 1) % 3
		if herramienta != util:
			_cambiar()
	var diferencia: Vector2 = destino - posicion
	if carga < 0 and diferencia.length() < 9.0:
		accion = true
		return
	var rumbo: Vector2 = diferencia.normalized()
	for i in CANTIDADES[dificultad - 1]:
		var offset: Vector2 = CRATERES[i] - posicion
		var frente: float = offset.dot(rumbo)
		if frente > 0.0 and frente < minf(42.0, diferencia.length()):
			var lateral: float = offset.cross(rumbo)
			if absf(lateral) < RADIOS[dificultad - 1] + 9.0:
				var lado: float = 1.0 if lateral >= 0.0 else -1.0
				diferencia = rumbo * 10.0 + Vector2(-rumbo.y, rumbo.x) * lado * 24.0
				break
	var frenada: Vector2 = diferencia - velocidad * 0.23
	mando = Vector2(signf(frenada.x) if absf(frenada.x) > 2.5 else 0.0, signf(frenada.y) if absf(frenada.y) > 2.5 else 0.0).limit_length()


func _estallar(p: Vector2, color: Color, cantidad: int) -> void:
	for i in cantidad:
		_particulas.append({"p": p, "v": Vector2.from_angle(_azar.randf_range(0, TAU)) * _azar.randf_range(8, 38), "t": _azar.randf_range(0.25, 0.8), "c": color})


func _efectos(dt: float) -> void:
	_destello = maxf(0.0, _destello - dt)
	_sacudida = maxf(0.0, _sacudida - dt)
	_aviso_t = maxf(0.0, _aviso_t - dt)
	for i in range(_particulas.size() - 1, -1, -1):
		var p: Dictionary = _particulas[i]
		var t: float = float(p["t"]) - dt
		p["t"] = t
		p["p"] = Vector2(p["p"]) + Vector2(p["v"]) * dt
		if t <= 0.0:
			_particulas.remove_at(i)


func _r(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2(floorf(x), floorf(y), floorf(w), floorf(h)), color)


func _sprite(mapa: Array[String], p: Vector2, escala: int = 1) -> void:
	for y in mapa.size():
		var fila: String = mapa[y]
		for x in fila.length():
			var c: String = fila[x]
			if _pal.has(c):
				var color: Color = _pal[c]
				_r(p.x + x * escala, p.y + y * escala, escala, escala, color)


func _texto(t: String, x: float, y: float, color: Color, e: int = 1) -> void:
	var cx: float = x
	for letra in t:
		if _glifos.has(letra):
			var filas: PackedStringArray = _glifos[letra]
			for fy in 5:
				for fx in 3:
					if filas[fy][fx] == "#":
						_r(cx + fx * e, y + fy * e, e, e, color)
		cx += 4 * e


func _centro(t: String, y: float, color: Color, e: int = 1) -> void:
	_texto(t, (320 - t.length() * 4 * e) * 0.5, y, color, e)


func _muestra(id: int, p: Vector2, dispersa: bool = false) -> void:
	if id <= 1:
		for k in 15:
			var dx: float = float((k * 7) % 17 - 8)
			var dy: float = float((k * 3) % 7 - 3)
			if dispersa:
				dy += sin(reloj * 6.0 + k) * 3.0
			_r(p.x + dx, p.y + dy, 2 if id == 1 else 1, 1, Estilo.CREMA)
	elif id == 2:
		_sprite(ROCA, p - Vector2(3, 3))
	else:
		for k in 5:
			var desvio: float = sin(reloj * 8.0 + k) * 5.0 if dispersa else 0.0
			_r(p.x - 6 + desvio, p.y - 5 + k * 2, 12, 2, Estilo.CREMA if k % 2 == 0 else Estilo.NARANJA)
		_r(p.x - 7, p.y - 6, 1, 12, Estilo.PETROLEO)


func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(4, 4))
	_r(0, 0, 320, 180, Estilo.NOCHE)
	# Cielo y horizonte de lado a lado; el suelo alcanza el borde inferior.
	for i in 42:
		_r((i * 73) % 320, 18 + (i * 17) % 25, 1, 1, Estilo.CREMA)
	for x in range(0, 320, 4):
		var horizonte: int = floori(46 + sin(x * 0.04) * 3 + sin(x * 0.11) * 2)
		_r(x, horizonte, 4, 180 - horizonte, Estilo.TINTA)
		_r(x, horizonte, 4, 2, Estilo.PETROLEO)
	_r(278, 24, 9, 9, Estilo.CIAN)
	_r(276, 26, 13, 5, Estilo.CIAN)
	_r(280, 25, 4, 4, Estilo.PETROLEO)
	var temblor: Vector2 = Vector2(roundf(sin(reloj * 91.0) * 2), roundf(cos(reloj * 77.0))) if _sacudida > 0.0 else Vector2.ZERO
	draw_set_transform(temblor * 4, 0.0, Vector2(4, 4))
	for i in 180:
		var x: int = (i * 67) % 320
		var y: int = 53 + (i * 31) % 127
		_r(x, y, 2 if i % 3 else 4, 1, Color(Estilo.PETROLEO, 0.25))
	for p in _huellas:
		_r(p.x - 2, p.y, 1, 2, Estilo.TINTA_SUAVE)
		_r(p.x + 2, p.y + 1, 1, 2, Estilo.TINTA_SUAVE)
	for i in CANTIDADES[dificultad - 1]:
		var c: Vector2 = CRATERES[i]
		var r: int = int(RADIOS[dificultad - 1]) + 2
		for y in range(-r, r + 1):
			var ancho: int = int(sqrt(maxf(0, r * r - y * y)))
			_r(c.x - ancho, c.y + y, ancho * 2 + 1, 1, Estilo.PETROLEO)
			if absi(y) < r - 2:
				var dentro: int = int(sqrt(maxf(0, (r - 2) * (r - 2) - y * y)))
				_r(c.x - dentro, c.y + y, dentro * 2 + 1, 1, Estilo.TINTA)
		_r(c.x - r * 0.5, c.y - r + 1, r, 1, Estilo.CREMA)
	_sprite(CAJON, CAJA - Vector2(7, 5))
	for i in objetivo_total:
		_r(CAJA.x - 10 + i * 6, CAJA.y + 12, 4, 3, Estilo.CIAN if i < entregadas.size() else Estilo.PETROLEO)
	_texto("CAJA", CAJA.x - 8, CAJA.y - 12, Estilo.CIAN)
	for m in muestras:
		if int(m["estado"]) != 0:
			continue
		var p: Vector2 = m["pos"]
		var id: int = m["id"]
		_muestra(id, p, float(m["espera"]) > 0.0)
		if id == 3 and progreso > 0.0 and cercana >= 0 and int(muestras[cercana]["id"]) == id:
			_sprite(TUBO, p + Vector2(-2, -9 + progreso * 3.0))
			var golpe: float = 2.0 if fmod(progreso, 0.25) < 0.12 else 0.0
			_r(p.x + 6, p.y - 11 + golpe, 6, 2, Estilo.PETROLEO)
			_r(p.x + 8, p.y - 9 + golpe, 1, 5, Estilo.CREMA)
		_texto(str(id + 1), p.x - 1, p.y + 8, Estilo.DORADO)
		if dificultad == 1:
			var icono: Array[String] = [CUCHARON, PINZAS, TUBO][UTILES[id]]
			_sprite(icono, p + Vector2(10, -4))
	if carga >= 0:
		var d: Vector2 = CAJA - posicion
		for k in range(1, 6):
			var p: Vector2 = posicion + d.normalized() * float(k * 5)
			_r(p.x, p.y, 1, 1, Estilo.CIAN)
	_r(posicion.x - 4, posicion.y + 2, 9, 2, Estilo.TINTA_SUAVE)
	if _inmune <= 0.0 or fmod(_inmune, 0.4) < 0.2:
		_sprite(ASTRONAUTA, posicion - Vector2(4, 8 + roundf(altura)))
		var util: Array[String] = [CUCHARON, PINZAS, TUBO][herramienta]
		_sprite(util, posicion + Vector2(5, -5 - roundf(altura)))
		if carga >= 0:
			_r(posicion.x - 7, posicion.y - 6 - roundf(altura), 4, 5, Estilo.DORADO)
	if cercana >= 0 and carga < 0 and fase == 1:
		var m: Dictionary = muestras[cercana]
		var id: int = m["id"]
		var ancho: float = clampf(progreso / (1.7 if id == 3 else 0.7), 0.0, 1.0) * 18
		_r(posicion.x - 10, posicion.y - altura - 15, 20, 3, Estilo.PETROLEO)
		_r(posicion.x - 9, posicion.y - altura - 14, ancho, 1, Estilo.CIAN)
		_texto("ESP", posicion.x - 6, posicion.y + 7, Estilo.CIAN)
	for part in _particulas:
		var p: Vector2 = part["p"]
		var color: Color = part["c"]
		_r(p.x, p.y, 1, 1, color)
	if _aviso_t > 0.0:
		_r(4, 19, 312, 8, Estilo.NOCHE)
		_centro(_aviso, 20, Estilo.CORAL)
	if _destello > 0.0:
		_r(0, 46, 320, 134, Color(Estilo.CREMA, _destello * 0.6))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(4, 4))
	_hud()
	if fase == 0:
		_r(53, 60, 214, 64, Estilo.NOCHE)
		_centro("RECOGE Y LLEVA A LA CAJA", 66, Estilo.CREMA, 2)
		_sprite(CUCHARON, Vector2(82, 87), 2)
		_sprite(PINZAS, Vector2(116, 87), 2)
		_sprite(TUBO, Vector2(150, 87), 2)
		_texto("+", 181, 92, Estilo.CIAN, 2)
		_sprite(CAJON, Vector2(202, 89), 2)
		_centro("%s G" % fraccion, 113, Estilo.DORADO)
	elif fase == 2:
		_r(63, 72, 194, 28, Estilo.NOCHE)
		_centro("CARGA A SALVO", 77, Estilo.CIAN, 2)
		_centro("+%d" % int(puntos), 91, Estilo.DORADO)
	elif fase == 3:
		_r(56, 74, 208, 22, Estilo.NOCHE)
		_centro("SIN OXIGENO" if oxigeno <= 0 else "TRAJE SIN SELLOS", 80, Estilo.CORAL, 2)


func _hud() -> void:
	_texto(str(int(puntos)).pad_zeros(4), 4, 4, Estilo.CREMA, 2)
	_texto("O2", 43, 5, Estilo.CIAN)
	_r(55, 4, 59, 10, Estilo.PETROLEO)
	_r(56, 5, 57 * oxigeno / LIMITES[dificultad - 1], 8, Estilo.CORAL if oxigeno < 20 else Estilo.CIAN)
	_texto(str(ceili(oxigeno)).pad_zeros(3), 120, 4, Estilo.CREMA, 2)
	_texto("S", 145, 8, Estilo.CREMA)
	for i in 3:
		_r(156 + i * 10, 5, 7, 7, Estilo.CREMA if i < vidas else Estilo.TINTA_SUAVE)
		_r(158 + i * 10, 7, 3, 3, Estilo.NOCHE)
	_texto("%d/%d" % [entregadas.size(), objetivo_total], 198, 4, Estilo.DORADO, 2)
	_texto("N%d" % dificultad, 242, 5, Estilo.CIAN)
	_texto("ESC SALIR", 280, 5, Estilo.CREMA)
	var icono: Array[String] = [CUCHARON, PINZAS, TUBO][herramienta]
	_sprite(icono, Vector2(5, 168))
	_r(15, 166, 9, 9, Estilo.PETROLEO)
	_texto("E", 18, 168, Estilo.CIAN)
	_texto(HERRAMIENTAS[herramienta], 28, 168, Estilo.CIAN)
	_texto("ESP RECOGER", 106, 168, Estilo.CREMA)
	_texto("BOLSA A CAJA" if carga >= 0 else "%s G" % fraccion, 181, 168, Estilo.DORADO)
	_texto("WASD", 299, 168, Estilo.CREMA)
