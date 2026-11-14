"""Efemerides de la Luna vistas desde el Mirador del Faro (Guayaquil), con la API de JPL Horizons.

Ademas calcula hacia donde apunta el borde iluminado respecto de la vertical del lugar, con el
angulo paralactico. Cerca del ecuador la Luna creciente se ve tumbada, como una sonrisa.
Opcionalmente consulta Dial-A-Moon (NASA SVS) para una hora concreta.

Uso (horas en UT; Guayaquil = UT - 5 h):
  python herramientas/luna_efemerides.py --inicio "2026-11-12 23:00" --fin "2026-11-13 03:00" --paso "30 m" --dialamoon 2026-11-13T00:30
Salida: Nasa_Game/Propuestas/Datos/luna_<inicio>.json y horizons_<inicio>.txt (respuesta cruda).
"""
import argparse
import datetime as dt
import json
import math
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "Nasa_Game" / "Propuestas" / "Datos"

# Faro del cerro Santa Ana: punto publico de referencia para el Mirador del Faro
LAT, LON, ALT_KM = -2.1797, -79.8770, 0.06
API = "https://ssd.jpl.nasa.gov/api/horizons.api"
DIALAMOON = "https://svs.gsfc.nasa.gov/api/dialamoon/{}"
CIELO = {"*": "día", "C": "crepúsculo civil", "N": "crepúsculo náutico", "A": "crepúsculo astronómico", "": "noche"}


