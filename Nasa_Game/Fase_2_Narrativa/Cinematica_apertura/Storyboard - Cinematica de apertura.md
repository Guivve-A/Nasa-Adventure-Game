# Storyboard · Cinemática de apertura: «Un punto de luz»

> Estado: **storyboard propuesto, sin validar;** corregido el 2026-11-15 tras dos verificaciones independientes (§9) y subido a nivel de cine en el **pase de fotografía** del mismo día (§10 guion de color, §11 fotografía plano a plano, §12 qué cambió). 0 créditos gastados, nada generado ni descargado. Lo valida Guillermo; después va el animatic (lote 09a) y solo entonces los fotogramas finos y el video.
> Guion: [[Guion - Cinematica de apertura]]. Datos: [[01_hechos_verificados]]. Lenguaje: [[02_lenguaje_visual]]. Tarifas: [[03_produccion_higgsfield]].
> Fecha: 2026-11-15. Saldo comprobado con `account status`: **853,75 créditos** (868,75 de 03, menos 15,00 del lote 08 de pantallas de carga).
> Marcas: **(sueño)** licencia declarada · **(cálculo)** cálculo propio con JPL Horizons, en `Datos/efemerides_storyboard.json` · **(sv)** sin verificar: no va en pantalla.

## 0. En cifras

| Cifra | Valor |
|---|---|
| Duración y planos | **118 s, 15 planos** (P01 a P15 = G01 a G15 del guion), de 6 a 12 s |
| Video generado | **79 s en 11 tomas** (10 planos; P14 se rueda en dos tomas); 35 s en Seedance 2.5 en la partida máxima |
| Sin video generado | P01 y P02 (render y cámara del motor, horneados con Movie Maker), P07 y P13 (fijas con movimiento en ffmpeg), P15 (motor en vivo) |
| Fotogramas clave | 17 de borrador (lote 09a) y 19 finales (uno, K01, de reserva) |
| Lote 09a cotizado | **4,25 créditos** (17 × 0,25). Tope de la partida: 6,00; quedan 1,75 para 7 reintentos |
| Presupuesto recomendado | **Partida de máxima calidad: 754,50 créditos** (88 % del saldo), tope de **783** (§5.4). Variante un 30,9 % más barata: **521,13**, tope de 542 (§5.5) |
| Planos héroe | P04 (la ignición), P11 (la huella), P13 (bandera y Tierra) y P14 (el ojo y la lágrima); plano firma: el reflejo de P02 (§11.3) |
| Texto en pantalla | 39 palabras: 4 rótulos y 2 frases históricas, todas del motor |

**El punto de luz tiene un lugar fijo en la pantalla.** P★ = (0,60 del ancho; 0,36 del alto, desde arriba) = píxel (1152, 389) a 1080p. Ahí caen, en orden: la chispa del cohete en la cima de su arco (P06), el borde superior de la Tierra (P07), el destello de la nave (P08), la Luna sobre Guayaquil (P12), la Tierra, ya sola, al final de P13, el punto del tubo al apagarse y el brillo de la lágrima en el lagrimal (P14). Desde 1:23 el ojo del jugador no se mueve de ese punto. Todo se ajusta en composición, sin costo.

## 1. Tabla de planos

### 1.1 Imagen

| # | Entra | Dur. | Tipo y encuadre | Cámara | Acción | Luz y color | Textura |
|---|---|---:|---|---|---|---|---|
| P01 | 0:00 | 9 s | General. Cámara alta 3/4 del juego; **la misma cámara del motor que P15** | Fija | 2 s de negro. Un punto blanco se abre en la pantalla del televisor y su luz descubre el cuarto. Ella duerme vestida, de lado y de cara al cuarto, solo rizos; respira. Órbita sobre el televisor | Una sola fuente: el tubo, blanco azulado, que late un 10 %. Sombra `#516B7C`, oscuro `#322C1D`. Onda cian en el banco. Ventana sin Luna **(cálculo)** | Render del motor, limpio. Tubo solo dentro de la pantalla |
| P02 | 0:09 | 6 s | De general a la pantalla vista de frente | Cámara del motor: avance, descenso y giro en una sola curva suave, hasta quedar perpendicular a la pantalla | El cuarto sale de cuadro; la cola de Órbita cruza y desaparece | El gris del tubo toma ámbar | Render del motor. Barrido → grano; el 4:3 se abre a 16:9 en 2 s (0:14–0:16) |
| P03 | 0:15 | 9 s | Gran plano general. 600 mm, f/11. Cohete a 1/6 del alto, en x = 0,60 (la vertical de P★); 6 o 7 siluetas de espaldas, < 5 % | Fija | Nadie se mueve. El aire tiembla | Sol duro de media mañana, contraluz. Ámbar y crema desaturados | 16 mm, grano al 100 % |
| P04 | 0:24 | 7 s | Mismo eje, 3 veces más cerrado (~1800 mm): cohete a 1/2 del alto | Fija; **cámara lenta al 50 %** | Un punto naranja se enciende en la base y se ensancha. El cohete se despega muy despacio, a 0:29, con el golpe grave | **Primer color saturado:** el naranja del fuego tiñe el vapor de ámbar | 16 mm, halación en la llama |
| P05 | 0:31 | 7 s | General. 24 mm, f/8, foco profundo, a 1 m sobre la orilla, detrás de las siluetas (< 10 %); la columna en x = 0,60 | Una inclinación lenta hacia arriba, a velocidad real | La columna de fuego y humo crema sale por arriba del cuadro | El fuego alumbra el humo desde dentro. Ámbar, crema y azul pálido | 16 mm al 90 %. Temblor del 1 % y arruga en el agua, en posproducción |
| P06 | 0:38 | 6 s | Plano general extremo del cielo. 50 mm, foco a infinito | Fija | La chispa blanca sube por el arco de la estela y se vuelve horizontal al llegar a su cima, en P★ (el giro de la trayectoria); el viento tuerce la estela | De azul pálido a índigo | 16 mm al 70 % |
| P07 | 0:44 | 8 s | La Tierra entera. 24 mm | Alejamiento lento: del 60 % al 25 % del alto, con el borde superior fijo en P★ | La Tierra se encoge | Negro puro. **Único azul saturado.** Gibosa, iluminada en unos 3/4 (77 %, **(cálculo)**), con una franja de noche en un borde | Grano al 40 % |
| P08 | 0:52 | 6 s | El borde de la Luna. 85 mm | Acercamiento y deriva lateral | 0–2 s: el disco de la Luna (render de LRO) crece desde el tamaño de la Tierra. 2–3 s: disolvencia al borde fino. 3–6 s: el borde llena el cuadro y deriva. Cruza un destello de 2 píxeles por P★ | Sol rasante en el terminador; plata y gris | Grano al 25 % |
| P09 | 0:58 | 9 s | Cenital. 35 mm, mirando recto hacia abajo | Descenso vertical; el último segundo, cuadro congelado | El suelo se acerca. Entra una sombra de cuatro patas, estirada 5 veces **(cálculo)**. Polvo en rayos rectos, a ras. Todo se detiene | Sol a 10,7° **(cálculo)**: sombras largas hacia arriba del cuadro. Gris neutro | Casi limpio: grano al 10 % |
| P10 | 1:07 | 6 s | El tubo: un 4:3 de 960 × 720 en el centro; el cuarto al 10 % a los lados | Fija | Imagen cabeza abajo 2 s; gira 180° de golpe. Una figura clara y translúcida, de lado y de cara a la escalera, quieta en el último peldaño, baja un pie muy despacio | Blanco y negro quemado | Tubo: 10 cuadros por segundo, estela, barrido, nieve |
| P11 | 1:13 | 10 s | Detalle. Macro de 100 mm, f/4, lateral, a ras del suelo | Fija (empuje de 0,5 % por segundo sobre el cuadro congelado) | El borde de una bota sale por arriba; caen unos granos en línea recta. Queda la huella. 9 s sin movimiento | Dentro de la sombra del módulo: luz de rebote, suave. Al fondo, el llano arde de Sol, fuera de foco | **El plano más nítido:** sin grano |
| P12 | 1:23 | 8 s | General nocturno. 50 mm, f/2, hacia el oeste: techos de la ciudad y cerros bajos. Ella de espaldas en el tercio izquierdo, fuera de foco; la Luna en P★, de 24 px, compuesta después del video | Fija | Ropa tendida que se mece. Ella levanta apenas la barbilla | Cuatro bombillos de tungsteno y la Luna. Ámbar sobre azul negro | Vuelve el 16 mm cálido: grano al 80 % |
| P13 | 1:31 | 8 s | General. Contrapicado de 14 mm a ras de suelo, Sol a la espalda. Bandera a un 9 % del alto, **entera** | Fija 1:31–1:33; inclinación hacia arriba de unos 21° **(cálculo)**, con arranque y frenado suaves, 1:33–1:37; fija 1:37–1:39 | 1:31–1:35: la bandera, entera abajo a la derecha, y la Tierra arriba comparten el cuadro (la imagen del homenaje). 1:35–1:37: la mirada sube; la bandera sale entera por el borde inferior. 1:37–1:39: solo la Tierra, en P★, y el cielo negro | Sol duro sin relleno, cielo negro. **Únicos colores: la bandera y la Tierra** | Sin grano |
| P14 | 1:39 | 12 s | **Único primer plano.** 100 mm, f/2, a la altura de la almohada; foco en las pestañas del ojo de arriba | Fija: se mueven la luz y ella | El tubo se apaga en un punto, que es una gota en el lagrimal del ojo de arriba. Una franja ámbar le sube por la mejilla. Abre los ojos y sonríe con los ojos. La lágrima cruza el puente de la nariz. Pestañea | De azul petróleo a ámbar `#F4A159` y crema `#F8C991` | Pintado, sin grano; el desenfoque se asienta. La gota, compuesta |
| P15 | 1:51 | 7 s | General. La cámara del juego (D-013) | La del juego | Se sienta de golpe y mira el banco. Órbita, sobre la caja, levanta la cabeza, la mira y salta al suelo (mínimo aceptable: levanta la cabeza y no salta) | La del juego (D-015): mañana de la paleta maestra | Motor, en vivo |

### 1.2 Sonido, texto y transición

| # | Sonido | Texto del motor | Transición al siguiente |
|---|---|---|---|
| P01 | Zumbido del tubo, siseo de nieve, grillos, ventilador. Respiración dormida, un ciclo cada 4 s. Tonos de radio por un parlante pequeño | R0, 0:00–0:02, sobre el negro: «Imágenes recreadas con IA» | El último cuadro es el primero de P02 |
| P02 | El zumbido baja de tono hasta ser viento. Los grillos se apagan uno a uno | — | La pantalla 4:3 llena el alto del cuadro; disolvencia por forma a K03 en blanco y negro; de 0:14 a 0:16 la máscara se abre a 16:9 y el gris cruza al color |
| P03 | Viento y agua en la orilla. A 0:21 el viento se corta: queda la respiración | R1, 0:17–0:20: «Centro Espacial Kennedy, Florida · 16 de julio de 1969» | Corte en el eje |
| P04 | **Primer silencio:** 5 s de fuego mudo en cámara lenta, solo respiración. A 0:29, el golpe grave, justo cuando el cohete se despega | — | Corte seco con el rugido |
| P05 | El rugido, a tope: el único momento en que la mezcla toca el límite | — | Corte en el movimiento: la llama sale por arriba |
| P06 | El rugido se aleja, pierde agudos y muere en 4 s | — | Disolvencia por forma, 1,5 s: el arco de la estela es el borde superior de la Tierra casi llena |
| P07 | **Segundo silencio,** 3 s. A 0:47, respiración cerrada, como en un casco. A 0:48, **primera nota** | — | Disolvencia por forma, 1,5 s: el disco azul se vuelve un disco gris del mismo tamaño |
| P08 | Respiración. A 0:55, un pitido de radio | — | Corte seco de gris a gris |
| P09 | Zumbido mecánico que sube. La respiración se detiene a 1:02. Contacto a 1:03: corte a nada. A 1:04 suelta el aire; un tono de radio | R2, 0:58–1:01: «Base Tranquilidad · 20 de julio». S1, 1:04–1:07, como cita: «Volvemos a respirar.» | Corte seco |
| P10 | Zumbido del tubo y siseo. Ninguna voz | — | Corte en la acción: el pie que baja |
| P11 | La respiración se detiene. **Tercer silencio,** 10 s: ni música ni radio | S2a, 1:20–1:23: «Es un pequeño paso para un hombre;» | Corte seco, de lo más pequeño a lo más lejano |
| P12 | Grillos de P01. Un perro lejos. Una bocina de barco, una vez. A 1:27, **segunda nota** | R3, 1:24–1:27: «Guayaquil · esa misma noche, 21:56». S2b, 1:27–1:31: «un salto gigante para la humanidad.» | Corte seco. La Luna ocupaba P★: ahí llegará la Tierra |
| P13 | **Tercera nota** y, debajo, el primer acorde. A 1:38, con la bandera ya fuera de cuadro, un golpe blando y el *clac* de una perilla | — | El tubo se apaga sobre la Tierra sola: se pliega en una raya a la altura de P★ y la raya, en un punto en P★. La bandera nunca se apaga ni hace de transición |
| P14 | A 1:45, **cuarta nota** y la primera toma de aire en 32 s. A 1:50, media risa; pájaros | — | Corte en el pestañeo |
| P15 | La mañana de Las Escalinatas: pájaros, un bus, el ventilador. Sin música. Un maullido | El del juego: a 1:57, «Habla con Órbita» | El control pasa al jugador |

Rótulos (R): abajo a la izquierda, blanco al 80 %, 3 s con fundidos de 0,5 s. Frases (S): centradas abajo, **entre comillas («…») y en cursiva**, con estilo de subtítulo de transmisión, para que se lean como citas históricas y no como palabras de ella (S1 cae cuando ella suelta el aire). Sin nombres.

## 2. Encargos por plano

> Reescritos el 2026-11-15 en el pase de fotografía (§12). Cada encargo declara óptica, diafragma, altura, luz motivada, contraste, color de película, movimiento y duración. La fotografía de cada plano, en tabla, está en §11; el guion de color, en §10.

**Cómo leerlo**
- `K` es el encargo del fotograma clave. Va tal cual en el lote 09a (`gpt_image_2_6`, `low`, 1k, 16:9, 0,25 créditos) y, aprobado el borrador, en el lote 09b con el borrador como referencia. Calidad del 09b según la partida (§5.4): `xhigh` 2k (4,50) en los fotogramas que se ven quietos o de cerca, `high` 2k (2,75) en el resto y `medium` (1,00) en K10.
- `K04a`, `K11a` y `K14d` no van en el 09a: se generan en el 09b con su fotograma hermano como referencia. Su encargo queda escrito aquí.
- `M` es el encargo de movimiento para el modelo de video. Cada uno declara duración, velocidad y movimiento de cámara.
- **Parámetros de video.** Seedance 2.5 va con `mode: omni_reference`, `resolution: 720p` y `generate_audio: false`. **MiniMax H3 no tiene `generate_audio`** (su pista, si trae, se descarta con `-an` al montar) y fija siempre `aspect_ratio: 16:9`, porque su valor por defecto es «auto». Seedance 2.0 Mini, 720p.
- **Antes del lote de video** se aplican en `herramientas/hf_generar.py` los dos arreglos que 03 §3 deja pendientes: resolver `@ANC_…` dentro de `params` y subir la espera de 15 a 30 min.
- **Puerta de control de cada clip, no solo de cada fotograma.** Un modelo de video puede añadir letras, emblemas o una bandera a mitad del clip aunque el fotograma inicial esté limpio (el cohete real llevaba «USA», «UNITED STATES» y la bandera pintados). De cada clip se extrae un cuadro cada 0,5 s (`ffmpeg -i clip.mp4 -vf fps=2 cuadros/%03d.png`) y se revisa al 200 % en busca de letras, insignias, banderas fuera de P13 y rostros. Un clip con marcas se descarta o se retoca; nunca se monta.
- `{ESTILO}` y `{GATO}` son bloques fijos de `bloques_prompt.json`; solo los llevan los planos del cuarto.
- **Los fotogramas se piden limpios.** El grano, la halación, el temblor de cuadro, la nieve y el barrido los pone el shader (§10.3). El encargo fija la óptica, la luz y la respuesta de color de la película.
- **Composición en fracciones del cuadro**, no en palabras vagas: P★ es «three fifths of the frame width and one third of the height from the top». El eje vertical del vuelo (P03 a P06) está en x = 0,60, la vertical de P★.
- Tarifas cotizadas otra vez el 2026-11-15 con `generate cost` (0 créditos): Seedance 2.5 a 720p, 7 por segundo (35, 42 y 56 a 5, 6 y 8 s, también con fotograma inicial y final); MiniMax H3, 2 por segundo (12 y 16 a 6 y 8 s); Seedance 2.0 Mini, 1 por segundo.
- Subida el 2026-11-15, sin costo: `@ANC_HABITACION` (el concepto validado `L05_A_manana_calida_final.png`).

Referencias: ![[L02_protagonista_tipo1_hoja.png|260]] ![[L02_gato_orbita_hoja.png|220]] ![[L05_A_manana_calida_final.png|300]]

