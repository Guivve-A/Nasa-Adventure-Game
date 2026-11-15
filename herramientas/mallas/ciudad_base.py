"""Ayudas comunes de los generadores de la zona «ciudad» (la Plaza de las Iguanas).

Las usan ciudad_mobiliario.py (familia URB y ARQ-08/09/10) y ciudad_arquitectura.py (casas, biblioteca y
suelo). Reutiliza el nucleo y las ayudas de estructuras_piedra_madera.py (prisma, poligono, mosaico...).

Convenciones: metros, +Y arriba, el frente de cada objeto mira a +Z (hacia la camara de juego), el origen
va en el centro de su base y todo apoya en y = 0. Solo colores de la paleta maestra y sus mezclas; el cian
queda para la tecnologia (la luz de la puerta de la biblioteca y la traza del osciloscopio).

Los GLB salen en juego/modelos/ciudad/<ID>.glb.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, RAIZ, Escena, Malla, flor, hoja, mezclar, tubo  # noqa: E402,F401
from estructuras_piedra_madera import (AZUL_T, LECHADA, METAL, METAL_BRILLO, MOLDURA, PIEDRA,  # noqa: E402,F401
                                       PIEDRA_TECHO, TABLON, VETAS, cuerda, encoger, grad, mosaico, piramide,
                                       poligono, prisma, rect, rect_c, tono)

SALIDA = RAIZ / "juego" / "modelos" / "ciudad"
ARRIBA = np.array([0.0, 1.0, 0.0])
FRENTE = np.array([0.0, 0.0, 1.0])
INCLINACION = 0.45   # cizalla 2.5D de los shaders (D-015); ver presesgar()


def t3(base, s=0.30, l=0.30):
    """Tres tonos pintados a partir de un color: sombra azul petroleo, base y luz crema."""
    base = np.asarray(base, float)
    return tono(mezclar(base, PAL["petroleo"], s), base, mezclar(base, PAL["crema"], l))


# ---------- tonos de la plaza ----------
AMARILLO = t3(mezclar(PAL["dorado"], PAL["crema"], 0.42), 0.26, 0.35)
AZUL = t3(mezclar(AZUL_T, PAL["piedra_clara"], 0.38), 0.25, 0.30)
CORAL = t3(mezclar(PAL["coral"], PAL["tierra1"], 0.50), 0.28, 0.30)
CREMA = t3(mezclar(PAL["crema"], PAL["piedra_clara"], 0.22), 0.30, 0.15)
ROSA = t3(mezclar(mezclar(PAL["coral"], PAL["crema"], 0.50), PAL["piedra_clara"], 0.18), 0.26, 0.25)
VERDE = t3(mezclar(mezclar(PAL["petroleo"], PAL["hierba_sol"], 0.40), PAL["crema"], 0.35), 0.25, 0.30)
MARFIL = t3(mezclar(mezclar(PAL["crema"], PAL["brillo"], 0.16), PAL["piedra_clara"], 0.10), 0.17, 0.10)   # biblioteca: cal calida
TEJAS = [mezclar(PAL["terracota"], PAL["coral"], 0.35), mezclar(PAL["terracota"], PAL["coral"], 0.60),
         mezclar(PAL["terracota"], PAL["sol"], 0.40), mezclar(PAL["terracota"], PAL["tierra2"], 0.40)]
TEJA_SOMBRA = mezclar(PAL["terracota"], PAL["madera2"], 0.45)
ZINC = [mezclar(PAL["piedra_clara"], PAL["petroleo"], 0.25), mezclar(PAL["piedra_clara"], PAL["tierra1"], 0.30),
        mezclar(PAL["terracota"], PAL["piedra"], 0.45), PAL["piedra"]]
MADERA = tono(PAL["madera1"], mezclar(PAL["madera1"], PAL["tierra2"], 0.6), mezclar(PAL["tierra2"], PAL["tierra1"], 0.45))
MADERA_SOL = tono(mezclar(PAL["madera1"], PAL["tierra2"], 0.5), mezclar(PAL["tierra2"], PAL["sol"], 0.25),
                  mezclar(PAL["tierra1"], PAL["sol"], 0.35))
PUERTA = t3(mezclar(PAL["petroleo"], PAL["hierba_sombra"], 0.22), 0.25, 0.22)   # verde azulado de las hojas
PERSIANA = t3(mezclar(AZUL_T, PAL["hierba_sombra"], 0.18), 0.25, 0.25)
VIDRIO = mezclar(PAL["petroleo"], PAL["oscuro"], 0.40)
VIDRIO_LUZ = mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.55)
HIERRO = tono(mezclar(PAL["oscuro"], PAL["petroleo"], 0.25), mezclar(PAL["piedra_osc"], PAL["petroleo"], 0.30),
              mezclar(PAL["piedra_osc"], PAL["piedra_clara"], 0.35))
HIERRO_VERDE = t3(mezclar(PAL["petroleo"], PAL["hierba_sombra"], 0.30), 0.30, 0.20)   # hierro pintado (banca, aros)
BARRO = t3(mezclar(PAL["terracota"], PAL["sol"], 0.30), 0.30, 0.25)             # macetas
TIERRA = mezclar(PAL["madera2"], PAL["tierra2"], 0.35)
TELA_SOL = mezclar(PAL["sol"], PAL["coral"], 0.35)
TELA_CREMA = mezclar(PAL["crema"], PAL["brillo"], 0.25)
TELA_AZUL = mezclar(PAL["petroleo"], AZUL_T, 0.55)
HOJA_OSC = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.25)
HOJA_CLARA = mezclar(PAL["hierba_sol"], PAL["dorado"], 0.35)
FLOR_ROSA = mezclar(mezclar(PAL["coral"], PAL["crema"], 0.30), PAL["piedra_clara"], 0.12)
FLOR_ROJA = mezclar(PAL["coral"], PAL["terracota"], 0.15)
FLOR_AMARILLA = mezclar(PAL["dorado"], PAL["crema"], 0.25)


# ---------- geometria ----------

def poli(cx, cz, r, n, giro=0.0, ex=1.0, ez=1.0):
    """Planta de n lados, antihoraria vista desde arriba (como rect())."""
    return [(cx + r * ex * math.cos(giro + 2 * math.pi * (i + 0.5) / n),
             cz - r * ez * math.sin(giro + 2 * math.pi * (i + 0.5) / n)) for i in range(n)]


def caja(m, x0, x1, y0, y1, z0, z1, tn, rng, techo="tono", bisel=0.0, ymin=None, ymax=None, var=0.04):
    """Bloque recto pintado (sin base). techo: "tono" = luz del tono, color, funcion o None."""
    techo = tn[2] if isinstance(techo, str) else techo
    p = rect(min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1))
    return prisma(m, p, p, y0, y1, tn, techo, rng, bisel=bisel, ymin=ymin, ymax=ymax, var=var)


def cilindro(m, cx, cz, r0, r1, y0, y1, n, tn, rng, techo="tono", giro=0.0, ymin=None, ymax=None, var=0.04,
             bisel=0.0, abanico=False):
    """Cilindro o tronco de cono facetado de n lados."""
    techo = tn[2] if isinstance(techo, str) else techo
    return prisma(m, poli(cx, cz, r0, n, giro), poli(cx, cz, r1, n, giro), y0, y1, tn, techo, rng, bisel=bisel,
                  ymin=ymin, ymax=ymax, var=var, abanico=abanico)


def cono(m, cx, cz, r, y0, y1, n, tn, rng, giro=0.0):
    base = [np.array([x, y0, z]) for x, z in poli(cx, cz, r, n, giro)]
    piramide(m, base, (cx, y1, cz), tn, rng)


def barra(m, puntos, radio, tn, rng, lados=5, tapa=True):
    """Barra o tubo de metal o madera a lo largo de una polilinea (sin ruido)."""
    radios = [radio] * len(puntos) if np.isscalar(radio) else radio
    tubo(m, puntos, radios, lados, tn[1], tn[2] if abs(puntos[-1][1] - puntos[0][1]) > 0.05 else tn[1], rng,
         ruido=0.0, tapa=tapa)


def extruir(m, pts, z0, z1, tn, rng, ymin=None, ymax=None, frente=None, var=0.04, cantos=True):
    """Relieve de fachada: poligono convexo [(x, y)...] con la cara frontal en z1 (mira a +Z) y cantos
    entre z0 y z1. 'frente' fija el color de la cara; si no, degradado vertical del tono."""
    ys = [p[1] for p in pts]
    ymin = min(ys) if ymin is None else ymin
    ymax = max(ys) if ymax is None else ymax

    def col(y):
        return grad((y - ymin) / max(ymax - ymin, 1e-9), tn)

    vf = 1 + rng.normal(0, var)
    cara = [np.array([x, y, z1]) for x, y in pts]
    poligono(m, cara, [(col(p[1]) if frente is None else np.asarray(frente, float)) * vf for p in cara], FRENTE)
    if not cantos or abs(z1 - z0) < 1e-6:
        return
    cen = np.mean(np.array(pts, float), axis=0)
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        q = [np.array([a[0], a[1], z0]), np.array([b[0], b[1], z0]), np.array([b[0], b[1], z1]),
             np.array([a[0], a[1], z1])]
        medio = (np.array(a, float) + np.array(b, float)) / 2 - cen
        fuera = np.array([medio[0], medio[1], 0.0])
        claro = 0.35 if fuera[1] > abs(fuera[0]) * 0.5 else (-0.12 if fuera[1] < -abs(fuera[0]) * 0.5 else 0.0)
        cols = []
        for p in q:
            c = col(p[1])
            c = mezclar(c, tn[2], claro) if claro > 0 else c * (1 + claro)
            cols.append(c * vf)
        poligono(m, q, cols, fuera)


def panel(m, x0, x1, y0, y1, z, col_bajo, col_alto=None, rng=None, var=0.03):
    """Rectangulo plano de fachada (mira a +Z) con degradado vertical."""
    col_alto = col_bajo if col_alto is None else col_alto
    vf = 1 + (rng.normal(0, var) if rng is not None else 0.0)
    cb, ca = np.asarray(col_bajo, float) * vf, np.asarray(col_alto, float) * vf
    poligono(m, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [cb, cb, ca, ca], FRENTE)


def tejado(m, p0, p1, p2, p3, rng, colores=None, paso=0.36, ancho=0.30, resalte=0.035, sombra=None):
    """Faldon de tejas entre el alero p0-p1 (abajo) y la cumbrera p3-p2 (arriba); p0, p1, p2, p3 en sentido
    antihorario visto desde fuera. Vale para trapecios y triangulos (p2 = p3). Cada hilada monta sobre la de
    abajo: su borde bajo se levanta 'resalte' y deja una contrahuella oscura."""
    colores = TEJAS if colores is None else colores
    sombra = TEJA_SOMBRA if sombra is None else sombra
    p0, p1, p2, p3 = (np.asarray(p, float) for p in (p0, p1, p2, p3))
    n = np.cross(p1 - p0, p3 - p0)
    if np.linalg.norm(n) < 1e-9:
        n = np.cross(p1 - p0, p2 - p0)
    n = n / np.linalg.norm(n)
    largo = max(np.linalg.norm((p3 + p2) / 2 - (p0 + p1) / 2), 1e-6)
    hiladas = max(1, int(round(largo / paso)))
    for k in range(hiladas):
        t0, t1 = k / hiladas, (k + 1) / hiladas
        a0, b0 = p0 + (p3 - p0) * t0, p1 + (p2 - p1) * t0
        a1, b1 = p0 + (p3 - p0) * t1, p1 + (p2 - p1) * t1
        ancho_h = np.linalg.norm(b0 - a0)
        cols = max(1, int(round(ancho_h / ancho)))
        desfase = 0.5 if k % 2 else 0.0
        cortes = [0.0] + [min(1.0, (j + desfase) / cols) for j in range(1, cols + (1 if desfase else 0))] + [1.0]
        cortes = sorted(set(cortes))
        for u0, u1 in zip(cortes[:-1], cortes[1:]):
            if u1 - u0 < 1e-4:
                continue
            c = np.asarray(colores[rng.integers(len(colores))], float) * (1 + rng.normal(0, 0.05))
            q0, q1 = a0 + (b0 - a0) * u0 + n * resalte, a0 + (b0 - a0) * u1 + n * resalte
            q2, q3 = a1 + (b1 - a1) * u1, a1 + (b1 - a1) * u0
            poligono(m, [q0, q1, q2, q3], [c * 0.84, c * 0.84, mezclar(c, PAL["crema"], 0.16),
                                            mezclar(c, PAL["crema"], 0.16)], n)
        # contrahuella de la hilada (mira alero abajo)
        poligono(m, [a0, b0, b0 + n * resalte, a0 + n * resalte], [sombra] * 4, (p0 + p1) / 2 - (p3 + p2) / 2)


def chapas(m, p0, p1, p2, p3, rng, ancho=0.55):
    """ARQ-03: faldon de chapas de zinc onduladas, unas grises y otras con oxido; cada chapa en dos tiras
    con una arista levantada (la onda)."""
    p0, p1, p2, p3 = (np.asarray(p, float) for p in (p0, p1, p2, p3))
    n = np.cross(p1 - p0, p3 - p0)
    n = n / np.linalg.norm(n)
    cols = max(1, int(round(np.linalg.norm(p1 - p0) / ancho)))
    for j in range(cols):
        c = np.asarray(ZINC[rng.integers(len(ZINC))], float) * (1 + rng.normal(0, 0.05))
        partes = 3
        for s in range(partes):
            u0, u1 = (j + s / partes) / cols, (j + (s + 1) / partes) / cols
            um = (u0 + u1) / 2
            a0, a1 = p0 + (p1 - p0) * u0, p3 + (p2 - p3) * u0
            b0, b1 = p0 + (p1 - p0) * u1, p3 + (p2 - p3) * u1
            c0, c1 = p0 + (p1 - p0) * um + n * 0.03, p3 + (p2 - p3) * um + n * 0.03
            claro, oscuro = mezclar(c, PAL["crema"], 0.18), c * 0.86
            poligono(m, [a0, c0, c1, a1], [claro * 0.92, claro * 0.92, claro, claro], n)
            poligono(m, [c0, b0, b1, c1], [oscuro * 0.92, oscuro * 0.92, oscuro, oscuro], n)


def planta_suelta(f, base, rng, alto=0.45, hojas=9, flores=0, col_flor=None, abierta=0.9):
    """Mata sencilla de hojas en rombo (y flores) para macetas, jardineras y enredaderas. Material Follaje."""
    base = np.asarray(base, float)
    for i in range(hojas):
        ang = 2 * math.pi * i / hojas + rng.uniform(-0.3, 0.3)
        inc = rng.uniform(0.25, abierta)
        d = np.array([math.cos(ang) * inc, 1.0 - inc * 0.55, math.sin(ang) * inc])
        nrm = np.array([-math.cos(ang) * 0.6, 0.8, -math.sin(ang) * 0.6])
        largo = alto * rng.uniform(0.75, 1.15)
        hoja(f, base, d, nrm, largo, largo * rng.uniform(0.30, 0.42), HOJA_OSC * (1 + rng.normal(0, 0.06)),
             mezclar(PAL["hierba_sol"], HOJA_CLARA, rng.uniform(0.0, 1.0)))
    for _ in range(flores):
        ang = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.25, 0.75) * alto * 0.7
        c = base + np.array([math.cos(ang) * r, alto * rng.uniform(0.55, 0.95), math.sin(ang) * r])
        col = FLOR_ROSA if col_flor is None else col_flor
        flor(f, c, np.array([math.cos(ang) * 0.4, 0.8, 0.45]), alto * rng.uniform(0.14, 0.2), col * (1 + rng.normal(0, 0.05)),
             FLOR_AMARILLA, 5, rng)


def enredadera(f, puntos, rng, densidad=14, ancho=0.28, col_flor=None, flores=0.45):
    """Buganvilla o hiedra pegada a una fachada (que mira a +Z): hojas y flores a lo largo de una polilinea."""
    puntos = [np.asarray(p, float) for p in puntos]
    for a, b in zip(puntos[:-1], puntos[1:]):
        pasos = max(2, int(np.linalg.norm(b - a) * densidad))
        for k in range(pasos):
            p = a + (b - a) * (k / pasos) + np.array([rng.uniform(-ancho, ancho), rng.uniform(-ancho, ancho) * 0.6,
                                                     rng.uniform(0.02, 0.10)])
            if rng.random() < flores:
                col = FLOR_ROSA if col_flor is None else col_flor
                flor(f, p + np.array([0, 0, 0.03]), np.array([rng.uniform(-0.3, 0.3), 0.45, 0.85]), rng.uniform(0.07, 0.11),
                     col * (1 + rng.normal(0, 0.06)), mezclar(col, PAL["crema"], 0.5), 5, rng)
            else:
                ang = rng.uniform(0, 2 * math.pi)
                d = np.array([math.cos(ang), math.sin(ang) - 0.4, 0.25])
                hoja(f, p, d, np.array([0.0, 0.5, 0.85]), rng.uniform(0.12, 0.2), rng.uniform(0.07, 0.11),
                     HOJA_OSC * (1 + rng.normal(0, 0.06)), mezclar(PAL["hierba_sol"], HOJA_CLARA, rng.uniform(0, 1)))


def presesgar(m: Malla, k=INCLINACION):
    """El material "Emisivo" no pasa por los shaders del proyecto y no recibe la inclinacion 2.5D
    (z -= k * y). Para que el brillo caiga donde se ve el objeto, sus vertices se guardan ya inclinados.
    Solo vale si el objeto se coloca sin giro y apoyado en y = 0."""
    for P in m.P:
        P[:, 2] -= k * P[:, 1]
    return m


def guardar(archivo, nodos, generador):
    """nodos: [(nombre_del_nodo, [mallas])]. Escribe juego/modelos/ciudad/<archivo>.glb e informa."""
    e = Escena(generador)
    total = 0
    lo, hi = np.full(3, 1e9), np.full(3, -1e9)
    for nombre, mallas in nodos:
        mallas = [x for x in mallas if len(x)]
        e.nodo(nombre, e.malla(*mallas, nombre=nombre))
        for x in mallas:
            total += len(x)
            a, b = x.caja_limites()
            lo, hi = np.minimum(lo, a), np.maximum(hi, b)
    ruta = e.guardar(SALIDA / f"{archivo}.glb")
    print(f"{archivo}: {total} triangulos, x [{lo[0]:+.2f}, {hi[0]:+.2f}] y [{lo[1]:+.2f}, {hi[1]:+.2f}] "
          f"z [{lo[2]:+.2f}, {hi[2]:+.2f}] -> {ruta.relative_to(RAIZ)}")
    return total
