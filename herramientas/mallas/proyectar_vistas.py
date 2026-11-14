"""Pinta la textura de una malla proyectando las vistas de su hoja de referencia (sin creditos).

Sirve cuando el imagen->3D entrega buena geometria pero mala textura (por ejemplo, gris plano).
Cada texel del mapa UV se ubica en 3D y toma el color de la vista hacia la que mira su cara:
frente, espalda, lado derecho (perfil) o lado izquierdo (perfil espejado), mezclados por el angulo.
Las vistas son las mismas que se mandaron a Tripo (fondo liso, figura centrada).

Orientacion: con --auto se prueban las 4 direcciones de frente (+X, -X, +Z, -Z), con y sin espejo de
la geometria, y se elige la que deja menos puntos sobre el fondo de las vistas. Lote 04: la protagonista
salio mirando a -X y en espejo (Tripo leyo su perfil derecho como vista izquierda); el gato, a +X.
El espejo (z -> -z, con el orden de los triangulos invertido) devuelve la quiralidad del diseno.

Uso:  python herramientas/mallas/proyectar_vistas.py <entrada.glb> <salida.glb>
          --frente-img F.png --espalda-img B.png --perfil-img P.png [--perfil-mira derecha|izquierda]
          [--lado 2048] [--auto | --frente -x --espejar]
"""
import argparse
import io
import json
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
TIPOS = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
COMPONENTES = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def leer_glb(ruta):
    data = Path(ruta).read_bytes()
    largo = struct.unpack("<I", data[12:16])[0]
    doc = json.loads(data[20:20 + largo])
    binario = data[20 + largo + 8:]

    def accessor(i):
        a = doc["accessors"][i]
        bv = doc["bufferViews"][a["bufferView"]]
        n, k = a["count"], COMPONENTES[a["type"]]
        dt = np.dtype(TIPOS[a["componentType"]])
        off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        paso = bv.get("byteStride", 0) or dt.itemsize * k
        filas = np.ndarray((n, k), dt, binario, off, (paso, dt.itemsize))
        return np.array(filas, dtype=np.float64 if dt == np.float32 else np.int64)

    prim = doc["meshes"][0]["primitives"][0]
    P = accessor(prim["attributes"]["POSITION"])
    UV = accessor(prim["attributes"]["TEXCOORD_0"])
    idx = accessor(prim["indices"]).reshape(-1, 3) if "indices" in prim else np.arange(len(P)).reshape(-1, 3)
    return P, UV, idx


def mascara_figura(img):
    a = np.asarray(img.convert("RGB")).astype(float)
    borde = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    fondo = np.median(borde, axis=0)
    return np.linalg.norm(a - fondo, axis=-1) > 30


class Vista:
    """Proyeccion ortografica: (u_mundo, y) -> pixel, ajustada al recuadro de la figura."""

    def __init__(self, ruta, eje_u, P):
        self.img = np.asarray(Image.open(ruta).convert("RGB")).astype(float)
        m = mascara_figura(Image.open(ruta))
        filas, cols = np.where(m.any(1))[0], np.where(m.any(0))[0]
        self.y0, self.y1 = filas[0], filas[-1]
        self.cx = (cols[0] + cols[-1]) / 2
        self.eje_u = np.asarray(eje_u, float)
        u = P @ self.eje_u
        self.ymin, self.ymax = P[:, 1].min(), P[:, 1].max()
        self.escala = (self.y1 - self.y0) / (self.ymax - self.ymin)
        self.ucen = (u.min() + u.max()) / 2

    def color(self, X):
        u = X @ self.eje_u
        px = self.cx + (u - self.ucen) * self.escala
        py = self.y1 - (X[:, 1] - self.ymin) * self.escala
        h, w = self.img.shape[:2]
        px = np.clip(np.round(px).astype(int), 0, w - 1)
        py = np.clip(np.round(py).astype(int), 0, h - 1)
        return self.img[py, px]


