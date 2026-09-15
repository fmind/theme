# Fmind for ConEmu

Files: [fmind.xml](fmind.xml).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Save a custom Fmind scheme in Settings → Features → Colors, then close ConEmu. In `ConEmu.xml`, replace that saved `PaletteN` key’s values with this file’s values, retaining its `PaletteN` key name. Reopen and select Fmind. Slot 15 is reserved for the white canvas; ANSI bright-white text needs an app override.