### P01 · El cuarto a oscuras (0:00–0:09)

- **Producción: render del motor,** con la misma cámara, la misma escena y los mismos shaders que P15 (D-013 y D-015), horneado al video con el modo Movie Maker de Godot (`--write-movie`, 24 fps). Solo así la rima P01 ↔ P15 (televisor ↔ caja, Órbita en la misma pose) es exacta: un fotograma generado no reproduce la distribución, la cámara ni las proporciones del motor. La pantalla es un recuadro aparte con el fotograma de P03 en blanco y negro; el latido de la luz, la onda cian y la apertura del punto son shader. Ella respira con una animación de reposo dormida (escala suave del torso, ciclo de 4 s). 0 créditos.
- **Fotografía (pase):** una sola fuente práctica, el tubo, con caída por distancia (la luz no llega a las esquinas): 8 a 1 entre el charco de luz del suelo y el resto. La cámara está fija pero **respira con ella:** una escala del 0,3 % en el mismo ciclo de 4 s que su respiración. Unas motas de polvo brillan en el haz del tubo.
- El televisor entra en el motor como pieza modelada por script, con su ID en el catálogo, **después** de que Guillermo valide su concepto (K01 y K02). La Habitación de noche también pasa antes su puerta. Por eso este plano se produce después de que la Habitación pase su puerta en el motor.
- **Reserva**, si la Habitación no está lista: K01 final pintado (`high` 2k, 2,75) con una **captura del motor del encuadre exacto** como primera referencia, en lugar de `@ANC_HABITACION`.
- El borrador K01 es, sobre todo, **el concepto de la Habitación de noche y del televisor del sueño**, que Guillermo valida primero (pendiente 4 del guion).

**K01 · fotograma clave** · referencias: `@ANC_HABITACION`, `@ANC_PROTA_1`, `@ANC_GATO`
```text
Same room, same furniture layout and same fixed high three-quarter top-down game camera as the first reference image, but at night, around 3 a.m. The girl is the character of the second reference and the cat is the one of the third. Low-key night interior lit like a quiet film scene by one single practical source: a small 1960s tube television in a walnut wooden cabinet on four tapered legs, standing on the floor at the foot of the bed exactly where the cardboard box stands in the reference (the box is gone). Its bulging 4:3 screen with rounded corners faces the camera, turned slightly toward the bed, and glows cool bluish white with a soft black-and-white picture of a tall white three-stage rocket standing beside its launch tower. That light falls off fast with distance: a bright pool on the terracotta tiles and on the near edge of the blue blanket, long soft shadows of the bed legs and the stool stretching away from the set, about eight to one between the lit floor and the dark corners, and a few dust motes glinting in the beam. The window shutters are ajar and show only a dark hillside with three or four tiny warm bulbs: no moon in the sky. The girl sleeps on top of the blue blanket, fully dressed in her khaki short-sleeve shirt worn open over a dark T-shirt, brown cargo pants and sneakers, without her bag, lying on her left side and facing the room, curled up with her face buried in her forearm: only her big dark curly hair shows, no face, with a cool rim of screen light on the curls. On top of the television, {GATO} sleeps with its tail hanging down over one upper corner of the screen. The telescope on its tripod points at the window. On the workbench the small oscilloscope shows a trembling cyan wave, the only other glow, and the brown tool bag hangs from the stool. The two lanterns by the stair landing are unlit. {ESTILO} Night palette: petrol-blue shadows, darkest tones warm and never pure black, cool white television light. No brand or lettering on the television. Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

### P02 · Entrar (0:09–0:15)

- **Producción: cámara del motor,** horneada con Movie Maker como P01. 0 créditos. Un solo empuje recto generado no puede ir de la cámara alta 3/4 a la pantalla vista de frente (hay que avanzar, bajar y girar); en el motor el movimiento es 3D de verdad.
- **Plano firma: el reflejo** (0 créditos). En los 2 últimos segundos (0:13–0:15), con la cámara ya frente a la pantalla, el vidrio curvo refleja lo que tiene delante, que es la cama: su silueta enroscada, los rizos y el rectángulo pálido de la ventana flotan al 15 % sobre la imagen del cohete, curvados por el abombado del tubo. Es físicamente exacto (el televisor mira a la cama) y dice sin palabras que ella está dentro de lo que sueña. Se hace en el motor: un render de la cama desde el punto de vista de la pantalla, en espejo, con la curvatura del shader del tubo, mezclado en modo pantalla. El reflejo se apaga con la disolvencia: la cámara «atraviesa» el vidrio.
- Al final de la toma, la pantalla del televisor (un 4:3 con el fotograma K03 en blanco y negro) llena el alto del cuadro; a los lados, el mueble. Disolvencia por forma a K03 en blanco y negro y 4:3 sobre negro, y de 0:14 a 0:16 el shader abre la máscara a 16:9 y cruza al color.
- K02 no es un extremo de la toma: es el **diseño del televisor** (referencia para modelarlo), el cuadro intermedio del animatic y la placa de P10.
- Plan B, 0 créditos, si la Habitación no está lista en el motor: empuje digital sobre K01 a 2k hasta la pantalla (que en K01 ya mira a la cámara; la máscara 4:3 del shader endereza el escorzo) y la misma disolvencia por forma. El reflejo se compone igual, desde K01.

**K02 · fotograma clave** · referencias: `@ANC_HABITACION`, `@ANC_GATO`
```text
Frontal close view at screen height, 35 mm lens at f/2.8, the camera square to the glass: the dream television that stands in the dark bedroom of the first reference image, a small 1960s tube television in a walnut wooden cabinet with rounded corners and four tapered legs, two plain round knobs and a cloth speaker grille to the right of the screen, with no brand plate, no numbers and no lettering anywhere. The bulging 4:3 glass screen with rounded corners occupies the central half of the frame width and two thirds of its height and is in crisp focus; the edges of the cabinet soften slightly. It shows a soft black-and-white picture with faint horizontal scan lines: a tall white three-stage rocket standing beside its launch tower, far away across flat water, slightly right of centre. The screen is the only light: its phosphor glow spills onto the walnut grain, the terracotta floor tiles and a corner of a blue blanket, and a faint reflection of the dark room and a pale window rectangle floats on the curved glass, less than one tenth as bright as the picture. From the top edge of the frame the tail of the cat of the second reference, gray-taupe with a dark tip, hangs across the upper right corner of the screen; the cat itself is out of frame. Around the set, petrol-blue darkness, never pure black. {ESTILO} The television and the room are painted in this low-poly style; only the picture on the screen looks like old footage. Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**M02 · movimiento** (cámara del motor, 6 s; no es encargo de un modelo de video)
- Trayectoria: una curva de Bézier desde la cámara del juego (D-013) hasta un punto frente a la pantalla, a su altura y perpendicular a ella; la cámara avanza, baja y gira a la vez, con arranque y frenado suaves (curva de velocidad en S, sin sacudidas). Durante el movimiento, la focal simulada pasa de la del juego a 35 mm equivalentes, para que el cuarto se aplane al llegar.
- 0–3 s: el cuarto se abre en paralaje real; la cola de Órbita cruza el borde superior y desaparece. 3–4 s: la pantalla crece hasta llenar el alto del cuadro. 4–6 s: el reflejo de la cama aparece en el vidrio y se apaga con la disolvencia.
- Ella no se mueve salvo la respiración. No aparece ningún objeto.
- Se valida con una captura de cada segundo en el motor antes de hornear.

### P03 · La torre (0:15–0:24)

- **Producción:** `minimax_h3`, fotograma inicial K03, 10 s (se montan 9), `aspect_ratio: 16:9` · **20 créditos por intento**, en las dos partidas.
- Se fija el tamaño del cohete en cuadro, no la focal: a 5 km, 1/6 del alto pide un 150 mm; con 600 mm estaría a unos 20 km **(cálculo)**. El cohete va en x = 0,60, la vertical de P★: todo el vuelo sube por esa línea hasta la chispa de P06.

**K03 · fotograma clave** · referencias: ninguna
```text
Extreme telephoto photograph, 600 mm full-frame-equivalent lens at f/11, camera locked on a heavy tripod at standing eye height, strongly compressed perspective that stacks the far shore, the launch tower and the haze into flat layers. Hard mid-morning sunlight from high behind the rocket: the scene is backlit, the rocket and the tower are rimmed with light, and hot haze over a perfectly still lagoon on a flat subtropical coast lowers the contrast to about two to one. Far away on the horizon, at three fifths of the frame width, stands a tall slender white three-stage rocket attached to its dark steel launch tower: tiny, about one sixth of the frame height, softened and wavering in the heat shimmer. Along the bottom edge of the frame, in its left two thirds, six or seven small black silhouettes of people seen from behind stand motionless on the hoods and beside two boxy 1960s cars, backlit, less than one twentieth of the frame height, no faces visible. A huge pale sky fills the upper two thirds of the frame. Colour of 1960s 16 mm reversal film: muted amber, cream and faded cyan, slightly lifted warm blacks, highlights that roll off softly. No markings, letters, flags or symbols on the rocket, the tower or the cars. Clean image without film grain or borders. No text, no logos, no insignia, no emblems, no watermark.
```

**M03 · movimiento** (`minimax_h3`, 10 s)
```text
Locked-off extreme telephoto shot, 10 seconds, real time, no camera movement at all, as if on a heavy tripod. Only the air moves: heat shimmer ripples horizontally over the water and makes the distant rocket and tower waver slightly. A faint wisp of white vapour drifts sideways from the rocket and dissolves. The silhouettes do not move. The water stays mirror still. No ignition, no smoke, no flames, no birds, no zoom. No text.
```

### P04 · La luz llega antes (0:24–0:31) · **plano héroe 1** (§11.3)

- **Producción, partida máxima:** `seedance_2_5` a 720p, `omni_reference`, inicial K04a y final K04b, 8 s (se montan 7) · **56 créditos por intento, 2 intentos.** Variante −30 %: la misma toma con 1,5 intentos.
- **Cámara lenta al 50 %** (como rodado a 48 cuadros por segundo): el despegue pesa y el silencio dura más. El golpe grave de 0:29 cae justo cuando el cohete se despega (5 s dentro del plano): el sonido llega con el movimiento, no con la luz.
- K04a es el mismo encuadre un instante antes, sin fuego: se genera con K04b como referencia.
- Óptica: mismo eje y mismo sitio que P03 (600 mm), 3 veces más cerrado: unos 1800 mm, el aspecto de una cámara de seguimiento de largo alcance **(cálculo)**. Manda el tamaño en cuadro.

**K04a · fotograma clave** (solo 09b) · referencias: K04b
```text
Same frame, same lens, same light and same colour as the reference image, a few seconds earlier: the rocket stands completely still on the launch platform beside its tower, with no fire, no steam cloud and no glow at its base; only a thin wisp of white vapour drifts from its side in the heat shimmer. No people. No markings, letters, flags or symbols on the rocket or the tower. Clean image without film grain or borders. No text, no logos, no insignia, no emblems, no watermark.
```

**K04b · fotograma clave** · referencias: ninguna
```text
Extreme telephoto photograph from a long-range tracking camera, about 1800 mm full-frame-equivalent lens at f/11, same camera position as a 600 mm view tightened three times, locked off, strongly compressed perspective and heat shimmer. A tall white three-stage rocket beside its dark steel launch tower stands at three fifths of the frame width and fills the central half of the frame height against a pale hot morning sky, rim-lit by the sun behind it; flat marsh and a strip of still water run along the bottom. The engines have just ignited: at the base, a blinding orange-white fire, the only saturated colour in the whole image, blooming with a soft red-orange halation. The fire lights the underside of the rocket and the steam from below, so the steam rolling outward low along the ground on both sides glows amber at its base and turns cream above. The rocket has barely left the pad, its base just above the launch platform, perfectly vertical, the tower still beside it. No people. Colour of 1960s 16 mm reversal film: muted cream and faded cyan everywhere except the fire, slightly lifted warm blacks. No markings, letters, flags or symbols on the rocket or the tower. Clean image without film grain or borders. No text, no logos, no insignia, no emblems, no watermark.
```

**M04 · movimiento** (`seedance_2_5`, 720p, inicial K04a y final K04b, 8 s)
```text
Locked-off extreme telephoto shot, 8 seconds, filmed in slow motion as if at 48 frames per second, so everything feels enormous and heavy. No camera movement, no shake, no zoom. Seconds 0 to 1: nothing happens, only heat shimmer. Seconds 1 to 5: a tiny orange point of fire ignites at the base of the rocket and silently swells into a blinding fireball; steam lit amber from below rolls outward along the ground in slow, massive billows. Seconds 5 to 8: the rocket begins to lift off extremely slowly and perfectly vertically, rising less than one fifth of its own height, and arrives exactly at the last frame. The tower stays in place. No explosion, no debris, no birds. No text.
```

### P05 · La columna (0:31–0:38)

- **Producción, partida máxima:** `seedance_2_5` a 720p, `omni_reference`, fotograma inicial K05, 8 s (se montan 7) · **56 créditos por intento**, 1,5 intentos. Variante −30 %: `minimax_h3`, 8 s, `aspect_ratio: 16:9`, 16 por intento.
- **Velocidad real:** después de la cámara lenta de P04, el tiempo se pone al día con el ruido. El temblor del 1 % y la arruga del agua, en posproducción.

**K05 · fotograma clave** · referencias: ninguna
```text
Wide-angle photograph, 24 mm lens at f/8, deep focus from the stones at the waterline to the horizon, camera one metre above the ground on the shore of a still lagoon, behind a small group of spectators, level and slightly tilted up. In the lower fifth of the frame: the dark shoreline, two boxy 1960s cars and six or seven black silhouettes of people seen from behind, standing still on the hoods and beside the cars, less than one tenth of the frame height, no faces. Far across the water, at three fifths of the frame width, a colossal column of fire and cream-white smoke climbs straight up from the horizon and leaves the top of the frame; the column glows from inside like a lantern with orange fire, is amber on its sunlit side and falls into soft cream shadow on the other; the rocket itself is only a bright point at the head of the flame near the top edge. The calm water mirrors the column. Huge pale blue sky. Colour of 1960s 16 mm reversal film: amber, cream and faded blue, slightly lifted warm blacks. No markings, letters, flags or symbols anywhere. Clean image without film grain or borders. No text, no logos, no insignia, no emblems, no watermark.
```

**M05 · movimiento** (`seedance_2_5` en la partida máxima; `minimax_h3` en la variante; 8 s)
```text
8 seconds, real time. One single slow upward tilt with an eased start, about three percent of the frame height per second, following the rising column of fire and smoke until the flame leaves the top of the frame, as if a heavy tripod head is being pushed by hand. The smoke column billows and thickens in slow, massive rolls, glowing from inside. The silhouettes stay almost perfectly still. The water stays calm and mirrors the glow. No camera shake, no zoom, no cuts. No text.
```

### P06 · La chispa (0:38–0:44)

- **Producción:** `minimax_h3`, fotograma inicial K06, 6 s, `aspect_ratio: 16:9` · **12 créditos por intento**, en las dos partidas.
- Raccord: el arco de la estela es un círculo de radio 0,30 del alto con centro **justo debajo de P★, en (0,60 del ancho; 0,66 del alto)**. P★ queda en la cima: la chispa llega allí volviéndose horizontal, como en el giro de la trayectoria, y nunca parece caer. Es el mismo círculo que la Tierra de P07. Se ajusta en composición.
- **Firma del punto de luz:** al llegar a P★, la chispa recibe en posproducción el mismo destello pequeño y redondo que llevarán la nave de P08 y la gota de P14 (§10.2).

**K06 · fotograma clave** · referencias: ninguna
```text
Looking steeply up into a vast empty sky, 50 mm lens focused at infinity at f/8, locked off. The sky grades smoothly from pale blue at the bottom of the frame to deep indigo at the top, as at high altitude. A single tiny white spark sits at three fifths of the frame width and one third of the height from the top, at the tip of a long, thin white exhaust trail that sweeps across the frame in one clean arc, like the upper part of a very large circle whose centre lies below the spark: the arc rises from the lower left and levels off at its apex exactly where the spark is. The trail is lit by the sun from below the frame, bright white on its lower side and softly shaded above; its lower part is wider, slightly twisted and thinned by high-altitude wind. Nothing else: no ground, no clouds, no aircraft, no birds, no sun in frame. Faded colour of 1960s 16 mm reversal film. Clean image without film grain or borders. No text, no logos, no insignia, no emblems, no watermark.
```

**M06 · movimiento** (`minimax_h3`, 6 s)
```text
Locked-off shot, 6 seconds, real time. The white spark climbs slowly along the arc, levels off as it reaches the apex and shrinks to a point of light that stays at the apex for the last two seconds. High-altitude wind slowly bends, twists and thins the lower part of the trail. The sky darkens slightly toward indigo. Nothing else moves and nothing enters the frame. No text.
```

### P07 · La Tierra entera (0:44–0:52)

