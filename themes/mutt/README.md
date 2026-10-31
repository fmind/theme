# NeoMutt

Fmind light colors for the NeoMutt email client. They use 24-bit `#RRGGBB` colors, which classic Mutt does not support, and enable `color_directcolor` before any `color` command; your terminal needs truecolor support.

Format: [NeoMutt colors](https://neomutt.org/guide/configuration.html#color) · [color_directcolor](https://neomutt.org/guide/reference.html#color-directcolor)

## Installation

1. Copy `fmind.muttrc` to `~/.mutt/fmind.muttrc` (or `~/.config/neomutt/fmind.muttrc`).
2. Source it in your `muttrc`:
   ```muttrc
   source ~/.mutt/fmind.muttrc
   ```
