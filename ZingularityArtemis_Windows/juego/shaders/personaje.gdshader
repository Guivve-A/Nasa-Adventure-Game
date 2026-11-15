// Mallas texturizadas (Tripo): textura pintada, luz celular y borde de luz.
// Acabado 2.5D (pintado = 1, uniforme comun): la textura ya trae la luz pintada de la hoja de referencia,
// asi que la luz de la escena solo la tine; la sombra proyectada la oscurece un poco y el borde se conserva.
// Con pintado = 0 vuelve la luz 3D celular por cara (se veia cada triangulo y partia la cara en dos).
shader_type spatial;
render_mode world_vertex_coords, specular_disabled;

#include "res://shaders/comun.gdshaderinc"

uniform sampler2D textura : source_color, filter_linear_mipmap;
uniform bool facetas_planas = true;  // normal de cara a partir de derivadas: se ve cada triangulo
uniform float saturacion = 1.0;
uniform float sombra_pintada : hint_range(0.0, 1.0) = 0.35;  // cuanto oscurece la sombra proyectada en 2.5D

void vertex() {
	pos_mundo = VERTEX;
	inclinar(VERTEX, NORMAL);
}

void fragment() {
	vec3 c = texture(textura, UV).rgb;
	float gris = dot(c, vec3(0.299, 0.587, 0.114));
	ALBEDO = mix(vec3(gris), c, saturacion);
	ROUGHNESS = 1.0;
	if (facetas_planas && pintado < 0.5) {
		NORMAL = normalize(cross(dFdy(VERTEX), dFdx(VERTEX)));
	}
}

void light() {
	float celular = paso_celular(dot(NORMAL, LIGHT)) * ATTENUATION;
	float plano = mix(1.0, ATTENUATION, sombra_pintada);
	DIFFUSE_LIGHT += LIGHT_COLOR * mix(celular, plano, pintado) * luz_moteada(pos_mundo) / PI;
	DIFFUSE_LIGHT += LIGHT_COLOR * borde(NORMAL, VIEW, LIGHT) * ATTENUATION / PI;
}
