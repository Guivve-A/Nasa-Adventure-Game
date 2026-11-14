# Gato Órbita: preparación para Godot

`rig_gato.py` se ejecutó de punta a punta con **Blender 5.3.0** y PER-09.
El resultado contiene 34 huesos DEF, 2.729 triángulos tras soldar, 1.375 vértices
con peso y los clips `reposo` (2 s) y `caminar` (1 s). La revision del paso
valida ambos ciclos a 120 Hz: diferencia maxima de patas respecto al descanso
de 2,1291 %, por debajo del limite del 5 %. Se capturaron seis instantes de
caminar en Godot 4.7.2. Evidencia: [informe del paso](salidas/paso_orbita/informe_paso_orbita.md).

Comprobaciones ejecutadas con Python estándar: sintaxis, docstring, comentarios
ASCII y lectura de argumentos; aceptación de un GLB sintético cíclico y rechazo
de seis variantes inválidas (joint ORG, clip ausente, duración errónea, ciclo
abierto, pesos sin normalizar y falta de skinning). También se comprobó el
rechazo de una ruta de salida fuera de la carpeta. Las muestras sintéticas se
eliminaron al terminar; no proceden del exportador de Blender.

Se leyó `PER-09.glb` sin modificarlo: contiene **2.733 triángulos**, una malla,
una imagen JPEG embebida, sin skin ni animaciones. No se instalaron ni
descargaron programas, complementos o recursos.

## Ejecución completa

Desde `herramientas/blender`, en PowerShell, sustituye la ruta del ejecutable:

```powershell
& 'C:/ruta/Blender 5.2/blender.exe' -b --factory-startup --python-exit-code 1 `
  --python './rig_gato.py' -- `
  --entrada 'C:/Users/guill/Desktop/Juego 2d-hd/pruebas/escena_exploracion/tripo/PER-09.glb' `
  --salida 'salidas/PER-09_rig.glb' `
  --guardar-blend 'salidas/orbita.blend' `
  --frente +x
