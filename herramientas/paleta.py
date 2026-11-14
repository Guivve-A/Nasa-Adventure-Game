"""Paleta maestra del juego y control de coherencia de color.

extraer:  colores dominantes de las imagenes aprobadas (k-means de ImageMagick). Escribe
          Nasa_Game/Fase_1_Arte/paleta_maestra.json y paleta_maestra.png
comparar: que parte del color de una imagen nueva cae cerca de la paleta maestra (Delta E CIE76).
          Es un indicador de deriva de color, no un veredicto artistico. Con --hoja ignora el fondo.

Uso:
  python herramientas/paleta.py extraer <img> [<img> ...] [--n 16] [--extra "#00E5FF=Cian"]
  python herramientas/paleta.py comparar <img> [<img> ...] [--hoja] [--tolerancia 20]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "Nasa_Game" / "Fase_1_Arte"
PALETA = DIR / "paleta_maestra.json"
COHERENCIA = DIR / "paleta_coherencia.json"
FONDO_NEUTRO = "#C9C3BE"


def magick(*args):
    return subprocess.run(["magick", *map(str, args)], capture_output=True, text=True, check=True).stdout


def clusters(imagenes, n, ancho=480):
    base = [*imagenes, "-resize", f"{ancho}x", "-background", FONDO_NEUTRO, "-alpha", "remove", "-alpha", "off",
            "+append"]
    fin = ["-depth", "8", "-format", "%c", "histogram:info:-"]
    try:
        salida = magick(*base, "-kmeans", n, *fin)
    except subprocess.CalledProcessError:
        salida = magick(*base, "-colors", n, *fin)
    colores = []
    for linea in salida.splitlines():
        m = re.search(r"^\s*(\d+):.*?(#[0-9A-Fa-f]{6})(?:[0-9A-Fa-f]{2})?\b", linea)
        if m:
            colores.append((int(m.group(1)), m.group(2).upper()))
    total = sum(c for c, _ in colores) or 1
    return sorted(((c / total, h) for c, h in colores), reverse=True)


def lab(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def lineal(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = lineal(r), lineal(g), lineal(b)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de(a, b):
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5


def extraer(a):
    paleta = [{"hex": h, "peso": round(p, 4), "lab": [round(v, 1) for v in lab(h)]}
              for p, h in clusters(a.imagenes, a.n)]
    for extra in a.extra:
        h, _, nota = extra.partition("=")
        paleta.append({"hex": h.upper(), "peso": 0.0, "lab": [round(v, 1) for v in lab(h)], "nota": nota})
    PALETA.write_text(json.dumps({"fuente": [Path(i).name for i in a.imagenes], "colores": paleta},
                                 indent=1, ensure_ascii=False), encoding="utf-8")
    args = ["montage", "-font", "Arial", "-pointsize", "18", "-fill", "white", "-background", "#1b1b1b",
            "-size", "220x130"]
    for c in paleta:
        texto = f"{c['peso'] * 100:.0f} %" if c["peso"] else c.get("nota", "")
        args += ["-label", f"{c['hex']}  {texto}", f"xc:{c['hex']}"]
    args += ["-tile", "6x", "-geometry", "+8+8", str(PALETA.with_suffix(".png"))]
    magick(*args)
    for c in paleta:
        print(f"{c['hex']}  {c['peso'] * 100:5.1f} %  Lab {c['lab']}  {c.get('nota', '')}")


def comparar(a):
    maestra = [tuple(c["lab"]) for c in json.loads(PALETA.read_text(encoding="utf-8"))["colores"]]
    resultados = json.loads(COHERENCIA.read_text(encoding="utf-8")) if COHERENCIA.exists() else {}
    for img in a.imagenes:
        cols = [(p, h, lab(h)) for p, h in clusters([img], 16, 640)]
        if a.hoja:
            esquina = magick(img, "-background", FONDO_NEUTRO, "-alpha", "remove", "-alpha", "off",
                             "-format", "%[hex:p{6,6}]", "info:").strip()[:6]
            fondo = lab("#" + esquina)
            cols = [c for c in cols if de(c[2], fondo) > 8]
        total = sum(p for p, _, _ in cols) or 1
        cerca = sum(p for p, _, l in cols if min(de(l, m) for m in maestra) <= a.tolerancia) / total
        medio = sum(p * min(de(l, m) for m in maestra) for p, _, l in cols) / total
        resultados[Path(img).name] = {"cerca_pct": round(cerca * 100, 1), "de_medio": round(medio, 1),
                                      "tolerancia": a.tolerancia}
        print(f"{Path(img).name:42} {cerca * 100:5.1f} % cerca de la paleta  (Delta E medio {medio:4.1f})")
    COHERENCIA.write_text(json.dumps(resultados, indent=1, ensure_ascii=False), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="orden", required=True)
    e = sub.add_parser("extraer")
    e.add_argument("imagenes", nargs="+")
    e.add_argument("--n", type=int, default=16)
    e.add_argument("--extra", action="append", default=[])
    c = sub.add_parser("comparar")
    c.add_argument("imagenes", nargs="+")
    c.add_argument("--hoja", action="store_true")
    c.add_argument("--tolerancia", type=float, default=20)
    a = ap.parse_args()
    extraer(a) if a.orden == "extraer" else comparar(a)


if __name__ == "__main__":
    main()
