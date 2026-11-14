# render ortografico sin luz de cerca (mismos ajustes que render_vistas.py), centrado en un punto
import bpy, sys, math
from mathutils import Vector
args = sys.argv[sys.argv.index("--") + 1:]
glb, salida, cx, cy, cz, escala, lado = args[0], args[1], *map(float, args[2:6]), int(args[6])
vistas = args[7].split(",") if len(args) > 7 else ["px", "my"]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
e = bpy.context.scene
e.world = bpy.data.worlds.new("F"); e.world.color = (0.80, 0.78, 0.76)
e.render.engine = "BLENDER_WORKBENCH"
e.display.shading.light = "FLAT"; e.display.shading.color_type = "TEXTURE"
e.view_settings.view_transform = "Standard"
e.render.resolution_x = e.render.resolution_y = lado
cam = bpy.data.cameras.new("C"); cam.type = "ORTHO"; cam.ortho_scale = escala
ob = bpy.data.objects.new("C", cam); e.collection.objects.link(ob); e.camera = ob
dirs = {"px": (1, 0, 0), "my": (0, -1, 0), "mx": (-1, 0, 0), "py": (0, 1, 0),
        "d45": (math.cos(math.radians(45)), -math.sin(math.radians(45)), 0.35)}
c = Vector((cx, cy, cz))
for n in vistas:
    d = Vector(dirs[n]).normalized()
    ob.location = c + d * 3
    ob.rotation_euler = (c - ob.location).to_track_quat("-Z", "Y").to_euler()
    cam.clip_end = 10
    e.render.filepath = "%s/%s.png" % (salida, n)
    bpy.ops.render.render(write_still=True)
print("CERCA_OK")
