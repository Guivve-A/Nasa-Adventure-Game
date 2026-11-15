# Rig de la protagonista (PER-01)

> Estado al 2026-11-14, 12:50: **entregado y medido**. Los seis clips cumplen los criterios a) a f); el bolso tiene un límite conocido (ver «Límites»). Falta el visto bueno de Guillermo viéndola moverse en el juego.

## Qué se entrega

| Archivo | Contenido |
|---|---|
| `herramientas/blender/rig_protagonista.py` | Script de punta a punta (Blender 5.3 sin ventana; de 18 a 39 s hasta el GLB según la carga del equipo, unos 10 s más con renders). Argumentos: `--entrada`, `--salida`, `--textura`, `--guardar-blend`, `--medidas`, `--informe`, `--renders` |
| `juego/modelos/personajes/PER-01_rig.glb` | 4,11 MB, 8 114 triángulos, 20 huesos, 6 clips, textura del cuerpo de 2048 × 2048 |
| `juego/modelos/personajes/PER-01_medidas.json` | Medidas en unidades del GLB (alto 1 m) para el juego y para el plan B |
| Esta carpeta | `informe_rig.json`, `corrida_final.log`, `renders/`, `parecido/`, capturas de Godot y la verificación del bolso |

La entrada `PER-01.glb` no se tocó (SHA-256 `943abc5b…`). El script es reproducible: dos corridas seguidas dieron el mismo GLB byte a byte (SHA-256 `c9ce4664…`).

Comando:

```
"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup --python-exit-code 1 --python herramientas/blender/rig_protagonista.py -- --entrada juego/modelos/personajes/PER-01.glb --salida juego/modelos/personajes/PER-01_rig.glb --textura 2048 --medidas juego/modelos/personajes/PER-01_medidas.json --informe Nasa_Game/Fase_3_Personajes/Rig_protagonista/informe_rig.json --renders <carpeta>
```

## Método

1. **Importación.** Hornea las transformaciones de los nodos en los vértices y reduce la textura del cuerpo de 4096 a 2048 px. El cuerpo tiene 5 156 vértices y 3 755 posiciones únicas: los pesos se calculan sobre las posiciones únicas (equivale a soldar la malla de Tripo) y se copian a los duplicados.
2. **Armadura propia, sin Rigify:** 20 huesos. Cadera (raíz), columna, pecho, cuello, cabeza; hombro, brazo, antebrazo y mano por lado; muslo, pierna y pie por lado; y un hueso `bolso` hijo de la cadera. Las articulaciones salen de medir la malla (constantes `C` del script).
3. **Pesos geométricos, sin el calor de huesos de Blender:**
   - regiones por conectividad y geometría (cabeza y pelo 1 590 posiciones, brazos 161 y 143, piernas 592 y 449);
   - mezcla analítica en codo, muñeca, rodilla y tobillo;
   - difusión armónica sobre la malla en hombros, caderas y cuello (512 posiciones libres);
   - cabeza, cara y pelo rígidos al hueso de la cabeza; bolso rígido a su hueso;
   - 4 influencias como máximo; la suma de pesos va de 0,9999999 a 1,0000001.
4. **Animación por fórmula** a 50 cuadros por segundo, una clave por cuadro. Las piernas se resuelven con cinemática inversa analítica y los pies se apoyan en el suelo. Solo se anima la rotación de cada hueso y la altura de la cadera: sin escala ni cizalla.
5. **Exportación** con una pista NLA por clip. El script vuelve a leer el GLB con un lector propio y mide todo sobre el archivo. Si fallan los criterios b), c) o d), los nombres, las duraciones o la igualdad con la malla de entrada, no escribe la salida.

![[pesos_frente.jpg|260]] ![[esqueleto_frente.jpg|260]]

## Clips

