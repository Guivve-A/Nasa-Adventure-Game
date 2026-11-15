# Inventario para la presentación

> Qué existe del proyecto «Luz cenicienta» al 2026-11-15, en qué estado está y con qué archivo se comprueba cada cifra. Es la base de [[Guion del video demo]], [[Guion del expositor]] y [[Tarjeta del expositor]]. Regla: lo que no está aquí con su origen no se dice en el video ni en el escenario.

**Estados:** **probado** = existe y pasa una prueba automática o una medición registrada; **provisional** = jugable, pero sin concepto validado por Guillermo; **en producción** = existe en parte o se está generando ahora.

## 1. El reto y cómo se juzga

### 1.1 Los dos enunciados

| Enunciado | Qué pide | Origen |
|---|---|---|
| **Space Mission Design Game** (reto global 2026, temática «Games», nivel intermedio y principiante) | Un juego interactivo para vivir el diseño y la gestión de una misión completa, «de concepto a operación», con mecánicas, visualizaciones, puntuación y escenarios que obliguen a resolver problemas y a hacer compromisos. Sugiere: accesible a todos los niveles, de 1 a 4 jugadores, empezar por el objetivo de la misión, que cada decisión tenga consecuencia, límites de presupuesto, masa, energía, comunicaciones y vida útil, y conceptos explicados con sencillez | `spaceappschallenge.org/2026/challenges/space-mission-design-game/` (consultado el 2026-11-15) |
| **Tu primera base espacial** (enunciado local, en la carpeta del proyecto) | «Diseña un juego para gestionar una base lunar o marciana: equilibra soporte vital, radiación, energía y alimentos» | `Referencias/Reto_base_espacial/reto_tu_primera_base_espacial.png` |

El evento de 2026 fue el 14 y 15 de noviembre; el juzgamiento empieza el 16.

### 1.2 Los cinco criterios y nuestra respuesta

Criterios oficiales (Judging & Awards Guide de Space Apps): impacto, creatividad, validez, relevancia y presentación.

| Criterio | Qué mira el jurado | Cómo responde el proyecto | Prueba |
|---|---|---|---|
| **Impacto** | Problema que ataca y a cuántos inspira o ayuda | Diseñar misiones suele aprenderse en teoría. El juego lo vuelve experiencia, en español y desde Guayaquil, y corre en un portátil escolar con gráfica integrada | fps medidos (§4); fichas con fuente (§3) |
| **Creatividad** | Originalidad o mejora significativa | Una aventura low-poly con acabado pintado (2.5D) y un gato científico; 9 minijuegos arcade, cada uno con una idea real; un telescopio con la Luna real de una noche concreta; una cinemática de homenaje al Apolo 11 | §2, §3 y §5 |
| **Validez** | Base científica, factibilidad, usabilidad | Datos verificados con fuentes primarias; la Luna se mide contra JPL Horizons; todo se demuestra jugable con teclado simulado; corre en hardware modesto | §3, §4 |
| **Relevancia** | Responde al reto y usa datos de NASA como núcleo, no como adorno | Base lunar y marciana con oxígeno, energía, alimentos y radiación (reto local). Arco de misión: armar el satélite, rastrearlo, ponerlo en órbita, aterrizar, operar y volver (reto global). Datos de LRO y JPL Horizons dentro del juego | §2.3, §3 |
| **Presentación** | Claridad, historia, estructura; también la demo | Video de 2:30 con guion de expositor de 1:30 sincronizado | [[Guion del video demo]] |

**Huecos honestos frente al reto global** (no se dicen como hechos; se responden si preguntan): no hay todavía presupuesto ni masa como recursos, ni modo de hasta 4 jugadores, ni una pantalla inicial donde se elija el objetivo de la misión. Sí hay decisiones con consecuencia: el aterrizaje programado de Marte (aterrizaje suave, duro o nave perdida, con la causa explicada) y las barras de la base.

**Aviso:** la guía global limita el video de envío a **30 s** (y las diapositivas a 7). El video de 2:30 sirve para la presentación local; para el envío global hace falta un corte de 30 s (ver dudas en [[Guion del video demo]] §6).

## 2. El juego

### 2.1 Mundo y arte

