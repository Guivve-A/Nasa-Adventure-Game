extends Node

# Tomas de video para el demo de la presentacion (no es una prueba del juego).
# Se graba con el modo de pelicula de Godot desde herramientas/demo/capturar.py:
#   python -I herramientas/juego_ejecutar.py --pelicula=<x.avi> ... -- --prueba=guion:res://pruebas/demo_captura.gd --toma=<id>
# Juega con teclas simuladas (las mismas funciones de pruebas.gd), a velocidad real.
# Marcas en la salida: "PRUEBA_OK demo.inicio cuadro=<n>" cuando empieza la accion y "PRUEBA_OK demo.fin cuadro=<n>"
# al terminar; capturar.py recorta el video entre las dos.
# Opciones tras "--": --toma=<id>  --segundos=<s> (por defecto los de la toma)  --sin_hud

var p: Node      # el nodo de pruebas.gd: _tecla, _toque, _apuntar, _soltar_todo, _usar_con_teclas, _atender_interfaz

const MINIJUEGOS := ["seguidor", "antena", "satelite", "telescopio", "linea_tiempo", "muestras", "banderas", "regreso", "orbita"]
const FICHAS_CUADERNO := ["luna_12_noviembre", "luz_cenicienta", "terminador", "mare_crisium", "pegaso", "chimborazo",
	"observatorio_quito", "gravedad_lunar", "mar_tranquilidad", "regolito", "estacion_cotopaxi", "realimentacion"]


func correr(pruebas: Node) -> void:
	p = pruebas
	Juego.modo_prueba = false        # dialogos y cargas a ritmo normal, como al jugar
	Juego.sin_guardar = true
	Juego.minijuegos_solos = true    # los minijuegos se juegan solos
	var toma := String(Juego.args.get("toma", ""))
	var seg := float(Juego.args.get("segundos", "0"))
	if toma.begins_with("mj_"):
		await _minijuego(toma.substr(3), seg if seg > 0.0 else 8.0)
		return
	match toma:
		"menu":
			await _menu(seg if seg > 0.0 else 8.0)
		"mapa":
			await _mapa(seg if seg > 0.0 else 8.0)
		"habitacion":
			# vuelta por el suelo despejado: la cama, el telescopio y el banco de trabajo
			await _zona("habitacion", "inicio", [Vector3(-1.1, 0.0, 0.7), Vector3(-1.3, 0.0, -0.5), Vector3(0.4, 0.0, -1.0),
				Vector3(1.5, 0.0, -1.1), Vector3(1.3, 0.0, 0.5), Vector3(-0.2, 0.0, 0.9)], seg if seg > 0.0 else 10.0, {"hud": true})
		"orbita":
			await _orbita(seg if seg > 0.0 else 10.0)
		"ciudad":
			await _zona("ciudad", "inicio", [Vector3(-6.0, 0.0, 2.4), Vector3(-2.0, 0.0, 2.8), Vector3(0.0, 0.0, 4.1),
				Vector3(3.8, 0.0, 2.6), Vector3(3.9, 0.0, -1.4), Vector3(4.6, 0.0, -2.6)], seg if seg > 0.0 else 10.0, {"hud": false})
		"sendero":
			# sube junto al panel y la antena hasta el flamboyan y baja por el otro lado del arroyo
			await _zona("sendero", "inicio", [Vector3(2.2, 0.0, 2.2), Vector3(1.95, 0.0, 0.75), Vector3(2.0, 0.0, -0.65),
				Vector3(0.98, 0.0, -2.11), Vector3(0.1, 0.0, -0.3), Vector3(-0.2, 0.0, 1.5), Vector3(-0.1, 0.0, 2.9)],
				seg if seg > 0.0 else 10.0, {"hud": false})
		"mirador":
			await _zona("mirador", "inicio", [], seg if seg > 0.0 else 10.0, {"hud": false})
		"luna":
			# hacia el este por el llano (el camino de vuelta de la ruta de prueba, al reves): sin la zanja
			await _zona("luna", "inicio", [Vector3(10.0, 0, -1.5), Vector3(24.0, 0, -4.5), Vector3(36.4, 0, -7.0)],
				seg if seg > 0.0 else 10.0, {"hud": false, "saltar": true, "correr": true})
		"luna_apolo":
			# tramo de la ruta de prueba hacia el punto de la foto con la etapa de descenso, con saltos
			await _zona("luna", "inicio", [Vector3(53.0, 0, -16.5), Vector3(59.6, 0, -15.6), Vector3(50.0, 0, -11.0)],
				seg if seg > 0.0 else 10.0, {"hud": false, "saltar": true, "colocar": Vector3(45.5, 0, -21.5)})
		"minimapa":
			# historia en curso: el siguiente paso es recoger el panel del sendero; el minimapa lo senala y se agranda con N
			await _zona("sendero", "inicio", [Vector3(2.2, 0.0, 2.2), Vector3(1.4, 0.0, 1.5), Vector3(2.6, 0.0, 0.9),
				Vector3(2.0, 0.0, -0.65), Vector3(1.0, 0.0, -1.4), Vector3(1.95, 0.0, 0.75)], seg if seg > 0.0 else 9.0,
				{"hud": true, "historia": ["hablo_orbita", "hab_convocatoria", "hab_seguidor", "ciudad_visitada"], "minimapa_grande": 3.0})
		"carga":
			await _carga(seg if seg > 0.0 else 12.0)
		"cuaderno":
			await _cuaderno(seg if seg > 0.0 else 9.0)
		_:
			p.comprobar(false, "demo.toma_desconocida", toma)


