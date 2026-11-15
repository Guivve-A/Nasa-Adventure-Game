# Satélite: Un cubo de 10 cm

Implementación en `juego/minijuegos/satelite/`. Solo este carril y esta carpeta de evidencia.

Datos reales: fichas `pegaso`, `cubesat` y `exa_2007`, leídas con `FUENTES.md`. Pegaso fue el primer satélite ecuatoriano; cuerpo de 10 cm y dos paneles de 27 cm. EXA se presentó el 29-08-2007 e inició actividades el 01-11-2007. No se generaliza el estándar CubeSat.

El montaje representa cuatro funciones, no la ubicación real del hardware. Dibujo propio por polígonos, sin emblemas y sin escala. Fuentes de 16 a 22 px, paleta de Estilo.

Modelo simplificado: unidades abstractas u por tramo, no vatios ni cifras de Pegaso. Paneles plegados: 2 u; uno abierto: 5/4/4 u en niveles 1/2/3; dos abiertos: 10/9/8 u. Computadora: 2 u por tramo; radio: 3 u por tramo; antena: 0 u. Batería inicialmente vacía, capacidad 4 u. Tramos de 4 s al sol y 4 s en sombra; generación en sombra 0 u. El saldo al sol carga la batería, con saturación en 4 u; la sombra la descarga. Integración por delta con corte exacto entre tramos.

Victoria: cuatro piezas colocadas por función, antena desplegada, computadora encendida, radio al sol encendida, generación al sol mayor o igual al consumo y batería suficiente hasta finalizar la sombra. Solución: dos paneles abiertos y radio apagada en sombra. Carga 4/4/3 u según nivel, gasto en sombra 2 u. Puede terminar con batería exactamente en 0 u (tolerancia numérica 0,001 u).

Duración máxima humana 180 s; ciclo de ensayo 8 s. El piloto usa las mismas operaciones de montaje y ajuste. El fallo automático monta todo pero conserva la antena plegada y pulsa la prueba.

Validación final (14-11-2026):

- Contrato: `python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:satelite --ritmo=8 --todo`. Se ejecutó también con `--todo` antes del separador para conservar toda la salida en `prueba_contrato.log`: `PRUEBAS hechas=13 fallos=0`, `FIN`, `errores=0`. Victorias en 15,627 s (nivel 1) y 14,628 s (nivel 3); fallo causal por antena en 6,293 s.
- Cobertura propia: `python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/satelite/prueba_satelite.gd --ritmo=8`. Resultado en `prueba_adicional.log`: 16 comprobaciones, 0 fallos. Montaje con eventos de teclado y arrastre, bloqueo de montaje incompleto, rechazo causal de un hueco ajeno, tres niveles con delta 0,016 y 0,37, y fallos por antena, computadora, radio apagada al sol, generación insuficiente y batería agotada en sombra. Pilotos ganadores entre 13,76 y 15,54 s.
- `montaje.png` y `balance.png`: capturas reales mediante el envoltorio, abiertas e inspeccionadas. Texto visible, sin recortes ni cruces con la antena. `balance.png` muestra la descarga en sombra.
- JSON válido; sangría de tabuladores, sin `class_name` ni comentarios con tildes. Sin instalaciones ni consultas externas.

No quedan pendientes funcionales en este carril. El entorno restringido emite avisos `Failed to open ... user://logs` y `Failed to read the root certificate store`; ambos constan en los logs. No hubo `PRUEBA_FALLO` ni `SCRIPT ERROR`. No se modificó infraestructura ajena para corregir esos avisos. La prueba de entradas usa eventos sintéticos sobre los manejadores reales; no se verificó un mando físico.

## Jugado con teclado y con ratón

La nueva `prueba_manos.gd` abre `Interfaz.abrir_minijuego("satelite", {"dificultad": 1})` en otra corrutina, desactiva el piloto y gana por teclado y por ratón mediante eventos físicos simulados con `Input.parse_input_event()`. Comprueba todas las teclas anunciadas, las cuatro piezas, los cinco ajustes, los botones de acción, Continuar, Esc en seis fases, cierre y árbol sin pausa. Es una comprobación del recorrido real del anfitrión, adicional a la prueba anterior que llamaba directamente a los manejadores.

Se precisó qué flechas eligen filas y cuáles cambian valores, se explicó Comprobar, se anunció el montaje por dos clics y se hizo visible una guía para ganar sin memorizar números. Las regiones de piezas y huecos ahora son controles con nombre y ayuda; la prueba obtiene sus posiciones con `get_global_rect()`. No se modificaron el modelo energético ni los datos reales. No se encontró una acción necesaria sin alternativa de teclado o ratón ni dependencia del foco durante la partida.

El inventario control por control, los comandos, la salida completa de ambas pruebas, la revisión visual y los límites de la evidencia están en [INFORME_MANOS.md](INFORME_MANOS.md). Los logs finales son `prueba_manos.log`, `prueba_minijuego_manos.log` y `prueba_manos_ventana.log`.

Resultado final: manos **88 comprobaciones, 0 fallos**; contrato **13 comprobaciones correctas**; ventana real **88 comprobaciones, 0 fallos**. Las dos pruebas solicitadas terminan con `FIN` y `errores=0`, sin `PRUEBA_FALLO` ni `SCRIPT ERROR`. Esc funciona durante instrucciones, pieza tomada, ajustes, sol, sombra y resultado. Se abrieron las cinco capturas finales: textos, botones y ayudas legibles, sin recortes importantes. Sin pendientes funcionales identificados; permanecen los avisos del entorno descritos arriba.
