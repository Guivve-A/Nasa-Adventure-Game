"""Sube imagenes ancla a Higgsfield una sola vez y guarda su id en Nasa_Game/Fase_1_Arte/anclas.json.

Las anclas son las imagenes aprobadas que se pasan como referencia en cada encargo para mantener
el estilo. En los lotes se citan como "@NOMBRE" y hf_generar.py las resuelve.

Uso:  python herramientas/hf_anclas.py NOMBRE=ruta [NOMBRE=ruta ...]
"""
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
ANCLAS = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "anclas.json"

cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe")


def main():
    anclas = json.loads(ANCLAS.read_text(encoding="utf-8")) if ANCLAS.exists() else {}
    for par in sys.argv[1:]:
        nombre, _, ruta = par.partition("=")
        r = subprocess.run([HF, "upload", "create", ruta, "--json"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
        if r.returncode != 0:
            print(f"{nombre}: error {(r.stderr or r.stdout).strip()[:200]}")
            continue
        datos = json.loads(r.stdout)
        anclas[nombre] = {"id": datos["id"], "archivo": Path(ruta).as_posix(),
                          "subida": datetime.date.today().isoformat()}
        print(f"{nombre:18} {datos['id']}  <- {ruta}")
    ANCLAS.parent.mkdir(parents=True, exist_ok=True)
    ANCLAS.write_text(json.dumps(anclas, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
