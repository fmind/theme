# Fmind for Pantheon Terminal

Files: [fmind.dconf](fmind.dconf).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Import only the terminal appearance keys using the scoped command below. Selects the Custom palette, light UI and explicit colors; system-style following is disabled so it cannot replace the palette.

Run from this directory, then reopen Terminal:

```sh
dconf load /io/elementary/terminal/settings/ < fmind.dconf
```

The destination is the terminal's [native settings path](https://github.com/elementary/terminal/blob/main/data/io.elementary.terminal.gschema.xml).
