"""Convierte los originales del lote A1 en los efectos del juego: juego/audio/<nombre>.ogg (Vorbis mono, 44,1 kHz).

Por cada efecto: elige la version (v1 o v2, segun analizar.py), recorta el silencio o se queda con el golpe mas
fuerte, normaliza el nivel (RMS de la parte activa, con el pico limitado), pone fundidos cortos y, en los
ambientes, cierra el bucle con un fundido cruzado para que no se oiga el salto. Despues mide cada ogg con
ffmpeg -af volumedetect y escribe conversion.json (lo usa registro.md).

No escucha nada: las cifras dicen que no es silencio y cuanto dura, no si suena bien.

Uso:  python -I convertir.py
"""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
SALIDA = RAIZ / "juego" / "audio"
TASA = 44100

# nombre en el juego: (original, modo, duracion maxima en s, RMS objetivo en dB, motivo de la eleccion)
#   corto    = ventana alrededor del golpe mas fuerte (pasos, golpes): no se solapan al repetirse
#   completo = recorta el silencio del principio y del final
#   bucle    = ambiente: todo el archivo con el final fundido sobre el principio
EFECTOS = {
	"paso": ("paso.mp3", "corto", 0.26, -17.0, "unica version"),
	"paso_luna": ("paso_luna.mp3", "corto", 0.36, -19.0,
		"v1: la v2 tiene el pico en -30,6 dB y el 64 % de la energia bajo 150 Hz (no se oiria en altavoces de portatil)"),
	"salto": ("salto_v2.mp3", "completo", 0.70, -17.0,
		"v2: la v1 tiene el 100 % de la energia bajo 150 Hz, un retumbo sin el roce de tela pedido"),
	"recoger": ("recoger.mp3", "completo", 1.00, -18.0, "unica version"),
	"umbral": ("umbral.mp3", "completo", 2.00, -19.0, "v1: la v2 se pago pero no se pudo descargar (conexion cortada)"),
	"logro": ("logro.mp3", "completo", 2.00, -18.0, "unica version"),
	"pagina": ("pagina.mp3", "corto", 0.55, -20.0, "unica version"),
	"radio": ("radio_v2.mp3", "completo", 0.80, -18.0,
		"v2: la v1 es casi silencio (pico -41,8 dB, RMS -57,7 dB)"),
	"golpe_mastil": ("golpe_mastil.mp3", "corto", 0.40, -18.0, "unica version"),
	"ambiente_luna": ("ambiente_luna.mp3", "bucle", 8.10, -18.0, "unica version"),
	"ambiente_sendero": ("ambiente_sendero.mp3", "bucle", 6.10, -20.0, "unica version"),
}
PICO_MAX = -1.0       # dBFS
CRUCE_BUCLE = 0.9     # s de fundido cruzado en los ambientes


def leer(ruta):
	r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ruta), "-ac", "1", "-ar", str(TASA), "-f", "f32le", "-"],
		capture_output=True, check=True)
	return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def db(v):
	return 20.0 * np.log10(max(float(v), 1e-9))


def envolvente(x, ventana_s=0.01):
	n = int(ventana_s * TASA)
	m = len(x) // n
	return np.array([np.sqrt(np.mean(x[i * n:(i + 1) * n] ** 2)) for i in range(m)]), n


def fundidos(x, entrada_s, salida_s):
	y = x.copy()
	a = min(int(entrada_s * TASA), len(y) // 2)
	b = min(int(salida_s * TASA), len(y) // 2)
	if a > 0:
		y[:a] *= np.linspace(0.0, 1.0, a)
	if b > 0:
		y[-b:] *= np.linspace(1.0, 0.0, b) ** 1.5
	return y


def recortar(x, modo, dur):
	env, n = envolvente(x)
	tope = env.max()
	if modo == "corto":
		i = int(np.argmax(env))
		# retrocede hasta el arranque del golpe (donde la envolvente cae 24 dB bajo el pico), como mucho 60 ms
		j = i
		while j > 0 and env[j - 1] > tope * 10 ** (-24 / 20) and (i - j) < 6:
			j -= 1
		ini = max(0, j * n - int(0.008 * TASA))
		fin = min(len(x), ini + int(dur * TASA))
		return fundidos(x[ini:fin], 0.004, dur * 0.45)
	if modo == "completo":
		activo = np.where(env > tope * 10 ** (-30 / 20))[0]
		ini = max(0, activo[0] * n - int(0.005 * TASA))
		fin = min(len(x), (activo[-1] + 1) * n, ini + int(dur * TASA))
		return fundidos(x[ini:fin], 0.004, min(0.12, (fin - ini) / TASA * 0.3))
	# bucle: fundido cruzado del final sobre el principio
	x = x[: int(dur * TASA)]
	c = int(CRUCE_BUCLE * TASA)
	cuerpo = x[: len(x) - c].copy()
	sube = np.sin(np.linspace(0.0, np.pi / 2.0, c)) ** 2
	cuerpo[:c] = x[len(x) - c:] * (1.0 - sube) + x[:c] * sube
	return cuerpo


def normalizar(x, rms_objetivo):
	env, _ = envolvente(x)
	activo = env[env > env.max() * 10 ** (-30 / 20)]
	rms = db(np.sqrt(np.mean(activo ** 2))) if len(activo) else db(np.sqrt(np.mean(x ** 2)))
	pico = db(np.abs(x).max())
	ganancia = min(rms_objetivo - rms, PICO_MAX - pico)
	return x * 10 ** (ganancia / 20), ganancia


def escribir_ogg(x, destino):
	with tempfile.TemporaryDirectory() as tmp:
		wav = Path(tmp) / "a.wav"
		with wave.open(str(wav), "wb") as w:
			w.setnchannels(1)
			w.setsampwidth(2)
			w.setframerate(TASA)
			w.writeframes((np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2").tobytes())
		subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "libvorbis", "-q:a", "5", "-ac", "1",
			str(destino)], check=True)


def medir(ruta):
	r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(ruta), "-af", "volumedetect", "-f", "null", "-"],
		capture_output=True, text=True, encoding="utf-8", errors="replace")
	datos = {}
	for linea in r.stderr.splitlines():
		for clave in ("mean_volume", "max_volume"):
			if clave + ":" in linea:
				datos[clave] = float(linea.split(clave + ":")[1].split("dB")[0])
		if "Duration:" in linea:
			h, m, s = linea.split("Duration:")[1].split(",")[0].strip().split(":")
			datos["duracion_s"] = round(int(h) * 3600 + int(m) * 60 + float(s), 3)
	return datos


def main():
	SALIDA.mkdir(parents=True, exist_ok=True)
	informe = {}
	for nombre, (origen, modo, dur, rms, motivo) in EFECTOS.items():
		x = leer(AQUI / "originales" / origen)
		y = recortar(x, modo, dur)
		y, ganancia = normalizar(y, rms)
		destino = SALIDA / (nombre + ".ogg")
		escribir_ogg(y, destino)
		m = medir(destino)
		m.update({"original": origen, "modo": modo, "ganancia_db": round(ganancia, 1), "eleccion": motivo,
			"bytes": destino.stat().st_size})
		informe[nombre] = m
		print("%-17s %-18s %-8s %5.2f s  media %6.1f dB  pico %5.1f dB  ganancia %+5.1f dB" % (
			nombre, origen, modo, m.get("duracion_s", 0.0), m.get("mean_volume", -99), m.get("max_volume", -99), ganancia))
	(AQUI / "conversion.json").write_text(json.dumps(informe, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
	main()
