shader_type spatial;
// Brillo sin sombra con la inclinacion 2.5D de la escena (D-015). El material «emisivo» del nucleo es un
// StandardMaterial3D que no se inclina: a 1 m de altura queda 0,45 m fuera de su sitio. Este lo acompana.
// El color de vertice (lineal) da el tono: calido (ffc98a) para bombillas y ventanas, cian para la tecnologia.
render_mode unshaded, world_vertex_coords, cull_disabled, shadows_disabled;

uniform float inclinacion = 0.45;
uniform float energia = 1.35;

void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
}

void fragment() {
	ALBEDO = COLOR.rgb * energia;
}
