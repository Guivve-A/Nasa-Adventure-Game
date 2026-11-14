# De los referentes a una identidad propia: dirección de arte viable para «Proyecto NASA-Ecuador»

## Resumen ejecutivo

Recomiendo un **diorama pintado con personajes 3D de unas tres cabezas, cámaras controladas y escenarios compactos**. Es la combinación más cercana al tablero y permite reservar el esfuerzo para composición, siluetas, color y animación.

Los referentes ofrecen soluciones diferentes: *Bravely Default* convierte ilustraciones en espacios con profundidad; *Link’s Awakening* regula el detalle según una escala de miniatura; *Octopath Traveler* integra sprites y escenarios mediante iluminación; *Monster Hunter Stories 2* utiliza proporciones e iluminación para cambiar el tono del mundo.

Sus apariencias pueden orientar el proyecto, pero sus motores y efectos no constituyen presupuestos adecuados para la Intel HD 620. Propongo una base visual que funcione sin SDFGI ni desenfoque en tiempo real.

Presento tres direcciones originales para Fase 1: **Gouache de taller**, **Maqueta de cerámica y aluminio** y **Atlas de luz y papel**. Recomiendo comenzar comparando las dos primeras.

Los FOV, conteos de triángulos y densidades de téxel comerciales que no pude verificar quedan identificados expresamente. No se modificaron archivos ni se consumieron créditos de Higgsfield.

## Decisiones recomendadas

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Lenguaje visual principal | Diorama pintado, superficies mates y personajes 3D. [inf; fuentes: Bravely y miniaturas][bravely] | Reunir acabados de todos los referentes: produciría reglas incompatibles de materiales, escala y detalle. | alta |
| Proporciones | Probar **3 cabezas** para protagonista y NPC humanos; distinguir edad y oficio mediante silueta, postura y vestuario. [inf; contexto de proporciones][second] | Usar automáticamente las proporciones alargadas de *Stories 2*: se alejan del tablero. | media |
| Cámara de exploración | Ensayar ortogonal y perspectiva moderada con el mismo encuadre; comenzar alrededor de **55° de inclinación hacia abajo desde la horizontal**. Es una propuesta propia. [inf][camera] | Cámara libre permanente: exige resolver más superficies, oclusiones y composiciones. | alta |
| Cámara del hub | Vista lateral oblicua, con pocos planos de profundidad y fondos ilustrados propios. [inf; principio de construcción pictórica][bravely] | Construir una ciudad completa visible desde cualquier dirección: amplía el trabajo fuera del encuadre útil. | alta |
| Sombreado | Color pintado + iluminación sencilla; toon suave opcional para personajes. [inf][material] | Cel muy duro y contorno negro grueso en todo: puede ocultar expresiones y competir con instrumentos pequeños. | media |
| Base de renderizado | Validar primero el aspecto en **Compatibility**, sin depender de SDFGI ni DOF. [doc/inf][renderers] | Convertir Forward+ y sus efectos avanzados en requisito estético antes de medir el portátil. | alta |
| Interfaz | Cuaderno científico contemporáneo: papel, anotaciones y trazos propios; conservar DotGothic16 y comprobar su lectura en español. [inf; licencia y origen de la fuente][font] | Trasladar literalmente el pergamino medieval y la ornamentación de los referentes. | alta |
| Producción | Aprobar cámara, proporción, paleta y material en una escena pequeña antes de generar familias de recursos. [inf; antecedentes de iteración visual][octotalk] | Aprobar modelos aislados por su atractivo en una imagen de presentación. | alta |
| Identidad original | Diseñar desde observación local, funciones científicas y una gramática propia de formas. [inf; límite idea/expresión][can351] | Cambiar colores o accesorios de diseños comerciales reconocibles. | alta |

## Afirmaciones que sostienen las decisiones

1. **[doc]** En *Bravely Default*, se dibujaron primero fondos 2D muy elaborados y después se resolvió su representación con profundidad estereoscópica. Los desarrolladores distinguen este trabajo del de sus mazmorras 3D convencionales. [Entrevista original, 2012][bravely]

2. **[doc]** *Bravely Second* elevó ligeramente las proporciones de todos los personajes; sus creadores explican que los cuerpos más compactos del anterior favorecían reconocer las caras cuando aparecían pequeñas. [Entrevista original, 2014][second]

3. **[doc]** *Bravely Default II* tomó como objetivos visuales ciudades de papel y campos semejantes a una maqueta ferroviaria. No debe describirse toda la saga como un único sistema de fondos estáticos. [Entrevista al productor, 2020/2021][bd2]

4. **[doc]** La dirección gráfica de *Link’s Awakening* imaginó a Link como una figurita de unos diez centímetros y limitó el detalle para conservar esa escala. [Blog oficial de Nintendo][la]

5. **[doc]** Los responsables de *Monster Hunter Stories 2* relacionan sus personajes más maduros y la mayor profundidad de iluminación con el objetivo de ampliar su público. [Entrevista a Capcom, 2021][mhs]

6. **[doc]** *Octopath Traveler* combina personajes 2D con entornos 3D; sus artistas añadieron luces puntuales a efectos de combate para que luz y sombra integraran a los personajes en el escenario. [Entrevista de Unreal Engine, 2019][octo]

7. **[doc]** La cámara giratoria de *Triangle Strategy* planteó un problema específico de compatibilidad visual con sus personajes de píxeles. [Entrevista a sus productores, 2022][triangle]

8. **[doc]** La charla GDC de *Guilty Gear Xrd* identifica el control manual de normales de vértice como una herramienta importante para dirigir el cel shading. Esto demuestra una técnica general; no demuestra que los juegos aquí estudiados empleen esa implementación. [Material de GDC, 2015][gdc]

9. **[doc]** Godot orienta Compatibility al hardware antiguo o de prestaciones bajas. Su tabla documenta SDFGI exclusivamente en Forward+ y DOF en Mobile/Forward+, pero no en Compatibility. **[inf]** Conviene que el aspecto básico del proyecto sobreviva sin esos efectos. [Documentación oficial consultada][renderers]

10. **[doc]** Godot advierte que el rendimiento no depende solamente de polígonos: también importan materiales, cambios de estado, llamadas de dibujo y trabajo por píxel. [Optimización de GPU][gpu]

11. **[doc]** DotGothic16 se inspira en caracteres bitmap de 16 × 16 y se distribuye bajo SIL Open Font License. **[inf]** Encaja especialmente bien con instrumentación y anotaciones digitales, previa comprobación de legibilidad. [Repositorio oficial][font]

