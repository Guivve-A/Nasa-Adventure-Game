# Arquitectura del juego jugable v0

Proyecto de Godot 4.7.2 (renderizador Mobile, 1280 × 720) en `juego/`. Todo se arma por código: no hay escenas `.tscn` salvo `principal.tscn`. Título provisional: «Luz cenicienta».

Quien construya una zona o un minijuego **solo toca su propia carpeta**. El núcleo (`nucleo/`, `interfaz/`, `shaders/`, `datos/`, `pruebas/`, `principal.gd`, `project.godot`) no se edita: si falta algo, se anota en el informe.

## 1. Mapa de carpetas

| Carpeta | Qué hay | Quién la toca |
|---|---|---|
| `nucleo/` | Autoloads y clases base | Solo el integrador |
| `interfaz/` | HUD, diálogo, ventana de carga, anfitrión de minijuegos, pausa, cuaderno y menú | Solo el integrador |
| `shaders/` | Los shaders **aprobados** del estilo 2.5D (D-015) y la marca de umbral | Nadie los cambia |
| `datos/` | `misiones.json` y `datos_espaciales.json` (55 fichas verificadas) con `FUENTES.md` | Solo el integrador |
| `zonas/<id>/` | `<id>.gd`, `zona.json`, `carga.jpg` y lo propio de la zona | El carril de esa zona |
| `minijuegos/<id>/` | `<id>.gd` y `minijuego.json` | El carril de ese minijuego |
| `modelos/entorno/` | GLB aprobados del sendero (TER, VEG, URB, COL, FX) | Lectura |
| `modelos/personajes/` | PER-01 (protagonista), PER-09 (Órbita con esqueleto), FAU-01 y COL-01 | Lectura |
| `modelos/<zona>/` | GLB nuevos de una zona, con su ID del catálogo | El carril de esa zona |
| `pruebas/pruebas.gd` | Pruebas automáticas | Solo el integrador |

`modelos/` tiene `.gdignore`: los GLB se cargan en tiempo de ejecución, sin importar.

## 2. Autoloads

| Nombre | Guion | Para qué |
|---|---|---|
| `Juego` | `nucleo/juego.gd` | Estado de la partida: banderas, inventario, cuaderno, misiones y guardado |
| `Audio` | `nucleo/audio.gd` | Sonidos provisionales: `Audio.sonar("ok")` (ok, error, pulsar, pagina, paso, salto, recoger, umbral, logro, tic, radio) |
| `Interfaz` | `nucleo/interfaz.gd` | Diálogos, avisos, ventana de carga, minijuegos, pausa, cuaderno y menú |
| `Zonas` | `nucleo/zonas.gd` | Cambio de zona, protagonista, Órbita y cámara |

Lo que más se usa:

```gdscript
Juego.poner_bandera("hab_seguidor")            # cumple un paso de misión (datos/misiones.json)
Juego.bandera("mir_luna")                      # -> bool (o el valor guardado)
Juego.sumar("panel_solar")                     # inventario; devuelve el total
Juego.anotar("luz_cenicienta")                 # abre una ficha del cuaderno
await Interfaz.decir([{"quien": "Órbita", "texto": "..."}, "texto sin nombre"])
var i: int = await Interfaz.elegir("¿Seguimos?", ["Sí", "Todavía no"])
Interfaz.aviso("Texto corto", 3.0)
var r: Dictionary = await Interfaz.abrir_minijuego("seguidor", {"dificultad": 1})
if r.get("superado", false): ...
Zonas.ir_a("sendero", "casa")                  # SIN await y como última instrucción
Zonas.jugador    Zonas.companero    Zonas.camara    Zonas.actual
```

**No uses `class_name`.** Las clases se nombran con `preload`: `const Piezas := preload("res://nucleo/piezas.gd")`. Las zonas ya heredan `Materiales`, `Recursos`, `Piezas`, `Iluminacion`, `Constructor`, `Umbral` e `Interactuable`.

**GDScript con tipos:** `var x := algo` falla si `algo` viene de un `Dictionary`, un `Array` o JSON («Cannot infer the type»). Escribe `var x: float = d["clave"]`.

## 3. Convenciones del mundo