# ------------------------------------------------------------------ utilidades

func _marca(nombre: String) -> void:
	print("PRUEBA_OK demo.%s cuadro=%d" % [nombre, Engine.get_frames_drawn()])


func _seg(s: float) -> void:
	# tiempo de juego que no se detiene con la pausa (con --fixed-fps es tiempo del video)
	await get_tree().create_timer(s, true, false, true).timeout


func _pulsar(codigo: int, s: float = 0.12) -> void:
	p._tecla(codigo, true)
	await _seg(s)
	p._tecla(codigo, false)


func _caminar(puntos: Array, correr: bool, saltar: bool) -> void:
	# camina por los puntos con WASD (y Mayus si corre); si se atasca pasa al siguiente punto
	var j: CharacterBody3D = Zonas.jugador
	var zona_inicial := Zonas.id_actual
	var hasta_salto := 0.6
	for destino in puntos:
		var quieto := 0.0
		var ultima := j.global_position
		while true:
			if Zonas.id_actual != zona_inicial:
				p._soltar_todo()
				return      # cruzo un umbral: el cambio de zona ya empezo
			if Zonas.ocupado or Interfaz.ocupada():
				p._soltar_todo()
				await get_tree().physics_frame
				continue
			var d: Vector3 = destino - j.global_position
			d.y = 0.0
			if d.length() < 0.35:
				break
			p._apuntar(d)
			p._tecla(KEY_SHIFT, correr)
			if saltar:
				hasta_salto -= get_physics_process_delta_time()
				if hasta_salto <= 0.0 and j.is_on_floor():
					p._tecla(KEY_SPACE, true)
					await get_tree().physics_frame
					p._tecla(KEY_SPACE, false)
					hasta_salto = 1.4
			await get_tree().physics_frame
			quieto += get_physics_process_delta_time()
			if quieto > 1.2:
				if j.global_position.distance_to(ultima) < 0.15:
					break
				ultima = j.global_position
				quieto = 0.0
	p._soltar_todo()


func _puntos_de_ruta(zona: Node) -> Array:
	# los puntos "ir" de la ruta de prueba de la zona, sin los que pisan un umbral (no debe cambiar de zona)
	var umbrales: Array = []
	for u in get_tree().get_nodes_in_group("umbrales"):
		if zona.is_ancestor_of(u):
			umbrales.append(u)
	var puntos: Array = []
	for paso in zona.ruta_de_prueba():
		if not (paso as Dictionary).has("ir"):
			continue
		var x: Vector3 = paso["ir"]
		var cerca := false
		for u in umbrales:
			if Vector2(u.global_position.x - x.x, u.global_position.z - x.z).length() < float(u.radio) + 0.9:
				cerca = true
		if not cerca:
			puntos.append(x)
	return puntos


func _entrar(id: String, entrada: String, opciones: Dictionary) -> void:
	Juego.nueva_partida()
	var historia: Array = opciones.get("historia", [])
	if historia.is_empty() and not bool(opciones.get("partida_nueva", false)):
		Juego.poner_bandera("visita_libre")
	for b in historia:
		Juego.poner_bandera(b)
	await Zonas.ir_a(id, entrada)
	await p._atender_interfaz(8.0)      # dialogo de llegada, si lo hay
	if not bool(opciones.get("hud", true)) or Juego.args.has("sin_hud"):
		Interfaz.mostrar_hud(false)
	await _seg(0.3)


# ------------------------------------------------------------------ tomas

