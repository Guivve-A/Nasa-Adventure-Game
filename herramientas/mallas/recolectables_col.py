"""Recolectables del ancla ANC_VISTA_JUEGO (lote 02) hechos por script: antena, panel solar y destello.

Recursos (hoja HR_COL_v1, COL-01 y COL-02):
  COL-01_script  antena parabolica caida y oxidada (derecha del ancla, x 1780-2350, y 560-960): plato concavo
                 facetado de 1,1 m con el borde inclinado unos 50 grados, tripode del alimentador con su cajita,
                 montura (cubo, brazo, pivote, columna, patas y base circular) y una enredadera (Follaje).
                 Sin parche de hierba: lo pone la escena. Se compara con COL-01_tripo (IA).
  COL-02         panel solar viejo (abajo a la derecha, x 1950-2500, y 1030-1350): 1,4 x 0,9 m, casi plano y
                 levantado por detras sobre dos patas; celdas azul oscuro (petroleo con oscuro) separadas por
                 lineas claras, una grieta, marco de metal oxidado con tornillos y hojas de enredadera encima.
  FX-01          destello de recolectable: estrella de cuatro puntas hecha con dos rombos cruzados (0,35 m de
                 alto), material Emisivo, de doble cara y de cara a la camara de juego (inclinada 50 grados).

Orientacion: cada recurso se modela tal como se ve en el ancla (+X derecha, -Z lejos) y se le descuenta el
giro en Y que ya le da layout.json (GIRO_LAYOUT). Asi la escena lo muestra como el ancla sin tocar el layout.
Si el layout cambia ese giro, se cambia aqui y se regenera.

Origen: centro de la huella en planta (caja XZ, medida en la orientacion del ancla), apoyado en y = 0.
Solo colores de la paleta maestra y sus mezclas. La luz calida y la sombra petroleo las pone la escena.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/recolectables_col.py [COL-01 COL-02 FX-01]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, RAIZ, Escena, Malla, marco, mezclar, rot_eje, rot_y, tubo  # noqa: E402

SALIDA = RAIZ / "pruebas" / "escena_exploracion" / "modelos"
ARRIBA = np.array([0.0, 1.0, 0.0])

# giro en Y (grados) que layout.json ya aplica a cada recurso; se descuenta al modelar
GIRO_LAYOUT = {"COL-01_script": -30.0, "COL-02": 12.0, "FX-01": 0.0}


def tono(sombra, base, luz):
    """Tres colores de un material pintado: sombra (abajo), base y luz (arriba)."""
    return tuple(np.asarray(c, float) for c in (sombra, base, luz))


# ---------- tonos ----------
# metal del plato: al sol la piedra clara sale casi blanca, por eso se templa con piedra (malva) y tierra1
METAL = tono(mezclar(PAL["piedra"], PAL["petroleo"], 0.30), mezclar(PAL["piedra_clara"], PAL["piedra"], 0.45),
             mezclar(PAL["piedra_clara"], PAL["tierra1"], 0.35))
# oxido: terracota en sombra, tierra2 de base y naranja (tierra2 con sol) en la luz
OXIDO = tono(mezclar(PAL["terracota"], PAL["madera2"], 0.30), mezclar(PAL["terracota"], PAL["tierra2"], 0.45),
             mezclar(PAL["tierra2"], PAL["sol"], 0.40))
# borde del plato: la banda naranja del ancla
BORDE = tono(PAL["terracota"], mezclar(PAL["tierra2"], PAL["sol"], 0.30), mezclar(PAL["sol"], PAL["tierra1"], 0.40))
# hierro de la montura y la parte de atras del plato (oxido oscuro, sin llegar a negro en la sombra)
HIERRO = tono(mezclar(PAL["terracota"], PAL["madera2"], 0.45), mezclar(PAL["terracota"], PAL["madera1"], 0.30),
              mezclar(PAL["terracota"], PAL["tierra2"], 0.60))
CAJA = tono(mezclar(PAL["tierra2"], PAL["piedra"], 0.50), mezclar(PAL["piedra_clara"], PAL["tierra1"], 0.55),
            mezclar(PAL["crema"], PAL["piedra_clara"], 0.35))
BOCA = PAL["oscuro"]
PERNO = tono(PAL["oscuro"], PAL["piedra_osc"], mezclar(PAL["piedra_osc"], PAL["piedra_clara"], 0.45))
# panel solar
CELDA = tono(mezclar(PAL["petroleo"], PAL["oscuro"], 0.62), mezclar(PAL["petroleo"], PAL["oscuro"], 0.38),
             mezclar(PAL["petroleo"], PAL["oscuro"], 0.22))
# iteracion 10 del ajuste al ancla: las lineas claras dominaban y el panel se leia blanco; en el ancla es azul marino
LINEA = mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.3)
GRIETA = mezclar(PAL["crema"], PAL["piedra_clara"], 0.30)
MARCO = OXIDO  # iteracion 10: el marco del ancla es de metal oxidado, no claro
# enredadera
HOJA_BASE = mezclar(PAL["hierba_sombra"], PAL["oscuro"], 0.12)
HOJA_PUNTA = mezclar(PAL["hierba_sol"], PAL["dorado"], 0.35)
TALLO_BAJO = mezclar(PAL["hierba_sombra"], PAL["madera2"], 0.45)
TALLO_ALTO = mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.40)


# ---------- ayudas ----------

def unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


def grad(t, tn):
    """Degradado pintado del nucleo: sombra abajo, base hacia el 60 % y luz arriba."""
    s, b, l = tn
    t = min(max(float(t), 0.0), 1.0)
    return mezclar(s, b, min(1.0, t * 1.7)) if t < 0.6 else mezclar(b, l, (t - 0.6) / 0.4)


class Pincel:
    """Degradado por altura de mundo entre y0 (oscuro) e y1 (claro)."""

    def __init__(self, y0, y1):
        self.y0, self.y1 = float(y0), float(y1)

    def t(self, p):
        return (p[1] - self.y0) / max(self.y1 - self.y0, 1e-6)

    def __call__(self, p, tn, k=1.0, dt=0.0):
        return grad(self.t(p) + dt, tn) * k


def tri_hacia(m, a, b, c, ca, cb, cc, hacia, normales=None):
    """Triangulo con la cara delantera hacia 'hacia' (invierte el orden si hace falta)."""
    a, b, c = (np.asarray(p, float) for p in (a, b, c))
    if np.dot(np.cross(b - a, c - a), hacia) < 0:
        b, c, cb, cc = c, b, cc, cb
    m.tri(a, b, c, ca, cb, cc, normales=normales)


def poligono(m, pts, cols, hacia):
    """Poligono convexo en abanico desde el primer punto, mirando hacia 'hacia'."""
    for i in range(1, len(pts) - 1):
        tri_hacia(m, pts[0], pts[i], pts[i + 1], cols[0], cols[i], cols[i + 1], hacia)


def barra(m, p0, p1, radio, lados, tn, pincel, rng, radio1=None, giro=None, tapa0=True, tapa1=True,
          oxido=None, var=0.05):
    """Barra prismatica de p0 a p1 con caras planas; cada cara con su degradado por altura de mundo.
    'oxido' = (tono, probabilidad): algunas caras salen con ese tono."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    u, v = marco(p1 - p0)
    r1 = radio if radio1 is None else radio1
    g = (math.pi / lados) if giro is None else giro
    ang = g + np.arange(lados) / lados * 2 * math.pi
    a0 = [p0 + (math.cos(t) * u + math.sin(t) * v) * radio for t in ang]
    a1 = [p1 + (math.cos(t) * u + math.sin(t) * v) * r1 for t in ang]
    for s in range(lados):
        s2 = (s + 1) % lados
        k = 1 + rng.normal(0, var)
        tn_c = oxido[0] if (oxido is not None and rng.random() < oxido[1]) else tn
        q = [a0[s], a0[s2], a1[s2], a1[s]]
        m.quad(*q, *[pincel(p, tn_c, k) for p in q])
    if tapa1:
        for s in range(lados):
            tri = (p1, a1[s], a1[(s + 1) % lados])
            m.tri(*tri, *[pincel(p, tn, 1.0, 0.15) for p in tri])
    if tapa0:
        for s in range(lados):
            tri = (p0, a0[(s + 1) % lados], a0[s])
            m.tri(*tri, *[pincel(p, tn) for p in tri])
    return a0, a1


