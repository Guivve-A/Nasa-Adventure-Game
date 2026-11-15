"""Mide un archivo de audio sin escucharlo: envolvente, pico, RMS, centro espectral y tonos dominantes.

Sirve para comprobar que un efecto generado no quedo en silencio, donde empieza y acaba el sonido, y si es
un tono (pitido, campana) o ruido (paso, soplo, agua). No sustituye a escucharlo.

Uso:  python -I analizar.py <archivo> [<archivo> ...] [--fino]
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
TASA = 44100


def leer(ruta):
    """Decodifica con ffmpeg a mono float32 a 44,1 kHz."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ruta), "-ac", "1", "-ar", str(TASA), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def db(v):
    return 20.0 * np.log10(max(float(v), 1e-9))


def envolvente(x, ventana_s=0.05):
    n = int(ventana_s * TASA)
    trozos = [x[i:i + n] for i in range(0, len(x) - n + 1, n)]
    return [db(np.sqrt(np.mean(t ** 2))) for t in trozos]


def espectro(x):
    if len(x) < 256:
        return 0.0, []
    ventana = np.hanning(len(x))
    mag = np.abs(np.fft.rfft(x * ventana))
    frec = np.fft.rfftfreq(len(x), 1.0 / TASA)
    centro = float(np.sum(frec * mag) / max(np.sum(mag), 1e-12))
    # tonos: los picos mas altos, separados al menos 60 Hz
    orden = np.argsort(mag)[::-1]
    picos = []
    for i in orden[:4000]:
        if all(abs(frec[i] - f) > 60.0 for f, _ in picos):
            picos.append((float(frec[i]), db(mag[i] / max(mag.max(), 1e-12))))
        if len(picos) >= 5:
            break
    return centro, picos


def bandas(x):
    mag = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    frec = np.fft.rfftfreq(len(x), 1.0 / TASA)
    total = max(mag.sum(), 1e-20)
    cortes = [0, 150, 500, 2000, 6000, 22050]
    return [100.0 * mag[(frec >= a) & (frec < b)].sum() / total for a, b in zip(cortes[:-1], cortes[1:])]


def medir(ruta, fino=False):
    x = leer(ruta)
    dur = len(x) / TASA
    pico = db(np.max(np.abs(x))) if len(x) else -180.0
    rms = db(np.sqrt(np.mean(x ** 2))) if len(x) else -180.0
    env = envolvente(x, 0.02 if fino else 0.05)
    centro, picos = espectro(x)
    # cuanto del pico espectral se lleva el tono mayor: cerca de 1 = tono puro; bajo = ruido
    mag = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    tonalidad = float(mag.max() / max(np.sqrt(np.mean(mag ** 2)), 1e-12))
    print(f"== {Path(ruta).name}: {dur:.3f} s  pico {pico:.1f} dB  RMS {rms:.1f} dB  centro {centro:.0f} Hz  cresta-espectral {tonalidad:.1f}")
    print("   bandas % (<150, 150-500, 500-2k, 2k-6k, >6k): " + "  ".join(f"{b:.0f}" for b in bandas(x)))
    print("   tonos: " + "  ".join(f"{f:.0f} Hz ({d:.0f} dB)" for f, d in picos))
    paso = 0.02 if fino else 0.05
    print(f"   envolvente cada {int(paso * 1000)} ms (dB): " + " ".join(f"{e:.0f}" for e in env))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for ruta in args:
        medir(ruta, "--fino" in sys.argv)


if __name__ == "__main__":
    main()
