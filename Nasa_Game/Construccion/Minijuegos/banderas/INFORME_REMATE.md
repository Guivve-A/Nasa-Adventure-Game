# Banderas: remate del arcade

Se conserva el arcade de tres misiones y amanecer. Campo completo de 1280 × 720 (320 × 180 a escala 4), sin marco exterior. El suelo, el cielo, los perfiles, las estrellas, los cráteres, las guías y los recorridos aprovechan el nuevo campo. Los mástiles están en x=100 y x=202, frente a los anteriores 88 y 168: separación de 102 en lugar de 80 píxeles. El recorrido va de x=8 a x=312. Marcador, vidas, reloj y teclas quedan a cuatro píxeles lógicos o más del borde. Se añadió Esc dentro del campo. Las misiones conservan pictogramas y frases de hasta siete palabras.

Se actualizaron resumen, instrucciones, controles y tres pistas de minijuego.json; se conservaron título, ficha, escena y orden. No se cambiaron datos reales ni el contrato. Las dos banderas permanecen en pie y sin daños; la histórica no aparece.

La prueba_manos.gd abre mediante Interfaz, pulsa Intro, juega leyendo el estado visible y enviando exclusivamente InputEventKey con Input.parse_input_event. Usa E en el mástil izquierdo y Espacio en el derecho para verificar ambas teclas anunciadas. Comprueba también campo completo, piloto desactivado, las tres misiones, amanecer, integridad de las banderas, resultado devuelto, cierre y ausencia de pausa. El pictograma de cada misión permanece junto a su línea de texto incluso después del cartel inicial.

## Dificultad 1 con teclas

- A/D o flechas para acercarse: velocidad máxima 48 píxeles lógicos/s, alcance de 7 alrededor del puesto, situado 9 píxeles a la izquierda del mástil. El trayecto entre puestos requiere unos 2,13 s a velocidad máxima, más aceleración y frenado.
- E o Espacio para dar 4 golpes a cada mástil, dentro de ±0,15 del centro del compás. Ventanas de unos 0,24 s y 0,21 s por cruce, respectivamente; enfriamiento entre golpes de 0,28 s.
- Mantener E o Espacio y soltar con la barra entre 35 y 41 píxeles. A velocidad máxima de 22 píxeles/s hay unos 0,27 s para soltar; al acertar se fija a 40.
- W/S o arriba/abajo para juntar las dos líneas. A la izquierda, la altura objetivo es 23 frente a 18 a la derecha, porque las bases difieren en 5 píxeles. Mantener ambas líneas iguales y quietas durante 0,7 s.
- Se conservaron los márgenes de dificultad 1 tras verificar que admiten el recorrido ampliado: victoria con teclado en 25,48 s, 3 vidas, golpes [4,4], barras [40,40], alturas [22,7632;18]. La igualdad se evalúa en la fila dibujada, redondeada a píxel. Límite de 99 s; los carteles y los 3,8 s de amanecer no descuentan tiempo. No fue necesario ampliar ventanas ni reducir la dificultad.

## Pruebas

Contrato: `python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:banderas --ritmo=8`

```text
13 PRUEBA_OK, 0 PRUEBA_FALLO
banderas.d1.termina_solo / banderas.d1.se_puede_superar: OK
banderas.d3.termina_solo / banderas.d3.se_puede_superar: OK
banderas.se_puede_fallar / banderas.el_fallo_explica_la_causa: OK
FIN
[godot: ok; 10 s; lineas=36; errores=0]
```

Teclado: `python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/banderas/prueba_manos.gd --ritmo=1`

```text
PRUEBAS hechas=11 fallos=0
FIN
[godot: ok; 33 s; lineas=23; errores=0]
```

Registro completo del teclado: arcade_manos.log; resumen del contrato: arcade_contrato.log. Godot también imprimió mensajes del entorno sobre user://logs y el almacén de certificados; al salir del contrato informó de dos recursos todavía en uso. No hubo fallos de guion ni de comprobaciones. No se modificó el entorno compartido.

## Capturas

Capturas con ventana y piloto, usando rutas absolutas; verificación visual realizada:

- arcade_1.png: 5 s, hincado al compás.
- arcade_2.png (15 s) y arcade_3.png (23 s): pendientes de repetir por el bloqueo externo descrito abajo.

Después de pasar ambas pruebas, un cambio concurrente en `juego/interfaz/ventana_carga.gd:303` introdujo `var y := l.position.y + l.size.y + 1.0`, que no compila: Cannot infer the type of "y". Impide inicializar Interfaz y las capturas posteriores resultan grises. Se conservaron como diagnostico_carga_2.png y diagnostico_carga_3.png, con sus registros arcade_captura_2.log y arcade_captura_3.log (errores=6). No son capturas válidas del arcade.

Pendiente: el agente responsable de interfaz debe declarar `var y: float = ...`; no se editó porque queda fuera de las carpetas autorizadas. Después hay que repetir las capturas a 15 y 23 s y revisar ambas imágenes. Se avisó al usuario del bloqueo. Las dos pruebas registradas arriba corresponden al arcade final con pictograma persistente y teclas E/Espacio, antes de aparecer el error ajeno.