- **Producción:** fija de 2k con alejamiento en ffmpeg (escala del 100 % al 42 % sobre negro, con el borde superior anclado en P★ y curva de velocidad suave: el alejamiento arranca rápido y frena, como una nave que se va). 0 créditos de video. Fotograma en `xhigh` en la partida máxima: se ve 8 s, quieto y entero.
- Composición: el disco ocupa el 60 % del alto, con centro en (0,60 del ancho; 0,66 del alto) y su borde superior en P★: es el círculo de la estela de P06. **El borde superior está iluminado** (la franja de noche va abajo a la izquierda), para que P★ sea un punto de luz.
- **Fase: gibosa, unos tres cuartos (77 %) (cálculo).** JPL Horizons (`COMMAND=399`, `CENTER=500@301`) da la Tierra vista desde la Luna: 96,6 % el 16-07 a las 12:00 UT, 92,4 % el 17-07, 86,5 % el 18-07 y **77,3 % a la entrada en órbita lunar** (19-07, 17:21 UT). La nave va hacia donde estará la Luna al llegar; desde unas 6 h después de la inyección translunar, la dirección Tierra-nave queda a menos de 12° de la de llegada (cálculo propio), así que la Tierra se ve como desde la Luna en la llegada. Datos en `Datos/efemerides_storyboard.json`. No se rotula. El modelo inventa geografías: se pide océano y nubes, sin costas nítidas.

**K07 · fotograma clave** · referencias: ninguna
```text
The whole planet Earth floating in pure black space, photographed with a 24 mm lens at f/8 from a departing spacecraft, exposed for the sunlit clouds so that no stars show. A blue-and-white gibbous globe about three quarters lit, hard sunlight from the upper right, a band of night along its lower left edge melting into the black, and a thin luminous blue line of atmosphere along the sunlit limb. The globe sits slightly right of centre and low in the frame: its sunlit top edge touches a point at three fifths of the frame width and one third of the height from the top, and its bottom edge sits just above the bottom of the frame, so it fills 60 percent of the frame height. Deep saturated ocean blue and bright white cloud swirls, with only faint hints of land under the clouds: no sharply drawn or recognisable coastlines, no city lights. No stars, no Moon, no spacecraft parts, no lens flare. The background is perfectly black. Crisp large-format clarity, almost grainless. No text, no logos, no insignia, no emblems, no watermark.
```

### P08 · La Luna crece (0:52–0:58)

- **Producción.** Las texturas de `externos/` (`lroc_color_poles_4k.tif`, 11 píxeles por grado; `ldem_4.tif`, 4 píxeles por grado; albedo sin sombras) no dan el borde a pantalla llena. Por eso:
  - **0–2 s:** render propio con esas texturas (proyecto `pruebas/luna_telescopio/`, 0 créditos): un disco del mismo tamaño y lugar que la Tierra al final de P07 (25 % del alto, borde superior en P★) que crece hasta el alto del cuadro.
  - **2–3 s:** disolvencia por forma al borde fino.
  - **3–6 s:** `minimax_h3`, fotograma inicial K08 final, 6 s (se montan 4), `aspect_ratio: 16:9` · **12 créditos por intento**, en las dos partidas.
  - El destello de la nave es un punto de 2 píxeles que pasa por P★, con la firma del punto de luz (§10.2), en posproducción.
- Alternativa sin video: pedir permiso de descarga de mapas de más resolución del CGI Moon Kit (nombre, fuente y tamaño por archivo) y renderizar todo el plano.
- Créditos: «Texturas lunares: NASA/GSFC/Arizona State University (LRO) y CGI Moon Kit, NASA SVS. NASA no revisó ni respalda esta obra» (§6).

**K08 · fotograma clave** · referencias: ninguna
```text
Photograph of the Moon from an approaching spacecraft, 85 mm lens at f/8, crisp large-format clarity. The curved limb of the Moon rises from the lower left and fills two thirds of the frame; the highest point of the limb sits at three fifths of the frame width and one third of the height from the top. Neutral silver-gray surface, densely cratered; hard, low raking sunlight from the right, so the craters near the terminator cast long black shadows and their sunward rims glow; on the left the surface sinks into darkness along a diagonal terminator. There is no atmosphere: every shadow edge is razor sharp and the black is absolute. Pure black sky, no stars, no Earth, no spacecraft. Nearly grainless, high contrast. No text, no logos, no insignia, no emblems, no watermark.
```

**M08 · movimiento** (`minimax_h3`, 6 s, `aspect_ratio: 16:9`)
```text
6 seconds, real time. A slow lateral drift from right to left along the curved limb of the Moon, about two percent of the frame width per second, with a very gentle approach, smooth as a spacecraft coasting, with no acceleration. The craters and their long shadows stay fixed on the surface; the light does not change. Nothing crosses the frame: no spacecraft, no stars, no Earth. No camera shake. No text.
```

### P09 · La sombra (0:58–1:07)

- **Producción, partida máxima:** `seedance_2_5` a 720p, `omni_reference`, fotograma inicial K09, **8 s** (se montan 8) · **56 créditos por intento**, 1,5 intentos. Variante −30 %: `minimax_h3`, 8 s, 16 por intento. Plan B, 0 créditos: K09 fija, con el polvo y el crecimiento de la sombra en posproducción.
- **El último segundo (1:06–1:07) es el último cuadro congelado,** en ffmpeg: la quietud del contacto es absoluta, cosa que un modelo de video no garantiza (siempre deja una deriva). Por eso se generan 8 s y no 10.
- La máquina nunca se ve: solo su sombra. Con el Sol a 10,7° la sombra mide 5,3 veces la altura **(cálculo)**.

**K09 · fotograma clave** · referencias: ninguna
```text
Camera looking straight down at the surface of the Moon from about thirty metres up, 35 mm lens at f/11, everything in focus. Neutral gray powdery regolith fills the whole frame, peppered with small craters and scattered rocks. The sun is only ten degrees above the horizon, off the bottom of the frame: hard single-source light with no atmosphere and no fill, so every rock and crater rim casts a long, razor-sharp black shadow toward the top of the frame and the sunlit faces of the rocks glow. Entering from the bottom centre and reaching the middle of the frame: the long black shadow of a four-legged landing craft, an angular body on four splayed legs with round footpads, stretched to about five times its natural length by the low sun. Only the shadow is visible; the craft itself is never in frame. Fine dust streaks radially outward along the ground in perfectly straight thin rays that hug the surface, with no billowing cloud. No footprints, no flags, no people. Crisp and nearly grainless. No text, no logos, no insignia, no emblems, no watermark.
```

**M09 · movimiento** (`seedance_2_5` en la partida máxima; `minimax_h3` en la variante; 8 s)
```text
8 seconds. The camera looks straight down and descends slowly and steadily, with no rotation: the ground comes closer and drifts slowly toward the bottom of the frame. The long four-legged shadow grows larger and its edges sharpen. Thin rays of dust shoot outward along the ground in perfectly straight lines, fast and flat, crisp as if shot with a very short shutter, with no cloud and no swirling, because there is no air. At the seventh second all motion stops at once: the descent stops, the shadow is still and sharp, and the dust is gone. The last second is completely still. The craft is never visible, only its shadow. No text.
```

### P10 · Lo que vio el mundo (1:07–1:13)

- **Producción:** `seedance_2_0_mini` a 720p, fotograma inicial K10, 8 s (se montan 6) · **8 créditos por intento**, en las dos partidas: la degradación destruye el detalle a propósito y pagar más no se vería. En ffmpeg: blanco y negro, 10 cuadros por segundo con estela (`fps=10,tmix`), giro de 180° los 2 primeros segundos y encaje a 960 × 720 sobre la placa K02 al 10 %. El barrido y la nieve, en shader.
- Se genera al derecho y limpio (hechos de [[01_hechos_verificados]] §3).
- **Riesgo legal (P10 y P11).** La página de NASA advierte que la restricción de imagen puede alcanzar a astronautas con traje identificables por el contexto histórico. La figura va sin rostro, sin nombre, sin placas ni parches en el traje y muy degradada, y P10 y P11 entran en la consulta legal de la decisión D4 del guion antes de publicar.

**K10 · fotograma clave** · referencias: ninguna
```text
Stark black-and-white image in the manner of a low-resolution slow-scan television camera, very high contrast with blown-out whites, crushed shadows and soft detail. View from a camera fixed low on the side of a landing craft on the Moon, wide 20 mm-equivalent lens with slight barrel distortion. On the left, in deep shadow, the dark angular leg of the craft with a ladder. On the lowest rung of the ladder, seen from the side and facing the ladder, a bulky figure in a white pressure suit with a large square backpack and a round helmet holds the rails with both hands and lowers one boot toward the round footpad. The figure is pale and slightly translucent, like a ghost image, with no visible face, no identifiable person and no markings on the suit. Behind it, a blinding sunlit plain, a slightly tilted horizon and a pitch-black sky without stars. A vertical band of glare runs down the right side of the picture. No flag, no lettering on the craft or the suit. No scan lines and no borders. No text, no logos, no insignia, no emblems, no watermark.
```

**M10 · movimiento** (`seedance_2_0_mini`, 720p, 8 s)
```text
Static camera, 8 seconds, real time. The suited figure stays on the lowest rung, holding the rails, and very slowly lowers one boot toward the footpad with the careful floating motion of low gravity, then stops just before touching it. No climbing, no walking, no jumping. Nothing else moves and the light does not change. No text.
```

### P11 · La huella (1:13–1:23) · **plano héroe 2** (§11.3)

- **Producción, partida máxima:** `seedance_2_5` a 720p, `omni_reference`, inicial K11a y final K11, 5 s · **35 créditos por intento, 2 intentos.** Variante −30 %: `minimax_h3`, inicial y final, 5 s, `aspect_ratio: 16:9`, 10 por intento. Después, K11 congelado 5 s con un empuje de 0,5 % por segundo (ffmpeg).
- **Cámara un poco lenta** (como a 36 cuadros por segundo): los granos caen despacio por la gravedad lunar, pero en línea recta. Obturador corto: granos nítidos, sin estela.
- K11a es K11 con el borde de una suela saliendo por arriba: se genera con K11 como referencia.
- Nadie da un paso: llegamos un segundo tarde.

**K11a · fotograma clave** (solo 09b) · referencias: K11
```text
Same frame, same lens, same focus and same light as the reference image, one second earlier: the edge of a gray boot sole with tread ribs is just lifting straight up out of the print and leaving through the top of the frame, with a few grains of dust hanging below it. Only the edge of the sole is visible: no person, no markings. The sharpest and cleanest image possible, without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**K11 · fotograma clave** · referencias: ninguna
```text
Macro photograph, 100 mm macro lens at f/4, camera lying on the ground, side view at a grazing angle of about ten degrees: a single fresh boot print pressed into fine gray lunar dust, with crisp parallel tread ribs and sharp vertical walls, like a print in damp flour. A razor-thin plane of focus lies across the ribs in the lower middle of the frame; the dust before and behind it melts within a few centimetres into a soft blur. The print lies inside a large cool shadow and is lit only by soft light bounced from the sunlit ground beyond it: gentle, almost shadowless, slightly cool gray, about two to one, just enough to model each rib. In the background the hard edge of the shadow crosses the frame diagonally from the upper left toward the right, and beyond it the plain blazes in direct sunlight, five stops brighter and strongly out of focus; a thin strip of pitch-black sky runs along the very top. No boot, no person, no flag, no equipment. The sharpest and cleanest image possible, without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**M11 · movimiento** (`seedance_2_5` en la partida máxima; `minimax_h3` en la variante; inicial K11a y final K11, 5 s)
```text
Static macro shot, 5 seconds, in gentle slow motion as if filmed at 36 frames per second. In the first second the edge of the boot sole lifts straight up out of the top of the frame and is gone. A few grains of dust detach and fall straight down in perfectly straight lines, slow and weightless in the low gravity, and stop dead without bouncing or drifting, with no cloud, because there is no air. From the third second absolutely nothing moves, and the focus does not breathe. No text.
```

### P12 · Desde aquí (1:23–1:31)

- **Producción:** `minimax_h3`, fotograma inicial K12, 8 s, `aspect_ratio: 16:9` · **16 créditos por intento**, en las dos partidas. Plan B, 0 créditos: K12 fija, con la ropa, un bombillo y sus rizos en posproducción. Fotograma en `xhigh` en la partida máxima (la figura de ella).
- **K12 se genera sin Luna** y la Luna se compone **después del video** sobre la toma fija (0 créditos). La cámara **no se mueve** por eso: una cámara quieta hace exacta la composición de la Luna.
- Geografía: la escalinata del cerro Santa Ana mira al oeste, a los techos de la ciudad y los cerros bajos; el río Guayas queda al este, a su espalda, y solo se oye (la bocina). El faro, la escalinata numerada y las barandas regeneradas son de 2002: no aparecen.
- **La Luna se compone a mano:** la de las 21:56 del 20-07-1969, renderizada con el proyecto del telescopio, a 16,2° sobre el oeste, iluminada al 35 %, con el borde brillante abajo y girado 23° a la derecha **(cálculo)**. Con 50 mm mide 24 px a 1080p, su tamaño verdadero. Su centro, en P★. Es el único punto de luz que no lleva destello: es real.
- Ella es una forma oscura y desenfocada, con las proporciones de su hoja; su mirada (la barbilla) apunta a P★.

**K12 · fotograma clave** · referencias: `@ANC_PROTA_1`
```text
Night photograph, vintage 50 mm lens wide open at f/2, locked off at standing eye height, looking west and slightly upward from the top of a steep public stairway in an old hillside neighbourhood of a tropical port city in 1969. The focus is on the distance: the stairway falling away between small wooden houses with corrugated zinc roofs, laundry hanging on lines, four bare yellow tungsten bulbs that bloom into soft round highlights, and beyond, the dark rooftops and scattered warm lights of the city and low hills under a deep blue-black sky. The bulbs are the only key light: warm pools on the steps and walls, everything else falls into blue-black, about sixteen to one. The patch of sky at three fifths of the frame width and one third of the height from the top, above the roofs, is clear and empty, with a few faint stars: no Moon in the sky. In the foreground at the left third, softly out of focus and seen from behind, stands the small chibi student of the reference sheet, with her proportions, her voluminous dark curly hair, her khaki short-sleeve shirt worn open over a dark T-shirt and her brown cargo pants, barefoot on the stone step, without any bag, her chin slightly raised toward that empty patch of sky; she is a dark soft shape with a thin warm rim light from a bulb behind her on the right, and her face is not visible. No cars, no antennas, no television sets, no signs, no lighthouse, no numbered steps, no modern railings. Warm colour of 1960s 16 mm reversal film: amber bulbs, deep blue-black night, slightly lifted blacks. Clean image without film grain or borders. No text, no logos, no insignia, no emblems, no watermark.
```

**M12 · movimiento** (`minimax_h3`, 8 s)
```text
Locked-off shot, 8 seconds, real time; the camera does not move at all. Almost nothing moves: the laundry sways slightly in a light warm breeze, one bulb flickers faintly once, the girl's curls stir. At the fourth second she raises her chin very slightly toward the empty patch of sky and stays still. The sky stays empty and still. Nobody else appears. No text.
```

### P13 · Lo que dejaron (1:31–1:39) · **plano héroe 3** (§11.3)

- **Producción:** fija de 2k en **4:3** (2048 × 1536), con una ventana de 16:9 (2048 × 1152) que sube **de y = 300 a y = 0** entre 1:33 y 1:37, con arranque y frenado suaves (`smoothstep`) (ffmpeg). Fija antes y después. 0 créditos de video. Fotograma en `xhigh` en la partida máxima.
- **Ventana corregida en el pase:** con y = 384 la Tierra empezaba a 31 px del borde superior (2,7 % del alto): sin aire sobre la cabeza. Con y = 300 empieza al 10 % del alto, y la bandera y su mástil (franja y = 1152–1400 de la placa) quedan entre el 74 % y el 96 % de la ventana: enteros. El horizonte (y ≈ 1330) cae al 89 %. La inclinación equivale a unos 21° (antes, 27°) **(cálculo)**. A 1:37 (y = 0) la bandera sale entera por abajo y la Tierra queda en P★, igual que antes.
- **La bandera no hace de transición.** Entera de 1:31 a 1:35 (la imagen del homenaje: la bandera abajo y la Tierra arriba), sale entera por el borde inferior de 1:35 a 1:37, y de 1:37 a 1:39 solo quedan la Tierra en P★ y el cielo negro. El *clac* (1:38) y el apagado del tubo (1:39) actúan solo sobre la Tierra.
- Si en el animatic se lee como diapositiva, se usa una deformación de perspectiva progresiva (`perspective` de ffmpeg) en lugar del desplazamiento puro.
- **La bandera se compone a mano, una vez:** tela en Blender con la textura dibujada por script (13 franjas y 50 estrellas en 9 filas alternas de 6 y 5; dato general, no está en 01), en su barra horizontal sin extender del todo (01 §1), iluminada de frente por el Sol bajo, como en la placa. Sin módulo en el plano: no consta dónde quedó la bandera **(sv)**.
- **La Tierra se compone a mano:** a 59,1° sobre el oeste, iluminada al 64 %, con el lado iluminado hacia arriba, de 1,89° **(cálculo)**: unos 25 px con 14 mm, casi lo mismo que la Luna de P12. Termina en P★.
- El Sol, a 14,5° y a la espalda de la cámara **(cálculo)**: la Tierra y el Sol nunca comparten cuadro.
- K13 del lote es el cuadro de 1:31–1:35 (bandera y Tierra juntas), en 16:9, para el animatic. **No se le pide la bandera al modelo:** el encargo pide un paño liso y neutro en su barra; encima se pone la bandera dibujada por script (0 créditos), deformada con la forma del paño. En el fotograma final de 4:3 se hace lo mismo con la bandera de Blender.

