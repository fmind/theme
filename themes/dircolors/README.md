# Fmind for dircolors

Fmind theme for [dircolors](https://www.gnu.org/software/coreutils/).

Files: [.dircolors](.dircolors).

Format: [dircolors invocation](https://www.gnu.org/software/coreutils/manual/html_node/dircolors-invocation.html) · [dircolors.hin](https://github.com/coreutils/coreutils/blob/master/src/dircolors.hin)

## Installation

Copy [.dircolors](.dircolors) to `~/.dircolors`, then evaluate it in `~/.bashrc` or `~/.zshrc`:

```sh
eval "$(dircolors -b ~/.dircolors)"
```

In Fish (`~/.config/fish/config.fish`), use the C-shell output format:

```fish
eval (dircolors -c ~/.dircolors)
```

## fd

[fd](https://github.com/sharkdp/fd#colorized-output) reads `LS_COLORS` from the environment and highlights matching paths and extensions automatically once `dircolors` is loaded above.
