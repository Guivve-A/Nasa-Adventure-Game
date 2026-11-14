"""Color medio por zona: ancla contra captura (RGB, hex y Delta E 76), para afinar la paleta de la escena.

Uso:  python herramientas/color_zonas.py <ancla.png> <captura.png>
Las zonas estan en coordenadas normalizadas (u0, v0, u1, v1) del ancla aprobada de la vista de juego.
"""
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from comparar_ancla import a_lab  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ZONAS = {
    "hierba_sol": (0.66, 0.58, 0.72, 0.66),
    "hierba_sombra_motas": (0.30, 0.30, 0.45, 0.38),
    "sendero_sol": (0.42, 0.85, 0.48, 0.95),
    "sendero_sombra": (0.555, 0.25, 0.60, 0.30),
    "agua": (0.90, 0.12, 0.96, 0.16),
    "tronco": (0.15, 0.25, 0.22, 0.35),
    "copa_hojas": (0.25, 0.00, 0.35, 0.06),
    "baranda_mosaico": (0.02, 0.84, 0.18, 0.98),
}


def medir(ruta):
    im = np.asarray(Image.open(ruta).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(float)
    res = {}
    for k, (u0, v0, u1, v1) in ZONAS.items():
        trozo = im[int(v0 * 720):int(v1 * 720), int(u0 * 1280):int(u1 * 1280)].reshape(-1, 3)
        res[k] = trozo.mean(0)
    return res


a, c = medir(sys.argv[1]), medir(sys.argv[2])
for k in ZONAS:
    de = float(np.linalg.norm(a_lab(a[k][None]) - a_lab(c[k][None])))
    ha = "#%02x%02x%02x" % tuple(int(round(x)) for x in a[k])
    hc = "#%02x%02x%02x" % tuple(int(round(x)) for x in c[k])
    print(f"{k:22} ancla {ha}  escena {hc}  dE {de:5.1f}")
