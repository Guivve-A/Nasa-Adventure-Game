extends "res://nucleo/minijuego.gd"

# Fechas y contenido: fichas locales y FUENTES.md; no se citan textos de misiones.
# El anio del disco figura en el campo fuente de disco_apolo11.
const HITOS: Array = [
	{"ficha": "observatorio_quito", "titulo": "Observatorio de Quito", "fecha": "1873", "epoca": "Siglo XIX.", "dato": "Pertenece a la Escuela Politécnica Nacional."},
	{"ficha": "estacion_cotopaxi", "titulo": "Estación Quito", "fecha": "1957", "epoca": "Mediados del siglo XX.", "dato": "Al pie del Cotopaxi, a 3 650 m."},
	{"ficha": "disco_apolo11", "titulo": "Disco del Apolo 11", "fecha": "1969", "epoca": "Mensajes rumbo a la Luna.", "dato": "Llevó mensajes de 73 países, incluido Ecuador."},
	{"ficha": "apolo_soyuz_1975", "titulo": "Apoyo al Apolo-Soyuz", "fecha": "1975", "epoca": "Después del viaje del disco.", "dato": "Quito participó con el indicativo QUI en la red de apoyo."},
	{"ficha": "sts2_despedida", "titulo": "Despedida del STS-2", "fecha": "14-11-1981", "epoca": "El cierre de la estación.", "dato": "Engle y Truly se despidieron de 75 empleados."},
	{"ficha": "estacion_entrega", "titulo": "Entrega a Ecuador", "fecha": "01-07-1982", "epoca": "Tras el cierre de la estación.", "dato": "La instalación se entregó a Ecuador, a CLIRSEN."},
	{"ficha": "exa_2007", "titulo": "Nace la EXA", "fecha": "2007", "epoca": "Comienzos del siglo XXI.", "dato": "Organización no gubernamental sin fines de lucro."},
	{"ficha": "pegaso_lanzamiento", "titulo": "Lanzamiento de Pegaso", "fecha": "2013", "epoca": "Después del nacimiento de EXA.", "dato": "Se lanzó desde Jiuquan, según el equipo de Pegaso."},
	{"ficha": "acuerdos_artemisa", "titulo": "Acuerdos Artemisa", "fecha": "21-06-2023", "epoca": "Después de Pegaso.", "dato": "Ecuador fue el país firmante n.º 26."}
]
const PISTAS_CLARAS: Array[String] = [
	"Primero: siglo XIX.", "Antes del disco lunar.", "Antes de Apolo-Soyuz.",
	"Antes del STS-2.", "Antes de la entrega.", "Antes de nacer EXA.",
	"Antes de Pegaso.", "Antes de Artemisa.", "Último hito."
]

var orden: Array[int] = []
var seleccion: int = 0
var tomada: bool = false
var comprobaciones: int = 0
var max_comprobaciones: int = 4
var _marcas: Array[bool] = []
var _reveladas: Dictionary = {}
var _pistas_claras: Dictionary = {}
var _paneles: Array[Panel] = []
var _titulos: Array[Label] = []
var _pistas: Array[Label] = []
var _fechas: Array[Label] = []
var _estados: Array[Label] = []
var _contador: Label
var _detalle: Label
var _mensaje: Label
var _comprobar_boton: Button
var _arrastrando: bool = false
var _auto: int = 0
var _pulso: float = 0.0
var _auto_inicio: bool = false


