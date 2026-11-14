# Brief común — Fase 0 (investigación técnica, arquitectura y pipeline)

Fecha: 2026-11-12. Idioma de los informes: español.

## Proyecto

RPG de aventura, simulación y exploración educativa en Godot 4 (nombre de trabajo: «Proyecto NASA-Ecuador»). Un estudiante de ingeniería de control en Guayaquil en su viaje para llegar a la NASA. Enseña ciencia real (astrofísica, electrónica) con mecánicas, nunca como examen. Estilo 2.5D/2D-HD, música ambient/shoegaze, tipografía DotGothic16 y un gato científico de compañero. El plan maestro tiene 8 fases con puertas de validación (PDF en `Nasa_Game/00_Plan_Maestro/`).

La Fase 0 (la actual) pide:
1. Motor y renderizado: Godot 4 Forward+, SDFGI frente a lightmaps horneados para el estilo 2D-HD, y sombras 3D sobre sprites 2D.
2. Pipeline de arte con IA: mallas base con Higgsfield, retopología automática, UV y texturizado, con consistencia visual y buen rendimiento.
3. Estructura de datos: ECS frente a la orientación a objetos de Godot, Git LFS y CI/CD.

## Objetivo visual (tablero del usuario)

Hay 14 capturas en `Nasa_Game/Referencias/Tablero_usuario/`. Son de un juego hecho con IA, «After the Wind», mostrado en un video de YouTube del canal @stefan_3d_ai (marca r/TopologyAI). El usuario quiere ese nivel de acabado, no copiarlo:
- Exploración con cámara alta 3/4 (unos 50-60° de inclinación), personaje chibi (2,5 a 3 cabezas) en 3D, suelo y rocas con textura pintada a mano, hierba en mechones y sombras suaves.
- Hub en vista lateral tipo diorama 2.5D con capas de profundidad (hierba en primer plano, tiendas, montañas con perspectiva atmosférica).
- Creador de personaje (cuerpo, piel, peinado, color, barba, ojos) con vista de cara y de cuerpo completo.
- Interfaz diegética de pergamino con trazos de pincel: HUD (retrato, vida, energía, objetos), rastreador de misión, lista de combos, avisos de «Obtenido», mapa ilustrado con leyenda, pantalla de título y pantallas de carga con viñetas tipo cómic.

Referentes de estilo que nombró el usuario: RPG de Nintendo, Monster Hunter, Pokémon, Zelda Ocarina of Time 3D y la saga Bravely. El juego debe ser original: se toman principios y técnicas, nunca personajes, arte, nombres ni diseños de esos juegos.

## Restricciones duras

- **Equipo de desarrollo (medido hoy):** Intel Core i5-7200U (2 núcleos, 4 hilos), 7,9 GB de RAM, gráfica integrada Intel HD Graphics 620 (controlador 31.0.101.2140), pantalla de 1920×1080, Windows 10 Home y 27 GB libres en disco. No hay GPU dedicada. Todo lo que recomiendes debe poder desarrollarse y ejecutarse ahí.
- **Motor:** Godot 4.7.2-stable (ya descargado, firma válida).
- **Instalado:** Git, Git LFS, Python 3.13, ffmpeg 9, ImageMagick 7, .NET, VS Code, GitHub CLI y Node 24. **No instalado:** Blender ni editores de imagen.
- **Presupuesto de IA:** 1000 créditos de Higgsfield (plan Plus), sin recarga prevista. Los costos reales medidos están en `Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md` y `hf_costos_default.md`; los parámetros de cada modelo, en `hf_modelos.json`. Higgsfield ofrece imagen, video, audio y también 3D (imagen→malla con Tripo, Hunyuan3D y Meshy; remesh, retexturizado y rigging) y sprites animados (`autosprite`, con direcciones isométricas).
- Un solo desarrollador con asistentes de IA. Cada recurso pasa por una puerta de validación con el usuario.

