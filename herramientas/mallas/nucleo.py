"""Nucleo comun para generar mallas low-poly pintadas por script (sin Blender).

Estilo (Biblia de arte): facetas planas y nitidas, cada una con un degradado pintado; luz calida,
sombra azul petroleo; solo colores de la paleta maestra. Cada triangulo lleva sus propios vertices
(sombreado plano) y un color por esquina en sRGB, que el GLB guarda en lineal (COLOR_0).

Convenciones del mundo: metros, +Y arriba, la camara de juego mira hacia -Z (lo lejano es -Z).
La protagonista mide 1,05 m (3 cabezas); el gato llega a su rodilla.

Materiales por nombre (la escena de Godot los reemplaza por sus shaders):
  "Facetado"  opaco, color de vertice          "Follaje"  doble cara, color de vertice
  "Agua"      superficie de agua               "Emisivo"  brillo cian (destellos, pantallas)

Uso tipico:
    from nucleo import Malla, Escena, PAL, mezclar, roca
    m = roca(semilla=3)
    e = Escena("TER-01"); e.nodo("TER-01_roca_grande", e.malla(m)); e.guardar("salida.glb")
"""
from __future__ import annotations

import json
import math
import struct
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]

# Paleta maestra (Biblia de arte, seccion 3). Se comprueba contra paleta_maestra.json al importar.
HEX = {
    "crema": "#F8C991", "sol": "#F4A159", "dorado": "#DAAA25",
    "tierra1": "#D09880", "tierra2": "#AF795E", "terracota": "#924930", "coral": "#E46043",
    "hierba_sol": "#A48A29", "hierba_sombra": "#6D6A2B",
    "madera1": "#836258", "madera2": "#583F22",
    "petroleo": "#516B7C", "piedra_osc": "#4B4E47", "piedra": "#998385", "piedra_clara": "#B8BBC6",
    "oscuro": "#322C1D", "cian": "#62E4E0", "cian_medio": "#36B1B2", "brillo": "#CEF8F5",
}
PAL = {k: np.array([int(v[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]) for k, v in HEX.items()}


def _comprobar_paleta():
    ruta = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "paleta_maestra.json"
    if ruta.exists():
        oficiales = {c["hex"].upper() for c in json.loads(ruta.read_text(encoding="utf-8"))["colores"]}
        faltan = {k for k, v in HEX.items() if v.upper() not in oficiales}
        assert not faltan, f"colores fuera de la paleta maestra: {faltan}"


_comprobar_paleta()


def mezclar(a, b, t):
    return np.asarray(a, float) * (1.0 - t) + np.asarray(b, float) * t


def srgb_a_lineal(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def rot_y(ang):
    c, s = math.cos(ang), math.sin(ang)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_eje(eje, ang):
    """Matriz de rotacion de Rodrigues alrededor de un eje unitario."""
    eje = np.asarray(eje, float) / np.linalg.norm(eje)
    x, y, z = eje
    c, s, t = math.cos(ang), math.sin(ang), 1 - math.cos(ang)
    return np.array([[t * x * x + c, t * x * y - s * z, t * x * z + s * y],
                     [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
                     [t * x * z - s * y, t * y * z + s * x, t * z * z + c]])


class Malla:
    """Triangulos sueltos con color sRGB por esquina; normales de cara salvo que se den."""

    def __init__(self, nombre: str, material: str = "Facetado"):
        self.nombre, self.material = nombre, material
        self.P: list[np.ndarray] = []
        self.C: list[np.ndarray] = []
        self.N: list[np.ndarray | None] = []

    def __len__(self):
        return len(self.P)

    def tri(self, a, b, c, ca, cb=None, cc=None, normales=None):
        cb = ca if cb is None else cb
        cc = ca if cc is None else cc
        self.P.append(np.array([a, b, c], float))
        self.C.append(np.clip(np.array([ca, cb, cc], float), 0, 1))
        self.N.append(None if normales is None else np.array(normales, float))

    def quad(self, a, b, c, d, ca, cb=None, cc=None, cd=None):
        """a-b-c-d en sentido antihorario visto desde fuera."""
        cb = ca if cb is None else cb
        cc = ca if cc is None else cc
        cd = ca if cd is None else cd
        self.tri(a, b, c, ca, cb, cc)
        self.tri(a, c, d, ca, cc, cd)

    def anexar(self, otra: "Malla", R=None, t=(0, 0, 0), s=1.0):
        """Copia los triangulos de otra malla, rotados (R 3x3), escalados y trasladados."""
        R = np.eye(3) if R is None else np.asarray(R, float)
        t = np.asarray(t, float)
        for P, C, N in zip(otra.P, otra.C, otra.N):
            self.P.append((P * s) @ R.T + t)
            self.C.append(C.copy())
            self.N.append(None if N is None else N @ R.T)

    def caja_limites(self):
        P = np.array(self.P).reshape(-1, 3)
        return P.min(0), P.max(0)

    def arrays(self):
        P = np.array(self.P).reshape(-1, 3)
        C = np.array(self.C).reshape(-1, 3)
        N = []
        for tri, n in zip(self.P, self.N):
            if n is None:
                fn = np.cross(tri[1] - tri[0], tri[2] - tri[0])
                fn /= max(np.linalg.norm(fn), 1e-12)
                N.append(np.tile(fn, (3, 1)))
            else:
                N.append(n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12))
        return P, np.array(N).reshape(-1, 3), C


# ---------- geometria ----------

def fibonacci(n):
    """n puntos casi uniformes sobre la esfera unidad."""
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)], 1)


