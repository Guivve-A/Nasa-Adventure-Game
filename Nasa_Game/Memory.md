---
tipo: memoria
actualizado: 2026-11-12
---

# Memoria del Proyecto NASA-Ecuador

> Se carga en cada sesión desde `CLAUDE.md` (raíz del repositorio). Aquí van las directivas de Guillermo, las decisiones con fecha, los datos medidos y las lecciones. El avance y los pendientes van en [[trabajos]].

## 1. Directivas de Guillermo

| Fecha | Directiva |
|---|---|
| 2026-11-12 | Crear un juego totalmente único con aires de AAA. Pulir cada aspecto y validar juntos cada recurso: escena, luz, isometría, ajustes y proporciones. |
| 2026-11-12 | Trabajar como un estudio profesional, con hojas de referencia y las técnicas habituales de los estudios AAA. Referentes: RPG de Nintendo, Monster Hunter, Pokémon, Ocarina of Time 3D y Bravely. |
| 2026-11-12 | Sacar el máximo provecho de los 1000 créditos de Higgsfield (plan Plus). |
| 2026-11-12 | Seguir el plan maestro de 8 fases: se presenta una fase y se espera su aprobación. |
| 2026-11-12 | La bóveda de Obsidian `Nasa_Game/` guarda el contexto. Mantener `CLAUDE.md`, `Memory.md` y `trabajos.md`. |
| 2026-11-12 | Delegar tareas a Codex para trabajar con eficiencia y gastar menos tokens. |
| 2026-11-12 | El estilo de la bóveda anterior (píxel-art) queda descartado: «muy superficial, carece de estilo artístico válido para un juego AAA». |
| 2026-11-12 | Pilar «mundo vivo»: interacciones de alto nivel con todo el entorno, movimientos sutiles del ambiente, sonidos coherentes y paleta de colores consistente. |
| 2026-11-12 | «Quiero que el sistema sea totalmente AAA, no quiero que te enfoques en que voy a renderizar todo aquí. Puedo alquilar PC en la nube.» Meta: un videojuego totalmente impresionante, con texturas y arte innovador. Corrige la primera versión de la Fase 0, que lo limitaba todo al portátil. |
| 2026-11-12 | Empezar ya los diseños con Higgsfield: «lowpoly, o cualquier otra forma recomendada». El alquiler del PC en la nube se ve después. |
| 2026-11-12 | «Me encantó la vista superior, así se debe ver.» La vista de juego del lote 02 es la meta de la exploración. |
| 2026-11-12 | Hacer hojas de referencia de los recursos «para que no se pierdan luego» y el juego sea coherente en diseño en el tiempo. |
| 2026-11-12 | Idea de Guillermo: una zona donde incrustar datos satelitales de NASA, por ejemplo mirar la Luna por un telescopio mientras la mascota da datos. |
| 2026-11-12 | «Sí, descárgalos»: autorizó descargar los tres archivos públicos de NASA para la prueba de la Luna. |
| 2026-11-12 | «Si requieres de Blender para modelaje solo indícamelo que yo lo descargo.» Las instalaciones las hace Guillermo: hay que pedírselas con la versión exacta y la fuente oficial. |
| 2026-11-12 | Sobre el modelado 3D: «Puedo aprender a usar blender, me gusta mucho la opción de tipo» (aprueba la ruta por tipo de recurso, D-014). Propone conectar Blender por MCP para que Claude dé los toques finales. |
| 2026-11-12 | «Esas tareas finas se las puedes delegar a codex, hasta agotar sus tokens; luego tomará el chat mañana Fable.» El trabajo debe quedar documentado para que otro modelo lo retome. |
| 2026-11-12 | «En este momento quiero las mallas listas, y una escena completa. Empecemos. Quiero trabajar contigo y validar si las mallas cumplen mis expectativas.» Autoriza adelantar mallas de personajes y entorno (fases 3 y 5) para la escena de prueba, con su validación. |
| 2026-11-12 | «El personaje principal se ve totalmente mal… Las facciones» y «Revisa correctamente el reference sheet». Se rehizo la malla desde una hoja de giro limpia (lotes 04b y 04c). |
| 2026-11-12 | «Sé que es 3D, pero recuerda: quiero darle texturas de 2D-HD o 2.5D.» Acabado pintado: la luz de la escena no debe dominar sobre el color pintado. |
| 2026-11-12 | «/loop Itera hasta que el escenario se vea como se requirió en las referencias.» Bucle de ajuste contra el ancla; estado en `pruebas/escena_exploracion/capturas/iteraciones/BUCLE.md`. |
| 2026-11-12 | «Siempre despliega agentes para seguir avanzando o puliendo cosas que se necesiten avanzar en las siguientes fases o en las actuales y así trabajamos con mayor eficiencia y rápido, manteniendo la profesionalidad en los resultados.» Mientras corre una tarea, los agentes avanzan en paralelo otras fases, con un verificador escéptico por resultado. Las puertas de validación y la regla de créditos siguen igual. |
| 2026-11-12 | «Mira, te indiqué que primero debíamos validar los escenarios y el estilo del arte conmigo.» «Siempre, sin excepciones.» Ningún escenario, pieza de arte ni estilo se construye sin su validación previa, paso a paso: concepto → hoja de referencia → producción → motor. Una «prueba técnica» con aspecto también pasa primero por él. |
| 2026-11-12 | «/loop Hacer que el personaje principal se parezca en gran medida, 80 % o más, al del reference sheet.» Estado en `Fase_1_Arte/Modelado/Lote_04/parecido/BUCLE_PROTAGONISTA.md`. |
| 2026-11-12 | Para después del bucle, la historia (Fase 2):<br>- al menos 1 hora de juego y más contenido espacial;<br>- al acostarse, la protagonista sueña que está en la Luna: camina, recolecta muestras y ve el Apolo;<br>- una misión es colocar juntas las banderas de Estados Unidos y Ecuador en la Luna;<br>- historia coherente y entretenida.<br><br>Después, la auditoría en orden: pantallas de carga, menús, botones, jugabilidad, escenarios, caminos y texturas. Escenarios: 1) habitación, 2) telescopio, 3) Luna, conectados como mundo abierto. |
| 2026-11-12 | «Pero recuerda siempre diseñar un espacio en la escena para entrada, salida, ventana de carga.» Cada escena lleva diseñado su tramo de entrada y salida (unos 2 × 2 m despejados, con la marca cian) y su ventana de carga. La prueba automática de cada zona lo mide. |
| 2026-11-13 | «USA TODAS TUS CAPACIDADES PARA EMPEZAR A CONSTRUIR EL MUNDO COMPLETO. Quiero empezar a jugar y ver los minijuegos, asimismo, que el juego se vaya enfocando en aspectos espaciales también.» Autoriza construir ya el juego jugable (`juego/`). Lo que no tiene concepto validado se construye como **provisional** y se le dice. |
| 2026-11-13 | «Para lo que necesites siempre recuerda que puedes lanzar agentes y subagentes tuyos y de Codex (siempre que este tenga créditos).» |
| 2026-11-13 | «Siempre recuerda el estilo que hemos llevado, utilizar recursos, mandar a modelar los que falten, usar todo.» Se usan las hojas de referencia y los modelos que ya existen; lo que falte se modela por script con su ID del catálogo, en el estilo aprobado. Nada de bloques grises donde va un objeto. |
| 2026-11-13 | **Base espacial.** «Quiero dentro de mi juego un sistema para un mundo abierto espacial, con dinámicas propias de una vida espacial. Créalo como si fuera un RPG, tipo SAO vista superior, Bravely de Nintendo. Minijuego que aparece al entrar en la biblioteca de la ciudad.» Reto de referencia: «gestionar una base lunar o marciana: equilibra soporte vital, radiación, energía y alimentos» (`Referencias/Reto_base_espacial/`). Diseño en [[Base espacial - Diseno]]. |
| 2026-11-14 | **Equipo.** Jean, Joel y Domenica construyen los minijuegos de la base en la Luna y en Marte, en 2D píxel-art, incorporados en libros de la biblioteca. Guillermo se encarga de todo lo demás. Plan en `PLAN_EQUIPO_BASE_LUNA_MARTE.md`. Repositorio: `github.com/Guivve-A/Nasa-Adventure-Game`. |
| 2026-11-14 | «No quiero nada genérico, recuerda usar todos los recursos disponibles para hacer un producto novedoso. Usa Higgsfield para lo que necesites, te doy el permiso.» Quiere ver el mapa, las interconexiones entre escenas y pantallas de carga «tipo Monster Hunter pero en versión NASA space». Si Claude lo hace más eficiente por sí mismo que con agentes, que lo haga. |
| 2026-11-14 | «Recuerda: todo debe ser jugable.» Nada se da por hecho con una prueba que no pase por el teclado o el ratón: cada zona, cada interacción y cada minijuego se demuestra jugable con entradas simuladas (`--prueba=manos`, `--prueba=recorrido_manos` y la `prueba_manos.gd` de cada minijuego) y, al final, jugándolo él. |
| 2026-11-14 | **Notas tras jugarlo.** «La sección de la Luna se ve extremadamente sencilla, le falta más recursos, dinámicas, efectos, sfx mejorados, y un mini mapa que me indique en dónde estoy y a dónde voy.» En curso: minimapa con el objetivo y sonido con archivos (agente del núcleo, tope de 8 créditos de Higgsfield para efectos) y la Luna v2 (agente de la zona). Estado en `Construccion/BUCLE_ESTILO.md`, filas 5a y 5b. |
| 2026-11-14 | «He visto todo, se necesita pulir bastante: los minijuegos están bastante simples, quiero que sean como minijuegos de Atari, con misiones básicas, no puro texto. Las pantallas de carga se ven mucho IA-like. Sé original. Genera diseños más como Bravely. Itera y perfecciona.» En curso: los 9 minijuegos se rehacen como arcade de acción (tres flujos `minijuegos-arcade`, con constructor, crítico y pulido) y las pantallas de carga se rediseñan pintadas y con composición propia (lote 08, tope de 18 créditos). |
| 2026-11-14 | «Continúa, quiero ver mejorías significativas en el gameplay y asimismo en el color de las escenas; cabe destacar que el gameplay de los 2 minijuegos de la biblioteca están siendo desarrollados por mis compañeros, esos no los toques.» Los minijuegos `base_luna` y `base_marte` (y la elección de libros de la biblioteca) no se tocan. En curso: color y vida de la Plaza y del Mirador, Luna v2, minimapa con sonido y los 9 minijuegos arcade. |
| 2026-11-14 | Al ver los minijuegos arcade: «Excelente, lo que no me gusta son los bordes en los minijuegos, eso trata de ver una manera mucho más optimizada de hacerlo.» El anfitrión ya no dibuja marco (campo sin recuadro, con resplandor de sus propios colores) y el contrato permite el campo a pantalla completa (`pantalla_completa`, 320 × 180 píxeles gordos); Codex amplía los 9. |
| 2026-11-14 | «Noté que en la parte del cuarto se ven los bordes del techo en la parte derecha, una zona vacía hueca.» La Habitación debe cerrar sus cantos y llenar el exterior que alcanza la cámara: ninguna escena puede mostrar vacío ni muros sin rematar. |
| 2026-11-14 | **Cinemática de apertura.** «En Death Stranding existen cinemáticas visualmente hermosas… quiero hacer una cinemática así para cuando el jugador le dé inicio a la partida, pueda ver el alunizaje del Apollo; que un agente produzca un guion, storytelling bello, como homenaje a USA y su alunizaje… todo el despegue, con estética sesentera, televisor viejo, sueño, y cuando termine la niña abra los ojos y con una lágrima de felicidad esté entusiasmada en aprender y ser astronauta. Empecemos por el storyboard, guion y luego el video con Higgsfield y sus mejores modelos.» Orden: guion y storyboard (los valida él) y después el video, con partida cotizada. Documentos en `Fase_2_Narrativa/Cinematica_apertura/` y viñetas en `Fase_1_Arte/Exploracion/Lote_09/`. En el material generado no van insignias, logotipos ni rostros de personas reales. |
| 2026-11-14 | Sobre la cinemática: «Hazlo, esto debe quedar cinemático a más no poder.» Nivel de exigencia: el mejor modelo de video en todos los planos, fotogramas clave en calidad alta, pase de dirección de fotografía (lente, luz, movimiento, grano y guion de color), música y diseño sonoro propios. No respondió si la niña es la protagonista de pequeña o la de hoy: lo decide el guion, con justificación, y él lo valida en el storyboard. |
| 2026-11-15 | Veredicto del storyboard «Un punto de luz»: «Excelente, pero que se vea la bandera estadounidense flameante en la Luna y, asimismo, mejora el diseño de la personaje en los últimos tramos de la cinemática.» Storyboard aprobado con dos cambios: P13 pasa a ser un plano de video con la bandera ondeando (con verdad: se movió al plantarla y, sin aire, siguió oscilando; lo demás es licencia de sueño declarada) y la protagonista se rediseña para los primeros planos finales (P14 y P15). |
| 2026-11-15 | «Usa los mejores modelos de Higgsfield para este objetivo, no importa el gasto.» Para la cinemática queda aprobado el gasto con los mejores modelos. El límite real es el saldo (849,50, sin recarga prevista): se produce por puertas, revisando cada entrega antes de la siguiente, y se le avisa si el saldo no alcanza. |
| 2026-11-15 | «Lanza el video de los movimientos I y II.» Orden directa: el video del despegue y de la Luna (P03 a P09) se genera sin esperar otra confirmación, en cuanto existan sus fotogramas finales. |
| 2026-11-15 | «He integrado 2 carpetas al directorio; estas son de los minijuegos desarrollados por mis compañeros, los que van en la biblioteca… quiero que los integres de manera coherente y cohesiva.» Carpetas: `Misión Artemis/` y `Marte_Gravedad2DHD/`. Se integran como copia generada en `juego/minijuegos/base_luna` y `base_marte` (script repetible), sin editar las carpetas de origen ni cambiar su gameplay: entrada por los libros, vuelta a la Plaza, Esc y pausa comunes, píxel nítido ×2, banderas y guardado compartidos. |
| 2026-11-15 | Ante las tres variantes de la bandera (A y A2 frontal con guante, B tres cuartos) y las tres direcciones de la protagonista (A low-poly fino, B pintado, C cine): «A y cine». Confirmado por él («Sí, eso»): **bandera A** (frontal, con el guante que suelta el asta) y **protagonista en la dirección C «cine»** para los planos finales (P14 y P15). |
| 2026-11-15 | **Presentación.** «Tengo 2 minutos y medio para presentar todo mi proyecto, el Challenge es Space Game Design; quiero que destaques todo en un video demo, arte y todo, para destacar qué es lo que se ha hecho y poder ganar; todo profesional, usa toda clase de recursos para editar el video: sonidos, sfx, imágenes en alta calidad… Destaca todo. Asimismo, entrega un guion de 1:30 min para el expositor y que vaya acorde al video.» Pasa a ser la prioridad. Entregables en `Nasa_Game/Presentacion/`: video demo de 2:30, guion del expositor de 1:30 sincronizado y tarjeta de apoyo. Todo dato que se diga o se muestre debe poder comprobarse en el repositorio; lo provisional no se presenta como terminado; sin logotipos de la NASA. |
| 2026-11-15 | **Nombre del juego: «Zingularity: Artemis»** («El juego se llama Zingularity: Artemis»). Sustituye al título de trabajo «Luz cenicienta» en presentación, diapositivas, video y, cuando él lo confirme, dentro del juego y del paquete. Público: jóvenes de 10 a 16 años de Sudamérica. |
| 2026-11-15 | «Entrega el juego completo ejecutable para solamente instalar.» Paquete portable de Windows en `entrega/` (motor de Godot incluido, `Instalar.cmd`, `Jugar.cmd`, extras de los compañeros), hecho con `herramientas/empaquetar_juego.py`. Un `.exe` único exige las plantillas de exportación, que él tendría que descargar. |
| 2026-11-15 | Sobre sus diapositivas de Canva (diseño `DAHbAaRfTk8`): «añádele capturas esenciales del juego, el storytelling, reference sheets de todo lo trabajado. Recuerda que el juego nació de la idea de que un estudiante, luego de ver el alunizaje, se interesó en la ciencia.» **Idea de origen del juego:** alguien joven ve el alunizaje y de ahí nace su interés por la ciencia; toda presentación del proyecto parte de ahí. En su documento solo se añaden páginas; no se borra ni se reescribe lo suyo. |

