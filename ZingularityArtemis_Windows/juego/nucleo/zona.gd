extends Node3D

# Base de toda zona del mundo. Cada zona vive en res://zonas/<id>/<id>.gd y empieza con
#   extends "res://nucleo/zona.gd"
# y tiene al lado su zona.json (nombre, lugar, momento, ventana de carga y estado del arte).
#
# La zona se arma por codigo en _construir(): geometria, luz, colisiones, entradas, umbrales e
# interactuables. El gestor (autoload Zonas) coloca despues a la protagonista en la entrada pedida
# y llama a al_entrar() cuando la ventana de carga ya se quito.
#
# Reglas:
# - La camara mira hacia -Z desde lo alto: -Z es «arriba» en pantalla y +X es la derecha.
# - Toda entrada y salida lleva un tramo despejado de unos 2 x 2 m (regla de Guillermo).
# - Las escaleras llevan una rampa de colision: la protagonista no sube escalones sueltos.
# - El cian (#62E4E0) se reserva para tecnologia e interaccion.

const Materiales := preload("res://nucleo/materiales.gd")
const Recursos := preload("res://nucleo/recursos.gd")
const Piezas := preload("res://nucleo/piezas.gd")
const Iluminacion := preload("res://nucleo/iluminacion.gd")
const Constructor := preload("res://nucleo/constructor.gd")
const Umbral := preload("res://nucleo/umbral.gd")
const Interactuable := preload("res://nucleo/interactuable.gd")

var id := ""
var meta: Dictionary = {}          # contenido de zona.json
var carpeta := ""                  # res://zonas/<id>
var entradas: Dictionary = {}      # nombre -> {"pos": Vector3, "mira": Vector3}

# Ajustes que cada zona puede cambiar en _construir()
var gravedad := 9.8                # m/s2 (Luna: 1.624)
var salto := 0.0                   # velocidad inicial del salto en m/s (0 = no se salta)
var factor_velocidad := 1.0        # multiplica la velocidad de la protagonista
var inercia := 1.0                 # 1 = Tierra; menor = acelera y frena mas despacio (Luna: 0.35)
var encuadre := 0.18               # fraccion del alto de pantalla que ocupa la protagonista (0.125 a 0.21)
var limites := Rect2()             # limites del foco de la camara en XZ (vacio = sin limite)
var cizalla := 0.45                # inclinacion 2.5D de los objetos (D-015)
var con_companero := true          # Orbita acompana en esta zona


func _ready() -> void:
	_construir()


# ------------------------------------------------------------------ para sobrescribir

func _construir() -> void:
	pass


func al_entrar(_entrada: String) -> void:
	# se llama cuando la ventana de carga ya se quito (puede ser una corrutina con dialogos)
	pass


func al_salir() -> void:
	pass


func orbita_dice() -> Array:
	# lineas propias de la zona cuando se habla con Orbita; vacio = la pista del objetivo actual
	return []


func ruta_de_prueba() -> Array:
	# recorrido automatico para las pruebas: lista de pasos
	#   {"ir": Vector3}                  camina hasta ese punto
	#   {"usar": "nombre_del_nodo"}      usa un interactuable de la zona
	#   {"esperar": segundos}
	#   {"bandera": "nombre"}            comprueba que esa bandera ya este puesta
	return []


# ------------------------------------------------------------------ entradas, umbrales e interactuables

func entrada(nombre: String, pos: Vector3, mira: Vector3 = Vector3(0, 0, 1)) -> void:
	# punto donde aparece la protagonista; "mira" es hacia donde queda mirando (0,0,1 = hacia la camara)
	entradas[nombre] = {"pos": pos, "mira": mira}


func umbral(nombre: String, pos: Vector3, destino_zona: String, destino_entrada: String = "inicio", etiqueta: String = "", opciones: Dictionary = {}) -> Node3D:
	# opciones: radio, requiere (bandera), mensaje_cerrado, con_tecla, al_cruzar (Callable)
	var u := Umbral.new()
	u.name = nombre
	u.destino_zona = destino_zona
	u.destino_entrada = destino_entrada
	u.etiqueta = etiqueta
	for clave in opciones:
		u.set(clave, opciones[clave])
	add_child(u)
	u.position = pos
	return u


func interactuable(nombre: String, pos: Vector3, texto: String, al_usar: Callable, opciones: Dictionary = {}) -> Node3D:
	# opciones: radio, altura_marca, una_vez, habilitado
	var i := Interactuable.new()
	i.name = nombre
	i.texto = texto
	i.al_usar = al_usar
	for clave in opciones:
		i.set(clave, opciones[clave])
	add_child(i)
	i.position = pos
	return i


