# Cinemática de apertura · Propuesta C: «La señal»

> Estado: **propuesta de guion, sin validar. 0 créditos gastados, nada descargado.** Guillermo la compara con [[Propuesta_A]] y [[Propuesta_B]] y elige; después vienen el storyboard y el animatic.
> Ángulo, y solo este: onírico. El hilo es la **señal de televisión**: sale de la Luna, cruza el vacío y el océano, entra por una antena, atraviesa el vidrio de un televisor y termina en los párpados de la niña. La nieve del televisor se vuelve polvo lunar y después estrellas.
> Base: [[01_hechos_verificados]] (datos y derechos), [[02_lenguaje_visual]] (óptica, luz, color, sonido), [[03_produccion_higgsfield]] (modelos y precios), [[Fase 2 - Analisis]] (historia, borrador sin aprobar) y `juego/datos/misiones.json` (misión 1, primer paso: «Habla con Órbita»).
> Marcas: **(ficción)** inventado y declarado · **(cálculo)** deducción propia, a repetir antes del fotograma final · **(sv)** sin verificar: no va en pantalla.

## 1. Título, logline y tema

- **Título:** «La señal» (subtítulo de trabajo: *nieve, polvo, estrellas*).
- **Logline:** una imagen de televisión sale de la Luna en julio de 1969 con un hombre que baja una escalera, cruza 388 000 km de vacío y todo el Pacífico, y 57 años después, dentro de un sueño, encuentra una antena en un techo de Guayaquil y los párpados de una estudiante que despierta llorando de alegría.
- **Tema:** al terminar, el jugador siente que aquello también se lo enviaron a él: que la imagen sigue viajando, que acaba de llegarle, y que ahora le toca contestar.

**Dos motivos, y ninguno más**

| Motivo | Qué es | Sus formas, en orden |
|---|---|---|
| **El grano** | Lo que se ve | Nieve del tubo → escarcha del cohete → polvo lunar → estrellas → luces de Guayaquil → motas de polvo en el rayo de sol → el brillo de una lágrima |
| **La señal** | Lo que nos lleva | Desde 1:05 la cámara **es** la señal: no la vemos, viajamos en ella |

| Cifra | Valor |
|---|---|
| Duración | **118 s** (1:58); recortable a 109 s (§7) |
| Planos | **17**, de 5 a 9 s; media de 6,9 s |
| Palabras en pantalla | **36** de 40 (40 con el aviso de IA): 3 rótulos y 3 subtítulos |
| Rostros | **1**: el de ella, en 2 planos seguidos, al final |
| Música | Primera nota en 1:06 |
| Video generado | 95 s en 13 planos; 2 fijas animadas; 1 plano de shader puro; 1 del motor |

## 2. Quién es «la niña»

**Decisión: la protagonista de hoy (PER-01),** dormida en su cuarto de Las Escalinatas la madrugada del día 1 del juego. No hay niña de 1969 ni recuerdo de infancia.

Por qué, desde este ángulo:
1. **La señal necesita llegar tarde.** El argumento entero es una imagen que sale en 1969 y encuentra a alguien que entonces no había nacido. Los 57 años son el viaje; una testigo de la época lo anula.
2. **Un solo cuerpo.** El último plano es el modelo que el jugador mueve 5 s después. Basta el ancla `@ANC_PROTA_1`; no hace falta la hoja nueva de una niña (unos 4,50 créditos).
3. **«Niña»** es como la ve quien la quiere. Dormida, con la cara a medio metro de una pantalla y los rizos sobre los brazos, lo es.

**Cómo se sostiene con verdad en 2026: todo es sueño, también el televisor.**

| Lo que se ve | Sostén | Estado |
|---|---|---|
| Un televisor de tubo con nieve, y en la nieve, 1969 | Es el sueño de alguien que conoce esas imágenes: el registro de la misión es público. Nunca se presenta como directo ni como grabación que alguien puso | Coherente con 01 §4 |
| Al despertar, **donde estaba el televisor hay una caja de cartón** | La caja está en el concepto validado ([[L05_A_manana_calida_final.png]]) al pie de la cama. En el borrador de la Fase 2 es la caja de Rafael, que la noche siguiente será su cápsula lunar. Aquí fue su televisor: de esa caja están hechos sus sueños | **(ficción)**, sobre canon sin aprobar |
| La señal llega a un techo de Guayaquil | Ruta real: Luna → antena en Australia → cable, microondas y satélite → Houston → cadenas. No consta que Ecuador la recibiera en directo; su primera estación terrena es de 1972. El desvío a Guayaquil ocurre **después** del rótulo «57 años después» | Hechos confirmados (01 §3 y §4); el desvío es licencia de sueño declarada |
| Nadie mira nada en la Guayaquil de 1969 | No se muestra | — |
| La vocación | No nace esa noche: en el cuarto ya hay telescopio y seguidor. El sueño le recuerda de qué tamaño es lo que quiere | Coherente con [[Fase 2 - Analisis]] §2 |

