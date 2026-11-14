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
