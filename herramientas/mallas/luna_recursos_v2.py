"""Recursos v2 de la Luna del sueno (zona «luna» del juego jugable v0), hechos por script.

PROVISIONAL: la Luna no tiene hoja de referencia ni concepto validado. La meta visual es el arte de carga
juego/interfaz/arte/carga_luna.jpg: rocas facetadas de caras grandes, la caja de carton con una Luna dibujada,
balizas cian y la etapa de descenso a lo lejos. Familia LUN. Escribe en juego/modelos/luna/<ID>.glb
(origen en el centro de la base, y = 0 en el suelo, +Z mira a la camara de juego):

  LUN-02  rocas: 8 variantes _a.._h (a-f gris lavanda claro, g-h basalto). Tamano unidad, para MultiMesh
  LUN-03  etapa de descenso GENERICA con detalle (la escalerilla mira a +Z). Sin letras, insignias ni banderas
  LUN-04  caja-capsula de carton: Luna de crayon en la cara +Z, aletas, escudo termico, ventanilla y linterna
  LUN-10  piedras pequenas: 4 variantes _a.._d de 4 a 7 triangulos, sin cara inferior. Tamano unidad
  LUN-11  bloques de eyecta: 3 variantes _a.._c, medio enterrados (bajan hasta y = -0,15). Tamano unidad
  LUN-12  baliza de camino (0,95 m): cuerpo «Facetado» y luz «Emisivo» en la misma malla
  LUN-13  instrumento A: estacion de medicion generica (caja dorada, panel, mastil con sensor, cable y disco)
  LUN-14  espejo de la Tierra: el reflejo va en la primitiva «Pintura» (color de vertice sin luz)
  LUN-15  soporte de herramientas (pinzas, cucharon, martillo) y 4 bolsas de muestra marcadas con puntos
  LUN-16  muestras sueltas: _a basalto, _b roca clara, _c terron de regolito. Tamano real (16 a 22 cm)
  LUN-17  instrumento B: tambor bajo con falda de lamina dorada, dos paneles y varilla de antena
  LUN-18  penascos grandes: _a bloque alto (2,6 x 2,0 x 2,0 m) y _b afloramiento bajo (3,0 x 1,1 x 2,2 m)
  LUN-19  camara de carton sobre tripode: el lente «Emisivo» mira a -Z

Estilo: facetas planas con degradado vertical (pie azul-gris, coronilla clara) y variacion de un 5 % por cara.
El color NO lleva luz direccional: la zona pinta la luz y la sombra con su shader segun la normal de mundo.
Solo mezclas de la paleta maestra; al guardar se comprueba que ningun color baje de 0,17 de luminancia sRGB
(nunca negro puro). Sin letras, cifras, insignias ni logotipos.

LUN-05 a LUN-09 siguen en herramientas/mallas/luna_modelos.py, de donde se importan las piezas y los tonos.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/luna_recursos_v2.py [--salida=<carpeta>] [--solo=LUN-03,LUN-04]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, Malla, casco_convexo, fibonacci, marco, mezclar, rot_eje, rot_y  # noqa: E402
from luna_modelos import (BLANCO, CARTON, CARTON_OSC, METAL, METAL_OSC, ORO, ORO_OSC, SOMBRA,  # noqa: E402
                          barra, bloque, disco, guardar, jit, octaedro, poli, torno)

GENERADOR = "herramientas/mallas/luna_recursos_v2.py"
SALIDA = None                      # None = juego/modelos/luna (la de luna_modelos)
INFORME: list[tuple] = []
W_LUMA = np.array([0.2126, 0.7152, 0.0722])
LUMA_MIN = 0.17
Y = np.array([0.0, 1.0, 0.0])

# ---------- tonos ----------
# v2b (2026-11-14, tras ver la zona en el motor): la roca clara se leia blanca y azul. Ahora coronilla calida,
# cuerpo malva gris y pie azul violeta, como las rocas del arte de carga (luz calida arriba, sombra fria abajo)
ROCA = mezclar(PAL["piedra_clara"], PAL["piedra"], 0.52)                                   # malva gris
ROCA_LUZ = mezclar(mezclar(PAL["piedra_clara"], PAL["crema"], 0.40), PAL["tierra1"], 0.12)  # coronilla calida
ROCA_PIE = mezclar(mezclar(PAL["petroleo"], PAL["piedra"], 0.30), PAL["piedra_osc"], 0.12)  # pie azul violeta
BASALTO = mezclar(PAL["piedra_osc"], PAL["petroleo"], 0.55)
BASALTO_LUZ = mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.42)
BASALTO_PIE = mezclar(BASALTO, PAL["oscuro"], 0.36)
FRESCA = mezclar(PAL["piedra_clara"], PAL["crema"], 0.20)                                  # roca recien partida
FRESCA_LUZ = mezclar(mezclar(PAL["piedra_clara"], PAL["crema"], 0.42), PAL["brillo"], 0.28)
FRESCA_PIE = mezclar(PAL["piedra"], PAL["petroleo"], 0.40)
TERRON = mezclar(PAL["piedra"], PAL["tierra2"], 0.32)                                      # tostado gris
ORO_NAR = mezclar(ORO, PAL["coral"], 0.38)                                                 # dorado anaranjado
GRIS = mezclar(METAL, BLANCO, 0.18)
GRIS_OSC = mezclar(METAL_OSC, PAL["piedra_osc"], 0.45)
QUEMADO = mezclar(METAL_OSC, PAL["oscuro"], 0.35)
PANEL_SOLAR = mezclar(PAL["petroleo"], PAL["oscuro"], 0.42)
PANEL_SOLAR_LUZ = mezclar(PAL["petroleo"], PAL["cian_medio"], 0.22)
NOCHE = mezclar(PAL["petroleo"], PAL["oscuro"], 0.48) * 0.92                               # azul noche, no negro
CINTA = mezclar(PAL["crema"], PAL["tierra1"], 0.40)
CANTO = mezclar(CARTON, PAL["crema"], 0.60)
CRAYON = mezclar(PAL["crema"], BLANCO, 0.45)
CORAL = mezclar(PAL["coral"], PAL["tierra1"], 0.18)
BOLSA = mezclar(PAL["crema"], BLANCO, 0.50)
# familias de lamina: (base, tono bajo, tono alto)
FAM = {
    "oro": (ORO, mezclar(ORO_OSC, PAL["terracota"], 0.25), mezclar(ORO, PAL["crema"], 0.45)),
    "nar": (ORO_NAR, mezclar(ORO_NAR, PAL["terracota"], 0.55), mezclar(ORO_NAR, PAL["crema"], 0.40)),
    "gris": (GRIS, mezclar(METAL, SOMBRA, 0.50), mezclar(GRIS, BLANCO, 0.40)),
    "osc": (GRIS_OSC, mezclar(GRIS_OSC, SOMBRA, 0.50), mezclar(GRIS_OSC, PAL["piedra_clara"], 0.35)),
}


def unit(v):
    v = np.asarray(v, float)
    return v / max(np.linalg.norm(v), 1e-12)


def luma(c):
    return np.asarray(c, float) @ W_LUMA


# ---------- guardado con comprobacion ----------

def asegurar_luz(mallas, minimo=LUMA_MIN):
    """Sube los colores de vertice que bajan de «minimo» de luminancia sRGB. Devuelve cuantos toco."""
    tocados = 0
    for m in mallas:
        for C in m.C:
            L = C @ W_LUMA
            for i in np.where(L < minimo)[0]:
                C[i] = PAL["oscuro"] * (minimo + 0.004) / luma(PAL["oscuro"]) if L[i] < 1e-4 else np.clip(C[i] * (minimo + 0.004) / L[i], 0, 1)
                tocados += 1
    return tocados


def guardar2(ident: str, nodos: list):
    """Como guardar() de luna_modelos, con la comprobacion de luminancia y el resumen de cada nodo."""
    for nombre, mallas, t in nodos:
        subidos = asegurar_luz(mallas)
        P = np.concatenate([np.array(m.P).reshape(-1, 3) for m in mallas if len(m)]) + np.asarray(t, float)
        C = np.concatenate([np.array(m.C).reshape(-1, 3) for m in mallas if len(m)])
        assert (C @ W_LUMA).min() >= LUMA_MIN, f"{nombre}: color por debajo de {LUMA_MIN}"
        INFORME.append((ident, nombre, sum(len(m) for m in mallas), P.min(0), P.max(0),
                        sorted({m.material for m in mallas if len(m)}), subidos, float((C @ W_LUMA).min())))
    guardar(ident, nodos, generador=GENERADOR, salida=SALIDA)


# ---------- piezas ----------

def tubo(m: Malla, p0, p1, r0, c0, c1=None, lados=6, r1=None, tapas=True, rng=None, s=0.06):
    """Cilindro o tronco de cono entre dos puntos; con rng, cada cara lleva su tono (lamina arrugada)."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    c0 = np.asarray(c0, float)
    c1 = c0 if c1 is None else np.asarray(c1, float)
    r1 = r0 if r1 is None else r1
    u, v = marco(p1 - p0)
    ang = np.arange(lados) / lados * 2 * math.pi
    a = [p0 + (math.cos(t) * u + math.sin(t) * v) * r0 for t in ang]
    b = [p1 + (math.cos(t) * u + math.sin(t) * v) * r1 for t in ang]
    eje = (p0 + p1) / 2
    for i in range(lados):
        j = (i + 1) % lados
        k = 1.0 if rng is None else 1 + rng.normal(0, s)
        poli(m, [a[i], a[j], b[j], b[i]], interior=eje, cols=[c0 * k, c0 * k, c1 * k, c1 * k])
    if tapas:
        if r0 > 1e-5:
            poli(m, a, c0, interior=eje)
        if r1 > 1e-5:
            poli(m, b, c1, interior=eje)


def torno_n(m: Malla, perfil, lados, centro=(0, 0, 0), giro=0.0, rng=None, s=0.05):
    """Solido de revolucion alrededor de Y cuyo perfil puede volver hacia dentro (platos, collares, cuencos).
    perfil = [(radio, y, color), ...]; cada tramo mira a la derecha del sentido de avance: normal (dy, -dr)."""
    centro = np.asarray(centro, float)
    paso = 2 * math.pi / lados
    for k in range(len(perfil) - 1):
        (ra, ya, ca), (rb, yb, cb) = perfil[k], perfil[k + 1]
        ca, cb = np.asarray(ca, float), np.asarray(cb, float)
        dr, dy = rb - ra, yb - ya
        for i in range(lados):
            t0, t1 = giro + i * paso, giro + (i + 1) * paso
            tm = (t0 + t1) / 2
            hacia = np.array([dy * math.cos(tm), -dr, dy * math.sin(tm)])
            v = 1.0 if rng is None else 1 + rng.normal(0, s)
            a0 = centro + np.array([math.cos(t0) * ra, ya, math.sin(t0) * ra])
            a1 = centro + np.array([math.cos(t1) * ra, ya, math.sin(t1) * ra])
            b0 = centro + np.array([math.cos(t0) * rb, yb, math.sin(t0) * rb])
            b1 = centro + np.array([math.cos(t1) * rb, yb, math.sin(t1) * rb])
            if ra < 1e-6:
                poli(m, [a0, b1, b0], hacia=hacia, cols=[ca * v, cb * v, cb * v])
            elif rb < 1e-6:
                poli(m, [a0, a1, b0], hacia=hacia, cols=[ca * v, ca * v, cb * v])
            else:
                poli(m, [a0, a1, b1, b0], hacia=hacia, cols=[ca * v, ca * v, cb * v, cb * v])


def plato(m: Malla, apice, eje, r, prof, c_dentro, c_fuera, lados=8):
    """Plato de antena: cono abierto con sus dos caras (la de dentro mira hacia el eje)."""
    apice, eje = np.asarray(apice, float), unit(eje)
    u, v = marco(eje)
    borde = [apice + eje * prof + (u * math.cos(t) + v * math.sin(t)) * r for t in np.arange(lados) / lados * 2 * math.pi]
    for i in range(lados):
        j = (i + 1) % lados
        poli(m, [apice, borde[i], borde[j]], hacia=eje, cols=[mezclar(c_dentro, SOMBRA, 0.35), c_dentro, c_dentro])
        poli(m, [apice, borde[i], borde[j]], c_fuera, hacia=-eje)


