# Antena — escena 2.1

Implementado el minijuego «Rastrear como en el Cotopaxi». Solo se escribieron archivos de `juego/minijuegos/antena/` y esta carpeta. No hubo archivos previos de antena que continuar. No se instalaron ni descargaron recursos.

## Archivos

- `juego/minijuegos/antena/antena.gd`: modelo, interfaz, teclado/ratón y piloto real.
- `juego/minijuegos/antena/minijuego.json`: metadatos, 3 instrucciones, 3 pistas, ficha `ganancia`, escena `2.1`, orden 2.
- `juego/minijuegos/antena/prueba_modelo.gd`: comprobaciones del modelo, historial, teclado y piloto.
- Evidencia: `prueba_minijuego.log`, `prueba_modelo.log`, `captura.log`, `vista.png`, `comparacion.png` y esta nota.

## Modelo y reglas

Parámetros **didácticos**, no mediciones ni reconstrucción del equipo histórico. Las únicas cifras históricas que muestra el lienzo vienen literalmente de `estacion_cotopaxi`: 3 650 m, operación de 1957 a 1981 y entrega en 1982. El concepto de ganancia procede de `ganancia` y `FUENTES.md`. No se vincula la estación con el Apolo 11 ni se muestran emblemas.

- Paso fijo de integración: 1/120 s, acumulado exclusivamente con `delta`. Orden proporcional `u = K × (objetivo − antena)`, limitada a ±95°/s; retardo puro de 30 pasos (0,25 s) y respuesta de velocidad de primer orden con constante de 0,12 s.
- GANANCIA: 0,4–12,0, pasos de 0,1. Inicial: 1,2. El teclado mueve 6 unidades/s y acumula fracciones para no depender de la frecuencia de cuadros. Se congela durante cada prueba.
- Objetivo angular: `−60 + 120 × [p − 0,1 sin(2πp)/(2π)]` grados, con `p = t / duración`. Antena inicial: −72°, velocidad inicial 0. El arco dibujado sigue este mismo ángulo.
- Duraciones de dificultad 1/2/3: 10 / 8,5 / 7 s. D1 sin viento. D2 y D3 tienen dos ráfagas opuestas, centradas en el 32 % y 65 % del paso; cada una dura 0,64 s con perfil coseno al cuadrado. Picos: 8 y 14°/s, respectivamente, sumados como perturbación de la velocidad.
- Señal normalizada: `100 × exp[−(error / 14°)²]`. Se acumula tiempo únicamente con señal **>70 %**. Victoria si ese tiempo alcanza **≥80 %** del paso: 8 / 6,8 / 5,6 s. La banda sombreada de la gráfica corresponde aproximadamente a ±8,36°; misma escala ±40° y duración en ambas gráficas.
- Hasta 3 pruebas completas; al fallar una se puede modificar K y comparar con la anterior. El anfitrión recibe el resultado al superar o agotar las 3 pruebas. Límite de sesión: 180 s. El historial persiste al reabrir/reintentar dentro del mismo anfitrión y dificultad.
- El piloto ajusta el mismo deslizador y llama al mismo botón. Usa K=3,0 para acertar y K=12,0 para fallar; no fuerza el resultado. El camino de fallo completa las 3 pruebas. La duración máxima nominal del piloto es unos 32 s en D1, inferior a 40 s; la prueba adicional midió D2: 8,93 s al acertar y 27,93 s al fallar, con cuadros de 0,19 s.

## Validación

Prueba solicitada ejecutada con el envoltorio y su candado global:

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:antena --ritmo=8 --todo
```

También se repitió con `--todo` antes de `--` para guardar toda la salida del envoltorio:

```text
PRUEBAS hechas=13 fallos=0
FIN
[godot: ok; 7 s; lineas=31; errores=0]
```

K=3,0: D1 94,000 %, D2 92,549 %, D3 83,810 % de tiempo útil. K=12,0: D1 26,083 %, D2 25,490 %, D3 24,881 %, con 14/11/9 cruces del error por cero. K=0,4 y 1,2: 0 % útil en las tres dificultades. El fallo explica que las correcciones grandes llegan tarde, el haz se pasa y oscila.

Prueba adicional:

```text
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/antena/prueba_modelo.gd --ritmo=8
PRUEBAS hechas=33 fallos=0
[godot: ok; 2 s; lineas=73; errores=0]
```

Comprueba ganancias bajas/media/alta en las 3 dificultades a 144 cuadros/s, oscilaciones medidas, comparación entre pruebas, historial al reabrir, ajuste de teclado a 144 cuadros/s y piloto completo D2 con `delta=0,19`. Inspección estática: tabuladores, comentarios sin tildes, sin `class_name` y JSON completo.

Capturas ejecutadas de una en una con Intel HD 620 y revisadas visualmente: `vista.png` (ganancia equilibrada) y `comparacion.png` (segunda prueba de ganancia alta y anterior al lado). Se corrigieron el solapamiento de la antena con el contador y la marca del umbral de señal.

## Pendientes

Ninguno de implementación. Falta valoración humana del ritmo y dificultad. El entorno imprime avisos de acceso a `user://logs` y de lectura del almacén de certificados de Windows; ambas pruebas terminan sin `PRUEBA_FALLO` ni `SCRIPT ERROR` y con 0 errores contabilizados por el envoltorio. No se modificaron el núcleo ni la configuración para ocultar esos avisos.
