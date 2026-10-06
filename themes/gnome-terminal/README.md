# Fmind for GNOME Terminal

Files: [fmind.dconf](fmind.dconf).

## Installation

Merge fragments into existing settings.

Import into a chosen profile with the scoped command below. The fragment only changes colors.

Create or select a profile in Preferences and copy its UUID from the profile’s settings. Import only into that profile, replacing `<profile-uuid>` and the file path below:

```sh
dconf load '/org/gnome/terminal/legacy/profiles:/:<profile-uuid>/' < /path/to/themes/gnome-terminal/fmind.dconf
```
