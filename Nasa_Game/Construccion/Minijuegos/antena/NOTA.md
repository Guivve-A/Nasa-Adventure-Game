# Antena — escena 2.1

Implementado el minijuego «Rastrear como en el Cotopaxi». Solo se escribieron archivos de `juego/minijuegos/antena/` y esta carpeta. No hubo archivos previos de antena que continuar. No se instalaron ni descargaron recursos.

## Archivos

- `juego/minijuegos/antena/antena.gd`: modelo, interfaz, teclado/ratón y piloto real.
- `juego/minijuegos/antena/minijuego.json`: metadatos, 3 instrucciones, 3 pistas, ficha `ganancia`, escena `2.1`, orden 2.
- `juego/minijuegos/antena/prueba_modelo.gd`: comprobaciones del modelo, historial, teclado y piloto.
- Evidencia: `prueba_minijuego.log`, `prueba_modelo.log`, `captura.log`, `vista.png`, `comparacion.png` y esta nota.

## Modelo y reglas

Parámetros **didácticos**, no mediciones ni reconstrucción del equipo histórico. Las únicas cifras históricas que muestra el lienzo vienen literalmente de `estacion_cotopaxi`: 3 650 m, operación de 1957 a 1981 y entrega en 1982. El concepto de ganancia procede de `ganancia` y `FUENTES.md`. No se vincula la estación con el Apolo 11 ni se muestran emblemas.

- Paso fijo de integración: 1/120 s, acumulado exclusivamente con `delta`. Orden proporcional `u = K × (objetivo − antena)`, limitada a ±95°/s; retardo puro de 30 pasos (0,25 s) y respuesta de velocidad de primer orden con constante de 0,12 s.
- GANANCIA: 0,4–12,0, pasos de 0,1. Inicial: 1,2. El teclado mueve 6 unidades/s y acumula fracciones para no depender de la frecuencia de cuadros. Se congela durante cada prueba.
- Objetivo angular: `−60 + 120 × [p − 0,1 sin(2πp)/(2π)]` grados, con `p = t / duración`. Antena inicial: −72°, velocidad inicial 0. El arco dibujado sigue este mismo ángulo.
- Duraciones de dificultad 1/2/3: 10 / 8,5 / 7 s. D1 sin viento. D2 y D3 tienen dos ráfagas opuestas, centradas en el 32 % y 65 % del paso; cada una dura 0,64 s con perfil coseno al cuadrado. Picos: 8 y 14°/s, respectivamente, sumados como perturbación de la velocidad.
- Señal normalizada: `100 × exp[−(error / 14°)²]`. Se acumula tiempo únicamente con señal **>70 %**. Victoria si ese tiempo alcanza **≥80 %** del paso: 8 / 6,8 / 5,6 s. La banda sombreada de la gráfica corresponde aproximadamente a ±8,36°; misma escala ±40° y duración en ambas gráficas.
- Hasta 3 pruebas completas; al fallar una se puede modificar K y comparar con la anterior. El anfitrión recibe el resultado al superar o agotar las 3 pruebas. Límite de sesión: 180 s. El historial persiste al reabrir/reintentar dentro del mismo anfitrión y dificultad.
- El piloto ajusta el mismo deslizador y llama al mismo botón. Usa K=3,0 para acertar y K=12,0 para fallar; no fuerza el resultado. El camino de fallo completa las 3 pruebas. La duración máxima nominal del piloto es unos 32 s en D1, inferior a 40 s; la prueba adicional midió D2: 8,93 s al acertar y 27,93 s al fallar, con cuadros de 0,19 s.

## Validación

Prueba solicitada ejecutada con el envoltorio y su candado global:

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:antena --ritmo=8 --todo
```

También se repitió con `--todo` antes de `--` para guardar toda la salida del envoltorio:

```text
PRUEBAS hechas=13 fallos=0
FIN
[godot: ok; 7 s; lineas=31; errores=0]
```

K=3,0: D1 94,000 %, D2 92,549 %, D3 83,810 % de tiempo útil. K=12,0: D1 26,083 %, D2 25,490 %, D3 24,881 %, con 14/11/9 cruces del error por cero. K=0,4 y 1,2: 0 % útil en las tres dificultades. El fallo explica que las correcciones grandes llegan tarde, el haz se pasa y oscila.

Prueba adicional:

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/antena/prueba_modelo.gd --ritmo=8
PRUEBAS hechas=33 fallos=0
[godot: ok; 2 s; lineas=73; errores=0]
```

Comprueba ganancias bajas/media/alta en las 3 dificultades a 144 cuadros/s, oscilaciones medidas, comparación entre pruebas, historial al reabrir, ajuste de teclado a 144 cuadros/s y piloto completo D2 con `delta=0,19`. Inspección estática: tabuladores, comentarios sin tildes, sin `class_name` y JSON completo.

