"""Enfoque D: deforma la geometria de PER-01 para que sus siluetas de frente, perfil y espalda
se parezcan mas a las de la hoja. No toca UV, indices, material ni textura.

Uso (desde la raiz del proyecto):
  python -I herramientas/mallas/ajustar_silueta_D.py [--entrada glb] [--salida glb] [--diagnosticos carpeta]

Metodo:
  1. Alinea cada vista con la hoja con UNA escala y UN desplazamiento (alinear() de proyectar_hoja.py).
  2. Por vista, rasteriza la silueta de la malla y la compara con la mascara de la hoja. Empareja
     puntos de contorno (malla -> hoja y hoja -> malla, el mas cercano con normal compatible) y obtiene
     muestras de desplazamiento 2D. La zona del bolso se ignora: el bolso 3D va aparte.
  3. Interpola esas muestras con nucleo gaussiano (campo suave) en la posicion proyectada de cada vertice.
  4. Compone el 3D por ejes: X solo lo ve el perfil; Z lo ven frente y espalda (mezcla segun cuanto mira
     el vertice a cada una); Y lo ven las tres (mezcla por orientacion).
  5. Suaviza el desplazamiento sobre la malla soldada, lo limita a 4 cm y revisa caras invertidas.
  6. Repite unas vueltas y guarda el GLB con las mismas UV y la textura original.
"""
import argparse
import json
import struct
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import proyectar_hoja as ph  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
LOTE = RAIZ / "Nasa_Game/Fase_1_Arte/Modelado/Lote_04"
# Cajas del bolso en coordenadas de cada recorte de la hoja (medidas a ojo sobre la hoja).
BOLSO = {"frente": (100, 458, 215, 628), "perfil": (105, 458, 186, 634), "espalda": (300, 452, 400, 630)}
MARGEN = 60          # px de lienzo extra alrededor del recorte
RADIO = 48           # px maximos de emparejamiento
SIGMA = 16           # px del nucleo gaussiano del campo
W0 = 0.01            # peso del "cero" en la interpolacion (aleja el campo de los contornos)
MAX_M = 0.04         # desplazamiento maximo por vertice, en metros


def morf(m, filtro, k):
    return np.asarray(Image.fromarray(m.astype(np.uint8) * 255).filter(filtro(k))) > 127


def limpiar(m):
    """Cierra y abre 5 px y rellena huecos chicos (no los huecos grandes reales)."""
    m = morf(morf(m, ImageFilter.MaxFilter, 5), ImageFilter.MinFilter, 5)
    m = morf(morf(m, ImageFilter.MinFilter, 5), ImageFilter.MaxFilter, 5)
    img = Image.fromarray(np.pad(m, 1).astype(np.uint8) * 255)
    ImageDraw.floodfill(img, (0, 0), 128)
    fondo = np.asarray(img)[1:-1, 1:-1] == 128
    huecos = ~m & ~fondo
    grandes = morf(morf(huecos, ImageFilter.MinFilter, 9), ImageFilter.MaxFilter, 9)
    return m | (huecos & ~grandes)


def contorno(m):
    """Pixeles del borde de la mascara y su normal hacia afuera."""
    b = m & ~morf(m, ImageFilter.MinFilter, 3)
    suave = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.GaussianBlur(3)), np.float32)
    gy, gx = np.gradient(suave)
    ys, xs = np.nonzero(b)
    n = -np.column_stack((gx[ys, xs], gy[ys, xs]))
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-6)
    return np.column_stack((xs, ys)).astype(np.float64), n


def emparejar(pa, na, pb, nb):
    """Para cada punto de a, el punto de b mas cercano con normal compatible (dentro de RADIO)."""
    j = np.full(len(pa), -1)
    for i0 in range(0, len(pa), 400):
        d2 = ((pa[i0:i0 + 400, None, :] - pb[None]) ** 2).sum(-1)
        d2[(na[i0:i0 + 400] @ nb.T) < 0.3] = np.inf
        k = np.argmin(d2, 1)
        ok = d2[np.arange(len(k)), k] <= RADIO ** 2
        j[i0:i0 + 400][ok] = k[ok]
    return j


def interpolar(xy, d, q):
    out = np.zeros((len(q), 2))
    if not len(xy):
        return out
    for i0 in range(0, len(q), 500):
        d2 = ((q[i0:i0 + 500, None, :] - xy[None]) ** 2).sum(-1)
        w = np.exp(-d2 / (2 * SIGMA ** 2))
        out[i0:i0 + 500] = (w @ d) / (w.sum(1, keepdims=True) + W0)
    return out


