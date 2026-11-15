# Satelite: revision de entradas

Fecha: 14-11-2026. La prueba abre el anfitrión real con dificultad 1 y lo gana primero solo con teclado y después solo con ratón. Todos los eventos entran mediante `Input.parse_input_event()`; no usa `jugar_solo()`, llamadas a manejadores, señales artificiales ni escritura del estado del modelo.

| Acción | Teclado | Ratón |
| --- | --- | --- |
| Empezar | Intro con el foco inicial del anfitrión | Clic en Empezar |
| Elegir pieza | A/D/W/S o flechas, recorrido circular | Clic sobre la pieza |
| Tomar pieza | E o Intro | Pulsar la pieza; mantener para arrastrar |
| Elegir hueco | A/D o izquierda/derecha: una posición; W/S o arriba/abajo: una fila de dos posiciones | Mover hasta el hueco |
| Colocar pieza | E o Intro | Soltar el arrastre en el hueco, o clic en pieza y después clic en hueco |
| Comprobar montaje | Espacio | Clic en Comprobar |
| Elegir fila de ajuste | W/S o arriba/abajo, recorrido circular | Clic directamente sobre la fila |
| Abrir/cerrar paneles | A/izquierda retrocede; D/derecha, E o Intro avanza entre plegados, uno y dos | Clic en Paneles avanza entre los tres estados |
| Antena | Elegir fila y A/D, izquierda/derecha, E o Intro alterna | Clic en Antena |
| Computadora | Elegir fila y A/D, izquierda/derecha, E o Intro alterna | Clic en Computadora |
| Radio al sol | Elegir fila y A/D, izquierda/derecha, E o Intro alterna | Clic en Radio al sol |
| Radio en sombra | Elegir fila y A/D, izquierda/derecha, E o Intro alterna | Clic en Radio en sombra |
| Probar ciclo | Espacio | Clic en Probar ciclo |
| Continuar tras victoria | Intro con el foco inicial del resultado | Clic en Continuar |
| Salir | Esc durante instrucciones, pieza tomada, ajustes, sol, sombra y resultado | Clic en Salir (Esc) |

La partida recibe acciones en `_input`, independientemente del foco de los botones. Durante el ciclo los ajustes se bloquean por igual para teclado y ratón; solo hay que observar la batería o salir. Empezar y Continuar usan el foco que asigna el anfitrión.

Cambios: el texto anterior decía que todas las flechas elegían ajustes, aunque izquierda/derecha cambia el valor. Se precisaron los controles en el JSON y en el lienzo, se explicó Comprobar y se anunció la colocación por dos clics que ya funcionaba. Las instrucciones y el balance ahora indican abrir ambos paneles y la antena y apagar la radio en sombra: el primer intento no exige adivinar cifras. Se añadieron regiones Control con nombre y ayuda sobre las piezas y los huecos; conservan el dibujo y propagan la entrada al lienzo, y permiten obtener sus posiciones mediante `get_global_rect()`.

La revisión no encontró una acción necesaria exclusiva de un dispositivo ni un bloqueo de foco en el minijuego. No se cambiaron los datos reales, los costes, la capacidad, las condiciones de victoria, los tiempos ni el piloto. La brecha principal era la evidencia: la prueba anterior llamaba directamente a `_input()` y `_gui_input()`, y no podía demostrar la llegada de eventos desde el anfitrión.

`prueba_manos.gd` comprueba cada tecla anunciada, las cuatro piezas, los cinco ajustes con ambos dispositivos, Comprobar, Probar, Continuar, el cierre y la restauración de pausa. También verifica los controles y textos dentro de 1120 × 520 y Esc en seis momentos de la partida. La parte B usa exclusivamente eventos de ratón desde Empezar hasta Continuar. Las comprobaciones de Esc son un recorrido adicional separado.

La primera corrida detectó un error de coordenadas en el propio guion de prueba: headless presenta una ventana de 64 × 64, mientras el lienzo lógico es 1280 × 720. Se corrigió aplicando `get_viewport().get_final_transform()` a las posiciones obtenidas de los controles. El diagnóstico inicial está en `diagnostico_manos_coordenadas.log`; no representa el resultado final.

Las capturas `manos_instrucciones.png`, `manos_raton_montaje.png`, `manos_teclado_balance.png`, `manos_raton_balance.png` y `manos_resultado.png` corresponden a una corrida con ventana real. La comprobación visual se registra junto a los resultados finales de abajo.

Pendientes funcionales del minijuego: ninguno identificado. El entorno emite errores de acceso a `user://logs` y al almacén de certificados, ajenos a este carril; se conservan en la salida. No se verificó un mando físico ni una sesión con una persona operando dispositivos: la evidencia es entrada física simulada y presentación real con ventana.

## Salida de las pruebas finales

Resultado final: 88 comprobaciones de manos y 13 de contrato correctas, sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Ambas partidas de manos ganan en el primer intento; el cierre restaura la pausa. La corrida adicional con ventana repite las 88 comprobaciones sin fallos.

