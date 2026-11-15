extends "res://nucleo/minijuego.gd"

# Ocular de salon: escalas, deriva y exposicion son reglas de juego.
# Solo las cifras leidas de las fichas son mediciones astronomicas.
const DT: float = 1.0 / 120.0
const CAMPO: Vector2 = Vector2(320, 180)
const MUNDO: Vector2 = Vector2(640, 260)
const HORIZONTE: float = 244.0
const RADIO_LUNA: int = 52
const CENTRO: Vector2 = Vector2(160, 94)
const RASGOS: Array[String] = ["TERMINADOR", "LUZ CENICIENTA", "MARE CRISIUM"]
const CORAZON: Array[String] = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
const TIERRA: Array[String] = ["...pppp...", ".ppvvvvpp.", "ppvvvvvppp", "pppvvppppp", "ppppppvvpp", ".ppppvvpp.", "...pppp..."]
const TUBO: Array[String] = ["......cc", "....pppc", "..ppppp.", "ppppp...", ".pp.....", "..p.....", ".p.p....", "p...p..."]
const MAR: Array[String] = ["..###...", ".#####..", "#######.", "########", ".######.", "..####..", "....#..."]
const GLIFOS: Dictionary = {
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
	"6":"###/#../###/#.#/###", "7":"###/..#/..#/.#./.#.", "8":"###/#.#/###/#.#/###",
	"9":"###/#.#/###/..#/###", ".":".../.../.../.../.#.", ",":".../.../.../.#./#..",
	"/":"..#/..#/.#./#../#..", ":":".../.#./.../.#./...", "-":".../.../###/.../...",
	"%":"#.#/..#/.#./#../#.#", "+":".../.#./###/.#./...", "!":".#./.#./.#./.../.#.",
}

var etapa: int = 0 # 0 buscar, 1 enfoque, 2 registrar, 3 final
var rasgo: int = 0
var visor: Vector2 = Vector2(450, 62)
var velocidad: Vector2 = Vector2.ZERO
var mira: Vector2 = CENTRO
var luna_mundo: Vector2 = Vector2(114, 194)
var luna_centro: Vector2 = CENTRO
var diana: Vector2 = CENTRO
var iluminacion: float = 0.0
var altura: float = 0.0
var inclinacion: float = 0.0
var vidas: int = 3
var puntos: float = 0.0
var limite: float = 90.0
var margen: float = 8.0
var ventana_foco: float = 0.2
var enfoque: float = 0.0
var exposicion: float = 0.0
var exposicion_meta: float = 6.0
var fuera: float = 0.0
var mando: Vector2 = Vector2.ZERO
var accion: bool = false
var pulso: bool = false
var _auto: int = 0
var _acum: float = 0.0
var reloj: float = 0.0
var t_etapa: float = 0.0
var inmune: float = 0.0
var destello: float = 0.0
var sacudida: float = 0.0
var causa: String = ""
var ganado: bool = false
var aviso: String = ""
var aviso_t: float = 0.0
var estrellas: Array[Vector3] = []
var particulas: Array[Dictionary] = []
var azar: RandomNumberGenerator = RandomNumberGenerator.new()
var glifos: Dictionary = {}


func _init() -> void:
	pantalla_completa = true


func _preparar() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	# Las fichas son la unica fuente de las cifras mostradas y de la fase dibujada.
	var ficha: Dictionary = Juego.ficha("luna_12_noviembre")
	var patron: RegEx = RegEx.new()
	patron.compile("[0-9]+[,\\.][0-9]+")
	var cifras: Array[RegExMatch] = patron.search_all(String(ficha.get("texto", "")))
	if cifras.size() >= 2:
		iluminacion = float(cifras[0].get_string().replace(",", ".")) / 100.0
		altura = float(cifras[1].get_string().replace(",", "."))
	var sonrisa: Dictionary = Juego.ficha("luna_sonriente")
	var orientacion: Array[RegExMatch] = patron.search_all(String(sonrisa.get("texto", "")))
	if not orientacion.is_empty():
		inclinacion = deg_to_rad(float(orientacion[0].get_string().replace(",", ".")) - 180.0)
	luna_mundo.y = HORIZONTE - altura * 2.5
	limite = [100.0, 85.0, 75.0][dificultad - 1]
	margen = [10.0, 7.0, 5.0][dificultad - 1]
	ventana_foco = [0.23, 0.14, 0.09][dificultad - 1]
	exposicion_meta = [5.5, 7.0, 8.0][dificultad - 1]
	azar.seed = int(parametros.get("semilla", 1220))
	for i in 310:
		estrellas.append(Vector3(azar.randf_range(0, MUNDO.x), azar.randf_range(0, MUNDO.y), azar.randf()))
	for c in GLIFOS:
		var mapa: String = GLIFOS[c]
		glifos[c] = mapa.split("/")
	queue_redraw()


