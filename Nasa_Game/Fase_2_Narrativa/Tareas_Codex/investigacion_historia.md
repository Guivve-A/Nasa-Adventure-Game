@@TAREA

Proyecto: RPG educativo de exploracion en Godot 4 (nombre de trabajo «Proyecto NASA-Ecuador»). Una estudiante de ingenieria de control de Guayaquil, con su gato cientifico Orbita, viaja en su sueno de llegar a la NASA. Estilo: low-poly pintado a mano, exploracion 2D-HD con camara alta. Ya existe una prueba del Mirador del Faro: telescopio que muestra la Luna real del momento con datos de JPL Horizons.

Pedido de Guillermo (2026-11-12) para la Fase 2 (historia y misiones):
- historia de al menos 1 hora de juego, coherente y entretenida, con mas contenido espacial;
- al acostarse, la protagonista suena que esta en la Luna: camina, recolecta muestras y ve el Apolo; una mision es colocar juntas la bandera de Estados Unidos y la de Ecuador;
- escenarios en orden, conectados como mundo abierto: 1) habitacion, 2) telescopio, 3) Luna.

Reglas: responde en espanol, texto corto y con cifras. Cada dato con su fuente primaria (URL de NASA, gobierno de Ecuador, tratado, articulo cientifico) y fecha de consulta; marca «sin verificar» lo que no confirmes en una fuente primaria. Usa la busqueda web integrada; NO uses Firecrawl salvo que una pagina no cargue de otra forma. No inventes. No escribas fuera del archivo de salida.

@@TAREA id=datos_espaciales salida=Nasa_Game/Fase_2_Narrativa/Investigacion/01_datos_espaciales_ecuador.md sandbox=read-only timeout=45 esfuerzo=high

Investiga y verifica datos reales que conecten a Ecuador con el espacio y con la Luna, utiles para misiones y dialogos del gato:
1. Ecuador y el programa Apolo: la estacion de rastreo de la NASA en Quito (nombre, red, anos, que misiones apoyo, si apoyo al Apolo 11); el mensaje de Ecuador en el disco de buena voluntad del Apolo 11; las rocas lunares de buena voluntad (Apolo 11 y 17) regaladas a Ecuador y que paso con ellas.
2. Ecuador hoy: firma de los Acuerdos Artemisa (fecha exacta y numero de pais firmante); la Agencia Espacial Civil Ecuatoriana (EXA), el satelite NEE-01 Pegaso y Ronnie Nader; el Observatorio Astronomico de Quito; el Chimborazo como punto de la superficie mas alejado del centro de la Tierra (cifra); planetarios o centros de ciencia en Guayaquil.
3. Superficie lunar en el Apolo, para el nivel del sueno: herramientas de recoleccion de muestras (pinzas, pala, rastrillo, tubos de nucleo, bolsas), como se documentaba cada muestra, cuantos kg trajo cada mision, la gravedad (1/6), temperaturas, regolito, la Tierra vista desde la Luna; la bandera del Apolo (Lunar Flag Assembly, por que parece ondear); la etapa de descenso que quedo en la Luna; como volvio el modulo de mando a la Tierra (amerizaje).
4. Reglas que el juego debe respetar: Tratado del Espacio Ultraterrestre de 1967 (una bandera no es reclamar territorio); recomendaciones de la NASA de 2011 para proteger los sitios del Apolo (distancias) y la ley One Small Step de 2020; uso de la insignia y el nombre de la NASA en obras comerciales; ley ecuatoriana de simbolos patrios sobre el uso de la bandera en obras y videojuegos.
Entrega: una tabla por bloque (dato | cifra | fuente | confianza) y al final 10 ideas de mision o dialogo que salgan de esos datos, cada una con el dato que la respalda.

@@TAREA id=historia_existente salida=Nasa_Game/Fase_2_Narrativa/Investigacion/02_historia_existente.md sandbox=read-only timeout=45 esfuerzo=medium

Lee y resume lo que ya existe de historia, sin inventar:
- `C:\Users\guill\Desktop\Juego\Juego_2d-hd\3_Guion_y_Mundo\historia.md` y `C:\Users\guill\Desktop\Juego\Juego_2d-hd\2_Arte_e_Interfaz\arte e Historia.md` (boveda anterior);
- la seccion de la Fase 2 (estructura narrativa y diseno de misiones) del PDF `Nasa_Game/00_Plan_Maestro/Plan Maestro de Desarrollo AAA.pdf` (extrae el texto con Python si hace falta);
- `Nasa_Game/Memory.md`, `Nasa_Game/Propuestas/Mirador del Faro - Luna con datos reales.md` y `Nasa_Game/Fase_1_Arte/Biblia de arte.md`.
Entrega:
1. Lo que pide el plan maestro para la Fase 2: entregables, puertas y criterios, citando la pagina.
2. Inventario de lo existente: personajes (con rasgos), lugares, misiones, mecanicas educativas, tono, finales. Marca lo que contradice decisiones nuevas (por ejemplo, el pixel-art descartado).
3. Huecos: lo que falta para una historia de al menos 1 hora con escenarios habitacion, telescopio y Luna conectados como mundo abierto.
