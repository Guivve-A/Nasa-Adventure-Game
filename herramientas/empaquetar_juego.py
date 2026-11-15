"""Arma el paquete portable de Windows de "Luz cenicienta": motor + copia del proyecto + lanzadores + LEEME + ZIP.

Decision tecnica: no hay plantillas de exportacion y el juego carga por codigo archivos sueltos (json, glb en
carpetas con .gdignore, guiones por ruta). Por eso el paquete NO es un .pck: lleva el ejecutable oficial de
Godot 4.7.2 (licencia MIT) renombrado y una copia del proyecto con su cache de importacion, y arranca con
--path, igual que en desarrollo.

Uso (desde la raiz del repositorio):
  python -I herramientas/empaquetar_juego.py              arma entrega/LuzCenicienta_Windows/ y su ZIP
  python -I herramientas/empaquetar_juego.py --sin-zip    solo la carpeta
  python -I herramientas/empaquetar_juego.py --solo-zip   rehace solo el ZIP de la carpeta ya armada
  python -I herramientas/empaquetar_juego.py --sin-importar   no pasa "--import" sobre las copias

No toca juego/ ni las carpetas de los companeros: solo las copia. La importacion de comprobacion se hace sobre
la COPIA, con el motor del paquete y bajo el candado global de Godot (herramientas/juego_ejecutar.py).
"""
import hashlib
import importlib.util
import os
import re
import shutil
import sys
import time
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
HERRAMIENTAS = RAIZ / "herramientas"
ENTREGA = RAIZ / "entrega"
NOMBRE = "LuzCenicienta_Windows"
PAQUETE = ENTREGA / NOMBRE
ZIP = ENTREGA / (NOMBRE + ".zip")
JUEGO = RAIZ / "juego"
ARTEMIS = RAIZ / "Misión Artemis"
MARTE = RAIZ / "Marte_Gravedad2DHD" / "Marte_Gravedad2DHD" / "Mision_Artemis_Marte"
EXE = "LuzCenicienta.exe"
EXE_CONSOLA = "LuzCenicienta_console.exe"

# Se excluye en cualquier carpeta
NOMBRES_FUERA = {"__pycache__", ".git", ".gitignore", ".gitattributes", "Thumbs.db", "desktop.ini", ".DS_Store",
                 ".candado_godot"}
SUFIJOS_FUERA = (".log", ".tmp", ".blend", ".blend1", ".pyc")
# Se excluye por ruta relativa a cada proyecto
FUERA_JUEGO = {"jugar.cmd", "capturas", ".godot/editor", ".godot/shader_cache"}
FUERA_ARTEMIS = {"capturas", "hojas_de_referencia", "herramientas", "Hojas de referencia.md", "jugar.cmd",
                 ".godot/editor", ".godot/shader_cache"}
FUERA_MARTE = {"herramientas", "jugar.cmd", ".godot/editor", ".godot/shader_cache"}

# Busqueda de datos personales
NOMBRES_PERMITIDOS = ["Guillermo"]  # el director aparece en los creditos y en comentarios del codigo
EXT_TEXTO = {".gd", ".gdshader", ".gdshaderinc", ".json", ".md", ".txt", ".cmd", ".cfg", ".godot", ".tscn", ".tres",
             ".import", ".uid", ".md5", ".csv", ".ini"}
CORREO = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
RUTA_USUARIO = re.compile(rb"(?i)[a-z]:[\\/]+(users|usuarios|documents and settings)[\\/]+")


