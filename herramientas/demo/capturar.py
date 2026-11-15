"""Graba la biblioteca de tomas del video demo a 1920x1080 y 30 cuadros por segundo, sin perder cuadros.

Usa el modo de pelicula de Godot (--write-movie con --fixed-fps) a traves de herramientas/juego_ejecutar.py, que
respeta el candado global (un solo Godot a la vez). Cada toma se graba en un .avi temporal (MJPEG + PCM), se recorta
y se convierte con ffmpeg a Nasa_Game/Presentacion/material/<id>.mp4 (H.264 CRF 14, yuv420p, AAC 192 kb/s si hay
sonido), con su hoja de cuadros en material/hojas/<id>.jpg. Al terminar borra el .avi.

Por que una copia espejo: Godot escribe el video al tamano del viewport del proyecto (1280x720 en juego/), no al de la
ventana. Para 1080p nativo, el proyecto se copia (robocopy /MIR, incremental) a %TEMP%/luz_demo_espejos/<nombre>
y ahi se anade un override.cfg: viewport 1920x1080 y stretch/scale = 1920/ancho_base, asi la interfaz queda igual
que en el juego. Los proyectos originales (juego/ y los de los companeros) no se tocan.

Uso:
  python -I herramientas/demo/capturar.py --lista
  python -I herramientas/demo/capturar.py <id> [<id> ...]        graba esas tomas (repetible: sobrescribe)
  python -I herramientas/demo/capturar.py --todas                graba todas
  python -I herramientas/demo/capturar.py --grupo=juego|minijuegos|externas
  opciones: --conservar (no borra los .avi)  --hoja=<video> (solo hace la hoja de cuadros de un video)

Recorte: en las tomas de juego/, el guion juego/pruebas/demo_captura.gd imprime "PRUEBA_OK demo.inicio cuadro=<n>"
y "demo.fin"; se corta entre las dos. En los proyectos externos se corta por segundos de juego (inicio, duracion).
Los juegos de los companeros solo tienen su --prueba, que corre a Engine.time_scale 6 (Luna) y 4 (Marte): se graban
con --fixed-fps 180 y 120, de modo que cada cuadro avanza 1/30 s de juego, y se leen como 30 fps (velocidad real).
Su sonido no vale en ese modo y se descarta.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent.parent
EJECUTAR = RAIZ / "herramientas" / "juego_ejecutar.py"
MATERIAL = RAIZ / "Nasa_Game" / "Presentacion" / "material"
HOJAS = MATERIAL / "hojas"
ESPEJOS = Path(tempfile.gettempdir()) / "luz_demo_espejos"
TEMPORAL = Path(tempfile.gettempdir()) / "luz_demo_tmp"
FPS = 30
ANCHO, ALTO = 1920, 1080
GUION = "--prueba=guion:res://pruebas/demo_captura.gd"
ARTEMIS = "Misión Artemis"
MARTE = "Marte_Gravedad2DHD/Marte_Gravedad2DHD/Mision_Artemis_Marte"

# --- tomas de juego/ (cada una es una grabacion con su recorte por marcas) ---
TOMAS_JUEGO = {
    "menu": "menu principal: titulo, la Luna y el foco recorriendo los botones",
    "mapa": "mapa del mundo ilustrado (desde el menu): el cursor recorre los lugares",
    "habitacion": "habitacion-taller de manana con HUD: la protagonista camina con Orbita detras",
    "orbita": "habitacion: hablar con Orbita (dialogo con pistas)",
    "ciudad": "Plaza de las Iguanas de tarde, sin HUD: fuente, fachadas y paseo",
    "sendero": "sendero del arroyo, sin HUD: el panel, la antena y la cuesta",
    "mirador": "Mirador del Faro de noche con la Luna, sin HUD",
    "luna": "la Luna del sueno: saltos lunares con Orbita, sin HUD",
    "luna_apolo": "la Luna del sueno: a saltos hacia el punto de la foto con la etapa de descenso, sin HUD",
    "minimapa": "sendero con HUD: el minimapa senala el panel solar y se agranda con N",
    "carga": "cambio de zona real: de la plaza al sendero por el umbral, con la pantalla de carga pintada",
    "cuaderno": "cuaderno abierto: fichas de datos reales con su fuente",
}
# tomas extra (juego/pruebas/demo_extra.gd), pedidas por el guion del 2026-11-15
GUION_EXTRA = "--prueba=guion:res://pruebas/demo_extra.gd"
TOMAS_EXTRA = {
    "mirador_telescopio": "Mirador de noche con HUD: camina al telescopio, pulsa E y se abre el ocular",
    "carga_mirador": "del Sendero al Mirador por el umbral: pantalla de carga pintada",
    "mirador_quieto": "Mirador de noche: ella y Orbita quietos junto al telescopio, la Luna sobre la ciudad",
    "mirador_alejar": "Mirador de noche: la camara se aleja con X (ultima imagen)",
    "luna_lenta": "Luna del sueno: saltos a paso lento con Orbita, sin HUD",
    "mapa_tecla_m": "en el Sendero, tecla M: mapa del mundo y el cursor recorre los lugares",
}
MINIJUEGOS = {
    "seguidor": "control con inercia y prealimentacion",
    "antena": "rastreo de satelites",
    "satelite": "armar un CubeSat",
    "telescopio": "la Luna del 12 de noviembre",
    "linea_tiempo": "hitos espaciales de Ecuador",
    "muestras": "herramientas lunares",
    "banderas": "plantar las dos banderas",
    "regreso": "reentrada",
    "orbita": "la orbita de Pegaso",
}

# --- grabaciones externas: una grabacion da una o varias tomas cortadas por segundos de juego ---
EXTERNAS = {
    "recorrido": {
        "proyecto": "juego", "args": ["--prueba=recorrido_manos", "--ritmo=2"], "fps": 30, "cuadros": 900, "sonido": False,
        "max": 900,
        "tomas": {"recorrido_manos": (3.0, 12.0, "--prueba=recorrido_manos con ventana: el juego jugandose solo con teclas simuladas (ritmo 2)")},
    },
    "telescopio_real": {
        "proyecto": "pruebas/luna_telescopio", "args": [], "fps": 30, "cuadros": 330, "sonido": False,
        "tomas": {"telescopio_luna_real": (1.0, 9.0, "la Luna real del telescopio: texturas LRO y efemerides de JPL Horizons")},
    },
    "artemis": {
        "proyecto": ARTEMIS, "args": ["--prueba"], "fps": 180, "sonido": False, "max": 1800,
        "tomas": {},      # se llenan tras ver la hoja de la grabacion completa (ver SEGMENTOS)
    },
    "marte_sup": {
        "proyecto": MARTE, "args": ["--capitulo=superficie"], "fps": 30, "cuadros": 300, "sonido": True, "max": 300,
        "tomas": {"marte_superficie": (1.5, 8.0, "Mision Artemis - Marte (companeros), --capitulo=superficie: la base ya aterrizada, sin jugador (sin --prueba)")},
    },
    "marte": {
        "proyecto": MARTE, "args": ["--prueba"], "fps": 120, "sonido": False, "max": 1800,
        "tomas": {},
    },
}
# segmentos elegidos de las grabaciones completas de los companeros (inicio y duracion en segundos de juego)
SEGMENTOS = RAIZ / "herramientas" / "demo" / "segmentos.json"


def cargar_segmentos():
    if SEGMENTOS.exists():
        datos = json.loads(SEGMENTOS.read_text(encoding="utf-8"))
        for fuente, tomas in datos.items():
            if fuente in EXTERNAS:
                for id_toma, s in tomas.items():
                    EXTERNAS[fuente]["tomas"][id_toma] = (float(s["inicio"]), float(s["duracion"]), s.get("que", ""))


def catalogo():
    """id -> (fuente, descripcion)"""
    cargar_segmentos()
    c = {}
    for t, d in TOMAS_JUEGO.items():
        c[t] = ("juego", d)
    for t, d in TOMAS_EXTRA.items():
        c[t] = ("juego", d)
    for m, d in MINIJUEGOS.items():
        c["mj_" + m] = ("juego", f"minijuego {m} jugandose solo: {d}")
    for fuente, g in EXTERNAS.items():
        for t, (_, _, d) in g["tomas"].items():
            c[t] = (fuente, d)
        c[fuente + "_completo"] = (fuente, "grabacion completa (solo para elegir segmentos; no va al material)")
    return c


# ------------------------------------------------------------------ espejo del proyecto

def ancho_base(proyecto: Path) -> int:
    texto = (proyecto / "project.godot").read_text(encoding="utf-8")
    m = re.search(r"window/size/viewport_width=(\d+)", texto)
    return int(m.group(1)) if m else 1152


def espejo(carpeta: str) -> Path:
    origen = (RAIZ / carpeta).resolve()
    nombre = re.sub(r"[^A-Za-z0-9_]+", "_", origen.name.encode("ascii", "ignore").decode()) or "proyecto"
    destino = ESPEJOS / nombre
    destino.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["robocopy", str(origen), str(destino), "/MIR", "/XF", ".candado_godot", "override.cfg",
                        "/NFL", "/NDL", "/NJH", "/NJS", "/NP"], capture_output=True, text=True)
    if r.returncode >= 8:
        raise SystemExit(f"robocopy fallo ({r.returncode}) al copiar {origen}:\n{r.stdout}\n{r.stderr}")
    escala = ANCHO / ancho_base(origen)
    (destino / "override.cfg").write_text(
        "; solo en la copia espejo para grabar el demo a 1080p (herramientas/demo/capturar.py)\n"
        "[display]\n"
        f"window/size/viewport_width={ANCHO}\nwindow/size/viewport_height={ALTO}\n"
        f"window/size/window_width_override={ANCHO}\nwindow/size/window_height_override={ALTO}\n"
        f"window/stretch/scale={escala:.6f}\n\n"
        "[editor]\nmovie_writer/mjpeg_quality=0.95\n", encoding="utf-8")
    return destino


# ------------------------------------------------------------------ grabar y convertir

def grabar(proyecto: Path, args: list, avi: Path, fps: int, maximo: float, cuadros=None) -> list:
    avi.parent.mkdir(parents=True, exist_ok=True)
    if avi.exists():
        avi.unlink()
    orden = [sys.executable, "-I", str(EJECUTAR), f"--proyecto={proyecto}", f"--pelicula={avi}", "--pantalla_completa",
             f"--resolucion={ANCHO}x{ALTO}", f"--fps={fps}", f"--max={maximo:.0f}"]
    if not (proyecto / ".godot").exists():
        orden.append("--importar")
    if cuadros:
        orden.append(f"--cuadros={cuadros}")
    orden += ["--", *args]
    print("  >", " ".join(orden[3:]), flush=True)
    inicio = time.time()
    r = subprocess.run(orden, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lineas = r.stdout.splitlines()
    for l in lineas:
        if any(k in l for k in ("demo.", "SCRIPT ERROR", "PRUEBA_FALLO", "[godot", "esperando turno")):
            print("   ", l, flush=True)
    print(f"   (grabacion: {time.time() - inicio:.0f} s)", flush=True)
    if not avi.exists():
        raise RuntimeError(f"no se escribio {avi}")
    return lineas


def cuadros_avi(avi: Path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                        "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(avi)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def convertir(avi: Path, salida: Path, a: int, b: int, sonido: bool) -> float:
    """cuadros a..b (incluidos) del avi a H.264 1080p30; devuelve los segundos"""
    salida.parent.mkdir(parents=True, exist_ok=True)
    filtro = (f"select='between(n\\,{a}\\,{b})',setpts=N/{FPS}/TB,"
              f"scale={ANCHO}:{ALTO}:flags=lanczos,format=yuv420p")
    orden = ["ffmpeg", "-y", "-v", "error", "-i", str(avi), "-vf", filtro, "-r", str(FPS),
             "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-profile:v", "high", "-movflags", "+faststart"]
    if sonido:
        orden += ["-af", f"atrim=start={a / FPS:.4f}:end={(b + 1) / FPS:.4f},asetpts=PTS-STARTPTS",
                  "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    else:
        orden += ["-an"]
    orden.append(str(salida))
    subprocess.run(orden, check=True)
    return (b - a + 1) / FPS


def hoja(video: Path, destino: Path, n: int = 8):
    """hoja de cuadros: n cuadros repartidos, en rejilla de 4 columnas"""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                       capture_output=True, text=True)
    dur = float(r.stdout.strip() or 1)
    filas = (n + 3) // 4
    destino.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf",
                    f"fps={n / dur:.5f},scale=480:-1,tile=4x{filas}:padding=4:color=black", "-frames:v", "1",
                    "-q:v", "3", str(destino)], check=True)
    return destino


def marca(lineas: list, nombre: str):
    for l in lineas:
        m = re.search(rf"demo\.{nombre} cuadro=(\d+)", l)
        if m:
            return int(m.group(1))
    return None


def registrar(id_toma: str, archivo: Path, segundos: float, que: str):
    indice = MATERIAL / "tomas.json"
    datos = json.loads(indice.read_text(encoding="utf-8")) if indice.exists() else {}
    datos[id_toma] = {"archivo": archivo.name, "segundos": round(segundos, 2), "que": que,
                      "grabada": time.strftime("%Y-%m-%d %H:%M")}
    indice.write_text(json.dumps(dict(sorted(datos.items())), ensure_ascii=False, indent=2), encoding="utf-8")


def toma_juego(id_toma: str, que: str, espejo_juego: Path, conservar: bool):
    avi = TEMPORAL / f"{id_toma}.avi"
    guion = GUION_EXTRA if id_toma in TOMAS_EXTRA else GUION
    lineas = grabar(espejo_juego, [guion, f"--toma={id_toma}"], avi, FPS, 400.0)
    a, b = marca(lineas, "inicio"), marca(lineas, "fin")
    total = cuadros_avi(avi)
    if a is None:
        raise RuntimeError(f"{id_toma}: el guion no imprimio demo.inicio")
    b = min(b if b is not None else total - 1, total - 1)
    salida = MATERIAL / f"{id_toma}.mp4"
    seg = convertir(avi, salida, a, b, sonido=True)
    hoja(salida, HOJAS / f"{id_toma}.jpg")
    registrar(id_toma, salida, seg, que)
    print(f"  OK {salida.relative_to(RAIZ)}  {seg:.1f} s (cuadros {a}-{b} de {total})", flush=True)
    if not conservar:
        avi.unlink(missing_ok=True)


def fuente_externa(fuente: str, ids: list, conservar: bool):
    g = EXTERNAS[fuente]
    proyecto = espejo(g["proyecto"])
    avi = TEMPORAL / f"{fuente}.avi"
    args = list(g["args"])
    if g["proyecto"] in (ARTEMIS, MARTE):
        capturas = TEMPORAL / f"{fuente}_capturas"
        capturas.mkdir(parents=True, exist_ok=True)
        args.append(f"--capturas={capturas}")
    grabar(proyecto, args, avi, g["fps"], float(g.get("max", 600)), g.get("cuadros"))
    total = cuadros_avi(avi)
    print(f"  {fuente}: {total} cuadros = {total / FPS:.1f} s de juego", flush=True)
    for id_toma in ids:
        if id_toma == fuente + "_completo":
            salida = TEMPORAL / f"{fuente}_completo.mp4"
            seg = convertir(avi, salida, 0, total - 1, sonido=False)
            h = hoja(salida, TEMPORAL / f"{fuente}_completo.jpg", n=int(min(48, max(8, seg // 3))))
            print(f"  completo: {salida} ({seg:.1f} s); hoja {h}", flush=True)
            continue
        inicio, dur, que = g["tomas"][id_toma]
        a = int(round(inicio * FPS))
        b = min(total - 1, a + int(round(dur * FPS)) - 1)
        salida = MATERIAL / f"{id_toma}.mp4"
        seg = convertir(avi, salida, a, b, sonido=bool(g["sonido"]))
        hoja(salida, HOJAS / f"{id_toma}.jpg")
        registrar(id_toma, salida, seg, que)
        print(f"  OK {salida.relative_to(RAIZ)}  {seg:.1f} s", flush=True)
    if not conservar:
        avi.unlink(missing_ok=True)


def main():
    args = sys.argv[1:]
    cat = catalogo()
    if not args or "--lista" in args:
        for t, (f, d) in cat.items():
            print(f"{t:24s} [{f}] {d}")
        return
    for a in args:
        if a.startswith("--hoja="):
            v = Path(a.split("=", 1)[1])
            print(hoja(v, v.with_suffix(".hoja.jpg"), n=16))
            return
    conservar = "--conservar" in args
    pedidas = [a for a in args if not a.startswith("--")]
    if "--todas" in args:
        pedidas = [t for t in cat if not t.endswith("_completo")]
    for a in args:
        if a.startswith("--grupo="):
            g = a.split("=", 1)[1]
            if g == "juego":
                pedidas += list(TOMAS_JUEGO)
            elif g == "minijuegos":
                pedidas += ["mj_" + m for m in MINIJUEGOS]
            elif g == "externas":
                pedidas += [t for t, (f, _) in cat.items() if f != "juego" and not t.endswith("_completo")]
    desconocidas = [t for t in pedidas if t not in cat]
    if desconocidas:
        raise SystemExit(f"tomas desconocidas: {desconocidas} (ver --lista)")
    MATERIAL.mkdir(parents=True, exist_ok=True)
    fallos = []
    de_juego = [t for t in pedidas if cat[t][0] == "juego"]
    if de_juego:
        espejo_juego = espejo("juego")
        for t in de_juego:
            print(f"== {t}", flush=True)
            try:
                toma_juego(t, cat[t][1], espejo_juego, conservar)
            except Exception as e:      # una toma fallida no corta las demas
                print(f"  FALLO {t}: {e}", flush=True)
                fallos.append(t)
    for fuente in EXTERNAS:
        ids = [t for t in pedidas if cat[t][0] == fuente]
        if ids:
            print(f"== {fuente}: {ids}", flush=True)
            try:
                fuente_externa(fuente, ids, conservar)
            except Exception as e:
                print(f"  FALLO {fuente}: {e}", flush=True)
                fallos += ids
    print(f"[capturar: {len(pedidas) - len(fallos)} de {len(pedidas)} tomas]" + (f" fallaron: {fallos}" if fallos else ""))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
