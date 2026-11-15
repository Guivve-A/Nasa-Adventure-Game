---
tipo: lote de arte
fase: 1
lote: L06
fecha: 2026-11-13
revisado: 2026-11-14
estado: propuesta · solo cotizado, espera la aprobación de Guillermo
creditos: 0
decisiones: D-013, D-015
---

# Lote 06: Luna del sueño y Mirador del Faro (propuesta)

## 1. Por qué este lote

- La **Luna del sueño** no tiene concepto, hoja ni paleta: 0 recursos en el [[Catalogo de recursos]]. El prototipo `pruebas/luna_sueno/` se detuvo por construirse sin validar.
- El **Mirador del Faro** solo tiene la escena de noche del lote 03, sin veredicto: salió como atardecer morado y no tiene diseñada la entrada ([[Lote 03 - Hojas de referencia y Mirador]]).
- Regla de Guillermo: cada escenario se valida con él antes de construirlo (concepto → hoja de referencia → producción → motor), y cada escena lleva diseñado su espacio de entrada y salida («ventana de carga»).
- Este lote es el paso «concepto» de los dos escenarios. **No se generó ninguna imagen: solo está cotizado.**
- Ilustra las escenas 2.1 a 2.5 (Mirador) y 3.1 a 3.5 (Luna) de [[Fase 2 - Analisis]], que sigue en borrador.
- Las 4 zonas de la Luna salen del pedido de Guillermo del 2026-11-12: en el sueño ella «camina» (L1), «recolecta muestras» (L2), «ve el Apolo» (L3) y coloca juntas las banderas de Estados Unidos y Ecuador (L4).

## 2. Lo que comparten los seis encargos

Lote: `lote_06_luna_mirador.json`. Sigue el formato del [[Lote 05 - Habitacion (propuesta)]].

| | |
|---|---|
| Modelo | GPT Image 2.6, calidad baja, 1k y 16:9: 0,25 créditos por imagen |
| Cámara | Bloque `{CAMARA_JUEGO}` (D-013): alta, sin horizonte ni cielo |
| Referencias | `@ANC_VISTA_JUEGO`, `@ANC_PROTA_1` y `@ANC_GATO` |
| Acabado | El 2D-HD del lote 05: desenfoque suave solo en los bordes, brillo y luz pintada (D-015) |
| Entrada y salida | Tramo despejado de unos 2 m, dentro de la zona nítida del cuadro, con la marca cian del concepto aprobado de la Habitación: un anillo de luz con un destello de cuatro puntas |
| Longitud | De 3 278 a 3 348 caracteres con los bloques ya expandidos. El encargo más largo generado con éxito mide 3 350 (`L05_A_manana_calida_final`) |

![[L05_A_manana_calida_final.png|420]]

*La marca cian del umbral (abajo a la derecha) es la que repiten los seis encargos.*

**Reglas duras escritas en los seis**

- Sin insignias, logotipos, emblemas, parches ni textos de agencias espaciales o misiones. Los encargos no nombran a la NASA ni al Apolo, para no atraer sus símbolos.
- La protagonista y Órbita son los únicos personajes: sin otras personas ni astronautas reales.
- Sin banderas, salvo las dos nuevas de L4. La bandera histórica no aparece.
- Sin texto ni interfaz (`{SIN_TEXTO}`): rosa de los vientos y carta estelar sin letras, etiquetas en blanco.
- El cian solo en tecnología e interacción: marca del umbral, anillo de 75 m, chapa de Órbita, destellos de muestra y ocular.
- En la Luna, la Tierra, el Sol, el cielo, las estrellas y el horizonte quedan fuera del cuadro, «ni reflejados en un casco». De la Tierra solo llega la luz.
- No se usa la palabra «diorama».

## 3. Los seis borradores

### Luna del sueño (4)

Las cuatro zonas del mapa lunar, en su orden de juego ([[Fase 2 - Analisis]], §5.1).

