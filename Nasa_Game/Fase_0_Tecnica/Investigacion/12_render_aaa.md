---
tipo: investigacion
fase: 0
revision: B
tarea: 12_render_aaa
fecha: 2026-11-12
---

# Fase 0 revB — Pila de render y producción visual para un acabado AAA estilizado en Godot 4.7 Forward+

## Resumen ejecutivo

Con GPU dedicada, **Forward+ sobre D3D12** pasa a ser el renderizador de producción y Mobile queda como perfil de compatibilidad para gráficas integradas (medido: 42 fps a 720p en la HD 620). Godot 4.7 cubre lo que un RPG estilizado necesita: GI en tres modalidades, niebla volumétrica, SSAO/SSIL/SSR, sombras suaves, partículas en GPU con colisión, decals, luces de área y salida HDR. **No** iguala a Unreal en geometría virtualizada, GI dinámica completa, trazado de rayos, escaladores de fabricante ni streaming de texturas; con cámara 3/4, mundo por zonas y arte pintado esas carencias pesan poco. [inf]

El «AAA» de los referentes depende más de dirección de arte, animación y coherencia que de la GPU. La apuesta recomendada es **GI híbrida** (LightmapGI en hub e interiores, SDFGI en exteriores del perfil alto) y **una firma visual propia** construida con `CompositorEffect` y shaders espaciales, elegida entre las doce candidatas del final. Ningún juego publicado en Godot 4 demuestra esta pila completa: hay que probarla con un corte vertical propio.

## Decisiones recomendadas

| Decisión | Recomendación | Alternativa descartada y por qué | Confianza |
|---|---|---|---|
| Renderizador | Forward+ con D3D12; Mobile como perfil de compatibilidad | Mobile o Compatibility como base: sin SDFGI, volumétricos, SSR ni búfer de normales | Alta |
| GI | Híbrida: LightmapGI + sondas en hub e interiores; SDFGI en exteriores (perfil alto); SSIL opcional | SDFGI en todo: fugas, cascadas e incidencia abierta con cámara ortogonal | Media |
| Cámara del hub | Perspectiva de FOV bajo (10–20°) en lugar de ortogonal | Ortogonal: riesgo con SDFGI y sin DOF natural de diorama | Media |
| Antialiasing | MSAA 4× + SMAA en recomendado; FSR 2.2 solo para escalar | TAA por defecto: emborrona contornos y trazos de la firma | Media |
| Posproceso propio | `CompositorEffect` con cómputo; efectos encapsulados y con interruptor | `ColorRect` con `SCREEN_TEXTURE`: sin normales ni control de etapa | Media |
| Sombras de la firma | `light()` propio con rampas en pocas familias de material | Material estándar toon: no permite teñir ni tramar la sombra | Alta |
| Texturas | 2K como norma, 4K solo en atlas de terreno; presupuesto de VRAM por zona | Suponer streaming: no existe en 4.7 estable | Alta |
| Vegetación | Brizna por instancia en MultiMesh por parcelas + viento global | Tarjetas alfa grandes: sobredibujo y aspecto genérico | Media |
| Firma visual | Elegir 1 principal y 2 de apoyo en Fase 1 tras ver prototipos | Activar todas: costo de GPU y de producción inasumible para una persona | Alta |
| Validación | Corte vertical medido en la GPU alquilada (tarea 11) antes de producir | Aprobar por capturas o por demos ajenas | Alta |

## Afirmaciones que sostienen las decisiones