Capturas ejecutadas de una en una con Intel HD 620 y revisadas visualmente: `vista.png` (ganancia equilibrada) y `comparacion.png` (segunda prueba de ganancia alta y anterior al lado). Se corrigieron el solapamiento de la antena con el contador y la marca del umbral de señal.

## Pendientes de la validación original

Ninguno de implementación. Falta valoración humana del ritmo y dificultad. El entorno imprime avisos de acceso a `user://logs` y de lectura del almacén de certificados de Windows; ambas pruebas terminan sin `PRUEBA_FALLO` ni `SCRIPT ERROR` y con 0 errores contabilizados por el envoltorio. No se modificaron el núcleo ni la configuración para ocultar esos avisos.

## Jugado con teclado y con ratón

Revisión del 14 de noviembre de 2026. Se leyeron las secciones 6 y 7 de `ARQUITECTURA.md`, la base del minijuego, el anfitrión y los ejemplos de entradas físicas de `pruebas.gd`. Esta validación usa el anfitrión real con `Juego.modo_prueba = false`, `Juego.sin_guardar = true` y ambos pilotos desactivados. Todas las jugadas entran mediante `Input.parse_input_event()`; no se llaman `_probar()`, `_ajustar()`, `_integrar()`, `terminar()` ni `jugar_solo()`, ni se escribe el estado del minijuego desde la prueba.

### Revisión de entradas

| Acción | Teclado | Ratón | Observación |
|---|---|---|---|
| Empezar | Intro, con el foco inicial del anfitrión | Clic en «Empezar» | Se prueba la apertura como en el juego, en una corrutina aparte. |
| Bajar ganancia | A o ← (`mover_izquierda`), mantener | Arrastrar el deslizador hacia la izquierda | Se verifica cada tecla anunciada y el descenso con arrastre. |
| Subir ganancia | D o → (`mover_derecha`), mantener | Arrastrar el deslizador hacia la derecha | Se verifica cada tecla anunciada y el ascenso con arrastre. |
| Iniciar un paso | E o Intro (`interactuar`), Espacio (`saltar`) | Clic en «Probar» | Se prueban las tres teclas; se bloquea el ajuste durante el paso. |
| Observar el seguimiento y comparar | Sin entrada durante los 10 s del paso D1 | Igual | El motor juega el paso con la ganancia elegida; no exige apuntar manualmente. |
| Continuar después de ganar | Intro | Clic en «Continuar» | A termina exclusivamente con teclas; B termina exclusivamente con ratón. |
| Salir | Esc | Clic en «Salir (Esc)» | Esc se prueba en instrucciones, ajuste, paso en curso y resultado. |

W/S y ↑/↓ (`mover_arriba`/`mover_abajo`) no tienen acción en este minijuego de un solo parámetro y no se anuncian. El deslizador y «Probar» tienen `FOCUS_NONE`; las entradas de juego se atienden en `_input()` y `_paso()`. No requieren recuperar el foco después de usar el ratón.

### Cambios y motivo

- Se añadió una referencia visible «INICIO» junto al deslizador y se indicó en las instrucciones. La ganancia inicial 1,2 daba 0 % útil en D1 y antes solo se orientaba hacia 3,0 después de fallar. Ahora se puede elegir una primera ganancia viable mirando la marca, sin conocer los números del piloto ni esperar un fallo.
- Se anunció Esc explícitamente en `controles`. Las demás teclas anunciadas ya tenían implementación y se comprueban individualmente.
- Se añadió `prueba_manos.gd`: victoria A por teclado, victoria B por ratón, cierre del resultado, pausa restaurada, ausencia de piloto, cada control anunciado, ganancia congelada durante el paso, límites de 1120 × 520 y salidas. Hay límites de espera y limpieza con Esc si falla un cierre.
- No se cambiaron datos reales, ecuaciones, ganancias iniciales, umbrales, dificultades, tiempos ni reglas del modelo.

El diagnóstico inicial del ratón falló por las coordenadas del guion de prueba: la ventana headless mide 64 × 64, con un lienzo lógico de 1280 × 720. `diagnostico_raton.log` registra la transformación y la llegada del clic al botón real al corregir esa escala. La prueba definitiva transforma los puntos de `get_global_rect()` mediante `get_viewport().get_final_transform()` antes de inyectar los eventos; así conserva también la escala real de una ventana. No se añadieron llamadas directas a botones ni al modelo. `prueba_manos_diagnostico.log` es un registro previo con fallos, no la validación final.

### Resultados de esta revisión

