# Fmind for GNOME Terminal

Files: [fmind.dconf](fmind.dconf).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Import into a chosen profile with the scoped command below. The fragment only changes colors.

Create or select a profile in Preferences and copy its UUID from the profile’s settings. Import only into that profile, replacing `<profile-uuid>` and the file path below:

```sh
dconf load '/org/gnome/terminal/legacy/profiles:/:<profile-uuid>/' < /path/to/themes/gnome-terminal/fmind.dconf
```
