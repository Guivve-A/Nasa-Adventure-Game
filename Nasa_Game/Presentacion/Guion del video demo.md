# Guion del video demo

> Video de presentación de «Luz cenicienta» para el reto de diseño de juegos espaciales. **150 s exactos, 1920 × 1080, 30 cuadros por segundo.** El expositor habla en vivo sobre el video durante 90 s ([[Guion del expositor]]); no hay voz grabada. Los otros 60 s son del video solo, con sonido pleno. Lista para el editor: `montaje.json` (misma carpeta). Cifras y estados: [[Inventario para la presentacion]].

> [!important] Versión 2 (2026-11-15)
> Este guion es el plan original. **Manda `montaje.json` v2**, que corrige lo que encontraron los dos críticos: título legible 2 s, el bloque 2 en el orden Órbita → Plaza → Sendero → Mirador → Luna → mapa → carga, la Luna sola en el ocular, G02 animado, un rótulo fijo para los 9 minijuegos con la idea de cada uno, la base en el orden de la historia (base lunar → rover → lluvia solar → despegue → Marte) y un respiro sobre la base de Marte de Domenica, cifras de pruebas y fps verdaderas, la lámina del Mirador con la Luna para la frase final y el collage de escenarios con las tomas de hoy. El texto del expositor vigente está en [[Guion del expositor]]; los cambios y el ensayo, en [[LEEME de la presentacion]].

## 1. Estructura

| Tramo | Tiempo | Dura | Voz | Qué tiene que lograr |
|---|---|---:|---|---|
| Gancho | 0:00–0:17 | 17 s | no | Emoción: ignición, huella, bandera y Tierra, ella que despierta, título |
| 1. Problema y respuesta | 0:17–0:34 | 17 s | **sí** | 500 millones lo miraron; nosotros queremos que lo construyan |
| 2. El mundo y su arte | 0:34–0:52 | 18 s | **sí** | Cinco escenarios pintados a mano, Órbita, mapa y carga |
| Respiro | 0:52–0:55 | 3 s | no | El ocular se abre a la Luna real |
| 3. Datos reales | 0:55–1:10 | 15 s | **sí** | LRO, JPL Horizons, 55 fichas con fuente |
| 4. Los 9 minijuegos | 1:10–1:22 | 12 s | no | Montaje rápido: una idea por juego |
| 5. La base: Luna y Marte | 1:22–1:41 | 19 s | **sí** | El corazón del reto: oxígeno, energía, alimentos y radiación |
| Respiro | 1:41–1:45 | 4 s | no | Despegue del cohete de la base |
| 6. Ingeniería y proceso | 1:45–2:06 | 21 s | **sí** | Concepto → hoja → motor; pruebas; portátil modesto; frase final |
| Cierre | 2:06–2:30 | 24 s | no | Cifras, equipo, última imagen, título |
| **Total** | | **150 s** | **90 s** | |

## 2. Reglas del montaje

- **Un solo rótulo a la vez**, de 6 palabras como máximo, en la tipografía de la interfaz del juego (crema `#F8C991` sobre una franja oscura translúcida, abajo a la izquierda). Entra con 6 cuadros de fundido y sale con 6.
- **Sello** (no cuenta como rótulo): «Imágenes recreadas con IA», pequeño, abajo a la derecha, al 70 %, en todo plano de la cinemática.
- Nada de logotipos, insignias ni la marca NASA como sello. Se escribe «datos abiertos de la NASA» y las fuentes (LRO, JPL Horizons).
- Lo provisional no se rotula como terminado. La cinemática lleva su sello; la Luna con texturas LRO lleva «prueba técnica».
- Capturas del juego a 1280 × 720 se escalan a 1920 × 1080 con Lanczos; si la toma se grabó a 1080p, mejor.
- Color: el juego ya trae su paleta (D-015). Solo un ajuste común de contraste; nada de filtros que cambien el estilo.
- Las transiciones son cortes, salvo donde se indica.

## 3. Plano a plano

**Material:** las rutas son relativas a `Nasa_Game/` salvo las que empiezan por `juego/`, `pruebas/`, `Misión Artemis/` o `Marte_Gravedad2DHD/`. «Clip» = video de la cinemática en `Fase_1_Arte/Exploracion/Lote_10/clips/<plano>_elegido.mp4`, que otro flujo está generando: **si existe al montar, se usa; si no, va la imagen fija con el movimiento indicado.** `T..` = toma por capturar (§4). `G..` = gráfico propio (§5).