func _empezar() -> void:
	sonar("radio")


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0 or etapa == 3:
		return
	if evento.is_action_pressed("interactuar") or evento.is_action_pressed("saltar"):
		if not evento.is_echo():
			pulso = true
		get_viewport().set_input_as_handled()


func _paso(delta: float) -> void:
	_acum += delta
	while _acum >= DT and activo:
		_acum -= DT
		_tic(DT)
	queue_redraw()


func _tic(dt: float) -> void:
	reloj += dt
	t_etapa += dt
	inmune = maxf(0, inmune - dt)
	destello = maxf(0, destello - dt)
	sacudida = maxf(0, sacudida - dt)
	aviso_t = maxf(0, aviso_t - dt)
	_animar(dt)
	if etapa == 3:
		if t_etapa >= 1.4:
			var porcentaje: String = ("%.1f" % (iluminacion * 100)).replace(".", ",")
			var elevacion: String = ("%.1f" % altura).replace(".", ",")
			var dato: String = "Sol: %s %%; altura: %s grados; la Tierra ilumina la noche lunar." % [porcentaje, elevacion]
			terminar(ganado, roundf(puntos), dato if ganado else causa)
		return
	luna_centro = CENTRO + Vector2(sin(reloj * 0.75) * dificultad * 2.0, sin(reloj * 0.49) * dificultad)
	diana = _rasgo_visible()
	enfoque = 0.5 + 0.5 * sin(t_etapa * (1.5 + dificultad * 0.4))
	if _auto == 0:
		mando = Vector2(eje_x(), -eje_y()).limit_length(1)
		accion = Input.is_action_pressed("interactuar") or Input.is_action_pressed("saltar")
	else:
		_piloto()
	mando = mando.limit_length(1)
	var disparo: bool = pulso
	pulso = false
	if etapa == 0:
		velocidad = velocidad.move_toward(mando * 100.0, 650.0 * dt)
		visor += velocidad * dt
		visor = visor.clamp(Vector2(0, 0), MUNDO)
		if disparo:
			if visor.distance_to(luna_mundo) <= [10.0, 8.0, 6.0][dificultad - 1]:
				_cambiar(1)
				puntos += 100
				sonar("recoger")
			else:
				_golpe("La Luna quedó fuera del visor: busca la sonrisa baja al oeste.")
	elif etapa == 1:
		if disparo:
			if absf(enfoque - 0.5) <= ventana_foco:
				_cambiar(2)
				mira = CENTRO
				puntos += 200
				sonar("salto")
			else:
				_golpe("El borde quedó desenfocado: pulsa cuando la aguja cruce la franja nítida.")
	elif etapa == 2:
		velocidad = velocidad.move_toward(mando * 42.0, 500.0 * dt)
		mira = (mira + velocidad * dt).clamp(Vector2(9, 36), Vector2(310, 157))
		var dentro: bool = mira.distance_to(diana) <= margen
		if accion and dentro:
			var antes: int = int(exposicion)
			exposicion += dt
			fuera = maxf(0, fuera - dt * 3)
			puntos += dt * 10
			if int(exposicion) > antes:
				sonar("tic")
				_chispas(mira, Estilo.DORADO, 3)
			if exposicion >= exposicion_meta:
				_chispas(diana, Estilo.CIAN, 24)
				sonar("ok")
				puntos += 300
				rasgo += 1
				exposicion = 0
				fuera = 0
				# Gracia breve para soltar E y trasladarse hacia la siguiente diana.
				accion = false
				inmune = 1.2
				destello = 0.12
				if rasgo >= 3:
					_final(true, "")
		elif accion and inmune <= 0:
			fuera += dt
			if fuera >= [0.85, 0.65, 0.45][dificultad - 1]:
				_golpe("La exposición se movió fuera del rasgo: suelta E al trasladar la mira.")
		else:
			fuera = maxf(0, fuera - dt * 2)
	if reloj >= limite and etapa != 3:
		_final(false, "Se cerró la ventana de observación antes de registrar los tres rasgos lunares.")


