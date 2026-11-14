---
tipo: propuesta
fase: 2 (narrativa y misiones)
angulo: misión científica
fecha: 2026-11-12
estado: borrador para el veredicto de Guillermo
fuentes: "[[01_datos_espaciales_ecuador]], [[03a_verificacion_ecuador]], [[03b_verificacion_apolo]], [[02_historia_existente]]"
---

# Propuesta B · «La bitácora de una noche»

> **Ángulo:** misión científica. Cada escena enseña un dato real y verificable con una mecánica jugable, y la historia hila esas misiones.
> **Pedido de Guillermo (2026-11-12):** historia de al menos 1 h, más contenido espacial, sueño lunar al acostarse, ver el Apolo, banderas de EE. UU. y Ecuador juntas y escenarios en orden (1 Habitación, 2 Telescopio, 3 Luna) unidos como mundo abierto.
> **Duración propuesta:** **85 min** de ruta principal y **41 min** de misiones secundarias. Un jugador un 30 % más rápido que el medio sigue por encima de 60 min (85 × 0,7 ≈ 60).

Los códigos entre corchetes (A1, E3, L6, R1…) remiten al informe [[01_datos_espaciales_ecuador]], **con las correcciones de [[03a_verificacion_ecuador]] y [[03b_verificacion_apolo]]**. Lo que no tiene fuente en esos informes va marcado como *(pendiente de verificar)*.

---

## 1. Premisa, tono y tema

**Premisa en 3 líneas**

1. Una tarde de noviembre en Guayaquil, una estudiante de ingeniería de control tiene hasta las 08:00 para entregar una bitácora de observación con datos medidos, el requisito de una convocatoria de prácticas en un centro espacial ficticio.
2. Con Órbita, su gato científico, repara una antena y un telescopio, sube al Mirador del Faro y mide la Luna real de esa noche antes de que se ponga a las 21:07.
3. Al acostarse sueña que camina por la Luna: aplica cada lección, mira el sitio del Apolo 11 sin tocarlo y planta juntas las banderas de Ecuador y EE. UU.; despierta y entrega una bitácora que solo podía escribirse desde la línea ecuatorial.

**Tono.** Cálido y costumbrista en Guayaquil, con humor costeño suave (Órbita, Lidia, Rafael). Preciso cuando habla la ciencia: cada cifra lleva unidad y fuente en el cuaderno. En la Luna, asombro y silencio: el vacío no transmite sonido, así que solo se oyen el traje, la respiración y la radio.

**Tema.** *Lo que se mide bien se puede compartir.* Observar, registrar y respetar lo que otros dejaron es la forma de llegar lejos. Las banderas expresan cooperación, no posesión (Tratado del Espacio, art. II [R1]).

**Arco emocional.** La protagonista duda de que una observación «desde el barrio» valga algo. Descubre que Ecuador ya tiene historia espacial real (la estación del Cotopaxi, el disco del Apolo 11, Pegaso, los Acuerdos Artemisa) y que la Luna vista desde el ecuador es distinta: se ve acostada, «sonriente». El sueño le da la imagen de lo que quiere construir, y su observación original resulta ser justo esa Luna de Guayaquil.

**Regla de oro del guion.** Ningún dato se presenta como examen. Se aprende haciendo: una mala elección muestra la consecuencia, Órbita explica la causa y se reintenta sin castigo. El cuaderno distingue con un sello **«Dato medido»**, **«Simulación»** y **«Sueño»**.

---

## 2. Estructura en actos

### 2.1 Tabla de escenas

Escenarios: **1** Habitación (cuarto-taller), **1b** Casa y Las Escalinatas, **1c** Sendero del arroyo (escena v1), **2** Mirador del Faro y telescopio, **3** Luna en el sueño.

