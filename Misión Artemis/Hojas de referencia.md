# Misión Artemis: Más allá de las páginas — hojas de referencia

> Primer paso del encargo: revisar lo que hay y fijar el diseño **antes** de tocar escenas. Fecha: 2026-11-14.
> Estado: **propuesta, sin validar**. Nada de esto está construido en Godot todavía.

## 1. Qué revisé

| Qué | Dónde | Qué encontré |
|---|---|---|
| Escena de Joel | `juego/minijuegos/base_luna/` | Base lunar en **vista superior**, rejilla de 20 × 13, 7 soles por turnos. Pasa sus pruebas (13 de 13 y 178 de 178). |
| Fondos de Jean | `recursos/fondos_luna/` (copiados aquí) | 5 escenas lunares, 6 capas de 640 × 360 cada una, repetibles en horizontal. |
| Personajes de Jean | `recursos/personajes/` (copiados aquí) | Jugador y 5 NPC de 32 × 32, vista lateral, con trajes de Artemis. |
| Tercera bandera | `recursos/banderas/bandera_3_ieee_ias_espol_foto.jpeg` | Bandera de IEEE IAS, rama estudiantil de la ESPOL. |
| Fondos de Marte | — | No están. Los entrega Domenica. |

**Lo que cambia.** La escena de Joel es de vista superior y por turnos. El encargo nuevo pide desplazamiento lateral en tiempo real. No se pueden «unir» tal cual: propongo un nivel lateral nuevo sobre los fondos con parallax, que reutiliza de Joel lo que sí vale.

| De Joel se conserva | De Jean se conserva |
|---|---|
| Los 5 datos reales de la NASA ya verificados con su fuente | Las capas de parallax y su script |
| Los números de consumo como punto de partida del equilibrio | Los 6 personajes y sus animaciones |
| Las ideas de crisis (tormenta solar, sombra del cráter, fuga) | El generador de píxel-art |
| La paleta de interfaz (cian, ámbar, verde, alerta) | |

## 2. Dirección de arte: por qué no se ve genérico

1. **Todo ocurre dentro de un libro.** La pantalla lleva un marco de página color crema y una cinta de capítulo («Capítulo 1 — La Luna»). Los capítulos son Luna, Viaje y Marte.
2. **Lo que falta se imagina.** Las partes del cohete sin construir se ven como un plano de puntos cian. Al entregar recursos, el plano se «rellena».
3. **Mundo frío, base cálida.** La Luna es azul grisácea y oscura. La base es crema con luces propias: ámbar en ventanas, cian en oxígeno, magenta en el invernadero y en la radiación.
4. **Un color por sistema.** Cian es oxígeno, ámbar es energía, verde es alimentos y magenta es radiación, tanto en el HUD como en los props y en las luces.
5. **Polo sur de verdad.** El Sol queda bajo y a la izquierda en todo el nivel, las sombras son largas hacia la derecha, la Tierra queda pegada al horizonte y el cráter del final está en sombra permanente, con hielo.

## 3. Las hojas

### Hoja 1 — Props, personajes, efectos y HUD
![Props](hojas_de_referencia/01_props.png)

### Hoja 2 — Escena: la base en calma
![Base en calma](hojas_de_referencia/02_escena_base_en_calma.png)

### Hoja 3 — Escena: el astillero con lluvia solar y meteoritos
![Astillero](hojas_de_referencia/03_escena_astillero_lluvia_solar.png)

### Hoja 4 — Mapa del nivel
![Mapa](hojas_de_referencia/04_mapa_del_nivel.png)

### Hoja 5 — Paleta, capas de parallax y proporciones
![Paleta](hojas_de_referencia/05_paleta_capas_proporciones.png)

Los props sueltos están en `recursos/props/` (24 PNG). Todo se regenera con `node herramientas/generar_hojas.js`.

## 4. Props

Una casilla mide 16 px y el jugador 32 px de alto. Tamaños en píxeles del arte.

