"""Zona jugable «sendero»: ampliacion minima de la escena aprobada (D-015) y su layout.

La escena aprobada (pruebas/escena_exploracion, escrita por escena_v1.py) se ve desde una camara fija. En el
juego la camara sigue a la protagonista y asoman los bordes del decorado. Este generador NO toca el centro
aprobado: vuelve a generar el suelo y la hierba con las mismas semillas (se comprueba que salen identicos a
los aprobados) y solo agrega, fuera del cuadro del ancla, lo que falta con LOS MISMOS recursos:

  TER-suelo            el mismo suelo, con el sendero prolongado hacia la plaza (sur) y el arroyo hacia el este
  VEG-hierba_corta     la misma hierba, sin las briznas que caerian sobre esos dos tramos nuevos
  VEG-hierba_corta_norte / _este / _oeste   hierba de la misma densidad en la franja que ve la camara de juego
  TER-09_agua_este     cinta de agua del tramo nuevo del arroyo
  TER-13_mosaico_ext   el mosaico de la plaza baja, continuado con el mismo dibujo
  TER-12_muro_B3       el tramo de muro que faltaba en el borde B (quedaba fuera del cuadro)
  COL-01_apuntada      la antena COL-01 ya reparada: el mismo modelo con el plato girado 30 grados hacia el cielo
  ARQ-09               farol (solo de noche; estado provisional)

Tambien escribe juego/zonas/sendero/layout.json: copia del layout aprobado con las rutas del juego, los
recursos nuevos y los trazados que usa sendero.gd para las colisiones (orilla del arroyo, puente, barandas).

Uso:  python -I herramientas/mallas/sendero_ampliacion.py
"""
import json
import math
import struct
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import escena_v1 as e  # noqa: E402
import recolectables_col as rc  # noqa: E402
from nucleo import PAL, Escena, Malla, caja, mezclar, rot_eje, rot_y, tubo  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "juego" / "modelos" / "sendero"
ENTORNO = RAIZ / "juego" / "modelos" / "entorno"
ZONA = RAIZ / "juego" / "zonas" / "sendero"
APROBADO = RAIZ / "pruebas" / "escena_exploracion" / "layout.json"

SENDERO_0, ARROYO_0 = e.SENDERO.copy(), e.ARROYO.copy()
# tramos nuevos (fuera del cuadro del ancla, que llega a z = 1,49 y a x = 5,5 en la fila del arroyo)
SUR = np.array([(0.40, 10.2), (0.30, 7.0), (0.10, 5.2), (-0.15, 3.9)])       # hacia la plaza: se antepone al sendero
ESTE = np.array([(10.8, -1.08), (12.9, -0.50), (16.2, 0.25)])                # aguas abajo: se agrega al arroyo
SENDERO_1 = np.concatenate([SUR, SENDERO_0])
ARROYO_1 = np.concatenate([ARROYO_0, ESTE])
SUR_TRAMO = np.concatenate([SUR, SENDERO_0[:1]])
ESTE_TRAMO = np.concatenate([ARROYO_0[-1:], ESTE])

# Lo que ve la camara de juego (encuadre 0,19; foco limitado a LIMITES): ver sendero_visibilidad.py y la nota
# de evidencia. La copa del flamboyan (2 a 3,4 m de alto) queda entre la camara y el suelo: si el foco sube al
# norte de z = -1, tapa el sendero lejano. Por eso la camara no pasa de z = -1 y la salida al Mirador esta donde
# el sendero se pierde bajo la copa (arriba al centro del ancla), no mas alla.
LIMITES = {"x": [-1.6, 3.2], "z": [-1.0, 2.9]}
CERCO = {"x": [-5.6, 7.2], "z": [-5.6, 5.0]}
UMBRAL_CIUDAD = (-0.10, 4.10)
UMBRAL_MIRADOR = (1.40, -4.40)
ENTRADA_CASA = (-0.15, 2.55)
ENTRADA_MIRADOR = (1.45, -2.95)
FAROLES = [(0.95, 3.25), (-0.95, -1.30), (2.30, -2.70), (0.85, 1.75)]
# muros invisibles: nadie camina por lo que la copa tapa (al norte del tronco y al oeste del sendero lejano)
MUROS = [[0.35, -5.6, 0.35, -3.4], [0.35, -3.4, 0.10, -2.8], [0.10, -2.8, -1.05, -2.45], [-4.4, -2.3, -5.7, -2.3]]
RUTA_NORTE = [(0.98, -2.11), (1.35, -2.92), (1.61, -3.33), (1.52, -3.90)]

PUENTE_ESCALA, PUENTE_MEDIO, PUENTE_TABLERO = 0.7, 1.33, 0.24   # TER-10: medio largo y alto del tablero del modelo


