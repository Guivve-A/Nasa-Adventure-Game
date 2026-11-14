---
tipo: propuesta
fecha: 2026-11-12
origen: idea de Guillermo
estado: validada con una prueba en Godot · espera la aprobación de diseño
fases: 2 (misiones), 5 (niveles) y 7 (interfaz)
---

# Mirador del Faro: la Luna con datos reales de NASA

> Idea de Guillermo (2026-11-12): «una zona donde pueda incrustar data satelital de la NASA, por ejemplo ver desde un telescopio y poder observar la Luna y que nuestra mascota aparezca dando datos, mientras la Luna se observa».

## Veredicto

**Viable, y da para más de lo previsto.** El juego puede mostrar la Luna real del día en que se juega, vista desde Guayaquil, con su fase, su distancia y su inclinación exactas. Los datos y las texturas salen de servicios públicos de NASA que se comprobaron hoy.

| Pregunta | Respuesta | Evidencia |
|---|---|---|
| ¿Hay datos de la Luna para cualquier hora y lugar? | Sí: fase, distancia, tamaño, altura y orientación | Consulta real a JPL Horizons, más abajo |
| ¿Hay imágenes de la Luna para cada hora de 2026? | Sí: 8 760 imágenes y una tabla JSON | NASA SVS 5587 y su API Dial-A-Moon, probada |
| ¿Hay texturas para una Luna 3D detallada? | Sí: mapa de color de LROC y mapa de relieve de LOLA | NASA SVS 4720, «CGI Moon Kit» |
| ¿Se pueden usar en un juego? | Sí, con crédito a NASA y sin sugerir su respaldo | Guía de uso de imágenes de NASA |
| ¿Rinde en el equipo? | Debería: es una esfera con textura | Sin medir todavía |

![[L03_ui_telescopio_luna.png]]

*Maqueta de interfaz del lote 03. La Luna de la maqueta la dibujó la IA; en el juego se usará la textura de NASA. Los números de las fichas son los reales de esta noche.*

## La prueba: la Luna de esta noche desde el Mirador

Consulta a la API de JPL Horizons (versión 1.2, efemérides DE441) para el faro del cerro Santa Ana, el 12 de noviembre de 2026. Script: `herramientas/luna_efemerides.py`. Respuesta guardada en `Propuestas/Datos/`.

| Hora en Guayaquil | Cielo | Altura | Iluminada | Distancia | Tamaño aparente | Borde iluminado |
|---|---|---:|---:|---:|---:|---|
| 18:00 | día | 38,8° | 11,9 % | 401 311 km | 29,8′ | abajo, algo a la derecha |
| 19:00 | crepúsculo | 26,4° | 12,1 % | 402 491 km | 29,7′ | abajo |
| 19:30 | noche | 20,0° | 12,2 % | 403 151 km | 29,6′ | abajo |
| 20:00 | noche | 13,6° | 12,3 % | 403 846 km | 29,6′ | abajo |
| 21:00 | noche | 0,8° | 12,5 % | 405 290 km | 29,5′ | abajo |

**Cruce con una segunda fuente.** Dial-A-Moon (NASA SVS) da, para las 20:00: fase del 12,76 %, edad de 3,75 días y distancia de 405 396 km. Su distancia es desde el centro de la Tierra; la de Horizons, desde el Mirador. La diferencia, 1 550 km, cuadra con el radio terrestre por el seno de la altura de la Luna: 6 371 km × sen 13,6° ≈ 1 498 km.

### Lo que esta noche puede enseñar el juego

- **La Luna «sonriente».** El borde iluminado apunta hacia abajo: de 182° a 206° medidos desde el cenit. Cerca del ecuador, la Luna creciente se ve acostada, como una sonrisa. Es un detalle propio de Guayaquil que el juego puede mostrar con exactitud.
- **La luz cenicienta.** En una creciente tan fina se ve la parte oscura del disco, iluminada por la luz que refleja la Tierra.
- **La distancia cambia según dónde estés.** Desde el Mirador la Luna se alejó casi 4 000 km entre las 18:00 y las 21:00. Casi todo se debe al giro de la Tierra, que aleja el Mirador de la Luna mientras esta se pone.
- **Esta noche está cerca de su distancia máxima:** 405 396 km desde el centro de la Tierra, dentro del rango del apogeo, con 29,6′ de tamaño aparente.

## Fuentes de NASA comprobadas hoy

