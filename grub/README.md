# GRUB 2

Fmind light theme for GRUB 2 bootloader.

## Installation

1. Copy the `grub/` directory to `/boot/grub/themes/fmind` (or `/boot/grub2/themes/fmind`).
2. In `/etc/default/grub`, set `GRUB_THEME="/boot/grub/themes/fmind/theme.txt"`.
3. Update GRUB configuration via `grub-mkconfig -o /boot/grub/grub.cfg` (or `update-grub`).
