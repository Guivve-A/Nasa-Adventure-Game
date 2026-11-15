extends Node2D

# Fondo de Marte con parallax (mismas capas que fondo_parallax.gd de la Luna) en tres horas.
# Las tres horas estan apiladas en cada capa; hora 0 = dia, 1 = atardecer, 2 = noche, con valores intermedios
# para pasar de una a otra poco a poco. Como las montanas tienen la misma forma en las tres horas, el cambio es limpio.

const CAPAS := [["capa_0_espacio", 0.02], ["capa_0b_sol_tierra", 0.06], ["capa_1_montanas_lejanas", 0.18], ["capa_2_montanas_medias", 0.35], ["capa_3_colinas_cercanas", 0.6]]
const HORAS := ["dia", "atardecer", "noche"]
const ANCHO := 640.0

var hora := 0.0
var _sprites: Array = []         # por capa: [dia, atardecer, noche]


func armar(carpeta: String) -> void:
	for i in CAPAS.size():
		var p := Parallax2D.new()
		p.scroll_scale = Vector2(CAPAS[i][1], 0.0)
		p.repeat_size = Vector2(ANCHO, 0.0)
		p.repeat_times = 3
		add_child(p)
		var tres: Array = []
		for h in HORAS:
			var s := Sprite2D.new()
			s.texture = preload("textura.gd").cargar(carpeta + "/" + h + "/" + CAPAS[i][0] + ".png")
			s.centered = false
			p.add_child(s)
			tres.append(s)
		_sprites.append(tres)
	poner_hora(0.0)


# suelo caminable: una tira por hora que se repite a lo ancho del nivel
func armar_suelo(carpeta: String, ancho: float, y: float) -> Node2D:
	var n := Node2D.new()
	var tres: Array = []
	for h in HORAS:
		var s := Sprite2D.new()
		s.texture = preload("textura.gd").cargar(carpeta + "/suelo_marte_" + h + ".png")
		s.centered = false
		s.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
		s.region_enabled = true
		s.region_rect = Rect2(0, 0, ancho, s.texture.get_height())
		s.position = Vector2(0, y)
		n.add_child(s)
		tres.append(s)
	_sprites.append(tres)
	poner_hora(hora)
	return n


func poner_hora(h: float) -> void:
	hora = clampf(h, 0.0, 2.0)
	var a := clampf(hora, 0.0, 1.0)            # cuanto atardecer encima del dia
	var n := clampf(hora - 1.0, 0.0, 1.0)      # cuanta noche encima del atardecer
	for i in _sprites.size():
		var tres: Array = _sprites[i]
		if i == 1:
			# los astros cambian de lugar: cada hora se desvanece por separado
			(tres[0] as Sprite2D).modulate.a = 1.0 - a
			(tres[1] as Sprite2D).modulate.a = a - n
			(tres[2] as Sprite2D).modulate.a = n
		else:
			(tres[0] as Sprite2D).modulate.a = 1.0
			(tres[1] as Sprite2D).modulate.a = a
			(tres[2] as Sprite2D).modulate.a = n
