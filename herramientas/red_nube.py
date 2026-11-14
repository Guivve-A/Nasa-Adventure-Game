"""Mide la conexion de este equipo hacia regiones de centros de datos y su ancho de banda.

Sirve para decidir donde alquilar un PC en la nube. No envia datos personales:
solo abre conexiones TCP y descarga/sube bytes de prueba.

Uso:  python herramientas/red_nube.py
"""
import socket
import statistics
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

# (etiqueta, host, puerto). Vultr publica un servidor de ping por ciudad; AWS, un extremo por region.
DESTINOS = [
    ("Miami (Vultr)", "fl-us-ping.vultr.com", 80),
    ("Atlanta (Vultr)", "ga-us-ping.vultr.com", 80),
    ("Dallas (Vultr)", "tx-us-ping.vultr.com", 80),
    ("Nueva Jersey (Vultr)", "nj-us-ping.vultr.com", 80),
    ("Chicago (Vultr)", "il-us-ping.vultr.com", 80),
    ("Los Angeles (Vultr)", "lax-ca-us-ping.vultr.com", 80),
    ("Ciudad de Mexico (Vultr)", "mex-mx-ping.vultr.com", 80),
    ("Santiago de Chile (Vultr)", "scl-cl-ping.vultr.com", 80),
    ("Sao Paulo (Vultr)", "sao-br-ping.vultr.com", 80),
    ("Virginia (AWS us-east-1)", "ec2.us-east-1.amazonaws.com", 443),
    ("Ohio (AWS us-east-2)", "ec2.us-east-2.amazonaws.com", 443),
    ("Oregon (AWS us-west-2)", "ec2.us-west-2.amazonaws.com", 443),
    ("Mexico (AWS mx-central-1)", "ec2.mx-central-1.amazonaws.com", 443),
    ("Sao Paulo (AWS sa-east-1)", "ec2.sa-east-1.amazonaws.com", 443),
    ("Nueva York (DigitalOcean)", "speedtest-nyc1.digitalocean.com", 443),
    ("San Francisco (DigitalOcean)", "speedtest-sfo3.digitalocean.com", 443),
]
MUESTRAS = 8


def latencia(host, puerto):
    try:
        ip = socket.gethostbyname(host)
    except OSError:
        return None
    tiempos = []
    for _ in range(MUESTRAS):
        inicio = time.perf_counter()
        try:
            with socket.create_connection((ip, puerto), timeout=3):
                tiempos.append((time.perf_counter() - inicio) * 1000)
        except OSError:
            pass
        time.sleep(0.05)
    return tiempos


def ancho_de_banda():
    resultados = {}
    try:
        inicio = time.perf_counter()
        with urllib.request.urlopen("https://speed.cloudflare.com/__down?bytes=25000000", timeout=60) as r:
            total = 0
            while True:
                bloque = r.read(65536)
                if not bloque:
                    break
                total += len(bloque)
        seg = time.perf_counter() - inicio
        resultados["bajada_mbps"] = total * 8 / seg / 1e6
    except Exception as error:  # noqa: BLE001
        resultados["bajada_error"] = str(error)
    try:
        datos = bytes(8_000_000)
        peticion = urllib.request.Request("https://speed.cloudflare.com/__up", data=datos, method="POST")
        inicio = time.perf_counter()
        with urllib.request.urlopen(peticion, timeout=90) as r:
            r.read()
        seg = time.perf_counter() - inicio
        resultados["subida_mbps"] = len(datos) * 8 / seg / 1e6
    except Exception as error:  # noqa: BLE001
        resultados["subida_error"] = str(error)
    return resultados


def main():
    print(f"{'Destino':32}{'min':>7}{'mediana':>9}{'max':>7}{'variacion':>11}  (ms, conexion TCP, {MUESTRAS} muestras)")
    filas = []
    for etiqueta, host, puerto in DESTINOS:
        t = latencia(host, puerto)
        if not t:
            print(f"{etiqueta:32}  sin respuesta")
            continue
        filas.append((statistics.median(t), etiqueta))
        variacion = statistics.pstdev(t) if len(t) > 1 else 0.0
        print(f"{etiqueta:32}{min(t):7.0f}{statistics.median(t):9.0f}{max(t):7.0f}{variacion:11.1f}")
    filas.sort()
    print("\nMas cercanos:", ", ".join(f"{e} ({m:.0f} ms)" for m, e in filas[:4]))
    print("\nAncho de banda (Cloudflare, una sola conexion):")
    for clave, valor in ancho_de_banda().items():
        print(f"  {clave}: {valor:.1f}" if isinstance(valor, float) else f"  {clave}: {valor}")


if __name__ == "__main__":
    main()
