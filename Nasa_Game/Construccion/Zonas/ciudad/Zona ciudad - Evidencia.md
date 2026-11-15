# Zona «ciudad»: La Plaza de las Iguanas

> Carril de la zona `ciudad` del juego jugable v0 (2026-11-14). **Escenario PROVISIONAL:** la plaza y la biblioteca no tienen concepto validado por Guillermo. Se construyeron solo con el estilo aprobado (D-011 y D-015) y las hojas `HR_URB_v1` y `HR_ARQ_v1`. Créditos de Higgsfield gastados: 0.

## Qué hay

- `juego/zonas/ciudad/ciudad.gd`, `zona.json` y `carga.jpg` (1024 px, captura propia de la biblioteca).
- Plaza de 26 × 18 m (x de −13 a 13; z de −9,3 a 8,2), con la fuente en el origen.
  - Fondo (arriba en pantalla): Biblioteca municipal en el centro y cuatro casas de colores.
  - Izquierda: la casa amarilla de la protagonista (ARQ-01) y dos casas más.
  - Derecha: la boca del camino del cerro, entre dos casas, con rocas, plantas y un tendedero.
  - Abajo: baranda URB-09 (la plaza es una terraza sobre el barrio).
- Mobiliario: fuente, 6 bancas, 7 jardineras con plantas, 4 faroles dobles, 2 faroles, kiosco de jugos (cerrado, con cartel dibujado), puesto de electrónica (cartel con un reloj), estatua de la iguana, poste indicador, bicicletero, 3 basureros, 2 postes de luz, 2 tendederos y 3 iguanas FAU-01 al sol.
- Flamboyán VEG-02 del sendero en la esquina del fondo a la derecha, con su sombra moteada sobre el puesto.
- Entradas: `inicio` y `casa` (−10,55; 0,55), `sendero` (10,7; 1,2) y `biblioteca` (0; −6,3).
- Umbrales con losa clara de 2,2 m y marca cian: `ACasa` → `habitacion:escalera` y `AlSendero` → `sendero:casa`.
- Interactuables: `Biblioteca`, `Fuente`, `Kiosco`, `PuestoElectronica`, `EstatuaIguana`, `PosteIndicador`, `Banca` e `Iguana` (regla «mirar sin espantar»: se esconde si llegas corriendo).
- Biblioteca: el primer uso da el diálogo y pone `base_visitada`; después pregunta qué libro abrir («Base en la Luna», «Base en Marte» o «Ahora no») y abre `base_luna` o `base_marte`. Pone `base_luna_hecha` o `base_marte_hecha` solo si el resultado trae `superado` y no trae `en_construccion`.
- Banderas: `ciudad_visitada`, `base_visitada`, `base_luna_hecha`, `base_marte_hecha`, `ciu_iguana` y `ciudad_noche_vista`.
- Fichas del cuaderno que abre: `chimborazo` (fuente), `cubesat` (puesto) y `observatorio_quito` (banca). Todas las cifras salen de `datos_espaciales.json`.
- Estados: tarde (luz aprobada, sin cambios) y noche provisional (con `mir_luna`): sin iguanas, vidrios de los faroles con brillo y charcos de luz pintados.

## IDs nuevos

| ID | Recurso | Archivo | Triángulos |
|---|---|---|---|
| **ARQ-13** | Biblioteca municipal: gradas, pórtico de 4 columnas, frontón con un libro abierto en relieve (sin letras) y puerta entreabierta con luz cian | `juego/modelos/ciudad/ARQ-13.glb` | 4 303 |
| **TER-14** | Suelo de la plaza: adoquín cálido, rosa de mosaico y losas claras en las salidas | `juego/modelos/ciudad/TER-14.glb` | 3 588 |

Variantes de color de IDs que ya existían: `ARQ-01_rosa`, `ARQ-02_coral`, `ARQ-02_crema`, `ARQ-02_verde` y `ARQ-02_zinc` (con el techo ARQ-03).

