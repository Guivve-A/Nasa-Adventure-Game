# Seguidor: revision de entradas

## Control por control

| Accion | Teclado | Raton |
| --- | --- | --- |
| Empezar | Intro sobre el boton inicial con foco | Clic en Empezar |
| Elegir parametro | W/S o flechas arriba/abajo; recorre los diales | Arrastrar el dial lo selecciona |
| Ganancia | A/D o flechas izquierda/derecha con ganancia elegida | Arrastrar el primer dial |
| Amortiguacion | A/D o flechas izquierda/derecha con amortiguacion elegida | Arrastrar el segundo dial |
| Velocidad conocida, en prealimentacion | Elegir el tercer dial y ajustar con A/D o flechas | Arrastrar el tercer dial |
| Probar | E o Intro, sin necesitar foco en Probar | Clic en Probar |
| Conservar solo un cambio | Elegir el parametro y pulsar Espacio | Clic en Solo ganancia, Solo amortiguacion o Solo cielo conocido; aparecen al modificar varios |
| Continuar tras ganar | Intro sobre Continuar | Clic en Continuar |
| Salir | Esc en instrucciones, ajuste, medicion y resultado | Salir inicial o Salir (Esc) en la cabecera |

Durante la medicion los ajustes quedan bloqueados para mantener una sola configuracion por curva. Se conserva la salida por Esc y por raton. Los diales y los botones del lienzo tienen FOCUS_NONE: sus acciones de teclado llegan por _input y por el eje continuo, independientemente del foco. Empezar y Continuar reciben el foco desde el anfitrion.

## Cambios y motivo

- Las instrucciones y el pie ahora anuncian WASD, flechas y la salida, ademas de E/Intro y Espacio. El aviso de multiples cambios nombra el boton real Solo… .
- Se propone observar la oscilacion inicial y subir amortiguacion hacia la mitad del dial. Permite ganar la segunda medicion del primer intento de dificultad 1 sin memorizar la solucion numerica. Las pruebas humanas siguen esa indicacion visual.
- Al pulsar Solo… se selecciona el parametro conservado: antes la marca podia quedarse en el ultimo dial arrastrado, aunque se conservara otro. Asi Espacio y los botones muestran la misma seleccion.
- El mensaje inferior se situa en y=472 con fuente de 16 px para dejar margen al borde del lienzo. Se comprueban los rectangulos de los controles y textos contra 1120 x 520.
- prueba_manos.gd abre por Interfaz, desactiva ambos pilotos y solo genera InputEventKey o InputEventMouseButton/InputEventMouseMotion por Input.parse_input_event(). No escribe diales ni llama a _probar(), _paso(), terminar() o jugar_solo(). Lee etiquetas, seleccion, curvas y valores para decidir y verificar.

No se modifican la ecuacion, los umbrales, las fichas, los valores iniciales, la duracion ni el numero de intentos.

## Verificacion

- Manos, ritmo 1: `PRUEBAS hechas=134 fallos=0`, codigo 0, 49 s. Seguimiento normal ganado en la segunda medicion de la primera partida por ambos medios; prealimentacion ganada en la primera medicion con ambos medios. Se verifican cierre, devolucion del resultado y restauracion de pausa en cada salida.
- Prueba original, ritmo 8: 13 `PRUEBA_OK`, codigo 0, 8 s. Incluye victoria en dificultades 1 y 3 y derrota con explicacion fisica.
- Corrida adicional con ventana, ritmo 1: `PRUEBAS hechas=148 fallos=0`, codigo 0, 55 s. Las 14 comprobaciones extra guardan capturas y revisan el lienzo en esos momentos. Salida completa en [prueba_manos_ventana.txt](prueba_manos_ventana.txt).
- Sin `PRUEBA_FALLO` ni `SCRIPT ERROR` en las tres corridas finales. El entorno sigue avisando de permisos en logs de `user://` y del almacen de certificados; los envoltorios devuelven 0 y `errores=0`.

Capturas abiertas e inspeccionadas: [instrucciones](manos_instrucciones.png), [teclado](manos_teclado.png), [raton](manos_raton.png) y [tres diales con Solo…](manos_rampa_varios.png). Textos legibles, instrucciones y botones iniciales dentro de la ventana de 1280 x 720; controles, curvas y avisos dentro del lienzo de 1120 x 520, sin solapamientos importantes. El tercer dial y los tres botones Solo… caben simultaneamente. Se conservan las comparaciones de curvas y las medidas anteriores.

Los clics se calculan desde `get_global_rect()` y luego pasan por `get_final_transform()` porque `Input.parse_input_event()` recibe posiciones de ventana. El diagnostico inicial mostro escala 0,05 y margen vertical 14 en headless: enviar coordenadas de lienzo sin convertirlas llevaba el cursor fuera de los botones. Se corrigio el simulador, sin introducir una ruta de entrada especial en el minijuego.

Pendiente: ninguno funcional en este carril. Esta evidencia es una partida mediante entradas simuladas por el flujo real y una inspeccion visual; no se presenta como una sesion realizada por un participante humano.

