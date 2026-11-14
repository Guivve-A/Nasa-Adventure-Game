---
tipo: biblia de arte
version: v0.1
fecha: 2026-11-12
estado: borrador · se amplía con cada veredicto de Guillermo
decisiones: D-011, D-012, D-013
---

# Biblia de arte · v0.1

Reglas para que todo el juego se vea igual en el tiempo. Nace de las tres imágenes que aprobó Guillermo. Cada recurso nuevo se compara contra esta página antes de mostrarse.

## 1. Anclas de estilo

Son las imágenes aprobadas. Se pasan como referencia en cada encargo; están subidas a Higgsfield y sus identificadores están en `anclas.json`.

| Ancla | Qué fija | Decisión |
|---|---|---|
| ![[L01_A_lowpoly_hub_gpt26.png\|300]] `ANC_HUB` | Estilo de interiores y del hub lateral | D-011 |
| ![[L01_A_lowpoly_exploracion_gpt26.png\|300]] `ANC_EXPLORACION` | Estilo de los exteriores | D-011 |
| ![[L02_exploracion_camara_alta.png\|300]] `ANC_VISTA_JUEGO` | Cámara y acabado de la exploración | D-013 |

Referencias de diseño, sin veredicto todavía: `ANC_PROTA_1`, `ANC_PROTA_2`, `ANC_GATO` y `ANC_MAPA` (lote 02).

## 2. Cinco pilares visuales

1. **Low-poly pintado a mano.** Facetas planas y nítidas, cada una con un degradado pintado. Sin texturas fotográficas.
2. **Luz cálida, sombra fría.** Luz principal cálida, sombra azul petróleo, borde de luz (rim) en las siluetas.
3. **La silueta primero.** Formas gruesas y simples que se lean a un octavo de la pantalla.
4. **El cian es la tecnología.** Se reserva para datos, hologramas, interacción y recolectables. Ningún otro objeto lo usa.
5. **Guayaquil vivo.** Vegetación tropical, fauna, cables, ropa tendida, techos de zinc y escalinatas.

## 3. Paleta maestra (medida)

Medida con `herramientas/paleta.py` sobre las tres anclas: 16 colores por k-means, más el cian del holograma.

![[paleta_maestra.png]]

| Papel | Colores |
|---|---|
| Luz cálida | `#F8C991` crema · `#F4A159` naranja de sol · `#DAAA25` dorado |
| Tierra, muros y terracota | `#D09880` · `#AF795E` · `#924930` · acento coral `#E46043` |
| Vegetación | `#A48A29` hierba al sol · `#6D6A2B` hierba en sombra |
| Maderas | `#836258` · `#583F22` |
| Sombra fría y piedra | `#516B7C` azul petróleo · `#4B4E47` · `#998385` · `#B8BBC6` |
| Lo más oscuro | `#322C1D`, nunca negro puro |
| Tecnología y datos | `#62E4E0` cian · `#36B1B2` cian medio · `#CEF8F5` brillo |

**Comprobación automática:** `python herramientas/paleta.py comparar <imagen>` mide qué parte del color de un recurso nuevo cae cerca de esta paleta. Es un indicador para detectar desvíos, no un veredicto. El resultado de cada hoja aparece en [[Catalogo de recursos]].

**Calibración (2026-11-12):** las anclas dan del 99 al 100 %, y las direcciones descartadas del lote 01 (gouache y maqueta) también dan 100 %. El indicador detecta desvíos de color, no de estilo. El centro espacial da 47 % porque usa la paleta fría: necesitará su propia paleta maestra cuando se apruebe.

**Excepción:** la Luna, los planetas y las imágenes de satélite del telescopio usan datos reales de NASA. Son fotográficos a propósito, dentro de un marco de interfaz que sí sigue la paleta.

## 4. Proporciones

- Estudiantes: 3 cabezas. Adultos: unas 3,5 cabezas.
- El gato llega más o menos a la rodilla del protagonista.
- Toda hoja de objetos lleva la silueta gris del estudiante como escala.

## 5. Cámaras

- **Exploración:** cámara alta fija, a unos 60° hacia abajo, sin horizonte ni cielo. El personaje ocupa un octavo del alto de la pantalla. Ancla: `ANC_VISTA_JUEGO`.
- **Hub e interiores:** diorama lateral en corte, con capas de primer plano y fondo. Ancla: `ANC_HUB`.
- **Telescopio:** vista de ocular a pantalla completa. Ver [[Mirador del Faro - Luna con datos reales]].

## 6. Interfaz

Cuaderno de ingeniería: papel milimetrado crema, tinta, papel rasgado, garabatos de circuitos y acentos azul petróleo y cian. Ancla: `ANC_MAPA`. En el juego, el texto se compone en el motor para poder traducirlo.

## 7. Luz por momento del día

| Momento | Luz principal | Sombras | Prácticas |
|---|---|---|---|
| Tarde, la luz base | Sol cálido y bajo | Azul petróleo | — |
| Noche | Luna azul fría | Azul profundo | Faroles, ventanas y guirnaldas cálidas |
| Centro espacial | Blanco frío | Azul y gris titanio | Dorado y cian |

## 8. Hacer y evitar

| Hacer | Evitar |
|---|---|
| Facetas visibles con degradado pintado | Texturas fotográficas, salvo los datos reales de NASA |
| Materiales mates; brillos pequeños solo en metal | Reflejos de espejo y plástico brillante |
| Silueta clara y pocas piezas | Ruido de detalle que no se lee a escala de juego |
| Cian solo para tecnología e interacción | Cian en ropa, flores o decoración |
| Diseños propios inspirados en Guayaquil | Logotipos, marcas, insignias de NASA y diseños de otros juegos |

## 9. Cómo nace un recurso

1. **Ficha.** Darle un ID con su prefijo de categoría, como `VEG-15`, y añadirlo a un encargo de hoja.
2. **Encargo.** Usar los bloques fijos de `bloques_prompt.json` (`{ESTILO}`, `{HOJA}`, `{ROTULOS}`…) y pasar las anclas como referencia (`@ANC_HUB`).
3. **Generación.** Con `herramientas/hf_generar.py`, que cotiza, respeta el tope del lote, descarga el original y registra todo.
4. **Control.** Medir la paleta y revisar la hoja ampliada: manos, rótulos y objetos.
5. **Veredicto.** Guillermo aprueba o pide cambios. El estado va a `veredictos.json`.
6. **Catálogo.** `python herramientas/manifiesto.py` actualiza `manifiesto_recursos.csv` y [[Catalogo de recursos]].
7. **Versiones.** Un cambio crea `v2`; la `v1` no se borra.

## 10. Bloques fijos de los encargos (v1)

Están en `bloques_prompt.json` y no se editan: un cambio crea un bloque nuevo, como `ESTILO_V2`, y se anota aquí.

| Bloque | Para qué sirve |
|---|---|
| `ESTILO` | El estilo low-poly pintado, la luz y la paleta |
| `HOJA` | Fondo, luz neutra, cuadrícula y silueta de escala de las hojas |
| `ROTULOS` | Rótulos en español bajo cada objeto |
| `CAMARA_JUEGO` | La cámara alta aprobada |
| `PROTAGONISTA` y `GATO` | La descripción fija de los dos personajes |
| `SIN_TEXTO` | Imágenes sin texto ni logotipos |
