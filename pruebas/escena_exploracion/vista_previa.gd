extends Node3D

# Vista previa de un recurso suelto, con la luz y los shaders de la escena.
# Argumentos tras "--":  --glb=<ruta>  --captura=<png>  [--altura=<m>]  [--angulo=juego|lateral]  [--giro=<grados>]  [--suave]
# Sin --captura queda abierta: flechas para girar, Esc para salir.

var captura := ""
var angulo := "juego"
var altura := 0.0
var animacion := ""
var tiempo := 0.0
var suave := false
var pintado := 1.0
var recurso: Node3D
var pivote := Node3D.new()
var camara := Camera3D.new()
var giro := 0.0


func _ready() -> void:
	var glb := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--glb="):
			glb = arg.trim_prefix("--glb=")
		elif arg.begins_with("--captura="):
			captura = arg.trim_prefix("--captura=")
		elif arg.begins_with("--altura="):
			altura = float(arg.trim_prefix("--altura="))
		elif arg.begins_with("--angulo="):
			angulo = arg.trim_prefix("--angulo=")
		elif arg.begins_with("--animacion="):
			animacion = arg.trim_prefix("--animacion=")
		elif arg.begins_with("--tiempo="):
			tiempo = float(arg.trim_prefix("--tiempo="))
		elif arg.begins_with("--giro="):
			giro = deg_to_rad(float(arg.trim_prefix("--giro=")))
		elif arg == "--suave":
			suave = true
		elif arg.begins_with("--pintado="):
			pintado = float(arg.trim_prefix("--pintado="))
	Iluminacion.montar(self)
	add_child(pivote)
	pivote.rotation.y = giro  # las mallas de Tripo miran a +-X: --giro=90 pone de frente la que mira a -X
	recurso = Materiales.cargar_glb(glb)
	if recurso == null:
		get_tree().quit(1)
		return
	pivote.add_child(recurso)
	var info := Materiales.aplicar(recurso)
	if suave:
		Materiales.ajustar_parametro("facetas_planas", false)  # normales suaves de la malla
	Materiales.ajustar_parametro("pintado", pintado)  # 1 = acabado 2.5D (por defecto), 0 = luz 3D celular
	var reproductor := recurso.find_child("AnimationPlayer", true, false) as AnimationPlayer
	if reproductor != null:
		print("ANIMACIONES ", reproductor.get_animation_list())
		if animacion != "":
			reproductor.play(animacion)
			reproductor.seek(tiempo, true)
			reproductor.speed_scale = 0.0  # congelada en el instante pedido
	var caja := Materiales.caja_mundo(recurso)
	if altura > 0.0 and caja.size.y > 0.0:
		recurso.scale *= altura / caja.size.y
		caja = Materiales.caja_mundo(recurso)
	# apoyar en el suelo y centrar
	recurso.position -= Vector3(caja.get_center().x, caja.position.y, caja.get_center().z)
	caja = Materiales.caja_mundo(recurso)
	_suelo(maxf(caja.size.x, caja.size.z) * 3.0 + 2.0)
	add_child(camara)
	camara.fov = 30.0
	_encuadrar(caja)
	print("RECURSO %s triangulos=%d superficies=%d tamano=%s" % [glb.get_file(), info["triangulos"], info["superficies"], str(caja.size)])
	if captura != "":
		for i in range(20):
			await get_tree().process_frame
		var imagen := get_viewport().get_texture().get_image()
		imagen.save_png(captura)
		print("CAPTURA_OK ", captura)
		get_tree().quit()


func _suelo(lado: float) -> void:
	var plano := MeshInstance3D.new()
	var malla := PlaneMesh.new()
	malla.size = Vector2(lado, lado)
	plano.mesh = malla
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("a48a29").darkened(0.15)
	mat.roughness = 1.0
	plano.material_override = mat
	add_child(plano)


func _encuadrar(caja: AABB) -> void:
	var inclinacion := deg_to_rad(55.0) if angulo == "juego" else deg_to_rad(18.0)
	var radio := caja.size.length() * 0.5
	var distancia := radio / tan(deg_to_rad(camara.fov * 0.5)) * 1.15
	var centro := caja.get_center()
	if angulo == "juego":
		centro.z -= 0.55 * centro.y  # la inclinacion del shader echa hacia atras lo que esta alto
	var dir := Vector3(0.0, sin(inclinacion), cos(inclinacion))
	if angulo == "lateral":
		dir = dir.rotated(Vector3.UP, deg_to_rad(35.0))
		Materiales.ajustar_parametro("inclinacion", 0.0)
	camara.look_at_from_position(centro + dir * distancia, centro, Vector3.UP)


func _process(delta: float) -> void:
	if captura != "":
		return
	if Input.is_action_pressed("ui_left"):
		giro -= delta * 1.5
	if Input.is_action_pressed("ui_right"):
		giro += delta * 1.5
	pivote.rotation.y = giro


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("ui_cancel"):
		get_tree().quit()
