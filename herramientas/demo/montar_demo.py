"""Monta el video demo de «Luz cenicienta» (150 s, 1920x1080, 30 cps) a partir de Nasa_Game/Presentacion/montaje.json.

COMO SE USA (desde la raiz del repositorio):

  python -I herramientas/demo/montar_demo.py --revisar
      Solo muestra el plan: que material usa cada segmento y que falta. No renderiza nada.

  python -I herramientas/demo/montar_demo.py --salida Nasa_Game/Presentacion/demo_v1.mp4 --hoja Nasa_Game/Presentacion/demo_v1_hoja.jpg
      Montaje completo. Los segmentos cuyo material no cambio se toman de la cache (intermedios/).

  python -I herramientas/demo/montar_demo.py --salida ... --solo S10,S23-S31
      Vuelve a renderizar SOLO esos segmentos (aunque su huella no cambie) y reutiliza los demas tal como esten
      en la cache; despues une, mezcla y codifica de nuevo (eso tarda unos minutos siempre).

  Otras opciones:
    --forzar               rehace todos los intermedios
    --hoja <jpg>           hoja de contacto: un cuadro cada 2 s con su tiempo debajo
    --solo-hoja <mp4>      solo hace la hoja de un video ya montado (con --hoja)
    --rapido               presets mas rapidos (para pruebas; peor compresion, misma nitidez)
    --preset-final <p>     preset x264 de la salida (por defecto veryfast: a 12 Mb/s no se ve diferencia con medium,
                           que tarda unas 3 veces mas en este i5; usar medium si sobra tiempo)
    --bajada-db <dB>       cuanto baja la musica bajo la voz (por defecto: mezcla.musica_bajo_voz_dB de montaje.json)
    --rampa <s>            rampa de la bajada (por defecto: mezcla.rampa_s de montaje.json)
    --fundido-rotulo <s>   fundido de entrada y salida de los rotulos (por defecto 0,3 s)
    --musica <ruta>        otra pista de musica (por defecto la de montaje.json, y si existe su *_automatizada.wav)
    --bajada auto|si|no    bajar la musica en las ventanas del expositor; 'auto' no la baja si la pista es la
                           *_automatizada (ya trae esa bajada hecha por herramientas/demo/audio_procesar.py)
    --lufs -16 --pico -1.5 objetivo de loudnorm

  Por defecto: musica audio/musica_demo.wav automatizada aqui (envolvente_musica): silencio hasta 11 s, notas del
  titulo a pleno, cama 15 dB bajo el pleno en las ventanas del expositor con rampas de 0,5 s, respiros a -6,
  minijuegos y cierre a pleno, fundido 148,5-149,5; efectos a -12 dB bajo la voz; sonido propio de los minijuegos a
  -6 dB; efectos bajo la voz a -20 dB (--efectos-voz-db); loudnorm a -16 LUFS y -1,5 dBTP.

  Archivos que lee (ademas de montaje.json, sin modificarlos):
    Nasa_Game/Presentacion/ajustes_montaje.json   ajustes del montador por segmento (fuente o rotulo), con su motivo
    montaje.json, campo 'material'        rutas y 'desde_s' elegidos al revisar las tomas: mandan sobre tomas_demo.json
    herramientas/demo/tomas_demo.json      que mp4 de material/ es cada toma T01..T30 y desde que segundo
    graficos/rotulos/rotulos.json          que PNG lleva cada rotulo ('G01 (titulo)' = capa G01_titulo.png)
    graficos/Gnn_*.png|mp4                 fondo del grafico; Gnn_fondo + Gnn_capa_1..N = capas que entran cada 1,5 s
    graficos/sello_ia.png                  sello de la cinematica; lineas_tv.png + vineta.png para el televisor
    audio/efectos_gancho.wav               premezcla de 0 a 17 s (sustituye a los efectos sueltos del gancho)

Que hace:
  1. Lee montaje.json (no lo modifica) y resuelve la fuente de cada segmento: clip de la cinematica, toma del juego
     (material/, ver herramientas/demo/tomas_demo.json para el mapa T01 -> archivo), grafico (graficos/G01*.png),
     o imagen fija. Si la fuente falta, prueba la 'alternativa'; si tampoco hay, pone un marcador negro con el
     nombre del segmento y sigue. Al final lista lo que falta.
  2. Renderiza cada segmento a intermedios/Sxx.mp4 (1920x1080, 30 cps, H.264 CRF 12, sin audio), con su duracion
     exacta en cuadros. Videos: recorte al tramo y escala Lanczos sin deformar (recorte centrado); pixel-art (minijuegos
     y juegos de los companeros) con vecino mas cercano. Imagenes fijas: movimiento lento (acercamiento, paneo, empuje,
     temblor) calculado con precision de subpixel en Python (PIL, remuestreo con filtro sobre la imagen original), sin
     temblor de redondeo. Transiciones: corte por defecto; disolvencia, mascara circular o cierre en punto donde
     montaje.json lo pide.
  3. Une los intermedios, superpone rotulos (PNG de graficos/ si existe; si no, se dibuja con la fuente de la interfaz
     del juego, Bahnschrift) con fundido y desplazamiento corto, nunca dos a la vez, y el sello «Imagenes recreadas con
     IA»; fundido desde negro al inicio y hacia negro al final.
  4. Audio: musica de audio/ (si no hay, silencio), bajada en las ventanas del expositor con rampas, efectos en sus
     tiempos (juego/audio/, audio/, Fase_4_Audio/Lote_A1/originales/), sonido propio de los minijuegos, loudnorm en
     dos pasadas (-16 LUFS, -1,5 dBTP) y AAC 192 kb/s.
  5. Salida H.264 perfil alto, yuv420p, 12 Mb/s (max 14), +faststart, y comprobacion con ffprobe de 4500 cuadros y
     150,0 s.

La carpeta Nasa_Game/Presentacion/intermedios/ es cache: se puede borrar entera.
"""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
Image.MAX_IMAGE_PIXELS = None

RAIZ = Path(__file__).resolve().parent.parent.parent
PRES = RAIZ / "Nasa_Game" / "Presentacion"
MONTAJE = PRES / "montaje.json"
AJUSTES = PRES / "ajustes_montaje.json"   # ajustes del montador (fuente o rotulo por segmento, con su motivo)
MATERIAL = PRES / "material"
GRAFICOS = PRES / "graficos"
AUDIO = PRES / "audio"
INTER = PRES / "intermedios"
TOMAS_CFG = Path(__file__).resolve().with_name("tomas_demo.json")
CARPETAS_EFECTOS = [AUDIO, RAIZ / "juego" / "audio", RAIZ / "Nasa_Game" / "Fase_4_Audio" / "Lote_A1" / "originales"]

W, H, FPS = 1920, 1080, 30
VERSION = "4"  # subir si cambia la forma de renderizar (invalida la cache)
CREMA = (0xF8, 0xC9, 0x91)
AMBAR = (0xF4, 0xA1, 0x59)
FUENTES_UI = [("C:/Windows/Fonts/bahnschrift.ttf", "SemiBold"), ("C:/Windows/Fonts/seguisb.ttf", None),
              ("C:/Windows/Fonts/segoeuib.ttf", None), ("C:/Windows/Fonts/arialbd.ttf", None)]
COLOR_709 = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
A709 = "scale=out_color_matrix=bt709:out_range=tv"
EXT_VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".webp"}
EXT_AUDIO = {".wav", ".ogg", ".mp3", ".flac", ".m4a", ".aac"}

EFECTOS_VOZ_DB = None  # --efectos-voz-db (por defecto -20: bajo la voz los efectos van a la altura de la cama)
PROPIO_DB = -6.0  # sonido propio de las tomas (minijuegos) bajo la musica: presente pero sin estorbar
PIXEL_TOMAS = {"T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19",
               "T22a", "T22", "T23", "T24", "T25", "T26"}


# ------------------------------------------------------------------ utilidades

def fr(t):
    return int(round(t * FPS + 1e-9))


def num(s):
    return float(str(s).replace(",", "."))


def norm(s):
    s = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def ruta_txt(p):
    return str(p).replace("\\", "/")


def rel(p):
    try:
        return ruta_txt(Path(p).resolve().relative_to(RAIZ))
    except Exception:
        return ruta_txt(p)


def ff(args, log=None):
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-y"] + [str(a) for a in args]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("ffmpeg fallo:\n" + " ".join(cmd)[:3000] + "\n" + r.stderr[-4000:])
    return r


_SONDA = {}


def sonda(p):
    """ffprobe con cache: {'ok', 'dur', 'w', 'h', 'audio'}"""
    p = Path(p)
    st = p.stat()
    clave = (str(p), st.st_size, st.st_mtime_ns)
    if clave in _SONDA:
        return _SONDA[clave]
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,pix_fmt:format=duration",
                        "-of", "json", str(p)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = {"ok": False, "dur": 0.0, "w": 0, "h": 0, "audio": False, "alfa": False}
    if r.returncode == 0:
        try:
            d = json.loads(r.stdout)
            for s in d.get("streams", []):
                if s.get("codec_type") == "video" and s.get("width"):
                    info["w"], info["h"] = s["width"], s["height"]
                    info["alfa"] = s.get("pix_fmt", "") in ("argb", "rgba", "abgr", "bgra", "yuva420p", "yuva444p",
                                                             "yuva444p10le", "gbrap", "ya8", "rgba64le")
                if s.get("codec_type") == "audio":
                    info["audio"] = True
            info["dur"] = float(d.get("format", {}).get("duration", 0) or 0)
            info["ok"] = info["w"] > 0 or (info["audio"] and info["dur"] > 0)
        except Exception:
            pass
    _SONDA[clave] = info
    return info


def huella_archivo(p):
    st = Path(p).stat()
    return [rel(p), st.st_size, st.st_mtime_ns]


def cargar_fuente(tam):
    for ruta, variante in FUENTES_UI:
        if Path(ruta).exists():
            f = ImageFont.truetype(ruta, tam)
            if variante:
                try:
                    f.set_variation_by_name(variante)
                except Exception:
                    pass
            return f
    return ImageFont.load_default()


# ------------------------------------------------------------------ resolucion de fuentes

def buscar_ruta(texto):
    """'Nasa_Game/x.png (2,5-4,5)' -> (Path o None, extra, ruta_limpia)"""
    texto = str(texto).strip()
    m = re.match(r"^(.*?\.(?:png|jpe?g|webp|mp4|mov|webm|mkv|avi))\s*(?:\((.*)\))?\s*$", texto, re.I)
    limpia, extra = (m.group(1).strip(), (m.group(2) or "").strip()) if m else (texto, "")
    for base in (RAIZ, RAIZ / "Nasa_Game"):
        for variante in {limpia, unicodedata.normalize("NFC", limpia), unicodedata.normalize("NFD", limpia)}:
            p = base / variante
            if p.exists() and p.is_file():
                return p, extra, limpia
    return None, extra, limpia


def rango_de(extra):
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*-\s*(\d+(?:[.,]\d+)?)", extra or "")
    return (num(m.group(1)), num(m.group(2))) if m else None


_TOMAS_CFG = None


def resolver_toma(tid, sid=None):
    """-> (Path, desde, recorte_inferior, nota) o (None, 0, 0, motivo)"""
    global _TOMAS_CFG
    if _TOMAS_CFG is None:
        _TOMAS_CFG = json.loads(TOMAS_CFG.read_text(encoding="utf-8")) if TOMAS_CFG.exists() else {}
    cfg = _TOMAS_CFG.get(tid, {})
    candidatos = []
    if MATERIAL.exists():
        for p in sorted(MATERIAL.iterdir()):
            if p.suffix.lower() in EXT_VIDEO and (p.stem.lower() == tid.lower() or p.stem.lower().startswith(tid.lower() + "_")):
                candidatos.append(p)
    tj = MATERIAL / "tomas.json"
    if tj.exists():
        try:
            for nombre, d in json.loads(tj.read_text(encoding="utf-8")).items():
                if isinstance(d, dict) and (d.get("toma") == tid or tid in (d.get("tomas") or [])):
                    candidatos.append(MATERIAL / d.get("archivo", nombre + ".mp4"))
        except Exception:
            pass
    for nombre in cfg.get("archivos", []):
        candidatos.append(MATERIAL / (nombre + ".mp4"))
    motivo = "sin archivo en material/"
    for p in candidatos:
        if p.exists():
            info = sonda(p)
            if not info["ok"] or info["w"] == 0:
                motivo = f"{p.name} ilegible (¿se esta grabando?)"
                continue
            desde = float(cfg.get("desde", 0.0))
            if "desde_final" in cfg:
                desde = max(0.0, info["dur"] - float(cfg["desde_final"]))
            if sid and sid in (cfg.get("desde_por_segmento") or {}):
                desde = float(cfg["desde_por_segmento"][sid])
            return p, desde, int(cfg.get("recorte_inferior", 0)), p.name
    return None, 0.0, 0, motivo


def es_capa_alfa(p):
    try:
        with Image.open(p) as im:
            return im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 250
    except Exception:
        return False