### Gancho · 0:00–0:17 · sin voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S01 | 0:00,0–0:02,5 | La torre. Clip `P03` o `Fase_1_Arte/Exploracion/Lote_09/L09b_K03_final.png`, acercamiento lento 100 → 106 %. Entra del negro en 0,5 s. Sello IA | — | Viento, agua en la orilla, respiración. Sin música | (callado) |
| S02 | 0:02,5–0:06,0 | La ignición. Clip `P04` o `Lote_09/L09b_K04a_final_r1.png` (0:02,5–0:04,5) y disolvencia de 0,3 s a `Lote_09/L09b_K04b_final.png` (0:04,5–0:06,0), con temblor del 1 % | — | Silencio con respiración. **Golpe grave a 0:04,8** | — |
| S03 | 0:06,0–0:08,5 | La columna. Clip `P05` o `Lote_10/fotogramas/L10_K05_placas_lisas.png`, inclinación hacia arriba (paneo vertical del 8 %) | — | **Rugido a tope** (el pico de la mezcla, −1 dBTP) | — |
| S04 | 0:08,5–0:11,0 | La huella. Clip `P11` o `Lote_09/L09b_K11a_final.png` (0:08,5–0:09,3) y corte a `Lote_09/L09b_K11_final.png`, empuje del 0,5 % por segundo | — | **Corte seco a silencio total** en el primer cuadro | — |
| S05 | 0:11,0–0:13,0 | La bandera y la Tierra. Clip `P13` o `Lote_09/L09d_K13a_final.png`, inclinación lenta hacia arriba | — | **Primera nota** de la música, sola | — |
| S06 | 0:13,0–0:15,5 | Ella abre los ojos. Clip `P14` o `Lote_09/L09c_P14c_C_cine_gpt.png`, acercamiento al ojo 100 → 112 % y franja ámbar que sube | — | Segunda nota. Toma de aire | — |
| S07 | 0:15,5–0:17,0 | Título sobre negro: un punto de luz ámbar que se abre (`G01`). Sin sello | **«Luz cenicienta»** | Acorde pleno. Desde 0:16,6 la música baja a cama (−20 dB) | Se prepara |

### 1. Problema y respuesta · 0:17–0:34 · voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S08 | 0:17,0–0:22,0 | El televisor de 1969. Clip `P10` o `Lote_09/L09b_K10_final.png` en 4:3 sobre negro, con grano y barrido de líneas. Sello IA | «20 de julio de 1969» (0:17,5–0:21,5) | Siseo de tubo bajo. Música en cama | «Más de quinientos millones… en un televisor.» |
| S09 | 0:22,0–0:27,0 | Guayaquil de noche. `Lote_09/L09b_K12_final_v2.png`, acercamiento lento. Sello IA | — | Grillos. Cama | «Aquí, en Guayaquil… de la noche.» |
| S10 | 0:27,0–0:34,0 | Del sueño al juego: disolvencia de 0,5 s a **T01** (Habitación-taller de mañana; ella cruza la alfombra hacia el banco y Órbita la sigue) | «Godot 4.7 · jugable hoy» (0:28,0–0:33,0) | Pájaros de mañana, `juego/audio/paso.ogg` | «Nosotros no queremos que solo lo miren…» |

### 2. El mundo y su arte · 0:34–0:52 · voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S11 | 0:34,0–0:38,0 | **T02**: ella habla con Órbita (E); globo de diálogo con su pista | — | Cama; `radio.ogg` bajo | «Luz cenicienta es una aventura…» |
| S12 | 0:38,0–0:42,0 | **T03**: Plaza de las Iguanas de tarde; camina hacia la biblioteca | «Habitación · Plaza · Sendero · Mirador · Luna» (0:38,0–0:44,0) | `paso.ogg` | «Una estudiante de ingeniería de control…» |
| S13 | 0:42,0–0:45,0 | **T04**: Sendero del arroyo, sube la escalera; minimapa con el objetivo | — | `ambiente_sendero.ogg` | «…recorren su barrio…» |
| S14 | 0:45,0–0:46,5 | **T07**: pantalla de carga pintada hacia el Mirador (o `Fase_1_Arte/Exploracion/Lote_08/L08_carga_mirador.png` con acercamiento) | — | `umbral.ogg` | «…hasta la Luna…» |
| S15 | 0:46,5–0:49,0 | **T05**: Mirador del Faro de noche, faroles y luciérnagas | «Minimapa con el objetivo» (0:46,5–0:49,0)* | Grillos | «…de un sueño.» |
| S16 | 0:49,0–0:50,5 | **T20**: Luna del sueño, salto lento con Órbita | — | `paso_luna.ogg`, `salto.ogg` | «Todo es low-poly pintado a mano…» |
| S17 | 0:50,5–0:52,0 | **T06**: mapa del mundo (tecla M), el cursor recorre los lugares (o `Construccion/Capturas/mapa_del_mundo.png` con paneo) | — | `pagina.ogg` | «…con mapa y cargas ilustrados.» |

