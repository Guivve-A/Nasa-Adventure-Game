extends Node3D

# Algo con lo que la protagonista puede interactuar al acercarse y pulsar "interactuar" (E, Intro o boton A).
# Muestra un rombo cian flotante cuando ella esta cerca: el cian es la unica pista visual de interaccion
# (pilar «el cian es la tecnologia» de la Biblia de arte).

signal usado(jugador: Node3D)

const Materiales := preload("res://nucleo/materiales.gd")

var texto := "Examinar"       # verbo que aparece en el aviso: "[E] Examinar"
var radio := 1.3              # distancia de uso en metros
var habilitado := true
var al_usar: Callable         # funcion que se llama al usarlo (puede ser una corrutina)
var altura_marca := 1.2       # altura del rombo sobre el origen del nodo
var una_vez := false          # se desactiva solo tras el primer uso
var prioridad := 0            # -1: solo se elige si no hay otra cosa al alcance y se le mira (Orbita)
var _marca: MeshInstance3D
var _t := 0.0
var _cerca := 0.0


func _ready() -> void:
	add_to_group("interactuables")
	_marca = MeshInstance3D.new()
	var brillo := Materiales.emisivo(Color("62e4e0"), 2.2)
	var punta := CylinderMesh.new()
	punta.top_radius = 0.0
	punta.bottom_radius = 0.085
	punta.height = 0.15
	punta.radial_segments = 4
	punta.rings = 1
	_marca.mesh = punta
	_marca.material_override = brillo
	_marca.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var abajo := MeshInstance3D.new()
	abajo.mesh = punta
	abajo.material_override = brillo
	abajo.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	abajo.rotation.x = PI
	abajo.position.y = -0.15
	_marca.add_child(abajo)
	_marca.visible = false
	add_child(_marca)


func _process(delta: float) -> void:
	_t += delta
	var jugador: Node3D = Zonas.jugador
	var d := 99.0
	if jugador != null and is_instance_valid(jugador):
		d = global_position.distance_to(jugador.global_position)
	var objetivo := 1.0 if (habilitado and d < radio + 2.2) else 0.0
	_cerca = move_toward(_cerca, objetivo, delta * 4.0)
	_marca.visible = _cerca > 0.02
	if _marca.visible:
		var elegido: bool = jugador != null and jugador.get("objetivo") == self
		var k := _cerca * (1.0 if elegido else 0.6)
		_marca.scale = Vector3.ONE * k * (1.25 if elegido else 1.0)
		# la inclinacion comun de la escena desplaza hacia atras lo que esta alto: la marca la acompana
		var cizalla := float(Materiales.parametros.get("inclinacion", 0.45))
		var alto := altura_marca + 0.05 * sin(_t * 3.0)
		_marca.global_position = global_position + Vector3(0.0, alto, -cizalla * (global_position.y + alto))
		_marca.rotation.y = _t * 1.5


func usar(jugador: Node3D) -> void:
	if not habilitado:
		return
	if una_vez:
		habilitado = false
	Audio.sonar("pulsar")
	usado.emit(jugador)
	if al_usar.is_valid():
		await al_usar.call()
