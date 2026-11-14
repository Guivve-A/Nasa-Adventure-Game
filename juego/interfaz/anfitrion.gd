extends Control

# Anfitrion de minijuegos: pone el marco comun (titulo, instrucciones, controles, pistas de Orbita y resultado)
# alrededor de cualquier minijuego de res://minijuegos/<id>/. Asi todos se presentan igual.
#
# minijuego.json:
#   {"titulo": "...", "resumen": "una frase", "instrucciones": ["paso 1", "paso 2"], "controles": "texto",
#    "pistas": ["mirada", "frase", "respuesta"], "ficha": "id_de_ficha", "orden": 1, "escena": "1.2"}

signal _boton(accion: String)

const Estilo := preload("res://interfaz/estilo.gd")
const LIENZO := Vector2(1120, 520)

var _marco: PanelContainer
var _titulo: Label
var _controles: Label
var _hueco: Control
var _capa: PanelContainer
var _capa_columna: VBoxContainer
var _salir: Button
var _minijuego: Control = null
var _resultado: Dictionary = {}
var _pendiente := false
var _pista := 0


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var velo := ColorRect.new()
	velo.color = Color(Estilo.NOCHE, 0.93)
	velo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(velo)

	_marco = Estilo.panel(Estilo.PAPEL, 16, 4, 16)
	add_child(_marco)
	var columna := VBoxContainer.new()
	columna.add_theme_constant_override("separation", 8)
	_marco.add_child(columna)
	var cabecera := HBoxContainer.new()
	_titulo = Estilo.texto("", 28, Estilo.TINTA, 700)
	_titulo.autowrap_mode = TextServer.AUTOWRAP_OFF
	_titulo.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	cabecera.add_child(_titulo)
	_salir = Estilo.boton("Salir (Esc)", 16)
	_salir.custom_minimum_size = Vector2(130, 36)
	_salir.focus_mode = Control.FOCUS_NONE
	_salir.pressed.connect(_abandonar)
	cabecera.add_child(_salir)
	columna.add_child(cabecera)
	var fondo_lienzo := Estilo.panel(Color("fbf3df"), 8, 2, 0)
	_hueco = Control.new()
	_hueco.custom_minimum_size = LIENZO
	_hueco.clip_contents = true
	fondo_lienzo.add_child(_hueco)
	columna.add_child(fondo_lienzo)
	_controles = Estilo.texto("", 16, Estilo.TINTA_SUAVE, 500)
	_controles.custom_minimum_size = Vector2(LIENZO.x, 0)
	columna.add_child(_controles)

	_capa = Estilo.panel(Color(Estilo.PAPEL, 0.98), 16, 4, 26)
	_capa.custom_minimum_size = Vector2(720, 0)
	_capa_columna = VBoxContainer.new()
	_capa_columna.add_theme_constant_override("separation", 12)
	_capa.add_child(_capa_columna)
	_capa.visible = false
	add_child(_capa)


func _process(_delta: float) -> void:
	if not visible:
		return
	_capa.reset_size()
	_marco.position = (size - _marco.size) * 0.5
	_capa.position = (size - _capa.size) * 0.5


func _unhandled_input(evento: InputEvent) -> void:
	if visible and _minijuego != null and evento.is_action_pressed("pausa"):
		get_viewport().set_input_as_handled()
		_abandonar()


func _abandonar() -> void:
	if _minijuego != null and _minijuego.get("activo"):
		_minijuego.set("activo", false)
		_resultado = {"superado": false, "abandonado": true, "puntos": 0.0, "detalle": ""}
		_pendiente = false
	elif _capa.visible:
		_boton.emit("salir")


func _al_terminar(resultado: Dictionary) -> void:
	_resultado = resultado
	_pendiente = false


func _llenar_capa(titulo: String, color: Color, lineas: Array, botones: Array) -> void:
	for hijo in _capa_columna.get_children():
		_capa_columna.remove_child(hijo)
		hijo.queue_free()
	_capa_columna.add_child(Estilo.texto(titulo, 30, color, 700))
	for l in lineas:
		if l is Control:
			_capa_columna.add_child(l)
		elif str(l) != "":
			var etiqueta := Estilo.texto(str(l), 20, Estilo.TINTA, 500)
			etiqueta.custom_minimum_size = Vector2(660, 0)
			_capa_columna.add_child(etiqueta)
	var fila := HBoxContainer.new()
	fila.add_theme_constant_override("separation", 12)
	fila.alignment = BoxContainer.ALIGNMENT_END
	var primero: Button = null
	for par in botones:
		var b := Estilo.boton(par[0], 20, par.size() > 2)
		b.custom_minimum_size = Vector2(170, 46)
		var accion: String = par[1]
		b.pressed.connect(func(): _boton.emit(accion))
		fila.add_child(b)
		if primero == null:
			primero = b
	_capa_columna.add_child(Estilo.separador(4))
	_capa_columna.add_child(fila)
	_capa.visible = true
	_capa.reset_size()
	if primero != null:
		primero.grab_focus.call_deferred()


