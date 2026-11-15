# Lote 10 · Video de los movimientos I y II

> Cinemática de apertura «Un punto de luz». Movimiento I «La torre» (P03 a P06) y movimiento II «El vacío» (P07 a P09).
> Estado al 2026-11-15, 12:10: **generado y montado.** Ocho tomas (280,00 créditos) y un montaje provisional de 52 s para el director: `montaje_mov_I_II.mp4`. Ver §7. (A las 09:40 estaba solo preparado y cotizado.)
> Fuentes: [[Storyboard - Cinematica de apertura]] (§2 encargos, §5.4 reparto, §10 color, §11 fotografía) y [[03_produccion_higgsfield]] (§1 a §3).
> Saldo de la cuenta en este momento (`account status`): **742,25 créditos**. Ya no son los 849,50 del encargo: el lote 09b de fotogramas finales se cobró entre medias.

## 1. Plan y costo

Un intento por toma, cotizado de verdad con su fotograma inicial real (`generate cost`, 0 créditos). Las tarifas coinciden con las del storyboard (§5.4): ninguna cambió.

| Plano | Modelo | s | Resolución | Fotograma inicial | Fotograma final | Créditos por toma |
|---|---|---:|---|---|---|---:|
| P03 La torre | `minimax_h3` | 10 | 2K (única) | `Lote_09/L09b_K03_final.png` | — | 20,00 |
| P04 ★ La ignición | `seedance_2_5` | 8 | 720p | `Lote_09/L09b_K04a_final_r1.png` | `Lote_09/L09b_K04b_final.png` | 56,00 |
| P05 La columna | `seedance_2_5` | 8 | 720p | `Lote_10/fotogramas/L10_K05_placas_lisas.png` (retoque de K05) | — | 56,00 |
| P06 La chispa | `minimax_h3` | 6 | 2K | `Lote_09/L09b_K06_final.png` | — | 12,00 |
| P07 La Tierra | fija + ffmpeg | 8 | — | **K07 no apto** (ver §2) | — | 0,00 |
| P08 La Luna crece | `minimax_h3` | 6 | 2K | `Lote_09/L09b_K08_final.png` | — | 12,00 |
| P09 La sombra | `seedance_2_5` | 8 | 720p | `Lote_09/L09b_K09_final.png` | — | 56,00 |
| **Una pasada** | | | | | | **212,00** |

| Movimiento | Una pasada | Con los intentos del storyboard (§5.4) |
|---|---:|---:|
| I (P03 a P06) | 144,00 | 244,00 (P04 ×2; P03, P05 y P06 ×1,5) |
| II (P08 y P09) | 68,00 | 102,00 (×1,5) |
| **Total** | **212,00** | **346,00** |

- Saldo tras una pasada: 530,25. Tras los intentos previstos: 396,25.
- Orden de lanzamiento recomendado: P04 primero (es el héroe y el de más riesgo, ver §2), después P03, P05 y P06; el movimiento II tras validar el I. Una toma cada vez: cada clip se revisa antes de gastar en el siguiente.
- Sin audio generado: Seedance 2.5 va con `--generate_audio false`; MiniMax H3 no tiene ese parámetro (su pista, si la trae, se quita con `-an` al montar).
- El escalado a 1080p no es de este lote.

## 2. Estado de cada fotograma

Revisados reducidos y con recortes al 200 % (las placas de los autos, al 400 %): cohete, torre, autos, personas, módulo y superficie.

| Fotograma | Veredicto | Motivo y notas |
|---|---|---|
| K03 | **Apto** | Sin letras ni marcas en el cohete, la torre ni los autos; las placas, lisas al 400 %. Siluetas de espaldas, sin rostros; autos y ropa de los sesenta. Hereda del borrador aprobado dos desvíos de composición: las siluetas miden un 16 % del alto (el encargo pedía menos del 5 %) y el cohete, un 24 % (pedía 1/6), en x ≈ 0,64 |
| K04a (primero) | Reserva | `lote_09b_r3.json` dice que abría el encuadre, pero el archivo que hay hoy en disco tiene el mismo encuadre que K04b. Se usa r1, la versión vigente |
| K04a_r1 | **Apto** | Mismo encuadre, luz y color que K04b; sin fuego; una hebra de vapor. Sin marcas |
| K04b | **Apto, con riesgo** | Sin marcas; fuego como único color saturado. Notas: 1) el cohete está en x ≈ 0,50, no en 0,60, y la torre a su derecha (§11.3 la pone a la izquierda; coincide con K03 y con el borrador aprobado); 2) el cohete lleva cuatro cohetes laterales en la base, como el borrador aprobado, que no son de la silueta de 1969; 3) entre K04a_r1 y K04b la base sube unos 70 px (un 6 % del cohete) pero la punta queda en el mismo sitio: el modelo puede «encoger» el cohete en vez de elevarlo. Se ve en el primer clip |
| K05 original | No apto tal cual | Las dos placas traseras llevan seudoletras («Z8B9»…) visibles al 400 % |
| K05 retocado | **Apto** | `Lote_10/fotogramas/L10_K05_placas_lisas.png`: las dos placas, lisas (relleno con su color medio y desenfoque de 1 px; 0 créditos). Columna en x ≈ 0,59; siluetas de espaldas sin rostros; sin marcas |
| K06 | **Apto** | Chispa en (0,616; 0,345), en la cima del arco. Solo cielo y estela |
| K07 y K07_r1 | **No aptos** | El globo se corta por abajo en los dos: mide 1412 px de diámetro y su borde inferior caería en y ≈ 1870, fuera del cuadro de 1520 (un 25 % del disco no está). El alejamiento de P07 (del 100 % al 42 %) dejaría ver el corte recto. Por lo demás, limpios: sin costas nítidas, sin estrellas, cima iluminada en (0,61; 0,30). **P07 no se monta todavía.** Remedio: un K07 con el disco al 45 % del alto, o ampliar el lienzo hacia abajo; se cotiza aparte |
| K08 | **Apto** | Cima del limbo en (0,56; 0,33); terminador a la izquierda; cielo negro sin estrellas ni Tierra |
| K09 | **Apto** | Sombra de cuatro patas que entra desde abajo al centro; rayos de polvo rectos; sin huellas, banderas ni personas; la nave no aparece |

## 3. Encargos de movimiento

Copiados tal cual de §2 del storyboard (M03, M04, M05, M06, M08 y M09). Solo cambia el final: el «No text.» se sustituye por la protección de su fotograma y la protección fija «No text, no logos, no insignia, no emblems, no watermark.». Ninguno nombra a la agencia, la misión, personas, marcas ni obras.

