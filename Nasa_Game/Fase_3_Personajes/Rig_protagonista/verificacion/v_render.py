"""Renders propios del verificador: sin luz (Workbench plano con textura), ortograficos.

Uso: blender -b --factory-startup --python-exit-code 1 --python v_render.py -- --glb <glb> --salida <carpeta>
        [--plan <json>] [--reposo] [--lado 480]
plan: {"clip": [t0, t1, ...]}. Por cada instante guarda frente (camara en +X), derecha (lado del bolso,
camara en -Y de Blender) e izquierda (camara en +Y). Con --reposo guarda la pose de union.
Escribe ademas <salida>/medidas.json con la caja evaluada de cada instante (para cruzarla con v_glb.py).
"""
import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--glb", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--plan")
    p.add_argument("--reposo", action="store_true")
    p.add_argument("--lado", type=int, default=480)
    p.add_argument("--vistas", default="frente,derecha,izquierda")
    p.add_argument("--ortho", type=float, default=1.30)
    p.add_argument("--obj", default="0.03,0,0.05")
    p.add_argument("--cuadrado", action="store_true")
    return p.parse_args(argv)


a = args()
salida = Path(a.salida).resolve()
salida.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(Path(a.glb).resolve()))
for o in [o for o in bpy.data.objects if o.type == "MESH" and not o.data.materials]:
    print("QUITADA", o.name)
    bpy.data.objects.remove(o, do_unlink=True)
mallas = [o for o in bpy.context.scene.objects if o.type == "MESH"]
arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
print("MALLAS", [m.name for m in mallas], "ARMADURA", arm.name if arm else None)
print("ACCIONES", sorted(x.name for x in bpy.data.actions))

esc = bpy.context.scene
if esc.world is None:
    esc.world = bpy.data.worlds.new("Fondo")
esc.world.color = (0.80, 0.78, 0.76)
esc.render.engine = "BLENDER_WORKBENCH"
sh = esc.display.shading
sh.light = "FLAT"
sh.color_type = "TEXTURE"
esc.view_settings.view_transform = "Standard"
esc.render.film_transparent = False
esc.render.image_settings.file_format = "PNG"
esc.render.resolution_percentage = 100
esc.render.resolution_x = int(a.lado * 0.75)
esc.render.resolution_y = a.lado

# losa de suelo: cara superior en z = -0.5 (referencia visual de pies hundidos o flotando)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.56))
losa = bpy.context.active_object
losa.scale = (3, 3, 0.12)
losa.name = "v_suelo"

cam_d = bpy.data.cameras.new("v_cam")
cam_d.type = "ORTHO"
cam_d.ortho_scale = a.ortho
if a.cuadrado:
    esc.render.resolution_x = a.lado
cam = bpy.data.objects.new("v_cam", cam_d)
esc.collection.objects.link(cam)
esc.camera = cam
OBJ = Vector(tuple(float(x) for x in a.obj.split(",")))
DIR = {"frente": Vector((1, 0, 0)), "derecha": Vector((0, -1, 0)), "izquierda": Vector((0, 1, 0)),
       "espalda": Vector((-1, 0, 0)), "tres4": Vector((0.7, -0.7, 0.45)).normalized(),
       "tres4izq": Vector((0.7, 0.7, 0.45)).normalized(), "juego": Vector((0.45, -0.35, 0.82)).normalized(),
       "atras4": Vector((-0.7, -0.7, 0.3)).normalized()}


def render(nombre, vistas):
    for v in vistas:
        d = DIR[v]
        cam.location = OBJ + d * 5
        cam.rotation_euler = (OBJ - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam_d.clip_end = 20
        esc.render.filepath = str(salida / f"{nombre}_{v}.png")
        bpy.ops.render.render(write_still=True)


def caja_evaluada():
    dg = bpy.context.evaluated_depsgraph_get()
    lo = [1e9] * 3
    hi = [-1e9] * 3
    for m in mallas:
        ev = m.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        for v in me.vertices:
            p = mw @ v.co
            for k in range(3):
                lo[k] = min(lo[k], p[k])
                hi[k] = max(hi[k], p[k])
        ev.to_mesh_clear()
    return [round(x, 5) for x in lo], [round(x, 5) for x in hi]


vistas = a.vistas.split(",")
medidas = {}
if a.reposo:
    if arm:
        arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    medidas["reposo_union"] = caja_evaluada()
    render("union", vistas)
    if arm:
        arm.data.pose_position = "POSE"

if a.plan:
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    fps = esc.render.fps / esc.render.fps_base
    ad = arm.animation_data
    if ad is None:
        ad = arm.animation_data_create()
    for tr in ad.nla_tracks:
        tr.mute = True
    for clip, tiempos in plan.items():
        act = bpy.data.actions.get(clip)
        if act is None:
            raise SystemExit("FALTA_CLIP " + clip)
        ad.action = act
        if hasattr(ad, "action_slot") and len(getattr(act, "slots", [])):
            ad.action_slot = act.slots[0]
        print("CLIP", clip, "rango", tuple(act.frame_range), "fps", fps)
        for t in tiempos:
            f = t * fps
            esc.frame_set(int(f), subframe=f - int(f))
            bpy.context.view_layer.update()
            nombre = "%s_%03d" % (clip, round(t * 100))
            medidas[nombre] = caja_evaluada()
            render(nombre, vistas)
(salida / "medidas.json").write_text(json.dumps(medidas, indent=1), encoding="utf-8")
print("RENDERS_OK", len(medidas))
