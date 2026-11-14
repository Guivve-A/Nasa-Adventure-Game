# «Tu primera base espacial» — diseño v0

> **Pedido de Guillermo (2026-11-13):** «Quiero dentro de mi juego un sistema para un mundo abierto espacial, con dinámicas propias de una vida espacial. Créalo como si fuera un RPG, tipo SAO vista superior, Bravely de Nintendo. Minijuego que aparece al entrar en la biblioteca de la ciudad.»
>
> **Reto de referencia** (`Nasa_Game/Referencias/Reto_base_espacial/reto_tu_primera_base_espacial.png`): «Diseña un juego para gestionar una base lunar o marciana: equilibra soporte vital, radiación, energía y alimentos para mantener viva la misión.»
>
> **Estado:** diseño propuesto por Claude, **sin validar**. El arte de la base y de la ciudad es provisional hasta que Guillermo apruebe sus conceptos.

## 1. Qué es

Un mundo abierto pequeño dentro del juego: una base en el polo sur de la Luna que hay que mantener viva. Se juega como un RPG de vista superior, con la misma cámara, la misma protagonista y el mismo estilo que el resto del juego.

- **Cómo se entra:** en la plaza de la ciudad está la biblioteca. Al cruzar su puerta, la protagonista abre un libro con holograma (recurso `TAL-13` del catálogo) y el libro la proyecta dentro de la base. Es una simulación: nadie corre peligro y se puede salir cuando se quiera («Cerrar el libro»).
- **Nombre provisional de la base:** «Base Chakana» (la chakana es la Cruz del Sur andina; la base está en el polo sur lunar). Lo decide Guillermo.
- **De quién se toma qué:** de los RPG de vista superior se toman principios (explorar un mundo, hablar, aceptar encargos, subir oficios, combates por turnos con riesgo y reserva). No se toma ningún nombre, personaje, interfaz ni arte ajeno.

## 2. Los cuatro medidores del reto

| Medidor | Qué mide | Baja con | Sube con |
|---|---|---|---|
| **Soporte vital** | Oxígeno y agua disponibles, y estado del depurador de CO₂ | El consumo de la tripulación, filtros gastados, fugas | Reciclador de agua, electrólisis (gasta energía y agua), hielo traído del cráter, plantas |
| **Energía** | Carga de las baterías | El consumo de la base, la sombra, el polvo en los paneles | Paneles limpios y bien orientados, más baterías |
| **Alimentos** | Raciones en despensa | Lo que come la tripulación cada sol | Cosechas del invernadero, reabastecimiento |
| **Radiación** | Dosis acumulada frente al límite de la misión | Tiempo en la superficie, tormentas solares | No baja: se **evita** con el refugio, el blindaje de regolito y menos horas fuera |

Si soporte vital, energía o alimentos llegan a cero, o la dosis pasa el límite, **la misión se interrumpe**: la tripulación evacúa sana y salva, y el parte explica la causa. No hay muerte.

## 3. Cómo es un sol (un día de trabajo)

1. **Parte de la mañana.** Control de misión resume el pronóstico (sol o sombra, actividad solar si ayer se llamó a la Tierra, cultivos) y propone 1 o 2 encargos.
2. **8 horas de trabajo.** La protagonista camina por la base. Cada módulo ofrece 2 o 3 acciones que cuestan horas, y a veces agua, energía o piezas.
3. **Oxígeno del traje.** Fuera de los módulos el traje gasta oxígeno en tiempo real. Se recarga en cualquier esclusa. Si se agota, vuelve de emergencia al hábitat y pierde 2 horas. Obliga a planear la ruta.
4. **Dormir** en el hábitat cierra el sol. Se calculan producción y consumo, crecen los cultivos y se sortea el suceso del sol siguiente.
5. **Parte del sol:** una tabla con qué subió, qué bajó y por qué, con un dato real al lado.

### Módulos y acciones (v0)

| Módulo | ID | Acciones |
|---|---|---|
| Hábitat | BAS-01 | Dormir (cierra el sol) · Ejercicio (1 h, cuida la salud) · Ver el parte |
| Invernadero | BAS-02 | Sembrar (1 h y agua) · Cuidar (1 h, crece más rápido) · Cosechar (1 h, da alimentos) |
| Paneles solares | BAS-03 | Limpiar el polvo (1 h) · Reorientar (1 h) |
| Baterías | BAS-04 | Ver la carga · Modo ahorro (sin horas; baja el consumo y la moral) |
| Soporte vital | BAS-05 | Cambiar el filtro de CO₂ (1 h y 1 filtro) · Reparar el reciclador (2 h y 1 pieza) · Producir oxígeno (gasta energía y agua) |
| Refugio | BAS-06 | Reforzar con regolito (2 h, más blindaje) · Refugiarse (durante una tormenta) |
| Antena | BAS-07 | Llamar a la Tierra (1 h: pronóstico de 2 soles y moral) |
| Rover | BAS-08 | Buscar hielo en el cráter en sombra (3 h, da agua) · Traer regolito (2 h) |
| Taller | BAS-09 | Fabricar filtro o pieza · Mejorar un módulo (gasta piezas) |

## 4. Capa de RPG