## 2. Decisiones

Las decisiones técnicas de la Fase 0 están propuestas en [[Fase 0 - Analisis]] y esperan la aprobación de Guillermo. Al aprobarse se copian aquí con su fecha.

| ID | Fecha | Decisión | Estado |
|---|---|---|---|
| D-000 | 2026-11-12 | El píxel-art de la bóveda anterior no se usa. La meta visual es el tablero de referencia y los referentes de mercado. | Decidido por Guillermo |
| D-011 | 2026-11-12 | **Dirección de arte: low-poly pintado a mano** (A1 del lote 01). Anclas de estilo: `L01_A_lowpoly_hub_gpt26.png` para el hub y `L01_A_lowpoly_exploracion_gpt26.png` para la exploración. | Decidido por Guillermo |
| D-012 | 2026-11-12 | **Tipo de juego: exploración, mapa mediano y 2D-HD**, como las capturas del tablero: cámara alta 3/4 con el personaje pequeño y mapa ilustrado de la región con recolección, fauna e hitos. | Decidido por Guillermo |
| D-013 | 2026-11-12 | **Vista de exploración aprobada:** `L02_exploracion_camara_alta.png`, con cámara alta a unos 60°, sin horizonte y el personaje a un octavo del alto. Es ancla de estilo. Ojo: en la imagen el personaje mide el 20,9 % del alto, no un octavo; la escena de prueba mide los dos tamaños para que Guillermo elija. | Decidido por Guillermo |
| D-015 | 2026-11-12 | **Estilo en el motor aprobado** («Sí, ese estilo»): el acabado 2.5D pintado de la escena del sendero es la base del arte en el motor para todos los escenarios. Abarca la luz pintada (las caras de espaldas al sol conservan el 55 % de la luz y las sombras proyectadas el 30 %), la sombra moteada, el sol `ffdcb4`, el ambiente `77849a`, el contraste 1,12 y la saturación 0,80 (`pruebas/escena_exploracion/`, vuelta 17 de `BUCLE.md`). | Decidido por Guillermo |
| D-016 | 2026-11-12 | **Habitación: rehacer el concepto.** El ancla ANC_HUB no sirve como concepto del cuarto: fallan la cámara, la distribución, el ambiente y el encaje con la historia. El nuevo concepto usa la vista superior 3/4 de D-013 (no un diorama de costado), «algo más cercano a juegos típicos, 2D-HD», y los elementos de la historia (seguidor motorizado, cama del sueño, telescopio). La hoja HR_TAL_v1 queda sin aprobar. | Decidido por Guillermo |
| D-017 | 2026-11-12 | **Protagonista v8T aprobada como modelo base** («Apruebo y mejora el bolso»). Es la malla de Tripo ajustada a las siluetas de la hoja, con la textura proyectada desde la hoja y limpiada de defectos (`L04_PER01_v8T.glb`). Da 81,1 % de parecido con su hoja con bolso (métrica v2), sin defectos graves según el verificador y el juez. Falta mejorar el bolso 3D: hoy es una caja plana y debe pintarse con la bolsa de la hoja. | Decidido por Guillermo |
| D-014 | 2026-11-12 | **Modelado 3D por tipo de recurso (ruta híbrida):** el entorno se hace por script (sin créditos) y las mallas base de personajes y fauna, con Tripo H3.1. Blender 5.2.4 LTS pasa a ser obligatorio, como taller de limpieza, rig y exportación. Detalle en [[Decision - Modelado 3D]]. | Decidido por Guillermo |
| D-018 | 2026-11-12 | **Habitación: borrador A «Mañana cálida».** Guillermo lo eligió entre los 6 del lote 05. La versión final (`Exploracion/Lote_05/L05_A_manana_calida_final.png`, 2,75 créditos) añade el descanso de la escalera como entrada y salida. La producción en el motor espera su validación con capturas. | Concepto elegido por Guillermo; la versión final espera su visto bueno |
| D-019 | 2026-11-13 | **Juego jugable v0 en `juego/`** (Godot 4.7.2, Mobile, 1280 × 720, todo por código). Mundo por zonas enlazadas con umbrales y ventana de carga: Habitación ↔ Plaza (con la biblioteca) ↔ Sendero ↔ Mirador; la cama lleva a la Luna del sueño y la biblioteca, a la base espacial. Contrato en `juego/ARQUITECTURA.md`. Título de trabajo: «Luz cenicienta» (sin «NASA»). | Propuesto por Claude; lo valida Guillermo jugando |

