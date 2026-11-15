"""Modelos de la habitacion-taller (zona "habitacion"), pintados por script con el nucleo comun.

Concepto validado por Guillermo: Nasa_Game/Fase_1_Arte/Exploracion/Lote_05/L05_A_manana_calida_final.png
(borrador A «Manana calida»). Hoja de los objetos del taller: HR_TAL_v1.png.

Escribe un .glb por recurso en juego/modelos/habitacion/:
  Catalogo TAL: TAL-01 banco, TAL-02 osciloscopio, TAL-06 placa, TAL-07 caja de herramientas, TAL-09 lampara,
                TAL-10 taburete, TAL-12 libros, TAL-14 telescopio pequeno.
  Nuevos TAL:   TAL-15 seguidor lunar, TAL-16 cuaderno abierto, TAL-17 vaso con lapices.
  Familia HAB:  HAB-01 cama, HAB-02 ventana con postigos, HAB-03 alfombra, HAB-04 repisa, HAB-05 poster del
                observatorio, HAB-06 caja de carton, HAB-07 baranda con puerta, HAB-08 felpudo, HAB-09 escalera
                con arco, HAB-10 esfera armilar, HAB-11 farol, HAB-12 paredes y suelo, HAB-13 casas del fondo,
                HAB-14 buganvilla, HAB-15 maceta colgante, HAB-16 macetero, HAB-17 cuadrito, HAB-12n el cuarto de noche (sin haces de sol).

Convenciones: metros, +Y arriba. HAB-12, HAB-13 y HAB-09 van en coordenadas del cuarto (origen en el centro
del suelo; pared del fondo en z = -AZ, pared derecha en x = +AX). Los muebles tienen el origen en el centro
de su base y el frente hacia +Z. Lo que cuelga de una pared tiene z = 0 en la cara de la pared y +Z hacia
el cuarto. Solo colores de la paleta maestra y sus mezclas; el cian solo en la traza y los LED (Emisivo).

Uso, desde la raiz del proyecto:  python -I herramientas/mallas/habitacion_modelos.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402

from nucleo import (PAL, RAIZ, Escena, Malla, fibonacci, flor, hoja, marco, mezclar, rot_eje, rot_y,  # noqa: E402
                    solido_facetado)

SALIDA = RAIZ / "juego" / "modelos" / "habitacion"
GENERADOR = "herramientas/mallas/habitacion_modelos.py"
RNG = np.random.default_rng(20261114)
C = PAL

# ---------- medidas del cuarto (las mismas que usa juego/zonas/habitacion/habitacion.gd) ----------
AX, AZ = 3.3, 2.7            # semiancho y semifondo del suelo
ALTO = 2.3                   # alto de las paredes
G = 0.25                     # grosor de las paredes
VX = 0.1                     # centro de la ventana (pared del fondo)
V_ANCHO, V_BASE, V_RECTO, V_ARCO = 1.3, 0.85, 1.62, 0.40
PARED_DER_FIN = 0.9          # la pared derecha llega hasta este z; despues viene la baranda
BAJO = -0.6                  # hasta donde bajan las caras de fuera

# ---------- colores: mezclas de la paleta maestra ----------
MAD = mezclar(C["madera1"], C["terracota"], 0.40)
MAD_CLARA = mezclar(C["madera1"], C["sol"], 0.42)
MAD_OSC = mezclar(C["madera2"], C["terracota"], 0.25)
PARED = mezclar(C["tierra2"], C["sol"], 0.38)
PARED_BAJA = mezclar(C["tierra2"], C["terracota"], 0.55)
PARED_ALTA = mezclar(C["tierra2"], C["petroleo"], 0.22)
CORTE = mezclar(C["piedra"], C["tierra1"], 0.45)       # v2: corte de casa de munecas calido (antes gris azulado)
EXTERIOR = mezclar(C["petroleo"], C["piedra_osc"], 0.45)
LUZ = mezclar(C["sol"], C["crema"], 0.55)
PIEDRA_CALIDA = mezclar(C["piedra_clara"], C["crema"], 0.55)
BLANCO = mezclar(C["crema"], C["brillo"], 0.55)
SABANA = mezclar(BLANCO, C["piedra_clara"], 0.25)
AZUL = mezclar(C["petroleo"], C["piedra_clara"], 0.22)
AZUL_OSC = mezclar(C["petroleo"], C["oscuro"], 0.25)
VERDE_AZUL = mezclar(mezclar(C["petroleo"], C["cian_medio"], 0.35), C["piedra_clara"], 0.12)
METAL = mezclar(C["piedra_clara"], C["piedra"], 0.35)
HIERRO = mezclar(C["piedra_osc"], C["oscuro"], 0.35)
CARTON = mezclar(C["tierra1"], C["crema"], 0.25)
TEJA = mezclar(C["terracota"], C["coral"], 0.30)
HOJA_OSC = mezclar(C["hierba_sombra"], C["oscuro"], 0.30)
HOJA = mezclar(mezclar(C["hierba_sombra"], C["petroleo"], 0.22), C["hierba_sol"], 0.25)   # verde, menos amarillo
HOJA_CLARA = mezclar(C["hierba_sol"], C["hierba_sombra"], 0.30)
FLOR = mezclar(C["coral"], C["brillo"], 0.10)
FLOR_CLARA = mezclar(C["coral"], C["crema"], 0.40)
ARRIBA = np.array([0.0, 1.0, 0.0])


# ---------- ayudas de geometria ----------

def jit(col, var=0.04):
    return np.clip(np.asarray(col, float) * (1.0 + RNG.normal(0, var)), 0, 1)


def cara(m, pts, hacia, col):
    """Poligono plano y convexo, orientado hacia 'hacia'. 'col' es un color o una funcion punto -> color."""
    pts = [np.asarray(p, float) for p in pts]
    n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    if n @ np.asarray(hacia, float) < 0:
        pts = pts[::-1]
    cols = [np.clip(col(p), 0, 1) if callable(col) else col for p in pts]
    for i in range(1, len(pts) - 1):
        m.tri(pts[0], pts[i], pts[i + 1], cols[0], cols[i], cols[i + 1])


def caja(m, c, t, col, R=None, tapa=None, sombra=0.28, luz=0.06, var=0.035, base=False):
    """Caja centrada en c, de tamano t, con giro R (3x3). Lados con degradado: sombra petroleo abajo."""
    c = np.asarray(c, float)
    h = np.asarray(t, float) / 2.0
    R = np.eye(3) if R is None else np.asarray(R, float)
    col = np.asarray(col, float)
    v = 1.0 + RNG.normal(0, var)
    bajo = np.clip(mezclar(col, C["petroleo"], sombra) * v, 0, 1)
    alto = np.clip(mezclar(col, C["crema"], luz) * v, 0, 1)
    arriba = np.clip((alto if tapa is None else np.asarray(tapa, float) * v) * 1.04, 0, 1)
    e = [c + R @ (h * np.array(s, float)) for s in
         [(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1)]]
    for a, b, cc, d in [(0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]:
        f = 1.0 + RNG.normal(0, var * 0.6)
        m.quad(e[a], e[b], e[cc], e[d], bajo * f, alto * f, alto * f, bajo * f)
    m.quad(e[4], e[7], e[6], e[5], arriba)
    if base:
        m.quad(e[0], e[1], e[2], e[3], bajo)


def prisma(m, a, b, ra, rb=None, n=6, ca=None, cb=None, tapa_a=False, tapa_b=True, giro=0.0, var=0.035):
    """Prisma, tronco de cono o cono entre los puntos a y b (cualquier direccion)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rb = ra if rb is None else rb
    ca = np.asarray(ca, float)
    cb = ca if cb is None else np.asarray(cb, float)
    t = b - a
    u, w = marco(t)
    ang = np.arange(n) / n * 2 * math.pi + giro
    A = [a + (math.cos(x) * u + math.sin(x) * w) * ra for x in ang]
    B = [b + (math.cos(x) * u + math.sin(x) * w) * rb for x in ang]
    eje = (a + b) / 2.0
    for i in range(n):
        j = (i + 1) % n
        q = [A[i], A[j], B[j], B[i]]
        nrm = np.cross(q[2] - q[0], q[3] - q[1])
        if nrm @ (sum(q) / 4.0 - eje) < 0:
            q = [A[j], A[i], B[i], B[j]]
        f = 1.0 + RNG.normal(0, var)
        c0, c1 = np.clip(ca * f, 0, 1), np.clip(cb * f, 0, 1)
        if rb < 1e-6:
            m.tri(q[0], q[1], q[2], c0, c0, c1)
        elif ra < 1e-6:
            m.tri(q[0], q[2], q[3], c0, c1, c1)
        else:
            m.quad(q[0], q[1], q[2], q[3], c0, c0, c1, c1)
    if tapa_a and ra > 1e-6:
        cara(m, A, -t, ca)
    if tapa_b and rb > 1e-6:
        cara(m, B, t, np.clip(cb * 1.04, 0, 1))


def viga(m, a, b, lado, col, col2=None, tapas=True):
    """Barra de seccion cuadrada entre dos puntos."""
    prisma(m, a, b, lado * 0.7071, n=4, ca=col, cb=col if col2 is None else col2, tapa_a=tapas, tapa_b=tapas,
           giro=math.pi / 4)


def bola(m, c, r, sombra, base, luz, npts=14, escala=(1, 1, 1)):
    pts = fibonacci(npts) * np.array(escala, float) * r
    s = solido_facetado("bola", pts, sombra, base, luz, RNG, var=0.05)
    m.anexar(s, t=c)


def anillo(m, c, r, normal, lado, col, n=12):
    u, w = marco(normal)
    c = np.asarray(c, float)
    pts = [c + (math.cos(k / n * 2 * math.pi) * u + math.sin(k / n * 2 * math.pi) * w) * r for k in range(n)]
    for k in range(n):
        viga(m, pts[k], pts[(k + 1) % n], lado, jit(col, 0.05), tapas=False)


def suave(x, a, b):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def guardar(nombre, *mallas):
    e = Escena(GENERADOR)
    e.nodo(nombre, e.malla(*mallas, nombre=nombre))
    ruta = e.guardar(SALIDA / f"{nombre.split('_')[0]}.glb")
    tris = sum(len(x) for x in mallas)
    P = np.concatenate([np.array(x.P).reshape(-1, 3) for x in mallas if len(x)])
    print(f"{ruta.name:14s} {tris:5d} tri  caja {np.round(P.min(0), 2)} .. {np.round(P.max(0), 2)}")
    return tris


# ====================================================================== taller (TAL)

def tal01():
    m = Malla("TAL-01_banco")
    L, D, H = 2.0, 0.76, 0.80
    for i in range(4):   # tablero de cuatro tablones
        zc = -D / 2 + (i + 0.5) * D / 4
        caja(m, (0, H - 0.035, zc), (L, 0.07, D / 4 - 0.008), MAD_CLARA,
             tapa=jit(mezclar(MAD_CLARA, C["crema"], 0.10), 0.05))
    for sx in (-1, 1):
        for sz in (-1, 1):
            caja(m, (sx * (L / 2 - 0.07), (H - 0.07) / 2, sz * (D / 2 - 0.07)), (0.10, H - 0.07, 0.10), MAD)
    for sz in (-1, 1):
        caja(m, (0, H - 0.13, sz * (D / 2 - 0.07)), (L - 0.24, 0.09, 0.04), MAD)
    for sx in (-1, 1):
        caja(m, (sx * (L / 2 - 0.07), H - 0.13, 0), (0.04, 0.09, D - 0.24), MAD)
        caja(m, (sx * (L / 2 - 0.07), 0.20, 0), (0.05, 0.06, D - 0.24), MAD_OSC)
    caja(m, (-0.27, 0.22, 0), (1.26, 0.04, D - 0.16), MAD, tapa=mezclar(MAD, C["crema"], 0.08))   # balda baja
    # cajonera verde azulada con tres cajones (hoja HR_TAL)
    caja(m, (0.62, 0.40, 0.0), (0.52, 0.66, D - 0.14), mezclar(VERDE_AZUL, C["petroleo"], 0.35))
    for k in range(3):
        y = 0.19 + k * 0.205
        caja(m, (0.62, y, D / 2 - 0.06), (0.46, 0.17, 0.03), VERDE_AZUL, sombra=0.15)
        caja(m, (0.62, y, D / 2 - 0.04), (0.14, 0.03, 0.02), mezclar(C["crema"], C["dorado"], 0.35), sombra=0.1)
    return guardar("TAL-01_banco", m)


def tal02():
    m = Malla("TAL-02_osciloscopio")
    e = Malla("TAL-02_traza", "Emisivo")
    crema = mezclar(C["crema"], C["piedra_clara"], 0.45)
    caja(m, (0, 0.18, 0), (0.44, 0.30, 0.36), crema, sombra=0.22)
    for sx in (-1, 1):
        for sz in (-1, 1):
            caja(m, (sx * 0.17, 0.015, sz * 0.13), (0.05, 0.03, 0.05), HIERRO)
    zf = 0.18 + 0.004
    pantalla = mezclar(C["oscuro"], C["petroleo"], 0.55)
    cara(m, [(-0.19, 0.07, zf), (0.06, 0.07, zf), (0.06, 0.29, zf), (-0.19, 0.29, zf)], (0, 0, 1),
         mezclar(crema, C["piedra"], 0.5))
    z2 = zf + 0.003
    cara(m, [(-0.175, 0.085, z2), (0.045, 0.085, z2), (0.045, 0.275, z2), (-0.175, 0.275, z2)], (0, 0, 1),
         lambda p: mezclar(pantalla, C["petroleo"], 0.35 * (p[1] - 0.085) / 0.19))
    # traza cian: una senoide de tramos rectos
    z3 = z2 + 0.004
    n = 14
    pts = [(-0.165 + 0.20 * k / n, 0.18 + 0.055 * math.sin(k / n * 4 * math.pi)) for k in range(n + 1)]
    blanco = np.ones(3)
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        g = 0.008
        cara(e, [(x0, y0 - g, z3), (x1, y1 - g, z3), (x1, y1 + g, z3), (x0, y0 + g, z3)], (0, 0, 1), blanco)
    # perillas y bornes
    for i, x in enumerate((0.105, 0.17)):
        for k, y in enumerate((0.10, 0.18, 0.26)):
            col = mezclar(C["petroleo"], C["piedra_clara"], 0.25) if (i + k) % 2 else HIERRO
            prisma(m, (x, y, zf), (x, y, zf + 0.028), 0.024, 0.02, n=6, ca=col)
    # asa y rejilla de arriba
    caja(m, (0, 0.34, 0.0), (0.24, 0.02, 0.05), mezclar(crema, C["piedra"], 0.5))
    return guardar("TAL-02_osciloscopio", m, e)


def tal06():
    m = Malla("TAL-06_placa")
    e = Malla("TAL-06_led", "Emisivo")
    verde = mezclar(C["hierba_sombra"], C["cian_medio"], 0.45)
    caja(m, (0, 0.008, 0), (0.22, 0.016, 0.14), verde, sombra=0.1, tapa=mezclar(verde, C["petroleo"], 0.2))
    caja(m, (-0.03, 0.026, 0.0), (0.07, 0.02, 0.04), HIERRO)                         # el chip
    caja(m, (0.06, 0.026, -0.04), (0.035, 0.02, 0.02), METAL)
    caja(m, (0.06, 0.03, 0.03), (0.02, 0.03, 0.02), mezclar(C["dorado"], C["crema"], 0.3))
    for k in range(6):
        caja(m, (-0.085 + k * 0.03, 0.024, -0.055), (0.012, 0.016, 0.012), HIERRO, var=0.08)
    for x in (-0.09, 0.09):
        caja(e, (x, 0.024, 0.05), (0.018, 0.016, 0.018), np.ones(3), sombra=0, luz=0, var=0)
    # cables hacia el seguidor
    for col, dz in ((C["dorado"], -0.02), (C["coral"], 0.02)):
        p = [np.array([0.09, 0.02, dz]), np.array([0.16, 0.05, dz * 2]), np.array([0.24, 0.012, dz * 3])]
        for a, b in zip(p[:-1], p[1:]):
            viga(m, a, b, 0.008, col, tapas=False)
    return guardar("TAL-06_placa", m, e)


