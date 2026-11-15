@echo off
rem 1) Remate en Codex de los cuatro minijuegos arcade ya reescritos (seguidor, antena, banderas, regreso),
rem    con el campo a pantalla completa. Resultado: logs\tanda_arcade_remate.txt.
rem 2) Espera a que termine la tanda que rehace los otros cinco (logs\tanda_arcade.txt con sus 5 lineas)
rem    y los amplia a pantalla completa. Resultado: logs\tanda_arcade_completa.txt.
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_arcade_remate.md --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_arcade_remate.txt 2>&1
:esperar
find /c " min " Nasa_Game\Construccion\Tareas_Codex\logs\tanda_arcade.txt | find ": 5" >nul
if errorlevel 1 (
  ping -n 61 127.0.0.1 >nul
  goto esperar
)
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_arcade_completa.md --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_arcade_completa.txt 2>&1
