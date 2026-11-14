"""Sube imagenes de entrada a Higgsfield una sola vez y guarda sus ids en un JSON del lote.

Para encargos con muchas referencias (por ejemplo, vistas para imagen->3D): asi la cotizacion y la
generacion usan el id y no vuelven a subir el archivo. Los PNG se suben como JPEG de calidad 92,
que pesan una fraccion y no cambian el resultado. Reintenta los fallos de red (HTTP 520).
No gasta creditos.

Uso:  python herramientas/hf_subir.py <subidas.json> <imagen> [<imagen> ...]
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe")


def como_jpeg(ruta: Path) -> Path:
    if ruta.suffix.lower() in (".jpg", ".jpeg"):
        return ruta
    destino = ruta.parent / "jpg" / (ruta.stem + ".jpg")
    destino.parent.mkdir(parents=True, exist_ok=True)
    Image.open(ruta).convert("RGB").save(destino, quality=92)
    return destino


def subir(ruta: Path, intentos=3):
    for k in range(intentos):
        r = subprocess.run([HF, "upload", "create", str(ruta), "--json"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
        if r.returncode == 0:
            return json.loads(r.stdout)["id"], None
        error = (r.stderr or r.stdout).strip()[:200]
        time.sleep(3 * (k + 1))
    return None, error


def main():
    destino = Path(sys.argv[1])
    mapa = json.loads(destino.read_text(encoding="utf-8")) if destino.exists() else {}
    for arg in sys.argv[2:]:
        ruta = Path(arg)
        if ruta.stem in mapa:
            print(f"{ruta.stem:28} ya subida: {mapa[ruta.stem]['id']}")
            continue
        jpg = como_jpeg(ruta)
        ident, error = subir(jpg)
        if ident is None:
            print(f"{ruta.stem:28} ERROR {error}")
            continue
        mapa[ruta.stem] = {"id": ident, "archivo": jpg.as_posix(), "bytes": jpg.stat().st_size}
        print(f"{ruta.stem:28} {ident}  ({jpg.stat().st_size // 1024} KB)")
        destino.write_text(json.dumps(mapa, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