| Plano | Protección añadida antes de la fija |
|---|---|
| P03 | No markings, letters, flags or symbols on the rocket, the tower or the cars. |
| P04 | No markings, letters, flags or symbols on the rocket or the tower. |
| P05 | No markings, letters, flags or symbols anywhere, and plain blank licence plates on the cars. |
| P06, P08 | (solo la fija) |
| P09 | No footprints, no flags, no people. |

Texto completo de cada toma: `tomas_movimientos_I_II.json` (en esta carpeta).

## 4. Línea de comandos

Herramienta: `herramientas/hf_video.py` (por defecto solo cotiza; crear exige `--generar` y un tope).

```text
# cotizar las seis (0 creditos)
python herramientas/hf_video.py --lote "Nasa_Game/Fase_1_Arte/Exploracion/Lote_10/tomas_movimientos_I_II.json" --solo-cotizar --mostrar-comando
# generar una toma (gasta); el tope del lote es 212
python herramientas/hf_video.py --lote "Nasa_Game/Fase_1_Arte/Exploracion/Lote_10/tomas_movimientos_I_II.json" --solo L10_P04_t1 --generar
# si la espera de 20 min se agota, recuperar sin gastar
python herramientas/hf_video.py --id L10_P04_t1 --recuperar <job_id>
```

Parámetros exactos que salen (ids de subida en `subidas_video.json`; subir no gasta):

| Toma | Parámetros |
|---|---|
| L10_P03_t1 | `minimax_h3 --start-image eb7d9bb4-5d21-4318-89fe-ed38f325271c --duration 10 --resolution 2K --aspect_ratio 16:9` |
| L10_P04_t1 | `seedance_2_5 --start-image 70828163-2fd3-4b9a-8291-da52e10fbabd --end-image c852ac76-4c4a-4257-a437-f96e41bd275b --duration 8 --resolution 720p --aspect_ratio 16:9 --mode omni_reference --generate_audio false` |
| L10_P05_t1 | `seedance_2_5 --start-image feeaea0d-ccc1-46f2-9604-d3446c7c18d5 --duration 8 --resolution 720p --aspect_ratio 16:9 --mode omni_reference --generate_audio false` |
| L10_P06_t1 | `minimax_h3 --start-image 135381f3-63ad-4d70-b5cc-7d89c68bea47 --duration 6 --resolution 2K --aspect_ratio 16:9` |
| L10_P08_t1 | `minimax_h3 --start-image f8378298-f648-47c9-85b2-4c1b28bce0d1 --duration 6 --resolution 2K --aspect_ratio 16:9` |
| L10_P09_t1 | `seedance_2_5 --start-image 2b17ee88-159c-4a29-9737-2591208afcc2 --duration 8 --resolution 720p --aspect_ratio 16:9 --mode omni_reference --generate_audio false` |

Todas llevan además `--prompt "<encargo>" --wait --wait-timeout 20m --json`.

**Parámetros comprobados** con `higgsfield model get <modelo> --json` (2026-11-15):
- `seedance_2_5`: `start_image` y `end_image` solo con `mode: omni_reference`; `duration` entera; `resolution` 480p, 720p, 1080p o 4k; `aspect_ratio` 16:9 por defecto; `generate_audio` verdadero por defecto (apagarlo no cambia el precio).
- `minimax_h3`: `start_image` y `end_image` (el final exige el inicial y no se mezclan con referencias); `duration` entera; `resolution` solo «2K»; `aspect_ratio` «auto» por defecto, por eso se fija 16:9; sin parámetro de audio; `batch_size` 1 por defecto.

## 5. Herramienta y registro

- `herramientas/hf_video.py`: valida modelo, resolución, duración y que el encargo termine con la protección fija y no nombre a la agencia, la misión ni personas reales; sube los fotogramas una vez (JPEG de calidad 95); cotiza; con `--generar` comprueba el tope, crea el trabajo con `--wait` (20 min), guarda la respuesta cruda en `_json/<id>.json`, baja `result_url` (el original, no la miniatura) a `clips/<id>.mp4`, añade la fila a `registro_video.json` (id del trabajo, modelo, parámetros, encargo, costo, saldo antes y después, archivo, veredicto) y monta la revisión en `revision/<id>/`: un cuadro cada 0,5 s, hoja de contacto, y el primer, el medio y el último cuadro a tamaño completo.
- Probada solo cotizando (las seis tomas, 212,00) y con `--revisar` sobre un clip de prueba sintético (borrado después).
- No toca `herramientas/hf_generar.py` ni el lote 09.

## 6. Pendiente

- [ ] Partida de video del director para los movimientos I y II (una pasada 212,00; con intentos 346,00).
- [ ] P07: nuevo K07 con el globo entero (cotizar aparte).
- [ ] Tras el primer clip de P04, decidir si se sigue con el fotograma final o solo con el inicial, según cómo resuelva la subida del cohete.
- [ ] Revisar cada clip con su hoja de contacto antes de montarlo (letras, insignias, banderas y rostros que el modelo pueda añadir a mitad de toma).

## P04

- **Tomas: 1. Costo: 56,00 créditos** (cotizado 56,00; trabajo `9488c3fd-b1c3-41ed-b02f-4cf7462eecff`, creado a las 09:19 y bajado de `result_url` con `--recuperar`, sin volver a generar). No se lanzó segunda toma: la primera pasa la lista y no hay un cambio concreto del encargo que la mejore con claridad.
- Modelo y parámetros: `seedance_2_5`, 8 s, 720p, 16:9, `omni_reference`, inicial K04a_r1 y final K04b, sin audio. Encargo: M04 del storyboard con la protección de P04. Semilla del servidor: 1792444174.
- Clip: 1280 × 720, 24 cps, 193 cuadros, 8,04 s. Elegido: `clips/P04_elegido.mp4` (copia de `clips/L10_P04_t1.mp4`). Hoja: `clips/P04_hoja.jpg`; revisión completa en `revision/L10_P04_t1/` (cuadros, primero, medio, último, recortes del cohete y comparación con K04b).

