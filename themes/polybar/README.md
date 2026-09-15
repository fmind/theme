# Fmind for Polybar

Files: [fmind.ini](fmind.ini).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Copy to `polybar/fmind.ini`; add `include-file = ~/.config/polybar/fmind.ini` at the top of your Polybar config. Use `${colors.background}` and `${colors.foreground}` in each bar, and the other named colors in modules. Merge with an existing `[colors]` section instead of defining it twice.
