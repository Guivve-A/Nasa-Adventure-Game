# Telescopio · La Luna sonriente

Implementado para la escena 2.2, orden 4, ficha `luz_cenicienta`. Solo se escribieron archivos en `juego/minijuegos/telescopio/` y en esta carpeta. No hubo descargas ni instalaciones.

## Archivos entregados

En `juego/minijuegos/telescopio/`:

- `telescopio.gd`: buscador, enfoque, reconocimiento secuencial y pilotos.
- `minijuego.json`: metadatos, 4 instrucciones, controles y 3 pistas.
- `luna.gdshader`: shader reutilizado de la prueba existente; añade desplazamiento del buscador y adapta el fondo a la paleta. Conserva la proyección, orientación y modelo de iluminación.
- `enfoque.gdshader`: desenfoque de 9 muestras de la imagen completa.
- `prueba_telescopio.gd`: prueba específica y capturas opcionales.
- `datos/luna.json`: copia íntegra de la efeméride.
- `texturas/luna_color_4k.jpg`, `texturas/luna_normales.png`, `texturas/texturas.json`: copias íntegras; carga con `Recursos.textura()` en ejecución, sin depender de importaciones.

En esta carpeta: `NOTA.md`, `prueba_contrato.log`, `prueba_modelo.log`, `prueba_visual.log`, `anfitrion.png` y `paso_0.png` a `paso_3.png`. Las 5 capturas se abrieron y revisaron; la del anfitrión verifica la integración completa. Se corrigió un solapamiento entre el dial y la lectura de altura.

## Datos y procedencia

Lectura previa: arquitectura completa, plantilla y JSON, base del minijuego, anfitrión, estilo, fichas y fuentes, prueba técnica lunar completa, propuesta del Mirador y ejemplos aprobados.

La observación permanece fija en **12-11-2026, 19:30, Guayaquil**: **241,4°** de acimut, **20,0°** de altura, **12,2 %** al Sol, **403 151 km**, fase creciente. La orientación se toma con toda la precisión del JSON: polo norte menos ángulo paraláctico; el borde apunta abajo (192,64° en la efeméride, 192,6° en la ficha). El tiempo de partida no cambia la fecha ni simula otra noche.

Fuentes locales: `juego/datos/datos_espaciales.json`, `juego/datos/FUENTES.md`, `pruebas/luna_telescopio/` y `Nasa_Game/Propuestas/Mirador del Faro - Luna con datos reales.md`. Crédito de las imágenes: **NASA's Scientific Visualization Studio, CGI Moon Kit (SVS 4720), LRO LROC WAC y LOLA**. Efemérides: **JPL Horizons, DE441**. Se registra la atribución aquí y en los metadatos; no se usan insignias, logos ni textos de misiones en la interfaz.

Se comprobó identidad SHA-256 con los archivos originales:

| Copia | SHA-256 |
|---|---|
| `datos/luna.json` | `3388ec78a6edcece71f2e3301ce3029e012e9fcb3888336d97ee6800e98d32dd` |
| `texturas/luna_color_4k.jpg` | `51b24920e147bd33440b366e2014d09bf860aabc7e7192be5e502d408a9b160e` |
| `texturas/luna_normales.png` | `8abe3301c133205c24173d679436b14b52bf7144676f7018eecb5f90ae889ec7` |
| `texturas/texturas.json` | `4ff2c4f0b50bd71e8203603b2c8296cf6f30ebdba9170c1591e77cbdb511691c` |

## Reglas del modelo

Las siguientes cifras son parámetros de jugabilidad, no nuevas mediciones astronómicas.

Se gana al confirmar, en orden: Luna centrada, enfoque suficiente y **3 rasgos** (terminador, luz cenicienta, Mare Crisium). Límite global **150 s**, calculado solo con `delta`. Al agotar revisiones o tiempo, se explica la causa de la situación actual.

| Regla | Nivel 1 | Nivel 2 | Nivel 3 |
|---|---:|---:|---:|
| Margen por eje al centrar | ±1,6° | ±1,2° | ±0,8° |
| Margen alrededor del foco 62/100 | ±7 | ±5 | ±3,5 |
| Nitidez mínima, escala didáctica | 93 % | 95 % | 96,5 % |
| Terminador: valor absoluto del producto normal·Sol | ≤0,12 | ≤0,09 | ≤0,065 |
| Distancia aceptada a Mare Crisium, fracción del radio | ≤0,17 | ≤0,14 | ≤0,11 |
| Revisiones que terminan la sesión | 5 | 4 | 3 |

