# Brief: corregir las acciones del rig del gato (herramientas/blender/rig_gato.py)

Contexto: juego en Godot 4.7.2 con arte low-poly. `herramientas/blender/rig_gato.py` (lo escribiste tu) ya corre de punta a punta en Blender 5.3.0, instalado en `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`. Claude le aplico cinco correcciones, probadas, que no debes deshacer (estan comentadas en el codigo):
1. Soldar vertices antes de los pesos automaticos (`soldar`): sin eso, 2 086 vertices quedaban sin peso.
2. Copiar pesos del vecino mas cercano a los vertices sueltos (`rellenar_pesos`): 5 vertices.
3. Hornear solo posicion y rotacion (sin escala) en `baked_actions`: la escala no uniforme de Rigify producia cizallamiento no exportable.
4. Recontar triangulos tras soldar (2733 -> 2729).
5. Exportar con `export_animation_mode='NLA_TRACKS'`: con ACTIONS salian tambien CTRL_reposo y CTRL_caminar.

Comando que funciona (desde la raiz del proyecto):

    & "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup --python-exit-code 1 --python herramientas\blender\rig_gato.py -- --entrada "C:\Users\guill\Desktop\Juego 2d-hd\pruebas\escena_exploracion\tripo\PER-09.glb" --salida salidas/PER-09_rig.glb --guardar-blend salidas/gato.blend --frente +x

Termina con status GLB_VALIDADO_ESTRUCTURALMENTE: 34 huesos DEF, acciones reposo (2 s) y caminar (1 s), 1 375 vertices con peso.

**El problema que queda:** en Godot, la pose de union del GLB (sin reproducir animacion) se ve perfecta: los pesos y la piel estan bien. Pero al reproducir "reposo" o "caminar" el gato se deforma mucho: las cuatro patas se estiran hacia abajo como puas y la cabeza se aplasta. Pasa igual en reposo, asi que no es el ciclo de paso: los valores de las acciones colocan mal los controles (IK de patas, cabeza o cuello) respecto de la pose de descanso del rig. Sospechas, por comprobar: controles IK de pata movidos a una altura o en un espacio de coordenadas equivocados (por ejemplo, z = 0 en vez de la altura real de la pata, o coordenadas de mundo en un canal local), estiramiento IK de Rigify activo, o un control raiz o de torso desplazado. Capturas: `pruebas/escena_exploracion/capturas/gato_union_vs_reposo.png` (izquierda, union bien; derecha, reposo mal) y `lamina_gato_rig.png` (caminar).

@@TAREA id=rig_gato_acciones salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/rig_gato_acciones.md sandbox=workspace-write cwd=herramientas/blender timeout=45 esfuerzo=high

Corrige `create_actions` (y lo que haga falta) para que reposo y caminar no deformen al gato. Reglas:
- Las acciones deben partir de la pose de descanso del rig y mover poco: reposo = respiracion leve del torso y cola que se mece; caminar = paso en diagonal en el sitio, con las patas a su altura real de descanso (sin estirar el IK) y la cabeza estable.
- Desactiva el estiramiento IK de Rigify en las patas si existe la propiedad (por ejemplo `IK_Stretch` = 0 en los controles de pata), para que nunca estire la malla.
- Compruebalo con Blender, por script y sin ventana: para los fotogramas 1, 8, 15 y 23 de caminar y el 1 y 30 de reposo, mide en el rig evaluado la longitud de cada hueso DEF de las patas y la distancia cabeza-torso. La diferencia con el reposo del rig debe quedar por debajo del 5 %. Imprime una tabla con esas medidas.
- Si puedes, renderiza con Workbench una imagen PNG del gato en el fotograma 1 de reposo y en el 8 de caminar (camara lateral) en herramientas/blender/salidas/, y describe lo que se ve.
- No deshagas las cinco correcciones. Al final ejecuta el comando completo y confirma status GLB_VALIDADO_ESTRUCTURALMENTE.
- Responde en espanol: que estaba mal, que cambiaste, la tabla de medidas y lo que no pudiste comprobar.
