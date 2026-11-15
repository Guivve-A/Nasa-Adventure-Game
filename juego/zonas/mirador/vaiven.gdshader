// Facetado pintado con vaiven de viento: cables de la guirnalda y banderines del Mirador (v2).
// Es el shader aprobado (shaders/facetado.gdshader, D-015) mas un desplazamiento por viento.
// El peso del vaiven viaja en UV.x: 0 en los amarres (no se mueven) y 1 en el centro del tramo.
shader_type spatial;
render_mode world_vertex_coords, specular_disabled, cull_disabled;

#include "res://shaders/comun.gdshaderinc"

uniform float viento = 1.0;       // lo sube la zona en las rachas
uniform float amplitud = 0.045;   // metros en el centro de un tramo con viento 1

void vertex() {
	float w = UV.x;
	float fase = dot(VERTEX.xz, vec2(0.9, 0.55));
	vec3 vaiven = vec3(sin(TIME * 1.6 + fase), 0.3 * sin(TIME * 2.1 + fase * 1.3), 0.7 * cos(TIME * 1.25 + fase));
	VERTEX += vaiven * w * amplitud * viento;
	pos_mundo = VERTEX;
	inclinar(VERTEX, NORMAL);
}

void fragment() {
	// los banderines son tela de dos caras: la cara de atras usa la normal opuesta
	if (!FRONT_FACING) {
		NORMAL = -NORMAL;
	}
	ALBEDO = pincelar(COLOR.rgb, pos_mundo);
	ROUGHNESS = 1.0;
}

void light() {
	float luz = luz_pintada(dot(NORMAL, LIGHT), ATTENUATION);
	DIFFUSE_LIGHT += LIGHT_COLOR * luz / PI;
	DIFFUSE_LIGHT += LIGHT_COLOR * borde(NORMAL, VIEW, LIGHT) * ATTENUATION / PI;
}