def usar(sendero, arroyo):
    e.SENDERO, e.ARROYO = sendero, arroyo


def guardar(ruta, nombre, *mallas):
    esc = Escena()
    esc.nodo(nombre, esc.malla(*mallas, nombre=nombre))
    esc.guardar(ruta)
    return esc.stats[nombre]


def dist(x, z, pts):
    return e.dist_polilinea(np.asarray(x, float), np.asarray(z, float), pts)[0]


def en_cuadro_ancla(x, z, margen=0.0):
    """Verdadero si el punto del suelo cae dentro del cuadro del ancla aprobada (encuadre 21)."""
    u, v = e._CAM.a_pantalla((float(x), 0.0, float(z)))
    return -margen <= u <= 1 + margen and -margen <= v <= 1 + margen


def en_tramo_nuevo(x, z, margen_sendero=0.05, margen_arroyo=1.1):
    """Sobre el sendero prolongado o el arroyo prolongado (solo los tramos nuevos)."""
    x, z = np.asarray(x, float), np.asarray(z, float)
    return (dist(x, z, SUR_TRAMO) < e.ancho_sendero(z) / 2 + margen_sendero) | (dist(x, z, ESTE_TRAMO) < margen_arroyo)


# ---------------------------------------------------------------- suelo y hierba

def suelo_y_hierba(informe):
    usar(SENDERO_0, ARROYO_0)
    rng = np.random.default_rng(2026)
    suelo_a = e.terreno(rng)
    hierba_a = e.hierba_corta(rng)
    tmp = SALIDA / "_tmp.glb"
    guardar(tmp, "TER-suelo", suelo_a)
    informe["suelo_identico_al_aprobado"] = tmp.read_bytes() == (ENTORNO / "TER-suelo.glb").read_bytes()
    guardar(tmp, "VEG-hierba_corta", hierba_a)
    informe["hierba_identica_a_la_aprobada"] = tmp.read_bytes() == (ENTORNO / "VEG-hierba_corta.glb").read_bytes()
    tmp.unlink()

    usar(SENDERO_1, ARROYO_1)
    suelo_b = e.terreno(np.random.default_rng(2026))
    pa, pb = np.array(suelo_a.P), np.array(suelo_b.P)
    ca, cb = np.array(suelo_a.C), np.array(suelo_b.C)
    cambia = (np.abs(pa - pb).max((1, 2)) > 1e-9) | (np.abs(ca - cb).max((1, 2)) > 1e-9)
    centros = pb[cambia].mean(1)
    dentro = [en_cuadro_ancla(c[0], c[2]) for c in centros]
    informe["suelo"] = {"triangulos": guardar(SALIDA / "TER-suelo.glb", "TER-suelo", suelo_b),
                        "triangulos_que_cambian": int(cambia.sum()),
                        "cambian_dentro_del_cuadro_del_ancla": int(sum(dentro)),
                        "caja_de_los_cambios_xz": [np.round(centros[:, [0, 2]].min(0), 2).tolist(),
                                                   np.round(centros[:, [0, 2]].max(0), 2).tolist()]}
    # la hierba aprobada, sin las briznas que quedarian sobre los tramos nuevos
    filtrada = Malla("VEG-hierba_corta", material="Follaje")
    quitadas, quitadas_en_cuadro = 0, 0
    for P, C, N in zip(hierba_a.P, hierba_a.C, hierba_a.N):
        base = (P[0] + P[1]) / 2
        if bool(en_tramo_nuevo(base[0], base[2])):
            quitadas += 1
            quitadas_en_cuadro += en_cuadro_ancla(base[0], base[2])
            continue
        filtrada.P.append(P)
        filtrada.C.append(C)
        filtrada.N.append(N)
    informe["hierba"] = {"triangulos": guardar(SALIDA / "VEG-hierba_corta.glb", "VEG-hierba_corta", filtrada),
                         "briznas_quitadas": quitadas, "quitadas_dentro_del_cuadro_del_ancla": int(quitadas_en_cuadro)}
    # densidad de la hierba aprobada (matas por m2 de hierba)
    rng_d = np.random.default_rng(1)
    X, Z = rng_d.uniform(-9, 9, 40000), rng_d.uniform(-8, 6.5, 40000)
    usar(SENDERO_0, ARROYO_0)
    f0 = float(e.en_hierba(X, Z).mean())
    usar(SENDERO_1, ARROYO_1)
    densidad = 7000 / (18 * 14.5 * f0)
    informe["hierba"]["densidad_matas_m2"] = round(densidad, 1)
    # la franja norte solo se ve al alejar la camara (el foco no pasa de z = -1 y a 0,19 el cuadro llega a
    # z = -7,8): se deja angosta y sin adornos, porque en la HD 620 cada triangulo fuera de cuadro tambien cuesta
    franjas = {"norte": ((-9.9, 11.5), (-10.6, -8.05)), "este": ((9.05, 11.5), (-8.05, 1.2)),
               "oeste": ((-9.9, -9.05), (-8.05, -3.4))}
    for k, (nombre, area) in enumerate(franjas.items()):
        (x0, x1), (z0, z1) = area
        X, Z = rng_d.uniform(x0, x1, 20000), rng_d.uniform(z0, z1, 20000)
        f = float(e.en_hierba(X, Z).mean())
        matas = int(densidad * (x1 - x0) * (z1 - z0) * f)
        m = e.hierba_corta(np.random.default_rng(4100 + k), matas=matas, area=area)
        m.nombre = f"VEG-hierba_corta_{nombre}"
        informe[m.nombre] = {"triangulos": guardar(SALIDA / f"{m.nombre}.glb", m.nombre, m), "matas": matas}
    return franjas