| # | Escena | Escenario | Objetivo | Mecánica jugable | Qué se aprende (dato real) | Min |
|---|---|---|---|---|---|---:|
| — | Título y elección de protagonista | Menú | Elegir PER-01 o PER-02 | Selector de cuerpo base | — | *(no cuenta)* |
| **Acto I** | **«La tarde de la convocatoria»** · 17:00–18:30 | | | | | **25** |
| 1 | La convocatoria | 1 Habitación | Leer la carta y revisar el taller | Exploración libre; inspeccionar 8 objetos del taller (TAL-01 a TAL-14) | Qué es una bitácora científica: fecha, hora, lugar, instrumento y unidad en cada entrada | 4 |
| 2 | Un satélite cabe aquí | 1 Habitación | Reparar la maqueta de Pegaso (TAL-11) | Circuito: conectar panel, batería, radio y antena en la protoboard (TAL-06) y medir con el multímetro (TAL-04) | NEE-01 Pegaso, primer satélite ecuatoriano: cubo de 10 cm, dos paneles de 27 cm, lanzado el 25-04-2013 (hora de Ecuador, según el equipo); proyecto iniciado en 2010 [E3, E4, 03a] | 6 |
| 3 | La caja de Rafael | 1b Casa | Recoger el motor que llegó y la libreta | Diálogo y entrega de objetos | Un motor paso a paso sirve para seguir el cielo (se usa en la escena 7) | 3 |
| 4 | Por Las Escalinatas | 1b Escalinatas y plaza | Conseguir batería (COL-07) y cable (COL-06); saludar a Lidia | Exploración y recolección; se abre el mapa del cuaderno | El Planetario de la Armada de Guayaquil abrió el 24-07-1984 (folleto de Lidia) [E8] | 4 |
| 5 | Rastrear como en el Cotopaxi | 1c Sendero | Levantar la antena caída (COL-01) y seguir un satélite | Reparar y apuntar a mano; después ajustar la ganancia de un control proporcional: poca ganancia se atrasa, mucha oscila | Control por realimentación (error = objetivo − posición). La estación Quito, al pie del Cotopaxi, rastreó naves de 1957 a 1981 con antenas de 12 m; apoyó al Apolo-Soyuz (1975) y se despidió del transbordador STS-2 el 14-11-1981 [A1, A2, 03a] | 8 |
| **Acto II** | **«La noche del Mirador»** · 18:30–21:10 | | | | | **22** |
| 6 | La Luna sonriente | 1c → 2 Subida al faro | Llegar al Mirador y encontrar la Luna | Orientación con altura y acimut en el cuaderno; la Luna baja en tiempo de juego | La creciente se ve al oeste tras la puesta del Sol y baja: 38,8° a las 18:00, 20,0° a las 19:30, 0,8° a las 21:00. Cerca del ecuador se ve acostada [[Mirador del Faro - Luna con datos reales]] | 4 |
| 7 | Un polo en el horizonte | 2 Mirador | Montar el motor y alinear la montura ecuatorial (MIR-03) | Alinear el eje polar casi horizontal; probar el seguimiento | En Guayaquil (≈ 2,2° S) el polo celeste está a unos 2° del horizonte y la Polar no se ve; el motor gira a unos 15° por hora *(pendiente de verificar: latitud y velocidad sidérea)* | 5 |
| 8 | La Luna de esta noche | 2 Telescopio | Primera entrada de la bitácora | Telescopio con la Luna real: encuadrar, marcar el terminador, ubicar 3 mares y la luz cenicienta | 12,2 % iluminada, 403 151 km desde el Mirador a las 19:30 (JPL Horizons). La luz cenicienta es luz del Sol reflejada por la Tierra | 7 |
| 9 | Ecuador ya dejó un mensaje | 2 Faro (cuarto de la Dra. Vega) | Reordenar el carrusel de diapositivas | Ordenar 9 diapositivas por pistas visibles en cada foto; el proyector muestra la secuencia | 1873 Observatorio de Quito; 1957 estación Quito; 1969 disco del Apolo 11 con el mensaje de Velasco Ibarra (73 países); 1975 Apolo-Soyuz; 1981 STS-2; 1982 entrega a Ecuador; 2007 EXA; 2013 Pegaso; 21-06-2023 Ecuador firma los Acuerdos Artemisa, país n.º 26 [A1–A4, E1–E3, E6] | 4 |
| 10 | Se pone a las 21:07 | 2 → 1 | Ver la puesta y volver a casa | Cinemática corta; vuelta por el atajo del faro | La Luna se pone cuando su borde superior toca el horizonte, con 34′ de refracción: 21:07 | 2 |
| **Acto III** | **«El sueño lunar»** | | | | | **33** |
| 11 | Buenas noches, Órbita | 1 Habitación → 3 | Acostarse | Escribir la entrada del día y apagar la lámpara; transición al sueño | — (puente emocional) | 2 |
| 12 | Seis veces más ligera | 3 Campamento del sueño | Aprender a moverse | Pista de 3 tramos: saltar, frenar y cargar una caja | Gravedad lunar 1,624 m/s², un sexto de la terrestre. El peso cambia; la masa, no: la caja pesa poco pero cuesta frenarla [L6] | 5 |
| 13 | La herramienta correcta | 3 Campo de cráteres | Tomar 4 muestras distintas | Elegir pinzas, cucharón, rastrillo o tubo con martillo; una elección mala muestra por qué falla | Regolito: polvo y fragmentos de impactos acumulados durante miles de millones de años. Herramientas Apolo 15–17; el Apolo 11 solo llevó cucharón de caja, pinzas pequeñas y tubos de 2 cm [L1–L3, L8, 03b] | 6 |
| 14 | Una roca necesita una historia | 3 Campo de cráteres | Documentar 2 muestras | Gnomon, 3 fotos antes, recoger, bolsa numerada y 1 foto después; un número mal puesto obliga a revisar el registro sin perder la muestra | Protocolo de los Apolo 15–17: 1 foto con el Sol a la espalda, un par estéreo de lado y 1 foto después. El gnomon da escala, color, vertical y ángulo del Sol [L4 corregido en 03b] | 5 |
| 15 | Mirar sin borrar | 3 Sitio del Apolo 11 | Fotografiar el sitio sin entrar | Cámara con zoom desde fuera de un anillo de 75 m; 5 objetivos | Quedó la etapa de descenso, con su placa; el resto del módulo despegó. NASA recomienda 75 m de exclusión alrededor del Apolo 11 (225 m en el 17). Los objetos conservan dueño [L12, R2, R3] | 5 |
| 16 | Dos banderas, un cielo | 3 Loma de la Cooperación (ficticia) | Plantar juntas las banderas de Ecuador y EE. UU. | Armar 2 mástiles, hincarlos con ritmo y extender las barras horizontales; ceremonia | La bandera del Apolo colgaba de una barra horizontal porque no hay viento: 0,91 × 1,52 m y mástil de 2,44 m. Una bandera no da territorio (art. II). Ecuador firmó los Acuerdos Artemisa en 2023 [L10, R1, E1] | 6 |
| 17 | Volver como Columbia | 3 Cielo lunar → regreso | Mirar la Tierra y emprender el regreso | Vista «mirar arriba»; ordenar 7 etapas del regreso | La Tierra queda casi fija en el cielo y tiene fases opuestas a las de la Luna. Regreso: ascenso, encuentro en órbita lunar, separación, reentrada con escudo térmico, paracaídas y amerizaje en el Pacífico el 24-07-1969, recogido por el USS Hornet [L9, L12, L13] | 4 |
| **Epílogo** | **«Bitácora entregada»** · 06:00–07:30 | | | | | **5** |
| 18 | Amerizaje en la cama | 1 Habitación | Terminar la bitácora | Elegir 3 entradas y compararlas con los datos reales | Los 6 alunizajes trajeron 382 kg y 2 196 muestras: 21,5 kg en el Apolo 11 y 110,5 kg en el 17 [L5 corregido] | 3 |
| 19 | La entrega | 1b Plaza de las Iguanas | Entregar la bitácora a Ari y a la Dra. Vega | Diálogo final; se abre el mundo libre | — (cierre del tema) | 2 |
| | **Total de la ruta principal** | | | | | **85** |

