# Fase 0 — Pila de renderizado para Godot 4.7 y la Intel HD 620

## Resumen ejecutivo

**Recomiendo Compatibility como renderizador principal**, con mundo 3D sencillo, personajes chibi de baja complejidad, texturas pintadas, iluminación ambiental y una luz principal. La resolución inicial debe ser **1280×720 para el mundo 3D**, conservando la interfaz a resolución de pantalla. [inf]

**LightmapGI es una mejora opcional**, condicionada a una prueba de horneado. Compatibility puede mostrar y hornear lightmaps mediante un RenderingDevice temporal, pero el horneado requiere una GPU con compute compatible; OpenGL por sí solo no basta. [doc]

**Mobile con D3D12 será el plan B**, sujeto a medición, si DOF, decals o su comportamiento de rendimiento justifican el cambio. Forward+, SDFGI y VoxelGI quedan fuera de la configuración de producción propuesta. [inf]

El acabado del tablero debe buscarse mediante composición, siluetas, materiales y profundidad por capas. No depende de activar todos los efectos avanzados. Los presupuestos de este informe son hipótesis de trabajo: **no se ejecutó Godot ni un benchmark en este equipo**. [inf]

## Decisiones recomendadas

Las recomendaciones son **[inf]**; sus fundamentos documentales aparecen en las secciones siguientes.

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Renderizador principal | Compatibility, OpenGL | Forward+ como requisito: añade funciones y costo que todavía no están justificados | Media |
| Plan B | Mobile con D3D12; comparar también Vulkan | Elegir una API únicamente por su versión anunciada: no demuestra estabilidad ni rendimiento | Media |
| GI inicial | Sin GI: ambiente, luz principal, relleno limitado y oclusión artística | SDFGI: costo elevado, riesgos con Intel y cámara ortogonal | Alta |
| GI para escenarios terminados | LightmapGI si supera la prueba local de horneado e iteración | VoxelGI: exige Forward+ y mantiene un costo de GI en ejecución | Media |
| Resolución | Mundo 3D a 720p; UI a resolución de pantalla | 1080p nativo como mínimo obligatorio: procesa 2,25 veces más píxeles | Alta |
| Cámara de exploración | Perspectiva, FOV vertical inicial de 30°, inclinación descendente de 55° | FOV amplio: altera demasiado escala y siluetas durante el desplazamiento | Media |
| Cámara del hub | Ortogonal, encuadre lateral fijo y profundidad por capas | Gran escenario completamente modelado hasta el horizonte: gasto poco útil para ese encuadre | Media |
| Personajes principales | Chibi 3D; sprites para elementos donde aporten una ventaja clara | Convertir todo a sprites: complica personalización, direcciones y sombras | Media |
| Sombras de sprites | Recorte alfa y proxy independiente; blob como opción económica | Depender del billboard visible para una sombra estable desde cualquier cámara | Alta |
| Materiales | StandardMaterial3D sencillo; toon y rim selectivos | Shader personalizado universal: más trabajo de mantenimiento y validación | Alta |
| Contornos | Casco invertido únicamente en personajes u objetos importantes | Contornos de pantalla completa por normales: exigen Forward+ para el búfer integrado | Alta |
| Puerta de rendimiento | 30 fps sostenidos a 720p y sesión prolongada estable | Aprobar por una captura bonita o por FPS medios de una escena vacía | Alta |

## Afirmaciones que sostienen las decisiones

1. **[doc]** Forward+ y Mobile utilizan RenderingDevice y pueden emplear Vulkan o D3D12 en Windows; Compatibility utiliza OpenGL. El método de renderizado y la API son decisiones diferentes. [Comparación oficial][R1]

2. **[doc]** Intel incluye la HD 620 en su tabla de soporte de DirectX 12, OpenGL 4.6 y Vulkan. Esa tabla describe capacidades de la familia y controladores adecuados; **la versión efectiva de Vulkan y el nivel de funciones de D3D12 con el controlador 31.0.101.2140 en este portátil están sin verificar**. [APIs de Intel][R2]

3. **[doc]** Existen reportes primarios de ventanas vacías con Vulkan en UHD 620 y de iluminación SDFGI incorrecta en Intel Windows. Son antecedentes con otros controladores/versiones, no una reproducción del problema en esta HD 620. [Ventana vacía][R3], [SDFGI en Intel][R4]

4. **[doc]** LightmapperRD hornea mediante compute shaders. No requiere instalar CUDA ni OpenCL. En Compatibility crea un RenderingDevice temporal; reproducir lightmaps ya horneados no exige RenderingDevice. [LightmapperRD][R5]

5. **[doc]** LightmapGI necesita UV2 sin solapamientos para superficies estáticas. Los objetos móviles reciben iluminación indirecta mediante probes; no adquieren automáticamente un lightmap superficial animado. [LightmapGI][R6]

6. **[doc]** SDFGI es una de las soluciones de GI más exigentes de Godot, funciona únicamente en Forward+ y no incorpora oclusores dinámicos. Existe además una incidencia abierta sobre artefactos con cámara ortogonal. [SDFGI][R7], [Incidencia ortogonal][R8]

7. **[doc]** Sprite3D y AnimatedSprite3D heredan las opciones de SpriteBase3D. Sus billboards se orientan hacia la cámara también al dibujar sombras; con varias cámaras, la documentación advierte comportamiento indefinido. [SpriteBase3D][R9]

8. **[doc]** DOF mediante CameraAttributes está disponible en Forward+ y Mobile, y no en Compatibility. CameraAttributesPractical permite controlar directamente las zonas cercanas y lejanas de desenfoque. [CameraAttributesPractical][R10]

9. **[doc]** El escalado bilineal 3D funciona en los tres renderizadores. FSR 1.0 y FSR 2.2 están documentados para Forward+; su costo puede anular el beneficio en GPU lentas. [Escalado 3D][R11]

10. **[doc]** La profundidad de pantalla puede consultarse en los tres renderizadores, pero el búfer integrado de normales/rugosidad solo existe en Forward+. Esto condiciona los contornos de posproceso. [Lectura de pantalla][R12]

