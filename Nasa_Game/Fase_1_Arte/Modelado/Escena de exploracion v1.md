# Escena de exploración v1

> **Qué es:** la vista aprobada del sendero ([[Lote 02 - Tipo de juego y personajes]], `ANC_VISTA_JUEGO`), construida en 3D en Godot 4.7.2 con mallas reales. Es el piloto de [[Decision - Modelado 3D]].
> **Pedido de Guillermo (2026-11-12):** «En este momento quiero las mallas listas, y una escena completa… Quiero trabajar contigo y validar si las mallas cumplen mis expectativas.»
> **Estado:** v1 en ajuste contra el ancla (bucle pedido por Guillermo el 2026-11-12). Van 9 iteraciones: el ΔE bajó de 28,0 a 20,6–20,8. El registro y los pendientes están en `pruebas/escena_exploracion/capturas/iteraciones/BUCLE.md`. Espera el veredicto de Guillermo.
> **Cambios principales:**
> - todo el trazado sale de píxeles del ancla (`herramientas/camara_ancla.py`);
> - acabado 2.5D pintado en todos los shaders;
> - sombra moteada bajo el flamboyán;
> - protagonista v2 desde la hoja de giro;
> - antena por script por defecto.

## Cómo verla

Proyecto: `pruebas/escena_exploracion/`. Para abrirla y recorrerla:

```
"C:\Users\guill\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" --path "C:\Users\guill\Desktop\Juego 2d-hd\pruebas\escena_exploracion"
```

| Tecla | Acción |
|---|---|
| 1 / 2 | Personaje al 21 % del alto (como el ancla) o al 12,5 % (como la biblia) |
| I | Activa o quita la inclinación hacia atrás de los objetos |
| A | Cambia la antena entre la versión de Tripo y la versión por script |
| Flechas, rueda | Mueven y acercan la cámara |
| F12 | Guarda una captura en `capturas/` |

## Cómo está hecha

| Parte | Cómo | Archivo |
|---|---|---|
| Protagonista, Órbita, iguana, antena (versión IA) | Tripo H3.1; la textura de la protagonista se proyectó desde su hoja | `Lote_04/`, `pruebas/escena_exploracion/tripo/` |
| Terreno, sendero, arroyo, plaza, rocas, hierba corta | Script (`herramientas/mallas/escena_v1.py`) | `modelos/` |
| Árbol, puente, escalinata, baranda, antena (script), panel, plantas, flores | Scripts de cuatro agentes sobre el núcleo común (`herramientas/mallas/nucleo.py`) | `modelos/` |
| Luz, materiales, cámara | Shaders propios: facetado, follaje con viento, agua, personaje | `shaders/`, `iluminacion.gd`, `escena.gd` |

**Estilo de la biblia, cómo se cumple:**

- facetas planas, cada una con un degradado pintado: es color de vértice por esquina;
- sol cálido y bajo que llega desde el fondo a la derecha, como en el ancla;
- sombra azul petróleo, que pone la luz ambiental;
- borde de luz en las siluetas;
- solo colores de la paleta maestra: el núcleo lo comprueba al cargar.

**Cámara:** 48° de inclinación y 40° de campo de visión, medidos contra el ancla. Los objetos se echan hacia atrás en el shader (`z -= 0,45·y`) para que se lean erguidos, como en la ilustración.

## Mediciones

En la HD 620, con Mobile a 1280×720, sin sincronía vertical, durante 6 s y tras 2 s de calentamiento. Codex usaba Blender en paralelo, así que las cifras son un piso.

| Encuadre | fps medios | ms por cuadro (media / p95) | Primitivas | Llamadas de dibujo |
|---|---:|---:|---:|---:|
| 21 % | 57,6 | 17,4 / 19,7 | 244 599 | 252 |
| 12,5 % | 56,5 | 17,7 / 20,2 | 245 168 | 420 |

La escena tiene 240 recursos y unos 218 000 triángulos únicos, con 28 000 briznas de hierba corta y 170 mechones. Para bajar las llamadas de dibujo, los mechones y las flores pueden pasar a `MultiMeshInstance3D`.

**Mallas de personaje:**

| Malla | Triángulos | Notas |
|---|---:|---|
| Protagonista (Tripo) | 4 930 | Con el script de limpieza de Codex se sacaron niveles exactos de 1 500 y 3 000 en Blender 5.3; a tamaño de juego, el de 1 500 se sostiene |
| Órbita (Tripo) | 2 729 tras soldar | **Con rig y animación, verificada en Godot.** Rigify Cat, 34 huesos DEF, `reposo` (2 s) y `caminar` (1 s) en bucle; en la escena camina junto a la protagonista. `herramientas/blender/rig_gato.py` (Codex) necesitó cinco correcciones mías y una de Codex: los huesos de la copia de exportación nacían con longitud cero y perdían su dirección de descanso. Las patas varían como máximo un 0,64 % de largo |
| Iguana (Tripo) | 2 376 | |
| Antena (Tripo) | 2 305 | Trae fundida la base de hierba de la hoja |

## Pendiente de validar con Guillermo

*(Se completa con la escena terminada.)*
