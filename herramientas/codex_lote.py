"""Lanza un lote de tareas a Codex (codex exec) en paralelo y guarda cada informe.

El archivo de tareas es un Markdown: lo que va antes de la primera linea
"@@TAREA ..." es el brief comun; cada "@@TAREA clave=valor ..." abre una tarea.

Claves: id, salida (ruta del informe), sandbox (read-only | workspace-write),
search (1 = busqueda web en vivo), timeout (minutos), cwd (carpeta de trabajo),
brief (0 = no anteponer el brief), esfuerzo (low | medium | high | xhigh).

Uso:  python herramientas/codex_lote.py <tareas.md> [--solo id1,id2] [--paralelo 5]
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent


def ruta_codex():
    base = Path(os.environ["LOCALAPPDATA"]) / "OpenAI" / "Codex" / "bin"
    exes = sorted(base.glob("*/codex.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not exes:
        raise SystemExit(f"No se encontro codex.exe en {base}")
    return str(exes[0])


def leer_tareas(archivo):
    brief, tareas, actual = [], [], None
    for linea in Path(archivo).read_text(encoding="utf-8").splitlines():
        if linea.startswith("@@TAREA "):
            campos = dict(par.split("=", 1) for par in linea[len("@@TAREA "):].split(" ") if "=" in par)
            actual = {"campos": campos, "texto": []}
            tareas.append(actual)
        elif actual is None:
            brief.append(linea)
        else:
            actual["texto"].append(linea)
    return "\n".join(brief).strip(), tareas


def correr(codex, brief, tarea, carpeta_logs):
    c = tarea["campos"]
    ident = c["id"]
    cwd = Path(c.get("cwd", "."))
    cwd = cwd if cwd.is_absolute() else (RAIZ / cwd)
    salida = Path(c["salida"])
    salida = salida if salida.is_absolute() else (RAIZ / salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    cuerpo = "\n".join(tarea["texto"]).strip()
    prompt = cuerpo if c.get("brief", "1") == "0" else f"{brief}\n\n---\n\n# TU TAREA\n\n{cuerpo}"
    cmd = [codex, "exec", "--skip-git-repo-check", "-C", str(cwd), "-s", c.get("sandbox", "read-only"),
           "--color", "never", "-c", f'model_reasoning_effort="{c.get("esfuerzo", "high")}"']
    if c.get("search", "0") == "1":
        cmd += ["-c", 'web_search="live"']
    cmd += ["-o", str(salida), "-"]
    log = carpeta_logs / f"{ident}.log"
    inicio = time.time()
    estado = "ok"
    try:
        with open(log, "wb") as f:
            r = subprocess.run(cmd, input=prompt.encode("utf-8"), stdout=f, stderr=subprocess.STDOUT,
                               timeout=float(c.get("timeout", "30")) * 60)
        if r.returncode != 0:
            estado = f"error (codigo {r.returncode})"
    except subprocess.TimeoutExpired:
        estado = "timeout"
    minutos = round((time.time() - inicio) / 60, 1)
    tam = salida.stat().st_size if salida.exists() else 0
    if estado == "ok" and tam == 0:
        estado = "sin informe"
    return {"id": ident, "estado": estado, "minutos": minutos, "bytes_informe": tam,
            "informe": str(salida), "log": str(log)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--solo", default="")
    ap.add_argument("--paralelo", type=int, default=5)
    a = ap.parse_args()
    codex = ruta_codex()
    brief, tareas = leer_tareas(a.archivo)
    if a.solo:
        elegidas = set(a.solo.split(","))
        tareas = [t for t in tareas if t["campos"]["id"] in elegidas]
    carpeta_logs = Path(a.archivo).resolve().parent / "logs"
    carpeta_logs.mkdir(exist_ok=True)
    print(f"Codex: {codex}\n{len(tareas)} tareas, {a.paralelo} en paralelo", flush=True)
    resultados = []
    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        for res in ex.map(lambda t: correr(codex, brief, t, carpeta_logs), tareas):
            resultados.append(res)
            print(f"  {res['id']:28} {res['estado']:22} {res['minutos']:>5} min  {res['bytes_informe']:>7} bytes", flush=True)
    estado_json = carpeta_logs / "estado.json"
    previo = json.loads(estado_json.read_text(encoding="utf-8")) if estado_json.exists() else {}
    previo.update({r["id"]: r for r in resultados})
    estado_json.write_text(json.dumps(previo, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