11. **[doc]** MultiMesh reduce el costo de dibujar muchas instancias, pero no realiza descarte de visibilidad individual por instancia. Conviene dividir la vegetación en grupos espaciales. [MultiMesh][R13]

12. **[inf]** Compatibility a 720p es el punto de partida más prudente para este proyecto; su superioridad frente a Mobile en este portátil **está sin verificar**. La documentación recomienda investigar los cuellos de botella en el hardware concreto. [Optimización de GPU][R14]

## Riesgos y cómo mitigarlos

| Riesgo | Consecuencia | Mitigación propuesta |
|---|---|---|
| Confundir soporte de API con estabilidad | Elegir Vulkan o D3D12 y descubrir fallos durante producción | Probar explícitamente cada combinación; registrar la API y el renderizador que realmente arrancaron |
| Horneado demasiado lento o fallido | Interrupciones frecuentes del trabajo | Empezar con una habitación y calidad baja; mantener iluminación sin GI como configuración completa |
| Hierba con demasiado recorte alfa | Pérdida de rendimiento aunque existan pocos triángulos | Reducir superficie vacía de las tarjetas, densidad y solapamientos; comparar con mechones opacos |
| Sombras dependientes del billboard | La sombra cambia al mover la cámara | Desactivar su sombra visible y usar proxy o blob |
| Diferencias de color entre renderizadores | Escenarios con aspecto distinto después de cambiar de método | Mantener capturas de referencia y ajustes explícitos por perfil |
| Picos ocultos por el promedio de FPS | Movimiento irregular y combate poco agradable | Medir percentiles de tiempo de cuadro y contar cuadros largos |
| Memoria compartida y poca RAM disponible | Paginación, pausas y cierres | Cargar por zonas, limitar texturas residentes y medir editor más juego |
| Pérdida de rendimiento tras varios minutos | La prueba breve parece suficiente, la sesión real falla | Repetir recorridos después de una sesión de 20 minutos |
| Optimizar una escena demasiado simple | El presupuesto falla cuando aparecen UI, NPC y agua | Incluir esos elementos desde la prueba representativa |

Las mitigaciones son **[inf]**. Sus fundamentos son los costos documentados de transparencias, sombras, materiales y organización de instancias. [Optimización de GPU][R14], [Optimización 3D][R15]

## Preguntas que debe decidir el usuario

Estas decisiones pueden resolverse al revisar la prueba visual; no bloquean este informe.

1. **Objetivo mínimo:** ¿se acepta 720p y 30 fps estables como base? Recomiendo aprobar ese objetivo y tratar 1080p/60 fps como mejoras. [inf]
2. **Desenfoque:** ¿el tilt-shift debe estar presente durante la exploración o puede reservarse para escenas concretas? Recomiendo mantener legible el plano de juego y dejar el DOF opcional. [inf]
3. **Tratamiento de personajes:** ¿se prioriza personalización 3D o apariencia de sprite ilustrado? Recomiendo personajes principales 3D, coherentes con el tablero, y probar sprites para NPC secundarios y efectos. [inf]
4. **Iluminación cambiante:** ¿el primer escenario necesita un ciclo continuo de día y noche? Recomiendo comenzar con estados artísticos discretos para facilitar la iluminación y su validación. [inf]

## Desarrollo

### 1. Alcance y grado de verificación

Fecha de consulta: **2026-11-12**. Se consultó documentación de la rama **4.7**, notas oficiales de 4.4–4.7, información de Intel y reportes primarios del repositorio de Godot.

Se revisaron el análisis local del tablero y capturas de exploración, hub y personalización. Las imágenes permiten orientar la dirección visual, pero no revelan el motor, shaders, geometría o iluminación utilizados por el juego mostrado. Cualquier traducción de ese acabado a una técnica concreta se identifica como **[inf]**.

Se toma **Godot 4.7.2-stable** y la configuración del equipo como datos del brief. No se ejecutó el motor, no se instalaron herramientas, no se modificaron archivos y no se consumieron créditos de Higgsfield.

### 2. Renderizadores y APIs

#### Matriz de funciones de Godot 4.7

**[doc]** La disponibilidad siguiente corresponde a la documentación consultada. “Sí” significa que existe la función; no implica que sea conveniente activarla en la HD 620. [Renderizadores][R1], [Antialiasing][R16], [CameraAttributes][R10], [Escalado][R11]

| Función | Forward+ | Mobile | Compatibility |
|---|---|---|---|
| API en Windows | Vulkan / D3D12 | Vulkan / D3D12 | OpenGL |
| SDFGI | Sí | No | No |
| VoxelGI | Sí | No | No |
| LightmapGI: reproducción | Sí | Sí | Sí |
| LightmapGI: horneado | GPU con RenderingDevice | GPU con RenderingDevice | RenderingDevice temporal |
| SSAO | Sí | No | Sí, implementación simplificada |
| SSIL | Sí | No | No |
| SSR | Sí | No | No |
| Niebla volumétrica | Sí | No | No |
| Niebla de profundidad/altura | Sí | Sí | Sí |
| Decals | Sí | Sí | No |
| Glow | Sí | Sí | Sí, implementación diferente |
| DOF | Sí | Sí | No |
| MSAA 3D | Sí | Sí | Sí |
| TAA | Sí | No | No |
| FXAA / SMAA integrados | Sí | Sí | No |
| FSR 1.0 / 2.2 | Sí | No | No |
| Escalado bilineal 3D | Sí | Sí | Sí |
| Sombras direccionales, omni y spot | Sí | Sí | Sí |
| PCSS direccional | Sí | No | No |
| PCSS omni/spot | Sí | Sí | No |
| Búfer de normales/rugosidad para shaders | Sí | No | No |
| Compute para shaders propios | Sí | Sí | No |

**[doc]** Compatibility utiliza un tratamiento diferente para luces con sombra, mediante varias pasadas y con diferencias de mezcla que pueden cambiar su apariencia. Por ello, trasladar valores de energía entre renderizadores no garantiza el mismo resultado. [Luces y sombras][R17]

#### Viabilidad en la HD 620

