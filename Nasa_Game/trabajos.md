---
tipo: seguimiento
actualizado: 2026-11-12
---

# Trabajos: avances y pendientes

> Qué se hizo, qué falta y en qué se gastaron los créditos. Las decisiones y las lecciones van en [[Memory]].

## Estado por fase

| Fase | Tema | Estado |
|---|---|---|
| 0 | Investigación técnica, arquitectura y pipeline | En revisión. La parte de PC en la nube y objetivo AAA queda para después, por indicación de Guillermo |
| 1 | Dirección de arte visual y cinematografía | Estilo aprobado (D-011, D-015). Esperan veredicto el lote 03 y la partida del lote 06 |
| 2 | Estructura narrativa y diseño de misiones | Pendiente |
| 3 | Personajes, animación y entidades | Pendiente |
| 4 | Diseño acústico espacial y banda sonora | Pendiente |
| 5 | Diseño de niveles y generación masiva | **Adelantada por orden de Guillermo (2026-11-13):** juego jugable v0 en `juego/`, en construcción |
| 6 | Mecánicas, físicas y game feel | **Adelantada:** núcleo jugable, minijuegos y base espacial en construcción |
| 7 | UI/UX, tipografía y accesibilidad | Pendiente |

## Hecho

### 2026-11-12

- [x] Higgsfield listo: CLI 1.2.2, sesión iniciada, espacio de trabajo «Private» y 9 skills instaladas.
- [x] Inventario del equipo y de las herramientas instaladas.
- [x] Catálogo de 119 modelos de Higgsfield y 169 cotizaciones, sin gastar créditos (`Fase_0_Tecnica/Datos/`).
- [x] Plan maestro y 14 referencias guardados en la bóveda. [[Analisis del tablero]] escrito.
- [x] Conexión con Codex por línea de comandos (`herramientas/codex_lote.py` y `codex_reanudar.py`).
- [x] `CLAUDE.md`, [[Memory]], [[Inicio]] y este archivo creados.
- [x] Nueve informes de investigación de Codex en `Fase_0_Tecnica/Investigacion/`. El de arquitectura se cortó a los 30 minutos y se recuperó reanudando la sesión.
- [x] Prueba de rendimiento en `pruebas/bench_render/`: 29 corridas en la HD 620. Mobile es el renderizador más rápido y estable; SDFGI no es viable.
- [x] Verificación independiente de los informes: 76 afirmaciones confirmadas, 16 imprecisas, 4 sin poder verificar y ninguna refutada.
- [x] [[Fase 0 - Analisis]] redactado, con 10 decisiones propuestas.
- [x] Guillermo pidió un objetivo AAA sin limitarse al portátil y ofreció alquilar un PC en la nube. Medidas la latencia y el ancho de banda desde Guayaquil ([[red_latencias]]).
- [x] Codex agotó su límite de uso a las 02:26; se restablecía a las 06:27.
- [x] Guillermo pidió empezar los diseños con Higgsfield y dejar el alquiler del PC para después.
- [x] `herramientas/hf_generar.py`: genera lotes con tope de créditos, descarga los originales y registra cada generación.
- [x] **Lote 01 de dirección de arte:** 7 imágenes, 19,25 créditos. Ver [[Lote 01 - Direcciones de arte]].
- [x] **Veredicto del lote 01:** Guillermo eligió el low-poly pintado a mano y un juego de exploración con mapa mediano en 2D-HD.
- [x] **Lote 02:** vista de juego con cámara alta, mapa de la región, centro espacial, dos hojas del protagonista y hoja del gato. 6 imágenes, 16,50 créditos. Ver [[Lote 02 - Tipo de juego y personajes]].
- [x] Guillermo aprobó la vista superior del lote 02 («así se debe ver»): D-013.
- [x] Sistema de coherencia: [[Biblia de arte]] v0.1, paleta maestra medida, anclas subidas a Higgsfield, bloques fijos de encargo y manifiesto de recursos con IDs.
- [x] **Lote 03:** nueve hojas de referencia con 104 recursos, escena de noche del Mirador y maqueta del telescopio. 11 imágenes, 30,25 créditos. Ver [[Lote 03 - Hojas de referencia y Mirador]] y [[Catalogo de recursos]].
- [x] Idea de la Luna con datos de NASA validada técnicamente con datos reales de esta noche: [[Mirador del Faro - Luna con datos reales]].
- [x] Guillermo autorizó descargar tres archivos públicos de NASA. Descargados a `externos/` con tamaño y SHA-256 comprobados (`Propuestas/Datos/descargas_nasa.json`).
- [x] Prueba técnica en Godot (`pruebas/luna_telescopio/`): la Luna real de las 19:30 desde el Mirador, con texturas de LRO. La máscara medida da 12,15 % iluminado y el borde a 192,6° del cenit; Horizons dice 12,2 % y 192,6°.
- [x] Verificación independiente de la prueba con tres revisores: orientación, datos y código. El de código encontró 9 problemas; el crítico era que las texturas no cargaban en el juego exportado. Corregidos 8; queda la orientación para cualquier instante.
- [x] Pruebas con el código final ([[Mirador del Faro - Luna con datos reales]]):
  - el juego exportado (`.pck`) da una captura idéntica a la del editor;
  - con HDR 2D el disco difiere 0,85 niveles;
  - la gibosa del 21 de noviembre da 91,21 % y 41,0°, igual que Horizons;
  - la Luna bajo el horizonte no se dibuja, antes de su salida ni después de su puesta;
  - `luna_medir.py` también mide la orientación de la textura: correlación de 0,990, sin giro ni espejo.
