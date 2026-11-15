"""Primeros planos del bolso en los peores instantes que da verificar_bolso.py (render sin luz, textura tal cual).

Uso:
  blender -b --factory-startup --python-exit-code 1 --python render_bolso_cerca.py -- --glb <PER-01_rig.glb> \
      --salida <carpeta> --tomas correr:0.08,recoger:0.44,salto_lunar:0.76,caminar:0.24
Por cada toma guarda tres vistas: frente (camara en +X), derecha del personaje (camara en -Y de Blender) y
tres cuartos desde arriba (parecida a la camara del juego).
"""
import argparse
import sys
from pathlib import Path

import bpy
from mathutils import Vector

FPS = 50


def argumentos():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--glb", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--tomas", default="correr:0.08,recoger:0.44")
    p.add_argument("--lado", type=int, default=520)
    p.add_argument("--ancho-m", type=float, default=0.62)
    return p.parse_args(argv)


def main():
    a = argumentos()
    salida = Path(a.salida).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    escena = bpy.context.scene
    escena.render.fps, escena.render.fps_base = FPS, 1.0
    bpy.ops.import_scene.gltf(filepath=a.glb)
    # el importador crea una icosfera como forma de los huesos: es una malla y saldria en el render
    for o in [o for o in bpy.data.objects if o.type == "MESH" and not o.data.materials]:
        bpy.data.objects.remove(o, do_unlink=True)
    armadura = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    armadura.hide_render = True
    ad = armadura.animation_data
    for pista in ad.nla_tracks:
        pista.mute = True

    if escena.world is None:
        escena.world = bpy.data.worlds.new("Fondo")
    escena.world.color = (0.80, 0.78, 0.76)
    escena.render.engine = "BLENDER_WORKBENCH"
    escena.display.shading.light = "FLAT"
    escena.display.shading.color_type = "TEXTURE"
    escena.view_settings.view_transform = "Standard"
    escena.render.image_settings.file_format = "PNG"
    escena.render.resolution_x = escena.render.resolution_y = a.lado
    escena.render.resolution_percentage = 100
    datos = bpy.data.cameras.new("Cerca")
    datos.type = "ORTHO"
    datos.ortho_scale = a.ancho_m
    datos.clip_end = 20.0
    camara = bpy.data.objects.new("Cerca", datos)
    escena.collection.objects.link(camara)
    escena.camera = camara
    vistas = {"frente": Vector((1.0, 0.0, 0.0)), "derecha": Vector((0.0, -1.0, 0.0)),
              "tres_cuartos": Vector((0.75, -0.55, 0.65)).normalized()}

    for toma in a.tomas.split(","):
        clip, t = toma.split(":")
        accion = next(x for x in bpy.data.actions if x.name.split(".")[0] == clip)
        ad.action = accion
        if hasattr(ad, "action_slot") and accion.slots:
            ad.action_slot = accion.slots[0]
        escena.frame_set(int(round(float(t) * FPS)))
        bpy.context.view_layer.update()
        hueso = armadura.pose.bones["bolso"]
        objetivo = armadura.matrix_world @ ((hueso.head + hueso.tail) / 2.0)
        for nombre, d in vistas.items():
            camara.location = objetivo + d * 4.0
            camara.rotation_euler = (objetivo - camara.location).to_track_quat("-Z", "Y").to_euler()
            escena.render.filepath = str(salida / ("bolso_%s_%s_%s.png" % (clip, t.replace(".", "p"), nombre)))
            bpy.ops.render.render(write_still=True)
    print("CERCA_OK")


main()
