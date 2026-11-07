# Fmind for delta

Files: [fmind.gitconfig](fmind.gitconfig).

Format: [delta configuration](https://dandavison.github.io/delta/configuration.html) · [delta options](https://dandavison.github.io/delta/full---help-output.html)

## Installation

Install the [bat theme](../bat/README.md) first, since delta reads `syntax-theme = "fmind"` from bat. Then include [fmind.gitconfig](fmind.gitconfig) from your global `~/.gitconfig`, or paste its `[delta]` section there:

```ini
[include]
	path = /path/to/theme/themes/delta/fmind.gitconfig
```