## Reglas para ti

1. No instales nada, no descargues ejecutables y no modifiques archivos: trabajas en solo lectura y tu respuesta final es el informe.
2. No ejecutes comandos que gasten créditos de Higgsfield ni que suban archivos (`generate create`, `generate workflow`, `upload create`, etc.).
3. En las búsquedas web usa consultas técnicas genéricas: no incluyas nombres de personas ni datos del proyecto.
4. Cita la fuente de cada afirmación técnica con su URL y distingue **[doc]** (documentación primaria), **[sec]** (fuente secundaria) e **[inf]** (inferencia tuya). Si no pudiste verificar algo, escribe «sin verificar». No inventes versiones, cifras ni compatibilidades. Prefiere fuentes de 2025-2026.
5. No reproduzcas texto con derechos de autor: resume con tus palabras.

## Formato de tu respuesta final (Markdown compatible con Obsidian)

Usa exactamente estas secciones, en este orden:

```
# <título del informe>
## Resumen ejecutivo            (máximo 180 palabras)
## Decisiones recomendadas       (tabla: Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja)
## Afirmaciones que sostienen las decisiones   (máximo 12, numeradas, cada una con URL y etiqueta [doc]/[sec]/[inf])
## Riesgos y cómo mitigarlos
## Preguntas que debe decidir el usuario
## Desarrollo                    (el análisis completo, con subtítulos)
## Fuentes
```

@@TAREA id=01_motor_render salida=Nasa_Game/Fase_0_Tecnica/Investigacion/01_motor_render.md sandbox=read-only search=1 timeout=30
Investiga y recomienda la pila de renderizado en Godot 4.7 para este proyecto y este equipo.

1. Renderizadores Forward+, Mobile y Compatibility en Godot 4.7: qué ofrece cada uno (SDFGI, VoxelGI, LightmapGI, SSAO, SSIL, SSR, niebla volumétrica, decals, glow, DOF, MSAA/TAA/FSR, sombras) y cuáles son viables en una Intel HD 620 (soporte de Vulkan, D3D12 y OpenGL; problemas conocidos de los controladores Intel de 7.ª generación con Godot 4).
2. Iluminación global: SDFGI, LightmapGI horneado, VoxelGI o sin GI (luz ambiente, luz de relleno y oclusión falsa). Requisitos para hornear lightmaps en este equipo (¿el horneado necesita GPU con Vulkan o compute?, ¿funciona si el proyecto usa Compatibility?, tiempos, UV2) y limitaciones de SDFGI (¿cámara ortogonal?, costo).
3. Sombras de sprites 2D sobre un mundo 3D (estilo HD-2D): Sprite3D y AnimatedSprite3D con billboard, alpha cut (discard u opaque prepass), proyección de sombra, el problema de que la sombra gire con el billboard y sus soluciones (malla proxy solo-sombra, sombra blob con Decal o quad, doble sprite), orden de transparencias y z-fighting.
4. Cámara para la vista 3/4 alta y para el hub lateral tipo diorama: ortogonal o perspectiva con FOV bajo, inclinación, desenfoque tilt-shift (DOF de CameraAttributes: en qué renderizadores existe), ajuste para evitar el temblor de sprites, resolución base y modo de stretch (1920×1080 frente a 1280×720 escalado), escalado 3D o FSR para la HD 620.
5. Sombreado estilizado: toon/cel con rim light (modos toon y rim de StandardMaterial3D frente a ShaderMaterial con `light()`), contornos (casco invertido, `next_pass`, posproceso por profundidad y normales), texturas pintadas a mano con bordes duros (flat shading), hierba en mechones (MultiMeshInstance3D, viento por shader) y agua estilizada.
6. Presupuesto de rendimiento para la HD 620 a 720p y 1080p: triángulos, draw calls, luces con sombra, tamaño del atlas de sombras, materiales transparentes y qué efectos apagar.
7. Novedades de Godot 4.4 a 4.7 relevantes para lo anterior.

