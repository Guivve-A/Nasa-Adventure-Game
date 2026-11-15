# Brief común

Trabajas en el «Proyecto NASA-Ecuador», un RPG educativo en Godot 4.7.2. La raíz del repositorio es tu carpeta de trabajo. Hay otros agentes trabajando a la vez en otras carpetas.

Guillermo, el director, pidió: **«Recuerda: todo debe ser jugable.»** Cada minijuego ya pasa su prueba automática, pero esa prueba lo juega con `jugar_solo()`, que no pasa por el teclado ni por el ratón. Tu trabajo es **demostrar que una persona puede jugarlo y ganarlo**, y arreglar lo que se lo impida.

Lee antes: `juego/ARQUITECTURA.md` (secciones 6 y 7), `juego/nucleo/minijuego.gd`, `juego/interfaz/anfitrion.gd` y, como ejemplo de prueba con teclas simuladas, las funciones `_tecla`, `_toque`, `_real` y `_manos` del final de `juego/pruebas/pruebas.gd`.

Reglas fijas:

- Toca **solo** la carpeta de tu minijuego (`juego/minijuegos/<id>/`) y tu carpeta de evidencia (`Nasa_Game/Construccion/Minijuegos/<id>/`).
- No instales ni descargues nada. Sin búsqueda web.
- GDScript sin `class_name`, con tabuladores y comentarios sin tildes. Tipos explícitos al leer diccionarios o JSON.
- No cambies los datos reales ni las reglas del modelo, salvo para corregir un error que demuestres.

## Qué entregar

1. **Revisión de entradas.** Lee el guion del minijuego y anota, control por control, cómo se hace cada acción con el teclado (acciones `mover_izquierda`, `mover_derecha`, `mover_arriba`, `mover_abajo`, `interactuar` = E o Intro, `saltar` = Espacio) y cómo con el ratón. Si una acción necesaria solo se puede hacer con uno de los dos, o depende de que un control tenga el foco y lo pierde, **arréglalo**.
2. **`juego/minijuegos/<id>/prueba_manos.gd`**: un guion `extends Node` con `func correr(pruebas: Node) -> void` que:
   - pone `Juego.modo_prueba = false` y `Juego.sin_guardar = true` al empezar, y deja `Juego.modo_prueba = true` al terminar;
   - abre el minijuego como lo abre el juego: lanza `Interfaz.abrir_minijuego("<id>", {"dificultad": 1})` en una corrutina aparte (sin esperar su resultado en la misma función) y espera a que `Interfaz.anfitrion.visible` sea verdadero;
   - pulsa «Empezar» con la tecla Intro simulada;
   - **parte A, solo teclado:** juega y GANA usando únicamente `Input.parse_input_event()` con `InputEventKey` (teclas físicas A, D, W, S o flechas, E, Intro y Espacio), leyendo el estado del minijuego (`Interfaz.anfitrion.get("_minijuego")`) para decidir qué tecla pulsar, como haría una persona mirando la pantalla. Cierra el resultado con Intro («Continuar»);
   - **parte B, solo ratón:** vuelve a abrirlo y lo gana usando únicamente `InputEventMouseButton` e `InputEventMouseMotion` (también con `Input.parse_input_event()`; las posiciones salen de `get_global_rect()` de cada control). Si el minijuego no tiene nada que pulsar con el ratón para alguna acción necesaria, añade ese control;
   - comprueba con `pruebas.comprobar(condicion, "nombre", "detalle")`: que cada parte terminó superada, que el anfitrión se cerró, que al terminar no queda el árbol en pausa y que cada control anunciado en el campo `controles` de `minijuego.json` responde.
3. **Corre las dos pruebas** y pega su salida en el informe:

```
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/<id>/prueba_manos.gd --ritmo=1
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:<id> --ritmo=8
```

   Las dos deben terminar sin `PRUEBA_FALLO` ni `SCRIPT ERROR`.
4. Revisa también lo que una persona nota y una prueba no: que el texto de `controles` e `instrucciones` diga exactamente las teclas que funcionan; que nada importante quede fuera del lienzo de 1120 × 520; que el primer intento a dificultad 1 sea ganable sin conocer los números; que se pueda salir con Esc en cualquier momento.
5. Informe final breve: qué controles tiene, qué arreglaste (con el porqué), la salida de las dos pruebas y lo que quede pendiente. Añade un apartado «Jugado con teclado y con ratón» a la `NOTA.md` de tu carpeta de evidencia.

@@TAREA id=manos_seguidor salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_seguidor.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `seguidor`: carpeta `juego/minijuegos/seguidor/`. Donde el brief dice `<id>`, es `seguidor`.

@@TAREA id=manos_antena salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_antena.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `antena`: carpeta `juego/minijuegos/antena/`. Donde el brief dice `<id>`, es `antena`.

@@TAREA id=manos_satelite salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_satelite.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `satelite`: carpeta `juego/minijuegos/satelite/`. Donde el brief dice `<id>`, es `satelite`.

@@TAREA id=manos_telescopio salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_telescopio.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `telescopio`: carpeta `juego/minijuegos/telescopio/`. Donde el brief dice `<id>`, es `telescopio`.

@@TAREA id=manos_linea_tiempo salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_linea_tiempo.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `linea_tiempo`: carpeta `juego/minijuegos/linea_tiempo/`. Donde el brief dice `<id>`, es `linea_tiempo`.

@@TAREA id=manos_muestras salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_muestras.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `muestras`: carpeta `juego/minijuegos/muestras/`. Donde el brief dice `<id>`, es `muestras`.

@@TAREA id=manos_banderas salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_banderas.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `banderas`: carpeta `juego/minijuegos/banderas/`. Donde el brief dice `<id>`, es `banderas`.

@@TAREA id=manos_regreso salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_regreso.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `regreso`: carpeta `juego/minijuegos/regreso/`. Donde el brief dice `<id>`, es `regreso`.

@@TAREA id=manos_orbita salida=Nasa_Game/Construccion/Tareas_Codex/informes/manos_orbita.md sandbox=workspace-write timeout=45 esfuerzo=high

Tu minijuego es `orbita`: carpeta `juego/minijuegos/orbita/`. Donde el brief dice `<id>`, es `orbita`.
