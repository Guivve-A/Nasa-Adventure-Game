# Bucle: protagonista parecida a su hoja de referencia

Pedido de Guillermo (2026-11-12): «/loop Hacer que el personaje principal se parezca en gran medida, 80 % o más, al del reference sheet».

**Hoja de referencia:** `Nasa_Game/Fase_1_Arte/Exploracion/Lote_02/L02_protagonista_tipo1_hoja.png` (frente, 3/4, perfil, espalda y cuatro expresiones).

**Meta:** parecido total ≥ 80 % con `herramientas/comparar_personaje.py`, y que Guillermo lo confirme a la vista.

## Métrica

Se compara la hoja con un render sin luz de la malla (`herramientas/blender/render_vistas.py`), vista por vista:

- **Silueta:** IoU de las dos siluetas.
- **Color:** 1 − ΔE medio / 40, con las imágenes suavizadas.
- **Estructura:** SSIM de la luminancia a 1/2 y 1/4 de escala.

Parecido de una vista = 0,4 × silueta + 0,3 × color + 0,3 × estructura. El total pondera doble el frente y la cabeza (el 36 % de arriba del frente).

- Spec: `spec_v2.json` (malla v2) y `spec_v3_bolso.json`; cambian las rutas de render.
- Cajas de la hoja: frente [200, 10, 720, 923], perfil [1410, 10, 1790, 923], espalda [1960, 10, 2450, 923].
- Con la malla mirando a +X: `px_cuerpo` es el frente, `my_cuerpo` el perfil derecho y `mx_cuerpo` la espalda.

## Registro (`parecido.jsonl`)

| Versión | Cambio | Total | Frente | Cabeza | Perfil | Espalda |
|---|---|---:|---:|---:|---:|---:|
| v2 | Lote 04c (Tripo desde la hoja de giro), sin bolso | 62,2 | 59,4 | 59,3 | 66,6 | 69,2 |
| v3_bolso | v2 + bolso y correa por script (`herramientas/blender/accesorio_bolso.py`) | 61,0 | 59,6 | 59,3 | 58,9 | 69,3 |
| v3_hoja | Codex: hoja proyectada sobre la textura (`herramientas/mallas/proyectar_hoja.py`): una alineación por vista, pesos (n·d)³ y 0,15 de la textura original. Verificado con medición propia. Deja trazos dobles en la cara y una costura de dos tonos | 64,9 | 61,5 | 60,1 | 71,5 | 74,8 |

**Métrica v2 (con registro).** La métrica v1 centraba cada figura en su caja, y la caja de la hoja incluye el bolso, que sobresale a un lado. Así comparaba el render corrido 8 px en el frente y 11 px en la cabeza.

La v2 (`--registro`) alinea el render con la hoja buscando la mejor silueta: escala ±4 % y desplazamiento ±24 px. Es el registro estándar entre imágenes.

Las cifras de arriba son de la v1 (la que usan los agentes del flujo). Con la v2:

| Versión | Total | Frente | Cabeza | Perfil | Espalda |
|---|---:|---:|---:|---:|---:|
| v2 | 68,2 | 68,0 | 65,9 | 69,5 | 72,1 |
| v3_bolso | 67,6 | 68,3 | 65,8 | 65,2 | 72,3 |
| **v3_hoja** | **73,7** | 75,9 | 67,2 | 76,4 | 79,7 |

En v3_hoja, la cabeza es lo más débil: color 61,6 y estructura 34,6. Con la hoja ya proyectada, lo que queda es el borde naranja del pelo, que cae en superficies oblicuas donde la vista frontal pesa poco por el (n·d)³.

**Resultados de la vuelta 2.** El flujo `wf_cb5b1503-94b` (8 agentes) probó cuatro enfoques sobre la geometría v2:

| Enfoque | Métrica v1 | Métrica v2 | Verificador |
|---|---:|---:|---|
| A: bandas y mezcla dominante | 67,9 | 74,3 | No confirmado: cuña negra en la mandíbula de perfil, rasgos del frente rasantes |
| B: deformación 2D | 63,7 | 73,3 | No confirmado: no mejora, estiramientos en el costado |
| C: cara con registro propio | 64,9 | 74,1 | **Confirmado: cara limpia** |
| D: silueta de la malla + proyección de Codex | 75,7 | **82,0** | No confirmado por la cara (ojo doble). La geometría sí sirve: siluetas de 92 a 97 % |

**Vuelta 3: combinar.** Se proyectaron las texturas A y C sobre la geometría de D (`L04_PER01_v4D_geometria.glb`). Métrica v2:

| Versión | Total | Frente | Cabeza | Perfil | Espalda |
|---|---:|---:|---:|---:|---:|
| **v5C** (geometría D + textura C) | **83,9** | 85,3 | 80,9 | 83,3 | 87,5 |
| v5A (geometría D + textura A) | 83,8 | 83,2 | 84,7 | 79,9 | 87,1 |

**Con el bolso** (`accesorio_bolso.py` sobre v5C), métrica v2:

