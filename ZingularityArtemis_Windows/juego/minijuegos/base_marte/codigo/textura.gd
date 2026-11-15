extends RefCounted

# Carga una imagen PNG. Si Godot ya la importo, usa load(); si no (por ejemplo, el juego principal se abre
# con su cache de importacion de antes), la lee directo del disco. Asi el capitulo de Marte funciona en los dos casos.

static var _cache := {}


static func cargar(ruta: String) -> Texture2D:
	if _cache.has(ruta):
		return _cache[ruta]
	var t: Texture2D = null
	if ResourceLoader.exists(ruta):
		t = load(ruta)
	else:
		var img := Image.load_from_file(ProjectSettings.globalize_path(ruta))
		if img != null and not img.is_empty():
			t = ImageTexture.create_from_image(img)
	_cache[ruta] = t
	return t
