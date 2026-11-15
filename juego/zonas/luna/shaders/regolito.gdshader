// Regolito lunar (LUN-01): variante del shader facetado aprobado para el terreno de la Luna del sueno.
// La malla del terreno va indexada (vertices compartidos), asi que la normal plana de cada cara (aspecto
// low-poly) se saca de las derivadas de la posicion. Su aspecto es PROVISIONAL (sin concepto validado).
// Como el suelo es casi llano y el acabado 2.5D aplana la luz, el relieve se pinta: cada faceta se aclara
// hacia un gris calido si mira a la luz y se oscurece hacia un violeta azulado si le da la espalda
// (asi se leen los crateres y la zanja, y el suelo deja de ser un azul uniforme). Nunca negro.
shader_type spatial;
render_mode world_vertex_coords, specular_disabled;

#include "res://shaders/comun.gdshaderinc"

uniform float grano = 0.08;          // variacion fina del regolito (0 = color plano)
uniform float relieve = 1.0;         // fuerza del relieve pintado por faceta
uniform vec3 luz_relieve = vec3(-0.72, 0.60, 0.20);   // de donde viene la luz pintada (mundo)
uniform vec3 tinte_luz = vec3(1.24, 1.16, 1.04);      // faceta al sol: gris calido
uniform vec3 tinte_sombra : source_color = vec3(0.52, 0.55, 0.84);   // faceta de espaldas: violeta, nunca negro
uniform float calidez = 0.0;         // 0 = noche; 1 = amanecer (el suelo se entibia)

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
	// normal plana en el mundo, sin la inclinacion 2.5D
	vec3 nm = normalize(cross(dFdx(pos_mundo), dFdy(pos_mundo)));
	if (nm.y < 0.0) {
		nm = -nm;
	}
	float cara = dot(nm, normalize(luz_relieve));
	float llano = normalize(luz_relieve).y;      // lo que recibe un suelo horizontal
	float t = clamp((cara - llano) * 2.6 * relieve, -1.0, 1.0);
	float g = ruido_valor(pos_mundo.xz * 2.5) * 0.6 + ruido_valor(pos_mundo.xz * 9.0) * 0.4;
	vec3 c = COLOR.rgb * (1.0 + (g - 0.5) * 2.0 * grano);
	c = pincelar(c, pos_mundo);
	c *= mix(vec3(1.0), vec3(1.10, 1.0, 0.86), calidez);
	vec3 claro = c * tinte_luz;
	vec3 oscuro = c * tinte_sombra;
	ALBEDO = t > 0.0 ? mix(c, claro, t) : mix(c, oscuro, -t);
	ROUGHNESS = 1.0;
}

void light() {
	// LIGHT_COLOR llega multiplicado por PI: se divide para igualar al Lambert estandar de Godot
	float luz = luz_pintada(dot(NORMAL, LIGHT), ATTENUATION);
	DIFFUSE_LIGHT += LIGHT_COLOR * luz / PI;
	DIFFUSE_LIGHT += LIGHT_COLOR * borde(NORMAL, VIEW, LIGHT) * ATTENUATION / PI;
}
