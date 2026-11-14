"""Enfoque A: repinta PER-01 desde la hoja con alineacion por bandas y mezcla dominante.

Variante de proyectar_hoja.py (v3). Cambios:
  1) cada vista se alinea por bandas horizontales (cabeza 0-38 %, torso 38-62 %, piernas 62-100 %
     del alto de la figura). Cada banda busca su escala y desplazamiento por IoU de silueta dentro
     de su franja; los parametros se interpolan con smoothstep entre bandas para no rasgar la textura;
  2) mezcla dominante: peso de vista = visible * max(0, n.d) * mascara suave; los pesos de las vistas
     se normalizan y se elevan al cuadrado (transicion suave pero con una vista dominante); la textura
     original pesa 0,01 donde alguna vista ve el texel, asi desaparecen los rasgos de Tripo;
  3) lo que ninguna vista pinta (costado izquierdo -Z y zonas ocultas) conserva la textura de Tripo,
     pero con su color ajustado (media y desviacion en Lab por zona: piel, pelo, camisa, pantalon,
     zapatos, oscuro) a los texels proyectados vecinos.

Uso: python -I herramientas/mallas/proyectar_hoja_A.py
Solo requiere numpy y Pillow. No usa Blender para el horneado.
"""
import argparse
import hashlib
import io
import json
import struct
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


RAIZ = Path(__file__).resolve().parents[2]
LOTE = RAIZ / "Nasa_Game/Fase_1_Arte/Modelado/Lote_04"
HOJA = RAIZ / "Nasa_Game/Fase_1_Arte/Exploracion/Lote_02/L02_protagonista_tipo1_hoja.png"
CAJAS = {"frente": (200, 10, 720, 923), "perfil": (1410, 10, 1790, 923),
         "espalda": (1960, 10, 2450, 923)}
# La derecha de la imagen es -Z, +X y +Z respectivamente.
EJES = {"frente": ([0, 0, -1], [1, 0, 0]),
        "perfil": ([1, 0, 0], [0, 0, 1]),
        "espalda": ([0, 0, 1], [-1, 0, 0])}
DT = {5126: "<f4", 5125: "<u4", 5123: "<u2", 5121: "u1"}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}

# Bandas en fraccion del alto de la figura, desde arriba
BANDAS = (("cabeza", 0.0, 0.38), ("torso", 0.38, 0.62), ("piernas", 0.62, 1.0))
TRANSICION = 0.04      # semiancho (fraccion del alto) de la mezcla smoothstep entre bandas
# Desplazamiento maximo por banda, fraccion del ancho / alto de la figura. El vertical es menor:
# con 5 % el torso del perfil subia 41 px para cubrir el bolso de la hoja (que la malla no tiene).
LIMITE_BANDA = (0.05, 0.025)
EXPONENTE = 4.0        # pesos normalizados elevados a este exponente (2 = "al cuadrado" del encargo; 4 deja menos fantasmas)
PERFIL_CABEZA = 0.3    # factor del perfil en la banda de la cabeza: la cara del frente pesa doble en la metrica
ESCALAS_BANDA = (0.93, 1.07)
PESO_ORIGINAL = 0.01
RAMPA_IZQ = 0.20       # margen angular para pasar suave de las vistas a Tripo junto al sector -Z
# Zonas de color: semilla RGB y altura (fraccion desde arriba)
ZONAS = {"pelo": ((70, 42, 30), 0.10), "piel": ((214, 132, 82), 0.30),
         "camisa": ((200, 170, 128), 0.35), "pantalon": ((122, 76, 46), 0.65),
         "zapatos": ((222, 200, 196), 0.95), "oscuro": ((40, 34, 34), 0.40)}
RASANTE = 0.2          # n.d por debajo del cual una vista no aporta (0 = max(0, n.d) del encargo); quita estiramientos rasantes
RAZON_MAX = 1.3        # limite de la razon de desviaciones (hoja / Tripo) del ajuste de color
PESO_ALTURA = 40.0     # unidades Lab por unidad de altura en el k-means de zonas
SIGMA_ZONA = 8.0       # suavizado (Lab) de la pertenencia a zonas


def leer_glb(ruta):
    datos = Path(ruta).read_bytes()
    magia, version, largo = struct.unpack_from("<III", datos)
    if (magia, version, largo) != (0x46546C67, 2, len(datos)):
        raise ValueError("GLB 2.0 invalido")
    trozos = {}
    off = 12
    while off < len(datos):
        n, tipo = struct.unpack_from("<II", datos, off)
        trozos[tipo] = datos[off + 8:off + 8 + n]
        off += 8 + n
    doc = json.loads(trozos[0x4E4F534A])
    return doc, trozos[0x004E4942]