func _zona(id: String, entrada: String, puntos: Array, segundos: float, opciones: Dictionary) -> void:
	await _entrar(id, entrada, opciones)
	if opciones.has("colocar"):
		var en: Vector3 = opciones["colocar"]
		# altura del suelo en ese punto (el terreno tiene relieve)
		var rayo := PhysicsRayQueryParameters3D.create(Vector3(en.x, 60.0, en.z), Vector3(en.x, -60.0, en.z), 1)
		var choque := Zonas.mundo.get_world_3d().direct_space_state.intersect_ray(rayo)
		if not choque.is_empty():
			en.y = float(choque["position"].y)
		var mira: Vector3 = (puntos[0] - en) if not puntos.is_empty() else Vector3(0, 0, 1)
		Zonas.jugador.colocar(en + Vector3(0.0, 0.3, 0.0), Vector3(mira.x, 0.0, mira.z).normalized())
		Zonas.companero.colocar_junto(Zonas.jugador.global_position, Vector3(mira.x, 0.0, mira.z).normalized())
		await _seg(0.6)
		Zonas.camara.centrar()
		await _seg(0.3)
	if puntos.is_empty():
		puntos = _puntos_de_ruta(Zonas.actual)
	_marca("inicio")
	_caminar(puntos, bool(opciones.get("correr", false)), bool(opciones.get("saltar", false)))
	if opciones.has("minimapa_grande"):
		await _seg(float(opciones["minimapa_grande"]))
		await _pulsar(KEY_N)
		await _seg(segundos - float(opciones["minimapa_grande"]) - 0.12)
	else:
		await _seg(segundos)
	p._soltar_todo()
	_marca("fin")


func _orbita(segundos: float) -> void:
	# hablar con Orbita al empezar la historia (partida nueva): se gira hacia el gato, pulsa E y pasa las lineas con E
	await _entrar("habitacion", "inicio", {"hud": true, "partida_nueva": true})
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	await _seg(0.8)
	await p._usar_con_teclas(Zonas.companero.hablar)
	while Engine.get_frames_drawn() < fin:
		await _seg(2.6)
		if Interfaz.dialogo.visible:
			await _pulsar(KEY_E)
	_marca("fin")


func _carga(segundos: float) -> void:
	# cambio de zona real: de la plaza al sendero caminando por el umbral, con la ventana de carga pintada
	await _entrar("ciudad", "sendero", {"hud": true})
	var destino := Vector3(12.3, 0.0, 1.2)
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	await _seg(0.6)
	_caminar([Vector3(10.6, 0.0, 1.6), destino], false, false)
	var con_dialogo := 0.0
	while Engine.get_frames_drawn() < fin:
		await get_tree().process_frame
		# el saludo de Orbita al llegar se lee y se cierra con E, como al jugar
		con_dialogo = con_dialogo + get_process_delta_time() if Interfaz.dialogo.visible else 0.0
		if con_dialogo > 2.8:
			await _pulsar(KEY_E)
			con_dialogo = 0.0
	p._soltar_todo()
	_marca("fin")


func _cuaderno(segundos: float) -> void:
	await _entrar("habitacion", "inicio", {"hud": true})
	for f in FICHAS_CUADERNO:
		Juego.anotar(f)
	await _seg(0.4)
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	await _seg(0.6)
	await _pulsar(KEY_TAB)
	await _seg(1.6)
	while Engine.get_frames_drawn() < fin:
		await _pulsar(KEY_DOWN)
		await _seg(1.5)
	_marca("fin")


func _menu(segundos: float) -> void:
	Interfaz.abrir_menu()
	await _seg(0.5)
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	var n := 0
	while Engine.get_frames_drawn() < fin:
		await _seg(1.3)
		await _pulsar(KEY_DOWN if n < 4 else KEY_UP)
		n = (n + 1) % 8
	_marca("fin")


func _mapa(segundos: float) -> void:
	Interfaz.abrir_menu()
	Interfaz.abrir_mapa(true)
	await _seg(0.6)
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	var teclas := [KEY_D, KEY_D, KEY_W, KEY_D, KEY_A, KEY_S, KEY_A, KEY_A]
	var n := 0
	while Engine.get_frames_drawn() < fin:
		await _seg(1.1)
		await _pulsar(teclas[n % teclas.size()])
		n += 1
	_marca("fin")


func _minijuego(id: String, segundos: float) -> void:
	if not MINIJUEGOS.has(id):
		p.comprobar(false, "demo.minijuego_desconocido", id)
		return
	var anfitrion: Control = Interfaz.anfitrion
	Interfaz.abrir_minijuego(id, {"dificultad": int(Juego.args.get("dificultad", "2"))})
	var espera := 300
	while espera > 0 and not (anfitrion.get("_minijuego") != null and bool(anfitrion.get("_minijuego").get("activo"))):
		await get_tree().process_frame
		espera -= 1
	await _seg(0.2)
	_marca("inicio")
	var fin := Engine.get_frames_drawn() + int(segundos * 30.0)
	while Engine.get_frames_drawn() < fin:
		var mj: Variant = anfitrion.get("_minijuego")
		if not anfitrion.visible or mj == null or not is_instance_valid(mj) or not bool(mj.get("activo")):
			await _seg(0.4)      # deja ver el final de la partida
			break
		await get_tree().process_frame
	_marca("fin")
