# Antena ? remate de Rastreo

Campo completo de 1280 ? 720 (320 ? 180 a escala 4), sin margenes. Se ampliaron cielo, arco, viento, vuelo de aves y recorrido hasta ambos bordes. Fondo fijo durante la sacudida para no descubrir bordes. HUD repartido a lo ancho y separado al menos 4 pixeles logicos del borde; mision permanente de seis palabras con pictograma y teclas dibujadas. JSON actualizado con instrucciones y pistas breves. Contrato y parametros conservados.

La estacion Quito sigue vinculada a la ficha estacion_cotopaxi: rastreo de naves de 1957 a 1981, sin relacion con Apolo 11.

## Ganar con teclas en dificultad 1

Intro empieza; A/D o flechas giran la antena. Seguir el arco con toques cortos mantiene el satelite dentro del haz ancho de 8 grados por lado. E o Espacio mantenidos estrechan el haz a 3 grados y emiten cada 0,25 s; el haz ancho emite cada 0,5 s. Esc sale.

Se conservan tres pasadas de 24, 21 y 18 s y meta de 45 paquetes. La antena permite 64 grados/s con aceleracion de 150 grados/s? y frenado exponencial de 0,16 s. Los maximos de seguimiento tras ampliar el campo son 7,41, 9,76 y 14,35 grados/s. Los paquetes pasan de 120 a 160 pixeles logicos/s para compensar la mayor distancia de descarga. No fue necesario rebajar la meta ni quitar inercia: la prueba con A/D y haz ancho obtuvo **118 paquetes**, repartidos en **45 + 39 + 34**. Hay 73 paquetes de margen sobre la meta.

La nueva prueba abre por Interfaz.abrir_minijuego en una corrutina aparte, inicia y cierra con Intro, y solo usa Input.parse_input_event con InputEventKey para jugar. Lee el estado para decidir A/D; no modifica el minijuego, no llama al piloto y verifica que este desactivado. Verifica victoria, resultado devuelto, anfitrion cerrado y arbol sin pausa.

## Pruebas

`python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:antena --ritmo=8`

```text
13 PRUEBA_OK; 0 PRUEBA_FALLO
Dificultad 1: superado=true, 224 paquetes (meta 45)
Dificultad 3: superado=true, 164 paquetes (meta 70)
Fallo deliberado: superado=false, 16 paquetes (meta 45)
FIN
[godot: ok; 18 s; lineas=30; errores=0]
```

`python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/antena/prueba_manos.gd --ritmo=1`

```text
ANTENA_MANOS paquetes=118 por_pasada=[45, 39, 34] enlace=59.29 visible=59.29
PRUEBAS hechas=9 fallos=0
FIN
[godot: ok; 76 s; lineas=21; errores=0]
```

Registros detallados: prueba_automatica.txt y prueba_manos.txt. Godot emitio avisos del entorno sobre user://logs y certificados; la primera prueba tambien aviso de dos recursos en uso al salir. El envoltorio termino con codigo 0, sin errores de guion ni fallos de pruebas. No se tocaron archivos compartidos para resolver avisos del entorno.

## Capturas

Con ventana y --auto, esperas de 6, 18 y 29 s:

- Nasa_Game/Construccion/Minijuegos/antena/arcade_1.png
- Nasa_Game/Construccion/Minijuegos/antena/arcade_2.png
- Nasa_Game/Construccion/Minijuegos/antena/arcade_3.png

Las tres capturas se abrieron y revisaron visualmente: momentos distintos, campo completo hasta los bordes, HUD y controles legibles.

## Pendiente

Nada del remate solicitado. Los avisos del entorno se dejan registrados; no bloquean las pruebas ni las capturas.