## 3. Datos medidos (2026-11-12)

**Equipo de desarrollo**
- Intel Core i5-7200U (2 núcleos, 4 hilos), 7,9 GB de RAM y gráfica integrada Intel HD Graphics 620 (controlador 31.0.101.2140).
- Pantalla de 1920×1080, Windows 10 Home, 27 GB libres en C:.
- Instalado: Git, Git LFS, Python 3.13, ffmpeg 9, ImageMagick 7, .NET, VS Code, GitHub CLI y Node 24.
- No instalado: Blender ni editores de imagen.

**Red desde Guayaquil (02:22 del 2026-11-12, Wi-Fi)**
- Latencia de conexión TCP: Miami 62 ms, Atlanta 74, Chicago 93, Virginia 94, Nueva Jersey 96, Dallas 99, Ohio 118, Ciudad de México 121, Santiago 131, Los Ángeles 132, São Paulo de 153 a 193 y Oregón 164.
- Ancho de banda: 106 Mbps de bajada y 45 Mbps de subida contra un nodo cercano; 46 Mbps desde Atlanta y 10 Mbps desde Miami en una sola conexión.
- Se repite con `python herramientas/red_nube.py`.

**Godot**
- Godot 4.7.2-stable con firma válida (Prehensile Tales B.V.), en `C:\Users\guill\Downloads\Godot_v4.7.2-stable_win64.exe\`.
- En la HD 620 arrancan los cuatro modos: Forward+ con Vulkan 1.3.215, Forward+ con D3D12 (nivel 12_0), Mobile con Vulkan, y Compatibility. Compatibility cambia solo a ANGLE (OpenGL ES 3.0 sobre Direct3D 11) porque el OpenGL del controlador es de baja calidad.
- Medición con `pruebas/bench_render/` (29 corridas, fps medios a 1280×720): Mobile 90 en la escena base, 43 con 40 000 briznas de hierba y 75 con 200 sprites; Compatibility 73, 42 y 41; Forward+ 68, 35 y 58. Forward+ con SDFGI, SSAO y glow da 20 fps con caídas a 9.
- A 1920×1080 con hierba densa todos rondan los 30 fps: el límite es el relleno de píxeles.
- El primer arranque de Forward+ tardó más de 90 s por la compilación de shaders.
- La escena del telescopio (`pruebas/luna_telescopio/`, Mobile) cuesta 0,74 ms de GPU a 720p, y de 2,2 a 2,5 ms con la Luna a pantalla completa. Lo midió el revisor de código.

**Higgsfield**
- Plan Plus, espacio de trabajo «Private», CLI 1.2.2. **Saldo al 2026-11-15: 849,50 créditos** (tras el lote 07, el lote A1 de audio, 7,50, el lote 08 de carga, 15,00, y el lote 09a del storyboard, 4,25). Saldo tras el lote 04c: 889,50 créditos. Se gastaron 116,75: 66,00 en los lotes 01 a 03 y 50,75 en el 04 (04a 36,00; 04b 2,75; 04c 12,00). De la partida de la escena v1 (tope 52,75) quedan 2,00. El detalle está en [[trabajos]].
- Los 1000 créditos de suscripción se acreditaron el 2026-11-12. **No se acumulan:** caducan al cierre del periodo de facturación (términos de Higgsfield, apartado 9.4). Los comprados aparte duran 90 días (apartado 9.6). Falta confirmar la fecha de renovación.
- Los términos permiten el uso comercial de los resultados (apartado 4.4), pero rigen las condiciones más restrictivas de cada proveedor (apartado 8). Las licencias de música vía Higgsfield no están verificadas para publicar.
- 119 modelos: imagen, video, audio y 3D. El 3D incluye imagen→malla (Tripo, Hunyuan3D, Meshy), remesh, retexturizado y rigging con biblioteca de animaciones. `autosprite` genera animaciones de sprites con direcciones isométricas.
- Catálogo, parámetros y 169 cotizaciones en `Fase_0_Tecnica/Datos/`.

**Codex**
- App de escritorio 26.1103 con sesión de ChatGPT. La línea de comandos utilizable es `%LOCALAPPDATA%\OpenAI\Codex\bin\<hash>\codex.exe` (codex-cli 0.167). Modelo configurado: gpt-6.1-sol.

**Trabajo anterior**
- Bóveda y repositorio «Gravedad 2D-HD» en `C:\Users\guill\Desktop\Juego\Juego_2d-hd` (remoto `Guivve-A/Juego_Godot_repo1_agentes`), del 8 y 9 de noviembre de 2026. Nació para el NASA Space Apps Challenge de Guayaquil, con el reto «Space Mission Design Game». Resumen en [[08_antecedentes_boveda_anterior]].

## 4. Costos medidos de Higgsfield (créditos)

| Recurso | Opción | Créditos |
|---|---|---|
| Imagen de borrador | `gpt_image_2_6` calidad low, 1k | 0,25 |
| Imagen de borrador | `text2image_soul_v2`, `soul_location` | 0,12 |
| Imagen final | `gpt_image_2_6` calidad high, 1k / 2k | 1,5 / 2,75 |
| Imagen final con referencias | `nano_banana_pro` 2k (hasta 14 referencias) | 2 |
| Vistas nuevas de un sujeto | `3d_jutsu_angles` 1k / 2k | 1,25 / 2,5 |
| Animación de sprite | `autosprite` turbo / pro / max | 2 / 3 / 14 |
| Imagen → malla 3D | `tripo_h3_1_image_to_3d` (sin textura 6, quads 10,5); el límite de caras no cambia el precio | 9 |
| Vistas → malla 3D | `tripo_h3_1_multiview_to_3d`, de 2 a 4 vistas | 9 |
| Imagen → malla low-poly | `hunyuan3d_v3_image_to_3d` con `generate_type` LowPoly (no deja fijar las caras) | 14 |
| Imagen → malla 3D | `hunyuan3d_v3_image_to_3d` (solo geometría 7) | 11 |
| Imagen → malla 3D | `meshy_v7_image_to_3d` (con rig 44, rig y animación 47,5) | 38 |
| Retopología | `meshy_v5_remesh` | 6 |
| Retexturizado | `meshy_v5_retexture` | 9,5 |
| Quitar fondo | `image_background_remover` | 1 |
| Música | `sonilo_music` / `elevenlabs_music_v2_5` por minuto | 3,75 / 8,72 |
| Efecto de sonido | `mirelo_text_to_audio` por segundo | 0,25 |
| Video | de `seedance1_5` a `seedance_2_5` por clip | 4,8 a 35 |

Las referencias de imagen no cambian el costo. `generate cost` no cotiza `image_to_3d`, `multi_image_to_3d`, `3d_rigging`, `sam_3_3d` ni `topaz_image`.

## 5. Lecciones

- **PowerShell bloquea los `.ps1`.** Usar `npm.cmd`, `npx.cmd` y `higgsfield.cmd`.
- **Instalaciones.** El modo automático bloquea instalar software externo. Se le da el comando a Guillermo.
- **Modelos 3D ocultos.** `higgsfield model list` en tabla no muestra los modelos 3D; `model list --json` sí. Usar `herramientas/hf_catalogo.py`.
- **Cotizar es gratis.** `generate cost` no crea trabajos. Para los modelos que exigen imagen se usa un marcador gris ya subido.
- **Codex por lotes.** El `codex.exe` de `WindowsApps` da «Acceso denegado». Funciona el de `%LOCALAPPDATA%\OpenAI\Codex\bin`, con el prompt por la entrada estándar en UTF-8, `-s read-only`, `-c web_search="live"` y `-o informe.md`.
- **Verificar lo delegado.** Los informes de Codex se contrastan con mediciones propias y con una revisión independiente antes de decidir. En la Fase 0, casi todos los informes recomendaban Compatibility sin haberlo medido; la medición favoreció a Mobile.
- **Codex y Firecrawl.** Codex usa el conector de Firecrawl de la cuenta de Guillermo. Nueve tareas en paralelo agotaron los créditos diarios, que se renuevan solos. Para lotes grandes, repartir las tareas o avisar antes.
- **Workflows y Firecrawl.** Los agentes de los workflows también usan Firecrawl. Los tres agentes del estudio de modelado lo dejaron sin créditos hasta el 2026-11-13 a las 03:58 UTC. En los encargos de investigación, pedir WebFetch y WebSearch para lo simple.
- **Medir las anclas, no confiar en el encargo.** Una imagen generada no respeta las proporciones pedidas. En `L02_exploracion_camara_alta.png` el encargo pedía al personaje a un octavo del alto (12,5 %) y salió al 20,9 %. La biblia de arte y D-013 copiaron el texto del encargo.
- **Hojas de personaje para multivista.** Antes de mandarlas a 3D, revisar que las vistas coincidan. En la hoja de PER-01, el bolso cuelga delante de la cadera en el frente y detrás en el perfil. Además, el perfil mira a la derecha (muestra el lado derecho), y Tripo pide frente, izquierda y espalda.
- **Modelado 3D.** Higgsfield no da low-poly controlable: Tripo rechaza `smart_low_poly` y Hunyuan LowPoly no deja fijar las caras. Tampoco separa piezas ni hace rig de cuadrúpedos. Las mallas de IA necesitan limpieza en Blender. Estudio completo en [[Decision - Modelado 3D]].
- **Tripo multivista por Higgsfield.**
  - Las vistas van en orden frente, izquierda, espalda y derecha. «Izquierda» es el lado izquierdo del objeto, que en la imagen mira hacia la izquierda.
  - Un perfil que mira a la derecha, puesto en la segunda ranura, deja la malla en espejo.
  - Las mallas salen mirando a ±X.
  - Si el objeto es simétrico, basta con mandar el perfil y su espejo.
- **Textura fallida de Tripo.** Puede devolver un gris plano (media 102, desviación 3) sin ningún aviso. Hay que revisar la desviación de cada textura. `herramientas/mallas/proyectar_vistas.py --auto` pinta la textura desde las vistas de la hoja, elige el frente y el espejo según cómo calzan las siluetas y no gasta créditos.
- **Subir una vez.** `herramientas/hf_subir.py` sube las imágenes de entrada como JPEG de 70 a 175 KB y guarda sus ids. Con ids, cotizar un lote de 4 mallas tarda segundos. Con rutas locales, cada cotización sube el archivo y una se cortó a los 120 s.
- **Godot: luz propia.** En `light()`, `LIGHT_COLOR` llega multiplicado por π: dividir entre π para igualar el Lambert estándar.
- **Godot: GLB en tiempo de ejecución.** `GLTFDocument.append_from_file` carga mallas sin importarlas. Si se guardan en una carpeta con `.gdignore`, el editor no las importa y se pueden regenerar al momento.
- **Comandos para Guillermo.** Usa la app de escritorio y no tiene el CLI `claude`. Los MCP se registran en el `.mcp.json` del proyecto. Su terminal es PowerShell: una ruta `.exe` entre comillas se ejecuta con `&` delante, o se le deja un lanzador `.cmd` (por ejemplo `pruebas/escena_exploracion/abrir_escena.cmd`).
- **MCP de Blender** (complemento `blender_mcp.py` 2.0, paquete `mcp-for-blender` 2.2.8).
  - Sus campos de claves de API (Hyper3D, Hunyuan3D, Tripo, Meshy, World Labs, Sketchfab, Poly Pizza) no vienen con Higgsfield: son cuentas aparte y se cobran aparte. El código no menciona Higgsfield.
  - La generación sigue por Higgsfield y el GLB se importa en Blender.
  - «Allow Telemetry», que envía prompts, código y capturas, y «Allow Remote Connections» vienen apagadas por defecto, pero aparecieron marcadas: hay que dejarlas desmarcadas.
  - `install-addon` falla si Blender aún no creó su carpeta de configuración: abrir Blender una vez antes.
- **Blender 5.3 instalado** (2026-11-12, `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`), en vez de la 5.2.4 LTS. Arranca sin ventana en la HD 620.
  - Sin ventana, una imagen empaquetada que viene de un GLB tiene `has_data` en falso hasta usarla: comprobar `packed_file`.
  - `herramientas/blender/limpiar_personaje.py` (Codex) funcionó tras esa corrección: niveles exactos de 1 500 y 3 000 triángulos en 9,3 s.
- **Rig de cuadrúpedos con Rigify, por script** (`herramientas/blender/rig_gato.py`, probado con Órbita en Blender 5.3):
  1. Soldar los vértices de Tripo antes de los pesos automáticos; si no, el cálculo de pesos no converge.
  2. Copiar el peso del vecino más cercano a las piezas finas sueltas.
  3. Hornear solo posición y rotación: la escala de Rigify produce cizallamiento, que glTF no admite.
  4. Exportar en modo `NLA_TRACKS`.
  5. Al crear los huesos de exportación, copiar sus extremos y su orientación. Con longitud cero pierden la dirección de descanso y la animación deforma la malla.
  6. En Godot, activar el bucle de cada animación.
  7. Revisar siempre la pose de unión contra la animada: separa los fallos de pesos de los fallos de animación.
- **Inclinación hacia atrás.** En el ancla, los objetos y personajes no tienen el escorzo de una cámara de 55°. Una cizalla en el shader (`z -= 0,55·y`) los muestra erguidos sin mover el suelo, y las sombras siguen correctas.
- **Límite de uso de Codex.** Las diez tareas de la Fase 0 agotaron el límite del plan de ChatGPT de Guillermo el 2026-11-12 a las 02:26; se restablecía a las 06:27. Enviar pocas tareas a la vez, con esfuerzo medio cuando baste, y comprobar que queda cupo antes de un lote.
- **Tiempo de las tareas de Codex.** Con esfuerzo alto tardan de 14 a 23 minutos. Dar 45 minutos de límite. Si una se corta, se reanuda con `codex exec resume <id de sesión>`; el id está al inicio de su log.
- **Meshy se retira.** El proveedor retiró `lowpoly` el 30-10-2026 y retira Meshy 7 para geometría el 31-12-2026. No basar la producción en `meshy_v7_image_to_3d`.
- **Mixamo** solo acepta FBX, OBJ o ZIP y solo hace rig de bípedos. Su licencia permite el uso comercial dentro del juego, sin redistribuir los archivos crudos.
- **Medir a 1080p.** Una ventana de 1920×1080 no cabe en esta pantalla: para medir esa resolución hay que usar `--fullscreen`.
- **Resultados de Higgsfield.** La respuesta trae `result_url` (el original en PNG) y `min_result_url` (una miniatura). Hay que bajar `result_url`. `herramientas/hf_generar.py` ya lo hace, cotiza antes, respeta un tope por lote y registra cada generación.
- **Modelos de imagen para este juego** (lote 01, mismo encargo): GPT Image 2.6 en calidad high y 2k sigue la dirección de arte al detalle. Nano Banana Pro deriva a caricatura isométrica con contorno. Seedream 5.5 da luz cinematográfica, pero ignora el low-poly.
- **Encargos de imagen.** Funciona un bloque de escena fijo más un bloque de estilo que cambia. Terminar con «No text, no logos, no interface». Revisar que no aparezcan objetos parecidos a productos comerciales.
- **Consistencia entre lotes.** Pasar como referencia las imágenes aprobadas (anclas de estilo) y un recorte del personaje mantiene el diseño: en el lote 02 el protagonista y el gato salieron iguales en hojas y escenas. Las referencias no cambian el costo en GPT Image 2.6.
- **Texto en imágenes.** GPT Image 2.6 escribió bien los rótulos en español del mapa, con tildes. Sirve para maquetas de interfaz; el texto final se compone en el motor.
- **Fondo transparente.** Una hoja de personaje puede volver con canal alfa aunque se pida fondo gris. Para verla o montarla hay que aplanarla: `magick archivo.png -background "#cfc8c3" -alpha remove`.
- **Fallo de subida.** Un error HTTP 520 al subir una referencia no cobra créditos. Se reintenta con `--solo <id>`.
- **Anclas subidas una vez.** Las imágenes aprobadas se suben a Higgsfield en JPEG de 1600 px con `herramientas/hf_anclas.py` y se citan como `@ANC_…`. Evita volver a subir PNG de 5 a 7 MB en cada encargo, que fue lo que provocó el error 520.
- **Hojas con rótulos.** En el lote 03, GPT Image 2.6 escribió bien los 104 rótulos con ID y tildes («VEG-01 Ceibo»…) en nueve hojas. Pedir rótulos en las hojas sirve.
- **Indicador de paleta.** Con ΔE ≤ 20, `paleta.py comparar` detecta desvíos de familia de color (cálida frente a fría), no de estilo: las direcciones descartadas del lote 01 también dan 100 %. El estilo lo juzga Guillermo.
- **Descargas.** Cada archivo externo va a su propia carpeta en `externos/` con `herramientas/descargar_nasa.py`, que comprueba el tamaño y guarda el SHA-256. `curl -I` no mostró las cabeceras de NASA SVS en PowerShell; con Python sí.
- **Orientación de mapas lunares.** Antes de usar un mapa, ubicar el punto más alto (cumbre Selenean, 5,4° N y 158,6° O) y el más bajo (cráter Antoniadi, unos 70° S y 172° O). El CGI Moon Kit tiene la longitud 0 al centro y el este a la derecha.
- **Prueba objetiva de la Luna.** El modo `--prueba` del telescopio pinta la máscara de luz; `herramientas/luna_medir.py` mide la fracción iluminada y el ángulo del borde y los compara con Horizons. Con `--captura` y `--textura` también correlaciona la textura con la luz cenicienta, y así detecta un giro o un espejo.
- **Pruebas por correlación.** Hay que excluir de la zona medida lo que dibuja la interfaz: dos líneas de rótulos bajaron la correlación de 0,990 a 0,650.
- **Juego exportado.** `Image.load_from_file` sobre una ruta `res://` funciona en el editor, pero falla en el juego exportado, porque el `.pck` solo lleva los `.ctex` importados. Las texturas van como recursos importados y se cargan con `preload`. Se prueba sin plantillas de exportación: `--headless --export-pack "<preset>" x.pck` y después `--main-pack x.pck`.
- **HDR 2D.** Con `rendering/viewport/hdr_2d` el lienzo es lineal.
  - Un shader que hace su propia gamma debe entregar color lineal con la curva sRGB exacta. Con `pow(x, 2.2)` las sombras bajan unos 6 niveles.
  - `Image.linear_to_srgb()` de Godot 4.7.2 solo acepta RGB8 y RGBA8, pero la captura con HDR llega en RGBAH. Se convierte píxel a píxel con `Color.linear_to_srgb()`, en 2,6 s a 720p.
