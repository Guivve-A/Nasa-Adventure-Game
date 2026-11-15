# Arma los JSON del lote 08 (laminas de carga pintadas) con un bloque de tecnica comun.
import json
import sys
from pathlib import Path

RAIZ = Path(r"C:\Users\guill\Desktop\Juego 2d-hd")
CARPETA = "Nasa_Game/Fase_1_Arte/Exploracion/Lote_08"

TECNICA = (
    "Painted as a full-bleed plate from a hand-made illustrated storybook: traditional gouache and transparent "
    "watercolor on textured cold-press paper, visible brush strokes, soft wet-in-wet washes with the paper grain "
    "showing through, simplified flat shapes with loose painterly edges, very few small details, large calm areas. "
    "Restrained warm palette of cream, ochre, terracotta, muted tropical green and petrol-blue shadows; shadows are "
    "colored, never black; low saturation. Strong atmospheric perspective: the far distance is pale, hazy and bluish "
    "with almost no detail, and only the focal area is a little crisper. Composition in three layered planes like a "
    "paper theater: a dark, simple silhouette framing the foreground, the lit middle ground, and a pale background. "
    "Matte and handmade: no glossy highlights, no bloom, no lens flare, no light rays, no 3D render look, no digital "
    "sharpness, no hyper-detail."
)

PERSONAJES = (
    "Tiny in the frame, less than one tenth of the image height: the young engineering student from the first "
    "reference image (voluminous dark curly hair, warm brown skin, khaki jacket and cargo pants, brown crossbody bag) "
    "and her small gray-taupe cat from the second reference image (cream face and paws, blue collar with a small "
    "cyan round tag). Use the references only for their design and colors, and paint both with a few gouache brush "
    "strokes in the same style as the scene."
)

CIERRE = "No text, no letters, no numbers, no logos, no insignia, no emblems, no flags. {SIN_TEXTO}"

ESCENAS = {
    "habitacion": (
        "A wide view of a small upstairs bedroom-workshop in an old wooden hillside house of a tropical port city, on a "
        "warm early morning. Through a big open window with wooden shutters, the pale hazy river city and a green hill "
        "far away. Inside: a simple bed with a blue blanket, a long workbench with hand tools, a soldering iron, "
        "notebooks and a small homemade motorized telescope mount, a little telescope on a tripod facing the window, "
        "potted plants and a terracotta tile floor with a woven rug. Soft morning light falls across the floor in one "
        "calm warm shape. The student sits at the workbench working on the mount and the cat sleeps on the windowsill. "
        "Foreground framed by dark leaf silhouettes of a potted plant and the edge of a wooden beam."
    ),
    "ciudad": (
        "A wide vista of a small neighborhood plaza at the foot of a hillside stair neighborhood in a tropical port "
        "city, late golden afternoon. Colorful simple houses with tin roofs climb the hill along a long stairway; at "
        "the back of the plaza a small municipal library with a few columns, wide steps and a softly glowing doorway; "
        "a round stone fountain, a couple of benches and two green iguanas resting on a low wall. Far away on the "
        "right, a pale wide river estuary dissolving into the haze. The student and the cat cross the plaza toward the "
        "library, seen from behind. Foreground framed by the dark silhouette of a big tree branch with a few red "
        "flowers and a low wall in shadow."
    ),
    "sendero": (
        "A wide vista of a forest path on a green hill above a tropical port city, warm afternoon. A dirt path winds "
        "beside a small turquoise stream with a wooden plank bridge; a huge old tree with red flowers spreads over the "
        "path; in a small clearing in the middle distance, a small homemade satellite dish antenna on a tripod and a "
        "little solar panel. Far below and behind, the pale hazy city and river. The student and the cat walk along "
        "the path toward the bridge. Foreground framed by dark silhouettes of large tropical leaves and ferns."
    ),
    "mirador": (
        "A wide vista of a hilltop lookout at night under the Moon: a stone terrace with a low balustrade and a small "
        "white lighthouse tower with one warm lit window, a telescope on a tripod pointed at the sky, a few warm string "
        "lights. Below, the city lights spread along a dark wide river, painted as soft dots of warm color. Low in a "
        "deep petrol-blue and indigo sky, a thin crescent Moon lying on its back like a smile, with the rest of its "
        "disc faintly visible in a soft gray glow (earthshine). The student looks through the telescope and the cat "
        "sits on the balustrade. Night shadows are deep blue and teal, never black; the lamp light is warm orange. "
        "Foreground framed by the dark silhouette of the balustrade and a flowering bush."
    ),
    "luna": (
        "A dreamlike wide vista of the surface of the Moon: a gently rolling gray plain with soft round craters and "
        "scattered rocks, long soft shadows painted in deep blue and violet, never black. High in a deep indigo night "
        "sky with a few sparse stars hangs a large half-lit blue and white Earth. On the plain, a trail of small "
        "bootprints and tiny paw prints, a small cardboard box resting on the ground like a tiny capsule, and far away "
        "the small simple silhouette of a generic four-legged lunar landing stage with no markings. The student, in a "
        "small soft original spacesuit with a clear bubble helmet, and the cat, with a tiny bubble helmet, hop across "
        "the plain in low gravity. Foreground framed by the dark silhouette of a big boulder and the rim of a crater."
    ),
}