def buscar_grafico(gid, reves=False):
    """Fondo del grafico <gid>. Reglas (graficos/ de la presentacion):
    - video legible (G01_apertura.mp4) antes que imagen; para el cierre, uno con 'reves/cierre' o el mismo invertido;
    - se descartan las capas con transparencia (G01_titulo.png, G04_equipo_capa.png...): van como rotulo o capa;
    - 'sobre_negro' (titulo ya incrustado) solo si no hay otra cosa, para no duplicar el rotulo;
    - si hay <gid>_fondo + <gid>_capa_N, se devuelve el fondo y las capas se animan (ver capas_grafico)."""
    if not GRAFICOS.exists():
        return None
    g = gid.lower()
    cand = [p for p in GRAFICOS.glob("*") if p.is_file() and p.suffix.lower() in EXT_IMAGEN | EXT_VIDEO
            and (norm(p.stem) == g or norm(p.stem).startswith(g + "_"))]
    if capas_grafico(gid):
        fondo = [p for p in cand if "fondo" in norm(p.stem)]
        if fondo:
            return fondo[0]

    def puntos(p):
        s = norm(p.stem)
        es_video = p.suffix.lower() in EXT_VIDEO
        if es_video and not sonda(p)["ok"]:
            return None
        if not es_video and es_capa_alfa(p):
            return None
        pt = 100 if es_video else 0
        if any(k in s for k in ("reves", "cierre", "inverso")):
            pt += 50 if reves else -200
        if "sobre_negro" in s:
            pt -= 60
        if "fondo" in s:
            pt -= 30
        return pt - 0.01 * len(s)

    validos = [(puntos(p), p) for p in cand]
    validos = [x for x in validos if x[0] is not None]
    if not validos:
        return None
    return max(validos, key=lambda x: x[0])[1]


def capas_grafico(gid):
    if not GRAFICOS.exists():
        return []
    capas = []
    for p in GRAFICOS.glob(f"{gid}_capa_*.png"):
        m = re.search(r"capa_(\d+)$", p.stem)
        if m:
            capas.append((int(m.group(1)), p))
    return [p for _, p in sorted(capas)]


def es_pixel(ruta=None, toma=None, dic=None):
    if dic and isinstance(dic, dict) and dic.get("minijuego"):
        return True
    if toma and toma in PIXEL_TOMAS:
        return True
    s = norm(ruta_txt(ruta or ""))
    return any(k in s for k in ("mision artemis", "marte_gravedad", "/minijuegos/", "/mj_", "/artemis_", "/marte_"))


def material_unidades(seg):
    """campo 'material' de montaje.json (rutas reales escritas por material_montaje.py) -> unidades de fuente.
    Se omiten los textos y los graficos (estos se resuelven por su id en 'fuente')."""
    unidades = []
    for m in seg.get("material") or []:
        if not isinstance(m, dict) or not m.get("ruta"):
            continue
        tipo = norm(m.get("tipo", ""))
        if tipo == "video":
            u = {"video": m["ruta"], "desde": float(m.get("desde_s", 0.0) or 0.0)}
        elif tipo == "fija":
            u = {"imagen": m["ruta"]}
        else:
            continue
        if "de" in m and "a" in m:
            u["de"], u["a"] = float(m["de"]), float(m["a"])
        unidades.append(u)
    return unidades


def material_de_toma(seg, u):
    """video del 'material' que corresponde a la unidad de toma u (por tramo de/a, o el primero) -> (Path, desde)"""
    for m in material_unidades(seg):
        if "video" not in m:
            continue
        if "de" in u and ("de" not in m or abs(m["de"] - float(u["de"])) > 1e-6):
            continue
        p, _, _ = buscar_ruta(m["video"])
        if p is not None and sonda(p)["ok"]:
            return p, m["desde"]
    return None, 0.0


def pieza_marcador(seg, t0, t1, que):
    return {"tipo": "marcador", "t0": t0, "t1": t1, "texto": f"{seg['id']} · falta {que}", "mov": "fijo"}


def pieza_de_ruta(p, t0, t1, mov, pixel, extra=""):
    tipo = "video" if p.suffix.lower() in EXT_VIDEO else "imagen"
    d = {"tipo": tipo, "ruta": p, "t0": t0, "t1": t1, "mov": mov, "pixel": pixel, "desde": 0.0}
    if "sello" in norm(extra):
        d["sello"] = "Imágenes recreadas con IA"
    return d


def resolver_unidad(seg, u, t0, t1, mov, faltan, etiqueta):
    """Una fuente (dict o texto) para [t0,t1] -> pieza o None si no existe."""
    if isinstance(u, str):
        p, extra, limpia = buscar_ruta(u)
        if p is None:
            faltan.append(f"{etiqueta} {limpia}")
            return None
        if p.suffix.lower() in EXT_VIDEO and not sonda(p)["ok"]:
            faltan.append(f"{etiqueta} {limpia} ilegible")
            return None
        return pieza_de_ruta(p, t0, t1, mov, es_pixel(p), extra)
    if not isinstance(u, dict):
        return None
    if "clip" in u:
        p, extra, limpia = buscar_ruta(u["clip"])
        if p is None or not sonda(p)["ok"]:
            faltan.append(f"{etiqueta} clip {Path(limpia).name}")
            return None
        d = pieza_de_ruta(p, t0, t1, "fijo", False)
        d["mov_original"] = mov
        return d
    if "video" in u:
        p, extra, limpia = buscar_ruta(u["video"])
        if p is None or not sonda(p)["ok"]:
            faltan.append(f"{etiqueta} video {Path(limpia).name}")
            return None
        d = {"tipo": "video", "ruta": p, "t0": t0, "t1": t1, "mov": "fijo", "desde": float(u.get("desde", 0.0)),
             "recorte_inf": 0, "pixel": es_pixel(p), "audio_propio": False}
        # v2: movimiento sobre el video (acercamiento a una zona), velocidad (camara lenta) y color (eq de ffmpeg)
        if u.get("mov") and norm(u["mov"]) != "fijo":
            d["vmov"] = u["mov"]
        if u.get("velocidad"):
            d["velocidad"] = float(u["velocidad"])
        if u.get("eq"):
            d["eq"] = str(u["eq"])
        return d
    if "toma" in u:
        tid = u["toma"]
        p, desde, rinf, nota = resolver_toma(tid, seg.get("id"))
        pm, dm = material_de_toma(seg, u)
        if pm is not None:  # material elegido a mano (montaje.json, campo material): manda sobre tomas_demo.json
            p, desde, nota = pm, dm, pm.name
        if p is None:
            faltan.append(f"{etiqueta} toma {tid} ({nota})")
            return None
        return {"tipo": "video", "ruta": p, "t0": t0, "t1": t1, "mov": "fijo", "desde": desde, "recorte_inf": rinf,
                "pixel": es_pixel(p, tid, u), "toma": tid, "audio_propio": False}
    if "grafico" in u:
        gid = u["grafico"]
        reves = "reves" in norm(u.get("sentido", ""))
        p = buscar_grafico(gid, reves)
        if p is None:
            faltan.append(f"{etiqueta} grafico {gid}")
            return None
        d = pieza_de_ruta(p, t0, t1, mov if p.suffix.lower() in EXT_IMAGEN else "fijo", False)
        d["grafico"] = gid
        if "fondo" in norm(p.stem) and capas_grafico(gid):
            d["capas"] = capas_grafico(gid)
            d["mov"] = "fijo"
        if reves and p.suffix.lower() in EXT_VIDEO and not any(k in norm(p.stem) for k in ("reves", "cierre", "inverso")):
            d["invertir"] = True
        return d
    if "imagen" in u:
        p, extra, limpia = buscar_ruta(u["imagen"])
        if p is None:
            faltan.append(f"{etiqueta} {limpia}")
            return None
        d = pieza_de_ruta(p, t0, t1, u.get("mov", mov), es_pixel(p), extra)
        if "casilla" in u:
            m = re.search(r"fila\s*(\d+)\D+col\D*(\d+)", norm(u["casilla"]))
            if m:
                d["casilla"] = (int(m.group(1)) - 1, int(m.group(2)) - 1)
        return d
    return None


def resolver_secuencia(seg, fuente, mov, faltan, etiqueta):
    """fuente -> lista de piezas que cubren [inicio, fin], o None si alguna parte esencial falta."""
    a, b = seg["inicio"], seg["fin"]
    if isinstance(fuente, list):
        partes = []
        sin_rango = []
        for u in fuente:
            r = None
            if isinstance(u, dict) and "de" in u:
                r = (float(u["de"]), float(u["a"]))
            elif isinstance(u, str):
                r = rango_de(buscar_ruta(u)[1])
            partes.append([u, r])
            if r is None:
                sin_rango.append(u)
        if sin_rango:  # reparto parejo
            n = len(partes)
            for i, pr in enumerate(partes):
                pr[1] = (a + (b - a) * i / n, a + (b - a) * (i + 1) / n)
        partes[0][1] = (a, partes[0][1][1])
        partes[-1][1] = (partes[-1][1][0], b)
        for i in range(1, len(partes)):
            partes[i][1] = (partes[i - 1][1][1], partes[i][1][1])
        piezas = []
        for u, (t0, t1) in partes:
            pz = resolver_unidad(seg, u, t0, t1, mov, faltan, etiqueta)
            piezas.append(pz)
        return piezas
    pz = resolver_unidad(seg, fuente, a, b, mov, faltan, etiqueta)
    return [pz]


def planificar(montaje):
    segs = montaje["segmentos"]
    dur_total = float(montaje["salida"].get("duracion_s", 150.0))
    planes = []
    avisos = []
    # continuidad
    for i, s in enumerate(segs):
        if i == 0 and abs(s["inicio"]) > 1e-6:
            avisos.append(f"{s['id']} empieza en {s['inicio']} y no en 0: se adelanta")
        if i > 0 and abs(s["inicio"] - segs[i - 1]["fin"]) > 1e-6:
            avisos.append(f"{s['id']} no empieza donde acaba {segs[i - 1]['id']} ({segs[i - 1]['fin']} -> {s['inicio']}); se ajusta")
    ajustes = {}
    if AJUSTES.exists():
        ajustes = json.loads(AJUSTES.read_text(encoding="utf-8")).get("segmentos", {})
    for i, s0 in enumerate(segs):
        s = dict(s0)
        aj = ajustes.get(s["id"], {})
        if "fuente" in aj:
            s["fuente"], s["material"], s["alternativa"] = aj["fuente"], None, None
            avisos.append(f"{s['id']}: fuente cambiada por ajustes_montaje.json ({aj.get('motivo', '')[:90]})")
        elif not ("partida" in norm(s.get("recorte") or "")):
            # material con tramos (de/a) escrito por material_montaje.py: manda sobre la fuente teorica
            mat = material_unidades(s)
            if len(mat) >= 2 and all("de" in u for u in mat):
                s["fuente"] = mat
        if "rotulo" in aj:
            if aj["rotulo"] is None:
                s["rotulo"] = None
                avisos.append(f"{s['id']}: rotulo quitado por ajustes_montaje.json ({aj.get('motivo', '')[:90]})")
            else:
                r = dict(s.get("rotulo") or {"inicio": s["inicio"] + 0.3, "fin": s["fin"] - 0.3})
                r["texto"], r["ajustado"] = aj["rotulo"], True
                s["rotulo"] = r
                avisos.append(f"{s['id']}: rotulo «{aj['rotulo']}» por ajustes_montaje.json")
        s["inicio"] = 0.0 if i == 0 else planes[-1]["fin"]
        if i == len(segs) - 1 and abs(s["fin"] - dur_total) > 1e-6:
            avisos.append(f"ultimo segmento {s['id']} acaba en {s['fin']}: se ajusta a {dur_total}")
            s["fin"] = dur_total
        mov = s.get("movimiento") or "fijo"
        recorte = norm(s.get("recorte") or "ninguno")
        faltan = []
        fuente = s.get("fuente")
        partida = "partida" in recorte and isinstance(fuente, list)
        usado = "fuente"
        if partida:
            partes = [resolver_unidad(s, u, s["inicio"], s["fin"], (u.get("mov") if isinstance(u, dict) else None) or "fijo",
                                      faltan, "fuente") for u in fuente]
            partes = [p or pieza_marcador(s, s["inicio"], s["fin"], describir_fuente(u)) for p, u in zip(partes, fuente)]
            piezas = [{"tipo": "partida", "partes": partes, "t0": s["inicio"], "t1": s["fin"], "mov": "fijo"}]
        else:
            piezas = resolver_secuencia(s, fuente, mov, faltan, "fuente")
            if any(p is None for p in piezas) and s.get("alternativa") is not None and not isinstance(fuente, list):
                alt = resolver_secuencia(s, s["alternativa"], mov, faltan, "alternativa")
                if all(p is not None for p in alt):
                    piezas, usado = alt, "alternativa"
            if any(p is None for p in piezas):
                usado = "marcador" if all(p is None for p in piezas) else usado + " + marcador"
                piezas = [p or None for p in piezas]
                for k, p in enumerate(piezas):
                    if p is None:
                        # tramo de la pieza que falta
                        if isinstance(fuente, list) and len(piezas) == len(fuente):
                            u = fuente[k]
                            t0 = float(u.get("de", s["inicio"])) if isinstance(u, dict) else s["inicio"]
                            t1 = float(u.get("a", s["fin"])) if isinstance(u, dict) else s["fin"]
                        else:
                            t0, t1 = s["inicio"], s["fin"]
                        que = describir_fuente(fuente[k] if isinstance(fuente, list) else fuente)
                        piezas[k] = pieza_marcador(s, t0, t1, que)
        for p in piezas:
            if "4:3" in recorte:
                p["recorte"] = "4:3"
        # transiciones internas
        movn, tn = norm(mov), norm(s.get("transicion_entrada") or "")
        trans_int = []
        ocular = GRAFICOS / "ocular_abre.mov"
        for k in range(1, len(piezas)):
            if ("mascara circular" in tn or "ocular" in tn) and ocular.exists() and sonda(ocular)["ok"]:
                # corte al ocular: negro con el ocular que se abre (graficos/ocular_abre.mov, con alfa) encima
                trans_int.append(("corte", 0.0))
                piezas[k]["superponer"] = ocular
            elif "mascara circular" in tn or "ocular" in tn:
                trans_int.append(("circleopen", 0.6))
            elif "disolvencia" in movn:
                m = re.search(r"disolvencia\s*(\d+(?:[.,]\d+)?)", movn)
                trans_int.append(("fade", num(m.group(1)) if m else 0.3))
            else:
                trans_int.append(("corte", 0.0))
        entrada = None
        negro = 0.0
        if "disolvencia" in tn and i > 0:
            m = re.search(r"disolvencia\s*(\d+(?:[.,]\d+)?)", tn)
            entrada = ("fade", num(m.group(1)) if m else 0.5)
        elif ("cierre en punto" in tn or "punto de luz" in tn) and i > 0:
            pz0 = piezas[0]
            if (len(piezas) == 1 and pz0.get("tipo") == "video" and sonda(pz0["ruta"]).get("alfa")
                    and planes[-1]["piezas"][-1]["tipo"] == "video"):
                # el grafico (G01_cierre.mov) ya trae el iris que se cierra: va ENCIMA de la toma anterior, que sigue
                pz0["fondo_previo"] = dict(planes[-1]["piezas"][-1])
            else:
                entrada = ("circleclose", 1.0)
        elif "desde negro" in tn:
            m = re.search(r"(\d+(?:[.,]\d+)?)\s*s", tn)
            negro = num(m.group(1)) if m else 0.5
        sello = s.get("sello")
        for p in piezas:
            if p.get("sello") and not sello:
                sello = p["sello"]
        planes.append({"id": s["id"], "inicio": s["inicio"], "fin": s["fin"], "n": fr(s["fin"]) - fr(s["inicio"]),
                       "piezas": piezas, "trans_int": trans_int, "entrada": entrada, "negro": negro,
                       "faltan": faltan, "usado": usado, "seg": s, "sello": sello})
    return planes, avisos


