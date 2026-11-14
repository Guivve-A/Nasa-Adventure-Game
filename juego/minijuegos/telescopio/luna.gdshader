shader_type canvas_item;

// Luna vista por un ocular. Cada pixel del disco se proyecta sobre una esfera y se convierte a
// longitud y latitud selenograficas para leer las texturas de NASA (color LROC, normales de LOLA).
// Marco del cuerpo: X hacia (lon 0, lat 0), Y hacia (lon 90 E, lat 0), Z hacia el polo norte.
// Pantalla: x a la derecha, y hacia el cenit, z hacia el observador.
// Cambios tras la verificacion: derivadas fuera de las ramas, textureGrad sin salto en la costura,
// sin envolver los polos, relieve exagerado en el shader (normales horneadas x1), luz cenicienta
// plana y escalada con la fase de la Tierra, y salida lineal si el proyecto usa HDR 2D.

uniform sampler2D color_luna : filter_linear_mipmap_anisotropic, repeat_disable;
uniform sampler2D normales_luna : filter_linear_mipmap_anisotropic, repeat_disable;
uniform vec3 dir_obs = vec3(1.0, 0.0, 0.0);   // punto subobservador (marco del cuerpo)
uniform vec3 dir_sol = vec3(0.0, 1.0, 0.0);   // punto subsolar (marco del cuerpo)
uniform float pa_norte = 0.0;                 // polo norte lunar respecto del cenit, radianes, positivo a la izquierda
uniform float lon_centro = 0.0;               // longitud en el centro del mapa, radianes
uniform vec2 centro = vec2(0.40, 0.5);        // centro del ocular, en UV del rectangulo
uniform float radio = 0.29;                   // radio del disco lunar, en fraccion del alto
uniform float radio_ocular = 0.46;            // radio del ocular, en fraccion del alto
uniform float aspecto = 1.7778;
uniform vec2 desplazamiento = vec2(0.0);     // Luna respecto del eje del buscador
uniform float exposicion = 1.45;
uniform float luz_cenicienta = 0.07;
uniform float factor_cenicienta = 1.0;        // fase de la Tierra vista desde la Luna, normalizada
uniform float relieve_terminador = 4.0;       // exageracion del relieve junto al terminador
uniform float relieve_base = 1.5;             // exageracion con el Sol alto
uniform bool usar_relieve = true;
uniform bool mostrar_luna = true;             // falso si la Luna esta bajo el horizonte
uniform bool salida_lineal = false;           // verdadero si el viewport usa HDR 2D
uniform int modo_prueba = 0;                  // 1: iluminado blanco, noche gris, fuera negro

float azar(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

// curva sRGB exacta: con HDR 2D Godot codifica la salida con ella, no con pow(1/2.2)
vec3 srgb_a_lineal(vec3 c) {
	return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c));
}