def tal07():
    m = Malla("TAL-07_caja_herramientas")
    azul = mezclar(C["petroleo"], C["piedra_clara"], 0.12)
    caja(m, (0, 0.10, 0), (0.44, 0.20, 0.24), azul, sombra=0.3)
    caja(m, (0, 0.215, 0), (0.46, 0.035, 0.26), mezclar(azul, C["piedra_clara"], 0.15), sombra=0.15)
    for sx in (-1, 1):
        caja(m, (sx * 0.14, 0.17, 0.125), (0.04, 0.07, 0.02), METAL, sombra=0.1)
        viga(m, (sx * 0.08, 0.232, 0), (sx * 0.08, 0.275, 0), 0.02, METAL)
    viga(m, (-0.09, 0.275, 0), (0.09, 0.275, 0), 0.024, METAL)
    return guardar("TAL-07_caja_herramientas", m)


def tal09():
    m = Malla("TAL-09_lampara")
    prisma(m, (0, 0, 0), (0, 0.025, 0), 0.085, 0.07, n=8, ca=HIERRO)
    codo = np.array([0.02, 0.24, -0.08])
    cabeza = np.array([-0.02, 0.36, 0.10])
    viga(m, (0, 0.025, 0), codo, 0.022, mezclar(C["piedra_osc"], C["piedra"], 0.3))
    viga(m, codo, cabeza, 0.022, mezclar(C["piedra_osc"], C["piedra"], 0.3))
    bola(m, codo, 0.025, HIERRO, mezclar(C["dorado"], C["madera1"], 0.4), C["dorado"], npts=8)
    d = np.array([-0.15, -0.75, 0.55])
    d /= np.linalg.norm(d)
    boca = cabeza + d * 0.14
    prisma(m, cabeza, boca, 0.035, 0.085, n=8, ca=HIERRO, cb=mezclar(C["piedra_osc"], C["petroleo"], 0.4),
           tapa_a=True, tapa_b=False)
    cara(m, [boca + (math.cos(k / 8 * 2 * math.pi) * marco(d)[0] + math.sin(k / 8 * 2 * math.pi) * marco(d)[1])
             * 0.075 for k in range(8)], d, LUZ)
    return guardar("TAL-09_lampara", m)


def tal10():
    m = Malla("TAL-10_taburete")
    prisma(m, (0, 0.43, 0), (0, 0.48, 0), 0.20, n=10, ca=MAD, cb=MAD_CLARA, tapa_a=True)
    pies = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        arriba, abajo = np.array([math.cos(a) * 0.12, 0.43, math.sin(a) * 0.12]), \
            np.array([math.cos(a) * 0.19, 0.0, math.sin(a) * 0.19])
        viga(m, abajo, arriba, 0.045, mezclar(MAD, C["petroleo"], 0.25), MAD)
        pies.append(abajo + (arriba - abajo) * 0.38)
    for k in range(4):
        viga(m, pies[k], pies[(k + 1) % 4], 0.03, MAD_OSC, tapas=False)
    return guardar("TAL-10_taburete", m)


def tal12():
    m = Malla("TAL-12_libros")
    paginas = mezclar(C["crema"], C["piedra_clara"], 0.25)
    tapas = [AZUL_OSC, mezclar(C["petroleo"], C["piedra"], 0.3), AZUL, mezclar(C["petroleo"], C["cian_medio"], 0.2),
             mezclar(C["terracota"], C["madera1"], 0.4), AZUL_OSC]
    # pila acostada a la izquierda
    y = 0.0
    for k, (w, col) in enumerate(((0.28, tapas[2]), (0.25, tapas[4]), (0.26, tapas[0]))):
        R = rot_y(RNG.uniform(-0.12, 0.12))
        caja(m, (-0.24, y + 0.025, 0.0), (w, 0.05, 0.19), col, R=R, sombra=0.2)
        caja(m, (-0.24, y + 0.025, 0.004), (w - 0.012, 0.036, 0.19), paginas, R=R, sombra=0.1)
        y += 0.052
    # fila de pie
    x = -0.04
    for k in range(5):
        w, h = RNG.uniform(0.045, 0.07), RNG.uniform(0.24, 0.30)
        caja(m, (x + w / 2, h / 2, 0.0), (w, h, 0.18), tapas[k], sombra=0.25)
        caja(m, (x + w / 2, h / 2 + 0.003, 0.004), (w - 0.012, h - 0.008, 0.18), paginas, sombra=0.1)
        x += w + 0.004
    R = rot_eje((0, 0, 1), -0.22)   # el ultimo, recostado
    caja(m, (x + 0.07, 0.125, 0.0), (0.05, 0.26, 0.18), tapas[5], R=R, sombra=0.25)
    return guardar("TAL-12_libros", m)


def tal14():
    m = Malla("TAL-14_telescopio")
    apice = np.array([0.0, 0.80, 0.0])
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3
        pie = np.array([math.cos(a) * 0.36, 0.0, math.sin(a) * 0.36])
        viga(m, pie, apice + (pie - apice) * 0.06, 0.04, mezclar(MAD, C["petroleo"], 0.2), MAD_CLARA)
        viga(m, pie, pie + (apice - pie) * 0.07, 0.05, HIERRO)
        medio = pie + (apice - pie) * 0.45
        viga(m, medio, (0, 0.40, 0), 0.02, HIERRO, tapas=False)
    prisma(m, (0, 0.78, 0), (0, 0.90, 0), 0.05, 0.04, n=6, ca=HIERRO, cb=mezclar(HIERRO, C["piedra"], 0.4))
    d = np.array([0.0, 0.50, -0.866])
    c = np.array([0.0, 0.97, 0.0])
    gris = mezclar(BLANCO, C["piedra_clara"], 0.6)
    prisma(m, c - d * 0.36, c + d * 0.40, 0.058, 0.062, n=8, ca=gris, cb=BLANCO, tapa_a=True, tapa_b=False)
    prisma(m, c + d * 0.40, c + d * 0.56, 0.07, n=8, ca=HIERRO, cb=mezclar(HIERRO, C["petroleo"], 0.3), tapa_b=False)
    u, w = marco(d)
    cara(m, [c + d * 0.54 + (math.cos(k / 8 * 2 * math.pi) * u + math.sin(k / 8 * 2 * math.pi) * w) * 0.064
             for k in range(8)], d, mezclar(C["petroleo"], C["brillo"], 0.55))
    prisma(m, c - d * 0.36, c - d * 0.47, 0.034, n=6, ca=HIERRO)                       # enfocador
    arr = np.cross(np.array([1.0, 0, 0]), d)
    arr /= np.linalg.norm(arr)
    if arr[1] < 0:
        arr = -arr
    prisma(m, c - d * 0.44, c - d * 0.44 + arr * 0.10, 0.022, n=6, ca=HIERRO, cb=mezclar(HIERRO, C["piedra"], 0.5))
    f = c + arr * 0.10 + d * 0.05                                                    # buscador
    prisma(m, f - d * 0.13, f + d * 0.13, 0.02, n=6, ca=HIERRO, cb=mezclar(HIERRO, C["piedra"], 0.3), tapa_a=True)
    viga(m, c + arr * 0.05 + d * 0.05, f, 0.02, HIERRO, tapas=False)
    return guardar("TAL-14_telescopio", m)


def tal15():
    """Seguidor lunar: montura casera de dos ejes, dos motores y una camara. La camara mira hacia -Z y arriba."""
    m = Malla("TAL-15_seguidor")
    caja(m, (0, 0.02, 0), (0.40, 0.04, 0.34), MAD_CLARA, tapa=mezclar(MAD_CLARA, C["crema"], 0.12))
    prisma(m, (0, 0.04, 0), (0, 0.075, 0), 0.13, 0.12, n=10, ca=MAD_OSC, cb=MAD)       # plato de azimut
    prisma(m, (0, 0.075, 0), (0, 0.11, 0), 0.06, n=8, ca=HIERRO, cb=mezclar(HIERRO, C["piedra"], 0.4))
    # horquilla de madera
    caja(m, (0, 0.125, 0), (0.30, 0.03, 0.07), MAD)
    for sx in (-1, 1):
        viga(m, (sx * 0.135, 0.13, 0), (sx * 0.135, 0.37, 0), 0.04, MAD, MAD_CLARA)
    # motores paso a paso: uno en el eje de altura y otro en el de azimut
    motor = METAL
    for c, t in (((0.215, 0.34, 0.0), (0.10, 0.09, 0.09)), ((-0.215, 0.20, 0.0), (0.10, 0.09, 0.09))):
        caja(m, c, t, motor, sombra=0.25)
        sx = 1 if c[0] > 0 else -1
        caja(m, (c[0] + sx * 0.055, c[1], c[2]), (0.012, 0.09, 0.09), HIERRO)
        caja(m, (c[0] - sx * 0.055, c[1], c[2]), (0.012, 0.09, 0.09), HIERRO)
    viga(m, (-0.135, 0.34, 0), (0.17, 0.34, 0), 0.022, HIERRO, tapas=False)            # eje de altura
    viga(m, (-0.215, 0.155, 0), (-0.215, 0.04, 0), 0.02, HIERRO, tapas=False)
    # cuna y camara, inclinadas hacia el cielo
    R = rot_eje((1, 0, 0), math.radians(38))
    c = np.array([0.0, 0.36, 0.0])
    caja(m, c + R @ np.array([0, -0.035, 0.0]), (0.20, 0.02, 0.12), MAD_OSC, R=R)
    caja(m, c + R @ np.array([0, 0.03, 0.01]), (0.15, 0.10, 0.09), HIERRO, R=R, sombra=0.15,
         tapa=mezclar(HIERRO, C["piedra"], 0.35))
    caja(m, c + R @ np.array([0.04, 0.09, 0.02]), (0.05, 0.03, 0.05), mezclar(HIERRO, C["piedra"], 0.2), R=R)
    d = R @ np.array([0, 0, -1.0])
    o = c + R @ np.array([0, 0.03, -0.035])
    prisma(m, o, o + d * 0.10, 0.042, 0.046, n=8, ca=HIERRO, cb=mezclar(HIERRO, C["piedra"], 0.4), tapa_b=False)
    u, w = marco(d)
    cara(m, [o + d * 0.085 + (math.cos(k / 8 * 2 * math.pi) * u + math.sin(k / 8 * 2 * math.pi) * w) * 0.04
             for k in range(8)], d, mezclar(C["petroleo"], C["brillo"], 0.35))
    # cables
    for col, p in ((C["dorado"], [(0.215, 0.29, 0.03), (0.19, 0.12, 0.10), (0.20, 0.045, 0.15)]),
                   (C["coral"], [(-0.215, 0.15, 0.03), (-0.12, 0.07, 0.12), (0.10, 0.045, 0.16)])):
        for a, b in zip(p[:-1], p[1:]):
            viga(m, a, b, 0.009, col, tapas=False)
    return guardar("TAL-15_seguidor", m)


def tal16():
    """Cuaderno abierto: la convocatoria copiada y el dibujo de la Luna."""
    m = Malla("TAL-16_cuaderno")
    papel = mezclar(C["crema"], BLANCO, 0.55)
    tinta = mezclar(C["petroleo"], C["oscuro"], 0.45)
    caja(m, (0, 0.006, 0), (0.46, 0.012, 0.31), AZUL_OSC, sombra=0.1)
    for sx in (-1, 1):
        R = rot_eje((0, 0, 1), -sx * 0.07)
        caja(m, (sx * 0.112, 0.026, 0), (0.215, 0.022, 0.29), papel, R=R, sombra=0.12, tapa=jit(papel, 0.02))
    y = 0.047

    def linea(x0, z0, x1, z1, g=0.006, col=tinta):
        a, b = np.array([x0, y, z0]), np.array([x1, y, z1])
        t = b - a
        n = np.array([-t[2], 0, t[0]])
        n = n / max(np.linalg.norm(n), 1e-9) * g / 2
        cara(m, [a - n, b - n, b + n, a + n], ARRIBA, col)

    for k in range(5):                                   # renglones de la convocatoria
        linea(-0.195, -0.10 + k * 0.035, -0.04 - 0.03 * (k % 2), -0.10 + k * 0.035)
    linea(-0.17, 0.085, -0.07, 0.085, 0.012, C["coral"])   # la fecha subrayada
    # la Luna dibujada: disco con tres crateres
    luna = mezclar(C["piedra_clara"], papel, 0.35)
    cx, cz = 0.115, -0.02
    cara(m, [(cx + math.cos(k / 10 * 2 * math.pi) * 0.062, y, cz + math.sin(k / 10 * 2 * math.pi) * 0.062)
             for k in range(10)], ARRIBA, luna)
    for dx, dz, r in ((-0.02, -0.015, 0.016), (0.022, 0.012, 0.012), (-0.005, 0.03, 0.009)):
        cara(m, [(cx + dx + math.cos(k / 6 * 2 * math.pi) * r, y + 0.001, cz + dz + math.sin(k / 6 * 2 * math.pi) * r)
                 for k in range(6)], ARRIBA, mezclar(C["piedra"], C["petroleo"], 0.3))
    linea(0.04, 0.09, 0.19, 0.09)
    linea(0.04, 0.115, 0.15, 0.115)
    viga(m, (0.25, 0.012, -0.08), (0.27, 0.012, 0.09), 0.012, C["dorado"], C["madera1"])   # el lapiz
    return guardar("TAL-16_cuaderno", m)


def tal17():
    m = Malla("TAL-17_lapices")
    vaso = mezclar(C["crema"], C["piedra_clara"], 0.4)
    prisma(m, (0, 0, 0), (0, 0.11, 0), 0.042, 0.05, n=8, ca=mezclar(vaso, C["petroleo"], 0.25), cb=vaso, tapa_b=False)
    cara(m, [(math.cos(k / 8 * 2 * math.pi) * 0.046, 0.10, math.sin(k / 8 * 2 * math.pi) * 0.046) for k in range(8)],
         ARRIBA, HIERRO)
    for k, col in enumerate((C["dorado"], C["coral"], C["petroleo"], C["madera1"], C["dorado"])):
        a = k * 1.3
        pie = np.array([math.cos(a) * 0.015, 0.03, math.sin(a) * 0.015])
        punta = np.array([math.cos(a) * 0.05, 0.19 + 0.02 * (k % 2), math.sin(a) * 0.05])
        viga(m, pie, punta, 0.011, col, tapas=True)
    return guardar("TAL-17_lapices", m)


# ====================================================================== habitacion (HAB)

