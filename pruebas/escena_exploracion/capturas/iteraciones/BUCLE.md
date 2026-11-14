# Bucle de ajuste de la escena al ancla

Pedido de Guillermo (2026-11-12): «/loop Itera hasta que el escenario se vea como se requirió en las referencias». También pidió «texturas de 2D-HD o 2.5D»: un acabado pintado, aunque las mallas sean 3D.

**Ancla:** `Nasa_Game/Fase_1_Arte/Exploracion/Lote_02/L02_exploracion_camara_alta.png` (D-013).

**Criterio de parada:** que Guillermo diga que se ve como la referencia. El ΔE solo orienta: mide masas de color por bloques de 40 px, no la riqueza de la ilustración.

## Cómo se itera (cada vuelta)

1. Cambiar el generador, los shaders o la luz.
2. Regenerar: `python -I herramientas/mallas/escena_v1.py`. Si cambió el árbol, antes `python -I herramientas/mallas/veg02_flamboyan.py`.
3. Capturar: `python -I herramientas/godot_captura.py pruebas/escena_exploracion -- --encuadre=21 --captura=<ruta absoluta>/itNN_escena.png`. El envoltorio cierra Godot si se cuelga al salir, algo que pasa a veces en la HD 620.
4. Medir: `python -I herramientas/comparar_ancla.py <ancla> itNN_escena.png itNN_lamina.png --etiqueta "..." >> iteraciones.jsonl`.
5. Mirar la lámina y `python -I herramientas/color_zonas.py <ancla> <captura>`, y decidir la siguiente corrección.

## Herramientas nuevas

- `herramientas/camara_ancla.py`: la cámara de la escena en Python. `al_suelo(u, v, y)` da el punto del mundo que el ancla pinta en el píxel (u, v). Todo el trazado de `escena_v1.py` sale de medidas en el ancla con esta función.
- `herramientas/comparar_ancla.py`: ΔE por bloques, rejilla 3×3 y lámina con el mapa de diferencias.
- `herramientas/color_zonas.py`: color medio por zona del ancla contra la captura.
- `herramientas/godot_captura.py`: captura o medición sin cuelgues.

## Registro

| It. | Cambio | ΔE medio | % bloques < 15 | Rejilla 3×3 (arriba-izq. … abajo-der.) |
|---|---|---:|---:|---|
| 00 | Base: protagonista v2, acabado 2.5D del personaje, recolectables generados | 27,96 | 20,0 | 33 35 27 / 25 20 33 / 28 24 28 |
| 01 | Todo el trazado desde píxeles del ancla (sendero, arroyo, puente, rocas, plantas, antena, panel, plaza, personajes); flamboyán al 62 % de alto (copa en paraguas, entra en cuadro) | 23,66 | 24,7 | 25 25 27 / 27 18 24 / 29 20 19 |
| 02 | Luz pintada del entorno (caras de espaldas con 50 %, sombras proyectadas con 20 %), sombra moteada, rocas al 62 % | 21,65 | 30,9 | 22 24 27 / 19 18 23 / 23 20 19 |
| 03 | Sol ffd2a0, ambiente malva, más flores, mosaico, tierra y hierba recoloreadas | 22,53 | 28,6 | se pasó de cálido: L 53,8, croma 42,5 |
| 04 | Luz intermedia (sol ffdcb4 ×1,15; ambiente 77849a ×0,62; sombras 0,55/0,7), plaza a −0,15 | 20,90 | 33,3 | 25 24 22 / 17 16 24 / 18 20 21 |
| 05 | Motas en estrella, escalinata TER-11, antena por script por defecto | 20,92 | 33,9 | |
| 06 | Escalinata a ras bajo la baranda (dos módulos, muro cortado), motas solo en el suelo | 20,74 | 34,2 | 25 24 23 / 17 17 22 / 18 20 21 |
| 07 | Flores más rojas con estambres chicos, destellos dorados en el agua | 20,62 | 34,7 | 24 23 22 / 17 17 22 / 18 20 21 |
| 08 | Arroyo angosto (cinta 1,05 m, cauce 0,6 m) con saltos de 28 cm, espuma al pie de las cascadas, rocas malva cálido, piedrecillas beige | 20,77 | 34,4 | 24 23 23 / 17 16 24 / 18 20 21 |
| 09 | Agua turquesa: la máscara de espuma (0,35 en toda el agua) la dejaba lechosa; cascadas con chorros; cantos malva con musgo | 20,83 | 34,0 | 24 23 24 / 18 16 24 / 18 20 21 |