| Comprobación | Resultado |
|---|---|
| Fotogramas inicial y final | El primer cuadro es K04a_r1; el último coincide con K04b (encuadre, fuego, vapor a los dos lados y altura del cohete) |
| Cámara | Fija: torre, plataforma, marisma y agua no se mueven en los 8 s |
| Ritmo | 0 a 1,5 s: quietud con la hebra de vapor. 1,5 s: punto naranja en la base. 1,5 a 5 s: el fuego crece y el vapor ámbar se abre en horizontal por el tercio inferior. 5,0 s: el morro empieza a subir (medido cuadro a cuadro: quieto en y = 100 hasta el cuadro 120) y acelera hasta y = 60 en el último. Cae justo en el golpe grave de 0:29 |
| Escala del despegue | Sube unos 40 px, un 8 % de su altura: menos de un quinto, como pide M04. Se lee como despegue lento y pesado, sin tirones |
| Letras, insignias, banderas, caras | Ninguna. El cohete y la torre siguen lisos |
| Defectos | Sin parpadeo (la luminancia media cambia como mucho 0,42 niveles entre cuadros). Sin fundidos ni piezas que aparezcan. El vapor se comporta como vapor (estamos en la Tierra) |
| Corte a P05 | El último cuadro tiene el cohete recién despegado con la llama blanca bajo la base: sirve para cortar a la columna |

**Veredicto: apto, elegido.** Problemas que quedan, ninguno bloqueante:
1. El riesgo previsto de K04b se cumplió a medias: el cuerpo conserva su tamaño, pero el tramo inferior de los propulsores se acorta unos 35 px (a 720p) en los últimos 2 s; la llama lo tapa casi entero.
2. Los brazos de la torre tienen un enrejado que al 200 % parece seudoletras; a tamaño real se lee como celosía. Viene de los fotogramas K04a y K04b. **Resuelto con un parche sin costo** (ver la segunda pasada, más abajo).
3. Heredados de K04b: el cohete en x ≈ 0,50 con la torre a su derecha (§11.3 pedía x = 0,60 y la torre a la izquierda) y los cuatro cohetes laterales.
4. El despegue es el 8 % de la altura, no el quinto completo que nombra §11.3 para el corte; si en el montaje hace falta más subida, se usan los 8 s enteros en vez de 7.

### P04 · Segunda pasada: parche de los brazos (2026-11-15, 0 créditos)

Un crítico independiente marcó el punto 2 como falta de la regla de letras (gravedad media): los tres brazos de la torre llevan un enrejado oscuro con trazos claros que forman seudoletras (x ≈ 0,52 a 0,58; y ≈ 0,23, 0,38 y 0,54). Vienen de K04a y K04b, así que otra toma de Seedance con los mismos fotogramas las repetiría. **No se generó una segunda toma** (quedan sin gastar los 56 créditos de la partida): se arregló en posproducción, como proponía el crítico.

- **Por qué no un parche fijo.** Se midió el color de los brazos en los 193 cuadros: con el fuego y la calima, el brazo inferior pasa de R 123 a 178 en los últimos 3 s y los otros dos suben unos 25 niveles. Un PNG fijo del cuadro 0 quedaría frío y oscuro encima del resplandor.
- **Qué se hizo.** Se usó un parche por cuadro (`revision/L10_P04_t1_parche/parche_brazos.py`, con numpy y ffmpeg). En cada brazo, solo la franja de las marcas (x 668 a 740 a 720p; filas 168 a 175, 270 a 278 y 383 a 390) se pinta como una celosía regular: diagonales en V cada 12 px con un montante, y desenfoque 1-2-1 para igualar la suavidad del video. El color sale de cada cuadro: los cordones oscuros del propio brazo como fondo y el cielo de encima para las diagonales (34 %), suavizado en 9 px y en 7 cuadros. El parche lleva 3 px de fundido en los extremos y un grano de σ 1,6. Los cordones, las barandillas, los tirantes de abajo y la unión con la torre no se tocan. El cohete (borde en x ≈ 660) queda fuera del parche en todos los cuadros.
- **Codificación.** libx264 con crf 12, preset slow, yuv420p y High, a 24 cps: 193 cuadros, 8,04 s, 3,6 MB. Fuera del parche no cambia nada: PSNR de 46,0 dB contra la t1.

| Comprobación | Resultado |
|---|---|
| Seudoletras | No queda ninguna en los tres brazos al 400 % a 720p ni a 1080p (escalado lanczos), en los cuadros 1, 97, 150 y 193 (`brazos_400_antes.png`, `brazos_400_parche.png` y `brazos_1080_parche.png`). Se lee una celosía lisa |
| Resplandor | El parche se calienta con el entorno: en el cuadro 193 el brazo inferior queda ámbar como la torre de alrededor, sin una mancha fría encima |
| Parpadeo | El salto máximo entre cuadros dentro del parche es de 1,04 a 1,05 niveles; en la t1 era de 1,10 a 1,66. Queda más estable que el original |
| Resto del clip | La hoja de contacto (un cuadro cada 0,5 s) y los cuadros primero, medio y último a tamaño completo coinciden con la t1: el mismo ritmo, el mismo despegue a los 5,0 s y la misma cámara fija. No hay letras, banderas ni caras |

**Veredicto: t1 con el parche, elegida.** `clips/P04_elegido.mp4` es ahora una copia de `clips/L10_P04_t1_parche.mp4`; el original sigue en `clips/L10_P04_t1.mp4`. Hoja: `clips/P04_hoja.jpg`. La revisión está en `revision/L10_P04_t1_parche/`. Siguen abiertos los puntos 1, 3 y 4 de arriba. Otra nota: el brazo pequeño de x ≈ 0,56 a 0,58 e y ≈ 0,69 tiene una barandilla con trazos irregulares; al 400 % no forma letras y el crítico no la señaló, pero conviene mirarla tras el escalado a 1080p.

## P03

- **Tomas: 1. Costo: 20,00 créditos** (cotizado 20,00; trabajo `25afe816-f41a-457d-a7b4-e0adb6c6c211`, creado a las 09:19 y bajado de `result_url` con `--recuperar`, sin volver a generar). No se lanzó una segunda toma: la primera pasa la lista, y lo que le falta (la calima) se resuelve mejor en posproducción que con otro intento, que además podría mover las siluetas.
- Modelo y parámetros: `minimax_h3`, 10 s, 2K, 16:9, solo con el fotograma inicial K03. Encargo: M03 del storyboard con la protección de P03.
- Clip: 2560 × 1440, 24 cps, 243 cuadros, 10,12 s y 1,5 MB. Trae una pista AAC que se quita con `-an` al montar. Elegido: `clips/P03_elegido.mp4` (copia byte a byte de `clips/L10_P03_t1.mp4`, mismo SHA-256). Hoja: `clips/P03_hoja.jpg`. La revisión completa (cuadros y los cuadros primero, medio y último) está en `revision/L10_P03_t1/`.

