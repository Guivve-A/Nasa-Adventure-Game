extends RefCounted

# Materiales del estilo aprobado (D-015): pone los shaders pintados segun el nombre del material que escribe
# el generador de mallas ("Facetado", "Follaje", "Agua", "Emisivo"). Las mallas con textura (Tripo) reciben el
# shader de personaje con su propia textura. Portado de pruebas/escena_exploracion/materiales.gd.
#
# Los parametros comunes (inclinacion, pintado, pinceladas, moteado_*) se ponen con ajustar_parametro():
# se guardan y se aplican tambien a los materiales que se creen despues.

const FACETADO := preload("res://shaders/facetado.gdshader")
const FOLLAJE := preload("res://shaders/follaje.gdshader")
const AGUA := preload("res://shaders/agua.gdshader")
const PERSONAJE := preload("res://shaders/personaje.gdshader")

const POR_DEFECTO := {
	"inclinacion": 0.45,
	"pintado": 1.0,
	"pinceladas": 0.0,
	"moteado_fuerza": 0.0,
	"moteado_centro": Vector2.ZERO,
	"moteado_radios": Vector2.ONE,
	"moteado_sombra": 0.4,
}

static var creados: Array[ShaderMaterial] = []   # materiales de la zona actual
static var fijos: Array[ShaderMaterial] = []     # materiales que pasan de zona en zona (jugadora, gato)
static var parametros: Dictionary = POR_DEFECTO.duplicate()
static var _compartidos: Dictionary = {}


static func _registrar(m: ShaderMaterial, fijo: bool) -> void:
	for nombre in parametros:
		m.set_shader_parameter(nombre, parametros[nombre])
	if fijo:
		fijos.append(m)
	else:
		creados.append(m)


static func material_para(original: Material, fijo: bool = false) -> Material:
	var nombre := original.resource_name if original else ""
	if nombre.begins_with("Emisivo"):
		return emisivo(Color("62e4e0"), 2.5)
	var nuevo := ShaderMaterial.new()
	if nombre.begins_with("Follaje"):
		nuevo.shader = FOLLAJE
	elif nombre.begins_with("Agua"):
		nuevo.shader = AGUA
		nuevo.render_priority = 1
	elif original is BaseMaterial3D and (original as BaseMaterial3D).albedo_texture != null:
		nuevo.shader = PERSONAJE
		nuevo.set_shader_parameter("textura", (original as BaseMaterial3D).albedo_texture)
	else:
		nuevo.shader = FACETADO
	_registrar(nuevo, fijo)
	return nuevo


static func aplicar(raiz: Node, fijo: bool = false, contar: bool = false) -> Dictionary:
	# cambia los materiales de todas las mallas bajo "raiz"; con contar = true devuelve los triangulos
	var tris := 0
	var superficies := 0
	for nodo in raiz.find_children("*", "MeshInstance3D", true, false):
		var mi := nodo as MeshInstance3D
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			mi.set_surface_override_material(s, material_para(mi.mesh.surface_get_material(s), fijo))
			if contar:
				var arrays := mi.mesh.surface_get_arrays(s)
				var indices: Variant = arrays[Mesh.ARRAY_INDEX]
				tris += (indices.size() if indices != null else arrays[Mesh.ARRAY_VERTEX].size()) / 3
			superficies += 1
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	return {"triangulos": tris, "superficies": superficies}


static func compartido(tipo: String) -> ShaderMaterial:
	# un material por tipo y por zona, para las piezas hechas por codigo (nucleo/piezas.gd):
	# "facetado", "follaje" o "agua"
	if _compartidos.has(tipo):
		return _compartidos[tipo]
	var m := ShaderMaterial.new()
	match tipo:
		"follaje":
			m.shader = FOLLAJE
		"agua":
			m.shader = AGUA
			m.render_priority = 1
		_:
			m.shader = FACETADO
	_registrar(m, false)
	_compartidos[tipo] = m
	return m


static func emisivo(color: Color, energia: float = 2.5) -> StandardMaterial3D:
	# brillo sin sombra: el cian de la tecnologia y la interaccion
	var brillo := StandardMaterial3D.new()
	brillo.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	brillo.albedo_color = color
	brillo.vertex_color_use_as_albedo = true
	brillo.emission_enabled = true
	brillo.emission = color
	brillo.emission_energy_multiplier = energia
	return brillo


static func ajustar_parametro(nombre: String, valor: Variant) -> void:
	parametros[nombre] = valor
	for m in creados:
		m.set_shader_parameter(nombre, valor)
	for m in fijos:
		m.set_shader_parameter(nombre, valor)


static func limpiar_zona() -> void:
	# al cambiar de zona: se sueltan sus materiales y los parametros vuelven a los valores por defecto
	creados.clear()
	_compartidos.clear()
	for nombre in POR_DEFECTO:
		ajustar_parametro(nombre, POR_DEFECTO[nombre])


static func caja_mundo(raiz: Node3D) -> AABB:
	var caja := AABB()
	var primera := true
	for nodo in raiz.find_children("*", "MeshInstance3D", true, false):
		var mi := nodo as MeshInstance3D
		if mi.mesh == null:
			continue
		var c := mi.global_transform * mi.mesh.get_aabb()
		caja = c if primera else caja.merge(c)
		primera = false
	if raiz is MeshInstance3D and (raiz as MeshInstance3D).mesh != null:
		var propia := (raiz as MeshInstance3D).global_transform * (raiz as MeshInstance3D).mesh.get_aabb()
		caja = propia if primera else caja.merge(propia)
	return caja