Consecuencia práctica: esta propuesta **no añade ningún objeto** a la Habitación. La variante con televisor real está en §8.

## 3. Guion en tres movimientos (118 s)

Los movimientos llevan el nombre de los tres estados del grano. Texturas según [[02_lenguaje_visual]] §2, con una regla propia: **1969 es película; 2026 es pintura.** El cambio ocurre sobre el océano, al cruzar la línea del anochecer.

Tres silencios: 0:34 (el vacío), 0:46 (la Luna quieta) y 1:43 (antes de que abra los ojos).

**Un solo ruido.** Todo el sonido que no es voz ni música sale del mismo ruido blanco, filtrado: siseo de nieve → rugido del cohete → estática de radio → oleaje → su respiración. Es el grano, pero para el oído. Se sintetiza en casa: 0 créditos y sin licencias.

### Movimiento I · «Nieve» — subir (0:00–0:37)

**C01 · 0:00–0:07 · Nieve**
- **IMAGEN:** negro, 1,5 s. Una raya blanca horizontal se abre de golpe y todo el cuadro es nieve: grano gris que hierve, líneas de barrido, las esquinas apenas curvadas. No hay mueble ni cuarto: estamos pegados al vidrio y no sabemos de quién es. Cámara fija. Hacia el segundo 5, la nieve casi arma algo: una vertical clara, que se deshace.
- **SONIDO:** *clac*. Un silbido agudo que sube y se queda (15,7 kHz, muy bajo). Siseo.
- **TEXTO:** ninguno.

**C02 · 0:07–0:15 · Sintonía**
- **IMAGEN:** la imagen rueda dos veces hacia arriba y engancha. Blanco y negro, 4:3, negros lavados: un cohete blanco de tres etapas en su torre. Del fuselaje se desprenden placas de escarcha que caen entre el grano; no se distingue cuál es hielo y cuál es nieve de la pantalla. Empuje del 2 % por segundo.
- **SONIDO:** bajo el siseo, por un parlante pequeño, la cuenta de la sala de lanzamiento (archivo): «…12, 11, 10, 9…».
- **TEXTO (0:09–0:12):** «16 de julio de 1969».

**C03 · 0:15–0:21 · Entrar**
- **IMAGEN:** el empuje no se detiene. Las líneas de barrido se separan hasta ser grano de 16 mm; el 4:3 se abre a 16:9; el gris toma ámbar.
- **SONIDO:** la cuenta se queda atrás. El siseo empieza a bajar de tono, sin cortarse: va camino de ser otra cosa.
- **TEXTO:** ninguno.

**C04 · 0:21–0:29 · Fuego y escarcha**
- **IMAGEN:** teleobjetivo largo, aplanado: torre, cohete y bruma apilados. Sol duro de media mañana. La llama brota bajo la base y tiñe el vapor de crema `#F8C991`. El hielo cae ahora en una nevada lenta alrededor de 110,6 m de metal blanco. El cohete tarda en moverse; cuando sube, sube despacio. El cuadro tiembla un 1 %.
- **SONIDO:** el siseo ya es rugido: el mismo ruido, tres octavas abajo, al tope de la mezcla. Es el único pico de toda la película.
- **TEXTO:** ninguno.

**C05 · 0:29–0:37 · El punto**
- **IMAGEN:** gran angular de 24 mm, fijo, cielo en nueve décimas del cuadro. La columna de humo abajo; arriba, el cohete es una chispa. El azul baja a índigo y a negro. La chispa se pierde entre el grano de la película. Tres segundos de negro con ese grano fino… que deja de hervir y empieza a moverse en una sola dirección: hacia fuera, en líneas rectas.
- **SONIDO:** el rugido se adelgaza. **0:34: corte a nada.** Primer silencio.
- **TEXTO:** ninguno.

### Movimiento II · «Polvo» — llegar (0:37–1:05)