| Ejecución | Comprobaciones correctas | Fallos | Resultado |
|---|---:|---:|---|
| Manos, sin ventana, ritmo 1 | 55 | 0 | Teclado: 93,8 % útil; ratón: 94 %. Ambas victorias en la primera prueba. |
| Prueba automática original, ritmo 8 | 13 | 0 | Victoria D1 y D3, fallo explicado y metadatos. |
| Manos, con ventana, ritmo 1 | 55 | 0 | Teclado y ratón: 94 % útil. Ambas victorias en la primera prueba. |

Las tres ejecuciones terminan con `FIN`, `errores=0`, sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Se respetó el candado global; los mensajes de espera reflejan ejecuciones de otros agentes. El entorno conserva los mensajes de acceso a `user://logs` y de lectura de certificados de Windows; se incluyen sin ocultarlos.

Salidas completas de los dos comandos solicitados:

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/antena/prueba_manos.gd --ritmo=1
(esperando turno: otro Godot esta corriendo)
ERROR: Failed to open 'user://logs/godot2026-11-14T13.44.52.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK guion_de_prueba_existe
PRUEBA_OK antena.teclado.abre_anfitrion
PRUEBA_OK antena.teclado.sin_piloto
PRUEBA_OK antena.teclado.empezar_con_Intro
PRUEBA_OK antena.teclado.ganancia_D
PRUEBA_OK antena.teclado.ganancia_A
PRUEBA_OK antena.teclado.ganancia_Right
PRUEBA_OK antena.teclado.ganancia_Left
PRUEBA_OK antena.manos.controles_y_textos_dentro_de_1120x520
PRUEBA_OK antena.manos.entradas_no_dependen_del_foco
PRUEBA_OK antena.teclado.Probar_con_E
PRUEBA_OK antena.teclado.ganancia_fija_durante_paso
ANTENA d1 K=2.9 paso=10.0 util=9.383 porcentaje=93.833 cruces=2 prueba=1
MINIJUEGO antena superado=true puntos=93.8 detalle=Señal > 70 % durante 93.8 % del paso; meta: 80 %. La ganancia sostiene el haz sobre el satélite.
PRUEBA_OK antena.teclado.superado
PRUEBA_OK antena.teclado.gana_primer_intento_con_marca_visible
PRUEBA_OK antena.teclado.Continuar_con_Intro.anfitrion_cerrado
PRUEBA_OK antena.teclado.Continuar_con_Intro.sin_pausa
PRUEBA_OK antena.raton.abre_anfitrion
PRUEBA_OK antena.raton.sin_piloto
PRUEBA_OK antena.raton.Empezar_existe
PRUEBA_OK antena.raton.Empezar_responde
PRUEBA_OK antena.raton.arrastrar_sube_ganancia
PRUEBA_OK antena.raton.arrastrar_baja_ganancia
PRUEBA_OK antena.raton.marca_INICIO
PRUEBA_OK antena.raton.Probar_responde
ANTENA d1 K=3.0 paso=10.0 util=9.400 porcentaje=94.000 cruces=2 prueba=1
MINIJUEGO antena superado=true puntos=94.0 detalle=Señal > 70 % durante 94.0 % del paso; meta: 80 %. La ganancia sostiene el haz sobre el satélite.
PRUEBA_OK antena.raton.superado
PRUEBA_OK antena.raton.gana_primer_intento_con_marca_visible
PRUEBA_OK antena.raton.Continuar_existe
PRUEBA_OK antena.raton.Continuar_con_clic.anfitrion_cerrado
PRUEBA_OK antena.raton.Continuar_con_clic.sin_pausa
PRUEBA_OK antena.Esc_instrucciones.abre_anfitrion
PRUEBA_OK antena.Esc_instrucciones.sin_piloto
PRUEBA_OK antena.Esc_instrucciones.anfitrion_cerrado
PRUEBA_OK antena.Esc_instrucciones.sin_pausa
PRUEBA_OK antena.Esc_ajuste.abre_anfitrion
PRUEBA_OK antena.Esc_ajuste.sin_piloto
MINIJUEGO antena superado=false puntos=0.0 detalle=
PRUEBA_OK antena.Esc_ajuste.anfitrion_cerrado
PRUEBA_OK antena.Esc_ajuste.sin_pausa
PRUEBA_OK antena.Esc_paso.abre_anfitrion
PRUEBA_OK antena.Esc_paso.sin_piloto
PRUEBA_OK antena.teclado.Probar_con_Espacio
MINIJUEGO antena superado=false puntos=0.0 detalle=
PRUEBA_OK antena.Esc_paso.anfitrion_cerrado
PRUEBA_OK antena.Esc_paso.sin_pausa
PRUEBA_OK antena.Esc_resultado.abre_anfitrion
PRUEBA_OK antena.Esc_resultado.sin_piloto
PRUEBA_OK antena.teclado.Probar_con_Intro
ANTENA d1 K=2.9 paso=10.0 util=9.383 porcentaje=93.833 cruces=2 prueba=1
MINIJUEGO antena superado=true puntos=93.8 detalle=Señal > 70 % durante 93.8 % del paso; meta: 80 %. La ganancia sostiene el haz sobre el satélite.
PRUEBA_OK antena.Esc_resultado.superado
PRUEBA_OK antena.Esc_resultado.gana_primer_intento_con_marca_visible
PRUEBA_OK antena.Esc_resultado.anfitrion_cerrado
PRUEBA_OK antena.Esc_resultado.sin_pausa
PRUEBA_OK antena.salir_raton.abre_anfitrion
PRUEBA_OK antena.salir_raton.sin_piloto
MINIJUEGO antena superado=false puntos=0.0 detalle=
PRUEBA_OK antena.raton.Salir_con_clic.anfitrion_cerrado
PRUEBA_OK antena.raton.Salir_con_clic.sin_pausa
PRUEBA_OK antena.manos.anfitrion_cerrado
PRUEBA_OK antena.manos.arbol_sin_pausa
PRUEBAS hechas=55 fallos=0
FIN
[godot: ok; 37 s; lineas=74; errores=0]
```

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:antena --ritmo=8
(esperando turno: otro Godot esta corriendo)
ERROR: Failed to open 'user://logs/godot2026-11-14T13.49.55.log'.
   at: copy (core/io/dir_access.cpp:429)
ERROR: Failed to open log file for writing: user://logs/godot.log
   at: rotate_file (core/io/logger.cpp:169)
ERROR: Failed to read the root certificate store.
   at: get_system_ca_certificates (platform/windows/os_windows.cpp:2582)
PRUEBA_OK antena.minijuego_json
PRUEBA_OK antena.json.titulo
PRUEBA_OK antena.json.resumen
PRUEBA_OK antena.json.controles
PRUEBA_OK antena.json.instrucciones
PRUEBA_OK antena.json.pistas
PRUEBA_OK antena.json.ficha
MINIJUEGO antena superado=true puntos=94.0 detalle=Señal > 70 % durante 94.0 % del paso; meta: 80 %. La ganancia sostiene el haz sobre el satélite.
PRUEBA_OK antena.d1.termina_solo
PRUEBA_OK antena.d1.se_puede_superar
MINIJUEGO antena superado=true puntos=83.8 detalle=Señal > 70 % durante 83.8 % del paso; meta: 80 %. La ganancia sostiene el haz sobre el satélite.
PRUEBA_OK antena.d3.termina_solo
PRUEBA_OK antena.d3.se_puede_superar
MINIJUEGO antena superado=false puntos=0.0 detalle=Señal > 70 % durante 26.1 % del paso; meta: 80 %. El motor recibe tarde correcciones grandes: el haz se pasa y oscila. Baja la ganancia.
PRUEBA_OK antena.se_puede_fallar
PRUEBA_OK antena.el_fallo_explica_la_causa
FIN
[godot: ok; 8 s; lineas=31; errores=0]
```

