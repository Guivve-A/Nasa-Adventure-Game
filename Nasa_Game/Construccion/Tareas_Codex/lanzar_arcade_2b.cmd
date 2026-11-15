@echo off
rem Segunda vuelta en Codex tras recuperar el cupo (2026-11-15), parte B:
rem remate a pantalla completa de banderas y regreso (quedaron cortados por el limite de uso).
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_arcade_remate.md --solo remate_banderas,remate_regreso --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda2_remate.txt 2>&1
