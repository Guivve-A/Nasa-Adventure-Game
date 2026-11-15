"""Mide la envolvente de un archivo de audio (RMS por ventana, en dBFS), estima el pulso y dibuja una grafica PNG.

No se puede escuchar el audio desde aqui: esta medicion es la evidencia de su forma (donde es suave, donde crece,
donde hay silencio) y se compara con las marcas de montaje.json.

Uso: python -I herramientas/demo/audio_envolvente.py <audio> [--png salida.png] [--ventana 0.5] [--marcas 11,13,15.5,70,82,123,142]
"""
import argparse
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
SR = 22050


def leer(ruta):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", ruta, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32)


def pulso(x):
    # flujo de energia en ventanas de 23 ms y autocorrelacion entre 60 y 180 BPM
    h = 512
    n = len(x) // h
    e = np.array([np.sum(x[i * h:(i + 1) * h] ** 2) for i in range(n)])
    o = np.maximum(np.diff(np.log(e + 1e-9)), 0)
    o = o - o.mean()
    ac = np.correlate(o, o, "full")[len(o) - 1:]
    fps = SR / h
    lags = np.arange(len(ac))
    bpm = 60 * fps / np.maximum(lags, 1)
    m = (bpm >= 60) & (bpm <= 180)
    i = lags[m][np.argmax(ac[m])]
    return 60 * fps / i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--png")
    ap.add_argument("--ventana", type=float, default=0.5)
    ap.add_argument("--marcas", default="")
    ap.add_argument("--desde", type=float, default=0.0)
    a = ap.parse_args()
    x = leer(a.audio)
    dur = len(x) / SR
    w = int(a.ventana * SR)
    n = len(x) // w
    db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * w:(i + 1) * w] ** 2)) + 1e-9) for i in range(n)])
    print(f"duracion {dur:.2f} s | pico {20*np.log10(np.max(np.abs(x))+1e-9):.1f} dBFS | RMS global {20*np.log10(np.sqrt(np.mean(x**2))+1e-9):.1f} dBFS")
    try:
        print(f"pulso estimado: {pulso(x):.1f} BPM (todo el archivo)")
        for (s, e) in [(0, 17), (17, 70), (70, 82), (82, 123), (123, 150)]:
            seg = x[int(s * SR):int(min(e, dur) * SR)]
            if len(seg) > SR * 4:
                print(f"  pulso {s:>3}-{e:<3} s: {pulso(seg):.1f} BPM")
    except Exception as err:  # noqa: BLE001
        print("pulso: no se pudo estimar", err)
    paso = max(1, int(5 / a.ventana))
    print("RMS por tramo de 5 s (dBFS):")
    for i in range(0, n, paso):
        t = i * a.ventana
        print(f"  {t:6.1f}-{t+5:6.1f} s  {np.mean(db[i:i+paso]):6.1f}  {'#' * max(0, int((np.mean(db[i:i+paso]) + 60) / 1.5))}")
    if a.png:
        W, H = 1600, 420
        img = Image.new("RGB", (W, H), "#1c282e")
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", 16)
        X = lambda t: 40 + (W - 60) * t / max(dur, 150)
        Y = lambda v: 30 + (H - 70) * (0 - max(v, -60)) / 60
        for v in (0, -10, -20, -30, -40, -50, -60):
            d.line([(40, Y(v)), (W - 20, Y(v))], fill="#2d3c44")
            d.text((4, Y(v) - 8), f"{v}", font=f, fill="#6a7d88")
        for t in range(0, int(max(dur, 150)) + 1, 10):
            d.text((X(t) - 8, H - 30), f"{t}", font=f, fill="#6a7d88")
        for m in [float(v) for v in a.marcas.split(",") if v]:
            d.line([(X(m), 20), (X(m), H - 36)], fill="#f4a159", width=1)
        pts = [(X(i * a.ventana), Y(v)) for i, v in enumerate(db)]
        d.line(pts, fill="#62e4e0", width=2)
        d.text((48, 4), f"{a.audio.split('/')[-1]}  RMS {a.ventana} s (dBFS); lineas naranjas = marcas del montaje", font=f, fill="#f8c991")
        img.save(a.png)
        print("grafica:", a.png)


if __name__ == "__main__":
    main()
