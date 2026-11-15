# Linea del tiempo a pantalla completa

Se conserva el arcade de escalinata, placas, saltos y animales. `_init()` activa `pantalla_completa`; el lienzo es 1280 x 720 (320 x 180 logicos, escala 4).

El marcador ocupa y=0..28, con todos sus indicadores a 4 pixeles o mas del borde. Cielo estrellado y lomas ocupan y=29..54; el mosaico se prolonga hasta y=179 y ambos bordes, con casas laterales. Las columnas pasan a x=70/160/250, las filas distan 80 pixeles y la camara mantiene a la jugadora en y=128 durante la subida. Direcciones, E para saltar y Esc se dibujan en y=170 dentro del campo. Los avisos de anio aparecen en y=151..161.

La rapidez pasa a 76 pixeles/s para compensar el recorrido mas ancho y largo. Dificultad 1 conserva 100 s, tres vidas y placas con tolerancia de 16 pixeles; sus animales aparecen cada 4,2 s y la placa correcta conserva el brillo cian. No se modificaron datos historicos ni parametros aceptados. JSON actualizado con resumen, tres instrucciones cortas, controles y tres pistas del arcade real.

`prueba_manos.gd` sigue usando exclusivamente `Input.parse_input_event` con `InputEventKey` para jugar. Recorre dificultades 1, 2 y 3, comprueba el campo completo, la ausencia de titulo/controles externos, victoria, cierre y arbol sin pausa. La prueba de modelo conserva su comprobacion de aterrizaje con las coordenadas nuevas (160,65).

## Prueba del contrato

Comando: `python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:linea_tiempo --ritmo=8`

```text
PRUEBA_OK linea_tiempo.minijuego_json
PRUEBA_OK linea_tiempo.json.titulo
PRUEBA_OK linea_tiempo.json.resumen
PRUEBA_OK linea_tiempo.json.controles
PRUEBA_OK linea_tiempo.json.instrucciones
PRUEBA_OK linea_tiempo.json.pistas
PRUEBA_OK linea_tiempo.json.ficha
PRUEBA_OK linea_tiempo.d1.termina_solo
PRUEBA_OK linea_tiempo.d1.se_puede_superar
PRUEBA_OK linea_tiempo.d3.termina_solo
PRUEBA_OK linea_tiempo.d3.se_puede_superar
PRUEBA_OK linea_tiempo.se_puede_fallar
PRUEBA_OK linea_tiempo.el_fallo_explica_la_causa
FIN
[godot: ok; 13 s; lineas=30; errores=0]
```

## Prueba con teclas

Comando: `python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/linea_tiempo/prueba_manos.gd --ritmo=1`

```text
LINEA_MANOS nivel=1 saltos=10 tiempo=34.72 vidas=3
LINEA_MANOS nivel=2 saltos=9 tiempo=34.73 vidas=3
LINEA_MANOS nivel=3 saltos=10 tiempo=35.05 vidas=2
PRUEBA_OK linea.manos.anfitrion_cerrado
PRUEBA_OK linea.manos.arbol_sin_pausa
PRUEBAS hechas=30 fallos=0
FIN
[godot: ok; 107 s; lineas=50; errores=0]
```

Las dos pruebas terminaron con codigo 0 y sin fallos de prueba ni errores de guion. El motor emitio mensajes de entorno sobre escritura de logs, certificados del sistema y recursos al salir; no se tocaron carpetas comunes para resolverlos. Log completo de teclas: `prueba_manos.log`.

## Capturas con ventana

Tres PNG de 1280 x 720, abiertos y revisados visualmente: campo sin marco exterior, HUD legible dentro del campo y progreso distinto (1/9, 3/9 y 6/9).

- `Nasa_Game/Construccion/Minijuegos/linea_tiempo/completa_1.png`: espera 5 s, primer hito revelado.
- `Nasa_Game/Construccion/Minijuegos/linea_tiempo/completa_2.png`: espera 14 s, disco lunar revelado.
- `Nasa_Game/Construccion/Minijuegos/linea_tiempo/completa_3.png`: espera 25 s, entrega revelada y salto hacia EXA.

Se ejecutaron mediante `python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=linea_tiempo --auto --captura=<ruta_absoluta_del_png> --espera=<5|14|25>`.

```text
completa_1.png: CAPTURA_OK; [godot: ok; 9 s; lineas=11; errores=0]
completa_2.png: CAPTURA_OK; [godot: ok; 16 s; lineas=11; errores=0]
completa_3.png: CAPTURA_OK; [godot: ok; 27 s; lineas=11; errores=0]
```

Log de las capturas validas: `completa_capturas_absolutas.log`. Los primeros intentos con rutas relativas no guardaron PNG; se repitieron con rutas absolutas y se comprobaron los archivos reales.

Pendiente: nada dentro del alcance solicitado. Solo se modifico `juego/minijuegos/linea_tiempo/` y su carpeta de evidencia.