\* Si T05 no muestra el minimapa, el rótulo pasa a S13 (0:42,0–0:45,0), que sí lo muestra.

### Respiro · 0:52–0:55 · sin voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S18 | 0:52,0–0:55,0 | **T08**: ella se asoma al telescopio del Mirador (0:52,0–0:53,0); máscara circular de ocular que se abre a `Propuestas/Capturas/luna_telescopio.png` (0:53,0–0:55,0) | «Guayaquil · 12 nov 2026, 19:30» | `radio.ogg` (pitido). La música sube a −10 dB y vuelve a cama a 0:54,7 | (pausa) |

### 3. Datos reales · 0:55–1:10 · voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S19 | 0:55,0–1:00,0 | La Luna con texturas LRO (`Propuestas/Capturas/luna_telescopio.png`, o **T21** si se graba), acercamiento lento 100 → 115 % hacia el terminador | «Texturas LRO · prueba técnica» | Cama | «Usamos datos abiertos de la NASA…» |
| S20 | 1:00,0–1:04,0 | **G02**: la máscara medida junto al disco de Horizons, con las dos cifras | «Medido 12,15 % · Horizons 12,2 %» | Cama | «…y su luz coincide con JPL Horizons.» |
| S21 | 1:04,0–1:07,5 | **T09**: el cuaderno (Tab); pasan tres fichas con su fuente | «55 fichas · 39 verificadas» | `pagina.ogg` ×2 | «Cada ficha del cuaderno cita su fuente.» |
| S22 | 1:07,5–1:10,0 | `Construccion/Capturas/vuelta6_arcade_nueve.jpg`: de una casilla a la rejilla entera | «9 minijuegos arcade» | Subida (riser) hacia el montaje | «Y cada minijuego enseña una idea real.» |

### 4. Los 9 minijuegos · 1:10–1:22 · sin voz

1,33 s por juego (40 cuadros), cortes en el pulso de la música. Música plena. Si falta una toma, va su casilla de `vuelta6_arcade_nueve.jpg` (cada una mide unos 640 × 360) con un empuje del 4 %.

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido |
|---|---|---|---|---|
| S23 | 1:10,00–1:11,33 | **T11** seguidor: el motor sigue la Luna, la barra REC se llena | «Control» | Sonido del juego |
| S24 | 1:11,33–1:12,67 | **T12** antena: el haz alcanza al satélite sobre el volcán | «Rastreo» | Sonido del juego |
| S25 | 1:12,67–1:14,00 | **T13** satélite: una pieza encaja en el cubo | «CubeSat» | Sonido del juego |
| S26 | 1:14,00–1:15,33 | **T14** telescopio: la franja dorada y el registro de un rasgo | «Observación» | Sonido del juego |
| S27 | 1:15,33–1:16,67 | **T15** línea de tiempo: salta a una placa y aparece el año | «Historia» | Sonido del juego |
| S28 | 1:16,67–1:18,00 | **T16** muestras: salto lunar y recoge con la herramienta | «Herramientas» | Sonido del juego |
| S29 | 1:18,00–1:19,33 | **T17** banderas: golpe al compás, «¡JUSTO!» | «Cooperación» | `golpe_mastil.ogg` |
| S30 | 1:19,33–1:20,67 | **T18** regreso: escudo abajo entre el calor, se abren los paracaídas | «Reentrada» | Sonido del juego |
| S31 | 1:20,67–1:22,00 | **T19** órbita: cruza el último anillo y se sella | «Órbita» | `logro.ogg`; la música baja a cama en 1:21,8 |

