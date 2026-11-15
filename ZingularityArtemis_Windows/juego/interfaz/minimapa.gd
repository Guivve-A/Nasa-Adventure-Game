extends Control

# Minimapa de navegacion (arriba a la derecha): «donde estoy y a donde voy». DISENO PROPIO Y PROVISIONAL (Fase 7
# sin validar): una carta de navegacion de a bordo dibujada por codigo con la paleta de interfaz/estilo.gd.
#
# - Norte arriba, como la camara: -Z es arriba y +X la derecha. La protagonista en el centro, como una flecha
#   que apunta hacia donde mira; Orbita, un punto naranja.
# - La forma del lugar: al entrar en una zona se sondea su suelo de colision con rayos (unos cuadros, sin parar el
#   juego) y se rellena desde la protagonista lo que se puede pisar. El disco dibuja ese suelo con su contorno de
#   tinta clara, los muebles y muros como bloques rayados y, en terreno con relieve, curvas de nivel cada metro.
#   Una zona puede dar su propia silueta con la variable opcional silueta_minimapa (PackedVector2Array en XZ).
# - Umbrales: estrella cian (hueca si esta cerrada). Interactuables habilitados, con un glifo por tipo: tarea de una
#   mision (rombo cian), persona o animal (punto naranja), algo que se recoge (triangulo claro), dato o lectura
#   (hoja de papel). Una zona puede forzar el tipo con set_meta("minimapa", "tarea"|"persona"|"recoger"|"dato").
# - El objetivo del paso en curso (Juego.destino_actual()): rombo dorado que pulsa; fuera del radio queda pegado
#   al borde con una flecha. Debajo, «a donde · distancia» (en dos lineas si no cabe).
# - Si el paso se cumple en otra zona, senala el umbral (o el objeto) de ESTA zona que acerca a ella, con una
#   busqueda en anchura sobre las rutas de datos/mapa.json.
# - En el mundo, un rombo dorado alargado flota sobre el destino, siempre encima de la geometria, con un hilo de
#   luz que baja hasta el punto (compensa la inclinacion 2.5D, como la marca cian).
# - Escala: que quepa zona.limites; una zona puede fijarla con la variable opcional radio_minimapa (metros).
# - Tecla N (accion "minimapa"): tamano normal o grande. Se oculta con menus, dialogos, carga, minijuegos y mapa.
# - Rendimiento: el fondo y el aro se dibujan solo al cambiar de tamano; puntos y carta se refrescan a 30 Hz.

const Estilo := preload("res://interfaz/estilo.gd")
const Materiales := preload("res://nucleo/materiales.gd")

const RADIO_PX := 80.0
const RADIO_PX_GRANDE := 150.0
const RADIO_POR_DEFECTO := 16.0
const REFRESCO := 0.25                 # s entre busquedas del destino y de los puntos
const CUADRO := 1.0 / 30.0             # s entre redibujos de lo que se mueve
const ANCHO_ROTULO := 250.0
const CELDAS_MAX := 112                # lado maximo de la carta en celdas
const RAYOS_POR_CUADRO := 700
const LATON := Color("a77f2e")         # el dorado de la paleta, apagado: bisel de laton del aro
const VERBOS_PERSONA := ["Hablar", "Observar", "Saludar", "Preguntar", "Acariciar"]
const VERBOS_RECOGER := ["Recoger", "Tomar", "Coger"]

const SHADER_CARTA := """
shader_type canvas_item;
uniform vec2 origen;
uniform vec2 tam = vec2(1.0);
uniform vec2 centro;
uniform float radio_m = 16.0;
uniform float rango = 0.0;
uniform float alfa = 0.0;
uniform vec4 c_suelo : source_color;
uniform vec4 c_borde : source_color;
uniform vec4 c_bloque : source_color;
uniform vec4 c_raya : source_color;
uniform vec4 c_curva : source_color;

void fragment() {
	vec2 d = UV * 2.0 - 1.0;
	float r = length(d);
	float dentro = 1.0 - smoothstep(0.955, 0.975, r);
	vec2 uv = (centro + d * radio_m - origen) / tam;
	float en_carta = step(0.0, uv.x) * step(uv.x, 1.0) * step(0.0, uv.y) * step(uv.y, 1.0);
	vec4 m = texture(TEXTURE, clamp(uv, vec2(0.0), vec2(1.0)));
	float w = m.r;
	float fw = max(fwidth(w), 0.0001);
	float suelo = smoothstep(0.5 - fw, 0.5 + fw, w);
	float borde = 1.0 - smoothstep(0.0, fw * 1.8, abs(w - 0.5));
	float b = m.g;
	float fb = max(fwidth(b), 0.0001);
	float bloque = smoothstep(0.5 - fb, 0.5 + fb, b);
	float raya = step(0.62, fract((FRAGCOORD.x + FRAGCOORD.y) / 5.0)) * bloque;
	float h = m.b * rango;
	float fh = max(fwidth(h), 0.0001);
	float curva = (1.0 - smoothstep(0.0, fh * 1.3, abs(fract(h + 0.5) - 0.5))) * step(0.6, rango) * suelo;
	vec4 col = vec4(c_suelo.rgb, c_suelo.a * suelo);
	col.rgb = mix(col.rgb, c_curva.rgb, curva * c_curva.a);
	col = mix(col, c_bloque, bloque * (1.0 - suelo));
	col.rgb = mix(col.rgb, c_raya.rgb, raya * c_raya.a * (1.0 - suelo));
	col = mix(col, vec4(c_borde.rgb, 1.0), borde * c_borde.a);
	COLOR = vec4(col.rgb, col.a * dentro * en_carta * alfa);
}
"""

