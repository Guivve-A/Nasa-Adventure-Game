# Benchmark procedural de Godot 4.7

Proyecto minimo para Intel i5-7200U, Intel HD 620 y Windows 10. No requiere assets,
paquetes de Python, plugins, importaciones externas ni acceso a Internet.
El ejecutor requiere Python 3.13 y un ejecutable local de Godot **4.7** con soporte
para abrir proyectos (`--path`), por ejemplo el editor oficial.

Desde la raiz del repositorio, en PowerShell:

```powershell
py -3.13 pruebas/bench_render/correr_bench.py 'C:\Godot\Godot_v4.7-stable_win64.exe' --rapido
py -3.13 pruebas/bench_render/correr_bench.py 'C:\Godot\Godot_v4.7-stable_win64.exe'
```

La primera orden hace 10 corridas de 6 s a 1280x720. La segunda hace 20 corridas de
12 s a 1280x720 y 1920x1080. Cada corrida tiene ademas 3 s de calentamiento,
posteriores a construir la escena y generar la textura de ruido. SDFGI se prueba
solo con `forward_plus`. El limite por corrida es 120 s, incluido el arranque;
puedes cambiarlo con `--timeout 180`. No se lanza una nueva corrida hasta cerrar
la anterior. El codigo de salida del ejecutor es 0 si todas son validas, 1 si hay
fallos y 130 si se interrumpe con Ctrl+C.

Los resultados se escriben junto a este README: `resultados.json` contiene los
registros completos y `resultados.md` la tabla. Se actualizan despues de cada
corrida. Cada invocacion conserva sus JSON individuales y logs en una carpeta
nueva `corridas/run_*/`, evitando reutilizar un resultado antiguo. Un fallo de
arranque, codigo de salida no nulo, JSON invalido o tiempo agotado queda registrado;
el ejecutor termina el proceso (y su arbol en Windows) y sigue con la matriz.

Ejemplo individual desde la raiz del repositorio:

```powershell
& 'C:\Godot\Godot_v4.7-stable_win64.exe' --path pruebas/bench_render --rendering-method gl_compatibility --rendering-driver opengl3 --resolution 1280x720 --windowed --disable-vsync -- --escena=sprites --segundos=12 --salida=individual.json
```

Los argumentos propios van despues de `--`; `bench.gd` usa
`OS.get_cmdline_user_args()`. Admite `--escena=base|hierba|sprites|sdfgi`,
`--segundos=N` positivo y finito y `--salida=ruta.json`. Por defecto usa `base`,
12 s y `resultado_individual.json`. Las rutas relativas de salida se resuelven
respecto al proyecto, con creacion de los directorios padres.

## Escenas y condiciones

- `base`: suelo de 60x60 m con `NoiseTexture2D` de 512x512 y semilla fija;
  50 cajas, 50 esferas y 50 cilindros con materiales toon; sol con sombras;
  cielo procedural y ambiente. Camara con perspectiva, FOV vertical de 30 grados,
  inclinacion de -55 grados, azimut inicial de 45 grados y orbita de 0.025 rad/s.
- `hierba`: base mas 40000 instancias de una malla de dos quads cruzados
  (cuatro triangulos por brizna), con deformacion de viento por shader y sombras.
- `sprites`: base mas 200 `Sprite3D` con una textura RGBA generada en memoria,
  billboard, `ALPHA_CUT_DISCARD`, iluminacion y proyeccion de sombras.
- `sdfgi`: base con `sdfgi_enabled`, `ssao_enabled` y `glow_enabled`;
  geometria estatica marcada como `GI_MODE_STATIC` para contribuir a SDFGI.

El proyecto abre a 1280x720, sin escalado del viewport, sin limite de FPS y con
vsync desactivado. `--resolution` cambia el tamano real solicitado de la ventana;
el JSON registra el tamano efectivo del render target y si cambio. El ejecutor
rechaza resoluciones efectivas distintas: una pantalla que limite la ventana de
1920x1080 puede producir una corrida invalida. Manten la ventana visible.

