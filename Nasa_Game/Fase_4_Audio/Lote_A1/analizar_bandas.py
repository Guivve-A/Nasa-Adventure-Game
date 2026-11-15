"""Envolvente por bandas de un archivo de audio (para ver ciclos lentos: respiracion, olas, cantos).

Uso:  python -I analizar_bandas.py <archivo> [ventana_s]
"""
import sys

import numpy as np

from analizar import TASA, db, leer

sys.stdout.reconfigure(encoding="utf-8")
BANDAS = [(20, 150), (150, 500), (500, 2000), (2000, 6000), (6000, 20000)]


def filtrar(x, bajo, alto):
    espectro = np.fft.rfft(x)
    frec = np.fft.rfftfreq(len(x), 1.0 / TASA)
    espectro[(frec < bajo) | (frec >= alto)] = 0.0
    return np.fft.irfft(espectro, len(x))


def main():
    ruta = sys.argv[1]
    ventana = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
    x = leer(ruta)
    n = int(ventana * TASA)
    print(f"{ruta}: {len(x) / TASA:.2f} s, ventana {ventana} s")
    for bajo, alto in BANDAS:
        y = filtrar(x, bajo, alto)
        env = [db(np.sqrt(np.mean(y[i:i + n] ** 2))) for i in range(0, len(y) - n + 1, n)]
        print(f"  {bajo:>5}-{alto:<5} Hz  RMS {db(np.sqrt(np.mean(y ** 2))):6.1f} dB | " + " ".join(f"{e:.0f}" for e in env))


if __name__ == "__main__":
    main()
