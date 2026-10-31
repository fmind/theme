# Fmind for Plymouth

Light splash theme for [Plymouth](https://www.freedesktop.org/wiki/Software/Plymouth/): a white screen with charcoal password prompts, questions and boot messages.

Format: [Plymouth script API](https://gitlab.freedesktop.org/plymouth/plymouth/-/blob/main/src/plugins/splash/script/script-lib-plymouth.c) · [script theme example](https://gitlab.freedesktop.org/plymouth/plymouth/-/blob/main/themes/script/script.script)

## Installation

Copy [fmind.plymouth](fmind.plymouth) and [fmind.script](fmind.script) to `/usr/share/plymouth/themes/fmind/`, then run `sudo plymouth-set-default-theme -R fmind`. Prompts and messages need Plymouth's label plugin (`plymouth-label` on Debian and Ubuntu, `plymouth-plugin-label` on Fedora); without it, the splash stays plain white and Esc switches to Plymouth's text details view, which shows prompts.
