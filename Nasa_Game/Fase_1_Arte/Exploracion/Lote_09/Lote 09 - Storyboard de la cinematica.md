---
tipo: lote de arte
fase: 1 y 2
lote: L09a, L09b, L09c
fecha: 2026-11-15
estado: fotogramas finales y pruebas generados; esperan el veredicto de Guillermo
creditos: 111,50 (09a 4,25; 09b y 09c 107,25)
---

# Lote 09: storyboard de la cinemática «Un punto de luz»

Fotogramas de la cinemática de apertura. Guion: [[Guion - Cinematica de apertura]]. Storyboard: [[Storyboard - Cinematica de apertura]]. Revisiones de hoy: [[Revision_P13_bandera]] y [[Revision_P14_personaje]].

## 0. En cifras

| | Imágenes | Créditos |
|---|---:|---:|
| 09a, viñetas de borrador | 17 | 4,25 |
| 09c, bandera (K13a): 2 variantes y 2 reintentos | 4 | 18,00 |
| 09c, protagonista (P14c): 3 direcciones, C en 3 modelos | 5 | 19,00 |
| 09b, fotogramas finales K03 a K12, con 4 reintentos | 16 | 70,25 |
| **Total** | **42** | **111,50** |

- Saldo: 849,50 al empezar el 09b y 09c; **742,25** al terminar (gastado 107,25; tope del encargo, 150).
- Partida: Guillermo, 2026-11-15: «Usa los mejores modelos de Higgsfield para este objetivo, no importa el gasto».
- Todas las imágenes de 09b y 09c, en `gpt_image_2_6` 2k `xhigh` (4,50) salvo K10 (`high`, 2,75) y las dos alternativas de modelo de P14c.
- Cada generación, con su encargo completo, está en `Nasa_Game/Fase_1_Arte/registro_generaciones.json`, con el veredicto de la revisión.

## 1. Láminas para el director

![[revision_bandera.jpg]]

![[revision_personaje.jpg]]

![[finales_lamina_1.jpg]]

![[finales_lamina_2.jpg]]

## 2. Lote 09a: viñetas de borrador

`lote_09a_storyboard.json`. `gpt_image_2_6`, `low`, 1k, 16:9, 0,25 cada una. 2026-11-15 01:45. Láminas: `storyboard_lamina_1.jpg` y `storyboard_lamina_2.jpg`.

| Id | Trabajo | Créditos | Veredicto |
|---|---|---:|---|
| L09_P01_cuarto_noche_borrador | 55346705 | 0,25 | Aprobado con el storyboard |
| L09_P02_televisor_borrador | c6044da5 | 0,25 | Aprobado con el storyboard |
| L09_P03_torre_borrador | e50362fb | 0,25 | Aprobado con el storyboard |
| L09_P04b_ignicion_borrador | 403ed80a | 0,25 | Aprobado con el storyboard |
| L09_P05_columna_borrador | da6ac466 | 0,25 | Aprobado con el storyboard |
| L09_P06_chispa_borrador | 8e514ff3 | 0,25 | Aprobado con el storyboard |
| L09_P07_tierra_borrador | 5be6cc97 | 0,25 | Aprobado con el storyboard |
| L09_P08_borde_luna_borrador | d1a80c9a | 0,25 | Aprobado con el storyboard |
| L09_P09_sombra_borrador | c2966f86 | 0,25 | Aprobado con el storyboard |
| L09_P10_fantasma_tv_borrador | 5703b1d6 | 0,25 | Aprobado con el storyboard |
| L09_P11_huella_borrador | db7e4c5f | 0,25 | Aprobado con el storyboard |
| L09_P12_guayaquil_1969_borrador | a545b43d | 0,25 | Aprobado; mejorar su espalda |
| L09_P13_bandera_tierra_borrador | 489b9537 | 0,25 | Cambio: la bandera ondea y se ve |
| L09_P14a_gota_fria_borrador | c75d1e8a | 0,25 | Cambio: mejorar su diseño |
| L09_P14b_franja_ambar_borrador | bfa0210a | 0,25 | Cambio: mejorar su diseño |
| L09_P14c_despierta_borrador | b9ec9318 | 0,25 | Cambio: mejorar su diseño |
| L09_P15_manana_borrador | 164d9eab | 0,25 | Cambio: mejorar su diseño |

