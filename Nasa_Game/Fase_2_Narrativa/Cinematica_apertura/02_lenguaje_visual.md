# Cinemática de apertura: lenguaje visual y sonoro

> Estado: **propuesta, sin validar.** Guillermo la valida junto con el guion y el storyboard, antes de gastar créditos. Se reproduce al pulsar «Nueva partida» y termina donde empieza la misión 1 «La convocatoria» (primer paso: hablar con Órbita).
> Datos: [[03b_verificacion_apolo]] y [[03a_verificacion_ecuador]]. Historia: [[Fase 2 - Analisis]]. Estilo: [[Biblia de arte]].
> Listón: cine, no «correcto». Cada plano declara su óptica, su luz motivada, su movimiento y su sonido; si no puede declararlos, no entra.

## 1. Puesta en escena contemplativa (solo principios del referente)

| Principio | Regla aplicable |
|---|---|
| Plano largo | 6 a 12 s por plano, nunca menos de 4 s. Entre 12 y 15 planos en 110 s. El corte llega un segundo después de lo cómodo. |
| Escala humana | Lo humano (niña, traje, cohete lejano) ocupa menos del 10 % del cuadro, en el tercio inferior; el resto es cielo, humo o suelo. Lo inmenso se mide con algo pequeño. |
| Silencio | Tres silencios de 2 a 3 s: antes de la ignición, al salir de la atmósfera y antes de la huella. El silencio es el plano más fuerte. |
| Música tardía | Ni una nota antes del segundo 45. Entra cuando el rugido muere, no encima. |
| Primer plano emocional | Solo tres de la niña: ojos iluminados por el tubo, rostro dormido, ojos que se abren con la lágrima. Teleobjetivo (85 a 135 mm), foco en el ojo cercano. |
| Un movimiento por plano | Empuje, grúa o paneo lento (2 a 5 % del cuadro por segundo), o cámara fija. Nunca dos movimientos ni cámara en mano dentro del sueño. |
| Rótulos sobrios | Del motor, no del video. Fuente fina, blanco al 80 %, abajo a la izquierda, 3 s con fundido de 0,5 s. Máximo 4: lugar y año, y nada más que el guion no justifique. |

**Óptica por movimiento:** I, 35 mm a la altura de los ojos de la niña sentada (íntimo). II, teleobjetivo largo y aplanado para el cohete (la torre y el humo apilados), gran angular de 18 a 24 mm para la Tierra que se aleja. III, gran angular bajo, a ras del regolito, para la escala; 100 mm macro para la huella. Profundidad de campo corta en todo lo humano; profunda en los paisajes.

**Luz motivada:** I, una sola fuente, el tubo (azul frío en su cara), y un resto cálido de lámpara en el fondo. II, el Sol duro sobre el humo blanco. III, Sol bajo y rasante, sin relleno: sombras negras y largas, cielo negro; la Tierra es la única luz azul. Despertar: la ventana de la mañana.

## 2. Guion de color

| Tramo | Paleta | Textura |
|---|---|---|
| Habitación de noche | Sombra azul petróleo `#516B7C`, oscuro `#322C1D`, luz del tubo blanco azulada | Limpia, digital, grano mínimo |
| La imagen del televisor | Blanco y negro con tinte frío; negros nunca puros | Tubo (§3) |
| Dentro del sueño, despegue | Ámbar y crema desaturados de película de 16 mm; humo `#F8C991` al sol | Grano medio, negros levantados, parpadeo leve |
| Viaje y Luna | Plata y gris neutro; la Tierra, único azul saturado | Grano que baja a medida que se aleja de la Tierra: el sueño gana nitidez |
| Blanco del despertar | Del blanco puro al crema `#F8C991` | Sin grano |
| Mañana en Las Escalinatas | Paleta maestra: `#F8C991`, `#F4A159`, `#DAAA25`, sombras `#516B7C` | Low-poly pintado del juego |

Lectura que debe quedar sin una palabra: **memoria (blanco y negro) → sueño (16 mm cálido) → hoy (pintado)**.

