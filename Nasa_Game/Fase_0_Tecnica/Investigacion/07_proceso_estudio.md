# Producción y validación de arte con IA — Fase 0

## Resumen ejecutivo

Se recomienda adoptar la disciplina documental y de revisión de un estudio, con un alcance adecuado para una sola persona: pocos recursos, referencias aprobadas, pruebas dentro de Godot y trazabilidad de cada gasto.

El proceso debe separar **aprobación de diseño**, **aprobación técnica** y **aprobación en contexto**. Una imagen atractiva, una malla generada o un rig automático no demuestran por sí solos que el recurso esté terminado.

Antes de producir personajes o escenarios completos, conviene demostrar una cadena pequeña: hoja coherente → recurso importable → animación funcional → cámara real → rendimiento medido. Los 1000 créditos deben administrarse mediante límites por recurso, por etapa y por proyecto, incluyendo resultados rechazados.

Este informe propone entregables, puertas, métricas y cuatro plantillas copiables a Obsidian. Los valores numéricos son **criterios iniciales propuestos**, pendientes de calibración; no son estándares AAA ni resultados de pruebas del juego.

Se consultaron documentos locales y fuentes primarias. No se modificaron archivos, instalaron programas, subieron recursos ni gastaron créditos.

## Decisiones recomendadas

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Disciplina de producción | Biblia breve, hojas ejecutables, manifiesto y evidencia por puerta. [inf] | Documentación extensa sin decisiones verificables: sobrecarga para una persona. | Alta |
| Patrón de calidad | Aprobar una pequeña familia de recursos dentro del motor y usarla como referencia. [inf] | Comparar cada generación con referentes externos diferentes: dificulta controlar la coherencia. | Alta |
| Personajes principales | Evaluar primero 3D chibi con una prueba temprana de deformación; conservar una alternativa de sprites. [inf] | Aprobar la ruta por un render estático: deja sin resolver animación, sombras y mantenimiento. | Media |
| Renderizador para validar arte | Proponer Compatibility como base de evaluación del equipo; comparar Forward+ mediante una prueba pequeña antes de comprometer efectos. [inf] | Hacer depender el acabado de SDFGI desde el inicio: no hay rendimiento local demostrado. | Media |
| Intercambio 3D | Priorizar GLB/glTF; mantener la integración en una escena propia de Godot. [doc][inf] | Depender de importación directa de `.blend`: Blender no está instalado. | Alta |
| Topología y UV | Exigir inspección y prueba de deformación después del remesh. [doc][inf] | Considerar «quads» o «low-poly» como certificados de calidad. | Alta |
| Dirección de IA | Bloques de estilo versionados, imágenes ancla propias y pruebas comparables. [inf] | Cambiar modelo, iluminación y prompt simultáneamente: impide identificar la causa de la deriva. | Alta |
| Personalización | Probar primero un cuerpo y pocas piezas intercambiables compatibles. [inf] | Generar cada combinación como personaje independiente: multiplica validaciones y gastos. | Alta |
| Créditos | Bolsa inicial de calibración de 60 créditos y reserva de 220 dentro de los 1000. [inf] | Gastar según aparezcan resultados atractivos, sin coste acumulado por recurso. | Media |
| Aprobación | Toda puerta aplicable requiere veredicto explícito del usuario sobre una versión identificada. [inf] | Interpretar silencio, entusiasmo general o aprobación del concepto como aprobación final. | Alta |

La propuesta de Compatibility requiere decidir una desviación respecto al Forward+ indicado en el plan maestro. Este informe **no cambia esa decisión ni configura el motor**.

## Afirmaciones que sostienen las decisiones

