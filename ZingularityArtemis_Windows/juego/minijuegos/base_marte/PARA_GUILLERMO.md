# Base en Marte — integración en Zingularity: Artemis

Hecho por Domenica (carril `minijuegos/base_marte/`). El libro «Base en Marte» de la biblioteca del pueblo ya abre este minijuego:
`ciudad.gd` llama a `Interfaz.abrir_minijuego("base_marte")` y, al superarlo, pone `base_marte_hecha`. **No hace falta tocar el núcleo para que funcione.**

## Qué es
El capítulo 2D de Marte (pixel art, 640 × 360 ampliado ×2 a pantalla completa con una SubViewport):
aterrizaje programable (siete minutos de terror), el equipo baja de la nave, banderas, base (hábitat, paneles,
extractor de oxígeno, taladro de hielo, invernadero), del día al atardecer, tormenta de polvo, noche y reporte a la Tierra.
Trae su HUD, su cuaderno de campo (11 notas con fuente) y a Órbita con traje espacial.

- `base_marte.gd` envuelve el capítulo (`pantalla_completa = true`), termina con `terminar(true, puntos, detalle)` y tiene `jugar_solo()`.
- Esc es del anfitrión (sale del libro). Tab abre el cuaderno de Marte. Ratón: flechas del aterrizaje y botones X.
- El capítulo pausa solo su propio nodo: nunca toca `get_tree().paused`.
- Las imágenes se cargan aunque no estén importadas (`codigo/textura.gd`), así que funciona con la caché `.godot` actual.

## Pruebas (pasan)
```
--prueba=minijuego:base_marte --ritmo=8                                   13/13
--prueba=guion:res://minijuegos/base_marte/prueba_manos.gd --ritmo=2      13/13  (teclas y clics físicos)
--prueba=nucleo --ritmo=8                                                  24/24
```

## Cambios en el núcleo — APLICADOS el 15-11-2026 con autorización de Guillermo
Los cinco puntos ya están hechos en este paquete. El bloqueo de Marte (punto 2) se activa solo cuando exista `minijuegos/base_luna/base_luna.gd`.

1. **Texto de la misión** (`datos/misiones.json`, paso `base_marte_hecha`): ya no hay contador de soles.
```json
"texto": "Abre el libro de Marte: aterriza, levanta la base y llama a la Tierra",
"pistas": [
  "Órbita mira los cuatro medidores y el cielo.",
  "Nada funciona sin energía: primero los paneles; el invernadero necesita el agua del hielo.",
  "Paracaídas a 11 km, cohetes a 2,1 km y navegación: sí. Limpia los paneles en la tormenta."
]
```
2. **Marte después de la Luna** (`zonas/ciudad/ciudad.gd`, en `_usar_biblioteca()`, justo después de `var reto: String = ...`). Aplicarlo solo cuando `base_luna` exista; si no, Marte quedaría bloqueado.
```gdscript
	if reto == "base_marte" and not Juego.bandera("base_luna_hecha"):
		await Interfaz.decir([{"quien": "Órbita", "texto": "Primero la Luna: allá se construye el cohete que nos lleva a Marte."}])
		return
```
3. **Notas de Marte en el cuaderno del juego**: pegar las 11 fichas de `fichas_marte_para_datos_espaciales.json` dentro de `"fichas"` en `datos/datos_espaciales.json`. `base_marte.gd` ya las anota solo cuando existen. Filas para `datos/FUENTES.md`:

| Id | Sello | Fila de verificación | Documento | Cita textual corta |
|---|---|---|---|---|
| `marte_senal` | Dato verificado | Base en Marte, cuaderno | ESA, «Spacecraft event time vs. Earth receive time» (2012) | — |
| `marte_siete` | Dato verificado | Base en Marte, cuaderno | NASA, Mars 2020: Entry, Descent and Landing (2021) | — |
| `marte_gravedad` | Dato verificado | Base en Marte, cuaderno | NASA/JPL, «Mars at a Glance» | — |
| `marte_sol` | Dato verificado | Base en Marte, cuaderno | NASA, Mars Fact Sheet (NSSDCA) | — |
| `marte_aire` | Dato verificado | Base en Marte, cuaderno | NASA, Mars Fact Sheet (NSSDCA) | — |
| `marte_moxie` | Dato verificado | Base en Marte, cuaderno | NASA/JPL, «MOXIE Completes Mars Mission» (2023) | — |
| `marte_hielo` | Dato verificado | Base en Marte, cuaderno | NASA/JPL, «NASA's Treasure Map for Water Ice on Mars» (2019) | — |
| `marte_polvo` | Dato verificado | Base en Marte, cuaderno | NASA, «Opportunity Rover Mission on Mars Comes to End» (2019) | — |
| `marte_frio` | Dato verificado | Base en Marte, cuaderno | NASA, Mars Fact Sheet (NSSDCA) | — |
| `marte_lunas` | Dato verificado | Base en Marte, cuaderno | NASA Science, «Phobos» y «Deimos» | — |
| `marte_unidades` | Dato verificado | Base en Marte, cuaderno | NASA, informe de la junta de investigación de la Mars Climate Orbiter (1999) | — |

4. **Nombre del juego**: `config/name="Zingularity: Artemis"` en `project.godot`, y el título en `LEEME.txt`, `Instalar.cmd` (acceso directo) y los `.cmd`.
5. **Quitar el extra viejo**: `extras/mision_artemis_marte` y su `.cmd` ya no hacen falta (es la v1; la versión buena está dentro del libro).
