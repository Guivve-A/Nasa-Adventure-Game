Agrupé **227 recursos en 18 MultiMesh**, conservando materiales, sombras, transformaciones y apoyos. Los nodos originales quedan ocultos para mantener referencias y cajas. [Código modificado](<C:/Users/guill/Desktop/Juego 2d-hd/pruebas/escena_exploracion/escena.gd:136>)

Mediciones a 720p con `--medir=6`.

| Encuadre | Llamadas antes → después | FPS antes → después | p95 ms antes → después |
|---|---:|---:|---:|
| 21 | 252 → 58 | 57,6 → 54,5 | 19,55 → 20,27 |
| 12 | 420 → 64 | 54,5 → 56,3 | 20,45 → 20,01 |

**Hay una regresión de rendimiento en el encuadre 21**, acompañada de más primitivas procesadas.

Con tiempo y pose fijados, la diferencia media RGB fue **0,001293 y 0,000009 sobre 255**. Verifiqué viento, inclinación, materiales, transformaciones y controles, con cero fallos funcionales.

Generé **18 capturas**. El informe incluye las comparaciones antes/después, diferencias amplificadas, líneas `MEDIDA` y comandos reproducibles. [Informe y capturas](<C:/Users/guill/Desktop/Juego 2d-hd/pruebas/escena_exploracion/capturas/multimesh/informe.md>)

Quedaron sin comprobar los GLB ausentes `COL-01_script`, `COL-02` y `FX-01`. Godot también registró errores del entorno de certificados y caché, detallados en el informe.