def describir_fuente(u):
    if isinstance(u, dict):
        for k in ("toma", "grafico", "clip", "imagen"):
            if k in u:
                return f"{k} {Path(str(u[k])).name}"
    if isinstance(u, list):
        return " + ".join(describir_fuente(x) for x in u)
    return Path(str(u)).name


def describir_pieza(p):
    if p["tipo"] == "marcador":
        return f"MARCADOR ({p['texto']})"
    if p["tipo"] == "partida":
        return "partida[" + " | ".join(describir_pieza(x) for x in p["partes"]) + "]"
    s = rel(p["ruta"])
    if p.get("toma"):
        s = f"{p['toma']}={Path(p['ruta']).name} desde {p.get('desde', 0):.2f}s"
    extra = []
    if p.get("casilla"):
        extra.append(f"casilla {p['casilla'][0] + 1},{p['casilla'][1] + 1}")
    if p.get("pixel"):
        extra.append("pixel")
    if p["tipo"] == "imagen" and norm(p.get("mov", "fijo")) != "fijo":
        extra.append(p["mov"])
    return s + (f" [{'; '.join(extra)}]" if extra else "")


# ------------------------------------------------------------------ imagenes fijas con movimiento (PIL)

def suave(p):
    p = min(1.0, max(0.0, p))
    return 0.5 * p + 0.5 * (0.5 - 0.5 * math.cos(math.pi * p))


def parse_mov(texto, dur):
    t = norm(texto or "fijo")
    efectos = []
    if "grano" in t or "barrido" in t:
        efectos.append("tv")
    if "franja ambar" in t:
        efectos.append("franja")
    z0 = z1 = 1.0
    f0 = f1 = (0.5, 0.5)
    temblor = 0.0
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*-+>\s*(\d+(?:[.,]\d+)?)\s*%", t)
    if "temblor" in t:
        mt = re.search(r"temblor\s*(\d+(?:[.,]\d+)?)", t)
        temblor = (num(mt.group(1)) if mt else 1.0) / 100.0
        z0 = z1 = 1.0 + 2.5 * temblor
    if "alejamiento de una casilla" in t:
        z0, z1, f0, f1 = 3.0, 1.0, ("casilla", 0, 0), (0.5, 0.5)
    elif "acercamiento" in t or "empuje" in t:
        if m:
            z0, z1 = num(m.group(1)) / 100, num(m.group(2)) / 100
        elif "empuje" in t:
            ms = re.search(r"empuje\s*(\d+(?:[.,]\d+)?)\s*%\s*/\s*s", t)
            mp = re.search(r"empuje\s*(\d+(?:[.,]\d+)?)\s*%", t)
            if ms:
                z1 = z0 * (1 + num(ms.group(1)) / 100 * dur)
            elif mp:
                z1 = z0 * (1 + num(mp.group(1)) / 100)
            else:
                z1 = z0 * 1.04
        else:
            z1 = z0 * 1.06
        fx, fy = 0.5, 0.5
        if "arriba" in t:
            fy = 0.25
        if "abajo" in t:
            fy = 0.75
        if "izquierda" in t:
            fx = 0.25
        if "derecha" in t:
            fx = 0.75
        if (fx, fy) != (0.5, 0.5):
            z1 = max(z1, 1.25) if not m else z1
        f0 = f1 = (fx, fy)
    elif "alejamiento" in t or "se aleja" in t:
        z0, z1 = 1.08, 1.0
    elif "paneo vertical" in t or "inclinacion" in t:
        mp = re.search(r"(\d+(?:[.,]\d+)?)\s*%", t)
        z = 1.0 + (num(mp.group(1)) / 100 if mp else 0.06)
        z0 = z1 = max(z0, z)
        if "abajo" in t:
            f0, f1 = (0.5, 0.0), (0.5, 1.0)
        else:
            f0, f1 = (0.5, 1.0), (0.5, 0.0)
    elif "paneo" in t:
        mp = re.search(r"(\d+(?:[.,]\d+)?)\s*%", t)
        z = 1.0 + (num(mp.group(1)) / 100 if mp else 0.08)
        z0 = z1 = max(z0, z)
        f0, f1 = (0.0, 0.5), (1.0, 0.5)
    # los efectos ('tv', 'franja') se aplican con filtros de ffmpeg en el grafo del segmento (ver Grafo.efectos):
    # no obligan a calcular cada cuadro en Python
    estatico = (z0 == z1 and f0 == f1 and temblor == 0)
    return {"z0": z0, "z1": z1, "f0": f0, "f1": f1, "temblor": temblor, "efectos": efectos, "estatico": estatico,
            "paneo_auto": "paneo" in t and "vertical" not in t and "lateral" not in t}


_MASCARA_TV = {}


def mascara_tv(bh, bw):
    """vineta de tubo * lineas de barrido * 0,92 (precalculada)"""
    if (bh, bw) not in _MASCARA_TV:
        yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32)
        v = np.clip(1 - 0.35 * (((xx - bw / 2) / (bw / 2)) ** 2 + ((yy - bh / 2) / (bh / 2)) ** 2) ** 1.5, 0.4, 1)
        v[::3, :] *= 0.86
        _MASCARA_TV[(bh, bw)] = (v * 0.92)[:, :, None]
    return _MASCARA_TV[(bh, bw)]


_CACHE_IMG = {}