1. **JPL Horizons API.** Calcula la posición y el aspecto de la Luna para un punto de la Tierra y una hora. Se probó con datos reales.
2. **NASA SVS 5587, «Moon Phase and Libration, 2026».** Publicada el 11-12-2025.
   - Una imagen por hora del año: 8 760 cuadros, hasta 5760×3240.
   - Tabla de datos `mooninfo_2026.json`: fase, diámetro, distancia, ascensión recta y declinación, punto subsolar, punto subterrestre y ángulo de posición.
   - El norte celeste va arriba. La versión con el sur arriba es la 5588.
   - Su API Dial-A-Moon responde por hora; se probó.
3. **NASA SVS 4720, «CGI Moon Kit».** Actualizada el 09-01-2026.
   - Mapas de color de LROC WAC: de 1024×512 a 27360×13680. Por ejemplo, `lroc_color_poles_4k.tif` (4096×2048, 12,5 MB).
   - Mapas de relieve de LOLA, en kilómetros: de `ldem_4.tif` (1440×720, 4,0 MB) a `ldem_64.tif` (23040×11520, 1 012,6 MB).
   - Crédito pedido: «NASA's Scientific Visualization Studio». Aviso de la página: están optimizados para la estética, no para la ciencia.
4. **Guía de uso de imágenes y medios de NASA.**
   - El material de NASA, incluidos los mapas de textura y los polígonos de modelos 3D, en general no tiene derechos de autor en EE. UU. La guía menciona las simulaciones gráficas por computadora entre los usos permitidos.
   - Hay que reconocer a NASA como fuente.
   - El uso comercial no puede sugerir, explícita ni implícitamente, que NASA respalda el producto.
   - La insignia, el logotipo y los identificadores de NASA no son de dominio público. La insignia no puede aparecer en imágenes generadas por IA.

## Cómo funcionaría en el juego

**La escena del telescopio**

- La Luna es una esfera 3D con el mapa de color de LROC (4k) y el relieve de LOLA convertido en mapa de normales.
- La luz del Sol llega desde la dirección del borde iluminado. La esfera gira según el punto subterrestre (la libración) y el ángulo paraláctico del Mirador. Así coinciden la fase, la inclinación y la cara visible.
- El ocular es una viñeta circular con retícula cian, enfoque y zoom. Una opción muestra la imagen invertida, como en un telescopio real.
- Órbita aparece en una esquina y comenta con los datos de la tabla, citando la fuente y la hora.
- Se pueden marcar mares y cráteres con su nombre. Los lugares de alunizaje del programa Apolo enlazan con el archivo Apolo del guion anterior.

**Los datos**

- **Sin conexión:** una tabla por hora para varios años, generada con `luna_efemerides.py` desde Horizons o tomada de la tabla anual de NASA SVS.
- **Con conexión (opcional):** una consulta a Horizons para la fecha y el lugar del jugador.
- **Respaldo:** fórmulas astronómicas en GDScript, comparadas contra Horizons con una tolerancia fijada.

**El juego**

- En el Acto I, la primera visita al Mirador muestra la Luna de ese día.
- Misión propuesta, «Bitácora lunar»: observar la Luna en tres fases distintas y anotarlas en el cuaderno. La recompensa es la carta estelar `COL-12`.
- Conecta con el Mirador del mapa del lote 02 y con el planetario y el archivo Apolo del guion anterior.

## Riesgos

| Riesgo | Qué hacer |
|---|---|
| El título de trabajo dice «NASA» | Para publicar, usar un título sin «NASA». En los créditos: «Datos: NASA/JPL Horizons; NASA Scientific Visualization Studio; LRO». |
| La práctica «en la NASA» del guion anterior | Mantener el centro espacial como ficticio, sin logotipos ni insignias, como en el lote 02. |
| Música de los videos de NASA SVS | Las versiones con música usan pistas de Universal Production Music, con derechos de terceros. No usarlas. |
| Precisión científica | Las texturas son «para la estética». Las cifras de las fichas salen siempre de Horizons o de la tabla de NASA. |
| Jugar sin internet | Tabla incluida en el juego; la consulta en línea es opcional. |

## Extensiones por validar

- **Planetas por el telescopio:** Júpiter con sus lunas y Saturno con sus anillos, con la misma API.
- **La Tierra vista desde satélites:** imágenes reales del estuario del Guayas para la misión «Vigía del Golfo» del guion anterior.
- **La Estación Espacial** pasando sobre Guayaquil, con sus datos orbitales públicos.

## Prueba técnica en Godot (2026-11-12)

Guillermo autorizó la descarga el mismo día («Sí, descárgalos»).

![[luna_telescopio.png]]

*Captura de Godot 4.7.2 (`pruebas/luna_telescopio/`): la Luna de las 19:30 desde el Mirador, con texturas de LRO, la luz cenicienta, a Órbita y las fichas calculadas.*

