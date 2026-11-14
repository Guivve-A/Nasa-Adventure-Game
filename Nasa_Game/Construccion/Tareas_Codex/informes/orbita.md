Implementado `orbita`, con teclado, ratón y trazo del intento anterior.

Archivos creados: `orbita.gd`, `minijuego.json` y `prueba_modelo.gd`. Dejé [informe, registros y captura](</C:/Users/guill/Desktop/Juego 2d-hd/Nasa_Game/Construccion/Minijuegos/orbita/NOTA.md>) en la carpeta de evidencia.

- Modelo: μ = 398 600 km³/s², radio 6 371 km, integración Verlet cada 2 s, tiempo ×300.
- Alturas verificadas: 627 km en niveles 1–2; 654 km en nivel 3.
- Velocidades calculadas: **7,547127** y **7,532610 km/s**.
- Victoria: 1 vuelta y diferencia de alturas **<150 / <80 / <40 km**.
- Corte didáctico de caída: 120 km. Vuelo máximo: 32 s; sesión: 180 s.

Prueba obligatoria: **13 comprobaciones, 0 fallos**, sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Piloto: victorias en 20,528 y 20,148 s; caída en 4,637 s. Pruebas adicionales: **14 comprobaciones, 0 fallos**. Captura revisada en Intel HD 620.

Pendiente: medir fps sostenidos y completar una sesión humana. El informe registra los avisos del entorno sobre logs/certificados y 4 objetos sin liberar al cerrar el ensayo auxiliar.