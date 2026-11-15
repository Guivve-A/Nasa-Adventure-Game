extends Control

# Mapa del mundo (tecla M): la ilustracion de la region en el cuaderno, con cada lugar, donde esta la
# protagonista y como se conecta cada escena con las demas (por donde se pasa y que hace falta para pasar).
# En visita libre (menu principal) o al terminar la historia se puede viajar a un lugar eligiendolo.
# Los nombres se componen aqui, sobre las placas en blanco de la ilustracion. Estilo provisional.

signal cerrado
signal viajar(id_zona: String)

const Estilo := preload("res://interfaz/estilo.gd")
const Recursos := preload("res://nucleo/recursos.gd")

var datos: Dictionary = {}
var nodos: Array = []
var elegido := 0
var modo_viaje := false
var _imagen: TextureRect
var _lienzo: Control
var _ficha: PanelContainer
var _columna: VBoxContainer
var _ayuda: Label
var _t := 0.0
var _titulo: Label


func _marco() -> Rect2:
	# rectangulo de la ilustracion (16:9), a la izquierda; la ficha del lugar va a su derecha
	var ancho := size.x * 0.70
	return Rect2(18.0, 64.0, ancho, ancho * 9.0 / 16.0)


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var fondo := ColorRect.new()
	fondo.color = Estilo.PAPEL
	fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(fondo)
	_imagen = TextureRect.new()
	_imagen.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_imagen.stretch_mode = TextureRect.STRETCH_SCALE
	_imagen.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_imagen)
	_titulo = Estilo.linea("MAPA DEL MUNDO", 26, Estilo.TINTA, 700)
	add_child(_titulo)
	_lienzo = Control.new()
	_lienzo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_lienzo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_lienzo.draw.connect(_dibujar)
	add_child(_lienzo)
	_ficha = Estilo.panel(Color(Estilo.PAPEL, 0.97), 14, 3, 16)
	_ficha.custom_minimum_size = Vector2(330, 0)
	_columna = VBoxContainer.new()
	_columna.add_theme_constant_override("separation", 6)
	_ficha.add_child(_columna)
	add_child(_ficha)
	_ayuda = Estilo.linea("", 15, Estilo.TINTA, 600)
	add_child(_ayuda)
	var d: Variant = Juego.leer_json("res://datos/mapa.json")
	if d is Dictionary:
		datos = d
		nodos = d.get("nodos", [])


func _punto(par: Variant) -> Vector2:
	var m := _marco()
	return m.position + Vector2(float(par[0]) * m.size.x, float(par[1]) * m.size.y)


func _nodo(id: String) -> Dictionary:
	for n in nodos:
		if n["id"] == id:
			return n
	return {}


func _visitado(id: String) -> bool:
	return bool(Juego.bandera("visitada_" + id)) or id == Zonas.id_actual


func _abierta(ruta: Dictionary) -> bool:
	if Juego.bandera("visita_libre"):
		return true
	for b in ruta.get("requiere", []):
		if not Juego.bandera(b):
			return false
	return true


func puede_viajar(id: String) -> bool:
	if not Zonas.existe(id) or id == Zonas.id_actual:
		return false
	return modo_viaje or bool(Juego.bandera("visita_libre")) or (bool(Juego.bandera("fin_v0")) and _visitado(id))


func abrir(viaje: bool = false) -> void:
	modo_viaje = viaje
	_imagen.texture = Recursos.textura(datos.get("imagen", ""))
	for i in nodos.size():
		if nodos[i]["id"] == Zonas.id_actual:
			elegido = i
	visible = true
	_refrescar()


func cerrar() -> void:
	if visible:
		visible = false
		Audio.sonar("pagina")
		cerrado.emit()


func _process(delta: float) -> void:
	if not visible:
		return
	_t += delta
	var m := _marco()
	_imagen.position = m.position
	_imagen.size = m.size
	_titulo.position = Vector2(m.position.x + 6.0, 20.0)
	_ficha.custom_minimum_size = Vector2(size.x - m.end.x - 34.0, 0)
	_ficha.reset_size()
	_ficha.position = Vector2(m.end.x + 16.0, m.position.y)
	_ayuda.position = Vector2(m.position.x + 6.0, m.end.y + 18.0)
	_lienzo.queue_redraw()


