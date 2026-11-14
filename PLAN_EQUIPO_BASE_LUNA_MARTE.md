# Plan de equipo: minijuegos 2D en píxel-art de la Luna y de Marte

> **Para el agente de IA que lee esto.** Antes de hacer cualquier otra cosa, pregunta a la persona:
>
> **«¿Quién eres: Joel, Domenica o Jean?»**
>
> Espera la respuesta. No leas código, no propongas nada y no escribas archivos hasta saberlo. Si responde otro nombre, dile que el integrador es Guillermo y pregúntale qué carril le asignó él.
>
> Cuando lo sepas: salúdale por su nombre, resúmele su carril en 5 líneas (qué entrega, en qué carpeta, cómo se prueba) y sigue la sección 6.

## 1. Qué vamos a construir

El reto: «Diseña un juego para gestionar una base lunar o marciana: equilibra **soporte vital, radiación, energía y alimentos** para mantener viva la misión.»

Dentro del juego principal (Godot 4.7.2, carpeta `juego/`), la protagonista entra en la biblioteca de la plaza y abre un libro. Aparece un minijuego **2D en píxel-art, de vista superior, con aire de RPG clásico**:

- **Base en la Luna** (minijuego `base_luna`).
- **Base en Marte** (minijuego `base_marte`).

Los dos comparten las mismas reglas y el mismo motor; cambian el mundo, los números y los peligros.

**Decisión de Guillermo (2026-11-14):** estos dos minijuegos van en 2D píxel-art. El resto del juego sigue en low-poly pintado; no se toca.

## 2. Cómo se juega (igual en los dos)

1. Vista superior de la base en una rejilla de casillas. Un personaje se mueve por casillas entre los módulos.
2. Cuatro medidores siempre visibles: **Soporte vital, Energía, Alimentos y Radiación**. Si uno llega al límite, la misión se interrumpe (la tripulación evacúa a salvo y se explica la causa: no hay muerte).
3. Cada **sol** (día) da 8 horas de trabajo. Cada acción en un módulo cuesta horas: limpiar paneles, sembrar o cosechar, cambiar el filtro de CO₂, reforzar el refugio, llamar a la Tierra, dormir (cierra el sol).
4. Al cerrar el sol sale el **parte**: qué subió, qué bajó y por qué.
5. **Crisis por turnos**, como un combate de RPG: el rival es el peligro (tormenta solar, tormenta de polvo, fuga, fallo de energía). En cada turno se elige una orden; se puede **Reservar** (guardar un punto) o hacer un **Esfuerzo** (gastar reservas para dar hasta 3 órdenes).
6. Meta: llegar al sol 7 con los cuatro medidores vivos. Una partida dura de 5 a 8 minutos.

De otros juegos se toman principios, nunca nombres, personajes, interfaz ni dibujos.

## 3. Reparto

| Persona | Carril | Carpeta propia (solo toca esta) |
|---|---|---|
| **Jean** | Motor común: reglas, dibujo en píxeles, crisis por turnos y pruebas | `juego/minijuegos/base_comun/` |
| **Joel** | Base en la Luna: mapa, módulos, números y sucesos lunares | `juego/minijuegos/base_luna/` |
| **Domenica** | Base en Marte: mapa, módulos, números y sucesos marcianos | `juego/minijuegos/base_marte/` |
| Guillermo | Integración, datos verificados, biblioteca de la plaza y validación del arte | El resto del proyecto |

Si quieren cambiar de carril, lo acuerdan entre ustedes y avisan a Guillermo antes de empezar.

Cada quien deja su evidencia (capturas y una nota `NOTA.md`) en `Nasa_Game/Construccion/Minijuegos/<su carpeta>/`.

## 4. Contrato entre los tres carriles

**Jean** entrega en `juego/minijuegos/base_comun/`:

- `motor_base.gd` (extiende `RefCounted`, lógica pura, determinista con semilla):