Veredicto de Guillermo (2026-11-15): «Excelente, pero que se vea la bandera estado unidense flameante en la luna y asimismo, mejora el diseño de la personaje en los últimos tramos de la cinemática».

## 3. Lote 09c: la bandera (K13a)

`lote_09c_bandera.json`, `lote_09c_bandera_r1.json` y `lote_09c_bandera_r2.json`. Revisión al 100 y 400 %: franjas contadas en tiras verticales del original, en el lado del asta y en el vuelo; estrellas contadas por columnas (11 columnas de 5 y 4 = 50).

| Id | Trabajo | Créditos | Franjas (asta / vuelo) | Barra | Veredicto |
|---|---|---:|---|---|---|
| L09c_K13a_v2_tres_cuartos_asta | be095035 | 4,50 | 13 / 13 | Sí | **Recomendada.** 50 estrellas, cantón junto al asta, anverso, la tela no toca el suelo. Ocupa el 51 % del alto (se pidió el 23 %) |
| L09c_K13a_v1_frontal_guante | da3a476c | 4,50 | 13 / 11 | Sí | Descartada: faltan 2 franjas en el vuelo |
| L09c_K13a_v1_frontal_guante_r1 | 7a29bb88 | 4,50 | 13 / 13 | **No** | Válida con reparo: flamea como con viento, lo que en la Luna no pasa |
| L09c_K13a_v1_frontal_guante_r2 | 8f82692d | 4,50 | 13 / 11 | Sí | Descartada: faltan 2 franjas en el vuelo |

- r1 añadió «las 13 franjas continuas hasta la punta»; r2, además, «la barra visible» y «no hay aire». Con el guante, el modelo no dio las dos cosas a la vez en 3 intentos.
- En todas, la Tierra sale unas 2,5 veces más grande de lo pedido: se sustituye en posproducción por la renderizada (Revision_P13 §4).
- Guante: blanco, sin parches ni marcas; no hay brazo, casco ni rostro.
- La bandera es más grande que en el cálculo de la grúa (§2.2 de Revision_P13): hay que rehacer la subida con la tela real de la imagen elegida.

## 4. Lote 09c: la protagonista (P14c)

`lote_09c_personaje.json`. Referencias: `@ANC_PROTA_1` y dos recortes de sus hojas (`subidas_09c.json`). Ángulo medido entre la línea de los ojos y la vertical; el storyboard pide menos de 10°.

| Id | Dirección | Modelo | Trabajo | Créditos | Ángulo | Veredicto |
|---|---|---|---|---:|---:|---|
| L09c_P14c_A_lowpoly_fino_gpt | A | gpt_image_2_6 xhigh | 09ace157 | 4,50 | 27° | Válida para comparar. Facetas finas en la piel, ojo bien hecho |
| L09c_P14c_B_pintado_gpt | B | gpt_image_2_6 xhigh | 439124d9 | 4,50 | 26° | Válida para comparar. Gouache con pincel, rizos por mechones |
| L09c_P14c_C_cine_gpt | C | gpt_image_2_6 xhigh | b3417879 | 4,50 | 21° | **La mejor.** Iris en capas, menisco, pestañas, lágrima fina, pecas y rubor. Rizos en bloques |
| L09c_P14c_C_cine_nbpro | C | nano_banana_pro 2k | c2c107c9 | 2,00 | 10° | Descartada: pelo negro facetado, camisa verdosa, ceja inferior fuera de sitio |
| L09c_P14c_C_cine_seedream55 | C | seedream_5_5 2k | 06a2d6f7 | 3,50 | 6° | Válida con reparo: cara horizontal y rizos mechón a mechón; ojos redondos de juguete |

