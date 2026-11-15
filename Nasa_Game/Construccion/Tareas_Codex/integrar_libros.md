# Brief común

Trabajas en el «Proyecto NASA-Ecuador» («Luz cenicienta»), un RPG educativo espacial en Godot 4.7.2. La raíz del repositorio es tu carpeta de trabajo. El juego principal está en `juego/` (3D low-poly pintado, 1280 × 720, renderizador Mobile, todo por código; contrato en `juego/ARQUITECTURA.md`). Hay otros agentes trabajando a la vez en otras carpetas.

## El pedido del director

Guillermo, el director, dijo el 2026-11-15: **«He integrado 2 carpetas al directorio; estas son de los minijuegos desarrollados por mis compañeros, los que van en la biblioteca… quiero que los integres de manera coherente y cohesiva.»** Antes había dicho que el *gameplay* de esos dos minijuegos es de sus compañeros (Jean, Joel y Domenica) y no se toca.

Las dos carpetas, en la raíz del repositorio, son proyectos de Godot 4.7 independientes, en 2D píxel-art, a 640 × 360 con `canvas_items` y filtro `nearest`:

| Carpeta | Proyecto | Contenido |
|---|---|---|
| `Misión Artemis/` | «Misión Artemis: Más allá de las páginas» | Base del polo sur lunar (construir el cohete, hielo, paneles, despegar), el viaje y un Marte provisional. `escenas/principal.tscn`, `codigo/`, `datos/`, `recursos/`, `LEEME.md` |
| `Marte_Gravedad2DHD/Marte_Gravedad2DHD/Mision_Artemis_Marte/` | «Misión Artemis — Marte» | Aterrizaje y nivel de Marte. `escenas/principal.tscn`, `codigo/`, `datos/marte.json`, `recursos/`, `LEEME.md`. Junto a él hay capas, objetos y un `.blend` de arte |

En el juego principal, la biblioteca de la Plaza (`juego/zonas/ciudad/ciudad.gd`, función `_usar_biblioteca`) ya ofrece dos libros, «Base en la Luna» y «Base en Marte», y abre los minijuegos con id `base_luna` y `base_marte` mediante `Interfaz.abrir_minijuego(...)`. Hoy esos minijuegos no existen en `juego/minijuegos/`. La misión secundaria `s1_base` de `juego/datos/misiones.json` usa las banderas `base_visitada`, `base_luna_hecha` y `base_marte_hecha`. El plan que se dio al equipo está en `PLAN_EQUIPO_BASE_LUNA_MARTE.md`.

## Qué significa «coherente y cohesiva»

1. **Se entra por los libros y se vuelve a la Plaza** sin costuras: el libro se abre, se juega y, al terminar o al salir, se vuelve al mismo punto de la biblioteca con el juego principal intacto (ni pausado ni con la escena cambiada).
2. **Un solo juego:** misma tecla para salir (Esc), mismo criterio de pausa, sin cerrar la aplicación (`get_tree().quit()`), sin cambiar la escena raíz (`change_scene_to_file`), sin tocar la ventana (pantalla completa, tamaño) ni la configuración global.
3. **Píxeles nítidos:** el minijuego se dibuja a 640 × 360 y se escala ×2 exacto a 1280 × 720, a pantalla completa y sin marco (el anfitrión ya admite `pantalla_completa`; mira `juego/nucleo/minijuego.gd` y `juego/interfaz/anfitrion.gd`).
4. **Progreso compartido:** al completar cada libro se pone su bandera (`base_luna_hecha` o `base_marte_hecha`), se guarda la partida y, si existe, se anota su ficha del cuaderno. Lo ya completado se puede volver a jugar.
5. **Un arco, dos libros:** el libro de la Luna cuenta la base lunar y el despegue; el de Marte, la llegada y la base marciana. Si el proyecto de la Luna trae un Marte «provisional», el libro de la Luna termina al despegar (o tras el viaje) y remite al libro de Marte, que usa el proyecto de Marte. Decide con los LEEME y el código, y explícalo.
6. **Aparecen en el menú «Minijuegos»** del juego principal con su título y su resumen, como los otros nueve.
7. **Sin tocar el gameplay de los compañeros:** reglas, niveles, datos, arte y diálogos quedan como ellos los hicieron.

