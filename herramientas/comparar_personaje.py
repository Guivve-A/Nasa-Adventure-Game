"""Parecido de un personaje 3D con su hoja de referencia, vista por vista, en porcentaje.

Para cada par (vista de la hoja, render sin luz de la malla con herramientas/blender/render_vistas.py):
  1. separa la figura del fondo (distancia al color del borde) y la recorta a su caja;
  2. escala las dos a la misma altura (512 px), las centra en un lienzo comun y registra el render contra la
     hoja con --registro (escala +-4 % y desplazamiento +-24 px que maximizan el IoU; sin la opcion, metrica v1);
  3. mide tres cosas:
     - silueta: IoU de las dos mascaras;
     - color: 1 - (dE76 medio dentro de la interseccion) / 40, con las imagenes suavizadas para no
       castigar el detalle fino;
     - estructura: SSIM de la luminancia dentro de la caja comun.
  Parecido de la vista = 0,4 silueta + 0,3 color + 0,3 estructura.
La vista "cabeza" sale del frente: el 36 % de arriba de cada figura, escalado aparte.
El parecido total es la media ponderada (cada vista trae su peso).

Uso:  python herramientas/comparar_personaje.py <spec.json> <lamina.png> [--etiqueta texto]
spec: {"vistas": [{"id": "frente", "hoja": ruta, "caja": [x0, y0, x1, y1], "render": ruta,
                   "espejo": false, "peso": 2, "cabeza": false}]}
Imprime una linea JSON con el parecido de cada vista y el total.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_ancla import a_lab  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
ALTO = 512


def figura(img):
    """Mascara de la figura: lo que se aleja del color mediano del borde."""
    a = np.asarray(img.convert("RGB")).astype(float)
    borde = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    fondo = np.median(borde, axis=0)
    m = np.linalg.norm(a - fondo, axis=-1) > 28
    filas, cols = np.where(m.sum(1) >= 3)[0], np.where(m.sum(0) >= 3)[0]
    return a, m, (cols[0], filas[0], cols[-1] + 1, filas[-1] + 1)


def normalizar(a, m, caja, fraccion_alta=1.0):
    """Recorta a la caja (o a su parte alta), escala a ALTO px de alto y centra en un lienzo cuadrado."""
    x0, y0, x1, y1 = caja
    y1 = y0 + int(round((y1 - y0) * fraccion_alta))
    a, m = a[y0:y1, x0:x1], m[y0:y1, x0:x1]
    h, w = m.shape
    ancho = max(1, int(round(w * ALTO / h)))
    img = Image.fromarray(a.astype(np.uint8)).resize((ancho, ALTO), Image.LANCZOS)
    msk = Image.fromarray((m * 255).astype(np.uint8)).resize((ancho, ALTO), Image.NEAREST)
    lienzo = np.full((ALTO, ALTO, 3), 128.0)
    mascara = np.zeros((ALTO, ALTO), bool)
    ox = (ALTO - ancho) // 2
    a0, a1 = max(0, ox), min(ALTO, ox + ancho)
    lienzo[:, a0:a1] = np.asarray(img).astype(float)[:, a0 - ox:a1 - ox]
    mascara[:, a0:a1] = np.asarray(msk)[:, a0 - ox:a1 - ox] > 127
    return lienzo, mascara


def mover(img, msk, s, dx, dy):
    """Escala el lienzo del render por s alrededor del centro y lo desplaza (dx, dy) px."""
    if abs(s - 1.0) > 1e-6:
        n = int(round(ALTO * s))
        im = np.asarray(Image.fromarray(img.astype(np.uint8)).resize((n, n), Image.LANCZOS)).astype(float)
        mk = np.asarray(Image.fromarray((msk * 255).astype(np.uint8)).resize((n, n), Image.NEAREST)) > 127
        lienzo, mascara = np.full((ALTO, ALTO, 3), 128.0), np.zeros((ALTO, ALTO), bool)
        o = (ALTO - n) // 2
        a0, b0 = max(0, o), max(0, -o)
        largo = min(ALTO - a0, n - b0)
        lienzo[a0:a0 + largo, a0:a0 + largo] = im[b0:b0 + largo, b0:b0 + largo]
        mascara[a0:a0 + largo, a0:a0 + largo] = mk[b0:b0 + largo, b0:b0 + largo]
        img, msk = lienzo, mascara
    img = np.roll(img, (dy, dx), (0, 1))
    msk = np.roll(msk, (dy, dx), (0, 1))
    return img, msk


def alinear(ref, ren):
    """Registro: escala (+-4 %) y desplazamiento (+-24 px) del render que maximizan el IoU de las siluetas.
    Sin esto, la caja de la hoja (que incluye el bolso) descentraba la comparacion 10 a 20 px."""
    _, ma = ref
    ib, mb = ren
    mejor = (-1.0, 1.0, 0, 0)
    for s in (0.96, 0.98, 1.0, 1.02, 1.04):
        _, m2 = mover(ib, mb, s, 0, 0)
        for dy in range(-24, 25, 4):
            for dx in range(-24, 25, 4):
                m3 = np.roll(m2, (dy, dx), (0, 1))
                iou = (ma & m3).sum() / max((ma | m3).sum(), 1)
                if iou > mejor[0]:
                    mejor = (iou, s, dx, dy)
    _, s0, dx0, dy0 = mejor
    for s in (s0 - 0.01, s0, s0 + 0.01):
        _, m2 = mover(ib, mb, s, 0, 0)
        for dy in range(dy0 - 3, dy0 + 4):
            for dx in range(dx0 - 3, dx0 + 4):
                m3 = np.roll(m2, (dy, dx), (0, 1))
                iou = (ma & m3).sum() / max((ma | m3).sum(), 1)
                if iou > mejor[0]:
                    mejor = (iou, s, dx, dy)
    _, s, dx, dy = mejor
    return mover(ib, mb, s, dx, dy), (round(s, 2), dx, dy)


def caja_media(x, r):
    """Media en una ventana de (2r+1)^2 con sumas acumuladas (sin scipy)."""
    p = np.pad(x, r, mode="edge")
    c = p.cumsum(0).cumsum(1)
    c = np.pad(c, ((1, 0), (1, 0)))
    n = 2 * r + 1
    return (c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]) / (n * n)


def ssim(a, b, r=5):
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = caja_media(a, r), caja_media(b, r)
    va = caja_media(a * a, r) - ma ** 2
    vb = caja_media(b * b, r) - mb ** 2
    cab = caja_media(a * b, r) - ma * mb
    return ((2 * ma * mb + c1) * (2 * cab + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2))


def comparar(ref, ren):
    (ia, ma), (ib, mb) = ref, ren
    union, inter = ma | mb, ma & mb
    iou = inter.sum() / max(union.sum(), 1)
    suave_a = np.stack([caja_media(ia[..., k], 4) for k in range(3)], -1)
    suave_b = np.stack([caja_media(ib[..., k], 4) for k in range(3)], -1)
    de = np.linalg.norm(a_lab(suave_a) - a_lab(suave_b), axis=-1)
    color = float(np.clip(1 - de[inter].mean() / 40.0, 0, 1)) if inter.any() else 0.0
    la = ia @ np.array([0.299, 0.587, 0.114])
    lb = ib @ np.array([0.299, 0.587, 0.114])
    # SSIM a dos escalas (1/2 y 1/4): mide formas (ojos, mechones, bolsillos) sin castigar desalineaciones
    # de pocos pixeles entre una ilustracion y un render, como el SSIM multiescala
    vals = []
    for f in (2, 4):
        n = ALTO // f
        ra = la.reshape(n, f, n, f).mean((1, 3))
        rb = lb.reshape(n, f, n, f).mean((1, 3))
        u = union.reshape(n, f, n, f).any((1, 3))
        s = ssim(ra, rb, r=3)
        vals.append(float(np.clip(s[u].mean(), 0, 1)) if u.any() else 0.0)
    estructura = float(np.mean(vals))
    total = 0.4 * iou + 0.3 * color + 0.3 * estructura
    return {"silueta": round(float(iou) * 100, 1), "color": round(color * 100, 1),
            "estructura": round(estructura * 100, 1), "parecido": round(total * 100, 1)}, de


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    lamina_r = sys.argv[2]
    etiqueta = sys.argv[sys.argv.index("--etiqueta") + 1] if "--etiqueta" in sys.argv else ""
    # metrica v2 (con --registro): alinea el render a la hoja por IoU antes de comparar. Sin la opcion queda la v1
    # (centrado por la caja de cada figura), que es la que usan los agentes del flujo wf_cb5b1503-94b
    sin_registro = "--registro" not in sys.argv
    filas, res, pesos = [], {}, []
    for v in spec["vistas"]:
        hoja = Image.open(RAIZ / v["hoja"]).convert("RGB").crop(tuple(v["caja"]))
        render = Image.open(v["render"]).convert("RGB")
        if v.get("espejo"):
            render = render.transpose(Image.FLIP_LEFT_RIGHT)
        fr = 0.36 if v.get("cabeza") else 1.0
        a, m, c = figura(hoja)
        ref = normalizar(a, m, c, fr)
        a, m, c = figura(render)
        ren = normalizar(a, m, c, fr)
        if not sin_registro:
            ren, ajuste = alinear(ref, ren)
        r, de = comparar(ref, ren)
        if not sin_registro:
            r["registro"] = ajuste
        res[v["id"]] = r
        pesos.append((r["parecido"], v.get("peso", 1)))
        filas.append((v["id"], ref, ren, de, r))
    total = sum(p * w for p, w in pesos) / sum(w for _, w in pesos)
    print(json.dumps({"etiqueta": etiqueta, "parecido_total": round(total, 1), "vistas": res}, ensure_ascii=False))

    # lamina: por vista, hoja | malla | superposicion (rojo = solo hoja, azul = solo malla)
    try:
        fuente = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        fuente = ImageFont.load_default()
    lam = Image.new("RGB", (3 * ALTO // 2 * len(filas) + 20, ALTO // 2 * 1 + 60), (24, 24, 24))
    lam = Image.new("RGB", (len(filas) * (3 * 256 + 20), 256 + 70), (24, 24, 24))
    d = ImageDraw.Draw(lam)
    for k, (nombre, (ia, ma), (ib, mb), de, r) in enumerate(filas):
        x = k * (3 * 256 + 20)
        sup = np.full((ALTO, ALTO, 3), 40.0)
        sup[ma & mb] = (200, 200, 200)
        sup[ma & ~mb] = (220, 60, 60)
        sup[mb & ~ma] = (70, 110, 230)
        for j, im in enumerate([ia, ib, sup]):
            lam.paste(Image.fromarray(im.astype(np.uint8)).resize((256, 256), Image.LANCZOS), (x + j * 256, 60))
        d.text((x + 6, 6), f"{nombre}: {r['parecido']} %", fill=(240, 220, 180), font=fuente)
        d.text((x + 6, 32), f"silueta {r['silueta']}  color {r['color']}  estructura {r['estructura']}",
               fill=(200, 200, 200), font=fuente)
    Path(lamina_r).parent.mkdir(parents=True, exist_ok=True)
    lam.save(lamina_r)


if __name__ == "__main__":
    main()
