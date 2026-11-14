import json
from pathlib import Path

import numpy as np
from PIL import Image


CARPETA = Path(__file__).resolve().parent


def cargar(nombre):
    return np.asarray(Image.open(CARPETA / nombre).convert("RGB"), dtype=np.int16)


def diferencia(antes, despues):
    delta = np.abs(antes - despues)
    return {
        "mae_rgb_255": float(delta.mean()),
        "mae_normalizado": float(delta.mean() / 255),
        "porcentaje_pixeles_distintos": float(np.any(delta > 0, axis=2).mean() * 100),
        "porcentaje_pixeles_delta_mayor_2": float(np.any(delta > 2, axis=2).mean() * 100),
        "maximo_canal": int(delta.max()),
    }


resultados = {}
for encuadre in ("21", "12"):
    casos = {}
    for caso in ("normal", "fijo", "viento", "sin_inclinacion"):
        sufijo = "" if caso == "normal" else "_" + caso
        antes = cargar(f"antes_{encuadre}{sufijo}.png")
        despues = cargar(f"despues_{encuadre}{sufijo}.png")
        casos[caso] = diferencia(antes, despues)
        if caso == "fijo":
            delta = np.clip(np.abs(antes - despues) * 8, 0, 255).astype(np.uint8)
            Image.fromarray(delta).save(CARPETA / f"diferencia_{encuadre}_x8.png")
    for version in ("antes", "despues"):
        fijo = cargar(f"{version}_{encuadre}_fijo.png")
        casos[f"efecto_viento_{version}"] = diferencia(
            fijo, cargar(f"{version}_{encuadre}_viento.png")
        )
        casos[f"efecto_inclinacion_{version}"] = diferencia(
            fijo, cargar(f"{version}_{encuadre}_sin_inclinacion.png")
        )
    resultados[encuadre] = casos

salida = json.dumps(resultados, indent=2, ensure_ascii=False) + "\n"
(CARPETA / "diferencias.json").write_text(salida, encoding="utf-8")
print(salida)