Modelados por primera vez desde las hojas (IDs del catálogo): URB-01, 02, 03, 05, 06, 07, 08, 10, 11 y 12; ARQ-01, 02, 08, 09 y 10. ARQ-04, 05 y 06 van dentro de las casas.

Generadores: `herramientas/mallas/ciudad_base.py`, `ciudad_mobiliario.py` (5 052 triángulos en 13 recursos) y `ciudad_arquitectura.py` (20 435 en 9 recursos).

Reutilizados: URB-09, TER-01, TER-02, TER-11, VEG-02, VEG-07, VEG-10, VEG-12, VEG-13, VEG-14 y FAU-01.

## Evidencia

- **Prueba `zona:ciudad`: 46 comprobaciones bien y 0 fallos** (entradas, umbrales despejados, ruta con la fuente, subida a la puerta de la biblioteca y salida al sendero).
- **Rendimiento** en la HD 620 a 1280 × 720 (`--medir=5`, meta de 40 fps):

| Punto | fps medio | ms p95 | Llamadas |
|---|---|---|---|
| Entrada `casa` | 43,8 | 27,3 | 65 |
| Centro (junto a la fuente) | 44,2 | 27,6 | 69 |
| Entrada `sendero` | 45,4 | 26,5 | 69 |
| Entrada `biblioteca` (cámara alejada) | 41,0 | 28,6 | 66 |
| `biblioteca` de noche | 41,2 | 28,6 | 76 |

- Capturas (carpeta `capturas/`):

![[01_plaza_entera.png]]
![[02_salida_casa.png]]
![[03_salida_sendero.png]]
![[04_salida_biblioteca.png]]
![[05_biblioteca.png]]
![[06_noche_provisional.png]]

## Decisiones que conviene validar

1. **Cámara en la biblioteca.** La cámara aprobada queda a menos de 7 m de altura y la fachada mide 5 m: de cerca solo se veían las columnas. Al acercarse a las gradas (z de −2,6 a −6,4) el encuadre baja de 0,17 a 0,10 y deja ver el frontón con el libro. Respeta lo que el jugador cambie con Z y X.
2. **Luz cian de la puerta.** De día va pintada (rendija emisiva y abanico en el podio y las gradas). Una luz real sobre la fachada costaba unos 3,5 fps.
3. **Noche sin luces reales.** Siete `OmniLight` bajaban la plaza a 27,5 fps y quemaban el adoquín claro. La noche usa brillo y charcos sumados: 41,2 fps.
4. **Límites de cámara:** x de −9,5 a 9,5 y z de −7,6 a 6,0. Detrás de las casas hay una ladera pintada, nunca el vacío.

## Pendiente

- Validación de Guillermo: plaza, biblioteca ARQ-13, suelo TER-14 y noche.
- La ventana de carga muestra `juego/interfaz/arte/carga_ciudad.jpg` (del integrador), no el `carga.jpg` de la zona. Esa ilustración enseña otra plaza (biblioteca a la derecha y escalinatas al fondo): si es el concepto que se valida, hay que rehacer la distribución.
- Anotar ARQ-13 y TER-14 en `manifiesto_recursos.csv` y en el catálogo (fuera de este carril).
- El margen de fps es corto en la vista de la biblioteca (41,0). Con una misma versión de la escena, dos mediciones seguidas dieron 36 y 40 fps mientras otros agentes usaban el equipo: conviene repetirla con el equipo libre.
- No hay vecinos (faltan sus mallas). El kiosco y el puesto están sin vendedor.
- No se modelaron URB-04 (glorieta), ARQ-07, ARQ-11 ni ARQ-12.
- El frontón entero solo se ve desde el podio; desde el pie de las gradas el libro queda en el borde de arriba.
- `base_luna` y `base_marte` todavía no existen: el núcleo avisa «en construcción» y no se ponen las banderas `_hecha`.
- Actualizar `trabajos.md` y `Memory.md` (lo hace el integrador).
