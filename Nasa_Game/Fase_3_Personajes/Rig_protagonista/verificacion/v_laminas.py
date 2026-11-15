"""Compone laminas: filas = vistas, columnas = instantes. Uso: python -I v_laminas.py <carpeta> <plan.json>"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
c = Path(sys.argv[1]); plan = json.loads(Path(sys.argv[2]).read_text())
vistas = ["frente", "derecha", "izquierda"]
for clip, ts in plan.items():
    for parte in range(0, len(ts), 4):
        tt = ts[parte:parte + 4]
        ims = [[Image.open(c / ("%s_%03d_%s.png" % (clip, round(t * 100), v))).convert("RGB") for t in tt] for v in vistas]
        w, h = ims[0][0].size
        L = Image.new("RGB", (w * len(tt), h * len(vistas)), "white")
        d = ImageDraw.Draw(L)
        for i, fila in enumerate(ims):
            for j, im in enumerate(fila):
                L.paste(im, (j * w, i * h))
                d.text((j * w + 6, i * h + 4), "%s t=%.2f %s" % (clip, tt[j], vistas[i]), fill=(0, 0, 0))
        L.save(c / ("lamina_%s_%d.jpg" % (clip, parte // 4)), quality=90)
        print("lamina_%s_%d.jpg" % (clip, parte // 4), L.size)