- **Oficios con nivel:** Ingeniería, Botánica, Soporte vital y Exploración. Cada acción da experiencia a su oficio; al subir de nivel cuesta menos horas o rinde más.
- **Encargos** de Control de misión, con recompensa en piezas, semillas o filtros.
- **Inventario:** piezas, filtros, semillas y hielo.
- **Compañeros:** Órbita (lee el dosímetro y avisa) y dos robots ayudantes originales que hacen una acción automática por sol si se les asigna.
- **Crisis por turnos.** Cuando llega un suceso se abre una pantalla de turnos: el «rival» es el peligro y tiene una barra de intensidad y un número de turnos; el «equipo» es la protagonista, Órbita y los sistemas de la base. En cada turno se elige una orden de un menú.
  - **Reservar:** no actúa, se protege y guarda 1 punto de reserva.
  - **Esfuerzo:** gasta reservas para dar hasta 3 órdenes en un turno. Sin reservas, queda en deuda y pierde los turnos siguientes.
  - Crisis de v0: **tormenta solar** (refugiarse, apagar equipos, poner los paneles de canto), **fallo de energía** (desconectar cargas, puentear una batería), **fuga en el hábitat** (localizar, sellar, bajar la presión) y **plaga en el invernadero** (aislar, podar, ajustar la humedad).
  - Cada orden correcta enseña la contramedida real. El resultado mueve los cuatro medidores.

## 5. Escenario de v0: «Los primeros 7 soles»

- Tripulación de 4. Empieza con reservas justas: un error se puede corregir, dos seguidos no.
- Sucesos fijos para aprender: sol 2, polvo en los paneles; sol 3, dos soles de sombra (hay que haber guardado energía); sol 5, tormenta solar (avisa un sol antes si se llamó a la Tierra); sol 6, fallo del reciclador.
- **Meta:** llegar al sol 7 con los cuatro medidores vivos, una cosecha hecha y el refugio reforzado. Después queda el modo libre.
- Un sol dura de 2 a 3 minutos. La partida de 7 soles, unos 20 minutos.
- El estado de la base se guarda con la partida (`Juego.estado["base"]`).

## 6. Datos reales

Cada sistema enseña un dato real con su fuente, como el resto del juego. El carril de datos los busca en fuentes primarias (NASA, ESA, artículos revisados) y los deja en `juego/base/datos_base.json` con su trazabilidad. Lo que no se verifique no entra.

Datos por verificar (ninguna cifra se da por buena hasta entonces): consumo diario de oxígeno, agua y alimento por persona; porcentaje de agua que recupera la Estación Espacial; dosis diaria medida en la superficie lunar y límites de dosis de una misión; grosor de regolito que hace falta de blindaje; duración del día y la noche lunares e iluminación del polo sur; hielo en los cráteres en sombra permanente; constante solar; retardo de la señal Tierra-Luna; horas de ejercicio diario en órbita; cultivos probados en el espacio; efecto del polvo lunar en los paneles.

El simulador simplifica, pero las proporciones salen de esos datos y el juego lo dice («modelo simplificado»).

## 7. El mundo

- Zona `base`: un tramo de unos 70 × 50 m del borde de un cráter del polo sur. Sol rasante, sombras muy largas y luz fría de relleno. Gravedad lunar (1,624 m/s²), salto flotante.
- Módulos conectados por túneles, con esclusas visibles; campo de paneles; plataforma de aterrizaje; el borde del cráter en sombra a un lado, adonde va el rover.
- **Entrada y salida:** se llega junto al libro holográfico abierto (`BAS-12`), que flota sobre una losa despejada. Es el umbral de vuelta a la biblioteca.
- Arte **provisional**, con las reglas del estilo aprobado: low-poly pintado, cian solo para tecnología, sin insignias ni logotipos. La imagen del reto es solo el enunciado: su paleta morada no es la del juego.

## 8. Arquitectura

| Pieza | Archivo | Qué hace |
|---|---|---|
| Simulación | `juego/base/sistema_base.gd` | Estado, acciones, cierre del sol, sucesos, oficios y guardado. Lógica pura, sin nodos visuales, determinista con semilla |
| Datos | `juego/base/base.json` y `juego/base/datos_base.json` | Módulos, acciones, sucesos y cifras reales con su fuente |
| Interfaz | `juego/base/interfaz_base.gd` y `juego/base/crisis.gd` | Los cuatro medidores, sol y horas, oxígeno del traje, panel de acciones, parte del sol y pantalla de crisis |
| Mundo | `juego/zonas/base/base.gd` y `juego/modelos/base/` | La zona, los módulos modelados y sus interactuables |
| Entrada | `juego/zonas/ciudad/` | La plaza con la biblioteca |
| Pruebas | `juego/base/prueba_base.gd` | Simulación de 7 soles con una estrategia buena (llega) y una mala (se interrumpe con su causa) |

Contrato mínimo de `sistema_base.gd` (lo usan el mundo y la interfaz):

```gdscript
signal cambio                      # algo cambió: refrescar la interfaz
signal sol_cerrado(parte: Dictionary)
signal crisis(suceso: Dictionary)
signal mision_interrumpida(causa: String)

func nueva(semilla: int = 1) -> void
func cargar(d: Dictionary) -> void          func guardar() -> Dictionary
func medidores() -> Dictionary              # {"soporte_vital", "energia", "alimentos", "radiacion"}: 0..1 y texto
func sol() -> int                           func horas() -> float
func acciones(modulo: String) -> Array      # [{"id", "nombre", "horas", "costo", "disponible", "motivo"}]
func hacer(modulo: String, accion: String) -> Dictionary   # {"ok", "mensaje", "ficha"}
func dormir() -> Dictionary                 # cierra el sol y devuelve el parte
func resolver_crisis(resultado: Dictionary) -> void
func nivel(oficio: String) -> int
```

## 9. Preguntas para Guillermo

1. ¿Luna o Marte? La propuesta es la Luna, porque enlaza con el sueño lunar y con los datos ya verificados.
2. ¿El nombre «Base Chakana»?
3. ¿Los ayudantes son robots originales, como aquí, o personas de la tripulación? Las personas piden mallas nuevas, con créditos.
4. ¿La biblioteca lleva interior propio o basta con la puerta que abre el libro?
5. ¿Aprobar la partida de conceptos de la base y de la ciudad (lote 06)?
