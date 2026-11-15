# Telescopio: La Luna sonriente — arcade

El visor recorre un cielo de 560 × 200 unidades, con inercia y un buscador del cielo completo. Centra la sonrisa baja del oeste y fija el enfoque al cruzar la aguja la franja dorada.
Después sigue tres dianas que derivan sobre la Luna: terminador, luz cenicienta y Mare Crisium. Mantener la exposición sobre cada rasgo llena su registro; la segunda muestra el recorrido Sol → Tierra → noche lunar.

Controles: flechas o WASD para mover; E o Espacio para centrar y enfocar, y mantener para registrar. Suelta la acción al pasar a otra diana. Intro abre y cierra las pantallas del anfitrión; Esc sale.

| Dificultad | Tiempo máximo | Centrado, radio | Foco, distancia máxima a 0,5 | Diana, radio | Exposición por rasgo | Exposición fuera antes del golpe |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 90 s | 10 px | ±0,20 | 8 px | 6 s | 0,85 s |
| 2 | 80 s | 8 px | ±0,14 | 6 px | 7 s | 0,65 s |
| 3 | 70 s | 6 px | ±0,09 | 4 px | 8 s | 0,45 s |

Los píxeles de la tabla son lógicos, antes del escalado ×4. En los tres niveles se gana al registrar los tres rasgos y se pierde al agotar el tiempo o las 3 vidas. Cada centrado fallido, enfoque fuera de franja o exposición movida cuesta una vida; resta 1,5 s del registro en curso. La deriva horizontal aumenta de ±2 a ±4 y ±6 px; la vertical, de ±1 a ±2 y ±3 px. Hay 1,3 s de inmunidad tras un golpe y 1,2 s de gracia entre registros. Los tiempos de exposición, escalas y márgenes son reglas de juego, no mediciones astronómicas.

Campo de 280 × 130, escalado ×4 a 1120 × 520: todo mediante `_draw()`, rectángulos enteros, mapas de caracteres y disco lunar calculado. No carga imágenes ni los shaders antiguos. Incluye partículas, destellos, sacudida, parpadeo y sonidos. Conserva id, herencia, contrato, dificultad, ficha, escena `2.2` y orden `4`; acepta además `semilla` para reproducir las estrellas.

Los valores se leen de `Juego.ficha`, procedentes de `juego/datos/datos_espaciales.json`: iluminación y altura de `luna_12_noviembre`, orientación de `luna_sonriente`; el anfitrión presenta `luz_cenicienta`. La única línea final reúne 12,2 %, 20,0 grados y el origen terrestre de la luz cenicienta. El reloj no cambia la efeméride.

## Verificación

Contrato obligatorio:

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:telescopio --ritmo=8
13 PRUEBA_OK; ningún PRUEBA_FALLO
[godot: ok; 10 s; lineas=30; errores=0]
```

Log: [arcade_prueba_contrato.log](arcade_prueba_contrato.log). Gana en niveles 1 y 3 y pierde usando las mismas reglas con `jugar_solo(false)`.

Teclas obligatorias, sin piloto ni cambios directos del estado:

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/telescopio/prueba_manos.gd --ritmo=1
PRUEBAS hechas=23 fallos=0
[godot: ok; 95 s; lineas=39; errores=0]
```

Log: [arcade_prueba_manos.log](arcade_prueba_manos.log). Ganó los tres niveles en 27,05 / 29,90 / 34,33 s de juego usando flechas + E, WASD + E y flechas + Espacio, respectivamente. La prueba pulsa Empezar y Continuar con Intro, comprueba los tres rasgos, el cierre del anfitrión y el árbol sin pausa en cada partida; al terminar restaura `Juego.modo_prueba = true`.

La prueba adicional del modelo comprueba los tres niveles, datos cargados y derrota por tiempo:

```text
PRUEBAS hechas=8 fallos=0
[godot: ok; 13 s; lineas=22; errores=0]
```

Log: [arcade_prueba_modelo.log](arcade_prueba_modelo.log).

## Capturas con ventana, abiertas y revisadas

- [arcade_1.png](arcade_1.png): búsqueda y pictograma inicial; `--espera=2.5`.
- [arcade_2.png](arcade_2.png): Luna desenfocada y aguja de enfoque; `--espera=5.3`.
- [arcade_3.png](arcade_3.png): registro de la luz cenicienta y trayectoria de la luz; `--espera=18`.

Se obtuvieron con `python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=telescopio --auto --captura=<ruta absoluta> --espera=<s>`. Los tres ejecutores finalizaron con `errores=0`; sus salidas están en `arcade_captura_1.log`, `arcade_captura_2.log` y `arcade_captura_3.log`.

Limitaciones: las victorias rápidas duran menos que el tiempo máximo de sesión (el contrato del piloto exige menos de 40 s de juego). No se ha hecho una sesión con una persona ni una medición de rendimiento en Intel HD 620. El entorno emite errores al abrir `user://logs` y leer certificados, y algunas corridas avisan de recursos retenidos al salir; las pruebas funcionales no registran fallos ni errores de guion. No se modificó el núcleo para esos avisos. Los recursos y notas de la versión anterior se conservaron sin usarlos.