| 10 | Puente al 0,7; rocas, helechos y flores en la orilla; 260 mechones (antes 170); suelo menos amarillo; contraste 1,08 y saturación 0,92 | 20,80 | 34,4 | 24 22 24 / 18 17 24 / 18 20 20 |
| 11 | Panel con líneas azul grisáceo y marco oxidado; antena girada 150° (boca arriba a la derecha); piedrecillas al 0,5 | 20,50 | 35,1 | 24 22 24 / 18 16 22 / 18 20 20 |
| 12 | Pinceladas 2D-HD por shader (`pinceladas` 0,7): casi no se notan | 20,63 | 34,2 | |
| 13 | Sendero al ancho medido en el ancla (1,5 m cerca, 1,05 a 1,2 m lejos), pétalos en la hierba, motas más arriba | 20,19 | 36,6 | 24 22 24 / 18 14 22 / 18 20 20 |
| 14 | **Rendimiento:** las motas por píxel bajaban la escena de 55 a 27 fps. Ahora son de una celda, con salida temprana | 20,20 | 36,1 | 38 fps |
| 15 | Motas y pinceladas de la hierba por vértice: **48 fps** (encuadre 21) y **44 fps** (encuadre 12) | 20,17 | 36,8 | |
| 16 | Saturación 0,86 | 19,45 | 39,2 | 22 21 23 / 18 14 21 / 19 19 18 |
| 17 | Saturación 0,80 y contraste 1,12: L, croma y contraste ya igualan al ancla (48,6 / 35,4 / 17,0 contra 49,1 / 34,2 / 17,5) | **19,39** | 39,1 | 22 20 23 / 18 15 21 / 19 19 18 |

| 18 | Lóbulo de copa delante del tronco para cubrir la esquina superior izquierda: esa zona subió de 21,7 a 29,3. **Descartado** | 20,36 | 36,3 | 29 20 23 / … |
| 19 | Estado final (igual a la vuelta 17) | **19,36** | 38,5 | |

**Bucle cerrado el 2026-11-12, tras 19 vueltas.** El color global ya iguala al ancla y la última prueba empeoró. Para seguir hace falta el veredicto de Guillermo o riqueza de ilustración (texturas pintadas). Guillermo pidió pasar después al bucle de la protagonista: que se parezca al menos en un 80 % al reference sheet.

Láminas de progreso: `progreso_it00_it07.png` y `progreso_it00_it17.png`. Las iteraciones 08 y 09 mejoran el arroyo a la vista, aunque el ΔE no lo note (es una zona chica).

**Rendimiento (vuelta 15):** 48,3 fps en el encuadre 21 y 44,2 en el 12, con 307 000 triángulos (antes 238 000) y 68 llamadas de dibujo. La escena base estaba en 57,6 fps; la diferencia sale de los mechones y plantas nuevos. Si hace falta, bajar los mechones de 260 a 200.

## Pendiente, por impacto (siguiente vuelta empieza arriba)

1. **Veredicto de Guillermo** sobre `progreso_it00_it17.png`: el ΔE se estanca en unos 19,4, porque el color global ya coincide. Lo que falta es riqueza de ilustración.
2. **Textura pintada (2D-HD) del suelo:** las pinceladas por shader casi no se ven. Lo que más acercaría el suelo y la hierba al ancla son texturas pintadas en Higgsfield, pero requieren aprobar créditos: quedan 2,00 de la partida de la escena, y una textura en calidad alta cuesta 1,5.
3. **Copa:** en el ancla, la esquina superior izquierda es casi toda copa; aquí asoman helechos. Agregar racimos hacia −X y +Z (`veg02_flamboyan.py`, `racimos`).
4. **Antena:** el plato está más parado que en el ancla, que lo tiene casi acostado. Haría falta inclinarlo en el modelo, porque el layout solo gira en Y.
5. **Gato:** visto de espaldas es un bulto beige; en el ancla se ve naranja y blanco, con el collar cian.
6. **Hierba en sombra:** más verde y con motas más densas, como en el ancla.
