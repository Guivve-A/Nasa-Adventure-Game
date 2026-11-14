# PER-01 v3: proyección de la hoja

El parecido total sube de **62,2 % a 64,9 %** (+2,7 puntos). **No alcanza el objetivo del 80 %.** No baja el parecido agregado de ninguna vista. La estructura de la cabeza sí baja: 26,1 % → 24,3 %.

## Archivos

- Script: `herramientas/mallas/proyectar_hoja.py`, desde la raíz del proyecto.
- Malla: [L04_PER01_v3_hoja.glb](../../L04_PER01_v3_hoja.glb).
- Imagen exacta incorporada al GLB: [textura.png](textura.png), 4096 × 4096, PNG sin pérdida.
- Resultado numérico del horneado: [horneado.json](horneado.json).
- Métrica antes/después: [metricas.json](metricas.json).
- Especificación de medición: [spec_v3.json](spec_v3.json).
- Láminas: [antes](antes_lamina.png), [después](despues_lamina.png).
- Cara de frente: [px_cabeza.png](renders/px_cabeza.png), [hoja_cabeza.png](hoja_cabeza.png), [comparación conjunta](cara_comparacion.png).
- Las ocho tomas sin luz están en `renders/`.

![Cara de la hoja y render frontal de la v3](cara_comparacion.png)

El panel izquierdo recorta el 36 % superior del frente de la hoja, como la métrica. El derecho muestra el `px_cabeza.png` completo del renderizador solicitado, cuya cámara usa el encuadre de cabeza predeterminado (0,42). Son encuadres diferentes; no se usó esta lámina para calcular el parecido.

## Método y conservación del recurso

Se proyectan frente desde +X, espalda desde -X y perfil derecho desde +Z; el perfil mira a la derecha de su imagen. Se aplica la matriz del nodo al calcular las posiciones y normales en el mundo. La matriz original del GLB se conserva.

La máscara de cada recorte separa los colores a más de 28 unidades RGB de la mediana de sus bordes. No se incluye la línea del suelo: los recortes terminan antes de la fila 923. El centroide establece el origen de la búsqueda; la altura establece la escala nominal. El ajuste se decide rasterizando las siluetas y maximizando su IoU, no haciendo coincidir la caja que contiene el bolso. Se exploran escalas de 92 % a 108 % y traslaciones de ±6 % del ancho/alto de la figura. Una búsqueda mediante correlación FFT a resolución reducida se refina a pasos de un píxel y 0,1 % de escala alrededor del mejor candidato. Es una optimización discreta, no una demostración de máximo continuo.

| Vista | IoU de alineación | Escala respecto de la nominal | Desplazamiento x, y |
|---|---:|---:|---:|
| Frente | 85,01 % | 101,4 % | +6, -12 px |
| Perfil derecho | 87,00 % | 101,5 % | +3, -7 px |
| Espalda | 87,07 % | 101,9 % | -4, -10 px |

Las imágenes `*_alineacion.png` muestran gris donde coinciden las siluetas, rojo donde solo hay hoja y azul donde solo hay malla. Este IoU de alineación es distinto del IoU de la métrica oficial, que recorta y normaliza por separado cada imagen.

Cada texel de superficie se rasteriza en UV y recupera su posición y normal interpoladas mediante coordenadas baricéntricas. Un búfer de profundidad al doble de la resolución de la hoja identifica el triángulo visible. Se evalúa su plano en la posición exacta proyectada; solo se acepta el propio triángulo o una profundidad coincidente dentro de 0,00002 m. Esto evita usar una tolerancia amplia que atraviese brazos o piernas.

En las zonas elegibles, cada vista aporta `visible × max(0, n·d)^3 × máscara_erosionada`. La erosión cuadrada es de 3 px (ventana 7 × 7). Los cuatro píxeles del soporte bilineal deben estar dentro de ella. La mezcla es exactamente `(suma(peso_v × hoja_v) + 0,15 × original) / (suma(peso_v) + 0,15)`, con redondeo final a RGB de 8 bits.

No se crea una proyección espejada desde -Z. Para conservar expresamente el costado izquierdo, sus texels se definen como aquellos cuya normal interpolada tiene -Z como eje dominante; en ese sector se omite el repintado. Son **2.058.415 texels**, con **0 diferencias** respecto de la imagen Tripo decodificada. Las zonas de transición que pertenecen a frente o espalda sí pueden recibir esas vistas. Esta definición del sector izquierdo queda registrada en `horneado.json`.

Se extiende el color doce texels fuera de las islas UV usando vecinos ortogonales, sin envolver los extremos del mapa. El relleno afecta 1.652.567 texels que no pertenecen a la superficie rasterizada; no altera los texels de las islas.

Se mantienen idénticos los bytes originales del búfer y los metadatos de geometría, índices, normales, UV, nodos, escenas, materiales y texturas. Se anexa el PNG y se cambia únicamente el enlace y el tipo MIME de la imagen, con los ajustes de longitud necesarios del contenedor. El JPEG anterior queda como datos sin uso dentro del GLB para conservar íntegro el búfer original. La geometría sigue teniendo **7.522 triángulos**. La v2, la hoja, los scripts existentes y la escena de Godot no se modificaron.

## Parecido oficial

Se ejecutó `comparar_personaje.py` con el spec original para el control y con una copia que solo cambia las rutas de render para la v3. Frente y cabeza pesan 2; perfil y espalda pesan 1. La cabeza de esta métrica proviene del 36 % superior de `px_cuerpo.png`, no de `px_cabeza.png`.

