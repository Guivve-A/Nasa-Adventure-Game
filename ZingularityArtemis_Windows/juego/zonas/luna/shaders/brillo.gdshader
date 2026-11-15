// Brillo de la Luna del sueno (anillo de 75 m, marcas del suelo, lamparas de las balizas, destellos).
// Sin luz ni sombra, como el emisivo del nucleo, pero con la inclinacion 2.5D comun: asi una lampara alta
// no se separa de su poste y una marca sobre el suelo con relieve sigue al terreno.
// «carrera» enciende un destello que recorre las balizas de camino en orden (cada una con su «retraso»):
// la luz corre hacia el siguiente objetivo.
shader_type spatial;
render_mode world_vertex_coords, unshaded, shadows_disabled;

uniform float inclinacion = 0.45;
uniform vec4 color : source_color = vec4(0.384, 0.894, 0.878, 1.0);
uniform float energia = 2.0;
uniform float pulso = 0.0;          // 0 = fijo; 0,3 = respira despacio
uniform float carrera = 0.0;        // 0 = sin destello que corre; 1 = destello completo
uniform float retraso = 0.0;        // fase de esta baliza en la carrera (radianes)

void vertex() {
	VERTEX.z -= inclinacion * VERTEX.y;
}

void fragment() {
	float destello = pow(max(sin(TIME * 2.2 - retraso), 0.0), 10.0) * carrera * 2.2;
	ALBEDO = color.rgb * energia * (1.0 + pulso * sin(TIME * 1.7) + destello);
}
