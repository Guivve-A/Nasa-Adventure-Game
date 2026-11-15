"""Cotiza y genera tomas de video con Higgsfield (Seedance 2.5, MiniMax H3...), con registro.

Una toma = un modelo, un encargo de movimiento, un fotograma inicial (y final opcional), duracion,
resolucion y un id. Por defecto SOLO COTIZA: crear un trabajo exige --generar.

- Los fotogramas locales se suben una vez (JPEG de calidad 95, gratis) y su id se guarda en
  Nasa_Game/Fase_1_Arte/Exploracion/Lote_10/subidas_video.json. Tambien se acepta un UUID ya subido.
- Parametros comprobados con `higgsfield model get <modelo> --json` (2026-11-15):
    seedance_2_5: los fotogramas solo valen con --mode omni_reference; --start-image / --end-image;
                  --duration (entero, 4 a 30 s); --resolution 480p|720p|1080p|4k; --aspect_ratio
                  (por defecto 16:9); --generate_audio false apaga el audio (no cambia el precio).
    minimax_h3:   --start-image / --end-image (el final exige el inicial; no se mezclan con
                  referencias); --duration entero; --resolution solo "2K"; --aspect_ratio por
                  defecto "auto": se fija 16:9. No tiene parametro de audio: si trae pista, se
                  descarta con -an al montar.
- Cada encargo debe terminar con la proteccion fija y no nombrar marcas, misiones ni personas.
- Con --generar: cotiza, comprueba el tope, crea el trabajo con --wait (20 min), guarda la
  respuesta cruda en Lote_10/_json/<id>.json, baja result_url (el original, no la miniatura) a
  Lote_10/clips/<id>.mp4, anade la fila a Lote_10/registro_video.json y monta la hoja de revision
  (un cuadro cada 0,5 s, primero, medio y ultimo) en Lote_10/revision/<id>/.

Uso:
  python herramientas/hf_video.py --id P03_t1 --modelo minimax_h3 --inicial K03.png \
      --duracion 10 --encargo-archivo M03.txt [--final K.png] [--resolucion 720p] [--tope 20] [--generar]
  python herramientas/hf_video.py --lote tomas.json [--solo P03_t1,P06_t1] [--generar]
      (tomas.json: {"tope_total": 300, "tomas": [{"id", "plano", "modelo", "inicial", "final",
       "duracion", "resolucion", "encargo"}...]})
  python herramientas/hf_video.py --revisar Nasa_Game/.../clips/P03_t1.mp4   (solo la hoja, sin red)
  python herramientas/hf_video.py --id P03_t1 --recuperar <job_id>   (espera y baja un trabajo ya creado)
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
LOTE = RAIZ / "Nasa_Game" / "Fase_1_Arte" / "Exploracion" / "Lote_10"
CLIPS = LOTE / "clips"
CRUDOS = LOTE / "_json"
REVISION = LOTE / "revision"
REGISTRO = LOTE / "registro_video.json"
SUBIDAS = LOTE / "subidas_video.json"

cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe") if cmd else None

PROTECCION = "No text, no logos, no insignia, no emblems, no watermark."
# Palabras que no pueden ir en un encargo (marcas, mision, personas reales, agencias)
PROHIBIDAS = re.compile(r"\b(nasa|apollo|apolo|saturn|armstrong|aldrin|collins|kennedy|cape canaveral|"
                        r"usa|u\.s\.a|united states|nixon|cronkite|eagle|columbia|tranquility)\b", re.I)

# Modelo -> como se pasan sus parametros (comprobado con model get)
MODELOS = {
    "seedance_2_5": {"resoluciones": ["480p", "720p", "1080p", "4k"], "resolucion": "720p",
                     "duracion": (4, 30), "fijos": {"mode": "omni_reference", "generate_audio": "false"}},
    "minimax_h3": {"resoluciones": ["2K"], "resolucion": "2K", "duracion": (4, 12), "fijos": {}},
    "seedance_2_0_mini": {"resoluciones": ["480p", "720p"], "resolucion": "720p", "duracion": (5, 12),
                          "fijos": {"generate_audio": "false"}},
}


def hf(*args, timeout=1500):
    r = subprocess.run([HF, *args], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def es_uuid(texto):
    return bool(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", texto or ""))


def subir(ruta_o_id):
    """Ruta local -> id de subida (cacheado). Un UUID se devuelve tal cual. Subir no gasta creditos."""
    if es_uuid(ruta_o_id):
        return ruta_o_id
    ruta = Path(ruta_o_id)
    if not ruta.is_absolute():
        ruta = RAIZ / ruta
    if not ruta.exists():
        raise SystemExit(f"No existe el fotograma: {ruta}")
    mapa = json.loads(SUBIDAS.read_text(encoding="utf-8")) if SUBIDAS.exists() else {}
    clave = ruta.relative_to(RAIZ).as_posix()
    firma = f"{ruta.stat().st_size}-{int(ruta.stat().st_mtime)}"
    if clave in mapa and mapa[clave].get("firma") == firma:
        return mapa[clave]["id"]
    from PIL import Image  # solo hace falta al subir
    jpg = LOTE / "subidas" / (ruta.stem + ".jpg")
    jpg.parent.mkdir(parents=True, exist_ok=True)
    Image.open(ruta).convert("RGB").save(jpg, quality=95)
    for intento in range(3):
        code, out, err = hf("upload", "create", str(jpg), "--json", timeout=300)
        if code == 0:
            ident = json.loads(out)["id"]
            mapa[clave] = {"id": ident, "jpg": jpg.relative_to(RAIZ).as_posix(), "bytes": jpg.stat().st_size,
                           "firma": firma}
            SUBIDAS.parent.mkdir(parents=True, exist_ok=True)
            SUBIDAS.write_text(json.dumps(mapa, indent=1, ensure_ascii=False), encoding="utf-8")
            return ident
    raise SystemExit(f"No se pudo subir {clave}: {(err or out)[:200]}")


def validar(toma):
    modelo = toma["modelo"]
    if modelo not in MODELOS:
        raise SystemExit(f"{toma['id']}: modelo sin comprobar ({modelo}). Conocidos: {list(MODELOS)}")
    m = MODELOS[modelo]
    toma.setdefault("resolucion", m["resolucion"])
    if toma["resolucion"] not in m["resoluciones"]:
        raise SystemExit(f"{toma['id']}: {modelo} no admite {toma['resolucion']} ({m['resoluciones']})")
    d = int(toma["duracion"])
    if not m["duracion"][0] <= d <= m["duracion"][1]:
        raise SystemExit(f"{toma['id']}: duracion {d} s fuera de {m['duracion']}")
    if toma.get("final") and not toma.get("inicial"):
        raise SystemExit(f"{toma['id']}: el fotograma final exige el inicial")
    encargo = " ".join(toma["encargo"].split())
    if not encargo.endswith(PROTECCION):
        raise SystemExit(f"{toma['id']}: el encargo debe terminar con «{PROTECCION}»")
    hallado = PROHIBIDAS.search(encargo)
    if hallado:
        raise SystemExit(f"{toma['id']}: el encargo nombra «{hallado.group(0)}»: prohibido")
    if not re.fullmatch(r"[A-Za-z0-9_\-]+", toma["id"]):
        raise SystemExit(f"id invalido: {toma['id']}")
    toma["encargo"] = encargo


def argumentos(toma):
    """Lista de argumentos de la linea de comandos (sin 'generate create|cost')."""
    m = MODELOS[toma["modelo"]]
    a = [toma["modelo"], "--prompt", toma["encargo"]]
    if toma.get("inicial"):
        a += ["--start-image", subir(toma["inicial"])]
    if toma.get("final"):
        a += ["--end-image", subir(toma["final"])]
    a += ["--duration", str(int(toma["duracion"])), "--resolution", toma["resolucion"],
          "--aspect_ratio", toma.get("aspecto", "16:9")]
    for k, v in m["fijos"].items():
        a += [f"--{k}", v]
    return a


def cotizar(toma):
    code, out, err = hf("generate", "cost", *argumentos(toma), "--json", timeout=180)
    if code != 0:
        raise SystemExit(f"{toma['id']}: no se pudo cotizar: {(err or out)[:300]}")
    return float(json.loads(out)["credits"])


def saldo():
    code, out, _ = hf("account", "status", "--json", timeout=60)
    try:
        return float(json.loads(out)["credits"])
    except Exception:  # noqa: BLE001
        return None


def revisar(clip):
    """Un cuadro cada 0,5 s, hoja de contacto y primero/medio/ultimo a tamano completo. Sin red."""
    clip = Path(clip)
    destino = REVISION / clip.stem
    cuadros = destino / "cuadros"
    if cuadros.exists():
        shutil.rmtree(cuadros)
    cuadros.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf", "fps=2", str(cuadros / "%03d.png")],
                   check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "default=nw=1:nk=1", str(clip)], capture_output=True, text=True).stdout.strip())
    for nombre, t in (("primero", 0.0), ("medio", dur / 2), ("ultimo", max(dur - 0.05, 0))):
        extra = ["-sseof", "-0.1"] if nombre == "ultimo" else ["-ss", f"{t:.2f}"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", *extra, "-i", str(clip), "-frames:v", "1",
                        "-update", "1", str(destino / f"{nombre}.png")], check=True)
    subprocess.run(["magick", "montage", str(cuadros / "*.png"), "-tile", "6x", "-geometry", "320x180+4+4",
                    "-background", "#222", str(destino / "hoja.jpg")], check=True)
    print(f"  revision: {destino.relative_to(RAIZ).as_posix()} ({dur:.2f} s)")
    return destino


def generar(toma, costo):
    CLIPS.mkdir(parents=True, exist_ok=True)
    CRUDOS.mkdir(parents=True, exist_ok=True)
    destino = CLIPS / f"{toma['id']}.mp4"
    if destino.exists():
        raise SystemExit(f"Ya existe {destino.name}: usa otro id (p. ej. {toma['id']}_t2)")
    args = argumentos(toma)
    antes = saldo()
    code, out, err = hf("generate", "create", *args, "--wait", "--wait-timeout", "20m", "--json", timeout=1500)
    crudo = CRUDOS / f"{toma['id']}.json"
    crudo.write_text(out or err, encoding="utf-8")
    fila = {"id": toma["id"], "plano": toma.get("plano"), "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "modelo": toma["modelo"], "parametros": None,
            "inicial": toma.get("inicial"), "final": toma.get("final"), "encargo": toma["encargo"],
            "costo_cotizado": costo, "job_id": None, "url": None, "archivo": None, "estado": "error",
            "detalle": None, "saldo_antes": antes, "saldo_despues": None, "veredicto": "pendiente"}
    fila["parametros"] = [x for x in args[1:] if x != toma["encargo"] and x != "--prompt"]
    fila["job_id"], url, estado = leer_trabajo(out)
    if code != 0 or not url:
        fila["detalle"] = f"code={code} status={estado or '?'}: " + (err or out)[:300]
    else:
        fila["url"] = url
        bajar(fila, destino)
    fila["saldo_despues"] = saldo()
    anotar(fila)
    print(f"  {toma['id']:14} {fila['estado']:14} {fila['archivo'] or fila['detalle']}")
    if fila["estado"] == "ok":
        revisar(destino)
    return fila


def leer_trabajo(salida):
    """(job_id, result_url, status) de la salida --json de create/get/wait. result_url es el original;
    min_result_url es solo una miniatura y nunca se usa."""
    try:
        datos = json.loads(salida)
        trabajo = datos[0] if isinstance(datos, list) else datos
        if isinstance(trabajo, dict) and "job" in trabajo and isinstance(trabajo["job"], dict):
            trabajo = trabajo["job"]
        return trabajo.get("id"), trabajo.get("result_url"), trabajo.get("status")
    except Exception:  # noqa: BLE001 - salida no JSON: se busca a mano
        job = re.search(r'"id"\s*:\s*"([0-9a-f-]{36})"', salida or "")
        url = re.search(r'"result_url"\s*:\s*"([^"]+)"', salida or "")
        est = re.search(r'"status"\s*:\s*"([a-z_]+)"', salida or "")
        return (job.group(1) if job else None, url.group(1) if url else None, est.group(1) if est else None)


def bajar(fila, destino):
    try:
        peticion = urllib.request.Request(fila["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(peticion, timeout=300) as r:
            destino.write_bytes(r.read())
        fila.update(estado="ok", archivo=destino.relative_to(RAIZ).as_posix(), detalle=None)
    except Exception as error:  # noqa: BLE001
        fila.update(estado="sin descargar", detalle=str(error)[:200])


def anotar(fila):
    historial = json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else []
    historial.append(fila)
    REGISTRO.write_text(json.dumps(historial, indent=1, ensure_ascii=False), encoding="utf-8")


def recuperar(ident, job_id):
    """Trabajo que paso la espera de 20 min o no se pudo bajar: espera de nuevo y baja result_url.
    No crea trabajos ni gasta creditos."""
    code, out, err = hf("generate", "wait", job_id, "--timeout", "20m", "--quiet", "--json", timeout=1500)
    _, url, estado = leer_trabajo(out)
    destino = CLIPS / f"{ident}.mp4"
    fila = {"id": ident, "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "job_id": job_id,
            "recuperado": True, "url": url, "archivo": None, "estado": "error",
            "detalle": None if url else f"code={code} status={estado or '?'}: " + (err or out)[:300],
            "veredicto": "pendiente"}
    if url:
        CLIPS.mkdir(parents=True, exist_ok=True)
        bajar(fila, destino)
    anotar(fila)
    print(f"  {ident:14} {fila['estado']:14} {fila['archivo'] or fila['detalle']}")
    if fila["estado"] == "ok":
        revisar(destino)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id")
    ap.add_argument("--plano")
    ap.add_argument("--modelo")
    ap.add_argument("--encargo")
    ap.add_argument("--encargo-archivo")
    ap.add_argument("--inicial")
    ap.add_argument("--final")
    ap.add_argument("--duracion", type=int)
    ap.add_argument("--resolucion")
    ap.add_argument("--aspecto", default="16:9")
    ap.add_argument("--tope", type=float, help="Tope de creditos (por toma o, con --lote, del total)")
    ap.add_argument("--lote")
    ap.add_argument("--solo", default="")
    grupo = ap.add_mutually_exclusive_group()
    grupo.add_argument("--solo-cotizar", action="store_true", help="Por defecto: cotiza y no crea nada")
    grupo.add_argument("--generar", action="store_true", help="Crea el trabajo (gasta creditos)")
    ap.add_argument("--revisar", help="Monta la hoja de revision de un clip ya bajado (sin red)")
    ap.add_argument("--recuperar", metavar="JOB_ID",
                    help="Con --id: espera un trabajo ya creado y baja su result_url (no gasta)")
    ap.add_argument("--mostrar-comando", action="store_true", help="Imprime la linea de comandos exacta")
    a = ap.parse_args()

    if a.revisar:
        revisar(a.revisar)
        return
    if HF is None:
        raise SystemExit("No se encuentra higgsfield.cmd")
    if a.recuperar:
        if not a.id:
            raise SystemExit("--recuperar exige --id")
        recuperar(a.id, a.recuperar)
        return

    if a.lote:
        spec = json.loads(Path(a.lote).read_text(encoding="utf-8"))
        tomas = spec["tomas"]
        tope = a.tope if a.tope is not None else spec.get("tope_total")
        if a.solo:
            elegidas = set(a.solo.split(","))
            tomas = [t for t in tomas if t["id"] in elegidas]
    else:
        encargo = a.encargo or (Path(a.encargo_archivo).read_text(encoding="utf-8") if a.encargo_archivo else None)
        if not (a.id and a.modelo and encargo and a.duracion):
            raise SystemExit("Faltan --id, --modelo, --encargo/--encargo-archivo o --duracion")
        tomas = [{"id": a.id, "plano": a.plano, "modelo": a.modelo, "encargo": encargo, "inicial": a.inicial,
                  "final": a.final, "duracion": a.duracion, "aspecto": a.aspecto,
                  **({"resolucion": a.resolucion} if a.resolucion else {})}]
        tope = a.tope

    total = 0.0
    for t in tomas:
        validar(t)
        t["_costo"] = cotizar(t)
        total += t["_costo"]
        print(f"  cotizado {t['id']:14} {t['modelo']:16} {t['duracion']:>3} s {t['resolucion']:>5} "
              f"{'ini+fin' if t.get('final') else 'ini':7} {t['_costo']:7.2f}", flush=True)
        if a.mostrar_comando:
            linea = ["higgsfield.cmd", "generate", "create"] + argumentos(t) + ["--wait", "--wait-timeout", "20m",
                                                                               "--json"]
            print("    " + " ".join(f'"{x}"' if " " in x else x for x in linea))
    print(f"Total cotizado: {total:.2f} creditos" + (f" (tope: {tope})" if tope is not None else ""))
    if not a.generar:
        print("Solo cotizacion: no se creo ningun trabajo.")
        return
    if tope is None:
        raise SystemExit("Para generar hace falta --tope (o tope_total en el lote).")
    if total > float(tope):
        raise SystemExit("La cotizacion supera el tope: no se genera nada.")
    # una toma a la vez: cada clip se revisa antes de seguir gastando
    for t in tomas:
        generar(t, t["_costo"])


if __name__ == "__main__":
    main()
