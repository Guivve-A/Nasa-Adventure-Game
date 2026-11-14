"""Enfoque C: repinta PER-01 desde la hoja con registro propio de la cara.

Parte de proyectar_hoja.py (v3) y cambia tres cosas:
  1) la cara: se registra la cara de la hoja contra un render frontal de la malla v2
     (que trae los ojos de Tripo) con una similitud (escala, giro, traslacion) que
     maximiza la correlacion normalizada de la luminancia. La cara de la hoja se
     proyecta con esa transformacion sobre los texels que miran al frente (n.d > 0,2),
     con peso total (original 0) y borde fundido de unos 4 px;
  2) el cuerpo: como v3, pero con pesos max(0, n.d)^1 y 0,01 de la original donde
     alguna vista ve el texel;
  3) lo que no se proyecta: se ajusta en Lab (media y desviacion) por grupos de color
     de la textura original, con estadisticas aprendidas de lo proyectado.

Uso: python -I herramientas/mallas/proyectar_hoja_C.py [--cara-registro ncc|identidad]
Solo requiere numpy y Pillow. No modifica geometria, UV ni materiales.
"""
import argparse
import hashlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import proyectar_hoja as ph  # noqa: E402

# Cara en coordenadas del recorte frontal de la hoja (caja 200,10,720,923).
CARA_CENTRO = (268.0, 192.0)
CARA_SEMIEJES = (92.0, 84.0)       # superelipse p=4: x 176..360, y 108..276
PLANTILLA_SEMIEJES = (80.0, 75.0)  # elipse para la correlacion: cejas, ojos, nariz, boca
CARA_PROD_MIN = 0.2                # n.d minimo para la cara
CARA_RAMPA = 0.1                   # rampa de n.d entre 0,2 y 0,3
PESO_ORIGINAL = 0.01
GRUPOS = 10


# ---------- color ----------
M_XYZ = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
BLANCO = np.array([0.95047, 1.0, 1.08883])


def a_lab(rgb):
    c = np.asarray(rgb, np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    t = (lin @ M_XYZ.T) / BLANCO
    f = np.where(t > 216 / 24389, np.cbrt(t), (24389 / 27 * t + 16) / 116)
    return np.stack((116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])), -1)


def de_lab(lab):
    lab = np.asarray(lab, np.float64)
    fy = (lab[..., 0] + 16) / 116
    f = np.stack((fy + lab[..., 1] / 500, fy, fy - lab[..., 2] / 200), -1)
    t = np.where(f ** 3 > 216 / 24389, f ** 3, (116 * f - 16) / (24389 / 27))
    lin = (t * BLANCO) @ np.linalg.inv(M_XYZ).T
    lin = np.clip(lin, 0, 1)
    c = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)
    return c * 255.0


def bilineal(img, x, y):
    """Muestreo bilineal; x, y dentro de [0, ancho-1) x [0, alto-1)."""
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    if img.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]
    a = img[y0, x0].astype(np.float32)
    b = img[y0, x0 + 1].astype(np.float32)
    c = img[y0 + 1, x0].astype(np.float32)
    d = img[y0 + 1, x0 + 1].astype(np.float32)
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