def anillo(m: Malla, centro, ex, ey, r0, r1, c0, c1=None, lados=12, a0=0.0, a1=2 * math.pi, hacia=None, onda=None):
    """Corona plana en el plano (ex, ey), entre los radios r0 y r1. «onda» = funcion(angulo) que multiplica el radio."""
    centro, ex, ey = np.asarray(centro, float), np.asarray(ex, float), np.asarray(ey, float)
    c1 = c0 if c1 is None else c1
    hacia = np.cross(ex, ey) if hacia is None else hacia
    ts = np.linspace(a0, a1, lados + 1)
    for i in range(lados):
        q = []
        for t, r in ((ts[i], r0), (ts[i], r1), (ts[i + 1], r1), (ts[i + 1], r0)):
            k = 1.0 if onda is None else onda(t)
            q.append(centro + (ex * math.cos(t) + ey * math.sin(t)) * r * k)
        poli(m, q, hacia=hacia, cols=[c0, c1, c1, c0])


def estrella4(m: Malla, centro, ex, ey, r, col, hacia, giro=0.0):
    """Estrella de cuatro puntas, como dibujada con crayon."""
    centro = np.asarray(centro, float)
    pts = []
    for k in range(8):
        rr = r if k % 2 == 0 else r * 0.34
        a = giro + k * math.pi / 4
        pts.append(centro + ex * rr * math.cos(a) + ey * rr * math.sin(a))
    for k in range(8):
        poli(m, [centro, pts[k], pts[(k + 1) % 8]], col, hacia=hacia)


def grad(y, y0, y1, sombra, base, luz):
    t = min(max((y - y0) / max(y1 - y0, 1e-6), 0.0), 1.0)
    return mezclar(sombra, base, min(1.0, t * 1.7)) if t < 0.6 else mezclar(base, luz, (t - 0.6) / 0.4)


def solido(nombre, pts, sombra, base, luz, rng, var=0.05, sin_base=False, y_grad=None, material="Facetado"):
    """Casco convexo facetado con degradado vertical. sin_base quita las caras apoyadas en el suelo."""
    pts = np.asarray(pts, float)
    m = Malla(nombre, material)
    y0, y1 = (pts[:, 1].min(), pts[:, 1].max()) if y_grad is None else y_grad
    for (i, j, k) in casco_convexo(pts):
        tri = pts[[i, j, k]]
        n = unit(np.cross(tri[1] - tri[0], tri[2] - tri[0]))
        if sin_base and n[1] < -0.9 and tri[:, 1].max() < pts[:, 1].min() + 0.02:
            continue
        v = 1.0 + rng.normal(0, var)
        m.tri(*tri, *[grad(p[1], y0, y1, sombra, base, luz) * v for p in tri])
    return m


def puntos_roca(rng, n, alto=0.6, fondo=0.85, radio=(0.62, 1.18), piso=0.40, cortes=2):
    """Puntos de una roca angulosa: pocos, de radio muy desigual, con cortes planos y la base aplanada.
    Sale normalizada: extension horizontal maxima 1, alto dado, centrada, base en y = 0."""
    pts = fibonacci(n) * rng.uniform(radio[0], radio[1], (n, 1))
    pts = pts @ rot_eje(unit(rng.normal(size=3)), rng.uniform(0, 2 * math.pi)).T
    for _ in range(cortes):
        d = unit([rng.normal(), abs(rng.normal()) * 0.6 + 0.1, rng.normal()])
        tope = rng.uniform(0.42, 0.66)
        h = pts @ d
        fuera = h > tope
        pts[fuera] -= np.outer(h[fuera] - tope, d)
        pts[fuera] += rng.normal(0, 0.004, (int(fuera.sum()), 3))
    pts[:, 2] *= fondo
    y0 = pts[:, 1].min() * piso
    bajos = pts[:, 1] < y0
    pts[bajos, 1] = y0 + rng.uniform(0, 0.006, int(bajos.sum()))
    pts[:, 1] -= pts[:, 1].min()
    pts[:, [0, 2]] /= max(np.ptp(pts[:, 0]), np.ptp(pts[:, 2]))
    pts[:, 1] *= alto / pts[:, 1].max()
    pts[:, 0] -= (pts[:, 0].max() + pts[:, 0].min()) / 2
    pts[:, 2] -= (pts[:, 2].max() + pts[:, 2].min()) / 2
    return pts


def ajustar_caja(m: Malla, tam=None):
    """Escala la malla a una caja de limites dada (ancho, alto, fondo), la centra en XZ y apoya su base en y = 0."""
    P = np.array(m.P)
    lo, hi = P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0)
    if tam is not None:
        esc = np.asarray(tam, float) / np.maximum(hi - lo, 1e-9)
        P, lo, hi = P * esc, lo * esc, hi * esc
    P[..., 0] -= (lo[0] + hi[0]) / 2
    P[..., 2] -= (lo[2] + hi[2]) / 2
    P[..., 1] -= lo[1]
    m.P = [p for p in P]
    return m


def lamina(m: Malla, a, b, c, d, nu, nv, familia, rng, interior, relieve=(-0.02, 0.05), var=0.05):
    """Cuadrilatero a-b (abajo), c-d (arriba; c sobre b, d sobre a) en nu x nv paneles de lamina arrugada:
    cada panel son 4 triangulos con el centro salido o hundido. familia(iu, iv) -> (base, bajo, alto)."""
    a, b, c, d = (np.asarray(p, float) for p in (a, b, c, d))
    nrm = unit(np.cross(b - a, d - a))
    if nrm @ ((a + b + c + d) / 4 - np.asarray(interior, float)) < 0:
        nrm = -nrm

    def P(u, v):
        return (a * (1 - u) + b * u) * (1 - v) + (d * (1 - u) + c * u) * v

    for iu in range(nu):
        for iv in range(nv):
            base, bajo, alto = familia(iu, iv)
            base = jit(base, rng, var)
            q = [P(iu / nu, iv / nv), P((iu + 1) / nu, iv / nv), P((iu + 1) / nu, (iv + 1) / nv), P(iu / nu, (iv + 1) / nv)]
            cen = sum(q) / 4 + nrm * rng.uniform(*relieve)
            tv = [iv / nv, iv / nv, (iv + 1) / nv, (iv + 1) / nv]
            cq = [mezclar(mezclar(base, bajo, 0.6), mezclar(base, alto, 0.5), t) for t in tv]
            for e in range(4):
                f = (e + 1) % 4
                k = 1 + rng.normal(0, var * 0.6)
                poli(m, [q[e], q[f], cen], hacia=nrm, cols=[cq[e] * k, cq[f] * k, base * k])


def caja_lamina(m: Malla, c, tam, fam, rng, div=(2, 1, 2), relieve=(-0.012, 0.03)):
    """Caja envuelta en lamina arrugada (sin cara inferior)."""
    c = np.asarray(c, float)
    hx, hy, hz = np.asarray(tam, float) / 2

    def V(sx, sy, sz):
        return c + np.array([sx * hx, sy * hy, sz * hz])

    nx, ny, nz = div
    lados = lambda iu, iv: fam  # noqa: E731
    tapa = lambda iu, iv: (mezclar(fam[0], fam[2], 0.35), fam[0], fam[2])  # noqa: E731
    lamina(m, V(-1, -1, 1), V(1, -1, 1), V(1, 1, 1), V(-1, 1, 1), nx, ny, lados, rng, c, relieve)
    lamina(m, V(1, -1, -1), V(-1, -1, -1), V(-1, 1, -1), V(1, 1, -1), nx, ny, lados, rng, c, relieve)
    lamina(m, V(1, -1, 1), V(1, -1, -1), V(1, 1, -1), V(1, 1, 1), nz, ny, lados, rng, c, relieve)
    lamina(m, V(-1, -1, -1), V(-1, -1, 1), V(-1, 1, 1), V(-1, 1, -1), nz, ny, lados, rng, c, relieve)
    lamina(m, V(-1, 1, 1), V(1, 1, 1), V(1, 1, -1), V(-1, 1, -1), nx, nz, tapa, rng, c, relieve)


# ---------- LUN-02 rocas ----------

def rocas():
    nodos = []
    # letra, semilla, puntos, alto, fondo, cortes, basalto
    variantes = [("a", 11, 11, 0.62, 0.86, 2, False), ("b", 23, 10, 0.47, 0.72, 1, False),
                 ("c", 37, 12, 0.93, 0.82, 2, False), ("d", 41, 10, 0.55, 0.62, 2, False),
                 ("e", 53, 13, 0.72, 0.95, 3, False), ("f", 67, 10, 0.82, 0.76, 1, False),
                 ("g", 71, 11, 0.58, 0.84, 2, True), ("h", 89, 10, 0.76, 0.70, 2, True)]
    for letra, semilla, n, alto, fondo, cortes, basalto in variantes:
        rng = np.random.default_rng(semilla)
        pts = puntos_roca(rng, n, alto, fondo, cortes=cortes)
        if basalto:
            m = solido(f"LUN-02_{letra}", pts, BASALTO_PIE, BASALTO, BASALTO_LUZ, rng)
        else:
            base = mezclar(ROCA, PAL["piedra"], rng.uniform(0.0, 0.25))
            m = solido(f"LUN-02_{letra}", pts, ROCA_PIE, base, ROCA_LUZ, rng)
        nodos.append((f"LUN-02_{letra}", [m], (0, 0, 0)))
    guardar2("LUN-02", nodos)


# ---------- LUN-10 piedras pequenas ----------

def piedras():
    rng = np.random.default_rng(10)

    def tonos(base):
        return mezclar(base, ROCA_PIE, 0.55), mezclar(base, ROCA_LUZ, 0.55)

    nodos = []
    # a: piramide de cuatro lados con la punta corrida
    m = Malla("LUN-10_a")
    pie, luz = tonos(ROCA)
    b = [(-0.50, 0, -0.34), (0.44, 0, -0.42), (0.50, 0, 0.36), (-0.40, 0, 0.44)]
    ap = (0.10, 0.52, -0.06)
    for i in range(4):
        poli(m, [b[i], b[(i + 1) % 4], ap], interior=(0, 0.1, 0), cols=[pie * (1 + rng.normal(0, 0.05))] * 2 + [luz])
    nodos.append(("LUN-10_a", [m], (0, 0, 0)))
    # b: lasca alargada con cumbrera
    m = Malla("LUN-10_b")
    pie, luz = tonos(mezclar(ROCA, PAL["piedra"], 0.3))
    b = [np.array(p, float) for p in ((-0.50, 0, -0.20), (0.50, 0, -0.27), (0.48, 0, 0.24), (-0.46, 0, 0.20))]
    r0, r1 = np.array([-0.28, 0.30, 0.02]), np.array([0.26, 0.40, -0.04])
    dentro = (0, 0.1, 0)
    poli(m, [b[0], b[1], r1, r0], interior=dentro, cols=[pie, pie, luz, luz])
    poli(m, [b[2], b[3], r0, r1], interior=dentro, cols=[pie * 1.06, pie * 1.06, luz, luz])
    poli(m, [b[3], b[0], r0], interior=dentro, cols=[pie * 0.95, pie * 0.95, luz])
    poli(m, [b[1], b[2], r1], interior=dentro, cols=[pie * 1.03, pie * 1.03, luz])
    nodos.append(("LUN-10_b", [m], (0, 0, 0)))
    # c: gema (antiprisma triangular truncado), algo mas calida
    m = Malla("LUN-10_c")
    pie, luz = tonos(FRESCA)
    B = [np.array([math.cos(a) * 0.52, 0, math.sin(a) * 0.52]) for a in (0.3, 0.3 + 2.2, 0.3 + 4.2)]
    T = [np.array([math.cos(a) * 0.26, 0.48, math.sin(a) * 0.26]) + np.array([0.04, 0, -0.03]) for a in (1.4, 1.4 + 2.0, 1.4 + 4.3)]
    T[1][1] = 0.40
    T[2][1] = 0.55
    dentro = (0, 0.2, 0)
    for i in range(3):
        j = (i + 1) % 3
        poli(m, [B[i], B[j], T[i]], interior=dentro, cols=[pie * (1 + rng.normal(0, 0.05))] * 2 + [luz])
        poli(m, [B[j], T[j], T[i]], interior=dentro, cols=[pie, luz, luz])
    poli(m, T, luz * 1.03, interior=dentro)
    nodos.append(("LUN-10_c", [m], (0, 0, 0)))
    # d: piramide pentagonal baja de basalto
    m = Malla("LUN-10_d")
    pie, luz = mezclar(BASALTO, BASALTO_PIE, 0.5), BASALTO_LUZ
    b = [np.array([math.cos(a) * r, 0, math.sin(a) * r * 0.8]) for a, r in ((0.2, 0.50), (1.5, 0.42), (2.7, 0.50), (3.9, 0.44), (5.2, 0.48))]
    ap = (-0.06, 0.36, 0.05)
    for i in range(5):
        poli(m, [b[i], b[(i + 1) % 5], ap], interior=(0, 0.1, 0), cols=[pie * (1 + rng.normal(0, 0.06))] * 2 + [luz])
    nodos.append(("LUN-10_d", [m], (0, 0, 0)))
    for _, mallas, _ in nodos:
        P = np.array(mallas[0].P)
        lo, hi = P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0)
        k = 1.0 / max(hi[0] - lo[0], hi[2] - lo[2])
        P *= k
        P[..., 0] -= (lo[0] + hi[0]) / 2 * k
        P[..., 2] -= (lo[2] + hi[2]) / 2 * k
        mallas[0].P = [p for p in P]
    guardar2("LUN-10", nodos)


