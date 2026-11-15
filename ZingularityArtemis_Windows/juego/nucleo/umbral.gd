extends Node3D

# Umbral: el punto de entrada y salida de una escena. Al pisarlo, el juego abre la ventana de carga y pasa a
# "destino_zona" por su entrada "destino_entrada". Se dibuja como la marca cian del concepto de la Habitacion.
#
# Regla de diseno (Guillermo, 2026-11-12): cada escena lleva disenado su espacio de entrada y salida. Alrededor
# de un umbral debe quedar un tramo despejado de unos 2 x 2 m, y la entrada asociada coloca a la protagonista
# a 1,2 m o mas de la marca, ya dentro de la escena y mirando hacia ella.

const SHADER := preload("res://shaders/umbral.gdshader")
const Materiales := preload("res://nucleo/materiales.gd")

var destino_zona := ""
var destino_entrada := "inicio"
var etiqueta := ""            # texto del aviso al acercarse, p. ej. "Al sendero del arroyo"
var radio := 0.7              # distancia a la que se cruza
var requiere := ""            # bandera necesaria para pasar ("" = siempre abierto)
var mensaje_cerrado := ""     # lo que dice Orbita si todavia no se puede pasar
var con_tecla := false        # true: hay que pulsar "interactuar" (puertas, la cama); false: se cruza al pisar
var sin_carga := false        # true: fundido corto en vez de la ventana de carga (puertas dentro de un mismo lugar)
var al_cruzar: Callable       # opcional: se llama antes de cambiar de zona (puede ser una corrutina)
var armado := false           # se arma cuando la protagonista se aleja: evita rebotar al llegar
var _malla: MeshInstance3D
var _material: ShaderMaterial
var _avisado := false
var _cruzando := false


func _ready() -> void:
	add_to_group("umbrales")
	_malla = MeshInstance3D.new()
	var plano := PlaneMesh.new()
	plano.size = Vector2(1.15, 1.15)
	_malla.mesh = plano
	_material = ShaderMaterial.new()
	_material.shader = SHADER
	_material.set_shader_parameter("inclinacion", float(Materiales.parametros.get("inclinacion", 0.45)))
	_malla.material_override = _material
	_malla.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_malla.position.y = 0.03
	add_child(_malla)


func abierto() -> bool:
	# en la visita libre (menu Lugares) todo esta abierto, para poder validar cada escenario
	return requiere == "" or bool(Juego.bandera(requiere)) or bool(Juego.bandera("visita_libre"))


func revisar(jugador: Node3D) -> void:
	# lo llama la protagonista en cada cuadro de fisica
	_material.set_shader_parameter("cerrado", 0.0 if abierto() else 1.0)
	_material.set_shader_parameter("inclinacion", float(Materiales.parametros.get("inclinacion", 0.45)))
	var d := Vector2(jugador.global_position.x - global_position.x, jugador.global_position.z - global_position.z).length()
	var misma_altura := absf(jugador.global_position.y - global_position.y) < 1.2
	var dentro := d < radio and misma_altura
	if not armado:
		if d > radio + 0.45:
			armado = true
		return
	if d > radio + 1.6:
		_avisado = false
	if d < radio + 1.4 and misma_altura and etiqueta != "" and abierto() and not _cruzando:
		Interfaz.rotular(self, ("[E] " if con_tecla else "") + etiqueta)
	else:
		Interfaz.rotular(self, "")
	if not dentro or _cruzando or Interfaz.ocupada():
		return
	if not abierto():
		if not _avisado:
			_avisado = true
			if mensaje_cerrado != "":
				Interfaz.decir([{"quien": "Órbita", "texto": mensaje_cerrado}])
		return
	if con_tecla and not Input.is_action_just_pressed("interactuar") and not jugador.get("piloto"):
		return
	cruzar()


func cruzar() -> void:
	if _cruzando:
		return
	_cruzando = true
	Interfaz.rotular(self, "")
	Audio.sonar("umbral")
	if al_cruzar.is_valid():
		await al_cruzar.call()
	if destino_zona != "" and destino_zona != Zonas.id_actual:
		# sin await: este nodo se libera junto con su zona durante el cambio
		Zonas.ir_a(destino_zona, destino_entrada, {"sin_carga": sin_carga})
		return
	if destino_zona != "":
		# otra entrada de la misma zona: el nodo sigue vivo
		await Zonas.ir_a(destino_zona, destino_entrada, {"sin_carga": true})
	armado = false
	_cruzando = false
