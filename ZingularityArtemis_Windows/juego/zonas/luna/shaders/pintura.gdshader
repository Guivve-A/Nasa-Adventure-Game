// Pintura sin luz (material «Pintura» de los GLB de la Luna): el color de vertice tal cual, con la
// inclinacion 2.5D comun. Lo usa el reflejo de la Tierra del espejo (LUN-14): un reflejo no recibe la luz
// de la escena, la trae. El color llega en lineal desde el GLB.
shader_type spatial;
render_mode world_vertex_coords, unshaded, shadows_disabled;

uniform float inclinacion = 0.45;
uniform float energia = 1.05;

void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
}

void fragment() {
	ALBEDO = COLOR.rgb * energia;
}
