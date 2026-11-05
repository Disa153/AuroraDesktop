@echo off
cd /d %~dp0
py -m pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --windowed --name AuroraDesktop src\main.py
echo EXE: dist\AuroraDesktop\AuroraDesktop.exe
pause
