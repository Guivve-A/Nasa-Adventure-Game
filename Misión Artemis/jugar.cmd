@echo off
rem Abre Mision Artemis. Define GODOT_EXE con la ruta de Godot 4.7 si no es esta.
set GODOT=C:\Users\Jcarl\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe
if defined GODOT_EXE set GODOT=%GODOT_EXE%
start "" "%GODOT%" --path "%~dp0."
