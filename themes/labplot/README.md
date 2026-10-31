# Fmind for LabPlot

Light color scheme for [LabPlot](https://labplot.kde.org/). LabPlot reads KDE color schemes, so it uses the shared [KDE Fmind.colors](../gtk/kde/color-schemes/Fmind.colors).

Format: [LabPlot ActionsManager.cpp](https://invent.kde.org/education/labplot/-/blob/master/src/frontend/ActionsManager.cpp) · [KColorScheme kcolorschememodel.cpp](https://invent.kde.org/frameworks/kcolorscheme/-/blob/master/src/kcolorschememodel.cpp)

## Installation

1. Copy [Fmind.colors](../gtk/kde/color-schemes/Fmind.colors) into the `color-schemes` folder of your user data directory: `~/.local/share/color-schemes/` on Linux, `%LOCALAPPDATA%\color-schemes\` on Windows or `~/Library/Application Support/color-schemes/` on macOS.
2. Restart LabPlot, then select **Settings → Color Scheme → Fmind**.
