# Aurora Desktop

Native Windows desktop customization prototype built with Python and PySide6.

## Run

```bat
py -m pip install -r requirements.txt
py src\main.py
```

## Build executable

Run `build_exe.bat`. The executable will be created in `dist\AuroraDesktop\AuroraDesktop.exe`.

## Current prototype

- Native PySide6 desktop interface
- Animated in-app weather/effect preview
- Effect intensity and speed controls
- Accent theme selection
- Dock layout preview
- Settings UI

Note: desktop-wide overlays, real application launching from Dock, and persistent Windows startup integration are not implemented yet.