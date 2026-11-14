"""Recorta vistas de las hojas de referencia para mandarlas a imagen->3D (Tripo).

Por cada recorte: corta la caja de la hoja, separa la figura del fondo (por canal alfa o por
distancia al color del borde), borra las estrellas cian de las hojas, ajusta la caja a la figura,
la centra en un cuadrado de fondo liso y la escala al lado pedido. Opcionalmente la espeja.
Al final arma una lamina con todos los recortes para revisarlos de un vistazo.

Uso:  python herramientas/recortar_vistas.py <spec.json>
spec: {"salida": "carpeta", "fondo": "#e6e1dc", "lado": 1024,
       "recortes": [{"id": "PER01_frente", "hoja": "ruta.png", "caja": [x0, y0, x1, y1], "espejo": false,
                     "sin_sombra": false, "borrar": [[x0, y0, x1, y1]]}]}
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def mascara(rgba):
    """Figura = alfa alto si la hoja trae transparencia; si no, lo que se aleja del color del borde."""
    alfa = rgba[..., 3]
    if (alfa < 250).mean() > 0.02:
        return alfa > 140
    rgb = rgba[..., :3]
    borde = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    fondo = np.median(borde, axis=0)
    return np.linalg.norm(rgb - fondo, axis=-1) > 30


def sin_cian(rgba, m):
    """Las hojas de recolectables traen una estrella cian encima: fuera de la figura."""
    r, g, b = (rgba[..., i].astype(float) for i in range(3))
    cian = (b - r > 60) & (g - r > 45) & (b > 150)
    return m & ~cian


def sin_sombra(rgba, m, banda=0.25):
    """Quita la sombra de suelo: gris poco saturado en la franja de abajo de la figura."""
    filas = np.where(m.any(1))[0]
    if not len(filas):
        return m
    alto = filas[-1] - filas[0] + 1
    rgb = rgba[..., :3]
    vmax, vmin = rgb.max(-1), rgb.min(-1)
    sat = (vmax - vmin) / np.maximum(vmax, 1)
    abajo = np.zeros_like(m)
    abajo[int(filas[-1] - banda * alto):] = True
    return m & ~(abajo & (sat < 0.13) & (vmax < 235))


def caja_figura(m, minimo=3):
    filas = np.where(m.sum(1) >= minimo)[0]
    cols = np.where(m.sum(0) >= minimo)[0]
    return cols[0], filas[0], cols[-1] + 1, filas[-1] + 1


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    salida = RAIZ / spec["salida"]
    salida.mkdir(parents=True, exist_ok=True)
    fondo = hex_rgb(spec.get("fondo", "#e6e1dc"))
    lado = int(spec.get("lado", 1024))
    miniaturas = []
    for r in spec["recortes"]:
        hoja = Image.open(RAIZ / r["hoja"]).convert("RGBA")
        x0, y0, x1, y1 = r["caja"]
        trozo = np.asarray(hoja.crop((x0, y0, x1, y1))).astype(float)
        m = mascara(trozo)
        if r.get("sin_cian"):  # solo para las estrellas de las hojas; la medalla del gato es cian
            m = sin_cian(trozo, m)
        for bx0, by0, bx1, by1 in r.get("borrar", []):  # rectangulos en coordenadas de la hoja
            m[max(by0 - y0, 0):max(by1 - y0, 0), max(bx0 - x0, 0):max(bx1 - x0, 0)] = False
        if r.get("sin_sombra"):
            m = sin_sombra(trozo, m)
        a0, b0, a1, b1 = caja_figura(m)
        trozo, m = trozo[b0:b1, a0:a1], m[b0:b1, a0:a1]
        # figura sobre fondo liso: el alfa se limpia (los halos de las hojas con transparencia se van)
        alfa = m[..., None].astype(float)
        rgb = trozo[..., :3] * alfa + fondo * (1 - alfa)
        h, w = m.shape
        margen = int(max(h, w) * 0.06)
        cuadro = max(h, w) + 2 * margen
        lienzo = np.tile(fondo, (cuadro, cuadro, 1))
        oy, ox = (cuadro - h) // 2, (cuadro - w) // 2
        lienzo[oy:oy + h, ox:ox + w] = rgb
        img = Image.fromarray(lienzo.clip(0, 255).astype(np.uint8)).resize((lado, lado), Image.LANCZOS)
        if r.get("espejo"):
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        destino = salida / f"{r['id']}.png"
        img.save(destino)
        miniaturas.append(img.resize((256, 256), Image.LANCZOS))
        print(f"{r['id']:28} figura {w}x{h} px -> {lado}x{lado}  {destino.relative_to(RAIZ)}")
    columnas = 6
    filas = (len(miniaturas) + columnas - 1) // columnas
    lamina = Image.new("RGB", (columnas * 260, filas * 260), (40, 40, 40))
    for k, im in enumerate(miniaturas):
        lamina.paste(im, ((k % columnas) * 260 + 2, (k // columnas) * 260 + 2))
    lamina.save(salida / "_lamina_recortes.png")


if __name__ == "__main__":
    main()