def cargar_ejecutor():
    """Reutiliza de juego_ejecutar.py la ruta de Godot, el candado global y la ejecucion con tiempo maximo."""
    spec = importlib.util.spec_from_file_location("juego_ejecutar", HERRAMIENTAS / "juego_ejecutar.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def ignorador(origen, fuera):
    origen = Path(origen)

    def ignorar(carpeta, nombres):
        rel_dir = Path(carpeta).relative_to(origen).as_posix()
        quitar = []
        for n in nombres:
            rel = n if rel_dir == "." else f"{rel_dir}/{n}"
            if rel in fuera or n in NOMBRES_FUERA or n.lower().endswith(SUFIJOS_FUERA):
                quitar.append(n)
        return quitar

    return ignorar


def copiar_proyecto(origen, destino, fuera):
    if not (origen / "project.godot").exists():
        raise SystemExit(f"No es un proyecto de Godot: {origen}")
    shutil.copytree(origen, destino, ignore=ignorador(origen, fuera))
    archivos = [p for p in destino.rglob("*") if p.is_file()]
    print(f"  {destino.relative_to(PAQUETE)}: {len(archivos)} archivos, "
          f"{sum(p.stat().st_size for p in archivos) / 1e6:.1f} MB", flush=True)


def limpiar_cache_editor(proyecto):
    for sub in ("editor", "shader_cache"):
        p = proyecto / ".godot" / sub
        if p.exists():
            shutil.rmtree(p)


def importar(ejecutor, proyecto):
    """Pasa --import sobre la COPIA con el motor del paquete: rehace lo que falte de la cache sin tocar el origen."""
    consola = str(PAQUETE / "motor" / EXE_CONSOLA)
    ejecutor.tomar_candado()
    try:
        r, e, t = ejecutor.correr([consola, "--headless", "--path", str(proyecto), "--import"], 400.0, False,
                                  ("FIN_NUNCA",))
    finally:
        ejecutor.soltar_candado()
    limpiar_cache_editor(proyecto)
    print(f"  importar {proyecto.relative_to(PAQUETE)}: {r}, {t:.0f} s, avisos de error={e['errores']}", flush=True)


def escribir_cmd(ruta, texto):
    datos = texto.strip("\n").replace("\r\n", "\n").replace("\n", "\r\n") + "\r\n"
    ruta.write_bytes(datos.encode("ascii"))  # falla si se cuela una tilde


def escribir_texto(ruta, texto, bom=True):
    datos = texto.strip("\n").replace("\r\n", "\n").replace("\n", "\r\n") + "\r\n"
    ruta.write_bytes(datos.encode("utf-8-sig" if bom else "ascii"))


# ---------------------------------------------------------------------------------------------- lanzadores

LANZADOR = r"""
@echo off
rem {comentario}
rem Si falta la cache de importacion (no deberia), la prepara una sola vez.
setlocal
set "MOTOR=%~dp0motor\LuzCenicienta.exe"
set "PROYECTO=%~dp0{proyecto}"
if not exist "%MOTOR%" goto falta
if not exist "%PROYECTO%\.godot\imported\" goto preparar
goto abrir
:preparar
echo Preparando el juego por primera vez...
"%MOTOR%" --headless --path "%PROYECTO%" --import
:abrir
start "" "%MOTOR%" --path "%PROYECTO%"{extra}
exit /b 0
:falta
echo No se encuentra el motor del juego junto a este archivo.
echo Descomprime TODO el archivo ZIP en una carpeta y vuelve a abrir este archivo desde ahi.
pause
exit /b 1
"""

INSTALAR = r"""
@echo off
rem Instala Luz cenicienta para este usuario, sin permisos de administrador.
rem Uso: Instalar.cmd [carpeta de destino] [/sin_accesos] [/sin_preguntas]
rem   Sin carpeta instala en %LOCALAPPDATA%\LuzCenicienta y crea el acceso directo "Luz cenicienta"
rem   en el Escritorio y en el menu Inicio. /sin_accesos no crea accesos directos; /sin_preguntas no pregunta.
rem   Para pruebas: las variables LUZC_ESCRITORIO y LUZC_PROGRAMAS cambian donde van los accesos directos.
setlocal EnableExtensions
set "ORIGEN=%~dp0"
set "ORIGEN=%ORIGEN:~0,-1%"
set "DESTINO=%LOCALAPPDATA%\LuzCenicienta"
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
echo   LUZ CENICIENTA - instalacion
echo   Desde: %ORIGEN%
echo   Hacia: %DESTINO%
echo.
if not exist "%ORIGEN%\motor\LuzCenicienta.exe" goto falta_origen
if /i "%ORIGEN%"=="%DESTINO%" goto accesos
if exist "%DESTINO%\motor\LuzCenicienta.exe" goto copiar
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
set "LUZC_EXE=%DESTINO%\motor\LuzCenicienta.exe"
set "LUZC_JUEGO=%DESTINO%\juego"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $e=$env:LUZC_ESCRITORIO; if(-not $e){$e=[Environment]::GetFolderPath('Desktop')}; $p=$env:LUZC_PROGRAMAS; if(-not $p){$p=[Environment]::GetFolderPath('Programs')}; foreach($d in @($e,$p)){ $s=$w.CreateShortcut((Join-Path $d 'Luz cenicienta.lnk')); $s.TargetPath=$env:LUZC_EXE; $s.Arguments='--path '+[char]34+$env:LUZC_JUEGO+[char]34; $s.WorkingDirectory=$env:LUZC_JUEGO; $s.IconLocation=$env:LUZC_EXE+',0'; $s.Description='Luz cenicienta: aventura espacial'; $s.Save() }"
if errorlevel 1 echo   Aviso: no se pudieron crear los accesos directos. Puedes jugar con Jugar.cmd de la carpeta instalada.
:listo
echo.
echo   Listo. Luz cenicienta quedo instalado en:
echo     %DESTINO%
echo   Para jugar: acceso directo "Luz cenicienta" (Escritorio o menu Inicio) o Jugar.cmd de esa carpeta.
echo   Para quitarlo: Desinstalar.cmd de esa carpeta.
echo.
if "%PREGUNTAR%"=="0" exit /b 0
set "RESP="
set /p "RESP=  Quieres abrir el juego ahora? (S/N): "
if /i "%RESP%"=="S" start "" "%DESTINO%\motor\LuzCenicienta.exe" --path "%DESTINO%\juego"
exit /b 0
:ocupado
echo   La carpeta de destino ya existe, tiene archivos y no es una instalacion de Luz cenicienta.
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
"""

DESINSTALAR = r"""
@echo off
rem Desinstala Luz cenicienta: borra la carpeta instalada y los accesos directos "Luz cenicienta".
rem Uso: Desinstalar.cmd [carpeta instalada] [/sin_accesos] [/sin_preguntas]
rem   Sin carpeta: la carpeta de este archivo si es una instalacion (no tiene Instalar.cmd); si no,
rem   %LOCALAPPDATA%\LuzCenicienta. La partida guardada vive aparte, en
rem   %APPDATA%\Godot\app_userdata\Luz cenicienta, y solo se borra si se confirma (nunca con /sin_preguntas).
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
set "DESTINO=%LOCALAPPDATA%\LuzCenicienta"
if not exist "%AQUI%motor\LuzCenicienta.exe" goto con_destino
if exist "%AQUI%Instalar.cmd" goto con_destino
set "DESTINO=%AQUI%"
:con_destino
if "%DESTINO:~-1%"=="\" set "DESTINO=%DESTINO:~0,-1%"
rem Si este archivo esta dentro de la carpeta que se borra, sigue desde una copia en la carpeta temporal.
if /i not "%AQUI%"=="%DESTINO%\" goto fuera
copy /y "%YO%" "%TEMP%\LuzCenicienta_desinstalar.cmd" >nul
cd /d "%TEMP%"
"%TEMP%\LuzCenicienta_desinstalar.cmd" "%DESTINO%"%OPCIONES%
:fuera
set "PARTIDA=%APPDATA%\Godot\app_userdata\Luz cenicienta"
echo.
echo   LUZ CENICIENTA - desinstalacion
echo   Carpeta: %DESTINO%
echo.
if not exist "%DESTINO%\motor\LuzCenicienta.exe" goto no_instalado
if "%PREGUNTAR%"=="0" goto quitar_accesos
set "RESP="
set /p "RESP=  Se borrara esa carpeta. Continuar? (S/N): "
if /i not "%RESP%"=="S" goto cancelado
:quitar_accesos
if "%ACCESOS%"=="0" goto partida
powershell -NoProfile -ExecutionPolicy Bypass -Command "$e=$env:LUZC_ESCRITORIO; if(-not $e){$e=[Environment]::GetFolderPath('Desktop')}; $p=$env:LUZC_PROGRAMAS; if(-not $p){$p=[Environment]::GetFolderPath('Programs')}; foreach($d in @($e,$p)){ $l=Join-Path $d 'Luz cenicienta.lnk'; if(Test-Path -LiteralPath $l){ Remove-Item -LiteralPath $l -Force } }"
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
echo   Luz cenicienta quedo desinstalado.
goto fin
:no_borrado
echo   No se pudo borrar todo: cierra el juego si esta abierto y vuelve a intentarlo.
goto fin
:no_instalado
echo   No hay una instalacion de Luz cenicienta en esa carpeta. No se borro nada.
goto fin
:cancelado
echo   Cancelado. No se borro nada.
:fin
if "%PREGUNTAR%"=="1" pause
if /i not "%YO_NOMBRE%"=="LuzCenicienta_desinstalar.cmd" exit /b 0
(goto) 2>nul & del "%YO%"
"""

LICENCIA = """
motor/LuzCenicienta.exe es Godot Engine 4.7.2-stable para Windows de 64 bits, el ejecutable oficial sin
modificar, solo renombrado. motor/LuzCenicienta_console.exe es su envoltorio de consola oficial (abre el mismo
motor y muestra sus mensajes: sirve para diagnosticar). Godot Engine se distribuye con la licencia MIT:

----------------------------------------------------------------------------------------------------------
Copyright (c) 2014-present Godot Engine contributors.
Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
----------------------------------------------------------------------------------------------------------

Componentes de terceros: el motor incluye bibliotecas de terceros (por ejemplo FreeType, ENet, mbedTLS, HarfBuzz,
Vulkan y otras), cada una con su propia licencia, compatibles con la redistribucion. La lista completa y sus
textos estan en https://godotengine.org/license y en el archivo COPYRIGHT.txt del codigo fuente de Godot.
"""

LEEME = """
LUZ CENICIENTA  -  aventura espacial educativa (version de prueba, 2026-11-15)
=============================================================================

Una estudiante de ingenieria de control de Guayaquil sigue su sueno de llegar a la NASA, con Orbita, su gato
cientifico. Exploras Las Escalinatas, el sendero y el Mirador del Faro, juegas minijuegos de estilo arcade sobre
satelites, antenas y telescopios, y en un sueno caminas por la Luna. Cada dato espacial del juego es real.


REQUISITOS
----------
- Windows 10 u 11 de 64 bits.
- Tarjeta grafica compatible con Vulkan (casi todas las de 2016 en adelante; tambien las integradas Intel HD).
  Probado en un portatil con Intel HD Graphics 620 y 8 GB de RAM.
- Unos 350 MB libres en el disco. No hace falta instalar Godot ni nada mas.


COMO JUGAR
----------
Primero descomprime TODO el ZIP (clic derecho > Extraer todo). Despues, una de dos:

  A) Instalarlo:   doble clic en Instalar.cmd
                   Lo copia en tu usuario (no pide permisos de administrador) y crea el acceso directo
                   "Luz cenicienta" en el Escritorio y en el menu Inicio. Al final te ofrece abrirlo.
                   Para quitarlo: Desinstalar.cmd (en la carpeta instalada o en esta).

  B) Sin instalar:  doble clic en Jugar.cmd   (o en "Jugar en pantalla completa.cmd")

Aviso de Windows SmartScreen: como es un programa sin firma digital, Windows puede mostrar
"Windows protegio su PC". Pulsa "Mas informacion" y despues "Ejecutar de todas formas".

La partida se guarda sola en %APPDATA%\\Godot\\app_userdata\\Luz cenicienta


CONTROLES
---------
  Moverse ................ W A S D  o  flechas
  Correr ................. Mayus (mantener)
  Interactuar / hablar ... E  o  Intro
  Saltar ................. Espacio
  Mapa del mundo ......... M
  Minimapa ............... N
  Cuaderno ............... Tab  o  C
  Pausa .................. Esc  (o P)
  Acercar / alejar ....... Z  y  X  (o Re Pag / Av Pag)
  Pantalla completa ...... F11
  Captura de pantalla .... F12 (se guarda en la carpeta juego\\capturas)
  Mando (gamepad) ........ tambien funciona: palanca o cruceta, A interactuar, X saltar, Y cuaderno,
                           Start pausa, B o gatillo derecho correr
Cada minijuego explica sus controles en su tarjeta de inicio.


QUE PARTES SON PROVISIONALES
----------------------------
Es una version jugable de trabajo: la historia se juega de principio a fin, pero parte del arte aun no tiene
su version final.
  - El sendero del arroyo ........ aprobado.
  - La habitacion-taller ......... concepto aprobado; su version en el juego espera revision.
  - La Plaza de las Iguanas y la biblioteca, el Mirador del Faro y la Luna del sueno: PROVISIONALES
    (construidos con el estilo aprobado, sin concepto final). La pantalla de carga lo indica.
  - Los dos juegos de la biblioteca (Mision Artemis en la Luna y en Marte) todavia NO estan integrados
    dentro del juego principal: se juegan aparte, como extras (ver abajo).
  - Las mallas de los vecinos de la plaza y parte del sonido estan pendientes.


EXTRAS: LOS JUEGOS DE LA BIBLIOTECA
-----------------------------------
Hechos por los companeros del equipo, en pixel-art 2D. Usan el mismo motor:
  - "Jugar extra - Mision Artemis (Luna).cmd": base en el polo sur lunar, construir el cohete y despegar.
  - "Jugar extra - Mision Artemis (Marte).cmd": aterrizaje, banderas, base, tormenta de polvo y noche en Marte.
  Controles: flechas o A/D moverse, Mayus correr, Espacio saltar, E usar (mantener E para extraer o
  desplegar), Tab cuaderno (Marte), F11 pantalla completa. Mas detalle en el LEEME.md de cada carpeta de extras.


CREDITOS
--------
  Direccion, diseno y desarrollo ........ Guillermo
  Juegos de la biblioteca (Luna y Marte) .. Jean, Joel y Domenica
  Guayaquil, Ecuador.

  Datos abiertos de la NASA: mapas de la Luna del Lunar Reconnaissance Orbiter (LRO) y efemerides de
  JPL Horizons. No se usan logotipos ni insignias de la NASA y el juego no esta respaldado por ella.
  Las fuentes de cada dato del cuaderno estan en juego\\datos\\FUENTES.md.

  Motor: Godot Engine 4.7.2 (godotengine.org), licencia MIT. Ver motor\\LICENCIA_GODOT.txt.


SI ALGO FALLA
-------------
  - "No se encuentra el motor": no se descomprimio todo el ZIP. Extrae todo y vuelve a intentarlo.
  - Pantalla negra o se cierra al abrir: actualiza el controlador de la tarjeta grafica (necesita Vulkan).
  - Para ver los mensajes del motor: abre una ventana de comandos en esta carpeta y escribe
      motor\\LuzCenicienta_console.exe --path juego
"""


# ---------------------------------------------------------------------------------------------- privacidad

def mismo_archivo(a, b):
    """Igualdad byte a byte por SHA-256 (los ejecutables del motor deben ser los oficiales sin cambios)."""
    def h(p):
        s = hashlib.sha256()
        with open(p, "rb") as f:
            for bloque in iter(lambda: f.read(1 << 20), b""):
                s.update(bloque)
        return s.hexdigest()
    return h(a) == h(b)


def buscar_datos_personales(carpeta, omitir=()):
    """Busca el nombre de usuario del equipo (tambien en UTF-16), rutas C:\\Users\\... y correos. Los ejecutables
    oficiales del motor se omiten: se comprueba aparte que son identicos a los de Godot (en el binario aparecen
    palabras como 'Anguilla' o 'guillemotleft' que no son datos personales)."""
    omitir = {Path(p).resolve() for p in omitir}
    usuario = os.environ.get("USERNAME", "").strip()
    patrones = []
    if usuario:
        patrones.append(re.compile(re.escape(usuario.encode("utf-8")), re.IGNORECASE))
        patrones.append(re.compile(re.escape(usuario.encode("utf-16-le")), re.IGNORECASE))
    hallazgos = []
    for p in sorted(carpeta.rglob("*")):
        if not p.is_file() or p.resolve() in omitir:
            continue
        datos = p.read_bytes()
        for permitido in NOMBRES_PERMITIDOS:
            datos = re.sub(re.escape(permitido.encode()), b"#" * len(permitido), datos, flags=re.IGNORECASE)
        rel = p.relative_to(carpeta).as_posix()
        for patron in patrones:
            if patron.search(datos):
                hallazgos.append(f"{rel}: nombre de usuario")
        if p.suffix.lower() in EXT_TEXTO:
            if RUTA_USUARIO.search(datos):
                hallazgos.append(f"{rel}: ruta de usuario ({RUTA_USUARIO.search(datos).group(0)!r})")
            m = CORREO.search(datos)
            if m:
                hallazgos.append(f"{rel}: correo ({m.group(0)!r})")
    return hallazgos


# ---------------------------------------------------------------------------------------------- pasos

def armar(ejecutor, sin_importar):
    consola_origen = Path(ejecutor.GODOT)
    gui_origen = consola_origen.with_name(consola_origen.name.replace("_console", ""))
    for p in (consola_origen, gui_origen):
        if not p.exists():
            raise SystemExit(f"No se encuentra {p}")
    if PAQUETE.exists():
        if PAQUETE.parent != ENTREGA:
            raise SystemExit("Ruta de salida inesperada")
        shutil.rmtree(PAQUETE)
    PAQUETE.mkdir(parents=True)

    print("1. Motor", flush=True)
    (PAQUETE / "motor").mkdir()
    shutil.copy2(gui_origen, PAQUETE / "motor" / EXE)
    shutil.copy2(consola_origen, PAQUETE / "motor" / EXE_CONSOLA)
    escribir_texto(PAQUETE / "motor" / "LICENCIA_GODOT.txt", LICENCIA, bom=False)

    print("2. Juego y extras (copias)", flush=True)
    copiar_proyecto(JUEGO, PAQUETE / "juego", FUERA_JUEGO)
    (PAQUETE / "juego" / "capturas").mkdir()
    (PAQUETE / "juego" / "capturas" / ".gdignore").write_bytes(b"")
    copiar_proyecto(ARTEMIS, PAQUETE / "extras" / "mision_artemis", FUERA_ARTEMIS)
    copiar_proyecto(MARTE, PAQUETE / "extras" / "mision_artemis_marte", FUERA_MARTE)

    proyectos = [PAQUETE / "juego", PAQUETE / "extras" / "mision_artemis", PAQUETE / "extras" / "mision_artemis_marte"]
    if not sin_importar:
        print("3. Cache de importacion (sobre las copias, con el motor del paquete)", flush=True)
        for proyecto in proyectos:
            importar(ejecutor, proyecto)
    for proyecto in proyectos:
        limpiar_cache_editor(proyecto)
        if not (proyecto / ".godot" / "imported").is_dir():
            print(f"  AVISO: {proyecto.name} sin .godot/imported: su lanzador importara la primera vez", flush=True)

    print("4. Lanzadores y LEEME", flush=True)
    escribir_cmd(PAQUETE / "Jugar.cmd", LANZADOR.format(
        comentario="Luz cenicienta: abre el juego sin instalarlo (doble clic).", proyecto="juego", extra=""))
    escribir_cmd(PAQUETE / "Jugar en pantalla completa.cmd", LANZADOR.format(
        comentario="Luz cenicienta a pantalla completa (F11 vuelve a ventana).", proyecto="juego",
        extra=" --fullscreen"))
    escribir_cmd(PAQUETE / "Jugar extra - Mision Artemis (Luna).cmd", LANZADOR.format(
        comentario="Extra: Mision Artemis (Luna), juego de la biblioteca hecho por el equipo. Se juega aparte.",
        proyecto=r"extras\mision_artemis", extra=""))
    escribir_cmd(PAQUETE / "Jugar extra - Mision Artemis (Marte).cmd", LANZADOR.format(
        comentario="Extra: Mision Artemis (Marte), juego de la biblioteca hecho por el equipo. Se juega aparte.",
        proyecto=r"extras\mision_artemis_marte", extra=""))
    escribir_cmd(PAQUETE / "Instalar.cmd", INSTALAR)
    escribir_cmd(PAQUETE / "Desinstalar.cmd", DESINSTALAR)
    escribir_texto(PAQUETE / "LEEME.txt", LEEME, bom=True)

    print("5. Comprobaciones", flush=True)
    for p in PAQUETE.rglob("*"):
        rel = p.relative_to(PAQUETE)
        if any(parte.startswith(".git") and parte != ".gitkeep" for parte in rel.parts) or p.suffix.lower() == ".log":
            raise SystemExit(f"Archivo que no debe ir: {rel}")
        if not str(rel).isascii():
            raise SystemExit(f"Nombre de archivo con tildes en el paquete: {rel}")
    capturas = [p for p in (PAQUETE / "juego" / "capturas").iterdir() if p.name != ".gdignore"]
    if capturas:
        raise SystemExit("Hay capturas en el paquete")
    motor = [(gui_origen, PAQUETE / "motor" / EXE), (consola_origen, PAQUETE / "motor" / EXE_CONSOLA)]
    for original, copia in motor:
        if not mismo_archivo(original, copia):
            raise SystemExit(f"{copia.name} no es identico al ejecutable oficial de Godot")
    print("  motor: identico byte a byte al ejecutable oficial de Godot 4.7.2 (SHA-256)", flush=True)
    hallazgos = buscar_datos_personales(PAQUETE, omitir=[c for _, c in motor])
    if hallazgos:
        print("  DATOS PERSONALES ENCONTRADOS:\n   " + "\n   ".join(hallazgos), flush=True)
        raise SystemExit(1)
    print("  sin datos personales (usuario, rutas de usuario ni correos)", flush=True)
    archivos = [p for p in PAQUETE.rglob("*") if p.is_file()]
    print(f"  paquete: {len(archivos)} archivos, {sum(p.stat().st_size for p in archivos) / 1e6:.1f} MB", flush=True)


def comprimir():
    if not PAQUETE.exists():
        raise SystemExit("Falta la carpeta del paquete: arma primero")
    print("6. ZIP", flush=True)
    inicio = time.time()
    temporal = ZIP.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temporal, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(PAQUETE.rglob("*")):
            arc = (Path(NOMBRE) / p.relative_to(PAQUETE)).as_posix()
            if p.is_dir():
                if not any(p.iterdir()):
                    z.writestr(arc + "/", b"")
                continue
            z.write(p, arc)
    temporal.replace(ZIP)
    with zipfile.ZipFile(ZIP) as z:
        malos = z.testzip()
        n = len(z.namelist())
    if malos:
        raise SystemExit(f"ZIP danado en {malos}")
    print(f"  {ZIP.relative_to(RAIZ)}: {n} entradas, {ZIP.stat().st_size / 1e6:.1f} MB "
          f"({ZIP.stat().st_size / 2**20:.1f} MiB), {time.time() - inicio:.0f} s", flush=True)


def gitignore():
    ruta = RAIZ / ".gitignore"
    texto = ruta.read_text(encoding="utf-8")
    if not any(l.strip() in ("entrega/", "/entrega/") for l in texto.splitlines()):
        texto = texto.rstrip("\n") + "\n\n# Paquete jugable generado (herramientas/empaquetar_juego.py)\nentrega/\n"
        ruta.write_text(texto, encoding="utf-8", newline="\n")
        print("  .gitignore: anadida la linea entrega/", flush=True)


def main():
    args = sys.argv[1:]
    gitignore()
    if "--solo-zip" not in args:
        armar(cargar_ejecutor(), "--sin-importar" in args)
    if "--sin-zip" not in args:
        comprimir()
    print("FIN", flush=True)


if __name__ == "__main__":
    main()
