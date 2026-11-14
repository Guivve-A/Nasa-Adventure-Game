"""Render de revision de un GLB: vistas ortograficas sin luz (la textura tal cual) desde cuatro lados.

Sirve para comparar una malla con su hoja de referencia sin que la luz del juego tape los rasgos.
Por cada lado guarda el cuerpo entero y un primer plano de la cabeza.

Uso:
  blender -b --factory-startup --python-exit-code 1 --python herramientas/blender/render_vistas.py -- \
      --glb <malla.glb> --salida <carpeta> [--cabeza 0.42] [--lado 800]

Salida: <carpeta>/<lado>_cuerpo.png y <carpeta>/<lado>_cabeza.png para los lados
mx, px (camara en -X y +X), my, py (camara en -Y y +Y de Blender; +Y de Blender = -Z de glTF),
y una linea VISTAS_OK con la caja de la malla.
"""
import argparse
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def argumentos():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--glb", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--cabeza", type=float, default=0.42, help="fraccion superior del alto que entra en el primer plano")
    p.add_argument("--lado", type=int, default=800)
    return p.parse_args(argv)


def caja(mallas):
    puntos = [o.matrix_world @ Vector(v) for o in mallas for v in o.bound_box]
    bajo = Vector((min(p.x for p in puntos), min(p.y for p in puntos), min(p.z for p in puntos)))
    alto = Vector((max(p.x for p in puntos), max(p.y for p in puntos), max(p.z for p in puntos)))
    return bajo, alto


def main():
    a = argumentos()
    # ruta absoluta: Blender toma las rutas relativas de render.filepath respecto del .blend (que no existe)
    salida = Path(a.salida).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=a.glb)
    mallas = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not mallas:
        raise SystemExit("El GLB no trae mallas")
    bajo, alto = caja(mallas)
    centro = (bajo + alto) / 2
    tam = alto - bajo

    escena = bpy.context.scene
    if escena.world is None:
        escena.world = bpy.data.worlds.new("Fondo")
    escena.world.color = (0.80, 0.78, 0.76)
    escena.render.engine = "BLENDER_WORKBENCH"
    sombreado = escena.display.shading
    sombreado.light = "FLAT"
    sombreado.color_type = "TEXTURE"
    escena.view_settings.view_transform = "Standard"
    escena.render.film_transparent = False
    escena.render.image_settings.file_format = "PNG"
    escena.render.resolution_percentage = 100

    datos = bpy.data.cameras.new("Revision")
    datos.type = "ORTHO"
    camara = bpy.data.objects.new("Revision", datos)
    escena.collection.objects.link(camara)
    escena.camera = camara

    lados = {"mx": Vector((-1, 0, 0)), "px": Vector((1, 0, 0)), "my": Vector((0, -1, 0)), "py": Vector((0, 1, 0))}
    distancia = 4 * max(tam)
    for nombre, d in lados.items():
        ancho = abs(d.x) * tam.y + abs(d.y) * tam.x  # ancho visible desde ese lado
        for toma in ("cuerpo", "cabeza"):
            if toma == "cuerpo":
                objetivo = centro.copy()
                alto_vis = tam.z
                escena.render.resolution_x = int(a.lado * 0.75)
                escena.render.resolution_y = a.lado
                datos.ortho_scale = 1.08 * max(alto_vis, ancho * 4 / 3)
            else:
                alto_vis = tam.z * a.cabeza
                objetivo = Vector((centro.x, centro.y, alto.z - alto_vis / 2))
                escena.render.resolution_x = a.lado
                escena.render.resolution_y = a.lado
                datos.ortho_scale = 1.04 * max(alto_vis, ancho)
            camara.location = objetivo + d * distancia
            camara.rotation_euler = (objetivo - camara.location).to_track_quat("-Z", "Y").to_euler()
            datos.clip_end = distancia * 3
            ruta = salida / f"{nombre}_{toma}.png"
            escena.render.filepath = str(ruta)
            bpy.ops.render.render(write_still=True)
    print("VISTAS_OK caja=%s tam=%s" % (tuple(round(v, 3) for v in bajo), tuple(round(v, 3) for v in tam)))


main()
