"""Lamina del bolso: hoja | v8T | v9, de cerca y a la misma escala, de frente y de perfil.

Los renders de cerca salen de render_cerca.py (camara ortografica de 0,24 m centrada en (0,12, -0,10, -0,085),
600 px: 2500 px/m). La hoja se recorta en el mismo punto y a la misma escala: se pasa del render de cuerpo entero
(render_vistas.py, 931,5 px/m) a la hoja con las cajas de la figura (alto de la figura y centro horizontal; en el
perfil, centro de la mitad de arriba, porque el bolso cambia el ancho de abajo).

Uso: python -I armar_comparacion.py   (desde esta carpeta o con rutas absolutas; no recibe argumentos)
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[5]
HOJA = RAIZ / "Nasa_Game/Fase_1_Arte/Exploracion/Lote_02/L02_protagonista_tipo1_hoja.png"
OBJ = (0.12, -0.10, -0.085)   # centro de las tomas de cerca (Blender)
ESC = 0.24                    # m que caben en la toma
LADO = 420                    # px de cada panel en la lamina
PXM = 931.5                   # px/m de render_vistas.py --lado 1000 (alto 0,994 m)
BOLSA_PERFIL_HOJA = (1585, 560)  # centro de la bolsa en el perfil de la hoja (px)
CAJA_CENTRO = {"px": (-0.009, -0.003), "my": (-0.001, -0.003)}  # centro de la caja de la malla (y o x, z)


def caja(img, frac=1.0):
    a = np.asarray(img.convert("RGB")).astype(float)
    borde = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    m = np.linalg.norm(a - np.median(borde, 0), axis=-1) > 28
    filas = np.where(m.sum(1) >= 3)[0]
    y0, y1 = filas[0], filas[-1] + 1
    corte = int(y0 + (y1 - y0) * frac)
    cols = np.where(m[y0:corte].sum(0) >= 3)[0]
    return cols[0], y0, cols[-1] + 1, y1


def recorte_hoja(vista):
    hoja = Image.open(HOJA).convert("RGB")
    zona = (200, 10, 720, 923) if vista == "px" else (1410, 10, 1790, 923)
    render = Image.open(AQUI / "renders" / f"{vista}_cuerpo.png")
    frac = 1.0 if vista == "px" else 0.45
    hx0, hy0, hx1, hy1 = caja(hoja.crop(zona), frac)
    rx0, ry0, rx1, ry1 = caja(render, frac)
    k = (hy1 - hy0) / (ry1 - ry0)
    # punto objetivo en el render de cuerpo entero
    cy, cz = CAJA_CENTRO[vista]
    horiz = OBJ[1] if vista == "px" else OBJ[0]
    rx = 375 + (horiz - cy) * PXM
    ry = 500 - (OBJ[2] - cz) * PXM
    sx = zona[0] + (hx0 + hx1) / 2 + (rx - (rx0 + rx1) / 2) * k
    sy = zona[1] + hy0 + (ry - ry0) * k
    if vista == "my":
        # en el perfil la hoja dibuja la bolsa detras de la cadera: se centra en ella (misma escala)
        sx, sy = BOLSA_PERFIL_HOJA
    medio = ESC * PXM * k / 2
    return hoja.crop((int(sx - medio), int(sy - medio), int(sx + medio), int(sy + medio))).resize(
        (LADO, LADO), Image.LANCZOS)


def main():
    try:
        f1, f2 = ImageFont.truetype("arial.ttf", 22), ImageFont.truetype("arial.ttf", 17)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    cols = ["Hoja (Lote 02)", "v8T (aprobada, bolso caja)", "v9 (bolso nuevo)"]
    filas = [("px", "Frente"), ("my", "Perfil derecho")]
    m, cab = 10, 40
    lam = Image.new("RGB", (3 * LADO + 4 * m + 30, 2 * (LADO + cab) + 3 * m + 60), (28, 28, 28))
    d = ImageDraw.Draw(lam)
    d.text((m, 8), "PER-01: bolso de herramientas, misma escala (0,24 m de lado, render sin luz)",
           fill=(240, 220, 180), font=f1)
    for i, (vista, nombre) in enumerate(filas):
        y = 50 + i * (LADO + cab + m)
        paneles = [recorte_hoja(vista)] + [
            Image.open(AQUI / f"cerca_{k}" / f"{vista}.png").convert("RGB").resize((LADO, LADO), Image.LANCZOS)
            for k in ("v8T", "v9")]
        for j, p in enumerate(paneles):
            x = 30 + m + j * (LADO + m)
            d.text((x, y + 8), f"{cols[j]} - {nombre}", fill=(220, 220, 220), font=f2)
            lam.paste(p, (x, y + cab))
    lam.save(AQUI / "bolso_comparacion.png")
    print("LAMINA_OK", AQUI / "bolso_comparacion.png")


main()
