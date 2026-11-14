# Auditoría del trabajo previo — Proyecto NASA-Ecuador
## Resumen ejecutivo

El trabajo anterior, llamado **Gravedad 2D-HD**, aporta una base narrativa aprovechable, conceptos visuales, un kit modular de habitación y un núcleo de diseño de misiones.

El hallazgo principal es que **existen dos estados distintos**: el último commit contiene una habitación 2D; la copia de trabajo incorpora un prólogo con escenario 3D, creador de avatar, guardado e integración con la consola. Esta ampliación todavía no está versionada y el README describe principalmente el estado anterior.

Conviene conservar la historia, los datos estructurados y la lógica educativa; reconstruir la presentación visual para el nuevo objetivo. Los muebles actuales son imágenes planas y el protagonista sigue siendo un sprite, aunque estén colocados en un mundo 3D.

La inspección fue de solo lectura. No ejecuté Godot, instalaciones, subidas ni generaciones. Los resultados de ejecución citados proceden de registros anteriores.

**Limitación:** `Nasa_Game/` no existe en esta bóveda. El contraste con el plan actual se basa en el brief proporcionado; sus PDF, tablero y matrices de costos quedan **sin verificar**.

## Decisiones recomendadas

Las recomendaciones son **[inf]**, sustentadas en las evidencias numeradas y el desarrollo posterior.

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Punto de partida | Conservar el repositorio y separar claramente versión confirmada, ampliación local y documentación desactualizada. | Reiniciar todo: perdería mecánicas, recursos y trazabilidad útiles. | alta |
| Historia | Mantener Guayaquil → formación → misión → transmisión del conocimiento. Revisar los nombres secundarios como propuestas. | Considerar aprobado todo el dossier: declara expresamente elementos pendientes de revisión. | alta |
| Protagonista | Conservar las opciones y el esquema de personalización; rehacer su representación para un chibi 3D. | Convertir el sprite procedural actual en arte final: no alcanza el objetivo visual. | alta |
| Gato científico | Adoptar el gato del brief actual. Conservar «Órbita» como nombre provisional. | Mantener abierta la elección gato/perro: corresponde a una decisión anterior ya superada. | alta |
| Habitación | Reutilizar Atardecer como guía de luz, materiales y composición; reconstruir volumen, escala y cámara. | Tratar el kit PNG como escenario 3D terminado: tiene perspectiva e iluminación dibujadas. | alta |
| Renderizado | Conservar Compatibility como referencia funcional en este equipo. Evaluar cualquier cambio mediante una escena pequeña y mediciones. | Imponer Forward+ y SDFGI por el estilo: el proyecto no acredita su rendimiento en la HD 620. | alta |
| Arquitectura | Mantener nodos, señales y `Resource`; reducir gradualmente la duplicación entre las dos implementaciones. | Migrar ahora a ECS: la inspección no revela una necesidad que justifique esa reconstrucción. | alta |
| Pipeline | Conservar originales, registro de procedencia y separación Arte/Godot; completar costos, licencias y aprobaciones por recurso. | Generar más variantes antes de cerrar cámara y escala: repetiría el problema anterior. | alta |
| Versionado y validación | Preservar primero los cambios locales y actualizar documentación y evidencias cuando se autoricen escrituras. Después, configurar LFS y automatización. | Dar por reproducible el proyecto actual desde Git: faltan archivos esenciales en los commits. | alta |

## Afirmaciones que sostienen las decisiones

1. **[doc] El proyecto local arranca en `res://scenes/main.tscn`, a 1280×720 y con `gl_compatibility`.** El README conserva la descripción de 384×216. Fuentes: [configuración actual][L4], [README][L5].

