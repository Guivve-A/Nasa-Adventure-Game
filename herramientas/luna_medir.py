"""Mide la Luna de las capturas del telescopio y la compara con JPL Horizons.

1. Fase y borde (captura del modo de prueba): el disco iluminado sale blanco, la noche gris y el resto
   negro. Calcula la fraccion iluminada y el angulo del centroide iluminado desde el cenit
   (0 = arriba, creciendo hacia la izquierda).
2. Orientacion de la textura (captura normal): proyecta la textura sobre el disco con una implementacion
   propia, distinta del shader, y la correlaciona con la zona de luz cenicienta para varios giros, con y
   sin espejo. Detecta una textura girada o en espejo, que la prueba 1 no ve.

Uso:  python herramientas/luna_medir.py <captura_prueba.png> <datos/luna.json> [--captura <normal.png> --textura <color.jpg>]
"""
import argparse
import json
import math
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
Image.MAX_IMAGE_PIXELS = None


def unidad(lon_deg, lat_deg):
    lon, lat = math.radians(lon_deg), math.radians(lat_deg)
    return np.array([math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)])


def fase_y_borde(mascara, datos):
    disco, luz = mascara > 64, mascara > 200
    ys, xs = np.nonzero(disco)
    cy, cx = ys.mean(), xs.mean()
    radio = math.sqrt(disco.sum() / math.pi)
    fraccion = luz.sum() / disco.sum() * 100
    ly, lx = np.nonzero(luz)
    angulo = math.degrees(math.atan2(-(lx.mean() - cx), -(ly.mean() - cy))) % 360
    err_f = fraccion - datos["iluminacion_pct"]
    err_a = (angulo - datos["borde_iluminado_desde_cenit_deg"] + 180) % 360 - 180
    print(f"Disco: centro ({cx:.1f}, {cy:.1f}) px, radio {radio:.1f} px")
    print(f"Fracción iluminada: {fraccion:.2f} %   (Horizons: {datos['iluminacion_pct']} %, diferencia {err_f:+.2f})")
    print(f"Borde iluminado: {angulo:.1f} grados desde el cenit   (Horizons: {datos['borde_iluminado_desde_cenit_deg']}, diferencia {err_a:+.1f})")
    return (cx, cy, radio), abs(err_f) < 0.6 and abs(err_a) < 2.0


def orientacion(captura, textura, mascara, disco, datos):
    cx, cy, radio = disco
    tex = np.asarray(Image.open(textura).convert("L"), dtype=np.float64)
    th, tw = tex.shape
    tex = tex[: th - th % 4, : tw - tw % 4].reshape(th // 4, 4, tw // 4, 4).mean(axis=(1, 3))
    th, tw = tex.shape
    rgb = np.asarray(Image.open(captura).convert("RGB"), dtype=np.float64)
    lum = rgb.mean(axis=2)
    # fuera las lineas y marcas de la interfaz (cian y brillantes) que cruzan la zona de noche
    interfaz = ((rgb[..., 2] - rgb[..., 0]) > 40) | (lum > 100)

    ys, xs = np.mgrid[0:lum.shape[0], 0:lum.shape[1]]
    sx, sy = (xs - cx) / radio, -(ys - cy) / radio
    noche = (np.abs(mascara - 128) < 20) & (sx ** 2 + sy ** 2 < 0.92 ** 2) & ~interfaz
    sx, sy, obs_lum = sx[noche], sy[noche], lum[noche]

    o = unidad(datos["subobservador_lon_deg"], datos["subobservador_lat_deg"])
    arriba = np.array([0.0, 0.0, 1.0]) - o[2] * o
    arriba /= np.linalg.norm(arriba)
    derecha = np.cross(arriba, o)  # este selenografico a la derecha con el norte arriba
    alfa0 = math.radians(datos["pa_polo_norte_deg"] - datos["angulo_paralactico_deg"])

    def correlacion(delta_deg, espejo):
        a = alfa0 + math.radians(delta_deg)
        x = sx * math.cos(a) + sy * math.sin(a)
        y = -sx * math.sin(a) + sy * math.cos(a)
        if espejo:
            x = -x
        z = np.sqrt(np.clip(1 - x * x - y * y, 0, 1))
        p = x[:, None] * derecha + y[:, None] * arriba + z[:, None] * o
        lon = np.degrees(np.arctan2(p[:, 1], p[:, 0]))
        lat = np.degrees(np.arcsin(np.clip(p[:, 2], -1, 1)))
        # muestreo bilineal (centro del texel en +0,5)
        u = ((lon + 180) % 360) / 360 * tw - 0.5
        v = np.clip((90 - lat) / 180 * th - 0.5, 0, th - 1.000001)
        u0, v0 = np.floor(u).astype(int), np.floor(v).astype(int)
        fu, fv = u - u0, v - v0
        u0, u1, v1 = u0 % tw, (u0 + 1) % tw, np.minimum(v0 + 1, th - 1)
        muestra = ((tex[v0, u0] * (1 - fu) + tex[v0, u1] * fu) * (1 - fv) +
                   (tex[v1, u0] * (1 - fu) + tex[v1, u1] * fu) * fv)
        return float(np.corrcoef(muestra, obs_lum)[0, 1])

    giros = np.arange(-4, 4.001, 0.25)
    sin_espejo = [correlacion(g, False) for g in giros]
    con_espejo = max(correlacion(g, True) for g in np.arange(-180, 180, 5))
    mejor = float(giros[int(np.argmax(sin_espejo))])
    r0 = correlacion(0.0, False)
    print(f"Textura: correlación {r0:.3f} sin giro; mejor giro {mejor:+.2f} grados; en espejo, como máximo {con_espejo:.3f}")
    return r0 > 0.9 and abs(mejor) <= 0.5 and con_espejo < 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prueba")
    ap.add_argument("datos")
    ap.add_argument("--captura")
    ap.add_argument("--textura")
    a = ap.parse_args()
    datos = json.load(open(a.datos, encoding="utf-8"))
    mascara = np.asarray(Image.open(a.prueba).convert("L"), dtype=np.float64)
    disco, ok = fase_y_borde(mascara, datos)
    if a.captura and a.textura:
        ok = orientacion(a.captura, a.textura, mascara, disco, datos) and ok
    print("RESULTADO:", "coincide con Horizons" if ok else "NO coincide")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
