# Revisión P14 · La protagonista en primer plano

> 2026-11-15. Responde a la nota de Guillermo sobre el storyboard: «mejora el diseño de la personaje en los últimos tramos de la cinemática» y «usa los mejores modelos de Higgsfield para este objetivo, no importa el gasto».
> Alcance: P14a, P14b, P14c y P15, y la espalda de P12. **No edita** el guion ni el storyboard: los cambios propuestos están en §8 para que otro agente los integre.
> Estado: **propuesta sin validar.** El lote de prueba [[lote_09c_personaje.json]] está cotizado (**19,00 créditos**) y **no se ha generado**.

## 0. En cifras

| | |
|---|---|
| Viñetas revisadas | 5 (P12, P14a, P14b, P14c y P15), a 1280 px y la cara al 200 % |
| Referencias comparadas | Hoja L02, hoja de giro L04 y la malla v8T del juego (`parecido/hoja_vs_v8T.png`) |
| Causa principal | El bloque `{ESTILO}` («crisp faceted flat-shaded planes… chunky simplified forms») aplicado a un macro de 100 mm. **En la hoja y en la malla del juego la cara es lisa y pintada;** solo el pelo es facetado |
| Direcciones | A · low-poly fino pintado; B · ilustración pintada con volumen; **C · cine estilizado (recomendada)** |
| Lote de prueba | 5 imágenes: A, B y C en `gpt_image_2_6` `xhigh` 2k (4,50 c/u); C además en `nano_banana_pro` 2k (2,00) y `seedream_5_5` 2k (3,50). **Total 19,00**, tope 20,00 |
| Siguiente, tras el veredicto | Hoja de expresiones en la dirección ganadora: 4,50 |
| Referencias nuevas | 3 recortes de las hojas aprobadas, subidos sin costo (`Lote_09/subidas_09c.json`) |
| Saldo comprobado hoy | **849,50**; quedaría en 830,50 tras la prueba |

## 1. Lo que se ve en las viñetas

![[L09_P14a_gota_fria_borrador.png|300]] ![[L09_P14b_franja_ambar_borrador.png|300]] ![[L09_P14c_despierta_borrador.png|300]]
![[L09_P12_guayaquil_1969_borrador.png|300]] ![[L09_P15_manana_borrador.png|300]] ![[L02_protagonista_tipo1_hoja.png|300]]

## 2. Diagnóstico

### 2.1 Por qué el primer plano no está a la altura

| # | Defecto | Dónde | Por qué pasa |
|---|---|---|---|
| 1 | **Facetas enormes en la cara:** la nariz es un poliedro de 5 caras, la frente y la mejilla son planos lisos con aristas duras | P14a, P14b, P14c | `{ESTILO}` pide facetas planas y formas gruesas. A 100 mm, una faceta de la malla ocupa un quinto del cuadro |
| 2 | **Planos duros que rompen la expresión:** las aristas cruzan párpados y mejillas; la sonrisa no puede subir la mejilla porque la mejilla es un plano | P14c | Igual que 1. Un gesto necesita volumen continuo |
| 3 | **Ojos de juguete:** discos con contorno negro grueso, esclerótica plástica, sin párpado inferior, sin línea de agua, sin pestañas en el ojo abierto (pierde el «ala» de la hoja), dos brillos cuadrados pegados encima | P14c | El modelo copió el ojo de la hoja de expresiones y lo agrandó sin construirlo |
| 4 | **Piel sin vida:** naranja plano y uniforme, sin translucidez en la nariz ni en el borde de la mejilla, sin vello ni variación de color | P14a, P14b, P14c | «Matte materials» y «flat-shaded» en `{ESTILO}` |
| 5 | **Rizos como bloques:** prismas de 6 a 8 caras, sin espiral ni mechones | P14a, P14b, P14c | Igual que 1 |
| 6 | **Boca de surco y cejas de losa:** la boca es una ranura; las cejas, dos placas planas | P14a, P14b, P14c | Igual que 1 |
| 7 | **La cabeza no está horizontal en P14c:** gira unos 40° hacia la vertical. Rompe el raccord con P14b y obligaría al video 14B a girar la cabeza, que M14B prohíbe | P14c | Los modelos enderezan las caras acostadas |
| 8 | **Expresión genérica:** «sonrisa de mascota» de ojos redondos; no se lee «despierta con algo que no le cabe en el pecho» | P14c | El encargo no describe la mecánica del gesto (párpado inferior, pómulo, comisura) |
| 9 | El arete cambia en cada viñeta: bola gris, diamante blanco, pirámide | P14a, P14b, P14c | Detalle sin anclar en el encargo |
| 10 | **P12, la espalda:** el pelo es una bola de fieltro lisa, no la masa de rizos de su hoja; la camisa caqui abierta se lee como una camiseta crema; la imagen es de miniatura de arcilla fotografiada, no de su estilo | P12 | El encargo pide «a dark soft shape» sin la vista de espalda como referencia |
| 11 | **P15:** en la viñeta mira la ventana, no el banco, y el pelo sale más claro y menos voluminoso que en la hoja | P15 | Es solo para el animatic: en producción P15 es la malla del juego |

