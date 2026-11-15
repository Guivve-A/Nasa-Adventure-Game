# Registro de créditos del video demo

> Tope de Higgsfield para todo el demo: **40 créditos**. Se cotiza antes con `generate cost` (gratis). Herramienta: `herramientas/demo/audio_generar.py` (lee `audio/lote_demo.json` y se niega a pasar del tope). Detalle de cada trabajo (prompt, parámetros, id del trabajo y URL original): `audio/registro_audio.json`.

## Cotizaciones (2026-11-15, sin gasto)

| Modelo | Duración | Créditos |
|---|---:|---:|
| `elevenlabs_music_v2_5` (instrumental) | 150 s | 21,80 |
| `elevenlabs_music_v2_5` | 75 s | 10,90 |
| `elevenlabs_music_v2` | 150 s | 9,60 |
| `sonilo_music` | 150 s | 9,38 |
| `mirelo_text_to_audio` | por segundo | 0,25 |

Se eligió ElevenLabs Music v2.5: es el único de la lista con modo instrumental garantizado (`force_instrumental`) y cabía en el tope dejando 18,20 para efectos.

## Gastos

| Fecha | Trabajo | Modelo | Duración | Créditos | Saldo antes | Saldo después |
|---|---|---|---:|---:|---:|---:|
| 2026-11-15 10:19 | Música del demo (`musica_demo`) | `elevenlabs_music_v2_5`, instrumental | 150 s (salió de 153,05 s) | 21,80 | 657,25 | 635,45 |
| 2026-11-15 10:19 | Rugido de cohete | `mirelo_text_to_audio` | 6 s | 1,50 | 635,45 | 633,95 |
| 2026-11-15 10:20 | Golpe grave de título | `mirelo_text_to_audio` | 3 s | 0,75 | 633,95 | 633,20 |
| 2026-11-15 10:20 | Subida (riser) | `mirelo_text_to_audio` | 3 s | 0,75 | 633,20 | 632,45 |
| 2026-11-15 10:21 | Barrido de transición | `mirelo_text_to_audio` | 2 s | 0,50 | 632,45 | 631,95 |
| 2026-11-15 10:21 | Grillos de noche | `mirelo_text_to_audio` | 6 s | 1,50 | 631,95 | 630,45 |
| 2026-11-15 10:21 | Viento y olas en la orilla | `mirelo_text_to_audio` | 4 s | 1,00 | 630,45 | 629,45 |
| 2026-11-15 10:22 | Tecleo suave | `mirelo_text_to_audio` | 3 s | 0,75 | 629,45 | 628,70 |
| | **Total del demo** | | | **28,55** | **657,25** | **628,70** |

**Quedan 11,45 del tope de 40.** Los gráficos no gastaron créditos (se hicieron por código). A las 10:45 la cuenta marcaba 424,70: la diferencia con 628,70 es de otros flujos (la cinemática), no del demo.

- 2026-11-15, demo v2 (correcciones de los críticos): **0 créditos**. Todo se rehízo con material, gráficos y audio ya existentes.
