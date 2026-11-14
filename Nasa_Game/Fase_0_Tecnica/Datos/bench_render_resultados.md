---
tipo: datos
fase: 0
fecha: 2026-11-12
---

# Rendimiento de los renderizadores de Godot 4.7.2 en la Intel HD 620

Medido con `pruebas/bench_render/` (escrito por Codex, revisado y ejecutado por Claude). Cada corrida calienta 3 s y mide de 10 a 12 s con vsync desactivado. Los JSON de cada corrida están en `pruebas/bench_render/corridas/`.

- **base:** 150 mallas con sombreado toon, suelo con textura, una luz direccional con sombra.
- **hierba:** la base más 40 000 briznas en un `MultiMesh` con viento.
- **sprites:** la base más 200 `Sprite3D` en billboard, con recorte alfa y sombra.
- **sdfgi:** la base con SDFGI, SSAO y glow.

## Corrida principal

| Método | Controlador | Escena | Resolución | FPS medio | FPS 1 % | Cuadro máx. ms | Llamadas | Primitivas | Memoria MiB |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| forward_plus | vulkan | base | 1280×720 | 68,1 | 54,8 | 19 | 305 | 93 321 | 117 |
| forward_plus | vulkan | base | 1920×1066 | 38,6 | 32,4 | 31 | 305 | 93 429 | 149 |
| forward_plus | vulkan | hierba | 1280×720 | 34,5 | 29,9 | 34 | 309 | 573 452 | 121 |
| forward_plus | vulkan | hierba | 1920×1066 | 22,9 | 19,1 | 55 | 308 | 573 429 | 152 |
| forward_plus | vulkan | sdfgi | 1280×720 | 19,7 | 8,7 | 119 | 306 | 93 468 | 481 |
| forward_plus | vulkan | sdfgi | 1920×1066 | 12,9 | 7,4 | 135 | 306 | 93 437 | 556 |
| forward_plus | vulkan | sprites | 1280×720 | 58,4 | 32,8 | 50 | 707 | 94 205 | 118 |
| forward_plus | vulkan | sprites | 1920×1066 | 35,5 | 27,8 | 38 | 707 | 94 228 | 149 |
| gl_compatibility | opengl3_angle | base | 1280×720 | 73,3 | 48,5 | 21 | 306 | 93 497 | 15 |
| gl_compatibility | opengl3_angle | base | 1920×1066 | 61,5 | 36,4 | 30 | 306 | 93 476 | 24 |
| gl_compatibility | opengl3_angle | hierba | 1280×720 | 41,7 | 27,7 | 37 | 309 | 573 452 | 17 |
| gl_compatibility | opengl3_angle | hierba | 1920×1066 | 30,0 | 21,7 | 48 | 308 | 573 413 | 26 |
| gl_compatibility | opengl3_angle | sprites | 1280×720 | 40,5 | 24,1 | 44 | 707 | 94 325 | 15 |
| gl_compatibility | opengl3_angle | sprites | 1920×1066 | 40,2 | 23,7 | 44 | 707 | 94 204 | 24 |
| mobile | vulkan | base | 1280×720 | 90,2 | 71,5 | 14 | 297 | 93 417 | 82 |
| mobile | vulkan | base | 1920×1066 | 56,4 | 44,5 | 24 | 297 | 93 423 | 97 |
| mobile | vulkan | hierba | 1280×720 | 42,5 | 35,7 | 29 | 299 | 573 444 | 85 |
| mobile | vulkan | hierba | 1920×1066 | 29,9 | 24,9 | 41 | 299 | 573 403 | 100 |
| mobile | vulkan | sprites | 1280×720 | 74,8 | 56,5 | 19 | 679 | 94 234 | 82 |
| mobile | vulkan | sprites | 1920×1066 | 49,7 | 28,3 | 78 | 679 | 94 207 | 97 |

Las corridas de «1920×1066» se pidieron a 1920×1080 en ventana; la ventana no cabe en la pantalla y Godot la recorta.

## Corridas extra: D3D12 y 1080p a pantalla completa

| Método | Controlador | Escena | Resolución | FPS medio | FPS 1 % | Cuadro máx. ms | Llamadas | Primitivas | Memoria MiB |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| mobile | d3d12 | base | 1280×720 | 114,4 | 50,8 | 33 | 297 | 93 515 | 95 |
| mobile | d3d12 | hierba | 1280×720 | 42,9 | 35,7 | 28 | 299 | 573 331 | 99 |
| mobile | d3d12 | sprites | 1280×720 | 98,3 | 60,8 | 18 | 679 | 94 089 | 145 |
| mobile | d3d12 | hierba | 1920×1080 | 31,4 | 28,6 | 36 | 299 | 573 281 | 114 |
| mobile | vulkan | base | 1920×1080 | 56,6 | 32,6 | 44 | 297 | 93 305 | 97 |
| mobile | vulkan | hierba | 1920×1080 | 32,0 | 28,2 | 36 | 299 | 573 293 | 100 |
| gl_compatibility | opengl3_angle | base | 1920×1080 | 71,3 | 46,1 | 24 | 305 | 93 312 | 24 |
| gl_compatibility | opengl3_angle | hierba | 1920×1080 | 32,1 | 28,5 | 35 | 308 | 573 330 | 26 |
| forward_plus | d3d12 | hierba | 1280×720 | 366,7 | 167,0 | 13 | 310 | 574 447 | 136 |

La última fila es anómala: 367 fps con 574 000 primitivas no es creíble en esta gráfica. No se usa.

## Límites

- Las escenas son sintéticas. No representan el juego.
- Durante la corrida principal había tareas de Codex activas. Una corrida rápida anterior dio cifras casi iguales en Mobile (90,8 / 43,2 / 75,0).
- La primera corrida de Forward+ superó el límite de 90 s, por la compilación de shaders del primer arranque.
- La memoria es la contabilidad del motor, no la memoria dedicada de video.
