---
tipo: plan de auditoría
fecha: 2026-11-12
estado: borrador · espera la aprobación de Guillermo
fases: 1 (arte), 2 (narrativa), 5 (niveles), 6 (mecánicas) y 7 (interfaz)
fuentes: "[[Escena de exploracion v1]], [[Mirador del Faro - Luna con datos reales]], [[Biblia de arte]], [[Catalogo de recursos]], [[Fase 0 - Analisis]], [[Propuesta_A]], [[Propuesta_B]], [[02_historia_existente]]"
---

# Plan de auditoría de construcción

> **Pedido de Guillermo (2026-11-12):** «empezar la auditoría de la construcción de pantallas de carga, menús, botones, jugabilidad, escenarios, caminos y texturas en orden. Por ejemplo, escenario 1) Habitación, 2) Telescopio, 3) Luna, y que se pueda llegar como un mundo abierto entre cada uno».
> **Qué es este documento:** el inventario de lo que existe, la lista de lo que falta, los criterios con los que se va a auditar cada elemento y el orden de trabajo. Ningún paso gasta créditos de Higgsfield.
>
> **Regla de Guillermo (2026-11-12): «primero debíamos validar los escenarios y el estilo del arte conmigo. Siempre, sin excepciones».**
> - Cada escenario pasa, en orden, por concepto → hoja de referencia → producción → motor, con el veredicto de Guillermo en cada paso.
> - Ningún carril construye un escenario, una pieza de arte o un estilo sin ese veredicto. Las «pruebas técnicas» con aspecto tampoco.
> - Por eso el carril C5 (prototipo de la Luna, `pruebas/luna_sueno/`) queda como medición técnica sin validar y se detiene hasta que la Luna tenga concepto y hoja aprobados.

## En cifras

| Medida | Valor |
|---|---|
| Escenarios pedidos | 3: Habitación, Telescopio y Luna, más 3 tramos que los unen (casa, Las Escalinatas y sendero) |
| Escenarios con algo jugable en el motor | **0**. Hay 2 pruebas técnicas: el sendero (vista fija con cámara libre) y el telescopio (pantalla fija) |
| Elementos transversales pedidos (carga, menús, botones, HUD, diálogos, guardado, transiciones, audio) | 0 en el proyecto nuevo; 6 en el prototipo descartado de la bóveda anterior, solo como lógica reutilizable |
| Recursos con ID en el catálogo | 104 conceptos v1 en 9 hojas, todos «espera veredicto». **0 para la Luna** |
| Mallas en el motor | 27 GLB por script y 8 de Tripo en `pruebas/escena_exploracion/` |
| Rendimiento medido en la HD 620 | Sendero: 48,3 fps a 720p (307 000 triángulos). Telescopio: 0,74 ms de GPU |
| Etapas de trabajo propuestas | 9, con 5 puertas de validación de Guillermo |
| Carriles de agentes en paralelo | 7 |

---

## 0. Decisiones que bloquean la construcción

La auditoría de lo existente puede empezar ya. Construir no, hasta que Guillermo decida esto:

| # | Decisión | Opciones | Qué bloquea |
|---|---|---|---|
| B1 | Aprobar la Fase 0, sobre todo D-001 (renderizador Mobile, 3D a 1280×720) | Aprobar o corregir | El esqueleto del juego y todas las cifras de rendimiento |
| B2 | **Meta de fps en la HD 620** | D-001 dice 30 fps estables; las propuestas A y B dicen 60 a 720p | Los umbrales de la sección 3 |
| B3 | Propuesta narrativa | A «Luz cenicienta» (88 min) o B «La bitácora de una noche» (85 min), o una mezcla | Las escenas, misiones y desbloqueos que se auditan en cada escenario |
| B4 | La frase «siendo vista con el Apolo que llegó a la Tierra» | A: verla junto a la etapa de descenso que sigue en la Luna. B: ser testigo en 1969 del regreso a la Tierra. C: ser vista desde la Tierra por su familia. D: ver la cápsula que volvió, fuera del sueño | Qué se construye en la Luna y si hace falta una cinemática de regreso |
| B5 | Tamaño del personaje | 12,5 % del alto (biblia) o 20,9 % (medido en el ancla) | Cámara, caminos, HUD y legibilidad |
| B6 | Inclinación de la cámara | La biblia dice unos 60°; la escena v1 usa 48° y 40° de campo, medidos contra el ancla | Todos los exteriores |
| B7 | Protagonista fija o creador de personaje | PER-01 fija, o PER-01 y PER-02 elegibles | Menú principal y guardado |
| B8 | Corte vertical | Propuesta A: unos 45 min primero (Habitación → Telescopio → sueño) | El alcance de las etapas 4 a 7 |

