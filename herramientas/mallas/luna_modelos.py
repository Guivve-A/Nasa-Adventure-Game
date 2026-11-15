"""Modelos de la Luna del sueno (zona «luna» del juego jugable v0), hechos por script.

NO hay hoja de referencia ni concepto validado de la Luna (el lote 06 esta por aprobar): todo esto es
PROVISIONAL. Familia nueva del catalogo: LUN. Recursos que escribe en juego/modelos/luna/<ID>.glb
(origen en el centro de la base, y = 0):
  LUN-05  baliza cian (tripode, panel y lampara)     LUN-05_estaca  estaca de ruta con punta cian
  LUN-06  bandera de Estados Unidos                   LUN-07  bandera de Ecuador (escudo simplificado)
          las dos de 0,91 x 1,52 m, mastil de 2,44 m (0,20 m hincados) y barra horizontal; la tela cuelga
          hacia +X y mira a +Z; pliegues modelados (no hay viento). El borde bajo queda a 1,31 m del suelo
  LUN-08  caja de herramientas: cucharon de caja, pinzas, tubo de nucleo y martillo
  LUN-09  casco de burbuja (radio 0,27 m; centro en el origen). Material «Casco» = la burbuja
          (la zona le pone su shader transparente); el aro del cuello es «Facetado»
LUN-01 es el terreno de regolito con crateres: lo genera la zona en el motor (juego/zonas/luna/terreno.gd).

LUN-02 (rocas), LUN-03 (etapa de descenso), LUN-04 (caja-capsula) y LUN-10 a LUN-19 viven en
herramientas/mallas/luna_recursos_v2.py, que importa de aqui las piezas (poli, bloque, barra, torno, disco,
octaedro, guardar) y los tonos. Las versiones v1 de LUN-02, 03 y 04 que habia en este archivo se quitaron.

Sin logotipos ni textos. Solo colores de la paleta maestra y sus mezclas.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/luna_modelos.py          (LUN-05, LUN-05_estaca y LUN-06 a LUN-09)
    python -I herramientas/mallas/luna_recursos_v2.py      (LUN-02, 03, 04 y LUN-10 a LUN-19)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, RAIZ, Escena, Malla, marco, mezclar, rot_y  # noqa: E402

SALIDA = RAIZ / "juego" / "modelos" / "luna"
RESUMEN: dict[str, int] = {}

# ---------- tonos ----------
SOMBRA = mezclar(PAL["petroleo"], PAL["oscuro"], 0.35)          # sombra azul profunda
LUZ = mezclar(PAL["piedra_clara"], PAL["brillo"], 0.30)
BLANCO = mezclar(PAL["crema"], PAL["brillo"], 0.55)             # el blanco del proyecto (como en la habitacion)
METAL = mezclar(PAL["piedra_clara"], PAL["petroleo"], 0.18)
METAL_OSC = mezclar(PAL["piedra_osc"], PAL["petroleo"], 0.30)
ORO = mezclar(PAL["dorado"], PAL["sol"], 0.35)
ORO_OSC = mezclar(PAL["dorado"], PAL["terracota"], 0.45)
# v2d: el carton salia salmon bajo la luz lavanda de la Tierra; ahora ocre, como la caja de carga_luna.jpg
CARTON = mezclar(mezclar(PAL["tierra2"], PAL["sol"], 0.38), PAL["dorado"], 0.12)
CARTON_OSC = mezclar(PAL["tierra2"], PAL["madera2"], 0.45)
ROJO = mezclar(PAL["coral"], PAL["terracota"], 0.42)
AZUL = mezclar(PAL["petroleo"], PAL["oscuro"], 0.30)
AZUL_EC = mezclar(PAL["petroleo"], PAL["cian_medio"], 0.12) * 0.86
AMARILLO = mezclar(PAL["dorado"], PAL["crema"], 0.12)
GRIS_ROCA = mezclar(PAL["piedra"], PAL["piedra_clara"], 0.45)


def jit(c, rng, s=0.04):
    return np.clip(np.asarray(c, float) * (1 + rng.normal(0, s)), 0, 1)


# ---------- piezas ----------

def poli(m: Malla, pts, col=None, interior=None, cols=None, hacia=None):
    """Poligono convexo en abanico. Se orienta lejos de «interior» o hacia el vector «hacia»."""
    pts = [np.asarray(p, float) for p in pts]
    n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    cen = np.mean(pts, axis=0)
    girar = False
    if interior is not None and n @ (cen - np.asarray(interior, float)) < 0:
        girar = True
    if hacia is not None and n @ np.asarray(hacia, float) < 0:
        girar = True
    idx = list(range(len(pts)))
    if girar:
        idx.reverse()
    if cols is None:
        cols = [col] * len(pts)
    for i in range(1, len(pts) - 1):
        a, b, c = idx[0], idx[i], idx[i + 1]
        m.tri(pts[a], pts[b], pts[c], cols[a], cols[b], cols[c])


def bloque(m: Malla, c, tam, col, R=None, sombra=0.30, luz=0.12, tapa=None, base=True):
    """Caja centrada en c, con degradado vertical (sombra azul abajo, luz arriba)."""
    c = np.asarray(c, float)
    h = np.asarray(tam, float) / 2
    R = np.eye(3) if R is None else np.asarray(R, float)
    bajo, alto = mezclar(col, SOMBRA, sombra), mezclar(col, LUZ, luz)
    P = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                P[(sx, sy, sz)] = c + R @ (np.array([sx, sy, sz]) * h)
    caras = [[(-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1)], [(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)],
             [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)], [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]]
    for q in caras:
        poli(m, [P[k] for k in q], interior=c, cols=[bajo if k[1] < 0 else alto for k in q])
    poli(m, [P[(-1, 1, -1)], P[(1, 1, -1)], P[(1, 1, 1)], P[(-1, 1, 1)]], alto if tapa is None else tapa, interior=c)
    if base:
        poli(m, [P[(-1, -1, -1)], P[(1, -1, -1)], P[(1, -1, 1)], P[(-1, -1, 1)]], bajo, interior=c)


def barra(m: Malla, p0, p1, r0, c0, c1=None, lados=6, r1=None, tapas=True):
    """Cilindro (o tronco de cono) entre dos puntos."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    c1 = c0 if c1 is None else c1
    r1 = r0 if r1 is None else r1
    u, v = marco(p1 - p0)
    ang = np.arange(lados) / lados * 2 * math.pi
    a = [p0 + (math.cos(t) * u + math.sin(t) * v) * r0 for t in ang]
    b = [p1 + (math.cos(t) * u + math.sin(t) * v) * r1 for t in ang]
    eje = (p0 + p1) / 2
    for i in range(lados):
        j = (i + 1) % lados
        poli(m, [a[i], a[j], b[j], b[i]], interior=eje, cols=[c0, c0, c1, c1])
    if tapas:
        if r0 > 1e-5:
            poli(m, a, c0, interior=eje)
        if r1 > 1e-5:
            poli(m, b, c1, interior=eje)


