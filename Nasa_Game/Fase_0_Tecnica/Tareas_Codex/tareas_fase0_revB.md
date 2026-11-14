# Brief común — Fase 0, revisión B (objetivo AAA con PC en la nube)

Fecha: 2026-11-12. Idioma de los informes: español.

## Proyecto

RPG de aventura, simulación y exploración educativa en Godot 4.7.2 (nombre de trabajo: «Proyecto NASA-Ecuador»). Un estudiante de ingeniería de control en Guayaquil en su viaje para llegar a la NASA, con un gato científico de compañero. Cámara alta 3/4 en exploración y hub lateral tipo diorama. El tablero de referencia del usuario está en `Nasa_Game/Referencias/Tablero_usuario/` y su análisis en `Analisis del tablero.md`. Referentes de estilo: RPG de Nintendo, Monster Hunter, Pokémon, Zelda Ocarina of Time 3D y la saga Bravely. El juego debe ser original.

## Qué cambió

El usuario corrigió la restricción principal de la Fase 0 anterior (`Nasa_Game/Fase_0_Tecnica/Fase 0 - Analisis.md`), que limitaba todo a lo que rinde su portátil y proponía el renderizador Mobile a 720p. Sus palabras: «quiero que el sistema sea totalmente AAA, no quiero que te enfoques en que voy a renderizar todo aquí. Puedo alquilar PC en la nube. Valida esa opción para un videojuego totalmente impresionante, con texturas y arte innovador». También pidió un mundo que se sienta vivo: interacción con todo el entorno, movimiento ambiental sutil, sonido coherente y paleta consistente.

## Datos medidos hoy

- **Portátil local:** Intel i5-7200U (2 núcleos), 8 GB de RAM, Intel HD Graphics 620, Windows 10, conexión por Wi-Fi. Pasa a ser un terminal: edición ligera, asistentes de IA y streaming del PC en la nube.
- **Latencia desde Guayaquil** (conexión TCP, 02:22 hora local): Miami 62 ms, Atlanta 74, Chicago 93, Virginia 94, Nueva Jersey 96, Dallas 99, Ohio 118, Ciudad de México 121, Santiago de Chile 131, Los Ángeles 132, São Paulo de 153 a 193 y Oregón 164.
- **Ancho de banda:** 106 Mbps de bajada y 45 Mbps de subida contra un nodo cercano. En una sola conexión TCP, 46 Mbps desde Atlanta y 10 Mbps desde Miami.
- **Rendimiento del portátil:** `Nasa_Game/Fase_0_Tecnica/Datos/bench_render_resultados.md`. Sirve como perfil mínimo de compatibilidad.
- **Higgsfield:** 1000 créditos de suscripción que caducan al cierre del periodo (hacia el 2026-12-12). Costos en `Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.md`. Ofrece imagen, video, audio, sprites y 3D (Tripo, Hunyuan3D y Meshy) por créditos.
- **Equipo humano:** un desarrollador con asistentes de IA (Claude Code y Codex). El asistente puede operar un equipo remoto por SSH.
- **Presupuesto en dinero para la nube:** sin definir. Da escenarios.

## Reglas para ti

1. No instales nada, no descargues ejecutables y no modifiques archivos: trabajas en solo lectura y tu respuesta final es el informe.
2. No crees cuentas, no contrates servicios y no ejecutes comandos que gasten créditos de Higgsfield.
3. En las búsquedas web usa consultas técnicas genéricas: no incluyas nombres de personas ni datos del proyecto.
4. Cita la fuente de cada precio, especificación y licencia con su URL y la fecha consultada. Distingue **[doc]** (página oficial del proveedor o documentación primaria), **[sec]** (fuente secundaria) e **[inf]** (inferencia tuya). Si no pudiste verificar algo, escribe «sin verificar». No inventes precios, regiones, versiones ni licencias.
5. No reproduzcas texto con derechos de autor: resume con tus palabras.
6. No añadas al informe avisos de herramientas, mensajes de facturación ni enlaces de pago.

## Formato de tu respuesta final (Markdown compatible con Obsidian)

