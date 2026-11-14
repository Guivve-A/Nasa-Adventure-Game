# «After the Wind»: reconstrucción del proceso y lecciones para Godot en gráfica integrada

## Resumen ejecutivo

**El video está localizado, pero «After the Wind» no es el juego de 20 dólares anunciado en el título.** Es una recopilación publicada el 2 de noviembre de 2026; su primer segmento presenta este proyecto. El desglose relacionado habla de unas seis semanas de desarrollo y aproximadamente **400 USD mensuales en herramientas**, como cifras declaradas, sin auditoría. [doc/sec; fuentes en A1–A2]

El proceso combina Godot, agentes de código, conceptos visuales, generación 3D con Tripo y trabajo de animación en Blender y Cascadeur. El creador aporta bocetos, referencias, decisiones y correcciones. Sus publicaciones documentan fallos de malla y problemas importantes de rendimiento. [doc; A3–A5]

Para tu Intel HD 620 recomiendo trasladar **la coherencia artística, las cámaras controladas y la producción por piezas**. La base propuesta es Godot 4.7 con Compatibility, iluminación sencilla, escenarios pequeños y lightmaps condicionados a comprobar el horneado local. SDFGI queda descartado para la primera versión. **El rendimiento y la equivalencia visual siguen sin verificar en tu equipo.** [inf; A7–A12]

## Decisiones recomendadas

Las recomendaciones de esta tabla son **[inf]**: decisiones propuestas a partir de la evidencia A1–A12, no resultados de un prototipo ejecutado.

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Interpretación del referente | Tratarlo como desarrollo dirigido por una persona y asistido por varias herramientas. | «La IA hizo todo por 20 USD»: confunde juegos y oculta intervención humana. A1–A5. | Alta |
| Renderizador inicial | Compatibility como primera configuración que medir; comparar Mobile si queda una carencia visual concreta. | Forward+ como obligación inicial: no hay medición local que justifique su coste. A7, A12. | Media |
| Iluminación global | Luz ambiental y direccional sencilla; evaluar lightmaps en una escena pequeña. | SDFGI para la primera versión: elevado coste y dependencia de Forward+. A7–A8. | Alta |
| Personajes | Probar un protagonista 3D sencillo y un compañero antes de decidir todo el reparto. | Creador completo de personajes desde el principio: multiplica combinaciones y validaciones. A3, A12. | Media |
| Vegetación | Suelo pintado y grupos limitados de hierba; MultiMesh dividido espacialmente. | Un nodo y una simulación por brizna: coste innecesario. A4, A10. | Alta |
| Generación de recursos | Referencia aprobada → malla → inspección → ajuste → prueba en Godot. | Generar escenas completas como una sola malla: dificulta corregir, reutilizar e interactuar. A3, A6. | Alta |
| Presupuesto de IA | Piloto de hasta 100 créditos; conservar al menos 900 hasta validar el proceso. | Producir un catálogo completo antes de medir calidad utilizable y coste de corrección. A6, A12. | Alta |
| Arquitectura | Escenas, composición de nodos y datos separados; funciones pequeñas para los agentes. | Introducir ECS propio por anticipación: añade infraestructura sin un problema medido. | Media |

## Afirmaciones que sostienen las decisiones