---

## 1. Inventario de lo que existe

**Estados usados**

- **Prueba:** demuestra una técnica; no es jugable.
- **Prototipo:** jugable de punta a punta, sin arte final.
- **Concepto:** imagen u hoja de referencia, sin nada en el motor.
- **Ausente:** no existe nada.

### 1.1 Por escenario

| Escenario | Qué hay | Dónde | Estado |
|---|---|---|---|
| **1 Habitación-taller** | Ancla de interiores `ANC_HUB` (diorama lateral en corte) | `Fase_1_Arte/Exploracion/Lote_01/L01_A_lowpoly_hub_gpt26.png` | Concepto aprobado (D-011) |
| | Hoja del taller: TAL-01 a TAL-14 (banco, osciloscopio, multímetro, maqueta de satélite, telescopio pequeño…) | `HR_TAL_v1.png` | Concepto · espera veredicto |
| | Cuarto 3D con jugador, cama, puerta y estantería, de la bóveda anterior | `Desktop\Juego\Juego_2d-hd\1_Mecanicas_y_Codigo\godot\scenes\bedroom.tscn` | Prototipo **con estilo descartado** (D-000). Sirve solo como lógica |
| | Malla, rig o escena del cuarto en el proyecto nuevo | — | **Ausente** |
| **1b Casa y E Las Escalinatas** | Hojas ARQ-01 a 12 y URB-01 a 12; mapa de la región | `HR_ARQ_v1.png`, `HR_URB_v1.png`, `L02_mapa_region.png` | Concepto |
| | Escena en el motor | — | **Ausente** |
| **S Sendero del arroyo** | Escena v1: terreno, arroyo, puente, escalinata, flamboyán, rocas, 28 000 briznas, 352 entradas en `layout.json` | `pruebas/escena_exploracion/` | **Prueba**. Cámara libre con flechas; no hay personaje controlable, colisiones ni interacción |
| | Bucle de 19 vueltas contra el ancla: ΔE de 27,96 a 19,36 | `capturas/iteraciones/BUCLE.md` | Cerrado; espera el veredicto de Guillermo |
| | Protagonista (Tripo, niveles de 1 500 y 3 000 triángulos) y Órbita con rig, `reposo` y `caminar` | `pruebas/escena_exploracion/tripo/` | Prueba. Órbita camina en el sitio |
| **2 Mirador y telescopio** | Luna real de JPL Horizons con texturas de LRO: fase y borde iluminado iguales a Horizons (12,15 % contra 12,2 %; 192,6°) | `pruebas/luna_telescopio/` | **Prueba**. Pantalla fija de una fecha; sin enfoque, zoom ni entrada salvo Esc |
| | Escena de noche del Mirador y maqueta de la interfaz del telescopio | `L03_mirador_noche_vista_juego.png`, `L03_ui_telescopio_luna.png` | Concepto · espera veredicto |
| | Hoja MIR-01 a 08 (faro, plataforma, telescopio, atril, guirnalda, cúpula) | `HR_MIR_v1.png` | Concepto |
| | Mirador 3D caminable | — | **Ausente** |
| **3 Luna del sueño** | Datos verificados del Apolo y del sitio (L1 a L13, R1 a R8) | `Fase_2_Narrativa/Investigacion/` | Investigación |
| | Hoja de referencia, terreno, etapa de descenso, herramientas, banderas o trajes | — | **Ausente**. No hay ni concepto |
| | Shader de la Luna del telescopio (reutilizable para la Tierra en el cielo) | `pruebas/luna_telescopio/luna.gdshader` | Prueba |

### 1.2 Transversal

