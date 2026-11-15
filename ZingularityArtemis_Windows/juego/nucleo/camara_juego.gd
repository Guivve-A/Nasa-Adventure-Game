extends Camera3D

# Camara de juego aprobada (D-013 y D-015): alta, fija, a 48 grados, campo de 40 grados, sin horizonte.
# Sigue a la protagonista con suavidad. El encuadre es la fraccion del alto de pantalla que ocupa el personaje:
# 0,21 en el ancla aprobada y 0,125 en el texto de la biblia; se cambia con Z y X (o la rueda) para decidir.

const INCLINACION_GRADOS := 48.0
const CAMPO_GRADOS := 40.0
const ALTO_PERSONAJE := 1.05

var objetivo: Node3D
var encuadre := 0.18
var cizalla := 0.45
var limites := Rect2()
var suavizado := 7.0
var fijo := false                 # true: no sigue (tomas fijas)
var _foco := Vector3.ZERO
var _encuadre_actual := 0.18


func _ready() -> void:
	fov = CAMPO_GRADOS
	current = true
	process_mode = Node.PROCESS_MODE_ALWAYS


func centrar() -> void:
	# corta directo al objetivo (al entrar a una zona)
	if objetivo != null and is_instance_valid(objetivo):
		_foco = _limitar(objetivo.global_position)
	_encuadre_actual = encuadre
	_colocar()


func _limitar(p: Vector3) -> Vector3:
	if limites.size.x > 0.0 and limites.size.y > 0.0:
		p.x = clampf(p.x, limites.position.x, limites.end.x)
		p.z = clampf(p.z, limites.position.y, limites.end.y)
	return p


func _process(delta: float) -> void:
	if not get_tree().paused and not Interfaz.ocupada():
		if Input.is_action_pressed("acercar"):
			encuadre = minf(encuadre + 0.08 * delta, 0.24)
		if Input.is_action_pressed("alejar"):
			encuadre = maxf(encuadre - 0.08 * delta, 0.10)
	if objetivo != null and is_instance_valid(objetivo) and not fijo:
		var peso := 1.0 - exp(-suavizado * delta)
		_foco = _foco.lerp(_limitar(objetivo.global_position), peso)
	_encuadre_actual = lerpf(_encuadre_actual, encuadre, 1.0 - exp(-6.0 * delta))
	_colocar()


func _unhandled_input(evento: InputEvent) -> void:
	if evento is InputEventMouseButton and evento.pressed and not Interfaz.ocupada():
		if evento.button_index == MOUSE_BUTTON_WHEEL_UP:
			encuadre = minf(encuadre + 0.01, 0.24)
		elif evento.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			encuadre = maxf(encuadre - 0.01, 0.10)


func _colocar() -> void:
	var inc := deg_to_rad(INCLINACION_GRADOS)
	# con la inclinacion del shader, la vertical se ve casi a su altura real
	var factor := cos(inc) + cizalla * sin(inc)
	var distancia := ALTO_PERSONAJE * factor / (2.0 * _encuadre_actual * tan(deg_to_rad(fov * 0.5)))
	var medio := _foco.y + ALTO_PERSONAJE * 0.5
	# la inclinacion comun dibuja cada punto en z - cizalla * y: el foco sigue a lo que se ve
	var foco := Vector3(_foco.x, medio, _foco.z - cizalla * medio)
	var direccion := Vector3(0.0, sin(inc), cos(inc))
	look_at_from_position(foco + direccion * distancia, foco, Vector3.UP)
	far = distancia * 4.0 + 20.0


func a_pantalla(punto: Vector3) -> Vector2:
	# posicion en pantalla de un punto del mundo, contando la inclinacion 2.5D
	return unproject_position(Vector3(punto.x, punto.y, punto.z - cizalla * punto.y))
