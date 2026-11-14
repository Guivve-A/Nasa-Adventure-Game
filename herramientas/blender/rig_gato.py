"""Prepara un gato Tripo con Rigify Cat para Godot. Probado en Blender 5.3.

Uso (PowerShell, desde herramientas/blender):
  & 'C:/ruta/blender.exe' -b --factory-startup --python-exit-code 1 `
      --python rig_gato.py -- --entrada 'C:/ruta/PER-09.glb' `
      --salida 'salidas/PER-09_rig.glb' --guardar-blend 'salidas/gato.blend' `
      --frente +x

Revision del metarig antes de generar:
  ... --salida salidas/gato.glb --guardar-blend salidas/ajuste.blend --solo-metarig
  Abrir ajuste.blend, editar metarig en Edit Mode y guardar otra copia local.
  ... --salida salidas/gato.glb --guardar-blend salidas/final.blend `
      --reanudar salidas/ajuste_corregido.blend

--reanudar tambien admite el blend final o el punto de control de pesos:
conserva rig y pesos manuales, recrea las acciones y la copia DEF de exportacion.
No ejecutar Generate Rig manualmente en el punto de control del metarig.

Solo se escribe bajo la carpeta de este script. Las rutas relativas de salida
son relativas a esa carpeta. No instala addons ni guarda preferencias.
Requiere Blender 5.2.x y Rigify ya incluido/disponible. Solo bpy, mathutils y
biblioteca estandar. El GLB de entrada nunca se modifica.

El frente se interpreta DESPUES de importar glTF a Blender. Se normaliza a -Y
en Blender (+Z en glTF), suelo Z=0 y centro XY=0. Una unidad es un metro; NO
se inventa una talla fisica para Tripo. El ajuste es una heuristica geometrica,
no una deteccion anatomica. El paso diagonal es un trote estilizado en el sitio.

Documentacion consultada:
https://docs.blender.org/api/5.2/bpy.ops.export_scene.html
https://docs.blender.org/api/5.2/info_quickstart.html
https://docs.blender.org/manual/en/5.2/addons/rigify/basics.html
"""

import argparse
import importlib
import json
import math
import os
from pathlib import Path
import statistics
import struct
import sys
import traceback

import bpy
from mathutils import Matrix, Quaternion, Vector


ROOT = Path(__file__).resolve().parent
FPS = 30
TAG = "rig_gato_role"
WRITTEN = []
WARNINGS = []


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def warn(message):
    WARNINGS.append(message)
    print("AVISO: " + message, flush=True)


def log(message):
    print("[rig_gato] " + message, flush=True)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--entrada", type=Path, help="GLB Tripo de solo lectura")
    parser.add_argument("--salida", required=True, type=Path, help="GLB bajo la carpeta del script")
    parser.add_argument("--guardar-blend", type=Path, metavar="ARCHIVO.blend")
    parser.add_argument("--frente", choices=("+x", "-x", "+y", "-y"), default="+x",
                        help="Frente en Blender despues de importar (defecto: +x)")
    parser.add_argument("--render-pruebas", action="store_true",
                        help="Renderizar vistas laterales Workbench de reposo 1 y caminar 8")
    parser.add_argument("--solo-metarig", action="store_true",
                        help="Guardar el ajuste inicial y terminar antes de Generate Rig")
    parser.add_argument("--reanudar", type=Path, metavar="ARCHIVO.blend",
                        help="Continuar un blend creado por este script; no reimporta ni reajusta")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    if not args.entrada and not args.reanudar:
        parser.error("Se necesita --entrada o --reanudar")
    if args.entrada and args.reanudar:
        parser.error("Use --entrada o --reanudar, no ambos")
    if args.solo_metarig and (not args.guardar_blend or args.reanudar):
        parser.error("--solo-metarig necesita --guardar-blend y una nueva --entrada")
    return args


def output_path(path, suffix):
    path = (ROOT / path).resolve() if not path.is_absolute() else path.resolve()
    require(path.is_relative_to(ROOT), "Salida fuera de herramientas/blender: " + str(path))
    require(path.suffix.lower() == suffix, "Extension esperada " + suffix + ": " + str(path))
    return path


def select_only(objects, active=None):
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.hide_set(False)
        obj.hide_viewport = False
        obj.select_set(True)
    bpy.context.view_layer.objects.active = active or objects[0]


def save_blend(path):
    path = output_path(path, '.blend')
    path.parent.mkdir(parents=True, exist_ok=True)
    # Evita archivos .blend1 al repetir la herramienta.
    bpy.context.preferences.filepaths.save_version = 0
    result = bpy.ops.wm.save_as_mainfile(filepath=str(path), check_existing=False)
    require('FINISHED' in result and path.is_file(), "No se pudo guardar " + str(path))
    WRITTEN.append(str(path))
    log("Guardado: " + str(path))


def enable_rigify():
    # No descarga extensiones: si no esta en la distribucion se informa el fallo.
    try:
        result = bpy.ops.preferences.addon_enable(module="rigify")
        require('FINISHED' in result, "Rigify no se pudo activar")
    except Exception as exc:
        raise RuntimeError("Rigify no esta disponible. Habilitelo en esta instalacion de Blender; "
                           "el script no instala ni descarga addons.") from exc


def mesh_points(meshes):
    return [obj.matrix_world @ v.co for obj in meshes for v in obj.data.vertices]


def bounds(points):
    require(bool(points), "La malla no tiene vertices")
    low = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    require(min(high - low) > 1e-6, "Caja de limites degenerada")
    return low, high


def quantile(values, q):
    values = sorted(values)
    require(bool(values), "No hay muestras para medir una region")
    x = q * (len(values) - 1)
    i = int(x)
    return values[i] * (1 - x + i) + values[min(i + 1, len(values) - 1)] * (x - i)


def import_cat(path, front):
    require(path.is_file() and path.suffix.lower() == '.glb', "Entrada GLB inexistente: " + str(path))
    # La ejecucion nueva parte de una escena vacia; no toca el archivo original.
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    result = bpy.ops.import_scene.gltf(filepath=str(path))
    require('FINISHED' in result, "El importador glTF no termino")
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    require(bool(meshes), "No se importaron mallas")
    require(not any(obj.type == 'ARMATURE' for obj in bpy.context.scene.objects),
            "La entrada ya tiene esqueleto. Se esperaba un gato Tripo sin rig")
    angle = {'+x': -math.pi / 2, '-x': math.pi / 2, '+y': math.pi, '-y': 0.0}[front]
    rotation = Matrix.Rotation(angle, 4, 'Z')
    # Hornea la jerarquia importada en los vertices, antes de eliminar empties.
    transforms = {obj: rotation @ obj.matrix_world.copy() for obj in meshes}
    for obj in meshes:
        require(not obj.data.shape_keys, "La entrada tiene shape keys; no se admite este caso")
        obj.data = obj.data.copy()
        obj.data.transform(transforms[obj])
        obj.parent = None
        obj.matrix_world = Matrix.Identity(4)
    for obj in list(bpy.context.scene.objects):
        if obj not in meshes:
            bpy.data.objects.remove(obj, do_unlink=True)
    low, high = bounds(mesh_points(meshes))
    offset = Vector(((low.x + high.x) / 2, (low.y + high.y) / 2, low.z))
    for index, obj in enumerate(meshes):
        obj.name = "Orbita_malla_%02d" % index
        obj[TAG] = "mesh"
        obj.data.transform(Matrix.Translation(-offset))
        # Facetas planas; conserva UV, material y textura originales.
        for polygon in obj.data.polygons:
            polygon.use_smooth = False
        obj.data.update()
        require(bool(obj.data.uv_layers), "Faltan UV en " + obj.name)
    bpy.context.view_layer.update()
    bpy.context.scene["rig_gato_source"] = str(path)
    bpy.context.scene["rig_gato_front"] = front
    warn("Frente normalizado a -Y Blender / +Z glTF. Las unidades importadas se interpretan como metros.")
    return meshes


def measure_cat(meshes):
    points = mesh_points(meshes)
    low, high = bounds(points)
    width, length, height = high - low
    # Agrupa los vertices bajos por lado y por posicion longitudinal (cuatro apoyos).
    feet = {}
    for side, sign in [('L', 1), ('R', -1)]:
        samples = [p for p in points if p.z < low.z + .20 * height and sign * p.x > .035 * width]
        require(len(samples) >= 12, "No se pudieron medir patas del lado " + side)
        centers = [quantile([p.y for p in samples], q) for q in (.15, .85)]
        for unused in range(24):
            groups = [[p for p in samples if abs(p.y - centers[i]) <= abs(p.y - centers[1-i])]
                      for i in range(2)]
            require(all(len(g) >= 4 for g in groups), "Apoyos ambiguos: revisar pose del gato")
            new = [statistics.mean(p.y for p in g) for g in groups]
            if max(abs(a-b) for a, b in zip(new, centers)) < 1e-7:
                break
            centers = new
        ordered = sorted(groups, key=lambda g: statistics.mean(p.y for p in g))
        for kind, group in zip(('front', 'rear'), ordered):
            feet[kind + '.' + side] = Vector((statistics.median(p.x for p in group),
                                               statistics.median(p.y for p in group),
                                               quantile([p.z for p in group], .15)))
    front_y = statistics.mean(feet['front.' + side].y for side in ('L', 'R'))
    rear_y = statistics.mean(feet['rear.' + side].y for side in ('L', 'R'))
    require(rear_y - front_y > .12 * length,
            "No se distinguen cuatro apoyos. Se necesita pose de pie y frente correcto")
    mid_y = (front_y + rear_y) / 2
    torso = [p for p in points if abs(p.y-mid_y) < .14*length and p.z > .25*height]
    require(len(torso) >= 8, "No se pudo medir el torso")
    back_z = quantile([p.z for p in torso], .88)
    belly_z = quantile([p.z for p in torso], .15)
    spine_z = .72 * back_z + .28 * belly_z
    head = [p for p in points if p.y < front_y + .06*length and p.z > .58*height]
    require(len(head) >= 8, "No se pudo medir cabeza; compruebe --frente")
    head_center = Vector((0, statistics.median(p.y for p in head),
                          statistics.median(p.z for p in head)))
    head_center.y = min(head_center.y, front_y - .025*length)
    head_center.z = max(head_center.z, spine_z + .06*height)
    # Se sigue la cola en cortes posteriores; una cola curvada o elevada es fragil.
    tail_root = Vector((0, rear_y + .025*length, spine_z))
    tail_samples = [p for p in points if p.y > rear_y + .08*length]
    tail_path = [tail_root]
    if len(tail_samples) >= 10:
        end_y = quantile([p.y for p in tail_samples], .98)
        for i in range(1, 6):
            y = tail_root.y + (end_y-tail_root.y) * i/5
            slab = [p for p in tail_samples if abs(p.y-y) < .07*length]
            if slab:
                tail_path.append(Vector((statistics.median(p.x for p in slab), y,
                                         statistics.median(p.z for p in slab))))
    if len(tail_path) < 3:
        tail_path = [tail_root, tail_root + Vector((0, .22*length, .03*height)),
                     tail_root + Vector((0, .38*length, .10*height))]
        warn("Cola sin muestras suficientes: se uso una proporcion de respaldo; ajustar a mano.")
    measurements = {'bounds_min': list(low), 'bounds_max': list(high),
                    'size_m': list(high-low), 'front_y': front_y, 'rear_y': rear_y,
                    'spine_z': spine_z, 'back_z': back_z, 'belly_z': belly_z,
                    'head_center': list(head_center),
                    'feet': {k: list(v) for k, v in feet.items()},
                    'tail_path': [list(v) for v in tail_path]}
    bpy.context.scene['rig_gato_measures'] = json.dumps(measurements)
    log("Medidas geometricas (m): " + json.dumps(measurements, ensure_ascii=True))
    warn("Apoyos, articulaciones, cabeza y cola son estimaciones; no certifican anatomia ni una pose de pie.")
    if not (.15 <= height <= 1.5):
        warn("Altura importada poco habitual para un gato: %.4f m. Revisar escala del recurso." % height)
    return measurements


def interpolate(x, knots):
    knots = sorted(knots)
    index = next((i for i in range(len(knots)-1) if x <= knots[i+1][0]), len(knots)-2)
    a, b = knots[index], knots[index+1]
    require(abs(b[0]-a[0]) > 1e-8, "Referencias coincidentes al ajustar metarig")
    return a[1] + (b[1]-a[1]) * (x-a[0])/(b[0]-a[0])


def path_point(path, factor):
    distances = [(b-a).length for a, b in zip(path, path[1:])]
    target = sum(distances) * factor
    for a, b, distance in zip(path, path[1:], distances):
        if target <= distance:
            return a.lerp(b, target/max(distance, 1e-9))
        target -= distance
    return path[-1].copy()


def create_metarig(measures):
    # Carga el preset que pertenece al Rigify instalado; no copia codigo externo.
    try:
        preset = importlib.import_module("rigify.metarigs.Animals.cat")
    except ModuleNotFoundError:
        preset = importlib.import_module("rigify.metarigs.animals.cat")
    armature = bpy.data.armatures.new("Orbita_metarig")
    meta = bpy.data.objects.new("metarig", armature)
    bpy.context.collection.objects.link(meta)
    select_only([meta])
    preset.create(meta)
    if meta.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    meta[TAG] = "metarig"
    meta.show_in_front = True
    required = ['spine', 'spine.003', 'spine.004', 'spine.006', 'tail.001']
    required += [n + side for side in ('.L', '.R')
                 for n in ('thigh', 'shin', 'foot', 'r_toe', 'upper_arm', 'forearm', 'hand', 'f_toe')]
    require(all(name in armature.bones for name in required),
            "El preset Cat instalado cambio su estructura: falta un hueso esperado")
    # Conserva el cuerpo del Cat; elimina subarboles faciales y dedos individuales.
    remove = set()
    for bone in armature.bones:
        if bone.name == 'face' or bone.name.startswith(('f_palm.', 'r_palm.')):
            remove.add(bone.name)
            remove.update(child.name for child in bone.children_recursive)
    bpy.ops.object.mode_set(mode='EDIT')
    for name in remove:
        armature.edit_bones.remove(armature.edit_bones[name])
    edit = armature.edit_bones
    original = {b.name: (b.head.copy(), b.tail.copy(), b.z_axis.copy()) for b in edit}
    low, high = Vector(measures['bounds_min']), Vector(measures['bounds_max'])
    width, length, height = high-low
    front_y, rear_y, spine_z = (measures[k] for k in ('front_y', 'rear_y', 'spine_z'))
    head = Vector(measures['head_center'])
    # Deformacion por regiones de las proporciones del preset, seguida de patas.
    y_knots = [(original['spine.006'][1].y, head.y - .08*length),
               (original['spine.006'][0].y, head.y),
               (original['spine.004'][0].y, front_y - .01*length),
               (original['spine.003'][0].y, (front_y+rear_y)*.5),
               (original['spine'][0].y, rear_y + .025*length)]
    template_ground = min(p.z for pair in original.values() for p in pair[:2])
    template_back = original['spine'][0].z
    z_knots = [(template_ground, .012*height), (template_back, spine_z),
               (original['spine.006'][1].z, head.z + .10*height)]
    half_paw = statistics.mean(abs(measures['feet'][key][0]) for key in measures['feet'])
    x_scale = half_paw / max(abs(original['thigh.L'][0].x), 1e-5)

    def warp(p):
        return Vector((p.x*x_scale, interpolate(p.y, y_knots), interpolate(p.z, z_knots)))

    for bone in edit:
        a, b, axis = original[bone.name]
        bone.head, bone.tail = warp(a), warp(b)
        bone.align_roll(axis)
    for side in ('L', 'R'):
        for kind, names in [('front', ['upper_arm', 'forearm', 'hand', 'f_toe']),
                            ('rear', ['thigh', 'shin', 'foot', 'r_toe'])]:
            paw = Vector(measures['feet'][kind+'.'+side])
            x, y = paw.x, paw.y
            # Rodilla hacia delante, corvejon hacia atras; codo hacia atras.
            if kind == 'rear':
                joints = [Vector((x, y-.035*length, spine_z*.96)),
                          Vector((x, y-.11*length, spine_z*.60)),
                          Vector((x, y+.035*length, spine_z*.31)),
                          Vector((x, y+.015*length, .045*height)),
                          Vector((x, y-.055*length, .018*height))]
            else:
                joints = [Vector((x, y+.015*length, spine_z*.93)),
                          Vector((x, y+.065*length, spine_z*.52)),
                          Vector((x, y+.010*length, .070*height)),
                          Vector((x, y-.025*length, .035*height)),
                          Vector((x, y-.070*length, .018*height))]
            for index, name in enumerate(names):
                bone = edit[name+'.'+side]
                bone.head, bone.tail = joints[index], joints[index+1]
                bone.align_roll(original[bone.name][2])
    # Coloca cuello/cabeza y deja una longitud util para los controles.
    edit['spine.004'].tail = edit['spine.004'].head.lerp(head, .48)
    edit['spine.005'].head = edit['spine.004'].tail
    edit['spine.005'].tail = head
    edit['spine.006'].head = head
    edit['spine.006'].tail = head + Vector((0, -.12*length, .08*height))
    tails = sorted([b for b in edit if b.name.startswith('tail.')], key=lambda b: b.name)
    path = [Vector(p) for p in measures['tail_path']]
    for index, bone in enumerate(tails):
        bone.head = path_point(path, index/len(tails))
        bone.tail = path_point(path, (index+1)/len(tails))
        bone.align_roll(Vector((0, 0, 1)))
    # Restablece uniones exactas tras el ajuste de cada region.
    for bone in edit:
        if bone.use_connect and bone.parent:
            bone.head = bone.parent.tail
        require(bone.length > 1e-6, "Hueso colapsado: " + bone.name)
    bpy.ops.object.mode_set(mode='OBJECT')
    for pb in meta.pose.bones:
        params = pb.rigify_parameters
        # Un segmento lineal por hueso evita B-Bones incompatibles con glTF.
        for attr in ('segments', 'bbones'):
            if hasattr(params, attr):
                setattr(params, attr, 1)
    bpy.context.scene['rig_gato_stage'] = 'metarig'
    return meta


def generate_rig(meta):
    select_only([meta])
    before = set(bpy.data.objects)
    result = bpy.ops.pose.rigify_generate()
    require('FINISHED' in result, "Rigify no pudo generar el rig")
    rigs = [o for o in bpy.data.objects if o not in before and o.type == 'ARMATURE']
    require(len(rigs) == 1, "Rigify no produjo exactamente un esqueleto nuevo")
    rig = rigs[0]
    rig.name = 'Orbita_Rigify'
    rig[TAG] = 'rig'
    rig.show_in_front = True
    for bone in rig.data.bones:
        bone.use_deform = bone.name.startswith('DEF-')
        bone.bbone_segments = 1
    require(sum(b.use_deform for b in rig.data.bones) > 12, "Rig generado sin suficientes DEF")
    meta.hide_set(True)
    meta.hide_render = True
    bpy.context.scene['rig_gato_stage'] = 'rig'
    return rig


def soldar(meshes, umbral=0.0005):
    """Las mallas de Tripo traen vertices duplicados en las costuras UV: el calor de huesos
    (Bone Heat) falla sobre islas sueltas. Soldar conserva las UV (son por esquina).
    Probado en Blender 5.3 con PER-09: sin soldar quedaban 2 086 vertices sin peso."""
    import bmesh
    total = 0
    for obj in meshes:
        bm = bmesh.new()
        try:
            bm.from_mesh(obj.data)
            antes = len(bm.verts)
            bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=umbral)
            bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
            total += antes - len(bm.verts)
            bm.to_mesh(obj.data)
        finally:
            bm.free()
        obj.data.update()
    log('Vertices soldados antes de los pesos: %d' % total)


def bind_automatic(meshes, rig):
    soldar(meshes)
    select_only(meshes + [rig], rig)
    result = bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    require('FINISHED' in result, "Fallo al emparentar con pesos automaticos")
    # El operador puede emitir un aviso de Bone Heat y aun devolver FINISHED.
    for obj in meshes:
        modifiers = [m for m in obj.modifiers if m.type == 'ARMATURE' and m.object == rig]
        require(len(modifiers) == 1, "No hay un modificador Armature unico en " + obj.name)
        modifiers[0].use_deform_preserve_volume = False
    rellenar_pesos(meshes, rig)


def rellenar_pesos(meshes, rig):
    """Piezas finas sueltas (bigotes, medalla) quedan sin peso: copian los del vecino mas cercano
    que si tiene. Probado en Blender 5.3 con PER-09: 5 vertices de unos 1 400."""
    from mathutils.kdtree import KDTree
    deform = {b.name for b in rig.data.bones if b.use_deform}
    for obj in meshes:
        grupos = {g.index: g.name for g in obj.vertex_groups if g.name in deform}
        con_peso, sin_peso = [], []
        for v in obj.data.vertices:
            pesos = [(grupos[g.group], g.weight) for g in v.groups if g.group in grupos and g.weight > 1e-4]
            (con_peso if pesos else sin_peso).append((v.index, v.co.copy(), pesos))
        if not sin_peso or not con_peso:
            continue
        kd = KDTree(len(con_peso))
        for i, (_, co, _) in enumerate(con_peso):
            kd.insert(co, i)
        kd.balance()
        for indice, co, _ in sin_peso:
            _, i, _ = kd.find(co)
            for nombre, peso in con_peso[i][2]:
                obj.vertex_groups[nombre].add([indice], peso, 'REPLACE')
        log('Pesos copiados del vecino mas cercano en %s: %d vertices' % (obj.name, len(sin_peso)))


def validate_weights(meshes, rig):
    deform = {b.name for b in rig.data.bones if b.use_deform and b.name.startswith('DEF-')}
    stats = []
    for obj in meshes:
        require(obj.parent == rig, "La malla no esta emparentada con el rig: " + obj.name)
        require(any(m.type == 'ARMATURE' and m.object == rig for m in obj.modifiers),
                "Falta modificador Armature en " + obj.name)
        groups = {g.index: g.name for g in obj.vertex_groups}
        missing, maximum, used = [], 0, set()
        for vertex in obj.data.vertices:
            raw = [(groups.get(g.group), g.weight) for g in vertex.groups
                   if groups.get(g.group) in deform]
            require(all(math.isfinite(w) and w >= 0 for unused, w in raw), "Peso invalido")
            weights = [(name, weight) for name, weight in raw if weight > 1e-8]
            if sum(w for unused, w in weights) < 1e-6:
                missing.append(vertex.index)
            maximum = max(maximum, len(weights))
            used.update(n for n, unused in weights)
        require(not missing, "Pesos incompletos en %s: %d vertices sin DEF (ejemplos %s). "
                "Revisar Bone Heat, islas, solapes y Weight Paint en el blend de pesos."
                % (obj.name, len(missing), missing[:12]))
        require(len(used) >= 8, "Los pesos solo usan %d huesos en %s" % (len(used), obj.name))
        stats.append({'mesh': obj.name, 'vertices': len(obj.data.vertices),
                      'weighted_def_bones': len(used), 'max_influences_before_limit': maximum})
    return stats


def new_action(obj, name, frames):
    # API de acciones en capas/slots de Blender 5.2; no usa Action.fcurves.
    action = bpy.data.actions.new(name)
    action.use_fake_user = True
    action.use_frame_range = True
    action.frame_start, action.frame_end = 1, frames+1
    action.use_cyclic = True
    slot = action.slots.new(obj.id_type, obj.name)
    strip = action.layers.new('Movimiento').strips.new(type='KEYFRAME')
    bag = strip.channelbag(slot, ensure=True)
    ad = obj.animation_data_create()
    ad.action, ad.action_slot = action, slot
    return action, slot, bag


def finish_curves(bag):
    for curve in bag.fcurves:
        for key in curve.keyframe_points:
            key.interpolation = 'LINEAR'
        curve.modifiers.new(type='CYCLES')


def reset_pose(rig):
    for pb in rig.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)


def paw_skin_samples(meshes, rig, measures):
    """Plantas fijas en la malla de union, con los mismos cuatro pesos del GLB."""
    feet = {k: Vector(v) for k, v in measures['feet'].items()}
    samples = {k: [] for k in feet}
    allowed = {b.name for b in rig.data.bones if b.name.startswith('DEF-') and b.use_deform}
    for obj in meshes:
        names = {g.index: g.name for g in obj.vertex_groups if g.name in allowed}
        for vertex in obj.data.vertices:
            if vertex.co.z >= .12*measures['size_m'][2]:
                continue
            foot = min(feet, key=lambda k: (vertex.co-feet[k]).length_squared)
            weights = sorted([(names[g.group], g.weight) for g in vertex.groups
                              if g.group in names and g.weight > 1e-8],
                             key=lambda item: item[1], reverse=True)[:4]
            total = sum(w for unused, w in weights)
            require(total > 1e-8, 'Planta sin pesos DEF')
            samples[foot].append((vertex.co.copy(), [(n, w/total) for n, w in weights]))
    require(all(samples.values()), 'Faltan vertices de una planta')
    return samples


def paw_skin_heights(rig, samples):
    # El horneado elimina escala DEF. Medir aqui la misma piel evita corregir
    # solo el origen IK mientras los vertices de la planta atraviesan el suelo.
    ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    used = {n for group in samples.values() for unused, weights in group for n, unused in weights}
    skin = {}
    for name in used:
        loc, rot, unused = ev.pose.bones[name].matrix.decompose()
        skin[name] = Matrix.LocRotScale(loc, rot, None) @ rig.data.bones[name].matrix_local.inverted()
    return {k: min(sum(w*(skin[n] @ co).z for n, w in weights) for co, weights in group)
            for k, group in samples.items()}


def create_actions(rig, measures, meshes):
    controls = ['torso', 'chest', 'head', 'hand_ik.L', 'hand_ik.R', 'foot_ik.L', 'foot_ik.R']
    require(all(n in rig.pose.bones for n in controls),
            "Los controles del Cat cambiaron. Esperados: " + ', '.join(controls))
    tail = next((n for n in ('tail.001_master', 'tail_master', 'tail.001')
                 if n in rig.pose.bones), None)
    require(tail is not None, "No se encontro control de cola del Cat")
    controls.append(tail)
    ad = rig.animation_data_create()
    ad.action = None
    for track in list(ad.nla_tracks):
        ad.nla_tracks.remove(track)
    for pb in rig.pose.bones:
        if 'IK_FK' in pb:
            pb['IK_FK'] = 0.0
        if 'IK_Stretch' in pb:
            pb['IK_Stretch'] = 0.0
    reset_pose(rig)
    bpy.context.view_layer.update()
    # Referencias en espacio de armature, tomadas SIN acciones. En particular,
    # los IK conservan su altura de descanso; no son posiciones sobre Z=0.
    evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    rest_controls = {n: evaluated.pose.bones[n].matrix.copy() for n in controls}

    def place_control(name, matrix):
        pb = rig.pose.bones[name]
        # Convertir desde armature a canales locales usando el padre EVALUADO,
        # incluidas las restricciones de los padres MCH de Rigify.
        bpy.context.view_layer.update()
        ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
        kwargs = {}
        if pb.parent:
            kwargs = {'parent_matrix': ev.pose.bones[pb.parent.name].matrix,
                      'parent_matrix_local': pb.parent.bone.matrix_local}
        pb.matrix_basis = pb.bone.convert_local_to_pose(
            matrix, pb.bone.matrix_local, invert=True, **kwargs)

    height = measures['size_m'][2]
    # Semizancada de 9 % de la talla (antes ~2 %); elevacion de 8,5 %.
    # La separacion de apoyos limita el recorrido en otros modelos.
    stride = min(.09*height, .27*(measures['rear_y']-measures['front_y']))
    lift = .085*height
    plants = paw_skin_samples(meshes, rig, measures)
    floor = {k: min(co.z for co, unused in group) for k, group in plants.items()}
    feet = [('hand_ik.L', 'front.L', 0), ('foot_ik.R', 'rear.R', 0),
            ('hand_ik.R', 'front.R', math.pi), ('foot_ik.L', 'rear.L', math.pi)]
    actions = []
    for name, count in [('reposo', 2*FPS), ('caminar', FPS)]:
        reset_pose(rig)
        action, slot, bag = new_action(rig, 'CTRL_'+name, count)
        for frame in range(1, count+2):
            bpy.context.scene.frame_set(frame)
            reset_pose(rig)
            # El ultimo fotograma usa fase cero exacta, igual al primero.
            phase = 2*math.pi*((frame-1) % count)/count
            bpy.context.view_layer.update()
            if name == 'reposo':
                # Respiracion por desplazamiento leve, sin escalar cuello ni cabeza.
                displacement = .003*height*(1-math.cos(phase))*.5
            else:
                # Dos pulsos por ciclo; bajar levemente deja margen al IK sin estirar.
                displacement = height*(-.008 + .006*(1-math.cos(2*phase)))
            matrix = rest_controls['torso'].copy()
            matrix.translation.z += displacement
            place_control('torso', matrix)
            pb = rig.pose.bones[tail]
            pb.rotation_mode = 'QUATERNION'
            axis = pb.bone.matrix_local.to_3x3().inverted() @ Vector((0, 0, 1))
            amplitude = .12 if name == 'reposo' else .22
            pb.rotation_quaternion = Quaternion(axis.normalized(), amplitude*math.sin(phase))
            # Cabeza fija en espacio de armature, aunque el torso respire/suba.
            place_control('head', rest_controls['head'])
            bpy.context.view_layer.update()
            # Delantera L + trasera R juntas; la otra diagonal a medio ciclo.
            targets = {}
            for n, foot, offset in feet:
                matrix = rest_controls[n].copy()
                elevation = 0.0
                if name == 'caminar':
                    p = phase + offset
                    swing = max(0.0, math.sin(p))
                    elevation = lift*swing*swing
                    # De atras hacia delante durante recuperacion, y vuelta
                    # durante apoyo. La diagonal opuesta va medio ciclo despues.
                    matrix.translation += Vector((0, stride*math.cos(p), elevation))
                # Margen submilimetrico contra el arco de interpolacion entre
                # claves: el apoyo de caminar queda a <0,2 mm del reposo (talla 1 m).
                clearance = .00002 if name == 'reposo' else .00015
                targets[foot] = floor[foot] + elevation + clearance*height
                place_control(n, matrix)
            bpy.context.view_layer.update()
            # Compensar el minimo de la piel que se exportara, conservando la
            # orientacion y altura de referencia de cada control. No tocar pesos.
            for unused in range(12):
                actual = paw_skin_heights(rig, plants)
                if max(abs(targets[k]-actual[k]) for k in targets) < 2e-7*height:
                    break
                for n, foot, unused_offset in feet:
                    ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
                    matrix = ev.pose.bones[n].matrix.copy()
                    matrix.translation.z += targets[foot]-actual[foot]
                    place_control(n, matrix)
                bpy.context.view_layer.update()
            require(max(abs(targets[k]-paw_skin_heights(rig, plants)[k]) for k in targets)
                    < 2e-5*height, 'No convergio el apoyo de las plantas')
            for n in controls:
                pb = rig.pose.bones[n]
                pb.rotation_mode = 'QUATERNION'
                for prop in ('location', 'rotation_quaternion', 'scale'):
                    pb.keyframe_insert(data_path=prop, frame=frame, group=n)
            # Rigify guarda estas propiedades en *_parent, no en *_ik.
            # Keyarlas evita que valores externos cambien el modo al reproducir.
            for pb in rig.pose.bones:
                for prop in ('IK_FK', 'IK_Stretch'):
                    if prop in pb:
                        pb[prop] = 0.0
                        pb.keyframe_insert(data_path='["%s"]' % prop, frame=frame, group=pb.name)
        finish_curves(bag)
        actions.append((name, action, slot, count))
    ad.action = None
    reset_pose(rig)
    log("Acciones de control: reposo 2 s; caminar 1 s, diagonales y sin avance de raiz")
    return actions


def export_skeleton(rig):
    # Se reconstruye la jerarquia: cada DEF usa como padre su ancestro DEF mas cercano.
    # No basta export_def_bones: los ancestros no deformantes pueden conservarse.
    armature = bpy.data.armatures.new('Orbita_DEF')
    target = bpy.data.objects.new('Orbita_esqueleto', armature)
    bpy.context.collection.objects.link(target)
    target[TAG] = 'export'
    target.matrix_world = rig.matrix_world.copy()
    select_only([target])
    bpy.ops.object.mode_set(mode='EDIT')
    sources = [b for b in rig.data.bones if b.name.startswith('DEF-') and b.use_deform]
    for source in sources:
        bone = armature.edit_bones.new(source.name)
        # Un EditBone nuevo tiene longitud cero. Asignar matrix antes de darle
        # longitud perdia su direccion (quedaba +Z), cambiando la pose de union.
        # Copiar extremos y roll conserva la misma referencia que usa la piel.
        bone.head = source.head_local
        bone.tail = source.tail_local
        bone.align_roll(source.matrix_local.to_3x3().col[2])
        bone.use_deform = True
        bone.use_connect = False
        bone.inherit_scale = 'FULL'
    for source in sources:
        parent = source.parent
        while parent and parent.name not in armature.edit_bones:
            parent = parent.parent
        if parent:
            armature.edit_bones[source.name].parent = armature.edit_bones[parent.name]
    bpy.ops.object.mode_set(mode='OBJECT')
    for source in sources:
        copied = armature.bones[source.name]
        error = max(abs(copied.matrix_local[i][j]-source.matrix_local[i][j])
                    for i in range(4) for j in range(4))
        require(error < 1e-4 and abs(copied.length-source.length) < 1e-5,
                'La copia DEF cambio la pose de descanso: %s (matriz %.8g, longitud %.8g)' %
                (source.name, error, abs(copied.length-source.length)))
    target.show_in_front = True
    return target