### 2.2 Cómo se calculó cada duración

Supuestos del jugador medio, por validar en una prueba cronometrada con al menos 5 personas:

- **Caminar:** 4 m/s en Guayaquil; 2 m/s en la Luna, a saltos.
- **Diálogo:** 5 s por burbuja de 2 renglones (lectura de unas 200 palabras por minuto más la reacción).
- **Mecánica:** primer intento más un reintento medio.
- **Margen:** de 10 a 25 % para curiosear, según cuánto invite la escena.

| # | Recorrido (s) | Diálogo (s) | Mecánica (s) | Margen (s) | Total |
|---|---:|---:|---:|---:|---:|
| 1 | 20 | 12 × 5 = 60 | 8 objetos × 15 = 120 | 40 | 240 s = 4 min |
| 2 | 0 | 10 × 5 = 50 | 4 subsistemas × 45 + 1 fallo explicado 60 = 240 | 70 | 360 s = 6 min |
| 3 | 30 | 16 × 5 = 80 | 30 | 40 | 180 s = 3 min |
| 4 | 300 m → 75 | 10 × 5 = 50 | 3 piezas × 20 = 60 | 55 | 240 s = 4 min |
| 5 | 200 m → 50 | 16 × 5 = 80 | reparar 90 + a mano 60 + 3 ajustes × 50 = 300 | 50 | 480 s = 8 min |
| 6 | 500 m con escalones → 125 | 8 × 5 = 40 | encontrar la Luna 45 | 30 | 240 s = 4 min |
| 7 | 0 | 10 × 5 = 50 | motor 60 + eje 2 × 60 + prueba 30 = 210 | 40 | 300 s = 5 min |
| 8 | 0 | 14 fichas × 5 = 70 | encuadre 60 + terminador 60 + 3 mares × 30 + luz cenicienta 30 + anotar 30 = 270 | 80 | 420 s = 7 min |
| 9 | 0 | 10 × 5 = 50 | 9 diapositivas = 150 | 40 | 240 s = 4 min |
| 10 | 60 | 6 × 5 = 30 | puesta 30 | 0 | 120 s = 2 min |
| 11 | 10 | 8 × 5 = 40 | anotar 30 + transición 15 | 25 | 120 s = 2 min |
| 12 | 30 | 10 × 5 = 50 | 3 tramos × 50 = 150 | 70 | 300 s = 5 min |
| 13 | 200 m → 100 | 6 × 5 = 30 | 4 muestras × 45 = 180 | 50 | 360 s = 6 min |
| 14 | 20 | 6 × 5 = 30 | 2 muestras × 100 = 200 | 50 | 300 s = 5 min |
| 15 | 240 m → 120 | 6 × 5 = 30 | 5 fotos × 25 = 125 | 25 | 300 s = 5 min |
| 16 | 120 m → 60 | 8 × 5 = 40 | 2 mástiles × 60 + 2 hincados × 30 + barras 30 + ceremonia 40 = 250 | 10 | 360 s = 6 min |
| 17 | 0 | 6 × 5 = 30 | mirar la Tierra 40 + 7 etapas 100 + cinemática 30 = 170 | 40 | 240 s = 4 min |
| 18 | 0 | 10 × 5 = 50 | 3 entradas y comparación = 100 | 30 | 180 s = 3 min |
| 19 | 160 m → 40 | 12 × 5 = 60 | 0 | 20 | 120 s = 2 min |

**Resultado:** 85 min de ruta principal, con 184 burbujas de diálogo. Las 8 misiones secundarias de la sección 6 suman 41 min más: **126 min** para quien lo complete todo.

