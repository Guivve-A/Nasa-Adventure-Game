"""Esqueleto, pesos y animaciones de la protagonista (PER-01), por script. Probado en Blender 5.3.

Uso (una sola instancia de Blender, sin ventana, desde la raiz del repositorio):
  blender -b --factory-startup --python-exit-code 1 --python herramientas/blender/rig_protagonista.py -- \
      --entrada juego/modelos/personajes/PER-01.glb --salida juego/modelos/personajes/PER-01_rig.glb \
      --textura 2048 --medidas juego/modelos/personajes/PER-01_medidas.json \
      [--guardar-blend <archivo.blend>] [--informe <json>] [--renders <carpeta>]

Que hace, de punta a punta (la entrada nunca se modifica):
  1. Importa el GLB (malla del cuerpo y bolso), hornea las transformaciones de los nodos en los vertices
     y reduce la textura del cuerpo a --textura px de lado.
  2. Mide la malla (suelo, tronco, brazos, piernas, bolso) y coloca una armadura propia de 20 huesos:
     cadera (raiz), columna, pecho, cuello, cabeza, hombro/brazo/antebrazo/mano x2, muslo/pierna/pie x2 y bolso.
  3. Calcula los pesos sin el calor de huesos de Blender: regiones por conectividad y geometria, mezcla
     analitica en codo, muneca, rodilla y tobillo, y difusion armonica sobre la malla en hombros, caderas y
     cuello. Cabeza, cara y pelo quedan rigidos al hueso de la cabeza; el bolso, rigido a su hueso.
  4. Genera seis clips por formula (reposo, caminar, correr, salto_lunar, recoger, celebrar) a 50 cuadros por
     segundo, con las piernas resueltas por cinematica inversa analitica y los pies apoyados en el suelo.
     Solo se anima la rotacion de cada hueso y la posicion vertical de la cadera (sin escala ni cizalla).
  5. Exporta un GLB (una pista NLA por clip) y lo comprueba leyendo el propio archivo: malla en reposo igual
     a la de entrada, estiramiento de aristas, altura de los pies, cierre de ciclos, bolso y zancadas.

Convenciones (las de la entrada): en glTF mira a +X, arriba +Y, derecha del personaje +Z, 1 m de alto y
origen a media altura. En Blender: mira a +X, arriba +Z, su derecha en -Y.
Las constantes de C estan medidas sobre PER-01 v9 (metros sobre el suelo y distancias laterales).
"""
import argparse
import json
import math
import struct
import sys
import time
import traceback
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector
from mathutils.bvhtree import BVHTree

RAIZ = Path(__file__).resolve().parents[2]
FPS = 50
# nombre, duracion en segundos, ciclico
CLIPS = [("reposo", 2.0, True), ("caminar", 0.8, True), ("correr", 0.56, True),
         ("salto_lunar", 1.2, True), ("recoger", 1.0, False), ("celebrar", 1.4, False)]
LADOS = (("izq", 1.0), ("der", -1.0))
HUESOS = ["cadera", "columna", "pecho", "cuello", "cabeza",
          "hombro_izq", "brazo_izq", "antebrazo_izq", "mano_izq",
          "hombro_der", "brazo_der", "antebrazo_der", "mano_der",
          "muslo_izq", "pierna_izq", "pie_izq", "muslo_der", "pierna_der", "pie_der", "bolso"]
PADRES = {"cadera": None, "columna": "cadera", "pecho": "columna", "cuello": "pecho", "cabeza": "cuello",
          "hombro_izq": "pecho", "brazo_izq": "hombro_izq", "antebrazo_izq": "brazo_izq", "mano_izq": "antebrazo_izq",
          "hombro_der": "pecho", "brazo_der": "hombro_der", "antebrazo_der": "brazo_der", "mano_der": "antebrazo_der",
          "muslo_izq": "cadera", "pierna_izq": "muslo_izq", "pie_izq": "pierna_izq",
          "muslo_der": "cadera", "pierna_der": "muslo_der", "pie_der": "pierna_der", "bolso": "cadera"}
IH = {n: i for i, n in enumerate(HUESOS)}

# Constantes medidas sobre PER-01 v9: h = metros sobre el suelo, y = distancia lateral al plano medio.
C = {
    "h_cadera": 0.400, "h_columna": 0.475, "h_pecho": 0.560, "h_cuello": 0.652, "h_cabeza": 0.690,
    "h_coronilla": 0.900,
    "h_art_cadera": 0.395, "y_art_cadera": 0.072, "h_rodilla": 0.240, "h_tobillo": 0.085,
    "adelanto_rodilla": 0.014,
    "h_hombro": 0.612, "y_hombro": 0.108, "h_clavicula": 0.630, "y_clavicula": 0.030,
    "t_codo": (0.075, 0.125), "t_muneca": (0.155, 0.195),
    # regiones
    "y_corte_brazo": 0.115,      # mas alla de esta distancia lateral solo hay brazo (bajo el pelo)
    "h_semilla_pierna": 0.300,   # por debajo, la pierna es una pieza suelta de la otra
    "h_libre_cadera": 0.455,     # hasta aqui llega la zona de difusion de la cadera
    "t_semilla_brazo": 0.045,    # a partir de aqui (m desde el hombro) el brazo ya no se mezcla con el tronco
    "y_libre_hombro": 0.080, "h_libre_hombro": (0.50, 0.70),
    # mezclas analiticas (semiancho en metros)
    "mezcla_codo": 0.022, "mezcla_muneca": (0.012, 0.014), "mezcla_rodilla": 0.035,
    "mezcla_tobillo": (0.085, 0.130),
    "tronco_cadera": (0.455, 0.515), "tronco_pecho": (0.535, 0.600),
    "clavicula_y": (0.035, 0.080), "clavicula_h": (0.575, 0.620),
    # cabeza y pelo
    "h_cabeza_segura": 0.705, "h_pelo_min": 0.635, "pelo_x_detras": -0.024, "pelo_y_lado": 0.060,
}

T0 = time.time()
AVISOS = []


def log(texto):
    print("[rig_protagonista %6.1f s] %s" % (time.time() - T0, texto), flush=True)


def aviso(texto):
    AVISOS.append(texto)
    print("AVISO: " + texto, flush=True)


def exigir(condicion, mensaje):
    if not condicion:
        raise RuntimeError(mensaje)


def argumentos():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    base = RAIZ / "juego/modelos/personajes"
    p.add_argument("--entrada", type=Path, default=base / "PER-01.glb", help="GLB aprobado, solo lectura")
    p.add_argument("--salida", type=Path, default=base / "PER-01_rig.glb", help="GLB con esqueleto y clips")
    p.add_argument("--textura", type=int, default=2048, help="lado maximo de la textura del cuerpo")
    p.add_argument("--guardar-blend", type=Path, help="guarda tambien la escena de Blender")
    p.add_argument("--medidas", type=Path, default=None, help="JSON de medidas (por defecto, junto a la salida)")
    p.add_argument("--informe", type=Path, help="JSON con todas las comprobaciones")
    p.add_argument("--renders", type=Path, help="carpeta para las tiras de cuadros y los mapas de pesos")
    a = p.parse_args(argv)
    a.entrada, a.salida = a.entrada.resolve(), a.salida.resolve()
    if a.medidas is None:
        a.medidas = a.salida.with_name(a.salida.stem.replace("_rig", "") + "_medidas.json")
    exigir(a.entrada.is_file(), "No existe la entrada: %s" % a.entrada)
    exigir(a.entrada != a.salida, "La salida pisaria la entrada")
    return a


# ---------------------------------------------------------------------------------------- utilidades

