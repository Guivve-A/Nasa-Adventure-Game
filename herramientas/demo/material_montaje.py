"""Anade a cada segmento de Nasa_Game/Presentacion/montaje.json el campo "material": las rutas reales, ya listas en
Nasa_Game/Presentacion/material/, con que se monta ese segmento (sin tocar tiempos, rotulos ni sonido).
  material: lista de {"ruta", "de", "a" (opcional, tiempo del video demo), "desde_s" (opcional: segundo de la toma
            donde empieza el tramo bueno), "tipo": video|fija|grafico}
  material_estado: "movimiento" (video real), "fija" (imagen con movimiento lento), "grafico" (lo hace el grafista)
Solo se escriben rutas que existen; lo que falta queda en "material_falta".
Uso: python -I herramientas/demo/material_montaje.py
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent.parent
P = RAIZ / "Nasa_Game" / "Presentacion"
MONTAJE = P / "montaje.json"
M = "Nasa_Game/Presentacion/material/"
F = M + "fijas/"


def v(nombre, desde=None, de=None, a=None, alt=None):
    d = {"ruta": M + nombre, "tipo": "video"}
    if desde is not None:
        d["desde_s"] = desde
    if de is not None:
        d["de"], d["a"] = de, a
    if alt:
        d["si_falta"] = alt
    return d


def f(nombre, de=None, a=None):
    d = {"ruta": F + nombre, "tipo": "fija"}
    if de is not None:
        d["de"], d["a"] = de, a
    return d


def g(gid):
    return {"ruta": f"Nasa_Game/Presentacion/graficos/ ({gid})", "tipo": "grafico"}


MAPA = {
    "S01": [v("cine/cine_P03.mp4")],
    "S02": [v("cine/cine_P04.mp4")],
    "S03": [v("cine/cine_P05.mp4"), f("cine__L10_K05_placas_lisas.jpg")],
    "S04": [f("cine__L09b_K11a_final.jpg", 8.5, 9.3), f("cine__L09b_K11_final.jpg", 9.3, 11.0)],
    "S05": [f("cine__L09d_K13a_final.jpg")],
    "S06": [f("cine__L09c_P14c_C_cine_gpt.jpg")],
    "S07": [g("G01")],
    "S08": [f("cine__L09b_K10_final.jpg")],
    "S09": [f("cine__L09b_K12_final_v2.jpg")],
    "S10": [v("habitacion.mp4", desde=1.0)],
    "S11": [v("orbita.mp4", desde=0.6)],
    "S12": [v("ciudad.mp4", desde=4.0)],
    "S13": [v("minimapa.mp4", desde=0.5)],
    "S14": [v("carga_mirador.mp4", desde=0.9, alt="carga.mp4")],
    "S15": [v("mirador_telescopio.mp4", desde=0.0)],
    "S16": [v("luna_lenta.mp4", desde=1.0, alt="luna.mp4")],
    "S17": [v("mapa_tecla_m.mp4", desde=1.0, alt="mapa.mp4")],
    "S18": [v("mirador_telescopio.mp4", desde=3.0, de=52.0, a=53.0), f("capturas__luna_telescopio.jpg", 53.0, 55.0)],
    "S19": [v("telescopio_luna_real.mp4", desde=0.0), f("capturas__luna_telescopio.jpg")],
    "S20": [g("G02")],
    "S21": [v("cuaderno.mp4", desde=2.0)],
    "S22": [f("capturas__vuelta6_arcade_nueve.jpg")],
    "S23": [v("mj_seguidor.mp4", desde=5.0)],
    "S24": [v("mj_antena.mp4", desde=2.5)],
    "S25": [v("mj_satelite.mp4", desde=5.5)],
    "S26": [v("mj_telescopio.mp4", desde=4.3)],
    "S27": [v("mj_linea_tiempo.mp4", desde=2.5)],
    "S28": [v("mj_muestras.mp4", desde=3.8)],
    "S29": [v("mj_banderas.mp4", desde=3.0)],
    "S30": [v("mj_regreso.mp4", desde=3.0)],
    "S31": [v("mj_orbita.mp4", desde=3.0)],
    "S32": [v("artemis_base.mp4")],
    "S33": [v("artemis_rover_hielo.mp4", de=85.0, a=87.5), v("artemis_marte.mp4", de=87.5, a=90.0)],
    "S34": [v("artemis_lluvia_solar.mp4", desde=0.3)],
    "S35": [f("marte__01_programa.jpg", 95.0, 96.0), v("marte_aterrizaje.mp4", desde=3.0, de=96.0, a=101.0)],
    "S36": [v("artemis_despegue_viaje.mp4", desde=0.5)],
    "S37": [g("G03")] + [f(n) for n in ["hojas__HR_PER_v1.jpg", "hojas__HR_URB_v1.jpg", "hojas__HR_VEG_v1.jpg",
                                        "hojas__Hojas_v1_lamina.jpg", "arte__L02_exploracion_camara_alta.jpg"]],
    "S38": [v("recorrido_manos.mp4"), {"ruta": M + "consola_recorrido_manos.txt", "tipo": "texto para G05"}, g("G05")],
    "S39": [v("mirador_telescopio.mp4", desde=0.0), {"ruta": M + "fps_medido.txt", "tipo": "texto: medicion real"}],
    "S40": [v("mirador_quieto.mp4")],
    "S41": [f("capturas__vuelta3_seis_escenas.jpg")],
    "S42": [f("capturas__vuelta6_arcade_nueve.jpg")],
    "S43": [v("cuaderno.mp4", desde=4.0)],
    "S44": [v("marte_superficie.mp4", alt="artemis_marte.mp4"), f("artemis__13_marte_base.jpg")],
    "S45": [v("telescopio_luna_real.mp4", desde=4.0), f("capturas__luna_telescopio.jpg")],
    "S46": [g("G04")],
    "S47": [v("mirador_alejar.mp4")],
    "S48": [g("G01")],
}


def existe(d):
    if d["tipo"] == "grafico":
        return True
    return (RAIZ / d["ruta"]).exists()


def main():
    datos = json.loads(MONTAJE.read_text(encoding="utf-8"))
    resumen = {}
    for s in datos["segmentos"]:
        lista = MAPA.get(s["id"], [])
        bien, falta = [], []
        for d in lista:
            if existe(d):
                bien.append(d)
            elif d.get("si_falta") and (RAIZ / (M + d["si_falta"])).exists():
                d2 = dict(d, ruta=M + d["si_falta"]); d2.pop("si_falta"); d2.pop("desde_s", None)
                bien.append(d2); falta.append(d["ruta"])
            else:
                falta.append(d["ruta"])
        for d in bien:
            d.pop("si_falta", None)
        s["material"] = bien
        if falta:
            s["material_falta"] = falta
        else:
            s.pop("material_falta", None)
        tipos = {d["tipo"] for d in bien}
        s["material_estado"] = ("movimiento" if "video" in tipos else "fija" if "fija" in tipos
                                else "grafico" if "grafico" in tipos else "sin material")
        resumen[s["id"]] = s["material_estado"] + (f" (falta {', '.join(Path(x).name for x in falta)})" if falta else "")
    MONTAJE.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, e in resumen.items():
        print(k, e)


if __name__ == "__main__":
    main()
