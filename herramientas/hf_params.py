"""Imprime los parametros de uno o varios modelos desde Nasa_Game/Fase_0_Tecnica/Datos/hf_modelos.json.

Uso:  python herramientas/hf_params.py autosprite tripo_3d ...
      python herramientas/hf_params.py --crudo autosprite     (JSON sin resumir)
      python herramientas/hf_params.py --tipo 3d              (todos los de un tipo)
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CAT = json.loads((Path(__file__).resolve().parent.parent / "Nasa_Game" / "Fase_0_Tecnica" / "Datos" / "hf_modelos.json").read_text(encoding="utf-8"))


def corto(v, n=150):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= n else s[: n - 3] + "..."


def resumen(jt):
    d = CAT.get(jt)
    if not d:
        print(f"## {jt}: no existe")
        return
    print(f"## {jt} | {d['name']} | {d['type']} | costo defecto: {d['cost_default']}")
    p = d["params"]
    if not isinstance(p, dict):
        print("   (sin params)", corto(p, 300))
        return
    lista = p.get("params") or p.get("parameters") or p.get("properties") or p.get("schema")
    extra = {k: v for k, v in p.items() if k not in ("params", "parameters", "properties", "schema")}
    if isinstance(lista, list):
        for it in lista:
            if isinstance(it, dict):
                nombre = it.get("name") or it.get("key")
                resto = {k: v for k, v in it.items() if k not in ("name", "key", "cli", "cli_hint") and v not in (None, "", [], {})}
                print(f"   - {nombre}: {corto(resto, 260)}")
            else:
                print("   -", corto(it, 260))
    elif isinstance(lista, dict):
        for nombre, it in lista.items():
            print(f"   - {nombre}: {corto(it, 260)}")
    for k, v in extra.items():
        if k in ("name", "job_type", "type", "display_name"):
            continue
        print(f"   * {k}: {corto(v, 400)}")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--crudo":
        for jt in args[1:]:
            print(json.dumps(CAT.get(jt), indent=1, ensure_ascii=False))
        return
    if args and args[0] == "--tipo":
        args = [jt for jt, d in CAT.items() if str(d["type"]) in args[1:]]
    for jt in args:
        resumen(jt)
        print()


if __name__ == "__main__":
    main()
