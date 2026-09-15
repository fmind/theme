# Fmind for SwayNotificationCenter

Files: [fmind.css](fmind.css).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Copy to `swaync/fmind.css`; import the installed default stylesheet followed by this file in your `swaync/style.css`, as shown below. Reload with `swaync-client --reload-css`. Covers notifications, actions, replies, groups and built-in widgets.

In `~/.config/swaync/style.css`:

```css
@import "/etc/xdg/swaync/style.css";
@import "fmind.css";
```

Adjust the first path if your package installs its default stylesheet elsewhere. See the [upstream configuration guide](https://github.com/ErikReider/SwayNotificationCenter#configuration).
