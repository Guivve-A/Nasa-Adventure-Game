"""Catalogo de modelos de Higgsfield con parametros y costo por defecto.

Solo usa comandos de lectura del CLI (model list, model get, generate cost).
No crea trabajos ni gasta creditos.

Uso:  python herramientas/hf_catalogo.py
Salida: Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json y hf_costos_default.md
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "Nasa_Game" / "Fase_0_Tecnica" / "Datos"
SALIDA.mkdir(parents=True, exist_ok=True)


def ruta_hf():
    """Devuelve el binario real (hf.exe) para evitar el paso por cmd.exe."""
    cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
    if not cmd:
        raise SystemExit("No se encontro higgsfield en el PATH")
    exe = Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe"
    if not exe.exists():
        raise SystemExit(f"No existe {exe}")
    return str(exe)


HF = ruta_hf()


def hf(*args, timeout=90):
    try:
        r = subprocess.run([HF, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def como_json(texto):
    try:
        return json.loads(texto)
    except Exception:
        return None


def listar():
    code, out, err = hf("model", "list", "--json")
    if code != 0:
        raise SystemExit(f"model list fallo: {err}")
    data = como_json(out)
    if isinstance(data, dict):
        for clave in ("models", "items", "data", "results"):
            if isinstance(data.get(clave), list):
                data = data[clave]
                break
    return data


def detalle(modelo):
    jt = modelo.get("job_type") or modelo.get("id") or modelo.get("jobType")
    code, out, err = hf("model", "get", jt, "--json")
    params = como_json(out) if code == 0 else None
    code2, out2, err2 = hf("generate", "cost", jt, "--prompt", "test", "--json")
    costo = None
    error = None
    if code2 == 0:
        j = como_json(out2) or {}
        costo = j.get("credits")
    else:
        error = (err2 or out2).replace("\n", " | ")[:300]
    return jt, {
        "name": modelo.get("name") or modelo.get("display_name"),
        "type": modelo.get("type") or modelo.get("media_type") or modelo.get("output_type"),
        "list_entry": modelo,
        "params": params,
        "cost_default": costo,
        "cost_error": error,
    }


def main():
    modelos = listar()
    if not isinstance(modelos, list):
        (SALIDA / "hf_model_list_raw.json").write_text(json.dumps(modelos, indent=2, ensure_ascii=False), encoding="utf-8")
        raise SystemExit("Forma inesperada de model list; se guardo el crudo")
    with ThreadPoolExecutor(max_workers=6) as ex:
        pares = list(ex.map(detalle, modelos))
    cat = dict(pares)
    (SALIDA / "hf_modelos.json").write_text(json.dumps(cat, indent=2, ensure_ascii=False), encoding="utf-8")

    filas = sorted(cat.items(), key=lambda kv: (str(kv[1]["type"]), kv[1]["cost_default"] if kv[1]["cost_default"] is not None else 1e9, kv[0]))
    md = ["# Higgsfield: costo por defecto de cada modelo", "",
          "Generado con `herramientas/hf_catalogo.py` (solo lectura: `model list`, `model get`, `generate cost`).",
          "El costo es el de los parametros por defecto con un prompt de texto; los que exigen imagen o video de entrada figuran con su error.", "",
          "| Tipo | job_type | Nombre | Creditos (defecto) | Nota |", "|---|---|---|---|---|"]
    for jt, d in filas:
        c = d["cost_default"]
        md.append(f"| {d['type']} | `{jt}` | {d['name']} | {c if c is not None else '-'} | {d['cost_error'] or ''} |")
        print(f"{str(d['type']):6} {jt:30} {str(c) if c is not None else '-':>7}  {d['cost_error'] or ''}")
    (SALIDA / "hf_costos_default.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n{len(cat)} modelos -> {SALIDA}")


if __name__ == "__main__":
    main()
