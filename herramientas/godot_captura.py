"""Lanza Godot para una captura o una medicion y lo cierra si se queda colgado al salir.

En la HD 620, Godot 4.7.2 a veces no termina despues de get_tree().quit(): la captura ya esta guardada,
pero el proceso queda vivo sin usar CPU (paso el 2026-11-12 con la escena de exploracion). Este envoltorio
lee la salida y, cuando ve CAPTURA_OK o MEDIDA, espera unos segundos y mata el arbol de procesos si sigue
vivo. Tambien corta todo si pasa el tiempo maximo.

Uso:  python herramientas/godot_captura.py <carpeta del proyecto> [res://escena.tscn] -- <argumentos del juego>
Ej.:  python herramientas/godot_captura.py pruebas/escena_exploracion -- --encuadre=21 --captura=C:/tmp/a.png
"""
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
GODOT = r"C:\Users\guill\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe"
CLAVES = ("CAPTURA_OK", "MEDIDA", "ESCENA", "RECURSO", "ANIMACIONES", "SCRIPT ERROR", "Parse Error", "ERROR: No se")
GRACIA_S = 8.0
MAXIMO_S = 300.0


def matar(proceso):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proceso.pid)], capture_output=True)


def main():
    if "--" not in sys.argv:
        raise SystemExit(__doc__)
    corte = sys.argv.index("--")
    previos, juego = sys.argv[1:corte], sys.argv[corte + 1:]
    proyecto = str(Path(previos[0]).resolve())
    orden = [GODOT, "--path", proyecto, *previos[1:], "--", *juego]
    inicio = time.time()
    proceso = subprocess.Popen(orden, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               encoding="utf-8", errors="replace")
    listo = {"t": None}

    def leer():
        for linea in proceso.stdout:
            if any(c in linea for c in CLAVES):
                print(linea.rstrip(), flush=True)
            if "CAPTURA_OK" in linea or linea.startswith("MEDIDA"):
                listo["t"] = time.time()

    hilo = threading.Thread(target=leer, daemon=True)
    hilo.start()
    estado = "ok"
    while proceso.poll() is None:
        ahora = time.time()
        if listo["t"] is not None and ahora - listo["t"] > GRACIA_S:
            matar(proceso)
            estado = "ok (Godot no salio solo: se cerro)"
            break
        if ahora - inicio > MAXIMO_S:
            matar(proceso)
            estado = "TIEMPO AGOTADO"
            break
        time.sleep(0.25)
    hilo.join(timeout=2)
    print(f"GODOT {estado} en {time.time() - inicio:.1f} s")
    sys.exit(0 if estado.startswith("ok") and listo["t"] is not None else 1)


if __name__ == "__main__":
    main()
