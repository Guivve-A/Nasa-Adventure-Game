# Seguidor: remate arcade

Campo completo de 1280 × 720 (320 × 180 píxeles ×4), sin margen del anfitrión. El recorrido crece de 300 a 340 píxeles y el arco de 64 a 100 píxeles de altura. El barrio ocupa todo el ancho y llega al borde inferior. Marcador y controles quedan dentro del campo; el contenido del marcador empieza a 4 píxeles del borde. La misión conserva su pictograma y una línea de siete palabras.

El JSON describe el motor, el freno y la grabación, conservando título, ficha, escena y orden. La prueba manual antigua se sustituye por dos partidas con teclas físicas: normal y prealimentación. Abre mediante Interfaz, pulsa Intro, maneja A/D y Espacio, activa E cuando corresponde y cierra el resultado con Intro. Comprueba victoria, devolución del resultado, cierre, árbol sin pausa y anotación de prealimentación.

En dificultad 1, la Luna recorre 340 píxeles en 32 s: 10,625 píxeles/s. El semivisor pasa de 17 a 19 píxeles: descontando el radio lunar de 6, el margen es ±13. Eso deja 1,22 s por lado, frente a 1,17 s antes de ampliar el campo. Se gana acumulando 24 s dentro del visor (60 s de vídeo a ritmo ×2,5), con tres vidas, 6 s iniciales de gracia y 96 s hasta el amanecer. Cada corte exige agotar 5 s de señal fuera del visor. Los impulsos aceleran a 80 píxeles/s²; el freno aumenta el roce de 1 a 7 s⁻¹. La prueba decide cada 0,1 s mirando posición y deslizamiento, sin mover objetos ni activar el piloto.

Prueba con teclas (comando solicitado con `--todo`, `--ritmo=1`):

```text
Normal: superado=true, puntos=4527, tiempo=30.1673007777787 s
Prealimentación: superado=true, puntos=4521, tiempo=30.4098075555563 s
PRUEBAS hechas=16 fallos=0
FIN
[godot: ok; 64 s; lineas=30; errores=0]
```

Godot mostró avisos del entorno sobre escritura del log de usuario y lectura del almacén de certificados. No hubo errores de guion ni fallos de prueba.

Prueba automática (`--prueba=minijuego:seguidor --ritmo=8`): 13 líneas `PRUEBA_OK`, ninguna `PRUEBA_FALLO`. Dificultad 1: 4528 puntos; dificultad 3: 3463 puntos. La partida deliberadamente fallida perdió con 17/60 s grabados y explicó el exceso de empuje y la oscilación.

```text
PRUEBA_OK seguidor.d1.termina_solo
PRUEBA_OK seguidor.d1.se_puede_superar
PRUEBA_OK seguidor.d3.termina_solo
PRUEBA_OK seguidor.d3.se_puede_superar
PRUEBA_OK seguidor.se_puede_fallar
PRUEBA_OK seguidor.el_fallo_explica_la_causa
FIN
[godot: ok; 18 s; lineas=30; errores=0]
```

Al salir, esta corrida también mostró el aviso de recursos aún en uso; el envoltorio terminó con código 0 y sin errores de guion.

Tres capturas con ventana, guardadas y revisadas visualmente a 1280 × 720:

- [arcade_1.png](arcade_1.png): `--espera=4`, entrada de la Luna y persecución inicial; 0/60 s grabados.
- [arcade_2.png](arcade_2.png): `--espera=13`, seguimiento y multiplicador ×2; 16/60 s grabados.
- [arcade_3.png](arcade_3.png): `--espera=24`, seguimiento con viento y multiplicador ×4; 43/60 s grabados.

Rutas: `Nasa_Game/Construccion/Minijuegos/seguidor/arcade_1.png`, `arcade_2.png` y `arcade_3.png`. Se usó el comando solicitado con rutas absolutas para guardar desde Godot. Las tres corridas finalizaron con `errores=0`.

Pendiente del alcance solicitado: nada. No se modificaron datos espaciales ni archivos fuera de la carpeta del minijuego y su evidencia.