def torno(m: Malla, perfil, lados, centro=(0, 0, 0), giro=0.0, tapa_abajo=True, tapa_arriba=True, rng=None):
    """Solido de revolucion alrededor de Y. perfil = [(radio, y, color), ...] de abajo arriba."""
    centro = np.asarray(centro, float)
    ang = np.arange(lados) / lados * 2 * math.pi + giro
    anillos = [[centro + np.array([math.cos(t) * r, y, math.sin(t) * r]) for t in ang] for r, y, _ in perfil]
    ymed = centro + np.array([0, (perfil[0][1] + perfil[-1][1]) / 2, 0])
    for k in range(len(perfil) - 1):
        for i in range(lados):
            j = (i + 1) % lados
            v = 1.0 if rng is None else 1 + rng.normal(0, 0.05)
            c0, c1 = np.asarray(perfil[k][2]) * v, np.asarray(perfil[k + 1][2]) * v
            eje = centro + np.array([0, (perfil[k][1] + perfil[k + 1][1]) / 2, 0])
            if perfil[k][0] < 1e-5:
                poli(m, [anillos[k][i], anillos[k + 1][j], anillos[k + 1][i]], interior=eje, cols=[c0, c1, c1])
            elif perfil[k + 1][0] < 1e-5:
                poli(m, [anillos[k][i], anillos[k][j], anillos[k + 1][i]], interior=eje, cols=[c0, c0, c1])
            else:
                poli(m, [anillos[k][i], anillos[k][j], anillos[k + 1][j], anillos[k + 1][i]], interior=eje,
                     cols=[c0, c0, c1, c1])
    if tapa_abajo and perfil[0][0] > 1e-5:
        poli(m, anillos[0], perfil[0][2], interior=ymed)
    if tapa_arriba and perfil[-1][0] > 1e-5:
        poli(m, anillos[-1], perfil[-1][2], interior=ymed)


