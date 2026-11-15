@echo off
rem Segunda vuelta en Codex tras recuperar el cupo (2026-11-15), parte A:
rem 1) orbita como arcade a pantalla completa; 2) satelite, telescopio, linea_tiempo y muestras a pantalla completa.
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_arcade.md --solo arcade_orbita --paralelo 1 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda2_orbita.txt 2>&1
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_arcade_completa.md --solo completa_satelite,completa_telescopio,completa_linea_tiempo,completa_muestras --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda2_completa.txt 2>&1
