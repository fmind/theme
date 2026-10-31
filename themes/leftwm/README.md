# Fmind for LeftWM

Light theme for [LeftWM](https://leftwm.org/).

Format: [LeftWM theme_config.rs](https://github.com/leftwm/leftwm/blob/main/leftwm/src/theme_config.rs) · [LeftWM theme guide](https://github.com/leftwm/leftwm/blob/main/themes/README.md)

## Installation

Copy [theme.ron](theme.ron) into your current LeftWM theme directory, `~/.config/leftwm/themes/current/` (`$XDG_CONFIG_HOME/leftwm/themes/current/`), replacing its `theme.ron`. The theme's `up` script must load it with `leftwm-command "LoadTheme $SCRIPTPATH/theme.ron"`, as LeftWM's bundled themes do; rerun `up` or restart LeftWM to apply it.
