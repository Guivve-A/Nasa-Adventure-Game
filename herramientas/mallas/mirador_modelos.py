"""Modelos del Mirador del Faro (zona «mirador» del juego jugable v0), hechos por script.

Hojas de referencia: HR_MIR_v1 (MIR-01 a MIR-08), HR_TAL_v1 (TAL-10, TAL-11), HR_ARQ_v1 (ARQ-09),
HR_URB_v1 (URB-07) y HR_VEG_v1 (VEG-08). Concepto: Lote_03/L03_mirador_noche_vista_juego.png.
Ninguna tiene aun el veredicto de Guillermo: todo esto es PROVISIONAL.

Recursos que escribe en juego/modelos/mirador/<ID>.glb (origen en el centro de la base, y = 0):
  MIR-01  faro (la puerta mira a +Z)            MIR-03  telescopio (apunta a +X, 20 grados de altura)
  MIR-04  binoculares de moneda (miran a +Z)    MIR-05  atril con carta estelar (frente a +Z)
  MIR-06  banca de piedra con manta             MIR-07  poste de la guirnalda
  MIR-09  mesa del club (ID nuevo)              MIR-10  porton del cerro (ID nuevo; hojas con bisagra)
  TAL-10  taburete                              TAL-11  maqueta de satelite (cubo y dos paneles 10:27)
  TAL-18  portatil del club (ID nuevo)          ARQ-09  farol
  ARQ-14  casas del barrio de fondo, simplificadas (ID nuevo; nodos _a, _b y _c)
  URB-07  maceta de barro                       VEG-08  buganvilla en cascada
  VEG-15  copa de arbol de fondo (ID nuevo)
Ademas escribe juego/modelos/mirador/calidos.json: las luces calidas de cada modelo (ventanas, bombillas)
en coordenadas locales. El material «Emisivo» del proyecto es cian (tecnologia), asi que lo calido lo dibuja
la zona con Piezas.nodo(m, "emisivo") a partir de esa lista (ver mirador_escena.py y zonas/mirador/mirador.gd).

IDs nuevos elegidos para no chocar con otros carriles: la habitacion ya usa TAL-15 a TAL-17 y la ciudad
ARQ-13 (biblioteca); por eso el portatil es TAL-18 y las casas de fondo ARQ-14.
La plataforma MIR-02, la ladera TER-15 y el layout de la zona los escribe mirador_escena.py.

Sin logotipos ni textos. Solo colores de la paleta maestra y sus mezclas, con UNA excepcion PROPUESTA al
director (sin aprobar): el magenta de la buganvilla (VEG-08 «magenta bracts» en el Catalogo) y de la cayena
magenta. Se midio en las referencias: mediana d42f78 en L03 y f93c90 en HR_VEG_v1. Antes salia coral enfriado
(salmon apagado) y el critico de la v2 lo rechazo. Si el director no lo aprueba, basta con MAGENTA = ROSA.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/mirador_modelos.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, RAIZ, Escena, Malla, caja, fibonacci, flor, hoja, marco, mezclar, rot_y, solido_facetado  # noqa: E402

SALIDA = RAIZ / "juego" / "modelos" / "mirador"
CALIDOS: dict[str, list] = {}
RESUMEN: dict[str, int] = {}


# ---------- tonos ----------

def osc(c, t=0.35):
    return mezclar(c, PAL["petroleo"], t)


def cla(c, t=0.3):
    return mezclar(c, PAL["crema"], t)


PIEDRA = mezclar(PAL["piedra_clara"], PAL["tierra1"], 0.55)        # piedra labrada melocoton (como TER-11)
PIEDRA_LUZ = mezclar(PAL["tierra1"], PAL["crema"], 0.40)
PIEDRA_MALVA = mezclar(PAL["piedra"], PAL["piedra_clara"], 0.35)
BLANCO = mezclar(PAL["piedra_clara"], PAL["crema"], 0.55)
MADERA = mezclar(PAL["madera1"], PAL["tierra2"], 0.6)
MADERA_LUZ = mezclar(PAL["tierra2"], PAL["tierra1"], 0.4)
MADERA_OSC = PAL["madera1"]
METAL = mezclar(PAL["piedra_osc"], PAL["petroleo"], 0.5)           # hierro pintado: nunca negro puro
METAL_LUZ = mezclar(METAL, PAL["piedra_clara"], 0.35)
TEJA = mezclar(PAL["terracota"], PAL["coral"], 0.35)
VERDE = mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.35)
VERDE_OSC = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.35)
ROSA = mezclar(mezclar(PAL["coral"], PAL["crema"], 0.20), PAL["piedra_clara"], 0.18)
ROSA_OSC = mezclar(PAL["coral"], PAL["piedra"], 0.30)
VIDRIO_APAGADO = mezclar(PAL["petroleo"], PAL["oscuro"], 0.35)
# excepcion propuesta (ver arriba): magenta medido en L03 y HR_VEG_v1
MAGENTA = np.array([0xD4, 0x2F, 0x78]) / 255.0
MAGENTA_LUZ = np.array([0xF0, 0x4A, 0x96]) / 255.0
# blanco de flor: crema de la paleta aclarado con el brillo (#CEF8F5), sin salir de la familia
BLANCO_FLOR = mezclar(PAL["crema"], PAL["brillo"], 0.58)


# ---------- geometria comun ----------

def _tri(m: Malla, a, b, c, ca, cb, cc):
    a, b, c = (np.asarray(p, float) for p in (a, b, c))
    if np.linalg.norm(np.cross(b - a, c - a)) > 1e-10:
        m.tri(a, b, c, ca, cb, cc)


def cara(m: Malla, pts, col=None, interior=None, arriba=False, cols=None):
    """Poligono plano y convexo. Se orienta hacia arriba, o al lado contrario de 'interior'."""
    P = [np.asarray(p, float) for p in pts]
    C = [np.asarray(c, float) for c in cols] if cols is not None else [np.asarray(col, float)] * len(P)
    n = np.cross(P[1] - P[0], P[2] - P[0])
    cen = sum(P) / len(P)
    voltear = False
    if arriba:
        voltear = n[1] < 0
    elif interior is not None:
        voltear = n @ (cen - np.asarray(interior, float)) < 0
    if voltear:
        P, C = P[::-1], C[::-1]
    for i in range(1, len(P) - 1):
        _tri(m, P[0], P[i], P[i + 1], C[0], C[i], C[i + 1])


def torno(m: Malla, perfil, lados, rng=None, var=0.04, giro=0.0, centro=(0, 0, 0), tapa=True, escala=(1.0, 1.0)):
    """Solido de revolucion facetado. perfil = [(radio, y, color)] de abajo arriba; lo exterior queda a la
    izquierda del recorrido (un tramo plano hacia dentro mira arriba; hacia fuera, abajo)."""
    cx, cy, cz = centro
    ang = giro + (np.arange(lados) + 0.5) / lados * 2 * math.pi
    anillos = [np.stack([cx + np.cos(ang) * r * escala[0], np.full(lados, cy + y), cz + np.sin(ang) * r * escala[1]], 1)
               for r, y, _ in perfil]
    for a in range(len(perfil) - 1):
        c0, c1 = np.asarray(perfil[a][2], float), np.asarray(perfil[a + 1][2], float)
        for s in range(lados):
            s2 = (s + 1) % lados
            v = 1.0 + (rng.normal(0, var) if rng is not None else 0.0)
            p0, p1, p2, p3 = anillos[a][s], anillos[a + 1][s], anillos[a + 1][s2], anillos[a][s2]
            _tri(m, p0, p1, p2, c0 * v, c1 * v, c1 * v)
            _tri(m, p0, p2, p3, c0 * v, c1 * v, c0 * v)
    if tapa and perfil[-1][0] > 1e-6:
        cara(m, list(anillos[-1]), perfil[-1][2], arriba=True)


def bloque(m: Malla, base, tam, col, ry=0.0, rng=None, sombra_t=0.35, luz_t=0.10, var=0.04, sin_base=True):
    """Caja apoyada en 'base' (centro de su cara de abajo), girada ry radianes sobre Y."""
    t = Malla("t")
    x, y, z = tam
    caja(t, (-x / 2, 0, -z / 2), (x / 2, y, z / 2), col, sombra_t, luz_t, rng, var, sin_base)
    m.anexar(t, R=rot_y(ry), t=base)


def barra(m: Malla, p0, p1, r, c0, c1=None, lados=5, r1=None, tapas=True):
    """Barra recta entre dos puntos (patas, tubos, postes), con degradado de c0 a c1."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    c1 = c0 if c1 is None else c1
    r1 = r if r1 is None else r1
    d = p1 - p0
    d = d / np.linalg.norm(d)
    u, v = marco(d)
    ang = (np.arange(lados) + 0.5) / lados * 2 * math.pi
    A = [p0 + (math.cos(a) * u + math.sin(a) * v) * r for a in ang]
    B = [p1 + (math.cos(a) * u + math.sin(a) * v) * r1 for a in ang]
    eje = (p0 + p1) / 2
    for s in range(lados):
        s2 = (s + 1) % lados
        cara(m, [A[s], A[s2], B[s2], B[s]], interior=eje, cols=[c0, c0, c1, c1])
    if tapas:
        cara(m, A, c0, interior=eje)
        cara(m, B, c1, interior=eje)


