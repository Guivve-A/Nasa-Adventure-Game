"""Plaza de las Iguanas, version 2 («color y vida»): recursos nuevos que dan vida a la plaza.

Recursos (juego/modelos/ciudad/<ID>.glb; origen en el centro de la base y frente hacia +Z):
  FAU-12  Paloma (ID NUEVO de la familia FAU): cuerpo, cabeza y dos alas en nodos aparte para el aleteo
          (FAU-12_ala_i y FAU-12_ala_d giran sobre el hombro). Mide 0,30 m de pico a cola.
  URB-13  Puesto de frutas (ID NUEVO): mesa de tablas, cajones de fruta de colores, platanos colgados,
          toldo a rayas, la lata de la confianza y una pizarra con una fruta dibujada (sin letras).
  URB-14  Tablon de anuncios (ID NUEVO): tablero de corcho con tejadillo y papeles de colores; el grande es
          la convocatoria, con una Luna creciente dibujada (sin letras ni numeros).
  URB-15  Grupo de macetas de barro (ID NUEVO): nodos URB-15_a (buganvilla, cayena y helecho) y URB-15_b
          (palmita y flores).
  VEG-04  Cocotero (hoja HR_VEG_v1): tronco anillado e inclinado, nueve palmas y cocos.
  COL-03  Placa de circuito, COL-06 Cable de cobre y COL-12 Carta estelar (hoja HR_COL_v1): recolectables.
  VEG-09_seto  Seto de cayena (hoja HR_VEG_v1, VEG-09): arbusto ligero de unos 100 triangulos para MultiMesh, en
          dos nodos: VEG-09_seto_roja y VEG-09_seto_magenta. Da la masa verde del borde de la plaza (v2.1).

Solo colores de la paleta maestra y sus mezclas. El cian queda para la tecnologia: aqui no se usa (el
destello de los recolectables es FX-01, ya hecho).

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/ciudad_vida.py [FAU-12 URB-13 ...]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, Escena, Malla, fibonacci, flor, hoja, mezclar, solido_facetado, tubo  # noqa: E402
from ciudad_base import (BARRO, FLOR_AMARILLA, FRENTE, HIERRO, HOJA_CLARA, HOJA_OSC, MADERA, MADERA_SOL,  # noqa: E402
                         SALIDA, TELA_CREMA, TIERRA, VIDRIO, barra, caja, cilindro, cono, enredadera, extruir,
                         panel, planta_suelta, poligono, t3, tejado, tono)

GENERADOR = "herramientas/mallas/ciudad_vida.py"

# ---------- tonos ----------
BUGANVILLA = mezclar(PAL["coral"], PAL["piedra_clara"], 0.30)       # el magenta no esta en la paleta: coral enfriado
CAYENA = mezclar(PAL["coral"], PAL["terracota"], 0.20)
TOLDO_CORAL = mezclar(PAL["coral"], PAL["sol"], 0.20)
TURQUESA = mezclar(PAL["cian_medio"], PAL["petroleo"], 0.35)          # pintura de la madera (no es el cian de datos)
MENTA = mezclar(mezclar(PAL["cian_medio"], PAL["hierba_sol"], 0.45), PAL["crema"], 0.40)
PAPEL = mezclar(PAL["crema"], PAL["brillo"], 0.30)
PLUMA = t3(mezclar(PAL["piedra"], PAL["piedra_clara"], 0.35), 0.30, 0.22)   # gris malva de la paloma


def esfera(m, centro, r, tn, rng, n=12, escala=(1.0, 1.0, 1.0), var=0.05):
    """Fruta, coco o cabeza: casco facetado pintado con degradado vertical."""
    pts = fibonacci(n) * rng.uniform(0.9, 1.08, (n, 1)) * r * np.array(escala) + np.asarray(centro, float)
    m.anexar(solido_facetado("x", pts, tn[0], tn[1], tn[2], rng, var=var))


def guardar_nodos(archivo, nodos):
    """nodos: [(nombre, [mallas], traslacion, padre)] con padre = indice en la lista o None."""
    e = Escena(GENERADOR)
    idx = []
    total = 0
    for nombre, mallas, t, padre in nodos:
        mallas = [x for x in mallas if len(x)]
        malla = e.malla(*mallas, nombre=nombre) if mallas else None
        total += sum(len(x) for x in mallas)
        idx.append(e.nodo(nombre, malla, t=t, padre=None if padre is None else idx[padre]))
    ruta = e.guardar(SALIDA / f"{archivo}.glb")
    print(f"{archivo}: {total} triangulos -> {ruta.name}")
    return total


# ---------- FAU-12 paloma ----------

def paloma():
    rng = np.random.default_rng(1201)
    c = Malla("FAU-12_cuerpo")
    # cuerpo: ovoide de pecho alto (frente hacia +Z)
    pts = []
    for z, r, y in ((0.10, 0.055, 0.135), (0.05, 0.075, 0.125), (-0.01, 0.07, 0.115), (-0.07, 0.05, 0.11), (-0.12, 0.025, 0.115)):
        for k in range(7):
            a = 2 * math.pi * k / 7
            pts.append((math.cos(a) * r, y + math.sin(a) * r * 0.85, z))
    cuerpo = solido_facetado("x", np.array(pts), PLUMA[0], PLUMA[1], PLUMA[2], rng)
    c.anexar(cuerpo)
    # cuello tornasol y cabeza
    cuello = tono(mezclar(PAL["petroleo"], PAL["hierba_sombra"], 0.35), mezclar(PAL["petroleo"], PAL["hierba_sol"], 0.30),
                  mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.45))
    esfera(c, (0.0, 0.175, 0.105), 0.045, cuello, rng, n=10)
    esfera(c, (0.0, 0.215, 0.125), 0.036, PLUMA, rng, n=10)
    # pico y ojos
    pico = [np.array(p) for p in ((-0.012, 0.212, 0.152), (0.012, 0.212, 0.152), (0.0, 0.205, 0.182), (0.0, 0.222, 0.152))]
    for a, b, d in ((0, 1, 2), (1, 3, 2), (3, 0, 2)):
        c.tri(pico[a], pico[b], pico[d], mezclar(PAL["piedra_osc"], PAL["tierra1"], 0.4))
    for s in (-1, 1):
        o = np.array([s * 0.033, 0.222, 0.135])
        poligono(c, [o + [0, -0.008, -0.008], o + [0, -0.008, 0.008], o + [0, 0.008, 0.008], o + [0, 0.008, -0.008]],
                 [mezclar(PAL["sol"], PAL["coral"], 0.4)] * 4, (s, 0, 0))
    # cola en abanico con banda oscura
    cola = [np.array(p) for p in ((-0.03, 0.12, -0.10), (0.03, 0.12, -0.10), (0.05, 0.11, -0.20), (-0.05, 0.11, -0.20))]
    oscura = mezclar(PAL["piedra_osc"], PAL["petroleo"], 0.4)
    c.quad(cola[0], cola[3], cola[2], cola[1], PLUMA[1], oscura, oscura, PLUMA[1])
    c.quad(cola[0], cola[1], cola[2], cola[3], PLUMA[0], PLUMA[0], oscura, oscura)
    # patas rosadas
    pata = tono(mezclar(PAL["coral"], PAL["madera1"], 0.4), mezclar(PAL["coral"], PAL["tierra1"], 0.4), PAL["tierra1"])
    for s in (-1, 1):
        caja(c, s * 0.02 - 0.008, s * 0.02 + 0.008, 0.0, 0.07, 0.0, 0.016, pata, rng, techo=None)
        caja(c, s * 0.02 - 0.012, s * 0.02 + 0.012, 0.0, 0.006, -0.005, 0.04, pata, rng)
    # alas: abiertas a lo largo de +X (derecha) y -X; el nodo va en el hombro
    alas = []
    for s, nombre in ((1, "FAU-12_ala_d"), (-1, "FAU-12_ala_i")):
        a = Malla(nombre)
        p0, p1 = np.array([0.0, 0.0, 0.05]), np.array([0.0, 0.0, -0.06])
        p2, p3 = np.array([s * 0.24, -0.01, -0.09]), np.array([s * 0.20, 0.0, 0.03])
        banda = mezclar(PAL["piedra_osc"], PAL["piedra"], 0.35)
        clara = mezclar(PAL["piedra_clara"], PAL["piedra"], 0.30)
        q = [p0, p3, p2, p1] if s > 0 else [p0, p1, p2, p3]
        cols = [clara, PLUMA[1], banda, PLUMA[2]] if s > 0 else [clara, PLUMA[2], banda, PLUMA[1]]
        a.quad(*q, *cols)
        a.quad(*q[::-1], *cols[::-1])    # cara de abajo
        alas.append((nombre, a))
    return guardar_nodos("FAU-12", [("FAU-12", [], (0, 0, 0), None), ("FAU-12_cuerpo", [c], (0, 0, 0), 0),
                                    (alas[0][0], [alas[0][1]], (0.05, 0.15, 0.02), 0),
                                    (alas[1][0], [alas[1][1]], (-0.05, 0.15, 0.02), 0)])


# ---------- URB-13 puesto de frutas ----------

def platanos(m, base, rng, n=6):
    base = np.asarray(base, float)
    tn = tono(mezclar(PAL["dorado"], PAL["hierba_sol"], 0.45), mezclar(PAL["dorado"], PAL["crema"], 0.15),
              mezclar(PAL["crema"], PAL["dorado"], 0.4))
    for k in range(n):
        a = 2 * math.pi * k / n
        d = np.array([math.cos(a) * 0.6, -1.0, math.sin(a) * 0.6])
        p0 = base + d * 0.02
        pts = [p0, p0 + d * 0.06 + [0, 0.0, 0], p0 + d * 0.11 + np.array([math.cos(a), 0.6, math.sin(a)]) * 0.03,
               p0 + d * 0.14 + np.array([math.cos(a), 1.4, math.sin(a)]) * 0.04]
        tubo(m, pts, [0.016, 0.022, 0.02, 0.008], 4, tn[0], tn[2], rng, ruido=0.0)


def puesto_frutas():
    rng = np.random.default_rng(1301)
    m = Malla("URB-13_puesto")
    f = Malla("URB-13_plantas", "Follaje")
    pintura = t3(TURQUESA, 0.25, 0.25)
    # mesa: frente de tablas pintadas turquesa y crema, tablero de madera
    for k in range(7):
        x0 = -0.95 + k * 0.27
        tn = pintura if k % 2 == 0 else t3(mezclar(PAL["crema"], PAL["tierra1"], 0.2), 0.25, 0.15)
        caja(m, x0, x0 + 0.265, 0.0, 0.68, 0.15, 0.42, tn, rng, techo=None)
    caja(m, -1.0, 0.95, 0.68, 0.74, -0.45, 0.47, MADERA_SOL, rng, techo=mezclar(PAL["tierra1"], PAL["sol"], 0.3))
    caja(m, -1.0, 0.95, 0.0, 0.68, -0.45, -0.40, MADERA, rng)
    # gradas de exposicion inclinadas hacia la camara (atras, mas altas)
    for k, (y, z) in enumerate(((0.74, 0.18), (0.86, -0.12), (0.98, -0.38))):
        caja(m, -0.98, 0.93, y, y + 0.05, z - 0.14, z + 0.14, MADERA_SOL, rng)
    # cajones de fruta: (x, fila, color, forma)
    frutas = [
        (-0.70, 0, mezclar(PAL["sol"], PAL["coral"], 0.35), "mango"), (-0.22, 0, PAL["sol"], "naranja"),
        (0.26, 0, mezclar(PAL["coral"], PAL["piedra_clara"], 0.25), "pitahaya"), (0.70, 0, mezclar(PAL["dorado"], PAL["hierba_sol"], 0.30), "maracuya"),
        (-0.55, 1, mezclar(PAL["sol"], PAL["dorado"], 0.4), "papaya"), (0.05, 1, PAL["coral"], "sandia"),
        (0.62, 1, mezclar(PAL["hierba_sol"], PAL["dorado"], 0.45), "limon"),
        (-0.40, 2, mezclar(PAL["dorado"], PAL["sol"], 0.3), "pina"), (0.40, 2, mezclar(PAL["sol"], PAL["coral"], 0.15), "mango"),
    ]
    filas = ((0.79, 0.18), (0.91, -0.12), (1.03, -0.38))
    for x, fila, col, forma in frutas:
        y, z = filas[fila]
        w = 0.21 if fila < 2 else 0.30
        caja(m, x - w, x + w, y, y + 0.09, z - 0.12, z + 0.12, MADERA_SOL, rng, techo=TIERRA)
        tn = tono(mezclar(col, PAL["petroleo"], 0.30), col, mezclar(col, PAL["crema"], 0.40))
        if forma == "pina":
            for dx in (-0.12, 0.0, 0.12):
                cilindro(m, x + dx, z, 0.055, 0.045, y + 0.08, y + 0.24, 6, tn, rng)
                planta_suelta(f, (x + dx, y + 0.24, z), rng, alto=0.13, hojas=6, abierta=0.5)
        elif forma == "sandia":
            for dx in (-0.1, 0.1):   # tajadas: roja con corteza verde
                cen = np.array([x + dx, y + 0.09, z + 0.02])
                pts = [cen + np.array([math.cos(a) * 0.09, math.sin(a) * 0.09 + 0.0, 0.0]) for a in np.linspace(0, math.pi, 6)]
                poligono(m, [cen] + pts, [mezclar(PAL["coral"], PAL["crema"], 0.2)] + [mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.2)] * 6, FRENTE)
                for p in pts[1:-1]:
                    poligono(m, [p + [0, 0, 0.005], p + [0.006, 0.006, 0.006], p + [-0.006, 0.006, 0.006]], [PAL["oscuro"]] * 3, FRENTE)
        else:
            r = {"mango": 0.05, "naranja": 0.045, "pitahaya": 0.05, "maracuya": 0.042, "papaya": 0.065, "limon": 0.032}[forma]
            n = 5 if fila < 2 else 7
            esc = (1.0, 0.85, 1.25) if forma in ("mango", "papaya", "pitahaya") else (1.0, 1.0, 1.0)
            for i in range(n):
                px = x + (i - (n - 1) / 2) * (2 * w - 0.06) / n
                pz = z + rng.uniform(-0.06, 0.06)
                esfera(m, (px, y + 0.09 + r * 0.8, pz), r, tn, rng, n=10, escala=esc)
                if forma == "pitahaya":
                    for a in range(3):
                        ang = a * 2.1 + rng.uniform(0, 0.5)
                        hoja(f, np.array([px, y + 0.09 + r * 1.2, pz]), np.array([math.cos(ang), 0.8, math.sin(ang)]),
                             np.array([0, 1.0, 0.3]), 0.05, 0.025, mezclar(PAL["hierba_sol"], PAL["hierba_sombra"], 0.5), HOJA_CLARA)
            if forma == "mango":   # un mango partido en flor, sobre el cajon
                esfera(m, (x, y + 0.09 + r * 2.2, z + 0.02), r * 0.8, tono(PAL["sol"], mezclar(PAL["sol"], PAL["crema"], 0.3), PAL["crema"]), rng, n=8)
    # postes, toldo a rayas coral y crema con flecos (follaje: se mueven con el viento)
    for sx in (-1, 1):
        caja(m, sx * 1.0 - 0.035, sx * 1.0 + 0.035, 0.0, 1.95, 0.40, 0.47, pintura, rng)
        caja(m, sx * 1.0 - 0.035, sx * 1.0 + 0.035, 0.0, 2.15, -0.48, -0.41, pintura, rng)
    n = 9
    for k in range(n):
        x0, x1 = -1.15 + k * 2.3 / n, -1.15 + (k + 1) * 2.3 / n
        col = (TOLDO_CORAL if k % 2 == 0 else TELA_CREMA) * (1 + rng.normal(0, 0.03))
        poligono(m, [(x0, 1.86, 0.78), (x1, 1.86, 0.78), (x1, 2.2, -0.6), (x0, 2.2, -0.6)],
                 [col * 0.9, col * 0.9, mezclar(col, PAL["crema"], 0.15), mezclar(col, PAL["crema"], 0.15)], (0, 1, 0.3))
        poligono(f, [(x0, 1.86, 0.785), ((x0 + x1) / 2, 1.70, 0.79), (x1, 1.86, 0.785)], [col * 0.85] * 3, FRENTE)
    caja(m, -1.17, 1.17, 2.15, 2.21, -0.64, -0.56, MADERA_SOL, rng)
    # platanos colgados del travesano
    for x in (-0.75, 0.55):
        barra(m, [(x, 2.16, -0.1), (x, 1.85, -0.1)], 0.008, tono(PAL["tierra2"], PAL["tierra2"], PAL["tierra1"]), rng, lados=3)
        platanos(m, (x, 1.85, -0.1), rng, n=7)
    # la lata de la confianza (petroleo, con una ranura) y la pizarra con un mango dibujado
    cilindro(m, 0.82, 0.30, 0.06, 0.06, 0.74, 0.88, 7, t3(PAL["petroleo"], 0.25, 0.3), rng)
    caja(m, 0.80, 0.84, 0.879, 0.884, 0.26, 0.34, tono(PAL["oscuro"], PAL["oscuro"], PAL["oscuro"]), rng)
    caja(m, -1.05, -0.55, 0.0, 0.05, 0.62, 0.66, MADERA, rng)
    for sx in (-1.0, -0.6):
        caja(m, sx - 0.02, sx + 0.02, 0.0, 0.62, 0.60, 0.64, MADERA, rng)
    caja(m, -1.07, -0.53, 0.30, 0.66, 0.64, 0.67, MADERA_SOL, rng)
    panel(m, -1.04, -0.56, 0.33, 0.63, 0.672, VIDRIO * 0.9, VIDRIO, rng)
    mango = [(-0.86, 0.40), (-0.74, 0.39), (-0.68, 0.47), (-0.72, 0.56), (-0.85, 0.55), (-0.9, 0.47)]
    extruir(m, mango, 0.672, 0.676, t3(mezclar(PAL["sol"], PAL["coral"], 0.3), 0.0, 0.3), rng, cantos=False)
    extruir(m, [(-0.79, 0.555), (-0.77, 0.555), (-0.74, 0.61), (-0.76, 0.61)], 0.672, 0.677, t3(PAL["hierba_sol"], 0, 0.2), rng, cantos=False)
    # una cayena en lata junto al poste
    cilindro(m, 1.12, 0.36, 0.09, 0.11, 0.0, 0.2, 7, t3(PAL["petroleo"], 0.2, 0.3), rng, techo=TIERRA)
    planta_suelta(f, (1.12, 0.2, 0.36), rng, alto=0.38, hojas=9, flores=4, col_flor=CAYENA)
    return guardar_nodos("URB-13", [("URB-13_puesto", [m, f], (0, 0, 0), None)])


# ---------- URB-14 tablon de anuncios ----------

def tablon():
    rng = np.random.default_rng(1401)
    m = Malla("URB-14_tablon")
    f = Malla("URB-14_plantas", "Follaje")
    W, Y0, Y1 = 0.78, 0.55, 1.55
    pintura = t3(mezclar(PAL["petroleo"], PAL["hierba_sombra"], 0.25), 0.25, 0.22)
    for sx in (-1, 1):
        caja(m, sx * (W + 0.05) - 0.05, sx * (W + 0.05) + 0.05, 0.0, 1.95, -0.06, 0.06, pintura, rng)
        caja(m, sx * (W + 0.05) - 0.09, sx * (W + 0.05) + 0.09, 0.0, 0.10, -0.1, 0.1, t3(PAL["piedra"], 0.3, 0.3), rng)
    # marco y corcho
    caja(m, -W - 0.06, W + 0.06, Y0 - 0.06, Y1 + 0.06, -0.05, 0.03, MADERA_SOL, rng)
    corcho = tono(mezclar(PAL["tierra2"], PAL["madera1"], 0.3), mezclar(PAL["tierra2"], PAL["tierra1"], 0.45), mezclar(PAL["tierra1"], PAL["sol"], 0.25))
    panel(m, -W, W, Y0, Y1, 0.034, corcho[1], corcho[2], rng)
    # tejadillo de tejas
    tejado(m, (-W - 0.2, 1.95, 0.28), (W + 0.2, 1.95, 0.28), (W + 0.2, 2.12, -0.12), (-W - 0.2, 2.12, -0.12), rng, paso=0.2, ancho=0.18)
    tejado(m, (W + 0.2, 2.02, -0.22), (-W - 0.2, 2.02, -0.22), (-W - 0.2, 2.12, -0.12), (W + 0.2, 2.12, -0.12), rng, paso=0.2, ancho=0.18)
    caja(m, -W - 0.1, W + 0.1, 1.86, 1.95, -0.08, 0.08, MADERA, rng)

    def hoja_papel(x0, y0, w, h, col, z=0.04, giro=0.0, rayas=3):
        cx, cy = x0 + w / 2, y0 + h / 2
        c, s = math.cos(giro), math.sin(giro)

        def P(u, v, dz=0.0):
            return (cx + c * u - s * v, cy + s * u + c * v, z + dz)
        poligono(m, [P(-w / 2, -h / 2), P(w / 2, -h / 2), P(w / 2, h / 2), P(-w / 2, h / 2)],
                 [col * 0.94, col * 0.94, col, col], FRENTE)
        tinta = mezclar(PAL["petroleo"], PAL["piedra_osc"], 0.3)
        for k in range(rayas):
            v = h / 2 - h * (k + 1.2) / (rayas + 1.4)
            u1 = w / 2 - 0.03 - (0.06 if k == rayas - 1 else 0.0)
            poligono(m, [P(-w / 2 + 0.03, v - 0.007, 0.002), P(u1, v - 0.007, 0.002), P(u1, v + 0.007, 0.002), P(-w / 2 + 0.03, v + 0.007, 0.002)],
                     [tinta] * 4, FRENTE)
        chincheta = (PAL["coral"], PAL["dorado"], PAL["petroleo"])[int(rng.integers(3))]
        q = P(0, h / 2 - 0.025, 0.004)
        poligono(m, [(q[0] - 0.014, q[1], q[2]), (q[0], q[1] - 0.014, q[2]), (q[0] + 0.014, q[1], q[2]), (q[0], q[1] + 0.014, q[2])], [chincheta] * 4, FRENTE)

    # la convocatoria: papel crema grande con un recuadro petroleo y una Luna creciente
    x0, y0, w, h = -0.70, 0.66, 0.62, 0.82
    hoja_papel(x0, y0, w, h, PAPEL, rayas=0)
    cielo = mezclar(PAL["petroleo"], PAL["oscuro"], 0.25)
    poligono(m, [(x0 + 0.06, y0 + 0.36, 0.042), (x0 + w - 0.06, y0 + 0.36, 0.042), (x0 + w - 0.06, y0 + h - 0.08, 0.042), (x0 + 0.06, y0 + h - 0.08, 0.042)],
             [cielo] * 4, FRENTE)
    cx, cy, r = x0 + w / 2, y0 + 0.58, 0.14
    luna = mezclar(PAL["crema"], PAL["brillo"], 0.3)
    for i in range(8):   # creciente: borde externo en arco y terminador eliptico
        a0, a1 = -math.pi / 2 + math.pi * i / 8, -math.pi / 2 + math.pi * (i + 1) / 8
        e0, e1 = math.cos(a0) * r, math.cos(a1) * r
        # «la Luna sonriente»: el borde iluminado apunta hacia abajo
        poligono(m, [(cx + math.sin(a0) * r, cy - e0 * 0.45, 0.044), (cx + math.sin(a0) * r, cy - e0, 0.044),
                     (cx + math.sin(a1) * r, cy - e1, 0.044), (cx + math.sin(a1) * r, cy - e1 * 0.45, 0.044)], [luna] * 4, FRENTE)
    for sx, sy in ((-0.18, 0.12), (0.17, 0.16), (-0.12, -0.13), (0.2, -0.1)):
        poligono(m, [(cx + sx - 0.012, cy + sy, 0.044), (cx + sx, cy + sy - 0.012, 0.044), (cx + sx + 0.012, cy + sy, 0.044), (cx + sx, cy + sy + 0.012, 0.044)],
                 [PAL["dorado"]] * 4, FRENTE)
    tinta = mezclar(PAL["petroleo"], PAL["piedra_osc"], 0.3)
    for k in range(4):
        yy = y0 + 0.30 - k * 0.065
        poligono(m, [(x0 + 0.07, yy - 0.008, 0.042), (x0 + w - 0.07 - 0.08 * (k == 3), yy - 0.008, 0.042),
                     (x0 + w - 0.07 - 0.08 * (k == 3), yy + 0.008, 0.042), (x0 + 0.07, yy + 0.008, 0.042)], [tinta] * 4, FRENTE)
    # otros papeles de colores
    hoja_papel(0.0, 1.12, 0.34, 0.36, mezclar(PAL["sol"], PAL["crema"], 0.45), giro=0.05)
    hoja_papel(0.38, 1.05, 0.32, 0.42, MENTA, giro=-0.06, rayas=4)
    hoja_papel(0.02, 0.66, 0.30, 0.40, mezclar(PAL["coral"], PAL["crema"], 0.55), giro=-0.03)
    hoja_papel(0.38, 0.62, 0.34, 0.36, mezclar(PAL["piedra_clara"], PAL["crema"], 0.4), giro=0.04, rayas=2)
    # enredadera en un poste
    enredadera(f, [(-W - 0.05, 0.1, 0.07), (-W - 0.05, 1.2, 0.07), (-W + 0.2, 1.9, 0.1)], rng, densidad=16, ancho=0.1,
               col_flor=BUGANVILLA, flores=0.5)
    return guardar_nodos("URB-14", [("URB-14_tablon", [m, f], (0, 0, 0), None)])


# ---------- URB-15 grupos de macetas ----------

def maceta(m, f, x, z, r, alto, rng, tipo, col=None):
    tn = BARRO if col is None else t3(col, 0.25, 0.25)
    cilindro(m, x, z, r * 0.78, r, 0.0, alto, 8, tn, rng, techo=TIERRA)
    cilindro(m, x, z, r * 1.06, r * 1.06, alto - 0.05, alto + 0.01, 8, tn, rng, techo=None)
    if tipo == "buganvilla":
        planta_suelta(f, (x, alto, z), rng, alto=0.62, hojas=14, flores=0)
        for _ in range(26):
            a, rr = rng.uniform(0, 2 * math.pi), rng.uniform(0.05, 0.36)
            c = np.array([x + math.cos(a) * rr, alto + rng.uniform(0.18, 0.62), z + math.sin(a) * rr])
            col_f = mezclar(BUGANVILLA, PAL["coral"], rng.uniform(0, 0.5))
            flor(f, c, np.array([math.cos(a) * 0.5, 0.8, math.sin(a) * 0.5 + 0.3]), rng.uniform(0.06, 0.09), col_f,
                 mezclar(col_f, PAL["crema"], 0.55), 3, rng)
    elif tipo == "cayena":
        planta_suelta(f, (x, alto, z), rng, alto=0.5, hojas=12, flores=6, col_flor=CAYENA)
    elif tipo == "helecho":
        for i in range(11):
            a = 2 * math.pi * i / 11 + rng.uniform(-0.2, 0.2)
            hoja(f, np.array([x, alto, z]), np.array([math.cos(a) * 0.9, 0.5, math.sin(a) * 0.9]), np.array([0, 1.0, 0.2]),
                 rng.uniform(0.32, 0.42), 0.09, HOJA_OSC, mezclar(PAL["hierba_sol"], HOJA_CLARA, 0.5), doblez=0.4)
    elif tipo == "palmita":
        for i in range(7):
            a = 2 * math.pi * i / 7
            hoja(f, np.array([x, alto + 0.05, z]), np.array([math.cos(a) * 0.5, 1.0, math.sin(a) * 0.5]), np.array([0, 0.4, 1.0]),
                 rng.uniform(0.5, 0.7), 0.13, HOJA_OSC, HOJA_CLARA, doblez=0.3)
    else:
        planta_suelta(f, (x, alto, z), rng, alto=0.32, hojas=8, flores=5, col_flor=FLOR_AMARILLA)


def macetas():
    rng = np.random.default_rng(1501)
    a_m, a_f = Malla("URB-15_a"), Malla("URB-15_a_plantas", "Follaje")
    maceta(a_m, a_f, -0.25, -0.05, 0.22, 0.42, rng, "buganvilla")
    maceta(a_m, a_f, 0.28, 0.02, 0.17, 0.32, rng, "cayena", col=TURQUESA)
    maceta(a_m, a_f, 0.05, 0.30, 0.12, 0.22, rng, "helecho")
    b_m, b_f = Malla("URB-15_b"), Malla("URB-15_b_plantas", "Follaje")
    maceta(b_m, b_f, 0.0, 0.0, 0.2, 0.40, rng, "palmita", col=mezclar(PAL["crema"], PAL["tierra1"], 0.3))
    maceta(b_m, b_f, 0.34, 0.16, 0.13, 0.24, rng, "flores")
    maceta(b_m, b_f, -0.30, 0.18, 0.13, 0.26, rng, "buganvilla", col=mezclar(PAL["coral"], PAL["sol"], 0.3))
    return guardar_nodos("URB-15", [("URB-15", [], (0, 0, 0), None), ("URB-15_a", [a_m, a_f], (0, 0, 0), 0),
                                    ("URB-15_b", [b_m, b_f], (0, 0, 0), 0)])


# ---------- VEG-04 cocotero ----------

def cocotero():
    rng = np.random.default_rng(404)
    t = Malla("VEG-04_tronco")
    f = Malla("VEG-04_palmas", "Follaje")
    H = 5.0
    centros = []
    for k in range(11):
        s = k / 10
        centros.append(np.array([0.55 * s ** 1.6, H * s, -0.15 * s * s]))
    radios = [0.17 - 0.06 * (k / 10) for k in range(11)]
    oscuro = mezclar(PAL["madera1"], PAL["tierra2"], 0.3)
    claro = mezclar(PAL["tierra1"], PAL["piedra"], 0.35)
    for k in range(10):   # anillos alternos del tronco
        tubo(t, [centros[k], centros[k + 1]], [radios[k] * 1.05, radios[k + 1]], 7, oscuro if k % 2 else claro,
             mezclar(claro, PAL["crema"], 0.2) if k % 2 == 0 else mezclar(oscuro, claro, 0.5), rng, ruido=0.04, tapa=k == 9)
    copa = centros[-1] + np.array([0, 0.05, 0])
    coco = tono(mezclar(PAL["hierba_sombra"], PAL["madera2"], 0.4), mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.3),
                mezclar(PAL["hierba_sol"], PAL["dorado"], 0.3))
    for a in (0.3, 2.2, 4.1, 5.3):
        esfera(t, copa + np.array([math.cos(a) * 0.15, -0.16, math.sin(a) * 0.15]), 0.1, coco, rng, n=9)
    # palmas: nervio que sube y cae en arco, foliolos a cada lado
    for i in range(9):
        a = 2 * math.pi * i / 9 + rng.uniform(-0.15, 0.15)
        d = np.array([math.cos(a), 0.0, math.sin(a)])
        largo = rng.uniform(1.9, 2.4)
        sube = rng.uniform(0.25, 0.6)
        lado = np.cross(np.array([0, 1.0, 0]), d)
        pts = []
        for k in range(8):
            s = k / 7
            pts.append(copa + d * largo * s + np.array([0, sube * math.sin(s * 2.4) - 1.25 * s * s, 0]))
        for k in range(1, 8):
            p, q = pts[k - 1], pts[k]
            eje = (q - p) / np.linalg.norm(q - p)
            s = k / 7
            col_b = mezclar(HOJA_OSC, PAL["hierba_sombra"], 0.3)
            col_p = mezclar(PAL["hierba_sol"], HOJA_CLARA, s)
            for sgn in (-1, 1):
                dirf = lado * sgn * 0.9 + eje * 0.45 + np.array([0, -0.35, 0])
                hoja(f, (p + q) / 2, dirf, np.array([0, 1.0, 0]) + eje * -0.2, 0.5 * (1.05 - 0.55 * s), 0.11, col_b, col_p, doblez=0.2)
        barra(t, pts, 0.02, tono(PAL["hierba_sombra"], mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.5), PAL["hierba_sol"]), rng, lados=3, tapa=False)
    return guardar_nodos("VEG-04", [("VEG-04", [t, f], (0, 0, 0), None)])


# ---------- VEG-09 seto de cayena (masa de vegetacion de la plaza, v2.1) ----------

def _mata(nombre, col_flor, semilla, flores=11):
    """Arbusto ligero (unos 100 triangulos) para MultiMesh: tres copas facetadas de hoja y flores de 3 petalos.
    Mide unos 1,0 m de ancho y 0,8 m de alto; origen en el centro de la base."""
    rng = np.random.default_rng(semilla)
    f = Malla(nombre, "Follaje")
    sombra = mezclar(HOJA_OSC, PAL["petroleo"], 0.30)
    base = mezclar(PAL["hierba_sombra"], HOJA_CLARA, 0.35)
    luz = mezclar(HOJA_CLARA, PAL["hierba_sol"], 0.35)
    copas = []
    for cx, cz, r, h in ((-0.22, 0.04, 0.36, 0.62), (0.2, -0.06, 0.34, 0.74), (0.02, 0.18, 0.30, 0.52)):
        pts = fibonacci(9) * rng.uniform(0.85, 1.12, (9, 1)) * np.array([r, h * 0.5, r])
        pts[:, 1] = np.maximum(pts[:, 1], -h * 0.32)
        pts += np.array([cx, h * 0.5 - 0.02, cz])
        pts[:, 1] = np.maximum(pts[:, 1], 0.0)
        f.anexar(solido_facetado("copa", pts, sombra, base, luz, rng, var=0.05, material="Follaje"))
        copas.append((cx, cz, r, h))
    for k in range(flores):
        cx, cz, r, h = copas[k % 3]
        a = rng.uniform(0, 2 * math.pi)
        u = rng.uniform(0.35, 0.85)
        p = np.array([cx + math.cos(a) * r * 0.75 * (1.0 - u * 0.4), h * (0.45 + 0.55 * u), cz + math.sin(a) * r * 0.75 * (1.0 - u * 0.4)])
        n = np.array([math.cos(a) * 0.6, 0.9, math.sin(a) * 0.6 + 0.35])
        col = mezclar(col_flor, PAL["crema"], rng.uniform(0.0, 0.18))
        flor(f, p + n / np.linalg.norm(n) * 0.03, n, rng.uniform(0.07, 0.1), col, mezclar(col, PAL["dorado"], 0.5), 3, rng)
    return f


def seto():
    roja = _mata("VEG-09_seto_roja", CAYENA, 901)
    magenta = _mata("VEG-09_seto_magenta", BUGANVILLA, 902, flores=13)
    return guardar_nodos("VEG-09_seto", [("VEG-09_seto", [], (0, 0, 0), None), ("VEG-09_seto_roja", [roja], (0, 0, 0), 0),
                                         ("VEG-09_seto_magenta", [magenta], (0, 0, 0), 0)])


# ---------- recolectables COL ----------

def placa():
    rng = np.random.default_rng(303)
    m = Malla("COL-03_placa")
    verde = tono(mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.55), mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.3),
                 mezclar(PAL["hierba_sol"], PAL["petroleo"], 0.25))
    caja(m, -0.13, 0.13, 0.0, 0.016, -0.09, 0.09, verde, rng, techo=verde[2])
    cobre = mezclar(PAL["sol"], PAL["terracota"], 0.3)
    for k in range(5):
        z = -0.07 + k * 0.035
        poligono(m, [(-0.11, 0.017, z - 0.004), (-0.11, 0.017, z + 0.004), (0.10, 0.017, z + 0.004), (0.10, 0.017, z - 0.004)], [cobre] * 4, (0, 1, 0))
    chip = tono(PAL["oscuro"], PAL["piedra_osc"], mezclar(PAL["piedra_osc"], PAL["piedra_clara"], 0.3))
    for x, z, w, d in ((-0.05, -0.02, 0.05, 0.035), (0.05, 0.03, 0.035, 0.025), (0.06, -0.05, 0.025, 0.02)):
        caja(m, x - w, x + w, 0.016, 0.03, z - d, z + d, chip, rng)
    cilindro(m, -0.08, 0.05, 0.016, 0.016, 0.016, 0.06, 6, t3(PAL["dorado"], 0.3, 0.3), rng)
    cilindro(m, 0.0, 0.06, 0.012, 0.012, 0.016, 0.05, 6, t3(PAL["coral"], 0.3, 0.3), rng)
    return guardar_nodos("COL-03", [("COL-03", [m], (0, 0, 0), None)])


def cable():
    rng = np.random.default_rng(306)
    m = Malla("COL-06_cable")
    cobre = tono(mezclar(PAL["terracota"], PAL["madera2"], 0.2), mezclar(PAL["sol"], PAL["terracota"], 0.35), mezclar(PAL["sol"], PAL["crema"], 0.4))
    for vuelta in range(3):
        r = 0.11 - vuelta * 0.012
        pts = [np.array([math.cos(a) * r, 0.025 + vuelta * 0.02, math.sin(a) * r * 0.9]) for a in np.linspace(0, 2 * math.pi, 13)]
        tubo(m, pts, [0.014] * 13, 5, cobre[1], cobre[2], rng, ruido=0.0, tapa=False)
    suelto = [np.array(p) for p in ((0.1, 0.03, 0.0), (0.18, 0.015, 0.05), (0.24, 0.012, 0.02), (0.29, 0.02, -0.04))]
    tubo(m, suelto, [0.012] * 4, 5, cobre[1], cobre[2], rng, ruido=0.0)
    return guardar_nodos("COL-06", [("COL-06", [m], (0, 0, 0), None)])


def carta():
    rng = np.random.default_rng(312)
    m = Malla("COL-12_carta")
    papel = PAPEL
    sombra = mezclar(PAPEL, PAL["petroleo"], 0.18)
    # dos paneles doblados como un libro abierto sobre el suelo
    for s in (-1, 1):
        a, b = (0.0, 0.01, -0.12), (0.0, 0.01, 0.12)
        c, d = (s * 0.17, 0.05, 0.12), (s * 0.17, 0.05, -0.12)
        cols = [sombra, sombra, papel, papel]
        poligono(m, [a, b, c, d], cols, (0, 1, 0))
        poligono(m, [a, d, c, b], [mezclar(papel, PAL["tierra1"], 0.3)] * 4, (0, -1, 0))
        tinta = mezclar(PAL["petroleo"], PAL["oscuro"], 0.2)
        estrellas = [(0.05, -0.07), (0.1, 0.02), (0.13, -0.04), (0.07, 0.08), (0.12, 0.09)]
        prev = None
        for u, v in estrellas:
            x, y, z = s * u, 0.01 + 0.04 * u / 0.17 + 0.003, v
            poligono(m, [(x - 0.008, y, z), (x, y, z + 0.008), (x + 0.008, y, z), (x, y, z - 0.008)], [tinta] * 4, (0, 1, 0))
            if prev is not None and s > 0:
                px, py, pz = prev
                dx, dz = z - pz, -(x - px)
                n = math.hypot(dx, dz) or 1.0
                dx, dz = dx / n * 0.003, dz / n * 0.003
                poligono(m, [(px - dx, py, pz - dz), (x - dx, y, z - dz), (x + dx, y, z + dz), (px + dx, py, pz + dz)], [tinta] * 4, (0, 1, 0))
            prev = (x, y, z)
    return guardar_nodos("COL-12", [("COL-12", [m], (0, 0, 0), None)])


RECURSOS = {"FAU-12": paloma, "URB-13": puesto_frutas, "URB-14": tablon, "URB-15": macetas, "VEG-04": cocotero,
            "COL-03": placa, "COL-06": cable, "COL-12": carta, "VEG-09_seto": seto}


def main():
    pedidos = sys.argv[1:] or list(RECURSOS)
    total = sum(RECURSOS[r]() for r in pedidos)
    print(f"TOTAL {total} triangulos en {len(pedidos)} recursos")


if __name__ == "__main__":
    main()
