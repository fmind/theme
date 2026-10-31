# Fmind for MakeHuman

Light theme for [MakeHuman](http://www.makehumancommunity.org/) 1.x: a flat white viewport, a gray grid, palette log colors and a light Qt style. Files: [fmind.mht](fmind.mht), [fmind.qss](fmind.qss).

Format: [setTheme in mhmain.py](https://github.com/makehumancommunity/makehuman/blob/master/makehuman/core/mhmain.py) · [bundled makehuman.mht](https://github.com/makehumancommunity/makehuman/blob/master/makehuman/data/themes/makehuman.mht)

## Installation

1. Copy [fmind.mht](fmind.mht) and [fmind.qss](fmind.qss) to the `data/themes/` folder of the MakeHuman program files, next to `makehuman.mht`. On macOS this folder is inside the app bundle under `Contents/Resources/makehuman/`.
2. Close MakeHuman, because it rewrites its settings on exit.
3. In `settings.ini` in the MakeHuman home folder, set `"guiTheme": "fmind"`. The home folder is `Documents/makehuman/v1py3/` on Windows and Linux (Linux falls back to `~/makehuman/v1py3/` without an XDG Documents folder) and `~/Documents/MakeHuman/v1py3/` on macOS, unless you configured another home folder, for example with `MH_HOME_LOCATION`.
4. Start MakeHuman. The Settings tab lists only its two built-in themes; choosing one of them replaces Fmind.
