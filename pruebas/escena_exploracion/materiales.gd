class_name Materiales
extends RefCounted

# Carga mallas .glb en tiempo de ejecucion y les pone los shaders de la escena segun el nombre del
# material que escribe el generador ("Facetado", "Follaje", "Agua", "Emisivo"). Las mallas con textura
# (Tripo) reciben el shader de personaje con su propia textura.

const FACETADO := preload("res://shaders/facetado.gdshader")
const FOLLAJE := preload("res://shaders/follaje.gdshader")
const AGUA := preload("res://shaders/agua.gdshader")
const PERSONAJE := preload("res://shaders/personaje.gdshader")

static var creados: Array[ShaderMaterial] = []


static func cargar_glb(ruta: String) -> Node3D:
	var doc := GLTFDocument.new()
	var estado := GLTFState.new()
	var error := doc.append_from_file(ruta, estado)
	if error != OK:
		push_error("No se pudo leer %s (error %d)" % [ruta, error])
		return null
	return doc.generate_scene(estado) as Node3D


static func material_para(original: Material) -> Material:
	var nombre := original.resource_name if original else ""
	if nombre.begins_with("Emisivo"):
		var brillo := StandardMaterial3D.new()
		brillo.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		brillo.vertex_color_use_as_albedo = true
		brillo.emission_enabled = true
		brillo.emission = Color("62e4e0")
		brillo.emission_energy_multiplier = 2.5
		return brillo
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
	creados.append(nuevo)
	return nuevo


static func aplicar(raiz: Node) -> Dictionary:
	# devuelve cuantos triangulos y superficies tiene el recurso
	var tris := 0
	var superficies := 0
	for nodo in raiz.find_children("*", "MeshInstance3D", true, false):
		var mi := nodo as MeshInstance3D
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			mi.set_surface_override_material(s, material_para(mi.mesh.surface_get_material(s)))
			var arrays := mi.mesh.surface_get_arrays(s)
			var indices = arrays[Mesh.ARRAY_INDEX]
			tris += (indices.size() if indices != null else arrays[Mesh.ARRAY_VERTEX].size()) / 3
			superficies += 1
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
	return {"triangulos": tris, "superficies": superficies}


static func ajustar_parametro(nombre: String, valor) -> void:
	for m in creados:
		m.set_shader_parameter(nombre, valor)


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
	return caja
