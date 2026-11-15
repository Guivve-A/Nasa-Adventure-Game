# Lote 08: pantallas de carga pintadas

> Pedido de Guillermo (2026-11-14): las pantallas de carga «se ven mucho IA-like. Sé original. Genera diseños más como Bravely. Itera y perfecciona». Antes había pedido pantallas con presencia, «en versión NASA space». Permiso del mismo día: «usa Higgsfield para lo que necesites». Tope del carril: 18,00 créditos. **Gastado: 15,00.** Saldo: 868,75 → 853,75. **El arte y la composición esperan su veredicto** (Fase 7 sin validar).

## 1. Dirección de arte

**Qué es.** Cada lugar tiene una lámina de libro ilustrado: gouache y acuarela sobre papel de grano, con la pincelada a la vista. La lámina está pegada con cinta en una hoja cuadriculada del cuaderno de ingeniería de la protagonista, y alrededor van las notas a tinta del viaje. La pantalla tiene que parecer una página que alguien pintó y anotó, no una captura con rótulos encima.

**Qué se toma del referente (solo principios).** Fondos que parecen pintados a mano, formas simples y planas, una paleta contenida y cálida con sombras de color, perspectiva atmosférica, vistas amplias con los personajes pequeños y composición por planos, como un teatro de papel: silueta oscura delante, zona iluminada en medio y fondo pálido.

**Qué se evita, porque delata a la IA:** brillo plástico, exceso de detalle minúsculo, rayos de luz de postal, todo nítido a la vez, saturación alta, acabado de render 3D y el texto blanco con contorno sobre la imagen.

**Paleta.** La de la [[Biblia de arte]]: el papel `#F6E7C8`, la tinta `#322C1D` (nunca negro), el azul petróleo `#516B7C` para el camino, la sombra de las lunas y la cuadrícula, la terracota `#924930` para el trazo del nombre y el aviso, y el coral `#E46043` para el sello. El cian no aparece: en esta página no hay tecnología.

**Texto.** Se escribe sobre el papel, nunca sobre la pintura. El nombre del lugar va en letra manuscrita (Segoe Print) con un trazo de pincel debajo. Los datos van en Bahnschrift, a 17 y 18 px, y las cabeceras en mayúsculas espaciadas. Todo es tinta oscura sobre crema, así que se lee sin contornos.

## 2. Tres composiciones para el motor

| | Idea | A favor | En contra |
|---|---|---|---|
| A | **Lámina en el cuaderno de campo.** La lámina, un poco torcida y pegada con tres tiras de cinta, ocupa los dos tercios de una hoja cuadriculada con costura y margen. Debajo, el nombre a mano. A la derecha, una columna de notas: el tramo dibujado como itinerario (punto de origen, camino punteado y destino en un círculo), la misión con su casilla, la ficha con su fuente y un sello de tampón. El indicador de carga es una fila de ocho lunas que se entintan fase a fase | Es la interfaz del cuaderno (biblia, sección 6) y una idea propia del juego. Enmarcar la imagen la convierte en un objeto pintado. El texto se lee sin trucos. No cuesta créditos extra | La pintura no ocupa toda la pantalla |
| B | **Teatro de papel.** La lámina en tres capas recortadas (silueta delantera, plano medio y fondo) que se desplazan a distinto ritmo | Da mucha profundidad y movimiento | Hay que generar y recortar tres capas por lugar: triplica el gasto, y los recortes de IA tienen bordes que la delatan |
| C | **Atlas ilustrado a doble página.** La pintura a sangre en la página izquierda y una cartela caligráfica con los datos en la derecha, con el pliegue en medio | Tiene presencia de libro | Compite con el mapa del mundo (que ya es un atlas) y la cartela formal se aleja del cuaderno de la protagonista |

**Elegida: A**, con dos ideas de las otras. De B, la lámina se asienta sobre la hoja al aparecer y la pintura deriva y se acerca muy despacio dentro de su marco. De C, el nombre del lugar se escribe a mano como en una cartela. Las tres láminas ya generadas sirven tal cual y la página es coherente con el cuaderno, el mapa y los menús.

## 3. Encargos y generaciones

Método: un borrador barato por lugar, mirarlo reducido y después la versión final con el borrador como referencia. La final del sendero se generó primero, como prueba, para comprobar que la calidad alta no volvía a un aspecto de IA; las otras cuatro se pagaron después. Los encargos completos están en `lote_08a_borradores.json` y `lote_08b_finales.json`, y se arman con `armar_lote_08.py`. Referencias: `@ANC_PROTA_1` y `@ANC_GATO`, solo por su diseño. **No se usaron las anclas low-poly**, porque arrastran la imagen hacia el render 3D.

Bloque común de técnica (inglés, en cada encargo): *«Painted as a full-bleed plate from a hand-made illustrated storybook: traditional gouache and transparent watercolor on textured cold-press paper, visible brush strokes, soft wet-in-wet washes… Restrained warm palette… shadows are colored, never black; low saturation. Strong atmospheric perspective… three layered planes like a paper theater… no glossy highlights, no bloom, no lens flare, no light rays, no 3D render look, no digital sharpness, no hyper-detail.»* Cierre: sin texto, letras, números, logotipos, insignias, emblemas ni banderas.