def disco(m: Malla, centro, normal, r, col, lados=6):
    n = np.asarray(normal, float) / np.linalg.norm(normal)
    u, v = marco(n)
    centro = np.asarray(centro, float)
    pts = [centro + (math.cos(a) * u + math.sin(a) * v) * r for a in (np.arange(lados) + 0.5) / lados * 2 * math.pi]
    cara(m, pts, col, interior=centro - n)


def tabla(m: Malla, centro, der, arr, w, h, t, col_frente, col_canto):
    """Tablero inclinado: 'der' y 'arr' son sus ejes (unitarios); el frente mira a der x arr... hacia n."""
    centro, der, arr = (np.asarray(v, float) for v in (centro, der, arr))
    n = np.cross(der, arr)
    n /= np.linalg.norm(n)
    esq = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                esq[(sx, sy, sz)] = centro + der * sx * w / 2 + arr * sy * h / 2 + n * sz * t / 2
    cara(m, [esq[(-1, -1, 1)], esq[(1, -1, 1)], esq[(1, 1, 1)], esq[(-1, 1, 1)]], col_frente, interior=centro)
    cara(m, [esq[(-1, -1, -1)], esq[(1, -1, -1)], esq[(1, 1, -1)], esq[(-1, 1, -1)]], col_canto, interior=centro)
    for eje, s in ((0, -1), (0, 1), (1, -1), (1, 1)):
        if eje == 0:
            pts = [esq[(s, -1, -1)], esq[(s, 1, -1)], esq[(s, 1, 1)], esq[(s, -1, 1)]]
        else:
            pts = [esq[(-1, s, -1)], esq[(1, s, -1)], esq[(1, s, 1)], esq[(-1, s, 1)]]
        cara(m, pts, col_canto, interior=centro)
    return n


def q_calido(lista, pts, normal):
    lista.append({"q": [[round(float(v), 4) for v in p] for p in pts], "n": [float(v) for v in normal]})


def b_calido(lista, p, r):
    lista.append({"b": [round(float(v), 4) for v in p], "r": r})


def guardar(ident: str, nodos: list, calidos=None):
    """nodos = [(nombre, [mallas], traslacion)]"""
    e = Escena("herramientas/mallas/mirador_modelos.py")
    total = 0
    for nombre, mallas, t in nodos:
        e.nodo(nombre, e.malla(*mallas, nombre=nombre), t=t)
        total += e.stats[nombre]
    e.guardar(SALIDA / f"{ident}.glb")
    RESUMEN[ident] = total
    if calidos:
        CALIDOS[ident] = calidos


# ---------- MIR-01 faro ----------

def faro():
    rng = np.random.default_rng(101)
    m = Malla("MIR-01_faro")
    cal = []
    L = 12
    terra, coral = PAL["terracota"], mezclar(PAL["coral"], PAL["terracota"], 0.30)
    torno(m, [(1.80, 0.0, osc(terra, 0.35)), (1.72, 0.56, terra), (1.62, 0.70, cla(terra, 0.25)),
              (1.47, 0.72, cla(terra, 0.35))], L, rng, tapa=False)
    # v2: dos franjas pintadas (coral y terracota) sobre el cuerpo blanco, como la hoja MIR-01
    def r_cuerpo(y):
        return 1.25 + (1.04 - 1.25) * (y - 2.95) / (4.55 - 2.95)
    # v2b: tres franjas alternas (terracota abajo, coral al medio y coral arriba, bajo la cornisa), como la hoja
    def r_bajo(y):
        return 1.47 + (1.31 - 1.47) * (y - 0.72) / (2.30 - 0.72)
    torno(m, [(1.47, 0.72, osc(terra, 0.25)), (r_bajo(1.38), 1.38, terra), (r_bajo(1.38), 1.38, osc(BLANCO, 0.30)),
              (1.31, 2.30, BLANCO), (1.31, 2.30, osc(coral, 0.2)),
              (1.25, 2.95, coral), (1.25, 2.95, osc(BLANCO, 0.12)), (r_cuerpo(3.30), 3.30, BLANCO),
              (r_cuerpo(3.30), 3.30, cla(BLANCO, 0.15)), (r_cuerpo(3.98), 3.98, BLANCO),
              (r_cuerpo(3.98), 3.98, osc(coral, 0.15)), (1.04, 4.55, cla(coral, 0.12))], L, rng, tapa=False)
    # cornisa y galeria
    torno(m, [(1.04, 4.55, osc(terra, 0.25)), (1.46, 4.74, terra), (1.46, 4.84, cla(terra, 0.2))], L, rng)
    ang = (np.arange(L) + 0.5) / L * 2 * math.pi
    aro = [np.array([math.cos(a) * 1.39, 5.36, math.sin(a) * 1.39]) for a in ang]
    for k in range(L):
        barra(m, (aro[k][0], 4.84, aro[k][2]), aro[k], 0.022, METAL, METAL_LUZ, 4)
        barra(m, aro[k], aro[(k + 1) % L], 0.022, METAL_LUZ, METAL_LUZ, 4, tapas=False)
    # linterna: zocalo, ocho montantes y techo; los vidrios son luces calidas
    torno(m, [(0.84, 4.84, osc(terra, 0.2)), (0.84, 5.04, terra), (0.78, 5.04, terra)], 8, rng, tapa=False)
    a8 = (np.arange(8) + 0.5) / 8 * 2 * math.pi
    for k in range(8):
        p = np.array([math.cos(a8[k]) * 0.80, 0.0, math.sin(a8[k]) * 0.80])
        barra(m, p + (0, 5.04, 0), p + (0, 5.86, 0), 0.035, METAL, METAL_LUZ, 4)
        k2 = (k + 1) % 8
        v0 = np.array([math.cos(a8[k]) * 0.76, 0.0, math.sin(a8[k]) * 0.76])
        v1 = np.array([math.cos(a8[k2]) * 0.76, 0.0, math.sin(a8[k2]) * 0.76])
        q_calido(cal, [v0 + (0, 5.06, 0), v1 + (0, 5.06, 0), v1 + (0, 5.84, 0), v0 + (0, 5.84, 0)], (v0 + v1) / 2)
    # v2b: la lampara de la linterna, un nucleo calido que se ve entre los vidrios (sin haz giratorio)
    b_calido(cal, (0, 5.45, 0), 0.30)
    torno(m, [(0.90, 5.86, osc(terra, 0.2)), (0.96, 5.94, coral), (0.52, 6.36, coral), (0.0, 6.76, cla(coral, 0.25))], 8, rng)
    barra(m, (0, 6.70, 0), (0, 7.08, 0), 0.03, METAL, METAL_LUZ, 4)
    torno(m, [(0.0, 7.04, METAL), (0.07, 7.11, METAL_LUZ), (0.0, 7.18, METAL_LUZ)], 5, rng)
    # puerta (cara +Z, sobre el zocalo) con tres gradas de piedra
    rz = 1.47 * math.cos(math.pi / L)
    bloque(m, (0, 0.70, rz - 0.10), (0.86, 1.42, 0.22), terra, rng=rng, luz_t=0.2)
    bloque(m, (0, 0.72, rz - 0.02), (0.60, 1.22, 0.16), osc(PAL["cian_medio"], 0.55), rng=rng)
    q_calido(cal, [(-0.14, 1.50, rz + 0.07), (0.14, 1.50, rz + 0.07), (0.14, 1.78, rz + 0.07), (-0.14, 1.78, rz + 0.07)], (0, 0, 1))
    for i, (z, h) in enumerate([(1.92, 0.47), (2.20, 0.24)]):
        bloque(m, (0, 0.0, z), (1.10, h, 0.30), PIEDRA if i else PIEDRA_LUZ, rng=rng, luz_t=0.25)
    bloque(m, (0, 0.0, 1.70), (1.10, 0.70, 0.22), PIEDRA_LUZ, rng=rng, luz_t=0.25)
    # farolito de la puerta
    barra(m, (0.52, 1.95, rz - 0.06), (0.52, 1.95, rz + 0.16), 0.02, METAL, METAL_LUZ, 4)
    bloque(m, (0.52, 1.70, rz + 0.16), (0.12, 0.05, 0.12), METAL, rng=rng)
    b_calido(cal, (0.52, 1.84, rz + 0.16), 0.07)
    # ventanas: una alta sobre la puerta (+Z) y otra hacia -X
    for (cx, cy, eje) in [(0.0, 3.62, "z"), (0.0, 1.75, "x")]:
        r_cara = (1.47 + (1.04 - 1.47) * (cy - 0.72) / (4.55 - 0.72)) * math.cos(math.pi / L)
        if cy < 2.3:
            r_cara = (1.47 + (1.31 - 1.47) * (cy - 0.72) / (2.30 - 0.72)) * math.cos(math.pi / L)
        if eje == "z":
            bloque(m, (cx, cy - 0.32, r_cara - 0.06), (0.52, 0.72, 0.16), terra, rng=rng, luz_t=0.2)
            q_calido(cal, [(-0.17, cy - 0.22, r_cara + 0.03), (0.17, cy - 0.22, r_cara + 0.03),
                           (0.17, cy + 0.30, r_cara + 0.03), (-0.17, cy + 0.30, r_cara + 0.03)], (0, 0, 1))
        else:
            bloque(m, (-(r_cara - 0.06), cy - 0.32, 0.0), (0.16, 0.72, 0.52), terra, rng=rng, luz_t=0.2)
            q_calido(cal, [(-(r_cara + 0.03), cy - 0.22, 0.17), (-(r_cara + 0.03), cy - 0.22, -0.17),
                           (-(r_cara + 0.03), cy + 0.30, -0.17), (-(r_cara + 0.03), cy + 0.30, 0.17)], (-1, 0, 0))
    guardar("MIR-01", [("MIR-01_faro", [m], (0, 0, 0))], cal)