func _preparar() -> void:
	# En la primera dificultad solo hay un par invertido.
	if dificultad == 1:
		orden.assign([0, 2, 1, 7, 8])
	elif dificultad == 2:
		orden.assign([2, 0, 1, 5, 3, 8, 7])
	else:
		orden.assign([2, 0, 1, 5, 3, 4, 8, 6, 7])
		max_comprobaciones = 3
	_marcas.resize(orden.size())
	_marcas.fill(false)
	_contador = _etiqueta("", Vector2(24, 10), Vector2(1072, 30), 20)
	_etiqueta("MÁS ANTIGUO  →  MÁS RECIENTE", Vector2(24, 43), Vector2(1072, 28), 16)
	for i in orden.size():
		var rect: Rect2 = _rect_tarjeta(i)
		var panel: Panel = Panel.new()
		panel.position = rect.position
		panel.size = rect.size
		panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(panel)
		_paneles.append(panel)
		_estados.append(_etiqueta("", rect.position + Vector2(8, 8), Vector2(rect.size.x - 16, 24), 16))
		_titulos.append(_etiqueta("", rect.position + Vector2(8, 38), Vector2(rect.size.x - 16, 104), 16))
		_pistas.append(_etiqueta("", rect.position + Vector2(8, 149), Vector2(rect.size.x - 16, 100), 16))
		_fechas.append(_etiqueta("", rect.position + Vector2(5, 263), Vector2(rect.size.x - 10, 30), 16))
	_mensaje = _etiqueta("", Vector2(24, 383), Vector2(1072, 26), 16)
	_detalle = _etiqueta("", Vector2(24, 414), Vector2(1072, 56), 18)
	_comprobar_boton = Estilo.boton("Comprobar · Espacio", 18, true)
	_comprobar_boton.position = Vector2(806, 474)
	_comprobar_boton.size = Vector2(290, 42)
	_comprobar_boton.focus_mode = Control.FOCUS_NONE
	_comprobar_boton.pressed.connect(_comprobar)
	add_child(_comprobar_boton)
	_etiqueta("E / Intro: tomar o soltar · ← →: elegir o mover", Vector2(24, 479), Vector2(770, 30), 16)
	_refrescar()


func _etiqueta(contenido: String, pos: Vector2, medida: Vector2, tam: int) -> Label:
	var etiqueta: Label = texto(contenido, tam, Estilo.TINTA, 600)
	etiqueta.position = pos
	etiqueta.custom_minimum_size = Vector2(medida.x, 0)
	etiqueta.size = medida
	add_child(etiqueta)
	return etiqueta


func _rect_tarjeta(i: int) -> Rect2:
	var ancho: float = (1072.0 - float(orden.size() - 1) * 8.0) / float(orden.size())
	return Rect2(24.0 + float(i) * (ancho + 8.0), 79.0, ancho, 298.0)


func _empezar() -> void:
	_refrescar()


func _paso(delta: float) -> void:
	if _auto == 0:
		return
	_pulso += delta
	if _pulso < 0.3:
		return
	_pulso = 0.0
	# Mismas operaciones de seleccion, movimiento adyacente y comprobacion que la persona.
	if not _auto_inicio:
		_auto_inicio = true
		if _auto < 0:
			seleccion = 0
			_mover(1)
		_comprobar()
		return
	if _auto < 0:
		_comprobar()
		return
	for i in range(orden.size() - 1):
		if orden[i] > orden[i + 1]:
			seleccion = i + 1
			_mover(-1)
			return
	_comprobar()


func _input(evento: InputEvent) -> void:
	if not activo or _auto != 0:
		return
	if evento.is_action_pressed("saltar"):
		_comprobar()
	elif evento.is_action_pressed("interactuar"):
		tomada = not tomada
		_refrescar()
	elif evento.is_action_pressed("mover_izquierda"):
		_desplazar(-1)
	elif evento.is_action_pressed("mover_derecha"):
		_desplazar(1)
	elif evento.is_action_pressed("mover_arriba"):
		seleccion = maxi(seleccion - 1, 0)
		_refrescar()
	elif evento.is_action_pressed("mover_abajo"):
		seleccion = mini(seleccion + 1, orden.size() - 1)
		_refrescar()
	else:
		return
	get_viewport().set_input_as_handled()


func _desplazar(direccion: int) -> void:
	if tomada:
		_mover(direccion)
	else:
		seleccion = clampi(seleccion + direccion, 0, orden.size() - 1)
		_refrescar()


func _mover(direccion: int) -> void:
	var destino: int = seleccion + direccion
	if destino < 0 or destino >= orden.size():
		return
	var hito: int = orden[seleccion]
	orden[seleccion] = orden[destino]
	orden[destino] = hito
	seleccion = destino
	_marcas.fill(false)
	_refrescar()