def disco(m: Malla, centro, normal, r, col, lados=8, ry=None):
    centro = np.asarray(centro, float)
    u, v = marco(normal)
    ry = r if ry is None else ry
    pts = [centro + u * math.cos(t) * r + v * math.sin(t) * ry for t in np.arange(lados) / lados * 2 * math.pi]
    poli(m, pts, col, hacia=normal)


def guardar(ident: str, nodos: list, generador: str = "herramientas/mallas/luna_modelos.py", salida=None):
    """nodos = [(nombre, [mallas], (x, y, z)), ...]. «generador» y «salida» los usa luna_recursos_v2.py."""
    e = Escena(generador)
    total = 0
    for nombre, mallas, t in nodos:
        e.nodo(nombre, e.malla(*mallas, nombre=nombre), t=t)
        total += sum(len(m) for m in mallas)
    e.guardar((SALIDA if salida is None else Path(salida)) / f"{ident}.glb")
    RESUMEN[ident] = total


# ---------- LUN-05 baliza y estaca ----------

def octaedro(m: Malla, c, r, col, alto=1.4):
    c = np.asarray(c, float)
    ecu = [c + np.array([math.cos(t) * r, 0, math.sin(t) * r]) for t in np.arange(4) * math.pi / 2 + math.pi / 4]
    for punta in (c + np.array([0, r * alto, 0]), c - np.array([0, r * alto, 0])):
        for i in range(4):
            poli(m, [ecu[i], ecu[(i + 1) % 4], punta], col, interior=c)


def baliza():
    m = Malla("LUN-05_cuerpo")
    luz = Malla("LUN-05_luz", "Emisivo")
    cima = np.array([0, 0.62, 0])
    for k in range(3):
        a = k * 2 * math.pi / 3 + math.pi / 2
        pie = np.array([math.cos(a) * 0.42, 0.0, math.sin(a) * 0.42])
        barra(m, pie, cima, 0.022, METAL_OSC, METAL, lados=4)
        torno(m, [(0.07, 0.0, METAL_OSC), (0.05, 0.03, METAL)], 6, centro=pie)
    barra(m, cima, (0, 1.22, 0), 0.028, METAL, mezclar(METAL, BLANCO, 0.4), lados=6)
    torno(m, [(0.085, 0.60, METAL_OSC), (0.085, 0.70, METAL)], 6)
    # panel solar inclinado hacia +Z
    R = np.array([[1, 0, 0], [0, math.cos(-0.7), -math.sin(-0.7)], [0, math.sin(-0.7), math.cos(-0.7)]])
    bloque(m, (0, 0.92, 0.13), (0.42, 0.26, 0.02), mezclar(PAL["petroleo"], PAL["oscuro"], 0.45), R=R, sombra=0.2, luz=0.25)
    barra(m, (0, 0.90, 0.02), (0, 0.92, 0.12), 0.015, METAL_OSC, lados=4)
    torno(m, [(0.06, 1.22, METAL_OSC), (0.075, 1.25, METAL), (0.06, 1.28, METAL)], 6)
    octaedro(luz, (0, 1.42, 0), 0.095, PAL["cian"])
    torno(luz, [(0.034, 1.02, PAL["cian_medio"]), (0.034, 1.06, PAL["cian"])], 6)
    guardar("LUN-05", [("LUN-05_baliza", [m, luz], (0, 0, 0))])

    e = Malla("LUN-05_estaca_cuerpo")
    le = Malla("LUN-05_estaca_luz", "Emisivo")
    barra(e, (0, -0.05, 0), (0, 0.58, 0), 0.028, METAL_OSC, METAL, lados=5)
    torno(e, [(0.075, 0.0, METAL_OSC), (0.045, 0.05, METAL)], 6)
    torno(le, [(0.036, 0.36, PAL["cian_medio"]), (0.036, 0.42, PAL["cian"])], 5)
    octaedro(le, (0, 0.70, 0), 0.085, PAL["cian"])
    guardar("LUN-05_estaca", [("LUN-05_estaca", [e, le], (0, 0, 0))])


# ---------- LUN-06 y LUN-07 banderas ----------