def casco_convexo(pts: np.ndarray):
    """Casco convexo por fuerza bruta (para n < 64): triangulos (i, j, k) antihorarios hacia fuera."""
    n = len(pts)
    centro = pts.mean(0)
    caras = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                nrm = np.cross(pts[j] - pts[i], pts[k] - pts[i])
                largo = np.linalg.norm(nrm)
                if largo < 1e-9:
                    continue
                d = (pts - pts[i]) @ (nrm / largo)
                d[[i, j, k]] = 0.0
                if np.all(d <= 1e-7):
                    caras.append((i, j, k))
                elif np.all(d >= -1e-7):
                    caras.append((i, k, j))
    # orientar hacia fuera respecto del centro (por si hay casi coplanares)
    salida = []
    for i, j, k in caras:
        nrm = np.cross(pts[j] - pts[i], pts[k] - pts[i])
        salida.append((i, j, k) if nrm @ (pts[i] - centro) >= 0 else (i, k, j))
    return salida


def degradado_cara(tri, ymin, ymax, sombra, base, luz, var=1.0):
    """Degradado pintado por esquina: oscuro abajo, base en medio, luz arriba."""
    cols = []
    for p in tri:
        t = (p[1] - ymin) / max(ymax - ymin, 1e-6)
        c = mezclar(sombra, base, min(1.0, t * 1.7)) if t < 0.6 else mezclar(base, luz, (t - 0.6) / 0.4)
        cols.append(np.asarray(c) * var)
    return cols


def solido_facetado(nombre, pts, sombra, base, luz, rng, var=0.06, encima=None, material="Facetado"):
    """Casco convexo de pts pintado con degradado vertical; 'encima' = (color, umbral_normal_y, desde_t)."""
    caras = casco_convexo(pts)
    m = Malla(nombre, material)
    ymin, ymax = pts[:, 1].min(), pts[:, 1].max()
    for (i, j, k) in caras:
        tri = pts[[i, j, k]]
        n = np.cross(tri[1] - tri[0], tri[2] - tri[0])
        n /= np.linalg.norm(n)
        cols = degradado_cara(tri, ymin, ymax, sombra, base, luz, 1.0 + rng.normal(0, var))
        if encima is not None and n[1] > encima[1]:
            for q, p in enumerate(tri):
                t = (p[1] - ymin) / max(ymax - ymin, 1e-6)
                if t > encima[2]:
                    cols[q] = mezclar(cols[q], encima[0], min(1.0, (t - encima[2]) / 0.12))
        m.tri(*tri, *cols)
    return m


def roca(nombre="roca", semilla=0, escala=(1.0, 0.7, 0.9), npts=18, musgo=True):
    """Roca tallada: pocos puntos irregulares, base plana y musgo en la coronilla."""
    rng = np.random.default_rng(semilla)
    pts = fibonacci(npts) * rng.uniform(0.72, 1.15, (npts, 1)) * np.array(escala) * 0.5
    piso = pts[:, 1].min() * 0.5
    bajos = pts[:, 1] < piso
    pts[bajos, 1] = piso + rng.uniform(0, 0.006, bajos.sum())
    pts[:, 1] -= pts[:, 1].min()
    base = PAL["piedra"]
    sombra, luz = mezclar(base, PAL["petroleo"], 0.6), mezclar(base, PAL["tierra1"], 0.5)
    enc = (PAL["hierba_sol"], 0.72, 0.78) if musgo else None
    return solido_facetado(nombre, pts, sombra, base, luz, rng, encima=enc)


