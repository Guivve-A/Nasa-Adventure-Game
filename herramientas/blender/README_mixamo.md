# Puente Tripo / Mixamo / Godot

**Estado: sin probar en Blender.** No hay Blender instalado en este equipo.
Se verificaron la sintaxis con Python 3.13 y partes independientes de `bpy`.
La consulta de la API oficial 5.2 no se pudo completar por errores de acceso.
Los operadores comprueban sus argumentos contra RNA al ejecutarse; una API
distinta produce un error en lugar de omitir silenciosamente una opcion.

Los scripts solo usan `bpy`, `mathutils` y biblioteca estandar. No instalan ni
descargan nada. Leen las entradas sin modificarlas. Limitan las salidas a esta
carpeta y sus subcarpetas, incluso si se ejecutan desde otro directorio.
Una salida existente se reemplaza solo despues de pasar las comprobaciones.
Los temporales quedan dentro de esta carpeta o de la carpeta de salida y se
eliminan al terminar. Los FBX se copian a un area temporal antes de importarlos,
junto con imagenes vecinas y su carpeta `<nombre_del_fbx>.fbm`, para aislar
cualquier archivo auxiliar que pueda generar el importador. Las texturas en
otras subcarpetas relativas deben reorganizarse junto al FBX antes de ejecutar.

## 1. Preparar el FBX para subirlo a Mixamo

PowerShell, desde `herramientas/blender/`:

```powershell
$blenderExe = 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
& $blenderExe -b --factory-startup --python-exit-code 1 --python ./glb_a_fbx_mixamo.py -- --entrada 'C:/Users/guill/Desktop/Juego 2d-hd/pruebas/escena_exploracion/tripo/PER-01.glb' --salida ./salidas/PER-01_mixamo.fbx --frente=-x
```

Cambiar la ruta de `blender.exe` por la real una vez instalado. `--python-exit-code`
es una opcion de Blender y va antes del separador `--`. Los errores controlados
del script tambien salen con codigo 1.

Pasos del primer script:

1. Inicia una escena vacia en metros e importa glTF, dejando al importador
   convertir +Y arriba a +Z arriba. No aplica una segunda conversion manual.
2. Quita animaciones y valores de morphs; si hay rig, evalua su pose de reposo.
   Hornea geometria y transformaciones globales en mallas sin rig, conservando
   UV y materiales. Mantiene sombreado plano; no remalla ni reduce poligonos.
3. Gira alrededor de Z para llevar el frente indicado a -Y de Blender.
   `--frente` se refiere a los ejes **despues de importar**. Admite `+x`, `-x`,
   `+y`, `-y`; para valores negativos conviene escribir `--frente=-x`.
4. Centra el centro horizontal de los limites geometricos en X=Y=0 y deja
   el vertice mas bajo en Z=0. No cambia el tamano: metros no implica que
   el personaje tenga automaticamente una altura humana correcta.
5. Materializa las imagenes en PNG temporales para que FBX pueda incrustarlas.
   Exporta triangulos con `path_mode='COPY'`, `embed_textures=True`, sin acciones,
   con ejes FBX -Y/+Z. Comprueba bloques binarios `Video/Content` no vacios.
6. Imprime un resumen JSON con triangulos, huesos de entrada/salida, acciones,
   frente elegido, limites en metros, imagenes incrustadas, ruta y bytes.

Sin `--frente`, compara el saliente de los pies con los tobillos en bandas de
altura. Imprime sus puntuaciones y rechaza una diferencia insuficiente.
Es una heuristica para un bipedo de pie: zapatos asimetricos, ropa, una pose
inclinada o anatomia inusual pueden producir un frente equivocado incluso
cuando supera el umbral. No reconoce una cara. Para PER-01 usar `--frente=-x`.

**Pose neutra:** una malla Tripo sin rig ya debe tener una pose neutra adecuada,
preferentemente T/A con brazos separados. El script conserva esa geometria;
no adivina articulaciones ni recoloca brazos o piernas. Un rig existente se
hornea en reposo, pero eso tampoco garantiza una T/A-pose. Mixamo requiere la
revision humana de los marcadores y solo admite humanoides bipedos: este flujo
no sirve para el gato PER-09 ni para la iguana FAU-01.

## 2. Descargar las animaciones y reunirlas

En Mixamo, utilizar siempre el mismo personaje rigeado. Descargar un primer
FBX **With Skin**, por ejemplo la animacion de reposo, y los adicionales
**Without Skin**. Mantener el mismo formato FBX y los mismos FPS en todos.
Elegir `In Place` en Mixamo si no se desea desplazamiento en caminar/correr:
el script conserva el movimiento de raiz recibido y no cierra bucles.

