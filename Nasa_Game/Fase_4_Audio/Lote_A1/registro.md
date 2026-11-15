# Lote A1: efectos de sonido del juego jugable v0

> Partida cerrada: 7,50 créditos de Higgsfield (tope 8,00), modelo `mirelo_text_to_audio` a 0,25 créditos por segundo. Generado el 2026-11-14. **Provisional:** la Fase 4 (diseño acústico) no está validada por Guillermo.

## Cómo se procesó

- Originales en `originales/` (MP3, 44,1 kHz). Registro máquina: `registro.json`; respuestas de la API en `_json/`.
- `analizar.py` y `analizar_bandas.py` miden cada archivo sin escucharlo: duración, pico, RMS, centro espectral, energía por bandas y envolvente cada 50 ms.
- `convertir.py` elige la versión, recorta, normaliza y escribe `juego/audio/<nombre>.ogg` (Vorbis mono, 44,1 kHz, calidad 5). Los cortos («corto») se quedan con el golpe más fuerte, para que no se solapen al repetirse. Los ambientes cierran el bucle con un fundido cruzado de 0,9 s. Resumen máquina: `conversion.json`.
- **Nadie los ha escuchado.** Las cifras de abajo dicen que no son silencio, cuánto duran y qué nivel tienen, no si suenan bien. Falta el veredicto de oído de Guillermo.

## Efectos

Nivel medido sobre el `.ogg` final con `ffmpeg -af volumedetect` (media y pico en dBFS).

| Efecto en el juego | Original elegido | Duración pedida | Costo | Archivo final | Duración final | Media | Pico | Por qué esta versión |
|---|---|---|---|---|---|---|---|---|
| `paso` | `paso.mp3` | 1 s | 0,25 | `juego/audio/paso.ogg` | 0,26 s | -22,7 | -1,5 | Única versión |
| `paso_luna` | `paso_luna.mp3` | 1 s | 0,25 | `juego/audio/paso_luna.ogg` | 0,36 s | -19,6 | -4,2 | La v2 tiene el pico en -30,6 dB y el 64 % de la energía bajo 150 Hz: no se oiría en altavoces de portátil |
| `salto` | `salto_v2.mp3` | 1 s | 0,25 | `juego/audio/salto.ogg` | 0,70 s | -17,2 | -4,9 | La v1 tiene el 100 % de la energía bajo 150 Hz: un retumbo, sin el roce pedido |
| `recoger` | `recoger.mp3` | 1 s | 0,25 | `juego/audio/recoger.ogg` | 0,74 s | -27,1 | -1,6 | Única versión (campanillas sobre 6 kHz) |
| `umbral` | `umbral.mp3` | 2 s | 0,50 | `juego/audio/umbral.ogg` | 2,00 s | -19,1 | -4,2 | La v2 se pagó pero no se descargó |
| `logro` | `logro.mp3` | 2 s | 0,50 | `juego/audio/logro.ogg` | 2,00 s | -31,8 | -1,9 | Única versión (tres notas; nivel medio bajo por ser campanas con mucho pico) |
| `pagina` | `pagina.mp3` | 1 s | 0,25 | `juego/audio/pagina.ogg` | 0,55 s | -24,3 | -1,3 | Única versión |
| `radio` | `radio_v2.mp3` | 1 s | 0,25 | `juego/audio/radio.ogg` | 0,82 s | -20,6 | -1,1 | La v1 es casi silencio (pico -41,8 dB, RMS -57,7 dB) |
| `golpe_mastil` | `golpe_mastil.mp3` | 1 s | 0,25 | `juego/audio/golpe_mastil.ogg` | 0,40 s | -28,2 | -0,7 | Única versión. Lo usa la Luna al plantar las banderas (`zonas/luna/luna.gd`) |
| `ambiente_luna` | `ambiente_luna.mp3` | 8 s | 2,00 | `juego/audio/ambiente_luna.ogg` | 7,11 s, bucle | -18,0 | -6,9 | Única versión. El 95 % de la energía está bajo 150 Hz: en altavoces de portátil se oirá muy poco |
| `ambiente_sendero` | `ambiente_sendero.mp3` | 6 s | 1,50 | `juego/audio/ambiente_sendero.ogg` | 5,11 s, bucle | -20,3 | -3,7 | Única versión (energía entre 2 y 6 kHz: agua y pájaros) |
| — | `paso_luna_v2.mp3` | 1 s | 0,25 | no se usa | | | | Descartada (ver `paso_luna`) |
| — | `radio.mp3` (v1) | — | — | no se usa | | | | Descartada (ver `radio`) |
| — | `salto.mp3` (v1) | — | — | no se usa | | | | Descartada (ver `salto`) |
| — | `umbral_v2` | 2 s | 0,50 | no existe | | | | Pagada; la descarga falló («Remote end closed connection»). La API la da por completada: su `result_url` está en `_json/umbral_v2.json` |

