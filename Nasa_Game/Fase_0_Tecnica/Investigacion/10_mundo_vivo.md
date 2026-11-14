# Fase 0 — Un mundo vivo y coherente en Godot 4.7 con Intel HD 620

## Resumen ejecutivo

El pilar debe traducirse en una regla: **las acciones del jugador producen respuestas coherentes; el ambiente mantiene actividad sutil incluso cuando nadie interactúa**. Esto requiere buena coordinación entre animación, sonido, estados y color.

Recomiendo **Compatibility como perfil inicial**, con 3D a 1280×720 y una meta provisional de 30 FPS. Forward+ quedaría como comparación técnica. Es una revisión propuesta del plan maestro, pendiente de validación, porque el equipo debe poder desarrollar y ejecutar el juego. [inf] [Base documental](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

El mayor retorno vendrá de interacciones reutilizables, pasos por superficie, objetos que conservan su estado, vegetación animada por shader y expresividad del gato. Reflejos, haces de luz y sombras de nube pueden representarse con efectos sencillos.

Desde Fase 0 deben reservarse contratos para interacción, tiempo, persistencia, audio, paleta y calidad gráfica. Este informe define esos contratos y sus pruebas futuras. **No se modificaron archivos, instalaron herramientas ni consumieron créditos. Los costos de rendimiento indicados son estimaciones, sin verificar mediante benchmark en esta máquina.**

## Decisiones recomendadas

Las recomendaciones de esta tabla son **[inf]**; sus fundamentos documentales se detallan en la sección siguiente.

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja |
|---|---|---|---|
| Renderizador inicial | Compatibility; comparar Mobile y Forward+ en una escena representativa | Forward+ obligatorio desde el inicio: condiciona toda la producción antes de comprobar su rendimiento | Media |
| Iluminación | Luz principal, relleno ambiental controlado y sombras acotadas; evaluar lightmaps en interiores | SDFGI como base: la documentación lo desaconseja para gráficas integradas | Alta |
| Movimiento ambiental | Shaders compartidos, animaciones breves y actividad por proximidad | Simulación física continua de plantas, telas y cables: demasiado mantenimiento y trabajo de CPU | Alta |
| Hierba reactiva | Dos posiciones globales: protagonista y gato | Textura de desplazamiento desde el primer prototipo: añade producción y actualización de otra textura | Alta |
| Partículas | Comparar emisores GPU y CPU pequeños; conservar sustitutos sencillos | Elegir únicamente por el nombre del renderizador: no refleja todas las funciones disponibles en 4.7 | Media |
| Interacciones | Composición de nodos y Resources; una interfaz común para ambos actores | ECS completo: complejidad sin beneficio demostrado para la escala inicial | Alta |
| Persistencia y NPC | Identificadores estables, cambios de estado y rutinas escritas por horarios | Simular permanentemente toda la población y toda la física | Alta |
| Audio | Sistema nativo de Godot, buses y AudioStreamInteractive | Incorporar FMOD/Wwise en Fase 0: añade otra integración antes de demostrar una necesidad | Alta |
| Color | Paleta semántica, rampas compartidas y revisión automática más aprobación visual | Corregir toda inconsistencia con una LUT global: puede ocultar problemas y alterar colores correctos | Alta |
| Alcance inicial | Una escena pequeña con respuestas completas y medibles | Distribuir efectos incompletos por muchas zonas | Alta |

## Afirmaciones que sostienen las decisiones

1. **[doc]** Godot ofrece Compatibility para hardware de gama baja; Mobile y Forward+ utilizan RenderingDevice. Tener soporte de API no garantiza rendimiento suficiente para una escena concreta. [Comparación de renderizadores 4.7](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

2. **[doc]** SDFGI funciona en Forward+ y la documentación señala que resulta exigente para gráficas integradas. [Environment: SDFGI](https://docs.godotengine.org/en/4.7/classes/class_environment.html#class-environment-property-sdfgi-enabled).

3. **[doc]** LightmapGI ofrece iluminación indirecta estática con buen rendimiento durante la ejecución; el horneado integrado necesita un dispositivo capaz de usar Mobile o Forward+. Su viabilidad de horneado en esta HD 620 está **sin verificar**. [LightmapGI](https://docs.godotengine.org/en/4.7/classes/class_lightmapgi.html).

4. **[doc]** Los uniforms globales permiten compartir viento y posiciones de actores entre shaders. Leerlos continuamente desde CPU introduce sincronización; conviene mantener también sus valores en un servicio del juego. [Lenguaje de sombreado](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html#global-uniforms).

5. **[doc]** MultiMesh reduce el trabajo de enviar muchas instancias al renderizador, pero su visibilidad se evalúa como conjunto. Por eso conviene dividir la vegetación espacialmente. [MultiMesh](https://docs.godotengine.org/en/4.7/classes/class_multimesh.html).

6. **[doc]** GPUParticles3D puede utilizarse en Compatibility, con restricciones: por ejemplo, `emit_particle()` no está disponible allí; los trails y la colisión SDF requieren Mobile o Forward+. CPUParticles3D simula en CPU y sigue dibujándose en GPU. [GPUParticles3D](https://docs.godotengine.org/en/4.7/classes/class_gpuparticles3d.html), [trails](https://docs.godotengine.org/en/4.7/tutorials/3d/particles/trails.html), [shaders de partículas](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/particle_shader.html).

7. **[doc]** Tween es una herramienta ligera para interpolaciones; AnimationPlayer resulta más adecuado cuando la animación necesita edición visual y tiempos definidos. [Tween](https://docs.godotengine.org/en/4.7/classes/class_tween.html).

8. **[doc]** AudioStreamInteractive combina clips mediante reglas de transición, incluidas transiciones al siguiente pulso o compás. La música necesita metadatos y edición compatibles con esas reglas. [AudioStreamInteractive](https://docs.godotengine.org/en/4.7/classes/class_audiostreaminteractive.html), [importación de audio](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_audio_samples.html).

9. **[doc]** AudioStreamPlayer3D aplica posicionamiento y atenuación respecto al oyente. Por defecto escucha desde la cámara; AudioListener3D permite cambiar ese punto. [AudioStreamPlayer3D](https://docs.godotengine.org/en/4.7/classes/class_audiostreamplayer3d.html).

10. **[doc]** Los ajustes de Environment están disponibles en los tres renderizadores. La corrección admite LUT de una dimensión o Texture3D y se aplica después del tonemapping. [Renderizadores 4.7](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html), [Environment](https://docs.godotengine.org/en/4.7/classes/class_environment.html#class-environment-property-adjustment-color-correction).

11. **[doc]** FFmpeg dispone de `loudnorm` con medición de sonoridad integrada, rango y pico verdadero, incluidas dos pasadas. **[inf]** Los objetivos de LUFS deben definirse para este juego y comprobarse sobre la mezcla completa. [FFmpeg: loudnorm](https://ffmpeg.org/ffmpeg-filters.html#loudnorm).

12. **[doc]** La información esencial debe disponer de símbolos, texto, formas u otras señales además del color. Los cambios globales de paleta pueden crear nuevas confusiones. [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/).

## Riesgos y cómo mitigarlos

| Riesgo | Mitigación propuesta |
|---|---|
| Una escena bonita que pierde fluidez al añadir transparencias | Medir hierba, partículas, agua y haces por separado; reducir primero superficie transparente y superposición. [inf] [Optimización GPU](https://docs.godotengine.org/en/4.7/tutorials/performance/gpu_optimization.html). |
| Interpretar “vivo” como movimiento constante | Reservar pausas, variaciones lentas y elementos inmóviles. Cada movimiento debe tener una causa y una intensidad definida. [inf] |
| Prometer interacción con cualquier objeto | Establecer categorías de respuesta y cubrir todos los elementos que visualmente prometen una acción; reutilizar comportamientos. [inf] |
| Gato y protagonista activan dos veces un mecanismo | Resolver las acciones mediante una única autoridad, con validación de estado y bloqueo temporal del objetivo. [inf] [Organización de escenas](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html). |
| Rutinas de NPC provocan picos de CPU | Escalonar decisiones y consultas de navegación; suspender la representación física de NPC lejanos. [inf] [Optimización de navegación](https://docs.godotengine.org/en/4.7/tutorials/navigation/navigation_optimizing_performance.html). |
| Lightmaps contradictorios con un ciclo solar continuo | Usarlos inicialmente en interiores de iluminación estable. Exteriores: luz directa y gradientes, sin depender de un horneado para cada hora. [inf] [LightmapGI](https://docs.godotengine.org/en/4.7/classes/class_lightmapgi.html). |
| Sonidos IA con diferente distancia, reverberación o volumen | Generar familias secas, aplicar un procesamiento común y asignar la acústica espacial dentro de Godot. [inf] [Buses](https://docs.godotengine.org/en/4.7/tutorials/audio/audio_buses.html). |
| Recursos IA con colores y detalle incompatibles | Corregir el recurso antes de importarlo; revisar albedo, escala de detalle y paleta bajo una iluminación de referencia. [inf] [ImageMagick](https://imagemagick.org/command-line-options/#remap). |
| Tirones al mostrar un shader por primera vez | Preparar los materiales durante la carga. En Compatibility, la documentación recomienda mostrarlos dentro del campo visible al menos un fotograma. [doc] [Compilación de shaders](https://docs.godotengine.org/en/4.7/tutorials/performance/pipeline_compilations.html). |
| Los 27 GB libres se consumen con originales y variantes | Conservar únicamente candidatos útiles, separar originales de recursos de ejecución y evitar vídeos como solución al movimiento ambiental. [inf] |

## Preguntas que debe decidir el usuario

1. **Perfil técnico:** ¿se acepta evaluar Compatibility como perfil principal, con meta inicial de 30 FPS y 3D a 720p?
2. **Tiempo del mundo:** ¿el día avanza continuamente o mediante franjas ligadas a acciones y descansos? Recomiendo franjas para el primer prototipo.
3. **Primer alcance:** ¿se valida una escena con ocho objetos interactivos, tres NPC y dos acciones del gato antes de ampliar el catálogo?
4. **Presupuesto sonoro:** ¿se reserva un máximo inicial de 50 créditos para pruebas y recursos de audio de esa primera zona?

## Desarrollo

### 1. Alcance, evidencia y criterio de calidad

Se consultó el plan maestro completo y las matrices locales de costos y parámetros. Las fases citadas corresponden a ese documento. La versión 4.7.2-stable figura en el [archivo oficial de Godot](https://godotengine.org/download/archive/4.7.2-stable/). [doc]

Las etiquetas significan:

- **[doc]:** documentación primaria, especificación o material oficial del desarrollador.
- **[sec]:** fuente secundaria; no fue necesaria para fundamentar estas recomendaciones.
- **[inf]:** propuesta, estimación o interpretación de este informe.

**No se comprobó el rendimiento de estas técnicas en el equipo.** La disponibilidad de funciones se contrastó principalmente con documentación fijada en **4.7**, evitando atribuir automáticamente a esa versión funciones de `latest`.

La definición operativa propuesta de “mundo vivo” tiene cuatro condiciones. [inf]

| Condición | Evidencia perceptible |
|---|---|
| El mundo continúa | Una cortina se mueve, cambia el ambiente sonoro o un NPC realiza una actividad |
| El mundo percibe | Hierba, animales, objetos o personajes responden al acercamiento |
| El mundo recuerda | Un interruptor, reparación o recolección conserva su resultado |
| El mundo es coherente | Viento, sonido, luz, color y animación describen la misma situación |

Una planta con viento, sonido de roce al pasar y recuperación suave cumple mejor el pilar que numerosas partículas sin relación con las acciones. Esta es una decisión de dirección propuesta, no una medición universal. [inf]

### 2. Presupuesto inicial para la HD 620

Propongo estas **condiciones de prueba**, sujetas a medición:

| Parámetro | Punto inicial propuesto |
|---|---|
| Renderizador | Compatibility |
| Resolución 3D | 1280×720; interfaz a resolución de ventana |
| Meta de presentación | 30 FPS: 33,3 ms por fotograma |
| Margen | Buscar una escena base por debajo de 25 ms antes del detalle ambiental |
| Iluminación | Una luz principal; luces locales escasas y sin sombras inicialmente |
| Sombras | Distancia corta y emisores seleccionados |
| NPC iniciales | Tres NPC cercanos más el gato |
| Partículas | Primer escalón de 32–64 visibles en total |
| Audio largo | Hasta cuatro flujos durante transiciones |
| Efectos cortos | Primer límite de doce voces simultáneas |

**Todos esos límites son [inf], no capacidades medidas ni límites del motor.** El escalado bilineal 3D está disponible en los tres renderizadores; reducir resolución ayuda cuando el límite está en GPU, pero no resuelve un cuello de botella de CPU. [doc] [Escalado de resolución](https://docs.godotengine.org/en/4.7/tutorials/3d/resolution_scaling.html).

La prueba futura debe comparar la misma cámara y recorrido con cada sistema activado y desactivado. Registrar tiempo de fotograma, percentiles, llamadas de dibujo, memoria y actividad de navegación; repetir un recorrido prolongado para detectar degradación térmica. CPU y GPU deben analizarse por separado, pues sus tiempos pueden solaparse. [inf] [Optimización GPU](https://docs.godotengine.org/en/4.7/tutorials/performance/gpu_optimization.html), [monitores Performance](https://docs.godotengine.org/en/4.7/classes/class_performance.html).

Para el estilo mixto, recomiendo mantener **un mundo físico 3D**, incluso en el hub lateral, y cambiar cámara y restricciones de movimiento. Si se utilizan personajes planos, Sprite3D puede recibir iluminación al activar `shaded`; su modo de transparencia necesita revisión. Un Sprite2D pertenece a otro sistema de representación y no sustituye directamente ese comportamiento. [inf/doc] [SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html).

### 3. Movimiento ambiental barato

En esta tabla, **bajo/medio/alto son costos relativos estimados [inf]**, bajo los límites anteriores. “Sí” significa que la técnica puede construirse con las funciones documentadas; su rendimiento y apariencia en la HD 620 están **sin verificar**.

La base técnica son los shaders espaciales, uniforms globales y sistemas de partículas de Godot. [doc] [Shaders espaciales](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html), [uniforms](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html), [partículas](https://docs.godotengine.org/en/4.7/tutorials/3d/particles/index.html).

| Técnica | Implementación propuesta y costo principal | Compatibility | Mobile | Forward+ |
|---|---|---|---|---|
| Vegetación al viento | Desplazar vértices con máscara de rigidez; costo GPU bajo con mallas pequeñas | Sí | Sí | Sí |
| Telas | Ondulación de una malla segmentada, fijada por máscara; bajo–medio según vértices | Sí | Sí | Sí |
| Cables | Curva de reposo y oscilación leve con extremos inmóviles; bajo | Sí | Sí | Sí |
| Hierba al paso | Distancia a dos actores en coordenadas mundiales; bajo | Sí | Sí | Sí |
| Huellas mediante textura | Muestrear una textura de deformación; costo adicional de producirla y actualizarla, medio | Sí, sin depender de compute | Sí | Sí |
| GPUParticles3D sencillas | Simulación GPU; costo bajo–medio, más dibujo y transparencia | Sí, con restricciones | Sí | Sí |
| CPUParticles3D | Simulación CPU más dibujo GPU; bajo con pocos elementos, crece con cantidad | Sí | Sí | Sí |
| Polvo en haces | Pocas motas dentro de un haz geométrico; medio por transparencia | Sí | Sí | Sí |
| Hojas | Emisor pequeño, sin colisiones, con caída y oscilación; bajo–medio | Sí | Sí | Sí |
| Insectos decorativos | Trayectorias analíticas y fases distintas; bajo | Sí | Sí | Sí |
| Aves lejanas | Siluetas animadas sobre rutas; bajo | Sí | Sí | Sí |
| Agua estilizada | Superficie opaca, ondas de normales/UV y espuma limitada; bajo–medio | Sí | Sí | Sí |
| Reflejo fingido | Color del cielo, textura ilustrada o brillo direccional; bajo | Sí | Sí | Sí |
| Luces inestables | Variación suave de emisión y, excepcionalmente, energía de una luz; bajo sin sombras | Sí | Sí | Sí |
| Nubes | Capas de cielo o geometría distante con UV móviles; bajo | Sí | Sí | Sí |
| Sombra de nube | Máscara mundial compartida en materiales receptores; bajo–medio por píxel | Sí | Sí | Sí |
| Hora del día | Gradientes de cielo, niebla, luz y ambiente; bajo si no fuerza recapturas | Sí | Sí | Sí |
| Respiración, orejas y cola | Animación breve o huesos seleccionados; bajo para pocos personajes | Sí | Sí | Sí |

Las restricciones concretas de GPU particles incluyen `emit_particle()`, trails y colisión SDF. Para el perfil inicial propongo prescindir de esas funciones avanzadas. [doc/inf] [GPUParticles3D](https://docs.godotengine.org/en/4.7/classes/class_gpuparticles3d.html), [colisiones](https://docs.godotengine.org/en/4.7/tutorials/3d/particles/collision.html).

#### Viento compartido y jerarquía de movimiento

El viento debe ser **un dato común**, con dirección, fuerza y ráfagas. Vegetación, telas, cables y ambiente sonoro derivan sus respuestas de ese dato, con sensibilidades diferentes. [inf] [Uniforms globales](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html#global-uniforms).

Para cada recurso deformable:

- Máscara de rigidez: raíz, costura o extremos inmóviles.
- Oscilación principal lenta y secundaria de menor amplitud.
- Variación por posición mundial e instancia para evitar sincronía.
- Volumen de visibilidad que incluya el desplazamiento máximo.
- Intensidad reducida en interiores y en el modo de movimiento reducido.

Son requisitos del pipeline propuestos [inf]. Un recurso IA que carezca de geometría apropiada, anclajes o máscara no debe aceptarse como “listo para viento”.

La hierba se agruparía con MultiMesh por sectores. Evitaría tanto un nodo por brizna como un único MultiMesh para toda la zona. [inf] [MultiMesh](https://docs.godotengine.org/en/4.7/classes/class_multimesh.html).

#### Hierba que se dobla

Primera implementación propuesta [inf]:

1. Publicar posición, radio e intensidad del protagonista y del gato.
2. Calcular influencia por distancia horizontal y limitarla también por altura.
3. Doblar desde la raíz, respetando la máscara de rigidez.
4. Suavizar velocidad e intensidad para evitar cambios bruscos.
5. Usar deformación analítica con recuperación inmediata y suave.

Esta solución representa la proximidad; **no conserva un sendero aplastado**. Si posteriormente se necesita memoria del paso de varios actores, evaluar una textura de desplazamiento local, de baja resolución, con desvanecimiento. Su productor y frecuencia de actualización también deben medirse. [inf] [Base de uniforms y texturas de shader](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html).

#### Partículas y pequeños agentes

Compararía GPU y CPU con cantidades idénticas. CPU puede resultar suficiente para unos pocos elementos; GPU evita trasladar esa simulación a los dos núcleos disponibles. Ninguna elección elimina el costo de dibujar transparencias. [inf/doc] [Sistemas de partículas](https://docs.godotengine.org/en/4.7/tutorials/3d/particles/index.html).

Propuesta inicial [inf]:

- Polvo: una región pequeña, sin colisiones.
- Hojas: eventos ocasionales ligados a ráfagas.
- Insectos: puntos de interés locales, sin pathfinding.
- Aves: rutas predefinidas y reacción de huida sólo si son cercanas.
- Elementos recogibles: entidades reales separadas de sus partículas decorativas.

Los haces se representarían con una malla sencilla y transparencia contenida. Una gran capa transparente que cubre toda la pantalla debe superar una prueba específica de costo. [inf] [Optimización GPU](https://docs.godotengine.org/en/4.7/tutorials/performance/gpu_optimization.html).

#### Agua, nubes y luces

Para el agua recomiendo comenzar con una superficie opaca pintada, dos movimientos de textura y espuma junto a orillas definidas. Las ondas provocadas por actores pueden ser círculos breves reutilizados. El reflejo sería una interpretación del cielo o de elementos importantes; no un espejo exacto. [inf] [Shaders espaciales](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html).

Las sombras de nube deben compartir escala y desplazamiento entre suelo, rocas y vegetación. Una máscara de zona evitará oscurecer interiores. Implementarlas en los materiales conserva una solución común sin depender de proyectores de luz. [inf] [Funciones por renderizador](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

El parpadeo de una pantalla o lámpara se haría principalmente variando su material. La emisión por sí sola no ilumina automáticamente los objetos próximos; una luz local adicional debe presupuestarse por separado. [doc/inf] [Luces y sombras](https://docs.godotengine.org/en/4.7/tutorials/3d/lights_and_shadows.html).

#### Hora del día y movimiento secundario

Recomiendo cuatro estados artísticos iniciales: mañana, tarde, atardecer y noche, conectados por gradientes. Cambiarían color ambiental, cielo, niebla, luz principal y mezcla sonora. Evitaría recalcular iluminación indirecta o capturas de reflexión continuamente. [inf] [Environment](https://docs.godotengine.org/en/4.7/tutorials/3d/environment_and_post_processing.html).

Respiración, parpadeos, orejas y cola comenzarían con AnimationPlayer. SpringBoneSimulator3D existe en 4.7 y puede aportar inercia a una cola; lo reservaría para el personaje o gato cercano. La documentación advierte sobre esqueletos escalados, por lo que no se debe combinar sin revisión con squash sobre ese Skeleton3D. [doc/inf] [SpringBoneSimulator3D](https://docs.godotengine.org/en/4.7/classes/class_springbonesimulator3d.html).

### 4. Interacción con el entorno

#### Qué significa “con todo su entorno”

Propongo clasificar los elementos por su promesa visual. [inf]

| Clase | Respuesta mínima |
|---|---|
| Fondo distante | Coherencia de luz, color y sonido |
| Superficie transitable | Pasos y respuesta contextual: polvo, roce o agua |
| Decoración cercana | Movimiento ambiental o pequeña reacción cuando corresponda |
| Objeto utilizable | Aviso claro, acción, respuesta y estado |
| Elemento científico | Comportamiento causal consistente con el modelo educativo |

Así, un ventilador reparado puede empezar a girar, producir sonido y mover una cinta cercana. Ese vínculo causal debe tener prioridad sobre añadir efectos independientes. [inf]

#### Componentes propuestos

Usaría composición de escenas y Resources: aprovecha las relaciones y señales de Godot sin introducir un ECS completo. [inf] [Organización de escenas](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html), [Resources](https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html).

| Componente | Responsabilidad |
|---|---|
| `InteractionSensor` | Mantener candidatos cercanos |
| `Interactable` | Describir acciones, condiciones y actores permitidos |
| `InteractionResolver` | Seleccionar objetivo y validar la ejecución |
| `FeedbackComponent` | Coordinar animación, audio y efecto visual |
| `WorldStateComponent` | Leer y aplicar el estado persistente |
| `ReactionComponent` | Responder a contacto, presencia o cambios de estado |
| `SurfaceProfile` | Identificar superficie para pasos y efectos |

La detección puede usar Area3D y consultas físicas filtradas. Recomiendo seleccionar por disponibilidad, prioridad explícita, distancia y orientación, con desempate estable e histéresis para que el aviso no salte entre objetos. Al pulsar, se revalida el objetivo inmediatamente. [inf] [Area3D](https://docs.godotengine.org/en/4.7/classes/class_area3d.html).

El resaltado inicial sería un cambio discreto del material más un icono. Un contorno de geometría adicional quedaría para los objetos donde aporte claridad; evitaría empezar con un contorno de pantalla completa. El material compartido no debe cambiar accidentalmente en todos los objetos al seleccionar uno. [inf] [Resources compartidos](https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html), [shaders](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html).

#### Respuestas físicas ligeras

| Objeto | Solución propuesta |
|---|---|
| Libro, cartel o maceta | Oscilación amortiguada del hijo visual |
| Puerta | Animación de un pivote y colisión sincronizada |
| Interruptor | Cambio breve de posición, clic y estado lógico |
| Pantalla | Textura/estado de material y sonido de confirmación |
| Cajón | Movimiento limitado y condición de apertura |
| Objeto realmente empujable | RigidBody3D sólo cuando la mecánica lo necesita |

Son decisiones [inf]. Para puertas y objetos móviles con colisión, AnimatableBody3D ofrece movimiento controlado y sincronización física. [doc] [AnimatableBody3D](https://docs.godotengine.org/en/4.7/classes/class_animatablebody3d.html).

El resultado lógico debe confirmarse antes de emitir el feedback de éxito. Una puerta bloqueada puede moverse ligeramente y sonar, pero no debe anunciar una apertura que no ocurrió. [inf]

#### Persistencia

Guardar cambios mediante claves estables, por ejemplo:

```text
zona/puerta_principal → abierta
zona/ventilador_01 → reparado
zona/recurso_03 → recolectado
npc/tecnico_01 → conversacion_pendiente
```

Propuesta [inf], apoyada en la serialización documentada de Godot: [guardado de partidas](https://docs.godotengine.org/en/4.7/tutorials/io/saving_games.html).

Deben distinguirse estado permanente, estado del día y reacción transitoria. Una reparación se guarda; una hoja en movimiento se reconstruye. Al cargar, se aplica el estado sin repetir recompensas ni sonidos de obtención. [inf]

#### NPC y gato

Para los primeros NPC propongo tres o cuatro actividades por persona, con destinos y animaciones compartidas: trabajar, desplazarse, descansar y conversar. Las decisiones se evaluarían lentamente; el desplazamiento seguiría actualizándose con la física. Los NPC fuera de la zona activa conservarían sólo su situación lógica. [inf]

La navegación debe solicitar rutas al cambiar realmente el destino y distribuir las consultas entre fotogramas. [doc] [Optimización de navegación](https://docs.godotengine.org/en/4.7/tutorials/navigation/navigation_optimizing_performance.html).

El gato utilizaría el mismo contrato de interacción con capacidades propias:

- Detectar un recurso y señalarlo.
- Activar un mecanismo expresamente autorizado.
- Mirar o acercarse al objetivo del jugador.
- Reaccionar a sonidos y descubrimientos con enfriamientos.
- Recuperarse de un atasco sin bloquear el progreso.

Estas capacidades son propuestas [inf]. Ambos actores deben compartir los estados de los objetivos y resolver conflictos antes de ejecutar una acción.

#### Qué extraer de los referentes

Las siguientes observaciones describen funciones públicas; no atribuyen arquitecturas internas a esos juegos.

| Referente | Principio documentado | Adaptación viable propuesta |
|---|---|---|
| Zelda | Uso de física en rompecabezas y atención a la distancia de sonidos ambientales. [doc] [Entrevista oficial](https://www.nintendo.com/en-za/News/2017/February/Find-out-some-of-Eiji-Aonuma-s-favourite-things-from-The-Legend-of-Zelda-series-in-our-interview--1198478.html), [diseño sonoro](https://www.nintendo.com/us/whatsnew/ask-the-developer-vol-9-the-legend-of-zelda-tears-of-the-kingdom-part-1/) | Pocas reglas causales reutilizables: alimentar, abrir, mover, detectar. [inf] |
| Monster Hunter Stories 2 | Habilidades del compañero para localizar recursos y superar obstáculos; acciones contextuales señaladas con iconos. [doc] [Manual](https://game.capcom.com/manual/MHST2/en/switch/page/3/3) | Dos capacidades claras del gato con oportunidades visibles de uso. [inf] |
| Bravely | Fondos ilustrados combinados con elementos 3D; en Bravely Default II, enemigos visibles capaces de perseguir al grupo. [doc] [Presentación original](https://www.nintendo.com/au/games/nintendo-3ds/bravely-default/), [segunda entrega](https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/BRAVELY-DEFAULT-II-1698006.html) | Composición de diorama y actores con reacciones escritas. [inf] |
| Pokémon: Let’s Go | Compañero presente y técnicas para actuar sobre obstáculos del mundo. [doc] [Sitio oficial](https://pokemonletsgo.pokemon.com/en-us/story/) | Vínculo expresivo y utilitario con el gato, sin multiplicar sistemas. [inf] |

Para un desarrollador, recomiendo adoptar estos principios de legibilidad, compañía y causalidad. La escala completa de sus contenidos queda fuera del primer alcance. [inf]

### 5. Game feel por impacto y costo

El orden siguiente es una propuesta **[inf]**. Los tiempos son valores iniciales para ajustar, no estándares.

| Orden | Mejora | Punto inicial | Costo |
|---|---|---|---|
| 1 | Respuesta inmediata al input | Foco, sonido o inicio de acción en el siguiente fotograma disponible | Bajo |
| 2 | Contacto y seguimiento | Acción sincronizada con contacto; recuperación breve | Bajo en ejecución; medio en autoría |
| 3 | Pasos y materiales | Sonido y efecto en el contacto del pie | Bajo |
| 4 | Tweens de interfaz | Transiciones aproximadas de 80–180 ms, cancelables | Bajo |
| 5 | Anticipación | Preparación visible sin retrasar innecesariamente el control | Bajo–medio |
| 6 | Squash and stretch | Deformación visual moderada en aterrizajes y objetos expresivos | Bajo |
| 7 | Cámara reactiva | Impulso pequeño con intensidad configurable y opción cero | Bajo |
| 8 | Hit stop | Pausas selectivas de aproximadamente 30–60 ms | Bajo; cuidado con la lógica temporal |

Tween y AnimationPlayer proporcionan las herramientas para estas respuestas. Evitar varios tweens compitiendo por la misma propiedad. [doc] [Tween](https://docs.godotengine.org/en/4.7/classes/class_tween.html).

El hit stop debería afectar a los actores implicados, preservando interfaz y audio. Recomiendo evitar que una pausa breve altere rutinas, reloj del mundo o recuperación del control. [inf]

Debe existir desde el contrato inicial una intensidad de movimiento que controle sacudidas, balanceo de cámara, zooms e inclinaciones. La revisión final de accesibilidad permanece en Fase 7, pero los efectos deben aceptar ese parámetro desde su implementación. [inf]

También conviene usar un tiempo ambiental propio: el `TIME` del shader está afectado por `time_scale`, pero no por la pausa del árbol. [doc] [Tiempo en shaders](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html#global-built-ins).

### 6. Sonido coherente y producción con IA

#### Guía sonora propuesta

Definir una ficha común antes de generar audio. [inf]

| Familia | Carácter propuesto |
|---|---|
| Barrio | Aire, vegetación y actividad humana distante con pausas |
| Cuarto | Ventilador, calle filtrada y objetos próximos |
| Laboratorio | Relés, teclas, ventilación y tonos instrumentales discretos |
| Simulador | Maquinaria contenida, graves moderados y señales informativas |
| Interfaz | Papel, pulsaciones y confirmaciones cortas de la misma familia |
| Gato | Repertorio pequeño, reconocible y sin repetición excesiva |
| Música | Ambient/shoegaze con espacio para acciones y señales científicas |

Cada zona tendría una base ambiental, una capa variable y eventos puntuales. El viento sonoro debe responder al mismo estado que mueve las telas. Una puerta o máquina debe modificar su sonido al cambiar su estado. [inf]

#### Posicionamiento, pasos y reverberación

Usaría AudioStreamPlayer3D para fuentes localizables y AudioStreamPlayer para música e interfaz. En las cámaras altas o laterales, probaría un AudioListener3D cercano al personaje para que la distancia de la cámara no distorsione la lectura sonora. [inf] [Audio posicional](https://docs.godotengine.org/en/4.7/classes/class_audiostreamplayer3d.html).

Los pasos consultarían un `SurfaceProfile`: tierra, concreto, madera, metal o agua. La animación indicaría el contacto; el sistema elegiría una variante evitando repetición inmediata. [inf]

Para acústica, reservar Area3D, capas de audio y buses de reverberación. El volumen de una habitación **no calcula automáticamente una acústica físicamente exacta**: se diseñan presets y se comprueban transiciones y solapamientos. [doc/inf] [Area3D](https://docs.godotengine.org/en/4.7/classes/class_area3d.html), [efectos](https://docs.godotengine.org/en/4.7/tutorials/audio/audio_effects.html).

La primera versión puede usar dos reverberaciones compartidas: habitación pequeña y laboratorio. Evitar un efecto independiente por emisor. [inf]

#### Música adaptativa

Comenzaría con tres estados: exploración, concentración y descubrimiento. AudioStreamInteractive gestionaría clips y transiciones; para música sin pulso regular usaría finales de frase y fundidos. Para música medida, cargar BPM, compás y duración comprobados. [inf/doc] [AudioStreamInteractive](https://docs.godotengine.org/en/4.7/classes/class_audiostreaminteractive.html).

Los cambios se solicitarían por nombre desde AudioStreamPlaybackInteractive. [doc] [Control del clip](https://docs.godotengine.org/en/4.7/classes/class_audiostreamplaybackinteractive.html).

Los parámetros locales consultados no demuestran generación de stems sincronizados. Por ello recomiendo comenzar con clips completos. AudioStreamSynchronized permite capas simultáneas, pero requiere material preparado para mantener coherencia musical. [inf/doc] [AudioStreamSynchronized](https://docs.godotengine.org/en/stable/classes/class_audiostreamsynchronized.html).

#### Familias de prompts y procesamiento

Plantilla propuesta [inf]:

```text
Familia y función:
Material o instrumentación:
Acción:
Distancia y perspectiva:
Duración:
Dinámica:
Acústica seca o ambiente:
Restricciones:
Referencia interna aprobada:
```

Ejemplo de familia SFX: objeto mecánico pequeño, grabación cercana y seca, una acción aislada, sin música ni voz. Entre variantes cambia el objeto o gesto; se mantiene la perspectiva.

Para música: instrumentación, densidad, registro, carácter armónico y función deben mantenerse entre clips. Pedir el mismo tempo no garantiza alineación ni estructura correctas. [inf]

Procesamiento común propuesto [inf], usando los filtros documentados de [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html):

1. Inspeccionar duración, canales, saturación y silencios.
2. Recortar el inicio sin eliminar el ataque.
3. Aplicar fundidos breves para evitar clics.
4. Corregir problemas concretos con EQ; evitar una cadena agresiva universal.
5. Medir sonoridad y pico verdadero.
6. Ajustar por familia y comparar en el juego.
7. Verificar bucles y transiciones.
8. Conservar original, versión procesada y parámetros utilizados.

#### Sonoridad y formatos

Objetivos de trabajo **[inf]**, pendientes de escucha y captura de una sesión representativa:

| Material | Objetivo inicial |
|---|---|
| Música aislada | Alrededor de −20 LUFS-I; pico verdadero ≤ −2 dBTP |
| Ambiente continuo | Alrededor de −28 LUFS-I, ajustado por zona |
| SFX breves | Nivel por familia y pico; evitar normalizar cada clic por LUFS-I |
| Mezcla completa | Explorar aproximadamente −18 LUFS-I, con margen dinámico |
| Salida | Comprobar que el pico verdadero no supere −1 dBTP |

Estos valores no constituyen una norma de videojuegos. `loudnorm` permite medir y procesar en dos pasadas; la suma de voces debe comprobarse por separado. [doc] [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html#loudnorm).

Recomiendo WAV para efectos cortos y repetidos, y Ogg Vorbis para música y ambientes largos. Una extensión `.ogg` no demuestra que el códec sea Vorbis: los resultados Ogg Opus requieren conversión. [doc/inf] [Importación](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_audio_samples.html), [carga de audio](https://docs.godotengine.org/en/4.7/tutorials/io/runtime_file_loading_and_saving.html).

Adoptaría 48 kHz como formato de entrega interno por consistencia, sin atribuirle mejora sobre un original de menor frecuencia. Desactivaría la normalización automática de importación cuando invalide niveles ya preparados. [inf] [Opciones de importación](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_audio_samples.html).

#### Cupo de créditos para la primera zona

Cálculo basado en las cotizaciones locales, cuya vigencia futura está **sin verificar**:

| Producción propuesta | Cálculo | Créditos |
|---|---:|---:|
| Tres candidatos musicales de 15 s, Sonilo | 3 × 0,94 | 2,82 |
| Tres clips musicales de 60 s, Sonilo | 3 × 3,75 | 11,25 |
| Doce SFX de 3 s, Mirelo | 12 × 0,75 | 9,00 |
| Primera pasada | | **23,07** |
| Una repetición completa como máximo | | **46,14 acumulados** |

**[inf] Propuesta: techo de 50 créditos**, con aprobación de cada recurso. Los precios no certifican calidad, posibilidad de bucle ni consistencia. Fuente local: [matriz de costos](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>).

El costo por defecto de Seed Audio no se utilizaría para proyectar una producción musical: no equivale a una cotización comparable por duración. Fuente local: [costos por defecto](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_default.md>).

### 7. Paleta consistente

#### Paleta maestra y sombreado

Propongo un Resource `PaletteDefinition` con versión y roles semánticos. Resources permite compartir datos entre escenas. [inf/doc] [Resources](https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html).

Debe contener:

- Neutros, papel, tinta y colores estructurales.
- Familias cálidas y tropicales; familias técnicas y frías.
- Acentos de personaje, interacción, energía y advertencia.
- Rampas para materiales, piel, vegetación y metal.
- Variantes aprobadas por hora.
- Sustituciones de accesibilidad.

Para toon, utilizar rampas compartidas muestreadas según la iluminación. La rampa del material y la LUT final cumplen funciones diferentes. Si el shader depende de `light()`, revisar que la iluminación por vértice no esté anulando esa función. [inf/doc] [Shaders espaciales](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html).

#### Gradación y LUT

En Godot 4.7, Environment permite ajustes y corrección mediante LUT en Compatibility, Mobile y Forward+. [doc] [Comparación](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html).

Usaría primero exposición, contraste y saturación moderados. Una LUT más compleja sólo se incorporaría tras aprobar un conjunto de escenas de referencia. La corrección se aplica después del tonemapping, por lo que éste también debe permanecer controlado. [inf/doc] [Environment](https://docs.godotengine.org/en/4.7/classes/class_environment.html#class-environment-property-adjustment-color-correction).

La interfaz conservaría sus colores semánticos mediante su propio tema y materiales, sin depender de que la gradación 3D produzca el color correcto. [inf]

#### Comprobación automática

Pipeline propuesto **[inf]**, realizable con ImageMagick y Python:

1. Identificar tipo de textura y espacio de color.
2. Excluir normales, rugosidad, máscaras y datos.
3. Muestrear píxeles visibles respetando alfa.
4. Convertir muestras y paleta al mismo espacio perceptual.
5. Calcular distancia a los colores o rampas autorizados.
6. Informar porcentaje alejado, desviaciones dominantes y excepciones.
7. Comparar antes/después bajo iluminación neutra y dentro de la escena.

ΔE76 es la distancia euclídea en CIELAB y sirve como aproximación inicial; no debe confundirse con una certificación de calidad artística. [doc] [W3C: diferencias de color](https://www.w3.org/TR/css-color-4/#color-difference).

Como umbral experimental, podría avisarse cuando más del 15 % de las muestras se aleje más de ΔE76=12 de su familia permitida. **Esos valores son [inf] y deben calibrarse con recursos aprobados.** Una textura pintada admite variaciones que una interfaz plana puede no admitir.

ImageMagick ofrece `-remap`, pero el remapeo duro puede eliminar matices. Lo reservaría para recursos de paleta estricta; para arte pintado priorizaría correcciones de tono, saturación y rampas por material. [doc/inf] [ImageMagick](https://imagemagick.org/command-line-options/#remap).

#### Daltonismo y deriva de IA

Los modos de daltonismo cambiarían **roles**, no colores detectados arbitrariamente: interacción, peligro, categorías científicas, marcadores y HUD. Añadir símbolos, patrones y texto. Los circuitos educativos deben poder leerse sin distinguir rojo de verde. [inf] [Accesibilidad del color](https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/).

Para corregir deriva de IA propongo [inf]:

- Referencia interna aprobada y especificación cromática común.
- Corrección del albedo antes de añadir iluminación artística.
- Evitar sombras y brillos fuertes pintados que contradigan la escena.
- Proteger piel, identidad del personaje y señales funcionales.
- Aplicar la misma transformación a toda una animación para evitar parpadeo.
- Regenerar únicamente cuando la corrección local no preserve el resultado deseado.

### 8. Reservas de arquitectura desde Fase 0

#### Servicios y autoridad

La organización propuesta es **[inf]**, apoyada en escenas desacopladas y señales documentadas: [organización de escenas](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html).

| Servicio | Responsabilidad |
|---|---|
| `WorldState` | Estado persistente y migraciones |
| `WorldClock` | Tiempo lógico, pausas y franjas |
| `ZoneDirector` | Activación y descarga de zona |
| `InteractionService` | Validación y resolución de acciones |
| `AudioDirector` | Ambiente, música y presupuesto de voces |
| `VisualEnvironment` | Viento, cielo, nubes y uniforms |
| `AccessibilitySettings` | Movimiento, colores y preferencias |
| `QualityProfile` | Límites de efectos y representación |

Los componentes locales se comunican mediante referencias y señales locales. El bus global queda reservado para cambios que interesan a varios sistemas. [inf]

Señales propuestas:

```text
zone_entered(zone_id)
time_segment_changed(segment_id)
weather_changed(weather_state)
interaction_completed(actor_id, target_id, action_id, result)
world_state_changed(entity_id, key, value)
discovery_registered(discovery_id)
accessibility_changed(settings)
quality_profile_changed(profile_id)
```

El detalle de contacto, pasos o foco permanece local salvo necesidad concreta. [inf]

#### Capas de colisión

Propuesta [inf], usando las capas y máscaras documentadas de [física](https://docs.godotengine.org/en/4.7/tutorials/physics/physics_introduction.html):

| Número de capa | Uso |
|---:|---|
| 1 | Entorno sólido |
| 2 | Protagonista |
| 3 | Gato |
| 4 | NPC |
| 5 | Props sólidos móviles |
| 6 | Áreas interactuables |
| 7 | Disparadores de zona o misión |
| 8 | Áreas acústicas |
| 9 | Volúmenes de superficie o agua |

Los sensores consultan las capas necesarias; una comprobación de oclusión utiliza sólidos. Protagonista y gato no necesitan bloquearse mutuamente. Las capas físicas deben distinguirse de las capas visuales. [inf]

#### Grupos

Reservar `interactables`, `persistent_entities`, `reactive_props`, `scheduled_npcs`, `ambient_agents` y `quality_scalable`. Los grupos sirven para organizar y registrar; no sustituirían la detección espacial en cada fotograma. [inf] [Grupos de Godot](https://docs.godotengine.org/en/4.7/tutorials/scripting/groups.html).

#### Uniforms globales

Contrato inicial propuesto [inf]:

| Uniform | Contenido |
|---|---|
| `wind_dir_strength` | Dirección y fuerza |
| `wind_phase` | Fase temporal de ráfagas |
| `player_pos_radius` | Posición y radio de influencia |
| `cat_pos_radius` | Posición y radio de influencia |
| `player_velocity` / `cat_velocity` | Intensidad direccional |
| `world_time_01` | Hora normalizada |
| `cloud_offset` | Desplazamiento de nubes |
| `environment_motion_scale` | Intensidad de movimiento |

Deben declararse antes de compilar los shaders consumidores. `VisualEnvironment` conservaría sus valores en CPU y los escribiría en RenderingServer. [doc/inf] [Uniforms globales](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html#global-uniforms).

#### Buses de audio

Reservar nombres estables: `Master`, `Music`, `Ambience`, `SFX`, `UI`, `Voice`, `Reverb_Room` y `Reverb_Lab`. Inicialmente, los retornos de reverberación de efectos irían a SFX; música e interfaz tendrían rutas independientes. [inf]

El orden físico del panel debe respetar que los buses envían hacia buses situados a su izquierda. Renombrarlos puede romper referencias de reproductores. [doc] [Buses de audio](https://docs.godotengine.org/en/4.7/tutorials/audio/audio_buses.html).

#### Datos de zona

Esquema conceptual propuesto **[inf]**; puede editarse como Resources `.tres` y validarse como datos. [Resources](https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html).

```json
{
  "schema_version": 1,
  "zone_id": "zona_prototipo",
  "scene_id": "escena_aprobada",
  "camera_profile": "exploracion",
  "palette_id": "paleta_v1",
  "environment_profile": "exterior_calido",
  "time_profile": "cuatro_franjas",
  "wind_profile": "brisa_suave",
  "soundscape_id": "ambiente_zona",
  "music_set_id": "musica_zona",
  "acoustic_regions": [],
  "surface_regions": [],
  "npc_schedule_ids": [],
  "interaction_ids": [],
  "persistence_namespace": "zona_prototipo",
  "quality_budget_id": "hd620_inicial"
}
```

Separar definición inmutable y estado de partida. Cada entidad necesita un identificador estable, versión de esquema y valores iniciales. No usar como identidad persistente un nombre de nodo que pueda cambiar durante la edición. [inf] [Guardado](https://docs.godotengine.org/en/4.7/tutorials/io/saving_games.html).

El manifiesto de recursos debería incluir origen, modelo/parámetros IA cuando corresponda, costo, versión de paleta, transformaciones y aprobación del usuario. La validación automática revisaría referencias, identificadores, formatos y métricas; la aceptación visual y sonora seguiría pasando por su puerta de validación. [inf]

### 9. Tabla priorizada de implementación

**Impacto, costo y esfuerzo son estimaciones [inf].** “Fase” indica dónde se implementaría o completaría después de aprobar Fase 0; las reservas de arquitectura se definen ahora.

| Prioridad | Sistema | Impacto en sensación de vida | Costo de rendimiento en HD 620 | Esfuerzo | Fase del plan |
|---|---|---|---|---|---|
| P0 | Contratos, IDs y perfiles de calidad | Muy alto, habilitador | Bajo | Medio | 0 |
| P0 | Escena de medición representativa | Indirecto, decisivo | Medición | Medio | 0 |
| P1 | Foco, aviso y respuesta inmediata | Muy alto | Bajo | Medio | 6; acabado 7 |
| P1 | Persistencia visible | Muy alto | Bajo durante juego | Medio | 6 |
| P1 | Paleta y materiales comunes | Muy alto | Bajo | Medio | 1 |
| P1 | Pasos por superficie | Alto | Bajo | Bajo–medio | 3 y 4; integración 6 |
| P1 | Viento de vegetación | Alto | Bajo | Medio | 1; aplicación 5 |
| P1 | Objetos que reaccionan | Alto | Bajo | Medio | 6 |
| P1 | Ambiente por capas y estados | Muy alto | Bajo–medio de CPU | Medio | 4; aplicación 5 |
| P1 | Anticipación y seguimiento | Alto | Bajo | Medio–alto de autoría | 3 y 6 |
| P2 | Gato expresivo e interactivo | Muy alto | Bajo–medio de CPU | Alto | 3 y 6 |
| P2 | Rutinas y reacciones de NPC | Alto | Medio de CPU | Alto | 3; aplicación 5 |
| P2 | Hierba reactiva a dos actores | Alto | Bajo | Medio | 5 y 6 |
| P2 | Telas y cables | Medio–alto | Bajo | Medio | 1 y 5 |
| P2 | Música adaptativa | Alto | Medio durante fundidos | Medio | 4 |
| P2 | Hora por gradientes y franjas | Alto | Bajo | Medio | 1, 3, 4 y 5 |
| P2 | UI animada y movimiento reducido | Alto | Bajo | Medio | 6; acabado 7 |
| P3 | Insectos, hojas y aves | Medio | Bajo–medio | Medio | 5 |
| P3 | Agua y reflejos fingidos | Medio–alto | Bajo–medio | Medio | 5 |
| P3 | Nubes y sombras compartidas | Medio | Bajo–medio de GPU | Medio | 5 |
| P3 | Polvo en haces | Medio | Medio por transparencia | Bajo–medio | 5 |
| P4 | Textura con memoria de pisadas | Medio | Medio | Alto | 6, sólo si hace falta |

La distribución de fases procede del [plan maestro local](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/00_Plan_Maestro/Plan Maestro de Desarrollo AAA.pdf>). Esta propuesta adelanta contratos y criterios de prueba, sin dar por aprobada la implementación de fases posteriores.

### 10. Lista de comprobación de «mundo vivo» por escena

Lista propuesta **[inf]**, basada en los contratos anteriores.

**Causalidad e interacción**

- [ ] Los objetos que prometen una acción tienen una respuesta.
- [ ] El foco es estable y el aviso corresponde al objetivo real.
- [ ] La acción confirma éxito, bloqueo o requisito pendiente.
- [ ] Protagonista y gato no duplican acciones ni recompensas.
- [ ] Una acción importante produce un cambio perceptible y coherente.
- [ ] El estado permanece al salir, volver y cargar partida.

**Movimiento**

- [ ] Cada movimiento ambiental tiene causa, intensidad y pausa.
- [ ] Viento visual y sonoro coinciden.
- [ ] Raíces, costuras y extremos permanecen anclados.
- [ ] La hierba responde a ambos actores sin atravesar pisos.
- [ ] Personajes y gato mantienen actividad secundaria discreta.
- [ ] Los efectos lejanos o invisibles reducen su actividad.
- [ ] El modo de movimiento reducido funciona.

**Sonido**

- [ ] La escena tiene identidad ambiental reconocible.
- [ ] Los pasos corresponden a la superficie.
- [ ] Los eventos de animación coinciden con sus sonidos.
- [ ] Fuentes y oyente producen distancias comprensibles.
- [ ] Las reverberaciones cambian sin cortes bruscos.
- [ ] No hay repetición inmediata molesta ni saturación.
- [ ] La música deja oír señales importantes.
- [ ] Bucles y transiciones carecen de clics.

**Color y lectura**

- [ ] Se utiliza una versión aprobada de paleta.
- [ ] Recursos nuevos pasan revisión automática y visual.
- [ ] Personaje, gato y objetivos se distinguen del fondo.
- [ ] Las distintas horas conservan legibilidad.
- [ ] Las señales esenciales incluyen forma, símbolo o texto.
- [ ] Los materiales no contienen iluminación pintada contradictoria.

**Rendimiento y validación**

- [ ] Se midió con todos los sistemas activos.
- [ ] Se registraron tiempos de fotograma y picos.
- [ ] Transparencias, sombras, navegación y voces están presupuestadas.
- [ ] El primer uso de materiales no produce tirones durante la interacción.
- [ ] Se probó un recorrido prolongado.
- [ ] Los ajustes de calidad conservan las funciones jugables.
- [ ] Los recursos tienen trazabilidad y aprobación.
- [ ] La escena supera su puerta de validación antes de multiplicarse.

## Fuentes

Documentación consultada para Godot **4.7**, salvo AudioStreamSynchronized, cuya página accesible fue `stable`. Las fuentes oficiales de juegos más antiguos se utilizan para describir esos referentes, no como evidencia de compatibilidad actual.

- **[doc] Godot — versión y renderizado:** [4.7.2-stable](https://godotengine.org/download/archive/4.7.2-stable/), [renderizadores](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html), [Environment](https://docs.godotengine.org/en/4.7/classes/class_environment.html), [LightmapGI](https://docs.godotengine.org/en/4.7/classes/class_lightmapgi.html), [escalado](https://docs.godotengine.org/en/4.7/tutorials/3d/resolution_scaling.html).
- **[doc] Godot — efectos y rendimiento:** [shaders](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shading_language.html), [Spatial](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/spatial_shader.html), [MultiMesh](https://docs.godotengine.org/en/4.7/classes/class_multimesh.html), [partículas](https://docs.godotengine.org/en/4.7/tutorials/3d/particles/index.html), [optimización GPU](https://docs.godotengine.org/en/4.7/tutorials/performance/gpu_optimization.html), [compilación](https://docs.godotengine.org/en/4.7/tutorials/performance/pipeline_compilations.html).
- **[doc] Godot — arquitectura y animación:** [escenas](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html), [Resources](https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html), [guardado](https://docs.godotengine.org/en/4.7/tutorials/io/saving_games.html), [navegación](https://docs.godotengine.org/en/4.7/tutorials/navigation/navigation_optimizing_performance.html), [Tween](https://docs.godotengine.org/en/4.7/classes/class_tween.html), [SpringBoneSimulator3D](https://docs.godotengine.org/en/4.7/classes/class_springbonesimulator3d.html).
- **[doc] Godot — sonido:** [AudioStreamInteractive](https://docs.godotengine.org/en/4.7/classes/class_audiostreaminteractive.html), [AudioStreamPlayer3D](https://docs.godotengine.org/en/4.7/classes/class_audiostreamplayer3d.html), [Area3D](https://docs.godotengine.org/en/4.7/classes/class_area3d.html), [buses](https://docs.godotengine.org/en/4.7/tutorials/audio/audio_buses.html), [importación](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_audio_samples.html).
- **[doc] Procesamiento y accesibilidad:** [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html), [ImageMagick](https://imagemagick.org/command-line-options/), [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/), [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-fixed-colour-alone/).
- **[doc] Referentes:** [Nintendo: sonido ambiental](https://www.nintendo.com/us/whatsnew/ask-the-developer-vol-9-the-legend-of-zelda-tears-of-the-kingdom-part-1/), [Capcom: acciones de compañero](https://game.capcom.com/manual/MHST2/en/switch/page/3/3), [Bravely Default](https://www.nintendo.com/au/games/nintendo-3ds/bravely-default/), [Bravely Default II](https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/BRAVELY-DEFAULT-II-1698006.html), [Pokémon: Let’s Go](https://pokemonletsgo.pokemon.com/en-us/story/).
- **[doc, local] Plan y datos proporcionados:** [plan maestro](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/00_Plan_Maestro/Plan Maestro de Desarrollo AAA.pdf>), [matriz de costos](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md>), [costos por defecto](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_default.md>), [parámetros de modelos](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json>).