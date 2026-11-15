# Zingularity: Artemis — landing

Página estática de descarga del juego. No tiene paso de compilación: Vercel la sirve tal cual.

Estilo: el del sitio de NASA Space Apps (Fira Sans pesada, azul en degradado, un solo acento amarillo), sin su logotipo ni su insignia.

| Archivo | Para qué |
|---|---|
| `index.html` | Portada, «El juego» (15 capturas en 4 pestañas), «Datos y recursos» y descarga |
| `estilos.css` | Estilos |
| `app.js` | Enlaces de descarga, insignia, pestañas, visor y animaciones |
| `capturas/` | Las 15 capturas del juego (1600 px de ancho, 4,05 MB en total) |
| `vercel.json` | URL limpias y caché de un año para las capturas |

## Animaciones

GSAP 3.12.5 y ScrollTrigger, cargados desde cdnjs. Si no cargan, la página funciona igual, sin animación.

- Entrada de la portada: el título sube palabra a palabra y la insignia aparece con rebote.
- Insignia: cambia entre Guayaquil, la Luna y Marte (sola cada 4,8 s o con sus tres botones) y se inclina siguiendo al puntero.
- Al bajar: títulos, pestañas, capturas y columnas aparecen escalonados; una línea amarilla bajo la barra marca el avance.
- Pestañas y visor: las capturas entran escalonadas; el visor pasa de una a otra con las flechas del teclado o sus botones.
- Con «reducir movimiento» activado en el sistema quedan solo fundidos: sin desplazamientos, giros ni cambio automático.

## Verla en local

```
python -m http.server 4173 --directory zingularity-artemis
```

Se abre en `http://localhost:4173`.

## Publicar en Vercel

- Nombre del proyecto: `zingularity-artemis`, que da la URL `https://zingularity-artemis.vercel.app` (libre al 2026-11-15). Una URL no admite los dos puntos ni el espacio de «Zingularity: Artemis»; el nombre completo va en el título de la página.
- Directorio raíz del proyecto: esta carpeta. Framework: «Other». Sin comando de build ni carpeta de salida.

## El botón de descarga

Los dos enlaces se cambian en un solo sitio: el objeto `DESCARGAS` al inicio de `app.js`.

El botón de Windows apunta a
`https://github.com/Guivve-A/Nasa-Adventure-Game/releases/latest/download/Zingularity-Artemis-Windows.zip`.
Funciona cuando exista un *release* en GitHub con un archivo llamado exactamente `Zingularity-Artemis-Windows.zip`. Al 2026-11-15 el repositorio no tiene ningún release: hasta entonces el botón lleva a una página 404 de GitHub.

No sirve enlazar el ZIP del código («Download ZIP»): trae punteros de Git LFS en lugar de las imágenes, los modelos y el audio.

## Recursos enlazados

Los de «Dentro del juego» constan en el repositorio (`Nasa_Game/Propuestas/Datos/descargas_nasa.json`). Los de los dos retos salen de sus pestañas de recursos, leídas el 2026-11-15:

- `spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources`
- `spaceappschallenge.org/2026/challenges/interplanetary-survival-guide-martian-map/?tab=resources`