**C06 · 0:37–0:46 · Polvo**
- **IMAGEN:** el grano era polvo. Vista cenital: suelo gris que pasa hacia atrás, cráteres con media sombra negra, y sobre él polvo disparado en rayos rectos, a ras, sin nube y sin remolino. Entra una sombra de cuatro patas, crece, se afila, se detiene. El polvo se va de cuadro y no vuelve.
- **SONIDO:** estática de radio (el mismo ruido, estrecho), un temblor grave, tonos de comunicación. «Contact light.» El temblor cesa.
- **TEXTO (0:43–0:45):** subtítulo «Luz de contacto.»

**C07 · 0:46–0:52 · Quieto**
- **IMAGEN:** a ras de suelo, 21 mm. Horizonte cercano y curvo, cielo negro, Sol rasante desde la derecha, sombras de decenas de metros. **Por primera vez no hay grano:** ni nieve, ni película, ni polvo. La imagen más limpia de la cinemática. Nada se mueve en 6 s.
- **SONIDO:** **segundo silencio,** entero. No hay traje ni respiración: el sueño aquí no tiene cuerpo.
- **TEXTO (0:47–0:50):** «Mar de la Tranquilidad».

**C08 · 0:52–0:57 · La cámara**
- **IMAGEN:** macro de 100 mm, al pie del módulo dorado. En una bandeja abatida, una caja metálica del tamaño de un ladrillo, con un objetivo: una cámara de televisión, **montada cabeza abajo**. En su lente, diminuta e invertida, una escalera. Empuje recto hacia el vidrio de la lente.
- **SONIDO:** un zumbido eléctrico leve que arranca. Un tono de radio.
- **TEXTO:** ninguno.

**C09 · 0:57–1:05 · Lo que vio el mundo**
- **IMAGEN:** atravesamos la lente y vemos lo que ella ve. Blanco y negro quemado, 10 cuadros por segundo, 320 líneas: y **patas arriba**. El cielo negro abajo, el suelo arriba, una escalera que cuelga del techo del cuadro. A 0:59 la imagen gira 180° de un golpe y el mundo queda derecho. Por la escalera baja una figura blanca, translúcida: se le ve el brillo de la pata del módulo a través del cuerpo, y cada movimiento deja estela. Se detiene en el último peldaño. Baja un pie.
- **SONIDO:** por el parlante pequeño, Houston: «And we're getting a picture on the TV.» (0:58). Silencio de radio. Y delgada, a 1:02: «That's one small step for man…».
- **TEXTO (0:58–1:01):** subtítulo «Y estamos recibiendo imagen en la tele.»
- **TEXTO (1:02–1:05):** subtítulo «Es un pequeño paso para un hombre;»

### Movimiento III · «Estrellas» — bajar (1:05–1:58)

Desde aquí la cámara es la señal. El cuadro lleva, al 6 %, las esquinas curvas y las líneas de barrido (shader): seguimos dentro de la imagen hasta que cruza el vidrio.

**C10 · 1:05–1:12 · Salir**
- **IMAGEN:** color otra vez, limpio. Lo que la cámara de televisión miraba ya desde su trípode, a 18 m: el módulo dorado y, a su lado, la bandera de Estados Unidos, entera, quieta en su barra horizontal, la tela con la onda que le quedó porque la barra no se extendió del todo. Dos segundos. Entonces la cámara se va hacia arriba y hacia atrás, cada vez más rápido: el llano, el borde curvo, la Luna completa. Y en el negro aparece el grano que faltaba: estrellas, nítidas, miles.
- **SONIDO:** **primera nota** (1:06): una cuerda grave, sostenida, que nace del zumbido de la cámara. Encima, una nota de piano.
- **TEXTO:** ninguno.

**C11 · 1:12–1:19 · La Tierra**
- **IMAGEN:** el disco de la Luna que se aleja se disuelve en otro disco, que crece: la Tierra. Gibosa, iluminada en dos tercios, y casi toda agua. La cara que miraba a la Luna en ese instante era el Pacífico: azul, nubes en espiral, un trozo ocre abajo a la izquierda, y a la derecha la noche. Es el único azul saturado desde que empezó la película. Acercamiento lento hasta que llena el cuadro.
- **SONIDO:** la segunda mitad de la frase, que viene con nosotros: «…one giant leap for mankind.» Segunda nota de piano.
- **TEXTO (1:13–1:17):** subtítulo «un salto gigante para la humanidad.»