# ---------- LUN-11 bloques de eyecta ----------

def eyecta():
    nodos = []

    def normalizar(m, hundir):
        P = np.array(m.P)
        lo, hi = P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0)
        k = 1.0 / max(hi[0] - lo[0], hi[2] - lo[2])
        P *= k
        P[..., 0] -= (lo[0] + hi[0]) / 2 * k
        P[..., 2] -= (lo[2] + hi[2]) / 2 * k
        P[..., 1] += -lo[1] * k - hundir
        m.P = [p for p in P]
        return m

    def pintar(nombre, pts, rng, hundir):
        # el degradado empieza en el suelo: lo enterrado no cuenta
        y1 = pts[:, 1].max()
        y0 = pts[:, 1].min() + hundir * (np.ptp(pts[:, 0]))
        return solido(nombre, pts, FRESCA_PIE, FRESCA, FRESCA_LUZ, rng, y_grad=(y0, y1))

    # a: losa inclinada, con una esquina clavada
    rng = np.random.default_rng(111)
    caja = np.array([[sx * 0.5, sy * 0.12, sz * 0.32] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], float)
    caja += rng.normal(0, 0.035, caja.shape)
    caja = caja @ (rot_eje([0, 0, 1], math.radians(24)) @ rot_eje([1, 0, 0], math.radians(-9))).T
    nodos.append(("LUN-11_a", [normalizar(pintar("LUN-11_a", caja, rng, 0.15), 0.15)], (0, 0, 0)))
    # b: cuna en pie, ladeada
    rng = np.random.default_rng(112)
    pts = np.array([[-0.42, 0, -0.28], [0.40, 0, -0.34], [0.46, 0, 0.26], [-0.36, 0, 0.30],
                    [-0.10, 0.80, -0.06], [0.12, 0.72, 0.04], [0.34, 0.36, -0.20]], float)
    pts += rng.normal(0, 0.02, pts.shape)
    pts = pts @ rot_eje([0, 0, 1], math.radians(-13)).T
    nodos.append(("LUN-11_b", [normalizar(pintar("LUN-11_b", pts, rng, 0.12), 0.12)], (0, 0, 0)))
    # c: bloque partido en dos fragmentos
    rng = np.random.default_rng(113)
    uno = np.array([[-0.50, 0, -0.22], [-0.06, 0, -0.30], [-0.02, 0, 0.22], [-0.46, 0, 0.26], [-0.34, 0.42, -0.06], [-0.10, 0.34, 0.04]], float)
    dos = np.array([[0.08, 0, -0.18], [0.50, 0, -0.10], [0.44, 0, 0.30], [0.12, 0, 0.24], [0.20, 0.26, 0.00], [0.40, 0.30, 0.10]], float)
    uno += rng.normal(0, 0.02, uno.shape)
    dos += rng.normal(0, 0.02, dos.shape)
    uno = uno @ rot_eje([0, 0, 1], math.radians(10)).T
    dos = dos @ rot_eje([1, 0, 0], math.radians(12)).T
    y1 = max(uno[:, 1].max(), dos[:, 1].max())
    m = solido("LUN-11_c", uno, FRESCA_PIE, FRESCA, FRESCA_LUZ, rng, y_grad=(0.05, y1))
    m.anexar(solido("x", dos, FRESCA_PIE, mezclar(FRESCA, ROCA, 0.4), FRESCA_LUZ, rng, y_grad=(0.05, y1)))
    nodos.append(("LUN-11_c", [normalizar(m, 0.10)], (0, 0, 0)))
    guardar2("LUN-11", nodos)


# ---------- LUN-18 penascos grandes ----------

def penascos():
    def parte(semilla, n, tam, pos, giro, cortes, alto_total, base):
        rng = np.random.default_rng(semilla)
        pts = puntos_roca(rng, n, alto=1.0, fondo=1.0, cortes=cortes, piso=0.45)
        pts = (pts * np.asarray(tam, float)) @ rot_y(giro).T + np.asarray(pos, float)
        return solido("parte", pts, mezclar(ROCA_PIE, PAL["piedra_osc"], 0.12), base, ROCA_LUZ, rng, var=0.045, y_grad=(0.0, alto_total))

    # a: bloque alto, con un contrafuerte y una losa apoyada
    a = Malla("LUN-18_a")
    a.anexar(parte(181, 13, (2.0, 2.0, 1.7), (0.15, 0, -0.10), 0.3, 3, 2.0, ROCA))
    a.anexar(parte(182, 11, (1.5, 1.15, 1.4), (-0.80, 0, 0.42), 1.1, 2, 2.0, mezclar(ROCA, PAL["piedra"], 0.18)))
    a.anexar(parte(183, 10, (1.0, 0.70, 0.9), (0.95, 0, 0.55), 2.0, 2, 2.0, mezclar(ROCA, PAL["piedra"], 0.30)))
    ajustar_caja(a, (2.6, 2.0, 2.0))
    # b: afloramiento bajo de losas
    b = Malla("LUN-18_b")
    b.anexar(parte(185, 13, (2.3, 1.05, 1.8), (-0.20, 0, -0.10), 0.2, 3, 1.1, ROCA))
    b.anexar(parte(186, 11, (1.5, 0.72, 1.3), (0.95, 0, 0.30), 0.9, 2, 1.1, mezclar(ROCA, PAL["piedra"], 0.22)))
    b.anexar(parte(187, 10, (1.0, 0.45, 0.9), (-1.10, 0, 0.55), 2.4, 2, 1.1, mezclar(ROCA, PAL["piedra"], 0.12)))
    ajustar_caja(b, (3.0, 1.1, 2.2))
    guardar2("LUN-18", [("LUN-18_a", [a], (0, 0, 0)), ("LUN-18_b", [b], (0, 0, 0))])


# ---------- LUN-03 etapa de descenso generica ----------