| ID | Escena | Qué se pide | Entrada y salida |
|---|---|---|---|
| `L06_L1_llegada_caja` | 3.1 | La caja de cartón de Rafael recién posada, tan ancha como alta es la protagonista, con el dibujo de la Luna pegado. Ella va en pleno salto largo y Órbita flota algo más alto. Huellas separadas y una zanja de práctica | La caja queda al borde de un claro de 2 m con la marca: es el umbral cama ↔ Luna. El camino sigue por un paso entre dos rocas, con su marca |
| `L06_L2_campo_muestras` | 3.2 y 3.3 | Cráter fresco de unos 4 m. Ella usa el cucharón de caja; en un soporte esperan las pinzas pequeñas, el martillo, el tubo de núcleo y las bolsas con la etiqueta en blanco. 4 puntos de muestra con destello cian | Paso de 2 m entre dos rocas, abajo a la izquierda, con la marca. Se sale por otro paso igual, arriba a la derecha |
| `L06_L3_anillo_respeto` | 3.4 | Una línea cian tenue cruza el cuadro: es un arco del anillo de 75 m. Los dos se detienen antes y sus huellas no la cruzan. Al fondo, pequeña, la etapa de descenso: forma genérica dorada y gris, sin letras. Ninguna bandera | Paso de 2 m abajo, con la marca. El camino sigue por fuera de la línea hasta otro paso igual |
| `L06_L4_loma_dos_banderas` | 3.5 | Loma intacta con dos banderas nuevas: Ecuador con escudo a la izquierda y Estados Unidos a la derecha. Mástiles iguales, barra horizontal, mismo tamaño y misma altura, sin tocar el suelo ni solaparse. Los dos, quietos, las miran. Amanece | Paso de 2 m al pie de la loma, con la marca |

- **Luz:** noche lunar bajo la Tierra casi llena (87 %, a 66° de altura: cálculo de la Fase 2). Luz azul fría, sombras azul profundo, nunca negro puro. En L4 entra el primer sol, rasante.
- **Trajes:** pequeños y originales. Tela crema acolchada, cinturón caqui, guantes, botas y mochila azul petróleo, y un aro coral en el cuello del casco. Sin insignias ni parches. La cara y el pelo de ella se ven por un casco redondo transparente, y conserva su bolso. Órbita lleva casco de burbuja y su chapa cian en el pecho.

### Mirador del Faro (2)

| ID | Escena | Qué se pide | Entrada y salida |
|---|---|---|---|
| `L06_M1_mirador_tarde` | 2.1 → 2.2 | Terraza de losas con rosa de los vientos, baranda curva sobre los techos del barrio, base del faro, telescopio con el ocular cian, atril con carta estelar, banca y guirnalda apagada. Ella acaba de llegar y Órbita se adelanta. Sol bajo y cálido | Descanso de llegada de 2 m entre dos postes con farol, abajo a la izquierda, con la marca. El portón del atajo de los faroles, cerrado |
| `L06_M2_mirador_anochecer` | 2.2 a 2.4 y 4.2 | La misma terraza a la hora azul: faroles, guirnalda y ventana del faro encendidos. Ella mira por el telescopio, que apunta bajo, y Órbita espera en la banca. La Luna y el cielo quedan fuera del cuadro | El mismo descanso. El portón del atajo, abierto y con su marca |

M1 y M2 comparten palabra por palabra la distribución y el umbral. Solo cambian la acción y la luz.

## 4. Decisiones de diseño que conviene conocer

1. **La Luna no cita `{ESTILO}`, `{PROTAGONISTA}` ni `{GATO}`.** `{ESTILO}` fija la paleta tropical y los otros dos describen la ropa de calle. Los encargos repiten la técnica de `{ESTILO}` palabra por palabra, con paleta lunar: regolito gris plata y gris azulado, sombras azul petróleo e índigo y pocos acentos cálidos. Los bloques aprobados no se tocan.
2. **Trajes sin rasgos de trajes reales:** sin bandas rojas en brazos y piernas, sin parche de bandera y sin visor dorado. Es un rumbo provisional: el traje necesita su propia hoja de referencia.
3. **L3 acerca la etapa de descenso.** La cámara de la escena del sendero (48°, campo de 40°, protagonista de 1,05 m al 12,5 % del alto) abarca 13,5 m de fondo y de 12,0 a 23,7 m de ancho (cálculo propio con `herramientas/camara_ancla.py`). A 75 m, la etapa queda más de 5 veces más lejos; a escala 1:4 (18,75 m) tampoco entra. El borrador la dibuja pequeña al fondo para juzgar el aspecto. En el juego se vería con el zoom de 3.4. Enlaza con el problema abierto 1 de la revisión C7: qué va a escala 1:4.
4. **La etapa de descenso es genérica pero se reconoce como tal:** cuerpo bajo y cuadrado, dorado y gris mate, sobre cuatro patas, sin letras, números ni marcas. No lleva la forma de ocho lados ni la lámina dorada del módulo real.
5. **Amanecer cálido en L4.** En la Luna real el amanecer no es dorado, porque no hay aire que tiña la luz. Se pinta blanco dorado por la biblia (luz cálida, sombra fría) y queda como licencia del sueño.
6. **Banderas de L4.** Van en orden alfabético, por tomar un criterio neutral: Ecuador a la izquierda. Los mástiles miden algo más del doble que la protagonista (2,44 m frente a 1,05 m). La Loma está a unos 150 m de la etapa, fuera del anillo: por eso el encargo pide suelo intacto, solo con las huellas de ellos, y no nombra el sitio histórico.
   - En calidad baja el escudo saldrá como una mancha: el borrador sirve para juzgar la composición, no la heráldica.
   - En el juego, las banderas llevarán su diseño oficial como textura, no lo que dibuje la IA.
   - Queda para la hoja de banderas: F2-07 las pide del mismo tamaño (0,91 × 1,52 m, proporción 5:3), pero el instructivo de 2009 da 3:2 a la de Ecuador ([[02_datos_pendientes]]). Hay que decidir si se iguala el alto o el paño entero, para no deformar ninguna.