func _rasgo_visible() -> Vector2:
	if rasgo == 0:
		return luna_centro + Vector2(-18, (1 - 2 * iluminacion) * sqrt(float(RADIO_LUNA * RADIO_LUNA - 324))).rotated(inclinacion)
	if rasgo == 1:
		return luna_centro + Vector2(-11, -11)
	return luna_centro + Vector2(19, 40)


func _cambiar(nueva: int) -> void:
	etapa = nueva
	t_etapa = 0
	velocidad = Vector2.ZERO
	destello = 0.15


func _golpe(motivo: String) -> void:
	if inmune > 0:
		return
	vidas -= 1
	inmune = 1.3
	sacudida = 0.25
	destello = 0.2
	exposicion = maxf(0, exposicion - 1.5)
	fuera = 0
	aviso = "SUELTA E AL MOVER" if etapa == 2 else ("ESPERA LA FRANJA" if etapa == 1 else "BAJA AL OESTE")
	aviso_t = 1.4
	sonar("error")
	_chispas(mira if etapa == 2 else CENTRO, Estilo.CORAL, 18)
	if vidas == 0:
		_final(false, motivo)


func _final(exito: bool, motivo: String) -> void:
	ganado = exito
	causa = motivo
	_cambiar(3)
	if exito:
		puntos += vidas * 100 + maxf(0, limite - reloj) * 5
		sonar("logro")
		_chispas(luna_centro, Estilo.DORADO, 45)


func _piloto() -> void:
	# Solo escribe las ordenes del jugador; nunca recoloca objetos ni concede aciertos.
	mando = Vector2.ZERO
	accion = false
	if _auto < 0:
		pulso = inmune <= 0 and t_etapa > 1.5
		return
	var error: Vector2 = (luna_mundo - visor) if etapa == 0 else (diana - mira)
	var correccion: Vector2 = error - velocidad * 0.10
	mando.x = signf(correccion.x) if absf(correccion.x) > 0.8 else 0.0
	mando.y = signf(correccion.y) if absf(correccion.y) > 0.8 else 0.0
	if etapa == 0:
		pulso = error.length() < 3 and velocidad.length() < 15
	elif etapa == 1:
		pulso = t_etapa > 1 and absf(enfoque - 0.5) < ventana_foco * 0.5
	elif etapa == 2:
		accion = error.length() < margen * 0.75


func _chispas(pos: Vector2, color: Color, cantidad: int) -> void:
	for i in cantidad:
		var v: Vector2 = Vector2.from_angle(azar.randf() * TAU) * azar.randf_range(8, 34)
		particulas.append({"p": pos, "v": v, "t": azar.randf_range(0.3, 0.9), "c": color})


func _animar(dt: float) -> void:
	for i in range(particulas.size() - 1, -1, -1):
		var p: Dictionary = particulas[i]
		var pos: Vector2 = p["p"]
		var v: Vector2 = p["v"]
		p["p"] = pos + v * dt
		p["t"] = float(p["t"]) - dt
		if float(p["t"]) <= 0:
			particulas.remove_at(i)


func _px(x: float, y: float, w: float, h: float, color: Color) -> void:
	draw_rect(Rect2(floorf(x), floorf(y), floorf(w), floorf(h)), color)


func _sprite(mapa: Variant, pos: Vector2, color: Color, escala: int = 1) -> void:
	for y in mapa.size():
		var fila: String = mapa[y]
		for x in fila.length():
			if fila[x] == ".":
				continue
			var tinta: Color = color
			if fila[x] == "v":
				tinta = Estilo.CREMA
			elif fila[x] == "c":
				tinta = Estilo.CIAN
			_px(pos.x + x * escala, pos.y + y * escala, escala, escala, tinta)


func _texto(t: String, x: float, y: float, color: Color, escala: int = 1) -> void:
	for c in t:
		if glifos.has(c):
			var filas: PackedStringArray = glifos[c]
			_sprite(filas, Vector2(x, y), color, escala)
		x += 4 * escala


func _cruz(p: Vector2, radio: float, color: Color) -> void:
	_px(p.x - radio, p.y, radio - 2, 1, color)
	_px(p.x + 3, p.y, radio - 2, 1, color)
	_px(p.x, p.y - radio, 1, radio - 2, color)
	_px(p.x, p.y + 3, 1, radio - 2, color)


func _anillo(p: Vector2, radio: float, color: Color) -> void:
	for i in 40:
		var a: float = TAU * i / 40
		_px(roundf(p.x + cos(a) * radio), roundf(p.y + sin(a) * radio), 1, 1, color)


