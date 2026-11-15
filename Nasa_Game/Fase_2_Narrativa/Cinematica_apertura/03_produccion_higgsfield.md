# Cinemática de apertura: plan de producción con Higgsfield

> Estado: **propuesta, sin gastar ni un crédito.** Todo lo de aquí se cotizó con `generate cost`, que no crea trabajos. Cada gasto necesita una partida aprobada por Guillermo, anotada en [[trabajos]] antes de generar.
> Fecha: 2026-11-14. Saldo comprobado con `account status`: **868,75 créditos**. Los de suscripción caducan hacia el 2026-12-12 y no hay recarga.
> Va con [[01_hechos_verificados]] (datos y derechos), [[02_lenguaje_visual]] (óptica, luz, color y sonido) y el guion `01_guion` cuando exista. Historia: [[Fase 2 - Analisis]]. Estilo: [[Biblia de arte]].
> Datos crudos: `Datos/cotizaciones_cinematica.json` (233 cotizaciones), más las 30 de este documento hechas a mano.

## 0. En cifras

| Presupuesto | Qué es | Créditos | Parte del saldo |
|---|---|---|---|
| **(a) Borrador** | a0: animatic con 15 fotogramas baratos (5,63). a1: los 13 planos en video barato (144,00) | **149,63** (a0 solo: 5,63) | 17,2 % (a0: 0,6 %) |
| **(b) Final equilibrada** | Fotogramas finos, 2 planos en Seedance 2.5, 10 en MiniMax H3, 1 barato, prueba A/B y escalado a 1080p | **526,38** | 60,6 % |
| **(c) El mejor modelo en todo** | Seedance 2.5 a 1080p nativo en los 13 planos | **2405,25** | 276,9 %: **no cabe** |

- **Recomendación:** a0 (animatic, 5,63) → validar ritmo con Guillermo → (b). Juntos suman **532,00** (61,2 %) y dejan **336,75** para el resto del juego. El borrador en video (a1) se omite: el animatic valida el ritmo y la prueba A/B valida el movimiento.
- Ni (c) a 720p con escalado cabe: **1135,25** (130,7 %). El techo de calidad lo pone el saldo.
- Mejora opcional (b+): la huella (P11), el clímax, también en Seedance 2.5: **+75,00**, total **601,38** (69,2 %).

## 1. Modelos de video disponibles hoy

Lista viva: `model list --json` da 45 modelos de video (118 en total) y `model get` sus parámetros. Cinema Studio 4.0 y 3.0 no salen en la lista, pero `model get` los devuelve. `seedance1_5` ya no existe («No model with job_type»).