**Compatibility — candidato principal. [inf]**  
Permite construir el estilo propuesto con iluminación directa, materiales estilizados, sombras, niebla sencilla y vegetación instanciada. Su elección busca reducir dependencias de funciones avanzadas y del controlador.

**Mobile — candidato que merece una comparación. [inf]**  
Su nombre no lo limita a teléfonos. Puede servir en escritorio y ofrece DOF y decals. No debe suponerse más rápido o más lento que Compatibility en todas las escenas: materiales, luces y cantidad de llamadas de dibujo cambian la comparación. [doc: Renderizadores][R1]

**Forward+ — técnicamente posible de investigar, sin aprobación para producción. [inf]**  
Los requisitos mínimos de Godot contemplan gráficas integradas con soporte adecuado, pero esos mínimos corresponden a proyectos sencillos. No demuestran que SDFGI, SSR o niebla volumétrica sean prácticos aquí. [doc: Requisitos][R18]

#### Vulkan, D3D12 y controladores Intel

**[doc]** La tabla de Intel anuncia las APIs de la familia HD 620. Para Godot, Vulkan 1.0 completo es la base documentada del backend Vulkan; los requisitos de ejecución con D3D12 incluyen nivel de funciones 12_0. La capacidad efectiva debe comprobarse con el motor y el controlador concreto. [Intel][R2], [Requisitos de Godot][R18]

Hay tres evidencias que conviene distinguir:

| Evidencia primaria | Lo que demuestra | Lo que permanece sin verificar |
|---|---|---|
| Ventana vacía con UHD 620, Vulkan y controlador antiguo [R3] | Existieron problemas de inicialización/renderizado en esa combinación | Que ocurra con HD 620 y 31.0.101.2140 |
| SDFGI incorrecto en UHD 620 con Intel Windows [R4] | Existe un antecedente concreto de errores de GI | Reproducción y solución en 4.7.2 sobre este portátil |
| Reporte de 2026 con HD 620, 31.0.101.2140 y Godot 4.7.1 usando D3D12 [R19] | Otra máquina logró ejecutar ese entorno | Rendimiento, estabilidad prolongada o compatibilidad completa |

Los tres son **[doc] como registros primarios**, no certificaciones de compatibilidad. No encontré una prueba que permita declarar que todas las Intel de séptima generación fallan con Godot 4, ni que este controlador elimine todos los problemas. **La estabilidad exacta permanece sin verificar.**

**[doc]** Intel mantiene esta familia bajo un modelo de soporte heredado. Su página consultada ofrece un controlador posterior al instalado, pero eso no demuestra que actualizar resuelva un problema de Godot. Este informe no depende de instalarlo. [Soporte Intel][R20]

**[inf]** Para Mobile, probar primero D3D12 y después Vulkan. Fijar la API explícitamente y comprobar el registro de arranque: el fallback automático puede hacer que una prueba termine ejecutándose en otro renderizador.

### 3. Iluminación global

#### Comparación práctica

| Técnica | Características documentadas | Aplicación propuesta |
|---|---|---|
| SDFGI | GI semidinámica, seguimiento por cascadas y alto costo; sin oclusores dinámicos [R7] | Descartar del objetivo mínimo [inf] |
| VoxelGI | GI en tiempo real para espacios pequeños/medianos; requiere Forward+ [R21] | No usar como solución principal [inf] |
| LightmapGI | Iluminación superficial estática; probes para objetos móviles [R6] | Candidato para escenarios cerrados y terminados [inf] |
| Sin GI | Iluminación directa y ambiente, sin rebotes calculados | Configuración inicial y alternativa completa [inf] |

#### Horneado de LightmapGI en este equipo

**[doc]** El requisito decisivo es **RenderingDevice con compute operativo**. El horneador integrado no es una alternativa de CPU para máquinas que únicamente puedan usar OpenGL. Compatibility puede solicitar un RenderingDevice temporal sin cambiar el renderizador de reproducción del proyecto. [LightmapperRD][R5]

Por tanto:

- **¿Necesita Vulkan?** Necesita el backend RenderingDevice; no debe expresarse como “solo Vulkan” porque Godot también dispone de D3D12. El horneado exitoso con cada API en este equipo está **sin verificar**. [doc/inf]
- **¿Necesita GPU con compute?** Sí, para LightmapperRD. [doc]
- **¿Necesita GPU dedicada?** La documentación no la exige como condición absoluta; sí identifica ventajas de velocidad en GPU dedicadas. La utilidad práctica de la HD 620 debe medirse. [doc/inf]
- **¿Funciona en un proyecto Compatibility?** Sí, condicionado a que pueda crear ese RenderingDevice temporal. [doc]

**[doc]** Los tiempos pueden ir de segundos a horas según la escena y calidad. No existe una cifra verificada para este portátil. El tamaño del lightmap y el supersampling también incrementan la memoria necesaria. [LightmapGI][R6]

Configuración inicial propuesta para experimentar, **no valores óptimos medidos**:

| Parámetro | Punto de partida [inf] |
|---|---|
| Escena | Una habitación o tramo pequeño de exterior |
| Calidad | Baja para iteración |
| Rebotes | 1–2 inicialmente |
| Supersampling | Desactivado |
| Denoiser | JNLM integrado |
| Atlas | Comenzar con 512–1024 por página y revisar el resultado |
| Geometría incluida | Arquitectura y suelo estáticos; excluir hierba animada y personajes |
| Iteración | Hornear cuando cambie la iluminación o geometría relevante |

**[doc]** JNLM está incluido y funciona mediante compute. OIDN es un denoiser externo; que pueda ejecutar su etapa de denoising en CPU no convierte el horneado completo de Godot en un proceso de CPU. [LightmapGI][R6]

#### UV2 y objetos móviles

**[doc]** Las UV2 deben asignar espacio exclusivo a las caras y contar con separación suficiente entre islas. Godot puede generarlas al importar; no hace falta Blender para esa operación. Conviene conservar los archivos `*.unwrap_cache` para mantener consistencia entre importaciones. [LightmapGI][R6]

**[inf]** Revisar UV2 antes de aceptar una malla generada con IA. Una textura de color correcta no demuestra que la malla esté preparada para lightmaps.

