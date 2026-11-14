Implementado `telescopio`: buscar, enfocar y señalar los 3 rasgos, con teclado y ratón y la Luna fotográfica original.

Archivos en [telescopio](</C:/Users/guill/Desktop/Juego 2d-hd/juego/minijuegos/telescopio/>): `telescopio.gd`, `minijuego.json`, `prueba_telescopio.gd`, ambos shaders, `datos/luna.json`, ambas texturas y `texturas.json`.

Reglas por dificultad 1/2/3:

- Centrado: ±1,6° / ±1,2° / ±0,8°.
- Enfoque: 62/100, margen ±7 / ±5 / ±3,5.
- Victoria: 3 rasgos reconocidos en orden.
- Límite: 150 s o 5/4/3 revisiones.
- Pilotos ganadores: aproximadamente 8 s mediante la lógica real.

Prueba exigida: **13 comprobaciones, 0 fallos**. Prueba adicional: **21 comprobaciones, 0 fallos**. Sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Capturas revisadas.

Dejé números completos, procedencia, registros y pendientes en [NOTA.md](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/telescopio/NOTA.md>). No queda funcionalidad pendiente; faltan mediciones sostenidas de FPS y verificación de exportación. Los avisos del motor sobre registros, certificados, caché y objetos al salir están documentados.