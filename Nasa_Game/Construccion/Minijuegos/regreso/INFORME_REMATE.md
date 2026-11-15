# Reentrada: remate arcade

Se conserva el juego de accion existente y su contrato. Cambios limitados a `juego/minijuegos/regreso/` y esta carpeta de evidencia.

- Pantalla completa de 1280 x 720, con 320 x 180 pixeles logicos x4. Cielo, franja y mar cubren el ancho; el altimetro flota sobre el cielo sin panel lateral. Capsula centrada en x=160, altura de vuelo y horizonte ampliados, mas estrellas y vetas, pictogramas repartidos en la introduccion.
- Marcador, calor, tres paracaidas y reloj dentro del campo, a 4 pixeles logicos o mas del borde. Mision persistente con pictograma y una linea de hasta seis palabras. E aparece en la franja.
- JSON actualizado: giro, picada, paracaidas y amerizaje; conserva titulo, ficha, escena y orden.
- Nueva `prueba_manos.gd`: abre por Interfaz en una corrutina, inicia con Intro, decide observando estado y envia unicamente InputEventKey fisicos mediante Input.parse_input_event. No llama al piloto ni escribe estado del minijuego. Cierra con Intro y comprueba victoria, anfitrion cerrado y arbol sin pausa.

## Como ganar en dificultad 1

Pulsos de A/D o flechas inclinan la capsula y la desplazan. Frenar con el lado opuesto por la inercia. Mantener el escudo dentro de +/-26 grados; esquivar bolsas de radio 11. El calor pierde 7 puntos/s con el escudo alineado y sin picada; se pierde a 100. S/abajo permite picada opcional (85 frente a 34 pixeles/s).

Al llegar a la franja, pulsar E o Espacio. La ventana mide 46 pixeles y se atraviesa a 27 pixeles/s: 1,70 s disponibles. Con tres telas la velocidad final es 15 pixeles/s y quedan 140 pixeles hasta el mar, mas de 8 s para dirigir hacia las boyas. Se acepta +/-26 pixeles alrededor del centro, con empuje de mando 70 y viento maximo 12. Son reglas del juego; no cifras fisicas reales.

La partida de teclado, sin picada, gano en 58,90 s: 1438 puntos, 8 bolsas esquivadas, 0 golpes, calor maximo 18/100; x=162,19, diana=161,19 (error 1,00 frente al margen 26). No fue necesario rebajar dificultad ni modificar las reglas de control.

## Pruebas ejecutadas

`python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:regreso --ritmo=8`

Victoria en dificultades 1 y 3; derrota explicada por calor. 13 comprobaciones correctas, cero fallos. Ejecucion final: `[godot: ok; 18 s; lineas=26; errores=0]`. Log: `arcade_contrato.log`.

`python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/regreso/prueba_manos.gd --ritmo=1`

```
REGRESO_MANOS calor_max=18.00 golpes=0 esquivadas=8 x=162.19 diana=161.19 tiempo=58.90
PRUEBA_OK regreso.manos.superado
PRUEBA_OK regreso.manos.anfitrion_cerrado
PRUEBA_OK regreso.manos.arbol_sin_pausa
PRUEBAS hechas=6 fallos=0
FIN
[godot: ok; 62 s; lineas=18; errores=0]
```

El entorno emitio avisos de permisos para user://logs y del almacen de certificados al iniciar; no hubo errores de guion ni fallos de comprobacion. Log completo: `arcade_manos.log`.

## Capturas con ventana

Las tres capturas estan guardadas e inspeccionadas visualmente, a 1280 x 720, con campo sin marco:

- `Nasa_Game/Construccion/Minijuegos/regreso/arcade_1.png`: espera 6 s, inicio de reentrada y primera bolsa de calor.
- `Nasa_Game/Construccion/Minijuegos/regreso/arcade_2.png`: espera 20 s, maniobra entre bolsas y puntuacion por esquivar.
- `Nasa_Game/Construccion/Minijuegos/regreso/arcade_3.png`: espera 33 s, llegada a la franja con pictogramas de E y paracaidas.

Comando utilizado para cada una: `python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=regreso --auto --captura=<ruta_absoluta_png> --espera=<6|20|33>`.

Resumen final de capturas: `[godot: ok; 14 s; lineas=11; errores=0]`, `[godot: ok; 23 s; lineas=11; errores=0]`, `[godot: ok; 37 s; lineas=11; errores=0]`. Logs: `arcade_captura_1.log`, `arcade_captura_2.log`, `arcade_captura_3.log`.

## Pendiente

Ningun entregable solicitado pendiente. La verificacion con teclado es automatizada; no se presenta como evaluacion subjetiva de una persona.

Incidencias resueltas: una edicion concurrente de `interfaz/ventana_carga.gd:303` rompio temporalmente la compilacion; el propietario de ese archivo la corrigio y la prueba automatica final volvio a pasar. El primer intento de captura con ruta relativa no guardo PNG; se repitio con rutas absolutas. No se modificaron archivos ajenos.