def etapa_descenso():
    rng = np.random.default_rng(1969)
    m = Malla("LUN-03_cuerpo")
    y0, y1, ap = 1.30, 2.95, 2.10             # cuerpo octogonal: 4,2 m entre caras
    r = ap / math.cos(math.pi / 8)
    ang = [math.pi / 8 + k * math.pi / 4 for k in range(8)]
    abajo = [np.array([math.cos(a) * r, y0, math.sin(a) * r]) for a in ang]
    arriba = [np.array([math.cos(a) * r, y1, math.sin(a) * r]) for a in ang]
    centro = np.array([0, (y0 + y1) / 2, 0])
    arriba_v = np.array([0.0, 1.0, 0.0])
    # caras: 3 x 2 paneles de lamina arrugada. Las diagonales, doradas; las de las patas, grises
    diag = (("oro", 0.50), ("nar", 0.30), ("osc", 0.14), ("gris", 0.06))
    recta = (("gris", 0.40), ("osc", 0.38), ("oro", 0.14), ("nar", 0.08))
    for k in range(8):
        j = (k + 1) % 8
        tabla = diag if k % 2 == 0 else recta
        nombres, pesos = [t[0] for t in tabla], [t[1] for t in tabla]
        elegidos = {(iu, iv): FAM[nombres[rng.choice(len(nombres), p=pesos)]] for iu in range(3) for iv in range(2)}
        if k == 0:
            elegidos[(1, 0)] = FAM["osc"]      # el hueco de donde sale la bandeja
        lamina(m, abajo[k], abajo[j], arriba[j], arriba[k], 3, 2, lambda iu, iv: elegidos[(iu, iv)], rng, centro)
    # aristas y cercos
    for k in range(8):
        e = np.array([1.004, 1.0, 1.004])
        barra(m, abajo[k] * e - Y * 0.02, arriba[k] * e + Y * 0.02, 0.042, METAL_OSC, METAL, lados=4)
    torno_n(m, [(r + 0.04, y1 - 0.08, METAL_OSC), (r + 0.04, y1 + 0.03, METAL), (r - 0.03, y1 + 0.03, mezclar(METAL, BLANCO, 0.25))],
            8, giro=math.pi / 8)
    torno_n(m, [(r + 0.04, y0 - 0.03, mezclar(METAL_OSC, SOMBRA, 0.4)), (r + 0.04, y0 + 0.08, METAL_OSC), (r - 0.01, y0 + 0.08, METAL)],
            8, giro=math.pi / 8)
    # cubierta: la etapa de ascenso ya no esta; el centro quedo chamuscado
    cubierta = mezclar(METAL, PAL["piedra_osc"], 0.35)
    quemado2 = mezclar(QUEMADO, cubierta, 0.45)
    c0 = np.array([0, y1, 0])
    dentro = [np.array([math.cos(a) * 1.30, y1, math.sin(a) * 1.30]) for a in ang]
    for k in range(8):
        j = (k + 1) % 8
        v = 1 + rng.normal(0, 0.04)
        poli(m, [c0, dentro[k], dentro[j]], hacia=arriba_v, cols=[QUEMADO * v, quemado2 * v, quemado2 * v])
        poli(m, [dentro[k], arriba[k], arriba[j], dentro[j]], hacia=arriba_v, cols=[quemado2 * v, cubierta * v, cubierta * v, quemado2 * v])
    poli(m, abajo, mezclar(METAL_OSC, SOMBRA, 0.5), hacia=-arriba_v)
    # collar de acople
    torno_n(m, [(0.66, y1, METAL_OSC), (0.66, y1 + 0.18, METAL), (0.50, y1 + 0.18, mezclar(METAL, BLANCO, 0.30)),
                (0.50, y1 + 0.03, QUEMADO), (0.0, y1 + 0.03, mezclar(QUEMADO, METAL_OSC, 0.5))], 12, rng=rng, s=0.03)
    # cuatro domos de tanque: dorados delante, plateados detras
    for sx, sz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        f = FAM["oro"] if sz > 0 else FAM["gris"]
        torno_n(m, [(0.40, y1, f[1]), (0.40, y1 + 0.10, f[0]), (0.31, y1 + 0.25, mezclar(f[0], f[2], 0.5)),
                    (0.15, y1 + 0.34, f[2]), (0.0, y1 + 0.365, f[2])], 8, centro=(sx * 1.12, 0, sz * 1.12), giro=0.2, rng=rng)
        d = unit([sx, 0, sz])
        barra(m, d * 0.66 + Y * (y1 + 0.07), d * 1.20 + Y * (y1 + 0.07), 0.035, METAL_OSC, METAL, lados=4, tapas=False)
    bloque(m, (0.0, y1 + 0.09, 1.38), (0.52, 0.18, 0.30), GRIS, sombra=0.35, base=False)
    bloque(m, (1.50, y1 + 0.07, 0.0), (0.30, 0.14, 0.52), GRIS_OSC, sombra=0.30, luz=0.25, base=False)
    # antena pequena generica en una esquina de la cubierta: mastil fino y plato
    pa = np.array([math.cos(ang[4]) * 1.78, y1, math.sin(ang[4]) * 1.78])
    torno_n(m, [(0.085, y1, METAL_OSC), (0.055, y1 + 0.07, METAL)], 6, centro=(pa[0], 0, pa[2]))
    cima = pa + Y * 1.05
    tubo(m, pa, cima, 0.022, METAL_OSC, mezclar(METAL, BLANCO, 0.3), lados=5, tapas=False)
    eje = unit([0.22, 0.72, 0.66])
    plato(m, cima, eje, 0.27, 0.10, mezclar(BLANCO, METAL, 0.25), METAL_OSC, lados=9)
    tubo(m, cima, cima + eje * 0.24, 0.010, METAL, lados=3, tapas=False)
    octaedro(m, cima + eje * 0.25, 0.028, METAL_OSC, alto=1.0)
    # tobera
    torno_n(m, [(0.80, 0.50, mezclar(METAL_OSC, SOMBRA, 0.5)), (0.76, 0.60, METAL_OSC), (0.54, 0.95, mezclar(METAL_OSC, PAL["piedra"], 0.4)),
                (0.38, 1.22, METAL_OSC), (0.34, y0, mezclar(METAL_OSC, SOMBRA, 0.3))], 12, rng=rng, s=0.04)
    # bandeja de equipo abatida en la cara diagonal delantera derecha, con dos cajas y dos tirantes
    nf, tf = unit([1, 0, 1]), unit([1, 0, -1])
    baja = math.radians(8)
    zb = nf * math.cos(baja) - Y * math.sin(baja)
    R = np.stack([tf, np.cross(zb, tf), zb], 1)
    cb = nf * (ap + 0.50) + Y * (y0 + 0.11 - 0.50 * math.sin(baja))
    bloque(m, cb, (1.12, 0.05, 0.98), GRIS, R=R, sombra=0.40, luz=0.20, tapa=mezclar(GRIS, BLANCO, 0.25))
    bloque(m, cb + R @ np.array([-0.26, 0.20, 0.06]), (0.38, 0.35, 0.38), mezclar(BLANCO, METAL, 0.30), R=R, sombra=0.35, base=False)
    caja_lamina(m, cb + R @ np.array([0.27, 0.15, -0.08]), (0.32, 0.25, 0.42), FAM["oro"], rng, div=(1, 1, 2))
    for s in (-1, 1):
        tubo(m, nf * (ap + 0.01) + tf * s * 0.52 + Y * 2.36, cb + R @ np.array([s * 0.53, 0.03, 0.46]), 0.014, METAL, lados=3, tapas=False)

    # patas: en +Z (escalerilla), +X, -Z y -X. 9,2 m entre zapatas opuestas
    p = Malla("LUN-03_patas")
    esc = Malla("LUN-03_escalerilla")
    plata = mezclar(METAL, BLANCO, 0.28)
    for k, a in enumerate((math.pi / 2, 0.0, -math.pi / 2, math.pi)):
        d = np.array([math.cos(a), 0, math.sin(a)])
        lado = np.array([-d[2], 0, d[0]])
        hombro = d * 2.58 + Y * 2.50
        pie = d * 4.60 + Y * 0.27
        e = unit(pie - hombro)
        rodilla = hombro + (pie - hombro) * 0.58
        esquinas_altas = [d * (ap + 0.01) + lado * s * 0.80 + Y * 2.84 for s in (-1, 1)]
        esquinas_bajas = [d * (ap + 0.01) + lado * s * 0.80 + Y * 1.40 for s in (-1, 1)]
        # armazon que separa el hombro del cuerpo
        for q in esquinas_altas:
            tubo(p, q, hombro, 0.046, METAL_OSC, METAL, lados=4)
        for q in esquinas_bajas:
            tubo(p, q, hombro, 0.040, METAL_OSC, METAL, lados=4)
        # puntal principal: tramo alto envuelto en dorado, tramo bajo plateado
        tubo(p, hombro, rodilla, 0.115, ORO, ORO_OSC, lados=6, rng=rng, s=0.08)
        tubo(p, rodilla - e * 0.07, rodilla + e * 0.07, 0.138, METAL, METAL_OSC, lados=6)
        tubo(p, rodilla, pie, 0.072, plata, METAL, lados=6)
        octaedro(p, pie, 0.115, METAL_OSC, alto=1.0)
        tubo(p, pie, d * 4.60 + Y * 0.10, 0.05, METAL_OSC, lados=5, tapas=False)
        # puntales secundarios en V y su travesano
        medios = []
        for q in esquinas_bajas:
            tubo(p, q, rodilla, 0.042, METAL_OSC, plata, lados=4)
            medios.append(q + (rodilla - q) * 0.45)
        tubo(p, medios[0], medios[1], 0.028, METAL_OSC, lados=4, tapas=False)
        # zapata en plato: se ve el cuenco desde arriba
        zc = d * 4.60
        torno_n(p, [(0.24, 0.0, mezclar(ORO_OSC, SOMBRA, 0.45)), (0.50, 0.05, ORO_OSC), (0.55, 0.15, ORO),
                    (0.49, 0.18, mezclar(ORO, PAL["crema"], 0.40)), (0.20, 0.10, ORO_OSC), (0.0, 0.10, mezclar(ORO_OSC, SOMBRA, 0.25))],
                10, centro=zc, rng=rng)
        if k != 0:
            # sonda de contacto, doblada sobre el suelo
            tubo(p, zc + lado * 0.40 + d * 0.30 + Y * 0.06, zc + lado * 0.60 + d * 0.78 + Y * 0.015, 0.012, METAL, lados=3)
        else:
            # escalerilla sobre la pata delantera: dos barandas, 8 peldanos, plataforma y una placa lisa
            n = d * (-e[1]) + Y * (e @ d)           # perpendicular al puntal: hacia fuera y arriba
            largo = pie - hombro
            for s in (-1, 1):
                tubo(esc, hombro + lado * s * 0.21 + n * 0.20, hombro + largo * 0.84 + lado * s * 0.21 + n * 0.20, 0.024, plata, METAL, lados=4)
                for t in (0.10, 0.45, 0.80):
                    c = hombro + largo * t
                    tubo(esc, c + lado * s * 0.07, c + lado * s * 0.21 + n * 0.20, 0.014, METAL_OSC, METAL, lados=3, tapas=False)
            for t in np.linspace(0.06, 0.80, 8):
                c = hombro + largo * t + n * 0.20
                tubo(esc, c - lado * 0.21, c + lado * 0.21, 0.017, plata, lados=4, tapas=False)
            c = hombro + largo * 0.43 + n * 0.225
            poli(esc, [c - lado * 0.15 - e * 0.10, c + lado * 0.15 - e * 0.10, c + lado * 0.15 + e * 0.10, c - lado * 0.15 + e * 0.10],
                 mezclar(METAL, BLANCO, 0.60), hacia=n)
            poli(esc, [c - lado * 0.15 - e * 0.10, c + lado * 0.15 - e * 0.10, c + lado * 0.15 + e * 0.10, c - lado * 0.15 + e * 0.10],
                 METAL_OSC, hacia=-n)
            # plataforma pequena sobre el hombro, con dos barandas
            bloque(esc, (0, 2.635, 2.48), (0.92, 0.05, 0.80), GRIS, sombra=0.40, luz=0.20, tapa=mezclar(GRIS, BLANCO, 0.20))
            for s in (-1, 1):
                for z in (2.14, 2.84):
                    tubo(esc, (s * 0.42, 2.66, z), (s * 0.42, 3.18, z), 0.020, METAL_OSC, plata, lados=4, tapas=False)
                tubo(esc, (s * 0.42, 3.18, 2.12), (s * 0.42, 3.18, 2.86), 0.022, plata, lados=4)
    guardar2("LUN-03", [("LUN-03_etapa_descenso", [m, p, esc], (0, 0, 0))])


# ---------- LUN-04 caja-capsula de carton ----------