## 3. Los años 60 y el televisor de tubo

- **Formato:** la imagen de 1969 vive en 4:3 dentro del 16:9. A los lados se ve el mueble del televisor y la habitación en penumbra, no barras negras.
- **Tubo:** esquinas redondeadas, barril leve, viñeta, líneas de barrido (Ecuador usa NTSC, 525 líneas), halo de fósforo en los blancos, nieve del 5 al 15 %, una deriva vertical cada 15 a 20 s.
- **Dato que se vuelve estética (confirmado):** la cámara lunar del Apolo 11 era de barrido lento, 10 cuadros por segundo y 320 líneas, en blanco y negro. Para emitirla se volvió a filmar un monitor y se convirtió a NTSC; por eso las figuras se ven fantasmales y con estela. Las imágenes de la Luna en el televisor llevan ese fantasma: estela en lo que se mueve y contraste quemado. Fuentes: [NASA, informe de las cintas del Apolo 11](https://www.nasa.gov/wp-content/uploads/static/history/alsj/a11/Apollo_11_TV_Tapes_Report.pdf) y [Parkes, CSIRO](https://www.parkes.atnf.csiro.au/news_events/apollo11/tv_from_moon.html). Que el despegue se emitiera en color: **sin verificar**, no se usa.
- **Reflejo:** en el vidrio curvo, la silueta de la niña y la lámpara, al 10 a 20 %. Se compone en posproducción.
- **Película de 16 mm** (dentro del sueño): grano, polvo y rayas suaves, halación en los altos, leve respiración de exposición.
- **Regla:** todo filtro de época se aplica en posproducción o en un shader del motor, sobre planos generados limpios. Así es uniforme y se ajusta sin regenerar.

**Transiciones de sueño:**
1. *Entrar:* empuje lento al televisor; las líneas de barrido se vuelven grano; el 4:3 se abre a 16:9 en 3 a 4 s. El marco del tubo se disuelve como un párpado.
2. *Dentro:* sin cortes duros; disoluciones por forma (el humo blanco se vuelve nube, la nube se vuelve el gris lunar).
3. *Salir:* el Sol lunar quema el cuadro a blanco; el blanco vira a crema y se vuelve la luz de la ventana. Variante: un instante de nieve («se apagó la tele») y corte a sus ojos.

## 4. Estructura emocional (100 a 115 s)

| Movimiento | Duración | Qué se ve | Arco |
|---|---|---|---|
| **I. Vigilia y umbral** | 25 a 30 s | Habitación de noche; la luz del tubo en su cara; en la pantalla, el cohete en la plataforma. Sus párpados pesan. Empuje y entrada en la imagen. | **Asombro** |
| **II. Despegue y viaje** | 35 a 40 s | Ignición vista de lejos, la columna de humo, el cohete diminuto en un cielo enorme; silencio al salir de la atmósfera; la Tierra que se aleja, entera. | **Pequeñez** |
| **III. Alunizaje, huella y despertar** | 35 a 45 s | Descenso sobre el gris, el polvo que se aquieta; la bota y la huella; la bandera en su barra; la Tierra en el cielo. Blanco. Sus ojos se abren, la lágrima, la sonrisa; se incorpora. | **Pertenencia → decisión** |

- El clímax es **la huella**, no el alunizaje: el plano más quieto y silencioso, 8 a 10 s sin música.
- La decisión se muestra, no se dice: tras la lágrima mira la ventana, sonríe y se sienta de golpe. Corte al control del jugador.
- Quién es la niña lo fija el guion (`01_guion`). La regla visual sirve para las dos opciones; si es la protagonista de hoy, el último primer plano debe calzar con [[L02_protagonista_tipo1_hoja.png]]. En 2026 nadie de su edad vio 1969 en directo: la imagen del tubo es una **grabación** y nunca se presenta como directo.

## 5. Sonido

| Movimiento | Se oye | Música |
|---|---|---|
| I | Zumbido del tubo (15,7 kHz de NTSC, muy bajo), siseo de nieve, grillos y la ciudad lejana de Guayaquil, su respiración. Voz de control de tierra filtrada (archivo, si se aprueba). | Ninguna |
| II | Cuenta atrás (archivo) → **silencio de 2 s** → rugido grave que satura y hace temblar el cuadro → corte en seco al vacío. Solo latido y respiración. | Entra al morir el rugido: tema de pocas notas, piano o cuerdas graves, muy lento |
| III | Radio del descenso con pitidos de comunicación (archivo, inglés con subtítulo); **silencio** en la huella; la frase histórica si el guion la usa. En el blanco, el latido se acelera; luego la mañana: pájaros, un bus lejano, el ventilador, un ronroneo. | Crece en la bandera y la Tierra; se resuelve en un acorde cálido al abrir los ojos y cede ante el primer sonido del juego |

- El audio de 1969 se **propone, no se descarga**: se documenta la fuente primaria y se pide permiso por archivo.
- Horas y frases solo desde [[03b_verificacion_apolo]]. Hoy 03b no trae las horas del despegue ni del alunizaje: **sin verificar**, fuera de pantalla hasta confirmarlas.
- Mezcla en 5.1 o estéreo ancho; el rugido es lo único que llega al tope. El vacío lunar se oye desde dentro del traje: respiración, radio, nada más.

## 6. Escribir para el video generativo (guion producible)

**Funciona:** planos de 4 a 12 s desde un **fotograma clave aprobado**; un sujeto; cámara fija, empuje, paneo o grúa lenta; humo, polvo, luz, partículas, paisajes; rostros quietos con cambios leves.
**Falla:** texto y logotipos (se deforman); manos en primer plano con tareas finas; multitudes con caras; continuidad de más de un plano; mecánica exacta (la separación de etapas real); cifras en instrumentos; física de baja gravedad (tiende a caminar como en la Tierra: preferir planos sin pasos o a cámara lenta justificada por el sueño).

**Reglas:**
- Un plano = un fotograma clave + una acción + un movimiento de cámara, de 5 a 10 s.
- Los modelos de **primer y último fotograma** (en el catálogo: `kling_o3_flf`) sirven para las transiciones: se fijan los dos extremos y el modelo hace el puente.
- Astronautas siempre de espaldas, en silueta o con el visor dorado bajado. Ninguna cara ni semejanza real.
- Ni insignias, ni parches, ni la palabra NASA, ni emblemas en ningún fotograma; revisión ampliada de cada uno. El cohete y el módulo se piden por forma («cohete blanco de tres etapas», «módulo dorado de cuatro patas»), sin texto en el fuselaje.
- La bandera de EE. UU. entera, con dignidad, en su barra horizontal (no hubo viento; 03b, L10).
- La niña: su hoja va como referencia en cada fotograma; misma ropa de dormir, peinado y luz. Sus tres primeros planos se generan en una sola sesión y se aprueban como set.
- Cotizar con `higgsfield.cmd generate cost` y anotar la partida antes de generar: fotogramas en borrador barato; video solo de los aprobados.

## 7. Puente con el juego

- **El último plano es el primero del juego:** cámara alta 3/4 sobre la cama, como [[L05_A_manana_calida_final.png]]. Desde el primer plano de sus ojos, grúa hacia arriba hasta ese encuadre, o corte en el pestañeo.
- **El último fotograma se genera desde una captura del motor** (como último fotograma del modelo de primer y último fotograma): cama, ventana y Órbita en el mismo sitio que en la partida.
- **Fundido de estilo en 2 a 3 s:** el grano y el desenfoque bajan a cero mientras el video se mezcla con el render en vivo; misma luz de ventana (`#F8C991` y `#F4A159`), mismas sombras `#516B7C`.
- **Órbita** aparece solo en ese plano final, ya con el aspecto del juego, mirándola: es el ancla entre el sueño y la partida, y el primer objetivo de la misión 1.
- El primer sonido del juego (pájaros de la mañana) empieza 1 s antes del corte, para que no se note la costura.
