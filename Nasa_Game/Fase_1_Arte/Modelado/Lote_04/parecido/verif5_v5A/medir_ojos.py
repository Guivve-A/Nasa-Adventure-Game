import sys
import numpy as np
from PIL import Image
for nombre, caja in [("px_cabeza.png", (300, 330, 740, 670)), ("py_cabeza.png", (60, 330, 480, 650)), ("my_cabeza.png", (540, 330, 960, 650))]:
    a = np.asarray(Image.open(nombre).convert("RGB")).astype(int)
    x0, y0, x1, y1 = caja
    r = a[y0:y1, x0:x1]
    R, G, B = r[..., 0], r[..., 1], r[..., 2]
    azul = (B > R + 5) & (B > 120)
    print(nombre, "pixeles gris-azulados (B>R) en la cara:", int(azul.sum()))
    if nombre == "px_cabeza.png":
        # blanco del ojo: claro y poco saturado
        blanco = (R > 190) & (G > 170) & (B > 150) & (R - B < 60)
        cols = np.where(blanco.any(0))[0] + x0
        mitad = 520
        izq = blanco[:, : mitad - x0]
        der = blanco[:, mitad - x0:]
        print("  esclerotica clara: ojo izquierdo de la imagen", int(izq.sum()), "px; ojo derecho", int(der.sum()), "px")
        for parte, m, off in [("izq", izq, x0), ("der", der, mitad)]:
            c = np.where(m.any(0))[0]
            if len(c):
                print(f"  ancho del blanco {parte}: x {c.min()+off}..{c.max()+off} ({c.max()-c.min()} px)")