def accessor(doc, binario, indice):
    a = doc["accessors"][indice]
    if "sparse" in a:
        raise ValueError("No se admiten accessors sparse")
    v = doc["bufferViews"][a["bufferView"]]
    dt = np.dtype(DT[a["componentType"]])
    k = NC[a["type"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return np.ndarray((a["count"], k), dt, binario, off,
                      (v.get("byteStride", dt.itemsize * k), dt.itemsize)).copy()


def geometria(doc, binario):
    # Este recurso tiene un solo nodo con malla y una matriz sin jerarquia.
    nodos = [n for n in doc["nodes"] if "mesh" in n]
    if len(nodos) != 1 or any(n.get("children") for n in doc["nodes"]):
        raise ValueError("Se esperaba una sola malla sin jerarquia")
    nodo = nodos[0]
    prims = doc["meshes"][nodo["mesh"]]["primitives"]
    if len(prims) != 1 or prims[0].get("mode", 4) != 4:
        raise ValueError("Se esperaba una primitiva de triangulos")
    p = prims[0]
    if any(k in nodo for k in ("translation", "rotation", "scale")):
        raise ValueError("Este recurso debe usar matriz o identidad")
    mat = np.array(nodo.get("matrix", np.eye(4).T.ravel()), float).reshape(4, 4).T
    pos = accessor(doc, binario, p["attributes"]["POSITION"]).astype(float)
    pos = pos @ mat[:3, :3].T + mat[:3, 3]
    uv = accessor(doc, binario, p["attributes"]["TEXCOORD_0"]).astype(float)
    idx = accessor(doc, binario, p["indices"]).reshape(-1, 3).astype(int)
    normales = accessor(doc, binario, p["attributes"]["NORMAL"]).astype(float)
    normales = normales @ np.linalg.inv(mat[:3, :3])
    normales /= np.maximum(np.linalg.norm(normales, axis=1, keepdims=True), 1e-12)
    material = doc["materials"][p.get("material", 0)]
    texid = material["pbrMetallicRoughness"]["baseColorTexture"]["index"]
    imid = doc["textures"][texid]["source"]
    v = doc["bufferViews"][doc["images"][imid]["bufferView"]]
    off = v.get("byteOffset", 0)
    original = np.array(Image.open(io.BytesIO(binario[off:off + v["byteLength"]])).convert("RGB"))
    return pos, uv, idx, normales, original, imid


def mascara(rgb):
    a = np.asarray(rgb, dtype=np.float32)
    borde = np.concatenate((a[0], a[-1], a[:, 0], a[:, -1]))
    fondo = np.median(borde, axis=0)
    return np.linalg.norm(a - fondo, axis=-1) > 28, fondo


def fragmentos(tri, ancho, alto):
    """Rasteriza centros de pixel; devuelve coordenadas y pesos baricentricos."""
    x0, y0 = np.maximum(np.ceil(tri.min(0)).astype(int), 0)
    x1, y1 = np.minimum(np.floor(tri.max(0)).astype(int), [ancho - 1, alto - 1])
    if x1 < x0 or y1 < y0:
        return None
    (ax, ay), (bx, by), (cx, cy) = tri
    den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    if abs(den) < 1e-12:
        return None
    x, y = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    a = ((by - cy) * (x - cx) + (cx - bx) * (y - cy)) / den
    b = ((cy - ay) * (x - cx) + (ax - cx) * (y - cy)) / den
    c = 1 - a - b
    dentro = (a >= -1e-9) & (b >= -1e-9) & (c >= -1e-9)
    if not dentro.any():
        return None
    return y[dentro], x[dentro], np.column_stack((a[dentro], b[dentro], c[dentro]))


def rasterizar(q, profundidad, idx, ancho, alto):
    z = np.full((alto, ancho), -np.inf, dtype=np.float32)
    propietario = np.full((alto, ancho), -1, dtype=np.int32)
    for t, vertices in enumerate(idx):
        f = fragmentos(q[vertices], ancho, alto)
        if f is None:
            continue
        yy, xx, b = f
        zz = b @ profundidad[vertices]
        gana = zz > z[yy, xx]
        yy, xx = yy[gana], xx[gana]
        z[yy, xx] = zz[gana]
        propietario[yy, xx] = t
    return z, propietario


def silueta(q, idx, ancho, alto):
    """Silueta rapida con PIL (solo para alinear; la visibilidad usa rasterizar)."""
    img = Image.new("1", (int(ancho), int(alto)), 0)
    d = ImageDraw.Draw(img)
    for t in q[idx]:
        d.polygon([(float(t[0, 0]), float(t[0, 1])), (float(t[1, 0]), float(t[1, 1])),
                   (float(t[2, 0]), float(t[2, 1]))], fill=1)
    return np.asarray(img, dtype=bool)


def alinear(pos, idx, eje, m):
    """Alineacion global (igual que v3): busqueda discreta por IoU y refinamiento a un pixel."""
    alto, ancho = m.shape
    u = pos @ eje
    ymin, ymax = pos[:, 1].min(), pos[:, 1].max()
    ys, xs = np.where(m)
    alto_fig, ancho_fig = np.ptp(ys) + 1, np.ptp(xs) + 1
    escala0 = (alto_fig - 1) / (ymax - ymin)
    centro = np.array([(u.min() + u.max()) / 2, -(ymin + ymax) / 2])
    plano = np.column_stack((u, -pos[:, 1])) - centro
    q0 = plano * escala0 + [ancho / 2, alto / 2]
    duenio = silueta(q0, idx, ancho, alto)
    my, mx = np.where(duenio)
    base = np.array([xs.mean(), ys.mean()]) - np.array([mx.mean(), my.mean()]) + [ancho / 2, alto / 2]
    limite = np.array([0.06 * ancho_fig, 0.06 * alto_fig])
    mejor = None
    for paso, escalas in ((3, np.linspace(0.92, 1.08, 33)), (1, None)):
        if escalas is None:
            escalas = np.linspace(max(0.92, mejor[1] - 0.006), min(1.08, mejor[1] + 0.006), 13)
        margen = 80
        w, h = int(np.ceil(ancho / paso)) + 2 * margen, int(np.ceil(alto / paso)) + 2 * margen
        ref = np.zeros((h, w), bool)
        pequena = np.asarray(Image.fromarray(m).resize((int(np.ceil(ancho / paso)), int(np.ceil(alto / paso))), Image.Resampling.NEAREST))
        ref[margen:margen + pequena.shape[0], margen:margen + pequena.shape[1]] = pequena
        ft = np.fft.rfft2(ref)
        if paso == 3:
            dx = np.arange(int(np.ceil(-limite[0] / paso)), int(np.floor(limite[0] / paso)) + 1)
            dy = np.arange(int(np.ceil(-limite[1] / paso)), int(np.floor(limite[1] / paso)) + 1)
        else:
            dx = np.arange(max(int(np.ceil(-limite[0])), int(round(mejor[2][0])) - 4),
                           min(int(np.floor(limite[0])), int(round(mejor[2][0])) + 4) + 1)
            dy = np.arange(max(int(np.ceil(-limite[1])), int(round(mejor[2][1])) - 4),
                           min(int(np.floor(limite[1])), int(round(mejor[2][1])) + 4) + 1)
        candidato = None
        for s in escalas:
            q = (plano * (escala0 * s) + base) / paso + margen
            sil = silueta(q, idx, w, h)
            correlacion = np.fft.irfft2(ft * np.conj(np.fft.rfft2(sil)), s=ref.shape).real
            inter = np.maximum(0, np.rint(correlacion[np.ix_(dy % h, dx % w)]))
            iou = inter / np.maximum(ref.sum() + sil.sum() - inter, 1)
            iy, ix = np.unravel_index(np.argmax(iou), iou.shape)
            val = (float(iou[iy, ix]), float(s), np.array([dx[ix], dy[iy]]) * paso)
            if candidato is None or val[0] > candidato[0]:
                candidato = val
        mejor = candidato
    _, factor, delta = mejor
    escala = escala0 * factor
    tras = base + delta - centro * escala
    return escala, tras, {"escala_base": float(escala0), "factor_escala": factor,
                         "desplazamiento_px": delta.tolist(), "traslacion_px": tras.tolist()}


def buscar_banda(qg, idx, m, r0, r1, c, limite, escalas, dxs, dys, paso):
    """IoU de silueta solo en las filas [r0, r1) de la hoja, para q = c + (qg - c) * k + d.

    La interseccion sale de una correlacion FFT; el area de la malla dentro de la franja se
    obtiene con sumas acumuladas por fila, porque depende del desplazamiento vertical.
    """
    h, w = m.shape
    margen = int(np.ceil(max(limite) / paso)) + 24
    hh, ww = int(np.ceil(h / paso)), int(np.ceil(w / paso))
    H, W = hh + 2 * margen, ww + 2 * margen
    ref = np.zeros((H, W), bool)
    ref[margen:margen + hh, margen:margen + ww] = np.asarray(
        Image.fromarray(m).resize((ww, hh), Image.Resampling.NEAREST))
    R0, R1 = margen + int(round(r0 / paso)), margen + int(round(r1 / paso))
    ref[:R0] = False
    ref[R1:] = False
    nref = ref.sum()
    ft = np.fft.rfft2(ref)
    mejor = None
    for k in escalas:
        q = (c + (qg - c) * k) / paso + margen
        sil = silueta(q, idx, W, H)
        corr = np.fft.irfft2(ft * np.conj(np.fft.rfft2(sil)), s=(H, W)).real
        cs = np.concatenate(([0], np.cumsum(sil.sum(1))))
        area = cs[np.clip(R1 - dys, 0, H)] - cs[np.clip(R0 - dys, 0, H)]
        inter = np.maximum(0, np.rint(corr[np.ix_(dys % H, dxs % W)]))
        iou = inter / np.maximum(nref + area[:, None] - inter, 1)
        iy, ix = np.unravel_index(np.argmax(iou), iou.shape)
        val = (float(iou[iy, ix]), float(k), np.array([dxs[ix], dys[iy]], float) * paso)
        if mejor is None or val[0] > mejor[0]:
            mejor = val
    return mejor


def pesos_banda(t, transicion=TRANSICION):
    """Particion de la unidad sobre la altura t (0 arriba, 1 abajo) con transiciones smoothstep."""
    def ss(a, b, x):
        s = np.clip((x - a) / (b - a), 0, 1)
        return s * s * (3 - 2 * s)
    w = []
    for j, (_, lo, hi) in enumerate(BANDAS):
        entra = ss(lo - transicion, lo + transicion, t) if j > 0 else np.ones_like(t)
        sale = 1 - ss(hi - transicion, hi + transicion, t) if j < len(BANDAS) - 1 else np.ones_like(t)
        w.append(entra * sale)
    return np.stack(w, -1)


def iou_franja(sil, m, r0, r1):
    a, b = sil[r0:r1], m[r0:r1]
    return float((a & b).sum() / max((a | b).sum(), 1))


class Vista:
    def __init__(self, nombre, hoja, pos, idx, carpeta):
        self.nombre = nombre
        self.rgb = np.asarray(hoja.crop(CAJAS[nombre]).convert("RGB"))
        self.m, self.fondo = mascara(self.rgb)
        self.erosion = np.asarray(Image.fromarray(self.m.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(7))) > 0
        # Mascara suave: 0 en el borde de la erosion de 3 px y 1 a unos 11 px dentro de la figura
        nucleo = Image.fromarray(self.m.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(15))
        self.suave = np.asarray(nucleo.filter(ImageFilter.BoxBlur(4)), np.float32) / 255 * self.erosion
        self.eje, self.direccion = map(lambda a: np.array(a, float), EJES[nombre])
        h, w = self.m.shape
        escala, tras, info = alinear(pos, idx, self.eje, self.m)
        qg = np.column_stack((pos @ self.eje, -pos[:, 1])) * escala + tras
        sil_g = silueta(qg, idx, w, h)
        ymin, ymax = pos[:, 1].min(), pos[:, 1].max()
        ys, xs = np.where(self.m)
        limite = np.array([LIMITE_BANDA[0] * (np.ptp(xs) + 1), LIMITE_BANDA[1] * (np.ptp(ys) + 1)])
        bandas = []
        for nb, f0, f1 in BANDAS:
            # Franja de la hoja que corresponde a la banda de la malla bajo la alineacion global
            r0 = int(np.clip(np.floor(-(ymax - f0 * (ymax - ymin)) * escala + tras[1]), 0, h))
            r1 = int(np.clip(np.ceil(-(ymax - f1 * (ymax - ymin)) * escala + tras[1]), 0, h))
            if f1 >= 1.0:
                r1 = h
            if f0 <= 0.0:
                r0 = 0
            filas = np.flatnonzero(self.m[r0:r1].any(1))
            cx = xs[(ys >= r0) & (ys < r1)].mean() if len(filas) else w / 2
            c = np.array([cx, (r0 + r1) / 2])
            lim2 = np.ceil(limite / 2).astype(int)
            g = buscar_banda(qg, idx, self.m, r0, r1, c, limite, np.linspace(*ESCALAS_BANDA, 15),
                             np.arange(-lim2[0], lim2[0] + 1), np.arange(-lim2[1], lim2[1] + 1), 2)
            d0 = g[2].astype(int)
            fino = buscar_banda(qg, idx, self.m, r0, r1, c, limite,
                                np.linspace(max(ESCALAS_BANDA[0], g[1] - 0.006), min(ESCALAS_BANDA[1], g[1] + 0.006), 7),
                                np.arange(max(-limite[0], d0[0] - 3), min(limite[0], d0[0] + 3) + 1).astype(int),
                                np.arange(max(-limite[1], d0[1] - 3), min(limite[1], d0[1] + 3) + 1).astype(int), 1)
            iou_ini = iou_franja(sil_g, self.m, r0, r1)
            k, d = fino[1], fino[2]
            e = c * (1 - k) + d
            print(f"    {nb}: k {k:.3f}, d {d.tolist()}, IoU franja {iou_ini:.4f} -> {fino[0]:.4f}", flush=True)
            bandas.append({"banda": nb, "filas_hoja": [r0, r1], "centro_px": c.tolist(), "k": k,
                           "desplazamiento_px": d.tolist(), "e": e.tolist(),
                           "iou_franja_global": iou_ini, "iou_franja_busqueda": fino[0]})
        self.bandas = bandas
        ks = np.array([b["k"] for b in bandas])
        es = np.array([b["e"] for b in bandas])
        self.t_vert = (ymax - pos[:, 1]) / (ymax - ymin)
        # Si dos bandas vecinas discrepan mucho, se ensancha la transicion hasta que la fila
        # de la hoja crezca de forma estricta con la altura (sin pliegues ni rasgaduras).
        tt = np.linspace(0, 1, 4001)
        self.transicion = None
        for tr in (TRANSICION, 0.06, 0.08, 0.10, 0.12):
            wt = pesos_banda(tt, tr)
            fila = (-(ymax - tt * (ymax - ymin)) * escala + tras[1]) * (wt @ ks) + (wt @ es)[:, 1]
            pendiente = np.diff(fila) / np.diff(tt)
            print(f"    transicion {tr}: pendiente minima {pendiente.min():.1f} px por alto (nominal {escala * (ymax - ymin):.1f})", flush=True)
            if pendiente.min() > 0.5 * escala * (ymax - ymin):
                self.transicion = tr
                break
        self.monotona = self.transicion is not None
        if not self.monotona:
            raise AssertionError(f"{nombre}: la interpolacion de bandas pliega o estira demasiado la textura")
        wv = pesos_banda(self.t_vert, self.transicion)
        self.qv = qg * (wv @ ks)[:, None] + wv @ es
        sil = silueta(self.qv, idx, w, h)
        for b in bandas:
            b["iou_franja_final"] = iou_franja(sil, self.m, *b["filas_hoja"])
        self.info = {**info, "iou_global": float((sil_g & self.m).sum() / max((sil_g | self.m).sum(), 1)),
                     "iou_bandas": float((sil & self.m).sum() / max((sil | self.m).sum(), 1)),
                     "fila_monotona": self.monotona, "transicion": self.transicion, "bandas": bandas}
        self.super = 2
        self.z, self.du = rasterizar(self.qv * self.super, pos @ self.direccion, idx, w * self.super, h * self.super)
        matrices = np.concatenate((self.qv[idx], np.ones((len(idx), 3, 1))), axis=2)
        validos = np.abs(np.linalg.det(matrices)) > 1e-10
        self.planos = np.zeros((len(idx), 3))
        self.planos[validos] = np.linalg.solve(matrices[validos], (pos @ self.direccion)[idx][validos, :, None])[..., 0]
        self.contribuciones = self.fondo_muestras = self.ocultos = 0
        Image.fromarray((self.suave * 255).astype(np.uint8)).save(carpeta / f"{nombre}_mascara_suave.png")
        sup = np.full((h, w, 3), 40, np.uint8)
        sup[self.m & sil] = [210, 210, 210]
        sup[self.m & ~sil] = [220, 60, 60]
        sup[sil & ~self.m] = [70, 110, 230]
        for b in bandas[1:]:
            sup[b["filas_hoja"][0], :] = [250, 220, 60]
        Image.fromarray(sup).save(carpeta / f"{nombre}_alineacion.png")

    def muestrear(self, q, puntos, normales, triangulo):
        x, y = q.T
        h, w = self.m.shape
        dot = normales @ self.direccion
        valido = (x >= 0) & (x < w - 1) & (y >= 0) & (y < h - 1) & (dot > 0)
        ids = np.flatnonzero(valido)
        pesos = np.zeros(len(puntos), np.float32)
        colores = np.zeros((len(puntos), 3), np.float32)
        fondo = np.zeros(len(puntos), bool)
        if not len(ids):
            return colores, pesos, fondo
        x0, y0 = np.floor(q[ids]).astype(int).T
        seguro = self.erosion[y0, x0] & self.erosion[y0 + 1, x0] & self.erosion[y0, x0 + 1] & self.erosion[y0 + 1, x0 + 1]
        ids = ids[seguro]
        if not len(ids):
            return colores, pesos, fondo
        pix = np.clip(np.rint(q[ids] * self.super).astype(int), 0, [w * self.super - 1, h * self.super - 1])
        du = self.du[pix[:, 1], pix[:, 0]]
        zreal = puntos[ids] @ self.direccion
        zvisible = (self.planos[np.maximum(du, 0), :2] * q[ids]).sum(1) + self.planos[np.maximum(du, 0), 2]
        visible = (du >= 0) & ((du == triangulo) | (np.abs(zreal - zvisible) <= 2e-5))
        self.ocultos += int((~visible).sum())
        ids = ids[visible]
        if not len(ids):
            return colores, pesos, fondo
        x0, y0 = np.floor(q[ids]).astype(int).T
        fx, fy = (q[ids] - np.column_stack((x0, y0))).T
        a = self.rgb[y0, x0].astype(np.float32)
        b = self.rgb[y0, x0 + 1].astype(np.float32)
        c = self.rgb[y0 + 1, x0].astype(np.float32)
        d = self.rgb[y0 + 1, x0 + 1].astype(np.float32)
        colores[ids] = (a * ((1 - fx) * (1 - fy))[:, None] + b * (fx * (1 - fy))[:, None]
                        + c * ((1 - fx) * fy)[:, None] + d * (fx * fy)[:, None])
        # Peso dominante: n.d a la primera potencia por la mascara suave
        pesos[ids] = np.clip((dot[ids] - RASANTE) / (1 - RASANTE), 0, 1) * self.suave[y0, x0]
        mal = ~(self.m[y0, x0] & self.m[y0, x0 + 1] & self.m[y0 + 1, x0] & self.m[y0 + 1, x0 + 1])
        fondo[ids] = mal
        self.contribuciones += len(ids)
        self.fondo_muestras += int(mal.sum())
        return colores, pesos, fondo


# --- color: sRGB <-> Lab (D65) ---
_M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
               [0.0193339, 0.1191920, 0.9503041]])
