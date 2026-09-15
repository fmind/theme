#!/bin/sh
# Fmind Linux virtual console colors

if [ "$TERM" = "linux" ]; then
    printf %b '\e[40m' '\e[8]' # set default background
    printf %b '\e[37m' '\e[8]' # set default foreground
    printf %b '\e]P0ffffff'    # 0 black (canvas)
    printf %b '\e]P8595d62'    # 8 bright black (muted)
    printf %b '\e]P1a50e0e'    # 1 red
    printf %b '\e]P9ea4335'    # 9 bright red
    printf %b '\e]P20d652d'    # 2 green
    printf %b '\e]PA34a853'    # 10 bright green
    printf %b '\e]P3934900'    # 3 yellow/orange
    printf %b '\e]PBe37400'    # 11 bright yellow/orange
    printf %b '\e]P4174ea6'    # 4 blue
    printf %b '\e]PC4285f4'    # 12 bright blue
    printf %b '\e]P5681da8'    # 5 magenta (purple)
    printf %b '\e]PD681da8'    # 13 bright magenta
    printf %b '\e]P600636d'    # 6 cyan (teal)
    printf %b '\e]PE00636d'    # 14 bright cyan
    printf %b '\e]P7202124'    # 7 white (text)
    printf %b '\e]PF202124'    # 15 bright white (text)
    clear
fi
