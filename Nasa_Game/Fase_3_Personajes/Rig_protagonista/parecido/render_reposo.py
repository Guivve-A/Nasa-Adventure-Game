"""Vistas de reposo de un GLB CON esqueleto, con el mismo encuadre que herramientas/blender/render_vistas.py.

Hace falta porque el importador de glTF de Blender crea una icosfera de 2 m como forma de los huesos: es una
malla, render_vistas.py la mete en la caja y el personaje sale a un 40 % de su tamano (el parecido cambia).
Este envoltorio ejecuta render_vistas.py sin modificarlo, quitando antes las mallas sin material.

Uso (desde la raiz del repositorio):
  blender -b --factory-startup --python-exit-code 1 --python \
      Nasa_Game/Fase_3_Personajes/Rig_protagonista/parecido/render_reposo.py -- \
      --glb juego/modelos/personajes/PER-01_rig.glb --salida <carpeta> --lado 1000
"""
from pathlib import Path

import bpy  # noqa: F401  (lo usa el codigo de render_vistas.py)

RAIZ = Path(__file__).resolve().parents[4]
fuente = (RAIZ / "herramientas/blender/render_vistas.py").read_text(encoding="utf-8")
viejo = '    mallas = [o for o in bpy.context.scene.objects if o.type == "MESH"]\n'
nuevo = ('    for o in [o for o in bpy.data.objects if o.type == "MESH" and not o.data.materials]:\n'
         '        print("QUITADA", o.name)\n'
         '        bpy.data.objects.remove(o, do_unlink=True)\n' + viejo)
if viejo not in fuente:
    raise SystemExit("render_vistas.py cambio: revisa este envoltorio")
exec(compile(fuente.replace(viejo, nuevo), "render_vistas_sin_icosfera", "exec"))