| Elemento | Qué hay | Estado |
|---|---|---|
| Proyecto de Godot del juego (`juego/`), Git y Git LFS | Solo propuesto en la Fase 0, §5 | **Ausente** |
| Pantalla de carga | Idea: una página del cuaderno con un dato y su fuente (propuestas A y B) | **Ausente** |
| Menú principal, opciones, créditos, pausa | Prototipo de la bóveda anterior: título, continuar, creador, opciones, créditos y pausa en `scripts/main.gd` (477 líneas) | Lógica reutilizable; **estilo descartado** |
| Botones y tema de interfaz | Estilo «cuaderno de ingeniería» en la biblia, §6. El panel del telescopio usa papel `#F3E6CB`, tinta `#2F2A24` y cian `#62E4E0` | Prueba (solo el telescopio) |
| HUD de exploración | Rótulo de depuración en la escena v1 | **Ausente** |
| Diálogos | Decisión propuesta: Dialogue Manager 4.2.0 tras un adaptador propio (Fase 0, §5). Frases de Órbita fijas en el telescopio | **Ausente**; el complemento no se ha probado en 4.7.2 |
| Cuaderno, inventario, mapa y viaje rápido | Maqueta del mapa `ANC_MAPA` | Concepto |
| Guardado | JSON con versión (`journey_v1.json`) y `preferences.cfg` en la bóveda anterior. Propuesto: JSON validado con migraciones y 2 respaldos | Lógica reutilizable |
| Transiciones entre zonas | Propuestas: 3 a 5 umbrales con carga de 1 a 3 s | **Ausente** |
| Controlador del personaje, colisiones, interacción | `player.gd` (CharacterBody3D, 2,05 m/s al caminar y 3,45 al correr) en la bóveda anterior | Lógica reutilizable; nada en el proyecto nuevo |
| Audio | Nada: ni buses, ni ambiente, ni pasos, ni música | **Ausente** |
| Idiomas | Decisión propuesta: gettext con español e inglés. Los textos de las pruebas están escritos en el código | **Ausente** |
| Tipografía | DotGothic16 propuesta, sin probar. Atkinson (OFL) y Cinzel en la bóveda anterior | Sin decidir |
| Texturas pintadas 2D-HD | Ninguna: el acabado sale del color por vértice y de los shaders `facetado`, `follaje`, `agua` y `personaje` | Prueba; las pinceladas por shader «casi no se notan» (vuelta 12) |

### 1.3 Herramientas que ya sirven para auditar

| Herramienta | Qué mide |
|---|---|
| `herramientas/godot_captura.py` | Captura o medición sin cuelgues en la HD 620 |
| `escena.gd --medir=<s>` | fps medios, ms por cuadro (media y p95), primitivas y llamadas de dibujo |
| `pruebas/bench_render/` | Comparación de renderizadores con escenas sintéticas |
| `herramientas/comparar_ancla.py` y `color_zonas.py` | ΔE por bloques y por zona contra un ancla |
| `herramientas/paleta.py comparar` | Qué parte del color cae en la paleta maestra (detecta desvíos de familia, no de estilo) |
| `herramientas/camara_ancla.py` | Punto del mundo que el ancla pinta en un píxel |
| `herramientas/luna_medir.py` | Fracción iluminada, ángulo del borde y orientación de la textura de la Luna |
| `herramientas/mallas/revisar_textura_glb.py` | Texturas grises fallidas de Tripo |

---

## 2. Lo que falta

### 2.1 Por escenario

| Escenario | Jugabilidad | Escenario y caminos | Texturas y luz |
|---|---|---|---|
| **1 Habitación** | Caminar, mirar e interactuar con 5 a 8 objetos; rompecabezas del seguidor (osciloscopio TAL-02); circuito de Pegaso (B); cama con «Dormir» y «Soñar otra vez»; escalera a la casa | Diorama del cuarto-taller con cámara lateral (`ANC_HUB`); la cámara y el paso a la vista alta del exterior | Luz de mañana y de noche (biblia, §7); lámpara TAL-09; ventana con la Luna |
| **1b / E Casa y barrio** | Desayuno y diálogo; recolección (COL-03, 05, 06, 07); kiosco de Lidia; puesto de Sam | Planta baja, puerta, Las Escalinatas con escalones numerados (ARQ-12), Plaza de las Iguanas y Mercado | Tarde y noche; faroles y guirnaldas |
| **S Sendero** | Personaje controlable, colisiones, Órbita que lo sigue, fauna, recolectables con destello cian | Unir la escena v1 con la plaza y con el Mirador; versión de noche | Texturas pintadas del suelo y la hierba (pendiente 2 del bucle); copa del flamboyán; versión de noche |
| **2 Telescopio** | Buscar, enfocar y marcar terminador, mares y luz cenicienta; seguimiento manual (A) o montura ecuatorial (B); tarjetas o diapositivas; entrar y salir del ocular | Mirador 3D (MIR-01 a 08), subida desde el sendero, atajo (B) | Noche con luz fría (biblia, §7); **ángulo paraláctico en cada instante** (pendiente de la prueba) |
| **3 Luna** | Caminar a 1/6 g con inercia; 4 herramientas; protocolo de foto con gnomon; anillo de 75 m alrededor del sitio del Apolo 11; dos banderas; regreso en 5 o 7 pasos | Llegada, campo de cráteres, anillo y loma; unos 450 × 450 m según A | **Paleta y luz lunar sin definir en la biblia**; regolito; Tierra en el cielo; trajes originales sin insignias |

