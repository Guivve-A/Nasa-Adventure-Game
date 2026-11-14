# Fase 0 — Pipeline de personajes, criaturas y props de Higgsfield a Godot

## Resumen ejecutivo

Recomiendo **un pipeline híbrido con una base 3D reutilizable**: protagonista y NPC importantes en 3D; NPC de fondo prerenderizados desde esas mismas bases; vegetación mediante geometría sencilla y tarjetas con transparencia recortada. Para el gato, la decisión depende de validar un rig cuadrúpedo: `autosprite` sirve como alternativa inicial.

El protagonista 3D encaja mejor con el tablero, el creador de personaje y las dos cámaras previstas. Esto **no exige Forward+**: la primera prueba debe usar Compatibility, escenas pequeñas y materiales sencillos en la HD 620.

La ruta económica propuesta es Tripo H3.1 → revisión → Mixamo para humanoides → importación en Godot. El rig del gato requiere trabajo específico; no está resuelto por los scripts revisados.

Propongo una prueba escalonada de **48 créditos según las cotizaciones locales**, con techo de 60 tras recotizar los parámetros definitivos. No se generó, subió, instaló ni modificó nada. Los presupuestos de rendimiento son hipótesis: todavía falta medirlos en este equipo.

## Decisiones recomendadas

Las recomendaciones y puntuaciones son **[inf]**. Su fundamento documental se desarrolla en las secciones siguientes.

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Representación del protagonista | Modelo 3D sencillo, rig compartido y materiales reutilizables | `autosprite` como representación principal: dificulta personalización, cambios de cámara e interacciones nuevas | Media |
| Representación del gato | Modelo 3D con rig cuadrúpedo propio si supera la prueba; sprites como sustituto provisional | Aplicar directamente rig y mocap humanoides: anatomía incompatible y soporte no verificado en Higgsfield | Media |
| Representación de NPC | 3D para personajes cercanos; prerenderizado desde esas bases para población de fondo | Generar independientemente todas las direcciones y acciones: acumula inconsistencias y revisiones | Media |
| Generador 3D inicial | Tripo H3.1 por economía; multivista cuando existan vistas realmente coherentes | Tripo P2 o generación detallada como opción general: mayor costo sin beneficio demostrado a tamaño de juego | Media |
| Humanoide con rig integrado | Meshy 7 como prueba comparativa o rescate, previa verificación del servicio | Convertirlo inmediatamente en dependencia de producción: hay anuncios de retirada del modelo del proveedor | Media |
| Animación humanoide económica | Mixamo manual, una vez validada la anatomía; reutilizar clips y rig | Automatizar Mixamo mediante interfaces no oficiales: mantenimiento y fiabilidad insuficientes | Alta |
| Limpieza inicial | Pedir geometría contenida, conservar UV válidas y revisar dentro de Godot | Hacer obligatoria una cadena local de remesh y horneado antes de probar un recurso | Alta |
| Blender | Herramienta opcional; 4.5 LTS como candidata a comprobar, sin instalar ahora | Afirmar que funcionará fluidamente por tener una HD 620: el equipo también limita CPU y memoria | Alta |
| Materiales | Albedo pintado, rugosidad constante, pocos materiales; normales solo donde aporten | PBR completo, desplazamiento y varias pasadas por defecto: gasto de memoria y render innecesario | Media |
| Perfil inicial de prueba | Godot Compatibility, 1280×720 internos y una iluminación sencilla | Exigir Forward+ y SDFGI como condición del pipeline de recursos | Alta |
| Presupuesto inicial | Prueba escalonada de 48 créditos cotizados; techo propuesto de 60 | Producir personajes completos antes de validar orientación, rig, cámaras y rendimiento | Alta |

## Afirmaciones que sostienen las decisiones

1. **[doc] Godot permite 3D con Compatibility y lo orienta a equipos modestos.** Elegir personajes 3D no obliga a utilizar Forward+. **[inf]** Es el punto de partida razonable para esta prueba en la HD 620. [Documentación de renderizadores](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).

2. **[doc] Godot recomienda glTF 2.0 y admite GLB. También importa FBX mediante ufbx.** Por ello, Blender no es obligatorio para introducir un FBX de Mixamo en el motor. [Formatos 3D disponibles](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).

3. **[doc] El retargeting necesita compatibilizar nombres, jerarquía y poses de reposo.** Godot proporciona `BoneMap`, `SkeletonProfile` y `SkeletonProfileHumanoid`; igualar nombres por sí solo no basta. [Retargeting de esqueletos](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html).

4. **[doc] `AnimationLibrary` almacena animaciones y `AnimationTree` organiza sus mezclas y transiciones.** Son piezas distintas del rig y de la malla. [AnimationLibrary](https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html), [AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html).

