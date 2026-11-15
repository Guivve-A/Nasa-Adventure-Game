# Telescopio: revisión de entradas

14-11-2026. Jugado mediante eventos físicos simulados, abriendo el anfitrión real. Se ganó a dificultad 1 con teclado y con ratón, sin piloto, sin revisiones y con 100 puntos en ambos casos. Solo se editaron las dos carpetas autorizadas.

## Controles comprobados

| Acción | Teclado | Ratón |
|---|---|---|
| Empezar | Intro sobre el foco inicial del anfitrión | Clic en Empezar |
| Acimut | A/D o ←/→ (`mover_izquierda/derecha`) | Arrastrar el dial de acimut; pulsar la Luna visible la centra |
| Altura | W/S o ↑/↓ (`mover_arriba/abajo`) | Arrastrar el dial de altura; pulsar la Luna también centra este eje |
| Enfocar | A/D o ←/→ | Arrastrar el dial de enfoque; rueda arriba/abajo sobre el ocular |
| Mover la mira | WASD o las cuatro flechas | Mover el puntero o pulsar dentro del ocular |
| Confirmar cada paso y rasgo | E, Intro (`interactuar`) o Espacio (`saltar`) | Clic en Confirmar |
| Cerrar la victoria | Intro sobre Continuar | Clic en Continuar |
| Salir | Esc en instrucciones, búsqueda, enfoque, marcas y resultado | Salir en instrucciones o botón superior Salir (Esc) |

Todos los controles anunciados responden. No fue necesario añadir controles: todas las acciones ya tenían ambas vías. Las entradas durante la partida no requieren enfocar un dial ni un botón; no se fuerza el foco desde la prueba.

## Cambios y motivo

- Añadido `prueba_manos.gd`: las partes A y B ganan exclusivamente con eventos `InputEventKey` o de ratón, respectivamente, enviados por `Input.parse_input_event()`. Empezar y Continuar se prueban con Intro en A y con clic en B.
- La prueba lee las lecturas y el estado de pantalla, no llama a `jugar_solo()`, `_input()`, `_gui_input()`, `_confirmar()`, `_objetivo_auto()` ni a la validación geométrica. Los tres puntos de reconocimiento proceden del ocular revisado visualmente. Las posiciones del ratón parten de `get_global_rect()` y se transforman a píxeles de ventana, también en headless.
- Corregida la instrucción que afirmaba que la barra medía nitidez: el dial ajusta el enfoque; la nitidez aparece como porcentaje y umbral. Se precisa dónde responde la rueda del ratón.
- El botón anuncia también Intro. Las ayudas anuncian WASD además de flechas y ratón; `controles` incluye Esc. No se alteraron datos, shaders, tiempos, tolerancias ni reglas de acierto.
- La primera comprobación con ventana reveló pulsaciones de prueba demasiado cortas para garantizar un cuadro procesado y movimiento pendiente antes de capturar. Se corrigió la sincronización del guion y su cierre tras un fallo. El diagnóstico se conserva en `diagnostico_sincronizacion.log`; la ejecución final con ventana pasa completa.

## Revisión visual y primer intento

Se abrieron y revisaron las doce capturas `manos_*.png`, obtenidas durante partidas reales de la prueba con ventana. Instrucciones, controles, lecturas, tres rasgos y resultado quedan legibles. Los controles visibles también pasan comprobaciones de límites del lienzo de 1120 × 520 en búsqueda, enfoque y los tres rasgos.

El primer intento dispone de 150 s, objetivo de búsqueda escrito y Luna visible, porcentaje de nitidez con umbral, explicación de cada rasgo y guía para Crisium. No exige conocer de antemano el acimut, la altura ni el foco ideal. La prueba enfoca siguiendo la nitidez mostrada, sin consultar el foco ideal del modelo. La victoria con teclado tardó 9,769 s de juego y la de ratón 1,063 s; son tiempos de entradas automatizadas, no una medición de rapidez humana. Ambas tuvieron cero revisiones. Esc y Salir devolvieron el árbol sin pausa en todos los estados comprobados.

## Resultados finales

| Ejecución | Resultado |
|---|---|
| Guion de manos, `--ritmo=1` | 90 comprobaciones, 0 fallos; ambas victorias; `errores=0` |
| Prueba común `minijuego:telescopio`, `--ritmo=8` | 13 comprobaciones correctas; victorias en niveles 1 y 3, fallo causal esperado; `errores=0` |
| Adicional con ventana y `--evidencia_manos` | 90 comprobaciones, 0 fallos; ambas victorias; `errores=0` |

