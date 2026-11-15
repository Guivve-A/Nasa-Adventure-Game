# LEEME de la presentación

> Qué proyectar, cómo ensayar, cómo volver a montar y qué falta revisar. Al 2026-11-15. Guion hablado: [[Guion del expositor]]. Atril: [[Tarjeta del expositor]]. Cifras: [[Inventario para la presentacion]]. Plan original del video: [[Guion del video demo]].

## 1. Qué archivo proyectar

**`Nasa_Game/Presentacion/demo_v2.mp4`**: 2:30 exactos (150,000 s, 4500 cuadros), 1920 × 1080, 30 cuadros por segundo, H.264 perfil alto, AAC 192 kb/s, con arranque rápido. Hoja de contacto (un cuadro cada 2 s): `demo_v2_hoja.jpg`.

- No uses `demo_v1.mp4` ni `DEMO_PRESENTACION.mp4`: tienen cifras que ya no son ciertas («329 comprobaciones · 0 fallos», «Más de 40 fps»).
- Reprodúcelo a pantalla completa, sin subtítulos ni mejoras de sonido del reproductor, y con el volumen del sistema al 100 %: el nivel se ajusta en la mesa de la sala.
- Prueba el sonido en la sala antes: lo que suena pleno (título, minijuegos y cierre) va a −14 LUFS; bajo la voz, la música queda unos 12 LU por debajo. Que el técnico ajuste con el tramo de 1:10 (minijuegos) y no lo toque después.

## 2. Cómo ensayar

El expositor habla en vivo sobre el video: 200 palabras en cinco bloques. La música baja sola cuando le toca hablar.

| Video | Hablas | Empieza con | Señal en pantalla |
|---|---|---|---|
| 0:00–0:17 | **no** | — | Torre, ignición, huella, bandera, ella despierta, título |
| 0:17–0:34 | sí | «Más de quinientos millones…» | Televisor viejo |
| 0:34–0:52 | sí | «Luz cenicienta es…» | Globo de Órbita |
| 0:52–0:54,5 | **no** | — | El ocular se abre sobre la Luna |
| 0:54,5–1:09,5 | sí | «Usamos datos abiertos…» | La Luna llena el ocular |
| 1:09,5–1:22 | **no** | — | Montaje de los 9 minijuegos (la música sube) |
| 1:22–1:42 | sí | «Y el corazón del reto…» | Píxel-art de la base |
| 1:42–1:45 | **no** | — | La base de Marte |
| 1:45–2:06 | sí | «Detrás hay método…» | Tres imágenes en fila |
| 2:06–2:30 | **no** | «Gracias» al final | Escenarios, equipo y título |

1. Dos pasadas leyendo con el video; tres de memoria con el video; una sin video, con cronómetro.
2. Ritmo: 2,5 palabras por segundo mientras hablas (150 por minuto). El bloque 3 **tiene** que terminar antes de 1:09,5; «Jugando» debe caer antes de 2:06.
3. Si te atrasas, suelta la pausa `//` del bloque y entra en el siguiente con su señal: el video no espera.
4. Si el video falla: versión de 45 s del [[Guion del expositor]].

## 3. Cómo volver a montar

Todo sale de `montaje.json` (v2) con `herramientas/demo/montar_demo.py`, desde la raíz del repositorio:

```
python -I herramientas/demo/graficos.py                      # graficos, rotulos y animaciones (G01, G02, ocular)
python -I herramientas/demo/montar_demo.py --revisar         # plan: que material usa cada segmento y que falta
python -I herramientas/demo/montar_demo.py --salida Nasa_Game/Presentacion/demo_v3.mp4 --hoja Nasa_Game/Presentacion/demo_v3_hoja.jpg
```

- Los segmentos que no cambian se toman de la caché (`intermedios/`, se puede borrar); un montaje completo tarda unos 15 minutos en el portátil y uno parcial, unos 5.
- **Clips nuevos de la cinemática.** Si aparecen en `Fase_1_Arte/Exploracion/Lote_10/clips/` los `P10_elegido.mp4`, `P11_elegido.mp4`, `P13_elegido.mp4` o `P14_elegido.mp4`, el montador los usa solo en S08, S04, S05 y S06 (hoy van con fotograma fijo y movimiento lento). Basta con volver a montar.
- **Cifras.** Si cambian las pruebas o los fps, se cambia el texto del rótulo en `montaje.json` (S38, S39), se corre `graficos.py` y se vuelve a montar. El registro de S38 se rehace con `python -I herramientas/demo/g05_registro.py <log> --titulo "..."`.
- **Sonido.** `--pleno -14` (tramos plenos) y `--bajada-db 15` (música bajo la voz) son los valores por defecto; `--pleno nan --lufs -16` vuelve a la normalización por integrado de la v1.
- Cambios rápidos sin tocar `montaje.json`: `ajustes_montaje.json` (hoy vacío).

