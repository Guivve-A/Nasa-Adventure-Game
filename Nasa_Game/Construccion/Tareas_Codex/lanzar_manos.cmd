@echo off
rem Lanza la tanda de pruebas de manos de los 9 minijuegos en Codex. El resultado queda en logs: tanda_manos.txt.
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_manos.md --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_manos.txt 2>&1