5. **[doc] Los billboards tienen limitaciones para proyectar sombras.** Además, los materiales con alpha blending no proyectan sombras; alpha scissor sí puede hacerlo. [SpriteBase3D](https://docs.godotengine.org/en/stable/classes/class_spritebase3d.html), [Materiales 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html).

6. **[doc] Blender advierte que QuadriFlow no sustituye la topología final de un personaje deformable.** Tampoco lo recomienda para reducir una malla que ya está geométricamente bien; para eso señala Decimate. [Remallado y retopología](https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html).

7. **[doc] Los requisitos publicados de Blender incluyen cuatro núcleos y 8 GB de RAM.** El i5-7200U tiene dos núcleos según la medición suministrada. **[inf]** La compatibilidad gráfica probable no equivale a cumplir todo el mínimo ni garantiza un flujo cómodo. [Requisitos de Blender](https://www.blender.org/download/requirements/).

8. **[doc] Intel documenta soporte de APIs gráficas para esta familia, condicionado por controlador y sistema.** **[inf]** Blender 4.5 LTS es una candidata razonable por generación gráfica; su ejecución concreta con el controlador indicado sigue **sin verificar**. [APIs de Intel](https://www.intel.com/content/www/us/en/support/articles/000005524/graphics.html), [Compatibilidad de Blender](https://developer.blender.org/docs/release_notes/compatibility/).

9. **[doc] Mixamo es gratuito con Adobe ID y su autorig está destinado a humanoides.** Esto respalda usarlo para el estudiante, no para resolver automáticamente el gato. [Preguntas frecuentes de Mixamo](https://helpx.adobe.com/la/creative-cloud/faq/mixamo-faq.html).

10. **[doc] La documentación actual de Meshy anuncia la retirada de `lowpoly` el 30-10-2026 y de Meshy 7 para generación de geometría el 31-12-2026.** **[inf]** El catálogo local de Higgsfield necesita contrastarse antes de producir en serie; no debe suponerse una correspondencia idéntica entre ambos contratos. [Image to 3D API](https://docs.meshy.ai/en/api/image-to-3d).

11. **[doc] La API de rigging consultada sigue describiendo como ruta adecuada los humanoides, mientras la interfaz web documenta cuadrúpedos.** El esquema local `3d_rigging` no expone selección de anatomía. El soporte efectivo de gato mediante Higgsfield está **sin verificar**. [API de rigging](https://docs.meshy.ai/en/api/rigging), [Rigging en la interfaz web](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging).

12. **[doc local] Los precios y parámetros de Higgsfield utilizados proceden de los archivos suministrados.** Son cotizaciones, no comprobantes de generaciones completadas. No tienen una URL pública verificada: [matriz de costos](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>), [catálogo de parámetros](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>). Los errores de cotización se mantienen como **sin verificar**, nunca como costo cero.

## Riesgos y cómo mitigarlos

| Riesgo | Cómo mitigarlo | Naturaleza de la evidencia |
|---|---|---|
| Confundir acabado visual con necesidad de geometría abundante | Juzgar silueta, materiales, animación y composición a tamaño de juego antes de aumentar detalle | [inf], a partir del tablero |
| Malla chibi difícil de riggear | Brazos separados, piernas distinguibles, manos sencillas y pruebas de flexión antes de texturizar más | [inf], apoyada en requisitos de [Mixamo](https://helpx.adobe.com/la/creative-cloud/faq/mixamo-faq.html) |
| El gato consume demasiadas iteraciones | Limitar la primera prueba a idle y caminar; detener la ruta si exige reparar cada pose | [inf], soporte de rig pendiente |
| Cambios o retirada de modelos | Archivar parámetros, resultados y fecha; verificar contratos antes de cada lote | [inf], anuncio de [Meshy](https://docs.meshy.ai/en/api/image-to-3d) |
| Brillos y sombras pintados que contradicen la iluminación | Entradas con luz neutra; revisar el modelo girándolo bajo una luz de prueba; retexturizar la malla aprobada si corresponde | [inf] |
| Sprites con cambios de volumen o detalles | Comparar direcciones y fotogramas en una hoja de contacto; aprobar a escala real | [inf], guía local de animación |
| Exceso de memoria por atlas | Resoluciones pequeñas, páginas limitadas, carga por zona y evitar normales duplicadas sin beneficio visible | [inf] |
| Scripts que destruyen transparencias válidas | No aplicar indiscriminadamente sus parches `OPAQUE` a pelo, hojas, gafas o tarjetas | [doc local], auditoría de los scripts |
| Remesh que rompe UV o deformación | Hacerlo antes del rig; conservar original; revisar textura y flexiones tras cada cambio | [inf], [Blender](https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html) |
| Rendimiento aceptable solo en una escena vacía | Medir el mismo recorrido con protagonista, gato, NPC, vegetación y sombras | [inf] |
| Discos y cachés ocupan los 27 GB disponibles | Procesar un recurso cada vez; conservar originales aprobados y limitar versiones intermedias | [inf] |

## Preguntas que debe decidir el usuario

- **Cámara:** ¿la exploración tendrá orientación fija o permitirá girar? Recomiendo orientación fija durante el prototipo.
- **Personalización inicial:** ¿bastan colores de piel/pelo, ojos y dos peinados, dejando cuerpos adicionales para después? Recomiendo ese alcance.
- **Gato:** si el rig cuadrúpedo no supera la prueba, ¿se acepta temporalmente una versión con sprites?
- **Objetivo mínimo:** ¿se acepta validar primero a 720p internos y 30 FPS estables? Recomiendo hacerlo antes de exigir 1080p.
- **Prueba futura:** ¿se destinarán hasta 60 créditos al experimento descrito, con revisión de cada recurso antes del siguiente gasto?

Estas decisiones quedan planteadas para la siguiente fase de ejecución. Este informe no consume ese presupuesto.

## Desarrollo

### 1. Alcance y lectura de las referencias

Se revisaron los ocho documentos y seis scripts solicitados, el catálogo de modelos y ambos archivos de costos. Se inspeccionaron visualmente `ref_02.jpg`, `ref_08.jpg` y `ref_14.jpg`; para el resto del tablero se utiliza la descripción suministrada.

Las capturas permiten evaluar el resultado visible, pero **no demuestran cómo se construyó el juego de referencia**, qué motor empleó ni su rendimiento en este equipo. No atribuyo a esas imágenes un pipeline concreto. **[inf]**

La guía `game-flow.md` corresponde a juegos web de Higgsfield. Aquí se aprovechan sus referencias de recursos, sin trasladar su arquitectura web a Godot. **[doc local]** [Referencia revisada](<C:/Users/guill/.agents/skills/higgsfield-websites/references/game-flow.md>).

### 2. Comparación de las cuatro representaciones

#### Criterios y pesos

Escala de **1 a 5**, donde 5 es mejor. En créditos significa menor gasto; en trabajo manual, menos trabajo; en riesgo, menor incertidumbre.

| Criterio | Peso |
|---|---:|
| Fidelidad al tablero | 25 % |
| Viabilidad en HD 620 | 25 % |
| Costo en créditos | 10 % |
| Consistencia entre direcciones | 15 % |
| Flexibilidad de animación | 10 % |
| Trabajo manual | 5 % |
| Riesgo | 10 % |

**[inf]** Son puntuaciones de planificación, no resultados de una prueba. Se apoyan en las capacidades documentadas de [Godot](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html), las restricciones de [rigging](https://docs.meshy.ai/en/api/rigging) y los [costos locales](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).

- **A:** `autosprite`, cinco direcciones generadas y tres reflejadas, sobre billboard.
- **B:** todos los actores correspondientes como modelos 3D animados.
- **C:** modelos 3D prerenderizados en ocho direcciones.
- **D:** protagonista 3D; gato con rig sencillo específico; NPC cercanos 3D y población de fondo prerenderizada.

| Actor | Vía | Fidelidad | HD 620 | Créditos | Direcciones | Animación | Manual | Riesgo | Total / 5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Protagonista | A | 3 | 5 | 4 | 2 | 2 | 3 | 2 | **3,25** |
| Protagonista | B | 5 | 3 | 2 | 5 | 5 | 2 | 3 | **3,85** |
| Protagonista | C | 4 | 4 | 2 | 5 | 2 | 1 | 3 | **3,50** |
| Protagonista | D | 5 | 3 | 2 | 5 | 5 | 2 | 3 | **3,85** |
| Gato | A | 3 | 5 | 4 | 2 | 2 | 3 | 2 | **3,25** |
| Gato | B | 4 | 3 | 3 | 5 | 4 | 1 | 1 | **3,35** |
| Gato | C | 4 | 4 | 3 | 5 | 2 | 1 | 3 | **3,60** |
| Gato | D | 4 | 4 | 4 | 5 | 3 | 1 | 2 | **3,70** |
| NPC | A | 3 | 5 | 4 | 2 | 2 | 4 | 3 | **3,40** |
| NPC | B | 4 | 3 | 2 | 5 | 5 | 2 | 3 | **3,60** |
| NPC | C | 4 | 5 | 3 | 5 | 2 | 2 | 4 | **4,00** |
| NPC | D | 4 | 5 | 4 | 5 | 4 | 3 | 4 | **4,35** |

El protagonista recibe la misma puntuación en B y D porque utiliza exactamente la misma representación. La ventaja del híbrido aparece en el conjunto de la escena. La puntuación del gato D presupone que se consigue un rig sencillo reutilizable; si falla, esa ventaja desaparece. **[inf]**

#### Por qué el protagonista debe conservar una base 3D

La personalización del tablero necesita cambios de cuerpo, pelo y cara visibles desde varios ángulos. Con 3D, las variantes pueden compartir esqueleto, animaciones y materiales. Con sprites, cada cambio de silueta necesita nuevas imágenes o un sistema de capas con sus propias oclusiones. **[inf]**, apoyada en el sistema de [esqueletos y retargeting de Godot](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html).

Ejemplo de planificación: dos cuerpos y cuatro peinados producen ocho combinaciones geométricas antes de añadir ropa. El recoloreado puede abaratar piel y pelo, pero no resuelve esas diferencias de silueta. **[inf]**

Las generaciones independientes imagen→3D tampoco entregan automáticamente cuerpos intercambiables. Para producción conviene **aprobar una base, conservar sus uniones y añadir variantes compatibles**, en lugar de generar cada versión completa. **[inf]**

#### Cuándo usar C

C resulta adecuada para NPC lejanos con repertorio limitado. Primero se valida el modelo y sus animaciones; después se capturan las ocho orientaciones desde una cámara idéntica a la de juego.

No elimina el trabajo de rig: lo desplaza a la preparación. Además, el hub lateral necesita otra familia de capturas si cambia mucho la elevación de cámara. **[inf]**

### 3. Contratos de Higgsfield y selección de modelos

#### Lo que realmente expone el catálogo local

| Modelo | Controles relevantes verificados en el JSON | Consecuencia |
|---|---|---|
| `image_to_3d` | `pose_mode`, `symmetry_mode`, `target_polycount`, `topology`, textura, remesh, rig y animación | Ruta integrada; costo sin verificar |
| `multi_image_to_3d` | Controles equivalentes y varias referencias | Útil con vistas coherentes; costo sin verificar |
| `meshy_v7_image_to_3d` | `standard/lowpoly`, triángulos/quads, objetivo poligonal, textura, rig y acción | Preferir `standard`; comprobar continuidad del backend |
| `tripo_h3_1_image_to_3d` | `face_limit`, `quad`, calidad geométrica, textura, PBR y semilla de textura | Buen candidato económico; no incluye rig en este contrato |
| `tripo_h3_1_multiview_to_3d` | Controles equivalentes a H3.1 | Candidato multivista económico |
| `tripo_p2_image_to_3d` | `face_limit`, `quad`, `delight`, UV y versiones/calidades de textura | Reserva para un problema concreto que justifique el costo |
| `hunyuan3d_v3_image_to_3d` | `face_count`, `Normal/LowPoly/Geometry`, tipo de polígono y PBR | Su mínimo observado impide asumir una salida ligera |
| `3d_rigging` | `model_url`, altura, animación y `animation_action_id` | No expone selección de cuadrúpedo |
| `meshy_v5_remesh` | Objetivo, triángulos/quads, origen y altura | Servicio de remallado; no prueba calidad de deformación |
| `meshy_v5_retexture` | Referencia visual o texto; conservar UV; PBR | Corregir apariencia conservando una geometría aprobada |
| `sam_3_3d` | Referencia, detección, semilla y GLB texturizado | Sin presupuesto poligonal ni rig expuestos |
| `3d_jutsu_angles` | Referencias y prompt; salida de imagen | Ayuda a proponer vistas; no certifica una reconstrucción coherente |

**[doc local]** [Catálogo completo](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>).

No deben trasladarse parámetros entre proveedores: `face_limit`, `face_count` y `target_polycount` son campos diferentes. Tampoco aparecen controles de resolución de textura en todos estos contratos; el tamaño final deberá verificarse y, si hace falta, reducirse después. **[doc local]/[inf]**

#### Modelo recomendado por recurso

Los valores siguientes son **objetivos de prueba [inf]**, no garantías de salida. Se fundamentan en el [catálogo local](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>).

| Recurso | Primera vía | Parámetros propuestos | Revisión necesaria |
|---|---|---|---|
| Estudiante chibi | Tripo H3.1 → Mixamo | `geometry_quality=standard`, `quad=false`, `face_limit=6000`, textura activada; probar PBR desactivado | Anatomía, manos, espalda y deformación |
| Humanoide con rig integrado | Meshy 7 | `model_type=standard`, `should_remesh=true`, `topology=triangle`, `target_polycount=6000`, textura sí, PBR no, `ultra_mode=false` | Precio y disponibilidad; calidad del rig |
| Gato | Tripo H3.1; multivista si existe | `face_limit=3000`, `quad=false`, calidad estándar y textura | Cuatro patas separadas, vientre y cola |
| Prop duro singular | Tripo H3.1 | `face_limit=500–2000`, `quad=false`, textura; sin rig | Planos, agujeros, dimensiones y colisión |
| Roca o tronco | Tripo H3.1 si la silueta lo justifica | Aproximadamente 300–1200 triángulos objetivo | Evitar detalle invisible |
| Hierba y hojas | Imagen para textura + geometría simple en Godot | No generar cada mechón como malla completa | Alpha, solapamiento y lectura |
| Edificio | Módulos sencillos en Godot; IA para conceptos, materiales y piezas singulares | No comenzar con un edificio monolítico detallado | Puertas, escala, colisiones y navegación |

Para Meshy humanoide: `pose_mode=a-pose` y `symmetry_mode=auto` como primera prueba. Usar `on` únicamente en una base realmente simétrica; separar luego bolsos, herramientas o accesorios asimétricos. Elegir T-pose cuando deba coincidir con un donante concreto. **[inf]**, controles del catálogo y requisitos de [retargeting](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html).

Para Tripo, la pose y simetría deben resolverse principalmente en la imagen: esos campos no aparecen en el contrato H3.1 revisado. **[doc local]**

#### Alternativas que no usaría como punto de partida

- **Hunyuan3D v3:** la matriz registra rechazo de un objetivo inferior a 40 000 caras. Puede servir como fuente para simplificar, pero no como salida directamente ajustada a estos presupuestos.
- **Tripo P2:** 34 créditos cotizados por defecto frente a 9 de H3.1. Reservarlo para un fallo visual demostrado.
- **SAM 3D:** útil para reconstrucción exploratoria, pero sin costo ni control de complejidad verificados para esta cadena.
- **`lowpoly` de Meshy:** aunque sigue en el esquema local, el proveedor anuncia su retirada. Utilizar la ruta estándar hasta verificar qué admite Higgsfield.

**[doc local]** [Costos](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>). **[doc]** [Retiradas del proveedor](https://docs.meshy.ai/en/api/image-to-3d).

### 4. Preparación de las imágenes

#### Contrato visual propuesto

**[inf]** Aprobar una ficha con proporción de 2,5–3 cabezas, siluetas redondeadas, cabello en masas, materiales mates, textura pintada y contraste suficiente con el entorno. Aplicar esos principios a diseños originales.

Para cada recurso:

| Aspecto | Preparación recomendada |
|---|---|
| Imagen individual | Un solo objeto o personaje completo; margen alrededor |
| Fondo | Liso, sin suelo, texto ni sombra proyectada |
| Luz | Neutra y amplia; evitar contraluces y reflejos intensos |
| Humanoide | A-pose o T-pose limpia, brazos y piernas distinguibles |
| Gato | Postura neutra de cuatro apoyos, patas distinguibles y cola separada |
| Vista única | Frontal o tres cuartos sin perspectiva extrema |
| Multivista | Frente, perfil, espalda y, si procede, perfil opuesto |
| Coherencia | Misma pose, escala, ropa, longitud de extremidades y accesorios |

**[inf]**, basada en las [reglas locales de entrada](<C:/Users/guill/.agents/skills/higgsfield-websites/references/game-meshy-input-rules.md>) y las restricciones de [rigging de Meshy](https://docs.meshy.ai/en/api/rigging).

Las vistas ortográficas son una **instrucción deseada**, no una propiedad garantizada de una imagen generada. Hay que comparar anchura, altura y ubicación de detalles. `3d_jutsu_angles` puede proponer otra vista, pero también inventar lo que no se ve. **[inf]**

Una lámina con varias figuras debe dividirse en archivos individuales antes de una reconstrucción multivista. No introducirla completa como si fuese una única figura. **[doc local]** [Reglas de entrada](<C:/Users/guill/.agents/skills/higgsfield-websites/references/game-meshy-input-rules.md>).

#### Fallos típicos y correcciones

| Fallo | Corrección preferida |
|---|---|
| Dedos fusionados o deformes | Simplificar manos; separar pulgar y palma; revisar solo las poses que el juego necesita |
| Pelo con agujeros o tiras frágiles | Rediseñar en mechones sólidos; separar peinado de cabeza para personalización |
| Brazos o piernas pegados | Corregir la referencia antes de pagar rigging |
| Capa unida al torso | Separarla o reducirla a una pieza con pocos huesos; evitar simulación inicial |
| Correas, gafas o herramientas deformes | Crear piezas independientes y sujetarlas mediante nodos/huesos |
| Espalda incoherente | Añadir vista posterior revisada; no aceptar una posterior generada sin comprobar |
| Textura con luz pintada | Retexturizar la geometría aprobada; probar `delight` en P2 solo si compensa su costo |
| Plano que parece invertido | Comprobar normales, culling y transparencia por separado |
| Rig con pinzamientos | Revisar pesos y geometría; más polígonos no garantizan arreglarlo |

Son **estrategias [inf]**. Los scripts locales muestran casos concretos de confusión entre transparencia y normales; no demuestran que todos los defectos procedan de ese problema. [Guía 3D revisada](<C:/Users/guill/.agents/skills/higgsfield-websites/references/game-3d-animation.md>).

### 5. Rig y animación

#### Comparación de herramientas

| Herramienta | Papel útil | Limitación para este proyecto |
|---|---|---|
| Higgsfield `3d_rigging` | Rig y acción solicitada desde un GLB | Precio sin verificar; no hay selector cuadrúpedo en el esquema local |
| Meshy 7 integrado | Prueba de geometría, textura, rig y un clip en una solicitud | 47,5 créditos cotizados; continuidad y resultado deben verificarse |
| Mixamo | Autorig y biblioteca para humanoides | Requiere intervención manual; no resuelve el gato |
| AccuRIG | Ajuste asistido de rig humanoide | Nueva aplicación; la HD 620 no está respaldada explícitamente por los requisitos revisados |
| Cascadeur | Crear o pulir movimiento y contactos | Nueva herramienta y aprendizaje; su mínimo publicado cita una GTX 550 Ti o superior |
| Rig propio en Godot | Control directo sobre el gato sencillo | Hay que construir esqueleto, pesos y clips; no es una solución automática existente |

**[doc]** [Mixamo](https://helpx.adobe.com/la/creative-cloud/faq/mixamo-faq.html), [AccuRIG](https://manual.reallusion.com/ActorCore-AccuRIG-1/Content/ENU/1.0/03-Introducing-the-User-Interface/System_Requirements.htm), [Cascadeur](https://cascadeur.com/help/installation/system_requirements), [Skeleton3D](https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html). **[inf]** Valoración de conveniencia.

No recomiendo añadir AccuRIG o Cascadeur al pipeline obligatorio de este equipo. Su ejecución real aquí está **sin verificar**.

#### `animation_action_id`

El catálogo local confirma:

- En `image_to_3d`, animar requiere rig y un identificador entero.
- Meshy 7 tiene un identificador predeterminado, pero eso no demuestra qué movimiento conviene.
- `3d_rigging` acepta identificador y activación de animación.
- No se incluyó un catálogo local de acciones con el que verificar nombres e IDs.

Por tanto, **no asigno números de memoria**. En la futura ejecución habrá que consultar la biblioteca, elegir una acción por nombre y recotizarla. Tampoco presupongo que la envoltura de Higgsfield entregue gratis los clips básicos documentados por el proveedor. **[doc local]/[inf]** [Catálogo](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>), [API del proveedor](https://docs.meshy.ai/en/api/rigging).

#### Gato y otras criaturas

Para el gato propongo, como **diseño [inf]**, unas 20–24 articulaciones deformantes: tronco, cabeza/cuello, dos o tres segmentos por pata y una cola corta de varios huesos. Empezar con idle y caminar.

El movimiento debe revisar apoyo, elevación y retorno de cada pata. La receta sinusoidal de la referencia local es un ejemplo técnico; no demuestra una marcha felina convincente. Los scripts de dragón no son un rig de gato listo para usar. **[doc local]/[inf]** [Animación procedural](<C:/Users/guill/.agents/skills/higgsfield-websites/references/game-procedural-animation.md>).

Sin Blender puede construirse una herramienta específica con `Skeleton3D`, `Skin` y pesos sobre la malla en Godot. **La API lo permite; la herramienta todavía habría que desarrollarla y validarla.** [Skeleton3D](https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html), [Skin](https://docs.godotengine.org/en/stable/classes/class_skin.html).

Si esa prueba no produce contactos aceptables con poco trabajo, usar A provisionalmente. No consumir intentos de rig humanoide esperando que se convierta en cuadrúpedo. **[inf]**

#### Fusión de clips y auditoría de scripts

| Script | Qué hace según su código | Precaución |
|---|---|---|
| `glb_merge_anims.py` | Copia animaciones entre GLB y remapea nodos por nombre | No hace retargeting anatómico |
| `glb_inspect.py` | Informa clips, skins, materiales y escalas de raíces | No cuenta triángulos ni valida completamente el archivo |
| `fbx2glb.py` | Utiliza Blender y pistas NLA para exportar acciones | No reúne por sí solo varios FBX separados |
| `rig_transfer.py` | Alinea donante por volumen y transfiere pesos | Exige proporciones/pose compatibles; no adapta bien un humanoide a un gato |
| `pipeline.py` | Corrige texturas repetibles y deriva mapas de luminancia | No genera UV, retopología ni rig |
| `seamless.py` | Corrige repetición de una textura | No es una herramienta para hojas de personajes |

**[doc local]** [Scripts revisados](<C:/Users/guill/.agents/skills/higgsfield-websites/scripts/>).

El fusionador debe limitarse inicialmente a **GLB del mismo rig**, con nombres únicos y datos de animación convencionales. Su lectura de accessors no implementa todos los casos posibles de glTF, y la corrección de escala supone un defecto concreto. No debe borrar escalados artísticos intencionales. **[inf]**, auditoría de [glb_merge_anims.py](<C:/Users/guill/.agents/skills/higgsfield-websites/scripts/glb_merge_anims.py>).

Además, el fusionador y el conversor fuerzan materiales opacos y de doble cara. Esto puede romper recursos con transparencias válidas y aumentar trabajo de render. Para esta producción deben revisarse esos parches antes de aplicarlos a recursos con pelo en tarjetas, vegetación o gafas. **[doc local]/[inf]**

#### Importación en Godot 4.7

Ruta propuesta:

1. Importar el GLB como escena; crear una escena de personaje que lo instancie.
2. Revisar escala, orientación, altura del suelo y nombres.
3. Para clips del mismo rig, conservar sus poses de reposo.
4. Para rigs distintos, configurar `BoneMap` y un perfil compatible.
5. Importar clips reutilizables como `AnimationLibrary`.
6. Usar `AnimationTree` para idle, caminar, correr e interacción.
7. Empezar con movimiento **in place**, conducido por `CharacterBody3D`.
8. Comprobar que la velocidad de desplazamiento coincide con la zancada.

**[doc]** [Importación](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html), [retargeting](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html), [bibliotecas](https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html), [mezclas](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html). **[inf]** Organización concreta.

La documentación consultada es la rama `stable`; los pasos no se ejecutaron en la instalación local 4.7.2. Su validación práctica queda pendiente.

### 6. Limpieza sin GPU dedicada

#### Blender: versión y expectativas

**Blender 4.5 LTS es una candidata para comprobar, no una compatibilidad demostrada en esta unidad.** La familia gráfica y sus APIs permiten considerarla, pero el procesador queda por debajo de los cuatro núcleos publicados y la RAM está prácticamente en el mínimo. Cuatro hilos no equivalen a cuatro núcleos. **[doc]/[inf]** [Requisitos](https://www.blender.org/download/requirements/), [APIs de Intel](https://www.intel.com/content/www/us/en/support/articles/000005524/graphics.html).

Si posteriormente se autoriza probarla, limitarla a una malla pequeña por proceso y vista sólida. No hacer depender la aprobación de recursos de renderizados pesados. Blender 3.6 puede servir para diagnóstico de compatibilidad, pero su antigüedad y las diferencias del exportador no lo hacen mi primera elección para una cadena nueva. **[inf]**, [compatibilidad de versiones](https://developer.blender.org/docs/release_notes/compatibility/).

No se ha verificado aquí aceleración de Cycles con la HD 620. El plan debe presupuestar los horneados como tareas de CPU hasta demostrar otra cosa.

#### Qué automatizar

Con Blender, las tareas candidatas son: aplicar transformaciones, retirar componentes aislados, revisar normales, simplificar props, crear UV, transferir texturas y exportar. Son **posibilidades [inf]**; los seis scripts existentes no implementan toda esa cadena. [Documentación de remallado](https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html).

| Técnica | Uso propuesto | Limitación |
|---|---|---|
| Decimate | Props y reducción moderada de una malla válida | Puede afectar silueta, UV y articulaciones |
| QuadriFlow | Base de retopología para revisión posterior | No garantiza bucles adecuados para animación |
| Instant Meshes | Alternativa de retopología asistida | Añade otra herramienta y no entrega automáticamente rig, UV y materiales |
| `meshy_v5_remesh` | Reducir trabajo local si el resultado supera inspección | 6 créditos cotizados para quads/8000; otros ajustes deben recotizarse |

**[doc]** [QuadriFlow y Decimate](https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html), [Instant Meshes](https://github.com/wjakob/instant-meshes). **[doc local]** [Precio de remesh](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).

Los quads no son automáticamente más baratos: al triangular, 8000 quads pueden convertirse aproximadamente en 16 000 triángulos. Hay que medir la geometría final, no comparar solamente el número solicitado. **[inf]**

#### UV, horneado y toon

**[inf]** Mantener las UV generadas si pasan revisión. Si cambia la topología, comprobarlas de nuevo; no asumir que sobrevivieron. Crear UV2 solamente cuando el recurso vaya a necesitarlas.

Si se hornea una textura destinada a albedo, separar color de iluminación. Hornear una textura que ya contiene sombras no recupera por sí solo un albedo neutro. Las normales derivadas del brillo tampoco reconstruyen la forma perdida. **[inf]**, auditoría de [pipeline.py](<C:/Users/guill/.agents/skills/higgsfield-websites/scripts/pipeline.py>).

Como material inicial propongo albedo pintado, metalicidad cero y rugosidad alta constante. Probar Lambert y Toon suavizado bajo la misma luz; elegir por correspondencia con el tablero. El shader toon debe configurarse en Godot: no se debe esperar que un material arbitrario de Blender se transfiera intacto. **[inf]**, capacidades de [StandardMaterial3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html).

#### Ruta completamente sin Blender

Tripo → revisión en Godot → Mixamo manual para humanoides → FBX importado con ufbx → bibliotecas y árbol de animación.

Para C, Godot puede servir como escena de captura con cámara y tiempos fijos; hará falta una herramienta de captura, todavía no incluida en los scripts revisados. **[inf]**

Los scripts basados en la biblioteca estándar ayudan a inspeccionar y fusionar GLB, pero **no sustituyen la reparación geométrica**. Si falla la anatomía o faltan UV utilizables, hay que corregir la entrada, recurrir a otra herramienta o rechazar el recurso.

### 7. Presupuestos iniciales para la HD 620

Todos los valores son **[inf]**, límites de trabajo propuestos para la prueba. Ninguna fuente consultada permite convertirlos en una garantía de FPS para esta máquina. Base: [renderizadores de Godot](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).

| Recurso visible | Triángulos finales | Textura inicial | Huesos deformantes | Materiales |
|---|---:|---|---:|---:|
| Protagonista equipado | 4000–6000; techo de prueba 8000 | Albedo 1024² | 24–40 | 1–2 |
| Gato | 2000–3000; techo 4000 | Albedo 512² | 20–24; techo 32 | 1 |
| NPC cercano | 1500–3500 | 512² compartida cuando encaje | 24–32 | 1–2 |
| Prop pequeño | 100–500 | Atlas compartido | 0 | 1 |
| Prop singular | 500–2000 | 512² | 0–4 | 1 |
| Roca | 200–800 | 256²–512² compartida | 0 | 1 |
| Mechón de hierba | 4–12 | Atlas compartido | 0 | 1 compartido |
| Árbol cercano | 800–2000 | 512²–1024² | 0 | 1–2 |
| Módulo de edificio | 1000–4000 | Material repetible de 512²–1024² | 0 | 1–2 |

Presupuesto agregado inicial **[inf]**:

- Un protagonista, un gato y hasta cuatro NPC 3D activos.
- Unas 50 000–100 000 caras triangulares visibles como banda de prueba.
- Intentar mantenerse por debajo de 100 llamadas de dibujo; investigar al superar 150.
- Una luz direccional con sombras de alcance corto; sin luces locales con sombra inicialmente.
- Atlas de sombras de 1024 como primera prueba.
- Sin SDFGI, desplazamiento, contornos por segunda malla ni desenfoque de profundidad inicial.

La cámara alta puede hacer que hierba y tarjetas cubran muchos píxeles. Por ello, una escena con pocos triángulos todavía puede ser costosa por transparencias y solapamientos. **[doc]/[inf]** [Materiales y transparencia](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html).

### 8. Pipeline de sprites

#### Parámetros iniciales

| Recurso/acción | Resolución de cuadro | Cuadros | Reproducción propuesta |
|---|---:|---:|---:|
| Protagonista, prueba | 256² | Caminar 12; idle 8 | 12 FPS |
| Gato | 128²; comparar 256² si pierde lectura | Caminar 12; idle 8 | 12 FPS |
| NPC de fondo | 128² | Caminar 8–12; idle 4–8 | 8–12 FPS |
| Acción corta | 128²–256² | 8–12 | Ajustada a duración y contacto |

**[inf]** Valores iniciales. El contrato confirma `frame_size`, `frame_count` y las direcciones; no garantiza el aspecto del resultado. [Catálogo local](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>).

Para A:

- Usar `iso_walk_up`, `iso_walk_northeast`, `iso_walk_right`, `iso_walk_southeast` e `iso_walk_down`.
- Reflejar para northwest, left y southwest.
- `is_humanoid=false` para el gato.
- `with_sound=false`.
- Empezar con `remove_bg=default`; probar `ultra` ante un problema concreto.
- En acciones estándar no enviar `prompt` ni `name`.
- Para `kind=custom`, ambos son obligatorios.

**[doc local]** No hay acciones isométricas de ataque enumeradas en el catálogo: ese caso necesitaría `custom` o una solución distinta.

El espejo cambia la lateralidad de bolsos, marcas y herramientas. Si es narrativamente importante, habrá que generar o renderizar las ocho direcciones reales. **[inf]**

#### Turbo, pro y max

| Tier | Cotización local | Interpretación |
|---|---:|---|
| `turbo` | 2 créditos | Base económica de comparación |
| `pro` | 3 créditos | Probar sobre la misma referencia y dirección |
| `max` | 14 créditos | Solo si demuestra una mejora necesaria |

**[doc local]** [Matriz](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).

**No se verificó una tasa de parpadeo ni una superioridad de consistencia por tier.** Tampoco está demostrado qué modelo de video utiliza internamente cada uno. Un tier más caro no garantiza corregir anatomía, orientación o halos.

La guía local afirma una fuerte coherencia al animar una imagen, pero eso no garantiza identidad perfecta entre cuadros ni entre trabajos independientes. Debe tratarse como una expectativa a probar. **[inf]**

#### Atlas y memoria

**[inf]** Empaquetar con ImageMagick y metadatos de región, duración y pivote. Mantener un ancla común en los pies y un encuadre compartido; no recentrar cada cuadro por separado.

Proponer páginas de hasta 2048², con extrusión de bordes y separación suficiente para el filtrado previsto. No asumir que 64 imágenes completas de 256² caben en una página de 2048² después de añadir margen.

Cálculo sin compresión:

- 60 cuadros de 256² RGBA8: **15 MiB**, antes de huecos, bordes y mipmaps.
- 60 cuadros de 128²: **3,75 MiB**.
- Un atlas RGBA8 de 2048²: **16 MiB**; aproximadamente 21,3 MiB con cadena completa de mipmaps.
- Un atlas de normales del mismo formato añade otro volumen equivalente.

Son **[inf] por cálculo**, no mediciones de la importación final. El formato de compresión elegido por Godot puede cambiar el consumo.

#### Normales, iluminación y sombras

En un mundo 3D, `CanvasTexture` y luces 2D no sustituyen el material espacial. Para normales sobre billboard conviene un `PlaneMesh` con material propio y atlas sincronizados. En un juego estrictamente 2D sí existe la ruta de normales con `CanvasTexture`. **[doc]/[inf]** [Iluminación 2D](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html), [material espacial](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html).

Para A no se dispone de normales geométricas originales. No aplicaría `pipeline.py` a sus cuadros: convierte a RGB y trata brillo como relieve, con lo que puede perder alpha e introducir iluminación falsa. **[doc local]/[inf]**

Para C sí puede capturarse color y normales del mismo modelo y pose, mediante un proceso adicional que normalice su espacio respecto al billboard. Ese capturador todavía tendría que implementarse. **[inf]**

Primera prueba recomendada: sprite iluminado de forma sencilla, recepción de sombras del escenario y sombra de contacto separada. Si se necesita proyección real, comparar alpha scissor y una malla simplificada que solo proyecte sombra. El billboard no adquiere volumen real por tener normales. **[inf]**, límites de [SpriteBase3D](https://docs.godotengine.org/en/stable/classes/class_spritebase3d.html).

### 9. Prueba A/B mínima y presupuesto

#### Experimento propuesto

Comparar el mismo diseño original, tamaño en pantalla, recorrido y luz. Las imágenes de pose para reconstrucción y las de reposo para sprites se preparan mediante recorte/orientación cuando sea posible; si necesitan nuevas generaciones, se recotiza el conjunto. **[inf]**

| Paso futuro | Trabajo | Unidades × créditos cotizados | Subtotal |
|---|---|---:|---:|
| Referencias | Protagonista y gato con `gpt_image_2_6`, high, 1k | 2 × 1,5 | 3 |
| A, protagonista | Cinco direcciones de caminar, turbo | 5 × 2 | 10 |
| A, protagonista | Idle down, turbo | 1 × 2 | 2 |
| Comparación de tier | Repetir walk down en pro | 1 × 3 | 3 |
| A, gato | Cinco direcciones de caminar, turbo | 5 × 2 | 10 |
| A, gato | Idle down, turbo | 1 × 2 | 2 |
| B, protagonista | Tripo H3.1 | 1 × 9 | 9 |
| B, gato | Tripo H3.1 | 1 × 9 | 9 |
| **Total de referencia** | | | **48 créditos** |

**[doc local]** Precios de los casos de la [matriz](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>). **Los ajustes de polígonos y PBR propuestos no están cotizados exactamente en esa tabla:** antes de ejecutar habrá que cerrar su precio. Propongo un techo total de **60 créditos**, no afirmar que el resultado final costará exactamente 48.

El rig humanoide de B se probaría con Mixamo, sin gasto de créditos Higgsfield. El rig del gato exige una herramienta local específica o trabajo manual: **su costo en tiempo no está incluido en los 48 créditos**. Sin esa etapa, la comparación del gato sería solo visual, no una A/B de locomoción completa.

#### Orden para evitar gasto prematuro

**[inf]**

1. Aprobar las dos referencias: 3 créditos cotizados.
2. Probar una dirección turbo por actor y pro en el humanoide: 7 adicionales.
3. Revisar silueta, alpha y tier antes de completar direcciones.
4. Completar A y generar B del protagonista.
5. Validar rig humanoide y las dos cámaras.
6. Generar B del gato únicamente cuando esté definida la vía de rig.
7. Derivar C de las bases aprobadas, sin otra generación de identidad.

Si Mixamo falla, el rescate de Meshy 7 con rig y animación tiene una cotización de **47,5 créditos**. Añadirlo a los 48 elevaría el experimento a **95,5**, antes de otros ajustes; no cabe en el techo recomendado de 60. Debe ser una decisión explícita posterior. **[doc local]/[inf]**

#### Escena y puerta de aceptación

**[inf]** Preparar una zona pequeña con suelo, rocas, hierba y una estructura sencilla. Comparar A/B/C manteniendo el escenario, con protagonista, gato y cuatro NPC reutilizados. Repetir una captura lateral para el hub.

| Área | Criterio propuesto |
|---|---|
| Rendimiento | Tras calentamiento, percentil 95 de frame time ≤33,3 ms en un recorrido de 60 segundos |
| Equipo | Exportación ejecutada en la HD 620; repetir durante 10 minutos para observar degradación sostenida |
| Memoria | Registrar proceso, memoria disponible y tirones; proponer ≤1,5 GB del juego como primera meta |
| Dirección | Ningún cambio de ropa, proporción o marcas incompatible entre orientaciones |
| Animación | Sin salto de escala ni cambio de altura al pasar entre idle y caminar |
| Contacto | Pies/patas sin hundimientos notorios ni deslizamiento persistente |
| Cámaras | Lectura aceptable tanto en exploración alta como en el hub lateral |
| Trabajo manual | Registrar minutos de reparación; detener una ruta que exija rehacer cada clip |
| Usuario | Aprobar hoja de contacto y video corto antes de ampliar el repertorio |

La prueba decide si B conserva suficiente margen, si C aporta ahorro útil y si A resulta aceptable para el gato. Un promedio de FPS por sí solo no cierra esa puerta. **[inf]**

### 10. Pipeline paso a paso para producción

| Paso | Herramienta | Salida | Puerta |
|---|---|---|---|
| 1. Definir recurso | Ficha Markdown o datos de Godot | Rol, escala, cámaras, presupuesto y acciones | Alcance aprobado |
| 2. Preparar concepto | Higgsfield, modelo de imagen elegido | Referencia original | Diseño aprobado |
| 3. Preparar vistas | ImageMagick; `3d_jutsu_angles` solo si hace falta | Una figura por archivo | Vistas coherentes |
| 4. Reconstruir | Tripo H3.1 o alternativa justificada | GLB base | Silueta y anatomía válidas |
| 5. Inspeccionar | Godot y `glb_inspect.py` | Registro técnico y vista giratoria | Geometría y materiales aceptables |
| 6. Limpiar | Parámetros de generación; Blender opcional; remesh si se justifica | Malla contenida | Presupuesto cumplido |
| 7. Aprobar textura | Godot; retexture solo ante defecto | Material final | Sin luz pintada incompatible |
| 8. Riggear | Mixamo humanoide; herramienta específica para criatura | Esqueleto y pesos | Flexiones y apoyos válidos |
| 9. Animar | Biblioteca verificada o animación propia | Repertorio mínimo | Cada clip aprobado |
| 10. Organizar clips | AnimationLibrary; fusionador solo con rigs compatibles | Bibliotecas reutilizables | Nombres, escala y pistas correctos |
| 11. Integrar | Escena de personaje y AnimationTree | Actor jugable | Movimiento y animación sincronizados |
| 12. Derivar representación | Captura en Godot + ImageMagick, o autosprite | Atlas si corresponde | Cámaras y pivotes correctos |
| 13. Medir | Exportación local y monitores | Frame time, memoria y costo manual | Puerta técnica |
| 14. Registrar aprobación | Manifiesto de recursos | Versión aceptada y procedencia | Usuario aprueba producción |

Es un **procedimiento propuesto [inf]**, apoyado en los contratos locales y la [importación de Godot](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).

El manifiesto debería conservar modelo exacto, parámetros, referencia, costo cotizado/real, triángulos finales, materiales, texturas, rig, clips y estado de aprobación. El recurso aprobado debe poder reproducirse o sustituirse sin perder su contrato con el juego. **[inf]**

## Fuentes

Las etiquetas **[doc]** identifican documentación primaria; **[doc local]**, archivos revisados del proyecto o habilidad; **[inf]**, propuestas y deducciones. No se utilizó una fuente secundaria para sostener una decisión principal.

**Documentación primaria consultada**

- [Godot — Renderizadores](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).
- [Godot — Formatos 3D](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).
- [Godot — Retargeting](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html).
- [Godot — AnimationLibrary](https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html).
- [Godot — AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html).
- [Godot — SpriteBase3D](https://docs.godotengine.org/en/stable/classes/class_spritebase3d.html).
- [Godot — Materiales 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html).
- [Godot — Luces y sombras 2D](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html).
- [Godot — Skeleton3D](https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html), [Skin](https://docs.godotengine.org/en/stable/classes/class_skin.html).
- [Blender — Requisitos](https://www.blender.org/download/requirements/). Se pudo contrastar mediante resultados indexados; la apertura directa devolvió 403.
- [Blender — Compatibilidad de versiones](https://developer.blender.org/docs/release_notes/compatibility/).
- [Blender 4.5 — Remallado](https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html).
- [Intel — APIs soportadas](https://www.intel.com/content/www/us/en/support/articles/000005524/graphics.html).
- [Adobe — Mixamo](https://helpx.adobe.com/la/creative-cloud/faq/mixamo-faq.html).
- [Reallusion — Requisitos de AccuRIG 1](https://manual.reallusion.com/ActorCore-AccuRIG-1/Content/ENU/1.0/03-Introducing-the-User-Interface/System_Requirements.htm).
- [Cascadeur — Requisitos](https://cascadeur.com/help/installation/system_requirements).
- [Meshy — Image to 3D](https://docs.meshy.ai/en/api/image-to-3d).
- [Meshy — Rigging API](https://docs.meshy.ai/en/api/rigging).
- [Meshy — Rigging en interfaz web](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging).
- [Instant Meshes — Repositorio original](https://github.com/wjakob/instant-meshes).

**Archivos locales revisados**

- [hf_modelos.json](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>).
- [hf_costos_matriz.md](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).
- [hf_costos_default.md](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_default.md>).
- [Referencias de la habilidad](<C:/Users/guill/.agents/skills/higgsfield-websites/references/>): `game-3d-animation.md`, `game-2d-animation.md`, `game-meshy-api.md`, `game-meshy-input-rules.md`, `game-procedural-animation.md`, `game-stylization.md`, `game-textures.md` y `game-flow.md`.
- [Scripts de la habilidad](<C:/Users/guill/.agents/skills/higgsfield-websites/scripts/>): `pipeline.py`, `rig_transfer.py`, `glb_merge_anims.py`, `fbx2glb.py`, `glb_inspect.py` y `seamless.py`.
- [Tablero del usuario](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Referencias/Tablero_usuario/>): inspección visual de `ref_02.jpg`, `ref_08.jpg` y `ref_14.jpg`.

**Sin verificar mediante ejecución:** rendimiento de Godot 4.7.2 en la escena propuesta; funcionamiento de Blender en esta unidad; rig cuadrúpedo a través de Higgsfield; catálogo vigente de IDs de animación; superioridad visual de los tiers de `autosprite`; costos de las configuraciones ajustadas que no aparecen en la matriz.