### 5. La base: Luna y Marte · 1:22–1:41 · voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S32 | 1:22,0–1:25,5 | **T22a**: Misión Artemis, la base del polo sur lunar | «El reto: sostener una base» | Cama | «Y el corazón del reto: sostener una base espacial.» |
| S33 | 1:25,0–1:30,0 | **T23**: el rover y la veta de hielo; corte a Marte, llegada (o `capturas/05_rover.png` 2,5 s y `capturas/11_marte_llegada.png` 2,5 s) | — | Cama | «Jean, Joel y Domenica crearon…» |
| S34 | 1:30,0–1:35,0 | **T22**: lluvia solar, carrera a la cúpula; acercamiento a las cuatro barras (o `capturas/02_lluvia_solar.png`) | «Lluvia solar: ¡a la cúpula!» | Alarma corta, baja | «Hay que equilibrar oxígeno, energía…» |
| S35 | 1:37,0–1:42,0 | **T25**: Marte, el simulador de aterrizaje: se programa y se prueba; sale el resultado con su causa | «Aterrizaje programado, sin pilotear en vivo» | Cama | «…por eso el aterrizaje se programa y se simula.» |

### Respiro · 1:41–1:45 · sin voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S36 | 1:41,0–1:45,0 | **T24**: despegue del cohete de la base y el viaje (o `capturas/09_despegue.png` 2 s y `capturas/10_viaje.png` 2 s) | — | Rugido corto; la música sube a −8 dB y baja a cama en 1:44,7 | (pausa) |

### 6. Ingeniería y proceso · 1:45–2:06 · voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido | Expositor |
|---|---|---|---|---|---|
| S37 | 1:45,0–1:50,0 | **G03**: tríptico que entra de izquierda a derecha cada 1,5 s: concepto `Fase_1_Arte/Exploracion/Lote_02/L02_exploracion_camara_alta.png` → hojas `Fase_1_Arte/Hojas_de_referencia/Hojas_v1_lamina.jpg` → motor `Construccion/Capturas/sendero_jugable.png` | «9 hojas · 104 piezas» | Cama; `pagina.ogg` en cada entrada | «Detrás hay método de estudio…» |
| S38 | 1:50,0–1:55,0 | Pantalla partida. Izquierda, `mj_muestras.mp4` (el recolector lunar jugándose solo con teclas); derecha, su registro real desplazándose (`graficos/G05_registro_largo.png`, de `material/consola_muestras_manos.txt`) | «Minijuegos: 212 pruebas, 0 fallos» | Cama; tecleo suave | «Todo está hecho por código, con pruebas que lo juegan solas con el teclado.» |
| S39 | 1:55,0–1:59,5 | `sendero.mp4` (no hay toma del portátil, T28) | «Corre en una Intel HD 620» (sin cifra: la Plaza mide 38,3 fps) | Cama | «Corre en un portátil modesto, con gráfica integrada.» |
| S40 | 2:00,0–2:06,0 | **T29**: el Mirador de noche; ella y Órbita junto al telescopio, la Luna sobre la ciudad. Cámara del juego, quieta | — | Grillos. La música crece desde 2:03 y está plena en 2:06 | «La próxima ingeniera… Jugando.» |

### Cierre · 2:06–2:30 · sin voz

| N.º | Entra–Sale | Qué se ve | Rótulo | Sonido |
|---|---|---|---|---|
| S41 | 2:06,0–2:08,5 | `Construccion/Capturas/vuelta3_seis_escenas.jpg`, paneo lento (o un corte de T01, T03, T04, T05) | «5 escenarios jugables» | Música plena |
| S42 | 2:08,5–2:11,0 | `Construccion/Capturas/vuelta6_arcade_nueve.jpg`, acercamiento lento | «9 minijuegos arcade» | Música |
| S43 | 2:11,0–2:13,5 | T09 (el cuaderno abierto) | «55 fichas con su fuente» | Música |
| S44 | 2:13,5–2:16,0 | `Misión Artemis/capturas/13_marte_base.png` (o T26) | «2 bases: Luna y Marte» | Música |
| S45 | 2:16,0–2:18,5 | `Propuestas/Capturas/luna_telescopio.png` | «Datos: LRO y JPL Horizons» | Música |
| S46 | 2:18,5–2:22,0 | **G04**: tarjeta del equipo sobre la lámina de hojas desenfocada | «Guillermo · Jean · Joel · Domenica» | Música |
| S47 | 2:22,0–2:26,0 | **Última imagen — T30**: el Mirador de noche; la cámara se aleja (tecla X) y queda ella, pequeña, frente a la Luna. Si no se graba: `Lote_09/L09d_K13a_final.png` con sello IA | — | El tema llega a su acorde final |
| S48 | 2:26,0–2:30,0 | **G01** al revés: la imagen se cierra en un punto de luz ámbar; queda el título y funde a negro en 2:29,5 | «Luz cenicienta» | Cola del acorde; 0,5 s de silencio al final |