**C12 · 1:19–1:24 · El plato**
- **IMAGEN:** vuelve el grano cálido de 16 mm: abajo es 1969. Mediodía de invierno, pasto pajizo. Un plato blanco de 26 m, inclinado hacia nosotros, que caemos dentro. En su base, dos personas de espaldas con la mano de visera, que no le llegan al 5 % del alto. El círculo del plato llena el cuadro.
- **SONIDO:** viento. Un graznido. La nota sostenida no se va.
- **TEXTO:** ninguno.

**C13 · 1:24–1:31 · El océano**
- **IMAGEN:** el círculo blanco se disuelve en el reflejo del Sol sobre el agua. Vuelo bajo y recto hacia el este, 18 mm. Mediodía: el mar es grano de luz. El día se acaba por delante: naranja, violeta, la línea del anochecer. Al cruzarla, **el grano de la película se limpia y el agua empieza a estar pintada**: facetas, pinceladas, azul petróleo `#516B7C`. Arriba vuelven las estrellas. Al fondo, una hilera de luces: una costa.
- **SONIDO:** el ruido es oleaje. Tercera y cuarta nota.
- **TEXTO:** ninguno.

**C14 · 1:31–1:38 · El techo**
- **IMAGEN:** las luces suben por un cerro como si las estrellas se hubieran posado: un río ancho, escalinatas, techos de zinc, ya en el low-poly pintado del juego, de noche. No hay Luna en el cielo. La cámara planea sobre los techos y baja hasta uno: una antena de espina de pescado, un cable plano que cae por la pared entre buganvillas hasta una ventana de arco con celosías. Dentro, una luz azulada que tiembla.
- **SONIDO:** grillos, un perro lejos, la bocina de un barco. Vuelve, muy bajo, el silbido de 15,7 kHz.
- **TEXTO (1:32–1:35):** «Guayaquil · 57 años después».

**C15 · 1:38–1:44 · El vidrio**
- **IMAGEN:** estamos dentro del tubo, detrás de la nieve: los granos pasan enormes y blandos, fuera de foco. Al otro lado del vidrio curvo, a medio metro, ella: dormida al revés en la cama, con la cabeza a los pies y la mejilla sobre los brazos cruzados, vestida. Somos su única luz. Por el borde de arriba cuelga y se mece la punta de una cola de gato. Empuje del 2 % por segundo, hasta que los granos quedan atrás: cruzamos el vidrio.
- **SONIDO:** el siseo, oído desde dentro, sordo. Su respiración: un ciclo cada 4 s. Un ronroneo.
- **TEXTO:** ninguno.

**C16 · 1:44–1:53 · Los párpados** (ver §4)

**C17 · 1:53–1:58 · La mañana (motor)** (ver §4)

### Texto en pantalla: 36 palabras de 40

| # | Texto | Palabras | Original y fuente |
|---|---|---:|---|
| R1 | «16 de julio de 1969» | 5 | Despegue a las 13:32:00 UTC, 08:32 en Guayaquil. NASA SP-4029 (01 §1) |
| S1 | «Luz de contacto.» | 3 | «Contact Light.», Aldrin, 102:45:40 de misión. ALSJ, «The Landing» (01 §2) |
| R2 | «Mar de la Tranquilidad» | 4 | Sitio: Tranquility Base (01 §1) |
| S2 | «Y estamos recibiendo imagen en la tele.» | 7 | «And we're getting a picture on the TV.», enlace de Houston (CAPCOM), 109:22:06. ALSJ, «One Small Step». **Comprobado hoy** en la página del ALSJ; releerla antes de fijar el subtítulo |
| S3 | «Es un pequeño paso para un hombre; un salto gigante para la humanidad.» | 13 | «That's one small step for (a) man; one giant leap for mankind.», Armstrong, 109:24:23. ALSJ. Redacción discutida: se subtitula como él quiso decirlo y el inglés no se imprime (01 §2) |
| R3 | «Guayaquil · 57 años después» | 4 | Del 21-07-1969 al 12-11-2026 (fecha del día 1 en F2-02, sin aprobar; vale hasta el 20-07-2027) |
| R0 | «Imágenes recreadas con IA» (opcional, sobre el negro inicial) | +4 | Recomendación de la guía de NASA (01 §5). Con él: **40** |