12. **[doc]** El artículo 7 de la Decisión Andina 351 distingue las ideas de su expresión concreta. **[inf]** Pueden estudiarse principios como miniaturización o sombreado por bandas sin reproducir personajes, ilustraciones, mapas ni interfaces particulares. [Texto primario][can351]

## Riesgos y cómo mitigarlos

| Riesgo | Mitigación |
|---|---|
| Confundir apariencia con implementación | Etiquetar las lecturas visuales como [inf]. Un borde oscuro no demuestra casco invertido; una sombra suave no demuestra lightmap. |
| Diseñar alrededor de efectos demasiado costosos | Aprobar primero una escena sin GI dinámica, DOF ni contornos de pantalla completa. Añadir efectos después de medir. [inf][renderers] |
| Personajes y fondos de familias visuales distintas | Compararlos juntos bajo la cámara final. Igualar escala de pincelada, contraste, saturación y respuesta a la luz. [inf; contexto de integración][octo] |
| Generaciones de IA atractivas pero inconsistentes | Usar una ficha aprobada de proporciones, formas, materiales y paleta; revisar cada recurso en escena antes de producir variantes. [inf] |
| Vegetación que domina el coste | Distribuirla por grupos pequeños y limitar capas solapadas. MultiMesh reduce llamadas, pero su agrupación también afecta al descarte por visibilidad. [doc/inf][multimesh] |
| Interfaz decorativa difícil de leer | Probar texto real en español, números y unidades a tamaño de juego. *Bravely Default II* revisó fuente, colores y fondos después de problemas de lectura en portátil. [doc][bd2ui] |
| Desdibujar la ciencia mediante estilización | Exagerar carcasas y siluetas; conservar relaciones funcionales: conexiones, piezas móviles, escalas, unidades y señales. [inf] |
| Parecido excesivo con una franquicia | Revisar conjuntamente silueta, vestuario, paleta, iconografía y composición; cambiar solo un elemento no garantiza independencia. [inf][can351] |
| Suponer que toda imagen espacial es reutilizable | Comprobar cada recurso: las condiciones de NASA distinguen contenido general, materiales de terceros, identificadores y usos promocionales. [doc][nasamedia] |

## Preguntas que debe decidir el usuario

1. **Dirección dominante:** ¿Gouache de taller, Maqueta de cerámica y aluminio o Atlas de luz y papel? Recomiendo **Gouache de taller** como primera candidata.
2. **Grado de miniaturización:** ¿personajes de tres cabezas claramente chibi o algo más alargados para representar al estudiante universitario?
3. **Superficie:** ¿pincelada visible y mate o volúmenes más limpios con pequeños brillos de material?
4. **Movimiento de cámara:** ¿encuadre fijo por zona o rotaciones limitadas en puntos concretos?
5. **Interfaz:** ¿cuaderno material predominante o combinación de cuaderno y paneles de instrumentación?
6. **Cambios horarios:** ¿atmósferas preparadas por escena o un ciclo continuo? La primera opción reduce las situaciones visuales que habrá que resolver. [inf]

## Desarrollo

### 1. Alcance y método de lectura

Se revisaron las catorce capturas del tablero local. La investigación se centra en:

- *Monster Hunter Stories* original de 3DS y *Stories 2* de Switch.
- Las versiones de Pokémon solicitadas.
- *Ocarina of Time 3D* de 3DS y los Zelda citados de Switch.
- *Bravely Default* y *Bravely Second* de 3DS; *Bravely Default II* de Switch.
- *Octopath Traveler*, *Triangle Strategy* y, como referencia principal de *Ni no Kuni*, **Wrath of the White Witch**.

Se diferencia la evidencia del remaster de la del lanzamiento original. Tampoco se trasladan las técnicas de *Ni no Kuni II* o *Cross Worlds* al primer juego.

**Etiquetas utilizadas:**

- **[doc]:** documentación primaria, declaraciones originales de desarrolladores o material publicado por sus responsables.
- **[sec]:** reseña, análisis independiente o reseña de artbook.
- **[inf]:** interpretación visual, deducción o propuesta de producción propia.

Una entrevista publicada por un medio constituye evidencia primaria cuando se atribuye una declaración a sus desarrolladores. La opinión del redactor sigue siendo secundaria.

La preferencia por 2025–2026 se aplica cuando aporta información pertinente: por ejemplo, la retrospectiva oficial de *Bravely Default* de 2025. Para técnicas de juegos históricos resultan más útiles sus entrevistas y presentaciones originales. [doc][bd2025]

#### Límites cuantitativos

| Dato solicitado | Resultado verificable |
|---|---|
| FOV exacto | **Sin verificar** para los títulos estudiados. No se atribuyen grados comerciales inventados. |
| Inclinación exacta | **Sin verificar**. Se describe como baja, media o alta según el encuadre habitual. |
| Cabezas por personaje | Rangos visuales orientativos **[inf]**, no especificaciones oficiales. Se refieren a humanos representativos, no a toda la población. |
| Triángulos por modelo | **Sin verificar** para las mallas comerciales. La suavidad aparente no permite recuperar su topología. |
| Geometría de sprites | La presentación de *Octopath* documenta seis vértices en los datos de dibujo de PaperSprite; no es un presupuesto de toda la escena. [doc][octotalk] |
| Téxeles por metro | **Sin verificar**. Se analiza la frecuencia visual del detalle, no una densidad medida. |
| Familias tipográficas exactas | **Sin verificar** por versión e idioma. Se describen categorías y funciones visuales. |
| Reparto entre luz horneada y dinámica | Solo se afirma cuando hay evidencia explícita; pintura, oclusión y lightmaps no se consideran equivalentes. |

Los presupuestos numéricos propuestos al final pertenecen **al proyecto**, no a los juegos comerciales.

### 2. Deconstrucción de los referentes

Las observaciones de cada ficha son **[inf]**, salvo las frases identificadas como [doc] o [sec]. Las fuentes enlazadas permiten distinguir la presentación visible de las declaraciones sobre su construcción.

#### 2.1. Monster Hunter Stories — 3DS