**Lo central:** las viñetas de P14 se parecen **menos** a ella que la propia malla del juego. La hoja L02, la hoja de giro y la malla v8T tienen la cara lisa y pintada y el pelo en mechones facetados con filo naranja. El facetado de la cara lo inventó el bloque de estilo, no su diseño. Corregirlo acerca el primer plano a su hoja y al juego a la vez.

### 2.2 Lo que funciona y se conserva

- **Identidad:** cara redonda, piel morena cálida, ojos grandes castaño oscuro con un ala corta al final de la línea de pestañas, cejas gruesas y algo arqueadas, nariz de botón pequeña, boca pequeña, unas pocas pecas y rubor suave, arete de plata en rombo, rizos castaño oscuro muy voluminosos con un rizo suelto en la sien.
- **Vestuario:** cuello de la camisa caqui de manga corta, abierta sobre la camiseta oscura.
- **Proporciones** de su hoja (unas 3,3 cabezas de alto): de cerca no se ven, pero la forma de la cara y el tamaño de los ojos respecto a la cara sí.
- **La luz de P14a y P14b:** el azul petróleo del alba y la franja ámbar rayada que sube en diagonal ya cuentan el plano. Se conservan.
- **La almohada y el cuello facetados:** dan el eco low-poly sin tocar la cara.

## 3. Diseño de primer plano: tres direcciones

El siguiente corte es al motor, con ella pequeña en cuadro (P15). La costura se esconde en el pestañeo y en 1 s de desenfoque (storyboard §3.3). Lo que cruza el corte no es la textura de la piel, que a esa distancia no se ve, sino **la silueta del pelo, la paleta y el filo dorado de los rizos**.

| | A · Low-poly fino pintado | B · Ilustración pintada con volumen | **C · Cine estilizado** |
|---|---|---|---|
| Qué es | Muchas más facetas, pequeñas y suaves, solo visibles en los brillos; pintura a mano sobre cada una. Rizos de facetas medianas; camisa y almohada, gruesas | Gouache digital sobre aguada, pincelada visible que sigue la forma, formas simples sin facetas, luz de cine | Modelado liso con la forma de su hoja: piel translúcida pintada, ojos construidos (córnea, iris en capas, línea de agua), rizos mechón a mechón con un bisel leve que recuerda el facetado. Solo la camisa y la almohada conservan facetas suaves |
| Qué gana | El vínculo más literal con «low-poly» | El acabado más «pintado a mano», cálido y de autor | El gesto: párpado, pómulo y sonrisa se mueven en volúmenes continuos. Es lo más parecido a su hoja y a su malla, que ya tienen la cara lisa |
| Qué arriesga | Contradice la hoja y la malla, que no tienen la cara facetada. Con la franja de luz en movimiento, las facetas pequeñas parpadean (sin medir: lo mide la prueba A/B de 14B). Una faceta mal puesta en el párpado parece un defecto | En video, las pinceladas «hierven» de un cuadro a otro y la cara deriva. Un plano de 12 s con luz que se mueve es lo más difícil para la pintura animada. Es el único plano pintado entre material fotográfico (16 mm) y el motor | Caer en el «personaje de película animada genérico». Se evita con la textura pintada, las pecas y el rubor de la hoja, el bisel de los rizos, la almohada facetada y la paleta del juego |
| Empalme en P15 | Directo en el estilo, pero la cara de P15 es lisa: el salto de facetas finas a cara lisa también se nota | El más brusco: de pintura a 3D | Cara lisa → cara lisa; rizos de mechón con bisel → rizos facetados; el desenfoque de 1 s y el cambio de escala esconden la diferencia de detalle |
| Modelo que le conviene | `gpt_image_2_6` (sigue la dirección de arte al detalle; lote 01) | `gpt_image_2_6`; `nano_banana_pro` deriva a ilustración con contorno, lo que aquí sí sirve | `gpt_image_2_6`, con `seedream_5_5` (luz de cine; ignora el low-poly, que en C es ventaja) y `nano_banana_pro` (hasta 14 referencias para la identidad) como alternativas |

