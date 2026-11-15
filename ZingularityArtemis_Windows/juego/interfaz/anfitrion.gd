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
const LIENZO_COMPLETO := Vector2(1280, 720)   # minijuegos con pantalla_completa = true (ver nucleo/minijuego.gd)

# Resplandor del campo: fuera del lienzo, cada pixel toma el color del campo reflejado en su borde, muy
# desenfocado (niveles bajos de la copia de pantalla) y atenuado con la distancia. Asi el campo no lleva marco:
# sus propios colores llegan hasta el borde de la pantalla. Un solo pase, sin imagenes ni viewport extra.
const RESPLANDOR := """
shader_type canvas_item;
uniform sampler2D pantalla : hint_screen_texture, filter_linear_mipmap, repeat_disable;
uniform vec4 campo = vec4(0.0625, 0.139, 0.875, 0.722);
uniform vec3 tinte : source_color = vec3(0.11, 0.157, 0.18);
uniform float fuerza = 0.62;
uniform float desenfoque = 5.5;
uniform float alcance = 150.0;

void fragment() {
	vec2 a = campo.xy;
	vec2 b = campo.xy + campo.zw;
	vec2 fuera = max(max(a - SCREEN_UV, SCREEN_UV - b), vec2(0.0));
	if (fuera.x + fuera.y <= 0.0) {
		COLOR = vec4(0.0);
	} else {
		vec2 espejo = clamp(SCREEN_UV, a, b);
		espejo += (espejo - SCREEN_UV) * 0.6;
		espejo = clamp(espejo, a + campo.zw * 0.04, b - campo.zw * 0.04);
		vec3 c = textureLod(pantalla, espejo, desenfoque).rgb;
		float d = length(fuera / SCREEN_PIXEL_SIZE) * (720.0 * SCREEN_PIXEL_SIZE.y);
		float caida = exp(-d / alcance);
		vec3 color = mix(tinte * 0.55, c, fuerza * caida);
		COLOR = vec4(color, 1.0);
	}
}
"""

var _marco: Control
var _ambiente: ColorRect
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
var _lienzo := LIENZO
var _completo := false           # el minijuego pidio toda la pantalla (pantalla_completa)


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	visible = false
	var velo := ColorRect.new()
	# fondo opaco: mientras se juega no se ve (ni se dibuja) el mundo 3D
	velo.color = Estilo.NOCHE.darkened(0.45)
	velo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(velo)

	# sin marco ni recuadro: el campo va centrado sobre el fondo y su resplandor llena los margenes
	_marco = Control.new()
	_marco.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_marco.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_marco)
	_hueco = Control.new()
	_hueco.custom_minimum_size = LIENZO
	_hueco.size = LIENZO
	_hueco.clip_contents = true
	_marco.add_child(_hueco)
	_ambiente = ColorRect.new()
	_ambiente.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_ambiente.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sombreador := Shader.new()
	sombreador.code = RESPLANDOR
	var material_resplandor := ShaderMaterial.new()
	material_resplandor.shader = sombreador
	material_resplandor.set_shader_parameter("tinte", Estilo.NOCHE)
	_ambiente.material = material_resplandor
	_marco.add_child(_ambiente)
	_titulo = Estilo.texto("", 18, Color(Estilo.PAPEL, 0.82), 700)
	_titulo.autowrap_mode = TextServer.AUTOWRAP_OFF
	_marco.add_child(_titulo)
	_salir = Button.new()
	_salir.text = "Esc · Salir"
	_salir.flat = true
	_salir.focus_mode = Control.FOCUS_NONE
	_salir.add_theme_font_override("font", Estilo.fuente(600))
	_salir.add_theme_font_size_override("font_size", 15)
	_salir.add_theme_color_override("font_color", Color(Estilo.PAPEL, 0.6))
	_salir.add_theme_color_override("font_hover_color", Estilo.PAPEL)
	_salir.add_theme_color_override("font_pressed_color", Estilo.PAPEL)
	_salir.pressed.connect(_abandonar)
	_marco.add_child(_salir)
	_controles = Estilo.texto("", 15, Color(Estilo.PAPEL, 0.55), 500)
	_controles.autowrap_mode = TextServer.AUTOWRAP_OFF
	_controles.clip_text = true
	_controles.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_controles.custom_minimum_size = Vector2(LIENZO.x, 0)
	_marco.add_child(_controles)

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
	_capa.position = (size - _capa.size) * 0.5
	_colocar()


func _colocar() -> void:
	# el campo centrado en pixeles enteros; titulo y salida en el margen de arriba, controles en el de abajo
	var origen: Vector2 = Vector2.ZERO if _completo else ((size - _lienzo) * 0.5).floor()
	_hueco.position = origen
	_hueco.size = _lienzo
	for nodo in [_ambiente, _titulo, _salir, _controles]:
		nodo.visible = not _completo
	_titulo.reset_size()
	_salir.reset_size()
	_controles.reset_size()
	_titulo.position = Vector2(origen.x + 2.0, origen.y - _titulo.size.y - 10.0)
	_salir.position = Vector2(origen.x + _lienzo.x - _salir.size.x, origen.y - _salir.size.y - 6.0)
	_controles.size.x = _lienzo.x
	_controles.position = Vector2(origen.x, origen.y + _lienzo.y + 12.0)
	if size.x > 0.0 and size.y > 0.0:
		var m: ShaderMaterial = _ambiente.material
		m.set_shader_parameter("campo", Vector4(origen.x / size.x, origen.y / size.y, _lienzo.x / size.x, _lienzo.y / size.y))


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
	_titulo.text = String(meta.get("titulo", id)).to_upper()
	_controles.text = meta.get("controles", "")
	_colocar()
	# el mundo 3D queda tapado por el fondo opaco: no se dibuja mientras dura el minijuego
	var vista := get_viewport()
	var tenia_3d: bool = not vista.disable_3d
	vista.disable_3d = true
	_pista = 0
	var solo := 0
	if Juego.modo_prueba or Juego.minijuegos_solos:
		solo = -1 if parametros.get("fallar", false) else 1
	var final: Dictionary = {}
	while true:
		if _minijuego != null and is_instance_valid(_minijuego):
			_minijuego.queue_free()
		_minijuego = guion.new()
		_completo = _minijuego.get("pantalla_completa") == true
		_lienzo = LIENZO_COMPLETO if _completo else LIENZO
		_colocar()
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
			if String(meta.get("controles", "")) != "":
				lineas.append(Estilo.texto("Controles: %s" % meta.get("controles", ""), 16, Estilo.TINTA_SUAVE, 500))
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
	vista.disable_3d = not tenia_3d
	return final