**K13 · fotograma clave** · referencias: ninguna
```text
Low-angle ultra-wide photograph on the surface of the Moon, 14 mm lens at f/11, everything in focus, camera thirty centimetres above the ground and tilted upward, the Sun low behind the camera. Hard single-source sunlight with no fill: every pebble and boot print casts a long black shadow pointing away from the camera, toward the horizon. At the bottom right, small and complete, stands a thin vertical pole whose base sits one twentieth of the frame height above the bottom edge; at its top a plain rectangular cloth about one tenth of the frame height hangs open from a horizontal rod along its top edge, perfectly still, keeping soft permanent wrinkles because the rod is not fully extended. The cloth is a blank, smooth, light neutral gray placeholder with no stripes, no stars and no pattern, front-lit by the low sun. At the foot of the pole, gray dust trampled by boot prints. The gray horizon lies very low in the frame. Above it, an enormous pitch-black sky without stars; near the top of the frame, at three fifths of the frame width and one tenth of the height from the top, small, about one fortieth of the frame height, the Earth: a blue-and-white gibbous globe about two thirds lit, with its lit side facing up. The Earth is the only colour; everything else, the cloth included, is neutral gray and black. No spacecraft, no people, no other equipment, no lettering, no camera shadow. Crisp and without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

### P14 · El punto de luz (1:39–1:51) · **plano héroe 4** (§11.3)

- **Producción, en dos tomas:**
  - **14A,** 1:39–1:45: `minimax_h3`, 6 s, inicial K14a y final K14b, `aspect_ratio: 16:9` · **12 créditos por intento**, en las dos partidas. Un suceso: la luz sube. Con los dos extremos fijados por fotogramas aprobados, el modelo solo interpola la luz; pagar Seedance aquí no mejora la identidad.
  - **14B,** 1:45–1:51: `seedance_2_5` a 720p, `omni_reference`, 6 s, inicial = último cuadro real de 14A (sacado con ffmpeg), final K14c, con `@ANC_PROTA_1` de referencia · **42 créditos por intento, 3 intentos**, en las dos partidas. Un solo suceso: abre los ojos y sonríe con los ojos.
  - Antes, **prueba A/B** de 14B a 4 s y 480p, con **K14b como fotograma inicial**: Seedance 2.5 (12), Cinema Studio 4.0 (12) y MiniMax H3 (8) = **32 créditos** en la partida máxima; la variante −30 % omite Cinema Studio (20). Mide si cada modelo sostiene la cara horizontal sin enderezarla ni deformarla. El ganador puede sustituir a Seedance 2.5 en P04, P05, P09, P11 y 14B al mismo precio (Cinema Studio 4.0 cuesta lo mismo).
- **La lágrima se compone, no se genera.** Ningún fotograma ni clip de P14 lleva gota. La gota es un elemento pintado (perla con brillo y refracción) que se compone sobre el **lagrimal** del ojo de arriba: de 1:39 a 1:41, brillo frío en P★ con la firma del punto de luz; de 1:41 a 1:45 pasa a dorado con la franja de luz; a 1:48 cruza el puente de la nariz y deja una línea fina.
- **El pestañeo** (1:50–1:51) se resuelve con 3 cuadros editados: K14d intercalado entre dos cuadros con los ojos a medio cerrar (mezcla en ffmpeg).
- **Si la cara horizontal falla** en la prueba A/B: los fotogramas se generan con la cara en vertical y se giran 90° en ffmpeg; la dirección de la luz se pide pensando en la imagen ya girada. Reserva: 3 × 4,50 = 13,50 créditos.
- Los cuatro fotogramas se generan en una sola tanda, K14b y K14c con K14a como primera referencia, y se aprueban como set.
- Luz motivada: la brisa abre un palmo una hoja de la celosía; por eso la franja sube en 4 s **(sueño)**. La franja está rayada por las lamas de la celosía, con bordes blandos (el Sol es una fuente extensa y la celosía está lejos de la almohada).
- El lagrimal del ojo de arriba se coloca en P★ desplazando el cuadro (el 2k da margen).
- **Plan B sin video:** los tres fotogramas con disolvencias y la lágrima compuesta.

**K14a · fotograma clave** · referencias: `@ANC_PROTA_1`
```text
Extreme close-up, 100 mm macro lens at f/2, camera fixed at pillow height with the lens axis parallel to the pillow. The sleeping face of the girl from the reference sheet, the same hand-painted low-poly character: warm brown skin, big closed eyelids with thick dark lashes, round cheeks, voluminous dark curly hair. She lies on her left side, so her face is horizontal in the frame, forehead toward the right and chin toward the left, her left cheek sunk into a cream pillow, a few curls fallen over her temple and the collar of a khaki shirt over a dark T-shirt at the edge of the frame. Eyes closed, calm, mouth relaxed. A razor-thin plane of focus lies on the lashes of her upper eye; her lower eye and the far curls fall softly out of focus. The lashes and the inner corner of that eye are slightly wet, with no visible teardrop. The inner corner of her upper eye sits slightly above and to the right of the centre of the frame. It is just before dawn: the only light is faint cool skylight from a window above her head, a thin cool edge along the bridge of her nose and the lashes; the whole face is in deep petrol-blue shadow, the darkest tones warm and never pure black, and there is no warm light anywhere yet. The background melts into a soft dark blur. {ESTILO} Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**K14b · fotograma clave** · referencias: `@ANC_PROTA_1`
```text
Extreme close-up, 100 mm macro lens at f/2, camera fixed at pillow height with the lens axis parallel to the pillow. The sleeping face of the girl from the reference sheet, the same hand-painted low-poly character: warm brown skin, big closed eyelids with thick dark lashes, round cheeks, voluminous dark curly hair. She lies on her left side, so her face is horizontal in the frame, forehead toward the right and chin toward the left, her left cheek sunk into a cream pillow, a few curls fallen over her temple and the collar of a khaki shirt over a dark T-shirt at the edge of the frame. Eyes still closed, calm. A razor-thin plane of focus lies on the lashes of her upper eye. A soft-edged band of amber morning sunlight, about one fifth of the frame wide and split into two or three soft stripes by window shutter slats, lies diagonally across her jaw and cheek at about thirty degrees and has just reached the closed eyelid of her upper eye; inside the band the skin glows warm orange and the painted facets catch the light, outside it everything stays petrol-blue, about four to one. The lashes and the inner corner of that eye are slightly wet and catch a warm glint, with no visible teardrop; the inner corner sits slightly above and to the right of the centre of the frame. The background melts into a soft dark blur. {ESTILO} Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**K14c · fotograma clave** · referencias: `@ANC_PROTA_1`
```text
Extreme close-up, 100 mm macro lens at f/2, camera fixed at pillow height with the lens axis parallel to the pillow. The face of the girl from the reference sheet, the same hand-painted low-poly character: warm brown skin, round cheeks, voluminous dark curly hair. She lies on her left side, so her face is horizontal in the frame, forehead toward the right and chin toward the left, her left cheek sunk into a cream pillow, a few curls fallen over her temple and the collar of a khaki shirt over a dark T-shirt at the edge of the frame. She has just woken: her large dark-brown eyes are open, wet and bright, looking softly past the camera without focusing, with two small rectangular catchlights from the window shutters in each eye. She smiles with her eyes: the upper cheek is raised and the mouth is a small closed smile. Her eyes are moist, but there is no teardrop and no tear line on her face. Warm morning light from the window now covers the face as a soft key from the upper right: cream and soft orange light, the far side of her face still in gentle petrol-blue shadow at about three to one, and a golden rim on the curls. The feeling is quiet, overwhelming joy, not sadness. The background is a soft warm blur. {ESTILO} Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**K14d · fotograma clave** (solo 09b; edición del último cuadro de 14B) · referencias: ese cuadro, `@ANC_PROTA_1`
```text
Edit of the first reference image: the same frame, the same face, the same light, the same colours and the same expression, with both eyes fully closed in a soft blink; nothing else changes. Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

**M14A · movimiento** (`minimax_h3`, inicial K14a y final K14b, 6 s, `aspect_ratio: 16:9`)
```text
Locked-off extreme close-up, 6 seconds, real time, no camera movement and no focus change. The girl sleeps and does not move, except for a tiny flutter of her closed eyelids and slow breathing. A soft slatted band of amber morning light climbs steadily from her jaw across her cheek until it reaches her closed eyelid, the way sunlight moves when a shutter opens a little in the breeze. Her eyes stay closed until the end. Her features and the painted faceted style do not change. No tears appear. No text.
```

**M14B · movimiento** (`seedance_2_5`, 720p, `omni_reference`, inicial = último cuadro de 14A, final K14c, referencia `@ANC_PROTA_1`, 6 s, `generate_audio: false`)
```text
Locked-off extreme close-up, 6 seconds, real time, no camera movement and no focus change. Keep the girl's face exactly as in the reference sheet and the first frame, in the same painted faceted style. Seconds 0 to 1.5: she opens her eyes slowly, the lashes parting first, and the window light catches in her pupils. Seconds 1.5 to 4: she lies still, looking softly past the camera without focusing, and breathes in once. Seconds 4 to 6: she smiles with her eyes, her upper cheek rises slightly, and she holds that look. The warm morning light on her face does not change. Subtle, restrained acting; no tears, no sobbing, no blinking, no head movement, no morphing. No text.
```

### P15 · La mañana (1:51–1:58)

- **Producción:** el motor, en vivo. 0 créditos.
- K15 solo sirve al animatic y de guía de puesta en escena. **Dos animaciones nuevas** (tarea de `juego/`, con su puerta):
  - ella se sienta de golpe; mínimo aceptable: ya sentada al tomar el control;
  - Órbita levanta la cabeza sobre la caja y salta al suelo (el rig del gato solo tiene reposo y caminar); mínimo aceptable: levanta la cabeza y no salta.
- **Fotografía:** la del juego (D-013, D-015). El pase solo pide que los rayos de la ventana lleven motas de polvo (partículas del motor): son los últimos puntos de luz.

**K15 · fotograma clave** · referencias: `@ANC_HABITACION`, `@ANC_PROTA_1`, `@ANC_GATO`
```text
Same room, same furniture layout, same warm early-morning light and same fixed high three-quarter top-down game camera as the first reference image. The girl is the character of the second reference and the cat is the one of the third. The girl has just sat up abruptly on top of the rumpled blue blanket of the bed, fully dressed in her khaki short-sleeve shirt worn open over a dark T-shirt, brown cargo pants and sneakers, without her bag, her hair tousled, one hand pressed on the mattress. She is not looking at the window: she looks across the room at the workbench, where the small motorized tracking mount, the open notebook and the oscilloscope with its cyan wave are. At the foot of the bed stands the plain cardboard box sealed with a cross of tape, as in the reference, and {GATO} lies on top of the box with its tail hanging over one upper corner and one paw dangling, its head raised, looking at her. Low warm morning sun comes through the open window shutters in slanted beams, the key light of the room at about three to one, with a few bright dust motes floating in the beams; the shadows stay petrol blue. The telescope points at the window and the brown tool bag hangs from the stool. There is no television anywhere. {ESTILO} Clean image without film grain. No text, no logos, no insignia, no emblems, no watermark.
```

## 3. Reglas de continuidad

### 3.1 Ella

| Rasgo | Regla |
|---|---|
| Quién | La protagonista de hoy (PER-01), la de su hoja: tres cabezas de alto. Ni niña de 1969 ni otra edad |
| Apariciones | Tres: P01 (solo rizos; ya es la malla del juego, en el render del motor), P12 (de espaldas y desenfocada), P14 (el único rostro). En P15, la malla del juego |
| Pelo | Rizos oscuros y voluminosos, con filo de luz: frío en P01, de tungsteno en P12, dorado en P14 |
| Ropa | Como en su hoja: camisa caqui de manga corta, abierta sobre una camiseta oscura; pantalón cargo **marrón** con cinturón; pulsera oscura en la muñeca izquierda. En los encargos: «khaki short-sleeve shirt worn open over a dark T-shirt, brown cargo pants». **Sin bolso:** cuelga del taburete en P01 y P15 |
| Pies | En el cuarto, con las zapatillas de su hoja (P15 es la malla del juego). En P12, descalza **(sueño)** |
| Postura | Sobre su lado izquierdo, de cara al cuarto (P01, K01 y P14): en P14 la frente queda a la derecha del cuadro y el ojo de arriba es el derecho |
| Lágrima | Una sola, en el lagrimal del ojo de arriba, **compuesta en posproducción** (ningún fotograma generado la lleva). Antes de 1:39 no existe. De 1:39 a 1:48 es una gota en el lagrimal, en P★: fría hasta 1:41, dorada desde 1:45. A 1:48 cruza el puente de la nariz: una línea fina y una perla. Nunca un chorro. En P15 no se ve |
| Método | `@ANC_PROTA_1` en cada fotograma donde aparece. Los tres de P14, en una tanda y aprobados como set. Revisión de la cara al 200 %, en los fotogramas y en los clips (un cuadro cada 0,5 s) |

Órbita: sobre el televisor en P01, la punta de la cola en P02 y P10, y sobre la caja, en la misma pose, en P15. Collar azul con la placa cian (`@ANC_GATO`). En P01, P02 y P15 es el modelo del juego, así que la pose es la misma por construcción.

### 3.2 Color y grano: de la señal a la mañana

Resumen. La paleta completa de cada tramo, en hexadecimal y con su porqué, y los valores del shader están en §10 (pase de fotografía).

| Tramo | Planos | Color | Grano (shader) |
|---|---|---|---|
| Cuarto de noche | P01 | Azul petróleo `#516B7C`; la pantalla, blanco y negro frío | 0 % |
| Umbral | P02 | El gris toma ámbar | Barrido → grano |
| Florida | P03 a P06 | Ámbar y crema desaturados. **Primer color saturado en P04:** el fuego | 100 → 70 % |
| El vacío | P07 a P09 | Negro, plata y gris. **Único azul saturado:** la Tierra | 40 → 10 % |
| La señal | P10 | Blanco y negro quemado, dentro del tubo | Tubo |
| La Luna | P11 y P13 | Gris neutro. Únicos colores: la bandera y la Tierra (de 1:37 a 1:39, solo la Tierra) | 0 % |
| Guayaquil, 1969 | P12 | Ámbar de bombillo sobre azul negro | 80 % |
| Despertar | P14 | De `#516B7C` a `#F4A159` y `#F8C991` | 0 % |
| Mañana | P15 | Paleta maestra del juego | 0 % |

- El grano cuenta la distancia: máximo en Florida, cero en la Luna, de vuelta en Guayaquil.
- Luz lunar: el Sol siempre viene del este y bajo; cielo negro sin estrellas; ninguna sombra con relleno salvo el rebote del suelo; el Sol nunca entra en un cuadro donde esté la Tierra.
- Negros nunca puros en el cuarto ni en el 16 mm (`#322C1D` en el cuarto y en Guayaquil; `#3A3226`, un poco más levantado, en Florida); puros solo en el cielo del espacio.

### 3.3 Raccords

| Corte | Regla |
|---|---|
| P01 → P02 | Una sola toma continua del motor: la cámara arranca en el cuadro de P01 |
| P02 → P03 | La pantalla del televisor (4:3, con K03 en blanco y negro) llena el alto del cuadro; disolvencia por forma a K03 en 4:3 sobre negro. De 0:14 a 0:16 (2 s) el shader abre la máscara a 16:9 y cruza al color |
| P03 → P04 | Corte en el eje con un salto de 3 veces (del 1/6 a la mitad del alto), para que se lea como decisión |
| P03 → P04 → P05 → P06 | El cohete sube siempre por la vertical de P★ (x = 0,60), desde la torre de P03 hasta la chispa de P06. P05 corta cuando la llama toca el borde superior |
| P06 → P07 | El arco de la estela y el borde superior de la Tierra casi llena son el mismo círculo: radio 0,30 del alto, centro en (0,60; 0,66), cima en P★. La chispa llega a la cima volviéndose horizontal |
| P07 → P08 | El disco de la Tierra (25 % del alto, borde superior en P★) y el de la Luna del render coinciden en tamaño y lugar. Dentro de P08, disolvencia por forma del render al borde fino (2–3 s) |
| P08 → P09 | Corte de gris a gris, con la luminancia igualada al 5 % |
| P10 → P11 | Corte en la acción: el pie baja en la peor imagen y la bota ya sale en la más nítida |
| P11 → P12 | La frase S2 cruza el corte: la primera mitad sobre la huella, la segunda sobre su nuca |
| P12 → P13 → P14 | Luna (P12), Tierra sola (P13, de 1:37 a 1:39), punto del tubo y gota del lagrimal (P14), en P★. La bandera sale entera de cuadro a 1:37, antes del *clac* (1:38) y del apagado (1:39): el pliegue del tubo actúa solo sobre la Tierra |
| P14 → P15 | Corte en el pestañeo (3 cuadros editados). 1 s de desenfoque que baja a cero sobre el motor |
| P01 ↔ P15 | La misma cámara del motor y la misma escena. Televisor ↔ caja. Órbita, en la misma pose |