var grande := false
var radio_m := RADIO_POR_DEFECTO       # metros que caben del centro al borde
# lo que senala ahora (las pruebas lo leen)
var tiene_objetivo := false
var objetivo_nombre := ""
var objetivo_distancia := 0.0
var objetivo_pos := Vector3.ZERO
var carta_lista := false               # la forma del lugar ya esta sondeada

var _fondo: Control
var _carta: TextureRect
var _aro: Control
var _capa: Control
var _rotulo: Label
var _rotulo_dist: Label
var _rotulo_visto := ""
var _rotulo_r := 0.0
var _rotulo_dos := false
var _nodo_objetivo: Node3D = null
var _umbrales: Array = []
var _puntos: Array = []                # [nodo, tipo]
var _espera := 0.0
var _cuadro := 0.0
var _t := 0.0
var _zona_vista: Node = null
var _rutas: Array = []
var _tareas := {}                      # nombres de nodo que son destino de algun paso de mision
var _marca: Node3D = null
var _rombo3d: Node3D = null
var _haz: MeshInstance3D = null
# carta de la zona (sondeo del suelo de colision)
var _carta_mat: ShaderMaterial
var _carta_zona: Node = null
var _sondeando := false
var _origen := Vector2.ZERO
var _celda := 0.5
var _n := Vector2i.ZERO
var _fila := 0
var _ref_y := 0.0
var _altos := PackedFloat32Array()
var _normales := PackedFloat32Array()
var _carta_alfa := 0.0
var _silueta := PackedVector2Array()


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_fondo = _lienzo(_dibujar_fondo)
	_carta = TextureRect.new()
	_carta.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_carta.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_carta.stretch_mode = TextureRect.STRETCH_SCALE
	_carta.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	var sh := Shader.new()
	sh.code = SHADER_CARTA
	_carta_mat = ShaderMaterial.new()
	_carta_mat.shader = sh
	_carta_mat.set_shader_parameter("c_suelo", Color(Estilo.PETROLEO, 0.62))
	_carta_mat.set_shader_parameter("c_borde", Color(Estilo.PAPEL, 0.85))
	_carta_mat.set_shader_parameter("c_bloque", Color(Estilo.TINTA, 0.72))
	_carta_mat.set_shader_parameter("c_raya", Color(Estilo.PAPEL_SOMBRA, 0.28))
	_carta_mat.set_shader_parameter("c_curva", Color(Estilo.PAPEL, 0.22))
	_carta.material = _carta_mat
	_carta.visible = false
	add_child(_carta)
	_aro = _lienzo(_dibujar_aro)
	_capa = _lienzo(_dibujar_capa)
	_rotulo = _linea_rotulo(16, Estilo.PAPEL, 600)
	_rotulo_dist = _linea_rotulo(18, Estilo.CREMA, 700)
	var mapa: Variant = Juego.leer_json("res://datos/mapa.json")
	if mapa is Dictionary:
		_rutas = mapa.get("rutas", [])
	Juego.misiones_cambiadas.connect(func(): _espera = 0.0)


func _leer_tareas() -> void:
	for m in Juego.misiones:
		for p in m.get("pasos", []):
			var nombre := String((p as Dictionary).get("destino", ""))
			if nombre != "" and not nombre.begins_with("@"):
				_tareas[nombre] = true


func _lienzo(dibujo: Callable) -> Control:
	var c := Control.new()
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.draw.connect(dibujo)
	add_child(c)
	return c


func _linea_rotulo(tam: int, color: Color, peso: int) -> Label:
	var l := Estilo.linea("", tam, color, peso)
	l.add_theme_color_override("font_outline_color", Estilo.TINTA)
	l.add_theme_constant_override("outline_size", 6)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.clip_text = true
	l.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	add_child(l)
	return l


func radio_px() -> float:
	return RADIO_PX_GRANDE if grande else RADIO_PX


func alto_total() -> float:
	# alto que ocupa (disco y rotulo): el HUD coloca el inventario debajo
	var alto := radio_px() * 2.0 + 6.0
	if _rotulo.visible:
		alto += 24.0
	if _rotulo_dist.visible:
		alto += 24.0
	return alto


func _input(evento: InputEvent) -> void:
	if is_visible_in_tree() and evento.is_action_pressed("minimapa"):
		grande = not grande
		Audio.sonar("tic")
		_espera = 0.0
		get_viewport().set_input_as_handled()


func _debe_verse() -> bool:
	if Zonas.actual == null or Zonas.ocupado or Zonas.jugador == null:
		return false
	var i: Node = Interfaz
	for nombre in ["dialogo", "anfitrion", "pausa", "cuaderno", "menu", "carga", "mapa"]:
		var c: Variant = i.get(nombre)
		if c != null and (c as Control).visible:
			return false
	return true


