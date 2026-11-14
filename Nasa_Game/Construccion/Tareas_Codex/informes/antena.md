Implementado `antena`, sin editar otras carpetas.

Archivos escritos: `antena.gd`, `minijuego.json` y `prueba_modelo.gd` en [antena](</C:/Users/guill/Desktop/Juego 2d-hd/juego/minijuegos/antena/>). Dejé logs, 2 capturas revisadas e informe en [NOTA.md](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/antena/NOTA.md>).

- Modelo proporcional: retardo de **0,25 s**, respuesta del motor de **0,12 s**.
- Victoria: señal **>70 % durante ≥80 %** del paso.
- Pasos de **10 / 8,5 / 7 s**; viento en dificultades 2 y 3.
- Máximo **3 pruebas y 180 s**. Piloto con lógica real; fallo nominal en unos **32 s**.

Prueba obligatoria: **13 comprobaciones, 0 fallos**. Adicional: **33 comprobaciones, 0 fallos**. Sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Con ganancia 3,0 se obtiene **94,0 / 92,5 / 83,8 %** de tiempo útil.

Pendiente: valoración humana del ritmo. El entorno emite avisos de logs y certificados de Windows, sin impedir las pruebas.