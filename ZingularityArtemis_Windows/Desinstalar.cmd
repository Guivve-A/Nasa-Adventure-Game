@echo off
rem Desinstala Zingularity - Artemis: borra la carpeta instalada y los accesos directos "Zingularity - Artemis".
rem Uso: Desinstalar.cmd [carpeta instalada] [/sin_accesos] [/sin_preguntas]
rem   Sin carpeta: la carpeta de este archivo si es una instalacion (no tiene Instalar.cmd); si no,
rem   %LOCALAPPDATA%\ZingularityArtemis. La partida guardada vive aparte, en
rem   %APPDATA%\ZingularityArtemis, y solo se borra si se confirma (nunca con /sin_preguntas).
rem   Para pruebas: las variables LUZC_ESCRITORIO y LUZC_PROGRAMAS cambian donde se buscan los accesos directos.
setlocal EnableExtensions
rem Se guardan antes de leer los argumentos: shift tambien desplaza %0.
set "AQUI=%~dp0"
set "YO=%~f0"
set "YO_NOMBRE=%~nx0"
set "DESTINO="
set "ACCESOS=1"
set "PREGUNTAR=1"
set "OPCIONES="
:argumentos
if "%~1"=="" goto fin_argumentos
if /i "%~1"=="/sin_accesos" (set "ACCESOS=0" & set "OPCIONES=%OPCIONES% /sin_accesos" & shift & goto argumentos)
if /i "%~1"=="/sin_preguntas" (set "PREGUNTAR=0" & set "OPCIONES=%OPCIONES% /sin_preguntas" & shift & goto argumentos)
set "DESTINO=%~f1"
shift
goto argumentos
:fin_argumentos
if defined DESTINO goto con_destino
set "DESTINO=%LOCALAPPDATA%\ZingularityArtemis"
if not exist "%AQUI%motor\ZingularityArtemis.exe" goto con_destino
if exist "%AQUI%Instalar.cmd" goto con_destino
set "DESTINO=%AQUI%"
:con_destino
if "%DESTINO:~-1%"=="\" set "DESTINO=%DESTINO:~0,-1%"
rem Si este archivo esta dentro de la carpeta que se borra, sigue desde una copia en la carpeta temporal.
if /i not "%AQUI%"=="%DESTINO%\" goto fuera
copy /y "%YO%" "%TEMP%\ZingularityArtemis_desinstalar.cmd" >nul
cd /d "%TEMP%"
"%TEMP%\ZingularityArtemis_desinstalar.cmd" "%DESTINO%"%OPCIONES%
:fuera
set "PARTIDA=%APPDATA%\ZingularityArtemis"
echo.
echo   ZINGULARITY: ARTEMIS - desinstalacion
echo   Carpeta: %DESTINO%
echo.
if not exist "%DESTINO%\motor\ZingularityArtemis.exe" goto no_instalado
if "%PREGUNTAR%"=="0" goto quitar_accesos
set "RESP="
set /p "RESP=  Se borrara esa carpeta. Continuar? (S/N): "
if /i not "%RESP%"=="S" goto cancelado
:quitar_accesos
if "%ACCESOS%"=="0" goto partida
powershell -NoProfile -ExecutionPolicy Bypass -Command "$e=$env:LUZC_ESCRITORIO; if(-not $e){$e=[Environment]::GetFolderPath('Desktop')}; $p=$env:LUZC_PROGRAMAS; if(-not $p){$p=[Environment]::GetFolderPath('Programs')}; foreach($d in @($e,$p)){ $l=Join-Path $d 'Zingularity - Artemis.lnk'; if(Test-Path -LiteralPath $l){ Remove-Item -LiteralPath $l -Force } }"
:partida
if "%PREGUNTAR%"=="0" goto borrar
if not exist "%PARTIDA%\" goto borrar
set "RESP="
set /p "RESP=  Borrar tambien la partida guardada? Se pierde el avance (S/N): "
if /i "%RESP%"=="S" rmdir /s /q "%PARTIDA%"
:borrar
cd /d "%TEMP%"
rmdir /s /q "%DESTINO%"
if exist "%DESTINO%\" goto no_borrado
echo   Zingularity - Artemis quedo desinstalado.
goto fin
:no_borrado
echo   No se pudo borrar todo: cierra el juego si esta abierto y vuelve a intentarlo.
goto fin
:no_instalado
echo   No hay una instalacion de Zingularity - Artemis en esa carpeta. No se borro nada.
goto fin
:cancelado
echo   Cancelado. No se borro nada.
:fin
if "%PREGUNTAR%"=="1" pause
if /i not "%YO_NOMBRE%"=="ZingularityArtemis_desinstalar.cmd" exit /b 0
(goto) 2>nul & del "%YO%"
