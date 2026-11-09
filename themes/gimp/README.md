# Fmind for GIMP

Fmind palette for [GIMP](https://www.gimp.org/).

Format: [GIMP palette loader](https://gitlab.gnome.org/GNOME/gimp/-/blob/master/app/core/gimppalette-load.c)

## Installation

Copy `Fmind.gpl` to the `palettes` folder of your [GIMP configuration folder](https://docs.gimp.org/3.2/en/gimp-fire-up.html#gimp-concepts-setup), then restart GIMP. For GIMP 3.2 this is `~/.config/GIMP/3.2/palettes/` on Linux, `%APPDATA%\GIMP\3.2\palettes\` on Windows and `~/Library/Application Support/GIMP/3.2/palettes/` on macOS; other versions use their own `major.minor` folder.

## ColorSlurp

[ColorSlurp](https://colorslurp.com/) imports GIMP palettes, not JSON ([ColorSlurp import formats](https://colorslurp.com/docs/guides/palettes)). Choose **File** > **Import Palettes** and select [Fmind.gpl](Fmind.gpl), or drop that file into the ColorSlurp window.

## Inkscape

[Inkscape](https://inkscape.org/) reads GIMP palettes ([Inkscape palettes](https://gitlab.com/inkscape/inkscape/-/blob/master/share/palettes/README) · [palette manual](https://inkscape-manuals.readthedocs.io/en/latest/palette.html)).

1. Copy [Fmind.gpl](Fmind.gpl) to your Inkscape palettes directory (`~/.config/inkscape/palettes/` on Linux).
2. In Inkscape, click the arrow on the bottom palette bar and select **Fmind**.
