"""Corridas extra del benchmark: D3D12 y 1080p real a pantalla completa.

Uso:  python pruebas/bench_render/extras.py <godot.exe>
Salida: pruebas/bench_render/resultados_extra.md y corridas/extra/*.json
"""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PROY = Path(__file__).resolve().parent
OUT = PROY / "corridas" / "extra"
OUT.mkdir(parents=True, exist_ok=True)

# (metodo, driver, resolucion, modo de ventana, escena)
CORRIDAS = [
    ("mobile", "d3d12", "1280x720", "--windowed", "base"),
    ("mobile", "d3d12", "1280x720", "--windowed", "hierba"),
    ("mobile", "d3d12", "1280x720", "--windowed", "sprites"),
    ("forward_plus", "d3d12", "1280x720", "--windowed", "hierba"),
    ("mobile", "vulkan", "1920x1080", "--fullscreen", "base"),
    ("mobile", "vulkan", "1920x1080", "--fullscreen", "hierba"),
    ("mobile", "d3d12", "1920x1080", "--fullscreen", "hierba"),
    ("gl_compatibility", "opengl3", "1920x1080", "--fullscreen", "base"),
    ("gl_compatibility", "opengl3", "1920x1080", "--fullscreen", "hierba"),
]


def main():
    godot = sys.argv[1]
    filas = []
    for metodo, driver, res, modo, escena in CORRIDAS:
        nombre = f"{metodo}_{driver}_{res}_{escena}"
        salida = OUT / f"{nombre}.json"
        if salida.exists():
            salida.unlink()
        cmd = [godot, "--path", str(PROY), "--rendering-method", metodo, "--rendering-driver", driver,
               "--resolution", res, modo, "--", f"--escena={escena}", "--segundos=10", f"--salida={salida}"]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=150)
        except subprocess.TimeoutExpired:
            filas.append((nombre, "timeout", "", "", "", "", ""))
            print(f"{nombre}: timeout", flush=True)
            continue
        if not salida.exists():
            filas.append((nombre, "sin resultado", "", "", "", "", ""))
            print(f"{nombre}: sin resultado", flush=True)
            continue
        d = json.loads(salida.read_text(encoding="utf-8"))
        fila = (nombre, "ok", f"{d['fps_mean']:.1f}", f"{d['fps_1pct_low']:.1f}", f"{d['frame_time_max_ms']:.0f}",
                f"{d['resolution']['width']}x{d['resolution']['height']}", d["rendering_driver"])
        filas.append(fila)
        print(" | ".join(fila), flush=True)
    md = ["| Corrida | Estado | FPS medio | FPS 1 % | Cuadro max ms | Resolucion efectiva | Controlador |", "|---|---|---:|---:|---:|---|---|"]
    md += ["| " + " | ".join(f) + " |" for f in filas]
    (PROY / "resultados_extra.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