def marco(tangente):
    """Dos vectores perpendiculares a la tangente (para anillos de tubos)."""
    t = np.asarray(tangente, float) / np.linalg.norm(tangente)
    ref = np.array([0, 1, 0]) if abs(t[1]) < 0.9 else np.array([1, 0, 0])
    u = np.cross(t, ref)
    u /= np.linalg.norm(u)
    return u, np.cross(t, u)


def tubo(m: Malla, centros, radios, lados, col_bajo, col_alto, rng, torsion=0.0, ruido=0.12, tapa=True):
    """Tronco, rama, raiz o barra: anillos perpendiculares a la polilinea, unidos por quads."""
    centros = [np.asarray(c, float) for c in centros]
    anillos = []
    for idx, (c, r) in enumerate(zip(centros, radios)):
        tang = (centros[min(idx + 1, len(centros) - 1)] - centros[max(idx - 1, 0)])
        u, v = marco(tang)
        ang = np.arange(lados) / lados * 2 * math.pi + idx * torsion
        rr = r * rng.uniform(1 - ruido, 1 + ruido, lados)
        anillos.append(c + np.outer(np.cos(ang) * rr, u) + np.outer(np.sin(ang) * rr, v))
    total = len(anillos) - 1
    for a in range(total):
        t0, t1 = a / total, (a + 1) / total
        for s in range(lados):
            s2 = (s + 1) % lados
            p0, p1, p2, p3 = anillos[a][s], anillos[a][s2], anillos[a + 1][s2], anillos[a + 1][s]
            var = 1 + rng.normal(0, 0.05)
            c0, c1 = mezclar(col_bajo, col_alto, t0) * var, mezclar(col_bajo, col_alto, t1) * var
            m.quad(p0, p1, p2, p3, c0, c0, c1, c1)
    if tapa:
        fin = anillos[-1]
        cen = fin.mean(0)
        for s in range(lados):
            m.tri(cen, fin[s], fin[(s + 1) % lados], col_alto)
    return m


