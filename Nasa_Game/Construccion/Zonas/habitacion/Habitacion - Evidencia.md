# Habitación-taller: evidencia de la zona en el motor

> Carril «habitacion» del juego jugable v0 (2026-11-14). Concepto validado: `Fase_1_Arte/Exploracion/Lote_05/L05_A_manana_calida_final.png` (D-018). **La producción en el motor espera la validación de Guillermo con estas capturas.**

## Qué quedó hecho

- `juego/zonas/habitacion/habitacion.gd` (525 líneas) y `zona.json`.
- 29 modelos por script en `juego/modelos/habitacion/` (12 409 triángulos en total), con `herramientas/mallas/habitacion_modelos.py`.
- Cuarto de 6,6 × 5,4 m, girado 20° como en el concepto para que se vean la pared del fondo y la de la derecha.
- Tres estados por banderas: mañana del día 1, noche (`mir_luna` y `mir_linea`, sin `luna_regreso`) y mañana del día 2 (`luna_regreso`).
- Entradas `inicio`, `escalera` y `cama`. Umbral `Escalera` → `ciudad:casa` («A la plaza»), cerrado hasta `hab_seguidor`.
- Siete interactuables: `Cuaderno`, `Seguidor`, `Poster`, `Telescopio`, `Caja`, `Ventana` y `Cama`.
- Banderas que pone: `hab_convocatoria`, `hab_seguidor`, `hab_noche`, `hab_durmio`, `hab_seguidor_v2` y `fin_v0`. Internas: `hab_saludo` y `hab_dia2`.

## Cifras medidas

| Medida | Resultado |
|---|---|
| Prueba `zona:habitacion` | 32 comprobaciones, 0 fallos |
| fps de mañana (HD 620, 1280 × 720, `--medir=5`) | 51,9 de media; p95 de 22,2 ms; 91 llamadas de dibujo |
| fps de noche | 48,0 de media; p95 de 24,0 ms; 96 llamadas de dibujo |
| Carga de la zona | 0,6 s sin ventana; de 1,4 a 2,5 s con ventana |
| Marca del descanso | 0,85 m despejados alrededor (lo mide la prueba); entrada `escalera` a 1,3 m |

## Capturas (todas miradas)

- ![[hab_manana.png]]
- ![[hab_noche.png]]
- ![[hab_descanso.png]]
- ![[hab_dia2.png]]
- Lámina concepto / motor: ![[lamina_concepto_vs_motor.jpg]]
- Los cuatro estados juntos: ![[lamina_estados.jpg]]

## Diferencias con el concepto

1. **Cámara.** El concepto es más cercano y más girado; en el motor se usa la cámara fija aprobada (48°, campo de 40°) con encuadre 0,20. Se ve más suelo y menos pared.
2. **Rayos de sol.** El concepto tiene haces con volumen; en el motor son tres franjas pintadas en el suelo.
3. **Buganvilla.** Flores magenta en el concepto; coral en el motor, porque la paleta maestra no tiene magenta. Las hojas salen más amarillas.
4. **Órbita.** En el concepto está sentado en el alféizar; en el motor sigue a la protagonista.
5. **Paredes.** Revoque con manchas y ladrillo visto en el concepto; degradado liso con zócalo en el motor.
6. **Cama.** Más grande y con sábanas más blancas en el concepto; va con la cabecera contra la pared izquierda.
7. **Banco.** El seguidor, la placa y las cajas de debajo son más grandes y detallados en el concepto.
8. **Descanso.** En el concepto queda abajo a la derecha, con el farol del frente a la vista; en el motor queda a la derecha y el farol del frente sale del cuadro cuando la cámara está centrada. La marca cian del núcleo (1,5 m) es mayor que la del concepto.
9. **Follaje en primer plano.** Verde oscuro y desenfocado en el concepto; plantas VEG-07, VEG-10 y VEG-12 en tonos oliva más una viñeta azul petróleo en las esquinas.
10. **Barrio por la ventana.** Escalinata y seis casas simples; el concepto muestra un barrio frondoso.

## IDs nuevos

- Taller: `TAL-15` seguidor lunar, `TAL-16` cuaderno abierto y `TAL-17` vaso con lápices.
- Habitación: `HAB-01` cama, `HAB-02` ventana con postigos, `HAB-03` alfombra, `HAB-04` repisa, `HAB-05` póster del observatorio, `HAB-06` caja de cartón, `HAB-07` baranda con puerta, `HAB-08` felpudo, `HAB-09` escalera con arco, `HAB-10` esfera armilar, `HAB-11` farol, `HAB-12` paredes y suelo, `HAB-12n` el cuarto de noche (sin haces de sol), `HAB-13` barrio de fuera, `HAB-14` buganvilla, `HAB-15` maceta colgante, `HAB-16` macetero y `HAB-17` cuadrito.
- Del catálogo, por script: `TAL-01`, `TAL-02`, `TAL-06`, `TAL-07`, `TAL-09`, `TAL-10`, `TAL-12` y `TAL-14`.
- Reutilizados de `modelos/entorno`: `VEG-07`, `VEG-10` y `VEG-12`.

## Lo que se resolvió dentro del carril (para el integrador)

- **El emisivo del núcleo no se inclina.** La traza del osciloscopio (a 1 m de alto) quedaba flotando 0,44 m delante. La zona cambia ese material por un shader propio de brillo que aplica la misma inclinación (`CODIGO_BRILLO` en `habitacion.gd`). Convendría llevarlo al núcleo.
- **Los faroles nunca caen a cero.** En `luz_pintada()` la regla «las sombras conservan el 30 %» también se aplica a la atenuación por distancia de las luces puntuales: cada `farol()` suma el 30 % de su energía a toda malla que toca, a cualquier distancia. Con tres faroles a 0,9 la noche parecía de día. Aquí van a 0,6 o 0,7, con `light_cull_mask = 1`, y el barrio (HAB-13) en la capa 2. Afecta a cualquier zona de noche.
- **Luz.** `interior_manana` e `interior_noche` son provisionales en el núcleo; la zona las ajusta con `cambios` (mañana: saturación 0,96, contraste 1,14, ambiente `94808a` a 0,60; noche: sol a 0,16, ambiente `3f4c68` a 0,62, exposición 0,86).

## Queda pendiente

- Validación de Guillermo de las cuatro capturas (producción en el motor).
- Las rutas de prueba de la noche y del día 2 están escritas, pero la prueba `zona:` solo recorre el estado por defecto (día 1). Los dos estados se cargaron con ventana sin errores; sus recorridos los ejercita `--prueba=recorrido`.
- Órbita sentado en el alféizar al empezar el día 1 (hoy sigue a la protagonista).
- La cama lleva a `luna:inicio`; depende de que exista la zona `luna`.
- `TAL-03`, `TAL-04`, `TAL-05`, `TAL-08`, `TAL-11` y `TAL-13` no están modelados: no aparecen en el concepto.
- Más detalle pintado en paredes (manchas de revoque) y un barrio más frondoso por la ventana, si Guillermo lo pide.
