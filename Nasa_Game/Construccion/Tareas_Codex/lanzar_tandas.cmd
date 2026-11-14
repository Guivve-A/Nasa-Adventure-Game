@echo off
rem Lanza las dos tandas de minijuegos de Codex, una tras otra. El resultado queda en logs: tanda_a.txt y tanda_b.txt.
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_codex_a.md --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_a.txt 2>&1
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\minijuegos_codex_b.md --paralelo 2 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_b.txt 2>&1
