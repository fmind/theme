#!/bin/sh
# Fmind bemenu configuration
# Options: https://github.com/Cloudef/bemenu/blob/master/client/common/common.c
# Unset slots keep bemenu's dark defaults, so alternating rows, cursor,
# feedback and border colors are set too.
export BEMENU_OPTS="--tb '#174ea6' \
 --tf '#ffffff' \
 --fb '#ffffff' \
 --ff '#202124' \
 --cb '#4285f4' \
 --cf '#202124' \
 --nb '#ffffff' \
 --nf '#202124' \
 --ab '#ffffff' \
 --af '#202124' \
 --hb '#d2e3fc' \
 --hf '#202124' \
 --fbb '#174ea6' \
 --fbf '#ffffff' \
 --sb '#d2e3fc' \
 --sf '#202124' \
 --scb '#ffffff' \
 --scf '#174ea6' \
 --bdr '#595d62'"