### 2.2 Transversal

| Elemento | Qué falta |
|---|---|
| Pantalla de carga | Diseño (página del cuaderno con dato y fuente), precompilación de shaders en la primera, medición del tiempo |
| Menú principal | Nuevo, Continuar, Opciones, Créditos y Salir; creador si B7 lo pide; fondo vivo |
| Pausa y opciones | Volumen por bus, escala de texto, remapeo, reducir movimiento, modos de daltonismo, calidad gráfica (perfil HD 620) |
| HUD | Objetivo actual, aviso de interacción, Órbita, reloj del cielo (B) |
| Botones | Tema único de interfaz: estados normal, foco, pulsado y desactivado; teclado, ratón y mando |
| Diálogos | Burbujas de 2 renglones, elecciones, voz de Órbita (cuaderno despierto, radio en el sueño) |
| Cuaderno | Inventario, bitácora con sellos «Dato», «Simulación» y «Sueño», mapa y viaje rápido |
| Guardado | Partida con versión, migraciones y 2 respaldos; estado del mundo (banderas plantadas, objetos recogidos) |
| Transiciones | Escalera, puerta, curva del camino, cama → Luna (6 a 40 s según la propuesta) y Luna → cama |
| Caminos | Trazado continuo entre los 6 nodos, señalización para el jugador y bloqueos con motivo en la historia |
| Audio | Buses, ambiente por zona, pasos por superficie, música adaptativa y silencio del vacío lunar (solo traje, respiración y radio) |
| Accesibilidad | Subtítulos, contraste, tamaño de texto, sin dependencia del color cian para información crítica |
| Créditos de datos | Atribución de NASA, JPL y LRO en créditos y en las fichas; sin logotipos ni nada que sugiera respaldo |

---

## 3. Criterios de la auditoría

Cada elemento recibe una ficha con ID `AUD-NNN`, la evidencia (captura con la cámara real del juego o una medición), el veredicto («cumple», «no cumple» o «no aplica») y quién lo revisó. **Nada se marca «cumple» sin evidencia.** Las cifras marcadas *(propuesta)* son metas a aprobar por Guillermo.

### 3.1 Comprobaciones comunes a todo elemento

| Eje | Comprobación | Umbral | Cómo se mide |
|---|---|---|---|
| **Legibilidad** | Se entiende en 2 s a la distancia de juego | Silueta reconocible al tamaño de encuadre elegido en B5 | Captura con la cámara real; prueba en escala de grises |
| | Texto legible | ≥ 24 px de alto de letra a 1080p y ≥ 16 px a 720p *(propuesta)* | Captura a 720p y en pantalla completa a 1080p |
| | Contraste del texto | ≥ 4,5:1 (WCAG 1.4.3) | Muestreo de color en la captura |
| **Biblia de arte** | Paleta | ≥ 90 % del color dentro de la paleta maestra *(propuesta)*; la Luna y la Tierra de NASA quedan exentas | `paleta.py comparar` |
| | Cian | Solo tecnología, datos, interacción y recolectables | Revisión de la captura |
| | Facetas y materiales | Facetas con degradado pintado, mates, sin texturas fotográficas | Revisión de la captura |
| | Luz | La del momento del día (biblia, §7) | Revisión de la captura |
| | Reglas fijas | Sin insignias, logotipos ni emblemas de la NASA ni de misiones; banderas con trato respetuoso | Lista de comprobación |
| **Rendimiento (HD 620, Mobile, 1280×720)** | fps | Media ≥ 60 o ≥ 30 según B2; **p95 ≤ 33,3 ms siempre** | `--medir=6` tras 2 s de calentamiento, sin sincronía vertical |
| | Geometría | ≤ 100 000 triángulos visibles y ≤ 300 llamadas de dibujo (Fase 0, §2.6) | Monitores de Godot |
| | Memoria | ≤ 2 GB de RAM del proceso *(propuesta, el equipo tiene 7,9 GB)* | Administrador de tareas o `Performance` |
| | 1080p | Se mide también en pantalla completa | `--fullscreen` (lección de Memory) |
| **Accesibilidad** | Entrada | Todo se usa con teclado, ratón y mando; controles remapeables | Prueba manual |
| | Información | Nada crítico solo por color; nada crítico solo por sonido | Prueba en escala de grises y sin audio |
| | Movimiento | Opción para reducir el movimiento de cámara y los destellos | Prueba manual |
| | Tiempo | Sin límites de tiempo que castiguen; el reloj del cielo de B nunca causa derrota | Revisión del diseño |
| **Historia** | Lugar en el guion | Cada elemento cita su escena de la propuesta elegida en B3 | Tabla de trazabilidad |
| | Datos | Cada cifra en pantalla lleva su código de fuente (A, E, L, R) o el sello «Sueño» | Revisión del texto |
| | Sin examen | Fallar muestra la consecuencia y deja reintentar | Prueba manual |

