# Misión Artemis — Marte (sección de Doménica)

Proyecto de Godot 4.7 solo con el capítulo de Marte. Usa el mismo motor, resolución (640×360), HUD, barras y personaje que *Misión Artemis*.

## Cómo jugar
Abre `project.godot` en Godot 4.7 y pulsa F5.
- ← → / A D: moverse · Espacio: saltar · E: usar / mantener: desplegar · Tab o clic en la libreta: cuaderno de campo · F11: pantalla completa

## Qué pasa en el capítulo
1. **Siete minutos de terror.** La señal tarda demasiado para pilotear en vivo: se programan el paracaídas, los cohetes y la navegación por terreno, y se prueba en el simulador. Puede terminar en aterrizaje suave, aterrizaje duro o «la nave se perdería», y siempre se explica la causa. Se ajusta el programa y se repite, sin muertes.
2. **Banderas:** Estados Unidos, Ecuador, IEEE IAS — ESPOL.
3. **Base:** hábitat, paneles, extractor de oxígeno (necesita paneles), taladro de hielo (necesita paneles) e invernadero (necesita agua del taladro). Con el trabajo, el día pasa a atardecer.
4. **Tormenta de polvo** al atardecer: hay que limpiar los paneles.
5. **Noche:** frío, Fobos y Deimos. Se levanta la antena, se corrige la unidad equivocada del reporte y se envía a la Tierra.

Cada descubrimiento se guarda en el **cuaderno de campo** (11 páginas). Cada página trae un dato real con su fuente. Las cifras del juego que no son reales (velocidades del simulador, ritmo de las barras) siguen un modelo simplificado.

## Pasarlo al proyecto del equipo
Copia sobre *Misión Artemis*:
- `codigo/nivel_marte.gd` (reemplaza al provisional; misma señal `terminado`), `codigo/aterrizaje.gd`, `codigo/cuaderno.gd`, `codigo/fondo_marte.gd`
- `datos/marte.json`
- `recursos/fondos_marte/` (día, atardecer y noche), `recursos/nivel/suelo_marte_*.png`, `recursos/props/extractor.png` y `taladro.png`

`principal.gd` del equipo no cambia. Hay que actualizar la parte de Marte de su `--prueba`, porque usaba `m.puntos`. Puede guiarse con la de este proyecto.

## Prueba automática
`godot --path . -- --prueba --capturas=<carpeta>` juega todo solo y guarda capturas. Resultado actual: 36 de 36.
`-- --capitulo=superficie` empieza ya aterrizado.

## Arte
Fondos, suelo y props nuevos están dibujados por código (`herramientas/`, Python + Pillow). No usan logos ni imágenes de la NASA. Guillermo valida el arte con las capturas.
