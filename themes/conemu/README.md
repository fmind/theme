# Fmind for ConEmu

Files: [fmind.xml](fmind.xml).

Format: [ConEmu colors](https://conemu.github.io/en/SettingsColors.html) · [ConEmu LoadPalettes](https://github.com/ConEmu/ConEmu/blob/master/src/ConEmu/Options.cpp)

## Installation

Save a custom Fmind scheme in Settings → Features → Colors, then close ConEmu. In `ConEmu.xml`, replace that saved `PaletteN` key’s values with this file’s values, retaining its `PaletteN` key name. Reopen and select Fmind. Slot 15 is reserved for the white canvas; ANSI bright-white text needs an app override.

## Cmder

Cmder uses ConEmu settings ([Cmder launcher](https://github.com/cmderdev/cmder/blob/master/launcher/src/CmderLauncher.cpp)). Install this scheme as above in Cmder's `vendor/conemu-maximus5/ConEmu.xml`.