# ---------- vistas ----------
class VistaC(ph.Vista):
    def visible(self, puntos, q, triangulo):
        """Visibilidad por bufer de profundidad, como v3, en la posicion proyectada q."""
        pix = np.rint(q * self.super).astype(int)
        du = self.du[pix[:, 1], pix[:, 0]]
        zreal = puntos @ self.direccion
        dm = np.maximum(du, 0)
        zvis = (self.planos[dm, :2] * q).sum(1) + self.planos[dm, 2]
        return (du >= 0) & ((du == triangulo) | (np.abs(zreal - zvis) <= 2e-5))

    def muestrear(self, puntos, normales, triangulo, potencia=1):
        q = self.proyectar(puntos)
        x, y = q.T
        h, w = self.m.shape
        dot = normales @ self.direccion
        valido = (x >= 0) & (x < w - 1) & (y >= 0) & (y < h - 1) & (dot > 0)
        ids = np.flatnonzero(valido)
        pesos = np.zeros(len(puntos), np.float32)
        colores = np.zeros((len(puntos), 3), np.float32)
        if not len(ids):
            return colores, pesos
        x0, y0 = np.floor(q[ids]).astype(int).T
        seguro = (self.erosion[y0, x0] & self.erosion[y0 + 1, x0]
                  & self.erosion[y0, x0 + 1] & self.erosion[y0 + 1, x0 + 1])
        ids = ids[seguro]
        if not len(ids):
            return colores, pesos
        vis = self.visible(puntos[ids], q[ids], triangulo)
        self.ocultos += int((~vis).sum())
        ids = ids[vis]
        if not len(ids):
            return colores, pesos
        colores[ids] = bilineal(self.rgb, q[ids, 0], q[ids, 1])
        pesos[ids] = np.maximum(dot[ids], 0) ** potencia
        self.contribuciones += len(ids)
        return colores, pesos