def paso(x, a, b):
    """Escalon suave de 0 (x <= a) a 1 (x >= b)."""
    t = np.clip((np.asarray(x, dtype=float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def QX(g):
    return Quaternion((1.0, 0.0, 0.0), math.radians(g))


def QY(g):
    return Quaternion((0.0, 1.0, 0.0), math.radians(g))


def QZ(g):
    return Quaternion((0.0, 0.0, 1.0), math.radians(g))


def suave(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3.0 - 2.0 * t)


def curva(p, claves):
    """Curva ciclica por tramos suavizados (pendiente nula en cada clave). claves: [(fase, valor)], fase en [0, 1)."""
    n = len(claves)
    pp = p if p >= claves[0][0] else p + 1.0
    for i in range(n):
        p0, v0 = claves[i]
        p1, v1 = claves[(i + 1) % n]
        if i == n - 1:
            p1 += 1.0
        if p0 <= pp <= p1:
            return v0 + (v1 - v0) * suave((pp - p0) / (p1 - p0))
    return claves[0][1]


def hermite(q, x0, x1, m0, m1):
    q2, q3 = q * q, q * q * q
    return (2 * q3 - 3 * q2 + 1) * x0 + (q3 - 2 * q2 + q) * m0 + (-2 * q3 + 3 * q2) * x1 + (q3 - q2) * m1


def entre_claves(t, claves):
    """Poses clave [(tiempo, dict)] -> dict interpolado con suavizado entre claves vecinas."""
    if t <= claves[0][0]:
        return dict(claves[0][1])
    for (t0, a), (t1, b) in zip(claves[:-1], claves[1:]):
        if t0 <= t <= t1:
            f = suave((t - t0) / (t1 - t0))
            return {k: a.get(k, 0.0) + (b.get(k, 0.0) - a.get(k, 0.0)) * f for k in set(a) | set(b)}
    return dict(claves[-1][1])


def rgb_a_hsv(c):
    mx, mn = c.max(1), c.min(1)
    d = mx - mn
    s = np.where(mx > 1e-9, d / np.maximum(mx, 1e-9), 0.0)
    dd = np.maximum(d, 1e-9)
    r, g, b = c[:, 0], c[:, 1], c[:, 2]
    hh = np.where(mx == r, ((g - b) / dd) % 6.0, np.where(mx == g, (b - r) / dd + 2.0, (r - g) / dd + 4.0)) / 6.0
    hh = np.where(d > 1e-9, hh, 0.0)
    return hh, s, mx


# ---------------------------------------------------------------------------------------- importar

def importar(ruta, lado_textura):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    exigir("FINISHED" in bpy.ops.import_scene.gltf(filepath=str(ruta)), "El importador glTF no termino")
    escena = bpy.context.scene
    mallas = [o for o in escena.objects if o.type == "MESH"]
    exigir(len(mallas) == 2, "Se esperaban 2 mallas (cuerpo y bolso) y hay %d" % len(mallas))
    exigir(not any(o.type == "ARMATURE" for o in escena.objects), "La entrada ya trae esqueleto")
    mallas.sort(key=lambda o: len(o.data.vertices))
    bolso, cuerpo = mallas
    if "bolso" not in bolso.name.lower():
        aviso("La malla pequena no se llama 'bolso' (%s): se toma como bolso por tamano" % bolso.name)
    for o in mallas:
        exigir(not o.data.shape_keys, "La entrada trae shape keys")
        o.data.transform(o.matrix_world)       # hornea la transformacion del nodo en los vertices
        o.parent = None
        o.matrix_world = Matrix.Identity(4)
        o.data.update()
    for o in list(escena.objects):
        if o not in mallas:
            bpy.data.objects.remove(o, do_unlink=True)
    cuerpo.name, cuerpo.data.name = "PER01_cuerpo", "PER01_cuerpo"
    bolso.name, bolso.data.name = "PER01_bolso", "PER01_bolso"

    # textura del cuerpo: se reduce y se vuelve a empaquetar como PNG nuevo (los pixeles, tal cual)
    nodo = next(n for n in cuerpo.data.materials[0].node_tree.nodes if n.type == "TEX_IMAGE" and n.image)
    vieja = nodo.image
    exigir(vieja.packed_file is not None, "La textura del cuerpo no viene empaquetada")
    antes = tuple(vieja.size)
    f = min(1.0, lado_textura / max(antes))
    ancho, alto = max(1, int(round(antes[0] * f))), max(1, int(round(antes[1] * f)))
    if (ancho, alto) != antes:
        vieja.scale(ancho, alto)
    px = np.empty(ancho * alto * 4, dtype=np.float32)
    vieja.pixels.foreach_get(px)
    nueva = bpy.data.images.new("PER01_cuerpo_color", ancho, alto, alpha=False)
    nueva.pixels.foreach_set(px)
    nueva.pack()
    nodo.image = nueva
    bpy.data.images.remove(vieja)
    log("Textura del cuerpo: %dx%d -> %dx%d" % (antes[0], antes[1], ancho, alto))
    return cuerpo, bolso, px.reshape(alto, ancho, 4), {"antes": list(antes), "despues": [ancho, alto]}


def geometria(obj):
    """Posiciones, triangulos y grafo de posiciones unicas (los vertices duplicados en las costuras UV se unen
    solo para calcular; la malla no se toca)."""
    me = obj.data
    n = len(me.vertices)
    co = np.empty(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(n, 3)
    me.calc_loop_triangles()
    nt = len(me.loop_triangles)
    tv = np.empty(nt * 3, dtype=np.int32)
    tl = np.empty(nt * 3, dtype=np.int32)
    me.loop_triangles.foreach_get("vertices", tv)
    me.loop_triangles.foreach_get("loops", tl)
    tv, tl = tv.reshape(nt, 3), tl.reshape(nt, 3)
    uv = np.empty(len(me.loops) * 2)
    me.uv_layers[0].data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    llave = np.round(co / 1e-5).astype(np.int64)
    _, primero, inv = np.unique(llave, axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel()
    up = co[primero]
    tu = inv[tv]
    ar = np.concatenate([tu[:, [0, 1]], tu[:, [1, 2]], tu[:, [2, 0]]])
    ar = np.unique(np.sort(ar, axis=1), axis=0)
    ar = ar[ar[:, 0] != ar[:, 1]]
    ady = [[] for _ in range(len(up))]
    for a, b in ar:
        ady[a].append(int(b))
        ady[b].append(int(a))
    return {"co": co, "tv": tv, "tri_uv": uv[tl], "inv": inv, "up": up, "tu": tu, "ar": ar, "ady": ady,
            "nt": nt, "nu": len(up)}


def componente(g, mascara, semilla):
    """Componente conexa de 'semilla' dentro del subgrafo de los vertices unicos marcados."""
    visto = np.zeros(g["nu"], dtype=bool)
    if not mascara[semilla]:
        return visto
    pila = [int(semilla)]
    visto[semilla] = True
    while pila:
        a = pila.pop()
        for b in g["ady"][a]:
            if mascara[b] and not visto[b]:
                visto[b] = True
                pila.append(b)
    return visto


def anillos(g, origen, maximo):
    """Distancia en aristas a los vertices de 'origen' (hasta 'maximo')."""
    dist = np.full(g["nu"], 99, dtype=np.int32)
    dist[origen] = 0
    frente = list(np.where(origen)[0])
    for k in range(1, maximo + 1):
        nuevo = []
        for a in frente:
            for b in g["ady"][a]:
                if dist[b] > k:
                    dist[b] = k
                    nuevo.append(b)
        frente = nuevo
    return dist


# ---------------------------------------------------------------------------------------- regiones y medidas

def clasificar(g, px, zs):
    """Cabeza y pelo (por color de la textura y posicion), brazos y piernas (por conectividad)."""
    up, tu = g["up"], g["tu"]
    alto_px, ancho_px = px.shape[:2]
    bar = np.array([[1 / 3, 1 / 3, 1 / 3], [0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6],
                    [0.45, 0.45, 0.1], [0.1, 0.45, 0.45], [0.45, 0.1, 0.45]])
    muestras = []
    for b in bar:
        p = (g["tri_uv"] * b[None, :, None]).sum(1)
        x = np.clip((p[:, 0] * ancho_px).astype(int), 0, ancho_px - 1)
        y = np.clip((p[:, 1] * alto_px).astype(int), 0, alto_px - 1)
        muestras.append(px[y, x, :3])
    color = np.median(np.stack(muestras), axis=0).astype(float)
    tono, sat, val = rgb_a_hsv(color)
    cen = up[tu].mean(1)
    hc = cen[:, 2] - zs
    h = up[:, 2] - zs

    # tronco: eje x a la altura del pecho (sin pelo todavia: se usa solo la banda bajo los hombros)
    banda = (h > 0.54) & (h < 0.62) & (np.abs(up[:, 1]) < 0.10)
    x_pecho = 0.5 * (up[banda, 0].min() + up[banda, 0].max())

    pelo = (val < 0.46) & (sat > 0.40) & ((tono < 0.075) | (tono > 0.95))
    cab_t = (hc > C["h_cabeza_segura"]) | (pelo & (hc > C["h_pelo_min"]) &
                                           ((cen[:, 0] < x_pecho + C["pelo_x_detras"]) |
                                            (np.abs(cen[:, 1]) > C["pelo_y_lado"])))
    cabeza = np.zeros(g["nu"], dtype=bool)
    cabeza[tu[cab_t].ravel()] = True
    exigir(1200 < cabeza.sum() < 2100, "Cabeza y pelo con %d vertices: fuera de lo esperado" % cabeza.sum())

    brazos, piernas = {}, {}
    for lado, s in LADOS:
        ys = up[:, 1] * s
        mascara = (ys > C["y_corte_brazo"]) & ~cabeza
        punta = int(np.argmax(np.where(mascara & (h < 0.45), ys, -9.0)))
        brazos[lado] = componente(g, mascara, punta)
        exigir(90 < brazos[lado].sum() < 320, "Brazo %s con %d vertices" % (lado, brazos[lado].sum()))
    mascara = (h < C["h_semilla_pierna"]) & ~brazos["izq"] & ~brazos["der"]
    for lado, s in LADOS:
        ys = up[:, 1] * s
        pie = int(np.argmin(np.where(mascara & (ys > 0.03), h, 9.0)))
        piernas[lado] = componente(g, mascara, pie)
        exigir(piernas[lado].sum() > 300, "Pierna %s con %d vertices" % (lado, piernas[lado].sum()))
    exigir(not (piernas["izq"] & piernas["der"]).any(), "Las piernas estan unidas por debajo de la entrepierna")
    sueltos = mascara & ~piernas["izq"] & ~piernas["der"]
    exigir(sueltos.sum() == 0, "%d vertices bajo la entrepierna no son de ninguna pierna" % sueltos.sum())
    log("Regiones: cabeza y pelo %d, brazos %d y %d, piernas %d y %d vertices unicos (de %d)" % (
        cabeza.sum(), brazos["izq"].sum(), brazos["der"].sum(), piernas["izq"].sum(), piernas["der"].sum(), g["nu"]))
    return {"cabeza": cabeza, "brazos": brazos, "piernas": piernas, "h": h, "x_pecho": float(x_pecho),
            "tri_cabeza": cab_t}


def centro_caja(p):
    return 0.5 * (p.min(0) + p.max(0))


def medir(g, reg, gb, zs):
    """Articulaciones en coordenadas de Blender, medidas sobre la malla."""
    up, h = g["up"], reg["h"]
    z = lambda alto: zs + alto
    tronco = ~reg["cabeza"] & ~reg["brazos"]["izq"] & ~reg["brazos"]["der"] & (np.abs(up[:, 1]) < 0.115)
    banda = tronco & (h > 0.36) & (h < 0.46)
    x_cad = 0.5 * (up[banda, 0].min() + up[banda, 0].max())
    x_pec = reg["x_pecho"]
    x_col = 0.5 * (x_cad + x_pec)
    art = {
        "cadera": (Vector((x_cad, 0, z(C["h_cadera"]))), Vector((x_col, 0, z(C["h_columna"])))),
        "columna": (Vector((x_col, 0, z(C["h_columna"]))), Vector((x_pec, 0, z(C["h_pecho"])))),
        "pecho": (Vector((x_pec, 0, z(C["h_pecho"]))), Vector((x_pec, 0, z(C["h_cuello"])))),
        "cuello": (Vector((x_pec, 0, z(C["h_cuello"]))), Vector((x_pec, 0, z(C["h_cabeza"])))),
        "cabeza": (Vector((x_pec, 0, z(C["h_cabeza"]))), Vector((x_pec - 0.01, 0, z(C["h_coronilla"])))),
    }
    extra = {"x_cadera": float(x_cad), "x_pecho": float(x_pec)}
    for lado, s in LADOS:
        # brazo: rebanadas a lo largo de la direccion nominal de la pose en A
        P = up[reg["brazos"][lado]]
        d0 = Vector((0.0, 0.47 * s, -0.88)).normalized()
        s0 = np.array([x_pec - 0.015, C["y_hombro"] * s, z(C["h_hombro"])])
        t = (P - s0) @ np.array(d0)
        arriba = P[(t > -0.01) & (t < 0.03)]
        x_h = float(np.clip(centro_caja(arriba)[0], x_pec - 0.03, x_pec + 0.01)) if len(arriba) >= 4 else x_pec - 0.015
        hombro = Vector((x_h, C["y_hombro"] * s, z(C["h_hombro"])))

        def rebanada(a, b, nominal):
            q = P[(t >= a) & (t < b)]
            if len(q) < 5:
                aviso("Brazo %s: rebanada %.3f-%.3f con %d vertices; se usa la posicion nominal" % (lado, a, b, len(q)))
                return Vector(nominal)
            c = Vector(centro_caja(q))
            if (c - Vector(nominal)).length > 0.03:
                aviso("Brazo %s: centro medido a %.1f cm del nominal; se usa el nominal" % (
                    lado, (c - Vector(nominal)).length * 100))
                return Vector(nominal)
            return c

        codo = rebanada(C["t_codo"][0], C["t_codo"][1], (x_h - 0.015, 0.150 * s, z(0.520)))
        muneca = rebanada(C["t_muneca"][0], C["t_muneca"][1], (x_h - 0.005, 0.195 * s, z(0.450)))
        punta = Vector(P[np.argsort(t)[-5:]].mean(0))
        art["hombro_" + lado] = (Vector((x_pec - 0.005, C["y_clavicula"] * s, z(C["h_clavicula"]))), hombro)
        art["brazo_" + lado] = (hombro, codo)
        art["antebrazo_" + lado] = (codo, muneca)
        art["mano_" + lado] = (muneca, punta)
        # pierna
        Q = up[reg["piernas"][lado]]
        hq = Q[:, 2] - zs
        ct = centro_caja(Q[(hq > 0.075) & (hq < 0.100)])
        cadera_art = Vector((x_cad, C["y_art_cadera"] * s, z(C["h_art_cadera"])))
        tobillo = Vector((float(ct[0]), float(ct[1]), z(C["h_tobillo"])))
        rodilla = Vector((0.5 * (cadera_art.x + tobillo.x) + C["adelanto_rodilla"],
                          0.5 * (cadera_art.y + tobillo.y), z(C["h_rodilla"])))
        punta_pie = Vector((float(Q[:, 0].max()) - 0.02, tobillo.y, z(0.03)))
        art["muslo_" + lado] = (cadera_art, rodilla)
        art["pierna_" + lado] = (rodilla, tobillo)
        art["pie_" + lado] = (tobillo, punta_pie)
    # bolso: cuelga de su borde superior trasero (lado de la cadera)
    pb = gb["co"]
    cb = centro_caja(pb)
    u = Vector((math.cos(math.radians(45.0)), -math.sin(math.radians(45.0)), 0.0))  # hacia fuera (accesorio_bolso_v2)
    zb = float(pb[:, 2].min())
    pivote = Vector((cb[0], cb[1], zb + 0.100)) - u * 0.022
    art["bolso"] = (pivote, pivote + Vector((0, 0, -0.09)))
    for n in HUESOS:
        exigir((art[n][1] - art[n][0]).length > 0.01, "Hueso demasiado corto: " + n)
    return art, extra


# ---------------------------------------------------------------------------------------- pesos

def calcular_pesos(g, reg, art, zs):
    up, h, nu = g["up"], reg["h"], g["nu"]
    nb = len(HUESOS)
    W = np.zeros((nu, nb))
    cabeza = reg["cabeza"]
    brazo_cualq = reg["brazos"]["izq"] | reg["brazos"]["der"]

    # 1) tronco por altura, con la clavicula hacia los lados (formula para todo; despues se pisa por region)
    w_cad = 1.0 - paso(h, *C["tronco_cadera"])
    w_pec = paso(h, *C["tronco_pecho"])
    w_col = 1.0 - w_cad - w_pec
    f = {lado: paso(up[:, 1] * s, *C["clavicula_y"]) * paso(h, *C["clavicula_h"]) for lado, s in LADOS}
    W[:, IH["cadera"]] = w_cad
    W[:, IH["columna"]] = w_col
    W[:, IH["pecho"]] = w_pec * (1.0 - f["izq"] - f["der"])
    W[:, IH["hombro_izq"]] = w_pec * f["izq"]
    W[:, IH["hombro_der"]] = w_pec * f["der"]

    libre = np.zeros(nu, dtype=bool)
    info = {}
    for lado, s in LADOS:
        # 2) brazo: cadena brazo -> antebrazo -> mano por planos bisectores en codo y muneca
        comp = reg["brazos"][lado]
        S_, E_ = art["brazo_" + lado]
        W_, F_ = art["mano_" + lado]
        ub, uf, um = (E_ - S_).normalized(), (W_ - E_).normalized(), (F_ - W_).normalized()
        n_codo, n_mun = np.array((ub + uf).normalized()), np.array((uf + um).normalized())
        P = up[comp]
        w_ante = paso((P - np.array(E_)) @ n_codo, -C["mezcla_codo"], C["mezcla_codo"])
        w_mano = paso((P - np.array(W_)) @ n_mun, -C["mezcla_muneca"][0], C["mezcla_muneca"][1])
        fila = np.zeros((comp.sum(), nb))
        fila[:, IH["brazo_" + lado]] = 1.0 - w_ante
        fila[:, IH["antebrazo_" + lado]] = w_ante * (1.0 - w_mano)
        fila[:, IH["mano_" + lado]] = w_ante * w_mano
        W[comp] = fila
        t = (up - np.array(S_)) @ np.array(ub)
        semilla_brazo = comp & (t >= C["t_semilla_brazo"])
        ys = up[:, 1] * s
        zona = (~cabeza & (ys > C["y_libre_hombro"]) & (h > C["h_libre_hombro"][0]) & (h < C["h_libre_hombro"][1])
                & ~semilla_brazo)
        libre |= zona
        info["libres_hombro_" + lado] = int(zona.sum())

        # 3) pierna: muslo -> pierna -> pie
        comp = reg["piernas"][lado]
        H_, K_ = art["muslo_" + lado]
        A_ = art["pierna_" + lado][1]
        n_rod = np.array(((K_ - H_).normalized() + (A_ - K_).normalized()).normalized())
        P = up[comp]
        w_pierna = paso((P - np.array(K_)) @ n_rod, -C["mezcla_rodilla"], C["mezcla_rodilla"])
        w_pie = 1.0 - paso(h[comp], *C["mezcla_tobillo"])
        fila = np.zeros((comp.sum(), nb))
        fila[:, IH["muslo_" + lado]] = 1.0 - w_pierna
        fila[:, IH["pierna_" + lado]] = w_pierna * (1.0 - w_pie)
        fila[:, IH["pie_" + lado]] = w_pierna * w_pie
        W[comp] = fila

    # 4) cabeza, cara y pelo: rigidos
    W[cabeza] = 0.0
    W[cabeza, IH["cabeza"]] = 1.0

    # 5) zonas libres: cadera (entre las piernas y la cintura), hombros y cuello
    zona_cadera = ~cabeza & ~brazo_cualq & (h >= C["h_semilla_pierna"]) & (h <= C["h_libre_cadera"])
    dist = anillos(g, cabeza, 2)
    eje = np.hypot(up[:, 0] - reg["x_pecho"], up[:, 1])
    zona_cuello = ~cabeza & (h > 0.64) & ((dist <= 1) | ((dist <= 2) & (eje < 0.055)))
    libre |= zona_cadera | zona_cuello
    info.update(libres_cadera=int(zona_cadera.sum()), libres_cuello=int(zona_cuello.sum()), libres=int(libre.sum()))

    # difusion armonica: cada peso libre es la media (ponderada por 1/longitud) de sus vecinos
    ar = g["ar"]
    largo = np.linalg.norm(up[ar[:, 0]] - up[ar[:, 1]], axis=1)
    wa = 1.0 / np.maximum(largo, 0.002)
    idx = np.where(libre)[0]
    pos = np.full(nu, -1, dtype=np.int64)
    pos[idx] = np.arange(len(idx))
    A = np.zeros((len(idx), len(idx)))
    B = np.zeros((len(idx), nb))
    for (a, b), w in zip(ar, wa):
        for i, j in ((a, b), (b, a)):
            if libre[i]:
                fi = pos[i]
                A[fi, fi] += w
                if libre[j]:
                    A[fi, pos[j]] -= w
                else:
                    B[fi] += w * W[j]
    exigir(np.all(np.diag(A) > 0), "Hay vertices libres sin vecinos")
    W[idx] = np.linalg.solve(A, B)

    # 6) cuello: en la zona del cuello la fraccion de cabeza u se reparte pecho -> cuello -> cabeza
    ic = np.where(zona_cuello)[0]
    u = np.clip(W[ic, IH["cabeza"]], 0.0, 1.0)
    resto = W[ic].copy()
    resto[:, IH["cabeza"]] = 0.0
    suma = resto.sum(1, keepdims=True)
    resto = np.where(suma > 1e-9, resto / np.maximum(suma, 1e-9), 0.0)
    nuevo = resto * np.maximum(0.0, 1.0 - 2.0 * u)[:, None]
    nuevo[:, IH["cabeza"]] = np.maximum(0.0, 2.0 * u - 1.0)
    nuevo[:, IH["cuello"]] += 1.0 - np.abs(2.0 * u - 1.0)
    W[ic] = nuevo

    # 7) suavizado ligero de todo lo que no es rigido de la cabeza
    movil = ~cabeza
    for _ in range(2):
        num = np.zeros_like(W)
        den = np.zeros(nu)
        np.add.at(num, ar[:, 0], W[ar[:, 1]] * wa[:, None])
        np.add.at(num, ar[:, 1], W[ar[:, 0]] * wa[:, None])
        np.add.at(den, ar[:, 0], wa)
        np.add.at(den, ar[:, 1], wa)
        media = num / np.maximum(den, 1e-12)[:, None]
        W[movil] = 0.5 * W[movil] + 0.5 * media[movil]

    # 8) limpieza: sin pesos minimos, 4 influencias como mucho y suma 1
    W = np.clip(W, 0.0, None)
    W[W < 0.02] = 0.0
    orden = np.argsort(-W, axis=1)
    quitar = orden[:, 4:]
    np.put_along_axis(W, quitar, 0.0, axis=1)
    suma = W.sum(1, keepdims=True)
    exigir(np.all(suma > 1e-6), "Vertices sin peso")
    W /= suma
    exigir(np.allclose(W[cabeza, IH["cabeza"]], 1.0), "La cabeza dejo de ser rigida")
    info["influencias_max"] = int((W > 0).sum(1).max())
    info["por_hueso"] = {n: int((W[:, IH[n]] > 0.5).sum()) for n in HUESOS}
    return W, info


# ---------------------------------------------------------------------------------------- armadura

def crear_armadura(art):
    arm = bpy.data.armatures.new("PER01_esqueleto")
    ob = bpy.data.objects.new("PER01_esqueleto", arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for n in HUESOS:
        eb = arm.edit_bones.new(n)
        eb.head, eb.tail = art[n][0], art[n][1]
        eb.roll = 0.0
        eb.use_deform = True
    for n in HUESOS:
        if PADRES[n]:
            arm.edit_bones[n].parent = arm.edit_bones[PADRES[n]]
            arm.edit_bones[n].use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")
    for n in HUESOS:
        b = arm.bones[n]
        exigir((b.head_local - art[n][0]).length < 1e-6, "El hueso %s no quedo donde se pidio" % n)
        ob.pose.bones[n].rotation_mode = "QUATERNION"
    return ob


def enlazar(obj, armadura, pesos_por_vertice):
    """pesos_por_vertice: matriz (vertices de Blender x huesos)."""
    for n in HUESOS:
        col = pesos_por_vertice[:, IH[n]]
        idx = np.where(col > 0)[0]
        if len(idx) == 0:
            continue
        vg = obj.vertex_groups.new(name=n)
        for i in idx:
            vg.add([int(i)], float(col[i]), "REPLACE")
    mod = obj.modifiers.new("Esqueleto", "ARMATURE")
    mod.object = armadura
    mod.use_deform_preserve_volume = False
    obj.parent = armadura
    obj.matrix_parent_inverse = Matrix.Identity(4)


# ---------------------------------------------------------------------------------------- cinematica y poses

class Cinematica:
    """Cinematica directa propia (la misma que usa Blender: cada hueso gira sobre su cabeza en reposo, en ejes de
    la armadura, y hereda la transformacion de su padre) y cinematica inversa analitica de las piernas."""

    def __init__(self, art, suelas, zs):
        self.cab = {n: art[n][0].copy() for n in HUESOS}
        self.zs = zs
        self.suelas = suelas                     # lado -> puntos de la suela relativos al tobillo (numpy)
        self.eje = {n: (art[n][1] - art[n][0]).normalized() for n in HUESOS}
        self.pierna = {}
        for lado, s in LADOS:
            H0, K0, A0 = self.cab["muslo_" + lado], self.cab["pierna_" + lado], self.cab["pie_" + lado]
            dm0, dp0 = (K0 - H0).normalized(), (A0 - K0).normalized()
            n0 = dm0.cross(dp0).normalized()
            exigir(n0.y > 0.9, "El plano de la rodilla en reposo no es sagital (lado %s)" % lado)
            sr = suelas[lado]
            # pivotes: el punto mas bajo de la suela con la punta arriba (talon) y con el talon arriba (punta)
            talon = sr[np.argmin((sr @ np.array(QY(-12.0).to_matrix()).T)[:, 2])]
            punta = sr[np.argmin((sr @ np.array(QY(22.0).to_matrix()).T)[:, 2])]
            self.pierna[lado] = {
                "H0": H0, "K0": K0, "A0": A0, "L1": (K0 - H0).length, "L2": (A0 - K0).length,
                "M0": self.marco(dm0, n0), "P0": self.marco(dp0, n0),
                "talon": A0 + Vector(talon), "punta": A0 + Vector(punta),
                "flex0": math.atan2(dm0.x, -dm0.z),
            }
        self.exceso = 0.0   # mayor distancia que le falto a una pierna para alcanzar su objetivo

    @staticmethod
    def marco(d, n):
        n2 = (n - d * n.dot(d)).normalized()
        return Matrix((d, n2, d.cross(n2))).transposed()

    def directa(self, pose):
        Q, P = {}, {}
        for n in HUESOS:
            d = pose["d"].get(n, Quaternion())
            pa = PADRES[n]
            if pa is None:
                Q[n] = d.copy()
                P[n] = self.cab[n] + pose["t"]
            else:
                Q[n] = Q[pa] @ d
                P[n] = P[pa] + Q[pa] @ (self.cab[n] - self.cab[pa])
        return Q, P

    def altura_tobillo(self, lado, qf):
        """Altura del tobillo sobre el punto mas bajo de la suela con el pie girado qf."""
        R = np.array(qf.to_matrix())
        return -float((self.suelas[lado] @ R.T)[:, 2].min())

    def construir(self, p):
        """Parametros (grados y metros; lo que falta vale 0) -> pose {'t': Vector, 'd': {hueso: Quaternion}}."""
        g = lambda k: p.get(k, 0.0)
        d = {}
        d["cadera"] = QZ(g("raiz_yaw")) @ QY(g("raiz_pitch")) @ QX(g("raiz_roll"))
        d["columna"] = QZ(g("col_yaw")) @ QY(g("col_pitch")) @ QX(g("col_roll"))
        d["pecho"] = QZ(g("pec_yaw")) @ QY(g("pec_pitch")) @ QX(g("pec_roll"))
        d["cuello"] = QZ(g("cue_yaw")) @ QY(g("cue_pitch")) @ QX(g("cue_roll"))
        d["cabeza"] = QZ(g("cab_yaw")) @ QY(g("cab_pitch")) @ QX(g("cab_roll"))
        for lado, s in LADOS:
            L = "_" + lado
            # hombro: elevar (hacia arriba) y adelantar; brazo: abrir, llevar adelante y girar sobre su eje
            d["hombro" + L] = QX(s * g("hom_elev" + L)) @ QZ(s * g("hom_adel" + L))
            d["brazo" + L] = (QX(s * g("abd" + L)) @ QY(-g("flex" + L))
                              @ Quaternion(self.eje["brazo" + L], math.radians(s * g("giro" + L))))
            d["antebrazo" + L] = (QX(s * g("codo_lat" + L)) @ QY(-g("codo" + L))
                                  @ Quaternion(self.eje["antebrazo" + L], math.radians(s * g("giro_ante" + L))))
            d["mano" + L] = (QX(s * g("mano_lat" + L)) @ QY(-g("mano_flex" + L))
                             @ Quaternion(self.eje["mano" + L], math.radians(s * g("giro_mano" + L))))
        pose = {"t": Vector((0.0, 0.0, g("raiz_z"))), "d": d}
        qr = d["cadera"]
        pr = self.cab["cadera"] + pose["t"]
        for lado, s in LADOS:
            L = "_" + lado
            pi = self.pierna[lado]
            pitch = g("pie_pitch" + L)
            qf = QZ(s * g("pie_yaw" + L)) @ QY(pitch)
            pivote = pi["talon"] if pitch < 0.0 else pi["punta"]
            a = pivote + Vector((g("pie_x" + L), s * g("pie_y" + L), 0.0)) + qf @ (pi["A0"] - pivote)
            a.z = self.zs + g("pie_z" + L) + self.altura_tobillo(lado, qf)
            H = pr + qr @ (pi["H0"] - self.cab["cadera"])
            polo = QZ(g("raiz_yaw") * 0.5) @ Vector((1.0, s * (0.10 + g("rodilla_abre" + L)), 0.0))
            qm, qp = self.inversa(lado, H, a, polo)
            d["muslo" + L] = qr.conjugated() @ qm
            d["pierna" + L] = qm.conjugated() @ qp
            d["pie" + L] = qp.conjugated() @ qf
            if lado == "der":
                # el bolso acompana al muslo derecho cuando este sube: evita que la pierna lo atraviese
                v = qr.conjugated() @ (qm @ (pi["K0"] - pi["H0"]))
                flex = math.degrees(math.atan2(v.x, -v.z) - pi["flex0"])
                sigue = 0.80 * max(flex, 0.0) + 0.15 * min(flex, 0.0)
                d["bolso"] = QY(-(sigue + g("bolso_pitch"))) @ QX(-g("bolso_fuera"))
        return pose

    def inversa(self, lado, H, A, polo):
        pi = self.pierna[lado]
        L1, L2 = pi["L1"], pi["L2"]
        v = A - H
        dist = v.length
        maxima = (L1 + L2) * 0.9985
        if dist > maxima:
            self.exceso = max(self.exceso, dist - maxima)
            v *= maxima / dist
            dist = maxima
            A = H + v
        dist = max(dist, abs(L1 - L2) + 1e-4)
        e = v.normalized()
        u = (polo - e * polo.dot(e)).normalized()
        cosa = max(-1.0, min(1.0, (L1 * L1 + dist * dist - L2 * L2) / (2.0 * L1 * dist)))
        sina = math.sqrt(max(0.0, 1.0 - cosa * cosa))
        K = H + (e * cosa + u * sina) * L1
        n = -(e.cross(u)).normalized()
        qm = (self.marco((K - H).normalized(), n) @ pi["M0"].transposed()).to_quaternion()
        qp = (self.marco((A - K).normalized(), n) @ pi["P0"].transposed()).to_quaternion()
        return qm, qp


def paso_pie(p, zancada, apoyo, alza, centro):
    """Recorrido de un pie en el sitio. p = fase (0 = toma de contacto). Devuelve (x, z).
    En el apoyo retrocede a velocidad constante; en el vuelo vuelve adelante con la misma velocidad en los extremos."""
    if p < apoyo:
        return centro + zancada * (0.5 - p / apoyo), 0.0
    q = (p - apoyo) / (1.0 - apoyo)
    m = -zancada * (1.0 - apoyo) / apoyo
    return centro + hermite(q, -zancada / 2, zancada / 2, m, m), alza * math.sin(math.pi * q ** 0.85) ** 2


# cabeceo del pie (grados; + = punta abajo, talon arriba) segun la fase de ese pie
CABECEO_CAMINAR = [(0.0, -16.0), (0.09, 0.0), (0.37, 0.0), (0.55, 27.0), (0.63, 33.0), (0.80, 6.0), (0.93, -13.0)]
CABECEO_CORRER = [(0.0, 3.0), (0.05, 0.0), (0.16, 0.0), (0.30, 32.0), (0.42, 56.0), (0.62, 34.0), (0.84, 0.0),
                  (0.95, 4.0)]
CAMINAR = {"zancada": 0.31, "apoyo": 0.55, "alza": 0.055, "centro": 0.012}
CORRER = {"zancada": 0.30, "apoyo": 0.30, "alza": 0.120, "centro": 0.0}


def p_reposo(u):
    a = 2.0 * math.pi * u
    resp = 0.5 * (1.0 - math.cos(a))        # inhalacion 0..1..0: en u = 0 es la pose de reposo exacta
    vaiven = math.sin(a)
    p = {"raiz_z": -0.003 * resp, "raiz_roll": 0.9 * vaiven, "col_roll": -0.6 * vaiven, "pec_roll": -0.3 * vaiven,
         "col_pitch": 0.6 * resp, "pec_pitch": -1.6 * resp, "cab_pitch": 0.9 * resp, "cab_roll": 0.5 * vaiven,
         "cab_yaw": 1.2 * vaiven, "cue_yaw": 0.6 * vaiven}
    for lado, s in LADOS:
        L = "_" + lado
        p["hom_elev" + L] = 2.2 * resp
        p["abd" + L] = 1.2 * resp
        p["flex" + L] = 1.2 * s * vaiven
        p["codo" + L] = 1.5 * resp
    return p


def p_caminar(u):
    k = CAMINAR
    a = 2.0 * math.pi * u
    bote = math.cos(4.0 * math.pi * (u - k["apoyo"] / 2.0))     # +1 con el pie de apoyo bajo la cadera
    p = {"raiz_z": -0.020 + 0.010 * bote, "raiz_pitch": 3.0, "raiz_roll": 2.2 * math.sin(a + 0.2),
         "raiz_yaw": -5.0 * math.cos(a), "col_yaw": 4.0 * math.cos(a), "pec_yaw": 5.0 * math.cos(a),
         "col_roll": -1.4 * math.sin(a + 0.2), "pec_roll": -0.8 * math.sin(a + 0.2), "col_pitch": 1.0,
         "pec_pitch": 0.5, "cue_yaw": -2.0 * math.cos(a), "cab_yaw": -2.0 * math.cos(a),
         "cab_pitch": -3.0 + 1.0 * math.cos(4.0 * math.pi * (u - k["apoyo"] / 2.0) + 0.8)}
    for (lado, s), f0 in zip(LADOS, (0.0, 0.5)):
        L = "_" + lado
        pp = (u + f0) % 1.0
        x, z = paso_pie(pp, k["zancada"], k["apoyo"], k["alza"], k["centro"])
        p["pie_x" + L], p["pie_z" + L] = x, z
        p["pie_pitch" + L] = curva(pp, CABECEO_CAMINAR)
        p["pie_y" + L] = -0.012
        br = math.cos(2.0 * math.pi * (u + f0 - 0.04))           # +1 con ESTA pierna delante: su brazo va atras
        p["flex" + L] = -22.0 * br + 2.0
        p["codo" + L] = 16.0 + 9.0 * 0.5 * (1.0 - br)
        p["abd" + L] = -3.0
    return p


def p_correr(u):
    k = CORRER
    a = 2.0 * math.pi * u
    bote = math.cos(4.0 * math.pi * (u - k["apoyo"] / 2.0))     # +1 a mitad del apoyo: es el punto mas bajo
    p = {"raiz_z": -0.034 - 0.020 * bote, "raiz_pitch": 11.0, "raiz_roll": 2.5 * math.sin(a + 0.3),
         "raiz_yaw": -7.0 * math.cos(a), "col_yaw": 6.0 * math.cos(a), "pec_yaw": 8.0 * math.cos(a),
         "col_roll": -1.5 * math.sin(a + 0.3), "pec_roll": -1.0 * math.sin(a + 0.3), "col_pitch": 4.0,
         "pec_pitch": 3.0, "cue_yaw": -3.5 * math.cos(a), "cab_yaw": -3.5 * math.cos(a), "cue_pitch": -5.0,
         "cab_pitch": -9.0 + 1.5 * bote}
    for (lado, s), f0 in zip(LADOS, (0.0, 0.5)):
        L = "_" + lado
        pp = (u + f0) % 1.0
        x, z = paso_pie(pp, k["zancada"], k["apoyo"], k["alza"], k["centro"])
        p["pie_x" + L], p["pie_z" + L] = x, z
        p["pie_pitch" + L] = curva(pp, CABECEO_CORRER)
        p["pie_y" + L] = -0.020
        br = math.cos(2.0 * math.pi * (u + f0 - 0.03))
        p["flex" + L] = -36.0 * br + 8.0
        p["codo" + L] = 80.0 - 10.0 * br
        p["abd" + L] = -7.0
        p["hom_elev" + L] = 3.0
    return p


def p_salto_lunar(u):
    """Flotacion en el aire (el juego lo usa mientras la protagonista no toca el suelo): no eleva la raiz."""
    a = 2.0 * math.pi * u
    s1, c1 = math.sin(a), math.cos(a)
    p = {"raiz_z": 0.010 * s1, "raiz_pitch": -2.0 + 3.0 * s1, "col_pitch": -2.0,
         "pec_pitch": -3.0 + 2.0 * math.sin(a - 0.5), "cab_pitch": -4.0 + 2.0 * math.sin(a - 0.9),
         "pie_x_izq": 0.035 + 0.050 * s1, "pie_z_izq": 0.075 + 0.030 * c1, "pie_pitch_izq": 26.0 + 8.0 * s1,
         "pie_x_der": -0.045 - 0.050 * s1, "pie_z_der": 0.085 - 0.030 * c1, "pie_pitch_der": 30.0 - 8.0 * s1}
    for lado, s in LADOS:
        L = "_" + lado
        p["abd" + L] = 40.0 + 9.0 * math.sin(a - 1.0)
        p["flex" + L] = 6.0 - 7.0 * s * s1
        p["codo" + L] = 22.0 + 6.0 * math.sin(a - 1.6)
        p["hom_elev" + L] = 6.0 + 3.0 * math.sin(a - 1.0)
    return p


AGACHADA = {"raiz_z": -0.185, "raiz_pitch": 22.0, "col_pitch": 22.0, "pec_pitch": 18.0, "cue_pitch": -14.0,
            "cab_pitch": -16.0, "rodilla_abre_izq": 0.30, "rodilla_abre_der": 0.30,
            "flex_izq": 86.0, "abd_izq": -14.0, "codo_izq": 8.0, "hom_adel_izq": 8.0,
            "flex_der": 30.0, "abd_der": 6.0, "codo_der": 25.0, "bolso_fuera": 6.0}
RECOGER = [(0.00, {}), (0.42, AGACHADA),
           (0.58, dict(AGACHADA, flex_izq=90.0, codo_izq=4.0, raiz_z=-0.190)), (1.00, {})]

ARRIBA = {"raiz_z": 0.028, "raiz_pitch": -2.0, "col_pitch": -5.0, "pec_pitch": -6.0, "cue_pitch": -5.0,
          "cab_pitch": -8.0, "pie_pitch_izq": 22.0, "pie_pitch_der": 22.0}
for _lado in ("izq", "der"):
    ARRIBA.update({"hom_elev_" + _lado: 20.0, "abd_" + _lado: 84.0, "flex_" + _lado: 14.0,
                   "codo_lat_" + _lado: 24.0, "mano_lat_" + _lado: 8.0})
ANTICIPA = {"raiz_z": -0.030, "raiz_pitch": 3.0, "col_pitch": 4.0, "cab_pitch": 6.0,
            "abd_izq": -4.0, "abd_der": -4.0, "flex_izq": -8.0, "flex_der": -8.0, "codo_izq": 25.0, "codo_der": 25.0}
CELEBRAR = [(0.00, {}), (0.16, ANTICIPA), (0.46, ARRIBA),
            (0.62, dict(ARRIBA, raiz_z=0.012, abd_izq=80.0, abd_der=80.0, codo_lat_izq=30.0, codo_lat_der=30.0,
                        pie_pitch_izq=10.0, pie_pitch_der=10.0)),
            (0.80, dict(ARRIBA, raiz_z=0.024, abd_izq=85.0, abd_der=85.0, pie_pitch_izq=19.0, pie_pitch_der=19.0)),
            (1.02, dict(ARRIBA, raiz_z=0.004, abd_izq=80.0, abd_der=80.0, pie_pitch_izq=3.0, pie_pitch_der=3.0,
                        cab_pitch=-5.0)),
            (1.40, {})]


def parametros(clip, tiempo, duracion):
    u = tiempo / duracion
    if clip == "reposo":
        return p_reposo(u)
    if clip == "caminar":
        return p_caminar(u)
    if clip == "correr":
        return p_correr(u)
    if clip == "salto_lunar":
        return p_salto_lunar(u)
    if clip == "recoger":
        return entre_claves(tiempo, RECOGER)
    if clip == "celebrar":
        return entre_claves(tiempo, CELEBRAR)
    raise RuntimeError("Clip desconocido: " + clip)


def crear_clips(armadura, cine):
    """Una accion por clip, con una clave por cuadro (interpolacion lineal) y una pista NLA silenciada."""
    reposo_q = {n: armadura.data.bones[n].matrix_local.to_quaternion() for n in HUESOS}
    ad = armadura.animation_data_create()
    clips = []
    for nombre, duracion, ciclico in CLIPS:
        cuadros = int(round(duracion * FPS))
        exigir(abs(cuadros / FPS - duracion) < 1e-9, "La duracion de %s no cae en cuadros enteros" % nombre)
        cine.exceso = 0.0
        poses = []
        for k in range(cuadros + 1):
            kk = k % cuadros if ciclico else k            # el ultimo cuadro de un ciclo es el primero, exacto
            poses.append(cine.construir(parametros(nombre, kk / FPS, duracion)))
        if cine.exceso > 5e-4:
            aviso("%s: a una pierna le faltaron %.1f mm para alcanzar su apoyo" % (nombre, cine.exceso * 1000))
        accion = bpy.data.actions.new(nombre)
        accion.use_fake_user = True
        ranura = accion.slots.new(armadura.id_type, armadura.name)
        bolsa = accion.layers.new("Movimiento").strips.new(type="KEYFRAME").channelbag(ranura, ensure=True)
        tiempos = np.arange(cuadros + 1, dtype=float)

        def escribir(ruta, indice, grupo, valores):
            fc = bolsa.fcurves.new(ruta, index=indice, group_name=grupo)
            fc.keyframe_points.add(len(valores))
            fc.keyframe_points.foreach_set("co", np.column_stack([tiempos, valores]).ravel())
            fc.keyframe_points.foreach_set("interpolation", [1] * len(valores))    # 1 = LINEAR
            fc.update()

        quietos = []
        for n in HUESOS:
            rq = reposo_q[n]
            qs = []
            previo = None
            for pose in poses:
                b = rq.conjugated() @ pose["d"].get(n, Quaternion()) @ rq
                b.normalize()
                if previo is not None and b.dot(previo) < 0.0:
                    b.negate()
                previo = b.copy()
                qs.append(b)
            if ciclico:
                qs[-1] = qs[0].copy()
            giro_max = max(2.0 * math.degrees(math.acos(min(1.0, abs(q.w)))) for q in qs)
            if giro_max < 0.08:
                # Godot descarta al importar las pistas que no se apartan del reposo, y entonces el hueso se
                # queda con la pose del clip anterior: un vaiven imperceptible mantiene viva la pista
                quietos.append(n)
                for k in range(cuadros + 1):
                    f = math.sin((2.0 if ciclico else 1.0) * math.pi * k / cuadros)
                    qs[k] = qs[k] @ Quaternion((1.0, 0.0, 0.0), math.radians(0.12) * f)
                if ciclico:
                    qs[-1] = qs[0].copy()
            ruta = 'pose.bones["%s"].rotation_quaternion' % n
            for i in range(4):
                escribir(ruta, i, n, [q[i] for q in qs])
        # posicion de la raiz: solo la vertical (en ejes locales del hueso)
        rq = reposo_q["cadera"]
        locs = [rq.conjugated() @ pose["t"] for pose in poses]
        if max(abs(pose["t"].z) for pose in poses) < 2e-4:
            for k in range(cuadros + 1):
                f = math.sin((2.0 if ciclico else 1.0) * math.pi * k / cuadros)
                locs[k] = rq.conjugated() @ Vector((0.0, 0.0, 0.0004 * f))
        for i in range(3):
            escribir('pose.bones["cadera"].location', i, "cadera", [v[i] for v in locs])
        pista = ad.nla_tracks.new()
        pista.name = nombre
        tira = pista.strips.new(nombre, 0, accion)
        tira.action_slot = ranura
        tira.action_frame_start, tira.action_frame_end = 0, cuadros
        tira.frame_start, tira.frame_end = 0, cuadros
        tira.extrapolation = "NOTHING"
        tira.blend_type = "REPLACE"
        pista.mute = True
        clips.append({"nombre": nombre, "duracion": duracion, "ciclico": ciclico, "cuadros": cuadros,
                      "accion": accion, "ranura": ranura, "poses": poses, "quietos": quietos})
        log("Clip %-12s %3d cuadros; huesos con vaiven minimo anadido: %s" % (nombre, cuadros, quietos or "ninguno"))
    return clips


def poner_clip(armadura, clip, cuadro):
    ad = armadura.animation_data
    if clip is None:
        ad.action = None
        for pb in armadura.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
    else:
        ad.action = clip["accion"]
        ad.action_slot = clip["ranura"]
    bpy.context.scene.frame_set(int(cuadro))
    bpy.context.view_layer.update()


def posiciones_deformadas(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    ev.to_mesh_clear()
    return co.reshape(-1, 3)


def comprobar_cinematica(armadura, cine, clips):
    """La cinematica propia (con la que se plantan los pies) debe coincidir con la de Blender."""
    peor = 0.0
    for clip in clips:
        for k in (0, clip["cuadros"] // 3, (2 * clip["cuadros"]) // 3):
            poner_clip(armadura, clip, k)
            _, P = cine.directa(clip["poses"][k])
            for n in HUESOS:
                peor = max(peor, (armadura.pose.bones[n].head - P[n]).length)
    poner_clip(armadura, None, 0)
    exigir(peor < 2e-5, "La cinematica propia y la de Blender difieren %.6f m" % peor)
    return peor


# ---------------------------------------------------------------------------------------- exportar

def exportar(ruta, armadura, mallas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_name(ruta.stem + ".validando.glb")
    bpy.ops.object.select_all(action="DESELECT")
    for o in mallas + [armadura]:
        o.select_set(True)
    bpy.context.view_layer.objects.active = armadura
    pistas = list(armadura.animation_data.nla_tracks)
    try:
        for p in pistas:
            p.mute = False
        res = bpy.ops.export_scene.gltf(
            filepath=str(temporal), check_existing=False, export_format="GLB", use_selection=True,
            export_yup=True, export_apply=False, export_texcoords=True, export_normals=True,
            export_tangents=False, export_materials="EXPORT", export_image_format="AUTO",
            export_cameras=False, export_lights=False, export_extras=False,
            export_skins=True, export_def_bones=False, export_leaf_bone=False, export_rest_position_armature=True,
            export_influence_nb=4, export_all_influences=False,
            export_animations=True, export_animation_mode="NLA_TRACKS", export_nla_strips=True,
            export_frame_range=False, export_frame_step=1, export_force_sampling=True,
            export_sampling_interpolation_fallback="LINEAR", export_anim_slide_to_zero=True,
            export_optimize_animation_size=False, export_reset_pose_bones=True,
            export_morph=False, export_morph_animation=False)
        exigir("FINISHED" in res and temporal.is_file(), "El exportador glTF no termino")
    finally:
        for p in pistas:
            p.mute = True
    return temporal


# ---------------------------------------------------------------------------------------- lectura del GLB

TIPOS = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


def leer_glb(ruta):
    datos = Path(ruta).read_bytes()
    magia, version, total = struct.unpack_from("<4sII", datos, 0)
    exigir(magia == b"glTF" and version == 2 and total == len(datos), "Cabecera GLB invalida: %s" % ruta)
    pos, doc, binario = 12, None, None
    while pos < total:
        tam, tipo = struct.unpack_from("<II", datos, pos)
        trozo = datos[pos + 8: pos + 8 + tam]
        pos += 8 + tam
        if tipo == 0x4E4F534A:
            doc = json.loads(trozo)
        elif tipo == 0x004E4942:
            binario = trozo
    exigir(doc is not None and binario is not None, "GLB sin JSON o sin BIN")
    return doc, binario


def accesor(doc, binario, i):
    a = doc["accessors"][i]
    exigir("sparse" not in a, "Accesor disperso no admitido")
    bv = doc["bufferViews"][a["bufferView"]]
    dt = np.dtype(TIPOS[a["componentType"]])
    n = NCOMP[a["type"]]
    ini = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    salto = bv.get("byteStride", dt.itemsize * n)
    if salto == dt.itemsize * n:
        m = np.frombuffer(binario, dtype=dt, count=a["count"] * n, offset=ini).reshape(a["count"], n)
    else:
        m = np.stack([np.frombuffer(binario, dtype=dt, count=n, offset=ini + k * salto) for k in range(a["count"])])
    if a.get("normalized") and dt != np.float32:
        return m.astype(np.float64) / float(np.iinfo(dt).max)
    return m.astype(np.float64) if dt == np.float32 else m.astype(np.int64)


def mat_trs(t, r, s):
    x, y, z, w = r
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M = np.eye(4)
    M[:3, :3] = R * np.asarray(s)[None, :]
    M[:3, 3] = t
    return M


class ModeloGLB:
    """Lo minimo de glTF para evaluar la piel del archivo exportado, como lo hara el motor."""

    def __init__(self, ruta):
        self.doc, self.bin = leer_glb(ruta)
        d = self.doc
        self.nodos = d["nodes"]
        self.padre = {}
        for i, n in enumerate(self.nodos):
            for h in n.get("children", []):
                self.padre[h] = i
        self.orden = sorted(range(len(self.nodos)), key=self.profundidad)
        exigir(len(d.get("skins", [])) == 1, "El GLB debe traer exactamente un skin")
        piel = d["skins"][0]
        self.art = piel["joints"]
        self.nombres = [self.nodos[j].get("name", "") for j in self.art]
        self.inv = accesor(d, self.bin, piel["inverseBindMatrices"]).reshape(-1, 4, 4).transpose(0, 2, 1)
        self.prims = []
        for i, n in enumerate(self.nodos):
            if "mesh" not in n:
                continue
            for pr in d["meshes"][n["mesh"]]["primitives"]:
                at = pr["attributes"]
                exigir("JOINTS_0" in at and "WEIGHTS_0" in at, "Malla sin piel: %s" % n.get("name"))
                exigir("JOINTS_1" not in at, "Mas de 4 influencias por vertice")
                pos = accesor(d, self.bin, at["POSITION"])
                tri = accesor(d, self.bin, pr["indices"]).reshape(-1, 3)
                self.prims.append({"nombre": n.get("name", ""), "pos": pos, "tri": tri,
                                   "art": accesor(d, self.bin, at["JOINTS_0"]),
                                   "pesos": accesor(d, self.bin, at["WEIGHTS_0"]),
                                   "uv": accesor(d, self.bin, at["TEXCOORD_0"]) if "TEXCOORD_0" in at else None})
        self.anims = {}
        for an in d.get("animations", []):
            canales = []
            for c in an["channels"]:
                sm = an["samplers"][c["sampler"]]
                exigir(sm.get("interpolation", "LINEAR") == "LINEAR", "Interpolacion no lineal en " + an["name"])
                canales.append((c["target"]["node"], c["target"]["path"],
                                accesor(d, self.bin, sm["input"]).ravel(), accesor(d, self.bin, sm["output"])))
            tiempos = np.unique(np.concatenate([c[2] for c in canales]).round(6))
            self.anims[an["name"]] = {"canales": canales, "tiempos": tiempos}
        self.orden_anims = [an["name"] for an in d.get("animations", [])]

    def profundidad(self, i):
        n = 0
        while i in self.padre:
            i = self.padre[i]
            n += 1
        return n

    def locales(self, anim=None, t=0.0):
        loc = []
        for n in self.nodos:
            exigir("matrix" not in n, "Nodo con matriz en vez de TRS")
            loc.append([np.array(n.get("translation", (0, 0, 0)), float), np.array(n.get("rotation", (0, 0, 0, 1)), float),
                        np.array(n.get("scale", (1, 1, 1)), float)])
        if anim is not None:
            for nodo, camino, tiempos, valores in self.anims[anim]["canales"]:
                i = int(np.searchsorted(tiempos, t, side="right") - 1)
                i = max(0, min(i, len(tiempos) - 1))
                if i < len(tiempos) - 1 and t > tiempos[i] + 1e-9:
                    f = (t - tiempos[i]) / (tiempos[i + 1] - tiempos[i])
                    a, b = valores[i], valores[i + 1]
                    if camino == "rotation" and np.dot(a, b) < 0:
                        b = -b
                    v = a + (b - a) * f
                else:
                    v = valores[i]
                if camino == "rotation":
                    v = v / np.linalg.norm(v)
                loc[nodo][{"translation": 0, "rotation": 1, "scale": 2}[camino]] = v
        return loc

    def globales(self, loc):
        G = [None] * len(self.nodos)
        for i in self.orden:
            M = mat_trs(*loc[i])
            G[i] = G[self.padre[i]] @ M if i in self.padre else M
        return G

    def piel(self, anim=None, t=0.0):
        """Posiciones deformadas de cada primitiva (lista de matrices n x 3), en coordenadas glTF."""
        G = self.globales(self.locales(anim, t))
        MJ = np.stack([G[j] @ self.inv[k] for k, j in enumerate(self.art)])
        salida = []
        for pr in self.prims:
            M = (pr["pesos"][:, :, None, None] * MJ[pr["art"]]).sum(1)
            p4 = np.concatenate([pr["pos"], np.ones((len(pr["pos"]), 1))], axis=1)
            salida.append(np.einsum("nij,nj->ni", M[:, :3, :], p4))
        return salida, G


def angulo_entre(a, b):
    """Angulo en grados entre dos cuaterniones (x, y, z, w)."""
    return 2.0 * math.degrees(math.acos(min(1.0, abs(float(np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b)))))))


def dimensiones_png(datos):
    exigir(datos[:8] == b"\x89PNG\r\n\x1a\n", "La imagen embebida no es PNG")
    return struct.unpack(">II", datos[16:24])


# ---------------------------------------------------------------------------------------- comprobaciones

def comprobar(ruta_glb, ruta_entrada, g, gb, reg, W_unicos, cuerpo, bolso, armadura, clips):
    inf = {}
    m = ModeloGLB(ruta_glb)
    doc = m.doc
    exigir(m.nombres and set(m.nombres) == set(HUESOS), "Huesos del GLB distintos de los previstos: %s" % m.nombres)
    exigir([a for a in m.orden_anims] and set(m.orden_anims) == {c[0] for c in CLIPS},
           "Clips del GLB distintos de los previstos: %s" % m.orden_anims)
    exigir(len(m.prims) == 2, "Se esperaban 2 primitivas y hay %d" % len(m.prims))
    pc = next(p for p in m.prims if "cuerpo" in p["nombre"])
    pb = next(p for p in m.prims if "bolso" in p["nombre"])
    ij = {n: m.nombres.index(n) for n in HUESOS}
    inf["malla"] = {"triangulos": int(len(pc["tri"]) + len(pb["tri"])), "triangulos_cuerpo": int(len(pc["tri"])),
                    "vertices_glb": int(len(pc["pos"]) + len(pb["pos"])), "huesos": len(m.art),
                    "clips": m.orden_anims}
    imagenes = []
    for im in doc["images"]:
        bv = doc["bufferViews"][im["bufferView"]]
        trozo = m.bin[bv.get("byteOffset", 0): bv.get("byteOffset", 0) + bv["byteLength"]]
        imagenes.append({"nombre": im.get("name"), "tipo": im.get("mimeType"), "bytes": bv["byteLength"],
                         "px": list(dimensiones_png(trozo)) if im.get("mimeType") == "image/png" else None})
    inf["imagenes"] = imagenes
    inf["glb_bytes"] = Path(ruta_glb).stat().st_size

    # a) la malla en reposo es la de entrada
    ent_doc, ent_bin = leer_glb(ruta_entrada)
    mundo = []
    for n in ent_doc["nodes"]:
        if "mesh" not in n:
            continue
        M = mat_trs(n.get("translation", (0, 0, 0)), n.get("rotation", (0, 0, 0, 1)), n.get("scale", (1, 1, 1)))
        for pr in ent_doc["meshes"][n["mesh"]]["primitives"]:
            p = accesor(ent_doc, ent_bin, pr["attributes"]["POSITION"])
            mundo.append(p @ M[:3, :3].T + M[:3, 3])
    ent = np.concatenate(mundo)
    sal = np.concatenate([pc["pos"], pb["pos"]])
    tri_ent = sum(ent_doc["accessors"][pr["indices"]]["count"] // 3
                  for me in ent_doc["meshes"] for pr in me["primitives"])

    def a_la_mas_cercana(a, b):
        peor = 0.0
        for i in range(0, len(a), 512):
            d2 = ((a[i:i + 512, None, :] - b[None, :, :]) ** 2).sum(-1)
            peor = max(peor, float(np.sqrt(d2.min(1)).max()))
        return peor

    reposo, _ = m.piel(None)
    inf["a_reposo"] = {
        "dif_max_salida_a_entrada_m": a_la_mas_cercana(sal, ent),
        "dif_max_entrada_a_salida_m": a_la_mas_cercana(ent, sal),
        "dif_max_piel_reposo_m": float(max(np.abs(reposo[0] - pc["pos"]).max(), np.abs(reposo[1] - pb["pos"]).max())),
        "triangulos_entrada": int(tri_ent), "triangulos_salida": inf["malla"]["triangulos"],
        "caja_min": [float(v) for v in sal.min(0)], "caja_max": [float(v) for v in sal.max(0)],
        "caja_entrada_min": [float(v) for v in ent.min(0)], "caja_entrada_max": [float(v) for v in ent.max(0)],
    }

    # correspondencia de los vertices del GLB con los unicos de Blender (por posicion en reposo)
    def a_blender(p):
        return np.column_stack([p[:, 0], -p[:, 2], p[:, 1]])

    def casar(p, up):
        idx = np.empty(len(p), dtype=np.int64)
        peor = 0.0
        for i in range(0, len(p), 512):
            d2 = ((p[i:i + 512, None, :] - up[None, :, :]) ** 2).sum(-1)
            idx[i:i + 512] = d2.argmin(1)
            peor = max(peor, float(np.sqrt(d2.min(1)).max()))
        return idx, peor

    unico_c, err_c = casar(a_blender(pc["pos"]), g["up"])
    exigir(err_c < 1e-5, "Los vertices del GLB no casan con la malla de Blender (%.6f)" % err_c)
    # pesos exportados frente a los calculados
    Wg = np.zeros((len(pc["pos"]), len(HUESOS)))
    for k in range(4):
        np.add.at(Wg, (np.arange(len(Wg)), np.array([IH[m.nombres[j]] for j in pc["art"][:, k]])), pc["pesos"][:, k])
    inf["pesos"] = {"dif_max_exportado_vs_calculado": float(np.abs(Wg - W_unicos[unico_c]).max()),
                    "suma_min": float(pc["pesos"].sum(1).min()), "suma_max": float(pc["pesos"].sum(1).max())}
    cabeza_glb = reg["cabeza"][unico_c]
    inf["b_cabeza"] = {"vertices_cabeza_y_pelo": int(cabeza_glb.sum()),
                       "no_rigidos": int((Wg[cabeza_glb, IH["cabeza"]] < 0.9999).sum())}
    exigir(np.allclose(pb["pesos"][:, 0], 1.0) and set(np.unique(pb["art"][:, 0])) == {ij["bolso"]},
           "El bolso no quedo rigido a su hueso")

    # aristas (por primitiva) y sus longitudes en reposo
    def aristas(tri):
        a = np.concatenate([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]])
        return np.unique(np.sort(a, axis=1), axis=0)

    ar_c, ar_b = aristas(pc["tri"]), aristas(pb["tri"])
    l0_c = np.linalg.norm(pc["pos"][ar_c[:, 0]] - pc["pos"][ar_c[:, 1]], axis=1)
    l0_b = np.linalg.norm(pb["pos"][ar_b[:, 0]] - pb["pos"][ar_b[:, 1]], axis=1)
    ar_cab = cabeza_glb[ar_c[:, 0]] & cabeza_glb[ar_c[:, 1]]
    suela = {lado: np.where(Wg[:, IH["pie_" + lado]] > 0.999)[0] for lado, _ in LADOS}
    y_suelo = float(sal[:, 1].min())
    tri_c = [tuple(int(v) for v in t) for t in pc["tri"]]

    def dentro_del_cuerpo(pos_c, pos_b):
        arbol = BVHTree.FromPolygons([Vector(v) for v in pos_c], tri_c)
        n, hondo = 0, 0.0
        for v in pos_b:
            loc, nor, _, d = arbol.find_nearest(Vector(v))
            if loc is not None and (Vector(v) - loc).dot(nor) < 0.0:
                n += 1
                hondo = max(hondo, d)
        return n, hondo

    n0, h0 = dentro_del_cuerpo(reposo[0], reposo[1])
    inf["e_bolso"] = {"reposo": {"vertices_dentro": n0, "hondura_max_m": h0, "vertices_bolso": int(len(pb["pos"]))}}
    inf["b_aristas"], inf["d_ciclos"], inf["raiz_plano"], inf["zancadas"], inf["duraciones"] = {}, {}, {}, {}, {}
    inf["c_pies"] = {}
    nodo_cadera = m.art[ij["cadera"]]
    for nombre, duracion, ciclico in CLIPS:
        an = m.anims[nombre]
        tiempos = an["tiempos"]
        inf["duraciones"][nombre] = float(tiempos[-1] - tiempos[0])
        exigir(abs(tiempos[0]) < 1e-6 and abs(tiempos[-1] - duracion) < 1e-4,
               "Duracion de %s: %.4f s (se pedian %.2f)" % (nombre, tiempos[-1] - tiempos[0], duracion))
        # d) cierre: primera y ultima clave de cada canal; raiz sin desplazamiento en el plano
        giro, tras, plano, n_rot = 0.0, 0.0, 0.0, 0
        for nodo, camino, ts, vs in an["canales"]:
            exigir(camino in ("rotation", "translation"), "Canal de %s en %s: no se esperaba" % (camino, nombre))
            if camino == "rotation":
                n_rot += 1
                giro = max(giro, angulo_entre(vs[0], vs[-1]))
            else:
                exigir(nodo == nodo_cadera, "Posicion animada en un hueso que no es la raiz (%s)" % nombre)
                tras = max(tras, float(np.abs(vs[0] - vs[-1]).max()))
                base = np.array(m.nodos[nodo].get("translation", (0, 0, 0)), float)
                plano = max(plano, float(np.abs(vs[:, [0, 2]] - base[[0, 2]]).max()))
        exigir(n_rot == len(HUESOS), "%s trae %d pistas de rotacion (se esperaban %d)" % (nombre, n_rot, len(HUESOS)))
        inf["d_ciclos"][nombre] = {"ciclico": ciclico, "giro_max_grados": giro, "traslacion_max_m": tras}
        inf["raiz_plano"][nombre] = plano
        # b) aristas, c) punto mas bajo, e) bolso, zancada
        peor_frac, peor_razon, peor_cab = 1.0, 0.0, 0.0
        y_min, y_max = 9.0, -9.0
        bolso_n, bolso_h = 0, 0.0
        pies = {lado: [] for lado, _ in LADOS}
        for k, t in enumerate(tiempos):
            (dc, db), _ = m.piel(nombre, float(t))
            rc = np.linalg.norm(dc[ar_c[:, 0]] - dc[ar_c[:, 1]], axis=1) / np.maximum(l0_c, 1e-9)
            rb = np.linalg.norm(db[ar_b[:, 0]] - db[ar_b[:, 1]], axis=1) / np.maximum(l0_b, 1e-9)
            validas = l0_c > 1e-5
            razones = np.concatenate([rc[validas], rb[l0_b > 1e-5]])
            peor_frac = min(peor_frac, float((razones <= 2.2).mean()))
            peor_razon = max(peor_razon, float(razones.max()))
            peor_cab = max(peor_cab, float(np.abs(rc[ar_cab & validas] - 1.0).max()))
            bajo = min(float(dc[:, 1].min()), float(db[:, 1].min()))
            y_min, y_max = min(y_min, bajo), max(y_max, bajo)
            if k % 2 == 0:
                nb_, hb_ = dentro_del_cuerpo(dc, db)
                bolso_n, bolso_h = max(bolso_n, nb_), max(bolso_h, hb_)
            for lado, _ in LADOS:
                pies[lado].append(dc[suela[lado]])
        inf["b_aristas"][nombre] = {"fraccion_min_bajo_2_2": peor_frac, "razon_max": peor_razon,
                                    "deformacion_max_cabeza_pelo": peor_cab, "cuadros": int(len(tiempos))}
        inf["c_pies"][nombre] = {"y_mas_bajo_min": y_min, "y_mas_bajo_max": y_max}
        inf["e_bolso"][nombre] = {"vertices_dentro_max": bolso_n, "hondura_max_m": bolso_h}
        if nombre in ("caminar", "correr"):
            # velocidad hacia atras de los puntos de la suela que tocan el suelo, entre claves consecutivas
            vel, contacto = [], np.zeros(len(tiempos) - 1, dtype=bool)
            for lado, _ in LADOS:
                P = np.stack(pies[lado])
                for k in range(len(tiempos) - 1):
                    b0, b1 = P[k][:, 1].min(), P[k + 1][:, 1].min()
                    if b0 < y_suelo + 0.004 and b1 < y_suelo + 0.004:
                        toca = P[k][:, 1] < b0 + 0.002
                        vel.append(-(P[k + 1][toca, 0] - P[k][toca, 0]).mean() / (tiempos[k + 1] - tiempos[k]))
                        contacto[k] = True
            vel = np.array(vel)
            exigir(len(vel) > 3, "No se detecto apoyo de los pies en " + nombre)
            v_med = float(np.median(vel))
            inf["zancadas"][nombre] = {"zancada_m": v_med * duracion, "velocidad_apoyo_m_s": v_med,
                                       "velocidad_p10": float(np.percentile(vel, 10)),
                                       "velocidad_p90": float(np.percentile(vel, 90)),
                                       "fraccion_del_ciclo_con_apoyo": float(contacto.mean())}

    # la piel de Blender (de donde salen los renders) coincide con la del archivo
    peor = 0.0
    for clip in clips:
        k = clip["cuadros"] // 3
        poner_clip(armadura, clip, k)
        (dc, db), _ = m.piel(clip["nombre"], k / FPS)
        bl = posiciones_deformadas(cuerpo)
        idx_bl = np.zeros(g["nu"], dtype=np.int64)
        idx_bl[g["inv"]] = np.arange(len(g["inv"]))
        peor = max(peor, float(np.abs(a_blender(dc) - bl[idx_bl[unico_c]]).max()))
    poner_clip(armadura, None, 0)
    inf["piel_blender_vs_glb_m"] = peor
    return inf, m


# ---------------------------------------------------------------------------------------- renders

def preparar_render():
    escena = bpy.context.scene
    if escena.world is None:
        escena.world = bpy.data.worlds.new("Fondo")
    escena.world.color = (0.80, 0.78, 0.76)
    escena.render.engine = "BLENDER_WORKBENCH"
    sh = escena.display.shading
    sh.light = "FLAT"
    sh.color_type = "TEXTURE"
    sh.show_xray = False
    escena.view_settings.view_transform = "Standard"
    escena.render.film_transparent = False
    escena.render.image_settings.file_format = "PNG"
    escena.render.resolution_percentage = 100
    datos = bpy.data.cameras.new("Revision")
    datos.type = "ORTHO"
    cam = bpy.data.objects.new("Revision", datos)
    escena.collection.objects.link(cam)
    escena.camera = cam
    return cam


def tomar(cam, centro, direccion, ancho_m, alto_m, ruta, px_por_m=600):
    escena = bpy.context.scene
    cam.location = centro + direccion * 6.0
    arriba = "Y" if abs(direccion.z) < 0.9 else "X"
    cam.rotation_euler = (centro - cam.location).to_track_quat("-Z", arriba).to_euler()
    cam.data.clip_end = 20.0
    escena.render.resolution_x = int(ancho_m * px_por_m)
    escena.render.resolution_y = int(alto_m * px_por_m)
    cam.data.ortho_scale = max(ancho_m, alto_m)
    escena.render.filepath = str(ruta)
    bpy.ops.render.render(write_still=True)
    exigir(Path(ruta).is_file(), "No se guardo el render %s" % ruta)


def renders(carpeta, armadura, cuerpo, bolso, clips, W_unicos, g, art, zs):
    carpeta.mkdir(parents=True, exist_ok=True)
    escena = bpy.context.scene
    cam = preparar_render()
    escritos = []
    instantes = {"reposo": [0.0, 0.25, 0.5, 0.75], "caminar": [i / 8 for i in range(8)],
                 "correr": [i / 8 for i in range(8)], "salto_lunar": [i / 6 for i in range(6)],
                 "recoger": [0.0, 0.2, 0.42, 0.5, 0.75, 1.0], "celebrar": [0.0, 0.11, 0.33, 0.5, 0.73, 1.0]}
    sep = {"reposo": 0.62, "caminar": 0.62, "correr": 0.66, "salto_lunar": 0.86, "recoger": 0.66, "celebrar": 0.90}
    # suelo: una losa fina y oscura para ver el apoyo
    me = bpy.data.meshes.new("suelo")
    X, Y = 12.0, 12.0
    me.from_pydata([(-X, -Y, zs - 0.004), (X, -Y, zs - 0.004), (X, Y, zs - 0.004), (-X, Y, zs - 0.004),
                    (-X, -Y, zs), (X, -Y, zs), (X, Y, zs), (-X, Y, zs)], [],
                   [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
    mat = bpy.data.materials.new("suelo")
    mat.diffuse_color = (0.25, 0.22, 0.20, 1.0)
    me.materials.append(mat)
    suelo = bpy.data.objects.new("suelo", me)
    escena.collection.objects.link(suelo)
    originales = [cuerpo, bolso]
    for o in originales + [armadura]:
        o.hide_render = True

    def copia_posada(desplazamiento):
        dg = bpy.context.evaluated_depsgraph_get()
        copias = []
        for o in originales:
            nueva = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
            ob = bpy.data.objects.new("copia", nueva)
            ob.location = desplazamiento
            escena.collection.objects.link(ob)
            copias.append(ob)
        return copias

    for clip in clips:
        nombre = clip["nombre"]
        for vista, direccion, eje in (("perfil", Vector((0, -1, 0)), Vector((1, 0, 0))),
                                      ("frente", Vector((1, 0, 0)), Vector((0, 1, 0)))):
            copias = []
            fracs = instantes[nombre]
            for i, f in enumerate(fracs):
                k = int(round(f * clip["cuadros"]))
                poner_clip(armadura, clip, k)
                copias += copia_posada(eje * (i * sep[nombre]))
            ancho = (len(fracs) - 1) * sep[nombre] + 0.70
            centro = eje * ((len(fracs) - 1) * sep[nombre] / 2.0) + Vector((0.03, 0.0, 0.07))
            ruta = carpeta / ("%s_%s.png" % (nombre, vista))
            tomar(cam, centro, direccion, ancho, 1.30, ruta, px_por_m=520)
            escritos.append(str(ruta))
            for ob in copias:
                datos = ob.data
                bpy.data.objects.remove(ob, do_unlink=True)
                bpy.data.meshes.remove(datos)
    poner_clip(armadura, None, 0)

    # mapa de pesos (un color por hueso) y esqueleto sobre la malla
    colores = {}
    for i, n in enumerate(HUESOS):
        tono = (i * 0.381966) % 1.0
        k = tono * 6.0
        r, gg, b = [max(0.0, min(1.0, abs(((k + d) % 6.0) - 3.0) - 1.0)) for d in (0.0, 4.0, 2.0)]
        colores[n] = np.array([0.25 + 0.75 * r, 0.25 + 0.75 * gg, 0.25 + 0.75 * b])
    escena.display.shading.color_type = "VERTEX"
    suelo.hide_render = True
    copias = []
    for o, pesos in ((cuerpo, W_unicos[g["inv"]]), (bolso, None)):
        nueva = o.data.copy()
        ob = bpy.data.objects.new("pesos", nueva)
        escena.collection.objects.link(ob)
        if pesos is None:
            rgb = np.tile(colores["bolso"], (len(nueva.vertices), 1))
        else:
            rgb = pesos @ np.stack([colores[n] for n in HUESOS])
        attr = nueva.color_attributes.new("pesos", "FLOAT_COLOR", "POINT")
        attr.data.foreach_set("color", np.column_stack([rgb, np.ones(len(rgb))]).ravel())
        nueva.color_attributes.active_color = attr
        nueva.color_attributes.render_color_index = nueva.color_attributes.find("pesos")
        copias.append(ob)
    for vista, direccion in (("frente", Vector((1, 0, 0))), ("espalda", Vector((-1, 0, 0))),
                             ("derecha", Vector((0, -1, 0))), ("izquierda", Vector((0, 1, 0)))):
        ruta = carpeta / ("pesos_%s.png" % vista)
        tomar(cam, Vector((0.0, 0.0, 0.0)), direccion, 0.80, 1.06, ruta, px_por_m=1000)
        escritos.append(str(ruta))
    # esqueleto: varillas de color sobre la malla en transparencia
    verts, caras = [], []
    for n in HUESOS:
        a, b = art[n]
        eje = (b - a).normalized()
        lado = eje.cross(Vector((0.3, 0.5, 0.8))).normalized()
        otro = eje.cross(lado)
        r = 0.006
        base = len(verts)
        medio = a + (b - a) * 0.15
        verts += [tuple(a), tuple(medio + lado * r), tuple(medio + otro * r), tuple(medio - lado * r),
                  tuple(medio - otro * r), tuple(b)]
        caras += [(base, base + 1, base + 2), (base, base + 2, base + 3), (base, base + 3, base + 4),
                  (base, base + 4, base + 1), (base + 5, base + 2, base + 1), (base + 5, base + 3, base + 2),
                  (base + 5, base + 4, base + 3), (base + 5, base + 1, base + 4)]
    me = bpy.data.meshes.new("varillas")
    me.from_pydata(verts, [], caras)
    attr = me.color_attributes.new("pesos", "FLOAT_COLOR", "POINT")
    attr.data.foreach_set("color", np.tile([0.05, 0.05, 0.9, 1.0], len(verts)))
    varillas = bpy.data.objects.new("varillas", me)
    escena.collection.objects.link(varillas)
    escena.display.shading.show_xray = True
    escena.display.shading.xray_alpha = 0.35
    for vista, direccion in (("frente", Vector((1, 0, 0))), ("derecha", Vector((0, -1, 0)))):
        ruta = carpeta / ("esqueleto_%s.png" % vista)
        tomar(cam, Vector((0.0, 0.0, 0.0)), direccion, 0.80, 1.06, ruta, px_por_m=1000)
        escritos.append(str(ruta))
    escena.display.shading.show_xray = False
    escena.display.shading.color_type = "TEXTURE"
    for ob in copias + [varillas, suelo, cam]:
        bpy.data.objects.remove(ob, do_unlink=True)
    for o in originales + [armadura]:
        o.hide_render = False
    return escritos


# ---------------------------------------------------------------------------------------- principal

def main():
    a = argumentos()
    exigir(bpy.app.version[:2] >= (5, 2), "Se requiere Blender 5.2 o posterior; hay " + bpy.app.version_string)
    cuerpo, bolso, px, textura = importar(a.entrada, a.textura)
    escena = bpy.context.scene
    escena.render.fps, escena.render.fps_base = FPS, 1.0
    escena.frame_start, escena.frame_end = 0, int(max(c[1] for c in CLIPS) * FPS)
    g, gb = geometria(cuerpo), geometria(bolso)
    zs = float(g["co"][:, 2].min())
    alto = float(g["co"][:, 2].max()) - zs
    log("Cuerpo: %d vertices (%d posiciones unicas), %d triangulos; bolso: %d triangulos; alto %.4f m, suelo z = %.4f"
        % (len(g["co"]), g["nu"], g["nt"], gb["nt"], alto, zs))
    reg = clasificar(g, px, zs)
    del px
    art, extra = medir(g, reg, gb, zs)
    W, info_pesos = calcular_pesos(g, reg, art, zs)
    log("Pesos: %s" % json.dumps(info_pesos))
    armadura = crear_armadura(art)
    enlazar(cuerpo, armadura, W[g["inv"]])
    Wb = np.zeros((len(gb["co"]), len(HUESOS)))
    Wb[:, IH["bolso"]] = 1.0
    enlazar(bolso, armadura, Wb)

    suelas = {}
    for lado, _ in LADOS:
        rigidos = reg["piernas"][lado] & (W[:, IH["pie_" + lado]] > 0.999)
        exigir(rigidos.sum() > 40, "Pie %s con pocos vertices rigidos" % lado)
        suelas[lado] = g["up"][rigidos] - np.array(art["pie_" + lado][0])
    cine = Cinematica(art, suelas, zs)
    clips = crear_clips(armadura, cine)
    err_cine = comprobar_cinematica(armadura, cine, clips)
    log("Cinematica propia frente a Blender: %.2e m" % err_cine)

    temporal = exportar(a.salida, armadura, [cuerpo, bolso])
    try:
        informe, modelo = comprobar(temporal, a.entrada, g, gb, reg, W, cuerpo, bolso, armadura, clips)
        temporal.replace(a.salida)
    finally:
        if temporal.exists():
            temporal.unlink()
    informe.update(entrada=str(a.entrada), salida=str(a.salida), blender=bpy.app.version_string, textura=textura,
                   pesos_info=info_pesos, cinematica_propia_vs_blender_m=err_cine, alto_malla_m=alto, fps=FPS)
    log("GLB escrito: %s (%.2f MB)" % (a.salida, informe["glb_bytes"] / 1e6))

    # medidas en unidades del GLB (y = arriba, z = derecha del personaje)
    def gl(v):
        return [round(float(v.x), 4), round(float(v.z), 4), round(float(-v.y), 4)]

    medidas = {
        "alto": 1.0,
        "cadera_y": round(float(art["muslo_izq"][0].z + art["muslo_der"][0].z) / 2.0, 4),
        "cuello_y": round(float(art["cuello"][0].z), 4),
        "hombro_y": round(float(art["brazo_izq"][0].z + art["brazo_der"][0].z) / 2.0, 4),
        "hombro_z": round(float(abs(art["brazo_izq"][0].y) + abs(art["brazo_der"][0].y)) / 2.0, 4),
        "rodilla_y": round(float(art["pierna_izq"][0].z + art["pierna_der"][0].z) / 2.0, 4),
        "zancada_caminar_m": round(informe["zancadas"]["caminar"]["zancada_m"], 4),
        "zancada_correr_m": round(informe["zancadas"]["correr"]["zancada_m"], 4),
        "duraciones": {n: round(informe["duraciones"][n], 4) for n, _, _ in CLIPS},
        "ciclicos": [n for n, _, c in CLIPS if c],
        "alto_malla": round(alto, 4), "suelo_y": round(zs, 4),
        "tobillo_y": round(float(art["pie_izq"][0].z + art["pie_der"][0].z) / 2.0, 4),
        "articulaciones": {n: gl(art[n][0]) for n in HUESOS},
        "nota": "Unidades del GLB (1 m de alto, origen a media altura, mira a +X, derecha +Z). Zancada = avance "
                "por ciclo completo sin que resbale el pie apoyado. Generado por herramientas/blender/rig_protagonista.py.",
    }
    a.medidas.parent.mkdir(parents=True, exist_ok=True)
    a.medidas.write_text(json.dumps(medidas, indent=1, ensure_ascii=False), encoding="utf-8")
    informe["medidas"] = medidas
    if a.renders:
        informe["renders"] = renders(a.renders.resolve(), armadura, cuerpo, bolso, clips, W, g, art, zs)
        log("Renders: %d imagenes en %s" % (len(informe["renders"]), a.renders))
    if a.guardar_blend:
        ruta = a.guardar_blend.resolve()
        ruta.parent.mkdir(parents=True, exist_ok=True)
        bpy.context.preferences.filepaths.save_version = 0
        bpy.ops.wm.save_as_mainfile(filepath=str(ruta), check_existing=False)
        informe["blend"] = str(ruta)
    informe["avisos"] = AVISOS
    if a.informe:
        a.informe.parent.mkdir(parents=True, exist_ok=True)
        a.informe.write_text(json.dumps(informe, indent=1, ensure_ascii=False), encoding="utf-8")
    return informe


if __name__ == "__main__":
    try:
        resumen = main()
        print("RESUMEN_RIG_PROTAGONISTA=" + json.dumps(resumen, ensure_ascii=True, sort_keys=True), flush=True)
    except Exception as exc:
        print("ERROR_RIG_PROTAGONISTA: " + str(exc), file=sys.stderr, flush=True)
        traceback.print_exc()
        raise
