"""Genera con Higgsfield los efectos de sonido de un lote de audio, con tope de creditos y registro.

Lee lote_A1.json (al lado de este archivo), cotiza cada trabajo con `generate cost` (gratis), se niega a
generar si lo ya gastado en el lote mas lo cotizado supera el tope, genera de uno en uno, baja el original
(`result_url`) a originales/<id>.<ext> y anota cada generacion en registro.json.

Uso:
  python -I generar.py --solo-cotizar            cotiza todo el lote, sin gastar
  python -I generar.py                           genera lo que falte (no repite lo ya generado)
  python -I generar.py --solo paso,paso_luna     genera solo esos
  python -I generar.py --repetir paso            vuelve a generar uno ya hecho (gasta otra vez; guarda el anterior)
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
LOTE = AQUI / "lote_A1.json"
REGISTRO = AQUI / "registro.json"
ORIGINALES = AQUI / "originales"
CRUDOS = AQUI / "_json"

cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
if not cmd:
    raise SystemExit("No se encuentra higgsfield.cmd en el PATH")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe")


def hf(*args, timeout=900):
    r = subprocess.run([HF, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def args_de(modelo, trabajo):
    return [modelo, "--prompt", trabajo["prompt"], "--duration", str(trabajo["duracion"])]


def cotizar(modelo, trabajo):
    code, out, err = hf("generate", "cost", *args_de(modelo, trabajo), "--json", timeout=120)
    if code != 0:
        raise SystemExit(f"No se pudo cotizar {trabajo['id']}: {(err or out)[:200]}")
    return float(json.loads(out)["credits"])


def saldo():
    code, out, _ = hf("account", "status", "--json", timeout=60)
    try:
        return float(json.loads(out)["credits"])
    except Exception:  # noqa: BLE001
        return None


def leer_registro():
    return json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else []


def generar(modelo, trabajo, sufijo=""):
    ident = trabajo["id"] + sufijo
    code, out, err = hf("generate", "create", *args_de(modelo, trabajo), "--wait", "--wait-timeout", "10m", "--json")
    CRUDOS.mkdir(parents=True, exist_ok=True)
    (CRUDOS / f"{ident}.json").write_text(out or err, encoding="utf-8")
    fila = {"id": ident, "estado": "error", "url": None, "archivo": None, "job_id": None, "detalle": None}
    if code != 0:
        fila["detalle"] = (err or out)[:300]
        return fila
    original = re.search(r'"result_url"\s*:\s*"([^"]+)"', out)
    job = re.search(r'"id"\s*:\s*"([0-9a-f-]{36})"', out)
    fila["job_id"] = job.group(1) if job else None
    if not original:
        estado = re.search(r'"status"\s*:\s*"([a-z_]+)"', out)
        fila["detalle"] = f"sin result_url (status={estado.group(1) if estado else '?'})"
        return fila
    url = original.group(1)
    ext = re.search(r"\.([a-z0-9]{2,5})$", url.split("?")[0], re.I)
    ext = ext.group(1).lower() if ext else "bin"
    ORIGINALES.mkdir(parents=True, exist_ok=True)
    destino = ORIGINALES / f"{ident}.{ext}"
    try:
        peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(peticion, timeout=180) as r:
            destino.write_bytes(r.read())
        fila.update(estado="ok", url=url, archivo=f"originales/{destino.name}", bytes=destino.stat().st_size)
    except Exception as error:  # noqa: BLE001
        fila.update(estado="sin descargar", url=url, detalle=str(error)[:200])
    return fila


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-cotizar", action="store_true")
    ap.add_argument("--solo", default="")
    ap.add_argument("--repetir", default="", help="ids que se generan otra vez aunque ya esten hechos")
    a = ap.parse_args()
    spec = json.loads(LOTE.read_text(encoding="utf-8"))
    modelo = spec["modelo"]
    tope = float(spec["tope"])
    registro = leer_registro()
    hechos = {f["id"] for f in registro if f["estado"] == "ok"}
    repetir = set(a.repetir.split(",")) - {""}
    solo = set(a.solo.split(",")) - {""}
    trabajos = [t for t in spec["trabajos"] if (not solo or t["id"] in solo or t["id"] in repetir)]
    if repetir and not solo:
        trabajos = [t for t in trabajos if t["id"] in repetir]
    pendientes = [t for t in trabajos if t["id"] not in hechos or t["id"] in repetir]

    gastado = sum(float(f.get("costo", 0.0)) for f in registro if f["estado"] in ("ok", "sin descargar"))
    total = 0.0
    for t in pendientes:
        t["_costo"] = cotizar(modelo, t)
        total += t["_costo"]
        print(f"  cotizado {t['id']:20} {t['duracion']:>3} s  {t['_costo']:5.2f}", flush=True)
    print(f"Cotizado: {total:.2f}  |  ya gastado en el lote: {gastado:.2f}  |  tope: {tope:.2f}", flush=True)
    if gastado + total > tope + 1e-9:
        raise SystemExit("El lote superaria su tope: no se genera nada.")
    if a.solo_cotizar or not pendientes:
        return

    antes = saldo()
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    for t in pendientes:
        veces = sum(1 for f in registro if f["id"].split("#")[0] == t["id"])
        sufijo = f"#{veces + 1}" if veces else ""
        fila = generar(modelo, t, sufijo.replace("#", "_v") if sufijo else "")
        fila.update(lote=spec["lote"], fecha=ahora, modelo=modelo, duracion=t["duracion"], prompt=t["prompt"],
                    costo=t["_costo"] if fila["estado"] != "error" else 0.0)
        if sufijo:
            fila["id"] = t["id"] + sufijo
        registro.append(fila)
        # se escribe tras cada trabajo: un fallo posterior no borra lo ya cobrado
        REGISTRO.write_text(json.dumps(registro, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  {fila['id']:20} {fila['estado']:14} {fila['archivo'] or fila['detalle']}", flush=True)
    despues = saldo()
    if antes is not None and despues is not None:
        print(f"Saldo: {antes:.2f} -> {despues:.2f} (gastado {antes - despues:.2f})", flush=True)


if __name__ == "__main__":
    main()
