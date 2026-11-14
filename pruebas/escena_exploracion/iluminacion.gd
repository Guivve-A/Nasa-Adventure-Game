class_name Iluminacion
extends RefCounted

# Luz de la tarde (Biblia de arte, seccion 7): sol calido y bajo que llega desde el fondo a la derecha
# (contraluz, como en la vista aprobada), sombras azul petroleo y un poco de brillo para el cian.

static func montar(padre: Node3D) -> DirectionalLight3D:
	var sol := DirectionalLight3D.new()
	sol.name = "Sol"
	sol.light_color = Color("ffdcb4")  # iteracion 4: un punto mas dorado que el original (ffe1bf); ffd2a0 saturaba
	sol.light_energy = 1.15
	sol.shadow_enabled = true
	sol.shadow_blur = 1.6
	sol.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sol.directional_shadow_max_distance = 40.0
	padre.add_child(sol)
	# el sol viaja desde el fondo derecho hacia el frente izquierdo, a unos 38 grados de altura
	sol.look_at_from_position(Vector3.ZERO, Vector3(-0.62, -0.62, 0.48), Vector3.UP)

	var entorno := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color("2b3a33")
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	# iteracion 4: entre el azul petroleo original (6f8fa3) y el malva calido del ancla; 7f7a86 a 0,7 aclaraba de mas
	e.ambient_light_color = Color("77849a")
	e.ambient_light_energy = 0.62
	e.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	e.tonemap_exposure = 0.95
	e.glow_enabled = true
	e.glow_intensity = 0.35
	e.glow_hdr_threshold = 1.2
	e.adjustment_enabled = true
	# iteracion 10 del ajuste al ancla: la escena quedaba con menos contraste (15,4 contra 17,5) y mas croma
	# (38,8 contra 34,2) que el ancla
	e.adjustment_contrast = 1.12
	e.adjustment_saturation = 0.80  # iteracion 17: 0,92 -> croma 38,9; 0,86 -> 36,6 (ancla 34,2)
	entorno.environment = e
	padre.add_child(entorno)
	return sol
