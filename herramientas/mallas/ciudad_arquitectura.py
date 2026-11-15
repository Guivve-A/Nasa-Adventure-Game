"""Arquitectura y suelo de la Plaza de las Iguanas (zona «ciudad»), segun la hoja HR_ARQ_v1.

Recursos (juego/modelos/ciudad/<archivo>.glb; el frente mira a +Z y la fachada queda en z = 0):
  ARQ-01        casa amarilla de dos pisos con balcon de madera (ARQ-06), tejas y buganvilla
  ARQ-01_rosa   la misma casa en rosa, sin buganvilla (relleno de calle)
  ARQ-02        casa azul de un piso, con ventana de reja (ARQ-04) y puerta de madera (ARQ-05)
  ARQ-02_coral, ARQ-02_crema, ARQ-02_verde   variantes de color para las calles del fondo
  ARQ-02_zinc   casa crema con techo de chapas de zinc (ARQ-03)
  ARQ-13        Biblioteca municipal (ID NUEVO): fachada original de aire republicano guayaquileno, con
                gradas, portico de cuatro columnas, fronton con un libro abierto en relieve (sin letras) y
                la puerta entreabierta por la que sale una rendija de luz cian ("Emisivo", ya inclinada)
  TER-14        suelo de la plaza (ID NUEVO): adoquin calido con cenefas, rosa de mosaico alrededor de la
                fuente y losas claras en las salidas. Va en coordenadas de la plaza (fuente en el origen)
                y partido en 6 nodos, porque el renderizador Mobile admite 8 luces por malla.

Escala «chibi» de la protagonista (1,05 m): un piso mide 2,3 m y una puerta 1,45 m.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/ciudad_arquitectura.py [ARQ-01 ARQ-02 ARQ-13 TER-14 ...]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, Malla, mezclar  # noqa: E402
from ciudad_base import (AMARILLO, AZUL, AZUL_T, BARRO, CORAL, CREMA, FLOR_AMARILLA, FLOR_ROJA, FLOR_ROSA, FRENTE,  # noqa: E402,F401
                         HIERRO, LECHADA, MADERA, MADERA_SOL, MARFIL, MOLDURA, PERSIANA, PIEDRA, PIEDRA_TECHO,
                         PUERTA, ROSA, TELA_CREMA, TIERRA, VERDE, VIDRIO, VIDRIO_LUZ, barra, caja, chapas, cilindro,
                         cono, enredadera, extruir, guardar, panel, planta_suelta, poligono, poli, presesgar, t3,
                         tejado, tono)

GENERADOR = "herramientas/mallas/ciudad_arquitectura.py"
PISO = 2.3

# ---------- v2 «color y vida»: fachadas vivas del barrio y detalles en contraste ----------
# (solo mezclas de la paleta maestra; el turquesa de la pintura es cian_medio con petroleo, como el mosaico)
AMARILLO_V = t3(mezclar(mezclar(PAL["dorado"], PAL["sol"], 0.30), PAL["crema"], 0.14), 0.28, 0.32)
TURQUESA_V = t3(mezclar(mezclar(PAL["petroleo"], PAL["cian_medio"], 0.55), PAL["piedra_clara"], 0.16), 0.24, 0.30)
CORAL_V = t3(mezclar(PAL["coral"], PAL["sol"], 0.25), 0.26, 0.28)
ANIL_V = t3(mezclar(mezclar(PAL["petroleo"], PAL["cian_medio"], 0.22), PAL["piedra_clara"], 0.24), 0.24, 0.30)
MENTA_V = t3(mezclar(mezclar(PAL["cian_medio"], PAL["hierba_sol"], 0.45), PAL["crema"], 0.36), 0.24, 0.30)
ROSA_V = t3(mezclar(PAL["coral"], PAL["piedra_clara"], 0.34), 0.25, 0.28)
CAL_V = t3(mezclar(PAL["crema"], PAL["brillo"], 0.30), 0.22, 0.12)
# detalles: marcos de cal, postigos y zocalos pintados en contraste
MARCO_CAL = t3(mezclar(PAL["crema"], PAL["brillo"], 0.45), 0.20, 0.05)
POSTIGO = {
    "turquesa": t3(mezclar(PAL["cian_medio"], PAL["petroleo"], 0.40), 0.25, 0.25),
    "coral": t3(mezclar(PAL["coral"], PAL["terracota"], 0.20), 0.25, 0.25),
    "amarillo": t3(mezclar(PAL["dorado"], PAL["sol"], 0.25), 0.25, 0.25),
    "verde": t3(mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.30), 0.25, 0.30),
    "anil": t3(PAL["petroleo"], 0.25, 0.25),
}
TOLDO = {"coral": mezclar(PAL["coral"], PAL["sol"], 0.15), "turquesa": mezclar(PAL["cian_medio"], PAL["petroleo"], 0.30),
         "amarillo": mezclar(PAL["dorado"], PAL["sol"], 0.35), "verde": mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.25)}
BUGANVILLA = mezclar(PAL["coral"], PAL["piedra_clara"], 0.30)


def toldo(m, f, cx, w, y, col, rng, prof=0.62, caida=0.34):
    """Toldo a rayas sobre una puerta o ventana: lona inclinada (col y crema), cenefa en picos que se mueve con
    el viento (follaje) y dos tirantes de hierro."""
    n = max(3, int(round(w / 0.17)))
    for k in range(n):
        x0, x1 = cx - w / 2 + w * k / n, cx - w / 2 + w * (k + 1) / n
        c = (np.asarray(col, float) if k % 2 == 0 else TELA_CREMA) * (1 + rng.normal(0, 0.03))
        poligono(m, [(x0, y - caida, prof), (x1, y - caida, prof), (x1, y, 0.02), (x0, y, 0.02)],
                 [c * 0.88, c * 0.88, mezclar(c, PAL["crema"], 0.12), mezclar(c, PAL["crema"], 0.12)], (0, 1, 0.5))
        poligono(f, [(x0, y - caida, prof + 0.004), ((x0 + x1) / 2, y - caida - 0.13, prof + 0.01), (x1, y - caida, prof + 0.004)],
                 [c * 0.82] * 3, FRENTE)
    for s in (-1, 1):
        barra(m, [(cx + s * (w / 2 - 0.05), y - 0.55, 0.02), (cx + s * (w / 2 - 0.05), y - caida - 0.01, prof - 0.03)], 0.012, HIERRO, rng, lados=4)


def R(x0, x1, y0, y1):
    """Rectangulo de fachada como poligono (x, y)."""
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# ---------- piezas de fachada (todas miran a +Z sobre el plano z) ----------

def ventana(m, cx, y0, w, h, z, rng, reja=False, persianas=False, f=None, arco=False, marco=None, postigo=None,
            flor=None):
    """ARQ-04: marco de piedra (o de cal pintada), vidrio oscuro con reflejo, cruz de madera y, si se pide, reja
    o persianas (postigos del color que se pida)."""
    PIEDRA_M = PIEDRA if marco is None else marco
    PERSIANA_P = PERSIANA if postigo is None else postigo
    x0, x1, y1 = cx - w / 2, cx + w / 2, y0 + h
    g = 0.08
    extruir(m, R(x0 - g, x0, y0, y1), z, z + 0.05, PIEDRA_M, rng, ymin=y0, ymax=y1 + 0.3)
    extruir(m, R(x1, x1 + g, y0, y1), z, z + 0.05, PIEDRA_M, rng, ymin=y0, ymax=y1 + 0.3)
    extruir(m, R(x0 - g - 0.03, x1 + g + 0.03, y1, y1 + 0.11), z, z + 0.06, PIEDRA_M, rng, ymin=y0, ymax=y1 + 0.3)
    extruir(m, R(x0 - g - 0.05, x1 + g + 0.05, y0 - 0.09, y0), z, z + 0.09, PIEDRA_M, rng, ymin=y0 - 0.2, ymax=y0 + 0.05)
    if arco:
        n = 5
        pts = [(cx + (w / 2 + g) * math.cos(a), y1 + 0.11 + (w / 2 + g) * 0.55 * math.sin(a)) for a in np.linspace(0, math.pi, n + 2)]
        extruir(m, pts, z, z + 0.05, PIEDRA, rng, ymin=y0, ymax=y1 + 0.6)
        pts = [(cx + (w / 2 - 0.02) * math.cos(a), y1 + 0.11 + (w / 2 - 0.02) * 0.5 * math.sin(a)) for a in np.linspace(0, math.pi, n + 2)]
        extruir(m, pts, z, z + 0.056, t3(VIDRIO_LUZ, 0.3, 0.1), rng, cantos=False)
    panel(m, x0, x1, y0, y1, z + 0.012, VIDRIO, VIDRIO_LUZ, rng)
    poligono(m, [(x0 + w * 0.12, y0 + h * 0.55, z + 0.014), (x0 + w * 0.42, y0 + h * 0.92, z + 0.014), (x0 + w * 0.12, y0 + h * 0.92, z + 0.014)],
             [mezclar(VIDRIO_LUZ, PAL["brillo"], 0.35)] * 3, FRENTE)
    cruz = PERSIANA_P[1] * (1 + rng.normal(0, 0.03))
    panel(m, cx - 0.025, cx + 0.025, y0, y1, z + 0.02, cruz * 0.85, cruz, rng)
    panel(m, x0, x1, y0 + h * 0.5 - 0.022, y0 + h * 0.5 + 0.022, z + 0.021, cruz, cruz, rng)
    if reja:
        n = max(3, int(round(w / 0.16)))
        for i in range(n):
            x = x0 + w * (i + 0.5) / n
            panel(m, x - 0.012, x + 0.012, y0 + 0.02, y1 - 0.02, z + 0.07, HIERRO[0], HIERRO[1], rng)
        for yy in (y0 + h * 0.2, y0 + h * 0.8):
            panel(m, x0, x1, yy - 0.012, yy + 0.012, z + 0.072, HIERRO[1], HIERRO[1], rng)
        yy = y0 + h * 0.5
        poligono(m, [(cx - 0.07, yy, z + 0.074), (cx, yy - 0.09, z + 0.074), (cx + 0.07, yy, z + 0.074), (cx, yy + 0.09, z + 0.074)],
                 [HIERRO[1]] * 4, FRENTE)
    if persianas:
        for s in (-1, 1):
            a = x0 - g - 0.02 if s < 0 else x1 + g + 0.02
            b = a + s * w * 0.46
            extruir(m, R(min(a, b), max(a, b), y0, y1), z, z + 0.035, PERSIANA_P, rng)
            for k in range(4):
                yy = y0 + h * (k + 0.5) / 4
                panel(m, min(a, b) + 0.03, max(a, b) - 0.03, yy - 0.012, yy + 0.012, z + 0.037, PERSIANA_P[0] * 0.9, None, rng)
    if f is not None:
        caja(m, x0 - 0.04, x1 + 0.04, y0 - 0.26, y0 - 0.09, z + 0.02, z + 0.2, BARRO, rng, techo=TIERRA)
        col_flor = flor if flor is not None else (FLOR_ROSA if rng.random() < 0.6 else FLOR_ROJA)
        enredadera(f, [(x0, y0 - 0.02, z + 0.12), (x1, y0 - 0.02, z + 0.12)], rng, densidad=18, ancho=0.07,
                   col_flor=col_flor, flores=0.6)


def puerta(m, cx, y0, w, h, z, rng, tn=PUERTA, grada=True, abierta=0.0, marco=None):
    """ARQ-05: marco de piedra y dos hojas de madera con cuarterones y aldabas. 'abierta' deja una rendija
    central de ese ancho (m) y devuelve su rectangulo (x0, x1, y0, y1) para la luz."""
    x0, x1, y1 = cx - w / 2, cx + w / 2, y0 + h
    g = 0.11
    MP = PIEDRA if marco is None else marco
    extruir(m, R(x0 - g, x0, y0, y1), z, z + 0.07, MP, rng, ymin=y0, ymax=y1 + 0.3)
    extruir(m, R(x1, x1 + g, y0, y1), z, z + 0.07, MP, rng, ymin=y0, ymax=y1 + 0.3)
    extruir(m, R(x0 - g - 0.04, x1 + g + 0.04, y1, y1 + 0.15), z, z + 0.085, MP, rng, ymin=y0, ymax=y1 + 0.3)
    extruir(m, R(cx - 0.09, cx + 0.09, y1, y1 + 0.19), z, z + 0.10, MP, rng, ymin=y0, ymax=y1 + 0.2)   # clave
    panel(m, x0, x1, y0, y1, z + 0.008, VIDRIO * 0.75, VIDRIO * 0.9, rng)
    for s in (-1, 1):
        a = cx + s * abierta / 2
        b = cx + s * w / 2
        lo, hi = min(a, b), max(a, b)
        extruir(m, R(lo, hi, y0, y1), z, z + 0.03, tn, rng, ymin=y0, ymax=y1)
        ancho = hi - lo
        for k, (ya, yb) in enumerate(((0.08, 0.42), (0.50, 0.92))):
            panel(m, lo + ancho * 0.16, hi - ancho * 0.16, y0 + h * ya, y0 + h * yb, z + 0.032, tn[0] * 0.92, tn[1] * 0.96, rng)
        xa = a + s * 0.07
        cilindro_frente(m, xa, y0 + h * 0.46, 0.035, z + 0.034, rng)
    if grada:
        caja(m, x0 - 0.2, x1 + 0.2, 0.0, max(y0, 0.09), z, z + 0.34, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.012)
    return (cx - abierta / 2, cx + abierta / 2, y0, y1)


def cilindro_frente(m, cx, cy, r, z, rng):
    """Aldaba: rombo oscuro de hierro sobre la hoja."""
    poligono(m, [(cx - r, cy, z), (cx, cy - r, z), (cx + r, cy, z), (cx, cy + r, z)], [HIERRO[0], HIERRO[0], HIERRO[2], HIERRO[2]], FRENTE)


def zocalo(m, x0, x1, z, rng, alto=0.42, hiladas=2):
    """Zocalo de sillares en la fachada (hiladas a tresbolillo)."""
    h = alto / hiladas
    for k in range(hiladas):
        x = x0 - (0.22 if k % 2 else 0.0)
        while x < x1 - 0.02:
            a, b = max(x, x0), min(x + rng.uniform(0.42, 0.6), x1)
            if b - a > 0.05:
                extruir(m, R(a + 0.008, b - 0.008, k * h + 0.006, (k + 1) * h - 0.006), z, z + 0.045, PIEDRA, rng,
                        ymin=-0.1, ymax=alto + 0.25, var=0.07)
            x = b if b > x else x + 0.5


def esquineros(m, x, lado, y0, y1, z, rng):
    """Sillares de esquina alternos (largo y corto) en el canto de una fachada."""
    k, y = 0, y0
    while y < y1 - 0.05:
        largo = 0.30 if k % 2 == 0 else 0.19
        a, b = (x - largo, x) if lado > 0 else (x, x + largo)
        extruir(m, R(a, b, y + 0.006, min(y + 0.23, y1) - 0.006), z, z + 0.035, PIEDRA, rng, ymin=y0 - 0.3, ymax=y1, var=0.06)
        y += 0.23
        k += 1


def maceta(m, f, x, z, rng, alto=0.24, flores=2, col=None):
    cilindro(m, x, z, 0.10, 0.14, 0.0, alto, 7, BARRO, rng, techo=TIERRA)
    planta_suelta(f, (x, alto, z), rng, alto=0.42, hojas=8, flores=flores, col_flor=col)


def balaustrada(m, x0, x1, y0, z0, z1, rng, tn=MADERA_SOL, alto=0.5, paso=0.2):
    """Balaustres y pasamanos a lo largo de X."""
    zc = (z0 + z1) / 2
    n = max(2, int(round((x1 - x0) / paso)))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        caja(m, x - 0.028, x + 0.028, y0, y0 + alto, zc - 0.028, zc + 0.028, tn, rng, techo=None, var=0.06)
    caja(m, x0 - 0.05, x1 + 0.05, y0 + alto, y0 + alto + 0.07, z0, z1, tn, rng)
    caja(m, x0 - 0.03, x1 + 0.03, y0, y0 + 0.05, z0 + 0.01, z1 - 0.01, tn, rng)


# ---------- casas ----------

def casa(nombre, rng, w=5.0, d=4.0, pisos=1, color=AZUL, techo="tejas", balcon=False, plantas=True,
         buganvilla=False, puerta_x=0.0, ventanas=(-1.55, 1.55), chimenea=False, marco=None, postigo=None,
         zocalo_pintado=None, puerta_tn=None, toldos=(), flor=None):
    """Casa de Las Escalinatas: muro de color sobre zocalo (de piedra o pintado), esquineros, puerta, ventanas y
    techo a dos aguas (tejas) o a un agua (chapas de zinc). Solo se modela lo que ve la camara alta.
    v2: marcos de cal, postigos y zocalo en un color de contraste, toldos a rayas [(x, ancho, y, color)] y
    flores del color que se pida."""
    m = Malla(nombre)
    f = Malla(nombre + "_plantas", "Follaje")
    X, H = w / 2, PISO * pisos
    caja(m, -X, X, 0.0, H, -d, 0.0, color, rng, techo=None, ymin=-0.4, ymax=H + 0.3, var=0.025)
    if zocalo_pintado is None:
        zocalo(m, -X, X, 0.0, rng)
    else:   # zocalo pintado a mano con su filete claro, sobre una hilada de piedra
        zocalo(m, -X, X, 0.0, rng, alto=0.16, hiladas=1)
        extruir(m, R(-X, X, 0.16, 0.66), 0.0, 0.025, zocalo_pintado, rng, ymin=0.0, ymax=0.9)
        extruir(m, R(-X, X, 0.66, 0.71), 0.0, 0.035, MARCO_CAL, rng, ymin=0.4, ymax=0.8)
    for _ in range(5):   # parches de enlucido y manchas de humedad: pintura a mano
        px, py = rng.uniform(-X + 0.5, X - 0.9), rng.uniform(0.8, H - 0.7)
        pw, ph = rng.uniform(0.35, 0.8), rng.uniform(0.2, 0.4)
        c = mezclar(color[1], color[2] if rng.random() < 0.6 else color[0], rng.uniform(0.3, 0.6))
        poligono(m, [(px, py, 0.004), (px + pw, py + rng.uniform(-0.05, 0.05), 0.004), (px + pw * 0.9, py + ph, 0.004),
                     (px + pw * 0.1, py + ph * 0.9, 0.004)], [c] * 4, FRENTE)
    # sombra de color bajo la cornisa: degradado violaceo pintado (nunca gris)
    sombra = mezclar(color[0], mezclar(PAL["petroleo"], PAL["piedra"], 0.4), 0.45)
    poligono(m, [(-X, H - 0.55, 0.003), (X, H - 0.55, 0.003), (X, H - 0.13, 0.003), (-X, H - 0.13, 0.003)],
             [color[1], color[1], sombra, sombra], FRENTE)
    esquineros(m, -X, -1, 0.42, H - 0.14, 0.0, rng)
    esquineros(m, X, 1, 0.42, H - 0.14, 0.0, rng)
    caja(m, -X - 0.05, X + 0.05, H - 0.13, H, -d - 0.05, 0.06, MOLDURA, rng, techo=None)       # cornisa
    # planta baja
    puerta(m, puerta_x, 0.09, 0.82, 1.45, 0.0, rng, tn=PUERTA if puerta_tn is None else puerta_tn, marco=marco)
    for vx in ventanas:
        ventana(m, vx, 0.95, 0.72, 0.92, 0.0, rng, reja=(pisos == 1 and vx == ventanas[0]), persianas=(vx != ventanas[0] or pisos > 1),
                f=f if plantas else None, marco=marco, postigo=postigo, flor=flor)
    for tx, tw, ty, tc in toldos:
        toldo(m, f, tx, tw, ty, tc, rng)
    if plantas:
        for s in (-1, 1):
            maceta(m, f, puerta_x + s * 0.78, 0.26, rng, col=FLOR_ROJA if s > 0 else flor)
    # planta alta
    ov = 0.36
    if pisos > 1:
        y2 = PISO
        caja(m, -X - 0.03, X + 0.03, y2 - 0.10, y2 + 0.02, -0.02, 0.05, MOLDURA, rng, techo=None)
        if balcon:      # ARQ-06
            ov = 1.0
            caja(m, -X + 0.12, X - 0.12, y2 - 0.10, y2, 0.0, 0.80, MADERA_SOL, rng, techo=mezclar(PAL["tierra2"], PAL["sol"], 0.2))
            for x in np.linspace(-X + 0.4, X - 0.4, 4):
                poligono(m, [(x - 0.04, y2 - 0.10, 0.06), (x + 0.04, y2 - 0.10, 0.06), (x + 0.04, y2 - 0.10, 0.70),
                             (x + 0.04, y2 - 0.45, 0.06), (x - 0.04, y2 - 0.45, 0.06)][:3] , [MADERA[1]] * 3, (0, -0.3, 1))
                extruir(m, [(x - 0.04, y2 - 0.46), (x + 0.04, y2 - 0.46), (x + 0.04, y2 - 0.10), (x - 0.04, y2 - 0.10)], 0.0, 0.34,
                        MADERA, rng)
            balaustrada(m, -X + 0.16, X - 0.16, y2, 0.70, 0.78, rng)
            for x in (-X + 0.16, 0.0, X - 0.16):
                caja(m, x - 0.045, x + 0.045, y2, H, 0.70, 0.79, MADERA_SOL, rng, techo=None)
            puerta(m, 0.0, y2 + 0.0, 0.74, 1.4, 0.0, rng, grada=False, tn=PUERTA if puerta_tn is None else puerta_tn, marco=marco)
            for vx in (-X + 0.95, X - 0.95):
                ventana(m, vx, y2 + 0.5, 0.6, 0.86, 0.0, rng, persianas=True, marco=marco, postigo=postigo)
            if plantas:
                maceta(m, f, -X + 0.45, 0.42, rng, flores=3)
                for s in (0, 1):
                    f2 = Malla("x", "Follaje")
                    maceta(m, f2, 0.0, 0.0, rng, flores=2, col=FLOR_ROJA)
                    f.anexar(f2, t=(X - 0.5 - s * 0.9, y2, 0.5))
                    m.P[-1:]  # (la maceta de barro ya esta en el suelo: se recoloca abajo)
        else:
            for vx in (-X + 1.0, 0.0, X - 1.0):
                ventana(m, vx, y2 + 0.55, 0.62, 0.9, 0.0, rng, persianas=True, f=f if plantas else None, marco=marco,
                        postigo=postigo, flor=flor)
    # techo
    W = X + 0.28
    if techo == "tejas":
        s = 0.48
        ye, yr = H - ov * s + 0.10, H + (d / 2) * s + 0.10
        tejado(m, (-W, ye, ov), (W, ye, ov), (W, yr, -d / 2), (-W, yr, -d / 2), rng)
        yb = H - 0.3 * s + 0.10
        tejado(m, (W, yb, -d - 0.3), (-W, yb, -d - 0.3), (-W, yr, -d / 2), (W, yr, -d / 2), rng)
        caja(m, -W, W, ye - 0.11, ye - 0.005, ov - 0.09, ov - 0.005, MADERA, rng, techo=None)       # alero
        caja(m, -W - 0.02, W + 0.02, yr - 0.02, yr + 0.07, -d / 2 - 0.09, -d / 2 + 0.09, t3(mezclar(PAL["terracota"], PAL["sol"], 0.3), 0.2, 0.3), rng)
        for sx in (-1, 1):   # hastiales y canto del faldon
            poligono(m, [(sx * X, H, 0.0), (sx * X, H, -d), (sx * X, yr - 0.10, -d / 2)],
                     [color[1], color[1], color[2]], (sx, 0, 0))
        if chimenea:
            cz = -d * 0.72
            yc = H + (d - abs(cz) if abs(cz) > d / 2 else abs(cz)) * s
            caja(m, X - 1.25, X - 0.85, yc - 0.2, yc + 0.62, cz - 0.2, cz + 0.2, t3(mezclar(PAL["crema"], PAL["tierra1"], 0.4)), rng,
                 techo=PIEDRA_TECHO, bisel=0.02)
            caja(m, X - 1.29, X - 0.81, yc + 0.62, yc + 0.70, cz - 0.24, cz + 0.24, PIEDRA, rng, techo=PIEDRA_TECHO)
    else:   # ARQ-03: chapas de zinc a un agua, alta al fondo
        ye, yr = H + 0.06, H + 0.95
        chapas(m, (-W, ye, ov), (W, ye, ov), (W, yr, -d - 0.2), (-W, yr, -d - 0.2), rng)
        caja(m, -W, W, ye - 0.10, ye - 0.005, ov - 0.09, ov - 0.005, MADERA, rng, techo=None)
        for sx in (-1, 1):
            poligono(m, [(sx * X, H, 0.0), (sx * X, H, -d), (sx * X, yr - 0.08, -d)], [color[1], color[1], color[2]], (sx, 0, 0))
        for _ in range(3):   # piedras que sujetan las chapas
            px, pz = rng.uniform(-X + 0.4, X - 0.4), rng.uniform(-d + 0.5, -0.4)
            py = ye + (yr - ye) * (ov - pz) / (ov + d + 0.2)
            caja(m, px - 0.12, px + 0.12, py, py + 0.12, pz - 0.1, pz + 0.1, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.02)
    if buganvilla:
        enredadera(f, [(X - 0.2, H + 0.25, 0.5 if balcon else 0.1), (X - 0.5, H - 0.5, 0.82 if balcon else 0.1),
                       (X - 0.35, PISO + 0.1, 0.82 if balcon else 0.1), (X - 0.25, 1.2, 0.1)], rng, densidad=26, ancho=0.34, flores=0.68,
                   col_flor=BUGANVILLA)
        enredadera(f, [(X - 1.6, H + 0.32, 0.7 if balcon else 0.3), (X - 0.3, H + 0.3, 0.6 if balcon else 0.3)], rng, densidad=22, ancho=0.26,
                   flores=0.65, col_flor=BUGANVILLA)
    return [(nombre, [m, f])]


# ---------- ARQ-13: Biblioteca municipal ----------

def biblioteca(rng):
    """Edificio principal de la plaza. Cuerpo central adelantado con podio (0,42 m), tres gradas, portico de
    cuatro columnas, entablamento con denticulos y fronton con un libro abierto en relieve; dos alas con
    ventanas de arco, cornisa y balaustrada. La puerta queda entreabierta: por la rendija sale la luz cian
    del libro del holograma. Origen en el centro de la fachada de las alas (z = 0); el podio llega a z = 2,0
    y las gradas a z = 2,75. Altura del podio para la zona: 0,42 m; hueco libre entre columnas: 2,3 m."""
    m = Malla("ARQ-13_biblioteca")
    f = Malla("ARQ-13_plantas", "Follaje")
    e = Malla("ARQ-13_luz", "Emisivo")
    YP, XC, XA, ZC, FONDO = 0.42, 2.9, 5.5, 0.6, -5.2
    YE, YC = 2.98, 3.50      # arranque del entablamento y de la cornisa del cuerpo central
    HA = 3.0                 # alto del muro de las alas
    muro = MARFIL
    # --- podio y gradas
    caja(m, -3.15, 3.15, 0.0, YP, 0.0, 2.0, PIEDRA, rng, techo=mezclar(PIEDRA_TECHO, PAL["crema"], 0.25), bisel=0.015, ymin=-0.2, ymax=0.6)
    # cenefa del podio: losas claras y oscuras frente a la puerta
    for i in range(10):
        x0 = -2.5 + i * 0.5
        c = mezclar(PAL["tierra1"], PAL["crema"], 0.55) if i % 2 else mezclar(PAL["terracota"], PAL["tierra1"], 0.55)
        poligono(m, [(x0 + 0.02, YP + 0.004, 1.92), (x0 + 0.48, YP + 0.004, 1.92), (x0 + 0.48, YP + 0.004, 1.74), (x0 + 0.02, YP + 0.004, 1.74)],
                 [c * 0.95, c * 0.95, c, c], (0, 1, 0))
    for k, (y1, z1) in enumerate(((0.28, 2.25), (0.14, 2.50))):
        caja(m, -2.6, 2.6, 0.0, y1, 2.0, z1 + 0.25 * 0 + 0.0, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.012, ymin=-0.2, ymax=0.6)
    caja(m, -2.6, 2.6, 0.0, 0.14, 2.0, 2.75, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.012, ymin=-0.2, ymax=0.6)
    for sx in (-1, 1):   # zancas con copa de piedra
        caja(m, sx * 2.6, sx * 3.15, 0.0, 0.56, 2.0, 2.8, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.02, ymin=-0.2, ymax=0.7)
        cx = sx * 2.875
        cilindro(m, cx, 2.4, 0.10, 0.07, 0.56, 0.66, 6, PIEDRA, rng, techo=None)
        cilindro(m, cx, 2.4, 0.07, 0.19, 0.66, 0.86, 6, PIEDRA, rng, techo=TIERRA)
        planta_suelta(f, (cx, 0.86, 2.4), rng, alto=0.42, hojas=9, flores=3, col_flor=FLOR_ROJA)
    # --- cuerpo central
    caja(m, -XC, XC, 0.0, YC, FONDO, ZC, muro, rng, techo=None, ymin=-0.5, ymax=YC + 0.6, var=0.02)
    zocalo(m, -XC, XC, ZC, rng, alto=YP + 0.36, hiladas=3)
    rend = puerta(m, 0.0, YP, 1.5, 2.1, ZC, rng, tn=t3(mezclar(PAL["madera1"], PAL["tierra2"], 0.55), 0.3, 0.3), grada=False, abierta=0.58)
    # rendija de luz cian y abanico de luz sobre el dintel
    poligono(e, [(rend[0], rend[2] + 0.02, ZC + 0.02), (rend[1], rend[2] + 0.02, ZC + 0.02), (rend[1], rend[3] - 0.02, ZC + 0.02),
                 (rend[0], rend[3] - 0.02, ZC + 0.02)], [PAL["cian"]] * 4, FRENTE)
    arco_y = YP + 2.1 + 0.19
    pts = [(0.62 * math.cos(a), arco_y + 0.34 * math.sin(a)) for a in np.linspace(0, math.pi, 7)]
    extruir(m, [(1.1 * x, arco_y + (y - arco_y) * 1.25 - 0.02) for x, y in pts], ZC, ZC + 0.06, PIEDRA, rng, ymin=arco_y - 0.5, ymax=arco_y + 0.5)
    extruir(m, pts, ZC, ZC + 0.066, t3(mezclar(PAL["cian_medio"], PAL["petroleo"], 0.45), 0.2, 0.2), rng, cantos=False)
    for k in range(1, 6):   # radios del abanico
        a = math.pi * k / 6
        poligono(m, [(0.02 * math.sin(a), arco_y - 0.0 + 0.0, ZC + 0.068), (0.6 * math.cos(a) + 0.02 * math.sin(a), arco_y + 0.33 * math.sin(a), ZC + 0.068),
                     (0.6 * math.cos(a) - 0.02 * math.sin(a), arco_y + 0.33 * math.sin(a) + 0.02 * math.cos(a) * 0, ZC + 0.068)],
                 [PIEDRA[2]] * 3, FRENTE)
    for sx in (-1, 1):   # ventanas altas a los lados de la puerta y faroles de pared
        ventana(m, sx * 2.0, YP + 0.62, 0.62, 1.42, ZC, rng, persianas=False, arco=True)
        caja(m, sx * 1.12 - 0.05, sx * 1.12 + 0.05, YP + 1.52, YP + 1.60, ZC, ZC + 0.2, HIERRO, rng)
        cristal = tono(mezclar(PAL["sol"], PAL["crema"], 0.35), mezclar(PAL["crema"], PAL["sol"], 0.25), mezclar(PAL["crema"], PAL["brillo"], 0.35))
        cilindro(m, sx * 1.12, ZC + 0.2, 0.05, 0.08, YP + 1.30, YP + 1.52, 4, cristal, rng, techo=None, giro=math.pi / 4)
        cono(m, sx * 1.12, ZC + 0.2, 0.10, YP + 1.60, YP + 1.72, 4, HIERRO, rng, giro=math.pi / 4)
    # --- portico: cuatro columnas (hueco central de 2,3 m para la losa de la puerta)
    for x in (-2.62, -1.33, 1.33, 2.62):
        caja(m, x - 0.19, x + 0.19, YP, YP + 0.12, 1.36, 1.74, PIEDRA, rng, techo=PIEDRA_TECHO, bisel=0.015)
        cilindro(m, x, 1.55, 0.15, 0.125, YP + 0.12, YE - 0.14, 8, MARFIL, rng, techo=None, ymin=YP - 0.6, ymax=YE + 0.2)
        cilindro(m, x, 1.55, 0.165, 0.165, YP + 0.12, YP + 0.19, 8, PIEDRA, rng)
        caja(m, x - 0.19, x + 0.19, YE - 0.14, YE, 1.36, 1.74, PIEDRA, rng, techo=None, ymin=YE - 0.5, ymax=YE + 0.1)
    # --- entablamento, denticulos y cornisa
    caja(m, -3.0, 3.0, YE, YC - 0.12, ZC, 1.80, MARFIL, rng, techo=None, ymin=YE - 0.8, ymax=YC + 0.2)
    panel(m, -2.9, 2.9, YE + 0.10, YC - 0.22, 1.803, mezclar(MARFIL[1], PAL["tierra1"], 0.35), mezclar(MARFIL[1], PAL["tierra1"], 0.2), rng)
    for i in range(24):
        x = -2.88 + i * 0.25
        extruir(m, R(x, x + 0.13, YC - 0.21, YC - 0.12), 1.80, 1.86, PIEDRA, rng, ymin=YC - 0.5, ymax=YC, var=0.05)
    caja(m, -3.1, 3.1, YC - 0.12, YC, ZC, 1.90, PIEDRA, rng, techo=PIEDRA_TECHO, ymin=YC - 0.5, ymax=YC + 0.1)
    # --- fronton con el libro abierto en relieve (sin letras)
    YA = 4.62
    extruir(m, [(-3.1, YC), (3.1, YC), (0.0, YA)], 1.2, 1.86, PIEDRA, rng, ymin=YC - 0.6, ymax=YA + 0.1)
    extruir(m, [(-2.52, YC + 0.10), (2.52, YC + 0.10), (0.0, YA - 0.20)], 1.86, 1.868, MARFIL, rng, ymin=YC - 0.3, ymax=YA + 0.4, cantos=False)
    yb = YC + 0.24
    tapa = t3(mezclar(PAL["terracota"], PAL["coral"], 0.4), 0.2, 0.25)
    hoja_t = t3(mezclar(PAL["crema"], PAL["brillo"], 0.45), 0.22, 0.0)
    for s in (-1, 1):
        cub = [(0.0, yb - 0.03), (s * 0.80, yb + 0.07), (s * 0.80, yb + 0.55), (0.0, yb + 0.43)]
        pag = [(s * 0.02, yb + 0.02), (s * 0.74, yb + 0.115), (s * 0.74, yb + 0.56), (s * 0.02, yb + 0.455)]
        if s < 0:
            cub, pag = cub[::-1], pag[::-1]
        extruir(m, cub, 1.868, 1.90, tapa, rng)
        extruir(m, pag, 1.90, 1.93, hoja_t, rng, var=0.02)
        for k in range(4):   # renglones: rayas, no letras
            t = 0.2 + k * 0.19
            x0, x1 = s * 0.12, s * (0.66 - (0.12 if k == 3 else 0.0))
            y0 = yb + 0.02 + (0.455 - 0.02) * t
            dy = 0.095 * abs(x0) / 0.72, 0.095 * abs(x1) / 0.72
            poligono(m, [(x0, y0 + dy[0] - 0.012, 1.932), (x1, y0 + dy[1] - 0.012, 1.932), (x1, y0 + dy[1] + 0.012, 1.932),
                         (x0, y0 + dy[0] + 0.012, 1.932)], [mezclar(PAL["tierra2"], PAL["madera1"], 0.3)] * 4, FRENTE)
    extruir(m, [(-0.035, yb - 0.16), (0.035, yb - 0.16), (0.035, yb + 0.02), (-0.035, yb + 0.02)], 1.868, 1.91, t3(PAL["coral"], 0.15, 0.2), rng)
    # remates del fronton
    for x, y in ((0.0, YA), (-3.0, YC), (3.0, YC)):
        caja(m, x - 0.13, x + 0.13, y, y + 0.14, 1.40, 1.86, PIEDRA, rng, techo=PIEDRA_TECHO)
        cono(m, x, 1.63, 0.12, y + 0.14, y + 0.42, 6, PIEDRA, rng)
    # --- techo del cuerpo central: dos aguas con la cumbrera hacia el fondo
    tejado(m, (-3.1, YC, FONDO), (-3.1, YC, 1.84), (0.0, YA, 1.84), (0.0, YA, FONDO), rng, paso=0.42, ancho=0.34)
    tejado(m, (3.1, YC, 1.84), (3.1, YC, FONDO), (0.0, YA, FONDO), (0.0, YA, 1.84), rng, paso=0.42, ancho=0.34)
    caja(m, -0.09, 0.09, YA - 0.03, YA + 0.07, FONDO, 1.80, t3(mezclar(PAL["terracota"], PAL["sol"], 0.3), 0.2, 0.3), rng)
    # --- alas
    for sx in (-1, 1):
        x0, x1 = (XC, XA) if sx > 0 else (-XA, -XC)
        caja(m, x0, x1, 0.0, HA, FONDO, 0.0, muro, rng, techo=None, ymin=-0.5, ymax=YC + 0.6, var=0.02)
        zocalo(m, x0, x1, 0.0, rng, alto=0.54, hiladas=3)
        for vx in (x0 + 0.72, x1 - 0.72):
            ventana(m, vx, 1.0, 0.66, 1.22, 0.0, rng, persianas=True, arco=True, f=f)
        esquineros(m, sx * XA, sx, 0.54, HA - 0.16, 0.0, rng)
        extruir(m, R(sx * XC - (0.0 if sx > 0 else 0.26), sx * XC + (0.26 if sx > 0 else 0.0), 0.54, HA - 0.16), 0.0, 0.05, PIEDRA, rng)
        caja(m, x0 - 0.02, x1 + 0.08 * (1 if sx > 0 else 0) - 0.0, HA - 0.16, HA, FONDO, 0.10, PIEDRA, rng, techo=PIEDRA_TECHO, ymin=HA - 0.6, ymax=HA + 0.1)
        balaustrada(m, x0 + 0.12, x1 - 0.06, HA, -0.07, 0.07, rng, tn=PIEDRA, alto=0.34, paso=0.24)
        # faldon de tejas del ala: sube hacia el cuerpo central
        if sx > 0:
            tejado(m, (x1, HA + 0.02, -0.14), (x1, HA + 0.02, FONDO), (x0, HA + 0.42, FONDO), (x0, HA + 0.42, -0.14), rng, paso=0.42, ancho=0.34)
        else:
            tejado(m, (x0, HA + 0.02, FONDO), (x0, HA + 0.02, -0.14), (x1, HA + 0.42, -0.14), (x1, HA + 0.42, FONDO), rng, paso=0.42, ancho=0.34)
        # costado exterior
        poligono(m, [(sx * XA, HA, 0.0), (sx * XA, HA, FONDO), (sx * XA, HA + 0.02, FONDO), (sx * XA, HA + 0.02, 0.0)], [muro[2]] * 4, (sx, 0, 0))
    presesgar(e)
    return [("ARQ-13_biblioteca", [m, f, e])]


# ---------- TER-14: suelo de la plaza (v2 «color y vida») ----------

# puntos de la zona (los mismos de juego/zonas/ciudad/ciudad.gd)
LOSAS = [(-12.0, 0.55, 2.2, 2.2), (12.3, 1.2, 2.2, 2.4), (0.0, -6.35, 5.6, 1.5)]   # (cx, cz, ancho, fondo): casa, sendero y pie de las gradas
BOCA = (11.4, 14.2, -0.35, 2.75)                                          # boca del camino: el adoquin se pierde en tierra
# v2: panos de adoquin en tres tonos separados por cenefas de mosaico turquesa y petroleo, una onda de mosaico
# que cruza la plaza por abajo (como las ondas de la escalinata), las fases de la Luna alrededor de la fuente y
# un medallon con una iguana. Sombra de color (azul violaceo) junto a las fachadas y desgaste en los caminos.
VX = (-9.4, -5.0, 5.0, 9.4)          # cenefas verticales (x)
HZ = (-5.0, 1.0)                     # cenefas horizontales (z)
HW = 0.18                            # medio ancho de una cenefa
MEDALLON = (-7.2, 2.75, 1.25)        # mosaico de la iguana: centro (x, z) y radio
R_ROSA = 4.02
R_LUNAS = 3.54                       # radio del anillo de las fases de la Luna
ONDA_HW = 0.40


def onda_z(x):
    """Linea media de la onda de mosaico que cruza la plaza (z en funcion de x)."""
    return 5.75 + 0.42 * math.sin(0.62 * x + 0.4)


def suelo(rng):
    X0, X1, Z0, Z1 = -15.2, 15.2, -10.4, 10.2
    NX, NZ = 3, 2
    trozos = [[Malla(f"TER-14_suelo_{i}{k}") for k in range(NZ)] for i in range(NX)]

    def trozo(x, z):
        i = min(NX - 1, max(0, int((x - X0) / (X1 - X0) * NX)))
        k = min(NZ - 1, max(0, int((z - Z0) / (Z1 - Z0) * NZ)))
        return trozos[i][k]

    lech = mezclar(mezclar(LECHADA, PAL["tierra2"], 0.35), PAL["petroleo"], 0.10)
    for i in range(NX):
        for k in range(NZ):
            a, b = X0 + (X1 - X0) * i / NX, X0 + (X1 - X0) * (i + 1) / NX
            c, d = Z0 + (Z1 - Z0) * k / NZ, Z0 + (Z1 - Z0) * (k + 1) / NZ
            poligono(trozos[i][k], [(a, 0.0, d), (b, 0.0, d), (b, 0.0, c), (a, 0.0, c)], [lech * 0.95, lech, lech * 1.03, lech], (0, 1, 0))

    # ---- tonos
    terracota = mezclar(PAL["terracota"], PAL["tierra1"], 0.50)
    crema_p = mezclar(PAL["crema"], PAL["tierra1"], 0.40)
    arena = mezclar(mezclar(PAL["tierra1"], PAL["crema"], 0.30), PAL["coral"], 0.10)
    familias = [terracota, crema_p, arena]
    turq = mezclar(PAL["cian_medio"], PAL["petroleo"], 0.30)
    turq_cl = mezclar(PAL["cian_medio"], PAL["brillo"], 0.25)
    petro = PAL["petroleo"]
    crema_m = mezclar(PAL["crema"], PAL["brillo"], 0.20)
    violeta = mezclar(PAL["petroleo"], PAL["piedra"], 0.40)
    clara = mezclar(PAL["crema"], PAL["tierra1"], 0.30)
    cenefa_t = mezclar(PAL["terracota"], PAL["tierra1"], 0.72)
    tierra = mezclar(PAL["tierra2"], PAL["tierra1"], 0.35)
    coral = mezclar(PAL["coral"], PAL["sol"], 0.15)

    def sombra_color(x, z):
        """0..1: junto a las fachadas el suelo se tine de azul violaceo (sombra con color, nunca gris)."""
        t = max(0.0, 1.0 - (z + 9.85) / 1.9)
        if x < 0 or not (BOCA[2] - 0.6 < z < BOCA[3] + 0.6):
            t = max(t, 1.0 - (13.3 - abs(x)) / 1.6)
        return min(1.0, t)

    def desgaste(x, z):
        """0..1: losas pulidas por los pasos en los caminos de la casa al sendero y a la biblioteca."""
        def seg(ax, az, bx, bz):
            vx, vz = bx - ax, bz - az
            t = max(0.0, min(1.0, ((x - ax) * vx + (z - az) * vz) / (vx * vx + vz * vz)))
            return math.hypot(x - ax - vx * t, z - az - vz * t)
        d = min(seg(-12.0, 0.55, 12.3, 1.2), seg(0.0, -6.4, 0.0, -1.0))
        return max(0.0, 1.0 - d / 1.5)

    def pintar(col, x, z):
        n = math.sin(0.31 * x + 0.17 * z) * math.sin(0.23 * z - 0.41 * x + 1.3)
        c = np.asarray(col, float) * (1 + 0.07 * n)
        c = mezclar(c, PAL["crema"], 0.12 * desgaste(x, z))
        return mezclar(c, violeta, 0.40 * sombra_color(x, z))

    def losa(m, x0, x1, z0, z1, col, y=0.006, junta=0.016, var=0.025):
        col = np.asarray(col, float)
        esquinas = [(x0 + junta, z1 - junta, 0.95), (x1 - junta, z1 - junta, 1.0), (x1 - junta, z0 + junta, 1.05), (x0 + junta, z0 + junta, 1.0)]
        poligono(m, [(x, y, z) for x, z, _ in esquinas],
                 [pintar(col, x, z) * k * (1 + rng.normal(0, var)) for x, z, k in esquinas], (0, 1, 0))

    def tesela(m, x0, x1, z0, z1, col, y=0.0075):
        losa(m, x0, x1, z0, z1, col, y=y, junta=0.009, var=0.04)

    def en_losa(x, z, margen=0.0):
        for cx, cz, w, d in LOSAS:
            if abs(x - cx) < w / 2 + margen and abs(z - cz) < d / 2 + margen:
                return True
        return False

    mx, mz, mr = MEDALLON

    def ocupado(x, z, margen=0.0):
        return (math.hypot(x, z) < R_ROSA + 0.24 + margen or en_losa(x, z, 0.22 + margen) or abs(z - onda_z(x)) < ONDA_HW + margen
                or math.hypot(x - mx, z - mz) < mr + 0.06 + margen)

    def familia(x, z):
        ci = sum(1 for v in VX if x > v)
        ri = 0 if z < HZ[0] else (1 if z < HZ[1] else (2 if z < onda_z(x) else 3))
        return familias[(ci + ri * 2) % 3]

    # ---- tierra de la boca del camino
    bx0, bx1, bz0, bz1 = BOCA
    poligono(trozo(bx1, (bz0 + bz1) / 2), [(bx0, 0.003, bz1), (X1, 0.003, bz1 + 0.5), (X1, 0.003, bz0 - 0.5), (bx0, 0.003, bz0)],
             [tierra * 0.95, tierra, mezclar(tierra, PAL["crema"], 0.15), tierra * 0.97], (0, 1, 0))

    # ---- adoquines por panos: hiladas a tresbolillo que se ajustan a cada pano
    paso = 0.40
    bandas = [(Z0, HZ[0] - HW), (HZ[0] + HW, HZ[1] - HW), (HZ[1] + HW, Z1)]
    for za, zb in bandas:
        nz = max(1, int(round((zb - za) / paso)))
        pz = (zb - za) / nz
        for k in range(nz):
            z0, z1 = za + k * pz, za + (k + 1) * pz
            zc = (z0 + z1) / 2
            cortes = [X0]
            if -9.85 < zc < 8.6:
                for v in VX:
                    cortes += [v - HW, v + HW]
            cortes.append(X1)
            for xa, xb in zip(cortes[0::2], cortes[1::2]):
                nx = max(1, int(round((xb - xa) / paso)))
                px = (xb - xa) / nx
                desf = px / 2 if k % 2 else 0.0
                for i in range(nx + 1):
                    x0, x1 = max(xa, xa - desf + i * px), min(xb, xa - desf + (i + 1) * px)
                    if x1 - x0 < 0.05:
                        continue
                    cx = (x0 + x1) / 2
                    if ocupado(cx, zc):
                        continue
                    if bx0 < cx and bz0 - 0.4 < zc < bz1 + 0.4 and rng.random() < (cx - bx0) / (bx1 - bx0) * 1.15:
                        continue
                    col = familia(cx, zc)
                    r = rng.random()
                    if r < 0.12:
                        col = mezclar(col, familias[int(rng.integers(3))], 0.6)
                    elif r < 0.15:
                        col = mezclar(col, PAL["tierra2"], 0.30)        # losa remendada
                    losa(trozo(cx, zc), x0, x1, z0, z1, col * (1 + rng.normal(0, 0.03)))

    # ---- cenefas de mosaico: petroleo a los lados y turquesa con crema al centro
    t = 0.12

    def cenefa(eje_v, fijo, a, b):
        n = int((b - a) / t)
        for j in range(n):
            s0, s1 = a + j * t, a + (j + 1) * t
            for s, (u0, u1) in enumerate(((-HW, -HW / 3), (-HW / 3, HW / 3), (HW / 3, HW))):
                col = petro if s != 1 else (turq if j % 2 == 0 else crema_m)
                if eje_v:
                    x0, x1, z0, z1 = fijo + u0, fijo + u1, s0, s1
                else:
                    x0, x1, z0, z1 = s0, s1, fijo + u0, fijo + u1
                cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
                if ocupado(cx, cz, -0.02) or (bx0 - 0.3 < cx and bz0 - 0.4 < cz < bz1 + 0.4):
                    continue
                tesela(trozo(cx, cz), x0, x1, z0, z1, col)

    for v in VX:
        cenefa(True, v, -9.85, 8.6)
    for h in HZ:
        cenefa(False, h, -13.3, 13.3)
    # rosetones en los cruces: cuadro turquesa con un rombo coral
    for v in VX:
        for h in HZ:
            if ocupado(v, h) or (bx0 - 0.3 < v and bz0 - 0.4 < h < bz1 + 0.4):
                continue
            m = trozo(v, h)
            tesela(m, v - 0.3, v + 0.3, h - 0.3, h + 0.3, turq, y=0.0085)
            poligono(m, [(v - 0.22, 0.0095, h), (v, 0.0095, h + 0.22), (v + 0.22, 0.0095, h), (v, 0.0095, h - 0.22)], [coral] * 4, (0, 1, 0))
            poligono(m, [(v - 0.08, 0.0102, h), (v, 0.0102, h + 0.08), (v + 0.08, 0.0102, h), (v, 0.0102, h - 0.08)], [crema_m] * 4, (0, 1, 0))

    # ---- onda de mosaico que cruza la plaza por abajo
    franjas = ((-0.40, -0.28, petro), (-0.28, -0.10, turq), (-0.10, 0.10, crema_m), (0.10, 0.28, turq_cl), (0.28, 0.40, petro))
    paso_o = 0.12
    x = -13.3
    while x < 13.3 - 1e-6:
        xa, xb = x + 0.0045, min(x + paso_o, 13.3) - 0.0045
        for v0, v1, col in franjas:
            col = np.asarray(col, float) * (1 + rng.normal(0, 0.04))
            pts = [(xa, onda_z(xa) + v0 + 0.0045), (xb, onda_z(xb) + v0 + 0.0045), (xb, onda_z(xb) + v1 - 0.0045), (xa, onda_z(xa) + v1 - 0.0045)]
            poligono(trozo((xa + xb) / 2, onda_z(xa)), [(px_, 0.0075, pz_) for px_, pz_ in pts],
                     [pintar(col, px_, pz_) for px_, pz_ in pts], (0, 1, 0))
        x += paso_o

    # ---- losas claras de las salidas, con marco de cenefa
    for cx, cz, w, d in LOSAS:
        m = trozo(cx, cz)
        losa(m, cx - w / 2 - 0.12, cx + w / 2 + 0.12, cz - d / 2 - 0.12, cz + d / 2 + 0.12, cenefa_t, y=0.005, junta=0.0)
        n_x, n_z = max(1, int(round(w / 0.7))), max(1, int(round(d / 0.7)))
        for i in range(n_x):
            for k in range(n_z):
                losa(m, cx - w / 2 + w * i / n_x, cx - w / 2 + w * (i + 1) / n_x, cz - d / 2 + d * k / n_z, cz - d / 2 + d * (k + 1) / n_z,
                     clara * (1.0 if (i + k) % 2 else 0.95), y=0.008)

    # ---- anillos de mosaico (rosa de la fuente y medallon)
    def anillo(r0, r1, n, colores, desfase=0.0, y=0.007, cx=0.0, cz=0.0):
        for i in range(n):
            a0, a1 = 2 * math.pi * (i + desfase) / n, 2 * math.pi * (i + 1 + desfase) / n
            j = 0.012 / max(r0, 0.5)
            col = np.asarray(colores[i % len(colores)], float) * (1 + rng.normal(0, 0.04))
            pts = [(r0 + 0.012, a0 + j), (r1 - 0.012, a0 + j), (r1 - 0.012, a1 - j), (r0 + 0.012, a1 - j)]
            am = (a0 + a1) / 2
            m = trozo(cx + math.cos(am) * (r0 + r1) / 2, cz + math.sin(am) * (r0 + r1) / 2)
            poligono(m, [(cx + r * math.cos(a), y, cz + r * math.sin(a)) for r, a in pts], [col * 0.95, col, col * 1.03, col], (0, 1, 0))

    def disco(cx, cz, r, col, y, lados=20):
        m = trozo(cx, cz)
        poligono(m, [(cx + r * math.cos(2 * math.pi * i / lados), y, cz + r * math.sin(2 * math.pi * i / lados)) for i in range(lados)],
                 [np.asarray(col, float) * (1 + 0.04 * math.sin(i)) for i in range(lados)], (0, 1, 0))

    crema, sol = PAL["crema"], PAL["sol"]
    anillo(1.55, 2.05, 24, [clara, clara * 0.93])
    anillo(2.05, 2.30, 48, [petro, crema_m])
    anillo(2.30, 2.55, 48, [crema, sol], desfase=0.5)
    anillo(2.55, 2.80, 48, [turq, petro])
    anillo(2.80, 3.06, 32, [clara, clara * 0.93], desfase=0.5)
    # cielo de mosaico con las ocho fases de la Luna (la nueva abajo, junto al camino; la llena hacia la biblioteca)
    cielo = mezclar(PAL["petroleo"], PAL["oscuro"], 0.22)
    anillo(3.06, R_ROSA, 48, [cielo, cielo * 0.93])
    luna = mezclar(PAL["crema"], PAL["brillo"], 0.35)
    luna_osc = mezclar(PAL["petroleo"], PAL["oscuro"], 0.62)
    rl = 0.33
    for k in range(8):
        a = math.pi / 2 + 2 * math.pi * k / 8
        cx, cz = math.cos(a) * R_LUNAS, math.sin(a) * R_LUNAS
        disco(cx, cz, rl + 0.035, crema_m, 0.0088)
        disco(cx, cz, rl, luna_osc, 0.0094)
        kk = k if k <= 4 else 8 - k
        fi = math.pi * kk / 4
        m = trozo(cx, cz)
        cortes = 10
        for s in range(cortes):
            v0, v1 = -rl + 2 * rl * s / cortes, -rl + 2 * rl * (s + 1) / cortes
            l0, l1 = math.sqrt(max(rl * rl - v0 * v0, 0)), math.sqrt(max(rl * rl - v1 * v1, 0))
            t0, t1 = math.cos(fi) * l0, math.cos(fi) * l1
            if k <= 4:
                a0, b0, a1, b1 = t0, l0, t1, l1
            else:
                a0, b0, a1, b1 = -l0, -t0, -l1, -t1
            if b0 - a0 < 1e-4 and b1 - a1 < 1e-4:
                continue
            poligono(m, [(cx + a0, 0.0102, cz - v0), (cx + b0, 0.0102, cz - v0), (cx + b1, 0.0102, cz - v1), (cx + a1, 0.0102, cz - v1)],
                     [luna * 0.96, luna, luna, luna * 0.96], (0, 1, 0))
        # estrella de cuatro puntas entre luna y luna
        ae = a + math.pi / 8
        ex, ez = math.cos(ae) * R_LUNAS, math.sin(ae) * R_LUNAS
        for g in range(4):
            b = g * math.pi / 2
            poligono(trozo(ex, ez), [(ex, 0.0098, ez), (ex + 0.05 * math.cos(b - 0.8), 0.0098, ez + 0.05 * math.sin(b - 0.8)),
                                     (ex + 0.17 * math.cos(b), 0.0098, ez + 0.17 * math.sin(b)),
                                     (ex + 0.05 * math.cos(b + 0.8), 0.0098, ez + 0.05 * math.sin(b + 0.8))], [PAL["dorado"]] * 4, (0, 1, 0))
    for _ in range(26):   # estrellitas sueltas
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(3.15, 3.95)
        x, z = math.cos(a) * r, math.sin(a) * r
        if min(math.hypot(x - math.cos(math.pi / 2 + 2 * math.pi * k / 8) * R_LUNAS, z - math.sin(math.pi / 2 + 2 * math.pi * k / 8) * R_LUNAS)
               for k in range(8)) < rl + 0.1:
            continue
        tesela(trozo(x, z), x - 0.035, x + 0.035, z - 0.035, z + 0.035, crema_m, y=0.0096)
    anillo(R_ROSA, R_ROSA + 0.22, 64, [turq, crema_m], y=0.006)

    # ---- medallon de la iguana (la plaza lleva su nombre)
    anillo(mr - 0.16, mr, 40, [petro, turq], cx=mx, cz=mz)
    anillo(mr - 0.26, mr - 0.16, 40, [coral, crema_m], cx=mx, cz=mz)
    disco(mx, mz, mr - 0.26, mezclar(PAL["crema"], PAL["tierra1"], 0.15), 0.0072, lados=28)
    S = 0.92
    mm = trozo(mx, mz)

    def W(lx, ly, y=0.0098):
        return (mx + lx * S, y, mz - ly * S)
    espina = [(0.95, 0.04), (0.66, 0.0), (0.40, -0.02), (0.12, 0.0), (-0.16, 0.04), (-0.40, 0.11), (-0.60, 0.06),
              (-0.75, -0.10), (-0.82, -0.30), (-0.76, -0.47), (-0.62, -0.55)]
    anchos = [0.0, 0.19, 0.17, 0.28, 0.22, 0.15, 0.11, 0.08, 0.06, 0.04, 0.0]
    verde = mezclar(PAL["hierba_sol"], PAL["hierba_sombra"], 0.25)
    verde_osc = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.25)
    verde_cl = mezclar(PAL["hierba_sol"], PAL["dorado"], 0.35)

    def lados(i):
        p = np.array(espina[i], float)
        a = np.array(espina[max(i - 1, 0)], float)
        b = np.array(espina[min(i + 1, len(espina) - 1)], float)
        tng = b - a
        tng /= np.linalg.norm(tng)
        nrm = np.array([-tng[1], tng[0]])
        return p + nrm * anchos[i] / 2, p - nrm * anchos[i] / 2

    # patas (debajo del cuerpo)
    for (ax, ay), sgn in (((0.36, 0.0), 1), ((0.36, 0.0), -1), ((-0.12, 0.03), 1), ((-0.12, 0.03), -1)):
        codo = (ax + 0.08, ay + sgn * 0.27)
        pie = (ax - 0.04, ay + sgn * 0.36)
        for p, q in (((ax, ay), codo), (codo, pie)):
            d = np.array(q) - np.array(p)
            nn = np.array([-d[1], d[0]]) / np.linalg.norm(d) * 0.035
            poligono(mm, [W(*(np.array(p) + nn)), W(*(np.array(q) + nn)), W(*(np.array(q) - nn)), W(*(np.array(p) - nn))], [verde_osc] * 4, (0, 1, 0))
        for dedo in (-0.5, 0.0, 0.5):
            dd = np.array([math.cos(math.atan2(sgn, -0.3) + dedo), math.sin(math.atan2(sgn, -0.3) + dedo)]) * 0.07
            poligono(mm, [W(pie[0], pie[1], 0.0099), W(pie[0] + dd[0] + 0.01, pie[1] + dd[1], 0.0099), W(pie[0] + dd[0] - 0.01, pie[1] + dd[1] + 0.01, 0.0099)],
                     [verde_osc] * 3, (0, 1, 0))
    # cuerpo y cola, con bandas oscuras en la cola
    for i in range(len(espina) - 1):
        l0, r0 = lados(i)
        l1, r1 = lados(i + 1)
        col = verde if i < 5 else (verde_osc if i % 2 else verde)
        poligono(mm, [W(*l0, 0.0101), W(*l1, 0.0101), W(*r1, 0.0101), W(*r0, 0.0101)], [col, col * 1.04, col * 1.04, col], (0, 1, 0))
    # cresta dorada en chevrones, papada y ojos
    for i in range(1, 6):
        p = np.array(espina[i], float)
        q = np.array(espina[i + 1], float)
        d = (q - p) / np.linalg.norm(q - p) * 0.09
        nn = np.array([-d[1], d[0]]) * 0.7
        poligono(mm, [W(*(p + nn), 0.0106), W(*(p + d * 1.2), 0.0106), W(*(p - nn), 0.0106)], [verde_cl] * 3, (0, 1, 0))
    poligono(mm, [W(0.70, -0.08, 0.0104), W(0.58, -0.17, 0.0104), W(0.52, -0.07, 0.0104)], [mezclar(PAL["sol"], PAL["dorado"], 0.5)] * 3, (0, 1, 0))
    for sgn in (1, -1):
        ex, ey = 0.78, 0.02 + sgn * 0.055
        poligono(mm, [W(ex - 0.025, ey, 0.0106), W(ex, ey + 0.025, 0.0106), W(ex + 0.025, ey, 0.0106), W(ex, ey - 0.025, 0.0106)], [PAL["oscuro"]] * 4, (0, 1, 0))
    nodos = []
    for i in range(NX):
        for k in range(NZ):
            nodos.append((f"TER-14_suelo_{i}{k}", [trozos[i][k]]))
    return nodos


RECURSOS = {
    # v2: colores vivos del barrio con detalles en contraste (marcos de cal, postigos, zocalo pintado y toldos)
    "ARQ-01": (lambda r: casa("ARQ-01_casa_amarilla", r, w=5.0, d=4.0, pisos=2, color=AMARILLO_V, balcon=True, buganvilla=True,
                              puerta_x=0.0, ventanas=(-1.6, 1.6), chimenea=True, marco=MARCO_CAL, postigo=POSTIGO["turquesa"],
                              zocalo_pintado=POSTIGO["turquesa"], puerta_tn=POSTIGO["coral"], flor=BUGANVILLA), 301),
    "ARQ-01_rosa": (lambda r: casa("ARQ-01_casa_rosa", r, w=4.6, d=4.0, pisos=2, color=ROSA_V, puerta_x=-1.0, ventanas=(0.9,),
                                   marco=MARCO_CAL, postigo=POSTIGO["verde"], zocalo_pintado=POSTIGO["anil"], buganvilla=True,
                                   toldos=((0.9, 1.15, 2.08, TOLDO["verde"]),), flor=FLOR_AMARILLA), 311),
    "ARQ-02": (lambda r: casa("ARQ-02_casa_azul", r, w=5.2, d=4.2, color=TURQUESA_V, puerta_x=-0.5, ventanas=(-1.8, 1.3),
                              marco=MARCO_CAL, postigo=POSTIGO["amarillo"], zocalo_pintado=CORAL_V, puerta_tn=POSTIGO["amarillo"],
                              toldos=((1.3, 1.1, 2.12, TOLDO["coral"]),), flor=BUGANVILLA), 302),
    "ARQ-02_coral": (lambda r: casa("ARQ-02_casa_coral", r, w=5.4, d=4.2, color=CORAL_V, puerta_x=0.7, ventanas=(-1.4, 1.95),
                                    marco=MARCO_CAL, postigo=POSTIGO["turquesa"], zocalo_pintado=POSTIGO["turquesa"],
                                    toldos=((0.7, 1.25, 1.9, TOLDO["turquesa"]),), flor=FLOR_AMARILLA), 312),
    "ARQ-02_crema": (lambda r: casa("ARQ-02_casa_crema", r, w=4.8, d=4.0, color=CAL_V, puerta_x=-1.2, ventanas=(0.2, 1.5),
                                    marco=None, postigo=POSTIGO["coral"], zocalo_pintado=POSTIGO["anil"], puerta_tn=POSTIGO["anil"],
                                    buganvilla=True, toldos=((0.85, 2.3, 2.12, TOLDO["amarillo"]),), flor=BUGANVILLA), 322),
    "ARQ-02_verde": (lambda r: casa("ARQ-02_casa_verde", r, w=5.0, d=4.2, color=MENTA_V, puerta_x=1.1, ventanas=(-1.5, -0.2),
                                    marco=MARCO_CAL, postigo=POSTIGO["coral"], zocalo_pintado=POSTIGO["verde"], puerta_tn=POSTIGO["coral"],
                                    flor=BUGANVILLA), 332),
    "ARQ-02_zinc": (lambda r: casa("ARQ-02_casa_zinc", r, w=4.6, d=3.8, color=ANIL_V, techo="zinc", puerta_x=0.9, ventanas=(-1.1,),
                                   plantas=True, marco=MARCO_CAL, postigo=POSTIGO["amarillo"], zocalo_pintado=AMARILLO_V,
                                   toldos=((-1.1, 1.1, 2.1, TOLDO["amarillo"]),), flor=FLOR_AMARILLA), 342),
    "ARQ-13": (biblioteca, 313),
    "TER-14": (suelo, 414),
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