ANCHO, ALTO = 1.52, 0.91
Y_BARRA = 2.24          # 2,44 m de mastil con 0,20 m hincados
X0 = 0.035


def tela(u, v):
    """Superficie de la tela con pliegues fijos: sujeta arriba por la barra, mas suelta abajo."""
    x = X0 + ANCHO * u * (1.0 - 0.035 * v)
    y = Y_BARRA - 0.015 - ALTO * v
    z = (0.008 + 0.040 * v) * math.sin(2 * math.pi * (2.4 * u + 0.22 * v) + 0.6) + 0.016 * v * math.sin(2 * math.pi * 5.1 * u + 1.3)
    return np.array([x, y, z])


def normal_tela(u, v):
    e = 1e-3
    n = np.cross(tela(u + e, v) - tela(u, v), tela(u, v) - tela(u, v + e))
    return n / np.linalg.norm(n)


def subdividir(tri, maximo=0.05):
    a, b, c = [np.asarray(p, float) for p in tri]
    lados = [np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)]
    if max(lados) <= maximo:
        return [(a, b, c)]
    k = int(np.argmax(lados))
    if k == 0:
        mid = (a + b) / 2
        return subdividir((a, mid, c), maximo) + subdividir((mid, b, c), maximo)
    if k == 1:
        mid = (b + c) / 2
        return subdividir((a, b, mid), maximo) + subdividir((a, mid, c), maximo)
    mid = (a + c) / 2
    return subdividir((a, b, mid), maximo) + subdividir((mid, b, c), maximo)


def sobre_tela(m: Malla, pts2d, col, capa):
    """Poligono convexo en metros respecto del centro de la bandera (+y arriba), pegado a la tela por las dos caras."""
    pts = [np.array([p[0], p[1]], float) for p in pts2d]
    for i in range(1, len(pts) - 1):
        for tri in subdividir((pts[0], pts[i], pts[i + 1])):
            for cara in (1, -1):
                P = []
                for q in tri:
                    u, v = 0.5 + q[0] / ANCHO, 0.5 - q[1] / ALTO
                    P.append(tela(u, v) + normal_tela(u, v) * cara * (0.004 + 0.0018 * capa))
                poli(m, P, col, hacia=(0, 0, cara))


def asta(m: Malla):
    barra(m, (0, -0.20, 0), (0, Y_BARRA + 0.03, 0), 0.022, mezclar(ORO_OSC, METAL_OSC, 0.4), mezclar(ORO, METAL, 0.45), lados=6)
    barra(m, (0, Y_BARRA, 0), (X0 + ANCHO + 0.02, Y_BARRA, 0), 0.013, mezclar(ORO, METAL, 0.45), mezclar(ORO, METAL, 0.6), lados=5)
    torno(m, [(0.03, Y_BARRA + 0.03, ORO_OSC), (0.0, Y_BARRA + 0.07, ORO)], 6, tapa_abajo=False)
    torno(m, [(0.045, -0.0, METAL_OSC), (0.026, 0.05, METAL)], 6, tapa_abajo=False, tapa_arriba=False)


def pano(m: Malla, nu, nv, color_de):
    """Malla de la tela por las dos caras; color_de(i, j) da el color de cada celda."""
    P = [[tela(i / nu, j / nv) for i in range(nu + 1)] for j in range(nv + 1)]
    for j in range(nv):
        for i in range(nu):
            col = np.asarray(color_de(i, j), float) * (1.0 - 0.07 * (j / nv))
            a, b, c, d = P[j][i], P[j][i + 1], P[j + 1][i + 1], P[j + 1][i]
            poli(m, [a, b, c, d], col, hacia=(0, 0, 1))
            poli(m, [a, b, c, d], col * 0.93, hacia=(0, 0, -1))


def estrella(pts_c, r, puntas=5, giro=math.pi / 2):
    cx, cy = pts_c
    borde = []
    for k in range(puntas * 2):
        rr = r if k % 2 == 0 else r * 0.40
        a = giro + k * math.pi / puntas
        borde.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return [[(cx, cy), borde[k], borde[(k + 1) % len(borde)]] for k in range(len(borde))]


