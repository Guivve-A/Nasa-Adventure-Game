# Tarjeta del expositor

> Una página para el atril. Guion completo: [[Guion del expositor]].

## Marcas de tiempo

| Video | Hablas | Primeras palabras | Señal en pantalla |
|---|---|---|---|
| 0:00–0:17 | no | — | Torre, fuego, huella, título |
| **0:17** | sí, 17 s | «Más de quinientos millones…» | Televisor viejo |
| **0:34** | sí, 18 s | «Luz cenicienta es…» | Globo de Órbita |
| 0:52–0:55 | no | — | El ocular se abre |
| **0:55** | sí, 15 s | «Usamos datos abiertos…» | La Luna llena la pantalla |
| 1:10–1:22 | no | — | Montaje de minijuegos |
| **1:22** | sí, 19 s | «Y el corazón del reto…» | Píxel-art de la base |
| 1:41–1:45 | no | — | Despega el cohete |
| **1:45** | sí, 21 s | «Detrás hay método…» | Tres imágenes en fila |
| 2:06–2:30 | no | «Gracias» al final | Cifras, equipo, título |

## Cinco cifras que no puedes equivocar

1. **55 fichas** de datos con su fuente; **39** son dato verificado.
2. **9 minijuegos** arcade, y **2 bases** (Luna y Marte) de Jean, Joel y Domenica.
3. La Luna del 12 de noviembre a las 19:30: medimos **12,15 %** iluminada; JPL Horizons da **12,2 %**.
4. **De 43 a 59 fps** en un portátil con Intel HD 620, a 1280 × 720.
5. Primer paso: **21:56 en Guayaquil**, visto por **más de 500 millones**.

(Y si preguntan: **329** comprobaciones con teclado simulado, 0 fallos; **más de 20 000** líneas de código. Confírmalas el día anterior.)

## Seis preguntas probables

**1. ¿Dónde están los datos de la NASA y para qué sirven?**
Texturas de LRO (NASA SVS 4720) y efemérides de JPL Horizons para la Luna del telescopio; el minijuego usa esa efeméride. Medimos 12,15 % contra 12,2 %. *(`juego/minijuegos/telescopio/datos/luna.json`, `pruebas/luna_telescopio/`)*

**2. ¿Qué se juega hoy y qué falta?**
Hoy: 5 escenarios, 11 misiones y 9 minijuegos, con teclado. En curso: la cinemática, la Luna v2 y abrir las bases desde la biblioteca; Plaza, Mirador y Luna son provisionales. *(`Construccion/BUCLE_ESTILO.md`, `juego/datos/misiones.json`)*

**3. ¿Cómo responde a «diseñar y gestionar una misión»?**
La base exige equilibrar oxígeno, energía, alimentos y radiación, y en Marte el aterrizaje se programa y el simulador muestra la consecuencia y su causa. Presupuesto, masa y juego de hasta 4 personas son el siguiente paso. *(LEEME de los dos proyectos de la biblioteca)*

**4. ¿Qué hizo la IA y qué hicieron ustedes?**
Usamos IA para el arte de concepto, la cinemática, el sonido y como asistente de código, y lo declaramos. El diseño, la dirección, la verificación de datos y las pruebas son nuestros; ningún dato entra sin fuente. *(`Fase_1_Arte/registro_generaciones.json`, `juego/datos/FUENTES.md`)*

**5. ¿Funciona en las computadoras de una escuela?**
Medimos de 43 a 59 fps en un portátil con gráfica integrada Intel HD 620. Usa el renderizador Mobile de Godot, el más rápido en ese equipo. *(`BUCLE_ESTILO.md` fila 3; `Memory.md` §3)*

**6. ¿Cómo saben que enseña algo?**
Cada minijuego está atado a una ficha del cuaderno y Órbita da pistas en tres niveles: mirada, frase y respuesta. Todavía no hemos medido el aprendizaje con jugadores: es la siguiente prueba. *(`juego/minijuegos/*/minijuego.json`, campo `ficha`; `misiones.json`)*
