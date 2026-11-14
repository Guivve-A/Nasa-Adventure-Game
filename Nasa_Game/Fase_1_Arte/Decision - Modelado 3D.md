# Decisión: modelado 3D con Blender, Higgsfield o ruta híbrida

> **Pregunta de Guillermo (2026-11-12):** «¿Cuál es más factible para el modelado de los personajes y recursos a partir de las hojas de referencia: Blender o Higgsfield?»
> **Estado:** **aprobada el 2026-11-12** (D-014): «me gusta mucho la opción de tipo». Guillermo aprendería Blender y pidió las mallas y una escena completa de inmediato. El piloto se ejecutó como **escena de exploración v1**, con otra partida (ver [[#Lo que se ejecutó: escena de exploración v1]]).
> **Cómo se hizo:**
> - dos investigadores, uno por ruta;
> - un juez que comprobó en las fuentes las afirmaciones de las que depende la decisión;
> - verificación propia;
> - una segunda ronda de verificadores independientes y un crítico del plan.
>
> Ver [[#Verificación]].

## Veredicto

**Ruta híbrida, con Blender obligatorio.** Ninguna de las dos rutas cumple sola la [[Biblia de arte]].

- **Blender 5.2 LTS, por script:** construye casi todo el entorno: rocas, arquitectura modular, props duros y troncos. Son unos 84 de los 104 recursos, sin gastar créditos. Da medidas exactas, facetas por construcción y color de la paleta maestra.
- **Higgsfield, con Tripo H3.1:** entrega en minutos la malla base de la protagonista, el gato, los NPC y la fauna, a 9 créditos por intento. Son 20 recursos; modelarlos a mano costaría decenas de horas por personaje.
- **Blender, además, es el taller de toda malla:** facetado, separación de piezas, color por cara, rig y exportación a GLB. Ninguna malla de IA sale lista para el juego.

**Por qué no Higgsfield solo:**
- no tiene low-poly controlable: rechaza `smart_low_poly`, y Hunyuan LowPoly no deja fijar las caras;
- entrega piezas fundidas: pelo, bolso y cuerpo salen en un solo bloque;
- trae la luz pintada en la textura;
- no hace rig de cuadrúpedos: el contrato de `3d_rigging` no tiene tipo de esqueleto.

**Por qué no Blender solo:** modelar a mano a la protagonista costaría de 40 a 120 h por los dos cuerpos, y al gato de 30 a 95 h, según el informe de Blender.

## Por tipo de recurso

Las horas son rangos de los informes, sin medir. El piloto las calibra.

| Recursos | Cantidad | Ruta | Créditos | Horas |
|---|---:|---|---:|---:|
| Rocas y terreno (TER-01 a 12) | 12 | Blender por script | 0 | 6–30 |
| Arquitectura modular e hitos (ARQ-01 a 12, MIR-01, 02 y 08) | 15 | Blender por script | 0 | 16–48 |
| Props duros (URB, TAL, COL y MIR-03 a 07) | 43 | Blender por script; la vaina de ceibo COL-10, por Tripo | 9–18 | 22–86 |
| Vegetación (VEG-01 a 14) | 14 | Troncos por script, follaje en tarjetas con viento; Tripo solo para 2 o 3 troncos de árboles grandes | 0–27, más 9–27,5 de texturas | 21–61 |
| Protagonista, dos cuerpos (PER-01 y 02) | 2 | Malla base de Tripo multivista y limpieza en Blender | 18–41,5 | 16–36 |
| Gato Órbita (PER-09) | 1 | Malla de Tripo; rig con el metarig Cat de Rigify; animación a mano | 9–20,75 | 27–85 |
| NPC (PER-03 a 08) | 6 | A: hoja nueva en A-pose y Tripo. B: Blender sobre la base de la protagonista | A: 70,5–124,5. B: 0 | A: 24–48. B: 60–150 |
| Fauna (FAU-01 a 11) | 11 | Tripo para 9 especies; mariposa y colibrí en Blender | 85,5–166,5 | 11–22 estáticas; 60–130 con rig |
| **Total** | **104** | | **36–71 el núcleo; hasta unos 490 con todo** | **143–416; hasta 720 si las bases de IA no sirven** |

El núcleo es la protagonista, el gato y el prop del piloto. «Con todo» suma NPC, fauna, calcomanías y texturas.

**Correcciones del crítico a estas cifras:**

- **Horas.**
  - El máximo es 720, no 710: si las bases de IA no sirven, el gato también se modela a mano (30–95 h).
  - Faltan de 10 a 30 h de aprendizaje de Blender, las herramientas comunes y las piezas del creador de personaje.
- **Créditos.**
  - Con las ramas opcionales del piloto, el núcleo llega a 94,25.
  - Si los props compactos pasaran a la IA, costarían de 315 a 630 créditos con Tripo, o de 490 a 980 con Hunyuan. Los 980 superan el saldo.
- **NPC.** Cuestan 70,5 con un intento por malla y 124,5 con dos; la hoja se paga una sola vez.

## El riesgo principal: cerrar la distancia con el ancla

![[prototipo_script_vs_ancla.jpg]]

*Arriba, el ancla aprobada (una pintura de IA, no un render). En medio, un prototipo que un investigador generó en 1,4 s, con numpy, sin Blender, sin texturas y sin ajuste artístico. Abajo, el mismo modelo con un error de importación que el piloto ya sabe evitar: el sufijo `-vcol` oscurece el color de vértice.*

El prototipo prueba que la cadena funciona: script, GLB, Godot y la paleta con un error de 3/255. Pero se ve genérico. Las anclas son pinturas, y ningún modelo 3D las igualará exactamente. El piloto mide cuánto se acerca cada ruta, con la cámara de juego y capturas lado a lado.

## Piloto propuesto por el juez (sustituido)

> Guillermo aprobó otra partida, centrada en la escena del ancla. Este diseño queda como referencia; lo que se ejecutó está en [[#Lo que se ejecutó: escena de exploración v1]].

**Objetivo:** antes de producir en serie, medir en Godot dos cosas:

- si la protagonista PER-01 (malla de Tripo limpiada en Blender) cumple la biblia de arte en 16 h o menos;
- qué ruta hace mejor y más rápido un prop duro, el osciloscopio TAL-02: script de Blender, Tripo o Hunyuan LowPoly.

**Créditos** (todo cotizado hoy dos veces, por el juez y por mí, sin gastar; ver `Modelado/cotizaciones_piloto.json`):

| Partida | Modelo | Créditos |
|---|---|---:|
| Prop TAL-02 por Tripo (ruta B) | `tripo_h3_1_image_to_3d`, `face_limit` 3000 | 9 |
| Protagonista PER-01, malla base | `tripo_h3_1_multiview_to_3d`, 3 vistas | 9 |
| **Seguro** | | **18** |
| Reserva: vistas limpias, sin bolso y en A-pose | `gpt_image_2_6` high 2k | 2,75 |
| Reserva: segundo intento de la protagonista | `tripo_h3_1_multiview_to_3d` | 9 |
| Opcional: prop por Hunyuan LowPoly (ruta C) | `hunyuan3d_v3_image_to_3d` | 14 |
| Solo si gana Tripo: segundo prop, TAL-05 | `tripo_h3_1_image_to_3d` | 9 |
| **Tope** | | **52,75** |

El tope queda por debajo de los 60 créditos de la prueba de pipeline de la Fase 0. El límite de caras no cambia el precio: con 500, 3 000 o 20 000 caras cuesta 9.

**Pasos y tope de horas** (36 h en total, unos 7 a 9 días hábiles):

1. Puerta 0, Guillermo: aprobar la partida, instalar Blender y dar a la hoja de PER-01 y a TAL-02 al menos el veredicto «sirve para el piloto».
2. Blender en la HD 620 (1 h): prueba de humo sin ventana y con interfaz; si no dibuja, probar con Vulkan.
3. Escena de medida en Godot (5 h): cámara de juego y cámara del hub, capturas a 720p y 1080p, triángulos, milisegundos por cuadro y comparación de siluetas.
4. Prop por script de Blender, ruta A (4 h, 0 créditos).
5. Prop por Tripo, ruta B (4 h, 9 créditos): limpieza en Blender y dos versiones de color.
6. Prop por Hunyuan LowPoly, ruta C (1 h, 14 créditos, opcional): solo se importa y se mide.
7. Segundo prop por la ruta ganadora (2 h), para medir el tiempo con las herramientas ya hechas.
8. Protagonista: malla base por Tripo multivista (9 créditos).
9. Protagonista en Blender (10 h): separar pelo y bolso, simetrizar, tres niveles de 1 500, 3 000 y 6 000 triángulos, color por cara de la paleta y textura solo para ojos y boca.
10. Rig y animación (6 h): Mixamo con la cuenta de Guillermo (reposo, caminar y correr); si falla con la cabeza grande, Rigify.
11. Medición y veredicto (3 h): capturas lado a lado con las anclas y una tabla con criterios, horas y créditos reales.

**Criterios de éxito.** Son umbrales del juez, sin calibrar:

- **Silueta:** IoU de 0,85 o más para la protagonista y de 0,80 o más para el prop.
- **Facetas visibles:** con la cámara de juego, el 80 % del área en facetas de 16 px² o más.
- **Presupuesto:** la protagonista, con 6 000 triángulos y 3 materiales como máximo; el prop, con 1 500 y 2.
- **Paleta:** 95 % o más en `paleta.py comparar`.
- **Luz pintada:** con luz uniforme, la diferencia entre las mitades izquierda y derecha es del 10 % o menos.
- **Animación:** reposo, caminar y correr funcionan en Godot sin errores.
- **Rendimiento:** la protagonista animada más 20 props cuestan 2 ms o menos por cuadro en la HD 620.
- **Costo:** 52,75 créditos o menos.
- **Veredicto de Guillermo:** «se ve como el juego aprobado».

**Regla de decisión:**

- **Props:**
  - si la ruta A cumple con 2 h o menos por prop, los 43 props van por Blender;
  - si gana Tripo, se propone pasar los 35 props compactos a Higgsfield (hasta 315 créditos, con aprobación).
- **Personajes:**
  - si la protagonista cumple en 16 h o menos, se generan PER-02, el gato y las bases de NPC y fauna antes de que caduquen los créditos;
  - si no, los personajes se modelan en Blender y el gato pasa a un piloto propio.

**Ajustes que propongo al plan del juez:**

- **Medir los dos tamaños de personaje.** El piloto puede medir a la vez el 12,5 % y el 21 %, porque en Godot solo cambia la distancia de la cámara. Así esa decisión no bloquea el arranque (ver [[#Decisiones que pide a Guillermo]]).
- **Lado del perfil.** El perfil de la hoja de PER-01 muestra el lado derecho; el juez lo dio por izquierdo. Tripo pide frente, izquierda y espalda, y su documentación no aclara qué lado es «izquierda». Hay que probarlo o espejar el perfil.
- **El bolso.** En el frente y en 3/4 cuelga delante de la cadera derecha; en el perfil, detrás. Se quita de las vistas y se modela aparte, como propone el juez.
- **El gato queda fuera del piloto.** Es el mayor riesgo de horas (27–85 h, sobre todo la animación) y necesita un piloto propio con tope de horas.

## Lo que se ejecutó: escena de exploración v1

Guillermo pidió las mallas y una escena completa ya, para validarlas con él. La escena recrea en Godot la vista aprobada del sendero (`pruebas/escena_exploracion/`).

**Partida aprobada:** 37,5 créditos seguros y un tope de 52,75.

**Gasto real:** 36,00 créditos en el lote 04a; el saldo pasó de 940,25 a 904,25.

| Recurso | Ruta | Resultado |
|---|---|---|
| Protagonista PER-01 | Tripo multivista: frente, perfil y espalda; tope de 5 000 caras | Buena geometría, de 4 930 triángulos. Pero la textura salió gris plana y la malla en espejo, porque Tripo leyó el perfil derecho como vista izquierda. Se corrigió sin créditos con `herramientas/mallas/proyectar_vistas.py --auto`: pinta la textura desde la hoja y espeja la geometría. En las cuatro vistas, entre el 1,7 % y el 3,1 % de las caras caen sobre el fondo |
| Órbita PER-09 | Tripo multivista: frente, perfil, espalda y perfil espejado | Bien: 2 733 triángulos, con textura y la medalla cian |
| Iguana FAU-01 | Tripo multivista con las dos vistas de la hoja, ampliadas | Bien: 2 376 triángulos. No hizo falta vista limpia: se ahorraron 1,5 créditos |
| Antena COL-01 | Tripo desde una imagen | 2 305 triángulos, con la base de hierba de la hoja fundida. Se compara con la versión por script |
| Entorno | Por script: terreno, sendero, arroyo con cascadas, plaza, rocas, árbol, puente, escalinata, baranda, panel, plantas y flores | 0 créditos |

**Técnica de cámara:** los objetos se echan hacia atrás en el shader (`z -= 0,55·y`), así se leen erguidos como en el ancla, que no tiene el escorzo de una cámara de 55°. La escena captura los dos tamaños de personaje (21 % y 12,5 %) y las dos antenas, y deja recorrerla con el teclado.

## Qué instalar

- **Ahora: Blender 5.2.4 LTS para Windows x64.** Lo descarga e instala Guillermo; hay 27 GB libres.
  - **Archivo:** `blender-5.2.4-windows-x64.msi`, de https://download.blender.org/release/Blender5.2/.
  - **Tamaño:** 366 022 656 bytes.
  - **SHA-256:** `bed4fef5219837a59ea4ca0c607a92326a2c8f5dc1c3c67ade72b41e4187895b`.
  - **Comprobar la descarga:** `certutil -hashfile blender-5.2.4-windows-x64.msi SHA256`.
- **Opcional: MCP de Blender** (paquete `mcp-for-blender`), para que Claude maneje en vivo el Blender que Guillermo tenga abierto. Sin él, Claude ya usa Blender por línea de comandos (`blender -b --python`). Instalación:
  1. Instalar `uv` con `winget install --id=astral-sh.uv -e` y abrir una terminal nueva.
  2. Instalar el complemento de Blender con `uvx mcp-for-blender install-addon`.
  3. Registrarlo en Claude Code sin telemetría: `claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender`.
  4. En Blender, ir a Edit → Preferences → Add-ons y activar «Interface: MCP for Blender».
  5. Con N, abrir la pestaña «MCP for Blender», dejar desmarcadas las integraciones externas (Poly Haven, Sketchfab, Hyper3D, Hunyuan3D, Meshy, Tripo y World Labs) y pulsar **Connect to Claude**.
  6. Abrir una sesión nueva de Claude, que es donde carga el MCP.

  Riesgos: es código de terceros; su herramienta `execute_blender_code` ejecuta Python arbitrario, así que hay que guardar antes de usarla; y el servidor local no tiene autenticación.
- **En el paso de rig:** una cuenta gratuita de Adobe para Mixamo. La crea Guillermo; no es software.
- **Nada más.** Blender cubre la reducción, las normales planas y la conversión a FBX para Mixamo. Para medir bastan Godot, Python e ImageMagick.
- **Solo si el piloto muestra que el portátil frena:** un PC en la nube con GPU para Blender. La ruta por script no lo necesita.

## Decisiones que pide a Guillermo

Estado al 2026-11-12:

- **Resueltas:**
  - la ruta por tipo, con Blender obligatorio (1);
  - la partida de la escena v1 (2);
  - aprender Blender (5).
- **Sustituida:** el veredicto de las hojas (3) pasa a ser el de las mallas en la escena.
- **Abierta:** el tamaño del personaje (4); la escena captura los dos para que elija viéndolos.

1. **Blender pasa a ser obligatorio.** En la [[Fase 0 - Analisis]] era opcional, con la versión 4.5 LTS.
2. **Partida del piloto:** 18 créditos seguros y un tope de 52,75.
3. **Veredicto de la hoja de PER-01 y de TAL-02**, al menos «sirve para el piloto».
4. **Tamaño del personaje en la exploración.** La biblia de arte, D-013 y el bloque `CAMARA_JUEGO` dicen «un octavo del alto» (12,5 %). En la imagen aprobada, la protagonista mide el 20,9 %: de y = 664 a y = 982 en 1 520 px, unos 226 px a 1080p. Con el 21 % se ve menos mapa y el personaje necesita más detalle.

![[ancla_altura_personaje.png]]

*La protagonista del ancla `L02_exploracion_camara_alta.png` con una regla cada 10 px (ampliada ×2). Mide 318 px de 1 520.*

5. **Experiencia en Blender.** La limpieza fina de la protagonista, los pesos y la animación del gato pueden recaer en ti. ¿Cuánta experiencia tienes con Blender? Cambia las horas del plan.

## Verificación

**Segunda ronda de verificadores** (fuentes primarias, intentando refutar):

| Afirmación | Veredicto | Dato |
|---|---|---|
| Blender 5.2 es LTS, con soporte hasta julio de 2028 | Confirmada | Salió el 2026-07-14. El 2026-11-10 salieron la 5.2.4 y la 5.3, que no es LTS |
| Archivos de la 5.2.4 | Confirmada | `.msi` de 366 022 656 bytes y `.zip` de 405 779 142 bytes, ambos con SHA-256 publicado |
| Requisitos mínimos y la HD 620 | Corregida | La HD 620 (Kaby Lake) es la primera GPU Intel admitida. El mínimo oficial es de 4 núcleos y 8 GB: la CPU de 2 núcleos queda por debajo y la RAM, justo en el mínimo |
| Opción `--gpu-backend vulkan` en Windows | Confirmada | Existe; en la 5.2 el predeterminado sigue siendo OpenGL |
| Rigify no trae metarig de ave | **Refutada** | Sí lo trae (`bird.py`), aunque el manual 5.2 lo omite. Sirve para la fauna con alas |
| Mixamo solo acepta FBX, OBJ o ZIP | Confirmada | Además, su rig automático es solo para humanoides bípedos |
| El exportador glTF guarda el color de vértice | Confirmada | Lo guarda si el objeto no tiene material |
| El sufijo `-vcol` de Godot oscurece el color | Confirmada | Activa sRGB en un color que ya es lineal |
| Detalles de Tripo y fechas de Meshy | Confirmadas o corregidas | `smart_low_poly` existe en la API de Tripo, pero Higgsfield no lo expone. Meshy deja `lowpoly` en dos etapas (30-10 y 30-11) y `meshy-7` el 31-12 |

**Crítico del plan.** Encontró 13 problemas. Los que cambiaron el trabajo:

- el lote mezclaba convenciones de perfil, y se confirmó en la malla en espejo;
- el bolso sigue en las vistas;
- la antena traía la base de hierba fundida;
- `hf_generar.py` no estaba probado con 3D; ya está corregido;
- el color plano por cara contradecía el degradado de la biblia: la escena usa color por esquina con degradado;
- la cámara de 60° salía del encargo y no del ancla: se resolvió con la inclinación hacia atrás;
- la aritmética, corregida arriba.

Quedan abiertos:

- calibrar el criterio de facetas a 720p;
- una tabla de medidas en metros por recurso;
- el respaldo del gato si su rig falla (sprites, con créditos que caducan);
- el calendario de puertas antes del 10-12.

**Comprobado por mí:**

- **Cotizaciones**, con un script propio: Tripo con una imagen cuesta 9 con 500, 3 000 o 20 000 caras; Tripo multivista con 3 vistas, 9; Hunyuan LowPoly, 14; `gpt_image_2_6` high 2k, 2,75. Higgsfield rechaza `smart_low_poly`. El contrato de `3d_rigging` no tiene tipo de esqueleto.
- **Tamaño del personaje en el ancla:** 20,9 %, medido con regla. Coincide con el juez.
- **Bolso de la hoja de PER-01:** confirmé la incoherencia, aunque con una corrección. El perfil muestra el lado derecho, no el izquierdo: mira hacia la derecha y no se ve el reloj, que en el frente está en la muñeca izquierda.
- **Prototipo:** 4 036 triángulos en 1,44 s, generado con numpy; los «7 minutos» que citaba el investigador no constan.
- **Aritmética** de créditos y horas por tipo: cuadra.

## Riesgos y puntos débiles

- **Nada está medido todavía:** no se generó ninguna malla ni se ejecutó Blender. Las horas son inferencias hasta el piloto.
- **Blender en este portátil:** no está probado. La CPU de 2 núcleos y el OpenGL del controlador, que Godot marca como de baja calidad, son riesgos. Planes B: Vulkan, la versión 4.5 LTS o un PC en la nube.
- **Scripts de Blender:** la ruta depende de que Claude escriba buenos scripts bpy y de la revisión visual de Guillermo. El prototipo se veía genérico.
- **Caducidad de los créditos:** caducan al cierre del periodo, hacia el 2026-12-12; la fecha no está confirmada. Si los veredictos no llegan a tiempo, NPC y fauna pasan a Blender con más horas, y los créditos sin usar se pierden.
- **Mixamo** puede fallar con un personaje de 3 cabezas y pelo voluminoso. El plan B, Rigify, cuesta más horas.
- **Uso comercial de las mallas 3D** de Higgsfield: no verificado. Solo consta lo general de los términos (apartados 4.4 y 8).
- **Costos sin cotizar:** `image_to_3d`, `multi_image_to_3d` y `3d_rigging` no se pueden cotizar. Tampoco se sabe si un trabajo fallido devuelve los créditos.

## Fuentes

- Informes y veredicto del juez: workflow `wf_dae7c755-892` (2026-11-12), con las fuentes de cada dato.
- Cotizaciones: `Modelado/cotizaciones_piloto.json`.
- Antecedentes: [[02_pipeline_personajes]] (Fase 0) y [[Lote 02 - Tipo de juego y personajes]].
