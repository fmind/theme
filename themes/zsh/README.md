# Fmind for Zsh

A light prompt theme for Zsh and Oh My Zsh.

Format: [Zsh prompt expansion](https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html) · [Oh My Zsh theme loader](https://github.com/ohmyzsh/ohmyzsh/blob/master/oh-my-zsh.sh)

## Installation

The prompt uses 24-bit `%F{#RRGGBB}` colors, so the terminal needs truecolor support.

### Oh My Zsh
1. Copy [fmind.zsh-theme](fmind.zsh-theme) to `~/.oh-my-zsh/custom/themes/fmind.zsh-theme`:
   ```sh
   cp themes/zsh/fmind.zsh-theme ~/.oh-my-zsh/custom/themes/fmind.zsh-theme
   ```
2. Set `ZSH_THEME="fmind"` in your `~/.zshrc`.
3. Reload Zsh (`source ~/.zshrc`).

### Standalone Zsh
Add the contents of [fmind.zsh-theme](fmind.zsh-theme) directly to your `~/.zshrc`.