## Reglas fijas

- **Las dos carpetas de origen son de solo lectura:** no edites, muevas, renombres ni borres nada dentro de `Misión Artemis/` ni de `Marte_Gravedad2DHD/`. Todo lo que el juego use es una **copia generada** dentro de `juego/minijuegos/base_luna/` y `juego/minijuegos/base_marte/`.
- La copia la hace un script repetible, `herramientas/integrar_libros.py`, para que cuando los compañeros actualicen sus carpetas baste volver a correrlo. El script copia, reescribe las rutas `res://` al nuevo sitio y aplica **solo parches mecánicos y listados** (por ejemplo, sustituir una llamada que cerraría el juego por un aviso al adaptador). Cada parche se documenta con archivo, línea y motivo. Nada de editar a mano la copia.
- No edites: `juego/zonas/` (otro agente trabaja ahí; si hace falta un cambio en `ciudad.gd`, descríbelo en el informe y no lo apliques), `juego/datos/misiones.json`, `juego/nucleo/juego.gd`, `juego/nucleo/audio.gd`, `juego/interfaz/hud.gd`, `juego/interfaz/ventana_carga.gd`, `juego/pruebas/pruebas.gd` ni los otros nueve minijuegos. Puedes ampliar `juego/interfaz/anfitrion.gd` y `juego/nucleo/minijuego.gd` solo con opciones nuevas que no cambien nada a quien no las pida.
- GDScript sin `class_name` en lo que escribas tú, con tabuladores, comentarios sin tildes y tipos explícitos al leer diccionarios o JSON. Scripts de Python con `sys.stdout.reconfigure(encoding="utf-8")`.
- No instales ni descargues nada. Sin búsqueda web. Sin créditos de Higgsfield.
- Godot solo con `python -I herramientas/juego_ejecutar.py` (candado global: espera su turno; no cierres procesos ajenos). Para ejecutar los proyectos originales sin modificarlos: `python -I herramientas/juego_ejecutar.py --ventana --proyecto="<carpeta>" -- <argumentos>` (lee la cabecera del script).
- Sin insignias, logotipos ni textos de la NASA añadidos por ti. Si los proyectos de origen traen alguno, no lo quites: anótalo en el informe para el director.

@@TAREA id=libros_mapa salida=Nasa_Game/Construccion/Tareas_Codex/informes/libros_mapa.md sandbox=workspace-write timeout=45 esfuerzo=high

**Mapa de los dos proyectos y diseño de la integración.** No escribas todavía nada en `juego/`.

1. Lee completos los dos proyectos (todo `codigo/`, `escenas/principal.tscn`, `project.godot`, `datos/`, `LEEME.md`). Ejecuta cada uno una vez con ventana para ver que arranca y saca una captura si el proyecto lo permite.
2. Escribe `Nasa_Game/Construccion/Base/Mapa de los proyectos de la biblioteca.md` con una tabla por proyecto: escena y guion de entrada; capítulos o estados y cómo se pasa de uno a otro; **cómo y dónde termina** (victoria, derrota, fin); acciones de entrada que usa y cómo las define (`InputMap`, teclas directas); todo uso de `get_tree()` (`quit`, `change_scene…`, `paused`, `root`, `reload_current_scene`), de `DisplayServer`, `Engine`, `OS`, `ProjectSettings`, `user://` y de autoloads; qué ajustes de `project.godot` necesita (tamaño, filtro, color de fondo, gravedad, capas); cada ruta `res://` que aparece en código, escenas y datos; uso de `class_name`; fuentes; audio; tamaño de los recursos; y cualquier error o aviso que salga al ejecutarlo.
3. Escribe `Nasa_Game/Construccion/Base/Integracion - Mision Artemis.md` con el **diseño**: qué libro abre qué proyecto y dónde termina cada uno (punto 5 del brief); el adaptador (un `minijuego.gd` por libro que extiende `res://nucleo/minijuego.gd`, con `pantalla_completa`, que instancia la escena copiada dentro de un `SubViewport` de 640 × 360 mostrado ×2, le pasa la entrada, detecta el final y llama a `terminar(...)`; cómo implementa `jugar_solo(acierta)` para las pruebas sin alterar las reglas); la lista prevista de parches mecánicos; el tratamiento de Esc, la pausa y el foco; el progreso y las banderas; el `minijuego.json` de cada libro (título, resumen, instrucciones cortas, controles reales, pistas, ficha, orden); la transición del libro que se abre y se cierra, dibujada por el adaptador con la paleta de `juego/interfaz/estilo.gd`; y las pruebas con teclas simuladas. Termina con riesgos y con las preguntas que solo el director puede responder.