### 3.2 Comprobaciones por tipo de elemento

| Elemento | Comprobaciones propias | Umbral |
|---|---|---|
| **Pantalla de carga** | Tiempo desde la acción hasta el primer cuadro jugable | ≤ 3 s en la HD 620 (propuesta A); ≤ 2 s en umbrales de puerta (propuesta B) |
| | Cuadro negro o congelado | ≤ 0,5 s *(propuesta)* |
| | Contenido | Un dato real con fuente o una ficha del cuaderno; se puede leer completo en el tiempo de carga |
| | Primer arranque | Shaders precompilados en la carga inicial; sin tirones al entrar a cada zona (p95 del primer minuto) |
| **Menús** | Respuesta | El foco reacciona en ≤ 100 ms *(propuesta)* |
| | Navegación | Foco visible siempre; Esc o B vuelve un nivel; ningún callejón sin salida |
| | Estado | «Continuar» desactivado sin partida; la opción cambiada se guarda al salir |
| **Botones** | Área | ≥ 44 × 44 px a 1080p (WCAG 2.5.5) |
| | Estados | Normal, foco, pulsado y desactivado distinguibles en escala de grises |
| | Coherencia | Un solo tema de interfaz para todo el juego |
| **HUD** | Ocupación | ≤ 10 % de la pantalla en exploración *(propuesta)* |
| | Conflicto | No tapa al personaje en ninguno de los dos encuadres de B5 |
| **Diálogos** | Formato | ≤ 2 renglones por burbuja; texto vía gettext (`.po`) |
| | Ritmo | Avance manual; opción de texto instantáneo |
| **Guardado** | Integridad | Guardar, cerrar a la fuerza y cargar: el estado coincide; el archivo dañado recurre al respaldo |
| | Versión | Una partida de la versión anterior carga con su migración |
| **Jugabilidad** | Control | Personaje responde en ≤ 1 cuadro; velocidad de 3 m/s en la Tierra y unos 4 m/s a saltos en la Luna (supuestos de A) |
| | Duración | Cada escena dura lo que dice su tabla, ±30 %; la ruta principal ≥ 60 min con 3 jugadores cronometrados |
| | Física lunar | Gravedad de 1,624 m/s² (L6); la inercia exige frenar con anticipación |
| **Escenarios** | Encuadre | Captura con la cámara real comparada con su ancla: ΔE de `comparar_ancla.py` como orientación, veredicto de Guillermo como criterio |
| | Escala | Proporciones de la biblia: estudiantes de 3 cabezas, gato a la rodilla |
| **Caminos** | Continuidad | Se llega a pie de cada nodo al siguiente sin carga salvo en los umbrales aprobados |
| | Lectura | El camino se distingue de la hierba en escala de grises desde la cámara alta |
| | Medidas | Ancho del sendero de 1,05 a 1,5 m (medido en el ancla); recorrido coherente con los minutos de la tabla (por ejemplo, 350 m de subida en 2.1 de A) |
| | Bloqueos | Todo camino cerrado tiene un motivo dicho en la historia (por ejemplo, Órbita: «Con tanto sol no vas a ver la Luna») |
| **Texturas** | Tamaño | Protagonista 1024²; gato, NPC y props 512² (Fase 0, §2.6); atlas compartidos en escenarios |
| | Calidad | Desviación de color > 3 en cada textura de Tripo (detecta el gris plano) |
| | Origen | Solo datos de NASA son fotográficos; cada textura externa con su SHA-256 y crédito |
| **Audio** | Mezcla | Buses separados (música, ambiente, efectos, voz) con volumen en opciones |
| | Coherencia | Pasos por superficie; en la Luna no hay sonido exterior |
| | Licencia | Ninguna pista con derechos de terceros; las de NASA SVS con música quedan excluidas |

