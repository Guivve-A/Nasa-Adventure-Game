// Low-poly pintado: color de vertice con degradado por faceta, luz celular calida y borde de luz.
// Con pintado = 1 (acabado 2.5D) las caras de espaldas al sol y las sombras conservan luz calida.
// La sombra fria (azul petroleo) la pone la luz ambiental del entorno.
shader_type spatial;
render_mode world_vertex_coords, specular_disabled;

#include "res://shaders/comun.gdshaderinc"

void vertex() {
	pos_mundo = VERTEX;
	inclinar(VERTEX, NORMAL);
}

void fragment() {
	ALBEDO = pincelar(COLOR.rgb, pos_mundo);
	ROUGHNESS = 1.0;
}

void light() {
	// LIGHT_COLOR llega multiplicado por PI: se divide para igualar al Lambert estandar de Godot
	float luz = luz_pintada(dot(NORMAL, LIGHT), ATTENUATION) * luz_moteada(pos_mundo);
	DIFFUSE_LIGHT += LIGHT_COLOR * luz / PI;
	DIFFUSE_LIGHT += LIGHT_COLOR * borde(NORMAL, VIEW, LIGHT) * ATTENUATION / PI;
}