- [x] Capturas de la prueba en `Propuestas/Capturas/`.
- [x] **Estudio Blender o Higgsfield para el modelado 3D** ([[Decision - Modelado 3D]]):
  - dos investigadores y un juez, más una verificación propia;
  - recomienda una ruta híbrida: Blender obligatorio para el entorno por script (84 recursos, 0 créditos) y Tripo H3.1 para las mallas base de personajes y fauna (20 recursos);
  - propone un piloto de 18 créditos seguros y 52,75 de tope;
  - las cotizaciones se repitieron dos veces, sin gasto.
- [x] **Lote 04a** (36 créditos): mallas de la protagonista, Órbita, la iguana y la antena. La textura de la protagonista se proyectó desde su hoja con `herramientas/mallas/proyectar_vistas.py`.
- [x] **Escena de exploración v1** en curso ([[Escena de exploracion v1]]): terreno, arroyo, rocas, hierba y flamboyán por script; corre a 61-66 fps en la HD 620.
- [x] **Codex escribió los scripts de Blender** (`herramientas/blender/`), sin probar porque Blender no está instalado:
  - `limpiar_personaje.py`: niveles de detalle;
  - `glb_a_fbx_mixamo.py` y `fbx_mixamo_a_glb.py`: ida y vuelta por Mixamo;
  - `rig_gato.py`: metarig Cat de Rigify, con reposo y caminar.

  Informes en `Fase_1_Arte/Modelado/Tareas_Codex/informes/`.
- [x] **Protagonista v2** (lotes 04b y 04c, 14,75 créditos): hoja de giro limpia (`L04_PER01_giro.png`) y Tripo multivista con textura detallada. La cara salió fiel a la hoja. En Godot, el acabado 2.5D (`pintado`) evita que el contraluz le parta la cara.
- [x] **Codex:**
  - MultiMesh en la escena: las llamadas de dibujo bajaron de 252 a 58 y de 420 a 64; los fps no cambian con claridad (falta verificarlo con una medición propia).
  - Paso del gato: zancada 4,4 veces mayor y apoyos con error de 0,2 mm; ya está en la escena.
- [x] **Bucle de ajuste al ancla:** 17 iteraciones, ΔE de 28,0 a 19,4. Luminosidad, croma y contraste igualan al ancla. La escena corre a 48 fps (encuadre 21) y 44 fps (encuadre 12) en la HD 620. Estado y pendientes en `pruebas/escena_exploracion/capturas/iteraciones/BUCLE.md`.
- [x] Investigación de Codex para la Fase 2, sin revisar todavía: `Fase_2_Narrativa/Investigacion/01_datos_espaciales_ecuador.md` y `02_historia_existente.md`.

### 2026-11-13

- [x] Guillermo eligió el borrador A «Mañana cálida» de la Habitación (D-018). Versión final con entrada y salida: 2,75 créditos.
- [x] Bucles cerrados: escena del sendero (19 vueltas, ΔE 19,4) y protagonista (v8T aprobada, D-017). El bolso nuevo (v9) da 82,1 % de parecido y ya va en el juego.
- [x] **Núcleo del juego jugable** en `juego/` (D-019), escrito y probado:
  - estado de la partida, banderas, misiones, cuaderno y guardado;
  - zonas con umbrales (entrada y salida diseñadas) y ventana de carga con un dato real;
  - protagonista jugable, Órbita que la sigue y da pistas, y la cámara aprobada;
  - diálogos, avisos, pausa, cuaderno, menú principal con «Minijuegos» y «Lugares»;
  - anfitrión de minijuegos con instrucciones, pistas y resultado;
  - shaders y luz aprobados (D-015), portados sin cambios;
  - pruebas automáticas: núcleo (16 de 16), zona y minijuego de plantilla.
