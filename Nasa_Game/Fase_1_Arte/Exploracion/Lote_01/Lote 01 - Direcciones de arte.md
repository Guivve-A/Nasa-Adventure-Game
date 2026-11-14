---
tipo: lote de arte
fase: 1
lote: L01
fecha: 2026-11-12
estado: espera el veredicto de Guillermo
creditos: 19.25
---

# Lote 01 — Direcciones de arte

Primera exploración con Higgsfield. Guillermo pidió empezar los diseños y probar «lowpoly, o cualquier otra forma recomendada».

**Qué se decide con este lote:** el lenguaje visual del juego. Todavía no se deciden personajes, cámara ni paleta final.

## Método

- **Una sola escena para comparar:** el cuarto-taller del estudiante en Guayaquil al atardecer, en vista lateral de diorama. Aparecen el estudiante, el gato con su placa cian, el libro con el holograma, el banco de electrónica y el cerro con el faro sobre el río.
- **Cuatro direcciones:** low-poly pintado, gouache, maqueta y papel.
- **Tres modelos de imagen** con el mismo encargo de low-poly, para elegir el motor.
- **Una vista de juego** en low-poly, con cámara alta.

![[Lote_01_lamina_comparativa.jpg]]

## Las imágenes

### A1. Low-poly pintado a mano

![[L01_A_lowpoly_hub_gpt26.png]]

- **Qué es:** geometría facetada, un degradado pintado en cada cara, luz cel con borde luminoso.
- **A favor:** siluetas limpias que se leen a tamaño de juego. Es la más barata de producir en 3D: pocas caras y degradados en lugar de texturas detalladas.
- **Riesgo:** si las facetas son muy grandes puede verse genérico. Lo evita la textura pintada.

### A1 en vista de juego

![[L01_A_lowpoly_exploracion_gpt26.png]]

- Escalinata de un barrio en el cerro, con iguana, ceibo, cables, ropa tendida, mosaicos, el río y el malecón.
- La cámara salió más baja que la del tablero. Sirve para juzgar el estilo, no el encuadre.

### B. Gouache de taller

![[L01_B_gouache_hub_gpt26.png]]

- **Qué es:** formas suaves con pincelada opaca visible en todas las superficies y acabado mate.
- **A favor:** es la más cercana al tablero de referencia y la más cálida.
- **Riesgo:** mantener la misma pincelada en todos los recursos.

### C. Maqueta de cerámica y aluminio

![[L01_C_maqueta_hub_gpt26.png]]

- **Qué es:** figuras como cerámica esmaltada, metal satinado y desenfoque de maqueta.
- **A favor:** es la de aspecto más lujoso y tangible.
- **Riesgo:** exige el renderizado más costoso (materiales finos y desenfoque) y modelos con más detalle. Depende del PC en la nube.

### D. Atlas de luz y papel

![[L01_D_atlas_papel_hub_gpt26.png]]

- **Qué es:** capas de papel recortado con borde rasgado, tinta y croquis de ingeniería en las paredes.
- **A favor:** es la identidad más original y conecta con una interfaz de cuaderno de ingeniería.
- **Riesgo:** integrar personajes 3D en un mundo de papel. Pide cámaras muy controladas.

### A2 y A3. El mismo encargo de low-poly en otros modelos

![[L01_A_lowpoly_hub_nbpro.png]]

- **A2, Nano Banana Pro:** lo interpretó como caricatura isométrica con contorno. Es la de menor acabado. En el estante dibujó una consola portátil parecida a un producto comercial: ese objeto no se usa.

![[L01_A_lowpoly_hub_seedream55.png]]

- **A3, Seedream 5.5:** no hizo low-poly, sino 3D cinematográfico con haces de luz. Sirve como meta de iluminación para cualquier dirección.

## Conclusiones de dirección de arte

1. **Motor de imagen:** GPT Image 2.6 es el que mejor sigue el encargo. Seedream 5.5 queda para claves de iluminación.
2. **Las cuatro direcciones son viables** y no muestran defectos en manos, caras ni objetos al ampliarlas.
3. **Recomendación:** mezclar A1 y B. Formas low-poly con textura de gouache en las caras, la luz de A3 como meta y la interfaz de cuaderno de D.
4. **Contenido para conservar:** el cerro con el faro, el holograma cian del libro, la placa cian del gato, la buganvilla, la iguana y el ceibo.

## Registro del lote

| Imagen | Modelo | Ajustes | Créditos |
|---|---|---|---:|
| `L01_A_lowpoly_hub_gpt26` | GPT Image 2.6 | high, 2k, 16:9 | 2,75 |
| `L01_A_lowpoly_hub_nbpro` | Nano Banana Pro | 2k, 16:9 | 2,00 |
| `L01_A_lowpoly_hub_seedream55` | Seedream 5.5 | 2k, 16:9 | 3,50 |
| `L01_B_gouache_hub_gpt26` | GPT Image 2.6 | high, 2k, 16:9 | 2,75 |
| `L01_C_maqueta_hub_gpt26` | GPT Image 2.6 | high, 2k, 16:9 | 2,75 |
| `L01_D_atlas_papel_hub_gpt26` | GPT Image 2.6 | high, 2k, 16:9 | 2,75 |
| `L01_A_lowpoly_exploracion_gpt26` | GPT Image 2.6 | high, 2k, 16:9 | 2,75 |
| **Total** | | | **19,25** |

Los encargos completos están en `lote_01a_modelos.json` y `lote_01b_direcciones.json`. El registro de todas las generaciones está en `Fase_1_Arte/registro_generaciones.json`.

## Veredicto de Guillermo (2026-11-12)

> «Me quedo con el estilo de una mezcla entre L01_A_lowpoly_exploracion_gpt26 para la exploración y L01_A_lowpoly_hub_gpt26.»

- [x] **Dirección elegida: A1, low-poly pintado a mano.** La imagen del hub fija el estilo del hub y la de exploración fija el de la exploración.
- [x] **Tipo de juego:** exploración, mapa mediano y 2D-HD, como las capturas del tablero: cámara alta con el personaje pequeño ([[ref_05.jpg]]) y mapa ilustrado de la región ([[ref_04.jpg]]).
- [x] Descartadas como dirección principal: B, C, D, A2 y A3.

Las dos imágenes elegidas pasan a ser las **anclas de estilo** de todos los lotes siguientes.