- Metros. `+Y` arriba. La cámara es fija y mira hacia `-Z` desde lo alto: **`-Z` es «arriba» en pantalla y `+X` la derecha.**
- Cámara aprobada (D-013): 48° de inclinación y 40° de campo, sin horizonte ni cielo. La protagonista mide 1,05 m y Órbita 0,5 m.
- **Inclinación 2.5D** (D-015): los shaders desplazan cada vértice `z -= 0,45 · y`. Es solo visual: las colisiones no se inclinan. Lo que no use los shaders del proyecto debe compensarlo (mira `interactuable.gd`).
- Colores: solo la paleta maestra de la `Biblia de arte.md`. El cian `#62E4E0` es **solo** para tecnología e interacción. Lo más oscuro es `#322C1D`, nunca negro puro.
- Capas de colisión: 1 = mundo, 2 = protagonista.

## 4. Cómo se hace una zona

Copia `zonas/plantilla/`. Una zona es `zonas/<id>/<id>.gd` con `extends "res://nucleo/zona.gd"`, más `zona.json`.

```gdscript
extends "res://nucleo/zona.gd"

func _construir() -> void:
    encuadre = 0.18                         # alto de la protagonista en pantalla (0,125 a 0,21)
    limites = Rect2(-4, -4, 8, 8)           # hasta dónde sigue la cámara (XZ)
    luces("tarde")                          # tarde = luz APROBADA; manana, noche, interior_manana,
                                            # interior_noche y luna son provisionales
    ambiente(0.7)                           # pinceladas 2D-HD
    montar_layout("res://zonas/x/layout.json", "res://modelos")   # layout como el del sendero
    modelo("res://modelos/x/TAL-01.glb", Vector3(2, 0, -1), 90.0) # un GLB suelto
    pieza(m)                                # malla hecha con Piezas (bloques simples)
    piso(Vector3.ZERO, Vector2(8, 6)); pared(...); columna(...); rampa(...); colision_de_malla(nodo); cerco(...)
    entrada("inicio", Vector3(0, 0, 0))
    umbral("AlSendero", Vector3(3, 0, 2), "sendero", "casa", "Al sendero", {"requiere": "hab_seguidor", "mensaje_cerrado": "..."})
    interactuable("Banco", Vector3(2, 0, -0.4), "Usar el banco", _usar_banco)

func al_entrar(nombre_entrada: String) -> void: ...   # diálogos de llegada; puede usar await
func orbita_dice() -> Array: ...                     # qué dice Órbita aquí (vacío = pista del objetivo)
func ruta_de_prueba() -> Array: ...                  # recorrido automático para las pruebas
```

Reglas de una zona:

1. **Entrada y salida diseñadas** (regla de Guillermo). Cada umbral tiene alrededor un tramo despejado de unos 2 × 2 m que se lee de un vistazo, con la marca cian en el suelo. Cada entrada coloca a la protagonista a 1,2 m o más de la marca. La prueba lo mide.
2. **Ventana de carga.** `zona.json` lleva `"carga": {"imagen": "res://zonas/<id>/carga.jpg", "fichas": [...]}` con 3 a 6 fichas de `datos/datos_espaciales.json` que tengan que ver con el lugar.
3. **`Zonas.ir_a()` va sin `await` y al final.** La zona que llama se libera durante el cambio. Lo que pase después va en `al_entrar()` de la zona de destino.
4. **Estado por banderas.** La zona decide qué mostrar según `Juego.bandera(...)` (mañana o noche, lo ya recogido). Cada paso de `datos/misiones.json` se cumple con `Juego.poner_bandera(...)`.
5. **Escaleras con rampa** de colisión. La protagonista no sube escalones sueltos.
6. **`ruta_de_prueba()`** devuelve los pasos (`{"ir": Vector3}`, `{"usar": "Nombre"}`, `{"esperar": s}`, `{"bandera": "x"}`) que completan la zona según el estado actual. `{"usar": "@orbita"}` habla con Órbita. Con el piloto, los minijuegos se juegan solos y los diálogos no esperan. Un minijuego que todavía no existe devuelve `superado` con `"en_construccion": true`: no bloquea.
7. **Rendimiento.** El equipo mínimo es una Intel HD 620: meta de 40 fps o más a 1280 × 720. Los repetidos van en MultiMesh (el layout lo hace solo). Una luz con sombra (el sol); los faroles, sin sombra. Mide con `--medir=5`.
8. `altura_suelo(x, z)` necesita un cuadro de física: úsala en `al_entrar()`, no en `_construir()`.

`zona.json`:

```json
{
  "nombre": "La habitación-taller", "lugar": "Las Escalinatas, Guayaquil", "momento": "Mañana del día 1",
  "estado_arte": "concepto validado (L05 A); producción sin validar",
  "orden": 1,
  "carga": {"imagen": "res://zonas/habitacion/carga.jpg", "fichas": ["observatorio_quito", "cielo_15_grados"]},
  "entradas": {"inicio": "...", "escalera": "...", "cama": "..."}
}
```

`estado_arte` empieza por `provisional` cuando el escenario no tiene concepto validado por Guillermo: la ventana de carga y el menú lo avisan.

## 5. Arte: estilo, recursos y modelado

Guillermo (2026-11-13): «Siempre recuerda el estilo que hemos llevado, utilizar recursos, mandar a modelar los que falten, usar todo.»

- **Estilo aprobado:** low-poly pintado a mano (D-011) con acabado 2.5D (D-015). Facetas planas con degradado, luz cálida y sombra azul petróleo. Normas en `Nasa_Game/Fase_1_Arte/Biblia de arte.md`.
- **Usa lo que ya existe.** Hojas de referencia en `Nasa_Game/Fase_1_Arte/Hojas_de_referencia/` (`HR_TAL`, `HR_MIR`, `HR_ARQ`, `HR_URB`, `HR_COL`, `HR_VEG`, `HR_TER`, `HR_FAU`, `HR_PER`), con 104 recursos con ID en `manifiesto_recursos.csv`. GLB ya hechos en `juego/modelos/entorno/` (TER, VEG, URB-09, COL, FX).
- **Lo que falte se modela por script, con su ID.** Generador: `herramientas/mallas/nucleo.py` (lee su docstring y un ejemplo como `estructuras_piedra_madera.py` o `recolectables_col.py`). Escribe tu generador en `herramientas/mallas/<zona>_*.py` y los GLB en `juego/modelos/<zona>/<ID>.glb`. Materiales por nombre: `Facetado`, `Follaje`, `Agua` y `Emisivo`. Un recurso sin ID en el catálogo recibe uno nuevo de su familia (por ejemplo `TAL-15`) y se anota en el informe.
- **`Piezas`** (`nucleo/piezas.gd`) sirve para suelos, paredes y bloques simples. Los muebles y objetos con forma propia van como GLB.
- **Sin créditos de Higgsfield.** Los personajes y la fauna que falten (Tripo) se piden a Guillermo en una partida aparte: no se generan.
- **Nada de insignias, logotipos ni textos de la NASA o de misiones.** Sin marcas comerciales.

## 6. Cómo se hace un minijuego

Copia `minijuegos/plantilla/`. Un minijuego es `minijuegos/<id>/<id>.gd` con `extends "res://nucleo/minijuego.gd"`, más `minijuego.json`. Es un `Control` de 1120 × 520 px que se dibuja con nodos o con `_draw()`.

```gdscript
extends "res://nucleo/minijuego.gd"

func _preparar() -> void: ...          # arma nodos y estado; size ya vale 1120 x 520; dificultad = 1..3
func _empezar() -> void: ...           # el jugador pulsó «Empezar»
func _paso(delta: float) -> void: ...  # cada cuadro mientras activo; usa SIEMPRE delta, nunca la hora del sistema
func jugar_solo(acierta: bool) -> void: ...   # OBLIGATORIO: se juega solo y termina (superado o no) en menos de 40 s de juego
# terminar(superado, puntos, "frase que explica la causa")
```

Reglas de un minijuego:

1. **Enseña algo real.** Cada uno gira sobre un dato espacial verificado o una idea de control, y su `ficha` existe en `datos/datos_espaciales.json`. No se inventan cifras: salen de las fichas o de `datos/FUENTES.md`.
2. **Nunca «incorrecto».** Al fallar, `detalle` explica la causa física («con tanta ganancia, la antena se pasa y oscila»).
3. **Un parámetro a la vez.** Los de control muestran la prueba anterior al lado de la actual.
4. **Teclado, mando y ratón.** Acciones: `mover_izquierda`, `mover_derecha`, `mover_arriba`, `mover_abajo`, `interactuar` (E o Intro), `saltar` (Espacio). Ayudas: `eje_x()` y `eje_y()`. `Esc` es del anfitrión.
5. **De 1 a 3 minutos**, con dificultad 1, 2 y 3. La 1 se supera al primer o segundo intento.
6. **Legible:** texto de 16 px o más, sin depender solo del color, sin parpadeos rápidos.
7. Etiquetas: `Estilo.texto()` hace salto de línea automático y necesita `custom_minimum_size.x`. Para una sola línea usa `Estilo.linea()`.
8. El marco, el título, las instrucciones, las pistas y el resultado los pone el anfitrión: no los dibujes.

