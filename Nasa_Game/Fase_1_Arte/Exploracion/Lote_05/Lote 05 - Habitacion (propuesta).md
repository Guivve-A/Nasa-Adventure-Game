---
tipo: lote de arte
fase: 1
lote: L05
fecha: 2026-11-12
estado: propuesta · solo cotizado, espera la aprobación de Guillermo
creditos: 0
decisiones: D-013, D-015, D-016
---

# Lote 05: Habitación-taller (propuesta)

## 1. Qué pidió Guillermo

- **D-016:** el concepto actual de la Habitación (`ANC_HUB`) no sirve. Fallan la cámara, la distribución, el ambiente y el encaje con la historia. Pidió «algo más cercano a juegos típicos, 2d hd».
- **D-015:** el acabado 2.5D pintado de la escena del sendero es el estilo de todo el juego.
- La Habitación es el escenario 1 de la historia ([[Fase 2 - Analisis]], escenas 1.1, 1.2, 2.5, 3.6, 4.1 y 4.3). Es el tutorial: despertar con Órbita, el rompecabezas del seguidor con el osciloscopio, la cama desde la que sueña con la Luna, el telescopio, el cuaderno, la caja de cartón de Rafael y la escalera hacia la casa. Debe verse de mañana y de noche.

## 2. Qué cambia frente a `ANC_HUB`

| | `ANC_HUB` (lote 01) | Lote 05 |
|---|---|---|
| Cámara | Diorama de costado, con horizonte y cielo | La vista superior 3/4 de D-013 (bloque `{CAMARA_JUEGO}`): sin horizonte y con el suelo llenando el cuadro |
| Escala | Protagonista a más de la mitad del alto (unos 480 de 905 px) | Personaje pequeño, a la escala de la exploración |
| Ancla de estilo | `@ANC_HUB` | `@ANC_VISTA_JUEGO`, `@ANC_PROTA_1` y `@ANC_GATO`. `ANC_HUB` no se pasa, para no arrastrar su cámara |
| Acabado | Ilustración plana | 2D-HD: desenfoque suave en los bordes (tilt-shift), haces de luz con polvo, brillo y viñeta sutiles |
| Historia | Holograma genérico y faro al fondo | Seguidor de la Luna en el banco, osciloscopio, cama con la caja de cartón, telescopio, cuaderno y salida hacia la casa |
| Paredes | Pared frontal abierta, vista lateral | Techo y paredes cercanas quitados; solo quedan las dos del fondo. En E, todas cortadas a media altura |

Se toman principios de los 2D-HD típicos: desenfoque de profundidad, luz volumétrica y lectura clara del recorrido. No se copia ningún juego, personaje ni producto. Sin texto, logotipos ni insignias de la NASA: el póster del observatorio va sin texto.

## 3. Borradores

Seis direcciones con GPT Image 2.6, calidad baja, 1k y 16:9. Todas con la cámara de D-013 y los mismos objetos de la historia. Cada encargo termina con `{ESTILO} {SIN_TEXTO}`. Lote: `lote_05_habitacion.json`.

| ID | Dirección | Luz | Qué resuelve |
|---|---|---|---|
| `L05_A_manana_calida` | Cuarto clásico: cama al fondo a la izquierda, banco con el seguidor a la derecha y escalera en el piso | Amanecer cálido con haces | Escena 1.1 (despertar) y la luz de mañana |
| `L05_B_noche_luna` | Antes de dormir: Luna creciente por la ventana, cama con borde cian y caja de cartón | Luna fría, lámpara y guirnalda cálidas | Escena 2.5 y el paso al sueño; prueba la luz de noche de la biblia |
| `L05_C_azotea_terraza` | Cuarto en la azotea; el seguidor está en la terraza, apuntando al cielo | Tarde, la luz base | Un taller con cielo para probar el seguidor (1.2 y 4.1) y el barrio visible desde arriba |
| `L05_D_cama_alta` | Cuarto compacto con cama alta y el taller debajo | Tarde por persianas y lámpara | Un espacio pequeño y denso, creíble en una casa de Las Escalinatas |
| `L05_E_casa_munecas` | Corte de casa de muñecas: paredes a media altura, pasillo y escalera a la cocina | Mañana | Une la Habitación con la casa (1b) en una sola lectura |
| `L05_F_recorrido_tutorial` | Distribución en L, pensada como primer cuarto jugable: cama → ventana y telescopio → seguidor → puerta | Tarde dorada | Lectura del tutorial: 5 objetos interactivos separados y marcados con destello cian |

