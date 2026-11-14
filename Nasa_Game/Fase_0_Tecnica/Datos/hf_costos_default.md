# Higgsfield: costo por defecto de cada modelo

Generado con `herramientas/hf_catalogo.py` (solo lectura: `model list`, `model get`, `generate cost`).
El costo es el de los parametros por defecto con un prompt de texto; los que exigen imagen o video de entrada figuran con su error.

| Tipo | job_type | Nombre | Creditos (defecto) | Nota |
|---|---|---|---|---|
| 3d | `tripo_3d` | Text to 3D | 5 |  |
| 3d | `hunyuan3d_v3_1_text_to_3d` | Hunyuan 3D v3.1 Text to 3D | 7 |  |
| 3d | `meshy_v6_text_to_3d` | Meshy 6 Text to 3D | 25 |  |
| 3d | `3d_rigging` | 3D Rigging | - | Error: Missing required params: model_url | Unknown params: prompt | Hint: Run: hf model get 3d_rigging |
| 3d | `hunyuan3d_v3_image_to_3d` | Hunyuan3D v3 Image to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get hunyuan3d_v3_image_to_3d |
| 3d | `image_to_3d` | Image to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get image_to_3d |
| 3d | `meshy_v5_remesh` | Meshy 5 Remesh | - | Error: Missing required params: model_url | Unknown params: prompt | Hint: Run: hf model get meshy_v5_remesh |
| 3d | `meshy_v5_retexture` | Meshy 5 Retexture | - | Error: Missing required params: model_url | Unknown params: prompt | Hint: Run: hf model get meshy_v5_retexture |
| 3d | `meshy_v7_image_to_3d` | Meshy 7 Image to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get meshy_v7_image_to_3d |
| 3d | `multi_image_to_3d` | Multi-Image to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get multi_image_to_3d |
| 3d | `sam_3_3d` | 3D Objects | - | Error: Missing required params: image_references | Hint: Run: hf model get sam_3_3d |
| 3d | `sam_3_3d_body` | 3D Body | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get sam_3_3d_body |
| 3d | `tripo_h3_1_image_to_3d` | Tripo H3.1 Image to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get tripo_h3_1_image_to_3d |
| 3d | `tripo_h3_1_multiview_to_3d` | Tripo H3.1 Multiview to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get tripo_h3_1_multiview_to_3d |
| 3d | `tripo_p2_image_to_3d` | Tripo P2 Image to 3D | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get tripo_p2_image_to_3d |
| audio | `seed_audio` | Seed Audio 1.0 | 0.1 |  |
| audio | `elevenlabs_music_v2` | ElevenLabs Music v2 | - | Error: Missing required params: duration | Hint: Run: hf model get elevenlabs_music_v2 |
| audio | `elevenlabs_music_v2_5` | ElevenLabs Music v2.5 | - | Error: Missing required params: duration | Hint: Run: hf model get elevenlabs_music_v2_5 |
| audio | `elevenlabs_v4` | Eleven v4 | - | Error: Missing required params: dialogue | Unknown params: prompt | Hint: Run: hf model get elevenlabs_v4 |
| audio | `elevenlabs_v4_turbo` | Eleven v4 Turbo | - | Error: Missing required params: dialogue | Unknown params: prompt | Hint: Run: hf model get elevenlabs_v4_turbo |
| audio | `inworld_text_to_speech` | Inworld Text to Speech | - | Error: Missing required params: voice | Hint: Run: hf model get inworld_text_to_speech |
| audio | `mirelo_text_to_audio` | Mirelo Text to Audio | - | Error: Missing required params: duration | Hint: Run: hf model get mirelo_text_to_audio |
| audio | `qwen_audio_tts` | Qwen Audio 3.0 TTS Flash | - | Error: Missing required params: voice_id, voice_type | Hint: Run: hf model get qwen_audio_tts |
| audio | `sonilo_music` | Sonilo Music | - | Error: Missing required params: duration | Hint: Run: hf model get sonilo_music |
| audio | `text2speech_v2` | Text to Speech V2 | - | Error: Missing required params: variant, voice_id, voice_type | Hint: Run: hf model get text2speech_v2 |
| data | `clip_transcriber` | Clip Transcriber | - | Error: Unknown params: prompt | Hint: Run: hf model get clip_transcriber |
| data | `image_text_detection` | Image Text Detection | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get image_text_detection |
| data | `speech2text` | Speech to Text | - | Error: Missing required params: audio_references | Unknown params: prompt | Hint: Run: hf model get speech2text |
| image | `soul_cinematic` | Soul Cinematic | 0.12 |  |
| image | `soul_location` | Soul Location | 0.12 |  |
| image | `text2image_soul_v2` | Higgsfield Soul 2.0 | 0.12 |  |
| image | `z_image` | Z Image | 0.15 |  |
| image | `gpt_image_2_5` | GPT Image 2.5 | 0.25 |  |
| image | `gpt_image_2_6` | GPT Image 2.6 | 0.25 |  |
| image | `gpt_image_2_6_flare` | GPT Image 2.6 Flare | 0.25 |  |
| image | `kling_omni_image` | Kling O1 Image | 0.5 |  |
| image | `seedream_5_0_flash` | Seedream 5.0 Flash | 0.5 |  |
| image | `flux_2` | FLUX.2 | 1 |  |
| image | `grok_image` | Grok Image | 1 |  |
| image | `nano_banana` | Nano Banana | 1 |  |
| image | `nano_banana_2_lite` | Nano Banana 2 Lite | 1 |  |
| image | `seedream_v4_5` | Seedream 4.5 | 1 |  |
| image | `seedream_v5_lite` | Seedream 5.0 Lite | 1 |  |
| image | `recraft_v4_1` | Recraft V4.1 | 1.25 |  |
| image | `flux_kontext` | Flux Kontext | 1.5 |  |
| image | `nano_banana_2_1` | Nano Banana 2.1 | 1.5 |  |
| image | `nano_banana_flash` | Nano Banana 2 | 1.5 |  |
| image | `flux_3_image` | FLUX 3 Image | 2 |  |
| image | `grok_image_2_0` | Grok Image 2.0 | 2 |  |
| image | `image_auto` | Image Auto | 2 |  |
| image | `nano_banana_pro` | Nano Banana Pro | 2 |  |
| image | `3d_jutsu_angles` | 3D Jutsu Angles | 2.5 |  |
| image | `seedream_v5_pro` | Seedream 5.0 Pro | 2.5 |  |
| image | `seedream_5_5` | Seedream 5.5 | 3.5 |  |
| image | `minimax_h3_image` | MiniMax H3 Image | 4 |  |
| image | `openai_hazel` | OpenAI Hazel | 4 |  |
| image | `ideogram_4_5` | Ideogram 4.5 | 6.25 |  |
| image | `gpt_image_2` | GPT Image 2 | 6.5 |  |
| image | `autosprite` | AutoSprite Animation | - | Error: Missing required params: image_references | Hint: Run: hf model get autosprite |
| image | `bytedance_image_upscale` | Bytedance Image Upscale | - | Error: Unknown params: prompt | Hint: Run: hf model get bytedance_image_upscale |
| image | `flux_2_pro_outpaint` | FLUX.2 Pro Outpaint | - | Error: Unknown params: prompt | Hint: Run: hf model get flux_2_pro_outpaint |
| image | `ideogram_vector` | Ideogram Vector | - | Error: Missing required params: operation | Hint: Run: hf model get ideogram_vector |
| image | `image_background_remover` | Image Background Remover | - | Error: Unknown params: prompt | Hint: Run: hf model get image_background_remover |
| image | `nano_banana_2_ai_stylist` | Nano Banana Pro | - | Error: Missing required params: image_references | Unknown params: prompt | Hint: Run: hf model get nano_banana_2_ai_stylist |
| image | `nano_banana_2_relight` | Nano Banana Pro | - | Error: Missing required params: brightness, color, image_references, light_quality, light_source | Unknown params: prompt | Hint: Run: hf model get nano_banana_2_relight |
| image | `nano_banana_2_shots` | Nano Banana Pro | - | Error: Unknown params: prompt | Hint: Run: hf model get nano_banana_2_shots |
| image | `nano_banana_2_skin_enhancer` | Nano Banana Pro | - | Error: Missing required params: image_references, preset_id | Unknown params: prompt | Hint: Run: hf model get nano_banana_2_skin_enhancer |
| image | `outpaint` | Outpaint | - | Error: Unknown params: prompt | Hint: Run: hf model get outpaint |
| image | `recraft_v4_styles` | Recraft V4 Styles | - | Error: Missing required params: style_id | Hint: Run: hf model get recraft_v4_styles |
| image | `soul_cast` | Soul Cast | - | Error: Missing required params: aspect_ratio | Hint: Run: hf model get soul_cast |
| image | `topaz_image` | Topaz | - | Error: Missing required params: image_references, output_height, output_width | Unknown params: prompt | Hint: Run: hf model get topaz_image |
| image | `topaz_image_generative` | Topaz | - | Error: Missing required params: image_references, output_height, output_width | Hint: Run: hf model get topaz_image_generative |
| text | `brain_activity` | Brain Activity | - | Error: Unknown params: prompt | Hint: Run: hf model get brain_activity |
| video | `seedance1_5` | Seedance 1.5 Pro | 4.8 |  |
| video | `grok_video_v15_lite` | Grok Imagine Video 1.5 Lite | 5 |  |
| video | `seedance_2_0_mini` | Seedance 2.0 Mini | 5 |  |
| video | `minimax_hailuo` | Minimax Hailuo | 6 |  |
| video | `kling_o3_flf` | Kling 3.0 Omni (Frames) | 6.25 |  |
| video | `kling_o3_image_reference` | Kling 3.0 Omni | 6.25 |  |
| video | `grok_video` | Grok Video | 7.5 |  |
| video | `kling3_0_turbo` | Kling 3.0 Turbo | 7.5 |  |
| video | `wan2_6` | Wan 2.6 Video | 7.5 |  |
| video | `wan2_7` | Wan 2.7 | 7.5 |  |
| video | `wan3_0` | Wan 3.0 | 8.75 |  |
| video | `kling2_6` | Kling 2.6 Video | 10 |  |
| video | `kling3_0` | Kling v3.0 | 10 |  |
| video | `minimax_h3` | MiniMax H3 | 10 |  |
| video | `veo3_1_lite` | Google Veo 3.1 Lite | 12 |  |
| video | `happy_horse_video` | Happy Horse Video | 12.5 |  |
| video | `minimax_h3_max` | MiniMax H3 Max | 12.5 |  |
| video | `wan3_0_prime` | Wan 3.0 Prime | 15 |  |
| video | `grok_video_v15` | Grok Video 1.5 | 22.5 |  |
| video | `seedance_2_0` | Seedance 2.0 | 22.5 |  |
| video | `gemini_omni` | Gemini Omni Flash | 24 |  |
| video | `flux_3_video` | FLUX 3 Video | 30 |  |
| video | `kling_4_0_flash` | Kling 4.0 Flash | 30 |  |
| video | `veo3_1` | Google Veo 3.1 | 32 |  |
| video | `kling4_0` | Kling 4.0 | 32.5 |  |
| video | `ad_multiplier` | Ad Multiplier | 35 |  |
| video | `seedance_2_5` | Seedance 2.5 | 35 |  |
| video | `ad_multiplier_v2` | Ad Multiplier Recreate | - | Error: exactly one video_references entry is required | Hint: Run: hf model get ad_multiplier_v2 |
| video | `bytedance_video_upscale` | Bytedance Video Upscale | - | Error: Missing required params: video_references | Unknown params: prompt | Hint: Run: hf model get bytedance_video_upscale |
| video | `depth_anything_video` | Depth Anything Video | - | Error: Missing required params: video_references | Unknown params: prompt | Hint: Run: hf model get depth_anything_video |
| video | `flux_3_video_edit` | FLUX 3 Video Edit | - | Error: Missing required params: video_references | Hint: Run: hf model get flux_3_video_edit |
| video | `fps_boost` | FPS Boost | - | Error: Missing required params: fps, variant, video_references | Unknown params: prompt | Hint: Run: hf model get fps_boost |
| video | `gemini_omni_flash_1_1` | Gemini Omni Flash 1.1 | - | Error: Missing required params: mode | Hint: Run: hf model get gemini_omni_flash_1_1 |
| video | `gemini_omni_flash_1_2` | Gemini Omni Flash 1.2 | - | Error: Missing required params: mode | Hint: Run: hf model get gemini_omni_flash_1_2 |
| video | `hf_mult_motion_control` | Genjutsu | - | Error: at least one image_references entry is required | exactly one video_references entry is required | Hint: Run: hf model get hf_mult_motion_control |
| video | `hf_mult_motion_control_flash` | Genjutsu Lite | - | Error: at least one image_references entry is required | exactly one video_references entry is required | Hint: Run: hf model get hf_mult_motion_control_flash |
| video | `hf_mult_replace_object` | Genjutsu | - | Error: at least one image_references entry is required | exactly one video_references entry is required | Hint: Run: hf model get hf_mult_replace_object |
| video | `hf_mult_replace_object_flash` | Genjutsu Lite | - | Error: at least one image_references entry is required | exactly one video_references entry is required | Hint: Run: hf model get hf_mult_replace_object_flash |
| video | `intone` | Higgsfield Intone | - | Error: one or two character_images are required | one to six audio_references are required | Hint: Run: hf model get intone |
| video | `kling_video_edit` | Kling 3.0 Omni Edit | - | Error: Missing required params: video_references | Hint: Run: hf model get kling_video_edit |
| video | `sam_3_video` | Remove Background | - | Error: exactly one video_references entry is required | Hint: Run: hf model get sam_3_video |
| video | `topaz_hyperion_2_5` | Topaz Hyperion 2.5 | - | Error: Missing required params: video_references | Unknown params: prompt | Hint: Run: hf model get topaz_hyperion_2_5 |
| video | `topaz_video` | Topaz | - | Error: Missing required params: video_references | Unknown params: prompt | Hint: Run: hf model get topaz_video |
| video | `video_background_remover` | Video Background Remover | - | Error: Unknown params: prompt | Hint: Run: hf model get video_background_remover |
| video | `video_deflicker` | Video Deflicker | - | Error: Missing required params: input_video | Unknown params: prompt | Hint: Run: hf model get video_deflicker |
| video | `video_upscale` | Video Upscale | - | Error: Missing required params: input_video | Unknown params: prompt | Hint: Run: hf model get video_upscale |
