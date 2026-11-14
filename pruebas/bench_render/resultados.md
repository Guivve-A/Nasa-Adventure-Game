# Resultados del benchmark de renderizado

Fecha UTC: 2026-11-12T06:49:34.047395+00:00. Python: 3.13.15.

Forward+ y Mobile: Vulkan. Compatibility: OpenGL 3. Calentamiento: 3 s.
FPS 1 %: inversa del tiempo medio del 1 % de cuadros mas lentos (redondeo hacia arriba).
Tiempos de cuadro: reloj real de CPU entre callbacks, no tiempo exclusivo de GPU.
Draw calls y primitivas: media por cuadro. Memoria: maximo reportado por el motor, en MiB.
Un contador 0 puede indicar informacion no disponible; la HD 620 usa memoria compartida.

| Metodo solicitado | Escena | Resolucion | Estado | FPS medio | FPS 1 % | Cuadro medio ms | Cuadro max ms | Draw calls | Primitivas | Memoria MiB | Metodo efectivo | Controlador | Adaptador | API | Error |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| forward_plus | base | 1280x720 | ok | 68.09 | 54.81 | 14.686 | 19.037 | 305.3 | 93321.5 | 117.42 | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| forward_plus | base | 1920x1080 | error | — | — | — | — | — | — | — | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| forward_plus | hierba | 1280x720 | ok | 34.46 | 29.91 | 29.019 | 33.789 | 308.5 | 573451.8 | 120.75 | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| forward_plus | hierba | 1920x1080 | error | — | — | — | — | — | — | — | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| forward_plus | sprites | 1280x720 | ok | 58.38 | 32.77 | 17.128 | 49.718 | 706.6 | 94205.3 | 117.54 | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| forward_plus | sprites | 1920x1080 | error | — | — | — | — | — | — | — | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| forward_plus | sdfgi | 1280x720 | ok | 19.74 | 8.68 | 50.666 | 118.959 | 305.6 | 93467.8 | 480.76 | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| forward_plus | sdfgi | 1920x1080 | error | — | — | — | — | — | — | — | forward_plus | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| mobile | base | 1280x720 | ok | 90.17 | 71.45 | 11.090 | 14.396 | 296.8 | 93417.5 | 82.11 | mobile | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| mobile | base | 1920x1080 | error | — | — | — | — | — | — | — | mobile | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| mobile | hierba | 1280x720 | ok | 42.53 | 35.68 | 23.511 | 28.706 | 298.8 | 573444.3 | 85.45 | mobile | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| mobile | hierba | 1920x1080 | error | — | — | — | — | — | — | — | mobile | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| mobile | sprites | 1280x720 | ok | 74.85 | 56.52 | 13.361 | 18.566 | 679.4 | 94234.1 | 82.24 | mobile | vulkan | Intel(R) HD Graphics 620 | 1.3.215 |  |
| mobile | sprites | 1920x1080 | error | — | — | — | — | — | — | — | mobile | vulkan | Intel(R) HD Graphics 620 | 1.3.215 | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| gl_compatibility | base | 1280x720 | ok | 73.35 | 48.50 | 13.634 | 21.020 | 305.6 | 93496.6 | 15.36 | gl_compatibility | opengl3_angle | ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2140) | OpenGL ES 3.0 (ANGLE 2.1.1 git hash: aaebda1c5a40) |  |
| gl_compatibility | base | 1920x1080 | error | — | — | — | — | — | — | — | gl_compatibility | opengl3_angle | ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2140) | OpenGL ES 3.0 (ANGLE 2.1.1 git hash: aaebda1c5a40) | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| gl_compatibility | hierba | 1280x720 | ok | 41.71 | 27.68 | 23.975 | 37.163 | 308.5 | 573452.2 | 17.19 | gl_compatibility | opengl3_angle | ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2140) | OpenGL ES 3.0 (ANGLE 2.1.1 git hash: aaebda1c5a40) |  |
| gl_compatibility | hierba | 1920x1080 | error | — | — | — | — | — | — | — | gl_compatibility | opengl3_angle | ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2140) | OpenGL ES 3.0 (ANGLE 2.1.1 git hash: aaebda1c5a40) | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |
| gl_compatibility | sprites | 1280x720 | ok | 40.50 | 24.10 | 24.693 | 44.022 | 707.0 | 94325.1 | 15.42 | gl_compatibility | opengl3_angle | ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2140) | OpenGL ES 3.0 (ANGLE 2.1.1 git hash: aaebda1c5a40) |  |
| gl_compatibility | sprites | 1920x1080 | error | — | — | — | — | — | — | — | gl_compatibility | opengl3_angle | ANGLE (Intel, Intel(R) HD Graphics 620 (0x00005916) Direct3D11 vs_5_0 ps_5_0, D3D11-31.0.101.2140) | OpenGL ES 3.0 (ANGLE 2.1.1 git hash: aaebda1c5a40) | La resolucion efectiva difiere de la solicitada o cambio durante la corrida. |

JSON individuales y logs: `corridas\run_kz4ist6c`.
