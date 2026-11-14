// Arroyo: turquesa con bandas de corriente, destellos y espuma donde el color de vertice lo marca (alfa).
shader_type spatial;
render_mode world_vertex_coords, specular_disabled, cull_disabled;

#include "res://shaders/comun.gdshaderinc"

// iteracion 3: el agua del ancla es oscura y poco saturada (#504e40 a #3e322d); los destellos la aclaran
uniform vec3 agua_honda : source_color = vec3(0.10, 0.30, 0.30);   // turquesa hondo (iteracion 9)
uniform vec3 agua_clara : source_color = vec3(0.22, 0.52, 0.47);   // verde agua del ancla
uniform vec3 espuma : source_color = vec3(0.81, 0.97, 0.96);       // #CEF8F5 brillo
uniform vec3 reflejo : source_color = vec3(1.0, 0.86, 0.58);       // destellos dorados del sol de la tarde (ancla)
uniform vec2 corriente = vec2(0.25, 0.6);                            // direccion y rapidez del flujo

void vertex() {
	pos_mundo = VERTEX;
	inclinar(VERTEX, NORMAL);
}

float ondas(vec2 p) {
	return sin(p.x * 3.1 + sin(p.y * 1.7)) * 0.5 + sin(p.y * 4.3 - p.x * 1.3) * 0.5;
}

void fragment() {
	vec2 p = pos_mundo.xz * 1.6 - corriente * TIME;
	float o = ondas(p) * 0.5 + 0.5;
	vec3 c = mix(agua_honda, agua_clara, smoothstep(0.35, 0.85, o));
	float destello = smoothstep(0.93, 0.99, ondas(p * 1.9 + 3.0) * 0.5 + 0.5);
	// mascara del generador: 0,35 = agua corriente, 0,75 = espuma al pie de una cascada, 1 = cascada.
	// Iteracion 9: antes se mezclaba tal cual y el 0,35 dejaba toda el agua lechosa.
	float espuma_m = smoothstep(0.5, 1.0, COLOR.r);
	// chorros: rayas que bajan por la cascada
	float chorro = 0.82 + 0.18 * sin(pos_mundo.x * 37.0 + pos_mundo.z * 29.0) * sin(pos_mundo.y * 25.0 + TIME * 9.0);
	c = mix(c, reflejo, destello * 0.85 * (1.0 - espuma_m));
	c = mix(c, espuma * chorro, espuma_m);
	ALBEDO = c;
	ROUGHNESS = 0.4;
	ALPHA = mix(0.93, 1.0, espuma_m);
}

void light() {
	float paso = paso_celular(dot(NORMAL, LIGHT)) * ATTENUATION;
	DIFFUSE_LIGHT += LIGHT_COLOR * (0.45 + 0.35 * paso) / PI;
}