func _refrescar() -> void:
	for hijo in _columna.get_children():
		_columna.remove_child(hijo)
		hijo.queue_free()
	if nodos.is_empty():
		return
	var n: Dictionary = nodos[elegido]
	var id: String = n["id"]
	var meta: Dictionary = Zonas.info(id)
	var construido := Zonas.existe(id)
	var nombre: String = meta.get("nombre", id) if construido else n.get("nombre", n.get("corto", id))
	var cabecera := Estilo.texto(nombre, 25, Estilo.TINTA, 700)
	cabecera.custom_minimum_size = Vector2(290, 0)
	_columna.add_child(cabecera)
	var detalle: Array = []
	for clave in ["lugar", "momento"]:
		if meta.get(clave, "") != "":
			detalle.append(meta[clave])
	if not detalle.is_empty():
		var sub := Estilo.texto(" · ".join(PackedStringArray(detalle)), 16, Estilo.TERRACOTA, 600)
		sub.custom_minimum_size = Vector2(290, 0)
		_columna.add_child(sub)
	var estado := "Estás aquí" if id == Zonas.id_actual else ("Visitado" if _visitado(id) else "Sin visitar")
	if not construido:
		estado = "En construcción"
	elif String(meta.get("estado_arte", "")).begins_with("provisional"):
		estado += " · arte provisional"
	_columna.add_child(Estilo.texto(estado, 15, Estilo.PETROLEO, 700))
	var que := Estilo.texto(n.get("que_hay", ""), 17, Estilo.TINTA, 500)
	que.custom_minimum_size = Vector2(290, 0)
	_columna.add_child(que)
	_columna.add_child(Estilo.texto("CONEXIONES", 13, Estilo.PETROLEO, 700))
	for r in datos.get("rutas", []):
		var otro := ""
		if r["de"] == id:
			otro = r["a"]
		elif r["a"] == id and not r.get("solo_ida", false) and not r.get("sueno", false):
			otro = r["de"]
		elif r["a"] == id and r.get("sueno", false):
			otro = r["de"]
		if otro == "":
			continue
		var nombre_otro: String = _nodo(otro).get("corto", otro)
		var linea := "→ %s, %s" % [nombre_otro, r.get("como", "")]
		if r["a"] == id and r.get("sueno", false):
			linea = "→ %s, al despertar" % nombre_otro
		var abierta := _abierta(r)
		var etiqueta := Estilo.texto(linea + ("" if abierta else "  (cerrado: falta avanzar en la misión)"), 16, Estilo.TINTA if abierta else Estilo.TINTA_SUAVE, 500)
		etiqueta.custom_minimum_size = Vector2(290, 0)
		_columna.add_child(etiqueta)
	if puede_viajar(id):
		var b := Estilo.boton("Viajar aquí (E)", 18, true)
		b.custom_minimum_size = Vector2(290, 42)
		b.focus_mode = Control.FOCUS_NONE
		b.pressed.connect(func(): _viajar())
		_columna.add_child(b)
	_ayuda.text = "Flechas: elegir lugar   ·   %sM o Esc: cerrar" % ("E: viajar   ·   " if puede_viajar(id) else "")
	_ayuda.reset_size()


func _viajar() -> void:
	var id: String = nodos[elegido]["id"]
	if puede_viajar(id):
		visible = false
		viajar.emit(id)


func _input(evento: InputEvent) -> void:
	if not visible or nodos.is_empty():
		return
	var direccion := Vector2.ZERO
	if evento.is_action_pressed("mover_izquierda"):
		direccion = Vector2.LEFT
	elif evento.is_action_pressed("mover_derecha"):
		direccion = Vector2.RIGHT
	elif evento.is_action_pressed("mover_arriba"):
		direccion = Vector2.UP
	elif evento.is_action_pressed("mover_abajo"):
		direccion = Vector2.DOWN
	if direccion != Vector2.ZERO:
		_mover(direccion)
		get_viewport().set_input_as_handled()
	elif evento.is_action_pressed("interactuar") or evento.is_action_pressed("ui_accept"):
		_viajar()
		get_viewport().set_input_as_handled()
	elif evento.is_action_pressed("pausa") or evento.is_action_pressed("mapa"):
		cerrar()
		get_viewport().set_input_as_handled()
	elif evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		for i in nodos.size():
			var cerca: bool = _punto(nodos[i]["pos"]).distance_to(evento.position) < 36.0 or _punto(nodos[i]["rotulo"]).distance_to(evento.position) < 56.0
			if cerca:
				elegido = i
				Audio.sonar("tic")
				_refrescar()