| Qué | Estado | Cifra comprobada | Origen |
|---|---|---|---|
| Motor | probado | Godot 4.7.2, renderizador Mobile, 1280 × 720 | `CLAUDE.md`; `juego/project.godot` |
| Código | probado | 20 255 líneas en los `.gd` de `juego/` (con pruebas, comentarios y líneas en blanco): «más de 20 000 líneas» | `find juego -name "*.gd" \| xargs cat \| wc -l` (2026-11-15) |
| Escenarios | Habitación y Sendero: validados por Guillermo. Plaza, Mirador y Luna: **provisionales**. Luna v2: **en producción** | 5 zonas: `habitacion`, `ciudad` (Plaza de las Iguanas), `sendero`, `mirador`, `luna` | `juego/zonas/*/zona.json`; `Construccion/BUCLE_ESTILO.md` filas 3 y 5j |
| Estilo | probado | Low-poly pintado a mano (D-011) y acabado 2.5D (D-015) aprobados | `Memory.md` §2 |
| Misiones | probado | 10 misiones jugables (de `m1_convocatoria` a `m10_referencia_fija`). `s1_base` («Tu primera base espacial») existe pero no se puede completar hasta que se integren `base_luna` y `base_marte` (en producción) | `juego/datos/misiones.json`; `juego/zonas/ciudad/ciudad.gd` |
| Protagonista y Órbita | probado | Protagonista v9 con 82,1 % de parecido a su hoja; Órbita con rig por script (Rigify) y pistas en tres niveles | `BUCLE_ESTILO.md` (tabla de estilo); `Memory.md` (lecciones de rig); `misiones.json` (`_nota`) |
| Mapa del mundo ilustrado | probado (capturado) | Cinco lugares, conexiones y candados (tecla M) | `juego/interfaz/mapa.gd`, `juego/datos/mapa.json`, `Construccion/Capturas/mapa_del_mundo.png` |
| Pantallas de carga pintadas | arte hecho; integración **en producción** (sin revisar) | 5 láminas finales del lote 08 | `Fase_1_Arte/Exploracion/Lote_08/L08_carga_*.png` |
| Minimapa con el objetivo | entregado por un agente, **sin revisión final** | — | `juego/interfaz/minimapa.gd`; `Construccion/Capturas/minimapa_*.png` |
| Sonido | probado por su agente | 11 archivos de sonido hechos para el juego (pasos, paso lunar, salto, recoger, umbral, logro, página, radio, golpe de mástil, ambiente de la Luna y del sendero) | `juego/audio/*.ogg` |
| Hojas de referencia | arte hecho; veredicto de Guillermo pendiente | 9 hojas, 104 recursos con ID | `Fase_1_Arte/Hojas_de_referencia/HR_*_v1.png`; `trabajos.md` (lote 03) |

### 2.2 Los 9 minijuegos arcade

Todos son arcade a pantalla completa (320 × 180 píxeles gordos sobre 1280 × 720) y se ganan solo con teclas simuladas. Estado: **probado**.

| Orden | Carpeta | Título en el juego | Idea real (una palabra para el montaje) | Ficha del cuaderno | Comprobaciones con teclado (`prueba_manos.gd`) |
|---|---|---|---|---|---|
| 1 | `seguidor` | El seguidor que tiembla | **Control** (inercia y prealimentación) | `realimentacion` | 16 |
| 2 | `antena` | Rastreo | **Rastreo** (45 paquetes en tres pasadas) | `estacion_cotopaxi` | 9 |
| 3 | `satelite` | Un cubo de 10 cm | **CubeSat** | `pegaso` | 28 |
| 4 | `telescopio` | La Luna sonriente | **Observación** (la Luna del 12 de noviembre, 12,2 %) | `luz_cenicienta` | 29 |
| 5 | `linea_tiempo` | La escalinata del tiempo | **Historia** (hitos espaciales de Ecuador) | `disco_apolo11` | 30 |
| 6 | `muestras` | Recolector lunar | **Herramientas** (herramientas del Apolo 11) | `herramientas_apolo11` | 66 |
| 7 | `banderas` | Dos banderas, un cielo | **Cooperación** (dos banderas juntas) | `bandera_lunar` | 11 |
| 8 | `regreso` | Volver como el módulo de mando | **Reentrada** | `modulo_mando` | 6 |
| 9 | `orbita` | Ni se cae ni se escapa | **Órbita** (Pegaso, 627 × 654 km en pantalla) | `pegaso` | 17 |
| | | | | **Total** | **212** comprobaciones, 0 fallos |