def caja_capsula():
    rng = np.random.default_rng(4)
    m = Malla("LUN-04_caja")
    w, h, d, g = 1.15, 0.82, 0.86, 0.03
    lateral = mezclar(CARTON, CARTON_OSC, 0.25)
    # cuatro paredes con grosor y fondo; abierta por arriba
    bloque(m, (0, h / 2, d / 2 - g / 2), (w, h, g), CARTON, sombra=0.32, luz=0.20)
    bloque(m, (0, h / 2, -d / 2 + g / 2), (w, h, g), CARTON, sombra=0.32, luz=0.20)
    bloque(m, (w / 2 - g / 2, h / 2, 0), (g, h, d - 2 * g), lateral, sombra=0.32, luz=0.15)
    bloque(m, (-w / 2 + g / 2, h / 2, 0), (g, h, d - 2 * g), lateral, sombra=0.32, luz=0.15)
    poli(m, [(-w / 2 + g, 0.05, -d / 2 + g), (w / 2 - g, 0.05, -d / 2 + g), (w / 2 - g, 0.05, d / 2 - g), (-w / 2 + g, 0.05, d / 2 - g)],
         mezclar(CARTON_OSC, SOMBRA, 0.45), hacia=(0, 1, 0))

    # solapas abiertas hacia fuera, con grosor y el canto ondulado mas claro
    def solapa(a, b, fuera, ancho, grados):
        a, b, fuera = np.asarray(a, float), np.asarray(b, float), np.asarray(fuera, float)
        ang = math.radians(grados)
        sube = fuera * ancho * math.cos(ang) + Y * ancho * math.sin(ang)
        mete = unit(b - a) * 0.02
        c_, d_ = b + sube - mete, a + sube + mete
        nrm = unit(np.cross(b - a, d_ - a))
        nrm = nrm if nrm[1] > 0 or (abs(nrm[1]) < 1e-6 and nrm @ fuera < 0) else -nrm
        if grados > 89:
            nrm = -fuera
        claro = mezclar(CARTON, PAL["crema"], 0.30)
        poli(m, [a, b, c_, d_], hacia=nrm, cols=[CARTON, CARTON, claro, claro])
        t = nrm * 0.014
        poli(m, [a - t, b - t, c_ - t, d_ - t], mezclar(CARTON_OSC, SOMBRA, 0.22), hacia=-nrm)
        partes = 6
        for i in range(partes):
            p0, p1 = d_ + (c_ - d_) * i / partes, d_ + (c_ - d_) * (i + 1) / partes
            col = CANTO if i % 2 == 0 else mezclar(CANTO, CARTON_OSC, 0.38)
            poli(m, [p0, p1, p1 - t, p0 - t], col, hacia=unit(sube))
        return a, b, c_, d_, nrm

    solapa((-w / 2, h, d / 2), (w / 2, h, d / 2), (0, 0, 1), 0.40, 66)       # delantera: levantada, no tapa el dibujo
    solapa((w / 2, h, -d / 2), (-w / 2, h, -d / 2), (0, 0, -1), 0.40, 52)    # trasera
    sx = solapa((w / 2, h, d / 2), (w / 2, h, -d / 2), (1, 0, 0), 0.34, 38)  # derecha
    si = solapa((-w / 2, h, -d / 2), (-w / 2, h, d / 2), (-1, 0, 0), 0.34, 10)   # izquierda: casi tendida, como en el arte

    # cinta de embalar: tiras a 4 mm de la superficie
    def tira(pts, hacia):
        poli(m, [np.asarray(q, float) for q in pts], hacia=hacia, cols=[CINTA, CINTA, mezclar(CINTA, BLANCO, 0.25), mezclar(CINTA, BLANCO, 0.25)])

    zf = d / 2 + 0.004
    tira([(-0.545, 0.30, zf), (-0.475, 0.30, zf), (-0.47, 0.78, zf), (-0.54, 0.78, zf)], (0, 0, 1))
    tira([(0.20, 0.07, zf), (0.53, 0.09, zf), (0.53, 0.16, zf), (0.20, 0.14, zf)], (0, 0, 1))
    a_, b_, c_, d_, nrm = si
    q0, q1 = a_ + (b_ - a_) * 0.55, a_ + (b_ - a_) * 0.72
    tira([q0 + nrm * 0.004, q1 + nrm * 0.004, q1 + (c_ - b_) * 0.55 + nrm * 0.004, q0 + (d_ - a_) * 0.55 + nrm * 0.004], nrm)
    tira([(-0.575 - 0.004, 0.62, q0[2]), (-0.575 - 0.004, 0.62, q1[2]), (-0.575 - 0.004, 0.82, q1[2]), (-0.575 - 0.004, 0.82, q0[2])], (-1, 0, 0))

    # dibujo de crayon en la cara +Z: un circulo crema con una Luna creciente dentro
    dib = Malla("LUN-04_dibujo")
    ex, ey, ez = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
    cx, cy = -0.02, 0.42
    c = np.array([cx, cy, d / 2 + 0.006])
    temblor = lambda t: 1 + 0.025 * math.sin(3 * t + 0.7) + 0.015 * math.sin(7 * t)  # noqa: E731
    anillo(dib, c, ex, ey, 0.212, 0.246, CRAYON, mezclar(CRAYON, PAL["crema"], 0.3), lados=20, hacia=ez, onda=temblor)
    R1, R2, e_ = 0.165, 0.146, 0.072
    xi = (R1 * R1 - R2 * R2 + e_ * e_) / (2 * e_)
    t1 = math.atan2(math.sqrt(R1 * R1 - xi * xi), xi)
    t2 = math.atan2(math.sqrt(R1 * R1 - xi * xi), xi - e_)
    gira = math.radians(-24)
    cg, sg = math.cos(gira), math.sin(gira)

    def pt(x, y, capa=0.010):
        return np.array([cx + x * cg - y * sg, cy + x * sg + y * cg, d / 2 + capa])

    n_seg = 12
    for i in range(n_seg):
        s0, s1 = i / n_seg, (i + 1) / n_seg
        q = []
        for s_, fuera_ in ((s0, True), (s0, False), (s1, False), (s1, True)):
            if fuera_:
                a = t1 + s_ * (2 * math.pi - 2 * t1)
                q.append(pt(R1 * math.cos(a), R1 * math.sin(a)))
            else:
                a = t2 + s_ * (2 * math.pi - 2 * t2)
                q.append(pt(e_ + R2 * math.cos(a), R2 * math.sin(a)))
        poli(dib, q, hacia=ez, cols=[CRAYON, mezclar(CRAYON, PAL["crema"], 0.35), mezclar(CRAYON, PAL["crema"], 0.35), CRAYON])
    for (sx_, sy_, rr, gg) in ((-0.43, 0.66, 0.050, 0.3), (0.40, 0.63, 0.056, 0.0), (0.45, 0.33, 0.036, 0.5), (-0.41, 0.17, 0.034, 0.2)):
        estrella4(dib, (sx_, sy_, d / 2 + 0.006), ex, ey, rr, PAL["dorado"], ez, giro=gg)

    # ventanilla dibujada en el lado +X: disco azul oscuro con aro crema y un reflejo
    xv = w / 2 + 0.005
    cv = np.array([xv, 0.44, 0.10])
    disco(dib, cv, (1, 0, 0), 0.140, NOCHE, lados=12)
    anillo(dib, cv + np.array([0.004, 0, 0]), -ez, ey, 0.132, 0.178, CRAYON, mezclar(CRAYON, PAL["crema"], 0.3), lados=14, hacia=ex, onda=temblor)
    poli(dib, [cv + np.array([0.004, 0.02, 0.07]), cv + np.array([0.004, 0.07, 0.03]), cv + np.array([0.004, 0.09, 0.05]), cv + np.array([0.004, 0.04, 0.09])],
         mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.45), hacia=ex)

    # aletas triangulares de carton pegadas a los lados
    for s in (-1, 1):
        z0 = -0.30
        p0, p1, p2 = np.array([s * w / 2, 0.04, z0]), np.array([s * w / 2, 0.62, z0]), np.array([s * (w / 2 + 0.36), 0.04, z0])
        t = np.array([0, 0, 0.022])
        oscuro = mezclar(CARTON, SOMBRA, 0.30)
        poli(m, [p0 + t, p2 + t, p1 + t], hacia=(0, 0, 1), cols=[oscuro, oscuro, mezclar(CARTON, PAL["crema"], 0.25)])
        poli(m, [p0, p2, p1], hacia=(0, 0, -1), cols=[oscuro, oscuro, CARTON])
        poli(m, [p1, p2, p2 + t, p1 + t], CANTO, hacia=(s * 0.85, 0.5, 0))
        poli(m, [p0, p2, p2 + t, p0 + t], mezclar(CARTON_OSC, SOMBRA, 0.3), hacia=(0, -1, 0))
        tira([(s * (w / 2 + 0.004), 0.30, z0 - 0.05), (s * (w / 2 + 0.004), 0.30, z0 + 0.07), (s * (w / 2 + 0.004), 0.40, z0 + 0.07), (s * (w / 2 + 0.004), 0.40, z0 - 0.05)], (s, 0, 0))

    # escudo termico: disco de carton apoyado en el lado -X, con una espiral de crayon
    esc = Malla("LUN-04_escudo")
    ne = unit([-0.72, 0.42, 0.55])
    Re, grosor = 0.375, 0.03
    ce = np.array([-0.742, 0.356, 0.18])
    eu = unit(Y - ne * (Y @ ne))                 # hacia arriba dentro del plano del disco
    el = np.cross(eu, ne)
    lados_e = 14
    borde = [ce + (el * math.cos(t) + eu * math.sin(t)) * Re for t in np.arange(lados_e) / lados_e * 2 * math.pi]
    for i in range(lados_e):
        j = (i + 1) % lados_e
        v = 1 + rng.normal(0, 0.03)
        ci = mezclar(mezclar(CARTON, SOMBRA, 0.25), mezclar(CARTON, PAL["crema"], 0.25), (borde[i][1] / 0.72))
        cj = mezclar(mezclar(CARTON, SOMBRA, 0.25), mezclar(CARTON, PAL["crema"], 0.25), (borde[j][1] / 0.72))
        poli(esc, [ce, borde[i], borde[j]], hacia=ne, cols=[mezclar(CARTON, PAL["crema"], 0.12) * v, ci * v, cj * v])
        poli(esc, [ce - ne * grosor, borde[i] - ne * grosor, borde[j] - ne * grosor], mezclar(CARTON_OSC, SOMBRA, 0.3), hacia=-ne)
        radial = unit((borde[i] + borde[j]) / 2 - ce)
        poli(esc, [borde[i], borde[j], borde[j] - ne * grosor, borde[i] - ne * grosor], CANTO if i % 2 == 0 else mezclar(CANTO, CARTON_OSC, 0.38), hacia=radial)
    pasos, vueltas = 26, 2.3
    for i in range(pasos):
        q = []
        for s_ in (i / pasos, (i + 1) / pasos):
            a = s_ * vueltas * 2 * math.pi + 0.6
            rr = 0.045 + (0.30 - 0.045) * s_
            for dr in (-0.012, 0.012):
                q.append(ce + ne * 0.004 + (el * math.cos(a) + eu * math.sin(a)) * (rr + dr))
        poli(esc, [q[0], q[1], q[3], q[2]], CORAL, hacia=ne)

    # manta coral con franjas crema que asoma por dentro, con una punta sobre la solapa derecha, y una almohada
    man = Malla("LUN-04_manta")
    nu, nv = 4, 3
    xs = np.linspace(-w / 2 + g + 0.005, w / 2 - g - 0.005, nu + 1)
    zs = np.linspace(-d / 2 + g + 0.005, d / 2 - g - 0.005, nv + 1)
    alt = np.array([[0.50 + 0.22 * (i / nu) + 0.12 * (1 - j / nv) + rng.uniform(-0.03, 0.03) for i in range(nu + 1)] for j in range(nv + 1)])
    alt[:, -1] = np.minimum(alt[:, -1] + 0.04, 0.86)
    franja = mezclar(PAL["crema"], BLANCO, 0.25)
    for j in range(nv):
        for i in range(nu):
            col = CORAL if i % 2 == 0 else franja
            P = [np.array([xs[i], alt[j][i], zs[j]]), np.array([xs[i + 1], alt[j][i + 1], zs[j]]),
                 np.array([xs[i + 1], alt[j + 1][i + 1], zs[j + 1]]), np.array([xs[i], alt[j + 1][i], zs[j + 1]])]
            k1, k2 = 1 + rng.normal(0, 0.05), 1 + rng.normal(0, 0.05)
            poli(man, [P[0], P[1], P[2]], col * k1, hacia=(0, 1, 0))
            poli(man, [P[0], P[2], P[3]], col * k2, hacia=(0, 1, 0))
    a_, b_, c_, d_, nrm = sx                      # solapa derecha: a delante, b detras
    f0, f1 = b_ + (a_ - b_) * 0.10, b_ + (a_ - b_) * 0.42
    sube = (c_ - b_)
    punta = [np.array([w / 2 - g - 0.005, 0.86, f0[2]]), np.array([w / 2 - g - 0.005, 0.86, f1[2]]),
             f1 + sube * 0.72 + nrm * 0.016, f0 + sube * 0.62 + nrm * 0.016]
    poli(man, [punta[0], punta[1], f1 + nrm * 0.016, f0 + nrm * 0.016], CORAL * 0.96, hacia=(0, 1, 0))
    poli(man, [f0 + nrm * 0.016, f1 + nrm * 0.016, punta[2], punta[3]], hacia=nrm, cols=[CORAL, CORAL, franja, franja])
    rng_a = np.random.default_rng(44)
    alm = fibonacci(10) * rng_a.uniform(0.85, 1.1, (10, 1)) * np.array([0.26, 0.10, 0.17]) + np.array([-0.20, 0.72, -0.10])
    man.anexar(solido("almohada", alm, mezclar(BOLSA, SOMBRA, 0.30), BOLSA, mezclar(BOLSA, BLANCO, 0.5), rng_a, var=0.03))

    # antena de pajita con bolita de papel de aluminio
    ant = Malla("LUN-04_antena")
    b0 = np.array([w / 2 - 0.08, h, -d / 2 + 0.08])
    b1 = b0 + np.array([0.03, 0.36, -0.02])
    b2 = b1 + np.array([0.16, 0.12, -0.04])
    for k in range(4):
        barra(ant, b0 + (b1 - b0) * k / 4, b0 + (b1 - b0) * (k + 1) / 4, 0.014, PAL["coral"] if k % 2 == 0 else BLANCO, lados=5, tapas=False)
    barra(ant, b1, b2, 0.014, BLANCO, PAL["coral"], lados=5)
    bola = fibonacci(10) * 0.05 + b2
    ant.anexar(solido("bola", bola, METAL_OSC, METAL, mezclar(METAL, BLANCO, 0.6), rng, var=0.08))

    # linterna pequena pegada con cinta en el lado +X, apuntando a +Z; el lente brilla
    lin = Malla("LUN-04_linterna")
    luz = Malla("LUN-04_lente", "Emisivo")
    xl, yl = w / 2 + 0.048, 0.715
    barra(lin, (xl, yl, 0.14), (xl, yl, 0.36), 0.036, METAL_OSC, METAL, lados=6)
    barra(lin, (xl, yl, 0.36), (xl, yl, 0.435), 0.040, METAL, mezclar(METAL, BLANCO, 0.35), lados=6, r1=0.056)
    disco(luz, (xl, yl, 0.437), (0, 0, 1), 0.046, PAL["cian"], lados=8)
    for z0, z1 in ((0.18, 0.23), (0.29, 0.33)):
        tira([(xl - 0.048 + 0.002, yl - 0.07, z0), (xl - 0.048 + 0.002, yl - 0.07, z1), (xl + 0.046, yl + 0.012, z1), (xl + 0.046, yl + 0.012, z0)], (0.6, 0.8, 0))
        tira([(xl - 0.048 + 0.002, yl + 0.075, z0), (xl - 0.048 + 0.002, yl + 0.075, z1), (xl + 0.046, yl + 0.012, z1), (xl + 0.046, yl + 0.012, z0)], (0.6, 0.8, 0))
    guardar2("LUN-04", [("LUN-04_caja_de_carton", [m, dib, esc, man, ant, lin, luz], (0, 0, 0))])


# ---------- LUN-12 baliza de camino ----------

def baliza_camino():
    m = Malla("LUN-12_cuerpo")
    luz = Malla("LUN-12_luz", "Emisivo")
    plata = mezclar(METAL, BLANCO, 0.30)
    # base lastrada de tres pies
    torno_n(m, [(0.085, 0.0, METAL_OSC), (0.085, 0.045, METAL), (0.045, 0.075, plata), (0.0, 0.075, plata)], 6)
    for k in range(3):
        a = k * 2 * math.pi / 3 + math.pi / 2
        d = np.array([math.cos(a), 0, math.sin(a)])
        tubo(m, d * 0.06 + Y * 0.035, d * 0.26 + Y * 0.012, 0.020, METAL, METAL_OSC, lados=4, r1=0.014, tapas=False)
        torno_n(m, [(0.040, 0.0, METAL_OSC), (0.026, 0.022, METAL), (0.0, 0.022, METAL)], 5, centro=d * 0.27)
    # mastil fino
    tubo(m, (0, 0.07, 0), (0, 0.79, 0), 0.016, METAL_OSC, plata, lados=5, tapas=False)
    # aro reflector
    torno_n(m, [(0.022, 0.615, METAL_OSC), (0.088, 0.622, METAL), (0.088, 0.655, mezclar(BLANCO, PAL["brillo"], 0.3)),
                (0.022, 0.662, plata)], 8)
    # portalampara y lampara cian
    torno_n(m, [(0.020, 0.77, METAL_OSC), (0.050, 0.795, METAL), (0.0, 0.795, METAL_OSC)], 6)
    octaedro(luz, (0, 0.865, 0), 0.062, PAL["cian"], alto=1.35)
    torno_n(luz, [(0.024, 0.40, PAL["cian_medio"]), (0.024, 0.45, PAL["cian"])], 5)
    guardar2("LUN-12", [("LUN-12_baliza_de_camino", [m, luz], (0, 0, 0))])


