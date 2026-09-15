#!/bin/sh
# Fmind i3lock-color script
alpha='dd'
background='#ffffff'
selection='#d2e3fc'
text='#202124'
blue='#174ea6'
green='#0d652d'
red='#a50e0e'

i3lock \
  --insidever-color="${selection}${alpha}" \
  --insidewrong-color="${selection}${alpha}" \
  --inside-color="${background}${alpha}" \
  --ringver-color="${green}${alpha}" \
  --ringwrong-color="${red}${alpha}" \
  --ring-color="${blue}${alpha}" \
  --line-color="${selection}${alpha}" \
  --keyhl-color="${green}${alpha}" \
  --bshl-color="${red}${alpha}" \
  --separator-color="${blue}${alpha}" \
  --verif-color="${text}" \
  --wrong-color="${red}" \
  --layout-color="${text}" \
  --time-color="${text}" \
  --date-color="${text}"