# ---------- MIR-03 telescopio ----------

ESTUCHE = (0.35, 0.0, 0.62)   # el estuche queda del lado contrario al ocular


def telescopio():
    rng = np.random.default_rng(103)
    m = Malla("MIR-03_telescopio")
    e = Malla("MIR-03_brillo", "Emisivo")
    piv = np.array([0.0, 1.02, 0.0])
    el = math.radians(20.0)                      # la Luna de las 19:30 esta a 20,0 grados de altura
    d = np.array([math.cos(el), math.sin(el), 0.0])
    up = np.array([-math.sin(el), math.cos(el), 0.0])
    for k in range(3):
        a = math.radians(90 + 120 * k)
        pie = np.array([0.52 * math.cos(a), 0.0, 0.52 * math.sin(a)])
        barra(m, pie, (0.05 * math.cos(a), 0.86, 0.05 * math.sin(a)), 0.034, MADERA_OSC, MADERA_LUZ, 4, r1=0.028)
        bloque(m, pie * 1.0, (0.09, 0.03, 0.09), METAL, rng=rng)
        barra(m, pie * 0.48 + (0, 0.42, 0), (0, 0.40, 0), 0.014, METAL, METAL_LUZ, 3, tapas=False)
    torno(m, [(0.085, 0.82, METAL), (0.10, 0.90, METAL_LUZ), (0.06, 0.98, METAL_LUZ)], 6, rng)
    barra(m, (0, 0.95, 0), piv, 0.045, METAL, METAL_LUZ, 5)
    # eje de contrapeso (montura ecuatorial, con el eje polar casi acostado)
    barra(m, piv, piv + (0, -0.10, -0.34), 0.016, METAL_LUZ, METAL_LUZ, 4)
    barra(m, piv + (0, -0.08, -0.26), piv + (0, -0.105, -0.36), 0.06, METAL, METAL_LUZ, 6)
    # tubo blanco, parasol y ocular
    barra(m, piv - d * 0.46, piv + d * 0.80, 0.078, osc(BLANCO, 0.30), cla(BLANCO, 0.4), 8)
    barra(m, piv + d * 0.72, piv + d * 0.96, 0.092, osc(PAL["terracota"], 0.2), PAL["terracota"], 8, tapas=False)
    disco(m, piv + d * 0.90, d, 0.085, VIDRIO_APAGADO, 8)
    barra(m, piv - d * 0.08, piv + d * 0.08, 0.090, METAL, METAL_LUZ, 8, tapas=False)
    barra(m, piv - d * 0.58, piv - d * 0.46, 0.034, METAL, METAL_LUZ, 6)
    disco(e, piv - d * 0.585, -d, 0.028, PAL["cian"], 6)
    # buscador
    barra(m, piv + up * 0.125 + d * 0.02, piv + up * 0.125 + d * 0.46, 0.024, osc(BLANCO, 0.3), BLANCO, 5)
    barra(m, piv + up * 0.07 + d * 0.12, piv + up * 0.13 + d * 0.12, 0.012, METAL, METAL, 3, tapas=False)
    barra(m, piv + up * 0.07 + d * 0.36, piv + up * 0.13 + d * 0.36, 0.012, METAL, METAL, 3, tapas=False)
    # estuche a un lado
    estuche = osc(PAL["cian_medio"], 0.60)
    bloque(m, ESTUCHE, (0.50, 0.22, 0.30), estuche, ry=0.35, rng=rng, luz_t=0.2)
    bloque(m, (ESTUCHE[0], 0.22, ESTUCHE[2]), (0.52, 0.04, 0.32), mezclar(estuche, PAL["piedra_clara"], 0.25), ry=0.35, rng=rng)
    guardar("MIR-03", [("MIR-03_telescopio", [m, e], (0, 0, 0))])


# ---------- MIR-04 binoculares de moneda ----------

def binoculares():
    rng = np.random.default_rng(104)
    m = Malla("MIR-04_binoculares")
    e = Malla("MIR-04_brillo", "Emisivo")
    verde = osc(PAL["cian_medio"], 0.62)
    verde_luz = mezclar(verde, PAL["piedra_clara"], 0.30)
    torno(m, [(0.27, 0.0, osc(verde, 0.3)), (0.25, 0.07, verde), (0.12, 0.12, verde_luz)], 8, rng, tapa=False)
    torno(m, [(0.075, 0.12, verde), (0.06, 0.96, verde_luz)], 6, rng)
    bloque(m, (0, 0.52, 0.075), (0.17, 0.24, 0.07), verde_luz, rng=rng)
    bloque(m, (0, 0.60, 0.112), (0.05, 0.02, 0.012), PAL["dorado"], rng=rng)
    bloque(m, (0, 0.94, 0), (0.30, 0.05, 0.10), METAL, rng=rng)
    cuerpo = mezclar(PAL["piedra_clara"], PAL["crema"], 0.25)
    for sx in (-1, 1):
        barra(m, (sx * 0.085, 1.08, -0.15), (sx * 0.085, 1.08, 0.17), 0.072, osc(cuerpo, 0.35), cuerpo, 7)
        barra(m, (sx * 0.085, 1.08, 0.15), (sx * 0.085, 1.08, 0.20), 0.080, verde, verde_luz, 7, tapas=False)
        disco(e, (sx * 0.085, 1.08, 0.185), (0, 0, 1), 0.058, PAL["cian_medio"], 7)
        barra(m, (sx * 0.085, 1.08, -0.20), (sx * 0.085, 1.08, -0.15), 0.040, METAL, METAL_LUZ, 5)
    bloque(m, (0, 1.04, 0.0), (0.10, 0.08, 0.20), verde, rng=rng)
    guardar("MIR-04", [("MIR-04_binoculares", [m, e], (0, 0, 0))])


