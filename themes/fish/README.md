# Fmind for Fish

Files: [fmind.theme](fmind.theme), [fmind.fish](fmind.fish).

Format: [fish theme files](https://fishshell.com/docs/current/cmds/fish_config.html#theme-files) · [fish syntax highlighting variables](https://fishshell.com/docs/current/interactive.html#syntax-highlighting)

## Installation

Recommended: copy [fmind.theme](fmind.theme) to `~/.config/fish/themes/fmind.theme`, then choose it in each interactive session from a `conf.d` file, such as `~/.config/fish/conf.d/theme.fish`:

```fish
if status is-interactive; and test -r $__fish_config_dir/themes/fmind.theme
    fish_config theme choose fmind
end
```

The theme file is data that fish validates, not a script. `fish_config theme choose` sets global variables for the current session only, so it belongs in `conf.d`; `fish_config theme save` instead writes universal variables after a confirmation prompt. The file has no `[light]` or `[dark]` sections, so fish applies the same colours whatever background the terminal reports. Fish 3.4 or later reads theme files from `~/.config/fish/themes`.

Alternative: copy [fmind.fish](fmind.fish) to `~/.config/fish/conf.d/fmind.fish`. Fish runs it as a script on every start.