def agua_este():
    """Cinta de agua del tramo nuevo, con el mismo ancho y la misma mascara de orilla que agua()."""
    m = Malla("TER-09_agua_este", material="Agua")
    y, medio, orilla = e.NIVELES[2], 1.05, np.full(3, 0.35)
    muestras = []
    for k in range(len(ESTE_TRAMO) - 1):
        for t in np.linspace(0, 1, 7, endpoint=False):
            muestras.append(ESTE_TRAMO[k] * (1 - t) + ESTE_TRAMO[k + 1] * t)
    muestras.append(ESTE_TRAMO[-1])
    # arranca 0,4 m antes del final de la cinta aprobada para que no quede rendija en el empalme
    d0 = (ARROYO_0[-1] - ARROYO_0[-2]) / np.linalg.norm(ARROYO_0[-1] - ARROYO_0[-2])
    muestras = [ARROYO_0[-1] - d0 * 0.4] + muestras
    for p, q in zip(muestras[:-1], muestras[1:]):
        d = q - p
        n = np.array([-d[1], d[0]]) / np.linalg.norm(d)
        a = (p[0] + n[0] * medio, y - 0.002, p[1] + n[1] * medio)
        b = (p[0] - n[0] * medio, y - 0.002, p[1] - n[1] * medio)
        c = (q[0] - n[0] * medio, y - 0.002, q[1] - n[1] * medio)
        f = (q[0] + n[0] * medio, y - 0.002, q[1] + n[1] * medio)
        m.quad(a, f, c, b, orilla, orilla, orilla, orilla)
    return m


def mosaico_ext(lado=0.14, junta=0.014):
    """El mosaico de la plaza baja continuado con la misma onda, fuera del cuadrado de 6 x 6 m aprobado."""
    rng = np.random.default_rng(131)
    m = Malla("TER-13_mosaico_ext")
    centro = np.array(e.suelo(0.06, 0.93, e.PLAZA_Y))
    azul = mezclar(PAL["petroleo"], PAL["cian_medio"], 0.45)
    turquesa = mezclar(PAL["cian_medio"], PAL["brillo"], 0.25)
    naranja = mezclar(PAL["sol"], PAL["coral"], 0.35)
    crema = mezclar(PAL["crema"], PAL["brillo"], 0.2)
    original = np.arange(-3.0, 3.0, lado)
    pasos_i = np.arange(-50, 60) * lado - 3.0
    for i in pasos_i:
        for j in pasos_i:
            if original[0] - 1e-6 <= i <= original[-1] + 1e-6 and original[0] - 1e-6 <= j <= original[-1] + 1e-6:
                continue
            x, z = centro[0] + i, centro[1] + j
            if x < -9.2 or z > 5.5 or z < -3.2 or x > 0.0:
                continue
            if e.lado_baranda(np.array(x), np.array(z)) < 0.12:
                continue
            onda = math.sin(0.95 * x + 0.55 * z + 0.9 * math.sin(0.6 * z - 0.3 * x))
            col = azul if onda > 0.55 else crema if onda > 0.15 else naranja if onda > -0.3 else crema if onda > -0.6 else turquesa
            col = col * rng.uniform(0.93, 1.05)
            y = e.PLAZA_Y + 0.006
            a = lado / 2 - junta / 2
            m.quad((x - a, y, z + a), (x + a, y, z + a), (x + a, y, z - a), (x - a, y, z - a), col)
    return m


# ---------------------------------------------------------------- antena reparada y farol

