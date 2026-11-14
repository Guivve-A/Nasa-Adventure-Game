"""Reanuda una sesion de Codex que se corto por tiempo y le pide el informe final.

El id de sesion esta en las primeras lineas del log de la tarea (session id: ...).

Uso:  python herramientas/codex_reanudar.py <id_sesion> <informe_salida.md> [carpeta_de_trabajo]
"""
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent

PROMPT = (
    "Se agoto el tiempo de la tarea. No hagas mas busquedas ni lecturas. "
    "Con lo que ya investigaste, escribe ahora el informe final completo en el formato pedido en el brief, "
    "con todas sus secciones y las fuentes que ya consultaste. Marca como 'sin verificar' lo que no alcanzaste a comprobar."
)


def main():
    sesion = sys.argv[1]
    salida = Path(sys.argv[2])
    salida = salida if salida.is_absolute() else RAIZ / salida
    cwd = sys.argv[3] if len(sys.argv) > 3 else str(RAIZ)
    base = Path(os.environ["LOCALAPPDATA"]) / "OpenAI" / "Codex" / "bin"
    codex = str(sorted(base.glob("*/codex.exe"), key=lambda p: p.stat().st_mtime, reverse=True)[0])
    cmd = [codex, "exec", "resume", "--skip-git-repo-check", "-c", 'model_reasoning_effort="medium"',
           "-o", str(salida), sesion, "-"]
    with open(str(salida) + ".log", "wb") as log:
        r = subprocess.run(cmd, input=PROMPT.encode("utf-8"), cwd=cwd, stdout=log, stderr=subprocess.STDOUT, timeout=1500)
    tam = salida.stat().st_size if salida.exists() else 0
    print(f"codigo {r.returncode}, informe de {tam} bytes en {salida}")


if __name__ == "__main__":
    main()
