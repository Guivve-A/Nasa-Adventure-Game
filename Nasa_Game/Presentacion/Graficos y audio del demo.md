# Gráficos y audio del demo

> Material para el montaje de [[Guion del video demo]] (`montaje.json`). Todo a 1920 × 1080 y 48 kHz. Créditos: [[registro_creditos]] (28,55 de 40). Se regenera con `herramientas/demo/graficos.py`, `g05_registro.py` y `audio_procesar.py`.

## 1. Sistema gráfico

- Fuente de la interfaz del juego: **Bahnschrift** (Bold en títulos, SemiBold en rótulos, Regular en notas). Paleta de `juego/interfaz/estilo.gd`: crema `#F8C991`, papel `#F6E7C8`, noche `#1C282E`, cian `#62E4E0` y naranja `#F4A159` (el punto de luz ámbar). Bahnschrift no trae «≈»: ese signo va en Segoe UI Light.
- **Rótulo** (una plantilla para todos): franja noche al 78 % con esquinas de 12 px y filete naranja de 8 px; texto crema de 58 px. Esquina inferior izquierda en (96, 960): deja libre la franja de ayuda del juego (abajo, 30 px). Los fundidos de 6 cuadros los hace el montaje.
- **Sello** «Imágenes recreadas con IA»: 30 px, abajo a la derecha, sobre una pastilla oscura suave, ya al 70 %.

## 2. Archivos (`graficos/`)

| Archivo | Plano | Uso |
|---|---|---|
| `G01_apertura.mp4` | S07 (15,5–17,0) | 1,5 s opaco: el punto ámbar aparece, se abre y entra el título |
| `G01_cierre.mov` | S48 (146,0–150,0) | 4 s con alfa (qtrle) **encima** de la última imagen: el iris se cierra en 0,6 s en un punto ámbar, entra el título (0,5–1,1 s), funde a negro en 3,5 s (= 149,5) y queda negro |
| `G01_titulo.png`, `G01_titulo_sobre_negro.png`, `G01_punto_luz.png` | — | Piezas sueltas del título |
| `rotulos/rotulo_SNN.png` | 30 rótulos | Texto exacto de `montaje.json`; índice con tiempos en `rotulos/rotulos.json`. S07 y S48 usan G01 |
| `G02_luna_medida.png` | S20 | Izquierda: la máscara real que midió `luna_medir.py` (`pruebas/luna_telescopio/capturas/luna_prueba.png`, 12,15 % y 192,6°). Derecha: el disco dibujado con los datos de JPL Horizons (12,2 % y 192,6°) |
| `G03_fondo.png` + `G03_capa_1..3.png` | S37 | Fondo y tres capas con alfa que entran cada 1,5 s; `G03_triptico.png` es el compuesto |
| `G04_equipo.png` (y `_capa`) | S46 | Equipo, Guayaquil y créditos de datos e IA sobre la lámina de hojas desenfocada |
| `G05_registro_provisional.png` (y `_largo`) | S38, mitad derecha | **Provisional:** registro real, pero de `muestras` (52 PRUEBA_OK, 2026-11-14). Al grabar T27: `python -I herramientas/demo/g05_registro.py <log de T27>` |
| `G06_cifras.png` (y `_capa`) | opcional en el cierre | 8 cifras del [[Inventario para la presentacion]] |
| `ocular_abre.mov` | S18 (53,0–55,0) | 2 s con alfa: negro con un ocular que se abre en 0,8 s y un aro cian |
| `lineas_tv.png` | S08 | Cuadro 4:3 con líneas de barrido y bordes de tubo; el grano se añade con `noise` de ffmpeg |
| `vineta.png` | opcional | Viñeta suave para las fijas de la cinemática |
| `sello_ia.png`, `sello_en_produccion.png` | cinemática / lo provisional | Sellos |
| `_hoja_de_contacto.jpg` | — | Revisión visual |

**Repeticiones a decidir en el montaje:** el rótulo de S46 repite los nombres de `G04` y el de S20 repite las cifras de `G02`. Propuesta: en esos dos planos, quitar el rótulo.

## 3. Audio (`audio/`)

Todos son wav de 48 kHz y 24 bits, medidos con `volumedetect` y `ebur128`: `audio/medicion_audio.json`. **Nadie los ha escuchado:** solo hay mediciones.