Informe: breve, con las rutas de los dos documentos y los cinco hallazgos que más condicionan la integración.

@@TAREA id=libros_integrar salida=Nasa_Game/Construccion/Tareas_Codex/informes/libros_integrar.md sandbox=workspace-write timeout=75 esfuerzo=high

**Integrar los dos libros en el juego**, siguiendo `Nasa_Game/Construccion/Base/Integracion - Mision Artemis.md` y `Mapa de los proyectos de la biblioteca.md` (ya escritos; léelos primero y corrige el diseño si al implementarlo ves que algo no funciona, anotando el cambio).

1. `herramientas/integrar_libros.py`: copia cada proyecto a `juego/minijuegos/base_luna/libro/` y `juego/minijuegos/base_marte/libro/` (sin `.godot`, capturas, hojas de referencia, `.blend` ni herramientas), reescribe las rutas `res://`, aplica los parches mecánicos y escribe `PARCHES.md` en cada carpeta con archivo, línea, texto original, texto nuevo y motivo. Debe poder correrse otra vez sin romper nada. Después corre `python -I herramientas/juego_ejecutar.py --importar -- --prueba=nucleo` para importar los recursos.
2. Los adaptadores `juego/minijuegos/base_luna/base_luna.gd` y `juego/minijuegos/base_marte/base_marte.gd` con su `minijuego.json`, según el diseño: pantalla completa, 640 × 360 ×2 exacto y nítido, Esc para salir, final detectado, banderas `base_luna_hecha` y `base_marte_hecha` con `Juego.poner_bandera(...)` y `Juego.guardar()`, y la transición del libro. El juego principal no debe quedar en pausa ni perder su escena al salir. Si el proyecto original define acciones de entrada en su `project.godot`, el adaptador las registra al entrar si no existen.
3. `prueba_manos.gd` en cada carpeta (`extends Node`; `func correr(pruebas: Node) -> void`): con `Juego.modo_prueba = false` y `Juego.sin_guardar = true`, abre el libro con `Interfaz.abrir_minijuego`, juega de verdad unos 20 segundos con teclas simuladas (`Input.parse_input_event` con `InputEventKey`: moverse, saltar, usar), comprueba que el personaje del minijuego se movió, sale con Esc y comprueba que el anfitrión se cerró, que el árbol no queda en pausa y que la escena principal sigue ahí; vuelve a entrar y a salir una segunda vez. Deja `Juego.modo_prueba = true` al terminar.
4. Pruebas, todas sin fallos (pega el resumen): `python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:base_luna --ritmo=8`, lo mismo con `base_marte`, las dos `prueba_manos.gd` con `--prueba=guion:res://minijuegos/<id>/prueba_manos.gd --ritmo=1`, `-- --prueba=nucleo --ritmo=6` y `-- --prueba=minijuegos --ritmo=8` (los otros nueve no deben romperse).
5. Capturas con ventana de cada libro en tres momentos (`--minijuego=<id> --captura=<png> --espera=<s>`), en `Nasa_Game/Construccion/Base/capturas/`, y una medición de fps (`--minijuego=<id> --medir=5`): 50 o más en la Intel HD 620.
6. Comprueba que las carpetas de origen siguen idénticas (`git status --short` no debe mostrar cambios dentro de ellas más allá de estar sin seguimiento; compara tamaños y fechas antes y después).

Informe: qué se integró y cómo, la lista de parches, el resultado de cada prueba, los fps, las rutas de las capturas, lo que haya que cambiar en `ciudad.gd` o en `misiones.json` (sin aplicarlo), los problemas encontrados en los proyectos de origen (para avisar a los compañeros) y lo que quedó pendiente o sin verificar.
