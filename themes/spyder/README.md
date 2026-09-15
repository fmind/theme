# Fmind for Spyder

Files: [fmind.ini](fmind.ini).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

For Spyder 6.1, create a custom Fmind syntax theme in Preferences → Appearance, then merge this fragment into that theme’s saved settings as detailed below. Select the Light interface theme.

Create a new syntax highlighting theme named Fmind through Preferences → Appearance and apply it, then close Spyder. Use `spyder --paths` to locate its configuration directory and open `spyder.ini`. Under `[appearance]`, find the entry `custom-N/name = Fmind`. Replace `custom-0` in this repository’s fragment with that exact `custom-N` identifier, then replace only that theme’s entries in the existing section. Preserve `custom_names` and other themes. Reopen Spyder, select Fmind, and select the Light interface theme. This avoids collisions with existing custom schemes; it does not replace the application’s UI stylesheet.
