"""Ejecuta el juego (carpeta juego/) con Godot 4.7.2: de uno en uno, y lo cierra si se cuelga.

Varios agentes trabajan a la vez en este equipo (2 nucleos, 8 GB, Intel HD 620). Dos Godot abiertos a la vez
falsean los fps y pueden agotar la memoria, asi que este envoltorio toma un candado global
(juego/.candado_godot) y espera su turno. Tambien mata el proceso si no sale solo (pasa en la HD 620).

Uso:
  python -I herramientas/juego_ejecutar.py [--ventana] [--max=<s>] [--todo] [--importar] -- <argumentos del juego>

  (sin --ventana)  corre con --headless: logica, fisica y guiones, sin GPU. Sirve para las pruebas.
  --ventana        abre la ventana real: capturas (--captura=<png>) y mediciones de fps (--medir=<s>).
  --max=<s>        tiempo maximo en segundos (por defecto 240).
  --todo           imprime toda la salida de Godot, no solo las lineas clave.
  --importar       antes de ejecutar, corre "--headless --import" (crea .godot y la cache de clases).
  --proyecto=<carpeta>  otro proyecto de Godot bajo el mismo candado, con su escena si hace falta. Ejemplo:
                   python -I herramientas/juego_ejecutar.py --ventana --proyecto=pruebas/escena_exploracion
                     res://vista_previa.tscn -- --glb=<glb> --animacion=caminar --tiempo=0.3 --captura=<png>
                   (en esos proyectos el fin lo marcan CAPTURA_OK o MEDIDA)
  --pelicula=<archivo.avi|.png>  graba video con el modo de pelicula de Godot (--write-movie) a cuadros fijos:
                   no pierde cuadros aunque el equipo vaya lento. Implica --ventana. Con .avi da MJPEG y sonido PCM;
                   con .png, una secuencia de PNG mas un .wav. El archivo se cierra cuando el juego sale.
  --resolucion=<AxB>   tamano de la ventana (por ejemplo 1920x1080); se pasa como --resolution.
  --fps=<n>        cuadros por segundo de la pelicula (por defecto 30); se pasa como --fixed-fps.
  --cuadros=<n>    sale solo tras <n> cuadros (--quit-after): para grabar proyectos que no terminan solos.
  --pantalla_completa  abre a pantalla completa (--fullscreen). En esta pantalla una ventana de 1920x1080 no
                   cabe (queda en 1866x1050); a pantalla completa el juego se dibuja a 1920x1080 de verdad.
  Ojo: el video sale del tamano del viewport del proyecto (1280x720 en juego/), no del de la ventana: Godot
  reescala cada cuadro. Para 1080p nativo, herramientas/demo/capturar.py graba una copia espejo del proyecto
  con un override.cfg (viewport 1920x1080 y stretch/scale 1,5, que deja la interfaz igual).

Argumentos del juego (los lee juego/principal.gd):
  --prueba=<nombre>          nucleo | zonas | minijuegos | recorrido | zona:<id> | minijuego:<id>
  --zona=<id> [--entrada=<nombre>]   abre una zona directamente
  --minijuego=<id>           abre un minijuego directamente
  --auto                     dialogos sin esperas y minijuegos que se juegan solos
  --captura=<png> [--espera=<s>]     guarda una captura tras <s> segundos (por defecto 2) y sale
  --medir=<s>                mide fps durante <s> segundos y sale
  --ritmo=<f>                Engine.time_scale (las pruebas usan 8)
  --pos=x,z  --mira=x,z      coloca a la protagonista (con --zona) para una captura

Marcadores de la salida: PRUEBA_OK, PRUEBA_FALLO, CAPTURA_OK, MEDIDA y FIN.
Codigo de salida: 0 si no hubo errores de guion, PRUEBA_FALLO ni tiempo agotado; 1 en caso contrario.
"""
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
PROYECTO = RAIZ / "juego"
GODOT_POR_DEFECTO = r"C:\Users\guill\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe"


def ruta_godot():
    """Ejecutable de Godot 4.7.2 (version de consola). En otro equipo se indica con la variable de entorno
    GODOT_EXE o escribiendo la ruta en herramientas/godot_local.txt (una linea; ese archivo no se comparte)."""
    local = Path(__file__).resolve().parent / "godot_local.txt"
    if os.environ.get("GODOT_EXE"):
        return os.environ["GODOT_EXE"]
    if local.exists():
        return local.read_text(encoding="utf-8").strip().strip('"')
    return GODOT_POR_DEFECTO


GODOT = ruta_godot()
CANDADO = PROYECTO / ".candado_godot"
CLAVES = ("PRUEBA_", "CAPTURA_OK", "MEDIDA", "FIN", "ZONA ", "MINIJUEGO ", "AVISO ", "SCRIPT ERROR", "Parse Error",
          "ERROR:", "   at:", "WARNING: res")
ERRORES = ("SCRIPT ERROR", "Parse Error", "PRUEBA_FALLO", "Failed to load script", "Cannot open file",
           "Invalid call", "Invalid access", "Invalid assignment", "Nonexistent function")
