# Brief comun: escena de exploracion v1 (Godot 4.7.2) y el gato Orbita

Proyecto: RPG de exploracion low-poly en Godot 4.7.2 (renderizador Mobile) que debe correr en un portatil con Intel HD 620. La escena de prueba esta en `pruebas/escena_exploracion/`: `escena.gd` lee `layout.json` (generado por `herramientas/mallas/escena_v1.py`), carga cada GLB en tiempo de ejecucion con `GLTFDocument` (carpetas `modelos/` y `tripo/`, ignoradas por el editor con `.gdignore`) y le pone los shaders de `shaders/` segun el nombre del material (`materiales.gd`). Los shaders usan `world_vertex_coords` y una cizalla `z -= inclinacion * y` (inclinacion 0,45) para que los objetos se lean erguidos.

Godot (consola): `C:\Users\guill\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe`
Blender 5.3: `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`

Comandos utiles (desde la raiz del proyecto, PowerShell; las rutas con espacios van entre comillas y el ejecutable con `&` delante):
- Captura: `& $G --path <ruta absoluta a pruebas\escena_exploracion> -- --encuadre=21 --captura=<png absoluto>` (encuadre 21 o 12).
- Medicion: `& $G --path <...> -- --encuadre=21 --medir=6` imprime una linea `MEDIDA ... fps_medio=... ms_p95=... primitivas=... llamadas=...`.
- Vista previa de un GLB con animacion: `& $G --path <...> res://vista_previa.tscn -- --glb=<ruta> --altura=0.5 --angulo=lateral --animacion=caminar --tiempo=0.25 --captura=<png>`.

Reglas: comentarios del codigo en espanol y sin tildes. No instales nada. No toques `nucleo.py` ni los scripts de los agentes de recursos. Al cambiar algo, mide antes y despues y deja la evidencia (lineas MEDIDA, capturas) en tu informe. Responde en espanol con: que cambiaste, mediciones antes/despues, capturas generadas y lo que no pudiste comprobar.

@@TAREA id=multimesh_escena salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/multimesh_escena.md sandbox=workspace-write cwd=pruebas/escena_exploracion timeout=45 esfuerzo=high

Hoy la escena tiene 240 recursos y 250-420 llamadas de dibujo; corre a 56-58 fps a 720p. Cambia `escena.gd` para que los recursos que se repiten (mismo `glb` y mismo `nodo` en `layout.json`, por ejemplo los 170 mechones `VEG-13`, las flores `VEG-14`, las piedras `TER-03` y `TER-05` y las plantas) se dibujen con un `MultiMeshInstance3D` por grupo (uno por superficie o material si hace falta), conservando: el material de shader de cada superficie, las sombras, la escala y la rotacion de cada instancia, el apoyo en el terreno y la opcion `nodo` que elige una variante dentro del GLB. Deja intactos los recursos unicos, los que tienen `animacion` (el gato) o `variante` (las dos antenas). Comprueba:
1. Mide con `--medir=6` en los dos encuadres antes y despues.
2. Captura los dos encuadres antes y despues y compara las imagenes (diferencia media por pixel). Deben verse iguales salvo el viento de la hierba.
3. Que la inclinacion (`world_vertex_coords`) y el viento sigan funcionando en las instancias.

@@TAREA id=gato_paso salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/gato_paso.md sandbox=workspace-write cwd=herramientas/blender timeout=45 esfuerzo=high

`herramientas/blender/rig_gato.py` ya funciona (ver `rig_gato_acciones.md` en los informes): el gato Orbita tiene rig Rigify Cat y dos acciones, pero el paso de "caminar" es muy pequeno y apenas se nota en el juego. Mejora `create_actions` para que "caminar" sea un paso de gato legible a tamano de juego: zancada claramente visible (patas en diagonal, alternando), un leve sube y baja del cuerpo, la cola que acompana y la cabeza estable; y que "reposo" tenga respiracion y cola visibles pero sutiles. Reglas: las patas apoyan en el suelo (la altura minima de cada pata en el ciclo no baja de la del reposo y en el apoyo vuelve a ella), sin estirar el IK (diferencia de largo de huesos DEF de las patas menor del 5 %), los ciclos cierran, y no deshagas ninguna correccion anterior (estan comentadas). Ejecuta el comando completo con el GLB de `C:\Users\guill\Desktop\Juego 2d-hd\pruebas\escena_exploracion\tripo\PER-09.glb`, confirma `GLB_VALIDADO_ESTRUCTURALMENTE`, y captura en Godot 6 instantes de "caminar" (cada 1/6 s) con la vista previa para mostrar el paso. Pon en el informe la tabla de alturas minimas de cada pata por instante y la de largos de huesos.