1. **[doc]** SDFGI, VoxelGI, SSIL, SSR, niebla volumétrica, TAA y FSR solo existen en Forward+; el búfer de normales y rugosidad también. [F1], informe `01_motor_render` §2.
2. **[doc]** La guía de GI ordena el costo de menor a mayor: ReflectionProbe, LightmapGI, VoxelGI, SSIL, SDFGI. Para escritorio propone empezar con SDFGI y ofrecer su desactivación; LightmapGI da la mejor luz indirecta pero es estática. [F2]
3. **[doc]** SDFGI no admite oclusores dinámicos, sufre fugas y saltos de cascada, y mantiene abierta una incidencia con cámara ortogonal. [F2], [F3]
4. **[doc]** El reemplazo de SDFGI (HDDAGI, PR 119869) sigue abierto con hito «4.x»; última actividad vista: 2026-08-30. No está en 4.7. [F4]
5. **[doc]** La niebla volumétrica tiene alcance finito, dispersión simple y fantasmas por reproyección temporal; los `FogVolume` aceptan shaders propios. [F5]
6. **[doc]** `CompositorEffect` ofrece cinco etapas (de pre-opaco a pos-transparente), acceso a color, profundidad, velocidad y, solo en Forward+, normales/rugosidad y especular separado. La clase está marcada como experimental. [F6], [F7]
7. **[doc]** Los escaladores documentados son bilineal, nearest, FSR 1 y FSR 2.2; FSR 2 sustituye a TAA y es el más caro. La página no menciona DLSS ni XeSS. [F8]
8. **[doc]** Godot 4.7 añade `AreaLight3D`, salida HDR y correcciones de clearcoat. En Windows el HDR exige D3D12 y Mobile o Forward+; Filmic y ACES quedan como tonemappers solo SDR. [F9], [F10]
9. **[doc]** 4.5 aporta búfer de plantilla (stencil), horneado de shaders en exportación, SMAA, mapas de normales dobladas y oclusión especular; 4.6 reescribe SSR, abarata las sondas, añade IK y mejora los LOD generados. [F11], [F12]
10. **[doc]** El streaming de texturas por nivel de mip aparece en 4.8 dev 5 (2026-09-10), sin fecha de versión estable. [F13]
11. **[doc]** El LOD automático se genera al importar, puede dar defectos en mallas con esqueleto y asigna un único nivel a todo un MultiMesh; los rangos de visibilidad permiten HLOD manual. [F14], [F15]
12. **[doc]** Hay implementaciones públicas con licencia MIT: contornos por campos de distancia con `CompositorEffect`, Kuwahara generalizado, hierba por brizna, nubes volumétricas en shader de cielo, océano FFT por cómputo y terreno con 32 texturas y 10 LOD. [F16]–[F21]
13. **[doc]** Encuesta de Steam de octubre de 2026: RTX 3060 y RTX 5070 empatan en 3,78 %; RTX 4060 3,51 %; GTX 1650 2,44 %. VRAM oficial: 12/8, 12, 8 y 4 GB. Godot recomienda como mínimo dedicado una GTX 1050 o RX 460. [F22], [F23], [F24]
14. **[inf]** En la HD 620, Forward+ con SDFGI rinde 19,7 fps a 720p y Mobile con 573 000 primitivas, 42 fps: la GI dinámica queda fuera del perfil de compatibilidad. Datos locales `bench_render_resultados.md`.

## Riesgos y cómo mitigarlos

| Riesgo | Mitigación |
|---|---|
| No hay juego publicado en Godot 4 que demuestre la pila completa | Corte vertical en el primer mes: una zona exterior y el hub, con medición por perfil |
| API de `CompositorEffect` experimental | Fijar 4.7.2; un efecto por archivo con interruptor; alternativa por shader espacial o casco invertido |
| Artefactos de SDFGI y horneados lentos | Lightmaps donde la luz es fija; SDFGI solo en exteriores y desactivable; revisar HDDAGI cuando se integre |
| VRAM sin streaming de texturas | Presupuesto por zona, carga por áreas, tope 2K y compresión BPTC/S3TC |
| Efectos pictóricos que parpadean o dejan estelas con AA temporal | MSAA + SMAA; filtrar fondos y no personajes mediante stencil; probar en movimiento |
| Divergencia visual entre Forward+ y Mobile | Capturas de referencia por perfil y prueba automática al cambiar materiales |

## Preguntas que debe decidir el usuario