- Ninguna de `gpt_image_2_6` deja la cara horizontal (21° a 27°); mejoran mucho a la viñeta del 09a, que la enderezaba unos 40°. Reserva del storyboard: cara en vertical y giro de 90° en ffmpeg.
- Todas mantienen el arete en rombo, la camisa caqui sobre la camiseta oscura y la lágrima como línea fina. Ninguna letra ni emblema.
- Riesgo de edad: en las cinco la cara es muy redonda y se lee más joven que 20 años. Revisarlo en la hoja de expresiones.
- No se generó la hoja de expresiones (4,50): espera la dirección que elija Guillermo.

## 5. Lote 09b: fotogramas finales

`lote_09b_finales.json` (primera tanda), `lote_09b_r2.json`, `lote_09b_r3.json` y `lote_09b_r4.json`. Encargos copiados por script de la §2 del storyboard, sin retocar. Delante va una frase que declara la viñeta como referencia de composición (ids en `subidas_09b.json`). K04a y K11a llevan su hermano final como referencia.

| Id | Trabajo | Calidad | Créditos | Veredicto |
|---|---|---|---:|---|
| L09b_K03_final | c6109403 | xhigh | 4,50 | Aprobada en revisión. Sin letras; autos de los 60; las figuras miden 1/6 del alto (se pidió 1/20) |
| L09b_K04a_final | b94f1d36 | xhigh | 4,50 | Aprobada: mismo encuadre que K04b |
| L09b_K04a_final_r1 | 37c1ef5b | xhigh | 4,50 | Duplicado: lo pedí por un error mío al comparar escalas; equivale al original |
| L09b_K04b_final | 26ca68fc | xhigh | 4,50 | Aprobada. Sin marcas; cohete en x = 0,50 (se pidió 0,60) |
| L09b_K05_final | 3981915a | xhigh | 4,50 | Aprobada. Columna en x = 0,59; placas en blanco |
| L09b_K06_final | c27dcf11 | xhigh | 4,50 | Aprobada. Chispa en P★ |
| L09b_K07_final | 3f1b4eda | xhigh | 4,50 | Descartada: el globo se corta abajo y el alejamiento de P07 lo enseñaría |
| L09b_K07_final_r1 | 130fa334 | xhigh | 4,50 | Aprobada. Globo entero; borde iluminado en P★ |
| L09b_K08_final | b2b27aa5 | xhigh | 4,50 | Aprobada. Cima del limbo en P★; cráteres algo repetidos |
| L09b_K09_final | 06205c2b | xhigh | 4,50 | Descartada: sombras de piedras en espiga, todas iguales |
| L09b_K09_final_r1 | 57633aa7 | xhigh | 4,50 | Aprobada. Sin la viñeta; sombras naturales y cuatro patas |
| L09b_K10_final | c60da9aa | high | 2,75 | Aprobada. Sin rostro ni marcas en el traje |
| L09b_K11_final | 4a3204d4 | xhigh | 4,50 | Aprobada |
| L09b_K11a_final | ac28441d | xhigh | 4,50 | Aprobada. Solo el borde de la suela |
| L09b_K12_final | fc2249e8 | xhigh | 4,50 | Descartada: pelo de fieltro, camisa crema y una bahía al fondo (el río queda a su espalda, §9 corrección 14) |
| L09b_K12_final_v2 | 28f7e7d7 | xhigh | 4,50 | Aprobada. Cambio 5 de Revision_P14 §8 y la espalda de la hoja de giro, sin viñeta; sin agua. Sale nítida, no desenfocada |

- Reintentos: K07 añadió «el globo entero dentro del cuadro»; K09, «sombras que siguen la forma de la piedra»; K12 v2 aplica el cambio 5 de la revisión del personaje y «sin río, bahía ni agua».
- Revisados al 200 %: cohetes, autos, trajes, la suela y la figura de ella. No hay letras, insignias, parches ni rostros.
- Pendientes, por depender del director: K01, K02, K13 (sale de K13a), K14a a K14d y K15.

## 6. Sin verificar

- Que Seedance 2.5 conserve las 13 franjas en movimiento: lo dice la puerta de control del clip.
- La paleta de los finales contra la paleta maestra (`paleta.py comparar`): no se midió.
- La diferencia entre `xhigh` y `max` en el primer plano: no se probó.