def caja_orientada(m, c, ex, ey, medios, tn, pincel, rng, caras_oxido=(), oxido=None, sin=()):
    """Caja centrada en c con ejes ex, ey (ez = ex x ey) y medios lados (hx, hy, hz).
    Devuelve las 4 esquinas de cada cara por nombre ('+x', '-x', '+y', '-y', '+z', '-z')."""
    ex, ey = unit(ex), unit(ey)
    ez = np.cross(ex, ey)
    hx, hy, hz = medios
    c = np.asarray(c, float)

    def P(sx, sy, sz):
        return c + ex * sx * hx + ey * sy * hy + ez * sz * hz

    caras = {"+x": [P(1, -1, -1), P(1, 1, -1), P(1, 1, 1), P(1, -1, 1)],
             "-x": [P(-1, -1, 1), P(-1, 1, 1), P(-1, 1, -1), P(-1, -1, -1)],
             "+y": [P(-1, 1, -1), P(-1, 1, 1), P(1, 1, 1), P(1, 1, -1)],
             "-y": [P(-1, -1, -1), P(1, -1, -1), P(1, -1, 1), P(-1, -1, 1)],
             "+z": [P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1)],
             "-z": [P(1, -1, -1), P(-1, -1, -1), P(-1, 1, -1), P(1, 1, -1)]}
    for nombre, q in caras.items():
        if nombre in sin:
            continue
        k = 1 + rng.normal(0, 0.05)
        tn_c = oxido if (oxido is not None and nombre in caras_oxido) else tn
        m.quad(*q, *[pincel(p, tn_c, k) for p in q])
    return caras


def perno(m, centro, normal, radio, alto, lados=6):
    """Cabeza de perno: prisma bajo con la tapa clara (se lee como un punto oscuro con brillo)."""
    n = unit(normal)
    u, v = marco(n)
    centro = np.asarray(centro, float)
    ang = np.arange(lados) / lados * 2 * math.pi
    b = [centro + (math.cos(t) * u + math.sin(t) * v) * radio for t in ang]
    t_ = [centro + n * alto + (math.cos(t) * u + math.sin(t) * v) * radio * 0.72 for t in ang]
    osc, base, luz = PERNO
    for s in range(lados):
        s2 = (s + 1) % lados
        tri_hacia(m, b[s], b[s2], t_[s2], osc, osc, base, b[s] + b[s2] - 2 * centro)
        tri_hacia(m, b[s], t_[s2], t_[s], osc, base, base, b[s] + b[s2] - 2 * centro)
    poligono(m, t_, [luz] * lados, n)


def hoja_corazon(m, base, direccion, normal, largo, ancho, c_base, c_punta, doblez=0.14):
    """Hoja de enredadera con forma de corazon (6 triangulos), plegada por el nervio; mira hacia 'normal'."""
    d = unit(direccion)
    n = unit(np.asarray(normal, float) - np.dot(normal, d) * d)
    lat = np.cross(n, d)
    b = np.asarray(base, float)

    def P(x, y, z):
        return b + d * (x * largo) + lat * (y * ancho) + n * (z * ancho)

    escot = P(0.08, 0.0, 0.0)
    nervio = P(0.45, 0.0, 0.0)
    punta = P(1.0, 0.0, -0.04)
    cm = mezclar(c_base, c_punta, 0.55)
    cb = mezclar(c_base, c_punta, 0.25) * 0.92   # borde bajo del pliegue, algo mas oscuro
    for lado in (1, -1):
        lob = P(-0.05, 0.30 * lado, -doblez * 0.6)
        anch = P(0.32, 0.50 * lado, -doblez)
        tri_hacia(m, escot, lob, nervio, c_base, cb, cm, n)
        tri_hacia(m, lob, anch, nervio, cb, cb, cm, n)
        tri_hacia(m, anch, punta, nervio, cb, c_punta, cm, n)