**Por qué no menos.** Si la prueba cronometrada diera un 30 % menos (59,5 min), bastaría con volver obligatoria una secundaria corta, como la S1 «Bitácora lunar».

---

## 3. El sueño lunar

### 3.1 Cómo se llega

- **Puerta:** la cama se desbloquea al terminar la escena 10, con la primera entrada de la bitácora escrita. Antes, acostarse da una frase de Órbita: «Todavía no, la Luna sigue arriba».
- **Ritual (escena 11):** la protagonista anota la hora de la puesta, Órbita se enrosca a sus pies y ella mira la maqueta de Pegaso que cuelga del techo. Al apagar la lámpara, las estrellas pegadas del techo se encienden. La cámara sube por la ventana, la ciudad se vuelve un mapa de cuaderno, la Tierra se curva y aparece la Luna. Es la viñeta 02 del guion anterior, al revés.
- **La transición esconde la carga** de la escena lunar: de 6 a 8 s, sin pantalla negra.

### 3.2 Reglas del sueño

- **Física honesta:** gravedad de un sexto, sin viento, sombras duras, cielo negro y silencio exterior. Lo que es sueño se dice: la protagonista no necesita nave ni oxígeno, y Órbita lleva un casco de pecera.
- **Sello «Sueño»** en las páginas del cuaderno que nacen aquí, distinto de «Dato medido».
- **Hora lunar:** mañana lunar con el Sol bajo, para que las sombras largas lean bien el relieve en low-poly. Ojo: la noche del 12-11-2026, con la Luna al 12 %, el Mar de la Tranquilidad aún está a oscuras según la geometría del terminador *(pendiente de verificar con el punto subsolar de Horizons)*. El sueño usa una fecha real en que amanezca en ese sitio, calculada con `herramientas/luna_efemerides.py`, para que la Tierra del cielo y la luz sean exactas. Órbita lo explica: «En los sueños el Sol sale cuando uno quiere. Hoy, de verdad, allá es de noche».
- **Arte:** la Luna del sueño es low-poly pintada, no fotográfica. Necesita una paleta gris cálida propia, que se aprueba en la Fase 1. El cian sigue reservado para la tecnología: el anillo de 75 m, el visor y las bolsas.

### 3.3 Qué se hace

**Mapa del sueño** (unos 600 × 400 m de juego):

| Lugar | Distancia | Uso |
|---|---|---|
| Campamento del sueño | Llegada | Pista de movimiento (escena 12) y punto de despertar |
| Campo de cráteres | 150 m del campamento | Muestras y documentación (escenas 13 y 14) |
| Anillo de 75 m del Apolo 11 | 300 m | Observación con zoom (escena 15). No se puede cruzar |
| Loma de la Cooperación (ficticia) | Fuera del anillo, a más de 100 m de él | Las dos banderas (escena 16) |
| Cresta de la Tierra | 80 m de la loma | Vista «mirar arriba» y regreso (escena 17) |

1. **Caminar con un sexto de g (escena 12).** Saltos largos, frenadas que patinan y una caja que se levanta con una mano pero cuesta detener. Órbita: «Tu masa viene contigo; lo que cambió es tu peso».
2. **Recolectar muestras (escenas 13 y 14).** Las herramientas son las de los Apolo 15 a 17, y el cuaderno lo aclara: pinzas para rocas, cucharón para suelo, rastrillo para separar fragmentos y tubo de núcleo con martillo para conservar las capas. El protocolo de fotos es el de esas misiones. Se llenan 8 bolsas numeradas, que vuelven al despertar como páginas de la bitácora, no como rocas: así nadie «se lleva» nada de la Luna.
3. **Ver el Apolo respetando su sitio (escena 15).**
   - El sitio del Apolo 11 se ve con un anillo cian de 75 m: la recomendación de NASA de 2011 para vehículos visitantes. El juego la adopta como norma propia y lo dice: «No es una ley para nosotras; es una buena costumbre» [R3, R5].
   - Se fotografían la etapa de descenso con su placa y las huellas históricas, más 3 objetos del sitio. El sismómetro y el retrorreflector del Apolo 11 quedan *pendientes de verificar* antes de modelarlos.
   - **La bandera del Apolo 11 no se muestra en pie.** Órbita explica que, según Aldrin, la derribó el despegue y que hoy no se sabe su estado [L11].
   - Sin insignias ni logotipos en el modelo. La placa se lee en el cuaderno como texto.
4. **Las dos banderas (escena 16).**
   - Se plantan en la Loma de la Cooperación, fuera del anillo. Cada una lleva un mástil telescópico y una barra horizontal, como las del Apolo: por eso «ondean» sin viento.
   - El hincado es un ritmo de martillo: el regolito se endurece a pocos centímetros *(pendiente de verificar la profundidad que lograron en el Apolo 11)*.
   - **Ceremonia breve:** las banderas a la misma altura, la protagonista da un paso atrás y Órbita se sienta. La protagonista recuerda que en 2011 Ronnie Nader dijo que EXA quería poner la bandera ecuatoriana en la Luna (*Sobrevuelo* 2011, p. 25). Se presenta como un sueño dicho en voz alta, no como un hecho.
   - Órbita: «No nos hacen dueños de nada. Dicen que vinimos juntos».
   - **Trato respetuoso:** las banderas no tocan el suelo, no se pueden tumbar, no hay chistes con ellas ni se usan como premio. Queda abierto si la de Ecuador lleva el escudo (proporción 3:2 según el instructivo de 2009) o es el tricolor sin escudo [03a, R8, R9].

