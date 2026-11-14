"""Agrega a la protagonista (PER-01) el bolso de herramientas y la correa cruzada de su hoja de referencia.

La hoja (Lote_02/L02_protagonista_tipo1_hoja.png) lleva un bolso de cuero en la cadera derecha, con un
destornillador de mango naranja, una llave y un alicate asomando, y una correa que cruza el pecho y la
espalda desde el hombro izquierdo. La malla de Tripo se hizo sin bolso (hoja de giro limpia), asi que se
agrega aqui como mallas aparte, con una textura de paleta para que el juego les ponga el shader de personaje.

En la hoja el bolso esta delante de la cadera en el frente y detras en el perfil (la hoja no es coherente):
aqui va en la cadera derecha girado 45 grados hacia delante, para que se lea en las dos vistas.

Uso:
  blender -b --factory-startup --python-exit-code 1 --python herramientas/blender/accesorio_bolso.py -- \
      --entrada <malla.glb> --salida <malla_con_bolso.glb>
Convencion de la malla (glTF): mira a +X, arriba +Y, 1 m de alto centrada en el origen; lado derecho +Z.
En Blender (Z arriba): mira a +X, arriba +Z, lado derecho -Y.
"""
import argparse
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

# paleta (sRGB): cada color ocupa una celda de 4x4 px en una imagen de 16x16
PALETA = {
    "cuero": (0.48, 0.29, 0.16), "cuero_luz": (0.62, 0.40, 0.22), "cuero_osc": (0.33, 0.19, 0.09),
    "correa": (0.42, 0.25, 0.14), "correa_luz": (0.56, 0.35, 0.19), "dorado": (0.85, 0.63, 0.20),
    "naranja": (0.91, 0.45, 0.16), "naranja_luz": (0.98, 0.62, 0.30), "metal": (0.62, 0.64, 0.68),
    "metal_osc": (0.36, 0.38, 0.42), "rojo": (0.78, 0.29, 0.16), "costura": (0.80, 0.66, 0.45),
}


def argumentos():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--entrada", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--angulo", type=float, default=45.0,
                   help="giro del bolso desde el frente hacia el costado derecho, en grados")
    p.add_argument("--sin-correa", action="store_true",
                   help="sin correa 3D: la textura proyectada de la hoja ya la trae pintada")
    return p.parse_args(argv)


