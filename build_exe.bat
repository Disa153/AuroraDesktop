@echo off
setlocal
cd /d "%~dp0"

set "PY_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PY_CMD=py -3"
)

if not defined PY_CMD (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys" >nul 2>nul
        if not errorlevel 1 set "PY_CMD=python"
    )
)

if not defined PY_CMD (
    echo [ERROR] Python could not be started.
    echo Install Python 3.12, 3.13 or 3.14 from https://www.python.org/downloads/windows/
    echo During setup enable "Add python.exe to PATH".
    pause
    exit /b 1
)

echo Using Python:
%PY_CMD% --version
echo.
echo Updating pip...
%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 goto :error

echo.
echo Installing project dependencies...
%PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Installing PyInstaller...
%PY_CMD% -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

rem Use a fresh output directory on every run.
rem This avoids permission errors when Windows still holds files
rem inside an older dist\AuroraDesktop folder.
set "BUILD_DIR=aurora_build_%RANDOM%_%RANDOM%"
mkdir "%BUILD_DIR%"
if errorlevel 1 goto :error

echo.
echo Building Aurora Desktop into %BUILD_DIR% ...
%PY_CMD% -m PyInstaller --noconfirm --windowed --name AuroraDesktop --distpath "%BUILD_DIR%\dist" --workpath "%BUILD_DIR%\work" --specpath "%BUILD_DIR%\spec" src\main.py
if errorlevel 1 goto :error

echo.
echo [SUCCESS] Build completed.
echo EXE: %CD%\%BUILD_DIR%\dist\AuroraDesktop\AuroraDesktop.exe
echo Copy the entire folder:
echo %CD%\%BUILD_DIR%\dist\AuroraDesktop
echo.
pause
exit /b 0

:error
echo.
echo [ERROR] Build stopped because a command failed.
echo Read the error above. No successful build is guaranteed.
pause
exit /b 1
