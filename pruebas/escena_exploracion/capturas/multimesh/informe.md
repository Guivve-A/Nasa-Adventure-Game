# Informe de agrupado con MultiMesh

## Cambio realizado

`escena.gd` agrupa por el par exacto `glb` y `nodo` despues de colocar los recursos y resolver `sobre`. El layout disponible produce 17 grupos de recursos repetidos, 227 recursos agrupados y 18 MultiMeshInstance3D. Un grupo tiene dos mallas hijas, de ahi los 18 lotes y las 229 transformaciones de malla verificadas.

Cada lote conserva las superficies de su malla y recibe los materiales activos de MeshInstance3D. Los ShaderMaterial se comparten con el registro de Materiales para que la tecla I siga actualizando la inclinacion. Las transformaciones incluyen la jerarquia interna del GLB, pivotes, altura normalizada, escala, rotacion y posicion final de apoyo. Se conserva cast_shadow, las capas y el material superpuesto.

Los nodos originales agrupados quedan ocultos para conservar las referencias de instancias y las cajas usadas por Materiales.caja_mundo. Esta decision conserva su coste de memoria y montaje. Los recursos unicos y las entradas con animacion o variante siguen usando su recorrido original.

El AABB personalizado une los limites de las instancias en coordenadas de mundo, con inclinacion cero y la inclinacion configurada, y cubre el balanceo actual de follaje de 0,035 m/m en X y 0,0175 m/m en Z. Luego convierte los limites al espacio local del lote.

## Entorno y mediciones

Godot 4.7.2.stable.official.ed1daf0bf, Vulkan Forward Mobile, Intel HD Graphics 620 y 1280 x 720. Cada medicion usa `--medir=6`, con el calentamiento de dos segundos que ya tenia la escena y VSync desactivado. Las capturas usan el MSAA y las sombras existentes.

### Referencia inicial y version final

| Encuadre | FPS antes | FPS despues | p95 antes, ms | p95 despues, ms | Llamadas antes | Llamadas despues | Primitivas antes | Primitivas despues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 21 | 57,6 | 54,5 | 19,55 | 20,27 | 252 | 58 | 244591 | 344388 |
| 12 | 54,5 | 56,3 | 20,45 | 20,01 | 420 | 64 | 245160 | 255926 |

Las llamadas se reducen un 77,0 % y un 84,8 %. En el encuadre 21 los FPS retroceden 3,1 en esta comparacion y las primitivas aumentan un 40,8 %. En el 12 las primitivas aumentan un 4,4 % y los FPS quedan dentro de la variacion observada en las repeticiones del original.

