Escribí estos archivos:

- [rig_gato.py](<C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/rig_gato.py>)
- [rig_gato_LEEME.md](<C:/Users/guill/Desktop/Juego 2d-hd/herramientas/blender/rig_gato_LEEME.md>): instrucciones completas y revisión manual.

Desde `herramientas/blender`, en PowerShell:

```powershell
& 'C:/ruta/blender.exe' -b --factory-startup --python-exit-code 1 `
  --python './rig_gato.py' -- `
  --entrada 'C:/Users/guill/Desktop/Juego 2d-hd/pruebas/escena_exploracion/tripo/PER-09.glb' `
  --salida 'salidas/PER-09_rig.glb' `
  --guardar-blend 'salidas/orbita.blend' `
  --frente +x
```

El script:

1. Importa la malla, conserva textura y UV, aplica facetas planas y normaliza el frente.
2. Mide apoyos y regiones del cuerpo; ajusta un Cat de Rigify simplificado, sin cara ni dedos individuales.
3. Genera el rig y aplica pesos automáticos.
4. Crea `reposo` de 2 segundos y `caminar` de 1 segundo, con movimiento diagonal en el sitio.
5. Hornea una copia con **solo huesos DEF**, exporta y comprueba estructura, pesos, triángulos y clips. Imprime un resumen JSON.

Para revisar antes de generar, añade `--solo-metarig`. Abre el `.blend` indicado, corrige huesos en **Edit Mode**, guarda otra copia y continúa con `--reanudar archivo.blend`. La guía incluye comandos completos.

**Lo más frágil es el ajuste anatómico y los pesos automáticos.** Revisa articulaciones, separación de patas, base de cola y contacto con el suelo. Corrige los grupos `DEF-*` mediante Weight Paint. El paso diagonal es un trote estilizado; en Godot habrá que activar Loop.

**Sin probar en Blender ni Godot.** Pasaron las comprobaciones de sintaxis, argumentos y validación binaria con muestras sintéticas. Confirmé también los 2.733 triángulos del original. No generé todavía ningún rig, `.blend` ni GLB final.
