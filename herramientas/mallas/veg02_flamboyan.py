"""VEG-02 Flamboyan: el arbol grande de flores rojas de la vista aprobada del sendero (ANC_VISTA_JUEGO).

Genera dos recursos con el nucleo (herramientas/mallas/nucleo.py), sin tocarlo:
  VEG-02.glb          tronco grueso y algo retorcido, raices tabulares que serpentean por el suelo hasta
                      3 m (sobre todo hacia +X y +Z, el sendero), ramas gruesas que se abren y copa en
                      paraguas de racimos de hojas, salpicada de ramilletes de flores rojo-coral.
                      Caja 7,3 x 5,4 x 5,3 m (ancho X, alto, fondo Z); copa desplazada ~1,45 m hacia +X.
  VEG-02_petalos.glb  flores caidas, planas y casi a ras del suelo (y <= 0,06 m), para esparcir alrededor
                      del tronco (parche de 4 x 3 m, 54 flores o grupos de petalos).

Nodos: VEG-02_flamboyan (raiz) con VEG-02_tronco ("Facetado": tronco, raices y ramas) y VEG-02_copa
("Follaje": hojas, nucleos de los racimos y flores); VEG-02_petalos ("Follaje").
Origen: centro de la base del tronco (el parche, en su centro), apoyado en y = 0.

Uso, desde la raiz del proyecto:  python -I herramientas/mallas/veg02_flamboyan.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402

from nucleo import (PAL, RAIZ, Escena, Malla, fibonacci, flor, hoja, marco, mezclar,  # noqa: E402
                    solido_facetado)

SALIDA = RAIZ / "pruebas" / "escena_exploracion" / "modelos"
GENERADOR = "herramientas/mallas/veg02_flamboyan.py"
ARRIBA = np.array([0.0, 1.0, 0.0])


# ---------- ayudas propias (el nucleo no se modifica) ----------

def normalizar(v):
    v = np.asarray(v, float)
    return v / max(float(np.linalg.norm(v)), 1e-12)


def catmull_rom(puntos, n):
    """n puntos sobre la curva suave que pasa por los puntos de control."""
    P = [np.asarray(p, float) for p in puntos]
    P = [2 * P[0] - P[1]] + P + [2 * P[-1] - P[-2]]
    tramos = len(P) - 3
    salida = []
    for k in range(n):
        u = k / (n - 1) * tramos
        i = min(int(u), tramos - 1)
        t = u - i
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        salida.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                             + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    return salida


def tono_madera(base, rng, acento):
    """Tono propio de una faceta de corteza: variacion suave y, a veces, un toque calido."""
    c = np.asarray(base, float) * (1.0 + rng.normal(0, 0.06))
    if rng.random() < acento:
        calido = PAL["terracota"] if rng.random() < 0.6 else PAL["tierra2"]
        c = mezclar(c, calido, rng.uniform(0.25, 0.45))
    return c


def degradado_faceta(pts, base):
    """Degradado pintado de una faceta: oscuro abajo y claro arriba segun su propia altura; las caras
    que miran al cielo se pintan claras y las que miran al suelo, oscuras."""
    pts = np.asarray(pts, float)
    n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    n = n / max(float(np.linalg.norm(n)), 1e-12)
    oscuro = mezclar(base, PAL["oscuro"], 0.2)
    claro = mezclar(base, PAL["tierra2"], 0.18)
    y0, y1 = pts[:, 1].min(), pts[:, 1].max()
    rango = max(y1 - y0, 0.05)
    peso = abs(n[1])
    cols = []
    for p in pts:
        t = (p[1] - y0) / rango * (1 - peso) + (0.5 + 0.5 * n[1]) * peso
        cols.append(mezclar(oscuro, claro, float(np.clip(t, 0, 1))))
    return cols


def tubo_pintado(m: Malla, centros, radios, lados, col_bajo, col_alto, rng, torsion=0.0, ruido=0.12,
                 tapa=True, alto=None, acento=0.3):
    """Como nucleo.tubo, pero cada faceta lleva su propio tono y su degradado pintado.

    'alto' da el radio vertical de cada anillo (secciones ovaladas: raices tabulares). Lo que queda bajo
    el suelo se aplana en y = 0 y se descartan las caras enterradas.
    """
    centros = [np.asarray(c, float) for c in centros]
    alto = radios if alto is None else alto
    anillos = []
    for idx, (c, r, rv) in enumerate(zip(centros, radios, alto)):
        tang = centros[min(idx + 1, len(centros) - 1)] - centros[max(idx - 1, 0)]
        u, v = marco(tang)
        ang = np.arange(lados) / lados * 2 * math.pi + idx * torsion
        k = rng.uniform(1 - ruido, 1 + ruido, lados)
        anillo = c + np.outer(np.cos(ang) * r * k, u) + np.outer(np.sin(ang) * rv * k, v)
        anillo[:, 1] = np.maximum(anillo[:, 1], 0.0)
        anillos.append(anillo)

    def poner(tri, cols):
        if max(p[1] for p in tri) < 1e-4:  # enterrado: no se ve nunca
            return
        m.tri(*tri, *cols)

    total = len(anillos) - 1
    for a in range(total):
        t = (a + 0.5) / total
        for s in range(lados):
            s2 = (s + 1) % lados
            q = [anillos[a][s], anillos[a][s2], anillos[a + 1][s2], anillos[a + 1][s]]
            # un tono por cara y su degradado; los dos triangulos de la cara lo comparten
            cols = degradado_faceta(q, tono_madera(mezclar(col_bajo, col_alto, t), rng, acento))
            poner([q[0], q[1], q[2]], [cols[0], cols[1], cols[2]])
            poner([q[0], q[2], q[3]], [cols[0], cols[2], cols[3]])
    if tapa:
        fin = anillos[-1]
        cen = fin.mean(0)
        for s in range(lados):
            m.tri(cen, fin[s], fin[(s + 1) % lados], mezclar(col_alto, PAL["tierra2"], 0.3))
    return m


class _Giro:
    """flor() toma su giro de rng.uniform(); este objeto lo fija para alternar las capas de petalos."""

    def __init__(self, angulo):
        self.angulo = angulo

    def uniform(self, *_):
        return self.angulo


ROJO_PUNTA = mezclar(PAL["coral"], PAL["terracota"], 0.4)
ROJO_BASE = mezclar(PAL["terracota"], PAL["oscuro"], 0.25)


def flor_flamboyan(m: Malla, centro, normal, radio, rng, punta=ROJO_PUNTA, base=ROJO_BASE, estambres=True):
    """Flor con tres capas de flor() del nucleo: dos estrellas alternas (corola llena de diez petalos,
    rojo oscuro en el centro y coral en las puntas) y una estrella pequena dorada (los estambres)."""
    n = normalizar(normal)
    c = np.asarray(centro, float)
    giro = rng.uniform(0, 2 * math.pi)
    flor(m, c, n, radio, punta, base, 5, _Giro(giro))
    # iteracion 7 del ajuste al ancla: la segunda corola va hacia el rojo (no hacia el coral) y los estambres
    # son mas chicos; con el sol calido la flor se leia como una estrella naranja
    flor(m, c + n * 0.008, n, radio * 0.8, mezclar(punta, PAL["terracota"], 0.25), base, 5,
         _Giro(giro + math.pi / 5))
    if estambres:
        flor(m, c + n * 0.016, n, radio * 0.15, mezclar(PAL["dorado"], PAL["coral"], 0.3), PAL["dorado"], 5,
             _Giro(giro + 0.3))


def petalo_suelto(m: Malla, centro, normal, largo, ancho, ang, col_base, col_punta):
    """Un petalo caido: rombo plano de dos triangulos."""
    n = normalizar(normal)
    u, v = marco(n)
    d = u * math.cos(ang) + v * math.sin(ang)
    lado = np.cross(n, d)
    c = np.asarray(centro, float)
    a, b = c - d * largo * 0.35, c + d * largo * 0.65
    i, o = c + lado * ancho * 0.5, c - lado * ancho * 0.5
    nn = [n, n, n]
    cm = mezclar(col_base, col_punta, 0.5)
    m.tri(a, i, b, col_base, cm, col_punta, nn)
    m.tri(a, b, o, col_base, col_punta, cm, nn)


# ---------- tronco, raices y ramas ----------

# corteza: madera1/madera2 con terracota, el rojizo del tronco del ancla
MADERA_BAJA = mezclar(PAL["madera2"], PAL["terracota"], 0.4)
MADERA_ALTA = mezclar(PAL["madera1"], PAL["terracota"], 0.45)


def tronco(m: Malla, rng):
    """Tronco grueso que se tuerce y se inclina un poco hacia el sendero (+X)."""
    eje = catmull_rom([(0.0, 0.0, 0.0), (0.04, 0.7, 0.03), (0.14, 1.35, -0.02), (0.30, 1.95, -0.09),
                       (0.40, 2.40, -0.13)], 8)
    radios = np.interp(np.linspace(0, 1, 8), [0, 0.18, 0.55, 1.0], [0.80, 0.64, 0.57, 0.50])
    tubo_pintado(m, eje, radios, 11, MADERA_BAJA, mezclar(MADERA_BAJA, MADERA_ALTA, 0.75), rng,
                 torsion=0.17, ruido=0.08, acento=0.4)


# angulo (grados, de +X hacia +Z: 90 = hacia la camara), largo, altura de arranque, amplitud y numero
# de ondas del serpenteo, grosor relativo
RAICES = [
    (6, 3.0, 1.00, 0.34, 0.9, 1.00),     # la larga hacia el sendero
    (46, 2.7, 0.95, 0.30, 1.1, 0.95),    # hacia el sendero y la camara
    (92, 1.5, 0.85, 0.16, 0.8, 0.85),
    (140, 1.4, 0.80, 0.16, 1.0, 0.80),
    (190, 2.0, 0.90, 0.24, 0.9, 0.90),
    (244, 1.1, 0.80, 0.10, 0.7, 0.80),
    (294, 1.3, 0.85, 0.14, 0.8, 0.80),
    (336, 1.9, 0.90, 0.22, 1.0, 0.90),
]


def camino(inicio, direccion, largo, amp, ondas, rng):
    """Polilinea en el plano del suelo que serpentea a los lados de una direccion."""
    d = normalizar([direccion[0], 0.0, direccion[2]])
    lado = np.array([-d[2], 0.0, d[0]])
    n = max(6, int(largo / 0.24) + 4)
    fase = rng.uniform(0, 2 * math.pi)
    pts = []
    for i in range(n):
        s = i / (n - 1)
        lat = amp * s ** 0.9 * math.sin(2 * math.pi * ondas * s + fase)
        pts.append(np.asarray(inicio, float) + d * s * largo + lado * lat)
    return pts, d


def raices(m: Malla, rng):
    """Raices tabulares: altas junto al tronco; luego gruesas y redondas, medio hundidas en el suelo,
    serpenteando hasta 3 m; al final se meten en la tierra en vez de afinarse en punta."""
    for ang, largo, h0, amp, ondas, grosor in RAICES:
        a = math.radians(ang + rng.uniform(-4, 4))
        dirr = np.array([math.cos(a), 0.0, math.sin(a)])
        pts, _ = camino(dirr * 0.2, dirr, largo, amp, ondas, rng)
        n = len(pts)
        centros, rh, rv = [], [], []
        for i, p in enumerate(pts):
            s = i / (n - 1)
            ancho = (0.12 + 0.18 * (1 - s) ** 0.8) * grosor
            redondo = ancho * 0.85
            e = max(math.hypot(p[0], p[2]) - 0.6, 0.0)  # distancia desde la corteza
            tope_lejos = 1.25 * redondo                 # lejos del tronco asoma algo mas de la mitad
            tope = tope_lejos + (h0 - tope_lejos) * math.exp(-e / 0.45)
            # ondula un poco en altura y en el ultimo cuarto se hunde del todo en la tierra
            hundir = max(0.0, (s - 0.72) / 0.28)
            tope += 0.035 * math.sin(7.0 * s + ang) * min(1.0, e) * (1 - hundir)
            tope -= 1.5 * tope_lejos * hundir ** 1.5
            vert = max(redondo, min(tope * 0.55, 0.45))
            rh.append(ancho)
            rv.append(vert)
            centros.append(np.array([p[0], tope - vert, p[2]]))
        tubo_pintado(m, centros, rh, 7, MADERA_BAJA, mezclar(MADERA_BAJA, MADERA_ALTA, 0.5), rng,
                     ruido=0.08, alto=rv, acento=0.35, tapa=False)


# ramas maestras: puntos de control, radio inicial y radio final
RAMAS = [
    # la rama larga hacia la derecha (+X), casi horizontal: la que cruza lo alto de la imagen
    ([(0.20, 1.70, -0.08), (1.05, 2.50, -0.22), (2.15, 3.10, -0.40), (3.25, 3.50, -0.55),
      (4.25, 3.75, -0.62)], 0.42, 0.11),
    # hacia la izquierda (-X)
    ([(0.05, 1.65, 0.02), (-0.60, 2.35, 0.20), (-1.30, 3.00, 0.25), (-1.90, 3.50, 0.10)], 0.38, 0.10),
    # hacia atras (-Z) y arriba
    ([(0.28, 1.90, -0.22), (0.55, 2.75, -0.95), (0.90, 3.55, -1.70), (1.15, 4.05, -2.30)], 0.36, 0.09),
    # hacia delante (+Z) y a la derecha
    ([(0.32, 1.95, 0.05), (0.95, 2.80, 0.55), (1.55, 3.55, 1.00), (1.95, 3.95, 1.35)], 0.34, 0.09),
    # al centro, hacia arriba
    ([(0.42, 2.10, -0.10), (0.78, 3.05, -0.28), (1.15, 3.95, -0.40)], 0.32, 0.08),
    # atras a la izquierda
    ([(0.08, 1.85, -0.15), (-0.50, 2.65, -0.80), (-1.00, 3.40, -1.50)], 0.31, 0.08),
]


def ramas(m: Malla, racimos_, rng):
    """Ramas maestras que se abren desde la cruz del tronco y ramillas hasta cada racimo de la copa."""
    muestras = []  # (punto, radio) a lo largo de las ramas maestras, para colgar las ramillas
    centros_r = np.array([c for c, _ in racimos_])
    for puntos, r0, r1 in RAMAS:
        puntos = [np.asarray(p, float) for p in puntos]
        # la punta de cada rama maestra termina dentro del racimo mas cercano
        fin = puntos[-1]
        j = int(np.argmin(np.linalg.norm(centros_r - fin, axis=1)))
        puntos[-1] = centros_r[j] - np.array([0, 0.15, 0])
        largo = sum(np.linalg.norm(puntos[i + 1] - puntos[i]) for i in range(len(puntos) - 1))
        n = max(5, int(largo / 0.45) + 2)
        cen = catmull_rom(puntos, n)
        rad = [r0 + (r1 - r0) * (i / (n - 1)) ** 0.8 for i in range(n)]
        tubo_pintado(m, cen, rad, 8, mezclar(MADERA_BAJA, MADERA_ALTA, 0.5), MADERA_ALTA, rng,
                     torsion=0.1, ruido=0.08, acento=0.35)
        for i in range(1, n):
            if i / (n - 1) >= 0.3:
                muestras.append((cen[i], rad[i]))
    puntos_m = np.array([p for p, _ in muestras])
    for C, r in racimos_:
        # punto de enganche: el mas cercano, prefiriendo los que quedan por debajo del racimo
        dist = np.linalg.norm(puntos_m - C, axis=1) + np.maximum(puntos_m[:, 1] - C[1] + 0.3, 0) * 2.0
        k = int(np.argmin(dist))
        P, rp = muestras[k]
        if np.linalg.norm(P - C) < 0.35:
            continue
        medio = (P + C) / 2 + np.array([0, 0.22, 0]) + rng.normal(0, 0.08, 3)
        cen = catmull_rom([P, medio, C - np.array([0, 0.1, 0])], 4)
        rad = list(np.linspace(min(rp * 0.65, 0.15), 0.045, 4))
        tubo_pintado(m, cen, rad, 5, mezclar(MADERA_BAJA, MADERA_ALTA, 0.6), MADERA_ALTA, rng,
                     ruido=0.08, acento=0.25)


# ---------- copa ----------

# elipse de la copa: mas ancha en X que honda en Z, porque la camara fija ve el fondo (Z) acortado
# y la cara frontal entera; asi se lee como el paraguas ancho del ancla y de la hoja
COPA_CX, COPA_CZ, COPA_AX, COPA_AZ = 1.45, -0.55, 3.05, 1.9
Y_COPA_BAJA, Y_COPA_ALTA = 3.4, 5.5
APLASTE = np.array([1.0, 0.72, 1.0])  # racimos achatados: la copa se lee como un paraguas


def domo(rho):
    return 4.15 + 0.5 * (1 - rho ** 2)


def racimos(rng):
    """Centros y radios de los racimos: paraguas ancho y plano, borde apenas caido y remates arriba.
    La rejilla es densa para que no queden claros vistos desde arriba; la luz moteada pasa entre hojas
    y por algun hueco del borde."""
    lista = []
    paso = 1.0
    for fila in range(-3, 4):
        for col in range(-4, 5):
            x = COPA_CX + (col + 0.5 * (fila % 2)) * paso + rng.uniform(-0.15, 0.15)
            z = COPA_CZ + fila * paso * 0.866 + rng.uniform(-0.15, 0.15)
            rho = math.hypot((x - COPA_CX) / COPA_AX, (z - COPA_CZ) / COPA_AZ)
            if rho > 0.95 or (rho > 0.75 and rng.random() < 0.1):
                continue
            y = domo(rho) + rng.uniform(-0.12, 0.12)
            lista.append((np.array([x, y, z]), 0.86 - 0.2 * rho + rng.uniform(-0.06, 0.06)))
    for k in range(14):  # borde del paraguas
        a = k / 14 * 2 * math.pi + rng.uniform(-0.12, 0.12)
        x = COPA_CX + math.cos(a) * COPA_AX * 1.02
        z = COPA_CZ + math.sin(a) * COPA_AZ * 1.02
        lista.append((np.array([x, 3.78 + rng.uniform(-0.1, 0.1), z]), 0.6 + rng.uniform(-0.05, 0.06)))
    # (iteracion 18 del ajuste al ancla: un lobulo delante del tronco para cubrir la esquina superior
    # izquierda subio el dE de esa zona de 21,7 a 29,3; se descarto)
    for k in range(5):  # remates del domo
        a = k / 5 * 2 * math.pi + rng.uniform(-0.3, 0.3)
        rho = rng.uniform(0.15, 0.5)
        x = COPA_CX + math.cos(a) * COPA_AX * rho
        z = COPA_CZ + math.sin(a) * COPA_AZ * rho
        lista.append((np.array([x, domo(rho) + 0.36, z]), 0.56 + rng.uniform(-0.04, 0.04)))
    return lista


HOJA_OSCURA = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.4)


def color_hoja(y, arriba, rng):
    """Base y punta de una hoja: mas oscuras abajo y hacia dentro, mas claras arriba, a veces doradas."""
    g = float(np.clip((y - Y_COPA_BAJA) / (Y_COPA_ALTA - Y_COPA_BAJA), 0, 1))
    a = float(np.clip((arriba + 0.6) / 1.6, 0, 1))
    tono = float(np.clip(0.5 * g + 0.5 * a + rng.normal(0, 0.12), 0, 1))
    base = mezclar(HOJA_OSCURA, PAL["hierba_sombra"], tono * 0.9)
    punta = mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], min(1.0, tono * 1.15))
    if rng.random() < 0.08 + 0.12 * tono:
        punta = mezclar(punta, PAL["dorado"], 0.4)
    return base, punta


def racimo_hojas(m: Malla, C, r, rng):
    """Hojas del racimo con la normal hacia fuera (la luz las modula) y la punta hacia abajo y afuera."""
    n = int(56 * (r / 0.85) ** 2)
    dirs = fibonacci(int(n / 0.8) + 4)
    dirs = dirs[dirs[:, 1] > -0.6]
    apice = C + np.array([0, r * 0.9, 0])
    for d0 in dirs:
        dirr = normalizar(d0 + rng.normal(0, 0.15, 3))
        pos = C + dirr * r * rng.uniform(0.62, 0.88) * APLASTE
        nrm = normalizar(dirr + np.array([0, 0.2, 0]))
        tang = pos - apice
        tang = tang - nrm * (tang @ nrm)
        if np.linalg.norm(tang) < 1e-3:
            tang = np.cross(nrm, rng.normal(0, 1, 3))
        tang = normalizar(normalizar(tang) + rng.normal(0, 0.35, 3))
        tang = normalizar(tang - nrm * (tang @ nrm))
        largo = rng.uniform(0.33, 0.42)
        ancho = largo * rng.uniform(0.52, 0.6)
        base, punta = color_hoja(pos[1], dirr[1], rng)
        hoja(m, pos - tang * largo * 0.3, tang, nrm, largo, ancho, base, punta, doblez=0.22)
        # dos tonos: la mitad de un lado del nervio, mas oscura (triangulos 2 y 4 de hoja())
        m.C[-3] = m.C[-3] * 0.84
        m.C[-1] = m.C[-1] * 0.84


def nucleo_racimo(C, r, rng):
    """Volumen oscuro y pequeno dentro del racimo: da fondo entre las hojas sin tapar toda la luz."""
    pts = fibonacci(12) * rng.uniform(0.85, 1.1, (12, 1)) * np.array([r * 0.5, r * 0.36, r * 0.5]) + C
    return solido_facetado("nucleo", pts, mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.55),
                           mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.2), PAL["hierba_sombra"], rng,
                           var=0.05, material="Follaje")


def racimo_flores(m: Malla, C, r, grupos, rng):
    """Ramilletes de 2 a 5 flores grandes sobre la cara alta y frontal del racimo, sobre las hojas."""
    cand = fibonacci(40)
    cand = cand[(cand[:, 1] > 0.05) | ((cand[:, 1] > -0.3) & (cand[:, 2] > 0.3))]
    for _ in range(grupos):
        eje = cand[int(rng.integers(len(cand)))]
        for _ in range(int(rng.integers(2, 6))):
            dirr = normalizar(eje + rng.normal(0, 0.28, 3))
            if dirr[1] < -0.35:
                continue
            nrm = normalizar(dirr + ARRIBA * 0.35)
            pos = C + dirr * r * 0.93 * APLASTE + nrm * 0.03
            flor_flamboyan(m, pos, nrm, rng.uniform(0.22, 0.29), rng,
                           punta=mezclar(ROJO_PUNTA, PAL["coral"], rng.uniform(0.0, 0.4)))


def copa(m: Malla, racimos_, rng):
    for C, r in racimos_:
        m.anexar(nucleo_racimo(C, r, rng))
    for C, r in racimos_:
        racimo_hojas(m, C, r, rng)
    for C, r in racimos_:
        # unos racimos van cargados de flores, otros menos (iteracion 3 del ajuste al ancla: la copa
        # del ancla es casi mitad flor roja; antes salian 0 a 2 ramilletes por racimo y se veia verde)
        tipo = rng.random()
        grupos = 3 if tipo < 0.4 else 2 if tipo < 0.8 else 1
        racimo_flores(m, C, r, grupos, rng)


# ---------- recursos ----------

def arbol():
    madera = Malla("VEG-02_tronco", "Facetado")
    follaje = Malla("VEG-02_copa", "Follaje")
    lista = racimos(np.random.default_rng(204))
    tronco(madera, np.random.default_rng(201))
    raices(madera, np.random.default_rng(202))
    ramas(madera, lista, np.random.default_rng(203))
    copa(follaje, lista, np.random.default_rng(205))
    e = Escena(GENERADOR)
    raiz = e.nodo("VEG-02_flamboyan")
    e.nodo("VEG-02_tronco", e.malla(madera), padre=raiz)
    e.nodo("VEG-02_copa", e.malla(follaje), padre=raiz)
    ruta = e.guardar(SALIDA / "VEG-02.glb")
    return ruta, e.stats, madera, follaje


def petalos(n=54):
    """Flores caidas en grupos sueltos dentro de una elipse de 4 x 3 m, casi a ras del suelo y mas
    ralas hacia el borde."""
    rng = np.random.default_rng(206)
    m = Malla("VEG-02_petalos", "Follaje")
    grupos = [np.array([rng.uniform(-1.3, 1.3), rng.uniform(-0.9, 0.9)]) for _ in range(7)]
    puntos = []
    intentos = 0
    while len(puntos) < n and intentos < 20000:
        intentos += 1
        if rng.random() < 0.6:
            p = grupos[int(rng.integers(len(grupos)))] + rng.normal(0, 0.5, 2)
        else:
            p = np.array([rng.uniform(-2.0, 2.0), rng.uniform(-1.5, 1.5)])
        if (p[0] / 1.95) ** 2 + (p[1] / 1.45) ** 2 > 1.0:
            continue
        if any(np.linalg.norm(p - q) < 0.3 for q in puntos):
            continue
        puntos.append(p)
    for k, (x, z) in enumerate(puntos):
        nrm = normalizar([rng.normal(0, 0.05), 1.0, rng.normal(0, 0.05)])
        centro = np.array([x, 0.018 + 0.0005 * k, z])
        tipo = rng.random()
        radio = rng.uniform(0.15, 0.21)
        punta = mezclar(ROJO_PUNTA, PAL["terracota"], rng.uniform(0.0, 0.35))
        if tipo < 0.6:  # flor entera
            flor_flamboyan(m, centro, nrm, radio, rng, punta=punta)
        elif tipo < 0.82:  # flor marchita: una sola estrella, sin estambres
            marchita = mezclar(punta, PAL["tierra2"], rng.uniform(0.1, 0.3))
            flor(m, centro, nrm, radio * 0.85, marchita, ROJO_BASE, 5, rng)
        else:  # petalos sueltos
            for _ in range(int(rng.integers(2, 4))):
                c = centro + np.array([rng.normal(0, 0.09), 0.0, rng.normal(0, 0.09)])
                petalo_suelto(m, c, nrm, rng.uniform(0.12, 0.17), rng.uniform(0.06, 0.08),
                              rng.uniform(0, 2 * math.pi), ROJO_BASE, punta)
    e = Escena(GENERADOR)
    e.nodo("VEG-02_petalos", e.malla(m))
    ruta = e.guardar(SALIDA / "VEG-02_petalos.glb")
    return ruta, e.stats, m, len(puntos)


def resumen(nombre, mallas):
    P = np.concatenate([np.array(x.P).reshape(-1, 3) for x in mallas if len(x)])
    lo, hi = P.min(0), P.max(0)
    print(f"  {nombre}: caja x [{lo[0]:.2f}, {hi[0]:.2f}]  y [{lo[1]:.2f}, {hi[1]:.2f}]  "
          f"z [{lo[2]:.2f}, {hi[2]:.2f}]  -> {hi[0] - lo[0]:.2f} x {hi[1] - lo[1]:.2f} x {hi[2] - lo[2]:.2f} m")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ruta, stats, madera, follaje = arbol()
    print(f"{ruta.name}: {sum(stats.values())} triangulos {stats}")
    resumen("VEG-02", [madera, follaje])
    ruta, stats, m, n = petalos()
    print(f"{ruta.name}: {sum(stats.values())} triangulos {stats}, {n} flores o grupos de petalos")
    resumen("VEG-02_petalos", [m])


if __name__ == "__main__":
    main()