def antena_apuntada(informe):
    mallas, info = rc.antena()
    todo = np.concatenate([np.array(m.P).reshape(-1, 3) for m in mallas if len(m)])
    lo, hi = todo.min(0), todo.max(0)
    mover = np.array([(lo[0] + hi[0]) / 2, lo[1], (lo[2] + hi[2]) / 2])
    giro = rc.GIRO_LAYOUT["COL-01_script"]
    R = rot_y(math.radians(-giro))
    # comprobacion: con el giro del generador sale la caja del modelo aprobado
    caja_gen = np.round(np.stack([((todo - mover) @ R.T).min(0), ((todo - mover) @ R.T).max(0)]), 2).tolist()
    informe["COL-01_caja_regenerada"] = caja_gen
    # misma disposicion que antena(): pivote de elevacion y eje del plato
    arriba = np.array([0.0, 1.0, 0.0])
    elev = math.radians(40.0)
    rumbo = rc.unit([-1.0, 0.0, -0.15])
    a = rc.unit(rumbo * math.cos(elev) + arriba * math.sin(elev))
    radio, hondo, grosor = 0.55, 0.17, 0.03
    pivote = np.array([0.0, 0.32, 0.0])
    a_h = rc.unit([a[0], 0.0, a[2]])
    cubo = pivote + a_h * 0.10 + arriba * 0.05
    vertice = cubo + a * (0.08 + grosor)
    ex = rc.unit(-arriba + a * np.dot(arriba, a))
    ez = np.cross(ex, a)
    Rd = np.stack([ex, a, ez], axis=1)
    t0 = math.radians(25)
    g = 2 * hondo * 0.86 * radio / radio ** 2
    normal = rc.unit([-g * math.cos(t0), 1.0, -g * math.sin(t0)])
    alto_p = np.array([0.86 * radio * math.cos(t0), hondo * 0.74, 0.86 * radio * math.sin(t0)])
    ap = Rd @ (alto_p - normal * (grosor + 0.012)) + vertice        # donde el puntal caido toca el borde
    pie = np.array([ap[0] - 0.24, 0.014, ap[2] + 0.12])

    def cerca_del_puntal(p, margen):
        ab = pie - ap
        t = np.clip(((p - ap) @ ab) / (ab @ ab), 0, 1)
        return np.linalg.norm(p - (ap + np.outer(t, ab)), axis=1).max() < margen

    giro_plato = rot_eje(np.cross(a, arriba), math.radians(30.0))     # el eje sube de 40 a 70 grados
    quitados = 0
    for m in mallas:
        P2, C2, N2 = [], [], []
        for P, C, N in zip(m.P, m.C, m.N):
            if cerca_del_puntal(P, 0.035 if m.material != "Follaje" else 0.10) and P[:, 1].min() < ap[1] + 0.05:
                quitados += 1          # el puntal que sostenia el plato caido (y su brote) ya no hace falta
                continue
            if ((P.mean(0) - pivote) @ a) > 0.02:                      # plato, alimentador y sus tirantes
                P = (P - pivote) @ giro_plato.T + pivote
                N = None if N is None else N @ giro_plato.T
            P2.append((P - mover) @ R.T)
            C2.append(C)
            N2.append(None if N is None else N @ R.T)
        m.P, m.C, m.N = P2, C2, N2
    informe["COL-01_apuntada"] = {"triangulos": guardar(SALIDA / "COL-01_apuntada.glb", "COL-01_antena", *mallas),
                                  "triangulos_del_puntal_quitados": quitados,
                                  "elevacion_del_eje_grados": 70}


def farol(informe):
    """ARQ-09, farol clasico (hoja HR_ARQ): hierro oscuro de la paleta, nunca negro, y vidrio crema."""
    rng = np.random.default_rng(909)
    m = Malla("ARQ-09_farol")
    hierro = mezclar(PAL["piedra_osc"], PAL["oscuro"], 0.45)
    claro = mezclar(PAL["piedra_osc"], PAL["petroleo"], 0.5)
    tubo(m, [(0, 0, 0), (0, 0.10, 0), (0, 0.24, 0)], [0.13, 0.12, 0.07], 6, hierro, claro, rng, ruido=0.04)
    tubo(m, [(0, 0.24, 0), (0, 1.0, 0), (0, 1.72, 0)], [0.045, 0.038, 0.034], 6, hierro, claro, rng, ruido=0.04, tapa=False)
    tubo(m, [(0, 1.72, 0), (0, 1.76, 0), (0, 1.80, 0)], [0.07, 0.085, 0.06], 6, hierro, claro, rng, ruido=0.03)
    # linterna: cuatro vidrios en tronco de piramide y sombrero
    vidrio_bajo, vidrio_alto = mezclar(PAL["sol"], PAL["crema"], 0.35), mezclar(PAL["crema"], PAL["brillo"], 0.35)
    r0, r1, y0, y1 = 0.075, 0.125, 1.80, 2.08
    esq = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    for k in range(4):
        (ax, az), (bx, bz) = esq[k], esq[(k + 1) % 4]
        m.quad((bx * r0, y0, bz * r0), (ax * r0, y0, az * r0), (ax * r1, y1, az * r1), (bx * r1, y1, bz * r1),
               vidrio_bajo, vidrio_bajo, vidrio_alto, vidrio_alto)
        tubo(m, [(ax * r0, y0, az * r0), (ax * r1, y1, az * r1)], [0.011, 0.011], 4, hierro, claro, rng, ruido=0.0, tapa=False)
        r2 = r1 + 0.03
        m.tri((bx * r2, y1, bz * r2), (ax * r2, y1, az * r2), (0, y1 + 0.13, 0), hierro, hierro, claro)
    tubo(m, [(0, y1 + 0.12, 0), (0, y1 + 0.19, 0)], [0.02, 0.008], 4, hierro, claro, rng, ruido=0.0)
    informe["ARQ-09"] = {"triangulos": guardar(SALIDA / "ARQ-09.glb", "ARQ-09_farol", m)}


