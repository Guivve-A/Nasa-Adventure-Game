extends AnimatedSprite2D

# Personaje lunar en pixel art (32 x 32 por cuadro) para Godot 4.
# Arma sus animaciones solo, a partir de recursos/personajes/<id>.png y <id>.json.
# La posicion del nodo es la de los pies, para apoyarlo directo en el suelo.
#
# Ids: jugador (quieto, caminar, saltar) y comandante, geologa, ingeniero, piloto, medica (quieto, hablar).
#
# Uso en el editor: crea un AnimatedSprite2D, asignale este script y escribe el id en "personaje".
# Uso por codigo:
#   var p = preload("personaje.gd").new()
#   p.personaje = "geologa"
#   add_child(p)

@export var personaje := "jugador"
@export var escala_pixel := 1.0    # el proyecto ya escala la pantalla: 1 = un pixel del arte

var tam := 32


func _ready() -> void:
	cargar(personaje)


func cargar(id: String) -> void:
	personaje = id
	var base: String = (get_script() as Script).resource_path.get_base_dir().get_base_dir() + "/recursos/personajes/"
	var hoja: Texture2D = load(base + id + ".png")
	var datos: JSON = load(base + id + ".json")
	if hoja == null or datos == null:
		push_warning("personaje.gd: falta recursos/personajes/%s.png o .json" % id)
		return
	var meta: Dictionary = datos.data
	tam = int(meta.get("tam", 32))
	var marcos := SpriteFrames.new()
	var anims: Dictionary = meta["animaciones"]
	for nombre in anims:
		var a: Dictionary = anims[nombre]
		marcos.add_animation(nombre)
		marcos.set_animation_speed(nombre, float(a["fps"]))
		marcos.set_animation_loop(nombre, bool(a["bucle"]))
		for c in int(a["cuadros"]):
			var recorte := AtlasTexture.new()
			recorte.atlas = hoja
			recorte.region = Rect2(c * tam, int(a["fila"]) * tam, tam, tam)
			marcos.add_frame(nombre, recorte)
	if marcos.has_animation("default") and not anims.has("default"):
		marcos.remove_animation("default")
	sprite_frames = marcos
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	centered = true
	offset = Vector2(0, -tam * 0.5)
	scale = Vector2(escala_pixel, escala_pixel)
	play("quieto")


func mirar(direccion: float) -> void:
	# los sprites miran a la derecha; con direccion negativa se voltean
	if direccion != 0.0:
		flip_h = direccion < 0.0
