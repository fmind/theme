# dircolors

Fmind theme for [dircolors](https://www.gnu.org/software/coreutils/).

Format: [dircolors invocation](https://www.gnu.org/software/coreutils/manual/html_node/dircolors-invocation.html) · [dircolors.hin](https://github.com/coreutils/coreutils/blob/master/src/dircolors.hin)

## Install

Copy [.dircolors](.dircolors) to `~/.dircolors`, then add this line to your shell configuration (`~/.bashrc` or `~/.zshrc`):

```sh
eval "$(dircolors -b ~/.dircolors)"
```
