@echo off
rem Zingularity - Artemis a pantalla completa (F11 vuelve a ventana).
rem Si falta la cache de importacion (no deberia), la prepara una sola vez.
setlocal
set "MOTOR=%~dp0motor\ZingularityArtemis.exe"
set "PROYECTO=%~dp0juego"
if not exist "%MOTOR%" goto falta
if not exist "%PROYECTO%\.godot\imported\" goto preparar
goto abrir
:preparar
echo Preparando el juego por primera vez...
"%MOTOR%" --headless --path "%PROYECTO%" --import
:abrir
start "" "%MOTOR%" --path "%PROYECTO%" --fullscreen
exit /b 0
:falta
echo No se encuentra el motor del juego junto a este archivo.
echo Descomprime TODO el archivo ZIP en una carpeta y vuelve a abrir este archivo desde ahi.
pause
exit /b 1
