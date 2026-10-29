# shellcheck shell=bash
# Fmind colors for man pages via less
export LESS_TERMCAP_mb=$'\e[1;31m'
export LESS_TERMCAP_md=$'\e[1;34m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_so=$'\e[48;2;210;227;252m\e[38;2;32;33;36m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_us=$'\e[4;32m'
export LESS_TERMCAP_ue=$'\e[0m'
# grotty SGR escapes bypass LESS_TERMCAP_*; request legacy overstriking instead.
export GROFF_NO_SGR=1