func _luna(c: Vector2, r: int, nitida: bool) -> void:
	# Una elipse interior deja exactamente la fraccion iluminada de la ficha.
	var k: float = 1 - 2 * iluminacion
	for x in range(-r, r + 1):
		var borde: float = sqrt(maxf(0, r * r - x * x))
		for y in range(-int(borde), int(borde) + 1):
			var local: Vector2 = Vector2(x, y).rotated(-inclinacion)
			var luz: bool = local.y >= k * sqrt(maxf(0, r * r - local.x * local.x))
			var color: Color = Estilo.CREMA if luz else Estilo.PETROLEO.darkened(0.35)
			if not nitida and (x + y) % 3 == 0:
				color = color.lerp(Estilo.NOCHE, 0.45)
			_px(c.x + x, c.y + y, 1, 1, color)
	if r > 20 and nitida:
		_sprite(MAR, c + Vector2(15, 36), Estilo.TINTA_SUAVE)
		_sprite(["##..", "###.", ".###", "..##"], c + Vector2(-22, -10), Estilo.NOCHE)
		_sprite([".##", "###", "##."], c + Vector2(6, -20), Estilo.NOCHE)


func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0, Vector2(4, 4))
	_px(0, 0, CAMPO.x, CAMPO.y, Estilo.NOCHE)
	var desplazamiento: Vector2 = Vector2.ZERO
	if sacudida > 0:
		desplazamiento = Vector2(roundf(sin(reloj * 65) * 2), roundf(cos(reloj * 47)))
	draw_set_transform(desplazamiento * 4, 0, Vector2(4, 4))
	if etapa == 0:
		_dibujar_busqueda()
	else:
		for s in estrellas:
			var p: Vector2 = Vector2(fposmod(s.x, CAMPO.x), fposmod(s.y, CAMPO.y))
			_px(p.x, p.y, 1, 1, Estilo.PETROLEO)
		_luna(luna_centro, RADIO_LUNA, etapa != 1 or absf(enfoque - 0.5) < ventana_foco)
		if etapa == 1:
			_dibujar_foco()
		elif etapa == 2:
			_dibujar_registro()
	for p in particulas:
		var pos: Vector2 = p["p"]
		var color: Color = p["c"]
		_px(pos.x, pos.y, 1, 1, color)
	draw_set_transform(Vector2.ZERO, 0, Vector2(4, 4))
	_dibujar_hud()
	if etapa == 0 and t_etapa < 2.0:
		_px(59, 65, 202, 40, Estilo.TINTA)
		_sprite(TUBO, Vector2(148, 68), Estilo.CREMA, 2)
		_texto("ENCUENTRA LA SONRISA DEL OESTE", 66, 93, Estilo.CREMA)
	if etapa == 3:
		_px(86, 80, 148, 22, Estilo.TINTA)
		_texto("TRES RASGOS" if ganado else "FIN DE SESION", 116 if ganado else 108, 87, Estilo.DORADO if ganado else Estilo.CORAL, 2)
	if aviso_t > 0:
		_px(90, 156, 140, 9, Estilo.TINTA)
		_texto(aviso, 160 - aviso.length() * 2, 158, Estilo.CORAL)
	if destello > 0:
		_px(0, 0, CAMPO.x, CAMPO.y, Color(Estilo.CORAL if inmune > 0 else Estilo.CREMA, destello))


func _dibujar_busqueda() -> void:
	var offset: Vector2 = CENTRO - visor
	for s in estrellas:
		var p: Vector2 = Vector2(s.x, s.y) + offset
		if p.y >= 0 and p.y < CAMPO.y:
			_px(p.x, p.y, 1, 1, Estilo.CREMA if s.z > 0.7 else Estilo.PETROLEO)
	var horizonte: float = HORIZONTE + offset.y
	if horizonte < CAMPO.y:
		_px(0, maxf(0, horizonte), CAMPO.x, CAMPO.y - maxf(0, horizonte), Estilo.TINTA)
		for x in range(0, int(CAMPO.x), 12):
			_px(x, horizonte - (x % 7), 8, 9, Estilo.TINTA)
	_luna(luna_mundo + offset, 8, true)
	_cruz(CENTRO, 13, Estilo.CIAN if inmune <= 0 or fmod(reloj, 0.3) > 0.15 else Estilo.CORAL)
	if visor.distance_to(luna_mundo) < 12:
		_texto("E", 178, 89, Estilo.CIAN, 2)
	# Buscador: mapa de todo el recorrido; el anillo indica el visor.
	_px(246, 31, 70, 41, Estilo.CREMA)
	_px(247, 32, 68, 39, Estilo.NOCHE)
	var m: Vector2 = Vector2(251, 37) + luna_mundo * Vector2(58.0 / MUNDO.x, 28.0 / MUNDO.y)
	_luna(m, 2, true)
	var v: Vector2 = Vector2(251, 37) + visor * Vector2(58.0 / MUNDO.x, 28.0 / MUNDO.y)
	_anillo(v, 4, Estilo.CIAN)
	_texto("O", 250, 65, Estilo.NARANJA)
	_texto("E", 309, 65, Estilo.NARANJA)
	_texto(("%.1f ALT" % (maxf(0, HORIZONTE - visor.y) / 2.5)).replace(".", ","), 5, 156, Estilo.CREMA)
	_sprite(TUBO, Vector2(8, 141), Estilo.CREMA, 1)