### 3.3 Hallazgos que ya se ven sin auditar

| Hallazgo | Evidencia | Peso |
|---|---|---|
| El sendero supera el presupuesto de la Fase 0: 307 000 triángulos frente a 100 000, y 28 000 briznas frente a 20 000 | `BUCLE.md`, vuelta 15; [[Escena de exploracion v1]] | Alto si B2 fija 60 fps: hoy da 48,3 y 44,2 fps |
| No hay personaje controlable, colisiones ni interacción en ningún proyecto nuevo | Búsqueda de `CharacterBody`, `CollisionShape` y `NavigationAgent3D` en `pruebas/`: 0 resultados | Bloquea la auditoría de jugabilidad y caminos |
| No hay nada de audio | Búsqueda de `AudioStream` en `pruebas/`: 0 resultados | Bloquea la auditoría de audio |
| La Luna no tiene hoja de referencia ni paleta | [[Catalogo de recursos]] y [[Biblia de arte]] | Bloquea el escenario 3 |
| La biblia y la escena v1 no coinciden en la cámara (60° frente a 48°) ni en el tamaño del personaje (12,5 % frente a 20,9 %) | [[Biblia de arte]] §5, `layout.json` | Medio |
| El texto de las pruebas está escrito en el código, sin gettext | `telescopio.gd`, `escena.gd` | Bajo hoy, alto al traducir |
| La escena v1 no define modo de estiramiento de ventana; el telescopio sí (`canvas_items`) | `project.godot` de cada prueba | Bajo: se resuelve en el esqueleto |

---

## 4. Orden de trabajo

El orden sigue el pedido: primero lo que se ve antes de jugar (carga, menús, botones), luego la jugabilidad y los escenarios en orden 1, 2 y 3, y al final los caminos y las texturas que los unen.

| Etapa | Qué | Depende de | Créditos | Puerta de Guillermo |
|---|---|---|---:|---|
| **0** | Decisiones B1 a B8 | — | 0 | Sí: sin ellas no se construye |
| **1** | Auditoría de lo existente: medir y capturar el sendero y el telescopio a 720p y 1080p, revisar el prototipo anterior, llenar las fichas `AUD-` | Puede empezar ya | 0 | No: informe |
| **2** | Esqueleto `juego/`: Git y LFS, `Main` persistente, gestor de zonas, entrada remapeable, guardado JSON, gettext, perfil gráfico de la HD 620 | B1, B2 | 0 | No: pruebas automáticas con GUT |
| **3** | Transversal, en el orden pedido: pantalla de carga → menú principal → pausa y opciones → tema de botones → HUD → diálogos → cuaderno | 2; B7 para el menú | 0 | **Puerta 1:** capturas de carga, menús y botones |
| **4** | Escenario 1 Habitación: volumen gris → jugabilidad (interactuables, seguidor, cama) → arte por script con TAL → luz de mañana y noche → audio | 2, 3; B3; veredicto de `HR_TAL_v1` | 0 | **Puerta 2:** recorrido grabado del cuarto |
| **5** | Tramos 1b, E y S: casa, Las Escalinatas, plaza y sendero v1 con personaje y colisiones; recorte del sendero al presupuesto de B2 | 4; veredicto de la escena v1 | 0 | Incluida en la puerta 3 |
| **6** | Escenario 2 Telescopio: Mirador 3D con MIR, entrada al ocular desde el mundo, interacción del telescopio, ángulo paraláctico | 5; B3 | 0 | **Puerta 3:** del cuarto al ocular a pie |
| **7** | Escenario 3 Luna: hoja de referencia lunar → volumen gris → caminar a 1/6 g → muestras → anillo de 75 m → banderas → regreso | 4 (cama); B3, B4; partida aprobada para la hoja y los trajes | Partida aparte | **Puerta 4:** el sueño completo |
| **8** | Mundo abierto: transiciones, viaje rápido, día y noche, persistencia, recorrido cronometrado ≥ 60 min con 3 jugadores, texturas pintadas finales | 4 a 7 | Según partida de texturas | **Puerta 5:** recorrido completo |