- **Cámara y proporción:** perspectiva de tercera persona, elevada y variable; no es una vista isométrica rígida. El protagonista infantil se lee aproximadamente en **3,5–4,5 cabezas**.
- **Modelado y sombreado:** masas compactas, cabello agrupado, extremidades simplificadas y equipamiento reconocible por silueta. Apariencia toon con separación marcada de luces y sombras y bordes oscuros en personajes; implementación de rampas y contornos **sin verificar**.
- **Textura y color:** detalle pintado de escala grande, colores locales claros y separación entre piel, ropa y equipamiento. El detalle pequeño tiene menor protagonismo que las masas.
- **Luz y fondos:** escenarios 3D organizados por zonas, con profundidad atmosférica y decorado que encuadra el recorrido. Reparto horneado/dinámico **sin verificar**.
- **UI y economía:** iconos grandes y texto de lectura directa; el diseño original aprovechaba dos pantallas. La compartimentación y simplificación de formas son principios aprovechables para controlar lo visible. **[doc]** Capcom confirma que la interfaz tuvo que reconstruirse para el remaster de una pantalla. [Entrevista][mhsui]

**Aplicación:** conservar la claridad de oficio y equipamiento; diseñar un gato científico con anatomía, accesorios y gestos propios.

#### 2.2. Monster Hunter Stories 2 — Switch

- **Cámara y proporción:** tercera persona en perspectiva, con mayor presencia del horizonte y puesta en escena cinematográfica. Humanos jóvenes aproximadamente de **5–6 cabezas**.
- **Modelado y sombreado:** siluetas más alargadas, caras y cabello diseñados para primeros planos; toon combinado con transiciones ambientales suaves. No puede certificarse una misma rampa o rim para todos los materiales.
- **Textura y paleta:** superficies de apariencia pintada, materiales diferenciados y mayor profundidad tonal que en el primero; acentos saturados sobre ambientes más modulados.
- **Luz y fondos:** mundo 3D con capas de terreno, vegetación y horizonte. **[doc]** Sus responsables destacan mejoras de iluminación, sombreado, agua, movimiento y proporciones; no publican en esta entrevista su distribución entre horneado y tiempo real.
- **UI y economía:** paneles de aventura, retratos e iconos de acciones; texto funcional separado del adorno. La decisión transferible es concentrar detalle expresivo en personajes y composiciones importantes, reduciendo detalle incidental fuera de ellas. [Entrevista a Capcom][mhs]

**Aplicación:** adoptar la jerarquía expresiva, ajustándola al chibi más compacto del tablero.

#### 2.3. Pokémon: Let’s Go, Pikachu! / Eevee! — Switch

- **Cámara y proporción:** vista alta de tres cuartos y encuadres controlados; perspectiva visualmente moderada, cuya matriz exacta está **sin verificar**. Protagonistas alrededor de **3,5–4 cabezas**.
- **Modelado y sombreado:** volúmenes redondeados, rasgos faciales amplios y accesorios grandes; sombreado suave de aspecto cartoon. No depende visualmente de un contorno negro grueso uniforme.
- **Textura y valores:** colores limpios, detalle superficial contenido y patrones grandes. El suelo y la arquitectura establecen un fondo legible para personajes pequeños.
- **Luz y fondos:** entornos 3D compactos y rutas cuidadosamente encuadradas. La claridad general no permite deducir lightmaps ni GI.
- **UI y economía:** paneles limpios, iconos destacados y tipografía sin remates de apariencia amable. Cámara limitada y formas simples permiten trabajar el acabado de cada vista. [Material oficial de la región][letsgo]

**Aplicación:** una referencia especialmente útil para calles pequeñas, patios universitarios y acompañamiento del gato.

#### 2.4. Pokémon Diamante Brillante / Perla Reluciente — Switch

- **Cámara y proporción:** exploración alta con lectura casi paralela; proyección exacta **sin verificar**. Personajes del mundo cercanos a **2 cabezas**, frente a representaciones más alargadas, aproximadamente **4,5–6**, durante combates.
- **Modelado y sombreado:** cuerpos de muñeco, manos y pies simples; superficies suavizadas y brillos visibles. No corresponde describir todo el acabado como cel shading.
- **Textura y paleta:** colores claros, superficies amplias y detalle que respeta una estructura modular; algunos brillos refuerzan la lectura de juguete.
- **Luz y fondos:** escenarios 3D de escala muy comprimida. El desenfoque aparente no proporciona parámetros verificables de lente.
- **UI y economía:** menús de información limpia y fichas de criaturas. **[doc]** El anuncio oficial destaca la conservación de la escala de pueblos y rutas. La compresión del espacio mantiene la lectura de lugares pequeños. [Sitio oficial][bdsp]; [anuncio primario][bdsppr]

**Aplicación:** tomar compacidad y lectura; evitar producir dos sistemas completos de proporciones para el protagonista.

#### 2.5. Leyendas Pokémon: Arceus — Switch

- **Cámara y proporción:** perspectiva libre de tercera persona, con encuadres bajos y elevados; humanos aproximadamente de **6–7 cabezas**.
- **Modelado y sombreado:** figuras más alargadas, ropa y equipo diferenciados por grandes formas; acabado cartoon de amplias zonas de color. Algoritmos concretos de borde, rampas y rim **sin verificar**.
- **Textura y valores:** paleta de verdes, azules y tierras, con sensación pictórica y contrastes ambientales contenidos. El horizonte tiene más importancia compositiva que en los remakes compactos.
- **Luz y fondos:** grandes entornos 3D, distancias largas y atmósfera. Reparto técnico de luces horneadas/dinámicas **sin verificar** en las fuentes primarias consultadas.
- **UI y economía:** lenguaje de registro de campo, símbolos y anotaciones. **[doc]** La investigación y elaboración de una primera Pokédex forman parte de su planteamiento oficial. Para este proyecto interesa convertir observación y registro en acciones, conservando escenarios mucho más pequeños. [Comunicado oficial][arceus]

**Aplicación:** vincular las herramientas científicas a explorar y observar; no tomar su escala territorial como objetivo de producción.

#### 2.6. Pokémon Espada / Escudo — Switch

- **Cámara y proporción:** combinación de recorridos con encuadres dirigidos y cámara controlable en el Área Silvestre, esto último confirmado oficialmente. Humanos alrededor de **5,5–6,5 cabezas**. [doc/inf][sword]
- **Modelado y sombreado:** siluetas diferenciadas por ropa y cabello; superficies cartoon con detalle selectivo. Contorno y rim no tienen una presencia uniforme que permita inferir una única técnica.
- **Textura y paleta:** ciudades con identidades cromáticas fuertes; personajes de colores más limpios frente al decorado. La repetición de módulos no tiene por qué implicar repetición de composición.
- **Luz y fondos:** escenario 3D; las rutas encuadradas y las áreas abiertas exigen tratamientos visuales distintos. Sistema exacto de iluminación **sin verificar**.
- **UI y economía:** lenguaje contemporáneo, deportivo y de dispositivos; paneles claros y números de fuerte jerarquía. Su lección más útil es admitir distintas cámaras según la función del lugar. [Material oficial][sword]

