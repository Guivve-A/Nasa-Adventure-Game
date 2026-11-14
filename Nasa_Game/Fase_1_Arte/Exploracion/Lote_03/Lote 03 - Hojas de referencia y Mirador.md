---
tipo: lote de arte
fase: 1
lote: L03
fecha: 2026-11-12
estado: espera el veredicto de Guillermo
creditos: 30.25
---

# Lote 03 — Hojas de referencia y Mirador del Faro

Responde a dos pedidos de Guillermo del 2026-11-12:

- Diseños de recursos en hojas de referencia, «para que no se pierdan luego» y el juego sea coherente en el tiempo.
- Validar la idea de mirar la Luna por un telescopio con datos de NASA mientras la mascota da datos. La validación está en [[Mirador del Faro - Luna con datos reales]].

## 1. Nueve hojas de referencia: 104 recursos

Cada recurso tiene un ID, como `VEG-01`, que lo une a su hoja, al manifiesto (`manifiesto_recursos.csv`) y al [[Catalogo de recursos]]. Las normas de estilo están en la [[Biblia de arte]].

![[Hojas_v1_lamina.jpg]]

| Hoja | Recursos | Color dentro de la paleta | Revisión ampliada |
|---|---:|---:|---|
| Vegetación | 14 | 91,6 % | Rótulos correctos. El ceibo tiene tronco de botella y algodón, como el real. El guayacán florece sin hojas. |
| Rocas y terreno | 12 | 100 % | Rótulos correctos. Sendero recto y curvo, listos como piezas de kit. |
| Arquitectura | 12 | 100 % | Rótulos correctos. Las casas salieron con teja de barro; el zinc queda como pieza aparte (`ARQ-03`). |
| Plaza y malecón | 12 | 100 % | Rótulos correctos. El kiosco de jugos encaja con Lidia; el puesto de electrónica, con el mercado. |
| Recolectables | 12 | 100 % | Rótulos correctos. Todos llevan el destello cian. |
| Taller de electrónica | 14 | 100 % | Rótulos correctos. El libro, cerrado y con holograma, mantiene el diseño del hub. |
| Fauna | 11 | 100 % | Rótulos correctos. Cada animal con vista lateral y frontal. |
| Reparto | 9 | 96,4 % | Rótulos correctos y alturas medidas en cabezas. Respeta los colores del guion anterior. |
| Mirador del Faro | 8 | 93,3 % | Rótulos correctos. El ocular del telescopio lleva el cian de interacción. |

**Observaciones para decidir**

- **Reparto:** Elena y Lidia tienen siluetas parecidas (redondas, con delantal). Conviene diferenciarlas más.
- **Reparto:** el pantalón del protagonista sigue marrón, como en el lote 02.
- **Arquitectura:** ¿techos de teja, de zinc o mezclados? En Las Peñas hay de ambos.

**Sobre la medición de paleta.** Como control, las direcciones descartadas del lote 01 (gouache y maqueta) también dan 100 %. El indicador detecta desvíos de color, no de estilo: el estilo lo sigue juzgando Guillermo. El centro espacial del lote 02 da 47 % porque usa la paleta fría; cuando se apruebe tendrá su propia paleta maestra.

## 2. Mirador del Faro: dos escenas

### Vista de juego de noche

![[L03_mirador_noche_vista_juego.png]]

- Mantiene la cámara alta aprobada: protagonista al telescopio, gato en la baranda, faro, binoculares, guirnalda, escalinata y casas abajo.
- **A corregir:** salió como atardecer morado, no como noche de luna. Para la noche hay que bajar la luz y enfriarla hacia el azul.
- Color dentro de la paleta: 93,5 %.

### Vista del telescopio con datos reales

![[L03_ui_telescopio_luna.png]]

- Los números de las fichas son los reales de esta noche a las 19:30 desde el Mirador, según JPL Horizons: creciente, 12 %, 403 151 km, 29,6′, 20° de altura y puesta a las 21:05.
- La Luna se ve «sonriente», con el borde iluminado abajo y algo a la derecha, como dicen los datos (193° desde el cenit).
- La Luna de la maqueta la dibujó la IA. En el juego será la textura de NASA, y los rótulos («Terminador», «Luz cenicienta») se colocarán por cálculo.
- Color dentro de la paleta: 53,8 %. Es lo esperado: la Luna es fotográfica y el cielo es de noche.

## Registro del lote

| Encargo | Imágenes | Créditos |
|---|---:|---:|
| `lote_03_hojas.json` (L03a): nueve hojas | 9 | 24,75 |
| `lote_03_mirador.json` (L03b): noche y telescopio | 2 | 5,50 |
| **Total** | **11** | **30,25** |

Todas con GPT Image 2.6, calidad high, 2k y 16:9. Por primera vez se usaron las anclas ya subidas (`@ANC_…`) y los bloques fijos de `bloques_prompt.json`.

## Veredicto de Guillermo

Pendiente.

- [ ] Hojas de referencia (dime los ID que cambiarías):
- [ ] Escena de noche del Mirador:
- [ ] Vista del telescopio:
- [ ] Idea de la Luna con datos de NASA:
