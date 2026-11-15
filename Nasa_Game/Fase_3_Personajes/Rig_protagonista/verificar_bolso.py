"""Verificacion independiente del criterio e): cuanto se mete el bolso en el cuerpo en cada clip.

No usa el codigo de rig_protagonista.py: importa el GLB ya exportado, reproduce cada clip con Blender y, cada
dos cuadros, cuenta los vertices del bolso que quedan DENTRO del cuerpo deformado. "Dentro" se decide por
paridad de cruces de tres rayos (mayoria de 2 sobre 3), que no depende de la normal del triangulo mas cercano.
La hondura es la distancia de esos vertices a la superficie mas cercana del cuerpo.

Uso:
  blender -b --factory-startup --python-exit-code 1 --python verificar_bolso.py -- --glb <PER-01_rig.glb> --salida <json>
"""
import argparse
import json
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

FPS = 50
RAYOS = [Vector((0.321, 0.557, 0.766)).normalized(), Vector((-0.642, 0.283, -0.713)).normalized(),
         Vector((0.119, -0.932, 0.342)).normalized()]


def argumentos():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--glb", required=True)
    p.add_argument("--salida", required=True)
    return p.parse_args(argv)


def malla_evaluada(obj, grafo):
    ev = obj.evaluated_get(grafo)
    m = ev.to_mesh()
    mw = ev.matrix_world
    pos = [mw @ v.co for v in m.vertices]
    m.calc_loop_triangles()
    tri = [tuple(t.vertices) for t in m.loop_triangles]
    ev.to_mesh_clear()
    return pos, tri


def cruces(arbol, origen, direccion):
    n, o = 0, origen
    while n < 64:
        loc, _, _, _ = arbol.ray_cast(o, direccion)
        if loc is None:
            break
        n += 1
        o = loc + direccion * 1e-5
    return n


def medir(cuerpo, bolso, grafo):
    pc, tc = malla_evaluada(cuerpo, grafo)
    pb, _ = malla_evaluada(bolso, grafo)
    arbol = BVHTree.FromPolygons(pc, tc)
    dentro, hondo, partes = 0, 0.0, {}
    for v in pb:
        votos = sum(cruces(arbol, v, d) % 2 for d in RAYOS)
        if votos >= 2:
            dentro += 1
            loc, _, indice, dist = arbol.find_nearest(v)
            hondo = max(hondo, dist)
            # parte del cuerpo que lo envuelve: hueso de mas peso del vertice mas cercano de ese triangulo
            cerca = min(tc[indice], key=lambda i: (pc[i] - v).length)
            grupos = cuerpo.data.vertices[cerca].groups
            if grupos:
                hueso = cuerpo.vertex_groups[max(grupos, key=lambda g: g.weight).group].name
                partes[hueso] = partes.get(hueso, 0) + 1
    medir.partes = partes
    return dentro, hondo, len(pb)


def main():
    a = argumentos()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene
    escena.render.fps, escena.render.fps_base = FPS, 1.0
    bpy.ops.import_scene.gltf(filepath=a.glb)
    armadura = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    cuerpo = next(o for o in bpy.data.objects if o.type == "MESH" and "cuerpo" in o.name)
    bolso = next(o for o in bpy.data.objects if o.type == "MESH" and "bolso" in o.name)
    ad = armadura.animation_data
    for pista in ad.nla_tracks:
        pista.mute = True
    res = {}
    # pose de union: sin accion y con los huesos en reposo
    ad.action = None
    for h in armadura.pose.bones:
        h.matrix_basis.identity()
    escena.frame_set(0)
    n, h, total = medir(cuerpo, bolso, bpy.context.evaluated_depsgraph_get())
    res["pose_de_union"] = {"vertices_dentro": n, "hondura_max_m": round(h, 4), "vertices_bolso": total}
    for accion in bpy.data.actions:
        nombre = accion.name.split(".")[0]
        ad.action = accion
        if hasattr(ad, "action_slot") and accion.slots:
            ad.action_slot = accion.slots[0]
        f0, f1 = (int(round(x)) for x in accion.frame_range)
        peor_n, peor_h, peor_t, suma, peor_partes = 0, 0.0, 0.0, 0, {}
        cuadros = list(range(f0, f1 + 1, 2))
        for f in cuadros:
            escena.frame_set(f)
            n, h, _ = medir(cuerpo, bolso, bpy.context.evaluated_depsgraph_get())
            suma += n
            if n > peor_n:
                peor_n, peor_t, peor_partes = n, f / FPS, dict(medir.partes)
            peor_h = max(peor_h, h)
        res[nombre] = {"cuadros": len(cuadros), "duracion_s": round((f1 - f0) / FPS, 3),
                       "vertices_dentro_max": peor_n, "fraccion_max": round(peor_n / total, 4),
                       "vertices_dentro_medio": round(suma / len(cuadros), 1),
                       "hondura_max_m": round(peor_h, 4), "peor_instante_s": round(peor_t, 3),
                       "partes_en_el_peor_instante": peor_partes}
    with open(a.salida, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print("BOLSO_OK " + json.dumps(res))


main()