1. ¿Qué familia de firma visual prefieres como principal: tinta y toon, pictórica o diorama fotográfico?
2. ¿Hora del día continua (obliga a GI dinámica) o estados discretos (permite lightmaps por estado)?
3. ¿El perfil para gráficas integradas se publica o solo sirve para desarrollo?
4. ¿Objetivo del perfil recomendado: 1080p o 1440p a 60 fps?
5. ¿Aceptas el hub en perspectiva de FOV bajo en lugar de ortogonal?
6. ¿La salida HDR entra en el lanzamiento o queda como mejora posterior?

## Desarrollo

### 1. Qué significa «AAA» en un RPG estilizado

Fecha de consulta de todas las fuentes: 2026-11-12. La atribución de rasgos a los referentes es **[inf]**: sus motores y técnicas internas están sin verificar.

| Rasgo observable | Depende sobre todo de | En Godot 4.7 |
|---|---|---|
| Luz indirecta con color y rebote | GPU + iluminación artística | LightmapGI, SDFGI, VoxelGI |
| Sombras suaves con contacto | GPU | PCSS, SSAO |
| Atmósfera: rayos, niebla de valle | GPU | Niebla volumétrica, `FogVolume` |
| Posproceso con identidad | Arte + GPU | Glow, DOF, tonemapper, `CompositorEffect` |
| Vegetación densa que reacciona | GPU + shader | MultiMesh, viento en vértices |
| Animación con peso y transiciones | Arte (casi todo) | AnimationTree, IK de 4.6 |
| VFX legibles y con estela | Arte + GPU | GPUParticles3D con colisión, estelas y atractores |
| Agua, clima y hora del día | Arte + shader | Shaders espaciales y de cielo |
| Paleta, siluetas y composición | Arte | — |
| Interfaz nítida y animada | Arte | Control a resolución nativa |
| Carga sin tirones | Ingeniería | Ubershaders, horneado de shaders |

Conclusión **[inf]**: la GPU compra atmósfera, densidad y resolución; la sensación de superproducción la deciden animación, VFX, sonido y coherencia, que son trabajo de arte.

### 2. Pila en Godot 4.7 Forward+

| Componente | Uso recomendado [inf] | Límite documentado [doc] |
|---|---|---|
| LightmapGI + sondas | Hub, interiores, zonas de luz fija | Estática; exige UV2 [F2] |
| SDFGI | Exteriores con hora del día, perfil alto | Sin oclusores dinámicos; fugas [F2] |
| VoxelGI | Interiores pequeños con luces móviles | Fugas en muros finos [F2] |
| SSIL / SSAO | Detalle de contacto en perfil alto | Costo moderado, media resolución [F2] |
| SSR | Agua y suelos mojados | Espacio de pantalla; reescrita en 4.6 [F12] |
| Sondas de reflexión | Reflejo base en toda escena | Octaédricas desde 4.6 [F12] |
| Niebla volumétrica | Rayos de luz, bruma, polvo | Alcance finito, fantasmas [F5] |
| Decals | Suciedad, charcos, sombras blob | Agrupados, sin límite por malla en Forward+ [F25] |
| Partículas GPU | Polen, hojas, chispas | Colisión con caja, esfera, SDF horneado y mapa de alturas [F25] |
| `AreaLight3D` | Ventanas, pantallas, letreros | Más cara que omni y spot (informe 01) |
| Salida HDR | Perfil alto en monitores compatibles | D3D12; sin Filmic ni ACES [F10] |
| MSAA, TAA, FSR 2.2, SMAA | Ver decisiones | FSR 2 anula TAA [F8] |

**Límites frente a Unreal y Unity, sin maquillar:**