### 3.4 Cómo se vuelve

- **Ruta principal (escena 17):** la protagonista sube a la cresta y la cámara pasa a la vista «mirar arriba», porque la cámara de exploración a unos 60° no muestra el cielo (D-013). La Tierra está quieta y en fase. Ordena las 7 etapas del regreso del Apolo 11 en el cuaderno y la acompaña una recreación estilizada del módulo de mando: reentrada, paracaídas y amerizaje.
- **Despertar:** el «amerizaje» es Órbita volcando el vaso de agua de la mesita. La protagonista despierta mojada y riéndose a las 06:00.
- **Salida libre:** desde el menú del cuaderno, «Despertar» funciona en cualquier momento. La partida guarda el avance del sueño.

### 3.5 La frase ambigua: «siendo vista con el Apolo que llegó a la Tierra»

| Opción | Lectura | Cómo se juega | Dato que la respalda |
|---|---|---|---|
| **A** | Ver el módulo lunar del Apolo que **quedó en la Luna** | Escena 15: se mira y se fotografía desde fuera del anillo | La etapa de descenso quedó en la Luna [L12] |
| **B** | Ser vista **junto al** Apolo: la foto de recuerdo | Escena 15: autorretrato con el teleobjetivo y la etapa de descenso al fondo, sin cruzar el anillo | Igual que A |
| **C** | El Apolo que **volvió a la Tierra**: el módulo de mando | Escena 17: la acompaña en su regreso hasta el amerizaje | El módulo de mando amerizó en el Pacífico el 24-07-1969 [L13]. El nombre «Columbia» está *pendiente de verificar* en fuente primaria |
| **D** | Que **la vean desde la Tierra** | Epílogo: Ari cuenta que anoche vio por el telescopio «un puntito» en la Luna. Es imposible: desde la Tierra no se distingue el sitio, y Órbita lo aclara con humor | Hay que verificar con cifras la resolución de un telescopio de aficionado |

**Esta propuesta usa A, B y C juntas**: se ve el sitio, se toma la foto y se vuelve «como Columbia». La D queda como guiño opcional.

> **Pregunta abierta para Guillermo:** ¿cuál de las cuatro lecturas querías decir? ¿O es otra?

---

## 4. Mundo abierto: cómo se conectan los escenarios

### 4.1 Mapa de conexiones

```
[1 Habitación] --escalera--> [1b Casa, planta baja] --puerta--> [1b Las Escalinatas]
                                                                     |
                                                            escalones numerados
                                                                     |
[3 Luna del sueño] <==cama== [1 Habitación]          [1b Plaza de las Iguanas] --sendero--> [1c Sendero del arroyo] --subida--> [2 Mirador del Faro]
                                                                                                                                      |
                                                                                                      atajo del faro (desde el Acto II) --> [1b Las Escalinatas]
```

### 4.2 Rutas, puertas y desbloqueos

| Ruta | Tipo | Abierta desde | Qué la abre | Umbral de carga |
|---|---|---|---|---|
| Habitación ↔ Casa | Escalera interior | Escena 1 | Leer la convocatoria | Corte en la escalera, menos de 1 s |
| Casa ↔ Las Escalinatas | Puerta de calle | Escena 3 | Recibir la caja de Rafael | Puerta: 1 a 2 s |
| Escalinatas ↔ Plaza ↔ Sendero | Exterior continuo | Escena 4 | Libre | Sin carga: una misma escena por tramos |
| Sendero ↔ Mirador | Subida con escalones | Escena 5 | La antena funciona y Sam da la llave del faro | Curva del camino: 1 a 2 s |
| Mirador → Escalinatas (atajo) | Escalera de servicio | Escena 10 | La Dra. Vega la abre | Igual que la puerta |
| Habitación ↔ Luna | Cama | Escena 10 | Primera entrada de la bitácora | Transición del sueño: 6 a 8 s |
| Viaje rápido | Mapa del cuaderno | Escena 19 | Final de la ruta principal | Pantalla de carga con datos de la bitácora |

### 4.3 Libertad y límites

- **Mundo abierto suave.** Desde la escena 4 se puede ir y volver entre la casa, la plaza, el sendero y el Mirador. La historia avanza con el reloj del cielo: la Luna baja mientras se juega, y si el jugador se entretiene, se pone. No hay derrota: Órbita propone mirarla «mañana» y la escena 8 usa la noche siguiente desde la tabla de NASA.
- **Reloj.** La tarde y la noche de la historia son el 12-11-2026: la Luna de esa noche ya está medida y coincide con Horizons. La «Luna de hoy», con la fecha real del jugador, se abre al terminar el juego, porque la orientación para cualquier instante sigue pendiente.
- **Después del final:**
  - mundo libre de día y de noche;
  - la cama permite «soñar otra vez», con la Luna libre y sus secundarias;
  - cada noche dormida avanza el calendario a la siguiente fecha de la S1 «Bitácora lunar»;
  - la antena del sendero sigue rastreando pases simulados.