**Licencias de sueño, declaradas**
- La señal tardó **1,3 s** en llegar a la Tierra **(cálculo)**; aquí, 33 s (de 1:05 a 1:38).
- Entre la primera imagen (109:22:06) y el pie en el suelo (109:24:15) pasaron 2 min 9 s; aquí, 6 s. La imagen se enderezó justo después de 109:22:34, no a los 2 s.
- La bandera quedó en pie a las 110:09:43, unos 45 min después del primer paso. Aquí se ve entre las dos mitades de la frase, que en realidad van seguidas. Si en el animatic la frase partida molesta, va entera sobre C11.
- La escarcha que cae del cohete es un hecho conocido que 01 no recoge **(sv)**: se confirma en el Apollo Flight Journal antes del fotograma; si no, C02 y C04 llevan solo vapor.
- La señal real acabó en Houston y en las cadenas. La antena de Guayaquil es del sueño.

## 4. El plano final y la entrada al juego

Referencias: ![[L02_protagonista_tipo1_hoja.png]] ![[L05_A_manana_calida_final.png]]

**C16 · 1:44–1:53 · Los párpados.** Macro de 100 mm, foco en las pestañas del ojo cercano. Cámara fija: lo único que se mueve es la luz.

| Segundo | Qué pasa |
|---|---|
| 1:44–1:46 | La nieve le tiembla en los párpados, blanca azulada: el último grano. Debajo, los ojos se mueven: sigue algo. En la línea de las pestañas hay ya una gota, con un punto de luz fría dentro. |
| 1:46–1:49 | Una franja ámbar `#F4A159`, la primera luz que entra por las celosías, le sube por la mejilla. Donde toca, el azul se apaga. El siseo se adelgaza y calla: **tercer silencio** (1:47). |
| 1:49 | La franja llega al párpado. Abre los ojos. El punto de luz de la gota es ahora dorado. |
| 1:49–1:51 | No se mueve. Mira sin enfocar, como quien cuida que no se le derrame lo que traía. Resuelve el acorde. |
| 1:51–1:53 | Sonríe: la mejilla sube y suelta la lágrima, que cruza de lado el puente de la nariz. Toma aire en media risa. Pájaros. Pestañea. |

Es alegría y no pena por tres cosas: la lágrima cae **porque** sonríe, cae con luz de mañana, y lo siguiente que hace es levantarse.

**C17 · 1:53–1:58 · La mañana (motor)**
- **IMAGEN:** corte en el pestañeo a la cámara alta 3/4 del juego, el encuadre del concepto aprobado, en render en vivo. Ella está al pie de la cama. Se incorpora de un impulso. **Donde estaba el televisor hay una caja de cartón** con su cinta en cruz, y sobre la caja Órbita, en la misma postura, con la cola colgando por el mismo borde. Levanta la cabeza y la mira. En los rayos de sol que entran por la ventana flotan motas de polvo: la nieve, por última vez. En el banco, la onda cian del osciloscopio da un respingo.
- **SONIDO:** la mañana de Las Escalinatas (pájaros, un bus, el ventilador), que empezó 1 s antes del corte. La cuerda sostenida se apaga bajo ella. Un maullido corto.
- **TEXTO:** el del juego: «Habla con Órbita».

**Cómo se cose**
1. **Corte en el pestañeo:** 2 o 3 cuadros de párpado cerrado tapan la costura. No se pide al modelo una grúa del ojo al plano general.
2. **C16 ya viene pintado.** Desde C13 el mundo de 2026 es low-poly pintado; C16 usa `@ANC_PROTA_1` y, como último fotograma, una captura del motor con la luz real de la ventana (`#F8C991`, `#F4A159`, sombras `#516B7C`).
3. **Fundido de estilo de 1 s:** el desenfoque del macro sigue en el primer cuadro del motor y baja a cero.
4. **La caja y el gato hacen la explicación** que nadie dice: mismo sitio, misma pose, otro objeto. Órbita es además el primer objetivo de la misión 1.
5. **El cian** es el color de lo interactivo en el juego. La onda del osciloscopio es la primera señal que le toca a ella, y está mal ajustada: es el tercer paso de la misión 1 («Ajusta el seguidor»).
6. **Meta del gesto:** que al tomar el control ella quede de pie en la alfombra con los brazos arriba, la pose exacta del concepto validado. Necesita una animación nueva: tarea de `juego/`, con su puerta. Mínimo aceptable: sentada en la cama.
7. Mantener Esc 1 s salta a C17.

**La promesa jugable:** la cinemática es un viaje de arriba abajo que el jugador no controla. El juego es el viaje de vuelta, de abajo arriba, y lo camina él.