def hab01():
    """Cama: cabecera en -X, largo 2,0 m en X y ancho 1,05 m en Z."""
    m = Malla("HAB-01_cama")
    L, W = 2.0, 1.05
    xc, xp = -L / 2 + 0.05, L / 2 - 0.05
    for sz in (-1, 1):
        caja(m, (xc, 0.48, sz * (W / 2 - 0.05)), (0.10, 0.96, 0.10), MAD)
        caja(m, (xc, 0.98, sz * (W / 2 - 0.05)), (0.12, 0.04, 0.12), MAD_CLARA)
        caja(m, (xp, 0.28, sz * (W / 2 - 0.05)), (0.10, 0.56, 0.10), MAD)
        caja(m, (0, 0.27, sz * (W / 2 - 0.045)), (L - 0.2, 0.15, 0.05), MAD, tapa=MAD_CLARA)
    caja(m, (xp, 0.33, 0), (0.05, 0.30, W - 0.2), MAD_CLARA)
    # cabecera con arco
    a = W / 2 - 0.10
    caja(m, (xc, 0.52, 0), (0.05, 0.56, 2 * a), MAD_CLARA)
    arco = [np.array([0.0, 0.80 + 0.17 * math.sin(k / 8 * math.pi), -a * math.cos(k / 8 * math.pi)]) for k in range(9)]
    for sx, x in ((-1, xc - 0.025), (1, xc + 0.025)):
        cara(m, [p + np.array([x, 0, 0]) for p in arco], (sx, 0, 0), lambda p: mezclar(MAD, MAD_CLARA, (p[1] - 0.8) / 0.17))
    for p, q in zip(arco[:-1], arco[1:]):
        cara(m, [p + (xc - 0.025, 0, 0), q + (xc - 0.025, 0, 0), q + (xc + 0.025, 0, 0), p + (xc + 0.025, 0, 0)],
             ARRIBA, jit(mezclar(MAD_CLARA, C["crema"], 0.15)))
    # colchon y almohada
    caja(m, (0.02, 0.40, 0), (L - 0.24, 0.16, W - 0.14), SABANA, sombra=0.20, luz=0.0)
    pts = fibonacci(14) * np.array([0.16, 0.07, 0.31]) + RNG.normal(0, 0.008, (14, 3))
    alm = solido_facetado("almohada", pts, mezclar(SABANA, C["petroleo"], 0.25), SABANA, BLANCO, RNG, var=0.03)
    m.anexar(alm, R=rot_y(0.15), t=(-0.66, 0.53, -0.03))
    # cobija azul facetada: rejilla con pliegues que cae por el lado del cuarto (+Z) y por el pie
    nx, nz = 7, 6
    x0, x1, z0, z1 = -0.30, L / 2 - 0.10, -W / 2 + 0.06, W / 2 - 0.02
    P = np.zeros((nx + 1, nz + 2, 3))
    for i in range(nx + 1):
        for k in range(nz + 1):
            x = x0 + (x1 - x0) * i / nx + (RNG.normal(0, 0.025) if 0 < i < nx else 0)
            z = z0 + (z1 - z0) * k / nz + (RNG.normal(0, 0.02) if 0 < k < nz else 0)
            P[i, k] = (x, 0.485 + abs(RNG.normal(0, 0.022)), z)
        P[i, nz + 1] = (P[i, nz, 0] + RNG.normal(0, 0.02), 0.20 + RNG.uniform(0, 0.07), W / 2 + 0.035)
    P[0, :, 0] += np.linspace(0.10, -0.08, nz + 2)      # el borde de arriba, torcido como en el concepto
    for i in range(nx):
        for k in range(nz + 1):
            a_, b_, c_, d_ = P[i, k], P[i + 1, k], P[i + 1, k + 1], P[i, k + 1]
            for tri in ((a_, b_, c_), (a_, c_, d_)) if (i + k) % 2 else ((a_, b_, d_), (b_, c_, d_)):
                col = jit(mezclar(AZUL, C["piedra_clara"], RNG.uniform(0, 0.30)), 0.06)
                if k == nz:
                    col = mezclar(col, C["petroleo"], 0.35)
                cara(m, tri, (0, 1, 0.6), col)
    # doblez de la sabana sobre la cobija
    caja(m, (-0.33, 0.495, 0.0), (0.12, 0.03, W - 0.16), BLANCO, R=rot_y(-0.08), sombra=0.1)
    return guardar("HAB-01_cama", m)


def _dovelas(m, a, b, y0, z=0.035, fondo=0.09, n=9, ancho=0.15):
    """Arco de ladrillos: semielipse de semiejes a y b que arranca en y0 (plano XY, relieve hacia +Z)."""
    cols = [mezclar(C["terracota"], C["sol"], 0.25), mezclar(C["tierra2"], C["terracota"], 0.4),
            mezclar(C["terracota"], C["coral"], 0.3)]
    for k in range(n):
        t = math.pi * (k + 0.5) / n
        p = np.array([math.cos(t) * (a + ancho / 2 - 0.01), y0 + math.sin(t) * (b + ancho / 2 - 0.01), z])
        ang = math.atan2(b * math.cos(t), -a * math.sin(t))
        largo = math.pi * (a + b) / 2 / n + 0.012
        caja(m, p, (largo, ancho, fondo), cols[k % 3], R=rot_eje((0, 0, 1), ang), sombra=0.18, var=0.05)


def _postigo(m, bisagra, R, ancho, alto):
    """Hoja de postigo con marco y lamas; crece hacia +X local desde la bisagra."""
    def loc(x, y, z=0.0):
        return np.asarray(bisagra, float) + R @ np.array([x, y, z])
    marco_c = mezclar(VERDE_AZUL, C["petroleo"], 0.30)
    for x in (0.035, ancho - 0.035):
        caja(m, loc(x, alto / 2), (0.07, alto, 0.045), marco_c, R=R, sombra=0.2)
    for y in (0.035, alto / 2, alto - 0.035):
        caja(m, loc(ancho / 2, y), (ancho - 0.14, 0.07, 0.045), marco_c, R=R, sombra=0.2)
    lama = R @ rot_eje((1, 0, 0), math.radians(35))
    for y0, y1 in ((0.07, alto / 2 - 0.035), (alto / 2 + 0.035, alto - 0.07)):
        n = 5
        for k in range(n):
            y = y0 + (k + 0.5) * (y1 - y0) / n
            caja(m, loc(ancho / 2, y), (ancho - 0.14, 0.022, (y1 - y0) / n * 1.05), jit(VERDE_AZUL, 0.05), R=lama,
                 sombra=0.12, tapa=mezclar(VERDE_AZUL, C["piedra_clara"], 0.25))


def hab02():
    """Ventana con arco de ladrillo, alfeizar ancho (el sitio de Orbita) y postigos verde azulado."""
    m = Malla("HAB-02_ventana")
    w = V_ANCHO / 2
    caja(m, (0, V_BASE - 0.04, 0.03), (V_ANCHO + 0.34, 0.08, 0.42), PIEDRA_CALIDA, sombra=0.25,
         tapa=mezclar(PIEDRA_CALIDA, LUZ, 0.35))
    for k in range(3):                                   # losetas del alfeizar
        caja(m, (-0.5 + k * 0.5, V_BASE + 0.004, 0.06), (0.47, 0.012, 0.33), jit(mezclar(PIEDRA_CALIDA, LUZ, 0.3), 0.05),
             sombra=0.05)
    _dovelas(m, w, V_ARCO, V_RECTO)
    cols = [mezclar(C["terracota"], C["sol"], 0.25), mezclar(C["tierra2"], C["terracota"], 0.4)]
    for sx in (-1, 1):
        n = 4
        for k in range(n):
            y = V_BASE + (k + 0.5) * (V_RECTO - V_BASE) / n
            caja(m, (sx * (w + 0.065), y, 0.035), (0.14, (V_RECTO - V_BASE) / n - 0.012, 0.09), cols[k % 2], sombra=0.18,
                 var=0.05)
    alto = V_RECTO - V_BASE + 0.30
    _postigo(m, (w + 0.15, V_BASE + 0.03, 0.07), rot_y(math.radians(-22)), 0.62, alto)
    _postigo(m, (-(w + 0.15), V_BASE + 0.03, 0.07), rot_y(math.radians(180 + 22)), 0.62, alto)
    return guardar("HAB-02_ventana", m)


def hab03():
    """Alfombra tejida de 2,4 x 1,5 m con franjas en zigzag y flecos."""
    m = Malla("HAB-03_alfombra")
    LX, LZ = 1.2, 0.75
    crema = mezclar(C["crema"], C["tierra1"], 0.35)
    terra = mezclar(C["terracota"], C["coral"], 0.25)
    azul = mezclar(C["petroleo"], C["piedra_clara"], 0.35)
    naranja = mezclar(C["sol"], C["coral"], 0.35)
    y0, y1 = 0.010, 0.014

    def franja(za, zb, col, y=y0):
        cara(m, [(-LX, y, za), (LX, y, za), (LX, y, zb), (-LX, y, zb)], ARRIBA, jit(col, 0.03))

    def dientes(za, zb, n, col):
        dx = 2 * LX / n
        for i in range(n):
            x = -LX + i * dx
            cara(m, [(x, y1, za), (x + dx, y1, za), (x + dx / 2, y1, zb)], ARRIBA, jit(col, 0.05))

    def zigzag(za, zb, n, col, g):
        dx = 2 * LX / n
        for i in range(n):
            x = -LX + i * dx
            a, b = (za, zb) if i % 2 == 0 else (zb, za)
            cara(m, [(x, y1, a), (x + dx, y1, b), (x + dx, y1, b + g), (x, y1, a + g)], ARRIBA, jit(col, 0.05))

    caja(m, (0, 0.005, 0), (2 * LX, 0.01, 2 * LZ), crema, sombra=0.2, tapa=crema)
    for s in (-1, 1):   # simetrica respecto del centro
        def z(v):
            return s * v
        franja(z(0.75), z(0.68), mezclar(crema, C["madera1"], 0.25), y1)
        dientes(z(0.68), z(0.54), 16, terra)
        franja(z(0.52), z(0.47), naranja, y1)
        zigzag(z(0.43) - 0.035, z(0.31) - 0.035, 12, azul, 0.07)
        franja(z(0.27), z(0.22), terra, y1)
    franja(-0.20, 0.20, mezclar(naranja, crema, 0.35), y1)
    n = 8
    dx = 2 * LX / n
    for i in range(n):                                   # rombos del centro
        x = -LX + (i + 0.5) * dx
        cara(m, [(x - dx * 0.4, y1 + 0.002, 0), (x, y1 + 0.002, 0.15), (x + dx * 0.4, y1 + 0.002, 0), (x, y1 + 0.002, -0.15)],
             ARRIBA, jit(azul if i % 2 else terra, 0.05))
    for sx in (-1, 1):                                   # flecos
        for k in range(15):
            zc = -LZ + (k + 0.5) * 2 * LZ / 15
            cara(m, [(sx * LX, 0.006, zc - 0.022), (sx * (LX + 0.11), 0.004, zc - 0.03 + RNG.normal(0, 0.008)),
                     (sx * (LX + 0.11), 0.004, zc + 0.03), (sx * LX, 0.006, zc + 0.022)], ARRIBA, jit(crema, 0.06))
    return guardar("HAB-03_alfombra", m)


def hab04():
    m = Malla("HAB-04_repisa")
    caja(m, (0, 1.42, 0.135), (1.45, 0.045, 0.27), MAD_CLARA, tapa=mezclar(MAD_CLARA, C["crema"], 0.12))
    for sx in (-1, 1):
        caja(m, (sx * 0.52, 1.36, 0.02), (0.05, 0.08, 0.04), MAD)
        viga(m, (sx * 0.52, 1.25, 0.02), (sx * 0.52, 1.39, 0.20), 0.04, MAD_OSC, MAD)
    return guardar("HAB-04_repisa", m)


def hab05():
    """Poster enmarcado: la cupula blanca de un observatorio sobre una loma. Sin texto."""
    m = Malla("HAB-05_poster")
    W, H = 1.05, 0.78
    for sx in (-1, 1):
        caja(m, (sx * (W / 2 - 0.03), 0, 0.02), (0.06, H, 0.04), MAD_CLARA)
        caja(m, (0, sx * (H / 2 - 0.03), 0.02), (W - 0.12, 0.06, 0.04), MAD_CLARA)
    a, b = W / 2 - 0.06, H / 2 - 0.06
    z = 0.012
    cielo_bajo, cielo_alto = mezclar(C["piedra_clara"], C["crema"], 0.3), mezclar(C["petroleo"], C["piedra_clara"], 0.25)
    cara(m, [(-a, -b, z), (a, -b, z), (a, b, z), (-a, b, z)], (0, 0, 1),
         lambda p: mezclar(cielo_bajo, cielo_alto, (p[1] + b) / (2 * b)))
    z += 0.003
    loma = mezclar(C["hierba_sombra"], C["hierba_sol"], 0.5)
    cara(m, [(-a, -b, z), (a, -b, z), (a, -0.12, z), (0.18, 0.0, z), (-0.16, -0.02, z), (-a, -0.20, z)], (0, 0, 1),
         lambda p: mezclar(HOJA_OSC, loma, (p[1] + b) / 0.35))
    z += 0.003
    cara(m, [(-0.02, -b, z), (0.10, -b, z), (0.06, -0.03, z), (0.0, -0.03, z)], (0, 0, 1), mezclar(C["crema"], C["tierra1"], 0.3))
    blanco = mezclar(BLANCO, C["piedra_clara"], 0.2)
    cara(m, [(-0.17, -0.03, z), (0.21, -0.03, z), (0.21, 0.09, z), (-0.17, 0.09, z)], (0, 0, 1),
         lambda p: mezclar(mezclar(blanco, C["petroleo"], 0.25), blanco, (p[0] + 0.17) / 0.38))
    for k in range(5):
        x = -0.14 + k * 0.075
        cara(m, [(x, -0.02, z + 0.002), (x + 0.03, -0.02, z + 0.002), (x + 0.03, 0.06, z + 0.002), (x, 0.06, z + 0.002)],
             (0, 0, 1), mezclar(C["petroleo"], C["piedra_clara"], 0.35))
    cupula = [(0.02 + math.cos(k / 8 * math.pi) * 0.135, 0.09 + math.sin(k / 8 * math.pi) * 0.135, z + 0.002) for k in range(9)]
    cara(m, cupula, (0, 0, 1), lambda p: mezclar(mezclar(blanco, C["petroleo"], 0.30), BLANCO, (p[0] + 0.115) / 0.27))
    cara(m, [(0.035, 0.10, z + 0.004), (0.065, 0.10, z + 0.004), (0.06, 0.218, z + 0.004), (0.04, 0.222, z + 0.004)],
         (0, 0, 1), mezclar(C["petroleo"], C["piedra"], 0.4))
    return guardar("HAB-05_poster", m)


def hab06():
    m = Malla("HAB-06_caja_carton")
    caja(m, (0, 0.24, 0), (0.62, 0.48, 0.50), CARTON, sombra=0.30, tapa=mezclar(CARTON, C["crema"], 0.15))
    cinta = mezclar(C["crema"], C["piedra_clara"], 0.2)
    caja(m, (0, 0.482, 0), (0.09, 0.006, 0.505), cinta, sombra=0.0)
    caja(m, (0, 0.40, 0.251), (0.09, 0.16, 0.006), cinta, sombra=0.1)
    cara(m, [(-0.3, 0.484, -0.003), (0.3, 0.484, -0.003), (0.3, 0.484, 0.003), (-0.3, 0.484, 0.003)], ARRIBA,
         mezclar(CARTON, C["madera2"], 0.5))
    hueco = mezclar(C["madera2"], C["oscuro"], 0.4)
    cara(m, [(-0.24, 0.28, 0.2515), (-0.10, 0.28, 0.2515), (-0.10, 0.33, 0.2515), (-0.24, 0.33, 0.2515)], (0, 0, 1), hueco)
    cara(m, [(0.311, 0.28, -0.07), (0.311, 0.28, 0.07), (0.311, 0.33, 0.07), (0.311, 0.33, -0.07)], (1, 0, 0), hueco)
    return guardar("HAB-06_caja_carton", m)