Entrega además una pila recomendada (principal y plan B) y el diseño de una prueba de rendimiento que confirme la decisión en este equipo (escenas, métricas y umbrales de aceptación).

@@TAREA id=02_pipeline_personajes salida=Nasa_Game/Fase_0_Tecnica/Investigacion/02_pipeline_personajes.md sandbox=read-only search=1 timeout=30
Define el pipeline de personajes, criaturas y props desde Higgsfield hasta Godot, y decide cómo se representan los personajes.

Lee antes (archivos locales): en `C:\Users\guill\.agents\skills\higgsfield-websites\references\` los archivos `game-3d-animation.md`, `game-2d-animation.md`, `game-meshy-api.md`, `game-meshy-input-rules.md`, `game-procedural-animation.md`, `game-stylization.md`, `game-textures.md` y `game-flow.md`; y en `C:\Users\guill\.agents\skills\higgsfield-websites\scripts\` los scripts `pipeline.py`, `rig_transfer.py`, `glb_merge_anims.py`, `fbx2glb.py`, `glb_inspect.py` y `seamless.py`. Lee también `Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json` (parámetros de `image_to_3d`, `multi_image_to_3d`, `meshy_v7_image_to_3d`, `hunyuan3d_v3_image_to_3d`, `tripo_h3_1_image_to_3d`, `tripo_h3_1_multiview_to_3d`, `tripo_p2_image_to_3d`, `3d_rigging`, `meshy_v5_remesh`, `meshy_v5_retexture`, `sam_3_3d`, `autosprite` y `3d_jutsu_angles`) y la matriz de costos.

1. Compara con una matriz de puntuación (fidelidad al tablero, viabilidad en la HD 620, costo en créditos, consistencia entre direcciones, flexibilidad de animación, trabajo manual y riesgo) estas opciones para el protagonista, el gato y los NPC: (A) sprites 2D generados con `autosprite` (direcciones iso up, northeast, right, southeast y down; espejo para las otras tres) sobre billboard; (B) modelo 3D generado (imagen→3D) con rig y animaciones, en tiempo real; (C) modelo 3D renderizado a hojas de sprites en 8 direcciones; (D) híbrido.
2. Para la vía 3D: qué modelo de Higgsfield conviene por tipo de recurso (personaje chibi, gato cuadrúpedo, prop duro, vegetación, edificio) y con qué parámetros (pose A o T, simetría, `target_polycount`, topología, textura, remesh); cómo preparar la imagen de entrada (vistas ortográficas, fondo liso, luz neutra, multivista coherente); fallos típicos de las mallas generadas (manos, pelo, capas, texturas con luz horneada) y cómo corregirlos.
3. Rig y animación: `3d_rigging` y los `animation_action_id` (biblioteca de animaciones) frente a Mixamo, AccuRIG y Cascadeur; retargeting; cuadrúpedos; fusión de varios clips en un GLB; importación en Godot 4.7 (glTF, AnimationLibrary, AnimationTree, retarget con BoneMap y SkeletonProfile).
4. Limpieza sin GPU dedicada: qué se puede automatizar con Blender por script en este equipo (¿qué versión de Blender corre en una HD 620?), retopología automática (QuadriFlow, Instant Meshes, decimate) frente a `meshy_v5_remesh`, UV, horneado y material toon; o cómo evitar Blender usando solo los parámetros de Higgsfield y los scripts de la skill.
5. Presupuestos por recurso (triángulos, tamaño de textura, huesos) acordes a la HD 620.
6. Para la vía de sprites: resolución de cuadro, cuadros por animación, empaquetado en atlas, problemas de consistencia y parpadeo de `autosprite` según `video_tier`, mapa de normales para iluminar sprites y sombras.

Entrega la recomendación con un plan de prueba A/B mínimo (qué generar, con qué modelo y cuántos créditos) para validar la decisión con el usuario antes de producir en serie, y el pipeline paso a paso con la herramienta de cada paso.

@@TAREA id=03_higgsfield_arte2d salida=Nasa_Game/Fase_0_Tecnica/Investigacion/03_higgsfield_arte2d.md sandbox=read-only search=1 timeout=30
Diseña la estrategia de producción de arte 2D y de gasto de créditos con Higgsfield.

Lee antes (archivos locales): `C:\Users\guill\.agents\skills\higgsfield-generate\SKILL.md` y, en su carpeta `references\`, `model-catalog.md`, `prompt-engineering.md`, `media-inputs.md`, `workflows.md` y `troubleshooting.md`; en `C:\Users\guill\.agents\skills\higgsfield-websites\references\`, `game-design-system.md`, `game-stylization.md`, `game-textures.md`, `game-audio.md` y `reference-boards.md`; en `C:\Users\guill\.agents\skills\higgsfield-brandkit\references\`, `logo.md` y `concept-boards.md`; y `C:\Users\guill\.agents\skills\higgsfield-soul-id\SKILL.md`. Lee también los tres archivos de `Nasa_Game/Fase_0_Tecnica/Datos/` (costos y parámetros).

1. Qué modelo usar para cada entregable y por qué (calidad, control por referencias, texto legible, fondo transparente, costo): exploración de estilo, concept de personaje, hoja de modelo o turnaround ortográfico (frente, 3/4, perfil y espalda), hoja de expresiones, hoja de props, concept de entorno, texturas repetibles pintadas a mano, capas de parallax, cielos, iconos y kit de interfaz, logotipo, mapa ilustrado, viñetas de carga y retratos de diálogo. Considera `3d_jutsu_angles`, `nano_banana_pro` (hasta 14 referencias), `gpt_image_2_6` (calidades low a max, fondo transparente), `seedream_5_5`, `flux_kontext`, `soul_location`, `recraft_v4_1`, `ideogram_vector`, `image_background_remover`, los upscalers y `nano_banana_2_relight`.
2. Cómo mantener la consistencia de estilo y de personaje entre generaciones (imágenes de referencia, hoja maestra, biblia de prompts con bloques fijos, Soul ID si sirve para personajes estilizados, edición por referencia) y qué no funciona.
3. Protocolo de iteración que minimice el desperdicio: borradores baratos (qué modelo y calidad), criterio para pasar a calidad final, lotes, cuándo reintentar y cuándo editar.
4. Audio con los mismos créditos: música (`sonilo_music`, `elevenlabs_music_v2` y `v2_5`), efectos (`mirelo_text_to_audio`) y voz; cuánto reservar.
5. Video: en qué casos vale la pena (tráiler, cinemática, VFX convertido a hoja de sprites, fondos animados) y cuánto cuesta.
6. Tres escenarios de presupuesto para 1000 créditos (conservador, equilibrado y ambicioso) para llegar a un vertical slice: 1 protagonista, 1 gato, 6 NPC, 1 hub lateral, 1 zona de exploración 3/4, 40 props, kit de interfaz, logotipo, mapa, 5 pistas de música y 30 efectos; con reserva de contingencia y desglose por partida.
7. Derechos de uso comercial de lo generado y restricciones de contenido según los términos vigentes de Higgsfield y de los modelos de terceros (búscalo en la web y cita).

Entrega además una plantilla de «registro de generación» (modelo, parámetros, prompt, referencias, costo, resultado y veredicto) para la trazabilidad.

@@TAREA id=04_caso_after_the_wind salida=Nasa_Game/Fase_0_Tecnica/Investigacion/04_caso_after_the_wind.md sandbox=read-only search=1 timeout=25
Reconstruye cómo se hizo el juego del tablero y qué lecciones deja.

1. Localiza el video de YouTube del canal @stefan_3d_ai en el que muestra el juego «After the Wind» (título aproximado en español: «Hice un juego con un plan de IA de $20...», 34 minutos) y las publicaciones relacionadas (r/TopologyAI u otras). Extrae: motor o framework; modelos y herramientas de IA usados para código, modelos 3D, texturas, animaciones, interfaz y audio; tiempo y costo declarados; qué hizo la IA sola y qué corrigió el autor; y los problemas que reporta.
2. Busca otros casos documentados de 2025-2026 de juegos 3D estilizados o HD-2D hechos principalmente con IA (agentes de código más generación de assets): pipelines, herramientas y, sobre todo, qué falló.
3. Deduce del tablero (puedes abrir las 14 imágenes) las técnicas visuales concretas: tipo de cámara, proporciones del personaje, tratamiento de texturas, hierba, sombras, composición del hub lateral y estilo de interfaz.
4. Traduce todo a recomendaciones aplicables a Godot 4.7 en un equipo con gráfica integrada.

Si no encuentras el video o un dato, dilo: no rellenes con suposiciones.

@@TAREA id=05_referencias_aaa salida=Nasa_Game/Fase_0_Tecnica/Investigacion/05_referencias_aaa.md sandbox=read-only search=1 timeout=30
Deconstruye las técnicas de arte de los referentes para extraer principios aplicables (no para copiar).

Referentes: Monster Hunter Stories 1 y 2; Pokémon (Let's Go, el remake de Diamante y Perla, Leyendas Arceus, Espada y Escudo); The Legend of Zelda: Ocarina of Time 3D, Link's Awakening (2019) y Echoes of Wisdom; Bravely Default, Bravely Second y Bravely Default II; Octopath Traveler y Triangle Strategy (HD-2D); Ni no Kuni.

Para cada uno: cámara (ángulo, ortogonal o perspectiva, FOV, tilt-shift), proporciones del personaje en cabezas, modelado y polígonos aproximados, sombreado (cel, rampas, rim, contorno), texturas (pintadas a mano, densidad de téxel), paleta y valores, iluminación (horneada o dinámica), tratamiento de fondos (pintados, dioramas, parallax), lenguaje de interfaz y tipografía, y la decisión técnica que hace posible ese aspecto en hardware modesto (3DS o Switch).

Luego sintetiza: (a) de 12 a 15 principios transferibles a un RPG ambientado en una ciudad tropical contemporánea y en instalaciones espaciales; (b) una tabla «tomar / adaptar / evitar»; (c) los límites de propiedad intelectual: qué elementos son estilo general y cuáles son expresión protegida que no debe imitarse; (d) tres direcciones de arte originales que combinen esos principios con una paleta cálida (ciudad) frente a una fría (centros espaciales), para que el usuario elija en la Fase 1.

Usa charlas de GDC, entrevistas a desarrolladores, reseñas de artbooks y análisis técnicos; cita las URL.

@@TAREA id=06_arquitectura_godot salida=Nasa_Game/Fase_0_Tecnica/Investigacion/06_arquitectura_godot.md sandbox=read-only search=1 timeout=30
Define la arquitectura de software, la estructura del repositorio y la cadena de herramientas en Godot 4.7.2.

1. ECS frente a composición con nodos y Resources: estado de los complementos ECS para Godot 4 y cuándo valen la pena; recomendación para un RPG con pocos cientos de entidades. Patrón de componentes con nodos, datos en Resources personalizados, autoloads mínimos, bus de eventos con señales e inyección de dependencias sencilla.
2. Máquinas de estado: FSM o HSM propias frente a complementos (Godot State Charts, LimboAI) y su compatibilidad con 4.7.
3. GDScript tipado, C# (hay .NET instalado) o GDExtension: recomendación y reglas de estilo (gdtoolkit: gdlint y gdformat).
4. Guardado: Resources, JSON o binario; riesgo de ejecutar código al cargar Resources de una partida; versionado y migración de partidas.
5. Diálogos y localización: Dialogue Manager frente a Dialogic 2 (estado en 4.7), i18n con CSV o gettext, español e inglés. Tipografía DotGothic16: licencia y cobertura de glifos del español (á é í ó ú ñ ü ¿ ¡); si no los cubre, alternativas de píxel o punto con licencia libre.
6. Cámara (Phantom Camera: estado en 4.7), navegación del gato (NavigationServer 3D o 2D, agentes, evitación), entrada (buffer de entrada, coyote time) y audio adaptativo (FMOD por GDExtension, Wwise o nativo con AudioStreamInteractive, AudioStreamSynchronized, buses y reverb por zona): recomendación para un solo desarrollador.
7. Estructura de carpetas del proyecto de Godot y del repositorio (el proyecto convive con una bóveda de Obsidian `Nasa_Game/` y una carpeta `herramientas/`), convenciones de nombres, ajustes de importación, `.gitignore`, `.gitattributes` con Git LFS (qué extensiones) y límites de LFS en GitHub.
8. Pruebas automáticas (GUT o gdUnit4 en 4.7), ejecución headless, CI/CD con GitHub Actions (exportación para Windows, plantillas de exportación, caché) y publicación opcional en itch.io.
9. Accesibilidad desde la arquitectura: remapeo de controles, escalado de texto, modos de daltonismo por shader y reducción de movimiento.

Entrega el árbol de carpetas propuesto, la lista de complementos con versión compatible verificada y licencia, y un registro de decisiones (ADR) de una línea por decisión.

@@TAREA id=07_proceso_estudio salida=Nasa_Game/Fase_0_Tecnica/Investigacion/07_proceso_estudio.md sandbox=read-only search=1 timeout=30
Diseña el proceso de producción y validación de arte «de estudio» adaptado a un desarrollador que trabaja con IA generativa.

1. Entregables de preproducción de un estudio AAA y su contenido estándar: biblia de arte, guía de estilo, hoja de modelo o turnaround (vistas, anotaciones, proporciones en cabezas, paleta con valores hex, materiales), hoja de expresiones y poses, hoja de props con escala, lineup de escala, concept de entorno, color script, claves de iluminación, y style frames de interfaz y de VFX. Qué debe llevar cada uno para considerarse aprobable.
2. Puertas de revisión por tipo de recurso con una lista de comprobación objetiva: silueta, lectura en escala de grises (valores), cumplimiento de paleta, proporciones, legibilidad a la distancia de la cámara de juego, densidad de téxel, coherencia de luz y presupuesto técnico. Incluye cómo medir cada criterio (por ejemplo con ImageMagick o Python).
3. Etapas de un recurso (concepto → hoja aprobada → blockout → modelo o sprite → textura → rig y animación → integración en motor → pulido) y qué se valida en cada una.
4. Manifiesto de recursos: campos (ID, tipo, fase, estado, modelo de IA, prompt, referencias, semilla si existe, costo en créditos, archivo fuente, archivo en motor, veredicto y fecha), convención de nombres y versiones.
5. Cómo adaptar la dirección de arte a la IA generativa: biblia de prompts con bloques de estilo fijos, imágenes ancla, control de la deriva de estilo, criterios de rechazo y límite de reintentos por recurso para proteger el presupuesto de 1000 créditos.
6. Definición de vertical slice y de «terminado» para este proyecto; riesgos de producción y mitigaciones.
7. Cómo presentar cada recurso al usuario para que lo valide rápido (lámina comparativa con la referencia, vista en motor con la cámara real, lista de comprobación con semáforo).

Entrega plantillas listas para usar en Markdown (compatibles con Obsidian): ficha de recurso, lista de comprobación de puerta, hoja de modelo y registro de créditos.

@@TAREA id=08_antecedentes salida=Nasa_Game/Fase_0_Tecnica/Investigacion/08_antecedentes_boveda_anterior.md sandbox=read-only search=0 timeout=25 cwd=C:\Users\guill\Desktop\Juego\Juego_2d-hd
Resume el trabajo previo de este mismo juego que está en `C:\Users\guill\Desktop\Juego\Juego_2d-hd` (una bóveda de Obsidian y repositorio Git anteriores). Trabaja en solo lectura.

Lee: `0_Reglas_Globales` (`index.md`, `log.md`, `validacion-claude-2026-11-09.md`); `1_Mecanicas_y_Codigo` (`README.md`, `solicitudes-arte.md` y la estructura del proyecto de Godot en `godot/`: `project.godot`, escenas, scripts y complementos); `2_Arte_e_Interfaz` (`arte e Historia.md`, `avatar.md`, `direccion-artistica.md`, `mascota-cientifica.md`, `primera-escena.md`; describe las imágenes PNG y las carpetas `kit-habitacion`, `referencias` y `storyboard`); `3_Guion_y_Mundo` (`historia.md`, `guion-video-30s.md`); `.tools`, `raw` y el historial de Git (`git log`).

Entrega: (1) las decisiones ya tomadas (historia, protagonista, gato, dirección de arte, paleta, tipografía, motor, renderizador, estructura); (2) el inventario de recursos existentes con ruta y estado; (3) el estado del proyecto de Godot (versión, renderizador configurado, escenas, scripts, qué funciona); (4) qué validó o criticó la revisión del 2026-11-09; (5) los pendientes y problemas abiertos; (6) qué conviene reutilizar tal cual, qué rehacer y qué descartar a la luz del nuevo objetivo visual del brief; (7) las contradicciones entre ese trabajo previo y el plan maestro actual.

@@TAREA id=10_mundo_vivo salida=Nasa_Game/Fase_0_Tecnica/Investigacion/10_mundo_vivo.md sandbox=read-only search=1 timeout=30
El usuario fijó este pilar de calidad: «El juego debe sentirse vivo: interacciones de alto nivel con todo su entorno, movimientos sutiles del ambiente, sonidos coherentes y paleta de colores consistente». Define cómo lograrlo en Godot 4.7 dentro del presupuesto de una Intel HD 620, y qué debe prever la arquitectura desde la Fase 0.

1. Movimiento ambiental barato: viento por vertex shader en vegetación, telas y cables; hierba que se dobla al paso del personaje (uniform global con la posición o textura de desplazamiento); partículas (GPUParticles3D frente a CPUParticles3D según el renderizador); polvo en haces de luz, hojas, insectos y aves como agentes baratos; agua y reflejos falsos; parpadeo de luces; nubes y sombras de nube proyectadas; ciclo de hora del día con gradientes; movimiento secundario del personaje y del gato (cola, orejas, respiración). Da el costo de cada técnica y di cuáles funcionan en Compatibility, Mobile y Forward+.
2. Interacción con el entorno: sistema de interacción por componentes (detección, prioridad, aviso en pantalla, resaltado por shader), respuestas físicas ligeras (objetos que se tambalean, puertas, interruptores, pantallas que reaccionan), estados persistentes del mundo, NPC con rutinas y reacciones al jugador, y el gato como segundo punto de interacción. Explica cómo lo resuelven los referentes (Zelda, Monster Hunter Stories, Bravely, Pokémon) y qué es viable para un solo desarrollador.
3. «Game feel»: anticipación y seguimiento en las animaciones, squash and stretch, hit stop, sacudida de cámara con opción de reducir el movimiento, respuesta inmediata de la interfaz y tweens. Lista priorizada por impacto y costo.
4. Sonido coherente: guía de estilo sonoro, capas de ambiente por zona, pasos según la superficie, audio posicional, reverb por zona con buses, música adaptativa con AudioStreamInteractive, niveles de sonoridad (LUFS) y formato de archivos. Explica cómo lograr coherencia cuando los efectos y la música se generan con IA (familias de prompts, posprocesado común con ffmpeg).
5. Paleta consistente: paleta maestra como recurso de datos, rampas compartidas para el sombreado toon, gradación de color y LUT en el Environment (qué renderizadores lo admiten), comprobación automática de la paleta en cada recurso (ImageMagick o Python), remapeo de paleta para los modos de daltonismo y cómo corregir la deriva de color de las imágenes generadas con IA.
6. Qué debe reservar la arquitectura desde ya: señales globales, capas de colisión, grupos, uniforms globales de shader, buses de audio y formato de datos de zona.

Entrega una tabla priorizada (impacto en la sensación de vida, costo de rendimiento en la HD 620, esfuerzo y fase del plan maestro en la que se implementa) y una lista de comprobación de «mundo vivo» para aplicar a cada escena.

@@TAREA id=09_bench_render salida=Nasa_Game/Fase_0_Tecnica/Investigacion/09_bench_render_instrucciones.md sandbox=workspace-write search=1 timeout=30 brief=0
Crea un proyecto mínimo de Godot 4.7 para medir el rendimiento de los renderizadores en `pruebas/bench_render/`. Escribe archivos solo dentro de esa carpeta. No ejecutes Godot, no instales nada y no descargues nada. El equipo de destino es un Intel i5-7200U con gráfica integrada Intel HD 620 y Windows 10.

Requisitos:
- `project.godot` válido para Godot 4.7 (config_version 5), ventana de 1280×720, vsync desactivado y escena principal `bench.tscn`.
- `bench.gd`: construye la escena por código según los argumentos de usuario que van después de `--`: `--escena=base|hierba|sprites|sdfgi`, `--segundos=N` (12 por defecto) y `--salida=ruta.json`.
  - `base`: suelo de 60×60 m con un material con textura procedural (NoiseTexture2D); 150 mallas (cajas, esferas y cilindros) con StandardMaterial3D en modo toon; DirectionalLight3D con sombras; WorldEnvironment con cielo procedural y luz ambiente; cámara en vista 3/4 (inclinación de −55°, perspectiva con FOV de 30°) que orbita despacio.
  - `hierba`: lo anterior más un MultiMeshInstance3D con 40 000 briznas (quads cruzados) con shader de viento.
  - `sprites`: la escena `base` más 200 Sprite3D en billboard con textura generada por código, alpha cut en discard y proyección de sombra.
  - `sdfgi`: la escena `base` con SDFGI, SSAO y glow activados en el Environment.
  - Tras 3 s de calentamiento mide durante N segundos: FPS medio, FPS del 1 % más lento, tiempo de cuadro medio y máximo (con `Time.get_ticks_usec()` por cuadro), draw calls y primitivas, memoria de video usada, nombre del adaptador, versión de la API gráfica y método de renderizado en uso. Escribe el JSON en `--salida` y cierra con `get_tree().quit()`.
- `correr_bench.py` (Python 3.13, solo biblioteca estándar): recibe la ruta del ejecutable de Godot. Para cada combinación de método {forward_plus, mobile, gl_compatibility} × escena × resolución {1280x720, 1920x1080} lanza Godot con el método de renderizado, la resolución y los argumentos de usuario; aplica un tiempo límite por corrida; recoge los JSON y escribe `resultados.json` y `resultados.md` (tabla). Debe tolerar que una combinación falle o se cuelgue (la termina, registra el error y sigue). Opción `--rapido` para correr solo 1280x720 con 6 s de medición. La escena `sdfgi` solo se corre con forward_plus.

Verifica en la documentación de Godot 4.7 los nombres exactos de la API y de los argumentos de línea de comandos (`--rendering-method`, `--rendering-driver`, `--resolution`, `--path`, `--` para los argumentos de usuario y `OS.get_cmdline_user_args()`), y las constantes de `RenderingServer.get_rendering_info()`. Los comentarios del código van sin tildes. Tu respuesta final: 10 líneas que expliquen cómo ejecutarlo y qué archivos creaste.