## 4. Sonido

> Afinado en el pase de fotografía (§12): el silencio, la respiración y la música se escriben con la imagen, al cuadro. Ninguna voz; ninguna nota antes de 0:48.

### 4.1 Mapa en línea de tiempo

Un carácter son 2 s. Los cortes exactos están en la tabla 1.1. Generado por script desde los tiempos de esta sección.

```text
tiempo         0:00      0:20      0:40      1:00      1:20      1:40      
planos         |01 |02|03  |04|05 |06|07 |08|09 |10|11  |12 |13 |14   |15 
respiracion    ~~~~~~~~~~~~~~~~~~~~~~··~~~~~~~·~~~~~················~~~···
tubo           =======···························===············!·········
ruido filtrado ·nnnnvvvvvv····####vv········zzz··nnn······················
radio          ·rrrr······················q····q··························
Guayaquil      gggggggg··································gggg·········mmmm
musica         ························11111···············223333333444···
golpes         ··············G················C·················K·······M·
silencios      ···········SSSS·······SS·······s·····SSSSS·················
```

Leyenda: `~` respiración, un ciclo cada 4 s · `=` zumbido del tubo · `!` el tubo se apaga · `n` siseo de nieve · `v` viento · `#` rugido · `z` zumbido mecánico · `r` tonos de radio por el parlante del televisor · `q` tono de radio del enlace (`q` de *Quindar*) · `g` noche de Guayaquil · `m` mañana · `1` a `4` las cuatro notas · `G` golpe grave (0:29) · `C` contacto (1:03) · `K` golpe blando, *clac* y apagado (1:38–1:39) · `M` maullido · `S` silencio.

**Cinco reglas que unen sonido e imagen**
1. **La respiración es el metrónomo.** Un ciclo de 4 s (15 por minuto, la de quien duerme). La música piensa en compases de 4/4 a 60 pulsos por minuto: un compás = una respiración. Cada nota entra en el arranque de una inspiración.
2. **El sonido llega tarde a lo lejano y a tiempo a lo cercano.** En P04 la luz llega primero y el golpe grave a 0:29, justo cuando el cohete se despega (5 s dentro del plano lento). En P09 y P11, sin aire, no hay sonido de lo que pasa afuera: solo lo que se oye dentro del traje.
3. **Los tres silencios crecen:** 8 s antes de la ignición (con respiración), 4 s al salir de la Tierra (sin respiración) y 10 s en la huella (sin nada). El último es el más largo y el más vacío: es el clímax.
4. **El silencio no es un corte de audio.** Debajo de cada silencio queda un piso de ruido rosa a −62 dBFS, inaudible en altavoces pero presente en auriculares, para que el jugador no crea que el sonido falló. En la huella, ese piso es lo único.
5. **El cuarto vuelve por el oído antes que por la vista.** Los grillos de P01 vuelven en P12 (la escalinata de 1969 suena como su cuarto); el zumbido del tubo vuelve en P10; el *clac* de la perilla (1:38) es lo primero del cuarto real; los pájaros de la mañana entran 1 s antes del corte a P15.

### 4.2 Plano a plano

| # | Qué se oye y cómo trabaja con la imagen |
|---|---|
| P01 | Zumbido del tubo (60 Hz y armónicos) y el silbido de 15,7 kHz del barrido NTSC a −50 dBFS: muchos adultos no lo oyen, los jóvenes sí. Siseo de nieve, grillos, ventilador. Respiración dormida. Tonos de radio por un parlante pequeño (filtro de 300 a 3000 Hz): el sonido sale **del televisor**, en el canal del centro |
| P02 | Mientras la cámara avanza, el cuarto se filtra (paso bajo de 8 kHz a 1 kHz): entramos en la pantalla. El zumbido baja una octava (60 a 30 Hz) en 4 s y se abre en ruido: es el viento de Florida. Los grillos se apagan uno a uno, uno por segundo |
| P03 | Viento y agua en la orilla, en estéreo ancho: el primer espacio abierto. A 0:21 el viento se corta en seco: quedan la respiración y el piso de ruido |
| P04 | **Primer silencio** con respiración: el fuego crece mudo en cámara lenta. A 0:29, cuando el cohete se despega, el golpe grave: ruido filtrado por debajo de 60 Hz, que se siente más que se oye |
| P05 | El rugido, a tope, con la **crepitación** del chorro supersónico (ruido con impulsos aleatorios encima del grave): el único momento en que la mezcla toca −1 dBTP |
| P06 | El rugido se aleja: el paso bajo baja de 8 kHz a 200 Hz y el nivel cae 30 dB en 4 s. Queda un hilo de viento |
| P07 | **Segundo silencio,** 4 s, sin respiración. A 0:47 vuelve la respiración, cerrada, como dentro de un casco (reverberación corta de 0,2 s y un realce en 300 Hz). A 0:48, **primera nota** |
| P08 | Respiración de casco. A 0:55, un tono de radio del enlace: un pitido senoidal de 250 ms (`q`) |
| P09 | Zumbido mecánico que sube, transmitido por la estructura (solo graves y medios). La respiración se detiene a 1:02. Contacto a 1:03: corte a nada (1 s de piso de ruido). A 1:04 suelta el aire; otro tono `q` |
| P10 | Zumbido del tubo y siseo, otra vez desde el canal del centro: volvemos al televisor. Ninguna voz |
| P11 | **Tercer silencio,** 10 s: ni música, ni radio, ni respiración. Solo el piso de ruido. Los granos caen sin sonido |
| P12 | Los grillos de P01 (la misma grabación). Un perro lejos a la izquierda. La bocina de un barco, una vez, detrás (el río está a su espalda). A 1:27, **segunda nota** |
| P13 | **Tercera nota** y, debajo, el primer acorde. A 1:38, con la bandera ya fuera de cuadro, un golpe blando de almohadilla y el *clac* de una perilla, secos y cercanos, sin reverberación: es el cuarto real |
| P14 | A 1:39, el apagado del tubo: un *tunc* grave y el silbido de 15,7 kHz que se corta. Solo queda la cola del acorde. A 1:45, **cuarta nota** y la primera toma de aire en 32 s, cerca y en el centro. A 1:48, media risa. A 1:50, los pájaros |
| P15 | La mañana de Las Escalinatas: pájaros, un bus lejano, el ventilador. Sin música. Un maullido corto. El nivel iguala al del bus de ambiente del juego: el empalme no salta |