def enredadera(fol, puntos, hacia_fn, rng, cada=0.075, largo=(0.065, 0.10), radio=0.0075, desde=0.06,
               ancho=0.86, hasta=None, colgar=0.25):
    """Tallo fino por una polilinea con hojas de corazon alternadas; hacia_fn(p) = hacia donde mira la hoja."""
    pts = [np.asarray(p, float) for p in puntos]
    tubo(fol, pts, [radio * (1.0 - 0.45 * i / max(len(pts) - 1, 1)) for i in range(len(pts))], 4,
         TALLO_BAJO, TALLO_ALTO, rng, ruido=0.05, tapa=False)
    tramos = np.cumsum([0.0] + [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)])
    total = tramos[-1] if hasta is None else min(hasta, tramos[-1])
    s, lado, n_hojas = desde, 1, 0
    while s < total:
        i = int(np.clip(np.searchsorted(tramos, s) - 1, 0, len(pts) - 2))
        f = (s - tramos[i]) / max(tramos[i + 1] - tramos[i], 1e-9)
        p = pts[i] * (1 - f) + pts[i + 1] * f
        tg = unit(pts[i + 1] - pts[i])
        n = unit(hacia_fn(p) + rng.normal(0, 0.22, 3))
        lat = unit(np.cross(n, tg)) * lado
        d = lat * 0.85 + tg * 0.35 - ARRIBA * colgar + rng.normal(0, 0.2, 3)
        d = unit(d - n * np.dot(d, n))
        L = rng.uniform(*largo)
        punta = mezclar(HOJA_PUNTA, PAL["crema"], rng.uniform(0.0, 0.18)) * rng.uniform(0.93, 1.05)
        hoja_corazon(fol, p + lat * 0.01 + n * 0.006, d, n, L, L * ancho, HOJA_BASE * rng.uniform(0.9, 1.1), punta)
        s += cada * rng.uniform(0.8, 1.2)
        lado = -lado
        n_hojas += 1
    return n_hojas


def terminar(mallas, giro_layout_deg):
    """Centra la huella en planta en el origen, apoya en y = 0 y descuenta el giro que da el layout."""
    P = np.concatenate([np.array(m.P).reshape(-1, 3) for m in mallas if len(m)])
    lo, hi = P.min(0), P.max(0)
    mover = np.array([(lo[0] + hi[0]) / 2, lo[1], (lo[2] + hi[2]) / 2])
    R = rot_y(math.radians(-giro_layout_deg))
    for m in mallas:
        m.P = [(tri - mover) @ R.T for tri in m.P]
        m.N = [None if n is None else n @ R.T for n in m.N]
    return hi - lo


# ---------- COL-01: antena parabolica ----------