def baked_actions(rig, target, actions):
    baked = []
    order = sorted(target.pose.bones, key=lambda pb: len(pb.parent_recursive))
    for name, action, slot, count in actions:
        rig.animation_data.action = action
        rig.animation_data.action_slot = slot
        baked_action, baked_slot, bag = new_action(target, name, count)
        previous = {}
        initial = None
        for frame in range(1, count+2):
            bpy.context.scene.frame_set(frame)
            bpy.context.view_layer.update()
            evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
            # Solo posicion y rotacion: Rigify estira huesos (escala no uniforme, incluso en reposo
            # tras el ajuste del metarig) y glTF no puede representar el cizallamiento que eso
            # produce en los hijos. Probado en Blender 5.3 con PER-09 (fallaba en DEF-forearm.L).
            desired = {}
            for pb in order:
                loc, rot, _ = evaluated.pose.bones[pb.name].matrix.decompose()
                desired[pb.name] = Matrix.LocRotScale(loc, rot, None)
            if frame == 1:
                initial = {n: m.copy() for n, m in desired.items()}
            if frame == count+1:
                gap = max(max(abs(desired[n][i][j]-initial[n][i][j]) for i in range(4)
                              for j in range(4)) for n in desired)
                require(gap < 1e-4, "El ciclo %s no cierra: error %.6g" % (name, gap))
            for pb in order:
                kwargs = {}
                if pb.parent:
                    kwargs = {'parent_matrix': desired[pb.parent.name],
                              'parent_matrix_local': pb.parent.bone.matrix_local}
                local = pb.bone.convert_local_to_pose(desired[pb.name], pb.bone.matrix_local,
                                                     invert=True, **kwargs)
                location, rotation, scale = local.decompose()
                # glTF no puede representar cizallamiento entre padres eliminados.
                rebuilt = Matrix.LocRotScale(location, rotation, scale)
                error = max(abs(local[i][j]-rebuilt[i][j]) for i in range(4) for j in range(4))
                require(error < 2e-4, "Cizallamiento no exportable en %s, %s frame %d. "
                        "Revisar escalas y rig." % (name, pb.name, frame))
                if pb.name in previous and rotation.dot(previous[pb.name]) < 0:
                    rotation.negate()
                previous[pb.name] = rotation.copy()
                pb.rotation_mode = 'QUATERNION'
                pb.location, pb.rotation_quaternion, pb.scale = location, rotation, scale
                for prop in ('location', 'rotation_quaternion', 'scale'):
                    pb.keyframe_insert(data_path=prop, frame=frame, group=pb.name)
        finish_curves(bag)
        baked.append((name, baked_action, baked_slot, count))
    rig.animation_data.action = None
    reset_pose(rig)
    target.animation_data.action = None
    reset_pose(target)
    for name, action, slot, count in baked:
        track = target.animation_data.nla_tracks.new()
        track.name = name
        strip = track.strips.new(name, 1, action)
        strip.action_slot = slot
        strip.action_frame_start, strip.action_frame_end = 1, count+1
        strip.frame_start, strip.frame_end = 1, count+1
        strip.extrapolation = 'NOTHING'
        strip.blend_type = 'REPLACE'
        # Los tracks se guardan silenciados para evitar sumar reposo y caminar.
        track.mute = True
    return baked


def validate_action_geometry(rig, actions, label):
    """Mide el depsgraph, no los canales ni solo las escalas de la accion."""
    samples = {'reposo': (1, 30), 'caminar': (1, 8, 15, 23)}
    prefixes = ('DEF-thigh.', 'DEF-shin.', 'DEF-foot.', 'DEF-r_toe.',
                'DEF-upper_arm.', 'DEF-forearm.', 'DEF-hand.', 'DEF-f_toe.',
                'DEF-shoulder.', 'DEF-pelvis.L', 'DEF-pelvis.R')
    bones = [b for b in rig.data.bones if b.name.startswith(prefixes)]
    require(len(bones) >= 16, 'Faltan huesos DEF de patas para medir')
    head, torso = 'DEF-spine.006', 'DEF-spine.003'
    reference_distance = (rig.data.bones[head].head_local -
                          rig.data.bones[torso].head_local).length
    rows = []
    columns = []
    measurements = {b.name: [b.length] for b in bones}
    measurements['cabeza-torso'] = [reference_distance]
    ad = rig.animation_data_create()
    for name, action, slot, count in actions:
        ad.action, ad.action_slot = action, slot
        # Se comprueba TODO el ciclo a 120 Hz, tambien entre claves de 30 fps.
        for tick in range(count*4+1):
            frame = 1 + tick/4
            bpy.context.scene.frame_set(int(frame), subframe=frame % 1)
            bpy.context.view_layer.update()
            ev = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
            lengths = {b.name: (ev.pose.bones[b.name].tail-ev.pose.bones[b.name].head).length
                       for b in bones}
            lengths['cabeza-torso'] = (ev.pose.bones[head].head-ev.pose.bones[torso].head).length
            for bone, length in lengths.items():
                reference = measurements[bone][0]
                change = abs(length/reference-1)*100
                require(math.isfinite(change) and change < 5,
                        '%s: %s %d, %s cambia %.4f %% (limite <5 %%)' %
                        (label, name, frame, bone, change))
                rows.append({'rig': label, 'action': name, 'frame': frame, 'bone': bone,
                             'rest_m': reference, 'evaluated_m': length, 'difference_pct': change})
                if frame in samples[name]:
                    measurements[bone].append(length)
            if frame in samples[name]:
                columns.append('%s:%d' % (name, frame))
    log('MEDIDAS %s (metros; cabeza-torso = origen DEF-spine.006 a DEF-spine.003)' % label)
    print('hueso | descanso | ' + ' | '.join(columns), flush=True)
    for name, values in measurements.items():
        print(name + ' | ' + ' | '.join('%.6f' % value for value in values), flush=True)
    log('%s: maxima diferencia en todo el ciclo %.6f %%' %
        (label, max(row['difference_pct'] for row in rows)))
    ad.action = None
    reset_pose(rig)
    bpy.context.view_layer.update()
    return rows