| ID | Prop | Tamaño | Para qué sirve en el juego |
|---|---|---|---|
| P01 | Cúpula hábitat | 128 × 72 | Refugio presurizado: recarga oxígeno y protege de la lluvia solar |
| P02 | Invernadero | 112 × 48 | Da alimentos; también protege |
| P03 | Refugio de regolito | 80 × 36 | La mejor protección contra la radiación |
| P04 | Nave de carga | 72 × 80 | Trae cajas de la Tierra cada cierto tiempo |
| P05 | Antena | 48 × 88 | Avisa con antelación de lluvias solares y de cargas |
| P06 | Panel solar | 56 × 44 | Alimenta las estaciones de carga |
| P07 | Recarga de oxígeno | 32 × 44 | Rellena el oxígeno del traje |
| P08 | Estación de carga | 24 × 44 | Rellena la energía del traje |
| P09 | Depósito de combustible | 56 × 40 | Guarda el combustible del despegue |
| P10 | Rover | 64 × 36 | Vehículo: más rápido y lleva más carga |
| P11, P12 | Suministros y caja | 40 × 30, 16 × 14 | Se recogen y se llevan a la constructora |
| P13 a P15 | Vetas: ilmenita, regolito, hielo | 32 × 20 | Se extraen. El hielo se convierte en combustible |
| P16 | Máquina constructora | 96 × 88 | Recibe los recursos y arma el cohete por fases |
| P17 a P20 | Cohete, fases 1 a 4 | 56 × 160 | Motores, tanque, etapa superior y punta |
| P21 a P23 | Banderas: EE. UU., Ecuador, IEEE IAS | 30 × 52 | Se plantan en Marte. Van rígidas, con varilla |
| F01, F02 | Meteorito y lluvia solar | — | Los dos peligros periódicos |

## 5. Capas de parallax

| Capa | Contenido | Velocidad |
|---|---|---|
| 0 | Espacio y estrellas | × 0,02 |
| 1 | Sol y Tierra | × 0,06 |
| 2 | Montañas lejanas | × 0,18 |
| 3 | Montañas medias | × 0,35 |
| 4 | Colinas cercanas | × 0,60 |
| 5 | Suelo jugable, props y personajes | × 1,00 |
| 6 | Rocas en primer plano (nueva) | × 1,30 |

- Uso la escena `5_polo_sur_sol_eterno`. La escena 4 trae una base pequeña dibujada al fondo, que se repetía a lo largo del nivel.
- **Marte:** las mismas ranuras con otra carpeta (`recursos/fondos_marte/`). Mientras no lleguen los fondos, cada capa es un color liso rotulado «pendiente». Al copiar los PNG con los mismos nombres, se conectan sin tocar código.

## 6. El nivel lunar

2 560 px de mundo (160 casillas), en un solo eje.

| Zona | Casillas | Qué hay | Peligro |
|---|---|---|---|
| Z1 Pista de carga | 0 a 30 | Nave de carga, cajas, la piloto | Meteoritos |
| Z2 Base polo sur | 30 a 80 | Oxígeno, cúpula, carga, invernadero, refugio, paneles, antena. Comandante y médica | Zona segura |
| Z3 Astillero | 80 a 105 | Constructora, cohete, combustible. El ingeniero | Zona segura a medias |
| Z4 Campo minero | 105 a 140 | Rover, vetas de ilmenita y regolito. La geóloga | Radiación media |
| Z5 Cráter en sombra | 140 a 160 | Hielo. Terreno en bajada, oscuro | Radiación alta y sin energía solar |

La base queda en el centro: hay que salir hacia los dos lados y volver.

## 7. Movilidad

| Acción | Tecla | Detalle |
|---|---|---|
| Caminar y correr | ← → o A/D, Mayús | Correr gasta más oxígeno |
| Salto lunar | Espacio | Alto y lento: 3 casillas, con gravedad de 1/6 |
| Impulso de mochila | Espacio en el aire | Un segundo salto corto que gasta energía |
| Cargar | E | Hasta 3 cajas a la espalda; con carga se camina más lento |
| Rover | E junto al rover | El doble de rápido y hasta 8 cajas; no salta escalones altos |
| Entrar a una cúpula | E o ↑ en la puerta | Dentro no baja el oxígeno ni sube la radiación |
| Extraer | Mantener E en una veta | Una barra corta; gasta energía |