Las dos ejecuciones solicitadas terminaron con código 0, sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Sus salidas completas se pegan debajo y se conservan también en `prueba_manos.log` y `prueba_minijuego_manos.log`. La adicional está en `prueba_manos_ventana.log`.

Pendientes de jugabilidad: ninguno detectado en esta revisión. Persisten avisos del entorno sobre registros `user://logs` y certificados, y una referencia a `cleanup` en la salida contractual; se conservan tal cual. No se verificaron exportaciones ni rendimiento sostenido.

## Salidas de las dos pruebas solicitadas

<details>
<summary>prueba_manos.log</summary>

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/telescopio/prueba_manos.gd --ritmo=1
ERROR: Failed to open 'user://logs/godot2026-11-14T14.05.45.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK guion_de_prueba_existe
PRUEBA_OK telescopio.teclado.abierto
PRUEBA_OK telescopio.teclado.sin_piloto
PRUEBA_OK telescopio.teclado.Empezar
PRUEBA_OK telescopio.lienzo.buscar
PRUEBA_OK telescopio.teclado.buscar_A
PRUEBA_OK telescopio.teclado.buscar_D
PRUEBA_OK telescopio.teclado.buscar_W
PRUEBA_OK telescopio.teclado.buscar_S
PRUEBA_OK telescopio.teclado.buscar_Left
PRUEBA_OK telescopio.teclado.buscar_Right
PRUEBA_OK telescopio.teclado.buscar_Up
PRUEBA_OK telescopio.teclado.buscar_Down
PRUEBA_OK telescopio.teclado.E_confirma_busqueda
PRUEBA_OK telescopio.lienzo.enfocar
PRUEBA_OK telescopio.teclado.enfocar_A
PRUEBA_OK telescopio.teclado.enfocar_D
PRUEBA_OK telescopio.teclado.enfocar_Left
PRUEBA_OK telescopio.teclado.enfocar_Right
PRUEBA_OK telescopio.teclado.Intro_confirma_enfoque
PRUEBA_OK telescopio.teclado.mira_A
PRUEBA_OK telescopio.teclado.mira_D
PRUEBA_OK telescopio.teclado.mira_W
PRUEBA_OK telescopio.teclado.mira_S
PRUEBA_OK telescopio.teclado.mira_Left
PRUEBA_OK telescopio.teclado.mira_Right
PRUEBA_OK telescopio.teclado.mira_Up
PRUEBA_OK telescopio.teclado.mira_Down
PRUEBA_OK telescopio.lienzo.rasgo_0
PRUEBA_OK telescopio.teclado.marca_0
PRUEBA_OK telescopio.lienzo.rasgo_1
PRUEBA_OK telescopio.teclado.marca_1
PRUEBA_OK telescopio.lienzo.rasgo_2
TELESCOPIO d1 marcas=3 revisiones=0 tiempo=9.769
MINIJUEGO telescopio superado=true puntos=100.0 detalle=Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.
PRUEBA_OK telescopio.teclado.marca_2
PRUEBA_OK telescopio.teclado.superado
TELESCOPIO_MANOS teclado { "superado": true, "puntos": 100.0, "detalle": "Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.", "tiempo": 9.76933533333334 }
PRUEBA_OK telescopio.teclado.anfitrion_cerrado
PRUEBA_OK telescopio.teclado.sin_pausa
PRUEBA_OK telescopio.raton.abierto
PRUEBA_OK telescopio.raton.sin_piloto
PRUEBA_OK telescopio.raton.Empezar
PRUEBA_OK telescopio.raton.clic_centra_luna_visible
PRUEBA_OK telescopio.raton.arrastra_acimut
PRUEBA_OK telescopio.raton.arrastra_altura
PRUEBA_OK telescopio.raton.boton_confirma_busqueda
PRUEBA_OK telescopio.raton.arrastra_enfoque
PRUEBA_OK telescopio.raton.rueda_abajo
PRUEBA_OK telescopio.raton.rueda_arriba
PRUEBA_OK telescopio.raton.boton_confirma_enfoque
PRUEBA_OK telescopio.raton.mira_0
PRUEBA_OK telescopio.raton.marca_0
PRUEBA_OK telescopio.raton.mira_1
PRUEBA_OK telescopio.raton.marca_1
PRUEBA_OK telescopio.raton.mira_2
TELESCOPIO d1 marcas=3 revisiones=0 tiempo=1.063
MINIJUEGO telescopio superado=true puntos=100.0 detalle=Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.
PRUEBA_OK telescopio.raton.marca_2
PRUEBA_OK telescopio.raton.superado
TELESCOPIO_MANOS raton { "superado": true, "puntos": 100.0, "detalle": "Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.", "tiempo": 1.06252522222222 }
PRUEBA_OK telescopio.raton.anfitrion_cerrado
PRUEBA_OK telescopio.raton.sin_pausa
PRUEBA_OK telescopio.Esc_instrucciones.anfitrion_cerrado
PRUEBA_OK telescopio.Esc_instrucciones.sin_pausa
PRUEBA_OK telescopio.Esc_buscar.abierto
PRUEBA_OK telescopio.Esc_buscar.sin_piloto
PRUEBA_OK telescopio.Esc_buscar.Empezar
MINIJUEGO telescopio superado=false puntos=0.0 detalle=
PRUEBA_OK telescopio.Esc_buscar.anfitrion_cerrado
PRUEBA_OK telescopio.Esc_buscar.sin_pausa
PRUEBA_OK telescopio.Esc_etapa_1.abierto
PRUEBA_OK telescopio.Esc_etapa_1.sin_piloto
PRUEBA_OK telescopio.Esc_etapa_1.Empezar
PRUEBA_OK telescopio.Esc_etapa_1.alcanzada
MINIJUEGO telescopio superado=false puntos=0.0 detalle=
PRUEBA_OK telescopio.Esc_etapa_1.anfitrion_cerrado
PRUEBA_OK telescopio.Esc_etapa_1.sin_pausa
PRUEBA_OK telescopio.Esc_etapa_2.abierto
PRUEBA_OK telescopio.Esc_etapa_2.sin_piloto
PRUEBA_OK telescopio.Esc_etapa_2.Empezar
PRUEBA_OK telescopio.Esc_etapa_2.alcanzada
MINIJUEGO telescopio superado=false puntos=0.0 detalle=
PRUEBA_OK telescopio.Esc_etapa_2.anfitrion_cerrado
PRUEBA_OK telescopio.Esc_etapa_2.sin_pausa
PRUEBA_OK telescopio.Esc_etapa_3.abierto
PRUEBA_OK telescopio.Esc_etapa_3.sin_piloto
PRUEBA_OK telescopio.Esc_etapa_3.Empezar
TELESCOPIO d1 marcas=3 revisiones=0 tiempo=0.730
MINIJUEGO telescopio superado=true puntos=100.0 detalle=Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.
PRUEBA_OK telescopio.Esc_resultado.visible
PRUEBA_OK telescopio.Esc_etapa_3.anfitrion_cerrado
PRUEBA_OK telescopio.Esc_etapa_3.sin_pausa
PRUEBA_OK telescopio.raton_Salir_instrucciones.anfitrion_cerrado
PRUEBA_OK telescopio.raton_Salir_instrucciones.sin_pausa
PRUEBA_OK telescopio.raton_Salir_activo.abierto
PRUEBA_OK telescopio.raton_Salir_activo.sin_piloto
PRUEBA_OK telescopio.raton_Salir_activo.Empezar
MINIJUEGO telescopio superado=false puntos=0.0 detalle=
PRUEBA_OK telescopio.raton_Salir_activo.anfitrion_cerrado
PRUEBA_OK telescopio.raton_Salir_activo.sin_pausa
PRUEBA_OK telescopio.manos.arbol_sin_pausa
PRUEBAS hechas=90 fallos=0
FIN
[godot: ok; 20 s; lineas=112; errores=0]
```

</details>

<details>
<summary>prueba_minijuego_manos.log</summary>

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:telescopio --ritmo=8
ERROR: Failed to open 'user://logs/godot2026-11-14T14.06.39.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK telescopio.minijuego_json
PRUEBA_OK telescopio.json.titulo
PRUEBA_OK telescopio.json.resumen
PRUEBA_OK telescopio.json.controles
PRUEBA_OK telescopio.json.instrucciones
PRUEBA_OK telescopio.json.pistas
PRUEBA_OK telescopio.json.ficha
MINIJUEGO telescopio superado=true puntos=100.0 detalle=Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.
PRUEBA_OK telescopio.d1.termina_solo
PRUEBA_OK telescopio.d1.se_puede_superar
MINIJUEGO telescopio superado=true puntos=100.0 detalle=Reconociste 3 rasgos: terminador, luz reflejada por la Tierra y Mare Crisium. El Sol ilumina el 12,2 %.
PRUEBA_OK telescopio.d3.termina_solo
PRUEBA_OK telescopio.d3.se_puede_superar
MINIJUEGO telescopio superado=false puntos=0.0 detalle=Buscas demasiado alto: esta noche la Luna está a 20,0° de altura. Baja el telescopio.
PRUEBA_OK telescopio.se_puede_fallar
PRUEBA_OK telescopio.el_fallo_explica_la_causa
FIN
   at: cleanup (core/object/object.cpp:2536)
[godot: ok; 12 s; lineas=30; errores=0]
```

</details>