def validate_paw_contacts(target, meshes, actions, measures, path):
    """Mide vertices deformados a 120 Hz, incluidos los intervalos entre claves."""
    feet = {k: Vector(v) for k, v in measures['feet'].items()}
    groups = {k: [] for k in feet}
    height = measures['size_m'][2]
    for obj in meshes:
        for vertex in obj.data.vertices:
            if vertex.co.z < .12*height:
                foot = min(feet, key=lambda k: (vertex.co-feet[k]).length_squared)
                groups[foot].append((obj.name, vertex.index))
    floor = {k: min(bpy.data.objects[n].data.vertices[i].co.z for n, i in group)
             for k, group in groups.items()}
    rows = []
    for name, action, slot, count in actions:
        target.animation_data.action, target.animation_data.action_slot = action, slot
        for tick in range(count*4+1):
            frame = 1 + tick/4
            bpy.context.scene.frame_set(int(frame), subframe=frame % 1)
            bpy.context.view_layer.update()
            vertices = {}
            dg = bpy.context.evaluated_depsgraph_get()
            for obj in meshes:
                ev = obj.evaluated_get(dg)
                mesh = ev.to_mesh()
                vertices[obj.name] = [ev.matrix_world @ v.co for v in mesh.vertices]
                ev.to_mesh_clear()
            minima = {k: min(vertices[n][i].z for n, i in group) for k, group in groups.items()}
            rows.append({'action': name, 'frame': frame, 'time_s': (frame-1)/FPS,
                         'minimums_m': minima})
    rest_min = {k: min(r['minimums_m'][k] for r in rows if r['action'] == 'reposo') for k in feet}
    support_error = 0.0
    for row in rows:
        for k in feet:
            value = row['minimums_m'][k]
            require(value >= floor[k]-2e-6*height, 'Planta bajo el suelo: %s %s %.4f' %
                    (k, row['action'], row['frame']))
            if row['action'] == 'caminar':
                require(value >= rest_min[k]-2e-6*height,
                        'Planta de caminar por debajo de reposo: ' + k)
                offset = 0 if k in ('front.L', 'rear.R') else math.pi
                swing = math.sin(2*math.pi*row['time_s']+offset)
                if swing <= 1e-8:
                    error = abs(value-rest_min[k])
                    support_error = max(support_error, error)
                    require(error < .0002*height, 'Apoyo separado del reposo: ' + k)
    for name in ('reposo', 'caminar'):
        cycle = [r for r in rows if r['action'] == name]
        require(max(abs(cycle[0]['minimums_m'][k]-cycle[-1]['minimums_m'][k]) for k in feet)
                < 2e-6*height, 'No cierra la piel de las plantas: ' + name)
    data = {'bind_floor_m': floor, 'rest_minimums_m': rest_min,
            'vertices_per_foot': {k: len(v) for k, v in groups.items()},
            'sample_hz': 4*FPS, 'support_max_error_m': support_error, 'samples': rows}
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    WRITTEN.append(str(path))
    lines = ['# Alturas minimas de las plantas', '',
             'Vertices deformados de la copia DEF de exportacion; metros, muestreo a 120 Hz.',
             'Grupos fijos: vertices bajo 12 % de la talla, asignados al apoyo mas cercano.',
             'Tolerancia de apoyo: 0,2 mm por metro de talla; tolerancia numerica: 0,002 mm.', '',
             '| Instante | Delantera L | Delantera R | Trasera L | Trasera R |',
             '|---|---:|---:|---:|---:|']
    order = ('front.L', 'front.R', 'rear.L', 'rear.R')
    lines.append('| Minimo reposo | ' + ' | '.join('%.7f' % rest_min[k] for k in order) + ' |')
    for row in rows:
        if row['action'] == 'caminar' and row['frame'] in (1, 6, 11, 16, 21, 26, 31):
            lines.append('| %.6f s | ' % row['time_s'] +
                         ' | '.join('%.7f' % row['minimums_m'][k] for k in order) + ' |')
    lines += ['', 'Error maximo de apoyo respecto de reposo: %.7f m.' % support_error,
              'Ninguna planta de caminar baja del minimo de reposo en las muestras.', '']
    path.with_suffix('.md').write_text('\n'.join(lines), encoding='utf-8')
    WRITTEN.append(str(path.with_suffix('.md')))
    log('PLANTAS_VALIDAS: 120 Hz; apoyo maximo %.7f m respecto a reposo' % support_error)
    target.animation_data.action = None
    reset_pose(target)
    return support_error


def render_action_checks(target, meshes, actions, directory):
    scene = bpy.context.scene
    old_camera, old_engine = scene.camera, scene.render.engine
    visibility = {o: o.hide_render for o in scene.objects}
    camera_data = bpy.data.cameras.new('Revision_lateral')
    camera = bpy.data.objects.new('Revision_lateral', camera_data)
    scene.collection.objects.link(camera)
    try:
        for obj in scene.objects:
            obj.hide_render = obj not in meshes and obj != camera
        camera_data.type = 'ORTHO'
        points = mesh_points(meshes)
        low, high = bounds(points)
        center = (low+high)/2
        camera.location = center + Vector((3*max(high-low), 0, 0))
        camera.rotation_euler = (center-camera.location).to_track_quat('-Z', 'Y').to_euler()
        camera_data.ortho_scale = 1.35*max(high.z-low.z, high.y-low.y)
        scene.camera = camera
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.render.resolution_x, scene.render.resolution_y = 1000, 1000
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'TEXTURE'
        scene.display.shading.show_shadows = True
        scene.display.shading.show_cavity = True
        scene.display.shading.background_type = 'WORLD'
        scene.world.color = (.12, .12, .12)
        for name, action, slot, unused in actions:
            frame = 1 if name == 'reposo' else 8
            target.animation_data.action, target.animation_data.action_slot = action, slot
            scene.frame_set(frame)
            path = directory / ('gato_%s_f%02d.png' % (name, frame))
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            require(path.is_file(), 'No se guardo el render ' + str(path))
            WRITTEN.append(str(path))
    finally:
        target.animation_data.action = None
        reset_pose(target)
        for obj, hidden in visibility.items():
            obj.hide_render = hidden
        scene.camera, scene.render.engine = old_camera, old_engine
        bpy.data.objects.remove(camera, do_unlink=True)
        bpy.data.cameras.remove(camera_data)


def export_meshes(meshes, target):
    result = []
    allowed = {b.name for b in target.data.bones}
    for source in meshes:
        obj = source.copy()
        obj.data = source.data.copy()
        bpy.context.collection.objects.link(obj)
        obj.name = source.name + '_GLB'
        obj[TAG] = 'export'
        world = source.matrix_world.copy()
        obj.parent = target
        obj.matrix_world = world
        for modifier in list(obj.modifiers):
            if modifier.type == 'ARMATURE':
                obj.modifiers.remove(modifier)
        modifier = obj.modifiers.new('Deformacion DEF', 'ARMATURE')
        modifier.object = target
        modifier.use_deform_preserve_volume = False
        for group in list(obj.vertex_groups):
            if group.name not in allowed:
                obj.vertex_groups.remove(group)
        # Limite explicito de cuatro influencias para el motor. No altera el original.
        indices = {g.index: g for g in obj.vertex_groups}
        for vertex in obj.data.vertices:
            all_groups = [g.group for g in vertex.groups]
            weights = sorted([(g.group, g.weight) for g in vertex.groups if g.weight > 1e-8],
                             key=lambda item: item[1], reverse=True)
            keep = weights[:4]
            total = sum(w for unused, w in keep)
            require(total > 1e-8, 'Vertice sin peso en copia exportable')
            kept_indices = {index for index, unused in keep}
            for index in all_groups:
                if index not in kept_indices:
                    indices[index].remove([vertex.index])
            for index, weight in keep:
                indices[index].add([vertex.index], weight/total, 'REPLACE')
        result.append(obj)
    return result


def accessor_values(doc, binary, index):
    accessor = doc['accessors'][index]
    require(not accessor.get('sparse'), 'Validador GLB: accessor sparse inesperado')
    view = doc['bufferViews'][accessor['bufferView']]
    require(view.get('buffer', 0) == 0, 'Validador GLB: buffer externo inesperado')
    formats = {5121: 'B', 5123: 'H', 5125: 'I', 5126: 'f'}
    counts = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}
    fmt = '<' + formats[accessor['componentType']] * counts[accessor['type']]
    size = struct.calcsize(fmt)
    stride = view.get('byteStride', size)
    start = view.get('byteOffset', 0) + accessor.get('byteOffset', 0)
    return [struct.unpack_from(fmt, binary, start+i*stride) for i in range(accessor['count'])]


def read_glb(path):
    with path.open('rb') as handle:
        header = handle.read(12)
        require(len(header) == 12, 'GLB truncado')
        magic, version, total = struct.unpack('<4sII', header)
        require(magic == b'glTF' and version == 2 and total == path.stat().st_size, 'Cabecera GLB invalida')
        doc, binary = None, None
        while handle.tell() < total:
            size, kind = struct.unpack('<II', handle.read(8))
            data = handle.read(size)
            require(len(data) == size, 'Chunk GLB truncado')
            if kind == 0x4E4F534A:
                doc = json.loads(data)
            elif kind == 0x004E4942:
                binary = data
    require(doc is not None and binary is not None, 'GLB sin JSON o BIN')
    return doc, binary