**Aplicación:** separar calle, taller, exploración y grandes vistas mediante encuadres adecuados a cada actividad.

#### 2.7. The Legend of Zelda: Ocarina of Time 3D — 3DS

- **Cámara y proporción:** perspectiva de tercera persona y encuadres de acción; inclinación variable. Link niño se lee aproximadamente en **4–5 cabezas**; adulto en **6–7**.
- **Modelado y sombreado:** geometría que prioriza silueta y articulaciones, con cabello y ropa resueltos en masas. Predomina una lectura difusa y pintada; no es el cel de *Ni no Kuni*.
- **Textura y valores:** texturas de apariencia manual, detalles arquitectónicos grandes y zonas cromáticas que distinguen lugares y funciones.
- **Luz y fondos:** espacios 3D contenidos, cielos y fondos lejanos; no debe heredarse sin comprobación la descripción de los fondos del original de Nintendo 64.
- **UI y economía:** corazones, asignación de objetos, símbolos y mapa; información repartida entre dos pantallas. **[doc]** La entrevista explica ajustes de profundidad para el indicador de objetivo y cambios de comportamiento al aumentar la frecuencia del juego. Su enseñanza es comprobar arte, cámara e interacción juntos. [Iwata Asks][oot]

**Aplicación:** orientar al jugador con arquitectura y color; dar al equipo científico una silueta comprensible desde lejos.

#### 2.8. The Legend of Zelda: Link’s Awakening — 2019, Switch

- **Cámara y proporción:** vista alta oblicua, de apariencia casi paralela; personajes alrededor de **2–2,5 cabezas**. FOV y proyección exactos **sin verificar**.
- **Modelado y sombreado:** volúmenes redondeados, caras reducidas a rasgos esenciales y materiales con pequeños brillos. No requiere contorno negro dominante.
- **Textura y valores:** colores locales definidos y microdetalle subordinado a la escala. **[doc]** Su director gráfico explica que la miniatura imaginada reguló cuánto detalle añadir. [Nintendo][la]
- **Luz y fondos:** mundo 3D de maqueta con contacto, sombras y enfoque selectivo. **[sec]** Digital Foundry describe la apariencia brillante de juguete y registra variaciones de resolución y caídas de rendimiento en la versión analizada. Esa publicación histórica no acredita el estado de parches posteriores. [Análisis directo][ladf]
- **UI y economía:** iconos claros y menús discretos. La miniaturización proporciona cohesión; por sí sola no garantiza bajo coste.

**Aplicación:** definir primero la escala material del mundo y mantenerla en todos los recursos.

#### 2.9. The Legend of Zelda: Echoes of Wisdom — Switch

- **Cámara y proporción:** alta de tres cuartos, con lectura de tablero; aproximadamente **2–2,5 cabezas** para personajes principales.
- **Modelado y sombreado:** volúmenes simples, formas redondeadas y materiales limpios; sombras y brillos aportan volumen sin necesitar un borde negro general.
- **Textura y paleta:** diferencias claras entre regiones y superficies, con detalle contenido en cada objeto. Los elementos manipulables destacan por forma y contraste.
- **Luz y fondos:** escenarios 3D construidos como espacios compactos, aunque el mundo total sea mayor. DOF, bake y número de luces concretos **sin verificar**.
- **UI y economía:** símbolos de objetos, cantidades y selección visual. **[doc]** Nintendo presenta el juego como una continuación del enfoque visual y de juego cenital consolidado con *Link’s Awakening*. [Entrevista oficial][echoes]

**Aplicación:** hacer reconocibles los objetos científicos manipulables por su forma y función antes de añadir etiquetas.

#### 2.10. Bravely Default — 3DS

- **Cámara y proporción:** encuadres dirigidos, vistas de ciudad próximas a una ilustración escénica y mayor elevación en otros espacios. Personajes aproximadamente de **2,5–3 cabezas**.
- **Modelado y sombreado:** personajes 3D compactos, ropa de silueta amplia y modelado subordinado al tamaño en pantalla; detalles pintados y sombreado suave.
- **Textura y valores:** línea, acuarela aparente, tonos de papel y contrastes reservados para hitos. La reseña del artbook confirma la convivencia de diseños chibi, versiones proporcionadas y estudios de entornos. [sec][artbravely]
- **Luz y fondos:** **[doc]** las ilustraciones de ciudades se transformaron en espacios con profundidad; las mazmorras podían ser 3D más convencional. La iluminación representada en una pintura no equivale a LightmapGI. [Entrevista][bravely]
- **UI y economía:** lenguaje de libro y ornamentación contenida; tipografía de lectura separada de los rótulos. Una cámara controlada permite conservar composiciones pictóricas muy trabajadas.

**Aplicación:** especialmente valioso para el hub lateral y vistas memorables de la ciudad.

#### 2.11. Bravely Second — 3DS

- **Cámara y proporción:** mantiene el enfoque escénico y encuadres controlados; humanos aproximadamente de **3–3,5 cabezas**.
- **Modelado y sombreado:** personajes 3D pequeños, siluetas amplias y detalle concentrado en peinados, vestuario y accesorios.
- **Textura y paleta:** continuidad pictórica, con variantes de color y formas según personaje y lugar; el artbook documenta personajes, escenarios y criaturas. [sec][artsecond]
- **Luz y fondos:** continúa la lectura de ilustración con profundidad; no se verificó un inventario técnico de luces o materiales.
- **UI y economía:** libro, fichas e iconos con jerarquía de RPG. **[doc]** Sus creadores explican que elevaron ligeramente las proporciones de todo el elenco y comprobaron que las caras seguían siendo reconocibles. [Entrevista][second]

**Aplicación:** permitir que un personaje universitario sea chibi sin eliminar toda sensación de edad; validar su cara a tamaño real de exploración.

#### 2.12. Bravely Default II — Switch

- **Cámara y proporción:** encuadres altos y dirigidos; humanos aproximadamente de **3–4 cabezas**, con cuerpos de muñeco más volumétricos.
- **Modelado y sombreado:** materiales más presentes, pequeñas reflexiones y sombreado suave; no es simplemente el acabado de 3DS a mayor resolución.
- **Textura y paleta:** ciudades pictóricas y superficies construidas para comunicar materiales; conviene vigilar la coherencia entre personajes y escenarios.
- **Luz y fondos:** **[doc]** ciudades concebidas como papercraft y campo como maqueta ferroviaria. El blog oficial de *Brilliant Lights* identifica expresamente la técnica de enfoque selectivo mostrada por el equipo de *Default II*. [Productor][bd2]; [blog oficial][bd2dof]
- **UI y economía:** paneles y retratos adaptados a una pantalla. **[doc]** Cambiaron fuentes, colores y fondos por problemas de legibilidad, y alejaron la cámara de mazmorras tras recibir comentarios. [Entrevista][bd2ui]

