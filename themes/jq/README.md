# Fmind for jq

Files: [fmind.sh](fmind.sh).

Format: [jq Colors](https://jqlang.org/manual/#colors)

## Installation

Copy [fmind.sh](fmind.sh) to `~/.config/jq/fmind.sh` and source it in `~/.bashrc` or `~/.zshrc`, or set `JQ_COLORS` directly in `~/.config/fish/config.fish`:

```sh
export JQ_COLORS='1;38;2;147;73;0:1;38;2;147;73;0:1;38;2;147;73;0:0;38;2;147;73;0:0;38;2;13;101;45:0;38;2;32;33;36:0;38;2;32;33;36:1;38;2;23;78;166'
```

```fish
set -gx JQ_COLORS '1;38;2;147;73;0:1;38;2;147;73;0:1;38;2;147;73;0:0;38;2;147;73;0:0;38;2;13;101;45:0;38;2;32;33;36:0;38;2;32;33;36:1;38;2;23;78;166'
```

Object keys are bold dark blue `#174EA6`, strings dark green `#0D652D`, numbers regular dark orange `#934900`, `null`/`false`/`true` bold dark orange `#934900`, and arrays and objects charcoal `#202124`. Requires a truecolor terminal. Tested with jq 1.8.2.
