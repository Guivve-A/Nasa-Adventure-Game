---
tipo: fase
fase: 2
titulo: Estructura narrativa y diseño de misiones
estado: borrador para aprobación de Guillermo
fecha: 2026-11-12
base: "[[Propuesta_A]]"
injertos: "[[Propuesta_B]], [[Propuesta_C]]"
verificaciones: "[[03a_verificacion_ecuador]], [[03b_verificacion_apolo]]"
auditoria: "[[Plan de auditoria]]"
---

# Fase 2 — Estructura narrativa y misiones

> **Estado: borrador para aprobación de Guillermo.** Nada de aquí se escribe en diálogo final ni se construye hasta que Guillermo apruebe o corrija las decisiones F2-01 a F2-16.
> **Pedido de Guillermo (2026-11-12):** validar la historia; al menos 1 h; más contenido espacial; que la protagonista, al acostarse, sueñe que camina por la Luna, recoge muestras y es «vista con el Apolo que llegó a la Tierra»; una misión para colocar juntas las banderas de Estados Unidos y Ecuador; una historia coherente y entretenida; y la auditoría de carga, menús, botones, jugabilidad, escenarios, caminos y texturas en orden (1 Habitación, 2 Telescopio, 3 Luna), unidos como mundo abierto.
> **Qué es este documento:** la síntesis del director creativo. Parte de [[Propuesta_A]] («Luz cenicienta», la mejor puntuada) e injerta las mejores ideas de [[Propuesta_B]] y [[Propuesta_C]]. Solo usa datos confirmados en [[03a_verificacion_ecuador]] y [[03b_verificacion_apolo]] o medidos por nosotros; el resto va marcado. La auditoría de construcción vive aparte, en [[Plan de auditoria]]; la sección 9 dice qué le pide esta historia.

**Marcas:** **(pv)** pendiente de verificar · **(cálculo propio)** deducción nuestra con datos de NASA o JPL, a revisar · **(corr.)** dato corregido en 03a o 03b · **(ficción)** inventado y declarado como tal.

## En cifras

| Medida | Valor |
|---|---|
| Escenas de la ruta principal | 20: un prólogo y 19 escenas en 4 actos |
| Ruta principal, jugador medio | **94 min** (estimación de diseño; falta la prueba cronometrada) |
| Jugador rápido (×0,7) | unos **66 min**: el mínimo de 1 h se cumple incluso así |
| Contenido espacial en la ruta principal | 78 de 94 min (**83 %**; en A era el 78 %) |
| El sueño lunar | 32 min, el acto más largo |
| Misiones secundarias | 10, unos 51 min en dos lotes: **145 min** para quien lo haga todo |
| Tiempo de la historia | 12 y 13 de noviembre de 2026: 2 días, 2 noches y 1 sueño |
| Escenarios | 1 Habitación → 1b Casa → E Barrio → S Sendero → 2 Mirador y telescopio → 3 Luna del sueño |
| Créditos de Higgsfield gastados en esta fase | **0** |

---

## 0. Qué se decide en esta puerta

| ID | Decisión propuesta | De dónde sale | Sección |
|---|---|---|---|
| **F2-01** | **Base narrativa: A «Luz cenicienta»**, con injertos de B y C. Arco con causa y efecto: el seguidor oscila → apagón y toma temblorosa → duda → sueño → arreglo con prealimentación y realimentación → la Luna compartida. | Puntajes de los jueces: A 8,15 · B 7,95 · C 7,55 | 1, 2 |
| **F2-02** | **Calendario fijo:** día 1 y noche 1 el 12-11-2026, sueño, día 2 y noche 2 el 13-11-2026, con la Luna real de esas noches (Horizons). La Luna de la fecha real del jugador se abre después del final. | A y B; datos del [[Mirador del Faro - Luna con datos reales]] y consulta de hoy | 2, 4 |
| **F2-03** | **Duración:** ruta principal de 94 min de diseño. Prueba cronometrada con 3 a 5 personas; si la mediana baja de 70 min, se alarga el sueño (secundarias S8 y S10 a la ruta), no el diálogo. | Método de A; margen de B | 3.2 |
| **F2-04** | **El sueño ocurre en el sitio del Apolo 11** (Mar de la Tranquilidad) con su equipo real: cucharón de caja, pinzas pequeñas y tubos de 2 cm. El rastrillo, los tubos de 4 cm y el protocolo de 3 fotos antes y 1 después van en la secundaria S8, declarados como «de otro tiempo» (Apolo 15 a 17). | 03b, L1–L4; jueces | 4 |
| **F2-05** | **Luz del sueño:** se llega de noche, bajo la Tierra casi llena (la misma luz cenicienta vista por el telescopio), y amanece con licencia de sueño en la ceremonia de las banderas. Órbita aclara que de verdad faltarían unos 2 días. | A; opción B de C; cálculo propio con `mooninfo_2026.json` | 4.2 |
| **F2-06** | **Respeto del sitio histórico:** anillo cian de 75 m que no castiga; aterrizaje a más de 2 km (mapa a escala 1:4, declarado); la bandera del Apolo 11 no se muestra en pie; sin astronautas reconocibles; de la Luna no se lleva nada: las bolsas vuelven como páginas. | R2–R4, L11; A, B y C | 4.3 |
| **F2-07** | **Dos banderas nuevas,** Estados Unidos y Ecuador, del mismo tamaño y a la misma altura, con barra horizontal y **malla fija** (no hay viento). No se pueden soltar, tirar, dañar ni usar como premio o chiste. La de Ecuador, con escudo (a confirmar con Guillermo y con un abogado). | L10, R1, R8; B | 4.3 |
| **F2-08** | **Lectura recomendada de la frase ambigua:** A + B + C de la tabla 4.5 (la foto junto a la etapa de descenso, el regreso como el módulo de mando con un lazo de control y el montaje de Elena mirando la Luna). **Queda abierta para Guillermo.** | A y C | 4.5 |
| **F2-09** | **Mundo abierto por nodos** con reloj por hitos (la Luna no se puede perder), 3 estados de luz horneados (mañana, tarde y noche) y cargas solo en 3 umbrales más el ocular. | C (reloj y mundo vivo); A (umbrales) | 5 |
| **F2-10** | **Sellos del cuaderno:** «Dato medido», «Simulación» y «Sueño». La Luna del telescopio es fotográfica (datos de NASA); la del sueño, low-poly pintada. | B y C; [[Biblia de arte]] §3 | 2.4 |
| **F2-11** | **Arco de ingeniería de control** en 3 pasos: ganancia (seguidor y antena) → límites (apagón, seguimiento a mano) → prealimentación más realimentación. Se aprende con mecánica y pistas en 3 niveles, nunca con examen. | A (seguidor) y B (antena) | 3, 6 |
| **F2-12** | **Reparto con arco propio** (A) y un abuelo que trabajó en la estación del Cotopaxi como **ficción declarada** (C). Órbita habla por el cuaderno estando despierta la protagonista y en voz alta, por la radio del casco, en el sueño. | A y C | 6 |
| **F2-13** | **Secundarias en 2 lotes:** lote 1 (23 min) con la ruta principal; lote 2 (28 min) después. Mundo vivo acotado: 4 vecinos con rutina, 6 especies por hito y 6 cambios que persisten. | Contención de B; ideas de C | 7 |
| **F2-14** | **Corte vertical primero:** unos 50 min, de la Habitación al telescopio y al sueño hasta las banderas. | A; [[Plan de auditoria]] B8 | 10 |
| **F2-15** | **Política de datos:** solo cifras confirmadas en 03a o 03b, o medidas con Horizons y la tabla de NASA. Lo pendiente no entra al diálogo final. Lista de datos que no se usan. | B; jueces | 8 |
| **F2-16** | **Nombres:** «Proyecto NASA-Ecuador» es solo interno; ningún título comercial lleva «NASA» (R7). La convocatoria «Ventana Lunar» y su centro espacial son ficticios y provisionales; sin logotipos ni nada que sugiera respaldo (R6). | 03b, R6–R7 | 6, 11 |

---

## 1. Cómo se eligió la base

**Puntajes de los dos jueces** (coherencia, entretenimiento, valor educativo, fidelidad al pedido y viabilidad):

| Propuesta | Juez 1 | Juez 2 | Media | Fuerte | Débil |
|---|---:|---:|---:|---|---|
| [[Propuesta_A]] «Luz cenicienta» (aventura emotiva) | 8,1 | 8,2 | **8,15** | El mejor arco: fracaso, duda, sueño como giro y cierre colectivo | Chimborazo sin corregir; E8 sin marcar; 2 días exigen más luz horneada |
| [[Propuesta_B]] «La bitácora de una noche» (misión científica) | 7,8 | 8,1 | 7,95 | La más rigurosa y la más barata: 6 sistemas para 19 escenas | Conflicto de plazo, sin punto bajo; herramientas de 15–17 en el sitio del 11 |
| [[Propuesta_C]] «Barrio con vista a la Luna» (mundo abierto vivo) | 7,7 | 7,4 | 7,55 | El mejor mundo abierto; cápsula de cartón; reentrada como lazo de control | Sin conflicto; alcance alto (11 secundarias, 47 coleccionables) |

**Qué se toma de cada una**