**Aplicación:** el acabado debe probarse caminando y leyendo, además de en capturas estáticas.

#### 2.13. Octopath Traveler — Switch

- **Cámara y proporción:** perspectiva escénica controlada, elevada en exploración; personajes de píxeles de alrededor de **3 cabezas**, con variación por sprite.
- **Modelado y sombreado:** personajes planos y escenario 3D. Las sombras dibujadas en el sprite y la iluminación del mundo cumplen funciones distintas; no es cel shading uniforme.
- **Textura y paleta:** píxeles visibles, materiales de escenario, contraste atmosférico y gradación por lugar.
- **Luz y fondos:** **[doc]** integra luz dinámica con efectos; la presentación técnica muestra bloom, DOF, gradación de color y materiales parametrizados.
- **UI y economía:** menús de jerarquía clara y ornamentación contenida. **[doc]** También hubo optimización de datos de sprites y memoria. Usar personajes planos no convirtió automáticamente el sistema completo en barato. [Presentación técnica][octotalk]; [entrevista][octo]

**Aplicación:** adoptar la integración entre actor y escenario; mantener opcionales los efectos que no sostengan el juego en el portátil.

#### 2.14. Triangle Strategy — Switch

- **Cámara y proporción:** vista oblicua elevada, giratoria en combate y con lectura axonométrica; proyección exacta **sin verificar**. Humanos de píxeles aproximadamente de **3,5–4 cabezas**.
- **Modelado y sombreado:** personajes 2D sobre arquitectura 3D escalonada. Las superficies del escenario y el dibujo de los personajes requieren reglas de detalle compatibles.
- **Textura y valores:** tierras, piedra, madera y acentos de identidad; los cambios de altura deben seguir siendo comprensibles bajo efectos e iluminación.
- **Luz y fondos:** escenario 3D que puede verse desde varios lados. Pipeline concreto de horneado/dinámico **sin verificar**.
- **UI y economía:** rejilla, alcance, retratos, estados y turnos; la información funcional ocupa una parte importante de la composición. **[doc]** Sus productores reconocen el reto de equilibrar cámara móvil y personajes de píxeles. [Entrevista][triangle]

**Aplicación:** tomar su claridad espacial para talleres y circuitos de interacción; restringir la rotación si no aporta una decisión de juego.

#### 2.15. Ni no Kuni: Wrath of the White Witch — Switch

- **Cámara y proporción:** perspectiva de tercera persona con encuadres variables; Oliver aproximadamente de **4–5 cabezas**, adultos más alargados.
- **Modelado y sombreado:** personajes 3D de aspecto cel, contornos finos y grandes áreas de color; ambientes de transiciones más suaves.
- **Textura y paleta:** fondos de apariencia pintada, arquitectura expresiva, vegetación organizada en masas y combinaciones de cálidos y fríos que separan planos.
- **Luz y fondos:** el mundo jugable es 3D; su apariencia de animación no significa que todos sus fondos sean dibujos planos. **[doc]** La entrevista distingue las secuencias animadas de la supervisión y storyboard de escenas en tiempo real. [Entrevista][nnk]
- **UI y economía:** libro de consulta, retratos, iconos e información de combate. **[doc]** Bandai Namco anunció la versión de Switch a 720p y 30 fps; no debe confundirse con el remaster de otras plataformas. [Comunicado][nnkswitch]

**Aplicación:** combinar ternura, vida cotidiana y asombro científico mediante color, actuación y composición.

**Precaución sobre la saga:** el análisis independiente de *Ni no Kuni II* estudia un fotograma de **PC con DirectX 11** y describe varios pasos para contornos e iluminación. No certifica la implementación del primer juego en Switch. [sec][nnkframe]

### 3. Qué explica realmente el acabado del tablero

La lectura de las capturas locales permite identificar cinco prioridades **[inf]**:

1. **La silueta se entiende antes que la textura.** Cabello, ropa y cuerpo forman masas grandes.
2. **El suelo tiene una organización cromática propia.** Caminos y áreas transitables se separan de la vegetación.
3. **La profundidad se construye por capas.** El hub dispone primer plano, actividad y horizonte.
4. **Los materiales comparten una escala de detalle.** Rocas, suelo y vegetación pertenecen a la misma familia pictórica.
5. **La interfaz prolonga la identidad del mundo.** Papel, pinceladas y mapa tienen continuidad visual.

Estas capturas no verifican su motor, topología, coste de producción ni rendimiento. Tampoco prueban que toda la vegetación sea geometría individual o que las sombras sean dinámicas.

Para el proyecto, el equivalente original puede surgir de **aleros, patios, sombras de árboles, superficies pintadas, instalaciones eléctricas, instrumentos y mobiliario de taller**, seleccionados mediante observación local.

### 4. Quince principios transferibles

Las siguientes son propuestas **[inf]** derivadas del análisis; no recetas atribuidas literalmente a los estudios.

| Principio | Ciudad tropical contemporánea | Instalaciones espaciales |
|---|---|---|
| 1. Diseñar para el encuadre | Fachadas y patios compuestos desde el recorrido | Laboratorios organizados alrededor de tareas visibles |
| 2. Priorizar silueta | Ropa, mochila y herramientas reconocibles | Equipamiento y funciones distinguibles por forma |
| 3. Mantener una escala de detalle | Pinceladas amplias en paredes y vegetación | Paneles simples; detalle concentrado en instrumentos |
| 4. Separar planos por valores | Sombras de aleros y fondos menos contrastados | Primer plano legible frente a estructuras distantes |
| 5. Reservar saturación | Acentos en protagonista y objetos útiles | Acentos funcionales sobre blancos y azules |
| 6. Dar identidad a cada lugar | Materiales y vegetación propios de cada zona | Código material por taller, control, ensayo o exposición |
| 7. Comprimir distancias | Una manzana significativa puede representar un barrio | Un conjunto de salas puede representar una instalación mayor |
| 8. Construir profundidad por capas | Vegetación cercana, actividad y horizonte | Pasarelas, sala de trabajo y volumen industrial lejano |
| 9. Dirigir las sombras | Una dirección de sol coherente por escena | Luz principal clara, con relleno contenido |
| 10. Modular sin uniformar | Reutilizar piezas variando composición | Reutilizar paneles, soportes y mobiliario |
| 11. Exagerar lo funcional | Conectores y herramientas algo mayores | Interfaces y partes móviles legibles desde cámara |
| 12. Mostrar ciencia en la acción | Diagnosticar, construir y observar | Medir, ajustar y ensayar con consecuencias visibles |
| 13. Usar animación con intención | Ventilador, ropa y vegetación seleccionada | Movimiento de un mecanismo o indicador relevante |
| 14. Unificar mundo e interfaz | Cuaderno de campo y mapas propios | Ese mismo cuaderno incorpora esquemas y registros |
| 15. Aprobar escenas completas | Personaje, gato, calle y HUD juntos | Los mismos actores bajo iluminación fría |

