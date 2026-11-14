# Higgsfield: matriz de costos para arte de videojuego

Generado con `herramientas/hf_costos_matriz.py`. Solo `generate cost`: no se creo ningun trabajo ni se gasto ningun credito.
Las cotizaciones con imagen usan un marcador gris; las de `model_url` usan una URL ficticia.

| Grupo | Caso | Creditos | Error |
|---|---|---|---|
| imagen | gpt_image_2_6 calidad=low 1k | 0.25 |  |
| imagen | gpt_image_2_6 calidad=low 2k | 0.5 |  |
| imagen | gpt_image_2_6 calidad=low 4k | 0.75 |  |
| imagen | gpt_image_2_6 calidad=medium 1k | 0.5 |  |
| imagen | gpt_image_2_6 calidad=medium 2k | 1 |  |
| imagen | gpt_image_2_6 calidad=medium 4k | 1.25 |  |
| imagen | gpt_image_2_6 calidad=high 1k | 1.5 |  |
| imagen | gpt_image_2_6 calidad=high 2k | 2.75 |  |
| imagen | gpt_image_2_6 calidad=high 4k | 4.25 |  |
| imagen | gpt_image_2_6 calidad=xhigh 1k | 2.5 |  |
| imagen | gpt_image_2_6 calidad=xhigh 2k | 4.5 |  |
| imagen | gpt_image_2_6 calidad=xhigh 4k | 7 |  |
| imagen | gpt_image_2_6 calidad=max 1k | 5 |  |
| imagen | gpt_image_2_6 calidad=max 2k | 9 |  |
| imagen | gpt_image_2_6 calidad=max 4k | 15 |  |
| imagen | gpt_image_2_6 high 1k fondo transparente | 1.5 |  |
| imagen | gpt_image_2_6 high 1k con 1 referencia | 1.5 |  |
| imagen | gpt_image_2_6 high 1k con 4 referencias | 1.5 |  |
| imagen | gpt_image_2_6 high 1k lote de 4 | 6 |  |
| imagen | gpt_image_2_6_flare calidad=low 1k | 0.25 |  |
| imagen | gpt_image_2_5 calidad=low 1k | 0.25 |  |
| imagen | gpt_image_2_6_flare calidad=medium 1k | 0.5 |  |
| imagen | gpt_image_2_5 calidad=medium 1k | 0.5 |  |
| imagen | gpt_image_2_6_flare calidad=high 1k | 1.5 |  |
| imagen | gpt_image_2_5 calidad=high 1k | 1.5 |  |
| imagen | nano_banana_pro 1k | 2 |  |
| imagen | nano_banana_flash (NB2) 1k | 1.5 |  |
| imagen | nano_banana_2_1 1k | 1.5 |  |
| imagen | nano_banana_pro 2k | 2 |  |
| imagen | nano_banana_flash (NB2) 2k | 2 |  |
| imagen | nano_banana_2_1 2k | 2 |  |
| imagen | nano_banana_pro 4k | 4 |  |
| imagen | nano_banana_flash (NB2) 4k | 3 |  |
| imagen | nano_banana_2_1 4k | 3 |  |
| imagen | nano_banana_pro 2k con 4 referencias | 2 |  |
| imagen | seedream_5_5 1k | 2.5 |  |
| imagen | 3d_jutsu_angles 1k | 1.25 |  |
| imagen | seedream_5_5 1.5k | 2.5 |  |
| imagen | 3d_jutsu_angles 1.5k | 1.25 |  |
| imagen | seedream_5_5 2k | 3.5 |  |
| imagen | 3d_jutsu_angles 2k | 2.5 |  |
| imagen | 3d_jutsu_angles 2k con 1 referencia | 2.5 |  |
| imagen | seedream_5_5 2k con 4 referencias | 3.5 |  |
| imagen | seedream_v5_pro (defecto) | 2.5 |  |
| imagen | seedream_v5_lite (defecto) | 1 |  |
| imagen | seedream_5_0_flash (defecto) | 0.5 |  |
| imagen | seedream_v4_5 (defecto) | 1 |  |
| imagen | flux_3_image (defecto) | 2 |  |
| imagen | flux_2 (defecto) | 1 |  |
| imagen | flux_kontext (defecto) | 1.5 |  |
| imagen | z_image (defecto) | 0.15 |  |
| imagen | text2image_soul_v2 (defecto) | 0.12 |  |
| imagen | soul_location (defecto) | 0.12 |  |
| imagen | recraft_v4_1 (defecto) | 1.25 |  |
| imagen | ideogram_4_5 (defecto) | 6.25 |  |
| imagen | kling_omni_image (defecto) | 0.5 |  |
| imagen | image_auto (defecto) | 2 |  |
| imagen | nano_banana (defecto) | 1 |  |
| imagen | nano_banana_2_lite (defecto) | 1 |  |
| imagen | grok_image_2_0 (defecto) | 2 |  |
| imagen | minimax_h3_image (defecto) | 4 |  |
| imagen | flux_kontext con 1 referencia | 1.5 |  |
| imagen | ideogram_vector generate calidad=low | 4 |  |
| imagen | ideogram_vector generate calidad=medium | 5 |  |
| imagen | ideogram_vector generate calidad=high | 6.5 |  |
| imagen | ideogram_vector vectorize | 3 |  |
| utilidad | image_background_remover | 1 |  |
| utilidad | bytedance_image_upscale 2k | 2 |  |
| utilidad | bytedance_image_upscale 4k | 2 |  |
| utilidad | topaz_image 2048x2048 | - | Error: job_type 'topaz_image' does not support alpha v2 cost estimation |
| utilidad | topaz_image 4096x4096 | - | Error: job_type 'topaz_image' does not support alpha v2 cost estimation |
| utilidad | nano_banana_2_relight | 2 |  |
| utilidad | nano_banana_2_shots | 4 |  |
| utilidad | outpaint | 2 |  |
| utilidad | flux_2_pro_outpaint | - | Error: at least one expand side must be non-zero | Hint: Run: hf model get flux_2_pro_outpaint |
| autosprite | autosprite iso_walk_down tier=turbo 25f 256px | 2 |  |
| autosprite | autosprite iso_walk_down tier=pro 25f 256px | 3 |  |
| autosprite | autosprite iso_walk_down tier=max 25f 256px | 14 |  |
| autosprite | autosprite idle turbo 25f 256px | 2 |  |
| autosprite | autosprite walk turbo 25f 256px | 2 |  |
| autosprite | autosprite attack turbo 25f 256px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 8f 256px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 12f 256px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 16f 256px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 49f 256px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 25f 128px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 25f 512px | 2 |  |
| autosprite | autosprite iso_walk_down turbo 25f 1024px | 2 |  |
| autosprite | autosprite iso_walk_down turbo remove_bg=ultra | 2 |  |
| autosprite | autosprite custom turbo | 2 |  |
| autosprite | autosprite no humanoide (gato) iso_walk_down turbo | 2 |  |
| 3d | tripo_3d texto (defecto) | 5 |  |
| 3d | tripo_3d texto sin textura | 2.5 |  |
| 3d | tripo_3d texto detallado | 12.5 |  |
| 3d | hunyuan3d_v3_1_text_to_3d std | 7 |  |
| 3d | hunyuan3d_v3_1_text_to_3d pro | 12 |  |
| 3d | meshy_v6_text_to_3d full | 25 |  |
| 3d | meshy_v6_text_to_3d preview | 25 |  |
| 3d | meshy_v6_text_to_3d lowpoly | 25 |  |
| 3d | image_to_3d (defecto: sin textura) | - | Error: job_type 'image_to_3d' does not support alpha v2 cost estimation |
| 3d | image_to_3d con textura | - | Error: job_type 'image_to_3d' does not support alpha v2 cost estimation |
| 3d | image_to_3d textura + remesh | - | Error: job_type 'image_to_3d' does not support alpha v2 cost estimation |
| 3d | image_to_3d textura + rig | - | Error: job_type 'image_to_3d' does not support alpha v2 cost estimation |
| 3d | image_to_3d textura + rig + animacion | - | Error: job_type 'image_to_3d' does not support alpha v2 cost estimation |
| 3d | multi_image_to_3d 4 vistas (defecto) | - | Error: job_type 'multi_image_to_3d' does not support alpha v2 cost estimation |
| 3d | multi_image_to_3d 4 vistas con textura | - | Error: job_type 'multi_image_to_3d' does not support alpha v2 cost estimation |
| 3d | multi_image_to_3d 4 vistas textura + rig | - | Error: job_type 'multi_image_to_3d' does not support alpha v2 cost estimation |
| 3d | meshy_v7_image_to_3d (defecto: textura + remesh) | 38 |  |
| 3d | meshy_v7_image_to_3d lowpoly | 38 |  |
| 3d | meshy_v7_image_to_3d sin textura | 25 |  |
| 3d | meshy_v7_image_to_3d + rig | 44 |  |
| 3d | meshy_v7_image_to_3d + rig + animacion | 47.5 |  |
| 3d | meshy_v7_image_to_3d ultra | 44 |  |
| 3d | hunyuan3d_v3_image_to_3d Normal | 11 |  |
| 3d | hunyuan3d_v3_image_to_3d LowPoly quads | - | Error: face_count: Input should be greater than or equal to 40000 |
| 3d | hunyuan3d_v3_image_to_3d Geometry (sin textura) | 7 |  |
| 3d | hunyuan3d_v3_image_to_3d Normal + PBR | 15 |  |
| 3d | tripo_h3_1_image_to_3d (defecto) | 9 |  |
| 3d | tripo_h3_1_image_to_3d sin textura | 6 |  |
| 3d | tripo_h3_1_image_to_3d quads 8000 caras | 10.5 |  |
| 3d | tripo_h3_1_image_to_3d detallado | 18 |  |
| 3d | tripo_h3_1_multiview_to_3d 4 vistas | 9 |  |
| 3d | tripo_p2_image_to_3d (defecto) | 34 |  |
| 3d | tripo_p2_image_to_3d quads 8000 caras | 34 |  |
| 3d | tripo_p2_image_to_3d textura=fast | 34 |  |
| 3d | tripo_p2_image_to_3d textura=detailed | 37 |  |
| 3d | tripo_p2_image_to_3d textura=extreme | 40 |  |
| 3d | sam_3_3d (objetos desde foto) | - | Error: job_type 'sam_3_3d' does not support alpha v2 cost estimation |
| 3d | sam_3_3d_body | 1 |  |
| 3d | 3d_rigging (solo rig) | - | Error: job_type '3d_rigging' does not support alpha v2 cost estimation |
| 3d | 3d_rigging + animacion | - | Error: job_type '3d_rigging' does not support alpha v2 cost estimation |
| 3d | meshy_v5_remesh quads 8000 | 6 |  |
| 3d | meshy_v5_retexture por texto | 9.5 |  |
| 3d | meshy_v5_retexture por imagen | 9.5 |  |
| audio | elevenlabs_music_v2_5 15s instrumental | 2.18 |  |
| audio | sonilo_music 15s | 0.94 |  |
| audio | elevenlabs_music_v2_5 30s instrumental | 4.36 |  |
| audio | sonilo_music 30s | 1.88 |  |
| audio | elevenlabs_music_v2_5 60s instrumental | 8.72 |  |
| audio | sonilo_music 60s | 3.75 |  |
| audio | elevenlabs_music_v2_5 120s instrumental | 17.44 |  |
| audio | sonilo_music 120s | 7.5 |  |
| audio | elevenlabs_music_v2_5 180s instrumental | 26.16 |  |
| audio | sonilo_music 180s | 11.25 |  |
| audio | elevenlabs_music_v2 30s | 1.92 |  |
| audio | elevenlabs_music_v2 120s | 7.68 |  |
| audio | mirelo_text_to_audio (SFX) 1s | 0.25 |  |
| audio | mirelo_text_to_audio (SFX) 3s | 0.75 |  |
| audio | mirelo_text_to_audio (SFX) 5s | 1.25 |  |
| audio | mirelo_text_to_audio (SFX) 10s | 2.5 |  |
| audio | seed_audio (defecto) | 0.1 |  |
| video | seedance_2_0_mini texto (defecto) | 5 |  |
| video | seedance_2_0_mini imagen->video (defecto) | 5 |  |
| video | seedance1_5 texto (defecto) | 4.8 |  |
| video | seedance1_5 imagen->video (defecto) | 4.8 |  |
| video | grok_video_v15_lite texto (defecto) | 5 |  |
| video | grok_video_v15_lite imagen->video (defecto) | 5 |  |
| video | kling3_0_turbo texto (defecto) | 7.5 |  |
| video | kling3_0_turbo imagen->video (defecto) | 7.5 |  |
| video | wan3_0 texto (defecto) | 8.75 |  |
| video | wan3_0 imagen->video (defecto) | 8.75 |  |
| video | kling_o3_flf texto (defecto) | 6.25 |  |
| video | kling_o3_flf imagen->video (defecto) | 6.25 |  |
| video | veo3_1_lite texto (defecto) | 12 |  |
| video | veo3_1_lite imagen->video (defecto) | 12 |  |
| video | kling4_0 texto (defecto) | 32.5 |  |
| video | kling4_0 imagen->video (defecto) | - | Error: Text-to-video does not accept reference inputs. | Hint: Run: hf model get kling4_0 |
| video | seedance_2_5 texto (defecto) | 35 |  |
| video | seedance_2_5 imagen->video (defecto) | - | Error: mode 't2v' does not accept reference media | Hint: Run: hf model get seedance_2_5 |
