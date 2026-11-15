// Vineta suave del sueno: las esquinas se van a un azul violeta que respira despacio. Nunca negro.
// v2d: el borde de abajo (el primer plano) se hunde un poco mas en el azul, como en carga_luna.jpg.
shader_type canvas_item;

uniform vec4 tinte : source_color = vec4(0.20, 0.20, 0.40, 1.0);
uniform float fuerza = 0.40;
uniform float primer_plano = 0.16;  // oscurece el tercio de abajo
uniform float calidez = 0.0;        // 0 = noche; 1 = amanecer (las esquinas se entibian)

void fragment() {
	vec2 d = UV - vec2(0.5);
	d.x *= 1.3;
	float v = smoothstep(0.34, 0.86, length(d));
	v = max(v, smoothstep(0.62, 1.0, UV.y) * primer_plano / max(fuerza, 0.01));
	float respira = 1.0 + 0.07 * sin(TIME * 0.45);
	vec3 c = mix(tinte.rgb, vec3(0.57, 0.29, 0.19), calidez * 0.6);
	COLOR = vec4(c, clamp(v * fuerza * respira, 0.0, 0.8));
}
