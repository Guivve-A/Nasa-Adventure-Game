extends RefCounted

# Fuente pixel propia de la seccion de Marte (herramientas/fuente_pixel.py dibuja las letras).
# Arma un FontFile de mapa de bits a partir de recursos/fuente/pixel_marte.png y .json.
# Tamano base 8: los tamanos de 8 a 15 se ven a 1x y los de 16 o mas a 2x, siempre nitidos.
# Si falta una letra, se usa la fuente por defecto de Godot.

const BASE := 8

static var _fuente: FontFile


static func obtener() -> Font:
	if _fuente != null:
		return _fuente
	# funciona suelto (res://recursos) o dentro del juego principal (res://minijuegos/base_marte/recursos)
	var raiz: String = "res://recursos/fuente/"
	if not FileAccess.file_exists(raiz + "pixel_marte.json"):
		raiz = "res://minijuegos/base_marte/recursos/fuente/"
	var tex: Texture2D = preload("textura.gd").cargar(raiz + "pixel_marte.png")
	var meta: Dictionary = (load(raiz + "pixel_marte.json") as JSON).data
	if tex == null:
		return ThemeDB.fallback_font
	var f := FontFile.new()
	f.antialiasing = TextServer.FONT_ANTIALIASING_NONE
	f.generate_mipmaps = false
	f.multichannel_signed_distance_field = false
	f.fixed_size = BASE
	f.fixed_size_scale_mode = TextServer.FIXED_SIZE_SCALE_INTEGER_ONLY
	f.fallbacks = [ThemeDB.fallback_font]
	var tam := Vector2i(BASE, 0)
	var asc := float(meta["ascenso"])
	var alto := float(meta["alto"])
	f.set_cache_ascent(0, BASE, asc)
	f.set_cache_descent(0, BASE, alto - asc)
	f.set_texture_image(0, tam, 0, tex.get_image())
	var glifos: Dictionary = meta["glifos"]
	for k in glifos:
		var g: Array = glifos[k]
		var cod := int(k)
		var x := float(g[0])
		var w := float(g[1])
		f.set_glyph_advance(0, BASE, cod, Vector2(w + 1.0, 0.0))
		f.set_glyph_offset(0, tam, cod, Vector2(0.0, -asc))
		f.set_glyph_size(0, tam, cod, Vector2(w, alto))
		f.set_glyph_uv_rect(0, tam, cod, Rect2(x, 0.0, w, alto))
		f.set_glyph_texture_idx(0, tam, cod, 0)
	_fuente = f
	return f
