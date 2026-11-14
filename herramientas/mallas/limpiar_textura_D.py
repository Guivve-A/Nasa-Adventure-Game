"""Estrategia D: limpia la textura proyectada de PER-01 (v5C) sin tocar geometria ni UV.

Por texel (posicion y normal en 3D, rasterizando las UV):
  1) fiabilidad r en [0, 1]:
     - g = max(n.d) sobre las tres vistas proyectadas (+X, -X, +Z); r cae a 0 si g < 0,35
       (rampa 0,30..0,42);
     - costado izquierdo de la cabeza (-Z, y > 0,15): r = 0;
     - cadera, gluteo y muslo derechos, donde quedo pintado el bolso de la hoja: r = 0 de
       frente y de espalda; en el costado (+Z) solo las herramientas (el cuero queda, porque
       la hoja dibuja el bolso ahi en el perfil). Se protege la correa pintada del frente;
     - naranja de canto en el pelo (borde de luz de otra vista): r = 0, salvo en la banda
       de 12 mm junto a la silueta de frente y de perfil, donde la hoja si lo pinta;
     - manchas oscuras en la piel del cuerpo y de los costados del cuello: r = 0;
     - texels que la proyeccion de C no alcanzo (texels_hoja.png de v5C = falso): r = 0.
       Son los puntos sueltos en las aristas (fallos de visibilidad), que C relleno con
       el color de Tripo ajustado en Lab y forman las lineas punteadas.
  2) relleno de lo no fiable, propagado sobre la superficie en 3D (rejilla de voxeles con
     empujar-tirar, que cruza costuras UV porque usa la posicion de mundo):
     - local: color fiable de los vecinos, sin zonas; sirve para huecos chicos (los puntos
       sueltos se rellenan antes con sus vecinos fiables en UV, dentro de la isla);
     - por zona: zonas de color de la textura original de Tripo (k-medias en Lab mas un
       indice de pelo) y una zona semantica de pelo (sin orejas, cara ni cuello); cada zona se rellena solo con texels fiables de la misma zona
       (y con color de la hoja coherente con esa zona); la forma sale de la luminancia de
       la textura original de Tripo (detalle de alta frecuencia), con el color de la zona.
     La mezcla entre los dos depende de cuanta superficie fiable hay alrededor.
  3) reflejos naranjas del pelo (y > 0,15): por defecto se mezclan un 30 % hacia el color
     medio del pelo (baja el brillo y mantiene el tono rojizo); --modo-reflejos hsv hace el
     -30 % literal de saturacion y brillo, que deja los reflejos verde oliva.
  4) brillo cuadrado del ojo derecho del personaje (+Z): se repinta redondo, con el radio
     del brillo del otro ojo; lo que sobra se pinta con el color del iris.
  5) dilatacion de las islas UV 16 px desde su interior (borde de 1 px descartado salvo en
     islas muy finas).

Uso: python -I herramientas/mallas/limpiar_textura_D.py [--mascaras]
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
import proyectar_hoja_C as pc  # noqa: E402

LOTE = ph.LOTE
# Voxeles (m)
VOX_LOCAL = 0.0025
VOX_ZONA = 0.005
VOX_DETALLE = 0.010
VOX_PELO = 0.006
ZONAS = 12
SIGMA_ZONA = 7.0       # suavidad de la pertenencia a zona (unidades de Lab)
PESO_PELO = 25.0       # peso del indice de pelo en el k-medias
GANANCIA_DETALLE = 1.0
LIMITE_DETALLE = 22.0  # tope del detalle de luminancia (L*)
DILATACION = 16


def suave(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ---------- rasterizado de texels ----------
def texels(pos, uv, idx, nor, w, h):
    """Devuelve indices lineales de los texels cubiertos, su posicion y su normal en 3D."""
    P = np.zeros((h * w, 3), np.float32)
    N = np.zeros((h * w, 3), np.float32)
    ocupado = np.zeros(h * w, bool)
    uvs = uv * [w, h] - 0.5
    for vertices in idx:
        f = ph.fragmentos(uvs[vertices], w, h)
        if f is None:
            continue
        yy, xx, b = f
        li = yy * w + xx
        P[li] = b @ pos[vertices]
        n = b @ nor[vertices]
        N[li] = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        ocupado[li] = True
    sup = np.flatnonzero(ocupado)
    return sup, P[sup], N[sup]


# ---------- rejilla 3D con empujar-tirar ----------
class Rejilla:
    def __init__(self, P, vox, margen=2):
        self.vox = vox
        self.o = P.min(0) - margen * vox
        self.dims = tuple(int(v) for v in np.ceil((P.max(0) + margen * vox - self.o) / vox))

    def indice(self, P):
        i = np.clip(((P - self.o) / self.vox).astype(np.int64), 0, np.array(self.dims) - 1)
        return (i[:, 0] * self.dims[1] + i[:, 1]) * self.dims[2] + i[:, 2]

    def acumular(self, P, valores, pesos):
        """Suma valores*pesos y pesos por voxel; valores (n, c)."""
        k = self.indice(P)
        n = int(np.prod(self.dims))
        S = np.stack([np.bincount(k, valores[:, c] * pesos, n) for c in range(valores.shape[1])], -1)
        W = np.bincount(k, pesos, n)
        return S.reshape(self.dims + (-1,)).astype(np.float32), W.reshape(self.dims).astype(np.float32)

    def muestrear(self, campo, P, escala=1):
        """Trilineal sobre los centros de voxel de un campo de tamano dims/escala."""
        vox = self.vox * escala
        f = (P - self.o) / vox - 0.5
        forma = np.array(campo.shape[:3])
        f = np.clip(f, 0, forma - 1.0001)
        i0 = np.floor(f).astype(np.int64)
        t = (f - i0).astype(np.float32)
        i1 = np.minimum(i0 + 1, forma - 1)
        sal = 0
        for dx in (0, 1):
            ix = i1[:, 0] if dx else i0[:, 0]
            wx = t[:, 0] if dx else 1 - t[:, 0]
            for dy in (0, 1):
                iy = i1[:, 1] if dy else i0[:, 1]
                wy = t[:, 1] if dy else 1 - t[:, 1]
                for dz in (0, 1):
                    iz = i1[:, 2] if dz else i0[:, 2]
                    wz = t[:, 2] if dz else 1 - t[:, 2]
                    pw = wx * wy * wz
                    v = campo[ix, iy, iz]
                    sal = sal + (v * pw[:, None] if v.ndim == 2 else v * pw)
        return sal


def reducir(A):
    """Suma bloques de 2x2x2 (rellena con ceros los ejes impares)."""
    pad = [(0, s % 2) for s in A.shape[:3]] + [(0, 0)] * (A.ndim - 3)
    A = np.pad(A, pad)
    X, Y, Z = (s // 2 for s in A.shape[:3])
    return A.reshape((X, 2, Y, 2, Z, 2) + A.shape[3:]).sum((1, 3, 5))


def ampliar(A, forma):
    """Interpolacion lineal x2 en cada eje (centros de voxel) y recorte a forma."""
    for eje in range(3):
        n = A.shape[eje]
        a = np.moveaxis(A, eje, 0)
        ant = np.concatenate((a[:1], a[:-1]), 0)
        sig = np.concatenate((a[1:], a[-1:]), 0)
        out = np.empty((2 * n,) + a.shape[1:], A.dtype)
        out[0::2] = 0.75 * a + 0.25 * ant
        out[1::2] = 0.75 * a + 0.25 * sig
        A = np.moveaxis(out[:forma[eje]], 0, eje)
    return A


def empujar_tirar(S, W, wref):
    """Rellena los voxeles vacios con el promedio de los datos mas cercanos (multiescala).

    S: (X, Y, Z, C) sumas ponderadas; W: (X, Y, Z) pesos. wref: peso que da confianza
    total en el nivel 0 (en el nivel l se usa wref * 4**l, porque es una superficie).
    Devuelve el campo de color y la piramide de pesos.
    """
    niveles = [(S, W)]
    while max(niveles[-1][1].shape) > 2:
        s, w = niveles[-1]
        niveles.append((reducir(s), reducir(w)))
    s, w = niveles[-1]
    C = s / np.maximum(w, 1e-9)[..., None]
    if (w <= 0).all():
        return np.zeros_like(S), [n[1] for n in niveles]
    for l in range(len(niveles) - 2, -1, -1):
        s, w = niveles[l]
        arriba = ampliar(C, s.shape[:3])
        a = np.clip(w / (wref * 4 ** l), 0, 1)[..., None]
        C = a * (s / np.maximum(w, 1e-9)[..., None]) + (1 - a) * arriba
    return C.astype(np.float32), [n[1] for n in niveles]


def caja3(A, r=1):
    """Suma en una caja de (2r+1)^3 voxeles, separable."""
    for eje in range(3):
        a = np.moveaxis(A, eje, 0)
        p = np.pad(a, [(r, r)] + [(0, 0)] * (a.ndim - 1))
        a = sum(p[i:i + a.shape[0]] for i in range(2 * r + 1))
        A = np.moveaxis(a, 0, eje)
    return A


# ---------- mascaras ----------
def fiabilidad(P, N, visto, lab5, bolso=True):
    x, y, z = P.T
    nx, ny, nz = N.T
    g = np.maximum(np.maximum(nx, -nx), nz)
    r_g = suave(0.30, 0.42, g)
    # Costado izquierdo de la cabeza: normal hacia -Z, salvo lo que mira bien al frente.
    m_izq = suave(0.13, 0.17, y) * suave(0.25, 0.45, -nz) * (1 - suave(0.5, 0.7, nx))
    # Bolso pintado: cadera, gluteo y muslo derechos (+Z), sin la mano ni el brazo.
    m_bolso = (suave(-0.198, -0.186, y) * (1 - suave(-0.006, 0.004, y))
               * suave(0.012, 0.028, z) * (1 - suave(0.128, 0.142, z)))
    # Correa pintada en el frente: banda diagonal z = 0,037 - 0,5 y, 14 mm de semiancho.
    correa = (suave(0.25, 0.45, nx) * (1 - suave(0.012, 0.016, np.abs(z - (0.037 - 0.5 * y))))
              * suave(-0.082, -0.072, y))
    m_bolso = m_bolso * (1 - correa) * float(bolso)
    # En el costado (+Z) solo se borran las herramientas (claras y saturadas, o gris metal);
    # el cuero del bolso queda como sombra marron: la hoja lo dibuja ahi en el perfil.
    L, croma = lab5[:, 0], np.hypot(lab5[:, 1], lab5[:, 2])
    herramienta = np.maximum(suave(30, 45, croma) * suave(50, 62, L),
                             suave(55, 70, L) * (1 - suave(10, 20, croma)))
    lado = suave(0.45, 0.65, nz)
    m_bolso = m_bolso * (1 - lado + lado * herramienta)
    r = r_g * (1 - m_izq) * (1 - m_bolso) * visto.astype(np.float32)
    return r.astype(np.float32), {"g": g, "r_g": r_g, "m_izq": m_izq, "m_bolso": m_bolso,
                                  "correa": correa, "herramienta": herramienta}


def indice_pelo(P, L0, radio=1):
    """Fraccion de texels oscuros (L* < 30 en Tripo) en una caja de (2 radio + 1) voxeles de 6 mm,
    solo arriba (y > 0,12). radio 1 = unos 18 mm; radio 3 = unos 42 mm."""
    rj = Rejilla(P, VOX_PELO)
    osc = (L0 < 30).astype(np.float32)
    S, W = rj.acumular(P, osc[:, None], np.ones(len(P), np.float32))
    S, W = caja3(S[..., 0], radio), caja3(W, radio)
    H = S / np.maximum(W, 1e-6)
    return (rj.muestrear(H, P) * suave(0.10, 0.14, P[:, 1])).astype(np.float32)


# Zonas de piel dentro de la masa de pelo (medidas en la malla con los colores de Tripo).
OREJAS = [((0.03, 0.255, 0.105), (0.04, 0.045, 0.035)), ((0.03, 0.255, -0.105), (0.04, 0.045, 0.035))]


def banda_silueta(P, ejes, ancho=0.012, res=0.001):
    """1 si la proyeccion del texel cae a menos de 'ancho' del contorno de la silueta.

    ejes: columnas de P que forman el plano de la vista ((1, 2) frente y espalda; (0, 1) perfil).
    Es donde la hoja pinta el borde naranja del pelo: ahi se conserva.
    """
    q = P[:, list(ejes)]
    o = q.min(0) - 3 * ancho
    ij = ((q - o) / res).astype(int)
    forma = ij.max(0) + int(3 * ancho / res) + 1
    m = np.zeros(forma, np.uint8)
    m[ij[:, 0], ij[:, 1]] = 255
    im = Image.fromarray(m).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    k = 2 * int(round(ancho / res)) + 1
    ero = np.asarray(im.filter(ImageFilter.MinFilter(k))) > 0
    return (~ero[ij[:, 0], ij[:, 1]]).astype(np.float32)


def elipsoide(P, centro, semiejes):
    d = np.sqrt((((P - np.array(centro)) / np.array(semiejes)) ** 2).sum(1))
    return 1 - suave(0.85, 1.15, d)


def piel_en_cabeza(P, N):
    """Orejas, cara y cuello: no son pelo aunque el pelo los rodee."""
    orejas = np.maximum(elipsoide(P, *OREJAS[0]), elipsoide(P, *OREJAS[1]))
    x, y, z = P.T
    cara = (suave(0.06, 0.08, x) * (1 - suave(0.09, 0.11, np.abs(z)))
            * suave(0.16, 0.18, y) * (1 - suave(0.325, 0.345, y)) * suave(0.2, 0.4, N[:, 0]))
    cuello = (1 - suave(0.19, 0.215, y)) * (1 - suave(0.055, 0.07, np.hypot(x - 0.01, z)))
    return np.maximum(np.maximum(orejas, cara), cuello).astype(np.float32)


# ---------- relleno ----------
def relleno_local(P, lab5, r, necesita):
    rj = Rejilla(P, VOX_LOCAL)
    S, W = rj.acumular(P, lab5, r)
    _, Wt = rj.acumular(P, lab5[:, :1], np.ones(len(P), np.float32))
    C, piramide = empujar_tirar(S, W, wref=8.0)
    del S
    q = P[necesita]
    color = rj.muestrear(C, q)
    del C
    # Fraccion fiable en el nivel 1 (5 mm) con caja de 3 voxeles (unos 15 mm).
    w1 = caja3(piramide[1])
    wt1 = caja3(reducir(Wt))
    frac = rj.muestrear(w1 / np.maximum(wt1, 1e-6), q, escala=2)
    return color.astype(np.float32), np.clip(frac, 0, 1).astype(np.float32)


def pertenencias(feat, cen):
    """Las dos zonas mas cercanas y sus pesos (softmax con SIGMA_ZONA)."""
    n = len(feat)
    z1 = np.empty(n, np.int16)
    z2 = np.empty(n, np.int16)
    p1 = np.empty(n, np.float32)
    for i in range(0, n, 1_000_000):
        d = ((feat[i:i + 1_000_000, None, :] - cen[None]) ** 2).sum(-1)
        o = np.argsort(d, 1)[:, :2]
        z1[i:i + 1_000_000], z2[i:i + 1_000_000] = o[:, 0], o[:, 1]
        d1 = np.take_along_axis(d, o[:, :1], 1)[:, 0]
        d2 = np.take_along_axis(d, o[:, 1:], 1)[:, 0]
        p1[i:i + 1_000_000] = 1 / (1 + np.exp(-(d2 - d1) / (2 * SIGMA_ZONA ** 2)))
    return z1, z2, p1


def pertenencia(k, K, z1, z2, p1, pelo):
    """Peso de la zona k: la zona K es el pelo; las demas son zonas de color fuera del pelo."""
    if k == K:
        return pelo
    return (1 - pelo) * (np.where(z1 == k, p1, 0) + np.where(z2 == k, 1 - p1, 0))


def relleno_zonas(P, lab5, L0, r, z1, z2, p1, pelo, excluir_pelo, necesita):
    """Por zona: color fiable de la misma zona (empujar-tirar) mas el detalle de Tripo.

    pelo: pertenencia a la zona semantica de pelo (indice de pelo alto, y > 0,12).
    excluir_pelo: texels fiables que no alimentan la zona de pelo (contaminacion naranja).
    """
    K = ZONAS
    # Centro de cada zona en el color de la hoja, aprendido en lo fiable.
    mu5 = np.zeros((K + 1, 3), np.float32)
    for k in range(K + 1):
        w = r * pertenencia(k, K, z1, z2, p1, pelo) * (r > 0.5)
        if k == K:
            w = w * (1 - excluir_pelo)
        mu5[k] = (lab5 * w[:, None]).sum(0) / max(w.sum(), 1e-6) if w.sum() > 0 else np.nan
    validos = ~np.isnan(mu5[:, 0])
    # Distancia al centro mas cercano (para el filtro de coherencia).
    dmin = np.full(len(P), np.inf, np.float32)
    for k in np.flatnonzero(validos):
        dmin = np.minimum(dmin, np.linalg.norm(lab5 - mu5[k], axis=1))
    rz = Rejilla(P, VOX_ZONA)
    rd = Rejilla(P, VOX_DETALLE)
    q = np.flatnonzero(necesita)
    acum = np.zeros((len(q), 3), np.float32)
    peso = np.zeros(len(q), np.float32)
    info = []
    for k in range(K + 1):
        pk = pertenencia(k, K, z1, z2, p1, pelo).astype(np.float32)
        sel = np.flatnonzero(pk > 0.01)
        if not len(sel):
            continue
        # Detalle: luminancia de Tripo menos su paso bajo dentro de la zona.
        S, W = rd.acumular(P[sel], L0[sel, None], pk[sel])
        Cd, _ = empujar_tirar(S, W, wref=30.0)
        mq = pk[q] > 0.01
        qs = q[mq]
        bajo = rd.muestrear(Cd, P[qs])[:, 0]
        det = np.clip(GANANCIA_DETALLE * (L0[qs] - bajo), -LIMITE_DETALLE, LIMITE_DETALLE)
        if validos[k]:
            d_prop = np.linalg.norm(lab5[sel] - mu5[k], axis=1)
            filtro = np.exp(-((d_prop - dmin[sel]) / 10.0) ** 2)
            wa = r[sel] * pk[sel] * filtro
            if k == K:
                wa = wa * (1 - excluir_pelo[sel])
        else:
            wa = np.zeros(len(sel), np.float32)
        if wa.sum() < 50:
            # Zona sin datos fiables: se usa la media global de la hoja en lo fiable de su color.
            base = np.repeat(mu5[validos].mean(0, keepdims=True), len(qs), 0)
        else:
            S, W = rz.acumular(P[sel], lab5[sel], wa)
            C, _ = empujar_tirar(S, W, wref=12.0)
            base = rz.muestrear(C, P[qs])
            del C
        base[:, 0] += det
        acum[mq] += base * pk[qs, None]
        peso[mq] += pk[qs]
        info.append({"zona": "pelo" if k == K else k, "texels": int(len(sel)), "rellenar": int(len(qs)),
                     "peso_fiable": float(wa.sum()),
                     "centro_hoja_lab": None if not validos[k] else np.round(mu5[k], 1).tolist()})
    return acum / np.maximum(peso, 1e-6)[:, None], info


# ---------- retoques ----------
def rgb_a_hsv(rgb):
    c = rgb / 255.0
    mx, mn = c.max(1), c.min(1)
    d = mx - mn
    h = np.zeros(len(c), np.float32)
    s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    r, g, b = c.T
    m = d > 1e-9
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6
    hg = (b - r) / np.maximum(d, 1e-9) + 2
    hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    h = np.where(m, h, 0)
    return h, s, mx


def hsv_a_rgb(h, s, v):
    c = v * s
    hp = (h / 60.0) % 6
    x = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(c)
    i = np.floor(hp).astype(int)
    r = np.choose(i, [c, x, z, z, x, c])
    g = np.choose(i, [x, c, c, x, z, z])
    b = np.choose(i, [z, z, x, c, c, x])
    m = v - c
    return np.stack((r + m, g + m, b + m), 1) * 255.0


def mascara_naranja(rgb):
    """Naranja claro y saturado (borde de luz de la hoja); el pelo oscuro queda fuera por el brillo."""
    h, s, v = rgb_a_hsv(rgb)
    return (suave(10, 16, h) * (1 - suave(50, 60, h)) * suave(0.45, 0.6, s)
            * suave(0.38, 0.5, v)).astype(np.float32)


def huecos_uv(sup, lab5, r, w, h, pasadas=3):
    """Rellena huecos chicos con el promedio de los vecinos fiables en UV (8 vecinos).

    Solo cruza texels ocupados, asi que no salta a otra isla. Devuelve, por texel de sup,
    el color y un peso (1 en la primera pasada, 0,8 y 0,6 despues, 0 si no se lleno).
    """
    img = np.zeros((h * w, 3), np.float32)
    img[sup] = lab5
    val = np.zeros(h * w, bool)
    val[sup] = r >= 0.5
    occ = np.zeros(h * w, bool)
    occ[sup] = True
    peso = np.zeros(h * w, np.float32)
    img, val, occ, peso = img.reshape(h, w, 3), val.reshape(h, w), occ.reshape(h, w), peso.reshape(h, w)
    for p in range(pasadas):
        S = np.zeros((h, w, 3), np.float32)
        C = np.zeros((h, w), np.float32)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ys = slice(max(dy, 0), h + min(dy, 0))
                yd = slice(max(-dy, 0), h + min(-dy, 0))
                xs = slice(max(dx, 0), w + min(dx, 0))
                xd = slice(max(-dx, 0), w + min(-dx, 0))
                v = val[ys, xs]
                S[yd, xd] += img[ys, xs] * v[..., None]
                C[yd, xd] += v
        nuevo = occ & ~val & (C >= 2)
        img[nuevo] = S[nuevo] / C[nuevo][:, None]
        val[nuevo] = True
        peso[nuevo] = 1.0 - 0.2 * p
        del S, C
    return img.reshape(-1, 3)[sup], peso.reshape(-1)[sup]


def bajar_reflejos(rgb, P, pelo, fraccion=0.3, modo="pelo", color_pelo=None):
    """Baja los reflejos naranjas del pelo (y > 0,15); pelo en [0, 1].

    modo "hsv": saturacion y brillo x (1 - fraccion), literal. El naranja amarillento
    desaturado se ve verde oliva junto al pelo rojizo.
    modo "pelo": mezcla una fraccion hacia el color medio del pelo (en Lab). Baja saturacion
    y brillo y mantiene el tono rojizo del pelo.
    Devuelve el color, la mascara y la bajada media de saturacion y brillo en lo enmascarado.
    """
    h, s, v = rgb_a_hsv(rgb)
    tono = suave(8, 16, h) * (1 - suave(48, 58, h))
    m = (suave(0.13, 0.17, P[:, 1]) * pelo * tono
         * suave(0.55, 0.70, s) * suave(0.35, 0.50, v))
    if modo == "hsv":
        k = 1 - fraccion * m
        sal = hsv_a_rgb(h, s * k, v * k)
    else:
        lab = pc.a_lab(rgb)
        lab = lab + (fraccion * m)[:, None] * (np.asarray(color_pelo) - lab)
        sal = pc.de_lab(lab)
    sel = m > 0.5
    stats = {}
    if sel.any():
        _, s2, v2 = rgb_a_hsv(sal[sel])
        stats = {"texels": int(sel.sum()),
                 "bajada_saturacion_pct": float(100 * (1 - s2.mean() / s[sel].mean())),
                 "bajada_brillo_pct": float(100 * (1 - v2.mean() / v[sel].mean()))}
    return sal, m, stats


def brillo_ojo(lab, P, N):
    """Repinta redondo el brillo del ojo derecho del personaje (+Z).

    Busca el brillo de los dos ojos en la cara (frente, x > 0,1): texels claros (L* > 80)
    a menos de 6 mm de su centro aproximado. El del ojo izquierdo (-Z) da el radio.
    Devuelve el lab modificado y un informe; si algo no cuadra, no cambia nada.
    """
    cara = (N[:, 0] > 0.5) & (P[:, 0] > 0.1) & (P[:, 1] > 0.27) & (P[:, 1] < 0.34)
    yz = P[:, 1:3]
    info = {}
    centros = {"der_+Z": np.array([0.307, 0.031]), "izq_-Z": np.array([0.307, -0.037])}
    claros = {}
    for nombre, c0 in centros.items():
        cerca = cara & (np.linalg.norm(yz - c0, axis=1) < 0.006)
        b = cerca & (lab[:, 0] > 80)
        claros[nombre] = np.flatnonzero(b)
        info[nombre] = {"texels_claros": int(b.sum())}
    ref = claros["izq_-Z"]
    obj = claros["der_+Z"]
    if len(ref) < 30 or len(obj) < 10:
        info["aplicado"] = False
        return lab, info
    c_ref = yz[ref].mean(0)
    radio = float(np.percentile(np.linalg.norm(yz[ref] - c_ref, axis=1), 95))
    # Region a repintar: lo que no es iris oscuro cerca del brillo (cuadro y media luna),
    # por debajo del borde superior de la media luna (arriba esta el parpado).
    c_obj = yz[obj].mean(0)
    tope = yz[obj, 0].max() + 0.0005
    cerca = cara & (np.linalg.norm(yz - c_obj, axis=1) < 0.0065) & (yz[:, 0] <= tope)
    iris = cara & (np.linalg.norm(yz - c_obj, axis=1) < 0.010) & (lab[:, 0] < 32)
    if iris.sum() < 100:
        info["aplicado"] = False
        return lab, info
    color_iris = np.median(lab[iris], 0)
    raro = cerca & (np.linalg.norm(lab - color_iris, axis=1) > 18)
    sel = np.flatnonzero(raro)
    # Centro nuevo: centroide de la mancha (cuadro + media luna).
    c_new = yz[sel].mean(0)
    color_brillo = np.median(lab[ref][lab[ref, 0] > 88], 0) if (lab[ref, 0] > 88).sum() > 5 else lab[ref].mean(0)
    zona = np.flatnonzero(cara & (np.linalg.norm(yz - c_new, axis=1) < radio * 1.6))
    d = np.linalg.norm(yz[zona] - c_new, axis=1)
    a = 1 - suave(radio - 0.0004, radio + 0.0004, d)
    nuevo = lab.copy()
    # Fuera del disco solo se tocan los texels raros (el resto ya es iris).
    fuera = np.isin(zona, sel) | (a > 0)
    zona, a = zona[fuera], a[fuera]
    nuevo[zona] = a[:, None] * color_brillo + (1 - a[:, None]) * color_iris
    info.update({"aplicado": True, "radio_mm": round(radio * 1000, 2),
                 "centro_yz": np.round(c_new, 4).tolist(), "texels_raros": int(len(sel)),
                 "texels_repintados": int(len(zona)), "color_iris_lab": np.round(color_iris, 1).tolist(),
                 "color_brillo_lab": np.round(color_brillo, 1).tolist()})
    return nuevo, info


def dilatar_desde_interior(tex, ocupado, pasos):
    """Erosiona 1 px las islas (salvo las muy finas) y extiende el interior 'pasos' px afuera."""
    im = Image.fromarray(ocupado.astype(np.uint8) * 255)
    interior = np.asarray(im.filter(ImageFilter.MinFilter(3))) > 0
    cerca_interior = np.asarray(Image.fromarray(interior.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
    base = interior | (ocupado & ~cerca_interior)
    ph.rellenar_bordes(tex, base, pasos=pasos + 1)
    return int((ocupado & ~base).sum())


# ---------- principal ----------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path, default=LOTE / "L04_PER01_v5C.glb")
    ap.add_argument("--original", type=Path, default=LOTE / "L04_PER01_v4D_geometria.glb")
    ap.add_argument("--visto", type=Path, default=LOTE / "parecido/v5C/texels_hoja.png")
    ap.add_argument("--salida", type=Path, default=LOTE / "L04_PER01_v7D.glb")
    ap.add_argument("--diagnosticos", type=Path, default=LOTE / "parecido/v7D")
    ap.add_argument("--mascaras", action="store_true", help="guarda tambien GLB con las mascaras pintadas")
    ap.add_argument("--sin-ojo", action="store_true")
    ap.add_argument("--reflejos", type=float, default=0.3, help="fraccion que bajan saturacion y brillo")
    ap.add_argument("--modo-reflejos", choices=("pelo", "hsv"), default="pelo")
    ap.add_argument("--conservar-bolso", action="store_true", help="solo diagnostico")
    ap.add_argument("--sin-naranja", action="store_true", help="no quita el naranja de canto en el pelo")
    a = ap.parse_args()
    if a.salida.resolve() in (a.entrada.resolve(), a.original.resolve()):
        raise ValueError("La salida no puede sobrescribir una entrada")
    inicio = time.monotonic()
    a.diagnosticos.mkdir(parents=True, exist_ok=True)
    d5, b5 = ph.leer_glb(a.entrada)
    pos, uv, idx, nor, t5, _ = ph.geometria(d5, b5)
    d0, b0 = ph.leer_glb(a.original)
    pos0, uv0, idx0, _, t0, imid0 = ph.geometria(d0, b0)
    if not (np.array_equal(pos, pos0) and np.array_equal(uv, uv0) and np.array_equal(idx, idx0)):
        raise ValueError("La entrada y la original deben tener la misma geometria y las mismas UV")
    h, w = t5.shape[:2]
    if t0.shape != t5.shape:
        raise ValueError("Las texturas deben medir lo mismo")
    print("Rasterizando texels...", flush=True)
    sup, P, N = texels(pos, uv, idx, nor, w, h)
    visto = (np.asarray(Image.open(a.visto)) > 0).ravel()[sup]
    rgb5 = t5.reshape(-1, 3)[sup].astype(np.float32)
    rgb0 = t0.reshape(-1, 3)[sup].astype(np.float32)
    lab5 = pc.a_lab(rgb5).astype(np.float32)
    lab0 = pc.a_lab(rgb0).astype(np.float32)
    print(f"  {len(sup)} texels ({time.monotonic() - inicio:.0f} s)", flush=True)

    r, m = fiabilidad(P, N, visto, lab5, bolso=not a.conservar_bolso)

    print("Indice de pelo y zonas...", flush=True)
    H = indice_pelo(P, lab0[:, 0])
    feat = np.column_stack((lab0, PESO_PELO * H)).astype(np.float32)
    rng = np.random.default_rng(3)
    cen = pc.kmeans(feat[rng.choice(len(feat), 200_000, replace=False)].copy(), ZONAS)
    z1, z2, p1 = pertenencias(feat, cen)
    # Pelo: oscuro cerca (18 mm) o dentro de la masa de pelo (42 mm), salvo orejas, cara y cuello.
    # La segunda escala recoge los reflejos claros de Tripo, que bajan el indice cercano.
    H2 = indice_pelo(P, lab0[:, 0], radio=3)
    piel_cab = piel_en_cabeza(P, N)
    pelo = np.maximum(suave(0.5, 0.7, H), suave(0.3, 0.5, H2) * (1 - piel_cab)
                      * suave(0.18, 0.22, P[:, 1]))
    # Por encima de la frente (y > 0,36) todo es pelo, aunque Tripo lo pinte naranja.
    pelo = np.maximum(pelo, suave(0.35, 0.38, P[:, 1])).astype(np.float32)

    # Contaminacion naranja en el pelo: el borde naranja de cada vista de la hoja cae de canto
    # sobre los mechones (lineas amarillas en las aristas). No alimenta ni conserva el pelo.
    naranja5 = mascara_naranja(rgb5)
    # Excepto en la banda de la silueta (frente/espalda y perfil), donde la hoja si pinta el
    # borde naranja: ahi se conserva lo proyectado aunque la vista lo vea de canto.
    banda = np.maximum(banda_silueta(P, (1, 2)), banda_silueta(P, (0, 1))) * pelo
    m["banda_pelo"] = banda
    m["naranja_pelo"] = naranja5 * pelo * (1 - banda)
    if not a.sin_naranja:
        r = r * (1 - m["naranja_pelo"])
    r = np.maximum(r, banda * naranja5 * visto)
    # Piel del cuerpo y de los costados del cuello/mandibula con manchas oscuras de otra vista
    # (franja del brazo derecho de espalda, mano manchada): fuera si se aleja de la piel.
    claro_piel = cen[:, 3] < 0.3 * PESO_PELO
    k_piel = int(np.argmin(np.where(claro_piel, np.linalg.norm(cen[:, :3] - [61, 21, 47], axis=1), np.inf)))
    p_piel = pertenencia(k_piel, ZONAS, z1, z2, p1, pelo)
    region = np.maximum((P[:, 1] < 0.15).astype(np.float32),
                        (P[:, 1] < 0.215) * (1 - suave(0.4, 0.55, N[:, 0])))
    ref = (p_piel > 0.8) & (r > 0.9) & (P[:, 1] < 0.15)
    mu_piel = np.median(lab5[ref], 0)
    m["mancha_piel"] = p_piel * region * suave(25, 35, np.linalg.norm(lab5 - mu_piel, axis=1))
    r = (r * (1 - m["mancha_piel"])).astype(np.float32)
    necesita = r < 0.999
    print(f"Fiables {100 * (r >= 0.999).mean():.1f} %, a rellenar {100 * necesita.mean():.1f} %", flush=True)

    print("Relleno local...", flush=True)
    f_local, frac = relleno_local(P, lab5, r, necesita)
    print("Relleno por zonas...", flush=True)
    f_zona, info_zonas = relleno_zonas(P, lab5, lab0[:, 0], r, z1, z2, p1, pelo, naranja5, necesita)
    b_local = suave(0.35, 0.75, frac)[:, None]
    relleno = b_local * f_local + (1 - b_local) * f_zona
    # Huecos chicos (puntos sueltos en las aristas): vecinos fiables en UV, dentro de la isla.
    print("Huecos chicos en UV...", flush=True)
    uvh, uvp = huecos_uv(sup, lab5, r, w, h)
    q = np.flatnonzero(necesita)
    b_uv = (uvp[q] * suave(0.5, 0.7, frac))[:, None]
    relleno = b_uv * uvh[q] + (1 - b_uv) * relleno
    lab = lab5.copy()
    rq = r[necesita][:, None]
    lab[necesita] = rq * lab5[necesita] + (1 - rq) * relleno

    info_ojo = {"aplicado": False, "omitido": True}
    if not a.sin_ojo:
        lab, info_ojo = brillo_ojo(lab, P, N)
        print("Ojo:", json.dumps(info_ojo), flush=True)

    rgb = pc.de_lab(lab).astype(np.float32)
    # Color medio del pelo de la hoja: texels fiables de pelo, oscuros y no naranjas.
    ref_pelo = (pelo > 0.9) & (r > 0.9) & (naranja5 < 0.1) & (lab5[:, 0] < 35)
    color_pelo = np.median(lab5[ref_pelo], 0)
    rgb, m_reflejo, info_reflejos = bajar_reflejos(rgb, P, pelo, a.reflejos, a.modo_reflejos, color_pelo)
    print("Reflejos:", json.dumps(info_reflejos), flush=True)

    print("Componiendo textura...", flush=True)
    tex = t5.copy().reshape(-1, 3)
    tex[sup] = np.clip(np.rint(rgb), 0, 255).astype(np.uint8)
    tex = tex.reshape(h, w, 3)
    ocupado = np.zeros(h * w, bool)
    ocupado[sup] = True
    ocupado = ocupado.reshape(h, w)
    borde = dilatar_desde_interior(tex, ocupado, DILATACION)
    imagen = Image.fromarray(tex)
    imagen.save(a.diagnosticos / "textura.png")

    def mapa(valores, nombre):
        im = np.zeros(h * w, np.uint8)
        im[sup] = np.clip(valores * 255, 0, 255).astype(np.uint8)
        Image.fromarray(im.reshape(h, w)).resize((1024, 1024), Image.BILINEAR).save(a.diagnosticos / nombre)

    mapa(r, "fiabilidad.png")
    mapa(m["m_izq"], "mascara_izquierda.png")
    mapa(m["m_bolso"], "mascara_bolso.png")
    mapa(m_reflejo, "mascara_reflejos.png")
    mapa(H, "indice_pelo.png")

    buf = io.BytesIO()
    imagen.save(buf, format="PNG")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    ph.guardar_glb(a.salida, d0, b0, buf.getvalue(), imid0)
    d2, b2 = ph.leer_glb(a.salida)
    d0b, b0b = ph.leer_glb(a.original)
    assert b2[:len(b0b)] == b0b
    for clave in ("meshes", "nodes", "accessors", "materials", "textures", "scenes"):
        assert d2[clave] == d0b[clave], clave

    if a.mascaras:
        # Mascaras en color para revisar en render: rojo = 1 - r, verde = bolso, azul = izquierda.
        mt = np.zeros((h * w, 3), np.uint8)
        gris = (lab5[:, 0] * 1.4).clip(0, 255)
        mt[sup] = np.column_stack((np.maximum(gris * r, (1 - r) * 255),
                                   np.maximum(gris * r, m["m_bolso"] * 255),
                                   np.maximum(gris * r, m["m_izq"] * 255))).astype(np.uint8)
        b = io.BytesIO()
        Image.fromarray(mt.reshape(h, w, 3)).save(b, format="PNG")
        d0c, b0c = ph.leer_glb(a.original)
        ph.guardar_glb(a.diagnosticos / "mascaras.glb", d0c, b0c, b.getvalue(), imid0)
        # Segundo juego: rojo = pelo, verde = naranja en el pelo, azul = mancha en la piel.
        mt[sup] = (np.column_stack((pelo, m["naranja_pelo"], m["mancha_piel"])) * 255).astype(np.uint8)
        b = io.BytesIO()
        Image.fromarray(mt.reshape(h, w, 3)).save(b, format="PNG")
        d0c, b0c = ph.leer_glb(a.original)
        ph.guardar_glb(a.diagnosticos / "mascaras_pelo_piel.glb", d0c, b0c, b.getvalue(), imid0)

    meta = {"entrada": str(a.entrada), "original": str(a.original), "salida": str(a.salida),
            "sha256_entrada": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
            "sha256_original": hashlib.sha256(a.original.read_bytes()).hexdigest(),
            "texels": int(len(sup)), "fiables_pct": float(100 * (r >= 0.999).mean()),
            "rellenados_pct": float(100 * necesita.mean()),
            "g_bajo_pct": float(100 * (m["g"] < 0.35).mean()),
            "no_vistos_pct": float(100 * (~visto).mean()),
            "izquierda_texels": int((m["m_izq"] > 0.5).sum()),
            "bolso_texels": int((m["m_bolso"] > 0.5).sum()),
            "correa_protegida_texels": int((m["correa"] > 0.5).sum()),
            "relleno_local_medio": float(b_local.mean()),
            "relleno_uv_texels": int((uvp > 0).sum()),
            "naranja_pelo_texels": int((m["naranja_pelo"] > 0.5).sum()),
            "mancha_piel_texels": int((m["mancha_piel"] > 0.5).sum()),
            "zona_piel": k_piel, "piel_hoja_lab": np.round(mu_piel, 1).tolist(),
            "reflejos_texels": int((m_reflejo > 0.5).sum()), "reflejos": info_reflejos,
            "reflejos_modo": a.modo_reflejos, "reflejos_fraccion": a.reflejos,
            "color_pelo_lab": np.round(color_pelo, 1).tolist(),
            "borde_reemplazado_texels": borde, "ojo": info_ojo,
            "zonas_centros": np.round(cen, 1).tolist(), "zonas": info_zonas,
            "parametros": {"VOX_LOCAL": VOX_LOCAL, "VOX_ZONA": VOX_ZONA, "VOX_DETALLE": VOX_DETALLE,
                           "ZONAS": ZONAS, "SIGMA_ZONA": SIGMA_ZONA, "PESO_PELO": PESO_PELO,
                           "GANANCIA_DETALLE": GANANCIA_DETALLE, "DILATACION": DILATACION},
            "segundos": round(time.monotonic() - inicio, 1)}
    (a.diagnosticos / "limpieza.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("fiables_pct", "rellenados_pct", "izquierda_texels", "bolso_texels",
                                             "reflejos_texels", "segundos")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