**Recomendación: C · cine estilizado.**
1. Es fiel a ella: su hoja y su malla del juego tienen la cara lisa. A y B la alejan de su diseño en direcciones opuestas.
2. Es el único plano de cara de la película (storyboard §3.1) y el que decide la emoción: necesita un gesto que se mueva, y el gesto necesita volumen continuo.
3. Es la más estable en video **(hipótesis, sin verificar)**: una superficie lisa con luz que cambia da menos parpadeo que facetas o pinceladas. La prueba A/B de 14B (storyboard §5.4, puerta 3) lo confirma o lo descarta antes del gasto grande.
4. El eco del juego queda donde se lee: el bisel de los rizos, la almohada y el cuello facetados, la paleta y el filo dorado.

**Bloque de estilo propuesto** (`ESTILO_PRIMER_PLANO`, nuevo; `{ESTILO}` no se toca, como pide `bloques_prompt.json`). Es el texto de la dirección C en §5.2.

## 4. La cara de cine

### 4.1 Ella, de cerca

| Rasgo | Cómo es |
|---|---|
| Edad | Unos 20 años, en las proporciones estilizadas de su hoja: joven, **no una niña**. Pómulos y mandíbula apenas definidos, sin cara de bebé. Natural: sin maquillaje, sin glamur, nada que la sexualice |
| Cara | Redonda, de mejillas llenas, con el mentón pequeño y suave |
| Ojos | Grandes, castaño oscuro, almendrados y redondos. Párpado superior con un pliegue suave; un ala corta y oscura al final de la línea de pestañas (de su hoja). Iris en capas con fibras radiales, córnea clara, línea de agua húmeda y un menisco fino. Pestañas sueltas, oscuras, más largas en el tercio exterior |
| Cejas | Gruesas, castaño oscuro, algo arqueadas, con pelo dibujado y no en losa |
| Nariz | De botón, pequeña y redondeada, con la punta translúcida a contraluz |
| Boca | Pequeña, labios llenos y suaves; en reposo, cerrada; en la sonrisa, cerrada y con las comisuras arriba |
| Piel | Morena cálida, pintada a mano con variación de color: más rojiza en mejillas, nariz y párpados. Unas pocas pecas finas y rubor suave (de su hoja). Vello fino que atrapa el filo de luz |
| Pelo | Rizos castaño oscuro en espirales definidas, agrupadas en mechones con volumen; cada mechón con un bisel leve. Un rizo suelto en la sien. Filo dorado en las puntas |
| Arete | Uno pequeño, de plata, en rombo: el mismo en los cuatro fotogramas |
| Ropa | El cuello de la camisa caqui con tejido de algodón; la camiseta oscura debajo |

### 4.2 La emoción de cada momento

| Fotograma | Tiempo | Qué siente | Cómo se ve | Luz |
|---|---|---|---|---|
| K14a · dormida | 1:39–1:41 | Sueño hondo, todavía allá | Párpados cerrados y relajados, pestañas apoyadas, boca suave y apenas abierta, cejas sin tensión. La gota en el lagrimal se compone | Alba fría: un filo azul en el puente de la nariz y las pestañas; todo en azul petróleo, 6:1 |
| K14b · la franja sube | 1:41–1:45 | El sueño se aclara; está a punto de volver | Igual que K14a, con un temblor mínimo del párpado (lo pone el video) | La franja ámbar rayada sube en diagonal a 30° de la mandíbula al párpado cerrado; fuera de ella, azul petróleo, 4:1 |
| K14c · despierta | 1:45–1:51 | Alegría que no le cabe: no quiere moverse para no perderla | Ojos abiertos, húmedos, sin enfocar. La sonrisa **nace en los ojos**: sube el párpado inferior, sube el pómulo, se pliegan las comisuras de los ojos; la boca solo después, cerrada. La sonrisa suelta la lágrima, que cruza de lado el puente de la nariz | Franjas ámbar sobre la mejilla y los ojos, crema en los altos, sombra azul petróleo cálida, 3:1. Dos brillos rectangulares de la celosía en cada ojo. Filo dorado en los rizos |
| K14d · pestañeo | 1:51 | — | Los dos ojos cerrados en un pestañeo suave; nada más cambia | La de K14c |