## 5. El homenaje y el lugar de Ecuador

**A Estados Unidos: por haberlo mostrado**
- Esta propuesta honra algo que casi nunca se cuenta: no solo fueron, **lo dejaron ver mientras pasaba**. La imagen salió sin retardo de seguridad (confirmado: el retardo de 6 s empezó con los Apolo 16 y 17) y la vieron más de 500 millones de personas (cifra de NASA). Emitieron en directo algo que podía salir mal.
- La frase más famosa llega partida por 388 000 km **(cálculo, JPL Horizons, centro a centro)**, y la segunda mitad, «para la humanidad», suena sobre la Tierra entera. No hace falta añadir nada.
- **La bandera** aparece una vez (C10), entera, quieta, a la altura de los ojos, 2 s sin música encima, tal como estuvo: con la tela ondulada por su barra. No se usa de transición ni lleva cámara lenta.
- **Lo que no hay:** himno, fanfarria, metales, discurso, presidente, emblemas, voz en off, superlativos.

**A quienes lo hicieron posible: los que cargaron la imagen**
- La cámara que alguien montó cabeza abajo en la bandeja del módulo (ALSJ) y que por eso mostró el mundo al revés unos segundos.
- La voz de Houston que avisa: «estamos recibiendo imagen». Sin nombre en pantalla.
- El plato de 26 m en un campo de Australia: en el primer paso el mundo veía la señal de esa estación, porque era la mejor (confirmado, 01 §3). Dos personas de espaldas, pequeñas.
- La figura que baja la escalera se ve como la vio el mundo: un fantasma translúcido a 10 cuadros por segundo. Es exacto y es respetuoso: ningún rostro, ningún nombre.

**Ecuador es adonde llega la mirada**
- En el disco de la Tierra de C11, Guayaquil cae en **el borde oscuro de la derecha**: la Luna estaba a 16° sobre su horizonte y era de noche (01 §1) **(cálculo)**. La cinemática va exactamente hacia allí.
- No se afirma que Ecuador recibiera la señal en 1969. El rótulo «57 años después» entra antes de la antena.
- La estación de Quito (Cotopaxi) no aparece ni se alude.
- **Simetría que el juego recoge después:** en 1969 Ecuador mandó palabras hacia arriba (el mensaje de Velasco Ibarra en el disco de 73 países, ficha `disco_apolo11` de la misión 3) y de arriba bajó una imagen. La cinemática muestra solo la bajada; la subida se la queda el juego.
- Para el cuaderno, no para la pantalla **(cálculo)**: la parte de la señal que no dio en la Tierra sigue viajando y en noviembre de 2026 está a 57,3 años luz.

## 6. Planos previstos (17)

Modelos y precios de [[03_produccion_higgsfield]]; no se cotizó nada nuevo. «H3» = MiniMax H3; «SD2.5» = Seedance 2.5 a 720p con escalado; «Mini» = Seedance 2.0 Mini.

| # | Plano | Cómo se produce | s generados |
|---|---|---|---:|
| C01 | Nieve a cuadro completo | Shader del motor: 0 créditos y 0 MB | 0 |
| C02 | Cohete en la torre, blanco y negro, 4:3, con escarcha | Mini, degradado en posproducción | 8 |
| C03 | Empuje: barrido → grano, 4:3 → 16:9 | H3 con primer fotograma (C02) y último (C04) | 6 |
| C04 | Ignición con nevada de hielo, teleobjetivo | **SD2.5** (plano héroe de fuego) | 8 |
| C05 | La chispa en el cielo que se vuelve negro | H3; los 3 s de negro y el grano que se ordena, en shader | 6 |
| C06 | Polvo en rayos rectos y sombra de cuatro patas, cenital | H3 | 10 |
| C07 | El llano sin grano, a ras de suelo | H3, casi fijo | 6 |
| C08 | La cámara de televisión cabeza abajo, macro | Fija con empuje (ffmpeg); el reflejo de la lente, compuesto | 0 |
| C09 | El fantasma en la escalera: invertido, gira, baja un pie | Mini; giro de 180°, 10 cuadros por segundo y estela en ffmpeg | 8 |
| C10 | Bandera y módulo a 18 m; la cámara sube; la Luna entera y estrellas | H3 para la subida; la Luna, con las texturas de LRO que ya están en `externos/`; estrellas en shader | 6 |
| C11 | La Tierra gibosa, cara del Pacífico | Fija con acercamiento (ffmpeg) | 0 |
| C12 | Plato de 26 m, mediodía de invierno, dos espaldas | H3 | 5 |
| C13 | Pacífico: del mediodía a la noche; de película a pintura | H3 con primer y último fotograma | 8 |
| C14 | Guayaquil pintada de noche; baja a la antena y a la ventana | H3, con `@ANC_EXPLORACION` | 8 |
| C15 | Ella dormida, vista desde dentro del tubo; la cola de Órbita | H3 con `@ANC_PROTA_1` y `@ANC_GATO`; la nieve delante, en shader | 6 |
| C16 | Párpados: del azul del tubo al ámbar; abre los ojos; la lágrima | **SD2.5** con primer y último fotograma (o el ganador de la prueba A/B) | 10 |
| C17 | Cámara del juego: la caja, Órbita, las motas, la onda cian | Motor | 0 |
| | **Total** | 13 clips, 16 fotogramas | **95** |