- **Otras fechas para probar.** `luna_efemerides.py --salida <carpeta temporal>` no ensucia `Propuestas/Datos`. Después, `luna_parametros.py` escribe el `luna.json` de una copia del proyecto.
- **Relieve y terminador.** Un mapa de normales enciende cráteres en plena noche si no se limita la luz a la zona cercana al terminador geométrico (`smoothstep` sobre el producto punto-Sol).
- **Luna con datos reales.** La API de JPL Horizons y Dial-A-Moon de NASA SVS responden para 2026. Script: `herramientas/luna_efemerides.py`. En la salida CSV de Horizons las columnas se llaman `Azi_(a-app)` y `Elev_(a-app)`.
- **NASA.** Los mapas de textura y polígonos de NASA se pueden usar en simulaciones con crédito. La insignia, el logotipo y los identificadores de NASA no son de dominio público y no pueden aparecer en imágenes generadas por IA. El uso comercial no puede sugerir respaldo. Las versiones con música de los videos de NASA SVS usan pistas con derechos de terceros.
- **Error: construir antes de validar.** El 2026-11-12 un agente construyó un prototipo de la Luna en Godot (`pruebas/luna_sueno/`) como «prueba de rendimiento», sin concepto ni estilo validados, y se le encargaron mejoras. Guillermo lo corrigió.
  - Antes de lanzar un agente, revisar si su trabajo crea o cambia un escenario, una pieza de arte o el estilo. Si el paso anterior no tiene su veredicto, no se lanza: se le presenta lo que hay para validar.
  - El prototipo queda como prueba técnica sin validar y no sirve de base de arte.
