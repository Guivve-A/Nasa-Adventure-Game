Corregido en [rig_gato.py](</C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/rig_gato.py>), conservando las cinco correcciones.

El fallo principal estaba en `export_skeleton`: asignaba la matriz a huesos nuevos de longitud cero y perdía su dirección de descanso. Al reproducir una acción, el horneado introducía grandes giros respecto de esa referencia incorrecta, deformando la piel.

Ahora copio los extremos y la orientación de cada DEF y verifico sus matrices de descanso. Las acciones usan movimientos pequeños desde el descanso, mantienen la altura real de los IK y estabilizan la cabeza. `IK_Stretch=0` también queda fijado mediante claves.

Medí **20 huesos DEF de las patas**, además de la distancia cabeza–torso, en el rig evaluado y la copia exportable. Este es el resumen de Rigify; la **[tabla completa con cada longitud](</C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/salidas/PER-09_rig.medidas.md>)** incluye ambas versiones.

| Acción | Fotograma | Máxima diferencia en patas | Cabeza–torso |
|---|---:|---:|---:|
| Descanso de referencia | — | — | 0,359193 m |
| reposo | 1 | 0,325 % | 0,359193 m |
| reposo | 30 | 0,319 % | 0,359122 m |
| caminar | 1 | 0,325 % | 0,359193 m |
| caminar | 8 | 0,641 % | 0,357865 m |
| caminar | 15 | 0,335 % | 0,359134 m |
| caminar | 23 | 0,642 % | 0,357865 m |

También comprobé todos los fotogramas de ambos ciclos: ninguna diferencia alcanza el **5 %**. Las matrices de piel del GLB coinciden con Blender con error máximo de **7,15 × 10⁻⁷**.

Los renders Workbench de [reposo, fotograma 1](</C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/salidas/gato_reposo_f01.png>) y [caminar, fotograma 8](</C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/salidas/gato_caminar_f08.png>) muestran la cabeza conservada y patas sin las púas anteriores.

Ejecuté el comando completo desde la raíz, añadiendo `--render-pruebas`: **código de salida 0 y `GLB_VALIDADO_ESTRUCTURALMENTE`**. Se regeneraron el GLB y `gato.blend`: 34 DEF, 2.729 triángulos, 1.375 vértices con peso y clips de 2/1 segundos. El `.blend` también se reabrió correctamente.

Falta comprobar el recurso corregido dentro de **Godot** y revisar visualmente el ciclo completo, especialmente contacto con el suelo y deslizamiento.