Origen: `juego/minijuegos/*/minijuego.json`; cifras de `BUCLE_ESTILO.md` fila 5j (2026-11-15, 09:15). Lámina: `Construccion/Capturas/vuelta6_arcade_nueve.jpg`. Prueba conjunta: los 9 se ganan en dificultad 1 y 3 y se pueden perder con causa (fila 5f).

### 2.3 La base en la Luna y en Marte (juegos de Jean, Joel y Domenica)

Proyectos de Godot 4.7 aparte, en píxel-art a 640 × 360. **Solo lectura.** Se abrirán desde los libros de la biblioteca de la Plaza: esa integración está **en producción** (hoy corren aparte; `juego/minijuegos/` no tiene `base_luna` ni `base_marte` todavía).

| Qué | Estado | Cifra | Origen |
|---|---|---|---|
| **Misión Artemis** (base del polo sur lunar, viaje y Marte provisional) | probado por su prueba automática | 4 barras: **oxígeno, energía, alimentos y radiación** (las cuatro del reto local). Cohete en 4 fases; 4 de hielo; 3 paneles; lluvia solar con cúpulas como refugio. Si el oxígeno llega a cero o la radiación al máximo, se pierde la mitad de la carga. Prueba: juega sola de punta a punta y comprueba **31 pasos** | `Misión Artemis/LEEME.md`; `Misión Artemis/capturas/02_lluvia_solar.png` |
| **Misión Artemis — Marte** (sección de Domenica) | probado por su prueba automática | «Siete minutos de terror»: se programa el aterrizaje (paracaídas, cohetes, navegación) y se prueba en un simulador: aterrizaje suave, duro o nave perdida, siempre con la causa. Base con hábitat, paneles, extractor de oxígeno, taladro de hielo e invernadero; tormenta de polvo; cuaderno de campo de 11 páginas con dato real y fuente. Prueba: **36 de 36** | `Marte_Gravedad2DHD/Marte_Gravedad2DHD/Mision_Artemis_Marte/LEEME.md` |
| Capturas existentes | — | 14 capturas de Misión Artemis; Marte no tiene capturas: hay que grabarlo | `Misión Artemis/capturas/01_inicio.png` a `14_fin.png` |

En el juego de Marte se plantan las banderas de Estados Unidos, Ecuador y de IEEE IAS — ESPOL (ver dudas).

## 3. Datos reales

| Qué | Estado | Cifra comprobada | Origen |
|---|---|---|---|
| Cuaderno de fichas | probado | **55 fichas**, cada una con fuente: 39 «Dato verificado», 6 «Dato medido», 4 «Cálculo propio», 4 «Concepto», 2 «Sueño». Temas: Luna 14, Ecuador 12, Apolo 12, Satélites 7, Control 6, Derecho espacial 4 | `juego/datos/datos_espaciales.json`; trazabilidad en `juego/datos/FUENTES.md` |
| Luna del telescopio con datos de NASA | **prueba técnica** (fuera del juego principal) | Texturas NASA SVS 4720 (LRO LROC WAC y LOLA). Luna de Guayaquil del 12-11-2026 a las 19:30: medido **12,15 %** iluminado y borde a **192,6°**; JPL Horizons: **12,2 %** y 192,6°. Correlación de orientación de la textura: 0,990 | `pruebas/luna_telescopio/`; `Propuestas/Capturas/luna_telescopio.png`; `trabajos.md` (2026-11-12) |
| Datos de NASA dentro del juego | probado | El minijuego del telescopio lleva la misma efeméride (12,2 %, fuente «JPL Horizons (DE441) · texturas NASA SVS 4720») | `juego/minijuegos/telescopio/datos/luna.json`, `texturas/texturas.json` |
| Hechos del Apolo 11 | verificados con fuentes primarias | Primer paso: 21-07-1969 a las 02:56:15 UTC = **21:56 del 20 en Guayaquil** (*El Universo* lo publicó como «9.56 del Ecuador»). Audiencia: **más de 500 millones** (NASA; Smithsonian) | `Fase_2_Narrativa/Cinematica_apertura/01_hechos_verificados.md` puntos 3 y 8 |
| Verificación de la Fase 2 | hecho | 03a: 18 confirmados, 3 corregidos, 5 sin verificar; 03b: 17 confirmados y 3 corregidos | `trabajos.md` |

Rótulo permitido: «datos abiertos de la NASA» y las fuentes (LRO, JPL Horizons, SVS). Nunca el logotipo ni la insignia.

## 4. Ingeniería y proceso

