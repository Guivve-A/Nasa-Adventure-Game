"""Mide las texturas que trae un GLB: tamano, media y desviacion por canal.

Tripo a veces devuelve una textura gris plana (media ~102, desviacion ~3) sin avisar. Con una
desviacion por debajo de 12 la textura se marca como FALLIDA. Opcionalmente extrae las imagenes.

Uso:  python herramientas/mallas/revisar_textura_glb.py <malla.glb> [--extraer <carpeta>]
"""
import io
import json
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")


def leer_glb(ruta: Path):
    datos = ruta.read_bytes()
    magia, version, largo = struct.unpack_from("<III", datos, 0)
    if magia != 0x46546C67:
        raise SystemExit(f"{ruta} no es un GLB")
    pos, js, binario = 12, None, b""
    while pos < largo:
        n, tipo = struct.unpack_from("<II", datos, pos)
        trozo = datos[pos + 8:pos + 8 + n]
        if tipo == 0x4E4F534A:
            js = json.loads(trozo)
        elif tipo == 0x004E4942:
            binario = trozo
        pos += 8 + n
    return js, binario


def main():
    ruta = Path(sys.argv[1])
    extraer = Path(sys.argv[sys.argv.index("--extraer") + 1]) if "--extraer" in sys.argv else None
    js, binario = leer_glb(ruta)
    malla_tri = 0
    for m in js.get("meshes", []):
        for p in m["primitives"]:
            if "indices" in p:
                malla_tri += js["accessors"][p["indices"]]["count"] // 3
    print(f"{ruta.name}: {len(js.get('meshes', []))} mallas, {malla_tri} triangulos, "
          f"{len(js.get('materials', []))} materiales, {len(js.get('images', []))} imagenes")
    fallidas = 0
    for k, im in enumerate(js.get("images", [])):
        vista = js["bufferViews"][im["bufferView"]]
        crudo = binario[vista.get("byteOffset", 0):vista.get("byteOffset", 0) + vista["byteLength"]]
        img = Image.open(io.BytesIO(crudo)).convert("RGB")
        a = np.asarray(img).astype(float)
        media, desv = a.reshape(-1, 3).mean(0), a.reshape(-1, 3).std(0)
        estado = "FALLIDA" if desv.mean() < 12 else "ok"
        fallidas += estado == "FALLIDA"
        print(f"  imagen {k} ({im.get('mimeType', '?')}, {img.size[0]}x{img.size[1]}): "
              f"media {media.round(1).tolist()} desviacion {desv.round(1).tolist()} -> {estado}")
        if extraer:
            extraer.mkdir(parents=True, exist_ok=True)
            img.save(extraer / f"{ruta.stem}_textura_{k}.png")
    sys.exit(1 if fallidas else 0)


if __name__ == "__main__":
    main()
