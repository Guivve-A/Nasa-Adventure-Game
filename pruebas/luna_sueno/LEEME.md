# Luna del sueño: prueba de rendimiento

> **SIN VALIDAR. NO ES BASE DE ARTE NI DE ESCENARIO (2026-11-12).** Este prototipo se construyó antes de que Guillermo validara el concepto y el estilo de la Luna, y eso rompe la regla del proyecto. Se queda solo como medición técnica: la HD 620 sostiene 63 fps con un terreno de 450 m. Su aspecto (terreno, luz, piezas, Tierra) no vale como dirección de arte. No se sigue trabajando aquí hasta que Guillermo valide el concepto y la hoja de referencia de la Luna.

> Etapa 7 del [Plan de auditoría](../../Nasa_Game/Auditoria/Plan%20de%20auditoria.md), carril C5. Es una **prueba técnica, no el nivel final**: mide si la HD 620 aguanta un terreno lunar grande con la cámara del sendero. No hay arte aprobado de la Luna (no existe hoja de referencia ni paleta lunar en la biblia), así que todo es volumen gris por script. 0 créditos de Higgsfield.

## Cómo abrirla

- Doble clic en `abrir_escena.cmd`.
- Teclas: flechas mueven, rueda aleja o acerca, `1` y `2` encuadre (21 % o 12,5 %), `C` vista del cielo, `F12` captura, `Esc` sale.
- Captura o medición, siempre con el envoltorio:

```
python -I herramientas/godot_captura.py pruebas/luna_sueno -- --captura=<png>
python -I herramientas/godot_captura.py pruebas/luna_sueno -- --medir=6
```

- Otros argumentos: `--encuadre=21|12`, `--zoom=<f>`, `--objetivo=x,z`, `--vista=juego|cielo`, `--sin_lod`, `--sin_rocas`, `--sin_inclinacion` y `--mapa=<png>` (guarda el heightmap).

## Qué contiene

| Elemento | Cifras | Archivo |
|---|---|---|
| Terreno | 450 × 450 m; heightmap de 512 × 512 celdas (0,88 m) generado al arrancar; 717 cráteres de 0,6 a 42 m de radio; relieve de −7,6 a +2,9 m; sitio llano (radio de 7 a 16 m) en el origen | `terreno.gd` |
| Niveles de detalle | 8 × 8 bloques de 56 m, 4 niveles (1, 2, 4 y 8 celdas por cuadro) que cambian a 70, 140 y 240 m; faldón de 1,5 m contra las grietas. Todo al detalle máximo serían 589 824 triángulos | `terreno.gd` |
| Anillo de 75 m | El terreno cubre ±225 m: el anillo de 75 m (R3) cabe 3 veces de ancho | — |
| Cráter análogo a Little West | 33 m de diámetro, a 62 m al este del sitio | `terreno.gd` |
| Etapa de descenso | Genérica, 456 triángulos: cuerpo octogonal de 4,2 m (paneles dorados y grises), tobera, 4 patas con zapatas a 9,2 m entre opuestas, unos 3 m de alto. **Sin insignias, banderas, textos ni logotipos** | `piezas.gd` |
| Rocas | 2 000, en 3 formas de 20 caras y 152 MultiMesh (uno por bloque y forma). Tamaños en ley de potencia: mediana de 0,17 m, máximo de 1,4 m. 50 % a menos de 40 m del sitio, 15 % entre 40 y 90 m y 35 % en el borde de los cráteres | `escena.gd` |
| Tierra | Esfera de 1,9° de diámetro aparente, a 66° de altura hacia el oeste (azimut 268°). La ilumina el sol de la escena: sale 62 % iluminada. Continentes inventados con ruido | `shaders/tierra.gdshader` |
| Sol | Rasante: 10° de altura desde el este (azimut 95°). Sombras de 2 cortes, 4096 px | `escena.gd` |
| Cámara | La del sendero: 48° de inclinación, 40° de campo, cizalla 2.5D de 0,45 | `escena.gd` |
| Marcador de escala | Poste de 1,05 m medido (5 franjas de 0,21 m) junto a la zapata sureste | `piezas.gd` |
| Gravedad | `physics/3d/default_gravity = 1.624` (dato L6 de la Fase 2; el encargo decía 1,62) | `project.godot` |
| Shaders | `facetado.gdshader` y `comun.gdshaderinc` copiados del sendero; `regolito.gdshader` es el facetado con la normal plana por derivadas, para que el terreno vaya indexado | `shaders/` |

## Rendimiento (HD 620, Mobile, 1280 × 720, sin vsync, `--medir=6`)

Antes de cada corrida se revisó `tasklist`: **no corrían Blender ni otro Godot** en ninguna. Hubo dos tandas:

- **Tanda A (equipo ocupado):** corría `limpiar_textura_D.py` de otro flujo (Python, hasta 2,4 GB de RAM y carga de CPU de 65 a 99 %).
- **Tanda B (la que vale):** se esperó a que terminara. La 1.ª corrida arrancó sin ningún Python; el otro flujo volvió a lanzar `limpiar_textura_D.py` a las 13:00, así que las corridas 2 a 5 de la tanda B lo tuvieron de fondo. Las cifras de ambas tandas difieren en menos de 3 fps.