| De | Se toma | Dónde queda |
|---|---|---|
| A | Columna vertebral, arcos del reparto, desglose de minutos, ficha «Luz cenicienta» como carga del sueño, montaje de Elena, final colectivo «La Luna de todos», corte vertical | Todo el documento |
| B | Antena del Cotopaxi con control proporcional, carrusel de 9 diapositivas verificadas, cita de Nader de 2011, sellos del cuaderno, banderas de malla fija, 6 sistemas reutilizables, lista de datos excluidos | 2.1, 2.4, 3.5, F2-10, 7, 8 |
| C | Caja de cartón de Rafael como cápsula, aterrizaje a más de 2 km, reentrada con el escudo térmico, reloj por hitos, barrio que recuerda, regla «mirar sin espantar», chapa cian de Órbita, atajo de los faroles, abuelo de la estación (ficción) | 3.1, 3.6, 5, 6, 7 |

**Qué se corrige respecto de A:** el Chimborazo pasa a «unos 6 384,4 km» (IGM-ESPE, 2019); el folleto del Planetario (E8) sale de la ruta principal porque no está verificado; el protocolo de 3 fotos sale del sitio del Apolo 11; la Luna de la noche 2 ya está calculada; el amanecer en Tranquilidad llega a unas 50 h, no a 42 h.

---

## 2. Premisa, tono y arco

### 2.1 Premisa en tres líneas

1. Una estudiante de ingeniería de control de Las Escalinatas, en Guayaquil, tiene dos noches para grabar 60 s de la Luna con el seguidor motorizado que construyó y postular a «Ventana Lunar», una convocatoria ficticia que la acerca a su sueño de trabajar algún día en la NASA.
2. La primera noche, un controlador que oscila y un corte de luz le arruinan la toma, y se pregunta si la Luna es para gente de su barrio.
3. Esa noche sueña que camina por la Luna, junto al sitio del Apolo 11, y vuelve con lo que le faltaba: una referencia fija, un registro honesto y gente con quien compartir el cielo.

### 2.2 Tema: «Lo lejos depende de dónde mides»

| Prueba del tema | Dato | Estado |
|---|---|---|
| Desde el centro de la Tierra, la cumbre más alejada es la del Chimborazo: unos 6 384,4 km, unos 2,1 km más que la del Everest | E7, IGM-ESPE 2019 | **corr.** (no usar 6 384 415,98 m) |
| Desde el Mirador, la Luna se aleja casi 4 000 km entre las 18:00 y las 21:00 del 12-11 por el giro de la Tierra | Horizons, medido | Confirmado |
| Ecuador ya llegó a la Luna: el mensaje de Velasco Ibarra viajó en el disco de buena voluntad del Apolo 11, con los de 73 países | A4 | Confirmado (que el disco siga allí es **pv**, §8.3) |
| La creciente de Guayaquil se ve «acostada»: el borde iluminado apunta hacia abajo (192,6° desde el cenit a las 19:30) | Horizons, medido | Confirmado |

### 2.3 Tono

- **Guayaquil:** cálido y costumbrista; humor de barrio, comida de casa, vecinos que opinan de todo.
- **Taller y telescopio:** preciso; cada cifra lleva unidad y fuente en el cuaderno.
- **Luna:** asombro sereno; silencio exterior, solo traje, respiración y la voz de Órbita por la radio.
- **Siempre:** se aprende probando, fallando y anotando qué cambió. Nunca un examen.

### 2.4 Reglas de coherencia

| Regla | Cómo se aplica |
|---|---|
| Un solo calendario | 12-11-2026 (día 1 y noche 1), sueño, 13-11-2026 (día 2 y noche 2). La fecha real del jugador solo se usa en el telescopio libre del final. |
| El sueño es ficción con datos reales | Los sucesos son inventados; las cifras no. Órbita lo dice al llegar: «Esto es un sueño. La Luna, no». |
| Sellos del cuaderno | «Dato medido» (con fuente y hora), «Simulación» (mecánica) y «Sueño». |
| Dos lunas, dos estilos | Telescopio: fotográfica, texturas de LRO (excepción de la biblia). Sueño: low-poly pintada. Se distingue el dato de la ficción a simple vista. |
| La NASA como meta, no como marca | Se nombra como aspiración, de forma factual. Convocatoria y centro espacial ficticios. Sin logotipos, insignias ni emblemas de misiones (R6, R7). |
| Banderas con respeto | Ver F2-07. |
| Sin astronautas reconocibles | El sitio del Apolo 11 se ve vacío, como hoy. Nadie con rostro o nombre de un astronauta. |

### 2.5 Arco de la protagonista

| Acto | Deseo | Lo que pasa | Cómo queda ella |
|---|---|---|---|
| I · La convocatoria | Postular | El seguidor oscila; Sam piensa dejar la carrera; Elena teme que se vaya lejos | Ilusionada, pero sola con el problema |
| II · La Luna que se escapa | Grabar esa noche | Antena y montura listas, pero se va la luz: toma temblorosa; la Luna se pone a las 21:07 | **Duda:** «A lo mejor la Luna no es para gente de Las Escalinatas» |
| III · Tranquilidad | — (está soñando) | Camina, registra, ve que Ecuador ya llegó en un disco, planta dos banderas juntas y vuelve como un módulo de mando | **Giro:** la distancia era una idea, no un muro |
| IV · Una referencia fija | Volver a intentarlo, ya no sola | Arregla el control; la familia y el barrio suben al Mirador | Lista para la siguiente ronda (capítulo 2) |

**Líneas de muestra** (borrador; cada una cabe en dos renglones):

| Momento | Quién | Texto |
|---|---|---|
| 1.2, tercer fallo | Dra. Vega (video) | «Cambia un parámetro. Si cambias tres, no sabrás cuál arregló el problema.» |
| 1.3 | Elena | «La NASA queda lejísimos, mija. Pero llévate la libreta.» |
| 2.3, apagón | Órbita | «Se fue la luz… y mira: ahora se ve la parte oscura.» |
| 2.4, duda | Protagonista | «A lo mejor la Luna no es para gente de Las Escalinatas.» |
| 2.4 | Ari | «Ecuador mandó un mensaje en 1969. Llegó antes que tú.» |
| 3.1 | Órbita | «Tu masa sigue contigo. Lo que cambió es tu peso.» |
| 3.5 | Órbita | «Representan nuestros sueños. No nos hacen dueños.» |
| 4.2 | Elena | «Ahora entiendo por qué la miras tanto.» |

---

## 3. Tabla de escenas

**Escenarios:** **1** Habitación-taller · **1b** Casa (planta baja y cocina) · **E** Barrio: Las Escalinatas, Plaza de las Iguanas y Mercado · **S** Sendero del arroyo ([[Escena de exploracion v1]]) · **2** Mirador del Faro y telescopio · **3** Luna del sueño.

**Columna «Verificación»:** 03a = [[03a_verificacion_ecuador]]; 03b = [[03b_verificacion_apolo]]; Hz = JPL Horizons medido; SVS = tabla `mooninfo_2026.json` de NASA SVS 5587.

### 3.1 Escenas