class VistaD:
    def __init__(self, nombre, hoja, pos, tri):
        self.nombre = nombre
        rgb = np.asarray(hoja.crop(ph.CAJAS[nombre]).convert("RGB"))
        m, _ = ph.mascara(rgb)
        self.eje = np.array(ph.EJES[nombre][0], float)
        self.dir = np.array(ph.EJES[nombre][1], float)
        self.escala, self.tras, self.info = ph.alinear(pos, tri, self.eje, m)
        self.hoja = limpiar(np.pad(m, MARGEN))
        self.alto, self.ancho = self.hoja.shape
        x0, y0, x1, y1 = BOLSO[nombre]
        self.bolso = np.zeros_like(self.hoja)
        self.bolso[y0 + MARGEN:y1 + MARGEN, x0 + MARGEN:x1 + MARGEN] = True
        self.pt, self.nt = contorno(self.hoja)
        fuera = ~self.bolso[self.pt[:, 1].astype(int), self.pt[:, 0].astype(int)]
        self.pt, self.nt = self.pt[fuera], self.nt[fuera]

    def proyectar(self, pos):
        return np.column_stack((pos @ self.eje, -pos[:, 1])) * self.escala + self.tras + MARGEN

    def silueta(self, pos, tri):
        _, du = ph.rasterizar(self.proyectar(pos), np.zeros(len(pos)), tri, self.ancho, self.alto)
        return limpiar(du >= 0)

    def iou(self, s, sin_bolso=False):
        h = self.hoja
        if sin_bolso:
            h, s = h & ~self.bolso, s & ~self.bolso
        return float((h & s).sum() / max((h | s).sum(), 1))

    def campo(self, pos, tri):
        """Desplazamiento 2D en px (hoja) por vertice y diagnosticos."""
        s = self.silueta(pos, tri)
        ps, ns = contorno(s)
        fuera = ~self.bolso[ps[:, 1].astype(int), ps[:, 0].astype(int)]
        ps, ns = ps[fuera], ns[fuera]
        j = emparejar(ps, ns, self.pt, self.nt)
        k = emparejar(self.pt, self.nt, ps, ns)
        a = j >= 0
        b = k >= 0
        xy = np.concatenate((ps[a], ps[k[b]]))
        d = np.concatenate((self.pt[j[a]] - ps[a], self.pt[b] - ps[k[b]]))
        # Contornos de malla sin pareja: anclas en cero (no se inventa forma).
        xy = np.concatenate((xy, ps[~a]))
        d = np.concatenate((d, np.zeros((int((~a).sum()), 2))))
        largo = np.linalg.norm(d, axis=1, keepdims=True)
        d *= np.minimum(1, RADIO / np.maximum(largo, 1e-9))
        return interpolar(xy, d, self.proyectar(pos)), s, {"pares_malla_hoja": int(a.sum()),
                                                          "pares_hoja_malla": int(b.sum()),
                                                          "contorno_sin_pareja": int((~a).sum())}

    def superposicion(self, s, ruta):
        sup = np.full(s.shape + (3,), 40, np.uint8)
        sup[self.hoja & s] = [210, 210, 210]
        sup[self.hoja & ~s] = [220, 60, 60]
        sup[s & ~self.hoja] = [70, 110, 230]
        img = Image.fromarray(sup)
        x0, y0, x1, y1 = BOLSO[self.nombre]
        ImageDraw.Draw(img).rectangle((x0 + MARGEN, y0 + MARGEN, x1 + MARGEN, y1 + MARGEN), outline=(240, 200, 60))
        img.save(ruta)


def soldar(pos):
    clave = np.round(pos, 6)
    _, primero, inversa = np.unique(clave, axis=0, return_index=True, return_inverse=True)
    return primero, inversa.ravel()


def normales_caras(p, tri):
    c = np.cross(p[tri[:, 1]] - p[tri[:, 0]], p[tri[:, 2]] - p[tri[:, 0]])
    return c


def normales_vertices(p, tri):
    c = normales_caras(p, tri)
    n = np.zeros_like(p)
    for k in range(3):
        np.add.at(n, tri[:, k], c)
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)


def suavizar(d, tri, n, pasos=12, lam=0.6):
    vecinos = np.concatenate((tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]))
    vecinos = np.concatenate((vecinos, vecinos[:, ::-1]))
    grado = np.bincount(vecinos[:, 0], minlength=n).astype(float)[:, None]
    for _ in range(pasos):
        suma = np.zeros_like(d)
        np.add.at(suma, vecinos[:, 0], d[vecinos[:, 1]])
        d = (1 - lam) * d + lam * suma / np.maximum(grado, 1)
    return d


def sigmoide(x):
    return 1 / (1 + np.exp(-x))


