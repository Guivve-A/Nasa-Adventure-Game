# Jugar en el navegador

Exportaciones web (HTML5 + WebAssembly) de los dos juegos 2D de la biblioteca, para jugarlos desde la landing sin descargar nada. La landing las abre en un marco a pantalla completa con botón «Volver» (sección «Jugar en el navegador» de `index.html`); cada una funciona también sola en `/jugar/<id>/`.

| Id | Juego | Origen (solo lectura) | Estado |
|---|---|---|---|
| `base-luna` | Misión Artemis: la base lunar (Luna, viaje y Marte provisional) | `Misión Artemis/` | ESTADO_BASE_LUNA |
| `marte` | Misión Artemis: Marte | `Marte_Gravedad2DHD/Marte_Gravedad2DHD/Mision_Artemis_Marte/` | ESTADO_MARTE |
| — | El mundo 3D de Guayaquil (`juego/`) | — | No se exporta: ver abajo |

Cada carpeta lleva `index.html`, `index.js`, `index.wasm`, `index.pck`, `index.audio.worklet.js` y los iconos. Vercel limita cada archivo a 100 MB; el más grande es `index.wasm`, de unos 36 MB.

## Cómo se generan (pasos repetibles)

1. **Plantillas web de Godot 4.7.2**, una sola vez por equipo:
   - Bajar `Godot_v4.7.2-stable_export_templates.tpz` y `SHA512-SUMS.txt` del release oficial: `https://github.com/godotengine/godot/releases/tag/4.7.2-stable`.
   - Comprobar el SHA-512 del `.tpz` contra `SHA512-SUMS.txt`.
   - Copiar de `templates/` solo `version.txt`, `web_nothreads_release.zip` y `web_nothreads_debug.zip` a `%APPDATA%\Godot\export_templates\4.7.2.stable\`.
2. **Exportar**, desde la raíz del repositorio:

   ```
   python -I herramientas/exportar_web.py            # los dos
   python -I herramientas/exportar_web.py marte      # uno
   ```

   El script:
   - copia `codigo/`, `datos/`, `escenas/`, `recursos/` y `project.godot` de cada juego a `web_build/<id>/` (carpeta ignorada por Git); las carpetas de los compañeros no se tocan;
   - en la copia cambia el renderizador a `gl_compatibility` (Mobile no existe en web) y escribe un `export_presets.cfg` con el preset «Web»: sin hilos (no exige las cabeceras COOP y COEP), lienzo adaptable, `*.json` incluido y `<base href="/jugar/<id>/">`, para que los archivos carguen aunque Vercel sirva la página como `/jugar/<id>` sin barra final;
   - corre Godot sin ventana (`--import` y `--export-release "Web"`), de uno en uno con el candado de `herramientas/juego_ejecutar.py`;
   - deja el resultado en `landing/jugar/<id>/` y avisa si algún archivo supera 100 MB.
3. **Probar** antes de publicar:

   ```
   python -m http.server 4173 --directory landing
   ```

   Abrir `http://localhost:4173/jugar/<id>/` en un navegador de escritorio, o la landing y su botón «Jugar ahora». La prueba sin cabeza que se usó está descrita abajo.

Si los compañeros cambian su juego, basta con repetir el paso 2.

## Prueba hecha

PRUEBA_PENDIENTE

## El mundo 3D (`juego/`) en el navegador

MUNDO_3D_PENDIENTE
