"""Corta las tomas de segmentos.json desde las grabaciones completas ya hechas (luz_demo_tmp/<fuente>.avi, que deja
capturar.py con --conservar), sin volver a grabar. Uso: python -I herramientas/demo/cortar_externas.py <fuente> [...]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capturar as c  # noqa: E402


def main():
    c.cargar_segmentos()
    for fuente in sys.argv[1:]:
        avi = c.TEMPORAL / f"{fuente}.avi"
        total = c.cuadros_avi(avi)
        for id_toma, (inicio, dur, que) in c.EXTERNAS[fuente]["tomas"].items():
            a = int(round(inicio * c.FPS))
            b = min(total - 1, a + int(round(dur * c.FPS)) - 1)
            salida = c.MATERIAL / f"{id_toma}.mp4"
            seg = c.convertir(avi, salida, a, b, sonido=False)
            c.hoja(salida, c.HOJAS / f"{id_toma}.jpg")
            c.registrar(id_toma, salida, seg, que)
            print(f"OK {salida.name} {seg:.1f} s", flush=True)


if __name__ == "__main__":
    main()
