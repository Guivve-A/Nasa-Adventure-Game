@echo off
rem Abre el juego jugable v0 (doble clic). Titulo provisional: "Luz cenicienta".
rem Controles: WASD o flechas, Mayus correr, E interactuar, Espacio saltar (en la Luna), Tab cuaderno,
rem Esc pausa, Z y X acercar y alejar, F11 pantalla completa, F12 captura (carpeta capturas).
rem En otro equipo: define la variable GODOT_EXE con la ruta de Godot 4.7.2 (version de consola).
set GODOT=C:\Users\guill\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe
if defined GODOT_EXE set GODOT=%GODOT_EXE%
if not exist "%GODOT%" (
  echo No se encuentra Godot 4.7.2 en "%GODOT%". Define la variable GODOT_EXE con su ruta.
  pause
  exit /b 1
)
if not exist "%~dp0.godot" (
  echo Preparando el proyecto por primera vez...
  "%GODOT%" --headless --path "%~dp0." --import
)
start "" "%GODOT%" --path "%~dp0."