def escribir_glb(ruta, P, UV, idx, png_bytes, nombre):
    bin_ = bytearray()
    vistas, accs = [], []

    def agregar(arr, comp, tipo, target, minmax=False):
        while len(bin_) % 4:
            bin_.append(0)
        off = len(bin_)
        bin_.extend(arr.tobytes())
        vistas.append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, **({"target": target} if target else {})})
        acc = {"bufferView": len(vistas) - 1, "componentType": comp, "count": int(arr.shape[0]), "type": tipo}
        if minmax:
            acc["min"], acc["max"] = arr.min(0).tolist(), arr.max(0).tolist()
        accs.append(acc)
        return len(accs) - 1

    a_p = agregar(P.astype(np.float32), 5126, "VEC3", 34962, True)
    a_uv = agregar(UV.astype(np.float32), 5126, "VEC2", 34962)
    a_i = agregar(idx.reshape(-1).astype(np.uint32), 5125, "SCALAR", 34963)
    while len(bin_) % 4:
        bin_.append(0)
    off_img = len(bin_)
    bin_.extend(png_bytes)
    vistas.append({"buffer": 0, "byteOffset": off_img, "byteLength": len(png_bytes)})
    while len(bin_) % 4:
        bin_.append(0)
    doc = {"asset": {"version": "2.0", "generator": "herramientas/mallas/proyectar_vistas.py"},
           "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"name": nombre, "mesh": 0}],
           "meshes": [{"name": nombre, "primitives": [{"attributes": {"POSITION": a_p, "TEXCOORD_0": a_uv},
                                                        "indices": a_i, "material": 0}]}],
           "materials": [{"name": "Personaje", "pbrMetallicRoughness": {"baseColorTexture": {"index": 0},
                                                                         "metallicFactor": 0.0, "roughnessFactor": 1.0}}],
           "textures": [{"source": 0, "sampler": 0}], "samplers": [{"magFilter": 9729, "minFilter": 9987}],
           "images": [{"bufferView": len(vistas) - 1, "mimeType": "image/png"}],
           "accessors": accs, "bufferViews": vistas, "buffers": [{"byteLength": len(bin_)}]}
    js = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    js += b" " * ((4 - len(js) % 4) % 4)
    with open(ruta, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bin_)))
        f.write(struct.pack("<II", len(js), 0x4E4F534A))
        f.write(js)
        f.write(struct.pack("<II", len(bin_), 0x004E4942))
        f.write(bytes(bin_))


EJES = {"+x": [1, 0, 0], "-x": [-1, 0, 0], "+z": [0, 0, 1], "-z": [0, 0, -1]}
FONDO = np.array([230, 225, 220.0])


def armar_vistas(a, P, F, tmp):
    R = np.cross(F, [0, 1, 0])  # lado derecho del personaje
    # visto de frente, la derecha de la imagen es el lado izquierdo del personaje (-R)
    frente = Vista(a.frente_img, -R, P)
    espalda = Vista(a.espalda_img, R, P)
    perfil_img = Image.open(a.perfil_img)
    if a.perfil_mira == "izquierda":
        perfil_img = perfil_img.transpose(Image.FLIP_LEFT_RIGHT)
    perfil_img.save(tmp)
    derecha = Vista(tmp, F, P)       # lado derecho: la figura mira a la derecha de la imagen
    perfil_img.transpose(Image.FLIP_LEFT_RIGHT).save(tmp)
    izquierda = Vista(tmp, -F, P)    # lado izquierdo: perfil espejado
    tmp.unlink()
    return [(frente, F), (espalda, -F), (derecha, R), (izquierda, -R)]


def en_fondo(vistas, P, idx):
    """Porcentaje de caras que, vistas desde su direccion, caen sobre el fondo de la imagen."""
    tris = P[idx]
    cen = tris.mean(1)
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    salida = []
    for vista, direccion in vistas:
        sel = (n @ direccion) > 0.5
        c = vista.color(cen[sel])
        salida.append(float((np.linalg.norm(c - FONDO, axis=1) < 25).mean() * 100) if sel.any() else 100.0)
    return salida