| Comprobación | Resultado |
|---|---|
| Fotograma inicial | El primer cuadro es K03: diferencia RMS de 3,3 niveles contra el fotograma escalado. El encuadre, las siete siluetas, los dos autos, el cohete, la torre y el reflejo son los mismos |
| Cámara | Fija los 10 s: el cielo cambia como mucho 0,98 niveles frente al primer cuadro y la orilla lejana, 1,47. Ni zoom ni deriva |
| Sujetos | Nadie se mueve: la diferencia entre el primer y el último cuadro solo marca los contornos (bordes por debajo del píxel, iguales en todas las figuras), con 2,6 niveles como máximo. El agua sigue como un espejo (2,0 como máximo) |
| Vapor | Una hebra blanca de venteo sale del costado del cohete, hacia la torre, a la altura del brazo superior. Aparece hacia 1,0 s, se abre y se riza de 3 a 6 s y se disuelve del todo hacia 7,0 s. Se comporta como vapor a contraluz, sin chorro ni fuego |
| Calima | Casi imperceptible: el temblor del cohete y la torre (0,77 niveles de media entre cuadros) es igual al del resto del cuadro. No se lee el «aire que tiembla» |
| Letras, insignias, banderas, caras | Ninguna. Las placas de los autos son rectángulos lisos, todas las figuras están de espaldas y el cohete y la torre siguen lisos |
| Defectos | Sin parpadeo: la luminancia media baja de forma suave de 172,9 a 172,3. Ningún objeto aparece, se funde ni se deforma |
| Corte a P04 | El último cuadro vuelve al estado de K03, sin vapor: el corte en el eje a K04a (mismo eje, sin fuego) queda limpio. Cualquier ventana de 9 s sirve para el montaje |

**Veredicto: apto, elegido.** Problemas que quedan, ninguno bloqueante:
1. **Calima casi ausente.** El storyboard pide que el aire tiemble (§2 M03 y §11). Se propone hacerla en el pase de posproducción con un desplazamiento horizontal suave, limitado a la franja del horizonte, del cohete y de su reflejo. Es más controlable que otra toma de 20 créditos.
2. **Vapor algo denso.** Es más brillante que el casco del cohete y se queda entre el cohete y la torre en vez de irse de lado. A tamaño real se lee como venteo, pero si el director lo quiere más tenue, se baja en el etalonaje con una máscara local o se monta la ventana de 1 a 10 s.
3. **Bitrate bajo** (unos 1,2 Mb/s a 2560 × 1440): el cielo aguanta, pero conviene revisar el bandeado del degradado tras el escalado y el grano de 16 mm.
4. Desvíos heredados de K03 y de su borrador aprobado: las siluetas miden un 16 % del alto (el encargo pedía menos del 5 %) y el cohete un 24 % (pedía 1/6), en x ≈ 0,64.

## P05

- **Tomas: 1. Costo: 56,00 créditos** (cotizado 56,00; trabajo `2c087629-2d06-4c6f-baa4-21cba340dea7`, creado a las 10:25 sin `--wait`, con el id anotado en el registro antes de esperar, y bajado de `result_url` con `--recuperar`). No había ninguna toma anterior de P05 en la cuenta ni en el registro. Dos cotizaciones previas fallaron por un error intermitente del servidor («Unsupported validation rules…») sin crear trabajo. No se lanzó una segunda toma: la primera pasa la lista y lo único que se desvía, la velocidad, no justifica otros 56.
- Modelo y parámetros: `seedance_2_5`, 8 s, 720p, 16:9, `omni_reference`, solo con el fotograma inicial `fotogramas/L10_K05_placas_lisas.png` (subida `feeaea0d…`), sin audio. Encargo: M05 del storyboard, más «No markings, letters, flags or symbols anywhere, and plain blank licence plates on the cars» y la protección fija (`encargos/M05_t1.txt`).
- Clip: 1280 × 720, 24 cps, 193 cuadros y 8,04 s. Elegido: `clips/P05_elegido.mp4` (copia byte a byte de `clips/L10_P05_t1.mp4`, mismo hash). Hoja: `clips/P05_hoja.jpg`. La revisión completa está en `revision/L10_P05_t1/`: cuadros, primero, medio y último, más los recortes `llama.png` y `siluetas.png`.

| Comprobación | Resultado |
|---|---|
| Fotograma inicial | El primer cuadro es K05 con las placas lisas: el mismo encuadre, la columna, las dos siluetas sobre los coches, las cinco de pie y el reflejo |
| Cámara | Una sola inclinación hacia arriba, sin zoom: la distancia entre las dos siluetas de los coches es la misma (358 px) en el primer cuadro y en el del medio. Arranca suave (el horizonte baja 5 px por cada 0,25 s al principio y 15 px al final) y sale por abajo a los 5,4 s |
| Velocidad | Unos 5,6 % del alto por segundo de media, frente al 3 % pedido. Se lee como pesada y continua, sin tirones ni temblor |
| Sujeto | La llama queda pegada al borde superior desde el principio: la cámara la sigue y no la alcanza, y la punta sale del cuadro. El humo crece y rueda en masas lentas y la base se ensancha. Es humo, no líquido. La columna se mantiene en x ≈ 0,56 los 8 s |
| Siluetas y agua | Las siluetas no se mueven y están de espaldas, sin rostro. El agua sigue en calma y refleja el resplandor |
| Letras, insignias, banderas, caras | Ninguna. Las placas son rectángulos lisos (recorte al 200 %) |
| Defectos | Sin parpadeo: la luminancia media cambia como mucho 0,38 niveles entre cuadros consecutivos y baja de forma suave de 132 a 122 al entrar en el cielo. Nada aparece, se funde ni se deforma |
| Corte a P06 | El último cuadro es la columna crema que sale por arriba contra un cielo más azul y oscuro. Corta bien al cielo vacío de P06 y sigue el guion de color (§10: el cielo se oscurece hacia el espacio) |

**Veredicto: apto, elegido.** Problemas que quedan, ninguno bloqueante:
1. **Inclinación más rápida que la pedida** (5,6 %/s frente a 3 %/s). Desde los 5,4 s solo se ven la columna y el cielo. Con los 7 s del montaje, la orilla ocupa los primeros 5,4 s y quedan 1,6 s de columna sola, lo que deja el cuadro listo para cortar al cielo de P06. Si el director quiere más orilla, se ralentiza en posproducción entre 0 y 5,4 s (por ejemplo, al 80 %) en lugar de pagar otra toma.
2. **La llama no se lee como un punto propio**: está pegada al borde superior desde el primer cuadro (así viene en K05) y sale enseguida. El corte «en el movimiento» de §2 cae sobre la columna, no sobre la llama. Encaja con la intención de §11 («la sigue y no la alcanza»).
3. Desvío heredado de K05: la columna queda en x ≈ 0,56 a media altura y no en 0,60. Se puede corregir con un reencuadre del 2 % al escalar a 1080p.
4. Quedan para posproducción, como manda el storyboard, el temblor del 1 %, la arruga del agua y el grano de 16 mm.