def bandera_estados_unidos():
    m = Malla("LUN-06_tela")
    nu, nv = 30, 26                       # 13 franjas de 2 filas; canton de 12 columnas (0,4 del largo) y 14 filas
    blanco = mezclar(BLANCO, PAL["piedra_clara"], 0.15)

    def color(i, j):
        if i < 12 and j < 14:
            return AZUL
        return ROJO if (j // 2) % 2 == 0 else blanco

    pano(m, nu, nv, color)
    # 50 estrellas en 9 filas de 6 y 5
    est = Malla("LUN-06_estrellas")
    cw, ch = 0.4 * ANCHO, ALTO * 7 / 13
    for fila in range(9):
        cuantas = 6 if fila % 2 == 0 else 5
        for k in range(cuantas):
            x = cw * ((2 * k + 1) if cuantas == 6 else (2 * k + 2)) / 12
            y = ch * (fila + 1) / 10
            c = (-ANCHO / 2 + x, ALTO / 2 - y)
            for tri in estrella(c, 0.027):
                sobre_tela(est, tri, blanco, 0)
    a = Malla("LUN-06_asta")
    asta(a)
    guardar("LUN-06", [("LUN-06_bandera_estados_unidos", [m, est, a], (0, 0, 0))])


def elipse(cx, cy, rx, ry, n=14, a0=0.0, a1=2 * math.pi, cerrar=False):
    ts = np.linspace(a0, a1, n, endpoint=cerrar)
    return [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in ts]


def bandera_ecuador():
    m = Malla("LUN-07_tela")
    nu, nv = 30, 24                       # amarillo 12 filas (la mitad), azul 6 y rojo 6

    def color(i, j):
        return AMARILLO if j < 12 else (AZUL_EC if j < 18 else ROJO)

    pano(m, nu, nv, color)
    # escudo simplificado al centro: ovalo con cielo, sol, nevado, rio y suelo verde; condor arriba;
    # banderas y ramas a los lados; base abajo. Sin textos.
    e = Malla("LUN-07_escudo")
    verde = mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.35)
    verde_osc = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.35)
    cielo = mezclar(PAL["petroleo"], PAL["brillo"], 0.62)
    oscuro = mezclar(PAL["piedra_osc"], PAL["oscuro"], 0.55)
    borde = mezclar(PAL["dorado"], PAL["terracota"], 0.50)
    for s in (-1, 1):
        # dos banderas por lado (franjas amarilla, azul y roja) y una rama
        for k, (dx, dy, incl) in enumerate(((0.100, 0.020, 0.55), (0.118, -0.030, 0.25))):
            base = np.array([s * 0.055, -0.075 + 0.02 * k])
            punta = np.array([s * (dx + 0.075), dy + 0.085 + incl * 0.06])
            eje = punta - base
            largo = np.linalg.norm(eje)
            eje /= largo
            nrm = np.array([-eje[1], eje[0]]) * s
            for f, col in enumerate((AMARILLO * 0.92, AZUL_EC, ROJO)):
                o0 = base + eje * largo * 0.45 + nrm * (0.012 * f - 0.006)
                o1 = punta + nrm * (0.012 * f - 0.006)
                sobre_tela(e, [o0, o1, o1 + nrm * 0.012, o0 + nrm * 0.012], col, 0)
            sobre_tela(e, [base - nrm * 0.004, punta + eje * 0.02 - nrm * 0.004, punta + eje * 0.02, base], oscuro, 0)
        for k in range(3):
            a0 = np.array([s * 0.070, -0.090])
            ang = math.radians(200 + 18 * k) if s < 0 else math.radians(-20 - 18 * k)
            p1 = a0 + np.array([math.cos(ang), math.sin(ang)]) * 0.085
            lat = np.array([-math.sin(ang), math.cos(ang)]) * 0.014
            sobre_tela(e, [a0, a0 + (p1 - a0) * 0.5 + lat, p1, a0 + (p1 - a0) * 0.5 - lat], verde if k % 2 == 0 else verde_osc, 1)
    sobre_tela(e, [(-0.034, -0.120), (0.034, -0.120), (0.022, -0.165), (-0.022, -0.165)], mezclar(PAL["terracota"], PAL["madera2"], 0.3), 1)
    sobre_tela(e, elipse(0, 0, 0.100, 0.130, 16), borde, 2)
    sobre_tela(e, elipse(0, 0, 0.086, 0.116, 16), cielo, 3)
    # suelo verde: el segmento bajo del ovalo
    t0 = math.asin(-0.030 / 0.116)
    seg = elipse(0, 0, 0.086, 0.116, 9, math.pi - t0, 2 * math.pi + t0, cerrar=True)
    sobre_tela(e, seg, verde, 4)
    sobre_tela(e, [(-0.004, -0.030), (0.014, -0.030), (0.040, -0.100), (-0.024, -0.108)], mezclar(AZUL_EC, PAL["brillo"], 0.25), 5)
    sobre_tela(e, [(-0.072, -0.030), (-0.012, 0.056), (0.004, -0.030)], BLANCO, 5)
    sobre_tela(e, [(-0.012, 0.056), (0.052, -0.030), (0.004, -0.030)], mezclar(BLANCO, PAL["petroleo"], 0.35), 5)
    sobre_tela(e, elipse(0.0, 0.084, 0.018, 0.018, 8), PAL["dorado"], 5)
    # condor con las alas abiertas
    sobre_tela(e, [(0.0, 0.118), (0.020, 0.142), (0.0, 0.168), (-0.020, 0.142)], oscuro, 6)
    for s in (-1, 1):
        sobre_tela(e, [(s * 0.012, 0.146), (s * 0.030, 0.128), (s * 0.108, 0.150), (s * 0.122, 0.186)], oscuro, 6)
    sobre_tela(e, [(0.004, 0.160), (0.030, 0.174), (0.012, 0.178)], mezclar(BLANCO, PAL["piedra"], 0.3), 7)
    a = Malla("LUN-07_asta")
    asta(a)
    guardar("LUN-07", [("LUN-07_bandera_ecuador", [m, e, a], (0, 0, 0))])