| Vista | fps medio | ms medio | ms p95 | Primitivas | Llamadas | Tanda A (fps / p95) |
|---|---|---|---|---|---|---|
| **Juego, encuadre 21 % (por defecto)** | **63,0** | 15,87 | **18,39** | 162 640 | 52 | 63,0 / 19,17 |
| Juego, 21 %, repetición | 64,6 | 15,47 | 17,53 | 162 640 | 52 | — |
| Juego, encuadre 12,5 % | 65,6 | 15,25 | 18,64 | 156 520 | 52 | 64,7 / 17,92 |
| Juego sin rocas | 66,0 | 15,15 | 17,25 | 103 280 | 18 | 65,2 / 18,54 |
| Alejada ×6 (lander y Little West) | — | — | — | 136 408 | 81 | 67,3 / 18,10 |
| Alejada ×20 (unos 120 m de suelo) | 69,3 | 14,43 | 16,79 | 115 336 | 196 | 68,2 / 17,74 |
| Alejada ×20 **sin niveles de detalle** | 49,2 | 20,34 | 23,45 | 590 728 | 196 | 47,0 / 24,99 |
| Cielo (vista baja hacia la Tierra) | 78,7 | 12,71 | 15,01 | 221 204 | 168 | 75,9 / 15,86 |

Lectura:

- La vista de juego da **63 fps de media y 18,4 ms de p95**. Referencia: el sendero dio 48,3 fps a 720p.
- Los niveles de detalle valen 20 fps en la vista lejana: bajan de 590 728 a 115 336 primitivas.
- Las 2 000 rocas cuestan de 1 a 3 fps y 34 llamadas.
- El límite es el relleno de píxeles (el shader de regolito en toda la pantalla y el filtro de sombras), no los triángulos: la vista del cielo, con medio cuadro negro, dibuja más primitivas y va más rápido.
- Arranque: generar el heightmap tarda de 1,6 a 2,5 s y montar las mallas de 0,9 a 1,5 s.

## Capturas

| | |
|---|---|
| ![Juego 21 %](capturas/01_juego_21.png) | ![Juego 12,5 %](capturas/02_juego_12.png) |
| `01_juego_21.png`: cámara de juego, marcador de 1,05 m al 21 % | `02_juego_12.png`: encuadre 12,5 % |
| ![Alejada ×6](capturas/03_panorama_zoom6.png) | ![Alejada ×20](capturas/05_panorama_zoom20.png) |
| `03_panorama_zoom6.png`: etapa de descenso y Little West | `05_panorama_zoom20.png`: campo de cráteres |
| ![Cielo](capturas/04_cielo_tierra.png) | ![Tierra ampliada](capturas/04b_tierra_ampliada.png) |
| `04_cielo_tierra.png`: la Tierra a 66° sobre el sitio | `04b_tierra_ampliada.png`: recorte ×8, fase del 62 % |

`capturas/heightmap_513.png`: el heightmap en gris (negro −7,63 m, blanco +2,91 m).

## Hallazgos y pendientes

1. **Error corregido:** con margen de histéresis en `visibility_range` y sin fundido, Godot dejaba sin dibujar los bloques cuyo centro caía en la banda de ±6 m de un cambio de nivel (faltaban bloques enteros en la vista alejada). Se quitó el margen.
2. **La Tierra no se ve con la cámara de juego.** A 66° de altura queda fuera de una cámara que mira hacia abajo a 48°. Para la foto «vista con el Apolo» hace falta otra cámara o un reflejo; es parte de la decisión B4.
3. **Choque de datos:** la Fase 2 dice que la Tierra está casi llena (87 %). Con sol rasante (10°) y la Tierra a 66°, la fracción máxima posible es de un 70 %; con el sol de esta prueba sale 62 %. Una Tierra al 87 % exige que el Sol esté bajo el horizonte del sitio (noche lunar). Hay que elegir: sol rasante o Tierra casi llena.
4. **Luz lunar sin dirección de arte.** Con sol a 10°, cada faceta que se inclina más de 10° hacia el lado contrario queda en sombra: aparecen triángulos oscuros sueltos en los cráteres pequeños. Es físicamente correcto, pero hay que decidir el estilo con la paleta lunar.
5. Las sombras de la etapa de descenso se ven escalonadas a 21 %: 4096 px repartidos en 40 m. Se puede subir la calidad del filtro o bajar la distancia.
6. Optimización posible: bloques más pequeños (16 × 16) acercarían el nivel 0 a lo que ve la cámara; hoy, sin rocas, el cuadro dibuja 103 280 primitivas (con la pasada de sombras) para una zona de pocos metros.
7. El horizonte de la vista del cielo es el borde del terreno (225 m); la Luna real tiene unos 2,4 km de horizonte. Para una vista baja haría falta un anillo lejano.
8. Datos de memoria, sin verificar en la bóveda: el tamaño y la distancia de Little West, y el sol de unos 10° del alunizaje del Apolo 11.
