Implementado `seguidor` en ambos modos, con teclado y ratón, comparación de curvas y bloqueo de cambios múltiples.

- Archivos: `seguidor.gd`, `minijuego.json` y `prueba_seguidor.gd`.
- Modelo: paso fijo de **1/240 s**, inercia **1**, rozamiento **0,6**.
- Victoria: franja **±4 %**, asentamiento **≤2,5 s** (**3,8 s** en rampa), sobrepaso **≤5 %** y error final **≤1,5 %**.
- Cada prueba dura **5 s**; máximo **6/5/4** según dificultad. Piloto completo en menos de **40 s**.
- Prueba oficial: **13 comprobaciones, 0 fallos**. Adicional: **19, 0 fallos**. Sin `PRUEBA_FALLO` ni `SCRIPT ERROR`.
- Capturas revisadas y evidencia guardada en [NOTA.md](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/seguidor/NOTA.md>).

Sin pendientes funcionales del minijuego. El entorno emitió avisos de permisos para logs y certificados; ambas pruebas finalizaron con código **0**.