"""Tabla compacta de todas las corridas guardadas (incluye las marcadas con error de resolucion).

Uso:  python pruebas/bench_render/tabla.py [carpeta_de_corridas]
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PROY = Path(__file__).resolve().parent


def main():
    carpetas = [Path(sys.argv[1])] if len(sys.argv) > 1 else sorted((PROY / "corridas").glob("run_*"), key=lambda p: p.stat().st_mtime)[-1:]
    filas = []
    for carpeta in carpetas:
        for archivo in sorted(carpeta.glob("*.json")):
            try:
                d = json.loads(archivo.read_text(encoding="utf-8"))
            except Exception:
                continue
            if "fps_mean" not in d:
                continue
            filas.append((d["rendering_method"], d["rendering_driver"], d["scene"],
                          f"{d['resolution']['width']}x{d['resolution']['height']}",
                          d["fps_mean"], d["fps_1pct_low"], d["frame_time_max_ms"],
                          d["draw_calls_mean"], d["primitives_mean"], d["video_memory_max_bytes"] / 1048576))
    print(f"{'metodo':17}{'driver':15}{'escena':9}{'resolucion':11}{'fps':>7}{'1%':>7}{'max ms':>8}{'draws':>7}{'prims':>9}{'MiB':>6}")
    for f in filas:
        print(f"{f[0]:17}{f[1]:15}{f[2]:9}{f[3]:11}{f[4]:7.1f}{f[5]:7.1f}{f[6]:8.0f}{f[7]:7.0f}{f[8]:9.0f}{f[9]:6.0f}")
    print(f"\n{len(filas)} corridas con medicion en {', '.join(str(c.name) for c in carpetas)}")


if __name__ == "__main__":
    main()