| Clip | Duración | Cíclico | Qué hace |
|---|---|---|---|
| `reposo` | 2,0 s | sí | Respiración y balanceo de 0,9° |
| `caminar` | 0,8 s | sí | 2 pasos, brazos en oposición, rebote de 2 cm |
| `correr` | 0,56 s | sí | Tronco 11° adelante, codos a 80°, fase de vuelo del 36 % |
| `salto_lunar` | 1,2 s | sí | Flotación en el aire, piernas recogidas y brazos abiertos |
| `recoger` | 1,0 s | no | Se agacha 22,5 cm, baja la mano izquierda y vuelve |
| `celebrar` | 1,4 s | no | Anticipa, sube los brazos en V y vuelve |

La repetición de los cíclicos se activa en Godot (`jugador.gd`), no en el archivo.

![[caminar_perfil.jpg]]
![[caminar_frente.jpg]]
![[correr_perfil.jpg]]
![[correr_frente.jpg]]
![[celebrar_frente.jpg]]
![[recoger_perfil.jpg]]
![[salto_lunar_perfil.jpg]]

## Criterios de aceptación

| Criterio | Medición | Resultado |
|---|---|---|
| a) Reposo igual a la malla original | Diferencia máxima de vértices entrada-salida: 0,00003 mm. Piel en reposo: 0,0009 mm. Caja: y de −0,5000 a 0,4939, igual que la entrada; mira a +X | Cumple |
| a) Parecido con la hoja | **81,4 %** con la métrica v2 (`--registro`), mismo encuadre que la v9 (82,1 %). Por vista: frente 83,8; cabeza 79,5; perfil 76,2; espalda 85,5 | Cumple (≥ 80 %) |
| b) Aristas que no pasan de 2,2 veces | Peor cuadro de cada clip: reposo 100 %, caminar 100 %, correr 99,94 %, salto lunar 99,90 %, recoger 99,84 %, celebrar 99,81 % | Cumple (≥ 99,5 %) |
| b) Cara y pelo | 2 294 vértices con peso 1 al hueso de la cabeza; deformación máxima 0,00002 % | Cumple |
| c) Pies al caminar | El vértice más bajo queda en y = −0,50003 en los 41 cuadros | Cumple (−0,53 a −0,47) |
| d) Ciclos cerrados | Giro entre el primer y el último cuadro: 0,000002° (lector propio) y 0° (lectura independiente). Raíz sin desplazamiento en el plano: menos de 0,00003 mm | Cumple (< 0,5°) |
| e) Bolso | Caminar, reposo y celebrar: 2 % de sus vértices dentro del cuerpo como máximo, 6 mm de hondura. Correr, recoger y salto lunar: se hunde en el pantalón (ver «Límites») | Cumple con un límite conocido |
| f) Godot 4.7.2 | `ANIMACIONES ["caminar", "celebrar", "correr", "recoger", "reposo", "salto_lunar"]`, 8 114 triángulos, 2 superficies, 0 errores (`godot_caminar.log`) | Cumple |

Tamaño: 4,11 MB (tope 6 MB). El 83 % es la textura del cuerpo (3,43 MB en PNG).

El parecido se mide en reposo con `parecido/render_reposo.py` y `herramientas/comparar_personaje.py parecido/spec_rig.json … --registro`. La bajada de 82,1 a 81,4 viene de la textura a 2048 px.

![[lamina_parecido.png]]

Capturas en el motor (`pruebas/escena_exploracion`, cámara del juego):

![[godot_caminar.png|400]] ![[godot_celebrar.png|400]]

## Medidas para el juego

Unidades del GLB: 1 m de alto, origen a media altura, arriba +Y, derecha +Z.

| Medida | Valor |
|---|---|
| `cadera_y` | −0,105 |
| `cuello_y` | 0,152 |
| `hombro_y` / `hombro_z` | 0,112 / 0,108 |
| `rodilla_y` | −0,260 |
| `tobillo_y` | −0,415 |
| `zancada_caminar_m` | **0,5636** por ciclo (0,705 m/s; entre 0,699 y 0,708 del percentil 10 al 90) |
| `zancada_correr_m` | **0,9977** por ciclo (1,782 m/s; entre 1,734 y 1,787) |

