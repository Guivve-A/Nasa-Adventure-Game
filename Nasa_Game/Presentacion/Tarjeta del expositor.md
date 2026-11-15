# Tarjeta del expositor

> Una página para el atril, para el video `demo_v2.mp4`. Guion completo: [[Guion del expositor]]. Cifras comprobadas el 2026-11-15.

## Marcas de tiempo

| Video | Hablas | Dura | Primeras palabras | Señal en pantalla |
|---|---|---:|---|---|
| 0:00–0:17 | no | — | — | Torre, fuego, huella, bandera, ella despierta, título |
| **0:17** | sí | 16 s | «Más de quinientos millones…» | Televisor viejo |
| **0:34** | sí | 17 s | «Luz cenicienta es…» | Globo de Órbita |
| 0:52–0:54,5 | no | — | — | El ocular se abre sobre la Luna |
| **0:54,5** | sí | 14 s | «Usamos datos abiertos…» | La Luna llena el ocular |
| 1:09,5–1:22 | no | — | — | Montaje de minijuegos |
| **1:22** | sí | 20 s | «Y el corazón del reto…» | Píxel-art de la base |
| 1:42–1:45 | no | — | — | La base de Marte |
| **1:45** | sí | 21 s | «Detrás hay método…» | Tres imágenes en fila |
| 2:06–2:30 | no | — | «Gracias» al final | Escenarios, equipo, título |

## Cinco cifras que no puedes equivocar

1. **55 fichas** de datos, cada una con su fuente; **39** son dato verificado con fuente primaria.
2. **9 minijuegos** arcade, **10 misiones** y **2 bases** (Luna y Marte) de Jean, Joel y Domenica.
3. La Luna del 12 de noviembre a las 19:30: medimos **12,15 %** iluminada; JPL Horizons da **12,2 %**.
4. Corre en un portátil con gráfica integrada **Intel HD 620**: de **38 a 60 fps** según la zona (medido el 15 de noviembre; la Plaza es la más pesada).
5. Primer paso: **21:56 en Guayaquil**, visto por **más de 500 millones**.

(Y si preguntan: **212** comprobaciones con teclado simulado en los 9 minijuegos, **0 fallos**; el recorrido completo de la historia se está volviendo a probar tras los últimos cambios. Confírmalas el día anterior.)

## Siete preguntas probables

**1. ¿Dónde están los datos de la NASA y para qué sirven?**
Texturas de LRO (NASA SVS 4720) y efemérides de JPL Horizons para la Luna del telescopio; el minijuego usa esa efeméride. Medimos 12,15 % contra 12,2 %. *(`juego/minijuegos/telescopio/datos/luna.json`, `pruebas/luna_telescopio/`)*

**2. ¿Qué se juega hoy y qué falta?**
Hoy: 5 escenarios, 10 misiones y 9 minijuegos, con teclado. En curso: la cinemática, la Luna v2 y abrir las dos bases desde la biblioteca; Plaza, Mirador y Luna son provisionales, y el minimapa y las cargas esperan su revisión final. *(`Construccion/BUCLE_ESTILO.md`, `juego/datos/misiones.json`)*

**3. ¿Cómo responde a «diseñar y gestionar una misión»?**
La base exige equilibrar oxígeno, energía, alimentos y radiación, y en Marte el aterrizaje se programa y el simulador muestra la consecuencia y su causa. Presupuesto, masa y juego de hasta 4 personas son el siguiente paso. *(LEEME de los dos proyectos de la biblioteca)*

**4. ¿Qué hizo la IA y qué hicieron ustedes?**
Usamos IA y lo declaramos. Con IA se hicieron el arte de concepto, la cinemática, la música y los efectos, y la mayor parte del código y de las pruebas la escribieron asistentes de IA bajo nuestra dirección. Nuestros son el diseño, la dirección de arte, la validación de cada recurso y la verificación de cada dato con su fuente primaria. *(`Fase_1_Arte/registro_generaciones.json`, `juego/datos/FUENTES.md`)*

**5. ¿Funciona en las computadoras de una escuela?**
Medimos de 38 a 60 fps en las cinco zonas, en un portátil con gráfica integrada Intel HD 620, el 15 de noviembre de 2026 (la Plaza es la más pesada, 38). Usa el renderizador Mobile de Godot, el más rápido en ese equipo. *(`Inventario para la presentacion.md`, fila de fps; `Memory.md` §3)*

**6. ¿Cómo saben que enseña algo?**
Cada minijuego está atado a una ficha del cuaderno y Órbita da pistas en tres niveles: mirada, frase y respuesta. Todavía no hemos medido el aprendizaje con jugadores: es la siguiente prueba. *(`juego/minijuegos/*/minijuego.json`, campo `ficha`; `misiones.json`)*

**7. ¿Para quién es?**
Para estudiantes de habla hispana, y corre en equipos con gráfica integrada como los de muchas escuelas. *(La edad objetivo la confirma Guillermo antes de presentar.)*

**Si preguntan por las fichas:** «39 son datos verificados con fuente primaria; las otras 16 son mediciones nuestras (6), cálculos (4), conceptos (4) o pasajes del sueño (2), y cada una lleva su sello y dice de dónde sale.» *(`juego/datos/datos_espaciales.json`, campo `sello`)*
