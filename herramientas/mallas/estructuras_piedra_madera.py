"""Estructuras de piedra y madera del ancla ANC_VISTA_JUEGO (lote 02): puente, escalinata y baranda.

Recursos (hojas HR_TER_v1 y HR_URB_v1):
  TER-10  puente de tablones: arriba a la derecha del ancla; cruza el arroyo a lo largo del eje X.
  TER-11  escalinata de mosaico: abajo a la izquierda; baja hacia +Z (hacia la camara).
  URB-09  baranda: dos pilares de piedra clara y barandales de metal oscuro; el tramo va a lo largo de X.

Cada recurso se escribe en pruebas/escena_exploracion/modelos/<ID>.glb, con un solo nodo "<ID>_<nombre>",
el origen en el centro de su base y apoyado en y = 0. Solo colores de la paleta maestra y sus mezclas.

Calibracion de color (carta de cubos con la luz de la escena, 2026-11-12): al sol, piedra_clara sale casi
blanca y madera1 sale rosada; el ancla tiene piedra melocoton y tablones anaranjados. Por eso la piedra se
calienta con tierra1/crema y la cara de arriba de los tablones se pinta con tierra2 y sol.

Uso, desde la raiz del proyecto:
    python -I herramientas/mallas/estructuras_piedra_madera.py [TER-10 TER-11 URB-09]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, RAIZ, Escena, Malla, marco, mezclar, solido_facetado  # noqa: E402

SALIDA = RAIZ / "pruebas" / "escena_exploracion" / "modelos"
ARRIBA = np.array([0.0, 1.0, 0.0])


def tono(sombra, base, luz):
    """Tres colores de un material pintado: sombra (abajo), base y luz (arriba)."""
    return tuple(np.asarray(c, float) for c in (sombra, base, luz))


# ---------- tonos ----------
# madera
TABLON = tono(PAL["madera2"], PAL["madera1"], mezclar(PAL["tierra2"], PAL["tierra1"], 0.3))
VETAS = [mezclar(PAL["tierra2"], PAL["sol"], 0.30), mezclar(PAL["madera1"], PAL["tierra2"], 0.65),
         mezclar(PAL["tierra2"], PAL["sol"], 0.12), mezclar(PAL["madera1"], PAL["tierra2"], 0.85)]
# la cara de sombra multiplica el albedo por el ambiente frio: con madera2 u oscuro en grandes superficies
# sale casi negra, por eso los postes y largueros arrancan en madera1 y madera2 queda para los acentos
POSTE = tono(PAL["madera1"], mezclar(PAL["madera1"], PAL["tierra2"], 0.7), mezclar(PAL["tierra2"], PAL["tierra1"], 0.4))
POSTE_TOPE = mezclar(PAL["tierra2"], PAL["tierra1"], 0.35)
LARGUERO = tono(PAL["madera2"], PAL["madera1"], mezclar(PAL["madera1"], PAL["tierra2"], 0.4))
CUERDA_CLARA = mezclar(PAL["crema"], PAL["tierra2"], 0.15)
CUERDA_OSCURA = mezclar(PAL["tierra2"], PAL["crema"], 0.25)
CLAVO = PAL["oscuro"]
CLAVO_BRILLO = mezclar(PAL["piedra_osc"], PAL["piedra_clara"], 0.5)
# piedra: la de las bases del puente es la de las rocas (piedra, malva) con musgo abajo
PIEDRA_BASE = tono(mezclar(PAL["piedra"], PAL["hierba_sombra"], 0.45), PAL["piedra"],
                   mezclar(PAL["piedra"], PAL["tierra1"], 0.5))
PIEDRA_BASE_TECHO = mezclar(PAL["piedra"], PAL["tierra1"], 0.45)
# piedra clara labrada (escalinata y pilares): al sol tiene que salir melocoton, como en el ancla (#F7BE94)
PIEDRA = tono(mezclar(PAL["piedra_clara"], PAL["petroleo"], 0.30), mezclar(PAL["piedra_clara"], PAL["tierra1"], 0.55),
              mezclar(PAL["tierra1"], PAL["crema"], 0.40))
PIEDRA_TECHO = mezclar(PAL["tierra1"], PAL["crema"], 0.30)
MOLDURA = tono(mezclar(PAL["tierra2"], PAL["petroleo"], 0.25), PAL["tierra2"], mezclar(PAL["tierra1"], PAL["sol"], 0.3))
# metal
METAL = tono(PAL["oscuro"], PAL["piedra_osc"], mezclar(PAL["piedra_osc"], PAL["piedra_clara"], 0.3))
METAL_BRILLO = mezclar(PAL["piedra_osc"], PAL["piedra_clara"], 0.4)
# mosaico. El cian se reserva para la tecnologia (Biblia, pilar 4): el azul claro del mosaico es petroleo con
# un 40 % de cian_medio, como el azul verdoso medido en el ancla (#618B9A), no el cian de los datos.
CREMA_T, SOL_T, PETROLEO_T = PAL["crema"], PAL["sol"], PAL["petroleo"]
AZUL_T = mezclar(PAL["petroleo"], PAL["cian_medio"], 0.4)
LECHADA = mezclar(PAL["piedra"], PAL["piedra_osc"], 0.25)


# ---------- ayudas de geometria ----------

def grad(t, tn):
    """Degradado pintado, el mismo del nucleo: sombra abajo, base hacia el 60 % y luz arriba."""
    s, b, l = tn
    t = min(max(float(t), 0.0), 1.0)
    return mezclar(s, b, min(1.0, t * 1.7)) if t < 0.6 else mezclar(b, l, (t - 0.6) / 0.4)


def normal_poligono(pts):
    """Normal de Newell: vale aunque los primeros puntos esten casi alineados."""
    n = np.zeros(3)
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n += [(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])]
    return n / max(np.linalg.norm(n), 1e-12)


def poligono(m, pts, cols, fuera=None):
    """Poligono convexo en abanico, con color por vertice; si se da 'fuera', mira hacia ese lado."""
    pts = [np.asarray(p, float) for p in pts]
    cols = [np.asarray(c, float) for c in cols]
    if fuera is not None and normal_poligono(pts) @ np.asarray(fuera, float) < 0:
        pts, cols = pts[::-1], cols[::-1]
    for i in range(1, len(pts) - 1):
        m.tri(pts[0], pts[i], pts[i + 1], cols[0], cols[i], cols[i + 1])


def rect(x0, x1, z0, z1):
    """Planta rectangular antihoraria vista desde arriba."""
    return [(x0, z1), (x1, z1), (x1, z0), (x0, z0)]


def rect_c(cx, cz, hx, hz, giro=0.0):
    """Planta rectangular centrada, girada 'giro' rad alrededor de Y."""
    c, s = math.cos(giro), math.sin(giro)
    return [(cx + c * x + s * z, cz - s * x + c * z) for x, z in rect(-hx, hx, -hz, hz)]


def octogono(cx, cz, h, c):
    """Seccion cuadrada de lado 2h con las aristas verticales achaflanadas c (lados impares = chaflanes)."""
    return [(cx - h + c, cz + h), (cx + h - c, cz + h), (cx + h, cz + h - c), (cx + h, cz - h + c),
            (cx + h - c, cz - h), (cx - h + c, cz - h), (cx - h, cz - h + c), (cx - h, cz + h - c)]


def encoger(planta, d):
    """Planta convexa antihoraria con cada lado metido d metros hacia dentro."""
    P = [np.asarray(p, float) for p in planta]
    lineas = []
    for i in range(len(P)):
        t = P[(i + 1) % len(P)] - P[i]
        t = t / np.linalg.norm(t)
        lineas.append((P[i] + np.array([t[1], -t[0]]) * d, t))
    salida = []
    for i in range(len(P)):
        (p1, t1), (p2, t2) = lineas[i - 1], lineas[i]
        s = np.linalg.solve(np.array([t1, -t2]).T, p2 - p1)[0]
        salida.append(p1 + s * t1)
    return salida


def prisma(m, planta0, planta1, y0, y1, tn, techo, rng, bisel=0.0, ymin=None, ymax=None, var=0.05,
           facetas=0.0, claros=(), realce=0.4, abanico=False):
    """Prisma entre planta0 (en y0) y planta1 (en y1); plantas convexas [(x, z)...] con el mismo numero de
    vertices, antihorarias vistas desde arriba. Lados con degradado vertical entre ymin e ymax, chaflan
    claro en la arista de arriba ('bisel') y techo pintado ('techo': color, funcion(punto) o None para no
    cerrarlo). 'facetas' parte cada lado en dos con un anillo intermedio movido al azar (tallado a mano);
    'claros' son los lados que se aclaran (aristas achaflanadas). 'abanico' parte el techo en triangulos
    desde el centro, cada uno con su tinte: con la luz celular todas las caras al sol reciben la misma luz,
    asi que las facetas se pintan. Devuelve los puntos del techo."""
    ymin = y0 if ymin is None else ymin
    ymax = y1 if ymax is None else ymax
    p0 = [np.asarray(p, float) for p in planta0]
    p1 = [np.asarray(p, float) for p in planta1]
    n = len(p0)
    cen = np.mean(p1, axis=0)
    yb = y1 - bisel
    f = (yb - y0) / max(y1 - y0, 1e-9)

    def col_lado(p, vf, claro=False):
        c = grad((p[1] - ymin) / max(ymax - ymin, 1e-9), tn)
        return (mezclar(c, tn[2], realce) if claro else c) * vf

    anillos = [[np.array([p[0], y0, p[1]]) for p in p0]]
    if facetas > 0:
        medio = []
        for a, b in zip(p0, p1):
            q = a + (b - a) * f * 0.5
            d = q - cen
            q = q + d / max(np.linalg.norm(d), 1e-9) * rng.uniform(-0.3, 1.0) * facetas
            medio.append(np.array([q[0], y0 + (yb - y0) * 0.5 + rng.uniform(-1, 1) * facetas, q[1]]))
        anillos.append(medio)
    anillos.append([np.array([q[0], yb, q[1]]) for q in (a + (b - a) * f for a, b in zip(p0, p1))])
    for r0, r1 in zip(anillos[:-1], anillos[1:]):
        for i in range(n):
            j = (i + 1) % n
            cara = [r0[i], r0[j], r1[j], r1[i]]
            cc = np.mean(cara, axis=0)
            vf = 1 + rng.normal(0, var)
            poligono(m, cara, [col_lado(p, vf, i in claros) for p in cara], cc - np.array([cen[0], cc[1], cen[1]]))
    tope = [np.array([q[0], y1, q[1]]) for q in (encoger(p1, bisel) if bisel > 0 else p1)]
    if bisel > 0:
        r = anillos[-1]
        for i in range(n):
            j = (i + 1) % n
            cara = [r[i], r[j], tope[j], tope[i]]
            cc = np.mean(cara, axis=0)
            vf = 1 + rng.normal(0, var)
            poligono(m, cara, [mezclar(col_lado(p, vf), tn[2], realce) for p in cara],
                     cc - np.array([cen[0], cc[1] - 1.0, cen[1]]))
    if techo is not None:
        pinta = (lambda p: techo(p)) if callable(techo) else (lambda p: np.asarray(techo, float))
        if abanico:
            c = np.mean(tope, axis=0) + np.array([0, rng.uniform(0.0, 0.003), 0])
            for i in range(n):
                a, b = tope[i], tope[(i + 1) % n]
                vf = 1 + rng.normal(0, 0.035)
                poligono(m, [c, a, b], [pinta(c) * vf * 1.03, pinta(a) * vf, pinta(b) * vf], ARRIBA)
        else:
            vf = 1 + rng.normal(0, var * 0.6)
            poligono(m, tope, [pinta(p) * vf for p in tope], ARRIBA)
    return tope


def bloque_tallado(m, cx, cz, abajo, arriba, alto, tn, techo, rng, mella=0.016):
    """Bloque de piedra tallada a mano (bases del puente): tronco de piramide con la cintura un poco salida
    y los hombros mordidos, cerrado por casco convexo y pintado con el degradado del nucleo."""
    pts = []
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        pts.append((cx + sx * abajo, rng.uniform(0, 0.004), cz + sz * abajo))
        w = (abajo + arriba) / 2 + rng.uniform(0.002, mella)
        pts.append((cx + sx * w, alto * rng.uniform(0.42, 0.6), cz + sz * w))
        hombro = alto - 0.035 + rng.uniform(-mella, mella) * 0.5
        pts.append((cx + sx * arriba, hombro, cz + sz * (arriba - rng.uniform(0.01, 0.03))))
        pts.append((cx + sx * (arriba - rng.uniform(0.01, 0.03)), hombro, cz + sz * arriba))
        pts.append((cx + sx * (arriba - 0.04), alto + rng.uniform(-0.005, 0.005), cz + sz * (arriba - 0.04)))
    sub = solido_facetado("base", np.array(pts, float), tn[0], tn[1], tn[2], rng, var=0.05, encima=(techo, 0.72, 0.86))
    m.anexar(sub)


def piramide(m, base, apice, tn, rng, var=0.04):
    """Remate en piramide sobre una planta (puntos 3D): cada cara oscura en la base y clara en la punta."""
    base = [np.asarray(p, float) for p in base]
    apice = np.asarray(apice, float)
    cen = np.mean(base, axis=0)
    for i in range(len(base)):
        a, b = base[i], base[(i + 1) % len(base)]
        vf = 1 + rng.normal(0, var)
        fuera = (a + b) / 2 - cen + np.array([0, 0.05, 0])
        poligono(m, [a, b, apice], [grad(0.55, tn) * vf, grad(0.55, tn) * vf, grad(1.0, tn) * vf], fuera)


def bloque_inclinado(m, x0, x1, z0, z1, ya, yb, tn, techo, rng, ymax, var=0.05):
    """Bloque de muro con el techo inclinado (alto ya en z0 y yb en z1): la zanca de la escalinata."""
    P = np.array([[x0, 0, z0], [x1, 0, z0], [x1, 0, z1], [x0, 0, z1],
                  [x0, ya, z0], [x1, ya, z0], [x1, yb, z1], [x0, yb, z1]], float)
    cen = P.mean(0)
    for idx in [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
        cara = P[list(idx)]
        vf = 1 + rng.normal(0, var)
        poligono(m, cara, [grad(p[1] / ymax, tn) * vf for p in cara], cara.mean(0) - cen)
    for tri in ([4, 5, 6], [4, 6, 7]):  # dos facetas pintadas, cada una con su tinte
        cara = P[tri]
        vf = 1 + rng.normal(0, 0.035)
        poligono(m, cara, [techo(p) * vf for p in cara], ARRIBA)


def cuerda(m, centros, radio, rng, lados=6, vuelta=0.45, tapas=True):
    """Cuerda torcida: tubo de pocos lados cuyos anillos giran a lo largo (una vuelta cada 'vuelta' metros),
    con hebras claras y oscuras alternas que quedan en espiral; la cara de abajo es mas oscura."""
    centros = [np.asarray(c, float) for c in centros]
    anillos, recorrido = [], 0.0
    for i, c in enumerate(centros):
        if i:
            recorrido += np.linalg.norm(c - centros[i - 1])
        tang = centros[min(i + 1, len(centros) - 1)] - centros[max(i - 1, 0)]
        u, v = marco(tang)
        a0 = recorrido / vuelta * 2 * math.pi
        anillos.append([c + (u * math.cos(a0 + k * 2 * math.pi / lados) + v * math.sin(a0 + k * 2 * math.pi / lados))
                        * radio for k in range(lados)])

    def col(p, c, base):
        alto = (p - c)[1] / radio  # -1 abajo, +1 arriba
        return base * (0.80 + 0.20 * (alto * 0.5 + 0.5))

    for a in range(len(centros) - 1):
        ca, cb = centros[a], centros[a + 1]
        for k in range(lados):
            k2 = (k + 1) % lados
            base = CUERDA_CLARA if k % 2 == 0 else CUERDA_OSCURA
            base = base * (1 + rng.normal(0, 0.03))
            cara = [anillos[a][k], anillos[a][k2], anillos[a + 1][k2], anillos[a + 1][k]]
            fuera = np.mean(cara, axis=0) - (ca + cb) / 2
            poligono(m, cara, [col(cara[0], ca, base), col(cara[1], ca, base), col(cara[2], cb, base),
                               col(cara[3], cb, base)], fuera)
    if tapas:
        for i, sentido in ((0, -1), (-1, 1)):
            tang = centros[-1] - centros[-2] if i == -1 else centros[1] - centros[0]
            poligono(m, anillos[i], [CUERDA_OSCURA] * lados, tang * sentido)


def mosaico(m, O, U, V, N, ancho, alto, colores, rng, largo=0.06, amplitud=0.05, onda=0.9, fase=0.0,
            junta=0.007, relieve=0.004):
    """Mosaico de ondas sobre una plancha (origen O, ejes U a lo ancho y V a lo alto, normal N): bandas
    paralelas que siguen una sinusoide, partidas en teselas que siguen la onda, como en el ancla. Las bandas
    del borde quedan recortadas por la onda. Cada tesela es un quad un poco levantado sobre la lechada."""
    O, U, V, N = (np.asarray(x, float) for x in (O, U, V, N))

    def P(u, v, e=0.0):
        return O + U * u + V * v + N * e

    poligono(m, [P(0, 0), P(ancho, 0), P(ancho, alto), P(0, alto)],
             [LECHADA * 0.88, LECHADA * 0.88, LECHADA * 1.04, LECHADA * 1.04], N)
    K = len(colores)

    def borde(k, u):
        if k <= 0:
            return 0.0
        if k >= K:
            return alto
        return float(np.clip(alto * k / K + amplitud * math.sin(2 * math.pi * u / onda + fase), 0.0, alto))

    teselas = 0
    for k in range(K):
        cortes = [0.0]
        u = largo * (0.5 if k % 2 else 1.0) + rng.uniform(-0.15, 0.15) * largo
        while u < ancho - largo * 0.4:
            cortes.append(u)
            u += largo * rng.uniform(0.85, 1.15)
        cortes.append(ancho)
        for ua, ub in zip(cortes[:-1], cortes[1:]):
            ua, ub = ua + junta / 2, ub - junta / 2
            lados = []
            for uu in (ua, ub):
                lo, hi = borde(k, uu) + junta / 2, borde(k + 1, uu) - junta / 2
                lados.append((lo, hi, hi - lo))
            if lados[0][2] < 0.004 and lados[1][2] < 0.004:
                continue
            esquinas = []
            for uu, (lo, hi, grueso) in zip((ua, ub), lados):
                if grueso < 0.004:  # la onda cierra la banda: tesela triangular
                    mid = (lo + hi) / 2
                    lo = hi = mid
                esquinas.append((uu, lo, hi))
            c = np.asarray(colores[k], float) * (1 + rng.normal(0, 0.05))
            if rng.random() < 0.08:  # alguna tesela de otro lote: mano artesana
                c = mezclar(c, colores[(k + 1) % K], 0.18)
            bajo, alto_c = c * 0.92, mezclar(c, PAL["crema"], 0.10)
            (u0, lo0, hi0), (u1, lo1, hi1) = esquinas
            pts = [P(u0, lo0, relieve), P(u1, lo1, relieve), P(u1, hi1, relieve), P(u0, hi0, relieve)]
            cols = [bajo, bajo, alto_c, alto_c]
            if lo0 == hi0:
                pts, cols = pts[:3], cols[:3]
            elif lo1 == hi1:
                pts, cols = [pts[0], pts[1], pts[3]], [cols[0], cols[1], cols[3]]
            poligono(m, pts, cols, N)
            teselas += 1
    return teselas


# ---------- TER-10: puente de tablones ----------

def puente(rng):
    """Tablones gruesos de travesano sobre dos largueros; cuatro postes en bases de piedra y barandas de
    cuerda torcida con comba, enrolladas dos vueltas en cada poste (HR_TER_v1 y el ancla)."""
    m = Malla("TER-10_puente")
    LARGO, ANCHO, N_TAB, JUNTA = 2.6, 1.3, 6, 0.035
    ancho_t = (LARGO - (N_TAB - 1) * JUNTA) / N_TAB
    Y0, Y1 = 0.15, 0.24          # tablones: 9 cm de grueso, la cubierta queda a 24 cm del suelo
    PX, PZ = 1.10, 0.74          # postes en las cuatro esquinas, por fuera de las puntas de los tablones
    Z_LARG = 0.40

    # largueros oscuros bajo la cubierta, apoyados en las dos orillas
    for z in (-Z_LARG, Z_LARG):
        planta = rect(-1.33, 1.33, z - 0.06, z + 0.06)
        prisma(m, planta, planta, 0.0, Y0, LARGUERO, LARGUERO[2], rng, bisel=0.01)

    # tablones con juntas, cada uno un poco torcido y con vetas pintadas
    for i in range(N_TAB):
        cx = -LARGO / 2 + ancho_t / 2 + i * (ancho_t + JUNTA)
        dz, giro = rng.uniform(-0.02, 0.02), rng.uniform(-0.02, 0.02)
        hz = ANCHO / 2 + rng.uniform(-0.03, 0.02)
        dy = rng.uniform(-0.004, 0.006)
        planta = rect_c(cx, dz, ancho_t / 2, hz, giro)
        tope = prisma(m, planta, planta, Y0 + dy, Y1 + dy, TABLON, None, rng, bisel=0.012, realce=0.5)
        A, B, C, D = tope  # (-u,+w) (+u,+w) (+u,-w) (-u,-w)

        def punto(fu, fw):
            return (1 - fu) * (1 - fw) * D + fu * (1 - fw) * C + fu * fw * B + (1 - fu) * fw * A

        vetas = [VETAS[j] for j in rng.permutation(len(VETAS))[:3]]
        cortes_u = [0.0, 1 / 3 + rng.uniform(-0.06, 0.06), 2 / 3 + rng.uniform(-0.06, 0.06), 1.0]
        for iu in range(3):
            for fw0, fw1 in ((0.0, 0.5), (0.5, 1.0)):
                cara = [punto(cortes_u[iu], fw0), punto(cortes_u[iu + 1], fw0),
                        punto(cortes_u[iu + 1], fw1), punto(cortes_u[iu], fw1)]
                v = vetas[iu] * (1 + rng.normal(0, 0.03))
                punta = mezclar(v, PAL["madera1"], 0.30) * 0.92  # las puntas, gastadas y oscuras
                medio = v * 1.04
                cols = [punta if fw in (0.0, 1.0) else medio for fw in (fw0, fw0, fw1, fw1)]
                poligono(m, cara, cols, ARRIBA)
        # clavos sobre cada larguero
        du = (C - D) / np.linalg.norm(C - D)
        dw = (A - D) / np.linalg.norm(A - D)
        for zl in (-Z_LARG, Z_LARG):
            fw = (zl - dz + hz) / (2 * hz)
            for fu in (0.24, 0.76):
                p = punto(fu, fw) + np.array([0, 0.003, 0])
                s = 0.014
                cara = [p - du * s - dw * s, p + du * s - dw * s, p + du * s + dw * s, p - du * s + dw * s]
                poligono(m, cara, [CLAVO, CLAVO, CLAVO_BRILLO, CLAVO], ARRIBA)

    # bases de piedra, postes y rollos de cuerda
    rollos = {}
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = sx * PX, sz * PZ
            bloque_tallado(m, cx, cz, 0.19, 0.145, 0.30, PIEDRA_BASE, PIEDRA_BASE_TECHO, rng)
            h = 0.085  # medio lado del poste (17 cm, grueso como en el ancla)
            tope = prisma(m, octogono(cx, cz, h, 0.02), octogono(cx, cz, h - 0.003, 0.02), 0.29, 0.98, POSTE,
                          POSTE_TOPE, rng, bisel=0.016, facetas=0.004, claros=(1, 3, 5, 7), realce=0.45)
            # marca del clavo en la cabeza del poste
            c = np.mean(tope, axis=0) + np.array([0, 0.002, 0])
            s = 0.018
            poligono(m, [c + [-s, 0, s], c + [s, 0, s], c + [s, 0, -s], c + [-s, 0, -s]],
                     [CLAVO, CLAVO, PAL["madera2"], CLAVO], ARRIBA)
            # dos vueltas de cuerda en el tercio alto del poste (camino de cuadrado redondeado)
            r = 0.027
            puntos = []
            pasos = 24
            a0 = math.pi / 2 if sz > 0 else -math.pi / 2  # empieza y termina por fuera del puente
            for k in range(pasos + 1):
                a = a0 + 2 * 2 * math.pi * k / pasos
                d = np.array([math.cos(a), math.sin(a)])
                cuadrado = d / max(abs(d[0]), abs(d[1])) * (h + r * 0.9)
                circulo = d * (h * 1.15 + r)
                q = mezclar(cuadrado, circulo, 0.35)
                puntos.append((cx + q[0], 0.755 + 2 * 2 * r * k / pasos, cz + q[1]))
            cuerda(m, puntos, r, rng)
            rollos[(sx, sz)] = (cx, cz, h + r)

    # barandas de cuerda con comba, de poste a poste a lo largo del puente
    for sz in (-1, 1):
        xa = rollos[(-1, sz)][0] + rollos[(-1, sz)][2]
        xb = rollos[(1, sz)][0] - rollos[(1, sz)][2]
        z = rollos[(-1, sz)][1]
        ya, comba, pasos = 0.81, 0.13, 30
        puntos = []
        for k in range(pasos + 1):
            t = k / pasos
            puntos.append((xa + (xb - xa) * t, ya - 4 * comba * t * (1 - t), z))
        cuerda(m, puntos, 0.023, rng)
    return m


# ---------- TER-11: escalinata de mosaico ----------

def escalinata(rng):
    """Cuatro contrahuellas con mosaico de ondas, un descanso con mosaico y zancas de piedra con pilaretes
    arriba (HR_TER_v1 y el ancla). Baja hacia +Z: lo alto queda al fondo (-Z)."""
    m = Malla("TER-11_escalinata")
    H, E, VUELO, XI, YMAX = 0.17, 0.045, 0.02, 1.03, 0.97
    niveles = [0.68, 0.51, 0.34, 0.17]       # techo de cada huella
    narices = [-0.52, -0.24, 0.50, 0.80]     # borde delantero de cada huella
    Z_FONDO = -0.80

    def techo_huella(z_atras, z_nariz):
        def f(p):
            t = (p[2] - z_atras) / max(z_nariz - z_atras, 1e-9)  # 0 junto a la contrahuella, 1 en la nariz
            return mezclar(mezclar(PIEDRA[1], PIEDRA_TECHO, 0.45), PIEDRA_TECHO, t)
        return f

    def losas(z0, z1, y0, y1, x0=-XI, x1=XI, piezas=3):
        """Huella partida en losas con juntas, sobre un lecho oscuro que se ve por las juntas."""
        anchos = rng.uniform(0.8, 1.2, piezas)
        bordes = x0 + np.concatenate([[0], np.cumsum(anchos)]) / anchos.sum() * (x1 - x0)
        poligono(m, [(x0, y0 + 0.002, z1), (x1, y0 + 0.002, z1), (x1, y0 + 0.002, z0), (x0, y0 + 0.002, z0)],
                 [LECHADA * 0.7] * 4, ARRIBA)
        for a, b in zip(bordes[:-1], bordes[1:]):
            ja = 0.004 if a > x0 + 1e-6 else 0.0
            jb = 0.004 if b < x1 - 1e-6 else 0.0
            planta = rect(a + ja, b - jb, z0, z1)
            dy = rng.uniform(-0.003, 0.003)
            prisma(m, planta, planta, y0, y1 + dy, PIEDRA, techo_huella(z0, z1), rng, bisel=0.012,
                   ymin=0.0, ymax=YMAX, abanico=True)

    teselas = 0
    for k, (y, zn) in enumerate(zip(niveles, narices)):
        z_atras = Z_FONDO if k == 0 else narices[k - 1] - VUELO
        if k == 2:
            # descanso: nariz, marco de piedra y mosaico de ondas en el piso
            losas(0.40, zn, y - E, y)
            for x0, x1 in ((-XI, -0.95), (0.95, XI)):
                planta = rect(x0, x1, z_atras, 0.40)
                prisma(m, planta, planta, y - E, y, PIEDRA, PIEDRA_TECHO, rng, bisel=0.006, ymin=0, ymax=YMAX,
                       abanico=True)
            planta = rect(-0.95, 0.95, z_atras, -0.19)
            prisma(m, planta, planta, y - E, y, PIEDRA, PIEDRA_TECHO, rng, bisel=0.006, ymin=0, ymax=YMAX,
                   abanico=True)
            teselas += mosaico(m, (-0.95, y - 0.007, 0.40), (1, 0, 0), (0, 0, -1), (0, 1, 0), 1.90, 0.59,
                               [CREMA_T, CREMA_T, PETROLEO_T, SOL_T, AZUL_T, PETROLEO_T, CREMA_T, CREMA_T],
                               rng, largo=0.065, amplitud=0.09, onda=0.95, fase=0.4)
        else:
            losas(z_atras, zn, y - E, y)
        # contrahuella con mosaico, bajo la nariz
        zr = zn - VUELO
        y_bajo = y - H
        # las contrahuellas miran a la camara y quedan en la sombra fria: sin petroleo, que ahi sale negro
        colores = [AZUL_T, SOL_T, CREMA_T] if k % 2 == 0 else [CREMA_T, SOL_T, AZUL_T]
        teselas += mosaico(m, (-XI, y_bajo, zr), (1, 0, 0), (0, 1, 0), (0, 0, 1), 2 * XI, (y - E) - y_bajo,
                           colores, rng, largo=0.055, amplitud=0.028, onda=0.75, fase=1.3 * k)

    # espalda de la escalinata (se ve solo desde atras o de lado)
    tn_espalda = [grad(0.0, PIEDRA), grad(0.0, PIEDRA), grad(0.6, PIEDRA), grad(0.6, PIEDRA)]
    poligono(m, [(-XI, 0, Z_FONDO), (XI, 0, Z_FONDO), (XI, niveles[0] - E, Z_FONDO), (-XI, niveles[0] - E, Z_FONDO)],
             tn_espalda, (0, 0, -1))

    # zancas: pilarete arriba, dos bloques de muro inclinados y un bloque al pie
    def y_zanca(z):
        return 0.80 - 0.407 * (z + 0.50)

    def techo_zanca(p):
        return mezclar(PIEDRA[1], PIEDRA_TECHO, 0.55 + 0.45 * min(1.0, max(0.0, p[1] / 0.8)))

    for lado in (-1, 1):
        xi, xe = lado * 1.01, lado * 1.25
        x0, x1 = min(xi, xe), max(xi, xe)
        pc = lado * 1.13
        cuerpo = rect_c(pc, -0.64, 0.14, 0.14)
        prisma(m, cuerpo, cuerpo, 0.0, 0.84, PIEDRA, None, rng, bisel=0.0, ymax=YMAX, facetas=0.006)
        sombrero = rect_c(pc, -0.64, 0.16, 0.16)
        tope = prisma(m, sombrero, sombrero, 0.84, 0.91, PIEDRA, None, rng, bisel=0.016, ymax=YMAX)
        piramide(m, tope, (pc, 0.965, -0.64), PIEDRA, rng)
        for za, zb in ((-0.494, 0.040), (0.046, 0.574)):
            bloque_inclinado(m, x0, x1, za, zb, y_zanca(za), y_zanca(zb), PIEDRA, techo_zanca, rng, YMAX)
        planta = rect(x0, x1, 0.580, 0.80)
        prisma(m, planta, planta, 0.0, 0.36, PIEDRA, PIEDRA_TECHO, rng, bisel=0.014, ymax=YMAX, facetas=0.005,
               abanico=True)
    print(f"  TER-11: {teselas} teselas de mosaico")
    return m


# ---------- URB-09: baranda ----------

def pilar(m, cx, rng):
    """Pilar de piedra clara: zocalo, fuste, moldura, sombrero con chaflan y remate en piramide."""
    Y = 0.85
    prisma(m, rect_c(cx, 0, 0.205, 0.205), rect_c(cx, 0, 0.200, 0.200), 0.0, 0.12, PIEDRA, PIEDRA_TECHO, rng,
           bisel=0.02, ymax=Y)
    prisma(m, rect_c(cx, 0, 0.175, 0.175), rect_c(cx, 0, 0.172, 0.172), 0.12, 0.61, PIEDRA, PIEDRA_TECHO, rng,
           ymax=Y, facetas=0.006)
    cuello = rect_c(cx, 0, 0.157, 0.157)
    prisma(m, cuello, cuello, 0.61, 0.655, MOLDURA, None, rng)
    tope = prisma(m, rect_c(cx, 0, 0.200, 0.200), rect_c(cx, 0, 0.205, 0.205), 0.655, 0.745, PIEDRA, None, rng,
                  bisel=0.015, ymax=Y)
    piramide(m, tope, (cx, Y, 0.0), PIEDRA, rng)


def baranda(rng):
    """Tramo de 3 m: dos pilares (centros a 2,65 m: al encadenar tramos, los pilares coinciden) unidos por
    dos barandales de metal oscuro con barrotes verticales finos."""
    m = Malla("URB-09_baranda")
    for cx in (-1.325, 1.325):
        pilar(m, cx, np.random.default_rng(909))  # los dos pilares iguales
    # barandal de 5,5 cm y barrotes de 2,6 cm: a tamano de juego (190 px/m en 1080p) dan 10 y 5 px
    for y0, y1 in ((0.155, 0.20), (0.55, 0.605)):
        planta = rect(-1.155, 1.155, -0.0275, 0.0275)
        prisma(m, planta, planta, y0, y1, METAL, METAL_BRILLO, rng, bisel=0.008, realce=0.35)
    for x in np.linspace(-1.05, 1.05, 15):
        planta = rect_c(x, 0.0, 0.013, 0.013)
        prisma(m, planta, planta, 0.20, 0.55, METAL, None, rng, ymin=0.155, ymax=0.605)
    return m


RECURSOS = {
    "TER-10": ("TER-10_puente", puente, 10),
    "TER-11": ("TER-11_escalinata", escalinata, 11),
    "URB-09": ("URB-09_baranda", baranda, 9),
}


def main():
    pedidos = sys.argv[1:] or list(RECURSOS)
    for rid in pedidos:
        nombre, fabrica, semilla = RECURSOS[rid]
        m = fabrica(np.random.default_rng(semilla))
        e = Escena("herramientas/mallas/estructuras_piedra_madera.py")
        e.nodo(nombre, e.malla(m, nombre=nombre))
        ruta = e.guardar(SALIDA / f"{rid}.glb")
        lo, hi = m.caja_limites()
        centro = (lo + hi) / 2
        print(f"{rid}: {len(m)} triangulos, tamano {np.round(hi - lo, 3).tolist()} m, "
              f"centro x {centro[0]:+.3f} z {centro[2]:+.3f}, y min {lo[1]:+.3f} -> {ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