- El tono `q` imita la forma de los tonos de control del enlace del Apolo (*Quindar*: 2525 Hz al abrir y 2475 Hz al cerrar, 250 ms; [ALSJ, «Quindar Tones»](https://www.nasa.gov/wp-content/uploads/static/history/alsj/quindar.html)). **Pendiente:** pasar el dato a [[01_hechos_verificados]] con esa fuente antes del montaje; si no se confirma, se usa un pitido genérico de 2,5 kHz. No va en pantalla.

### 4.3 Partitura de silencios

| # | Tiempo | Dura | Qué queda | Nivel |
|---|---|---:|---|---|
| 1 | 0:21–0:29 | 8 s | Respiración y piso de ruido (el fuego mudo desde 0:25) | −40 LUFS a corto plazo |
| 2 | 0:44–0:48 | 4 s | Solo el piso de ruido | −62 dBFS |
| 3 | 1:03–1:04 | 1 s | Solo el piso de ruido (el contacto) | −62 dBFS |
| 4 | 1:13–1:23 | 10 s | Solo el piso de ruido (la huella) | −62 dBFS |

La respiración contenida desde 1:13 hasta 1:45 (32 s) no es silencio: la música vuelve a 1:27, pero ella no respira hasta abrir los ojos.

### 4.4 Música: el encargo

**«Un punto de luz», tema de apertura.** Composición propia o por encargo con cesión de derechos por escrito (03 §4): la música generada sirve solo de maqueta del animatic.

| Aspecto | Encargo |
|---|---|
| Duración | 1:03 de música, de 0:48 a 1:51, más 2 s de cola bajo la mañana. Versión corta de 106 s si se aprueba el recorte D7 |
| Instrumentación | Piano vertical con fieltro (sordina), grabado muy cerca, con el ruido de los martillos y del pedal. Violonchelo solo, *sul tasto* y sin vibrato. Contrabajo con arco, en armónicos naturales, solo para los graves. Una capa opcional: el mismo piano copiado a cinta y devuelto con un *wow* del 0,3 %, el temblor de los aparatos de los 60, a −18 dB del piano. **Nada de metales, percusión, coro ni sintetizadores brillantes:** el guion excluye fanfarria e himno |
| Tempo | Libre (*rubato*) y sin pulso audible. Para sincronizar, un mapa a 60 pulsos por minuto en 4/4: un compás = una respiración de 4 s. Puntos de sincronía exactos: 0:48, 1:27, 1:31 y 1:45 |
| Armonía | Re mayor, con la tercera (fa sostenido) **retenida** hasta 1:45. 0:48: re grave solo (piano, con pedal, cuelga 9 s y se apaga antes del descenso). 1:27: la, violonchelo, sostenido. 1:31: mi sobre re y la, el primer acorde, abierto y sin modo: suena a pregunta durante 14 s. 1:45: fa sostenido en el registro medio del piano: el acorde se vuelve re mayor (con la novena): la respuesta |
| Dinámica | *pp* todo el tiempo; un solo *mp* a 1:45, sin crescendo. La cola se funde bajo la mañana entre 1:49 y 1:53 |
| Dónde calla | De 0:00 a 0:48 (nada), de 0:58 a 1:27 (el descenso, la señal y la huella: 29 s) y desde 1:51 (el juego) |
| Entregables | Pistas separadas en WAV de 48 kHz y 24 bits (piano, cuerdas, cinta) y la mezcla; partitura o MIDI; documento de cesión de derechos |
| Maqueta del animatic | En un secuenciador gratuito con un piano de muestras libre de derechos (0 créditos). Si se prefiere generada: Sonilo, 60 s = 3,75 créditos, **solo maqueta** |

### 4.5 Mezcla

| Tramo | Nivel a corto plazo | Picos |
|---|---|---|
| Cuarto (P01, P02, P10) | −30 LUFS | −12 dBTP |
| Florida antes del fuego (P03, P04) | −28 a −40 LUFS | −10 dBTP |
| Rugido (P05) | −10 LUFS | **−1 dBTP**, el único |
| Vacío y Luna (P07 a P09, P11, P13) | −32 a −62 LUFS | −14 dBTP |
| Guayaquil (P12) | −30 LUFS | −12 dBTP |
| Despertar (P14) | −26 LUFS, −22 en la cuarta nota | −8 dBTP |
| Mañana (P15) | el bus de ambiente del juego | — |

- **Integrado: −20 LUFS ± 2, con un rango de sonoridad de unos 15 LU.** Corrige los −16 LUFS del storyboard anterior: con 32 s de casi silencio, −16 obligaría a subir los silencios y se perdería el contraste. Es una mezcla de cine, no de anuncio.
- Estéreo. Lo que sale del televisor (P01, P10) va al centro y en banda estrecha; Florida y Guayaquil, anchos; el traje (P07 a P09), estrecho y cercano.

### 4.6 Lista por conseguir

| # | Sonido | Planos | Cómo se consigue | Créditos |
|---|---|---|---|---:|
| 1 | Ruido blanco filtrado: siseo de nieve, viento, rugido con crepitación, estática | P01 a P06 y P10 | Síntesis propia (ffmpeg o Python): un solo ruido con filtros distintos | 0 |
| 2 | Zumbido del tubo, su silbido de 15,7 kHz y su apagado | P01, P02, P10, P14 | Síntesis | 0 |
| 3 | Golpe grave de la ignición | P04 | Síntesis: ráfaga de ruido filtrada por debajo de 60 Hz | 0 |
| 4 | Zumbido mecánico que sube | P09 | Síntesis | 0 |
| 5 | Tonos de radio: los del parlante del televisor y los `q` del enlace | P01, P08, P09 | Síntesis: tonos senoidales de 250 ms. No se imita ninguna voz | 0 |
| 6 | Respiración: dormida, cerrada, contenida, la toma de aire final y la media risa | Todo | Grabación propia | 0 |
| 7 | Noche de Guayaquil: grillos, ventilador, perro lejano, bocina de barco | P01, P12 | Grabación propia en Guayaquil | 0 |
| 8 | Agua en la orilla | P03 | Grabación propia | 0 |
| 9 | Golpe blando de almohadilla y *clac* de perilla | P13 | Grabación propia | 0 |
| 10 | Mañana de Las Escalinatas: pájaros, un bus, el ventilador | P14, P15 | Grabación propia | 0 |
| 11 | Maullido corto | P15 | Grabación propia | 0 |
| 12 | Música: «Un punto de luz» (§4.4) | P07, P12, P13, P14 | Composición propia o por encargo, con cesión de derechos | 0 |

- Para el animatic basta una maqueta sintetizada. Lo generado (Sonilo, Mirelo) sirve solo de maqueta: su licencia para publicar está sin verificar ([[03_produccion_higgsfield]] §4).
- Capa opcional de voz con audio real de 1969 (decisión D3 del guion): **no se descarga nada** sin permiso por archivo y consulta legal.

## 5. Presupuesto

> **El pase de fotografía cambia la recomendación:** se pide la partida de máxima calidad de §5.4 (754,50; tope 783) o, si Guillermo prefiere guardar créditos, la variante de §5.5 (521,13; tope 542). §5.1 a §5.3 quedan como la partida B anterior, para comparar.

Intentos previstos: 1,5 por fotograma y por toma; 3 en la toma 14B. Tarifas de [[03_produccion_higgsfield]] §2, comprobadas por el verificador con `generate cost` (P03 20, P04 56, P10 8, P11 10, 14B 42).

### 5.1 Por plano (escenario equilibrado)

| # | Fotogramas finales (1 pasada) | Video | s | Por intento | Intentos | Video |
|---|---:|---|---:|---:|---:|---:|
| P01 | 2,75 (K01, **reserva** si no hay render del motor) | render del motor | — | — | — | 0 |
| P02 | 2,75 (K02, diseño del televisor y placa de P10) | cámara del motor | — | — | — | 0 |
| P03 | 2,75 | MiniMax H3 | 10 | 20 | 1,5 | 30,00 |
| P04 | 5,50 (K04a y K04b) | **Seedance 2.5** | 8 | 56 | 1,5 | 84,00 |
| P05 | 2,75 | MiniMax H3 | 8 | 16 | 1,5 | 24,00 |
| P06 | 2,75 | MiniMax H3 | 6 | 12 | 1,5 | 18,00 |
| P07 | 2,75 | fija, ffmpeg | — | — | — | 0 |
| P08 | 2,75 (K08) | render de LRO (2 s) + MiniMax H3 | 6 | 12 | 1,5 | 18,00 |
| P09 | 2,75 | MiniMax H3 | 10 | 20 | 1,5 | 30,00 |
| P10 | 1,00 (`medium`) | Seedance 2.0 Mini | 8 | 8 | 1,5 | 12,00 |
| P11 | 5,50 (K11a y K11) | MiniMax H3, inicial y final | 5 | 10 | 1,5 | 15,00 |
| P12 | 2,75 | MiniMax H3 | 8 | 16 | 1,5 | 24,00 |
| P13 | 2,75 (4:3) | fija, ffmpeg | — | — | — | 0 |
| P14 | 18,00 (K14a, b y c en `xhigh`, y K14d, el pestañeo) | 14A: MiniMax H3 · 14B: **Seedance 2.5** | 6 + 6 | 12 + 42 | 1,5 y 3 | 18,00 + 126,00 |
| P15 | 0 | motor | — | — | — | 0 |
| **Total** | **57,50** | 11 tomas | **81** | 224 | | **399,00** |

### 5.2 Por escenario

| Escenario | Qué incluye | Créditos | Saldo que deja |
|---|---|---:|---:|
| **A · Borrador** | Lote 09a (17 fotogramas `low`, cotizado en 4,25; tope de 6,00) y animatic con ffmpeg y sonido de maqueta | **6,00** | 847,75 |
| **B · Equilibrado** | A + fotogramas finales (57,50 × 1,5 = 86,25) + prueba A/B (32,00) + video (399,00) + escalado a 1080p de 10 tomas, todas menos P10, que se degrada a 960 × 720 (tope de 20,00, **sv**). Cuenta la partida A por su tope | **543,25** | 310,50 |
| B+ | B con la huella (P11) y la sombra (P09) también en Seedance 2.5, solo si la prueba A/B muestra una diferencia clara: +112,50 | 655,75 | 198,00 |
| **C · Máximo** | Seedance 2.5 a 720p en las 10 tomas (menos P10) con los mismos intentos (841,50), todos los fotogramas en `xhigh` (123,00), A/B, escalado y borradores | **1022,50** | **no cabe:** faltan 168,75 |
| C′ | C con un solo intento por toma y 2 en 14B | 742,00 | 111,75, sin margen para un fallo |

- Borrador en video (Seedance 2.0 Mini, 81 s × 1,5 = 121,50): no se recomienda; el animatic valida el ritmo y la prueba A/B, el movimiento.
- **Por qué B y no C:** en la tabla de votos ciegos que cita 03, Seedance 2.5 (1161) y MiniMax H3 (1134) están a 27 puntos y Seedance cuesta 3,5 veces más. En planos casi quietos, el fotograma clave decide el aspecto. Con el mismo dinero, B paga de 1,5 a 3 tomas por plano para elegir la mejor; C′ paga una. Seedance 2.5 va donde el movimiento decide: el fuego y la cara. La prueba A/B mide la diferencia con nuestro propio material antes de comprometer el resto.
- Frente al primer storyboard (532,38): P02 pasa al motor (−18,00 de video), P08 pasa a H3 sobre un fotograma fino (+18,00 de video y +2,75 de fotograma), y el pestañeo de P14 se presupuesta siempre (+4,50). Con los intentos: **+10,87**.
- Reserva fuera de B, con su propia aprobación si hace falta: la cara de P14 generada en vertical y girada (3 × 4,50 = 13,50).

### 5.3 Partida que se recomienda pedir

Por puertas; cada una se presenta con su evidencia (fotogramas al 200 %, clips revisados cuadro a cuadro cada 0,5 s) y espera el visto bueno.

| Puerta | Partida | Esperado | Tope |
|---|---|---:|---:|
| 1 | Lote 09a: borradores y animatic (ya abierta) | 4,25 | 6,00 |
| 2 | Lote 09b: 19 fotogramas finales (K01 solo si no hay render del motor); los tres de P14, como set | 86,25 | 90,00 |
| 3 | Prueba A/B de 14B, con K14b como fotograma inicial | 32,00 | 32,00 |
| 4 | Video por movimientos: I (P03 a P06) 156,00 · II (P08 y P09) 48,00 · III (P10 a P14) 195,00. Antes: los dos arreglos de `hf_generar.py` (03 §3) | 399,00 | 420,00 |
| 5 | Escalado a 1080p. Antes se mide la resolución real de la primera toma de H3: el catálogo dice «2K» y Artificial Analysis, 768p. Si sale a 1080p o más, sus tomas no se escalan | ≤ 20,00 | 20,00 |
| | **Total** | **541,50** | **568,00** |

Con el tope entero quedarían 285,75 créditos para el resto del juego. Los de suscripción caducan hacia el 2026-12-12.

### 5.4 Partida de máxima calidad (pase de fotografía, recomendada)

> Sustituye la recomendación de §5.3. Tarifas cotizadas de nuevo el 2026-11-15 con `generate cost` (0 créditos): Seedance 2.5 a 720p 35, 42 y 56 a 5, 6 y 8 s (igual con inicial y final); MiniMax H3 12 y 16 a 6 y 8 s; Seedance 2.0 Mini 8 a 8 s; GPT Image 2.6 `xhigh` 2k 4,50 (también en 4:3) y `medium` 2k 1,00. Saldo comprobado: **853,75**.

**Criterio.** El dinero va donde el ojo lo ve y donde el modelo decide la imagen: el fuego, el humo, el polvo en el vacío, el clímax y la cara. Seedance 2.5 (1.º de la tabla de votos ciegos, 1161) en esos cinco planos; MiniMax H3 (1134), a un tercio del precio, en los planos fijos o de un solo movimiento lento, donde el fotograma clave decide el aspecto; Seedance 2.0 Mini en la señal de televisión, que se degrada a propósito. Ningún modelo a 1080p nativo: el grano de 16 mm y el tubo esconden la diferencia, y el escalado cuesta 1 crédito por clip de 5 s frente a 9 por segundo de más.

| Plano | Modelo | s | Por intento | Intentos | Video | Por qué ese modelo |
|---|---|---:|---:|---:|---:|---|
| P03 | MiniMax H3 | 10 | 20 | 1,5 | 30,00 | Fijo: solo tiembla el aire |
| P04 ★ | **Seedance 2.5**, inicial y final | 8 | 56 | **2** | 112,00 | Héroe: fuego, vapor y cámara lenta |
| P05 | **Seedance 2.5** | 8 | 56 | 1,5 | 84,00 | Humo que rueda con un movimiento de cámara |
| P06 | MiniMax H3 | 6 | 12 | 1,5 | 18,00 | Fijo: una chispa y una estela |
| P08 | MiniMax H3 | 6 | 12 | 1,5 | 18,00 | Una deriva lenta sobre un fotograma fino |
| P09 | **Seedance 2.5** | 8 | 56 | 1,5 | 84,00 | Física del polvo sin aire y descenso; el último segundo, congelado |
| P10 | Seedance 2.0 Mini | 8 | 8 | 1,5 | 12,00 | Se degrada a 10 cuadros por segundo y 960 × 720 |
| P11 ★ | **Seedance 2.5**, inicial y final | 5 | 35 | **2** | 70,00 | Héroe: el clímax; granos en caída lenta y recta |
| P12 | MiniMax H3 | 8 | 16 | 1,5 | 24,00 | Fijo; casi nada se mueve |
| P14A | MiniMax H3, inicial y final | 6 | 12 | 1,5 | 18,00 | Los dos extremos los fijan fotogramas aprobados: solo se mueve la luz |
| P14B ★ | **Seedance 2.5**, inicial, final y `@ANC_PROTA_1` | 6 | 42 | **3** | 126,00 | Héroe: la cara; única toma que admite referencia del personaje junto a los dos extremos |
| **Video** | 5 tomas en Seedance 2.5 (35 s), 5 en H3, 1 en Mini | **79** | | | **596,00** | |

| Puerta | Partida | Esperado | Tope |
|---|---|---:|---:|
| 1 | Lote 09a: borradores y animatic (ya abierta) | 4,25 | 6,00 |
| 2 | Lote 09b: 18 fotogramas finales. `xhigh` 2k (4,50) en los 11 que se ven quietos o de cerca: K04a, K04b, K07, K11a, K11, K12, K13 (4:3), K14a, K14b, K14c y K14d; `high` 2k (2,75) en K02, K03, K05, K06, K08 y K09; `medium` (1,00) en K10. Una pasada: 67,00; con 1,5 intentos | 100,50 | 105,00 |
| 3 | Prueba A/B de 14B a 4 s y 480p: Seedance 2.5 (12), Cinema Studio 4.0 (12) y MiniMax H3 (8). El ganador sustituye a Seedance 2.5 al mismo precio | 32,00 | 32,00 |
| 4 | Video por movimientos, con validación tras cada uno: I (P03 a P06) 244,00 · II (P08 y P09) 102,00 · III (P10 a P14) 250,00. Antes: los dos arreglos de `hf_generar.py` | 596,00 | 620,00 |
| 5 | Escalado a 1080p de 10 tomas (todas menos P10). Antes se mide la resolución real de H3 | ≤ 20,00 | 20,00 |
| | **Total** (con la puerta 1 por su tope) | **754,50** | **783,00** |

- **Saldo que deja:** 99,25 con lo esperado y 70,75 si se agotan todos los topes. Los créditos de suscripción caducan hacia el 2026-12-12; lo que quede para el resto del juego antes de esa fecha es esa cifra. Pendientes conocidos fuera de esta partida: lote 06 (tope 8,50) y la decisión de las mallas de los vecinos (5 × 9 = 45 en Tripo).
- **Reserva fuera de la partida,** con su propia aprobación: K01 pintado si la Habitación no pasa su puerta (2,75); la cara de P14 en vertical si falla la cara horizontal (13,50).
- **Música y efectos: 0 créditos.** Síntesis propia, grabaciones propias y música compuesta o encargada con cesión de derechos (§4.4 y §4.6). Una maqueta generada para el animatic (Sonilo, 60 s, 3,75) es opcional y no se publica.
- **La puerta 3 puede abaratar la 4.** Si en la prueba A/B MiniMax H3 sostiene la cara igual que Seedance 2.5, se vuelve a cotizar P09 y P11 en H3 antes de la puerta 4 (ahorro de 115,00).
- Frente a la partida B de §5.3 (543,25): +211,25. Compra Seedance 2.5 en la columna (P05), el polvo (P09) y la huella (P11), un segundo intento seguro en los dos héroes de video (P04 y P11), calidad `xhigh` en 11 fotogramas y Cinema Studio 4.0 en la prueba A/B.

### 5.5 Variante un 30 % más barata

Para si Guillermo prefiere guardar créditos. Mantiene Seedance 2.5 en los dos planos donde el movimiento decide la emoción (la ignición y el despertar) y las tres tomas de la cara.

| Cambio frente a §5.4 | Efecto |
|---|---:|
| P05, P09 y P11 en MiniMax H3 (16, 16 y 10 por intento, 1,5 intentos) | −175,00 |
| P04 con 1,5 intentos en vez de 2 | −28,00 |
| Fotogramas: `xhigh` solo en los cuatro de P14; `high` 2k en los otros 13; K10 `medium` (pasada de 54,75, 1,5 intentos) | −18,37 |
| Prueba A/B sin Cinema Studio 4.0 (Seedance 2.5 y H3) | −12,00 |
| **Total** | **−233,37** |

| Puerta | Esperado | Tope |
|---|---:|---:|
| 1 · Lote 09a | 4,25 | 6,00 |
| 2 · Lote 09b | 82,13 | 86,00 |
| 3 · Prueba A/B | 20,00 | 20,00 |
| 4 · Video: I 156,00 · II 42,00 · III 195,00 | 393,00 | 410,00 |
| 5 · Escalado | ≤ 20,00 | 20,00 |
| **Total** (con la puerta 1 por su tope) | **521,13** (−30,9 %) | **542,00** |

- Saldo que deja: 332,62 (311,75 con todos los topes).
- Qué se pierde: el humo de la columna, el polvo del alunizaje y los granos de la huella quedan en el modelo de 1134 puntos en vez del de 1161; la huella pierde su segundo intento seguro. Ningún plano cambia de encuadre, duración ni sonido: la película es la misma.

## 6. Integración en el motor

Tarea de `juego/`, con su puerta; aquí no se tocó nada.

| Tema | Plan |
|---|---|
| Entrada | En `nucleo/interfaz.gd`, la acción `"nueva"` del menú: tras `Juego.nueva_partida()` y `menu.cerrar()`, se reproduce la cinemática y, al terminar o saltar, `Zonas.ir_a("habitacion", …)` |
| P01 y P02 | Render de la Habitación de noche con la cámara del juego y el movimiento de M02, horneado con el modo Movie Maker de Godot (`--write-movie`, 24 fps) y montado al principio del `.ogv`. Así comparten cámara y escena con P15 y la rima televisor ↔ caja es exacta. Exige la Habitación y el televisor aprobados en el motor |
| Reproducción | Un `.ogv` (Ogg Theora, 1080p, 24 fps, `-q:v 6`) con P01 a P14: 111 s. `VideoStreamPlayer` a pantalla completa en un `AspectRatioContainer` de 16:9, sobre una `CanvasLayer` propia. Variante de 720p para el perfil mínimo |
| Qué va horneado | Geometría, tiempo y composiciones: el montaje, las disolvencias, los 10 cuadros por segundo y la estela de P10, el 4:3 de P10, la Luna de P12, la bandera y la Tierra de P13, la gota de P14 y los 3 cuadros del pestañeo |
| Qué pone el shader | Grano de 16 mm por tramo (tabla 3.2), barrido, nieve y abombado del tubo, la apertura de 4:3 a 16:9 de P02 (0:14–0:16), el punto que se abre en P01 y el apagado hacia P★ al final de P13, solo sobre la Tierra. Sus valores se animan desde `tiempos.json` |
| Texto | `Label` del motor, leídos de `tiempos.json` y sincronizados con `stream_position`: R0 a R3, S1 y S2. S1 y S2 con comillas y en cursiva. Nada de texto en el video |
| Sonido | Dos pistas aparte del video (música y efectos), en los buses del juego, para que respeten los controles de volumen. Hay que medir que la deriva quede por debajo de 40 ms en 118 s |
| Saltar | Mantener Esc (o el botón equivalente) 1 s, con un anillo de progreso; cualquier tecla muestra el aviso 2 s. Salta a P15. Desde la segunda «Nueva partida», el aviso sale desde el principio |
| Empalme | La Habitación se construye **antes** de que empiece el video y queda oculta y en pausa: construirla durante la reproducción haría tropezar la decodificación. En el pestañeo se oculta la capa del video y se ve la zona, con 1 s de desenfoque que baja a cero. Entrada nueva `despertar`: ella sentada en la cama, Órbita sobre la caja. A los 6 s aparece «Habla con Órbita» y se suelta el control |
| Animaciones nuevas | Ella: dormida con respiración (P01) y sentarse de golpe (P15; mínimo: ya sentada). Órbita: levantar la cabeza y saltar de la caja (P15; mínimo: levanta la cabeza y no salta) |
| Créditos | «Imágenes recreadas con IA». «Texturas lunares: NASA/GSFC/Arizona State University (LRO) y CGI Moon Kit, NASA SVS. NASA no revisó ni respalda esta obra». «Material histórico: NASA» solo si entra material real (D3 o D4 del guion) |
| Accesibilidad | Opción «Reducir destellos»: nieve al 5 % y ningún parpadeo de campo entero por encima de 3 por segundo. Las frases S1 y S2 son subtítulos y siguen el tamaño de texto de las opciones |
| Prueba | `--prueba=cinematica`, con entradas simuladas (`Input.parse_input_event`): 1) mantener Esc y comprobar que se llega a la Habitación con el control; 2) reproducir entera y comprobar el empalme y el objetivo; 3) medir los fps de decodificación en la HD 620 |
| Tamaño | De 110 a 270 MB a 1080p (estimación de 03 §6, **sv**); con Git LFS |

Sin verificar en Godot 4.7.2, y se prueba antes de montar: que un `ShaderMaterial` funcione sobre el `VideoStreamPlayer` (si no, su textura va en un `TextureRect`); que se pueda saltar a un instante del `.ogv`; que Movie Maker hornee la Habitación con los shaders aprobados; y los fps reales con el archivo final.

## 7. Datos calculados, cambios frente al guion y decisiones

### 7.1 Cálculos de hoy (pendiente 2 del guion)

JPL Horizons, 2026-11-15. Datos crudos en `Datos/efemerides_storyboard.json`. Todos son **(cálculo)** y solo fijan la imagen; ninguno va rotulado.

| Dato | Valor | Plano |
|---|---|---|
| Luna desde Guayaquil, 20-07-1969 a las 21:56 | 16,2° sobre el oeste (azimut 264°), iluminada al 35,0 %; borde brillante abajo, girado 23° a la derecha | P12 |
| Luna en la madrugada del 12-11-2026 | Bajo el horizonte toda la noche (entre −60° y −33°): no hay Luna en la ventana | P01 |
| Tierra vista desde la nave en la travesía (16 a 19-07-1969) | **Unos tres cuartos (77 %)**: la fase de la Tierra vista desde la Luna a la llegada (19-07, 17:21 UT). Desde la posición de la Luna de cada día: 96,6 % (16-07), 92,4 % (17-07), 86,5 % (18-07); la nave no está ahí, sino camino del punto de llegada | P07 |
| Tierra desde el sitio, con la bandera en pie (21-07, 03:42 UTC) | 59,1° sobre el oeste (azimut 273°), iluminada al 64,2 %, diámetro de 1,89° | P13 |
| Sol desde el sitio | A 10,7° al alunizar y a 14,5° con la bandera, sobre el este | P09, P11, P13 |

- El guion decía «la Tierra, casi en el cenit»: está alta, a 31° del cenit. El guion ya se corrigió.
- Las coordenadas del sitio usadas (0,674° N; 23,473° E) no están en 01: hay que añadirlas con su fuente.
- Siguen abiertos los pendientes 1 (pasar a 01 los dos datos del ALSJ sobre la sombra y la Tierra), 3 (lugar de la bandera respecto del módulo) y 4 (validar la Habitación de noche y el televisor: K01 y K02 son ese concepto).

### 7.2 Cambios frente al guion

| # | Cambio | Motivo |
|---|---|---|
| 1 | P14 en dos tomas (H3 de 6 s y Seedance 2.5 de 6 s) en vez de una de 10 s | Un suceso por toma; el intento del plano más frágil baja de 70 a 42 créditos |
| 2 | P12 se genera a 8 s, no a 6 | Sin estirar la toma: +4 créditos por intento |
| 3 | P13 con 14 mm y placa 4:3, no 18 mm | Con 18 mm no caben a la vez la bandera y la Tierra a 59° |
| 4 | P★: un lugar fijo de la pantalla para el punto de luz | Hace visible el motivo sin una palabra; 0 créditos |
| 5 | P08 empieza como un disco igual al de la Tierra (render) y pasa a un borde fino en H3 | Disolvencia exacta de P07, y detalle que las texturas de LRO no dan a pantalla llena |
| 6 | 19 fotogramas finales, no 13 | Extremos de toma (K04a, K11a), el diseño del televisor (K02), K08, los tres de P14 y el pestañeo (K14d) |
| 7 | Zapatillas puestas en el cuarto; descalza solo en el sueño | P15 es la malla del juego, que lleva zapatillas |
| 8 | La brisa abre la celosía en P14 | Da causa a la franja de luz que sube |
| 9 | P01 y P02, render y cámara del motor | La rima P01 ↔ P15 exige la misma cámara; un empuje recto generado no llega a la pantalla |
| 10 | La lágrima de P14 se compone | Los modelos no la sostienen entre tomas; 14B queda con un solo suceso |