## P06

- **Tomas: 2. Costo: 24,00 créditos** (12,00 cotizados por toma; trabajos `adf6b7be-7701-44fc-8b29-4981a3e0709b` (t1) y `d932a37a-6ec5-421b-8cb0-517d4a94a546` (t2)). Se crearon sin `--wait` y el id quedó en `registro_video.json` antes de esperar; se bajaron de `result_url` con `--recuperar`. Antes de generar se comprobó que no había ninguna toma de P06 en el registro, en `clips/` ni entre los trabajos de la cuenta.
- Modelo y parámetros: `minimax_h3`, 6 s, 2K, 16:9, solo con el fotograma inicial K06 (`135381f3-…`). Encargos en `encargos/M06_t1.txt` (M06 del storyboard con la protección) y `encargos/M06_t2.txt`.
- Aviso de la herramienta: la primera cotización devolvió «Unsupported validation rules for minimax_h3»; al repetirla, el mismo encargo cotizó 12. Es un fallo intermitente del servidor, no del encargo.
- Clip elegido: 2560 × 1440, 24 cps, 158 cuadros, 6,58 s y 1,8 MB. Trae pista AAC: se quita con `-an` al montar. Elegido: `clips/P06_elegido.mp4` (copia byte a byte de `clips/L10_P06_t2.mp4`, mismo SHA-256). Hoja: `clips/P06_hoja.jpg`. Revisión completa en `revision/L10_P06_t1/` y `revision/L10_P06_t2/`.

| Comprobación | t1 (encargo M06) | t2 (encargo ajustado) |
|---|---|---|
| Fotograma inicial | K06: chispa en (0,621; 0,347) | K06: chispa en (0,618; 0,345) |
| Chispa | No se detiene. Avanza 125 px (de x 0,621 a 0,670) y baja 12 px después de la cima, hasta el último cuadro. Se lee como que empieza a caer, justo lo que §2 prohíbe | Avanza 58 px frenando y **queda quieta de 4,5 a 6,5 s** en (0,641; 0,350). Se enciende en un destello redondo de 0,5 a 4,5 s y se encoge a un punto en los 2 s finales |
| Cielo | De 2 a 5 s se oscurece hasta negro violeta: arriba (26, 4, 33) y la luminancia media baja de 108 a 61. No es el índigo `#2B2F5A` de §10, y la estela se apaga con él | Constante, como en K06: arriba (46, 41, 92) y luminancia de 108,1 a 107,4. No se oscurece hacia el índigo pedido |
| Estela y viento | La parte baja se tuerce y forma rizos; bien | La parte baja se tuerce, adelgaza y se disuelve hacia la izquierda; la parte alta sigue unida a la chispa |
| Cámara | Fija | Fija |
| Letras, insignias, banderas, caras | Ninguna | Ninguna |
| Defectos | Ningún parpadeo, pero el cambio de luz es brusco (diferencia de hasta 9,4 niveles entre cuadros) | Sin parpadeo (diferencia máxima de 0,72 niveles entre cuadros). Nada aparece ni se funde |
| Corte a P07 | La chispa sigue moviéndose y queda en x 0,670, demasiado lejos de P★ | La chispa está quieta en el último segundo y medio: sirve para la disolvencia por forma |

Cambio de la t2: la t1 falló en dos puntos que se pueden escribir en el encargo, el desplazamiento de la chispa más allá de la cima y el cielo que se vuelve negro. La t2 pide que la chispa no se desplace, que se quede sobre el arco y que la exposición y los colores no cambien («the sky never turns black or purple»).

**Veredicto: t2 apta y elegida.** Es la que respeta la regla principal del plano: la chispa llega a la cima y se queda en ella sin caer. Problemas que quedan, ninguno bloqueante:
1. **Destello grande** de la chispa de 0,5 a 4,5 s (un halo de unos 40 px a 2560): se lee como el sol reflejado en la nave. La firma del punto de luz (§10.2) se iba a poner en posproducción; hay que decidir si se aprovecha este destello o se suaviza con una máscara para que no compita con la firma. En los 2 s finales ya es un punto.
2. **Posición:** la chispa termina en (0,641; 0,350), no en P★ (0,60; 0,36). Se arregla en posproducción con un reencuadre de unos 105 px a 2560 (escalar un 4 % y desplazar), sin costo. Así también coincide con la cima del disco de K07.
3. **El cielo no pasa al índigo** que pide §10 (de `#B9CBD6` a `#2B2F5A`). Se hace en el etalonaje con un degradado animado en la mitad superior. Es más controlable que el oscurecimiento de la t1, que también apagaba la estela.
4. La parte baja de la estela casi desaparece en el último segundo; en la disolvencia a P07 eso ayuda, porque solo queda el arco alto.
5. El bitrate es bajo (unos 1,0 Mb/s a 2560 × 1440). Conviene revisar el bandeado del degradado del cielo tras el escalado y el grano de 16 mm.

## P08

- **Tomas: 1. Costo: 12,00 créditos** (cotizado 12,00; saldo de 548,70 a 536,70). Trabajo `c2629880-6694-47ce-9523-2714f3bc22a1`, creado sin `--wait` con el id anotado en `registro_video.json` antes de esperar, y bajado de `result_url` con `--recuperar`. Antes de generar se comprobó que no había ninguna toma de P08 en el registro, en `clips/` ni entre los trabajos de la cuenta (la subida de K08, `f8378298…`, no aparecía en ningún trabajo). No se lanzó una segunda toma: la primera pasa la lista y lo que queda no se arregla con un cambio concreto del encargo.
- Modelo y parámetros: `minimax_h3`, 6 s, 2K, 16:9, solo con el fotograma inicial K08 (`Lote_09/L09b_K08_final.png`). Encargo: M08 del storyboard con la protección fija (`encargos/M08_t1.txt`).
- Clip: 2560 × 1440, 24 cps, 158 cuadros, 6,58 s y 21,7 MB (unos 26 Mb/s, mucho más que P03 y P06). Trae una pista AAC que se quita con `-an` al montar. Elegido: `clips/P08_elegido.mp4` (copia byte a byte de `clips/L10_P08_t1.mp4`, mismo SHA-256). Hoja: `clips/P08_hoja.jpg`. Revisión completa en `revision/L10_P08_t1/`.

