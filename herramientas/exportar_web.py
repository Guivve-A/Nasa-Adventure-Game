"""Exporta a web (HTML5) los juegos 2D de los companeros para jugarlos desde la landing.

No toca las carpetas de origen ni el paquete de Windows: trabaja sobre copias en web_build/<id>/
(carpeta ignorada por Git) y deja la exportacion en landing/jugar/<id>/.

Uso (desde la raiz del repositorio):
  python -I herramientas/exportar_web.py                 # todos
  python -I herramientas/exportar_web.py base-luna       # uno

Requisitos: Godot 4.7.2 (consola) y sus plantillas web sin hilos en
%APPDATA%/Godot/export_templates/4.7.2.stable/ (web_nothreads_release.zip y web_nothreads_debug.zip).
Godot corre de uno en uno con el candado de herramientas/juego_ejecutar.py.

Cambios en la copia, nunca en el origen:
  - renderizador gl_compatibility (Mobile no existe en web);
  - export_presets.cfg con un preset "Web": sin hilos (no exige cabeceras COOP/COEP), lienzo adaptable,
    *.json incluido y <base href="/jugar/<id>/"> para que los .js, .wasm y .pck carguen aunque Vercel
    sirva la pagina sin barra final (/jugar/<id>).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import juego_ejecutar as je  # noqa: E402  (candado y ruta de Godot)

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web_build"
SALIDA = RAIZ / "landing" / "jugar"
LIMITE_VERCEL = 100 * 1024 * 1024

JUEGOS = {
    "base-luna": RAIZ / "Misión Artemis",
    "marte": RAIZ / "Marte_Gravedad2DHD" / "Marte_Gravedad2DHD" / "Mision_Artemis_Marte",
}
CARPETAS = ["codigo", "datos", "escenas", "recursos"]

# Solo en la copia web: el navegador no tiene las fuentes del sistema que en Windows dibujan las flechas
# (la fuente por defecto de Godot no trae U+2190 ni U+2192 y saldrian cajas).
PARCHES = {
    "base-luna": [("codigo/nivel_luna.gd", "← → / A D: moverse", "Flechas o A D: moverse"),
                  ("codigo/nivel_marte.gd", "← → / A D: moverse", "Flechas o A D: moverse")],
}

PRESET = """[preset.0]

name="Web"
platform="Web"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter="*.json"
exclude_filter=""
export_path=""
patches=PackedStringArray()
encryption_include_filters=""
encryption_exclude_filters=""
seed=0
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.0.options]

custom_template/debug=""
custom_template/release=""
variant/extensions_support=false
variant/thread_support=false
vram_texture_compression/for_desktop=true
vram_texture_compression/for_mobile=false
html/export_icon=true
html/custom_html_shell=""
html/head_include="<base href=\\"/jugar/{id}/\\">"
html/canvas_resize_policy=2
html/focus_canvas_on_start=true
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false
progressive_web_app/ensure_cross_origin_isolation_headers=false
"""


def preparar(id_, origen):
    destino = WEB / id_
    destino.mkdir(parents=True, exist_ok=True)
    for c in CARPETAS:
        if (destino / c).exists():
            shutil.rmtree(destino / c)
        shutil.copytree(origen / c, destino / c)
    texto = (origen / "project.godot").read_text(encoding="utf-8")
    texto = texto.replace('renderer/rendering_method="mobile"', 'renderer/rendering_method="gl_compatibility"')
    texto = texto.replace('"Mobile")', '"GL Compatibility")')
    if "gl_compatibility" not in texto:
        texto = texto.replace("[rendering]\n", '[rendering]\n\nrenderer/rendering_method="gl_compatibility"\n', 1)
    (destino / "project.godot").write_text(texto, encoding="utf-8")
    for archivo, viejo, nuevo in PARCHES.get(id_, []):
        ruta = destino / archivo
        contenido = ruta.read_text(encoding="utf-8")
        if viejo not in contenido:
            print(f"  aviso: el parche de {archivo} ya no aplica")
        ruta.write_text(contenido.replace(viejo, nuevo), encoding="utf-8")
    (destino / "export_presets.cfg").write_text(PRESET.replace("{id}", id_), encoding="utf-8")
    return destino


def godot(args, maximo=600):
    orden = [je.GODOT, "--headless"] + args
    print(">", " ".join(orden), flush=True)
    r = subprocess.run(orden, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=maximo)
    salida = (r.stdout or "") + (r.stderr or "")
    for linea in salida.splitlines():
        if any(k in linea for k in ("ERROR", "error", "WARNING", "savepack", "Export")):
            print("  ", linea)
    return r.returncode, salida


def exportar(id_):
    proyecto = preparar(id_, JUEGOS[id_])
    destino = SALIDA / id_
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    je.tomar_candado()
    try:
        godot(["--path", str(proyecto), "--import"], 600)
        codigo, salida = godot(["--path", str(proyecto), "--export-release", "Web", str(destino / "index.html")], 600)
    finally:
        je.soltar_candado()
    total = 0
    for f in sorted(destino.iterdir()):
        t = f.stat().st_size
        total += t
        aviso = "  <- SUPERA 100 MB (Vercel)" if t > LIMITE_VERCEL else ""
        print(f"  {f.name:32s} {t / 1048576:8.2f} MB{aviso}")
    ok = codigo == 0 and (destino / "index.pck").exists() and (destino / "index.wasm").exists()
    print(f"{id_}: {'OK' if ok else 'FALLO'} (codigo {codigo}), {total / 1048576:.2f} MB")
    return ok


def main():
    pedidos = [a for a in sys.argv[1:] if a in JUEGOS] or list(JUEGOS)
    resultados = {i: exportar(i) for i in pedidos}
    sys.exit(0 if all(resultados.values()) else 1)


if __name__ == "__main__":
    main()