**Elo:** tabla de imagen a video con audio de Artificial Analysis, consultada el 2026-11-14 (votos ciegos; la página no muestra fecha; [fuente](https://artificialanalysis.ai/video/leaderboard/image-to-video)). Kling 3.0 Pro es el punto de anclaje (1000).

| Modelo (`job_type`) | Duración | Resolución | Aspecto | Fotogramas | Referencias y modos | Audio nativo | Elo |
|---|---|---|---|---|---|---|---|
| Seedance 2.5 (`seedance_2_5`) | 4 a 30 s | 480p, 720p, 1080p | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | inicial y final (solo en `omni_reference`) | hasta 30 imágenes, video y audio; edición y extensión; `draft` | `generate_audio`, sí por defecto | **1161 (1.º)** |
| Cinema Studio 4.0 (`cinematic_studio_video_4_0`) | sin verificar (cotiza de 4 a 12 s) | 480p, 720p, 1080p | igual que Seedance 2.5 | inicial y final (`omni_reference`) | los mismos modos, más cámara, lente, diafragma, época, género, ritmo, luz y paleta | sí por defecto | no figura |
| Cinema Studio 3.0 (`cinematic_studio_3_0`) | sin verificar | hasta 4K según el catálogo | — | inicial | — | — | no figura |
| Seedance 2.0 (`seedance_2_0`) | 4 a 15 s | 480p a 4K | 7 relaciones, con 21:9 | inicial y final | hasta 9 imágenes, 3 videos, 3 audios; `genre`; modo `fast` (≤720p) | sí | 1141 |
| Seedance 2.0 Mini (`seedance_2_0_mini`) | cotiza de 5 a 12 s | 480p, 720p | 7, con 21:9 | inicial y final | como 2.0 | sí | no figura |
| MiniMax H3 (`minimax_h3`) | cotiza de 4 a 12 s | «2K» (única opción) | 7, con 21:9 | inicial y final (sin mezclar con referencias) | imágenes, video y audio de referencia | sin verificar | 1134 (la tabla dice «768p») |
| MiniMax H3 Max (`minimax_h3_max`) | cotiza de 5 a 12 s | 480p, 768p | 7 | inicial y final | hasta 12 referencias | sin verificar | 1116 |
| Wan 3.0 / Prime (`wan3_0`, `wan3_0_prime`) | 2 a 30 s | 480p, 720p, 1080p | 6 | inicial y final | referencias; `enable_thinking` | sí | 1109 (3.0) |
| Gemini Omni Flash 1.2 (`gemini_omni_flash_1_2`) | 8 s por defecto; con fotogramas, ≤10 s | 360p a 4K | 16:9, 9:16 | inicial y final (`image-to-video`) | referencias, edición y extensión | sin verificar | 1085 |
| FLUX 3 Video (`flux_3_video`) | cotiza de 5 a 12 s | 720p, 1080p, 2K, 4K | 8, con 21:9 | inicial y final | hasta 10 imágenes o videos | sí | 1069 |
| Grok Video 1.5 (`grok_video_v15`) | 2 a 15 s | 480p, 720p, 1080p (1080p sin referencias) | — | inicial | o referencias | audio de referencia | 1047 |
| Happy Horse (`happy_horse_video`) | cotiza de 5 a 12 s | 720p, 1080p | 5 | inicial | — | — | 1035 (1.1) |
| Kling 3.0 (`kling3_0`) | 3 a 15 s | `std`, `pro`, `4k` | 16:9, 9:16, 1:1 | inicial y final | — | `sound` on/off | 1000 |
| Kling 3.0 Omni Frames (`kling_o3_flf`) | 3 a 15 s | `std`, `pro`, `4k` | 3 | inicial y final | varios planos (`multi_shots`) | `sound` | 1004 (Omni Pro) |
| Kling 4.0 (`kling4_0`) | 10 s por defecto | 720p, 1080p | 5, con 21:9 | inicial y final | referencias, elementos, edición | sin parámetro | no figura |
| Kling 4.0 Flash (`kling_4_0_flash`) | 10 s por defecto | 720p | 5 | inicial | referencias | sin parámetro | no figura |
| Kling 3.0 Turbo (`kling3_0_turbo`) | 3 a 15 s | 720p, 1080p | 3 | inicial | — | — | no figura |
| Kling 2.6 (`kling2_6`) | 5 o 10 s | — | 3 | inicial | — | `sound` | no figura |
| Veo 3.1 (`veo3_1`) | 4, 6 u 8 s | sin parámetro (sin verificar) | 16:9, 9:16 | inicial | — | sin parámetro (sin verificar) | 955 (Fast: 935) |
| Veo 3.1 Lite (`veo3_1_lite`) | 4, 6 u 8 s (8 con dos fotogramas) | — | 16:9, 9:16 | inicial y final | — | `generate_audio`, no por defecto | ~1063 en un espejo; sin verificar |
| Hailuo (`minimax_hailuo`) | 6 o 10 s | 512, 768, 1080 (1080 solo a 6 s) | — | inicial (final solo en variantes viejas) | — | no | no figura |

Utilidades de video: `bytedance_video_upscale` (1080p, 2K, 4K; preset `old_film`), `topaz_video`, `topaz_hyperion_2_5`, `fps_boost`, `video_deflicker`, `video_upscale`, `video_background_remover`.

## 2. Cotizaciones por plano, con fotograma inicial

Créditos por plano. Cotizado el 2026-11-14 con el marcador gris ya subido (`dcfc3212…`) como fotograma inicial.

| Modelo | 720p: 5 / 8 / 10 / 12 s | 1080p: 5 / 8 / 10 / 12 s | Por segundo (720p / 1080p) |
|---|---|---|---|
| Seedance 2.5 | 35 / 56 / 70 / 84 | 80 / 128 / 160 / 192 | 7 / 16 (480p: 3) |
| Cinema Studio 4.0 | 35 / 56 / 70 / 84 | 80 / 128 / 160 / 192 | 7 / 16 (480p: 3) |
| Cinema Studio 3.0 | — | 65 / 104 / 130 / 156 | — / 13 |
| Seedance 2.0 | 22,5 / 36 / 45 / 54 | 60 / 96 / 120 / 144 | 4,5 / 12 (4K: 22) |
| Seedance 2.0 `fast` | 12,5 / 20 / 25 / 30 | no admite | 2,5 |
| Seedance 2.0 Mini | 5 / 8 / 10 / 12 | no admite | 1 |
| MiniMax H3 («2K») | 10 / 16 / 20 / 24 | (la misma) | 2 |
| MiniMax H3 Max (768p) | 12,5 / 20 / 25 / 30 | — | 2,5 |
| Wan 3.0 | 8,75 / 14 / 17,5 / 21 | 17,5 / 28 / 35 / 42 | 1,75 / 3,5 |
| Wan 3.0 Prime | 15 / 24 / 30 / 36 | 30 / 48 / 60 / 72 | 3 / 6 |
| Wan 2.7 | 7,5 / 12 / 15 / 18 | 12,5 / 20 / 25 / 30 | 1,5 / 2,5 |
| Gemini Omni Flash 1.2 | 11,25 / 18 / 22,5 / 27* | 16,25 / 26 / 32,5 / 39* | 2,25 / 3,25 (4K: 6,75) |
| FLUX 3 Video | 30 / 48 / 60 / 72 | 40 / 64 / 80 / 96 | 6 / 8 (4K: 13) |
| Grok Video 1.5 | 22,5 / 36 / 45 / 54 | 40 / 64 / 80 / 96 | 4,5 / 8 |
| Happy Horse | 12,5 / 20 / 25 / 30 | 22,5 / 36 / 45 / 54 | 2,5 / 4,5 |
| Kling 4.0 | 11,25 / 18 / 22,5 / 27 | 16,25 / 26 / 32,5 / 39 | 2,25 / 3,25 |
| Kling 4.0 Flash | 15 / 24 / 30 / 36 | no admite | 3 |
| Kling 3.0 `std` / `pro` / `4k` | 10 / 16 / 20 / 24 · 12,5 / 20 / 25 / 30 · 30 / 48 / 60 / 72 | — | 2 / 2,5 / 6 |
| Kling 3.0 Omni Frames `std` / `pro` | 6,25 / 10 / 12,5 / 15 · 9 / 14,4 / 18 / 21,6 | — | 1,25 / 1,8 |
| Kling 3.0 Turbo | 7,5 / 12 / 15 / 18 | 8 s: 16 | 1,5 / 2 |
| Kling 2.6 | 5 s: 10 · 10 s: 20 | — | 2 |
| Veo 3.1 (4 / 6 / 8 s) | `fast` basic o high: 16 / 24 / 32 · `fast` ultra: 36 / 54 / 72 · `preview` basic o high: 40 / 60 / 80 · `preview` ultra: 60 / 90 / 120 | — | 4 / 9 / 10 / 15 |
| Veo 3.1 Lite (4 / 6 / 8 s) | 6 / 9 / 12 | — | 1,5 |
| Hailuo 2.3 (768, 6 s) | 6 | — | 1 |

\* Gemini acepta la cotización de 12 s, pero su regla limita a 10 s los planos con fotogramas: fallaría al crear el trabajo.

**Lo que no cambia el precio** (comprobado): quitar el audio en Seedance 2.5 y Cinema Studio 4.0 (56 con y sin audio); el `bitrate_mode` alto (128); añadir el fotograma final (56); pasar 3 imágenes de referencia (56). En Kling 3.0 apagar el sonido sí abarata: `std` de 8 s, de 16 a 12; `pro`, de 20 a 14.

**Otros modos y utilidades** (con un clip gris de 5 s a 720p subido como marcador; subir no gasta):

| Operación | Créditos |
|---|---|
| Seedance 2.5 `draft` (8 s; sale a precio de 480p) | 24 |
| Seedance 2.5 final desde un `draft_job_id` (cotizado con un id ficticio, 8 s, 1080p) | 128: el borrador no abarata el final (sin verificar con un borrador real) |
| Seedance 2.5 extender 5 s / editar 5 s (720p) | 35 / 38 |
| Escalar a 1080p, `bytedance_video_upscale` estándar / pro (clip de 5 s) | **1** / 10 |
| Escalar a 4K, estándar (clip de 5 s) | 4 |
| Subir a 48 fps, `fps_boost` bytedance / topaz (clip de 5 s) | 20 / 17 |
| `topaz_video` | no se puede cotizar («does not support alpha v2 cost estimation») |

Conclusión de precio: **generar a 720p y escalar cuesta 7 + 0,2 créditos por segundo; el 1080p nativo, 16.** Falta comprobar si el escalado sube con la duración (solo se cotizó un clip de 5 s) y si su calidad iguala al nativo.

## 3. Fotogramas clave (imagen fija)

Cada plano nace de un fotograma aprobado ([[02_lenguaje_visual]] §6).

| Modelo | Opción | Créditos |
|---|---|---|
| `gpt_image_2_6` | low 1k (borrador) | 0,25 |
| `gpt_image_2_6` | medium 1k / 2k | 0,5 / 1 |
| `gpt_image_2_6` | high 1k / **2k** (final) | 1,5 / **2,75** |
| `gpt_image_2_6` | xhigh 2k (primeros planos de la niña) | 4,5 |
| `nano_banana_pro` | 2k con referencias | 2 |
| `seedream_5_5` | 2k | 3,5 |
| `soul_cinematic` | 2k, 21:9 (estética de cine; deriva del estilo) | 0,12 |

- Las referencias no cambian el costo (`gpt_image_2_6` acepta hasta 16).
- GPT Image 2.6 es el modelo que mejor siguió la dirección de arte en el lote 01 ([[Memory]]). `soul_cinematic` a 0,12 sirve para explorar la luz y el encuadre, no para la niña.
- **Referencias:** las anclas ya subidas se citan como `@ANC_…` (`Fase_1_Arte/anclas.json`): `@ANC_PROTA_1` (hoja de la protagonista), `@ANC_GATO` y `@ANC_EXPLORACION` (estilo). Falta subir, gratis con `herramientas/hf_anclas.py`, el concepto de la habitación `L05_A_manana_calida_final.png` (`@ANC_HABITACION`, para P01 y la luz de la mañana) y una captura del motor del encuadre inicial.
- **La niña:** si el guion elige a la protagonista de hoy, basta `@ANC_PROTA_1` en cada fotograma. Si elige a la protagonista de pequeña, hace falta antes una hoja nueva de ella a los 8 a 10 años (borrador 0,25 y final 2,75, unos 4,50 con reintentos). Sus tres primeros planos se generan en una sola tanda y se aprueban como set.
- **Texto fijo** de cada encargo: `{SIN_TEXTO}` y, además, «no insignia, no patches, no flags on suits, no letters on the rocket, no real faces». Después, revisión ampliada de cada fotograma.

**Lote de fotogramas** (mismo formato que `Exploracion/Lote_07/lote_07a_borradores.json`; carpeta propuesta `Fase_2_Narrativa/Cinematica_apertura/Lote_CIN01/`):

```json
{"lote": "CIN01a", "carpeta": "Nasa_Game/Fase_2_Narrativa/Cinematica_apertura/Lote_CIN01", "tope": 6.0,
 "trabajos": [
  {"id": "CIN01_P15_despertar_borrador", "modelo": "gpt_image_2_6",
   "params": {"aspect_ratio": "16:9", "resolution": "1k", "quality": "low"},
   "imagenes": ["@ANC_PROTA_1", "@ANC_HABITACION"],
   "prompt": "Extreme close-up, 85 mm lens, shallow depth of field, focus on the near eye... {SIN_TEXTO}"}]}
```

`python herramientas/hf_generar.py <lote.json> --solo-cotizar` cotiza y frena si el lote pasa el tope.

**Lote de video:** `hf_generar.py` sirve sin tocarlo si el fotograma va en `params` con su id de subida (sale `--start-image <id>`): `"params": {"mode": "omni_reference", "start-image": "<id>", "duration": 8, "resolution": "720p", "generate_audio": false}`. Hay dos límites que conviene arreglar antes de la partida (no se tocaron en esta tarea):
1. las `@ANC` no se resuelven dentro de `params`;
2. la espera es de 15 minutos, poca para un video de 1080p: subirla a 30.

## 4. Música y sonido

| Modelo | Uso | Créditos |
|---|---|---|
| `elevenlabs_music_v2_5` instrumental | música | 10 s 1,46 · 60 s 8,72 · 120 s 17,44 (0,145/s) |
| `elevenlabs_music_v2` | música | 30 s 1,92 · 120 s 7,68 (0,064/s) |
| `sonilo_music` | música | 30 s 1,88 · 120 s 7,50 (0,0625/s) |
| `mirelo_text_to_audio` | efectos | 1 s 0,25 · 30 s 7,50 (0,25/s) |
| `seed_audio` | efectos, ambiente, voz | 0,10 por generación (no tiene duración; la longitud que entrega está sin verificar) |
| Audio nativo del video | — | gratis, pero viene pegado al plano y puede traer música o voces |

**Licencias: sin verificar para publicar.**
- Los términos de Higgsfield permiten el uso comercial (apartado 4.4), pero remiten a las condiciones más restrictivas de cada proveedor (apartado 8) ([[Memory]], §3).
- Ejemplo concreto: los términos de Eleven Music (actualizados el 09-10-2026, [fuente](https://elevenlabs.io/eleven-music-model-specific-terms)) excluyen las «Studio Games» en todos los planes de autoservicio. Solo se salvan los juegos indie: menos de 500 000 USD de ingresos del juego y menos de 1 000 000 USD del estudio en el último año. No consta qué plan de ElevenLabs aplica a lo generado a través de Higgsfield.
- De Sonilo, Mirelo, Seed Audio y el audio nativo de Seedance o MiniMax no se revisaron los términos.

**Recomendación:** generar el video con `generate_audio: false` (cuesta lo mismo; en Kling, `sound: off` abarata) y montar el sonido aparte. Alternativas sin riesgo de licencia:
1. **Música:** composición propia o por encargo con cesión de derechos por escrito. El tema es de pocas notas (piano o cuerdas graves, [[02_lenguaje_visual]] §5): cabe hacerlo en un secuenciador gratuito.
2. **Ambiente de la mañana grabado en Guayaquil:** pájaros, un bus lejano, el ventilador, un gato ronroneando. Son auténticos, gratis y propios.
3. **Efectos CC0** de bibliotecas públicas: cada descarga necesita el permiso de Guillermo (nombre, fuente y tamaño).
4. **Audio de 1969:** los medios de NASA en general no tienen derechos de autor en EE. UU. ([NASA, guía de uso](https://www.nasa.gov/nasa-brand-center/images-and-media/)), pero las voces son de personas identificables: uso comercial con consulta legal ([[01_hechos_verificados]] §6). Las fuentes están listadas ahí. **No se descargó nada.** La llamada presidencial no se usa.
5. **Música generada solo como maqueta** del animatic (Sonilo, 120 s = 7,50), nunca en la versión publicada mientras la licencia siga sin verificar.

## 5. Presupuestos

### 5.1 Desglose de planos para presupuestar

16 planos, unos 105 s montados. 13 se generan en video (96 s); P07 y P13 son imágenes fijas con movimiento lento hecho con ffmpeg, y P16 sale del motor. Los nombres siguen la estructura de [[02_lenguaje_visual]] §4; el guion puede cambiarlos.

| # | Plano | Tipo | s generados | s montados |
|---|---|---|---|---|
| P01 | Habitación de noche: la niña ante el televisor (35 mm) | niña | 8 | 7 |
| P02 | Sus ojos iluminados por el tubo (100 mm) | niña, primer plano | 6 | 5 |
| P03 | En la pantalla, el cohete en la plataforma (blanco y negro, 4:3, compuesto en el mueble) | televisor | 8 | 7 |
| P04 | Empuje al televisor y entrada al sueño (inicial: P03 compuesto; final: el fotograma de P05) | transición | 6 | 5 |
| P05 | Ignición vista de lejos (teleobjetivo largo) | fuego y humo | 8 | 8 |
| P06 | Columna de humo y el cohete diminuto en un cielo enorme | humo | 8 | 7 |
| P07 | Salida de la atmósfera, en silencio | imagen fija animada | 0 | 5 |
| P08 | La Tierra que se aleja, entera | espacio | 8 | 7 |
| P09 | Descenso sobre el gris | Luna | 8 | 7 |
| P10 | El polvo que se aquieta y las patas | Luna | 6 | 5 |
| P11 | La bota y la huella (macro de 100 mm), el clímax | Luna | 10 | 9 |
| P12 | La bandera en su barra horizontal | Luna | 6 | 6 |
| P13 | La Tierra en el cielo lunar; el Sol quema a blanco | imagen fija animada | 0 | 6 |
| P14 | Del blanco a su rostro dormido | niña, primer plano | 6 | 5 |
| P15 | Abre los ojos: la lágrima y la sonrisa (85 mm) | niña, primer plano | 8 | 8 |
| P16 | Corte en el pestañeo al encuadre del juego; se incorpora; Órbita la mira | motor | 0 | 6 |
| | **Total** | | **96** | **103** (+2 de negro y rótulo) |

Fotogramas: 15. Son 12 iniciales de video (P04 reutiliza los de P03 y P05), P07, P13 y la placa frontal del televisor para componer P03. Intentos previstos: 1,5 por plano y por fotograma.

### 5.2 (a) Borrador completo para validar el ritmo: 149,63

| Partida | Cálculo | Generaciones | Créditos |
|---|---|---|---|
| a0: fotogramas `gpt_image_2_6` low 1k | 15 × 1,5 × 0,25 | 22,5 | 5,63 |
| a0: animatic con ffmpeg (empujes sobre fijas y sonido de maqueta propio) | — | — | 0 |
| a1: video `seedance_2_0_mini` 720p, con fotograma inicial y final | 96 s × 1 × 1,5 | 19,5 | 144,00 |
| **Total** | | **42** | **149,63** (17,2 %; a0 solo, 0,6 %) |

### 5.3 (b) Versión final equilibrada: 526,38

| Partida | Modelo | Cálculo | Generaciones | Créditos |
|---|---|---|---|---|
| Fotogramas de la niña (P01, P02, P14, P15) | `gpt_image_2_6` xhigh 2k | 4 × 1,5 × 4,5 | 6 | 27,00 |
| Resto de fotogramas | `gpt_image_2_6` high 2k | 11 × 1,5 × 2,75 | 16,5 | 45,38 |
| Prueba A/B en P15, 4 s: Seedance 2.5 480p (12), Cinema Studio 4.0 480p (12) y MiniMax H3 (8) | varios | 12 + 12 + 8 | 3 | 32,00 |
| Planos héroe: P05 (ignición) y P15 (lágrima) | `seedance_2_5` 720p (o el ganador de la A/B) | 16 s × 7 × 1,5 | 3 | 168,00 |
| P01, P02, P04, P06, P08, P09, P10, P11, P12 y P14 | `minimax_h3` | 72 s × 2 × 1,5 | 15 | 216,00 |
| P03, el televisor (se degrada a propósito) | `seedance_2_0_mini` 720p | 8 s × 1 × 1,5 | 1,5 | 12,00 |
| Escalado a 1080p de 12 clips, más uno de reserva | `bytedance_video_upscale` estándar | tope de 13 × 2 (sin verificar) | 13 | 26,00 |
| **Total** | | | **58** | **526,38** (60,6 %) |

- Con efectos de Mirelo (40 s × 1,5 × 0,25 = 15,00): 541,38. No se recomienda mientras su licencia siga sin verificar (§4).
- (b+) con P11 en Seedance 2.5 (10 s × 7 × 1,5 = 105, en vez de 30): **601,38** (69,2 %).

### 5.4 (c) El mejor modelo en todos los planos: 2405,25 (no cabe)

| Partida | Cálculo | Generaciones | Créditos |
|---|---|---|---|
| Fotogramas `gpt_image_2_6` xhigh 2k | 15 × 1,5 × 4,5 | 22,5 | 101,25 |
| Video `seedance_2_5` 1080p nativo | 96 s × 16 × 1,5 | 19,5 | 2304,00 |
| **Total** | | **42** | **2405,25** (276,9 %) |

- Variante (c′): Seedance 2.5 a 720p más escalado, 96 × 7 × 1,5 + 101,25 + 26 = **1135,25** (130,7 %). Tampoco cabe.
- Ni con un solo intento por plano (672 + 101,25 + 26 = 799,25, el 92 %) es prudente: no queda margen para un fallo.

## 6. Posproducción e integración (sin créditos)

**Flujo:** clips limpios → recorte y normalización → empujes de las fijas → composición del televisor → transiciones → máster de 1080p y 24 fps → mezcla estéreo → `.ogv` → filtros de época y subtítulos en el motor.

```bash
# 1. Recortar y normalizar cada plano (24 fps, 1920x1080, sin audio)
ffmpeg -ss 0.4 -t 7 -i P05_final.mp4 -vf "fps=24,scale=1920:1080:flags=lanczos,setsar=1" -an -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p cortes/P05.mp4
# 2. Imagen fija con empuje lento (P07, P13)
ffmpeg -loop 1 -framerate 24 -i P07.png -vf "scale=3840:-2,zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1920x1080:fps=24" -t 5 -c:v libx264 -crf 12 -pix_fmt yuv420p cortes/P07.mp4
# 3. Televisor (P03): 10 fps con estela (camara lunar de barrido lento), blanco y negro, 4:3, sobre la placa del mueble
ffmpeg -i P03.mp4 -i placa_tv.png -filter_complex "[0:v]fps=10,tmix=frames=3:weights='1 0.5 0.25',fps=24,hue=s=0,curves=preset=increase_contrast,scale=960:720,vignette=PI/5[tv];[1:v][tv]overlay=x=480:y=180[v]" -map "[v]" -c:v libx264 -crf 12 cortes/P03.mp4
# 4. Transiciones: quemar a blanco (P13 -> P14) y disolver por forma
ffmpeg -i cortes/P13.mp4 -i cortes/P14.mp4 -filter_complex "xfade=transition=fadewhite:duration=1.5:offset=4.5" -c:v libx264 -crf 12 cortes/P13_P14.mp4
# 5. Unir (lista.txt con: file 'cortes/P01.mp4' ...)
ffmpeg -f concat -safe 0 -i lista.txt -c copy master_1080p.mp4
# 6. Mezcla estereo a -16 LUFS
ffmpeg -i musica.wav -i efectos.wav -i ambiente.wav -filter_complex "amix=inputs=3:normalize=0,loudnorm=I=-16:TP=-1:LRA=11" -ar 48000 mezcla.wav
# 7. Ogg Theora para Godot (receta de la documentacion oficial)
ffmpeg -i master_1080p.mp4 -i mezcla.wav -map 0:v -map 1:a -c:v libtheora -q:v 6 -g:v 64 -c:a libvorbis -q:a 6 -ac 2 cinematica_apertura.ogv
# variante de 720p
ffmpeg -i master_1080p.mp4 -i mezcla.wav -map 0:v -map 1:a -vf "scale=-2:720" -c:v libtheora -q:v 6 -g:v 64 -c:a libvorbis -q:a 6 -ac 2 cinematica_apertura_720p.ogv
```

Los coeficientes (posición del 4:3 en la placa, viñeta, contraste) son valores de partida: se ajustan con el storyboard. La curvatura del tubo se hace mejor en el shader.

**Reproducción en Godot 4.7** ([documentación oficial, «Playing videos»](https://docs.godotengine.org/en/stable/tutorials/animation/playing_videos.html), página de la 4.7):
- El núcleo solo reproduce **Ogg Theora (`.ogv`)**, con audio Vorbis opcional, en un `VideoStreamPlayer`. WebM se quitó en la 4.0; H.264 y H.265 no entran por patentes.
- La documentación dice que una extensión puede añadir otros formatos, pero no nombra ninguna: queda **sin verificar** para la 4.7.2.
- Recomienda 1080p como máximo y preferiblemente 30 fps en escritorio, y 720p en móvil o web. Decodifica en la CPU, solo en mono o estéreo (el 5.1 se reduce a estéreo), y no reproduce desde una URL.
- El ffmpeg 9.0.2 instalado trae `libtheora` y `libvorbis` (comprobado).

**Medición propia** (2026-11-14): 10 s del concepto L05 con un empuje lento, codificados con `-q:v 6 -g:v 64`. La decodificación se midió con ffmpeg en un solo hilo del i5-7200U, como aproximación al motor.

| Versión | Tamaño de 10 s | MB/s | Decodificar 10 s |
|---|---|---|---|
| 1080p limpio | 9,7 MB | 0,97 | 2,6 s (3,9 veces el tiempo real) |
| 1080p con grano horneado | 69,3 MB | 6,93 | 8,1 s (1,2 veces: al límite) |
| 720p limpio | 5,0 MB | 0,50 | 1,2 s (8,5 veces) |
| 720p con grano horneado | 34,2 MB | 3,42 | 3,0 s |

- **El grano, la nieve y las líneas de barrido van en un shader del motor, nunca horneados:** el grano multiplica el archivo por 7 y triplica el costo de decodificar.
- Se hornean solo la geometría y el tiempo: la estela de 10 fps, el 4:3 dentro del mueble y los fundidos.
- **Tamaño estimado** de la cinemática de unos 105 s: 1080p limpio, unos 100 MB con la textura de la prueba. Con el movimiento real de un video generado, de 150 a 250 MB (el factor de 1,5 a 2,5 es una estimación, sin verificar). A 720p, de 80 a 130 MB. Audio Vorbis q6, unos 2,5 MB. Va al repositorio con Git LFS.
- **Integración** (para una tarea de `juego/`; aquí no se tocó):
  - «Nueva partida» → escena de la cinemática con un `VideoStreamPlayer` a pantalla completa (`expand` dentro de un `AspectRatioContainer` de 16:9) y un `ShaderMaterial` con el tubo y el grano de 16 mm, según el tramo.
  - Los subtítulos y rótulos son `Label` del motor, sincronizados con `stream_position` y leídos de un JSON con tiempos.
  - Mantener Esc 1 s salta la cinemática. Al terminar se pasa a la Habitación con el fundido de estilo de [[02_lenguaje_visual]] §7.
  - Falta comprobar que un `ShaderMaterial` aplicado al `VideoStreamPlayer` funciona en la 4.7.2; si no, se usa su textura en un `TextureRect`.
  - Falta medir los fps en el motor con el `.ogv` real.

## 7. Recomendación por tipo de plano

| Tipo de plano | Modelo | Por qué |
|---|---|---|
| **Despegue con fuego y humo** (P05) | Seedance 2.5 a 720p y escalado, o Cinema Studio 4.0 si gana la A/B | 1.º en la tabla de Artificial Analysis con audio (1161) y 2.º sin audio (1128). El catálogo de Higgsfield lo da como «SOTA… serious motion, cinematic». El grano de 16 mm del sueño disimula la diferencia entre 720p y 1080p. |
| Humo y cielo (P06), espacio (P08) | MiniMax H3 | 4.º con audio (1134) a 2 créditos por segundo, 3,5 veces más barato que Seedance 2.5. Son planos de un solo movimiento lento. |
| **Superficie lunar** (P09, P10, P12) | MiniMax H3 | Planos casi quietos, polvo que se asienta y paisaje. Sin pasos: la baja gravedad es un fallo conocido de estos modelos ([[02_lenguaje_visual]] §6). |
| La huella (P11), el clímax | MiniMax H3 en (b); Seedance 2.5 en (b+) | El macro casi quieto no exige mucho al modelo; el +75 se gasta solo si la A/B muestra una diferencia clara. |
| **Primer plano de la niña** (P15, y P02 y P14) | P15: Seedance 2.5 o Cinema Studio 4.0, según la A/B, con `@ANC_PROTA_1` además del fotograma inicial. P02 y P14: MiniMax H3 | La lágrima es el plano que decide la emoción y el riesgo de deformar la cara es máximo. Seedance 2.5 admite hasta 30 imágenes de referencia junto al fotograma inicial para sostener la identidad. P02 y P14 son casi fijos. |
| **Televisor** (P03) | Seedance 2.0 Mini (1 crédito por segundo) | El blanco y negro, los 10 fps, la estela y el tubo destruyen el detalle a propósito: pagar calidad ahí no se nota. Alternativa: película de archivo del lanzamiento sin personas (NARA y NASA, [[01_hechos_verificados]] §6), con permiso de descarga. |
| Transición al sueño (P04) | MiniMax H3 con fotograma inicial y final (8 s = 16, cotizado) | Fija los dos extremos. Kling 3.0 Omni Frames (1,25 a 1,8 por segundo) es la alternativa, pero puntúa 1004, contra 1134. |
| Fijas animadas (P07, P13) | `gpt_image_2_6` high 2k y ffmpeg | Son planos de contemplación: un empuje del 2 al 5 % del cuadro por segundo basta, sin gastar en video. |
| Despertar en la habitación (P16) | El motor | Su último plano es el primero del juego: con la misma luz y la misma cámara, la costura no se ve. |

**Por qué no los demás:**
- Veo 3.1 queda en 955 y cobra de 4 a 15 créditos por segundo.
- FLUX 3 Video cobra de 6 a 8 por segundo y queda en 1069.
- Seedance 2.0 a 1080p cobra 12 por segundo, por debajo de Seedance 2.5 en la tabla.
- Seedance 2.0 en 4K (22 por segundo) solo se justificaría si se pidiera 4K.

**Lo que no se pudo comprobar:**
- **La calidad real de ningún modelo con este estilo:** no se generó nada. La tabla Elo mide preferencias generales con otros encargos, no la estética de 16 mm ni el pintado del juego. La prueba A/B de 32 créditos existe para eso.
- **Cinema Studio 4.0:**
  - no está en la tabla Elo;
  - comparte precios y modos con Seedance 2.5, pero que esté construido sobre él es una suposición;
  - sus identificadores de cámara, lente, época y género no se pueden listar desde el CLI (`preset list` no tiene ese tipo).
- **MiniMax H3:** su parámetro dice «2K», pero la tabla Elo lo lista como «768p». Falta saber qué resolución entrega de verdad.
- **Escalado:** solo se cotizó un clip de 5 s (1 crédito). Falta saber cuánto cobra por segundo y cómo queda frente al 1080p nativo.
- **`draft_job_id`:** el final cotizó a precio completo con un id ficticio. Falta saber si el final reproduce el borrador.
- **Veo 3.1:** no se sabe qué resolución entrega ni si trae audio, porque no tiene esos parámetros.
- **Duraciones máximas** de MiniMax H3, Kling 4.0, FLUX 3 Video y Cinema Studio 4.0.
- **Hailuo:** el CLI convierte «768» en número y rechaza la cotización con esa resolución. Solo se cotizó la variante 2.3 por defecto: 6 s, 6 créditos.
- **Licencias de audio** a través de Higgsfield; los derechos de voz e imagen del audio de 1969.
- **Rendimiento en el motor:** solo se midió con ffmpeg. Tampoco se probó el shader sobre el `VideoStreamPlayer`.

## 8. Partidas a aprobar, en orden

Cada etapa se presenta con su evidencia y espera el visto bueno de Guillermo antes de la siguiente.

1. **Guion y storyboard** validados (`01_guion`, [[02_lenguaje_visual]]): 0 créditos.
2. **Fotogramas de borrador y animatic** (CIN01a): tope de **6,00**. Valida ritmo, encuadres y la niña.
3. **Fotogramas finales** (CIN01b): **72,38**, tope de 80. Los tres primeros planos de la niña se aprueban como set.
4. **Prueba A/B** del despertar (P15): **32,00**. Elige el modelo de los planos héroe.
5. **Video final por movimientos** (I, II y III), con validación tras cada uno: **396,00**, tope de 420 (168 + 216 + 12).
6. **Escalado:** tope de **26,00**. Montaje, mezcla e integración en el motor: 0 créditos.

Total de (b): **526,38**. Con el animatic: **532,00**. Quedan **336,75** para el resto del juego antes de que caduquen los créditos, hacia el 2026-12-12.