- [x] `juego/ARQUITECTURA.md`: el contrato para los agentes que construyen zonas y minijuegos.
- [x] `herramientas/juego_ejecutar.py`: ejecuta Godot de uno en uno, con candado global.
- [x] Codex: 55 fichas del cuaderno con datos verificados (`juego/datos/datos_espaciales.json` y `FUENTES.md`), en 7 min.
- [x] Diseño de la base espacial: [[Base espacial - Diseno]] (pedido de Guillermo del 2026-11-13).
- [x] Flujos lanzados, cada carril con su verificador escéptico: rig de la protagonista y lote 06 de conceptos (solo cotizar); Habitación y Plaza con biblioteca; Sendero y Mirador; base espacial (datos reales, simulación, mundo e interfaz); minijuegos seguidor, antena y satélite. Codex: línea de tiempo, órbita y regreso.

## Pendiente

### De Guillermo

- [x] **Estilo en el motor aprobado** (D-015, 2026-11-12): el acabado 2.5D pintado de la escena del sendero es la base de todo el juego.
- [x] **Habitación: rehacer el concepto** (D-016). El ancla ANC_HUB no sirve, por la cámara, la distribución, el ambiente y la historia. Guillermo pide «algo más cercano a juegos típicos, 2D-HD», con la vista superior de D-013.
- [x] Partida del lote 05 aprobada («Sí: 4,25 y tope 8,50») y borrador A elegido.
- [ ] **Jugar el prototipo** (`juego/jugar.cmd`) y validar cada escenario con capturas: Habitación (concepto validado), Sendero (aprobado), y los provisionales: Plaza con biblioteca, Mirador, Luna del sueño y base espacial.
- [ ] Dar el visto bueno a la versión final del concepto A de la Habitación y al bolso v9 de la protagonista.
- [ ] **Aprobar la partida del lote 06** (conceptos de la Luna y del Mirador de tarde; después, de la plaza con la biblioteca y de la base espacial).
- [ ] Responder las preguntas de [[Base espacial - Diseno]] (Luna o Marte, nombre de la base, robots o tripulación, interior de la biblioteca).
- [ ] Decidir si se gasta una partida de Tripo en las mallas de los vecinos (Elena, Rafael, Lidia, Sam, Ari): hoy la plaza no tiene personas.
- [ ] Veredicto de la protagonista v6 (bucle del 80 %; corre la limpieza de la textura).
- [ ] Decidir si se gastan los 2,00 créditos que quedan de la partida (o una partida nueva) en texturas pintadas del suelo para el acabado 2D-HD.
- [ ] **Dar el veredicto del lote 03:** hojas de referencia, escena de noche y vista del telescopio.
- [ ] Veredicto del resto del lote 02: mapa, centro espacial, protagonista y gato (solo se aprobó la vista superior).
- [ ] **Decidir el modelado 3D** ([[Decision - Modelado 3D]]):
  - aprobar la ruta híbrida, con Blender obligatorio;
  - aprobar la partida del piloto: 18 créditos seguros y un tope de 52,75;
  - dar a la hoja de PER-01 y a TAL-02 al menos el veredicto «sirve para el piloto»;
  - decidir el tamaño del personaje: el texto dice 12,5 % y el ancla mide 20,9 %;
  - contar cuánta experiencia tiene con Blender.
- [ ] Instalar Blender 5.2.4 LTS para Windows x64, de download.blender.org, antes del piloto. Guillermo se ofreció a descargarlo. Reemplaza a la 4.5 LTS que proponía la Fase 0.
- [ ] Crear una cuenta gratuita de Adobe para Mixamo, para el paso de rig del piloto.
- [ ] Aprobar o corregir la Fase 0: [[Fase 0 - Analisis]].
- [ ] Confirmar la fecha de renovación del plan de Higgsfield. Los créditos de suscripción caducan al cierre del periodo, hacia el 2026-12-12; el piloto debería terminar antes del 2026-11-26.
- [ ] Decidir el repositorio remoto y si hay fecha límite.
- [ ] Confirmar en Git el trabajo sin versionar de la bóveda anterior (`Desktop\Juego\Juego_2d-hd`).

