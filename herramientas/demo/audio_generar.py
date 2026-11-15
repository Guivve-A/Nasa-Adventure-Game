"""Genera con Higgsfield la musica y los efectos del video demo, con tope de creditos y registro.

Lee Nasa_Game/Presentacion/audio/lote_demo.json, cotiza cada trabajo con `generate cost` (gratis), se niega a
generar si lo ya gastado en el lote mas lo cotizado supera el tope (40 creditos para todo el demo), genera de uno
en uno con --wait, baja el original (`result_url`) a audio/originales/<id>.<ext> y anota cada generacion en
audio/registro_audio.json (modelo, parametros, prompt, costo, saldo antes y despues).

Uso:
  python -I herramientas/demo/audio_generar.py --solo-cotizar
  python -I herramientas/demo/audio_generar.py --solo musica_demo
  python -I herramientas/demo/audio_generar.py                     genera lo que falte
  python -I herramientas/demo/audio_generar.py --repetir grillos    vuelve a generar (gasta otra vez)
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
RAIZ = Path(__file__).resolve().parents[2]
AUDIO = RAIZ / "Nasa_Game" / "Presentacion" / "audio"
LOTE = AUDIO / "lote_demo.json"
REGISTRO = AUDIO / "registro_audio.json"
ORIGINALES = AUDIO / "originales"
CRUDOS = AUDIO / "_json"

cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
if not cmd:
    raise SystemExit("No se encuentra higgsfield.cmd en el PATH")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe")


def hf(*args, timeout=1500):
    r = subprocess.run([HF, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def args_de(t):
    return [t["modelo"], "--prompt", t["prompt"], "--duration", str(t["duracion"]), *t.get("extra", [])]


def cotizar(t):
    code, out, err = hf("generate", "cost", *args_de(t), "--json", timeout=120)
    if code != 0:
        raise SystemExit(f"No se pudo cotizar {t['id']}: {(err or out)[:200]}")
    return float(json.loads(out)["credits"])


def saldo():
    _, out, _ = hf("account", "status", "--json", timeout=60)
    try:
        return float(json.loads(out)["credits"])
    except Exception:  # noqa: BLE001
        return None


def leer_registro():
    return json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else []


def generar(t, ident):
    code, out, err = hf("generate", "create", *args_de(t), "--wait", "--wait-timeout", "20m", "--json")
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
        with urllib.request.urlopen(peticion, timeout=300) as r:
            destino.write_bytes(r.read())
        fila.update(estado="ok", url=url, archivo=f"originales/{destino.name}", bytes=destino.stat().st_size)
    except Exception as error:  # noqa: BLE001
        fila.update(estado="sin descargar", url=url, detalle=str(error)[:200])
    return fila


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-cotizar", action="store_true")
    ap.add_argument("--solo", default="")
    ap.add_argument("--repetir", default="")
    a = ap.parse_args()
    spec = json.loads(LOTE.read_text(encoding="utf-8"))
    tope = float(spec["tope"])
    registro = leer_registro()
    hechos = {re.sub(r"_v\d+$", "", f["id"]) for f in registro if f["estado"] == "ok"}
    solo = set(a.solo.split(",")) - {""}
    repetir = set(a.repetir.split(",")) - {""}
    trabajos = spec["trabajos"]
    if solo or repetir:
        trabajos = [t for t in trabajos if t["id"] in solo | repetir]
    pendientes = [t for t in trabajos if t["id"] not in hechos or t["id"] in repetir]

    gastado = sum(float(f.get("costo", 0.0)) for f in registro if f["estado"] in ("ok", "sin descargar"))
    total = 0.0
    for t in pendientes:
        t["_costo"] = cotizar(t)
        total += t["_costo"]
        print(f"  cotizado {t['id']:16} {t['modelo']:24} {t['duracion']:>4} s  {t['_costo']:6.2f}", flush=True)
    print(f"Cotizado: {total:.2f} | ya gastado en el demo: {gastado:.2f} | tope: {tope:.2f}", flush=True)
    if gastado + total > tope + 1e-9:
        raise SystemExit("Se superaria el tope del demo: no se genera nada.")
    if a.solo_cotizar or not pendientes:
        return

    for t in pendientes:
        veces = sum(1 for f in registro if f["id"] == t["id"] or f["id"].startswith(t["id"] + "_v"))
        ident = t["id"] + (f"_v{veces + 1}" if veces else "")
        antes = saldo()
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        fila = generar(t, ident)
        despues = saldo()
        fila.update(lote=spec["lote"], fecha=ahora, modelo=t["modelo"], duracion=t["duracion"], prompt=t["prompt"],
                    extra=t.get("extra", []), cotizado=t["_costo"], saldo_antes=antes, saldo_despues=despues,
                    costo=t["_costo"] if fila["estado"] != "error" else 0.0)
        if fila["estado"] == "error" and antes is not None and despues is not None and antes - despues > 0.001:
            fila["costo"] = round(antes - despues, 2)
        registro.append(fila)
        REGISTRO.write_text(json.dumps(registro, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  {ident:16} {fila['estado']:14} {fila['archivo'] or fila['detalle']}  saldo {antes} -> {despues}", flush=True)


if __name__ == "__main__":
    main()