| Variante | Total | Cabeza | Perfil | Nota |
|---|---:|---:|---:|---|
| Bolso a 45° con correa 3D | 81,5 | 78,4 | 78,5 | Se ven dos correas: la 3D y la pintada |
| **Bolso a 45° sin correa 3D** | **82,9** | 80,9 | 78,8 | Elegida. Frente 84,9, espalda 87,1 |
| Bolso a 70° | 72,4–73,0 | se desploma | | Descartado |

**Versión final: `L04_PER01_v6C.glb`**, 7 694 triángulos (7 522 del cuerpo y 172 del bolso). En la escena va como `pruebas/escena_exploracion/tripo/PER-01_v6.glb`.

En Godot, con el acabado 2.5D, se lee como la hoja. Detalle pendiente: el pelo lleva arriba brillos amarillos algo fuertes, del borde naranja de la hoja proyectado sobre la coronilla.

**BUCLE CERRADO (2026-11-12): Guillermo aprobó la v8T como modelo base (D-017).**

- `L04_PER01_v8T.glb` da 81,1 % de parecido con bolso y 81,9 % sin él (métrica v2): frente 83,6; cabeza 79,4; perfil 75,2; espalda 85,4.
- La limpieza (estrategia T, `herramientas/mallas/limpiar_textura_T.py`) corrigió los 7 defectos de v5C. El verificador y el juez no encontraron defectos graves (flujo `wf_151a2471-347`).
- El perfil baja por el bolso: la hoja lo dibuja detrás de la cadera en el perfil y delante en el frente.
- Pendiente aprobado: mejorar el bolso 3D con la pintura de la bolsa de la hoja (flujo `wf_0a41f526-fdc`, salida `L04_PER01_v9.glb`). Se le muestra a Guillermo antes de integrarlo.

**Verificación de v5C y v5A** (flujo `wf_1df051d0-061`, dos verificadores y un juez). Las cifras se reproducen exactas y la geometría está sana: no hay caras invertidas ni picos, y el desplazamiento máximo es de 2,6 cm.

- **v5A no se confirma:** ojo asimétrico de frente y rasgos dobles en los costados.
- **v5C gana la cara de frente**, pero tampoco se confirma por defectos de proyección rasante:
  - oreja izquierda corrida y cuña oscura en la mandíbula;
  - mechones corridos delante de las orejas;
  - brillo cuadrado en un ojo;
  - costuras UV;
  - brillos del pelo más fuertes que en la hoja;
  - bolso de la hoja pintado en la cadera y el glúteo;
  - franja oscura en el brazo de espalda.

**Vuelta 4: limpieza** (flujo `wf_151a2471-347`). Dos estrategias, cada una con verificador, y un juez:

- **T:** volver a la textura original de Tripo, con ajuste de color en Lab, donde la proyección es rasante (g = max(n·d) < 0,35), en el costado izquierdo de la cabeza y en la zona del bolso pintado.
- **D:** rellenar esas zonas por difusión desde los texels bien proyectados de la misma zona.

Las dos dilatan las islas UV 16 px y bajan un 30 % los brillos del pelo. Salidas: `L04_PER01_v7{T,D}.glb` (sin bolso) y `L04_PER01_v8{T,D}.glb` (con bolso).

**Vuelta 2 (2026-11-12):** el flujo `wf_cb5b1503-94b` prueba cuatro enfoques en paralelo, cada uno con un verificador escéptico:

- **A:** alineación por bandas, con la hoja dominante.
- **B:** deformación 2D no rígida.
- **C:** registro propio de la cara.
- **D:** ajustar la silueta de la malla.

Salidas: `L04_PER01_v4{A,B,C,D}.glb` y `parecido/v4*/`.

Estimación del techo: con una proyección casi perfecta, el color sube a unos 88 y la estructura a unos 65; el total quedaría cerca del 80 %. Para pasar con margen hace falta también mejor silueta (enfoque D).

Componentes de la v2:

| Vista | Silueta | Color | Estructura |
|---|---:|---:|---:|
| Frente | 80 | 62 | 29 |
| Cabeza | 94 | 46 | 26 |

Lo débil es el color y la estructura: la textura de Tripo sale de la hoja de giro, con luz plana, y es más clara y menos contrastada que la hoja pintada.

**El bolso.** En la hoja está delante de la cadera en el frente y en la vista 3/4, pero detrás en el perfil. Se dejó delante, girado 45°, para favorecer dos de las tres vistas, y por eso el perfil baja de 66,6 a 58,9.

## En curso y siguiente

1. **Codex** (`Tareas_Codex/protagonista_parecido.md`, tarea `proyectar_hoja`): repintar la textura con las vistas de la hoja, alineadas por silueta y con visibilidad por profundidad. Sale como `L04_PER01_v3_hoja.glb`.
2. Pasar el bolso a la malla con la textura proyectada: `accesorio_bolso.py --entrada L04_PER01_v3_hoja.glb`.
3. Si no llega al 80 %:
   - ajustar el color global de la textura (media y desviación en Lab, contra la hoja);
   - revisar las proporciones de la cara (ojos más grandes en la hoja).