Las bases más directamente documentadas son el control de detalle según escala, la construcción pictórica de profundidad, la integración por luz y la necesidad de comprobar cámara y legibilidad. [doc][la] [doc][bravely] [doc][octo] [doc][bd2ui]

### 5. Tabla «tomar / adaptar / evitar»

| Tomar | Adaptar al proyecto | Evitar |
|---|---|---|
| Claridad chibi | Tres cabezas, postura y vestuario de estudiante adulto | Una silueta reconocible de un protagonista comercial |
| Diorama compacto | Calles, patios y talleres contemporáneos | Convertir la ciudad en una aldea fantástica genérica |
| Fondos pictóricos con profundidad | Horizonte urbano y paisajes observados localmente | Calcar panoramas o composiciones distintivas |
| Sombreado controlado | Toon suave o materiales mates coherentes | Aplicar una rampa idéntica a piel, metal, papel y vegetación |
| Contraste cálido/frío | Ciudad acogedora y tecnología precisa | Usarlo como único indicador de peligro o interacción |
| Compañero expresivo | Gato con conducta felina y función narrativa propia | Trajes, rasgos o gestos identificables de mascotas comerciales |
| Cuaderno y mapa ilustrado | Registro científico, croquis y leyendas originales | Copiar marcos, iconos y distribución ornamental |
| Modularidad | Biblioteca pequeña de piezas combinables | Llenar el escenario de objetos únicos |
| Enfoque selectivo | Reservarlo para una mejora opcional o ilustraciones | Hacer ilegible la exploración para imitar tilt-shift |
| Modelos asistidos por IA | Evaluar silueta, deformación, materiales y escena | Confundir un render atractivo con un recurso validado |
| Grandes formas de vegetación | Copas y grupos de plantas de lectura clara | Densidad uniforme de hierba sobre todo el suelo |
| Escenas de ciencia | Aparatos simplificados pero funcionalmente coherentes | Símbolos y cables arbitrarios que enseñen relaciones falsas |

### 6. Límites de propiedad intelectual

#### Principios generales que pueden estudiarse

Como criterios de diseño **[inf]**, pueden adoptarse:

- Proporciones chibi.
- Perspectiva alta, cámara ortogonal o encuadres de diorama.
- Texturas de apariencia pintada.
- Sombreado por bandas, control de normales y contornos.
- Paletas limitadas, separación de valores y perspectiva atmosférica.
- Interfaz inspirada en papel, fichas o instrumentos.
- Arquitectura modular y escenarios por capas.

La distinción jurídica relevante es entre la idea y **su realización concreta**, no entre una imagen «idéntica» y otra con algunos cambios. Los artículos 4, 5 y 7 de la Decisión 351 protegen obras y contemplan sus transformaciones, mientras distinguen las ideas de su expresión. [doc][can351]

#### Expresión concreta que no debe reproducirse

Para este proyecto deben diseñarse desde cero **[inf]**:

- Personajes, criaturas y combinaciones reconocibles de rasgos.
- Vestuario, armas, herramientas fantásticas y accesorios distintivos.
- Mapas, edificios ficticios y composiciones características.
- Ilustraciones, texturas, modelos, animaciones, sonidos y música.
- Emblemas, iconos y ornamentación particular de las interfaces.
- Logotipos y nombres usados como identidad comercial.

Una paleta cálida o un cuerpo de tres cabezas no convierte automáticamente un diseño en copia. Tampoco garantiza independencia combinar una silueta, ropa, colores y poses reconocibles. **No existe un porcentaje universal de cambios que vuelva segura una reproducción.** Esta última es una conclusión práctica, no una regla numérica de la norma. [inf][can351]

Para comunicar el proyecto, conviene emplear «diorama pintado» o «2.5D» como descripción propia y reservar los nombres de franquicias para la documentación interna de referencias.

#### Recursos de NASA y fuentes tipográficas

NASA distingue su contenido general de los materiales de terceros y establece condiciones específicas para imágenes, identificadores y usos promocionales. Los logotipos y emblemas no deben tratarse como recursos automáticamente libres ni utilizarse para sugerir patrocinio. [doc][nasamedia] [doc][nasabrand]

DotGothic16 dispone de licencia OFL; su uso requiere conservar las condiciones de esa licencia. La licencia de una fuente tampoco autoriza copiar una composición gráfica comercial que la utilice. [doc/inf][font]

### 7. Tres direcciones de arte originales para Fase 1

**Todos los nombres, colores y parámetros siguientes son propuestas propias [inf].** Los códigos hexadecimales expresan colores base, no una medición de los referentes.

| Aspecto | A. Gouache de taller | B. Maqueta de cerámica y aluminio | C. Atlas de luz y papel |
|---|---|---|---|
| Idea central | Una aventura científica pintada y vivida | Un mundo material pequeño y tangible | Un cuaderno de exploración convertido en espacio |
| Personajes | 3 cabezas, formas suaves y ropa práctica | 2,75–3 cabezas, volúmenes más compactos | 3–3,25 cabezas, siluetas algo más gráficas |
| Superficie | Pincelada visible, variación de color, acabado mate | Color limpio, rugosidad alta y brillos pequeños | Textura de papel y pincelada más plana |
| Cámara | Alta oblicua; hub lateral | Alta, casi paralela; composición de maqueta | Muy controlada; escenas por capas |
| Ciudad cálida | Crema `#F1D7A4`, terracota `#BC6548`, verde `#526F4A`, azul petróleo `#315A61` | Marfil `#E8D9BB`, coral `#D47958`, ocre `#C49A44`, verde `#617760` | Papel `#E8D6AC`, arcilla `#B96851`, tinta `#344A4C`, verde gris `#71816B` |
| Espacio frío | Blanco azulado `#DCE7E9`, azul gris `#6D91A4`, profundo `#283E57`, cian `#78BCC0` | Blanco `#E2E8E6`, aluminio `#87979F`, azul `#446782`, cian `#8AC1C4` | Papel frío `#DFE6E3`, tinta azul `#30455D`, gris `#7B929B`, turquesa `#68A6AC` |
| Interfaz | Cuaderno usado, sellos y anotaciones propias | Fichas y paneles de instrumentación | Atlas, croquis y esquemas superpuestos |
| Mayor fortaleza | Cercanía al tablero y expresividad | Cohesión entre formas y materiales | Profundidad pictórica con alcance controlado |
| Principal riesgo | Variación de pincelada entre recursos | Acabado excesivamente plástico | Desajustes entre personaje y fondo |

