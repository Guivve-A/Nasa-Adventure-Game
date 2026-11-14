# Brief común

Trabajas en el «Proyecto NASA-Ecuador» (nombre interno), un RPG educativo de exploración en Godot 4.7.2 con arte low-poly pintado a mano. La raíz del repositorio es tu carpeta de trabajo. Equipo: portátil i5-7200U, 8 GB, Intel HD 620, Windows 10. Hay otros agentes trabajando a la vez en otras carpetas.

Construyes UN minijuego del juego jugable v0 (carpeta `juego/`). **Antes de escribir nada lee completos:**

1. `juego/ARQUITECTURA.md` (el contrato; obligatorio), sobre todo las secciones 2, 6 y 7.
2. El ejemplo que funciona: `juego/minijuegos/plantilla/plantilla.gd` y `minijuego.json`.
3. El guion base que heredas: `juego/nucleo/minijuego.gd`. Y el anfitrión que lo enmarca: `juego/interfaz/anfitrion.gd`.
4. `juego/interfaz/estilo.gd` (colores y tipografías) y `juego/datos/datos_espaciales.json` con `juego/datos/FUENTES.md` (las fichas reales).
5. La prueba que tendrás que pasar: función `_minijuego` de `juego/pruebas/pruebas.gd`.

Reglas fijas:

- Toca **solo** los archivos de tu minijuego: `juego/minijuegos/<id>/` y tu carpeta de evidencia `Nasa_Game/Construccion/Minijuegos/<id>/`. No edites nada más.
- No instales ni descargues nada. No uses Higgsfield, Firecrawl ni búsqueda web: todo lo que necesitas está en el repositorio.
- GDScript sin `class_name`, con sangría de tabuladores y comentarios sin tildes. Cuidado con `:=` sobre valores de diccionarios, listas o JSON: pon el tipo explícito (`var x: float = d["a"]`).
- Los textos que ve el jugador van en español correcto, con tildes, cortos y con cifras. Nunca la palabra «incorrecto»: al fallar se explica la causa.
- Los datos y las cifras salen de las fichas de `datos_espaciales.json`. No inventes hechos. La estación de Quito (Cotopaxi) nunca se relaciona con el Apolo 11. Nada de insignias, logotipos ni textos de la NASA o de misiones.
- El lienzo mide 1120 × 520 px. Texto de 16 px o más. Paleta de `estilo.gd`; el cian solo para datos e interacción. Se juega entero con teclado (acciones `mover_izquierda`, `mover_derecha`, `mover_arriba`, `mover_abajo`, `interactuar`, `saltar`) y también con ratón.
- Usa siempre `delta` en `_paso(delta)`, nunca la hora del sistema.
- `jugar_solo(acierta)` es obligatorio: con `true` gana **jugando con la lógica real** (moviendo el estado como lo haría una persona), y con `false` falla por un camino real con una explicación causal. Debe terminar en menos de 40 s de juego.
- `minijuego.json` completo: `titulo`, `resumen`, `instrucciones` (2 a 4), `controles`, `pistas` (3 niveles: una mirada de Órbita, una frase y la respuesta), `ficha`, `escena` y `orden`.

Prueba (ejecútala si tu entorno deja lanzar procesos; si no, dilo en el informe y explica cómo revisaste el código):

```
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:<id> --ritmo=8 --todo
```

Debe terminar sin `PRUEBA_FALLO` ni `SCRIPT ERROR`.

Informe final: qué archivos escribiste, las reglas del modelo con sus números (umbrales de victoria y duración), la salida de la prueba y lo que quede pendiente. Deja además una nota breve en tu carpeta de evidencia.

- Ya hay dos minijuegos tuyos aprobados que puedes mirar como ejemplo de calidad: `juego/minijuegos/orbita/` y `juego/minijuegos/linea_tiempo/`.
- Si en tu carpeta hay archivos de un intento anterior interrumpido, revísalos y continúa desde ahí.

@@TAREA id=telescopio salida=Nasa_Game/Construccion/Tareas_Codex/informes/telescopio.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `telescopio`: «La Luna sonriente» (escena 2.2). En el Mirador, la protagonista busca la Luna de esa noche con el telescopio.

