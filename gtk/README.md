# Fmind GTK

Native GTK 2, GTK 3.20+ and GTK 4 widget themes. Windows, editors, panels and popovers are white; selections and semantic feedback use pale fills. Google Sans is the UI font and Google Sans Code is the monospace font. Missing fonts use the system fallback.

## Install

Copy this entire directory to `~/.themes/Fmind/`, preserving [common.css](common.css), [index.theme](index.theme) and all version subdirectories. Select Fmind in your desktop's GTK theme chooser. This package does not change your settings automatically.

For an isolated GTK 3 or GTK 4 application preview, use `GTK_THEME=Fmind application-command`. GTK 2 follows the desktop theme setting; for an isolated preview use `GTK2_RC_FILES="$HOME/.themes/Fmind/gtk-2.0/gtkrc" application-command`. Replace `application-command` with the application you want to preview.

Fmind is exclusively light. The `gtk-dark.css` entry points deliberately load the same light palette. GTK 3 uses its built-in Adwaita resource for geometry and symbolic assets; GTK 4 uses its built-in Default resource. GTK 2 uses its built-in drawing engine. No copied third-party base styles, external rendering engines or downloaded image assets are needed.

The theme includes buttons, suggested/destructive actions, entries, selection, checks, radios, switches, menus, popovers, tooltips, tabs, lists, scrollbars, scales, progress and semantic messages, with disabled and backdrop states. It exports GTK 3's named theme colors for applications that draw custom controls. Applications can override system themes; libadwaita applications are not covered by installing this package. GTK versions older than 3.20 use a different selector model and remain pending.

## Full bundle checklist

The [free Dracula GTK repository](https://github.com/dracula/gtk) also contains desktop-shell and window-manager themes. The catalog's GTK entry remains pending until those companions are implemented and checked.

- [x] [GTK 2 widgets](gtk-2.0/gtkrc), using the native drawing engine.
- [x] [GTK 3.20+ widgets](gtk-3.0/gtk.css).
- [x] [GTK 4 widgets](gtk-4.0/gtk.css).
- [ ] GTK 3 before 3.20.
- [ ] Application-specific widget refinements for the apps in the reference bundle.
- [ ] GNOME Shell.
- [ ] Cinnamon.
- [ ] KDE Plasma, Aurorae and Kvantum.
- [ ] Metacity.
- [ ] Xfwm, including HiDPI decorations.
- [ ] Unity.

The shared color layer is maintained directly. The built-in base theme can evolve with GTK; the tested toolkit versions and validation limits are recorded in [coverage](../COVERAGE.md).