# ---------- MIR-05 atril con carta estelar ----------

def atril():
    rng = np.random.default_rng(105)
    m = Malla("MIR-05_atril")
    cal = []
    for sx in (-1, 1):
        barra(m, (sx * 0.40, 0, 0.26), (sx * 0.36, 0.98, -0.04), 0.036, MADERA_OSC, MADERA_LUZ, 4)
        barra(m, (sx * 0.40, 0, -0.30), (sx * 0.36, 0.98, -0.04), 0.036, MADERA_OSC, MADERA_LUZ, 4)
    barra(m, (-0.39, 0.40, 0.14), (0.39, 0.40, 0.14), 0.026, MADERA, MADERA_LUZ, 4)
    fi = math.radians(38.0)
    der = np.array([1.0, 0.0, 0.0])
    arr = np.array([0.0, math.cos(fi), -math.sin(fi)])
    centro = np.array([0.0, 1.05, 0.02])
    n = tabla(m, centro, der, arr, 1.02, 0.66, 0.05, MADERA, MADERA_OSC)
    carta = mezclar(PAL["petroleo"], PAL["oscuro"], 0.30)
    c2 = centro + n * 0.030
    cara(m, [c2 - der * 0.45 - arr * 0.27, c2 + der * 0.45 - arr * 0.27, c2 + der * 0.45 + arr * 0.27, c2 - der * 0.45 + arr * 0.27],
         interior=centro, cols=[carta, osc(carta, -0.25), mezclar(carta, PAL["petroleo"], 0.6), carta])
    # estrellas y una linea de constelacion (sin texto)
    estrellas = [(-0.32, 0.12), (-0.18, -0.05), (-0.02, 0.06), (0.14, -0.10), (0.30, 0.02), (0.22, 0.17),
                 (-0.26, -0.17), (0.05, 0.19), (0.36, -0.18), (-0.38, -0.02)]
    c3 = centro + n * 0.034
    for i, (u, v) in enumerate(estrellas):
        r = 0.022 if i < 5 else 0.013
        p = c3 + der * u + arr * v
        cara(m, [p - der * r, p - arr * r, p + der * r, p + arr * r], PAL["brillo"] if i < 5 else PAL["crema"], interior=centro)
    for (u0, v0), (u1, v1) in zip(estrellas[:4], estrellas[1:5]):
        a, b = c3 + der * u0 + arr * v0 - n * 0.002, c3 + der * u1 + arr * v1 - n * 0.002
        lado = np.cross(n, b - a)
        lado = lado / np.linalg.norm(lado) * 0.004
        cara(m, [a - lado, b - lado, b + lado, a + lado], mezclar(PAL["cian_medio"], carta, 0.35), interior=centro)
    # listones del marco y repisa
    bloque(m, (0, 0.80, 0.24), (1.02, 0.04, 0.08), MADERA_LUZ, rng=rng)
    # farolito colgado a la izquierda (luz calida)
    barra(m, (-0.50, 1.36, -0.16), (-0.66, 1.40, -0.16), 0.016, METAL, METAL_LUZ, 4)
    barra(m, (-0.64, 1.40, -0.16), (-0.64, 1.32, -0.16), 0.008, METAL, METAL, 3, tapas=False)
    torno(m, [(0.0, 1.33, METAL), (0.075, 1.29, METAL_LUZ), (0.06, 1.27, METAL)], 5, rng, centro=(-0.64, 0, -0.16), tapa=False)
    torno(m, [(0.055, 1.09, METAL), (0.065, 1.11, METAL_LUZ), (0.0, 1.11, METAL_LUZ)], 5, rng, centro=(-0.64, 0, -0.16), tapa=False)
    b_calido(cal, (-0.64, 1.19, -0.16), 0.075)
    guardar("MIR-05", [("MIR-05_atril", [m], (0, 0, 0))], cal)


# ---------- MIR-06 banca ----------

def banca():
    rng = np.random.default_rng(106)
    m = Malla("MIR-06_banca")
    for sx in (-1, 1):
        bloque(m, (sx * 0.62, 0.0, 0.0), (0.24, 0.38, 0.44), PIEDRA, rng=rng, luz_t=0.15)
        bloque(m, (sx * 0.62, 0.0, 0.0), (0.30, 0.08, 0.50), PIEDRA_MALVA, rng=rng)
    bloque(m, (0.0, 0.38, 0.0), (1.74, 0.13, 0.52), PIEDRA_LUZ, rng=rng, luz_t=0.3, sombra_t=0.2)
    # manta de rayas doblada sobre un extremo (v2: coral, crema, dorado y petroleo, como un tejido de colores)
    rayas = [mezclar(PAL["coral"], PAL["terracota"], 0.25), cla(PAL["piedra_clara"], 0.6), PAL["dorado"],
             mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.10), mezclar(PAL["coral"], PAL["terracota"], 0.25), cla(PAL["sol"], 0.3)]
    x = 0.22
    for i in range(6):
        c = rayas[i]
        w = 0.09
        y, z0, z1 = 0.518, -0.27, 0.27
        cara(m, [(x, y, z0), (x + w, y, z0), (x + w, y, z1), (x, y, z1)], c, arriba=True)
        cara(m, [(x, y, z1), (x + w, y, z1), (x + w, 0.22, z1 + 0.012), (x, 0.22, z1 + 0.012)], interior=(x, 0.3, 0),
             cols=[c, c, osc(c, 0.35), osc(c, 0.35)])
        cara(m, [(x, y, z0), (x + w, y, z0), (x + w, 0.30, z0 - 0.012), (x, 0.30, z0 - 0.012)], interior=(x, 0.3, 0),
             cols=[c, c, osc(c, 0.35), osc(c, 0.35)])
        x += w
    guardar("MIR-06", [("MIR-06_banca", [m], (0, 0, 0))])


# ---------- MIR-07 poste de la guirnalda ----------

ALTO_AMARRE = 2.30   # altura a la que se ata el cable (lo usa mirador_escena.py)


def poste_guirnalda():
    rng = np.random.default_rng(107)
    m = Malla("MIR-07_poste")
    bloque(m, (0, 0, 0), (0.32, 0.30, 0.32), PIEDRA_MALVA, rng=rng, luz_t=0.2)
    barra(m, (0, 0.28, 0), (0, 2.46, 0), 0.068, MADERA_OSC, MADERA_LUZ, 5, r1=0.058)
    cuerda = cla(PAL["tierra2"], 0.55)
    torno(m, [(0.066, 2.20, osc(cuerda, 0.2)), (0.082, 2.24, cuerda), (0.082, 2.34, cuerda), (0.064, 2.38, cuerda)], 6, rng, tapa=False)
    guardar("MIR-07", [("MIR-07_poste", [m], (0, 0, 0))])


# ---------- MIR-09 mesa del club ----------

ALTO_MESA = 0.755