def _poste(m, x, z=0.0, alto=1.0):
    caja(m, (x, alto / 2, z), (0.13, alto, 0.13), MAD, sombra=0.3)
    caja(m, (x, alto + 0.03, z), (0.18, 0.06, 0.18), PIEDRA_CALIDA, sombra=0.2)
    prisma(m, (x, alto + 0.06, z), (x, alto + 0.14, z), 0.127, 0.0, n=4, ca=PIEDRA_CALIDA,
           cb=mezclar(PIEDRA_CALIDA, C["crema"], 0.4), giro=math.pi / 4)


def _tramo(m, a, b, R=None, origen=(0, 0, 0)):
    """Tramo de baranda entre las abscisas a y b (eje X local), con pasamanos y balaustres."""
    R = np.eye(3) if R is None else R
    o = np.asarray(origen, float)

    def loc(x, y):
        return o + R @ np.array([x, y, 0.0])
    largo = b - a
    caja(m, loc((a + b) / 2, 0.86), (largo, 0.06, 0.08), MAD_CLARA, R=R, tapa=mezclar(MAD_CLARA, C["crema"], 0.15))
    caja(m, loc((a + b) / 2, 0.16), (largo, 0.05, 0.05), MAD, R=R)
    n = max(1, int(round(largo / 0.15)))
    for k in range(n):
        x = a + (k + 0.5) * largo / n
        caja(m, loc(x, 0.51), (0.04, 0.65, 0.04), jit(MAD, 0.05), R=R, sombra=0.3)


def hab07():
    """Baranda de 2,0 m con la puerta abierta. Corre por +X; el cuarto queda del lado +Z y la escalera en -Z."""
    m = Malla("HAB-07_baranda")
    for x in (0.0, 0.45, 1.45, 2.0):
        _poste(m, x)
    _tramo(m, 0.065, 0.385)
    _tramo(m, 1.515, 1.935)
    # la hoja de la puerta, abierta hacia la escalera y apoyada junto al muro
    R = rot_y(math.radians(100))
    o = (0.45, 0.0, -0.07)
    _tramo(m, 0.03, 0.93, R=R, origen=o)
    for x in (0.03, 0.93):
        caja(m, np.array(o) + R @ np.array([x, 0.50, 0.0]), (0.05, 0.78, 0.05), MAD_CLARA, R=R)
    caja(m, np.array(o) + R @ np.array([0.90, 0.55, 0.035]), (0.05, 0.10, 0.02), HIERRO, R=R)   # cerrojo
    return guardar("HAB-07_baranda", m)


def hab08():
    m = Malla("HAB-08_felpudo")
    fibra = mezclar(C["tierra2"], C["dorado"], 0.25)
    caja(m, (0, 0.011, 0), (0.80, 0.022, 0.50), mezclar(fibra, C["madera2"], 0.3), sombra=0.2, tapa=fibra)
    for k in range(1, 5):
        a, b = 0.40 - k * 0.07, 0.25 - k * 0.05
        y = 0.022 + 0.001 * k
        cara(m, [(-a, y, -b), (a, y, -b), (a, y, b), (-a, y, b)], ARRIBA,
             jit(mezclar(fibra, C["madera2"], 0.35) if k % 2 else mezclar(fibra, C["crema"], 0.25), 0.04))
    return guardar("HAB-08_felpudo", m)


def hab09():
    """Descanso de madera, escalera que baja hacia +X y muro con arco. Origen en el borde del cuarto,
    frente a la puerta de la baranda (x = AX del cuarto); la baranda corre de z = -0.95 a z = 1.05."""
    m = Malla("HAB-09_escalera")
    Z0, Z1 = -0.95, 1.05
    piedra = mezclar(PIEDRA_CALIDA, C["tierra1"], 0.35)
    n = 4
    for k in range(n):                                   # tablones del descanso
        x = (k + 0.5) * 0.70 / n
        caja(m, (x, -0.03, (Z0 + Z1) / 2), (0.70 / n - 0.008, 0.06, Z1 - Z0), jit(MAD_CLARA, 0.05),
             tapa=jit(mezclar(MAD_CLARA, C["crema"], 0.10), 0.05))
    caja(m, (0.35, (-0.06 + BAJO * 3) / 2, (Z0 + Z1) / 2), (0.70, -BAJO * 3 - 0.06, Z1 - Z0), mezclar(PARED_BAJA, C["petroleo"], 0.3))
    for i in range(7):                                   # escalones
        y = -(i + 1) * 0.18
        caja(m, (0.70 + 0.13 + 0.26 * i, (y - 2.4) / 2, 0.0), (0.26, y + 2.4, 1.0), piedra, sombra=0.35,
             tapa=jit(mezclar(piedra, LUZ, 0.25), 0.04))
    # muro con arco, cara hacia el cuarto (-X)
    xm, alto_m = 0.95, 1.35
    a, y_recto, b = 0.50, 0.55, 0.38

    def col_muro(p):
        t = suave(p[1], -0.6, alto_m)
        c = mezclar(PARED_BAJA, PARED, t)
        brillo = math.exp(-((p[2] / 0.9) ** 2) - ((p[1] - 0.5) / 0.9) ** 2) * 0.35     # la luz del farol
        return mezclar(c, LUZ, brillo)

    def arco(z):
        return y_recto + b * math.sqrt(max(0.0, 1 - (z / a) ** 2))
    zs = sorted(set(np.round(np.concatenate([np.linspace(Z0, -a, 3), np.linspace(-a, a, 9), np.linspace(a, Z1, 3)]), 4)))
    for z0, z1 in zip(zs[:-1], zs[1:]):
        if z0 >= -a - 1e-6 and z1 <= a + 1e-6:
            cara(m, [(xm, arco(z0), z0), (xm, arco(z1), z1), (xm, alto_m, z1), (xm, alto_m, z0)], (-1, 0, 0), col_muro)
            cara(m, [(xm, arco(z0), z0), (xm, arco(z1), z1), (xm + G, arco(z1), z1), (xm + G, arco(z0), z0)], (0, -1, 0),
                 mezclar(PARED_BAJA, LUZ, 0.25))
        else:
            for ya, yb in ((-2.4, -0.6), (-0.6, 0.4), (0.4, alto_m)):
                cara(m, [(xm, ya, z0), (xm, ya, z1), (xm, yb, z1), (xm, yb, z0)], (-1, 0, 0), col_muro)
    for sz in (-1, 1):                                   # jambas del arco
        cara(m, [(xm, -2.4, sz * a), (xm + G, -2.4, sz * a), (xm + G, y_recto, sz * a), (xm, y_recto, sz * a)], (0, 0, -sz),
             mezclar(PARED_BAJA, LUZ, 0.2))
    cara(m, [(xm, alto_m, Z0), (xm + G, alto_m, Z0), (xm + G, alto_m, Z1), (xm, alto_m, Z1)], ARRIBA, CORTE)
    cara(m, [(xm, -2.4, Z1), (xm + G, -2.4, Z1), (xm + G, alto_m, Z1), (xm, alto_m, Z1)], (0, 0, 1), EXTERIOR)
    tmp = Malla("dovelas")
    _dovelas(tmp, a, b, y_recto, z=0.03, fondo=0.08, n=9, ancho=0.13)
    m.anexar(tmp, R=rot_y(-math.pi / 2), t=(xm, 0, 0))
    # v2: sin el panel calido del fondo del pasaje (flotaba en el aire): la escalinata sigue en HAB-18
    # murete del frente del descanso
    caja(m, (0.475, (0.34 + BAJO * 3) / 2, Z1 + 0.06), (0.95, 0.34 - BAJO * 3, 0.12), EXTERIOR, tapa=CORTE)
    return guardar("HAB-09_escalera", m)


def hab10():
    m = Malla("HAB-10_esfera_armilar")
    laton = mezclar(C["dorado"], C["madera1"], 0.25)
    prisma(m, (0, 0, 0), (0, 0.025, 0), 0.075, 0.06, n=8, ca=mezclar(laton, C["madera2"], 0.4), cb=laton)
    prisma(m, (0, 0.025, 0), (0, 0.11, 0), 0.016, 0.012, n=6, ca=laton)
    c = np.array([0, 0.225, 0])
    eje = np.array([math.sin(0.41), math.cos(0.41), 0])
    anillo(m, c, 0.115, (0, 0, 1), 0.014, laton)
    anillo(m, c, 0.105, eje, 0.012, mezclar(laton, C["crema"], 0.2))
    anillo(m, c, 0.10, (1, 0.2, 0.1), 0.010, laton, n=10)
    viga(m, c - eje * 0.13, c + eje * 0.13, 0.008, mezclar(laton, C["madera2"], 0.3), tapas=False)
    bola(m, c, 0.035, mezclar(laton, C["madera2"], 0.5), laton, mezclar(C["dorado"], C["crema"], 0.4), npts=10)
    return guardar("HAB-10_esfera_armilar", m)


def hab11():
    m = Malla("HAB-11_farol")
    caja(m, (0, 0.02, 0), (0.17, 0.04, 0.17), HIERRO)
    caja(m, (0, 0.165, 0), (0.115, 0.25, 0.115), mezclar(C["sol"], C["crema"], 0.45), sombra=0.0, luz=0.6, var=0.02,
         tapa=LUZ)
    for sx in (-1, 1):
        for sz in (-1, 1):
            caja(m, (sx * 0.065, 0.165, sz * 0.065), (0.02, 0.26, 0.02), HIERRO)
    caja(m, (0, 0.165, 0), (0.14, 0.018, 0.14), HIERRO)
    prisma(m, (0, 0.29, 0), (0, 0.385, 0), 0.13, 0.03, n=4, ca=HIERRO, cb=mezclar(HIERRO, C["piedra"], 0.35),
           giro=math.pi / 4)
    prisma(m, (0, 0.385, 0), (0, 0.41, 0), 0.02, n=5, ca=HIERRO)
    anillo(m, (0, 0.445, 0), 0.035, (0, 0, 1), 0.009, HIERRO, n=8)
    return guardar("HAB-11_farol", m)


# ---------- HAB-12: suelo de baldosas, paredes del fondo y de la derecha y bordes cortados ----------

SIN_HAZ = False              # True: variante de noche del cuarto (HAB-12n), sin los haces de sol pintados


def luz_ventana(x, z):
    """Luz pintada que entra por la ventana: tres haces que se abren sobre el suelo (0..1)."""
    if SIN_HAZ:
        return 0.0
    d = z + AZ
    if d < 0.10 or d > 3.9:
        return 0.0
    medio = 0.62 + 0.20 * d
    u = (x - (VX + 0.06 * d)) / medio
    if abs(u) > 1.2:
        return 0.0
    borde = suave(1.2 - abs(u), 0.0, 0.35)
    rayas = 0.60 + 0.40 * math.cos(u * math.pi * 2.6)
    return borde * rayas * suave(d, 0.10, 0.55) * (1.0 - suave(d, 2.3, 3.9))


def _suelo(m):
    junta = mezclar(C["terracota"], C["madera2"], 0.55)
    cara(m, [(-AX, 0, -AZ), (AX, 0, -AZ), (AX, 0, AZ), (-AX, 0, AZ)], ARRIBA, junta)
    nx, nz = 15, 12
    dx, dz = 2 * AX / nx, 2 * AZ / nz
    j = 0.012
    tonos = [mezclar(C["terracota"], C["sol"], 0.42), mezclar(C["terracota"], C["tierra2"], 0.55),
             mezclar(C["coral"], C["tierra2"], 0.60), mezclar(C["terracota"], C["sol"], 0.30)]
    for i in range(nx):
        for k in range(nz):
            x0, x1 = -AX + i * dx + j, -AX + (i + 1) * dx - j
            z0, z1 = -AZ + k * dz + j, -AZ + (k + 1) * dz - j
            base = jit(tonos[RNG.integers(0, 4)], 0.05)
            # las esquinas del cuarto, algo mas frias y oscuras (vineta pintada)
            lejos = suave(math.hypot((x0 + x1) / 2 / AX, (z0 + z1) / 2 / AZ), 0.75, 1.35)
            base = mezclar(base, mezclar(C["terracota"], C["petroleo"], 0.35), 0.45 * lejos)

            def col(p, base=base):
                s = luz_ventana(p[0], p[2])
                return np.clip(mezclar(base, LUZ, 0.62 * s) * (1.0 + 0.10 * s), 0, 1)
            con_luz = max(luz_ventana(x, z) for x in (x0, (x0 + x1) / 2, x1) for z in (z0, (z0 + z1) / 2, z1)) > 0.01
            sub = 4 if con_luz else 1
            for a in range(sub):
                for b in range(sub):
                    xa, xb = x0 + (x1 - x0) * a / sub, x0 + (x1 - x0) * (a + 1) / sub
                    za, zb = z0 + (z1 - z0) * b / sub, z0 + (z1 - z0) * (b + 1) / sub
                    cara(m, [(xa, 0.004, za), (xb, 0.004, za), (xb, 0.004, zb), (xa, 0.004, zb)], ARRIBA, col)


def _col_pared(p, foco=None):
    y = p[1]
    if y < 0.9:
        c = mezclar(PARED_BAJA, PARED, max(0.0, y) / 0.9)
    else:
        c = mezclar(PARED, PARED_ALTA, min(1.0, (y - 0.9) / (ALTO - 0.9)))
    if foco is not None:
        c = mezclar(c, LUZ, 0.30 * math.exp(-((p[0] - foco) / 1.5) ** 2 - ((y - 1.2) / 1.3) ** 2))
    return c


def _pared_fondo(m):
    z = -AZ
    w = V_ANCHO / 2

    def arco(x):
        return V_RECTO + V_ARCO * math.sqrt(max(0.0, 1 - ((x - VX) / w) ** 2))
    xs = sorted(set(np.round(np.concatenate([np.linspace(-AX, VX - w, 6), np.linspace(VX - w, VX + w, 11),
                                             np.linspace(VX + w, AX, 6)]), 4)))
    ys = [0.0, 0.5, 1.0, 1.65, ALTO]
    for x0, x1 in zip(xs[:-1], xs[1:]):
        if x0 >= VX - w - 1e-6 and x1 <= VX + w + 1e-6:
            tramos = [[(x0, 0.0), (x1, 0.0), (x1, 0.45), (x0, 0.45)], [(x0, 0.45), (x1, 0.45), (x1, V_BASE), (x0, V_BASE)],
                      [(x0, arco(x0)), (x1, arco(x1)), (x1, ALTO), (x0, ALTO)]]
            # intrados del arco y alfeizar (el grosor del muro)
            cara(m, [(x0, arco(x0), z), (x1, arco(x1), z), (x1, arco(x1), z - G), (x0, arco(x0), z - G)], (0, -1, 0.2),
                 mezclar(PARED_BAJA, LUZ, 0.30))
            cara(m, [(x0, V_BASE, z), (x1, V_BASE, z), (x1, V_BASE, z - G), (x0, V_BASE, z - G)], ARRIBA,
                 mezclar(PARED, LUZ, 0.4))
        else:
            tramos = [[(x0, ya), (x1, ya), (x1, yb), (x0, yb)] for ya, yb in zip(ys[:-1], ys[1:])]
        for t in tramos:
            f = 1.0 + RNG.normal(0, 0.025)
            cara(m, [(x, y, z) for x, y in t], (0, 0, 1), lambda p, f=f: _col_pared(p, None if SIN_HAZ else VX) * f)
    for sx in (-1, 1):                                   # jambas
        x = VX + sx * w
        cara(m, [(x, V_BASE, z), (x, V_RECTO, z), (x, V_RECTO, z - G), (x, V_BASE, z - G)], (-sx, 0, 0),
             mezclar(PARED_BAJA, LUZ, 0.35))
    cara(m, [(-AX - G, ALTO, z - G), (AX + G, ALTO, z - G), (AX + G, ALTO, z), (-AX - G, ALTO, z)], ARRIBA, CORTE)
    # zocalo de baldosas
    n = 15
    for k in range(n):
        x = -AX + (k + 0.5) * 2 * AX / n
        caja(m, (x, 0.07, z + 0.012), (2 * AX / n - 0.012, 0.14, 0.024), mezclar(C["terracota"], C["madera2"], 0.25),
             sombra=0.15, var=0.06)