def inspect_glb(path, expected_triangles):
    doc, binary = read_glb(path)
    nodes = doc.get('nodes', [])
    skins = doc.get('skins', [])
    require(len(skins) == 1, 'El GLB debe contener un unico skin')
    joints = skins[0]['joints']
    require(all(nodes[j].get('name', '').startswith('DEF-') for j in joints),
            'Se exportaron joints que no son DEF')
    require(not any(n.get('name', '').startswith(('ORG-', 'MCH-')) for n in nodes),
            'Se filtraron controles/mecanismos al GLB')
    triangles = 0
    for mesh in doc.get('meshes', []):
        for primitive in mesh['primitives']:
            require(primitive.get('mode', 4) == 4, 'Primitiva GLB no triangular')
            attrs = primitive['attributes']
            require('JOINTS_0' in attrs and 'WEIGHTS_0' in attrs, 'Malla exportada sin skinning')
            weights = accessor_values(doc, binary, attrs['WEIGHTS_0'])
            # El exportador usa pesos FLOAT con esta configuracion.
            require(doc['accessors'][attrs['WEIGHTS_0']]['componentType'] == 5126,
                    'Validador: pesos cuantizados inesperados')
            require(all(all(math.isfinite(x) and x >= 0 for x in row) and abs(sum(row)-1) < 1e-4
                        for row in weights), 'Pesos GLB invalidos o sin normalizar')
            index = primitive.get('indices', attrs['POSITION'])
            triangles += doc['accessors'][index]['count'] // 3
    require(triangles == expected_triangles, 'Cambio inesperado de triangulos: %d -> %d'
            % (expected_triangles, triangles))
    animations = doc.get('animations', [])
    require(len(animations) == 2 and {a.get('name') for a in animations} == {'reposo', 'caminar'},
            'El GLB no contiene exactamente reposo y caminar; trae %s'
            % [(a.get('name'), len(a.get('channels', []))) for a in animations])
    durations = {}
    for animation in animations:
        require(bool(animation.get('channels')), 'Animacion sin canales')
        require(all(c['target'].get('node') in joints for c in animation['channels']),
                'Canal de animacion fuera de huesos DEF')
        starts, ends = [], []
        varying = False
        for sampler in animation['samplers']:
            times = accessor_values(doc, binary, sampler['input'])
            values = accessor_values(doc, binary, sampler['output'])
            starts.append(times[0][0])
            ends.append(times[-1][0])
            varying |= any(max(abs(x-y) for x, y in zip(row, values[0])) > 1e-5 for row in values[1:])
            # Quaternion q y -q representan la misma orientacion.
            gap = max(abs(x-y) for x, y in zip(values[0], values[-1]))
            if len(values[0]) == 4:
                gap = min(gap, max(abs(x+y) for x, y in zip(values[0], values[-1])))
            require(gap < 3e-4, 'El GLB no cierra el ciclo ' + animation['name'])
        duration = max(ends)-min(starts)
        require(varying, 'Animacion completamente estatica: ' + animation['name'])
        expected = 2 if animation['name'] == 'reposo' else 1
        require(abs(duration-expected) < 1e-4, 'Duracion incorrecta en ' + animation['name'])
        durations[animation['name']] = round(duration, 6)
    require(bool(doc.get('images')) and all('bufferView' in i for i in doc['images']),
            'El GLB no contiene las texturas embebidas')
    return {'triangles': triangles, 'def_joints': len(joints), 'animations_seconds': durations,
            'embedded_images': len(doc['images']), 'glb_bytes': path.stat().st_size}


def validate_export_skin(path, target, actions):
    """Verifica transformaciones de piel reales del GLB contra el DEF evaluado.

    Las longitudes solas no detectan el fallo original: una orientacion de union
    erronea puede girar la piel 180 grados y conservar la longitud del hueso.
    """
    doc, binary = read_glb(path)
    nodes, skin = doc['nodes'], doc['skins'][0]
    parents = {child: i for i, node in enumerate(nodes) for child in node.get('children', [])}
    inverse_bind = [Matrix([row[i:i+4] for i in range(0, 16, 4)]).transposed()
                    for row in accessor_values(doc, binary, skin['inverseBindMatrices'])]
    conversion = Matrix.Rotation(-math.pi/2, 4, 'X')
    samples = {'reposo': (1, 30), 'caminar': (1, 8, 15, 23)}
    maximum = 0.0
    try:
        for name, action, slot, unused in actions:
            animation = next(a for a in doc['animations'] if a['name'] == name)
            target.animation_data.action, target.animation_data.action_slot = action, slot
            for frame in samples[name]:
                local = {i: dict(node) for i, node in enumerate(nodes)}
                for channel in animation['channels']:
                    sampler = animation['samplers'][channel['sampler']]
                    times = accessor_values(doc, binary, sampler['input'])
                    values = accessor_values(doc, binary, sampler['output'])
                    seconds = (frame-1)/FPS
                    index = min(range(len(times)), key=lambda i: abs(times[i][0]-seconds))
                    require(abs(times[index][0]-seconds) < 1e-5, 'Falta muestra GLB para medir skin')
                    local[channel['target']['node']][channel['target']['path']] = values[index]
                cache = {}

                def world(index):
                    if index not in cache:
                        node = local[index]
                        if 'matrix' in node:
                            m = Matrix([node['matrix'][i:i+4] for i in range(0, 16, 4)]).transposed()
                        else:
                            q = node.get('rotation', (0, 0, 0, 1))
                            m = Matrix.LocRotScale(Vector(node.get('translation', (0, 0, 0))),
                                                   Quaternion((q[3], *q[:3])),
                                                   Vector(node.get('scale', (1, 1, 1))))
                        cache[index] = world(parents[index]) @ m if index in parents else m
                    return cache[index]

                bpy.context.scene.frame_set(frame)
                bpy.context.view_layer.update()
                ev = target.evaluated_get(bpy.context.evaluated_depsgraph_get())
                for joint, ibm in zip(skin['joints'], inverse_bind):
                    bone = nodes[joint]['name']
                    expected = (conversion @ ev.pose.bones[bone].matrix @
                                target.data.bones[bone].matrix_local.inverted() @ conversion.inverted())
                    actual = world(joint) @ ibm
                    error = max(abs(actual[i][j]-expected[i][j]) for i in range(4) for j in range(4))
                    maximum = max(maximum, error)
                    require(error < 2e-4, 'Skin GLB distinto del DEF: %s %d %s (%.8g)' %
                            (name, frame, bone, error))
        log('Matrices de piel GLB: %d joints x 6 muestras; error maximo %.8g' %
            (len(skin['joints']), maximum))
        return maximum
    finally:
        target.animation_data.action = None
        reset_pose(target)
        bpy.context.view_layer.update()


def write_measurement_table(path, rows):
    samples = [('reposo', 1), ('reposo', 30), ('caminar', 1), ('caminar', 8),
               ('caminar', 15), ('caminar', 23)]
    lines = ['# Medidas del gato', '',
             'Metros. Referencia: pose de descanso de los huesos. Se valida cada fotograma de ambos ciclos.',
             'Cabeza-torso: distancia entre los origenes de DEF-spine.006 y DEF-spine.003.', '']
    for label in ('Rigify', 'DEF_exportacion'):
        group = [r for r in rows if r['rig'] == label]
        lines += ['## ' + label, '',
                  '| Hueso | Descanso | ' + ' | '.join('%s %d' % s for s in samples) + ' |',
                  '|---|' + '---:|' * 7]
        for bone in dict.fromkeys(r['bone'] for r in group):
            values = [r for r in group if r['bone'] == bone]
            measured = [next(r['evaluated_m'] for r in values if (r['action'], r['frame']) == s)
                        for s in samples]
            lines.append('| %s | %s |' % (bone, ' | '.join('%.6f' % v for v in
                                                         [values[0]['rest_m']] + measured)))
        lines += ['', 'Diferencia maxima en todo el ciclo: %.6f %%.' %
                  max(r['difference_pct'] for r in group), '']
    path.write_text('\n'.join(lines), encoding='utf-8')
    WRITTEN.append(str(path))


def triangle_count(meshes):
    total = 0
    for obj in meshes:
        obj.data.calc_loop_triangles()
        total += len(obj.data.loop_triangles)
    return total