def antena(semilla=11):
    rng = np.random.default_rng(semilla)
    fac = Malla("COL-01_antena")
    fol = Malla("COL-01_enredadera", material="Follaje")

    # disposicion medida en el ancla: el plato mira a la izquierda y arriba; la montura queda detras (+X)
    elev = math.radians(40.0)                  # el eje sube 40 grados: el borde queda a unos 50 del suelo
    rumbo = unit([-1.0, 0.0, -0.15])
    a = unit(rumbo * math.cos(elev) + ARRIBA * math.sin(elev))
    R, D, grosor, lados = 0.55, 0.17, 0.03, 16
    P = np.array([0.0, 0.32, 0.0])             # pivote de elevacion
    a_h = unit([a[0], 0.0, a[2]])
    H = P + a_h * 0.10 + ARRIBA * 0.05         # extremo del cubo trasero
    V = H + a * (0.08 + grosor)                # vertice de la cara concava
    C = V + a * D                              # centro del borde
    ex = unit(-ARRIBA + a * np.dot(ARRIBA, a))   # angulo 0 = punto mas bajo del borde
    ez = np.cross(ex, a)                       # angulo 90 = lado lejano del borde
    Rd = np.stack([ex, a, ez], axis=1)

    def X(p):
        return Rd @ np.asarray(p, float) + V

    def normal_p(r, t):
        g = 2 * D * r / R ** 2
        return unit([-g * math.cos(t), 1.0, -g * math.sin(t)])

    # ---- plato ----
    FR = [0.0, 0.32, 0.60, 0.83, 0.94, 1.0]
    th = math.pi / lados + np.arange(lados) / lados * 2 * math.pi

    def golpe(t):
        # abolladura del borde arriba a la derecha (como si hubiera caido sobre esa esquina)
        d = math.atan2(math.sin(t - math.radians(160)), math.cos(t - math.radians(160)))
        return 0.04 * math.exp(-(d / 0.30) ** 2)

    anillos = [[np.array([0.0, rng.normal(0, 0.003), 0.0])] * lados]
    for k, f in enumerate(FR[1:], start=1):
        fila = []
        for t in th:
            r, y = f * R, D * f * f
            if k < len(FR) - 1:
                r += rng.normal(0, 0.004)
                y += rng.normal(0, 0.006)
            else:
                g = golpe(t)
                r -= g
                y -= 0.5 * g
            fila.append(np.array([r * math.cos(t), y, r * math.sin(t)]))
        anillos.append(fila)
    W = [[X(p) for p in fila] for fila in anillos]
    ys = np.array([p[1] for fila in W for p in fila])
    pin = Pincel(ys.min(), ys.max())

    # manchas de oxido en el marco del plato: (radio relativo, angulo, alcance en m)
    manchas = [(rng.uniform(0.3, 0.9), rng.uniform(0, 2 * math.pi), rng.uniform(0.09, 0.17)) for _ in range(7)]

    def oxido_en(pm):
        x, z = pm[0], pm[2]
        r = math.hypot(x, z) / R
        amt = 0.0
        for rc, tc, alc in manchas:
            amt = max(amt, 1 - math.hypot(x - rc * R * math.cos(tc), z - rc * R * math.sin(tc)) / alc)
        return amt + max(0.0, r - 0.72) * 1.1

    def color_interior(pw, pm, clase, k, w):
        r = math.hypot(pm[0], pm[2]) / R
        metal = grad(0.55 * pin.t(pw) + 0.45 * r, METAL) * k
        if clase == 0:
            return metal
        ox = grad(pin.t(pw), OXIDO) * k
        return mezclar(metal, ox, 1.0 if clase == 2 else w)

    def faceta(trm):
        trw = [X(p) for p in trm]
        cen = np.mean(trm, 0)
        amt = oxido_en(cen)
        clase = 2 if amt > 0.55 or rng.random() < 0.05 else (1 if amt > 0.2 else 0)
        k = 1 + rng.normal(0, 0.045)
        cols = [color_interior(pw, pm, clase, k, rng.uniform(0.25, 0.85)) for pw, pm in zip(trw, trm)]
        fac.tri(*trw, *cols)

    nk = len(FR)
    for s in range(lados):
        s2 = (s + 1) % lados
        faceta([anillos[0][s], anillos[1][s2], anillos[1][s]])
        for k in range(1, nk - 2):
            q = [anillos[k][s], anillos[k][s2], anillos[k + 1][s2], anillos[k + 1][s]]
            if rng.random() < 0.5:   # diagonal al azar: manchas menos regulares
                faceta([q[0], q[1], q[2]])
                faceta([q[0], q[2], q[3]])
            else:
                faceta([q[0], q[1], q[3]])
                faceta([q[1], q[2], q[3]])
    # banda naranja del borde (interior), labio y canto exterior
    labio = [anillos[-1][s] + np.array([math.cos(t), 0, math.sin(t)]) * 0.022 - np.array([0, 0.008, 0])
             for s, t in enumerate(th)]
    atras_borde = [anillos[-1][s] - normal_p(R, t) * grosor for s, t in enumerate(th)]
    for s in range(lados):
        s2 = (s + 1) % lados
        k = 1 + rng.normal(0, 0.05)
        for q in ([anillos[-2][s], anillos[-2][s2], anillos[-1][s2], anillos[-1][s]],
                  [anillos[-1][s], anillos[-1][s2], labio[s2], labio[s]],
                  [labio[s], labio[s2], atras_borde[s2], atras_borde[s]]):
            qw = [X(p) for p in q]
            fac.quad(*qw, *[pin(p, BORDE, k) for p in qw])
    # parte de atras (convexa): hierro oxidado, pocas caras
    atras = [[anillos[0][0] - np.array([0, grosor, 0])] * lados]
    for k in (2, 4):
        atras.append([anillos[k][s] - normal_p(FR[k] * R, t) * grosor for s, t in enumerate(th)])
    atras.append(atras_borde)
    for s in range(lados):
        s2 = (s + 1) % lados
        tri = [X(atras[0][s]), X(atras[1][s]), X(atras[1][s2])]
        fac.tri(*tri, *[pin(p, HIERRO) for p in tri])
        for k in range(1, len(atras) - 1):
            q = [X(atras[k][s]), X(atras[k + 1][s]), X(atras[k + 1][s2]), X(atras[k][s2])]
            tn = OXIDO if rng.random() < 0.3 else HIERRO
            kk = 1 + rng.normal(0, 0.05)
            fac.quad(*q, *[pin(p, tn, kk) for p in q])
    # costuras radiales de los petalos del plato (tiras finas sobre la cara concava)
    for s in (1, 5, 9, 13):
        t = th[s]
        tg = np.array([-math.sin(t), 0.0, math.cos(t)])
        tira = []
        for k in range(1, nk - 1):
            p = anillos[k][s] + normal_p(FR[k] * R, t) * 0.003
            tira.append((X(p - tg * 0.0065), X(p + tg * 0.0065)))
        c_cost = mezclar(PAL["terracota"], PAL["madera2"], 0.55)
        for (i0, d0), (i1, d1) in zip(tira[:-1], tira[1:]):
            fac.quad(i0, d0, d1, i1, c_cost, c_cost, c_cost * 1.12, c_cost * 1.12)

    # ---- alimentador: cajita en el eje y tripode ----
    F = C + a * 0.34
    exb = unit(ex * math.cos(math.radians(25)) + ez * math.sin(math.radians(25)))
    hb = 0.07
    pin_caja = Pincel(F[1] - 0.12, F[1] + 0.10)
    caras = caja_orientada(fac, F, exb, a, (hb, hb, hb), CAJA, pin_caja, rng, caras_oxido=("+x", "-z"),
                           oxido=OXIDO, sin=("+y",))
    # boca del alimentador en la cara de fuera: marco claro y hueco oscuro hundido
    ezb = np.cross(exb, a)
    sup = F + a * hb
    ext = [sup + (exb * sx + ezb * sz) * hb for sx, sz in ((-1, -1), (-1, 1), (1, 1), (1, -1))]
    inte = [sup + (exb * sx + ezb * sz) * hb * 0.58 for sx, sz in ((-1, -1), (-1, 1), (1, 1), (1, -1))]
    fondo = [p - a * 0.035 for p in inte]
    for i in range(4):
        j = (i + 1) % 4
        q = [ext[i], ext[j], inte[j], inte[i]]
        poligono(fac, q, [pin_caja(p, CAJA, 1.04) for p in q], a)
        tri_hacia(fac, inte[i], inte[j], fondo[j], BOCA * 1.3, BOCA * 1.3, BOCA, -(inte[i] + inte[j]) / 2 + sup)
        tri_hacia(fac, inte[i], fondo[j], fondo[i], BOCA * 1.3, BOCA, BOCA, -(inte[i] + inte[j]) / 2 + sup)
    poligono(fac, fondo, [BOCA] * 4, a)
    nucleo_boca = [F + a * (hb - 0.033) + (exb * sx + ezb * sz) * 0.016 for sx, sz in ((-1, 0), (0, 1), (1, 0), (0, -1))]
    poligono(fac, nucleo_boca, [PAL["dorado"]] * 4, a)
    # tripode: dos patas al borde de abajo a la izquierda y una larga al centro derecho
    pin_feed = Pincel(pin.y0, F[1] + 0.05)
    for r_f, t_deg in ((0.84, 12.0), (0.80, 78.0), (0.46, 205.0)):
        t = math.radians(t_deg)
        pm = np.array([r_f * R * math.cos(t), D * r_f * r_f, r_f * R * math.sin(t)])
        q = X(pm + normal_p(r_f * R, t) * 0.004)
        hacia = unit(q - F)
        sale = F - a * (hb * 0.7) + unit(hacia - a * np.dot(hacia, a)) * hb * 0.6
        barra(fac, sale, q, 0.016, 4, OXIDO, pin_feed, rng, tapa0=False, giro=math.pi / 4)
        # placa de anclaje sobre la cara concava
        tg = np.array([-math.sin(t), 0.0, math.cos(t)])
        rad = np.array([math.cos(t), 0.0, math.sin(t)])
        n_p = normal_p(r_f * R, t)
        placa = [X(pm + n_p * 0.005 + (rad * sx + tg * sz) * 0.032) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        poligono(fac, placa, [pin(p, HIERRO, 1.05) for p in placa], Rd @ n_p)

    # ---- montura ----
    pin_m = Pincel(0.0, P[1] + 0.12)
    barra(fac, X([0, -grosor + 0.004, 0]), H, 0.085, 8, HIERRO, pin_m, rng, oxido=(OXIDO, 0.35))   # cubo
    brazo_b = P + ARRIBA * 0.01
    barra(fac, H + a * 0.02, brazo_b, 0.034, 4, HIERRO, pin_m, rng, giro=math.pi / 4)               # brazo
    eje_p = unit(np.cross(ARRIBA, a_h))      # eje de elevacion, horizontal y perpendicular al rumbo
    barra(fac, P - eje_p * 0.11, P + eje_p * 0.11, 0.035, 8, HIERRO, pin_m, rng)                     # eje
    for sgn in (-1, 1):
        perno(fac, P + eje_p * (0.11 * sgn), eje_p * sgn, 0.03, 0.018)
        caja_orientada(fac, P + eje_p * (0.075 * sgn) - ARRIBA * 0.045, a_h, ARRIBA, (0.04, 0.06, 0.012),
                       HIERRO, pin_m, rng, sin=("-y",))                                               # horquilla
    B = np.array([P[0] + 0.03, 0.0, P[2]])
    alto_base = 0.04
    barra(fac, B, B + ARRIBA * alto_base, 0.25, 12, HIERRO, Pincel(-0.08, 0.20), rng, tapa0=False,
          oxido=(OXIDO, 0.4))                                                                         # base
    barra(fac, B + ARRIBA * alto_base, B + ARRIBA * (alto_base + 0.028), 0.155, 10, OXIDO,
          Pincel(-0.05, 0.22), rng, tapa0=False)                                                      # aro
    for i in range(6):
        t = i / 6 * 2 * math.pi + 0.3
        perno(fac, B + np.array([math.cos(t) * 0.205, alto_base, math.sin(t) * 0.205]), ARRIBA, 0.02, 0.014)
    y_col = alto_base + 0.028
    barra(fac, B + ARRIBA * y_col, B + ARRIBA * (y_col + 0.05), 0.10, 8, HIERRO, pin_m, rng, tapa0=False)
    tope = P[1] - 0.105
    barra(fac, B + ARRIBA * (y_col + 0.05), B + ARRIBA * (tope - 0.035), 0.068, 8, HIERRO, pin_m, rng,
          tapa0=False, oxido=(OXIDO, 0.3))                                                            # columna
    barra(fac, B + ARRIBA * (tope - 0.035), B + ARRIBA * tope, 0.09, 8, OXIDO, pin_m, rng, tapa0=False)  # collar
    # patas en A hacia la derecha (atras del plato)
    for sgn in (-1, 1):
        arriba_p = P + eje_p * (0.085 * sgn) + np.array([0.02, -0.01, 0.0])
        pie = np.array([P[0] + 0.42, 0.012, P[2] + 0.17 * sgn])
        barra(fac, arriba_p, pie, 0.018, 4, HIERRO, pin_m, rng, giro=math.pi / 4, oxido=(OXIDO, 0.4))
        caja_orientada(fac, pie + ARRIBA * 0.006, unit(pie - P) * np.array([1, 0, 1]), ARRIBA,
                       (0.04, 0.008, 0.035), HIERRO, Pincel(-0.1, 0.3), rng, sin=("-y",))
    # puntal caido a la izquierda: sostiene el borde bajo del plato
    t0 = math.radians(25)
    alto_p = np.array([0.86 * R * math.cos(t0), D * 0.74, 0.86 * R * math.sin(t0)])
    ap = X(alto_p - normal_p(0.86 * R, t0) * (grosor + 0.012))
    pie_iz = np.array([ap[0] - 0.24, 0.014, ap[2] + 0.12])
    barra(fac, ap, pie_iz, 0.014, 4, HIERRO, pin_m, rng, giro=math.pi / 4, oxido=(OXIDO, 0.5))

    # ---- enredadera ----
    rc = 0.068 + 0.012

    def hacia_columna(p):
        r = np.array([p[0] - B[0], 0.0, p[2] - B[2]])
        return unit(unit(r) + ARRIBA * 0.55)

    helice = []
    for i in range(10):
        f = i / 9
        ang = math.radians(115) + f * 2 * math.pi * 1.05
        helice.append(B + np.array([math.cos(ang) * rc, y_col + 0.03 + f * (tope - y_col - 0.02), math.sin(ang) * rc]))
    inicio = [B + np.array([-0.30, 0.008, 0.30]), B + np.array([-0.21, alto_base + 0.01, 0.21]),
              B + np.array([math.cos(math.radians(115)) * 0.12, y_col + 0.012, math.sin(math.radians(115)) * 0.12])]

    def sobre_atras(r_f, t_deg, sep=0.014):
        t = math.radians(t_deg)
        pm = np.array([r_f * R * math.cos(t), D * r_f * r_f, r_f * R * math.sin(t)])
        return X(pm - normal_p(r_f * R, t) * (grosor + sep))

    def sobre_dentro(r_f, t_deg, sep=0.016):
        t = math.radians(t_deg)
        pm = np.array([r_f * R * math.cos(t), D * r_f * r_f, r_f * R * math.sin(t)])
        return X(pm + normal_p(r_f * R, t) * sep)

    t_lab = math.radians(268)
    sobre_labio = X(np.array([(R + 0.035) * math.cos(t_lab), D + 0.01, (R + 0.035) * math.sin(t_lab)]))
    camino1 = (inicio + helice + [H + ARRIBA * 0.07 + eje_p * 0.05, sobre_atras(0.35, 300), sobre_atras(0.66, 284),
                                  sobre_atras(0.93, 272), sobre_labio, sobre_dentro(0.9, 262), sobre_dentro(0.76, 252),
                                  sobre_dentro(0.66, 240)])
    eje_mundo = a.copy()

    def hacia_1(p):
        # en la columna mira hacia fuera; sobre el plato, hacia fuera de su cara (atras o dentro)
        if p[1] < tope + 0.02 and np.linalg.norm((p - B) * np.array([1, 0, 1])) < 0.2:
            return hacia_columna(p)
        lado = np.dot(p - C, eje_mundo)
        return unit((eje_mundo if lado > -0.06 else -eje_mundo) + ARRIBA * 0.6)

    n1 = enredadera(fol, camino1, hacia_1, rng, cada=0.068, largo=(0.07, 0.105), desde=0.12)
    # zarcillo que cae de la columna al suelo, por delante
    camino2 = [helice[5] + np.array([0.0, 0.0, 0.01]), B + np.array([-0.10, 0.13, 0.17]),
               B + np.array([-0.17, 0.07, 0.27]), B + np.array([-0.24, 0.02, 0.36]), B + np.array([-0.33, 0.012, 0.40])]
    n2 = enredadera(fol, camino2, lambda p: unit(ARRIBA + np.array([0.0, 0.0, 0.3])), rng, cada=0.07,
                    largo=(0.055, 0.085), desde=0.05)
    # brote pequeno sobre el borde bajo, a la izquierda
    pie_b = pie_iz + np.array([0.06, 0.0, 0.05])
    camino3 = [pie_b, (pie_b + ap) / 2 + ARRIBA * 0.03, ap + ARRIBA * 0.02 - eje_mundo * 0.02, sobre_dentro(1.03, 8, 0.03),
               sobre_dentro(0.9, 18), sobre_dentro(0.8, 30)]
    n3 = enredadera(fol, camino3, lambda p: unit(eje_mundo + ARRIBA * 0.5), rng, cada=0.075,
                    largo=(0.05, 0.08), desde=0.10)

    info = {"hojas": n1 + n2 + n3, "eje_plato": [round(float(v), 3) for v in a],
            "centro_borde": [round(float(v), 3) for v in C], "alimentador": [round(float(v), 3) for v in F]}
    return [fac, fol], info


# ---------- COL-02: panel solar ----------

def panel(semilla=23):
    rng = np.random.default_rng(semilla)
    fac = Malla("COL-02_panel_solar")
    fol = Malla("COL-02_enredadera", material="Follaje")
    Lx, Lz = 1.40, 0.90          # medidas del marco
    fb, hf, hc = 0.055, 0.045, 0.034   # ancho del marco, alto del marco y altura de las celdas
    nx, nz = 9, 6
    # pose medida en el ancla: girado en planta (el borde largo baja hacia la derecha), levantado por detras
    # 7 grados y algo mas alto a la derecha
    Rp = rot_y(math.radians(-22.0)) @ rot_eje([0, 0, 1], math.radians(2.5)) @ rot_eje([1, 0, 0], math.radians(7.0))
    esquinas = np.array([[sx * Lx / 2, sy, sz * Lz / 2] for sx in (-1, 1) for sz in (-1, 1) for sy in (0.0, hf)])
    t0 = np.array([0.0, -float((esquinas @ Rp.T)[:, 1].min()), 0.0])

    def T(p):
        return Rp @ np.asarray(p, float) + t0

    nrm = Rp @ ARRIBA     # normal de la cara del panel en mundo
    pin = Pincel(-0.02, hf + 0.12)
    xi, zi = Lx / 2 - fb, Lz / 2 - fb   # medio interior

    # fondo claro (las lineas entre celdas) y celdas octogonales (las esquinas achaflanadas dejan rombos claros)
    fondo = [T([-xi, hc, -zi]), T([-xi, hc, zi]), T([xi, hc, zi]), T([xi, hc, -zi])]
    poligono(fac, fondo, [LINEA * 0.95, LINEA, LINEA, LINEA * 0.95], nrm)
    margen, hueco, chafl = 0.010, 0.011, 0.022
    px = (2 * xi - 2 * margen) / nx
    pz = (2 * zi - 2 * margen) / nz
    # celdas con manchas de suciedad u oxido (fila, columna)
    sucias = {(5, 3): 0.55, (5, 4): 0.35, (4, 4): 0.25, (0, 8): 0.4, (3, 0): 0.3}
    for i in range(nx):
        for j in range(nz):
            x0 = -xi + margen + i * px + hueco / 2
            x1 = x0 + px - hueco
            z0 = -zi + margen + j * pz + hueco / 2
            z1 = z0 + pz - hueco
            c = chafl
            octo = [(x0 + c, z1), (x1 - c, z1), (x1, z1 - c), (x1, z0 + c), (x1 - c, z0), (x0 + c, z0),
                    (x0, z0 + c), (x0, z1 - c)]
            pts = [T([x, hc + 0.004, z]) for x, z in octo]
            # brillo del vidrio: banda diagonal clara que cruza el panel
            k = 1 + rng.normal(0, 0.04)
            cols = []
            for (x, z) in octo:
                lejos = (-(z) / (2 * zi)) + 0.5                     # 0 delante, 1 detras
                banda = math.exp(-((x * 0.55 - z + 0.05) / 0.22) ** 2)
                cc = grad(0.15 + 0.5 * lejos + 0.35 * banda, CELDA) * k
                cols.append(cc)
            if (j, i) in sucias:
                w = sucias[(j, i)]
                tinte = mezclar(PAL["tierra2"], PAL["hierba_sol"], rng.uniform(0.2, 0.6))
                cols = [mezclar(cc, tinte, w * rng.uniform(0.4, 1.0)) for cc in cols]
            poligono(fac, pts, cols, nrm)

    # grieta: mancha de oxido alrededor del golpe y rayas claras que salen de el
    golpe = np.array([0.24, -0.04])
    mancha = []
    for q in range(9):
        t = q / 9 * 2 * math.pi
        r = 0.065 * rng.uniform(0.6, 1.1)
        mancha.append(T([golpe[0] + math.cos(t) * r * 1.3, hc + 0.0055, golpe[1] + math.sin(t) * r]))
    c_m = mezclar(PAL["tierra2"], PAL["sol"], 0.25)
    poligono(fac, [T([golpe[0], hc + 0.0055, golpe[1]])] + mancha + [mancha[0]],
             [mezclar(c_m, PAL["crema"], 0.3)] + [mezclar(c_m, CELDA[1], 0.45)] * 10, nrm)
    for q in range(6):
        ang = q / 6 * 2 * math.pi + rng.uniform(-0.3, 0.3)
        largo = rng.uniform(0.14, 0.33)
        p = golpe.copy()
        ancho = 0.011
        for seg in range(3):
            ang += rng.uniform(-0.45, 0.45)
            paso = largo / 3
            p2 = p + np.array([math.cos(ang), math.sin(ang)]) * paso
            perp = np.array([-math.sin(ang), math.cos(ang)])
            a2 = ancho * 0.55
            raya = [T([q2[0], hc + 0.007, q2[1]]) for q2 in
                    (p + perp * ancho / 2, p2 + perp * a2 / 2, p2 - perp * a2 / 2, p - perp * ancho / 2)]
            poligono(fac, raya, [GRIETA, GRIETA * 0.95, GRIETA * 0.95, GRIETA], nrm)
            p, ancho = p2, a2
    poligono(fac, [T([golpe[0] + math.cos(t) * 0.016, hc + 0.0075, golpe[1] + math.sin(t) * 0.016])
                   for t in np.arange(6) / 6 * 2 * math.pi], [PAL["crema"]] * 6, nrm)

    # marco: tapa en tramos (oxido por cara), canto exterior, canto interior y fondo
    ext = [(-Lx / 2, Lz / 2), (Lx / 2, Lz / 2), (Lx / 2, -Lz / 2), (-Lx / 2, -Lz / 2)]
    inn = [(-xi, zi), (xi, zi), (xi, -zi), (-xi, -zi)]
    oxidos = [OXIDO, tono(PAL["terracota"], mezclar(PAL["tierra2"], PAL["sol"], 0.35), mezclar(PAL["sol"], PAL["crema"], 0.3))]
    for lado in range(4):
        e0, e1 = np.array(ext[lado]), np.array(ext[(lado + 1) % 4])
        i0, i1 = np.array(inn[lado]), np.array(inn[(lado + 1) % 4])
        tramos = 7 if lado % 2 == 0 else 5
        for q in range(tramos):
            f0, f1 = q / tramos, (q + 1) / tramos
            pts2 = [e0 + (e1 - e0) * f0, e0 + (e1 - e0) * f1, i0 + (i1 - i0) * f1, i0 + (i1 - i0) * f0]
            pts = [T([x, hf, z]) for x, z in pts2]
            k = 1 + rng.normal(0, 0.05)
            r_ = rng.random()
            if r_ < 0.32:
                cols = [pin(p, oxidos[rng.integers(0, 2)], k) for p in pts]
            elif r_ < 0.62:
                ox = oxidos[rng.integers(0, 2)]
                cols = [mezclar(pin(p, MARCO, k), pin(p, ox, k), rng.uniform(0.2, 0.9)) for p in pts]
            else:
                cols = [pin(p, MARCO, k) for p in pts]
            poligono(fac, pts, cols, nrm)
        # canto exterior (se ve delante y a la derecha)
        tramos_c = 4
        fuera = Rp @ np.array([-(e1[1] - e0[1]), 0.0, e1[0] - e0[0]])   # normal hacia fuera del canto
        for q in range(tramos_c):
            f0, f1 = q / tramos_c, (q + 1) / tramos_c
            a2, b2 = e0 + (e1 - e0) * f0, e0 + (e1 - e0) * f1
            pts = [T([a2[0], 0.0, a2[1]]), T([b2[0], 0.0, b2[1]]), T([b2[0], hf, b2[1]]), T([a2[0], hf, a2[1]])]
            ox = rng.random() < 0.45
            cols = [pin(p, oxidos[0] if ox else MARCO, 0.92) for p in pts]
            poligono(fac, pts, cols, fuera)
        # canto interior (pequeno escalon hacia las celdas)
        pts = [T([i0[0], hc, i0[1]]), T([i1[0], hc, i1[1]]), T([i1[0], hf, i1[1]]), T([i0[0], hf, i0[1]])]
        hacia_dentro = Rp @ np.array([-(i0[0] + i1[0]), 0.0, -(i0[1] + i1[1])])
        poligono(fac, pts, [pin(p, MARCO, 0.8) for p in pts], hacia_dentro)
    poligono(fac, [T([x, 0.0, z]) for x, z in ext], [MARCO[0] * 0.8] * 4, -nrm)
    # tornillos en las esquinas y en el medio de los lados largos
    for x, z in [(-1, -1), (1, -1), (1, 1), (-1, 1), (0, -1), (0, 1)]:
        perno(fac, T([x * (Lx / 2 - fb / 2), hf, z * (Lz / 2 - fb / 2)]), nrm, 0.019, 0.011)
    # dos patas oxidadas sostienen el borde de atras
    for x in (-0.5, 0.5):
        arriba_p = T([x, 0.0, -Lz / 2 + 0.07])
        pie = np.array([arriba_p[0], 0.008, arriba_p[2] - 0.05])
        if arriba_p[1] > 0.03:
            barra(fac, arriba_p, pie, 0.012, 4, HIERRO, Pincel(0.0, 0.2), rng, giro=math.pi / 4)

    # enredadera: planta que trepa por la esquina de atras a la derecha y un tallo que cruza por delante
    esq = T([Lx / 2 - 0.06, hf + 0.01, -Lz / 2 + 0.05])
    raiz = esq + np.array([0.12, 0.0, -0.10])
    raiz[1] = 0.01

    def hacia_arriba(p):
        return unit(ARRIBA * 1.0 + nrm * 0.4 + np.array([0.0, 0.0, 0.35]))

    tallos = [
        [raiz, raiz + np.array([-0.02, 0.12, 0.02]), raiz + np.array([-0.05, 0.22, 0.03]), raiz + np.array([-0.04, 0.32, 0.0])],
        [raiz, raiz + np.array([-0.06, 0.08, 0.05]), esq + nrm * 0.03, T([Lx / 2 - 0.25, hc + 0.03, -Lz / 2 + 0.2]),
         T([Lx / 2 - 0.42, hc + 0.025, -Lz / 2 + 0.33])],
        [raiz + np.array([0.02, 0.0, 0.02]), raiz + np.array([0.08, 0.1, 0.04]), raiz + np.array([0.12, 0.2, 0.08]),
         raiz + np.array([0.10, 0.26, 0.10])],
        [esq + nrm * 0.03, T([Lx / 2 - 0.12, hc + 0.03, -Lz / 2 + 0.28]), T([Lx / 2 - 0.16, hc + 0.025, 0.05]),
         T([Lx / 2 - 0.10, hc + 0.022, 0.22])],
    ]
    hojas = 0
    for k, camino in enumerate(tallos):
        hacia = hacia_arriba if k in (0, 2) else (lambda p: unit(nrm + ARRIBA * 0.3))
        hojas += enredadera(fol, camino, hacia, rng, cada=0.07, largo=(0.07, 0.105), desde=0.05, colgar=0.05)
    frente = [T([-0.05, -0.02, Lz / 2 + 0.12]), T([-0.04, hf + 0.012, Lz / 2 - 0.02]), T([-0.12, hc + 0.022, Lz / 2 - 0.16]),
              T([-0.22, hc + 0.02, Lz / 2 - 0.26])]
    frente[0][1] = 0.01
    hojas += enredadera(fol, frente, lambda p: unit(nrm + ARRIBA * 0.2), rng, cada=0.075, largo=(0.06, 0.09),
                        desde=0.06, colgar=0.0)
    return [fac, fol], {"hojas": hojas, "celdas": nx * nz}


# ---------- FX-01: destello ----------

def destello():
    """Estrella de cuatro puntas: union de un rombo alto (0,35 m) y uno ancho (0,30 m), brazos concavos,
    de doble cara y girada para mirar a la camara de juego (que baja unos 50 grados)."""
    m = Malla("FX-01_destello", material="Emisivo")
    alto, ancho, cintura = 0.35, 0.30, 0.036
    elev = math.radians(50.0)
    u = np.array([1.0, 0.0, 0.0])
    v = np.array([0.0, math.cos(elev), -math.sin(elev)])
    n = np.cross(u, v)

    def P(x, y):
        return u * x + v * y

    puntas = {0: ancho / 2, 90: alto / 2, 180: ancho / 2, 270: alto / 2}
    contorno, cols = [], []
    c_punta = mezclar(PAL["cian"], PAL["cian_medio"], 0.35)
    c_flanco = PAL["cian"]
    c_cintura = mezclar(PAL["brillo"], PAL["cian"], 0.35)
    for g in range(0, 360, 90):
        e = np.array([math.cos(math.radians(g)), math.sin(math.radians(g))])
        tip = e * puntas[g]
        # punta, flanco concavo y cintura (en orden antihorario)
        w = np.array([math.cos(math.radians(g + 45)), math.sin(math.radians(g + 45))]) * cintura
        e2 = np.array([math.cos(math.radians(g + 90)), math.sin(math.radians(g + 90))])
        tip2 = e2 * puntas[(g + 90) % 360]
        medio1 = (tip + w) / 2
        medio1 = e * np.dot(medio1, e) + (medio1 - e * np.dot(medio1, e)) * 0.5
        medio2 = (w + tip2) / 2
        medio2 = e2 * np.dot(medio2, e2) + (medio2 - e2 * np.dot(medio2, e2)) * 0.5
        for q, c in ((tip, c_punta), (medio1, c_flanco), (w, c_cintura), (medio2, c_flanco)):
            contorno.append(P(*q))
            cols.append(c)
    centro = P(0.0, 0.0)
    for i in range(len(contorno)):
        j = (i + 1) % len(contorno)
        m.tri(centro, contorno[i], contorno[j], PAL["brillo"], cols[i], cols[j])   # cara hacia la camara
        m.tri(centro, contorno[j], contorno[i], PAL["brillo"], cols[j], cols[i])   # cara de atras
    return [m], {"normal": [round(float(x), 3) for x in n]}


# ---------- principal ----------

def guardar(ident, nodo, mallas):
    e = Escena()
    e.nodo(nodo, e.malla(*mallas, nombre=nodo))
    ruta = e.guardar(SALIDA / f"{ident}.glb")
    return ruta, e.stats[nodo]


def main(pedidos):
    informe = {}
    if "COL-01" in pedidos:
        mallas, info = antena()
        tam = terminar(mallas, GIRO_LAYOUT["COL-01_script"])
        ruta, tris = guardar("COL-01_script", "COL-01_antena", mallas)
        informe["COL-01_script"] = {"glb": str(ruta.relative_to(RAIZ)), "triangulos": tris,
                                    "por_material": {m.material: len(m) for m in mallas},
                                    "tamano_m": [round(float(x), 3) for x in tam], **info}
    if "COL-02" in pedidos:
        mallas, info = panel()
        tam = terminar(mallas, GIRO_LAYOUT["COL-02"])
        ruta, tris = guardar("COL-02", "COL-02_panel_solar", mallas)
        informe["COL-02"] = {"glb": str(ruta.relative_to(RAIZ)), "triangulos": tris,
                             "por_material": {m.material: len(m) for m in mallas},
                             "tamano_m": [round(float(x), 3) for x in tam], **info}
    if "FX-01" in pedidos:
        mallas, info = destello()
        tam = terminar(mallas, GIRO_LAYOUT["FX-01"])
        ruta, tris = guardar("FX-01", "FX-01_destello", mallas)
        informe["FX-01"] = {"glb": str(ruta.relative_to(RAIZ)), "triangulos": tris,
                            "tamano_m": [round(float(x), 3) for x in tam], **info}
    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:] or ["COL-01", "COL-02", "FX-01"])