def mesa_club():
    rng = np.random.default_rng(109)
    m = Malla("MIR-09_mesa")
    e = Malla("MIR-09_brillo", "Emisivo")
    tablero = mezclar(PAL["tierra2"], PAL["sol"], 0.25)
    bloque(m, (0, 0.70, 0), (1.56, 0.055, 0.78), tablero, rng=rng, luz_t=0.3, sombra_t=0.25)
    for sx in (-1, 1):
        # patas plegables en X
        barra(m, (sx * 0.62, 0, -0.30), (sx * 0.62, 0.70, 0.30), 0.024, METAL, METAL_LUZ, 4)
        barra(m, (sx * 0.62, 0, 0.30), (sx * 0.62, 0.70, -0.30), 0.024, METAL, METAL_LUZ, 4)
    barra(m, (-0.62, 0.35, 0), (0.62, 0.35, 0), 0.016, METAL, METAL_LUZ, 4, tapas=False)
    # v2: manta tejida de colores doblada sobre el extremo izquierdo; cuelga por delante (+Z)
    franjas = [mezclar(PAL["coral"], PAL["terracota"], 0.2), PAL["dorado"], cla(PAL["piedra_clara"], 0.55),
               mezclar(PAL["petroleo"], PAL["cian_medio"], 0.0), mezclar(PAL["coral"], PAL["terracota"], 0.2)]
    x0, x1 = -0.78, -0.33
    for i, c in enumerate(franjas):
        za, zb = -0.40 + 0.80 * i / len(franjas), -0.40 + 0.80 * (i + 1) / len(franjas)
        cara(m, [(x0, 0.7563, za), (x1, 0.7563, za), (x1, 0.7563, zb), (x0, 0.7563, zb)], c, arriba=True)
    for i, c in enumerate(franjas[:3]):
        xa, xb = x0 + (x1 - x0) * i / 3, x0 + (x1 - x0) * (i + 1) / 3
        cara(m, [(xa, 0.7563, 0.40), (xb, 0.7563, 0.40), (xb, 0.50, 0.415), (xa, 0.50, 0.415)], interior=(xa, 0.6, 0.0),
             cols=[c, c, osc(c, 0.35), osc(c, 0.35)])
        cara(m, [(x0 - 0.002, 0.7563, -0.40 + 0.8 * i / 3), (x0 - 0.002, 0.7563, -0.40 + 0.8 * (i + 1) / 3),
                 (x0 - 0.015, 0.46, -0.40 + 0.8 * (i + 1) / 3), (x0 - 0.015, 0.46, -0.40 + 0.8 * i / 3)],
             interior=(0.0, 0.6, 0.0), cols=[franjas[i + 1], franjas[i + 1], osc(franjas[i + 1], 0.35), osc(franjas[i + 1], 0.35)])
    # mantel de papel con un circulo (carta del cielo), sin texto
    papel = cla(PAL["piedra_clara"], 0.65)
    cara(m, [(-0.10, 0.757, -0.30), (0.26, 0.757, -0.30), (0.26, 0.757, -0.04), (-0.10, 0.757, -0.04)], papel, arriba=True)
    torno(m, [(0.10, 0.759, PAL["petroleo"]), (0.085, 0.759, PAL["petroleo"])], 10, None, centro=(0.08, 0, -0.17), tapa=False)
    # las cuatro partes del satelite: panel (energia), radio, antena y computadora
    y = 0.756
    bloque(m, (-0.52, y, 0.24), (0.20, 0.012, 0.11), mezclar(PAL["petroleo"], PAL["oscuro"], 0.2), ry=0.2, rng=rng, luz_t=0.0)
    bloque(m, (-0.22, y, 0.26), (0.10, 0.05, 0.07), PAL["coral"], ry=-0.25, rng=rng)
    barra(m, (0.02, y + 0.012, 0.22), (0.20, y + 0.012, 0.30), 0.008, METAL_LUZ, PAL["piedra_clara"], 4)
    bloque(m, (0.10, y, 0.27), (0.03, 0.025, 0.03), METAL, rng=rng)
    bloque(m, (0.52, y, 0.27), (0.13, 0.014, 0.09), mezclar(PAL["hierba_sombra"], PAL["cian_medio"], 0.35), ry=0.15, rng=rng)
    bloque(e, (0.52, y + 0.014, 0.27), (0.03, 0.006, 0.03), PAL["cian"], ry=0.15, sombra_t=0.0)
    # caja de piezas debajo
    bloque(m, (0.25, 0.0, -0.05), (0.40, 0.26, 0.30), cla(PAL["tierra2"], 0.25), ry=0.3, rng=rng)
    guardar("MIR-09", [("MIR-09_mesa", [m, e], (0, 0, 0))])


# ---------- TAL-11 maqueta de satelite ----------

def maqueta():
    rng = np.random.default_rng(111)
    m = Malla("TAL-11_maqueta")
    e = Malla("TAL-11_brillo", "Emisivo")
    lado = 0.11                      # el cubo; cada panel mide 2,7 veces el lado (ficha «pegaso»: 10 cm y 27 cm)
    panel = lado * 2.7
    torno(m, [(0.085, 0.0, MADERA_OSC), (0.075, 0.022, MADERA_LUZ)], 7, rng)
    barra(m, (0, 0.02, 0), (0, 0.20, 0), 0.008, METAL, METAL_LUZ, 4, tapas=False)
    cy = 0.20
    cubo = mezclar(PAL["piedra_clara"], PAL["crema"], 0.3)
    bloque(m, (0, cy, 0), (lado, lado, lado), cubo, ry=0.0, rng=rng, sin_base=False, luz_t=0.3)
    azul = mezclar(PAL["petroleo"], PAL["oscuro"], 0.25)
    for sx in (-1, 1):
        x0, x1 = sx * lado / 2, sx * (lado / 2 + panel)
        yb, yt = cy + lado, cy + lado + 0.012
        # panel abisagrado en la arista de arriba, con tres celdas
        for k in range(3):
            xa = x0 + (x1 - x0) * (k / 3 + 0.02)
            xb = x0 + (x1 - x0) * ((k + 1) / 3 - 0.02)
            caja(m, (min(xa, xb), yb, -lado / 2), (max(xa, xb), yt, lado / 2), mezclar(azul, PAL["petroleo"], 0.25 * k), 0.2, 0.0, rng, sin_base=False)
        caja(m, (min(x0, x1), yb - 0.004, -lado / 2 - 0.006), (max(x0, x1), yb, lado / 2 + 0.006), METAL_LUZ, 0.2, 0.0, rng, sin_base=False)
    barra(m, (0, cy + lado, 0.03), (0.02, cy + lado + 0.16, 0.03), 0.004, METAL_LUZ, PAL["piedra_clara"], 3)
    bloque(e, (0.0, cy + lado * 0.45, lado / 2 + 0.001), (0.022, 0.022, 0.004), PAL["cian"], sombra_t=0.0)
    guardar("TAL-11", [("TAL-11_maqueta", [m, e], (0, 0, 0))])


# ---------- TAL-18 portatil del club ----------

def portatil():
    rng = np.random.default_rng(115)
    m = Malla("TAL-18_portatil")
    e = Malla("TAL-18_pantalla", "Emisivo")
    bloque(m, (0, 0, 0), (0.34, 0.018, 0.24), METAL, rng=rng, luz_t=0.2)
    cara(m, [(-0.14, 0.0185, -0.09), (0.14, 0.0185, -0.09), (0.14, 0.0185, 0.04), (-0.14, 0.0185, 0.04)], METAL_LUZ, arriba=True)
    fi = math.radians(18.0)
    der = np.array([1.0, 0.0, 0.0])
    arr = np.array([0.0, math.cos(fi), -math.sin(fi)])
    centro = np.array([0.0, 0.018, -0.12]) + arr * 0.115
    n = tabla(m, centro, der, arr, 0.34, 0.23, 0.012, METAL, METAL)
    c2 = centro + n * 0.0075
    cara(e, [c2 - der * 0.155 - arr * 0.10, c2 + der * 0.155 - arr * 0.10, c2 + der * 0.155 + arr * 0.10, c2 - der * 0.155 + arr * 0.10],
         PAL["cian_medio"], interior=centro)
    guardar("TAL-18", [("TAL-18_portatil", [m, e], (0, 0, 0))])


# ---------- TAL-10 taburete ----------

def taburete():
    rng = np.random.default_rng(110)
    m = Malla("TAL-10_taburete")
    torno(m, [(0.17, 0.41, MADERA_OSC), (0.18, 0.46, MADERA_LUZ)], 7, rng)
    for k in range(3):
        a = math.radians(30 + 120 * k)
        barra(m, (0.19 * math.cos(a), 0, 0.19 * math.sin(a)), (0.11 * math.cos(a), 0.42, 0.11 * math.sin(a)), 0.022, MADERA_OSC, MADERA, 4)
    guardar("TAL-10", [("TAL-10_taburete", [m], (0, 0, 0))])


# ---------- MIR-10 porton del cerro ----------

MEDIO_PORTON = 1.25      # los pilares van en z = +-1,25 (hueco libre de 2,1 m)