| Carencia en Godot 4.7 | Evidencia | Compensación en este juego [inf] |
|---|---|---|
| Geometría virtualizada tipo Nanite | Solo LOD automático y HLOD [F14], [F15] | Cámara alta y zonas acotadas limitan el horizonte |
| GI dinámica completa tipo Lumen | SDFGI semidinámica; HDDAGI sin integrar [F4] | Lightmaps dirigidos por arte y luces de relleno |
| Trazado de rayos por hardware | Solo fontanería inicial de Vulkan RT en 4.7 dev **[sec]** [F26] | El estilo no necesita reflejos exactos |
| DLSS y XeSS | No documentados [F8] | FSR 2.2 y escala bilineal |
| Streaming de texturas | Llega en 4.8 dev [F13] | Presupuesto de VRAM por zona |
| Terreno integrado | Complemento externo MIT [F21] | Terreno modelado o Terrain3D |
| Editor de VFX por nodos y tienda de recursos amplia | **[inf]**, sin verificar | Biblioteca propia de pocos efectos reutilizables |

La comparación detallada con Unity HDRP queda **sin verificar**.

### 3. Técnicas de arte innovador viables

| Técnica | Implementación en Godot | Referencia pública |
|---|---|---|
| Pictórico (Kuwahara) | Cómputo en `CompositorEffect`; aplicar a fondos y excluir personajes con stencil | Kuwahara generalizado MIT [F17]; filtro anisótropo en tiempo real, Kyprianidis 2009 [F27] |
| Contornos de tinta | Profundidad + normales en `CompositorEffect`; grosor por campos de distancia | Proyecto MIT con inundación por saltos, Forward+ [F16] |
| Toon con rampas | `light()` propio con rampa en textura y sombra teñida | Charla de GDC 2015 sobre Guilty Gear Xrd [F28]; shaders espaciales (informe 01) |
| Tramas y medios tonos | Patrón en espacio de pantalla dentro de `light()` | Sin implementación verificada hoy |
| Acuarela o gouache | Papel en pantalla, borde húmedo por profundidad, granulado en sombra | Sin implementación verificada hoy |
| Tilt-shift de diorama | DOF cercano y lejano de `CameraAttributesPractical` con FOV bajo | Estilo HD-2D explicado por sus autores [F29] |
| Cielo y nubes | Shader de cielo pintado; marcha de rayos en perfil alto | Demo MIT de nubes volumétricas [F18] |
| Agua estilizada | Profundidad para orilla, espuma y refracción; FFT opcional | Océano FFT por cómputo, MIT [F19] |
| Hierba densa interactiva | Brizna por instancia, agrupación por ruido, mapa de pisadas | Proyecto MIT basado en la charla de GDC 2021 de Ghost of Tsushima [F20] |
| Viento global | Un ruido compartido como uniforme global para hierba, árboles, ropa y partículas | [inf]; pilar descrito en `10_mundo_vivo` |
| Pintado a mano que responde a la luz | Albedo pintado sin sombra horneada + normal suave + rim | [inf] |

La demo oficial de posproceso por cómputo sirve de plantilla para los efectos propios. [F30]

### 4. Juegos hechos con Godot 4

| Juego | Verificado | Técnica |
|---|---|---|
| DOGWALK (Blender Studio, 2025) | **[doc]** Proyecto abierto; papel recortado, animación tipo stop-motion, glTF desde Blender, recortes de funciones y trucos de luz por rendimiento [F31] | Versión y GI sin verificar |
| PVKK (Bippinbits) | **[doc]** Charla de GodotCon 2024 sobre entornos separados, posproceso y atmósfera [F32] | Detalle sin verificar |
| Road to Vostok | **[sec]** Portado de Unity a Godot 4 con acabado realista [F33] | Sin verificar |
| Slay the Spire 2 (2026) | **[doc]** En el escaparate oficial [F34] | 2D; prueba madurez de producción, no de render 3D |

Lectura honesta **[inf]**: el escaparate oficial no documenta ninguna producción 3D con GI dinámica, volumétricos y posproceso propio a la vez.

### 5. Especificaciones objetivo y escalado

Las GPU salen de la encuesta de Steam [F22] y su VRAM de la tabla del fabricante [F23]. Los fps y presupuestos son **[inf], sin verificar** hasta medir en la GPU alquilada.