# ---------------------------------------------------------------- colisiones que salen de los trazados

def leer_glb(ruta, nodo):
    b = Path(ruta).read_bytes()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    binario = b[20 + n + 8:]
    for nd in j["nodes"]:
        if nd.get("name") == nodo and "mesh" in nd:
            partes = []
            for pr in j["meshes"][nd["mesh"]]["primitives"]:
                a = j["accessors"][pr["attributes"]["POSITION"]]
                bv = j["bufferViews"][a["bufferView"]]
                partes.append(np.frombuffer(binario, dtype="<f4", count=a["count"] * 3,
                                            offset=bv.get("byteOffset", 0) + a.get("byteOffset", 0)).reshape(-1, 3))
            return np.concatenate(partes)
    return np.zeros((0, 3))


def huella_tronco(r):
    """Celdas de 0,3 m que el tronco y las ramas bajas del flamboyan ocupan a la altura del cuerpo."""
    V = leer_glb(ENTORNO / "VEG-02.glb", "VEG-02_tronco").astype(float)
    V = V * np.array([r["escala"], r["escala"] * r.get("escala_y", 1.0), r["escala"]])
    V = V @ rot_y(math.radians(r["rot_y"])).T + np.array(r["pos"])
    cuerpo = V[(V[:, 1] > 0.12) & (V[:, 1] < 1.0)]
    celdas = sorted({(round(float(x) / 0.3), round(float(z) / 0.3)) for x, _, z in cuerpo})
    return [[round(i * 0.3, 2), round(k * 0.3, 2)] for i, k in celdas]


def puente_mundo():
    pos, eje = np.array(e.PUENTE["pos"]), np.array(e.PUENTE["eje"])
    medio = PUENTE_MEDIO * PUENTE_ESCALA
    return pos - eje * medio, pos + eje * medio, eje


