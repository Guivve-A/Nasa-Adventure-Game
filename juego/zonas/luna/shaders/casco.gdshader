// Casco de burbuja (LUN-09): cristal casi invisible, con el borde claro y un destello pintado.
// Lleva la inclinacion 2.5D comun para acompanar a la cabeza del personaje.
shader_type spatial;
render_mode world_vertex_coords, unshaded, blend_mix, cull_back, shadows_disabled, depth_draw_never;

uniform float inclinacion = 0.45;
uniform vec4 tinte : source_color = vec4(0.81, 0.97, 0.96, 1.0);
uniform float fondo = 0.07;         // opacidad en el centro
uniform float borde = 0.62;         // opacidad en el contorno

void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
	NORMAL = normalize(vec3(NORMAL.x, NORMAL.y + inclinacion * NORMAL.z, NORMAL.z));
}

void fragment() {
	vec3 n = normalize(NORMAL);
	float fresnel = pow(1.0 - clamp(dot(n, VIEW), 0.0, 1.0), 2.4);
	// destello fijo arriba a la izquierda, como pintado
	float brillo = smoothstep(0.90, 0.95, dot(n, normalize(vec3(-0.42, 0.62, 0.66))));
	float brillo2 = smoothstep(0.975, 0.99, dot(n, normalize(vec3(0.38, -0.30, 0.87)))) * 0.5;
	ALBEDO = tinte.rgb * (0.85 + 0.5 * brillo);
	ALPHA = clamp(fondo + borde * fresnel + 0.55 * brillo + brillo2, 0.0, 0.92);
}