def componer(vistas, campos, p, tri):
    """Pasa los campos 2D a 3D por ejes, mezclando por orientacion del vertice."""
    n = normales_vertices(p, tri)
    f, pe, e = vistas["frente"], vistas["perfil"], vistas["espalda"]
    cf, cp, ce = campos["frente"], campos["perfil"], campos["espalda"]
    d = np.zeros_like(p)
    # X: solo el perfil lo ve (eje de imagen del perfil = +X).
    d[:, 0] = cp[:, 0] / pe.escala
    # Z: frente (eje de imagen -Z) y espalda (eje +Z), mezclados por cuanto mira el vertice a cada una.
    wf = sigmoide(4 * n[:, 0])
    d[:, 2] = wf * (-cf[:, 0] / f.escala) + (1 - wf) * (ce[:, 0] / e.escala)
    # Y: las tres vistas (fila de imagen = -Y).
    w = np.column_stack((0.05 + np.maximum(n[:, 0], 0) ** 2, 0.05 + np.maximum(-n[:, 0], 0) ** 2, 0.05 + n[:, 2] ** 2))
    dy = np.column_stack((-cf[:, 1] / f.escala, -ce[:, 1] / e.escala, -cp[:, 1] / pe.escala))
    d[:, 1] = (w * dy).sum(1) / w.sum(1)
    return d


def limitar(t):
    largo = np.linalg.norm(t, axis=1, keepdims=True)
    return t * np.minimum(1, MAX_M / np.maximum(largo, 1e-12))


def corregir_invertidas(p0, t, tri, n0, area0):
    """Reduce el desplazamiento en los vertices de caras invertidas o colapsadas."""
    for vuelta in range(40):
        c = normales_caras(p0 + t, tri)
        area = np.linalg.norm(c, axis=1)
        malas = ((c * n0).sum(1) <= 0) | (area < 0.2 * area0)
        if not malas.any():
            return vuelta, 0
        v = np.unique(tri[malas])
        t[v] *= 0.6
    return 40, int(malas.sum())