| | Compatibilidad | Mínimo | Recomendado | Alto |
|---|---|---|---|---|
| GPU de referencia | Intel HD 620 | GTX 1650 (4 GB) | RTX 3060 (12 GB) o RTX 4060 (8 GB) | RTX 5070 (12 GB) |
| Renderizador | Mobile | Forward+ | Forward+ | Forward+ |
| Resolución y objetivo | 720p, 30 fps | 1080p con escala 0,67–0,75, 30–60 fps | 1080p–1440p, 60 fps | 1440p–4K, 60 fps |
| GI | Ambiente + lightmaps | Lightmaps + sondas | + SDFGI a media resolución | SDFGI alta + SSIL |
| Volumétricos, SSR | No | No | Sí, calidad media | Sí, calidad alta |
| AA | MSAA 2× | FSR 2.2 o SMAA | MSAA 4× + SMAA | MSAA 4× o supermuestreo |
| Firma de posproceso | Casco invertido | Contornos | Contornos + pictórico | Completa + HDR |
| Triángulos visibles | 0,1–0,5 M | 1–1,5 M | 2–4 M | 5–8 M |
| VRAM de texturas | ≤1 GB compartida | 2,5 GB | 5 GB | 8 GB |
| Luces con sombra | 1 direccional | 1 + 2 locales | 1 + 4–6 | 1 + 8, luces de área |
| Briznas visibles | 40 000 (medido) | 150 000 | 400 000 | 1 000 000 |

Escalado sin tocar la lógica **[inf]**: un recurso de «perfil de calidad» fija escala 3D, GI, volumétricos, sombras, densidad de MultiMesh, sesgo de LOD y efectos del compositor. El cambio de renderizador se decide al arrancar. Los materiales necesitan una rama sin búfer de normales para Mobile.

### 6. Qué cambia en el pipeline de recursos

Valores **[inf]**, a confirmar con el corte vertical:

- **Densidad de téxel:** 512 px/m en entorno y 1024 px/m en personajes principales.
- **Mapas:** albedo pintado sin luz horneada, normal, ORM empaquetado y emisivo; normales dobladas opcionales (4.5). [F11]
- **Polígonos:** protagonista y gato 40 000–60 000; NPC 15 000–25 000; props 500–8 000.
- **LOD:** automático en entorno, revisado a mano en mallas con esqueleto; HLOD por grupos de edificios. [F14], [F15]
- **Colisiones:** primitivas o convexas simples, separadas de la malla visual.
- **Formatos:** glTF desde Blender; BPTC para calidad alta y S3TC para lo demás en escritorio. [F25]
- **UV2** limpia en todo lo que reciba lightmap.

### 7. Novedades de 4.5 a 4.7 que ayudan

Complementa la tabla del informe 01 §8. **4.5:** stencil para enmascarar efectos y siluetas tras muros, horneado de shaders, SMAA, oclusión especular. **4.6:** SSR nueva, sondas más baratas, IK para pies y manos, glow antes del tonemapper, importación de texturas más rápida. **4.7:** `AreaLight3D`, HDR, vista previa de shaders en el editor, `DrawableTexture2D` (útil para mapas de pisadas), escala y rotación de partículas 3D. [F9], [F11], [F12]

### 8. Firmas visuales candidatas para la Fase 1

Costos **[inf]**, sin medir.

| # | Firma | Costo de GPU | Costo de producción |
|---|---|---|---|
| 1 | Diorama con tilt-shift y FOV bajo | Medio | Bajo |
| 2 | Tinta: contornos de grosor variable | Bajo–medio | Medio |
| 3 | Fondos pictóricos (Kuwahara selectivo) | Medio–alto | Medio |
| 4 | Toon con rampas y sombras teñidas | Bajo | Medio |
| 5 | Papel y gouache en pantalla | Bajo | Bajo |
| 6 | Tramas y medios tonos en la sombra | Bajo | Bajo |
| 7 | Pradera densa que se aparta al pasar | Alto | Medio |
| 8 | Cielo pintado con nubes vivas | Medio–alto | Medio |
| 9 | Agua con orilla, espuma y cáusticas falsas | Medio | Medio |
| 10 | Rayos de luz y bruma según la hora | Medio–alto | Bajo |
| 11 | Materiales pintados que responden a la luz | Bajo | Alto |
| 12 | Aire habitado: polen, hojas y luciérnagas con colisión | Bajo–medio | Bajo |