- **Persistencia.** Los objetos recogidos, las bolsas, las fotos y las diapositivas quedan en el cuaderno. Las banderas del sueño siguen plantadas al volver a soñar.

---

## 5. Órbita y el reparto

| ID | Personaje | Papel en esta historia | Escenas |
|---|---|---|---|
| PER-01 / PER-02 | Protagonista A / B | La misma estudiante de ingeniería de control con dos cuerpos base. Su meta: una práctica espacial. Habla de NASA solo como sueño personal; la convocatoria es de un centro ficticio [R7]. Nombre por decidir | Todas |
| PER-09 | Órbita | Guía científico y voz de los datos: cita fuente y hora. Humor costeño. Olfatea los objetos interactivos y los señala con la placa cian del collar. En el mundo real solo la protagonista le entiende: los demás oyen «miau», y es un chiste recurrente. En el sueño lleva casco de pecera y explica la física. Su rig y su animación de caminar ya existen | Todas |
| PER-03 | Elena | La mamá. Entrega la libreta: «Si algo te sorprende, apúntalo». En la cena pregunta por la Luna y le da el pie a Ari | 3, 10, 18 |
| PER-04 | Rafael | El papá. Trae la caja con el motor. Humor de taller: «Esto no se arma con fe, se arma con tornillos» | 3, 18 |
| PER-05 | Lidia | Vendedora de jugos en la plaza. Da el folleto del Planetario y su dicho propio: «Luna acostada, algo trae». Lleva a la secundaria S7 | 4, 19, S7 |
| PER-06 | Sam | Compañero de clase. Tiene la carpeta de la convocatoria y ayuda con la antena. Es el que se equivoca en voz alta: sube la ganancia hasta que la antena oscila | 5, 19 |
| PER-07 | Dra. Vega | Ingeniera que cuida el Mirador y su club de observación. Su papá trabajó en la estación del Cotopaxi (**ficción**: un homenaje a los 220 ecuatorianos que llegaron a trabajar allí [03a]). Guarda el carrusel de diapositivas. Su regla: «Cambia un parámetro a la vez» | 7, 9, 10, 19 |
| PER-08 | Ari | Estudiante menor del club de observación. Hace las preguntas que haría un niño («¿Cómo se ve la Tierra desde allá?») y recibe la bitácora al final | 8, 10, 19 |

**El hilo de cada uno.** Elena y Rafael son el hogar que empuja; Lidia, el saber del barrio; Sam, el error que enseña; la Dra. Vega, el método y la memoria del Cotopaxi; Ari, el relevo. Órbita une la ciencia con el humor.

---

## 6. Misiones y recompensas

### 6.1 Principales

| ID | Misión | Escenas | Recompensa |
|---|---|---|---|
| M1 | La convocatoria | 1 | Cuaderno de campo: inventario y bitácora |
| M2 | Un satélite cabe aquí | 2 | Multímetro (herramienta de circuitos) y página de Pegaso |
| M3 | La caja de Rafael | 3 | Motor de seguimiento y libreta |
| M4 | Por Las Escalinatas | 4 | Mapa del cuaderno y folleto del Planetario |
| M5 | Rastrear como en el Cotopaxi | 5 | Antena operativa, llave del faro y parche original «Estación» |
| M6 | La Luna sonriente | 6 | Página «Altura y acimut» |
| M7 | Un polo en el horizonte | 7 | Telescopio con seguimiento |
| M8 | La Luna de esta noche | 8 | Primera entrada de la bitácora («Dato medido») |
| M9 | Ecuador ya dejó un mensaje | 9 | Línea de tiempo y paráfrasis del mensaje ecuatoriano del disco [A4] |
| M10 | Se pone a las 21:07 | 10 | Atajo del faro y la cama del sueño |
| M11 | Seis veces más ligera | 11, 12 | Traje del sueño (diseño original, sin insignias) |
| M12 | Muestras con historia | 13, 14 | Kit de herramientas y 8 bolsas numeradas |
| M13 | Mirar sin borrar | 15 | Teleobjetivo y foto del sitio |
| M14 | Dos banderas, un cielo | 16 | Página «Juntos» y la loma como punto de viaje del sueño |
| M15 | Volver como Columbia | 17, 18 | Bitácora completa |
| M16 | La entrega | 19 | Final; se abren la «Luna de hoy», «Soñar otra vez» y el viaje rápido |

### 6.2 Secundarias (41 min)

