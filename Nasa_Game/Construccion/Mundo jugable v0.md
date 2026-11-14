# Mundo jugable v0

> Registro de la construcción del juego jugable (`juego/`). Orden de Guillermo del 2026-11-13: «USA TODAS TUS CAPACIDADES PARA EMPEZAR A CONSTRUIR EL MUNDO COMPLETO. Quiero empezar a jugar y ver los minijuegos, asimismo, que el juego se vaya enfocando en aspectos espaciales también.»
>
> El contrato técnico está en `juego/ARQUITECTURA.md`. Las decisiones, en [[Memory]] (D-018 y D-019). El avance, en [[trabajos]].

## Cómo se juega

- Doble clic en `juego/jugar.cmd`.
- Controles: WASD o flechas para moverse, Mayús para correr, E para interactuar, Espacio para saltar (en la Luna), Tab para el cuaderno, Esc para la pausa, Z y X para acercar y alejar, F11 pantalla completa y F12 captura.
- Menú: **Nueva partida**, **Minijuegos** (cada reto suelto) y **Lugares** (cada escenario por separado, para validarlo).

## Qué está validado y qué es provisional

| Parte | Base de arte | Estado |
|---|---|---|
| Estilo en el motor (shaders, luz de la tarde, cámara) | D-013 y D-015 | **Aprobado.** Portado sin cambios |
| Protagonista | D-017 (v8T) con el bolso v9 | Aprobada; el bolso v9 espera el visto bueno |
| Órbita | Hoja del lote 02 y rig propio | Hoja sin veredicto |
| Habitación | Concepto A elegido (D-018) | Concepto validado; la producción en el motor se valida con capturas |
| Sendero | Escena aprobada (D-015) | Aprobado; la ampliación jugable se valida |
| Plaza con biblioteca | Hojas `HR_URB` y `HR_ARQ`, sin concepto | **Provisional** |
| Mirador | Concepto L03 y hoja `HR_MIR`, sin veredicto | **Provisional** |
| Luna del sueño | Sin concepto (lote 06 por aprobar) | **Provisional** |
| Base espacial | Sin concepto; diseño en [[Base espacial - Diseno]] | **Provisional** |
| Interfaz (menús, cuaderno, ventana de carga) | Biblia de arte, sección 6 | **Provisional** (Fase 7 sin validar) |
| Sonido | Pitidos generados por código | **Provisional** (Fase 4 sin hacer) |
| Luces de mañana, noche, interior y Luna | Tabla de la biblia, sección 7 | **Provisionales** |

Lo provisional se avisa dentro del juego: en la ventana de carga y en el menú «Lugares».

## El mundo

```
[Habitación] ─escalera─ [Plaza de las Iguanas] ─camino del cerro─ [Sendero del arroyo] ─ [Mirador del Faro]
     │                         │                                                              │
     │ cama (de noche)         │ biblioteca                                    atajo de los faroles
     ▼                         ▼                                                              │
[Luna del sueño]        [Base Chakana]  ◄── también desde el menú «Minijuegos»                └──► [Habitación]
```

Ruta principal (`juego/datos/misiones.json`): la convocatoria y el seguidor (habitación) → la plaza → el panel y la antena (sendero) → la maqueta de Pegaso, la Luna por el telescopio y la línea de tiempo (mirador) → dormir → la Luna del sueño (saltos, muestras, la foto con la etapa de descenso, las dos banderas y el regreso) → el seguidor con prealimentación → fin del prototipo. Misión secundaria: «Tu primera base espacial».

## Carriles y quién los hizo

| Carril | Qué entrega | Quién | Verificación |
|---|---|---|---|
| Núcleo y contrato | `juego/nucleo`, `juego/interfaz`, `juego/pruebas`, `ARQUITECTURA.md` | Claude (integrador) | Prueba `nucleo`: 16 de 16; capturas revisadas |
| Fichas del cuaderno | `juego/datos/datos_espaciales.json` (55) | Codex | Verificador escéptico (pendiente) |
| Rig de la protagonista | `juego/modelos/personajes/PER-01_rig.glb` | Flujo `rig-y-conceptos` | Verificador escéptico |
| Lote 06 de conceptos | `Fase_1_Arte/Exploracion/Lote_06/` (solo cotizado) | Flujo `rig-y-conceptos` | Verificador escéptico |
| Habitación y Plaza | `juego/zonas/habitacion`, `juego/zonas/ciudad` | Flujo `construir-mundo` (zonas1) | Verificador escéptico por zona |
| Sendero y Mirador | `juego/zonas/sendero`, `juego/zonas/mirador` | Flujo `construir-mundo` (zonas2) | Verificador escéptico por zona |
| Base espacial | `juego/base`, `juego/zonas/base` | Flujo `construir-mundo` (base): datos, simulación, mundo, interfaz e integración | Verificador por carril y uno final |
| Minijuegos de control | `seguidor`, `antena`, `satelite` | Flujo `construir-mundo` (mini1) | Verificador escéptico por minijuego |
| Minijuegos | `linea_tiempo`, `orbita`, `regreso` | Codex | Verificador escéptico (pendiente) |
| Luna del sueño | `juego/zonas/luna` | Flujo `construir-mundo` (zonas3), por lanzar | — |
| Minijuegos | `telescopio`, `muestras`, `banderas` | Flujo `construir-mundo` (mini2), por lanzar | — |

## Pruebas

```
python -I herramientas/juego_ejecutar.py -- --prueba=nucleo --ritmo=6
python -I herramientas/juego_ejecutar.py -- --prueba=zonas --ritmo=6
python -I herramientas/juego_ejecutar.py -- --prueba=minijuegos --ritmo=8
python -I herramientas/juego_ejecutar.py -- --prueba=recorrido --ritmo=6
```

`recorrido` juega la historia de punta a punta con el piloto automático.

## Estado

Se actualiza al cerrar cada carril: ver la sección «Hecho» de [[trabajos]].