```

`--python-exit-code 1` permite detectar excepciones desde PowerShell o una
automatización. `--salida` es obligatorio. `--entrada` es obligatorio salvo al
reanudar. `--guardar-blend` recibe una ruta y es opcional; conviene usarlo para
poder corregir ajustes o pesos. `--frente` admite `+x`, `-x`, `+y`, `-y` y usa
`+x` por defecto. Para un valor negativo también puedes usar `--frente=-x`.
El frente se refiere a los ejes de Blender **después** de importar el GLB.

Toda salida debe estar dentro de `herramientas/blender/`; las rutas relativas
se resuelven respecto a la carpeta del script. La herramienta puede crear
subcarpetas. Reemplaza archivos de salida del mismo nombre, pero rechaza pisar
la entrada. No guarda preferencias ni instala Rigify: lo activa durante la
sesión y falla con un mensaje si no está disponible en esa distribución.

Con los nombres del ejemplo, una ejecución completa intenta escribir:

- `salidas/PER-09_rig.glb`: modelo con textura embebida, skin DEF y dos clips.
- `salidas/orbita.metarig.blend`: malla y metarig ajustado, antes de generar.
- `salidas/orbita.pesos.blend`: rig generado y pesos antes de validar/animar.
- `salidas/orbita.blend`: rig editable, acciones de control y copia DEF oculta.
- `salidas/PER-09_rig.medidas.md`: tablas de longitudes y distancia cabeza-torso.
- `salidas/PER-09_rig.medidas.json`: medidas de todos los fotogramas de ambos ciclos.

Añade `--render-pruebas` para guardar también `gato_reposo_f01.png` y
`gato_caminar_f08.png`, vistas laterales de la copia exportable con Workbench.

El GLB se exporta primero como `PER-09_rig.validando.glb` y solo sustituye la
salida definitiva después de pasar las comprobaciones. Ese temporal se elimina
al terminar o al fallar normalmente; una interrupción del proceso puede dejarlo.
Los `.blend` de revisión pueden existir aunque falle un paso posterior.

## Paso legible y contacto de las plantas

`caminar` conserva el ciclo de un segundo y las diagonales alternas. La
zancada completa alcanza el 18 % de la talla (limitada por la distancia entre
apoyos); la elevacion alcanza el 8,5 %. El torso oscila un 1,2 % y la cabeza
conserva su matriz de referencia. `reposo` respira un 0,3 % y mueve la cola
con una amplitud de 0,12 rad; caminar usa 0,22 rad.

La altura de los IK se compensa con los vertices de las plantas y los mismos
cuatro pesos de la exportacion, sin cambiar pesos ni la pose de union. Ademas
de las tablas de longitudes, se escriben `PER-09_rig.plantas.md` y `.json`.
Se comprueba la piel exportable a 120 Hz, incluidos los intervalos entre
claves: ninguna planta de caminar puede bajar del minimo de reposo y el
retorno al apoyo debe estar a menos de 0,2 mm por metro de talla.
Las longitudes DEF tambien se validan a 120 Hz; el limite sigue siendo <5 %.

## Pasos que realiza

1. Importa el GLB con el importador oficial. Hornea las transformaciones de la
   jerarquía en los vértices y conserva materiales, imagen y UV. Usa sombreado
   plano para las facetas, sin remallar ni reducir polígonos.
2. Convierte el frente indicado a **−Y en Blender**, centra XY y pone el punto
   más bajo en Z=0. El exportador convierte Z arriba de Blender a Y arriba de
   glTF; el frente resultante es **+Z en el GLB**. No hagas otra conversión de
   ejes a mano. Se interpreta una unidad como un metro, conservando el tamaño
   importado: el archivo no aporta una talla anatómica fiable.
3. Mide caja de límites, cuatro grupos de vértices bajos para los apoyos,
   cortes del torso, región frontal alta para cabeza y cortes posteriores para
   cola. Imprime estas medidas en metros y las guarda en propiedades de escena.
   Son estimaciones geométricas, no reconocimiento anatómico.
4. Crea el preset **Cat de Rigify** instalado. Elimina los subárboles de cara
   y dedos individuales; conserva cabeza, cuello, columna, patas y cola.
   Ajusta el cuerpo por regiones, coloca articulaciones con proporciones
   aproximadas y adapta la cola a los cortes medidos. Usa segmentos lineales
   para evitar depender de deformaciones B-Bone que glTF no reproduce.
5. Genera Rigify y emparenta con `ARMATURE_AUTO`. Comprueba modificador,
   pesos DEF y cobertura de todos los vértices. Un resultado `FINISHED` del
   operador no basta: Bone Heat puede fallar aunque el operador termine.
6. Crea `CTRL_reposo` de 2 segundos y `CTRL_caminar` de 1 segundo, a 30 fps.
   Reposo desplaza levemente el torso para respirar y mece la cola, sin escalar.
   La cabeza queda estable. Caminar usa objetivos IK a su altura de descanso:
   delantera izquierda con trasera derecha, y la otra diagonal medio ciclo
   después. Es un **trote estilizado**, sin avance de raíz, con elevación de las
   patas durante la recuperación. Se fija `IK_Stretch=0` en los cuatro controles
   de propiedades de Rigify. No es un estudio biomecánico de marcha felina.
7. Construye otro esqueleto con **solo DEF**, conectando cada hueso a su
   ancestro DEF más cercano. Copia extremos y roll antes de hornear y verifica
   las matrices de descanso: asignar la matriz a un EditBone de longitud cero
   perdía su dirección y causaba la deformación al reproducir las acciones.
   Hornea posición y rotación de las matrices evaluadas de Rigify y produce
   las acciones finales `reposo` y `caminar`. Detecta ciclos abiertos y
   cizallamiento que no puede convertirse fielmente a traslación/rotación/escala.
   La copia de malla conserva como máximo cuatro influencias normalizadas por
   vértice. Los pesos del rig editable no se recortan.
8. Exporta solo las copias de malla y esqueleto. Lee el GLB generado y exige
   un skin, joints DEF, ausencia de ORG/MCH, triángulos conservados, pesos
   normalizados, imágenes embebidas y exactamente dos clips con movimiento,
   duración de 2/1 segundos y cierre de ciclo. Al terminar imprime
   `RESUMEN_RIG_GATO=...` en JSON con triángulos, huesos, acciones, avisos y
   archivos escritos. Ante errores imprime `ERROR_RIG_GATO` y un resumen parcial.
   Mide todos los DEF de patas y la distancia cabeza-torso en el depsgraph de
   Rigify y de la copia DEF; rechaza diferencias del 5 % o mayores. Imprime
   las muestras de caminar 1/8/15/23 y reposo 1/30 y guarda las tablas. Comprueba
   además las matrices de piel del GLB (nodos animados × inverseBindMatrices)
   contra el DEF evaluado en esas seis muestras.

## Revisar y corregir el metarig

Para detenerse antes de generar y pesar, usa el comando completo con:

```powershell
  --guardar-blend 'salidas/ajuste.blend' --solo-metarig