**La lágrima.** En la prueba de look de P14c va pintada en la imagen, porque Guillermo tiene que juzgar la emoción completa. En producción sigue la regla del storyboard (§3.1): **ningún fotograma ni clip la lleva** y se compone después. La prueba sirve además de modelo para el compositor.

## 5. Encargos

### 5.1 Cómo se arma el encargo de P14c

Cada encargo de prueba es: **cámara + identidad + momento + luz + estilo (A, B o C) + protecciones.** Solo cambia el estilo, para comparar las direcciones con todo lo demás igual. El texto completo de cada trabajo está en `Fase_1_Arte/Exploracion/Lote_09/lote_09c_personaje.json`.

Referencias, en este orden y en los cinco trabajos:
1. `@ANC_PROTA_1`: la hoja L02 completa.
2. `481919be-a76a-4920-bb90-662b31f458fc`: la fila de cuatro cabezas de la hoja L02 (`referencias_09c/L09c_ref_caras_hoja.png`).
3. `39712f78-40d4-4043-8355-9074af995982`: la cabeza de frente, limpia, de la hoja de giro L04 (`referencias_09c/L09c_ref_cara_giro.png`).

**Cámara**
```text
Extreme close-up film frame, 100 mm macro lens at f/2, camera locked off at pillow height with the lens axis parallel to the pillow. She lies on her left side with her left cheek sunk into a cream pillow, so her face is horizontal in the frame: forehead toward the right edge, chin toward the left edge, and the line through her two eyes runs vertically. Her upper eye (her right eye) is in the upper half of the frame and its inner corner sits at three fifths of the frame width and one third of the height from the top; her lower eye is half hidden by the pillow and falls softly out of focus. A razor-thin plane of focus lies on the lashes of her upper eye. Her voluminous dark curls fill the right third of the frame, out of focus; the cream pillow fills the lower third; the collar of her khaki short-sleeve shirt over a dark T-shirt shows at the left edge.
```

**Identidad**
```text
She is exactly the character of the reference images (the full character sheet, its row of head studies and the clean front view of her head): a round face, warm brown skin, large dark-brown eyes with a small dark wing at the outer end of the upper lash line, thick softly arched dark-brown brows, a small rounded button nose, a small mouth, a few faint freckles and a soft warm blush on the cheeks, a tiny silver diamond-shaped stud earring, and big voluminous dark-brown curly hair with one small curl at the temple. She is a university student about twenty years old drawn with the stylized proportions of her sheet: youthful but not a child, gently defined cheekbones and jaw, natural, no makeup look.
```

**Momento (P14c)**
```text
She has just woken. Her eyes are open, wet and bright, looking softly past the camera without focusing. The smile is born in her eyes: the lower lids lift, the upper cheek rises, the outer corners crinkle softly, and her mouth is only a small closed smile beginning. One single small tear has just left the inner corner of her upper eye and runs sideways across the bridge of her nose as a thin glistening line with a tiny bead at its tip; never a stream. The feeling is quiet, overwhelming joy, not sadness.
```

**Luz**
```text
Light: low warm morning sun through wooden window shutters. Soft-edged bands of amber light, split by the shutter slats, fall diagonally across her cheek and eyes at about thirty degrees, rising from her jaw toward her upper eyelid; between the bands the skin stays in a gentle petrol-blue shade, about three to one, the darkest tones warm and never black. Two small rectangular catchlights from the shutters shine in each eye, a golden rim of light runs along the curls, and the background is a soft warm blur.
```