# ---------- LUN-13 instrumento A: estacion de medicion ----------

def estacion_medicion():
    rng = np.random.default_rng(13)
    m = Malla("LUN-13_cuerpo")
    luz = Malla("LUN-13_luz", "Emisivo")
    plata = mezclar(METAL, BLANCO, 0.30)
    blanco = mezclar(BLANCO, METAL, 0.12)
    # caja baja envuelta en lamina dorada sobre cuatro patas cortas
    cx = -0.06
    for sx in (-1, 1):
        for sz in (-1, 1):
            tubo(m, (cx + sx * 0.20, 0.0, sz * 0.14), (cx + sx * 0.19, 0.14, sz * 0.13), 0.022, METAL_OSC, METAL, lados=4, tapas=False)
            torno_n(m, [(0.045, 0.0, METAL_OSC), (0.030, 0.02, METAL), (0.0, 0.02, METAL)], 5, centro=(cx + sx * 0.20, 0, sz * 0.14))
    caja_lamina(m, (cx, 0.29, 0.0), (0.50, 0.30, 0.38), FAM["oro"], rng, div=(2, 1, 2), relieve=(-0.010, 0.028))
    bloque(m, (cx, 0.135, 0.0), (0.46, 0.02, 0.34), METAL_OSC, sombra=0.2, base=True)
    octaedro(luz, (cx + 0.19, 0.39, 0.195), 0.020, PAL["cian"], alto=1.0)
    # panel solar pequeno inclinado, a un lado (-X), en un brazo
    px_, py_ = -0.47, 0.50
    tubo(m, (cx - 0.25, 0.36, 0.0), (px_, py_ - 0.03, 0.0), 0.016, METAL_OSC, METAL, lados=4, tapas=False)
    inc = math.radians(34)
    ejx, ejy = np.array([1.0, 0, 0]), np.array([0, math.sin(inc), -math.cos(inc)])       # ejy sube y se aleja
    nrm = np.cross(ejx, ejy)                                                        # mira arriba y a +Z
    cp = np.array([px_, py_, 0.0])
    aw, ah = 0.15, 0.20
    esq = [cp - ejx * aw - ejy * ah, cp + ejx * aw - ejy * ah, cp + ejx * aw + ejy * ah, cp - ejx * aw + ejy * ah]
    poli(m, [q - nrm * 0.02 for q in esq], METAL_OSC, hacia=-nrm)
    for i in range(4):
        j = (i + 1) % 4
        poli(m, [esq[i], esq[j], esq[j] - nrm * 0.02, esq[i] - nrm * 0.02], plata, interior=cp - nrm * 0.01)
    for i in range(2):
        for j in range(3):
            q0 = cp + ejx * (-aw + 0.012 + i * (aw - 0.006)) + ejy * (-ah + 0.012 + j * (2 * ah - 0.012) / 3) + nrm * 0.001
            q = [q0, q0 + ejx * (aw - 0.018), q0 + ejx * (aw - 0.018) + ejy * ((2 * ah - 0.012) / 3 - 0.012), q0 + ejy * ((2 * ah - 0.012) / 3 - 0.012)]
            col = mezclar(PANEL_SOLAR, PANEL_SOLAR_LUZ, 0.25 + 0.5 * ((i + j) % 2))
            poli(m, q, hacia=nrm, cols=[col, col, mezclar(col, PANEL_SOLAR_LUZ, 0.4), mezclar(col, PANEL_SOLAR_LUZ, 0.4)])
    # mastil de 1,0 m con cabeza de sensor blanca con aletas
    mx, mz = cx + 0.10, -0.27
    torno_n(m, [(0.07, 0.0, METAL_OSC), (0.045, 0.03, METAL), (0.0, 0.03, METAL)], 6, centro=(mx, 0, mz))
    tubo(m, (mx, 0.02, mz), (mx, 1.00, mz), 0.017, METAL_OSC, plata, lados=5, tapas=False)
    tubo(m, (mx, 0.34, mz), (mx, 0.34, -0.19), 0.013, METAL_OSC, lados=3, tapas=False)
    torno_n(m, [(0.050, 0.98, mezclar(blanco, SOMBRA, 0.3)), (0.050, 1.10, blanco), (0.0, 1.10, mezclar(blanco, PAL["brillo"], 0.3))], 6, centro=(mx, 0, mz))
    for ya in (1.005, 1.04, 1.075):
        torno_n(m, [(0.050, ya, METAL), (0.095, ya + 0.004, plata), (0.050, ya + 0.008, blanco)], 6, centro=(mx, 0, mz), giro=0.5)
    # cable por el suelo hasta un sensor en forma de disco a 0,8 m en +X
    tramo = [np.array(q, float) for q in ((cx + 0.25, 0.20, 0.06), (0.30, 0.012, 0.13), (0.45, 0.012, 0.05), (0.58, 0.012, 0.11), (0.72, 0.03, 0.03))]
    for a, b in zip(tramo[:-1], tramo[1:]):
        tubo(m, a, b, 0.010, METAL_OSC, mezclar(METAL_OSC, PAL["piedra"], 0.3), lados=3, tapas=False)
    torno_n(m, [(0.110, 0.0, METAL_OSC), (0.115, 0.035, METAL), (0.085, 0.055, plata), (0.035, 0.060, blanco), (0.0, 0.075, blanco)],
            8, centro=(0.80, 0, 0.0), rng=rng, s=0.03)
    guardar2("LUN-13", [("LUN-13_estacion_de_medicion", [m, luz], (0, 0, 0))])


# ---------- LUN-14 espejo de la Tierra ----------

def espejo_tierra():
    rng = np.random.default_rng(14)
    m = Malla("LUN-14_cuerpo")
    ref = Malla("LUN-14_reflejo", "Pintura")
    inc = math.radians(35)                         # el espejo se recuesta 35 grados respecto del suelo
    ex = np.array([1.0, 0, 0])
    ey = np.array([0, math.sin(inc), -math.cos(inc)])          # hacia arriba del espejo: sube y se aleja
    n = np.cross(ex, ey)                                        # mira a +Z y hacia arriba
    R = 0.31
    c = np.array([0, 0.045 + R * math.sin(inc) + 0.02, 0.02])

    def P(u, v, capa=0):
        return c + ex * u + ey * v + n * (0.004 * capa)

    # aro de carton con canto, y cinta
    lados = 16
    aro = 0.365
    onda = lambda t: 1 + 0.02 * math.sin(4 * t + 1.0)  # noqa: E731
    anillo(m, c + n * 0.006, ex, ey, R - 0.004, aro, mezclar(CARTON, PAL["crema"], 0.30), CARTON, lados=lados, hacia=n, onda=onda)
    ts = np.linspace(0, 2 * math.pi, lados + 1)
    for i in range(lados):
        q0 = c + (ex * math.cos(ts[i]) + ey * math.sin(ts[i])) * aro * onda(ts[i])
        q1 = c + (ex * math.cos(ts[i + 1]) + ey * math.sin(ts[i + 1])) * aro * onda(ts[i + 1])
        poli(m, [q0 + n * 0.006, q1 + n * 0.006, q1 - n * 0.022, q0 - n * 0.022], CANTO if i % 2 == 0 else mezclar(CANTO, CARTON_OSC, 0.38),
             hacia=unit((q0 + q1) / 2 - c))
    disco(m, c - n * 0.022, -n, aro, mezclar(CARTON_OSC, SOMBRA, 0.3), lados=lados)
    for a in (0.5, 2.4, 4.3):
        d1, d2 = ex * math.cos(a) + ey * math.sin(a), -ex * math.sin(a) + ey * math.cos(a)
        q = c + n * 0.011 + d1 * 0.335
        poli(m, [q - d1 * 0.06 - d2 * 0.03, q + d1 * 0.05 - d2 * 0.03, q + d1 * 0.05 + d2 * 0.03, q - d1 * 0.06 + d2 * 0.03], CINTA, hacia=n)
    # caballete bajo de carton: dos costillas y una pata de papel de aluminio
    yb = c[1] + ey[1] * 0.20
    zb = c[2] + ey[2] * 0.20 - 0.03
    for s in (-1, 1):
        x = s * 0.17
        p0, p1, p2 = np.array([x, 0.0, c[2] + 0.20]), np.array([x, 0.0, zb - 0.02]), np.array([x, yb, zb])
        t = np.array([0.02 * s, 0, 0])
        poli(m, [p0, p1, p2], hacia=(s, 0, 0), cols=[mezclar(CARTON, SOMBRA, 0.3), mezclar(CARTON, SOMBRA, 0.3), CARTON])
        poli(m, [p0 - t, p1 - t, p2 - t], mezclar(CARTON_OSC, SOMBRA, 0.25), hacia=(-s, 0, 0))
        poli(m, [p1, p2, p2 - t, p1 - t], CANTO, hacia=(0, 0.2, -1))
    pata0 = c + ey * 0.26 - n * 0.02
    pata1 = np.array([0.0, 0.0, pata0[2] - 0.20])
    tubo(m, pata0, pata1, 0.020, mezclar(METAL, BLANCO, 0.45), METAL, lados=5, rng=rng, s=0.08)
    bola = fibonacci(9) * rng.uniform(0.8, 1.15, (9, 1)) * 0.05 + pata1 + Y * 0.03
    m.anexar(solido("bola", bola, METAL_OSC, METAL, mezclar(METAL, BLANCO, 0.6), rng, var=0.08))

    # el reflejo: cielo azul noche, la Tierra casi llena y tres estrellas (material «Pintura», sin luz)
    borde_c, centro_c = NOCHE, mezclar(NOCHE, PAL["petroleo"], 0.35)
    ts = np.linspace(0, 2 * math.pi, 21)
    for i in range(20):
        poli(ref, [P(0, 0), P(R * math.cos(ts[i]), R * math.sin(ts[i])), P(R * math.cos(ts[i + 1]), R * math.sin(ts[i + 1]))],
             hacia=n, cols=[centro_c, borde_c, borde_c])
    eu, ev, rt = 0.025, 0.012, 0.18
    mar = mezclar(PAL["petroleo"], PAL["cian_medio"], 0.42)
    mar_hondo = mezclar(PAL["petroleo"], NOCHE, 0.25)
    halo = mezclar(PAL["petroleo"], PAL["brillo"], 0.48)
    ts = np.linspace(0, 2 * math.pi, 19)
    for i in range(18):
        a0, a1 = ts[i], ts[i + 1]
        poli(ref, [P(eu + (rt + 0.014) * math.cos(a0), ev + (rt + 0.014) * math.sin(a0), 1), P(eu + (rt + 0.014) * math.cos(a1), ev + (rt + 0.014) * math.sin(a1), 1),
                   P(eu + rt * math.cos(a1), ev + rt * math.sin(a1), 1), P(eu + rt * math.cos(a0), ev + rt * math.sin(a0), 1)],
             hacia=n, cols=[mezclar(halo, NOCHE, 0.55), mezclar(halo, NOCHE, 0.55), halo, halo])
        poli(ref, [P(eu + 0.03, ev + 0.03, 2), P(eu + rt * math.cos(a0), ev + rt * math.sin(a0), 2), P(eu + rt * math.cos(a1), ev + rt * math.sin(a1), 2)],
             hacia=n, cols=[mar, mar_hondo, mar_hondo])
    verde = mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.45)
    ocre = mezclar(PAL["hierba_sol"], PAL["tierra1"], 0.50)

    def tierra(pts, col, col2=None, capa=3):
        col2 = col if col2 is None else col2
        poli(ref, [P(eu + x, ev + y, capa) for x, y in pts], hacia=n, cols=[col if k % 2 == 0 else col2 for k in range(len(pts))])

    tierra([(-0.110, 0.070), (-0.060, 0.022), (0.005, 0.030), (0.040, 0.085), (-0.010, 0.128), (-0.075, 0.118)], verde, ocre)      # norte
    tierra([(-0.004, 0.034), (0.030, -0.022), (0.048, -0.014), (0.020, 0.036)], ocre, verde)                                       # istmo
    tierra([(0.026, -0.018), (0.040, -0.120), (0.062, -0.150), (0.098, -0.075), (0.090, -0.032), (0.052, -0.010)], verde, ocre)    # sur
    nube = mezclar(PAL["brillo"], PAL["crema"], 0.12)
    for pts in ([(-0.150, -0.020), (-0.085, -0.060), (-0.020, -0.052), (-0.090, -0.028)],
                [(-0.060, -0.105), (0.000, -0.128), (0.030, -0.110), (-0.025, -0.095)],
                [(0.050, 0.110), (0.105, 0.085), (0.135, 0.040), (0.088, 0.070)],
                [(-0.045, 0.150), (0.010, 0.158), (0.045, 0.140), (-0.005, 0.138)],
                [(0.095, -0.010), (0.150, -0.030), (0.140, -0.070), (0.110, -0.040)]):
        tierra(pts, nube, mezclar(nube, halo, 0.35), capa=4)
    # franja estrecha en sombra a la izquierda: el terminador es media elipse (Tierra casi llena)
    sombra_t = mezclar(NOCHE, PAL["petroleo"], 0.25)
    k_term = 0.74
    fs = np.linspace(math.pi / 2, 3 * math.pi / 2, 11)
    for i in range(10):
        q = [P(eu + rt * math.cos(fs[i]), ev + rt * math.sin(fs[i]), 5), P(eu + rt * k_term * math.cos(fs[i]), ev + rt * math.sin(fs[i]), 5),
             P(eu + rt * k_term * math.cos(fs[i + 1]), ev + rt * math.sin(fs[i + 1]), 5), P(eu + rt * math.cos(fs[i + 1]), ev + rt * math.sin(fs[i + 1]), 5)]
        poli(ref, q, hacia=n, cols=[sombra_t, mezclar(sombra_t, mar_hondo, 0.45), mezclar(sombra_t, mar_hondo, 0.45), sombra_t])
    for (u, v, rr, gg) in ((-0.205, 0.165, 0.026, 0.2), (0.215, -0.165, 0.022, 0.0), (0.235, 0.120, 0.016, 0.4)):
        estrella4(ref, P(u, v, 1), ex, ey, rr, mezclar(PAL["crema"], PAL["brillo"], 0.5), n, giro=gg)
    guardar2("LUN-14", [("LUN-14_espejo_de_la_tierra", [m, ref], (0, 0, 0))])