def _pared_derecha(m):
    x = AX
    zs = np.linspace(-AZ, PARED_DER_FIN, 8)
    ys = [0.0, 0.5, 1.0, 1.65, ALTO]
    for z0, z1 in zip(zs[:-1], zs[1:]):
        for ya, yb in zip(ys[:-1], ys[1:]):
            f = 1.0 + RNG.normal(0, 0.025)
            cara(m, [(x, ya, z0), (x, ya, z1), (x, yb, z1), (x, yb, z0)], (-1, 0, 0),
                 lambda p, f=f: mezclar(_col_pared(p), C["sol"], 0.10) * f)
    cara(m, [(x, ALTO, -AZ - G), (x + G, ALTO, -AZ - G), (x + G, ALTO, PARED_DER_FIN), (x, ALTO, PARED_DER_FIN)], ARRIBA, CORTE)
    cara(m, [(x, BAJO, PARED_DER_FIN), (x + G, BAJO, PARED_DER_FIN), (x + G, ALTO, PARED_DER_FIN), (x, ALTO, PARED_DER_FIN)],
         (0, 0, 1), lambda p: mezclar(EXTERIOR, CORTE, suave(p[1], 0.0, ALTO)))
    n = 8
    largo = PARED_DER_FIN + AZ
    for k in range(n):
        z = -AZ + (k + 0.5) * largo / n
        caja(m, (x - 0.012, 0.07, z), (0.024, 0.14, largo / n - 0.012), mezclar(C["terracota"], C["madera2"], 0.25),
             sombra=0.15, var=0.06)


def _bordes(m):
    """Las paredes cercanas, cortadas: la izquierda baja en curva desde el fondo; la del frente es un murete."""
    def alto_izq(z):
        return 0.32 + (ALTO - 0.32) * (1.0 - suave(z, -AZ - G, -AZ + 1.5)) ** 1.6
    xo, xi = -AX - G, -AX
    zs = np.concatenate([np.linspace(-AZ - G, -AZ + 1.5, 9), np.linspace(-AZ + 1.5, AZ + G, 5)[1:]])
    for z0, z1 in zip(zs[:-1], zs[1:]):
        h0, h1 = alto_izq(z0), alto_izq(z1)
        cara(m, [(xo, BAJO, z0), (xo, BAJO, z1), (xo, h1, z1), (xo, h0, z0)], (-1, 0, 0),
             lambda p: mezclar(EXTERIOR, mezclar(EXTERIOR, C["piedra"], 0.35), suave(p[1], 0, ALTO)))
        cara(m, [(xo, h0, z0), (xi, h0, z0), (xi, h1, z1), (xo, h1, z1)], (0, 1, 0.3), jit(CORTE, 0.03))
        cara(m, [(xi, 0, z0), (xi, 0, z1), (xi, h1, z1), (xi, h0, z0)], (1, 0, 0), lambda p: _col_pared(p))
    # murete del frente
    x1 = AX
    cara(m, [(xo, BAJO, AZ + G), (x1, BAJO, AZ + G), (x1, 0.32, AZ + G), (xo, 0.32, AZ + G)], (0, 0, 1),
         lambda p: mezclar(EXTERIOR, mezclar(EXTERIOR, C["piedra"], 0.3), suave(p[1], BAJO, 0.32)))
    cara(m, [(xo, 0.32, AZ), (x1, 0.32, AZ), (x1, 0.32, AZ + G), (xo, 0.32, AZ + G)], ARRIBA, CORTE)
    cara(m, [(xi, 0, AZ), (x1, 0, AZ), (x1, 0.32, AZ), (xi, 0.32, AZ)], (0, 0, -1), lambda p: _col_pared(p))
    # postes del frente: el del farol y el de la esquina del descanso
    _poste(m, -1.6, AZ + G / 2, 0.80)
    _poste(m, AX + 0.0, AZ + G / 2, 1.0)


def hab12():
    m = Malla("HAB-12_cuarto")
    _suelo(m)
    _pared_fondo(m)
    _pared_derecha(m)
    _bordes(m)
    return guardar("HAB-12_cuarto", m)


def hab12n():
    """El mismo cuarto de noche: sin los haces de sol pintados en el suelo ni el resplandor de la ventana."""
    global SIN_HAZ
    SIN_HAZ = True
    m = Malla("HAB-12n_cuarto_noche")
    _suelo(m)
    _pared_fondo(m)
    _pared_derecha(m)
    _bordes(m)
    SIN_HAZ = False
    return guardar("HAB-12n_cuarto_noche", m)


VENTANAS = []                # (centro, medio_ancho, medio_alto, normal) de cada ventana de las casas: HAB-19


def _casa(m, x, y, z, lado, alto, col, giro=0.0):
    R = rot_y(giro)
    caja(m, (x, y + alto / 2, z), (lado, alto, lado), col, R=R, sombra=0.40, var=0.05)
    teja_b, teja_a = mezclar(TEJA, C["madera2"], 0.25), mezclar(TEJA, C["sol"], 0.25)
    prisma(m, (x, y + alto, z), (x, y + alto + lado * 0.32, z), lado * 0.80, lado * 0.16, n=4, ca=teja_b, cb=teja_a,
           giro=math.pi / 4 - giro)
    hueco = mezclar(C["petroleo"], C["oscuro"], 0.35)
    for sx in (-0.25, 0.25):
        c = np.array([x, y + alto * 0.58, z]) + R @ np.array([sx * lado, 0, lado / 2 + 0.01])
        ex, ey = R @ np.array([lado * 0.09, 0, 0]), np.array([0, alto * 0.16, 0])
        cara(m, [c - ex - ey, c + ex - ey, c + ex + ey, c - ex + ey], R @ np.array([0, 0, 1.0]), hueco)
        VENTANAS.append((c, ex, ey, R @ np.array([0, 0, 1.0])))      # para las ventanas encendidas (HAB-19)


# ---------- v3: la ladera baja en bancales (terrazas con muro de piedra), como Las Escalinatas ----------
# Bordes de cada bancal (z de delante a z de detras). La altura de cada uno es la de la ladera suave en su centro.
TERRAZAS = [-2.6, -4.1, -5.7, -7.6, -9.9, -12.8, -16.3, -20.6, -25.8, -32.0, -48.0]
# Cono que se ve por la ventana del fondo (coordenadas del cuarto). Medido con la camara real y la inclinacion 2.5D
# (Nasa_Game/Construccion/Zonas/habitacion/v2/medir_ventana.gd): con los encuadres 0,20 y 0,125 el vano mira el suelo
# de fuera en x de -0,2 a 4,3 y z de -9,5 a -15,2; lo que queda entre el muro y z = -9,5 solo asoma por el borde de
# abajo si mide mas de 1 m. Aqui no va ninguna casa grande del barrio, solo la vista compuesta.
CONO_X, CONO_Z = (-0.9, 4.6), (-16.6, -2.6)
VISTA_Z = (-9.9, -16.3)          # donde se compone la vista (dos bancales)
# Estado del RNG comun justo despues de HAB-13 v2: HAB-13 v3 usa su propio generador y despues se repone este
# estado, para que la buganvilla, las macetas y el resto (HAB-14 en adelante) no cambien.
RNG_TRAS_HAB13 = {"bit_generator": "PCG64",
                  "state": {"state": 253684933851803439002519314945443696037,
                            "inc": 73030421956038382396665486183601481221},
                  "has_uint32": 0, "uinteger": 3132931250}


def _alto_suave(z):
    # v3: la ladera sigue bajando despues de z = -11 (antes quedaba llana): bancales y muros tambien al fondo
    return -0.9 - 2.6 * suave(-z, 3.0, 11.0) - 1.4 * suave(-z, 11.0, 22.0)


def _terraza(z):
    """(z de delante, z de detras, altura) del bancal que contiene z."""
    for z0, z1 in zip(TERRAZAS[:-1], TERRAZAS[1:]):
        if z >= z1:
            return z0, z1, _alto_suave((z0 + z1) / 2)
    z0, z1 = TERRAZAS[-2], TERRAZAS[-1]
    return z0, z1, _alto_suave((z0 + z1) / 2)


def _asentar(z, lado, dz=0.0):
    """Lleva una casa al centro de su bancal sin que pise el muro: (z, lado, altura del suelo)."""
    z0, z1, y = _terraza(z)
    fondo = z0 - z1
    lado = min(lado, fondo * 0.74)
    holgura = max(0.0, (fondo - lado * 1.2) / 2)
    return (z0 + z1) / 2 + max(-holgura, min(holgura, dz)), lado, y


def _escalon_y(z):
    """Altura de la escalinata: llana sobre cada bancal y bajando en escalones al pie de cada muro."""
    z0, z1, abajo = _terraza(z)
    if z0 >= TERRAZAS[0] - 1e-6:
        return abajo
    arriba = _terraza(z0 + 0.01)[2]
    salto = arriba - abajo
    if salto < 0.02:
        return abajo
    d = min(max(salto / 0.17 * 0.30, 0.3), (z0 - z1) * 0.7)
    return arriba - salto * min(1.0, (z0 - z) / d)


def _en_cono(x, z, margen=0.0):
    return CONO_X[0] - margen <= x <= CONO_X[1] + margen and CONO_Z[0] - margen <= z <= CONO_Z[1] + margen


def hab13():
    """El barrio que se ve por la ventana y sobre las paredes: ladera en bancales con casas de colores y una
    escalinata. Tambien el suelo oscuro de fuera, para que nunca se vea el vacio. Coordenadas del cuarto.
    v3: bancales con muro de piedra; el cono de la ventana queda libre de casas grandes y lleva su propia vista."""
    m = Malla("HAB-13_barrio")
    v = Malla("HAB-13_arboles", "Follaje")
    tierra = mezclar(C["hierba_sombra"], C["oscuro"], 0.40)
    fria = mezclar(tierra, C["petroleo"], 0.45)

    def alto(z):          # v3: la ladera baja en bancales
        return _terraza(z)[2]

    def col_ladera(p):
        t = suave(-p[2], 3.0, 20.0)
        return mezclar(mezclar(tierra, C["hierba_sol"], 0.22), fria, t) * (1.0 + 0.05 * math.sin(p[0] * 1.7 + p[2]))
    # v2: la ladera llega mas lejos (con el encuadre mas alejado se veia el vacio en la esquina de arriba)
    xs = np.concatenate([[-36.0, -28.0], np.linspace(-20, 20, 11), [28.0, 36.0]])
    muro = mezclar(mezclar(C["piedra"], C["tierra1"], 0.35), PIEDRA_CALIDA, 0.25)
    remate = mezclar(PIEDRA_CALIDA, C["crema"], 0.25)
    for i, (z0, z1) in enumerate(zip(TERRAZAS[:-1], TERRAZAS[1:])):
        y = _alto_suave((z0 + z1) / 2)
        for x0, x1 in zip(xs[:-1], xs[1:]):
            cara(m, [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], ARRIBA, col_ladera)
        # muro del bancal: de la altura de este bancal a la del de delante, con su remate claro
        if i > 0:
            ya = _alto_suave((TERRAZAS[i - 1] + z0) / 2)
            if ya - y > 0.02:
                cara(m, [(xs[0], y, z0), (xs[-1], y, z0), (xs[-1], ya, z0), (xs[0], ya, z0)], (0, 0, 1),
                     lambda p, y=y, ya=ya: mezclar(mezclar(muro, C["petroleo"], 0.40), muro, suave(p[1], y, ya))
                     * (1.0 + 0.06 * math.sin(p[0] * 2.3)))
                cara(m, [(xs[0], ya + 0.05, z0 + 0.12), (xs[-1], ya + 0.05, z0 + 0.12), (xs[-1], ya + 0.05, z0),
                         (xs[0], ya + 0.05, z0)], ARRIBA, remate)
                cara(m, [(xs[0], ya, z0 + 0.12), (xs[-1], ya, z0 + 0.12), (xs[-1], ya + 0.05, z0 + 0.12),
                         (xs[0], ya + 0.05, z0 + 0.12)], (0, 0, 1), mezclar(remate, C["petroleo"], 0.25))
    # suelo de fuera, a la izquierda y delante del cuarto. v2: a la derecha (x > AX + G) baja la escalinata (HAB-18)
    xs2 = np.linspace(-36, AX + G, 9)
    zs2 = np.linspace(-2.6, 18, 7)
    for x0, x1 in zip(xs2[:-1], xs2[1:]):
        for z0, z1 in zip(zs2[:-1], zs2[1:]):
            cara(m, [(x0, BAJO, z0), (x1, BAJO, z0), (x1, BAJO, z1), (x0, BAJO, z1)], ARRIBA,
                 lambda p: mezclar(tierra, fria, 0.5 + 0.5 * math.sin(p[0] * 0.9) * math.cos(p[2] * 0.7)))
    # la escalinata, por detras de la ventana. v3: llana sobre cada bancal y en escalones al pie de cada muro
    piedra = mezclar(PIEDRA_CALIDA, C["tierra1"], 0.3)
    paso = 0.30
    for k in range(46):
        z = -3.05 - k * paso
        x = VX + 0.10 + 0.06 * (-(z + 3.6) / 0.55)
        arriba, abajo = _escalon_y(z) + 0.06, alto(z) - 0.10
        caja(m, (x, (arriba + abajo) / 2, z), (0.95, arriba - abajo, paso + 0.01), piedra, sombra=0.4,
             tapa=jit(mezclar(piedra, LUZ, 0.3), 0.04))
        # murete de los dos lados donde la escalera baja
        if arriba - alto(z) > 0.12:
            for s in (-1, 1):
                caja(m, (x + s * 0.53, (arriba + 0.16 + abajo) / 2, z), (0.11, arriba + 0.16 - abajo, paso + 0.01),
                     mezclar(muro, PIEDRA_CALIDA, 0.3), tapa=remate, sombra=0.4)
    colores = [mezclar(C["crema"], C["sol"], 0.25), mezclar(C["sol"], C["coral"], 0.3), mezclar(C["tierra1"], C["crema"], 0.4),
               mezclar(C["petroleo"], C["piedra_clara"], 0.45), mezclar(C["coral"], C["crema"], 0.45),
               mezclar(C["dorado"], C["crema"], 0.45)]
    # casas a la izquierda de la escalinata (las de la derecha caian dentro del cono de la ventana: v3 las quita)
    for i, (dx, z, lado, h) in enumerate(((-1.10, -3.95, 1.15, 1.35), (-1.25, -5.45, 1.30, 1.50), (-1.30, -7.10, 1.40, 1.60))):
        zc, lado, y = _asentar(z, lado)
        _casa(m, VX + dx - 0.15, y - 0.05, zc, lado, h, colores[(i * 4 + 1) % 6], (-0.10, 0.05, 0.10)[i])
    k = 0
    variedad = np.random.default_rng(20261315)
    for fila, z in enumerate((-4.6, -6.6, -8.9, -11.6, -14.8, -18.5, -23.0)):
        paso = 2.3 + 0.25 * fila
        x = -17.0 + (fila % 2) * 1.1
        while x < 17.0:
            lado = RNG.uniform(1.5, 2.0) * (1.0 + 0.08 * fila)
            if abs(x - (VX + 0.25 + 0.06 * (-(z + 3.6) / 0.55))) > 2.2 + lado / 2:   # deja libre la escalinata y sus casas
                dz, h, giro = RNG.uniform(-0.3, 0.3), RNG.uniform(1.3, 2.3), RNG.uniform(-0.12, 0.12)
                zc, lado2, y = _asentar(z, lado, dz)
                if not _en_cono(x, zc, lado2 / 2):
                    _casa_variada(m, v, variedad, x, y - 0.05, zc, lado2, h, colores[k % 6], giro)
                k += 1
            elif RNG.random() < 0.6:
                pass
            x += paso + RNG.uniform(0, 0.5)
    # copas de arboles entre las casas
    for _ in range(26):
        x, z = RNG.uniform(-16, 16), RNG.uniform(-20, -3.8)
        if abs(x - VX) < 1.2 and z > -9:
            continue
        r = RNG.uniform(0.5, 0.9)
        pts = fibonacci(12) * np.array([r, r * 0.8, r]) * RNG.uniform(0.8, 1.15, (12, 1))
        s = solido_facetado("copa", pts, HOJA_OSC, mezclar(HOJA, C["hierba_sombra"], 0.5), HOJA_CLARA, RNG, var=0.06,
                            material="Follaje")
        if not _en_cono(x, z, r):
            v.anexar(s, t=(x, alto(z) + r * 0.9, z))
    _vista_ventana(m, v, colores)
    return guardar("HAB-13_barrio", m, v)


