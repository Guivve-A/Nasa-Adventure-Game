// Comun a los shaders de la escena: inclinacion hacia atras, luz celular calida con borde de luz,
// acabado 2.5D pintado y sombra moteada del arbol.
// La camara de juego mira hacia -Z desde lo alto. Echar los objetos hacia atras (-Z) en proporcion a su
// altura hace que se lean erguidos, como en las ilustraciones aprobadas, sin tocar el suelo (y = 0).

uniform float inclinacion = 0.55;   // tan del angulo de inclinacion; 0 = sin inclinar
uniform float borde_luz = 0.45;     // intensidad del borde de luz (rim)
uniform float suavidad = 0.10;      // ancho de la transicion luz/sombra

// Acabado 2.5D (pedido de Guillermo, 2026-11-12: «texturas de 2D-HD o 2.5D»): la luz pintada del ancla
// no deja negras las caras de espaldas al sol ni las sombras; el color pintado manda.
uniform float pintado : hint_range(0.0, 1.0) = 1.0;   // 0 = luz celular por cara; 1 = acabado pintado
uniform float sombra_cara = 0.55;       // en 2.5D, luz que conserva una cara de espaldas al sol
uniform float sombra_proyectada = 0.7;  // en 2.5D, cuanto quita una sombra proyectada (1 = toda)

// Sombra moteada del flamboyan: zona eliptica del suelo en sombra con manchas de sol entre las hojas.
uniform vec2 moteado_centro = vec2(0.0, 0.0);
uniform vec2 moteado_radios = vec2(1.0, 1.0);
uniform float moteado_fuerza = 0.0;     // 0 = apagado
uniform float moteado_sombra = 0.4;     // luz que queda en la sombra del arbol
uniform float moteado_escala = 3.0;     // celdas de mancha por metro (manchas de 15 a 30 cm)

varying vec3 pos_mundo;  // cada shader la llena en vertex() con la posicion de mundo

void inclinar(inout vec3 v, inout vec3 n) {
	// VERTEX y NORMAL en coordenadas de mundo (render_mode world_vertex_coords)
	v.z -= inclinacion * v.y;
	// la normal bajo la cizalla z' = z - k y se transforma con la inversa transpuesta
	n = normalize(vec3(n.x, n.y + inclinacion * n.z, n.z));
}

float paso_celular(float ndl) {
	return smoothstep(0.0, suavidad, ndl);
}

float borde(vec3 normal, vec3 vista, vec3 luz) {
	float fresnel = pow(1.0 - clamp(dot(normal, vista), 0.0, 1.0), 3.0);
	// mas borde en los contornos que miran hacia el sol (contraluz de la tarde)
	float contraluz = clamp(dot(luz, -vista) * 0.5 + 0.5, 0.0, 1.0);
	return fresnel * contraluz * borde_luz;
}

float luz_pintada(float ndl, float atenuacion) {
	float celular = paso_celular(ndl);
	float cara = mix(celular, mix(sombra_cara, 1.0, celular), pintado);
	float sombra = mix(1.0, atenuacion, mix(1.0, sombra_proyectada, pintado));
	return cara * sombra;
}

float azar(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float ruido_valor(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	vec2 u = f * f * (3.0 - 2.0 * f);
	return mix(mix(azar(i), azar(i + vec2(1.0, 0.0)), u.x), mix(azar(i + vec2(0.0, 1.0)), azar(i + vec2(1.0, 1.0)), u.x), u.y);
}

// Pinceladas (2D-HD): trazos alargados en el mundo, a dos escalas, que aclaran hacia el dorado y oscurecen
// hacia el oliva, como el gouache del ancla. 0 = color plano.
uniform float pinceladas = 0.0;

vec3 pincelar(vec3 c, vec3 p) {
	if (pinceladas <= 0.0) {
		return c;
	}
	vec2 q = vec2(p.x * 0.8 + p.z * 0.6, -p.x * 0.6 + p.z * 0.8);  // trazos girados unos 37 grados
	float t1 = ruido_valor(vec2(q.x * 2.2, q.y * 8.0));
	float t2 = ruido_valor(vec2(q.x * 5.5, q.y * 17.0) + vec2(4.0, 1.3));
	float n = t1 * 0.65 + t2 * 0.35;
	vec3 claro = c * vec3(1.12, 1.08, 0.9);
	vec3 oscuro = c * vec3(0.84, 0.9, 0.94);
	return mix(c, mix(oscuro, claro, smoothstep(0.32, 0.68, n)), pinceladas);
}

float motas_estrella(vec2 p) {
	// manchas de sol con forma de estrella (el sol entre las hojas del ancla): una por celda, no en todas,
	// con giro y tamano al azar y bordes nitidos. Cada mancha cabe entera en su celda (centro en 0,3-0,7 y
	// radio maximo 0,3), asi que basta mirar la celda propia: la version de 3x3 celdas bajaba la escena de
	// 55 a 27 fps en la HD 620 (la hierba tiene mucho sobredibujado).
	vec2 c = floor(p);
	float a = azar(c);
	if (a < 0.35) {
		return 0.0;
	}
	vec2 d = p - (c + 0.3 + vec2(azar(c + 3.1), azar(c + 7.7)) * 0.4);
	float ang = atan(d.y, d.x) + a * 6.2832;
	// lobulos irregulares: cinco puntas mas un tercer armonico, como hojas y no como pegatinas
	float lobulos = 1.0 + 0.24 * cos(5.0 * ang) + 0.1 * cos(3.0 * ang + a * 9.0);
	float radio = (0.12 + 0.1 * azar(c + 1.3)) * lobulos;
	return 1.0 - smoothstep(radio - 0.03, radio + 0.02, length(d));
}

float luz_moteada(vec3 p) {
	if (moteado_fuerza <= 0.0) {
		return 1.0;
	}
	vec2 d = (p.xz - moteado_centro) / moteado_radios;
	float zona = (1.0 - smoothstep(0.65, 1.0, length(d))) * moteado_fuerza;
	zona *= 1.0 - smoothstep(0.25, 0.6, p.y);  // solo el suelo, la hierba y los pies: no el tronco
	if (zona <= 0.001) {
		return 1.0;  // fuera de la sombra del arbol no se calcula nada
	}
	float mota = motas_estrella(p.xz * moteado_escala);
	return mix(1.0, mix(moteado_sombra, 1.15, mota), zona);
}