Total frente a la estimación del guion (574,76): **543,25**.

### 7.3 Decisiones para Guillermo

| # | Decisión | Recomendación |
|---|---|---|
| S1 | ¿Se aprueba el storyboard de 15 planos y 118 s? | Sí; el animatic decide el recorte a 106 s (D7 del guion) |
| S2 | ¿Se lanza el lote 09a (4,25; tope de 6,00)? | Sí: es la partida ya abierta |
| S3 | ¿Se acepta el punto fijo P★? | Sí |
| S4 | ¿P14 en dos tomas, con la lágrima compuesta? | Sí |
| S5 | ¿Zapatillas en el cuarto y descalza en el sueño? | Sí; la alternativa es descalza también en P15, con una variante de la malla |
| S6 | Presupuesto | **Partida de máxima calidad** (§5.4): 754,50, tope de 783, por puertas; deja 99,25. Si prefiere guardar créditos: la variante de §5.5 (521,13, tope de 542; deja 332,62) |
| S7 | ¿P01 y P02 en el motor? | Sí. Obliga a validar antes el concepto del televisor y la Habitación de noche (K01, K02) y a esperar a que la Habitación pase su puerta |
| S8 | ¿R1 como «Centro Espacial Kennedy, Florida · 16 de julio de 1969»? | Sí: es el sitio exacto. La alternativa, «Cabo Kennedy», era el nombre de época de la zona, no el de la plataforma |
| S9 | **La apertura es un segundo sueño** (la noche del 11 al 12) | Si se aprueba, el análisis de la Fase 2 pasa de «2 días, 2 noches y 1 sueño» a «2 sueños», y D11 cambia la escena 2.5 (decisión D14 del guion) |
| S10 | ¿Se aprueba el guion de color (§10) y la firma del punto de luz? | Sí: empalma con la paleta del juego en cuatro costuras exactas |
| S11 | ¿Todo esférico, con el sistema de focales y los cuatro planos héroe (§11)? | Sí |
| S12 | ¿Se encarga la música según §4.4 (composición propia o por encargo con cesión de derechos)? | Sí; para el animatic basta una maqueta en un secuenciador gratuito |

## 8. Lote 09a

- Archivo: `Nasa_Game/Fase_1_Arte/Exploracion/Lote_09/lote_09a_storyboard.json`. Los encargos se copian de este documento por script, bloque a bloque, sin retocarlos; el script comprueba que los 17 son idénticos a los bloques K y terminan en «No text, no logos, no insignia, no emblems, no watermark.».
- 17 trabajos: uno por plano (P01 a P13 y P15) y tres de P14. `gpt_image_2_6`, `low`, 1k, 16:9. Ids `L09_P01_cuarto_noche_borrador` … `L09_P15_manana_borrador`.
- Anclas: `@ANC_HABITACION` en P01, P02 y P15; `@ANC_PROTA_1` en P01, P12, P14a, P14b, P14c y P15; `@ANC_GATO` en P01, P02 y P15. Los otros 10 van sin referencias.
- **Composiciones del animatic, a 0 créditos,** sobre los borradores: la bandera dibujada por script en el paño neutro de K13; la Luna del 20-07-1969 en P★ sobre K12; la gota del lagrimal en K14a, b y c.
- Tras generar: lámina de contacto, revisión de cada cuadro al 200 % (insignias, letras, rostros, banderas) y animatic con ffmpeg.

- **Pase de fotografía (2026-11-15):** los 17 encargos se reescribieron en §2 y se copiaron por script al JSON. Comprobado: 17 idénticos a sus bloques K, todos terminan con las protecciones, ninguno nombra a NASA, a la misión, a personas reales, marcas de película ni obras ajenas; de 134 a 377 palabras. Las anclas no cambian.

**Cotización del 2026-11-15, repetida tras el pase de fotografía** (`python herramientas/hf_generar.py Nasa_Game/Fase_1_Arte/Exploracion/Lote_09/lote_09a_storyboard.json --solo-cotizar`):

| Trabajos | Por trabajo | Total | Tope | Margen |
|---:|---:|---:|---:|---:|
| 17 | 0,25 | **4,25** | 6,00 | 1,75 (7 reintentos) |

**Generado el 2026-11-15, de 01:46 a 01:48,** dentro de la partida de borradores que Guillermo abrió el 2026-11-14 («Empecemos por el storyboard»): 17 viñetas, 4,25 créditos; saldo 849,50. La decisión S2 queda cumplida por esa partida; las demás siguen esperando su veredicto.

![[storyboard_lamina_1.jpg]]
![[storyboard_lamina_2.jpg]]

Revisión de las 17 viñetas (Claude, a tamaño de lámina, no al 200 %): ninguna muestra insignias, letras ni rostros de personas reales. P13 trae el paño neutro donde la bandera se compone por script, y P14a a P14c vienen sin la gota, que también se compone; ninguna de las dos composiciones está hecha todavía, ni el animatic.

## 9. Correcciones tras la verificación

Dos verificadores independientes revisaron el guion, este storyboard y el lote el 2026-11-15 (datos y reglas; continuidad, viabilidad y presupuesto). Ninguno encontró problemas graves. Se corrigió todo, en los tres archivos y, donde tocaba, en [[01_hechos_verificados]] y `Datos/efemerides_storyboard.json`.

**Problemas medios**

| # | Problema | Qué cambió |
|---|---|---|
| 1 | P07: la Tierra «unos dos tercios» | Recalculado con Horizons. El verificador proponía «casi llena, ≈ 95 %», tomando la vista desde la Luna del 16 y 17-07; pero la nave va hacia el punto de llegada, y desde allí la Tierra está al **77 %** (19-07, 17:21 UT). Se fija «gibosa, unos tres cuartos» en K07, la tabla 1.1, la nota de P07, §7.1 y el JSON de efemérides, con el razonamiento |
| 2 | La bandera se usaba de transición (el gato «la apagaba») | P13 deja la bandera entera de 1:31 a 1:35, la saca entera de cuadro de 1:35 a 1:37 y termina 2 s con la Tierra sola. El *clac* (1:38) y el apagado (1:39) actúan solo sobre la Tierra. Guion G13, §4, §5 y §7; storyboard 1.1, 1.2, P13, 3.3 y 4.1 |
| 3 | P02 imposible con un empuje recto | P01 y P02 pasan al motor: render y cámara 3D reales, horneados con Movie Maker. Plan B: empuje digital sobre K01, con la pantalla del televisor mirando a la cámara. Se unifica la apertura de 4:3 a 16:9 en 2 s (0:14–0:16) |
| 4 | P01 y P15 no compartían cámara | P01 es render del motor, la misma escena y cámara que P15. Reserva: K01 pintado con una captura del motor del encuadre exacto, después de que la Habitación pase su puerta |
| 5 | `generate_audio` no existe en MiniMax H3 | Se quita de H3 (su pista se descarta con `-an`) y se fija `aspect_ratio: 16:9` en cada toma de H3. Se anotan los dos arreglos de `hf_generar.py` antes del lote de video |
| 6 | P06 → P07: la chispa llegaba a P★ bajando | Círculo con centro en (0,60; 0,66) y cima en P★, igual al disco de la Tierra. K06 («levels off at its apex»), M06 y K07 («slightly right of centre and low») corregidos |
| 7 | P08: las texturas de LRO no bastan a pantalla llena | Render de LRO solo 2 s; después, H3 de 6 s sobre K08 fino (+2,75 de fotograma y 12 por intento). Alternativa: permiso de descarga de mapas de más resolución |
| 8 | 14B: cinco sucesos en 6 s y cara horizontal | 14B solo abre los ojos y sonríe con los ojos. La lágrima se compone en el lagrimal; el pestañeo, con 3 cuadros editados (K14d). La prueba A/B mide la cara horizontal; si falla, cara en vertical y giro de 90° |
| 9 | La revisión al 200 % solo cubría fotogramas | Puerta de control por clip: un cuadro cada 0,5 s con `fps=2`, revisado al 200 %; un clip con marcas no se monta |

**Problemas leves**

| # | Problema | Qué cambió |
|---|---|---|
| 10 | R1 «Cabo Kennedy» no era el sitio exacto | «Centro Espacial Kennedy, Florida · 16 de julio de 1969». El texto pasa a 39 palabras de 40 |
| 11 | El guion decía «casi en el cenit» y 18 mm | G13: «alta sobre el oeste, a unos 59°», 14 mm; pendiente 2 del guion cerrado |
| 12 | «Víspera del día 1» | «La noche del 11 al 12 de noviembre, horas antes de que empiece el día 1» |
| 13 | «De −46° a −33°» | «Entre −60° y −33°», en §7.1 y en el JSON |
| 14 | K12 miraba al oeste hacia el río | Techos de la ciudad y cerros bajos; el río solo se oye. Añadido «no lighthouse, no numbered steps, no modern railings». K12 se genera **sin Luna** y la Luna se compone después del video |
| 15 | K13 pedía la bandera a GPT en calidad baja | K13 pide un paño liso y neutro; la bandera dibujada por script (13 franjas, 50 estrellas) se compone encima. La bandera queda entera en todo cuadro quieto |
| 16 | Créditos y atribución | Línea de créditos de las texturas de LRO y el CGI Moon Kit con «NASA no revisó ni respalda esta obra»; «Material histórico: NASA» solo si entra material real (01 §5 corregido) |
| 17 | P10 y P11, riesgo por contexto histórico | Figura sin rostro, sin nombre, sin placas y muy degradada; P10 y P11 entran en la consulta legal de D4 |
| 18 | S1 y S2 podían leerse como palabras de ella | En pantalla, con comillas y en cursiva de subtítulo de transmisión |
| 19 | K04b pedía 800 mm | «About 1800 mm lens look» desde el mismo sitio (cálculo); manda el tamaño en cuadro |
| 20 | 01 §3: 28 s cabeza abajo | Imagen desde 109:22:06, «cabeza abajo» a 109:22:11, derecha tras 109:22:34: unos 23 s (01 y guion) |
| 21 | M10 contradecía a K10 | M10: se queda en el último peldaño y baja una bota. K10: de lado, de cara a la escalera |
| 22 | Vestuario: «khaki cargo pants» | Como en la hoja: camisa caqui abierta sobre camiseta oscura y pantalón cargo marrón (K01, K12, K14a-c, K15 y §3.1). K01 fija «lying on her left side, facing the room» |
| 23 | Orden de puertas y escalado | La prueba A/B usa K14b como fotograma inicial. Se mide la resolución real de H3 antes de escalar |
| 24 | P15: faltaba la animación de Órbita | Declarada, con mínimo aceptable: levanta la cabeza sobre la caja y no salta |
| 25 | P13 y P01, fijas animadas | P01 es render del motor, con respiración. P13: si se lee como diapositiva en el animatic, deformación de perspectiva progresiva en ffmpeg |
| 26 | Contabilidad: falta el lote 08 en `trabajos.md` | No se toca aquí: lo registra el orquestador (853,75 = 868,75 − 15,00) |
| 27 | La apertura es un segundo sueño | Decisión D14 del guion y S9 aquí: si se aprueba, la Fase 2 pasa a «2 sueños» |

**Cifras que cambian:** presupuesto B de 532,38 a **543,25** (tope de 558 a **568**); fotogramas finales de 17 a 19; texto de 37 a 39 palabras. El video sigue en 81 s y 11 tomas, y el lote 09a, en 17 trabajos.

## 10. Guion de color y textura

> Del pase de fotografía (§12). Lectura sin palabras: **memoria (blanco y negro) → sueño (16 mm cálido) → vacío (sin color) → pertenencia (el ámbar del barrio) → hoy (pintado).** El color se retira a medida que ella se aleja de la Tierra y vuelve, ya como el del juego, cuando el sueño la devuelve a su escalinata.

![[guion_de_color.png]]

### 10.1 Paleta por tramo

Los colores marcados **(J)** son exactamente de la paleta maestra del juego ([[Biblia de arte]], `paleta_maestra.png`): son las costuras por donde la cinemática empalma con el juego.

| Tramo | Planos | Tiempo | Paleta | Por qué |
|---|---|---|---|---|
| 1 · Vigilia | P01, P02 | 0:00–0:15 | Sombra profunda `#1F2A31` · azul petróleo `#516B7C` (J) · lo más oscuro `#322C1D` (J) · fósforo `#D6E2EE` · cian del osciloscopio `#62E4E0` (J) · nogal `#583F22` (J) | El cuarto duerme. La única luz es una pantalla: la curiosidad como fuente de luz. El cian del osciloscopio es lo único de «hoy» encendido |
| 2 · Umbral | P02 → P03 | 0:13–0:16 | Gris de tubo `#8E8E86` → ámbar viejo `#C9A66B` | La memoria de todos (blanco y negro) se vuelve sueño propio (color), a la vez que el 4:3 se abre a 16:9 |
| 3 · La torre | P03, P04 | 0:15–0:31 | Cielo pálido `#D9D6C8` · calima `#E8DCC0` · cian desvaído `#A9B7B3` · negro levantado `#3A3226`. **Único saturado:** el fuego `#FF8A2A`, núcleo `#FFF1D6`, vapor iluminado `#F4A159` (J) | Un álbum heredado: desaturado quiere decir lejos y antes. El fuego es el primer color pleno de la película: la emoción llega antes que el ruido |
| 4 · La columna y la chispa | P05, P06 | 0:31–0:44 | Humo al sol `#F8C991` (J) · fuego en el humo `#F4A159` (J) · cielo `#B9CBD6` → índigo `#2B2F5A` | Subir es perder el aire: el cielo se oscurece hacia el espacio y el color se va con él |
| 5 · El vacío | P07 a P09 | 0:44–1:07 | Negro puro `#000000` (el único de la película: el espacio) · océano `#2A6FB5` · nubes `#F2F5F7` · atmósfera `#7FB2E5` · plata lunar `#B5B4AE` · regolito `#7D7C78` · sombra `#0B0B0C` | Pequeñez. El mundo pierde el color; lo único azul es lo que se dejó atrás |
| 6 · La señal | P10 | 1:07–1:13 | Blanco quemado `#F4F4EE` · gris `#8E8E88` · negro del tubo `#1A1A1A` · tinte frío `#DCE6EE` | Lo que vio el mundo: la imagen más pobre y la más compartida |
| 7 · La huella | P11 | 1:13–1:23 | Gris de rebote `#8C8B88` · sombra fría `#6E7276` · llano quemado `#F2EFE8` · cielo `#000000` | El clímax es nitidez y silencio: el color desaparece para que solo quede la forma de la huella |
| 8 · Desde aquí | P12 | 1:23–1:31 | Bombillo `#F4A159` (J) · halo `#FFD08A` · noche `#141B26` · zinc `#3B4650` · sombra cálida `#322C1D` (J) · Luna `#E8E4D8` | Pertenencia. El ámbar de su barrio en 1969 es el mismo del juego y del amanecer: la Luna de allá y la escalinata de acá, en una sola luz |
| 9 · Lo que dejaron | P13 | 1:31–1:39 | Cielo `#000000` · regolito al sol `#B5B4AE` · en sombra `#8A8985`. Bandera: rojo `#B22234`, azul `#3C3B6E`, blanco `#F4F4F0` · Tierra `#2A6FB5` | El único color humano en la Luna es una bandera, y encima, la casa de todos. Los colores de la bandera son de referencia y se ajustan a la tela iluminada por el Sol bajo; el blanco no llega a puro para no quemarse |
| 10 · Despertar | P14 | 1:39–1:51 | `#1F2A31` → `#516B7C` (J) · franja `#F4A159` (J) · crema `#F8C991` (J) · filo de los rizos `#DAAA25` (J) | Su propia ventana le devuelve el color al mundo: el ámbar del sueño era el de su casa |
| 11 · Mañana | P15 | 1:51–1:58 | La paleta maestra: `#F8C991` `#F4A159` `#DAAA25` `#D09880` `#AF795E` `#924930` `#516B7C` `#322C1D` `#62E4E0` | El juego. Nada se corrige en el empalme: P14 ya llegó a estos colores |

**Empalme con el juego, en cuatro costuras:**
1. `#516B7C`, la sombra del juego, es la sombra del cuarto en P01, la del despertar en P14 y la de la mañana en P15.
2. `#F4A159` aparece tres veces y siempre en lo que más importa: el vapor de la ignición (P04), los bombillos de Guayaquil (P12) y la primera luz en su cara (P14).
3. `#F8C991`, el humo al sol de Florida (P05), es la luz llena de su cara (P14) y la luz de la mañana del juego.
4. `#322C1D`, lo más oscuro del juego, es el negro del cuarto, de la película de 16 mm y de Guayaquil. El negro puro `#000000` solo existe en el espacio.

### 10.2 La firma del punto de luz

El motivo de la película tiene su propia temperatura de color: **empieza frío y termina dorado.**

