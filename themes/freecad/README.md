# FreeCAD

Fmind theme for [FreeCAD](https://www.freecad.org/).

Format: [Qt style sheets](https://doc.qt.io/qt-6/stylesheet-reference.html) · [FreeCAD style sheet search paths](https://github.com/FreeCAD/FreeCAD/blob/main/src/Gui/StartupProcess.cpp)

## Install

1. Copy `Fmind.qss` to the `Gui/Stylesheets/` folder of FreeCAD's user data directory. Run `App.getUserAppDataDir()` in FreeCAD's Python console to print that directory; for FreeCAD 1.1 on Linux it is usually `~/.local/share/FreeCAD/v1-1/`.
2. Open Edit → Preferences → Display → UI.
3. Select **Fmind** under Style sheet (advanced).
