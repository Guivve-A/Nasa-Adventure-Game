Escrito: [limpiar_personaje.py](<C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/limpiar_personaje.py>).

Uso desde esta carpeta, cuando instales Blender:

```powershell
& 'C:\ruta\blender.exe' -b --factory-startup --python-exit-code 1 --python .\limpiar_personaje.py -- `
  --entrada 'C:\Users\guill\Desktop\Juego 2d-hd\pruebas\escena_exploracion\tripo\PER-01.glb' `
  --salida '.\salidas\PER-01' `
  --objetivos 1500,3000,6000 `
  --umbral-soldar 0.0005 `
  --altura 1.7
```

Omite `--altura` para conservar el tamaño importado.

El script:

1. Importa el GLB, aplica sus transformaciones y conserva su orientación.
2. Ajusta opcionalmente la altura sobre Z; después suelda vértices y recalcula normales.
3. Genera cada LOD desde la base limpia usando Decimate Collapse y sombreado plano, conservando UV y materiales. El objetivo limita los triángulos del personaje completo; puede quedar ligeramente por debajo.
4. Exporta `PER-01_1500.glb`, `PER-01_3000.glb` y `PER-01_6000.glb`. Comprueba los triángulos exportados y las imágenes incrustadas.
5. Imprime un resumen JSON con triángulos, caja en metros, huesos, acciones y archivos escritos.

Las salidas deben quedar dentro de esta carpeta de trabajo. No sobrescribe archivos existentes. Si la base limpia ya está por debajo del objetivo, conserva su geometría.

**Validación limitada:** pasaron las comprobaciones de sintaxis, argumentos y lectura del contenedor GLB con datos sintéticos. No se ejecutó Blender ni se procesaron los personajes reales; tampoco pudo consultarse la documentación 5.2. El código permanece **sin probar contra bpy**.

**Riesgos:** soldar puede unir superficies cercanas; Decimate puede deformar siluetas y texturas; las superficies abiertas no tienen un exterior inequívoco. Rechaza rigs, animaciones y shape keys con un mensaje claro.