Combinación de partida sugerida **[inf]**: 4 + 2 como base, 1 en el hub y 10 como atmósfera.

## Fuentes

Consultadas el 2026-11-12. [doc] salvo indicación.

[F1]: https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html
[F2]: https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/introduction_to_global_illumination.html
[F3]: https://github.com/godotengine/godot/issues/60522
[F4]: https://github.com/godotengine/godot/pull/119869
[F5]: https://docs.godotengine.org/en/4.7/tutorials/3d/volumetric_fog.html
[F6]: https://docs.godotengine.org/en/4.7/classes/class_compositoreffect.html
[F7]: https://docs.godotengine.org/en/4.7/tutorials/rendering/compositor.html
[F8]: https://docs.godotengine.org/en/4.7/tutorials/3d/resolution_scaling.html
[F9]: https://godotengine.org/releases/4.7/
[F10]: https://docs.godotengine.org/en/4.7/tutorials/rendering/hdr_output.html
[F11]: https://godotengine.org/releases/4.5/
[F12]: https://godotengine.org/releases/4.6/
[F13]: https://godotengine.org/article/dev-snapshot-godot-4-8-dev-5/
[F14]: https://docs.godotengine.org/en/4.7/tutorials/3d/mesh_lod.html
[F15]: https://docs.godotengine.org/en/4.7/tutorials/3d/visibility_ranges.html
[F16]: https://github.com/pink-arcana/godot-distance-field-outlines
[F17]: https://godotshaders.com/shader/generalized-kuwahara/
[F18]: https://github.com/clayjohn/godot-volumetric-cloud-demo
[F19]: https://github.com/2Retr0/GodotOceanWaves
[F20]: https://github.com/2Retr0/GodotGrass
[F21]: https://github.com/TokisanGames/Terrain3D
[F22]: https://store.steampowered.com/hwsurvey/videocard/
[F23]: https://www.nvidia.com/en-us/geforce/graphics-cards/compare/
[F24]: https://docs.godotengine.org/en/4.7/about/system_requirements.html
[F25]: https://docs.godotengine.org/en/4.7/about/list_of_features.html
[F26]: https://phoronix.com/news/godot-4.7-dev-1-vulkan-rt
[F27]: https://diglib.eg.org/handle/10.2312/CGF.v28i7pp1955-1963
[F28]: https://gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
[F29]: https://www.unrealengine.com/en-US/spotlights/octopath-traveler-s-hd-2d-art-style-and-story-make-for-a-jrpg-dream-come-true
[F30]: https://github.com/godotengine/godot-demo-projects/tree/master/compute/post_shader
[F31]: https://godotengine.org/article/godot-showcase-dogwalk/
[F32]: https://talks.godotengine.org/godotcon-24/talk/P339BT/
[F33]: https://80.lv/articles/this-upcoming-survival-shooter-game-switches-from-unity-to-godot
[F34]: https://godotengine.org/showcase/slay-the-spire-2/

- Motor y documentación: [F1], [F2], [F5]–[F15], [F24], [F25].
- Incidencias y desarrollo: [F3], [F4], [F13].
- Implementaciones públicas: [F16]–[F21], [F30].
- Hardware: [F22], [F23].
- Charlas y artículos: [F27], [F28], [F29], [F31], [F32], [F34].
- Fuentes secundarias **[sec]**: [F26], [F33].
- Datos locales: `Datos/bench_render_resultados.md`, `Investigacion/01_motor_render.md`, `Investigacion/10_mundo_vivo.md`.