## 4. Tomas por capturar

Se graban con el modo de película de Godot por `herramientas/juego_ejecutar.py` (candado global; no abrir otro Godot): `python -I herramientas/juego_ejecutar.py --pelicula=<archivo>.avi --pantalla_completa --resolucion=1920x1080 --fps=30 -- --zona=<id> ...`. Para mover a la protagonista con teclas, un guion **nuevo** en `juego/pruebas/demo_<toma>.gd` que imite el estilo de `--prueba=manos` (teclas reales con `Input.parse_input_event`). Si el texto de ayuda de controles del pie de pantalla estorba, se recorta en el montaje (franja inferior de 30 px). Los juegos de los compañeros se graban con `--proyecto=` y su modo `--prueba` (sin tocar sus carpetas). Material crudo a `Nasa_Game/Presentacion/material/`.

| Id | Dónde | Qué tiene que pasar | Dura | Plano |
|---|---|---|---:|---|
| T01 | `--zona=habitacion` (mañana) | Ella cruza la alfombra hacia el banco; Órbita la sigue con su correa. Luz de mañana | 8 s | S10 |
| T02 | `--zona=habitacion` | Se gira hacia Órbita y pulsa E: globo con la pista | 5 s | S11 |
| T03 | `--zona=ciudad` | Cruza la Plaza de las Iguanas en diagonal hacia la biblioteca | 5 s | S12 |
| T04 | `--zona=sendero` | Sube la escalera hacia la hierba; minimapa con el destino visible | 4 s | S13 |
| T05 | `--zona=mirador` (noche) | Camina entre faroles y luciérnagas hacia el telescopio; minimapa visible. Una pasada aparte con `--medir=5` para el contador de fps | 4 s | S15, S39 |
| T06 | cualquier zona, tecla M | Abre el mapa del mundo y recorre los cinco lugares | 3 s | S17 |
| T07 | umbral Sendero → Mirador | La pantalla de carga pintada con su movimiento lento | 3 s | S14 |
| T08 | `--zona=mirador` | Se acerca al telescopio y lo usa (E) | 2 s | S18 |
| T09 | cualquier zona, Tab | Abre el cuaderno y pasa tres fichas despacio (que se lea «Fuente») | 5 s | S21, S43 |
| T11–T19 | `--minijuego=<id>` (seguidor, antena, satelite, telescopio, linea_tiempo, muestras, banderas, regreso, orbita) | El momento de más acción de cada uno (ver S23 a S31), en dificultad 1; con su sonido. Se puede usar `--auto` | 3 s c/u | S23–S31 |
| T20 | `--zona=luna` | Salto lento a baja gravedad con Órbita al lado | 3 s | S16 |
| T21 | `--proyecto=pruebas/luna_telescopio` (opcional) | La Luna real girando apenas en el ocular | 5 s | S19 |
| T22a | Misión Artemis, inicio | La base con la cúpula y el personaje | 3 s | S32 |
| T22 | Misión Artemis | Aviso de lluvia solar, carrera a la cúpula; las cuatro barras visibles | 5 s | S34 |
| T23 | Misión Artemis | Rover y extracción de hielo (mantener E) | 3 s | S33 |
| T24 | Misión Artemis | Despegue del cohete y viaje | 4 s | S36 |
| T25 | Misión Artemis — Marte, desde el inicio del capítulo | Programar el aterrizaje, el simulador y el resultado con su causa | 6 s | S35 |
| T26 | Misión Artemis — Marte, `--capitulo=superficie` | La base con paneles e invernadero; tormenta de polvo | 3 s | S44 |
| T27 | `--prueba=recorrido_manos` con ventana, y la salida de la consola | El juego jugándose solo + el registro con `PRUEBA_OK`. Guardar el registro de texto: alimenta G05 | 5 s | S38 |
| T28 | Cámara de teléfono, fuera del motor | El portátil real con el juego corriendo, sin mostrar datos personales en pantalla | 5 s | S39 |
| T29 | `--zona=mirador` (noche) | Ella y Órbita quietos junto al telescopio, la Luna sobre la ciudad | 6 s | S40 |
| T30 | `--zona=mirador` (noche) | Igual que T29, alejando la cámara con X | 4 s | S47 |