## 8. Supervivencia

| Barra | Baja o sube cuando | Se recupera en | Si llega al límite |
|---|---|---|---|
| Oxígeno | Baja fuera de las cúpulas; más al correr | Recarga de oxígeno y cúpulas | Vuelves a la cúpula con parte de la carga perdida |
| Energía | Baja al extraer, usar el impulso y el rover | Estaciones de carga | No puedes extraer ni usar el impulso |
| Alimentos | Baja despacio todo el tiempo | Invernadero y cajas verdes | Caminas más lento |
| Radiación | Sube lejos de la base y en la lluvia solar | Baja sola dentro de un refugio | Igual que el oxígeno |

Nadie muere: el castigo es volver a la cúpula y perder tiempo, para no frustrar.

## 9. Eventos

- **Lluvia solar:** cada 90 a 120 s. La antena avisa 15 s antes. Dura 20 s; fuera de un refugio la radiación sube rápido.
- **Meteoritos:** cada 60 a 90 s caen de 3 a 5. Una sombra en el suelo marca dónde. Al caer dejan una veta nueva: el peligro también da recursos.
- **Carga de la Tierra:** cada 2 minutos baja una nave con cajas a la pista.

## 10. Objetivos

| Fase | Entregas en la constructora | Se arma |
|---|---|---|
| 1 | 4 cajas | Motores |
| 2 | 4 cajas y 4 de ilmenita | Tanque |
| 3 | 4 cajas y 4 de regolito | Etapa superior |
| 4 | 4 de ilmenita y 4 de regolito | Punta |
| Despegue | 4 de hielo (combustible al 100 %) y la batería del cohete llena | Lanzamiento |

- **Viaje:** pantalla de carga con el cohete que va de la Luna a Marte sobre una trayectoria de puntos.
- **Marte (provisional, lo trabaja Domenica):** plantar las 3 banderas y desplegar los módulos de la base.

Las cifras son de diseño y se ajustan al probar. Son un punto de partida, no datos reales.

## 11. Datos reales que usa el diseño

- En el polo sur lunar el Sol queda justo bajo o sobre el horizonte y las montañas dan sombras largas (NASA, 2022, ya verificado por Joel).
- Hay hielo de agua en las sombras de los cráteres polares (NASA/JPL, 2018, ya verificado por Joel).
- La exosfera lunar no protege de la radiación del Sol ni de los meteoroides (NASA Science, ya verificado por Joel).
- Las banderas del Apolo llevaban una varilla horizontal para verse extendidas sin viento. **Sin verificar aquí:** hay que leerlo en la fuente antes de mostrarlo como «Dato real».
- El encargo dice que el polo sur «recibe menor radiación continua». **No lo encontré en las fuentes revisadas.** Lo que sí está verificado es la luz casi constante en las cimas y el hielo en las sombras. Propongo usar eso como razón de la ubicación.

## 12. Lo que no pude hacer y lo que hay que decidir

1. **Mapa 3D mejorado.** El texto pegado empieza en «Parte: Juego 2D»; la parte del mapa 3D no llegó. No hice esa hoja para no inventarla.
2. **Vista lateral contra vista superior.** El plan del equipo fija la vista superior como decisión de Guillermo. Este diseño la cambia a lateral: hay que avisarle.
3. **Tercera bandera.** Lleva los logotipos de IEEE e IAS. En píxel-art queda como bandera blanca con la onda verde; usar los logotipos reales en el juego depende de que su rama tenga permiso.
4. **Tamaño de pantalla.** Las escenas están a 640 × 360 (× 2 = 1280 × 720). Dentro del marco de minijuegos del juego principal el lienzo es de 1 120 × 520: se vería un recorte de 560 × 260.
5. **Arte por código.** Todo esto se generó con un script propio, sin gastar créditos de Higgsfield y sin imágenes de terceros.