# ---------- LUN-08 caja de herramientas ----------

def herramientas():
    rng = np.random.default_rng(8)
    m = Malla("LUN-08_caja")
    w, h, d = 0.66, 0.26, 0.36
    g = 0.022
    col = mezclar(METAL, BLANCO, 0.25)
    y0 = 0.06
    for sx in (-1, 1):
        for sz in (-1, 1):
            barra(m, (sx * (w / 2 - 0.05), 0, sz * (d / 2 - 0.05)), (sx * (w / 2 - 0.05), y0, sz * (d / 2 - 0.05)), 0.028, METAL_OSC, lados=5)
    bloque(m, (0, y0 + g / 2, 0), (w, g, d), METAL_OSC, sombra=0.2)
    bloque(m, (0, y0 + h / 2, d / 2 - g / 2), (w, h, g), col)
    bloque(m, (0, y0 + h / 2, -d / 2 + g / 2), (w, h, g), col)
    bloque(m, (w / 2 - g / 2, y0 + h / 2, 0), (g, h, d - 2 * g), mezclar(col, METAL_OSC, 0.25))
    bloque(m, (-w / 2 + g / 2, y0 + h / 2, 0), (g, h, d - 2 * g), mezclar(col, METAL_OSC, 0.25))
    bloque(m, (0, y0 + h * 0.62, d / 2 + 0.004), (w * 0.9, 0.05, 0.008), mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.2), sombra=0.1, base=False)
    # asa
    barra(m, (-0.20, y0 + h, 0), (-0.20, y0 + h + 0.16, 0), 0.014, METAL_OSC, METAL, lados=4)
    barra(m, (0.20, y0 + h, 0), (0.20, y0 + h + 0.16, 0), 0.014, METAL_OSC, METAL, lados=4)
    barra(m, (-0.20, y0 + h + 0.16, 0), (0.20, y0 + h + 0.16, 0), 0.018, METAL, mezclar(METAL, BLANCO, 0.4), lados=5)

    t = Malla("LUN-08_herramientas")
    # cucharon de caja: mango y cuchara en forma de caja abierta por delante
    b0 = np.array([-0.21, y0 + 0.04, -0.04])
    b1 = b0 + np.array([-0.10, 0.62, -0.06])
    barra(t, b0, b1, 0.016, METAL_OSC, METAL, lados=5)
    cu = b1 + np.array([-0.02, 0.07, 0.0])
    cc = mezclar(METAL, BLANCO, 0.35)
    bloque(t, cu + np.array([0, -0.045, 0]), (0.16, 0.012, 0.11), cc)
    bloque(t, cu + np.array([0, 0, -0.050]), (0.16, 0.09, 0.012), cc)
    bloque(t, cu + np.array([0.075, 0, 0]), (0.012, 0.09, 0.11), mezclar(cc, METAL_OSC, 0.3))
    bloque(t, cu + np.array([-0.075, 0, 0]), (0.012, 0.09, 0.11), mezclar(cc, METAL_OSC, 0.3))
    # pinzas: dos varillas en V estrecha con un aro en la base
    p0 = np.array([0.02, y0 + 0.04, 0.03])
    for s in (-1, 1):
        barra(t, p0, p0 + np.array([s * 0.045, 0.60, 0.05]), 0.011, METAL_OSC, mezclar(METAL, BLANCO, 0.3), lados=4)
        barra(t, p0 + np.array([s * 0.045, 0.60, 0.05]), p0 + np.array([s * 0.012, 0.67, 0.055]), 0.010, mezclar(METAL, BLANCO, 0.3), lados=4)
    torno(t, [(0.03, 0.0, METAL_OSC), (0.03, 0.03, METAL)], 6, centro=p0 + np.array([0, 0.16, 0.012]))
    # tubo de nucleo de 2 cm con su tapa
    c0 = np.array([0.22, y0 + 0.04, -0.03])
    c1 = c0 + np.array([0.08, 0.56, -0.05])
    barra(t, c0, c1, 0.020, ORO_OSC, ORO, lados=6)
    barra(t, c1, c1 + (c1 - c0) * 0.06, 0.026, METAL, mezclar(METAL, BLANCO, 0.4), lados=6)
    # martillo apoyado en el borde
    h0 = np.array([-0.02, y0 + h + 0.012, 0.11])
    barra(t, h0 + np.array([-0.16, 0, 0]), h0 + np.array([0.14, 0.01, 0.02]), 0.014, METAL_OSC, METAL, lados=5)
    bloque(t, h0 + np.array([0.16, 0.015, 0.022]), (0.06, 0.06, 0.13), mezclar(METAL_OSC, PAL["piedra_osc"], 0.4), R=rot_y(0.12))
    _ = rng
    guardar("LUN-08", [("LUN-08_caja_de_herramientas", [m, t], (0, 0, 0))])


