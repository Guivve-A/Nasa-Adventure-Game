# arma lamina de caras: hoja neutra, hoja frente 36 %, v5C px_cabeza, v5A px_cabeza
import sys
from PIL import Image, ImageDraw
base = sys.argv[1]
hoja = Image.open(base + '/../../../Exploracion/Lote_02/L02_protagonista_tipo1_hoja.png').convert('RGB')
H = 700
fondo = (207, 200, 195)
def render(p):
    im = Image.open(p).convert('RGBA')
    bb = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    im = im.crop(bb)
    bg = Image.new('RGBA', im.size, fondo + (255,))
    return Image.alpha_composite(bg, im).convert('RGB')
x0, y0, x1, y1 = 200, 10, 720, 923
paneles = [
    ('hoja: cara neutra', hoja.crop((163, 979, 701, 1459))),
    ('hoja: frente 36 %', hoja.crop((x0, y0, x1, y0 + round((y1 - y0) * 0.36)))),
    ('v5C px_cabeza', render(base + '/verif5_v5C/px_cabeza.png')),
    ('v5A px_cabeza', render(base + '/verif5_v5A/px_cabeza.png')),
]
esc = []
for t, im in paneles:
    w = round(im.width * H / im.height)
    esc.append((t, im.resize((w, H), Image.LANCZOS)))
W = sum(im.width for _, im in esc) + 20 * (len(esc) + 1)
out = Image.new('RGB', (W, H + 60), (240, 240, 240))
d = ImageDraw.Draw(out)
x = 20
for t, im in esc:
    out.paste(im, (x, 40)); d.text((x, 12), t, fill=(0, 0, 0)); x += im.width + 20
out.save(base + '/juicio_v5/lamina_caras.png')
print(out.size)
