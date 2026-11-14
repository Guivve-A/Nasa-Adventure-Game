// La Tierra en el cielo lunar: esfera simple con oceanos, continentes y nubes de ruido (inventados, no son
// la geografia real; para el juego final se usaria una textura de NASA). La ilumina solo el sol de la escena,
// asi que la fase sale sola de la geometria Sol-Luna-Tierra.
shader_type spatial;
render_mode ambient_light_disabled, specular_disabled, shadows_disabled;

varying vec3 p_obj;

void vertex() {
	p_obj = VERTEX;
}

float azar3(vec3 p) {
	return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);
}

float ruido3(vec3 p) {
	vec3 i = floor(p);
	vec3 f = fract(p);
	vec3 u = f * f * (3.0 - 2.0 * f);
	float a = mix(mix(azar3(i), azar3(i + vec3(1, 0, 0)), u.x), mix(azar3(i + vec3(0, 1, 0)), azar3(i + vec3(1, 1, 0)), u.x), u.y);
	float b = mix(mix(azar3(i + vec3(0, 0, 1)), azar3(i + vec3(1, 0, 1)), u.x), mix(azar3(i + vec3(0, 1, 1)), azar3(i + vec3(1, 1, 1)), u.x), u.y);
	return mix(a, b, u.z);
}

void fragment() {
	vec3 d = normalize(p_obj);
	float c = ruido3(d * 2.2) * 0.6 + ruido3(d * 5.0) * 0.4;
	float n = ruido3(d * 4.0 + vec3(7.0)) * 0.7 + ruido3(d * 11.0) * 0.3;
	vec3 oceano = vec3(0.05, 0.15, 0.42);
	vec3 suelo = mix(vec3(0.30, 0.38, 0.19), vec3(0.62, 0.52, 0.35), ruido3(d * 8.0));
	vec3 col = mix(oceano, suelo, smoothstep(0.53, 0.57, c));
	col = mix(col, vec3(0.95), smoothstep(0.84, 0.9, abs(d.y)));
	col = mix(col, vec3(0.96), smoothstep(0.56, 0.74, n) * 0.85);
	ALBEDO = col;
	ROUGHNESS = 1.0;
}

void light() {
	DIFFUSE_LIGHT += LIGHT_COLOR * clamp(dot(NORMAL, LIGHT), 0.0, 1.0) / PI;
}
