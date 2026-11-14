"""Descarga archivos publicos de NASA a carpetas propias y deja su procedencia.

Cada archivo va a su propia carpeta nueva dentro de externos/ (datos no confiables: no se ejecuta
nada desde ahi). Comprueba que el tamano coincida con el anunciado por el servidor y calcula SHA-256.
La procedencia queda en Nasa_Game/Propuestas/Datos/descargas_nasa.json.

Uso:  python herramientas/descargar_nasa.py
"""
import datetime
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "Nasa_Game" / "Propuestas" / "Datos" / "descargas_nasa.json"

# (url, carpeta, pagina de origen) aprobados por Guillermo el 2026-11-12
ARCHIVOS = [
    ("https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/lroc_color_poles_4k.tif",
     "externos/nasa_svs_4720_color", "https://svs.gsfc.nasa.gov/4720"),
    ("https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/ldem_4.tif",
     "externos/nasa_svs_4720_relieve", "https://svs.gsfc.nasa.gov/4720"),
    ("https://svs.gsfc.nasa.gov/vis/a000000/a005500/a005587/mooninfo_2026.json",
     "externos/nasa_svs_5587_tabla", "https://svs.gsfc.nasa.gov/5587"),
]


def main():
    registro = json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else []
    for url, carpeta, pagina in ARCHIVOS:
        destino_dir = RAIZ / carpeta
        destino_dir.mkdir(parents=True, exist_ok=True)
        destino = destino_dir / url.rsplit("/", 1)[-1]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        h = hashlib.sha256()
        with urllib.request.urlopen(req, timeout=300) as r, open(destino, "wb") as f:
            anunciado = int(r.headers.get("Content-Length") or -1)
            while True:
                bloque = r.read(1 << 20)
                if not bloque:
                    break
                f.write(bloque)
                h.update(bloque)
        tam = destino.stat().st_size
        ok = anunciado in (-1, tam)
        registro.append({"archivo": destino.relative_to(RAIZ).as_posix(), "url": url, "pagina": pagina,
                         "bytes": tam, "bytes_anunciados": anunciado, "sha256": h.hexdigest(),
                         "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                         "aprobado_por": "Guillermo, 2026-11-12 («Sí, descárgalos»)"})
        print(f"{'ok ' if ok else 'TAMANO DISTINTO'} {destino.relative_to(RAIZ).as_posix():58} {tam:>10} bytes  sha256 {h.hexdigest()[:16]}…")
    REGISTRO.write_text(json.dumps(registro, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
