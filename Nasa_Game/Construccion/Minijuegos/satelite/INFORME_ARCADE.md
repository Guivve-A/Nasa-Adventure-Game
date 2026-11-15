El bastidor se mueve bajo una cinta vertical: E gira entre cinco conectores, y cada pieza solo encaja en su cara; la chatarra se esquiva.
Tras montar panel, batería, computadora, radio y antena, los paneles se despliegan y hay que centrar el cubo bajo el receptor y mantener E durante 3 segundos.

Controles: izquierda/derecha o A/D mueven; E o Espacio giran y, al final, mantienen la radio; abajo/S acelera la cinta x2,5. Ratón opcional: mover y clic. Intro empieza y cierra el resultado; Esc sale.

| Dificultad | Límite | Chatarra cada | Margen de encaje/enlace |
| --- | --- | --- | --- |
| 1 | 110 s | 3,6 s | +/-12 px lógicos |
| 2 | 95 s | 2,6 s | +/-10 px lógicos |
| 3 | 80 s | 1,9 s | +/-8 px lógicos |

En todas: cinco piezas y 3 s de enlace para ganar; tres golpes o agotar el límite sin completar la misión hacen perder. La chatarra golpea a +/-12 px del bastidor; una pieza en otra cara golpea dentro del margen del nivel. Hay 1,5 s de protección después de cada golpe. Una pieza perdida recircula sin quitar vida. Las piezas caen a 7 px/s y la chatarra a 8,75 px/s; S multiplica tanto la velocidad como la alimentación por 2,5. Estas cifras son reglas arcade, no prestaciones de un satélite real.

Duración normal comprobada sin cinta rapida: 61,867 s / 62,250 s / 62,667 s (niveles 1/2/3). El piloto usa la misma palanca rapida que S y termina en menos de 40 s con las reglas reales. Solo escribe los mandos; nunca instala piezas ni modifica posiciones.

Datos: Juego.ficha("cubesat") proporciona el texto y las dimensiones del JSON (10 cm de cuerpo y dos paneles de 27 cm). Se dibujan esas proporciones al desplegarse y se muestra una sola línea factual al terminar. Se conserva ficha=pegaso, escena=1.5, orden=3; también se anota cubesat al ganar. Maqueta de funciones: no es un plano de Pegaso.

Pruebas finales:

- Contrato: `python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:satelite --ritmo=8` (también repetida con --todo para guardar el resumen): `PRUEBAS hechas=13 fallos=0`; `[godot: ok; 13 s; lineas=28; errores=0]`. Registro: arcade_contrato.log.
- Manos: `python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/satelite/prueba_manos.gd --ritmo=1`: `PRUEBAS hechas=25 fallos=0`; `[godot: ok; 92 s; lineas=42; errores=0]`. Registro: arcade_manos.log. Abre en una corrutina, empieza con Intro, gana con InputEventKey en las tres dificultades sin piloto, cierra con Intro y comprueba anfitrion cerrado/arbol sin pausa. Deja Juego.modo_prueba=true.
- Adicional: `--prueba=guion:res://minijuegos/satelite/prueba_satelite.gd --ritmo=8`: `PRUEBAS hechas=21 fallos=0`; `[godot: ok; 7 s; lineas=38; errores=0]`. Comprueba delta 0,016/0,37, duración normal, dimensiones del JSON, recirculación y perdida por inacción. Registro: arcade_modelo.log.

Capturas con ventana, generadas con el envoltorio y revisadas visualmente a 1280 x 720:

- arcade_1.png: espera 6 s; primera pieza cayendo hacia su conector.
- arcade_2.png: espera 15 s; dos subsistemas instalados y computadora a punto de encajar.
- arcade_3.png: espera 28 s; cinco subsistemas, paneles desplegados y señal activa.

Ruta comun: Nasa_Game/Construccion/Minijuegos/satelite/. Todo el dibujo se genera en _draw(), rejilla 280 x 130 ampliada x4; sprites y letras con mapas de caracteres, paleta Estilo, sin imagenes externas, descargas ni creditos. Destellos, sacudida, partículas y parpadeo de protección; llamadas sonar a radio, tic, salto, recoger, error, ok y logro.

Pendiente/sin verificar: ratón opcional y mando físico no se probaron automáticamente; tampoco se hizo escucha humana del audio. No hay PRUEBA_FALLO ni errores de guion. El entorno restringido emite errores al abrir user://logs y leer certificados; además aparecen avisos de recursos/ObjectDB al salir; se conservan en los registros y el envoltorio devuelve errores=0. No se tocaron el nucleo ni las carpetas de otros minijuegos.

Los informes y capturas anteriores de montaje/balance pertenecen a la versión sustituida; INFORME_ARCADE.md y arcade_* son la evidencia vigente.