7. **La marca cian en la Luna.** Solo la caja de L1 es un umbral con carga (cama ↔ Luna). En L2, L3 y L4 la marca señala el paso entre zonas, que se abren en orden (tras 3.1, 3.3 y 3.4) y se cruzan a pie.
8. **Mirador, frente a la noche del lote 03.**
   - No se pasa `ANC_HUB`, para no arrastrar su cámara lateral.
   - Se añaden el atril (MIR-05) y el descanso de llegada.
   - El anochecer se pide «azul, no morado».
   - Quedan fuera los binoculares (MIR-04) y la cúpula (MIR-08), para que la terraza se lea.
   - El portón del atajo aparece cerrado de tarde y abierto al anochecer, porque Ari lo abre tras 2.4.
   - Según §5.4, la única carga del Mirador es el ocular: del sendero se llega a pie. El descanso es la entrada visible del nodo y el sitio para una carga si el portátil la exigiera.
9. **El seguidor no aparece en el Mirador.** Falta decidir si se monta en el telescopio público o en su propio trípode (escena 2.2). Se resuelve en la versión final o en la hoja.

## 5. Costo cotizado

Salida de `python -I herramientas/hf_generar.py Nasa_Game/Fase_1_Arte/Exploracion/Lote_06/lote_06_luna_mirador.json --solo-cotizar` (no crea trabajos ni gasta). Repetida el 2026-11-14, con el mismo resultado:

```
  cotizado L06_L1_llegada_caja                  gpt_image_2_6          0.25
  cotizado L06_L2_campo_muestras                gpt_image_2_6          0.25
  cotizado L06_L3_anillo_respeto                gpt_image_2_6          0.25
  cotizado L06_L4_loma_dos_banderas             gpt_image_2_6          0.25
  cotizado L06_M1_mirador_tarde                 gpt_image_2_6          0.25
  cotizado L06_M2_mirador_anochecer             gpt_image_2_6          0.25
Total cotizado: 1.50 creditos (tope del lote: 1.5)
```

Versión final: los mismos encargos en calidad alta y 2k cotizan **2,75 créditos** cada uno (16,50 los seis, cotizados con una copia temporal del lote). Solo se proponen 2: una zona de la Luna y una luz del Mirador.

| Partida | Créditos |
|---|---:|
| 6 borradores (calidad baja, 1k) | 1,50 |
| 2 versiones finales, una por escenario (calidad alta, 2k) | 5,50 |
| **Seguro** | **7,00** |
| Una ronda de corrección de hasta 6 borradores | 1,50 |
| **Tope propuesto** | **8,50** |

- Saldo actual: **885,25 créditos**, comprobado el 2026-11-14 con `higgsfield account status`, antes y después de cotizar. Coincide con la última fila del registro de [[trabajos]] (lote 05b).
- El tope es el 0,96 % del saldo. Con el tope gastado quedarían 876,75.
- El tope no cubre repetir una versión final (2,75) ni una tercera: pedirían partida nueva.
- El archivo del lote tiene su propio tope en 1,5: `hf_generar.py` se niega a generar si la cotización lo supera.

**Comprobaciones hechas, sin gastar**

- 371 comprobaciones automáticas de las reglas de la sección 2 sobre el JSON: 0 fallos (repetido el 2026-11-14). El comprobador detectó 13 de 13 sabotajes de prueba: la Tierra o la Luna en el cuadro, «diorama», el nombre de la misión, una bandera en el sitio histórico, una bandera que toca el suelo, sin barra horizontal, sin marca cian, sin `{SIN_TEXTO}`, insignias en el traje, calidad alta, tope subido y el ancla del hub.
- Las versiones finales (los 6 encargos en calidad alta y 2k) se volvieron a cotizar el 2026-11-14: 2,75 cada una, 16,50 en total.
- Revisión escéptica de Codex, en solo lectura: 11 hallazgos.
  - 7 aplicados: umbrales dentro de la zona nítida, pasos de salida con su marca en L1, L2 y L3, pinzas pequeñas, regreso en la caja y una frase en inglés.
  - 2 aplicados a medias: la forma de la etapa y el suelo intacto de la Loma.
  - 2 descartados: nombrar en L1 el límite de 2 km y cambiar el traje por una túnica. Lo primero no se puede dibujar; lo segundo dejaría de leerse como traje.
