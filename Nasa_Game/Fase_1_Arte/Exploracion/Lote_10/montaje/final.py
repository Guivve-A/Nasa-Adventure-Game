# Une los segmentos con cortes y dos disolvencias de 1,5 s; tono de sala muy bajo. 0 creditos.
import subprocess
from pathlib import Path
SEG = Path(__file__).parent / "seg"
OUT = Path(r"C:\Users\guill\Desktop\Juego 2d-hd\Nasa_Game\Fase_1_Arte\Exploracion\Lote_10\montaje_mov_I_II.mp4")
ins = []
for n in ["S03", "S04", "S05", "S06", "S07", "S08", "S09"]:
    ins += ["-i", str(SEG / f"{n}.mkv")]
# tono de sala: ruido marron, paso bajo, unos -58 dBFS
ins += ["-f", "lavfi", "-i", "anoisesrc=color=brown:amplitude=0.02:sample_rate=48000:duration=52"]
norm = ",".join(["fps=24", "format=yuv420p10le", "setsar=1", "settb=1/24"])
fc = []
for i in range(7):
    fc.append(f"[{i}:v]{norm}[v{i}]")
fc.append("[v0][v1][v2][v3]concat=n=4:v=1:a=0,settb=1/24[a1]")          # 0 a 29,75 (P06 con 0,75 s de cola)
fc.append("[a1][v4]xfade=transition=fade:duration=1.5:offset=28.25,settb=1/24[a2]")   # P06 -> P07, centrada en 29,0
fc.append("[a2][v5]xfade=transition=fade:duration=1.5:offset=36.25[a3]")   # P07 -> P08, centrada en 37,0
fc.append("[a3][v6]concat=n=2:v=1:a=0,format=yuv420p[vout]")               # P08 -> P09 corte seco en 43,0
fc.append("[7:a]lowpass=f=300,highpass=f=40,volume=0.5,afade=t=in:d=1,afade=t=out:st=51:d=1,aformat=channel_layouts=stereo[aout]")
cmd = ["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
       "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "24",
       "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", "-t", "52", str(OUT)]
subprocess.run(cmd, check=True)
print("ok", OUT)

