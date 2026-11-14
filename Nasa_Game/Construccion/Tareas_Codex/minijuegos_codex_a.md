# Brief común

Trabajas en el «Proyecto NASA-Ecuador» (nombre interno), un RPG educativo de exploración en Godot 4.7.2 con arte low-poly pintado a mano. La raíz del repositorio es tu carpeta de trabajo. Equipo: portátil i5-7200U, 8 GB, Intel HD 620, Windows 10. Hay otros agentes trabajando a la vez en otras carpetas.

Construyes UN minijuego del juego jugable v0 (carpeta `juego/`). **Antes de escribir nada lee completos:**

1. `juego/ARQUITECTURA.md` (el contrato; obligatorio), sobre todo las secciones 2, 6 y 7.
2. El ejemplo que funciona: `juego/minijuegos/plantilla/plantilla.gd` y `minijuego.json`.
3. El guion base que heredas: `juego/nucleo/minijuego.gd`. Y el anfitrión que lo enmarca: `juego/interfaz/anfitrion.gd`.
4. `juego/interfaz/estilo.gd` (colores y tipografías) y `juego/datos/datos_espaciales.json` con `juego/datos/FUENTES.md` (las fichas reales).
5. La prueba que tendrás que pasar: función `_minijuego` de `juego/pruebas/pruebas.gd`.

Reglas fijas:

- Toca **solo** los archivos de tu minijuego: `juego/minijuegos/<id>/` y tu carpeta de evidencia `Nasa_Game/Construccion/Minijuegos/<id>/`. No edites nada más.
- No instales ni descargues nada. No uses Higgsfield, Firecrawl ni búsqueda web: todo lo que necesitas está en el repositorio.
- GDScript sin `class_name`, con sangría de tabuladores y comentarios sin tildes. Cuidado con `:=` sobre valores de diccionarios, listas o JSON: pon el tipo explícito (`var x: float = d["a"]`).
- Los textos que ve el jugador van en español correcto, con tildes, cortos y con cifras. Nunca la palabra «incorrecto»: al fallar se explica la causa.
- Los datos y las cifras salen de las fichas de `datos_espaciales.json`. No inventes hechos. La estación de Quito (Cotopaxi) nunca se relaciona con el Apolo 11. Nada de insignias, logotipos ni textos de la NASA o de misiones.
- El lienzo mide 1120 × 520 px. Texto de 16 px o más. Paleta de `estilo.gd`; el cian solo para datos e interacción. Se juega entero con teclado (acciones `mover_izquierda`, `mover_derecha`, `mover_arriba`, `mover_abajo`, `interactuar`, `saltar`) y también con ratón.
- Usa siempre `delta` en `_paso(delta)`, nunca la hora del sistema.
- `jugar_solo(acierta)` es obligatorio: con `true` gana **jugando con la lógica real** (moviendo el estado como lo haría una persona), y con `false` falla por un camino real con una explicación causal. Debe terminar en menos de 40 s de juego.
- `minijuego.json` completo: `titulo`, `resumen`, `instrucciones` (2 a 4), `controles`, `pistas` (3 niveles: una mirada de Órbita, una frase y la respuesta), `ficha`, `escena` y `orden`.

Prueba (ejecútala si tu entorno deja lanzar procesos; si no, dilo en el informe y explica cómo revisaste el código):

```
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:<id> --ritmo=8 --todo
```

Debe terminar sin `PRUEBA_FALLO` ni `SCRIPT ERROR`.

Informe final: qué archivos escribiste, las reglas del modelo con sus números (umbrales de victoria y duración), la salida de la prueba y lo que quede pendiente. Deja además una nota breve en tu carpeta de evidencia.

- Ya hay dos minijuegos tuyos aprobados que puedes mirar como ejemplo de calidad: `juego/minijuegos/orbita/` y `juego/minijuegos/linea_tiempo/`.
- Si en tu carpeta hay archivos de un intento anterior interrumpido, revísalos y continúa desde ahí.

@@TAREA id=regreso salida=Nasa_Game/Construccion/Tareas_Codex/informes/regreso.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `regreso`: «Volver como el módulo de mando» (escena 3.6 y sección 4.4 del borrador `Nasa_Game/Fase_2_Narrativa/Fase 2 - Analisis.md`). Al final del sueño lunar, la protagonista vuelve a la Tierra en su caja de cartón, igual que volvió el módulo de mando.

- Parte 1, ordenar los 6 pasos del regreso: despegue de la etapa de ascenso, encuentro en órbita lunar, separación del módulo de servicio, reentrada con el escudo térmico por delante, paracaídas y amerizaje. Tarjetas que se mueven con el teclado o el ratón, y botón «Comprobar». Si un par queda al revés, se explica por qué (sin el encuentro en órbita no hay nave para volver; el escudo va antes que los paracaídas).
- Parte 2, la reentrada: la caja cae y hay que mantener el escudo mirando hacia delante dentro de un margen de ángulo durante unos 20 s mientras el aire la empuja. Es un lazo de control: izquierda y derecha corrigen; si se corrige de más, oscila. Barra de temperatura que sube cuando el escudo se desvía.
- Dificultad: margen más estrecho y ráfagas más fuertes.
- El fallo explica la causa (el escudo quedó de lado demasiado tiempo; correcciones tardías y grandes hacen oscilar).
- Datos de las fichas `modulo_mando`, `regreso_seis_pasos` y `muestras_apolo11`, tal cual. Dibujo propio (una caja de cartón con un escudo; nada de insignias ni cápsulas reales).
- `minijuego.json`: ficha `modulo_mando`, escena `3.6`, orden 9.

