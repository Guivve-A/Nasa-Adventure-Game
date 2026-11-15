"""Vista previa sin Godot de la habitacion con la camara de juego (solo color de vertice, sin luz).

Sirve para buscar huecos, cantos sin tapa y fondo vacio sin ocupar la GPU compartida: reproduce la camara de
juego/nucleo/camara_juego.gd (48 grados, campo de 40, inclinacion 2.5D z -= 0,45 y), el giro del cuarto de
juego/zonas/habitacion/habitacion.gd y el descarte de caras traseras de los materiales opacos.
Los pixeles que quedan con el color de fondo se pintan de magenta y se cuentan: ese es el «vacio».

Uso:  python -I herramientas/mallas/habitacion_vista_previa.py <salida.png> [encuadre] [foco_x,foco_z] [--noche] [--ancho=960]
"""
from __future__ import annotations

import json
import math
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
HAB = RAIZ / "juego" / "modelos" / "habitacion"
ENT = RAIZ / "juego" / "modelos" / "entorno"
GIRO = math.radians(20.0)
CIZ = 0.45
W, H = 640, 360
LIMITES = (-0.6, -1.3, 1.0, -0.2)       # x0, z0, x1, z1 (habitacion.gd)


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def leer_glb(ruta):
    datos = Path(ruta).read_bytes()
    largo_js = struct.unpack_from("<I", datos, 12)[0]
    doc = json.loads(datos[20:20 + largo_js])
    binario = datos[20 + largo_js + 8:]

    def acc(i):
        a = doc["accessors"][i]
        bv = doc["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]
        tipo = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}[a["componentType"]]
        off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(binario, tipo, a["count"] * n, off).reshape(a["count"], n)
        if tipo == np.uint8:
            arr = arr / 255.0
        elif tipo == np.uint16 and n > 1:
            arr = arr / 65535.0
        return arr.astype(float)
    salida = []

    def nodo(i, M):
        nd = doc["nodes"][i]
        t = np.array(nd.get("translation", [0, 0, 0]), float)
        q = nd.get("rotation", [0, 0, 0, 1])
        s = np.array(nd.get("scale", [1, 1, 1]), float)
        x, y, z, w = q
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        L = np.eye(4)
        L[:3, :3] = R * s
        L[:3, 3] = t
        M2 = M @ L
        if "mesh" in nd:
            for pr in doc["meshes"][nd["mesh"]]["primitives"]:
                P = acc(pr["attributes"]["POSITION"])
                C = acc(pr["attributes"]["COLOR_0"])[:, :3] if "COLOR_0" in pr["attributes"] else np.full((len(P), 3), 0.5)
                idx = acc(pr["indices"]).astype(int).ravel() if "indices" in pr else np.arange(len(P))
                mat = doc["materials"][pr["material"]] if "material" in pr else {}
                P = P @ M2[:3, :3].T + M2[:3, 3]
                salida.append((P[idx].reshape(-1, 3, 3), C[idx].reshape(-1, 3, 3), bool(mat.get("doubleSided", False))))
        for h in nd.get("children", []):
            nodo(h, M2)
    for r in doc["scenes"][doc.get("scene", 0)]["nodes"]:
        nodo(r, np.eye(4))
    return salida


def colocar(ruta, pos=(0, 0, 0), giro=0.0, escala=1.0):
    """GLB en coordenadas del cuarto -> mundo."""
    R = rot_y(GIRO) @ rot_y(math.radians(giro))
    res = []
    for P, C, doble in leer_glb(ruta):
        Pm = (P * escala) @ R.T + rot_y(GIRO) @ np.asarray(pos, float)
        res.append((Pm, C, doble))
    return res


def escena(noche=False):
    FUERA = -0.6
    AX, AZ = 3.3, 2.7
    obj = []
    obj += colocar(HAB / ("HAB-12n.glb" if noche else "HAB-12.glb"))
    obj += colocar(HAB / "HAB-13.glb")
    obj += colocar(HAB / "HAB-02.glb", (0.1, 0, -AZ))
    obj += colocar(HAB / "HAB-07.glb", (AX, 0, 0.9), -90)
    obj += colocar(HAB / "HAB-09.glb", (AX, 0, 1.85))
    obj += colocar(HAB / "TAL-01.glb", (2.9, 0, -0.45), -90)
    obj += colocar(HAB / "HAB-01.glb", (-2.2, 0, -2.1))
    obj += colocar(HAB / "HAB-16.glb", (2.75, 0, -2.2))
    for nombre in ("HAB-18.glb", "HAB-19.glb") if noche else ("HAB-18.glb",):
        if (HAB / nombre).exists():
            obj += colocar(HAB / nombre)
    fuera = [("VEG-10.glb", (-4.3, FUERA, 2.6), 20.0, 2.6), ("VEG-12.glb", (-4.6, FUERA, 0.6), 80.0, 2.0),
             ("VEG-07.glb", (-4.4, FUERA, -1.4), 140.0, 2.2), ("VEG-10.glb", (-2.6, FUERA, 3.9), 200.0, 2.2),
             ("VEG-12.glb", (-0.6, FUERA, 4.1), 10.0, 2.0), ("VEG-07.glb", (1.3, FUERA, 4.0), 250.0, 1.9),
             ("VEG-10.glb", (3.0, FUERA, 4.1), 90.0, 2.3)]
    # la vegetacion de fuera que pone habitacion.gd en _plantas() (lista FUERA_V2)
    gd = (RAIZ / "juego" / "zonas" / "habitacion" / "habitacion.gd").read_text(encoding="utf-8")
    import re
    for ruta, x, y, z, giro, esc in re.findall(r'\[(?:ENT|HAB) \+ "([A-Z0-9-]+\.glb)", Vector3\(([-\d.]+), ([-\w.]+), ([-\d.]+)\), ([-\d.]+), ([-\d.]+)\]', gd):
        yv = {"FUERA": FUERA, "CALLE": -2.52}.get(y)
        fuera.append((ruta, (float(x), float(yv if yv is not None else y), float(z)), float(giro), float(esc)))
    fuera = list(dict.fromkeys(fuera))
    for nombre, pos, giro, esc in fuera:
        base = ENT if nombre.startswith("VEG") else HAB
        if (base / nombre).exists():
            obj += colocar(base / nombre, pos, giro, esc)
    return obj