```

En este modo se escribe únicamente `ajuste.blend`; `--salida` sigue siendo
obligatorio, pero no se exporta un GLB. Abre el archivo en Blender y selecciona
`metarig`. En **Edit Mode**, revisa de lado, frente y arriba, con rayos X:

- Columna dentro del volumen del torso; cuello siguiendo su eje y cabeza con
  pivote próximo a la unión con el cuello.
- Hombros/caderas a ambos lados del cuerpo; rodillas, codos, corvejones y
  muñecas dentro de la malla. Conserva una ligera flexión para que IK tenga
  un plano de doblado estable.
- Puntas y bases de patas próximas al suelo; patas izquierdas y derechas
  separadas y sin huesos cruzados.
- Cola dentro de su volumen a lo largo de toda la curva, especialmente la
  base. No confíes en los cortes posteriores si la cola se eleva o se enrosca.

Mueve huesos en Edit Mode; conserva nombres, tipos Rigify, padres y conexiones.
No escales/rotes los objetos, ni generes el rig manualmente en este punto de
control. Guarda, por ejemplo, `salidas/ajuste_corregido.blend`, y continúa:

```powershell
& 'C:/ruta/Blender 5.2/blender.exe' -b --factory-startup --python-exit-code 1 `
  --python './rig_gato.py' -- `
  --reanudar 'salidas/ajuste_corregido.blend' `
  --salida 'salidas/PER-09_rig.glb' `
  --guardar-blend 'salidas/orbita.blend'
```

No repitas `--entrada`: reanudar usa la malla y el metarig del blend sin
reajustarlos. `--frente` se ignora al reanudar porque ya se normalizó la escena.
Si necesitas cambiar tamaño o pose de reposo, hazlo antes de este proceso y
comienza otra importación: las medidas guardadas no se recalculan al reanudar.

## Revisar los pesos y las animaciones

El ajuste del metarig y los pesos automáticos son los puntos más frágiles.
Una malla de IA puede tener patas pegadas al torso, superficies superpuestas,
triángulos degenerados, islas desconectadas o poca geometría en articulaciones.
La cola también puede recibir pesos de las patas traseras. El agrupamiento de
vértices bajos puede confundir una pose sentada con cuatro apoyos.

Abre el blend final y selecciona las acciones `CTRL_reposo` / `CTRL_caminar`
en `Orbita_Rigify` mediante el Action Editor y su slot del objeto. Reproduce
1–60 para reposo o 1–30 para caminar; 61 y 31 repiten el inicio para cerrar el
clip. Revisa hombros, vientre, codos, caderas, patas y base de cola. Comprueba
deslizamiento, penetración del suelo y estiramiento de patas. Un ciclo numérico
correcto no garantiza un movimiento agradable.

Para arreglar pesos, selecciona una malla `Orbita_malla_*` y trabaja en
**Weight Paint** sobre sus grupos `DEF-*`. Comprueba ambos lados y las islas
pequeñas. Normaliza los pesos y evita influencias de patas contrarias. No pintes
las copias `*_GLB`: están ocultas y se reconstruyen al reanudar.
Si falla la cobertura de pesos, usa `orbita.pesos.blend`, que se guarda antes
de esa comprobación. Tras corregir, guarda como otro archivo local y ejecuta:

```powershell
& 'C:/ruta/Blender 5.2/blender.exe' -b --factory-startup --python-exit-code 1 `
  --python './rig_gato.py' -- `
  --reanudar 'salidas/orbita_corregida.blend' `
  --salida 'salidas/PER-09_rig.glb' `
  --guardar-blend 'salidas/orbita_final.blend'
```

Al reanudar un blend que ya contiene el rig, conserva sus pesos y no vuelve a
generarlo. **Recrea las animaciones procedurales** y las copias exportables;
cualquier edición manual de esas acciones se pierde. Para cambiar el metarig,
vuelve al punto de control anterior a Generate Rig y repite los pesos.

En Godot, comprueba tamaño y frente, `Skeleton3D`, skin, textura y reproducción
de ambos clips. Activa **Loop** para cada animación en las opciones de
importación y reimporta: glTF no guarda un indicador universal de repetición
infinita. El paso diagonal de un segundo puede deslizar si la velocidad de
desplazamiento del personaje no se coordina con la longitud de zancada.

## Límites pendientes de comprobar

- Otras versiones de Blender y otros gatos. Si el preset instalado cambia
  nombres o estructura, el script falla con un mensaje.
- Revisión artística del ciclo completo, contacto con suelo y deslizamiento.
  Las dos imágenes Workbench muestran cabeza y patas sin las deformaciones
  grandes del recurso anterior; no sustituyen una revisión de movimiento.
- Paridad de la copia DEF y del rig original tras limitar a cuatro pesos:
  puede cambiar ligeramente la deformación. El script rechaza cizallamiento
  apreciable en lugar de exportar una aproximación silenciosa.
- Importación del recurso corregido en Godot 4.7.2 y configuración de bucles.

Referencias oficiales usadas: [exportación glTF en API 5.2](https://docs.blender.org/api/5.2/bpy.ops.export_scene.html),
[acciones en capas y slots](https://docs.blender.org/api/5.2/info_quickstart.html),
[uso de Rigify](https://docs.blender.org/manual/en/5.2/addons/rigify/basics.html)
y [preset Cat del repositorio oficial](https://github.com/blender/blender-addons/blob/main/rigify/metarigs/Animals/cat.py).
La consulta directa de algunas páginas falló; se contrastaron sus firmas
mediante los resultados indexados de la documentación oficial.