Colocar los FBX y cualquier carpeta `.fbm`/textura que los acompane en una
subcarpeta como `descargas/`. No perder las imagenes externas.

```powershell
& $blenderExe -b --factory-startup --python-exit-code 1 --python ./fbx_mixamo_a_glb.py -- --malla ./descargas/reposo.fbx --animaciones './descargas/caminar.fbx,./descargas/correr.fbx' --nombres reposo,caminar,correr --salida ./salidas/PER-01_animado.glb
```

`--nombres` asigna primero el nombre a la accion del FBX con malla, si la tiene,
y despues a una accion por cada archivo adicional, en el orden indicado.
Si el primero es una T-pose **sin accion**, usar solo `--nombres caminar,correr`.
No se crea una accion reposo artificial. Para reunir solamente la animacion
de un unico FBX, omitir `--animaciones` e indicar un nombre. Se rechazan clips
de un solo instante. Las listas usan comas; las rutas no pueden contener comas.

Pasos del segundo script:

1. Importa el FBX con malla y exige un solo armature, malla con modificador de
   armature y grupos de vertices, UV e imagenes cargadas.
2. Importa cada FBX adicional, exige un solo armature, una accion de huesos y
   ausencia de malla. Compara FPS, nombres de huesos, padres, matrices y largos
   de reposo, y transformacion global. Rechaza esqueletos distintos; no hace
   retargeting ni cambia nombres de huesos o prefijos Mixamo.
3. Copia las acciones usando slots de la API moderna, verifica sus rutas y
   elimina los rigs temporales. Crea una pista NLA por clip con nombres unicos,
   conservando el intervalo de claves y desplazandolo al fotograma cero.
4. Exporta las pistas por separado en un GLB, con muestreo a cada fotograma,
   skin, todos los huesos, normales planas y materiales. La conversion de ejes
   de vuelta a glTF se deja al exportador. No aplica transformaciones al rig.
5. Lee el JSON del GLB generado para comprobar nombres y duraciones de clips,
   canales no vacios, conjunto de joints, triangulos, imagenes internas y textura
   de color base por primitiva. Acepta una diferencia temporal de hasta 1,1
   fotogramas por redondeo de muestreo. Publica la salida solo al pasar esto.
6. Imprime un resumen JSON con todos los nombres de huesos, numero de triangulos,
   FPS, nombres e intervalos de acciones, duracion fuente/exportada en segundos,
   imagenes incrustadas, ruta y bytes escritos.

## Comprobaciones y riesgos pendientes

- Se leyo PER-01.glb mediante biblioteca estandar, sin modificarlo: 4 930
  triangulos, una malla, una imagen PNG interna, sin skins ni animaciones.
  Su altura declarada en glTF es 1 metro. No se comprobo visualmente su pose.
- Pasaron pruebas aisladas con datos sinteticos para el frente negativo,
  deteccion geometrica y rechazo de ambiguedad, bloques FBX 7400/7500 y
  comprobaciones del JSON GLB con nombres, imagenes, triangulos y duraciones
  correctos e incorrectos. Estas pruebas no ejecutan ni simulan `bpy`.
- No se ejecutaron importadores/exportadores de Blender ni se genero un FBX/GLB
  real. No se verificaron la API exacta 5.2.4, la apariencia de materiales,
  la aceptacion del FBX por Mixamo, el rig automatico ni la reproduccion en Godot.
- FBX no representa todos los nodos de materiales glTF. Los materiales Tripo
  deben conservar una conexion exportable entre textura y Principled BSDF.
  Contar imagenes incrustadas no garantiza su apariencia; el segundo script
  comprueba ademas la referencia de textura de color base en el GLB.
- La comprobacion de esqueletos es deliberadamente estricta. Exportaciones de
  otro personaje, otra orientacion de huesos o configuraciones distintas pueden
  requerir retargeting fuera de estos scripts.
- El GLB conserva los pesos recibidos y puede exportar mas de cuatro influencias.
  Revisar los limites de influencias de la importacion en Godot si los FBX
  contienen pesos inusuales. No se valida anatomia ni calidad de deformacion.
- Antes de integrarlo en el juego, revisar frente, altura, pies, textura,
  separacion de clips, movimiento de raiz y deformacion de manos/hombros/caderas.

Referencia oficial solicitada (consulta no completada):
<https://docs.blender.org/api/5.2/>.
