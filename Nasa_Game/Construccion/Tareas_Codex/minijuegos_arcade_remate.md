# Brief común

Trabajas en el «Proyecto NASA-Ecuador», un RPG educativo espacial en Godot 4.7.2 (carpeta `juego/`). La raíz del repositorio es tu carpeta de trabajo. Hay otros agentes trabajando a la vez en otras carpetas.

Tu minijuego YA fue rehecho como arcade de acción (campo en píxeles gordos dibujado con `_draw()`, marcador, vidas y tiempo) y pasa su prueba automática. El director pidió: «como minijuegos de Atari, con misiones básicas, no puro texto» y «todo debe ser jugable». La reescritura se cortó antes del remate. **No lo rehagas: remátalo.**

Lee antes: `juego/ARQUITECTURA.md` (secciones 6 y 7), `juego/nucleo/minijuego.gd`, `juego/interfaz/anfitrion.gd`, el guion de tu minijuego completo y, como ejemplo de teclas simuladas, las funciones `_tecla`, `_toque`, `_real` y `_manos` del final de `juego/pruebas/pruebas.gd`.

## Qué entregar

0. **Campo a PANTALLA COMPLETA.** El director dijo: «lo que no me gusta son los bordes en los minijuegos». El anfitrión ya no dibuja marco, y el contrato nuevo deja al minijuego ocupar toda la pantalla: añade `func _init() -> void: pantalla_completa = true` (mira `juego/nucleo/minijuego.gd`); el lienzo pasa de 1120 × 520 a **1280 × 720, es decir 320 × 180 píxeles gordos ×4**. Adapta el juego a ese campo: fondo, suelo, cielo y recorridos llegan a los cuatro bordes; el marcador, las vidas, la barra y el tiempo van dentro del campo, a 4 píxeles lógicos o más del borde; reparte el espacio ganado (más cielo, más recorrido), no lo dejes vacío. Con pantalla completa el anfitrión no muestra título ni línea de controles durante la partida: lo imprescindible (por ejemplo «E») se dibuja en el campo como pictograma. Revisa todas las constantes que dependían de 280 × 130 y vuelve a ajustar la dificultad 1 para que siga siendo ganable.
1. **`minijuego.json` al día con el juego nuevo.** Hoy el pie de la pantalla muestra controles de la versión vieja (tarjetas, diales, «Probar»). Reescribe `controles` (una línea corta: flechas o WASD, E o Espacio, Esc), `instrucciones` (2 o 3 frases muy cortas), `resumen` y las 3 `pistas` para que describan lo que de verdad se juega. Conserva `titulo`, `ficha`, `escena` y `orden`. Nada de párrafos.
2. **Coherencia en pantalla.** Durante la partida no debe quedar texto de la versión vieja ni controles que ya no existen. La misión se muestra con un pictograma y una línea de 8 palabras como máximo.
3. **`prueba_manos.gd` nueva** en la carpeta del minijuego (`extends Node`; `func correr(pruebas: Node) -> void`), que sustituye a la vieja si existe:
   - pone `Juego.modo_prueba = false` y `Juego.sin_guardar = true` al empezar, y deja `Juego.modo_prueba = true` al terminar;
   - abre el minijuego como lo abre el juego: lanza `Interfaz.abrir_minijuego("<id>", {"dificultad": 1})` en una corrutina aparte y espera a que `Interfaz.anfitrion.visible` sea verdadero;
   - pulsa «Empezar» con la tecla Intro simulada;
   - juega y GANA usando únicamente `Input.parse_input_event()` con `InputEventKey` (teclas físicas A, D, W, S o flechas, E, Intro y Espacio), leyendo el estado del minijuego (`Interfaz.anfitrion.get("_minijuego")`) para decidir qué tecla pulsar, como haría una persona mirando la pantalla; cierra el resultado con Intro;
   - comprueba con `pruebas.comprobar(condicion, "nombre", "detalle")` que terminó superado, que el anfitrión se cerró y que el árbol no queda en pausa.
   Si al jugarlo con teclas descubres que una persona no puede ganarlo en dificultad 1 (margen imposible, tecla que no responde, foco perdido), **arréglalo en el guion del minijuego** y explica el cambio con los números.
4. **Tres capturas** con ventana en momentos distintos de la partida, en `Nasa_Game/Construccion/Minijuegos/<id>/arcade_1.png`, `arcade_2.png` y `arcade_3.png`:

```
python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=<id> --auto --captura=<png> --espera=<s>
```

5. **Las dos pruebas sin fallos** (pega el resumen en el informe):

```
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:<id> --ritmo=8
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/<id>/prueba_manos.gd --ritmo=1
```

## Reglas fijas

- Toca **solo** `juego/minijuegos/<id>/` y tu evidencia en `Nasa_Game/Construccion/Minijuegos/<id>/`.
- No instales ni descargues nada. Sin búsqueda web. Sin créditos de Higgsfield.
- GDScript sin `class_name`, con tabuladores, comentarios sin tildes y tipos explícitos al leer diccionarios o JSON.
- Godot solo con `python -I herramientas/juego_ejecutar.py` (candado global: espera su turno; no cierres procesos ajenos).
- No cambies los datos reales (salen de `juego/datos/datos_espaciales.json`). Contrato intacto: `_preparar`, `_empezar`, `_paso(delta)`, `terminar(...)`, `jugar_solo(acierta)` y los `parametros` que ya acepta.

## Informe

Breve: qué cambiaste, cómo se gana con teclas en dificultad 1 (con los números), el resultado de las dos pruebas, las rutas de las capturas y lo que quedó pendiente.

@@TAREA id=remate_seguidor salida=Nasa_Game/Construccion/Tareas_Codex/informes/remate_seguidor.md sandbox=workspace-write timeout=45 esfuerzo=medium

Tu minijuego: id `seguidor`, carpeta `juego/minijuegos/seguidor/` («El seguidor que tiembla»: mantener la Luna dentro del visor manejando un motor con inercia; con `parametros.modo == "prealimentacion"` hay ayuda de «velocidad del cielo» y al ganar así se llama `Juego.anotar("prealimentacion")`).

@@TAREA id=remate_antena salida=Nasa_Game/Construccion/Tareas_Codex/informes/remate_antena.md sandbox=workspace-write timeout=45 esfuerzo=medium

Tu minijuego: id `antena`, carpeta `juego/minijuegos/antena/` («Rastreo»: girar la antena para seguir satélites y bajar paquetes en 3 pasadas). La estación de Quito (ficha `estacion_cotopaxi`) rastreó naves de 1957 a 1981 y nunca se relaciona con el Apolo 11.

@@TAREA id=remate_banderas salida=Nasa_Game/Construccion/Tareas_Codex/informes/remate_banderas.md sandbox=workspace-write timeout=45 esfuerzo=medium

Tu minijuego: id `banderas`, carpeta `juego/minijuegos/banderas/` («Dos banderas, un cielo»: hincar los mástiles al compás, extender la barra y nivelar las dos banderas). Respeto absoluto: las banderas de Estados Unidos y de Ecuador no caen ni se dañan; la histórica no se muestra.

@@TAREA id=remate_regreso salida=Nasa_Game/Construccion/Tareas_Codex/informes/remate_regreso.md sandbox=workspace-write timeout=45 esfuerzo=medium

Tu minijuego: id `regreso`, carpeta `juego/minijuegos/regreso/` («Reentrada»: mantener el escudo por delante, esquivar el calor, abrir los paracaídas en la franja y amerizar en la zona marcada).