| ID | Misión | Dónde | Mecánica | Dato | Recompensa | Min |
|---|---|---|---|---|---|---:|
| S1 | Bitácora lunar | Mirador; avanza al dormir | Observar 3 fases en 3 noches de la tabla de NASA: el 12-11 (12 %), una noche cercana al cuarto creciente y el 21-11 (91,2 %) | Las fases salen de la geometría Sol-Tierra-Luna; el ciclo dura unos 29,5 días *(pendiente de verificar)* | Carta estelar COL-12 y zoom del telescopio | 8 |
| S2 | El Chimborazo gana desde el centro | Habitación | Globo con alturas: comparar el nivel del mar con la distancia al centro de la Tierra | La cumbre del Chimborazo está a unos 6 384,4 km del centro, 2,1 km más que la del Everest (IGM-ESPE, 2019) [E7 corregido] | Página y póster del cuarto | 4 |
| S3 | Las llamas del Cotopaxi | Todo el barrio | Encontrar 5 fotos perdidas de la estación | 578 160 horas de apoyo en 22 años; el personal ecuatoriano pasó de 50 a 220; una foto de 1973 muestra llamas junto a la antena [03a] | Accesorio para Órbita (pañuelo de llama) | 6 |
| S4 | Fauna del cerro | Sendero y plaza | Fotografiar 6 animales (FAU) con el mismo protocolo de la Luna: foto antes de acercarse | Documentar sin perturbar vale en la Tierra y en la Luna | Página de fauna | 6 |
| S5 | Luna acostada | Plaza (Lidia) | Comparar el dicho de Lidia con 2 observaciones | La inclinación de la creciente depende de la latitud, no del clima | Jugo y una frase nueva de Lidia | 3 |
| S6 | La Tierra tiene fases | Luna, en 3 sueños | Fotografiar la Tierra desde la cresta | Las fases de la Tierra son opuestas a las de la Luna [L9] | Postal «Tierra creciente» | 5 |
| S7 | Muestras de sobra | Luna | Completar 12 bolsas con 4 tipos de material | Comparar con las 58 muestras del Apolo 11 y las 741 del Apolo 17 [L5, 03b] | Rastrillo dorado (cosmético) | 6 |
| S8 | Pegaso en órbita | Habitación, tras el final | Mantener el enlace con la maqueta en una simulación | Pegaso tuvo una anomalía tras un acercamiento orbital el 23-05-2013; NASA no confirmó un choque, y el contacto volvió el 25-01-2014 [E5, 03a] | Parche original «Pegaso» | 3 |

**Recompensas sin insignias:** parches, postales y accesorios son diseños propios. Ninguno imita el emblema de una misión real.

---

## 7. Qué se reutiliza y qué es nuevo

### 7.1 Se reutiliza

| Recurso | Uso en la historia | Fuente |
|---|---|---|
| Escena de exploración v1 (terreno, arroyo, puente, flamboyán, hierba) | Escenario 1c, escena 5 y S4 | [[Escena de exploracion v1]] |
| Antena COL-01 (las versiones de Tripo y por script) | Antena caída de la escena 5 | Lote 04a |
| Protagonista (Tripo, niveles de 1 500 y 3 000 triángulos) | Todas | `limpiar_personaje.py` |
| Órbita con rig, reposo y caminar | Todas | `rig_gato.py` |
| Iguana (Tripo) | Plaza y S4 | Lote 04a |
| Prueba del telescopio con la Luna real (0,74 ms de GPU) | Escenas 8 y 10 y S1 | `pruebas/luna_telescopio/` |
| `luna_efemerides.py`, `luna_parametros.py` y `mooninfo_2026.json` | Fechas de la historia, de S1 y del sueño | [[Mirador del Faro - Luna con datos reales]] |
| Hojas de referencia v1 | TAL-01 a 14 (cuarto), MIR-01 a 08 (Mirador), COL-01 a 12, ARQ, URB, VEG, FAU y PER | [[Catalogo de recursos]] |
| Mapa de la región del lote 02 | Mapa del cuaderno y viaje rápido | `ANC_MAPA` |
| Reparto, viñetas y frases del guion anterior | Elena, Rafael, Lidia, Sam, Vega y Ari; viñeta 02 al revés | Bóveda anterior |

### 7.2 Es nuevo

| Pieza | Cómo se haría | Créditos |
|---|---|---|
| Habitación-taller y casa en diorama | Script y props de las hojas TAL | 0 por script |
| Las Escalinatas y la plaza (un tramo) | Script, como la escena v1 | 0 |
| Mirador del Faro en 3D | Script y hoja MIR | 0 |
| Luna del sueño: terreno, cráteres y rocas | Script | 0 |
| Etapa de descenso del Apolo 11, herramientas, gnomon y bolsas | Script con planos públicos, revisados contra fuentes | 0 |
| Dos banderas con barra horizontal | Malla fija con arrugas modeladas, sin tela simulada | 0 |
| Traje del sueño para PER-01 y casco de Órbita | Hoja nueva y malla | Partida por aprobar (unos 9 por malla en Tripo) |
| PER-03 a PER-08 en 3D | Tripo multivista desde hojas nuevas | Partida por aprobar (6 × 9 = 54) |
| Tierra en el cielo lunar | Esfera con textura de NASA y crédito | 0 *(licencia pendiente de verificar)* |
| Interfaz: cuaderno, bitácora, carrusel, cámara de fotos y vista «mirar arriba» | Godot | 0 |
| 184 burbujas de diálogo en la ruta principal, más fichas y secundarias | Guion en la Fase 2 | 0 |

**Seis sistemas para 19 escenas.** Para contener el alcance, las mecánicas se repiten:

1. circuito y multímetro: escenas 2 y 7, y S8;
2. orientación por altura y acimut: escenas 5 y 6;
3. telescopio: escena 8, S1 y S5;
4. ordenar tarjetas: escenas 9 y 17;
5. cámara de fotos con protocolo: escenas 14 y 15, S4 y S6;
6. herramientas y bolsas: escena 13 y S7.

---

## 8. Riesgos de alcance en el portátil mínimo (Intel HD 620)

| Riesgo | Por qué | Cómo reducirlo |
|---|---|---|
| Exteriores pesados | La escena v1 ya da 57,6 fps a 720p con 244 599 primitivas y 252 llamadas de dibujo | Mechones y flores en `MultiMeshInstance3D`, niveles de detalle de 1 500 triángulos y hierba reducida en el perfil mínimo. Meta: 60 fps a 720p con Mobile |
| Mundo abierto continuo | Tres zonas a la vez no caben en 8 GB con la HD 620 | Zonas en escenas separadas, unidas por umbrales: escalera, puerta, curva del camino y cama. Carga de 1 a 2 s, disimulada |
| Compilación de shaders | El primer arranque de Forward+ tardó más de 90 s | Renderizador Mobile y precompilación de los shaders en la pantalla de carga inicial |
| Sombras largas en la Luna | El Sol bajo alarga las sombras y cuesta un mapa de sombras grande | 1 luz direccional con 2 cascadas y oclusión horneada en los cráteres. A cambio, la Luna no tiene hierba ni follaje y es la escena más barata |
| Banderas | La tela simulada es cara y además sería falsa: no hay viento | Malla fija con pliegues modelados: más barata y fiel a la historia |
| Telescopio | Medido: 0,74 ms de GPU, y de 2,2 a 2,5 ms con la Luna a pantalla completa | Sin riesgo; se mantiene |
| Orientación de la Luna para cualquier instante | Sigue pendiente; cerca del cenit gira hasta 12° por minuto | La historia usa horas fijas ya medidas (19:30 y 21:00 del 12-11-2026). La «Luna de hoy» queda para después del final |
| Volumen de diálogo | 184 burbujas en la ruta principal, más su traducción | Burbujas de 2 renglones y un archivo de texto aparte para traducir |
| Personajes nuevos | 6 personajes más un traje: unos 63 créditos y su limpieza en Blender | Personajes secundarios estáticos o con 3 animaciones (reposo, hablar, señalar). La partida se pide aparte |
| Escenas que crecen | 19 escenas y 8 secundarias | Seis mecánicas reutilizables. Corte de seguridad: S6 a S8 pasan a una ampliación sin tocar la ruta de 85 min |
| Precisión científica | Una cifra mal puesta cae sobre un juego educativo | Cada dato con código de fuente. Los *pendientes de verificar* se verifican antes de escribir el diálogo final |
| Marca NASA y símbolos | El título interno lleva «NASA»; hay banderas y un sitio histórico | Título comercial sin «NASA» [R7]; centro espacial ficticio; sin insignias; trato de las banderas revisado por un abogado [03a] |

---

## 9. Datos pendientes de verificar

| Dato | Escena | Qué hacer |
|---|---|---|
| Latitud de Guayaquil (≈ 2,2° S) y altura del polo celeste | 7 | Fuente oficial (IGM) |
| Velocidad del seguimiento sidéreo (unos 15° por hora) | 7 | Fuente astronómica primaria |
| Duración del ciclo de fases (unos 29,5 días) | S1 | NASA, *Moon facts* |
| Estado de iluminación del Mar de la Tranquilidad el 12-11-2026 y fecha de amanecer para el sueño | 3.2 | Punto subsolar con `luna_efemerides.py` |
| Sismómetro y retrorreflector del Apolo 11 | 15 | Informe de la misión del Apolo 11 |
| Nombre «Columbia» del módulo de mando | 17 | Resumen de la misión en NASA |
| Profundidad a la que entró el mástil en el Apolo 11 | 16 | ALSJ o informe de misión |
| Licencia y crédito de la textura de la Tierra | 17 y S6 | Guía de imágenes de NASA |
| Escalones numerados de las escalinatas reales del cerro Santa Ana (cifra) | 4 | Fuente municipal, solo si se quiere citar |
| Resolución de un telescopio de aficionado sobre la Luna | 3.5 (opción D) | Cálculo con fuente |

**No se usan, por falta de fuente:** que Quito rastreara el Apolo 11 [A3], el paradero de las rocas lunares regaladas a Ecuador [A5, A6] y el cohete de Pegaso.

---

## 10. Preguntas para Guillermo

1. ¿Qué querías decir con «siendo vista con el Apolo que llegó a la Tierra»? Opciones A a D en la sección 3.5.
2. ¿La bandera de Ecuador va con escudo o es el tricolor sin escudo?
3. ¿La noche de la historia es fija (12-11-2026, ya medida) o quieres la fecha real del jugador desde el principio?
4. ¿El sueño ocurre en el sitio del Apolo 11, el más conocido, o en el del Apolo 17, donde las herramientas del juego sí coinciden con las históricas?
5. ¿Nombre de la protagonista y del centro espacial ficticio?
6. ¿Te sirven 85 min de ruta principal o prefieres acercarte a 60 y ganar tiempo de producción?
