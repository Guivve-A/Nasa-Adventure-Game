@@TAREA

Proyecto: RPG low-poly en Godot 4.7.2. Guillermo pidio que la protagonista (PER-01) se parezca al menos en un 80 % a su hoja de referencia. Hay una metrica: `herramientas/comparar_personaje.py` (silueta IoU, color dE76 y SSIM multiescala, por vista; frente y cabeza pesan doble). La malla actual (v2) mide 62,2 %.

Datos:
- Malla v2: `Nasa_Game/Fase_1_Arte/Modelado/Lote_04/L04_PER01_giro_tripo_mv.glb` (Tripo H3.1, 7 522 triangulos, una textura JPEG de 4096 px). En glTF mira a +X, arriba es +Y y mide 1,0 m de alto, centrada en el origen (y de -0,5 a 0,5). El lado derecho del personaje es +Z (lleva el reloj en la muneca izquierda, -Z).
- Hoja de referencia: `Nasa_Game/Fase_1_Arte/Exploracion/Lote_02/L02_protagonista_tipo1_hoja.png` (2688x1520, fondo gris liso). Cajas de las vistas: frente [200,10,720,923]; perfil derecho (la figura mira a la derecha de la imagen) [1410,10,1790,923]; espalda [1960,10,2450,923]. La linea de suelo esta en las filas 924 a 928 (no incluirla). En la hoja hay un bolso con herramientas en la cadera derecha y una correa cruzada que la malla no tiene: no importa, se pinta en la textura.
- Render sin luz para medir: `"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup --python-exit-code 1 --python herramientas/blender/render_vistas.py -- --glb <malla.glb> --salida <carpeta> --lado 1000`. Con esta malla: px_cuerpo = frente, my_cuerpo = perfil derecho, mx_cuerpo = espalda.
- Medicion: `python -I herramientas/comparar_personaje.py Nasa_Game/Fase_1_Arte/Modelado/Lote_04/parecido/spec_v2.json <lamina.png>` (copia el spec y cambia las rutas de render a tu carpeta).

Reglas: comentarios del codigo en espanol y sin tildes. No instales nada. No gastes creditos. No toques los archivos de otras tareas ni la escena de Godot. Responde en espanol con: que hiciste, cifras antes y despues por vista, ruta de los archivos y lo que no pudiste comprobar.

@@TAREA id=proyectar_hoja salida=Nasa_Game/Fase_1_Arte/Modelado/Tareas_Codex/informes/proyectar_hoja.md sandbox=workspace-write timeout=45 esfuerzo=high

Escribe `herramientas/mallas/proyectar_hoja.py`, que repinte la textura de la malla v2 con las vistas de la hoja y guarde `Nasa_Game/Fase_1_Arte/Modelado/Lote_04/L04_PER01_v3_hoja.glb` (misma geometria y UV; solo cambia la imagen). Requisitos:
1. Proyeccion ortografica por vista (frente desde +X, espalda desde -X, perfil derecho desde +Z). El lado izquierdo (-Z) conserva la textura de Tripo.
2. Alineacion por silueta: rasteriza la silueta de la malla en cada vista y busca la escala (±8 %) y el desplazamiento (±6 % del tamano de la figura) que maximizan el IoU con la mascara de la hoja. La caja de la hoja incluye el bolso, asi que no alinees por la caja.
3. Visibilidad con bufer de profundidad: un texel solo toma color de una vista si es la superficie visible desde ella (sin pintar el brazo con el torso de atras, ni la cara interna de las piernas).
4. Peso por texel = visible × max(0, n·d)^3 × (dentro de la mascara de la hoja erosionada 3 px). Mezcla con la textura original: color = (suma de peso_v × hoja_v + 0,15 × original) / (suma de peso_v + 0,15). Nunca tomes color del fondo de la hoja.
5. Rellena los bordes de las islas UV (como `herramientas/mallas/proyectar_vistas.py`) para que no aparezcan costuras.
6. Comprueba y pon en el informe:
   - el parecido antes (62,2 %) y despues, por vista, con la metrica;
   - el % de texels que tomaron color de la hoja;
   - el % de esos que cayeron sobre el fondo (debe ser casi 0);
   - un primer plano de la cara de frente (`px_cabeza.png`) junto al de la hoja.
   Si la textura nueva baja el parecido de alguna vista, dilo y explica por que.