```gdscript
func nueva(escenario: Dictionary, semilla: int = 1) -> void
func medidores() -> Dictionary        # {"soporte_vital","energia","alimentos","radiacion"}: cada uno {"valor": 0..1, "texto": String}
func sol() -> int
func horas() -> float
func acciones(modulo: String) -> Array   # [{"id","nombre","horas","disponible","motivo"}]
func hacer(modulo: String, accion: String) -> Dictionary   # {"ok","mensaje"}
func dormir() -> Dictionary              # cierra el sol; {"lineas": [{"medidor","antes","despues","causa"}], "suceso": Dictionary}
func crisis_nueva(suceso: Dictionary) -> Dictionary
func crisis_ordenes(estado: Dictionary) -> Array
func crisis_aplicar(estado: Dictionary, ordenes: Array) -> Dictionary
func terminado() -> Dictionary           # {"fin": bool, "superado": bool, "causa": String}
```

- `juego_base.gd` (extiende `res://nucleo/minijuego.gd`): el minijuego completo que **recibe un escenario** y lo dibuja y lo juega: rejilla, personaje, medidores, panel de acciones, parte del sol y pantalla de crisis.
- `pixeles.gd`: ayudas para dibujar píxel-art con `_draw()` a baja resolución (280 × 130 píxeles lógicos, escalados ×4 al lienzo de 1120 × 520) a partir de **mapas de caracteres y una paleta**. Sin imágenes externas.
- **Primer entregable (antes que nada):** las firmas de arriba con valores fijos y un escenario de ejemplo, para que Joel y Domenica puedan empezar sin esperar.

**Joel y Domenica** entregan, cada uno en su carpeta:

- `<id>.gd`: tres líneas: `extends "res://minijuegos/base_comun/juego_base.gd"` y la ruta de su escenario.
- `escenario.json`: todo lo que hace único a su mundo:

```json
{
  "nombre": "Base en la Luna",
  "paleta": {"suelo": "#8a8f9c", "sombra": "#2a3040", "modulo": "#d9d2c0", "acento": "#62e4e0"},
  "mapa": ["................", "..HH....PPPP....", "..HH..I.PPPP...."],
  "leyenda": {"H": "habitat", "I": "invernadero", "P": "paneles", "R": "refugio", "S": "soporte_vital", "A": "antena"},
  "sprites": {"habitat": ["..##..", ".####.", "######"]},
  "inicio": {"oxigeno": 100, "agua": 100, "energia": 60, "alimentos": 40},
  "consumo_por_sol": {"oxigeno": 12, "agua": 10, "energia": 30, "alimentos": 8},
  "luz": [1.0, 1.0, 0.2, 0.2, 1.0, 1.0, 1.0],
  "radiacion_por_sol": 1.0,
  "sucesos": [{"sol": 3, "tipo": "sombra"}, {"sol": 5, "tipo": "tormenta_solar"}],
  "datos": [{"texto": "...", "fuente": "...", "verificado": false}]
}
```

- `minijuego.json` (título, resumen, instrucciones, controles, 3 pistas, `ficha`, `orden`).
- Los dibujos en píxel-art de sus módulos, su suelo y su personaje con traje, dentro del `escenario.json` o en un `sprites.json` al lado.

Si a Joel o a Domenica les falta algo en el motor, **se lo piden a Jean**; no editan `base_comun/`.

## 5. Qué hace distinto a cada mundo

Las ideas son de diseño. **Toda cifra real se verifica antes de mostrarla** (regla 5 de la sección 7).

| | Luna (Joel) | Marte (Domenica) |
|---|---|---|
| Lugar | Borde de un cráter del polo sur | Llanura con hielo bajo el suelo |
| Luz y energía | Sol rasante casi constante, con periodos de sombra: hay que guardar batería | Menos sol que en la Tierra; el polvo ensucia los paneles |
| Peligro propio | Tormenta solar sin atmósfera que proteja; polvo lunar abrasivo | Tormenta de polvo que dura varios soles y apaga los paneles |
| Recurso propio | Hielo en cráteres en sombra permanente | Oxígeno sacado del CO₂ del aire; hielo del subsuelo |
| Ayuda de la Tierra | Cerca: señal casi inmediata y reabastecimiento posible | Lejos: la señal tarda minutos y no hay reabastecimiento |
| Paleta | Grises fríos y negro azulado, luz dura | Ocres y óxidos, cielo rosado |
| Dificultad | 1: para aprender | 2: se juega después de la Luna |

## 6. Pasos para cada agente