def preparar_imagen(p, casilla=None, pixel=False, caja=(W, H), mitad=None, zmin=None):
    """Imagen de trabajo en RGB. Con zmin, se reduce una vez (Lanczos) para que la ventana mas grande del movimiento
    mida lo mismo que la caja de salida: asi cada cuadro remuestrea casi 1:1, rapido y sin aliasing."""
    clave = (str(p), casilla, pixel, caja, mitad, zmin)
    if clave in _CACHE_IMG:
        return _CACHE_IMG[clave]
    if zmin is not None and not pixel:
        im = preparar_imagen(p, casilla, False, caja, mitad, None)
        iw, ih = im.size
        bw, bh = caja
        base_w = ih * bw / bh if iw / ih > bw / bh else iw
        s = bw * zmin / base_w
        if s < 0.97:
            im = im.resize((max(1, round(iw * s)), max(1, round(ih * s))), Image.Resampling.LANCZOS)
        _CACHE_IMG[clave] = im
        return im
    im = Image.open(p)
    im.load()
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fondo = Image.new("RGBA", im.size, (0, 0, 0, 255))
        fondo.alpha_composite(im)
        im = fondo
    im = im.convert("RGB")
    if casilla is not None:
        iw, ih = im.size
        cw = (iw - ih) * 16 / 21 if iw > ih else iw / 3
        ch = cw * 9 / 16
        bx = (iw - 3 * cw) / 4
        by = (ih - 3 * ch) / 4
        r, c = casilla
        x0, y0 = bx + c * (cw + bx), by + r * (ch + by)
        im = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
    if mitad is not None and im.size == (W, H):
        # grafico a pantalla completa puesto en media pantalla: se toma la mitad con mas contenido
        a = np.asarray(im.convert("L"), dtype=np.float32)
        opciones = {0: a[:, :W // 2].sum(), W // 4: a[:, W // 4:W // 4 + W // 2].sum(), W // 2: a[:, W // 2:].sum()}
        x = max(opciones, key=opciones.get)
        im = im.crop((x, 0, x + W // 2, H))
    if pixel:
        # x2 sobre lo necesario seria mas nitido pero triplica el tiempo por cuadro; x1,3 basta a 1080p
        k = math.ceil(max(caja[0] / im.size[0], caja[1] / im.size[1]) * 1.3)
        if k > 1:
            im = im.resize((im.size[0] * k, im.size[1] * k), Image.Resampling.NEAREST)
    _CACHE_IMG[clave] = im
    return im


class Estela:
    """Ruido de grano precalculado para el efecto de televisor."""
    tex = None

    @classmethod
    def textura(cls, i, h, w):
        if cls.tex is None or cls.tex[0].shape != (h, w):
            rng = np.random.default_rng(7)
            cls.tex = [rng.normal(0, 9, (h, w, 1)).astype(np.float32) for _ in range(6)]
        return cls.tex[i % 6]


def cuadro_imagen(im, mv, t, t0, t1, caja, efectos, filtro=None):
    iw, ih = im.size
    bw, bh = caja
    p = (t - t0) / max(1e-6, (t1 - t0))
    e = suave(p)
    z = mv["z0"] * (mv["z1"] / mv["z0"]) ** e
    if mv["f0"][0] == "casilla":
        # de la casilla (1,1) de una rejilla 3x3 a la imagen entera
        cf = (1 / 6, 1 / 6)
        f = (cf[0] + (0.5 - cf[0]) * e, cf[1] + (0.5 - cf[1]) * e)
    else:
        f = (mv["f0"][0] + (mv["f1"][0] - mv["f0"][0]) * e, mv["f0"][1] + (mv["f1"][1] - mv["f0"][1]) * e)
    if iw / ih > bw / bh:
        wh = ih
        ww = ih * bw / bh
    else:
        ww = iw
        wh = iw * bh / bw
    if mv.get("paneo_auto") and iw / ih < (bw / bh) * 0.92:
        # imagen mas alta que el cuadro: el paneo va de arriba abajo y muestra toda la altura
        z = 1.0
        f = (0.5, e)
    ww, wh = ww / z, wh / z
    cx = min(max(f[0] * iw, ww / 2), iw - ww / 2)
    cy = min(max(f[1] * ih, wh / 2), ih - wh / 2)
    if mv["temblor"]:
        a = mv["temblor"] * 0.5
        cx += ww * a * (0.6 * math.sin(2 * math.pi * 7.3 * t + 1.1) + 0.4 * math.sin(2 * math.pi * 12.7 * t + 0.3))
        cy += wh * a * (0.6 * math.sin(2 * math.pi * 6.1 * t + 2.0) + 0.4 * math.sin(2 * math.pi * 11.3 * t + 4.2))
    caja_src = (cx - ww / 2, cy - wh / 2, cx + ww / 2, cy + wh / 2)
    if filtro is None:
        filtro = Image.Resampling.BICUBIC
    out = im.resize((bw, bh), filtro, box=caja_src)
    if efectos:
        a = np.asarray(out, dtype=np.float32)
        if "tv" in efectos:
            i = int(round(t * FPS))
            yb = ((t * 0.45) % 1.0) * (bh * 1.3) - bh * 0.15
            ys = np.arange(bh, dtype=np.float32)
            banda = (np.exp(-((ys - yb) / (bh * 0.05)) ** 2) * 18 + 6)[:, None, None]
            a *= mascara_tv(bh, bw)
            a += Estela.textura(i, bh, bw)
            a += banda
        if "franja" in efectos:
            yc = bh * (1.15 - 1.3 * min(1.0, max(0.0, p)))
            ys = np.arange(bh, dtype=np.float32)
            banda = np.exp(-((ys - yc) / (bh * 0.12)) ** 2) * 0.22
            a += banda[:, None, None] * np.array(AMBAR, dtype=np.float32)[None, None, :]
        out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return out


def lienzo(pieza, caja_total=(W, H)):
    """caja de dibujo y posicion dentro del cuadro segun el recorte"""
    if pieza.get("recorte") == "4:3":
        bw = round(caja_total[1] * 4 / 3)
        return (bw, caja_total[1]), ((caja_total[0] - bw) // 2, 0)
    return caja_total, (0, 0)


def marco_pieza(pieza, t, caja_total, mv, mitad=None):
    caja, pos = lienzo(pieza, caja_total)
    if pieza["tipo"] == "marcador":
        return cuadro_marcador(pieza["texto"], caja_total)
    if pieza.get("capas"):
        return cuadro_capas(pieza, t, caja_total)
    if pieza.get("pixel") and mv["estatico"]:
        # pixel-art quieto: vecino mas cercano directo sobre el original
        im = preparar_imagen(pieza["ruta"], pieza.get("casilla"), False, caja, mitad)
        out = cuadro_imagen(im, mv, t, pieza["t0"], pieza["t1"], caja, [], Image.Resampling.NEAREST)
    else:
        zmin = 1.0 if mv.get("paneo_auto") else min(mv["z0"], mv["z1"])
        im = preparar_imagen(pieza["ruta"], pieza.get("casilla"), pieza.get("pixel", False), caja, mitad, zmin)
        out = cuadro_imagen(im, mv, t, pieza["t0"], pieza["t1"], caja, [])
    if caja != caja_total:
        fondo = Image.new("RGB", caja_total, (0, 0, 0))
        fondo.paste(out, pos)
        out = fondo
    return out


_CAPAS = {}
PASO_CAPAS = 0.8     # v2: el triptico entra de izquierda a derecha cada 0,8 s (antes 1,5: dejaba la derecha vacia)
ENTRADA_CAPA = 0.45  # fundido y desplazamiento de cada capa


def cuadro_capas(pieza, t, caja):
    """fondo del grafico + capas <gid>_capa_N que entran una tras otra con fundido y deslizamiento corto"""
    clave = (str(pieza["ruta"]), tuple(str(c) for c in pieza["capas"]), caja)
    if clave not in _CAPAS:
        fondo = np.asarray(preparar_imagen(pieza["ruta"], None, False, caja).resize(caja, Image.Resampling.LANCZOS),
                           dtype=np.float32)
        capas = []
        for c in pieza["capas"]:
            im = Image.open(c).convert("RGBA")
            if im.size != caja:
                im = im.resize(caja, Image.Resampling.LANCZOS)
            bb = im.getchannel("A").getbbox() or (0, 0, 1, 1)
            a = np.asarray(im.crop(bb), dtype=np.float32)
            capas.append((bb, a[:, :, :3], a[:, :, 3:] / 255.0))
        _CAPAS[clave] = (fondo, capas)
    fondo, capas = _CAPAS[clave]
    out = fondo.copy()
    for k, (bb, rgb, alfa) in enumerate(capas):
        e = (t - (pieza["t0"] + k * PASO_CAPAS)) / ENTRADA_CAPA
        if e <= 0:
            continue
        e = min(1.0, e)
        ease = 1 - (1 - e) ** 3
        dx = int(round(-30 * (1 - ease)))
        x0, y0 = bb[0] + dx, bb[1]
        h_, w_ = rgb.shape[:2]
        xa, xb = max(0, x0), min(caja[0], x0 + w_)
        if xb <= xa:
            continue
        sub = out[y0:y0 + h_, xa:xb]
        al = alfa[:, xa - x0:xb - x0] * ease
        sub[:] = sub * (1 - al) + rgb[:, xa - x0:xb - x0] * al
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def cuadro_marcador(texto, caja=(W, H)):
    im = Image.new("RGB", caja, (0, 0, 0))
    d = ImageDraw.Draw(im)
    f = cargar_fuente(26)
    bb = d.textbbox((0, 0), texto, font=f)
    d.text(((caja[0] - (bb[2] - bb[0])) / 2, (caja[1] - (bb[3] - bb[1])) / 2), texto, font=f, fill=(110, 110, 110))
    return im


# ------------------------------------------------------------------ render de segmentos

ENC_TMP = ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "8", "-pix_fmt", "yuv420p"] + COLOR_709


def enc_inter(args):
    return ["-c:v", "libx264", "-preset", args.preset_inter, "-crf", "12", "-pix_fmt", "yuv420p",
            "-g", "60", "-an"] + COLOR_709


HILOS = 4  # PIL suelta el GIL al remuestrear: 4 hilos rinden ~3x en el i5 de 2 nucleos


def tubo_a_ffmpeg(cuadro, n, caja, salida, enc, log):
    """cuadro(i) -> PIL.Image; se calculan en paralelo por tandas y se envian en orden a ffmpeg."""
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{caja[0]}x{caja[1]}", "-r", str(FPS), "-i", "-", "-vf", A709 + ",format=yuv420p",
           "-frames:v", str(n)] + enc + [str(salida)]
    with open(log, "a", encoding="utf-8") as flog:
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=flog)
        try:
            with ThreadPoolExecutor(HILOS) as ex:
                tanda = HILOS * 2
                for i0 in range(0, n, tanda):
                    for b in ex.map(lambda i: cuadro(i).tobytes(), range(i0, min(n, i0 + tanda))):
                        pr.stdin.write(b)
            pr.stdin.close()
        except BrokenPipeError:
            pass
        if pr.wait() != 0:
            raise RuntimeError(f"ffmpeg (tubo) fallo para {salida}; ver {log}")


def video_con_movimiento(pz, a, b, caja, salida, ss, filtro, dur_in, log):
    """Video con acercamiento ('vmov', mismo lenguaje que las fijas: 'acercamiento 100->140 % hacia arriba izquierda'):
    se decodifica en orden y cada cuadro se recorta con la caja interpolada (subpixel, sin temblor), con vecino mas
    cercano si es pixel-art. Si el video se acaba antes, se repite su ultimo cuadro."""
    info = sonda(pz["ruta"])
    w0, h0 = info["w"], info["h"]
    n = fr(b) - fr(a)
    mv = parse_mov(pz["vmov"], b - a)
    filtro_px = Image.Resampling.NEAREST if pz.get("pixel") else Image.Resampling.BICUBIC
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-nostdin", "-ss", f"{ss:.4f}", "-t", f"{dur_in:.4f}", "-i",
                            str(pz["ruta"]), "-vf", filtro + ",format=rgb24", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{caja[0]}x{caja[1]}", "-r", str(FPS), "-i", "-", "-vf", A709 + ",format=yuv420p",
           "-frames:v", str(n)] + ENC_TMP + [str(salida)]
    tam = w0 * h0 * 3
    ultimo = None
    with open(log, "a", encoding="utf-8") as flog:
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=flog)
        for i in range(n):
            buf = dec.stdout.read(tam)
            if buf and len(buf) == tam:
                ultimo = Image.frombuffer("RGB", (w0, h0), buf, "raw", "RGB", 0, 1)
            if ultimo is None:
                ultimo = Image.new("RGB", (w0, h0), (0, 0, 0))
            out = cuadro_imagen(ultimo, mv, a + i / FPS, a, b, caja, [], filtro_px)
            enc.stdin.write(out.tobytes())
        enc.stdin.close()
        dec.stdout.close()
        dec.wait()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg (video con movimiento) fallo para {salida}; ver {log}")


def cadena_escala(pieza, caja, info):
    """filtro para llevar un video a 'caja' sin deformar"""
    bw, bh = caja
    flags = "neighbor" if pieza.get("pixel") else "lanczos"
    pre = ""
    rinf = int(pieza.get("recorte_inf", 0) or 0)
    if rinf and info["h"]:
        pre = f"crop=iw:ih-{round(rinf * info['h'] / 1080)}:0:0,"
    if pieza.get("recorte") == "4:3":
        iw = round(H * 4 / 3)
        return (pre + f"scale={iw}:{H}:force_original_aspect_ratio=decrease:flags={flags}:out_color_matrix=bt709:out_range=tv,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black")
    return (pre + f"scale={bw}:{bh}:force_original_aspect_ratio=increase:flags={flags}:out_color_matrix=bt709:out_range=tv,"
            f"crop={bw}:{bh}")


