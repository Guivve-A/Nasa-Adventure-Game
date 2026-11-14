"""Repinta PER-01 desde la hoja, sin modificar geometria, UV ni materiales.

Uso: python -I herramientas/mallas/proyectar_hoja.py
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
from PIL import Image, ImageFilter


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


def alinear(pos, idx, eje, m):
    """Busqueda global discreta por IoU seguida de refinamiento a un pixel.

    La FFT evalua todas las traslaciones permitidas para cada escala. Se usan
    siluetas rasterizadas, no cajas, para decidir el ajuste. El centroide solo
    establece el origen de la ventana de busqueda.
    """
    alto, ancho = m.shape
    u = pos @ eje
    ymin, ymax = pos[:, 1].min(), pos[:, 1].max()
    ys, xs = np.where(m)
    alto_fig, ancho_fig = np.ptp(ys) + 1, np.ptp(xs) + 1
    escala0 = (alto_fig - 1) / (ymax - ymin)
    centro = np.array([(u.min() + u.max()) / 2, -(ymin + ymax) / 2])
    plano = np.column_stack((u, -pos[:, 1])) - centro
    q0 = plano * escala0 + [ancho / 2, alto / 2]
    _, duenio = rasterizar(q0, np.zeros(len(pos)), idx, ancho, alto)
    my, mx = np.where(duenio >= 0)
    base = np.array([xs.mean(), ys.mean()]) - np.array([mx.mean(), my.mean()]) + [ancho / 2, alto / 2]
    limite = np.array([0.06 * ancho_fig, 0.06 * alto_fig])
    mejor = None
    # Un lienzo con margen evita que el recorte cambie el area durante la busqueda.
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
            _, du = rasterizar(q, np.zeros(len(pos)), idx, w, h)
            sil = du >= 0
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
    q = np.column_stack((u, -pos[:, 1])) * escala + tras
    # Medida final sin recortar la silueta proyectada fuera de la caja de la hoja.
    margen = 150
    _, du = rasterizar(q + margen, np.zeros(len(pos)), idx, ancho + 2 * margen, alto + 2 * margen)
    ref = np.pad(m, margen)
    sil = du >= 0
    iou = (ref & sil).sum() / max((ref | sil).sum(), 1)
    return escala, tras, {"iou": float(iou), "escala_base": float(escala0),
                         "factor_escala": factor, "desplazamiento_px": delta.tolist(),
                         "limites_desplazamiento_px": limite.tolist(),
                         "traslacion_px": tras.tolist(), "centro_inicial_px": base.tolist()}


class Vista:
    def __init__(self, nombre, hoja, pos, idx, carpeta):
        self.nombre = nombre
        self.rgb = np.asarray(hoja.crop(CAJAS[nombre]).convert("RGB"))
        self.m, self.fondo = mascara(self.rgb)
        self.erosion = np.asarray(Image.fromarray(self.m.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(7))) > 0
        self.eje, self.direccion = map(lambda a: np.array(a, float), EJES[nombre])
        self.escala, self.tras, self.info = alinear(pos, idx, self.eje, self.m)
        q = self.proyectar(pos)
        h, w = self.m.shape
        self.super = 2
        self.z, self.du = rasterizar(q * self.super, pos @ self.direccion, idx, w * self.super, h * self.super)
        # Plano de profundidad por triangulo para consultar en la posicion exacta
        # del texel, evitando una tolerancia amplia que acepte otra superficie.
        matrices = np.concatenate((q[idx], np.ones((len(idx), 3, 1))), axis=2)
        validos = np.abs(np.linalg.det(matrices)) > 1e-10
        self.planos = np.zeros((len(idx), 3))
        self.planos[validos] = np.linalg.solve(matrices[validos], (pos @ self.direccion)[idx][validos, :, None])[..., 0]
        self.contribuciones = self.fondo_muestras = self.ocultos = 0
        Image.fromarray(self.m).save(carpeta / f"{nombre}_mascara.png")
        Image.fromarray(self.erosion).save(carpeta / f"{nombre}_mascara_erosion3.png")
        _, du = rasterizar(q, pos @ self.direccion, idx, w, h)
        sil = du >= 0
        sup = np.full((h, w, 3), 40, np.uint8)
        sup[self.m & sil] = [210, 210, 210]
        sup[self.m & ~sil] = [220, 60, 60]
        sup[sil & ~self.m] = [70, 110, 230]
        Image.fromarray(sup).save(carpeta / f"{nombre}_alineacion.png")

    def proyectar(self, puntos):
        return np.column_stack((puntos @ self.eje, -puntos[:, 1])) * self.escala + self.tras

    def muestrear(self, puntos, normales, triangulo):
        q = self.proyectar(puntos)
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
        pix = np.rint(q[ids] * self.super).astype(int)
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
        pesos[ids] = np.maximum(dot[ids], 0) ** 3
        # Auditoria del soporte bilineal contra la mascara sin erosionar.
        mal = ~(self.m[y0, x0] & self.m[y0, x0 + 1] & self.m[y0 + 1, x0] & self.m[y0 + 1, x0 + 1])
        fondo[ids] = mal
        self.contribuciones += len(ids)
        self.fondo_muestras += int(mal.sum())
        return colores, pesos, fondo


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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", type=Path, default=LOTE / "L04_PER01_giro_tripo_mv.glb")
    ap.add_argument("--salida", type=Path, default=LOTE / "L04_PER01_v3_hoja.glb")
    ap.add_argument("--hoja", type=Path, default=HOJA)
    ap.add_argument("--diagnosticos", type=Path, default=LOTE / "parecido/v3_hoja")
    a = ap.parse_args()
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
        print(f"  IoU {v.info['iou']:.4f}, escala {v.info['factor_escala']:.4f}, desplazamiento {v.info['desplazamiento_px']}", flush=True)
    h, w = original.shape[:2]
    tex = original.copy()
    ocupado = np.zeros((h, w), bool)
    pintado = np.zeros((h, w), bool)
    fondo = np.zeros((h, w), bool)
    lado_izq = np.zeros((h, w), bool)
    # glTF usa v=0 en la fila superior y centros UV en (pixel+0.5)/tamano.
    uvs = uv * [w, h] - 0.5
    for t, vertices in enumerate(idx):
        f = fragmentos(uvs[vertices], w, h)
        if f is None:
            continue
        yy, xx, b = f
        puntos = b @ pos[vertices]
        n = b @ normales[vertices]
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        # El sector cuyo eje dominante es -Z queda reservado a la textura Tripo.
        izquierda = (-n[:, 2] > np.abs(n[:, 0])) & (-n[:, 2] > np.abs(n[:, 1]))
        lado_izq[yy, xx] = izquierda
        acum = 0.15 * original[yy, xx].astype(np.float32)
        peso = np.full(len(yy), 0.15, np.float32)
        for vista in vistas:
            ids = np.flatnonzero(~izquierda)
            color, pv, mal = vista.muestrear(puntos[ids], n[ids], t)
            acum[ids] += color * pv[:, None]
            peso[ids] += pv
            fondo[yy[ids], xx[ids]] |= mal & (pv > 0)
        tex[yy, xx] = np.clip(np.rint(acum / peso[:, None]), 0, 255).astype(np.uint8)
        ocupado[yy, xx] = True
        pintado[yy, xx] = peso > 0.15
        if t % 1000 == 0:
            print(f"Horneando triangulo {t}/{len(idx)}", flush=True)
    # Antes del padding, la zona izquierda debe coincidir byte por byte.
    izq_diferentes = int(np.any(tex[lado_izq] != original[lado_izq], axis=1).sum())
    if izq_diferentes:
        raise AssertionError("El lado izquierdo cambio")
    print("Rellenando bordes UV...", flush=True)
    padding = rellenar_bordes(tex, ocupado)
    imagen = Image.fromarray(tex)
    imagen.save(a.diagnosticos / "textura.png")
    Image.fromarray(pintado).save(a.diagnosticos / "texels_hoja.png")
    Image.fromarray(ocupado).save(a.diagnosticos / "texels_superficie.png")
    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    guardar_glb(a.salida, doc, binario, buf.getvalue(), imid)
    # Verifica la conservacion binaria de accessors, nodos, UV y materiales.
    d2, b2 = leer_glb(a.salida)
    d0, b0 = leer_glb(a.entrada)
    assert b2[:len(b0)] == b0
    for clave in ("meshes", "nodes", "accessors", "materials", "textures", "scenes"):
        assert d2[clave] == d0[clave], clave
    assert d2["bufferViews"][:-1] == d0["bufferViews"]
    meta = {"entrada": str(a.entrada), "salida": str(a.salida), "hoja": str(a.hoja),
            "sha256_entrada": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
            "sha256_hoja": hashlib.sha256(a.hoja.read_bytes()).hexdigest(),
            "triangulos": len(idx), "textura_px": [w, h], "geometria_uv_nodos_materiales_identicos": True,
            "texels_superficie": int(ocupado.sum()), "texels_con_hoja": int(pintado.sum()),
            "texels_con_hoja_pct_superficie": float(100 * pintado.sum() / ocupado.sum()),
            "texels_con_hoja_pct_imagen": float(100 * pintado.mean()),
            "texels_fondo": int(fondo.sum()), "texels_fondo_pct_pintados": float(100 * fondo.sum() / max(pintado.sum(), 1)),
            "muestras_fondo": sum(v.fondo_muestras for v in vistas),
            "texels_izquierda_conservados": int(lado_izq.sum()), "texels_izquierda_diferentes": izq_diferentes,
            "criterio_izquierda": "normal interpolada con eje dominante -Z; no hay proyeccion desde -Z",
            "padding_texels": padding, "peso_original": 0.15, "erosion_px": 3,
            "profundidad_supermuestreo": 2, "profundidad_tolerancia_m": 2e-5,
            "vistas": {v.nombre: {**v.info, "muestras_aceptadas": v.contribuciones,
                                    "muestras_sobre_fondo": v.fondo_muestras,
                                    "muestras_ocultas_rechazadas": v.ocultos} for v in vistas},
            "segundos": round(time.monotonic() - inicio, 1)}
    (a.diagnosticos / "horneado.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