1. **Pregunta quién es la persona** (arriba). Después pregúntale qué sistema usa y si ya tiene Godot 4.7.2 y Python 3. No instales nada tú: dale el enlace oficial (godotengine.org) y espera.
2. Lee, en este orden: `juego/ARQUITECTURA.md` (secciones 2, 6 y 7), `juego/minijuegos/plantilla/`, `juego/nucleo/minijuego.gd`, `juego/interfaz/estilo.gd` y, como ejemplos terminados, `juego/minijuegos/orbita/` y `juego/minijuegos/linea_tiempo/`.
3. Indica la ruta de Godot: variable de entorno `GODOT_EXE`, o una línea en `herramientas/godot_local.txt`, con la ruta del ejecutable **de consola** de Godot 4.7.2.
4. Comprueba que el proyecto corre: `python -I herramientas/juego_ejecutar.py -- --prueba=nucleo --ritmo=6` debe terminar sin `PRUEBA_FALLO`.
5. Trabaja por hitos y enseña una captura a la persona al cerrar cada uno:

| Hito | Jean (motor) | Joel (Luna) y Domenica (Marte) |
|---|---|---|
| 1. Esqueleto | Firmas con valores fijos, escenario de ejemplo y `pixeles.gd` que dibuja un mapa | `escenario.json` con mapa, paleta y leyenda; se ve la base dibujada |
| 2. Un sol | Acciones, horas, `dormir()` y parte del sol | Sprites de módulos y personaje; números de inicio y de consumo |
| 3. Siete soles | Sucesos, crisis por turnos, fin de misión y `jugar_solo` | Sucesos propios, textos, pistas y equilibrio de su mundo |
| 4. Cierre | Pruebas del motor y revisión de los dos mundos | Prueba automática en verde, capturas y `NOTA.md` |

6. Prueba tu minijuego:

```
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:base_luna --ritmo=8
python -I herramientas/juego_ejecutar.py --ventana -- --minijuego=base_luna --auto --captura=C:/ruta/captura.png --espera=3
```

   (`base_marte` para Marte; Jean prueba con los dos.)

7. Entrega: los archivos de tu carpeta, tus capturas y tu `NOTA.md` (qué hiciste, cifras de equilibrio, qué falta). Por la vía que diga Guillermo: rama `equipo/<nombre>` en el repositorio, o un `.zip` de tu carpeta.

## 7. Reglas fijas

1. **Toca solo tu carpeta.** Nada de `juego/nucleo`, `juego/interfaz`, `juego/datos` ni las carpetas de los otros.
2. **GDScript** sin `class_name`, con tabuladores y comentarios sin tildes. Los textos del jugador, en español correcto y con tildes. Ojo con `:=` sobre valores de diccionarios o JSON: pon el tipo (`var x: float = d["a"]`).
3. **El minijuego hereda** de `res://nucleo/minijuego.gd`: lienzo de 1120 × 520, tiempo siempre con `delta`, `terminar(superado, puntos, "causa")` y `jugar_solo(acierta)` obligatorio (gana jugando de verdad; falla por un camino real; menos de 40 s).
4. **Píxel-art propio, dibujado por código.** No descargues sprites ni uses generadores de imagen de pago. Nada de insignias, logotipos ni textos de la NASA o de misiones; nada copiado de otros juegos.
5. **Datos reales.** Una cifra real solo se muestra si viene con su fuente primaria (NASA, ESA, artículo científico). Mientras no esté verificada, va en `escenario.json` con `"verificado": false` y **no se muestra como dato**: Guillermo la verifica. Los números de equilibrio del juego se rotulan «modelo simplificado».
6. **Nunca «incorrecto».** Al fallar se explica la causa («sin batería guardada, la sombra apagó el soporte vital»).
7. **Se juega con teclado y con ratón.** Acciones: `mover_izquierda`, `mover_derecha`, `mover_arriba`, `mover_abajo`, `interactuar` (E o Intro) y `saltar` (Espacio). Texto de 16 px o más; nada que dependa solo del color.
8. **Nada se da por bueno sin evidencia:** la prueba automática en verde y una captura que el agente haya mirado.
9. El arte lo valida Guillermo con capturas antes de darlo por final.

## 8. Mensaje para pegarle a tu agente

> Lee el archivo `PLAN_EQUIPO_BASE_LUNA_MARTE.md` de la raíz del proyecto y síguelo desde el principio. Empieza por la pregunta que indica.