@@TAREA id=seguidor salida=Nasa_Game/Construccion/Tareas_Codex/informes/seguidor.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `seguidor`: «El seguidor que tiembla» (escenas 1.2 y 4.1 de `Nasa_Game/Fase_2_Narrativa/Fase 2 - Analisis.md`). La protagonista estudia ingeniería de control y construyó un seguidor motorizado para que su cámara siga a la Luna. Hay que ajustar su control.

- Modelo: un motor con inercia y rozamiento sigue una referencia. Control con dos parámetros, GANANCIA y AMORTIGUACIÓN (proporcional y derivativo). Simula con paso fijo dentro de `_paso(delta)`.
- Jugada: dos deslizadores y el botón «Probar» (E o Intro). Regla de la casa: **un parámetro por prueba** (si se mueven los dos, el juego pide elegir uno). Cada prueba dura unos 5 s y se dibuja en un osciloscopio: la referencia (un punto de luz que cruza la pared), la respuesta y, más tenue, la prueba anterior al lado.
- Se supera cuando la respuesta se asienta rápido, casi sin sobrepaso y sin error final (define los tres umbrales y muéstralos como una franja en la gráfica). Máximo de pruebas según la dificultad.
- El fallo explica la causa: con poca ganancia se atrasa; con mucha ganancia y poca amortiguación oscila; con demasiada amortiguación llega tarde.
- Modo `parametros.get("modo") == "prealimentacion"` (escena 4.1): la referencia es una rampa a la velocidad conocida del cielo (15 grados por hora, ficha `cielo_15_grados`, con el reloj acelerado). Aparece un tercer control, «Velocidad conocida del cielo». Con solo realimentación queda un error constante en la rampa; al darle al motor la velocidad conocida, el error cae a cero con ganancias suaves. En dificultad 3, además, cortes breves de energía. Al superar este modo llama a `Juego.anotar("prealimentacion")`. `jugar_solo` debe funcionar en los dos modos.
- `minijuego.json`: ficha `realimentacion`, escena `1.2`, orden 1. Las fichas `ganancia`, `amortiguacion`, `realimentacion` y `prealimentacion` ya existen: úsalas para los textos.

@@TAREA id=antena salida=Nasa_Game/Construccion/Tareas_Codex/informes/antena.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `antena`: «Rastrear como en el Cotopaxi» (escena 2.1). En el sendero hay una antena parabólica caída. Hay que reapuntarla para que siga el paso de un satélite.

- Modelo: control proporcional con retardo del actuador. El satélite cruza el cielo en un arco (unos 10 s). Un solo deslizador, GANANCIA, y el botón «Probar». Con poca ganancia la antena se atrasa; con mucha, se pasa y oscila.
- Vista: el arco del cielo con el satélite y el haz de la antena, una barra de «señal recibida» y la gráfica del error con la prueba anterior al lado.
- Se supera si la señal se mantiene por encima del umbral durante el 80 % del paso. Dificultad 2 y 3: paso más rápido y ráfagas de viento.
- Datos: la estación Quito, al pie del Cotopaxi, rastreó naves de 1957 a 1981 (ficha `estacion_cotopaxi`; léela y no añadas nada: **nunca** la relaciones con el Apolo 11).
- `minijuego.json`: ficha `ganancia`, escena `2.1`, orden 2.

@@TAREA id=satelite salida=Nasa_Game/Construccion/Tareas_Codex/informes/satelite.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `satelite`: «Un cubo de 10 cm» (escena 1.5). En la mesa del club hay un kit para armar la maqueta de Pegaso, el primer satélite ecuatoriano (fichas `pegaso`, `cubesat` y `exa_2007`: léelas y usa solo sus datos).

- Jugada en dos pasos: (1) colocar los cuatro subsistemas en su sitio del cubo (energía con paneles, radio, antena y computadora) arrastrando con el ratón o con el teclado (elegir pieza y hueco); (2) cuadrar el balance de energía: elegir cómo desplegar los paneles y qué equipos encender para que lo generado cubra lo consumido en la parte de la órbita con sol y alcance la batería en la sombra (números pequeños y claros, que tú defines y rotulas como «modelo simplificado»).
- El fallo explica la causa: sin antena desplegada la radio no llega a tierra; consume más de lo que generan los paneles; sin computadora nadie ordena los datos.
- Dibujo propio del satélite (un cubo con dos paneles desplegables), sin logotipos.
- `minijuego.json`: ficha `pegaso`, escena `1.5`, orden 3.