def espejar(P, idx):
    P = P.copy()
    P[:, 2] *= -1
    return P, idx[:, [0, 2, 1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--frente-img", required=True)
    ap.add_argument("--espalda-img", required=True)
    ap.add_argument("--perfil-img", required=True)
    ap.add_argument("--perfil-mira", default="derecha", help="hacia donde mira la figura en la imagen del perfil")
    ap.add_argument("--frente", default="+x")
    ap.add_argument("--espejar", action="store_true", help="espeja la geometria en Z antes de pintar")
    ap.add_argument("--auto", action="store_true", help="elige frente y espejo por el ajuste de las siluetas")
    ap.add_argument("--lado", type=int, default=2048)
    a = ap.parse_args()

    P0, UV, idx0 = leer_glb(a.entrada)
    tmp = Path(a.salida).with_suffix(".perfil_tmp.png")
    candidatos = [(f, e) for f in EJES for e in (False, True)] if a.auto else [(a.frente, a.espejar)]
    mejor = None
    for f, e in candidatos:
        P, idx = espejar(P0, idx0) if e else (P0, idx0)
        F = np.array(EJES[f], float)
        fondo = en_fondo(armar_vistas(a, P, F, tmp), P, idx)
        print(f"  frente {f} espejo {'si' if e else 'no'}: en el fondo {', '.join(f'{v:.1f}' for v in fondo)} % "
              f"(frente, espalda, derecha, izquierda)")
        if mejor is None or sum(fondo) < mejor[0]:
            mejor = (sum(fondo), f, e)
    _, f, e = mejor
    print(f"Orientacion elegida: frente {f}, espejo {'si' if e else 'no'}")
    P, idx = espejar(P0, idx0) if e else (P0, idx0)
    F = np.array(EJES[f], float)
    vistas = armar_vistas(a, P, F, tmp)
    frente, espalda = vistas[0][0], vistas[1][0]

    T = a.lado
    tex = np.zeros((T, T, 3))
    peso_tex = np.zeros((T, T))
    tris = P[idx]
    normales = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    normales /= np.maximum(np.linalg.norm(normales, axis=1, keepdims=True), 1e-12)
    uvs = UV[idx] * (T - 1)
    for t in range(len(idx)):
        (ax, ay), (bx, by), (cx, cy) = uvs[t]
        x0, x1 = int(np.floor(min(ax, bx, cx))), int(np.ceil(max(ax, bx, cx)))
        y0, y1 = int(np.floor(min(ay, by, cy))), int(np.ceil(max(ay, by, cy)))
        if x1 < 0 or y1 < 0 or x0 >= T or y0 >= T:
            continue
        xs, ys = np.meshgrid(np.arange(max(x0, 0), min(x1, T - 1) + 1), np.arange(max(y0, 0), min(y1, T - 1) + 1))
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-12:
            continue
        l1 = ((by - cy) * (xs - cx) + (cx - bx) * (ys - cy)) / den
        l2 = ((cy - ay) * (xs - cx) + (ax - cx) * (ys - cy)) / den
        l3 = 1 - l1 - l2
        dentro = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
        if not dentro.any():
            continue
        X = (l1[dentro, None] * tris[t, 0] + l2[dentro, None] * tris[t, 1] + l3[dentro, None] * tris[t, 2])
        n = normales[t]
        acum, total = np.zeros((len(X), 3)), 0.0
        for vista, direccion in vistas:
            w = max(0.0, float(n @ direccion)) ** 2
            if w > 0:
                acum += w * vista.color(X)
                total += w
        if total < 1e-6:  # cara horizontal (coronilla, hombros): frente y espalda por igual
            acum = 0.5 * (frente.color(X) + espalda.color(X))
            total = 1.0
        yy, xx = ys[dentro], xs[dentro]
        tex[yy, xx] = acum / total
        peso_tex[yy, xx] = 1.0
    # rellenar los huecos entre islas UV para que el filtrado no muestre costuras
    for _ in range(12):
        vacio = peso_tex == 0
        if not vacio.any():
            break
        suma = np.zeros_like(tex)
        cuenta = np.zeros_like(peso_tex)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            suma += np.roll(tex * peso_tex[..., None], (dy, dx), (0, 1))
            cuenta += np.roll(peso_tex, (dy, dx), (0, 1))
        nuevo = vacio & (cuenta > 0)
        tex[nuevo] = suma[nuevo] / cuenta[nuevo, None]
        peso_tex[nuevo] = 1.0
    img = Image.fromarray(np.clip(tex, 0, 255).astype(np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    escribir_glb(a.salida, P, UV, idx, buf.getvalue(), Path(a.salida).stem)
    img.resize((512, 512)).save(Path(a.salida).with_suffix(".textura.png"))
    meta = {"entrada": Path(a.entrada).name, "frente": f, "espejo": e, "triangulos": int(len(idx)),
            "textura": T, "en_fondo_pct": dict(zip(["frente", "espalda", "derecha", "izquierda"],
                                                   [round(v, 1) for v in en_fondo(vistas, P, idx)]))}
    Path(a.salida).with_suffix(".json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{Path(a.salida).name}: {len(idx)} triangulos, textura {T}x{T}, {len(buf.getvalue()) // 1024} KB")


if __name__ == "__main__":
    main()
