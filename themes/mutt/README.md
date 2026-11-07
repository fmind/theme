# NeoMutt

Fmind light colors for the NeoMutt email client. They use 24-bit `#RRGGBB` colors, which classic Mutt does not support, and enable `color_directcolor` before any `color` command; your terminal needs truecolor support.

Format: [NeoMutt colors](https://neomutt.org/guide/configuration.html#color) · [color_directcolor](https://neomutt.org/guide/reference.html#color-directcolor)

## Installation

1. Copy `fmind.muttrc` to `~/.config/neomutt/fmind.muttrc` (or `~/.mutt/fmind.muttrc`).
2. Source it from your `neomuttrc` with the path you chose:
   ```muttrc
   source ~/.config/neomutt/fmind.muttrc
   ```
