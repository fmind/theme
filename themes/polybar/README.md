# Fmind for Polybar

Files: [fmind.ini](fmind.ini).

Format: [Polybar configuration](https://github.com/polybar/polybar/wiki/Configuration)

## Installation

Copy to `~/.config/polybar/fmind.ini`; add `include-file = ~/.config/polybar/fmind.ini` at the top of your Polybar config. Use `${colors.background}` and `${colors.foreground}` in each bar, and the other named colors in modules. Merge with an existing `[colors]` section instead of defining it twice.
