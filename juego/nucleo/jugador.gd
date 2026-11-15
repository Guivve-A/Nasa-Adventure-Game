extends CharacterBody3D

# La protagonista jugable. Movimiento relativo a la camara fija (arriba en pantalla = -Z), interaccion por
# cercania y cruce de umbrales. El modelo es la malla aprobada (D-017, v9 con el bolso). Si existe la version
# con esqueleto (PER-01_rig.glb) usa sus clips "reposo", "caminar", "correr" y "salto_lunar"; si no, se mueve
# con un bamboleo por codigo.

signal piloto_llego

const Materiales := preload("res://nucleo/materiales.gd")
const Recursos := preload("res://nucleo/recursos.gd")

const MODELOS := ["res://modelos/personajes/PER-01_rig.glb", "res://modelos/personajes/PER-01.glb"]
const MEDIDAS := "res://modelos/personajes/PER-01_medidas.json"
const ALTO := 1.05               # metros (escena aprobada)
const VEL_CAMINAR := 2.0         # m/s
const VEL_CORRER := 3.6

var gravedad := 9.8
var salto := 0.0
var factor_velocidad := 1.0
var inercia := 1.0
var mirando := Vector3(0, 0, 1)   # hacia donde mira (unitario, en XZ)
var objetivo: Node3D = null       # interactuable al alcance
var modelo: Node3D
var animador: AnimationPlayer
var piloto := false               # piloto automatico (pruebas y escenas guiadas)
var piloto_destino := Vector3.ZERO
var piloto_correr := false
var zancada_caminar := 0.0        # metros por ciclo a 1 m de alto (PER-01_medidas.json); 0 = sin dato
var zancada_correr := 0.0
var _pivote := Node3D.new()       # gira hacia donde camina
var _bamboleo := Node3D.new()     # movimiento por codigo cuando no hay esqueleto
var _fase := 0.0
var _clip := ""
var _atasco := 0.0


func _ready() -> void:
	add_to_group("jugador")
	collision_layer = 2
	collision_mask = 1
	floor_snap_length = 0.35
	floor_max_angle = deg_to_rad(50.0)
	var forma := CollisionShape3D.new()
	var capsula := CapsuleShape3D.new()
	capsula.radius = 0.2
	capsula.height = 1.0
	forma.shape = capsula
	forma.position.y = 0.5
	add_child(forma)
	add_child(_pivote)
	_pivote.add_child(_bamboleo)
	_montar_modelo()


func _montar_modelo() -> void:
	for ruta in MODELOS:
		modelo = Recursos.instancia(ruta, true)
		if modelo != null:
			break
	if modelo == null:
		# sin malla: una capsula, para que el juego siga siendo jugable
		var mi := MeshInstance3D.new()
		var capsula := CapsuleMesh.new()
		capsula.radius = 0.2
		capsula.height = ALTO
		mi.mesh = capsula
		mi.position.y = ALTO * 0.5
		_bamboleo.add_child(mi)
		return
	_bamboleo.add_child(modelo)
	# alto de 1,05 m, base en el suelo y centrada bajo el nodo
	var caja := Materiales.caja_mundo(modelo)
	if caja.size.y > 0.0:
		modelo.scale = Vector3.ONE * ALTO / caja.size.y
	caja = Materiales.caja_mundo(modelo)
	modelo.position -= Vector3(caja.get_center().x, caja.position.y, caja.get_center().z) - global_position
	animador = modelo.find_child("AnimationPlayer", true, false) as AnimationPlayer
	if animador != null:
		for nombre in ["reposo", "caminar", "correr", "salto_lunar"]:
			if animador.has_animation(nombre):
				animador.get_animation(nombre).loop_mode = Animation.LOOP_LINEAR
		var medidas: Variant = Juego.leer_json(MEDIDAS)
		if medidas is Dictionary:
			zancada_caminar = float(medidas.get("zancada_caminar_m", 0.0))
			zancada_correr = float(medidas.get("zancada_correr_m", 0.0))
	_orientar(1.0)


func colocar(pos: Vector3, mira: Vector3 = Vector3(0, 0, 1)) -> void:
	global_position = pos
	velocity = Vector3.ZERO
	var plano := Vector3(mira.x, 0.0, mira.z)
	if plano.length() > 0.01:
		mirando = plano.normalized()
	_orientar(1.0)
	objetivo = null
	piloto = false


func caminar_hasta(destino: Vector3, corriendo: bool = false, maximo_s: float = 25.0) -> bool:
	# piloto automatico: camina en linea recta hasta "destino". Devuelve false si no llego a tiempo.
	piloto_destino = destino
	piloto_correr = corriendo
	piloto = true
	_atasco = 0.0
	var limite := maximo_s
	while piloto and limite > 0.0:
		await get_tree().physics_frame
		limite -= get_physics_process_delta_time()
	var llego := not piloto
	piloto = false
	return llego


func mirar_a(punto: Vector3) -> void:
	var d := Vector3(punto.x - global_position.x, 0.0, punto.z - global_position.z)
	if d.length() > 0.01:
		mirando = d.normalized()


