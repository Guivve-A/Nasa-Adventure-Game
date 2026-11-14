"""Compara una captura del motor con su imagen ancla: diferencia de color por zonas (Delta E en Lab).

No busca igualdad de pixeles (la escena nunca sera la ilustracion), sino que las masas de color esten en su
sitio: la copa roja arriba a la izquierda, el sendero naranja, el agua turquesa, etc. Reduce las dos imagenes
a bloques de 40x40 px (sobre 1280x720), mide el Delta E 76 de cada bloque y resume:
  - media y mediana del Delta E, y el % de bloques por debajo de 15 y de 25;
  - una rejilla 3x3 con el Delta E medio de cada zona (para saber donde atacar);
  - luminosidad, croma y contraste medios de cada imagen.
Guarda una lamina: ancla | captura | mapa de diferencia con la rejilla.

Uso:  python herramientas/comparar_ancla.py <ancla.png> <captura.png> <lamina.png> [--etiqueta "iteracion 1"]
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
ANCHO, ALTO, BLOQUE = 1280, 720, 40


def a_lab(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def cargar(ruta):
    return np.asarray(Image.open(ruta).convert("RGB").resize((ANCHO, ALTO), Image.LANCZOS)).astype(float)


def bloques(img):
    return img.reshape(ALTO // BLOQUE, BLOQUE, ANCHO // BLOQUE, BLOQUE, 3).mean((1, 3))


def resumen(lab):
    croma = np.hypot(lab[..., 1], lab[..., 2])
    return {"L": round(float(lab[..., 0].mean()), 1), "croma": round(float(croma.mean()), 1),
            "contraste_L": round(float(lab[..., 0].std()), 1)}


def main():
    ancla_r, captura_r, lamina_r = sys.argv[1:4]
    etiqueta = sys.argv[sys.argv.index("--etiqueta") + 1] if "--etiqueta" in sys.argv else ""
    ancla, captura = cargar(ancla_r), cargar(captura_r)
    la, lc = a_lab(bloques(ancla)), a_lab(bloques(captura))
    de = np.linalg.norm(la - lc, axis=-1)
    filas, cols = de.shape
    rejilla = [[round(float(de[i * filas // 3:(i + 1) * filas // 3, j * cols // 3:(j + 1) * cols // 3].mean()), 1)
                for j in range(3)] for i in range(3)]
    datos = {"etiqueta": etiqueta, "deltaE_media": round(float(de.mean()), 2),
             "deltaE_mediana": round(float(np.median(de)), 2),
             "bloques_bajo_15_pct": round(float((de < 15).mean() * 100), 1),
             "bloques_bajo_25_pct": round(float((de < 25).mean() * 100), 1),
             "rejilla_3x3": rejilla, "ancla": resumen(a_lab(ancla)), "captura": resumen(a_lab(captura))}
    print(json.dumps(datos, ensure_ascii=False))

    # lamina: ancla | captura | mapa de diferencia (rojo = lejos del ancla)
    mapa = np.clip(de / 40.0, 0, 1)
    calor = np.stack([mapa * 255, (1 - mapa) * 160, (1 - mapa) * 60], -1).astype(np.uint8)
    calor = Image.fromarray(calor).resize((ANCHO, ALTO), Image.NEAREST)
    gris = Image.fromarray(captura.astype(np.uint8)).convert("L").convert("RGB")
    calor = Image.blend(gris, calor, 0.6)
    d = ImageDraw.Draw(calor)
    try:
        fuente = ImageFont.truetype("arial.ttf", 34)
        chica = ImageFont.truetype("arial.ttf", 30)
    except OSError:
        fuente = chica = ImageFont.load_default()
    for i in range(3):
        for j in range(3):
            x0, y0 = j * ANCHO // 3, i * ALTO // 3
            d.rectangle([x0, y0, x0 + ANCHO // 3, y0 + ALTO // 3], outline=(255, 255, 255), width=2)
            d.text((x0 + 14, y0 + 10), f"{rejilla[i][j]:.0f}", fill=(255, 255, 255), font=fuente,
                   stroke_width=3, stroke_fill=(0, 0, 0))
    lamina = Image.new("RGB", (ANCHO * 3 + 40, ALTO + 70), (24, 24, 24))
    for k, im in enumerate([Image.fromarray(ancla.astype(np.uint8)), Image.fromarray(captura.astype(np.uint8)), calor]):
        lamina.paste(im, (k * (ANCHO + 20), 70))
    d = ImageDraw.Draw(lamina)
    titulos = ["Ancla aprobada", f"Escena {etiqueta}".strip(),
               f"Diferencia: media {datos['deltaE_media']}  ·  {datos['bloques_bajo_15_pct']} % de bloques < 15"]
    for k, t in enumerate(titulos):
        d.text((k * (ANCHO + 20) + 10, 18), t, fill=(240, 220, 180), font=chica)
    Path(lamina_r).parent.mkdir(parents=True, exist_ok=True)
    lamina.save(lamina_r)


if __name__ == "__main__":
    main()