Para cualquier marca se exige radio normalizado <0,97: ni el espacio exterior ni el limbo se confunden con el terminador. La luz cenicienta exige normal·Sol <−0,12 y radio <0,88. La normal se reconstruye con la misma proyección esférica del shader. La tolerancia de Crisium equivale a 25,7 / 21,2 / 16,6 px con el radio de 151,2 px. La guía de 38 px encuadra el entorno y no determina el acierto.

El punto de Mare Crisium procede de la proyección independiente publicada en la propuesta: (588,4; 522,4) en una imagen cuyo centro es (512; 360) y radio 208,8 px. Se conserva su posición normalizada (76,4 / 208,8; 162,4 / 208,8), sin inventar coordenadas selenográficas ni geología.

Buscador esquemático: 6 px/°, campo circular amplio, Luna ampliada a 14,7 px de radio. Acimut limitado a 200–290°, altura a 0–70°, velocidad por eje 9°/s. El ocular detallado tiene radio lunar 151,2 px. La mira se mueve a 115 px/s. El enfoque varía a 0,2 unidades/s en escala 0–1; desenfoque = 30 × distancia al foco, en píxeles. Ratón: clic sobre la Luna para centrar, diales, rueda de enfoque y movimiento de mira; E/Intro/Espacio o botón confirman.

Puntuación de victoria: máximo entre 40 y (100 − 10 × revisiones). Fallo: 0. `jugar_solo(true)` mueve los mismos estados y confirma por la lógica común. `jugar_solo(false)` sube realmente a unos 58° y agota las revisiones mediante la comprobación de centrado; no fuerza `terminar()`.

## Pruebas ejecutadas

Siempre mediante el envoltorio y su candado global, con Godot **4.7.2**. Sin cambios en el núcleo.

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:telescopio --ritmo=8 --todo
```

Pasó al implementarse. La última repetición añadió `--todo` antes de `--` para guardar también la salida íntegra del motor en `prueba_contrato.log`:

```text
TELESCOPIO d1 marcas=3 revisiones=0 tiempo=7.956
PRUEBA_OK telescopio.d1.termina_solo
PRUEBA_OK telescopio.d1.se_puede_superar
TELESCOPIO d3 marcas=3 revisiones=0 tiempo=8.157
PRUEBA_OK telescopio.d3.termina_solo
PRUEBA_OK telescopio.d3.se_puede_superar
MINIJUEGO telescopio superado=false puntos=0.0 detalle=Buscas demasiado alto: esta noche la Luna está a 20,0° de altura. Baja el telescopio.
PRUEBA_OK telescopio.se_puede_fallar
PRUEBA_OK telescopio.el_fallo_explica_la_causa
PRUEBAS hechas=13 fallos=0
FIN
[godot: ok; 5 s; lineas=30; errores=0]
```

Prueba adicional:

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/telescopio/prueba_telescopio.gd --ritmo=8
PRUEBAS hechas=21 fallos=0
FIN
[godot: ok; 6 s; lineas=37; errores=0]
```

Pilotos de los tres niveles: **7,971 / 8,074 / 8,114 s de juego**, 3 marcas y 0 revisiones. Comprueba además el disco, frontera geométrica, luz terrestre frente al Sol, posición de Crisium, enfoque, centrado con ratón, confirmación por acción de teclado, rueda de enfoque, fallo real al señalar el Sol y agotamiento causal a 150 s.

Con ventana, la misma prueba pasó y guardó las 4 fases visuales usando `--evidencia_telescopio`. La captura del anfitrión se obtuvo con `--ventana --minijuego=telescopio --auto --captura=.../anfitrion.png --espera=4.5`. Dispositivo informado: Intel HD Graphics 620, Vulkan, Mobile. Revisión estática adicional: JSON válido, 4 instrucciones, 3 pistas, ficha/escena/orden correctos, sangría de tabuladores y comentarios GDScript sin tildes.

## Límites y pendientes

No quedan funciones del minijuego pendientes. No se midió una tasa de fotogramas sostenida ni se verificó una exportación.

Las corridas no contienen `PRUEBA_FALLO` ni `SCRIPT ERROR`. El motor sí informa que no puede escribir registros en `user://logs`, que no puede leer el almacén de certificados y, con ventana, que no puede guardar la caché de shaders (`_save_to_cache`, `f.is_null()`). La última corrida contractual también notificó 5 instancias ObjectDB al salir. Las pruebas y capturas finalizaron con código 0; esos avisos se conservan en los registros, sin ocultarlos ni modificar carpetas compartidas para resolverlos.