### Descargas

Cada archivo está en su propia carpeta de `externos/`, con tamaño y SHA-256 en `Propuestas/Datos/descargas_nasa.json`.

| Archivo | Bytes | Contenido |
|---|---:|---|
| `lroc_color_poles_4k.tif` | 13 095 388 | Color, 4096×2048, RGB de 8 bits |
| `ldem_4.tif` | 4 153 352 | Relieve, 1440×720, en km, coma flotante |
| `mooninfo_2026.json` | 2 094 339 | 8 760 horas de 2026 |

### Cómo funciona

1. `herramientas/luna_texturas.py` comprueba la orientación de los mapas con rasgos conocidos:
   - el punto más alto cae a 0,0° de la cumbre Selenean;
   - el más bajo, a 0,4° del cráter Antoniadi;
   - la cara visible es más oscura y más baja.

   Después convierte el color a JPG y el relieve a un mapa de normales sin exagerar.
2. `herramientas/luna_efemerides.py` consulta Horizons para el Mirador: punto subobservador, punto subsolar, ángulo del polo norte y ángulo paraláctico. `herramientas/luna_parametros.py` toma la fila de una hora y calcula la puesta.
3. El shader proyecta cada píxel del disco sobre la esfera, lo pasa a longitud y latitud selenográficas y lee las texturas. La luz sigue la ley de Lommel-Seeliger, que da a la Luna llena su brillo parejo hasta el borde. El relieve se exagera ×4 junto al terminador y ×1,5 en el resto.
4. Las texturas son recursos importados de Godot y se cargan con `preload`: el color en BC7 con mipmaps y las normales sin pérdida. Así existen también en el juego exportado.
5. Las fichas, los rótulos («Terminador», «Luz cenicienta») y la frase de Órbita se calculan con los datos, según la fase y la altura.
6. `herramientas/luna_medir.py` mide las capturas contra Horizons: fracción iluminada, ángulo del borde y orientación de la textura.

### Mediciones

Todas con el código final. `luna_medir.py` da «coincide con Horizons» en los tres casos medidos: editor, juego exportado y HDR 2D.

| Prueba | Godot | Referencia o criterio |
|---|---:|---:|
| Fracción iluminada (máscara) | 12,15 % | Horizons: 12,2 % |
| Borde iluminado desde el cenit | 192,6° | Horizons: 192,6° |
| Orientación de la textura (`luna_medir.py`) | Correlación 0,990; mejor giro 0,00°; en espejo, 0,303 como máximo | Más de 0,9; giro de 0,5° o menos; espejo por debajo de 0,5 |
| Posición de Mare Crisium (revisor) | (586,8; 524,3) px | Proyección independiente: (588,4; 522,4) px |
| Gibosa del 21 nov a las 21:00, a 70,6° de altura | 91,21 % y borde a 41,0° | Horizons: 91,2 % y 41,0° |
| Juego exportado (`.pck`) contra el editor | 0 niveles de diferencia | Idénticos |
| HDR 2D contra normal, dentro del disco | 0,85 niveles de media, 1 como máximo | Sin cambio visible |
| Costo en GPU, HD 620 a 720p (revisor) | 0,74 ms; 2,2 a 2,5 ms con la Luna a pantalla completa | 16,7 ms por cuadro a 60 fps |

![[luna_gibosa_2026-11-21.png]]

*La misma escena con la gibosa del 21 de noviembre a las 21:00: el disco crece a 32,7′ y el borde iluminado queda arriba a la izquierda. Sin luz cenicienta visible, el rótulo no aparece.*

![[luna_bajo_horizonte_2026-11-12.png]]

*A las 22:00 de hoy la Luna ya se puso: no se dibuja, y Órbita lo dice. A las 06:00 de mañana, por el este, dice que todavía no sale.*

### Verificación independiente

- **Orientación:** un revisor rehízo la proyección por su cuenta, sin mirar el shader. Los rasgos caen a 0,6 px o menos en la luz cenicienta y a entre 1 y 2,5 px en la media luna. Descartó el espejo, el giro de 180° y los errores de signo. Confirmó en la documentación de Horizons que las longitudes son positivas al este y que NP.ang y SN.ang se miden de norte a este.
- **Datos:** otro revisor comparó la tabla de NASA con Horizons en las 8 760 horas de 2026. Diferencia máxima: 0,0075 puntos de iluminación, 0,67 km de distancia y 0,006° en la libración. Con las correcciones topocéntricas (paralaje y ángulo paraláctico) la tabla reproduce lo que se ve desde el Mirador. Las descargas coinciden en tamaño y SHA-256.
- **Código:** un tercer revisor auditó el shader y el script como si fueran a producción, con un emulador propio del shader y un `.pck` exportado. Encontró 9 problemas: 1 crítico, 3 medios y 5 bajos. La captura de esta noche era correcta; los fallos aparecían en el juego exportado, en otras fechas o con otros ajustes.

