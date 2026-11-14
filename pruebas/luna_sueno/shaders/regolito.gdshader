// Regolito lunar: variante del shader facetado para el terreno.
// La malla del terreno va indexada (vertices compartidos, un tercio de la memoria de caras sueltas), asi que
// la normal plana de cada cara (aspecto low-poly) se saca de las derivadas de la posicion.
shader_type spatial;
render_mode world_vertex_coords, specular_disabled;

#include "res://shaders/comun.gdshaderinc"

uniform float grano = 0.07;  // variacion fina del regolito (0 = color plano)

void vertex() {
	pos_mundo = VERTEX;
	inclinar(VERTEX, NORMAL);
}

void fragment() {
	vec3 n = normalize(cross(dFdx(VERTEX), dFdy(VERTEX)));
	if (dot(n, VIEW) < 0.0) {
		n = -n;
	}
	NORMAL = n;
	float g = ruido_valor(pos_mundo.xz * 2.5) * 0.6 + ruido_valor(pos_mundo.xz * 9.0) * 0.4;
	ALBEDO = COLOR.rgb * (1.0 + (g - 0.5) * 2.0 * grano);
	ROUGHNESS = 1.0;
}

void light() {
	// LIGHT_COLOR llega multiplicado por PI: se divide para igualar al Lambert estandar de Godot
	float luz = luz_pintada(dot(NORMAL, LIGHT), ATTENUATION);
	DIFFUSE_LIGHT += LIGHT_COLOR * luz / PI;
	DIFFUSE_LIGHT += LIGHT_COLOR * borde(NORMAL, VIEW, LIGHT) * ATTENUATION / PI;
}
