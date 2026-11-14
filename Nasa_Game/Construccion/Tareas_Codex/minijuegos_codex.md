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

@@TAREA id=linea_tiempo salida=Nasa_Game/Construccion/Tareas_Codex/informes/linea_tiempo.md sandbox=workspace-write timeout=50 esfuerzo=high

Minijuego `linea_tiempo`: «Ecuador ya dejó un mensaje» (escena 2.4 del borrador `Nasa_Game/Fase_2_Narrativa/Fase 2 - Analisis.md`). En el atril del Mirador hay diapositivas desordenadas con la historia espacial de Ecuador. Hay que ordenarlas de la más antigua a la más reciente.

- Los 9 hitos, que debes tomar **tal cual** de las fichas (búscalos en `datos_espaciales.json` y `FUENTES.md`; si un hito no tiene ficha, no lo uses y dilo): 1873 Observatorio Astronómico de Quito · 1957 estación Quito al pie del Cotopaxi · 1969 el disco del Apolo 11 con el mensaje de Ecuador (73 países) · 1975 apoyo al Apolo-Soyuz · 14-11-1981 despedida del STS-2 · 01-07-1982 entrega de la estación a Ecuador · 2007 nace la EXA · 2013 Pegaso · 21-06-2023 Acuerdos Artemisa (firmante n.º 26).
- Cada tarjeta muestra un título y una **pista de su época** (no el año). El jugador las ordena: con el teclado elige una tarjeta y la mueve a izquierda o derecha; con el ratón la arrastra. Botón «Comprobar».
- Al comprobar, las tarjetas bien colocadas respecto a sus vecinas se marcan y aparece el año; las demás reciben una pista más clara. No hay castigo: se sigue hasta ordenar todas o agotar los intentos (dificultad 1: 5 tarjetas y 4 comprobaciones; 2: 7 tarjetas; 3: las 9 y 3 comprobaciones).
- El fallo explica qué par quedó al revés y por qué (qué vino antes).
- `minijuego.json`: ficha `disco_apolo11`, escena `2.4`, orden 5.

@@TAREA id=orbita salida=Nasa_Game/Construccion/Tareas_Codex/informes/orbita.md sandbox=workspace-write timeout=50 esfuerzo=high

Minijuego `orbita`: «Ni se cae ni se escapa». En el Mirador hay un simulador para poner un satélite pequeño en órbita circular alrededor de la Tierra, como Pegaso.

- Modelo: gravedad de la Tierra en 2D (μ = 398 600 km³/s², radio 6 371 km), integración con paso fijo dentro de `_paso(delta)` y el tiempo acelerado. El satélite se suelta a una altura dada con velocidad tangencial.
- Jugada: un deslizador de velocidad (km/s) y el botón «Lanzar». Se ve la Tierra, la trayectoria que va dejando y, más tenue, la del intento anterior. Lecturas: altura mínima y máxima de la órbita.
- Se supera si, tras una vuelta completa, la altura mínima y la máxima difieren menos que un margen (dificultad 1: 150 km; 2: 80 km; 3: 40 km y otra altura).
- El fallo explica la causa: con poca velocidad la órbita roza la atmósfera y cae; con demasiada se alarga en una elipse o se escapa.
- Datos: busca en las fichas la altura de la órbita de Pegaso y úsala **solo si está** (si no, usa 640 km y rotúlalo como «altura de ejemplo»). La velocidad circular a esa altura sale de v = √(μ / r) y se rotula «cálculo propio». Comprueba el número en tu informe.
- `minijuego.json`: ficha `pegaso`, escena `secundaria`, orden 8.

@@TAREA id=regreso salida=Nasa_Game/Construccion/Tareas_Codex/informes/regreso.md sandbox=workspace-write timeout=50 esfuerzo=high

Minijuego `regreso`: «Volver como el módulo de mando» (escena 3.6 y sección 4.4 del borrador `Nasa_Game/Fase_2_Narrativa/Fase 2 - Analisis.md`). Al final del sueño lunar, la protagonista vuelve a la Tierra en su caja de cartón, igual que volvió el módulo de mando.

- Parte 1, ordenar los 6 pasos del regreso: despegue de la etapa de ascenso, encuentro en órbita lunar, separación del módulo de servicio, reentrada con el escudo térmico por delante, paracaídas y amerizaje. Tarjetas que se mueven con el teclado o el ratón, y botón «Comprobar». Si un par queda al revés, se explica por qué (sin el encuentro en órbita no hay nave para volver; el escudo va antes que los paracaídas).
- Parte 2, la reentrada: la caja cae y hay que mantener el escudo mirando hacia delante dentro de un margen de ángulo durante unos 20 s mientras el aire la empuja. Es un lazo de control: izquierda y derecha corrigen; si se corrige de más, oscila. Barra de temperatura que sube cuando el escudo se desvía.
- Dificultad: margen más estrecho y ráfagas más fuertes.
- El fallo explica la causa (el escudo quedó de lado demasiado tiempo; correcciones tardías y grandes hacen oscilar).
- Datos de las fichas `modulo_mando`, `regreso_seis_pasos` y `muestras_apolo11`, tal cual. Dibujo propio (una caja de cartón con un escudo; nada de insignias ni cápsulas reales).
- `minijuego.json`: ficha `modulo_mando`, escena `3.6`, orden 9.
