"""Cierre tipografico del teaser: ZINGULARITY / ARTEMIS, dibujado con PIL (sin imagenes generadas).

Uso: python -I herramientas/demo/outro_teaser.py <salida.png>
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 3840, 2160
FONDO = (9, 13, 24)
CREMA = (246, 232, 200)
AMBAR = (244, 161, 89)
CIAN = (98, 228, 224)
FUENTE = "C:/Windows/Fonts/bahnschrift.ttf"


def fuente(tam, variante):
    f = ImageFont.truetype(FUENTE, tam)
    try:
        f.set_variation_by_name(variante)
    except Exception:
        pass
    return f


def texto_espaciado(d, texto, f, y, color, espacio):
    anchos = [d.textlength(c, font=f) for c in texto]
    total = sum(anchos) + espacio * (len(texto) - 1)
    x = (W - total) / 2
    for c, a in zip(texto, anchos):
        d.text((x, y), c, font=f, fill=color)
        x += a + espacio
    return total


img = Image.new("RGB", (W, H), FONDO)

# resplandor suave detras del titulo
halo = Image.new("RGB", (W, H), (0, 0, 0))
dh = ImageDraw.Draw(halo)
dh.ellipse((W / 2 - 1500, H / 2 - 700, W / 2 + 1500, H / 2 + 700), fill=(26, 40, 66))
halo = halo.filter(ImageFilter.GaussianBlur(320))
img = Image.blend(img, Image.composite(halo, img, Image.new("L", (W, H), 255)), 0.85)
img = Image.eval(img, lambda v: min(255, v))
base = Image.new("RGB", (W, H), FONDO)
img = Image.blend(base, img, 0.9)
# recomponer: fondo + halo aditivo
img = Image.new("RGB", (W, H), FONDO)
img = Image.fromarray(__import__("numpy").clip(
    __import__("numpy").asarray(img).astype("int16") + __import__("numpy").asarray(halo).astype("int16"), 0, 255
).astype("uint8"))

d = ImageDraw.Draw(img)

# estrellas discretas, fijas
import random
r = random.Random(7)
for _ in range(260):
    x, y = r.uniform(0, W), r.uniform(0, H)
    if abs(y - H / 2) < 420 and abs(x - W / 2) < 1500:
        continue
    t = r.choice([2, 2, 3, 4])
    v = r.randint(70, 150)
    d.ellipse((x, y, x + t, y + t), fill=(v, v, min(255, v + 25)))

# orbita: arco fino que cruza por detras del titulo, con un punto ambar
cx, cy, rx, ry = W / 2, H / 2 + 60, 1650, 520
pts = []
for i in range(0, 361):
    a = math.radians(i)
    pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a) * 0.55 - 0.18 * rx * math.cos(a)))
d.line(pts[200:340], fill=(60, 84, 120), width=5)
px, py = pts[318]
d.ellipse((px - 22, py - 22, px + 22, py + 22), fill=AMBAR)

# titulo
f1 = fuente(430, "Bold Condensed")
y1 = H / 2 - 400
ancho = texto_espaciado(d, "ZINGULARITY", f1, y1, CREMA, 46)

# regla ambar con muesca cian
yr = H / 2 + 110
d.rectangle((W / 2 - ancho / 2, yr, W / 2 + ancho / 2, yr + 8), fill=AMBAR)
d.rectangle((W / 2 - 60, yr - 6, W / 2 + 60, yr + 14), fill=FONDO)
d.ellipse((W / 2 - 14, yr - 10, W / 2 + 14, yr + 18), fill=CIAN)

# subtitulo
f2 = fuente(190, "Light")
texto_espaciado(d, "ARTEMIS", f2, H / 2 + 190, CREMA, 150)

f3 = fuente(64, "SemiLight")
texto_espaciado(d, "LUNA  ·  MARTE  ·  GUAYAQUIL, ECUADOR", f3, H / 2 + 520, (150, 170, 196), 14)

img.save(sys.argv[1])
print("ok", sys.argv[1])
