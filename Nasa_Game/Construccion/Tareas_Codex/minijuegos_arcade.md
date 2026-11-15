# Brief común

Trabajas en el «Proyecto NASA-Ecuador», un RPG educativo espacial en Godot 4.7.2 (carpeta `juego/`). La raíz del repositorio es tu carpeta de trabajo. Hay otros agentes trabajando a la vez en otras carpetas.

Lee completos antes de escribir: `juego/ARQUITECTURA.md` (secciones 2, 6 y 7), `juego/nucleo/minijuego.gd`, `juego/interfaz/anfitrion.gd`, `juego/interfaz/estilo.gd` y la carpeta actual de tu minijuego. Como ejemplo de lo que se pide, mira un minijuego ya rehecho: `juego/minijuegos/seguidor/seguidor.gd` y `juego/minijuegos/regreso/regreso.gd` (campo en píxeles gordos dibujado con `_draw()`).

Guillermo, el director, jugó los minijuegos y dijo: **«están bastante simples, quiero que sean como minijuegos de Atari, con misiones básicas, no puro texto»**, «no quiero nada genérico», «sé original» y «todo debe ser jugable». Tu minijuego hoy es un panel con deslizadores, botones y párrafos. Hay que **REHACERLO** como un juego de acción de salón recreativo de principios de los 80. Se toman principios; nunca sprites, nombres ni pantallas de juegos existentes.

## Qué es un minijuego arcade aquí

- Un campo de juego dibujado por código con `_draw()`, en píxeles gordos: resolución lógica de 280 × 130 escalada ×4 al lienzo de 1120 × 520, sin suavizado; fondo oscuro y la paleta de `estilo.gd` (crema, naranja, coral, dorado, petróleo y cian para lo interactivo). Sprites hechos con mapas de caracteres; nada de imágenes externas.
- Se controla un objeto en tiempo real con las flechas o WASD, más E o Espacio para la acción. El ratón es opcional. Respuesta inmediata, con inercia donde tenga sentido.
- Una MISIÓN básica que se entiende mirando: un pictograma y una línea corta (máximo 8 palabras) al empezar; nada de párrafos durante el juego. Marcador, 3 vidas o una barra, y tiempo, dibujados dentro del campo con números grandes en píxeles.
- Dura de 60 a 120 segundos. Dificultad 1, 2 y 3: más velocidad, más obstáculos o menos margen. La 1 se gana al primer o segundo intento.
- Con «jugo»: destellos, sacudida breve de pantalla, partículas de píxeles, parpadeo al perder una vida, y sonidos con `sonar("nombre")` (ok, error, tic, salto, recoger, radio, logro; un nombre que no exista no hace nada).
- El dato real se aprende JUGANDO (la mecánica lo demuestra) y con una sola línea al terminar; la ficha la muestra el anfitrión. Las cifras reales salen de `juego/datos/datos_espaciales.json`, sin inventar.
- Contrato intacto: mismo id y carpeta; `extends "res://nucleo/minijuego.gd"`; `_preparar`, `_empezar`, `_paso(delta)` con delta (nunca la hora del sistema); `terminar(superado, puntos, "causa en una frase")`, nunca con la palabra «incorrecto»; `jugar_solo(acierta)` juega con las reglas reales moviendo el mismo estado que las teclas; se siguen aceptando `parametros` (dificultad y los propios del minijuego). `minijuego.json` actualizado: título, resumen, instrucciones (2 o 3 muy cortas), controles, 3 pistas, ficha, escena y orden como estaban.
- `prueba_manos.gd` en la carpeta (`extends Node`; `func correr(pruebas: Node) -> void`): pone `Juego.modo_prueba = false` y `Juego.sin_guardar = true`, abre el minijuego con `Interfaz.abrir_minijuego` en una corrutina aparte, pulsa «Empezar» con Intro y lo GANA solo con teclas simuladas (`Input.parse_input_event` con `InputEventKey`), mirando el estado como lo haría una persona; cierra con Intro; comprueba con `pruebas.comprobar(...)` que se superó, que el anfitrión se cerró y que el árbol no queda en pausa; al final deja `Juego.modo_prueba = true`. Ejemplo de teclas simuladas: funciones `_tecla`, `_toque` y `_manos` de `juego/pruebas/pruebas.gd`. Si ya existe una `prueba_manos.gd` de la versión vieja, reescríbela para el juego nuevo.

## Reglas fijas

- Toca **solo** `juego/minijuegos/<id>/` y tu evidencia en `Nasa_Game/Construccion/Minijuegos/<id>/`.
- No instales ni descargues nada. Sin búsqueda web. Sin créditos de Higgsfield.
- GDScript sin `class_name`, con tabuladores, comentarios sin tildes y tipos explícitos al leer diccionarios o JSON.
- Godot solo con `python -I herramientas/juego_ejecutar.py` (candado global: espera su turno; hay otros agentes y el director puede tener el juego abierto, no cierres procesos ajenos).
- Los minijuegos de la base lunar y de Marte de la biblioteca son de otro equipo: no existen en tu carpeta y no se tocan.

## Pruebas obligatorias, sin fallos

```
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:<id> --ritmo=8
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/<id>/prueba_manos.gd --ritmo=1
```

