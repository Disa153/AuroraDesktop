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
echo Installing application dependencies...
%PY_CMD% -m pip install --upgrade pip
if errorlevel 1 goto :error

%PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Starting Aurora Desktop...
%PY_CMD% src\main.py
if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo [ERROR] A command failed. Read the error above.
pause
exit /b 1
