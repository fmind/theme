# GRUB 2

Fmind light theme for GRUB 2 bootloader.

Format: [GRUB theme file format](https://www.gnu.org/software/grub/manual/grub/html_node/Theme-file-format.html)

## Installation

1. Copy this directory to `/boot/grub/themes/fmind` (or `/boot/grub2/themes/fmind`).
1. GRUB reads only PF2 fonts, so convert Google Sans for the terminal font: `grub-mkfont -s 16 -o /boot/grub/themes/fmind/google-sans-16.pf2 GoogleSans-Regular.ttf`. Without it, GRUB falls back to its default font.
1. In `/etc/default/grub`, set `GRUB_THEME="/boot/grub/themes/fmind/theme.txt"`.
1. Update GRUB configuration via `grub-mkconfig -o /boot/grub/grub.cfg` (or `update-grub`).