func _dibujar_foco() -> void:
	_texto("BORROSO", 22, 87, Estilo.PETROLEO)
	_texto("NITIDO", 260, 87, Estilo.CREMA)
	_px(45, 143, 230, 10, Estilo.TINTA)
	_px(50, 145, 220, 6, Estilo.PETROLEO)
	_px(160 - ventana_foco * 220, 145, ventana_foco * 440, 6, Estilo.DORADO)
	_px(50 + enfoque * 220, 142, 2, 12, Estilo.CIAN)
	_cruz(luna_centro, 58, Estilo.CIAN)
	_texto("E", 158, 157, Estilo.CIAN)


func _dibujar_registro() -> void:
	var color: Color = Estilo.CIAN if mira.distance_to(diana) <= margen else Estilo.NARANJA
	_anillo(diana, margen, color)
	_texto(str(rasgo + 1), diana.x + margen + 3, diana.y - 2, color)
	if inmune <= 0 or fmod(reloj, 0.3) > 0.15:
		_cruz(mira, 7, Estilo.CIAN)
	_px(246, 98, 65, 7, Estilo.PETROLEO)
	_px(247, 99, 63 * minf(1, exposicion / exposicion_meta), 5, Estilo.DORADO)
	_texto("MANTEN E", 258, 88, Estilo.CIAN)
	_texto("%d/3" % rasgo, 262, 113, Estilo.CREMA, 2)
	for i in 3:
		_texto("+" if i < rasgo else "-", 254 + i * 19, 139, Estilo.DORADO if i < rasgo else Estilo.PETROLEO, 2)
	if rasgo == 1:
		_sprite(TIERRA, Vector2(19, 101), Estilo.PETROLEO, 3)
		_texto("TIERRA", 22, 131, Estilo.CREMA)
		# Luz reflejada: la flecha sale de la Tierra y llega a la noche lunar.
		for i in 15:
			var f: float = fposmod(reloj * 0.5 + i / 15.0, 1)
			var p: Vector2 = Vector2(52, 108).lerp(diana, f)
			_px(p.x, p.y, 2, 1, Estilo.CREMA)
		_texto("SOL", 26, 67, Estilo.DORADO)
		_texto("+", 25, 77, Estilo.DORADO, 2)
		for i in 4:
			_px(33, 88 + fposmod(reloj * 9 + i * 3, 12), 1, 2, Estilo.DORADO)


func _dibujar_hud() -> void:

	_texto("%05d" % int(puntos), 4, 4, Estilo.CREMA, 2)
	for i in 3:
		_sprite(CORAZON, Vector2(136 + i * 12, 5), Estilo.CORAL if i < vidas else Estilo.TINTA_SUAVE)
	_texto("%02d" % maxi(0, ceili(limite - reloj)), 292, 4, Estilo.CREMA, 2)
	_texto("TIEMPO", 257, 6, Estilo.PAPEL)

	var orden: String = "BUSCA LA SONRISA BAJA AL OESTE"
	if etapa == 1:
		orden = "E EN LA FRANJA NITIDA"
	elif etapa == 2:
		orden = RASGOS[mini(rasgo, 2)]
	_texto(orden, 160 - orden.length() * 2, 21, Estilo.CREMA)

	_texto("WASD MOVER", 5, 170, Estilo.CIAN)
	_texto("E FOCO / REGISTRAR", 113, 170, Estilo.CREMA)
	_texto("ESC SALIR", 279, 170, Estilo.CREMA)
