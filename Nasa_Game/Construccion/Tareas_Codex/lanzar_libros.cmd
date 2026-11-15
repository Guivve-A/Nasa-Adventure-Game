@echo off
rem Integracion de los dos minijuegos de la biblioteca (carpetas de los companeros), en Codex:
rem 1) mapa de los dos proyectos y diseno de la integracion; 2) integracion en juego/minijuegos/base_luna y base_marte.
cd /d "C:\Users\guill\Desktop\Juego 2d-hd"
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\integrar_libros.md --solo libros_mapa --paralelo 1 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_libros_mapa.txt 2>&1
python -I herramientas\codex_lote.py Nasa_Game\Construccion\Tareas_Codex\integrar_libros.md --solo libros_integrar --paralelo 1 > Nasa_Game\Construccion\Tareas_Codex\logs\tanda_libros_integrar.txt 2>&1