- **Hoja de giro antes de Tripo.** Con una hoja de giro limpia, Tripo multivista con `texture_quality: detailed` (12 créditos) dio una cara fiel y una textura con color.
  - La hoja debe tener cuatro vistas en pose A, sin bolso, con la cara despejada y luz plana.
  - GPT Image dibujó los dos perfiles mirando a la derecha: se usa uno y su espejo.
  - Revisar la malla sin luz con `herramientas/blender/render_vistas.py` y la textura con `herramientas/mallas/revisar_textura_glb.py`.
- **Acabado 2.5D.** Con el contraluz del ancla, la luz celular por cara partía la cara del personaje en dos y dejaba negro todo lo que mira a la cámara. En el modo `pintado = 1`:
  - la textura o el color pintado manda;
  - las caras de espaldas al sol conservan el 55 % de la luz;
  - las sombras proyectadas conservan el 30 %.
- **Efectos por píxel sobre la hierba.** La hierba tiene mucho sobredibujado (miles de briznas de doble cara), así que cada operación por píxel se multiplica.
  - La sombra moteada en estrella, calculada por píxel con 3×3 celdas, bajó la escena de 55 a 27 fps en la HD 620.
  - En la hierba se calcula por vértice; en el suelo, una sola celda con salida temprana: 48 fps.
  - Medir los fps después de cada efecto nuevo.
