# Omarchy

Fmind theme for [Omarchy](https://omarchy.org/).

Format: [Omarchy manual: Making your own theme](https://learn.omacom.io/2/the-omarchy-manual/92/making-your-own-theme) · [colors.toml resolver](https://github.com/omacom/omarchy/blob/quattro/bin/omarchy-theme-color)

## Install

Copy [colors.toml](colors.toml) into a user theme folder, then apply it:

```sh
mkdir -p ~/.config/omarchy/themes/fmind
cp colors.toml ~/.config/omarchy/themes/fmind/
omarchy-theme-set fmind
```

Omarchy generates the terminal, editor, Hyprland and other app configs from these colors. For a matching background, copy a [wallpaper](../../wallpapers/README.md) to `~/.config/omarchy/backgrounds/fmind/`.