def porton():
    rng = np.random.default_rng(120)
    pil = Malla("MIR-10_pilares")
    cal = []
    for sz in (-1, 1):
        z = sz * MEDIO_PORTON
        bloque(pil, (0, 0, z), (0.46, 0.14, 0.46), PIEDRA_MALVA, rng=rng)
        bloque(pil, (0, 0.14, z), (0.40, 1.30, 0.40), PIEDRA, rng=rng, luz_t=0.15)
        bloque(pil, (0, 1.44, z), (0.50, 0.08, 0.50), PIEDRA_LUZ, rng=rng, luz_t=0.3)
        # farolito sobre cada pilar
        torno(pil, [(0.09, 1.52, METAL), (0.07, 1.56, METAL_LUZ)], 5, rng, centro=(0, 0, z))
        for k in range(4):
            a = math.radians(45 + 90 * k)
            barra(pil, (0.075 * math.cos(a), 1.56, z + 0.075 * math.sin(a)), (0.075 * math.cos(a), 1.80, z + 0.075 * math.sin(a)), 0.008, METAL, METAL_LUZ, 3, tapas=False)
        torno(pil, [(0.12, 1.80, METAL), (0.0, 1.92, METAL_LUZ)], 4, rng, centro=(0, 0, z), giro=math.pi / 4)
        b_calido(cal, (0, 1.68, z), 0.065)
    hojas = []
    for nombre, sz in (("MIR-10_hoja_n", 1), ("MIR-10_hoja_s", -1)):
        h = Malla(nombre)
        # bisagra en el origen del nodo; la hoja se extiende 1,0 m hacia el centro del hueco
        for k in range(5):
            z0 = sz * (0.03 + k * 0.196)
            z1 = sz * (0.03 + k * 0.196 + 0.18)
            alto = 1.22 + 0.05 * math.sin(k * 1.1 + (0 if sz > 0 else 2))
            caja(h, (-0.025, 0.12, min(z0, z1)), (0.025, alto, max(z0, z1)), MADERA if k % 2 else MADERA_LUZ, 0.35, 0.1, rng, sin_base=False)
        for y in (0.30, 1.02):
            caja(h, (-0.045, y, min(0.0, sz * 1.0)), (0.045, y + 0.09, max(0.0, sz * 1.0)), MADERA_OSC, 0.3, 0.1, rng, sin_base=False)
        for y in (0.34, 1.06):
            caja(h, (-0.05, y, min(0.0, sz * 0.16)), (0.05, y + 0.03, max(0.0, sz * 0.16)), METAL, 0.2, 0.2, rng, sin_base=False)
        hojas.append((nombre, [h], (0.0, 0.0, -sz * (MEDIO_PORTON - 0.21))))
    guardar("MIR-10", [("MIR-10_pilares", [pil], (0, 0, 0))] + hojas, cal)


# ---------- ARQ-09 farol ----------

def farol():
    rng = np.random.default_rng(209)
    m = Malla("ARQ-09_farol")
    cal = []
    torno(m, [(0.15, 0.0, METAL), (0.11, 0.14, METAL_LUZ), (0.05, 0.24, METAL)], 6, rng, tapa=False)
    torno(m, [(0.045, 0.24, METAL), (0.034, 2.00, METAL_LUZ)], 5, rng, tapa=False)
    torno(m, [(0.034, 2.00, METAL), (0.13, 2.06, METAL_LUZ), (0.11, 2.08, METAL_LUZ)], 6, rng)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        barra(m, (0.10 * math.cos(a), 2.08, 0.10 * math.sin(a)), (0.13 * math.cos(a), 2.42, 0.13 * math.sin(a)), 0.010, METAL, METAL_LUZ, 3, tapas=False)
    torno(m, [(0.18, 2.42, METAL), (0.06, 2.58, METAL_LUZ), (0.0, 2.68, METAL_LUZ)], 4, rng, giro=math.pi / 4)
    b_calido(cal, (0, 2.25, 0), 0.095)
    guardar("ARQ-09", [("ARQ-09_farol", [m], (0, 0, 0))], cal)


# ---------- URB-07 maceta ----------

def maceta():
    rng = np.random.default_rng(307)
    m = Malla("URB-07_maceta")
    terra = PAL["terracota"]
    torno(m, [(0.20, 0.0, osc(terra, 0.35)), (0.30, 0.40, terra), (0.34, 0.41, cla(terra, 0.2)), (0.34, 0.47, cla(terra, 0.3)),
              (0.28, 0.47, cla(terra, 0.15)), (0.27, 0.42, mezclar(PAL["madera2"], PAL["tierra2"], 0.3))], 8, rng)
    guardar("URB-07", [("URB-07_maceta", [m], (0, 0, 0))])


# ---------- ARQ-14 casas del barrio de fondo ----------

def casa(nombre, w, d, h, pared, techo, semilla, pisos):
    rng = np.random.default_rng(semilla)
    m = Malla(nombre)
    cal = []
    bloque(m, (0, 0, 0), (w, h, d), pared, rng=rng, sombra_t=0.40, luz_t=0.15)
    # techo a dos aguas con la cumbrera a lo largo de X, pintado por paneles
    a = 0.30
    x0, x1, z0, z1 = -w / 2 - a, w / 2 + a, -d / 2 - a, d / 2 + a
    yb, yc = h - 0.06, h + d * 0.30
    cols = max(3, int(round(w / 1.2)))
    for lado in (1, -1):
        zb = z1 if lado > 0 else z0
        for i in range(cols):
            xa, xb = x0 + (x1 - x0) * i / cols, x0 + (x1 - x0) * (i + 1) / cols
            for j in range(2):
                ta, tb = j / 2, (j + 1) / 2
                v = 1.0 + rng.normal(0, 0.07)
                ca, cb = mezclar(osc(techo, 0.30), techo, ta) * v, mezclar(osc(techo, 0.30), cla(techo, 0.2), tb) * v
                pa = [(xa, yb + (yc - yb) * ta, zb * (1 - ta)), (xb, yb + (yc - yb) * ta, zb * (1 - ta)),
                      (xb, yb + (yc - yb) * tb, zb * (1 - tb)), (xa, yb + (yc - yb) * tb, zb * (1 - tb))]
                cara(m, pa, arriba=True, cols=[ca, ca, cb, cb])
    for sx in (-1, 1):
        cara(m, [(sx * w / 2, h, -d / 2), (sx * w / 2, h, d / 2), (sx * w / 2, yc - 0.10, 0)], cla(pared, 0.1), interior=(0, h, 0))
    # ventanas: las encendidas van a la lista de luces calidas; las apagadas, azul oscuro
    marco_c = osc(pared, 0.45)

    def ventana(cx, cy, eje, sx=1, ancho=0.62, alto=0.82, prob=0.62):
        if eje == "z":
            zf = d / 2 + 0.015
            cara(m, [(cx - ancho / 2 - 0.07, cy - alto / 2 - 0.07, zf), (cx + ancho / 2 + 0.07, cy - alto / 2 - 0.07, zf),
                     (cx + ancho / 2 + 0.07, cy + alto / 2 + 0.07, zf), (cx - ancho / 2 - 0.07, cy + alto / 2 + 0.07, zf)], marco_c, interior=(0, cy, 0))
            pts = [(cx - ancho / 2, cy - alto / 2, zf + 0.02), (cx + ancho / 2, cy - alto / 2, zf + 0.02),
                   (cx + ancho / 2, cy + alto / 2, zf + 0.02), (cx - ancho / 2, cy + alto / 2, zf + 0.02)]
            nrm = (0, 0, 1)
        else:
            xf = sx * (w / 2 + 0.015)
            cara(m, [(xf, cy - alto / 2 - 0.07, cx - ancho / 2 - 0.07), (xf, cy - alto / 2 - 0.07, cx + ancho / 2 + 0.07),
                     (xf, cy + alto / 2 + 0.07, cx + ancho / 2 + 0.07), (xf, cy + alto / 2 + 0.07, cx - ancho / 2 - 0.07)], marco_c, interior=(0, cy, cx))
            xf += sx * 0.02
            pts = [(xf, cy - alto / 2, cx - ancho / 2), (xf, cy - alto / 2, cx + ancho / 2),
                   (xf, cy + alto / 2, cx + ancho / 2), (xf, cy + alto / 2, cx - ancho / 2)]
            nrm = (sx, 0, 0)
        if rng.random() < prob:
            q_calido(cal, pts, nrm)
        else:
            cara(m, pts, VIDRIO_APAGADO, interior=(0, cy, 0) if eje == "z" else (0, cy, cx))

    n_frente = max(2, int(w / 1.6))
    for p in range(pisos):
        cy = 1.55 + p * 2.55
        for i in range(n_frente):
            cx = -w / 2 + w * (i + 0.5) / n_frente
            if p == 0 and i == n_frente // 2:
                # puerta
                caja(m, (cx - 0.38, 0.0, d / 2), (cx + 0.38, 1.9, d / 2 + 0.05), MADERA, 0.35, 0.1, rng)
                continue
            ventana(cx, cy, "z")
        for sx in (-1, 1):
            for cz in (-d / 4, d / 4):
                ventana(cz, cy, "x", sx)
    return m, cal