| Momento | Plano | Color | Tratamiento |
|---|---|---|---|
| El tubo se enciende | P01 | `#E6F0FF` | Punto que se abre (shader) |
| La chispa en la cima | P06 | `#FFFFFF` | Destello compuesto |
| El borde de la Tierra | P07 | `#F2F5F7` | Del fotograma |
| La nave | P08 | `#FFFFFF` | Destello compuesto, 2 px |
| La Luna de 1969 | P12 | `#E8E4D8` | Sin destello: es real |
| La Tierra sola | P13 | `#2A6FB5` | Del fotograma; el tubo la pliega |
| El tubo se apaga | P14 | `#DCEBFF` | Punto que se cierra (shader) |
| La gota | P14 | `#DCEBFF` → `#FFD27A` | Gota pintada y compuesta |

- **El destello compuesto es siempre el mismo:** un disco suave de 6 px a 1080p con un halo del 2 % del ancho, sin rayos, sin estrella y sin destello alargado; sube y baja en 12 cuadros. Cuando el jugador lo ve por tercera vez, ya sabe mirarlo.

### 10.3 Textura por tramo (valores del shader)

Grano al 100 % = desviación de 6 niveles de 255 en los tonos medios, con el tamaño del grano de 16 mm a 1080p (unos 2 px). Todo se anima desde `tiempos.json`, con rampas de 1 s en los cortes por forma.

| Tramo | Negro de salida | Grano | Halación | Temblor de cuadro | Viñeta | Nitidez |
|---|---|---:|---|---|---:|---|
| Vigilia (P01, P02) | `#322C1D` | 0 % → grano en el barrido | — | — | 10 % | La del motor |
| Florida (P03 a P06) | `#3A3226` | 100 → 70 % | Roja anaranjada en el fuego y los altos (radio del 1,2 % del ancho) | 0,15 % del alto | 20 % | Desenfoque de 0,6 px: la lente de la época |
| Vacío (P07 a P09) | `#000000` | 40 → 10 % | — | — | 0 % | Plena |
| Señal (P10) | `#1A1A1A` | Tubo: 525 líneas, nieve 10 %, abombado, 10 cuadros por segundo con estela | Halo de fósforo en los blancos | Deriva vertical cada 15 s | 35 % | Baja a propósito |
| Huella (P11) | `#000000` en el cielo | **0 %** | — | — | 0 % | **La más alta de la película** |
| Guayaquil (P12) | `#322C1D` | 80 % | En los bombillos | 0,15 % del alto | 25 % | Desenfoque de 0,6 px |
| Luna (P13) | `#000000` | 0 % | — | — | 0 % | Plena |
| Despertar (P14) | `#1F2A31` | 0 % | — | — | 15 % | El desenfoque del macro se asienta en 1 s sobre el motor |
| Mañana (P15) | La del juego | — | — | — | — | La del juego |

- El grano cuenta la distancia: máximo en Florida, cero en la Luna, de vuelta en Guayaquil. La nitidez cuenta lo contrario: lo más nítido es lo más lejano (la huella).
- Opción «Reducir destellos»: nieve al 5 %, sin deriva vertical y ningún parpadeo de campo entero por encima de 3 por segundo.

## 11. Fotografía plano a plano

### 11.1 Decisiones de óptica

- **Todo esférico; nada anamórfico.** Tres razones: 1) la verdad de 1969 (el 16 mm documental y las cámaras lunares eran esféricos); 2) el destello alargado y el desenfoque ovalado del anamórfico se leen como cine de acción de hoy y competirían con el punto de luz, que debe ser el único destello de la película; 3) los modelos reproducen mal y sin constancia los defectos del anamórfico entre tomas. El cambio de formato de la película ya existe y es otro: el 4:3 del tubo que se abre a 16:9 en P02.
- **Las focales cuentan la distancia.** Florida, con teleobjetivo largo (600 y 1800 mm): el mundo visto desde lejos, aplanado, como lo vio la gente de la orilla. El vacío, con focales medias (24 a 85 mm): objetividad. La Luna, con los dos extremos: 14 mm para la escala y 100 mm macro para la intimidad. **El único 50 mm con una persona es P12:** la mirada humana normal, la de ella, en su escalinata. El despertar, con 100 mm: lo más cerca que la película se permite estar de alguien.
- Las focales son equivalentes en formato completo (35 mm). Profundidad de campo corta en todo lo humano; profunda en los paisajes.
- **Un movimiento por plano, con intención,** o cámara fija. Nunca cámara en mano.

### 11.2 Tabla

| # | Óptica | Diafragma y foco | Cámara | Luz motivada | Contraste | Movimiento e intención | Velocidad | Textura |
|---|---|---|---|---|---|---|---|---|
| P01 | La del juego (D-013) | Todo en foco | Alta 3/4 a unos 60° | El tubo: blanco azulado, con caída por distancia y un latido del 10 %. El cian del osciloscopio de contrapunto | 8:1 | Fija que **respira:** escala del 0,3 % en ciclo de 4 s, con ella | Real | Motor limpio |
| P02 | De la del juego a 35 mm | Al final, f/2,8 simulado sobre el vidrio | Baja de la altura del juego a la de la pantalla y queda perpendicular | El tubo; el reflejo de la cama al 15 % | 10:1 | Curva de Bézier en S: avanzar, bajar y girar. **Caer dentro** | Real | Barrido → grano |
| P03 | 600 mm | f/11, infinito; la calima ablanda | Trípode a la altura de los ojos, nivelada | Sol de media mañana detrás del cohete: contraluz y filo | 2:1 | Fija: la espera; nadie se mueve | Real | 16 mm, 100 % |
| P04 ★ | ~1800 mm | f/11 | La misma posición de P03 | Contraluz del Sol y el fuego desde abajo sobre el vapor y la panza del cohete | El fuego quema 3 pasos sobre el cielo; el resto, 2:1 | Fija: el peso | **Cámara lenta al 50 %** | 16 mm, halación en la llama |
| P05 | 24 mm | f/8, foco profundo | A 1 m, detrás de las siluetas, un poco hacia arriba | Sol y el fuego dentro del humo, como una linterna | 4:1 | Una sola inclinación hacia arriba al 3 % por segundo: la mirada de la orilla sigue al cohete y no lo alcanza | Real: el tiempo se pone al día con el ruido | 16 mm, 90 %; temblor del 1 % en posproducción |
| P06 | 50 mm | f/8, infinito | Casi al cenit | El Sol, desde abajo del cuadro, sobre la estela | 3:1 | Fija: dejarlo ir | Real | 16 mm, 70 % |
| P07 | 24 mm | f/8 | Desde la nave, sin horizonte | Sol duro arriba a la derecha, sin relleno | Extremo, negro puro | Alejamiento digital que arranca rápido y frena: la nave se va | Real | Grano 40 % |
| P08 | 85 mm (y render) | f/8 | Desde la nave | Sol rasante desde la derecha, en el terminador | Extremo | Deriva lateral al 2 % por segundo y un acercamiento leve | Real | Grano 25 % |
| P09 | 35 mm | f/11 | Cenital, de 30 m hacia abajo | Sol a 10,7° desde abajo del cuadro; solo el rebote del suelo | El mayor de la película | Descenso constante y parada en seco; el último segundo, congelado | Real; obturador corto (polvo nítido) | Grano 10 % |
| P10 | 20 mm con barril | Fijo | Baja, en el costado del módulo | Sol detrás; la figura, en sombra, se vuelve fantasma | Quemado | Fija | 10 cuadros por segundo con estela | Tubo |
| P11 ★ | 100 mm macro | f/4: plano de foco de milímetros en las costillas | A ras del suelo, lateral, a unos 10° | Rebote del suelo soleado dentro de la sombra del módulo; el fondo, 5 pasos más claro | 2:1 en la huella | Fija; después, empuje del 0,5 % por segundo sobre el cuadro congelado, hacia la punta | **Un poco lenta (36 cuadros por segundo);** obturador corto | Sin grano: el plano más nítido |
| P12 | 50 mm de época | f/2: la ciudad en foco, ella desenfocada | De pie, a la altura de los ojos, un poco hacia arriba | Cuatro bombillos de tungsteno (2700 K): clave y filo. La Luna, compuesta | 16:1 | Fija, para que la Luna compuesta sea exacta | Real | 16 mm, 80 %; halación en los bombillos |
| P13 ★ | 14 mm | f/11, todo en foco | A 30 cm del suelo, inclinada 35° hacia arriba | Sol bajo a la espalda: la bandera de frente; las sombras apuntan al horizonte | Extremo, cielo negro | Fija, inclinación de unos 21° con arranque y frenado suaves, fija: de lo que dejaron a donde volvieron | Real | Sin grano |
| P14 ★ | 100 mm macro | f/2: foco en las pestañas del ojo de arriba | A la altura de la almohada, eje paralelo a ella | Luz fría del cielo antes del alba → franja de sol rayada por la celosía (la brisa abre una hoja) → la ventana entera | 6:1 → 4:1 → 3:1 | Fija: se mueven la luz y ella | Real | Pintado, sin grano |
| P15 | La del juego | — | La del juego (D-013) | El sol de la mañana por la celosía, con motas de polvo | La del juego (D-015) | La del juego | Real | Motor en vivo |

### 11.3 Planos héroe

Cuatro planos que deben quedar en la memoria. Llevan el mejor modelo, más intentos, fotogramas `xhigh` y la composición más cuidada. Además, un **plano firma** gratuito: el reflejo de P02.

**1 · P04, la ignición (0:24–0:31).**
- Composición: el cohete en la vertical x = 0,60, del 25 % al 75 % del alto; la torre, una vertical oscura a su izquierda. La franja de marisma y agua, abajo, por debajo del 82 %. El fuego (el primer color saturado de la película) en la base, a la derecha del centro y abajo; el vapor se abre en horizontal por el tercio inferior: una cruz de vertical y horizontal. El cielo de arriba a la izquierda queda vacío.
- Recorrido del ojo: fuego → cuerpo del cohete → la vertical por la que subirá hasta P★.
- Tiempo: 5 s de fuego mudo en cámara lenta; el golpe grave cuando la base se despega. El corte llega cuando el cohete subió un quinto de su altura.

**2 · P11, la huella (1:13–1:23).**
- Composición en tres franjas, la Luna entera en tres valores: abajo, la huella gris y fría en la sombra; en medio, el llano que arde de blanco, desenfocado; arriba, un 6 % de cielo negro. El borde de la sombra cruza en diagonal, de (0; 0,30) a (1; 0,45).
- La huella en el tercio inferior, en diagonal (talón abajo a la izquierda, punta arriba a la derecha): las costillas son líneas que llevan el ojo hacia el borde de la sombra y la luz.
- Tiempo: un segundo de bota que se va y granos que caen; 9 s de quietud. Ni música ni respiración.

**3 · P13, lo que dejaron (1:31–1:39).**
- Composición inicial: la bandera entera abajo a la derecha (del 74 % al 96 % del alto, hacia x = 0,80) y la Tierra arriba, en x = 0,60 y al 10 % del alto: una diagonal corta de la bandera a la Tierra, la línea del homenaje. El 70 % del cuadro es cielo negro: lo humano es pequeño. Las huellas y sus sombras apuntan hacia el mástil.
- Movimiento: la mirada deja la bandera, que sale entera por abajo, y sube hasta la Tierra, que llega a P★. Composición final: la Tierra sola, del tamaño de una uña, en el negro.
- La bandera nunca se corta en un cuadro quieto y nunca hace de transición.

**4 · P14, el ojo y la lágrima (1:39–1:51).**
- Composición: la cara en horizontal; el lagrimal del ojo de arriba en P★ (0,60; 0,36). La franja de luz entra en diagonal a 30°, de la mandíbula (abajo a la izquierda) al párpado. Los rizos llenan el tercio derecho, desenfocados; la almohada crema, el tercio inferior.
- La gota es el último punto de luz de la película: fría en el lagrimal, dorada cuando la toca la franja. Dos brillos rectangulares de la celosía en cada ojo cuando los abre.
- Tiempo: 6 s de luz que sube, 6 s de ojos que se abren y sonríen, y el corte en el pestañeo.

**Plano firma · P02, el reflejo (0:13–0:15).** En el vidrio curvo, sobre la imagen del cohete, flota su silueta dormida: ella está dentro de lo que sueña. 0 créditos (§2, P02).

## 12. Pase de fotografía

Hecho el 2026-11-15. **No cambia la historia, los datos, los 15 planos, las duraciones montadas ni las 39 palabras en pantalla.** Cambia cómo se ve y se oye cada plano, y cuánto se gasta en cada uno.

| # | Qué cambió | Por qué |
|---|---|---|
| 1 | Guion de color con la paleta de cada tramo en hexadecimal y su porqué (§10.1) | La progresión estaba en una tabla de cuatro colores; ahora cada tramo tiene su paleta y cuatro costuras exactas con la paleta del juego |
| 2 | Firma del punto de luz: un solo destello compuesto y una temperatura que va de fría a dorada (§10.2) | Hace del motivo una regla visual que el jugador aprende sin palabras |
| 3 | Valores del shader por tramo: negro, grano, halación, temblor, viñeta y nitidez (§10.3) | La textura de época se ajusta sin regenerar y se puede medir |
| 4 | Todo esférico; sistema de focales por distancia; un movimiento por plano (§11.1) | Verdad de época, un solo destello en la película y constancia entre tomas |
| 5 | Tabla de fotografía de cada plano: óptica, foco, altura, luz motivada, contraste, movimiento, velocidad y textura (§11.2) | Lo pedía el listón: si un plano no declara su óptica y su luz, no entra ([[02_lenguaje_visual]], «Listón») |
| 6 | Cuatro planos héroe (P04, P11, P13 y P14) y un plano firma (P02), con su composición (§11.3) | Concentra la calidad y los intentos donde se queda la memoria |
| 7 | Los 17 encargos del lote 09a y los de K04a, K11a y K14d, reescritos con óptica, diafragma, altura, luz, contraste, película, movimiento y duración (§2) | De «correcto» a «cine»; se mantienen las protecciones y las referencias |
| 8 | El vuelo sube por la vertical de P★ (x = 0,60) de P03 a P06 | El ojo sigue una sola línea desde la torre hasta la chispa |
| 9 | P04 en cámara lenta al 50 %; el golpe de 0:29 coincide con el despegue | El silencio dura más y el sonido llega con el peso, no con la luz |
| 10 | P05 a velocidad real | Contraste con P04: el tiempo se pone al día con el ruido |
| 11 | P09: 8 s generados y el último segundo congelado (antes, 10 s) | La quietud del contacto es absoluta; −2 s de video |
| 12 | P11: cámara un poco lenta, obturador corto, plano de foco de milímetros, 2:1 en la huella y fondo 5 pasos más claro | El clímax tiene que ser el plano más nítido y más quieto |
| 13 | P13: la ventana empieza en y = 300 (antes, 384); inclinación de unos 21° | La Tierra tenía 31 px de aire sobre ella; ahora, el 10 % del alto. La bandera sigue entera |
| 14 | P14: franja rayada por las lamas, brillos de la ventana en los ojos, contraste de 6:1 a 3:1; 14A en MiniMax H3 en las dos partidas | Luz motivada y legible; con los dos extremos fijados, Seedance no mejora la identidad en 14A |
| 15 | P01 respira (escala del 0,3 % cada 4 s); P02 refleja la cama en el vidrio | Dos detalles de cine a 0 créditos |
| 16 | K06, K07 y K08: estela iluminada, borde superior de la Tierra iluminado con su línea de atmósfera, cima del limbo lunar en P★ | El raccord por forma de P06 → P07 → P08 cae sobre un punto de luz |
| 17 | Sonido: la respiración como metrónomo, silencios con piso de ruido a −62 dBFS, crepitación del rugido, filtrado de entrada en P02, tonos del enlace (pendientes de pasar a 01) y apagado del tubo (§4) | El silencio, la respiración y la música trabajan con la imagen, al cuadro |
| 18 | Mezcla integrada a −20 LUFS (antes, −16) | Con 32 s de casi silencio, −16 aplastaba el contraste |
| 19 | Encargo de música escrito: instrumentación, tempo, armonía, dinámica, dónde entra y dónde calla, entregables (§4.4) | Se puede encargar ya |
| 20 | Partida de máxima calidad: **754,50** (tope 783,00); variante un 30,9 % más barata: **521,13** (tope 542,00) (§5.4 y §5.5) | Cotizadas otra vez hoy; sustituyen la partida B (543,25) |
| 21 | Lote 09a actualizado y vuelto a cotizar: 17 trabajos, **4,25** (tope 6,00). No se generó nada (§8) | Los borradores ya deben mostrar la fotografía nueva |

**Pendientes del pase**
- Pasar a [[01_hechos_verificados]] los tonos del enlace (2525 y 2475 Hz, 250 ms) con su fuente del ALSJ antes del montaje.
- Comprobar en el animatic tres cosas que solo se ven en movimiento: el ritmo de la cámara lenta de P04, la inclinación de 21° de P13 y la respiración de la cámara de P01 (si se nota, se baja al 0,15 %).
- El sistema de focales y los planos héroe se validan con Guillermo junto con el storyboard.