def pedir(url):
    req = urllib.request.Request(url, headers={"User-Agent": "efemerides-luna/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def horizons(inicio, fin, paso):
    p = {"format": "json", "COMMAND": "'301'", "OBJ_DATA": "'NO'", "MAKE_EPHEM": "'YES'",
         "EPHEM_TYPE": "'OBSERVER'", "CENTER": "'coord@399'", "COORD_TYPE": "'GEODETIC'",
         "SITE_COORD": f"'{LON % 360:.4f},{LAT:.4f},{ALT_KM}'", "START_TIME": f"'{inicio}'",
         "STOP_TIME": f"'{fin}'", "STEP_SIZE": f"'{paso}'", "QUANTITIES": "'2,4,10,13,14,15,16,17,20,23,24,42'",
         "CSV_FORMAT": "'YES'", "ANG_FORMAT": "'DEG'", "RANGE_UNITS": "'KM'"}
    url = API + "?" + urllib.parse.urlencode(p)
    datos = json.loads(pedir(url))
    if "error" in datos:
        raise SystemExit("Horizons: " + datos["error"])
    return url, datos


def tabla(texto):
    lineas = texto.splitlines()
    i0, i1 = lineas.index("$$SOE"), lineas.index("$$EOE")
    cab = next(linea for linea in reversed(lineas[:i0]) if "Date__" in linea)
    nombres = [c.strip() or f"col{i}" for i, c in enumerate(cab.split(","))]
    return [dict(zip(nombres, [v.strip() for v in linea.split(",")])) for linea in lineas[i0 + 1:i1]]


def col(fila, fragmento):
    for clave, valor in fila.items():
        if fragmento in clave:
            return valor
    raise KeyError(f"{fragmento} no esta entre las columnas {list(fila)}")


def horas(valor):
    partes = valor.split()
    if len(partes) == 3:
        signo = -1 if partes[0].startswith("-") else 1
        return signo * (abs(float(partes[0])) + float(partes[1]) / 60 + float(partes[2]) / 3600)
    return float(valor)


def fase(ilum, creciente):
    if ilum < 1:
        return "luna nueva"
    if ilum > 99:
        return "luna llena"
    if 47 <= ilum <= 53:
        return "cuarto creciente" if creciente else "cuarto menguante"
    if ilum < 47:
        return "creciente" if creciente else "menguante"
    return "gibosa creciente" if creciente else "gibosa menguante"


def lado(angulo):
    # 0 = arriba; crece hacia la izquierda, como el angulo de posicion visto en el cielo
    nombres = ["arriba", "arriba a la izquierda", "a la izquierda", "abajo a la izquierda",
               "abajo", "abajo a la derecha", "a la derecha", "arriba a la derecha"]
    return nombres[int(((angulo % 360) + 22.5) // 45) % 8]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inicio", required=True)
    ap.add_argument("--fin", required=True)
    ap.add_argument("--paso", default="30 m")
    ap.add_argument("--dialamoon", default="", help="Hora UT para Dial-A-Moon, p. ej. 2026-11-13T00:30")
    ap.add_argument("--salida", default=str(SALIDA), help="Carpeta de salida; para pruebas, una temporal")
    a = ap.parse_args()
    carpeta = Path(a.salida)
    carpeta.mkdir(parents=True, exist_ok=True)
    url, datos = horizons(a.inicio, a.fin, a.paso)
    marca = a.inicio.replace(" ", "_").replace(":", "")
    (carpeta / f"horizons_{marca}.txt").write_text(datos["result"], encoding="utf-8")

    filas, phi = [], math.radians(LAT)
    for f in tabla(datos["result"]):
        ut = dt.datetime.strptime(col(f, "Date__"), "%Y-%b-%d %H:%M")
        dec = math.radians(float(col(f, "DEC")))
        h = math.radians(horas(col(f, "Hour_Ang")) * 15)
        # angulo paralactico: posicion del cenit vista desde la Luna, medida desde el norte celeste hacia el este
        q = math.degrees(math.atan2(math.sin(h), math.tan(phi) * math.cos(dec) - math.sin(dec) * math.cos(h)))
        chi = float(col(f, "SN.ang"))
        borde = (chi - q) % 360
        ilum = float(col(f, "Illu%"))
        creciente = "T" in col(f, "/r").upper()
        filas.append({
            "ut": ut.strftime("%Y-%m-%d %H:%M"),
            "guayaquil": (ut - dt.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "cielo": CIELO.get(f.get("col1", "").strip(), f.get("col1", "")),
            "elevacion_deg": round(float(col(f, "Elev_")), 1),
            "azimut_deg": round(float(col(f, "Azi_")), 1),
            "iluminacion_pct": round(ilum, 1),
            "fase": fase(ilum, creciente),
            "elongacion_deg": round(float(col(f, "S-O-T")), 1),
            "angulo_fase_deg": round(float(col(f, "S-T-O")), 1),
            "distancia_km": round(float(col(f, "delta"))),
            "diametro_arcmin": round(float(col(f, "Ang-diam")) / 60, 2),
            "subobservador_lon_deg": round(float(col(f, "ObsSub-LON")), 2),
            "subobservador_lat_deg": round(float(col(f, "ObsSub-LAT")), 2),
            "subsolar_lon_deg": round(float(col(f, "SunSub-LON")), 2),
            "subsolar_lat_deg": round(float(col(f, "SunSub-LAT")), 2),
            "pa_polo_norte_deg": round(float(col(f, "NP.ang")), 3),
            "pa_borde_iluminado_deg": round(chi, 3),
            "angulo_paralactico_deg": round(q, 3),
            "borde_iluminado_desde_cenit_deg": round(borde, 2),
            "borde_iluminado_se_ve": lado(borde),
        })

    dial = None
    if a.dialamoon:
        try:
            dial = json.loads(pedir(DIALAMOON.format(a.dialamoon)))
        except Exception as error:  # noqa: BLE001
            dial = {"error": str(error)}

    salida = {"sitio": {"nombre": "Mirador del Faro (faro del cerro Santa Ana, Guayaquil)", "lat": LAT, "lon": LON,
                        "alt_km": ALT_KM},
              "fuente": {"servicio": "JPL Horizons API", "url": url, "firma": datos.get("signature", {})},
              "filas": filas, "dialamoon": dial}
    (carpeta / f"luna_{marca}.json").write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")

    firma = datos.get("signature", {})
    print(f"JPL Horizons {firma.get('source', '')} {firma.get('version', '')} · sitio {LAT}, {LON}")
    print(f"{'Guayaquil':17}{'cielo':24}{'elev':>6}{'ilum %':>8}  {'fase':18}{'dist km':>9}{'diam':>7}  borde iluminado")
    for r in filas:
        print(f"{r['guayaquil']:17}{r['cielo']:24}{r['elevacion_deg']:6.1f}{r['iluminacion_pct']:8.1f}  "
              f"{r['fase']:18}{r['distancia_km']:9d}{r['diametro_arcmin']:7.2f}  "
              f"{r['borde_iluminado_desde_cenit_deg']:5.0f} grados ({r['borde_iluminado_se_ve']})")
    if dial:
        print("\nDial-A-Moon:", json.dumps({k: v for k, v in dial.items() if k != "image"}, ensure_ascii=False)[:900])
        if isinstance(dial.get("image"), dict):
            print("Imagen:", {k: dial["image"].get(k) for k in ("url", "filename", "width", "height")})


if __name__ == "__main__":
    main()
