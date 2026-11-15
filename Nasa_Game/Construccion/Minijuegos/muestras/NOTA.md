# Muestras ? pantalla completa

Ampliado el arcade existente a 1280 ? 720 (320 ? 180 p?xeles l?gicos ?4), mediante `pantalla_completa = true` en `_init()`. Se conservan recolecci?n, saltos con inercia, herramientas, entrega de una bolsa por viaje y par?metros existentes.

El cielo ocupa hasta la cota 46, con estrellas, Tierra y horizonte continuo; el terreno llega a ambos lados y al borde inferior. Los recorridos usan x=10..306 e y=60..158, con caja en (32,108) y muestras en (108,68), (220,64), (284,146) y (126,148). Los cr?teres se redistribuyeron. Los indicadores flotan dentro del campo, a un m?nimo de 4 p?xeles l?gicos del borde, sin bandas ni marco exterior. E aparece como tecla dibujada junto a la herramienta; Espacio, WASD y Esc tambi?n se muestran dentro.

La velocidad pasa de 50 a 62 p?xeles l?gicos/s para compensar los trayectos ampliados. Dificultad 1 conserva 105 s de ox?geno, tres sellos, tres cr?teres peque?os e iconos de herramienta. La prueba con teclas completa las cuatro entregas con unos 72 s de ox?geno restantes y sellos restantes. Los datos reales y el contrato permanecen intactos. `minijuego.json` actualiza resumen, controles, tres instrucciones y tres pistas; conserva t?tulo, ficha, escena y orden.

## Verificaci?n

`python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:muestras --ritmo=8`

13 comprobaciones correctas; victorias en dificultades 1 y 3 y derrota deliberada explicada. Resumen observado (tambi?n en `completa_prueba.log`):

```text
[godot: ok; 13 s; lineas=30; errores=0]
```

`python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/muestras/prueba_manos.gd --ritmo=1`

Solo utiliza `Input.parse_input_event` con `InputEventKey` para jugar y pulsar Empezar/Continuar. Gana los tres niveles y las cuatro variantes de una muestra; verifica lienzo completo, ausencia de t?tulo/controles externos, piloto desactivado, cierre del anfitri?n y ?rbol sin pausa. Resumen literal de `completa_manos.log`:

```text
PRUEBAS hechas=66 fallos=0
[godot: ok; 163 s; lineas=87; errores=0]
```

Las ejecuciones usan el candado global. Godot informa problemas del entorno al escribir `user://logs` y leer certificados, adem?s de recursos pendientes al salir; el ejecutor termina con c?digo 0 y sin errores de guion ni `PRUEBA_FALLO`.

## Capturas nuevas

Comando para cada imagen: `python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=muestras --auto --captura=<ruta_absoluta> --espera=<s>`.

- `Nasa_Game/Construccion/Minijuegos/muestras/completa_1.png`: 6 s, recogida con Espacio; revisada visualmente.
- `Nasa_Game/Construccion/Minijuegos/muestras/completa_2.png`: 16 s, una entrega y otra bolsa en camino; revisada visualmente.
- `Nasa_Game/Construccion/Minijuegos/muestras/completa_3.png`: 27 s, dos entregas y regreso con roca usando pinzas; revisada visualmente.

Prueba adicional del modelo (`prueba_muestras.gd`, ritmo 8): cubre 30 combinaciones de dificultad, muestra y acierto, entrega, recuperaci?n tras herramienta err?nea, ox?geno, gravedad e inercia. Resumen de `completa_modelo.log`:

```text
PRUEBAS hechas=57 fallos=0
[godot: ok; 8 s; lineas=67; errores=0]
```

Pendiente: nada de lo solicitado. Las tres capturas finales existen, miden 1280 ? 720 y se revisaron visualmente. No se prob? un mando f?sico ni se midieron FPS. La revision visual corrigio una fila inferior causada por redondeo del horizonte. Los primeros intentos con ruta relativa no guardaron PNG; las capturas finales usan rutas absolutas y logs `completa_*_final.log`. La evidencia arcade anterior corresponde al campo de 280 ? 130.
