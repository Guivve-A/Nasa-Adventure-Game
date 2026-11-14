"""Camara de la escena de exploracion en Python: proyecta puntos del mundo a la pantalla y al reves.

Reproduce `_colocar_camara()` de pruebas/escena_exploracion/escena.gd (encuadre, distancia, foco) y la
inclinacion de los shaders (z -= k * y). Sirve para colocar recursos donde los pinta el ancla: se mide el
pixel en la imagen aprobada y se obtiene el punto del suelo que cae ahi.

Uso como modulo:
    from camara_ancla import Camara
    c = Camara()                      # lee layout.json, encuadre 21
    c.a_pantalla((x, y, z))           # -> (u, v) normalizados, 0..1 desde arriba a la izquierda
    c.al_suelo(u, v, y=0.0)           # -> (x, z) del punto a esa altura que se ve en (u, v)
Uso como programa:  python herramientas/camara_ancla.py u v [y]
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
LAYOUT = RAIZ / "pruebas" / "escena_exploracion" / "layout.json"


class Camara:
    def __init__(self, encuadre="21", aspecto=16 / 9, layout=LAYOUT, datos=None):
        c = datos if datos is not None else json.loads(Path(layout).read_text(encoding="utf-8"))["camara"]
        self.k = float(c["inclinacion_objetos"])
        inc = math.radians(float(c["inclinacion_deg"]))
        self.fov = math.radians(float(c["fov_deg"]))  # vertical, como Camera3D (keep_height)
        self.aspecto = aspecto
        alto = float(c["alto_personaje"])
        fraccion = float(c["encuadres"][encuadre])
        factor = math.cos(inc) + self.k * math.sin(inc)
        dist = alto * factor / (2 * fraccion * math.tan(self.fov / 2))
        obj = np.array(c["objetivo"], float)
        self.foco = obj + np.array([0, alto / 2, -self.k * alto / 2])
        d = np.array([0, math.sin(inc), math.cos(inc)])
        self.pos = self.foco + d * dist
        self.adelante = -d
        self.derecha = np.array([1.0, 0, 0])
        self.arriba = np.cross(self.derecha, self.adelante)
        self.t = math.tan(self.fov / 2)

    def a_pantalla(self, p, inclinar=True):
        p = np.array(p, float)
        if inclinar:
            p = p + np.array([0, 0, -self.k * p[1]])
        r = p - self.pos
        z = r @ self.adelante
        u = 0.5 + (r @ self.derecha) / (z * self.t * self.aspecto) / 2
        v = 0.5 - (r @ self.arriba) / (z * self.t) / 2
        return float(u), float(v)

    def al_suelo(self, u, v, y=0.0):
        rayo = (self.adelante + self.derecha * (2 * u - 1) * self.t * self.aspecto
                - self.arriba * (2 * v - 1) * self.t)
        s = (y - self.pos[1]) / rayo[1]
        q = self.pos + rayo * s
        return float(q[0]), float(q[2] + self.k * y)  # deshace la inclinacion: z del mundo


if __name__ == "__main__":
    u, v = float(sys.argv[1]), float(sys.argv[2])
    y = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    print("suelo x=%.2f z=%.2f" % Camara().al_suelo(u, v, y))