Y tres capturas con ventana en momentos distintos de la partida, guardadas en tu carpeta de evidencia como `arcade_1.png`, `arcade_2.png` y `arcade_3.png`:

```
python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=<id> --auto --captura=<png> --espera=<s>
```

## Informe

Breve: la mecánica en dos líneas, controles, cómo se gana y cómo se pierde en cada dificultad (con los números), el resultado de las dos pruebas (pega el resumen), las rutas de las capturas y lo que quedó pendiente o sin verificar.

@@TAREA id=arcade_satelite salida=Nasa_Game/Construccion/Tareas_Codex/informes/arcade_satelite.md sandbox=workspace-write timeout=50 esfuerzo=high

Tu minijuego: id `satelite`, carpeta `juego/minijuegos/satelite/`. SATÉLITE («Un cubo de 10 cm»): las piezas de un CubeSat (panel, radio, antena, computadora y batería) caen por una cinta; se mueve el bastidor del cubo con izquierda y derecha y se gira con E para encajar cada pieza en su cara; la chatarra hay que esquivarla. Misión: armar el satélite completo antes de que acabe el tiempo y encender la señal (fichas `pegaso` y `cubesat`).

@@TAREA id=arcade_telescopio salida=Nasa_Game/Construccion/Tareas_Codex/informes/arcade_telescopio.md sandbox=workspace-write timeout=50 esfuerzo=high

Tu minijuego: id `telescopio`, carpeta `juego/minijuegos/telescopio/`. TELESCOPIO («La Luna sonriente»): un campo de estrellas grande por el que se mueve el visor del telescopio con las flechas, con un buscador pequeño en una esquina. Misión: encontrar la Luna (baja, al oeste, sonrisa fina), centrarla y clavar el enfoque con E en el momento justo; después, tres dianas sobre ella: el terminador, la luz cenicienta y el Mare Crisium. Puedes dibujar la Luna en píxeles; los datos son los de las fichas `luna_12_noviembre`, `luna_sonriente` y `luz_cenicienta` (12,2 % iluminada, a 20,0 grados de altura).

@@TAREA id=arcade_linea_tiempo salida=Nasa_Game/Construccion/Tareas_Codex/informes/arcade_linea_tiempo.md sandbox=workspace-write timeout=50 esfuerzo=high

Tu minijuego: id `linea_tiempo`, carpeta `juego/minijuegos/linea_tiempo/`. LÍNEA DE TIEMPO («La escalinata del tiempo»): una escalinata de mosaico vista de lado o desde arriba; la protagonista salta de escalón en escalón y debe pisar las placas en orden, de la más antigua a la más reciente, mientras ruedan cocos o cruzan iguanas. Cada placa muestra un pictograma y su año solo aparece al pisarla bien. Misión: subir los hitos en orden (los hitos y fechas salen de las fichas: 1873, 1957, 1969, 1975, 1981, 1982, 2007, 2013 y 2023; usa los que tengan ficha). La estación de Quito nunca se relaciona con el Apolo 11.

@@TAREA id=arcade_muestras salida=Nasa_Game/Construccion/Tareas_Codex/informes/arcade_muestras.md sandbox=workspace-write timeout=50 esfuerzo=high

Tu minijuego: id `muestras`, carpeta `juego/minijuegos/muestras/`. MUESTRAS («Recolector lunar»): vista superior de un campo lunar; la astronauta se mueve a saltos lentos (1/6 g, con inercia) y cambia de herramienta con E entre cucharón (polvo), pinzas (roca) y tubo (capas). Misión: recoger 4 muestras con la herramienta que toca y llevarlas a la caja antes de que se acabe el oxígeno; con la herramienta equivocada la muestra se escapa y se ve por qué. `parametros.muestra` (0 a 3) sigue valiendo: juega solo esa.

@@TAREA id=arcade_orbita salida=Nasa_Game/Construccion/Tareas_Codex/informes/arcade_orbita.md sandbox=workspace-write timeout=50 esfuerzo=high

Tu minijuego: id `orbita`, carpeta `juego/minijuegos/orbita/`. ÓRBITA («Ni se cae ni se escapa»): el satélite gira alrededor de la Tierra con gravedad real en 2D; con E o arriba se enciende el motor hacia delante y con abajo se frena. Misión: pasar por los anillos de control y dejar la órbita circular a la altura de Pegaso (ficha `pegaso`: 627 × 654 km) sin rozar la atmósfera ni escaparse, con combustible limitado.

CAMBIO PARA ESTE MINIJUEGO (manda sobre el brief común): hazlo directamente a PANTALLA COMPLETA. El director rechazó los bordes. Añade `func _init() -> void: pantalla_completa = true` (mira `juego/nucleo/minijuego.gd`): el lienzo mide 1280 × 720, es decir 320 × 180 píxeles gordos ×4, y el campo llega a los cuatro bordes; marcador, barra y tiempo van dentro del campo, a 4 píxeles lógicos o más del borde. Con pantalla completa el anfitrión no muestra título ni controles durante la partida. Ejemplos ya hechos así: `juego/minijuegos/seguidor/seguidor.gd` y `juego/minijuegos/antena/antena.gd`.