- **Godot se cuelga al salir.** En la HD 620, Godot 4.7.2 a veces no termina tras `quit()`, aunque la captura ya esté guardada. Usar `herramientas/godot_captura.py`, que lo cierra.
- **Colocar desde el ancla.** `herramientas/camara_ancla.py` reproduce la cámara de la escena: `al_suelo(u, v, y)` lleva un píxel del ancla al suelo. El trazado medido «a ojo» estaba corrido hasta 1,8 m, y la copa del árbol quedaba fuera del cuadro.
- **Medir contra el ancla.** `herramientas/comparar_ancla.py` da el ΔE por bloques y una rejilla 3×3. Del 28 bajó al 20,6 al corregir la composición y la luz. Ahí se estanca: lo que falta es riqueza de ilustración, que el ΔE no ve.
- **PowerShell.** `"$n: texto"` invalida la línea entera: escribir `${n}`. `Remove-Item` con comodín sobre una ruta en variable se bloquea: borrar por nombre con `-LiteralPath`.
- **Godot sin editor.** Un proyecto que se ejecuta con `--path` sin haber abierto el editor no tiene la caché de clases: `class_name` falla. En `juego/` no se usa `class_name` (todo va con `preload` y `extends "res://..."`) y `--headless --import` crea `.godot` (8 s).
- **Un solo Godot a la vez.** Con varios agentes en un equipo de 2 núcleos, `herramientas/juego_ejecutar.py` toma un candado global, corre sin ventana por defecto (4 s por prueba) y cierra Godot si se cuelga. Sirve también para otros proyectos con `--proyecto=`.
- **Color de vértice en lineal.** Una malla hecha por código con `Color("af795e")` sale lavada: el shader espera lineal. `nucleo/piezas.gd` convierte con `srgb_to_linear()`, igual que el generador de GLB.
- **Etiquetas con salto de línea.** Un `Label` con `autowrap` dentro de un contenedor reporta al principio una altura enorme: el panel queda alto si no se llama `reset_size()` después del primer cuadro. Para una sola línea, quitar el `autowrap` (si no, escribe una letra por línea).
- **Corrutinas y nodos liberados.** No se hace `await` de un cambio de zona desde un nodo de la zona que se libera: Godot avisa «Resumed function after await, but class instance is gone». El cambio se lanza sin `await` y lo que sigue va en `al_entrar()` de la zona de destino.
- **Contrato antes de repartir.** El núcleo, una zona y un minijuego de plantilla y las pruebas automáticas se escribieron antes de lanzar a los agentes: cada carril solo toca su carpeta y se comprueba solo (`--prueba=zona:<id>`, `--prueba=minijuego:<id>`).
- **Codex para lo mecánico.** Las 55 fichas del cuaderno salieron en 7 min con esfuerzo medio y sin web, a partir de los documentos ya verificados (`Construccion/Tareas_Codex/`). Después construyó los 9 minijuegos (de 8 a 18 min cada uno, con su prueba automática en verde).
- **Un piloto automático no prueba que algo sea jugable.** El piloto movía a la protagonista y llamaba a `usar()` directamente: pasaba 114 comprobaciones y aun así había tres trabas de juego real.
  - La tecla que cierra un diálogo o un minijuego (E o Intro) volvía a usar el objeto de al lado en el mismo cuadro: `Interfaz.ocupada()` sigue en verdadero 0,3 s después de cerrar.
  - El compañero, siempre cerca, ganaba la interacción: ahora gana lo que está de frente y al compañero solo se le habla mirándolo (`prioridad = -1`).
  - El compañero se recolocaba «detrás» al girarse hacia él y daba vueltas: ahora sigue con correa y se queda quieto.
  - Las pruebas de manos meten teclas con `Input.parse_input_event(InputEventKey)`, que recorren el mismo camino que las reales (también sin ventana).