**[doc]** Si una luz hornea toda su contribución sobre el escenario estático, los objetos móviles no proyectan automáticamente su sombra dinámica sobre esas superficies. Para conservarla, puede mantenerse dinámica la luz direccional y hornear su contribución indirecta, o utilizar blobs. [LightmapGI][R6]

#### SDFGI y cámaras ortogonales

**[doc]** La incidencia ortogonal consultada sigue abierta. Eso permite afirmar que hay un problema conocido; no justifica declarar que cualquier cámara ortogonal es absolutamente incompatible. [Incidencia][R8]

**[inf]** SDFGI queda descartado por la combinación de costo, convergencia, cascadas y riesgo de controladores. Cambiar la cámara a perspectiva no resuelve esas otras limitaciones.

#### Iluminación sin GI

Propuesta artística **[inf]**:

- Ambiente moderado para evitar negros sin información.
- Una luz principal cálida.
- Relleno frío tenue cuando el ambiente no baste.
- Oclusión pintada en contactos y cavidades.
- Sombras de contacto simples bajo personajes.
- Fondos progresivamente más claros y menos contrastados.

Este tratamiento debe validarse con movimiento y cambios de iluminación. Una sombra pintada muy direccional puede entrar en conflicto con la luz dinámica. [inf]

### 4. Sprites 2D y sombras en un mundo 3D

#### Configuración de partida

**[doc]** Sprite3D y AnimatedSprite3D ofrecen recorte alfa, billboard, sombreado y opciones heredadas de proyección de sombra. El sombreado del sprite está desactivado por defecto; debe habilitarse cuando se quiera integrar su iluminación con la escena. [SpriteBase3D][R9]

| Modo | Comportamiento | Uso propuesto |
|---|---|---|
| Alpha normal | Mezcla parcial; problemas de ordenación; los materiales de mezcla alfa no proyectan sombras | VFX y elementos translúcidos [inf] |
| `ALPHA_CUT_DISCARD` | Transparencia binaria; evita buena parte de la ordenación problemática | Primera opción para sprites y vegetación [inf] |
| `ALPHA_CUT_OPAQUE_PREPASS` | Dibuja primero la parte opaca y después la translúcida; mayor costo | Solo si mejora bordes de forma visible [inf] |
| Alpha hash | Representa transparencia mediante patrón | Evaluación secundaria: puede introducir ruido en elementos pequeños [inf] |

Comportamientos **[doc]**: [SpriteBase3D][R9], [Materiales 3D][R22].

**[doc]** El prepass no elimina universalmente los errores entre regiones parcialmente transparentes. Tampoco MSAA por sí solo suaviza el borde interno de un recorte alfa; para eso debe evaluarse alpha-to-coverage. [Materiales][R22], [Antialiasing][R16]

#### Billboard y orientación de la sombra

**[doc]** El billboard sigue la cámara al dibujar sombras. Su silueta proyectada puede variar al cambiar el encuadre; con varias cámaras, la documentación advierte un resultado indefinido. [SpriteBase3D][R9]

Soluciones:

| Solución | Implementación propuesta [inf] | Límite |
|---|---|---|
| Malla proxy solo sombra | Cápsula o figura simple independiente del billboard; `SHADOWS_ONLY` | Aproxima la silueta |
| Doble sprite | Sprite visible con billboard y sombra desactivada; segundo sprite sin billboard, solo sombra | Hay que sincronizar animación y orientación |
| Blob con quad | Quad elíptico con textura suave, sin iluminación, adaptado al suelo | No se proyecta automáticamente sobre paredes/escalones |
| Blob con Decal | Proyección sobre superficies receptoras en Mobile/Forward+ | Decal no está disponible en Compatibility |

**[doc]** `SHADOW_CASTING_SETTING_SHADOWS_ONLY` conserva la sombra sin mostrar la geometría. No equivale a ocultar el nodo con `visible = false`. [GeometryInstance3D][R23]

**[inf]** Para personajes 3D, comenzar con su sombra normal y comparar un proxy simplificado. Para sprites, comenzar con blob o proxy independiente.

#### Transparencias y z-fighting

**[doc]** Godot ordena los objetos con mezcla alfa de atrás hacia delante; las superficies superpuestas pueden producir errores. La profundidad de cámara y la separación geométrica también afectan artefactos de profundidad. [Materiales][R22], [Camera3D][R24]

Medidas propuestas **[inf]**:

- Mantener la prueba de profundidad activa.
- Ajustar el origen del sprite a sus pies.
- Separar físicamente capas de follaje y decoración.
- Mantener el blob ligeramente separado del suelo, adaptando esa distancia a la escala.
- Usar rangos de cámara ajustados al escenario.
- Reservar `render_priority` para casos concretos: no corrige intersecciones geométricas.
- Evitar cambiar arbitrariamente la profundidad del personaje para forzar su orden visual.

### 5. Cámaras, resolución y estabilidad visual

#### Exploración 3/4 alta

Configuración inicial **[inf]**:

- Perspectiva.
- FOV vertical de **30°**, comparando 25–35°.
- Inclinación de **55° bajo la horizontal**, comparando 50–60°.
- Azimut fijo por zona.
- Distancia de cámara ajustada para mantener el tamaño del protagonista.
- Movimiento de seguimiento suave, sin rotación libre inicialmente.

**[doc]** La perspectiva reduce el tamaño aparente con la distancia; la cámara ortogonal conserva ese tamaño. [Camera3D][R24]

**[inf]** La ortogonal merece una variante de prueba si se busca una lectura más gráfica o una escala constante de sprites. La perspectiva de FOV bajo es mi primera opción para el chibi 3D y los relieves del tablero.

#### Hub lateral

Propuesta **[inf]**:

- Cámara ortogonal.
- Inclinación descendente leve, aproximadamente 8–15°, ajustada al suelo visible.
- Plano principal de desplazamiento claramente definido.
- Primer plano, zona de juego y fondo con separación espacial.
- Montañas y cielo mediante planos o imágenes cuando no necesiten interacción.
- Profundidad atmosférica mediante color y niebla sencilla.

