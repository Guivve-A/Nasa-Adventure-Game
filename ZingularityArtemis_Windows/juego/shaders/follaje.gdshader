// Hojas, hierba y flores: doble cara, color de vertice, viento sutil y luz que envuelve (follaje).
shader_type spatial;
render_mode world_vertex_coords, specular_disabled, cull_disabled;

#include "res://shaders/comun.gdshaderinc"

uniform float viento = 0.035;        // amplitud del balanceo en metros por metro de altura
uniform float velocidad = 1.3;

// sombra moteada y pinceladas calculadas por vertice: las briznas son diminutas y la hierba tiene mucho
// sobredibujado; por pixel, las motas bajaban la escena de 55 a 27 fps en la HD 620
varying float moteado_v;
varying vec3 pincel_v;

void vertex() {
	// el balanceo crece con la altura del vertice y varia con la posicion (rafagas)
	float fase = VERTEX.x * 0.7 + VERTEX.z * 0.5;
	float rafaga = sin(TIME * velocidad + fase) * 0.6 + sin(TIME * velocidad * 2.3 + fase * 1.7) * 0.4;
	float altura = max(VERTEX.y, 0.0);
	VERTEX.x += rafaga * viento * altura;
	VERTEX.z += rafaga * viento * 0.5 * altura;
	pos_mundo = VERTEX;
	moteado_v = luz_moteada(VERTEX);
	pincel_v = pincelar(COLOR.rgb, VERTEX);
	inclinar(VERTEX, NORMAL);
}

void fragment() {
	ALBEDO = pincel_v;
	ROUGHNESS = 1.0;
	// en la cara trasera la normal se invierte para que la hoja no quede negra
	if (!FRONT_FACING) {
		NORMAL = -NORMAL;
	}
}

void light() {
	// luz que envuelve: el follaje deja pasar algo de luz por detras
	float ndl = dot(NORMAL, LIGHT) * 0.75 + 0.25;
	float luz = luz_pintada(ndl, ATTENUATION) * moteado_v;
	DIFFUSE_LIGHT += LIGHT_COLOR * luz / PI;
	DIFFUSE_LIGHT += LIGHT_COLOR * borde(NORMAL, VIEW, LIGHT) * ATTENUATION * 0.6 / PI;
}
