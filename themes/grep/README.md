# Fmind for GNU grep

Light color scheme for GNU grep.

Files: [fmind.sh](fmind.sh).

Format: [GNU grep GREP_COLORS](https://www.gnu.org/software/grep/manual/html_node/Environment-Variables.html)

## Installation

Source [fmind.sh](fmind.sh) from `~/.bashrc` or `~/.zshrc`, or set `GREP_COLORS` directly:

```sh
export GREP_COLORS='ms=01;38;2;32;33;36;48;2;254;239;195:mc=01;38;2;32;33;36;48;2;254;239;195:sl=:cx=:fn=01;38;2;23;78;166:ln=38;2;89;93;98:bn=38;2;89;93;98:se=38;2;89;93;98'  # bash and zsh
set -gx GREP_COLORS 'ms=01;38;2;32;33;36;48;2;254;239;195:mc=01;38;2;32;33;36;48;2;254;239;195:sl=:cx=:fn=01;38;2;23;78;166:ln=38;2;89;93;98:bn=38;2;89;93;98:se=38;2;89;93;98'  # fish
```