`minijuego.json`: `titulo`, `resumen` (una frase), `instrucciones` (2 a 4 pasos), `controles`, `pistas` (3 niveles: una mirada, una frase y la respuesta), `ficha`, `escena` (la del borrador de la Fase 2) y `orden`.

## 7. Pruebas y capturas

Godot se ejecuta **siempre** con el envoltorio, que toma un candado global (hay varios agentes y un solo equipo) y cierra Godot si se cuelga:

```
python -I herramientas/juego_ejecutar.py -- --prueba=nucleo --ritmo=8
python -I herramientas/juego_ejecutar.py -- --prueba=zona:habitacion --ritmo=6
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:seguidor --ritmo=8
python -I herramientas/juego_ejecutar.py --ventana -- --zona=habitacion --captura=C:/ruta/a.png --espera=3
python -I herramientas/juego_ejecutar.py --ventana -- --zona=habitacion --pos=1.5,-0.5 --mira=0,-1 --captura=C:/ruta/b.png
python -I herramientas/juego_ejecutar.py --ventana -- --zona=habitacion --banderas=mir_luna,mir_linea --captura=C:/ruta/noche.png
python -I herramientas/juego_ejecutar.py --ventana -- --zona=sendero --medir=5
python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=seguidor --auto --captura=C:/ruta/c.png --espera=4
python -I herramientas/juego_ejecutar.py --ventana -- --zona=habitacion --captura_carga=C:/ruta/carga.png --captura=C:/ruta/d.png
```

- Sin `--ventana` corre sin GPU (lógica y física). Con `--ventana` abre la ventana real: capturas y fps.
- `--todo` imprime toda la salida de Godot. Sale con código 1 si hay errores de guion o `PRUEBA_FALLO`.
- `--zona` entra en «visita libre» (umbrales abiertos). Con `--historia` respeta los requisitos. `--banderas=a,b` pone banderas antes de entrar. `--sin_hud` oculta el HUD en la captura.
- Mira tus capturas con la herramienta de lectura de imágenes antes de dar nada por bueno.
- Pocas corridas con ventana y de una en una: cada una ocupa la GPU de todos.

## 8. Ruta del prototipo

`datos/misiones.json` define los pasos y sus banderas. Zonas y enlaces:

| Zona | Entradas | Salidas | Banderas que pone |
|---|---|---|---|
| `habitacion` | `inicio`, `escalera`, `cama` | Escalera → `ciudad:casa` (requiere `hab_seguidor`); cama (de noche) → `luna:inicio` | `hab_convocatoria`, `hab_seguidor`, `hab_noche`, `hab_durmio`, `hab_seguidor_v2`, `fin_v0` |
| `ciudad` | `inicio`, `casa`, `sendero`, `biblioteca` | → `habitacion:escalera`; → `sendero:casa`; puerta de la biblioteca → `base:inicio` | `ciudad_visitada` |
| `sendero` | `casa`, `mirador` | → `ciudad:sendero`; → `mirador:sendero` (requiere `sen_antena`) | `sendero_visitado`, `sen_panel`, `sen_antena` |
| `mirador` | `sendero`, `inicio` | → `sendero:mirador`; atajo de los faroles → `habitacion:escalera` (requiere `mir_luna` y `mir_linea`) | `mirador_visitado`, `mir_satelite`, `mir_luna`, `mir_linea` |
| `luna` | `inicio` | La caja → `habitacion:cama`; `despertar()` desde la pausa | `luna_baliza`, `luna_muestras`, `luna_foto`, `luna_banderas`, `luna_regreso` |
| `base` | `inicio` | El libro holográfico → `ciudad:biblioteca`; `despertar()` desde la pausa | `base_visitada`, `base_sol_1`, `base_meta` |

Minijuegos: `seguidor` (habitación), `antena` (sendero), `satelite`, `telescopio`, `linea_tiempo` y `orbita` (mirador), `muestras`, `banderas` y `regreso` (luna).

**La base espacial** («Tu primera base espacial») es un mundo propio dentro del juego: diseño en `Nasa_Game/Construccion/Base espacial - Diseno.md`, código en `juego/base/` y zona `base`. Sus pruebas propias se corren con `--prueba=guion:res://base/prueba_base.gd`.