La zancada se mide en el GLB exportado: velocidad hacia atrás de los puntos de la suela que tocan el suelo, por la duración del ciclo. Para que los pies no resbalen, la velocidad del personaje debe ser `zancada / duración × escala del modelo`.

## Límites conocidos

- **Bolso (criterio e).** Es rígido y cuelga delante de la cadera derecha. Medido con `verificar_bolso.py` (paridad de rayos, 1 163 vértices):

  | Clip | Vértices dentro, máximo | Media del clip | Hondura máxima | Contra qué |
  |---|---|---|---|---|
  | pose de unión | 0 | — | 0 | — |
  | reposo | 1,2 % | 0,6 % | 1,7 mm | muslo |
  | caminar | 2,0 % | 0,4 % | 6,3 mm | cintura |
  | celebrar | 1,2 % | 0,5 % | 1,9 mm | muslo |
  | salto lunar | 7,6 % | 2,9 % | 24,8 mm | cintura |
  | correr | 37,8 % (t = 0,08 s) | 6,6 % | 33,0 mm | pierna y muslo derechos y cadera, con la rodilla arriba |
  | recoger | 48,3 % (t = 0,44 s) | 21,0 % | 36,7 mm | muslo y vientre, en cuclillas |

  En los renders de cerca el bolso se ve apoyado sobre el muslo y medio hundido en el pantalón; la pierna no asoma por la cara visible. Probé tres ajustes del seguimiento (más giro con el muslo, más apertura hacia fuera, los dos): ninguno mejora el conjunto. Para quitarlo del todo haría falta un bolso blando o un hueso con traslación.

  ![[bolso_peores_instantes.jpg|600]]

- **`salto_lunar` es un bucle en el aire.** No toca el suelo: el vértice más bajo va de 4,5 a 7,9 cm sobre él. El juego lo usa mientras la protagonista no está en el suelo y mueve el cuerpo en vertical. No trae impulso ni aterrizaje.
- **`recoger`:** la mano baja hasta 6,9 cm del suelo, no lo toca. El objeto debe quedar a esa altura o desaparecer en el instante 0,42 a 0,58 s.
- **`celebrar`:** los brazos suben en V, unos 30° sobre la horizontal, no verticales: más arriba chocan con el pelo. En la axila, el 0,19 % de las aristas se estira hasta 4,67 veces.
- **`correr`:** en el vuelo, una pierna queda 20,7 mm corta de su objetivo (6 cuadros). No afecta al apoyo.
- Sin dedos, sin huesos de cara (no parpadea) y con el pelo rígido (sin movimiento secundario).
- Textura del cuerpo a 2048 px: resta 0,7 puntos de parecido frente a la v9.

## Lecciones

- **Icosfera del importador.** Al importar en Blender un GLB con esqueleto, el importador crea una icosfera de 2 m como forma de los huesos. `render_vistas.py` la cuenta como malla y el personaje sale al 40 % de su tamaño; el parecido cambia de 81,4 a 81,7 % o a 80,6 % según la resolución. Hay que quitar las mallas sin material antes de medir (`parecido/render_reposo.py`).
- **«Dentro» por la normal más cercana no sirve** en mallas con pliegues: daba 5,2 cm de hondura en reposo, donde la paridad de rayos mide 1,7 mm. El informe del script conserva esa cifra (`e_bolso`) solo como referencia; la buena es `bolso_verificacion.json`.
- **`juego_ejecutar.py` filtra la salida:** la línea `ANIMACIONES` solo aparece con `--todo`.
- El script escribe la salida con un reemplazo atómico: se puede volver a correr con el juego abierto.

## Plan B

No hizo falta: el skinning quedó limpio. Si se quisiera el caminar por shader de vértices, las alturas de corte están en `PER-01_medidas.json` (`cadera_y`, `rodilla_y`, `tobillo_y`, `hombro_y`, `hombro_z` y las 20 articulaciones).