Total: 15 trabajos, 7,50 créditos (6,25 del primer pase y 1,25 de las segundas versiones).

## Encargos (prompts)

| Efecto | Prompt |
|---|---|
| paso | A single soft footstep of a sneaker on a packed dirt path with a little fine gravel, close microphone, dry, outdoors, no reverb. No voice, no speech, no music. |
| paso_luna | A single muffled thud of a heavy boot pressing into fine dry powdery dust, heard from inside a space helmet, very dull and soft, low frequencies only, no echo. No voice, no speech, no music. |
| paso_luna_v2 | One single heavy footstep in deep dry sand, a deep thump with a short sandy crunch, loud and clear, isolated, dry, no reverb, with silence before and after. No voice, no speech, no music. |
| salto | A short soft whoosh of fabric and a light push off the ground, a small jump with a quiet cloth rustle, close and dry. No voice, no grunt, no speech, no music. |
| salto_v2 | One quick whoosh of air, a fast bright swish like swinging a thin stick through the air once, loud and clear, isolated, dry. No voice, no speech, no music. |
| recoger | A short bright pick-up sound: a small metal part lifted with a soft glassy chime, clean and pleasant, item collected in a cozy adventure game. No voice, no speech, no melody. |
| umbral | A soft airy whoosh that rises into a gentle shimmering tone, like stepping through a doorway of light, calm and warm, smooth fade out. No voice, no speech, no melody. |
| umbral_v2 | A magical whoosh: a smooth airy swoosh that rises in pitch and ends in a bright sparkling shimmer, loud and clear, isolated. No voice, no speech, no melody. |
| logro | A warm short success chime: three soft bell-like notes rising, with a gentle sparkle tail, calm and hopeful, clean ending. No voice, no speech, no drums. |
| pagina | A single paper page turning in a notebook, crisp, close microphone, dry room. No voice, no speech, no music. |
| radio | A short clean two-tone intercom beep inside a space helmet with a tiny static click at the end, friendly and soft. No voice, no speech, no music. |
| radio_v2 | Two clear electronic beeps of a walkie-talkie, the second one higher in pitch, loud and clear, isolated, dry, with silence after. No voice, no speech, no music. |
| golpe_mastil | A single dull metallic clank of a small hammer driving a thin aluminum pole into dry compact dust, muffled as if heard through a space suit, short, no echo. No voice, no speech, no music. |
| ambiente_luna | Calm slow breathing inside a space helmet over the soft steady low hum of a suit life-support fan, intimate, muffled, continuous and even from start to end. No voice, no speech, no beeps, no music. |
| ambiente_sendero | A gentle small stream flowing over stones with a few tropical songbirds in the late afternoon and a light breeze in the leaves, continuous natural ambience, even from start to end. No voice, no speech, no music. |

## En el juego

- `nucleo/audio.gd` busca primero `res://audio/<nombre>_<zona>.ogg` (así suena `paso_luna` en la Luna), luego `res://audio/<nombre>.ogg` y, si no hay archivo, el pitido sintetizado de siempre (`ok`, `error`, `pulsar` y `tic` siguen sintetizados).
- `Audio.paso()`: el paso de la protagonista. Un paso cada 210 ms como mínimo, con el tono ±7 % y el nivel ±1,5 dB distintos cada vez. `jugador.gd` llama a `sonar("paso", -26.0)` y ese ajuste es la marca que lo desvía aquí.
- Nivel del paso con archivo: `volumen_db` (-8) + `PASO_AJUSTE_DB` (-22) = -30 dB de ganancia sobre `paso.ogg` (RMS -22,7 dB). Antes el golpe sintetizado sonaba a -34 dB de ganancia; la primera integración lo había subido a -18 dB. **Sin escuchar: Guillermo lo valida de oído.**
- Cualquier otro `sonar("paso", x)` (la iguana de la plaza: +2, -2 y +3 dB) suena entero, con su ajuste y sin el límite de 210 ms; busca primero `paso_animal.ogg` (no existe) y cae en `paso.ogg`.
- `Audio.ambiente(nombre)`: bucle con fundido de entrada de 1,6 s y de salida de 1,1 s. Al cambiar de zona arranca solo el de esa zona (hoy, la Luna y el sendero); baja 9 dB mientras hay un minijuego abierto y se apaga en el menú.

## Pendiente

- Escucharlos (Guillermo) y dar el veredicto por efecto.
- Ambientes de la habitación, la plaza y el Mirador: no hay archivo; esas zonas quedan en silencio de fondo.
- Decidir si se recupera `umbral_v2` (pagada) con una descarga autorizada.
