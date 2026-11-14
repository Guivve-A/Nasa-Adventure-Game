"""Escena de exploracion v1: la vista aprobada del sendero (ANC_VISTA_JUEGO) construida en 3D.

Genera el terreno (suelo facetado, sendero de tierra, cauce del arroyo con dos cascadas y la plaza baja
tras la baranda), el agua, las rocas y la distribucion de todos los recursos (layout.json) que lee
pruebas/escena_exploracion/escena.gd. Las posiciones salen de medir el ancla: la protagonista esta en
el origen y la camara de juego mira hacia -Z (lo lejano es -Z; la derecha de la imagen es +X).

Uso:  python -I herramientas/mallas/escena_v1.py
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nucleo import PAL, Escena, Malla, caja, fibonacci, mezclar, roca, solido_facetado  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
ESCENA = RAIZ / "pruebas" / "escena_exploracion"
MODELOS = ESCENA / "modelos"
LOTE = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "Modelado" / "Lote_04"

# ---------- camara y trazados medidos en el ancla ----------
# Cada punto se mide en pixeles normalizados (u, v) sobre L02_exploracion_camara_alta.png (u a la derecha,
# v hacia abajo) y se lleva al suelo con la misma camara de la escena (herramientas/camara_ancla.py). Asi la
# escena cae donde la pinta el ancla. Iteracion 1 del bucle de ajuste al ancla (2026-11-12).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from camara_ancla import Camara  # noqa: E402

CAMARA = {"inclinacion_deg": 48.0, "fov_deg": 40.0, "objetivo": [0.45, 0.0, -0.6],
          "inclinacion_objetos": 0.45, "encuadres": {"21": 0.21, "12": 0.125}, "alto_personaje": 1.05}
_CAM = Camara(datos=CAMARA)


def suelo(u, v, y=0.0):
    """Punto (x, z) del mundo, a la altura y, que se ve en el pixel (u, v) del ancla."""
    return _CAM.al_suelo(u, v, y)


def trazado(puntos, y=0.0):
    return np.array([suelo(u, v, y) for u, v in puntos])


NIVELES = [-0.06, -0.34, -0.62]                  # nivel del agua antes, entre y despues de las cascadas (saltos de 28 cm)
SENDERO = trazado([(0.37, 1.45), (0.38, 1.22), (0.41, 1.0), (0.42, 0.82), (0.46, 0.65), (0.52, 0.5),
                   (0.55, 0.4), (0.58, 0.31), (0.63, 0.23), (0.665, 0.215)])
# rama que sube entre la copa y las rocas (arriba al centro del ancla)
SENDERO_LEJOS = trazado([(0.60, 0.27), (0.575, 0.15), (0.555, 0.05), (0.54, -0.06), (0.53, -0.2), (0.52, -0.4)])
ARROYO = np.array([suelo(0.95, -0.4, NIVELES[0]), suelo(0.92, -0.15, NIVELES[0]), suelo(0.88, 0.0, NIVELES[0]),
                   suelo(0.85, 0.09, NIVELES[1]), suelo(0.78, 0.19, NIVELES[1]), suelo(0.80, 0.27, NIVELES[1]),
                   suelo(0.86, 0.32, NIVELES[2]), suelo(0.93, 0.38, NIVELES[2]), suelo(1.0, 0.42, NIVELES[2]),
                   suelo(1.12, 0.48, NIVELES[2]), suelo(1.3, 0.55, NIVELES[2])])
CASCADAS = [suelo(0.855, 0.085, -0.16), suelo(0.84, 0.295, -0.33)]   # donde el agua baja un escalon
# borde de la plaza baja con baranda (abajo a la izquierda): pilares del ancla en (0,08; 0,77) y (0,28; 0,97)
BARANDA = trazado([(-0.16, 0.56), (0.36, 1.06)])
BORDE_B = np.array([BARANDA[1], BARANDA[1] + np.array([-1.15, 5.75])])  # segundo borde: no invade el sendero
PLAZA_Y = -0.8  # la escalinata de mosaico (TER-11) baja 0,8 m desde la baranda hacia la plaza, como en el ancla
_P0, _P1 = np.array(suelo(0.67, 0.215, 0.02)), np.array(suelo(0.80, 0.135, 0.02))  # extremos del puente
PUENTE = {"pos": tuple((_P0 + _P1) / 2), "eje": tuple((_P1 - _P0) / np.linalg.norm(_P1 - _P0))}


def dist_polilinea(px, pz, pts):
    """Distancia minima de cada punto a la polilinea y abscisa curvilinea del punto mas cercano."""
    p = np.stack([px, pz], -1)[..., None, :]
    a, b = pts[:-1], pts[1:]
    ab = b - a
    t = np.clip(((p - a) * ab).sum(-1) / (ab * ab).sum(-1), 0, 1)
    cerca = a + t[..., None] * ab
    d = np.linalg.norm(p - cerca, axis=-1)
    i = d.argmin(-1)
    largos = np.concatenate([[0], np.cumsum(np.linalg.norm(ab, axis=1))])
    s = largos[i] + np.take_along_axis(t, i[..., None], -1)[..., 0] * np.linalg.norm(ab, axis=1)[i]
    return d.min(-1), s


def _lado(linea, x, z):
    (ax, az), (bx, bz) = linea
    largo = math.hypot(bx - ax, bz - az)
    return ((bx - ax) * (z - az) - (bz - az) * (x - ax)) / largo


def lado_baranda(x, z):
    """Distancia con signo a la plaza baja: > 0 dentro (tras la baranda y a la izquierda del borde B)."""
    return np.minimum(_lado(BARANDA, x, z), _lado(BORDE_B, x, z))


def nivel_agua(x, z):
    _, s = dist_polilinea(x, z, ARROYO)
    _, s1 = dist_polilinea(np.array([CASCADAS[0][0]]), np.array([CASCADAS[0][1]]), ARROYO)
    _, s2 = dist_polilinea(np.array([CASCADAS[1][0]]), np.array([CASCADAS[1][1]]), ARROYO)
    return np.where(s < s1[0], NIVELES[0], np.where(s < s2[0], NIVELES[1], NIVELES[2]))


def ruido(x, z):
    return (np.sin(1.3 * x + 0.7 * z) * 0.5 + np.sin(2.3 * z - 1.7 * x + 1.1) * 0.3
            + np.sin(4.1 * x + 3.7 * z + 2.0) * 0.2)


def ancho_sendero(z):
    # iteracion 13: medido en el ancla (borde a borde visible 1,5 m cerca, 1,05-1,2 m lejos); el color de tierra
    # se desvanece 0,25 m mas alla, asi que el ancho del trazado es el visible menos 0,25 m
    return np.interp(-z, [-10, 0, 1.3, 2.1, 3.0], [1.3, 1.25, 0.93, 0.82, 0.85])


def altura(x, z):
    h = ruido(x, z) * 0.045
    ds, _ = dist_polilinea(x, z, SENDERO)
    ds2, _ = dist_polilinea(x, z, SENDERO_LEJOS)
    en_sendero = np.clip(1 - (np.minimum(ds, ds2) - ancho_sendero(z) / 2) / 0.35, 0, 1)
    h = h * (1 - 0.7 * en_sendero) - 0.035 * en_sendero
    # cauce del arroyo: lecho bajo el agua y orillas en talud
    da, _ = dist_polilinea(x, z, ARROYO)
    lecho = nivel_agua(x, z) - 0.28
    medio_ancho = 0.6  # iteracion 8: cauce mas angosto, como el arroyo del ancla
    t = np.clip((da - medio_ancho) / 0.75, 0, 1)
    h = np.where(da < medio_ancho + 0.75, mezclar(lecho, h, t * t * (3 - 2 * t)), h)
    # plaza baja: el muro de contencion tapa el talud
    tp = np.clip(lado_baranda(x, z) / 0.35, 0, 1)
    return mezclar(h, PLAZA_Y, tp)


def color_suelo(x, z, h, rng):
    n = ruido(x * 1.7 + 3, z * 1.7 - 2) * 0.5 + 0.5
    # el suelo bajo la hierba es oscuro (medido en el ancla: media #565E31); las puntas claras las ponen las briznas
    # iteracion 3: suelo de hierba menos pardo y mas oliva (ancla en sombra #6a6438 a #8f7b31)
    hierba = mezclar(mezclar(PAL["hierba_sombra"], PAL["oscuro"], 0.08), PAL["hierba_sol"], 0.05 + 0.3 * n)
    ds, _ = dist_polilinea(x, z, SENDERO)
    ds2, _ = dist_polilinea(x, z, SENDERO_LEJOS)
    w = np.clip(1 - (np.minimum(ds, ds2) - ancho_sendero(z) / 2) / 0.25, 0, 1)
    # tierra del ancla: pardo anaranjado con algo de oliva (#907333 a #9d774d), no rosado
    centro = np.clip(1 - np.minimum(ds, ds2) / (ancho_sendero(z) / 2), 0, 1)
    tierra = mezclar(mezclar(mezclar(PAL["tierra2"], PAL["dorado"], 0.2), PAL["oscuro"], 0.1), PAL["sol"],
                     0.04 + 0.14 * centro * n)
    c = mezclar(hierba, tierra, w[..., None])
    da, _ = dist_polilinea(x, z, ARROYO)
    orilla = np.clip(1 - (da - 0.85) / 0.6, 0, 1)
    piedra = mezclar(PAL["piedra"], PAL["tierra2"], 0.4 * n)
    c = mezclar(c, piedra, orilla[..., None])
    lado = lado_baranda(x, z)
    baldosa = mezclar(mezclar(PAL["tierra1"], PAL["crema"], 0.3), PAL["piedra"], 0.2 + 0.2 * n)  # piedra calida del ancla
    c = np.where((lado > 0.1)[..., None], baldosa, c)
    return c * (1 + rng.normal(0, 0.012))


def terreno(rng, ancho=30.0, fondo=26.0, celda=0.46):
    xs = np.arange(-ancho / 2, ancho / 2 + 1e-6, celda)
    zs = np.arange(-fondo * 0.62, fondo * 0.38 + 1e-6, celda)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    X = X + rng.uniform(-0.12, 0.12, X.shape) * celda
    Z = Z + rng.uniform(-0.12, 0.12, Z.shape) * celda
    H = altura(X, Z) + rng.uniform(-0.01, 0.01, X.shape)
    m = Malla("TER-suelo")
    for i in range(len(xs) - 1):
        a = np.stack([X[i], H[i], Z[i]], -1)
        b = np.stack([X[i + 1], H[i + 1], Z[i + 1]], -1)
        for j in range(len(zs) - 1):
            p00, p10, p11, p01 = a[j], b[j], b[j + 1], a[j + 1]
            # cada triangulo toma un color de su centro: facetas limpias, con degradado por altura
            for tri in ((p00, p01, p11), (p00, p11, p10)):
                cen = np.mean(tri, 0)
                c = color_suelo(np.array(cen[0]), np.array(cen[2]), cen[1], rng)
                cols = [c * (1 + 0.25 * (p[1] - cen[1])) for p in tri]
                m.tri(*tri, *cols)
    return m


def agua():
    """Cinta de agua a lo largo del arroyo, con escalones en las cascadas (espuma = blanco)."""
    m = Malla("TER-09_agua", material="Agua")
    pts = ARROYO
    muestras = []
    for k in range(len(pts) - 1):
        for t in np.linspace(0, 1, 7, endpoint=False):
            muestras.append(pts[k] * (1 - t) + pts[k + 1] * t)
    muestras.append(pts[-1])
    muestras = np.array(muestras)
    niveles = nivel_agua(muestras[:, 0], muestras[:, 1])
    medio = 1.05  # mas ancho que el lecho: el borde queda bajo el talud de la orilla (el arroyo del ancla es angosto)
    tras_cascada = False
    for k in range(len(muestras) - 1):
        p, q = muestras[k], muestras[k + 1]
        d = q - p
        n = np.array([-d[1], d[0]]) / np.linalg.norm(d)
        y0, y1 = niveles[k], niveles[k + 1]
        cascada = abs(y1 - y0) > 1e-3
        a = (p[0] + n[0] * medio, y0, p[1] + n[1] * medio)
        b = (p[0] - n[0] * medio, y0, p[1] - n[1] * medio)
        c = (q[0] - n[0] * medio, y1, q[1] - n[1] * medio)
        e = (q[0] + n[0] * medio, y1, q[1] + n[1] * medio)
        espuma = np.ones(3) if cascada else np.zeros(3)
        orilla = np.full(3, 0.35)
        # al pie de cada cascada queda un manto de espuma que se deshace aguas abajo
        arriba = np.full(3, 0.75) if tras_cascada else orilla
        m.quad(a, e, c, b, arriba if not cascada else espuma, orilla if not cascada else espuma,
               espuma if cascada else orilla, arriba if not cascada else espuma)
        tras_cascada = cascada
    return m


def mosaico(rng, lado=0.14, junta=0.014):
    """Suelo de mosaico de la plaza baja (abajo a la izquierda del ancla): teselas en ondas azul, crema,
    naranja y turquesa, con juntas por donde asoma la piedra del suelo."""
    m = Malla("TER-13_mosaico")
    centro = np.array(suelo(0.06, 0.93, PLAZA_Y))
    azul = mezclar(PAL["petroleo"], PAL["cian_medio"], 0.45)
    turquesa = mezclar(PAL["cian_medio"], PAL["brillo"], 0.25)
    naranja = mezclar(PAL["sol"], PAL["coral"], 0.35)
    crema = mezclar(PAL["crema"], PAL["brillo"], 0.2)
    for i in np.arange(-3.0, 3.0, lado):
        for j in np.arange(-3.0, 3.0, lado):
            x, z = centro[0] + i, centro[1] + j
            if lado_baranda(np.array(x), np.array(z)) < 0.12:
                continue
            onda = math.sin(0.95 * x + 0.55 * z + 0.9 * math.sin(0.6 * z - 0.3 * x))
            col = azul if onda > 0.55 else crema if onda > 0.15 else naranja if onda > -0.3 else crema if onda > -0.6 else turquesa
            col = col * rng.uniform(0.93, 1.05)
            y = PLAZA_Y + 0.006
            a, b = lado / 2 - junta / 2, lado / 2 - junta / 2
            m.quad((x - a, y, z + b), (x + a, y, z + b), (x + a, y, z - b), (x - a, y, z - b), col)
    return m


def roca_escena(nombre, semilla, escala, npts=32, musgo=True):
    """Roca del ancla: gris violaceo con la cara de luz clara y fria (el calor lo pone el sol) y musgo."""
    rng = np.random.default_rng(semilla)
    pts = fibonacci(npts) * rng.uniform(0.8, 1.12, (npts, 1)) * np.array(escala) * 0.5
    piso = pts[:, 1].min() * 0.45
    bajos = pts[:, 1] < piso
    pts[bajos, 1] = piso + rng.uniform(0, 0.006, bajos.sum())
    pts[:, 1] -= pts[:, 1].min()
    base = mezclar(PAL["piedra"], PAL["piedra_osc"], 0.5)
    # iteracion 8: las rocas del ancla son malva calido (#a3786a al sol); con petroleo 0,6 salian gris azulado
    sombra, luz = mezclar(base, PAL["petroleo"], 0.3), mezclar(base, PAL["tierra1"], 0.3)
    enc = (mezclar(PAL["hierba_sol"], PAL["hierba_sombra"], 0.35), 0.8, 0.78) if musgo else None
    m = solido_facetado(nombre, pts, sombra, base, luz, rng, var=0.06, encima=enc)
    # hundida un 12 % en el suelo, como en el ancla
    alto = pts[:, 1].max()
    m.P = [p - np.array([0, 0.12 * alto, 0]) for p in m.P]
    return m


def en_hierba(x, z, margen=0.05):
    """Verdadero donde hay hierba: fuera del sendero, del arroyo y de la plaza."""
    ds, _ = dist_polilinea(x, z, SENDERO)
    ds2, _ = dist_polilinea(x, z, SENDERO_LEJOS)
    da, _ = dist_polilinea(x, z, ARROYO)
    return (np.minimum(ds, ds2) > ancho_sendero(z) / 2 + margen) & (da > 1.1) & (lado_baranda(x, z) < -0.25)


def hierba_corta(rng, matas=7000, area=((-9, 9), (-8, 6.5))):
    """Matas de briznas por toda la hierba (la textura de pasto del ancla): base oscura, punta dorada."""
    m = Malla("VEG-hierba_corta", material="Follaje")
    (x0, x1), (z0, z1) = area
    X = rng.uniform(x0, x1, matas * 2)
    Z = rng.uniform(z0, z1, matas * 2)
    ok = en_hierba(X, Z)
    X, Z = X[ok][:matas], Z[ok][:matas]
    Y = altura(X, Z)
    arriba = np.array([0.0, 1.0, 0.0])
    for x, y, z in zip(X, Y, Z):
        for _ in range(rng.integers(3, 6)):
            ang = rng.uniform(0, 2 * math.pi)
            d = np.array([math.cos(ang), 0, math.sin(ang)])
            lado = np.cross(d, arriba) * rng.uniform(0.022, 0.04)
            h = rng.uniform(0.06, 0.17)
            base = np.array([x, y - 0.015, z]) + d * rng.uniform(0, 0.06)
            punta = base + d * rng.uniform(0.03, 0.08) + np.array([0, h, 0])
            c0 = mezclar(PAL["hierba_sombra"], PAL["oscuro"], 0.3)
            c1 = mezclar(PAL["hierba_sol"], mezclar(PAL["hierba_sombra"], PAL["dorado"], 0.5),
                         rng.uniform(0, 0.35)) * rng.uniform(0.9, 1.08)
            m.tri(base - lado, base + lado, punta, c0, c0, c1, normales=[arriba] * 3)
    return m


def muro(nombre, a, b, rng, alto=0.95, grosor=0.32, base=PLAZA_Y - 0.08):
    """Muro de contencion de sillares (TER-12) entre a y b, del suelo de la plaza a ras del sendero."""
    m = Malla(nombre)
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0]])  # hacia la plaza
    largo = np.linalg.norm(b - a)
    k = 0.0
    fila = 0
    y = base
    while y < base + alto - 1e-6:
        h = min(0.32, base + alto - y)
        k = -0.25 * (fila % 2)  # sillares trabados
        while k < largo:
            l = rng.uniform(0.45, 0.75)
            k0, k1 = max(k, 0.0), min(k + l - 0.03, largo)
            if k1 > k0:
                p0 = a + d * k0
                p1 = a + d * k1
                # caja orientada: se arma en local y se gira
                tmp = Malla("tmp")
                col = mezclar(PAL["piedra_clara"], PAL["piedra"], rng.uniform(0.15, 0.5))
                caja(tmp, (0, y, -grosor / 2), (k1 - k0, y + h - 0.025, grosor / 2), col, sombra_t=0.4, rng=rng)
                ang = math.atan2(-d[1], d[0])
                m.anexar(tmp, R=np.array([[math.cos(ang), 0, math.sin(ang)], [0, 1, 0], [-math.sin(ang), 0, math.cos(ang)]]),
                         t=(p0[0] + n[0] * grosor / 2, 0, p0[1] + n[1] * grosor / 2))
            k += l
        y += h
        fila += 1
    return m


def piedras_sueltas(nombre, semilla, n=7, radio=0.45):
    """Grupo de piedras pequenas (TER-03)."""
    rng = np.random.default_rng(semilla)
    m = Malla(nombre)
    for k in range(n):
        esc = rng.uniform(0.07, 0.15) * np.array([1.2, 0.7, 1.0])
        r = roca_escena(nombre, semilla * 10 + k, tuple(esc * 2), npts=12, musgo=False)
        ang = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, radio)
        m.anexar(r, t=(math.cos(ang) * d, 0, math.sin(ang) * d))
    # iteracion 8: en el ancla las piedrecillas del sendero son beige claro, no gris azulado
    m.C = [mezclar(c, mezclar(PAL["tierra1"], PAL["crema"], 0.3), 0.55) for c in m.C]
    return m


def piedras_de_rio(nombre, semilla, n=9):
    """Cantos rodados (TER-05): mas redondos y lisos, gris azulado."""
    rng = np.random.default_rng(semilla)
    m = Malla(nombre)
    for k in range(n):
        esc = np.array([rng.uniform(0.18, 0.4), rng.uniform(0.08, 0.16), rng.uniform(0.15, 0.32)])
        pts = fibonacci(16) * rng.uniform(0.92, 1.05, (16, 1)) * esc
        pts[:, 1] -= pts[:, 1].min()
        # iteracion 9: los cantos del ancla son malva medio con musgo; con piedra_clara y crema salian casi blancos
        base = mezclar(PAL["piedra"], PAL["piedra_osc"], rng.uniform(0.2, 0.5))
        r = solido_facetado(nombre, pts, mezclar(base, PAL["petroleo"], 0.4), base, mezclar(base, PAL["tierra1"], 0.25), rng,
                            encima=(mezclar(PAL["hierba_sol"], PAL["hierba_sombra"], 0.4), 0.85, 0.8))
        ang = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0.1, 0.9)
        m.anexar(r, t=(math.cos(ang) * d, 0, math.sin(ang) * d * 0.6))
    return m


def guardar(nombre, *mallas):
    e = Escena()
    e.nodo(nombre, e.malla(*mallas, nombre=nombre))
    ruta = e.guardar(MODELOS / f"{nombre}.glb")
    return ruta, e.stats[nombre]


def colocar(lista, ident, glb, x, z, rot_deg=0.0, escala=1.0, y=None, **extra):
    """Apoya el recurso en el terreno salvo que se de y."""
    if y is None:
        y = float(altura(np.array(x), np.array(z)))
    lista.append({"id": ident, "glb": glb, "pos": [round(float(x), 3), round(float(y), 3), round(float(z), 3)],
                  "rot_y": round(float(rot_deg), 1), "escala": escala, **extra})


def main():
    rng = np.random.default_rng(2026)
    MODELOS.mkdir(parents=True, exist_ok=True)
    informe = {}
    informe["TER-suelo"] = guardar("TER-suelo", terreno(rng))[1]
    informe["TER-09_agua"] = guardar("TER-09_agua", agua())[1]
    informe["VEG-hierba_corta"] = guardar("VEG-hierba_corta", hierba_corta(rng))[1]
    informe["TER-13_mosaico"] = guardar("TER-13_mosaico", mosaico(np.random.default_rng(13)))[1]
    rocas = {
        "TER-01_a": roca_escena("TER-01_a", 7, (1.7, 1.1, 1.45), 34),
        "TER-01_b": roca_escena("TER-01_b", 19, (1.4, 0.95, 1.2), 30),
        "TER-02_a": roca_escena("TER-02_a", 3, (0.95, 0.65, 0.85), 24),
        "TER-02_b": roca_escena("TER-02_b", 31, (0.8, 0.6, 0.75), 22),
    }
    for nombre, m in rocas.items():
        informe[nombre] = guardar(nombre, m)[1]
    informe["TER-03"] = guardar("TER-03", piedras_sueltas("TER-03", 5))[1]
    informe["TER-05"] = guardar("TER-05", piedras_de_rio("TER-05", 8))[1]

    L = []
    # entorno base
    colocar(L, "TER-suelo", "modelos/TER-suelo.glb", 0, 0, y=0.0)
    colocar(L, "TER-09_agua", "modelos/TER-09_agua.glb", 0, 0, y=0.0)
    colocar(L, "VEG-hierba_corta", "modelos/VEG-hierba_corta.glb", 0, 0, y=0.0)
    colocar(L, "TER-13_mosaico", "modelos/TER-13_mosaico.glb", 0, 0, y=0.0)
    # rocas: pixel (u, v) de su base en el ancla
    for ident, glb, (u, v), r, s in [
        ("roca_iguana", "TER-01_a", (0.17, 0.60), 20, 1.0), ("roca_arbol", "TER-02_a", (0.36, 0.28), 60, 0.9),
        ("roca_centro", "TER-02_b", (0.53, 0.265), 10, 0.7), ("roca_frente", "TER-01_b", (0.555, 0.84), 200, 0.95),
        ("roca_frente2", "TER-02_a", (0.61, 0.97), 120, 0.9), ("roca_cascada", "TER-01_b", (0.91, 0.285), 75, 1.05),
        ("roca_orilla", "TER-02_b", (0.82, 0.245), 300, 0.9), ("roca_orilla2", "TER-01_a", (0.905, 0.48), 140, 0.9),
        ("roca_orilla3", "TER-02_b", (0.985, 0.38), 220, 0.9), ("roca_derecha", "TER-01_b", (0.965, 0.74), 30, 1.2),
        ("roca_lejos", "TER-02_a", (0.72, 0.06), 230, 0.9), ("roca_puente", "TER-02_b", (0.80, 0.03), 80, 0.8),
        ("roca_puente2", "TER-01_b", (0.975, 0.1), 15, 0.85), ("roca_plaza", "TER-02_a", (0.27, 0.78), 150, 0.75),
        ("roca_bajo_der", "TER-02_a", (0.91, 0.98), 40, 0.9),
        ("roca_rio1", "TER-02_b", (0.775, 0.29), 110, 0.6), ("roca_rio2", "TER-02_a", (0.725, 0.255), 250, 0.55),
        ("roca_rio3", "TER-02_b", (0.955, 0.06), 30, 0.75), ("roca_rio4", "TER-01_b", (0.66, 0.05), 160, 0.7),
        ("roca_lejos2", "TER-01_a", (0.05, -0.15), 90, 1.2), ("roca_lejos3", "TER-01_b", (1.15, 0.2), 200, 1.3),
        ("roca_lejos4", "TER-02_a", (-0.2, 0.9), 40, 1.1), ("roca_lejos5", "TER-02_b", (1.2, 0.9), 300, 1.2),
        ("roca_lejos6", "TER-01_a", (0.35, -0.3), 120, 1.0),
    ]:
        x, z = suelo(u, v)
        # las rocas del ancla miden 0,6 a 1 m: los modelos TER-01/02 (1,4 a 1,7 m) se reducen, salvo la de la iguana
        colocar(L, ident, f"modelos/{glb}.glb", x, z, r, s if ident == "roca_iguana" else s * 0.62)
    # grupos de piedrecillas a los lados del sendero y cantos rodados en el arroyo
    for k, (u, v) in enumerate([(0.38, 0.86), (0.515, 0.78), (0.465, 0.915), (0.56, 0.6), (0.52, 0.71),
                                (0.33, 0.96), (0.60, 0.36), (0.50, 0.45), (0.63, 0.27)]):
        x, z = suelo(u, v)
        colocar(L, f"piedras_{k}", "modelos/TER-03.glb", x, z, k * 47, 0.5)  # it. 10: mas chicas, como en el ancla
    for k, (u, v) in enumerate([(0.83, 0.215), (0.80, 0.30), (0.92, 0.36), (0.875, 0.03), (0.97, 0.43)]):
        x, z = suelo(u, v, -0.3)
        colocar(L, f"cantos_{k}", "modelos/TER-05.glb", x, z, k * 63, 1.0,
                y=float(nivel_agua(np.array(x), np.array(z))) - 0.2)

    # recursos de los agentes (si falta el archivo, la escena lo omite y lo avisa)
    # flamboyan: base del tronco en (0,20; 0,42) del ancla; copa en paraguas al 62 % del alto del modelo,
    # para que entre en el cuadro arriba a la izquierda como en el ancla (el flamboyan es de copa ancha y baja)
    ARBOL = suelo(0.20, 0.42)
    colocar(L, "VEG-02", "modelos/VEG-02.glb", ARBOL[0], ARBOL[1], 0, 1.0, escala_y=0.62)
    colocar(L, "VEG-02_lejos", "modelos/VEG-02.glb", 8.6, -7.5, 140, 0.9, escala_y=0.62)
    # petalos caidos en la hierba a la izquierda del sendero (flores rojas del ancla en u 0,25-0,4, v 0,25-0,7)
    PETALOS = suelo(0.30, 0.47)
    colocar(L, "VEG-02_petalos", "modelos/VEG-02_petalos.glb", PETALOS[0], PETALOS[1], 0, 0.7)
    eje = np.array(PUENTE["eje"])
    colocar(L, "TER-10", "modelos/TER-10.glb", PUENTE["pos"][0], PUENTE["pos"][1],
            math.degrees(math.atan2(-eje[1], eje[0])), 0.7, y=0.02)  # iteracion 10: el modelo (2,66 m) se veia 1,5 veces el del ancla
    # plaza baja: muros de contencion en sus dos bordes, baranda sobre el muro A y escalinata en el borde B
    dA = (BARANDA[1] - BARANDA[0]) / np.linalg.norm(BARANDA[1] - BARANDA[0])
    nA = np.array([-dA[1], dA[0]])
    dB = (BORDE_B[1] - BORDE_B[0]) / np.linalg.norm(BORDE_B[1] - BORDE_B[0])
    nB = np.array([-dB[1], dB[0]])
    inicio_A = BARANDA[1] - dA * 9.8
    rng_m = np.random.default_rng(12)
    # tramo del borde A ocupado por la escalinata (dos modulos TER-11 de 2,06 m centrados donde el ancla
    # pinta el mosaico): ahi no hay muro, la escalera baja directo desde la baranda
    s_esc = float((np.array(suelo(0.13, 0.86)) - BARANDA[1]) @ dA)
    s0, s1 = s_esc - 2.06, s_esc + 2.06
    muros = [("TER-12_muro_A", inicio_A, BARANDA[1] + dA * s0), ("TER-12_muro_B1", BORDE_B[0], BORDE_B[0] + dB * 0.2),
             ("TER-12_muro_B2", BORDE_B[0] + dB * 2.95, BORDE_B[1])]
    if s1 < -0.3:
        muros.append(("TER-12_muro_A2", BARANDA[1] + dA * s1, BARANDA[1]))
    for nombre, a, b in muros:
        informe[nombre] = guardar(nombre, muro(nombre, a, b, rng_m))[1]
        colocar(L, nombre, f"modelos/{nombre}.glb", 0, 0, y=0.0)
    ang_A = math.degrees(math.atan2(-dA[1], dA[0]))
    for k, s in enumerate([1.55, 4.65, 7.75]):  # distancia desde la esquina, hacia atras por el borde A
        p = BARANDA[1] - dA * s + nA * 0.16
        colocar(L, f"URB-09_{k}", "modelos/URB-09.glb", p[0], p[1], ang_A, 1.0, y=0.07)
    # escalinata con mosaico (TER-11) pegada a la baranda, donde el ancla la pinta (abajo a la izquierda, entre
    # los pilares): baja desde el borde A hacia la plaza; su fondo (z local -0,8) toca la cara del muro
    for k, ds in enumerate((-1.03, 1.03)):
        c_esc = BARANDA[1] + dA * (s_esc + ds) + nA * 0.8
        # la huella alta del modelo esta a 0,68 m: con y = -0,70 queda a ras del suelo de arriba
        colocar(L, f"TER-11_{k}", "modelos/TER-11.glb", c_esc[0], c_esc[1], math.degrees(math.atan2(nA[0], nA[1])),
                1.0, y=-0.70)
    ANTENA = suelo(0.77, 0.555)
    colocar(L, "COL-01_script", "modelos/COL-01_script.glb", ANTENA[0], ANTENA[1], 120, 1.0, variante="script")  # it. 10: boca arriba a la derecha
    colocar(L, "COL-01_tripo", "tripo/COL-01_tripo.glb", ANTENA[0], ANTENA[1], -75, 1.0, variante="tripo", altura=0.9)
    PANEL = suelo(0.835, 0.81)
    colocar(L, "COL-02", "modelos/COL-02.glb", PANEL[0], PANEL[1], 12, 1.0)
    x, z = suelo(0.845, 0.48, 1.0)
    colocar(L, "FX-01_antena", "modelos/FX-01.glb", x, z, 0, 1.0, y=1.0)
    x, z = suelo(0.85, 0.715, 0.6)
    colocar(L, "FX-01_panel", "modelos/FX-01.glb", x, z, 0, 1.0, y=0.6)

    # personajes y fauna (Tripo). Medidas: protagonista 1,05 m; gato al 50 % de su alto (ancla); iguana 1 m.
    # PER-01 v2 (lote 04c, desde la hoja de giro) mira a +X; 76,1 grados la deja de espaldas por el sendero, como el ancla
    PROTA = suelo(0.47, 0.635)
    # PER-01 v6 (2026-11-12): malla ajustada a las siluetas de la hoja, textura proyectada desde la hoja y bolso 3D
    # (83 % de parecido con su hoja, metrica v2); mira a +X como la v2
    colocar(L, "PER-01", "tripo/PER-01_v6.glb", PROTA[0], PROTA[1], 76.1, 1.0, altura=1.05)
    # el gato con rig (Rigify Cat, herramientas/blender/rig_gato.py) mira a +Z en glTF y camina en el sitio
    GATO = suelo(0.535, 0.625)
    colocar(L, "PER-09", "tripo/PER-09_rig.glb", GATO[0], GATO[1], 166.1, 1.0, altura=0.5, animacion="caminar")
    colocar(L, "FAU-01", "tripo/FAU-01.glb", *suelo(0.17, 0.58), 180.0, 1.0, altura=0.3, sobre="roca_iguana")

    # vegetacion baja: matas en los pixeles del ancla y relleno alrededor (fuera del sendero, el agua y la plaza)
    plantas = [("VEG-14_blanca", 0.355, 0.62), ("VEG-14_blanca", 0.32, 0.775), ("VEG-14_blanca", 0.62, 0.46),
               ("VEG-14_blanca", 0.90, 0.635), ("VEG-14_blanca", 0.70, 0.89), ("VEG-14_rosa", 0.63, 0.645),
               ("VEG-14_rosa", 0.65, 0.82), ("VEG-14_rosa", 0.97, 0.22), ("VEG-14_amarilla", 0.73, 0.96),
               ("VEG-14_amarilla", 0.975, 0.58), ("VEG-14_rosa", 0.91, 0.17), ("VEG-14_rosa", 0.995, 0.31),
               ("VEG-14_blanca", 0.72, 0.31)]  # iteracion 10: orilla del arroyo con flores, como el ancla
    for k, (ident, u, v) in enumerate(plantas):
        x, z = suelo(u, v)
        colocar(L, f"{ident}_{k}", f"modelos/VEG-14.glb", x, z, k * 37, 1.0, nodo=ident)
    rng2 = np.random.default_rng(7)
    puestos = 0
    while puestos < 260:  # iteracion 10: la hierba del ancla es mas densa (antes 170)
        x, z = rng2.uniform(-11, 11), rng2.uniform(-10, 7)
        ds, _ = dist_polilinea(np.array(x), np.array(z), SENDERO)
        ds2, _ = dist_polilinea(np.array(x), np.array(z), SENDERO_LEJOS)
        da, _ = dist_polilinea(np.array(x), np.array(z), ARROYO)
        if min(ds, ds2) < ancho_sendero(z) / 2 + 0.15 or da < 1.2 or lado_baranda(x, z) > -0.3:
            continue
        if math.hypot(x - ARBOL[0], z - ARBOL[1]) < 0.9:
            continue
        tam = rng2.choice(["VEG-13_p", "VEG-13_m", "VEG-13_g"], p=[0.45, 0.35, 0.2])
        colocar(L, f"hierba_{puestos}", "modelos/VEG-13.glb", x, z, rng2.uniform(0, 360), rng2.uniform(0.8, 1.25),
                nodo=tam, grupo="hierba")
        puestos += 1
    for k, (u, v, nodo_id) in enumerate([(0.03, 0.57, "heliconia"), (0.195, 0.70, "heliconia"), (0.04, 0.52, "anchas"),
                                         (0.29, 0.61, "anchas"), (0.04, 0.94, "anchas"), (0.08, 0.28, "helecho"),
                                         (0.82, 0.03, "helecho"), (0.95, 0.91, "anchas"), (0.96, 0.54, "helecho"),
                                         (0.83, 0.17, "helecho"), (0.94, 0.25, "anchas"), (0.25, 0.53, "heliconia"),
                                         (0.89, 0.04, "helecho"), (0.74, 0.31, "anchas"), (0.99, 0.31, "helecho"),
                                         (0.86, 0.41, "anchas"), (0.70, 0.03, "helecho")]):
        glb = {"heliconia": "VEG-07", "anchas": "VEG-10", "helecho": "VEG-12"}[nodo_id]  # IDs del agente de plantas
        x, z = suelo(u, v)
        colocar(L, f"planta_{k}", f"modelos/{glb}.glb", x, z, k * 53, 1.0)

    # sombra moteada del flamboyan: en el ancla cubre de u 0,05 a 0,75 y de v 0,2 a 0,55
    # iteracion 13: la protagonista (v 0,64) queda al sol con su sombra marcada, como en el ancla
    c = suelo(0.38, 0.32)
    rx = abs(suelo(0.72, 0.32)[0] - suelo(0.04, 0.32)[0]) / 2
    rz = abs(suelo(0.38, 0.15)[1] - suelo(0.38, 0.50)[1]) / 2
    ambiente = {"moteado": {"centro": [round(c[0], 3), round(c[1], 3)], "radios": [round(rx, 3), round(rz, 3)],
                            "fuerza": 1.0, "sombra": 0.45},
                "pinceladas": 0.7}  # iteracion 12: textura pintada 2D-HD por shader
    # camara medida contra el ancla: mas baja y con mas perspectiva que los 60 grados del encargo
    (ESCENA / "layout.json").write_text(json.dumps({"camara": CAMARA, "ambiente": ambiente, "recursos": L},
                                                   indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    print(json.dumps({"triangulos": informe, "recursos_en_layout": len(L)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