func _ficha_control(id_ficha: String) -> Control:
	var f := Juego.ficha(id_ficha)
	if f.is_empty():
		return Estilo.separador(0)
	var caja := Estilo.panel(Color("fffaf0"), 10, 2, 12)
	var columna := VBoxContainer.new()
	columna.add_child(Estilo.texto("AL CUADERNO · %s" % String(f.get("titulo", "")).to_upper(), 14, Estilo.PETROLEO, 700))
	var cuerpo := Estilo.texto(f.get("texto", ""), 18, Estilo.TINTA, 500)
	cuerpo.custom_minimum_size = Vector2(630, 0)
	columna.add_child(cuerpo)
	columna.add_child(Estilo.texto("Fuente: %s" % f.get("fuente", ""), 14, Estilo.TINTA_SUAVE, 500))
	caja.add_child(columna)
	return caja


func jugar(id: String, parametros: Dictionary) -> Dictionary:
	var meta := Juego.info_minijuego(id)
	var ruta := "res://minijuegos/%s/%s.gd" % [id, id]
	if meta.is_empty() or not FileAccess.file_exists(ruta):
		print("AVISO minijuego inexistente: ", id)
		return {"superado": false, "error": "no existe", "puntos": 0.0}
	var guion: Variant = load(ruta)
	visible = true
	_titulo.text = meta.get("titulo", id)
	_controles.text = meta.get("controles", "")
	_marco.reset_size()
	_pista = 0
	var solo := 0
	if Juego.modo_prueba:
		solo = -1 if parametros.get("fallar", false) else 1
	var final: Dictionary = {}
	while true:
		if _minijuego != null and is_instance_valid(_minijuego):
			_minijuego.queue_free()
		_minijuego = guion.new()
		_hueco.add_child(_minijuego)
		_minijuego.position = Vector2.ZERO
		_minijuego.terminado.connect(_al_terminar)
		_minijuego.set("_solo", solo)
		_minijuego.preparar(parametros, meta)
		if solo == 0:
			var lineas: Array = [meta.get("resumen", "")]
			var n := 1
			for paso in meta.get("instrucciones", []):
				lineas.append("%d. %s" % [n, paso])
				n += 1
			if _pista > 0:
				var pistas: Array = meta.get("pistas", [])
				if not pistas.is_empty():
					lineas.append("Órbita: «%s»" % pistas[mini(_pista - 1, pistas.size() - 1)])
			_llenar_capa(meta.get("titulo", id), Estilo.TINTA, lineas, [["Empezar", "empezar", true], ["Salir", "salir"]])
			var accion: String = await _boton
			_capa.visible = false
			if accion == "salir":
				final = {"superado": false, "abandonado": true, "puntos": 0.0}
				break
		_pendiente = true
		_minijuego.empezar()
		while _pendiente:
			await get_tree().process_frame
		final = _resultado
		print("MINIJUEGO %s superado=%s puntos=%.1f detalle=%s" % [id, str(final.get("superado", false)), float(final.get("puntos", 0.0)), str(final.get("detalle", ""))])
		if solo != 0 or final.get("abandonado", false):
			break
		var siguiente := ""
		if final.get("superado", false):
			Audio.sonar("ok")
			var id_ficha: String = meta.get("ficha", "")
			var extra: Array = [final.get("detalle", "")]
			if id_ficha != "":
				Juego.anotar(id_ficha)
				extra.append(_ficha_control(id_ficha))
			_llenar_capa("¡Logrado!", Estilo.CIAN_MEDIO, extra, [["Continuar", "continuar", true], ["Otra vez", "reintentar"]])
			siguiente = await _boton
		else:
			Audio.sonar("error")
			_pista += 1
			_llenar_capa("Casi", Estilo.TERRACOTA, [final.get("detalle", ""), "Órbita puede darte una pista antes del próximo intento."], [["Reintentar", "reintentar", true], ["Salir", "salir"]])
			siguiente = await _boton
		_capa.visible = false
		if siguiente != "reintentar":
			break
	if final.get("superado", false):
		var ficha_final: String = meta.get("ficha", "")
		if ficha_final != "":
			Juego.anotar(ficha_final)
	if _minijuego != null and is_instance_valid(_minijuego):
		_minijuego.queue_free()
	_minijuego = null
	_capa.visible = false
	visible = false
	return final