class Grafo:
    def __init__(self, tmp, tag, log):
        self.ins = []
        self.chains = []
        self.tmp = tmp
        self.tag = tag
        self.log = log
        self.k = 0

    def etiqueta(self):
        self.k += 1
        return f"q{self.k}"

    def capa_alfa(self, ruta, n):
        """video con alfa (qtrle argb) como capa yuva420p de n cuadros"""
        idx = len(self.ins)
        self.ins.append(["-i", str(ruta)])
        lab = self.etiqueta()
        self.chains.append(f"[{idx}:v]setpts=PTS-STARTPTS,fps={FPS},format=rgba,scale=out_color_matrix=bt709:out_range=tv,"
                           f"format=yuva420p,trim=end_frame={n}[{lab}]")
        return lab

    def pieza(self, pz, a, b, caja=(W, H), mitad=None):
        """agrega la pieza en el tramo absoluto [a,b]; devuelve (etiqueta, cuadros). Con 'superponer', pone encima
        un video con alfa desde el inicio de la pieza (el ocular de S18)."""
        lab, n = self._pieza(pz, a, b, caja, mitad)
        if pz.get("superponer"):
            capa = self.capa_alfa(pz["superponer"], n)
            l2 = self.etiqueta()
            self.chains.append(f"[{lab}][{capa}]overlay=0:0:eof_action=pass,format=yuv420p,trim=end_frame={n}[{l2}]")
            lab = l2
        return lab, n

    def _pieza(self, pz, a, b, caja=(W, H), mitad=None):
        n = fr(b) - fr(a)
        lab = self.etiqueta()
        cola = f"tpad=stop_mode=clone:stop_duration=600,trim=end_frame={n},settb=1/{FPS},setpts=N/{FPS}/TB,setsar=1"
        if pz.get("fondo_previo"):
            # la toma anterior sigue debajo y el grafico con alfa (iris que se cierra, titulo, negro) va encima
            fondo = {k: v for k, v in pz["fondo_previo"].items() if k != "superponer"}
            lf, _ = self._pieza(fondo, a, b, caja, mitad)
            capa = self.capa_alfa(pz["ruta"], n)
            self.chains.append(f"[{lf}][{capa}]overlay=0:0:eof_action=pass,format=yuv420p,{cola}[{lab}]")
            return lab, n
        if pz["tipo"] == "partida":
            l1, _ = self.pieza(pz["partes"][0], a, b, (W // 2, H), "izq")
            l2, _ = self.pieza(pz["partes"][1], a, b, (W // 2, H), "der")
            self.chains.append(f"[{l1}][{l2}]hstack=inputs=2,setsar=1[{lab}]")
            return lab, n
        if pz["tipo"] == "video":
            info = sonda(pz["ruta"])
            vel = float(pz.get("velocidad", 1.0) or 1.0)
            ss = pz.get("desde", 0.0) + (a - pz["t0"]) * vel
            ss = max(0.0, min(ss, max(0.0, info["dur"] - 0.2)))
            pts = "setpts=PTS-STARTPTS" if vel == 1.0 else f"setpts=(PTS-STARTPTS)/{vel:.4f}"
            eq = f",eq={pz['eq']}" if pz.get("eq") else ""
            if pz.get("vmov"):
                # acercamiento sobre el video: cada cuadro se recorta con precision de subpixel en Python (como las fijas)
                mp4 = self.tmp / f"{self.tag}_{lab}_vmov.mp4"
                video_con_movimiento(pz, a, b, caja, mp4, ss, pts + f",fps={FPS}{eq}", (b - a) * vel + 1.0, self.log)
                idx = len(self.ins)
                self.ins.append(["-i", str(mp4)])
                self.chains.append(f"[{idx}:v]setpts=PTS-STARTPTS,format=yuv420p,{cola}[{lab}]")
                return lab, n
            idx = len(self.ins)
            self.ins.append(["-ss", f"{ss:.4f}", "-t", f"{(b - a) * vel + 1.0:.4f}", "-i", str(pz["ruta"])])
            inv = ",reverse" if pz.get("invertir") else ""
            alfa = ",format=rgba,premultiply=inplace=1" if info.get("alfa") else ""  # transparente -> sobre negro
            self.chains.append(f"[{idx}:v]{pts},fps={FPS}{eq}{inv}{alfa},{cadena_escala(pz, caja, info)},"
                               f"format=yuv420p,{cola}[{lab}]")
            return self.efectos(lab, n, parse_mov(pz.get("mov_original", ""), 1)["efectos"], pz, a), n
        # imagen o marcador
        mv = parse_mov(pz.get("mov", "fijo"), pz["t1"] - pz["t0"]) if pz["tipo"] == "imagen" else parse_mov("fijo", 1)
        if pz["tipo"] == "marcador" or (mv["estatico"] and not pz.get("capas")):
            png = self.tmp / f"{self.tag}_{lab}.png"
            marco_pieza(pz, a, caja, mv, mitad).save(png)
            idx = len(self.ins)
            self.ins.append(["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS + 0.5:.4f}", "-i", str(png)])
            self.chains.append(f"[{idx}:v]{A709},format=yuv420p,{cola}[{lab}]")
            return self.efectos(lab, n, mv["efectos"], pz, a), n
        mp4 = self.tmp / f"{self.tag}_{lab}.mp4"
        marco_pieza(pz, a, caja, mv, mitad)  # llena la cache de la imagen antes de los hilos
        tubo_a_ffmpeg(lambda i: marco_pieza(pz, a + i / FPS, caja, mv, mitad), n, caja, mp4, ENC_TMP, self.log)
        idx = len(self.ins)
        self.ins.append(["-i", str(mp4)])
        self.chains.append(f"[{idx}:v]setpts=PTS-STARTPTS,format=yuv420p,{cola}[{lab}]")
        return self.efectos(lab, n, mv["efectos"], pz, a), n

    def capa_png(self, nombre, crear):
        p = self.tmp / nombre
        if not p.exists():
            crear().save(p)
        return p

    def entrada_png(self, p, n):
        idx = len(self.ins)
        self.ins.append(["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS + 0.5:.4f}", "-i", str(p)])
        lab = self.etiqueta()
        self.chains.append(f"[{idx}:v]format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[{lab}]")
        return lab

    def efectos(self, lab, n, efectos, pz, a):
        """efectos de imagen con filtros de ffmpeg (rapidos): 'tv' = grano + lineas + vineta + barrido; 'franja' ambar"""
        if "tv" in efectos:
            def crear_tv():
                lin, vin = GRAFICOS / "lineas_tv.png", GRAFICOS / "vineta.png"
                if lin.exists() and vin.exists():
                    im = Image.open(vin).convert("RGBA").resize((W, H))
                    im.alpha_composite(Image.open(lin).convert("RGBA").resize((W, H)))
                    return im
                m = mascara_tv(H, W)[:, :, 0] / 0.92
                a_ = ((1 - m) * 255).clip(0, 255).astype(np.uint8)
                return Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), a_]), "RGBA")

            def crear_barrido():
                ys = np.linspace(-1, 1, 200, dtype=np.float32)
                al = (np.exp(-(ys / 0.45) ** 2) * 34).astype(np.uint8)
                a_ = np.repeat(al[:, None], W, axis=1)
                return Image.fromarray(np.dstack([np.full((200, W, 3), 255, np.uint8), a_]), "RGBA")
            c1 = self.entrada_png(self.capa_png("tv_capa.png", crear_tv), n)
            c2 = self.entrada_png(self.capa_png("tv_barrido.png", crear_barrido), n)
            l1, l2 = self.etiqueta(), self.etiqueta()
            self.chains.append(f"[{lab}]noise=alls=9:allf=t+u[{l1}]")
            self.chains.append(f"[{l1}][{c1}]overlay=0:0:eof_action=pass,format=yuv420p[{l2}]")
            l3 = self.etiqueta()
            self.chains.append(f"[{l2}][{c2}]overlay=x=0:y='mod(t*0.45,1)*H*1.3-H*0.15-h/2':eval=frame:eof_action=pass,"
                               f"format=yuv420p,trim=end_frame={n}[{l3}]")
            lab = l3
        if "franja" in efectos:
            def crear_franja():
                hh = 300
                ys = np.linspace(-1, 1, hh, dtype=np.float32)
                al = (np.exp(-(ys / 0.42) ** 2) * 60).astype(np.uint8)
                a_ = np.repeat(al[:, None], W, axis=1)
                rgb = np.zeros((hh, W, 3), np.uint8)
                rgb[:] = AMBAR
                return Image.fromarray(np.dstack([rgb, a_]), "RGBA")
            c = self.entrada_png(self.capa_png("franja_ambar.png", crear_franja), n)
            l1 = self.etiqueta()
            d = max(0.1, pz["t1"] - pz["t0"])
            self.chains.append(f"[{lab}][{c}]overlay=x=0:y='H*1.15-1.3*H*clip(({a - pz['t0']:.4f}+t)/{d:.4f},0,1)-h/2'"
                               f":eval=frame:eof_action=pass,format=yuv420p,trim=end_frame={n}[{l1}]")
            lab = l1
        return lab

    def unir(self, l1, n1, l2, n2, trans):
        tipo, d = trans
        lab = self.etiqueta()
        if tipo == "corte" or d <= 0:
            self.chains.append(f"[{l1}][{l2}]concat=n=2:v=1:a=0[{lab}]")
            return lab, n1 + n2
        nd = fr(d)
        off = (n1 - nd) / FPS
        self.chains.append(f"[{l1}][{l2}]xfade=transition={tipo}:duration={nd / FPS:.4f}:offset={off:.4f}[{lab}]")
        return lab, n1 + n2 - nd


def render_segmento(plan, previo, salida, args, tmp, log):
    piezas = plan["piezas"]
    a, b = plan["inicio"], plan["fin"]
    # via rapida: una sola imagen con movimiento, sin transiciones -> tubo directo al intermedio
    if (len(piezas) == 1 and piezas[0]["tipo"] == "imagen" and not plan["entrada"] and not plan["negro"]):
        mv = parse_mov(piezas[0].get("mov", "fijo"), piezas[0]["t1"] - piezas[0]["t0"])
        if (not mv["estatico"] or piezas[0].get("capas")) and not mv["efectos"]:
            marco_pieza(piezas[0], a, (W, H), mv)
            tubo_a_ffmpeg(lambda i: marco_pieza(piezas[0], a + i / FPS, (W, H), mv), plan["n"], (W, H), salida,
                          enc_inter(args), log)
            return
    g = Grafo(tmp, plan["id"], log)
    acc = None
    if plan["entrada"] and previo is not None:
        tipo, d = plan["entrada"]
        lp, np_ = g.pieza(previo["piezas"][-1], a, a + d)
        acc = (lp, np_)
    bordes = [p["t1"] for p in piezas[:-1]]
    for k, pz in enumerate(piezas):
        t0 = a if k == 0 else bordes[k - 1]
        t1 = b if k == len(piezas) - 1 else bordes[k]
        if k < len(piezas) - 1:
            t1 += plan["trans_int"][k][1]
        lab, n = g.pieza(pz, t0, t1)
        if acc is None:
            acc = (lab, n)
        else:
            trans = plan["entrada"] if (k == 0) else plan["trans_int"][k - 1]
            acc = g.unir(acc[0], acc[1], lab, n, trans)
    final = acc[0]
    if plan["negro"] > 0:
        lab = g.etiqueta()
        g.chains.append(f"[{final}]fade=t=in:st=0:d={plan['negro']:.3f}[{lab}]")
        final = lab
    grafo = tmp / f"{plan['id']}_grafo.txt"
    grafo.write_text(";\n".join(g.chains), encoding="utf-8")
    args_ff = []
    for i in g.ins:
        args_ff += i
    ff(args_ff + ["-/filter_complex", grafo, "-map", f"[{final}]", "-frames:v", plan["n"], "-r", FPS]
       + enc_inter(args) + [salida])


def huella_plan(plan, previo):
    def hp(p):
        d = {k: v for k, v in p.items() if k not in ("ruta", "partes")}
        if "ruta" in p:
            d["ruta"] = huella_archivo(p["ruta"])
        if "partes" in p:
            d["partes"] = [hp(x) for x in p["partes"]]
        if "capas" in p:
            d["capas"] = [huella_archivo(c) for c in p["capas"]]
        return d
    datos = {"v": VERSION, "id": plan["id"], "a": plan["inicio"], "b": plan["fin"], "piezas": [hp(p) for p in plan["piezas"]],
             "ti": plan["trans_int"], "e": plan["entrada"], "negro": plan["negro"]}
    if plan["entrada"] and previo is not None:
        datos["previa"] = hp(previo["piezas"][-1])
    return hashlib.sha1(json.dumps(datos, sort_keys=True, default=str).encode("utf-8")).hexdigest()


# ------------------------------------------------------------------ rotulos y sello

def rotulos_manifiesto():
    """graficos/rotulos/rotulos.json (del agente de graficos): segmento -> archivo"""
    p = GRAFICOS / "rotulos" / "rotulos.json"
    if not p.exists():
        return {}
    try:
        return {r["segmento"]: r for r in json.loads(p.read_text(encoding="utf-8"))}
    except Exception:
        return {}


def buscar_rotulo_png(seg, rot):
    if not GRAFICOS.exists():
        return None
    man = rotulos_manifiesto().get(seg["id"])
    if man and man.get("archivo"):
        arch = man["archivo"].strip()
        m = re.match(r"^(G\d+)\s*\((\w+)\)", arch)
        if m:  # "G01 (titulo)": la capa con transparencia de ese grafico
            for q in sorted(GRAFICOS.glob(f"{m.group(1)}_*{m.group(2)}*.png"), key=lambda x: len(x.name)):
                if es_capa_alfa(q):
                    return q
        else:
            for q in (GRAFICOS / arch, GRAFICOS / "rotulos" / arch):
                if q.exists():
                    return q
    for k in ("png", "archivo", "grafico"):
        if isinstance(rot, dict) and rot.get(k):
            p, _, _ = buscar_ruta(rot[k])
            if p is None:
                p = GRAFICOS / rot[k]
            if p.exists():
                return p
    sid = seg["id"].lower()
    slug = re.sub(r"[^a-z0-9]+", "_", norm(rot.get("texto", ""))).strip("_")
    for p in sorted(GRAFICOS.rglob("*.png")):
        s = norm(p.stem)
        padre = norm(p.parent.name)
        if s in (f"rotulo_{sid}", f"{sid}_rotulo", f"r_{sid}") or s.startswith(f"rotulo_{sid}_") \
                or (padre.startswith("rotulo") and (s == sid or s.startswith(sid + "_"))):
            return p
        if slug and len(slug) >= 4 and s.startswith("rotulo") and slug[:24] in s:
            return p
    return None


def recortar_alfa(p, destino):
    im = Image.open(p).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if bb is None:
        return None
    if im.size != (W, H):
        # rotulo suelto: abajo a la izquierda
        im.save(destino)
        return destino, 96, H - 96 - im.size[1]
    im.crop(bb).save(destino)
    return destino, bb[0], bb[1]