def casas():
    datos = [
        ("ARQ-14_a", 5.0, 4.4, 5.5, mezclar(PAL["crema"], PAL["tierra1"], 0.35), PAL["terracota"], 131, 2),
        ("ARQ-14_b", 5.6, 4.2, 3.1, mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.50), TEJA, 132, 1),
        ("ARQ-14_c", 4.2, 4.6, 5.3, mezclar(PAL["sol"], PAL["tierra1"], 0.55), mezclar(PAL["terracota"], PAL["madera1"], 0.3), 133, 2),
    ]
    nodos, cal_todas = [], {}
    for nombre, w, d, h, pared, techo, semilla, pisos in datos:
        m, cal = casa(nombre, w, d, h, pared, techo, semilla, pisos)
        nodos.append((nombre, [m], (0, 0, 0)))
        cal_todas[nombre] = cal
    guardar("ARQ-14", nodos)
    for nombre, cal in cal_todas.items():
        CALIDOS[nombre] = cal


# ---------- VEG-15 copa de arbol de fondo ----------

def copa():
    rng = np.random.default_rng(415)
    pts = fibonacci(14) * rng.uniform(0.78, 1.12, (14, 1)) * np.array([1.25, 0.95, 1.15])
    pts[:, 1] -= pts[:, 1].min()
    pts[pts[:, 1] < 0.35, 1] *= 0.4
    m = solido_facetado("VEG-15_copa", pts, osc(PAL["hierba_sombra"], 0.55), mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.15),
                        mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.55), rng, var=0.07)
    guardar("VEG-15", [("VEG-15_copa", [m], (0, 0, 0))])


# ---------- VEG-08 buganvilla ----------

def buganvilla():
    rng = np.random.default_rng(408)
    f = Malla("VEG-08_buganvilla", "Follaje")
    t = Malla("VEG-08_tallos")
    # cascada que cuelga de un muro: nace en (0, 0, 0) y cae hacia -Y por delante (+Z)
    for k in range(5):
        x = rng.uniform(-0.7, 0.7)
        pts = [np.array([x * 0.3, 0.05, -0.05]), np.array([x * 0.7, 0.10, 0.22]), np.array([x, -0.5, 0.36]), np.array([x * 1.1, -1.2, 0.30])]
        for a, b in zip(pts[:-1], pts[1:]):
            barra(t, a, b, 0.022, PAL["madera2"], MADERA_OSC, 3, tapas=False)
    for _ in range(120):
        u = rng.uniform(-1, 1)
        y = 0.28 - abs(rng.normal(0, 0.75))
        if y < -1.7:
            continue
        ancho = 1.05 * (1.0 - 0.35 * max(0.0, -y) / 1.7)
        base = np.array([u * ancho, y, 0.20 + 0.20 * math.cos(u * 1.3) + rng.uniform(-0.08, 0.10)])
        normal = np.array([u * 0.5 + rng.normal(0, 0.25), 0.55 + rng.normal(0, 0.2), 1.0])
        direccion = np.array([rng.normal(0, 0.6), -0.6 + rng.normal(0, 0.4), 0.25])
        if rng.random() < 0.60:
            # v2b: bracteas magenta (excepcion propuesta), mas claras arriba, donde les da la luz
            rosa = mezclar(MAGENTA_LUZ, MAGENTA, rng.uniform(0, 1.0) * (0.4 + 0.6 * min(1.0, -y / 1.2 + 0.3)))
            for _ in range(2):
                c = base + rng.normal(0, 0.06, 3)
                flor(f, c, normal, rng.uniform(0.08, 0.12), rosa, mezclar(rosa, PAL["crema"], 0.55), petalos=3, rng=rng)
        else:
            verde = mezclar(VERDE_OSC, VERDE, rng.uniform(0, 1))
            hoja(f, base, direccion, normal, rng.uniform(0.16, 0.24), rng.uniform(0.09, 0.13), VERDE_OSC, verde)
    guardar("VEG-08", [("VEG-08_buganvilla", [f, t], (0, 0, 0))])


# ---------- v2: MIR-11 pizarra de constelaciones (ID nuevo) ----------

PIZARRA_FI = 12.0                     # el tablero se inclina 12 grados hacia atras
PIZARRA_CENTRO = (0.0, 1.10, 0.0)     # centro del tablero (frente a +Z)
PIZARRA_TAM = (1.04, 0.74)
# estrellas de tiza (u, v en metros sobre el tablero); las tres primeras son las que se unen en el juego:
# las puntas de la creciente y el borde iluminado, que apunta hacia abajo (ficha luna_sonriente)
# v2b: mas dos estrellas senuelo (indices 3 y 4) que no estan en la creciente: la jugadora elige en orden
PIZARRA_ESTRELLAS = [(-0.24, 0.10), (0.0, -0.12), (0.24, 0.10), (-0.07, 0.25), (0.14, -0.01)]
PIZARRA_HORIZONTE = -0.27


def pizarra():
    rng = np.random.default_rng(111)
    m = Malla("MIR-11_pizarra")
    fi = math.radians(PIZARRA_FI)
    der = np.array([1.0, 0.0, 0.0])
    arr = np.array([0.0, math.cos(fi), -math.sin(fi)])
    centro = np.array(PIZARRA_CENTRO)
    # caballete pintado (v2b): patas dorado tierra y marco coral, para no confundirla con el atril de madera
    pata, pata_luz = mezclar(PAL["dorado"], PAL["tierra2"], 0.45), mezclar(PAL["dorado"], PAL["crema"], 0.25)
    for sx in (-1, 1):
        barra(m, (sx * 0.46, 0.0, 0.10), centro + der * sx * 0.44 + arr * 0.40 - (0, 0, 0.04), 0.032, pata, pata_luz, 4)
    barra(m, (0.0, 0.0, -0.46), centro + arr * 0.42 - (0, 0, 0.06), 0.030, pata, pata_luz, 4)
    marco_c = mezclar(PAL["coral"], PAL["terracota"], 0.25)
    n = tabla(m, centro, der, arr, PIZARRA_TAM[0] + 0.12, PIZARRA_TAM[1] + 0.12, 0.045, marco_c, osc(marco_c, 0.3))
    pizarra_c = mezclar(PAL["petroleo"], PAL["oscuro"], 0.55)
    c2 = centro + n * 0.0235
    w, h = PIZARRA_TAM[0] / 2, PIZARRA_TAM[1] / 2
    cara(m, [c2 - der * w - arr * h, c2 + der * w - arr * h, c2 + der * w + arr * h, c2 - der * w + arr * h], interior=centro,
         cols=[pizarra_c, osc(pizarra_c, 0.15), mezclar(pizarra_c, PAL["petroleo"], 0.25), pizarra_c])
    tiza = cla(PAL["piedra_clara"], 0.35)
    c3 = c2 + n * 0.002
    # horizonte de tiza con dos lomas (el cerro) y estrellas de fondo
    hz = [(-0.48, PIZARRA_HORIZONTE + 0.02), (-0.28, PIZARRA_HORIZONTE + 0.07), (-0.10, PIZARRA_HORIZONTE),
          (0.18, PIZARRA_HORIZONTE + 0.04), (0.48, PIZARRA_HORIZONTE)]
    for (u0, v0), (u1, v1) in zip(hz[:-1], hz[1:]):
        a, b = c3 + der * u0 + arr * v0, c3 + der * u1 + arr * v1
        lado = np.cross(n, b - a)
        lado = lado / np.linalg.norm(lado) * 0.007
        cara(m, [a - lado, b - lado, b + lado, a + lado], mezclar(tiza, pizarra_c, 0.25), interior=centro)
    for _ in range(16):
        u, v = rng.uniform(-0.47, 0.47), rng.uniform(-0.18, 0.33)
        if min(math.hypot(u - a, v - b) for a, b in PIZARRA_ESTRELLAS) < 0.09:
            continue
        r = rng.uniform(0.007, 0.013)
        p = c3 + der * u + arr * v
        cara(m, [p - der * r, p - arr * r, p + der * r, p + arr * r], mezclar(tiza, pizarra_c, rng.uniform(0.2, 0.5)), interior=centro)
    # repisa de la tiza
    bloque(m, centro - arr * (h + 0.07) + n * 0.04 - (0, 0.02, 0), (PIZARRA_TAM[0], 0.03, 0.07), MADERA_LUZ, rng=rng)
    bloque(m, centro - arr * (h + 0.05) + n * 0.05 + der * 0.30, (0.06, 0.016, 0.016), tiza, rng=rng)
    guardar("MIR-11", [("MIR-11_pizarra", [m], (0, 0, 0))])


