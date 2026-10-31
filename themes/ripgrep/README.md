# Fmind for ripgrep

Light theme configuration for [ripgrep](https://github.com/BurntSushi/ripgrep).

Format: [ripgrep configuration file](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md#configuration-file) · [ripgrep --colors](https://github.com/BurntSushi/ripgrep/blob/master/crates/core/flags/defs.rs)

## Installation

Copy [fmind.ripgreprc](fmind.ripgreprc) to `~/.config/ripgrep/` and set the `RIPGREP_CONFIG_PATH` environment variable in your shell profile:

```sh
export RIPGREP_CONFIG_PATH="$HOME/.config/ripgrep/fmind.ripgreprc"
```

Or append its flags to your existing ripgrep configuration file.