void fragment() {
	vec2 p = (UV - centro) * vec2(aspecto, 1.0);
	p.y = -p.y;
	float r_ocular = length(p);

	vec3 fondo = vec3(0.110, 0.157, 0.180); // Estilo.NOCHE
	vec2 celda = floor(UV * vec2(aspecto, 1.0) * 260.0);
	if (azar(celda) > 0.9972) {
		fondo = mix(fondo, vec3(0.965, 0.906, 0.784), 0.4 + 0.3 * azar(celda + 7.3));
	}
	vec3 col = modo_prueba == 1 ? vec3(0.0) : fondo;

	// geometria y derivadas fuera de las ramas
	vec2 d = (p - desplazamiento) / radio;
	float rr = dot(d, d);
	float rad = sqrt(rr);
	float aa = fwidth(rad);
	vec2 dc = d / max(rad, 1.0);
	float z = sqrt(max(1.0 - dot(dc, dc), 0.0));
	vec3 norte = vec3(0.0, 0.0, 1.0);
	vec3 a = normalize(norte - dot(norte, dir_obs) * dir_obs);  // norte proyectado en el cielo
	vec3 b = cross(dir_obs, a);
	vec2 s_n = vec2(-sin(pa_norte), cos(pa_norte));
	vec2 s_b = vec2(-cos(pa_norte), -sin(pa_norte));
	vec3 punto = normalize(dot(dc, s_n) * a + dot(dc, s_b) * b + z * dir_obs);
	float lon = atan(punto.y, punto.x);
	float lat = asin(clamp(punto.z, -1.0, 1.0));
	vec2 uv = vec2(fract(0.5 + (lon - lon_centro) / TAU), 0.5 - lat / PI);
	vec2 gx = dFdx(uv);
	vec2 gy = dFdy(uv);
	gx.x -= round(gx.x);
	gy.x -= round(gy.x);
	float geo = dot(punto, dir_sol);

	if (mostrar_luna && rr <= 1.0) {
		if (modo_prueba == 1) {
			col = geo > 0.0 ? vec3(1.0) : vec3(0.5);
		} else {
			vec3 albedo = pow(textureGrad(color_luna, uv, gx, gy).rgb, vec3(2.2));
			vec3 n = punto;
			vec3 n1 = textureGrad(normales_luna, uv, gx, gy).rgb * 2.0 - 1.0;
			if (usar_relieve && dot(n1, n1) > 1e-4) {
				n1 = normalize(n1);
				float k = mix(relieve_terminador, relieve_base, smoothstep(0.17, 0.5, geo));
				n = normalize(punto + k * (n1 - dot(n1, punto) * punto) / max(dot(n1, punto), 0.2));
			}
			float mu0 = dot(n, dir_sol);
			float mu = max(dot(n, dir_obs), 0.0);
			// Lommel-Seeliger: la Luna llena se ve pareja, sin oscurecerse hacia el borde
			float sol = mu0 > 0.0 ? 2.0 * mu0 / (mu0 + mu + 1e-4) : 0.0;
			// el relieve solo puede encender cumbres apenas pasado el terminador, no en plena noche
			sol *= smoothstep(-0.025, 0.015, geo);
			// la luz cenicienta llega desde la Tierra (direccion del observador): disco plano
			vec3 cenicienta = albedo * luz_cenicienta * factor_cenicienta * vec3(0.82, 0.9, 1.1)
				* (1.0 - smoothstep(-0.05, 0.05, geo));
			vec3 luna = pow(albedo * sol * exposicion + cenicienta, vec3(1.0 / 2.2));
			float suave = clamp((1.0 - rad) / max(aa, 1e-5), 0.0, 1.0);
			col = mix(fondo, luna, suave);
		}
	}

	if (modo_prueba == 0) {
		// reticula cian fina, con hueco en el centro
		float linea = 0.0012;
		float hueco = radio * 1.08;
		bool en_cruz = (abs(p.x) < linea && abs(p.y) > hueco) || (abs(p.y) < linea && abs(p.x) > hueco);
		if (en_cruz && r_ocular < radio_ocular - 0.01) {
			col = mix(col, vec3(0.38, 0.89, 0.88), 0.55);
		}
		float anillo = 1.0 - smoothstep(0.0, 0.004, abs(r_ocular - (radio_ocular - 0.012)));
		col = mix(col, vec3(0.38, 0.89, 0.88), anillo * 0.7);
		col *= (1.0 - smoothstep(radio_ocular - 0.03, radio_ocular, r_ocular)) * 0.92 + 0.08 * step(r_ocular, radio_ocular);
	}
	if (r_ocular > radio_ocular) {
		col = modo_prueba == 1 ? vec3(0.0) : vec3(0.318, 0.420, 0.486); // Estilo.PETROLEO
	}
	if (salida_lineal) {
		col = srgb_a_lineal(clamp(col, 0.0, 1.0));
	}
	COLOR = vec4(col, 1.0);
}