_MI = np.linalg.inv(_M)
_BLANCO = np.array([0.95047, 1.0, 1.08883])


def rgb_a_lab(rgb):
    c = np.asarray(rgb, np.float64) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = c @ _M.T / _BLANCO
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack((116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])), -1)


def lab_a_rgb(lab):
    fy = (lab[:, 0] + 16) / 116
    f = np.stack((fy + lab[:, 1] / 500, fy, fy - lab[:, 2] / 200), -1)
    xyz = np.where(f > 0.206893, f ** 3, (f - 16 / 116) / 7.787) * _BLANCO
    c = np.clip(xyz @ _MI.T, 0, 1)
    c = np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)
    return np.clip(c * 255, 0, 255)


def por_trozos(fn, x, n=1_000_000):
    return np.concatenate([fn(x[i:i + n]) for i in range(0, len(x), n)])


def zonas_kmeans(lab, t, rng):
    """K-means (Lab + altura) con semillas nombradas; devuelve centros."""
    nombres = list(ZONAS)
    centros = np.array([np.r_[rgb_a_lab(np.array([ZONAS[z][0]]))[0], PESO_ALTURA * ZONAS[z][1]] for z in nombres])
    muestra = rng.choice(len(lab), min(400_000, len(lab)), replace=False)
    x = np.column_stack((lab[muestra], PESO_ALTURA * t[muestra]))
    for _ in range(20):
        d = ((x[:, None, :] - centros[None]) ** 2).sum(-1)
        et = d.argmin(1)
        for j in range(len(centros)):
            if (et == j).sum() > 100:
                centros[j] = x[et == j].mean(0)
    return nombres, centros


