@echo off
rem Lanza en Codex la tanda de minijuegos arcade (satelite, telescopio, linea_tiempo, muestras, orbita).
rem El resultado queda en logs: tanda_arcade.txt.
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_arcade.md --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_arcade.txt 2>&1
