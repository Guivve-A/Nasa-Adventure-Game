# Hoja de contacto: un cuadro por segundo (en el medio de cada segundo) con el plano debajo.
import subprocess, sys
from pathlib import Path
L10 = Path(r"C:\Users\guill\Desktop\Juego 2d-hd\Nasa_Game\Fase_1_Arte\Exploracion\Lote_10")
VID = L10 / "montaje_mov_I_II.mp4"
OUT = L10 / "montaje_mov_I_II_hoja.jpg"
TMP = Path(__file__).parent / "hoja"
TMP.mkdir(exist_ok=True)
PLANOS = [("P03", 0, 9), ("P04", 9, 16.5), ("P05", 16.5, 23), ("P06", 23, 29), ("P07", 29, 37), ("P08", 37, 43), ("P09", 43, 52)]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VID), "-vf", "select=eq(mod(n\\,24)\\,12),scale=320:180", "-fps_mode", "passthrough",
                "-frames:v", "52", str(TMP / "c%02d.png")], check=True)
args = ["magick", "montage"]
for s in range(52):
    t = s + 0.5
    pl = next(p for p, a, b in PLANOS if a <= t < b)
    seg = 15 + s
    args += ["-label", f"{pl}  {seg // 60}:{seg % 60:02d}", str(TMP / f"c{s + 1:02d}.png")]
args += ["-tile", "8x", "-geometry", "320x180+4+4", "-background", "#111111", "-fill", "#dddddd",
         "-pointsize", "16", "-font", "Arial", "-quality", "90", str(OUT)]
subprocess.run(args, check=True)
print("ok", OUT)