#### A. Gouache de taller — recomendada

La ciudad se representa mediante superficies soleadas, sombra fresca, paredes con variación cromática y vegetación en masas. El trabajo científico comparte esa cercanía: carcasas usadas, herramientas cuidadas y anotaciones visibles.

En las instalaciones espaciales cambia la temperatura cromática, mientras se conserva la misma escala de pincelada. El protagonista y el gato siguen perteneciendo al mismo mundo. Los instrumentos reciben bordes más precisos que la decoración.

La identidad procede del contraste entre **vida cotidiana y precisión científica**. Es la candidata más próxima al acabado pintado del tablero.

#### B. Maqueta de cerámica y aluminio

Los objetos parecen construidos con pocos materiales coherentes: cerámica pintada, metal satinado, tela mate y plástico de pequeñas reflexiones. La ciudad conserva colores cálidos; las instalaciones espaciales introducen blancos, aluminio y azules.

El chibi es compacto, pero herramientas, conectores y articulaciones conservan lectura funcional. Los brillos se reservan para comunicar material o interacción.

Su desarrollo debe comenzar con una luz sencilla. La sensación tangible deberá sostenerse mediante forma, color y rugosidad, sin depender de reflejos costosos.

#### C. Atlas de luz y papel

La ciudad se presenta mediante capas ilustradas, planos de profundidad y actores 3D de materiales mates. Las instalaciones espaciales añaden cortes de salas, esquemas y vistas preparadas alrededor de acciones concretas.

El cuaderno mantiene continuidad entre exploración, mapa y registros científicos. El parallax sería moderado para conservar la cohesión pictórica.

Es una opción adecuada si el usuario prioriza composición e ilustración. Su compromiso es aceptar cámaras muy controladas y atmósferas preparadas: un fondo con sombras pintadas necesita revisión cuando cambia la luz o el punto de vista.

### 8. Traducción al equipo disponible

#### Base visual propuesta

Para la HD 620 recomiendo que la primera escena aprobable pueda funcionar con:

- Personajes 3D de materiales sencillos.
- Color y sombreado amplio en texturas.
- Ambiente y una iluminación principal.
- Sombras de contacto simples; sombra dinámica solo si la medición la permite.
- Fondos lejanos pintados.
- Vegetación agrupada y localizada.
- Ausencia de dependencia de SDFGI y DOF.

Son decisiones **[inf]** de alcance. La documentación permite justificar Compatibility como punto de partida y materiales sencillos como estrategia; **no certifica el rendimiento concreto de este portátil**. [doc][renderers] [doc][gpu]

Godot permite toon y rim en sus materiales estándar. Que una opción exista no obliga a activarla en todos los recursos. También distingue la transparencia mezclada del recorte alfa: este último puede resultar apropiado para vegetación de borde definido, aunque sigue siendo necesario medir el solapamiento. [doc/inf][material]

#### Presupuestos iniciales propios

Estos rangos son **objetivos de arranque [inf]**, no límites de la HD 620 ni cifras extraídas de Nintendo, Capcom o Square Enix.

| Recurso o condición | Objetivo inicial |
|---|---|
| Protagonista completo | 3.000–6.000 triángulos |
| Gato | 1.000–2.500 triángulos |
| NPC común | 1.500–3.000 triángulos |
| Prop pequeño | Decenas a pocos centenares de triángulos |
| Textura de prop habitual | 256–512 px, según tamaño en pantalla |
| Textura principal de personaje | Empezar con 1.024 px y comprobar si puede reducirse |
| Materiales | Pocos materiales compartidos por familia |
| Iluminación con sombra | Comenzar con ninguna; ensayar una principal |
| Resolución de comparación | Mundo a 1.280 × 720; comprobar aparte la lectura del HUD |
| Objetivo de juego | 30 fps estables, pendiente de prueba local |

El creador de personaje introduce una excepción: una cara que funciona pequeña puede fallar en primer plano. Deben comprobarse ambas vistas antes de aumentar toda la resolución o geometría. [inf]

La densidad de téxel debe regularse por **detalle visible a la cámara final**. Un texto que el jugador necesita leer merece otro tratamiento que una fachada lejana. No conviene usar el tamaño de una textura como sustituto de una evaluación visual. [inf; fundamento sobre costes y materiales][gpu]

#### Puerta de validación de arte

La comparación de Fase 1 debería utilizar una misma escena original:

**Estudiante y gato → calle tropical corta → taller con instrumento interactivo → sala espacial.**

Para cada dirección se aprobarían:

1. Silueta en tamaño de exploración.
2. Cara y cuerpo en el creador.
3. Relación entre personaje, gato y entorno.
4. Lectura del objeto interactivo.
5. HUD y diálogo con texto real en español.
6. Coherencia entre paleta cálida y fría.
7. Rendimiento medido en el portátil.

Primero puede resolverse con primitivas, materiales y recursos ya disponibles en Godot. El estilo elegido debe superar esa comparación antes de gastar créditos en una colección extensa.

**Esta investigación no ejecutó esa prueba ni verificó tiempos de renderizado.** La elección estética queda preparada para revisión; la viabilidad de cada configuración deberá confirmarse con la escena local.

## Fuentes

Las fuentes históricas se utilizan para sus versiones y declaraciones originales. Las páginas `stable` de Godot se consultaron como documentación vigente, sin convertirlas en una auditoría del ejecutable descargado.

