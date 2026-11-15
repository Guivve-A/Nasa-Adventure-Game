"""G05: panel del registro de pruebas (mitad derecha de S38) con texto REAL de una ejecucion.

Toma un log de Godot, se queda con las lineas PRUEBA_OK / PRUEBA_FALLO / PRUEBAS / MINIJUEGO / FIN (sin rutas ni
errores del sistema) y dibuja:
  - G05_registro.png        960x1080, el panel con las ultimas lineas (para la pantalla partida 50/50)
  - G05_registro_largo.png  960 x N, todas las lineas, para desplazarlo en el montaje (crop con y animada)
Si el log no viene de T27 (recorrido_manos), el titulo del panel dice de que prueba viene.

Uso: python -I herramientas/demo/g05_registro.py <log> [--titulo "texto"] [--sufijo _provisional]
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "Nasa_Game" / "Presentacion" / "graficos"
FONDO = (18, 26, 30)
BARRA = (28, 40, 46)
CIAN = (98, 228, 224)
CREMA = (248, 201, 145)
PAPEL = (246, 231, 200)
TENUE = (122, 141, 150)
CORAL = (228, 96, 67)
W, H = 960, 1080
MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 26)
MONO_B = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26)
TIT = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 32)
TIT.set_variation_by_name(b"SemiBold")
INTERLINEA = 38


def lineas_utiles(ruta):
    texto = Path(ruta).read_text(encoding="utf-8", errors="replace")
    out = []
    for l in texto.splitlines():
        l = l.rstrip()
        if not re.match(r"^(PRUEBA_OK|PRUEBA_FALLO|PRUEBAS |MINIJUEGO |FIN$)", l):
            continue
        if re.search(r"[A-Za-z]:[\\/]|/Users/|\\Users\\", l):   # nada de rutas personales
            continue
        if l.startswith("MINIJUEGO"):
            l = re.sub(r" detalle=.*$", "", l)
        out.append(l[:58] + ("…" if len(l) > 58 else ""))
    return out


def color_de(l):
    if l.startswith("PRUEBA_OK"):
        return CIAN, MONO_B, 10
    if l.startswith("PRUEBA_FALLO"):
        return CORAL, MONO_B, 13
    if l.startswith("PRUEBAS"):
        return CREMA, MONO_B, len(l)
    return TENUE, MONO, 0


def dibujar_lineas(d, lineas, x, y):
    for l in lineas:
        color, f, n = color_de(l)
        d.text((x, y), l[:n], font=f, fill=color)
        d.text((x + f.getlength(l[:n]), y), l[n:], font=MONO, fill=PAPEL if n else TENUE)
        y += INTERLINEA


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--titulo", default="Registro · prueba con teclas simuladas")
    ap.add_argument("--sufijo", default="")
    a = ap.parse_args()
    lineas = lineas_utiles(a.log)
    if not lineas:
        raise SystemExit("El log no tiene lineas PRUEBA_OK")
    cabecera = 92
    # panel fijo con las ultimas lineas que caben
    caben = (H - cabecera - 40) // INTERLINEA
    img = Image.new("RGB", (W, H), FONDO)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, cabecera - 20], fill=BARRA)
    for i, c in enumerate(((228, 96, 67), (218, 170, 37), (98, 228, 224))):
        d.ellipse([28 + i * 30, 26, 46 + i * 30, 44], fill=c)
    d.text((140, 18), a.titulo, font=TIT, fill=CREMA)
    dibujar_lineas(d, lineas[-caben:], 36, cabecera + 4)
    img.save(SAL / f"G05_registro{a.sufijo}.png")
    # v2: el largo (el que se desplaza en S38) lleva la misma cabecera con el titulo
    largo = Image.new("RGB", (W, cabecera + 40 + INTERLINEA * len(lineas)), FONDO)
    dl = ImageDraw.Draw(largo)
    dl.rectangle([0, 0, W, cabecera - 20], fill=BARRA)
    for i, c in enumerate(((228, 96, 67), (218, 170, 37), (98, 228, 224))):
        dl.ellipse([28 + i * 30, 26, 46 + i * 30, 44], fill=c)
    dl.text((140, 18), a.titulo, font=TIT, fill=CREMA)
    dibujar_lineas(dl, lineas, 36, cabecera + 4)
    largo.save(SAL / f"G05_registro_largo{a.sufijo}.png")
    ok = sum(1 for l in lineas if l.startswith("PRUEBA_OK"))
    print(f"{len(lineas)} lineas, {ok} PRUEBA_OK -> G05_registro{a.sufijo}.png")


if __name__ == "__main__":
    main()