```
B1-B8 ─┬─> 2 Esqueleto ─> 3 Carga/menús/botones ─> 4 Habitación ─┬─> 5 Tramos ─> 6 Telescopio ─┐
       │                                                         └─> 7 Luna (cama) ────────────┼─> 8 Mundo abierto
1 Auditoría de lo existente (ya) ──────────────────────────────────────────────────────────────┘
```

**Corte vertical (si B8 lo aprueba):** las etapas 4, 6 y 7 se hacen primero solo con las escenas del corte (en A: 1.1, 1.2, 2.2, 2.3 y de 3.1 a 3.5), y la etapa 5 se reduce a un tramo del sendero.

### 4.1 Agentes en paralelo

Cada carril entrega archivos y capturas; otro agente revisa antes de que se usen (lección «verificar lo delegado»). Ninguno gasta créditos de Higgsfield. Para la web, WebSearch y WebFetch; Firecrawl no.

| Carril | Agente | Trabajo | Puede empezar | Entrega |
|---|---|---|---|---|
| **C1 Medición** | Claude (subagente) | Etapa 1: `--medir` y capturas del sendero y del telescopio a 720p y 1080p; tiempos de arranque; fichas `AUD-001` en adelante | Ya | `Auditoria/` con capturas y cifras |
| **C2 Interfaz** | Claude (subagente) | Etapa 3: maquetas en Godot de carga, menús y botones sobre el tema del cuaderno; contraste y tamaños medidos | Tras B1 y B7 | Escena de interfaz y capturas |
| **C3 Esqueleto** | Claude (subagente) | Etapa 2: proyecto `juego/`, gestor de zonas, guardado, entrada y gettext, reutilizando la lógica de `main.gd` y `player.gd` de la bóveda anterior | Tras B1 | Proyecto y pruebas GUT |
| **C4 Habitación** | Claude (subagente) | Etapa 4: volumen gris del diorama y props TAL por script sobre `herramientas/mallas/nucleo.py` | Tras C3 y el veredicto de `HR_TAL_v1` | Escena y capturas con la cámara real |
| **C5 Luna** | Claude (subagente) | Etapa 7: volumen gris del terreno lunar, etapa de descenso sin insignias y prueba de rendimiento con rocas en MultiMesh | Tras B4; la prueba de rendimiento puede ir ya | Escena de prueba y cifras |
| **C6 Investigación** | Codex (`codex_lote.py`, pocas tareas a la vez) | Guías de accesibilidad con cifras citables; verificar los datos pendientes (bandera de Ecuador, disco del Apolo 11, Luna del 13-11-2026) | Ya, si queda cupo de Codex | Informes en `Auditoria/Investigacion/` |
| **C7 Revisión** | Claude (subagente independiente) | Revisa cada entrega contra la sección 3 antes de mostrarla a Guillermo | Desde la primera entrega | Veredicto por ficha |

**Límites:** como máximo 3 carriles con Godot a la vez, porque la HD 620 mide mal con varios procesos (la medición de la escena v1 fue un piso por tener Blender abierto). C1 mide con el equipo libre.

---

## 5. Preguntas para Guillermo

1. ¿Apruebas la Fase 0 y qué meta de fps quieres en la HD 620: 30 o 60 a 720p? (B1, B2)
2. ¿Propuesta A, B o una mezcla? (B3)
3. ¿Qué quisiste decir con «siendo vista con el Apolo que llegó a la Tierra»: A, B, C, D o una mezcla? La propuesta A recomienda A como jugabilidad y C como cierre. (B4)
4. ¿Personaje al 12,5 % o al 20,9 % del alto, y cámara a 48° o a 60°? (B5, B6)
5. ¿Protagonista fija o creador de personaje? (B7)
6. ¿Primero el corte vertical de unos 45 min? (B8)
7. ¿Arranco ya la etapa 1 (auditoría de lo existente, 0 créditos) con los carriles C1 y C6?