### De Claude

- [ ] **Seguir el bucle de ajuste al ancla** hasta el visto bueno de Guillermo (pendientes 1 a 7 de `BUCLE.md`).
- [x] **Fase 2, borrador listo** (flujo `wf_26dcca38-bc2`, 9 agentes):
  - Datos verificados con fuentes primarias, en `03a` (18 confirmados, 3 corregidos, 5 sin verificar) y `03b` (17 confirmados y 3 corregidos).
  - Propuestas A «Luz cenicienta» (88 min), B «La bitácora de una noche» (85 min) y C «Barrio con vista a la Luna» (85 min).
  - Los jueces eligieron A (8,15) con injertos de B y C.
  - Síntesis: `Fase_2_Narrativa/Fase 2 - Analisis.md`, con 94 min de ruta principal, las decisiones F2-01 a F2-16 y 9 preguntas para Guillermo.
  - Plan de auditoría: `Auditoria/Plan de auditoria.md` (etapas 0 a 8 y carriles C1 a C7).
- [ ] **Carriles en paralelo** (2026-11-12):
  - C7: revisión escéptica del borrador de la Fase 2.
  - C5: prototipo gris de la Luna, que dio 63 fps (verificado), **construido sin validar y detenido**. Guillermo recordó que los escenarios y el estilo se validan con él antes de construir, siempre y sin excepciones. Queda solo como medición técnica. La mejora C5b se canceló (flujo `wf_87d07bec-501`, detenido antes de tocar archivos).
  - C6: Codex investiga accesibilidad y datos pendientes (la bandera de Ecuador, el disco del Apolo 11 y la Luna del 13-11-2026).
  - C1 (medir lo existente) espera a que el equipo quede libre.
- [ ] **Bucle de la protagonista** (meta: 80 % o más de parecido con su hoja):
  - v5C llega a 83,9 % y v6C, con bolso, a 82,9 % (métrica registrada);
  - corre la limpieza de defectos de textura (flujo `wf_151a2471-347`);
  - estado en `Fase_1_Arte/Modelado/Lote_04/parecido/BUCLE_PROTAGONISTA.md`.
- [ ] Verificar con una medición propia el MultiMesh de Codex.
- [ ] Luna de cualquier fecha sin conexión: leer `mooninfo_2026.json` y aplicar en Godot las correcciones topocéntricas de Guayaquil. Calcular el ángulo paraláctico en cada instante: cerca del cenit el disco gira hasta 12° por minuto.
- [ ] Telescopio: cielo de día y crepúsculo, eclipses y hora de salida en el panel.
- [ ] Lote 04, después del veredicto: correcciones de las hojas, noche del Mirador con luz fría, HUD sobre la vista de juego y primera malla 3D del protagonista.
- [ ] Retomar la revisión de la Fase 0 para el objetivo AAA con PC en la nube, cuando Guillermo lo pida. El flujo de investigación quedó interrumpido (`wf_3ca8ac6e-3b6`); solo existe el informe parcial `12_render_aaa.md`, sin verificar.
- [ ] Piloto de modelado 3D, después de la puerta 0 ([[Decision - Modelado 3D]]): prop TAL-02 por tres rutas y la protagonista PER-01 por Tripo y Blender, medidos en Godot. Tope: 52,75 créditos y 36 h. Reemplaza a la prueba de pipeline de 60 créditos de la Fase 0.
- [ ] Piloto propio del gato (rig y animación de un cuadrúpedo), con tope de horas, después del piloto de modelado.
- [x] Scripts de Codex probados en Blender 5.3:
  - `limpiar_personaje.py`: funciona tras una corrección. Genera la protagonista con 1 500 y 3 000 triángulos.
  - `rig_gato.py`: funciona tras cinco correcciones mías y una de Codex. Órbita camina en la escena, verificada en Godot.
- [ ] Rig de la protagonista por Mixamo (`glb_a_fbx_mixamo.py` y `fbx_mixamo_a_glb.py`, sin probar). Necesita la cuenta gratuita de Adobe de Guillermo.
- [ ] En `limpiar_personaje.py` y `rig_gato.py`, permitir salidas fuera de `herramientas/blender/`.
- [ ] Animación del gato: hoy es un paso pequeño en el sitio. Falta revisar el contacto con el suelo, darle más amplitud y moverlo por el mundo.
- [ ] Probar el horneado de un lightmap en la HD 620.
- [ ] Probar DotGothic16 con texto en español a tamaño de juego.
- [ ] Inicializar Git y Git LFS y crear la estructura del proyecto de Godot.
- [ ] Fase 1: dirección de arte.