| Comprobación | Resultado |
|---|---|
| Fotograma inicial | El primer cuadro es K08: la cima del limbo está en (0,556; 0,325), el terminador a la izquierda y los mismos cráteres |
| Cámara | Deriva lateral continua: la superficie se desplaza unos 260 px a la derecha (un 10 % del ancho en 6,6 s, 1,6 %/s frente al 2 %/s pedido) y baja unos 140 px, con un acercamiento leve (un cráter de referencia pasa de 180 a 205 px, +14 %). El limbo casi no se mueve: la cima termina en (0,571; 0,368). Se lee como una nave que orbita y se acerca, no como un paneo sobre una foto |
| Velocidad | Constante: la diferencia media entre cuadros se mantiene entre 4,4 y 4,6 niveles en todo el clip, con un arranque apenas más suave (3,8). Sin aceleración ni tirones ni temblor |
| Luz | No cambia: el Sol sigue rasante desde la derecha y las sombras no se mueven sobre los cráteres. La luminancia media baja de 55,8 a 49,9 solo porque entra más zona en sombra; el salto máximo entre cuadros es 0,35 |
| Cielo | Negro absoluto en los cuadros 1, 7 y 13 (máximo 0 en la franja superior): sin estrellas, sin Tierra y sin nave |
| Letras, insignias, banderas, caras | Ninguna |
| Defectos | Sin parpadeo ni objetos que aparezcan o se fundan. A tamaño completo, las paredes de los cráteres llevan estrías finas tipo pincel y algunas sombras interiores tienen bordes dentados (ya estaban en K08; H3 las acentúa un poco hacia el final) |
| Corte a P09 | El último cuadro es limbo gris sobre negro, quieto y legible: sirve para el corte de gris a gris con P09 (la luminancia se iguala al 5 % en el montaje). El storyboard monta 4 de los 6 s: cualquier ventana sirve |

**Veredicto: apto, elegido.** Problemas que quedan, ninguno bloqueante:
1. **Deriva algo más lenta que la pedida** (1,6 %/s frente a 2 %/s) y con un descenso leve del limbo (4 % del alto). En los 4 s que se montan no se nota; si hace falta, se acelera un 20 % en posproducción.
2. **Estrías y sombras dentadas** en las paredes de los cráteres, sobre todo en la mitad izquierda hacia el final. A tamaño de pantalla se leen como relieve. Si molestan tras el escalado a 1080p, se monta la ventana de 0 a 4 s, que es la más limpia.
3. **La disolvencia de 2 a 3 s** desde el disco renderizado (§2) y el destello de 2 px de la nave por P★ siguen pendientes: van en posproducción, como manda el storyboard.

## P09

- **Tomas: 2. Costo: 112,00 créditos** (56,00 cotizados por toma; saldo de 536,70 a 424,70). Trabajos `18ef7b4e-1fe2-45aa-a451-7a372373548d` (t1) y `48763821-0aad-4f31-a8da-55db3b51a1bd` (t2). Los dos se crearon sin `--wait`, con el id anotado en `registro_video.json` antes de esperar, y se bajaron de `result_url` con `--recuperar`. Antes de generar se comprobó que no había ninguna toma de P09 en el registro, en `clips/` ni entre los trabajos de la cuenta. Las cotizaciones fallaron varias veces con el error intermitente «Unsupported validation rules for seedance_2_5», que no crea trabajo; al repetirlas dieron 56.
- Modelo y parámetros: `seedance_2_5`, 8 s, 720p, 16:9, `omni_reference`, sin audio, fotograma inicial K09 (`Lote_09/L09b_K09_final.png`, subida `2b17ee88…`). Encargos: `encargos/M09_t1.txt` (M09 del storyboard con «No footprints, no flags, no people» y la protección fija) y `encargos/M09_t2.txt`.
- Clips: 1280 × 720, 24 cps, 193 cuadros, 8,04 s, sin pista de audio. Elegido: `clips/P09_elegido.mp4` (copia byte a byte de `clips/L10_P09_t1.mp4`). Hoja: `clips/P09_hoja.jpg`. Revisión completa en `revision/L10_P09_t1/` y `revision/L10_P09_t2/` (con los recortes `zoom/`, `z/` y `j/`).

| Comprobación | t1 (elegida) | t2 (descartada) |
|---|---|---|
| Fotograma inicial | **No es K09** (RMSE 30,7 niveles a 320 × 180): el suelo empieza unos 65 px más arriba y la sombra es un 15 % más corta, con las cuatro zapatas a la vista. El clip **termina** en la composición de K09 (cráteres y zapatas en su sitio) | Tampoco es K09 (RMSE 32,2): sombra más pequeña y cuatro zapatas a la vista |
| Cámara | El suelo baja unos 60 px y la sombra crece un 17 % (las patas pasan de 400 a 470 px), sin girar. **No cambia la escala:** los cráteres no crecen, así que se lee como una deriva lenta y no como un descenso | El suelo no se mueve; solo crece la sombra. **A los 4,29 s la sombra vuelve de golpe a su tamaño inicial y crece otra vez:** un bucle visible |
| Ritmo y parada | Diferencia entre cuadros de 1,5 a 1,9 hasta los 2 s; frenada suave de 3 a 4,5 s; quieto (< 0,1) desde los 4,5 s hasta el final. Pide constante hasta los 7 s y parada seca | Movimiento irregular y el salto de los 4,29 s |
| Polvo | Rayos rectos y finos a ras del suelo, radiales desde debajo de la sombra; sin nube, sin bruma, sin remolino. Se mueven con el suelo, no salen disparados | Igual |
| Letras, insignias, banderas, huellas, caras, nave | Ninguna | Ninguna |
| Defectos | Sin parpadeo (luma de 97,1 a 96,0, en descenso suave) ni piezas que aparezcan o se fundan; la silueta de cuatro patas se conserva | El salto descalifica la toma |
| Corte a P10 | El final está quieto y nítido, sirve para el congelado del último segundo y el corte seco | — |

Cambio de la t2: pidió un descenso con escala («the craters, rocks and their shadows grow steadily larger… about three percent per second»), a velocidad constante los 8 s, para cortar y congelar en ffmpeg a los 7 s, que el primer cuadro fuera el de referencia y que el polvo se apagara al final. No funcionó: Seedance dejó el suelo fijo y volvió a empezar el crecimiento de la sombra a mitad del clip.

