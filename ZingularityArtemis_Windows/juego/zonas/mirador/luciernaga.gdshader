shader_type spatial;
// Luciernagas del Mirador (v2b): un cuadro que mira a la camara con un punto redondo y un halo suave, en mezcla
// aditiva, que late despacio. MultiMesh: el color de cada una llega por el color de instancia;
// INSTANCE_CUSTOM.x es su fase y INSTANCE_CUSTOM.y el brillo extra (se asusta o se reune en la banca).
// La inclinacion 2.5D se aplica a mano al centro, como en el resto de la escena.
render_mode unshaded, blend_add, cull_disabled, shadows_disabled, depth_draw_never;

uniform float inclinacion = 0.45;
uniform float energia = 2.6;
uniform float tam = 0.07;          // medio lado del cuadro en metros

varying float fase;
varying float susto;

void vertex() {
	fase = INSTANCE_CUSTOM.x * 6.2832;
	susto = INSTANCE_CUSTOM.y;
	vec3 centro = (MODEL_MATRIX * vec4(0.0, 0.0, 0.0, 1.0)).xyz;
	centro.z -= inclinacion * centro.y;
	vec4 vista = VIEW_MATRIX * vec4(centro, 1.0);
	vista.xy += VERTEX.xy * tam;
	POSITION = PROJECTION_MATRIX * vista;
}

void fragment() {
	// late cada 2 a 3 s: encendida un rato y casi apagada otro, nunca del todo negra
	float s = 0.5 + 0.5 * sin(TIME * 2.4 + fase);
	float pulso = 0.22 + 0.78 * s * s * s;
	float d = length(UV - vec2(0.5)) * 2.0;
	float nucleo = smoothstep(0.32, 0.12, d);
	float halo = exp(-d * d * 5.0) * 0.45;
	float a = (nucleo + halo) * clamp(pulso + susto, 0.0, 1.6);
	ALBEDO = COLOR.rgb * energia * a;
}