Usa exactamente estas secciones, en este orden:

```
# <título del informe>
## Resumen ejecutivo            (máximo 180 palabras)
## Decisiones recomendadas       (tabla: Decisión | Recomendación | Alternativa descartada y por qué | Confianza alta/media/baja)
## Afirmaciones que sostienen las decisiones   (máximo 14, numeradas, cada una con URL y etiqueta [doc]/[sec]/[inf])
## Riesgos y cómo mitigarlos
## Preguntas que debe decidir el usuario
## Desarrollo                    (el análisis completo, con subtítulos)
## Fuentes
```

@@TAREA id=11_pc_en_la_nube salida=Nasa_Game/Fase_0_Tecnica/Investigacion/11_pc_en_la_nube.md sandbox=read-only search=1 timeout=45
Valida la opción de alquilar un PC en la nube para desarrollar este juego desde Guayaquil.

1. Opciones reales hoy: PC en la nube con Windows y GPU, por hora o por mes (Shadow PC, Paperspace de DigitalOcean, AWS EC2 G4dn, G5 y G6 con DCV, Azure serie NV, Google Cloud con GPU, Vagon, AirGPU, Maximum Settings, TensorDock y otras que encuentres), y alquiler de GPU en Linux para cargas de IA (RunPod, Vast.ai, Lambda y similares). Para cada una: GPU y VRAM, precio por hora y por mes, costo del disco persistente y del tráfico de salida, regiones (¿hay Miami, Atlanta o Virginia?), si acepta clientes de Ecuador y con qué formas de pago, protocolo de streaming, si el disco persiste al apagar y límites de uso.
2. Con las latencias medidas, qué región y qué proveedor convienen. Qué latencia total esperar con Parsec, con Moonlight y Sunshine o con DCV. Requisitos de red (Mbps, cable frente a Wi-Fi) y del equipo cliente (decodificación H.264 y H.265 en una Intel HD 620).
3. Dimensionamiento: qué GPU, VRAM, RAM y disco necesitan (a) Godot 4.7 Forward+ con SDFGI y volumétricos, junto con Blender; (b) la generación local de imagen y de 3D con modelos abiertos (ComfyUI, imagen a malla). ¿Una sola máquina o dos perfiles distintos?
4. Tres escenarios de costo mensual (20, 60 y 120 horas de uso) con desglose: cómputo, disco, tráfico y licencias. Compáralos con comprar una PC de escritorio con una GPU equivalente (punto de equilibrio en meses) y con los servicios de tarifa plana.
5. Flujo de trabajo: dónde corre cada cosa (editor de Godot, Blender, Claude Code y Codex, Git y Git LFS, bóveda de Obsidian); operación por SSH desde el asistente frente a escritorio remoto; sincronización; copias de seguridad; apagado automático para no pagar horas muertas; seguridad de las credenciales.
6. Riesgos: latencia al probar un juego de acción, cortes de red, cambios de precio, disponibilidad de GPU, pérdida de datos al borrar la instancia y restricciones por país.
7. Plan de prueba de 2 a 3 horas para validar antes de comprometerse: qué medir (latencia de entrada, calidad de imagen, fps del benchmark de `pruebas/bench_render/`, tiempo de importación del proyecto) y criterios de aceptación.

Entrega una recomendación principal y una alternativa, con su costo mensual estimado.

@@TAREA id=12_render_aaa salida=Nasa_Game/Fase_0_Tecnica/Investigacion/12_render_aaa.md sandbox=read-only search=1 timeout=45
Define la pila de renderizado y de producción visual para un acabado AAA estilizado en Godot 4.7 Forward+, suponiendo que se desarrolla con una GPU dedicada.

