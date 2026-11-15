# Misión Artemis: Más allá de las páginas

Minijuego 2D de vista lateral en Godot 4.7: la base del polo sur lunar, el viaje y Marte. Es un proyecto de Godot independiente; esta carpeta solo tiene archivos del minijuego.

## Abrirlo

- Doble clic en `jugar.cmd`. Si tu Godot está en otra ruta, define la variable `GODOT_EXE`.
- O abre `project.godot` en el editor de Godot y pulsa F5.

## Controles

| Tecla | Acción |
|---|---|
| ← → o A/D | Moverse |
| Mayús | Correr (gasta más oxígeno) |
| Espacio | Saltar. Otra vez en el aire: impulso de mochila (gasta energía) |
| E | Hablar, recoger, entrar, subir al rover, entregar, despegar |
| Mantener E | Extraer de una veta, orientar un panel, desplegar un módulo |
| F11 | Pantalla completa |

## Qué hay que hacer

1. **Construir el cohete:** lleva cajas, ilmenita y regolito a la constructora del astillero. Son 4 fases.
2. **Preparar el despegue:** lleva 4 de hielo del cráter al depósito y orienta los 3 paneles solares para cargar la batería.
3. **Despegar** desde el cohete.
4. **En Marte (provisional):** planta las 3 banderas y despliega los 3 módulos.

Cuida las cuatro barras. Las cúpulas, el invernadero y el refugio te protegen de la lluvia solar. Si el oxígeno llega a cero o la radiación al máximo, el equipo te lleva a la cúpula y pierdes la mitad de la carga.

## Carpetas

| Carpeta | Contenido |
|---|---|
| `codigo/` | `principal.gd` (capítulos y prueba), `nivel_luna.gd`, `viaje.gd`, `nivel_marte.gd`, `hud.gd`, `fondo_parallax.gd`, `personaje.gd` |
| `datos/` | `nivel_luna.json` (alturas, props y personajes) y `dialogos.json` (se puede editar) |
| `recursos/` | Fondos de la Luna, personajes, props, suelo y la foto de la tercera bandera |
| `hojas_de_referencia/` | Las 5 hojas y su documento, `Hojas de referencia.md` |
| `herramientas/` | `generar_hojas.js`: regenera hojas, props, suelo y `nivel_luna.json` |
| `capturas/` | 14 capturas de la última prueba |

## Conectar los fondos de Marte

Copia los PNG de 640 × 360, repetibles en horizontal, a `recursos/fondos_marte/` con estos nombres:

`capa_0_espacio.png`, `capa_0b_sol_tierra.png`, `capa_1_montanas_lejanas.png`, `capa_2_montanas_medias.png`, `capa_3_colinas_cercanas.png`

Cada capa que exista sustituye a su silueta provisional, sin tocar código. Para el viaje, un `recursos/fondos_viaje/fondo.png` sustituye al cielo de estrellas.

## Probar

```
<Godot> --path "<esta carpeta>" -- --prueba --capturas=<carpeta>
```

Juega solo de principio a fin y comprueba 31 pasos. `--capitulo=marte` o `--capitulo=viaje` abre directamente ese capítulo.

## Pendiente

- Jugarlo a mano y ajustar el equilibrio: las cifras son un punto de partida.
- Marte es provisional: el arte y el diseño final son de Domenica.
- Sin sonido todavía.
- No está conectado al juego principal (`juego/minijuegos/`): hoy corre aparte.