def escribir_glb(ruta, doc, binario, pos_local, nor_local):
    nuevo = bytearray(binario)
    p = doc["meshes"][0]["primitives"][0]["attributes"]
    for clave, datos in (("POSITION", pos_local), ("NORMAL", nor_local)):
        a = doc["accessors"][p[clave]]
        v = doc["bufferViews"][a["bufferView"]]
        if v.get("byteStride", 12) != 12:
            raise ValueError("Se esperaba un accessor VEC3 compacto")
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        crudo = datos.astype("<f4").tobytes()
        nuevo[off:off + len(crudo)] = crudo
        a["min"] = datos.min(0).astype(float).tolist()
        a["max"] = datos.max(0).astype(float).tolist()
    js = json.dumps(doc, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    js += b" " * (-len(js) % 4)
    nuevo.extend(b"\0" * (-len(nuevo) % 4))
    ruta.write_bytes(struct.pack("<III", 0x46546C67, 2, 28 + len(js) + len(nuevo))
                     + struct.pack("<II", len(js), 0x4E4F534A) + js
                     + struct.pack("<II", len(nuevo), 0x004E4942) + bytes(nuevo))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", type=Path, default=LOTE / "L04_PER01_giro_tripo_mv.glb")
    ap.add_argument("--salida", type=Path, default=LOTE / "L04_PER01_v4D_geometria.glb")
    ap.add_argument("--diagnosticos", type=Path, default=LOTE / "parecido/v4D/ajuste")
    ap.add_argument("--vueltas", type=int, default=5)
    a = ap.parse_args()
    if a.entrada.resolve() == a.salida.resolve():
        raise ValueError("La salida no puede sobrescribir la entrada")
    inicio = time.monotonic()
    a.diagnosticos.mkdir(parents=True, exist_ok=True)
    doc, binario = ph.leer_glb(a.entrada)
    pos, uv, idx, normales, _, _ = ph.geometria(doc, binario)
    primero, inv = soldar(pos)
    p0 = pos[primero]
    tri = inv[idx]
    tri = tri[(tri[:, 0] != tri[:, 1]) & (tri[:, 1] != tri[:, 2]) & (tri[:, 2] != tri[:, 0])]
    n0 = normales_caras(p0, tri)
    area0 = np.linalg.norm(n0, axis=1)
    print(f"{len(pos)} vertices ({len(p0)} soldados), {len(idx)} triangulos", flush=True)
    hoja = Image.open(ph.HOJA).convert("RGB")
    vistas = {}
    for nombre in ph.CAJAS:
        print(f"Alineando {nombre}...", flush=True)
        vistas[nombre] = VistaD(nombre, hoja, p0, tri)
        print(f"  IoU {vistas[nombre].info['iou']:.4f}", flush=True)
    t = np.zeros_like(p0)
    registro = []
    for vuelta in range(a.vueltas + 1):
        p = p0 + t
        campos, sil, info = {}, {}, {}
        for nombre, v in vistas.items():
            campos[nombre], sil[nombre], info[nombre] = v.campo(p, tri)
            info[nombre]["iou"] = round(v.iou(sil[nombre]), 4)
            info[nombre]["iou_sin_bolso"] = round(v.iou(sil[nombre], True), 4)
            if vuelta in (0, a.vueltas):
                v.superposicion(sil[nombre], a.diagnosticos / f"{nombre}_{'antes' if vuelta == 0 else 'despues'}.png")
        registro.append({"vuelta": vuelta, "vistas": info,
                         "desplazamiento_max_cm": round(float(np.linalg.norm(t, axis=1).max() * 100), 2),
                         "desplazamiento_medio_cm": round(float(np.linalg.norm(t, axis=1).mean() * 100), 2)})
        print(json.dumps(registro[-1]), flush=True)
        if vuelta == a.vueltas:
            break
        d = componer(vistas, campos, p, tri)
        d = suavizar(d, tri, len(p0))
        t = limitar(t + d)
        t = suavizar(t, tri, len(p0), pasos=4, lam=0.5)
        t = limitar(t)
        arreglos, quedan = corregir_invertidas(p0, t, tri, n0, area0)
        if arreglos:
            print(f"  correccion de caras: {arreglos} pasos, quedan {quedan}", flush=True)
    c = normales_caras(p0 + t, tri)
    invertidas = int(((c * n0).sum(1) <= 0).sum())
    colapsadas = int((np.linalg.norm(c, axis=1) < 0.2 * area0).sum())
    # Normales: suaves soldadas donde el original era suave; locales donde habia arista dura.
    pw = (p0 + t)[inv]
    n_sold0 = normales_vertices(p0, tri)[inv]
    n_sold1 = normales_vertices(p0 + t, tri)[inv]
    n_loc1 = normales_vertices(pw, idx)
    suave = (normales * n_sold0).sum(1) > 0.98
    nuevas = np.where(suave[:, None], n_sold1, n_loc1)
    # Volver al espacio local del nodo.
    nodo = [n for n in doc["nodes"] if "mesh" in n][0]
    mat = np.array(nodo.get("matrix", np.eye(4).T.ravel()), float).reshape(4, 4).T
    pos_local = (pw - mat[:3, 3]) @ np.linalg.inv(mat[:3, :3]).T
    nor_local = nuevas @ mat[:3, :3]
    nor_local /= np.maximum(np.linalg.norm(nor_local, axis=1, keepdims=True), 1e-12)
    escribir_glb(a.salida, doc, binario, pos_local, nor_local)
    # Comprobaciones: UV, indices y textura intactos; posiciones releidas iguales.
    d2, b2 = ph.leer_glb(a.salida)
    d0, b0 = ph.leer_glb(a.entrada)
    pos2, uv2, idx2, _, tex2, _ = ph.geometria(d2, b2)
    assert np.array_equal(uv2, uv) and np.array_equal(idx2, idx)
    assert np.allclose(pos2, pw, atol=1e-5)
    for clave in ("materials", "textures", "images", "nodes", "bufferViews"):
        assert d2[clave] == d0[clave], clave
    largo = np.linalg.norm(t, axis=1)
    # Mapa del desplazamiento en el frente (px de la hoja, para ver donde se movio).
    f = vistas["frente"]
    q = f.proyectar(p0)
    img = Image.new("RGB", (f.ancho, f.alto), (30, 30, 30))
    dib = ImageDraw.Draw(img)
    for i in np.argsort(-q[:, 1] * 0):
        c = int(min(255, largo[i] / MAX_M * 255))
        dib.point((float(q[i, 0]), float(q[i, 1])), fill=(c, 80, 255 - c))
    img.save(a.diagnosticos / "frente_desplazamiento.png")
    meta = {"entrada": str(a.entrada), "salida": str(a.salida), "vertices": len(pos), "soldados": len(p0),
            "triangulos": len(idx), "max_cm": round(float(largo.max() * 100), 2),
            "medio_cm": round(float(largo.mean() * 100), 2), "p95_cm": round(float(np.percentile(largo, 95) * 100), 2),
            "vertices_mas_1cm": int((largo > 0.01).sum()), "caras_invertidas": invertidas,
            "caras_colapsadas_20pct": colapsadas, "caja_mundo": [pw.min(0).tolist(), pw.max(0).tolist()],
            "parametros": {"radio_px": RADIO, "sigma_px": SIGMA, "w0": W0, "max_m": MAX_M, "vueltas": a.vueltas,
                           "bolso_ignorado": BOLSO},
            "alineacion": {k: v.info for k, v in vistas.items()},
            "registro": registro, "segundos": round(time.monotonic() - inicio, 1)}
    (a.diagnosticos / "ajuste.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("max_cm", "medio_cm", "p95_cm", "caras_invertidas",
                                            "caras_colapsadas_20pct", "segundos")}), flush=True)


if __name__ == "__main__":
    main()