## Registro de créditos de Higgsfield

| Fecha | Partida | Modelo | Cantidad | Créditos | Saldo | Aprobó |
|---|---|---|---|---|---|---|
| 2026-11-12 | Saldo inicial (1000 de suscripción acreditados ese día) | — | — | — | 1006,25 | — |
| 2026-11-12 | Cotizaciones y marcador gris de prueba | `generate cost` | 169 | 0 | 1006,25 | — |
| 2026-11-12 | Lote 01a: la misma escena low-poly en tres modelos | GPT Image 2.6, Nano Banana Pro y Seedream 5.5 | 3 | 8,25 | 998,00 | Guillermo («empezar con los diseños») |
| 2026-11-12 | Lote 01b: gouache, maqueta, papel y vista de juego low-poly | GPT Image 2.6 | 4 | 11,00 | 987,00 | Guillermo («empezar con los diseños») |
| 2026-11-12 | Lote 02: vista de juego, mapa, centro espacial, protagonista (2) y gato | GPT Image 2.6 | 6 | 16,50 | 970,50 | Guillermo (eligió la dirección para seguir) |
| 2026-11-12 | Lote 03a: nueve hojas de referencia (104 recursos) | GPT Image 2.6 | 9 | 24,75 | 945,75 | Guillermo («quiero diseños de recursos… reference sheets») |
| 2026-11-12 | Lote 03b: noche del Mirador y maqueta del telescopio | GPT Image 2.6 | 2 | 5,50 | 940,25 | Guillermo (validar la idea del telescopio) |
| 2026-11-12 | **Partida aprobada:** escena de exploración v1 (piloto de modelado). Seguro: 37,5 (protagonista 9, Órbita 9, iguana 10,5 con su vista limpia, antena COL-01 9 para comparar con el script). Tope: 52,75 | Tripo H3.1 y GPT Image 2.6 | — | — | 940,25 | Guillermo («Sí: 37,5 y tope 52,75») |
| 2026-11-12 | Lote 04a: mallas de la protagonista, Órbita, la iguana y la antena. La iguana no necesitó vista limpia: su hoja ya trae frente y lado | Tripo H3.1 (multivista ×3, imagen ×1) | 4 | 36,00 | 904,25 | Guillermo (partida de la escena v1). Quedan 16,75 de la partida |
| 2026-11-12 | Lote 04b: hoja de giro limpia de la protagonista (frente, perfil y espalda en A, sin bolso y con la cara despejada). Guillermo: la malla «se ve totalmente mal… las facciones» | GPT Image 2.6 high 2k | 1 | 2,75 | 901,50 | Guillermo (reserva de la partida de la escena v1). Quedan 14,00 |
| 2026-11-12 | **Partida aprobada:** lote 05, conceptos de la Habitación (D-016). Seguro: 4,25 (6 borradores por 1,50 y la versión final elegida por 2,75). Tope: 8,50 (una ronda de corrección y una segunda luz) | GPT Image 2.6 | — | — | 889,50 | Guillermo («Sí: 4,25 y tope 8,50») |
| 2026-11-12 | Lote 05a: 6 borradores de la Habitación con vista superior 3/4 y aire 2D-HD (A mañana, B noche, C azotea, D cama alta, E casa de muñecas, F cuarto-tutorial en L). Lámina: `Exploracion/Lote_05/_lamina_lote05.png` | GPT Image 2.6 low 1k | 6 | 1,50 | 888,00 | Guillermo (partida del lote 05). Quedan 7,00 del tope |
| 2026-11-12 | Lote 04c: malla nueva de la protagonista desde la hoja de giro (frente, perfil espejado, espalda y perfil), textura detallada. La cara salió fiel a la hoja | Tripo H3.1 multivista ×4 | 1 | 12,00 | 889,50 | Guillermo (reserva de la partida de la escena v1). Quedan 2,00 |
| 2026-11-13 | Lote 05b: versión final del concepto A de la Habitación, con el descanso de la escalera como entrada y salida (`Exploracion/Lote_05/L05_A_manana_calida_final.png`) | GPT Image 2.6 high 2k | 1 | 2,75 | 885,25 | Guillermo (partida del lote 05). Quedan 4,25 del tope |