| Qué | Estado | Cifra | Origen |
|---|---|---|---|
| fps en Intel HD 620 a 1280 × 720 | medido el 2026-11-15, 11:59, sin otros procesos de Godot (`--medir=5`) | Habitación 56,3; **Plaza 38,3**; Sendero 41,1; Mirador 40,1; Luna 60,3. Como la Plaza baja de 40, el video no lleva cifra de fps: «Corre en una Intel HD 620». (Medición anterior, vuelta 3: de 43,6 a 59,3, antes de la Plaza v2 y la Luna v2) | `material/fps_medido.txt`; `BUCLE_ESTILO.md` filas 3 y 5j |
| Equipo de medición | medido | i5-7200U, 8 GB, Intel HD 620 | `Memory.md` §3 |
| Historia completa con teclas simuladas | probado (vuelta 4) | **117** comprobaciones, 0 fallos (WASD, E, diálogos y umbrales) | `BUCLE_ESTILO.md` fila 4 |
| Minijuegos con teclas simuladas | probado (vuelta 5j) | **212** comprobaciones, 0 fallos | §2.2 |
| Total usado en el video (v2) | corrido el 2026-11-15, 12:00 a 12:16 | **212 comprobaciones con teclas simuladas en los 9 minijuegos, 0 fallos** (seguidor 16, antena 9, satélite 28, telescopio 29, línea de tiempo 30, muestras 66, banderas 11, regreso 6, órbita 17). El recorrido completo (`--prueba=recorrido_manos`) **no** se cuenta: la corrida de la mañana dio 126 y 7 fallos (Mirador) y se volvió a correr (ver LEEME de la presentación). El «329» de la v1 ya no vale | `material/consola_muestras_manos.txt`; LEEME de la presentación |
| Otras pruebas entregadas por agentes, sin revisión final | — | núcleo 22, manos 23, zonas 332, zona:ciudad 87 | `BUCLE_ESTILO.md` fila 5j. No se usan en pantalla |
| Del concepto al motor | hecho | Ancla de vista `L02_exploracion_camara_alta.png` → hojas `HR_*_v1.png` → Sendero en el motor (ΔE 19,4 contra el ancla) | `Fase_1_Arte/Exploracion/Lote_02/`, `Hojas_de_referencia/`, `Construccion/Capturas/sendero_jugable.png`; `Memory.md` D-015 |
| Hoja → modelo 3D | hecho | Protagonista v8T: 81,1 % de parecido; v9: 82,1 % | `Fase_1_Arte/Modelado/Lote_04/parecido/hoja_vs_v8T.png`; `Memory.md` D-017 |

## 5. Cinemática de apertura «Un punto de luz»

| Qué | Estado | Origen |
|---|---|---|
| Guion y storyboard (15 planos) | hechos y verificados | `Fase_2_Narrativa/Cinematica_apertura/` |
| Fotogramas finales K03 a K12 | hechos | `Fase_1_Arte/Exploracion/Lote_09/L09b_K*_final*.png` |
| Bandera (variante A) y protagonista (dirección «cine») | elegidas por Guillermo | `L09d_K13a_final.png`, `L09d_K13b_final.png`, `L09c_P14c_C_cine_gpt.png` |
| Video (clips) | **en producción**: al 2026-11-15, 09:40 no se había generado ningún clip | `Fase_1_Arte/Exploracion/Lote_10/Lote 10 - Video de los movimientos I y II.md` |

Fotogramas útiles para el gancho: K03 (torre), K04a y K04b (antes y durante la ignición; usar `L09b_K04a_final_r1.png`), K05 retocado sin placas (`Lote_10/fotogramas/L10_K05_placas_lisas.png`), K06 (chispa), K10 (televisor), K11a y K11 (la huella), K12 v2 (Guayaquil de noche), K13a (bandera y Tierra), P14c C (el despertar). **K07 (Tierra) no es apto** según la revisión del lote 10: no usarlo. Todas llevan el sello «Imágenes recreadas con IA».

## 6. Lo que NO se dice

- Que las bases de la Luna y de Marte ya se abren desde el juego principal (integración en curso).
- Que la Luna del telescopio con texturas LRO es el minijuego (es una prueba técnica; el minijuego usa su efeméride).
- Que la cinemática está terminada (está en producción).
- Que hay presupuesto, masa o multijugador.
- Que lo validó o respalda la NASA.
- Cifras de pruebas sin volver a correrlas el día de la presentación.
