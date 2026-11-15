# Lote 10 · Video de los movimientos I y II

> Cinemática de apertura «Un punto de luz». Movimiento I «La torre» (P03 a P06) y movimiento II «El vacío» (P07 a P09).
> Estado al 2026-11-15, 09:40: **preparado y cotizado. No se generó ningún video ni se gastó ningún crédito.**
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