2. **[doc] El último commit cambia de alcance respecto de la copia de trabajo.** `e748501` contiene la habitación 2D; `scenes/`, `scripts/`, `assets/`, `tests/`, `tools/` y el dossier aparecen sin seguimiento en el estado Git inspeccionado. Fuente histórica: [commit e748501](https://github.com/Guivve-A/Juego_Godot_repo1_agentes/commit/e748501fb0af4b5768c9a54cb1f720f42f17f3f5); diferencias locales observadas mediante `git status` y `git diff`.

3. **[doc] El escenario nuevo combina arquitectura 3D con imágenes planas.** `bedroom.gd` genera geometría; `prop.gd` coloca muebles como `Sprite3D`; `avatar.gd` dibuja el personaje en una imagen de 40×56 píxeles. Fuentes: [habitación][L7], [props][L8], [avatar][L9].

4. **[doc] Los muebles tienen `shaded = false` y proyección de sombras desactivada.** El avatar también utiliza `shaded = false`. Por tanto, esta implementación no demuestra recepción de iluminación 3D sobre esos sprites. La documentación relaciona `shaded` con la influencia de `Light3D`. Fuentes: [props][L8], [avatar][L9], [SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html).

5. **[doc] Existe evidencia histórica de ejecución con la HD 620 mediante ANGLE.** `flow-rendered.log` registra Compatibility y 33 comprobaciones aprobadas. No contiene mediciones de FPS ni certifica el código actual completo. Fuente: [registro de ejecución][L10].

6. **[doc] La simulación ya separa lógica y datos.** Hay cinco clases `Resource`, catálogos `.tres`, funciones orbitales y un evaluador de misión. Fuentes: [datos][L11], [núcleo][L12].

7. **[doc] El kit tiene doce PNG RGBA y procedencia registrada, pero sus doce filas mantienen `verified=false` y condiciones de publicación pendientes.** Las copias dentro de Godot coinciden por SHA-256 con los originales. Fuente: [registro de recursos][L13].

8. **[doc] La personalización, el cuarto cálido, el libro holográfico y las proporciones de Atardecer están documentados como decisiones del usuario.** El catálogo final del avatar permanece abierto. Fuentes: [índice][L1], [avatar][L14], [primera escena][L15].

9. **[doc] El gato no estaba cerrado en el trabajo anterior.** La ficha proponía gato o perro; el dossier usa «Órbita» como apodo provisional. Fuente: [mascota científica][L16]. La elección de gato procede del brief actual.

10. **[doc] La revisión del 2026-11-09 cuestionó escala, resolución de recursos, condiciones del evento y derechos.** Después se registró la decisión de continuar y elegir Space Mission Design Game. Fuentes: [revisión][L3], [bitácora][L2]. Sus afirmaciones sobre reglas del evento no se ratifican aquí.

11. **[doc] Compatibility admite renderizado 3D y lightmaps ya horneados; SDFGI corresponde a Forward+.** El horneado de LightmapGI requiere hardware con soporte de RenderingDevice. Fuente: [renderizadores de Godot 4.7](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

12. **[inf] Conviene conservar Compatibility como base de comparación y no comprometer todavía el proyecto con SDFGI ni con horneado local.** La recomendación combina la ejecución histórica disponible, la ausencia de pruebas con otros renderizadores y el costo de preparación de LightmapGI, que utiliza GPU y UV2. Fuentes: [registro local][L10], [LightmapGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html).

## Riesgos y cómo mitigarlos

| Riesgo | Evidencia o implicación | Mitigación recomendada [inf] |
|---|---|---|
| Pérdida de la ampliación local | El proyecto configurado depende de archivos sin seguimiento. | Revisar y preservar ese conjunto antes de reorganizar o migrar. |
| Documentación contradictoria | Conviven 28 px, 36 px, un sprite de 56 px y dos resoluciones de interfaz. | Establecer una ficha vigente de cámara, escala, resolución y representación del personaje. |
| Confundir concepto con resultado jugable | La portada utiliza Atardecer; la habitación ejecutada tiene un acabado bastante más provisional. | Validar capturas del recorrido real y etiquetar las ilustraciones como concepto. |
| Falsa confianza en las pruebas | Los registros muestran 33 comprobaciones; el test actual incorpora dos adicionales. | Repetir la validación tras fijar una versión reproducible y registrar commit, configuración y resultados. |
| Cambiar de renderizador sin presupuesto técnico | Solo hay evidencia local de Compatibility/ANGLE. | Comparar una escena representativa; medir tiempo de cuadro, memoria y estabilidad antes de decidir. |
| Publicación con procedencia incompleta | El registro del kit mantiene condiciones por verificar; falta registro equivalente de varios recursos nuevos. | Completar procedencia, modelo, costo, licencia y aprobación por recurso. |
| Presentar simplificaciones como ciencia calculada | Vida útil, enlace y ciertos resultados dependen de tablas y multiplicadores de juego. | Identificar qué se calcula, qué se aproxima y qué constituye una regla de diseño. |
| Consumir los 1000 créditos repitiendo exploraciones | La bóveda registra generaciones, pero no sus costos. | Incorporar el costo real y una puerta de validación antes de cada nueva producción. |

## Preguntas que debe decidir el usuario

1. **Nombre:** ¿«Gravedad» se conserva como título o queda como nombre del prototipo anterior?
2. **Alcance inicial:** ¿la primera validación visual será la habitación o un pequeño exterior con la cámara alta del nuevo tablero?
3. **Narrativa:** ¿se mantienen los tres actos y el reparto propuesto, o se concentra primero la historia en estudiante, gato y mentora?
4. **Interfaz:** ¿el pergamino se aplica a exploración y diario, reservando una terminal científica para la consola?
5. **Destino:** ¿la presentación a Space Apps sigue condicionando el producto o queda separada del desarrollo por ocho fases?

El gato y la necesidad de funcionar en el equipo indicado ya están fijados por el brief; no requieren reabrirse.

## Desarrollo

### 1. Alcance y criterio de la auditoría

Se leyeron los documentos solicitados, las escenas y scripts del proyecto, recursos de datos, utilidades locales y evidencias guardadas. Se inspeccionaron visualmente los conceptos, las láminas del kit, los storyboards y las capturas del prototipo.

También se examinó el PDF interno **Arte e Historia**, de 14 páginas, junto con su fuente Markdown. No es el PDF del plan maestro actual. [doc: dossier][L17]

Las etiquetas se interpretan así:

- **[doc]:** documentación primaria, código, archivo o registro inspeccionado.
- **[sec]:** fuente secundaria. No fue necesaria para sostener este informe.
- **[inf]:** interpretación o recomendación derivada de las evidencias.

Una prueba documentada anteriormente se informa como evidencia histórica. **No se ejecutaron pruebas nuevas ni se abrió el editor.**

No se encontraron `AGENTS.md` ni una carpeta `Nasa_Game/` dentro de la bóveda. Por ello no se verificaron directamente las ocho fases, sus puertas, las 14 capturas nuevas ni los archivos `hf_costos_*` y `hf_modelos.json`.

### 2. Decisiones anteriores y su grado de aprobación

#### Historia y protagonista

La premisa está bastante consolidada: un avatar personalizable estudia ingeniería en Guayaquil, descubre un libro científico y aplica posteriormente lo aprendido en una misión espacial.

El arco propuesto comprende:

| Acto | Contenido | Estado anterior |
|---|---|---|
| I — Guayaquil | Cuarto, familia, Malecón, universidad, pruebas, graduación y aceptación de una práctica. | Cuarto implementado; resto principalmente storyboard. |
| II — Una señal débil | Entrenamiento, diseño de misión, pérdida del enlace y diagnóstico. | Consola y escenarios implementados; dramatización pendiente. |
| III — Una pregunta compartida | Biblioteca, vuelo con inercia, planetario, Apolo y entrega del cuaderno. | Diseño narrativo y visual. |

El protagonista no tiene género ni apariencia fija. «Alex» es el nombre predeterminado del código, no un personaje narrativo aprobado. La especialidad **ingeniería de control** queda más definida en el brief actual que en las notas antiguas. [doc: historia][L18], [controlador del prólogo][L6]

Elena, Rafael, Lidia Vera, Sam Rivas, Dra. Vega y Ari forman el reparto propuesto. Los nombres y diálogos siguen sujetos a revisión. La idea educativa más consistente es **observar, cambiar un parámetro, comprobar y volver a intentar**. [doc: historia][L18]

#### Gato científico

La documentación antigua dejó abierta la especie. Propuso bata clara `#F8F9FA`, acento cian `#00E5FF`, puntero y funciones de guía del planetario.

«Órbita» aparece como nombre de trabajo. Existen siluetas esquemáticas de gato y perro, pero no un personaje final, modelo, rig ni animaciones integradas. El brief actual resuelve la especie a favor del gato. [doc: mascota][L16], [dossier][L17]

#### Dirección de arte

Las decisiones documentadas fueron:

- Personajes chibi con píxeles visibles.
- Materiales reconocibles: madera, textiles, piedra, yeso y vegetación tropical.
- Luz cálida y sombras frías.
- Composición en primer plano, recorrido nítido y fondo.
- Espacio con planetas realistas, manteniendo personajes e interfaz definidos.
- Atardecer como referencia elegida de proporciones para la habitación.

La referencia principal anterior era **Village Square, Emberfall**, cuya procedencia seguía sin verificar. La atribución del tablero nuevo no debe transferirse automáticamente a esta captura distinta. [doc: dirección artística][L19], [referencia anterior][L20]

#### Paleta y tipografía

La paleta del dossier es una **paleta de prueba**, no una aprobación final:

| Uso | Color documentado |
|---|---|
| Luz ámbar | `#E39D58` |
| Sombra índigo | `#28294C` |
| Madera | `#895545` |
| Vegetación | `#52694F` |
| Holograma | `#00E5FF` |
| Papel | `#F8F0DF` |

La consola utiliza azul noche `#0F1228` y cian `#00E5FF`; el prólogo añade dorado `#D6B477`, papel `#EEE8D9` y tinta `#101926`. Son sistemas parcialmente distintos. [doc: dossier][L17], [consola][L21], [prólogo][L6]

**DotGothic16 fue una intención de diseño, pero no está instalada en los recursos del proyecto.** La consola intenta cargarla y utiliza la fuente predeterminada si falta. El prólogo usa Cinzel y Atkinson, con archivos de licencia OFL incluidos en `assets/fonts/`. [doc: consola][L21], [recursos del proyecto][L22]

#### Motor y organización

Godot 4.7.2 está documentado en el README y en los registros de ejecución. `project.godot` declara características de la familia 4.7 y Compatibility.

La bóveda distribuyó responsabilidades entre reglas, código, arte y guion. La carpeta `raw/` se reservó para originales de solo lectura, pero actualmente está vacía. La sincronización copia arte hacia Godot sin modificar los originales. [doc: índice][L1], [sincronización][L23]

### 3. Inventario de recursos existentes

Las rutas siguientes son relativas a la raíz auditada. Los estados describen existencia e integración observadas; las valoraciones de reutilización son **[inf]**.

#### Documentación y narrativa

| Ruta | Contenido y estado |
|---|---|
| `0_Reglas_Globales/index.md` | Índice, decisiones y reglas de coordinación. Versionado; parcialmente desactualizado respecto al prólogo. |
| `0_Reglas_Globales/log.md` | Bitácora del 8 y 9 de noviembre. Versionada; no registra toda la ampliación local posterior. |
| `0_Reglas_Globales/validacion-claude-2026-11-09.md` | Revisión técnica y del evento. Versionada, con modificaciones locales. |
| `1_Mecanicas_y_Codigo/README.md` | Arquitectura, ejecución, pruebas y pendientes de la implementación anterior. |
| `1_Mecanicas_y_Codigo/solicitudes-arte.md` | Contrato y pedidos de arte; varias solicitudes siguen pendientes. |
| `2_Arte_e_Interfaz/arte e Historia.md` | Biblia visual v0.1, reparto, 18 viñetas y matriz de producción. Sin seguimiento Git. |
| `2_Arte_e_Interfaz/arte e Historia.pdf` | Presentación del dossier en 14 páginas. Sin seguimiento Git. |
| `2_Arte_e_Interfaz/{avatar,direccion-artistica,mascota-cientifica,primera-escena}.md` | Fichas de diseño, procedencia y decisiones. Versionadas. |
| `3_Guion_y_Mundo/historia.md` | Fuente narrativa declarada, ligada a los tres escenarios de misión. |
| `3_Guion_y_Mundo/guion-video-30s.md` | Guion de presentación centrado en habitación y simulación. No es un video terminado. |

Fuentes documentales: [reglas][L1], [código][L5], [dossier][L17], [historia][L18].

#### Conceptos PNG

Todos están en `2_Arte_e_Interfaz/`.

| Archivo | Descripción visual y estado |
|---|---|
| `avatar-concepto-01.png` — 1024×688 | Tres combinaciones de estudiante, cabello, ojos y accesorios sobre fondo oscuro. Referencia de apariencia; no contiene capas listas para animación. |
| `habitacion-concepto-01.png` — 1344×752 | Cuarto amplio, ventana tropical, cama y escritorio científico. El protagonista tiene mayor presencia en el encuadre. Concepto inicial. |
| `habitacion-02-atardecer.png` — 1344×752 | Madera cálida, sol diagonal, mobiliario al fondo y objetos desenfocados delante. Variante elegida como dirección de proporciones. |
| `habitacion-02-atardecer-escala.png` — 1344×752 | Avatar junto al escritorio para comparar alturas. Es también el fondo utilizado por la portada del prototipo. |
| `habitacion-03-hora-azul.png` — 1344×752 | Sombras violetas, lámpara ámbar y ciudad al anochecer. Variante alternativa. |
| `habitacion-03-hora-azul-escala.png` — 1344×752 | Revisión con avatar junto al escritorio; permite evaluar mobiliario y libro. |

Las dos versiones de escala sirven para comparar proporciones, pero no constituyen mediciones del mundo jugable. [doc: avatar][L14], [primera escena][L15]

#### Kit de habitación

Raíz: `2_Arte_e_Interfaz/kit-habitacion/`.

| Ruta | Contenido y estado |
|---|---|
| `fuentes/muebles.png` | Lámina 1024×1024: escritorio, silla, cama y estantería. |
| `fuentes/estructura.png` | Lámina 1024×1024: puerta, ventana, mesita y planta. |
| `fuentes/interaccion.png` | Lámina 1024×1024: libro cerrado, abierto, holograma y avatar. |
| `vista-previa.png` | Catálogo rotulado de doce piezas, 1280×990. |
| `piezas/` | Doce recortes RGBA independientes. |
| `README.md` | Guía de colocación, importación y anclajes. |
| `asset-register.csv` | Procedencia por pieza; verificación de publicación pendiente. |

Las doce piezas existentes son:

| Archivo en `piezas/` | Dimensiones |
|---|---:|
| `avatar-muestra.png` | 159×405 |
| `cama.png` | 396×344 |
| `escritorio.png` | 378×272 |
| `estanteria.png` | 272×395 |
| `holograma.png` | 308×273 |
| `libro-abierto.png` | 372×231 |
| `libro-cerrado.png` | 331×244 |
| `mesita.png` | 245×251 |
| `planta.png` | 261×307 |
| `puerta.png` | 195×399 |
| `silla.png` | 201×310 |
| `ventana.png` | 390×345 |

El conjunto tiene coherencia cromática y material. Su volumen aparente, iluminación y orientación están incorporados al dibujo. Las doce copias en `godot/arte/kit-habitacion/` son idénticas a estos originales. [doc: kit][L24], [registro][L13]; interpretación visual **[inf]**.

#### Referencias y storyboard

| Ruta bajo `2_Arte_e_Interfaz/` | Contenido y estado |
|---|---|
| `referencias/village-square-emberfall.png` | Aldea oblicua, personajes pixelados, iluminación cálida, vegetación y diálogo ornamental. Material de estudio; procedencia pendiente. |
| `referencias/referencia-principal.md` | Análisis por capas y comparables. |
| `storyboard/01-orbita-y-cuarto.png` | Viñetas 01–03: creador, tránsito espacial y recorrido al escritorio. |
| `storyboard/02-libro-y-guayaquil.png` | 04–06: libro, familia y paseo junto al río. |
| `storyboard/03-formacion.png` | 07–09: universidad, pruebas y graduación/carta. |
| `storyboard/04-control-de-mision.png` | 10–12: despliegue, enlace débil y recuperación. |
| `storyboard/05-biblioteca-y-minijuegos.png` | 13–15: biblioteca, vuelo con inercia y planetario. |
| `storyboard/06-apolo-y-cierre.png` | 16–18: archivo Apolo, cuaderno y cierre. |
| `storyboard/modelos-esquematicos.png` | Gato, perro y astronauta de frente/perfil. |

Los siete PNG de storyboard miden 1190×205. Son esquemas geométricos de composición, con flechas y rótulos; **no son arte final ni animaciones**. La carpeta completa carece de seguimiento Git. [doc: dossier][L17], [referencia][L20]

#### Recursos y evidencias dentro de Godot

| Ruta bajo `1_Mecanicas_y_Codigo/godot/` | Estado |
|---|---|
| `arte/kit-habitacion/` | Doce imágenes copiadas y archivos `.import`, versionados. |
| `assets/fonts/` | Cinzel, Atkinson y sus licencias; sin seguimiento Git. |
| `assets/ui/atardecer.png` | Copia idéntica de Atardecer con escala. |
| `assets/ui/{atmosphere,orbit}.gdshader` | Atmósfera de portada e introducción orbital procedural. |
| `assets/ui/gravedad_theme.tres` | Tema visual de interfaz. |
| `assets/avatar/layers.png` y `draw_layers.py` | Atlas y generador auxiliar. No encontré referencias al atlas desde los scripts GDScript actuales. |
| `evidence/{title,customizer,intro,room,book,mission,complete}.png` | Siete capturas a 1280×720. |
| `evidence/*.log`, `prologue-results.json`, `mcp-*.json` | Evidencias de ejecución, pruebas y operaciones MCP anteriores. |
| `../capturas/verificacion-2026-11-09.png` | Montaje de la habitación 2D, consola y simulación lunar; versionado. |

No se encontraron modelos `.glb`, `.gltf`, `.fbx`, `.obj` o `.blend`, ni archivos de música/audio `.wav`, `.ogg` o `.mp3` en el proyecto inspeccionado. El prólogo genera sonidos breves de interfaz mediante código. [doc: recursos][L22], [prólogo][L6]

#### `.tools`, complementos y originales

| Ruta | Estado y utilidad |
|---|---|
| `.tools/godot-mcp/` | Servidor MCP externo, paquete local 0.1.1, licencia MIT; contiene fuente, compilación y dependencias Node. |
| `.tools/mcp-client.mjs` | Cliente de integración con rutas locales al ejecutable; además escribe evidencias cuando se ejecuta. No se ejecutó. |
| `.tools/pdf-review/storyboard.png` | Captura de una página del dossier para revisión visual. |
| `raw/` | Vacía. |
| `godot/addons/` | No existe; no se encontraron complementos de editor configurados en `project.godot`. |

El servidor de `.tools` es una utilidad externa al juego. La regla local actual lo excluye de Git. [doc: paquete MCP][L25], [configuración][L4], [exclusiones][L26]

### 4. Estado real del proyecto de Godot

#### Dos implementaciones coexistentes

| Aspecto | Último commit | Copia de trabajo actual |
|---|---|---|
| Entrada | `escenas/habitacion/habitacion.tscn` | `scenes/main.tscn` |
| Mundo | `Node2D`, `CharacterBody2D`, sprites y orden por Y | `Node3D`, `CharacterBody3D`, arquitectura y sprites 3D |
| Resolución configurada | 384×216, escalado entero | 1280×720, `canvas_items`, sin ajuste entero explícito |
| Personaje | Imagen estática del kit | Avatar procedural personalizable |
| Inicio | Habitación directa | Portada, creador, intro y habitación |
| Persistencia | Sin guardado de recorrido documentado | Identidad y apertura del libro en JSON |
| Renderizador | Compatibility | Compatibility |

Esta diferencia está comprobada en `git diff`; el README no basta para describir el estado actual. [doc: configuración][L4], [README][L5]

#### Escenas, scripts y responsabilidades

| Grupo | Implementación |
|---|---|
| `scenes/main.tscn` + `scripts/main.gd` | Portada, creador, intro, panel del libro, misión, pausa, opciones, créditos y fin del prólogo. |
| `scenes/bedroom.tscn` + `scripts/bedroom.gd` | Cámara, entorno, luces, arquitectura procedural, proximidad al libro y salida. |
| `scenes/player.tscn` + `scripts/player.gd` | Movimiento relativo a cámara, carrera, gravedad y colisiones. |
| `scripts/avatar.gd` | Dibujo del avatar, colores, peinados, accesorios y poses simples. |
| `scenes/props/*.tscn` + `scripts/prop.gd` | Nueve escenas de muebles/interactivos con representación plana y huella de colisión opcional. |
| `escenas/habitacion/`, `jugador/`, `interactivos/` | Implementación 2D anterior, todavía presente. |
| `escenas/mision/` | Consola y representación animada de la misión; reutilizadas por el prólogo. |
| `nucleo/` | Catálogo, escala antigua, entradas, mecánica orbital y evaluador. |
| `datos/` | Cinco clases `Resource`, cuatro cuerpos, tres escenarios, tres lanzadores y once componentes. |
| `pruebas/`, `tests/` | Pruebas orbitales y de recorrido/interfaz. |
| `tools/` | Utilidades para guardar arquitectura y regenerar tema. |

Fuentes: [prólogo][L6], [habitación][L7], [núcleo][L12], [datos][L11], [consola][L21].

La cámara actual es ortográfica, con `size=7.2`. Según su posición y el punto utilizado por `look_at`, mira aproximadamente **16° por encima de la horizontal**. Ese cálculo es **[inf]** y explicita la convención angular; no corresponde a una vista claramente alta como la descrita en el nuevo brief. El mundo se presenta mediante un contenedor con `stretch_shrink=2`. [doc: escena][L27], [habitación][L7], [prólogo][L6]

#### Qué está respaldado como funcional

Los registros históricos muestran:

- Inicio y navegación al creador.
- Cambio de apariencia y nombre con caracteres españoles.
- Intro saltable y transición automática.
- Movimiento, suelo y bloqueo por escritorio.
- Pausa y reanudación.
- Proximidad al libro, apertura y holograma separado.
- Acceso a la consola y regreso.
- Salida por la puerta.
- Persistencia de identidad y libro tras recargar la escena.

El registro gráfico informa **33 comprobaciones sin fallos**. El test actual añade comprobaciones de encaje de instrumentos y restauración del aviso del libro que no aparecen en ese registro. Por tanto, **la ejecución histórica no acredita exactamente todos los archivos actuales**. [doc: registro][L10], [test][L28]

El README informa otras **23 pruebas aprobadas** de física y balance, y ejecuciones de 180 y 720 cuadros. Son resultados documentados anteriormente, no repetidos en esta auditoría. [doc: README][L5]

No quedan acreditados rendimiento sostenido, exportaciones actuales, funcionamiento web, audio musical ni una campaña completa. Tampoco existe `export_presets.cfg` en el proyecto inspeccionado.

#### Arquitectura y alcance científico

La arquitectura ya sigue el modelo de Godot: nodos para comportamiento y representación, señales para comunicación y `Resource` para datos. `Componente` significa componente de una nave; **no implica que exista un ECS**. [doc: datos][L11], [núcleo][L12]

El código implementa cálculos orbitales y de propelente, pero también reglas simplificadas:

| Elemento | Tratamiento observado |
|---|---|
| Velocidades y transferencias | Funciones matemáticas de mecánica orbital. |
| Propelente | Cálculo a partir de masa seca, Δv e impulso específico. |
| Energía en Marte | Factor por distancia al Sol. |
| Vida útil | Mínimo entre vida del bus y límite tabulado de la órbita. |
| Enlace | Capacidad tabulada por destino y comparación con datos generados. |
| Radiación | Condición binaria del bus para espacio profundo. |
| Resultado científico | Multiplicadores y umbrales de juego. |

La estructura es reutilizable. La presentación educativa debe explicar sus aproximaciones. La nueva integración ya añade un rótulo general que distingue costos/componentes simulados de constantes NASA/JPL; eso resuelve parcialmente un pendiente del README. [doc: evaluador][L29], [prólogo][L6]

### 5. Qué validó o criticó la revisión del 2026-11-09

La revisión tuvo dos planos: adecuación al evento y preparación técnica. **No fue una aprobación global del juego ni del acabado visual.** [doc: revisión][L3]

| Tema | Conclusión registrada entonces |
|---|---|
| Categoría | Cuestionó asumir una categoría independiente de videojuegos; pidió responder a un reto. |
| Reto | Consideró compatible Space Mission Design Game, con necesidad de construir su bucle de diseño y simulación. |
| Evaluación | Corrigió los criterios del plan anterior por Influence, Creativity, Validity, Relevance y Presentation. |
| Evento local | Registró requisitos de equipo, presencialidad, datos y video. |
| Calendario | Advirtió sobre trabajo anterior al inicio y recomendó una pausa. |
| Derechos | Señaló música de referencia, material de archivo, insignias, atribución y condiciones de IA pendientes. |
| Infraestructura | Aclaró que Claude podía trabajar directamente en la carpeta; no necesitaba un MCP de archivos. |
| Escala | Detectó incompatibilidad entre dimensiones del cuarto, avatar y encuadre. |
| Recursos | Criticó tamaños y cuadrículas de píxel inconsistentes. |
| Integración | Propuso copiar recursos hacia Godot para mantener intacta la carpeta de Arte. |
| Tipografía | Pidió verificar tildes, ñ y signos con DotGothic16. |

Después se registraron tres decisiones del usuario: continuar, elegir Space Mission Design Game y confirmar equipo registrado. La bitácora dejó sin efecto la recomendación de pausa. Esto documenta una decisión, **no una confirmación externa de elegibilidad**. [doc: bitácora][L2]

Además, `git diff` muestra que la copia local de la revisión eliminó filas relativas a fechas, ventana de envío y regla de inicio. El commit conserva esas filas. No hay evidencia suficiente para atribuir una intención a esa edición.

Los requisitos del evento y sus fechas quedan **sin verificar actualmente** en este informe; se describen como contenido de la revisión histórica.

### 6. Historial Git y reproducibilidad

El historial inspeccionado contiene dos commits:

| Commit | Fecha registrada | Contenido |
|---|---|---|
| `4dbae03` | 2026-11-09 00:45, UTC−05:00 | Bóveda, fichas, referencias y kit modular. |
| `e748501` | 2026-11-09 02:18, UTC−05:00 | Habitación 2D, consola, datos, pruebas, historia y revisión. |

`main` y la referencia local `origin/main` apuntan a `e748501`. No se consultó el remoto, por lo que esa coincidencia **no confirma el estado remoto actual**. [doc: historial Git inspeccionado]

Hay tres archivos seguidos modificados: `.gitignore`, la revisión y `project.godot`. La ampliación del prólogo y el dossier permanecen sin seguimiento.

`git lfs ls-files` no devolvió archivos y no existe `.gitattributes`. Tampoco se encontraron flujos `.github/workflows/`. **LFS y CI/CD no están configurados en este repositorio inspeccionado.**

### 7. Pendientes y problemas abiertos

| Prioridad | Pendiente | Estado observado |
|---|---|---|
| Inmediata | Preservar y documentar el prólogo local | No versionado; el proyecto configurado depende de él. |
| Inmediata | Fijar cámara, proporciones y resolución | Contratos antiguos incompatibles entre sí y con el objetivo nuevo. |
| Inmediata | Elegir una implementación principal | Coexisten rutas, entradas y escalas en español e inglés. |
| Alta | Personaje final | Sin modelo 3D, cuerpo configurable, barba ni vista facial independiente. |
| Alta | Gato | Solo ficha y silueta de propuesta. |
| Alta | Entorno final | Arquitectura procedural provisional; muebles planos sin iluminación dinámica. |
| Alta | Tipografía | DotGothic16 ausente. |
| Alta | Costos y procedencia | Sin contabilidad histórica de créditos ni registro completo de recursos nuevos. |
| Alta | Validación actual | Registros anteriores al conjunto exacto de pruebas actual; sin perfil de rendimiento. |
| Media | Datos científicos visibles | Rótulo general incorporado; falta trazabilidad por variable y aproximación. |
| Media | Guardar diseños de misión | Existe `DisenoMision`, pero el guardado del prólogo conserva avatar y libro, no diseños. |
| Media | Pedidos de arte antiguos | Sin carpetas entregadas de iconos de misión, espacio y fuente solicitada. |
| Posterior | Mundo y progresión | Casa, ciudad, campus, biblioteca, planetario, Apolo, inventario y progresión no implementados como conjunto. |
| Posterior | Presentación | Inglés de interfaz, exportación y video final pendientes. |
| Posterior | Cooperación | Los roles de consola son rótulos; no hay modo de equipo implementado. |

Fuentes: [README][L5], [solicitudes][L30], [prólogo][L6], [dossier][L17].

La inspección de referencias detectó dos rutas inexistentes con significados diferentes: DotGothic16 es una entrada opcional ausente; `scenes/architecture.scn` es la salida prevista de `bake_architecture.gd`, no una dependencia necesaria para arrancar. No deben contabilizarse como dos fallos equivalentes.

### 8. Qué reutilizar, rehacer y descartar

«Reutilizar tal cual» significa conservar como base de trabajo. Los estados pendientes de publicación del registro de recursos siguen vigentes.

| Tratamiento | Elementos | Motivo [inf] |
|---|---|---|
| **Reutilizar tal cual** | Originales, bitácora, historial y registro de procedencia | Conservan decisiones y trazabilidad. |
| **Reutilizar tal cual** | Clases de datos y catálogo de misiones | Ya separan datos de interfaz y comportamiento. |
| **Reutilizar como base** | Mecánica orbital, evaluador y pruebas | Aportan un bucle educativo concreto; necesitan validación y explicación de aproximaciones. |
| **Reutilizar como base** | Estados del prólogo, esquema de avatar y guardado | Son independientes del acabado definitivo, aunque conviene modularizarlos. |
| **Reutilizar como referencia** | Atardecer, paleta cálida y libro cian | Encajan con la identidad propia y con un diorama cuidado. |
| **Reutilizar provisionalmente** | Kit PNG | Permite probar recorridos y composición sin gastar créditos. |
| **Rehacer** | Avatar y gato | Deben responder al nuevo lenguaje visual y a sus vistas y animaciones. |
| **Rehacer** | Muebles principales y materiales | El objetivo requiere volumen y una iluminación coherente con la escena. |
| **Rehacer** | Cámara y escala | La implementación actual no representa la exploración alta solicitada. |
| **Rehacer** | Interfaz final | Existen paneles funcionales, pero no el sistema de pergamino, pincel, mapa y avisos del brief. |
| **Rehacer** | Presentación espacial definitiva | El planeta procedural actual funciona como transición visual, no como representación geográfica validada. |
| **Descartar como requisito vigente** | Contrato obligatorio de avatar a 28/36 px y resolución 384×216 | Fue una hipótesis anterior, no una restricción del nuevo producto. |
| **Retirar gradualmente del flujo activo** | Duplicación de habitaciones y sistemas de entrada | Mantener dos bases aumenta la posibilidad de corregir la equivocada. |
| **Descartar del producto final** | Captura externa usada como arte propio o música comercial de referencia | Son materiales de estudio, sin entrega final acreditada. |
| **Descartar como evidencia actual** | Afirmación global de que todo funciona por haber pasado 23 o 33 pruebas | Los registros cubren alcances y versiones diferentes. |

Descartar del flujo activo no significa borrar los originales ni el historial.

### 9. Contradicciones con el brief y el plan actual

Este contraste se limita al brief recibido. La correspondencia exacta con páginas y puertas del PDF actual queda **sin verificar**.

| Tema | Trabajo previo | Brief actual | Resolución recomendada [inf] |
|---|---|---|---|
| Identidad | Gravedad 2D-HD, vinculado a un reto | Proyecto NASA-Ecuador, RPG por ocho fases | Separar nombre del prototipo, título y destino de presentación. |
| Personaje | Sprite pixelado, incluido en mundo 3D | Chibi 3D de 2,5–3 cabezas | Conservar personalización; reconstruir representación. |
| Renderizador | Compatibility | Investigación de Forward+ y GI | Tratar Forward+ como hipótesis pendiente de medición. |
| Cámara | Cuarto fijo y relativamente bajo | Exploración alta y hub lateral | Definir cámaras por modo y validar una muestra de cada una. |
| Iluminación | Sombras dibujadas, geometría iluminada y sprites sin sombreado | Sombras suaves coherentes y estudio de sombras sobre sprites | Crear una prueba específica; no darla por resuelta con el prólogo. |
| Arte | Imagen → recortes PNG → sprites | Imagen → malla → retopología → UV → texturizado | El pipeline 3D aún no existe en esta bóveda. |
| Interfaz | Paneles azul oscuro/cian y portada dorada | Pergamino, pincel, HUD, mapa y avisos | Unificar lenguaje y reservar variantes justificadas por función. |
| Mascota | Gato o perro pendiente | Gato científico | Actualizar la ficha; conservar nombre y personalidad como pendientes. |
| Tipografía | DotGothic16 prevista; Cinzel/Atkinson utilizadas | DotGothic16 | Definir aplicación por contexto e incorporar el recurso aprobado. |
| Mecánicas | Consola centrada en misión espacial | Aventura, simulación y exploración educativa | Integrar la consola como sistema dentro del RPG. |
| Equipo | Reparto Claude/Arte y equipo del evento | Un desarrollador con asistentes | Simplificar responsabilidades y distinguir equipo de presentación de equipo técnico. |
| Presupuesto | Generaciones sin costos registrados | 1000 créditos sin recarga | No inferir saldo ni costo histórico; presupuestar desde datos medidos. |
| Proceso | Producción ya iniciada y aprobaciones parciales | Fase 0 con puertas | Considerar lo existente material exploratorio hasta superar la puerta correspondiente. |
| Video | Dossier propone mostrar el prólogo; guion propone priorizar misiones | Alcance nuevo todavía por validar | Elegir un único objetivo de presentación cuando exista una versión representativa. |

No hay una contradicción importante en la premisa educativa: la observación, el diagnóstico y el rediseño son compatibles con enseñar mediante mecánicas. La brecha principal está en **representación visual, organización del estado vigente y alcance de producción**.

## Fuentes

**Fuentes locales primarias [doc]**

Las rutas corresponden a `C:\Users\guill\Desktop\Juego\Juego_2d-hd`.

- [Índice][L1], [bitácora][L2] y [revisión del 2026-11-09][L3].
- [Configuración de Godot][L4], [README técnico][L5] y [solicitudes de arte][L30].
- [Prólogo][L6], [habitación][L7], [props][L8], [avatar procedural][L9] y [escena 3D][L27].
- [Registro de ejecución][L10] y [pruebas del prólogo][L28].
- [Datos][L11], [núcleo][L12], [evaluador][L29] y [consola][L21].
- [Registro de recursos][L13], [ficha de avatar][L14], [primera escena][L15], [mascota][L16] y [kit][L24].
- [Dossier Markdown][L17], [dossier PDF][L31], [historia][L18], [dirección artística][L19] y [referencia anterior][L20].
- [Recursos del proyecto][L22], [sincronización][L23], [paquete MCP][L25] y [exclusiones Git][L26].
- Historial y estado observados con `git log`, `git status`, `git diff` y `git lfs ls-files`, sin consulta al remoto.

**Documentación externa primaria [doc]**

- [Godot 4.7 — Renderizadores](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html): capacidades y diferencias entre métodos.
- [Godot 4.7 — SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html): iluminación del sprite y comportamiento de billboards con sombras.
- [Godot 4.7 — LightmapGI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/using_lightmap_gi.html): horneado, GPU y UV2.

La documentación externa consultada corresponde a Godot 4.7; no sustituye una comprobación de rendimiento con el ejecutable 4.7.2 en este equipo.

[L1]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/0_Reglas_Globales/index.md>
[L2]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/0_Reglas_Globales/log.md>
[L3]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/0_Reglas_Globales/validacion-claude-2026-11-09.md>
[L4]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/project.godot>
[L5]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/README.md>
[L6]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/scripts/main.gd>
[L7]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/scripts/bedroom.gd>
[L8]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/scripts/prop.gd>
[L9]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/scripts/avatar.gd>
[L10]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/evidence/flow-rendered.log>
[L11]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/datos/>
[L12]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/nucleo/>
[L13]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/kit-habitacion/asset-register.csv>
[L14]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/avatar.md>
[L15]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/primera-escena.md>
[L16]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/mascota-cientifica.md>
[L17]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/arte e Historia.md>
[L18]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/3_Guion_y_Mundo/historia.md>
[L19]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/direccion-artistica.md>
[L20]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/referencias/referencia-principal.md>
[L21]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/escenas/mision/consola_mision.gd>
[L22]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/assets/>
[L23]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/herramientas/sincronizar_arte.ps1>
[L24]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/kit-habitacion/README.md>
[L25]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/.tools/godot-mcp/package.json>
[L26]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/.gitignore>
[L27]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/scenes/bedroom.tscn>
[L28]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/tests/prologue_flow.gd>
[L29]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/godot/nucleo/evaluador_mision.gd>
[L30]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/1_Mecanicas_y_Codigo/solicitudes-arte.md>
[L31]: <C:/Users/guill/Desktop/Juego/Juego_2d-hd/2_Arte_e_Interfaz/arte e Historia.pdf>