1. **[doc]** La documentación de producción debe acompañarse de puntos de evaluación claros. La descripción de esta sesión de GDC aborda precisamente las etapas de preproducción y sus requisitos de avance; no establece una plantilla universal. [GDC, preproducción y dirección de arte, 2024](https://gdcvault.com/play/1034593/Art-Direction-Summit-Pre-Production).

2. **[doc]** Las hojas de personaje sirven como referencia de construcción, vistas, poses y expresiones; el lineup comunica relaciones de escala. [Toon Boom, hojas de personaje, actualizado el 10-11-2026](https://helpcentre.toonboom.com/hc/en-ca/articles/57134612631955-Character-Design-03-Finalizing-the-character-sheets), [referencia de model sheets](https://learn.toonboom.com/modules/character-design/topic/character-model-sheets).

3. **[doc]** El desarrollo visual define personajes, mundos, color y composición en relación con la historia; las claves de color orientan posteriormente la iluminación. Son prácticas documentadas en animación, transferibles aquí como metodología, no como requisitos de un motor. [Disney, desarrollo visual](https://disneyanimation.com/process/visual-development/), [iluminación](https://www.disneyanimation.com/process/lighting/).

4. **[doc]** Valve recomienda comprobar silueta, orientación y patrones de valor dentro del juego antes de añadir complejidad de color. Se toman esos principios, sin adoptar sus diseños. [Valve, Character Art Guide](https://help.steampowered.com/en/faqs/view/0688-7692-4D5A-1935).

5. **[doc]** Godot orienta Compatibility hacia equipos antiguos o modestos. SDFGI pertenece a Forward+; las funciones disponibles cambian entre renderizadores. **[inf]** Por ello conviene validar el acabado sin depender inicialmente de SDFGI. [Godot, renderizadores](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).

6. **[doc]** LightmapGI permite iluminación precalculada de bajo coste durante la ejecución, pero el horneado integrado requiere soporte para RenderingDevice. Ejecutar lightmaps y poder hornearlos son condiciones distintas. [Godot, LightmapGI](https://docs.godotengine.org/en/stable/classes/class_lightmapgi.html).

7. **[doc]** Godot recomienda glTF 2.0 y admite GLB; importar `.blend` implica llamar a Blender instalado. [Godot, formatos 3D](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).

8. **[doc]** El remallado automático no garantiza topología adecuada para deformación. **[inf]** Un personaje generado debe superar pruebas de articulaciones antes de aprobarse para animación. [Blender 4.5 LTS, remeshing](https://docs.blender.org/manual/th/4.5/modeling/meshes/retopology.html).

9. **[doc]** Reutilizar materiales y reducir cambios de estado ayuda al renderizado; las transparencias superpuestas pueden aumentar el coste. **[inf]** Deben revisarse conjuntamente geometría, materiales, vegetación y cobertura de efectos. [Godot, optimización de GPU](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html).

10. **[doc]** ImageMagick permite extraer alfa, convertir espacios de color y comparar imágenes. **[inf]** Estas operaciones sirven como instrumentos de revisión, pero una métrica de semejanza no determina la calidad artística. [ImageMagick, opciones](https://imagemagick.org/command-line-options/), [comparación](https://imagemagick.org/compare/).

11. **[doc]** WCAG establece contraste mínimo de 4,5:1 para texto normal y 3:1 para texto grande, con condiciones y excepciones. **[inf]** Adoptar 4,5:1 para texto funcional del juego es una referencia conservadora; no certifica accesibilidad integral. [W3C, contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

12. **[doc]** Godot ofrece monitores de memoria, llamadas de dibujo y rendimiento, algunos limitados a depuración. Sus requisitos mínimos no garantizan el rendimiento de un proyecto concreto. **[inf]** La aprobación técnica necesita medición en el portátil indicado. [Godot, Performance](https://docs.godotengine.org/en/stable/classes/class_performance.html), [requisitos del sistema](https://docs.godotengine.org/en/stable/about/system_requirements.html).

## Riesgos y cómo mitigarlos

| Riesgo | Cómo detectarlo | Mitigación propuesta [inf] |
|---|---|---|
| Buen concepto, recurso imposible de animar | Hombros, cadera o patas fallan en poses simples. | Probar deformación antes del texturizado final; simplificar ropa y articulaciones. |
| Falta de herramientas de corrección | Un defecto exige editar UV, pesos o topología fuera de las herramientas actuales. | Marcar la reparación como pendiente. Usar provisionalmente primitivas, piezas rígidas o sprites; no presuponer instalaciones. |
| Deriva entre generaciones | Cambian proporciones, pincelada, materiales o rasgos de identidad. | Comparación con anclas propias bajo idénticas condiciones; modificar una variable por intento. |
| Turnaround contradictorio | Bolsillos, mechones o accesorios cambian de lado o volumen. | Resolver contradicciones en la hoja antes de generar la malla. |
| Personalización demasiado costosa | Cada peinado o cuerpo exige un rig diferente. | Un rig común, interfaces de montaje y matriz pequeña de compatibilidad. |
| Vegetación y VFX saturan la integrada | Aumenta el tiempo de cuadro al activar esas capas. | Medir por grupos; reducir capas, cobertura y materiales antes de añadir detalle. |
| Sombras incoherentes | La textura contiene una sombra fija que contradice la luz del motor. | Separar color de material y luz de escena; comprobar dos orientaciones de iluminación. |
| Gastos invisibles | Se contabiliza solo el resultado elegido. | Registrar cada trabajo, fallo, edición y reintento; reconciliar cargos. |
| Agotamiento de disco | Crecen originales, variantes y cachés simultáneamente. | Techo de almacenamiento por lote; conservar fuentes aprobadas y registrar descartes sin borrarlos automáticamente. |
| Falsa precisión de las métricas | Un recurso pasa un promedio y sigue siendo ilegible. | Combinar medición con tareas de reconocimiento a tamaño real. |
| Arte científico incorrecto | Conectores, instrumentos o diagramas parecen plausibles pero enseñan algo falso. | Verificación técnica específica antes de aprobar recursos educativos. |
| Referentes demasiado literales | Coinciden vestuario, emblemas, composiciones o interfaz distintiva. | Extraer principios y construir formas, iconografía y contexto propios. |

## Preguntas que debe decidir el usuario

Estas decisiones se presentan para revisión posterior; ninguna se considera aprobada por este informe.

- **Base técnica:** ¿se acepta evaluar Compatibility como perfil principal y Forward+ como comparación?
- **Personajes:** ¿se prioriza conservar el protagonista 3D, incluso si requiere simplificar accesorios y animaciones?
- **Interfaz:** ¿se prefiere un cuaderno científico ilustrado, pergamino estilizado o una combinación con telemetría? Recomiendo explorar primero el cuaderno ilustrado.
- **Personalización inicial:** ¿basta un cuerpo base con variaciones de piel, ojos y dos peinados para demostrar el sistema?
- **Rendimiento:** ¿se acepta como objetivo inicial 30 FPS con mundo a 1280×720 en la pantalla de 1920×1080?
- **Presupuesto:** ¿se acepta separar 60 créditos para calibración y mantener 220 de reserva?
- **Ámbito de aprobación:** ¿cada decisión puede congelarse por recurso y puerta, permitiendo revisar después solo lo que cambie?

## Desarrollo

### 1. Alcance y evidencia revisada

Se leyó el [plan maestro local](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/00_Plan_Maestro/Plan Maestro de Desarrollo AAA.pdf>), de tres páginas. Se consultaron los dos documentos de costes y los parámetros del catálogo local. Se confirmó la existencia de las 14 capturas y se inspeccionaron siete: exploración, título, obtención de objetos, hub y personalización.

Las capturas permiten estudiar composición y acabado aparente. **No permiten verificar** topología, renderizador, número de polígonos, iluminación utilizada o rendimiento del juego mostrado.

El plan sitúa dirección visual en Fase 1 y personajes en Fase 3. Aquí se define el sistema de producción y sus futuras pruebas; las propuestas de paleta, proporciones y alcance siguen pendientes.

**Convenciones del informe:**

- **[doc]:** documentación primaria.
- **[sec]:** fuente secundaria; no se necesita para las decisiones principales de este informe.
- **[inf]:** propuesta o deducción adaptada al proyecto.
- **Sin verificar:** falta evidencia suficiente.

Las fuentes web se consultaron el **12-11-2026**. Las páginas `stable` de Godot son referencias móviles: no constituyen una verificación exacta de cada comportamiento en el ejecutable 4.7.2 local.

### 2. Qué significa trabajar «como un estudio»

La unidad de producción será **un recurso con una función, una especificación y una versión verificable**. Una misma imagen puede ser un concepto aprobado y seguir sin ser una textura utilizable.

Se recomienda distinguir dos dimensiones:

| Dimensión | Ejemplos |
|---|---|
| Etapa de producción | Concepto, hoja, blockout, geometría, textura, animación, integración, pulido. |
| Estado de revisión | Borrador, en revisión, cambios solicitados, aprobado, rechazado, sustituido. |

Así se evita que «aprobado» signifique simultáneamente aprobado para modelar, aprobado visualmente y terminado.

El desarrollador prepara y mide; el asistente ayuda a detectar defectos y documentar; **el usuario aprueba la versión y la puerta concretas**. [inf]

### 3. Entregables de preproducción y contenido aprobable

No existe un paquete único obligatorio para todos los estudios AAA. La siguiente tabla sintetiza prácticas de desarrollo visual y las convierte en un contrato de producción para este proyecto. Las cantidades son propuestas de alcance. [inf; fundamentos en las afirmaciones 1–4]

| Entregable | Contenido mínimo | Condición para considerarlo aprobable |
|---|---|---|
| **Biblia de arte** | Intención narrativa; pilares visuales; lenguaje de formas; personajes, entornos, materiales, luz, UI y VFX; referencias comentadas; límites técnicos; ejemplos permitidos y rechazados; versiones. | Cada pilar se traduce en una regla observable y un ejemplo. No quedan contradicciones entre capítulos. |
| **Guía de estilo** | Resumen operativo de la biblia: proporciones, paletas, pincelada, bordes, detalle, materiales, iluminación y presentación. | Permite revisar un recurso sin reinterpretar toda la biblia. Enlaza reglas e imágenes ancla vigentes. |
| **Hoja de modelo / turnaround** | Frente, perfil, espalda y 3/4; vistas adicionales para asimetrías; pose neutra; líneas de construcción; altura en cabezas; medidas; paleta HEX; materiales; accesorios y uniones. | Las vistas describen el mismo objeto. Ningún volumen, lateralidad o material esencial queda ambiguo. |
| **Hoja de expresiones** | Neutra, alegría, concentración, duda, sorpresa y frustración; ojos y boca separados cuando corresponda; límites de deformación. | Conserva identidad y proporciones. Las expresiones se distinguen al tamaño de retrato previsto. |
| **Hoja de poses** | Reposo, caminar, observar, manipular herramienta y alcanzar; gato: reposo, marcha, atención y ayuda. Apoyos y centro de masa anotados. | La acción se reconoce por silueta y es realizable con el rig o sistema de sprites previsto. |
| **Hoja de props** | Vistas necesarias, dimensiones, materiales, variantes, punto de agarre, pivote, colisión y función interactiva. | Escala y montaje inequívocos; conectores y funciones científicas revisados cuando sean relevantes. |
| **Lineup de escala** | Protagonista, gato, NPC, puerta, mesa, instrumento y otros elementos recurrentes sobre suelo común, con regla métrica. | Todos comparten unidades y escala; la altura estilizada no vuelve inservibles mesas, puertas o agarres. |
| **Concepto de entorno** | Plano funcional sencillo; rutas; zonas transitables; masas principales; primer, segundo y tercer plano; materiales y módulos reutilizables. | El espacio se puede construir y recorrer. La composición funciona desde la cámara jugable. |
| **Color script** | Secuencia de pequeñas viñetas con emoción, momento narrativo, dominante, contraste y transición entre zonas. | Se entiende la progresión cromática al ver el conjunto reducido. No exige resolver todavía cada escenario. |
| **Claves de iluminación** | Una clave por situación importante: dirección de luz, color, relación entre luz y sombra, ambiente, niebla y tratamiento del foco jugable. | Cada efecto tiene una implementación prevista y una alternativa compatible con el perfil técnico. |
| **Style frames de UI** | HUD, misión, aviso de obtención, diálogo, mapa, título, carga y creador; jerarquía, tipografía y estados. | Textos reales en español, contraste, foco de navegación y tamaños verificables; fondos separados del texto funcional. |
| **Style frames de VFX** | Inicio, máxima intensidad y disipación; forma, color, duración, área, capas, materiales y función informativa. | Se distingue la acción que comunica y existe un presupuesto técnico. El dibujo estático no se presenta como animación validada. |

**Paquete inicial recomendado:** biblia de 8–12 páginas equivalentes, guía de dos páginas, una hoja del protagonista, una del gato, una de props, un lineup y dos encuadres de entorno. Son límites de trabajo propuestos, no requisitos de industria. [inf]

#### Proporciones y paleta de ejemplo

Para convertir «2,5–3 cabezas» en una regla ejecutable, propongo probar **2,75 cabezas**, con tolerancia inicial de **±0,10** en la hoja ortográfica. El cabello y los accesorios se miden aparte. No se debe medir esa proporción directamente en una vista con escorzo. [inf]

Esta paleta es una **hipótesis original de trabajo**, no una extracción del tablero ni una aprobación de Fase 1:

| Función | HEX de ejemplo |
|---|---|
| Tinta y contornos interiores | `#242B34` |
| Papel cálido | `#E8D9B5` |
| Tierra | `#B57A50` |
| Vegetación media | `#66834E` |
| Sombra vegetal | `#344C40` |
| Acento cálido | `#C96F3D` |
| Azul técnico | `#365B7A` |
| Gris de instrumento | `#87969C` |

La guía necesita **rampas de sombra, base y luz por material**, además de colores para piel, cabello y ojos. Ocho muestras generales no bastan para especificar todos los recursos. [inf]

### 4. Puertas comunes y cómo medirlas

#### Condiciones de prueba

Cada revisión debe identificar resolución, cámara, tamaño en pantalla, renderizador, iluminación, versión del recurso y versión de la biblia.

Se proponen dos contextos: exploración 3/4 y hub lateral. En exploración, «55°» debe definirse como **elevación sobre el plano horizontal**, evitando confundirla con el ángulo respecto a la vertical. La proyección, encuadre y distancia se congelan después del blockout aprobado. [inf]

| Criterio | Medición propuesta | Umbral inicial propuesto [inf] |
|---|---|---|
| **Silueta** | Máscara negra desde las vistas homologadas; reconocimiento de tipo y orientación en cinco capturas mezcladas. | Identificación correcta en 4/5, con exposición de dos segundos por captura. |
| **Conservación de forma** | Superponer máscara aprobada y candidata, alineadas por suelo y escala uniforme; opcionalmente calcular intersección/unión, IoU. | IoU ≥0,85 como alarma de cambio en la misma vista y pose; no sustituye revisión visual. |
| **Valores** | Captura en gris lineal y muestras de personaje/objeto frente a su fondo local. | Diferencia de mediana de luminancia ≥0,08 en los fondos de prueba, más reconocimiento correcto. Revisar contornos que se pierdan. |
| **Paleta** | Albedo o imagen neutra, con máscaras por material; comparar con sus rampas aprobadas. | ≥90% de píxeles opacos dentro de la tolerancia pactada; excepciones identificadas. |
| **Proporciones** | Puntos de referencia en vistas ortográficas: cabeza, hombros, cadera, rodillas y suelo. | Altura en cabezas acordada; relaciones principales dentro de ±5%, salvo deformación expresiva aprobada. |
| **Lectura en cámara** | Vista a tamaño real, sin ampliar, sobre tres fondos representativos. | Se reconocen orientación, rol e interacción; ningún detalle esencial depende del zoom de revisión. |
| **Densidad de téxel** | Medir UV frente a área de superficie; checker en el motor. | Objetivo inicial de 256 px/m y variación ±25% entre superficies equivalentes. Excepciones explícitas. |
| **Luz coherente** | Recurso en escena neutra y dos direcciones de luz; revisión de sombras, brillo y contacto. | Sin sombras direccionales contradictorias en albedo ni reflejos que cambien injustificadamente de material. |
| **Presupuesto técnico** | Geometría, materiales, texturas, animación y coste dentro de una escena representativa. | Cumplir la ficha y mantener la escena dentro del presupuesto aprobado. |
| **Integridad** | Importar y recorrer todas las vistas y animaciones previstas. | Sin texturas ausentes, pivotes incorrectos, recortes accidentales o errores nuevos de importación. |

Los promedios de luminancia, el IoU y la proximidad de color son **detectores de problemas**. No certifican belleza, identidad o legibilidad por sí solos. [inf]

#### Medición con ImageMagick

Ejemplos para futuras revisiones; los comandos siguientes imprimen resultados y no escriben archivos:

```powershell
# Dimensiones y canales.
magick identify -format "%f | %wx%h | %[channels]" "recurso.png"

# Estadísticas de un recorte en gris lineal.
# Sustituir tamaño y posición por la región de interés.
magick "captura.png" -crop 120x160+600+260 +repage -colorspace LinearGray -format "media=%[fx:mean] desviacion=%[fx:standard_deviation]" info:

# Caja ocupada por una silueta procedente de alfa.
magick "recurso.png" -alpha extract -threshold 50% -trim -format "caja=%wx%h desplazamiento=%X,%Y" info:

# Diferencia entre imágenes con idéntico encuadre y dimensiones.
magick compare -metric RMSE "aprobado.png" "candidato.png" null:
```

Las operaciones están documentadas por [ImageMagick](https://imagemagick.org/command-line-options/); el uso de RMSE corresponde a su [herramienta de comparación](https://imagemagick.org/compare/). **Un RMSE bajo no implica un buen diseño.**

Se verificó localmente la conversión a `LinearGray` y la lectura de estadísticas sobre una referencia. La media de la captura completa no se utilizó como criterio artístico: contiene interfaz del video, subtítulos y zonas ajenas al juego.

#### Medición con Python

La implementación puede trabajar en memoria con imágenes y máscaras. Se comprobó la disponibilidad local de Pillow y NumPy, sin instalar nada.

- **IoU:** `píxeles(A ∩ B) / píxeles(A ∪ B)`. Comparar máscaras de la misma vista y pose, sin deformar una para hacerla coincidir.
- **Proporciones:** `altura_corporal / altura_cabeza`. Guardar coordenadas de puntos y definición de cada medida.
- **Valores:** convertir sRGB a RGB lineal antes de obtener luminancia. No aplicar un umbral a una imagen cuyo contraste se haya normalizado por separado.
- **Paleta:** para cada material, calcular la distancia al color más cercano de su rampa. Como prueba inicial simple puede usarse distancia RMS en RGB lineal con tolerancia 0,10; no es una medida perceptual.
- **Estabilidad de sprite:** medir por fotograma la posición del apoyo y los puntos de identidad; distinguir desplazamiento intencional de vibración.
- **Presupuesto:** sumar bytes de archivos y dimensiones; registrar aparte memoria residente medida en Godot.

Los algoritmos y tolerancias de este apartado son propuestas **[inf]**. La gestión de espacios de color debe seguir la [documentación de ImageMagick](https://imagemagick.org/color-management/).

#### Densidad de téxel y UV

Para una textura de `W × H`, un triángulo con área UV normalizada `Auv` y área en mundo `Am²` permite estimar:

```text
densidad ≈ sqrt((Auv × W × H) / Am²)    [píxeles/metro]
```

Es una estimación escalar: debe acompañarse de un checker para detectar estiramiento direccional. Medir después de fijar la escala del recurso. [inf]

La revisión comprueba costuras visibles, distorsión, contaminación entre islas con mipmaps y asignación de resolución según visibilidad. Las UV de albedo pueden compartir zonas cuando se haya previsto; las UV destinadas a lightmaps necesitan su revisión específica. [Godot, preparación de lightmaps — doc](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_lightmap_gi.html).

### 5. Puertas específicas por tipo de recurso

Todas incorporan los criterios comunes aplicables. «No aplica» exige una explicación.

| Tipo | Comprobaciones adicionales propuestas [inf] |
|---|---|
| **Personaje 3D** | Anatomía estilizada consistente; manos y pies distinguibles; accesorios estables; prueba de hombros, cadera y rodillas; apoyos sin deslizamiento visible; transiciones entre clips. |
| **Gato 3D** | Volúmenes y patrón de pelaje coherentes; cuatro patas distinguibles cuando corresponda; cola y orejas sin deformaciones accidentales; prueba propia de rig cuadrúpedo. |
| **Sprite animado** | Alfa real; tamaño de celda y pivote estables; continuidad de ropa y rostro; ausencia de fotogramas recortados; direcciones coherentes; bucle sin salto accidental. |
| **Prop interactivo** | Escala, punto de agarre, estado activo/inactivo, colisión y reconocimiento; instrumento científicamente coherente si comunica una función real. |
| **Módulo de entorno** | Encaje entre piezas, bordes, colisión, escala de textura, ausencia de huecos y lectura de rutas. |
| **Vegetación y rocas** | Familia de formas reconocible; variación controlada; repetición poco evidente; contacto con suelo; coste con la cantidad real de instancias. |
| **UI e iconos** | Estados normal, foco, pulsado y deshabilitado; textos largos; tildes, ñ y símbolos; contraste; navegación; escalado sin cortar contenido. |
| **Mapa ilustrado** | Correspondencia con el espacio jugable, leyenda, iconos distinguibles y rutas comprensibles. |
| **VFX** | Anticipación, acción y cierre legibles; duración; oclusión de información importante; coexistencia de varios efectos; modo de movimiento reducido previsto. |
| **Título y carga** | Identidad propia, jerarquía, zonas seguras de texto y coherencia con el juego real. |
| **Piezas de personalización** | Compatibilidad con cuerpo y rig; unión de cuello y cabello; intersecciones; retrato y cuerpo consistentes; combinaciones probadas. |

Para sprites en 3D, Godot distingue recibir iluminación, transparencia y comportamiento de billboard; su documentación advierte particularidades de sombras al usar billboards. La puerta debe probar el recurso con la cámara y luz definitivas. [SpriteBase3D — doc](https://docs.godotengine.org/en/stable/classes/class_spritebase3d.html).

### 6. Etapas del recurso y validación

Los códigos `AR0–AR7` identifican puertas de arte; **no son las fases 0–7 del plan maestro**.

| Etapa | Puerta | Qué se valida antes de continuar |
|---|---|---|
| **Concepto** | AR0: intención | Función, identidad, silueta, originalidad, prioridad y techo de gasto. |
| **Hoja aprobada** | AR1: especificación | Vistas coherentes, proporciones, escala, materiales, paleta y asimetrías resueltas. |
| **Blockout** | AR2: volumen y cámara | Tamaño, encuadre, navegación, agarres, contacto y lectura con geometría sencilla. |
| **Modelo o sprite** | AR3: construcción | Forma, integridad, pivote, geometría o alfa, UV y presupuesto provisional. En personajes, prueba temprana de deformación. |
| **Textura** | AR4: superficie | Paleta, materiales, pincelada, téxel y ausencia de iluminación contradictoria. |
| **Rig y animación** | AR5: movimiento | Pesos, apoyos, continuidad, identidad temporal y acciones necesarias. En sprites equivale a revisar los clips. |
| **Integración en motor** | AR6: contexto | Cámara real, interacción, sombras, colisión, UI relacionada y coste de la escena. |
| **Pulido** | AR7: terminado | Correcciones cerradas, evidencias completas, manifiesto actualizado y aprobación final. |

La primera prueba en motor ocurre en blockout. AR6 comprueba la integración completa. [inf]

Si cambia una decisión aprobada, se reabren las puertas afectadas: modificar solo el color no exige reconstruir el rig; modificar proporciones puede afectar geometría, UV, animación y cámara. El manifiesto registra esas dependencias. [inf]

### 7. Pipeline viable con las herramientas actuales

La entrega base será GLB/glTF para 3D y PNG para imágenes/sprites, con metadatos de animación cuando corresponda. Godot documenta el soporte de glTF y sus alternativas de importación. [doc](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)

Flujo propuesto **[inf]**:

1. Resolver diseño y escala antes de pedir una malla.
2. Usar imágenes coherentes de la hoja como entrada, según el contrato real del modelo.
3. Importar el resultado en una escena de revisión pequeña.
4. Medir geometría y materiales; revisar silueta y UV.
5. Aplicar remesh únicamente si resuelve un defecto identificado.
6. Volver a comprobar forma y UV después del remesh.
7. Aprobar superficie antes de producir animaciones completas.
8. Integrar mediante una escena propia de Godot con colisión, interacción y configuración de juego.

**Límite actual:** sin Blender ni editor de imagen, puede inspeccionarse e integrarse mucho contenido, pero no debe darse por resuelta la corrección manual de topología, UV o pesos. Un recurso que necesite esas reparaciones queda en `cambios_solicitados`, con la capacidad faltante identificada.

Para props sencillos, el blockout con primitivas y materiales de Godot permite avanzar. Para personajes, piezas rígidas o sprites pueden demostrar comportamiento mientras se decide la solución definitiva. Esto no demuestra equivalencia visual con el objetivo 3D. [inf]

#### Presupuesto técnico inicial

Son límites conservadores de ensayo, **sin verificar mediante una escena del proyecto**:

| Elemento | Propuesta inicial [inf] |
|---|---|
| Protagonista | Hasta 8.000 triángulos; hasta dos materiales; albedo de 1024². |
| Gato | Hasta 4.000 triángulos; un material; albedo de 512². |
| Prop común | 100–1.500 triángulos; material compartido cuando sea viable. |
| Entorno | Texturas repetibles o atlas de 512²–1024², según cobertura real. |
| Rig del protagonista | Hasta 40 huesos deformantes como punto de partida. |
| Escena piloto | Alarma inicial en 80.000 triángulos visibles y 200 llamadas de dibujo. |
| Texturas residentes | Alarma inicial en 128 MiB. |
| Resolución | Mundo de prueba a 1280×720; UI comprobada también a 1920×1080. |
| Almacenamiento | Revisar lote al añadir 2 GiB; procurar conservar 10 GiB libres. |

Estos números no son máximos de Godot ni garantías de fluidez. Superarlos obliga a revisar evidencia; cumplirlos no garantiza rendimiento.

Los contadores de primitivas del motor pueden incluir pases adicionales y no equivalen directamente al número de triángulos originales. [Godot, Performance — doc](https://docs.godotengine.org/en/stable/classes/class_performance.html).

#### Protocolo de rendimiento

Propuesta **[inf]**:

- Probar una escena con personaje, gato, vegetación, UI y VFX simultáneos.
- Ejecutar un recorrido reproducible de tres minutos, después del calentamiento.
- Medir intervalos entre cuadros: objetivo inicial `p95 ≤ 33,3 ms` y `p99 ≤ 50 ms`, separando cargas.
- Repetir con una sesión de diez minutos para detectar degradación sostenida.
- Comparar capas activadas y desactivadas para atribuir costes.
- Medir el juego exportado y, por separado, la experiencia de edición.

Los monitores de Godot apoyan el diagnóstico; para percentiles hace falta registrar intervalos por cuadro. El FPS actualizado una vez por segundo no describe por sí solo los tirones. [doc](https://docs.godotengine.org/en/stable/classes/class_performance.html)

### 8. Manifiesto, nombres y versiones

Se recomienda una ficha Markdown por recurso como fuente de verdad y un índice generado a partir de ellas. No mantener manualmente dos registros completos contradictorios. [inf]

| Grupo | Campos |
|---|---|
| Identidad | `id`, nombre, tipo, familia, función, prioridad. |
| Producción | Fase del plan, etapa, puerta, estado, responsable. |
| Especificación | Biblia, cámara, unidades, proporciones y presupuesto técnico. |
| Generación | Proveedor, identificador exacto del modelo, parámetros, prompt enviado, referencias y semilla si existe. |
| Procedencia | Origen y permiso de las referencias; modificaciones posteriores. |
| Coste | Cotizado, reservado, cobrado, devolución confirmada y total acumulado. |
| Archivos | Fuente, derivados, ruta en motor y SHA-256. |
| Revisión | Evidencias, resultados, veredicto, aprobador, fecha y observaciones. |
| Dependencias | Recursos utilizados, versiones y puertas que deben reabrirse si cambian. |

Una URL temporal del proveedor no sustituye al archivo fuente conservado. Una semilla ausente se registra como `null`; no se inventa ni se envía a modelos que no la admiten. [inf]

Convención propuesta:

```text
ID estable:
chr_001_estudiante
cmp_001_gato
prp_014_multimetro
env_006_roca_tropical
ui_003_aviso_obtenido
vfx_002_conexion

Archivo de revisión:
<id>__<etapa>__<variante>__v###.<ext>

Ejemplos:
chr_001_estudiante__turnaround__base__v003.png
chr_001_estudiante__mesh__base__v005.glb
chr_001_estudiante__tex_albedo__base__v002.png
chr_001_estudiante__anim_walk__base__v004.glb
```

Usar minúsculas, ASCII y guiones bajos. Evitar nombres como `final_final`. Las revisiones publicadas no se sobrescriben. El archivo activo en motor puede conservar una ruta estable; la ficha identifica qué revisión y hash contiene. [inf]

Para binarios grandes, Git LFS almacena punteros en Git y el contenido por separado. **No elimina el coste local de los originales ni reemplaza una copia de seguridad.** [Git LFS — doc](https://git-lfs.com/)

Se propone versionar fichas, escenas y configuración; usar LFS de forma selectiva para fuentes binarias. Godot desaconseja versionar su caché `.godot/`. [Proceso de importación — doc](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)

Una futura validación automática puede comprobar IDs, campos, rutas, hashes, dimensiones, presupuestos y ausencia de referencias rotas. La aprobación artística seguirá siendo humana. [inf]

### 9. Dirección de arte para IA generativa

#### Biblia de prompts

Cada receta debe incluir bloques versionados y diferenciar intención visual de parámetros realmente admitidos por el modelo. [inf]

```text
RECETA: chr_turnaround_v001
BIBLIA: art_v001
ANCLAS: lista de IDs y versiones

[ESTILO FIJO]
Aventura científica ilustrada.
Volúmenes simplificados y superficies pintadas.
Detalle concentrado en rostro, manos y función del objeto.
Acabado coherente con las imágenes ancla aprobadas.

[IDENTIDAD FIJA]
Proporciones y rasgos de la hoja aprobada.
Vestuario, materiales y lateralidad de accesorios.
Elementos que deben permanecer invariantes.

[RECURSO VARIABLE]
Qué personaje, prop o entorno se necesita.
Función jugable y diferencias permitidas.

[PRESENTACIÓN]
Vista, pose, encuadre, fondo y luz de revisión.
Separación necesaria entre piezas.

[EXCLUSIONES]
Marcas ajenas, texto decorativo ilegible, accesorios adicionales,
fotorealismo y cambios de identidad no solicitados.

[SALIDA]
Resolución, formato, transparencia y cantidad solicitada.
```

`[EXCLUSIONES]` es parte de la receta textual. Solo se convierte en un campo de prompt negativo si el modelo lo admite.

En el catálogo local, `gpt_image_2_6` no expone `seed`; Tripo H3.1 expone `texture_seed`, que no debe describirse como semilla completa de geometría. `autosprite` restringe `prompt` y `name` al modo `custom`. Estos son datos del [catálogo local consultado](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>), no una comprobación del servicio en vivo.

#### Imágenes ancla

Propuesta **[inf]**:

- Una hoja propia aprobada del protagonista.
- Una hoja propia del gato.
- Una muestra de roca, suelo y vegetación.
- Un encuadre de exploración y otro de hub.
- Un frame de UI y otro de VFX.

Los referentes externos explican objetivos generales. Las anclas propias gobiernan la producción.

Después del primer modelo aprobado, sus renders ortográficos pueden reemplazar vistas contradictorias de un turnaround generado. La ficha debe distinguir entre especificación de diseño y evidencia del recurso construido.

#### Control de deriva

Evaluar cada candidato junto al último aprobado, con igual escala, luz y cámara. Registrar diferencias en cinco ejes: forma, proporción, paleta, superficie y detalle. Cambiar una variable principal por intento. [inf]

Se propone revisar el conjunto después de cada cinco recursos aprobados. Si una variante mejora la dirección general, primero se aprueba una nueva versión de la biblia y se determina qué recursos quedan afectados.

**Rechazo inmediato propuesto:**

- Contradicción entre vistas o pérdida de identidad.
- Elementos ajenos al brief.
- Anatomía o conexiones funcionales incorrectas.
- Texto falso incorporado a instrumentos educativos.
- Sombras incompatibles con el tratamiento acordado.
- Artefactos de alfa o animación que alteren la silueta.
- Recurso sin ruta viable de integración o corrección.
- Similitud demasiado literal con un diseño externo.

Un incumplimiento medible y reparable puede recibir `cambios_solicitados`; un candidato que exige rediseño vuelve a la puerta correspondiente. [inf]

### 10. Protección del presupuesto de 1000 créditos

La [matriz local](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>) describe consultas de coste con entradas de prueba. **No es un registro de consumo ni una garantía de precio futuro.**

| Operación | Cotización registrada |
|---|---:|
| GPT Image 2.6, low, 1k | 0,25 |
| GPT Image 2.6, high, 1k | 1,5 |
| GPT Image 2.6, high, 2k | 2,75 |
| Tripo H3.1 imagen→3D, defecto | 9 |
| Tripo H3.1 multivista, caso de cuatro vistas | 9 |
| Hunyuan3D v3 imagen→3D, Normal | 11 |
| Meshy 7 imagen→3D, defecto | 38 |
| Meshy 5 remesh, caso de 8000 quads | 6 |
| Meshy 5 retexturizado | 9,5 |
| AutoSprite turbo, casos consultados | 2 |
| AutoSprite pro, caso consultado | 3 |
| AutoSprite max, caso consultado | 14 |

La estimación del rigging independiente y algunas rutas 3D no está disponible en esa matriz. **Coste sin verificar** no significa gratuito. El caso Hunyuan `LowPoly quads` contiene un error de validación, por lo que no ofrece un precio utilizable.

#### Distribución propuesta [inf]

| Bolsa | Créditos |
|---|---:|
| Calibración técnica del pipeline | 60 |
| Anclas y preproducción visual | 120 |
| Personajes, props y animación prioritarios | 300 |
| Kit inicial de entorno | 120 |
| UI y VFX | 100 |
| Audio posterior | 80 |
| Reserva | 220 |
| **Total** | **1000** |

Es una distribución del presupuesto declarado; no se consultó el saldo actual. La reserva se mantiene separada hasta revisar consumo y tasa de aprobación.

#### Límites de intentos [inf]

| Etapa | Límite ordinario |
|---|---|
| Concepto de un diseño | Una generación inicial y hasta dos correcciones. |
| Conversión a malla | Una inicial y un reintento dirigido. |
| Remesh | Una operación por versión de geometría. |
| Retexturizado | Una operación por versión de geometría/UV. |
| Clip de animación | Una inicial y una corrección antes de revisar la receta. |
| Coste acumulado | Alarma en 25 créditos para recurso común y 60 para protagonista o compañero. |

Se detiene al alcanzar **el límite de intentos o el económico**, lo que ocurra primero. Renombrar una variante no reinicia el presupuesto.

Ejemplo: dos intentos Tripo de 9, un remesh de 6 y un retexturizado de 9,5 suman **33,5 créditos**, antes de conceptos y rigging. Es una simulación aritmética basada en cotizaciones locales.

Para sprites, el coste crece por acción y dirección. Cinco direcciones y dos acciones equivalen a diez trabajos: **20 créditos a 2 por trabajo**, si siguen vigentes esas condiciones. El catálogo contiene cinco direcciones isométricas nominales por varias acciones; no demuestra ocho vistas independientes ni coherencia entre ellas.

La simetría puede permitir reutilización reflejada, pero debe rechazarse cuando invierta accesorios, escritura o elementos de identidad. [inf]

### 11. Vertical slice y definición de «terminado»

#### Prueba técnica de Fase 0

Debe demostrar una cadena de producción pequeña: un prop, una muestra de superficie y una prueba mínima de personaje animado en una escena de revisión. Su aprobación responde a «¿podemos producir y validar esto en el equipo disponible?». [inf]

No equivale a aprobar diseños definitivos de las fases siguientes.

#### Vertical slice propuesto [inf]

Un recorrido de **5–8 minutos**, desarrollado cuando las puertas del plan permitan avanzar:

- Hub lateral pequeño con un personaje interactuable.
- Zona de exploración 3/4 conectada.
- Protagonista y gato con sus acciones imprescindibles.
- Entre 8 y 12 recursos de entorno reutilizables.
- Una interacción científica con efecto observable.
- HUD, objetivo, aviso de obtención y diálogo.
- Una familia de VFX y una ambientación sonora representativa.

Ejemplo de interacción: recuperar una medición ajustando un instrumento y observar cómo cambia una señal. Su exactitud científica requiere diseño y comprobación específicos; no se aprueba aquí una mecánica concreta.

El creador completo queda fuera del alcance inicial recomendado. Un cuerpo, variaciones de color y dos peinados pueden demostrar la compatibilidad de piezas.

#### «Terminado» para un recurso

- Supera las puertas aplicables.
- Se reconoce y funciona con la cámara real.
- Cumple la especificación técnica aprobada.
- No tiene defectos críticos abiertos.
- Conserva fuente, parámetros y procedencia.
- Registra todos sus gastos conocidos.
- Identifica versión, hash y dependencias.
- Tiene aprobación explícita del usuario en AR7.

#### «Terminado» para el vertical slice

Además de sus recursos, debe demostrar recorrido completo, interacción comprensible, coherencia entre escenas y rendimiento sostenido en el portátil. La producción debe poder repetirse para un segundo recurso de la misma familia sin inventar nuevamente el proceso. [inf]

### 12. Presentación para aprobación rápida

Cada revisión contendrá una lámina breve y evidencia complementaria. [inf]

| Zona | Contenido |
|---|---|
| Encabezado | ID, versión, puerta y decisión solicitada. |
| Referencia | Hoja o ancla propia aprobada; referente externo solo si explica un principio. |
| Candidato | Misma vista, escala y condiciones que la referencia. |
| Diagnóstico | Silueta, gris, paleta y detalle del defecto relevante. |
| Motor | Captura completa con cámara real; recorte 1:1 identificado aparte. |
| Semáforo | Criterio, umbral, resultado y evidencia. |
| Pie | Cambios desde la revisión anterior y coste acumulado. |

Propuesta de semáforo:

- **Verde — cumple:** criterio aplicable demostrado.
- **Amarillo — pendiente:** falta prueba o corrección; no autoriza avanzar en lo que dependa de ella.
- **Rojo — incumple:** necesita corrección o cambio de diseño.
- **N/A — justificado:** no corresponde a ese recurso.

No promediar colores para ocultar un fallo crítico. Ningún amarillo aplicable queda convertido en aprobación por defecto.

Formato de respuesta del usuario:

```text
APROBAR chr_001_estudiante v003 AR1
CAMBIOS chr_001_estudiante v003 AR1: reducir mochila; conservar rostro
RECHAZAR chr_001_estudiante v003 AR1: no corresponde a la dirección acordada
```

Para movimiento, adjuntar un clip corto a velocidad real y una vista lenta adicional. Para rendimiento, medir sin que la grabación altere la prueba. Antes de integración, la captura en motor se marca **pendiente**; un montaje ilustrado no ocupa su lugar.

### 13. Plantillas listas para Obsidian

Las cuatro plantillas siguientes son propuestas **[inf]**. Los campos vacíos no equivalen a criterios cumplidos.

#### Plantilla: ficha de recurso

```markdown
---
id: chr_001_estudiante
nombre: Estudiante
tipo: personaje_3d
familia: protagonistas
fase_plan: 0
etapa: concepto
puerta: AR0
estado: borrador
version: v001
prioridad: alta
responsable: ""
biblia_version: ""
receta_prompt_version: ""
modelo_ia: ""
semilla: null
semilla_alcance: no_disponible
coste_cotizado: null
coste_reservado: 0
coste_cobrado: null
coste_acumulado: null
techo_creditos: 60
archivo_fuente: ""
archivo_motor: ""
sha256: ""
veredicto: pendiente
aprobador: ""
fecha_veredicto: null
---

# chr_001_estudiante — Estudiante

## Función
- Función jugable:
- Qué debe reconocer el jugador:
- Diferencias permitidas:
- Invariantes:

## Especificación
| Campo | Objetivo aprobado | Medido |
|---|---|---|
| Altura y unidades | | |
| Proporción en cabezas | | |
| Triángulos o celdas | | |
| Materiales | | |
| Texturas y dimensiones | | |
| Densidad de téxel | | |
| Huesos / clips / direcciones | | |
| Cámara y tamaño en pantalla | | |

## Generación
- Proveedor:
- Modelo exacto:
- Identificador de trabajo:
- Fecha:
- Parámetros exactos:
- Semilla y alcance:
- Operaciones posteriores:

### Prompt realmente enviado
> Pegar el texto completo, sin resumir.

### Referencias
| ID / versión | Ruta o URL | Uso | Procedencia / permiso |
|---|---|---|---|
| | | | |

## Archivos y dependencias
| Papel | Ruta | Versión / hash |
|---|---|---|
| Fuente | | |
| Derivado | | |
| Motor | | |
| Evidencia | | |

- Depende de:
- Un cambio aquí obliga a revisar:

## Créditos
- Trabajos asociados: [[Registro de créditos]]
- Cotizado:
- Reservado:
- Cobrado confirmado:
- Cargos pendientes:
- Total acumulado del recurso:

## Revisión
- Puerta solicitada:
- Checklist: [[Puerta de revisión]]
- Cambios desde la versión anterior:
- Defectos abiertos:
- Decisión solicitada:
- Veredicto literal del usuario:
- Fecha y versión aprobadas:
```

#### Plantilla: lista de comprobación de puerta

```markdown
---
recurso_id: ""
version: ""
puerta: AR0
estado: pendiente
fecha: null
aprobador: ""
---

# Puerta de revisión

## Condiciones
- Biblia / receta:
- Cámara / escena:
- Renderizador:
- Resolución del mundo / de la UI:
- Tamaño del recurso en pantalla:
- Iluminación:
- Equipo:
- Versión del motor:
- Hash del recurso:

## Evidencia
- Hoja de referencia:
- Comparativa:
- Captura en motor:
- Clip:
- Registro técnico:

## Comprobaciones
Usar: VERDE, AMARILLO, ROJO o N/A con justificación.

| Criterio | Método | Umbral aprobado | Resultado | Semáforo |
|---|---|---|---|---|
| Silueta y orientación | | | | |
| Valores | | | | |
| Paleta | | | | |
| Proporciones y escala | | | | |
| Lectura en cámara | | | | |
| Téxel y UV | | | | |
| Materiales y luz | | | | |
| Geometría / alfa | | | | |
| Animación / continuidad | | | | |
| Interacción / colisión | | | | |
| Presupuesto técnico | | | | |
| Exactitud científica | | | | |
| Identidad y procedencia | | | | |

## Cierre
- [ ] Todas las comprobaciones aplicables tienen evidencia.
- [ ] Los N/A están justificados.
- [ ] No quedan incumplimientos críticos.
- [ ] Coste acumulado actualizado.
- [ ] Fuente y archivo de motor identificados.
- [ ] Aprobación explícita recibida.

## Veredicto
- Decisión: PENDIENTE / APROBADO / CAMBIOS / RECHAZADO
- Recurso, versión y puerta:
- Texto literal del usuario:
- Fecha:
- Correcciones requeridas:
- Puertas o dependencias que se reabren:
```

#### Plantilla: hoja de modelo

```markdown
---
recurso_id: ""
version: v001
estado: borrador
biblia_version: ""
unidad_mundo: metro
altura_m: null
altura_cabezas: null
---

# Hoja de modelo

## Identidad
- Nombre funcional:
- Tres rasgos invariantes:
- Función y personalidad visual:
- Elementos intercambiables:
- Asimetrías que no se pueden reflejar:

## Vistas
Todas comparten escala y línea de suelo.

| Vista | Imagen | Anotaciones pendientes |
|---|---|---|
| Frente | ![[frente.png]] | |
| Perfil | ![[perfil.png]] | |
| Espalda | ![[espalda.png]] | |
| Tres cuartos | ![[tres_cuartos.png]] | |
| Vista adicional necesaria | | |

## Construcción y medidas
| Medida | Objetivo | Tolerancia | Observación |
|---|---|---|---|
| Altura corporal sin accesorios | | | |
| Altura de cabeza sin cabello | | | |
| Altura en cabezas | | | |
| Ancho de hombros | | | |
| Línea de cadera | | | |
| Altura de rodilla | | | |
| Tamaño de manos y pies | | | |

## Paleta
Especificar HEX sRGB; no confiar en texto generado dentro de la imagen.

| Material / zona | Sombra HEX | Base HEX | Luz HEX |
|---|---|---|---|
| Piel / pelaje | | | |
| Cabello | | | |
| Ropa principal | | | |
| Accesorios | | | |

## Materiales
| Zona | Material | Brillo / rugosidad previstos | Detalle permitido |
|---|---|---|---|
| | | | |

## Montaje y movimiento
- Pose neutra:
- Pivote:
- Puntos de agarre:
- Piezas separadas:
- Articulaciones críticas:
- Límites de deformación:
- Colisión prevista:

## Expresiones y poses
- [[Hoja de expresiones]]
- [[Hoja de poses]]
- [[Lineup de escala]]

## Cámara real
- Cámara / encuadre:
- Altura aproximada en píxeles:
- Rasgos que deben sobrevivir a esa escala:
- Evidencia de blockout:

## Aprobación AR1
- [ ] Vistas coherentes.
- [ ] Proporciones medibles.
- [ ] Materiales y paleta completos.
- [ ] Asimetrías resueltas.
- [ ] Función, escala y montaje claros.
- [ ] Veredicto explícito sobre esta versión.

- Veredicto:
- Aprobador:
- Fecha:
```

#### Plantilla: registro de créditos

```markdown
---
presupuesto_inicial: 1000
fecha_inicio: null
saldo_proveedor_consultado: null
fecha_saldo_proveedor: null
---

# Registro de créditos

## Bolsas
Son asignaciones de planificación, no cargos.

| Bolsa | Asignado | Cobrado confirmado | Reservado pendiente |
|---|---:|---:|---:|
| Calibración | 60 | 0 | 0 |
| Anclas y preproducción | 120 | 0 | 0 |
| Personajes, props y animación | 300 | 0 | 0 |
| Entorno | 120 | 0 | 0 |
| UI y VFX | 100 | 0 | 0 |
| Audio | 80 | 0 | 0 |
| Reserva | 220 | 0 | 0 |
| Total | 1000 | 0 | 0 |

## Trabajos
Una fila por trabajo, incluidos fallos y resultados rechazados.
"N/D" significa cargo todavía desconocido, nunca cero.

| Fecha | ID trabajo | Recurso / versión | Operación / modelo | Parámetros o enlace | Cotizado | Reserva pendiente | Cobrado | Devuelto confirmado | Resultado / decisión |
|---|---|---|---|---|---:|---:|---:|---:|---|
| | | | | | | | N/D | 0 | |

## Conciliación
- Cobrado confirmado acumulado:
- Devoluciones confirmadas:
- Consumo neto:
- Reservas todavía pendientes:
- Trabajos con cargo desconocido:
- Disponible para nuevos trabajos:
- Diferencia con saldo del proveedor:
- Explicación de la diferencia:

## Reglas de cálculo
Consumo neto =
cargos confirmados - devoluciones confirmadas.

Disponible de planificación =
1000 - consumo neto - reservas todavía pendientes.

No contabilizar simultáneamente un cargo y su antigua reserva.
No anticipar devoluciones.
Si un trabajo sigue sin cargo conocido, mantener su reserva.

## Eficiencia
- Recursos aprobados:
- Coste de trabajos asociados a esos recursos:
- Coste total de intentos, incluidos descartes:
- Horas de reparación:
- Causas recurrentes de rechazo:

## Cambios de presupuesto
| Fecha | Bolsa origen | Bolsa destino | Créditos | Motivo | Aprobación |
|---|---|---|---:|---|---|
| | | | | | |
```

## Fuentes

**Documentación primaria y prácticas de producción**

- **[doc]** [GDC 2024: preproducción y dirección de arte](https://gdcvault.com/play/1034593/Art-Direction-Summit-Pre-Production). Se consultó la descripción pública; no se atribuye contenido no revisado de la charla.
- **[doc]** [Toon Boom: finalización de hojas de personaje](https://helpcentre.toonboom.com/hc/en-ca/articles/57134612631955-Character-Design-03-Finalizing-the-character-sheets). Actualizado el 10-11-2026.
- **[doc]** [Toon Boom: Character Model Sheets](https://learn.toonboom.com/modules/character-design/topic/character-model-sheets).
- **[doc]** [Disney: desarrollo visual](https://disneyanimation.com/process/visual-development/) e [iluminación](https://www.disneyanimation.com/process/lighting/). Referencias de animación; su adaptación al proyecto está identificada como inferencia.
- **[doc]** [Valve: Character Art Guide](https://help.steampowered.com/en/faqs/view/0688-7692-4D5A-1935). Principios de silueta y valores; fecha de actualización sin verificar.

**Documentación técnica**

- **[doc]** Godot: [renderizadores](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html), [requisitos](https://docs.godotengine.org/en/stable/about/system_requirements.html), [formatos 3D](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).
- **[doc]** Godot: [LightmapGI](https://docs.godotengine.org/en/stable/classes/class_lightmapgi.html), [preparación de lightmaps](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_lightmap_gi.html), [SpriteBase3D](https://docs.godotengine.org/en/stable/classes/class_spritebase3d.html).
- **[doc]** Godot: [optimización de GPU](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html), [Performance](https://docs.godotengine.org/en/stable/classes/class_performance.html), [proceso de importación](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html).
- **[doc]** [Blender 4.5 LTS: remeshing](https://docs.blender.org/manual/th/4.5/modeling/meshes/retopology.html). Limitación del remallado automático verificada en el contenido indexado; no se comprobó ejecución local de Blender.
- **[doc]** ImageMagick: [opciones](https://imagemagick.org/command-line-options/), [gestión de color](https://imagemagick.org/color-management/), [comparación](https://imagemagick.org/compare/).
- **[doc]** [W3C: contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- **[doc]** [Git LFS](https://git-lfs.com/).

**Fuentes locales**

- [Plan maestro](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/00_Plan_Maestro/Plan Maestro de Desarrollo AAA.pdf>): fases, dirección general y puertas de validación.
- [Matriz de costes](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>) y [costes por defecto](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_default.md>): cotizaciones registradas, no consumo real.
- [Catálogo de parámetros](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>): restricciones y campos disponibles en la captura local.
- [Tablero del usuario](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Referencias/Tablero_usuario/>): evidencia visual; técnicas internas y rendimiento del juego mostrado, **sin verificar**.