Revision visual final: se abrieron las cinco capturas. Instrucciones, montaje, ambos balances y resultado son legibles, las tildes y flechas se muestran correctamente y ningun control importante queda recortado. El pie de controles ocupa dos lineas.

### prueba_manos.log

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/satelite/prueba_manos.gd --ritmo=1
ERROR: Failed to open 'user://logs/godot2026-11-14T13.58.45.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK guion_de_prueba_existe
PRUEBA_OK satelite.teclado.abre_anfitrion
PRUEBA_OK satelite.teclado.sin_piloto
PRUEBA_OK satelite.teclado.Empezar_Intro
PRUEBA_OK satelite.teclado.elegir_A
PRUEBA_OK satelite.teclado.elegir_D
PRUEBA_OK satelite.teclado.elegir_W
PRUEBA_OK satelite.teclado.elegir_S
PRUEBA_OK satelite.teclado.elegir_Left
PRUEBA_OK satelite.teclado.elegir_Right
PRUEBA_OK satelite.teclado.elegir_Up
PRUEBA_OK satelite.teclado.elegir_Down
PRUEBA_OK satelite.teclado.tomar_E
PRUEBA_OK satelite.teclado.hueco_arriba_dos_columnas
PRUEBA_OK satelite.teclado.hueco_abajo_dos_columnas
PRUEBA_OK satelite.teclado.montaje_Enter_y_Comprobar_Espacio
PRUEBA_OK satelite.ajustes_teclado.dentro_1120x520
PRUEBA_OK satelite.teclado.cambiar_A
PRUEBA_OK satelite.teclado.cambiar_D
PRUEBA_OK satelite.teclado.cambiar_Left
PRUEBA_OK satelite.teclado.cambiar_Right
PRUEBA_OK satelite.teclado.cambiar_E
PRUEBA_OK satelite.teclado.cambiar_Enter
PRUEBA_OK satelite.teclado.fila_W
PRUEBA_OK satelite.teclado.fila_S
PRUEBA_OK satelite.teclado.fila_Up
PRUEBA_OK satelite.teclado.fila_Down
PRUEBA_OK satelite.teclado.ajuste_antena
PRUEBA_OK satelite.teclado.ajuste_computadora
PRUEBA_OK satelite.teclado.ajuste_radio_sol
PRUEBA_OK satelite.teclado.ajuste_radio_sombra
PRUEBA_OK satelite.teclado.Probar_Espacio
SATELITE d1 fase=3 paneles=2 bateria=2.000 juego=12.511
MINIJUEGO satelite superado=true puntos=100.0 detalle=Las 4 piezas funcionan: generas 10 u, consumes 5 u al sol y guardas 4 u; en sombra gastas 2 u. Modelo simplificado.
PRUEBA_OK satelite.teclado.superado_primer_intento
PRUEBA_OK satelite.teclado.Continuar_Intro.anfitrion_cerrado
PRUEBA_OK satelite.teclado.Continuar_Intro.sin_pausa
PRUEBA_OK satelite.raton.abre_anfitrion
PRUEBA_OK satelite.raton.sin_piloto
PRUEBA_OK satelite.raton.Empezar_clic
PRUEBA_OK satelite.montaje_raton.dentro_1120x520
PRUEBA_OK satelite.raton.arrastrar_pieza_0
PRUEBA_OK satelite.raton.tomar_clic_1
PRUEBA_OK satelite.raton.colocar_clic_pieza_1
PRUEBA_OK satelite.raton.arrastrar_pieza_2
PRUEBA_OK satelite.raton.tomar_clic_3
PRUEBA_OK satelite.raton.colocar_clic_pieza_3
PRUEBA_OK satelite.raton.Comprobar_clic
PRUEBA_OK satelite.raton.ajuste_paneles
PRUEBA_OK satelite.raton.ajuste_antena
PRUEBA_OK satelite.raton.ajuste_computadora
PRUEBA_OK satelite.raton.ajuste_radio_sol
PRUEBA_OK satelite.raton.ajuste_radio_sombra
PRUEBA_OK satelite.ajustes_raton.dentro_1120x520
PRUEBA_OK satelite.raton.Probar_clic
SATELITE d1 fase=3 paneles=2 bateria=2.000 juego=11.066
MINIJUEGO satelite superado=true puntos=100.0 detalle=Las 4 piezas funcionan: generas 10 u, consumes 5 u al sol y guardas 4 u; en sombra gastas 2 u. Modelo simplificado.
PRUEBA_OK satelite.raton.superado_primer_intento
PRUEBA_OK satelite.raton.Continuar_clic.anfitrion_cerrado
PRUEBA_OK satelite.raton.Continuar_clic.sin_pausa
PRUEBA_OK satelite.Esc_instrucciones.abre_anfitrion
PRUEBA_OK satelite.Esc_instrucciones.sin_piloto
PRUEBA_OK satelite.Esc_instrucciones.anfitrion_cerrado
PRUEBA_OK satelite.Esc_instrucciones.sin_pausa
PRUEBA_OK satelite.Esc_pieza_tomada.abre_anfitrion
PRUEBA_OK satelite.Esc_pieza_tomada.sin_piloto
MINIJUEGO satelite superado=false puntos=0.0 detalle=
PRUEBA_OK satelite.Esc_pieza_tomada.anfitrion_cerrado
PRUEBA_OK satelite.Esc_pieza_tomada.sin_pausa
PRUEBA_OK satelite.Esc_ajustes.abre_anfitrion
PRUEBA_OK satelite.Esc_ajustes.sin_piloto
MINIJUEGO satelite superado=false puntos=0.0 detalle=
PRUEBA_OK satelite.Esc_ajustes.anfitrion_cerrado
PRUEBA_OK satelite.Esc_ajustes.sin_pausa
PRUEBA_OK satelite.Esc_sol.abre_anfitrion
PRUEBA_OK satelite.Esc_sol.sin_piloto
MINIJUEGO satelite superado=false puntos=0.0 detalle=
PRUEBA_OK satelite.Esc_sol.anfitrion_cerrado
PRUEBA_OK satelite.Esc_sol.sin_pausa
PRUEBA_OK satelite.Esc_sombra.abre_anfitrion
PRUEBA_OK satelite.Esc_sombra.sin_piloto
PRUEBA_OK satelite.Esc_alcanza_sombra
MINIJUEGO satelite superado=false puntos=0.0 detalle=
PRUEBA_OK satelite.Esc_sombra.anfitrion_cerrado
PRUEBA_OK satelite.Esc_sombra.sin_pausa
PRUEBA_OK satelite.Esc_resultado.abre_anfitrion
PRUEBA_OK satelite.Esc_resultado.sin_piloto
SATELITE d1 fase=3 paneles=2 bateria=2.000 juego=10.094
MINIJUEGO satelite superado=true puntos=100.0 detalle=Las 4 piezas funcionan: generas 10 u, consumes 5 u al sol y guardas 4 u; en sombra gastas 2 u. Modelo simplificado.
PRUEBA_OK satelite.Esc_resultado.superado_primer_intento
PRUEBA_OK satelite.Esc_resultado.anfitrion_cerrado
PRUEBA_OK satelite.Esc_resultado.sin_pausa
PRUEBA_OK satelite.salir_raton.abre_anfitrion
PRUEBA_OK satelite.salir_raton.sin_piloto
MINIJUEGO satelite superado=false puntos=0.0 detalle=
PRUEBA_OK satelite.raton.Salir_clic.anfitrion_cerrado
PRUEBA_OK satelite.raton.Salir_clic.sin_pausa
PRUEBA_OK satelite.manos.anfitrion_cerrado
PRUEBA_OK satelite.manos.arbol_sin_pausa
PRUEBAS hechas=88 fallos=0
FIN
[godot: ok; 59 s; lineas=109; errores=0]
```

### prueba_minijuego_manos.log

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:satelite --ritmo=8
ERROR: Failed to open 'user://logs/godot2026-11-14T13.59.48.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK satelite.minijuego_json
PRUEBA_OK satelite.json.titulo
PRUEBA_OK satelite.json.resumen
PRUEBA_OK satelite.json.controles
PRUEBA_OK satelite.json.instrucciones
PRUEBA_OK satelite.json.pistas
PRUEBA_OK satelite.json.ficha
MINIJUEGO satelite superado=true puntos=100.0 detalle=Las 4 piezas funcionan: generas 10 u, consumes 5 u al sol y guardas 4 u; en sombra gastas 2 u. Modelo simplificado.
PRUEBA_OK satelite.d1.termina_solo
PRUEBA_OK satelite.d1.se_puede_superar
MINIJUEGO satelite superado=true puntos=100.0 detalle=Las 4 piezas funcionan: generas 8 u, consumes 5 u al sol y guardas 3 u; en sombra gastas 2 u. Modelo simplificado.
PRUEBA_OK satelite.d3.termina_solo
PRUEBA_OK satelite.d3.se_puede_superar
MINIJUEGO satelite superado=false puntos=0.0 detalle=Sin antena desplegada la radio no llega a tierra: falta el enlace para enviar datos.
PRUEBA_OK satelite.se_puede_fallar
PRUEBA_OK satelite.el_fallo_explica_la_causa
FIN
[godot: ok; 23 s; lineas=29; errores=0]
```

### Corrida adicional con ventana

```text
python -I herramientas/juego_ejecutar.py --ventana --todo -- --prueba=guion:res://minijuegos/satelite/prueba_manos.gd --ritmo=1 --capturas_manos
SATELITE_CAPTURA manos_instrucciones error=0
SATELITE_CAPTURA manos_teclado_balance error=0
SATELITE_CAPTURA manos_resultado error=0
SATELITE_CAPTURA manos_raton_montaje error=0
SATELITE_CAPTURA manos_raton_balance error=0
PRUEBAS hechas=88 fallos=0
FIN
[godot: ok; 78 s; lineas=115; errores=0]
```