def lote(nombre, sufijo, params, tope, ids, extra=None, previa=None):
    trabajos = []
    for zona in ids:
        prompt = "A storybook painting. " + ESCENAS[zona] + " " + PERSONAJES + " " + TECNICA + " " + CIERRE
        imagenes = ["@ANC_PROTA_1", "@ANC_GATO"]
        if previa and zona in previa:
            imagenes.append(previa[zona])
            prompt = ("Keep the composition, the layout and the painting technique of the last reference image (the "
                      "approved draft) and repaint it as a finished, cleaner gouache plate with the same loose "
                      "brushwork. " + prompt)
        if extra and zona in extra:
            prompt = prompt.replace("A storybook painting. ", "A storybook painting. " + extra[zona] + " ")
        trabajos.append({"id": f"L08_carga_{zona}{sufijo}", "modelo": "gpt_image_2_6", "params": params,
                         "imagenes": imagenes, "prompt": prompt})
    return {"lote": nombre, "carpeta": CARPETA, "tope": tope,
            "_nota": "Laminas de carga pintadas (lote 08). Permiso de Guillermo del 2026-11-14: «usa Higgsfield para lo que necesites». Tope del carril: 18 creditos.",
            "trabajos": trabajos}


if __name__ == "__main__":
    fase = sys.argv[1]
    destino = RAIZ / CARPETA
    destino.mkdir(parents=True, exist_ok=True)
    ZONAS = ["habitacion", "ciudad", "sendero", "mirador", "luna"]
    if fase == "a":
        spec = lote("L08a", "_borrador", {"aspect_ratio": "16:9", "resolution": "1k", "quality": "low"}, 1.25, ZONAS)
        (destino / "lote_08a_borradores.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
    if fase == "b":
        subidas = json.loads((destino / "subidas.json").read_text(encoding="utf-8"))
        previa = {z: subidas[f"L08_carga_{z}_borrador"]["id"] for z in ZONAS}
        extra = {
            "habitacion": "Keep the cat asleep on the windowsill and the student at the workbench.",
            "ciudad": "Make the red flowers on the foreground branch fewer and smaller, loosely painted.",
            "luna": "Paint the Earth softer and less saturated, with gouache, not as a photograph.",
        }
        params = {"aspect_ratio": "16:9", "resolution": "2k", "quality": "high"}
        spec = lote("L08b", "", params, 13.75, ZONAS, extra=extra, previa=previa)
        for t in spec["trabajos"]:
            t["prompt"] = t["prompt"].replace(
                "repaint it as a finished, cleaner gouache plate with the same loose brushwork. ",
                "repaint it as the finished gouache plate at higher resolution, with the same loose brushwork, the "
                "same paper grain and the same level of detail: do not add fine detail, do not sharpen, do not make "
                "it look like digital art. ")
        (destino / "lote_08b_finales.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
    print("ok", fase)
