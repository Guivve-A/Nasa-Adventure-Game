// Marca de umbral (entrada y salida de cada escena): anillo y estrella de cuatro puntas en cian sobre el suelo,
// como en el concepto aprobado de la Habitacion (L05 A). Sin sombra, con pulso suave. Sigue la inclinacion
// comun para quedar pegada al suelo en cualquier altura.
shader_type spatial;
render_mode world_vertex_coords, unshaded, blend_mix, cull_disabled, depth_draw_never, shadows_disabled;

uniform float inclinacion = 0.45;
uniform vec3 color : source_color = vec3(0.384, 0.894, 0.878);   // #62E4E0
uniform float fuerza = 1.0;        // 0 = cerrado (apagado), 1 = abierto
uniform float cerrado = 0.0;       // 1 = umbral aun no disponible: se ve tenue y sin estrella

void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
}

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float r = length(p);
	float pulso = 0.5 + 0.5 * sin(TIME * 2.2);
	float anillo = smoothstep(0.08, 0.0, abs(r - (0.74 + 0.04 * pulso)));
	float halo = smoothstep(1.0, 0.2, r) * 0.14;
	// estrella de cuatro puntas: |x|^k + |y|^k < c con k < 1
	float estrella_d = pow(abs(p.x), 0.55) + pow(abs(p.y), 0.55);
	float estrella = smoothstep(0.78, 0.60, estrella_d) * (0.75 + 0.25 * pulso);
	float brillo = anillo * 0.9 + halo + estrella * (1.0 - cerrado);
	brillo *= mix(1.0, 0.35, cerrado) * fuerza;
	ALBEDO = color * (1.0 + 0.5 * estrella);
	ALPHA = clamp(brillo * 0.9, 0.0, 0.8);
}