1. Qué significa «AAA» en un RPG estilizado con cámara 3/4 y hub lateral: lista concreta de rasgos técnicos observables en los referentes (iluminación global, sombras suaves, volumetría, posproceso, densidad de vegetación, animación, VFX, agua, clima, hora del día, interfaz). Di cuáles dependen del arte y cuáles de la GPU.
2. Pila en Godot 4.7 Forward+: iluminación global (SDFGI, VoxelGI, LightmapGI con sondas: cuándo conviene cada una), niebla volumétrica, SSAO, SSIL y SSR, calidad de sombras, TAA, FSR 2 y MSAA, decals, partículas en GPU con colisión y estelas, sondas de reflexión, AreaLight3D y salida HDR. Límites conocidos de Godot frente a Unreal y Unity (sé honesto) y cómo se compensan en un juego estilizado.
3. Técnicas de arte innovador en tiempo real con implementación viable en Godot (CompositorEffect, shaders espaciales, búfer de normales): render pictórico (Kuwahara y variantes, trazos de pincel), contornos de tinta por profundidad y normales, sombreado toon con rampas y función de luz propia, tramas y medios tonos, acuarela o gouache, tilt-shift de diorama, cielos y nubes estilizados, agua estilizada, hierba interactiva densa, viento global y materiales pintados a mano que responden a la luz. Cita implementaciones públicas, charlas (GDC, SIGGRAPH) y juegos que las usan.
4. Juegos hechos en Godot 4 con acabado visual alto, y qué técnica usa cada uno.
5. Especificaciones objetivo para el jugador: propone perfil mínimo, recomendado y alto con GPU concretas, y cómo escalar con ajustes de calidad sin tocar la lógica (desde el perfil Mobile medido en una Intel HD 620 hasta Forward+ completo). Presupuestos por perfil: triángulos, texturas, luces y vegetación.
6. Qué cambia en el pipeline de recursos al subir el listón: resolución y densidad de téxel, mapas (normal, ORM, emisivo), polígonos por personaje, LOD, colisiones y formatos.
7. Novedades de Godot 4.5 a 4.7 que ayudan.

Entrega la pila recomendada por perfil de calidad y una lista de 8 a 12 «firmas visuales» candidatas para que el usuario elija en la Fase 1, cada una con su costo de GPU y de producción.

@@TAREA id=13_arte_generativo_gpu salida=Nasa_Game/Fase_0_Tecnica/Investigacion/13_arte_generativo_gpu.md sandbox=read-only search=1 timeout=45
Diseña el pipeline de texturas y arte con una GPU alquilada, combinado con los créditos de Higgsfield.

1. Modelos abiertos ejecutables hoy en una GPU de 16 a 48 GB para: imagen (concepto y texturas), materiales PBR repetibles (albedo, normal, rugosidad y altura), imagen a malla 3D con textura, retopología y UV automáticas, rig automático de bípedos y de cuadrúpedos, animación (texto o video a movimiento), ampliación de resolución, y música y efectos de sonido. Para cada uno: VRAM necesaria, calidad y licencia (¿permite el uso comercial de los resultados?). Distingue lo verificado de lo que no.
2. ComfyUI u otra orquestación: flujos concretos para (a) entrenar un LoRA de estilo con el arte aprobado del proyecto, para fijar un estilo propio y consistente; (b) texturas pintadas repetibles; (c) hojas de modelo multivista coherentes; (d) imagen → malla → textura → Godot. Da tiempos por paso y costo en horas de GPU.
3. Reparto óptimo entre Higgsfield (créditos que caducan) y la GPU alquilada (pago por hora): qué conviene hacer con cada uno y en qué orden.
4. Herramientas de acabado: Blender por script (limpieza, retopología, horneado de mapas y exportación), pintura de texturas (Blender, ArmorPaint, Material Maker) y animación (Cascadeur o similares). Di cuáles necesitan GPU.
5. Cómo lograr texturas y arte innovador de forma reproducible: dirección de estilo propia (sin imitar juegos existentes), biblioteca de materiales maestros, hojas de trim, densidad de téxel, control de valores y paleta, y validación automática.
6. Riesgos: licencias, consistencia, artefactos de las mallas generadas, tiempo de limpieza, tamaño de las descargas de modelos y almacenamiento.

Entrega un pipeline paso a paso con la herramienta, el tiempo y el costo por recurso tipo (personaje, criatura, prop, material y entorno), y la lista de modelos recomendada con su licencia.
