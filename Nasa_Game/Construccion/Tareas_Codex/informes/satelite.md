Implementado `satelite`, escena **1.5**, orden **3**, con montaje por teclado y arrastre, balance energético y dibujo propio.

Archivos escritos:

- [satelite.gd](juego/minijuegos/satelite/satelite.gd)
- [minijuego.json](juego/minijuegos/satelite/minijuego.json)
- [prueba_satelite.gd](juego/minijuegos/satelite/prueba_satelite.gd)
- [Nota, capturas y logs](Nasa_Game/Construccion/Minijuegos/satelite/NOTA.md)

El **modelo simplificado** usa unidades abstractas:

| Paneles | Generación por nivel 1/2/3 |
|---|---|
| Plegados | 2/2/2 u |
| Uno abierto | 5/4/4 u |
| Dos abiertos | 10/9/8 u |

Computadora: **2 u** por tramo; radio: **3 u**; batería inicialmente vacía, capacidad **4 u**. En sombra se generan **0 u**.

Para ganar: montar las cuatro piezas, desplegar la antena, mantener computadora y radio al sol, cubrir el consumo solar y conservar batería suficiente para la sombra. La solución abre ambos paneles y apaga la radio en sombra.

Duración máxima: **180 s**; ensayo: **4 s al sol + 4 s en sombra**. Los pilotos terminaron en menos de **16 s**.

Prueba requerida: **13 comprobaciones, 0 fallos**. Pruebas adicionales: **16 comprobaciones, 0 fallos**. Sin `PRUEBA_FALLO` ni `SCRIPT ERROR`; capturas inspeccionadas.

Sin pendientes funcionales. Persisten avisos del entorno sobre escritura de logs y certificados, documentados en la evidencia.