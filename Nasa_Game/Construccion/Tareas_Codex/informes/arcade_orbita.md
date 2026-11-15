Órbita rehecho a **pantalla completa**, con gravedad 2D, inercia, combustible, anillos y efectos de píxeles.
La misión exige cambiar de altura entre enlaces y terminar con una órbita estable sin motor.

**Controles:** E/Espacio/W/↑ impulsa; S/↓ frena; soltar conserva la inercia.

| Nivel | Anillos | Margen anillo | Motor | Tiempo límite | Variación final |
|---|---:|---:|---:|---:|---:|
| 1 | 6 | ±170 km | 28 s | 105 s | ≤140 km |
| 2 | 7 | ±120 km | 25 s | 110 s | ≤90 km |
| 3 | 8 | ±85 km | 23 s | 115 s | ≤55 km |

Se gana completando los anillos y manteniendo cuatro segundos sin motor, centrado en 640,5 km con margen de ±70/45/27,5 km. Se pierde por tres anillos fallados, bajar a 120 km, abandonar el campo o agotar el tiempo.

Pruebas obligatorias aprobadas:

```text
Minijuego: 13 PRUEBA_OK; 0 PRUEBA_FALLO
[godot: ok; 9 s; lineas=27; errores=0]

Manos: PRUEBAS hechas=17 fallos=0
[godot: ok; 177 s; lineas=29; errores=0]
```

Capturas revisadas: [arcade_1](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/orbita/arcade_1.png>), [arcade_2](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/orbita/arcade_2.png>), [arcade_3](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/orbita/arcade_3.png>).

[Informe completo](<C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/orbita/NOTA.md>). Pendiente: valoración humana de dificultad y escucha del audio. Nivel 2 verificado mediante el modelo; manos cubre niveles 1 y 3.