def write_glb(path, target, meshes, triangles, actions):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path(path.with_name(path.stem + '.validando.glb'), '.glb')
    select_only(meshes+[target], target)
    tracks = list(target.animation_data.nla_tracks)
    try:
        # El exportador evalua cada pista horneada de manera independiente.
        for track in tracks:
            track.mute = False
        result = bpy.ops.export_scene.gltf(
            filepath=str(temporary), check_existing=False, export_format='GLB',
            use_selection=True, export_yup=True, export_apply=False,
            export_texcoords=True, export_normals=True, export_materials='EXPORT',
            export_image_format='AUTO', export_cameras=False, export_lights=False,
            export_skins=True, export_def_bones=True, export_leaf_bone=False,
            export_influence_nb=4, export_all_influences=False,
            # NLA_TRACKS: solo las pistas horneadas (reposo y caminar). Con ACTIONS tambien salian
            # CTRL_reposo y CTRL_caminar del rig de control (probado en Blender 5.3).
            export_animations=True, export_animation_mode='NLA_TRACKS',
            export_nla_strips=True, export_frame_range=False, export_frame_step=1,
            export_force_sampling=True, export_anim_slide_to_zero=True,
            export_merge_animation='ACTION', export_optimize_animation_size=False,
            export_morph=False, export_morph_animation=False)
        require('FINISHED' in result and temporary.is_file(), 'El exportador glTF no termino')
        info = inspect_glb(temporary, triangles)
        for track in tracks:
            track.mute = True
        info['max_glb_skin_matrix_error'] = validate_export_skin(temporary, target, actions)
        os.replace(temporary, path)
        WRITTEN.append(str(path))
        return info
    finally:
        for track in tracks:
            track.mute = True
        if temporary.exists():
            temporary.unlink()


def resume(path):
    require(path.is_file() and path.suffix.lower() == '.blend', 'Blend para reanudar inexistente')
    bpy.ops.wm.open_mainfile(filepath=str(path))
    require(bpy.context.scene.get('rig_gato_stage') in ('metarig', 'rig'),
            'El blend no es un punto de control de rig_gato.py')
    enable_rigify()
    # Borra unicamente las copias etiquetadas que pertenecen a este script.
    for obj in list(bpy.data.objects):
        if obj.get(TAG) == 'export':
            bpy.data.objects.remove(obj, do_unlink=True)
    meshes = [o for o in bpy.context.scene.objects if o.get(TAG) == 'mesh']
    metas = [o for o in bpy.context.scene.objects if o.get(TAG) == 'metarig']
    rigs = [o for o in bpy.context.scene.objects if o.get(TAG) == 'rig']
    require(meshes and len(metas) == 1 and len(rigs) <= 1, 'Punto de control ambiguo o incompleto')
    require(all(o.type == 'MESH' for o in meshes), 'Etiqueta mesh en objeto incorrecto')
    measures = json.loads(bpy.context.scene['rig_gato_measures'])
    for obj in meshes + metas + rigs:
        require(max(abs(obj.matrix_world[i][j] - (1 if i == j else 0))
                    for i in range(4) for j in range(4)) < 1e-5,
                'Se cambio una transformacion de objeto. Editar huesos en Edit Mode y conservar objetos identidad: '
                + obj.name)
    require((bpy.context.scene['rig_gato_stage'] == 'rig') == bool(rigs),
            'Etapa inconsistente: no generar Rigify manualmente; dejarlo al script')
    return meshes, metas[0], rigs[0] if rigs else None, measures


def main():
    args = arguments()
    # instalado: Blender 5.3 (2026-11-12); se escribio contra la API 5.2, que la 5.3 conserva
    require(bpy.app.version[:2] >= (5, 2),
            'Se requiere Blender 5.2 o posterior; encontrado ' + bpy.app.version_string)
    output = output_path(args.salida, '.glb')
    blend = output_path(args.guardar_blend, '.blend') if args.guardar_blend else None
    input_path = (args.entrada or args.reanudar).resolve()
    planned = [output, output.with_name(output.stem+'.validando.glb')]
    if blend:
        planned += [blend, blend.with_name(blend.stem+'.metarig.blend'),
                    blend.with_name(blend.stem+'.pesos.blend')]
    planned = [p.resolve() for p in planned]
    require(all(p.is_relative_to(ROOT) for p in planned), 'Una salida derivada sale de herramientas/blender')
    require(input_path not in planned, 'Una salida pisaria el archivo de entrada; use otro nombre')
    # El metarig puede necesitar auto-run al abrirse; aqui Rigify se habilita explicitamente.
    if args.reanudar:
        meshes, meta, rig, measures = resume(input_path)
    else:
        enable_rigify()
        meshes = import_cat(input_path, args.frente)
        measures = measure_cat(meshes)
        meta = create_metarig(measures)
        rig = None
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.render.fps, scene.render.fps_base = FPS, 1.0
    scene.frame_start, scene.frame_end = 1, 2*FPS+1
    triangles = triangle_count(meshes)
    if args.solo_metarig:
        select_only([meta])
        save_blend(blend)
        return {'status': 'METARIG_PARA_REVISION', 'triangles': triangles,
                'metarig_bones': len(meta.data.bones), 'rig_bones': 0, 'actions': []}
    if rig is None:
        if blend:
            select_only([meta])
            save_blend(blend.with_name(blend.stem+'.metarig.blend'))
        log('Generando Rigify Cat')
        rig = generate_rig(meta)
        log('Emparentando con pesos automaticos')
        bind_automatic(meshes, rig)
        # soldar quita triangulos degenerados (PER-09: 2733 -> 2729): la cuenta de control es la de ahora
        triangles = triangle_count(meshes)
    # Guarda incluso pesos defectuosos para corregirlos y continuar con --reanudar.
    if blend:
        save_blend(blend.with_name(blend.stem+'.pesos.blend'))
    weight_stats = validate_weights(meshes, rig)
    # Elimina solo acciones creadas anteriormente por esta herramienta.
    # Se limpian antes sus usuarios en el rig y en las copias ya eliminadas.
    rig.animation_data_create().action = None
    for track in list(rig.animation_data.nla_tracks):
        rig.animation_data.nla_tracks.remove(track)
    for action in list(bpy.data.actions):
        if action.get('rig_gato_action'):
            bpy.data.actions.remove(action, do_unlink=True)
    actions = create_actions(rig, measures, meshes)
    for unused, action, unused_slot, unused_count in actions:
        action['rig_gato_action'] = True
    geometry = validate_action_geometry(rig, actions, 'Rigify')
    log('Creando copia DEF y horneando acciones')
    target = export_skeleton(rig)
    baked = baked_actions(rig, target, actions)
    for unused, action, unused_slot, unused_count in baked:
        action['rig_gato_action'] = True
    geometry += validate_action_geometry(target, baked, 'DEF_exportacion')
    report = output.with_name(output.stem + '.medidas.json')
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(geometry, ensure_ascii=True, indent=2), encoding='utf-8')
    WRITTEN.append(str(report))
    write_measurement_table(report.with_suffix('.md'), geometry)
    copies = export_meshes(meshes, target)
    support_error = validate_paw_contacts(target, copies, baked, measures,
                                         output.with_name(output.stem + '.plantas.json'))
    scene.frame_set(1)
    info = write_glb(output, target, copies, triangles, baked)
    if args.render_pruebas:
        render_action_checks(target, copies, baked, output.parent)
    # El blend final abre el rig editable; oculta las copias de exportacion.
    for obj in copies+[target]:
        obj.hide_set(True)
        obj.hide_render = True
    rig.animation_data.action = actions[0][1]
    rig.animation_data.action_slot = actions[0][2]
    select_only([rig])
    scene.frame_set(1)
    if blend:
        save_blend(blend)
    warn('glTF no codifica repeticion infinita: activar Loop en Godot para reposo y caminar.')
    warn('Geometria animada medida en Blender; falta revisar el recurso corregido dentro de Godot.')
    return {'status': 'GLB_VALIDADO_ESTRUCTURALMENTE', 'triangles': triangles,
            'metarig_bones': len(meta.data.bones), 'rig_bones': len(rig.data.bones),
            'actions': ['reposo', 'caminar'], 'weights': weight_stats,
            'max_paw_support_error_m': support_error,
            'max_geometry_difference_pct': max(r['difference_pct'] for r in geometry), **info}


if __name__ == '__main__':
    try:
        summary = main()
        summary.update(files_written=WRITTEN, warnings=WARNINGS,
                       blender_version=bpy.app.version_string)
        print('RESUMEN_RIG_GATO=' + json.dumps(summary, ensure_ascii=True, sort_keys=True), flush=True)
    except Exception as exc:
        print('ERROR_RIG_GATO: ' + str(exc), file=sys.stderr, flush=True)
        print('RESUMEN_RIG_GATO=' + json.dumps({'status': 'ERROR', 'error': str(exc),
              'files_written': WRITTEN, 'warnings': WARNINGS}, ensure_ascii=True), flush=True)
        traceback.print_exc()
        # --python-exit-code 1 garantiza estado de fallo tambien desde automatizaciones.
        raise