func _process(delta: float) -> void:
	_t += delta
	var hay := Zonas.actual != null and Zonas.jugador != null and not Zonas.ocupado
	var ver := hay and _debe_verse()
	visible = ver
	if not hay:
		tiene_objetivo = false
		_nodo_objetivo = null
		_ver_marca(false)
		return
	var r := radio_px()
	var lado := Vector2(r * 2.0, r * 2.0)
	if _fondo.size != lado:
		for c in [_fondo, _carta, _aro, _capa]:
			(c as Control).size = lado
		_fondo.queue_redraw()
		_aro.queue_redraw()
		_cuadro = 0.0
	if Zonas.actual != _zona_vista:
		_zona_vista = Zonas.actual
		_espera = 0.0
	if Zonas.actual != _carta_zona:
		_empezar_carta()
	_espera -= delta
	if _espera <= 0.0:
		actualizar_ahora()
	_medir_objetivo()
	_poner_rotulo(r)
	size = Vector2(r * 2.0, alto_total())
	if ver:
		_mover_marca()
		if carta_lista and _carta_alfa < 1.0:
			_carta_alfa = minf(1.0, _carta_alfa + delta * 3.0)
		_cuadro -= delta
		if _cuadro <= 0.0:
			_cuadro = CUADRO
			_refrescar_carta()
			_capa.queue_redraw()
	else:
		_ver_marca(false)


func _poner_rotulo(r: float) -> void:
	_rotulo.visible = tiene_objetivo
	_rotulo_dist.visible = false
	if not tiene_objetivo:
		return
	var metros := _metros(objetivo_distancia)
	var completo := "%s · %s" % [objetivo_nombre, metros]
	if completo == _rotulo_visto and is_equal_approx(r, _rotulo_r):
		_rotulo_dist.visible = _rotulo_dos
		return
	_rotulo_visto = completo
	_rotulo_r = r
	var fuente := Estilo.fuente(600)
	var ancho := fuente.get_string_size(completo, HORIZONTAL_ALIGNMENT_LEFT, -1, 16).x + 14.0
	if ancho <= ANCHO_ROTULO:
		_rotulo.text = completo
	else:
		# no cabe en una linea: el nombre arriba (recortado con puntos suspensivos) y la distancia debajo
		_rotulo.text = objetivo_nombre
		ancho = minf(fuente.get_string_size(objetivo_nombre, HORIZONTAL_ALIGNMENT_LEFT, -1, 16).x + 14.0, ANCHO_ROTULO)
		_rotulo_dist.visible = true
		_rotulo_dist.text = metros
	# centrado bajo el disco, pero sin salirse por la derecha de la pantalla
	var x := minf(r - ancho * 0.5, r * 2.0 - ancho)
	_rotulo.size = Vector2(ancho, 24.0)
	_rotulo.position = Vector2(x, r * 2.0 + 2.0)
	if _rotulo_dist.visible:
		_rotulo_dist.size = Vector2(ancho, 24.0)
		_rotulo_dist.position = Vector2(x, r * 2.0 + 24.0)
	_rotulo_dos = _rotulo_dist.visible


func actualizar_ahora() -> void:
	# vuelve a buscar la escala, los puntos y el destino (cada REFRESCO s, o al instante desde las pruebas)
	_espera = REFRESCO
	if Zonas.actual == null or Zonas.jugador == null:
		return
	if _tareas.is_empty():
		_leer_tareas()
	_escala()
	_recoger_puntos()
	_resolver_objetivo()
	_medir_objetivo()


func _medir_objetivo() -> void:
	var j: Node3D = Zonas.jugador
	if j != null and _nodo_objetivo != null and is_instance_valid(_nodo_objetivo) and _nodo_objetivo.is_inside_tree():
		objetivo_pos = _nodo_objetivo.global_position
		objetivo_distancia = Vector2(objetivo_pos.x - j.global_position.x, objetivo_pos.z - j.global_position.z).length()
		tiene_objetivo = true
	else:
		tiene_objetivo = false


static func _metros(d: float) -> String:
	if d >= 10.0:
		return "%d m" % int(round(d))
	return ("%.1f m" % d).replace(".", ",")


# ------------------------------------------------------------------ escala y puntos

func _escala() -> void:
	var zona: Node = Zonas.actual
	var propio: Variant = zona.get("radio_minimapa")
	var r := RADIO_POR_DEFECTO
	if propio != null and float(propio) > 0.0:
		r = float(propio)
	else:
		var lim: Variant = zona.get("limites")
		if lim is Rect2 and (lim as Rect2).has_area():
			var rect: Rect2 = lim
			r = clampf(rect.size.length() * 0.5 + 3.5, 4.5, 24.0)
	radio_m = r * (1.5 if grande else 1.0)


func _de_la_zona(n: Node) -> bool:
	return n != null and is_instance_valid(n) and n.is_inside_tree() and Zonas.actual.is_ancestor_of(n)


func _recoger_puntos() -> void:
	_umbrales.clear()
	_puntos.clear()
	for u in get_tree().get_nodes_in_group("umbrales"):
		if _de_la_zona(u) and (u as Node3D).is_visible_in_tree():
			_umbrales.append(u)
	for i in get_tree().get_nodes_in_group("interactuables"):
		if not _de_la_zona(i) or not bool(i.get("habilitado")) or int(i.get("prioridad")) < 0:
			continue
		_puntos.append([i, _tipo_de(i)])


func _tipo_de(n: Node) -> String:
	# tarea | persona | recoger | dato (la zona puede forzarlo con set_meta("minimapa", ...))
	var propio := String(n.get_meta("minimapa", ""))
	if propio != "":
		return propio
	if _tareas.has(String(n.name)):
		return "tarea"
	var verbo := String(n.get("texto"))
	for v in VERBOS_PERSONA:
		if verbo.begins_with(v):
			return "persona"
	for v in VERBOS_RECOGER:
		if verbo.begins_with(v):
			return "recoger"
	return "dato"


# ------------------------------------------------------------------ a donde voy