def render_marco(vista, uv, idx, original, caja):
    """Render sin luz de la malla en el marco del recorte frontal (a vista.super px por px).

    Usa el bufer de propietarios de la vista: cada pixel toma el UV interpolado
    de su triangulo visible y muestrea la textura original (bilineal).
    """
    s = vista.super
    x0, y0, x1, y1 = caja
    du = vista.du[y0 * s:y1 * s, x0 * s:x1 * s]
    yy, xx = np.nonzero(du >= 0)
    t = du[yy, xx]
    q = vista.proyectar_cache * s
    tri = q[idx[t]]
    px = xx + x0 * s
    py = yy + y0 * s
    a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
    den = (b[:, 1] - c[:, 1]) * (a[:, 0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (a[:, 1] - c[:, 1])
    den = np.where(np.abs(den) < 1e-12, 1e-12, den)
    l1 = ((b[:, 1] - c[:, 1]) * (px - c[:, 0]) + (c[:, 0] - b[:, 0]) * (py - c[:, 1])) / den
    l2 = ((c[:, 1] - a[:, 1]) * (px - c[:, 0]) + (a[:, 0] - c[:, 0]) * (py - c[:, 1])) / den
    l3 = 1 - l1 - l2
    uvp = l1[:, None] * uv[idx[t, 0]] + l2[:, None] * uv[idx[t, 1]] + l3[:, None] * uv[idx[t, 2]]
    th, tw = original.shape[:2]
    p = np.clip(uvp * [tw, th] - 0.5, 0, [tw - 1.001, th - 1.001])
    img = np.full(du.shape + (3,), 205.0, np.float32)
    img[yy, xx] = bilineal(original, p[:, 0], p[:, 1])
    return img, du >= 0


# ---------- registro de la cara ----------
def luminancia(rgb):
    return rgb.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)


def suavizar(lum, sigma):
    """Desenfoque gaussiano separable en numpy (Pillow no lo aplica al modo F)."""
    r = max(1, int(np.ceil(3 * sigma)))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    p = np.pad(lum.astype(np.float32), r, mode="edge")
    p = sum(k[i] * p[:, i:i + p.shape[1] - 2 * r] for i in range(2 * r + 1))
    p = sum(k[i] * p[i:i + p.shape[0] - 2 * r] for i in range(2 * r + 1))
    return p.astype(np.float32)


_CACHE = {}


def alinear_con_cache(pos, idx, eje, m):
    """Envuelve ph.alinear: reutiliza el resultado guardado si la entrada y la hoja no cambian."""
    clave = ",".join(str(int(v)) for v in eje)
    if clave in _CACHE.get("vistas", {}):
        d = _CACHE["vistas"][clave]
        return d["escala"], np.array(d["tras"]), d["info"]
    escala, tras, info = _alinear_original(pos, idx, eje, m)
    _CACHE.setdefault("vistas", {})[clave] = {"escala": float(escala), "tras": tras.tolist(), "info": info}
    return escala, tras, info


_alinear_original = ph.alinear
ph.alinear = alinear_con_cache


def matriz(s, ang):
    c, n = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    return s * np.array([[c, -n], [n, c]])


def registrar_cara(hoja_rgb, render, marco_caja, sup):
    """Similitud T: hoja -> marco del render. Maximiza la NCC de la luminancia.

    T(p) = c + s R(ang) (p - c) + t, con c el centro de la cara.
    Busqueda en rejilla gruesa y luego fina; devuelve parametros y NCC.
    """
    cx, cy = CARA_CENTRO
    ax, by = PLANTILLA_SEMIEJES
    lh = suavizar(luminancia(hoja_rgb), 0.8)
    lr = suavizar(luminancia(render), 0.8 * sup)
    yy, xx = np.mgrid[int(cy - by):int(cy + by) + 1, int(cx - ax):int(cx + ax) + 1]
    dentro = ((xx - cx) / ax) ** 2 + ((yy - cy) / by) ** 2 <= 1
    pts = np.column_stack((xx[dentro], yy[dentro])).astype(np.float64)
    val = lh[pts[:, 1].astype(int), pts[:, 0].astype(int)].astype(np.float64)
    ox, oy = marco_caja[0], marco_caja[1]
    hr, wr = lr.shape
    c = np.array([cx, cy])

    def ncc_lote(p, v, s, ang, ts):
        base = (p - c) @ matriz(s, ang).T + c
        coords = base[None] + ts[:, None, :]
        X = (coords[..., 0] - ox) * sup
        Y = (coords[..., 1] - oy) * sup
        fuera = (X < 0) | (X >= wr - 1) | (Y < 0) | (Y >= hr - 1)
        X = np.clip(X, 0, wr - 1.001)
        Y = np.clip(Y, 0, hr - 1.001)
        r = bilineal(lr, X.ravel(), Y.ravel()).reshape(X.shape).astype(np.float64)
        a = v - v.mean()
        r = r - r.mean(1, keepdims=True)
        n = (r * a[None]).sum(1) / np.sqrt((r * r).sum(1) * (a * a).sum() + 1e-9)
        n[fuera.any(1)] = -1
        return n

    def buscar(p, v, escalas, angulos, ts):
        mejor = (-2, None)
        for s in escalas:
            for ang in angulos:
                n = ncc_lote(p, v, s, ang, ts)
                k = int(np.argmax(n))
                if n[k] > mejor[0]:
                    mejor = (float(n[k]), (float(s), float(ang), ts[k].tolist()))
        return mejor

    sub = slice(None, None, 3)
    rej = np.arange(-16, 16.01, 2)
    ts = np.array([(tx, ty) for ty in rej for tx in rej], float)
    g = buscar(pts[sub], val[sub], np.arange(0.88, 1.1201, 0.02), np.arange(-6, 6.01, 1.5), ts)
    s0, a0, t0 = g[1]
    rej = np.arange(-2, 2.01, 0.5)
    ts = np.array([(t0[0] + tx, t0[1] + ty) for ty in rej for tx in rej], float)
    f = buscar(pts, val, np.arange(s0 - 0.02, s0 + 0.0201, 0.005), np.arange(a0 - 1.5, a0 + 1.51, 0.5), ts)
    identidad = float(ncc_lote(pts, val, 1.0, 0.0, np.zeros((1, 2)))[0])
    s, ang, t = f[1]
    return {"escala": s, "giro_grados": ang, "traslacion_px": t, "centro_px": [cx, cy],
            "ncc": f[0], "ncc_gruesa": g[0], "ncc_identidad": identidad,
            "pixeles_plantilla": int(len(pts))}


def inversa(reg):
    """Devuelve la funcion marco -> hoja (T^-1)."""
    c = np.array(reg["centro_px"])
    mi = np.linalg.inv(matriz(reg["escala"], reg["giro_grados"]))
    t = np.array(reg["traslacion_px"])
    return lambda q: (q - c - t) @ mi.T + c


def mascara_cara(forma):
    h, w = forma
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = CARA_CENTRO
    a, b = CARA_SEMIEJES
    m = (np.abs((xx - cx) / a) ** 4 + np.abs((yy - cy) / b) ** 4) <= 1
    # Borde fundido: erosion de 2 px y caja de 5 px -> rampa de unos 4 px.
    im = Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(5))
    im = im.filter(ImageFilter.BoxBlur(2))
    return np.asarray(im, np.float32) / 255.0


