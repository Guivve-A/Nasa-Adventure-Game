"""Matriz de costos de Higgsfield para los modelos utiles en un videojuego.

Solo usa `generate cost` (no crea trabajos ni gasta creditos).
Los modelos que exigen imagen usan un marcador gris ya subido (IMG).

Uso:  python herramientas/hf_costos_matriz.py
Salida: Nasa_Game/Fase_0_Tecnica/Datos/hf_costos_matriz.json y .md
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "Nasa_Game" / "Fase_0_Tecnica" / "Datos"

IMG = "dcfc3212-00c2-4602-9d58-aed0b8109c37"   # marcador gris 768x768 (upload id)
URL3D = "https://example.com/modelo.glb"       # URL ficticia: solo para cotizar

cmd = shutil.which("higgsfield.cmd") or shutil.which("higgsfield")
HF = str(Path(cmd).parent / "node_modules" / "@higgsfield" / "cli" / "vendor" / "hf.exe")


def costo(job, params):
    args = [HF, "generate", "cost", job]
    for k, v in params.items():
        if k == "image":
            for ref in (v if isinstance(v, list) else [v]):
                args += ["--image", ref]
        else:
            args += [f"--{k}", str(v).lower() if isinstance(v, bool) else str(v)]
    args.append("--json")
    try:
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if r.returncode == 0:
        try:
            return json.loads(r.stdout).get("credits"), None
        except Exception:
            return None, r.stdout[:200]
    return None, (r.stderr or r.stdout).strip().replace("\n", " | ")[:260]


P = "test"
CASOS = []


def caso(grupo, etiqueta, job, **params):
    CASOS.append((grupo, etiqueta, job, params))


# ---------- Imagen: concept art, hojas de referencia, texturas, UI ----------
for q in ("low", "medium", "high", "xhigh", "max"):
    for res in ("1k", "2k", "4k"):
        caso("imagen", f"gpt_image_2_6 calidad={q} {res}", "gpt_image_2_6", prompt=P, quality=q, resolution=res)
caso("imagen", "gpt_image_2_6 high 1k fondo transparente", "gpt_image_2_6", prompt=P, quality="high", resolution="1k", background="transparent")
caso("imagen", "gpt_image_2_6 high 1k con 1 referencia", "gpt_image_2_6", prompt=P, quality="high", resolution="1k", image=IMG)
caso("imagen", "gpt_image_2_6 high 1k con 4 referencias", "gpt_image_2_6", prompt=P, quality="high", resolution="1k", image=[IMG] * 4)
caso("imagen", "gpt_image_2_6 high 1k lote de 4", "gpt_image_2_6", prompt=P, quality="high", resolution="1k", batch_size=4)
for q in ("low", "medium", "high"):
    caso("imagen", f"gpt_image_2_6_flare calidad={q} 1k", "gpt_image_2_6_flare", prompt=P, quality=q, resolution="1k")
    caso("imagen", f"gpt_image_2_5 calidad={q} 1k", "gpt_image_2_5", prompt=P, quality=q, resolution="1k")
for res in ("1k", "2k", "4k"):
    caso("imagen", f"nano_banana_pro {res}", "nano_banana_pro", prompt=P, resolution=res)
    caso("imagen", f"nano_banana_flash (NB2) {res}", "nano_banana_flash", prompt=P, resolution=res)
    caso("imagen", f"nano_banana_2_1 {res}", "nano_banana_2_1", prompt=P, resolution=res)
caso("imagen", "nano_banana_pro 2k con 4 referencias", "nano_banana_pro", prompt=P, resolution="2k", image=[IMG] * 4)
for res in ("1k", "1.5k", "2k"):
    caso("imagen", f"seedream_5_5 {res}", "seedream_5_5", prompt=P, resolution=res)
    caso("imagen", f"3d_jutsu_angles {res}", "3d_jutsu_angles", prompt=P, resolution=res)
caso("imagen", "3d_jutsu_angles 2k con 1 referencia", "3d_jutsu_angles", prompt=P, resolution="2k", image=IMG)
caso("imagen", "seedream_5_5 2k con 4 referencias", "seedream_5_5", prompt=P, resolution="2k", image=[IMG] * 4)
for job in ("seedream_v5_pro", "seedream_v5_lite", "seedream_5_0_flash", "seedream_v4_5", "flux_3_image", "flux_2", "flux_kontext",
            "z_image", "text2image_soul_v2", "soul_location", "recraft_v4_1", "ideogram_4_5", "kling_omni_image", "image_auto",
            "nano_banana", "nano_banana_2_lite", "grok_image_2_0", "minimax_h3_image"):
    caso("imagen", f"{job} (defecto)", job, prompt=P)
caso("imagen", "flux_kontext con 1 referencia", "flux_kontext", prompt=P, image=IMG)
for q in ("low", "medium", "high"):
    caso("imagen", f"ideogram_vector generate calidad={q}", "ideogram_vector", operation="generate", prompt=P, quality=q)
caso("imagen", "ideogram_vector vectorize", "ideogram_vector", operation="vectorize", image=IMG)

# ---------- Utilidades de imagen ----------
caso("utilidad", "image_background_remover", "image_background_remover", image=IMG)
caso("utilidad", "bytedance_image_upscale 2k", "bytedance_image_upscale", image=IMG, resolution="2k")
caso("utilidad", "bytedance_image_upscale 4k", "bytedance_image_upscale", image=IMG, resolution="4k")
caso("utilidad", "topaz_image 2048x2048", "topaz_image", image=IMG, output_width=2048, output_height=2048)
caso("utilidad", "topaz_image 4096x4096", "topaz_image", image=IMG, output_width=4096, output_height=4096)
caso("utilidad", "nano_banana_2_relight", "nano_banana_2_relight", image=IMG, brightness=50, color="#ffd9a0", light_quality="soft", light_source="ful")
caso("utilidad", "nano_banana_2_shots", "nano_banana_2_shots", image=IMG)
caso("utilidad", "outpaint", "outpaint", image=IMG)
caso("utilidad", "flux_2_pro_outpaint", "flux_2_pro_outpaint", image=IMG)

# ---------- Sprites animados (AutoSprite) ----------
for tier in ("turbo", "pro", "max"):
    caso("autosprite", f"autosprite iso_walk_down tier={tier} 25f 256px", "autosprite", image=IMG, kind="iso_walk_down", video_tier=tier)
caso("autosprite", "autosprite idle turbo 25f 256px", "autosprite", image=IMG, kind="idle")
caso("autosprite", "autosprite walk turbo 25f 256px", "autosprite", image=IMG, kind="walk")
caso("autosprite", "autosprite attack turbo 25f 256px", "autosprite", image=IMG, kind="attack")
for fc in (8, 12, 16, 49):
    caso("autosprite", f"autosprite iso_walk_down turbo {fc}f 256px", "autosprite", image=IMG, kind="iso_walk_down", frame_count=fc)
for fs in (128, 512, 1024):
    caso("autosprite", f"autosprite iso_walk_down turbo 25f {fs}px", "autosprite", image=IMG, kind="iso_walk_down", frame_size=fs)
caso("autosprite", "autosprite iso_walk_down turbo remove_bg=ultra", "autosprite", image=IMG, kind="iso_walk_down", remove_bg="ultra")
caso("autosprite", "autosprite custom turbo", "autosprite", image=IMG, kind="custom", name="soldar", prompt="soldering at a desk")
caso("autosprite", "autosprite no humanoide (gato) iso_walk_down turbo", "autosprite", image=IMG, kind="iso_walk_down", is_humanoid=False)

# ---------- 3D ----------
caso("3d", "tripo_3d texto (defecto)", "tripo_3d", prompt=P)
caso("3d", "tripo_3d texto sin textura", "tripo_3d", prompt=P, texture=False, pbr=False)
caso("3d", "tripo_3d texto detallado", "tripo_3d", prompt=P, geometry_quality="detailed", texture_quality="detailed")
caso("3d", "hunyuan3d_v3_1_text_to_3d std", "hunyuan3d_v3_1_text_to_3d", prompt=P)
caso("3d", "hunyuan3d_v3_1_text_to_3d pro", "hunyuan3d_v3_1_text_to_3d", prompt=P, mode="pro")
caso("3d", "meshy_v6_text_to_3d full", "meshy_v6_text_to_3d", prompt=P)
caso("3d", "meshy_v6_text_to_3d preview", "meshy_v6_text_to_3d", prompt=P, mode="preview")
caso("3d", "meshy_v6_text_to_3d lowpoly", "meshy_v6_text_to_3d", prompt=P, model_type="lowpoly")
caso("3d", "image_to_3d (defecto: sin textura)", "image_to_3d", image=IMG)
caso("3d", "image_to_3d con textura", "image_to_3d", image=IMG, should_texture=True)
caso("3d", "image_to_3d textura + remesh", "image_to_3d", image=IMG, should_texture=True, should_remesh=True, target_polycount=8000, topology="quad")
caso("3d", "image_to_3d textura + rig", "image_to_3d", image=IMG, should_texture=True, enable_rigging=True, pose_mode="a-pose")
caso("3d", "image_to_3d textura + rig + animacion", "image_to_3d", image=IMG, should_texture=True, enable_rigging=True, pose_mode="a-pose", enable_animation=True, animation_action_id=92)
caso("3d", "multi_image_to_3d 4 vistas (defecto)", "multi_image_to_3d", image=[IMG] * 4)
caso("3d", "multi_image_to_3d 4 vistas con textura", "multi_image_to_3d", image=[IMG] * 4, should_texture=True)
caso("3d", "multi_image_to_3d 4 vistas textura + rig", "multi_image_to_3d", image=[IMG] * 4, should_texture=True, enable_rigging=True, pose_mode="a-pose")
caso("3d", "meshy_v7_image_to_3d (defecto: textura + remesh)", "meshy_v7_image_to_3d", image=IMG)
caso("3d", "meshy_v7_image_to_3d lowpoly", "meshy_v7_image_to_3d", image=IMG, model_type="lowpoly")
caso("3d", "meshy_v7_image_to_3d sin textura", "meshy_v7_image_to_3d", image=IMG, should_texture=False)
caso("3d", "meshy_v7_image_to_3d + rig", "meshy_v7_image_to_3d", image=IMG, enable_rigging=True, pose_mode="a-pose")
caso("3d", "meshy_v7_image_to_3d + rig + animacion", "meshy_v7_image_to_3d", image=IMG, enable_rigging=True, pose_mode="a-pose", enable_animation=True)
caso("3d", "meshy_v7_image_to_3d ultra", "meshy_v7_image_to_3d", image=IMG, ultra_mode=True)
caso("3d", "hunyuan3d_v3_image_to_3d Normal", "hunyuan3d_v3_image_to_3d", image=IMG)
caso("3d", "hunyuan3d_v3_image_to_3d LowPoly quads", "hunyuan3d_v3_image_to_3d", image=IMG, generate_type="LowPoly", polygon_type="quadrilateral", face_count=8000)
caso("3d", "hunyuan3d_v3_image_to_3d Geometry (sin textura)", "hunyuan3d_v3_image_to_3d", image=IMG, generate_type="Geometry")
caso("3d", "hunyuan3d_v3_image_to_3d Normal + PBR", "hunyuan3d_v3_image_to_3d", image=IMG, enable_pbr=True)
caso("3d", "tripo_h3_1_image_to_3d (defecto)", "tripo_h3_1_image_to_3d", image=IMG)
caso("3d", "tripo_h3_1_image_to_3d sin textura", "tripo_h3_1_image_to_3d", image=IMG, texture=False, pbr=False)
caso("3d", "tripo_h3_1_image_to_3d quads 8000 caras", "tripo_h3_1_image_to_3d", image=IMG, quad=True, face_limit=8000)
caso("3d", "tripo_h3_1_image_to_3d detallado", "tripo_h3_1_image_to_3d", image=IMG, geometry_quality="detailed", texture_quality="detailed")
caso("3d", "tripo_h3_1_multiview_to_3d 4 vistas", "tripo_h3_1_multiview_to_3d", image=[IMG] * 4)
caso("3d", "tripo_p2_image_to_3d (defecto)", "tripo_p2_image_to_3d", image=IMG)
caso("3d", "tripo_p2_image_to_3d quads 8000 caras", "tripo_p2_image_to_3d", image=IMG, quad=True, face_limit=8000)
for tq in ("fast", "detailed", "extreme"):
    extra = {"texture_version": "v3.5-20260815"} if tq == "fast" else {}
    caso("3d", f"tripo_p2_image_to_3d textura={tq}", "tripo_p2_image_to_3d", image=IMG, texture_quality=tq, **extra)
caso("3d", "sam_3_3d (objetos desde foto)", "sam_3_3d", image=IMG)
caso("3d", "sam_3_3d_body", "sam_3_3d_body", image=IMG)
caso("3d", "3d_rigging (solo rig)", "3d_rigging", model_url=URL3D)
caso("3d", "3d_rigging + animacion", "3d_rigging", model_url=URL3D, enable_animation=True, animation_action_id=92)
caso("3d", "meshy_v5_remesh quads 8000", "meshy_v5_remesh", model_url=URL3D, target_polycount=8000, topology="quad")
caso("3d", "meshy_v5_retexture por texto", "meshy_v5_retexture", model_url=URL3D, text_style_prompt="hand painted")
caso("3d", "meshy_v5_retexture por imagen", "meshy_v5_retexture", model_url=URL3D, image_style_url="https://example.com/estilo.png")

# ---------- Audio ----------
for d in (15, 30, 60, 120, 180):
    caso("audio", f"elevenlabs_music_v2_5 {d}s instrumental", "elevenlabs_music_v2_5", prompt=P, duration=d, force_instrumental=True)
    caso("audio", f"sonilo_music {d}s", "sonilo_music", prompt=P, duration=d)
for d in (30, 120):
    caso("audio", f"elevenlabs_music_v2 {d}s", "elevenlabs_music_v2", prompt=P, duration=d)
for d in (1, 3, 5, 10):
    caso("audio", f"mirelo_text_to_audio (SFX) {d}s", "mirelo_text_to_audio", prompt=P, duration=d)
caso("audio", "seed_audio (defecto)", "seed_audio", prompt=P)

# ---------- Video (cinematicas, VFX, fondos animados) ----------
for job in ("seedance_2_0_mini", "seedance1_5", "grok_video_v15_lite", "kling3_0_turbo", "wan3_0", "kling_o3_flf", "veo3_1_lite", "kling4_0", "seedance_2_5"):
    caso("video", f"{job} texto (defecto)", job, prompt=P)
    caso("video", f"{job} imagen->video (defecto)", job, prompt=P, image=IMG)


def main():
    with ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(lambda c: costo(c[2], c[3]), CASOS))
    filas = []
    for (grupo, etiqueta, job, params), (cr, err) in zip(CASOS, res):
        filas.append({"grupo": grupo, "caso": etiqueta, "job_type": job, "params": {k: (v if not isinstance(v, list) else f"{len(v)} refs") for k, v in params.items()}, "creditos": cr, "error": err})
    (SALIDA / "hf_costos_matriz.json").write_text(json.dumps(filas, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# Higgsfield: matriz de costos para arte de videojuego", "",
          "Generado con `herramientas/hf_costos_matriz.py`. Solo `generate cost`: no se creo ningun trabajo ni se gasto ningun credito.",
          "Las cotizaciones con imagen usan un marcador gris; las de `model_url` usan una URL ficticia.", "",
          "| Grupo | Caso | Creditos | Error |", "|---|---|---|---|"]
    ultimo = None
    for f in filas:
        if f["grupo"] != ultimo:
            print(f"\n[{f['grupo']}]")
            ultimo = f["grupo"]
        c = f["creditos"]
        md.append(f"| {f['grupo']} | {f['caso']} | {c if c is not None else '-'} | {f['error'] or ''} |")
        print(f"  {f['caso']:58} {str(c) if c is not None else '-':>7}  {f['error'] or ''}")
    (SALIDA / "hf_costos_matriz.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n{len(filas)} cotizaciones -> {SALIDA}")


if __name__ == "__main__":
    main()