**Estimación, con las tarifas de 03 y 1,5 intentos por pieza: unos 530 créditos** (61 % del saldo de 868,75 que registra 03; quedarían unos 339).

| Partida | Cálculo | Créditos |
|---|---|---:|
| Animatic: 16 fotogramas de borrador | 16 × 1,5 × 0,25 | 6,00 |
| Fotogramas de ella (C15, C16 inicial y final) | 3 × 1,5 × 4,5 | 20,25 |
| Resto de fotogramas | 13 × 1,5 × 2,75 | 53,63 |
| Prueba A/B en C16 | como en 03 | 32,00 |
| Video: Mini 16 s, H3 61 s, SD2.5 18 s | (16 + 122 + 126) × 1,5 | 396,00 |
| Escalado a 1080p de 11 clips | tope de 11 × 2 **(sv)** | 22,00 |
| **Total** | | **529,88** |

Queda dentro del plan de referencia de 03 (532,00). La cifra firme sale de `generate cost` con el storyboard aprobado.

## 7. Riesgos de producción

| Riesgo | Cómo se evita |
|---|---|
| **No se entiende que viajamos en la señal** | Tres apoyos: el raster al 6 % sobre todo el movimiento III, la frase que sigue sonando durante el viaje, y la nota sostenida que nace del zumbido de la cámara. Animatic con 3 a 5 personas y una pregunta: «¿qué era lo que viajaba?». Si menos de la mitad acierta, C10 arranca con la imagen de C09 encogiéndose a un punto que sale de la Luna |
| **No se lee que el televisor era la caja** | Mismo sitio en el cuadro, misma pose de Órbita, misma cola por el mismo borde. Se prueba en el animatic. Plan B: la variante con televisor real (§8) |
| **Destellos al inicio** (nieve a pantalla completa) | Nieve de bajo contraste (del 5 al 15 %, como fija 02), sin parpadeo de campo entero por encima de 3 por segundo. Opción «Reducir destellos» en accesibilidad, que deja la nieve casi quieta |
| **Peso del archivo** | Nieve, grano, raster y estrellas van en shader; nunca horneados. 03 midió que el grano multiplica el archivo por 7. C01 no pesa nada |
| **La Tierra y la Luna inventadas por el modelo** | La Luna sale de datos (texturas de LRO ya descargadas). La cara del Pacífico es casi toda agua y nubes: poco que inventar. Antes del fotograma se repiten con `herramientas/luna_efemerides.py`: punto de la Tierra bajo la Luna (hoy: unos 6° S y 154° O, unos 3 000 km al sur de Hawái), fase (64 %) y línea del anochecer (hacia 134° O) |
| **Letras, insignias, parches** | Todo se pide por forma: «cohete blanco de tres etapas», «módulo dorado de cuatro patas», «plato blanco», «caja metálica con lente». El cohete solo aparece lejos o degradado; la figura, translúcida y a 320 líneas. Revisión ampliada de cada fotograma |
| **Bandera mal dibujada** | Ocupa menos del 4 % del cuadro y está quieta. Se compone a mano sobre el fotograma (50 estrellas y 13 franjas: dato general, se confirma antes) |
| **Gravedad lunar y escalera** | La figura casi no se mueve: un peldaño y un pie. El blanco y negro, los 10 cuadros por segundo y la estela tapan lo demás |
| **C13: del día a la noche y de película a pintura en un plano** | Primer y último fotograma aprobados. Plan B: tres fijas (mediodía, anochecer, noche) con el horizonte clavado y disolución larga; el cambio de estilo, con un fundido entre dos versiones del mismo cuadro |
| **Guayaquil reconocible** | El barrio es ficticio: sin monumentos, rótulos ni marcas. Techos, escalinatas, río y luces |
| **Su cara** | Solo 2 planos. En C15 hay nieve y vidrio por delante; C16 es un ojo, pestañas y rizos, no un retrato. Se generan en una tanda y se aprueban como set, pintados y no fotorrealistas |
| **La lágrima** | Va en los dos fotogramas y recorre 2 cm. Plan B: se genera sin lágrima y el brillo se compone con máscara |
| **Voces de 1969** | Son de personas identificables: consulta legal antes de publicar y permiso de Guillermo por cada descarga (nombre, fuente y tamaño). Nunca se imitan ni se sintetizan. **Plan B sin voces:** tonos hechos por nosotros y las frases como rótulo; el guion se sostiene igual |
| **Música** | Propia: una cuerda sostenida y 5 notas de piano. Lo generado, solo como maqueta |
| **Se aparta de 02 en tres cosas** | (1) No abre en la habitación: abre dentro de la nieve. (2) El clímax no es la huella: es la llegada a los párpados. (3) El paso se ve como lo vio el mundo, no en macro. Si Guillermo quiere la huella, entra en C10 antes de la bandera (+5 s) |
| **Duración al límite (118 s)** | Primeros recortes: sale C12 (−5 s), C07 baja a 4 s (−2 s) y C05 a 6 s (−2 s): quedan 16 planos y 109 s |
| **Datos pendientes** | Hora local del plato (mediodía si el huso es UTC+10) **(sv)**; que en la madrugada del 12-11-2026 no haya Luna sobre Guayaquil **(cálculo)**; la escarcha del despegue **(sv)**; que la señal saliera por la antena del módulo y no por una desplegable (el ALSJ lo sugiere; no se muestra) |
| **Canon sin aprobar** | La caja de Rafael y la fecha del día 1 dependen de la Fase 2. Si cambian, cambian un rótulo y una línea |

