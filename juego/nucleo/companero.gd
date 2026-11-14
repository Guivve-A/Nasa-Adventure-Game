extends Node3D

# Orbita, el gato cientifico: sigue a la protagonista, se sienta cuando ella se detiene y da pistas al hablarle.
# Modelo con esqueleto (rig de Rigify hecho por script) y clips "reposo" y "caminar".

const Materiales := preload("res://nucleo/materiales.gd")
const Recursos := preload("res://nucleo/recursos.gd")
const Interactuable := preload("res://nucleo/interactuable.gd")

const MODELO := "res://modelos/personajes/PER-09_rig.glb"
const ALTO := 0.5

var jugador: CharacterBody3D
var modelo: Node3D
var animador: AnimationPlayer
var hablar: Node3D
var _pivote := Node3D.new()
var _mira := Vector3(0, 0, 1)
var _clip := ""
var _pistas_dadas := {}


func _ready() -> void:
	add_child(_pivote)
	modelo = Recursos.instancia(MODELO, true)
	if modelo != null:
		_pivote.add_child(modelo)
		var caja := Materiales.caja_mundo(modelo)
		if caja.size.y > 0.0:
			modelo.scale = Vector3.ONE * ALTO / caja.size.y
		caja = Materiales.caja_mundo(modelo)
		modelo.position -= Vector3(caja.get_center().x, caja.position.y, caja.get_center().z) - global_position
		animador = modelo.find_child("AnimationPlayer", true, false) as AnimationPlayer
		if animador != null:
			for nombre in ["reposo", "caminar"]:
				if animador.has_animation(nombre):
					animador.get_animation(nombre).loop_mode = Animation.LOOP_LINEAR
	hablar = Interactuable.new()
	hablar.name = "HablarConOrbita"
	hablar.texto = "Hablar con Órbita"
	hablar.radio = 1.0
	hablar.altura_marca = 0.75
	hablar.al_usar = _hablar
	add_child(hablar)


func colocar_junto(pos: Vector3, mira: Vector3) -> void:
	var lado := Vector3(mira.z, 0.0, -mira.x)
	global_position = pos + lado * 0.6 - mira * 0.35
	_mira = mira


func _physics_process(delta: float) -> void:
	if jugador == null or not is_instance_valid(jugador):
		return
	var mira: Vector3 = jugador.mirando
	var lado := Vector3(mira.z, 0.0, -mira.x)
	var destino: Vector3 = jugador.global_position - mira * 0.75 + lado * 0.55
	var d := destino - global_position
	d.y = 0.0
	var distancia := d.length()
	var rapidez := 0.0
	if distancia > 9.0:
		global_position = destino
	elif distancia > 0.55:
		rapidez = minf(distancia * 2.6, 4.2)
		global_position += d.normalized() * rapidez * delta
		_mira = d.normalized()
	# sigue el suelo con un rayo hacia abajo
	var espacio := get_world_3d().direct_space_state
	var desde := Vector3(global_position.x, jugador.global_position.y + 1.6, global_position.z)
	var consulta := PhysicsRayQueryParameters3D.create(desde, desde - Vector3(0.0, 5.0, 0.0), 1)
	var golpe := espacio.intersect_ray(consulta)
	var suelo: float = golpe["position"].y if not golpe.is_empty() else jugador.global_position.y
	global_position.y = lerpf(global_position.y, suelo, minf(1.0, 12.0 * delta))
	# el gato mira a +Z: girar theta sobre Y lleva +Z a (sin, 0, cos)
	_pivote.rotation.y = lerp_angle(_pivote.rotation.y, atan2(_mira.x, _mira.z), minf(1.0, 10.0 * delta))
	if animador != null:
		var clip := "caminar" if rapidez > 0.3 else "reposo"
		if clip != _clip and animador.has_animation(clip):
			animador.play(clip, 0.2)
			_clip = clip
		animador.speed_scale = clampf(rapidez / 1.4, 0.8, 2.2) if clip == "caminar" else 1.0


func _hablar() -> void:
	var lineas: Array = []
	var zona: Node3D = Zonas.actual
	if zona != null:
		lineas = zona.orbita_dice()
	if lineas.is_empty():
		var paso := Juego.paso_actual()
		var pistas: Array = paso.get("pistas", [])
		var clave: String = paso.get("bandera", "")
		if pistas.is_empty():
			var texto: String = paso.get("pista", "")
			if texto == "":
				texto = "Miau." if Juego.objetivo() == "" else "Yo iría por ahí: %s" % Juego.objetivo()
			pistas = [texto]
		# pistas en niveles: cada vez que se le pregunta por lo mismo, dice un poco mas
		var nivel: int = mini(int(_pistas_dadas.get(clave, 0)), pistas.size() - 1)
		_pistas_dadas[clave] = nivel + 1
		lineas = [{"quien": "Órbita", "texto": String(pistas[nivel])}]
	await Interfaz.decir(lineas)
	Juego.poner_bandera("hablo_orbita")
