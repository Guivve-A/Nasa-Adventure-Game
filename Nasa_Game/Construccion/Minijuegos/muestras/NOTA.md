# muestras · La herramienta correcta

Implementado en `juego/minijuegos/muestras/`: `muestras.gd`, `minijuego.json` y `prueba_muestras.gd`. Solo se escribieron archivos de ese carril y esta carpeta de evidencia. Escena 3.2, orden 6, ficha `herramientas_apolo11`.

Se leyeron el contrato completo, plantilla, base, anfitrión, estilo, datos, fuentes y prueba común. Fuentes de contenido: `herramientas_apolo11`, `regolito`, `bolsas_numeradas`, `muestras_apolo11`. Datos históricos mostrados: tubo de 2 cm; 21,5 kg en 58 muestras. Herramientas, terreno facetado, capas y bolsas son dibujos propios por código, sin recursos externos ni insignias.

Victoria: recoger y registrar 4 muestras, o 1 con `parametros.muestra` entre 0 y 3; `-1` juega las cuatro. Suelo fino y fragmentos pequeños usan cucharón; roca suelta, pinzas; columna, tubo y martillo. Cada registro exige bolsa y lugar coincidentes: A→2, B→4, C→1, D→3. Esas etiquetas y el croquis son didácticos. Confundir número o lugar conserva la muestra y permite corregir sin penalización de puntos. Victoria: 100 puntos; fallo: 0.

Ritmo didáctico explícito, sin atribuirlo a una medición histórica: exactamente 4 golpes válidos, 1 pulso/s, luego Extraer. Ventanas por dificultad: ±0,24 / ±0,17 / ±0,10 s. 3 golpes dejan el tubo corto; 5 invalidan la extracción; 6 (2 de más) rompen el ritmo. Dos golpes fuera de ventana o repetidos en el mismo pulso también fallan. A los 8 s se evalúa la extracción. La dificultad reduce ayudas: herramienta sugerida en 1, categoría en 2 y solo objetivo en 3.

Límite de sesión: 150 s para las cuatro o 90 s para una. Recogida: 0,9 s; confirmación de registro: 1,6 s; demostración causal del fallo: 2,2 s. Todo avanza con delta; integración temporal en pasos de hasta 1/120 s. El piloto elige y confirma mediante la lógica compartida, y golpea al pasar los pulsos; no fuerza resultados. Duraciones medidas: 23,192 s las cuatro; 3,817–10,117 s una muestra. El piloto de fallo termina en menos de 4 s eligiendo una herramienta que no conserva la muestra.

Prueba requerida ejecutada:

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:muestras --ritmo=8 --todo
13 PRUEBA_OK
FIN
[godot: ok; 7 s; lineas=28; errores=0]
```

Prueba adicional, con el mismo envoltorio: `--prueba=guion:res://minijuegos/muestras/prueba_muestras.gd --ritmo=8`. Resultado: `PRUEBAS hechas=61 fallos=0`. Cubre dificultad 1–3, muestra -1 y 0–3, ambos pilotos, bolsa y croquis corregibles, recorrido de ratón, entradas de teclado, golpes 3/4/5/6, desajustes, ventanas y límite de sesión. Se ejecutó sin GPU y con ventana real (Intel HD 620). No hubo `PRUEBA_FALLO` ni `SCRIPT ERROR`.

Evidencia: registros `prueba_requerida.log`, `prueba_modelo.log`, `prueba_visual.log`, `captura_anfitrion.log`; capturas 01–06, todas abiertas y revisadas, incluyendo anfitrión, herramientas, corrección, croquis, ritmo y capas revueltas. Texto mínimo 16 px, sin recortes observados.

Pendiente fuera de este carril: el entorno restringido imprime errores al escribir `user://logs` y leer el almacén de certificados; no impidieron las pruebas ni las capturas. No se midieron FPS ni se hizo una sesión humana completa con mando físico. No quedan tareas de implementación del minijuego.