| # | Escena | Esc. | Objetivo | Mecánica | Dato real | Verificación | Min |
|---|---|---|---|---|---|---|---:|
| **P.0** | Título | 1 | Empezar | Menú; la cámara baja de la Luna a la ventana del cuarto; creador solo si Guillermo lo pide | — | — | 2 |
| | **Acto I · «La convocatoria»** (día 1, mañana) | | | | | | **22** |
| 1.1 | Despertar con Órbita | 1 | Conocer el taller y leer la convocatoria: grabar 60 s de la Luna con un instrumento propio antes de la medianoche del día 2 | Caminar, mirar, 5 objetos; el cuaderno se abre por primera vez | Póster del Observatorio Astronómico de Quito, fundado en 1873 | E6, 03a: confirmado | 4 |
| 1.2 | El seguidor que tiembla | 1 | Que el motor siga un punto de luz que cruza la pared | Rompecabezas de control en el osciloscopio (TAL-02): ganancia y amortiguación, un parámetro por prueba, con la gráfica anterior al lado | El cielo gira unos 15° por hora (360° en 24 h) | cálculo propio | 6 |
| 1.3 | Desayuno | 1b | Hablar con Elena y Rafael; recibir la libreta | Diálogo con 2 elecciones; globo de la cocina; la foto del abuelo con llamas junto a una antena | Chimborazo a unos 6 384,4 km del centro, 2,1 km más que el Everest. La estación del Cotopaxi tenía llamas junto a su antena de 12 m (foto de 1973). El abuelo es **ficción** | E7 **corr.** y A1, 03a | 3 |
| 1.4 | Bajar Las Escalinatas | E | Llegar al Mercado | Exploración libre; recolectar piezas (COL-03, COL-05); saludar a Lidia; ver la primera placa pintada (abre S5) | — (mundo y ritmo) | — | 4 |
| 1.5 | El puesto de Sam | E | Conseguir un codificador para el motor | Armar la maqueta de un satélite de 10 cm: energía, radio, antena y computadora. Sam cuenta que piensa dejar la carrera | Pegaso: primer satélite ecuatoriano, cubo de 10 cm con dos paneles de 27 cm, de la EXA (ONG civil de 2007), lanzado el 25-04-2013 (hora de Ecuador, según el equipo); el proyecto se inició en 2010 | E2–E4, 03a (E4 **corr.**) | 5 |
| | **Acto II · «La Luna que se escapa»** (día 1, tarde y noche 1) | | | | | | **25** |
| 2.1 | Rastrear como en el Cotopaxi | S | Subir al Mirador; levantar la antena caída (COL-01) | Reapuntar la antena con un control proporcional: con poca ganancia se atrasa, con mucha oscila | La estación Quito, al pie del Cotopaxi a 3 650 m, rastreó naves de 1957 a 1981, con antenas de 12 m desde 1960–1963, y apoyó al Apolo-Soyuz en 1975 | A1 **corr.** y A2, 03a | 5 |
| 2.2 | La Luna sonriente | 2 | Montar el seguidor y encontrar la Luna | Alinear la montura ecuatorial con el eje polar casi acostado; buscar, enfocar y marcar terminador, luz cenicienta y Mare Crisium. Órbita señala el Mar de la Tranquilidad en la parte oscura | A las 19:30: 12,2 % iluminada, a 403 151 km, a 20,0° de altura, borde iluminado a 192,6° del cenit. El polo sur celeste está a unos 2,2° sobre el horizonte (latitud del Mirador, 2,18° S). Tranquilidad está de noche: el Sol, 25° bajo su horizonte | Hz (prueba medida: 12,15 % y 192,6°); polo y Tranquilidad: cálculo propio con SVS | 7 |
| 2.3 | La señal se cae | 2 | Grabar 60 s | Corte de luz: el seguidor se detiene y ella sigue la Luna a mano con 2 perillas. La toma sale temblorosa; con el barrio a oscuras, la luz cenicienta se ve mejor | La Luna recorre su propio diámetro (29,6′) en unos 2 min | cálculo propio | 5 |
| 2.4 | Ecuador ya dejó un mensaje | 2 | Superar la duda | Diálogo de duda con Órbita (3 respuestas, ninguna castiga); Ari y ella ordenan 9 diapositivas en el atril (MIR-05) por pistas visibles en cada foto | 1873 Observatorio de Quito · 1957 estación Quito · 1969 disco con el mensaje de Velasco Ibarra (73 países) · 1975 Apolo-Soyuz · 14-11-1981 despedida del STS-2 · 01-07-1982 entrega a Ecuador · 2007 EXA · 2013 Pegaso · 21-06-2023 Acuerdos Artemisa, firmante n.º 26 | A1, A2, A4, E1, E2, E3, E6; 03a | 5 |
| 2.5 | Bajada de los faroles | 2 → E → 1 | Volver a casa y dormir | Atajo de los faroles, que abre Ari; barrio de noche; la Luna se pone a las 21:07; Elena mira el cielo en el patio; la caja de cartón de Rafael espera junto a la cama | Puesta de la Luna a las 21:07, con el borde superior en el horizonte y la refracción | Hz y `luna_parametros.py` | 3 |
| | **Acto III · «Tranquilidad»** (el sueño) | | | | | | **32** |
| 3.1 | Alunizaje de cartón | 3 | Llegar y aprender a moverse | La caja de Rafael aterriza con un golpe sordo; pista corta: caminar a saltos, frenar con anticipación, saltar una zanja | Gravedad de 1,624 m/s², cerca de 1/6 de la terrestre: baja el peso, no la masa. Se aterriza fuera del límite de 2 km del sitio | L6 y R4, 03b | 4 |
| 3.2 | La herramienta correcta | 3 | Recoger 4 muestras distintas | Elegir cucharón de caja, pinzas pequeñas o tubo de núcleo con martillo; una mala elección muestra por qué falla | Herramientas del Apolo 11: cucharón de caja, pinzas pequeñas y tubos de 2 cm hincados con martillo. Regolito: polvo y roca de impactos de miles de millones de años | L1, L3, L8; 03b | 7 |
| 3.3 | Una roca necesita su registro | 3 | Registrar 3 muestras | Bolsa numerada, croquis del lugar y ficha. Un número equivocado se corrige en el registro sin perder la muestra | Las bolsas numeradas ligaban cada muestra a su registro. En el Apolo 11 la documentación fue «bastante simple»; el protocolo completo llegó después (S8) | L4 **corr.**, 03b | 4 |
| 3.4 | Mirar sin borrar | 3 | Ver el sitio del Apolo 11 sin entrar | Rodear el anillo cian de 75 m; zoom a la etapa de descenso, sus patas y las huellas; foto «vista con el Apolo» con la Tierra arriba | La etapa de descenso se quedó en la Luna. Recomendación de 75 m de exclusión. Los objetos conservan dueño. La bandera histórica no está confirmada en pie. La Tierra, casi fija a unos 66° de altura | L11, L12, R2, R3; 03b. Altura de la Tierra: cálculo propio con SVS | 6 |
| 3.5 | Dos banderas, un cielo | 3 | Colocar juntas las banderas de Estados Unidos y Ecuador | Elegir sitio fuera del anillo, armar los 2 conjuntos, hincar con ritmo, extender las barras, igualar alturas; amanece en el sueño | Banderas de 0,91 × 1,52 m con mástil de 2,44 m y barra horizontal: no hay viento. Una bandera no da territorio (art. II). Ecuador firmó los Acuerdos Artemisa. En 2011, Nader dijo que la EXA quería poner la bandera ecuatoriana en la Luna | L10, R1, E1; 03b y 03a | 6 |
| 3.6 | Volver como el módulo de mando | 3 → 1 | Regresar | Ordenar 6 pasos del regreso; mantener el escudo térmico de la caja dentro de un margen de ángulo (lazo de control); despertar | Solo volvió el módulo de mando: reentró con el escudo por delante y amerizó en el Pacífico el 24-07-1969, a unas 13 millas náuticas del USS Hornet. El Apolo 11 trajo 21,5 kg en 58 muestras; las 6 misiones, 382 kg | L12, L13, L5 **corr.**; 03b | 5 |
| | **Acto IV · «Una referencia fija»** (día 2 y noche 2) | | | | | | **13** |
| 4.1 | El arreglo | 1 | Que el seguidor funcione solo | Rompecabezas final: darle al motor la velocidad conocida del cielo (prealimentación) y dejar que el control corrija solo el error; batería contra los cortes (más fácil con S4) | Prealimentación más realimentación: el control solo corrige lo que la referencia no predice | Concepto de la carrera; 15° por hora, cálculo propio | 5 |
| 4.2 | La Luna de todos | E → S → 2 | Grabar y enviar los 60 s | Todos suben al Mirador: Rafael con la batería, Sam con el codificador, Lidia con jugos; Elena y Rafael miran por primera vez; elegir la mejor toma | Noche 2 a las 19:30: 19,0 % iluminada, a 31,0° de altura y 402 285 km. Se pone hacia las 21:50–22:00 | Hz, consulta del 12-11-2026; hora exacta de la puesta pv (falta la refracción) | 5 |
| 4.3 | La primera página | 2 → 1 | Cerrar el capítulo | Elegir qué observación va en la primera página; Ari recibe el turno del telescopio; llamada de la Dra. Vega; gancho del capítulo 2 | Mañana, 14-11-2026, se cumplen 45 años de la despedida del STS-2 a los 75 empleados de la estación Quito (07:04, hora local) | A2, 03a | 3 |
| | **Total de la ruta principal** | | | | | | **94** |

### 3.2 Por qué dura eso cada escena

Método de A. Supuestos: 3 m/s caminando en la Tierra; unos 4 m/s a saltos en la Luna; una línea de diálogo cada 4 s (15 por minuto); rompecabezas de 3 o 4 intentos de unos 50 s, con el fallo aparte.

| # | Recorrido | Diálogo | Mecánica | Fallo y reintento | Total |
|---|---:|---:|---:|---:|---:|
| P.0 | 0 | 0 | 1,5 | 0,5 | 2 |
| 1.1 | 1 | 1 | 1,5 | 0,5 | 4 |
| 1.2 | 0 | 1 | 3,5 | 1,5 | 6 |
| 1.3 | 0,5 | 1,5 | 1 | 0 | 3 |
| 1.4 | 2 (unos 300 m) | 0,5 | 1 | 0,5 | 4 |
| 1.5 | 0,5 | 1,5 | 2,5 | 0,5 | 5 |
| 2.1 | 1,5 (subida) | 1 | 2 (antena) | 0,5 | 5 |
| 2.2 | 0,5 | 1,5 | 4 (eje, buscar, enfocar, 3 rasgos) | 1 | 7 |
| 2.3 | 0 | 1 | 3 (2 tomas de 60 s) | 1 | 5 |
| 2.4 | 0,5 | 2 (la duda) | 2 (9 diapositivas) | 0,5 | 5 |
| 2.5 | 2 (unos 350 m) | 1 | 0 | 0 | 3 |
| 3.1 | 1 | 0,5 | 2 | 0,5 | 4 |
| 3.2 | 2 | 0,5 | 3,5 (4 objetivos) | 1 | 7 |
| 3.3 | 0,5 | 0,5 | 2,5 (3 registros) | 0,5 | 4 |
| 3.4 | 2 (medio anillo, unos 240 m) | 1 | 2,5 (zoom y foto) | 0,5 | 6 |
| 3.5 | 1 | 1 | 3 | 1 | 6 |
| 3.6 | 0,5 | 1 | 3 (orden y escudo) | 0,5 | 5 |
| 4.1 | 0,5 | 1 | 3 | 0,5 | 5 |
| 4.2 | 1,5 | 1,5 | 2 | 0 | 5 |
| 4.3 | 0,5 | 1,5 | 1 | 0 | 3 |
| **Suma** | **18** | **20,5** | **44,5** | **11** | **94** |