## Salida de los dos comandos solicitados

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/seguidor/prueba_manos.gd --ritmo=1
```

<details>
<summary>Salida completa</summary>

```text
ERROR: Failed to open 'user://logs/godot2026-11-14T13.44.03.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK guion_de_prueba_existe
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.manos.empezar_intro
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.teclado.elegir_83
PRUEBA_OK seguidor.teclado.elegir_87
PRUEBA_OK seguidor.teclado.elegir_4194322
PRUEBA_OK seguidor.teclado.elegir_4194320
PRUEBA_OK seguidor.teclado.ajustar_68
PRUEBA_OK seguidor.teclado.ajustar_65
PRUEBA_OK seguidor.teclado.ajustar_4194321
PRUEBA_OK seguidor.teclado.ajustar_4194319
PRUEBA_OK seguidor.teclado.dial_0
PRUEBA_OK seguidor.teclado.dial_1
PRUEBA_OK seguidor.teclado.bloquea_varios_cambios
PRUEBA_OK seguidor.teclado.espacio_conserva_amortiguacion
PRUEBA_OK seguidor.teclado.dial_0
PRUEBA_OK seguidor.teclado.espacio_conserva_ganancia
PRUEBA_OK seguidor.teclado.dial_0
PRUEBA_OK seguidor.teclado.E_prueba
SEGUIDOR modo=paso d=1 prueba=1 K=16.0 D=1.0 cielo=0.0 asienta=4.021 sobre=0.52604 error=0.01740 juego=7.56
PRUEBA_OK seguidor.manos.medicion_termina
PRUEBA_OK seguidor.teclado.observa_oscilacion
PRUEBA_OK seguidor.teclado.dial_1
PRUEBA_OK seguidor.teclado.intro_prueba
PRUEBA_OK seguidor.manos.controles_en_1120x520
SEGUIDOR modo=paso d=1 prueba=2 K=16.0 D=7.0 cielo=0.0 asienta=1.146 sobre=0.00003 error=0.00000 juego=13.99
MINIJUEGO seguidor superado=true puntos=100.0 detalle=La respuesta queda en la franja: Asienta 1.15 s · sobrepasa 0.0 %. Error final 0.00 %. Ganancia y amortiguación equilibran rapidez y estabilidad.
PRUEBA_OK seguidor.manos.medicion_termina
PRUEBA_OK seguidor.teclado.gana_segunda_medicion
PRUEBA_OK seguidor.teclado.compara_anterior
PRUEBA_OK seguidor.teclado.superado
PRUEBA_OK seguidor.teclado.cierra_continuar
PRUEBA_OK seguidor.teclado.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.manos.empezar_raton
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.raton.arrastra_dial_0
PRUEBA_OK seguidor.raton.arrastra_dial_1
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.bloquea_varios_cambios
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.solo_ganancia
PRUEBA_OK seguidor.raton.arrastra_dial_1
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.solo_amortiguacion
PRUEBA_OK seguidor.raton.arrastra_dial_1
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.probar
SEGUIDOR modo=paso d=1 prueba=1 K=16.0 D=1.0 cielo=0.0 asienta=4.021 sobre=0.52604 error=0.01740 juego=6.47
PRUEBA_OK seguidor.manos.medicion_termina
PRUEBA_OK seguidor.raton.observa_oscilacion
PRUEBA_OK seguidor.raton.arrastra_dial_1
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.manos.controles_en_1120x520
SEGUIDOR modo=paso d=1 prueba=2 K=16.0 D=7.0 cielo=0.0 asienta=1.146 sobre=0.00003 error=0.00000 juego=11.89
MINIJUEGO seguidor superado=true puntos=100.0 detalle=La respuesta queda en la franja: Asienta 1.15 s · sobrepasa 0.0 %. Error final 0.00 %. Ganancia y amortiguación equilibran rapidez y estabilidad.
PRUEBA_OK seguidor.manos.medicion_termina
PRUEBA_OK seguidor.raton.gana_segunda_medicion
PRUEBA_OK seguidor.raton.compara_anterior
PRUEBA_OK seguidor.raton.superado
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.cierra_continuar
PRUEBA_OK seguidor.raton.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.manos.empezar_intro
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.teclado.dial_0
PRUEBA_OK seguidor.teclado.dial_1
PRUEBA_OK seguidor.teclado.dial_2
PRUEBA_OK seguidor.rampa_teclado.solo_cielo
PRUEBA_OK seguidor.teclado.dial_2
SEGUIDOR modo=rampa d=1 prueba=1 K=8.0 D=5.0 cielo=15.0 asienta=0.000 sobre=0.00083 error=0.00083 juego=8.78
MINIJUEGO seguidor superado=true puntos=100.0 detalle=La respuesta queda en la franja: Asienta 0.00 s · sobrepasa 0.1 %. Error final 0.08 %. La prealimentación anticipa el giro y la realimentación corrige el resto.
PRUEBA_OK seguidor.manos.medicion_termina
PRUEBA_OK seguidor.rampa_teclado.gana_primera_medicion
PRUEBA_OK seguidor.rampa_teclado.superado
PRUEBA_OK seguidor.rampa_teclado.cierra_esc_resultado
PRUEBA_OK seguidor.rampa_teclado.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.manos.empezar_raton
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.raton.arrastra_dial_0
PRUEBA_OK seguidor.raton.arrastra_dial_1
PRUEBA_OK seguidor.raton.arrastra_dial_2
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.rampa_raton.solo_cielo
PRUEBA_OK seguidor.raton.arrastra_dial_2
PRUEBA_OK seguidor.raton.boton_disponible
SEGUIDOR modo=rampa d=1 prueba=1 K=8.0 D=5.0 cielo=15.0 asienta=0.000 sobre=0.00083 error=0.00083 juego=6.14
MINIJUEGO seguidor superado=true puntos=100.0 detalle=La respuesta queda en la franja: Asienta 0.00 s · sobrepasa 0.1 %. Error final 0.08 %. La prealimentación anticipa el giro y la realimentación corrige el resto.
PRUEBA_OK seguidor.manos.medicion_termina
PRUEBA_OK seguidor.rampa_raton.gana_primera_medicion
PRUEBA_OK seguidor.rampa_raton.superado
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.rampa_raton.cierra_continuar
PRUEBA_OK seguidor.rampa_raton.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.esc.instrucciones
PRUEBA_OK seguidor.esc.instrucciones.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.salir_instrucciones
PRUEBA_OK seguidor.raton.salir_instrucciones.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.manos.empezar_intro
PRUEBA_OK seguidor.manos.controles_en_1120x520
MINIJUEGO seguidor superado=false puntos=0.0 detalle=
PRUEBA_OK seguidor.esc.ajuste
PRUEBA_OK seguidor.esc.ajuste.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.manos.empezar_raton
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.raton.boton_disponible
MINIJUEGO seguidor superado=false puntos=0.0 detalle=
PRUEBA_OK seguidor.raton.salir_ajuste
PRUEBA_OK seguidor.raton.salir_ajuste.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.manos.empezar_intro
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.esc.durante_medicion
MINIJUEGO seguidor superado=false puntos=0.0 detalle=
PRUEBA_OK seguidor.esc.medicion
PRUEBA_OK seguidor.esc.medicion.sin_pausa
PRUEBA_OK seguidor.manos.abre_por_interfaz
PRUEBA_OK seguidor.manos.sin_piloto
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.manos.empezar_raton
PRUEBA_OK seguidor.manos.controles_en_1120x520
PRUEBA_OK seguidor.raton.boton_disponible
PRUEBA_OK seguidor.raton.boton_disponible
MINIJUEGO seguidor superado=false puntos=0.0 detalle=
PRUEBA_OK seguidor.raton.salir_medicion
PRUEBA_OK seguidor.raton.salir_medicion.sin_pausa
PRUEBA_OK seguidor.manos.anfitrion_cerrado
PRUEBA_OK seguidor.manos.arbol_sin_pausa
PRUEBAS hechas=134 fallos=0
FIN
[godot: ok; 49 s; lineas=158; errores=0]
```

</details>

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:seguidor --ritmo=8
```

