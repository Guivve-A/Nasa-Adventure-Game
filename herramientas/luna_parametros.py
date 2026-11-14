"""Prepara los datos de la Luna para la escena del telescopio en Godot.

Toma la fila de una hora local de la consulta a Horizons (luna_efemerides.py), calcula la hora de
puesta con el criterio de los almanaques (el borde superior toca el horizonte, con 34' de refraccion
estandar) y escribe datos/luna.json.

Uso:  python herramientas/luna_parametros.py <luna_*.json de Horizons> "2026-11-12 19:30" <proyecto_godot>
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def main():
    origen, hora, proyecto = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    datos = json.loads(origen.read_text(encoding="utf-8"))
    filas = datos["filas"]
    fila = next(f for f in filas if f["guayaquil"] == hora)

    puesta = None
    for f1, f2 in zip(filas, filas[1:]):
        # altura del centro (sin refraccion) a la que el borde superior toca el horizonte aparente
        umbral = -(34 + f1["diametro_arcmin"] / 2) / 60
        e1, e2 = f1["elevacion_deg"] - umbral, f2["elevacion_deg"] - umbral
        if e1 > 0 >= e2:
            t1 = datetime.strptime(f1["guayaquil"], "%Y-%m-%d %H:%M")
            t2 = datetime.strptime(f2["guayaquil"], "%Y-%m-%d %H:%M")
            puesta = t1 + (t2 - t1) * (e1 / (e1 - e2))
            break

    salida = dict(fila)
    salida["puesta_guayaquil"] = (puesta + timedelta(seconds=30)).strftime("%H:%M") if puesta else None
    salida["criterio_puesta"] = "borde superior con refracción estándar de 34′, como en los almanaques"
    salida["sitio"] = datos["sitio"]["nombre"]
    salida["fuente"] = "JPL Horizons (DE441) · texturas NASA SVS 4720 (LRO LROC y LOLA)"
    destino = proyecto / "datos" / "luna.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{destino}: {fila['guayaquil']}, iluminada {fila['iluminacion_pct']} %, "
          f"borde a {fila['borde_iluminado_desde_cenit_deg']} grados, puesta {salida['puesta_guayaquil']}")


if __name__ == "__main__":
    main()