def dibujar_rotulo(texto, destino):
    f = cargar_fuente(40)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bb = tmp.textbbox((0, 0), texto, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    px, py, barra = 30, 18, 5
    w, h = tw + 2 * px + barra, th + 2 * py
    sombra = 18
    im = Image.new("RGBA", (w + 2 * sombra, h + 2 * sombra), (0, 0, 0, 0))
    som = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(som).rounded_rectangle((sombra, sombra + 4, sombra + w, sombra + h + 4), 8, fill=(0, 0, 0, 110))
    im = Image.alpha_composite(im, som.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((sombra, sombra, sombra + w, sombra + h), 8, fill=(12, 14, 24, 150))
    d.rectangle((sombra, sombra + 10, sombra + barra - 1, sombra + h - 10), fill=AMBAR + (255,))
    d.text((sombra + barra + px - bb[0], sombra + py - bb[1]), texto, font=f, fill=CREMA + (255,))
    im.save(destino)
    return destino, 96 - sombra, H - 110 - h - sombra


def dibujar_sello(texto, destino):
    sel = sorted(GRAFICOS.rglob("sello*.png")) if GRAFICOS.exists() else []
    if " ia" in norm(texto) or norm(texto).endswith("ia"):
        sel = [s for s in sel if re.search(r"(^|_)ia($|_)", norm(s.stem))]
    if sel:
        r = recortar_alfa(sel[0], destino)
        if r:
            return r
    f = cargar_fuente(22)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bb = tmp.textbbox((0, 0), texto, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    m = 8
    im = Image.new("RGBA", (tw + 2 * m, th + 2 * m), (0, 0, 0, 0))
    som = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(som).text((m - bb[0] + 1, m - bb[1] + 2), texto, font=f, fill=(0, 0, 0, 200))
    im = Image.alpha_composite(im, som.filter(ImageFilter.GaussianBlur(2)))
    ImageDraw.Draw(im).text((m - bb[0], m - bb[1]), texto, font=f, fill=(243, 237, 228, 255))
    a = np.asarray(im).copy()
    a[:, :, 3] = (a[:, :, 3].astype(np.float32) * 0.7).astype(np.uint8)
    Image.fromarray(a).save(destino)
    return destino, W - 40 - im.size[0], H - 34 - im.size[1]


def rotulo_en_grafico(pl):
    """True si el rotulo del segmento es el titulo de un grafico ('G01 (titulo)') y el fondo usado es la animacion
    de ese grafico, que ya trae el titulo dibujado (G01_apertura.mp4, G01_cierre.mov): no se superpone dos veces."""
    man = rotulos_manifiesto().get(pl["id"])
    m = re.match(r"^(G\d+)\s*\(", (man or {}).get("archivo", ""))
    if not m:
        return False
    return any(p.get("grafico") == m.group(1) and p["tipo"] == "video" for p in pl["piezas"])


def lista_rotulos(planes, avisos):
    rots = []
    for pl in planes:
        r = pl["seg"].get("rotulo")
        if isinstance(r, dict) and r.get("texto") and rotulo_en_grafico(pl):
            avisos.append(f"{pl['id']}: el rotulo «{r['texto']}» ya va dentro del grafico animado; no se superpone")
            continue
        if isinstance(r, dict) and r.get("texto"):
            rots.append({"seg": pl["seg"], "texto": r["texto"], "a": float(r.get("inicio", pl["inicio"])),
                         "b": float(r.get("fin", pl["fin"])), "rot": r})
    rots.sort(key=lambda x: x["a"])
    for i in range(1, len(rots)):
        if rots[i]["a"] < rots[i - 1]["b"] - 1e-6:
            avisos.append(f"rotulos solapados: {rots[i - 1]['seg']['id']} hasta {rots[i - 1]['b']} y {rots[i]['seg']['id']} "
                          f"desde {rots[i]['a']}: se acorta el primero")
            rots[i - 1]["b"] = rots[i]["a"]
    return [r for r in rots if r["b"] - r["a"] > 0.1]


def tramos_sello(planes):
    tramos = []
    for pl in planes:
        s = pl.get("sello")
        if s:
            if tramos and tramos[-1][2] == s and abs(tramos[-1][1] - pl["inicio"]) < 1e-6:
                tramos[-1][1] = pl["fin"]
            else:
                tramos.append([pl["inicio"], pl["fin"], s])
    return tramos


# ------------------------------------------------------------------ audio

def buscar_musica(montaje, forzada=None):
    """Prefiere la version automatizada (ya trae la bajada bajo la voz) si existe junto a la pista de montaje.json."""
    if forzada:
        p = RAIZ / forzada
        return p if p.exists() else None
    pista = (montaje.get("musica") or {}).get("pista", "")
    p, _, _ = buscar_ruta(re.sub(r"\s*\(.*\)\s*$", "", pista)) if pista else (None, "", "")
    if p is None:
        m = re.match(r"^(.*?\.\w+)", pista or "")
        if m:
            q = RAIZ / m.group(1)
            p = q if q.exists() else None
    if p is not None and sonda(p)["ok"]:
        return p
    if AUDIO.exists():
        cand = [x for x in AUDIO.rglob("*") if x.suffix.lower() in EXT_AUDIO
                and any(norm(x.stem).startswith(k) for k in ("musica", "music", "tema", "banda"))]
        cand.sort(key=lambda x: (x.suffix.lower() != ".wav", -x.stat().st_mtime))
        for x in cand:
            if sonda(x)["ok"]:
                return x
    return None


PALABRAS_VACIAS = {"de", "y", "en", "el", "la", "bajo", "baja", "suave", "x2", "cada", "entrada", "a", "del"}
SINONIMOS = {"televisor": ["tv"], "agua": ["orilla"], "riser": ["subida"], "pajaros": ["aves", "ambiente_sendero"]}


def buscar_efecto(nombre):
    clave = [w for w in re.findall(r"[a-z_]+", norm(nombre)) if w not in PALABRAS_VACIAS]
    if not clave:
        return None
    mejor, puntos = None, 0
    for carpeta in CARPETAS_EFECTOS:
        if not carpeta.exists():
            continue
        for x in carpeta.rglob("*"):
            if x.suffix.lower() not in EXT_AUDIO or norm(x.stem).startswith(("musica", "music", "efectos_")):
                continue
            s = norm(x.stem)
            # todas las palabras (o un sinonimo): «golpe grave» no es golpe_mastil
            if not all(w in s or any(o in s for o in SINONIMOS.get(w, [])) for w in clave):
                continue
            pt = len(clave) + (0.5 if carpeta == AUDIO else 0) - 0.01 * len(s)
            if pt > puntos:
                mejor, puntos = x, pt
    return mejor


def lista_efectos(planes, montaje, faltan_audio):
    ventanas = montaje.get("ventanas_expositor", [])
    mez = montaje.get("mezcla", {})
    bajo_voz = EFECTOS_VOZ_DB if EFECTOS_VOZ_DB is not None else float(mez.get("efectos_bajo_voz_dB", -12))

    def en_voz(t):
        return any(v["inicio"] - 0.05 <= t < v["fin"] for v in ventanas)

    efs = []
    # premezcla de efectos del gancho (audio/efectos_gancho.wav, de herramientas/demo/audio_procesar.py):
    # si existe, sustituye a los efectos sueltos de los segmentos del gancho
    fin_gancho = 0.0
    for v in montaje.get("ventanas_sin_voz", []):
        if "gancho" in norm(v.get("tramo", "")):
            fin_gancho = float(v["fin"])
    premezcla = AUDIO / "efectos_gancho.wav"
    if fin_gancho > 0 and premezcla.exists() and sonda(premezcla)["ok"]:
        efs.append({"ruta": premezcla, "t": 0.0, "dur": fin_gancho + 0.5, "ss": 0.0, "g": 0.0})
    else:
        fin_gancho = 0.0
    for pl in planes:
        son = pl["seg"].get("sonido") or {}
        a, b = pl["inicio"], pl["fin"]
        if b <= fin_gancho + 1e-6:
            continue
        for e in son.get("efectos") or []:
            en = norm(e)
            if "sonido propio" in en:
                for pz in pl["piezas"]:
                    if pz["tipo"] == "video" and sonda(pz["ruta"])["audio"]:
                        efs.append({"ruta": pz["ruta"], "t": pz["t0"], "dur": pz["t1"] - pz["t0"],
                                    "ss": pz.get("desde", 0.0) + max(0.0, a - pz["t0"]),
                                    "g": bajo_voz if en_voz(pz["t0"]) else PROPIO_DB})
                continue
            veces, paso = 1, 0.7
            m = re.search(r"x\s*(\d+)", en)
            if m:
                veces = int(m.group(1))
            if "en cada entrada" in en:
                veces, paso = 3, 1.5
            t = a
            mt = re.search(r"\ben\s+(\d+(?:[.,]\d+)?)", en)
            if mt:
                t = num(mt.group(1))
            ruta_txt_ = re.match(r"^([\w./ -]+\.(?:ogg|wav|mp3|flac|m4a))", e.strip())
            p = None
            if ruta_txt_:
                for base in (RAIZ, RAIZ / "Nasa_Game"):
                    q = base / ruta_txt_.group(1)
                    if q.exists():
                        p = q
                        break
                if p is None:
                    p = buscar_efecto(Path(ruta_txt_.group(1)).stem)
            else:
                p = buscar_efecto(re.sub(r"\ben\s+\d.*$", "", e))
            if p is None:
                faltan_audio.append(f"{pl['id']} efecto «{e}»")
                continue
            for k in range(veces):
                tk = t + k * paso
                if tk >= b:
                    break
                corte = b - tk
                efs.append({"ruta": p, "t": tk, "dur": corte, "ss": 0.0, "g": bajo_voz if en_voz(tk) else 0.0})
    return efs


def envolvente_musica(musica, montaje, args, dur_total, destino, informe):
    """Automatiza la musica por tramos del guion y escribe destino (wav f32, 48 kHz, estereo).

    Cada tramo tiene un nivel objetivo respecto del nivel pleno del tema (REF = RMS medio de 55-125 s, donde suena
    entero) y se le da una ganancia constante = objetivo - RMS medio del tramo, con limites; asi la cama bajo la voz
    queda ~15 dB por debajo del pleno aunque el tema crezca o decaiga solo. Entre tramos, rampas de 0,5 s: las
    bajadas terminan justo cuando empieza a hablar el expositor y las subidas empiezan al callar.
      gancho  0-11 silencio (la premezcla de efectos manda), 11-17 notas del titulo a pleno
      voz     ventanas_expositor: REF - bajada (15 dB por defecto)
      respiros REF - 6; montaje de minijuegos REF; cierre REF (hasta +6 dB, el tema decae solo) y fundido 148,5-149,5
    """
    sr = 48000
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(musica), "-t", f"{dur_total}", "-f", "f32le", "-ac", "2",
                        "-ar", str(sr), "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
    n = int(round(dur_total * sr))
    if len(a) < n:
        a = np.vstack([a, np.zeros((n - len(a), 2), np.float32)])
    a = a[:n]
    pot = (a.astype(np.float64) ** 2).mean(axis=1)

    def rms_db(t0, t1):
        s = pot[int(t0 * sr):int(t1 * sr)]
        return 10 * math.log10(s.mean() + 1e-12) if len(s) else -90.0

    ref = rms_db(55.0, 125.0)
    D = args.bajada_db
    rampa = args.rampa
    voz = sorted((float(v["inicio"]), float(v["fin"])) for v in montaje.get("ventanas_expositor", []))
    marcas = (montaje.get("musica") or {}).get("marcas", {})
    t_nota = float(marcas.get("primera_nota", 11.0))
    tramos = []  # (a, b, objetivo dB respecto de REF, gmin, gmax, nombre)
    for v in montaje.get("ventanas_sin_voz", []):
        a0, b0, nombre = float(v["inicio"]), float(v["fin"]), norm(v.get("tramo", ""))
        if "gancho" in nombre:
            tramos.append((a0, t_nota, None, 0, 0, "gancho: silencio"))
            tramos.append((t_nota, b0, 0.0, -6, 4, "gancho: titulo"))
        elif "respiro" in nombre:
            tramos.append((a0, b0, -6.0, -8, 6, nombre))
        elif "cierre" in nombre:
            tramos.append((a0, b0, 0.0, 0, 6, nombre))
        else:
            tramos.append((a0, b0, 0.0, -3, 3, nombre))
    unidas = []
    for a0, b0 in voz:  # ventanas contiguas = un solo tramo (sin cambios de nivel a mitad de frase)
        if unidas and a0 <= unidas[-1][1] + 1e-6:
            unidas[-1][1] = max(unidas[-1][1], b0)
        else:
            unidas.append([a0, b0])
    for a0, b0 in unidas:
        tramos.append((a0, b0, -D, -22, 0, "voz"))
    tramos.sort()
    gan = []
    for a0, b0, obj, gmin, gmax, nombre in tramos:
        if obj is None:
            g = -90.0
        else:
            g = min(gmax, max(gmin, ref + obj - rms_db(a0, b0)))
        gan.append(g)
    informe["musica_tramos"] = [f"{t[0]:6.2f}-{t[1]:6.2f} {t[5]:<28} {g:+6.1f} dB -> {rms_db(t[0], t[1]) + g:6.1f} dBFS"
                                for t, g in zip(tramos, gan)]
    # curva de control cada 1 ms, en dB, con rampas
    paso = 0.001
    ts = np.arange(0, dur_total + paso, paso)
    curva = np.empty_like(ts)
    for (a0, b0, *_), g in zip(tramos, gan):
        curva[(ts >= a0 - 1e-9) & (ts < b0)] = g
    curva[ts >= tramos[-1][1]] = gan[-1]
    puntos = []
    crescendo = marcas.get("crescendo")
    for k in range(1, len(tramos)):
        B, g1, g2 = tramos[k][0], gan[k - 1], gan[k]
        if abs(g2 - g1) < 0.05:
            continue
        if crescendo is not None and "cierre" in tramos[k][5] and g2 > g1 and float(crescendo) < B:
            # v2: crescendo de verdad bajo la ultima frase del expositor (unos +3 dB/s) hasta 5 dB bajo el pleno,
            # y el resto en 0,6 s al callar (antes subia de golpe en 0,5 s)
            c = float(crescendo)
            medio = g2 - 5.0
            puntos.append((c, B, g1, max(g1, medio)))
            puntos.append((B, B + 0.6, max(g1, medio), g2))
            informe["crescendo"] = f"{c:.1f}-{B:.1f} s: {g1:+.1f} -> {max(g1, medio):+.1f} dB; {B:.1f}-{B + 0.6:.1f} s: -> {g2:+.1f} dB"
            continue
        if g1 <= -60:          # desde silencio: entrada corta de 0,3 s
            r0, r1 = B, B + 0.3
        elif g2 < g1:          # baja: termina cuando empieza la voz
            r0, r1 = B - rampa, B
        else:                  # sube: empieza al callar
            r0, r1 = B, B + rampa
        puntos.append((r0, r1, g1, g2))
    for r0, r1, g1, g2 in puntos:
        sel = (ts >= r0) & (ts < r1)
        x = (ts[sel] - r0) / (r1 - r0)
        x = 0.5 - 0.5 * np.cos(np.pi * x)
        if g1 <= -60 or g2 <= -60:  # en amplitud cuando sale de / va a silencio
            l1, l2 = 10 ** (max(g1, -90) / 20), 10 ** (max(g2, -90) / 20)
            curva[sel] = 20 * np.log10(np.maximum(1e-5, l1 + (l2 - l1) * x))
        else:
            curva[sel] = g1 + (g2 - g1) * x
    # fundido final 148,5 -> 149,5 y silencio despues
    f0, f1 = dur_total - 1.5, dur_total - 0.5
    amp = 10 ** (curva / 20)
    sel = (ts >= f0) & (ts < f1)
    amp[sel] *= 0.5 + 0.5 * np.cos(np.pi * (ts[sel] - f0) / (f1 - f0))
    amp[ts >= f1] = 0.0
    amp[curva <= -89] = 0.0
    tm = np.arange(n) / sr
    g = np.interp(tm, ts, amp).astype(np.float32)
    a *= g[:, None]
    pr = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                         "-c:a", "pcm_f32le", str(destino)], input=a.tobytes(), capture_output=True)
    if pr.returncode != 0:
        raise RuntimeError("no se pudo escribir la musica automatizada: " + pr.stderr.decode("utf-8", "replace")[-500:])
    informe["musica_ref"] = f"pleno del tema {ref:.1f} dBFS RMS; bajo la voz {D:.0f} dB por debajo; rampas {rampa} s"
    return destino


def mezclar_audio(planes, montaje, args, dur_total, tmp, informe):
    musica = buscar_musica(montaje, args.musica)
    if args.bajada == "auto":
        bajar = musica is not None and "automatizada" not in norm(musica.stem)
    else:
        bajar = args.bajada == "si"
    informe["bajada"] = bajar
    if musica is not None and bajar:
        musica = envolvente_musica(musica, montaje, args, dur_total, tmp / "musica_envolvente.wav", informe)
        bajar = False  # la bajada ya esta en el archivo
    faltan_audio = []
    efs = lista_efectos(planes, montaje, faltan_audio)
    informe["musica"] = rel(musica) if musica else None
    informe["efectos"] = [f"{e['t']:.2f}s {Path(e['ruta']).name} ({e['g']:+.0f} dB)" for e in efs]
    informe["faltan_audio"] = faltan_audio
    salida = tmp / "mezcla.wav"
    if musica is None and not efs:
        ff(["-f", "lavfi", "-t", f"{dur_total}", "-i", "anullsrc=r=48000:cl=stereo", "-c:a", "pcm_s16le", salida])
        informe["loudnorm"] = "sin audio: silencio"
        return salida
    huella = hashlib.sha1(json.dumps({"v": VERSION, "m": huella_archivo(musica) if musica else None, "bajar": bajar,
                                      "efs": [[huella_archivo(e["ruta"]), e["t"], e["dur"], e["ss"], e["g"]] for e in efs],
                                      "ventanas": montaje.get("ventanas_expositor"), "mezcla": montaje.get("mezcla"),
                                      "args": [args.bajada_db, args.rampa, args.lufs, args.pico], "d": dur_total,
                                      "norma": "plenos v2", "pleno": args.pleno, "marcas": (montaje.get("musica") or {}).get("marcas"),
                                      "sin_voz": montaje.get("ventanas_sin_voz"), "propio": PROPIO_DB},
                                     sort_keys=True, default=str).encode("utf-8")).hexdigest()
    cache_wav, cache_h = INTER / "mezcla.wav", INTER / "mezcla.huella"
    if cache_wav.exists() and cache_h.exists() and cache_h.read_text(encoding="utf-8").strip() == huella:
        informe["loudnorm_final"] = "de la cache (intermedios/mezcla.wav)"
        return cache_wav
    mez = montaje.get("mezcla", {})
    D = args.bajada_db if args.bajada_db is not None else abs(float(mez.get("musica_bajo_voz_dB", -15)))
    r = args.rampa if args.rampa is not None else float(mez.get("rampa_s", 0.5))
    ins, chains, labs = [], [], []
    if musica is not None:
        ws = []
        for v in (montaje.get("ventanas_expositor", []) if bajar else []):
            a0, b0 = float(v["inicio"]), float(v["fin"])
            ws.append(f"clip((t-{a0 - r:.3f})/{r:.3f},0,1)*clip(({b0 + r:.3f}-t)/{r:.3f},0,1)")
        expr = "0"
        for w in ws:
            expr = f"max({expr},{w})"
        ins += ["-i", str(musica)]
        chains.append(f"[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=0:{dur_total},"
                      f"asetnsamples=n=256,volume='pow(10,-{D:.2f}*({expr})/20)':eval=frame[mus]")
        labs.append("mus")
    n_in = 1 if musica is not None else 0
    for j, e in enumerate(efs):
        if e["ss"] > 0:
            ins += ["-ss", f"{e['ss']:.3f}"]
        ins += ["-i", str(e["ruta"])]
        n = n_in
        n_in += 1
        dur = max(0.05, e["dur"])
        fo = min(0.15, dur / 3)
        ms = int(round(e["t"] * 1000))
        lab = f"e{j}"
        chains.append(f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=0:{dur:.3f},"
                      f"afade=t=out:st={dur - fo:.3f}:d={fo:.3f},adelay={ms}:all=1,volume={e['g']:.1f}dB[{lab}]")
        labs.append(lab)
    chains.append("".join(f"[{l}]" for l in labs) + f"amix=inputs={len(labs)}:normalize=0:duration=longest,"
                  f"apad=whole_dur={dur_total},atrim=0:{dur_total}[mix]")
    grafo = tmp / "audio_grafo.txt"
    grafo.write_text(";\n".join(chains), encoding="utf-8")
    cruda = tmp / "mezcla_cruda.wav"
    ff(ins + ["-/filter_complex", grafo, "-map", "[mix]", "-c:a", "pcm_f32le", "-ar", "48000", cruda])
    # Normalizacion: ganancia fija + limitador, medida con el medidor de loudnorm (EBU R128, pico real).
    # No se usa loudnorm para procesar: si el pico no le deja ir en lineal pasa a modo dinamico, comprime el rango
    # (LRA 11) y la cama bajo la voz sube ~6 dB, justo lo que no se quiere bajo el expositor.
    I, TP = args.lufs, args.pico

    def medir(p):
        rr = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(p), "-af",
                             f"loudnorm=I={I}:TP={TP}:print_format=json", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", rr.stderr, re.S)
        d = json.loads(m.group(0)) if m else {}
        try:
            return float(d["input_i"]), float(d["input_tp"]), d.get("input_lra")
        except Exception:
            return None, None, None

    def medir_tramos(p, tramos_):
        """LUFS integrados de la union de unos tramos (EBU R128, con el medidor de loudnorm)"""
        if not tramos_:
            return None
        partes = ";".join(f"[0:a]atrim={a0:.3f}:{b0:.3f},asetpts=PTS-STARTPTS[p{k}]" for k, (a0, b0) in enumerate(tramos_))
        fc = (partes + ";" + "".join(f"[p{k}]" for k in range(len(tramos_)))
              + f"concat=n={len(tramos_)}:v=0:a=1,loudnorm=I={I}:TP={TP}:print_format=json[o]")
        rr = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(p), "-filter_complex", fc, "-map", "[o]",
                             "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", rr.stderr, re.S)
        try:
            return float(json.loads(m.group(0))["input_i"])
        except Exception:
            return None

    # tramos plenos (sin voz y con la musica arriba): notas del titulo, montaje de minijuegos y cierre
    marcas = (montaje.get("musica") or {}).get("marcas", {})
    plenos, voces = [], [(float(v["inicio"]), float(v["fin"])) for v in montaje.get("ventanas_expositor", [])]
    for v in montaje.get("ventanas_sin_voz", []):
        nombre, a0, b0 = norm(v.get("tramo", "")), float(v["inicio"]), float(v["fin"])
        if "gancho" in nombre:
            plenos.append((float(marcas.get("primera_nota", 11.0)), b0))
        elif "montaje" in nombre:
            plenos.append((a0 + 0.5, b0))
        elif "cierre" in nombre:
            plenos.append((a0 + 0.6, min(b0, dur_total - 1.5)))

    final_fade = max(0.0, dur_total - 1.5)
    i0, tp0, lra0 = medir(cruda)
    informe["loudnorm_medido"] = {"LUFS": i0, "dBTP": tp0, "LRA": lra0}
    if i0 is None or i0 < -70:
        ff(["-i", cruda, "-af", f"apad=whole_dur={dur_total},atrim=0:{dur_total}", "-c:a", "pcm_s16le", salida])
    else:
        # v2: la ganancia se fija para que los tramos PLENOS den args.pleno (-14 LUFS); bajo la voz la cama queda
        # ~12 LU por debajo. Antes se normalizaba el integrado a -16 y los plenos quedaban en -11,5.
        objetivo = args.pleno
        ip0 = medir_tramos(cruda, plenos) if objetivo is not None else None
        g = (objetivo - ip0) if ip0 is not None else (I - i0)
        techo = TP - 0.7  # el limitador trabaja con muestras; 0,7 dB de margen para el pico real (sobremuestreado)
        for _ in range(4):
            ff(["-i", cruda, "-af", f"volume={g:.3f}dB,alimiter=limit={10 ** (techo / 20):.4f}:attack=3:release=80:"
                f"level=false,aresample=48000,afade=t=out:st={final_fade:.3f}:d=1.0,"
                f"apad=whole_dur={dur_total},atrim=0:{dur_total}", "-c:a", "pcm_s16le", "-ar", "48000", salida])
            i1, tp1, lra1 = medir(salida)
            if i1 is None:
                break
            if tp1 > TP:
                techo -= (tp1 - TP) + 0.1
            if ip0 is not None:
                ip1 = medir_tramos(salida, plenos)
                err = objetivo - ip1
            else:
                err = I - i1
            if abs(err) <= 0.2 and tp1 <= TP:
                break
            g += err
        informe["loudnorm_final"] = {"LUFS": i1, "dBTP": tp1, "LRA": lra1, "ganancia_dB": round(g, 2),
                                     "techo_limitador_dB": round(techo, 2),
                                     "plenos_LUFS": medir_tramos(salida, plenos), "voz_LUFS": medir_tramos(salida, voces)}
    shutil.copyfile(salida, cache_wav)
    cache_h.write_text(huella, encoding="utf-8")
    return cache_wav


