# Guion del expositor

> Para decir en vivo **sobre** el [[Guion del video demo]]. El video dura 2:30; el expositor habla **1:30** en cinco bloques y calla durante el gancho, los dos respiros, el montaje de minijuegos y el cierre. **204 palabras** (contadas con «low-poly», «LRO» y «JPL» como una palabra cada una), a unas 136 por minuto: ritmo de presentación tranquilo. Cifras y fuentes: [[Inventario para la presentacion]]. Apoyo en el atril: [[Tarjeta del expositor]].

**Cómo usarlo.** Arranca el video y no hables hasta que aparezca el título «Luz cenicienta» y se apague (0:17). Cada bloque empieza en una imagen fácil de reconocer: esa es la señal. `/` = respiro corto; `//` = pausa de un segundo. Lo que está en **negrita** se dice con peso. No leas los rótulos: el texto los completa.

## Guion

**0:00 a 0:17 · Callado.** En pantalla: la torre, la ignición, la huella, la bandera con la Tierra y ella que abre los ojos. Termina en el título.

---

**Bloque 1 · 0:17 a 0:34** · *Pantalla: un televisor viejo; después Guayaquil de noche; después el cuarto del juego.* · 37 palabras

> Más de **quinientos millones** de personas vieron el primer paso en un televisor. /
> Aquí, en Guayaquil, eran las **nueve y cincuenta y seis** de la noche. //
> Nosotros no queremos que solo lo miren. /
> Queremos que lo **diseñen**.

*Señal de entrada:* el televisor 4:3 sobre negro. *La última frase cae cuando ya se ve el juego.*

---

**Bloque 2 · 0:34 a 0:52** · *Pantalla: ella habla con Órbita; la Plaza, el Sendero, el Mirador de noche, la Luna, el mapa.* · 41 palabras

> **Luz cenicienta** es una aventura de exploración espacial. /
> Una estudiante de ingeniería de control y Órbita, su gato científico, recorren su barrio, Las Escalinatas, hasta la Luna de un sueño. /
> Todo es low-poly **pintado a mano**, con mapa y cargas ilustrados.

*Señal de entrada:* el globo de diálogo de Órbita.

---

**0:52 a 0:55 · Callado.** Ella se asoma al telescopio y el ocular se abre a la Luna.

---

**Bloque 3 · 0:55 a 1:10** · *Pantalla: la Luna con texturas reales; el gráfico «Medido 12,15 % · Horizons 12,2 %»; el cuaderno; la rejilla de minijuegos.* · 34 palabras

> Usamos **datos abiertos de la NASA**: /
> nuestra Luna lleva texturas del orbitador LRO y su luz coincide con **JPL Horizons**. /
> Cada ficha del cuaderno cita su fuente. //
> Y cada minijuego enseña **una idea real**.

*Señal de entrada:* la Luna llena la pantalla. *Termina justo cuando la rejilla de minijuegos se abre: ahí entra la música.*

---

**1:10 a 1:22 · Callado.** Montaje de los 9 minijuegos, una palabra por juego. Deja que suene.

---

**Bloque 4 · 1:22 a 1:41** · *Pantalla: la base lunar en píxel-art; el rover; Marte; la lluvia solar con las cuatro barras; el simulador de aterrizaje.* · 44 palabras

> Y el **corazón del reto**: sostener una base espacial. /
> **Jean, Joel y Domenica** crearon la del polo sur lunar y la de Marte. /
> Hay que equilibrar **oxígeno, energía, alimentos y radiación**. //
> En Marte, la señal tarda demasiado: / el aterrizaje se programa y se simula.

*Señal de entrada:* corta la música y aparece el píxel-art. *Al decir los nombres, mira al público, no a la pantalla.*

---

**1:41 a 1:45 · Callado.** El cohete de la base despega.

---

**Bloque 5 · 1:45 a 2:06** · *Pantalla: concepto → hoja → motor; el juego jugándose solo con su registro; el portátil; el Mirador de noche.* · 48 palabras

> Detrás hay **método de estudio**: concepto, hoja de referencia y motor. /
> Más de **veinte mil** líneas de código y pruebas que juegan solas. /
> Corre a más de **cuarenta** cuadros por segundo en un portátil modesto. //
> La próxima ingeniera de una misión lunar puede estar hoy en **Guayaquil**. /
> **Jugando.**