En las finales se añadió: *«repaint it as the finished gouache plate at higher resolution, with the same loose brushwork, the same paper grain and the same level of detail: do not add fine detail, do not sharpen, do not make it look like digital art»*.

| ID | Modelo y parámetros | Escena | Créditos | Veredicto de Claude |
|---|---|---|---:|---|
| `L08_carga_habitacion_borrador` | GPT Image 2.6, low, 1k, 16:9 | Cuarto-taller por la mañana, ventana con el río y el cerro, la protagonista en el banco con la montura y Órbita dormida en el alféizar | 0,25 | Sirve. Pintado y cálido |
| `L08_carga_ciudad_borrador` | ídem | Plaza al pie de la escalinata, la biblioteca, la fuente y dos iguanas; el estuario al fondo | 0,25 | Sirve. Corregir: menos flores rojas delante |
| `L08_carga_sendero_borrador` | ídem | Camino junto al arroyo, el puente, el árbol de flores rojas, la antena y el panel; la ciudad abajo | 0,25 | El mejor: es una lámina de libro |
| `L08_carga_mirador_borrador` | ídem | Terraza del faro de noche, el telescopio, las luces de la ciudad junto al río y la Luna creciente acostada con luz cenicienta | 0,25 | Sirve. La Luna sonriente se lee bien |
| `L08_carga_luna_borrador` | ídem | Llanura lunar del sueño, la Tierra a medias, huellas, la caja, el módulo genérico sin marcas, cascos burbuja | 0,25 | Sirve. Corregir: una Tierra menos saturada y menos fotográfica |
| `L08_carga_sendero` | GPT Image 2.6, high, 2k (2688 × 1520), con el borrador | Igual que el borrador | 2,75 | Mantiene la pincelada y el nivel de detalle. Aprobada para el juego |
| `L08_carga_habitacion` | ídem | Ídem | 2,75 | Fiel al borrador. Aprobada para el juego |
| `L08_carga_ciudad` | ídem | Ídem, con menos flores | 2,75 | Corrección aplicada. Aprobada para el juego |
| `L08_carga_mirador` | ídem | Ídem | 2,75 | Fiel; el cielo gana pincelada. Aprobada para el juego |
| `L08_carga_luna` | ídem | Ídem, con la Tierra más suave | 2,75 | La Tierra quedó pintada. Los cascos son muy tenues (se ven al ampliar) y la ropa es la de diario, no un traje. Aceptable para un sueño; se anota para el veredicto |

Total: 1,25 en borradores y 13,75 en finales, **15,00**. Revisión: ninguna lámina lleva texto, logotipos, insignias ni banderas. El módulo lunar es una silueta genérica.

![[_lamina_borradores.jpg]]
![[_lamina_finales.jpg]]

## 4. En el motor

`juego/interfaz/ventana_carga.gd`, rehecho con la composición A. Mantiene la interfaz pública (`preparar(meta)`, `mostrar(meta)` y `ocultar()`), la preferencia por `res://interfaz/arte/carga_<id>.jpg`, el tramo, la misión, la ficha con su fuente y su sello, el aviso de escenario provisional y el modo de prueba sin esperas. Sin lámina, dibuja una aguada nocturna con la Luna.

Las láminas entran en `juego/interfaz/arte/carga_<id>.jpg` a 1600 px de ancho, como recursos importados. Las anteriores (lote 07) están guardadas en `antes_arte/`.

## 5. Iteraciones en el motor

| Vuelta | Qué se vio | Qué se cambió |
|---|---|---|
| v1 (`capturas/v1_sendero_carga.png`) | La ficha del cuaderno no aparecía y el objetivo caía al pie: las etiquetas con salto de línea informaban una altura enorme. La estrella del «inicio» tapaba la cabecera | `reset_size()` cada cuadro en las etiquetas con salto. Fuera la estrella |
| v2 (`capturas/v2_*`) | El sello tapaba la línea de la fuente. La cuadrícula pesaba un poco. Texto de la ficha justo para leer | El sello baja 10 px, la cuadrícula pasa al 7 % y el texto de la ficha sube de 17 a 18 px |
| v3 (`capturas/v3_tramo_habitacion_a_ciudad.png`) | El tramo con origen (de la habitación a la plaza) se dibuja como itinerario | — |
| v4 (`capturas/v4_*`) | Mucho aire bajo la lámina. Con la carga mínima de 1,5 s apenas se entintaban dos lunas | La lámina crece a 842 × 474 y las lunas avanzan casi 3 veces más rápido (un ciclo en 2,2 s) |

Antes y después: `capturas/antes_despues_ciudad.jpg` y `capturas/antes_despues_habitacion.jpg`.

![[capturas/antes_despues_ciudad.jpg]]

## 6. Pendiente

- El veredicto de Guillermo sobre la dirección (lámina en el cuaderno) y sobre las cinco láminas.
- En la Luna, decidir si los cascos y el traje deben leerse más (repetir la final costaría 2,75).
- El mapa del mundo (`mapa_mundo.jpg`, lote 07) sigue con el acabado anterior: si se aprueba esta dirección, conviene repintarlo igual.