**Protecciones** (cierran los cinco)
```text
No large flat facets on the face, no plastic or toy-like eyes, no thick outlines, no anime style, no childlike baby face, and the face stays horizontal, never tilted upright. Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

### 5.2 Los tres estilos

**A · Low-poly fino pintado**
```text
Style: refined hand-painted low-poly 3D for a game cinematic, a much denser mesh than the game model. The face is built from many small soft facets that show only as a delicate tessellation in the highlights, each facet painted with a soft gradient and fine brush texture, so the cheeks, eyelids and lips stay round and expressive with no large flat planes and no hard creases across the features. The eyes are smooth painted spheres with a layered iris, a wet waterline and fine individual lashes. The curls are spiral ringlets built from medium facets with hand-painted gradients; the shirt and the pillow keep chunkier facets. Matte, warm and painted.
```

**B · Ilustración pintada con volumen**
```text
Style: a painted illustration with volume, digital gouache over soft watercolour washes with a faint warm paper texture, visible confident brushstrokes that follow the form, simple rounded shapes with no hard facets anywhere, soft lost-and-found edges, the light painted like a film still. The skin is built with warm transparent glazes; the eye is painted with care: a layered iris, a wet waterline and a few strong lash strokes. The curls are painted as rhythmic ringlet clumps with dry-brush highlights; the shirt and the pillow are loosely blocked in with broad strokes.
```

**C · Cine estilizado (recomendada; propuesta de `ESTILO_PRIMER_PLANO`)**
```text
Style: a stylized cinematic 3D close-up from a feature-length animated film, smooth sculpted forms that keep the design of her sheet. Soft translucent skin with a gentle subsurface glow where the sunlight passes through the edge of the cheek and the tip of the nose, a hand-painted skin texture with subtle colour variation, faint freckles and fine peach fuzz catching the rim light. Eyes full of life: a clear cornea, a layered dark-brown iris with fine radial fibres, a wet waterline and a thin moist meniscus, individual dark lashes. The curls are defined ringlet by ringlet, each spiral clump sculpted with soft rounded volume and a faint bevelled edge that echoes the low-poly game style; the khaki collar shows a fine cotton weave, and only the shirt and the cream pillow keep gentle low-poly faceted planes. Not photorealistic: painted, warm and stylized.
```

### 5.3 Hoja de expresiones de primer plano (dirección C)

Se genera **después** del veredicto, con la dirección y el modelo ganadores (si gana A o B, se cambia el bloque de estilo). Sirve de referencia a K14a, K14b, K14c y a la toma 14B. **La fila de arriba no lleva lágrima,** para que el modelo de video no la invente; la lágrima va en un recuadro aparte, que se recorta antes de pasar la hoja al video. Mismas referencias que la prueba. `gpt_image_2_6` `xhigh` 2k, 16:9: **4,50** (cotizado).

```text
Character expression sheet for a cinematic close-up, on a plain warm light-gray background, even soft studio light from the upper right, clean grid with generous spacing. She is exactly the character of the reference images (the full character sheet, its row of head studies and the clean front view of her head): a round face, warm brown skin, large dark-brown eyes with a small dark wing at the outer end of the upper lash line, thick softly arched dark-brown brows, a small rounded button nose, a small mouth, a few faint freckles and a soft warm blush on the cheeks, a tiny silver diamond-shaped stud earring, and big voluminous dark-brown curly hair with one small curl at the temple. She is a university student about twenty years old drawn with the stylized proportions of her sheet: youthful but not a child, gently defined cheekbones and jaw, natural, no makeup look. [Bloque C de §5.2] Top row, three large panels, each the same extreme close-up of her face lying on her left side on a cream pillow, face horizontal (forehead to the right, chin to the left, upper eye in the upper half), framed like a 100 mm lens: 1) deeply asleep, eyelids closed and relaxed, lashes resting on the cheek, lips soft; 2) waking, the upper eyelid half open, lashes parting, an unfocused gaze, cheeks still relaxed; 3) awake and smiling with the eyes: lower lids lifted, upper cheek raised, a small closed smile, eyes moist and shining, no tear. Bottom row, the same three expressions upright and seen from the front at the same scale, plus a smaller fourth panel: a detail study of a single tear, a tiny bead at the inner corner of the eye and a thin glistening line across the bridge of the nose. The same face, hair, earring and khaki collar in every panel. No labels, no numbers. No text, no logos, no insignia, no emblems, no watermark.
```

## 6. Modelos

Cotizado hoy con `generate cost` (0 créditos), con `@ANC_PROTA_1` como referencia y 16:9 salvo donde se indica. Parámetros leídos con `model get`.

| Modelo | Opción | Créditos | Referencias | Para este plano |
|---|---|---:|---:|---|
| `gpt_image_2_6` | high 2k | 2,75 | hasta 16 | Lo que pide el storyboard para el resto |
| `gpt_image_2_6` | **xhigh 2k** | **4,50** | hasta 16 | La prueba de las tres direcciones |
| `gpt_image_2_6` | **max 2k** | **9,00** | hasta 16 | Nivel nuevo, por encima de `xhigh`. Candidato para los cuatro fotogramas finales de P14 |
| `gpt_image_2_6` | xhigh 4k / max 4k | 7,00 / 15,00 | hasta 16 | No: el video sale a 720p y el plan B, a 1080p; 2k sobra |
| `gpt_image_2_6_flare` | xhigh 2k | 4,50 | hasta 16 | Mismos parámetros; no hay descripción ni prueba: fuera |
| `nano_banana_pro` | **2k** / 4k | **2,00** / 4,00 | hasta 14 | Alternativa de C por la identidad con muchas referencias. Riesgo medido en el lote 01: deriva a caricatura con contorno |
| `nano_banana_2_1` | 2k / 4k, `thinking_level` high | 2,00 / 3,00 | — | Sin prueba en el proyecto: fuera |
| `seedream_5_5` | **2k** | **3,50** | hasta 10 | Alternativa de C. En el lote 01 dio la mejor luz de cine e ignoró el low-poly: en C eso ayuda |
| `seedream_v5_pro` | 2k | 2,50 | hasta 10 | Versión anterior de la misma familia: fuera |
| `soul_cinematic` | 2k | 0,12 | **1** | Solo una referencia y deriva del estilo (03 §3): no sirve para ella |
| `flux_3_image` | 2k / 4k | 3,00 / 19,00 | — | Sin prueba en el proyecto: fuera |
| `openai_hazel` | high | 6,00 | hasta 16 | No admite 16:9 (solo 1:1, 3:2 y 2:3): fuera |

**Qué modelo para cada dirección**
- **A:** `gpt_image_2_6`. Es el que sigue el low-poly al detalle (lote 01).
- **B:** `gpt_image_2_6`; `nano_banana_pro` como segunda opción, porque su deriva a ilustración aquí no estorba.
- **C:** `gpt_image_2_6` de base. Alternativas: `seedream_5_5` (la luz) y `nano_banana_pro` (la identidad). Por eso C va en tres modelos.

**Para los fotogramas finales** (lote 09b), el director pidió lo mejor: K14a, K14b, K14c y K14d en `gpt_image_2_6` **`max` 2k (9,00)** en vez de `xhigh` (4,50), si `gpt_image_2_6` gana la prueba. Son el único primer plano de la película. Una pasada: 36,00 en vez de 18,00 (**+18,00**); con 1,5 intentos, +27,00. Antes conviene un `max` contra `xhigh` del fotograma ganador (9,00) para ver si la diferencia se nota **(sin verificar)**.

## 7. Lote de prueba 09c

Archivo: `Nasa_Game/Fase_1_Arte/Exploracion/Lote_09/lote_09c_personaje.json`. Cotizado con `python herramientas/hf_generar.py … --solo-cotizar`: **19,00 créditos** (tope del lote: 20,00). **No se generó nada.**

| Id | Dirección | Modelo | Parámetros | Créditos |
|---|---|---|---|---:|
| `L09c_P14c_A_lowpoly_fino_gpt` | A | `gpt_image_2_6` | 16:9, 2k, `xhigh` | 4,50 |
| `L09c_P14c_B_pintado_gpt` | B | `gpt_image_2_6` | 16:9, 2k, `xhigh` | 4,50 |
| `L09c_P14c_C_cine_gpt` | C | `gpt_image_2_6` | 16:9, 2k, `xhigh` | 4,50 |
| `L09c_P14c_C_cine_nbpro` | C | `nano_banana_pro` | 16:9, 2k | 2,00 |
| `L09c_P14c_C_cine_seedream55` | C | `seedream_5_5` | 16:9, 2k | 3,50 |
| | | | **Total** | **19,00** |
| `L09c_hoja_expresiones_C` (en `_siguiente_tras_veredicto`, no se ejecuta con el lote) | ganadora | `gpt_image_2_6` | 16:9, 2k, `xhigh` | 4,50 |

- Generar, tras aprobar la partida: `python herramientas/hf_generar.py Nasa_Game/Fase_1_Arte/Exploracion/Lote_09/lote_09c_personaje.json`. La partida va antes en `trabajos.md`.
- Las referencias nuevas son recortes de dos hojas aprobadas: no traen diseño nuevo. Sus ids están en `Lote_09/subidas_09c.json`; no se añadieron a `anclas.json`.

**Cómo se revisa** (antes de enseñarlo a Guillermo)
1. Cada imagen a 1280 px y la zona del ojo de arriba, la nariz y el arete al 200 %.
2. La cara horizontal: la línea entre los ojos a menos de 10° de la vertical, y el lagrimal cerca de (0,60; 0,36). Si dos de los tres `gpt_image_2_6` enderezan la cabeza, se activa la reserva del storyboard: cara en vertical y giro de 90° en ffmpeg.
3. Contra su hoja: ala de las pestañas, cejas, nariz de botón, pecas y rubor, arete en rombo, rizo de la sien.
4. Edad: joven, no una niña. Nada que la sexualice.
5. Ninguna letra, insignia ni emblema; la lágrima, una línea fina y no un chorro.
6. `python herramientas/paleta.py comparar` contra la paleta maestra.
7. Lámina con las cinco al mismo tamaño, junto a la cabeza de su hoja.

## 8. Cambios propuestos para el storyboard (los integra otro agente)

| # | Dónde | Cambio |
|---|---|---|
| 1 | K14a, K14b, K14c | Cambiar «the same hand-painted low-poly character» y `{ESTILO}` por el bloque de la dirección ganadora (`ESTILO_PRIMER_PLANO`, nuevo en `bloques_prompt.json`), y añadir los bloques de identidad y protecciones de §5.1. Referencias: `@ANC_PROTA_1`, los dos recortes de la cara y la hoja de expresiones aprobada |
| 2 | K14b y K14c | Generarlos con K14a **y** la hoja de expresiones como referencias, en una tanda (ya lo pide §2). En K14c, añadir «the line through her two eyes runs vertically… never tilted upright» |
| 3 | M14A y M14B | «the painted faceted style» → «the same stylized painted style of the first frame» |
| 4 | §5.4, puerta 2 | K14a a K14d en `max` 2k si gana `gpt_image_2_6`: +18,00 por pasada. Añadir la hoja de expresiones (4,50) y esta prueba (19,00) |
| 5 | K12 | Añadir el recorte de espalda de la hoja de giro como referencia (`9d0b5c50-0f81-4d30-837e-aa9386a69700`, `referencias_09c/L09c_ref_espalda_giro.png`) y cambiar «she is a dark soft shape» por: «seen from behind exactly as in the back view of her turnaround sheet: a big rounded mass of separate dark curl clumps, never a smooth ball; her khaki short-sleeve shirt with rolled cuffs and plain blank shoulder patches with no symbol, her brown cargo pants with side pockets; she is soft and out of focus, but her silhouette reads clearly against the lit wall». El estilo del plano (16 mm) no cambia |
| 6 | P15 | El fotograma K15 solo sirve al animatic; en producción es la malla v8T/v9 (cara lisa, ya muy cerca de su hoja). Para la costura: comprobar en una captura del motor con la cámara de P15 que el castaño del pelo y el filo dorado coinciden con el K14c aprobado, y que el arete y el rubor de la textura se ven. Si el animatic se repite, el encargo de K15 ya pide que mire el banco; la viñeta falló en eso |

## 9. Sin verificar

- Que una cara lisa parpadee menos que una facetada o pintada en el video de 14B: hipótesis; la mide la prueba A/B de la puerta 3.
- La diferencia visible entre `xhigh` y `max` en `gpt_image_2_6`: no medida.
- Qué es `gpt_image_2_6_flare`: el catálogo no lo describe.
- Que los modelos mantengan la cara horizontal: P14c del 09a no lo hizo; lo dice la prueba.
- La fuerza de `nano_banana_pro` para sostener la identidad con 3 referencias: no medida en este proyecto.