<details>
<summary>Salida completa</summary>

```text
(esperando turno: otro Godot esta corriendo)
ERROR: Failed to open 'user://logs/godot2026-11-14T13.48.15.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK seguidor.minijuego_json
PRUEBA_OK seguidor.json.titulo
PRUEBA_OK seguidor.json.resumen
PRUEBA_OK seguidor.json.controles
PRUEBA_OK seguidor.json.instrucciones
PRUEBA_OK seguidor.json.pistas
PRUEBA_OK seguidor.json.ficha
MINIJUEGO seguidor superado=true puntos=100.0 detalle=La respuesta queda en la franja: Asienta 1.02 s · sobrepasa 0.2 %. Error final 0.00 %. Ganancia y amortiguación equilibran rapidez y estabilidad.
PRUEBA_OK seguidor.d1.termina_solo
PRUEBA_OK seguidor.d1.se_puede_superar
MINIJUEGO seguidor superado=true puntos=100.0 detalle=La respuesta queda en la franja: Asienta 1.02 s · sobrepasa 0.2 %. Error final 0.00 %. Ganancia y amortiguación equilibran rapidez y estabilidad.
PRUEBA_OK seguidor.d3.termina_solo
PRUEBA_OK seguidor.d3.se_puede_superar
MINIJUEGO seguidor superado=false puntos=0.0 detalle=La ganancia empuja y falta amortiguación: el motor se pasa y oscila. Asienta 4.02 s · sobrepasa 52.6 %. Error final 1.74 %
PRUEBA_OK seguidor.se_puede_fallar
PRUEBA_OK seguidor.el_fallo_explica_la_causa
FIN
[godot: ok; 8 s; lineas=35; errores=0]
```

</details>

