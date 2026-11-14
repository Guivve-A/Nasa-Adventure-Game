# Brief comun: scripts de Blender para el juego (Proyecto NASA-Ecuador)

Contexto: RPG de exploracion en Godot 4.7.2, arte low-poly pintado a mano (facetas planas y nitidas). Las mallas de personajes salen de Tripo (Higgsfield) como GLB texturizado y hay que dejarlas listas para el motor en Blender 5.2.4 LTS, por script y sin ventana:

    blender.exe -b --factory-startup --python <script.py> -- <argumentos>

Blender todavia no esta instalado en este equipo (se instalara el 5.2.4 LTS para Windows x64), asi que no puedes ejecutarlo: escribe el codigo contra la API de Blender 5.2 (bpy) con cuidado, sin funciones obsoletas, y deja claro que esta sin probar. Consulta la documentacion oficial de la API 5.2 si dudas (docs.blender.org/api/5.2/).

Reglas:
- Escribe solo dentro de tu carpeta de trabajo (herramientas/blender/). No instales ni descargues nada.
- Python de Blender: solo bpy, bmesh, mathutils y la biblioteca estandar.
- Comentarios del codigo en espanol y sin tildes; cada script con un docstring de uso al principio y argumentos con argparse (los que vienen tras "--" en sys.argv).
- Que cada script imprima un resumen verificable al terminar (triangulos, huesos, acciones, archivos escritos) y falle con un mensaje claro si algo no cuadra.
- Unidades en metros. glTF es +Y arriba; Blender es +Z arriba (el importador convierte). Las mallas de Tripo miran hacia +X o -X segun el caso: no asumas el frente, detectalo o recibelo por argumento.
- Archivos de prueba (solo lectura): C:/Users/guill/Desktop/Juego 2d-hd/pruebas/escena_exploracion/tripo/PER-01.glb (protagonista, 4 930 triangulos, textura propia, mira a -X), PER-09.glb (gato Orbita, 2 733 triangulos, mira a +X) y FAU-01.glb (iguana).
- Responde en espanol con: archivos escritos, como se usan, que hace cada paso, que no se pudo comprobar y riesgos.

@@TAREA id=limpiar_personaje salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/limpiar_personaje.md sandbox=workspace-write cwd=herramientas/blender timeout=45 esfuerzo=medium

Escribe herramientas/blender/limpiar_personaje.py: importa un GLB de personaje, aplica transformaciones, suelda vertices duplicados (merge by distance con umbral pequeno y configurable), recalcula normales hacia fuera, y genera niveles de detalle con el modificador Decimate (Collapse) a triangulos objetivo dados (por defecto 1500, 3000 y 6000; si la malla ya tiene menos, la deja igual). Cada nivel con sombreado plano (sin suavizado), conservando UV y la textura original. Exporta cada nivel como GLB aparte (<salida>_<n>.glb) con la textura incluida. Argumentos: --entrada, --salida (prefijo), --objetivos 1500,3000,6000, --umbral-soldar 0.0005, --altura (reescala a esa altura en metros, opcional). Al final imprime los triangulos de cada nivel y la caja de cada uno.

@@TAREA id=mixamo salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/mixamo.md sandbox=workspace-write cwd=herramientas/blender timeout=45 esfuerzo=medium

Escribe dos scripts para usar Mixamo (que solo acepta FBX, OBJ o ZIP y solo rigea humanoides bipedos):
1. herramientas/blender/glb_a_fbx_mixamo.py: importa el GLB de la protagonista, la orienta mirando a -Y de Blender (el frente que espera Mixamo), la apoya en el suelo y centrada en el origen, en pose neutra, y exporta un FBX con la textura incrustada (path_mode COPY y embed_textures) listo para subir. Argumentos: --entrada, --salida, --frente (+x, -x, +y, -y; por defecto lo detecta como mejor puedas y lo explica).
2. herramientas/blender/fbx_mixamo_a_glb.py: importa uno o varios FBX descargados de Mixamo (el primero con malla y los demas solo animacion "without skin"), une las acciones en un solo armature con nombres claros (reposo, caminar, correr), y exporta un GLB con todas las animaciones y la textura. Argumentos: --malla, --animaciones a.fbx,b.fbx, --nombres reposo,caminar,correr, --salida. Imprime huesos, acciones y su duracion.

@@TAREA id=rig_gato salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/rig_gato.md sandbox=workspace-write cwd=herramientas/blender timeout=45 esfuerzo=high

Escribe herramientas/blender/rig_gato.py para el gato companero (cuadrupedo; Mixamo no sirve). Pasos: importar PER-09.glb; anadir el metarig Cat de Rigify (addon rigify, que viene con Blender; activalo por script) y ajustarlo a la malla con la caja de limites y proporciones medidas (cabeza, cuello, columna, cuatro patas y cola), con una opcion para guardar el .blend y retocar a mano; generar el rig; emparentar la malla con pesos automaticos; crear por script dos acciones ciclicas: "reposo" (respiracion y cola que se mece, 2 s) y "caminar" (paso de cuadrupedo con patas en diagonal, 1 s, en el sitio); y exportar un GLB con la malla, el esqueleto deformante (solo huesos DEF, como necesita Godot) y las dos acciones. Argumentos: --entrada, --salida, --guardar-blend, --frente (+x por defecto). Explica bien que partes son mas fragiles (ajuste del metarig, pesos automaticos en una malla de IA) y como revisarlas a mano.
