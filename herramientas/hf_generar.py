"""Genera un lote de imagenes con Higgsfield, con tope de creditos y registro.

Lee un archivo JSON con el lote, cotiza cada trabajo, se niega a generar si la suma
supera el tope, genera en paralelo, descarga cada resultado y deja trazabilidad en
Nasa_Game/Fase_1_Arte/registro_generaciones.json.

Formato del lote:
{
  "lote": "L01",
  "carpeta": "Nasa_Game/Fase_1_Arte/Exploracion/Lote_01",
  "tope": 20,
  "trabajos": [
    {"id": "L01_A_lowpoly", "modelo": "gpt_image_2_6",
     "params": {"aspect_ratio": "16:9", "resolution": "2k", "quality": "high"},
     "imagenes": ["ruta_o_id_opcional"], "prompt": "..."}
  ]
}

Uso:  python herramientas/hf_generar.py <lote.json> [--solo-cotizar] [--solo id1,id2]
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "registro_generaciones.json"
# Bloques de texto fijos ({NOMBRE} en el prompt) y anclas de estilo ya subidas ("@NOMBRE" en imagenes)
BLOQUES = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "bloques_prompt.json"
ANCLAS = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "anclas.json"

cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe")
URL_MEDIA = re.compile(r'https?://[^"\s\\]+\.(?:png|jpe?g|webp|gif|glb|gltf|fbx|obj|zip|usdz|mp4|mp3|wav)(?:\?[^"\s\\]*)?', re.I)


def hf(*args, timeout=1200):
    r = subprocess.run([HF, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def expandir(texto):
    """Reemplaza {NOMBRE} por el bloque fijo del mismo nombre; falla si queda alguno sin definir."""
    if BLOQUES.exists():
        for clave, valor in json.loads(BLOQUES.read_text(encoding="utf-8")).items():
            if not clave.startswith("_"):
                texto = texto.replace("{" + clave + "}", valor)
    pendientes = re.findall(r"\{[A-Z_0-9]+\}", texto)
    if pendientes:
        raise SystemExit(f"Bloques sin definir en bloques_prompt.json: {pendientes}")
    return texto


def resolver(ref):
    """'@NOMBRE' -> id de la imagen ancla ya subida; cualquier otra cosa se pasa tal cual."""
    if ref.startswith("@"):
        return json.loads(ANCLAS.read_text(encoding="utf-8"))[ref[1:]]["id"]
    return ref


def args_de(trabajo):
    # los modelos de imagen a 3D (Tripo) no aceptan --prompt: solo se pasa si el trabajo lo trae
    a = [trabajo["modelo"]] + (["--prompt", expandir(trabajo["prompt"])] if trabajo.get("prompt") else [])
    for ref in trabajo.get("imagenes", []):
        a += ["--image", resolver(ref)]
    for k, v in trabajo.get("params", {}).items():
        a += [f"--{k}", str(v).lower() if isinstance(v, bool) else str(v)]
    return a


def cotizar(trabajo):
    code, out, err = hf("generate", "cost", *args_de(trabajo), "--json", timeout=120)
    if code != 0:
        return None, (err or out)[:200]
    try:
        return float(json.loads(out)["credits"]), None
    except Exception:
        return None, out[:200]


def saldo():
    code, out, _ = hf("account", "status", "--json", timeout=60)
    try:
        return float(json.loads(out)["credits"])
    except Exception:
        return None


def generar(trabajo, carpeta, redescargar=False):
    ident = trabajo["id"]
    crudo = carpeta / "_json" / f"{ident}.json"
    if redescargar:
        # Vuelve a bajar el original desde la respuesta ya guardada: no crea trabajos ni gasta creditos.
        code, out, err = (0, crudo.read_text(encoding="utf-8"), "") if crudo.exists() else (1, "", "sin respuesta guardada")
    else:
        code, out, err = hf("generate", "create", *args_de(trabajo), "--wait", "--wait-timeout", "15m", "--json")
        crudo.parent.mkdir(parents=True, exist_ok=True)
        crudo.write_text(out or err, encoding="utf-8")
    registro = {"id": ident, "estado": "error", "url": None, "archivo": None, "job_id": None, "detalle": None}
    if code != 0:
        registro["detalle"] = (err or out)[:300]
        return registro
    # result_url es el original; min_result_url es solo una miniatura comprimida.
    # Sin result_url no se adivina: la primera URL de medios podria ser una imagen de entrada.
    original = re.search(r'"result_url"\s*:\s*"([^"]+)"', out)
    job = re.search(r'"id"\s*:\s*"([0-9a-f-]{36})"', out)
    registro["job_id"] = job.group(1) if job else None
    estado = re.search(r'"status"\s*:\s*"([a-z_]+)"', out)
    if not original:
        registro["detalle"] = (f"sin result_url (status={estado.group(1) if estado else '?'}); "
                               f"revisar {crudo.relative_to(RAIZ).as_posix()}")
        return registro
    url = original.group(1)
    sufijo = re.search(r"\.([a-z0-9]{2,5})$", url.split("?")[0], re.I)
    ext = (sufijo.group(1).lower() if sufijo else "bin").replace("jpeg", "jpg")
    destino = carpeta / f"{ident}.{ext}"
    try:
        peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(peticion, timeout=180) as r:
            destino.write_bytes(r.read())
        registro.update(estado="ok", url=url, archivo=str(destino.relative_to(RAIZ)).replace("\\", "/"))
    except Exception as error:  # noqa: BLE001
        registro.update(estado="sin descargar", url=url, detalle=str(error)[:200])
    return registro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lote")
    ap.add_argument("--solo-cotizar", action="store_true")
    ap.add_argument("--solo", default="")
    ap.add_argument("--redescargar", action="store_true", help="Baja de nuevo los originales ya generados, sin gastar")
    a = ap.parse_args()
    spec = json.loads(Path(a.lote).read_text(encoding="utf-8"))
    trabajos = spec["trabajos"]
    if a.solo:
        elegidos = set(a.solo.split(","))
        trabajos = [t for t in trabajos if t["id"] in elegidos]
    carpeta = RAIZ / spec["carpeta"]
    carpeta.mkdir(parents=True, exist_ok=True)

    if a.redescargar:
        historial = json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else []
        for t in trabajos:
            r = generar(t, carpeta, redescargar=True)
            for fila in historial:
                if fila["id"] == r["id"]:
                    fila.update(url=r["url"], archivo=r["archivo"], estado=r["estado"])
            print(f"  {r['id']:36} {r['estado']:14} {r['archivo'] or r['detalle']}", flush=True)
        REGISTRO.write_text(json.dumps(historial, indent=1, ensure_ascii=False), encoding="utf-8")
        return

    total = 0.0
    for t in trabajos:
        costo, error = cotizar(t)
        t["_costo"] = costo
        if costo is None:
            raise SystemExit(f"No se pudo cotizar {t['id']}: {error}")
        total += costo
        print(f"  cotizado {t['id']:36} {t['modelo']:20} {costo:6.2f}", flush=True)
    print(f"Total cotizado: {total:.2f} creditos (tope del lote: {spec['tope']})", flush=True)
    if total > float(spec["tope"]):
        raise SystemExit("El lote supera su tope: no se genera nada.")
    if a.solo_cotizar:
        return

    antes = saldo()
    historial = json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else []
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # el registro se escribe al terminar cada trabajo: un fallo posterior no borra lo ya cobrado
    with ThreadPoolExecutor(max_workers=3) as ex:
        futuros = {ex.submit(generar, t, carpeta): t for t in trabajos}
        for fut in as_completed(futuros):
            t = futuros[fut]
            try:
                r = fut.result()
            except Exception as error:  # noqa: BLE001
                r = {"id": t["id"], "estado": "error", "url": None, "archivo": None, "job_id": None,
                     "detalle": f"excepcion local: {error}"[:300]}
            historial.append({"lote": spec["lote"], "fecha": ahora, "modelo": t["modelo"], "params": t.get("params", {}),
                              "referencias": t.get("imagenes", []), "prompt": expandir(t.get("prompt", "")),
                              "costo_cotizado": t["_costo"], "veredicto": "pendiente", **r})
            REGISTRO.write_text(json.dumps(historial, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"  {r['id']:36} {r['estado']:14} {r['archivo'] or r['detalle']}", flush=True)
    despues = saldo()
    if antes is not None and despues is not None:
        print(f"Saldo: {antes:.2f} -> {despues:.2f} (gastado {antes - despues:.2f})")


if __name__ == "__main__":
    main()