def _casa_variada(m, v, rng, x, y, z, lado, alto, col, giro, tipo=None):
    """v3: casas del barrio menos repetidas: unas con tejado, otras con azotea (pretil, tanque o ropa tendida),
    algunas de dos plantas, y alguna maceta. Todo con un generador propio (no toca el RNG comun)."""
    azar = rng.random()
    if tipo is not None:
        azar = 0.2 if tipo == "tejado" else 0.7
    tipo = azar
    if tipo < 0.55:
        _casa(m, x, y, z, lado * rng.uniform(0.9, 1.1), alto * rng.uniform(0.85, 1.2), col, giro)
        return
    R = rot_y(giro)
    ancho, fondo = lado * rng.uniform(0.95, 1.25), lado * rng.uniform(0.8, 1.0)
    h = alto * (rng.uniform(1.15, 1.45) if tipo > 0.85 else rng.uniform(0.8, 1.05))
    caja(m, (x, y + h / 2, z), (ancho, h, fondo), col, R=R, sombra=0.42, var=0.05, tapa=mezclar(C["tierra1"], C["piedra"], 0.45))
    # pretil de la azotea
    pret = mezclar(col, C["crema"], 0.25)
    for (cx, cz, tx, tz) in ((0, fondo / 2 - 0.05, ancho, 0.10), (0, -fondo / 2 + 0.05, ancho, 0.10),
                             (-ancho / 2 + 0.05, 0, 0.10, fondo), (ancho / 2 - 0.05, 0, 0.10, fondo)):
        caja(m, np.array([x, y + h + 0.11, z]) + R @ np.array([cx, 0, cz]), (tx, 0.22, tz), pret, R=R, sombra=0.25,
             tapa=PIEDRA_CALIDA, var=0.02)
    if rng.random() < 0.5:           # tanque de agua
        c = np.array([x, y + h, z]) + R @ np.array([ancho * 0.22, 0, -fondo * 0.15])
        tanque = mezclar(C["petroleo"], C["piedra_clara"], 0.35)
        prisma(m, c, c + ARRIBA * 0.55, 0.26, n=8, ca=mezclar(tanque, C["petroleo"], 0.3), cb=tanque)
    else:                            # ropa tendida
        a = np.array([x, y + h + 0.55, z]) + R @ np.array([-ancho * 0.35, 0, 0.1])
        b = np.array([x, y + h + 0.55, z]) + R @ np.array([ancho * 0.35, 0, 0.1])
        viga(m, a, b, 0.012, mezclar(C["crema"], C["tierra1"], 0.4), tapas=False)
        telas = [mezclar(C["coral"], C["crema"], 0.25), mezclar(C["petroleo"], C["piedra_clara"], 0.5),
                 mezclar(C["dorado"], C["crema"], 0.3), mezclar(C["crema"], BLANCO, 0.5)]
        for t in (0.15, 0.42, 0.7):
            p = a + (b - a) * t
            q = p + (b - a) / np.linalg.norm(b - a) * 0.28
            col_t = telas[int(rng.integers(0, len(telas)))]
            v.quad(p, q, q - ARRIBA * 0.36, p - ARRIBA * 0.36, col_t, col_t, mezclar(col_t, C["petroleo"], 0.3),
                   mezclar(col_t, C["petroleo"], 0.3))
    # ventanas en la fachada que mira al cuarto
    hueco = mezclar(C["petroleo"], C["oscuro"], 0.35)
    pisos = 2 if h > alto * 1.1 else 1
    for piso in range(pisos):
        yv = y + h * (0.62 if pisos == 1 else (0.32 + 0.42 * piso))
        for sx in (-0.25, 0.25):
            c = np.array([x, yv, z]) + R @ np.array([sx * ancho, 0, fondo / 2 + 0.01])
            ex, ey = R @ np.array([lado * 0.09, 0, 0]), np.array([0, min(0.2, h * 0.14), 0])
            cara(m, [c - ex - ey, c + ex - ey, c + ex + ey, c - ex + ey], R @ np.array([0, 0, 1.0]), hueco)
            VENTANAS.append((c, ex, ey, R @ np.array([0, 0, 1.0])))


def _vista_ventana(m, v, colores):
    """v3: lo que se ve por la ventana del fondo, compuesto como la vista del concepto L05_A: la escalinata bajando
    entre dos bancales, casitas bajas a los dos lados vistas desde arriba (tejados y azoteas con ropa tendida), copas,
    macetas y un farol que de noche se enciende (HAB-19). Va donde mira el vano (VISTA_Z, medido): lo que esta mas
    cerca del muro no se ve por la ventana y lo que mide mas de 1 m asomaria cortado, por eso todo es bajo.
    Generador propio (no toca el RNG comun)."""
    rng = np.random.default_rng(20261316)
    barro = mezclar(C["terracota"], C["tierra2"], 0.35)

    def copa(x, z, r):
        y = _terraza(z)[2]
        prisma(m, (x, y, z), (x, y + r * 0.9, z), 0.045, 0.03, n=5, ca=MAD_OSC, cb=MAD)
        pts = fibonacci(12) * np.array([1.0, 0.8, 1.0]) * r * rng.uniform(0.85, 1.15, (12, 1))
        s = solido_facetado("copa", pts, HOJA_OSC, mezclar(HOJA, C["hierba_sombra"], 0.5), HOJA_CLARA, rng, var=0.06,
                            material="Follaje")
        v.anexar(s, t=(x, y + r * 0.9 + r * 0.5, z))

    def casita(x, z, lado, alto, col, tipo, giro=0.0):
        y = _terraza(z)[2] - 0.04
        _casa_variada(m, v, rng, x, y, z, lado, alto, col, giro, tipo=tipo)

    # derecha de la escalinata: dos filas de casitas por bancal, alternando tejado y azotea
    casita(2.15, -10.55, 0.90, 0.55, colores[1], "tejado", -0.06)
    casita(3.30, -10.70, 0.95, 0.50, colores[3], "azotea", 0.05)
    casita(2.30, -12.00, 0.85, 0.50, colores[4], "azotea", 0.04)
    casita(3.50, -12.05, 0.90, 0.55, colores[0], "tejado", -0.08)
    casita(2.50, -13.60, 0.95, 0.55, colores[5], "tejado", 0.06)
    casita(3.65, -13.70, 0.90, 0.50, colores[2], "azotea", -0.05)
    casita(2.65, -15.30, 0.90, 0.50, colores[3], "azotea", 0.03)
    casita(3.85, -15.40, 0.95, 0.55, colores[1], "tejado", -0.04)
    # izquierda de la escalinata (franja estrecha): copas y una casita al borde
    casita(-0.25, -12.10, 0.80, 0.50, colores[4], "tejado", 0.08)
    for x, z, r in ((0.20, -10.9, 0.30), (0.40, -13.5, 0.34), (0.55, -15.7, 0.30), (2.85, -11.35, 0.26),
                    (3.05, -14.75, 0.30), (4.45, -11.4, 0.36), (4.60, -14.4, 0.38), (1.95, -14.6, 0.24)):
        copa(x, z, r)
    # macetas de barro junto a la escalinata
    for x, z in ((0.45, -10.2), (1.70, -11.4), (0.75, -12.5), (1.95, -13.1), (1.00, -14.2), (2.10, -15.9)):
        y = _terraza(z)[2]
        prisma(m, (x, y, z), (x, y + 0.14, z), 0.08, 0.11, n=7, ca=mezclar(barro, C["petroleo"], 0.3), cb=barro)
        _mata_local(v, rng, (x, y + 0.2, z), 6, 2, 0.10)
    # farol de la escalinata, junto al muro del bancal (de noche lo enciende HAB-19)
    for x, z in ((0.50, -12.55),):
        y = _terraza(z)[2]
        viga(m, (x, y, z), (x, y + 0.75, z), 0.04, HIERRO)
        lamp = np.array([x, y + 0.82, z])
        caja(m, lamp, (0.10, 0.13, 0.10), mezclar(C["sol"], C["crema"], 0.45), sombra=0.0, luz=0.6, tapa=HIERRO)
        LUCES.append((lamp, 0.055))


def _mata_local(v, rng, base, n_hojas, n_flores, radio):
    """Como _mata, con un generador propio."""
    base = np.asarray(base, float)
    for _ in range(n_hojas):
        d = np.array([rng.normal(0, 1), rng.normal(0.2, 0.7), abs(rng.normal(0.5, 0.5))])
        o = base + rng.normal(0, radio, 3) * np.array([1, 0.6, 0.35])
        hoja(v, o, d, np.array([rng.normal(0, 0.3), 0.5, 1.0]), rng.uniform(0.10, 0.15), rng.uniform(0.07, 0.09),
             HOJA_OSC, HOJA if rng.random() < 0.6 else HOJA_CLARA)
    for _ in range(n_flores):
        o = base + rng.normal(0, radio, 3) * np.array([1, 0.6, 0.3]) + np.array([0, 0.03, 0.05])
        flor(v, o, np.array([rng.normal(0, 0.3), 0.6, 1.0]), rng.uniform(0.045, 0.065), FLOR,
             mezclar(C["dorado"], C["crema"], 0.4), petalos=5, rng=rng)


def _mata(v, base, n_hojas, n_flores, radio, caida=0.25):
    base = np.asarray(base, float)
    for _ in range(n_hojas):
        d = np.array([RNG.normal(0, 1), RNG.normal(-caida, 0.7), abs(RNG.normal(0.5, 0.5))])
        o = base + RNG.normal(0, radio, 3) * np.array([1, 0.6, 0.35]) + np.array([0, 0, 0.04])
        hoja(v, o, d, np.array([RNG.normal(0, 0.3), 0.5, 1.0]), RNG.uniform(0.12, 0.19), RNG.uniform(0.08, 0.11),
             jit(HOJA_OSC, 0.08), jit(HOJA if RNG.random() < 0.6 else HOJA_CLARA, 0.08))
    for _ in range(n_flores):
        o = base + RNG.normal(0, radio, 3) * np.array([1, 0.6, 0.3]) + np.array([0, 0, 0.10])
        flor(v, o, np.array([RNG.normal(0, 0.3), 0.35, 1.0]), RNG.uniform(0.055, 0.085),
             jit(FLOR if RNG.random() < 0.65 else FLOR_CLARA, 0.06), mezclar(C["dorado"], C["crema"], 0.4), petalos=5, rng=RNG)


def hab14():
    """Buganvilla que cuelga sobre la ventana. x centrado en la ventana, y desde el suelo, z = 0 en la pared."""
    v = Malla("HAB-14_buganvilla", "Follaje")
    t = Malla("HAB-14_tallos")
    # guia: baja desde lo alto del muro, cruza el arco y cuelga a la izquierda
    guia = [(-1.75, 2.28), (-1.35, 2.20), (-0.95, 2.26), (-0.55, 2.18), (-0.15, 2.24), (0.25, 2.16), (0.60, 2.22),
            (0.95, 2.12), (1.25, 2.20)]
    for (x0, y0), (x1, y1) in zip(guia[:-1], guia[1:]):
        viga(t, (x0, y0, 0.05), (x1, y1, 0.05), 0.022, MAD_OSC, tapas=False)
    for x, y in guia:
        _mata(v, (x, y, 0.06), 12, 5, 0.14)
    for x, largo in ((-1.55, 0.9), (-1.05, 1.15), (-0.85, 0.5), (0.9, 0.45), (-0.3, 0.25), (0.35, 0.22)):
        n = max(2, int(largo / 0.2))
        for k in range(1, n + 1):
            _mata(v, (x + RNG.normal(0, 0.04), 2.2 - k * largo / n, 0.05), 6, 3 if k < n else 4, 0.09, caida=0.6)
        viga(t, (x, 2.2, 0.04), (x + 0.03, 2.2 - largo, 0.04), 0.014, MAD_OSC, tapas=False)
    return guardar("HAB-14_buganvilla", t, v)


def hab15():
    """Maceta colgante con potus. Origen en el borde de la maceta; la pared queda en z = -0.30."""
    m = Malla("HAB-15_maceta")
    v = Malla("HAB-15_potus", "Follaje")
    barro = mezclar(C["terracota"], C["tierra2"], 0.35)
    prisma(m, (0, -0.17, 0), (0, 0.0, 0), 0.10, 0.14, n=8, ca=mezclar(barro, C["petroleo"], 0.3), cb=barro, tapa_a=True,
           tapa_b=False)
    cara(m, [(math.cos(k / 8 * 2 * math.pi) * 0.13, -0.02, math.sin(k / 8 * 2 * math.pi) * 0.13) for k in range(8)],
         ARRIBA, mezclar(C["madera2"], C["oscuro"], 0.3))
    gancho = np.array([0.0, 0.62, 0.0])
    cuerda = mezclar(C["crema"], C["tierra1"], 0.4)
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.5
        viga(m, (math.cos(a) * 0.135, -0.01, math.sin(a) * 0.135), gancho, 0.012, cuerda, tapas=False)
    viga(m, (0, 0.66, -0.30), (0, 0.66, 0.03), 0.035, MAD)                              # el brazo de la pared
    viga(m, (0, 0.44, -0.29), (0, 0.65, -0.08), 0.03, MAD_OSC, tapas=False)
    claro = mezclar(HOJA_CLARA, C["crema"], 0.15)
    for k in range(9):                                   # copa
        a = k * 2.4
        hoja(v, (math.cos(a) * 0.05, 0.0, math.sin(a) * 0.05), (math.cos(a), 0.9, math.sin(a)), (math.cos(a), 1.0, math.sin(a)),
             RNG.uniform(0.16, 0.22), 0.12, jit(HOJA, 0.06), jit(claro, 0.06))
    for k in range(6):                                   # guias que cuelgan
        a = k * 2 * math.pi / 6 + RNG.uniform(-0.3, 0.3)
        largo = RNG.uniform(0.45, 0.95)
        fuera = np.array([math.cos(a), 0, math.sin(a)])
        n = int(largo / 0.11)
        for i in range(n):
            s = (i + 0.5) / n
            p = fuera * (0.13 + 0.06 * math.sin(s * 2.5)) + np.array([0, 0.02 - s * largo, 0])
            lado = np.cross(fuera, ARRIBA) * (1 if i % 2 else -1)
            hoja(v, p, fuera * 0.5 + lado * 0.8 - ARRIBA * 0.7, fuera + ARRIBA * 0.5, RNG.uniform(0.11, 0.15), 0.095,
                 jit(HOJA, 0.07), jit(claro if RNG.random() < 0.6 else HOJA_CLARA, 0.07))
    return guardar("HAB-15_maceta", m, v)