# ------------------------------------------------------------------ luz y ambiente

func luces(momento: String = "tarde", cambios: Dictionary = {}) -> DirectionalLight3D:
	return Iluminacion.montar(self, momento, cambios)


func farol(pos: Vector3, color: Color = Color("ffc98a"), energia: float = 1.6, alcance: float = 4.5) -> OmniLight3D:
	return Iluminacion.farol(self, pos, color, energia, alcance)


func ambiente(pinceladas: float = 0.7, moteado: Dictionary = {}) -> void:
	# textura pintada 2D-HD (0.7 en el sendero aprobado) y, si se pide, sombra moteada de un arbol:
	# {"centro": [x, z], "radios": [rx, rz], "fuerza": 1.0, "sombra": 0.45}
	var datos := {"ambiente": {"pinceladas": pinceladas}}
	if not moteado.is_empty():
		datos["ambiente"]["moteado"] = moteado
	Constructor.aplicar_ambiente(datos)


# ------------------------------------------------------------------ geometria

func pieza(m: Dictionary, material: String = "facetado", pos: Vector3 = Vector3.ZERO, giro_grados: float = 0.0, sombra: bool = true) -> MeshInstance3D:
	# agrega a la zona una malla hecha con Piezas (ver nucleo/piezas.gd)
	var nodo := Piezas.nodo(m, material, sombra)
	add_child(nodo)
	nodo.position = pos
	nodo.rotation.y = deg_to_rad(giro_grados)
	return nodo


func modelo(ruta: String, pos: Vector3, giro_grados: float = 0.0, opciones: Dictionary = {}) -> Node3D:
	# coloca un GLB (ruta res://...). opciones: altura (normaliza el alto en metros), escala, animacion
	var nodo := Recursos.instancia(ruta)
	if nodo == null:
		push_warning("AVISO falta el modelo %s" % ruta)
		return null
	add_child(nodo)
	if opciones.has("altura"):
		nodo = Constructor.normalizar_altura(self, nodo, float(opciones["altura"]))
	nodo.scale *= float(opciones.get("escala", 1.0))
	nodo.rotation.y = deg_to_rad(giro_grados)
	nodo.position = pos
	if opciones.has("animacion"):
		Constructor.reproducir(nodo, opciones["animacion"])
	return nodo


func montar_layout(ruta_json: String, base: String = "", omitir: Array = []) -> Dictionary:
	# arma un layout como el del sendero aprobado; devuelve {"instancias", "faltan", "recursos"}
	var datos: Variant = JSON.parse_string(FileAccess.get_file_as_string(ruta_json))
	if not (datos is Dictionary):
		push_warning("AVISO layout ilegible: %s" % ruta_json)
		return {"instancias": {}, "faltan": [], "recursos": 0}
	Constructor.aplicar_ambiente(datos)
	var carpeta_base := base if base != "" else ruta_json.get_base_dir()
	var r := Constructor.montar(self, datos, carpeta_base, omitir)
	if not r["faltan"].is_empty():
		push_warning("AVISO faltan modelos del layout: %s" % str(r["faltan"]))
	return r


# ------------------------------------------------------------------ colisiones (capa 1 = mundo)

func _cuerpo(forma: Shape3D, pos: Vector3, giro_grados: float = 0.0) -> StaticBody3D:
	var cuerpo := StaticBody3D.new()
	cuerpo.collision_layer = 1
	cuerpo.collision_mask = 0
	var cs := CollisionShape3D.new()
	cs.shape = forma
	cuerpo.add_child(cs)
	add_child(cuerpo)
	cuerpo.position = pos
	cuerpo.rotation.y = deg_to_rad(giro_grados)
	return cuerpo


func pared(centro: Vector3, tam: Vector3, giro_grados: float = 0.0) -> StaticBody3D:
	# caja de colision invisible (paredes, muebles, bordes)
	var forma := BoxShape3D.new()
	forma.size = tam
	return _cuerpo(forma, centro, giro_grados)


func piso(centro: Vector3, tam: Vector2, grosor: float = 0.5) -> StaticBody3D:
	# suelo plano: la cara de arriba queda en centro.y
	var forma := BoxShape3D.new()
	forma.size = Vector3(tam.x, grosor, tam.y)
	return _cuerpo(forma, centro - Vector3(0.0, grosor * 0.5, 0.0))


