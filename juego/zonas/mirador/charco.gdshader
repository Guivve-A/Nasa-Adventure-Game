shader_type spatial;
// Charco de luz pintado (v2c): un disco sobre las losas, en mezcla aditiva, que cae suave hacia el borde.
// En el acabado pintado (D-015) el color de las losas manda y una OmniLight apenas las calienta: el charco dorado
// del farol encendido se pinta aqui. UV va de 0 a 1 en el disco; el centro es (0,5; 0,5).
render_mode unshaded, world_vertex_coords, blend_add, cull_disabled, shadows_disabled, depth_draw_never;

uniform float inclinacion = 0.45;
uniform vec3 color : source_color = vec3(0.957, 0.631, 0.349);   // f4a159, sol de la paleta
uniform float fuerza = 1.4;

void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
}

void fragment() {
	float d = length(UV - vec2(0.5)) * 2.0;
	float a = 1.0 - smoothstep(0.0, 1.0, d);
	ALBEDO = color * fuerza * a * (0.35 + 0.65 * a);
}
