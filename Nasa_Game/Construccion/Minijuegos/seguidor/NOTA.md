# Seguidor — construcción

Implementación propia en `juego/minijuegos/seguidor/`. Sin descargas ni cambios al núcleo.

Motor didáctico normalizado, inercia 1 y rozamiento 0,6; integración semiimplícita a 240 Hz. Control proporcional con derivada de la medida. La velocidad conocida se convierte en esfuerzo mediante la calibración `(D + roce) × velocidad`. Estos coeficientes y umbrales son reglas del modelo, no datos de una cámara real.

Pruebas de 5 s; máximo de 6/5/4 pruebas en dificultad 1/2/3; límite humano de 180 s. Victoria: permanecer en ±4 % tras 2,5 s desde el salto (3,8 s desde el inicio en rampa), sobrepaso ≤5 % y error final ≤1,5 %. Escala normalizada; 1 equivale a 15° en rampa. Reloj ×720: 15°/h equivale a 0,2 unidades/s. Dificultad 3 en rampa: cortes [1,1; 1,2) y [1,9; 2,0) s, sin esfuerzo motor durante esos intervalos.

Fichas utilizadas: realimentacion, ganancia, amortiguacion, prealimentacion y cielo_15_grados. Definiciones completas en ayudas de los controles. La cifra celeste procede de la ficha local; no es una efeméride lunar exacta.

Prueba común: `PRUEBAS hechas=13 fallos=0`, código 0, sin PRUEBA_FALLO ni SCRIPT ERROR. Prueba adicional: `PRUEBAS hechas=19 fallos=0`, código 0 (dos modos × tres dificultades × éxito/fallo, un parámetro, invariancia con delta, atraso de rampa, anotación y teclado a 60 cuadros/s). Autopiloto a paso de prueba de 0,01 s: éxitos en 5,3–10,6 s; fallos hasta 31,8 s. Prueba común con reloj ×8: éxitos 6,08/10,74 s y fallo 32,15 s. Sin anticipación, rampa con error final 13,92 %; con 15°/h, 0,083 % (residuo numérico, dentro de tolerancia).

Capturas `seguidor.png` (anfitrión, dificultad 3) y `rampa.png` (lienzo, dificultad 3) abiertas e inspeccionadas: diales, franja, comparación y textos sin solapamientos. En rampa son visibles los intervalos de corte. Dorado al final: banda de error final; línea punteada superior: límite de sobrepaso; línea vertical: plazo de asentamiento. No quedan pendientes funcionales dentro del carril. La entrada directa `--minijuego` del núcleo no reenvía `modo`; el modo de historia se activa pasando el diccionario contratado. La prueba propia lo verifica sin tocar el núcleo.

Reproducir:

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=minijuego:seguidor --ritmo=8 --todo
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/seguidor/prueba_seguidor.gd --ritmo=8
```

Archivos: `seguidor.gd`, `minijuego.json`, `prueba_seguidor.gd`; evidencia: esta nota, `prueba_comun.txt`, `prueba_adicional.txt`, `seguidor.png` y `rampa.png`.

El entorno emite avisos de permisos al escribir logs de `user://` y al leer certificados del sistema; las pruebas finalizan con código 0. La primera captura no se guardó porque faltaba esta carpeta: no se tomó el marcador CAPTURA_OK como prueba de existencia.

## Jugado con teclado y con ratón

Revisión del 14 de noviembre de 2026: `prueba_manos.gd` abre por el anfitrión real, pulsa Empezar, gana y cierra Continuar mediante eventos físicos simulados. Parte A solo teclado; parte B solo ratón. Se verifican además el tercer dial de prealimentación con ambos medios, los tres botones Solo…, el bloqueo de cambios múltiples, las curvas anterior/actual y las salidas en cada fase, sin dejar el árbol en pausa. Los pilotos están desactivados y los diales nunca se escriben desde la prueba.

W/S o ↑/↓ eligen; A/D o ←/→ ajustan; E/Intro prueban; Espacio conserva el cambio elegido. El ratón arrastra y pulsa Probar/Solo… . Intro o clic abre Empezar y cierra Continuar; Esc y Salir abandonan. Los controles del lienzo no necesitan foco. Al pulsar Solo… ahora la selección sigue al parámetro conservado. Las instrucciones proponen subir amortiguación hacia el centro tras observar oscilaciones; la prueba gana la segunda medición de dificultad 1 siguiendo esa pista, sin memorizar 6,5. Modelo y datos sin cambios.

La prueba de manos sin ventana finalizó `PRUEBAS hechas=134 fallos=0`, código 0. Sus clics parten de `get_global_rect()` y se convierten con `get_final_transform()` a coordenadas de ventana, necesario también en headless (escala 0,05 y margen vertical 14 observados). Revisión completa, comandos, resultados finales y salidas en [INFORME_MANOS.md](INFORME_MANOS.md).

Prueba original: 13 `PRUEBA_OK`, código 0, 8 s. Repetición con ventana y capturas: `PRUEBAS hechas=148 fallos=0`, código 0, 55 s. Sin `PRUEBA_FALLO` ni `SCRIPT ERROR` en las tres corridas finales. Las cuatro capturas `manos_*.png` fueron abiertas e inspeccionadas: instrucciones, botones, diales y texto dentro de sus límites, incluidos los tres botones Solo… de rampa. Sin pendientes funcionales en este carril; las partidas se realizaron con eventos de entrada simulados y revisión visual.
