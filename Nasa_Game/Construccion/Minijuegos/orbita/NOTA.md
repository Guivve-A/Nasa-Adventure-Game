# Orbita: entrega del carril

Implementado «Ni se cae ni se escapa». Solo se escribieron archivos en las dos carpetas autorizadas.

Archivos del minijuego: `orbita.gd`, `minijuego.json` y `prueba_modelo.gd`. Evidencia: esta nota, `prueba_minijuego.txt`, `prueba_modelo.txt`, `captura.txt` y `lienzo.png`. Gráficos originales por dibujo procedural, sin descargas ni recursos externos. Se usan los colores y las fuentes de `estilo.gd`.

## Datos y modelo

- La ficha `pegaso_orbita` y su fila en `FUENTES.md` verifican 627 × 654 km. Se toma 627 km para niveles 1 y 2; 654 km para nivel 3. Se indica «modelo circular idealizado»: no se atribuye una órbita circular al Pegaso real. La ficha de recompensa es `pegaso`, escena `secundaria`, orden 8.
- Constantes exigidas por el encargo: μ = 398 600 km³/s² y R = 6 371 km. Gravedad central 2D: a = −μ r / |r|³. Sin arrastre, perturbaciones ni propulsión durante el vuelo.
- Integración velocity Verlet con paso físico fijo de 2 s, acumulado desde `delta`; aceleración temporal ×300. El tiempo nunca depende del reloj del sistema. El trazo toma una muestra cada 8 s físicos.
- Comprobación independiente con Python: a 627 km, r = 6 998 km y √(398600/6998) = **7,547127346 km/s**. A 654 km, r = 7 025 km y v = **7,532610007 km/s**. Se muestran 7,547 y 7,533 km/s como «Cálculo propio». Periodos circulares: 5 826,022109 s y 5 859,771944 s; a ×300 son 19,420074 y 19,532573 s de juego.
- Victoria: giro acumulado ≥ 2π y altura máxima − mínima **estrictamente menor** que 150 / 80 / 40 km según nivel. Son alturas observadas desde el lanzamiento, incluida la posición inicial. Puntuación: 100 al superar, 0 al fallar.
- Deslizador: 5,000–11,500 km/s; resolución 0,001 km/s. Teclado/mando: 0,6 km/s por segundo. Ratón y teclado activan el mismo lanzamiento; se bloquea la velocidad durante el vuelo.
- Caída: altura ≤ 120 km. Este corte es una regla didáctica explícita del simulador, no un espesor atmosférico verificado; se explica que no se modela arrastre. Escape: energía específica ≥ 0 y distancia al centro ≥ 2 veces el radio inicial. Elipse: una vuelta con diferencia de alturas excesiva, o vuelo sin cerrar tras 9 600 s físicos (32 s de juego). Límite total de sesión: 180 s, incluido el ajuste previo.
- Al reintentar, el hueco persistente del anfitrión conserva el último trazo y las lecturas de ese nivel en metadatos; no se modifica el anfitrión ni se guarda en disco. Trazo anterior tenue y discontinuo, actual continuo; ambos usan la misma escala adaptativa.
- `jugar_solo(true)` mueve el deslizador a la velocidad calculada y lanza; `false` lo mueve a 5,500 km/s y lanza. Ambos recorren la integración y las condiciones reales, sin forzar resultados.

## Verificación ejecutada

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=minijuego:orbita --ritmo=8 --todo
PRUEBAS hechas=13 fallos=0
FIN
[godot: ok; 8 s; lineas=29; errores=0]
```

Se puso también `--todo` antes de `--` porque es donde el envoltorio reconoce la opción de salida completa. No hubo `PRUEBA_FALLO` ni `SCRIPT ERROR`. Últimos tiempos del piloto: nivel 1, 20,528 s; nivel 3, 20,148 s; caída, 4,637 s. Diferencias de altura al ganar: 0,475 km y 1,469 km, respectivamente.

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/orbita/prueba_modelo.gd --ritmo=8
PRUEBAS hechas=14 fallos=0
FIN
[godot: ok; 2 s; lineas=35; errores=0]
```

El ensayo auxiliar comprueba los 3 niveles, elipse a 8 km/s (1 vuelta), escape a 11 km/s, elipse larga a 9 km/s, caída a 5,5 km/s, igualdad de alturas con cuadros de 0,017 y 0,13 s, conservación del intento previo y entradas reales de teclado/ratón. El ratón se comprueba enviando eventos al viewport, no solo cambiando variables.

Captura con el envoltorio, ventana real Mobile/Vulkan e Intel HD 620: `CAPTURA_OK`, salida 0. `lienzo.png` se abrió y revisó visualmente: sin recortes en textos ni solapamientos entre barra y leyenda. Se corrigió el dibujo de la Tierra y la separación inferior tras la primera revisión.

## Incidencias y límites

Las corridas imprimen errores del entorno al abrir `user://logs/godot.log` y leer el almacén de certificados. No bloquearon las pruebas; sus salidas completas se conservan. Solo el ensayo auxiliar imprime un aviso de 4 instancias ObjectDB al cerrar; la prueba obligatoria y la captura no lo imprimen. No se modificaron rutas de usuario ni el núcleo para silenciarlos.

Pendiente: no se midieron fps sostenidos ni se hizo una sesión humana completa de 1–3 min. Sí se verificaron la lógica, las entradas de ambos dispositivos y la imagen en el equipo objetivo. La raíz no contiene repositorio Git, por lo que no se pudo generar un diff con `git status`.