# ---------- LUN-15 soporte de herramientas y bolsas de muestras ----------

def soporte_y_bolsas():
    rng = np.random.default_rng(15)
    m = Malla("LUN-15_soporte")
    plata = mezclar(METAL, BLANCO, 0.30)
    # tripode de 1,0 m con aro
    cima = np.array([0, 0.95, -0.02])
    pies = []
    for k in range(3):
        a = k * 2 * math.pi / 3 - math.pi / 2          # un pie atras y dos delante
        pie = np.array([math.cos(a) * 0.30, 0.0, math.sin(a) * 0.30 - 0.02])
        pies.append(pie)
        tubo(m, pie, cima, 0.018, METAL_OSC, plata, lados=4, tapas=False)
        torno_n(m, [(0.045, 0.0, METAL_OSC), (0.030, 0.02, METAL), (0.0, 0.02, METAL)], 5, centro=(pie[0], 0, pie[2]))
    torno_n(m, [(0.030, 0.93, METAL_OSC), (0.045, 0.95, METAL), (0.030, 1.00, plata), (0.0, 1.00, plata)], 6, centro=(0, 0, -0.02))
    ya, ra = 0.74, 0.21
    ca = np.array([0, ya, -0.02])
    n_aro = 9
    pts_aro = [ca + np.array([math.cos(t) * ra, 0, math.sin(t) * ra]) for t in np.arange(n_aro) / n_aro * 2 * math.pi]
    for i in range(n_aro):
        tubo(m, pts_aro[i], pts_aro[(i + 1) % n_aro], 0.012, METAL, plata, lados=3, tapas=False)
    for pie in pies:
        en_pata = pie + (cima - pie) * (ya / 0.95)
        fuera = unit([en_pata[0] - ca[0], 0, en_pata[2] - ca[2]])
        tubo(m, en_pata, ca + fuera * ra, 0.010, METAL_OSC, lados=3, tapas=False)

    def colgar(ang_g):
        a = math.radians(ang_g)
        q = ca + np.array([math.cos(a) * ra, 0, math.sin(a) * ra])
        tubo(m, q + Y * 0.012, q - Y * 0.05, 0.007, METAL_OSC, lados=3, tapas=False)
        return q - Y * 0.05

    h = Malla("LUN-15_herramientas")
    # pinzas: dos varillas en V estrecha
    q = colgar(140)
    for s in (-1, 1):
        tubo(h, q, q + np.array([s * 0.035, -0.40, 0.0]), 0.009, METAL_OSC, plata, lados=3, tapas=False)
        tubo(h, q + np.array([s * 0.035, -0.40, 0.0]), q + np.array([s * 0.008, -0.47, 0.0]), 0.008, plata, lados=3)
    torno_n(h, [(0.022, q[1] - 0.10, METAL_OSC), (0.022, q[1] - 0.075, METAL)], 5, centro=(q[0], 0, q[2]))
    # cucharon de mango largo, boca abajo: mango y cuchara en forma de caja abierta
    q = colgar(65)
    tubo(h, q, q - Y * 0.52, 0.012, METAL_OSC, plata, lados=4, tapas=False)
    cc = q - Y * 0.57
    claro = mezclar(METAL, BLANCO, 0.40)
    bloque(h, cc + np.array([0, 0.045, 0]), (0.13, 0.012, 0.10), claro)
    bloque(h, cc + np.array([0, 0, -0.045]), (0.13, 0.09, 0.012), claro)
    bloque(h, cc + np.array([0.060, 0, 0]), (0.012, 0.09, 0.10), mezclar(claro, METAL_OSC, 0.3))
    bloque(h, cc + np.array([-0.060, 0, 0]), (0.012, 0.09, 0.10), mezclar(claro, METAL_OSC, 0.3))
    # martillo colgado del mango
    q = colgar(15)
    tubo(h, q, q - Y * 0.30, 0.012, mezclar(PAL["madera1"], PAL["tierra2"], 0.3), mezclar(PAL["madera1"], PAL["tierra1"], 0.4), lados=4, tapas=False)
    bloque(h, q - Y * 0.33, (0.13, 0.06, 0.06), mezclar(METAL_OSC, PAL["piedra_osc"], 0.3), sombra=0.3, luz=0.3)

    # cuatro bolsas de muestra con la boca doblada y cinta, marcadas con 1 a 4 puntos coral
    b = Malla("LUN-15_bolsas")
    pun = Malla("LUN-15_puntos")
    lona, lona_luz, lona_pie = BOLSA, mezclar(BOLSA, BLANCO, 0.5), mezclar(BOLSA, mezclar(SOMBRA, PAL["piedra"], 0.5), 0.45)
    patrones = {1: [(0, 0)], 2: [(-0.3, -0.3), (0.3, 0.3)], 3: [(-0.36, -0.36), (0, 0), (0.36, 0.36)], 4: [(-0.3, -0.3), (0.3, -0.3), (-0.3, 0.3), (0.3, 0.3)]}

    def bolsa(pos, giro, cuantos, abierta=False, tam=(0.24, 0.115, 0.19)):
        Rg = rot_y(giro)
        ax, alto, az = tam[0] / 2, tam[1], tam[2] / 2

        def W(x, y, z):
            return np.asarray(pos, float) + Rg @ np.array([x, y, z])

        # cuerpo: base ancha y cara de arriba mas pequena e inclinada hacia la camara
        base = [W(-ax, 0, -az), W(ax, 0, -az), W(ax, 0, az), W(-ax, 0, az)]
        k = 0.80
        tapa = [W(-ax * k, alto * 1.12, -az * k), W(ax * k, alto * 1.12, -az * k), W(ax * k, alto * 0.80, az * k), W(-ax * k, alto * 0.80, az * k)]
        dentro = W(0, alto * 0.4, 0)
        for i in range(4):
            j = (i + 1) % 4
            v = 1 + rng.normal(0, 0.04)
            poli(b, [base[i], base[j], tapa[j], tapa[i]], interior=dentro, cols=[lona_pie * v, lona_pie * v, lona * v, lona * v])
        nt = unit(np.cross(tapa[1] - tapa[0], tapa[3] - tapa[0]))
        nt = nt if nt[1] > 0 else -nt
        ct = sum(tapa) / 4
        ux, uz = (tapa[1] - tapa[0]) / 2, (tapa[3] - tapa[0]) / 2
        if abierta:
            # boca abierta: un cerco de lona y suelo oscuro dentro
            for i in range(4):
                j = (i + 1) % 4
                arriba = [tapa[i] + nt * 0.035 + (tapa[i] - ct) * 0.10, tapa[j] + nt * 0.035 + (tapa[j] - ct) * 0.10]
                poli(b, [tapa[i], tapa[j], arriba[1], arriba[0]], interior=ct, cols=[lona, lona, lona_luz, lona_luz])
                poli(b, [tapa[i], tapa[j], arriba[1], arriba[0]], mezclar(lona_pie, SOMBRA, 0.3), hacia=ct + nt * 0.02 - (tapa[i] + tapa[j]) / 2)
            suelo = mezclar(BASALTO, PAL["piedra"], 0.25)
            poli(b, [q + nt * 0.012 for q in tapa], hacia=nt, cols=[suelo, suelo * 1.1, suelo * 0.95, suelo * 1.05])
        else:
            poli(b, tapa, hacia=nt, cols=[lona_luz, lona_luz, lona, lona])
            # boca doblada: una solapa a lo largo del borde de atras, sujeta con cinta
            a0, a1 = tapa[0] + nt * 0.004, tapa[1] + nt * 0.004
            doblez = [a0, a1, a1 + uz * 0.55 + nt * 0.012, a0 + uz * 0.55 + nt * 0.012]
            poli(b, doblez, hacia=nt, cols=[lona, lona, mezclar(lona, lona_pie, 0.45), mezclar(lona, lona_pie, 0.45)])
            cinta_c = ct - uz * 0.72
            poli(b, [cinta_c - ux * 0.28 - uz * 0.45 + nt * 0.017, cinta_c + ux * 0.28 - uz * 0.45 + nt * 0.017,
                     cinta_c + ux * 0.28 + uz * 0.62 + nt * 0.019, cinta_c - ux * 0.28 + uz * 0.62 + nt * 0.019], CINTA * 0.93, hacia=nt)
            # puntos coral en la mitad delantera de la cara de arriba
            cpun = ct + uz * 0.42
            for (px_, pz_) in patrones[cuantos]:
                q = cpun + ux * px_ * 0.95 + uz * pz_ * 0.62 + nt * 0.005
                rr = 0.017
                e1, e2 = unit(ux), unit(uz)
                poli(pun, [q - e1 * rr, q + e2 * rr, q + e1 * rr, q - e2 * rr], CORAL, hacia=nt)

    bolsa((-0.44, 0, 0.26), 0.35, 1)
    bolsa((-0.15, 0, 0.40), -0.12, 2)
    bolsa((0.17, 0, 0.38), 0.10, 3)
    bolsa((0.46, 0, 0.20), -0.40, 4, abierta=False)
    bolsa((0.36, 0, -0.16), 0.5, 0, abierta=True, tam=(0.22, 0.15, 0.20))
    guardar2("LUN-15", [("LUN-15_soporte_y_bolsas", [m, h, b, pun], (0, 0, 0))])


# ---------- LUN-16 muestras sueltas ----------

def muestras_sueltas():
    nodos = []
    # a: basalto oscuro azulado, en bloque
    rng = np.random.default_rng(161)
    pts = puntos_roca(rng, 9, alto=0.13, fondo=0.85, radio=(0.75, 1.1), cortes=2) * np.array([0.20, 1, 0.20])
    nodos.append(("LUN-16_a", [solido("LUN-16_a", pts, BASALTO_PIE, BASALTO, BASALTO_LUZ, rng)], (0, 0, 0)))
    # b: roca clara angulosa, en esquirla alargada
    rng = np.random.default_rng(162)
    pts = np.array([[-0.5, 0, -0.16], [0.42, 0, -0.22], [0.5, 0, 0.12], [-0.38, 0, 0.2], [-0.2, 0.46, 0.0], [0.28, 0.62, -0.04], [0.44, 0.3, 0.02]], float)
    pts += rng.normal(0, 0.02, pts.shape)
    pts[:, 1] = np.maximum(pts[:, 1], 0)
    pts = pts * np.array([0.22, 0.22, 0.22])
    nodos.append(("LUN-16_b", [solido("LUN-16_b", pts, mezclar(FRESCA_PIE, FRESCA, 0.3), FRESCA, FRESCA_LUZ, rng)], (0, 0, 0)))
    # c: terron de regolito, redondeado y bajo
    rng = np.random.default_rng(163)
    pts = puntos_roca(rng, 11, alto=0.10, fondo=0.9, radio=(0.9, 1.08), cortes=0, piso=0.55) * np.array([0.18, 1, 0.18])
    nodos.append(("LUN-16_c", [solido("LUN-16_c", pts, mezclar(TERRON, PAL["petroleo"], 0.40), TERRON, mezclar(TERRON, PAL["crema"], 0.40), rng)], (0, 0, 0)))
    for _, mallas, _ in nodos:
        ajustar_caja(mallas[0])
    guardar2("LUN-16", nodos)