def hab16():
    m = Malla("HAB-16_macetero")
    prisma(m, (0, 0, 0), (0, 0.22, 0), 0.22, 0.27, n=9, ca=mezclar(MAD, C["petroleo"], 0.3), cb=MAD, tapa_b=False)
    prisma(m, (0, 0.22, 0), (0, 0.42, 0), 0.27, 0.24, n=9, ca=MAD, cb=MAD_CLARA, tapa_b=False)
    for y, r in ((0.09, 0.245), (0.33, 0.262)):
        prisma(m, (0, y, 0), (0, y + 0.035, 0), r, n=9, ca=HIERRO, tapa_b=False)
    cara(m, [(math.cos(k / 9 * 2 * math.pi) * 0.235, 0.39, math.sin(k / 9 * 2 * math.pi) * 0.235) for k in range(9)],
         ARRIBA, mezclar(C["madera2"], C["oscuro"], 0.35))
    return guardar("HAB-16_macetero", m)


def hab17():
    """Cuadrito: una lamina del rio al atardecer, sujeta con cinta. Sin texto."""
    m = Malla("HAB-17_cuadrito")
    W, H = 0.44, 0.31
    papel = mezclar(C["crema"], BLANCO, 0.5)
    caja(m, (0, 0, 0.006), (W, H, 0.012), papel, sombra=0.1)
    a, b, z = W / 2 - 0.025, H / 2 - 0.025, 0.014
    cara(m, [(-a, -0.02, z), (a, -0.02, z), (a, b, z), (-a, b, z)], (0, 0, 1),
         lambda p: mezclar(mezclar(C["sol"], C["crema"], 0.4), mezclar(C["petroleo"], C["piedra_clara"], 0.5), (p[1] + 0.02) / (b + 0.02)))
    cara(m, [(-a, -b, z), (a, -b, z), (a, -0.02, z), (-a, -0.02, z)], (0, 0, 1),
         lambda p: mezclar(mezclar(C["petroleo"], C["cian_medio"], 0.25), mezclar(C["petroleo"], C["piedra_clara"], 0.4), (p[1] + b) / (b - 0.02)))
    z += 0.002
    for x, s in ((-0.08, 1.0), (0.07, 0.7)):
        cara(m, [(x - 0.035 * s, -0.045, z), (x + 0.035 * s, -0.045, z), (x + 0.025 * s, -0.06, z), (x - 0.025 * s, -0.06, z)],
             (0, 0, 1), MAD_OSC)
        cara(m, [(x, -0.04, z), (x + 0.03 * s, -0.04, z), (x, 0.02 * s, z)], (0, 0, 1), papel)
    cara(m, [(0.10, -0.02, z), (a, -0.02, z), (a, 0.01, z), (0.14, 0.025, z)], (0, 0, 1), HOJA_OSC)
    caja(m, (0, H / 2 - 0.005, 0.016), (0.07, 0.035, 0.004), mezclar(C["crema"], C["dorado"], 0.3), sombra=0.0)
    return guardar("HAB-17_cuadrito", m)


# ---------- v2: HAB-18 exterior de la derecha y HAB-19 ventanas encendidas ----------
# Van al final de main(): asi no cambian la secuencia aleatoria (RNG) de los modelos anteriores.

HUECO = mezclar(C["petroleo"], C["oscuro"], 0.35)
LUCES = []                   # faroles de la calle: (centro, medio_lado) para HAB-19


def _alto_ladera(z):
    """La misma ladera de HAB-13 (v3: en bancales)."""
    return _terraza(z)[2]


def _degradado(col, y0, y1, sombra=0.45):
    """Color de una pared: mas oscuro y frio abajo (sombra petroleo), el color pleno arriba."""
    return lambda p: mezclar(mezclar(col, C["petroleo"], sombra), col, suave(p[1], y0, y1))


def _pared(m, a, b, y0, y1, hacia, col):
    """Pared vertical entre los puntos a y b del suelo (x, z), de y0 a y1."""
    cara(m, [(a[0], y0, a[1]), (b[0], y0, b[1]), (b[0], y1, b[1]), (a[0], y1, a[1])], hacia, col)