GRACIA_S = 6.0
CANDADO_VIEJO_S = 900.0
ESPERA_CANDADO_S = 2400.0


def matar(proceso):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proceso.pid)], capture_output=True)


def tomar_candado():
    inicio = time.time()
    avisado = False
    while True:
        try:
            descriptor = os.open(str(CANDADO), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(descriptor, f"{os.getpid()} {time.time():.0f}".encode())
            os.close(descriptor)
            return
        except FileExistsError:
            try:
                edad = time.time() - CANDADO.stat().st_mtime
            except FileNotFoundError:
                continue
            if edad > CANDADO_VIEJO_S:
                try:
                    CANDADO.unlink()
                except OSError:
                    pass
                continue
            if time.time() - inicio > ESPERA_CANDADO_S:
                raise SystemExit("No se pudo tomar el candado de Godot (otro proceso lo tiene hace demasiado)")
            if not avisado:
                print("(esperando turno: otro Godot esta corriendo)", flush=True)
                avisado = True
            time.sleep(1.5)


def soltar_candado():
    try:
        CANDADO.unlink()
    except OSError:
        pass


def correr(orden, maximo, todo, marcas_fin=("FIN",)):
    inicio = time.time()
    proceso = subprocess.Popen(orden, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               encoding="utf-8", errors="replace")
    estado = {"fin": None, "errores": 0, "lineas": 0}

    def leer():
        for linea in proceso.stdout:
            estado["lineas"] += 1
            texto = linea.rstrip()
            if todo or any(c in texto for c in CLAVES):
                print(texto, flush=True)
            if any(e in texto for e in ERRORES):
                estado["errores"] += 1
            if any(texto.startswith(m) or (m != "FIN" and m in texto) for m in marcas_fin):
                estado["fin"] = time.time()

    hilo = threading.Thread(target=leer, daemon=True)
    hilo.start()
    resultado = "ok"
    while proceso.poll() is None:
        ahora = time.time()
        if estado["fin"] is not None and ahora - estado["fin"] > GRACIA_S:
            matar(proceso)
            resultado = "ok (Godot no salio solo: se cerro)"
            break
        if ahora - inicio > maximo:
            matar(proceso)
            resultado = "TIEMPO AGOTADO"
            estado["errores"] += 1
            break
        time.sleep(0.2)
    hilo.join(timeout=3.0)
    return resultado, estado, time.time() - inicio


def main():
    if "--" not in sys.argv:
        raise SystemExit(__doc__)
    corte = sys.argv.index("--")
    previos, juego = sys.argv[1:corte], sys.argv[corte + 1:]
    ventana = "--ventana" in previos
    todo = "--todo" in previos
    importar = "--importar" in previos
    maximo = 240.0
    proyecto = PROYECTO
    escena = []
    pelicula = None
    resolucion = None
    fps = "30"
    for p in previos:
        if p.startswith("--max="):
            maximo = float(p.split("=", 1)[1])
        elif p.startswith("--pelicula="):
            pelicula = Path(p.split("=", 1)[1]).resolve()
            ventana = True
        elif p.startswith("--resolucion="):
            resolucion = p.split("=", 1)[1]
        elif p.startswith("--fps="):
            fps = p.split("=", 1)[1]
        elif p.startswith("--proyecto="):
            # otro proyecto de Godot (p. ej. pruebas/escena_exploracion) bajo el mismo candado
            proyecto = (RAIZ / p.split("=", 1)[1]).resolve()
        elif p.startswith("res://"):
            escena.append(p)
    propio = proyecto == PROYECTO
    marcas_fin = ("FIN",) if propio else ("FIN", "CAPTURA_OK", "MEDIDA")
    if not Path(GODOT).exists():
        raise SystemExit(f"No se encuentra Godot en {GODOT}. Define GODOT_EXE o escribe la ruta en herramientas/godot_local.txt")
    tomar_candado()
    try:
        if importar or (propio and not (PROYECTO / ".godot").exists()):
            r, e, t = correr([GODOT, "--headless", "--path", str(proyecto), "--import"], 300.0, False, ("FIN_NUNCA",))
            print(f"[importar: {r}, {t:.0f} s]", flush=True)
        orden = [GODOT, "--path", str(proyecto), *escena]
        if not ventana:
            orden.append("--headless")
        if resolucion:
            orden += ["--resolution", resolucion]
        if "--pantalla_completa" in previos:
            orden.append("--fullscreen")
        for p in previos:
            if p.startswith("--cuadros="):
                orden += ["--quit-after", p.split("=", 1)[1]]
        if pelicula is not None:
            pelicula.parent.mkdir(parents=True, exist_ok=True)
            orden += ["--write-movie", str(pelicula), "--fixed-fps", fps]
        orden += ["--", *juego]
        resultado, estado, segundos = correr(orden, maximo, todo, marcas_fin)
    finally:
        soltar_candado()
    print(f"[godot: {resultado}; {segundos:.0f} s; lineas={estado['lineas']}; errores={estado['errores']}]", flush=True)
    sys.exit(1 if estado["errores"] else 0)


if __name__ == "__main__":
    main()