# ------------------------------------------------------------------ union final

def montar_final(planes, montaje, mezcla, salida, args, tmp, informe, avisos):
    dur_total = float(montaje["salida"].get("duracion_s", 150.0))
    n_total = fr(dur_total)
    lista = tmp / "lista.txt"
    lista.write_text("".join(f"file '{ruta_txt(INTER / (p['id'] + '.mp4'))}'\n" for p in planes), encoding="utf-8")
    ins = ["-f", "concat", "-safe", "0", "-i", str(lista), "-i", str(mezcla)]
    chains = [f"[0:v]settb=1/{FPS},setpts=N/{FPS}/TB,format=yuv420p[b0]"]
    base = "b0"
    nin = 2
    fdr = args.fundido_rotulo
    rots = lista_rotulos(planes, avisos)
    informe["rotulos"] = []
    for j, r in enumerate(rots):
        destino = tmp / f"rotulo_{j:02d}.png"
        if r["rot"].get("ajustado"):
            # texto cambiado en ajustes_montaje.json: misma plantilla que los demas (graficos.py --rotulo)
            png = tmp / f"rotulo_{j:02d}_ajustado.png"
            subprocess.run([sys.executable, "-I", str(Path(__file__).with_name("graficos.py")), "--rotulo", r["texto"],
                            str(png)], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if not png.exists():
                png = None
        else:
            png = buscar_rotulo_png(r["seg"], r["rot"])
        res = recortar_alfa(png, destino) if png else None
        origen = rel(png) if res else "dibujado"
        if res is None:
            res = dibujar_rotulo(r["texto"], destino)
        p, x0, y0 = res
        a, b = r["a"], r["b"]
        f = min(fdr, (b - a) / 3)
        # v2: rotulos encadenados (montaje de minijuegos): sin fundido en los cortes intermedios
        fi = 0.0 if r["rot"].get("sin_fundido_entrada") else f
        fo = 0.0 if r["rot"].get("sin_fundido_salida") else f
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{b - a + 0.1:.3f}", "-i", str(p)]
        lab = f"r{j}"
        fades = ""
        if fi > 0:
            fades += f"fade=t=in:st={a:.4f}:d={fi:.3f}:alpha=1,"
        if fo > 0:
            fades += f"fade=t=out:st={b - fo:.4f}:d={fo:.3f}:alpha=1,"
        chains.append(f"[{nin}:v]format=rgba,setpts=PTS-STARTPTS+{a:.4f}/TB,{fades}"
                      f"scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[{lab}]")
        xexpr = str(x0)
        if fi > 0:
            xexpr += f"-24*pow(max(0,1-(t-{a:.4f})/{fi:.3f}),2)"
        if fo > 0:
            xexpr += f"+12*pow(max(0,(t-{b - fo:.4f})/{fo:.3f}),2)"
        nb = f"b{j + 1}"
        chains.append(f"[{base}][{lab}]overlay=x='{xexpr}':y={y0}:eval=frame:eof_action=pass:"
                      f"enable='gte(t,{a:.4f})*lt(t,{b:.4f})'[{nb}]")
        base = nb
        nin += 1
        informe["rotulos"].append(f"{a:6.2f}-{b:6.2f} «{r['texto']}» ({origen})")
    tramos = tramos_sello(planes)
    if tramos:
        sp, sx, sy = dibujar_sello(tramos[0][2], tmp / "sello.png")
        for j, (a, b, _) in enumerate(tramos):
            ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{b - a + 0.1:.3f}", "-i", str(sp)]
            lab = f"s{j}"
            chains.append(f"[{nin}:v]format=rgba,setpts=PTS-STARTPTS+{a:.4f}/TB,"
                          f"scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[{lab}]")
            nb = f"c{j}"
            chains.append(f"[{base}][{lab}]overlay=x={sx}:y={sy}:eof_action=pass:enable='between(t,{a:.4f},{b:.4f})'[{nb}]")
            base = nb
            nin += 1
        informe["sello"] = [f"{a:.2f}-{b:.2f}" for a, b, _ in tramos]
    entrada = planes[0]["negro"] or 0.5
    fin_negro = dur_total - 0.5
    nota = norm(planes[-1]["seg"].get("nota", ""))
    m = re.search(r"fundido a negro en (\d+(?:[.,]\d+)?)", nota)
    if m:
        fin_negro = num(m.group(1))
    chains.append(f"[{base}]fade=t=in:st=0:d={entrada:.3f},fade=t=out:st={fin_negro:.3f}:d={dur_total - fin_negro:.3f},"
                  f"format=yuv420p[v]")
    grafo = tmp / "final_grafo.txt"
    grafo.write_text(";\n".join(chains), encoding="utf-8")
    ff(ins + ["-/filter_complex", grafo, "-map", "[v]", "-map", "1:a",
              "-c:v", "libx264", "-profile:v", "high", "-preset", args.preset_final, "-b:v", "12M", "-maxrate", "14M",
              "-bufsize", "24M", "-pix_fmt", "yuv420p", "-r", FPS, "-frames:v", n_total] + COLOR_709 +
       ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{dur_total}", "-movflags", "+faststart", salida])


def comprobar(salida, dur_total):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-show_entries",
                        "stream=codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,nb_read_packets,duration,bit_rate"
                        ":format=duration,bit_rate", "-of", "json", str(salida)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    d = json.loads(r.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    res = {"video": f"{v['codec_name']} {v.get('profile')} {v['width']}x{v['height']} {v['pix_fmt']} {v['r_frame_rate']}",
           "cuadros": int(v.get("nb_read_packets", 0)),"dur_video": float(v.get("duration", 0)),
           "dur_audio": float(a.get("duration", 0)) if a else None, "dur_formato": float(d["format"]["duration"]),
           "mbps_video": round(int(v.get("bit_rate", 0) or 0) / 1e6, 2),
           "audio": f"{a['codec_name']} {round(int(a.get('bit_rate', 0) or 0) / 1000)} kb/s" if a else None}
    res["ok"] = res["cuadros"] == fr(dur_total) and abs(res["dur_video"] - dur_total) < 0.02
    return res


# ------------------------------------------------------------------ hoja de contacto

def hoja_contacto(video, destino, cada=2.0):
    tmp = INTER / "_hoja"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    paso = fr(cada)
    ff(["-i", video, "-vf", f"select='not(mod(n\\,{paso}))',scale=320:180:flags=lanczos", "-fps_mode", "vfr",
        "-q:v", "3", tmp / "c_%04d.jpg"])
    cuadros = sorted(tmp.glob("c_*.jpg"))
    cols = 6
    tw, th, rot = 320, 180, 24
    filas = math.ceil(len(cuadros) / cols)
    hoja = Image.new("RGB", (cols * (tw + 6) + 6, filas * (th + rot + 6) + 6), (28, 28, 30))
    d = ImageDraw.Draw(hoja)
    f = cargar_fuente(18)
    for i, c in enumerate(cuadros):
        x = 6 + (i % cols) * (tw + 6)
        y = 6 + (i // cols) * (th + rot + 6)
        hoja.paste(Image.open(c), (x, y))
        t = i * cada
        d.text((x + 4, y + th + 2), f"{int(t // 60)}:{t % 60:04.1f}  ({t:.0f} s)", font=f, fill=(230, 220, 200))
    hoja.save(destino, quality=88)
    shutil.rmtree(tmp, ignore_errors=True)
    return len(cuadros)


# ------------------------------------------------------------------ principal

def expandir_ids(texto, ids):
    sel = set()
    for parte in re.split(r"[,\s]+", texto.strip()):
        if not parte:
            continue
        m = re.match(r"^S?(\d+)\s*-\s*S?(\d+)$", parte, re.I)
        if m:
            for n in range(int(m.group(1)), int(m.group(2)) + 1):
                sel.add(f"S{n:02d}")
        else:
            sel.add(parte.upper())
    desconocidos = sel - set(ids)
    if desconocidos:
        raise SystemExit(f"--solo: ids desconocidos {sorted(desconocidos)}")
    return sel


def main():
    ap = argparse.ArgumentParser(description="Monta el video demo desde montaje.json (ver la cabecera del script).")
    ap.add_argument("--salida", help="mp4 de salida (relativo a la raiz del repositorio)")
    ap.add_argument("--hoja", help="jpg de la hoja de contacto (un cuadro cada 2 s)")
    ap.add_argument("--solo-hoja", help="hace solo la hoja de este video (con --hoja)")
    ap.add_argument("--solo", help="ids a volver a renderizar, p. ej. S10,S23-S31")
    ap.add_argument("--forzar", action="store_true", help="rehace todos los intermedios")
    ap.add_argument("--revisar", action="store_true", help="solo muestra el plan")
    ap.add_argument("--rapido", action="store_true", help="presets rapidos para pruebas")
    ap.add_argument("--preset-final", default=None)
    ap.add_argument("--preset-inter", default=None)
    ap.add_argument("--musica", default=None, help="pista de musica (por defecto la de montaje.json; prefiere *_automatizada)")
    ap.add_argument("--bajada", choices=["auto", "si", "no"], default="auto",
                    help="bajar la musica bajo la voz; auto = solo si la pista no es la *_automatizada")
    ap.add_argument("--bajada-db", type=float, default=15.0, help="dB que baja la musica bajo la voz (encargo: 14 a 16)")
    ap.add_argument("--rampa", type=float, default=0.5, help="rampa de la bajada en s (encargo: medio segundo)")
    ap.add_argument("--efectos-voz-db", type=float, default=-20.0,
                    help="ganancia de los efectos dentro de las ventanas del expositor (montaje.json dice -12; a -12 "
                         "los grillos y pasos quedaban 6 dB por encima de la cama de musica)")
    ap.add_argument("--lufs", type=float, default=-16.0, help="objetivo integrado si no se usa --pleno")
    ap.add_argument("--pleno", type=float, default=-14.0,
                    help="LUFS de los tramos plenos (titulo, minijuegos, cierre); la cama bajo la voz queda ~12 LU por "
                         "debajo. Con --pleno nan se vuelve a normalizar el integrado a --lufs")
    ap.add_argument("--pico", type=float, default=-1.5)
    ap.add_argument("--fundido-rotulo", type=float, default=0.3)
    args = ap.parse_args()
    global EFECTOS_VOZ_DB
    EFECTOS_VOZ_DB = args.efectos_voz_db
    if args.pleno is not None and math.isnan(args.pleno):
        args.pleno = None
    args.preset_final = args.preset_final or ("ultrafast" if args.rapido else "veryfast")
    args.preset_inter = args.preset_inter or ("ultrafast" if args.rapido else "superfast")

    if args.solo_hoja:
        if not args.hoja:
            raise SystemExit("--solo-hoja necesita --hoja")
        n = hoja_contacto(RAIZ / args.solo_hoja, RAIZ / args.hoja)
        print(f"hoja: {args.hoja} ({n} cuadros)")
        return

    t_ini = time.time()
    montaje = json.loads(MONTAJE.read_text(encoding="utf-8"))
    dur_total = float(montaje["salida"].get("duracion_s", 150.0))
    planes, avisos = planificar(montaje)
    total = sum(p["n"] for p in planes)
    if total != fr(dur_total):
        avisos.append(f"suma de cuadros {total} != {fr(dur_total)}")

    print(f"montaje.json: {len(planes)} segmentos, {total} cuadros ({total / FPS:.2f} s)")
    for p in planes:
        marca = "  " if p["usado"] == "fuente" else ("~ " if p["usado"] == "alternativa" else "! ")
        print(f"{marca}{p['id']} {p['inicio']:7.2f}-{p['fin']:7.2f} ({p['n']:3d} c) {p['usado']:<11} "
              + " + ".join(describir_pieza(x) for x in p["piezas"])
              + (f"  <{p['entrada'][0]} {p['entrada'][1]}s>" if p["entrada"] else ""))
    for a in avisos:
        print("AVISO:", a)
    if args.revisar:
        return
    if not args.salida:
        raise SystemExit("falta --salida")

    INTER.mkdir(parents=True, exist_ok=True)
    leeme = INTER / "LEEME.txt"
    if not leeme.exists():
        leeme.write_text("Carpeta de cache de herramientas/demo/montar_demo.py: un video por segmento (Sxx.mp4) con su\n"
                         "huella (Sxx.huella) y archivos temporales en _tmp/. Se puede borrar entera en cualquier momento;\n"
                         "el siguiente montaje la vuelve a crear (tarda mas porque renderiza todo de nuevo).\n",
                         encoding="utf-8")
    tmp = INTER / "_tmp"
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True, exist_ok=True)
    log = tmp / "ffmpeg_tubo.log"
    ids = [p["id"] for p in planes]
    solo = expandir_ids(args.solo, ids) if args.solo else None

    t_seg = time.time()
    hechos, cache = [], []
    for i, pl in enumerate(planes):
        previo = planes[i - 1] if i > 0 else None
        h = huella_plan(pl, previo)
        mp4 = INTER / f"{pl['id']}.mp4"
        hf = INTER / f"{pl['id']}.huella"
        vigente = mp4.exists() and hf.exists() and hf.read_text(encoding="utf-8").strip() == h
        if solo is not None:
            rehacer = pl["id"] in solo or not mp4.exists()
        else:
            rehacer = args.forzar or not vigente
        if not rehacer:
            cache.append(pl["id"])
            continue
        t0 = time.time()
        render_segmento(pl, previo, mp4, args, tmp, log)
        hf.write_text(h, encoding="utf-8")
        n_real = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                     "stream=nb_read_packets", "-of", "csv=p=0", str(mp4)],
                                    capture_output=True, text=True).stdout.strip() or 0)
        estado = "ok" if n_real == pl["n"] else f"CUADROS {n_real} != {pl['n']}"
        print(f"  render {pl['id']}: {pl['n']} cuadros en {time.time() - t0:5.1f} s ({estado})", flush=True)
        if n_real != pl["n"]:
            raise SystemExit(f"{pl['id']}: el intermedio tiene {n_real} cuadros y debia tener {pl['n']}")
        hechos.append(pl["id"])
    t_seg = time.time() - t_seg
    print(f"intermedios: {len(hechos)} renderizados en {t_seg:.0f} s, {len(cache)} de la cache")

    informe = {}
    t_aud = time.time()
    mezcla = mezclar_audio(planes, montaje, args, dur_total, tmp, informe)
    t_aud = time.time() - t_aud
    print(f"audio: {t_aud:.0f} s; musica: {informe.get('musica') or 'NO HAY (silencio)'}; "
          f"{len(informe.get('efectos', []))} efectos; final {informe.get('loudnorm_final', informe.get('loudnorm'))}")

    salida = RAIZ / args.salida
    salida.parent.mkdir(parents=True, exist_ok=True)
    t_fin = time.time()
    montar_final(planes, montaje, mezcla, salida, args, tmp, informe, avisos)
    t_fin = time.time() - t_fin
    print(f"union, rotulos y codificacion final: {t_fin:.0f} s")
    for r in informe.get("rotulos", []):
        print("  rotulo", r)
    if informe.get("sello"):
        print("  sello IA:", ", ".join(informe["sello"]))

    c = comprobar(salida, dur_total)
    print(f"salida: {rel(salida)}  {c['video']}, {c['cuadros']} cuadros, video {c['dur_video']:.3f} s, "
          f"audio {c['dur_audio']} s, formato {c['dur_formato']:.3f} s, {c['mbps_video']} Mb/s, {c['audio']} -> "
          f"{'OK' if c['ok'] else 'FALLA'}")
    if args.hoja:
        n = hoja_contacto(salida, RAIZ / args.hoja)
        print(f"hoja: {args.hoja} ({n} cuadros)")

    falt = [(p["id"], p["usado"], p["faltan"]) for p in planes if p["usado"] != "fuente"]
    print(f"\nSEGMENTOS SIN SU MATERIAL ({len(falt)}):")
    for sid, usado, fl in falt:
        print(f"  {sid}: {usado}; falta {'; '.join(fl) if fl else '?'}")
    if informe.get("faltan_audio"):
        print(f"EFECTOS SIN ARCHIVO ({len(informe['faltan_audio'])}): " + "; ".join(informe["faltan_audio"]))
    notas = [(p["id"], p["seg"]["nota"]) for p in planes if p["seg"].get("nota")]
    if notas:
        print("NOTAS DE montaje.json PARA EL MONTADOR:")
        for sid, n in notas:
            print(f"  {sid}: {n}")
    for a in avisos:
        print("AVISO:", a)
    print(f"\nTIEMPO TOTAL: {time.time() - t_ini:.0f} s")
    shutil.rmtree(tmp, ignore_errors=True)
    if not c["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
