"""Mobiliario de la Plaza de las Iguanas (zona «ciudad»), segun las hojas HR_URB_v1 y HR_ARQ_v1.

Recursos (cada uno en juego/modelos/ciudad/<ID>.glb, origen en el centro de la base, frente hacia +Z):
  URB-01 banca              URB-02 fuente (agua con el material "Agua")     URB-03 kiosco de jugos
  URB-05 farol doble        URB-06 basurero                                 URB-07 jardinera (sin plantas)
  URB-08 estatua de iguana  URB-10 poste indicador                          URB-11 bicicletero
  URB-12 puesto de electronica (traza cian del osciloscopio en "Emisivo")
  ARQ-08 poste de luz       ARQ-09 farol                                    ARQ-10 tendedero

Escala: la protagonista mide 1,05 m; una puerta mide 1,45 m y un asiento queda a 0,32 m.
Sin letras, marcas ni logotipos: los carteles son dibujos (un vaso, tres ondas, flechas).

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/ciudad_mobiliario.py [URB-01 URB-02 ...]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, Malla, mezclar, roca  # noqa: E402
from ciudad_base import (AZUL_T, BARRO, FLOR_AMARILLA, FLOR_ROJA, FLOR_ROSA, FRENTE, HIERRO,  # noqa: E402,F401
                         HIERRO_VERDE, LECHADA, MADERA, MADERA_SOL, PERSIANA, PIEDRA, PIEDRA_TECHO, PUERTA,
                         TELA_AZUL, TELA_CREMA, TELA_SOL, TIERRA, VIDRIO, VIDRIO_LUZ, barra, caja, cilindro, cono,
                         cuerda, enredadera, extruir, guardar, mosaico, panel, planta_suelta, poligono, poli,
                         presesgar, t3, tono)

GENERADOR = "herramientas/mallas/ciudad_mobiliario.py"
CRISTAL = tono(mezclar(PAL["sol"], PAL["crema"], 0.35), mezclar(PAL["crema"], PAL["sol"], 0.25),
               mezclar(PAL["crema"], PAL["brillo"], 0.35))     # vidrio de farol, calido
AGUA, CASCADA, ESPUMA = np.array([0.35] * 3), np.array([1.0] * 3), np.array([0.75] * 3)


def banca(rng):
    """URB-01: listones de madera sobre dos costados de hierro pintado."""
    m = Malla("URB-01_banca")
    L = 0.65
    for sx in (-1, 1):
        x = sx * (L - 0.06)
        caja(m, x - 0.03, x + 0.03, 0.0, 0.32, 0.16, 0.22, HIERRO_VERDE, rng)          # pata delantera
        caja(m, x - 0.03, x + 0.03, 0.0, 0.70, -0.24, -0.18, HIERRO_VERDE, rng)        # pata trasera y respaldo
        caja(m, x - 0.035, x + 0.035, 0.46, 0.50, -0.24, 0.24, HIERRO_VERDE, rng)      # apoyabrazos
        cilindro(m, x, 0.25, 0.045, 0.045, 0.44, 0.52, 6, HIERRO_VERDE, rng)           # voluta
        caja(m, x - 0.03, x + 0.03, 0.26, 0.30, -0.2, 0.2, HIERRO_VERDE, rng)          # travesano
    for k, z in enumerate((-0.13, 0.0, 0.13)):
        tn = MADERA_SOL if k % 2 == 0 else MADERA
        caja(m, -L, L, 0.30, 0.34, z - 0.055, z + 0.055, tn, rng, techo=mezclar(tn[2], PAL["sol"], 0.25))
    for y in (0.42, 0.56):
        caja(m, -L, L, y, y + 0.10, -0.235, -0.195, MADERA_SOL, rng)
    return [("URB-01_banca", [m])]


def fuente(rng):
    """URB-02: pila redonda con banda de mosaico de ondas, dos platos y remate; agua en los tres niveles."""
    m = Malla("URB-02_fuente")
    a = Malla("URB-02_agua", "Agua")
    N = 12
    cilindro(m, 0, 0, 1.62, 1.60, 0.0, 0.07, N, PIEDRA, rng, techo=PIEDRA_TECHO)                 # grada
    cilindro(m, 0, 0, 1.45, 1.45, 0.07, 0.36, N, PIEDRA, rng, techo=None, ymin=0.0, ymax=0.45)
    cilindro(m, 0, 0, 1.50, 1.50, 0.36, 0.44, N, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.015, abanico=True)
    # banda de mosaico en cada cara de la pila
    planta = poli(0, 0, 1.455, N)
    colores = [PAL["petroleo"], AZUL_T, PAL["crema"], PAL["sol"]]
    for i in range(N):
        p0, p1 = np.array(planta[i]), np.array(planta[(i + 1) % N])
        medio = (p0 + p1) / 2
        normal = np.array([medio[0], 0.0, medio[1]])
        normal /= np.linalg.norm(normal)
        u = np.array([p1[0] - p0[0], 0.0, p1[1] - p0[1]])
        ancho = np.linalg.norm(u)
        u /= ancho
        if np.cross(u, np.array([0, 1.0, 0])) @ normal < 0:   # U a lo ancho con la normal hacia fuera
            p0, u = p1, -u
        O = np.array([p0[0], 0.11, p0[1]]) + normal * 0.004
        mosaico(m, O, u, np.array([0, 1.0, 0]), normal, ancho, 0.21, colores, rng, largo=0.085, amplitud=0.03,
                onda=ancho, fase=0.0)
    # fuste y platos
    cilindro(m, 0, 0, 0.30, 0.22, 0.30, 0.92, 8, PIEDRA, rng, techo=None, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.24, 0.86, 0.92, 1.10, 10, PIEDRA, rng, techo=None, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.86, 0.86, 1.10, 1.16, 10, PIEDRA, rng, techo=PIEDRA_TECHO, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.15, 0.12, 1.16, 1.50, 8, PIEDRA, rng, techo=None, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.12, 0.50, 1.50, 1.62, 8, PIEDRA, rng, techo=None, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.50, 0.50, 1.62, 1.67, 8, PIEDRA, rng, techo=PIEDRA_TECHO, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.08, 0.06, 1.67, 1.82, 6, PIEDRA, rng, techo=None, ymin=0.3, ymax=1.9)
    cilindro(m, 0, 0, 0.06, 0.11, 1.82, 1.88, 6, PIEDRA, rng, techo=None, ymin=0.3, ymax=1.9)
    cono(m, 0, 0, 0.11, 1.88, 2.06, 6, PIEDRA, rng)
    # agua: espejo de cada nivel y cortinas que caen
    for r, y, n in ((1.26, 0.445, N), (0.78, 1.165, 10), (0.43, 1.675, 8)):
        poligono(a, [np.array([x, y, z]) for x, z in poli(0, 0, r, n)], [AGUA] * n, (0, 1, 0))
    for r, y0, y1, n, ancho in ((0.87, 1.15, 0.45, 8, 0.24), (0.51, 1.65, 1.17, 6, 0.13)):
        for i in range(n):
            ang = 2 * math.pi * (i + 0.5) / n
            c = np.array([math.cos(ang) * r, 0.0, math.sin(ang) * r])
            t = np.array([-math.sin(ang), 0.0, math.cos(ang)]) * ancho / 2
            arr, aba = np.array([0, y0, 0]), np.array([0, y1, 0])
            poligono(a, [c - t + aba, c + t + aba, c + t * 0.8 + arr, c - t * 0.8 + arr], [CASCADA] * 4, c)
            poligono(a, [np.array([c[0] + math.cos(ang + k) * ancho * 0.7, y1 + 0.004, c[2] + math.sin(ang + k) * ancho * 0.7])
                         for k in np.linspace(0, 2 * math.pi, 6, endpoint=False)], [ESPUMA] * 6, (0, 1, 0))
    return [("URB-02_fuente", [m, a])]


def kiosco(rng):
    """URB-03: kiosco de jugos con toldo a rayas, tres botellones, cajas de fruta y un cartel dibujado."""
    m = Malla("URB-03_kiosco")
    f = Malla("URB-03_plantas", "Follaje")
    # mostrador de tablas pintadas y tablero
    for k in range(8):
        x0 = -1.0 + k * 0.25
        tn = PUERTA if k % 2 == 0 else t3(mezclar(PUERTA[1], PAL["petroleo"], 0.3), 0.25, 0.2)
        caja(m, x0, x0 + 0.245, 0.0, 0.72, 0.0, 0.55, tn, rng, techo=None)
    caja(m, -1.08, 1.08, 0.72, 0.78, -0.05, 0.62, MADERA_SOL, rng, techo=mezclar(PAL["tierra1"], PAL["sol"], 0.3))
    caja(m, -1.0, 1.0, 0.0, 1.5, -0.6, -0.52, MADERA, rng)                                  # trasera
    caja(m, -1.0, 1.0, 1.1, 1.14, -0.52, -0.25, MADERA_SOL, rng)                            # repisa
    for sx in (-1, 1):
        caja(m, sx * 1.0 - 0.04, sx * 1.0 + 0.04, 0.0, 1.80, 0.50, 0.58, MADERA_SOL, rng)
        caja(m, sx * 1.0 - 0.04, sx * 1.0 + 0.04, 0.0, 2.08, -0.62, -0.54, MADERA_SOL, rng)
    # toldo a rayas con cenefa en picos
    n = 8
    for k in range(n):
        x0, x1 = -1.2 + k * 2.4 / n, -1.2 + (k + 1) * 2.4 / n
        c = TELA_SOL if k % 2 == 0 else TELA_CREMA
        c = c * (1 + rng.normal(0, 0.03))
        poligono(m, [(x0, 1.74, 0.86), (x1, 1.74, 0.86), (x1, 2.12, -0.72), (x0, 2.12, -0.72)],
                 [c * 0.9, c * 0.9, mezclar(c, PAL["crema"], 0.15), mezclar(c, PAL["crema"], 0.15)], (0, 1, 0.3))
        poligono(m, [(x0, 1.74, 0.86), ((x0 + x1) / 2, 1.58, 0.87), (x1, 1.74, 0.86)], [c * 0.82] * 3, FRENTE)
    caja(m, -1.22, 1.22, 2.08, 2.14, -0.76, -0.68, MADERA_SOL, rng)
    # botellones y vasos
    for x, col in ((-0.62, PAL["sol"]), (-0.28, FLOR_ROSA), (0.06, mezclar(PAL["dorado"], PAL["hierba_sol"], 0.35))):
        tn = tono(col * 0.8, col, mezclar(col, PAL["crema"], 0.4))
        cilindro(m, x, 0.26, 0.125, 0.125, 0.80, 1.06, 7, tn, rng, techo=None)
        cilindro(m, x, 0.26, 0.135, 0.10, 1.06, 1.11, 7, HIERRO_VERDE, rng)
        cilindro(m, x, 0.26, 0.13, 0.13, 0.78, 0.80, 7, HIERRO_VERDE, rng, techo=None)
        caja(m, x - 0.015, x + 0.015, 0.82, 0.85, 0.38, 0.43, HIERRO, rng)
    for k in range(3):
        cilindro(m, 0.40 + k * 0.09, 0.30, 0.03, 0.04, 0.78, 0.92 - k * 0.03, 6, t3(TELA_CREMA, 0.2, 0.1), rng)
    # cartel dibujado: pizarra con un vaso de jugo y su pajita (sin letras)
    caja(m, 0.60, 1.0, 0.92, 1.46, 0.585, 0.61, MADERA_SOL, rng)
    panel(m, 0.635, 0.965, 0.955, 1.425, 0.612, VIDRIO * 0.9, VIDRIO, rng)
    vaso = [(0.735, 1.03), (0.865, 1.03), (0.895, 1.27), (0.705, 1.27)]
    extruir(m, vaso, 0.612, 0.616, t3(PAL["sol"], 0.0, 0.3), rng, cantos=False)
    extruir(m, [(0.705, 1.27), (0.895, 1.27), (0.90, 1.30), (0.70, 1.30)], 0.612, 0.617, t3(TELA_CREMA, 0, 0), rng, cantos=False)
    extruir(m, [(0.80, 1.20), (0.82, 1.20), (0.88, 1.39), (0.86, 1.39)], 0.612, 0.618, t3(FLOR_ROSA, 0, 0), rng, cantos=False)
    # cajas de fruta delante
    for cx, cz, frutas in ((-0.62, 0.88, "pina"), (-0.12, 0.92, "naranja")):
        caja(m, cx - 0.22, cx + 0.22, 0.0, 0.26, cz - 0.15, cz + 0.15, MADERA_SOL, rng, techo=TIERRA)
        for sx in (-1, 1):
            caja(m, cx + sx * 0.22 - 0.02, cx + sx * 0.22 + 0.02, 0.0, 0.29, cz - 0.16, cz + 0.16, MADERA, rng)
        if frutas == "pina":
            for dx in (-0.1, 0.1):
                tn = t3(mezclar(PAL["dorado"], PAL["sol"], 0.3), 0.15, 0.3)
                cilindro(m, cx + dx, cz, 0.075, 0.06, 0.24, 0.42, 6, tn, rng)
                planta_suelta(f, (cx + dx, 0.42, cz), rng, alto=0.16, hojas=6, abierta=0.6)
        else:
            for dx, dz in ((-0.12, -0.05), (0.0, 0.04), (0.12, -0.04), (-0.05, 0.08), (0.08, 0.09)):
                col = PAL["sol"] if rng.random() < 0.7 else PAL["dorado"]
                cilindro(m, cx + dx, cz + dz, 0.035, 0.055, 0.25, 0.30, 6, t3(col, 0.15, 0.3), rng, techo=None)
                cono(m, cx + dx, cz + dz, 0.055, 0.30, 0.345, 6, t3(col, 0.15, 0.3), rng)
    # flores y hojas sobre el toldo
    enredadera(f, [(-1.2, 2.02, -0.3), (-0.7, 1.86, 0.4), (-0.2, 1.80, 0.7)], rng, densidad=16, ancho=0.2)
    enredadera(f, [(-1.2, 1.9, 0.6), (-1.22, 1.3, 0.72)], rng, densidad=14, ancho=0.12, flores=0.15)
    planta_suelta(f, (0.5, 2.0, -0.2), rng, alto=0.4, hojas=9, flores=2)
    return [("URB-03_kiosco", [m, f])]


def _farol_cabeza(m, cx, y, rng, r=0.11):
    """Linterna: tapa de hierro, vidrio calido y pie. 'y' es el centro del vidrio."""
    cilindro(m, cx, 0, r * 0.62, r, y - 0.13, y + 0.11, 4, CRISTAL, rng, techo=None, giro=math.pi / 4)
    cilindro(m, cx, 0, r * 0.72, r * 0.55, y - 0.17, y - 0.13, 4, HIERRO, rng, techo=None, giro=math.pi / 4)
    cilindro(m, cx, 0, r * 1.25, r * 1.25, y + 0.11, y + 0.13, 4, HIERRO, rng, giro=math.pi / 4)
    cono(m, cx, 0, r * 1.2, y + 0.13, y + 0.26, 4, HIERRO, rng, giro=math.pi / 4)
    cilindro(m, cx, 0, 0.015, 0.02, y + 0.25, y + 0.31, 4, HIERRO, rng)


def farol_doble(rng):
    """URB-05: poste de hierro con dos brazos curvos y dos linternas (centros del vidrio en x = +-0,42, y = 2,06)."""
    m = Malla("URB-05_farol_doble")
    caja(m, -0.17, 0.17, 0.0, 0.13, -0.17, 0.17, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.02)
    cilindro(m, 0, 0, 0.10, 0.06, 0.13, 0.42, 8, HIERRO, rng, techo=None, ymin=0, ymax=2.6)
    cilindro(m, 0, 0, 0.075, 0.075, 0.42, 0.47, 8, HIERRO, rng, ymin=0, ymax=2.6)
    cilindro(m, 0, 0, 0.038, 0.032, 0.47, 2.50, 6, HIERRO, rng, techo=None, ymin=0, ymax=2.6)
    cilindro(m, 0, 0, 0.055, 0.055, 2.50, 2.56, 6, HIERRO, rng)
    cono(m, 0, 0, 0.04, 2.56, 2.70, 6, HIERRO, rng)
    for sx in (-1, 1):
        barra(m, [(0, 2.18, 0), (sx * 0.16, 2.40, 0), (sx * 0.32, 2.50, 0), (sx * 0.42, 2.44, 0), (sx * 0.42, 2.36, 0)],
              0.018, HIERRO, rng, lados=5)
        barra(m, [(0, 2.04, 0), (sx * 0.12, 2.12, 0), (sx * 0.18, 2.26, 0)], 0.012, HIERRO, rng, lados=4)
        _farol_cabeza(m, sx * 0.42, 2.06, rng)
    return [("URB-05_farol_doble", [m])]


def farol(rng):
    """ARQ-09: farol clasico de un solo cuerpo (centro del vidrio en y = 2,0)."""
    m = Malla("ARQ-09_farol")
    caja(m, -0.15, 0.15, 0.0, 0.10, -0.15, 0.15, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.02)
    cilindro(m, 0, 0, 0.09, 0.055, 0.10, 0.40, 8, HIERRO, rng, techo=None, ymin=0, ymax=2.2)
    cilindro(m, 0, 0, 0.065, 0.065, 0.40, 0.45, 8, HIERRO, rng, ymin=0, ymax=2.2)
    cilindro(m, 0, 0, 0.035, 0.03, 0.45, 1.80, 6, HIERRO, rng, techo=None, ymin=0, ymax=2.2)
    _farol_cabeza(m, 0.0, 2.0, rng, r=0.13)
    return [("ARQ-09_farol", [m])]


def basurero(rng):
    """URB-06: duelas de madera en un armazon de hierro pintado, con capota."""
    m = Malla("URB-06_basurero")
    n = 8
    planta = poli(0, 0, 0.21, n)
    for i in range(n):
        a, b = planta[i], planta[(i + 1) % n]
        tn = MADERA_SOL if i % 2 == 0 else MADERA
        vf = 1 + rng.normal(0, 0.04)
        fuera = np.array([(a[0] + b[0]) / 2, 0, (a[1] + b[1]) / 2])
        poligono(m, [(a[0], 0.08, a[1]), (b[0], 0.08, b[1]), (b[0], 0.62, b[1]), (a[0], 0.62, a[1])],
                 [tn[0] * vf, tn[0] * vf, tn[2] * vf, tn[2] * vf], fuera)
    cilindro(m, 0, 0, 0.225, 0.225, 0.60, 0.66, n, HIERRO_VERDE, rng, techo=VIDRIO)
    cilindro(m, 0, 0, 0.225, 0.225, 0.06, 0.10, n, HIERRO_VERDE, rng, techo=None)
    for sx in (-1, 1):
        for sz in (-1, 1):
            caja(m, sx * 0.17 - 0.02, sx * 0.17 + 0.02, 0.0, 0.08, sz * 0.17 - 0.02, sz * 0.17 + 0.02, HIERRO_VERDE, rng)
        barra(m, [(sx * 0.2, 0.64, 0), (sx * 0.2, 0.80, 0), (sx * 0.12, 0.88, 0)], 0.018, HIERRO_VERDE, rng, lados=4)
    caja(m, -0.24, 0.24, 0.86, 0.90, -0.2, 0.2, HIERRO_VERDE, rng, bisel=0.012)
    return [("URB-06_basurero", [m])]


def jardinera(rng):
    """URB-07: cajon de piedra con pilaretes y panel de mosaico; la tierra queda lista para las plantas
    (VEG-07, VEG-10 y VEG-14 se colocan encima desde la zona)."""
    m = Malla("URB-07_jardinera")
    caja(m, -0.78, 0.78, 0.0, 0.40, -0.43, 0.43, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.015, ymax=0.5)
    for sx in (-1, 1):
        for sz in (-1, 1):
            caja(m, sx * 0.72 - 0.11, sx * 0.72 + 0.11, 0.0, 0.48, sz * 0.38 - 0.10, sz * 0.38 + 0.10, PIEDRA, rng,
                 techo=PIEDRA_TECHO, bisel=0.02, ymax=0.5)
    poligono(m, [(-0.60, 0.404, 0.30), (0.60, 0.404, 0.30), (0.60, 0.404, -0.30), (-0.60, 0.404, -0.30)],
             [TIERRA * 0.9, TIERRA, TIERRA * 1.05, TIERRA], (0, 1, 0))
    colores = [PAL["petroleo"], AZUL_T, PAL["crema"], PAL["sol"]]
    mosaico(m, (-0.60, 0.09, 0.434), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.20, 0.24, colores, rng, largo=0.08,
            amplitud=0.035, onda=0.6)
    return [("URB-07_jardinera", [m])]


def estatua_iguana(rng):
    """URB-08: iguana de bronce verdoso sobre una roca ocre, en un pedestal de piedra caliza calida con una placa
    de tres ondas (sin letras). v2.1: nada de gris; la caliza va de crema arriba a ocre abajo."""
    m = Malla("URB-08_estatua_iguana")
    caliza = tono(mezclar(mezclar(PAL["tierra1"], PAL["sol"], 0.35), PAL["terracota"], 0.18),
                   mezclar(PAL["crema"], PAL["sol"], 0.28), mezclar(PAL["crema"], PAL["brillo"], 0.25))
    caliza_techo = mezclar(PAL["crema"], PAL["brillo"], 0.18)
    caja(m, -0.62, 0.62, 0.0, 0.11, -0.44, 0.44, caliza, rng, techo=caliza_techo, bisel=0.015, ymin=0.0, ymax=0.9)
    caja(m, -0.50, 0.50, 0.11, 0.58, -0.34, 0.34, caliza, rng, techo=None, ymin=0.0, ymax=0.9)
    caja(m, -0.56, 0.56, 0.58, 0.66, -0.39, 0.39, caliza, rng, techo=caliza_techo, bisel=0.02, ymin=0.0, ymax=0.75)
    # placa: marco dorado, fondo verde azulado y tres ondas
    oro = t3(mezclar(PAL["dorado"], PAL["crema"], 0.2), 0.2, 0.3)
    extruir(m, [(-0.27, 0.22), (0.27, 0.22), (0.27, 0.48), (-0.27, 0.48)], 0.34, 0.352, oro, rng)
    panel(m, -0.24, 0.24, 0.25, 0.45, 0.354, PERSIANA[0], PERSIANA[1], rng)
    for k in range(3):
        y = 0.295 + k * 0.05
        xs = np.linspace(-0.18, 0.18, 7)
        for i in range(6):
            ya, yb = y + (0.014 if i % 2 else -0.014), y + (-0.014 if i % 2 else 0.014)
            poligono(m, [(xs[i], ya - 0.009, 0.356), (xs[i + 1], yb - 0.009, 0.356), (xs[i + 1], yb + 0.009, 0.356),
                         (xs[i], ya + 0.009, 0.356)], [oro[2]] * 4, FRENTE)
    # roca ocre (arenisca de la loma, no gris)
    from nucleo import fibonacci, solido_facetado
    rr = np.random.default_rng(11)
    pts = fibonacci(16) * rr.uniform(0.72, 1.15, (16, 1)) * np.array((1.0, 0.42, 0.66)) * 0.5
    piso = pts[:, 1].min() * 0.5
    pts[pts[:, 1] < piso, 1] = piso
    pts[:, 1] -= pts[:, 1].min()
    r = solido_facetado("roca", pts, mezclar(PAL["tierra2"], PAL["terracota"], 0.35), mezclar(PAL["tierra1"], PAL["sol"], 0.25),
                        mezclar(PAL["crema"], PAL["sol"], 0.3), rr)
    m.anexar(r, t=(-0.02, 0.66, 0.0))
    # iguana de bronce: verde oliva en la panza, cardenillo en los costados y luces doradas en el lomo
    bajo = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.30)
    alto = mezclar(mezclar(PAL["cian_medio"], PAL["hierba_sol"], 0.55), PAL["crema"], 0.18)
    oro_lomo = mezclar(PAL["dorado"], PAL["crema"], 0.25)
    espina = [(-0.66, 0.74, 0.16), (-0.52, 0.80, 0.10), (-0.34, 0.90, 0.03), (-0.16, 1.02, 0.0), (0.04, 1.12, 0.0),
              (0.22, 1.20, 0.0), (0.36, 1.30, 0.0), (0.47, 1.34, 0.0), (0.58, 1.32, 0.0)]
    radios = [0.012, 0.03, 0.055, 0.095, 0.115, 0.095, 0.075, 0.07, 0.03]
    from nucleo import tubo
    tubo(m, espina, radios, 6, bajo, alto, rng, ruido=0.06)
    for x, y, z, px, pz in ((0.20, 1.14, 0.08, 0.34, 0.22), (0.20, 1.14, -0.08, 0.34, -0.22),
                            (-0.14, 0.98, 0.08, -0.06, 0.24), (-0.14, 0.98, -0.08, -0.06, -0.24)):
        tubo(m, [(x, y, z), ((x + px) / 2, y + 0.02, pz * 0.9), (px, y - 0.2, pz)], [0.04, 0.032, 0.026], 5, bajo,
             mezclar(bajo, alto, 0.6), rng, ruido=0.05)
    # cresta: puas triangulares a doble cara
    for i in range(3, 7):
        a, b = np.array(espina[i]), np.array(espina[i + 1])
        for t in (0.15, 0.6):
            p = a + (b - a) * t
            q = a + (b - a) * (t + 0.3)
            top = (p + q) / 2 + np.array([-0.02, radios[i] + 0.07, 0.0])
            p, q = p + np.array([0, radios[i] * 0.8, 0]), q + np.array([0, radios[i] * 0.8, 0])
            m.tri(p, q, top, alto * 0.95, alto * 0.95, oro_lomo)
            m.tri(q, p, top, alto * 0.85, alto * 0.85, oro_lomo * 0.95)
    # papada
    g0, g1 = np.array([0.36, 1.25, 0.0]), np.array([0.50, 1.28, 0.0])
    gb = np.array([0.42, 1.14, 0.0])
    for s in (1, -1):
        d = np.array([0, 0, 0.035 * s])
        poligono(m, [g0 + d, g1 + d, gb], [bajo, bajo, mezclar(bajo, alto, 0.4)], d)
    return [("URB-08_estatua_iguana", [m])]


def poste_indicador(rng):
    """URB-10: poste de madera con tres tablas en flecha (sin letras) sobre una base de piedra."""
    m = Malla("URB-10_poste_indicador")
    f = Malla("URB-10_plantas", "Follaje")
    r = roca("base", semilla=5, escala=(0.5, 0.34, 0.46), npts=14, musgo=False)
    m.anexar(r)
    caja(m, -0.05, 0.05, 0.12, 1.72, -0.05, 0.05, MADERA, rng, ymin=0.1, ymax=1.8)
    cono(m, 0, 0, 0.085, 1.72, 1.86, 4, PERSIANA, rng, giro=math.pi / 4)
    tablas = [(1.40, 1.0, 0.62), (1.13, -1.0, 0.58), (0.86, 1.0, 0.52)]
    for y, s, largo in tablas:
        x0, x1 = -0.16 * s, largo * s
        pts = [(x0, y), (x1 - 0.13 * s, y), (x1, y + 0.09), (x1 - 0.13 * s, y + 0.18), (x0, y + 0.18)]
        if s < 0:
            pts = pts[::-1]
        tn = MADERA_SOL
        extruir(m, pts, 0.05, 0.085, tn, rng, ymin=y - 0.1, ymax=y + 0.22)
        for xx in (0.0, x1 - 0.2 * s):
            panel(m, xx - 0.012, xx + 0.012, y + 0.08, y + 0.105, 0.087, PAL["oscuro"] * 1.4, None, rng)
    planta_suelta(f, (-0.22, 0.0, 0.12), rng, alto=0.26, hojas=7)
    planta_suelta(f, (0.24, 0.0, 0.08), rng, alto=0.22, hojas=6)
    return [("URB-10_poste_indicador", [m, f])]


def bicicletero(rng):
    """URB-11: tres aros de hierro pintado sobre losas y una bicicleta apoyada (sin marca)."""
    m = Malla("URB-11_bicicletero")
    for x in (-0.62, 0.0, 0.62):
        caja(m, x - 0.12, x + 0.12, 0.0, 0.05, -0.42, 0.42, PIEDRA, rng, techo=PIEDRA_TECHO)
        barra(m, [(x, 0.05, -0.32), (x, 0.50, -0.32), (x, 0.66, -0.20), (x, 0.70, 0.0), (x, 0.66, 0.20), (x, 0.50, 0.32),
                  (x, 0.05, 0.32)], 0.025, HIERRO_VERDE, rng, lados=5, tapa=False)
    # bicicleta de lado, delante de los aros
    z = 0.50
    cuadro = t3(mezclar(PAL["sol"], PAL["dorado"], 0.4), 0.2, 0.25)
    goma = tono(PAL["oscuro"] * 1.3, PAL["piedra_osc"], mezclar(PAL["piedra_osc"], PAL["piedra"], 0.5))
    for cx in (-0.40, 0.44):
        aro = [(cx + 0.25 * math.cos(a), 0.25 + 0.25 * math.sin(a), z) for a in np.linspace(0, 2 * math.pi, 11)]
        barra(m, aro, 0.022, goma, rng, lados=4, tapa=False)
        for a in (0.3, 1.35, 2.4):
            barra(m, [(cx + 0.24 * math.cos(a), 0.25 + 0.24 * math.sin(a), z), (cx - 0.24 * math.cos(a), 0.25 - 0.24 * math.sin(a), z)],
                  0.006, HIERRO, rng, lados=3, tapa=False)
    sillin, pedal, pipa = (-0.16, 0.60, z), (-0.06, 0.24, z), (0.30, 0.62, z)
    for a, b in ((( -0.40, 0.25, z), sillin), (sillin, pedal), (pedal, (-0.40, 0.25, z)), (pedal, pipa), (sillin, pipa),
                 (pipa, (0.44, 0.25, z))):
        barra(m, [a, b], 0.018, cuadro, rng, lados=4)
    barra(m, [pipa, (0.27, 0.76, z)], 0.014, HIERRO, rng, lados=4)
    barra(m, [(0.27, 0.76, z - 0.17), (0.27, 0.76, z + 0.17)], 0.014, HIERRO, rng, lados=4)
    caja(m, -0.26, -0.08, 0.62, 0.66, z - 0.05, z + 0.05, MADERA, rng)
    caja(m, 0.33, 0.55, 0.56, 0.72, z - 0.13, z + 0.13, t3(mezclar(PAL["crema"], PAL["tierra1"], 0.35), 0.25, 0.2), rng,
         techo=TIERRA)
    return [("URB-11_bicicletero", [m])]


def puesto_electronica(rng):
    """URB-12: puesto de reparaciones con lona azul, osciloscopio (traza cian), cajonera, placa y cajas."""
    m = Malla("URB-12_puesto")
    f = Malla("URB-12_plantas", "Follaje")
    e = Malla("URB-12_traza", "Emisivo")
    for sx in (-1, 1):
        caja(m, sx * 0.95 - 0.04, sx * 0.95 + 0.04, 0.0, 1.74, 0.46, 0.54, MADERA_SOL, rng)
        caja(m, sx * 0.95 - 0.04, sx * 0.95 + 0.04, 0.0, 1.96, -0.54, -0.46, MADERA_SOL, rng)
    caja(m, -1.0, 1.0, 1.90, 1.96, -0.56, -0.48, MADERA, rng)
    barra(m, [(-1.05, 1.74, 0.5), (1.05, 1.74, 0.5)], 0.035, MADERA_SOL, rng, lados=5)
    # lona azul con panza: tres pasos de fondo a frente y cuatro panos
    xs = np.linspace(-1.14, 1.14, 5)
    zs = [(-0.66, 2.02), (0.0, 1.84), (0.72, 1.74)]
    for i in range(4):
        for k in range(2):
            (z0, y0), (z1, y1) = zs[k + 1], zs[k]
            c = TELA_AZUL * (1 + rng.normal(0, 0.06))
            hund = 0.03 if i in (1, 2) else 0.0
            poligono(m, [(xs[i], y0, z0), (xs[i + 1], y0, z0), (xs[i + 1], y1 - hund, z1), (xs[i], y1 - hund, z1)],
                     [c * 0.86, c * 0.86, mezclar(c, PAL["piedra_clara"], 0.25), mezclar(c, PAL["piedra_clara"], 0.25)],
                     (0, 1, 0.2))
        c = TELA_AZUL * 0.8
        poligono(m, [(xs[i], 1.74, 0.72), ((xs[i] + xs[i + 1]) / 2, 1.60, 0.73), (xs[i + 1], 1.74, 0.72)], [c] * 3, FRENTE)
    # mesa y repisa
    caja(m, -1.0, 1.0, 0.66, 0.72, -0.46, 0.52, MADERA_SOL, rng, techo=mezclar(PAL["tierra1"], PAL["sol"], 0.25))
    caja(m, -0.95, 0.95, 1.16, 1.20, -0.50, -0.20, MADERA_SOL, rng)
    for x, col in ((-0.7, PAL["sol"]), (-0.48, PAL["dorado"]), (0.62, TELA_AZUL), (0.8, PAL["coral"])):
        cilindro(m, x, -0.34, 0.07, 0.07, 1.20, 1.32, 7, t3(col, 0.2, 0.3), rng)
    caja(m, -0.2, 0.3, 1.20, 1.34, -0.46, -0.26, t3(mezclar(PAL["tierra1"], PAL["crema"], 0.3)), rng)
    # osciloscopio: caja crema, pantalla oscura y traza cian (tecnologia)
    crema = t3(mezclar(PAL["crema"], PAL["piedra_clara"], 0.35), 0.3, 0.15)
    caja(m, 0.12, 0.56, 0.72, 0.98, -0.12, 0.20, crema, rng, bisel=0.012)
    panel(m, 0.16, 0.38, 0.77, 0.94, 0.202, VIDRIO * 0.8, VIDRIO, rng)
    for k in range(3):
        panel(m, 0.42 + (k % 2) * 0.06, 0.46 + (k % 2) * 0.06, 0.79 + (k // 2) * 0.08 + (k % 2) * 0.02,
              0.83 + (k // 2) * 0.08 + (k % 2) * 0.02, 0.203, PAL["piedra_osc"], PAL["piedra"], rng)
    xs2 = np.linspace(0.175, 0.365, 8)
    ys2 = [0.855, 0.90, 0.81, 0.90, 0.81, 0.90, 0.81, 0.855]
    for i in range(7):
        a, b = np.array([xs2[i], ys2[i], 0.206]), np.array([xs2[i + 1], ys2[i + 1], 0.206])
        g = np.array([0, 0.008, 0])
        poligono(e, [a - g, b - g, b + g, a + g], [PAL["cian"]] * 4, FRENTE)
    # cajonera de piezas
    gris = t3(mezclar(PAL["piedra"], PAL["piedra_clara"], 0.4), 0.3, 0.2)
    caja(m, -0.62, -0.20, 0.72, 0.92, -0.10, 0.16, gris, rng)
    for i in range(4):
        for k in range(2):
            panel(m, -0.60 + i * 0.10, -0.52 + i * 0.10, 0.745 + k * 0.085, 0.81 + k * 0.085, 0.162,
                  PAL["piedra_osc"] * 1.1, PAL["piedra"], rng)
    # placa de circuito, carrete de cable y cautin en su soporte
    placa = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.45)
    caja(m, -0.12, 0.10, 0.72, 0.735, 0.26, 0.44, t3(placa, 0.2, 0.2), rng, techo=mezclar(placa, PAL["hierba_sol"], 0.25))
    for dx, dz in ((-0.07, 0.31), (0.0, 0.36), (0.05, 0.30), (-0.03, 0.40)):
        caja(m, dx - 0.012, dx + 0.012, 0.735, 0.745, dz - 0.012, dz + 0.012, t3(PAL["dorado"], 0.1, 0.3), rng)
    cilindro(m, 0.70, 0.30, 0.07, 0.07, 0.72, 0.76, 8, t3(PAL["sol"], 0.2, 0.3), rng, techo=PAL["terracota"])
    barra(m, [(0.62, 0.74, 0.02), (0.84, 0.86, -0.04)], 0.014, HIERRO, rng, lados=4)
    barra(m, [(0.84, 0.86, -0.04), (0.90, 0.89, -0.055)], 0.022, t3(PAL["coral"], 0.2, 0.2), rng, lados=5)
    caja(m, 0.58, 0.66, 0.72, 0.76, -0.02, 0.06, HIERRO, rng)
    # cartelito apoyado en la mesa: dos rayas, sin letras (el texto lo pone el dialogo)
    panel(m, -0.92, -0.70, 0.725, 0.86, 0.50, TELA_CREMA * 0.92, TELA_CREMA, rng)
    for y in (0.78, 0.82):
        panel(m, -0.89, -0.73, y, y + 0.012, 0.502, PAL["madera2"], None, rng)
    # caja de herramientas azul y cajon de madera bajo la mesa
    azul = t3(TELA_AZUL, 0.3, 0.25)
    caja(m, -0.66, -0.12, 0.0, 0.24, 0.10, 0.42, azul, rng, bisel=0.015)
    caja(m, -0.44, -0.34, 0.24, 0.28, 0.20, 0.32, HIERRO, rng)
    caja(m, 0.12, 0.58, 0.0, 0.26, 0.08, 0.40, MADERA_SOL, rng, techo=mezclar(PAL["tierra2"], PAL["tierra1"], 0.4))
    # cables colgados y hiedra en el poste derecho
    for k in range(2):
        aro = [(-0.95 + 0.07, 1.42 - k * 0.24 + 0.10 * math.sin(a), 0.56 + 0.02 + 0.0 * a) for a in np.linspace(0, 2 * math.pi, 9)]
        aro = [(x + 0.10 * math.cos(a), y, zz) for (x, y, zz), a in zip(aro, np.linspace(0, 2 * math.pi, 9))]
        barra(m, aro, 0.012, HIERRO, rng, lados=4, tapa=False)
    enredadera(f, [(0.98, 1.85, 0.5), (1.0, 1.2, 0.56), (0.97, 0.75, 0.56)], rng, densidad=16, ancho=0.10, flores=0.0)
    presesgar(e)
    return [("URB-12_puesto_electronica", [m, f, e])]


def tendedero(rng):
    """ARQ-10: dos postes, una cuerda con panza y cuatro prendas (material Follaje: doble cara y viento)."""
    m = Malla("ARQ-10_tendedero")
    f = Malla("ARQ-10_ropa", "Follaje")
    for sx in (-1, 1):
        barra(m, [(sx * 1.4, 0.0, 0), (sx * 1.4, 1.78, 0)], 0.045, MADERA, rng, lados=6)
        m.anexar(roca("p", semilla=20 + sx, escala=(0.26, 0.14, 0.24), npts=12, musgo=False), t=(sx * 1.4 + 0.12, 0, 0.1))

    def y_cuerda(x):
        return 1.50 + 0.20 * (x / 1.4) ** 2

    cuerda(m, [(x, y_cuerda(x), 0.0) for x in np.linspace(-1.4, 1.4, 9)], 0.014, rng, lados=4, vuelta=0.3)
    n = np.array([0.0, 0.25, 0.97])

    def pano(x0, x1, alto, franjas):
        """Rectangulo colgado de la cuerda, partido en franjas horizontales [(fraccion, color)...]."""
        y0a, y0b = y_cuerda(x0), y_cuerda(x1)
        t = 0.0
        for frac, col in franjas:
            t1 = t + frac
            a, b = y0a - alto * t, y0b - alto * t
            c, d = y0b - alto * t1, y0a - alto * t1
            col = np.asarray(col, float) * (1 + rng.normal(0, 0.03))
            f.tri((x0, a, 0.0), (x1, c, 0.01), (x1, b, 0.0), col, col * 0.9, col, [n, n, n])
            f.tri((x0, a, 0.0), (x0, d, 0.01), (x1, c, 0.01), col, col * 0.9, col * 0.9, [n, n, n])
            t = t1

    azul = mezclar(TELA_AZUL, PAL["piedra_clara"], 0.25)
    pano(-1.12, -0.72, 0.62, [(0.5, TELA_CREMA), (0.08, azul), (0.08, TELA_CREMA), (0.08, azul), (0.26, TELA_CREMA)])
    coral = mezclar(PAL["coral"], PAL["sol"], 0.25)
    pano(-0.50, -0.06, 0.42, [(1.0, coral)])
    pano(-0.62, -0.50, 0.16, [(1.0, coral * 0.92)])
    pano(-0.06, 0.06, 0.16, [(1.0, coral * 0.92)])
    pano(0.22, 0.40, 0.36, [(1.0, TELA_AZUL)])
    pano(0.40, 0.58, 0.36, [(1.0, TELA_AZUL * 0.9)])
    pano(0.80, 1.14, 0.56, [(0.2, TELA_CREMA), (0.1, coral), (0.1, TELA_CREMA), (0.1, coral), (0.1, TELA_CREMA),
                            (0.1, coral), (0.3, TELA_CREMA)])
    return [("ARQ-10_tendedero", [m, f])]


def poste_luz(rng):
    """ARQ-08: poste de madera con cruceta, aisladores y transformador (sin cables: se leen como telaranas
    desde la camara alta)."""
    m = Malla("ARQ-08_poste_luz")
    barra(m, [(0, 0, 0), (0, 3.7, 0)], [0.085, 0.06], MADERA, rng, lados=6)
    caja(m, -0.62, 0.62, 3.30, 3.40, -0.05, 0.05, MADERA_SOL, rng)
    barra(m, [(-0.3, 3.3, 0.0), (0.0, 3.0, 0.03)], 0.02, MADERA, rng, lados=4)
    barra(m, [(0.3, 3.3, 0.0), (0.0, 3.0, 0.03)], 0.02, MADERA, rng, lados=4)
    for x in (-0.52, -0.2, 0.2, 0.52):
        cilindro(m, x, 0, 0.035, 0.025, 3.40, 3.50, 6, t3(mezclar(PAL["crema"], PAL["piedra_clara"], 0.4), 0.3, 0.1), rng)
    gris = t3(mezclar(PAL["piedra_clara"], PAL["crema"], 0.3), 0.35, 0.1)
    cilindro(m, 0, 0.2, 0.15, 0.15, 2.40, 2.84, 8, gris, rng)
    caja(m, -0.06, 0.06, 2.84, 2.92, 0.14, 0.26, HIERRO, rng)
    caja(m, -0.09, 0.09, 1.20, 1.46, 0.07, 0.15, gris, rng)
    return [("ARQ-08_poste_luz", [m])]


RECURSOS = {
    "URB-01": (banca, 101), "URB-02": (fuente, 102), "URB-03": (kiosco, 103), "URB-05": (farol_doble, 105),
    "URB-06": (basurero, 106), "URB-07": (jardinera, 107), "URB-08": (estatua_iguana, 108),
    "URB-10": (poste_indicador, 110), "URB-11": (bicicletero, 111), "URB-12": (puesto_electronica, 112),
    "ARQ-08": (poste_luz, 208), "ARQ-09": (farol, 209), "ARQ-10": (tendedero, 210),
}


def main():
    pedidos = sys.argv[1:] or list(RECURSOS)
    total = 0
    for rid in pedidos:
        fabrica, semilla = RECURSOS[rid]
        total += guardar(rid, fabrica(np.random.default_rng(semilla)), GENERADOR)
    print(f"TOTAL {total} triangulos en {len(pedidos)} recursos")


if __name__ == "__main__":
    main()