def muestra_cara(vista, alfa_hoja, inv, puntos, normales, triangulo):
    dot = normales @ vista.direccion
    alfa = np.zeros(len(puntos), np.float32)
    color = np.zeros((len(puntos), 3), np.float32)
    ids = np.flatnonzero(dot > CARA_PROD_MIN)
    if not len(ids):
        return color, alfa
    q = vista.proyectar(puntos[ids])
    h, w = vista.m.shape
    dentro = (q[:, 0] >= 0) & (q[:, 0] < w - 1) & (q[:, 1] >= 0) & (q[:, 1] < h - 1)
    ids, q = ids[dentro], q[dentro]
    if not len(ids):
        return color, alfa
    p = inv(q)
    dentro = (p[:, 0] >= 0) & (p[:, 0] < w - 1) & (p[:, 1] >= 0) & (p[:, 1] < h - 1)
    ids, q, p = ids[dentro], q[dentro], p[dentro]
    if not len(ids):
        return color, alfa
    a = bilineal(alfa_hoja, p[:, 0], p[:, 1])
    usar = a > 0
    ids, q, p, a = ids[usar], q[usar], p[usar], a[usar]
    if not len(ids):
        return color, alfa
    vis = vista.visible(puntos[ids], q, triangulo)
    ids, p, a = ids[vis], p[vis], a[vis]
    rampa = np.clip((dot[ids] - CARA_PROD_MIN) / CARA_RAMPA, 0, 1)
    alfa[ids] = a * rampa
    color[ids] = bilineal(vista.rgb, p[:, 0], p[:, 1])
    return color, alfa


# ---------- ajuste de color ----------
def kmeans(x, k, iters=20, semilla=7):
    rng = np.random.default_rng(semilla)
    cen = x[rng.choice(len(x), k, replace=False)]
    for _ in range(iters):
        g = asignar(x, cen)
        for j in range(k):
            if (g == j).any():
                cen[j] = x[g == j].mean(0)
    return cen


def asignar(x, cen, lote=1_000_000):
    out = np.empty(len(x), np.int16)
    for i in range(0, len(x), lote):
        d = ((x[i:i + lote, None, :] - cen[None]) ** 2).sum(-1)
        out[i:i + lote] = d.argmin(1)
    return out


def ajuste_color(orig_lab, nuevo_lab, grupo_todos, proyectado, k):
    """Por grupo de color: (o - mu_o) / sd_o * sd_n + mu_n, aprendido en lo proyectado."""
    salida = orig_lab.copy()
    info = []
    go = orig_lab[proyectado]
    gn = nuevo_lab[proyectado]
    gp = grupo_todos[proyectado]
    mu_o_g, sd_o_g = go.mean(0), go.std(0) + 1e-3
    mu_n_g, sd_n_g = gn.mean(0), gn.std(0) + 1e-3
    corr_g = ((go - mu_o_g) * (gn - mu_n_g)).mean(0) / (sd_o_g * sd_n_g)
    for j in range(k):
        sel = gp == j
        if sel.sum() >= 2000:
            o, nn = go[sel], gn[sel]
            mu_o, sd_o = o.mean(0), o.std(0) + 1e-3
            mu_n, sd_n = nn.mean(0), nn.std(0) + 1e-3
            corr = ((o - mu_o) * (nn - mu_n)).mean(0) / (sd_o * sd_n)
        else:
            mu_o, sd_o, mu_n, sd_n, corr = mu_o_g, sd_o_g, mu_n_g, sd_n_g, corr_g
        # Dentro de un grupo, gran parte de sd_n es ruido de registro (otro material
        # cae en el mismo texel). Solo se usa la desviacion explicada (corr * sd_n),
        # que equivale a la pendiente de la regresion, acotada a [0,5; 1,5].
        r = np.clip(corr * sd_n / sd_o, 0.5, 1.5)
        todos = grupo_todos == j
        salida[todos] = (orig_lab[todos] - mu_o) * r + mu_n
        info.append({"grupo": j, "texels_proyectados": int(sel.sum()), "texels_total": int(todos.sum()),
                     "media_original_lab": np.round(mu_o, 2).tolist(), "media_nueva_lab": np.round(mu_n, 2).tolist(),
                     "razon_desviacion_bruta": np.round(sd_n / sd_o, 3).tolist(),
                     "correlacion": np.round(corr, 3).tolist(),
                     "razon_aplicada": np.round(r, 3).tolist()})
    return salida, info