- **Lectura:** el 47 % es mecánica y el 22 % diálogo (unas 310 líneas). Es un juego, no una novela visual.
- **Piso de 60 min:** el jugador rápido queda en unos 66 min (×0,7).
- **Prueba obligatoria** (F2-03): cronometrar a 3–5 personas que no conozcan el juego con el primer prototipo de punta a punta.

### 3.3 Contenido espacial por acto

| Acto | Min | Espaciales | Escenas espaciales |
|---|---:|---:|---|
| Prólogo y I | 24 | 11 | 1.2 y 1.5 |
| II | 25 | 22 | 2.1 a 2.4 |
| III | 32 | 32 | todas |
| IV | 13 | 13 | todas |
| **Total** | **94** | **78 (83 %)** | |

---

## 4. El sueño lunar

### 4.1 Cómo se llega

1. Al final de 2.5, la cama brilla con un borde cian. Junto a ella, la caja de cartón de los adornos de Navidad que Rafael dejó «por si necesitas guardar algo», con el dibujo de la Luna que ella hizo en el cuaderno.
2. Transición en el motor, saltable: el ventilador baja de giro, el barrio se apaga, las estrellas pegadas del techo se encienden, la sábana se vuelve regolito y la ventana, la Tierra. La transición **esconde la carga**: sin pantalla negra.
3. Si la carga tarda más, la pantalla es la página del cuaderno con la ficha «Luz cenicienta» que ella marcó en 2.2: el puente visual entre el escenario 2 y el 3.

### 4.2 Dónde y cuándo

| Pregunta | Respuesta | Verificación |
|---|---|---|
| Lugar | Cerca del sitio del Apolo 11, Mar de la Tranquilidad (unos 0,67° N y 23,47° E) | Coordenadas: pv |
| Por qué ahí | Es donde viajó el mensaje de Ecuador (A4) y el «Apolo» que todos conocen | A4: confirmado |
| Momento | La misma noche del 12-11-2026 | F2-02 |
| Luz al llegar | **De noche.** A las 19:30 de Guayaquil (00:30 UT del 13-11), el Sol está unos 25° bajo el horizonte de Tranquilidad | cálculo propio con SVS |
| La Tierra en el cielo | Casi llena, cerca del **87 %** (fases opuestas: complemento del 12,6 % de la Luna). A unos **66° de altura**; durante el mes oscila entre 59° y 73° | L9 (03b) y cálculo propio con SVS |
| Amanecer real | Hacia el 15-11-2026 a las 02:00 UT (21:00 del 14-11 en Guayaquil): **unas 50 h** después | cálculo propio con SVS |
| Licencia del sueño | El sueño comprime el tiempo y amanece sobre las banderas (3.5). Órbita: «Aquí, de verdad, faltarían unos dos días» | Declarado como «Sueño» |

**Consecuencia de diseño:** la protagonista camina bajo la Tierra casi llena, la misma luz que vio como luz cenicienta desde el Mirador. Encaja con la luz de noche de la [[Biblia de arte]] §7 (principal azul fría, sombra azul profunda). La cámara alta no ve el cielo, así que hay 4 tomas con cámara baja: llegada, foto con el sitio, banderas y despedida.

**Cómo se calculó:** distancia angular entre el sitio y los puntos subsolar y subterrestre de `externos/nasa_svs_5587_tabla/mooninfo_2026.json`, hora por hora. Hay que repetirlo con Horizons antes del texto final (F2-15).

### 4.3 Qué se hace

**Caminar a 1/6 g (3.1)**
- 1,624 m/s² (L6). Al acelerar y frenar se nota la inercia: frenar exige anticipación. El paso a saltos es el más eficiente.
- Sin sonido exterior: solo traje, respiración y la voz de Órbita por la radio del casco.
- La caja de cartón aterriza **fuera del límite de descenso de 2 km** (R4). El mapa lunar está a escala 1:4 y el cuaderno lo dice: los 2 km se recorren en unos 500 m de juego.
- Órbita lleva un casco de burbuja y flota un poco más porque pesa menos; sus huellas son las únicas de gato en la Luna (chiste recurrente de C).

**Recolectar muestras con las herramientas del Apolo 11 (3.2 y 3.3)**

| Herramienta | Para qué | Objetivo en el juego | Dato |
|---|---|---|---|
| Cucharón de caja | Suelo y fragmentos pequeños | Regolito fino junto a un cráter pequeño | L1 |
| Pinzas pequeñas | Rocas sueltas | Una roca oscura de basalto | L1 |
| Tubo de núcleo de 2 cm y martillo | Una columna que conserva las capas | Dos golpes de más rompen el ritmo; uno de menos deja el tubo corto | L3 |
| Bolsa numerada, croquis y ficha | Ligar la muestra a su registro | 3 muestras registradas | L4 |

- **Bolsa equivocada:** la muestra no se pierde; se corrige el registro, igual que en el taller se anota qué cambió.
- **Nadie se lleva nada de la Luna:** al despertar, las bolsas vuelven como páginas del cuaderno, no como rocas (B).
- **Lo que no es del Apolo 11** (rastrillo, tubos de 4 cm, gnomon con 3 fotos antes y 1 después; el gnomon en el Apolo 11 es **pv**) va en la secundaria S8, declarado como equipo de los Apolo 15 a 17 (L2, L3, L4).

**Ver el Apolo respetando su sitio (3.4)**
- Anillo de luz cian tenue a 75 m de la etapa de descenso (R3). El cian es interacción según la biblia; aquí significa «mira, no toques». Cruzarlo no castiga: la protagonista se detiene sola y Órbita dice por qué. El juego lo presenta como buena costumbre, no como ley (R3 son recomendaciones; R5 solo obliga a acuerdos con NASA).
- Con zoom se ven la etapa de descenso, sus patas y las huellas de 1969. La placa se ve sin texto legible; su contenido no se cita (pv).
- **La bandera del Apolo 11 no se muestra en pie** (L11). Órbita cuenta que, según Aldrin, la derribó el despegue.
- **Momento emocional:** Órbita recuerda que el mensaje de Ecuador viajó en un disco del tamaño de una moneda de 50 centavos (A4). Que el disco quedara en el sitio es **pv**: hasta verificarlo, el texto dice «viajó hasta aquí», no «está aquí».
- **Foto «vista con el Apolo»:** la protagonista y Órbita en primer plano, la etapa de descenso al fondo y la Tierra arriba. Es la recompensa de la misión y la imagen del capítulo.

**Colocar juntas las banderas de Estados Unidos y Ecuador (3.5)**

1. **Elegir el sitio:** la «Loma de las Dos Banderas» (ficción), a unos 150 m de la etapa de descenso: el doble del radio de protección y sin huellas históricas.
2. **Armar los conjuntos:** dos banderas nuevas del mismo tamaño, 0,91 × 1,52 m, con mástil de 2,44 m y barra horizontal (L10). Malla fija con pliegues modelados (B).
3. **Hincar el mástil:** golpear con ritmo, no con fuerza. La profundidad real del Apolo 11 es pv; la mecánica no depende de la cifra.
4. **Extender la barra:** si no se extiende del todo, la tela queda ondulada, como le pasó a la tripulación del Apolo 11 (L10, Platoff). No hay viento.
5. **Igualar alturas:** las dos a la misma altura, separadas lo justo para que ninguna tape a la otra.
6. **Ceremonia:** la protagonista recuerda que en 2011 Ronnie Nader dijo que la EXA quería poner la bandera ecuatoriana en la Luna (*Sobrevuelo* 2011, p. 25; 03a). Se presenta como un sueño dicho en voz alta, no como un hecho.
7. **Amanece:** la luz del Sol entra rasante y la escena queda 10 s en silencio, sin interfaz.