El ejecutor fija Vulkan para Forward+ y Mobile, y OpenGL 3 para Compatibility,
de modo que la comparacion de los dos primeros use la misma API. El proyecto
desactiva el fallback automatico a OpenGL y D3D12. Ademas, el ejecutor comprueba
version 4.7, metodo, controlador, resolucion, vsync y efectos declarados por Godot.
Si el controlador del equipo no admite una combinacion, se registra como fallo;
no se atribuyen sus cifras a otro renderizador. Abrir el proyecto directamente
usa Compatibility. No se usa modo headless para medir renderizado.

## Metricas

`Time.get_ticks_usec()` mide los intervalos entre callbacks de `_process()`.
Se descarta el intervalo que cruza el final del calentamiento; la medicion acaba
al completar el primer cuadro que alcanza N segundos. `measured_seconds` refleja
la duracion real y puede exceder ligeramente la solicitada.

- `fps_mean`: cuadros medidos / segundos reales; no media de los FPS instantaneos.
- `fps_1pct_low`: 1000000 / media en microsegundos de los `ceil(cuadros * 0.01)`
  intervalos mas lentos. No es el percentil 99 invertido.
- `frame_time_mean_ms`, `frame_time_max_ms`: media y maximo de esos intervalos.
- `draw_calls_mean/max`, `primitives_mean/max`: contadores del motor por cuadro,
  leidos durante la medicion, con la posible latencia del render thread.
- `video_memory_mean_bytes`, `video_memory_max_bytes`, `video_memory_last_bytes`:
  memoria contabilizada por Godot. La tabla muestra el maximo en MiB.
- `adapter_name`, `graphics_api_version`, `rendering_method`, `rendering_driver`:
  informacion del dispositivo y del backend realmente usados.

Un contador de renderizado puede devolver 0 cuando no esta disponible. La memoria
reportada no equivale a VRAM fisica dedicada ni a toda la memoria compartida de
la HD 620. Los tiempos incluyen CPU, presentacion y esperas, no son tiempos GPU.
Los efectos y costes visuales pueden diferir entre renderizadores. Usa las mismas
condiciones de energia, temperatura y aplicaciones abiertas para comparar.

## API verificada en la documentacion oficial 4.7

- [Linea de comandos](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html):
  `--path <directory>`, `--rendering-method <renderer>`,
  `--rendering-driver <driver>`, `--resolution <W>x<H>`, `--windowed`,
  `--disable-vsync`, `--max-fps <fps>`, `--audio-driver <driver>` y separador `--`.
  Los tres metodos son `forward_plus`, `mobile` y `gl_compatibility`.
- [RenderingServer](https://docs.godotengine.org/en/4.7/classes/class_renderingserver.html):
  `get_rendering_info(info: RenderingInfo) -> int`,
  `RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME = 1`,
  `RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME = 2`,
  `RENDERING_INFO_VIDEO_MEM_USED = 5` (bytes). Los contadores requieren al menos
  dos cuadros renderizados y pueden devolver 0 si no estan disponibles.
  Identificacion mediante `get_video_adapter_name()`,
  `get_video_adapter_api_version()`, `get_current_rendering_method()` y
  `get_current_rendering_driver_name()`; controladores `vulkan` y `opengl3`.
- [OS](https://docs.godotengine.org/en/4.7/classes/class_os.html):
  `get_cmdline_user_args() -> PackedStringArray` obtiene los argumentos tras `--`.
- [ProjectSettings](https://docs.godotengine.org/en/4.7/classes/class_projectsettings.html):
  ventana, vsync, escalado desactivado y fallbacks del dispositivo.
- [SpriteBase3D](https://docs.godotengine.org/en/4.7/classes/class_spritebase3d.html),
  [BaseMaterial3D](https://docs.godotengine.org/en/4.7/classes/class_basematerial3d.html),
  [Environment](https://docs.godotengine.org/en/4.7/classes/class_environment.html),
  [NoiseTexture2D](https://docs.godotengine.org/en/4.7/classes/class_noisetexture2d.html) y
  [GeometryInstance3D](https://docs.godotengine.org/en/4.7/classes/class_geometryinstance3d.html):
  materiales toon, billboard y descarte alfa, efectos, textura asincrona y GI estatica.

Todos los assets se generan por codigo. No hay recursos de terceros.
La entrega se reviso de forma estatica y el ejecutor se verifico con procesos
simulados; no se ejecuto Godot ni se midio rendimiento durante su creacion.