**Ojo con la escala:** `{CAMARA_JUEGO}` pide al personaje a un octavo del alto (12,5 %). En `ANC_VISTA_JUEGO` mide el 20,9 %. Al llegar los borradores se mide la altura del personaje en cada uno.

## 4. Costo cotizado

Salida de `python -I herramientas/hf_generar.py <lote> --solo-cotizar` (no crea trabajos ni gasta):

```
  cotizado L05_A_manana_calida                  gpt_image_2_6          0.25
  cotizado L05_B_noche_luna                     gpt_image_2_6          0.25
  cotizado L05_C_azotea_terraza                 gpt_image_2_6          0.25
  cotizado L05_D_cama_alta                      gpt_image_2_6          0.25
  cotizado L05_E_casa_munecas                   gpt_image_2_6          0.25
  cotizado L05_F_recorrido_tutorial             gpt_image_2_6          0.25
Total cotizado: 1.50 creditos (tope del lote: 2)
```

Versión final: el mismo encargo en calidad alta y 2k cotiza **2,75 créditos** para cualquiera de las seis direcciones (las seis se cotizaron en esa calidad; total 16,50 si se hicieran todas, que no es la propuesta).

| Partida | Créditos |
|---|---:|
| 6 borradores (calidad baja, 1k) | 1,50 |
| Versión final del concepto elegido (calidad alta, 2k) | 2,75 |
| **Seguro** | **4,25** |
| Una ronda de corrección de hasta 6 borradores | 1,50 |
| Segunda versión final del mismo cuarto con la otra luz (mañana o noche) | 2,75 |
| **Tope propuesto** | **8,50** |

Saldo actual: **889,50 créditos** (comprobado con `higgsfield account status` tras el lote 04c). El tope es el 0,96 % de ese saldo.

**Corrección posterior al verificador (2026-11-12).** Nueva cotización: 1,50, igual que antes.
- Se quitó «diorama» de los seis encargos, porque Guillermo rechazó el diorama de costado. Queda solo el desenfoque tilt-shift.
- La azotea (C) ya tiene ventana.
- En la noche (B), la Luna se ve por su haz de luz y su reflejo en el vidrio, porque la cámara de juego no ve el cielo.
- Todos piden la luz pintada de D-015, con la sombra suave y de color, nunca negra.

## 5. Lo que no se hará hasta que Guillermo apruebe

- No se genera ningún borrador: el lote solo está cotizado.
- No se genera la versión final en calidad alta hasta que elija un borrador.
- No se sube ninguna ancla nueva ni se reemplaza `ANC_HUB` en `anclas.json`.
- No se cambia la sección 5 de la [[Biblia de arte]] («Hub e interiores: diorama lateral»), que contradice D-016. Al aprobar, pasará a la vista de D-013.
- No se crean bloques nuevos en `bloques_prompt.json`. Propuesta para después: un bloque `ACABADO_2DHD` con el texto del acabado, que hoy se repite en los seis encargos.
- No se rehace la hoja de props `HR_TAL_v1`, que sigue sin aprobar.
- No se modela nada en 3D ni se construye la Habitación en Godot.

## 6. Para decidir

1. ¿Se aprueba la partida: 4,25 seguros y tope de 8,50?
2. ¿Se quita o se cambia alguna de las seis direcciones antes de generar?