La apariencia de diorama no exige DOF: también depende de encuadre, escala, capas y contraste. [inf]

#### DOF y tilt-shift

**[doc]** CameraAttributesPractical ofrece controles de desenfoque cercano y lejano en Mobile y Forward+. No funciona sobre viewports con fondo transparente. [CameraAttributesPractical][R10]

**[inf]** El DOF convencional puede sugerir una miniatura, pero no representa una óptica tilt-shift completa. En este proyecto conviene mantener nítidos personaje, objetos interactivos y sendero.

En Compatibility, la alternativa inicial es usar fondos previamente suavizados y menor contraste. Un desenfoque personalizado de pantalla añade costo y debe aprobarse mediante comparación. [inf]

#### Evitar temblor

Hay que separar **temblor de movimiento** y **aliasing de imagen**.

**[doc]** Para movimiento, Godot permite interpolación física 3D. La documentación propone que una cámara manual siga la transformación interpolada del objetivo desde `_process()`, evitando heredar simultáneamente movimientos que produzcan interpolación duplicada. [Interpolación][R25]

Medidas visuales propuestas **[inf]**:

- Mantener resolución interna y tamaño del sprite estables durante la comparación.
- Evitar líneas y mechones más pequeños que un píxel.
- Usar mipmaps en texturas pintadas vistas a distancia.
- Comparar MSAA 2× con ausencia de MSAA.
- Para sprites pixel art, probar cuantización de la presentación a la rejilla de píxeles; conservar físicas continuas.
- No aplicar pixel snapping a todo el proyecto si la dirección final es pintura suave.

#### 720p, 1080p y stretch

**Recomendación principal [inf]:**

| Elemento | Ajuste |
|---|---|
| Tamaño lógico inicial de UI | 1280×720 |
| Stretch | `canvas_items` |
| Aspecto inicial | `keep`, para conservar el encuadre 16:9 |
| Pantalla de 1920×1080 | UI renderizada a resolución de salida |
| Mundo 3D | Escala aproximada de `0.6667`, equivalente a 1280×720 |
| Filtro de escalado | Bilineal |
| Perfil opcional | Escala 3D `1.0`, si 1080p supera el benchmark |

**[doc]** `canvas_items` no reduce por sí mismo la resolución del mundo 3D. El modo `viewport` sí escala el viewport completo, incluida la interfaz. El escalado 3D permite reducir el mundo sin reducir los elementos 2D. [Múltiples resoluciones][R26]

**[inf]** El modo `viewport` a 1280×720 es una alternativa sencilla, pero debe revisarse la legibilidad de DotGothic16 al ampliarse. No lo tomaría como primera opción para una interfaz de texto abundante.

**[doc]** Godot 4.7 incorpora escalado 3D nearest. La API recomienda divisores enteros para evitar píxeles desiguales. [Viewport][R27]

**[inf]** Para la pintura del tablero prefiero bilineal. Escalar 720p a 1080p con nearest produce una ampliación de 1,5×, poco apropiada para una rejilla uniforme.

#### FSR

**[doc]** FSR 1 y FSR 2.2 requieren Forward+ según la guía consultada. FSR 2 añade procesamiento temporal y puede introducir desenfoque o rastros. [Escalado][R11], [Antialiasing][R16]

**[inf]** No cambiaría a Forward+ para obtener FSR en esta HD 620. Primero reduciría la resolución interna con bilineal y mediría el resultado.

### 6. Sombreado estilizado

#### Toon y rim

**[doc]** StandardMaterial3D ofrece difuso toon, especular toon y rim. El difuso toon permite transiciones duras moduladas por rugosidad; el rim integrado responde a las luces y no es simplemente emisión en los bordes. [Materiales][R22]

Propuesta **[inf]**:

- Arquitectura y rocas: materiales sencillos con pintura dominante.
- Personajes: comparar difuso toon con iluminación suave.
- Especular desactivado en superficies que deban parecer mate.
- Rim tenue en protagonistas y objetos seleccionados.
- Evitar un rim intenso en todo el escenario.

**[doc]** Un ShaderMaterial con `light()` permite definir las bandas de iluminación y usar atenuación/sombras. Esa función se evalúa por luz y píxel; no se ejecuta con `vertex_lighting` o sombreado por vértice forzado. [Shaders espaciales][R28]

**[inf]** Un shader propio se justifica cuando el material estándar no logra la dirección aprobada. Conviene crear pocas familias compartidas y conservar las sombras mediante `ATTENUATION`.

#### Contornos

| Técnica | Ventajas | Costos o límites |
|---|---|---|
| Casco invertido | Silueta controlable y utilizable sin búfer de normales | Otra pasada; problemas en juntas y normales duras |
| `next_pass` | Aplica otro material sobre la misma geometría | Vuelve a dibujar el objeto |
| Posproceso por profundidad | Puede detectar siluetas sin normales integradas | Lecturas de pantalla; pierde líneas internas coplanares |
| Posproceso por profundidad y normales | Mayor información de bordes | El búfer integrado de normales requiere Forward+ |

Fundamentos **[doc]**: [Material y `next_pass`][R29], [Lectura de pantalla][R12], [Posprocesado y profundidad][R30].

**[inf]** Usar casco invertido solo en protagonistas y objetos relevantes. `next_pass` es un mecanismo para ejecutar otra pasada; no es por sí solo un algoritmo de contorno ni garantiza un orden inmediato después del material original.

#### Texturas pintadas y flat shading

Propuesta **[inf]**:

- Modelar las formas grandes que afectan a la silueta.
- Reservar normales duras para planos deliberadamente facetados.
- Mantener suavidad en rostro, extremidades y superficies redondeadas.
- Pintar variación de color y pincelada, evitando ruido fotográfico.
- Compartir materiales y atlas donde tenga sentido.
- Empezar con texturas de 512–1024 para recursos comunes; justificar excepciones por tamaño en pantalla.

Flat shading y textura pintada son decisiones independientes: es posible combinar pintura con normales suaves. Los bordes visualmente duros no requieren facetar todos los triángulos. [inf]

#### Hierba

