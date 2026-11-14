# linea_tiempo · Ecuador ya dejó un mensaje

Implementado el 13-11-2026. Solo se escribieron archivos dentro del minijuego y de esta carpeta de evidencia. Sin instalaciones, descargas ni servicios externos.

## Archivos

- `juego/minijuegos/linea_tiempo/linea_tiempo.gd`: modelo, tarjetas, controles, pistas y piloto.
- `juego/minijuegos/linea_tiempo/minijuego.json`: metadatos completos; ficha `disco_apolo11`, escena `2.4`, orden `5`.
- `juego/minijuegos/linea_tiempo/prueba_linea_tiempo.gd`: comprobaciones adicionales de los tres niveles, entradas y duración del piloto.
- Esta nota, `prueba_oficial.txt`, `prueba_entradas.txt`, `captura_nivel3.png` y `captura_anfitrion.png`.

## Reglas

| Dificultad | Tarjetas | Comprobaciones máximas | Hitos incluidos (índice de la tabla siguiente) |
|---|---:|---:|---|
| 1 | 5 | 4 | 1, 2, 3, 8, 9 |
| 2 | 7 | 4 | 1, 2, 3, 4, 6, 8, 9 |
| 3 | 9 | 3 | Todos |

Victoria: **0 pares adyacentes invertidos**, comprobada con el botón o Espacio, incluida la última comprobación disponible. Premio: 100 puntos, sin descuento por movimientos o comprobaciones. Fallo: agotar el presupuesto dejando al menos 1 par invertido; el resultado identifica ese par, sus fechas y qué vino antes.

Las marcas ✓ indican exclusivamente orden correcto con las vecinas inmediatas, no posición absoluta ni tarjeta inmóvil. Se borran al mover; las fechas ya descubiertas se conservan para aprender. Las otras tarjetas reciben una pista relativa más clara y una explicación ampliada al seleccionarlas. El teclado toma/suelta con E/Intro y desplaza con izquierda/derecha; arriba/abajo permite elegir otra tarjeta. El ratón arrastra por inserciones adyacentes, incluso cruzando varios huecos. No se bloquean tarjetas.

Duración humana prevista: 1–3 minutos, sin cronómetro de derrota ni espera obligatoria. No se ha medido con una persona. El piloto usa delta, actúa cada 0,30 s y hace movimientos y comprobaciones por las mismas funciones que las entradas. Medido con pasos de 0,05 s: victorias en 0,90 / 1,80 / 2,40 s (niveles 1/2/3), siempre en 2 comprobaciones; fallos en 1,20 / 1,20 / 0,90 s, agotando 4/4/3 comprobaciones. Ambos caminos terminan antes de 40 s; no llaman directamente a terminar desde el piloto.

## Fichas y fechas

Todos los hitos solicitados tienen ficha; no se excluyó ninguno. Trazabilidad cotejada con `juego/datos/datos_espaciales.json` y `juego/datos/FUENTES.md`:

| Índice | Fecha revelada | Ficha |
|---|---|---|
| 1 | 1873 | `observatorio_quito` |
| 2 | 1957 | `estacion_cotopaxi` |
| 3 | 1969 | `disco_apolo11` (año en su campo `fuente`; 73 países en `texto`) |
| 4 | 1975 | `apolo_soyuz_1975` |
| 5 | 14-11-1981 | `sts2_despedida` |
| 6 | 01-07-1982 | `estacion_entrega` |
| 7 | 2007 | `exa_2007` |
| 8 | 2013 | `pegaso_lanzamiento` |
| 9 | 21-06-2023 | `acuerdos_artemisa` (firmante n.º 26) |

No se vincula la estación con Apolo 11. No se afirma la permanencia actual del disco. El título solicitado se conserva; el cuerpo describe el viaje histórico. Sin emblemas, logotipos ni transcripciones de mensajes de misiones. Las pistas de época y relaciones antes/después son ayudas didácticas derivadas de estas fechas, no acontecimientos adicionales.

## Verificación ejecutada

Comando oficial:

```text
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:linea_tiempo --ritmo=8 --todo
```

Resultado final: código 0; **13 PRUEBA_OK**, ningún `PRUEBA_FALLO` ni `SCRIPT ERROR`; victorias d1/d3 y fallo causal d1. Cierre: `[godot: ok; 2 s; lineas=26; errores=0]`. Salida guardada en `prueba_oficial.txt`. El envoltorio solo interpreta `--todo` antes del separador; también se ejecutó así la prueba adicional para conservar su salida completa.

Prueba adicional con ventana, siempre bajo el candado del envoltorio:

```text
python -I herramientas/juego_ejecutar.py --ventana --todo -- --prueba=guion:res://minijuegos/linea_tiempo/prueba_linea_tiempo.gd --ritmo=8
```

**PRUEBAS hechas=27 fallos=0**. Comprueba cantidad, fechas inicialmente ocultas, marcas vecinales, movimientos sin gastar intentos, victoria mediante acciones de teclado, arrastre de varios huecos, victoria/fallo del piloto en los tres niveles antes de 40 s y ajuste de textos. Las entradas son eventos sintéticos por las rutas del minijuego; no un ensayo manual de teclas físicas. Motor observado: Godot 4.7.2, Vulkan Mobile, Intel HD 620. Ambas capturas fueron abiertas y revisadas: nueve tarjetas legibles, texto mínimo 16 px y controles dentro del lienzo; la segunda muestra el anfitrión real. La primera usa un fondo de prueba gris; el anfitrión aporta el fondo papel final.

El entorno emite errores al abrir `user://logs/godot.log`, rotar registros y leer certificados del sistema. Persisten fuera del alcance autorizado; no producen fallos de guion ni de las pruebas. Una primera captura del anfitrión falló por la ruta con espacios; se corrigió el entrecomillado y se verificó el PNG guardado.

Pendiente: prueba humana de comprensión y duración; no se midieron fps de forma sostenida. No hay bloqueos de implementación conocidos.
