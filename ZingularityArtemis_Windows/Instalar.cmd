@echo off
rem Instala Zingularity - Artemis para este usuario, sin permisos de administrador.
rem Uso: Instalar.cmd [carpeta de destino] [/sin_accesos] [/sin_preguntas]
rem   Sin carpeta instala en %LOCALAPPDATA%\ZingularityArtemis y crea el acceso directo "Zingularity - Artemis"
rem   en el Escritorio y en el menu Inicio. /sin_accesos no crea accesos directos; /sin_preguntas no pregunta.
rem   Para pruebas: las variables LUZC_ESCRITORIO y LUZC_PROGRAMAS cambian donde van los accesos directos.
setlocal EnableExtensions
set "ORIGEN=%~dp0"
set "ORIGEN=%ORIGEN:~0,-1%"
set "DESTINO=%LOCALAPPDATA%\ZingularityArtemis"
set "ACCESOS=1"
set "PREGUNTAR=1"
:argumentos
if "%~1"=="" goto fin_argumentos
if /i "%~1"=="/sin_accesos" (set "ACCESOS=0" & shift & goto argumentos)
if /i "%~1"=="/sin_preguntas" (set "PREGUNTAR=0" & shift & goto argumentos)
set "DESTINO=%~f1"
shift
goto argumentos
:fin_argumentos
if "%DESTINO:~-1%"=="\" set "DESTINO=%DESTINO:~0,-1%"
echo.
echo   ZINGULARITY: ARTEMIS - instalacion
echo   Desde: %ORIGEN%
echo   Hacia: %DESTINO%
echo.
if not exist "%ORIGEN%\motor\ZingularityArtemis.exe" goto falta_origen
if /i "%ORIGEN%"=="%DESTINO%" goto accesos
if exist "%DESTINO%\motor\ZingularityArtemis.exe" goto copiar
if not exist "%DESTINO%\" goto copiar
for /f "delims=" %%A in ('dir /a /b "%DESTINO%" 2^>nul') do goto ocupado
:copiar
echo   Copiando el juego (unos 350 MB, puede tardar un minuto)...
if not exist "%DESTINO%\" mkdir "%DESTINO%"
if not exist "%DESTINO%\" goto error_copia
robocopy "%ORIGEN%\motor" "%DESTINO%\motor" /MIR /R:2 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto error_copia
robocopy "%ORIGEN%\juego" "%DESTINO%\juego" /MIR /XD capturas /R:2 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto error_copia
if not exist "%DESTINO%\juego\capturas\" mkdir "%DESTINO%\juego\capturas"
copy /y "%ORIGEN%\juego\capturas\.gdignore" "%DESTINO%\juego\capturas\" >nul
robocopy "%ORIGEN%\extras" "%DESTINO%\extras" /MIR /R:2 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto error_copia
robocopy "%ORIGEN%" "%DESTINO%" *.cmd *.txt /XF Instalar.cmd /R:2 /W:1 /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto error_copia
:accesos
if "%ACCESOS%"=="0" goto listo
echo   Creando los accesos directos del Escritorio y del menu Inicio...
set "LUZC_EXE=%DESTINO%\motor\ZingularityArtemis.exe"
set "LUZC_JUEGO=%DESTINO%\juego"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $e=$env:LUZC_ESCRITORIO; if(-not $e){$e=[Environment]::GetFolderPath('Desktop')}; $p=$env:LUZC_PROGRAMAS; if(-not $p){$p=[Environment]::GetFolderPath('Programs')}; foreach($d in @($e,$p)){ $s=$w.CreateShortcut((Join-Path $d 'Zingularity - Artemis.lnk')); $s.TargetPath=$env:LUZC_EXE; $s.Arguments='--path '+[char]34+$env:LUZC_JUEGO+[char]34; $s.WorkingDirectory=$env:LUZC_JUEGO; $s.IconLocation=$env:LUZC_EXE+',0'; $s.Description='Zingularity - Artemis: aventura espacial'; $s.Save() }"
if errorlevel 1 echo   Aviso: no se pudieron crear los accesos directos. Puedes jugar con Jugar.cmd de la carpeta instalada.
:listo
echo.
echo   Listo. Zingularity - Artemis quedo instalado en:
echo     %DESTINO%
echo   Para jugar: acceso directo "Zingularity - Artemis" (Escritorio o menu Inicio) o Jugar.cmd de esa carpeta.
echo   Para quitarlo: Desinstalar.cmd de esa carpeta.
echo.
if "%PREGUNTAR%"=="0" exit /b 0
set "RESP="
set /p "RESP=  Quieres abrir el juego ahora? (S/N): "
if /i "%RESP%"=="S" start "" "%DESTINO%\motor\ZingularityArtemis.exe" --path "%DESTINO%\juego"
exit /b 0
:ocupado
echo   La carpeta de destino ya existe, tiene archivos y no es una instalacion de Zingularity - Artemis.
echo   Elige otra carpeta vacia. No se copio nada.
goto error
:falta_origen
echo   No se encuentra el juego junto a este archivo.
echo   Descomprime TODO el archivo ZIP en una carpeta y vuelve a abrir Instalar.cmd desde ahi.
goto error
:error_copia
echo   No se pudo copiar el juego a la carpeta de destino. Revisa el espacio libre en el disco.
:error
if "%PREGUNTAR%"=="1" pause
exit /b 1
