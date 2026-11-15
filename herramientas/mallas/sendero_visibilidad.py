"""Zona «sendero»: que ve la camara de juego desde cada foco y que tapa la copa del flamboyan.

La camara de juego (nucleo/camara_juego.gd) es la misma del ancla, pero sigue a la protagonista. Dos cosas
hay que medir antes de fijar los limites de la camara, el cerco y los umbrales:

  1. El suelo que entra en cuadro desde cada foco limite (para saber hasta donde hay que tener decorado).
  2. Si el tronco y la copa de VEG-02 (hasta 3,4 m de alto, entre la camara y el suelo) tapan a la
     protagonista en un punto dado. La copa NO se toca (centro aprobado, D-015): se limita la camara y el paso.

Uso:
  python -I herramientas/mallas/sendero_visibilidad.py                    informe de los limites del layout
  python -I herramientas/mallas/sendero_visibilidad.py mapa <fx> <fz>     mapa de lo tapado con ese foco
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from camara_ancla import Camara  # noqa: E402
from nucleo import rot_y  # noqa: E402
from sendero_ampliacion import leer_glb  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
LAYOUT = RAIZ / "juego" / "zonas" / "sendero" / "layout.json"
MODELOS = RAIZ / "juego" / "modelos"
ENCUADRE = 0.19
W, H = 320, 180


def cargar():
    L = json.loads(LAYOUT.read_text(encoding="utf-8"))
    verts = []
    for r in L["recursos"]:
        if not r["id"].startswith("VEG-02") or "petalos" in r["id"]:
            continue
        for nodo in ("VEG-02_tronco", "VEG-02_copa"):
            V = leer_glb(MODELOS / r["glb"], nodo).astype(float)
            V = V * np.array([r["escala"], r["escala"] * r.get("escala_y", 1.0), r["escala"]])
            verts.append(V @ rot_y(math.radians(r["rot_y"])).T + np.array(r["pos"]))
    return L, np.concatenate(verts)


def camara(L, fx, fz, encuadre=ENCUADRE):
    datos = dict(L["camara"])
    datos["objetivo"] = [fx, 0.0, fz]
    datos["encuadres"] = {"j": encuadre}
    return Camara("j", datos=datos)


def proyectar(cam, P):
    """(u, v, profundidad) de puntos del mundo, con la inclinacion 2.5D."""
    P = np.asarray(P, float).reshape(-1, 3)
    Q = P + np.outer(P[:, 1], [0, 0, -cam.k])
    r = Q - cam.pos
    z = r @ cam.adelante
    u = 0.5 + (r @ cam.derecha) / (z * cam.t * cam.aspecto) / 2
    v = 0.5 - (r @ cam.arriba) / (z * cam.t) / 2
    return u, v, z


def mapa_de_profundidad(cam, V, radio=2):
    u, v, z = proyectar(cam, V)
    prof = np.full((H, W), np.inf)
    ok = (u > -0.05) & (u < 1.05) & (v > -0.05) & (v < 1.05) & (z > 0.1)
    px, py, pz = (u[ok] * W).astype(int), (v[ok] * H).astype(int), z[ok]
    for dx in range(-radio, radio + 1):
        for dy in range(-radio, radio + 1):
            x, y = np.clip(px + dx, 0, W - 1), np.clip(py + dy, 0, H - 1)
            np.minimum.at(prof, (y, x), pz)
    return prof


def tapada(cam, prof, x, z, y_suelo=0.0):
    """Fraccion del cuerpo (pies, cintura, cabeza) tapada o fuera de cuadro; -1 si los pies no entran."""
    alturas = [0.1, 0.55, 1.0]
    u, v, d = proyectar(cam, [(x, y_suelo + h, z) for h in alturas])
    if not (0.02 < u[0] < 0.98 and 0.04 < v[0] < 0.98):
        return -1.0
    mal = 0
    for ui, vi, di in zip(u, v, d):
        if not (0 <= ui < 1 and 0 <= vi < 1):
            mal += 1
            continue
        if prof[int(vi * H), int(ui * W)] < di - 0.3:
            mal += 1
    return mal / len(alturas)


def cuadro_en_suelo(cam):
    return [tuple(round(c, 2) for c in cam.al_suelo(u, v)) for u, v in ((0, 0), (1, 0), (1, 1), (0, 1))]


def main():
    L, V = cargar()
    J = L.get("jugable", {})
    if len(sys.argv) > 3 and sys.argv[1] == "mapa":
        fx, fz = float(sys.argv[2]), float(sys.argv[3])
        cam = camara(L, fx, fz)
        prof = mapa_de_profundidad(cam, V)
        print("foco", fx, fz, "cuadro en el suelo", cuadro_en_suelo(cam))
        xs = np.arange(-6.0, 8.01, 0.5)
        print("        " + "".join("%+d" % int(x) if abs(x - round(x)) < 1e-6 and int(x) % 2 == 0 else "  " for x in xs))
        for z in np.arange(-11.0, 5.01, 0.5):
            fila = ""
            for x in xs:
                t = tapada(cam, prof, x, z)
                fila += "  " if t < 0 else " ." if t == 0 else " o" if t < 0.5 else " #"
            print("%6.1f %s" % (z, fila))
        return
    lim = J["limites"]
    informe = {"encuadre": ENCUADRE, "limites": lim, "focos": {}}
    esquinas = {"NO": (lim["x"][0], lim["z"][0]), "NE": (lim["x"][1], lim["z"][0]),
                "SE": (lim["x"][1], lim["z"][1]), "SO": (lim["x"][0], lim["z"][1])}
    todo = []
    for nombre, (fx, fz) in esquinas.items():
        cam = camara(L, fx, fz)
        c = cuadro_en_suelo(cam)
        todo += c
        informe["focos"][nombre] = {"foco": [fx, fz], "cuadro_en_el_suelo": c}
    todo = np.array(todo)
    informe["suelo_que_entra_en_cuadro"] = {"x": [float(todo[:, 0].min()), float(todo[:, 0].max())],
                                            "z": [float(todo[:, 1].min()), float(todo[:, 1].max())]}
    # la protagonista en cada punto clave, con la camara donde quedaria (foco limitado)
    puntos = {"entrada_casa": J["entrada_casa"], "umbral_ciudad": J["umbral_ciudad"],
              "entrada_mirador": J["entrada_mirador"], "umbral_mirador": J["umbral_mirador"],
              "antena": J["antena"], "panel": J["panel"], "iguana": J["iguana"]}
    for k, p in enumerate(J.get("ruta_norte", [])):
        puntos["ruta_norte_%d" % k] = p
    informe["puntos"] = {}
    for nombre, (x, z) in puntos.items():
        fx = min(max(x, lim["x"][0]), lim["x"][1])
        fz = min(max(z, lim["z"][0]), lim["z"][1])
        cam = camara(L, fx, fz)
        prof = mapa_de_profundidad(cam, V)
        u, v, _ = proyectar(cam, [(x, 0.0, z)])
        informe["puntos"][nombre] = {"pos": [x, z], "foco": [fx, fz], "pantalla_uv": [round(float(u[0]), 3), round(float(v[0]), 3)],
                                     "tapada": tapada(cam, prof, x, z)}
    print(json.dumps(informe, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