- Ya existe una prueba con la Luna **real** (texturas de NASA LRO ya descargadas y fase calculada con JPL Horizons): `pruebas/luna_telescopio/` (`telescopio.gd`, `luna.gdshader`, `datos/luna.json` y `texturas/`). Léela y reutilízala: copia a tu carpeta el shader, el json y las texturas que necesites. Cárgalas en tiempo de ejecución con `preload("res://nucleo/recursos.gd").textura(ruta)` (sirve sin importar). Documento: `Nasa_Game/Propuestas/Mirador del Faro - Luna con datos reales.md`.
- Jugada en tres pasos: (1) BUSCAR: mover el telescopio (acimut y altura) hasta encontrar la Luna, baja en el oeste, con un buscador de campo ancho y la lectura de coordenadas; (2) ENFOCAR: girar la rueda de enfoque hasta que la imagen quede nítida; (3) SEÑALAR con la mira tres rasgos, uno por vez: el terminador, la luz cenicienta (la parte oscura que se alcanza a ver) y el Mare Crisium.
- Datos reales del 12-11-2026 a las 19:30 desde Guayaquil (fichas `luna_12_noviembre`, `luna_sonriente`, `luz_cenicienta`, `terminador`, `mare_crisium`): no cambies ninguna cifra.
- El fallo explica la causa (buscas demasiado alto: esta noche la Luna está a 20 grados; esa zona brillante no es la luz cenicienta, es la parte que ilumina el Sol).
- La Luna es fotográfica a propósito (excepción de la Biblia de arte); el marco y los controles siguen la paleta.
- `minijuego.json`: ficha `luz_cenicienta`, escena `2.2`, orden 4.

@@TAREA id=muestras salida=Nasa_Game/Construccion/Tareas_Codex/informes/muestras.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `muestras`: «La herramienta correcta» (escenas 3.2 y 3.3). En la Luna del sueño hay que recoger y registrar 4 muestras con las herramientas del Apolo 11 (fichas `herramientas_apolo11`, `regolito`, `bolsas_numeradas`, `muestras_apolo11`: léelas y usa solo sus datos).

- Cada muestra tiene dos pasos: (1) ELEGIR la herramienta: cucharón de caja para el suelo fino y los fragmentos pequeños; pinzas pequeñas para una roca suelta; tubo de núcleo de 2 cm con martillo para una columna que conserva las capas (aquí hay que dar los golpes justos con ritmo: uno de menos deja el tubo corto, dos de más rompen el ritmo); (2) REGISTRAR: meterla en la bolsa numerada que corresponde y marcar el lugar en el croquis. Un número equivocado no pierde la muestra: se corrige el registro y se explica por qué importa.
- Si se elige mal la herramienta, se ve por qué falla (las pinzas no retienen el polvo; el cucharón revuelve las capas).
- `parametros.get("muestra", -1)`: con 0 a 3 se juega una sola muestra; con -1 (menú), las cuatro seguidas. Dificultad: menos ayudas y ritmo más fino.
- Dibujo propio de herramientas y terreno, sin insignias.
- `minijuego.json`: ficha `herramientas_apolo11`, escena `3.2`, orden 6.

@@TAREA id=banderas salida=Nasa_Game/Construccion/Tareas_Codex/informes/banderas.md sandbox=workspace-write timeout=55 esfuerzo=high

Minijuego `banderas`: «Dos banderas, un cielo» (escena 3.5 y sección 4.3 de la Fase 2). Pedido expreso del director: colocar **juntas** en la Luna las banderas de Estados Unidos y de Ecuador. Fichas `bandera_lunar`, `tratado_espacio`, `acuerdos_artemisa` y `zona_75_m`: léelas y usa solo sus datos.

- Cinco pasos: (1) ELEGIR EL SITIO en un mapa pequeño: fuera del anillo de 75 m de la etapa de descenso y sin huellas históricas (elegir dentro explica la recomendación, no castiga); (2) ARMAR los dos conjuntos: mástil, barra horizontal y tela; (3) HINCAR cada mástil con ritmo, no con fuerza (barra de compás); (4) EXTENDER la barra del todo: si queda corta, la tela se ve ondulada, porque no hay viento que la sostenga; (5) IGUALAR ALTURAS: las dos a la misma altura y separadas lo justo para que ninguna tape a la otra.
- Reglas de respeto, sin excepción: las banderas no se sueltan, no caen, no se dañan y no hay animación de caída; no son premio ni chiste; la bandera histórica del Apolo 11 no se muestra. Dibújalas con `_draw()`, reconocibles y bien proporcionadas: Estados Unidos con sus franjas y su cantón de estrellas simplificado; Ecuador con el amarillo doble de ancho, el azul, el rojo y el escudo simplificado al centro (para que no se confunda con la de Colombia). Las dos del mismo tamaño.
- Al superarlo, amanece (la luz pasa de azul fría a cálida) y queda la escena 3 s en silencio. El texto final recuerda que una bandera no da territorio (Tratado del Espacio) y que Ecuador firmó los Acuerdos Artemisa: es cooperación.
- `minijuego.json`: ficha `bandera_lunar`, escena `3.5`, orden 7.