*Señal de entrada:* el tríptico de tres imágenes. *«Jugando» se dice sola, después de un respiro, y el expositor se queda quieto: entra la música del cierre.*

---

**2:06 a 2:30 · Callado.** Cifras, el equipo y el título. Al final: «Gracias».

## Conteo

| Bloque | Tiempo | Dura | Palabras | Palabras por segundo |
|---|---|---:|---:|---:|
| 1 | 0:17–0:34 | 17 s | 37 | 2,18 |
| 2 | 0:34–0:52 | 18 s | 41 | 2,28 |
| 3 | 0:55–1:10 | 15 s | 34 | 2,27 |
| 4 | 1:22–1:41 | 19 s | 44 | 2,32 |
| 5 | 1:45–2:06 | 21 s | 48 | 2,29 |
| **Total** | | **90 s** | **204** | **2,27** |

## De dónde sale cada afirmación

| Frase | Origen |
|---|---|
| Más de quinientos millones vieron el primer paso | `Fase_2_Narrativa/Cinematica_apertura/01_hechos_verificados.md`, punto 8 (NASA y Smithsonian) |
| Las 21:56 en Guayaquil | Mismo archivo, punto 3 (*El Universo*: «9.56 del Ecuador») |
| Estudiante de ingeniería de control y gato científico | `CLAUDE.md`; `juego/datos/misiones.json` |
| Las Escalinatas | Subtítulo de las zonas en el juego (`Construccion/Capturas/vuelta3_seis_escenas.jpg`) |
| Low-poly pintado a mano, mapa y cargas | D-011 y D-015 en `Memory.md`; `juego/interfaz/mapa.gd`; `Fase_1_Arte/Exploracion/Lote_08/` |
| Texturas de LRO y coincidencia con Horizons | `juego/minijuegos/telescopio/texturas/texturas.json`; `trabajos.md` (2026-11-12: 12,15 % frente a 12,2 %) |
| Cada ficha cita su fuente | `juego/datos/datos_espaciales.json` (55 fichas, campo `fuente`) y `FUENTES.md` |
| Cada minijuego enseña una idea real | Campo `ficha` de cada `juego/minijuegos/*/minijuego.json` |
| La base: cuatro barras, Luna y Marte | `Misión Artemis/LEEME.md`; `Marte_Gravedad2DHD/Marte_Gravedad2DHD/Mision_Artemis_Marte/LEEME.md` |
| Aterrizaje programado y simulado | LEEME de Marte, punto 1 |
| Concepto, hoja de referencia y motor | `Fase_1_Arte/Exploracion/Lote_02/`, `Hojas_de_referencia/`, `Construccion/Capturas/sendero_jugable.png` |
| Más de veinte mil líneas | 20 255 líneas en los `.gd` de `juego/` (2026-11-15) |
| Pruebas que juegan solas | `--prueba=recorrido_manos` y `prueba_manos.gd` (`Construccion/BUCLE_ESTILO.md`, filas 4 y 5j) |
| Más de cuarenta cuadros por segundo en un portátil modesto | De 43,6 a 59,3 fps en Intel HD 620 (`BUCLE_ESTILO.md`, fila 3) |

## Versión de emergencia · 45 s

Por si cortan el tiempo. Se dice sin video o sobre el corte de 30 s, si se hace. **103 palabras.**

> Más de quinientos millones de personas vieron el primer paso en un televisor. / Nosotros queremos que lo diseñen. //
> Luz cenicienta es una aventura espacial hecha en Guayaquil: una estudiante de ingeniería y Órbita, su gato científico, exploran su barrio hasta la Luna. /
> Tiene nueve minijuegos arcade con ideas reales, cincuenta y cinco fichas con su fuente y una Luna con datos de LRO y JPL Horizons. /
> Jean, Joel y Domenica crearon las bases de la Luna y de Marte, donde se equilibran oxígeno, energía, alimentos y radiación. /
> Y corre en un portátil modesto. //
> La próxima ingeniera lunar puede estar hoy en Guayaquil. / Jugando.

## Ensayo

1. Dos pasadas leyendo con el video; tres de memoria con el video; una sin video y con cronómetro (90 s ± 3).
2. Si te atrasas en un bloque, suelta la frase marcada con `//` siguiente y salta al próximo bloque en su señal: **el video no espera**.
3. Si el video falla, di la versión de 45 s y ofrece mostrar el juego en el portátil después.
4. Antes de presentar, vuelve a correr las pruebas y confirma las cifras de la tarjeta.