func _gui_input(evento: InputEvent) -> void:
	if not activo or _auto != 0:
		return
	if evento is InputEventMouseButton and evento.button_index == MOUSE_BUTTON_LEFT:
		if evento.pressed:
			for i in orden.size():
				if _rect_tarjeta(i).has_point(evento.position):
					seleccion = i
					tomada = true
					_arrastrando = true
					grab_focus()
					_refrescar()
					break
		else:
			_arrastrando = false
			tomada = false
			_refrescar()
	elif evento is InputEventMouseMotion and _arrastrando:
		if (evento.button_mask & MOUSE_BUTTON_MASK_LEFT) == 0:
			_arrastrando = false
			tomada = false
			_refrescar()
			return
		for i in orden.size():
			if _rect_tarjeta(i).has_point(Vector2(evento.position.x, 100)):
				while seleccion != i:
					_mover(1 if i > seleccion else -1)
				break


func _pista_clara(hito: int) -> String:
	var anteriores: Array[int] = []
	for otro in orden:
		if otro < hito:
			anteriores.append(otro)
	if anteriores.is_empty():
		return "Es el hito más antiguo de estas %d tarjetas." % orden.size()
	anteriores.sort()
	var anterior: Dictionary = HITOS[anteriores.back()]
	return "Va después de «%s»." % anterior["titulo"]


func _causa() -> String:
	for i in range(orden.size() - 1):
		if orden[i] > orden[i + 1]:
			var antes: Dictionary = HITOS[orden[i + 1]]
			var despues: Dictionary = HITOS[orden[i]]
			return "«%s» (%s) vino antes que «%s» (%s); ese par quedó al revés." % [antes["titulo"], antes["fecha"], despues["titulo"], despues["fecha"]]
	return "Todos los hitos avanzan de la fecha más antigua a la más reciente."


func _comprobar() -> void:
	if not activo:
		return
	comprobaciones += 1
	tomada = false
	_arrastrando = false
	var bien: int = 0
	for i in orden.size():
		var izquierda: bool = i == 0 or orden[i - 1] < orden[i]
		var derecha: bool = i == orden.size() - 1 or orden[i] < orden[i + 1]
		_marcas[i] = izquierda and derecha
		if _marcas[i]:
			_reveladas[orden[i]] = true
			bien += 1
		else:
			_pistas_claras[orden[i]] = true
	_refrescar()
	if bien == orden.size():
		terminar(true, 100.0, "Ordenaste %d hitos: de 1873 al 21-06-2023. El disco llevó mensajes de 73 países, incluido Ecuador." % orden.size())
	elif comprobaciones >= max_comprobaciones:
		terminar(false, 0.0, "Usaste las %d comprobaciones. %s" % [max_comprobaciones, _causa()])
	else:
		sonar("pagina")


func _refrescar() -> void:
	_contador.text = "%d tarjetas · Comprobaciones: %d de %d" % [orden.size(), comprobaciones, max_comprobaciones]
	for i in orden.size():
		var hito: Dictionary = HITOS[orden[i]]
		var fondo: Color = Estilo.CREMA if _marcas[i] else Estilo.PAPEL
		var borde: Color = Estilo.CIAN_MEDIO if i == seleccion else Estilo.TINTA_SUAVE
		_paneles[i].add_theme_stylebox_override("panel", Estilo.caja(fondo, 5, 4 if i == seleccion else 2, borde, 0))
		_estados[i].text = "%d · %s" % [i + 1, "✓" if _marcas[i] else ("↔" if i == seleccion and tomada else "○")]
		_titulos[i].text = hito["titulo"]
		_pistas[i].text = PISTAS_CLARAS[orden[i]] if _pistas_claras.has(orden[i]) and not _marcas[i] else String(hito["epoca"])
		# Las fechas ya descubiertas se conservan, pero las marcas se borran al mover.
		_fechas[i].text = hito["fecha"] if _reveladas.has(orden[i]) else "Fecha oculta"
		_fechas[i].add_theme_color_override("font_color", Estilo.PETROLEO)
	var elegido: Dictionary = HITOS[orden[seleccion]]
	_mensaje.text = "Tarjeta %d %s · ✓ = orden con sus vecinas · Las fechas descubiertas se conservan." % [seleccion + 1, "tomada" if tomada else "seleccionada"]
	var pista: String = _pista_clara(orden[seleccion]) if _pistas_claras.has(orden[seleccion]) else String(elegido["epoca"])
	_detalle.text = "%s: %s %s" % [elegido["titulo"], elegido["dato"], pista]


func jugar_solo(acierta: bool) -> void:
	_auto = 1 if acierta else -1
	_pulso = 0.0
