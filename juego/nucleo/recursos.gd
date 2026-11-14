extends RefCounted

# Carga en tiempo de ejecucion, con cache, de mallas GLB (carpeta modelos/, con .gdignore) y de imagenes.
# Las plantillas no entran al arbol: se duplican con instancia() y se liberan con liberar() al salir.

const Materiales := preload("res://nucleo/materiales.gd")

static var _plantillas: Dictionary = {}
static var _texturas: Dictionary = {}


static func existe(ruta: String) -> bool:
	return FileAccess.file_exists(ruta)


static func plantilla(ruta: String, fijo: bool = false) -> Node3D:
	# malla GLB con los materiales del estilo ya puestos; null si el archivo no existe o no se puede leer
	var clave := ruta + ("|fijo" if fijo else "")
	if _plantillas.has(clave):
		var guardada: Variant = _plantillas[clave]
		if guardada == null or is_instance_valid(guardada):
			return guardada
	var nodo: Node3D = null
	if FileAccess.file_exists(ruta):
		var doc := GLTFDocument.new()
		var estado := GLTFState.new()
		var error := doc.append_from_file(ruta, estado)
		if error == OK:
			nodo = doc.generate_scene(estado) as Node3D
		else:
			push_warning("No se pudo leer %s (error %d)" % [ruta, error])
	if nodo != null:
		Materiales.aplicar(nodo, fijo)
	_plantillas[clave] = nodo
	return nodo


static func instancia(ruta: String, fijo: bool = false) -> Node3D:
	var p := plantilla(ruta, fijo)
	if p == null:
		return null
	return p.duplicate() as Node3D


static func olvidar_zona() -> void:
	# las plantillas de la zona llevan materiales de esa zona: se sueltan al cambiar (las fijas se quedan)
	for clave in _plantillas.keys():
		if String(clave).ends_with("|fijo"):
			continue
		var p: Variant = _plantillas[clave]
		if p != null and is_instance_valid(p):
			p.free()
		_plantillas.erase(clave)


static func textura(ruta: String) -> Texture2D:
	# imagen importada por Godot si existe; si no, leida del disco (sirve sin exportar)
	if _texturas.has(ruta):
		return _texturas[ruta]
	var t: Texture2D = null
	if ResourceLoader.exists(ruta):
		t = load(ruta) as Texture2D
	elif FileAccess.file_exists(ruta):
		var imagen := Image.new()
		if imagen.load(ProjectSettings.globalize_path(ruta)) == OK:
			imagen.generate_mipmaps()
			t = ImageTexture.create_from_image(imagen)
	_texturas[ruta] = t
	return t


static func liberar() -> void:
	for p in _plantillas.values():
		if p != null and is_instance_valid(p):
			p.free()
	_plantillas.clear()
	_texturas.clear()
