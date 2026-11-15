# Telescopio a pantalla completa

Se conserva el arcade existente de busqueda, enfoque y exposicion. `pantalla_completa = true` activa el lienzo de 1280 x 720 (320 x 180 pixeles logicos x4). Solo se editaron telescopio.gd, minijuego.json, prueba_manos.gd y esta evidencia.

El cielo y el suelo de busqueda llegan a los bordes sin bandas de HUD. El recorrido pasa a 640 x 260 y el buscador representa ese espacio. La Luna ocupa un radio de 52 pixeles, centrada en (160, 94); sus tres dianas y el dibujo de Mare Crisium se adaptan al nuevo radio. El enfoque usa una barra de 220 pixeles en y=145. La exposicion se muestra a la derecha y la Tierra a la izquierda. Marcador, vidas y tiempo quedan arriba con al menos 4 pixeles de margen; los controles E y Esc se dibujan dentro del campo, en la parte inferior.

Dificultad 1: 100 segundos, tolerancia de 10 pixeles en las dianas, franja de enfoque de 0.23 y exposiciones de 5.5 segundos. Se mantienen tres vidas. Los datos astronomicos siguen procediendo de las fichas reales.

Metadatos: controles abreviados, tres instrucciones cortas y tres pistas del juego real. La prueba de manos conserva Input.parse_input_event con InputEventKey, recorre las tres dificultades y comprueba ademas el lienzo completo y la ausencia del titulo y controles exteriores.

## Verificacion

Contrato: `python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:telescopio --ritmo=8`

```
PRUEBA_OK telescopio.d1.termina_solo
PRUEBA_OK telescopio.d1.se_puede_superar
PRUEBA_OK telescopio.d3.termina_solo
PRUEBA_OK telescopio.d3.se_puede_superar
PRUEBA_OK telescopio.se_puede_fallar
PRUEBA_OK telescopio.el_fallo_explica_la_causa
FIN
[godot: ok; 11 s; lineas=30; errores=0]
```

Registro completo: completa_contrato.log. El motor tambien emitio avisos del entorno sobre el registro user://, certificados y recursos al salir; no hubo errores de guion ni PRUEBA_FALLO.

Manos: `python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/telescopio/prueba_manos.gd --ritmo=1`

```
PRUEBA_OK telescopio.d1.gana_con_teclas
PRUEBA_OK telescopio.d1.anfitrion_cerrado
PRUEBA_OK telescopio.d1.sin_pausa
PRUEBA_OK telescopio.d2.gana_con_teclas
PRUEBA_OK telescopio.d2.anfitrion_cerrado
PRUEBA_OK telescopio.d2.sin_pausa
PRUEBA_OK telescopio.d3.gana_con_teclas
PRUEBA_OK telescopio.d3.anfitrion_cerrado
PRUEBA_OK telescopio.d3.sin_pausa
PRUEBA_OK telescopio.manos.arbol_sin_pausa
PRUEBAS hechas=29 fallos=0
FIN
[godot: ok; 101 s; lineas=49; errores=0]
```

Registro completo: completa_manos.log. En los tres niveles se verifico tambien campo_completo, sin_marco_exterior y sin_piloto. Tiempos de juego: 27.08 s, 31.63 s y 36.91 s; tres vidas al ganar. Esta es verificacion automatizada con teclas, no una prueba humana de dificultad.

## Capturas y cierre

Capturas reales con ventana, revisadas visualmente y verificadas como PNG de 1280 x 720:

- `Nasa_Game/Construccion/Minijuegos/telescopio/completa_1.png`: inicio de la busqueda, espera 2.8 s.
- `Nasa_Game/Construccion/Minijuegos/telescopio/completa_2.png`: desplazamiento hacia la Luna, espera 4.8 s.
- `Nasa_Game/Construccion/Minijuegos/telescopio/completa_3.png`: exposicion de luz cenicienta, espera 17 s.

Se generaron con `python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=telescopio --auto --captura=<ruta_absoluta_del_png> --espera=<s>`. Registros correctos: completa_captura_1_absoluta.log, completa_captura_2_absoluta.log y completa_captura_3.log; todos terminan con errores=0. Los primeros intentos con ruta relativa no guardaron el archivo, por lo que se repitieron con rutas absolutas y se comprobo su existencia real.

Verificado el 15 de noviembre de 2026 en Godot 4.7.2, mediante el ejecutor y su candado global. Pendiente: nada de lo solicitado. La ganabilidad al primer o segundo intento por una persona sigue siendo una valoracion humana; aqui se verifico la victoria automatizada mediante teclas en los tres niveles.
