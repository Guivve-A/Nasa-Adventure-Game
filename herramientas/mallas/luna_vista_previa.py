"""Vista previa rapida de los GLB de la Luna, sin Godot ni Blender (numpy + PIL, pintor por triangulos).

Pinta cada GLB de herramientas/mallas (los que escribe nucleo.Escena: POSITION, NORMAL, COLOR_0 y material
por nombre) en dos vistas: la de la camara de juego (48 grados hacia abajo, con la inclinacion 2.5D) y una
de tres cuartos mas baja. Luz parecida a la de la zona: principal lavanda desde la izquierda y relleno azul.
Solo sirve para revisar forma y color antes de llevarlo al motor; no es la imagen del juego.

Uso:
    python -I herramientas/mallas/luna_vista_previa.py <salida.png> <a.glb> [<b.glb> ...]
"""
from __future__ import annotations

import json
import math
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

TIPOS = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}
COMPS = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}


def leer_glb(ruta):
    datos = Path(ruta).read_bytes()
    largo_js = struct.unpack_from("<I", datos, 12)[0]
    doc = json.loads(datos[20:20 + largo_js])
    binario = datos[20 + largo_js + 8:]

    def acc(i):
        a = doc["accessors"][i]
        v = doc["bufferViews"][a["bufferView"]]
        n = a["count"] * COMPS[a["type"]]
        arr = np.frombuffer(binario, TIPOS[a["componentType"]], n, v.get("byteOffset", 0) + a.get("byteOffset", 0))
        return arr.reshape(a["count"], COMPS[a["type"]]) if COMPS[a["type"]] > 1 else arr

    tris = []

    def recorrer(i, M):
        nodo = doc["nodes"][i]
        t = np.array(nodo.get("translation", [0, 0, 0]))
        q = nodo.get("rotation", [0, 0, 0, 1])
        s = np.array(nodo.get("scale", [1, 1, 1]))
        x, y, z, w = q
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        L = np.eye(4)
        L[:3, :3] = R * s
        L[:3, 3] = t
        G = M @ L
        if "mesh" in nodo:
            for p in doc["meshes"][nodo["mesh"]]["primitives"]:
                P = acc(p["attributes"]["POSITION"])
                C = acc(p["attributes"]["COLOR_0"])[:, :3]
                idx = acc(p["indices"])
                mat = doc["materials"][p["material"]]["name"]
                Pw = P @ G[:3, :3].T + G[:3, 3]
                C = np.where(C <= 0.0031308, C * 12.92, 1.055 * np.power(np.clip(C, 0, 1), 1 / 2.4) - 0.055)
                for k in range(0, len(idx), 3):
                    a, b, c = idx[k:k + 3]
                    tris.append((Pw[[a, b, c]], C[[a, b, c]].mean(0), mat))
        for h in nodo.get("children", []):
            recorrer(h, G)

    for i in doc["scenes"][0]["nodes"]:
        recorrer(i, np.eye(4))
    return tris


def pintar(tris, ancho, alto, pitch_deg, yaw_deg, cizalla=0.45, fondo=(46, 50, 78)):
    img = Image.new("RGB", (ancho, alto), fondo)
    d = ImageDraw.Draw(img)
    luz = np.array([-0.70, 0.58, 0.40])
    luz /= np.linalg.norm(luz)
    amb = np.array([0.36, 0.40, 0.62])
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    Ry = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0], [-math.sin(yaw), 0, math.cos(yaw)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(pitch), -math.sin(pitch)], [0, math.sin(pitch), math.cos(pitch)]])
    V = Rx @ Ry
    todos = np.concatenate([t[0] for t in tris])
    todos = todos.copy()
    todos[:, 2] -= cizalla * todos[:, 1]
    pv = todos @ V.T
    lo, hi = pv[:, :2].min(0), pv[:, :2].max(0)
    esc = 0.86 * min(ancho / max(hi[0] - lo[0], 1e-6), alto / max(hi[1] - lo[1], 1e-6))
    centro = (lo + hi) / 2
    lista = []
    for P, col, mat in tris:
        Q = P.copy()
        Q[:, 2] -= cizalla * Q[:, 1]
        n = np.cross(P[1] - P[0], P[2] - P[0])
        if np.linalg.norm(n) < 1e-12:
            continue
        n /= np.linalg.norm(n)
        q = Q @ V.T
        nv = np.cross(q[1] - q[0], q[2] - q[0])
        if nv[2] <= 0 and mat not in ("Follaje",):
            continue
        if mat in ("Emisivo",):
            c = np.array([0.38, 0.89, 0.88]) * 1.15
        elif mat in ("Pintura",):
            c = col
        else:
            ndl = max(float(n @ luz), 0.0)
            k = 0.55 + 0.45 * min(ndl / 0.12, 1.0)
            c = col * (np.array([0.93, 0.90, 0.98]) * k + amb * 0.45)
        xy = [(ancho / 2 + (p[0] - centro[0]) * esc, alto / 2 - (p[1] - centro[1]) * esc) for p in q]
        lista.append((q[:, 2].mean(), xy, tuple(int(v) for v in np.clip(c, 0, 1) * 255)))
    lista.sort(key=lambda e: e[0])
    for _, xy, c in lista:
        d.polygon(xy, fill=c)
    return img


def main():
    salida = Path(sys.argv[1])
    paneles = []
    for ruta in sys.argv[2:]:
        tris = leer_glb(ruta)
        a = pintar(tris, 420, 360, 48, 0)
        b = pintar(tris, 420, 360, 20, -35)
        fila = Image.new("RGB", (840, 380), (30, 32, 50))
        fila.paste(a, (0, 20))
        fila.paste(b, (420, 20))
        ImageDraw.Draw(fila).text((6, 4), Path(ruta).stem, fill=(230, 230, 230))
        paneles.append(fila)
    lam = Image.new("RGB", (840, 380 * len(paneles)))
    for i, p in enumerate(paneles):
        lam.paste(p, (0, 380 * i))
    lam.save(salida)
    print("vista previa:", salida)


if __name__ == "__main__":
    main()
