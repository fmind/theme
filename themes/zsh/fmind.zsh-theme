# https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html
# Fmind light prompt theme for Zsh

autoload -Uz vcs_info
precmd_vcs_info() { vcs_info }
precmd_functions+=( precmd_vcs_info )
setopt prompt_subst

zstyle ':vcs_info:git:*' formats ' %F{#595d62}(%F{#174ea6}%b%F{#595d62})%f'
zstyle ':vcs_info:*' enable git

PROMPT='%F{#174ea6}%~%f${vcs_info_msg_0_} %(?.%F{#0d652d}❯%f.%F{#a50e0e}❯%f) '
RPROMPT='%(?..%F{#a50e0e}%?%f)'
