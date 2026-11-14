Escribí estos archivos:

- [glb_a_fbx_mixamo.py](<C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/glb_a_fbx_mixamo.py>): importa, orienta hacia −Y, centra, apoya en el suelo y exporta FBX con texturas incrustadas.
- [fbx_mixamo_a_glb.py](<C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/fbx_mixamo_a_glb.py>): comprueba esqueletos, reúne acciones en un armature y exporta un GLB con animaciones y textura.
- [README_mixamo.md](<C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/README_mixamo.md>): comandos completos, pasos, comprobaciones y riesgos.

Uso desde esta carpeta, sustituyendo las rutas del ejecutable y las entradas:

```powershell
& 'C:/ruta/blender.exe' -b --factory-startup --python-exit-code 1 --python ./glb_a_fbx_mixamo.py -- --entrada 'C:/modelos/PER-01.glb' --salida ./salidas/PER-01.fbx --frente=-x

& 'C:/ruta/blender.exe' -b --factory-startup --python-exit-code 1 --python ./fbx_mixamo_a_glb.py -- --malla ./descargas/reposo.fbx --animaciones './descargas/caminar.fbx,./descargas/correr.fbx' --nombres reposo,caminar,correr --salida ./salidas/PER-01_animado.glb
```

Ambos imprimen resúmenes verificables y rechazan datos incompatibles. Las salidas y temporales quedan dentro de la carpeta de trabajo.

**Sin probar en Blender:** pasaron la sintaxis y pruebas aisladas de auxiliares; no pude comprobar la API exacta 5.2, exportaciones reales, Mixamo ni Godot. La documentación oficial tampoco pudo consultarse por errores de acceso.

Riesgos principales: la detección automática del frente puede equivocarse; una malla sin rig conserva su pose y necesita llegar en una pose neutra adecuada; materiales y deformaciones requieren revisión visual. Confirmé mediante lectura del GLB que PER-01 tiene 4 930 triángulos y carece de rig.
