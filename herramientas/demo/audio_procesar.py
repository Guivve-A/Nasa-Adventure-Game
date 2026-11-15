"""Deja listo el audio del video demo en Nasa_Game/Presentacion/audio/ (wav 48 kHz, 24 bits).

1. Musica (originales/musica_demo.mp3, ElevenLabs Music v2.5, 153,05 s, 90 BPM medidos):
   - musica_demo.wav: se recorta 0,180 s al inicio para que los pulsos caigan en multiplos exactos de 2/3 s
     (asi los cortes del montaje de 1:10,00 a 1:22,00, cada 1,333 s = 2 pulsos, caen en el pulso); se corta a 150,0 s
     con fundido de salida de 148,5 a 149,5 y 0,5 s de silencio final.
   - musica_demo_automatizada.wav: la misma con la automatizacion de volumen de montaje.json (silencio hasta 11,0;
     pleno; cama a -20 dB bajo el expositor; -10 dB en el ocular; -8 dB en el despegue; crescendo de 123 a 126;
     compensacion de +2,5 a +5,5 dB en el cierre porque el tema decrece solo desde 125 s).
2. Efectos de Higgsfield (Mirelo): recorte de silencio, fundidos de 10/50 ms y normalizacion de pico.
3. Efectos derivados de los del juego y sintetizados con numpy (siseo de televisor, alarma corta, toma de aire,
   y alternativas sinteticas de golpe grave, subida y barrido).
4. efectos_gancho.wav: premezcla de efectos de 0:00 a 0:17 segun el guion (S01 a S07).

Uso: python -I herramientas/demo/audio_procesar.py
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parents[2]
AUDIO = RAIZ / "Nasa_Game" / "Presentacion" / "audio"
ORIG = AUDIO / "originales"
JUEGO = RAIZ / "juego" / "audio"
SR = 48000
DESFASE_PULSO = 0.180   # fase medida del pulso de 90 BPM en el original
DURACION = 150.0


def leer(ruta, canales=1):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ruta), "-ac", str(canales), "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    x = np.frombuffer(r.stdout, dtype=np.float32).copy()
    return x.reshape(-1, canales) if canales > 1 else x


def escribir(nombre, x):
    x = np.asarray(x, dtype=np.float32)
    canales = 1 if x.ndim == 1 else x.shape[1]
    destino = AUDIO / nombre
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(canales), "-i", "-",
                    "-c:a", "pcm_s24le", str(destino)], input=x.tobytes(), check=True)
    return destino


def db(v):
    return 10 ** (v / 20)


def pico(x, objetivo_db):
    m = float(np.max(np.abs(x)))
    return x * (db(objetivo_db) / m) if m > 0 else x


def fundidos(x, ent=0.01, sal=0.05):
    x = x.copy()
    a, b = int(ent * SR), int(sal * SR)
    rampa_a = np.linspace(0, 1, a, dtype=np.float32)
    rampa_b = np.linspace(1, 0, b, dtype=np.float32)
    if x.ndim == 1:
        x[:a] *= rampa_a
        x[-b:] *= rampa_b
    else:
        x[:a] *= rampa_a[:, None]
        x[-b:] *= rampa_b[:, None]
    return x


def recortar_silencio(x, umbral_db=-60):
    env = np.abs(x if x.ndim == 1 else x.max(axis=1))
    sobre = np.where(env > db(umbral_db))[0]
    if len(sobre) == 0:
        return x
    return x[max(0, sobre[0] - int(0.005 * SR)):]


def curva(claves, n):
    t = np.arange(n) / SR
    tiempos = [c[0] for c in claves]
    valores = [c[1] for c in claves]
    return db(np.interp(t, tiempos, valores)).astype(np.float32)


# automatizacion de la musica (s, dB relativo a pleno), de montaje.json y el guion (seccion 6)
AUTOMATIZACION = [
    (0.0, -90), (11.0, -90), (11.3, 0),        # gancho: sin musica hasta la primera nota
    (16.6, 0), (17.0, -20),                    # titulo: acorde pleno y baja a cama
    (52.0, -20), (52.4, -10), (54.6, -10), (55.0, -20),   # S18 ocular: sube a -10 y vuelve a cama
    (69.6, -20), (70.0, 0),                    # S22 -> montaje de minijuegos pleno
    (81.6, 0), (82.0, -20),                    # vuelve a cama para el bloque 5
    (101.0, -20), (101.4, -8), (104.6, -8), (105.0, -20),  # S36 despegue
    (123.0, -20), (126.0, 0),                  # crece desde 123 y plena en 126
    (130.0, 2.5), (135.0, 4.5), (140.0, 5.5),  # compensa el decrescendo propio del tema
    (148.5, 5.5), (149.5, -90), (150.0, -90),  # cola y 0,5 s de silencio
]


def musica():
    x = leer(ORIG / "musica_demo.mp3", 2)
    x = x[int(DESFASE_PULSO * SR):]
    n = int(DURACION * SR)
    if len(x) < n:
        x = np.vstack([x, np.zeros((n - len(x), 2), np.float32)])
    x = x[:n].copy()
    fin = curva([(0, 0), (148.5, 0), (149.5, -90), (150, -90)], n)
    cruda = x * fin[:, None]
    escribir("musica_demo.wav", pico(cruda, -1.0))
    auto = x * curva(AUTOMATIZACION, n)[:, None]
    escribir("musica_demo_automatizada.wav", pico(auto, -1.0))


MIRELO = {
    # id: (pico dB, fundido de salida s)
    "rugido_cohete": (-1.0, 0.3),
    "golpe_grave": (-1.0, 0.3),
    "subida": (-1.0, 0.02),
    "barrido": (-3.0, 0.1),
    "grillos": (-6.0, 0.4),
    "viento_orilla": (-6.0, 0.4),
    "tecleo": (-6.0, 0.2),
}


def efectos_mirelo():
    for ident, (p, sal) in MIRELO.items():
        x = leer(ORIG / f"{ident}.mp3")
        if ident in ("golpe_grave", "barrido", "subida"):
            x = recortar_silencio(x)
        escribir(f"{ident}.wav", fundidos(pico(x, p), 0.01, sal))


def ruido_rosa(n, rng):
    b = np.zeros(7)
    blanco = rng.standard_normal(n)
    y = np.empty(n)
    for i, w in enumerate(blanco):  # filtro de Paul Kellet
        b[0] = 0.99886 * b[0] + w * 0.0555179
        b[1] = 0.99332 * b[1] + w * 0.0750759
        b[2] = 0.96900 * b[2] + w * 0.1538520
        b[3] = 0.86650 * b[3] + w * 0.3104856
        b[4] = 0.55000 * b[4] - w * 0.5329522
        b[5] = -0.7616 * b[5] - w * 0.0168980
        y[i] = b.sum() + b[6] + w * 0.5362
        b[6] = w * 0.115926
    return y / np.max(np.abs(y))


def pasabanda(x, bajo, alto):
    f = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    f[(fr < bajo) | (fr > alto)] = 0
    return np.fft.irfft(f, len(x))


def sinteticos():
    rng = np.random.default_rng(1969)
    # siseo de televisor de tubo: ruido de banda media con zumbido de 60 Hz muy bajo y un leve vaiven
    n = int(4.0 * SR)
    t = np.arange(n) / SR
    s = pasabanda(rng.standard_normal(n), 1500, 9000)
    s = s / np.max(np.abs(s)) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * t))
    s += 0.05 * np.sin(2 * np.pi * 60 * t) + 0.03 * np.sin(2 * np.pi * 120 * t)
    escribir("siseo_tv.wav", fundidos(pico(s, -12.0), 0.2, 0.4))

    # alarma corta y baja: tres pitidos de dos tonos (660/550 Hz), suaves
    n = int(2.0 * SR)
    t = np.arange(n) / SR
    a = np.zeros(n)
    for k in range(3):
        ini = 0.1 + k * 0.6
        for j, f0 in enumerate((660, 550)):
            m = (t >= ini + j * 0.2) & (t < ini + j * 0.2 + 0.18)
            env = np.sin(np.pi * (t[m] - (ini + j * 0.2)) / 0.18) ** 0.5
            a[m] += env * (np.sin(2 * np.pi * f0 * t[m]) + 0.3 * np.sin(2 * np.pi * 3 * f0 * t[m]) / 3)
    escribir("alarma_corta.wav", fundidos(pico(a, -6.0), 0.005, 0.1))

    # toma de aire: ruido rosa de banda 600-4000 Hz con envolvente que sube 0,7 s y se corta suave
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    r = pasabanda(ruido_rosa(n, rng), 600, 4000)
    env = np.clip(t / 0.7, 0, 1) ** 1.6 * np.clip((1.0 - t) / 0.3, 0, 1)
    escribir("toma_aire.wav", fundidos(pico(r * env, -12.0), 0.01, 0.05))

    # alternativas sinteticas por si las de Mirelo no convencen al oido
    n = int(2.5 * SR)
    t = np.arange(n) / SR
    f = 30 + 50 * np.exp(-t / 0.08)                       # caida de tono 80 -> 30 Hz
    fase = 2 * np.pi * np.cumsum(f) / SR
    g = np.sin(fase) * np.exp(-t / 0.7)
    g += 0.25 * pasabanda(rng.standard_normal(n), 30, 300) * np.exp(-t / 0.25)
    g[: int(0.004 * SR)] += np.linspace(0.6, 0, int(0.004 * SR))   # ataque
    escribir("sint_golpe_grave.wav", fundidos(pico(g, -1.0), 0.001, 0.3))

    n = int(3.0 * SR)
    t = np.arange(n) / SR
    k = t / 3.0
    f = 200 * (8 ** k)                                   # 200 -> 1600 Hz
    fase = 2 * np.pi * np.cumsum(f) / SR
    tono = np.sin(fase) + 0.5 * np.sin(2 * fase) + 0.25 * np.sin(3 * fase)
    aire = pasabanda(rng.standard_normal(n), 2000, 12000)
    aire = aire / np.max(np.abs(aire))
    s = (0.5 * tono / 1.75 + 0.5 * aire) * k ** 2
    escribir("sint_subida.wav", fundidos(pico(s, -1.0), 0.05, 0.02))

    n = int(1.2 * SR)
    t = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(t / 1.0, 0, 1)) ** 2
    w = pasabanda(ruido_rosa(n, rng), 200, 6000) * env
    pan = np.clip(t / 1.0, 0, 1)
    estereo = np.stack([w * np.cos(pan * np.pi / 2), w * np.sin(pan * np.pi / 2)], axis=1)
    escribir("sint_barrido.wav", fundidos(pico(estereo, -3.0), 0.01, 0.1))


def derivados():
    # respiracion dentro del casco (ambiente_luna.ogg del juego) y rugido corto para el despegue de la base
    r = leer(JUEGO / "ambiente_luna.ogg")
    escribir("respiracion.wav", fundidos(pico(r[: int(6.0 * SR)], -10.0), 0.3, 0.5))
    rug = leer(AUDIO / "rugido_cohete.wav")
    escribir("rugido_corto.wav", fundidos(rug[: int(3.5 * SR)], 0.02, 1.2))


def ventana_mas_fuerte(x, dur):
    w = int(dur * SR)
    paso = int(0.05 * SR)
    mejor, i0 = -1, 0
    for i in range(0, len(x) - w, paso):
        e = float(np.mean(x[i:i + w] ** 2))
        if e > mejor:
            mejor, i0 = e, i
    return x[i0:i0 + w]


def gancho():
    n = int(17.0 * SR)
    mez = np.zeros(n, np.float32)

    def poner(x, t0, gan_db, recorte=None):
        x = x if recorte is None else x[: int(recorte * SR)]
        i = int(t0 * SR)
        j = min(n, i + len(x))
        mez[i:j] += (x[: j - i] * db(gan_db)).astype(np.float32)

    viento = leer(AUDIO / "viento_orilla.wav")
    resp = leer(AUDIO / "respiracion.wav")
    golpe = leer(AUDIO / "golpe_grave.wav")
    rugido = leer(AUDIO / "rugido_cohete.wav")
    aire = leer(AUDIO / "toma_aire.wav")
    # S01 0-2,5: viento y agua de la orilla, respiracion; S02 2,5-6: solo respiracion y golpe grave en 4,8
    poner(fundidos(viento[: int(3.0 * SR)], 0.5, 0.5), 0.0, -8)
    poner(fundidos(resp[: int(6.0 * SR)], 0.4, 0.3), 0.0, -10)
    poner(golpe, 4.8, -2)
    # S03 6-8,5: rugido a tope (la parte mas fuerte del archivo), corte seco a silencio en 8,5 (S04)
    r = ventana_mas_fuerte(rugido, 2.5)
    r = r * np.clip(np.arange(len(r)) / (0.25 * SR), 0, 1)   # entra en 0,25 s
    poner(r, 6.0, 0)
    mez[int(8.5 * SR):int(11.0 * SR)] = 0.0                 # silencio total
    # S06 13-15,5: toma de aire hacia 13,4
    poner(aire, 13.4, -4)
    escribir("efectos_gancho.wav", np.clip(mez, -0.891, 0.891))


def medir():
    filas = []
    for f in sorted(AUDIO.glob("*.wav")):
        info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=sample_rate,channels",
                                          "-of", "json", str(f)], capture_output=True, text=True).stdout)
        vd = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "volumedetect,ebur128=peak=true", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
        def tomar(clave):
            for linea in reversed(vd.splitlines()):
                if clave in linea:
                    return linea.split(clave)[1].strip().split()[0]
            return "?"
        filas.append({
            "archivo": f.name,
            "duracion_s": round(float(info["format"]["duration"]), 3),
            "canales": info["streams"][0]["channels"],
            "hz": int(info["streams"][0]["sample_rate"]),
            "media_dB": tomar("mean_volume:"),
            "pico_dB": tomar("max_volume:"),
            "LUFS_integrados": tomar("I:"),
            "pico_real_dBTP": tomar("Peak:"),
        })
    (AUDIO / "medicion_audio.json").write_text(json.dumps(filas, indent=1, ensure_ascii=False), encoding="utf-8")
    for r in filas:
        print(f"{r['archivo']:32} {r['duracion_s']:8.3f} s {r['canales']} can {r['hz']} Hz  media {r['media_dB']:>6}  pico {r['pico_dB']:>6}  "
              f"I {r['LUFS_integrados']:>6} LUFS  TP {r['pico_real_dBTP']:>6}")


if __name__ == "__main__":
    musica()
    efectos_mirelo()
    sinteticos()
    derivados()
    gancho()
    medir()