def _ventana(m, c, n, w, h, postigo=None, registrar=True, puerta=False):
    """Ventana (o puerta) sobre una fachada de normal n: marco, hueco oscuro y postigos abiertos."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    u = np.cross(ARRIBA, n)
    c = np.asarray(c, float) + n * 0.008
    ex, ey = u * w, ARRIBA * h
    marco_col = mezclar(PIEDRA_CALIDA, C["crema"], 0.3)
    cara(m, [c - ex * 1.22 - ey * 1.12, c + ex * 1.22 - ey * 1.12, c + ex * 1.22 + ey * 1.12, c - ex * 1.22 + ey * 1.12], n,
         marco_col)
    c2 = c + n * 0.006
    cara(m, [c2 - ex - ey, c2 + ex - ey, c2 + ex + ey, c2 - ex + ey], n, MAD_OSC if puerta else HUECO)
    if postigo is not None:
        for s in (-1, 1):
            pc = c + n * 0.01 + u * s * w * 1.85
            cara(m, [pc - u * w * 0.55 - ey, pc + u * w * 0.55 - ey, pc + u * w * 0.55 + ey, pc - u * w * 0.55 + ey], n,
                 jit(postigo, 0.05))
    if registrar and not puerta:
        VENTANAS.append((c2, ex, ey, n))


def _tejado(m, x0, x1, z0, z1, y, alto, vuelo=0.2):
    """Tejado a cuatro aguas sobre un rectangulo, de teja, con la cumbrera a lo largo del lado mayor.
    v3: alero mas ancho y cada agua con su tono (la de la izquierda, al sol; la de la derecha y la de atras, en
    sombra), para que se lea como volumen."""
    x0, x1, z0, z1 = x0 - vuelo, x1 + vuelo, z0 - vuelo, z1 + vuelo
    yt = y + alto
    teja_b, teja_a = jit(mezclar(TEJA, C["madera2"], 0.28), 0.04), jit(mezclar(TEJA, C["sol"], 0.28), 0.04)
    tonos = {(0, 1, 1): 0.90, (-1, 1, 0): 1.10, (1, 1, 0): 0.70, (0, 1, -1): 0.62}

    def col(p, f=1.0):
        return np.clip(mezclar(teja_b, teja_a, suave(p[1], y, yt)) * f, 0, 1)

    def agua(pts, n):
        cara(m, pts, n, lambda p, f=tonos[n]: col(p, f))

    def hiladas(A, B, Ar, Br, n):
        # filas de teja: franjas oscuras finas paralelas al alero (A-B) que suben hacia la cumbrera (Ar-Br)
        A, B, Ar, Br = (np.asarray(q, float) for q in (A, B, Ar, Br))
        nrm = np.cross(B - A, Ar - A)
        nrm = nrm / np.linalg.norm(nrm)
        if nrm[1] < 0:
            nrm = -nrm
        for k in range(1, 5):
            t0, t1 = k / 5.0, k / 5.0 + 0.045
            P0, Q0 = A + (Ar - A) * t0 + nrm * 0.008, B + (Br - B) * t0 + nrm * 0.008
            P1, Q1 = A + (Ar - A) * t1 + nrm * 0.008, B + (Br - B) * t1 + nrm * 0.008
            if np.linalg.norm(Q0 - P0) < 0.05:
                continue
            cara(m, [P0, Q0, Q1, P1], n, mezclar(teja_b, C["madera2"], 0.35) * tonos[n])
    if x1 - x0 >= z1 - z0:
        d, cz = (z1 - z0) / 2, (z0 + z1) / 2
        hiladas((x0, y, z1), (x1, y, z1), (x0 + d, yt, cz), (x1 - d, yt, cz), (0, 1, 1))
        hiladas((x0, y, z0), (x0, y, z1), (x0 + d, yt, cz), (x0 + d, yt, cz), (-1, 1, 0))
    else:
        d, cx = (x1 - x0) / 2, (x0 + x1) / 2
        hiladas((x0, y, z0), (x0, y, z1), (cx, yt, z0 + d), (cx, yt, z1 - d), (-1, 1, 0))
        hiladas((x0, y, z1), (x1, y, z1), (cx, yt, z1 - d), (cx, yt, z1 - d), (0, 1, 1))
    if x1 - x0 >= z1 - z0:
        d, cz = (z1 - z0) / 2, (z0 + z1) / 2
        a, b = (x0 + d, yt, cz), (x1 - d, yt, cz)
        agua([(x0, y, z1), (x1, y, z1), b, a], (0, 1, 1))
        agua([(x0, y, z0), (x1, y, z0), b, a], (0, 1, -1))
        agua([(x0, y, z0), (x0, y, z1), a], (-1, 1, 0))
        agua([(x1, y, z0), (x1, y, z1), b], (1, 1, 0))
        viga(m, a, b, 0.07, mezclar(TEJA, C["madera2"], 0.45))
    else:
        d, cx = (x1 - x0) / 2, (x0 + x1) / 2
        a, b = (cx, yt, z0 + d), (cx, yt, z1 - d)
        agua([(x0, y, z0), (x0, y, z1), b, a], (-1, 1, 0))
        agua([(x1, y, z0), (x1, y, z1), b, a], (1, 1, 0))
        agua([(x0, y, z0), (x1, y, z0), a], (0, 1, -1))
        agua([(x0, y, z1), (x1, y, z1), b], (0, 1, 1))
        viga(m, a, b, 0.07, mezclar(TEJA, C["madera2"], 0.45))
    # canto del alero (se lee como el grosor de la teja) y su sombra por debajo
    for (pa, pb, n) in (((x0, z1), (x1, z1), (0, 0, 1)), ((x0, z0), (x0, z1), (-1, 0, 0))):
        _pared(m, pa, pb, y - 0.09, y, n, mezclar(TEJA, C["madera2"], 0.6))
    cara(m, [(x0, y - 0.09, z0), (x1, y - 0.09, z0), (x1, y - 0.09, z1), (x0, y - 0.09, z1)], (0, -1, 0),
         mezclar(TEJA, C["oscuro"], 0.55))


def _suelo_baldosas(m, x0, x1, z0, z1, y, tonos, paso=0.5, borde=0.0):
    """Suelo de losas con junta oscura: adoquines, azoteas, terrazas."""
    junta = mezclar(tonos[0], C["oscuro"], 0.45)
    cara(m, [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], ARRIBA, junta)
    nx, nz = max(1, int(round((x1 - x0) / paso))), max(1, int(round((z1 - z0) / paso)))
    dx, dz = (x1 - x0) / nx, (z1 - z0) / nz
    j = min(dx, dz) * 0.06
    for i in range(nx):
        for k in range(nz):
            off = (dx * 0.5) if (k % 2 and borde == 0.0) else 0.0
            xa = x0 + i * dx + j + off
            xb = min(x1, x0 + (i + 1) * dx - j + off)
            if xb - xa < dx * 0.3:
                continue
            za, zb = z0 + k * dz + j, z0 + (k + 1) * dz - j
            col = jit(tonos[RNG.integers(0, len(tonos))], 0.05)
            cara(m, [(xa, y + 0.006, za), (xb, y + 0.006, za), (xb, y + 0.006, zb), (xa, y + 0.006, zb)], ARRIBA, col)


def _copa(v, c, r, escala=(1.0, 0.8, 1.0)):
    pts = fibonacci(12) * np.array(escala) * r * RNG.uniform(0.85, 1.15, (12, 1))
    s = solido_facetado("copa", pts, HOJA_OSC, mezclar(HOJA, C["hierba_sombra"], 0.5), HOJA_CLARA, RNG, var=0.06,
                        material="Follaje")
    v.anexar(s, t=c)


def _arbol(m, v, x, y, z, alto=1.6, r=0.8):
    prisma(m, (x, y, z), (x, y + alto, z), 0.09, 0.06, n=5, ca=MAD_OSC, cb=MAD)
    _copa(v, (x, y + alto + r * 0.45, z), r)
    _copa(v, (x + r * 0.55, y + alto + r * 0.1, z + 0.2), r * 0.6)


def _maceta(m, v, x, y, z, r=0.13, flores=True):
    barro = mezclar(C["terracota"], C["tierra2"], 0.35)
    prisma(m, (x, y, z), (x, y + r * 1.4, z), r * 0.8, r, n=7, ca=mezclar(barro, C["petroleo"], 0.3), cb=barro)
    _mata(v, (x, y + r * 1.6, z - 0.04), 9, 4 if flores else 0, r * 0.9, caida=-0.2)


def _casa_rect(m, x0, x1, z0, z1, y0, y1, col, tejado=0.55, ventanas=((0, 0, 1),), postigo=None, puerta=None):
    """Casa de bloque con tejado; ventanas en las fachadas que se ven (+Z y -X)."""
    caja(m, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0), col, sombra=0.42, var=0.04)
    if tejado:
        _tejado(m, x0, x1, z0, z1, y1, tejado)
    yv = y1 - min(0.62, (y1 - y0) * 0.35)
    for n in ventanas:
        n = np.asarray(n, float)
        if n[2] > 0:
            ancho = x1 - x0
            k = max(1, int(ancho / 1.0))
            for i in range(k):
                x = x0 + (i + 0.5) * ancho / k
                if puerta is not None and abs(x - puerta) < 0.45:
                    continue
                _ventana(m, (x, yv, z1), n, 0.13, 0.19, postigo)
            if puerta is not None:
                _ventana(m, (puerta, y0 + 0.5, z1), n, 0.2, 0.42, puerta=True)
        else:
            fondo = z1 - z0
            k = max(1, int(fondo / 1.1))
            for i in range(k):
                _ventana(m, (x0, yv, z0 + (i + 0.5) * fondo / k), n, 0.13, 0.19, postigo)


def hab18():
    """Exterior de la derecha (v2): la escalinata baja desde el descanso hasta una calle de adoquines, entre la casa
    del vecino (azotea con tanque, ropa tendida y macetas) y una casa mas baja con tejado; mas abajo, terrazas de
    Las Escalinatas con casas y arboles; y a la izquierda y al fondo, mas barrio para el encuadre alejado.
    Tambien el muro que une la pared derecha del cuarto con el muro del arco: cierra el hueco detras del descanso.
    Coordenadas del cuarto, como HAB-12."""
    m = Malla("HAB-18_exterior")
    v = Malla("HAB-18_follaje", "Follaje")
    E0 = AX + G                      # cara de fuera de la pared derecha (3.55)
    XI, XA = AX + 0.95, AX + 0.95 + G    # muro del arco: cara de dentro y de fuera (4.25 y 4.5)
    ZC0, ZC1 = 1.35, 2.35            # ancho de la escalinata (como HAB-09)
    piedra = mezclar(PIEDRA_CALIDA, C["tierra1"], 0.35)
    alto_m = 1.35
    YC = -2.52                       # la calle de abajo
    YT = -3.3                        # las terrazas de mas abajo
    FONDO = -3.6

    # 1. muro que une la pared derecha con el muro del arco: detras del descanso ya no queda hueco
    z0, z1 = PARED_DER_FIN - G, PARED_DER_FIN
    _pared(m, (E0, z1), (XI, z1), -0.7, alto_m, (0, 0, 1), _degradado(PARED, -0.7, alto_m, 0.35))
    cara(m, [(AX, alto_m, z0), (XA, alto_m, z0), (XA, alto_m, z1), (AX, alto_m, z1)], ARRIBA, CORTE)

    # 2. la escalinata sigue bajando (los 7 primeros escalones estan en HAB-09) hasta la calle
    for i in range(7, 14):
        y = -(i + 1) * 0.18
        caja(m, (AX + 0.83 + 0.26 * i, (y + FONDO) / 2, (ZC0 + ZC1) / 2), (0.26, y - FONDO, 1.0), piedra, sombra=0.35,
             tapa=jit(mezclar(piedra, LUZ, 0.25), 0.04))
    # murete de la derecha, escalonado, y pasamanos de hierro a la izquierda
    for i in range(1, 14):
        y = -(i + 1) * 0.18
        x = AX + 0.83 + 0.26 * i
        if x - 0.13 < XA:
            continue
        caja(m, (x, (y + 0.42 + FONDO) / 2, ZC1 + 0.07), (0.26, y + 0.42 - FONDO, 0.14), mezclar(PARED_BAJA, PARED, 0.35),
             tapa=CORTE, sombra=0.4)
    viga(m, (XA + 0.05, -0.42 + 0.78, ZC0 + 0.05), (AX + 0.83 + 0.26 * 13, YC + 0.78, ZC0 + 0.05), 0.035, HIERRO)
    for i in (3, 7, 11):
        x = AX + 0.83 + 0.26 * i
        viga(m, (x, -(i + 1) * 0.18, ZC0 + 0.05), (x, -(i + 1) * 0.18 + 0.78, ZC0 + 0.05), 0.03, HIERRO)

    # 3. la casa del vecino, detras y a la izquierda de la escalinata, con azotea
    YA = -0.30
    colA = mezclar(C["dorado"], C["crema"], 0.45)
    xA1, zA0, zA1 = 7.4, -AZ - G, ZC0 - 0.05
    _pared(m, (XA, zA1), (xA1, zA1), FONDO, YA, (0, 0, 1), _degradado(colA, -2.6, YA, 0.5))
    _pared(m, (xA1, zA0), (xA1, zA1), FONDO, YA, (1, 0, 0), _degradado(colA, -2.6, YA, 0.6))
    for x, y in ((5.25, -1.15), (6.55, -1.15)):
        _ventana(m, (x, y, zA1), (0, 0, 1), 0.15, 0.22, VERDE_AZUL)
    _ventana(m, (5.9, YC + 0.48, zA1), (0, 0, 1), 0.2, 0.42, puerta=True)
    # zocalo del vecino y la azotea
    _pared(m, (XA, zA1 + 0.004), (xA1, zA1 + 0.004), FONDO, YC + 0.3, (0, 0, 1), mezclar(colA, C["terracota"], 0.45))
    _suelo_baldosas(m, E0, xA1, zA0, zA1, YA, [mezclar(C["tierra1"], C["piedra"], 0.5), mezclar(C["tierra2"], C["piedra"], 0.4),
                                                 mezclar(C["tierra1"], C["crema"], 0.3)], paso=0.55, borde=1.0)
    pret = mezclar(colA, C["crema"], 0.2)
    caja(m, ((XA + xA1) / 2, YA + 0.22, zA1 - 0.07), (xA1 - XA, 0.44, 0.14), pret, tapa=PIEDRA_CALIDA, sombra=0.3)
    caja(m, (xA1 - 0.07, YA + 0.22, (zA0 + zA1) / 2), (0.14, 0.44, zA1 - zA0), pret, tapa=PIEDRA_CALIDA, sombra=0.3)
    caja(m, ((E0 + xA1) / 2, YA + 0.22, zA0 + 0.07), (xA1 - E0, 0.44, 0.14), pret, tapa=PIEDRA_CALIDA, sombra=0.3)
    # caseta de la escalera de la azotea, tanque de agua, ropa tendida y macetas
    caja(m, (4.25, YA + 0.6, -2.05), (1.2, 1.2, 1.1), colA, tapa=CORTE, sombra=0.4)
    _ventana(m, (4.25, YA + 0.42, -1.5), (0, 0, 1), 0.2, 0.4, puerta=True)
    tanque = mezclar(C["petroleo"], C["piedra_clara"], 0.35)
    for sx in (-1, 1):
        for sz in (-1, 1):
            viga(m, (6.55 + sx * 0.28, YA, -1.85 + sz * 0.28), (6.55 + sx * 0.28, YA + 0.32, -1.85 + sz * 0.28), 0.05, HIERRO)
    prisma(m, (6.55, YA + 0.32, -1.85), (6.55, YA + 1.1, -1.85), 0.42, n=9, ca=mezclar(tanque, C["petroleo"], 0.3), cb=tanque)
    prisma(m, (6.55, YA + 1.1, -1.85), (6.55, YA + 1.2, -1.85), 0.42, 0.15, n=9, ca=tanque, cb=mezclar(tanque, C["crema"], 0.3))
    pa, pb = np.array([4.95, YA, -0.55]), np.array([7.05, YA, 0.55])
    for p in (pa, pb):
        viga(m, p, p + ARRIBA * 1.35, 0.05, MAD_OSC)
    cuerda = mezclar(C["crema"], C["tierra1"], 0.4)
    ca, cb = pa + ARRIBA * 1.3, pb + ARRIBA * 1.3
    viga(m, ca, cb, 0.012, cuerda, tapas=False)
    telas = [mezclar(C["coral"], C["crema"], 0.25), mezclar(C["petroleo"], C["piedra_clara"], 0.5), mezclar(C["dorado"], C["crema"], 0.3),
             mezclar(C["crema"], BLANCO, 0.5), mezclar(C["tierra1"], C["coral"], 0.3)]
    eje = (cb - ca) / np.linalg.norm(cb - ca)
    for k, (t, ancho, largo) in enumerate(((0.15, 0.30, 0.42), (0.32, 0.36, 0.55), (0.50, 0.26, 0.36), (0.66, 0.40, 0.48),
                                           (0.84, 0.24, 0.34))):
        a = ca + (cb - ca) * t
        b = a + eje * ancho
        col = jit(telas[k], 0.04)
        sombra = mezclar(col, C["petroleo"], 0.3)
        v.quad(a, b, b - ARRIBA * largo + np.array([0, 0, 0.04]), a - ARRIBA * largo + np.array([0, 0, 0.04]), col, col, sombra, sombra)
    for x in (5.2, 5.75, 6.3):
        _maceta(m, v, x, YA, zA1 - 0.32)
    _maceta(m, v, 7.05, YA, -0.9, 0.16, flores=False)

    # 4. la casa de abajo, a la derecha de la escalinata, con tejado
    xB0, xB1, zB0, zB1 = 4.6, 7.4, ZC1 + 0.14, 5.6
    colB = mezclar(C["petroleo"], C["piedra_clara"], 0.45)
    # v3: tejado con mas pendiente y alero, para que se lea como volumen y no como una alfombra
    _casa_rect(m, xB0, xB1, zB0, zB1, FONDO, -0.95, colB, tejado=1.05, ventanas=((0, 0, 1), (-1, 0, 0)), postigo=MAD_CLARA,
               puerta=6.0)
    # franja de jardin entre el descanso y la casa de abajo, al nivel del suelo de fuera
    tierra = mezclar(C["hierba_sombra"], C["oscuro"], 0.40)
    cara(m, [(E0, BAJO, AZ + 0.2), (xB0, BAJO, AZ + 0.2), (xB0, BAJO, 18.0), (E0, BAJO, 18.0)], ARRIBA,
         lambda p: mezclar(tierra, mezclar(tierra, C["hierba_sol"], 0.25), 0.5 + 0.5 * math.sin(p[2] * 1.3)))
    _pared(m, (XA, ZC1 + 0.14), (xB0, ZC1 + 0.14), FONDO, BAJO, (0, 0, 1), _degradado(PARED_BAJA, -2.6, BAJO))

    # 5. la calle de adoquines y su farol
    xS0, xS1 = 7.4, 9.6
    _suelo_baldosas(m, xS0, xS1, -2.6, 18.0, YC, [mezclar(piedra, C["piedra"], 0.4), mezclar(piedra, C["tierra2"], 0.3),
                                                  mezclar(C["piedra"], C["petroleo"], 0.2)], paso=0.42)
    for z in (1.0, 7.5):
        base = np.array([9.25, YC, z])
        viga(m, base, base + ARRIBA * 1.7, 0.07, HIERRO)
        viga(m, base + ARRIBA * 1.62, base + ARRIBA * 1.62 + np.array([-0.32, 0, 0]), 0.035, HIERRO)
        lamp = base + np.array([-0.32, 1.42, 0])
        caja(m, lamp, (0.13, 0.2, 0.13), mezclar(C["sol"], C["crema"], 0.45), sombra=0.0, luz=0.6, tapa=HIERRO)
        prisma(m, lamp + ARRIBA * 0.1, lamp + ARRIBA * 0.2, 0.12, 0.02, n=4, ca=HIERRO, giro=math.pi / 4)
        LUCES.append((lamp, 0.075))
    # muro de contencion bajo la ladera, con enredadera
    muro = mezclar(C["piedra"], C["piedra_osc"], 0.35)
    _pared(m, (xA1, -2.6), (36.0, -2.6), YT - 0.3, _alto_ladera(-2.6), (0, 0, 1), _degradado(muro, YT, -0.9, 0.45))
    for x in np.arange(9.0, 35.0, 2.6):              # contrafuertes con su remate
        caja(m, (x, (YT - 0.3 + _alto_ladera(-2.6)) / 2, -2.5), (0.32, _alto_ladera(-2.6) - YT + 0.3, 0.2),
             mezclar(muro, C["tierra1"], 0.25), tapa=CORTE, sombra=0.45)
    for x in np.arange(8.0, 34.0, 1.7):
        _mata(v, (x + RNG.uniform(-0.3, 0.3), -1.2 + RNG.uniform(-0.3, 0.2), -2.55), 8, 2, 0.22, caida=0.6)

    # 6. delante: la calle se abre en una placita con dos casas y arboles
    cara(m, [(xB0, YC, zB1), (xS0, YC, zB1), (xS0, YC, 18.0), (xB0, YC, 18.0)], ARRIBA, mezclar(piedra, C["tierra2"], 0.4))
    _casa_rect(m, 4.7, 6.6, 8.2, 10.0, YC, -1.0, mezclar(C["coral"], C["crema"], 0.45), tejado=0.55, postigo=VERDE_AZUL,
               ventanas=((0, 0, 1), (-1, 0, 0)))
    _arbol(m, v, 6.9, YC, 6.6, 1.5, 0.75)
    _arbol(m, v, 5.0, YC, 11.6, 1.7, 0.85)

    # 7. las terrazas de mas abajo: casas en filas, tejados y copas de arboles
    cara(m, [(xS1, YT, -2.6), (40.0, YT, -2.6), (40.0, YT, 20.0), (xS1, YT, 20.0)], ARRIBA,
         lambda p: mezclar(tierra, mezclar(tierra, C["petroleo"], 0.4), suave(p[0], 12.0, 30.0)))
    cara(m, [(xS1, YT, -2.6), (xS1, YT, 20.0), (xS1, YC, 20.0), (xS1, YC, -2.6)], (-1, 0, 0), _degradado(piedra, YT, YC))
    colores = [mezclar(C["crema"], C["sol"], 0.25), mezclar(C["sol"], C["coral"], 0.3), mezclar(C["tierra1"], C["crema"], 0.4),
               mezclar(C["petroleo"], C["piedra_clara"], 0.45), mezclar(C["coral"], C["crema"], 0.45),
               mezclar(C["dorado"], C["crema"], 0.45)]
    k = 0
    for fila, z in enumerate((-1.3, 2.3, 5.9, 9.5, 13.1, 16.7)):
        x = xS1 + 1.2 + (fila % 2) * 0.9
        while x < 34.0:
            lado = RNG.uniform(1.4, 1.9)
            if RNG.random() < 0.82:
                _casa(m, x, YT, z + RNG.uniform(-0.25, 0.25), lado, RNG.uniform(1.2, 2.0), colores[k % 6], RNG.uniform(-0.1, 0.1))
                k += 1
            else:
                _arbol(m, v, x, YT, z, RNG.uniform(1.2, 1.8), RNG.uniform(0.6, 0.85))
            if RNG.random() < 0.45:
                _copa(v, (x + lado * 0.75, YT + RNG.uniform(1.1, 1.6), z + 0.9), RNG.uniform(0.5, 0.75))
            x += lado + RNG.uniform(0.7, 1.3)

    # 8. mas barrio para el encuadre alejado: a la izquierda, al nivel del suelo de fuera, y lejos, en la ladera
    for fila, z in enumerate((-1.6, 2.0, 5.6, 9.2, 12.8)):
        x = -7.6 - (fila % 2) * 0.9
        while x > -34.0:
            lado = RNG.uniform(1.4, 1.9)
            if RNG.random() < 0.8:
                _casa(m, x, BAJO, z + RNG.uniform(-0.25, 0.25), lado, RNG.uniform(1.2, 1.9), colores[k % 6], RNG.uniform(-0.1, 0.1))
                k += 1
            else:
                _arbol(m, v, x, BAJO, z, RNG.uniform(1.2, 1.8), RNG.uniform(0.6, 0.85))
            x -= lado + RNG.uniform(0.7, 1.3)
    for fila, z in enumerate((-4.6, -6.6, -8.9, -11.6, -14.8, -18.5, -23.0, -28.0, -33.5)):
        lejos = fila >= 7
        x = -34.0 + (fila % 2) * 1.1
        while x < 34.0:
            lado = RNG.uniform(1.6, 2.2) * (1.0 + 0.08 * fila)
            if lejos or abs(x) > 17.5:
                dz, h, giro = RNG.uniform(-0.3, 0.3), RNG.uniform(1.3, 2.3), RNG.uniform(-0.12, 0.12)
                zc, lado2, y = _asentar(z, lado, dz)          # v3: cada casa sobre su bancal
                _casa(m, x, y - 0.05, zc, lado2, h, colores[k % 6], giro)
                k += 1
            x += 2.3 + 0.25 * fila + RNG.uniform(0, 0.5)
    for _ in range(40):
        x, z = RNG.uniform(-34, 34), RNG.uniform(-36, -4)
        if abs(x) < 17.0 and z > -24.0:
            continue
        r = RNG.uniform(0.6, 1.0)
        _copa(v, (x, _alto_ladera(z) + r * 0.9, z), r)
    return guardar("HAB-18_exterior", m, v)


def hab19():
    """Ventanas encendidas del barrio y faroles de la calle, para la noche. La zona les pone un brillo calido
    que se inclina con la escena; aqui solo importa la forma."""
    rng = np.random.default_rng(20261119)
    m = Malla("HAB-19_ventanas_noche")
    col = mezclar(C["sol"], C["crema"], 0.5)
    for c, ex, ey, n in VENTANAS:
        if rng.random() > 0.55:
            continue
        c = np.asarray(c, float) + np.asarray(n, float) * 0.006
        cara(m, [c - ex - ey, c + ex - ey, c + ex + ey, c - ex + ey], n, col)
    for c, r in LUCES:
        caja(m, c, (r * 2 + 0.01, 0.21, r * 2 + 0.01), col, sombra=0.0, luz=0.0)
    return guardar("HAB-19_ventanas_noche", m)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    total = 0
    global RNG
    for f in (tal01, tal02, tal06, tal07, tal09, tal10, tal12, tal14, tal15, tal16, tal17,
              hab01, hab02, hab03, hab04, hab05, hab06, hab07, hab08, hab09, hab10, hab11, hab12, hab13, hab14, hab15,
              hab16, hab17, hab12n, hab18, hab19):
        if f is hab13:
            # v3: HAB-13 con su propio generador; despues se repone el estado que dejaba la v2 (ver RNG_TRAS_HAB13)
            comun = RNG
            RNG = np.random.default_rng(20261313)
            try:
                total += f()
            finally:
                RNG = comun
                RNG.bit_generator.state = RNG_TRAS_HAB13
            continue
        total += f()
    print(f"TOTAL {total} triangulos en {SALIDA}")


if __name__ == "__main__":
    main()
