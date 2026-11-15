"""Escena del Mirador del Faro (zona «mirador» del juego jugable v0): plataforma, ladera y layout.

Concepto: Lote_03/L03_mirador_noche_vista_juego.png (sin veredicto de Guillermo: todo es PROVISIONAL).
La camara del juego mira hacia -Z, asi que el concepto (isometrico) se gira: la escalinata queda arriba a la
izquierda, el faro arriba a la derecha, la balaustrada curva abajo y a la derecha, y el barrio al este.

Escribe:
  juego/modelos/mirador/MIR-02.glb   plataforma: losas (6 trozos), balaustrada, bordillo, pilares y muro de contencion
  juego/modelos/mirador/TER-15.glb   ladera del cerro (ID nuevo): norte, oeste y fondo del valle
  juego/zonas/mirador/layout.json    recursos (formato de nucleo/constructor.gd) y "jugable": colisiones,
                                     entradas, umbrales, interactuables, guirnaldas, luces calidas y rutas
Los modelos sueltos (faro, telescopio, casas...) los escribe mirador_modelos.py: correr ese primero.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/mirador_modelos.py
    python -I herramientas/mallas/mirador_escena.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mirador_modelos as mm  # noqa: E402
from nucleo import PAL, RAIZ, Escena, Malla, mezclar  # noqa: E402

SALIDA = RAIZ / "juego" / "modelos" / "mirador"
ZONA = RAIZ / "juego" / "zonas" / "mirador"

# ---------- trazado (metros; -Z es arriba en pantalla y +X la derecha) ----------
W, E, N = -5.6, 6.2, -4.3              # bordes rectos de la terraza
CX, CZ, RX, RZ = 0.3, -0.6, 5.9, 4.6   # media elipse del lado sur
A_BAL = 150.0                          # la balaustrada cubre el arco de 150 a 0 grados
PORTON_Z = -1.9                        # centro del porton del cerro (borde este)
BAJ_X1, BAJ_Z0, BAJ_Z1 = 8.0, -3.2, -0.6   # descanso de la bajada de los faroles
ESC_X = -4.2                           # eje de la escalinata TER-11 (2,58 m de ancho)
FARO = (2.9, -2.9, -25.0)              # x, z, giro: la puerta mira a la terraza
TELESCOPIO = (3.3, 1.3, 8.0)
MESA = (0.2, -2.2, 0.0)
ATRIL = (-4.2, 0.4, 20.0)
BANCA = (-1.6, -3.85, 0.0)


def arco(a_grados, dentro=0.0):
    a = math.radians(a_grados)
    return np.array([CX + (RX - dentro) * math.cos(a), CZ + (RZ - dentro) * math.sin(a)])


def normal_arco(a_grados):
    a = math.radians(a_grados)
    n = np.array([math.cos(a) / RX, math.sin(a) / RZ])
    return n / np.linalg.norm(n)


def contorno():
    pts = [np.array([W, N]), np.array([W, CZ])]
    pts += [arco(a) for a in range(174, 0, -6)]
    pts += [np.array([E, CZ]), np.array([E, N])]
    return pts


def mundo(pos, giro_grados, local, escala=1.0):
    """Punto local de un modelo -> mundo (misma convencion que rotation.y de Godot)."""
    t = math.radians(giro_grados)
    x, y, z = (float(v) * escala for v in local)
    return [pos[0] + x * math.cos(t) + z * math.sin(t), pos[1] + y, pos[2] - x * math.sin(t) + z * math.cos(t)]


# ---------- poligonos en planta ----------

def recortar(poli, punto, normal):
    """Deja la parte del poligono con (p - punto) . normal <= 0."""
    sal = []
    n = len(poli)
    for i in range(n):
        a, b = poli[i], poli[(i + 1) % n]
        da, db = (a - punto) @ normal, (b - punto) @ normal
        if da <= 0:
            sal.append(a)
        if (da < 0 < db) or (db < 0 < da):
            sal.append(a + (b - a) * (da / (da - db)))
    return sal


def recortar_convexo(poli, region):
    cen = sum(region) / len(region)
    for i in range(len(region)):
        a, b = region[i], region[(i + 1) % len(region)]
        d = b - a
        n = np.array([-d[1], d[0]])
        if (cen - a) @ n > 0:
            n = -n
        poli = recortar(poli, a, n)
        if len(poli) < 3:
            return []
    return poli


def area(poli):
    return 0.5 * abs(sum(poli[i][0] * poli[(i + 1) % len(poli)][1] - poli[(i + 1) % len(poli)][0] * poli[i][1] for i in range(len(poli))))


def abanico(m: Malla, poli, y, c_centro, c_borde):
    cen = sum(poli) / len(poli)
    c3 = np.array([cen[0], y, cen[1]])
    for i in range(len(poli)):
        a, b = poli[i], poli[(i + 1) % len(poli)]
        pa, pb = np.array([a[0], y, a[1]]), np.array([b[0], y, b[1]])
        if np.cross(pa - c3, pb - c3)[1] < 0:
            pa, pb = pb, pa
        mm._tri(m, c3, pa, pb, c_centro, c_borde, c_borde)


def caja_dir(m: Malla, p, u, largo, alto, ancho, col, y0=0.0, rng=None, sombra_t=0.32, luz_t=0.12, var=0.05):
    """Caja centrada en p (planta), con su largo sobre el eje horizontal u."""
    u = np.asarray(u, float) / np.linalg.norm(u)
    v = np.array([-u[1], u[0]])
    f = 1.0 + (rng.normal(0, var) if rng is not None else 0.0)
    bajo, alto_c = mezclar(col, PAL["petroleo"], sombra_t) * f, mezclar(col, PAL["crema"], luz_t) * f
    esq = [p + u * sx * largo / 2 + v * sz * ancho / 2 for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    aba = [np.array([q[0], y0, q[1]]) for q in esq]
    arr = [np.array([q[0], y0 + alto, q[1]]) for q in esq]
    eje = np.array([p[0], y0 + alto / 2, p[1]])
    for i in range(4):
        k = (i + 1) % 4
        mm.cara(m, [aba[i], aba[k], arr[k], arr[i]], interior=eje, cols=[bajo, bajo, alto_c, alto_c])
    mm.cara(m, arr, alto_c, arriba=True)


# ---------- MIR-02 plataforma ----------

def abanico_v(m: Malla, poli, y, c_centro, cols_borde):
    """Como abanico, pero con un color propio en cada vertice del borde (musgo y desgaste por esquina)."""
    cen = sum(poli) / len(poli)
    c3 = np.array([cen[0], y, cen[1]])
    for i in range(len(poli)):
        j = (i + 1) % len(poli)
        a, b = poli[i], poli[j]
        pa, pb = np.array([a[0], y, a[1]]), np.array([b[0], y, b[1]])
        ca, cb = cols_borde[i], cols_borde[j]
        if np.cross(pa - c3, pb - c3)[1] < 0:
            pa, pb, ca, cb = pb, pa, cb, ca
        mm._tri(m, c3, pa, pb, c_centro, ca, cb)


# v2 (color): piedra con variacion calida y fria. La noche la tine de azul y violeta donde no llega la luz,
# y los faroles la vuelven dorada: por eso el tono base es malva claro y no melocoton.
# v2b (critica): losas pequenas (unos 0,45 m) que alternan crema calido (familia d6b48c) y gris frio, con una
# diferencia de luminosidad de 15 a 25 entre familias; junta fina de musgo verde a media luz, no casi negra.
TONOS_LOSA = [
    (mezclar(PAL["crema"], PAL["piedra"], 0.35), 0.30),                     # crema calido (d6b48c aprox.)
    (mezclar(PAL["tierra1"], PAL["piedra_clara"], 0.35), 0.22),             # rosa piedra calido
    (mezclar(PAL["crema"], PAL["tierra2"], 0.30), 0.10),                    # arena dorada
    (mezclar(PAL["piedra"], PAL["piedra_clara"], 0.40), 0.14),              # malva
    (mezclar(PAL["piedra_clara"], PAL["petroleo"], 0.30), 0.12),            # gris frio
    (mezclar(PAL["piedra"], PAL["petroleo"], 0.30), 0.12),                  # gris frio gastado (oscuro)
]
MUSGO = mezclar(mezclar(PAL["hierba_sombra"], PAL["hierba_sol"], 0.35), PAL["petroleo"], 0.22)
LIQUEN = [mezclar(PAL["hierba_sol"], PAL["piedra_clara"], 0.45), mezclar(PAL["dorado"], PAL["piedra_clara"], 0.55),
          mezclar(PAL["hierba_sombra"], PAL["piedra_clara"], 0.35)]
# losas de paso (gastadas y mas claras): de la llegada a la mesa, al telescopio y al atril
PASOS = [((-3.6, -1.5), (0.2, -1.2)), ((0.2, -1.2), (3.0, 1.2)), ((-3.6, -1.5), (-3.6, 0.9)), ((0.2, -1.2), (5.6, -1.9)),
         ((-1.6, -3.1), (-3.0, -1.6))]


def en_paso(p):
    for a, b in PASOS:
        a, b = np.array(a), np.array(b)
        t = np.clip((p - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1)
        if np.linalg.norm(p - (a + (b - a) * t)) < 0.75:
            return True
    return False


def losas(rng):
    """Losas irregulares (celdas de Voronoi con junta), repartidas en 3 x 2 trozos para que cada trozo reciba
    solo las luces calidas que tiene cerca."""
    region_a = contorno()
    region_b = [np.array(p) for p in ((E - 0.05, BAJ_Z0), (BAJ_X1, BAJ_Z0), (BAJ_X1, BAJ_Z1), (E - 0.05, BAJ_Z1))]
    paso = 0.47
    semillas = []
    for fila, z in enumerate(np.arange(N - 0.4, CZ + RZ + 0.5, paso * 0.88)):
        for x in np.arange(W - 0.4 + (paso * 0.5 if fila % 2 else 0.0), BAJ_X1 + 0.5, paso):
            semillas.append(np.array([x, z]) + rng.uniform(-0.15, 0.15, 2))
    semillas = np.array(semillas)
    colores = [c for c, _ in TONOS_LOSA]
    pesos = np.array([w for _, w in TONOS_LOSA])
    pesos = pesos / pesos.sum()
    cortes_x = [-1.8, 2.2]
    trozos = {(i, k): Malla(f"MIR-02_losas_{i}{k}") for i in range(3) for k in range(2)}
    n_losas = 0
    for s in semillas:
        celda = [s + np.array(d) * 1.1 for d in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        for o in semillas[np.linalg.norm(semillas - s, axis=1) < 1.5]:
            if o is s or np.allclose(o, s):
                continue
            celda = recortar(celda, (s + o) / 2, o - s)
            if len(celda) < 3:
                break
        if len(celda) < 3:
            continue
        for region in (region_a, region_b):
            trozo = recortar_convexo(list(celda), region)
            if len(trozo) < 3 or area(trozo) < 0.012:
                continue
            cen = sum(trozo) / len(trozo)
            radio = max(0.07, float(np.mean([np.linalg.norm(p - cen) for p in trozo])))
            junta = [cen + (p - cen) * (1.0 - 0.016 / radio) for p in trozo]
            col = np.asarray(colores[rng.choice(len(colores), p=pesos)], float) * (1.0 + rng.normal(0, 0.045))
            i = 0 if cen[0] < cortes_x[0] else (1 if cen[0] < cortes_x[1] else 2)
            k = 0 if cen[1] < -0.9 else 1
            # desgaste: las losas de paso tienen el centro pulido y claro y el borde gastado; cerca del borde de la
            # terraza y en una de cada cuatro losas, el musgo sube por las esquinas desde la junta
            cerca_borde = min(abs(cen[0] - W), abs(cen[1] - N)) < 1.0 or np.linalg.norm((cen - np.array([CX, CZ])) / np.array([RX, RZ])) > 0.85
            paso_gastado = en_paso(cen)
            musgosa = (cerca_borde and rng.random() < 0.7) or (not paso_gastado and rng.random() < 0.22)
            cols_borde = []
            for _ in junta:
                c = mezclar(col, PAL["petroleo"], 0.06) if not paso_gastado else mezclar(col, PAL["crema"], 0.10)
                if musgosa and rng.random() < 0.6:
                    c = mezclar(c, MUSGO, rng.uniform(0.40, 0.75))
                cols_borde.append(c)
            centro_c = mezclar(col, PAL["crema"], 0.24 if paso_gastado else 0.08)
            abanico_v(trozos[(i, k)], junta, 0.0, centro_c, cols_borde)
            # liquen: manchas pequenas y claras sobre una de cada cinco losas, nunca en las de paso
            if not paso_gastado and rng.random() < 0.20:
                for _ in range(rng.integers(1, 3)):
                    centro_l = cen + (junta[rng.integers(len(junta))] - cen) * rng.uniform(0.35, 0.75)
                    r_l = rng.uniform(0.03, 0.065)
                    pts = [centro_l + np.array([math.cos(a), math.sin(a)]) * r_l * rng.uniform(0.6, 1.0)
                           for a in np.linspace(0, 2 * math.pi, 7)[:-1] + rng.uniform(0, 1)]
                    lc = LIQUEN[rng.integers(len(LIQUEN))]
                    abanico(trozos[(i, k)], pts, 0.003, mezclar(lc, PAL["crema"], 0.1), mezclar(lc, col, 0.45))
            n_losas += 1
    # lecho de las juntas, apenas por debajo: musgo oscuro entre las losas
    base = Malla("MIR-02_juntas")
    junta_c = MUSGO
    for region in (region_a, region_b):
        mm.cara(base, [np.array([p[0], -0.012, p[1]]) for p in region], junta_c, arriba=True)
    return trozos, base, n_losas


def linea_balaustrada():
    """Puntos de los pilares sobre el arco, de 150 a 0 grados, a distancias iguales."""
    fino = [arco(a, 0.2) for a in np.linspace(A_BAL, 0.0, 301)]
    largo = np.concatenate([[0.0], np.cumsum([np.linalg.norm(b - a) for a, b in zip(fino[:-1], fino[1:])])])
    n = int(round(largo[-1] / 1.62))
    pts = []
    for i in range(n + 1):
        d = largo[-1] * i / n
        j = min(int(np.searchsorted(largo, d)), len(fino) - 1)
        pts.append(fino[j])
    return pts


def pilar(m, p, rng, lado=0.36, alto=0.94):
    caja_dir(m, p, (1, 0), lado + 0.08, 0.10, lado + 0.08, mm.PIEDRA_MALVA, 0.0, rng)
    caja_dir(m, p, (1, 0), lado, alto - 0.10, lado, mm.PIEDRA, 0.10, rng, luz_t=0.18)
    caja_dir(m, p, (1, 0), lado + 0.10, 0.09, lado + 0.10, mm.PIEDRA_LUZ, alto, rng, luz_t=0.3)
    y = alto + 0.09
    h = (lado + 0.02) / 2
    punta = np.array([p[0], y + 0.11, p[1]])
    esq = [np.array([p[0] + sx * h, y, p[1] + sz * h]) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for i in range(4):
        mm.cara(m, [esq[i], esq[(i + 1) % 4], punta], mezclar(mm.PIEDRA_LUZ, PAL["crema"], 0.15 + 0.1 * (i % 2)),
                interior=np.array([p[0], y - 0.2, p[1]]))


def tramo_balaustrada(m, a, b, rng):
    d = b - a
    largo = float(np.linalg.norm(d))
    u = d / largo
    medio = (a + b) / 2
    caja_dir(m, medio, u, largo - 0.30, 0.17, 0.26, mm.PIEDRA_MALVA, 0.0, rng)
    caja_dir(m, medio, u, largo - 0.26, 0.13, 0.30, mm.PIEDRA_LUZ, 0.62, rng, luz_t=0.28)
    n = max(2, int((largo - 0.5) / 0.30))
    for i in range(n):
        p = a + u * (0.36 + (largo - 0.72) * (i + 0.5) / n)
        caja_dir(m, p, u, 0.12, 0.45, 0.13, mm.PIEDRA, 0.17, rng, sombra_t=0.40, luz_t=0.10)


def muro_contencion(m, camino, rng, y_fondo=-6.4):
    """Muro de sillares bajo el borde de la terraza; 'camino' rodea la terraza de oeste a este por el sur."""
    filas = [0.0, -0.16, -1.0, -1.95, -3.0, -4.3, y_fondo]
    for a, b in zip(camino[:-1], camino[1:]):
        d = b - a
        largo = float(np.linalg.norm(d))
        if largo < 0.02:
            continue
        u = d / largo
        n2 = np.array([-u[1], u[0]])           # hacia fuera de la terraza
        partes = max(1, int(round(largo / 0.95)))
        for f in range(len(filas) - 1):
            y0, y1 = filas[f], filas[f + 1]
            s0, s1 = 0.10 * abs(y0) + (0.05 if f == 0 else 0.0), 0.10 * abs(y1) + (0.05 if f == 0 else 0.0)
            base = mm.PIEDRA_LUZ if f == 0 else mezclar(mm.PIEDRA_MALVA, PAL["petroleo"], min(0.45, 0.10 + 0.08 * f))
            for k in range(partes):
                t0, t1 = k / partes, (k + 1) / partes
                p0, p1 = a + d * t0, a + d * t1
                # v2c: cuanto mas hondo, mas se funde con la noche del valle (antes era un pano claro y plano)
                col = np.asarray(base, float) * (1.0 + rng.normal(0, 0.07)) * max(0.42, 1.0 - 0.11 * f)
                arriba, abajo = mezclar(col, PAL["crema"], 0.08), mezclar(col, PAL["petroleo"], 0.22)
                q = [np.array([*(p0 + n2 * s0), y0])[[0, 2, 1]], np.array([*(p1 + n2 * s0), y0])[[0, 2, 1]],
                     np.array([*(p1 + n2 * s1), y1])[[0, 2, 1]], np.array([*(p0 + n2 * s1), y1])[[0, 2, 1]]]
                dentro = np.array([(p0 + p1)[0] / 2 - n2[0], (y0 + y1) / 2, (p0 + p1)[1] / 2 - n2[1]])
                mm.cara(m, q, interior=dentro, cols=[arriba, arriba, abajo, abajo])


def plataforma():
    rng = np.random.default_rng(202)
    trozos, juntas, n_losas = losas(rng)
    bal = Malla("MIR-02_balaustrada")
    pilares = linea_balaustrada()
    for i, p in enumerate(pilares[:-1]):          # el ultimo punto lo ocupa el pilar del porton
        pilar(bal, p, rng)
    for a, b in zip(pilares[:-1], pilares[1:]):
        tramo_balaustrada(bal, a, b, rng)
    # borde este, al norte del porton
    ne0, ne1 = np.array([E - 0.2, PORTON_Z - mm.MEDIO_PORTON]), np.array([E - 0.2, N + 0.2])
    tramo_balaustrada(bal, ne0, ne1, rng)
    pilar(bal, ne1, rng)
    # bordillo del lado oeste (bajo la guirnalda)
    bordillo = [np.array([W + 0.16, N + 0.2]), np.array([W + 0.16, CZ])] + [arco(a, 0.2) for a in (174, 166, 158, A_BAL)]
    for a, b in zip(bordillo[:-1], bordillo[1:]):
        d = b - a
        caja_dir(bal, (a + b) / 2, d, float(np.linalg.norm(d)) + 0.05, 0.30, 0.30, mm.PIEDRA_MALVA, 0.0, rng, luz_t=0.2)
    # pie de la escalinata: dos pilares y los muros laterales que suben con ella
    for x in (ESC_X - 1.43, ESC_X + 1.43):
        pilar(bal, np.array([x, N + 0.05]), rng, lado=0.42, alto=1.16)
        x0, x1, z0, z1 = x - 0.14, x + 0.14, N - 0.16, N - 3.4
        h0, h1, yb = 0.50, 0.50 + 1.92, -0.25
        eje = np.array([x, 0.8, (z0 + z1) / 2])
        col = mm.PIEDRA
        bajo, alto_c = mezclar(col, PAL["petroleo"], 0.35), mezclar(col, PAL["crema"], 0.12)
        for xx in (x0, x1):
            mm.cara(bal, [(xx, yb, z0), (xx, yb + 1.9, z1), (xx, h1, z1), (xx, h0, z0)], interior=eje, cols=[bajo, bajo, alto_c, alto_c])
        mm.cara(bal, [(x0, h0, z0), (x1, h0, z0), (x1, h1, z1), (x0, h1, z1)], mezclar(mm.PIEDRA_LUZ, PAL["crema"], 0.1), arriba=True)
        mm.cara(bal, [(x0, yb, z0), (x1, yb, z0), (x1, h0, z0), (x0, h0, z0)], interior=eje, cols=[bajo, bajo, alto_c, alto_c])
    # relleno bajo la escalinata y descanso de arriba: no se ve el vacio entre los tramos ni al final
    x0, x1 = ESC_X - 1.3, ESC_X + 1.3
    relleno = mezclar(mm.PIEDRA_MALVA, PAL["petroleo"], 0.35)
    mm.cara(bal, [(x0, -0.06, N), (x1, -0.06, N), (x1, 1.86, N - 3.2), (x0, 1.86, N - 3.2)], relleno, arriba=True)
    mm.cara(bal, [(x0 - 0.3, 1.915, N - 3.15), (x1 + 0.3, 1.915, N - 3.15), (x1 + 0.3, 1.915, N - 6.5), (x0 - 0.3, 1.915, N - 6.5)],
            arriba=True, cols=[mm.PIEDRA, mm.PIEDRA, relleno, relleno])
    # antepechos del descanso de la bajada
    for z in (BAJ_Z0, BAJ_Z1):
        a, b = np.array([E + 0.30, z]), np.array([BAJ_X1 + 0.1, z])
        caja_dir(bal, (a + b) / 2, b - a, float(np.linalg.norm(b - a)), 0.52, 0.26, mm.PIEDRA, 0.0, rng, luz_t=0.2)
        caja_dir(bal, (a + b) / 2, b - a, float(np.linalg.norm(b - a)) + 0.06, 0.08, 0.32, mm.PIEDRA_LUZ, 0.52, rng, luz_t=0.3)
    # muro de contencion: oeste, arco sur, este y descanso de la bajada
    muro = Malla("MIR-02_muro")
    camino = [np.array([W, N - 0.3]), np.array([W, CZ])] + [arco(a) for a in range(174, 0, -6)] + [
        np.array([E, CZ]), np.array([BAJ_X1, BAJ_Z1]), np.array([BAJ_X1, BAJ_Z0]), np.array([E, BAJ_Z0]), np.array([E, N - 0.3])]
    muro_contencion(muro, camino, rng)
    e = Escena("herramientas/mallas/mirador_escena.py")
    total = 0
    for (i, k), t in trozos.items():
        if len(t):
            e.nodo(t.nombre, e.malla(t, nombre=t.nombre))
            total += e.stats[t.nombre]
    for nombre, mallas in (("MIR-02_juntas", [juntas]), ("MIR-02_balaustrada", [bal]), ("MIR-02_muro", [muro])):
        e.nodo(nombre, e.malla(*mallas, nombre=nombre))
        total += e.stats[nombre]
    e.guardar(SALIDA / "MIR-02.glb")
    return total, n_losas, pilares, bordillo


# ---------- TER-15 ladera del cerro ----------

def valle_h(x, z):
    """Suelo del valle (v2b). Al este sube hasta -3,6 m, justo bajo la bajada de los faroles, y luego baja hacia
    el rio: asi el barrio iluminado queda dentro del encuadre de la camara alta, a la derecha de la terraza."""
    sx = min(1.0, max(0.0, (x - 6.5) / 1.5)) * (1.0 - 0.85 * min(1.0, max(0.0, (x - 9.0) / 16.0)))
    sz = min(1.0, max(0.0, (3.5 - z) / 3.0))
    return -8.6 + 5.0 * sx * sz + 0.25 * math.sin(x * 0.4) * math.cos(z * 0.3)


RIO = ((14.2, 3.0), (18.6, -30.0))      # eje del rio que baja por el valle (agua oscura con reflejo de Luna)
LUCES_BARRIO: list = []                  # [x, y, z, radio] de ventanas, faroles y calles (puntos de brillo)
REFLEJO_LUNA: list = []                  # cuadrilateros del reflejo frio de la Luna en el rio


def dist_rio(x, z):
    a, b = np.array(RIO[0]), np.array(RIO[1])
    p = np.array([x, z])
    t = np.clip((p - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1)
    return float(np.linalg.norm(p - (a + (b - a) * t)))


def _barrio():
    """Casas bajas del barrio, de noche: muros apagados, tejas oscuras y ventanas encendidas (puntos calidos)."""
    rng = np.random.default_rng(1207)
    paredes = [mezclar(PAL["crema"], PAL["tierra1"], 0.35), mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.50),
               mezclar(PAL["sol"], PAL["tierra1"], 0.55), mezclar(PAL["tierra1"], PAL["piedra"], 0.4),
               mezclar(PAL["piedra_clara"], PAL["crema"], 0.3)]
    techos = [PAL["terracota"], mezclar(PAL["terracota"], PAL["coral"], 0.35), mezclar(PAL["terracota"], PAL["madera1"], 0.3)]
    casas = []
    # v2c (critica): casas mas bajas y pequenas, en hileras mas juntas: desde la camara alta los tejados altos tapaban
    # las ventanas de la hilera de atras. Muros apagados y tejas hacia el azul de la noche: las luces mandan.
    for fila, z in enumerate(np.arange(2.0, -30.0, -2.7)):
        for x in np.arange(9.0 + (1.3 if fila % 2 else 0.0), 31.0, 2.6):
            px, pz = x + rng.uniform(-0.5, 0.5), z + rng.uniform(-0.4, 0.4)
            if px < 12.0 and -4.0 < pz < 0.4:          # la bajada de los faroles y su ladera
                continue
            w, d = rng.uniform(1.4, 2.0), rng.uniform(1.3, 1.8)
            if dist_rio(px, pz) < w / 2 + 1.3 or rng.random() < 0.10:
                continue
            h = rng.uniform(1.2, 1.9)
            casas.append({"x": px, "z": pz, "w": w, "d": d, "h": h, "y": valle_h(px, pz) - 0.15, "giro": rng.uniform(-8, 8),
                          "pared": mezclar(paredes[rng.integers(len(paredes))], PAL["petroleo"], 0.30) * 0.70,
                          "techo": mezclar(techos[rng.integers(len(techos))], PAL["petroleo"], 0.45) * 0.62,
                          "semilla": int(rng.integers(1 << 30))})
    return casas


BARRIO = _barrio()


def casa_barrio(m, c):
    rng = np.random.default_rng(c["semilla"])
    x, z, w, d, h, y = c["x"], c["z"], c["w"], c["d"], c["h"], c["y"]
    t = math.radians(c["giro"])
    u, v = np.array([math.cos(t), -math.sin(t)]), np.array([math.sin(t), math.cos(t)])

    def p3(lx, ly, lz):
        q = np.array([x, z]) + u * lx + v * lz
        return np.array([q[0], y + ly, q[1]])

    pared, techo = c["pared"], c["techo"]
    bajo, alto = mezclar(pared, PAL["petroleo"], 0.35), mezclar(pared, PAL["crema"], 0.05)
    eje = p3(0, h / 2, 0)
    esq = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    for i in range(4):
        a, b = esq[i], esq[(i + 1) % 4]
        mm.cara(m, [p3(a[0], 0, a[1]), p3(b[0], 0, b[1]), p3(b[0], h, b[1]), p3(a[0], h, a[1])], interior=eje, cols=[bajo, bajo, alto, alto])
    # tejado a dos aguas, cumbrera a lo largo de x local
    vu = 0.25
    cum = h + d * 0.32
    for s in (1, -1):
        cb, ca = mezclar(techo, PAL["petroleo"], 0.25), mezclar(techo, PAL["crema"], 0.08 if s > 0 else 0.0)
        mm.cara(m, [p3(-w / 2 - vu, h - 0.05, s * (d / 2 + vu)), p3(w / 2 + vu, h - 0.05, s * (d / 2 + vu)), p3(w / 2 + vu, cum, 0), p3(-w / 2 - vu, cum, 0)],
                interior=p3(0, h - 1.0, 0), cols=[cb, cb, ca, ca])
    for s in (1, -1):
        mm.cara(m, [p3(s * w / 2, h, -d / 2), p3(s * w / 2, h, d / 2), p3(s * w / 2, cum - 0.05, 0)], alto, interior=eje)
    # ventanas encendidas (puntos de brillo): frente (+Z) y costado oeste (-X), que son las caras que ve la camara
    yv = min(0.85, h - 0.35)
    for lx in np.linspace(-w / 2 + 0.4, w / 2 - 0.4, max(1, int(w / 0.75))):
        if rng.random() < 0.75:
            q = p3(lx, yv, d / 2 + 0.05)
            LUCES_BARRIO.append([round(float(q[0]), 2), round(float(q[1]), 2), round(float(q[2]), 2), round(float(rng.uniform(0.10, 0.13)), 3)])
    if rng.random() < 0.55:
        q = p3(-w / 2 - 0.05, yv, rng.uniform(-d / 4, d / 4))
        LUCES_BARRIO.append([round(float(q[0]), 2), round(float(q[1]), 2), round(float(q[2]), 2), 0.10])


def rio(m):
    """Agua oscura del rio y, en un tramo, el reflejo frio de la Luna (lo dibuja la zona con brillo)."""
    a, b = np.array(RIO[0]), np.array(RIO[1])
    eje = b - a
    largo = float(np.linalg.norm(eje))
    eu = eje / largo
    lado = np.array([-eu[1], eu[0]])
    agua, agua_borde = PAL["petroleo"] * 0.42, mezclar(PAL["petroleo"], PAL["piedra"], 0.3) * 0.5
    n = int(largo / 1.5)
    for i in range(n):
        p0, p1 = a + eje * i / n, a + eje * (i + 1) / n
        ancho = 1.0 + 0.25 * math.sin(i * 0.9)
        y0, y1 = valle_h(*p0) + 0.10, valle_h(*p1) + 0.10
        q = [np.array([*(p0 - lado * ancho)[:1], y0, (p0 - lado * ancho)[1]]), np.array([(p0 + lado * ancho)[0], y0, (p0 + lado * ancho)[1]]),
             np.array([(p1 + lado * ancho)[0], y1, (p1 + lado * ancho)[1]]), np.array([(p1 - lado * ancho)[0], y1, (p1 - lado * ancho)[1]])]
        mm.cara(m, q, arriba=True, cols=[agua_borde, agua_borde, agua, agua])
    # reflejo: trazos cortos y quebrados en el centro del rio, entre z -4 y -16 (la Luna baja al oeste)
    rng = np.random.default_rng(77)
    for t in np.linspace(0.16, 0.50, 11):
        c = a + eje * t + lado * rng.uniform(-0.25, 0.25)
        lar, anc = rng.uniform(0.35, 0.8), rng.uniform(0.06, 0.13) * (1.4 - t)
        yc = valle_h(*c) + 0.13
        pts = [c - eu * lar / 2 - lado * anc, c + eu * lar / 2 - lado * anc, c + eu * lar / 2 + lado * anc, c - eu * lar / 2 + lado * anc]
        REFLEJO_LUNA.append([[round(float(p[0]), 3), round(yc, 3), round(float(p[1]), 3)] for p in pts])

def terreno(m, xs, zs, altura, color, rng, mover=0.28, fijo_z0=True):
    P = {}
    for i, x in enumerate(xs):
        for k, z in enumerate(zs):
            borde = (fijo_z0 and k == 0) or i in (0, len(xs) - 1)
            jx, jz = (0.0, 0.0) if borde else rng.uniform(-mover, mover, 2)
            P[(i, k)] = np.array([x + jx, altura(x + jx, z + jz), z + jz])
    for i in range(len(xs) - 1):
        for k in range(len(zs) - 1):
            a, b, c, d = P[(i, k)], P[(i + 1, k)], P[(i + 1, k + 1)], P[(i, k + 1)]
            tris = ((a, b, c), (a, c, d)) if (i + k) % 2 == 0 else ((a, b, d), (b, c, d))
            for t in tris:
                col = np.asarray(color(sum(t) / 3, rng), float)
                mm.cara(m, list(t), arriba=True, cols=[col * (1.0 + rng.normal(0, 0.04)) for _ in t])


def ladera():
    rng = np.random.default_rng(215)
    roca_c = mezclar(PAL["piedra"], PAL["petroleo"], 0.45)
    musgo = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.40)

    def color_roca(p, r):
        return mezclar(roca_c, musgo, 0.75) if r.random() < 0.42 else mezclar(roca_c, PAL["piedra_clara"], r.uniform(0.0, 0.25))

    def color_valle(p, r):
        # v2b: el valle de noche, azul petroleo hondo con manchas de arboleda; las luces del barrio se leen encima
        base = mezclar(PAL["petroleo"], PAL["piedra_osc"], 0.25) * 0.62
        if r.random() < 0.35:
            base = mezclar(PAL["hierba_sombra"], PAL["petroleo"], 0.55) * 0.55
        return base * (1.0 + r.normal(0, 0.05))

    norte = Malla("TER-15_norte")
    terreno(norte, np.arange(ESC_X + 1.58, E + 0.9, 1.05), np.arange(N - 0.02, N - 4.2, -0.9),
            lambda x, z: (N - z) * 1.15 + 0.22 * math.sin(x * 1.7 + z) * min(1.0, (N - z)), color_roca, rng)
    xs_o = np.arange(-11.5, W - 0.25, 1.0).tolist() + [W - 0.3]
    terreno(norte, xs_o[:-1] + [ESC_X - 1.58], np.arange(N - 0.02, N - 4.2, -0.9),
            lambda x, z: (N - z) * 1.0 - 0.2 - max(0.0, (W - 0.4) - x) * 0.8, color_roca, rng)
    oeste = Malla("TER-15_oeste")
    terreno(oeste, xs_o, np.arange(N, 8.6, 1.0),
            lambda x, z: -0.2 - max(0.0, (W - 0.4) - x) * 0.8 - 0.25 * max(0.0, z - 1.0), color_roca, rng, fijo_z0=False)
    fondo = Malla("TER-15_fondo")
    # v2b: al este el valle sube hasta casi el pie de la bajada (-3,6 m): asi el barrio cae dentro del encuadre
    terreno(fondo, np.arange(-18.0, 34.1, 2.0), np.arange(-30.0, 18.1, 2.0), valle_h, color_valle, rng, mover=0.5, fijo_z0=False)
    barrio = Malla("TER-15_barrio")
    for c in BARRIO:
        casa_barrio(barrio, c)
    rio(barrio)
    e = Escena("herramientas/mallas/mirador_escena.py")
    total = 0
    for t in (norte, oeste, fondo, barrio):
        e.nodo(t.nombre, e.malla(t, nombre=t.nombre))
        total += e.stats[t.nombre]
    e.guardar(SALIDA / "TER-15.glb")
    return total


# ---------- layout ----------

def guirnalda(puntos, bombillas, cables, paso=0.52):
    """Cable colgante entre amarres [(x, y, z)], con una bombilla cada 'paso' metros."""
    for a, b in zip(puntos[:-1], puntos[1:]):
        a, b = np.asarray(a, float), np.asarray(b, float)
        tramo = float(np.linalg.norm(b - a))
        flecha = 0.10 + 0.10 * tramo
        n = max(4, int(tramo / 0.22))
        linea = []
        for i in range(n + 1):
            t = i / n
            p = a + (b - a) * t
            p[1] -= flecha * 4 * t * (1 - t)
            # v2: el cuarto valor es el peso del vaiven (0 en los amarres, 1 en el centro del tramo)
            linea.append([round(float(v), 3) for v in p] + [round(4 * t * (1 - t), 3)])
        cables.append(linea)
        if bombillas is None:
            continue
        nb = max(2, int(round(tramo / paso)))
        for i in range(nb):
            t = (i + 0.5) / nb
            p = a + (b - a) * t
            p[1] -= flecha * 4 * t * (1 - t) + 0.075
            bombillas.append([round(float(p[0]), 3), round(float(p[1]), 3), round(float(p[2]), 3), 0.062, round(4 * t * (1 - t) + 0.15, 3)])


# v2: banderines de tela (coral, dorado, crema, petroleo, magenta y naranja) bajo la guirnalda
COLORES_BANDERIN = [mezclar(PAL["coral"], PAL["terracota"], 0.15), PAL["dorado"], mezclar(PAL["crema"], PAL["piedra_clara"], 0.3),
                    mezclar(PAL["petroleo"], PAL["piedra_clara"], 0.12), mezclar(mezclar(PAL["coral"], PAL["petroleo"], 0.30), PAL["crema"], 0.08),
                    PAL["sol"]]


def hexa(c):
    c = np.clip(np.asarray(c, float), 0, 1)
    return "%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)


def banderines(puntos, cables, lista, paso=0.32):
    """Cuerda de banderines triangulares entre amarres; cada banderin: 3 vertices, color y 3 pesos de vaiven."""
    k = len(lista)
    for a, b in zip(puntos[:-1], puntos[1:]):
        a, b = np.asarray(a, float), np.asarray(b, float)
        tramo = float(np.linalg.norm(b - a))
        flecha = 0.14 + 0.12 * tramo
        n = max(4, int(tramo / 0.22))
        linea = []
        for i in range(n + 1):
            t = i / n
            p = a + (b - a) * t
            p[1] -= flecha * 4 * t * (1 - t)
            linea.append([round(float(v), 3) for v in p] + [round(4 * t * (1 - t), 3)])
        cables.append(linea)
        u = (b - a) / tramo
        nb = max(2, int(tramo / paso))
        for i in range(nb):
            t0, t1 = (i + 0.18) / nb, (i + 0.82) / nb
            tm = (t0 + t1) / 2
            p0, p1 = a + (b - a) * t0, a + (b - a) * t1
            p0[1] -= flecha * 4 * t0 * (1 - t0)
            p1[1] -= flecha * 4 * t1 * (1 - t1)
            punta = (p0 + p1) / 2 - np.array([0.0, 0.19, 0.0]) + np.array([-u[2], 0.0, u[0]]) * 0.02
            w0, w1, wm = 4 * t0 * (1 - t0), 4 * t1 * (1 - t1), 4 * tm * (1 - tm) + 0.35
            lista.append([round(float(v), 3) for v in (*p0, *p1, *punta)] + [hexa(COLORES_BANDERIN[k % len(COLORES_BANDERIN)]),
                                                                              round(w0, 3), round(w1, 3), round(wm, 3)])
            k += 1


def layout(pilares, bordillo):
    rng = np.random.default_rng(303)
    calidos = json.loads((SALIDA / "calidos.json").read_text(encoding="utf-8"))
    rec, bombillas, ventanas, cables, luces = [], [], [], [], []
    columnas, cajas, muros = [], [], []

    def poner(ident, glb, pos, giro=0.0, escala=1.0, lista_calidos=None, clave=None, **extra):
        r = {"id": ident, "glb": glb, "pos": [round(float(v), 3) for v in pos], "rot_y": round(float(giro), 2), "escala": round(float(escala), 3)}
        r.update(extra)
        rec.append(r)
        if lista_calidos is not None:
            for c in calidos.get(clave or Path(glb).stem, []):
                if "b" in c:
                    lista_calidos[0].append(mundo(pos, giro, c["b"], escala) + [c["r"] * escala])
                else:
                    lista_calidos[1].append([mundo(pos, giro, p, escala) for p in c["q"]])
        return r

    fijos = (bombillas, ventanas)
    poner("MIR-02", "mirador/MIR-02.glb", (0, 0, 0), suelto=True)
    poner("TER-15", "mirador/TER-15.glb", (0, 0, 0), suelto=True)
    # escalinata de mosaico (la parte baja de TER-11 mira a +Z) y bajada de los faroles (gira 90: baja hacia +X)
    poner("TER-11_a", "entorno/TER-11.glb", (ESC_X, 0.0, N - 0.8))
    poner("TER-11_b", "entorno/TER-11.glb", (ESC_X, 0.96, N - 2.4))
    poner("TER-11_c", "entorno/TER-11.glb", (BAJ_X1 + 0.8, -0.96, PORTON_Z), 90.0)
    poner("TER-11_d", "entorno/TER-11.glb", (BAJ_X1 + 2.4, -1.92, PORTON_Z), 90.0)
    # faro
    fx, fz, fg = FARO
    poner("MIR-01", "mirador/MIR-01.glb", (fx, 0, fz), fg, lista_calidos=fijos)
    columnas.append([fx, fz, 1.78, 3.0])
    escalon = mundo((fx, 0, fz), fg, (0, 0, 1.95))
    cajas.append([escalon[0], escalon[2], 1.15, 0.85, fg, 0.9])
    # porton del cerro, con sus faroles (se encienden al abrirse)
    porton_b, porton_q = [], []
    poner("MIR-10", "mirador/MIR-10.glb", (E, 0, PORTON_Z), 0.0, lista_calidos=(porton_b, porton_q), suelto=True)
    for s in (-1, 1):
        columnas.append([E, PORTON_Z + s * mm.MEDIO_PORTON, 0.27, 2.0])
    # telescopio, binoculares, atril, banca, mesa del club
    tx, tz, tg = TELESCOPIO
    poner("MIR-03", "mirador/MIR-03.glb", (tx, 0, tz), tg)
    columnas.append([tx, tz, 0.46, 1.5])
    est = mundo((tx, 0, tz), tg, mm.ESTUCHE)
    columnas.append([est[0], est[2], 0.27, 0.4])
    nb = normal_arco(125.0)
    pb = arco(125.0) - nb * 0.75
    giro_b = math.degrees(math.atan2(nb[0], nb[1]))
    poner("MIR-04", "mirador/MIR-04.glb", (pb[0], 0, pb[1]), giro_b)
    columnas.append([pb[0], pb[1], 0.27, 1.3])
    ax, az, ag = ATRIL
    poner("MIR-05", "mirador/MIR-05.glb", (ax, 0, az), ag, lista_calidos=fijos)
    cajas.append([ax, az, 1.15, 0.62, ag, 1.3])
    poner("MIR-06", "mirador/MIR-06.glb", (BANCA[0], 0, BANCA[1]), BANCA[2])
    cajas.append([BANCA[0], BANCA[1], 1.8, 0.56, BANCA[2], 0.6])
    mx, mz, mg = MESA
    poner("MIR-09", "mirador/MIR-09.glb", (mx, 0, mz), mg)
    cajas.append([mx, mz, 1.6, 0.82, mg, 0.9])
    maqueta = mundo((mx, mm.ALTO_MESA, mz), mg, (-0.05, 0, -0.14))
    portatil = mundo((mx, mm.ALTO_MESA, mz), mg, (0.56, 0, -0.12))
    poner("TAL-11", "mirador/TAL-11.glb", maqueta, mg + 12.0)
    poner("TAL-18", "mirador/TAL-18.glb", portatil, mg - 14.0)
    for i, (dx, dz) in enumerate(((-1.18, -0.05), (0.55, -0.72))):
        poner(f"TAL-10_{i}", "mirador/TAL-10.glb", (mx + dx, 0, mz + dz), 40.0 * i)
        columnas.append([mx + dx, mz + dz, 0.2, 0.5])
    # macetas con plantas (junto a la escalinata y a la puerta del faro)
    # v2: macetas con flores roja, blanca y magenta (VEG-09 cayena) ademas de las plantas de hoja
    macetas = [(-2.3, -3.72, 1.25, "entorno/VEG-07.glb", None, 1.0), (-2.82, -3.12, 0.85, "mirador/VEG-09.glb", "VEG-09_roja", 1.05),
               (3.85, -1.05, 1.30, "entorno/VEG-10.glb", None, 1.15), (4.55, -0.75, 0.85, "mirador/VEG-09.glb", "VEG-09_magenta", 1.05),
               (-5.1, -3.95, 1.0, "entorno/VEG-12.glb", None, 0.8), (5.35, -3.65, 0.85, "mirador/VEG-09.glb", "VEG-09_blanca", 1.05),
               (-4.35, 1.40, 0.80, "entorno/VEG-14.glb", "VEG-14_amarilla", 2.2), (-0.30, -3.72, 0.8, "mirador/VEG-09.glb", "VEG-09_magenta", 1.0)]
    for i, (x, z, s, planta, nodo, sp) in enumerate(macetas):
        poner(f"URB-07_{i}", "mirador/URB-07.glb", (x, 0, z), 30.0 * i, s)
        extra = {"nodo": nodo} if nodo else {}
        extra["suelto"] = True          # fuera del MultiMesh de la ladera: estas si proyectan sombra
        poner(f"VEG-maceta_{i}", planta, (x, 0.40 * s, z), 50.0 * i, sp, **extra)
        columnas.append([x, z, 0.33 * s, 0.8])
    # postes de la guirnalda (MIR-07): borde oeste y borde norte
    alto = mm.ALTO_AMARRE
    oeste = [np.array([W + 0.16, -3.3]), np.array([W + 0.16, -1.15]), arco(166, 0.2), arco(A_BAL + 1.5, 0.05)]
    norte = [np.array([-2.25, N - 0.02]), np.array([-0.15, N - 0.02]), np.array([1.4, N - 0.02])]
    for i, p in enumerate(oeste + norte):
        poner(f"MIR-07_{i}", "mirador/MIR-07.glb", (p[0], 0, p[1]), 15.0 * i)
        columnas.append([float(p[0]), float(p[1]), 0.15, 2.4])
    guirnalda([(p[0], alto, p[1]) for p in oeste], bombillas, cables)
    faro_amarre = (fx - 1.26 * 0.69, 2.5, fz - 1.26 * 0.724)
    guirnalda([(ESC_X + 1.43, 1.3, N + 0.05)] + [(p[0], alto, p[1]) for p in norte] + [faro_amarre], bombillas, cables)
    # v2: banderines por debajo de la guirnalda, en los mismos postes
    cables_band, lista_band = [], []
    banderines([(p[0], alto - 0.30, p[1]) for p in oeste], cables_band, lista_band)
    banderines([(p[0], alto - 0.30, p[1]) for p in norte] + [(fx - 1.30 * 0.69, 2.1, fz - 1.30 * 0.724)], cables_band, lista_band)

    # ---- v2: vida del Mirador ----
    # farol apagado (ARQ-09) que la protagonista enciende; pizarra de constelaciones (MIR-11); recolectables COL
    farol_n = (-1.95, 3.0)
    poner("ARQ-09_nuevo", "mirador/ARQ-09.glb", (farol_n[0], 0.0, farol_n[1]), 0.0, suelto=True)
    columnas.append([farol_n[0], farol_n[1], 0.14, 2.4])
    piz = (-0.35, 2.30, 0.0)
    poner("MIR-11", "mirador/MIR-11.glb", (piz[0], 0.0, piz[1]), piz[2], suelto=True)
    centro_piz = mundo((piz[0], 0.0, piz[1]), piz[2], mm.PIZARRA_CENTRO)
    caja_piz = mundo((piz[0], 0.0, piz[1]), piz[2], (0.0, 0.0, -0.16))
    cajas.append([caja_piz[0], caja_piz[2], 1.16, 0.66, piz[2], 1.5])
    fi = math.radians(mm.PIZARRA_FI)
    t = math.radians(piz[2])
    der_w = [math.cos(t), 0.0, -math.sin(t)]
    arr_l = (0.0, math.cos(fi), -math.sin(fi))
    arr_w = [arr_l[2] * math.sin(t), arr_l[1], arr_l[2] * math.cos(t)]
    n_w = list(np.cross(np.array(der_w), np.array(arr_w)))
    frente_piz = [centro_piz[i] + n_w[i] * 0.0235 for i in range(3)]
    pizarra = {"centro": [round(float(v), 4) for v in frente_piz], "der": [round(float(v), 4) for v in der_w],
               "arr": [round(float(v), 4) for v in arr_w], "n": [round(float(v), 4) for v in n_w],
               "estrellas": [list(e) for e in mm.PIZARRA_ESTRELLAS]}
    recolectables = {
        "CartaEstelar": [-3.30, 1.85, "carta_estelar", "COL-12", 25.0],
        "AntenaVarilla": [1.30, -1.20, "antena_de_varilla", "COL-08", -30.0],
        "CableCobre": [4.95, 1.15, "cable_de_cobre", "COL-06", 10.0],
    }
    for nombre, (x, z, _, ident, g) in recolectables.items():
        poner(f"{ident}_rec", f"mirador/{ident}.glb", (x, 0.0, z), g, 1.6, suelto=True)
    # luciernagas: grupos [x, y, z, radio, alto, cuantas] junto a las plantas, la buganvilla y la plaza
    # v2b: un grupo mas junto a la banca (maceta magenta): sentada y quieta, se reunen 10 o mas
    luciernagas = [[-6.3, -0.2, -0.8, 1.3, 1.3, 7], [-2.6, 0.3, -3.0, 0.9, 1.0, 6], [-0.3, 0.3, -3.3, 0.8, 0.9, 7], [4.2, 0.3, -0.6, 0.9, 1.0, 5],
                   [-2.4, -0.6, 4.7, 1.5, 1.5, 7], [2.6, -0.8, 4.9, 1.5, 1.5, 6], [-0.6, 0.4, 1.4, 1.3, 1.0, 5],
                   [6.8, 0.2, 1.4, 1.2, 1.2, 4]]
    # v2b: luces de la ciudad de abajo, DENTRO del encuadre: el barrio del valle este (TER-15_barrio) con sus
    # ventanas encendidas, faroles de calle entre las hileras de casas y luces sueltas mas lejos (puntos de brillo)
    puntos_ciudad = list(LUCES_BARRIO)
    rng_c = np.random.default_rng(909)
    for z in np.arange(0.35, -30.0, -3.3):
        for x in np.arange(9.5, 31.0, 2.3):
            px, pz = x + rng_c.uniform(-0.4, 0.4), z + rng_c.uniform(-0.3, 0.3)
            if (px < 12.0 and -4.0 < pz < 0.4) or dist_rio(px, pz) < 1.2:
                continue
            puntos_ciudad.append([round(px, 2), round(valle_h(px, pz) + 0.9, 2), round(pz, 2), 0.09])
    # v2c: el camino del barrio sube por la loma bajo la bajada de los faroles: faroles de calle que la camara si ve
    for t in np.linspace(0.0, 1.0, 9):
        for dz in (-0.25, 0.25):
            px = 7.0 + 5.6 * t + rng_c.uniform(-0.2, 0.2)
            pz = 0.2 - 4.6 * t + dz * 3.0 + rng_c.uniform(-0.2, 0.2)
            puntos_ciudad.append([round(px, 2), round(valle_h(px, pz) + 0.55, 2), round(pz, 2), 0.085])
    for _ in range(70):
        x, z = rng_c.uniform(20.0, 34.0), rng_c.uniform(-30.0, -4.0)
        puntos_ciudad.append([round(x, 2), round(valle_h(x, z) + rng_c.uniform(0.4, 1.8), 2), round(z, 2), round(float(rng_c.uniform(0.07, 0.12)), 3)])
    # buganvilla en cascada por fuera de la balaustrada
    for i, a in enumerate((128.0, 97.0, 61.0, 24.0)):
        n2 = normal_arco(a)
        p = arco(a) + n2 * 0.07
        poner(f"VEG-08_{i}", "mirador/VEG-08.glb", (p[0], 0.22, p[1]), math.degrees(math.atan2(n2[0], n2[1])), 1.0 + 0.12 * (i % 2))
    # v2: buganvilla tambien por el muro sur del descanso de la bajada (desde el borde este se ve entero)
    for i, x in enumerate((6.75, 7.65)):
        poner(f"VEG-08_d{i}", "mirador/VEG-08.glb", (x, 0.22, BAJ_Z1 + 0.08), 0.0, 1.05 - 0.1 * i)
    # rocas y plantas del cerro: borde oeste, pie de la ladera norte y bajo el muro
    rocas = [(-6.6, -2.6, -0.5, "a", 2.0), (-6.9, -0.4, -0.8, "b", 2.3), (-6.5, 1.5, -0.9, "a", 1.9), (-7.9, -1.6, -1.6, "b", 2.6),
             (-5.6, 3.0, -1.5, "b", 2.2), (-4.0, 4.3, -2.2, "a", 2.6), (-7.6, 3.4, -2.3, "a", 2.8), (-1.2, 5.3, -2.9, "b", 2.4),
             (2.4, 5.0, -2.7, "a", 2.6), (5.3, 3.4, -2.6, "b", 2.3), (-6.9, -4.9, 0.2, "b", 2.2), (-0.9, -5.0, 0.2, "a", 2.0),
             (1.0, -5.2, 0.3, "b", 1.8), (5.6, -5.0, 0.2, "a", 2.2), (7.3, -4.4, -1.4, "b", 2.4)]
    # v2c: fuera la roca grande del sureste (7,4; 0,6): su musgo claro tapaba las luces del barrio
    for i, (x, z, y, v, s) in enumerate(rocas):
        poner(f"TER-01_{i}", f"entorno/TER-01_{v}.glb", (x, y, z), 47.0 * i, s)
    plantas = [("VEG-10", -6.3, -1.5, -0.35, 1.5), ("VEG-10", -6.4, 2.6, -1.0, 1.6), ("VEG-12", -6.2, 0.5, -0.5, 1.3),
               ("VEG-12", -6.6, -3.5, -0.4, 1.4), ("VEG-07", -7.2, 1.0, -1.2, 1.6), ("VEG-10", -7.4, -3.2, -1.0, 1.7),
               ("VEG-12", -4.9, 3.6, -1.6, 1.5), ("VEG-10", -2.6, 4.9, -2.4, 1.8), ("VEG-12", 0.6, 5.4, -2.6, 1.6),
               ("VEG-10", 4.0, 4.4, -2.4, 1.7), ("VEG-07", -6.2, -4.8, 0.5, 1.5), ("VEG-10", -1.9, -5.0, 0.7, 1.6),
               ("VEG-12", 0.2, -4.9, 0.6, 1.4), ("VEG-07", 2.2, -5.5, 1.2, 1.5), ("VEG-10", 4.9, -5.3, 0.9, 1.7),
               ("VEG-12", 6.4, -5.0, 0.6, 1.5)]
    for i, (v, x, z, y, s) in enumerate(plantas):
        poner(f"{v}_c{i}", f"entorno/{v}.glb", (x, y, z), 63.0 * i, s)
    # barrio de fondo (ARQ-14) y copas de arboles (VEG-15), cuesta abajo hacia el este y el sur
    # Solo se ven las fachadas que miran a +Z, y lo que esta mas bajo sale mas abajo en pantalla (unos 1,35 m por
    # metro de desnivel): la casa del noreste queda cuesta arriba para que sus ventanas asomen sobre la bajada.
    casas = [("a", 10.0, -5.6, -8.7, 0.0), ("c", 9.6, -8.0, 1.4, -6.0), ("b", 15.2, -6.4, -9.6, 4.0), ("c", 14.6, -8.6, -3.0, 5.0),
             ("b", 8.9, -9.2, 7.8, 5.0), ("c", 13.0, -9.2, 6.8, 8.0), ("b", 1.6, -9.6, 9.6, 4.0), ("a", -5.2, -10.0, 10.6, -5.0)]
    # v2b: al este ahora esta el barrio de TER-15; las casas ARQ-14 quedan solo al sur y al oeste
    casas = [c for c in casas if c[1] < 7.0]
    for i, (v, x, y, z, g) in enumerate(casas):
        poner(f"ARQ-14_{i}", "mirador/ARQ-14.glb", (x, y, z), g, 1.0, lista_calidos=fijos, clave=f"ARQ-14_{v}", nodo=f"ARQ-14_{v}")
    copas = [(a, rng.uniform(1.5, 2.6), rng.uniform(1.8, 2.6), rng.uniform(0.6, 1.5)) for a in range(18, 172, 13)]
    n_copa = 0
    for a, fuera, s, bajo in copas:
        if a < 57:          # v2c: las copas del este tapaban el valle (se leian como ladera verde de dia)
            continue
        p = arco(a) + normal_arco(a) * fuera
        poner(f"VEG-15_{n_copa}", "mirador/VEG-15.glb", (p[0], -bajo - 1.66 * s, p[1]), 77.0 * n_copa, s)
        n_copa += 1
    for x, y, z, s in [(-8.6, -5.2, 5.8, 2.8), (-9.4, -4.6, 1.6, 2.6), (-9.2, -3.6, -2.6, 2.4), (4.6, -6.8, 7.8, 3.0), (-2.4, -6.6, 8.2, 3.0)]:
        poner(f"VEG-15_{n_copa}", "mirador/VEG-15.glb", (x, y, z), 77.0 * n_copa, s)
        n_copa += 1
    # v2b: arboles bajos entre las casas del barrio (sobre el suelo del valle; pequenos para no tapar las luces)
    for x, z, s in [(12.6, -7.4, 0.8), (10.4, -12.6, 0.9), (15.6, -2.0, 0.8), (19.6, -9.4, 0.9),
                    (13.0, -16.8, 0.8), (21.4, -20.0, 1.0)]:
        poner(f"VEG-15_{n_copa}", "mirador/VEG-15.glb", (x, valle_h(x, z) - 0.2, z), 77.0 * n_copa, s)
        n_copa += 1
    # faroles de la bajada (ARQ-09)
    faroles = [(BAJ_X1 - 0.1, 0.0, BAJ_Z0 - 0.02), (BAJ_X1 + 2.6, -1.95, BAJ_Z1 + 0.25), (BAJ_X1 + 5.2, -3.6, BAJ_Z0 + 0.1)]
    for i, p in enumerate(faroles):
        poner(f"ARQ-09_{i}", "mirador/ARQ-09.glb", p, 0.0, lista_calidos=fijos)
    columnas.append([faroles[0][0], faroles[0][2], 0.14, 2.4])

    # ---- luces calidas (OmniLight sin sombra): [x, y, z, energia, alcance] ----
    luz_puerta = mundo((fx, 0, fz), fg, (0.52, 1.84, 1.6))
    luz_atril = mundo((ax, 0, az), ag, (-0.64, 1.19, -0.16))
    # pocas y de alcance corto: en el renderizador Mobile cada luz se calcula en todos los pixeles de las mallas
    # que toca (por eso el suelo va en 6 trozos). Con 6 luces de 7 a 9 m la zona bajaba de 40 fps en la HD 620.
    # v2 (color): charcos de luz. Alcance corto y caida rapida (la zona sube omni_attenuation): dorado bajo la
    # guirnalda y junto a las puertas, y entre los charcos la noche azul y violeta.
    luces += [[W + 1.6, 1.3, -2.5, 2.3, 3.2], [W + 0.9, 1.4, -1.05, 1.8, 2.6], [-1.2, 1.3, N + 1.35, 2.3, 3.2], [0.9, 1.3, N + 1.3, 2.0, 2.8],
              [round(luz_puerta[0], 2), 1.84, round(luz_puerta[2], 2), 1.4, 2.9],
              [faroles[0][0], 2.1, faroles[0][2] + 0.3, 2.3, 3.2]]
    luz_porton = [E + 0.1, 1.7, PORTON_Z, 2.4, 3.2]

    # ---- colisiones: [x0, z0, x1, z1, alto] ----
    borde = [[float(p[0]), float(p[1])] for p in bordillo] + [[float(p[0]), float(p[1])] for p in pilares[1:]]
    borde[-1] = [E - 0.1, PORTON_Z + mm.MEDIO_PORTON]
    for a, b in zip(borde[:-1], borde[1:]):
        muros.append([a[0], a[1], b[0], b[1], 1.6])
    muros.append([E - 0.1, PORTON_Z - mm.MEDIO_PORTON, E - 0.1, N, 1.6])
    muros.append([E, N - 0.15, W, N - 0.15, 2.4])     # ladera norte y pie de la escalinata (se sale por la marca)
    for sx in (-1.43, 1.43):
        columnas.append([ESC_X + sx, N + 0.05, 0.25, 1.3])
    muros.append([E + 0.2, BAJ_Z0, BAJ_X1 + 0.5, BAJ_Z0, 1.6])
    muros.append([E + 0.2, BAJ_Z1, BAJ_X1 + 0.5, BAJ_Z1, 1.6])
    muros.append([BAJ_X1 + 0.45, BAJ_Z0, BAJ_X1 + 0.45, BAJ_Z1, 1.6])
    cierre = [E, PORTON_Z - mm.MEDIO_PORTON, E, PORTON_Z + mm.MEDIO_PORTON, 1.6]

    ocular = mundo((tx, 0, tz), tg, (-0.55, 0, 0.0))
    puerta = mundo((fx, 0, fz), fg, (0, 0, 2.65))
    mark_sendero = [ESC_X, N + 1.3]
    mark_atajo = [E + 1.15, PORTON_Z]
    jugable = {
        "limites": {"x": [-2.4, 5.3], "z": [-2.3, 1.6]},
        "piso": {"centro": [1.6, 0.0], "tam": [16.4, 9.6]},
        "muros": [[round(v, 3) for v in m] for m in muros],
        "cierre_porton": cierre,
        "columnas": [[round(float(v), 3) for v in c] for c in columnas],
        "cajas": [[round(float(v), 3) for v in c] for c in cajas],
        "entrada": {"pos": [-3.55, -1.55], "mira": [0.5, 0.87]},
        "umbral_sendero": mark_sendero,
        "umbral_atajo": mark_atajo,
        "porton": [E, PORTON_Z],
        "interactuables": {
            "MesaClub": [round(maqueta[0], 2), round(maqueta[2] + 0.1, 2)],
            "Simulador": [round(portatil[0] + 0.12, 2), round(portatil[2] + 0.1, 2)],
            "Telescopio": [round(ocular[0] + 0.15, 2), round(ocular[2], 2)],
            "Atril": [ax, az],
            "Binoculares": [round(float(pb[0]), 2), round(float(pb[1]), 2)],
            "Banca": [BANCA[0], BANCA[1]],
            "Faro": [round(puerta[0], 2), round(puerta[2], 2)],
            "Pizarra": [piz[0], round(piz[1] + 0.55, 2)],
            "Farol": [round(farol_n[0] + 0.25, 2), round(farol_n[1] - 0.35, 2)],
        },
        "ruta": {
            "mesa": [mx - 0.3, mz + 0.86], "telescopio": [round(ocular[0] - 0.42, 2), round(ocular[2] + 0.25, 2)],
            "atril": [ax + 0.45, az + 0.95], "paso_1": [1.0, 0.3], "paso_2": [5.2, 0.15], "paso_3": [5.3, PORTON_Z],
            # v2: recorrido de las interacciones nuevas (banca, recolectables, farol y pizarra)
            "banca": [BANCA[0], BANCA[1] + 0.75], "tras_banca": [-1.9, -1.95],
            "AntenaVarilla": [1.30, -0.85], "CartaEstelar": [-3.05, 1.55], "Farol": [-1.7, 2.45],
            "Pizarra": [piz[0], round(piz[1] + 0.75, 2)], "tras_pizarra": [0.65, 2.9], "CableCobre": [4.6, 0.8],
        },
        "banca_asiento": [BANCA[0] + 0.35, BANCA[1] + 0.62],
        "banderines": lista_band,
        "cables_banderines": cables_band,
        # v2b: la luz va 0,6 m bajo la linterna y separada del poste (que ademas queda fuera de su mascara):
        # deja el charco dorado en las losas, a 1-1,5 m del pie, sin quemar el poste
        # v2c: la luz se adelanta hacia la terraza (0,85 m) para que el charco caiga en las losas y no en la balaustrada
        "farol_nuevo": {"pos": [farol_n[0], farol_n[1]], "bombilla": [farol_n[0], 2.25, farol_n[1], 0.11],
                        "luz": [farol_n[0] + 0.1, 1.5, farol_n[1] - 0.85, 2.0, 2.6],
                        "charco": [farol_n[0] + 0.15, farol_n[1] - 0.75, 1.45]},
        "regalo_luciernagas": [BANCA[0] - 0.4, BANCA[1] + 0.9],
        "reflejo_luna": REFLEJO_LUNA,
        "pizarra": pizarra,
        "recolectables": recolectables,
        "luciernagas": luciernagas,
        "puntos_ciudad": puntos_ciudad,
        "cables": cables,
        "bombillas": [[round(float(v), 3) for v in b] for b in bombillas],
        "ventanas": [[[round(float(v), 3) for v in p] for p in q] for q in ventanas],
        "porton_bombillas": [[round(float(v), 3) for v in b] for b in porton_b],
        "luces": luces,
        "luz_porton": luz_porton,
    }
    datos = {"generador": "herramientas/mallas/mirador_escena.py", "ambiente": {"pinceladas": 0.7}, "recursos": rec, "jugable": jugable}
    ZONA.mkdir(parents=True, exist_ok=True)
    (ZONA / "layout.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(rec), len(bombillas), len(ventanas)


def main():
    tris_plat, n_losas, pilares, bordillo = plataforma()
    tris_ladera = ladera()
    n_rec, n_bomb, n_vent = layout(pilares, bordillo)
    print(f"MIR-02: {tris_plat} triangulos, {n_losas} losas, {len(pilares) - 1} pilares de balaustrada")
    print(f"TER-15: {tris_ladera} triangulos, {len(BARRIO)} casas en el barrio, {len(LUCES_BARRIO)} ventanas encendidas")
    print(f"layout: {n_rec} recursos, {n_bomb} bombillas, {n_vent} ventanas encendidas")


if __name__ == "__main__":
    main()
