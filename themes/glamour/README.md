# Fmind for Glamour

Files: [fmind.json](fmind.json).

Format: [Glamour styles](https://github.com/charmbracelet/glamour/tree/master/styles) · [`GLAMOUR_STYLE` in GitHub CLI](https://cli.github.com/manual/gh_help_environment)

## Installation

[Glamour](https://github.com/charmbracelet/glamour) renders Markdown in terminal tools. Copy `fmind.json` to `~/.config/glamour/fmind.json` and point `GLAMOUR_STYLE` at it.

## GitHub CLI

`gh` renders issues, pull requests, releases and READMEs with Glamour:

```sh
export GLAMOUR_STYLE="$HOME/.config/glamour/fmind.json"  # bash and zsh
set -gx GLAMOUR_STYLE ~/.config/glamour/fmind.json       # fish
gh repo view fmind/theme
```

`H1` renders as a white-on-blue badge, `H2`–`H3` and links are dark blue, `H4`–`H5` are charcoal, inline code is dark blue on light gray, and emphasis is purple and upright. Glamour reduces the syntax colors inside code blocks to the nearest 256-color values. Tested with GitHub CLI 2.103.3.
