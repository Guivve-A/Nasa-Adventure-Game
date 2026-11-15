shader_type spatial;
// Brillo sin sombra (como brillo.gdshader) con el mismo vaiven que vaiven.gdshader: las bombillas de la
// guirnalda se mecen con su cable. El peso del vaiven viaja en UV.x.
render_mode unshaded, world_vertex_coords, cull_disabled, shadows_disabled;

uniform float inclinacion = 0.45;
uniform float energia = 2.2;
uniform float viento = 1.0;
uniform float amplitud = 0.045;

varying float semilla;

void vertex() {
	semilla = VERTEX.x * 3.1 + VERTEX.z * 1.7;
	float w = UV.x;
	float fase = dot(VERTEX.xz, vec2(0.9, 0.55));
	vec3 vaiven = vec3(sin(TIME * 1.6 + fase), 0.3 * sin(TIME * 2.1 + fase * 1.3), 0.7 * cos(TIME * 1.25 + fase));
	VERTEX += vaiven * w * amplitud * viento;
	VERTEX.z -= inclinacion * VERTEX.y;
}

void fragment() {
	// un parpadeo muy lento y suave, distinto en cada bombilla (sin destellos rapidos)
	float tibio = 0.92 + 0.08 * sin(TIME * 0.9 + semilla);
	ALBEDO = COLOR.rgb * energia * tibio;
}