func _resolver_objetivo() -> void:
	_nodo_objetivo = null
	objetivo_nombre = ""
	var destino: Dictionary = Juego.destino_actual()
	if destino.is_empty():
		return
	var zona_paso := String(destino.get("zona", ""))
	var nombre := String(destino.get("destino", ""))
	var aqui := Zonas.id_actual
	if zona_paso == "" or zona_paso == aqui:
		if nombre == "":
			return
		if nombre == "@orbita":
			if Zonas.companero != null and Zonas.companero.visible:
				_nodo_objetivo = Zonas.companero
				objetivo_nombre = "Órbita"
			return
		var nodo := _buscar(nombre)
		if nodo != null:
			_nodo_objetivo = nodo
			objetivo_nombre = _nombre_de(nodo)
		return
	# el paso es de otra zona: la salida de esta zona que acerca a ella
	var siguiente := _siguiente_zona(aqui, zona_paso)
	if siguiente == "":
		return
	var salida := _salida_hacia(aqui, siguiente)
	if salida != null:
		_nodo_objetivo = salida
		objetivo_nombre = _nombre_de(salida)


func _buscar(nombre: String) -> Node3D:
	var zona: Node = Zonas.actual
	var n: Node = zona.get_node_or_null(nombre)
	if n == null:
		n = zona.find_child(nombre, true, false)
	if n is Node3D and (n as Node3D).is_visible_in_tree():
		if n.is_in_group("interactuables") and not bool(n.get("habilitado")):
			return null
		return n
	return null


func _nombre_de(n: Node) -> String:
	if n.is_in_group("umbrales"):
		var e := String(n.get("etiqueta"))
		return e if e != "" else "Salida"
	var t := String(n.get("texto"))
	return t if t != "" else String(n.name)


func _ruta_abierta(r: Dictionary) -> bool:
	if bool(Juego.bandera("visita_libre")):
		return true
	for b in r.get("requiere", []):
		if not bool(Juego.bandera(String(b))):
			return false
	return true


func _vecinos(id: String) -> Array:
	var lista: Array = []
	for r in _rutas:
		var ruta: Dictionary = r
		if not _ruta_abierta(ruta):
			continue
		var de := String(ruta.get("de", ""))
		var a := String(ruta.get("a", ""))
		if de == id:
			lista.append(a)
		elif a == id and not bool(ruta.get("solo_ida", false)) and not bool(ruta.get("sueno", false)):
			lista.append(de)
	if id == "luna" and not lista.has("habitacion"):
		lista.append("habitacion")       # la caja de carton despierta en la cama
	return lista


func _siguiente_zona(desde: String, hasta: String) -> String:
	# busqueda en anchura: devuelve la primera zona del camino mas corto
	var previo := {desde: ""}
	var cola: Array = [desde]
	while not cola.is_empty():
		var z: String = cola.pop_front()
		if z == hasta:
			break
		for v in _vecinos(z):
			if previo.has(v):
				continue
			# desde aqui mismo, solo vale una salida que exista de verdad en la zona
			if z == desde and _salida_hacia(desde, String(v)) == null:
				continue
			previo[v] = z
			cola.append(v)
	if not previo.has(hasta):
		return ""
	var paso := hasta
	while String(previo[paso]) != desde:
		paso = previo[paso]
	return paso


func _salida_hacia(aqui: String, siguiente: String) -> Node3D:
	if aqui == "habitacion" and siguiente == "luna":
		return _buscar("Cama")
	if aqui == "luna" and siguiente == "habitacion":
		return _buscar("Caja")
	var cerrada: Node3D = null
	for u in get_tree().get_nodes_in_group("umbrales"):
		if not _de_la_zona(u) or String(u.get("destino_zona")) != siguiente or not (u as Node3D).is_visible_in_tree():
			continue
		if aqui == "mirador" and siguiente == "habitacion" and String(u.name) != "AtajoFaroles":
			continue
		if u.abierto():
			return u
		cerrada = u
	if aqui == "mirador" and siguiente == "habitacion":
		return null          # el atajo de los faroles aun cerrado: se vuelve por el sendero
	return cerrada


# ------------------------------------------------------------------ carta de la zona (forma del lugar)

func _empezar_carta() -> void:
	# sondea el suelo de colision de la zona: unos cuadros de rayos (RAYOS_POR_CUADRO cada uno), sin parar el juego
	_carta_zona = Zonas.actual
	carta_lista = false
	_carta_alfa = 0.0
	_carta.visible = false
	_sondeando = false
	_silueta = PackedVector2Array()
	var propia: Variant = _carta_zona.get("silueta_minimapa")
	if propia is PackedVector2Array and (propia as PackedVector2Array).size() >= 3:
		_silueta = propia
		carta_lista = true
		return
	var j: Node3D = Zonas.jugador
	var caja := Rect2(Vector2(j.global_position.x, j.global_position.z), Vector2.ZERO)
	var lim: Variant = _carta_zona.get("limites")
	if lim is Rect2 and (lim as Rect2).has_area():
		caja = caja.merge(lim)
	for grupo in ["umbrales", "interactuables"]:
		for n in get_tree().get_nodes_in_group(grupo):
			if _de_la_zona(n):
				var p: Vector3 = (n as Node3D).global_position
				caja = caja.expand(Vector2(p.x, p.z))
	var entradas: Variant = _carta_zona.get("entradas")
	if entradas is Dictionary:
		for e in (entradas as Dictionary).values():
			var p: Vector3 = (e as Dictionary).get("pos", Vector3.ZERO)
			caja = caja.expand(Vector2(p.x, p.z))
	caja = caja.grow(4.0)
	_celda = maxf(0.25, maxf(caja.size.x, caja.size.y) / float(CELDAS_MAX))
	_n = Vector2i(mini(CELDAS_MAX, ceili(caja.size.x / _celda)), mini(CELDAS_MAX, ceili(caja.size.y / _celda)))
	_origen = caja.get_center() - Vector2(_n) * _celda * 0.5
	_ref_y = j.global_position.y
	_altos.resize(_n.x * _n.y)
	_altos.fill(NAN)
	_normales.resize(_n.x * _n.y)
	_normales.fill(0.0)
	_fila = 0
	_sondeando = true