## 8. Preguntas para Guillermo

1. ¿El televisor es **del sueño** (al despertar es la caja de cartón) o lo quieres como **objeto real** del cuarto? Lo segundo crea un recurso nuevo con su hoja y su puerta, y en C17 Órbita queda sobre el televisor apagado.
2. ¿Versión con las voces de 1969 (permiso de descarga y consulta legal) o sin voces?
3. ¿La frase del primer paso partida en dos (el pie, y la Tierra) o entera sobre la Tierra?
4. ¿El aviso «Imágenes recreadas con IA» va sobre el negro inicial o en los créditos?
5. ¿Quieres la huella en macro además del fantasma del televisor (+5 s)?

## 9. Fuentes

- Hechos, horas, frases, televisión de 1969, Ecuador y derechos: [[01_hechos_verificados]].
- Lenguaje visual, color, sonido y reglas del video generativo: [[02_lenguaje_visual]].
- Modelos, precios y posproducción: [[03_produccion_higgsfield]].
- Historia y reparto (borrador): [[Fase 2 - Analisis]]; verificaciones [[03a_verificacion_ecuador]] y [[03b_verificacion_apolo]].
- Consultas de hoy (2026-11-15, con WebFetch; sin descargas, sin Firecrawl, sin Higgsfield):
  - Apollo Lunar Surface Journal, «One Small Step»: https://apollojournals.org/alsj/a11/a11.step.html. De ahí salen la frase de 109:22:06, la cámara montada cabeza abajo en la bandeja del módulo y el giro de la imagen tras 109:22:34. Alternativa de la misma página: 109:22:48, «Okay. Neil, we can see you (on the TV) coming down the ladder now.»
  - JPL Horizons, Luna vista desde el centro de la Tierra el 21-07-1969 a las 02:56 UT: 0,00259464 ua (388 153 km) y 0,02157897 min de tiempo de luz (1,29 s). https://ssd.jpl.nasa.gov/api/horizons.api
- Cálculos propios a partir de la tabla de 01 §1 (altura 16°, azimut 264° desde Guayaquil): punto de la Tierra bajo la Luna, fase de la Tierra y línea del anochecer. Se repiten con Horizons antes de los fotogramas.
- Imágenes de referencia: [[L05_A_manana_calida_final.png]], [[L02_protagonista_tipo1_hoja.png]] y [[L02_gato_orbita_hoja.png]].