- **[doc]** [Capcom: cambio de dirección artística en Stories 2][mhs] — entrevista, GameSpot, 2021.
- **[doc]** [Capcom: adaptación de Stories a nuevas plataformas][mhsui] — entrevista, Siliconera, 2024.
- **[doc]** [Pokémon Let’s Go: material oficial de Kanto][letsgo].
- **[doc]** [Diamante Brillante / Perla Reluciente: sitio oficial][bdsp] y [anuncio de presentación][bdsppr].
- **[doc]** [Leyendas Pokémon: Arceus: comunicado de lanzamiento][arceus], 2022.
- **[doc]** [Espada / Escudo: cámara y Área Silvestre][sword].
- **[doc]** [Ocarina of Time 3D: entrevista al equipo][oot], Nintendo, 2011.
- **[doc]** [Link’s Awakening: dirección gráfica y escala de diorama][la], Nintendo.
- **[sec]** [Link’s Awakening: análisis técnico directo][ladf], Digital Foundry, 2019.
- **[doc]** [Echoes of Wisdom: Ask the Developer][echoes], Nintendo, 2024.
- **[doc]** [Bravely Default: construcción de fondos con profundidad][bravely], Dengeki, 2012.
- **[doc]** [Bravely Second: proporciones y reconocimiento de personajes][second], Famitsu, 2014.
- **[doc]** [Bravely Default II: ciudades de papel y campos de maqueta][bd2], Dengeki, 2020/2021.
- **[doc]** [Bravely Default II: revisión de interfaz y cámara][bd2ui], Famitsu, 2020.
- **[doc]** [Brilliant Lights: miniaturización y técnica procedente de Default II][bd2dof], Square Enix, 2022.
- **[doc]** [Retrospectiva oficial de Bravely Default][bd2025], Square Enix, 2025.
- **[sec]** [Reseña de The Art of Bravely Default][artbravely], Parka Blogs.
- **[sec]** [Reseña de Bravely Second Design Works][artsecond], Halcyon Realms, 2015.
- **[doc]** [Octopath Traveler: entrevista de desarrollo][octo], Unreal Engine, 2019.
- **[doc]** [Octopath Traveler: presentación de Unreal Fest East 2018][octotalk], publicada por Epic Games Japan.
- **[doc]** [Triangle Strategy: entrevista a sus productores][triangle], Destructoid, 2022.
- **[doc]** [Ni no Kuni: entrevista sobre la colaboración visual][nnk], RPG Site, 2012.
- **[doc]** [Ni no Kuni: especificación anunciada para Switch][nnkswitch], Bandai Namco, 2019.
- **[sec]** [Ni no Kuni II: análisis de un fotograma de PC][nnkframe], Thomas Poulet.
- **[doc]** [Guilty Gear Xrd: material de GDC sobre dirección del cel shading][gdc], 2015. Se consultaron la ficha y pasajes indexados del material; no se verificó la reproducción completa del vídeo.
- **[doc]** Godot: [renderizadores][renderers], [optimización de GPU][gpu], [materiales estándar][material], [Camera3D][camera] y [MultiMesh][multimesh].
- **[doc]** [DotGothic16: repositorio y licencia][font].
- **[doc]** [Decisión Andina 351][can351], especialmente artículos 4, 5 y 7.
- **[doc]** NASA: [uso de imágenes y medios][nasamedia] y [normas de identidad][nasabrand].
- **[inf; material local]** [Tablero del usuario](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Referencias/Tablero_usuario/>) — catorce capturas revisadas como objetivo visual, sin atribuirles un pipeline demostrado.

[mhs]: https://www.gamespot.com/articles/monster-hunter-stories-2s-new-art-style-was-in-response-to-fan-feedback/1100-6493222/
[mhsui]: https://www.siliconera.com/interview-preparing-monster-hunter-stories-1-and-2-for-new-platforms/
[letsgo]: https://pokemonletsgo.pokemon.com/en-us/kanto-region/
[bdsp]: https://diamondpearl.pokemon.com/en-us/
[bdsppr]: https://press.pokemon.com/en/POKEMON-ANNOUNCES-NEW-VIDEO-GAMES-POKEMON-BRILLIANT-DIAMOND-POKEMON-SH
[arceus]: https://press.pokemon.com/en/POKEMON-LEGENDS-ARCEUS-NOW-AVAILABLE
[sword]: https://swordshield.pokemon.com/en-us/gameplay/wild-area/
[oot]: https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/3/1/
[la]: https://zelda.nintendo.com/links-awakening/blog/director-yoshiki-haruhana/
[ladf]: https://www.digitalfoundry.net/articles/digitalfoundry-2019-zelda-links-awakening-tech-analysis
[echoes]: https://www.nintendo.com/us/whatsnew/ask-the-developer-vol-13-the-legend-of-zelda-echoes-of-wisdom-part-1/
[bravely]: https://dengekionline.com/elem/000/000/542/542374/index-2.html
[second]: https://www.famitsu.com/news/201401/18046733.html
[bd2]: https://dengekionline.com/articles/60981/
[bd2ui]: https://www.famitsu.com/news/202010/29208426.html
[bd2dof]: https://www.jp.square-enix.com/bdbl_SP/blog/2022/01/10951.html
[bd2025]: https://www.square-enix-games.com/en_US/news/bravely-default-flying-fairy-hd-remaster-interview
[artbravely]: https://www.parkablogs.com/content/book-review-art-of-bravely-default
[artsecond]: https://halcyonrealms.com/books/bravely-second-design-works-2013-2015-art-book-review/
[octo]: https://www.unrealengine.com/spotlights/octopath-traveler-s-hd-2d-art-style-and-story-make-for-a-jrpg-dream-come-true
[octotalk]: https://www.docswell.com/s/EpicGamesJapan/KXPWY5-UE4_UFE2018_ACQUIRE_OCTOPATHTRAVELER
[triangle]: https://www.destructoid.com/triangle-strategy-interview-producers-asano-arai-square-enix-hd-2d-tactics-rpg/
[nnk]: https://www.rpgsite.net/interview/3075-e3-2012-ni-no-kuni-wrath-of-the-white-witch-interview
[nnkswitch]: https://www.bandainamcoent.com/es_mx/news/ni-no-kuni-wrath-of-the-white-witch-remastered-release-trailer
[nnkframe]: https://blog.thomaspoulet.fr/posts/ni-no-kuni-2-frame-analysis/
[gdc]: https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf
[renderers]: https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html
[gpu]: https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html
[material]: https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html
[camera]: https://docs.godotengine.org/en/stable/classes/class_camera3d.html
[multimesh]: https://docs.godotengine.org/en/stable/classes/class_multimesh.html
[font]: https://github.com/fontworks-fonts/DotGothic16
[can351]: https://www.comunidadandina.org/StaticFiles/DocOf/DEC351.pdf
[nasamedia]: https://www.nasa.gov/nasa-brand-center/images-and-media/
[nasabrand]: https://www.nasa.gov/nasa-brand-center/brand-guidelines/

Firecrawl agotó su cupo durante la investigación. Su aviso indica: “To continue now, add credits or upgrade your plan at [https://firecrawl.dev/pricing](https://firecrawl.dev/pricing).”