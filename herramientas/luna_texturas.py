"""Convierte las texturas de la Luna de NASA (CGI Moon Kit, SVS 4720) a formatos que Godot carga.

- Color LROC (TIFF 8 bits, 4096x2048) -> JPG.
- Relieve LOLA (TIFF flotante en km, 1440x720) -> mapa de normales en el marco del cuerpo (PNG RGB8).
  Marco del cuerpo: X hacia (lon 0, lat 0), Y hacia (lon 90 E, lat 0), Z hacia el polo norte.

Antes de convertir comprueba la orientacion de los mapas con rasgos conocidos de la Luna:
  - el punto mas alto (cumbre Selenean, unos 5,4 N y 158,6 O) y el mas bajo (crater Antoniadi,
    unos 70 S y 172 O) deben caer donde dice la convencion supuesta;
  - la cara visible (centro del mapa si la longitud 0 esta al centro) es mas oscura y mas baja;
  - el color y el relieve deben estar alineados (los mares oscuros son bajos).

Uso:  python herramientas/luna_texturas.py <color.tif> <relieve.tif> <carpeta_salida> [--exageracion 4]
"""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
Image.MAX_IMAGE_PIXELS = None
RADIO_KM = 1737.4


def lon_lat(x, y, w, h, lon_centro):
    """Centro del texel (x, y) -> (lon, lat) en grados, con longitud este creciendo hacia la derecha."""
    return lon_centro - 180 + (x + 0.5) / w * 360, 90 - (y + 0.5) / h * 180


def distancia_ang(lon1, lat1, lon2, lat2):
    a = math.radians
    c = (math.sin(a(lat1)) * math.sin(a(lat2)) +
         math.cos(a(lat1)) * math.cos(a(lat2)) * math.cos(a(lon1 - lon2)))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("color")
    ap.add_argument("relieve")
    ap.add_argument("salida")
    ap.add_argument("--exageracion", type=float, default=4.0)
    a = ap.parse_args()
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    color = Image.open(a.color).convert("RGB")
    alt = np.asarray(Image.open(a.relieve), dtype=np.float64)  # km respecto de 1737,4 km
    h, w = alt.shape

    # 1. Orientacion: rasgos conocidos con la convencion "longitud 0 al centro, este a la derecha"
    y_max, x_max = np.unravel_index(np.argmax(alt), alt.shape)
    y_min, x_min = np.unravel_index(np.argmin(alt), alt.shape)
    cumbre = lon_lat(x_max, y_max, w, h, 0.0)
    fondo = lon_lat(x_min, y_min, w, h, 0.0)
    err_cumbre = distancia_ang(*cumbre, -158.6, 5.4)
    err_fondo = distancia_ang(*fondo, -172.0, -70.0)
    espejo_cumbre = distancia_ang(-cumbre[0], cumbre[1], -158.6, 5.4)

    lum = np.asarray(color.convert("L").resize((w, h), Image.BILINEAR), dtype=np.float64)
    banda = slice(h // 6, 5 * h // 6)  # +-60 grados de latitud
    mitad_centro = np.s_[banda, w // 4: 3 * w // 4]
    lum_centro = lum[mitad_centro].mean()
    lum_resto = np.concatenate([lum[banda, : w // 4], lum[banda, 3 * w // 4:]], axis=1).mean()
    alt_centro = alt[mitad_centro].mean()
    alt_resto = np.concatenate([alt[banda, : w // 4], alt[banda, 3 * w // 4:]], axis=1).mean()
    corr = float(np.corrcoef(lum[banda].ravel(), alt[banda].ravel())[0, 1])
    corr_espejo = float(np.corrcoef(lum[banda, ::-1].ravel(), alt[banda].ravel())[0, 1])

    print(f"Relieve: {w}x{h}, de {alt.min():.2f} a {alt.max():.2f} km")
    print(f"Punto más alto en lon {cumbre[0]:.1f}, lat {cumbre[1]:.1f} -> a {err_cumbre:.1f} grados de la cumbre Selenean "
          f"(si el mapa estuviera en espejo: {espejo_cumbre:.1f})")
    print(f"Punto más bajo en lon {fondo[0]:.1f}, lat {fondo[1]:.1f} -> a {err_fondo:.1f} grados del cráter Antoniadi")
    print(f"Mitad central frente al resto: brillo {lum_centro:.1f} / {lum_resto:.1f}; altura {alt_centro:.2f} / {alt_resto:.2f} km")
    print(f"Correlación brillo-altura: {corr:.3f} alineados, {corr_espejo:.3f} con el color en espejo")
    orientacion_ok = err_cumbre < 3 and err_fondo < 5 and lum_centro < lum_resto and alt_centro < alt_resto and corr > corr_espejo
    if not orientacion_ok:
        raise SystemExit("La orientación de los mapas no coincide con la supuesta: no se convierte nada.")

    # 2. Color
    color.save(salida / "luna_color_4k.jpg", quality=92)

    # 3. Normales en el marco del cuerpo
    lon = np.radians(lon_lat(np.arange(w), 0, w, h, 0.0)[0])[None, :]
    lat = np.radians(lon_lat(0, np.arange(h), w, h, 0.0)[1])[:, None]
    d_lon, d_lat = 2 * math.pi / w, math.pi / h
    k = a.exageracion
    h_lon = (np.roll(alt, -1, axis=1) - np.roll(alt, 1, axis=1)) / (2 * d_lon) * k
    arriba = np.vstack([alt[:1], alt[:-1]])
    abajo = np.vstack([alt[1:], alt[-1:]])
    h_lat = (arriba - abajo) / (2 * d_lat) * k  # la fila 0 es el norte
    r = RADIO_KM + alt
    cos_lat = np.maximum(np.cos(lat), 0.02)
    p = np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat) * np.ones_like(lon)], axis=-1)
    e_lon = np.stack([-np.sin(lon), np.cos(lon), np.zeros_like(lon)], axis=-1) * np.ones((h, 1, 1))
    e_lat = np.stack([-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat) * np.ones_like(lon)], axis=-1)
    n = p - (h_lon / (r * cos_lat))[..., None] * e_lon - (h_lat / r)[..., None] * e_lat
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    Image.fromarray(np.clip((n + 1) * 127.5 + 0.5, 0, 255).astype(np.uint8), "RGB").save(salida / "luna_normales.png")

    info = {"color": "luna_color_4k.jpg", "normales": "luna_normales.png", "lon_centro_deg": 0.0,
            "este_a_la_derecha": True, "exageracion_relieve": k,
            "altura_min_km": round(float(alt.min()), 3), "altura_max_km": round(float(alt.max()), 3),
            "comprobacion": {"cumbre_lon_lat": [round(c, 2) for c in cumbre], "error_cumbre_deg": round(err_cumbre, 2),
                             "fondo_lon_lat": [round(c, 2) for c in fondo], "error_fondo_deg": round(err_fondo, 2),
                             "brillo_centro_resto": [round(lum_centro, 1), round(lum_resto, 1)],
                             "altura_centro_resto_km": [round(alt_centro, 3), round(alt_resto, 3)],
                             "correlacion_brillo_altura": [round(corr, 3), round(corr_espejo, 3)]},
            "fuente": "NASA's Scientific Visualization Studio, CGI Moon Kit (SVS 4720): LRO LROC WAC y LOLA"}
    (salida / "texturas.json").write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Escritos luna_color_4k.jpg y luna_normales.png ({w}x{h}, exageración {k}) en {salida}")


if __name__ == "__main__":
    main()
