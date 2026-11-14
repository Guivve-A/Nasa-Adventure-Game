"""Manifiesto de recursos del arte del juego.

Reune los rotulos "XXX-NN Nombre" de los encargos de hojas de referencia (lote_*.json dentro de
Nasa_Game/Fase_1_Arte) y escribe:
  - Nasa_Game/Fase_1_Arte/manifiesto_recursos.csv  (para herramientas y hojas de calculo)
  - Nasa_Game/Fase_1_Arte/Hojas_de_referencia/Catalogo de recursos.md  (para Obsidian)
El estado sale de Nasa_Game/Fase_1_Arte/veredictos.json (clave: ID del recurso o id de la hoja).

Uso:  python herramientas/manifiesto.py
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "Nasa_Game" / "Fase_1_Arte"
CATALOGO = DIR / "Hojas_de_referencia" / "Catalogo de recursos.md"
CATEGORIAS = {"VEG": "Vegetación", "TER": "Rocas y terreno", "ARQ": "Arquitectura", "URB": "Plaza y malecón",
              "COL": "Recolectables", "TAL": "Taller de electrónica", "FAU": "Fauna", "PER": "Reparto",
              "MIR": "Mirador del Faro"}
PATRON = re.compile(r'"([A-Z]{3}-\d{2}) ([^"]+)"\s*([^;"]*)')
POR_DEFECTO = "Concepto v1 · espera veredicto"


def leer(nombre):
    ruta = DIR / nombre
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def main():
    veredictos, coherencia = leer("veredictos.json"), leer("paleta_coherencia.json")
    filas, hojas = [], []
    for lote in sorted(DIR.rglob("lote_*.json")):
        spec = json.loads(lote.read_text(encoding="utf-8"))
        for t in spec["trabajos"]:
            items = PATRON.findall(t["prompt"])
            if not items:
                continue
            imagen = RAIZ / spec["carpeta"] / f"{t['id']}.png"
            titulo = re.search(r'Title: "([^"]+)"', t["prompt"])
            hojas.append({"id": t["id"], "titulo": titulo.group(1) if titulo else t["id"], "imagen": imagen,
                          "n": len(items), "estado": veredictos.get(t["id"], POR_DEFECTO)})
            for ident, nombre, encargo in items:
                encargo = re.split(r"\.\s|\{", encargo)[0].strip(" ,.")
                filas.append({"id": ident, "nombre": nombre, "categoria": CATEGORIAS.get(ident[:3], ident[:3]),
                              "hoja": t["id"], "archivo_hoja": imagen.relative_to(RAIZ).as_posix(),
                              "encargo": encargo,
                              "estado": veredictos.get(ident) or veredictos.get(t["id"]) or POR_DEFECTO,
                              "version": t["id"].rsplit("_", 1)[-1]})

    with open(DIR / "manifiesto_recursos.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)

    md = ["---", "tipo: catalogo", "generado_por: herramientas/manifiesto.py", "---", "",
          "# Catálogo de recursos", "",
          "> Se genera con `python herramientas/manifiesto.py`. No se edita a mano: los cambios van en los encargos "
          "(`lote_*.json`) o en `veredictos.json`. La lista completa está en `manifiesto_recursos.csv`.", "",
          f"**{len(filas)} recursos en {len(hojas)} hojas.** Normas de estilo: [[Biblia de arte]].", "",
          "| Hoja | Recursos | Color dentro de la paleta | Estado |", "|---|---:|---|---|"]
    for h in hojas:
        c = coherencia.get(h["imagen"].name)
        texto = f"{c['cerca_pct']} % (ΔE medio {c['de_medio']})" if c else "sin medir"
        md.append(f"| [[#{h['titulo']}]] | {h['n']} | {texto} | {h['estado']} |")
    for h in hojas:
        md += ["", f"## {h['titulo']}", "", f"![[{h['imagen'].name}]]", "",
               "| ID | Nombre | Encargo (inglés) | Estado |", "|---|---|---|---|"]
        md += [f"| {r['id']} | {r['nombre']} | {r['encargo']} | {r['estado']} |" for r in filas if r["hoja"] == h["id"]]
    CATALOGO.parent.mkdir(parents=True, exist_ok=True)
    CATALOGO.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(filas)} recursos en {len(hojas)} hojas -> manifiesto_recursos.csv y {CATALOGO.name}")


if __name__ == "__main__":
    main()
