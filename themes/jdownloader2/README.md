# JDownloader 2

Fmind light color theme for JDownloader 2.

Format: [JDownloader LAFSettings](https://github.com/mycodedoesnotcompile2/jdownloader_mirror/blob/main/svn_trunk/src/org/jdownloader/updatev2/gui/LAFSettings.java) · [LAF config path](https://github.com/mycodedoesnotcompile2/jdownloader_mirror/blob/main/svn_trunk/src/org/jdownloader/updatev2/gui/LAFOptions.java)

## Install

1. In Settings → Advanced Settings, check **GraphicalUserInterfaceSettings: Look And Feel Theme**. Use a light theme such as `DEFAULT` or `FLATLAF_LIGHT`, then close JDownloader.
2. Copy `fmind.json` into the `cfg/laf/` folder of the JDownloader installation directory, named after the theme's class: `JDDefaultLookAndFeel.json` for `DEFAULT` or `FlatLightLaf.json` for `FLATLAF_LIGHT`. Create the folder if needed, and merge the keys into any existing file of that name.
3. Start JDownloader. The file recolors JDownloader's panels, tables, progress bars and speed meter; the look and feel draws the remaining controls.
