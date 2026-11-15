extends RefCounted

# Luz por momento del dia (Biblia de arte, seccion 7).
# "tarde" es la luz APROBADA por Guillermo (D-015, vuelta 17 del ajuste al ancla): no se cambia.
# "manana", "noche", "interior_manana", "interior_noche" y "luna" son PROVISIONALES: parten de la tarde y de la
# tabla de la biblia, y esperan la validacion de Guillermo con una captura en el motor.

const MOMENTOS := {
	"tarde": {
		"sol": "ffdcb4", "energia": 1.15, "direccion": Vector3(-0.62, -0.62, 0.48),
		"ambiente": "77849a", "ambiente_energia": 0.62, "fondo": "2b3a33",
		"contraste": 1.12, "saturacion": 0.80, "exposicion": 0.95,
	},
	"manana": {
		"sol": "ffe6c4", "energia": 1.10, "direccion": Vector3(0.55, -0.70, 0.45),
		"ambiente": "8a93a6", "ambiente_energia": 0.66, "fondo": "33423c",
		"contraste": 1.10, "saturacion": 0.82, "exposicion": 0.98,
	},
	"interior_manana": {
		"sol": "ffd9a6", "energia": 1.20, "direccion": Vector3(0.35, -0.62, 0.70),
		"ambiente": "8c8496", "ambiente_energia": 0.74, "fondo": "241f1c",
		"contraste": 1.10, "saturacion": 0.84, "exposicion": 1.0,
	},
	"noche": {
		"sol": "8fa9d8", "energia": 0.40, "direccion": Vector3(-0.45, -0.75, 0.48),
		"ambiente": "33456a", "ambiente_energia": 0.55, "fondo": "0c121b",
		"contraste": 1.10, "saturacion": 0.80, "exposicion": 1.0,
	},
	"interior_noche": {
		"sol": "9db8e0", "energia": 0.40, "direccion": Vector3(0.35, -0.62, 0.70),
		"ambiente": "4a5670", "ambiente_energia": 0.85, "fondo": "12161d",
		"contraste": 1.08, "saturacion": 0.80, "exposicion": 1.0,
	},
	"luna": {
		"sol": "bcd2f0", "energia": 0.85, "direccion": Vector3(-0.30, -0.88, 0.36),
		"ambiente": "34435c", "ambiente_energia": 0.70, "fondo": "07090d",
		"contraste": 1.12, "saturacion": 0.70, "exposicion": 1.0,
	},
}


static func montar(padre: Node3D, momento: String = "tarde", cambios: Dictionary = {}) -> DirectionalLight3D:
	# "cambios" permite a una zona ajustar un valor suelto (por ejemplo {"energia": 1.0})
	var m: Dictionary = MOMENTOS.get(momento, MOMENTOS["tarde"]).duplicate()
	for clave in cambios:
		m[clave] = cambios[clave]
	var sol := DirectionalLight3D.new()
	sol.name = "Sol"
	sol.light_color = Color(String(m["sol"]))
	sol.light_energy = float(m["energia"])
	sol.shadow_enabled = true
	sol.shadow_blur = 1.6
	sol.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sol.directional_shadow_max_distance = float(m.get("sombra_distancia", 40.0))
	padre.add_child(sol)
	var direccion: Vector3 = m["direccion"]
	sol.look_at_from_position(Vector3.ZERO, direccion, Vector3.UP)

	var entorno := WorldEnvironment.new()
	entorno.name = "Entorno"
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(String(m["fondo"]))
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(String(m["ambiente"]))
	e.ambient_light_energy = float(m["ambiente_energia"])
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	e.tonemap_exposure = float(m["exposicion"])
	e.glow_enabled = true
	e.glow_intensity = 0.35
	e.glow_hdr_threshold = 1.2
	e.adjustment_enabled = true
	e.adjustment_contrast = float(m["contraste"])
	e.adjustment_saturation = float(m["saturacion"])
	entorno.environment = e
	padre.add_child(entorno)
	return sol


static func farol(padre: Node3D, posicion: Vector3, color: Color = Color("ffc98a"), energia: float = 1.6, alcance: float = 4.5) -> OmniLight3D:
	# luz practica calida (faroles, lamparas, guirnaldas). Sin sombra: en la HD 620 cada sombra extra cuesta.
	var luz := OmniLight3D.new()
	luz.light_color = color
	luz.light_energy = energia
	luz.omni_range = alcance
	luz.omni_attenuation = 1.4
	luz.shadow_enabled = false
	padre.add_child(luz)
	luz.position = posicion
	return luz