# ---------- LUN-17 instrumento B ----------

def instrumento_b():
    rng = np.random.default_rng(17)
    m = Malla("LUN-17_cuerpo")
    plata = mezclar(METAL, BLANCO, 0.30)
    blanco = mezclar(BLANCO, METAL, 0.15)
    # falda de lamina dorada arrugada, extendida en el suelo
    sect = 12
    radios = [0.70 * rng.uniform(0.86, 1.08) for _ in range(sect)]
    for i in range(sect):
        j = (i + 1) % sect
        a0, a1 = i / sect * 2 * math.pi, (i + 1) / sect * 2 * math.pi
        d0, d1 = np.array([math.cos(a0), 0, math.sin(a0)]), np.array([math.cos(a1), 0, math.sin(a1)])
        dm = unit(d0 + d1)
        f = FAM["oro"] if i % 3 else FAM["nar"]
        col = jit(f[0], rng, 0.07)
        dentro0, dentro1 = d0 * 0.24 + Y * 0.035, d1 * 0.24 + Y * 0.035
        medio = dm * 0.47 + Y * rng.uniform(0.012, 0.045)
        fuera0, fuera1 = d0 * radios[i] + Y * 0.012, d1 * radios[j] + Y * 0.012
        poli(m, [dentro0, dentro1, medio], hacia=Y, cols=[mezclar(col, f[1], 0.5), mezclar(col, f[1], 0.5), col])
        poli(m, [dentro0, medio, fuera0], hacia=Y, cols=[mezclar(col, f[1], 0.5), col, mezclar(col, f[2], 0.4)])
        poli(m, [dentro1, fuera1, medio], hacia=Y, cols=[mezclar(col, f[1], 0.5), mezclar(col, f[2], 0.4), col])
        poli(m, [medio, fuera1, fuera0], hacia=Y, cols=[col * 1.04, mezclar(col, f[2], 0.45), mezclar(col, f[2], 0.45)])
    # tambor bajo
    torno_n(m, [(0.25, 0.03, mezclar(blanco, SOMBRA, 0.45)), (0.25, 0.17, mezclar(blanco, SOMBRA, 0.15)), (0.255, 0.17, ORO_OSC), (0.255, 0.215, ORO),
                (0.25, 0.215, blanco), (0.25, 0.30, blanco), (0.20, 0.33, mezclar(blanco, PAL["brillo"], 0.3)), (0.0, 0.33, blanco)], 10, rng=rng, s=0.03)
    bloque(m, (0, 0.35, 0), (0.16, 0.04, 0.10), METAL_OSC, sombra=0.2, luz=0.3, base=False)
    # dos paneles solares pequenos en brazos laterales
    inc = math.radians(30)
    ejy = np.array([0, math.sin(inc), -math.cos(inc)])
    for s in (-1, 1):
        tubo(m, (s * 0.24, 0.24, 0), (s * 0.40, 0.30, 0), 0.014, METAL_OSC, METAL, lados=4, tapas=False)
        ejx = np.array([1.0, 0, 0])
        nrm = np.cross(ejx, ejy)
        cp = np.array([s * 0.54, 0.31, 0.0])
        aw, ah = 0.15, 0.115
        esq = [cp - ejx * aw - ejy * ah, cp + ejx * aw - ejy * ah, cp + ejx * aw + ejy * ah, cp - ejx * aw + ejy * ah]
        poli(m, [q - nrm * 0.018 for q in esq], METAL_OSC, hacia=-nrm)
        for i in range(4):
            j = (i + 1) % 4
            poli(m, [esq[i], esq[j], esq[j] - nrm * 0.018, esq[i] - nrm * 0.018], plata, interior=cp - nrm * 0.009)
        for i in range(2):
            q0 = cp + ejx * (-aw + 0.010 + i * aw) + ejy * (-ah + 0.010) + nrm * 0.001
            q = [q0, q0 + ejx * (aw - 0.020), q0 + ejx * (aw - 0.020) + ejy * (2 * ah - 0.020), q0 + ejy * (2 * ah - 0.020)]
            col = mezclar(PANEL_SOLAR, PANEL_SOLAR_LUZ, 0.25 + 0.5 * i)
            poli(m, q, hacia=nrm, cols=[col, col, mezclar(col, PANEL_SOLAR_LUZ, 0.4), mezclar(col, PANEL_SOLAR_LUZ, 0.4)])
    # varilla de antena con bolita
    v0, v1 = np.array([0.10, 0.33, -0.08]), np.array([0.16, 0.86, -0.14])
    tubo(m, v0, v1, 0.008, METAL_OSC, plata, lados=3, tapas=False)
    octaedro(m, v1 + Y * 0.02, 0.026, mezclar(METAL, BLANCO, 0.5), alto=1.0)
    guardar2("LUN-17", [("LUN-17_instrumento_de_superficie", [m], (0, 0, 0))])


# ---------- LUN-19 camara de carton ----------

def camara_carton():
    m = Malla("LUN-19_cuerpo")
    luz = Malla("LUN-19_lente", "Emisivo")
    plata = mezclar(METAL, BLANCO, 0.45)
    madera = mezclar(PAL["madera1"], PAL["tierra2"], 0.35)
    # tripode de varillas
    cima = np.array([0, 0.80, 0])
    for k in range(3):
        a = k * 2 * math.pi / 3 + math.pi / 2
        pie = np.array([math.cos(a) * 0.27, 0, math.sin(a) * 0.27])
        tubo(m, pie, cima - unit(pie) * (-0.02), 0.014, mezclar(madera, SOMBRA, 0.3), mezclar(madera, PAL["crema"], 0.25), lados=4, tapas=False)
        torno_n(m, [(0.030, 0.0, mezclar(madera, SOMBRA, 0.4)), (0.0, 0.03, madera)], 4, centro=(pie[0], 0, pie[2]))
    torno_n(m, [(0.035, 0.78, METAL_OSC), (0.060, 0.80, METAL), (0.060, 0.825, plata), (0.0, 0.825, plata)], 6)
    # la camara: una caja de carton
    cc = np.array([0, 0.915, 0])
    bloque(m, cc, (0.27, 0.18, 0.17), CARTON, sombra=0.32, luz=0.22, tapa=mezclar(CARTON, PAL["crema"], 0.30))
    # aro de papel de aluminio y lente, mirando a -Z
    zl = -0.085
    torno_dir = np.array([0, 0, -1.0])
    aro0 = [cc + np.array([math.cos(t) * 0.070, math.sin(t) * 0.070 + 0.0, zl]) for t in np.arange(8) / 8 * 2 * math.pi]
    aro1 = [cc + np.array([math.cos(t) * 0.062, math.sin(t) * 0.062, zl - 0.045]) for t in np.arange(8) / 8 * 2 * math.pi]
    den1 = [cc + np.array([math.cos(t) * 0.046, math.sin(t) * 0.046, zl - 0.045]) for t in np.arange(8) / 8 * 2 * math.pi]
    den0 = [cc + np.array([math.cos(t) * 0.046, math.sin(t) * 0.046, zl - 0.012]) for t in np.arange(8) / 8 * 2 * math.pi]
    eje_l = cc + np.array([0, 0, zl - 0.02])
    for i in range(8):
        j = (i + 1) % 8
        v = 1 + 0.07 * math.sin(i * 2.4)
        poli(m, [aro0[i], aro0[j], aro1[j], aro1[i]], interior=eje_l, cols=[METAL * v, METAL * v, plata * v, plata * v])
        poli(m, [aro1[i], aro1[j], den1[j], den1[i]], plata * v, hacia=torno_dir)
        poli(m, [den1[i], den1[j], den0[j], den0[i]], METAL_OSC, hacia=eje_l - (den1[i] + den1[j]) / 2)
    poli(luz, den0, PAL["cian"], hacia=torno_dir)
    # visor arriba, boton de crayon coral, pantalla dibujada detras y cinta
    bloque(m, cc + np.array([-0.07, 0.115, 0.01]), (0.08, 0.05, 0.09), mezclar(CARTON, CARTON_OSC, 0.4), sombra=0.25, luz=0.2, base=False)
    disco(m, cc + np.array([0.075, 0.0925, 0.02]), (0, 1, 0), 0.026, CORAL, lados=8)
    zt = 0.085 + 0.003
    poli(m, [cc + np.array([-0.10, -0.06, zt]), cc + np.array([0.06, -0.06, zt]), cc + np.array([0.06, 0.055, zt]), cc + np.array([-0.10, 0.055, zt])],
         CRAYON, hacia=(0, 0, 1))
    poli(m, [cc + np.array([-0.085, -0.045, zt + 0.003]), cc + np.array([0.045, -0.045, zt + 0.003]), cc + np.array([0.045, 0.04, zt + 0.003]), cc + np.array([-0.085, 0.04, zt + 0.003])],
         hacia=(0, 0, 1), cols=[NOCHE, NOCHE, mezclar(NOCHE, PAL["petroleo"], 0.5), mezclar(NOCHE, PAL["petroleo"], 0.5)])
    poli(m, [cc + np.array([0.135 + 0.003, -0.09, -0.03]), cc + np.array([0.135 + 0.003, -0.09, 0.03]), cc + np.array([0.135 + 0.003, 0.09, 0.03]), cc + np.array([0.135 + 0.003, 0.09, -0.03])],
         CINTA, hacia=(1, 0, 0))
    poli(m, [cc + np.array([0.105, 0.0925, -0.03]), cc + np.array([0.135, 0.0925, -0.03]), cc + np.array([0.135, 0.0925, 0.03]), cc + np.array([0.105, 0.0925, 0.03])],
         CINTA, hacia=(0, 1, 0))
    # piloto cian encima, del lado de la camara de juego: de frente el lente no se ve
    octaedro(luz, cc + np.array([0.02, 0.105, 0.055]), 0.016, PAL["cian"], alto=1.0)
    guardar2("LUN-19", [("LUN-19_camara_de_carton", [m, luz], (0, 0, 0))])


RECURSOS = (("LUN-02", rocas), ("LUN-10", piedras), ("LUN-11", eyecta), ("LUN-18", penascos), ("LUN-03", etapa_descenso),
            ("LUN-04", caja_capsula), ("LUN-12", baliza_camino), ("LUN-13", estacion_medicion), ("LUN-14", espejo_tierra),
            ("LUN-15", soporte_y_bolsas), ("LUN-16", muestras_sueltas), ("LUN-17", instrumento_b), ("LUN-19", camara_carton))


def main():
    global SALIDA
    solo = None
    for a in sys.argv[1:]:
        if a.startswith("--salida="):
            SALIDA = Path(a.split("=", 1)[1])
            SALIDA.mkdir(parents=True, exist_ok=True)
        elif a.startswith("--solo="):
            solo = set(a.split("=", 1)[1].split(","))
    for ident, fn in RECURSOS:
        if solo is None or ident in solo:
            fn()
    total = 0
    actual = None
    for ident, nombre, tris, lo, hi, materiales, subidos, minimo in INFORME:
        if ident != actual:
            suma = sum(f[2] for f in INFORME if f[0] == ident)
            print(f"{ident}: {suma} triangulos")
            actual = ident
            total += suma
        t = hi - lo
        print(f"    {nombre}: {tris} tri; caja {t[0]:.2f} x {t[1]:.2f} x {t[2]:.2f} m (x, y, z); y de {lo[1]:.2f} a {hi[1]:.2f}; "
              f"materiales {', '.join(materiales)}; luminancia minima {minimo:.2f}" + (f"; {subidos} colores subidos" if subidos else ""))
    print("total:", total)


if __name__ == "__main__":
    main()