func _physics_process(_delta: float) -> void:
	if not _sondeando:
		return
	if Zonas.actual != _carta_zona or Zonas.jugador == null:
		_sondeando = false
		return
	var espacio := Zonas.jugador.get_world_3d().direct_space_state
	var consulta := PhysicsRayQueryParameters3D.new()
	consulta.collision_mask = 1
	var filas := maxi(1, RAYOS_POR_CUADRO / maxi(1, _n.x))
	for f in filas:
		if _fila >= _n.y:
			break
		var z := _origen.y + (float(_fila) + 0.5) * _celda
		for i in _n.x:
			var x := _origen.x + (float(i) + 0.5) * _celda
			consulta.from = Vector3(x, _ref_y + 12.0, z)
			consulta.to = Vector3(x, _ref_y - 20.0, z)
			var golpe := espacio.intersect_ray(consulta)
			if not golpe.is_empty():
				var k := _fila * _n.x + i
				_altos[k] = (golpe["position"] as Vector3).y
				_normales[k] = (golpe["normal"] as Vector3).y
		_fila += 1
	if _fila >= _n.y:
		_sondeando = false
		_cerrar_carta()


func _cerrar_carta() -> void:
	# relleno desde la protagonista: suelo = celdas alcanzables sin escalon alto; bloque = lo que sobresale junto a el
	var total := _n.x * _n.y
	var tol := clampf(_celda * 0.8, 0.3, 0.9)
	var suelo := PackedByteArray()
	suelo.resize(total)
	suelo.fill(0)
	var j: Node3D = Zonas.jugador
	var cj := Vector2i(int((j.global_position.x - _origen.x) / _celda), int((j.global_position.z - _origen.y) / _celda))
	var inicio := -1
	var mejor := 99.0
	for dz in range(-4, 5):
		for dx in range(-4, 5):
			var c := cj + Vector2i(dx, dz)
			if c.x < 0 or c.y < 0 or c.x >= _n.x or c.y >= _n.y:
				continue
			var k := c.y * _n.x + c.x
			var dh := absf(_altos[k] - j.global_position.y)
			if not is_nan(_altos[k]) and _normales[k] > 0.5 and dh < 0.7:
				var puntaje := dh + Vector2(dx, dz).length() * 0.1
				if puntaje < mejor:
					mejor = puntaje
					inicio = k
	if inicio < 0:
		return
	var cola := PackedInt32Array([inicio])
	suelo[inicio] = 1
	var cabeza := 0
	var hmin := _altos[inicio]
	var hmax := hmin
	var lados := [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
	while cabeza < cola.size():
		var k := cola[cabeza]
		cabeza += 1
		var c := Vector2i(k % _n.x, k / _n.x)
		for l in lados:
			var v: Vector2i = c + l
			if v.x < 0 or v.y < 0 or v.x >= _n.x or v.y >= _n.y:
				continue
			var kv := v.y * _n.x + v.x
			if suelo[kv] != 0 or is_nan(_altos[kv]) or _normales[kv] < 0.5:
				continue
			if absf(_altos[kv] - _altos[k]) > tol:
				continue
			suelo[kv] = 1
			hmin = minf(hmin, _altos[kv])
			hmax = maxf(hmax, _altos[kv])
			cola.append(kv)
	# bloques: lo que sobresale del suelo vecino, hasta 6 celdas hacia dentro (muebles, muros, rocas)
	var bloque := PackedByteArray()
	bloque.resize(total)
	bloque.fill(0)
	var base := PackedFloat32Array()
	base.resize(total)
	var dist := PackedByteArray()
	dist.resize(total)
	var cola2 := PackedInt32Array()
	for k in total:
		if suelo[k] != 0:
			base[k] = _altos[k]
			cola2.append(k)
	cabeza = 0
	while cabeza < cola2.size():
		var k := cola2[cabeza]
		cabeza += 1
		if dist[k] >= 6:
			continue
		var c := Vector2i(k % _n.x, k / _n.x)
		for l in lados:
			var v: Vector2i = c + l
			if v.x < 0 or v.y < 0 or v.x >= _n.x or v.y >= _n.y:
				continue
			var kv := v.y * _n.x + v.x
			if suelo[kv] != 0 or bloque[kv] != 0 or is_nan(_altos[kv]):
				continue
			if _altos[kv] < base[k] + 0.25:
				continue
			bloque[kv] = 1
			base[kv] = base[k]
			dist[kv] = dist[k] + 1
			cola2.append(kv)
	var rango := hmax - hmin
	var img := Image.create(_n.x, _n.y, false, Image.FORMAT_RGBA8)
	for k in total:
		var h := 0.0
		if suelo[k] != 0 and rango > 0.001:
			h = (_altos[k] - hmin) / rango
		img.set_pixel(k % _n.x, k / _n.x, Color(float(suelo[k]), float(bloque[k]), h, 1.0))
	_carta.texture = ImageTexture.create_from_image(img)
	_carta_mat.set_shader_parameter("origen", _origen)
	_carta_mat.set_shader_parameter("tam", Vector2(_n) * _celda)
	_carta_mat.set_shader_parameter("rango", rango)
	_carta.visible = true
	carta_lista = true


func _refrescar_carta() -> void:
	if not _carta.visible:
		return
	var j: Node3D = Zonas.jugador
	_carta_mat.set_shader_parameter("centro", Vector2(j.global_position.x, j.global_position.z))
	_carta_mat.set_shader_parameter("radio_m", radio_m)
	_carta_mat.set_shader_parameter("alfa", _carta_alfa)


# ------------------------------------------------------------------ dibujo

func _al_mapa(p: Vector3, centro: Vector2, r: float) -> Vector2:
	var j: Node3D = Zonas.jugador
	return centro + Vector2(p.x - j.global_position.x, p.z - j.global_position.z) * (r / radio_m)


func _dibujar_fondo() -> void:
	# fondo fijo: noche petroleo con anillos de distancia y la cruz (solo se redibuja al cambiar de tamano)
	var r := radio_px()
	var c := Vector2(r, r)
	_fondo.draw_circle(c, r + 5.0, Color(Estilo.TINTA, 0.85))
	_fondo.draw_circle(c, r, Color(Estilo.NOCHE, 0.9))
	for f in [0.33, 0.66]:
		_fondo.draw_arc(c, r * f, 0.0, TAU, 48, Color(Estilo.CIAN_MEDIO, 0.2), 1.0, true)
	_fondo.draw_line(c + Vector2(-r, 0), c + Vector2(r, 0), Color(Estilo.CIAN_MEDIO, 0.1), 1.0)
	_fondo.draw_line(c + Vector2(0, -r), c + Vector2(0, r), Color(Estilo.CIAN_MEDIO, 0.1), 1.0)


func _dibujar_aro() -> void:
	# aro de laton biselado con las marcas de rumbo grabadas, como el anillo de un telescopio (fijo)
	var r := radio_px()
	var c := Vector2(r, r)
	var ancho := 7.0 if grande else 6.0
	var medio := r + ancho * 0.5 - 1.0
	_aro.draw_arc(c, medio, 0.0, TAU, 72, LATON, ancho, true)
	# luz desde arriba a la izquierda: brillo en el arco de arriba, sombra en el de abajo
	_aro.draw_arc(c, medio + ancho * 0.25, PI * 1.05, PI * 1.7, 32, Color(Estilo.DORADO.lightened(0.35), 0.9), 1.6, true)
	_aro.draw_arc(c, medio - ancho * 0.25, PI * 0.05, PI * 0.7, 32, Color(Estilo.TINTA, 0.55), 1.6, true)
	_aro.draw_arc(c, r + ancho, 0.0, TAU, 72, Estilo.TINTA, 1.5, true)
	_aro.draw_arc(c, r - 1.0, 0.0, TAU, 72, Estilo.TINTA, 1.5, true)
	# marcas de rumbo grabadas en el laton: cada 10 grados, mas largas cada 45
	for i in 36:
		var ang := TAU * float(i) / 36.0
		var dir := Vector2(sin(ang), -cos(ang))
		var largo := ancho * (0.85 if i % 9 == 0 else 0.45)
		_aro.draw_line(c + dir * (r + ancho - 1.0 - largo), c + dir * (r + ancho - 1.0), Color(Estilo.TINTA, 0.8), 1.2, true)
	# remaches en los cuatro diagonales
	for i in 4:
		var ang := TAU * (float(i) + 0.5) / 4.0
		var q := c + Vector2(sin(ang), -cos(ang)) * medio
		_aro.draw_circle(q, 2.2, Estilo.TINTA)
		_aro.draw_circle(q + Vector2(-0.5, -0.5), 1.2, Estilo.DORADO.lightened(0.3))
	# el norte: una pestana de laton con su letra
	var n := c + Vector2(0, -(r + ancho * 0.5))
	var pestana := PackedVector2Array([n + Vector2(-9, -6), n + Vector2(9, -6), n + Vector2(6, 9), n + Vector2(-6, 9)])
	_aro.draw_colored_polygon(pestana, LATON)
	pestana.append(pestana[0])
	_aro.draw_polyline(pestana, Estilo.TINTA, 1.5, true)
	var fuente := Estilo.fuente(700)
	_aro.draw_string(fuente, n + Vector2(-5, 7), "N", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Estilo.TINTA)


func _dibujar_capa() -> void:
	# lo que se mueve: puntos, objetivo y la protagonista (30 Hz)
	if Zonas.jugador == null or Zonas.actual == null:
		return
	var r := radio_px()
	var c := Vector2(r, r)
	var cv := _capa
	if not _silueta.is_empty():
		var poli := PackedVector2Array()
		for p in _silueta:
			poli.append(_al_mapa(Vector3(p.x, 0.0, p.y), c, r))
		poli.append(poli[0])
		cv.draw_polyline(poli, Color(Estilo.PAPEL, 0.8), 1.5, true)
	elif not carta_lista:
		# mientras se sondea la forma del lugar: un barrido corto, la unica animacion del disco
		var barrido := fmod(_t / 1.2, 1.0) * TAU
		for s in 6:
			var a0 := barrido - float(s + 1) * 0.08
			var a1 := barrido - float(s) * 0.08
			cv.draw_colored_polygon(PackedVector2Array([c, c + Vector2(sin(a0), -cos(a0)) * r, c + Vector2(sin(a1), -cos(a1)) * r]),
				Color(Estilo.CIAN, 0.09 * (1.0 - float(s) / 6.0)))
	# interactuables con su glifo y umbrales
	for par in _puntos:
		var nodo: Variant = par[0]
		if not is_instance_valid(nodo) or nodo == _nodo_objetivo:
			continue
		var q := _al_mapa((nodo as Node3D).global_position, c, r)
		if q.distance_to(c) < r - 6.0:
			_glifo(cv, q, String(par[1]))
	for u in _umbrales:
		if not is_instance_valid(u) or u == _nodo_objetivo:
			continue
		var q := _al_mapa(u.global_position, c, r)
		if q.distance_to(c) < r - 7.0:
			_estrella(cv, q, 6.5, Estilo.CIAN, u.abierto())
	# Orbita
	var gato: Node3D = Zonas.companero
	if gato != null and gato.visible and gato != _nodo_objetivo:
		var q := _al_mapa(gato.global_position, c, r)
		if q.distance_to(c) < r - 4.0:
			cv.draw_circle(q, 4.2, Estilo.TINTA)
			cv.draw_circle(q, 3.1, Estilo.NARANJA)
	# el objetivo (encima del aro: la flecha del borde se ve entera)
	if tiene_objetivo:
		var q := _al_mapa(objetivo_pos, c, r)
		var dentro := q.distance_to(c) <= r - 10.0
		var dir := (q - c).normalized() if q.distance_to(c) > 0.5 else Vector2.UP
		if not dentro:
			q = c + dir * (r - 10.0)
		# camino discontinuo desde la protagonista (sobra si ya se esta encima de un umbral)
		var junto_umbral := _nodo_objetivo != null and _nodo_objetivo.is_in_group("umbrales") and objetivo_distancia < 2.2
		if not junto_umbral:
			var largo := c.distance_to(q) - 9.0
			var n := int(largo / 9.0)
			for i in n:
				var a := c + dir * (8.0 + float(i) * 9.0)
				cv.draw_line(a, a + dir * 4.5, Color(Estilo.DORADO, 0.7), 2.0, true)
		var pulso := 1.0 + 0.16 * sin(_t * TAU / 1.6)
		_rombo(cv, q, 7.5 * pulso, Estilo.DORADO)
		if not dentro:
			var punta := c + dir * (r + 3.0)
			var lado := Vector2(-dir.y, dir.x)
			var tri := PackedVector2Array([punta + dir * 11.0, punta + lado * 7.0, punta - lado * 7.0])
			cv.draw_colored_polygon(tri, Estilo.DORADO)
			tri.append(tri[0])
			cv.draw_polyline(tri, Estilo.TINTA, 1.5, true)
	# la protagonista: flecha hacia donde mira
	var mira: Vector3 = Zonas.jugador.get("mirando")
	var m := Vector2(mira.x, mira.z)
	if m.length() < 0.01:
		m = Vector2(0, 1)
	m = m.normalized()
	var lado2 := Vector2(-m.y, m.x)
	var flecha := PackedVector2Array([c + m * 9.0, c - m * 6.0 + lado2 * 6.5, c - m * 3.0, c - m * 6.0 - lado2 * 6.5])
	cv.draw_colored_polygon(flecha, Estilo.PAPEL)
	flecha.append(flecha[0])
	cv.draw_polyline(flecha, Estilo.TINTA, 2.0, true)


func _glifo(cv: Control, q: Vector2, tipo: String) -> void:
	match tipo:
		"tarea":
			# rombo cian hueco: la tecnologia (un reto o un aparato de la historia)
			var pts := PackedVector2Array([q + Vector2(0, -5.5), q + Vector2(4.5, 0), q + Vector2(0, 5.5), q + Vector2(-4.5, 0)])
			cv.draw_colored_polygon(pts, Color(Estilo.NOCHE, 0.9))
			pts.append(pts[0])
			cv.draw_polyline(pts, Estilo.CIAN, 2.0, true)
		"persona":
			cv.draw_circle(q, 4.2, Estilo.TINTA)
			cv.draw_circle(q, 3.1, Estilo.NARANJA)
			cv.draw_circle(q + Vector2(0, -1.0), 1.1, Estilo.CREMA)
		"recoger":
			var tri := PackedVector2Array([q + Vector2(0, -4.5), q + Vector2(4.2, 3.2), q + Vector2(-4.2, 3.2)])
			cv.draw_colored_polygon(tri, Estilo.BRILLO)
			tri.append(tri[0])
			cv.draw_polyline(tri, Estilo.TINTA, 1.3, true)
		_:
			# hoja de papel con la esquina doblada: un dato, un cartel, algo que leer o mirar
			var hoja := PackedVector2Array([q + Vector2(-3.5, -4.5), q + Vector2(1.5, -4.5), q + Vector2(3.5, -2.5), q + Vector2(3.5, 4.5), q + Vector2(-3.5, 4.5)])
			cv.draw_colored_polygon(hoja, Estilo.PAPEL)
			hoja.append(hoja[0])
			cv.draw_polyline(hoja, Estilo.TINTA, 1.2, true)
			cv.draw_line(q + Vector2(-1.8, 0.0), q + Vector2(1.8, 0.0), Estilo.TINTA_SUAVE, 1.0)
			cv.draw_line(q + Vector2(-1.8, 2.2), q + Vector2(1.8, 2.2), Estilo.TINTA_SUAVE, 1.0)


func _estrella(cv: Control, q: Vector2, t: float, color: Color, llena: bool) -> void:
	var pts := PackedVector2Array()
	for i in 8:
		var ang := TAU * float(i) / 8.0
		var largo := t if i % 2 == 0 else t * 0.38
		pts.append(q + Vector2(sin(ang), -cos(ang)) * largo)
	if llena:
		cv.draw_colored_polygon(pts, color)
	pts.append(pts[0])
	cv.draw_polyline(pts, Estilo.TINTA if llena else color, 1.4 if llena else 1.8, true)


func _rombo(cv: Control, q: Vector2, t: float, color: Color) -> void:
	var pts := PackedVector2Array([q + Vector2(0, -t), q + Vector2(t * 0.75, 0), q + Vector2(0, t), q + Vector2(-t * 0.75, 0)])
	cv.draw_colored_polygon(pts, color)
	pts.append(pts[0])
	cv.draw_polyline(pts, Estilo.TINTA, 2.0, true)
	cv.draw_line(q + Vector2(0, -t * 0.55), q + Vector2(t * 0.3, 0), Color(Estilo.PAPEL, 0.8), 1.5, true)


# ------------------------------------------------------------------ marca en el mundo

func _crear_marca() -> void:
	# rombo dorado alargado (alto = 2,5 veces el ancho) que se dibuja siempre encima de la geometria, con contorno
	# de tinta, y un hilo de luz hasta el punto: se lee como «ve alli» aunque lo tape un mueble
	_marca = Node3D.new()
	_marca.name = "MarcaObjetivo"
	_rombo3d = Node3D.new()
	_marca.add_child(_rombo3d)
	var brillo := Materiales.emisivo(Estilo.DORADO, 2.4)
	brillo.no_depth_test = true
	brillo.render_priority = 11
	var contorno := StandardMaterial3D.new()
	contorno.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	contorno.albedo_color = Estilo.TINTA
	contorno.cull_mode = BaseMaterial3D.CULL_FRONT
	contorno.no_depth_test = true
	contorno.render_priority = 10
	var punta := CylinderMesh.new()
	punta.top_radius = 0.0
	punta.bottom_radius = 0.12
	punta.height = 0.30
	punta.radial_segments = 4
	punta.rings = 1
	for capa in [[brillo, 1.0], [contorno, 1.2]]:
		for abajo in [false, true]:
			var mi := MeshInstance3D.new()
			mi.mesh = punta
			mi.material_override = capa[0]
			mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			mi.scale = Vector3.ONE * float(capa[1])
			mi.position.y = 0.15 * float(capa[1]) * (-1.0 if abajo else 1.0)
			if abajo:
				mi.rotation.x = PI
			_rombo3d.add_child(mi)
	var hilo := CylinderMesh.new()
	hilo.top_radius = 0.016
	hilo.bottom_radius = 0.016
	hilo.height = 1.0
	hilo.radial_segments = 6
	hilo.rings = 1
	var luz := StandardMaterial3D.new()
	luz.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	luz.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	luz.albedo_color = Color(Estilo.DORADO, 0.55)
	_haz = MeshInstance3D.new()
	_haz.mesh = hilo
	_haz.material_override = luz
	_haz.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_marca.add_child(_haz)
	Zonas.mundo.add_child(_marca)


func _ver_marca(ver: bool) -> void:
	if _marca != null and is_instance_valid(_marca):
		_marca.visible = ver


func _mover_marca() -> void:
	if _marca == null or not is_instance_valid(_marca):
		if not tiene_objetivo or Zonas.mundo == null:
			return
		_crear_marca()
	# junto a un umbral sobra (ya se ve su marca cian y su rotulo); lejos crece para leerse a distancia
	var es_umbral := tiene_objetivo and _nodo_objetivo.is_in_group("umbrales")
	_marca.visible = tiene_objetivo and not (es_umbral and objetivo_distancia < 2.2)
	if not _marca.visible:
		return
	var k := clampf(0.85 + objetivo_distancia * 0.05, 0.85, 1.7)
	_rombo3d.scale = Vector3.ONE * k
	# el punto en el suelo: un umbral es su marca cian (plano a ras de suelo); lo demas, el origen del nodo
	var p := objetivo_pos
	var alto := 1.0
	if es_umbral:
		alto = 0.95
	elif _nodo_objetivo.is_in_group("interactuables"):
		alto = float(_nodo_objetivo.get("altura_marca")) + 0.6
	elif _nodo_objetivo == Zonas.companero:
		alto = 1.05
	alto += 0.3 * (k - 0.85)
	alto += 0.07 * sin(_t * 2.4)
	var cizalla := float(Materiales.parametros.get("inclinacion", 0.45))
	var suelo := p + Vector3(0.0, 0.03, -cizalla * (p.y + 0.03))
	var arriba := p + Vector3(0.0, alto, -cizalla * (p.y + alto))
	_rombo3d.global_position = arriba
	_rombo3d.rotation.y = _t * 1.2
	# hilo de luz desde la punta de abajo del rombo hasta el suelo
	var bajo := arriba + Vector3(0.0, -0.32 * k, cizalla * 0.32 * k)
	var eje := bajo - suelo
	var largo := eje.length()
	_haz.visible = largo > 0.05
	if _haz.visible:
		var y := eje / largo
		var x := Vector3.RIGHT
		var z := x.cross(y).normalized()
		_haz.global_transform = Transform3D(Basis(x, y * largo, z), (bajo + suelo) * 0.5)
