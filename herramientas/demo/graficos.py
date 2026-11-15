"""Graficos propios del video demo (sin creditos): PNG con transparencia a 1920x1080 y animaciones cortas.

Sistema grafico: la paleta y la fuente de la interfaz del juego (juego/interfaz/estilo.gd): Bahnschrift (fuente
variable del sistema; Bold para titulos, SemiBold para rotulos), crema f8c991, papel f6e7c8, noche 1c282e,
cian 62e4e0 y naranja f4a159 (el punto de luz ambar del titulo).

Salida en Nasa_Game/Presentacion/graficos/:
  G01_titulo.png, G01_titulo_sobre_negro.png, G01_punto_luz.png, G01_apertura.mp4 (S07, 1,5 s),
  G01_cierre.mov (S48, 4 s, con alfa: el iris se cierra sobre la ultima imagen, queda el titulo y funde a negro)
  G02_luna_medida.png (S20), G03_triptico.png y sus capas G03_capa_1..3.png (S37), G04_equipo.png (S46),
  G06_cifras.png (tarjeta de cifras), rotulos/rotulo_SNN.png (un PNG por rotulo de montaje.json),
  sello_ia.png, sello_en_produccion.png, vineta.png, lineas_tv.png, ocular_abre.mov (S18), _hoja_de_contacto.jpg

Uso: python -I herramientas/demo/graficos.py [--sin-video]
     python -I herramientas/demo/graficos.py --rotulo "texto nuevo" salida.png   (rotulo suelto, misma plantilla)
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parents[2]
NASA = RAIZ / "Nasa_Game"
SAL = NASA / "Presentacion" / "graficos"
W, H = 1920, 1080
FUENTE = "C:/Windows/Fonts/bahnschrift.ttf"

NOCHE = (28, 40, 46)
CREMA = (248, 201, 145)
PAPEL = (246, 231, 200)
TINTA = (50, 44, 29)
CIAN = (98, 228, 224)
CIAN_MEDIO = (54, 177, 178)
NARANJA = (244, 161, 89)
PETROLEO = (81, 107, 124)
SOMBRA_LUNA = (59, 74, 82)


def fuente(tam, estilo=b"SemiBold"):
    f = ImageFont.truetype(FUENTE, tam)
    f.set_variation_by_name(estilo)
    return f


def lienzo(color=None):
    return Image.new("RGBA", (W, H), (0, 0, 0, 0) if color is None else color + (255,))


def ancho(texto, f, espaciado=0):
    return f.getlength(texto) + espaciado * max(0, len(texto) - 1)


def escribir(d, xy, texto, f, color, espaciado=0, ancla="la"):
    if not espaciado:
        d.text(xy, texto, font=f, fill=color, anchor=ancla)
        return
    x, y = xy
    total = ancho(texto, f, espaciado)
    if ancla[0] == "m":
        x -= total / 2
    elif ancla[0] == "r":
        x -= total
    for c in texto:
        d.text((x, y), c, font=f, fill=color, anchor="l" + ancla[1])
        x += f.getlength(c) + espaciado


def sombra(capa, radio=10, opacidad=0.55, desplazamiento=(0, 4)):
    # sombra suave bajo los pixeles opacos de "capa"
    a = capa.getchannel("A").point(lambda v: int(v * opacidad))
    s = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(radio))
    base = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    base.alpha_composite(s, desplazamiento)
    base.alpha_composite(capa)
    return base


def resplandor(capa, color, radio, opacidad):
    a = capa.getchannel("A").filter(ImageFilter.GaussianBlur(radio)).point(lambda v: min(255, int(v * opacidad)))
    g = Image.new("RGBA", capa.size, color + (0,))
    g.putalpha(a)
    base = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    base.alpha_composite(g)
    base.alpha_composite(capa)
    return base


YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


def distancia(cx=W / 2, cy=H / 2):
    return np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)


D_CENTRO = distancia()


def punto_luz(radio, intensidad=1.0, nucleo=True):
    """Punto de luz ambar sobre negro (RGB, uint8): halo amplio + nucleo crema."""
    halo = np.exp(-(D_CENTRO / max(radio, 1.0)) ** 2) * 0.85
    halo += np.exp(-(D_CENTRO / max(radio * 3.2, 1.0)) ** 2) * 0.22
    img = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        img[..., i] += halo * NARANJA[i]
    if nucleo:   # True/False o un peso entre 0 y 1
        n = np.exp(-(D_CENTRO / max(radio * 0.18, 1.2)) ** 2) * float(nucleo)
        for i in range(3):
            img[..., i] += n * (255 - NARANJA[i] * 0.3) * 0.9
    return np.clip(img * intensidad, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- G01 titulo

TITULO = "Zingularity: Artemis"   # 2026-11-15: nombre definitivo (antes «Luz cenicienta»; copias *_luz en graficos/)
SUBTITULO = "Una aventura de exploración espacial · Guayaquil, Ecuador"
TITULO_ANCHO_MAX = 1560   # deja al menos 180 px de margen a cada lado


def tam_titulo():
    # 168 px como el titulo anterior; si el nombre no cabe con margen comodo, se reduce hasta caber
    tam = 168
    while tam > 80 and ancho(TITULO, fuente(tam, b"Bold"), 2) > TITULO_ANCHO_MAX:
        tam -= 2
    return tam


def capa_titulo(alfa_titulo=1.0, alfa_sub=1.0):
    # v2: el subtitulo va mas abajo, fuera del halo del punto de luz, en crema (~40 px de altura de mayuscula)
    # sobre una franja oscura difusa, sin resplandor ambar encima (antes, cian sobre el halo, no se leia)
    capa = lienzo()
    d = ImageDraw.Draw(capa)
    ft = fuente(tam_titulo(), b"Bold")
    escribir(d, (W / 2, H / 2 - 10), TITULO, ft, CREMA + (int(255 * alfa_titulo),), espaciado=2, ancla="ms")
    capa = resplandor(capa, NARANJA, 26, 0.55)
    if alfa_sub <= 0:
        return capa
    fs = fuente(54, b"SemiBold")
    ys = H / 2 + 170
    w = ancho(SUBTITULO, fs, 1)
    franja = lienzo()
    ImageDraw.Draw(franja).rounded_rectangle([W / 2 - w / 2 - 44, ys - 58, W / 2 + w / 2 + 44, ys + 24], radius=20,
                                             fill=(6, 8, 12, int(185 * alfa_sub)))
    capa.alpha_composite(franja.filter(ImageFilter.GaussianBlur(14)))
    texto = lienzo()
    escribir(ImageDraw.Draw(texto), (W / 2, ys), SUBTITULO, fs, CREMA + (int(255 * alfa_sub),), espaciado=1, ancla="ms")
    capa.alpha_composite(sombra(texto, 4, 0.9, (0, 2)))
    return capa


def g01():
    t = capa_titulo()
    t.save(SAL / "G01_titulo.png")
    fondo = Image.fromarray(punto_luz(400, 0.5, nucleo=False)).convert("RGBA")
    fondo.alpha_composite(t)
    fondo.convert("RGB").save(SAL / "G01_titulo_sobre_negro.png")
    Image.fromarray(punto_luz(26, 1.0)).save(SAL / "G01_punto_luz.png")


def suave(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def video(nombre, cuadros, fps=30, alfa=False):
    destino = SAL / nombre
    if alfa:
        args = ["-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                "-c:v", "qtrle", "-pix_fmt", "argb", str(destino)]
    else:
        args = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(destino)]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", *args], stdin=subprocess.PIPE)
    for c in cuadros:
        p.stdin.write(c.tobytes())
    p.stdin.close()
    p.wait()
    print("  video", destino.name)


def g01_apertura():
    # S07 (v2: 14,5-17,0, 2,5 s): el punto ambar aparece y se abre en halo; el titulo esta entero a los 0,45 s
    # (se lee 2,05 s) y el subtitulo a los 0,75 s
    def cuadros():
        n = 75
        for i in range(n):
            t = i / 30
            r = 6 + 394 * suave((t - 0.05) / 0.65)
            inten = 0.35 + 0.65 * suave(t / 0.2) - 0.45 * suave((t - 0.3) / 0.8)
            base = Image.fromarray(punto_luz(r, inten, nucleo=1.0 - suave((t - 0.15) / 0.35))).convert("RGBA")
            base.alpha_composite(capa_titulo(suave((t - 0.12) / 0.33), suave((t - 0.4) / 0.35)))
            yield np.array(base.convert("RGB"))
    video("G01_apertura.mp4", cuadros())


def g01_cierre():
    # S48, 146,0-150,0: capa con alfa sobre la ultima imagen. 0-0,6 s el iris se cierra en un punto ambar;
    # 0,5-1,1 entra el titulo; 3,0-3,5 todo funde a negro (149,5); 3,5-4,0 negro.
    titulo = capa_titulo()

    def cuadros():
        for i in range(120):
            t = i / 30
            k = suave(t / 0.6)
            radio_iris = 1150 * (1 - k)
            borde = 40
            a_negro = np.clip((D_CENTRO - radio_iris) / borde + k, 0, 1)   # cerrado del todo al final
            # el nucleo del punto se apaga mientras entra el titulo, para no lavar las letras
            luz = punto_luz(max(6.0, 26 + 300 * suave((t - 0.55) / 0.8)), 0.4 + 0.6 * suave((t - 0.4) / 0.3),
                            nucleo=1.0 - 0.9 * suave((t - 0.6) / 0.6)).astype(np.float32)
            # anillo ambar en el borde del iris mientras se cierra
            anillo = np.exp(-((D_CENTRO - radio_iris) / 30) ** 2) * (1 - k) * 0.6
            rgb = luz * a_negro[..., None]
            for c in range(3):
                rgb[..., c] += anillo * NARANJA[c]
            alfa = np.clip(a_negro + anillo, 0, 1)
            capa = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alfa * 255]).astype(np.uint8), "RGBA")
            at = suave((t - 0.4) / 0.45)   # v2: entero a los 0,85 s, se lee hasta 3,2 s (2,35 s)
            if at > 0:
                tt = titulo.copy()
                tt.putalpha(tt.getchannel("A").point(lambda v: int(v * at)))
                capa.alpha_composite(tt)
            fin = suave((t - 3.2) / 0.4)
            if fin > 0:
                negro = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * fin)))
                capa.alpha_composite(negro)
            yield np.array(capa)
    video("G01_cierre.mov", cuadros(), alfa=True)


# ---------------------------------------------------------------- rotulos y sellos

ROT_X, ROT_BASE = 96, H - 120   # esquina inferior izquierda de la franja (deja libre la franja de ayuda del juego)


def rotulo(texto, sub=None):
    """Franja abajo a la izquierda. Con 'sub', una segunda linea mas pequena en cian (montaje de minijuegos: el
    rotulo principal queda fijo y la segunda linea cambia en cada corte)."""
    capa = lienzo()
    f = fuente(58, b"SemiBold")
    fsub = fuente(40, b"Regular")
    pad_x, pad_y = 38, 24
    alto_txt = f.getmetrics()[0] + 6
    w = ancho(texto, f, 1)
    alto_sub = 0
    if sub:
        w = max(w, ancho(sub, fsub, 1))
        alto_sub = 52
    w = int(w + 2 * pad_x + 10)
    h = int(alto_txt + 2 * pad_y - 6 + alto_sub)
    x0, y1 = ROT_X, ROT_BASE
    y0 = y1 - h
    franja = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    df = ImageDraw.Draw(franja)
    df.rounded_rectangle([x0, y0, x0 + w, y1], radius=12, fill=NOCHE + (200,))
    df.rounded_rectangle([x0, y0, x0 + 8, y1], radius=4, fill=NARANJA + (255,))
    capa = sombra(franja, 16, 0.5, (0, 6))
    d = ImageDraw.Draw(capa)
    escribir(d, (x0 + pad_x + 10, y1 - pad_y - 4 - alto_sub), texto, f, CREMA + (255,), espaciado=1, ancla="ls")
    if sub:
        escribir(d, (x0 + pad_x + 10, y1 - pad_y - 2), sub, fsub, CIAN + (255,), espaciado=1, ancla="ls")
    return capa


def rotulos():
    m = json.loads((NASA / "Presentacion" / "montaje.json").read_text(encoding="utf-8"))
    carpeta = SAL / "rotulos"
    carpeta.mkdir(exist_ok=True)
    for viejo in carpeta.glob("rotulo_S*.png"):   # sin restos de rotulos que ya no estan en montaje.json
        viejo.unlink()
    indice = []
    for s in m["segmentos"]:
        r = s.get("rotulo")
        if not r:
            continue
        if s["id"] in ("S07", "S48"):      # el titulo va en G01, no en la franja
            indice.append({"segmento": s["id"], "texto": r["texto"], "archivo": "G01 (titulo)", "inicio": r["inicio"], "fin": r["fin"]})
            continue
        palabras = len([p for p in r["texto"].replace("·", " ").split() if p.strip()])
        rotulo(r["texto"], r.get("sub")).save(carpeta / f"rotulo_{s['id']}.png")
        indice.append({"segmento": s["id"], "texto": r["texto"], "archivo": f"rotulos/rotulo_{s['id']}.png",
                       "inicio": r["inicio"], "fin": r["fin"], "palabras": palabras})
    (carpeta / "rotulos.json").write_text(json.dumps(indice, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"  {sum(1 for i in indice if i['archivo'].startswith('rotulos'))} rotulos")
    return indice


def sello(texto, nombre):
    capa = lienzo()
    f = fuente(30, b"Regular")
    w = ancho(texto, f, 1)
    pastilla = lienzo()
    ImageDraw.Draw(pastilla).rounded_rectangle([W - 56 - w - 18, H - 48 - 30, W - 56 + 18, H - 48 + 12], radius=10, fill=NOCHE + (150,))
    capa.alpha_composite(pastilla.filter(ImageFilter.GaussianBlur(2)))
    texto_capa = lienzo()
    escribir(ImageDraw.Draw(texto_capa), (W - 56, H - 48), texto, f, PAPEL + (255,), espaciado=1, ancla="rs")
    capa.alpha_composite(sombra(texto_capa, 3, 0.9, (0, 1)))
    capa.putalpha(capa.getchannel("A").point(lambda v: int(v * 0.70)))   # al 70 %
    capa.save(SAL / nombre)


# ---------------------------------------------------------------- G02 Luna medida contra Horizons

def disco_mascara(diametro):
    a = np.array(Image.open(RAIZ / "pruebas/luna_telescopio/capturas/luna_prueba.png").convert("L")).astype(np.int32)
    lit = a > 200
    oscuro = (a > 60) & (a <= 200)
    disco = lit | oscuro
    ys, xs = np.nonzero(disco)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    fraccion = lit.sum() / disco.sum()
    ly, lx = np.nonzero(lit)
    ang = np.degrees(np.arctan2(lx.mean() - cx, -(ly.mean() - cy)))
    ang_antihorario = (360 - ang) % 360
    rgba = np.zeros(a.shape + (4,), np.uint8)
    rgba[oscuro] = SOMBRA_LUNA + (255,)
    rgba[lit] = CREMA + (255,)
    img = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1], "RGBA")
    # suaviza el borde escalando en dos pasos
    img = img.resize((diametro * 2, diametro * 2), Image.LANCZOS).resize((diametro, diametro), Image.LANCZOS)
    return img, fraccion, ang_antihorario


def disco_horizons(diametro, k, angulo):
    # creciente de fraccion k con el borde iluminado a "angulo" grados desde el cenit, en sentido antihorario
    s = diametro * 2
    r = s / 2
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float64)
    px, py = xx - r + 0.5, yy - r + 0.5
    th = np.radians(angulo)
    u = np.array([-np.sin(th), -np.cos(th)])
    v = np.array([u[1], -u[0]])
    a = px * u[0] + py * u[1]
    b = px * v[0] + py * v[1]
    dentro = px ** 2 + py ** 2 <= r ** 2
    lit = dentro & (a > (1 - 2 * k) * np.sqrt(np.clip(r ** 2 - b ** 2, 0, None)))
    rgba = np.zeros((s, s, 4), np.uint8)
    rgba[dentro] = SOMBRA_LUNA + (255,)
    rgba[lit] = CREMA + (255,)
    return Image.fromarray(rgba, "RGBA").resize((diametro, diametro), Image.LANCZOS), lit.sum() / dentro.sum()


def fondo_noche():
    g = np.zeros((H, W, 3), np.float32)
    t = np.clip(1 - D_CENTRO / 1300, 0, 1)
    for i in range(3):
        g[..., i] = NOCHE[i] * (0.55 + 0.6 * t)
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")


def g02():
    img = fondo_noche()
    d = ImageDraw.Draw(img)
    diam = 440
    izq, frac_m, ang_m = disco_mascara(diam)
    der, frac_h = disco_horizons(diam, 0.122, 192.6)
    cy = 410
    for cx, disco in ((W / 2 - 400, izq), (W / 2 + 400, der)):
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(halo).ellipse([cx - diam / 2 - 6, cy - diam / 2 - 6, cx + diam / 2 + 6, cy + diam / 2 + 6], outline=CIAN_MEDIO + (160,), width=3)
        img.alpha_composite(halo)
        img.alpha_composite(disco, (int(cx - diam / 2), int(cy - diam / 2)))
    fe = fuente(40, b"SemiBold")
    fg = fuente(120, b"Bold")
    fp = fuente(34, b"Regular")
    for cx, etiqueta, cifra, nota in ((W / 2 - 400, "Medido en el motor", "12,15 %", "borde iluminado a 192,6°"),
                                      (W / 2 + 400, "JPL Horizons", "12,2 %", "borde iluminado a 192,6°")):
        escribir(d, (cx, 160), etiqueta.upper(), fe, CIAN, espaciado=4, ancla="ms")
        escribir(d, (cx, cy + diam / 2 + 125), cifra, fg, CREMA, ancla="ms")
        escribir(d, (cx, cy + diam / 2 + 172), nota, fp, PAPEL, ancla="ms")
    escribir(d, (W / 2, cy + 14), "≈", ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 120), PETROLEO, ancla="ms")
    escribir(d, (W / 2, 84), "Luna de Guayaquil · 12 nov 2026, 19:30", fuente(40, b"Regular"), PAPEL, espaciado=1, ancla="ms")
    img.convert("RGB").save(SAL / "G02_luna_medida.png")
    return frac_m, ang_m, frac_h


def _creciente(rgba, k, angulo):
    """Deja encendida solo la parte del disco (RGBA, crema = iluminado) que cae en una creciente de fraccion k con el
    borde a 'angulo': sirve para que la parte iluminada crezca desde el limbo hasta su fase."""
    a = np.asarray(rgba).copy()
    s = a.shape[0]
    r = s / 2
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float64)
    px, py = xx - r + 0.5, yy - r + 0.5
    th = np.radians(angulo)
    u = np.array([-np.sin(th), -np.cos(th)])
    v = np.array([u[1], -u[0]])
    pa = px * u[0] + py * u[1]
    pb = px * v[0] + py * v[1]
    dentro = pa > (1 - 2 * k) * np.sqrt(np.clip(r ** 2 - pb ** 2, 0, None))
    lit = (a[..., 0] > 150) & (a[..., 3] > 0)
    apagar = lit & ~dentro
    a[apagar, 0], a[apagar, 1], a[apagar, 2] = SOMBRA_LUNA
    return Image.fromarray(a, "RGBA")


def g02_animado():
    """S20 (4 s): las dos lunas se encienden desde el limbo hasta su fase y las cifras cuentan hasta 12,15 % y 12,2 %
    en el primer segundo; despues queda quieto (es el mismo grafico que G02_luna_medida.png)."""
    diam = 440
    izq, _, _ = disco_mascara(diam)
    der, _ = disco_horizons(diam, 0.122, 192.6)
    cy = 410
    base = fondo_noche()
    d = ImageDraw.Draw(base)
    fe, fg, fp = fuente(40, b"SemiBold"), fuente(120, b"Bold"), fuente(34, b"Regular")
    centros = (W / 2 - 400, W / 2 + 400)
    for cx, etiqueta in zip(centros, ("Medido en el motor", "JPL Horizons")):
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(halo).ellipse([cx - diam / 2 - 6, cy - diam / 2 - 6, cx + diam / 2 + 6, cy + diam / 2 + 6],
                                     outline=CIAN_MEDIO + (160,), width=3)
        base.alpha_composite(halo)
        escribir(d, (cx, 160), etiqueta.upper(), fe, CIAN, espaciado=4, ancla="ms")
        escribir(d, (cx, cy + diam / 2 + 172), "borde iluminado a 192,6°", fp, PAPEL, ancla="ms")
    escribir(d, (W / 2, cy + 14), "≈", ImageFont.truetype("C:/Windows/Fonts/segoeuil.ttf", 120), PETROLEO, ancla="ms")
    escribir(d, (W / 2, 84), "Luna de Guayaquil · 12 nov 2026, 19:30", fuente(40, b"Regular"), PAPEL, espaciado=1, ancla="ms")

    def cuadros():
        ultimo = None
        for i in range(120):
            t = i / 30
            p = suave((t - 0.15) / 1.0)
            if p >= 1.0 and ultimo is not None:
                yield ultimo
                continue
            im = base.copy()
            k = 0.2 * p   # 0,2 > 0,122: al final la mascara medida queda entera, tal cual
            im.alpha_composite(_creciente(izq, k, 192.6), (int(centros[0] - diam / 2), int(cy - diam / 2)))
            im.alpha_composite(_creciente(der, k, 192.6), (int(centros[1] - diam / 2), int(cy - diam / 2)))
            dd = ImageDraw.Draw(im)
            escribir(dd, (centros[0], cy + diam / 2 + 125), f"{12.15 * p:.2f} %".replace(".", ","), fg, CREMA, ancla="ms")
            escribir(dd, (centros[1], cy + diam / 2 + 125), f"{12.2 * p:.1f} %".replace(".", ","), fg, CREMA, ancla="ms")
            ultimo = np.array(im.convert("RGB"))
            yield ultimo
    video("G02_luna_medida.mp4", cuadros())


def luna_sola():
    """La Luna del telescopio (captura 1080p de material/telescopio_luna_real.mp4) sin el panel de datos, el globo de
    Orbita ni el gato: solo el disco y sus dos rotulos (Luz cenicienta, Terminador), centrada y al 82 %, sobre negro.
    Para S18 (el ocular se abre sobre la Luna sola), S19 y S45: el acercamiento ya no corta la interfaz."""
    src = SAL.parent / "material" / "telescopio_luna_real.mp4"
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2", "-i", str(src), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=True)
    import io
    im = np.asarray(Image.open(io.BytesIO(r.stdout)).convert("RGB")).astype(np.float32)
    lum = im.mean(axis=2)
    # disco: lo que no es cielo negro dentro de la zona central (sin panel ni gato)
    zona = np.zeros_like(lum, bool)
    zona[60:1020, 420:1150] = True
    # disco: gris (poco saturado) y no negro; el aro de la reticula y las lineas guia son cian y quedan fuera
    sat = im.max(axis=2) - im.min(axis=2)
    disco = (lum > 20) & (sat < 18) & zona
    ys, xs = np.nonzero(disco)
    cx, cy = float(xs.mean()), float(ys.mean())
    rad = float(np.sqrt(disco.sum() / np.pi))   # radio por el area: estrellas y letras pesan poco
    d = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    m_disco = np.clip((rad + 5 - d) / 3, 0, 1)
    # rotulos y lineas guia: pixeles brillantes o cian en dos franjas a la derecha del disco
    brillo = im.max(axis=2)
    m_txt = np.zeros_like(lum)
    for (x0, x1, y0, y1) in ((int(cx) - 40, 1265, 236, int(cy) - 60), (int(cx), 1268, int(cy) + 120, int(cy) + 260)):
        sub = np.clip((brillo[y0:y1, x0:x1] - 45) / 70, 0, 1)
        m_txt[y0:y1, x0:x1] = np.maximum(m_txt[y0:y1, x0:x1], sub)
    mascara = np.maximum(m_disco, m_txt)[..., None]
    limpia = Image.fromarray(np.clip(im * mascara, 0, 255).astype(np.uint8))
    esc = 0.82   # v2b: los dos rotulos caben dentro del ocular (radio 470 px)
    w2, h2 = round(W * esc), round(H * esc)
    limpia = limpia.resize((w2, h2), Image.LANCZOS)
    lienzo_ = Image.new("RGB", (W, H), (0, 0, 0))
    lienzo_.paste(limpia, (round(W / 2 - cx * esc), round(H / 2 - cy * esc)))
    lienzo_.save(SAL / "luna_sola.png")
    print(f"  luna_sola.png: disco en ({cx:.0f}, {cy:.0f}), radio {rad:.0f} px")


ESCENAS = [   # G07: un cuadro de cada escenario jugable, de las tomas grabadas el 2026-11-15 (material/)
    ("Habitación-taller", "habitacion.mp4", 3.0, None, False),
    ("Plaza de las Iguanas", "ciudad.mp4", 5.0, None, True),
    ("Sendero del arroyo", "sendero.mp4", 3.0, None, False),
    ("Mirador del Faro", "mirador_alejar.mp4", 4.5, None, True),
    ("Luna del sueño", "luna_lenta.mp4", 2.0, (0.56, 0.48, 1.7), True),
]


def g07():
    """S41: los 5 escenarios jugables, uno por casilla (3 arriba y 2 abajo), con su nombre. Plaza, Mirador y Luna
    llevan la marca «arte provisional»: su arte aun espera la validacion de Guillermo."""
    import io
    img = fondo_noche()
    pw, ph = 560, 315
    hx, hy = 52, 96
    filas = [(0, 1, 2), (3, 4)]
    y0 = 70
    fl = fuente(36, b"SemiBold")
    fp = fuente(26, b"Regular")
    for f, fila in enumerate(filas):
        total = len(fila) * pw + (len(fila) - 1) * hx
        x0 = (W - total) / 2
        y = y0 + f * (ph + hy)
        for j, idx in enumerate(fila):
            nombre, archivo, t, recorte, provisional = ESCENAS[idx]
            r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(SAL.parent / "material" / archivo),
                                "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True)
            cuadro = Image.open(io.BytesIO(r.stdout)).convert("RGB")
            if recorte:
                fx, fy, z = recorte
                cw, ch = cuadro.width / z, cuadro.height / z
                cxx = min(max(fx * cuadro.width, cw / 2), cuadro.width - cw / 2)
                cyy = min(max(fy * cuadro.height, ch / 2), cuadro.height - ch / 2)
                cuadro = cuadro.crop((round(cxx - cw / 2), round(cyy - ch / 2), round(cxx + cw / 2), round(cyy + ch / 2)))
                from PIL import ImageEnhance
                cuadro = ImageEnhance.Contrast(cuadro).enhance(1.25)
                cuadro = ImageEnhance.Color(cuadro).enhance(1.15)
            x = int(x0 + j * (pw + hx))
            marco = lienzo()
            ImageDraw.Draw(marco).rounded_rectangle([x - 6, y - 6, x + pw + 6, y + ph + 6], radius=10, fill=PAPEL + (255,))
            img.alpha_composite(sombra(marco, 16, 0.6, (0, 8)))
            img.alpha_composite(cubrir_img(cuadro, pw, ph).convert("RGBA"), (x, int(y)))
            d = ImageDraw.Draw(img)
            escribir(d, (x + pw / 2, y + ph + 50), nombre, fl, CREMA + (255,), ancla="ms")
            if provisional:
                etq = "arte provisional"
                wt = ancho(etq, fp, 1)
                pas = lienzo()
                ImageDraw.Draw(pas).rounded_rectangle([x + pw - wt - 34, y + 12, x + pw - 12, y + 50], radius=8,
                                                      fill=NOCHE + (215,))
                img.alpha_composite(pas)
                escribir(ImageDraw.Draw(img), (x + pw - 23, y + 40), etq, fp, PAPEL + (255,), espaciado=1, ancla="rs")
    img.convert("RGB").save(SAL / "G07_escenarios.png")


def cubrir_img(im, w, h):
    esc = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


# ---------------------------------------------------------------- G03 triptico concepto -> hoja -> motor

def cubrir(ruta, w, h):
    im = Image.open(ruta).convert("RGB")
    esc = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


TRIPTICO = [
    ("Concepto", "Ancla de vista aprobada", NASA / "Fase_1_Arte/Exploracion/Lote_02/L02_exploracion_camara_alta.png"),
    ("Hoja de referencia", "Cada pieza con su ID: VEG-01…", NASA / "Fase_1_Arte/Hojas_de_referencia/Hojas_v1_lamina.jpg"),
    ("Motor", "Sendero jugable en Godot", NASA / "Construccion/Capturas/sendero_jugable.png"),
]


def g03():
    # v2: paneles de 560 x 315 (antes 528 x 297) y bloque centrado en vertical
    pw, ph = 560, 315
    hueco = 74
    x0 = (W - (3 * pw + 2 * hueco)) // 2
    y0 = 330
    capas = []
    for i, (titulo, nota, ruta) in enumerate(TRIPTICO):
        capa = lienzo()
        x = x0 + i * (pw + hueco)
        marco = lienzo()
        dm = ImageDraw.Draw(marco)
        dm.rounded_rectangle([x - 8, y0 - 8, x + pw + 8, y0 + ph + 8], radius=10, fill=PAPEL + (255,))
        capa.alpha_composite(sombra(marco, 18, 0.6, (0, 10)))
        capa.alpha_composite(cubrir(ruta, pw, ph).convert("RGBA"), (x, y0))
        d = ImageDraw.Draw(capa)
        escribir(d, (x, y0 - 64), f"{i + 1}", fuente(64, b"Bold"), NARANJA + (255,), ancla="ls")
        escribir(d, (x + 52, y0 - 66), titulo, fuente(50, b"SemiBold"), CREMA + (255,), ancla="ls")
        escribir(d, (x + pw / 2, y0 + ph + 64), nota, fuente(34, b"Regular"), PAPEL + (255,), ancla="ms")
        if i < 2:   # flecha fina hacia el panel siguiente
            ax0, ax1, ay = x + pw + 26, x + pw + hueco - 26, y0 + ph / 2
            d.line([(ax0, ay), (ax1, ay)], fill=CIAN + (255,), width=4)
            d.polygon([(ax1 + 6, ay), (ax1 - 14, ay - 12), (ax1 - 14, ay + 12)], fill=CIAN + (255,))
        capa.save(SAL / f"G03_capa_{i + 1}.png")
        capas.append(capa)
    fondo = fondo_noche()
    fondo.convert("RGB").save(SAL / "G03_fondo.png")
    for c in capas:
        fondo.alpha_composite(c)
    fondo.convert("RGB").save(SAL / "G03_triptico.png")


# ---------------------------------------------------------------- G04 equipo y creditos

def g04():
    lam = cubrir(NASA / "Fase_1_Arte/Hojas_de_referencia/Hojas_v1_lamina.jpg", W, H).filter(ImageFilter.GaussianBlur(16)).convert("RGBA")
    velo = Image.new("RGBA", (W, H), NOCHE + (205,))
    lam.alpha_composite(velo)
    capa = lienzo()
    d = ImageDraw.Draw(capa)
    escribir(d, (W / 2, 250), "EQUIPO", fuente(40, b"SemiBold"), CIAN + (255,), espaciado=10, ancla="ms")
    escribir(d, (W / 2, 372), "Guillermo · Jean · Joel · Domenica", fuente(96, b"Bold"), CREMA + (255,), espaciado=1, ancla="ms")
    escribir(d, (W / 2, 452), "Guayaquil, Ecuador", fuente(48, b"Regular"), PAPEL + (255,), espaciado=2, ancla="ms")
    d.line([(W / 2 - 160, 540), (W / 2 + 160, 540)], fill=NARANJA + (255,), width=3)
    fl = fuente(36, b"Regular")
    escribir(d, (W / 2, 625), "Datos abiertos de la NASA: LRO y JPL Horizons", fl, PAPEL + (255,), ancla="ms")
    escribir(d, (W / 2, 683), "Imágenes de la cinemática recreadas con IA", fl, PAPEL + (255,), ancla="ms")
    escribir(d, (W / 2, 741), "Música y efectos del video generados con IA", fl, PAPEL + (255,), ancla="ms")
    capa = sombra(capa, 8, 0.7, (0, 3))
    capa.save(SAL / "G04_equipo_capa.png")
    lam.alpha_composite(capa)
    lam.convert("RGB").save(SAL / "G04_equipo.png")


# ---------------------------------------------------------------- G06 cifras del cierre

CIFRAS = [   # v2, comprobadas el 2026-11-15 (ver LEEME de la presentacion.md)
    ("5", "escenarios jugables"),
    ("9", "minijuegos arcade"),
    ("10", "misiones jugables"),            # m1 a m10 de juego/datos/misiones.json (s1_base espera las dos bases)
    ("55", "fichas con su fuente"),
    ("2", "bases: Luna y Marte"),
    ("212", "pruebas con teclas, 0 fallos"),   # las 9 prueba_manos.gd de los minijuegos
    ("38–60", "fps · Intel HD 620"),        # --medir=5 en las 5 zonas: Plaza 38,3 ... Luna 60,3
    ("+20 000", "líneas de código"),
]


def g06():
    img = fondo_noche()
    capa = lienzo()
    d = ImageDraw.Draw(capa)
    escribir(d, (W / 2, 150), TITULO.upper() + " EN CIFRAS", fuente(40, b"SemiBold"), CIAN + (255,), espaciado=8, ancla="ms")
    cw, ch = 400, 300
    x0 = (W - 4 * cw) / 2
    y0 = 250
    fg = fuente(118, b"Bold")
    fl = fuente(31, b"Regular")
    for i, (cifra, etiqueta) in enumerate(CIFRAS):
        cx = x0 + (i % 4) * cw + cw / 2
        cy = y0 + (i // 4) * ch
        escribir(d, (cx, cy + 130), cifra, fg, (NARANJA if i % 2 == 0 else CREMA) + (255,), ancla="ms")
        escribir(d, (cx, cy + 190), etiqueta, fl, PAPEL + (255,), ancla="ms")
    for k in range(1, 4):
        x = x0 + k * cw
        d.line([(x, y0 + 40), (x, y0 + 2 * ch - 60)], fill=PETROLEO + (180,), width=2)
    escribir(d, (W / 2, 900), "Datos abiertos de la NASA: LRO y JPL Horizons", fuente(34, b"Regular"), PAPEL + (220,), ancla="ms")
    capa = sombra(capa, 8, 0.6, (0, 3))
    capa.save(SAL / "G06_cifras_capa.png")
    img.alpha_composite(capa)
    img.convert("RGB").save(SAL / "G06_cifras.png")


# ---------------------------------------------------------------- vineta, lineas de televisor y ocular

def vineta():
    nx = (XX - W / 2) / (W / 2)
    ny = (YY - H / 2) / (H / 2)
    r = np.sqrt(nx ** 2 * 0.85 + ny ** 2)
    a = np.clip((r - 0.62) / 0.75, 0, 1) ** 1.6 * 0.55
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(SAL / "vineta.png")


def lineas_tv():
    # para S08: cuadro 4:3 (1440x1080) centrado; lineas de barrido cada 4 px y esquinas de tubo
    rgba = np.zeros((H, W, 4), np.uint8)
    x0 = (W - 1440) // 2
    lineas = ((np.arange(H) % 4) >= 2).astype(np.float32) * 0.22
    rgba[:, x0:x0 + 1440, 3] = (lineas[:, None] * 255).astype(np.uint8)
    # tubo: oscurece los bordes del 4:3 con esquinas redondeadas
    nx = (XX[:, x0:x0 + 1440] - x0 - 720) / 720
    ny = (YY[:, x0:x0 + 1440] - 540) / 540
    sup = (np.abs(nx) ** 6 + np.abs(ny) ** 6) ** (1 / 6)
    borde = np.clip((sup - 0.86) / 0.14, 0, 1)
    rgba[:, x0:x0 + 1440, 3] = np.clip(rgba[:, x0:x0 + 1440, 3] + borde * 255, 0, 255).astype(np.uint8)
    rgba[:, :x0, 3] = 255
    rgba[:, x0 + 1440:, 3] = 255
    Image.fromarray(rgba, "RGBA").save(SAL / "lineas_tv.png")


def ocular_abre():
    # S18, 53,0-55,0: capa negra con un agujero circular que se abre (de 0 a 470 px de radio en 0,8 s) y un aro cian
    def cuadros():
        for i in range(60):
            t = i / 30
            r = 470 * suave(t / 0.8)
            a = np.clip((D_CENTRO - r) / 18, 0, 1)
            aro = np.exp(-((D_CENTRO - r) / 4) ** 2) * 0.7 * (r > 4)
            rgb = np.zeros((H, W, 3), np.float32)
            for c in range(3):
                rgb[..., c] = aro * CIAN_MEDIO[c]
            alfa = np.clip(a + aro, 0, 1)
            yield np.dstack([rgb, alfa * 255]).astype(np.uint8)
    video("ocular_abre.mov", cuadros(), alfa=True)


def hoja_de_contacto():
    archivos = ["G01_titulo_sobre_negro.png", "G02_luna_medida.png", "G03_triptico.png", "G04_equipo.png", "G06_cifras.png"]
    fondo_prueba = cubrir(NASA / "Construccion/Capturas/sendero_jugable.png", W, H).convert("RGBA")
    muestras = []
    for a in archivos:
        muestras.append(Image.open(SAL / a).convert("RGB"))
    for r in ["rotulo_S12.png", "rotulo_S34.png", "rotulo_S23.png"]:
        b = fondo_prueba.copy()
        b.alpha_composite(Image.open(SAL / "rotulos" / r))
        b.alpha_composite(Image.open(SAL / "sello_ia.png"))
        b.alpha_composite(Image.open(SAL / "vineta.png"))
        muestras.append(b.convert("RGB"))
    tw, th = 640, 360
    hoja = Image.new("RGB", (tw * 3, th * 3), (10, 10, 10))
    for i, m in enumerate(muestras[:9]):
        hoja.paste(m.resize((tw, th), Image.LANCZOS), ((i % 3) * tw, (i // 3) * th))
    hoja.save(SAL / "_hoja_de_contacto.jpg", quality=90)


def main():
    SAL.mkdir(parents=True, exist_ok=True)
    if "--rotulo" in sys.argv:   # rotulo suelto con la misma plantilla: --rotulo "texto" salida.png
        i = sys.argv.index("--rotulo")
        rotulo(sys.argv[i + 1]).save(sys.argv[i + 2])
        return
    con_video = "--sin-video" not in sys.argv
    g01()
    rotulos()
    sello("Imágenes recreadas con IA", "sello_ia.png")
    sello("En producción", "sello_en_produccion.png")
    frac_m, ang_m, frac_h = g02()
    print(f"  G02: mascara {frac_m*100:.2f} % y {ang_m:.1f}° (antihorario desde el cenit); disco Horizons dibujado {frac_h*100:.2f} %")
    g03()
    g04()
    g06()
    g07()
    luna_sola()
    vineta()
    lineas_tv()
    hoja_de_contacto()
    if con_video:
        g01_apertura()
        g01_cierre()
        g02_animado()
        ocular_abre()


if __name__ == "__main__":
    main()