**[doc]** MultiMesh permite dibujar muchas instancias de forma eficiente, pero su descarte de visibilidad es por conjunto. [MultiMesh][R13]

Propuesta **[inf]**:

- Mechones de pocas caras, concentrados junto a caminos y rocas.
- MultiMesh por parcelas.
- Viento en vértices con raíz inmóvil y desplazamiento creciente hacia la punta.
- Fase distinta por instancia.
- Sin sombras en hierba pequeña.
- Reducir densidad a distancia.
- Comparar tarjetas con recorte alfa y mechones opacos.

**[inf]** Un jardín de quads grandes con mucho espacio transparente puede ser más costoso que mechones opacos algo más detallados. Debe evaluarse el área cubierta y el solapamiento, además de los triángulos.

#### Agua

Configuración inicial **[inf]**:

- Una superficie sencilla.
- Color por zonas.
- Movimiento lento de UV.
- Espuma mediante textura o geometría separada.
- Reflejos artísticos o del entorno.
- Sin SSR ni una cámara adicional de reflejo.

**[doc]** En 3D, la textura de pantalla se captura antes de la pasada transparente; no incluye automáticamente otros objetos transparentes. Esto limita ciertas composiciones de agua y refracción. [Lectura de pantalla][R12]

**[inf]** Añadir profundidad de orilla o transparencia únicamente si mejora una escena concreta y conserva el presupuesto.

### 7. Presupuesto inicial de rendimiento

**Todos los números de esta sección son [inf]: objetivos de diseño para probar, no capacidades certificadas de la HD 620.**

#### Presupuesto por encuadre

| Recurso | Perfil 720p, objetivo 30 fps | Perfil 1080p nativo, experimental |
|---|---:|---:|
| Triángulos visibles de la pasada principal | 60 000–100 000 | Empezar con 40 000–70 000 |
| Draw calls 3D visibles | ≤100 | ≤80 inicialmente |
| Draw calls totales, incluyendo sombra y UI | ≤200 | ≤160 inicialmente |
| Luces con sombra | 1 direccional | 0–1 direccional |
| Luces locales visibles | 0–2, sin sombra | 0–2, sin sombra |
| Atlas direccional inicial | 1024² | 1024² |
| Atlas direccional a comparar | 2048² si mejora claramente | 2048² solo con margen |
| Atlas posicional | 0 si no hay sombras omni/spot | Igual |
| MSAA | Desactivado frente a 2× | Desactivado inicialmente |
| Mezcla alfa simultánea | 1–2 capas relevantes por píxel | Mantener o reducir |
| Mechones de hierba visibles | Empezar con 500–1500 | Empezar con 500–1000 |
| Materiales distintos visibles | Intentar ≤20–30 | Mismo objetivo |

**[inf]** Los valores menores para 1080p son un inicio conservador de la prueba, no una relación matemática entre resolución y geometría. La resolución afecta especialmente el trabajo por píxel; las llamadas de dibujo y muchos costos geométricos no disminuyen al bajar a 720p.

**[doc]** Godot permite distinguir estadísticas de pasada visible, sombras y canvas. Las sombras pueden volver a dibujar objetos varias veces. No debe compararse el conteo de geometría única con el total de primitivas procesadas como si fueran lo mismo. [Viewport][R27]

#### Sombras

Configuración propuesta **[inf]**:

- Una direccional.
- Comparar un mapa único con dos divisiones.
- Distancia de sombra limitada al espacio jugable visible.
- Calidad de filtrado baja al principio.
- Sin PCSS.
- Excluir hierba, partículas y detalles pequeños de los proyectores de sombra.
- Probar atlas de 1024 antes de aumentar resolución.

**[doc]** El atlas direccional y el posicional son distintos. Establecer el atlas posicional en cero desactiva sombras omni/spot, no las direccionales. [Viewport][R27]

#### Efectos apagados en la configuración inicial

**[inf]** SDFGI, VoxelGI, SSAO, SSIL, SSR, niebla volumétrica, DOF, glow, TAA, FSR, contornos de pantalla completa y cámaras de reflejo.

Después del benchmark, probar de uno en uno: MSAA 2×, glow tenue y SSAO simplificado de Compatibility. Mantener únicamente mejoras perceptibles en el encuadre real. [inf]

### 8. Novedades de Godot 4.4 a 4.7 relevantes

| Versión | Cambio verificado [doc] | Consecuencia propuesta [inf] |
|---|---|---|
| 4.4 | Ubershaders para reducir pausas de compilación [R31] | Evaluar arranque frío y ejecución caliente por separado |
| 4.4 | Interpolación física 3D [R31] | Utilizarla para estabilizar seguimiento y movimiento |
| 4.4 | Shadowmasks, muestreo bicúbico y mejoras de lightmaps [R31] | Investigar sombras estáticas lejanas y menor densidad de lightmap |
| 4.4 | Fallback de renderizado y máscara de proyectores de sombra [R31] | Registrar el backend real y excluir detalles innecesarios |
| 4.5 | Shader baker para exportaciones [R32] | Considerarlo al preparar builds; no sustituye medir el juego |
| 4.5 | Cambios en interpolación 3D y uso de media precisión en Mobile cuando el hardware lo permite [R32] | No extrapolar ganancias de GPU móviles modernas a la HD 620 |
| 4.6 | SSAO simplificado para Compatibility [R33] | Puede evaluarse sin migrar a Forward+ |
| 4.6 | Cambios de glow y mejoras de precisión/debanding en Mobile [R34] | Revisar color al cambiar de perfil |
| 4.6 | D3D12 por defecto en proyectos nuevos de Windows según la guía de migración [R35] | Fijar la API explícitamente durante la prueba |
| 4.7 | `AreaLight3D`, salida HDR y escalado 3D nearest [R36] | Nearest es evaluable; HDR y luces de área no son requisitos de este proyecto |

**[doc]** AreaLight3D tiene limitaciones por renderizador y un costo superior al de luces omni/spot; en Compatibility no proyecta sombras. [AreaLight3D][R37]

**[inf]** Estas mejoras no convierten automáticamente a Forward+ en la elección adecuada para este portátil. Tampoco una corrección anunciada en otra versión demuestra su efecto sobre 4.7.2 y el controlador instalado.

