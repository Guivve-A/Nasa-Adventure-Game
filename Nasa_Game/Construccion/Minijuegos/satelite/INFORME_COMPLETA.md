# Satelite a pantalla completa

Se conserva el arcade de montaje y enlace. `_init()` activa `pantalla_completa`; el lienzo mide 1280 x 720 (320 x 180 pixeles logicos x4).

Distribucion: HUD y vidas en y=4..14; campo abierto de cinco carriles en x=0..267, y=18..163; centros x=32,84,136,188,240. Las piezas nacen en y=28 y el carro recoge en y=146. La zona derecha x=268..319 muestra los cinco conectores y el pictograma E; el suelo ocupa todo el ancho hasta y=179. Ayudas inferiores en y=171, con cuatro pixeles de margen. Mas anchura para desplazarse y 50 pixeles extra de altura para la caida y el enlace.

La caida usa 10,5 pixeles/s (S multiplica por 2,5), conservando tiempo para reconocer y girar el conector. En nivel 1 la chatarra aparece cada 4,8 s de cinta, frente a 3,6 s antes. Se conservan tres vidas y 110 s. Datos reales y parametros intactos. JSON actualizado con controles cortos, tres instrucciones y tres pistas.

La prueba de manos observa el campo nuevo y solo pulsa teclas mediante Input.parse_input_event con InputEventKey. Comprueba lienzo completo, movimiento, giro, cinco piezas, enlace, victoria, cierre del anfitrion y arbol sin pausa en los tres niveles.

## Pruebas

`python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/satelite/prueba_manos.gd --ritmo=1`

```text
PRUEBAS hechas=28 fallos=0
FIN
[godot: ok; 99 s; lineas=45; errores=0]
```

La ejecucion emite avisos del entorno sobre user://logs y certificados, y recursos en uso al salir. No hay errores de guion ni PRUEBA_FALLO.

## Capturas con ventana

Generadas con `python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=satelite --auto --captura=<ruta absoluta> --espera=<s>` y abiertas para revision visual. Resolucion: 1280 x 720, sin marco exterior ni recortes de HUD.

- [completa_1.png](completa_1.png): 4 s, primera pieza y chatarra en caida.
- [completa_2.png](completa_2.png): 15 s, dos subsistemas montados y computadora en caida.
- [completa_3.png](completa_3.png): 27 s, cinco subsistemas montados y desplazamiento hacia el receptor para encender el enlace.

Los logs `completa_captura_1.log`, `completa_captura_2.log` y `completa_captura_3.log` registran CAPTURA_OK, FIN y errores=0. Se repitieron las capturas con rutas absolutas porque las primeras rutas relativas no permitieron guardar los PNG. Los tres archivos finales existen y fueron inspeccionados.

## Contrato y cierre

`python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:satelite --ritmo=8`

Resumen: **13 PRUEBA_OK, 0 PRUEBA_FALLO**. JSON valido; victorias automaticas en niveles 1 y 3; derrota automatica con causa explicada.

```text
PRUEBA_OK satelite.d1.termina_solo
PRUEBA_OK satelite.d1.se_puede_superar
PRUEBA_OK satelite.d3.termina_solo
PRUEBA_OK satelite.d3.se_puede_superar
PRUEBA_OK satelite.se_puede_fallar
PRUEBA_OK satelite.el_fallo_explica_la_causa
FIN
[godot: ok; 11 s; lineas=28; errores=0]
```

Sin pendientes funcionales identificados. El nivel 1 fue ganado por entradas simuladas al primer recorrido; la facilidad para una persona nueva no se midio con un jugador humano. Permanecen los avisos del entorno documentados arriba. Solo se modificaron el minijuego satelite y su evidencia.