def pertenencia(lab, t, centros):
    x = np.column_stack((lab, PESO_ALTURA * t))
    d = ((x[:, None, :] - centros[None]) ** 2).sum(-1)
    d -= d.min(1, keepdims=True)
    p = np.exp(-d / (2 * SIGMA_ZONA ** 2))
    return p / p.sum(1, keepdims=True)


def rellenar_bordes(tex, ocupado, pasos=12):
    """Extiende doce texels fuera de las islas, sin envolver los bordes del mapa."""
    m = ocupado.copy()
    for _ in range(pasos):
        vecinos = np.zeros_like(m)
        vecinos[1:] |= m[:-1]
        vecinos[:-1] |= m[1:]
        vecinos[:, 1:] |= m[:, :-1]
        vecinos[:, :-1] |= m[:, 1:]
        yy, xx = np.where(vecinos & ~m)
        if not len(yy):
            break
        suma = np.zeros((len(yy), 3), np.float32)
        cuenta = np.zeros(len(yy), np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            y, x = yy + dy, xx + dx
            valido = (y >= 0) & (y < m.shape[0]) & (x >= 0) & (x < m.shape[1])
            ids = np.flatnonzero(valido)
            ids = ids[m[y[ids], x[ids]]]
            suma[ids] += tex[y[ids], x[ids]]
            cuenta[ids] += 1
        tex[yy, xx] = np.rint(suma / cuenta[:, None]).astype(np.uint8)
        m[yy, xx] = True
    return int(m.sum() - ocupado.sum())


def guardar_glb(ruta, doc, binario, png, imid):
    # Conserva todos los bytes originales; solo anexa la imagen y cambia su enlace.
    nuevo = bytearray(binario)
    nuevo.extend(b"\0" * (-len(nuevo) % 4))
    off = len(nuevo)
    nuevo.extend(png)
    doc["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": len(png)})
    doc["images"][imid]["bufferView"] = len(doc["bufferViews"]) - 1
    doc["images"][imid]["mimeType"] = "image/png"
    doc["buffers"][0]["byteLength"] = len(nuevo)
    nuevo.extend(b"\0" * (-len(nuevo) % 4))
    js = json.dumps(doc, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    js += b" " * (-len(js) % 4)
    ruta.write_bytes(struct.pack("<III", 0x46546C67, 2, 28 + len(js) + len(nuevo))
                     + struct.pack("<II", len(js), 0x4E4F534A) + js
                     + struct.pack("<II", len(nuevo), 0x004E4942) + nuevo)


def main():
    global EXPONENTE, PERFIL_CABEZA, RASANTE
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", type=Path, default=LOTE / "L04_PER01_giro_tripo_mv.glb")
    ap.add_argument("--salida", type=Path, default=LOTE / "L04_PER01_v4A.glb")
    ap.add_argument("--hoja", type=Path, default=HOJA)
    ap.add_argument("--diagnosticos", type=Path, default=LOTE / "parecido/v4A")
    ap.add_argument("--cache", type=Path, default=None,
                    help="npz con los mapas horneados; si existe se reutiliza (solo para iterar la mezcla)")
    ap.add_argument("--exponente", type=float, default=EXPONENTE)
    ap.add_argument("--perfil-cabeza", type=float, default=PERFIL_CABEZA)
    ap.add_argument("--razon-max", type=float, default=RAZON_MAX)
    ap.add_argument("--rasante", type=float, default=RASANTE,
                    help="cambia el horneado: usar otro --cache")
    a = ap.parse_args()
    EXPONENTE, PERFIL_CABEZA, RASANTE = a.exponente, a.perfil_cabeza, a.rasante
    if a.entrada.resolve() == a.salida.resolve():
        raise ValueError("La salida no puede sobrescribir la entrada")
    inicio = time.monotonic()
    a.diagnosticos.mkdir(parents=True, exist_ok=True)
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    doc, binario = leer_glb(a.entrada)
    pos, uv, idx, normales, original, imid = geometria(doc, binario)
    hoja = Image.open(a.hoja).convert("RGB")
    vistas = []
    for nombre in CAJAS:
        print(f"Alineando {nombre}...", flush=True)
        v = Vista(nombre, hoja, pos, idx, a.diagnosticos)
        vistas.append(v)
        print(f"  IoU global {v.info['iou_global']:.4f} -> por bandas {v.info['iou_bandas']:.4f}", flush=True)
        for b in v.bandas:
            print(f"    {b['banda']}: k {b['k']:.3f}, d {b['desplazamiento_px']}, IoU franja "
                  f"{b['iou_franja_global']:.4f} -> {b['iou_franja_final']:.4f}", flush=True)
    h, w = original.shape[:2]
    ymin, ymax = pos[:, 1].min(), pos[:, 1].max()
    if a.cache is not None and a.cache.exists():
        z = np.load(a.cache)
        ocupado, lado_izq, fondo = z["ocupado"], z["lado_izq"], z["fondo"]
        pv_map, col_map, alt_map, nz_map = z["pv"], z["col"], z["alt"], z["nz"]
        print(f"Mapas horneados leidos de {a.cache}", flush=True)
    else:
        ocupado = np.zeros((h, w), bool)
        lado_izq = np.zeros((h, w), bool)
        fondo = np.zeros((h, w), bool)
        pv_map = np.zeros((len(vistas), h, w), np.float16)
        col_map = np.zeros((len(vistas), h, w, 3), np.uint8)
        alt_map = np.zeros((h, w), np.float32)
        nz_map = np.zeros((h, w), np.float32)
        uvs = uv * [w, h] - 0.5
        for t, vertices in enumerate(idx):
            f = fragmentos(uvs[vertices], w, h)
            if f is None:
                continue
            yy, xx, b = f
            puntos = b @ pos[vertices]
            n = b @ normales[vertices]
            n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
            dom = -n[:, 2] - np.maximum(np.abs(n[:, 0]), np.abs(n[:, 1]))
            izquierda = dom > 0
            # Rampa angular fuera del sector -Z: las vistas entran poco a poco junto a Tripo
            rampa = np.clip(-dom / RAMPA_IZQ, 0, 1)
            ids = np.flatnonzero(rampa > 0)
            pv = np.zeros((len(vistas), len(yy)), np.float32)
            col = np.zeros((len(vistas), len(yy), 3), np.float32)
            for j, vista in enumerate(vistas):
                if not len(ids):
                    break
                q = b[ids] @ vista.qv[vertices]
                c, p, mal = vista.muestrear(q, puntos[ids], n[ids], t)
                pv[j, ids] = p * rampa[ids]
                col[j, ids] = c
                fondo[yy[ids], xx[ids]] |= mal & (p > 0)
            pv_map[:, yy, xx] = pv
            col_map[:, yy, xx] = np.clip(np.rint(col), 0, 255).astype(np.uint8)
            alt_map[yy, xx] = (ymax - puntos[:, 1]) / (ymax - ymin)
            nz_map[yy, xx] = n[:, 2]
            lado_izq[yy, xx] = izquierda
            ocupado[yy, xx] = True
            if t % 1000 == 0:
                print(f"Horneando triangulo {t}/{len(idx)}", flush=True)
        if a.cache is not None:
            np.savez(a.cache, ocupado=ocupado, lado_izq=lado_izq, fondo=fondo, pv=pv_map,
                     col=col_map, alt=alt_map, nz=nz_map)
    occ = np.flatnonzero(ocupado.ravel())
    T = alt_map.ravel()[occ]
    pv = pv_map.reshape(len(vistas), -1)[:, occ].astype(np.float32)
    if PERFIL_CABEZA != 1.0:
        # Atenua el perfil en la cabeza (con la misma transicion suave que las bandas)
        jp = list(CAJAS).index("perfil")
        pv[jp] *= 1 - (1 - PERFIL_CABEZA) * pesos_banda(T)[:, 0]
    W = pv.sum(0)
    pn = pv / np.maximum(W, 1e-12)
    p2 = pn ** EXPONENTE
    p2 /= np.maximum(p2.sum(0), 1e-12)
    C = np.zeros((len(occ), 3), np.float32)
    for j in range(len(vistas)):
        C += p2[j][:, None] * col_map[j].reshape(-1, 3)[occ]
    del pv_map, col_map, pn
    peso_map = np.zeros((h, w), np.float32)
    peso_map.ravel()[occ] = W
    if np.any(peso_map[lado_izq] > 0):
        raise AssertionError("El sector izquierdo recibio color de una vista")

    print("Ajustando el color de Tripo por zonas...", flush=True)
    orig = original.reshape(-1, 3)[occ]
    NZ = nz_map.ravel()[occ]
    lab_o = por_trozos(rgb_a_lab, orig).astype(np.float32)
    rng = np.random.default_rng(7)
    nombres, centros = zonas_kmeans(lab_o, T, rng)
    memb = por_trozos(lambda i: pertenencia(lab_o[i], T[i], centros), np.arange(len(occ))).astype(np.float32)
    zona_dura = memb.argmax(1)
    pintado_final = (W[:, None] * C + PESO_ORIGINAL * orig) / (W + PESO_ORIGINAL)[:, None]
    # Vecinos: texels bien pintados que no estan en el costado derecho (+Z) y no tocan el -Z
    fuente = (W >= 0.5) & (NZ < 0.3)
    zonas_info = {}
    trans = []
    for j, nz in enumerate(nombres):
        sel = fuente & (zona_dura == j)
        if sel.sum() < 2000:
            sel = (W >= 0.5) & (zona_dura == j)
        if sel.sum() < 2000:
            trans.append((np.zeros(3), np.ones(3), np.zeros(3)))
            zonas_info[nz] = {"texels_zona": int((zona_dura == j).sum()), "fuente": int(sel.sum()), "ajuste": "ninguno"}
            continue
        lo = lab_o[sel].astype(np.float64)
        ln = rgb_a_lab(pintado_final[sel])
        mo, so, mn, sn = lo.mean(0), lo.std(0) + 1e-6, ln.mean(0), ln.std(0)
        r = np.clip(sn / so, 1 / a.razon_max, a.razon_max)
        trans.append((mo, r, mn))
        zonas_info[nz] = {"texels_zona": int((zona_dura == j).sum()), "fuente": int(sel.sum()),
                          "centro_lab_altura": centros[j].round(2).tolist(),
                          "media_tripo_lab": mo.round(2).tolist(), "media_hoja_lab": mn.round(2).tolist(),
                          "razon_desviacion": r.round(3).tolist()}
    print(json.dumps(zonas_info, indent=1), flush=True)

    def ajustar(i):
        lab = lab_o[i].astype(np.float64)
        acum = np.zeros_like(lab)
        for j, (mo, r, mn) in enumerate(trans):
            acum += memb[i, j:j + 1] * ((lab - mo) * r + mn)
        return lab_a_rgb(acum)
    ajustado = por_trozos(ajustar, np.arange(len(occ)))
    final = np.where((W > 0)[:, None], (W[:, None] * C + PESO_ORIGINAL * ajustado) / (W + PESO_ORIGINAL)[:, None], ajustado)
    tex = original.copy()
    plano = tex.reshape(-1, 3)
    plano[occ] = np.clip(np.rint(final), 0, 255).astype(np.uint8)
    # Mapa de zonas para revisar
    paleta = np.array([[230, 40, 40], [40, 200, 60], [40, 90, 230], [230, 200, 40], [200, 40, 200], [40, 220, 220]], np.uint8)
    zmap = np.zeros((h * w, 3), np.uint8)
    zmap[occ] = paleta[zona_dura]
    Image.fromarray(zmap.reshape(h, w, 3)).resize((1024, 1024), Image.Resampling.NEAREST).save(a.diagnosticos / "zonas_uv.png")
    pintado = peso_map > 0
    dominante = peso_map / (peso_map + PESO_ORIGINAL) > 0.5
    print("Rellenando bordes UV...", flush=True)
    padding = rellenar_bordes(tex, ocupado)
    imagen = Image.fromarray(tex)
    imagen.save(a.diagnosticos / "textura.png")
    Image.fromarray(pintado).save(a.diagnosticos / "texels_hoja.png")
    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    guardar_glb(a.salida, doc, binario, buf.getvalue(), imid)
    d2, b2 = leer_glb(a.salida)
    d0, b0 = leer_glb(a.entrada)
    assert b2[:len(b0)] == b0
    for clave in ("meshes", "nodes", "accessors", "materials", "textures", "scenes"):
        assert d2[clave] == d0[clave], clave
    assert d2["bufferViews"][:-1] == d0["bufferViews"]
    sup = ocupado.sum()
    meta = {"entrada": str(a.entrada), "salida": str(a.salida), "hoja": str(a.hoja),
            "sha256_entrada": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
            "sha256_hoja": hashlib.sha256(a.hoja.read_bytes()).hexdigest(),
            "triangulos": len(idx), "textura_px": [w, h],
            "texels_superficie": int(sup), "texels_con_hoja": int(pintado.sum()),
            "texels_con_hoja_pct_superficie": float(100 * pintado.sum() / sup),
            "texels_hoja_dominante_pct_superficie": float(100 * dominante.sum() / sup),
            "texels_fondo": int(fondo.sum()), "muestras_fondo": sum(v.fondo_muestras for v in vistas),
            "texels_izquierda": int(lado_izq.sum()), "padding_texels": padding,
            "peso_original": PESO_ORIGINAL, "exponente": EXPONENTE, "perfil_cabeza": PERFIL_CABEZA, "razon_max": a.razon_max, "rasante": RASANTE,
            "limite_banda": LIMITE_BANDA, "rampa_izquierda": RAMPA_IZQ, "bandas": BANDAS,
            "transicion": TRANSICION, "zonas": zonas_info,
            "vistas": {v.nombre: {**v.info, "muestras_aceptadas": v.contribuciones,
                                    "muestras_sobre_fondo": v.fondo_muestras,
                                    "muestras_ocultas_rechazadas": v.ocultos} for v in vistas},
            "segundos": round(time.monotonic() - inicio, 1)}
    (a.diagnosticos / "horneado.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("texels_con_hoja_pct_superficie", "texels_hoja_dominante_pct_superficie",
                                           "texels_fondo", "segundos")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