- El registro de generaciones sigue en 38 filas, ninguna del lote 06.
- La cotización acepta encargos de hasta 20 000 caracteres, pero eso no prueba que se generen: por eso ninguno pasa de 3 350.

## 6. Qué se revisará en cada borrador

- **Escala:** altura del personaje frente al 12,5 % pedido. En `L05_A_manana_calida_final.png` ocupa cerca de un tercio del alto (medido a ojo).
- **Cuadro:** ni Tierra, ni Sol, ni cielo, ni horizonte.
- **Reglas:** ninguna letra, número, insignia o parche; solo dos personajes; ninguna bandera en L1, L2, L3, M1 y M2.
- **L4:** dos banderas, misma altura, sin tocar el suelo, 13 franjas y el amarillo al doble de alto.
- **Cian:** solo en la marca, el anillo, la chapa, los destellos y el ocular.
- **Umbral:** entero dentro del cuadro, nítido y sin objetos encima.
- **Paleta:** `python herramientas/paleta.py comparar`. El Mirador debería quedar cerca del 93,5 % del lote 03. La Luna dará bajo, como el 47 % del centro espacial: su paleta se medirá del concepto aprobado.

## 7. Lo que no se hará hasta que Guillermo apruebe

- No se genera ningún borrador ni versión final.
- No se sube ninguna imagen ni ancla. Propuesta: subir `L05_A_manana_calida_final.png` como ancla del umbral y pasarla como cuarta referencia en las versiones finales. Subir es gratis, pero necesita su permiso.
- No se crean bloques en `bloques_prompt.json`. Propuesta: `ESTILO_LUNA`, `TRAJE_LUNA`, `UMBRAL` y `REGLAS_DURAS`, con el texto que hoy se repite en los encargos.
- No se cambia la [[Biblia de arte]]. Le faltan la paleta lunar, la luz «noche lunar» y la regla del umbral.
- No se hacen las hojas de referencia de la Luna (traje, herramientas, etapa de descenso, banderas y rocas) ni se rehace `HR_MIR_v1`.
- No se modela ni se construye nada en Godot. `pruebas/luna_sueno/` sigue detenido.
- Quedan fuera de este lote las 4 tomas con cámara baja de la Luna (llegada, foto con el sitio, banderas y despedida), donde sí se ve la Tierra, y la vista del ocular.

**Después del «sí»:** generar los 6 borradores (el mismo comando sin `--solo-cotizar`), montar la lámina, medir, y pedir las 2 finales en `lote_06b_final.json` con el borrador elegido como referencia. Cada gasto se anota en [[trabajos]].

## 8. Para decidir antes de generar

1. ¿Se aprueba la partida: **7,00 seguros y tope de 8,50**?
2. ¿Se quita o se cambia alguno de los seis borradores?
3. **Bandera de Ecuador:** ¿con escudo, como está escrito, o tricolor sin escudo? Es la pregunta 3 de la Fase 2.
4. **Orden de las banderas:** ¿Ecuador a la izquierda y Estados Unidos a la derecha, o al revés?
5. **Trajes:** ¿sirve el rumbo crema, caqui, azul petróleo y aro coral, o prefieres otro color?
6. **Marca cian:** ¿en todos los pasos entre zonas de la Luna, como está escrito, o solo en la caja, que es el único umbral con carga?
7. **L3:** ¿aceptas que el concepto acerque la etapa de descenso, aunque a 75 m no entre en el cuadro de juego?

Las preguntas 3 a 7 ya tienen una opción escrita en los encargos: basta con decir «como está» o indicar el cambio.

## 9. Estado (2026-11-14)

- **Listo para presentar.** Los 4 entregables están completos: el lote, las reglas duras, la cotización y esta nota.
- **Nada generado ni subido.** Saldo 885,25 antes y después; el registro de generaciones sigue en 38 filas; en la carpeta solo están el JSON y esta nota.
- El lote no se cambió el 2026-11-14: se revisó contra el encargo, la historia (§3.1, §4 y §5), el concepto aprobado de la Habitación y la noche del lote 03, y se repitieron las comprobaciones.
- Los guiones de apoyo (`comprobar_lote06.py`, `l06_reverificar.py`, `huella_camara.py`, la copia de cotización final y el informe de Codex) están en la carpeta temporal de la sesión, no en el repositorio. Si se quieren conservar, van a `herramientas/`.
- Siguiente paso: las 7 respuestas de la sección 8. Sin ellas no se genera.