# ---------- diagnosticos ----------
def lamina_registro(hoja_rgb, render, marco, sup, reg, inv, ruta):
    x0, y0, x1, y1 = marco
    ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float64)
    pr = np.column_stack((xs.ravel(), ys.ravel()))
    # Hoja en el marco del render con T y sin T
    h, w = hoja_rgb.shape[:2]

    def llevar(fn):
        p = fn(pr)
        p[:, 0] = np.clip(p[:, 0], 0, w - 1.001)
        p[:, 1] = np.clip(p[:, 1], 0, h - 1.001)
        return bilineal(hoja_rgb, p[:, 0], p[:, 1]).reshape(ys.shape + (3,))

    con_t = llevar(inv)
    sin_t = llevar(lambda q: q)
    ren = render[::sup, ::sup][:ys.shape[0], :ys.shape[1]]
    ajedrez = ((np.floor(ys / 12) + np.floor(xs / 12)) % 2 == 0)[..., None]
    paneles = [sin_t, ren, con_t, np.where(ajedrez, con_t, ren),
               np.abs(sin_t - ren), np.abs(con_t - ren)]
    tira = np.concatenate([np.clip(p, 0, 255) for p in paneles], 1).astype(np.uint8)
    Image.fromarray(tira).resize((tira.shape[1] * 2, tira.shape[0] * 2), Image.LANCZOS).save(ruta)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path, default=ph.LOTE / "L04_PER01_giro_tripo_mv.glb")
    ap.add_argument("--salida", type=Path, default=ph.LOTE / "L04_PER01_v4C.glb")
    ap.add_argument("--hoja", type=Path, default=ph.HOJA)
    ap.add_argument("--diagnosticos", type=Path, default=ph.LOTE / "parecido/v4C")
    ap.add_argument("--cara-registro", choices=("ncc", "identidad"), default="ncc")
    ap.add_argument("--potencia", type=float, default=1.0, help="exponente de n.d en el cuerpo (v3 usaba 3)")
    a = ap.parse_args()
    if a.entrada.resolve() == a.salida.resolve():
        raise ValueError("La salida no puede sobrescribir la entrada")
    inicio = time.monotonic()
    a.diagnosticos.mkdir(parents=True, exist_ok=True)
    doc, binario = ph.leer_glb(a.entrada)
    pos, uv, idx, normales, original, imid = ph.geometria(doc, binario)
    hoja = Image.open(a.hoja).convert("RGB")
    # Cache de la alineacion global (la misma busqueda de v3), valida solo con los mismos archivos.
    firma = hashlib.sha256(a.entrada.read_bytes() + a.hoja.read_bytes()).hexdigest()
    ruta_cache = ph.LOTE / "parecido/v4C/alineacion_cache.json"
    if ruta_cache.exists():
        c = json.loads(ruta_cache.read_text(encoding="utf-8"))
        if c.get("firma") == firma:
            _CACHE.update(c)
    _CACHE["firma"] = firma
    vistas = {}
    for nombre in ph.CAJAS:
        print(f"Alineando {nombre}...", flush=True)
        v = VistaC(nombre, hoja, pos, idx, a.diagnosticos)
        v.proyectar_cache = v.proyectar(pos)
        vistas[nombre] = v
        print(f"  IoU {v.info['iou']:.4f}, escala {v.info['factor_escala']:.4f}", flush=True)
    ruta_cache.write_text(json.dumps(_CACHE, indent=1), encoding="utf-8")
    fr = vistas["frente"]

    # 1) Registro de la cara contra el render frontal de la v2.
    marco = (120, 60, 420, 330)
    render, _ = render_marco(fr, uv, idx, original, marco)
    if a.cara_registro == "ncc":
        reg = registrar_cara(fr.rgb, render, marco, fr.super)
    else:
        reg = {"escala": 1.0, "giro_grados": 0.0, "traslacion_px": [0.0, 0.0],
               "centro_px": list(CARA_CENTRO), "ncc": None}
    reg["modo"] = a.cara_registro
    print("Registro de la cara:", json.dumps(reg), flush=True)
    inv = inversa(reg)
    alfa_hoja = mascara_cara(fr.m.shape) * fr.erosion
    Image.fromarray(np.clip(render, 0, 255).astype(np.uint8)).save(a.diagnosticos / "v2_frente_marco.png")
    Image.fromarray((alfa_hoja * 255).astype(np.uint8)).save(a.diagnosticos / "cara_mascara_hoja.png")
    lamina_registro(fr.rgb, render, marco, fr.super, reg, inv, a.diagnosticos / "cara_registro.png")

    # Pasada 1: acumula la hoja por texel.
    h, w = original.shape[:2]
    acum = np.zeros((h, w, 3), np.float32)
    peso = np.zeros((h, w), np.float32)
    cara = np.zeros((h, w, 3), np.float32)
    alfa = np.zeros((h, w), np.float32)
    ocupado = np.zeros((h, w), bool)
    lado_izq = np.zeros((h, w), bool)
    uvs = uv * [w, h] - 0.5
    for t, vertices in enumerate(idx):
        f = ph.fragmentos(uvs[vertices], w, h)
        if f is None:
            continue
        yy, xx, b = f
        puntos = b @ pos[vertices]
        n = b @ normales[vertices]
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        izquierda = (-n[:, 2] > np.abs(n[:, 0])) & (-n[:, 2] > np.abs(n[:, 1]))
        lado_izq[yy, xx] = izquierda
        ocupado[yy, xx] = True
        ids = np.flatnonzero(~izquierda)
        if len(ids):
            ac = np.zeros((len(ids), 3), np.float32)
            pe = np.zeros(len(ids), np.float32)
            for v in vistas.values():
                c, pv = v.muestrear(puntos[ids], n[ids], t, potencia=a.potencia)
                ac += c * pv[:, None]
                pe += pv
            acum[yy[ids], xx[ids]] = ac
            peso[yy[ids], xx[ids]] = pe
        c, al = muestra_cara(fr, alfa_hoja, inv, puntos, n, t)
        cara[yy, xx] = c
        alfa[yy, xx] = al
        if t % 1000 == 0:
            print(f"Horneando triangulo {t}/{len(idx)}", flush=True)

    # Pasada 2: color proyectado, ajuste Lab de lo no proyectado y mezcla final.
    print("Ajuste de color...", flush=True)
    sup_idx = np.flatnonzero(ocupado.ravel())
    o_rgb = original.reshape(-1, 3)[sup_idx].astype(np.float32)
    pe = peso.ravel()[sup_idx]
    al = alfa.ravel()[sup_idx]
    hojac = acum.reshape(-1, 3)[sup_idx] / np.maximum(pe, 1e-6)[:, None]
    carac = cara.reshape(-1, 3)[sup_idx]
    # Color de pura hoja (sin original): cara con alfa sobre la mezcla de vistas.
    pura = np.where((pe > 0)[:, None], hojac, carac)
    pura = al[:, None] * carac + (1 - al[:, None]) * pura
    o_lab = a_lab(o_rgb).astype(np.float32)
    rng = np.random.default_rng(3)
    muestra = o_lab[rng.choice(len(o_lab), min(200_000, len(o_lab)), replace=False)]
    cen = kmeans(muestra.copy(), GRUPOS)
    grupo = asignar(o_lab, cen)
    proyectado = (pe >= 0.25) | (al >= 0.5)
    ajus_lab, info_grupos = ajuste_color(o_lab, a_lab(pura).astype(np.float32), grupo, proyectado, GRUPOS)
    ajus = de_lab(ajus_lab).astype(np.float32)
    visto = (pe > 0) | (al > 0)
    mezcla = (acum.reshape(-1, 3)[sup_idx] + PESO_ORIGINAL * ajus) / (pe + PESO_ORIGINAL)[:, None]
    final = np.where(visto[:, None], mezcla, ajus)
    final = al[:, None] * carac + (1 - al[:, None]) * final
    tex = original.copy().reshape(-1, 3)
    tex[sup_idx] = np.clip(np.rint(final), 0, 255).astype(np.uint8)
    tex = tex.reshape(h, w, 3)
    print("Rellenando bordes UV...", flush=True)
    padding = ph.rellenar_bordes(tex, ocupado)
    imagen = Image.fromarray(tex)
    imagen.save(a.diagnosticos / "textura.png")
    m = np.zeros(h * w, bool)
    m[sup_idx[visto]] = True
    Image.fromarray(m.reshape(h, w)).save(a.diagnosticos / "texels_hoja.png")
    m[:] = False
    m[sup_idx[al > 0]] = True
    Image.fromarray(m.reshape(h, w)).save(a.diagnosticos / "texels_cara.png")
    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    ph.guardar_glb(a.salida, doc, binario, buf.getvalue(), imid)
    d2, b2 = ph.leer_glb(a.salida)
    d0, b0 = ph.leer_glb(a.entrada)
    assert b2[:len(b0)] == b0
    for clave in ("meshes", "nodes", "accessors", "materials", "textures", "scenes"):
        assert d2[clave] == d0[clave], clave
    # Cambio medio en Lab de lo no visto (ajuste del paso 3).
    no_visto = ~visto
    cambio = float(np.linalg.norm(ajus_lab[no_visto] - o_lab[no_visto], axis=1).mean()) if no_visto.any() else 0.0
    meta = {"entrada": str(a.entrada), "salida": str(a.salida), "hoja": str(a.hoja),
            "sha256_entrada": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
            "sha256_hoja": hashlib.sha256(a.hoja.read_bytes()).hexdigest(),
            "triangulos": len(idx), "textura_px": [w, h],
            "registro_cara": reg, "cara_superelipse": {"centro": CARA_CENTRO, "semiejes": CARA_SEMIEJES},
            "texels_superficie": int(len(sup_idx)),
            "texels_vistos": int(visto.sum()), "texels_vistos_pct": float(100 * visto.mean()),
            "texels_proyectados_fuerte_pct": float(100 * proyectado.mean()),
            "texels_cara": int((al > 0).sum()), "texels_cara_alfa1": int((al >= 0.999).sum()),
            "texels_izquierda_reservados": int(lado_izq.sum()),
            "ajuste_no_visto_dE76_medio": cambio, "grupos": info_grupos,
            "peso_original": PESO_ORIGINAL, "potencia_n_d": a.potencia, "padding_texels": padding,
            "vistas": {k: {**v.info, "muestras_aceptadas": v.contribuciones,
                           "muestras_ocultas_rechazadas": v.ocultos} for k, v in vistas.items()},
            "segundos": round(time.monotonic() - inicio, 1)}
    (a.diagnosticos / "horneado.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("registro_cara", "texels_vistos_pct", "texels_cara",
                                             "ajuste_no_visto_dE76_medio", "segundos")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