def camara(encuadre, foco_xz):
    inc = math.radians(48.0)
    fov = math.radians(40.0)
    factor = math.cos(inc) + CIZ * math.sin(inc)
    dist = 1.05 * factor / (2.0 * encuadre * math.tan(fov / 2))
    medio = 0.525
    fx = min(max(foco_xz[0], LIMITES[0]), LIMITES[2])
    fz = min(max(foco_xz[1], LIMITES[1]), LIMITES[3])
    foco = np.array([fx, medio, fz - CIZ * medio])
    d = np.array([0.0, math.sin(inc), math.cos(inc)])
    ojo = foco + d * dist
    adelante = -d
    der = np.cross(adelante, [0, 1, 0])
    der /= np.linalg.norm(der)
    arriba = np.cross(der, adelante)
    return ojo, adelante, der, arriba, math.tan(fov / 2)


def render(obj, encuadre, foco_xz, fondo=(0x24, 0x1F, 0x1C)):
    ojo, ad, der, arr, th = camara(encuadre, foco_xz)
    tw = th * W / H
    zbuf = np.full((H, W), np.inf)
    img = np.zeros((H, W, 3))
    img[:] = np.array(fondo) / 255.0
    lleno = np.zeros((H, W), bool)
    for P, C, doble in obj:
        P = P.copy()
        P[..., 2] -= CIZ * P[..., 1]
        rel = P - ojo
        zc = rel @ ad
        xc = rel @ der
        yc = rel @ arr
        valido = (zc > 0.05).all(1)
        sx = (xc / np.maximum(zc, 1e-6) / tw * 0.5 + 0.5) * W
        sy = (0.5 - yc / np.maximum(zc, 1e-6) / th * 0.5) * H
        area = (sx[:, 1] - sx[:, 0]) * (sy[:, 2] - sy[:, 0]) - (sx[:, 2] - sx[:, 0]) * (sy[:, 1] - sy[:, 0])
        if not doble:
            valido &= area < 0          # antihorario en pantalla (y hacia abajo) = cara delantera
        Cs = np.where(C <= 0.0031308, C * 12.92, 1.055 * np.power(np.clip(C, 0, 1), 1 / 2.4) - 0.055)
        for t in np.nonzero(valido & (np.abs(area) > 1e-9))[0]:
            x0, x1 = int(max(0, math.floor(sx[t].min()))), int(min(W - 1, math.ceil(sx[t].max())))
            y0, y1 = int(max(0, math.floor(sy[t].min()))), int(min(H - 1, math.ceil(sy[t].max())))
            if x0 > x1 or y0 > y1:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            a = area[t]
            w0 = ((sx[t, 1] - gx) * (sy[t, 2] - gy) - (sx[t, 2] - gx) * (sy[t, 1] - gy)) / a
            w1 = ((sx[t, 2] - gx) * (sy[t, 0] - gy) - (sx[t, 0] - gx) * (sy[t, 2] - gy)) / a
            w2 = 1 - w0 - w1
            m = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            if not m.any():
                continue
            z = w0 * zc[t, 0] + w1 * zc[t, 1] + w2 * zc[t, 2]
            zb = zbuf[y0:y1 + 1, x0:x1 + 1]
            m &= z < zb
            if not m.any():
                continue
            zb[m] = z[m]
            col = w0[..., None] * Cs[t, 0] + w1[..., None] * Cs[t, 1] + w2[..., None] * Cs[t, 2]
            img[y0:y1 + 1, x0:x1 + 1][m] = col[m]
            lleno[y0:y1 + 1, x0:x1 + 1][m] = True
    vacio = ~lleno
    img[vacio] = (1.0, 0.0, 1.0)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8), float(vacio.mean())


def main():
    salida = sys.argv[1]
    encuadre = float(sys.argv[2]) if len(sys.argv) > 2 else 0.20
    foco = tuple(float(v) for v in sys.argv[3].split(",")) if len(sys.argv) > 3 else (0.1, 0.3)
    noche = "--noche" in sys.argv
    global W, H
    for a in sys.argv:
        if a.startswith("--ancho="):
            W = int(a.split("=")[1])
            H = W * 9 // 16
    img, vacio = render(escena(noche), encuadre, foco)
    Image.fromarray(img).save(salida)
    print(f"{salida}: vacio {vacio * 100:.2f} % del cuadro")


if __name__ == "__main__":
    main()