1. **[doc] El video exacto es *Made a Game With a $20 AI Plan and Already Got Sales*, de Stefan 3D AI, publicado el 2 de noviembre de 2026.** «After the Wind» ocupa el segmento **0:58–6:06**. La página y sus metadatos discrepan entre 34:28 y 34:29 de duración. [Video y capítulos](https://www.youtube.com/watch?v=iJ83GYk2BIA).

2. **[sec] La publicación que recoge una conversación con el creador atribuye al proyecto unas seis semanas de trabajo y alrededor de 400 USD mensuales en herramientas.** Identifica Godot, Claude Code con Opus 5.5, Codex/Astra, Tripo y Cascadeur. Son declaraciones transmitidas por un tercero; no presupuestos auditados. [Desglose en r/TopologyAI](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/).

3. **[doc] El creador documenta un jefe construido mediante boceto propio, conceptos en Codex, Tripo P2 para malla y textura, y Claude trabajando en Blender para rig y animación.** Declara que el intento de 5.000 quads no funcionó bien y que obtuvo mejor resultado con 25.000 triángulos. [Proceso original, 3 de noviembre de 2026](https://www.instagram.com/p/DfScKvloe1b/).

4. **[doc] El creador reporta problemas de rendimiento y correcciones específicas:** simulación de cuerdas fuera de cámara, un caso de interacción sobre una torre de 19.000 triángulos y shaders reescritos. Declara pasar de 26 a 80 FPS en su Mac con calidad Medium; faltan condiciones suficientes para reproducir esa comparación. [Optimización original, 31 de octubre de 2026](https://www.instagram.com/p/DfK26HtIKQR/).

5. **[doc/sec] La consistencia depende de instrucciones persistentes y revisión.** El creador publica habilidades para conservar contexto, reutilizar investigación y revisar tareas; el desglose secundario añade una guía artística y prompts satisfactorios guardados en JSON. [Publicación original de herramientas](https://www.instagram.com/p/De2FG-7IsIn/), [desglose secundario](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/).

6. **[doc] Los fallos de generación pueden afectar la función del objeto:** en *Remote Delivery* se documentan huecos cerrados, simetrías no deseadas y pequeñas ediciones que exigieron corrección manual. Otra entrada describe pérdida de detalles y caras flotantes al cambiar el orden de texturizado y remallado. [Proceso de objetos](https://tealrobot.substack.com/p/how-i-make-3d-game-assets-with-ai), [revisión del proceso](https://tealrobot.substack.com/p/slop-isnt-the-only-objection-to-ai).

7. **[doc] SDFGI funciona únicamente con Forward+ y es una de las técnicas de iluminación global más exigentes de Godot.** Admite luces dinámicas, pero no oclusores dinámicos ni superficies emisivas dinámicas. [Godot 4.7: SDFGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_sdfgi.html).

8. **[doc] Reproducir lightmaps y hornearlos tienen requisitos distintos.** Compatibility puede representarlos; el horneado requiere Forward+ o Mobile y emplea la GPU. LightmapGI necesita UV2 y su iluminación horneada es estática. [Arquitectura de renderizado](https://docs.godotengine.org/en/4.7/engine_details/architecture/internal_rendering_architecture.html), [LightmapGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html).

9. **[doc] Un sprite dentro del mundo 3D puede participar en la iluminación mediante `Sprite3D` o `AnimatedSprite3D` y `shaded`.** La transparencia mezclada puede producir problemas de orden; `alpha_cut` ofrece alternativas con otros compromisos. Los billboards tienen advertencias específicas al proyectar sombras. [Godot 4.7: SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html).

10. **[doc] MultiMesh permite representar muchas instancias eficientemente, pero no realiza descarte individual por cámara de cada instancia.** Por ello conviene organizar la vegetación en grupos espaciales. [Godot 4.7: MultiMeshes](https://docs.godotengine.org/en/4.7/tutorials/performance/using_multimesh.html).

11. **[doc] La importación directa de archivos `.blend` depende de Blender instalado.** Godot los convierte primero a glTF; recibir glTF/GLB permite evitar esa dependencia de importación. [Godot 4.7: formatos 3D](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).

12. **[inf] La capacidad de abrir Godot no demuestra que el acabado del tablero vaya a rendir bien en la HD 620.** Los requisitos oficiales corresponden a proyectos sencillos. Recomiendo validar primero una escena representativa a 1280×720 con un objetivo inicial de 30 FPS; ambas cifras son criterios propuestos, no mediciones. [Requisitos oficiales](https://docs.godotengine.org/en/4.7/about/system_requirements.html).

## Riesgos y cómo mitigarlos

| Riesgo | Cómo mitigarlo |
|---|---|
| Confundir una demostración atractiva con un juego terminado | Registrar por separado aspecto visual, controles, contenido, estabilidad y rendimiento. Las seis semanas describen un hito de desarrollo temprano. [doc: publicación del creador](https://www.instagram.com/p/De4rsmxoH_Z/). |
| Agotar créditos buscando una malla perfecta | Fijar un máximo de intentos por recurso y revisar el resultado dentro de Godot antes de continuar. [inf, apoyada en los fallos de A3 y A6]. |
| Recibir mallas que necesitan reparación | Con las herramientas actuales, rechazar o regenerar las defectuosas. La reparación de topología y pesos queda como capacidad pendiente; Godot no sustituye el trabajo de edición descrito por los autores. [inf; A3, A6, A11]. |
| Copiar las optimizaciones del referente sin conocer su coste | Medir primero. No introducir C++, simulaciones de cuerdas o shaders complejos por imitación. [inf; A4]. |
| Mantener sombras pintadas incompatibles con la luz del escenario | Revisar el recurso bajo la iluminación prevista y pedir referencias con iluminación neutra cuando se necesite flexibilidad. [inf; A3, A6]. |
| Usar lightmaps sin poder hornearlos de forma práctica | Validar tiempo, memoria y estabilidad de un horneado pequeño antes de convertirlos en requisito del proyecto. [inf; A8]. |
| Cambios de código que rompan funciones anteriores | Trabajar en cambios pequeños, conservar versiones recuperables y comprobar el comportamiento visible tras cada incorporación. [inf; organización y herramientas de Godot citadas en Desarrollo]. |
| Confundir referencias artísticas con contenido reutilizable | Crear siluetas, motivos gráficos y personajes propios; mantener procedencia y aprobación de cada recurso. [inf; criterio de producción solicitado]. |

## Preguntas que debe decidir el usuario

1. **¿Prima el acabado pintado del tablero o la apariencia de sprites de un HD-2D más tradicional?** Mi recomendación es comenzar por personajes 3D sencillos y escenarios pintados.

2. **¿Aceptamos 720p y 30 FPS como primera puerta de rendimiento?** Es una meta inicial; después se evaluaría mejorar resolución o fluidez.

3. **¿Se pospone el creador de personajes?** Recomiendo un protagonista fijo con pocas variantes hasta validar el juego.

4. **¿Se reserva un máximo de 100 créditos para el piloto?** La propuesta concreta aparece abajo; cada generación seguiría pasando por tu puerta de aprobación.

5. **¿Se evaluará más adelante una herramienta de edición de mallas?** Actualmente falta una vía local práctica para corregir los defectos geométricos y de animación documentados. No he instalado ni descargado ninguna.

## Desarrollo

### 1. Alcance y calidad de la evidencia

Consulta realizada el **12 de noviembre de 2026**. Revisé las **14 imágenes**, los dos informes locales de costes y parámetros relevantes de `hf_modelos.json`. El trabajo fue de solo lectura: no modifiqué archivos, no subí recursos ni ejecuté generaciones de Higgsfield.

En este informe:

- **[doc]** identifica documentación primaria o una declaración original del creador. Una declaración original acredita que se hizo esa afirmación; no demuestra que sus cifras estén auditadas.
- **[sec]** identifica una reconstrucción o entrevista publicada por otra persona.
- **[inf]** identifica mis deducciones y recomendaciones.

El servicio de transcripciones recuperó una pista en árabe etiquetada como `manual`. La solicitud de la pista inglesa recibió errores 429. La traducción contiene términos deformados; por eso contrasté nombres y procesos con publicaciones escritas. **No considero verificados los datos que solo pudieran deducirse de esos términos ambiguos.** La página del video indica además doblaje automático y promoción pagada. [doc: página del video](https://www.youtube.com/watch?v=iJ83GYk2BIA).

La documentación técnica consultada corresponde a la rama **Godot 4.7**. No constituye una prueba ejecutada específicamente sobre tu instalación 4.7.2 ni sobre su controlador gráfico.

### 2. Qué es realmente el video del tablero

Es una recopilación de proyectos enviados por la comunidad. El presentador juega a «After the Wind»; **no se presenta como su desarrollador**. El creador publica sus avances en `@afterthewindgame`. Una entrada original del 24 de octubre lo describe como desarrollo temprano y declara seis semanas de trabajo. [doc: video](https://www.youtube.com/watch?v=iJ83GYk2BIA&t=58s), [estado del proyecto](https://www.instagram.com/p/De4rsmxoH_Z/).

El título sobre una suscripción de 20 USD y ventas en App Store pertenece al conjunto de la recopilación. **No debe utilizarse como presupuesto de «After the Wind».**

También hay una atribución engañosa que conviene evitar: encontré republicaciones tituladas «AI is horrible at game design». En el hilo relacionado esa frase aparece como opinión de un comentarista. **No la atribuyo al desarrollador.** [doc del comentario, no del desarrollo](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/).

### 3. Herramientas y reparto de trabajo de «After the Wind»

| Área | Lo que permiten afirmar las fuentes | Lo que permanece sin verificar |
|---|---|---|
| Motor | Godot. Confirmado por publicaciones originales. [doc: optimización](https://www.instagram.com/p/DfK26HtIKQR/). | Versión exacta, renderizador, API gráfica y configuración de GI. |
| Código | Claude Code con Opus 5.5 según el desglose relacionado. [sec: proceso](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/). | Porcentaje de código generado, cambios manuales y cobertura de pruebas. |
| Conceptos | Bocetos humanos y conceptos en Codex con una habilidad que conoce el estilo. [doc: jefe](https://www.instagram.com/p/DfScKvloe1b/). | Modelo exacto de imagen empleado en cada ilustración. |
| Mallas | Tripo P2 para el jefe documentado; el desglose distingue recursos grandes y objetos pequeños hechos en Blender. [doc: jefe](https://www.instagram.com/p/DfScKvloe1b/), [sec: proceso](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/). | Que absolutamente todas las mallas sigan el mismo proceso. |
| Texturas | Tripo para el jefe y su armadura. [doc: proceso original](https://www.instagram.com/p/DfScKvloe1b/). | Resoluciones, mapas, UV y cantidad de retoque de todo el juego. |
| Animaciones | Claude en Blender para ese jefe, con videos de pingüinos como referencia. Cascadeur aparece también en la explicación del video. [doc: jefe](https://www.instagram.com/p/DfScKvloe1b/), [sec: segmento del video](https://www.youtube.com/watch?v=iJ83GYk2BIA&t=329s). | Reparto exacto entre animación manual, asistencia y generación para cada personaje. |
| Interfaz e ilustraciones | El video atribuye ilustraciones a ChatGPT; las capturas confirman un sistema gráfico coherente. [sec: video](https://www.youtube.com/watch?v=iJ83GYk2BIA&t=107s). | Herramienta de maquetación, fuente, atlas y proceso específico de cada componente de interfaz. |
| Efectos y ambiente | El autor documenta habilidades para efectos, postprocesado y clima por expedición. [doc: herramientas](https://www.instagram.com/p/De2FG-7IsIn/), [ambiente](https://www.instagram.com/p/De7X9jXoC6g/). | Técnicas exactas de niebla, sombras y tratamiento de color. |
| Música y sonido | No obtuve una atribución suficientemente verificable. | **Sin verificar.** No los atribuyo a Suno, ElevenLabs o Higgsfield por aparecer en otros proyectos. |

El presupuesto secundario aproxima unos 300 USD para suscripciones de Claude y Codex, 20 USD para Tripo y 50 USD para Cascadeur, dentro de un total redondeado de unos 400 USD mensuales. No permite calcular el coste total del proyecto ni incluye una valoración del trabajo humano. [sec: desglose](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/).

**No hay evidencia suficiente para afirmar que alguna fase completa se ejecutó autónomamente, sin selección ni correcciones.** Sí hay evidencia de generación de recursos y automatización de operaciones, acompañadas de dirección humana.

### 4. Qué falló y qué corrigió el creador

El ejemplo más concreto es el segundo jefe: el autor cambió la representación geométrica después de un resultado insatisfactorio. Esto demuestra que **pedir quads o marcar “low poly” no resuelve automáticamente las necesidades de una criatura animada**. Tampoco demuestra que 25.000 triángulos sean apropiados para todos los personajes o para tu portátil. [doc: jefe](https://www.instagram.com/p/DfScKvloe1b/); interpretación **[inf]**.

La publicación de rendimiento es especialmente relevante. El autor describe trabajo que seguía ejecutándose fuera de cámara, revisión de shaders y traslado de cálculos pesados a C++. Explica además que la hierba es una superficie de briznas que sigue la cámara. Las cifras publicadas corresponden a su Mac, con modelo, resolución y recorrido de prueba insuficientemente especificados. [doc: optimización](https://www.instagram.com/p/DfK26HtIKQR/).

La lección aplicable es **[inf]**: antes de aumentar calidad visual, comprobar qué se dibuja y simula, cuánto cuesta y cuándo puede dejar de procesarse. La elección de una técnica debe responder a esa medición.

### 5. Otros casos documentados de 2025–2026

No encontré una muestra amplia de juegos HD-2D terminados con repositorio, facturas y pruebas reproducibles. Los siguientes casos tienen distintos niveles de evidencia; no deben tratarse como equivalentes.

| Caso y fecha | Proceso documentado | Fallos o límites documentados | Fuerza de la evidencia |
|---|---|---|---|
| **The Little Prince: Across the Stars**, publicación consultada de 2026; fecha exacta sin verificar | Su autor declara 16 días, Opus 5.5 para desarrollo, Tripo y Blender para recursos, Unity para navegador. | El propio autor exige WebGPU, declara ausencia de alternativa WebGL2 y descargas grandes por capítulo. Coste total y autonomía real: sin verificar. | **[doc] Declaración original**, sin auditoría del proyecto. [Publicación](https://www.reddit.com/r/TopologyAI/comments/1x4xs3z/16_days_locked_in_opus_55_tripo_ai_blender_this/). |
| **Tidebreaker**, publicación consultada de 2026; fecha exacta sin verificar | El desglose identifica conceptos con GPT Images 2.5, Blender y Tripo P2, sprites con una herramienta propia, audio con ElevenLabs y código con Opus 5.5. | No localicé una explicación suficientemente detallada de fallos, costes o correcciones. **Sin verificar.** | **[sec] Desglose de demostración**; framework exacto sin verificar. [Publicación](https://www.reddit.com/r/TopologyAI/comments/1x4u616/gpt_image_2_tripo_ai_opus_55_an_oristyle/). |
| **Remote Delivery**, junio–agosto de 2026 | Claude para ideación, Nano Banana Pro para conceptos, Meshy para mallas/texturas, GIMP y Blender para correcciones, Unity para integración. | Huecos cerrados, simetría añadida, rampas que no encajan, caras ocultas incompletas y polígonos flotantes. | **[doc] Diario original con ejemplos.** Uso de agentes para escribir el conjunto del código: **sin verificar**. [Objetos](https://tealrobot.substack.com/p/how-i-make-3d-game-assets-with-ai), [túneles](https://tealrobot.substack.com/p/how-i-built-a-modular-tunnel-system), [texturas](https://tealrobot.substack.com/p/slop-isnt-the-only-objection-to-ai). |
| **Roguelike cenital sin título**, publicación consultada de 2026; fecha exacta sin verificar | Autor declara Meshy → Blender → Godot. | Reporta mejores resultados en objetos que en criaturas; tras numerosos intentos encargó el protagonista a un artista. | **[doc] Testimonio original**, sin proyecto auditado. Agente de código: **sin verificar**. [Experiencia publicada](https://www.reddit.com/r/meshyai/comments/1sjig1n/using_ai_generated_3d_assets_in_my_game_3_months/). |

*Remote Delivery* aporta una advertencia útil sobre el orden de operaciones. Su autor obtuvo mejores detalles texturizando antes de remallar, pero tuvo que eliminar caras flotantes después. **No es una regla universal:** es un resultado particular que invita a comparar ambos órdenes y comprobar qué preserva cada servicio. [doc: experiencia original](https://tealrobot.substack.com/p/slop-isnt-the-only-objection-to-ai); interpretación **[inf]**.

El autor también declara participación en el programa de colaboradores de Meshy. Esto no invalida sus ejemplos, pero impide tratar el relato como evaluación comercial independiente. [doc: declaración del artículo](https://tealrobot.substack.com/p/how-i-make-3d-game-assets-with-ai).

### 6. Lectura visual de las 14 capturas

Todo este apartado es **[inf]**, basado en inspección de las imágenes locales. Describe lo visible y propone explicaciones; no identifica código ni ajustes internos.

| Capturas | Observación | Técnica trasladable |
|---|---|---|
| `ref_02`, `05–08`, `10–11` | Exploración desde una cámara alta, terreno muy visible y poca deformación aparente por distancia. | Cámara 3/4 fija. Ensayar 50–60° de inclinación como punto de partida. Una imagen no permite distinguir con seguridad proyección ortográfica de perspectiva con poca convergencia. |
| `ref_01`, `14` | Cabeza grande, ojos simples, manos y botas legibles, masas de pelo amplias. | Personaje estilizado con pocos detalles pequeños. **La vista de cuerpo completo parece más próxima a 3,5–4 cabezas que a 2,5–3**, dependiendo de cómo se mida el pelo. Tu proporción puede ser deliberadamente distinta. |
| `ref_02`, `05–08`, `11` | Rocas con manchas amplias de color, musgo y aristas enfatizadas; caminos ocres sobre verdes variados. | Texturas pintadas que describen materiales a distancia. La lectura depende de masas y contraste, no solo de resolución. |
| `ref_05–12` | Hierba de tamaños y tonos distintos, espacios despejados y flores puntuales. | Combinar textura de suelo con mechones. Evitar cubrir todo con la misma densidad y orientación. |
| `ref_05–11` | Oscurecimientos suaves y contactos que integran objetos y terreno. | Conservar sombra de contacto y dirección luminosa coherente. No puede determinarse si emplea lightmaps, AO, GI o color pintado. |
| `ref_09`, `12` | Hub lateral: hierba delante, personajes y tiendas en la franja central, paisaje azulado detrás. | Composición de diorama con planos separados y perspectiva atmosférica. El paralaje es plausible, pero no demostrable mediante capturas. |
| `ref_03`, `04`, `10`, `12–14` | Papel cálido, pinceladas oscuras o turquesas, iconos ilustrados y jerarquía consistente. | Un pequeño sistema reutilizable de paneles, selección, avisos, leyendas y botones. El mapa y las viñetas comparten el lenguaje del juego. |

Hay una precisión terminológica importante: **parte de esta interfaz está tematizada como objetos físicos, pero el HUD superpuesto no es necesariamente diegético**. La apariencia de pergamino y la existencia dentro del mundo son propiedades distintas. **[inf]**

El referente tampoco demuestra un proceso de pixel art. En las capturas domina una apariencia pintada con personajes y escenarios volumétricos. Adoptar sus principios no obliga a utilizar sprites ni a reproducir todos los efectos asociados a otros juegos HD-2D. **[inf]**

### 7. Traducción a Godot 4.7 y la Intel HD 620

#### Renderizado e iluminación

Propongo **[inf]** tres escalones:

1. **Base:** Compatibility, escenario pequeño, luz ambiental, una luz direccional y sombras limitadas.
2. **Mejora condicionada:** lightmaps para geometría estática, si un horneado local resulta estable y práctico.
3. **Comparación puntual:** Mobile cuando una necesidad visual justifique probarlo. Forward+ quedaría para experimentos acotados.

La documentación distingue los renderizadores y sus controladores; la elección no puede resolverse únicamente por el nombre de la GPU. La compatibilidad efectiva con tu controlador y el rendimiento quedan pendientes de prueba. [doc: renderizadores](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html), [requisitos](https://docs.godotengine.org/en/4.7/about/system_requirements.html).

Si se hornea toda la iluminación directa e indirecta, las superficies estáticas dejan de recibir ciertas sombras dinámicas como en una configuración completamente dinámica. Para ese caso, la propia documentación contempla sombras de contacto simplificadas. Hay que elegir conscientemente entre iluminación completamente horneada e iluminación híbrida. [doc: modos de LightmapGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html).

**No recomiendo SDFGI como requisito artístico:** las capturas no prueban que se haya utilizado y su coste contradice la prioridad de un prototipo ligero. **[inf; A7]**

#### Sombras sobre sprites

Si se elige un protagonista 2D, debe situarse dentro de la escena 3D mediante `Sprite3D` o `AnimatedSprite3D` para participar en su iluminación. Un `Sprite2D` del HUD pertenece a otro sistema de representación. [doc: SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html).

El ensayo propuesto **[inf]** sería: un sprite con `shaded`, una pared y una luz que proyecte sombra. Revisar recepción, recorte y orden de transparencias desde la cámara final. La sombra proyectada por el propio personaje puede simplificarse con una mancha de contacto si la silueta del billboard da resultados poco convincentes.

Esta ruta sigue siendo alternativa. El personaje 3D sencillo encaja mejor con lo observado y permite evaluar el recurso desde los dos encuadres del tablero. **[inf]**

#### Vegetación y composición

Recomiendo **[inf]** producir primero un suelo convincente y añadir hierba solamente donde contribuya a la silueta. Los MultiMesh se dividirían por zonas para evitar mantener un grupo enorme visible por una sola parte. La limitación de descarte individual está documentada. [doc: MultiMesh](https://docs.godotengine.org/en/4.7/tutorials/performance/using_multimesh.html).

Para el hub, la primera prueba puede usar geometría sencilla en la franja jugable y fondos ilustrados separados. Cámara, contraste y superposición deben funcionar antes de añadir movimiento ambiental. **[inf]**

### 8. Proceso de arte propuesto con los recursos disponibles

Este proceso es **[inf]**, apoyado en los casos anteriores y en tu catálogo local:

**Referencia aprobada → generación de una pieza → inspección en Godot → reducción o remallado si hace falta → textura y UV comprobadas → animación → aprobación final.**

Conviene fijar:

- **Referencia artística:** paleta, proporciones, materiales y ejemplos propios aprobados.
- **Ficha por recurso:** herramienta, parámetros, referencia, coste, intentos, defectos y aprobación.
- **Inspección geométrica:** frente, espalda, laterales y base; piezas móviles separadas y pivote utilizable.
- **Inspección animada:** caminar, girar y una acción representativa; comprobar deformaciones y contacto con el suelo.
- **Inspección visual:** legibilidad a tamaño real dentro del juego.
- **Inspección de rendimiento:** incorporar recursos progresivamente y medir el cambio.

No equipararía remallado automático con topología adecuada para animar. Tampoco confundiría las UV de textura con las UV2 requeridas para lightmaps. [inf: casos de A3 y A6; doc: requisitos UV2 de LightmapGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html).

Con Blender ausente, propondría recibir **GLB** y usar escenas heredadas o envoltorios propios para integrar el recurso. Las reparaciones profundas seguirían pendientes; no deben ocultarse bajo la etiqueta «listo para juego». [inf; doc: importación](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).

#### Piloto de créditos

Las cantidades siguientes proceden de **cotizaciones locales**, no de generaciones completadas. Algunas usaron marcadores o URL ficticias; no demuestran que el recurso final vaya a funcionar ni que todas las combinaciones mantengan el precio.

| Ensayo propuesto | Créditos cotizados |
|---|---:|
| Cuatro conceptos, `gpt_image_2_6`, high, 1k | 6 |
| Tres pruebas de recursos con `tripo_h3_1_image_to_3d`, configuración cotizada por defecto | 27 |
| Una comparación con `tripo_p2_image_to_3d`, configuración cotizada por defecto | 34 |
| Un remallado y un retexturizado con las configuraciones cotizadas | 15,5 |
| **Total previsto** | **82,5** |
| **Margen hasta el límite propuesto de 100** | **17,5** |

Fuente **[doc local]**: [hf_costos_matriz.md](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).

No incluyo un precio para rigging genérico: la matriz devuelve errores de estimación. Tampoco traslado a Higgsfield las condiciones de reintento o precios publicados para Tripo o Meshy contratados directamente.

La recomendación económica **[inf]** es aprobar primero imágenes de referencia y comparar después calidad utilizable por crédito. El proceso completo de personaje animado sigue **sin coste verificado**.

### 9. Código, datos y control de versiones

Recomiendo **[inf]** aprovechar las escenas y nodos de Godot mediante composición: movimiento, interacción, inventario y presentación separados. Los datos de objetos, misiones y actividades educativas deben poder cambiar sin reescribir sus comportamientos. No hay evidencia de que un ECS propio sea necesario para la escala inicial. [doc: organización de escenas](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html).

La lección de las herramientas persistentes del referente puede aplicarse con documentos sencillos: decisiones vigentes, tarea actual, criterios de aceptación y resultado de la última comprobación. No exige replicar sus suscripciones ni su infraestructura. **[inf; A5]**

Para Git recomiendo **[inf]** mantener código, escenas textuales y documentación en Git; usar LFS selectivamente para binarios grandes y no versionar cachés regenerables. LFS separa el almacenamiento de esos archivos del historial Git ordinario; no elimina sus necesidades de espacio. [doc: control de versiones y LFS](https://docs.godotengine.org/en/4.7/tutorials/best_practices/version_control_systems.html).

La primera automatización debería comprobar importación y exportación, usando la misma versión del motor y sus plantillas. La exportación sin interfaz está documentada, pero una ejecución `headless` no valida el aspecto visual ni el rendimiento de la HD 620. [doc: línea de comandos](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html); alcance de la validación **[inf]**.

### 10. Puerta de validación antes de producir contenido

La prueba propuesta **[inf]** es una escena pequeña con protagonista, gato, camino, rocas, hierba y una interacción educativa breve. Debe permitir verificar:

1. Lectura del personaje y del camino desde la cámara final.
2. Movimiento, contacto con el suelo y una interacción.
3. HUD legible y dos paneles representativos.
4. Rendimiento durante un recorrido repetible, con resolución y ajustes registrados.
5. Coste por recurso aceptado y número de correcciones.
6. Tiempo y estabilidad de importación; horneado separado si se evalúa LightmapGI.

La aprobación debería basarse en esa escena jugable y sus mediciones. **Hasta entonces, alcanzar el acabado del tablero en tu portátil es una hipótesis de producción.**

## Fuentes

**Primarias del referente**

- [Video completo y capítulos, 2 de noviembre de 2026](https://www.youtube.com/watch?v=iJ83GYk2BIA).
- [Estado de desarrollo temprano, 24 de octubre](https://www.instagram.com/p/De4rsmxoH_Z/).
- [Herramientas persistentes del creador, 23 de octubre](https://www.instagram.com/p/De2FG-7IsIn/).
- [Postprocesado y clima, 25 de octubre](https://www.instagram.com/p/De7X9jXoC6g/).
- [Optimización, 31 de octubre](https://www.instagram.com/p/DfK26HtIKQR/).
- [Proceso de un jefe, 3 de noviembre](https://www.instagram.com/p/DfScKvloe1b/).

**Desgloses secundarios**

- [r/TopologyAI: herramientas, tiempo y presupuesto de «After the Wind»](https://www.reddit.com/r/TopologyAI/comments/1xdfp4f/no_coding_or_gamedev_background_6_weeks_with_opus/).
- [r/TopologyAI: proceso detallado del jefe](https://www.reddit.com/r/TopologyAI/comments/1xmzbn2/codex_3d_ai_opus_55_from_a_notebook_sketch_to_an/).
- [r/TopologyAI: Tidebreaker](https://www.reddit.com/r/TopologyAI/comments/1x4u616/gpt_image_2_tripo_ai_opus_55_an_oristyle/).

**Otros relatos originales**

- [The Little Prince: Across the Stars](https://www.reddit.com/r/TopologyAI/comments/1x4xs3z/16_days_locked_in_opus_55_tripo_ai_blender_this/).
- [Remote Delivery: objetos, junio de 2026](https://tealrobot.substack.com/p/how-i-make-3d-game-assets-with-ai).
- [Remote Delivery: túneles, julio de 2026](https://tealrobot.substack.com/p/how-i-built-a-modular-tunnel-system).
- [Remote Delivery: texturas y correcciones, agosto de 2026](https://tealrobot.substack.com/p/slop-isnt-the-only-objection-to-ai).
- [Experiencia con recursos 3D en un roguelike](https://www.reddit.com/r/meshyai/comments/1sjig1n/using_ai_generated_3d_assets_in_my_game_3_months/).

**Documentación técnica primaria**

- [Godot 4.7: requisitos](https://docs.godotengine.org/en/4.7/about/system_requirements.html).
- [Renderizadores](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).
- [Arquitectura de renderizado](https://docs.godotengine.org/en/4.7/engine_details/architecture/internal_rendering_architecture.html).
- [SDFGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_sdfgi.html).
- [LightmapGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html).
- [SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html).
- [MultiMesh](https://docs.godotengine.org/en/4.7/tutorials/performance/using_multimesh.html).
- [Formatos 3D](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html).
- [Organización de escenas](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html).
- [Git y LFS](https://docs.godotengine.org/en/4.7/tutorials/best_practices/version_control_systems.html).
- [Línea de comandos y exportación](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html).

**Material local**

- Capturas `ref_01.jpg`–`ref_14.jpg` en [Tablero_usuario](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Referencias/Tablero_usuario>).
- [Matriz de costes](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).
- [Costes por defecto](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_default.md>).
- [Catálogo local de parámetros](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>).