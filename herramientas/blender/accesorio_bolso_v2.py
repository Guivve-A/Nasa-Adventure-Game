"""Bolso de herramientas v2 de la protagonista (PER-01): bolsa de cuero pintada como la de la hoja.

Mejora de accesorio_bolso.py (v8T llevaba una caja plana de color uniforme). Aqui:
  - forma: bolsa de cuero con esquinas redondeadas (bisel de 2 segmentos), boca abierta con borde y
    fondo interior, fuelle lateral (pliegue hacia dentro en los costados), solapa delantera con borde
    inferior curvo que cubre la mitad de arriba, bolsillo delantero con su tapa, hebilla dorada y dos
    argollas doradas arriba de los costados (la correa pintada llega a la de delante);
  - pintura: la cara delantera (cuerpo, solapa y bolsillo) lleva los pixeles de la bolsa del frente de la
    hoja, enderezados con una homografia y proyectados con UV planas; las caras que la hoja no muestra
    llevan degradados de la paleta de la bolsa (medida en la propia hoja), claro arriba y oscuro abajo,
    con costuras claras pintadas;
  - herramientas: destornillador de mango naranja grueso con brillo, llave de boca abierta y alicates
    con mandibulas abiertas (mangos ambar como en la hoja; --mangos rojo para mangos rojos).
Sigue colgando en la cadera derecha girado 45 grados hacia delante, como en v8T, sin correa 3D.

Uso:
  blender -b --factory-startup --python-exit-code 1 --python herramientas/blender/accesorio_bolso_v2.py -- \
      --entrada <malla.glb> --salida <malla_con_bolso.glb> [--atlas <png>] [--info <json>]
Convencion de la malla (glTF): mira a +X, arriba +Y, 1 m de alto centrada en el origen; lado derecho +Z.
En Blender (Z arriba): mira a +X, arriba +Z, lado derecho -Y.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

RAIZ = Path(__file__).resolve().parents[2]
HOJA = RAIZ / "Nasa_Game/Fase_1_Arte/Exploracion/Lote_02/L02_protagonista_tipo1_hoja.png"

# bolsa en el frente de la hoja (px de la hoja, 2688x1520): esquinas de la cara delantera
# (sup. izq., sup. der., inf. der., inf. izq.) y del bolsillo, medidas sobre un recorte ampliado con reticula
CARA_HOJA = [(325, 531), (384, 546), (371, 624), (308, 604)]
BOLSILLO_HOJA = [(321, 552), (369, 563), (360, 604), (317, 598)]
FONDO_HOJA = (0xc8 / 255, 0xb8 / 255, 0xaf / 255)  # gris del fondo de la hoja

# medidas del personaje en la hoja (frente): alto 897 px (filas 25 a 922), eje en x = 447
#   bolsa: centro a 0,386 del alto desde los pies y a 0,113 del alto hacia su derecha
ALTURA_REL = 0.386
LATERAL_REL = 0.113

ATLAS = 512
# baldosas del atlas en px (x, y desde arriba, ancho, alto)
BALDOSAS = {
    "frente": (0, 0, 256, 256),
    "cuero": (256, 0, 64, 256), "cuero_osc": (320, 0, 64, 256), "tan": (384, 0, 64, 256),
    "interior": (448, 0, 64, 256),
    "naranja": (0, 256, 64, 256), "metal": (64, 256, 64, 256), "ambar": (128, 256, 64, 256),
    "rojo": (192, 256, 64, 256), "dorado": (256, 256, 64, 256), "hebilla": (320, 256, 64, 256),
    "oscuro": (384, 256, 64, 256),
}
COSTURA = np.array([0.86, 0.72, 0.50])


def argumentos():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--entrada", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--angulo", type=float, default=45.0,
                   help="giro del bolso desde el frente hacia el costado derecho, en grados")
    p.add_argument("--ancho", type=float, default=0.115, help="ancho de la bolsa (m, malla de 1 m)")
    p.add_argument("--alto", type=float, default=0.100, help="alto de la bolsa")
    p.add_argument("--hondo", type=float, default=0.044, help="fondo de la bolsa (fuelle)")
    p.add_argument("--altura", type=float, default=ALTURA_REL, help="centro de la bolsa, fraccion del alto")
    p.add_argument("--lateral", type=float, default=LATERAL_REL,
                   help="distancia del centro al eje del cuerpo vista de frente, fraccion del alto")
    p.add_argument("--deslizar", type=float, default=0.020,
                   help="corre el bolso a lo largo de la cadera hacia delante y al centro (m): acerca su argolla "
                        "a la punta de la correa pintada")
    p.add_argument("--tolerancia", type=int, default=3,
                   help="puntos de la espalda del bolso (de 25) que pueden quedar dentro del cuerpo")
    p.add_argument("--mangos", choices=("hoja", "rojo"), default="hoja",
                   help="color de los mangos de los alicates: ambar de la hoja o rojo")
    p.add_argument("--atlas", help="guarda tambien la textura del bolso en este PNG")
    p.add_argument("--info", help="guarda en este JSON la posicion y las medidas del bolso")
    return p.parse_args(argv)


# ------------------------------------------------------------------ textura

def homografia(origen, destino):
    """H 3x3 que lleva los 4 puntos de origen a los 4 de destino."""
    filas = []
    for (x, y), (X, Y) in zip(origen, destino):
        filas.append([x, y, 1, 0, 0, 0, -X * x, -X * y, -X])
        filas.append([0, 0, 0, x, y, 1, -Y * x, -Y * y, -Y])
    _, _, vt = np.linalg.svd(np.array(filas, float))
    h = vt[-1].reshape(3, 3)
    return h / h[2, 2]


def aplicar(h, pts):
    pts = np.asarray(pts, float)
    q = np.c_[pts, np.ones(len(pts))] @ h.T
    return q[:, :2] / q[:, 2:3]


def leer_hoja():
    img = bpy.data.images.load(str(HOJA), check_existing=True)
    w, h = img.size
    px = np.empty(w * h * 4, np.float32)
    img.pixels.foreach_get(px)  # imagen de 8 bits: valores sRGB tal cual, filas desde abajo
    return px.reshape(h, w, 4)[::-1, :, :3].copy()


def muestrear(hoja, xs, ys):
    """Bilineal: xs, ys en px de la hoja (filas desde arriba)."""
    x0 = np.clip(np.floor(xs).astype(int), 0, hoja.shape[1] - 2)
    y0 = np.clip(np.floor(ys).astype(int), 0, hoja.shape[0] - 2)
    fx, fy = (xs - x0)[..., None], (ys - y0)[..., None]
    a, b = hoja[y0, x0], hoja[y0, x0 + 1]
    c, d = hoja[y0 + 1, x0], hoja[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def rellenar(img, mascara, vueltas=200):
    """Rellena por difusion los pixeles marcados con el promedio de sus vecinos validos."""
    img, m = img.copy(), mascara.copy()
    for _ in range(vueltas):
        if not m.any():
            break
        validos = (~m).astype(np.float32)
        suma = np.zeros_like(img)
        cuenta = np.zeros(m.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            suma += np.roll(np.roll(img * validos[..., None], dy, 0), dx, 1)
            cuenta += np.roll(np.roll(validos, dy, 0), dx, 1)
        nuevos = m & (cuenta > 0)
        img[nuevos] = suma[nuevos] / cuenta[nuevos][:, None]
        m &= ~nuevos
    return img


def baldosa_frente(hoja, lado):
    """La cara delantera de la bolsa de la hoja, enderezada a un cuadrado de lado x lado."""
    h = homografia([(0, 0), (1, 0), (1, 1), (0, 1)], CARA_HOJA)
    s, t = np.meshgrid((np.arange(lado) + 0.5) / lado, (np.arange(lado) + 0.5) / lado)
    xy = aplicar(h, np.c_[s.ravel(), t.ravel()])
    cara = muestrear(hoja, xy[:, 0], xy[:, 1]).reshape(lado, lado, 3)
    r, g, b = cara[..., 0], cara[..., 1], cara[..., 2]
    fondo = np.abs(cara - np.array(FONDO_HOJA)).sum(2) < 0.10
    # puntas de las herramientas que bajan por delante del borde: naranja vivo, ambar o metal azulado
    herramienta = (((r > 0.80) & (b < 0.36)) | ((b >= r) & (b > 0.30))) & (t < 0.30)
    # argollas doradas de la hoja en los bordes: el modelo 3D lleva las suyas
    argolla = (r > 0.80) & (g > 0.50) & (b < 0.40) & ((s < 0.15) | (s > 0.85))
    cara = rellenar(cara, fondo | herramienta | argolla)
    return cara, h


def degradado(alto, ancho, arriba, abajo, ruido=0.035, semilla=0):
    t = np.linspace(0, 1, alto)[:, None, None]
    base = np.array(arriba)[None, None] * (1 - t) + np.array(abajo)[None, None] * t
    base = np.repeat(base, ancho, 1)
    rng = np.random.default_rng(semilla)
    # manchas suaves de pincel: suma de ondas de baja frecuencia
    yy, xx = np.mgrid[0:alto, 0:ancho] / 64.0
    mancha = np.zeros((alto, ancho))
    for _ in range(5):
        fx, fy, fase = rng.uniform(0.5, 3.0), rng.uniform(0.5, 3.0), rng.uniform(0, 6.3)
        mancha += np.sin(xx * fx * 6.3 + yy * fy * 6.3 + fase)
    return np.clip(base * (1 + ruido * mancha[..., None] / 2.5), 0, 1)


def costura(img, puntos, color=COSTURA, paso=7, largo=4, grosor=1, alfa=0.85):
    """Costura discontinua sobre una polilinea de px (x, y)."""
    acum = 0.0
    for (x0, y0), (x1, y1) in zip(puntos[:-1], puntos[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0)))
        for k in range(n):
            if (acum % paso) < largo:
                x = int(round(x0 + (x1 - x0) * k / n))
                y = int(round(y0 + (y1 - y0) * k / n))
                img[max(0, y - grosor + 1):y + grosor, max(0, x - grosor + 1):x + grosor] = (
                    img[max(0, y - grosor + 1):y + grosor, max(0, x - grosor + 1):x + grosor] * (1 - alfa)
                    + np.asarray(color) * alfa)
            acum += 1


def perfil_brillo(ancho, base, borde, brillo, centro=0.36, medio=0.07):
    """Baldosa de mango: oscuro en los bordes, base al medio y una franja de brillo."""
    x = np.linspace(0, 1, ancho)
    redondez = 1 - (2 * x - 1) ** 2
    col = np.array(borde)[None] * (1 - redondez[:, None]) + np.array(base)[None] * redondez[:, None]
    franja = np.clip(1 - np.abs(x - centro) / medio, 0, 1) ** 1.5
    col = col * (1 - franja[:, None]) + np.array(brillo)[None] * franja[:, None]
    return col


def pintar_atlas(hoja, s_flap, t_flap, rect_bolsillo):
    atlas = np.zeros((ATLAS, ATLAS, 3), np.float32)

    def poner(nombre, img):
        x, y, w, h = BALDOSAS[nombre]
        atlas[y:y + h, x:x + w] = img

    lado = BALDOSAS["frente"][2]
    cara, h = baldosa_frente(hoja, lado)
    # paleta de la bolsa medida en la hoja: cuero del cuerpo (fuera del bolsillo) y cuero claro del bolsillo
    s, t = np.meshgrid((np.arange(lado) + 0.5) / lado, (np.arange(lado) + 0.5) / lado)
    s0, t0, s1, t1 = rect_bolsillo
    en_bolsillo = (s > s0) & (s < s1) & (t > t0) & (t < t1)
    nucleo = (s > 0.1) & (s < 0.9) & (t > 0.1) & (t < 0.9)
    cuero = np.median(cara[nucleo & ~en_bolsillo], 0)
    tan = np.median(cara[en_bolsillo & (s > s0 + 0.05) & (s < s1 - 0.05) & (t > t0 + 0.05) & (t < t1 - 0.05)], 0)
    # costuras claras: borde curvo de la solapa y contorno del bolsillo, en px de la baldosa
    curva = [(int(sx * lado), int(ty * lado)) for sx, ty in zip(s_flap, t_flap)]
    curva_dentro = [(x, y - 5) for x, y in curva]
    costura(cara, curva_dentro, alfa=0.55)
    m = 5
    contorno = [(s0 * lado + m, t0 * lado + m), (s1 * lado - m, t0 * lado + m), (s1 * lado - m, t1 * lado - m),
                (s0 * lado + m, t1 * lado - m), (s0 * lado + m, t0 * lado + m)]
    costura(cara, contorno, alfa=0.35)
    poner("frente", cara)

    def baldosa_cuero(arriba, abajo, semilla):
        img = degradado(256, 64, arriba, abajo, semilla=semilla)
        costura(img, [(5, 3), (5, 252)])
        costura(img, [(58, 3), (58, 252)])
        costura(img, [(5, 6), (58, 6)])
        costura(img, [(5, 249), (58, 249)])
        return img

    poner("cuero", baldosa_cuero(np.clip(cuero * 1.30, 0, 1), cuero * 0.62, 1))
    poner("cuero_osc", baldosa_cuero(cuero * 1.05, cuero * 0.55, 2))
    img = degradado(256, 64, np.clip(tan * 1.15, 0, 1), tan * 0.70, semilla=3)
    costura(img, [(5, 3), (5, 252)], alfa=0.6)
    costura(img, [(58, 3), (58, 252)], alfa=0.6)
    poner("tan", img)
    poner("interior", degradado(256, 64, cuero * 0.45, cuero * 0.18, semilla=4))
    poner("oscuro", degradado(256, 64, cuero * 0.70, cuero * 0.45, semilla=5))

    def mango(base, borde, brillo, arriba=1.10, abajo=0.85):
        fila = perfil_brillo(64, base, borde, brillo)
        t = np.linspace(arriba, abajo, 256)[:, None, None]
        return np.clip(fila[None] * t, 0, 1)

    poner("naranja", mango((0.97, 0.44, 0.04), (0.66, 0.22, 0.02), (1.0, 0.80, 0.55)))
    poner("metal", mango((0.58, 0.61, 0.68), (0.32, 0.34, 0.40), (0.92, 0.94, 0.97)))
    poner("ambar", mango((0.95, 0.60, 0.08), (0.66, 0.36, 0.03), (1.0, 0.88, 0.55)))
    poner("rojo", mango((0.80, 0.20, 0.12), (0.50, 0.10, 0.06), (1.0, 0.62, 0.50)))
    poner("dorado", mango((0.86, 0.64, 0.20), (0.56, 0.38, 0.08), (1.0, 0.92, 0.60)))
    heb = np.repeat(np.repeat(np.array([[[0.86, 0.64, 0.20]]]), 256, 0), 64, 1)
    heb[40:216, 14:50] = (0.24, 0.13, 0.07)                       # hueco de la hebilla (cuero oscuro)
    heb[40:216, 29:35] = (0.95, 0.80, 0.42)                       # lengueta
    heb[:20] *= 1.10
    heb[236:] *= 0.80
    poner("hebilla", np.clip(heb, 0, 1))
    return atlas, h, {"cuero_rgb": np.round(cuero * 255).tolist(), "tan_rgb": np.round(tan * 255).tolist()}


def uv_baldosa(nombre, fx, fy, margen=2):
    """fx, fy en [0, 1] dentro de la baldosa (fy desde arriba) -> UV de Blender."""
    x, y, w, h = BALDOSAS[nombre]
    fx = min(max(fx, 0.0), 1.0)
    fy = min(max(fy, 0.0), 1.0)
    px = x + margen + fx * (w - 2 * margen)
    py = y + margen + fy * (h - 2 * margen)
    return px / ATLAS, 1 - py / ATLAS


# ------------------------------------------------------------------ geometria (marco local: x=u fuera, y=v, z=w)

class Bolso:
    def __init__(self):
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.new("UVMap")

    def cerrar(self, caras):
        caras = [f for f in caras if f.is_valid]
        bmesh.ops.recalc_face_normals(self.bm, faces=caras)
        for f in caras:
            f.normal_update()
        return caras

    def uv_planar(self, caras, nombre, eje_x, eje_y, x0, x1, y_arriba, y_abajo):
        for f in caras:
            for lp in f.loops:
                p = lp.vert.co
                fx = (p.dot(eje_x) - x0) / (x1 - x0)
                fy = (y_arriba - p.dot(eje_y)) / (y_arriba - y_abajo)
                lp[self.uv].uv = uv_baldosa(nombre, fx, fy)

    def prisma(self, contorno, origen, ea, eb, en, grosor):
        """Contorno 2D (a, b) en el plano (ea, eb), extruido 'grosor' hacia en. Pieza cerrada."""
        delante = [self.bm.verts.new(origen + ea * a + eb * b + en * grosor) for a, b in contorno]
        detras = [self.bm.verts.new(origen + ea * a + eb * b) for a, b in contorno]
        caras = [self.bm.faces.new(delante), self.bm.faces.new(list(reversed(detras)))]
        n = len(contorno)
        for i in range(n):
            j = (i + 1) % n
            caras.append(self.bm.faces.new((detras[i], detras[j], delante[j], delante[i])))
        res = bmesh.ops.triangulate(self.bm, faces=caras[:2], quad_method="BEAUTY", ngon_method="EAR_CLIP")
        caras = caras[2:] + list(res["faces"])
        return self.cerrar(caras)

    def tubo(self, puntos, radios, lados, ref):
        """Anillos a lo largo de una polilinea, con tapas. ref: direccion de referencia del angulo 0."""
        anillos = []
        for i, (p, r) in enumerate(zip(puntos, radios)):
            t = (puntos[min(i + 1, len(puntos) - 1)] - puntos[max(i - 1, 0)]).normalized()
            a = (ref - t * ref.dot(t)).normalized()
            b = t.cross(a)
            anillos.append([self.bm.verts.new(p + (a * math.cos(2 * math.pi * k / lados)
                                                   + b * math.sin(2 * math.pi * k / lados)) * r)
                            for k in range(lados)])
        caras = []
        for r0, r1 in zip(anillos[:-1], anillos[1:]):
            for k in range(lados):
                j = (k + 1) % lados
                caras.append(self.bm.faces.new((r0[k], r0[j], r1[j], r1[k])))
        tapas = [self.bm.faces.new(list(reversed(anillos[0]))), self.bm.faces.new(anillos[-1])]
        res = bmesh.ops.triangulate(self.bm, faces=tapas, quad_method="BEAUTY", ngon_method="EAR_CLIP")
        return self.cerrar(caras + list(res["faces"]))

    def uv_mango(self, caras, nombre, a, b, lado_dir, radio):
        """UV de mango: x = posicion a traves del mango vista de frente, y = a lo largo (arriba = claro)."""
        eje = (b - a)
        largo = eje.length
        eje.normalize()
        for f in caras:
            for lp in f.loops:
                p = lp.vert.co - a
                fx = 0.5 + p.dot(lado_dir) / (2.2 * radio)
                fy = 1 - p.dot(eje) / largo
                lp[self.uv].uv = uv_baldosa(nombre, fx, fy)


def seccion(hd, ha, rc, pliegue, seg=2):
    """Corte horizontal de la bolsa: rectangulo redondeado (u, v) con el fuelle hundido en los costados."""
    rc = max(rc, 0.0015)
    pts = []
    centros = [(hd - rc, ha - rc, 0), (-(hd - rc), ha - rc, 90), (-(hd - rc), -(ha - rc), 180),
               (hd - rc, -(ha - rc), 270)]
    for k, (cu, cv, a0) in enumerate(centros):
        for i in range(seg + 1):
            ang = math.radians(a0 + 90 * i / seg)
            pts.append((cu + rc * math.cos(ang), cv + rc * math.sin(ang)))
        if k == 0:
            pts.append((0.0, ha - pliegue))       # fuelle del costado +v
        elif k == 2:
            pts.append((0.0, -(ha - pliegue)))    # fuelle del costado -v
    return pts


def cuerpo_bolsa(bolso, hd, ha, hh, bisel, rc, pliegue, borde, hondo_boca):
    bm = bolso.bm
    niveles = []
    for k in range(3):  # bisel del fondo, 2 segmentos
        th = math.radians(45 * k)
        e = bisel * (1 - math.sin(th))
        niveles.append((e, -hh + bisel * (1 - math.cos(th))))
    niveles.append((0.0, hh))                                  # boca (borde de fuera)
    niveles.append((borde, hh))                                # borde de dentro
    niveles.append((borde, hh - hondo_boca))                   # fondo visible del interior
    anillos = []
    for e, z in niveles:
        pts = seccion(hd - e, ha - e, rc - e, max(pliegue - e * 0.5, 0.0015))
        anillos.append([bm.verts.new((u, v, z)) for u, v in pts])
    exteriores, interiores = [], []
    for i, (r0, r1) in enumerate(zip(anillos[:-1], anillos[1:])):
        n = len(r0)
        for k in range(n):
            j = (k + 1) % n
            f = bm.faces.new((r0[k], r0[j], r1[j], r1[k]))
            (interiores if i >= 4 else exteriores).append(f)
    abajo = bm.faces.new(list(reversed(anillos[0])))
    fondo = bm.faces.new(anillos[-1])
    res = bmesh.ops.triangulate(bm, faces=[abajo, fondo], quad_method="BEAUTY", ngon_method="EAR_CLIP")
    nuevas = list(res["faces"])
    todas = bolso.cerrar(exteriores + interiores + nuevas)
    tapa_abajo = [f for f in nuevas if f.normal.z < -0.5]
    fondo_dentro = [f for f in nuevas if f.normal.z > 0.5]
    return todas, set(interiores) | set(fondo_dentro), set(tapa_abajo)


def main():
    a = argumentos()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(Path(a.entrada).resolve()))
    cuerpo = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    dg = bpy.context.evaluated_depsgraph_get()
    verts, polys = [], []
    for o in cuerpo:
        me = o.evaluated_get(dg).to_mesh()
        me.transform(o.matrix_world)
        base = len(verts)
        verts += [v.co.copy() for v in me.vertices]
        polys += [[base + i for i in p.vertices] for p in me.polygons]
        o.evaluated_get(dg).to_mesh_clear()
    bvh = BVHTree.FromPolygons(verts, polys)
    zmin = min(v.z for v in verts)
    zmax = max(v.z for v in verts)
    H = zmax - zmin
    print("cuerpo: alto %.3f m, z de %.3f a %.3f" % (H, zmin, zmax))

    hd, ha, hh = a.hondo / 2, a.ancho / 2, a.alto / 2
    ang = math.radians(a.angulo)
    u = Vector((math.cos(ang), -math.sin(ang), 0.0))  # 0 = de frente, 90 = costado derecho (-Y)
    w = Vector((0, 0, 1))
    v = w.cross(u).normalized()                       # derecha de la cara vista de frente

    # ---- posicion: altura de la hoja; se aleja de la cadera hasta que la espalda del bolso no la corte ----
    zc = zmin + a.altura * H
    hit = bvh.ray_cast(u * 2.0 + Vector((0, 0, zc)), -u, 10.0)
    if hit[0] is None:
        raise SystemExit("sin cadera a la altura del bolso")
    p_cadera = Vector((hit[0].x, hit[0].y, zc))

    def dentro(p):
        loc, nor, _, _ = bvh.find_nearest(p)
        return loc is not None and (p - loc).dot(nor) < 0

    def corta(c):
        """Puntos de la espalda del bolso que quedan dentro del cuerpo."""
        n = 0
        for i in range(5):
            for j in range(5):
                q = c - u * hd + v * (ha * (2 * i / 4 - 1) * 0.85) + w * (hh * (2 * j / 4 - 1) * 0.85)
                n += dentro(q)
        return n

    t_lat = (a.lateral * H + p_cadera.y) / max(-u.y, 1e-3)   # -y del centro = lateral pedido
    t = max(hd + 0.004, t_lat)
    desliz = v * a.deslizar
    print("cadera (%.3f, %.3f), t lateral %.3f, puntos dentro al inicio %d"
          % (p_cadera.x, p_cadera.y, t_lat, corta(p_cadera + u * t + desliz)))
    while corta(p_cadera + u * t + desliz) > a.tolerancia and t < 0.2:
        t += 0.002
    centro = p_cadera + u * t + desliz
    print("bolso: centro (%.3f, %.3f, %.3f), %.1f cm fuera de la cadera, lateral %.3f (pedido %.3f)"
          % (*centro, t * 100, -centro.y, a.lateral * H))

    # ---- textura ----
    hoja = leer_hoja()
    # bolsillo de la hoja en coordenadas de la cara (s, t en [0, 1], t desde arriba)
    h_cara = homografia([(0, 0), (1, 0), (1, 1), (0, 1)], CARA_HOJA)
    st = aplicar(np.linalg.inv(h_cara), BOLSILLO_HOJA)
    s0, s1 = float((st[0, 0] + st[3, 0]) / 2), float((st[1, 0] + st[2, 0]) / 2)
    t0, t1 = float((st[0, 1] + st[1, 1]) / 2), float((st[2, 1] + st[3, 1]) / 2)
    print("bolsillo en la cara: s %.2f-%.2f, t %.2f-%.2f" % (s0, s1, t0, t1))
    # solapa: cubre la mitad de arriba; borde inferior curvo (mas bajo al centro)
    t_lado, t_centro = 0.36, 0.45  # en la hoja el borde de la solapa queda a 0,37 del alto en los lados
    n_curva = 9
    s_flap = [i / (n_curva - 1) for i in range(n_curva)]
    t_flap = [t_lado + (t_centro - t_lado) * math.sin(math.pi * s) ** 1.2 for s in s_flap]
    atlas, _, paleta = pintar_atlas(hoja, s_flap, t_flap, (s0, t0, s1, t1))

    img = bpy.data.images.new("PER01_bolso_v2", ATLAS, ATLAS, alpha=False)
    rgba = np.concatenate([atlas, np.ones((ATLAS, ATLAS, 1), np.float32)], 2)[::-1]
    img.pixels.foreach_set(rgba.astype(np.float32).ravel())  # imagen nueva sRGB: valores tal cual
    img.pack()
    if a.atlas:
        ruta = Path(a.atlas).resolve()
        ruta.parent.mkdir(parents=True, exist_ok=True)
        copia = img.copy()
        copia.filepath_raw = str(ruta)
        copia.file_format = "PNG"
        copia.save()
    mat = bpy.data.materials.new("PER01_bolso_v2")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Linear"
    mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 1.0

    # ---- geometria en el marco local (x = fuera, y = derecha de la cara, z = arriba) ----
    X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    b = Bolso()

    def proyectar_frente(caras, otra, umbral=0.45):
        """Caras que miran hacia fuera: pixeles de la hoja en UV planas; el resto, la baldosa 'otra'."""
        for f in caras:
            if f.normal.x > umbral:
                b.uv_planar([f], "frente", Y, -Z, -ha, ha, -hh, hh)
            elif abs(f.normal.y) >= abs(f.normal.x) and abs(f.normal.y) >= abs(f.normal.z):
                b.uv_planar([f], otra, X if f.normal.y > 0 else -X, Z, -hd if f.normal.y > 0 else hd,
                            hd if f.normal.y > 0 else -hd, hh, -hh)
            elif f.normal.z > 0.6:
                b.uv_planar([f], otra, Y, -X, -ha, ha, -hd, hd)
            elif f.normal.z < -0.6:
                b.uv_planar([f], "oscuro", Y, X, -ha, ha, -hd, hd)
            else:
                b.uv_planar([f], otra, -Y, Z, -ha, ha, hh, -hh)

    # cuerpo
    caras, interior, abajo = cuerpo_bolsa(b, hd, ha, hh, bisel=0.010, rc=0.011, pliegue=0.007,
                                          borde=0.004, hondo_boca=0.030)
    fuera = [f for f in caras if f not in interior and f not in abajo]
    proyectar_frente(fuera, "cuero")
    b.uv_planar(list(interior), "interior", Y, Z, -ha, ha, hh, hh - 0.03)
    b.uv_planar(list(abajo), "oscuro", Y, X, -ha, ha, -hd, hd)
    n_cuerpo = len(caras)

    # solapa: cara delantera de arriba, borde inferior curvo
    def st_a_local(s, t_):
        return (-ha + 2 * ha * s, hh - 2 * hh * t_)

    # sup. der. -> borde curvo de derecha a izquierda -> sup. izq.
    contorno = [st_a_local(1.0, 0.0)] + [st_a_local(s, t_) for s, t_ in
                                          zip(reversed(s_flap), reversed(t_flap))] + [st_a_local(0.0, 0.0)]
    # la solapa no pasa de las esquinas redondeadas de la bolsa (6 mm por costado), para no quedar al aire
    contorno = [(min(max(y, -ha + 0.006), ha - 0.006), z) for y, z in contorno]
    solapa = b.prisma(contorno, X * (hd + 0.0004), Y, Z, X, 0.0030)
    proyectar_frente(solapa, "cuero_osc")

    # bolsillo (donde lo dibuja la hoja) y su tapa
    y0, z1 = st_a_local(s0, t0)
    y1, z0 = st_a_local(s1, t1)
    bm_h = 0.0045

    def rect_redondeado(ya, yb, za, zb, r, seg=2):
        pts = []
        esquinas = [(yb - r, za + r, 270), (yb - r, zb - r, 0), (ya + r, zb - r, 90), (ya + r, za + r, 180)]
        for cy, cz, a0 in esquinas:
            for i in range(seg + 1):
                an = math.radians(a0 + 90 * i / seg)
                pts.append((cy + r * math.cos(an), cz + r * math.sin(an)))
        return pts

    bolsillo = b.prisma(rect_redondeado(y0, y1, z0, z1, 0.004), X * (hd + 0.0004), Y, Z, X, 0.0060)
    proyectar_frente(bolsillo, "tan")
    # tapa del bolsillo: 45 % de arriba, borde inferior curvo
    zt = z1 - 0.45 * (z1 - z0)
    tapa = [(y1, z1), (y0, z1)]
    for i in range(7):
        s = i / 6
        yy = y0 + (y1 - y0) * s
        tapa.append((yy, zt - 0.004 * math.sin(math.pi * s)))
    tapa = [(min(max(y, y0 + 0.0008), y1 - 0.0008), min(z, z1 - 0.0008)) for y, z in tapa]
    tapa_caras = b.prisma(tapa, X * (hd + 0.0060), Y, Z, X, 0.0022)
    proyectar_frente(tapa_caras, "tan")
    # hebilla dorada en el cierre de la tapa
    yh = (y0 + y1) / 2
    hebilla = b.prisma(rect_redondeado(yh - 0.0055, yh + 0.0055, zt - 0.0085, zt + 0.0035, 0.0015, 1),
                       X * (hd + 0.0080), Y, Z, X, 0.0020)
    for f in hebilla:
        if f.normal.x > 0.5:
            b.uv_planar([f], "hebilla", Y, -Z, yh - 0.0055, yh + 0.0055, -(zt + 0.0035), -(zt - 0.0085))
        else:
            b.uv_planar([f], "dorado", Y, Z, yh - 0.0055, yh + 0.0055, zt + 0.0035, zt - 0.0085)
    # argollas doradas arriba de los costados (la correa pintada llega a la de la derecha de la cara)
    argollas = []
    for lado in (-1, 1):
        cy = lado * (ha - 0.0015)
        za, zb = hh - 0.007, hh + 0.005
        anillo = [(-0.0045, za), (0.0045, za), (0.0035, zb), (-0.0035, zb)]
        caras_a = b.prisma(anillo, Y * cy + X * 0.004, X, Z, Y * lado, 0.0018)
        for f in caras_a:
            # cara de fuera: marco dorado con hueco (baldosa de hebilla); cantos dorados
            nombre = "hebilla" if abs(f.normal.y) > 0.5 else "dorado"
            b.uv_planar([f], nombre, X, Z, 0.004 - 0.0045, 0.004 + 0.0045, zb, za)
        argollas += caras_a

    # ---- herramientas (salen de la boca; plano de la cara para que se lean de frente) ----
    boca = hh - 0.028  # arrancan dentro de la bolsa
    # destornillador: mango naranja grueso con brillo, mango arriba como en la hoja
    pd = Vector((0.15 * hd, -0.38 * ha, 0.0))
    inclina = Vector((0, -0.10, 1)).normalized()
    a0 = pd + Z * boca
    puntos = [a0 + inclina * d for d in (0.0, 0.013, 0.064, 0.075, 0.081)]
    radios = [0.0074, 0.0100, 0.0100, 0.0086, 0.0050]
    mango = b.tubo(puntos, radios, 8, X)
    b.uv_mango(mango, "naranja", puntos[0], puntos[-1], Y, 0.0100)
    vastago = b.tubo([a0 - inclina * 0.022, a0 + inclina * 0.002], [0.0019, 0.0019], 4, X)
    b.uv_mango(vastago, "metal", a0 - inclina * 0.022, a0, Y, 0.0019)

    # llave de boca abierta, detras, un poco inclinada
    L, ancho_l, R = 0.052, 0.0040, 0.0110
    yc = L + R * 0.6
    llave = [(-ancho_l, 0.0), (ancho_l, 0.0), (ancho_l, L)]
    for g in (-55, -20, 20, 50):
        an = math.radians(g)
        llave.append((R * math.cos(an), yc + R * math.sin(an)))
    llave += [(0.0036, yc + R * 0.35), (0.0036, yc + R * 0.15), (-0.0036, yc + R * 0.15), (-0.0036, yc + R * 0.35)]
    for g in (130, 160, 200, 235):
        an = math.radians(g)
        llave.append((R * math.cos(an), yc + R * math.sin(an)))
    llave.append((-ancho_l, L))
    rot = math.radians(14)  # inclinada hacia fuera, a la izquierda del destornillador vista de frente
    eje_a = Vector((0, math.cos(rot), math.sin(rot)))
    eje_b = Vector((0, -math.sin(rot), math.cos(rot)))
    o_llave = Vector((-0.30 * hd, -0.55 * ha, boca - 0.002))
    llave_caras = b.prisma(llave, o_llave, eje_a, eje_b, X, 0.0028)
    for f in llave_caras:
        for lp in f.loops:
            p = lp.vert.co - o_llave
            lp[b.uv].uv = uv_baldosa("metal", 0.5 + p.dot(eje_a) / (2.4 * R), 1 - p.dot(eje_b) / (yc + R))

    # alicates: mangos que salen de la boca, eje y mandibulas abiertas en V
    pa = Vector((0.05 * hd, 0.45 * ha, 0.0))
    giro = math.radians(8)
    arriba = Vector((0, -math.sin(giro), math.cos(giro)))
    lado_al = Vector((0, math.cos(giro), math.sin(giro)))
    eje_al = pa + Z * (hh + 0.026)
    color_mango = "ambar" if a.mangos == "hoja" else "rojo"
    alicates = []
    for s_ in (-1, 1):
        base = eje_al - arriba * 0.050 + lado_al * (s_ * 0.0085)
        medio = eje_al - arriba * 0.022 + lado_al * (s_ * 0.0058)
        tope = eje_al - arriba * 0.004 + lado_al * (s_ * 0.0020)
        m = b.tubo([base, medio, tope], [0.0054, 0.0060, 0.0042], 5, X)
        b.uv_mango(m, color_mango, base, tope, lado_al, 0.0060)
        alicates += m
        # mandibula: del eje hacia arriba y afuera, afinando (abiertas en V, como en la hoja)
        j0 = eje_al + lado_al * (-s_ * 0.0012)
        j1 = eje_al + arriba * 0.018 + lado_al * (s_ * 0.0078)
        j2 = eje_al + arriba * 0.036 + lado_al * (s_ * 0.0130)
        mj = b.tubo([j0, j1, j2], [0.0055, 0.0045, 0.0024], 4, X)
        b.uv_mango(mj, "metal", j0, j2, lado_al, 0.0055)
        alicates += mj
    perno = b.tubo([eje_al - X * 0.0040, eje_al + X * 0.0040], [0.0050, 0.0050], 6, Y)
    b.uv_mango(perno, "metal", eje_al - X * 0.0040, eje_al + X * 0.0040, Y, 0.0050)

    # ---- al mundo ----
    base_m = Matrix((u, v, w)).transposed().to_4x4()
    bmesh.ops.transform(b.bm, matrix=Matrix.Translation(centro) @ base_m, verts=b.bm.verts)
    bmesh.ops.triangulate(b.bm, faces=b.bm.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
    me = bpy.data.meshes.new("PER01_bolso")
    b.bm.to_mesh(me)
    b.bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new("PER01_bolso", me)
    bpy.context.scene.collection.objects.link(ob)
    tris = len(me.polygons)
    print("bolso v2: %d triangulos (cuerpo %d caras antes de triangular)" % (tris, n_cuerpo))

    salida = Path(a.salida).resolve()
    salida.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(salida), export_format="GLB", export_cameras=False,
                              export_lights=False, export_apply=True)
    if a.info:
        Path(a.info).write_text(json.dumps({
            "centro_blender": [round(c, 4) for c in centro], "angulo": a.angulo,
            "medidas_m": {"ancho": a.ancho, "alto": a.alto, "hondo": a.hondo},
            "triangulos": tris, "bolsillo_st": [round(s0, 3), round(t0, 3), round(s1, 3), round(t1, 3)],
            "paleta_hoja": paleta, "mangos_alicates": a.mangos}, indent=1), encoding="utf-8")
    print("BOLSO_OK", salida, tris)


main()