## 4. Qué cambió de la v1 a la v2

Correcciones de los dos críticos del 2026-11-15 (video y guion):

| Problema | Arreglo en la v2 |
|---|---|
| «329 comprobaciones · 0 fallos» era falso (el recorrido de hoy da 126 y 7 fallos) | Se corrieron las 9 `prueba_manos.gd`: **212 comprobaciones, 0 fallos**. Rótulo de S38: «Minijuegos: 212 pruebas, 0 fallos». El recorrido completo no se muestra |
| «43–59 fps» desactualizado | Medido hoy con `--medir=5`, sin otro Godot: Habitación 56,3; **Plaza 38,3**; Sendero 41,1; Mirador 40,1; Luna 60,3. Como la Plaza baja de 40, el rótulo no lleva cifra: «Corre en una Intel HD 620» |
| «11 misiones» era falso | 10 misiones (G06 y tarjeta). `s1_base` no se puede completar hasta integrar las bases |
| El guion no cabía en sus ventanas | 200 palabras a 2,5 palabras por segundo, con margen en cada bloque; «construyan» en vez de «diseñen»; «low-poly de acabado pintado» en vez de «pintado a mano»; sin «veinte mil líneas» en el texto hablado |
| La IA, subestimada en la tarjeta | Pregunta 4 nueva: el código y las pruebas los escribieron sobre todo asistentes de IA bajo dirección del equipo |
| Título legible 0,9 s; subtítulo ilegible | Título entero 2,05 s (14,5–17,0) y 2,35 s en el cierre; subtítulo en crema, más grande, fuera del halo y con franja oscura |
| Zoom del telescopio cortaba la interfaz | `graficos/luna_sola.png`: la Luna y sus dos rótulos, sin panel ni globo; el ocular se abre sobre ella |
| Carga pintada como doble exposición | La lámina de carga de la Luna (`juego/interfaz/arte/carga_luna.jpg`) entera, con acercamiento lento |
| Rótulos de minijuegos de 1,3 s | Un rótulo fijo de 14 s, «9 minijuegos · 9 ideas reales», y debajo la idea de cada juego, que cambia en cada corte |
| La base no se entendía como el reto | Rótulos «El reto: sostener una base», «Oxígeno, energía, alimentos y radiación» con acercamiento a las cuatro barras; orden de la historia (base → rover → lluvia solar → despegue → Marte); Marte de Domenica (`marte_superficie.mp4`) en vez del capítulo provisional; sin «Siete minutos de terror» |
| «Dos juegos de la biblioteca» | «Juegos del equipo · en integración» |
| Mirador oscuro y sin Luna durante 10 s | S40: la lámina de carga del Mirador (ella junto al telescopio, frente a la Luna) con acercamiento lento; S47: el alejamiento del Mirador en cámara lenta |
| Sonido: plenos a −11,5 LUFS, crescendo de golpe | Plenos normalizados a −14 LUFS; crescendo real de 2:03 a 2:06 y subida al montaje de 1:09,5 a 1:10 |
| G02 congelado, G04 quieto, tríptico vacío, collage viejo | G02 animado (las lunas se encienden y las cifras cuentan); G04 con empuje del 3 %; tríptico más grande y con entradas cada 0,8 s; G07 nuevo con un cuadro de cada escenario de hoy |
| Avisos del juego bajo los rótulos | Tomas empezadas después del título de zona (Habitación desde 2,0 s, Sendero desde 3,0 s); el Mirador lleva su propio título de zona y ningún rótulo encima |

## 5. Qué es provisional en el video

- **Cinemática (0:00–0:17 y 0:17–0:27):** S01 a S03 son clips de video; S04, S05, S06 y S08 (huella, bandera, despertar y televisor) son fotogramas fijos con movimiento lento porque sus clips (P10, P11, P13 y P14) aún no existen. Llevan el sello «Imágenes recreadas con IA».
- **Escenarios:** la Plaza, el Mirador y la Luna son provisionales (su arte espera la validación de Guillermo); en el collage de 2:06 llevan la marca «arte provisional». La Luna v2 está en construcción.
- **Las dos bases** se juegan como proyectos aparte: abrirlas desde los libros de la biblioteca está en integración (lo dice el rótulo de S33).
- **Minimapa y pantallas de carga:** funcionan, pero esperan su revisión final.
- **Recorrido completo con teclas:** hoy no está en verde (126 comprobaciones, 7 fallos: un error de guion en el Mirador, `PlacaLuciernagas` liberada en `pruebas.gd:553`). Por eso el video solo cita las 212 pruebas de los minijuegos.
- **El telescopio** del ocular es la prueba técnica de `pruebas/luna_telescopio/` (lo dice su rótulo).