## 5. Gráficos propios (`Nasa_Game/Presentacion/graficos/`)

| Id | Qué | Datos |
|---|---|---|
| G01 | Título «Luz cenicienta»: un punto de luz ámbar `#F4A159` que se abre sobre negro (y su versión al revés para el cierre) | Paleta de `Fase_1_Arte/paleta_maestra.png` |
| G02 | La Luna medida contra Horizons: dos discos lado a lado, cifras grandes | 12,15 % y 192,6° medidos; 12,2 % y 192,6° de JPL Horizons (`trabajos.md`, 2026-11-12; `juego/minijuegos/telescopio/datos/luna.json`) |
| G03 | Tríptico concepto → hoja → motor, con flechas finas | Las tres imágenes de S37 |
| G04 | Tarjeta del equipo | Solo los nombres de pila: Guillermo, Jean, Joel y Domenica |
| G05 | Panel de registro de pruebas, con texto real de T27 | Salida real de la consola, sin rutas personales |

## 6. Audio

**Mezcla.** Pleno (gancho, montaje y cierre): −14 LUFS integrados, picos a −1 dBTP. Bajo la voz del expositor: música a −20 dB del nivel pleno y efectos a −12 dB; rampas de 0,4 s. El expositor habla en vivo: en los tramos con voz no puede haber nada que compita con las palabras (sin melodías al frente).

**Música** (pedido para el agente de audio, cotizar antes; tope del demo: 40 créditos). Un tema propio de 2:30, cálido y orquestal con un pulso electrónico suave, que ecoe las notas sueltas de la cinemática: notas aisladas en el gancho (0:11 y 0:13), cama sin melodía al frente bajo la voz, una sección rítmica de 12 s para el montaje (1:10–1:22) y un crescendo con acorde final para el cierre (2:06–2:30). Sin parecido buscado con ninguna banda sonora existente.

**Efectos.** Del juego: `juego/audio/` (paso, paso_luna, salto, recoger, umbral, logro, pagina, radio, golpe_mastil, ambiente_luna, ambiente_sendero). Por generar o tomar de `Fase_4_Audio/Lote_A1/originales/`: golpe grave de ignición (2 s), rugido de cohete (6 s), riser (3 s), siseo de televisor (4 s), alarma corta (2 s), viento y agua (4 s), grillos (6 s).

## 7. Dudas para Guillermo

1. **Nombre oficial del reto y del evento.** El reto global de 2026 se llama «Space Mission Design Game»; el enunciado de la carpeta dice «Tu primera base espacial». ¿Cuál se nombra? ¿Se puede escribir «NASA Space Apps Challenge 2026 · Guayaquil» en texto plano en el cierre?
2. **Nombre del equipo.** ¿Tiene nombre? Hoy el cierre solo lleva los cuatro nombres de pila.
3. **Video de 30 s.** La guía global de Space Apps limita el video de envío a 30 s. ¿Hacemos también un corte de 30 s (gancho + montaje + cierre)?
4. **Ortografía:** el LEEME de Marte escribe «Doménica»; en los encargos va «Domenica». ¿Cuál va en pantalla?
5. **Bandera de IEEE IAS — ESPOL** en el juego de Marte: ¿se puede mostrar en el video, o se evita ese plano?
6. **Uso de IA.** El arte de concepto, la cinemática, la música y los efectos salieron de modelos de IA (Higgsfield), y buena parte del código se escribió con asistentes. ¿Cómo quiere declararlo ante el jurado (las reglas de Space Apps piden transparencia)?
7. **Créditos de la cinemática.** Si los clips no llegan a tiempo, el gancho va con fotogramas fijos animados: ¿le parece bien?
8. ¿Puede filmar T28 (el portátil corriendo el juego) con su teléfono?