def pizarra_mundo(pos, giro_grados, u, v, despegue=0.004):
    """Punto (u, v) del tablero de MIR-11 en coordenadas locales del modelo (para el layout)."""
    fi = math.radians(PIZARRA_FI)
    der = np.array([1.0, 0.0, 0.0])
    arr = np.array([0.0, math.cos(fi), -math.sin(fi)])
    n = np.cross(der, arr)
    p = np.array(PIZARRA_CENTRO) + n * (0.0235 + despegue) + der * u + arr * v
    return p


# ---------- v2: VEG-09 cayena en maceta (roja y magenta) ----------

def cayena():
    """Arbusto de cayena (hibisco) pequeno para las macetas: hojas verdes y flores de cinco petalos."""
    nodos = []
    for nombre, flor_c, semilla in (("VEG-09_roja", mezclar(PAL["coral"], PAL["terracota"], 0.35), 409),
                                    ("VEG-09_magenta", MAGENTA_LUZ, 419),
                                    ("VEG-09_blanca", BLANCO_FLOR, 429)):
        rng = np.random.default_rng(semilla)
        f = Malla(nombre, "Follaje")
        for _ in range(46):
            ang = rng.uniform(0, 2 * math.pi)
            alto = rng.uniform(0.05, 0.62)
            r = 0.30 * (1.0 - 0.45 * (alto / 0.62) ** 2) * rng.uniform(0.4, 1.0)
            base = np.array([math.cos(ang) * r * 0.4, alto * 0.6, math.sin(ang) * r * 0.4])
            direccion = np.array([math.cos(ang), 0.45 + rng.normal(0, 0.2), math.sin(ang)])
            normal = np.array([math.cos(ang) * 0.4, 1.0, math.sin(ang) * 0.4])
            verde = mezclar(VERDE_OSC, VERDE, rng.uniform(0.1, 1.0))
            hoja(f, base, direccion, normal, rng.uniform(0.16, 0.24), rng.uniform(0.09, 0.12), VERDE_OSC, verde)
        # v2b: mas flores y mas grandes, para que el acento se lea desde la camara alta
        for _ in range(15):
            ang = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(0.06, 0.28)
            c = np.array([math.cos(ang) * r, rng.uniform(0.36, 0.66), math.sin(ang) * r])
            nrm = np.array([math.cos(ang) * 0.6, 1.0, math.sin(ang) * 0.6 + 0.5])
            flor(f, c, nrm, rng.uniform(0.09, 0.12), flor_c, mezclar(PAL["dorado"], flor_c, 0.3), petalos=5, rng=rng)
        nodos.append((nombre, [f], (0, 0, 0)))
    guardar("VEG-09", nodos)


# ---------- v2: recolectables COL-12 (carta estelar), COL-08 (antena de varilla) y COL-06 (cable de cobre) ----------

def carta_estelar():
    rng = np.random.default_rng(612)
    m = Malla("COL-12_carta")
    papel = cla(PAL["piedra_clara"], 0.55)
    azul = mezclar(PAL["petroleo"], PAL["oscuro"], 0.35)
    # hoja doblada en dos, un poco abierta, con la cara de dentro azul y estrellas de tinta clara
    a0, a1 = math.radians(8), math.radians(22)
    for s, ang in ((-1, a0), (1, a1)):
        x1 = s * 0.20 * math.cos(ang)
        y1 = 0.20 * math.sin(ang)
        cara(m, [(0, 0.004, -0.14), (x1, y1 + 0.004, -0.14), (x1, y1 + 0.004, 0.14), (0, 0.004, 0.14)], arriba=True,
             cols=[azul, mezclar(azul, PAL["petroleo"], 0.4), mezclar(azul, PAL["petroleo"], 0.4), azul])
        cara(m, [(0, 0.0, -0.14), (x1, y1, -0.14), (x1, y1, 0.14), (0, 0.0, 0.14)], papel, interior=(x1 * 0.5, y1 + 1.0, 0))
        for _ in range(5):
            t = rng.uniform(0.15, 0.85)
            z = rng.uniform(-0.11, 0.11)
            p = np.array([x1 * t, y1 * t + 0.006, z])
            r = rng.uniform(0.008, 0.014)
            cara(m, [p + (-r, 0, 0), p + (0, 0, r), p + (r, 0, 0), p + (0, 0, -r)], PAL["crema"], arriba=True)
    guardar("COL-12", [("COL-12_carta", [m], (0, 0, 0))])


def antena_varilla():
    rng = np.random.default_rng(608)
    m = Malla("COL-08_antena")
    # base con rotula y tres tramos telescopicos, tumbada en el suelo con una pizca de inclinacion
    bloque(m, (0, 0, 0), (0.07, 0.05, 0.07), METAL, rng=rng, luz_t=0.2)
    p = np.array([0.0, 0.035, 0.0])
    d = np.array([math.cos(math.radians(10)), math.sin(math.radians(6)), math.sin(math.radians(10))])
    radios = [0.012, 0.009, 0.006]
    for i, r in enumerate(radios):
        q = p + d * 0.16
        barra(m, p, q, r, METAL_LUZ if i % 2 == 0 else cla(METAL_LUZ, 0.3), cla(METAL_LUZ, 0.25), 5)
        p = q
    torno(m, [(0.0, -0.012, PAL["dorado"]), (0.014, 0.0, PAL["dorado"]), (0.0, 0.012, cla(PAL["dorado"], 0.3))], 5, rng, centro=tuple(p))
    guardar("COL-08", [("COL-08_antena", [m], (0, 0, 0))])


def cable_cobre():
    rng = np.random.default_rng(606)
    m = Malla("COL-06_cable")
    cobre, cobre_luz = mezclar(PAL["terracota"], PAL["sol"], 0.45), mezclar(PAL["sol"], PAL["crema"], 0.35)
    # rollo de cable: tres vueltas como toro facetado
    for k, rr in enumerate((0.085, 0.072, 0.096)):
        anillo = [np.array([math.cos(a) * rr, 0.018 + 0.012 * k, math.sin(a) * rr]) for a in np.linspace(0, 2 * math.pi, 11)]
        for a, b in zip(anillo[:-1], anillo[1:]):
            barra(m, a, b, 0.011, osc(cobre, 0.15), cobre_luz if k == 1 else cobre, 4, tapas=False)
    barra(m, (0.09, 0.02, 0.0), (0.17, 0.012, 0.05), 0.010, cobre, cobre_luz, 4)
    guardar("COL-06", [("COL-06_cable", [m], (0, 0, 0))])


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for fn in (faro, telescopio, binoculares, atril, banca, poste_guirnalda, mesa_club, maqueta, portatil, taburete,
               porton, farol, maceta, casas, copa, buganvilla, pizarra, cayena, carta_estelar, antena_varilla, cable_cobre):
        fn()
    (SALIDA / "calidos.json").write_text(json.dumps(CALIDOS, separators=(",", ":")), encoding="utf-8")
    for ident, n in RESUMEN.items():
        print(f"{ident}: {n} triangulos")
    print("total:", sum(RESUMEN.values()), "| luces calidas:", {k: len(v) for k, v in CALIDOS.items()})


if __name__ == "__main__":
    main()