- **Fallos de la propia prueba.** Dos «atascos» del recorrido con teclas eran de la prueba: el caminante no rodeaba obstáculos, y no notaba que la protagonista había cruzado un umbral con el impulso mientras atendía la interfaz. Antes de tocar el juego, reproducir el fallo aislado y volcar el estado (posición, umbrales cercanos, banderas de la interfaz).
- **Límite de uso de Claude (plan Pro).** Ocho agentes a la vez agotan la ventana de 5 horas en unos 80 minutos (medido el 2026-11-14 y el 15: de 1,1 a 1,4 puntos por minuto), y un flujo cortado pierde lo que cada agente llevaba a medias.
  - Los agentes van con `model: 'opus'`; con el modelo principal, tres guionistas y un sintetizador gastaron 9 puntos del límite semanal en 40 minutos.
  - No más de 4 agentes a la vez; los flujos se lanzan por orden de prioridad, no todos juntos.
  - Cada turno del hilo principal con el contexto lleno también cuesta: no sondear; esperar los avisos.
  - Un `CronCreate` de una sola vez reanuda tras el reinicio solo si la app sigue abierta.
- **Cupo de Codex.** Unas 9 tareas de minijuegos agotan su ventana; al cortarse deja `error (codigo 1)` y el aviso «try again at…» al final del log. Lo escrito en disco puede estar completo aunque la tarea figure con error: probarlo antes de repetirla.
- **Heredoc con barras invertidas o comillas raras:** volvió a fallar dos veces el 2026-11-14 (rutas de Windows y un bloque con comillas). Los scripts de edición van siempre en un archivo escrito con Write.