### Revisión visual

Se repitió el guion completo con ventana real, Vulkan Mobile e Intel HD Graphics 620:

```text
python -I herramientas/juego_ejecutar.py --ventana --todo -- --prueba=guion:res://minijuegos/antena/prueba_manos.gd --ritmo=1 --capturas_manos
PRUEBAS hechas=55 fallos=0
FIN
[godot: ok; 38 s; lineas=79; errores=0]
```

Registro completo: [prueba_manos_ventana.log](prueba_manos_ventana.log). Se abrieron e inspeccionaron las cuatro capturas nuevas:

- [Instrucciones](manos_instrucciones.png): pasos completos, botones «Empezar» y «Salir» visibles.
- [Ajuste inicial](manos_inicio.png): marca INICIO alineada con el deslizador, leyenda de teclas exacta y legible. El lienzo mide 1120 × 520; cada control y etiqueta cabe dentro, también según la comprobación de rectángulos.
- [Paso con ratón](manos_paso.png): seguimiento, señal, tiempo útil y curva anterior visibles, sin recortes importantes. Los textos del minijuego usan al menos 16 px.
- [Resultado](manos_resultado.png): explicación, ficha y «Continuar» visibles y accesibles.

### Pendiente tras esta revisión

No quedan bloqueos funcionales detectados. La evidencia corresponde a entradas físicas simuladas y a inspección visual de una ventana real; falta valoración humana del ritmo y de la comprensión educativa. No se instalaron ni descargaron recursos, ni se hizo búsqueda web. Los cambios y la evidencia se limitan a las dos carpetas autorizadas de `antena`.