func _mover(direccion: Vector2) -> void:
	# el lugar mas cercano en esa direccion
	var origen := _punto(nodos[elegido]["pos"])
	var mejor := -1
	var mejor_coste := INF
	for i in nodos.size():
		if i == elegido:
			continue
		var d := _punto(nodos[i]["pos"]) - origen
		var avance := d.normalized().dot(direccion)
		if avance < 0.25:
			continue
		var coste := d.length() / avance
		if coste < mejor_coste:
			mejor_coste = coste
			mejor = i
	if mejor >= 0:
		elegido = mejor
		Audio.sonar("tic")
		_refrescar()


func _dibujar() -> void:
	if nodos.is_empty():
		return
	var mano := Estilo.fuente(700, true)
	# rutas que la ilustracion no trae pintadas y candados de las cerradas
	for r in datos.get("rutas", []):
		var abierta := _abierta(r)
		if r.get("dibujar", false):
			var puntos: Array = r.get("puntos", [])
			for i in puntos.size() - 1:
				var a := _punto(puntos[i])
				var b := _punto(puntos[i + 1])
				var tramos := int(a.distance_to(b) / 14.0)
				for k in tramos:
					if k % 2 == 0:
						_lienzo.draw_line(a.lerp(b, float(k) / tramos), a.lerp(b, float(k + 1) / tramos), Color(Estilo.NARANJA if abierta else Estilo.TINTA_SUAVE, 0.9), 3.0, true)
		if not abierta:
			var medio := (_punto(_nodo(r["de"])["pos"]) + _punto(_nodo(r["a"])["pos"])) * 0.5
			if r.get("dibujar", false) and r.get("puntos", []).size() > 2:
				medio = _punto(r["puntos"][1])
			_lienzo.draw_circle(medio, 13.0, Estilo.PAPEL)
			_lienzo.draw_arc(medio, 13.0, 0.0, TAU, 24, Estilo.TINTA, 2.0, true)
			_lienzo.draw_rect(Rect2(medio + Vector2(-5.5, -1.5), Vector2(11, 8)), Estilo.TINTA, true)
			_lienzo.draw_arc(medio + Vector2(0, -2), 4.0, PI, TAU, 10, Estilo.TINTA, 2.0, true)
	# lugares
	for i in nodos.size():
		var n: Dictionary = nodos[i]
		var id: String = n["id"]
		var p := _punto(n["pos"])
		var aqui := id == Zonas.id_actual
		var visto := _visitado(id)
		if i == elegido:
			_lienzo.draw_arc(p, 24.0 + 3.0 * sin(_t * 4.0), 0.0, TAU, 40, Estilo.CIAN_MEDIO, 4.0, true)
		_lienzo.draw_circle(p, 11.0, Estilo.TINTA)
		_lienzo.draw_circle(p, 8.0, Estilo.CIAN if aqui else (Estilo.CREMA if visto else Estilo.PAPEL_SOMBRA))
		if aqui:
			_lienzo.draw_arc(p, 16.0 + 6.0 * (0.5 + 0.5 * sin(_t * 3.0)), 0.0, TAU, 32, Color(Estilo.CIAN_MEDIO, 0.8), 2.5, true)
		# nombre sobre la placa de la ilustracion
		var texto: String = n.get("corto", id)
		var centro := _punto(n["rotulo"])
		var tam := mano.get_string_size(texto, HORIZONTAL_ALIGNMENT_LEFT, -1, 19)
		if n.get("sin_placa", false):
			_lienzo.draw_rect(Rect2(centro - Vector2(tam.x * 0.5 + 10.0, 18.0), Vector2(tam.x + 20.0, 34.0)), Color(Estilo.PAPEL, 0.92), true)
		var color := Estilo.TINTA if (visto or modo_viaje) else Estilo.TINTA_SUAVE
		_lienzo.draw_string(mano, centro + Vector2(-tam.x * 0.5, 7.0), texto, HORIZONTAL_ALIGNMENT_LEFT, -1, 19, color)
		if aqui:
			_lienzo.draw_string(Estilo.fuente(700), p + Vector2(18.0, -16.0), "ESTÁS AQUÍ", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Estilo.PETROLEO)