func columna(base: Vector3, radio: float, alto: float = 2.0) -> StaticBody3D:
	# cilindro de colision (troncos, postes, rocas redondas)
	var forma := CylinderShape3D.new()
	forma.radius = radio
	forma.height = alto
	return _cuerpo(forma, base + Vector3(0.0, alto * 0.5, 0.0))


func rampa(desde: Vector3, hasta: Vector3, ancho: float, grosor: float = 0.3) -> StaticBody3D:
	# plano inclinado entre dos puntos (centro de cada extremo): para escaleras y cuestas
	var eje := hasta - desde
	var largo := eje.length()
	var forma := BoxShape3D.new()
	forma.size = Vector3(ancho, grosor, largo)
	var cuerpo := _cuerpo(forma, (desde + hasta) * 0.5)
	var adelante := eje.normalized()
	var lado := Vector3.UP.cross(adelante).normalized()
	var arriba := adelante.cross(lado).normalized()
	cuerpo.basis = Basis(lado, arriba, adelante)
	cuerpo.position -= arriba * grosor * 0.5
	return cuerpo


func colision_de_malla(nodo: Node) -> int:
	# colision exacta (triangulos) para todas las mallas bajo un nodo: suelos con relieve, puentes, muros.
	# Devuelve cuantas mallas recibieron colision. No usar en hierba ni follaje.
	var n := 0
	var lista: Array = nodo.find_children("*", "MeshInstance3D", true, false)
	if nodo is MeshInstance3D:
		lista.append(nodo)
	for hijo in lista:
		var mi := hijo as MeshInstance3D
		if mi.mesh == null or mi.is_queued_for_deletion():
			continue
		var forma := mi.mesh.create_trimesh_shape()
		if forma == null:
			continue
		var cuerpo := StaticBody3D.new()
		cuerpo.collision_layer = 1
		cuerpo.collision_mask = 0
		var cs := CollisionShape3D.new()
		cs.shape = forma
		cuerpo.add_child(cs)
		add_child(cuerpo)
		cuerpo.global_transform = mi.global_transform
		n += 1
	return n


func cerco(rect: Rect2, alto: float = 3.0, y: float = 0.0, grosor: float = 0.6) -> void:
	# cuatro paredes invisibles alrededor de un rectangulo en XZ: nadie se sale del mapa
	var c := rect.get_center()
	var t := rect.size
	pared(Vector3(c.x, y + alto * 0.5, rect.position.y - grosor * 0.5), Vector3(t.x + grosor * 2.0, alto, grosor))
	pared(Vector3(c.x, y + alto * 0.5, rect.end.y + grosor * 0.5), Vector3(t.x + grosor * 2.0, alto, grosor))
	pared(Vector3(rect.position.x - grosor * 0.5, y + alto * 0.5, c.y), Vector3(grosor, alto, t.y))
	pared(Vector3(rect.end.x + grosor * 0.5, y + alto * 0.5, c.y), Vector3(grosor, alto, t.y))


# ------------------------------------------------------------------ varios

func altura_suelo(x: float, z: float, desde: float = 20.0) -> float:
	# altura del suelo de colision en un punto (rayo hacia abajo); NAN si no hay suelo
	var espacio := get_world_3d().direct_space_state
	var consulta := PhysicsRayQueryParameters3D.create(Vector3(x, desde, z), Vector3(x, desde - 60.0, z), 1)
	var golpe := espacio.intersect_ray(consulta)
	if golpe.is_empty():
		return NAN
	return golpe["position"].y


func recolectable(nombre: String, pos: Vector3, id_objeto: String, nodo_visual: Node3D = null, texto: String = "Recoger") -> Node3D:
	# objeto que se recoge una sola vez por partida: suma al inventario y pone la bandera "tomo_<zona>_<nombre>"
	var marca := "tomo_%s_%s" % [id, nombre]
	if Juego.bandera(marca):
		if nodo_visual != null:
			nodo_visual.queue_free()
		return null
	var inter: Node3D = null
	var accion := func() -> void:
		Juego.poner_bandera(marca)
		var total := Juego.sumar(id_objeto)
		Audio.sonar("recoger")
		Interfaz.aviso("+1 %s (%d)" % [id_objeto.replace("_", " "), total], 2.0)
		if nodo_visual != null and is_instance_valid(nodo_visual):
			nodo_visual.queue_free()
		var yo := get_node_or_null(nombre)
		if yo != null:
			yo.queue_free()
	inter = interactuable(nombre, pos, texto, accion, {"radio": 1.1, "altura_marca": 0.7, "una_vez": true})
	return inter