### 9. Pila principal y plan B

#### Pila principal propuesta

| Componente | Selección [inf] |
|---|---|
| Motor | Godot 4.7.2-stable, versión fijada |
| Renderizador | Compatibility / OpenGL |
| Mundo | 3D por zonas pequeñas |
| Personajes | Chibi 3D con materiales compartidos |
| Sprites | Recorte alfa; sombra independiente cuando proceda |
| Iluminación | Ambiente y una direccional; rellenos muy limitados |
| GI | Sin GI durante iteración; LightmapGI opcional tras validación |
| Sombras | Direccional corta y filtrado económico; blobs donde convenga |
| Cámara | Perspectiva baja en exploración; ortogonal en hub |
| Resolución | 720p 3D, UI a resolución de salida |
| Vegetación | MultiMesh por parcelas y viento simple |
| Posprocesado | Desactivado inicialmente |

#### Plan B: Mobile con D3D12

**[inf]** Mantener geometría, recursos, cámaras y recorrido comparables. Activarlo como candidato si:

- DOF o decals pasan a ser requisitos visuales.
- Reduce tiempos de cuadro en la escena representativa.
- Supera la sesión prolongada sin errores.
- El resultado visual recibe aprobación.

Si D3D12 falla, probar Mobile con Vulkan. Si ambas variantes son peores, conservar Compatibility.

**[inf]** Para un perfil económico adicional: Compatibility sin sombras dinámicas, blobs y menor densidad de vegetación. Reducir a 960×540 únicamente después de revisar legibilidad y calidad visual.

### 10. Prueba de rendimiento y puerta de validación

#### Escenas necesarias

Todas son propuestas **[inf]** y pueden construirse con primitivas y recursos existentes, sin generar activos de IA.

| Escena | Contenido | Qué debe resolver |
|---|---|---|
| A. Base | Suelo, rocas simples, personaje y ambiente | Costo mínimo de cada backend |
| B. Exterior | Sendero, relieve, protagonista, gato, cuatro NPC, hierba y una direccional | Viabilidad del encuadre principal |
| C. Hub | Primer plano, zona jugable y fondo; tiendas y luces locales | Capas, transparencias y encuadre lateral |
| D. Sprites | Sprites cruzándose, pared, escalón y cámara móvil | Recorte alfa, billboard, proxies y ordenación |
| E. Agua y efectos | Agua, partículas y hierba superpuestas | Sensibilidad al costo por píxel |
| F. Personalización | Personaje, cambios de pelo/color, rostro y cuerpo | Costo de materiales y vistas adicionales |
| G. Horneado | Habitación pequeña con UV2 y probes | Éxito, tiempo y memoria de LightmapGI |

En F, comparar dos vistas simultáneas con una sola vista que cambia de encuadre. Si se usan SubViewports, actualizar únicamente los necesarios para la interacción. [inf]

#### Matriz de ejecución

**[inf]** Probar secuencialmente:

1. Compatibility / OpenGL.
2. Mobile / D3D12.
3. Mobile / Vulkan.
4. Forward+ sin efectos avanzados, como referencia.
5. SDFGI o VoxelGI únicamente como diagnóstico opcional si Forward+ resulta estable.

Resoluciones:

- Mundo a 1280×720.
- Mundo a 1920×1080.
- Salida 1080p con mundo 720p y UI nativa.

No ejecutar toda la matriz con todos los efectos combinados. Primero comparar backends con iluminación equivalente; después añadir una función cada vez. [inf]

#### Condiciones reproducibles

Propuesta **[inf]**:

- Equipo conectado a corriente y mismo modo de energía.
- Mismo recorrido automatizado, semilla y encuadre.
- Sin captura de video durante la medición principal.
- Registrar aplicaciones abiertas.
- Separar primer arranque y arranques posteriores.
- Calentar 60 segundos; medir 180 segundos.
- Tres repeticiones por candidato.
- Repetir el candidato ganador tras 20 minutos.
- Usar una exportación de producción cuando existan las plantillas; medir también editor más juego.

**[doc]** El Visual Profiler permite observar tiempos de CPU/GPU relacionados con renderizado; el Profiler convencional cubre scripts y físicas. Los monitores permiten seguir FPS, memoria y otras estadísticas. [Depurador][R38]

#### Métricas

Registrar **[inf]**:

- Tiempo de cuadro mediano, p95 y p99.
- Número de cuadros superiores a 50 y 100 ms.
- Tiempo de CPU y GPU cuando la medición esté disponible.
- Draw calls visibles, de sombra y de UI.
- Primitivas procesadas.
- Memoria del proceso, memoria disponible del sistema y memoria gráfica compartida.
- Tiempo de carga y primer cuadro controlable.
- Errores gráficos, cierres, pérdidas del dispositivo y fallback.
- Resultado visual: estabilidad de sprites, sombras, hierba y legibilidad.

#### Umbrales de aceptación

**Son criterios propuestos [inf], pendientes de aprobación visual y medición.**

| Puerta | Umbral |
|---|---|
| Escenario representativo a 720p, sin límite de FPS | Mediana ≤28 ms; p95 ≤33,3 ms; p99 ≤50 ms |
| Cuadros muy largos | Ninguno >100 ms durante el recorrido caliente sin cargas |
| Juego limitado a 30 fps | Sin caídas sostenidas por debajo de 30 fps |
| Sesión de 20 minutos | Sin cierres, errores gráficos persistentes ni degradación sostenida >10% |
| Memoria | Mantener aproximadamente 1,5 GB disponibles durante editor más juego, sin pausas frecuentes de paginación |
| Horneado de prueba | Completar correctamente y poder reproducirlo en Compatibility |
| Iteración de luz | Horneado preliminar pequeño ≤5 minutos como objetivo |
| Horneado final de una zona pequeña | ≤20 minutos como límite de comodidad inicial |
| Perfil 1080p | Superar sus propios umbrales; no heredar la aprobación de 720p |
| Perfil 60 fps opcional | p95 ≤16,7 ms en escenas representativas |