## 6. Índice de la bóveda

- [[Inicio]]: mapa de la bóveda.
- [[trabajos]]: avances, pendientes y registro de créditos.
- `00_Plan_Maestro/`: PDF del plan maestro.
- `Fase_0_Tecnica/`: [[Fase 0 - Analisis]], `Investigacion/`, `Datos/` y `Tareas_Codex/`.
- `Fase_1_Arte/`:
  - [[Biblia de arte]], `paleta_maestra.png`, `anclas.json`, `bloques_prompt.json`, `manifiesto_recursos.csv` y `registro_generaciones.json`.
  - [[Decision - Modelado 3D]] y su evidencia en `Modelado/`.
  - `Hojas_de_referencia/`: nueve hojas v1 y el [[Catalogo de recursos]].
  - `Exploracion/Lote_NN/`: [[Lote 01 - Direcciones de arte]], [[Lote 02 - Tipo de juego y personajes]] y [[Lote 03 - Hojas de referencia y Mirador]].
- `Propuestas/`: [[Mirador del Faro - Luna con datos reales]], sus datos en `Propuestas/Datos/` y sus capturas en `Propuestas/Capturas/`.
- `Referencias/Tablero_usuario/`: 14 capturas y [[Analisis del tablero]].
- `Construccion/`: [[Mundo jugable v0]] (qué se construyó, carriles y estado), [[Base espacial - Diseno]], `Zonas/`, `Minijuegos/`, `Base/` y `Tareas_Codex/`.
- `Fase_3_Personajes/Rig_protagonista/`: esqueleto y animaciones de la protagonista.
- `Referencias/Reto_base_espacial/`: el enunciado «Tu primera base espacial».
- Fuera de la bóveda: `juego/` (el juego jugable; contrato en `juego/ARQUITECTURA.md`) y `herramientas/juego_ejecutar.py`.