def caja(m: Malla, p0, p1, col, sombra_t=0.35, luz_t=0.0, rng=None, var=0.04, sin_base=True):
    """Prisma recto entre p0 y p1 (esquinas opuestas), con degradado vertical en los lados."""
    v = 1 + (rng.normal(0, var) if rng is not None else 0)
    col = np.asarray(col, float)
    bajo = mezclar(col, PAL["petroleo"], sombra_t) * v
    alto = mezclar(col, PAL["crema"], luz_t) * v
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    P = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1],
                  [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], float)
    for a, b, c, d in [(0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]:
        m.quad(P[a], P[b], P[c], P[d], bajo, alto, alto, bajo)
    m.quad(P[4], P[7], P[6], P[5], alto)
    if not sin_base:
        m.quad(P[0], P[1], P[2], P[3], bajo)
    return m


def hoja(m: Malla, base, direccion, normal, largo, ancho, col_base, col_punta, doblez=0.25):
    """Hoja en rombo con nervio doblado (4 triangulos); normales hacia 'normal' (follaje)."""
    d = np.asarray(direccion, float) / np.linalg.norm(direccion)
    n = np.asarray(normal, float) / np.linalg.norm(normal)
    lado = np.cross(n, d)
    lado /= max(np.linalg.norm(lado), 1e-9)
    base = np.asarray(base, float)
    medio = base + d * largo * 0.45
    punta = base + d * largo
    i = medio + lado * ancho * 0.5 - n * ancho * doblez
    o = medio - lado * ancho * 0.5 - n * ancho * doblez
    cm = mezclar(col_base, col_punta, 0.45)
    nn = [n, n, n]
    m.tri(base, i, medio, col_base, cm, cm, nn)
    m.tri(base, medio, o, col_base, cm, cm, nn)
    m.tri(medio, i, punta, cm, cm, col_punta, nn)
    m.tri(medio, punta, o, cm, col_punta, cm, nn)


def flor(m: Malla, centro, normal, radio, col_petalo, col_centro, petalos=5, rng=None):
    """Flor plana de petalos triangulares con centro de otro color."""
    n = np.asarray(normal, float) / np.linalg.norm(normal)
    u, v = marco(n)
    centro = np.asarray(centro, float)
    giro = rng.uniform(0, 2 * math.pi) if rng is not None else 0.0
    nn = [n, n, n]
    for k in range(petalos):
        a0 = giro + k / petalos * 2 * math.pi
        a1 = a0 + 2 * math.pi / petalos * 0.5
        a2 = a0 - 2 * math.pi / petalos * 0.5
        punta = centro + (u * math.cos(a0) + v * math.sin(a0)) * radio
        p1 = centro + (u * math.cos(a1) + v * math.sin(a1)) * radio * 0.45
        p2 = centro + (u * math.cos(a2) + v * math.sin(a2)) * radio * 0.45
        m.tri(centro, p1, punta, col_centro, col_petalo, col_petalo, nn)
        m.tri(centro, punta, p2, col_centro, col_petalo, col_petalo, nn)


# ---------- escritura GLB ----------

class Escena:
    """Escribe un .glb (glTF 2.0 binario) con mallas, materiales por nombre y nodos."""

    DOBLE_CARA = {"Follaje", "Agua"}

    def __init__(self, generador="herramientas/mallas"):
        self.bin = bytearray()
        self.doc = {"asset": {"version": "2.0", "generator": generador},
                    "buffers": [], "bufferViews": [], "accessors": [], "meshes": [], "nodes": [],
                    "materials": [], "scenes": [{"nodes": []}], "scene": 0}
        self._mat = {}
        self.stats = {}

    def _material(self, nombre):
        if nombre not in self._mat:
            self._mat[nombre] = len(self.doc["materials"])
            self.doc["materials"].append({
                "name": nombre, "doubleSided": nombre in self.DOBLE_CARA,
                "pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1], "metallicFactor": 0.0,
                                         "roughnessFactor": 0.9}})
        return self._mat[nombre]

    def _accessor(self, arr, comp, tipo, target, minmax=False):
        data = arr.tobytes()
        while len(self.bin) % 4:
            self.bin.append(0)
        off = len(self.bin)
        self.bin += data
        self.doc["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": len(data), "target": target})
        acc = {"bufferView": len(self.doc["bufferViews"]) - 1, "componentType": comp,
               "count": int(arr.shape[0]), "type": tipo}
        if minmax:
            acc["min"] = arr.min(0).tolist()
            acc["max"] = arr.max(0).tolist()
        self.doc["accessors"].append(acc)
        return len(self.doc["accessors"]) - 1

    def malla(self, *mallas: Malla, nombre=None):
        """Una malla glTF con una primitiva por material."""
        prims, total = [], 0
        for m in mallas:
            if not len(m):
                continue
            P, N, C = m.arrays()
            lin = np.concatenate([srgb_a_lineal(C), np.ones((len(C), 1))], 1).astype(np.float32)
            idx = np.arange(len(P), dtype=np.uint32)
            prims.append({"attributes": {
                "POSITION": self._accessor(P.astype(np.float32), 5126, "VEC3", 34962, True),
                "NORMAL": self._accessor(N.astype(np.float32), 5126, "VEC3", 34962),
                "COLOR_0": self._accessor(lin, 5126, "VEC4", 34962)},
                "indices": self._accessor(idx, 5125, "SCALAR", 34963),
                "material": self._material(m.material)})
            total += len(P) // 3
        nombre = nombre or mallas[0].nombre
        self.doc["meshes"].append({"name": nombre, "primitives": prims})
        self.stats[nombre] = total
        return len(self.doc["meshes"]) - 1

    def nodo(self, nombre, malla=None, t=(0, 0, 0), rot_y_rad=0.0, s=1.0, padre=None):
        q = [0.0, math.sin(rot_y_rad / 2), 0.0, math.cos(rot_y_rad / 2)]
        s3 = [float(s)] * 3 if np.isscalar(s) else [float(v) for v in s]
        nodo = {"name": nombre, "translation": [float(v) for v in t], "rotation": q, "scale": s3}
        if malla is not None:
            nodo["mesh"] = malla
        self.doc["nodes"].append(nodo)
        idx = len(self.doc["nodes"]) - 1
        if padre is None:
            self.doc["scenes"][0]["nodes"].append(idx)
        else:
            self.doc["nodes"][padre].setdefault("children", []).append(idx)
        return idx

    def guardar(self, ruta):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        while len(self.bin) % 4:
            self.bin.append(0)
        self.doc["buffers"] = [{"byteLength": len(self.bin)}]
        js = json.dumps(self.doc, separators=(",", ":")).encode("utf-8")
        js += b" " * ((4 - len(js) % 4) % 4)
        total = 12 + 8 + len(js) + 8 + len(self.bin)
        with open(ruta, "wb") as f:
            f.write(struct.pack("<III", 0x46546C67, 2, total))
            f.write(struct.pack("<II", len(js), 0x4E4F534A))
            f.write(js)
            f.write(struct.pack("<II", len(self.bin), 0x004E4942))
            f.write(bytes(self.bin))
        return ruta
