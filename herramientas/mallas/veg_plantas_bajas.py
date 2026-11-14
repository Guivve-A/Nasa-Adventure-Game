"""Plantas bajas y flores de la vista aprobada del sendero (ANC_VISTA_JUEGO), pintadas por script.

Genera con el nucleo (herramientas/mallas/nucleo.py), sin tocarlo, un .glb por recurso en
pruebas/escena_exploracion/modelos/:
  VEG-13.glb  mechones de hierba: nodos VEG-13_p (0,25 m), VEG-13_m (0,40 m) y VEG-13_g (0,60 m).
  VEG-14.glb  matas de flores silvestres de unos 0,4 m de diametro: nodos VEG-14_blanca, VEG-14_rosa
              y VEG-14_amarilla.
  VEG-12.glb  helecho de 0,8 m: nodo VEG-12_helecho.
  VEG-07.glb  ave del paraiso (la heliconia naranja del ancla), 0,9 m: nodo VEG-07_ave_del_paraiso.
  VEG-10.glb  planta tropical de hojas anchas (las matas verdes grandes del ancla), 0,9 m:
              nodo VEG-10_hojas_anchas.
Todos los nodos estan en el origen (centro de la base, apoyado en y = 0): la escena elige la variante
por su nombre. Material unico "Follaje" (doble cara, se mece con el viento).

Estilo: hojas y briznas anchas, puntiagudas y plegadas por el nervio (dos facetas nitidas, una mas
oscura), degradado pintado de la base oscura a la punta clara y nervio aclarado. La normal de
sombreado de cada faceta mezcla la de la cara con "arriba" y "hacia fuera de la mata": la luz celular
de la escena reparte luz y sombra por hojas enteras, como en el ancla. (El shader de follaje usa la
normal del vertice tal cual en las dos caras, medido el 2026-11-12.)

Con --vistas <carpeta> escribe ademas copias de revision (las variantes en fila y una lamina con la
silueta gris de 1,05 m) para capturarlas con vista_previa.tscn. No forman parte del juego.

Uso, desde la raiz del proyecto:  python -I herramientas/mallas/veg_plantas_bajas.py [--vistas <carpeta>]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402

from nucleo import (PAL, RAIZ, Escena, Malla, fibonacci, flor, marco, mezclar, rot_eje,  # noqa: E402
                    solido_facetado)

SALIDA = RAIZ / "pruebas" / "escena_exploracion" / "modelos"
GENERADOR = "herramientas/mallas/veg_plantas_bajas.py"
ARRIBA = np.array([0.0, 1.0, 0.0])
AUREO = math.pi * (3.0 - math.sqrt(5.0))  # angulo aureo: reparte hojas y briznas sin huecos

# ---------- colores: solo mezclas de la paleta maestra ----------
# Medidos en el ancla (ya con su luz): hoja clara #CEA915, media #625D10, oscura #444922; brizna en la
# punta #EFBB18, en el medio #95801A y en la base #77732E. Con la luz calida de la escena (x1,25 x1,04
# x0,83 en lineal) eso pide cuerpo de hoja cerca de hierba_sombra y puntas entre hierba_sol y dorado.
VERDE_BASE = mezclar(PAL["hierba_sombra"], PAL["oscuro"], 0.5)      # arranque de hojas y tallos
VERDE_FRIO = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.3)     # hojas bajas, interior de la mata
VERDE = PAL["hierba_sombra"]
CUERPO = mezclar(PAL["hierba_sombra"], PAL["oscuro"], 0.12)          # cuerpo de las hojas grandes
OLIVA = PAL["hierba_sol"]
MEDIO = mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.6)
PUNTA = mezclar(PAL["hierba_sol"], PAL["dorado"], 0.6)
PUNTA_CLARA = mezclar(PAL["dorado"], PAL["crema"], 0.3)

BLANCO = mezclar(PAL["crema"], PAL["brillo"], 0.5)                   # margarita: crema con brillo
# rosa: coral con crema; un 15 % de piedra_clara lo enfria hacia el rosa (el rosa puro del ancla,
# #FB8198, queda fuera de la paleta maestra)
ROSA = mezclar(mezclar(PAL["coral"], PAL["crema"], 0.35), PAL["piedra_clara"], 0.15)
AMARILLO = mezclar(PAL["dorado"], PAL["crema"], 0.2)
NARANJA = PAL["sol"]


# ---------- ayudas propias (el nucleo no se modifica) ----------

def normalizar(v):
    v = np.asarray(v, float)
    n = float(np.linalg.norm(v))
    return v / n if n > 1e-12 else v * 0.0


def horizontal(ang):
    return np.array([math.cos(ang), 0.0, math.sin(ang)])


def rampa(a, paradas):
    """Color en a (0..1) sobre una lista de paradas (posicion, color)."""
    a = float(np.clip(a, 0.0, 1.0))
    for (a0, c0), (a1, c1) in zip(paradas, paradas[1:]):
        if a <= a1:
            return mezclar(c0, c1, (a - a0) / max(a1 - a0, 1e-9))
    return np.asarray(paradas[-1][1], float)


def verde(a, claro=0.5):
    """Degradado pintado de las hojas: a = 0 en la base oscura, 1 en la punta al sol.
    'claro' (0..1) decide cuanto se dora la punta."""
    punta = mezclar(OLIVA, PUNTA, claro)
    return rampa(a, [(0.0, VERDE_BASE), (0.4, CUERPO), (0.75, MEDIO), (1.0, punta)])


def verde_hierba(a, claro=0.5):
    """Degradado de las briznas: base oliva oscura, medio oliva y punta dorada (a veces casi crema)."""
    punta = mezclar(PUNTA, mezclar(PAL["dorado"], PAL["crema"], 0.2), claro)
    return rampa(a, [(0.0, mezclar(VERDE, PAL["oscuro"], 0.3)), (0.35, VERDE), (0.65, MEDIO), (1.0, punta)])


def perfil(u, paradas):
    """Factor de ancho a lo largo de una hoja (paradas: posicion 0..1, factor)."""
    return float(np.interp(u, [p[0] for p in paradas], [p[1] for p in paradas]))


def poner(m: Malla, a, b, c, ca, cb, cc, sombreado=None):
    """Triangulo con una sola normal de sombreado en sus tres esquinas (faceta nitida)."""
    n = np.cross(b - a, c - a)
    largo = float(np.linalg.norm(n))
    if largo < 1e-10:
        return
    n = n / largo
    ns = sombreado(n, (a + b + c) / 3.0) if sombreado is not None else n
    m.tri(a, b, c, ca, cb, cc, normales=[ns, ns, ns])


def sombreado_mata(centro, cara=0.5, arriba=0.65, radial=0.35):
    """Normal de sombreado de una faceta de follaje: la de la cara (vuelta hacia fuera y arriba),
    mas 'arriba' y mas 'hacia fuera del centro de la mata' (da volumen a toda la planta)."""
    centro = np.asarray(centro, float)

    def f(n, c):
        r = c - centro
        r[1] = 0.0
        r = normalizar(r)
        if float(n @ (r + ARRIBA * 0.6)) < 0.0:
            n = -n
        return normalizar(cara * n + arriba * ARRIBA + radial * r)
    return f


def espina_arco(base, d, th0, th1, largo, K, gamma=1.6, sub=8):
    """Espina de K tramos que sale de 'base' con azimut d. El angulo desde la vertical pasa de th0 a th1
    (la hoja se abre y cae hacia la punta). Devuelve K+1 puntos y la normal de la cara de arriba en cada
    uno (perpendicular a la espina, en el plano vertical de d)."""
    d = normalizar(np.array([d[0], 0.0, d[2]]))
    p = np.asarray(base, float).copy()
    puntos, normales = [p.copy()], []
    ds = largo / (K * sub)
    for k in range(K + 1):
        th = th0 + (th1 - th0) * (k / K) ** gamma
        normales.append(-math.cos(th) * d + math.sin(th) * ARRIBA)
        if k == K:
            break
        for j in range(sub):
            uu = (k * sub + j + 0.5) / (K * sub)
            th = th0 + (th1 - th0) * uu ** gamma
            p = p + (math.sin(th) * d + math.cos(th) * ARRIBA) * ds
        puntos.append(p.copy())
    return puntos, normales


def tangente(P, i):
    K = len(P) - 1
    return normalizar(P[min(i + 1, K)] - P[max(i - 1, 0)])


def girar_normales(P, N, rho):
    """Gira la cara de la lamina sobre su eje, cada vez mas hacia la punta (torsion natural)."""
    K = len(P) - 1
    return [rot_eje(tangente(P, i), rho * (0.3 + 0.7 * i / K)) @ n for i, n in enumerate(N)]


def lamina(m: Malla, puntos, anchos, normales, colores, sombreado, pliegue=0.18, mitad=0.88, lado=1,
           nervio=0.0):
    """Hoja o brizna facetada a lo largo de una espina (el ultimo punto es la punta).

    En cada punto hay tres vertices: borde izquierdo, nervio y borde derecho; los bordes bajan
    'pliegue * ancho' respecto del nervio (lomo en V). Dos facetas por tramo y lado; la mitad 'lado'
    (+1 derecha, -1 izquierda) se pinta 'mitad' veces mas oscura. 'nervio' aclara la linea central.
    """
    P = [np.asarray(p, float) for p in puntos]
    K = len(P) - 1
    filas = []
    for i in range(K):
        T = tangente(P, i)
        N = np.asarray(normales[i], float)
        N = normalizar(N - T * float(N @ T))
        S = normalizar(np.cross(T, N))
        w = float(anchos[i])
        caida = N * w * pliegue
        filas.append((P[i] - S * w / 2 - caida, P[i], P[i] + S * w / 2 - caida))
    col = [np.asarray(c, float) for c in colores]
    fi = mitad if lado < 0 else 1.0
    fd = mitad if lado > 0 else 1.0
    for i in range(K):
        L0, M0, R0 = filas[i]
        e0, e1 = col[i], col[i + 1]
        n0, n1 = mezclar(e0, PUNTA_CLARA, nervio), mezclar(e1, PUNTA_CLARA, nervio)
        if i + 1 < K:
            L1, M1, R1 = filas[i + 1]
            poner(m, L0, M0, M1, e0 * fi, n0 * fi, n1 * fi, sombreado)
            poner(m, L0, M1, L1, e0 * fi, n1 * fi, e1 * fi, sombreado)
            poner(m, M0, R0, R1, n0 * fd, e0 * fd, e1 * fd, sombreado)
            poner(m, M0, R1, M1, n0 * fd, e1 * fd, n1 * fd, sombreado)
        else:
            punta = P[K]
            poner(m, L0, M0, punta, e0 * fi, n0 * fi, e1 * fi, sombreado)
            poner(m, M0, R0, punta, n0 * fd, e0 * fd, e1 * fd, sombreado)


def cinta(m: Malla, puntos, anchos, colores, sombreado):
    """Tallo o peciolo fino: dos cintas cruzadas a lo largo de una polilinea (se ve desde cualquier giro)."""
    P = [np.asarray(p, float) for p in puntos]
    for i in range(len(P) - 1):
        T = normalizar(P[i + 1] - P[i])
        ref = ARRIBA if abs(T[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
        u = normalizar(np.cross(T, ref))
        v = normalizar(np.cross(T, u))
        for lado in (u, v):
            a0, a1 = lado * anchos[i] / 2, lado * anchos[i + 1] / 2
            q = [P[i] - a0, P[i] + a0, P[i + 1] + a1, P[i + 1] - a1]
            c0, c1 = colores[i], colores[i + 1]
            poner(m, q[0], q[1], q[2], c0, c0, c1, sombreado)
            poner(m, q[0], q[2], q[3], c0, c1, c1, sombreado)


def raquis(m: Malla, P, N, anchos, colores, sombreado):
    """Eje de la fronde del helecho: cinta plana en el plano de la fronde."""
    for i in range(len(P) - 1):
        S0 = normalizar(np.cross(tangente(P, i), N[i])) * anchos[i] / 2
        S1 = normalizar(np.cross(tangente(P, i + 1), N[i + 1])) * anchos[i + 1] / 2
        poner(m, P[i] - S0, P[i] + S0, P[i + 1] + S1, colores[i], colores[i], colores[i + 1], sombreado)
        poner(m, P[i] - S0, P[i + 1] + S1, P[i + 1] - S1, colores[i], colores[i + 1], colores[i + 1], sombreado)


def muestrear(P, N, s):
    """Punto, tangente y normal de la cara a la fraccion s (0..1) del largo de la polilinea."""
    seg = [float(np.linalg.norm(P[i + 1] - P[i])) for i in range(len(P) - 1)]
    total = sum(seg)
    obj = s * total
    acum = 0.0
    for i, l in enumerate(seg):
        if acum + l >= obj or i == len(seg) - 1:
            t = (obj - acum) / max(l, 1e-9)
            pos = P[i] + (P[i + 1] - P[i]) * t
            T = normalizar(P[i + 1] - P[i])
            n = normalizar(mezclar(N[i], N[i + 1], t))
            return pos, T, n
        acum += l
    return P[-1], tangente(P, len(P) - 1), N[-1]


def pinna(m: Malla, base, d, n, largo, ancho, c0, c1, sombreado, oscura=1, mitad=0.84, pliegue=0.22):
    """Foliolo del helecho: rombo plegado de dos triangulos; la mitad 'oscura' (+1 derecha, -1 izq.)
    se pinta mas oscura."""
    d = normalizar(d)
    n = normalizar(n - d * float(n @ d))
    s = normalizar(np.cross(d, n))
    punta = base + d * largo
    medio = base + d * largo * 0.42
    caida = n * ancho * pliegue
    izq = medio - s * ancho / 2 - caida
    der = medio + s * ancho / 2 - caida
    cm = mezclar(c0, c1, 0.5)
    fi = mitad if oscura < 0 else 1.0
    fd = mitad if oscura > 0 else 1.0
    poner(m, izq, base, punta, cm * fi, c0 * fi, c1 * fi, sombreado)
    poner(m, base, der, punta, c0 * fd, cm * fd, c1 * fd, sombreado)


class _Giro:
    """flor() del nucleo toma su giro de rng.uniform(); este objeto lo fija (capas de petalos alternas)."""

    def __init__(self, angulo):
        self.angulo = angulo

    def uniform(self, *_):
        return self.angulo


def escalar_a(m: Malla, alto):
    """Escala uniforme para que la planta mida exactamente 'alto' (el pie sigue en y = 0)."""
    ymax = max(float(p[:, 1].max()) for p in m.P)
    s = alto / ymax
    m.P = [p * s for p in m.P]
    return m


def apoyar(m: Malla):
    """Nada por debajo del suelo: lo que baja de y = 0 se deja en y = 0."""
    for p in m.P:
        p[:, 1] = np.maximum(p[:, 1], 0.0)
    return m


# ---------- VEG-13 mechones de hierba ----------

PERFIL_BRIZNA = [(0.0, 0.7), (0.25, 1.0), (0.55, 0.9), (0.8, 0.58), (1.0, 0.0)]


def mechon(nombre, alto, n, ancho_rel, K, rng):
    """Mechon en abanico de briznas anchas y plegadas: las del centro erguidas, las del borde abiertas
    y caidas; base oliva oscura y puntas doradas, como los mechones altos del ancla."""
    m = Malla(nombre, "Follaje")
    sombra = sombreado_mata((0.0, alto * 0.15, 0.0), cara=0.5, arriba=0.7, radial=0.35)
    rb = alto * 0.09
    for k in range(n):
        u = (k + 0.5) / n                               # 0 = centro, 1 = borde
        az = k * AUREO + rng.normal(0, 0.2)
        d = horizontal(az)
        base = d * rb * math.sqrt(u) * rng.uniform(0.5, 1.0)
        th0 = math.radians(4 + 36 * u + rng.normal(0, 5))
        th1 = th0 + math.radians(12 + 34 * u + rng.normal(0, 6))
        largo = alto * (1.08 - 0.3 * u) * rng.uniform(0.86, 1.06)
        P, N = espina_arco(base, d, th0, th1, largo, K)
        N = girar_normales(P, N, rng.normal(0, 0.5))
        W = alto * ancho_rel * rng.uniform(0.85, 1.15)
        anchos = [W * perfil(i / K, PERFIL_BRIZNA) for i in range(K)]
        claro = rng.uniform(0.2, 1.0) * (1.0 - 0.3 * u)
        cols = [verde_hierba((0.6 * (i / K) + 0.4 * (P[i][1] / alto)) ** 1.15, claro) for i in range(K + 1)]
        lamina(m, P, anchos, N, cols, sombra, pliegue=0.2, mitad=0.84, lado=rng.choice([-1, 1]),
               nervio=0.1)
    return escalar_a(apoyar(m), alto)


# ---------- VEG-14 flores silvestres ----------

VARIANTES_FLOR = {
    # petalo: color de la punta; interior: arranque del petalo; disco: centro (flor() del nucleo)
    "blanca": dict(n=10, petalos=9, radio=(0.036, 0.046), petalo=BLANCO,
                   interior=mezclar(BLANCO, PAL["dorado"], 0.25),
                   disco=PAL["dorado"], disco_c=PAL["sol"]),
    "rosa": dict(n=8, petalos=6, radio=(0.044, 0.056), petalo=ROSA,
                 interior=mezclar(PAL["coral"], PAL["terracota"], 0.2),
                 disco=PAL["dorado"], disco_c=mezclar(PAL["dorado"], PAL["sol"], 0.5)),
    "amarilla": dict(n=9, petalos=7, radio=(0.04, 0.05), petalo=AMARILLO,
                     interior=mezclar(PAL["dorado"], PAL["sol"], 0.35),
                     disco=PAL["sol"], disco_c=mezclar(PAL["sol"], PAL["terracota"], 0.45)),
}


def corola(m: Malla, centro, n, R, petalos, c_in, c_out, giro, copa=0.18):
    """Corola de petalos redondeados (3 triangulos cada uno), con las puntas algo levantadas en copa.
    El nucleo da flor() con petalos en punta de estrella; las flores del ancla los tienen redondos."""
    n = normalizar(n)
    u, v = marco(n)
    h = math.pi / petalos * 0.92

    def pt(r, a, alza):
        return centro + (u * math.cos(a) + v * math.sin(a)) * r + n * alza

    nn = [n, n, n]
    cm = mezclar(c_in, c_out, 0.6)
    for k in range(petalos):
        a = giro + 2 * math.pi * k / petalos
        s1, s2 = pt(0.6 * R, a - h, copa * R * 0.35), pt(0.6 * R, a + h, copa * R * 0.35)
        t1, t2 = pt(R, a - h * 0.5, copa * R), pt(R, a + h * 0.5, copa * R)
        m.tri(centro, s1, t1, c_in, cm, c_out, normales=nn)
        m.tri(centro, t1, t2, c_in, c_out, c_out, normales=nn)
        m.tri(centro, t2, s2, c_in, c_out, cm, normales=nn)


def mata_flores(nombre, tipo, rng):
    """Roseta de hojitas, unas briznas y 6 a 12 flores sobre tallos finos (unos 0,4 m de diametro)."""
    v = VARIANTES_FLOR[tipo]
    m = Malla(nombre, "Follaje")
    sombra = sombreado_mata((0.0, 0.04, 0.0), cara=0.6, arriba=0.6, radial=0.3)
    # hojitas en roseta baja
    for k in range(12):
        d = horizontal(k * AUREO + rng.normal(0, 0.25))
        largo = rng.uniform(0.09, 0.15)
        th0 = math.radians(rng.uniform(42, 62))
        th1 = th0 + math.radians(rng.uniform(22, 38))
        P, N = espina_arco(d * rng.uniform(0.0, 0.04), d, th0, th1, largo, 2)
        W = largo * rng.uniform(0.36, 0.46)
        cols = [verde(0.0), verde(0.4, 0.2), verde(0.75, 0.5)]
        lamina(m, P, [W * 0.45, W], N, cols, sombra, pliegue=0.2, mitad=0.84, lado=rng.choice([-1, 1]),
               nervio=0.15)
    # briznas sueltas entre los tallos (en el ancla las flores salen del pasto)
    for k in range(6):
        d = horizontal(rng.uniform(0, 2 * math.pi))
        P, N = espina_arco(d * rng.uniform(0.02, 0.08), d, math.radians(rng.uniform(8, 25)),
                           math.radians(rng.uniform(35, 55)), rng.uniform(0.14, 0.22), 3)
        W = rng.uniform(0.018, 0.024)
        cols = [verde_hierba(0.05), verde_hierba(0.4, 0.5), verde_hierba(0.75, 0.7), verde_hierba(1.0, 0.8)]
        lamina(m, P, [W * 0.7, W, W * 0.7], N, cols, sombra, pliegue=0.2, mitad=0.86,
               lado=rng.choice([-1, 1]))
    # flores sobre tallos finos: las del centro mas altas
    n = v["n"]
    for j in range(n):
        uu = (j + 0.5) / n
        d = horizontal(j * AUREO + rng.normal(0, 0.3))
        r = 0.165 * math.sqrt(uu) * rng.uniform(0.8, 1.05)
        alto = 0.27 - 0.13 * (r / 0.165) + rng.normal(0, 0.02)
        centro = d * r + ARRIBA * alto
        pie = d * r * 0.25
        medio = mezclar(pie, centro, 0.5) + d * 0.015
        nrm = normalizar(ARRIBA + d * 0.22 * (r / 0.165) + rng.normal(0, 0.12, 3))
        cinta(m, [pie, medio, centro - nrm * 0.004], [0.009, 0.007, 0.005], [VERDE_BASE, VERDE, VERDE], sombra)
        R = rng.uniform(*v["radio"])
        giro = rng.uniform(0, 2 * math.pi)
        corola(m, centro, nrm, R, v["petalos"], v["interior"], v["petalo"], giro)
        flor(m, centro + nrm * (0.18 * R * 0.35 + 0.004), nrm, R * 0.3, v["disco"], v["disco_c"], 6, _Giro(giro))
    return apoyar(m)


# ---------- VEG-12 helecho ----------

def helecho(nombre, rng, alto=0.8):
    """Frondes que salen empinadas del centro y se arquean hasta caer; foliolos en pares que menguan
    hacia la punta. La mitad de cada foliolo que mira a la base de la fronde va mas oscura."""
    m = Malla(nombre, "Follaje")
    sombra = sombreado_mata((0.0, 0.12, 0.0), cara=0.65, arriba=0.5, radial=0.35)
    nf = 12
    for k in range(nf):
        u = (k + 0.5) / nf                              # 0 = frondes del centro (altas), 1 = las del borde
        d = horizontal(k * AUREO + rng.normal(0, 0.15))
        th0 = math.radians(8 + 40 * u + rng.normal(0, 4))
        th1 = math.radians(72 + 48 * u + rng.normal(0, 6))
        largo = rng.uniform(0.86, 0.98) * (1.0 - 0.2 * u)
        K = 8
        P, N = espina_arco(d * 0.025, d, th0, th1, largo, K, gamma=1.8)
        N = girar_normales(P, N, rng.normal(0, 0.15))
        cols_r = [verde(0.1 + 0.55 * i / K, 0.3) for i in range(K + 1)]
        raquis(m, P, N, [0.016 - 0.011 * i / K for i in range(K + 1)], cols_r, sombra)
        claro = rng.uniform(0.3, 1.0) * (1.0 - 0.4 * u)
        npar = 14
        for j in range(npar):
            s = 0.12 + 0.86 * (j + 0.5) / npar
            pos, T, Nf = muestrear(P, N, s)
            S = normalizar(np.cross(T, Nf))
            lp = largo * 0.19 * float(np.interp(s, [0.1, 0.35, 0.7, 1.0], [0.6, 1.0, 0.7, 0.18]))
            beta = math.radians(28 + 20 * s)
            a = 0.15 + 0.5 * s + 0.35 * float(np.clip(pos[1] / alto, 0, 1)) - 0.15 * u
            c0 = verde(a * 0.6, claro)
            c1 = verde(min(1.0, a + 0.22), claro)
            for lado in (1, -1):
                dirp = normalizar(S * lado * math.cos(beta) + T * math.sin(beta) - Nf * 0.18)
                pinna(m, pos, dirp, Nf, lp, lp * 0.34, c0, c1, sombra, oscura=lado)
    return escalar_a(apoyar(m), alto)


# ---------- hojas grandes (VEG-07 y VEG-10) ----------

def hoja_grande(m: Malla, base, d, th0, th1, largo, ancho, alto_planta, forma, sombra, rng, K=5, claro=0.6,
                rho=0.0, oscura=0.0, pliegue=0.12):
    """Lamina ancha y puntiaguda que se arquea hacia fuera, con nervio claro y dos tonos.
    'oscura' (0..1) la tine de verde frio (hojas bajas e interiores)."""
    P, N = espina_arco(base, d, th0, th1, largo, K, gamma=1.4)
    N = girar_normales(P, N, rho)
    anchos = [ancho * perfil(i / K, forma) for i in range(K)]
    cols = []
    for i in range(K + 1):
        a = 0.45 * (i / K) ** 1.2 + 0.55 * float(np.clip(P[i][1] / alto_planta, 0, 1))
        cols.append(mezclar(verde(a, claro), VERDE_FRIO, oscura))
    lamina(m, P, anchos, N, cols, sombra, pliegue=pliegue, mitad=0.84, lado=rng.choice([-1, 1]), nervio=0.3)
    return P


FORMA_LANZA = [(0.0, 0.12), (0.18, 0.7), (0.4, 1.0), (0.62, 0.9), (0.82, 0.5), (1.0, 0.0)]
FORMA_OVAL = [(0.0, 0.32), (0.17, 0.85), (0.38, 1.0), (0.6, 0.88), (0.8, 0.5), (0.92, 0.24), (1.0, 0.0)]


def flor_ave(m: Malla, base, alto, d, rng, sombra, escala=1.0):
    """Flor del ave del paraiso como la del ancla: tallo, espata en barca y una corona de lanzas
    naranja que se abre hacia arriba como una llama (coral en la base, sol, punta dorada)."""
    d = normalizar(d)
    lat = normalizar(np.cross(ARRIBA, d))
    top = base + ARRIBA * alto + d * 0.05
    medio = base + ARRIBA * alto * 0.5 + d * 0.012
    cinta(m, [base, medio, top], [0.024, 0.019, 0.015], [VERDE_BASE, VERDE, OLIVA], sombra)
    # espata: barca alargada que apunta hacia fuera y algo arriba
    esp = normalizar(d + ARRIBA * 0.3)
    e = escala
    P = [top - esp * 0.03 * e, top + esp * 0.07 * e, top + esp * 0.17 * e, top + esp * 0.25 * e]
    cols = [VERDE, mezclar(PAL["terracota"], PAL["coral"], 0.4), PAL["coral"], mezclar(PAL["coral"], NARANJA, 0.4)]
    lamina(m, P, [0.03 * e, 0.045 * e, 0.032 * e], [ARRIBA] * 4, cols, sombra, pliegue=-0.3, mitad=0.8, lado=1)
    # corona de lanzas en abanico, mas larga en el centro
    origen = top + esp * 0.07 * e + ARRIBA * 0.015 * e
    n_lanzas = 7
    for k in range(n_lanzas):
        f = k / (n_lanzas - 1) - 0.5                       # -0.5 .. 0.5 a lo ancho del abanico
        elev = math.radians(rng.uniform(55, 80) - 30 * abs(f))
        azim = f * math.radians(200) + rng.normal(0, 0.1)
        horiz = normalizar(d * math.cos(azim) + lat * math.sin(azim))
        dl = normalizar(horiz * math.cos(elev) + ARRIBA * math.sin(elev))
        largo = rng.uniform(0.17, 0.22) * (1.0 - 0.35 * abs(f)) * e
        # la lanza se curva un poco hacia fuera
        p1 = origen + dl * largo * 0.5
        p2 = origen + normalizar(dl + horiz * 0.35) * largo
        nl = normalizar(np.cross(dl, normalizar(np.cross(ARRIBA, dl) + lat * 1e-3)))
        if float(nl @ ARRIBA) < 0:
            nl = -nl
        cols = [mezclar(PAL["coral"], PAL["terracota"], 0.3), mezclar(NARANJA, PAL["coral"], 0.25),
                mezclar(NARANJA, PAL["dorado"], 0.45)]
        lamina(m, [origen, p1, p2], [0.024 * e, 0.042 * e], [nl, nl], cols, sombra, pliegue=0.22, mitad=0.8,
               lado=1 if f >= 0 else -1, nervio=0.0)


def ave_del_paraiso(nombre, rng, alto=0.9):
    """VEG-07: mata densa de hojas largas y anchas en abanico, arqueadas, y dos flores naranja encima."""
    m = Malla(nombre, "Follaje")
    sombra = sombreado_mata((0.0, 0.25, 0.0), cara=0.7, arriba=0.45, radial=0.35)
    nh = 12
    for k in range(nh):
        u = (k + 0.5) / nh                              # 0 = hojas del centro (altas), 1 = las del borde
        d = horizontal(k * AUREO + rng.normal(0, 0.2))
        th_pec = math.radians(6 + 30 * u + rng.normal(0, 4))
        alto_pec = rng.uniform(0.12, 0.26) * (1.15 - 0.6 * u)
        base = d * 0.03
        fin = base + (math.sin(th_pec) * d + math.cos(th_pec) * ARRIBA) * alto_pec
        cinta(m, [base, fin], [0.026, 0.018], [VERDE_BASE, VERDE], sombra)
        largo = rng.uniform(0.44, 0.56) * (1.0 - 0.15 * u)
        th0 = th_pec + math.radians(4 + 22 * u)
        th1 = th0 + math.radians(36 + 40 * u + rng.normal(0, 6))
        hoja_grande(m, fin, d, th0, th1, largo, largo * rng.uniform(0.3, 0.36), alto, FORMA_LANZA, sombra,
                    rng, claro=rng.uniform(0.4, 1.0) * (1 - 0.4 * u), rho=rng.normal(0, 0.25),
                    oscura=0.45 * max(0.0, u - 0.5) * 2)
    d0 = horizontal(rng.uniform(0, 2 * math.pi))
    flor_ave(m, d0 * 0.02, 0.66, d0, rng, sombra)
    d1 = horizontal(math.atan2(d0[2], d0[0]) + math.radians(150))
    flor_ave(m, d1 * 0.04, 0.5, d1, rng, sombra, escala=0.85)
    return escalar_a(apoyar(m), alto)


def hojas_anchas(nombre, rng, alto=0.9):
    """VEG-10: roseta densa en cupula de hojas anchas y puntiagudas: las de arriba erguidas y claras,
    las de abajo abiertas, caidas y mas oscuras."""
    m = Malla(nombre, "Follaje")
    sombra = sombreado_mata((0.0, 0.25, 0.0), cara=0.7, arriba=0.45, radial=0.35)
    capas = [  # (hojas, alto del peciolo, angulo de la hoja desde la vertical, caida, largo, tinte frio)
        (8, (0.03, 0.09), (62, 76), (30, 42), (0.3, 0.36), 0.45),
        (7, (0.2, 0.3), (36, 50), (28, 40), (0.33, 0.39), 0.15),
        (5, (0.4, 0.5), (14, 26), (24, 34), (0.32, 0.37), 0.0),
    ]
    k_total = 0
    for n, (h0, h1), (a0, a1), (c0, c1), (l0, l1), frio in capas:
        for k in range(n):
            d = horizontal(k_total * AUREO + rng.normal(0, 0.15))
            k_total += 1
            th = rng.uniform(a0, a1)
            th_pec = math.radians(th * 0.45)
            alto_pec = rng.uniform(h0, h1)
            base = d * 0.025
            fin = base + (math.sin(th_pec) * d + math.cos(th_pec) * ARRIBA) * alto_pec
            cinta(m, [base, fin], [0.022, 0.015], [VERDE_BASE, VERDE], sombra)
            largo = rng.uniform(l0, l1)
            th0 = math.radians(th)
            th1 = th0 + math.radians(rng.uniform(c0, c1))
            hoja_grande(m, fin, d, th0, th1, largo, largo * rng.uniform(0.48, 0.54), alto, FORMA_OVAL, sombra,
                        rng, K=6, claro=rng.uniform(0.5, 1.0), rho=rng.normal(0, 0.2), oscura=frio, pliegue=0.1)
    return escalar_a(apoyar(m), alto)


# ---------- revision ----------

def silueta_escala():
    """Silueta gris del estudiante (1,05 m, 3 cabezas) para las laminas de revision."""
    rng = np.random.default_rng(1)
    gris = PAL["piedra_clara"]
    m = Malla("silueta", "Facetado")
    cuerpo = fibonacci(16) * np.array([0.17, 0.33, 0.12]) + np.array([0.0, 0.33, 0.0])
    cuerpo[:, 1] = np.maximum(cuerpo[:, 1], 0.0)
    m.anexar(solido_facetado("cuerpo", cuerpo, mezclar(gris, PAL["petroleo"], 0.4), gris, gris, rng, var=0.0))
    cabeza = fibonacci(14) * 0.2 + np.array([0.0, 0.85, 0.0])
    m.anexar(solido_facetado("cabeza", cabeza, mezclar(gris, PAL["petroleo"], 0.4), gris, gris, rng, var=0.0))
    return m


def medidas(m: Malla):
    lo, hi = m.caja_limites()
    return [round(float(v), 3) for v in (hi - lo)]


def escribir(ruta, piezas):
    """piezas: lista de (nombre, malla, (x, z)). Devuelve triangulos y tamano por nodo."""
    e = Escena(GENERADOR)
    info = {}
    for nombre, malla, (x, z) in piezas:
        e.nodo(nombre, e.malla(malla, nombre=nombre), t=(x, 0.0, z))
        info[nombre] = {"triangulos": e.stats[nombre], "tamano_xyz_m": medidas(malla)}
    e.guardar(ruta)
    return info


def main():
    ap = argparse.ArgumentParser(description="Plantas bajas y flores (VEG-07, 10, 12, 13 y 14)")
    ap.add_argument("--vistas", help="carpeta para las copias de revision (no van al juego)")
    args = ap.parse_args()

    def r(semilla):
        return np.random.default_rng(semilla)

    recursos = {
        "VEG-13": [("VEG-13_p", mechon("VEG-13_p", 0.25, 12, 0.14, 3, r(131))),
                   ("VEG-13_m", mechon("VEG-13_m", 0.40, 18, 0.12, 3, r(132))),
                   ("VEG-13_g", mechon("VEG-13_g", 0.60, 26, 0.105, 4, r(133)))],
        "VEG-14": [("VEG-14_blanca", mata_flores("VEG-14_blanca", "blanca", r(141))),
                   ("VEG-14_rosa", mata_flores("VEG-14_rosa", "rosa", r(142))),
                   ("VEG-14_amarilla", mata_flores("VEG-14_amarilla", "amarilla", r(143)))],
        "VEG-12": [("VEG-12_helecho", helecho("VEG-12_helecho", r(121)))],
        "VEG-07": [("VEG-07_ave_del_paraiso", ave_del_paraiso("VEG-07_ave_del_paraiso", r(71)))],
        "VEG-10": [("VEG-10_hojas_anchas", hojas_anchas("VEG-10_hojas_anchas", r(101)))],
    }
    informe = {}
    for ident, variantes in recursos.items():
        informe[ident] = escribir(SALIDA / f"{ident}.glb", [(n, m, (0.0, 0.0)) for n, m in variantes])

    if args.vistas:
        carpeta = Path(args.vistas)
        carpeta.mkdir(parents=True, exist_ok=True)
        for ident in ("VEG-13", "VEG-14"):
            piezas, x = [], 0.0
            for n, m in recursos[ident]:
                ancho = medidas(m)[0]
                piezas.append((n, m, (x + ancho / 2, 0.0)))
                x += ancho + 0.12
            escribir(carpeta / f"{ident}_vista.glb", piezas)
        # lamina de conjunto: fila de atras las plantas grandes, delante hierba y flores, y la silueta
        fila_atras = [("silueta", silueta_escala())] + [(n, m) for i in ("VEG-12", "VEG-07", "VEG-10")
                                                          for n, m in recursos[i]]
        fila_delante = [(n, m) for i in ("VEG-13", "VEG-14") for n, m in recursos[i]]
        piezas = []
        for fila, z in ((fila_atras, -0.8), (fila_delante, 0.45)):
            anchos = [medidas(m)[0] for _, m in fila]
            x = -(sum(anchos) + 0.15 * (len(fila) - 1)) / 2
            for (n, m), a in zip(fila, anchos):
                piezas.append((n, m, (x + a / 2, z)))
                x += a + 0.15
        escribir(carpeta / "lamina_vista.glb", piezas)

    print(json.dumps(informe, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