**Veredicto: t1 apta y elegida.** Es continua, sin saltos ni parpadeo, con la física del polvo correcta y el final quieto. Problemas que quedan:
1. **No hay descenso real:** la escala no cambia. En posproducción se puede añadir un acercamiento lento (escalar del 100 % al 108 % de 0 a 4,5 s sobre 1280 × 720) para que el suelo «se acerque»; conviene hacerlo después del escalado a 1080p.
2. **La parada es una frenada a los 4,5 s, no un corte seco a los 7 s.** Hay dos opciones de montaje, sin costo: (a) estirar el tramo de 0 a 4,0 s a unos 6,5 s con interpolación (`minterpolate`) y congelar el cuadro de corte, con lo que la parada queda seca y en su sitio, o (b) montarla tal cual, con 3,5 s de quietud, más de lo que pide el plano. Se recomienda la (a), que deja el contacto a 1:03 como manda la mezcla.
3. **El primer cuadro no es K09.** Nadie ve K09 antes de P09, así que no rompe la continuidad, pero el arranque tiene la sombra más corta que el fotograma aprobado.
4. **Corte desde P08:** P08 termina con una luminancia media de 50 y P09 empieza en 97. Hay que igualarla al 5 % en el etalonaje (§10, «corte de gris a gris»).
5. El polvo no «sale disparado»: los rayos viajan con el suelo. Si se quiere el disparo, se añade en posproducción (rayos radiales con desenfoque de movimiento de 1 cuadro) en los 3 s previos al contacto.

## 7. Montaje de los movimientos I y II (2026-11-15, 0 créditos)

- **Video:** `montaje_mov_I_II.mp4`. H.264 High, 1280 × 720, 24 cps, yuv420p, crf 14. Dura **52,000 s y tiene 1248 cuadros** (medido con ffprobe), de 0:15 a 1:07 de la cinemática. Sin textos y sin música. Lleva un tono de sala de ruido marrón con paso bajo de 300 Hz: media −60 dB y pico −46 dB.
- **Hoja de contacto:** `montaje_mov_I_II_hoja.jpg`, con un cuadro por segundo, tomado a mitad de cada segundo, y el plano y el minuto debajo.
- **Scripts y pruebas:** están en `montaje/`. `montar.py` arma los segmentos, `final.py` los une y `hoja.py` hace la hoja. También quedan la placa de la Tierra (`P07_placa_tierra.jpg`), la medición de luma P08→P09 (`luma.json`) y las dos disolvencias a tamaño completo (`disolvencias_29s_37s.png`).

### 7.1 Línea de tiempo montada

| Plano | Entra | Dura | Fuente y ventana | Arreglo en el montaje | Salida |
|---|---|---:|---|---|---|
| P03 | 0:15 | 9 s | `P03_elegido` (t1) de 0 a 9 s | Escalado de 2560 a 1280 con lanczos, sin audio | Corte en el eje |
| P04 | 0:24 | 7,5 s | `P04_elegido` (t1 con parche) de 0,5 a 8,0 s | Reencuadre del crítico: recorte de 1184 × 666 desde (0; 27) y escalado al 108 %. El cohete pasa de x 0,49 a 0,53. La ignición cae a 1,0 s del plano y el despegue a 4,5 s (0:28,5, junto al golpe grave de 0:29) | Corte seco |
| P05 | 0:31,5 | 6,5 s | `P05_elegido` (t1) de 0 a 6,5 s | Corte antes de que domine el humo «en coliflor», como pidió el crítico. P04 y P05 suman los mismos 14 s del storyboard (7,5 + 6,5 en vez de 7 + 7) | Corte seco |
| P06 | 0:38 | 6 s (+0,75) | `P06_elegido` (t2), entero, con el último cuadro sostenido 0,17 s | Reencuadre al 112 %: recorte de 2286 × 1286 desde (269; 41). La chispa queda en P★ (0,60; 0,36), justo en la cima del disco de P07 | **Disolvencia de 1,5 s** centrada en 0:44, de la estela al borde de la Tierra |
| P07 | 0:44 | 8 s (±0,75) | Placa hecha a partir de K07_r1 (ver §7.2) | Alejamiento del 60 % al 25 % del alto, con una curva exponencial (la velocidad aparente es constante). El borde superior queda fijo en P★. Se dibuja cuadro a cuadro con posición subpíxel y supermuestreo ×2, sin saltos | **Disolvencia de 1,5 s** centrada en 0:52, del disco azul al limbo gris |
| P08 | 0:52 | 6 s (+0,75) | `P08_elegido` (t1), entero | Escalado de 2560 a 1280, apenas más lento (×1,025) para llenar 6,75 s | Corte seco de gris a gris |
| P09 | 0:58 | 9 s | `P09_elegido` (t1) de 0 a 4,0 s | Opción B del crítico, sin las partículas. El tramo se estira a 5,0 s con `minterpolate` (mci y aobmc). Se añade un acercamiento constante del 100 % al 112 % hacia (0,50; 0,55), que **se detiene en seco a los 5 s (contacto a 1:03)**. Del último cuadro se hace un **congelado de 4 s** hasta 1:07. La ganancia ×1,115 iguala el gris de la superficie con el final de P08 (113,5 frente a 101,8) | Fin |

### 7.2 P07: la Tierra sin un K07 nuevo (provisional)

K07_r1 corta el globo por abajo. Para no gastar créditos, se armó una placa con el disco completo:

1. Círculo ajustado por mínimos cuadrados al borde iluminado: centro (1617; 1186), radio 732 px y desviación de 2,2 px.
2. El casquete que falta, desde 30 filas antes del corte (las últimas filas de K07 vienen estiradas), se rellena con el espejo del hemisferio norte sobre el ecuador del disco. Ese espejo tiene el mismo radio, así que el borde y la atmósfera casan. El paso se funde en 140 px.
3. La mitad baja se recorta al círculo, con un halo azul de 14 px.
4. Encima va una banda de noche abajo a la izquierda (terminador suave), como pide §1.1, que cubre casi todo el relleno.

A tamaño completo no se ve costura ni corte recto (`montaje/P07_placa_tierra.jpg`). Es un arreglo para este montaje: en la versión final conviene un K07 con el disco entero y la noche donde manda el cálculo (77 % iluminado).

### 7.3 Revisión del montaje

Revisé la hoja de contacto, los cuadros 0, 26 y 51,95 s a tamaño completo y las dos disolvencias (29 y 37 s).

