# Dos banderas, un cielo

Implementado el 14-11-2026. Solo se escribieron archivos de las dos carpetas autorizadas.

Archivos de juego: `banderas.gd`, `minijuego.json` y `prueba_banderas.gd` en `juego/minijuegos/banderas/`. Metadatos: ficha `bandera_lunar`, escena `3.5`, orden 7. No requiere recursos externos.

Modelo y reglas:

- Cinco pasos reales, con las mismas operaciones para persona y piloto. Sitios A (interior), B (huellas) y C (suelo libre). A y B explican y permiten volver a elegir, sin descontar nada. El anillo representa 75 m desde la etapa de descenso: recomendación técnica para visitantes robóticos, no ley. El mapa es esquemático.
- Cada conjunto requiere mástil, barra y tela, en ese orden. Las banderas permanecen sujetas; no hay física, daño ni caída. Son una instalación nueva del sueño; no se muestra una bandera histórica.
- Compás de 1,5 s, un pulso por ciclo. Dificultades 1/2/3: centro ±18/14/11 % del ciclo (±0,27/0,21/0,165 s); 3/3/4 pulsos por mástil. Con 5 pulsos fuera de ventana termina con causa. No se mide fuerza.
- Barras al 100 %, con ajuste final al extremo desde 99,9 %. Con 3 comprobaciones sin extender ambas termina explicando que falta soporte y no hay viento. Los pliegues son estáticos.
- Alturas entre 130 y 240 unidades gráficas; diferencia máxima 2. Separación entre mástiles de 190 a 250 px, telas de 180 × 90 px: hueco de 10 a 70 px. Ambas banderas tienen igual tamaño nominal; amarillo ecuatoriano doble que azul y rojo, con escudo simplificado; Estados Unidos con 13 franjas y cantón de 50 estrellas simplificadas. No son proporciones legales ni medidas físicas verificadas.
- Límite humano: 180 s; 100 puntos al completar. Amanecer ficticio de 1,5 s y luego escena estática durante 3 s en silencio, antes de emitir el resultado al anfitrión. El minijuego no reproduce sonidos. El anfitrión conserva su sonido de resultado después de la pausa.
- Datos factuales solo de `bandera_lunar`, `tratado_espacio`, `acuerdos_artemisa` y `zona_75_m`, contrastados con `FUENTES.md`. Compás, tolerancias, montaje, duraciones y unidades gráficas son reglas didácticas. El resultado cita el artículo II y la firma ecuatoriana del 21-06-2023 (país n.º 26).

Verificación:

```
python -I herramientas/juego_ejecutar.py -- --prueba=minijuego:banderas --ritmo=8 --todo
[godot: ok; 9 s; lineas=26; errores=0]
```

13 comprobaciones del contrato aprobadas: metadatos, victoria en dificultades 1 y 3, fallo real y causa. Salida en `prueba_contrato.txt`. Sin `PRUEBA_FALLO` ni `SCRIPT ERROR`.

```
python -I herramientas/juego_ejecutar.py --todo -- --prueba=guion:res://minijuegos/banderas/prueba_banderas.gd --ritmo=8
PRUEBAS hechas=22 fallos=0
[godot: ok; 1 s; lineas=38; errores=0]
```

Prueba propia a 60 pasos/s: victorias de 21,100 / 21,133 / 24,167 s; fallos de 13,350 / 13,383 / 16,417 s (dificultades 1/2/3). Verifica estado real del montaje, compás, extensión, alturas, separación y ceremonia de al menos 4,5 s. También verifica sitio protegido sin castigo y orden de soporte. Salida en `prueba_reglas.txt`.

Capturas `soportes.png` (13,2 s) y `amanecer.png` (19 s), generadas con el envoltorio y revisadas visualmente: texto legible, botones dentro del lienzo, escudo reconocible y ninguna tela oculta en el final.

Pendiente: no hay bloqueo funcional. No se midieron fps ni se realizó una partida humana completa con dispositivos físicos. El entorno emite avisos de acceso a `user://logs` y de lectura del almacén de certificados; no son errores de guion, y el envoltorio devuelve código 0. No se modificó el núcleo para resolverlos.