| Vista | Parecido v2 | Parecido v3 | Cambio |
|---|---:|---:|---:|
| Frente | 59,4 % | 61,5 % | +2,1 puntos |
| Cabeza | 59,3 % | 60,1 % | +0,8 puntos |
| Perfil derecho | 66,6 % | 71,5 % | +4,9 puntos |
| Espalda | 69,2 % | 74,8 % | +5,6 puntos |
| **Total ponderado** | **62,2 %** | **64,9 %** | **+2,7 puntos** |

| Vista | Silueta v2 → v3 | Color v2 → v3 | Estructura v2 → v3 |
|---|---:|---:|---:|
| Frente | 79,9 → 79,9 % | 62,4 → 69,1 % | 29,2 → 29,4 % |
| Cabeza | 93,9 → 94,0 % | 46,2 → 50,8 % | 26,1 → 24,3 % |
| Perfil derecho | 86,0 → 86,0 % | 67,4 → 76,7 % | 40,0 → 47,1 % |
| Espalda | 84,8 → 84,8 % | 72,9 → 81,4 % | 44,8 → 54,8 % |

La disminución de estructura de la cabeza es coherente con el primer plano: aparecen transiciones en mejillas y trazos dobles en la boca. La alineación global por silueta no alinea individualmente ojos, boca y mechones. La mezcla obligatoria retiene rasgos de la textura anterior, y las vistas aportan detalle desde direcciones distintas. La malla conserva posiciones y volúmenes que difieren de la ilustración; el bolso tampoco adquiere volumen al pintarlo. No se aisló experimentalmente cuánto contribuye cada causa a la caída del componente de estructura.

El cambio de 0,1 puntos en la silueta de cabeza procede de la segmentación por color de la métrica: la geometría y su contorno real no cambiaron.

## Cobertura y fondo

| Dato | Resultado |
|---|---:|
| Texels rasterizados sobre superficie UV | 10.414.844 |
| Texels con aporte de la hoja | 5.546.432 |
| Cobertura sobre texels de superficie | **53,2551 %** |
| Cobertura sobre la imagen completa de 4096² | **33,0593 %** |
| Texels pintados cuyo soporte tomó fondo | **0 / 5.546.432 = 0,0000 %** |
| Muestras de vista sobre fondo | **0** |

La cobertura cuenta aporte de peso positivo, aunque el redondeo final pueda producir el mismo RGB que el original. No cuenta el relleno exterior de las islas. Se auditan los cuatro píxeles de cada muestra bilineal contra la máscara original sin erosionar. El 0 % de fondo está comprobado respecto de esa máscara automática; no existe una anotación manual independiente de todos los píxeles de la hoja.

El búfer rechazó por ocultación 1.009.542 muestras frontales, 2.430.285 de perfil y 901.979 de espalda, después del filtro angular y de máscara. Son muestras por vista; no equivalen a texels únicos.

## Comprobaciones realizadas y límites

- Horneado completo con NumPy y Pillow ya instalados: 236,8 segundos. Sin instalaciones, red ni créditos.
- Aserciones de conservación binaria del búfer original, UV, geometría, nodos y materiales: correctas.
- Aserción de coincidencia del sector izquierdo con la textura Tripo: correcta.
- Prueba sintética de dos superficies superpuestas: acepta la delantera y rechaza la posterior.
- Prueba sintética de máscara vacía: no aporta color de hoja.
- Prueba del relleno UV: propaga al vecino y no cruza a los extremos opuestos del mapa.
- Importación y ocho renders sin luz con Blender 5.3.0: correctos. Caja y dimensiones coinciden con la v2.
- Medición oficial y revisión visual de cara, lámina completa y alineaciones.

No se comprobó la apariencia dentro de Godot 4.7.2, con iluminación del juego, animación o cámara de juego. No se certifica un parecido perceptual del 80 %: la métrica medida es 64,9 %. Tampoco se demuestra el máximo continuo del ajuste ni una segmentación manual perfecta. La prueba sintética comprueba el mecanismo de ocultación; no constituye una revisión manual de cada texel de brazos y caras internas de piernas.

## Reproducción

Ejecutar desde la raíz del proyecto, sin instalar dependencias:

```powershell
python -I herramientas/mallas/proyectar_hoja.py

& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup --python-exit-code 1 --python herramientas/blender/render_vistas.py -- --glb Nasa_Game/Fase_1_Arte/Modelado/Lote_04/L04_PER01_v3_hoja.glb --salida Nasa_Game/Fase_1_Arte/Modelado/Lote_04/parecido/v3_hoja/renders --lado 1000

python -I herramientas/comparar_personaje.py Nasa_Game/Fase_1_Arte/Modelado/Lote_04/parecido/spec_v2.json Nasa_Game/Fase_1_Arte/Modelado/Lote_04/parecido/v3_hoja/antes_lamina.png --etiqueta "v2 antes del repintado"

python -I herramientas/comparar_personaje.py Nasa_Game/Fase_1_Arte/Modelado/Lote_04/parecido/v3_hoja/spec_v3.json Nasa_Game/Fase_1_Arte/Modelado/Lote_04/parecido/v3_hoja/despues_lamina.png --etiqueta "v3 hoja, visibilidad y original 0.15"
```

La procedencia es exclusivamente la malla Tripo v2 y la hoja local suministradas para esta tarea; sus SHA-256 están en `horneado.json`. No se añadieron recursos externos. Para volver al estado anterior basta con seguir usando `L04_PER01_giro_tripo_mv.glb`; no se cambió ninguna referencia de la escena.