## 6. Lo que Guillermo debe revisar con sus propios ojos y oídos

Nadie pudo escuchar el sonido: solo se midió.

1. **Todo el sonido, de principio a fin**, en los altavoces de la sala si se puede: que la música bajo la voz no tape al expositor; que el crescendo de 2:03 a 2:06 se sienta como subida y no como golpe; que el rugido del cohete (0:06) y el despegue (1:34,5) no asusten; que el sonido propio de los minijuegos no estorbe.
2. **El texto en vivo con el video**, cronometrado: si a tu ritmo algún bloque no cabe, se recorta el texto, no el video.
3. **La pregunta 7 de la tarjeta** («¿Para quién es?»): confirmar la edad objetivo.
4. **La pregunta 4** (qué hizo la IA): que la respuesta te represente.
5. **La cifra de fps** antes de presentar: la Plaza dio 38,3; si se optimiza y todas las zonas pasan de 40, se puede volver a poner «40 fps o más · Intel HD 620».
6. **El recorrido completo** (`--prueba=recorrido_manos`): si se arregla el Mirador y queda en verde, se puede volver a citar en S38 y en la tarjeta.
7. **El collage de escenarios (2:06)** y la marca «arte provisional»: decidir si se queda.
8. **Los rótulos de los minijuegos**, uno por uno: que la idea que dice cada uno sea la que tú quieres contar.
9. Que en ningún cuadro aparezca algo que sugiera respaldo de la NASA: se dice «datos abiertos de la NASA» y se citan LRO y JPL Horizons, sin logotipos.

## 7. Comprobaciones hechas para la v2

| Qué | Cómo | Resultado |
|---|---|---|
| Pruebas con teclas de los 9 minijuegos | `python -I herramientas/juego_ejecutar.py -- --prueba=guion:res://minijuegos/<id>/prueba_manos.gd --ritmo=1` | 212 PRUEBA_OK, 0 PRUEBA_FALLO (seguidor 16, antena 9, satélite 28, telescopio 29, línea de tiempo 30, muestras 66, banderas 11, regreso 6, órbita 17) |
| Recorrido completo con teclas | `... -- --prueba=recorrido_manos --ritmo=2` | 126 hechas, 7 fallos (sin cambios desde la mañana) |
| fps de las cinco zonas | `... --ventana -- --zona=<id> --medir=5` | 56,3 / 38,3 / 41,1 / 40,1 / 60,3 |
| Misiones | `juego/datos/misiones.json` | 10 de la ruta principal (m1 a m10), más `s1_base` y la plantilla |
| Fichas | `juego/datos/datos_espaciales.json` | 55: 39 «Dato verificado», 6 medidos, 4 cálculos, 4 conceptos, 2 del sueño |
| Líneas de código | `.gd` de `juego/` | 20 677 |
| Video final | `ffprobe` | H.264 High, 1920 × 1080, yuv420p, 30/1, **4500 cuadros, 150,000 s**; 10,6 Mb/s; AAC 48 kHz 189 kb/s; `+faststart` |
| Sonido final | medidor EBU R128 de ffmpeg (`loudnorm` y `ebur128`) | Integrado −18,3 LUFS; pico real −2,1 dBTP; LRA 15,9. Plenos: minijuegos −13,8 y cierre −13,5 LUFS; título −18,8 (música que entra). Bajo la voz: de −28,1 a −28,9 LUFS (unos 15 LU por debajo del pleno). Respiros: −20,0 (ocular) y −20,5 (Marte) |
| Crescendo de 2:03 a 2:06 | sonoridad momentánea | −28,4 (2:03,1) → −26,0 (2:04,1) → −17,3 (2:05,1) → −15,8 (2:06,1) → −14,1 (2:06,6): sube de forma continua, sin golpe |
| Entrada del montaje de minijuegos | sonoridad momentánea | −28,7 (1:09,6) → −17,7 (1:10,1) → −14,5 (1:11,1): la subida es de 0,5 s y cae en el primer corte, a propósito (con el efecto de subida de S22) |

**Nota sobre el sonido.** El encargo pedía −16 LUFS integrados; la revisión pidió que los tramos plenos quedaran en −14. Se eligió lo segundo: con 91 s de cama bajo la voz, el integrado queda en −18,3. Si la sala lo pide más fuerte, que suba el volumen de la mesa: el pico real tiene 2,1 dB de margen. Si la cama bajo la voz se oye demasiado baja, se puede montar con `--bajada-db 14` (queda a unos −27,5).