- **Reglas:** en ningún cuadro hay letras, insignias, banderas ni rostros. Los brazos de la torre de P04 van con el parche.
- **P06→P07:** es la mejor transición del montaje. La chispa se posa sobre la cima del disco de la Tierra y la estela sigue su curva.
- **P07→P08:** se lee como la Tierra sobre el limbo lunar, no como «el disco azul se vuelve un disco gris del mismo tamaño». Falta el render de LRO de 0 a 2 s de P08 (§2), que convierte la disolvencia en una disolvencia por forma.
- **P04→P05:** el salto de luz que señaló el crítico se ve: el cielo pasa de crema calimoso a azul limpio, y la orilla y los coches son otros. No lo corregí en el montaje. Queda para el etalonaje.
- **P03→P04:** el cohete pasa de x 0,64 a 0,53. Se nota menos que antes (0,49), pero sigue habiendo salto. No recorté P03 porque el recorte del crítico (desde x = 599) se come el primer coche y las tres primeras siluetas.
- **P09:** el acercamiento y el congelado ya se leen como un descenso que termina en el contacto. Siguen el polvo «grabado» en el suelo y la textura de metal cepillado. Falta el polvo disparado.

### 7.4 Tabla final por plano

| Plano | Modelo | Tomas | Créditos | Elegida | Veredicto del crítico |
|---|---|---:|---:|---|---|
| P03 La torre | `minimax_h3` 10 s 2K | 1 | 20,00 | t1 | Sirve: limpio y casi quieto. Pendiente: salto de encuadre en el corte a P04, calima y color |
| P04 ★ La ignición | `seedance_2_5` 8 s 720p, inicial y final | 1 | 56,00 | t1 con parche de los brazos (0 créditos) | Sirve: ignición a 1,5 s, vapor ámbar y despegue a 5 s. Las seudoletras de los brazos ya están resueltas |
| P05 La columna | `seedance_2_5` 8 s 720p | 1 | 56,00 | t1 | Sirve con etalonaje y recorte. El cambio de lugar y de luz frente a P03 y P04 sigue abierto |
| P06 La chispa | `minimax_h3` 6 s 2K | 2 | 24,00 | t2 | Sirve. Pendiente: bajar el halo y poner la firma en P★ (el reencuadre ya está hecho) |
| P07 La Tierra | ffmpeg y Python sobre K07_r1 | 0 | 0,00 | placa completada | Sin crítica todavía (el crítico la marcó como no apta por el corte). Se resolvió con la placa de §7.2, que es provisional |
| P08 La Luna crece | `minimax_h3` 6 s 2K | 1 | 12,00 | t1 | Sirve: deriva limpia. Estrías finas en las paredes de los cráteres |
| P09 La sombra | `seedance_2_5` 8 s 720p | 2 | 112,00 | t1 montada con la opción B | **No cumplía** (grave): paneo sin descenso y polvo grabado. Con el montaje hay descenso y parada seca. Falta el polvo, y la opción A (56 créditos) sigue abierta |
| **Total** | | **8** | **280,00** | | |

- **Saldo de la cuenta** (`higgsfield.cmd account status`, 2026-11-15 a las 12:10): **424,70 créditos**. Este montaje gastó 0.
- **Cuadre del registro** (`registro_video.json`, una fila por trabajo):
  - Gasto en video: 20 + 56 + 56 + 12 + 12 + 12 + 56 + 56 = **280,00**.
  - Saldo antes del video: 742,25. Saldo previsto: 462,25.
  - Diferencia con el saldo real: 37,55 créditos, que se gastaron fuera de este lote entre tomas (4,50 antes de P04 y 33,05 entre P03 y P05; los saldos «antes» del registro lo muestran). No son de video.

### 7.5 Lo que queda por mejorar en estos planos (sin gastar créditos)

1. **Etalonaje en 10 bits:**
   - Igualar el cielo de P04 y P05 al crema calimoso de P03 (#D9D6C8 y #E8DCC0), con niebla en el tercio bajo de P05 y siluetas aplastadas a #3A3226.
   - Pasar el cielo de P06 al índigo #2B2F5A.
   - Llevar P09 hacia el regolito #7D7C78.
2. **Calima de P03:** desplazamiento horizontal suave, limitado al horizonte, al cohete y al reflejo.
3. **P06:** halo de la chispa a −60 % entre 0,5 y 4,5 s, la firma del punto de luz en P★ (6 px, 12 cuadros) y un giro de −0,3°.
4. **P09:** rayos de polvo radiales compuestos que salen del centro en los 3 s previos al contacto, y un desenfoque direccional de 1 px contra el cepillado. Si no basta, la opción A del crítico (otra toma de Seedance con inicial y final, **56 créditos, necesita aprobación**).
5. **P08:** si las estrías molestan a 1080p, montar la ventana de 0 a 4 s acelerada un 20 %. Eso obliga a rehacer el render de 0 a 2 s.
6. **P04:** revisar a 1080p la barandilla pequeña (x ≈ 0,57, y ≈ 0,69).

### 7.6 Lo que falta para la versión final

- **Grano y tubo por shader:**
  - 16 mm al 100-70 % en Florida, al 40-10 % en el vacío;
  - halación en la llama de P04;
  - temblor del 1 % y arruga del agua en P05.
- **Sonido:** viento y agua, primer silencio, golpe grave, rugido con crepitación, segundo silencio, respiración de casco, tonos `q`, zumbido y contacto (§4). Hoy solo hay tono de sala.
- **Rótulos R1 y R2 y la frase S1:** se componen en el motor.
- **Escalado a 1080p** de todo el montaje. Si se hace con IA y no con lanczos, revisar que no vuelvan las marcas en los brazos de P04.
- **Render de LRO para P08 (0 a 2 s)** desde `pruebas/luna_telescopio/`: un disco gris del tamaño y el lugar de la Tierra al final de P07, para la disolvencia por forma.
- **K07 nuevo** con el disco entero, que sustituya la placa provisional (se cotiza aparte).
- **P01 y P02 del motor** (el cuarto a oscuras y la entrada al televisor), horneados con Movie Maker, y el paso de 4:3 a 16:9 hacia K03.
- **Movimiento III** (P10 a P14) y P15.

### 7.7 Pendiente del director

- [ ] Ver `montaje_mov_I_II.mp4` y dar su veredicto sobre los movimientos I y II.
- [ ] Decidir P09: dejar el montaje (0 créditos y polvo compuesto) o pagar la opción A (56 créditos).
- [ ] Aprobar o no la partida de un K07 nuevo.
