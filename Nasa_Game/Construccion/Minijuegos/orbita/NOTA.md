# Orbita arcade: entrega

El satelite cruza anillos de distintas alturas bajo gravedad central 2D: impulsar eleva el lado opuesto y frenar lo baja.
Tras los enlaces, hay que dejar una orbita casi circular a la altura media de Pegaso durante cuatro segundos sin motor.

Pantalla completa: 1280x720, rejilla 320x180 ampliada x4, campo hasta los cuatro bordes. Todo se dibuja con _draw(), mapas de caracteres y paleta de estilo.gd: trayectoria prevista, estela, particulas, destellos, sacudida, parpadeo de vida y sonidos sonar(). Sin imagenes externas ni descargas.

Controles: E, Espacio, W o arriba = progrado; S o abajo = retrogrado; soltar = inercia. Raton opcional: izquierdo motor, derecho freno. Intro empieza y cierra el resultado; Esc sale.

| Nivel | Enlaces | Margen anillo | Combustible (motor a fondo) | Limite de vuelo | Diferencia max-min final | Error del centro final |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 6 | +/-170 km | 28 s | 105 s | <=140 km | <=70 km |
| 2 | 7 | +/-120 km | 25 s | 110 s | <=90 km | <=45 km |
| 3 | 8 | +/-85 km | 23 s | 115 s | <=55 km | <=27.5 km |

Victoria: todos los enlaces, ambos margenes finales y cuatro segundos consecutivos sin motor; al menos 60 s de vuelo. Derrota en cualquier nivel: tres anillos fallados, altura <=120 km (corte atmosferico didactico), salida del campo (apoapsis previsto >6000 km o energia orbital >=0), o tiempo agotado. El combustible tambien se consume frenando; agotarlo impide corregir, pero permite continuar por inercia si la trayectoria es segura.

Las alturas verificadas se extraen de Juego.ficha("pegaso_orbita") en datos_espaciales.json. Se conserva ficha="pegaso", escena="secundaria", orden=8. La circularizacion es una mision idealizada, no una afirmacion sobre la forma real de la orbita de Pegaso. Los margenes, anillos y combustible son reglas del juego. Gravedad a=-mu*r/|r|^3, mu=398600 y R=6371; Verlet con paso fijo, tiempo fisico x210. El dibujo amplifica alturas. jugar_solo usa los mismos mandos, estado y reglas a x3.5; no fuerza resultados.

Pruebas obligatorias ejecutadas:

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:orbita --ritmo=8
13 PRUEBA_OK; 0 PRUEBA_FALLO
[godot: ok; 9 s; lineas=27; errores=0]

python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/orbita/prueba_manos.gd --ritmo=1
PRUEBAS hechas=17 fallos=0
FIN
[godot: ok; 177 s; lineas=29; errores=0]
```

Manos gana con Input.parse_input_event e InputEventKey, sin piloto ni cambios directos al vuelo. Nivel 1: 77.826 s totales, 6/6 enlaces, tres vidas, 8.00 s de motor restantes. Nivel 3: 93.788 s, 8/8 enlaces, tres vidas, 3.19 s restantes. Ambos cierran con Intro y dejan el arbol sin pausa. Registros: prueba_minijuego.log y prueba_manos.log.

Modelo adicional: PRUEBAS hechas=11 fallos=0 (modelo_arcade.log). Comprueba victoria en los tres niveles, gravedad inversa al cuadrado, independencia de los fps, alturas desde ficha y caida al frenar.

Capturas reales con ventana, revisadas visualmente; todas muestran el campo completo y marcadores legibles:

- Nasa_Game/Construccion/Minijuegos/orbita/arcade_1.png: --espera=3, primer enlace.
- Nasa_Game/Construccion/Minijuegos/orbita/arcade_2.png: --espera=12, tres enlaces y maniobra hacia el cuarto.
- Nasa_Game/Construccion/Minijuegos/orbita/arcade_3.png: --espera=20, cinco enlaces y aproximacion al sexto.

Las tres corridas devolvieron CAPTURA_OK y errores=0; comandos y salida en arcade_1.log, arcade_2.log y arcade_3.log. Los antiguos .txt y lienzo.png pertenecen a la version anterior.

Pendiente: valoracion humana de dificultad y escucha del audio. El nivel 2 tiene prueba del modelo, no prueba de manos. El motor emite un aviso del almacen de certificados y, en algunas salidas, avisos de recursos; el ejecutor devuelve errores=0 y ninguna comprobacion falla. APPDATA se redirigio a subcarpetas de esta evidencia para los logs locales.