### Correcciones aplicadas tras la verificación

- **Hora de puesta:** pasó de 21:04 a **21:07**. Ahora sigue el criterio de los almanaques: el borde superior toca el horizonte, con 34′ de refracción. La de 21:04 era el centro del disco sin refracción. La maqueta del lote 03 decía 21:05.
- **Decimales:** el ángulo del polo norte y el paraláctico se guardan con tres decimales. El redondeo giraba el disco 0,02°.

Hallazgos del revisor de código:

| Hallazgo | Gravedad | Corrección y prueba |
|---|---|---|
| Las texturas no existían en el juego exportado: la Luna salía como un disco gris y el gato desaparecía | Crítica | Recursos importados y `preload`. El `.pck` exportado da una captura idéntica a la del editor |
| La Luna se dibujaba bajo el horizonte; rótulos y frase fijos | Media | Aviso y frase según el acimut; rótulos según la fase. Probado a las 22:00 de hoy, a las 06:00 de mañana y con la gibosa del 21 de noviembre |
| Con HDR 2D la gamma se aplicaba dos veces y la captura no lo mostraba | Media | El shader entrega color lineal con la curva sRGB exacta y la captura lo convierte de vuelta. Disco: 0,85 niveles de diferencia |
| La orientación vale solo para la hora de la fila; cerca del cenit gira hasta 12° por minuto | Media | **Pendiente**: calcular el ángulo paraláctico en el juego para cada instante |
| Polos y costura de ±180°: saltos de nivel de detalle | Baja | Sin envolver en vertical y derivadas corregidas en la costura |
| Derivadas dentro de ramas y `smoothstep` con los bordes invertidos | Baja | Geometría fuera de las ramas y bordes en orden |
| Relieve ×4 horneado en el mapa | Baja | Mapa sin exagerar; el shader aplica ×4 junto al terminador y ×1,5 en el resto |
| La luz cenicienta oscurecía el limbo un 40 % y no cambiaba con la fase | Baja | Sin el factor de ángulo y escalada con la fase de la Tierra vista desde la Luna |
| Aspecto y tamaño del disco fijos | Baja | El disco escala con el diámetro aparente (29,4′ a 33,5′) y la ventana conserva la proporción |

Dos hallazgos más salieron al probar las correcciones:

- `Image.linear_to_srgb()` de Godot 4.7.2 solo acepta imágenes de 8 bits. Con HDR 2D la captura quedaba sin convertir, 20 niveles más oscura. Ahora se convierte píxel a píxel (2,6 s por captura).
- La salida lineal con `pow(x, 2.2)` oscurecía las sombras unos 6 niveles frente a la curva sRGB exacta que usa Godot.

La prueba de orientación de `luna_medir.py` daba 0,650: las líneas cian de los rótulos cruzan la zona de luz cenicienta. Al excluirlas da 0,990.

### Límites conocidos

- **Una hora fija:** la escena usa la fila de una hora. Cerca del cenit, que en Guayaquil ocurre unas dos veces al mes, el disco gira rápido: el 21 de noviembre el borde iluminado pasa de 41° a 89° entre las 21:00 y las 22:00. Para cualquier instante, el juego debe calcular el ángulo paraláctico con la declinación y el ángulo horario.
- **Solo 2026:** la tabla cubre las 8 760 horas de 2026. Para otro año hace falta la tabla anual de NASA de ese año o Horizons.
- **Ruta sin conexión:** el ángulo del eje de la tabla se mide desde el norte J2000. Hay que pasarlo al norte de la fecha (hasta 0,17°) antes de restar el ángulo paraláctico.
- **Cielo siempre nocturno:** de día y en el crepúsculo se siguen dibujando estrellas sobre fondo negro.
- **Sin eclipses:** en un eclipse lunar la Luna saldría llena y blanca.
- **Bajo el horizonte:** el panel no da la hora de salida; «Se pone» queda en «—».
- **Vista a ojo desnudo:** un telescopio real sin diagonal invierte la imagen 180°. Puede ser una opción del juego.
- **Sin sombras proyectadas:** el relieve solo sombrea; no hay sombras arrojadas por cráteres.
- **Imagen fija:** no hay enfoque ni zoom todavía.