func _physics_process(delta: float) -> void:
	var libre: bool = not Interfaz.ocupada()
	var entrada := Vector2.ZERO
	var corre := false
	if piloto:
		var d := piloto_destino - global_position
		d.y = 0.0
		if d.length() < 0.22:
			piloto = false
			piloto_llego.emit()
		else:
			entrada = Vector2(d.x, d.z).normalized()
			corre = piloto_correr
	elif libre:
		entrada = Input.get_vector("mover_izquierda", "mover_derecha", "mover_arriba", "mover_abajo")
		corre = Input.is_action_pressed("correr")
	var direccion := Vector3(entrada.x, 0.0, entrada.y)
	var rapidez_meta := (VEL_CORRER if corre else VEL_CAMINAR) * factor_velocidad
	var meta := direccion * rapidez_meta
	var en_suelo := is_on_floor()
	var aceleracion := (18.0 if en_suelo else 5.0) * inercia
	velocity.x = move_toward(velocity.x, meta.x, aceleracion * delta)
	velocity.z = move_toward(velocity.z, meta.z, aceleracion * delta)
	if en_suelo:
		if salto > 0.0 and libre and not piloto and Input.is_action_just_pressed("saltar"):
			velocity.y = salto
			Audio.sonar("salto")
	else:
		velocity.y -= gravedad * delta
	move_and_slide()
	if global_position.y < -40.0:
		_reaparecer()
	var plana := Vector3(velocity.x, 0.0, velocity.z)
	if plana.length() > 0.25:
		mirando = plana.normalized()
	_orientar(minf(1.0, 14.0 * delta))
	_animar(delta, plana.length(), corre, is_on_floor())
	_buscar_interaccion(libre)
	for u in get_tree().get_nodes_in_group("umbrales"):
		u.revisar(self)


func _reaparecer() -> void:
	# se cayo del mapa: vuelve a la entrada de la zona
	var zona: Node3D = Zonas.actual
	var pos := Vector3(0.0, 1.0, 0.0)
	if zona != null and not zona.entradas.is_empty():
		pos = zona.entradas.values()[0]["pos"] + Vector3(0.0, 0.3, 0.0)
	colocar(pos)


func _orientar(peso: float) -> void:
	# el modelo mira a +X: girar theta sobre Y lleva +X a (cos, 0, -sin)
	var angulo := atan2(-mirando.z, mirando.x)
	_pivote.rotation.y = lerp_angle(_pivote.rotation.y, angulo, peso)


func _animar(delta: float, rapidez: float, corre: bool, en_suelo: bool) -> void:
	var andando := rapidez > 0.25
	var paso_antes := sin(_fase)
	_fase += delta * rapidez * 6.5
	if andando and en_suelo and paso_antes * sin(_fase) < 0.0:
		Audio.sonar("paso", -26.0)
	if animador != null:
		var clip := "reposo"
		if not en_suelo and animador.has_animation("salto_lunar"):
			clip = "salto_lunar"
		elif andando and corre and animador.has_animation("correr"):
			clip = "correr"
		elif andando:
			clip = "caminar"
		if animador.has_animation(clip):
			if clip != _clip:
				animador.play(clip, 0.18)
				_clip = clip
			var ritmo := 1.0
			# la velocidad del clip sigue a la del cuerpo para que los pies no resbalen
			if clip == "caminar":
				ritmo = _ritmo(rapidez, zancada_caminar, VEL_CAMINAR)
			elif clip == "correr":
				ritmo = _ritmo(rapidez, zancada_correr, VEL_CORRER)
			animador.speed_scale = ritmo
			_bamboleo.position = Vector3.ZERO
			_bamboleo.rotation = Vector3.ZERO
			return
	# sin esqueleto: saltitos y balanceo
	var fuerza := clampf(rapidez / VEL_CAMINAR, 0.0, 1.6)
	var bote := absf(sin(_fase)) * 0.05 * fuerza
	var respiro := sin(Time.get_ticks_msec() * 0.002) * 0.006
	_bamboleo.position.y = lerpf(_bamboleo.position.y, bote + respiro, minf(1.0, 18.0 * delta))
	_bamboleo.rotation.x = lerpf(_bamboleo.rotation.x, sin(_fase) * 0.07 * fuerza, minf(1.0, 12.0 * delta))
	_bamboleo.rotation.z = lerpf(_bamboleo.rotation.z, -0.10 * fuerza, minf(1.0, 8.0 * delta))


func _ritmo(rapidez: float, zancada: float, nominal: float) -> float:
	if zancada > 0.0 and animador != null and animador.current_animation != "":
		var duracion := animador.current_animation_length
		var avance := zancada * ALTO / maxf(duracion, 0.05)   # m/s a ritmo 1
		return clampf(rapidez / maxf(avance, 0.05), 0.4, 2.2)
	return clampf(rapidez / nominal, 0.5, 1.6)


func reproducir(clip: String) -> void:
	# clips sueltos ("recoger", "celebrar"): suena una vez y vuelve al ciclo normal
	if animador != null and animador.has_animation(clip):
		animador.speed_scale = 1.0
		animador.play(clip, 0.12)
		_clip = clip


func _buscar_interaccion(libre: bool) -> void:
	var mejor: Node3D = null
	var mejor_nota := INF
	if libre:
		for n in get_tree().get_nodes_in_group("interactuables"):
			if not n.habilitado or not n.is_visible_in_tree():
				continue
			var hacia: Vector3 = n.global_position - global_position
			var d: float = hacia.length()
			if d >= float(n.radio):
				continue
			hacia.y = 0.0
			var de_frente := 0.0
			if hacia.length() > 0.05:
				de_frente = hacia.normalized().dot(mirando)
			var prioridad: int = int(n.get("prioridad"))
			if prioridad < 0 and de_frente < 0.2:
				continue
			# gana lo que esta de frente y cerca; lo de prioridad baja, solo si no hay otra cosa
			var nota: float = d - 0.45 * de_frente - 10.0 * float(prioridad)
			if nota < mejor_nota:
				mejor = n
				mejor_nota = nota
	if mejor != objetivo:
		objetivo = mejor
		Interfaz.indicar(("[E] " + objetivo.texto) if objetivo != null else "")
	if objetivo != null and libre and not piloto and Input.is_action_just_pressed("interactuar"):
		mirar_a(objetivo.global_position)
		objetivo.usar(self)