def imagen_paleta():
    img = bpy.data.images.new("PER01_accesorios_paleta", 16, 16, alpha=False)
    pix = [0.0] * (16 * 16 * 4)
    celdas = {}
    for k, (nombre, rgb) in enumerate(PALETA.items()):
        cx, cy = (k % 4) * 4, (k // 4) * 4
        # la imagen nueva es sRGB: los pixels van tal cual (pasarlos a lineal los oscurecia dos veces)
        for y in range(cy, cy + 4):
            for x in range(cx, cx + 4):
                i = (y * 16 + x) * 4
                pix[i:i + 4] = [*rgb, 1.0]
        celdas[nombre] = ((cx + 2) / 16, (cy + 2) / 16)
    img.pixels = pix
    img.pack()
    return img, celdas


def material(img):
    mat = bpy.data.materials.new("PER01_accesorios")
    mat.use_nodes = True
    nodos = mat.node_tree.nodes
    bsdf = nodos.get("Principled BSDF")
    tex = nodos.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Closest"
    mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 1.0
    return mat


class Pieza:
    """Malla en construccion con bmesh: caras con su color de paleta (una UV por cara)."""

    def __init__(self, nombre, celdas):
        self.nombre, self.celdas = nombre, celdas
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.new("UVMap")

    def pintar(self, caras, color, claro=None, oscuro=None):
        """Color por cara: las que miran arriba toman 'claro' y las que miran abajo 'oscuro'."""
        for f in caras:
            f.normal_update()
            c = color
            if claro and f.normal.z > 0.55:
                c = claro
            elif oscuro and f.normal.z < -0.45:
                c = oscuro
            u, v = self.celdas[c]
            for loop in f.loops:
                loop[self.uv].uv = (u, v)

    def caja(self, centro, ejes, medios, color, claro=None, oscuro=None, bisel=0.0):
        """Caja orientada: ejes = (u, v, w) ortonormales, medios = semilados."""
        r = bmesh.ops.create_cube(self.bm, size=2.0)
        verts = r["verts"]
        m = Matrix((ejes[0] * medios[0], ejes[1] * medios[1], ejes[2] * medios[2])).transposed()
        for vt in verts:
            vt.co = centro + m @ vt.co
        caras = list({f for vt in verts for f in vt.link_faces})
        if bisel > 0:
            aristas = list({e for f in caras for e in f.edges})
            try:
                res = bmesh.ops.bevel(self.bm, geom=aristas, offset=bisel, segments=1, affect="EDGES",
                                      profile=0.5)
                caras = list(set(caras) | set(res.get("faces", [])))
                caras = [f for f in caras if f.is_valid]
            except Exception as error:  # noqa: BLE001
                print("aviso: sin bisel", error)
        self.pintar(caras, color, claro, oscuro)
        return caras

    def cilindro(self, a, b, radio, lados, color, claro=None):
        eje = (b - a)
        largo = eje.length
        eje.normalize()
        r = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=lados, radius1=radio, radius2=radio, depth=largo)
        rot = eje.to_track_quat("Z", "Y").to_matrix().to_4x4()
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation((a + b) / 2) @ rot, verts=r["verts"])
        caras = list({f for vt in r["verts"] for f in vt.link_faces})
        self.pintar(caras, color, claro)

    def cinta(self, puntos, normales, ancho, color, claro):
        """Cinta sobre la superficie: dos vertices por punto, de cara hacia fuera."""
        verts = []
        for i, (p, n) in enumerate(zip(puntos, normales)):
            t = (puntos[min(i + 1, len(puntos) - 1)] - puntos[max(i - 1, 0)]).normalized()
            lado = t.cross(n).normalized() * (ancho / 2)
            verts.append((self.bm.verts.new(p - lado), self.bm.verts.new(p + lado)))
        caras = []
        for (a0, a1), (b0, b1) in zip(verts[:-1], verts[1:]):
            caras.append(self.bm.faces.new((a0, b0, b1, a1)))
        bmesh.ops.recalc_face_normals(self.bm, faces=caras)
        # que miren hacia fuera del cuerpo: si quedaron al reves, se invierten
        f0 = caras[0]
        f0.normal_update()
        if f0.normal.dot(normales[0]) < 0:
            bmesh.ops.reverse_faces(self.bm, faces=caras)
        self.pintar(caras, color, claro)

    def objeto(self, mat):
        me = bpy.data.meshes.new(self.nombre)
        self.bm.to_mesh(me)
        self.bm.free()
        me.materials.append(mat)
        ob = bpy.data.objects.new(self.nombre, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob


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

    def golpe(origen, direccion):
        hit = bvh.ray_cast(Vector(origen), Vector(direccion).normalized(), 10.0)
        if hit[0] is None:
            raise SystemExit(f"sin superficie desde {origen} hacia {direccion}")
        return hit[0], hit[1]

    img, celdas = imagen_paleta()
    mat = material(img)

    # ---- bolso: cadera derecha (-Y en Blender), girado 45 grados hacia delante (+X) ----
    z_bolso = zmin + 0.40 * H
    ang = math.radians(a.angulo)
    fuera = Vector((math.cos(ang), -math.sin(ang), 0.0))  # 0 = de frente, 90 = costado derecho (-Y)
    p_cadera, n_cadera = golpe(fuera * 2.0 + Vector((0, 0, z_bolso)), -fuera)
    u = fuera.copy()                                   # hondo del bolso (hacia fuera)
    w = Vector((0, 0, 1))
    v = w.cross(u).normalized()                        # a lo largo de la cadera
    hondo, ancho, alto = 0.026, 0.085, 0.065           # semilados (bolso de 17 x 13 x 5 cm)
    centro = p_cadera + u * (hondo + 0.012) + Vector((0, 0, -0.01))
    bolso = Pieza("PER01_bolso", celdas)
    bolso.caja(centro, (u, v, w), (hondo, ancho, alto), "cuero", "cuero_luz", "cuero_osc", bisel=0.008)
    # solapa: cubre la mitad de arriba de la cara de fuera, un poco mas grande
    bolso.caja(centro + u * (hondo + 0.004) + w * (alto * 0.35), (u, v, w), (0.005, ancho * 1.03, alto * 0.62),
               "cuero_osc", "cuero")
    bolso.caja(centro + u * (hondo + 0.011) + w * (alto * 0.0), (u, v, w), (0.004, 0.012, 0.012), "dorado")
    # bolsillo lateral (la hoja muestra uno en el frente del bolso)
    bolso.caja(centro + u * (hondo + 0.006) - v * (ancho * 0.45) - w * (alto * 0.35), (u, v, w),
               (0.006, ancho * 0.32, alto * 0.38), "cuero", "cuero_luz", "cuero_osc")
    # herramientas que asoman por arriba
    tope = centro + w * alto
    bolso.cilindro(tope - v * 0.035 - w * 0.02, tope - v * 0.035 + w * 0.045, 0.0085, 6, "naranja", "naranja_luz")
    bolso.cilindro(tope - v * 0.035 + w * 0.045, tope - v * 0.035 + w * 0.06, 0.004, 5, "metal")
    bolso.caja(tope + v * 0.01 + w * 0.025, (u, v, w), (0.004, 0.006, 0.04), "metal", "metal")       # llave
    bolso.caja(tope + v * 0.01 + w * 0.068, (u, v, w), (0.005, 0.013, 0.008), "metal_osc", "metal")  # boca
    bolso.cilindro(tope + v * 0.045 - w * 0.02, tope + v * 0.04 + w * 0.035, 0.006, 5, "rojo")        # alicate
    bolso.cilindro(tope + v * 0.055 - w * 0.02, tope + v * 0.06 + w * 0.033, 0.006, 5, "rojo")

    # ---- correa: del hombro izquierdo (+Y) al bolso, por delante y por detras ----
    z_hombro = zmin + 0.66 * H
    pegada = 0.006

    def sobre_superficie(y, z, desde):
        """Punto de la superficie en (y, z) visto desde delante (+X) o desde atras (-X). Si el rayo pasa
        de largo (la cintura es angosta), se acerca al eje del cuerpo hasta tocarlo."""
        sx = 1.0 if desde == "frente" else -1.0
        for _ in range(12):
            hit = bvh.ray_cast(Vector((sx * 2.0, y, z)), Vector((-sx, 0, 0)), 10.0)
            if hit[0] is not None:
                return hit[0] + hit[1] * pegada, hit[1]
            y *= 0.85
        raise SystemExit(f"sin superficie en y={y:.3f} z={z:.3f} desde {desde}")

    def recorrido(desde):
        pts, ns = [], []
        destino_y = (centro + v * 0.0).y
        destino_z = tope.z - 0.005
        for i in range(19):
            t = i / 18
            y = (1 - t) * 0.062 + t * (destino_y + (0.035 if desde == "frente" else -0.01))
            z = (1 - t) * z_hombro + t * destino_z
            p, n = sobre_superficie(y, z, desde)
            pts.append(p)
            ns.append(n)
        return pts, ns

    pf, nf = recorrido("frente")
    pb, nb = recorrido("espalda")
    # por encima del hombro: de delante hacia atras, rayos desde arriba
    arco_p, arco_n = [], []
    for i in range(1, 6):
        x = pf[0].x + (pb[0].x - pf[0].x) * i / 6
        p, n = golpe((x, 0.062, zmax + 0.5), (0, 0, -1))
        arco_p.append(p + n * pegada)
        arco_n.append(n)
    puntos = list(reversed(pf)) + arco_p + pb
    normales = list(reversed(nf)) + arco_n + nb
    correa = Pieza("PER01_correa", celdas)
    correa.cinta(puntos, normales, 0.03, "correa", "correa_luz")  # en la hoja la correa mide unos 3 cm
    # hebilla en el pecho
    i_heb = len(pf) // 3
    p_h, n_h = pf[i_heb], nf[i_heb]
    t_h = (pf[i_heb + 1] - pf[i_heb - 1]).normalized()
    correa.caja(p_h + n_h * 0.003, (n_h, t_h.cross(n_h).normalized(), t_h), (0.003, 0.014, 0.012), "dorado")

    ob_bolso = bolso.objeto(mat)
    piezas = [ob_bolso]
    if a.sin_correa:
        correa.bm.free()
    else:
        piezas.append(correa.objeto(mat))
    tris = sum(len(p.vertices) - 2 for o in piezas for p in o.data.polygons)
    print("accesorios: %d triangulos" % tris)

    salida = Path(a.salida).resolve()
    salida.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(salida), export_format="GLB", export_cameras=False,
                              export_lights=False, export_apply=True)
    print("BOLSO_OK", salida)


main()