- **Dato:** el art. II del Tratado del Espacio prohíbe la apropiación nacional (R1). Ecuador es el firmante n.º 26 de los Acuerdos Artemisa (E1), lo que no le da un vuelo lunar. La misión expresa cooperación.
- **Bandera de Ecuador:** con escudo, para que no se confunda con la de Colombia; proporción 3:2 según el instructivo de 2009 (copia no oficial, pv contra el original). La Constitución la reconoce como símbolo patrio (R8). Antes de publicar, opinión de un abogado (03a, #25).
- **Reglas fijas:** no se pueden soltar, tirar ni dañar; no hay animación de caída; no se toca la bandera histórica; no son premio ni chiste.

### 4.4 Cómo se vuelve (3.6)

1. **Orden del regreso** en el cuaderno, 6 pasos: despegue de la etapa de ascenso, encuentro en órbita lunar, separación del módulo de servicio, reentrada con el escudo térmico, paracaídas y amerizaje (L12, L13).
2. **Reentrada jugable (C):** la caja de cartón cae hacia la Tierra y el jugador mantiene el escudo por delante, dentro de un margen de ángulo. Es un lazo de control, el oficio de la protagonista.
3. **Sensaciones (A):** el calor de la reentrada se vuelve el sol de la mañana en la cara; los paracaídas, la cortina que abre Elena.
4. **Montaje cruzado:** antes de despertar, 8 s de Elena en el patio, de noche, mirando la Luna acostada (lectura C de la frase).
5. **Amerizaje:** Órbita vuelca el vaso de agua de la mesita. Ella despierta mojada y riéndose a las 06:30.
6. **Cierre:** el cuaderno muestra las fichas del sueño con el sello «Sueño» y los datos con «Dato medido». El Apolo 11 trajo 21,5 kg; el 17, 110,5 kg; las 6 misiones, 382 kg (L5 corr.). Ella trajo 4 bolsas que pesan cero, y una idea.

**Volver a soñar:** desde el final del acto III, la cama ofrece «Soñar otra vez» cualquier noche. Las banderas siguen donde se plantaron. «Despertar» está siempre en el menú del cuaderno: no hay muerte en el sueño.

### 4.5 La frase ambigua: «siendo vista con el Apolo que llegó a la Tierra»

| Lectura | Qué significaría | Cómo se juega | A favor | En contra |
|---|---|---|---|---|
| **A** | Verla **junto al módulo lunar del Apolo 11**, que sigue en la Luna | Foto de 3.4 con la etapa de descenso al fondo | Fiel a L12 y R3; barata; ya está en la ruta | La etapa de descenso nunca «llegó a la Tierra» |
| **B** | El Apolo que **sí volvió**: el módulo de mando | Regreso de 3.6 con sus 6 pasos y el lazo de control del escudo, con la caja de cartón en vez de la cápsula real | Cumple «llegó a la Tierra» al pie de la letra (L13) | No muestra la cápsula real, para evitar insignias |
| **C** | Ser **vista desde la Tierra** | Montaje de 8 s de Elena mirando la Luna desde el patio | Cierra el arco familiar | No muestra ningún Apolo |
| **D** | **Testigo en 1969** o vista por un astronauta | El sueño ocurre en 1969, o una silueta la saluda | Muy emotiva | Mostraría astronautas reales o lo parecería; 2 cinemáticas caras. **No se recomienda** |

**Recomendación (F2-08):** A + B + C, como está en la ruta. D, descartada.

> **Pregunta abierta para Guillermo:** ¿qué quisiste decir con «siendo vista con el Apolo que llegó a la Tierra»? ¿A, B, C, D, una mezcla u otra cosa?

---

## 5. Mapa de mundo abierto

### 5.1 Nodos y rutas

```
[1 Habitación] ─escalera─ [1b Casa] ─puerta─ [E Las Escalinatas] ─ [E Plaza de las Iguanas] ─ [E Mercado]
      │                                            ▲                       │
      │ cama (dormir / despertar)                  │                [S Sendero del arroyo]
      ▼                                            │                  arroyo, puente, antena
[3 Luna: llegada de la caja] ─ [campo de muestras] │                       │
      ─ [anillo de 75 m] ─ [Loma de las Dos Banderas]                [2 Mirador del Faro] ─ocular─ [telescopio]
                                                   │                       │
                                                   └──── atajo de los faroles (desde 2.4) ─┘
```

**Distancias de diseño:** casa 60 m de recorrido; Las Escalinatas unos 160 m de subida; plaza y Mercado 120 × 80 m; sendero unos 300 m; Mirador 40 × 30 m; atajo de bajada unos 350 m; Luna unos 600 × 450 m a escala 1:4.

### 5.2 Desbloqueos

| Tramo | Cómo se pasa | Se abre | Motivo en la historia |
|---|---|---|---|
| Habitación ↔ casa | Escalera interior, sin carga | Desde el inicio | El cuarto es el tutorial |
| Casa ↔ Las Escalinatas | Puerta de la calle | Al terminar 1.3: Elena entrega la libreta | La familia «da permiso» para salir al mundo |
| Escalinatas ↔ Plaza ↔ Mercado | A pie, continuo | Con la puerta | Barrio abierto; secundarias del lote 1 |
| Plaza ↔ sendero ↔ Mirador | A pie, continuo | Tras el codificador (1.5). Antes, Órbita: «Con tanto sol no vas a ver la Luna» | El reloj pasa a la tarde |
| Mirador → barrio (atajo de los faroles) | Portón del cerro | Ari lo abre tras 2.4; primero de bajada, luego en los dos sentidos | Volver antes de las 21:30, como pidió Elena (sin castigo) |
| Mirador ↔ telescopio | Acercarse al ocular | Desde 2.2 | La carga se esconde en el acercamiento |
| Cama → Luna | Dormir | Tras 2.5 (la primera vez es obligatoria) | El sueño es la única «nave» |
| Dentro de la Luna | A pie, a saltos | Llegada → muestras (tras 3.1) → anillo (tras 3.3) → Loma (tras 3.4) | Cada zona enseña lo que necesita la siguiente |
| Luna → cama | Terminar 3.6; después, «Despertar» desde el cuaderno | Siempre | Salida clara |
| Día 2 | Todo el mapa abierto; el Mirador se activa al anochecer (4.2) | Tras 4.1 | Último paseo libre antes del clímax |
| Viaje rápido | Mapa del cuaderno (`ANC_MAPA`) entre nodos visitados | Desde el día 2; el primer recorrido siempre a pie | — |
| Después del final | Todo abierto; telescopio con la fecha real del jugador; «Soñar otra vez» | Tras 4.3 | Juego libre y secundarias |

### 5.3 Reloj por hitos (F2-09)

El reloj avanza por hitos, no por minutos reales: **la Luna no se puede perder.**

| Hito | Escenas | Luz | Qué cambia en el barrio |
|---|---|---|---|
| Mañana, día 1 | 1.1–1.5 | Mañana (nueva en la biblia) | Lidia abre el kiosco; Sam en el Mercado |
| Tarde | 2.1 | Tarde (luz base de la biblia) | Iguanas en los muros; periquitos |
| Noche con Luna | 2.2–2.4 | Noche | Faroles y guirnalda del Mirador |
| Noche sin Luna | 2.5 | Noche | Vecinos en las puertas; Elena en el patio |
| Sueño | 3.1–3.6 | Noche lunar → amanecer | — |
| Mañana, día 2 | 4.1 | Mañana | Cambios persistentes visibles |
| Tarde y noche 2 | 4.2–4.3 | Tarde → noche | Todos suben al Mirador |

**3 estados de luz horneados** (mañana, tarde y noche) en lugar de un ciclo continuo: la tarde y la noche del día 2 reutilizan las del día 1.

### 5.4 Cargas

| Umbral | Qué la esconde | Meta |
|---|---|---|
| Casa ↔ calle | Abrir la puerta (fundido de 1 s) | ≤ 3 s en la HD 620 |
| Plaza ↔ sendero | Curva del camino; el cerro tapa la vista (solo si la memoria lo exige) | ≤ 3 s |
| Mirador ↔ ocular | El acercamiento al telescopio | ≤ 3 s |
| Cama ↔ Luna | La transición del sueño; si no alcanza, la ficha «Luz cenicienta» | Sin pantalla negra |

Cada pantalla de carga es una página del cuaderno con un dato real y su fuente (A y B). Los umbrales y su medición están en [[Plan de auditoria]] §3.2.

---

## 6. Reparto y Órbita

Según la hoja [[Catalogo de recursos#Reparto · v1]] (`HR_PER_v1.png`). Los nombres vienen del guion anterior y siguen siendo propuestas.

| ID | Personaje | Papel | Arco | Escenas |
|---|---|---|---|---|
| PER-01 | **Protagonista** (nombre por decidir) | Estudiante de ingeniería de control; vive en Las Escalinatas; construyó un seguidor motorizado. Habla de la NASA solo como sueño personal | Del «es demasiado lejos» al «depende de dónde mido» | Todas |
| PER-02 | Protagonista B | Si hay creador de personaje, segundo cuerpo. Si la protagonista es fija, **un primo del colegio técnico** que ayuda en S4 | Ninguno propio | P.0 o S4 |
| PER-03 | **Elena**, la madre | Vende almuerzos en el barrio y entrega la libreta. Su miedo: que su hija se vaya lejos | De «queda lejísimos» a mirar por el telescopio en 4.2 | 1.3, 2.5, 3.6, 4.2 |
| PER-04 | **Rafael**, el padre | Repara electrodomésticos; de él viene el gusto por los circuitos. Su caja de cartón se vuelve la cápsula del sueño | Apoyo callado: en 4.2 trae la batería que faltaba | 1.3, 2.5, 4.2 |
| — | **El abuelo** (padre de Rafael, **ficción**) | Trabajó en la estación del Cotopaxi: un homenaje al personal ecuatoriano, que pasó de 50 a 220 personas (03a). Solo en foto y recuerdos. **Nunca se dice que siguiera al Apolo 11** (A3) | — | 1.3, S6 |
| PER-05 | **Lidia** | Kiosco de jugos de la Plaza de las Iguanas; la voz del barrio | Ancla de humor; sube jugos al Mirador en 4.2 | 1.4, S2, 4.2 |
| PER-06 | **Sam** | Compañero de carrera con un puesto de piezas en el Mercado; piensa dejar los estudios para trabajar | Su duda refleja la de ella. En 4.2 sube con el codificador nuevo y decide terminar el semestre | 1.5, S7, 4.2 |
| PER-07 | **Dra. Vega** | Ingeniera ecuatoriana de un centro espacial internacional **ficticio**; aparece en el video de la convocatoria. Su regla, «un parámetro a la vez», es la del juego | Modelo a seguir; en 4.3 llama para anunciar la siguiente ronda | 1.2, 4.3 |
| PER-08 | **Ari** | Colegiala del club de observación del Mirador. Le recuerda que Ecuador ya llegó a la Luna y abre el atajo | Recibe el turno del telescopio en 4.3: el relevo | 2.4, S1, S3, 4.2, 4.3 |
| PER-09 | **Órbita** | Gato científico y compañero | Ver abajo | Todas |

### 6.1 Órbita, cinco funciones

| Función | Cómo se juega |
|---|---|
| Guía de datos | Da las fichas con fuente y hora, como ya hace en la prueba del telescopio |
| Pistas en 3 niveles | Una mirada, luego una frase, luego la respuesta. Nunca dice «incorrecto»: explica la causa |
| Señal de interacción | Su chapa cian brilla cerca de lo que se puede tocar: la única pista visual (pilar «el cian es tecnología»). Huele recolectables a menos de 8 m |
| Se cuela | Entra por huecos y trae piezas (COL) o abre un pestillo |
| Compañía | En la duda (2.4) se le sube al regazo. No discute: se queda |

- **Despierta la protagonista:** las frases de Órbita salen en el globo del cuaderno; la familia solo oye maullidos (chiste recurrente).
- **En el sueño:** casco de burbuja, traje pequeño original sin insignias y voz por la radio del casco. Es la primera vez que ella lo oye hablar en voz alta.

---

## 7. Misiones

### 7.1 Principales

| ID | Misión | Escenas | Recompensa |
|---|---|---|---|
| M1 | La convocatoria | 1.1–1.2 | Seguidor v1 y página «Realimentación» |
| M2 | Piezas del cerro | 1.3–1.5 | Libreta, codificador y ficha «Pegaso» |
| M3 | Rastrear como en el Cotopaxi | 2.1 | Antena operativa y página «Ganancia» |
| M4 | La Luna de esta noche | 2.2–2.3 | Página «Luna sonriente» (fase 1 de S1), ficha «Luz cenicienta» y la toma temblorosa |
| M5 | Ecuador ya dejó un mensaje | 2.4–2.5 | Línea de tiempo, paráfrasis del mensaje ecuatoriano y atajo de los faroles |
| M6 | Seis veces más ligera | 3.1 | Salto lunar y ficha «Masa y peso» |
| M7 | Muestras con registro | 3.2–3.3 | 4 muestras registradas y página «Regolito» |
| M8 | Mirar sin borrar | 3.4 | Foto con el Apolo y ficha «Etapa de descenso» |
| M9 | Dos banderas, un cielo | 3.5 | Foto al amanecer y página «Cooperación» |
| M10 | Volver como el módulo de mando | 3.6 | Comparación con los 382 kg y «Soñar otra vez» |
| M11 | Una referencia fija | 4.1 | Seguidor v2 |
| M12 | La Luna de todos | 4.2–4.3 | Video enviado, fase 2 de S1 y gancho del capítulo 2 |

**Seis sistemas para todo el juego** (B): circuito y multímetro (1.5, S2, S4) · control y gráfica (1.2, 2.1, 4.1, 3.6) · telescopio (2.2, 2.3, 4.2, S1) · ordenar tarjetas (2.4, 3.6) · cámara y registro (3.3, 3.4, S3, S8, S9) · herramientas y bolsas (3.2, S8).

### 7.2 Secundarias

**Lote 1, con la ruta principal (23 min)**

| ID | Misión | Dónde | Se abre | Qué se aprende | Verificación | Min | Recompensa |
|---|---|---|---|---|---|---:|---|
| S1 | Bitácora lunar | 2 | 2.2 | 3 fases: noche 1 (12,2 %), noche 2 (19,0 %) y la fecha real del jugador después del final | Hz | 6 | Carta estelar COL-12 |
| S3 | Mirar sin espantar | E, S | 1.4 | Fotografiar 6 especies (FAU) para el club de Ari; si el animal huye, la ficha no cuenta. La misma regla que en la Luna | — | 6 | Pegatinas; los animales se asoman a la ventana por la mañana |
| S4 | Chatarra útil | E, S | 1.4 | Batería (COL-07) y panel (COL-02): energía para no depender de la red | — | 5 | 4.1 más fácil: el seguidor resiste los cortes |
| S8 | Otro tiempo, otras herramientas | 3 | Al volver a soñar | Rastrillo, tubos de 4 cm, gnomon y protocolo de 3 fotos antes y 1 después: equipo y método de los Apolo 15 a 17, no de 1969 | L2–L4, 03b (que el Apolo 11 no llevara gnomon: **pv**) | 6 | 2 muestras más y ficha «Herramientas por misión» |

**Lote 2, después (28 min)**

| ID | Misión | Dónde | Qué se aprende | Verificación | Min | Recompensa |
|---|---|---|---|---|---:|---|
| S2 | La radio de Lidia | E | Reparar una radio (COL-04): continuidad con el multímetro | — | 5 | La radio suena en el kiosco (cambio persistente) |
| S5 | La escalinata del tiempo | E | 9 placas pintadas en los escalones, con los mismos hitos de 2.4 y detalles: llamas junto a la antena (1973), 578 160 horas de apoyo en 22 años, personal de 50 a 220, despedida del STS-2 a las 07:04 | 03a | 6 | Póster de la línea de tiempo en la Habitación |
| S6 | La foto del abuelo | 1b | 3 recuerdos (credencial sin logotipos, carta y foto). La estación pasó a Ecuador el 01-07-1982. Ficción declarada; nunca el Apolo 11 | A1 **corr.**, 03a | 5 | Escena con los padres; la foto se cuelga en el cuarto |
| S7 | Pegaso, la historia completa | E | Anomalía del 23-05-2013 tras acercarse a un cuerpo de cohete de 1985; NASA no confirmó un choque; contacto recuperado el 25-01-2014; órbita de 627 × 654 km. Enseña a no convertir una hipótesis en certeza | E5, 03a | 4 | Página de Sam; chapa del satélite para el collar de Órbita, sin logotipos |
| S9 | Postales de la Tierra | 3 → E | Fotografiar la Tierra en distintos sueños: fases opuestas a las de la Luna | L9, 03b | 4 | Postales en las puertas de los vecinos (cambio persistente) |
| S10 | Noche lunar | 3 | 5 puntos de interés: unos −173 °C en la oscuridad y +127 °C a pleno Sol; cráteres y regolito; la Tierra que no se pone | L7–L9, 03b (que no se ponga en el sitio es deducción, no cita) | 4 | Página «Noche lunar» |

**Total de secundarias: 51 min. Con todo: 145 min.**

### 7.3 Mundo vivo acotado (F2-13)

- **Rutinas por hito** de 4 vecinos: Elena, Rafael, Lidia y Sam. El resto, quietos o de paso.
- **Fauna por hito:** 6 especies del catálogo FAU (iguanas y periquitos de tarde; garzas al anochecer; cangrejos y gato callejero de noche).
- **El barrio recuerda, 6 cambios:** la radio de Lidia suena; la antena del sendero sigue apuntando; la guirnalda del Mirador queda encendida; la línea de tiempo cuelga en el cuarto; las banderas siguen en cada sueño; las postales de la Tierra aparecen en las puertas.
- **Movimiento sutil:** ropa tendida, cables que se mecen, hojas del flamboyán, ondas del arroyo y polvo lunar que cae despacio.

---

## 8. Datos: qué se usa y con qué verificación (F2-15)

### 8.1 Confirmados y usados

| Código | Dato usado | Verificación |
|---|---|---|
| A1 | Estación Quito al pie del Cotopaxi, 3 650 m; operó de 1957 a 1981 y pasó a Ecuador el 01-07-1982; antenas de 12 m | 03a, **corr.** |
| A2 | Apolo-Soyuz en 1975; despedida del STS-2 el 14-11-1981 a las 07:04 a 75 empleados | 03a |
| A4 | Disco de buena voluntad: 73 países, mensajes reducidos 200 veces, del tamaño de una moneda de 50 centavos; mensaje de Velasco Ibarra (paráfrasis fiel) | 03a |
| E1 | Acuerdos Artemisa: Ecuador, n.º 26, el 21-06-2023 | 03a |
| E2–E4 | EXA, ONG de 2007; Pegaso: cubo de 10 cm, paneles de 27 cm, 25-04-2013 (según el equipo); iniciado en 2010 | 03a, E4 **corr.** |
| E5 | Anomalía de 2013 sin colisión confirmada; contacto el 25-01-2014 | 03a |
| E6 | Observatorio Astronómico de Quito, 1873 | 03a |
| E7 | Chimborazo: unos 6 384,4 km del centro; 2,1 km más que el Everest | 03a, **corr.** (IGM-ESPE 2019) |
| Nader 2011 | Meta dicha de poner la bandera ecuatoriana en la Luna | 03a, *Sobrevuelo* p. 25 |
| L1–L13 | Herramientas, gravedad, temperaturas, regolito, Tierra en el cielo, banderas, etapa de descenso, regreso y masas | 03b (L4 y L5 **corr.**) |
| R1–R4 | Art. II; propiedad (arts. VIII y IX); 75 m; 2 km | 03b |
| R6–R7 | Sin insignias; sin «NASA» en el título comercial | 03b (R7 **corr.**, más estricto) |
| R8 | Bandera, escudo e himno: símbolos patrios (Constitución, art. 2) | 03a |
| Hz | Luna del 12-11 (12,2 %, 403 151 km, 192,6°, puesta 21:07) y del 13-11 (19,0 %, 31,0°, 402 285 km a las 19:30) | Medido con `luna_efemerides.py` |

### 8.2 Cálculos propios (comprobar con Horizons antes del diálogo final)

| Cálculo | Valor | Con qué |
|---|---|---|
| Giro aparente del cielo | Unos 15° por hora | 360° / 24 h |
| La Luna recorre su diámetro | Unos 2 min | 29,6′ a unos 14,5° por hora |
| Polo sur celeste desde el Mirador | Unos 2,2° sobre el horizonte | Latitud del script, 2,18° S |
| Tranquilidad de noche el 12-11 a las 19:30 | Sol unos 25° bajo el horizonte | `mooninfo_2026.json` |
| Tierra vista desde Tranquilidad | Cerca del 87 %, a unos 66° (entre 59° y 73° en el mes) | `mooninfo_2026.json` |
| Amanecer real en Tranquilidad | Unas 50 h después (15-11-2026, 02:00 UT) | `mooninfo_2026.json` |

### 8.3 Pendientes de verificar (no entran al diálogo final)

| Dato | Dónde | Qué hacer |
|---|---|---|
| Que el disco quedara en el sitio del Apolo 11 | 3.4 | Fuente primaria (informe de misión) |
| Coordenadas del sitio del Apolo 11 | 4.2 | Fuente primaria de NASA |
| Hora exacta de la puesta del 13-11 con refracción | 4.2 | `luna_parametros.py` sobre la consulta de hoy |
| Profundidad del mástil en el Apolo 11 | 3.5 | ALSJ o informe de misión |
| Si el Apolo 11 llevó gnomon (03b solo fecha en 15–17 el protocolo de fotos) | 4.3, S8 | Lista de herramientas del Apolo 11 (JSC o ALSJ) |
| Bandera de Ecuador: proporción y escudo en la norma oficial; uso en una obra | 3.5 | Original del instructivo y la Resolución 24-047; abogado |
| Nombre «Columbia» del módulo de mando | — | Por eso ninguna misión lleva ese nombre |
| Planetario de la Armada, 24-07-1984 (E8) | Fuera de la ruta | Fuente de INOCAR; podría volver como objeto opcional |
| «Ventana Lunar» no coincide con un programa real | Toda la historia | Búsqueda antes de fijar el nombre |
| Licencia y crédito de una textura de la Tierra de NASA | 3.4, S9 | Guía de imágenes de NASA; la descarga necesita el permiso de Guillermo |
| Cortes de luz como contexto del país | 2.3 | Solo ambiente; ninguna cifra sin fuente |

### 8.4 No se usan, por falta de fuente

- Que la estación Quito rastreara el Apolo 11 (A3).
- El paradero de las rocas lunares regaladas a Ecuador, ni que se perdieran (A5, A6).
- El cohete de Pegaso (LM-2D) y la fecha en UTC.
- Los 6 384 415,98 m del Chimborazo.
- Los 444 escalones del cerro Santa Ana y las mareas del Guayas sin la tabla de INOCAR.

---

## 9. Lo que esta historia le pide a la auditoría

La auditoría de pantallas de carga, menús, botones, jugabilidad, escenarios, caminos y texturas está en [[Plan de auditoria]]. Este documento responde su bloqueo **B3** (propuesta narrativa), propone **B4** (frase ambigua, sigue abierta) y **B8** (corte vertical). Lista de comprobación narrativa, en el orden pedido:

| Orden | Escenario | Escenas | Qué debe auditarse por la historia |
|---|---|---|---|
| 0 | Transversal | P.0, todas | Menú con la cámara que baja de la Luna a la ventana; cuaderno con sellos y mapa; «Despertar» y «Soñar otra vez»; pantallas de carga con dato y fuente; botones del tema «cuaderno»; diálogos de 2 renglones; guardado de banderas, placas y cambios del barrio |
| 1 | Habitación | 1.1, 1.2, 2.5, 3.6, 4.1, 4.3 | 5 interactuables; rompecabezas del seguidor con gráfica; cama con borde cian; transición sin pantalla negra; luz de mañana y de noche |
| 1b–E–S | Casa, barrio y sendero | 1.3–1.5, 2.1, 2.5, 4.2 | Puerta con motivo (la libreta); bloqueo del sendero con motivo («con tanto sol…»); atajo de los faroles; antena COL-01 jugable; 3 estados de luz; rutinas de 4 vecinos |
| 2 | Mirador y telescopio | 2.2–2.4, 4.2 | Entrada al ocular desde el mundo; montura, enfoque y marcas; apagón y 2 perillas; atril con 9 diapositivas; Luna del 12-11 y del 13-11 |
| 3 | Luna | 3.1–3.6 | Caminar a 1,624 m/s²; 3 herramientas del Apolo 11; anillo de 75 m que no castiga; banderas iguales y fijas; reentrada con margen de ángulo; paleta lunar propia (no existe aún en la biblia) |
| Caminos | Todo el mapa | — | Se llega a pie de cada nodo al siguiente; minutos de recorrido coherentes con la tabla 3.2 |

---

## 10. Corte vertical (F2-14)

Unos **50 min**, para validar el tono y el ritmo antes de producir todo:

| Escenas | Min |
|---|---:|
| 1.1 y 1.2 (Habitación y seguidor) | 10 |
| 2.2 y 2.3 (telescopio y apagón), con un solo tramo del sendero | 12 |
| Cama y transición | 1 |
| 3.1 a 3.5 (del alunizaje a las banderas) | 27 |
| **Total** | **50** |

Después: el barrio, la antena, el acto IV y las secundarias del lote 1.

---

## 11. Qué se reutiliza y qué es nuevo

### 11.1 Se reutiliza

| Recurso | Estado | Uso |
|---|---|---|
| [[Escena de exploracion v1]]: terreno, arroyo, puente, flamboyán, hierba, iguana y antena COL-01 | Prueba; espera veredicto | Tramo S de día y de noche; antena de 2.1 |
| Protagonista de Tripo con niveles de 1 500 y 3 000 triángulos | Hecha | Todas las escenas |
| Órbita con rig, `reposo` y `caminar` | Verificada en Godot | Todas; faltan saltar y sentarse |
| Telescopio con la Luna real (shader, LRO, Horizons, `luna_medir.py`) | Probado; falta el ángulo paraláctico en cada instante | 2.2, 2.3, 4.2 y S1 |
| `luna_efemerides.py`, `luna_parametros.py` y `mooninfo_2026.json` | Funcionan | Noches 1 y 2, cálculos del sueño y S1 |
| Catálogo: TAL, MIR, COL, URB, ARQ, TER, VEG, FAU y PER | Concepto v1, espera veredicto | Habitación, barrio y Mirador |
| Mapa de la región del lote 02 (`ANC_MAPA`) | Maqueta | Nodos, mapa del cuaderno y viaje rápido |
| Guion anterior: libreta de Elena, regla de la Dra. Vega, kiosco de Lidia, cierre con Ari, viñeta 02 al revés | Propuesta | Adaptados al nuevo arco ([[02_historia_existente]]) |
| Ideas de misión 5 a 10 de [[01_datos_espaciales_ecuador]] | Propuesta de Codex | Base del acto III, con las correcciones de 03b |
| Lógica de `main.gd` y `player.gd` de la bóveda anterior | Estilo descartado | Menús y controlador (ver [[Plan de auditoria]]) |

### 11.2 Es nuevo

| Recurso | Cómo se haría | Créditos |
|---|---|---:|
| Habitación-taller y casa (diorama `ANC_HUB`) | Script con piezas TAL y ARQ | 0 |
| Las Escalinatas, Plaza de las Iguanas y Mercado | Script con URB y ARQ | 0 |
| Mirador del Faro en 3D | Script con MIR | 0 |
| Luna del sueño: regolito low-poly pintado, cráteres y rocas | Script (heightmap y MultiMesh) | 0 |
| Etapa de descenso (recreación sin insignias ni texto legible), herramientas, bolsas y caja de cartón | Script con fotos públicas de referencia | 0 |
| 2 conjuntos de bandera con barra horizontal | Malla fija con pliegues modelados | 0 |
| Hoja de referencia y paleta de la Luna del sueño | Lote de imagen nuevo | Partida por aprobar |
| Traje de la protagonista y casco de Órbita | Script sobre su malla, o Tripo H3.1 | 0 por script; unos 9 por malla con Tripo (partida por aprobar) |
| PER-03 a PER-08 en 3D | Tripo multivista desde hojas nuevas | Unos 54 (6 × 9), partida por aprobar |
| Tierra en el cielo lunar con fase | El shader de la Luna con textura terrestre de NASA | 0; la descarga necesita permiso |
| Mecánicas: control, seguimiento manual, tarjetas, registro, herramientas, banderas, reentrada | GDScript, en 6 sistemas | 0 |
| Unas 310 líneas de ruta principal, más unas 150 de secundarias | Guion | 0 |

---

## 12. Riesgos para el portátil mínimo (Intel HD 620)

| Riesgo | Cifra de referencia | Cómo se reduce | Cómo se controla |
|---|---|---|---|
| Exteriores pesados | El sendero da 48,3 fps a 720p con 307 000 triángulos, frente a un presupuesto de 100 000 ([[Plan de auditoria]] §3.3) | MultiMesh para mechones y flores; niveles de detalle; hierba solo en sendero y jardines; suelo pintado en el barrio | `--medir=6` a 720p y 1080p; meta según B2 (30 o 60 fps) |
| Mundo abierto continuo | 8 GB de RAM; Mobile | Nodos con 3 umbrales y el ocular; solo la zona actual y la vecina en memoria | Tiempo de carga ≤ 3 s medido en el portátil |
| Luz de mañana, tarde y noche | Un ciclo dinámico cuesta luz y sombras | 3 estados horneados; lightmap solo tras probar el horneado | Captura de cada estado con la cámara real |
| Barrio de noche con muchas luces | Mobile limita las luces por objeto | Faroles y guirnaldas con emisión y luz pintada en los vértices; pocas luces reales | Contar luces y llamadas de dibujo |
| 7 personajes en 4.2 | Personajes de 1 500 triángulos | Máximo 6 esqueletos animados; el resto quieto; animaciones simples (reposo, hablar, señalar) | Llamadas de dibujo y p95 |
| Terreno lunar abierto | Unos 600 × 450 m | Heightmap de 512 × 512 con niveles de detalle, rocas en MultiMesh, sin hierba; 1 luz direccional | Es la zona más barata; medir igual |
| Polvo lunar | Las partículas en GPU rinden poco en la HD 620 | Partículas en CPU, como máximo 64 por salto | Perfil de GPU |
| Compilación de shaders | Forward+ tardó más de 90 s en el primer arranque | Mobile y precompilación en la carga inicial | p95 del primer minuto en cada zona |
| Telescopio | 0,74 ms de GPU; 2,2 a 2,5 ms con la Luna a pantalla completa | Sin cambios | Ya medido |
| Duración < 60 min | Estimación de diseño | Prueba cronometrada; alargar el sueño si falta | Mediana ≥ 70 min |
| Alcance de producción | 94 min, 20 escenas, 10 secundarias | Corte vertical de 50 min; secundarias en 2 lotes; 6 sistemas reutilizables | Veredicto de Guillermo por puerta |
| Datos y símbolos | Juego educativo; banderas; sitio histórico | F2-15; reglas de F2-06 y F2-07; abogado antes de publicar | Revisión del guion contra R1–R8 |

---

## 13. Preguntas para Guillermo

1. **La frase del Apolo:** ¿qué quisiste decir con «siendo vista con el Apolo que llegó a la Tierra»? ¿A, B, C, D, una mezcla u otra cosa? (4.5; la recomendación es A + B + C).
2. **Protagonista:** ¿fija o con creador de personaje? ¿Qué nombre lleva? De eso depende PER-02.
3. **Bandera de Ecuador:** ¿con escudo (recomendado, para no confundirla con la de Colombia) o tricolor?
4. **Duración:** ¿apruebas 94 min de ruta principal, o prefieres acercarte a 75 y ganar tiempo de producción?
5. **Sitio del sueño:** ¿Apolo 11 (recomendado, por el mensaje de Ecuador) o Apolo 17, donde el rastrillo sí es histórico?
6. **El abuelo de la estación del Cotopaxi** como ficción declarada: ¿te gusta?
7. **Órbita:** ¿habla por el cuaderno despierta la protagonista y en voz alta solo en el sueño?
8. **Corte vertical:** ¿aprobar primero los 50 min, de la Habitación al telescopio y al sueño?
9. **Nombres:** ¿«Ventana Lunar» para la convocatoria? ¿Qué nombre para el centro espacial ficticio y para el título comercial sin «NASA»?

---

## 14. Fuentes

- Propuestas: [[Propuesta_A]], [[Propuesta_B]] y [[Propuesta_C]].
- Verificaciones: [[03a_verificacion_ecuador]] y [[03b_verificacion_apolo]].
- Investigación de Codex: [[01_datos_espaciales_ecuador]] y [[02_historia_existente]].
- Proyecto: [[Memory]], [[Biblia de arte]], [[Catalogo de recursos]], [[Escena de exploracion v1]], [[Mirador del Faro - Luna con datos reales]], [[Fase 0 - Analisis]] y [[Plan de auditoria]].
- Consulta nueva de hoy: JPL Horizons para el Mirador, 13-11-2026 de 18:00 a 23:00 cada 10 min, con `herramientas/luna_efemerides.py --inicio "2026-11-13 23:00" --fin "2026-11-14 04:00" --paso "10 m"`. La respuesta quedó fuera de la bóveda; para guardarla en `Propuestas/Datos/`, repetir el comando sin `--salida`.
- Cálculos del sueño: `externos/nasa_svs_5587_tabla/mooninfo_2026.json` (NASA SVS 5587), puntos subsolar y subterrestre hora por hora.

---

## Revisión C7

> Revisor escéptico, 2026-11-12. Se contrastó cada cifra con [[03a_verificacion_ecuador]], [[03b_verificacion_apolo]], [[Mirador del Faro - Luna con datos reales]] y `mooninfo_2026.json`. Sin créditos ni Firecrawl.

**Comprobaciones**

| Punto | Resultado |
|---|---|
| Suma de la tabla 3.1 | 2 + 22 + 25 + 32 + 13 = **94 min** ✔. Subtotales por acto ✔. Las 4 columnas de 3.2 suman 18 + 20,5 + 44,5 + 11 = 94 ✔, y cada fila coincide con 3.1 |
| Mínimo de 1 h | 94 ≥ 60 ✔; ×0,7 = 65,8 ✔. Es estimación de diseño: falta la prueba cronometrada (F2-03) |
| Otras sumas | Espacial 11 + 22 + 32 + 13 = 78 (83,0 %) ✔; lote 1 = 23 ✔, lote 2 = 28 ✔, 51 y 145 ✔; corte vertical 10 + 12 + 1 + 27 = 50 ✔; medias de los jueces ✔ |
| Noche 2 (13-11, 19:30) | Repetida la consulta a Horizons (en una carpeta temporal): **19,0 %, 31,0°, 402 285 km** ✔. Centro del disco a +0,8° a las 21:50 y −1,4° a las 22:00: puesta del borde superior con refracción hacia las **21:57** (cálculo propio, sigue **pv**) |
| Cálculos del sueño | Con `mooninfo_2026.json`: Sol −25,3° en Tranquilidad a las 00:30 UT ✔; Tierra a 66,2° ✔ y entre 59,0° y 73,2° en noviembre ✔; amanecer el 15-11 hacia las 02:00 UT, 49,5 h después ✔; fase lunar SVS 12,6 % ✔ |
| Enlaces `[[...]]` | Los 14 destinos existen, incluido `Catalogo de recursos#Reparto · v1` ✔. Biblia §3 (excepción de NASA) y §7 (noche) ✔ |
| Pedido de Guillermo | Cubierto: ≥ 1 h, 83 % espacial, sueño al acostarse, caminar, muestras, ver el Apolo (3.4), banderas juntas (3.5) y los escenarios 1 → 2 → 3 unidos por nodos |
| Reglas | Sin insignias ni logotipos; NASA solo como meta y como fuente; banderas con F2-07 ✔ |

**Cambios aplicados**

1. «22 escenas» → **20** (prólogo y 19) en «En cifras» y en §12: la tabla 3.1 tiene 20 filas.
2. §2.2: «Ecuador ya está en la Luna» → «ya llegó», con la marca **pv** de §8.3 (que el disco siga allí no está verificado).
3. 2.1: las antenas de 12 m se instalaron entre 1960 y 1963 (03a, #4), no en 1957.
4. 3.6: «junto al USS Hornet» → «a unas 13 millas náuticas» (03b, L13).
5. S10: «la Tierra que no se pone» marcada como deducción (03b, matices).
6. S8 y §4.3: el gnomon fuera del Apolo 11 marcado **pv**; fila nueva en §8.3.

**Problemas abiertos (decide Guillermo)**

1. **Escala de la Luna:** §4.3 dice mapa 1:4, pero el anillo de 75 m se rodea en unos 240 m (escala 1:1) y la Loma está «a unos 150 m». Falta decir qué va a escala y qué no.
2. **Hueco en el arco:** en 1.2 se ajusta la ganancia y en la noche 1 la toma la arruina solo el apagón. Para que el arreglo de 4.1 tenga causa, el atraso u oscilación del seguidor v1 debe verse en 2.2–2.3.
3. **Título «Ecuador ya dejó un mensaje»** (2.4 y M5): «dejó» sugiere que el disco sigue en la Luna (pv). Propuesta: «Ecuador ya mandó un mensaje».
4. **Fauna:** F2-13 dice «6 especies por hito»; §7.3 nombra 5 en total (iguanas, periquitos, garzas, cangrejos y gato callejero). Falta la sexta y aclarar el reparto.
5. **Hora del sueño:** se calculó a las 19:30, pero ella se duerme después de las 21:30. A las 22:00 el Sol estaría unos 24° bajo el horizonte; no cambia el diseño.
6. **Premisa 2.1:** «Ventana Lunar… la acerca a su sueño de trabajar en la NASA» puede leerse como vínculo con la NASA. Conviene redactarla sin relación causal.
7. **Evidencia de la noche 2:** la consulta a Horizons sigue fuera de la bóveda. Repetir el comando de §14 sin `--salida` para guardarla en `Propuestas/Datos/`.
8. **Corte vertical:** los 50 min no suman el tramo del sendero que incluye (unos 1,5 min).
