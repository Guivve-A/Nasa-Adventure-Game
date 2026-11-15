"""Prepara las imagenes fijas del video demo en 16:9 y 1920x1080 o mayor, listas para un movimiento lento.

Reglas: nunca se estira una imagen.
  - si su proporcion esta a menos del 2 % de 16:9: recorte centrado a 16:9 (y si queda por debajo de 1920 de ancho,
    se amplia con Lanczos, o con vecino mas cercano x3 si es pixel-art);
  - si no: margen pintado (la misma imagen ampliada, desenfocada y oscurecida de fondo) y la imagen entera al centro.
Salida: Nasa_Game/Presentacion/material/fijas/<grupo>__<nombre>.jpg (JPEG 95, 4:4:4) y fijas/fijas.json.
Uso: python -I herramientas/demo/fijas.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent.parent
SALIDA = RAIZ / "Nasa_Game" / "Presentacion" / "material" / "fijas"
NG = RAIZ / "Nasa_Game"
L09 = NG / "Fase_1_Arte" / "Exploracion" / "Lote_09"
EXP = NG / "Fase_1_Arte" / "Exploracion"
HR = NG / "Fase_1_Arte" / "Hojas_de_referencia"
ART = RAIZ / "Misión Artemis" / "capturas"

# grupo, ruta, pixel_art
FUENTES = []
for n in ["L09b_K03_final", "L09b_K04a_final_r1", "L09b_K04b_final", "L09b_K05_final", "L09b_K06_final",
          "L09b_K07_final_r1", "L09b_K08_final", "L09b_K09_final_r1", "L09b_K10_final", "L09b_K11a_final",
          "L09b_K11_final", "L09b_K12_final_v2", "L09b_K12_final", "L09d_K13a_final", "L09d_K13b_final",
          "L09c_K13a_v2_tres_cuartos_asta", "L09c_P14c_C_cine_gpt"]:
    FUENTES.append(("cine", L09 / f"{n}.png", False))
FUENTES.append(("cine", EXP / "Lote_10" / "fotogramas" / "L10_K05_placas_lisas.png", False))
for p in sorted(HR.glob("HR_*_v1.png")) + [HR / "Hojas_v1_lamina.jpg"]:
    FUENTES.append(("hojas", p, False))
for rel in ["Lote_01/L01_A_lowpoly_exploracion_gpt26.png", "Lote_01/L01_A_lowpoly_hub_gpt26.png",
            "Lote_02/L02_exploracion_camara_alta.png", "Lote_02/L02_mapa_region.png",
            "Lote_02/L02_protagonista_tipo1_hoja.png", "Lote_02/L02_gato_orbita_hoja.png",
            "Lote_03/L03_mirador_noche_vista_juego.png", "Lote_03/L03_ui_telescopio_luna.png",
            "Lote_05/L05_A_manana_calida_final.png", "Lote_07/L07_mapa_mundo.png", "Lote_07/L07_carga_luna.png",
            "Lote_07/L07_carga_plaza.png", "Lote_08/L08_carga_habitacion.png", "Lote_08/L08_carga_ciudad.png",
            "Lote_08/L08_carga_sendero.png", "Lote_08/L08_carga_mirador.png", "Lote_08/L08_carga_luna.png"]:
    FUENTES.append(("arte", EXP / rel, False))
FUENTES.append(("arte", NG / "Fase_1_Arte" / "Modelado" / "Lote_04" / "L04_PER01_giro.png", False))
FUENTES.append(("arte", NG / "Fase_1_Arte" / "paleta_maestra.png", False))
for rel in ["Construccion/Capturas/mapa_del_mundo.png", "Propuestas/Capturas/luna_telescopio.png",
            "Construccion/Capturas/vuelta6_arcade_nueve.jpg", "Construccion/Capturas/vuelta3_seis_escenas.jpg"]:
    FUENTES.append(("capturas", NG / rel, False))
for p in sorted(ART.glob("*.png")):
    FUENTES.append(("artemis", p, True))

W, H = 1920, 1080


def preparar(img: Image.Image, pixel: bool) -> tuple:
    img = img.convert("RGB")
    w, h = img.size
    r = (w / h) / (16 / 9)
    if pixel and abs(r - 1) < 0.02:
        k = 3 if w < W else 1
        return img.resize((w * k, h * k), Image.NEAREST), f"pixel x{k}"
    if abs(r - 1) < 0.02:
        if r > 1:
            nw = round(h * 16 / 9); x = (w - nw) // 2
            img = img.crop((x, 0, x + nw, h))
        else:
            nh = round(w * 9 / 16); y = (h - nh) // 2
            img = img.crop((0, y, w, y + nh))
        modo = "recorte 16:9"
        if img.width < W:
            img = img.resize((W, H), Image.LANCZOS)
            modo += " + Lanczos"
        return img, modo
    # margen pintado: lienzo 16:9 que contiene la imagen entera, al menos 1920x1080
    escala = max(1.0, W / w if w / h >= 16 / 9 else H / h)
    iw, ih = round(w * escala), round(h * escala)
    lw, lh = (iw, round(iw * 9 / 16)) if iw / ih >= 16 / 9 else (round(ih * 16 / 9), ih)
    lh = max(lh, round(ih * 1.06)); lw = round(lh * 16 / 9)       # aire alrededor
    fondo = img.resize((lw, round(lw * h / w)) if w / h < lw / lh else (round(lh * w / h), lh), Image.LANCZOS)
    fx, fy = (fondo.width - lw) // 2, (fondo.height - lh) // 2
    fondo = fondo.crop((fx, fy, fx + lw, fy + lh)).filter(ImageFilter.GaussianBlur(lw / 40))
    fondo = ImageEnhance.Brightness(fondo).enhance(0.45)
    figura = img.resize((iw, ih), Image.LANCZOS) if escala != 1.0 else img
    fondo.paste(figura, ((lw - iw) // 2, (lh - ih) // 2))
    return fondo, "margen pintado"


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    indice = {}
    for grupo, ruta, pixel in FUENTES:
        if not ruta.exists():
            print("FALTA", ruta)
            continue
        with Image.open(ruta) as im:
            orig = im.size
            out, modo = preparar(im, pixel)
        nombre = f"{grupo}__{ruta.stem}.jpg".replace(" ", "_")
        out.save(SALIDA / nombre, quality=95, subsampling=0)
        indice[nombre] = {"fuente": str(ruta.relative_to(RAIZ)).replace("\\", "/"), "original": list(orig),
                          "salida": list(out.size), "modo": modo}
        print(f"{nombre:60s} {orig[0]}x{orig[1]} -> {out.width}x{out.height} ({modo})")
    (SALIDA / "fijas.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(indice), "fijas")


if __name__ == "__main__":
    main()