**[inf]** Si el horneado excede esos tiempos, reducir densidad y calidad una vez y volver a medir. Si sigue siendo impráctico, aprobar iluminación sin GI para la primera zona.

#### Regla final de selección

**[inf]** Elegir la combinación que supere estabilidad, rendimiento y revisión visual. Para abandonar Compatibility, Mobile debe aportar una función necesaria o una mejora medible relevante; una diferencia pequeña dentro de la variación entre repeticiones no basta.

La puerta de Fase 0 quedará cerrada con:

- Configuración exacta del perfil aprobado.
- Tabla de resultados de las repeticiones.
- Capturas comparables.
- Incidencias pendientes.
- Aprobación del usuario sobre el exterior, el hub y los personajes.

**Estado actual: investigación terminada; rendimiento local y horneado sin verificar.**

## Fuentes

Todas las fuentes utilizadas son primarias. **[doc]** identifica documentación oficial y registros primarios de incidencias; estos últimos se han tratado como reportes, no como garantías. **[inf]** identifica recomendaciones y deducciones de este informe. No fue necesario fundamentar decisiones en fuentes **[sec]**.

- **Renderizadores y hardware:** [R1 — Comparación de renderizadores][R1]; [R2 — APIs de Intel][R2]; [R18 — Requisitos de Godot][R18]; [R20 — Soporte heredado de Intel][R20].
- **Incidencias:** [R3 — Ventana vacía con Vulkan][R3]; [R4 — SDFGI en Intel Windows][R4]; [R8 — SDFGI y cámara ortogonal][R8]; [R19 — Entorno HD 620/D3D12 reportado en 2026][R19].
- **Iluminación y materiales:** [R5 — LightmapperRD][R5]; [R6 — LightmapGI][R6]; [R7 — SDFGI][R7]; [R21 — VoxelGI][R21]; [R17 — Luces y sombras][R17]; [R22 — Materiales 3D][R22]; [R28 — Shaders espaciales][R28]; [R37 — AreaLight3D][R37].
- **Sprites, cámaras y pantalla:** [R9 — SpriteBase3D][R9]; [R23 — GeometryInstance3D][R23]; [R24 — Camera3D][R24]; [R10 — CameraAttributesPractical][R10]; [R11 — Escalado 3D][R11]; [R16 — Antialiasing][R16]; [R26 — Múltiples resoluciones][R26]; [R27 — Viewport][R27]; [R25 — Interpolación][R25].
- **Rendimiento y contornos:** [R13 — MultiMesh][R13]; [R14 — Optimización GPU][R14]; [R15 — Optimización 3D][R15]; [R12 — Lectura de pantalla][R12]; [R29 — Material y next_pass][R29]; [R30 — Posprocesado][R30]; [R38 — Profiler y monitores][R38].
- **Versiones:** [R31 — Godot 4.4][R31]; [R32 — Godot 4.5][R32]; [R33 — SSAO de Compatibility][R33]; [R34 — Godot 4.6][R34]; [R35 — Migración a 4.6][R35]; [R36 — Godot 4.7][R36].

[R1]: https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html
[R2]: https://www.intel.com/content/www/us/en/support/articles/000005524/graphics.html
[R3]: https://github.com/godotengine/godot/issues/69046
[R4]: https://github.com/godotengine/godot/issues/86833
[R5]: https://docs.godotengine.org/en/4.7/classes/class_lightmapperrd.html
[R6]: https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html
[R7]: https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_sdfgi.html
[R8]: https://github.com/godotengine/godot/issues/60522
[R9]: https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html
[R10]: https://docs.godotengine.org/en/4.7/classes/class_cameraattributespractical.html
[R11]: https://docs.godotengine.org/en/4.7/tutorials/3d/resolution_scaling.html
[R12]: https://docs.godotengine.org/en/4.7/tutorials/shaders/screen-reading_shaders.html
[R13]: https://docs.godotengine.org/en/4.7/tutorials/performance/using_multimesh.html
[R14]: https://docs.godotengine.org/en/4.7/tutorials/performance/gpu_optimization.html
[R15]: https://docs.godotengine.org/en/4.7/tutorials/performance/optimizing_3d_performance.html
[R16]: https://docs.godotengine.org/en/4.7/tutorials/3d/3d_antialiasing.html
[R17]: https://docs.godotengine.org/en/4.7/tutorials/3d/lights_and_shadows.html
[R18]: https://docs.godotengine.org/en/4.7/about/system_requirements.html
[R19]: https://github.com/godotengine/godot/issues/122029
[R20]: https://www.intel.com/content/www/us/en/download/776137/intel-7th-10th-gen-processor-graphics-windows.html
[R21]: https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_voxel_gi.html
[R22]: https://docs.godotengine.org/en/4.7/tutorials/3d/standard_material_3d.html
[R23]: https://docs.godotengine.org/en/4.7/classes/class_geometryinstance3d.html
[R24]: https://docs.godotengine.org/en/4.7/classes/class_camera3d.html
[R25]: https://docs.godotengine.org/en/4.7/tutorials/physics/interpolation/advanced_physics_interpolation.html
[R26]: https://docs.godotengine.org/en/4.7/tutorials/rendering/multiple_resolutions.html
[R27]: https://docs.godotengine.org/en/4.7/classes/class_viewport.html
[R28]: https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html
[R29]: https://docs.godotengine.org/en/4.7/classes/class_material.html
[R30]: https://docs.godotengine.org/en/4.7/tutorials/shaders/advanced_postprocessing.html
[R31]: https://godotengine.org/releases/4.4/
[R32]: https://godotengine.org/releases/4.5/
[R33]: https://docs.godotengine.org/en/4.7/tutorials/3d/environment_and_post_processing.html
[R34]: https://godotengine.org/releases/4.6/
[R35]: https://docs.godotengine.org/en/4.7/tutorials/migrating/upgrading_to_godot_4.6.html
[R36]: https://godotengine.org/releases/4.7/
[R37]: https://docs.godotengine.org/en/4.7/classes/class_arealight3d.html
[R38]: https://docs.godotengine.org/en/4.7/tutorials/scripting/debug/debugger_panel.html