def orilla_jugable(separacion=1.0, paso=0.2):
    """Muro invisible por la orilla de este lado del arroyo, con el hueco del puente.
    Devuelve tramos [x0, z0, x1, z1]."""
    pts = ARROYO_1
    cadena = []
    for k in range(len(pts) - 1):
        p, q = pts[k], pts[k + 1]
        d = (q - p) / np.linalg.norm(q - p)
        n = np.array([-d[1], d[0]])            # el lado del sendero (noroeste del tramo alto, sur del tramo bajo)
        if k > 0:
            # esquina convexa: arco entre la normal del tramo anterior y la de este
            d0 = (p - pts[k - 1]) / np.linalg.norm(p - pts[k - 1])
            n0 = np.array([-d0[1], d0[0]])
            a0, a1 = math.atan2(n0[1], n0[0]), math.atan2(n[1], n[0])
            da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
            for t in np.linspace(0, 1, max(2, int(abs(da) / 0.2) + 1)):
                ang = a0 + da * t
                cadena.append(p + separacion * np.array([math.cos(ang), math.sin(ang)]))
        largo = float(np.linalg.norm(q - p))
        for s in np.arange(0, largo + 1e-6, paso):
            cadena.append(p + d * s + n * separacion)
    cadena = np.array(cadena)
    lejos = dist(cadena[:, 0], cadena[:, 1], pts) >= separacion - 0.03
    zona = (cadena[:, 0] > -1) & (cadena[:, 0] < 9.5) & (cadena[:, 1] > -11.5) & (cadena[:, 1] < 3.5)
    ini, fin, eje = puente_mundo()
    lat = np.array([-eje[1], eje[0]])
    a_lo_largo = (cadena - ini) @ eje
    de_lado = (cadena - ini) @ lat
    largo_p = float(np.linalg.norm(fin - ini))
    en_puente = (np.abs(de_lado) < 0.72) & (a_lo_largo > -0.6) & (a_lo_largo < largo_p + 0.4)
    medio_ancho = 0.52
    tramos = []
    previo, previo_ok = None, False
    for p, ok_lejos, ok_zona, puente, s, l in zip(cadena, lejos, zona, en_puente, a_lo_largo, de_lado):
        if not (ok_lejos and ok_zona):
            continue
        ok = not puente
        if previo is not None and np.linalg.norm(p - previo["p"]) < 0.9:
            if ok and previo_ok:
                tramos.append([*previo["p"], *p])
            elif ok != previo_ok:
                # corte del puente: el extremo libre se une a la baranda de ese lado
                libre = p if ok else previo["p"]
                s_l, l_l = (s, l) if ok else (previo["s"], previo["l"])
                ancla = ini + eje * float(np.clip(s_l, 0.0, largo_p)) + lat * math.copysign(medio_ancho, l_l)
                tramos.append([*libre, *ancla])
        previo, previo_ok = {"p": p, "s": s, "l": l}, ok
    # barandas del puente y su fondo
    # (arrancan 0,25 m dentro del tablero: dejan libres los 0,85 m que pide el umbral del Mirador)
    for sg in (-1, 1):
        tramos.append([*(ini + lat * sg * medio_ancho + eje * 0.25), *(fin + lat * sg * medio_ancho)])
    tramos.append([*(fin + lat * medio_ancho), *(fin - lat * medio_ancho)])
    # une tramos casi alineados para no crear cientos de cuerpos
    unidos = []
    for t in tramos:
        t = [float(v) for v in t]
        if unidos:
            u = unidos[-1]
            d1 = np.array([u[2] - u[0], u[3] - u[1]])
            d2 = np.array([t[2] - t[0], t[3] - t[1]])
            pegados = math.hypot(u[2] - t[0], u[3] - t[1]) < 1e-6
            if pegados and np.linalg.norm(d1) > 0 and np.linalg.norm(d2) > 0:
                cos = float(d1 @ d2 / (np.linalg.norm(d1) * np.linalg.norm(d2)))
                if cos > 0.9995 and np.linalg.norm(d1) < 3.0:
                    u[2], u[3] = t[2], t[3]
                    continue
        unidos.append(t)
    return [[round(v, 3) for v in t] for t in unidos], {"inicio": ini, "fin": fin, "eje": eje, "medio_ancho": medio_ancho}


# ---------------------------------------------------------------- layout

RUTAS = {"tripo/PER-01_v6.glb": "personajes/PER-01.glb", "tripo/PER-09_rig.glb": "personajes/PER-09_rig.glb",
         "tripo/FAU-01.glb": "personajes/FAU-01.glb", "tripo/COL-01_tripo.glb": "personajes/COL-01_tripo.glb"}
DE_LA_ZONA = {"TER-suelo", "VEG-hierba_corta"}
SUELTOS = ("FX-01", "COL-02", "COL-01", "FAU-01", "TER-10")


def libre_para_adorno(x, z, margen_sendero=0.75):
    """Sitio valido para una planta o una roca nueva: en la hierba, lejos de umbrales, entradas y faroles."""
    if not bool(e.en_hierba(np.array(x), np.array(z), margen_sendero)):
        return False
    if float(dist(x, z, ARROYO_1)) < 1.7:
        return False
    for px, pz in (UMBRAL_CIUDAD, UMBRAL_MIRADOR, ENTRADA_CASA, ENTRADA_MIRADOR, *FAROLES):
        if math.hypot(x - px, z - pz) < 1.7:
            return False
    return True