# ---------- LUN-09 casco de burbuja ----------

def casco():
    R = 0.27
    b = Malla("LUN-09_burbuja", "Casco")
    gajos, anillos = 12, 7
    corte = math.radians(142)                 # abierta por abajo: el cuello
    for a in range(anillos):
        t0, t1 = corte * a / anillos, corte * (a + 1) / anillos
        for g in range(gajos):
            f0, f1 = 2 * math.pi * g / gajos, 2 * math.pi * (g + 1) / gajos

            def P(t, f):
                return np.array([math.sin(t) * math.cos(f), math.cos(t), math.sin(t) * math.sin(f)]) * R
            p00, p01, p10, p11 = P(t0, f0), P(t0, f1), P(t1, f0), P(t1, f1)
            col = mezclar(PAL["piedra_clara"], PAL["brillo"], 0.6)
            if a == 0:
                tri = [p00, p11, p10]
                b.tri(*tri, col, col, col, normales=[q / R for q in tri])
            else:
                for tri in ([p00, p01, p11], [p00, p11, p10]):
                    b.tri(*tri, col, col, col, normales=[q / R for q in tri])
    aro = Malla("LUN-09_aro")
    yc = R * math.cos(corte)
    rc = R * math.sin(corte)
    torno(aro, [(rc + 0.030, yc - 0.050, METAL_OSC), (rc + 0.042, yc - 0.020, METAL), (rc + 0.030, yc + 0.012, mezclar(METAL, BLANCO, 0.45)),
                (rc + 0.004, yc + 0.012, METAL)], 12, tapa_abajo=False, tapa_arriba=False)
    luz = Malla("LUN-09_luz", "Emisivo")
    octaedro(luz, (rc + 0.045, yc - 0.018, 0.0), 0.016, PAL["cian"], alto=1.0)
    guardar("LUN-09", [("LUN-09_casco_de_burbuja", [b, aro, luz], (0, 0, 0))])


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    # LUN-02, LUN-03, LUN-04 y LUN-10 a LUN-19 los escribe luna_recursos_v2.py
    for fn in (baliza, bandera_estados_unidos, bandera_ecuador, herramientas, casco):
        fn()
    for ident, n in RESUMEN.items():
        print(f"{ident}: {n} triangulos")
    print("total:", sum(RESUMEN.values()))


if __name__ == "__main__":
    main()
