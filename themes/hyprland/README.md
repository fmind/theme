# Fmind for Hyprland

Files: [fmind.lua](fmind.lua), [Hyprlock](hyprlock.conf).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

For Hyprland 0.55+, copy the Lua file beside `hypr/hyprland.lua`; load `require("fmind")` after appearance settings. Includes borders, group titles and a white desktop background. For Hyprlock, merge the supplied background, input-field and clock widgets into `hypr/hyprlock.conf`, replacing existing equivalents. Authentication settings remain yours.