def layout(informe, franjas):
    usar(SENDERO_1, ARROYO_1)
    aprobado = json.loads(APROBADO.read_text(encoding="utf-8"))
    L = []
    quitados = []
    for r in aprobado["recursos"]:
        r = dict(r)
        glb = r["glb"]
        if glb in RUTAS:
            r["glb"] = RUTAS[glb]
        elif r["id"] in DE_LA_ZONA:
            r["glb"] = f"sendero/{r['id']}.glb"
        else:
            r["glb"] = glb.replace("modelos/", "entorno/")
        if r["id"].startswith(SUELTOS):
            r["suelto"] = True
        x, z = r["pos"][0], r["pos"][2]
        if r.get("grupo") == "hierba":
            # mechones que quedarian sobre los tramos nuevos o dentro del claro del umbral de la plaza (fuera del
            # cuadro del ancla). El umbral del Mirador esta dentro del cuadro aprobado: ahi no se quita nada.
            if bool(en_tramo_nuevo(x, z, 0.15, 1.2)) or math.hypot(x - UMBRAL_CIUDAD[0], z - UMBRAL_CIUDAD[1]) < 1.0:
                quitados.append({"id": r["id"], "en_cuadro_del_ancla": bool(en_cuadro_ancla(x, z))})
                continue
        L.append(r)
    informe["mechones_quitados"] = quitados

    def poner(ident, glb, x, z, rot=0.0, escala=1.0, y=None, **extra):
        e.colocar(L, ident, glb, x, z, rot, escala, y, **extra)

    # piezas nuevas de la zona
    for nombre in ["VEG-hierba_corta_norte", "VEG-hierba_corta_este", "VEG-hierba_corta_oeste", "TER-09_agua_este",
                   "TER-13_mosaico_ext", "TER-12_muro_B3"]:
        poner(nombre, f"sendero/{nombre}.glb", 0, 0, y=0.0)
    # baranda del borde B (URB-09, la misma del borde A): su primer pilar coincide con el pilar de la esquina
    dB = (e.BORDE_B[1] - e.BORDE_B[0]) / np.linalg.norm(e.BORDE_B[1] - e.BORDE_B[0])
    nB = np.array([-dB[1], dB[0]])
    ang_B = math.degrees(math.atan2(-dB[1], dB[0]))
    for k, s in enumerate([1.53 + 0.149, 4.59 + 0.149]):
        p = e.BORDE_B[0] + dB * s + nB * 0.062
        poner(f"URB-09_B{k}", "entorno/URB-09.glb", p[0], p[1], ang_B, 1.0, y=0.074)
    # mechones VEG-13 en la franja norte, con la densidad del layout aprobado
    rng = np.random.default_rng(71)
    n_aprobados = sum(1 for r in aprobado["recursos"] if r.get("grupo") == "hierba")
    X, Z = rng.uniform(-11, 11, 20000), rng.uniform(-10, 7, 20000)
    usar(SENDERO_0, ARROYO_0)
    validos = [1 for x, z in zip(X[:4000], Z[:4000]) if bool(e.en_hierba(np.array(x), np.array(z), 0.15))]
    usar(SENDERO_1, ARROYO_1)
    dens = n_aprobados / (22 * 17 * len(validos) / 4000)
    (x0, x1), (z0, z1) = franjas["norte"]
    meta, puestos = 0, 0      # sin mechones en la franja norte (no entra en cuadro; ver LIMITES)
    while puestos < meta:
        x, z = rng.uniform(x0, x1), rng.uniform(z0, -10.0)
        if not bool(e.en_hierba(np.array(x), np.array(z), 0.15)) or float(dist(x, z, ARROYO_1)) < 1.2:
            continue
        tam = rng.choice(["VEG-13_p", "VEG-13_m", "VEG-13_g"], p=[0.45, 0.35, 0.2])
        poner(f"hierba_n{puestos}", "entorno/VEG-13.glb", x, z, rng.uniform(0, 360), rng.uniform(0.8, 1.25),
              nodo=str(tam), grupo="hierba")
        puestos += 1
    informe["mechones_nuevos"] = puestos
    # plantas, flores y rocas de las mismas familias en las tres franjas nuevas (nada dentro del cuadro del ancla)
    plantas = {"heliconia": "VEG-07", "anchas": "VEG-10", "helecho": "VEG-12"}
    flores = ["VEG-14_blanca", "VEG-14_rosa", "VEG-14_amarilla"]
    rocas = [("TER-01_a", 0.62), ("TER-01_b", 0.6), ("TER-02_a", 0.58), ("TER-02_b", 0.56)]
    zonas = [("s", (0.9, 7.6), (2.9, 5.4), 5, 6, 2),
             ("e", (7.2, 11.2), (-0.9, 1.9), 4, 4, 2), ("o", (-9.6, -5.2), (-7.5, -3.2), 4, 3, 1)]
    cuenta = {"plantas": 0, "flores": 0, "rocas": 0}
    ocupados = []
    for clave, (x0, x1), (z0, z1), n_pl, n_fl, n_ro in zonas:
        for tipo, total in (("rocas", n_ro), ("plantas", n_pl), ("flores", n_fl)):
            puestos, intentos = 0, 0
            while puestos < total and intentos < 4000:
                intentos += 1
                x, z = rng.uniform(x0, x1), rng.uniform(z0, z1)
                if en_cuadro_ancla(x, z, 0.06) or not libre_para_adorno(x, z, 0.75 if tipo != "flores" else 0.25):
                    continue
                if any(math.hypot(x - ox, z - oz) < 0.9 for ox, oz in ocupados):
                    continue
                ocupados.append((x, z))
                if tipo == "rocas":
                    glb, esc = rocas[int(rng.integers(0, 4))]
                    poner(f"roca_{clave}{puestos}", f"entorno/{glb}.glb", x, z, rng.uniform(0, 360), round(esc * rng.uniform(0.85, 1.25), 3))
                elif tipo == "plantas":
                    nombre = list(plantas)[int(rng.integers(0, 3))]
                    poner(f"planta_{clave}{puestos}", f"entorno/{plantas[nombre]}.glb", x, z, rng.uniform(0, 360), 1.0)
                else:
                    nodo = flores[int(rng.integers(0, 3))]
                    poner(f"{nodo}_{clave}{puestos}", "entorno/VEG-14.glb", x, z, rng.uniform(0, 360), 1.0, nodo=nodo)
                puestos += 1
                cuenta[tipo] += 1
    informe["adornos_nuevos"] = cuenta

    por_id = {r["id"]: r for r in L}
    tramos, puente = orilla_jugable()
    dA = (e.BARANDA[1] - e.BARANDA[0]) / np.linalg.norm(e.BARANDA[1] - e.BARANDA[0])
    nA = np.array([-dA[1], dA[0]])
    s_esc = float((np.array(e.suelo(0.13, 0.86)) - e.BARANDA[1]) @ dA)
    c_esc = e.BARANDA[1] + dA * s_esc

    def r2(v):
        return [round(float(a), 3) for a in v]

    jugable = {
        "limites": LIMITES, "cerco": CERCO,
        "umbral_ciudad": r2(UMBRAL_CIUDAD), "umbral_mirador": r2(UMBRAL_MIRADOR),
        "entrada_casa": r2(ENTRADA_CASA), "entrada_mirador": r2(ENTRADA_MIRADOR),
        "faroles": [r2(f) for f in FAROLES],
        "muros": MUROS, "ruta_norte": [r2(p) for p in RUTA_NORTE],
        "orilla": tramos,
        "puente": {"inicio": r2(puente["inicio"]), "fin": r2(puente["fin"]), "eje": r2(puente["eje"]),
                   "medio_ancho": puente["medio_ancho"], "tablero_y": round(0.02 + PUENTE_TABLERO * PUENTE_ESCALA, 3)},
        "baranda_a": {"desde": r2(e.BARANDA[1] - dA * 9.6 + nA * 0.16), "hasta": r2(e.BARANDA[1] + nA * 0.16)},
        "baranda_b": {"desde": r2(e.BORDE_B[0] + nB * 0.16), "hasta": r2(e.BORDE_B[0] + dB * 6.6 + nB * 0.16)},
        "escalinata": {"arriba": r2(c_esc - nA * 0.05), "abajo": r2(c_esc + nA * 1.75), "ancho": 3.9, "y_abajo": e.PLAZA_Y},
        "tronco": huella_tronco(por_id["VEG-02"]),
        "antena": r2((por_id["COL-01_script"]["pos"][0], por_id["COL-01_script"]["pos"][2])),
        "panel": r2((por_id["COL-02"]["pos"][0], por_id["COL-02"]["pos"][2])),
        "iguana": r2((por_id["FAU-01"]["pos"][0], por_id["FAU-01"]["pos"][2])),
    }
    informe["tramos_de_orilla"] = len(tramos)
    informe["celdas_del_tronco"] = len(jugable["tronco"])
    ZONA.mkdir(parents=True, exist_ok=True)
    (ZONA / "layout.json").write_text(
        json.dumps({"_nota": "Escrito por herramientas/mallas/sendero_ampliacion.py a partir del layout aprobado "
                             "(pruebas/escena_exploracion/layout.json, D-015). No editar a mano.",
                    "camara": aprobado["camara"], "ambiente": aprobado["ambiente"], "jugable": jugable,
                    "recursos": L}, indent=1, ensure_ascii=False), encoding="utf-8")
    informe["recursos_en_layout"] = len(L)
    informe["recursos_del_layout_aprobado"] = len(aprobado["recursos"])


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    informe = {}
    franjas = suelo_y_hierba(informe)
    informe["TER-09_agua_este"] = {"triangulos": guardar(SALIDA / "TER-09_agua_este.glb", "TER-09_agua_este", agua_este())}
    informe["TER-13_mosaico_ext"] = {"triangulos": guardar(SALIDA / "TER-13_mosaico_ext.glb", "TER-13_mosaico_ext", mosaico_ext())}
    dB = (e.BORDE_B[1] - e.BORDE_B[0]) / np.linalg.norm(e.BORDE_B[1] - e.BORDE_B[0])
    muro = e.muro("TER-12_muro_B3", e.BORDE_B[0] + dB * 0.2, e.BORDE_B[0] + dB * 2.95, np.random.default_rng(123))
    informe["TER-12_muro_B3"] = {"triangulos": guardar(SALIDA / "TER-12_muro_B3.glb", "TER-12_muro_B3", muro)}
    antena_apuntada(informe)
    farol(informe)
    layout(informe, franjas)
    (SALIDA / "informe_generador.json").write_text(json.dumps(informe, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(informe, ensure_ascii=False))


if __name__ == "__main__":
    main()