### Música

`musica_demo.wav` (150,000 s, estéreo) y `musica_demo_automatizada.wav` (la misma con la mezcla del guion). Se colocan en **0:00** del video, sin desplazar.

- Original de ElevenLabs Music v2.5 en modo instrumental: 153,05 s. Se le quitaron 0,180 s al inicio para alinear el pulso.
- **Pulso medido: 90 BPM exactos.** Tras el recorte cae en múltiplos de 0,6667 s desde el 0. Así, los cortes del montaje de minijuegos (70,000 + n × 1,333) caen todos en el pulso: 1,333 s son dos pulsos.
- **Forma medida** (RMS cada 5 s): no siguió las marcas pedidas.
  - De 0 a 55 s nace suave y crece de −35 a −19 dBFS.
  - De 55 a 125 s se mantiene plena, entre −14 y −16.
  - Desde 125 s decrece sola (−18, −21, −22) y se apaga hacia 145 a 148 s.
  - En el montaje de 70 a 82 s no hay un salto de energía propio.
  - Hay ataques cerca de 12,1 s, 12,8 s y 15,5 s. Por la medición, podrían coincidir con las notas sueltas y el acorde del título.
- Automatización de `musica_demo_automatizada.wav`, en dB respecto del pleno:

| Tramo | dB |
|---|---|
| 0 a 11,0 | silencio |
| 11,0 a 11,3 | entra hasta pleno |
| 16,6 a 17,0 | baja a cama |
| 17 a 52 | cama, −20 |
| 52,0 a 52,4 | sube a −10 |
| 54,6 a 55,0 | vuelve a cama |
| 69,6 a 70,0 | sube a pleno |
| 81,6 a 82,0 | vuelve a cama |
| 101,0 a 101,4 | sube a −8 |
| 104,6 a 105,0 | vuelve a cama |
| 123 a 126 | crescendo hasta pleno |
| 126 a 140 | de +2,5 a +5,5, para compensar el decrecimiento propio del tema |
| 148,5 a 149,5 | fundido |
| 149,5 a 150 | silencio |

  Pico del archivo: −1 dBFS. La sonoridad final (−14 LUFS) se ajusta en la mezcla del montaje.

### Efectos

| Archivo | s | Para | Origen |
|---|---:|---|---|
| `efectos_gancho.wav` | 17,0 | S01–S07, premezcla | Viento y olas con respiración (0–2,5), solo respiración (2,5–6), golpe grave en 4,8, rugido a tope (6,0–8,5), silencio total desde 8,5 y toma de aire en 13,4 |
| `rugido_cohete.wav` | 6,0 | S03 | Mirelo |
| `rugido_corto.wav` | 3,5 | S36 | Del anterior |
| `golpe_grave.wav` | 3,0 | S02 (4,8); opcional en el título | Mirelo |
| `subida.wav` | 3,0 | S22 (de 67,0 a 70,0) | Mirelo |
| `barrido.wav` | 2,0 | Transiciones | Mirelo |
| `grillos.wav` | 6,0 | S09, S15, S40 | Mirelo |
| `viento_orilla.wav` | 4,0 | S01 | Mirelo |
| `tecleo.wav` | 3,0 | S38 | Mirelo. Salió casi en silencio (pico −31 dBFS) y se subió a −6: lleva más ruido de fondo |
| `respiracion.wav` | 6,0 | S01–S02 | `juego/audio/ambiente_luna.ogg` (respiración en el casco) |
| `siseo_tv.wav` | 4,0 | S08 | Sintetizado |
| `alarma_corta.wav` | 2,0 | S34 | Sintetizado: tres pitidos dobles de 660 y 550 Hz |
| `toma_aire.wav` | 1,2 | S06 | Sintetizado: ruido filtrado |
| `sint_golpe_grave.wav`, `sint_subida.wav`, `sint_barrido.wav` | — | Reserva | Sintetizados |

Del juego, sin cambios: `juego/audio/` (paso, paso_luna, salto, umbral, pagina, radio, golpe_mastil, logro). Los pájaros de S10: `juego/audio/ambiente_sendero.ogg` (arroyo y pájaros) o el sonido de la toma.
