# La escalinata del tiempo

La protagonista sube una escalinata de mosaico: busca el pictograma pendiente y aterriza sobre su placa para revelar el año. Cocos rodantes e iguanas obligan a moverse y saltar; pisar otra época consume una vida.

Campo dibujado con `_draw()`, mapas de caracteres y tipografía de píxeles: 280 × 130, escalado ×4. Incluye partículas, destellos, sacudida, parpadeo de inmunidad y sonidos del proyecto.

**Controles:** flechas o WASD para moverse; E o Espacio para saltar; Esc para salir. El salto dura 0,75 s. Las teclas responden con aceleración y frenado breves.

**Victoria:** activar los nueve hitos en orden, aterrizando en sus placas. **Derrota:** perder las tres vidas o agotar el tiempo. Cada choque o placa ajena quita una vida; después hay 2 s de inmunidad. Caminar sobre una placa no descubre su fecha.

| Dificultad | Tiempo máximo | Coco / iguana (píxeles lógicos/s) | Aparición de peligro | Margen de aterrizaje X / Y |
|---|---:|---:|---:|---:|
| 1 | 100 s | 24 / 28 | cada 3,5 s | ±16 / ±9 px |
| 2 | 90 s | 32 / 39 | cada 2,6 s | ±13 / ±9 px |
| 3 | 80 s | 42 / 51 | cada 1,9 s | ±10 / ±9 px |

El primer peligro aparece a los 2,7 s de movimiento efectivo; las celebraciones detienen brevemente a los animales. La dificultad 1 además marca el borde de la placa pendiente. Los límites permiten partidas de 80–100 s; una ruta óptima puede acabar antes de 60 s. Con teclas simuladas se ganaron los niveles en 36,40 / 36,40 / 36,75 s, con 3 / 3 / 2 vidas restantes.

**Datos:** se leen las fichas de `juego/datos/datos_espaciales.json` durante la preparación. Años comprobados: 1873, 1957, 1969, 1975, 1981, 1982, 2007, 2013 y 2023. El año del disco procede de su fuente; el de la entrega se distingue del cierre mencionado en la misma ficha. La estación Quito y el disco del Apolo 11 son placas independientes; no se atribuye apoyo al Apolo 11 a la estación.

**Pruebas obligatorias:**

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:linea_tiempo --ritmo=8
13 PRUEBA_OK, ningún PRUEBA_FALLO
[godot: ok; 16 s; lineas=30; errores=0]

python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/linea_tiempo/prueba_manos.gd --ritmo=1
PRUEBAS hechas=24 fallos=0
[godot: ok; 113 s; lineas=44; errores=0]
```

La prueba de manos abre el anfitrión en otra corrutina, comienza con Intro, gana los tres niveles exclusivamente mediante `InputEventKey`, cierra con Intro y comprueba la victoria devuelta, el anfitrión cerrado y el árbol sin pausa. Alterna flechas/E y WASD/Espacio. No llama al piloto ni modifica el estado del juego.

Regresión adicional: `prueba_linea_tiempo.gd`, **24 comprobaciones, 0 fallos**. Comprueba años, fechas ocultas, caminar frente a aterrizar, evasión de cocos, agotamiento del tiempo y pilotos de victoria/derrota en los tres niveles en menos de 40 s. Logs: `arcade_contrato.log`, `arcade_manos.log` y `arcade_modelo.log`.

**Capturas con ventana:**

- `Nasa_Game/Construccion/Minijuegos/linea_tiempo/arcade_1.png` — espera de 4 s.
- `Nasa_Game/Construccion/Minijuegos/linea_tiempo/arcade_2.png` — espera de 16 s.
- `Nasa_Game/Construccion/Minijuegos/linea_tiempo/arcade_3.png` — espera de 28 s.

**Pendiente o sin verificar:** valoración humana del ritmo y medición de FPS. La ruta óptima de unos 36 s queda por debajo del objetivo nominal de 60–120 s; el piloto cumple su contrato de menos de 40 s sin cambiar las reglas. Godot imprime avisos de acceso a `user://logs`, certificados de Windows y recursos al cerrar, también observados en otras pruebas del proyecto; no hay `SCRIPT ERROR` ni fallos de comprobación. No se modificó el núcleo para silenciarlos.