MultiMesh realiza el descarte espacial por grupo y envia todas sus instancias cuando el grupo es visible. Esto explica una posible causa del aumento de primitivas y del coste GPU observado. La relacion causal con los FPS queda como inferencia, sin un perfil GPU por etapa. [Documentacion oficial de MultiMesh](https://docs.godotengine.org/en/stable/classes/class_multimesh.html)

Las lineas siguientes corresponden a la referencia tomada antes de editar y a la version final.

```text
MEDIDA encuadre=21 cuadros=346 fps_medio=57.6 ms_medio=17.38 ms_p95=19.55 primitivas=244591 llamadas=252 resolucion=(1280.0, 720.0)
MEDIDA encuadre=21 cuadros=328 fps_medio=54.5 ms_medio=18.35 ms_p95=20.27 primitivas=344388 llamadas=58 resolucion=(1280.0, 720.0)
MEDIDA encuadre=12 cuadros=327 fps_medio=54.5 ms_medio=18.35 ms_p95=20.45 primitivas=245160 llamadas=420 resolucion=(1280.0, 720.0)
MEDIDA encuadre=12 cuadros=338 fps_medio=56.3 ms_medio=17.77 ms_p95=20.01 primitivas=255926 llamadas=64 resolucion=(1280.0, 720.0)
```

### Repeticiones y ensayo del limite de visibilidad

Se ejecutaron dos rondas alternando la fuente original guardada en `escena_antes.gd.txt` y el primer agrupado. Ese agrupado usaba un margen global para el descarte. El original reprodujo las mismas cantidades de primitivas y llamadas de la referencia. Sus FPS variaron entre 62,1 y 73,9 en el encuadre 21 y entre 56,2 y 59,7 en el 12.

La version final sustituye aquel margen global por el AABB personalizado descrito arriba. En el encuadre 12 esto reduce las primitivas del agrupado de 282984 a 255926. Las lineas de estas rondas corresponden al ensayo anterior al ajuste final.

```text
antes, ronda 1
MEDIDA encuadre=21 cuadros=444 fps_medio=73.9 ms_medio=13.54 ms_p95=16.89 primitivas=244591 llamadas=252 resolucion=(1280.0, 720.0)
despues, ronda 1
MEDIDA encuadre=21 cuadros=341 fps_medio=56.7 ms_medio=17.63 ms_p95=19.29 primitivas=344388 llamadas=58 resolucion=(1280.0, 720.0)
antes, ronda 1
MEDIDA encuadre=12 cuadros=358 fps_medio=59.7 ms_medio=16.76 ms_p95=19.06 primitivas=245160 llamadas=420 resolucion=(1280.0, 720.0)
despues, ronda 1
MEDIDA encuadre=12 cuadros=330 fps_medio=55.0 ms_medio=18.20 ms_p95=20.10 primitivas=282984 llamadas=64 resolucion=(1280.0, 720.0)
antes, ronda 2
MEDIDA encuadre=21 cuadros=373 fps_medio=62.1 ms_medio=16.10 ms_p95=17.51 primitivas=244591 llamadas=252 resolucion=(1280.0, 720.0)
despues, ronda 2
MEDIDA encuadre=21 cuadros=333 fps_medio=55.4 ms_medio=18.03 ms_p95=19.98 primitivas=344388 llamadas=58 resolucion=(1280.0, 720.0)
antes, ronda 2
MEDIDA encuadre=12 cuadros=338 fps_medio=56.2 ms_medio=17.79 ms_p95=20.34 primitivas=245160 llamadas=420 resolucion=(1280.0, 720.0)
despues, ronda 2
MEDIDA encuadre=12 cuadros=335 fps_medio=55.7 ms_medio=17.94 ms_p95=20.04 primitivas=282984 llamadas=64 resolucion=(1280.0, 720.0)
```

Los archivos `despues_21_medida.log` y `despues_12_medida.log` contienen las primeras pruebas del margen global, con 51,4 y 51,7 FPS. La primera coincidio parcialmente con importaciones del editor. Las rondas anteriores se ejecutaron secuencialmente al terminar la importacion. Los resultados finales estan en `final_21_medida.log` y `final_12_medida.log`.

## Comparacion de imagenes

La diferencia media se calcula como la media del valor absoluto de la diferencia de los tres canales RGB en todos los pixeles, sobre la escala de 0 a 255. Los PNG tienen 1280 x 720 pixeles. `comparar.py` reproduce las cuentas y `diferencias.json` contiene los valores completos.

### Capturas con el comando normal

| Encuadre | Antes | Despues | Diferencia media RGB |
| --- | --- | --- | --- |
| 21 | [Antes](antes_21.png) | [Despues](despues_21.png) | 2.260027 |
| 12 | [Antes](antes_12.png) | [Despues](despues_12.png) | 5.479379 |

Estas capturas se tomaron al cabo de los 40 cuadros del comando existente. TIME, el agua y la animacion del gato avanzan segun el tiempo real de cada ejecucion. Por ello se hizo tambien la comparacion controlada siguiente.

### Capturas con tiempo y pose fijados

El controlador `verificar.gd` carga la fuente original o la final. Fija el gato en 0,25 s y sustituye TIME solo en los Shader temporales de la prueba. El agua queda en 0,25 s. El follaje se captura en 0,25 s y 1,25 s. La escena de juego conserva sus shaders originales.

| Encuadre | Estado | Antes | Despues | Diferencia media RGB |
| --- | --- | --- | --- | --- |
| 21 | Inclinacion 0,45 y viento en 0,25 s | [Antes](antes_21_fijo.png) | [Despues](despues_21_fijo.png) | 0.001292679 |
| 21 | Inclinacion 0,45 y viento en 1,25 s | [Antes](antes_21_viento.png) | [Despues](despues_21_viento.png) | 0.003152127 |
| 21 | Inclinacion 0 y viento en 0,25 s | [Antes](antes_21_sin_inclinacion.png) | [Despues](despues_21_sin_inclinacion.png) | 0.000768953 |
| 12 | Inclinacion 0,45 y viento en 0,25 s | [Antes](antes_12_fijo.png) | [Despues](despues_12_fijo.png) | 0.000009404 |
| 12 | Inclinacion 0,45 y viento en 1,25 s | [Antes](antes_12_viento.png) | [Despues](despues_12_viento.png) | 0.000000000 |
| 12 | Inclinacion 0 y viento en 0,25 s | [Antes](antes_12_sin_inclinacion.png) | [Despues](despues_12_sin_inclinacion.png) | 0.000000000 |

La equivalencia visual se conserva con diferencias residuales muy pequenas. En la toma fija del encuadre 21, el 0,005534 % de los pixeles difiere mas de dos niveles de canal y la diferencia maxima de canal es 28. En el encuadre 12 cambia un pixel y la diferencia maxima de canal es 13. El origen exacto de esos residuos queda sin aislar. La inspeccion visual y las transformaciones verificadas son coherentes con diferencias de rasterizacion y sombras en bordes.

Las imagenes de diferencia absoluta amplificada ocho veces estan en [encuadre 21](diferencia_21_x8.png) y [encuadre 12](diferencia_12_x8.png).

### Viento e inclinacion

| Encuadre | Efecto | Cambio medio del original | Cambio medio del agrupado |
| --- | --- | --- | --- |
| 21 | viento | 3.309383681 | 3.309177156 |
| 21 | inclinacion | 27.005367115 | 27.005369285 |
| 12 | viento | 4.848493200 | 4.848499711 |
| 12 | inclinacion | 27.919391638 | 27.919384404 |

Para viento se compara 0,25 s con 1,25 s manteniendo el agua y la pose. Para inclinacion se compara 0,45 con cero manteniendo la camara y el tiempo. Ambos efectos producen el mismo cambio visual antes y despues, dentro de los residuos anteriores. Los materiales de cada superficie y las matrices de las instancias coinciden con sus originales, incluidos los shaders con world_vertex_coords.

## Verificacion funcional

La comprobacion de GDScript mediante `--headless --script res://escena.gd --check-only` termino con la salida normal del motor. La ejecucion grafica verifico materiales por superficie, sombras, las 229 transformaciones, las mallas individuales ocultas y las excepciones visibles. Tambien verifico el gato reproduciendo caminar y el apoyo de la iguana sobre roca_iguana.

Se inyectaron eventos por `_unhandled_input` para I, A, 1 y 2. La inclinacion se desactiva y restaura a 0,45 en todos los materiales compartidos, la antena Tripo se oculta y reaparece y ambos encuadres responden.

```text
PRUEBA_LOTES lotes=18 transformaciones=229
PRUEBA_CONTROLES inclinacion=OK antena_tripo=OK encuadres=OK
PRUEBA version=despues fallos=0 materiales_follaje=12
```

Los registros completos estan en `prueba_antes.log`, `prueba_despues.log` y `verificacion_script.log`. El controlador es una prueba adicional para esta regresion y sus capturas. La carpeta de evidencia contiene `.gdignore` para evitar importarla en el editor.

## Limites y elementos pendientes de comprobar

- Desde la referencia inicial faltan `modelos/COL-01_script.glb`, `modelos/COL-02.glb` y `modelos/FX-01.glb`. La geometria y apariencia de esos recursos quedan sin verificar. La antena Tripo disponible y su conmutacion si se comprobaron.
- Las ejecuciones graficas registran un error al leer el almacen de certificados del sistema. El controlador visual registra tambien dos errores de escritura de cache de shader. Godot devuelve codigo de salida 1 en esas ejecuciones, aunque genera las capturas y las comprobaciones terminan con cero fallos.
- Las capturas normales registran las fugas de CanvasItem/ObjectDB presentes tambien en la fuente original. La primera ejecucion del editor registro errores de escritura de ajustes fuera del proyecto y del log de usuario. Los registros siguientes usan una ruta absoluta de log dentro de la carpeta de evidencia.
- Los ensayos cubren los recursos disponibles en este layout y ambos encuadres. Quedan sin perfilar el coste GPU por etapa, otras camaras y sesiones de juego prolongadas.
- El agrupado conserva el coste de los nodos originales ocultos. La mejora comprobada corresponde a las llamadas de dibujo. En el encuadre 21 se observa una regresion de FPS.

## Reproduccion

Desde esta carpeta de proyecto, con `$g` apuntando al ejecutable indicado por el usuario y `$proyecto` a la ruta absoluta del proyecto.

```powershell
& $g --path $proyecto -- --encuadre=21 --medir=6
& $g --path $proyecto -- --encuadre=12 --medir=6
& $g --path $proyecto --script res://capturas/multimesh/medir_original.gd -- --encuadre=21 --medir=6
& $g --path $proyecto --script res://capturas/multimesh/medir_original.gd -- --encuadre=12 --medir=6
& $g --path $proyecto --script res://capturas/multimesh/verificar.gd -- --prueba_version=antes
& $g --path $proyecto --script res://capturas/multimesh/verificar.gd -- --prueba_version=despues
python capturas/multimesh/comparar.py
```

Para dirigir los logs dentro del espacio de trabajo se puede agregar `--log-file` con una ruta absoluta antes de `--`. Los PNG normales se reproducen con el comando `--captura` del brief.
