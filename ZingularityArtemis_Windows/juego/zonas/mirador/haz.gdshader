shader_type spatial;
// Haz del faro (v2): cuna de luz aditiva y tenue que gira desde la linterna. UV.x = distancia relativa
// desde la linterna (0 a 1) y UV.y = posicion a lo ancho (-1 a 1). La inclinacion 2.5D se aplica a mano.
render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled;

uniform float inclinacion = 0.45;
uniform vec3 color : source_color = vec3(1.0, 0.86, 0.62);
uniform float intensidad = 0.035;

void vertex() {
	vec3 mundo = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	mundo.z -= inclinacion * mundo.y;
	POSITION = PROJECTION_MATRIX * VIEW_MATRIX * vec4(mundo, 1.0);
}

void fragment() {
	float largo = pow(1.0 - clamp(UV.x, 0.0, 1.0), 1.6);
	float ancho = 1.0 - smoothstep(0.35, 1.0, abs(UV.y));
	ALBEDO = color * intensidad * largo * ancho;
}
