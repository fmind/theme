# Fmind GTK

Native GTK 2, GTK 3.20+ and GTK 4 widget themes, with GNOME Shell and Cinnamon desktop themes and Metacity and Xfwm window decorations. Windows, editors, panels and popovers are white; selections and semantic feedback use pale fills. Google Sans is the UI font and Google Sans Code is the monospace font. Missing fonts use the system fallback.

## Install

Copy this entire directory to `~/.themes/Fmind/`, preserving [common.css](common.css), [index.theme](index.theme) and all version subdirectories. Select Fmind in your desktop's GTK theme chooser. This package does not change your settings automatically.

For an isolated GTK 3 or GTK 4 application preview, use `GTK_THEME=Fmind application-command`. GTK 2 follows the desktop theme setting; for an isolated preview use `GTK2_RC_FILES="$HOME/.themes/Fmind/gtk-2.0/gtkrc" application-command`. Replace `application-command` with the application you want to preview.

Fmind is exclusively light. The `gtk-dark.css` entry points deliberately load the same light palette. GTK 3 uses its built-in Adwaita resource for geometry and symbolic assets; GTK 4 uses its built-in Default resource. GTK 2 uses its built-in drawing engine. No copied third-party base styles, external rendering engines or downloaded image assets are needed.

The theme includes buttons, suggested/destructive actions, entries, selection, checks, radios, switches, menus, popovers, tooltips, tabs, lists, scrollbars, scales, progress and semantic messages, with disabled and backdrop states. It exports GTK 3's named theme colors for applications that draw custom controls. Applications can override system themes; libadwaita applications are not covered by installing this package. GTK 3 versions older than 3.20 use a different selector model and remain pending.

## GNOME Shell

Copy this complete GTK package to `~/.themes/Fmind/` or `~/.local/share/themes/Fmind/`. Keep the [shell entry point](gnome-shell/gnome-shell.css), [shared shell colors](gnome-shell/common.css), shell assets and Cinnamon assets in their existing relative locations. The shell reuses the package's vector controls; copying only `gnome-shell/` is insufficient.

Enable the official [User Themes extension](https://extensions.gnome.org/extension/19/user-themes/) version matching your GNOME release, then select Fmind through your shell theme chooser. Changing the GTK application theme alone does not select a shell theme. This package does not install extensions or change settings automatically.

The default entry targets GNOME 47+, whose native switches have moving handles and optional accessibility status symbols. For GNOME 43–46, replace `gnome-shell/gnome-shell.css` in your installed copy with [legacy.css](gnome-shell/legacy.css), keeping the filename `gnome-shell.css`. The legacy entry supplies explicit off/on checkbox and switch images. Both entries load the same color layer and remain light regardless of GNOME's light/dark preference.

GNOME supplies its installed default beneath the user stylesheet, so Fmind keeps native layout and geometry without an absolute resource import or a bundled third-party base theme. Fmind sets fixed palette priority for imported color rules and preserves St's grouped-selector ordering. Panels, overview and dash, application grid, search, calendar, notifications, quick settings, dialogs, entries, keyboards, switchers, screenshot controls, workspace feedback and Looking Glass are covered. Ordinary text surfaces are white; screenshot masks and selection previews preserve transparency so the selected content stays visible. Looking Glass uses Google Sans Code.

The legacy entry was checked using St 43.9 and Mutter 43.8. The modern entry was checked against GNOME 50.4's released light and dark stylesheets using that same native engine. A complete GNOME 50 runtime, intermediate versions, third-party extensions and lock-screen behavior remain unverified. Older selectors from the free reference are retained, but pre-43 shells have not been validated. This user theme does not install a GDM login-screen theme. See [coverage](../COVERAGE.md) for native rendering evidence and limits.

## Cinnamon desktop

The [Cinnamon stylesheet](cinnamon/cinnamon.css) is included when you copy this entire package to `~/.themes/Fmind/`. In Cinnamon System Settings → Themes, choose Fmind for Desktop. The Applications and Window borders choices are separate; select the GTK and Metacity components where your desktop supports them. No settings are changed by this package.

Cinnamon imports its installed base at `/usr/share/cinnamon/theme/cinnamon.css` for native geometry, then applies Fmind colors and its own vector controls. That installed file is required. If your distribution installs Cinnamon under another prefix, adjust the first import in the copied Fmind stylesheet to the actual base file. Keep the `cinnamon/assets/` directory beside the stylesheet. The system stylesheet and its assets are reused locally, not bundled or downloaded by Fmind.

The color layer covers horizontal and vertical panels, applets and window lists, menus and search, calendar and events, entries, dialogs, notifications, sound controls and meters, workspace overview and expo, switchers, desklets, virtual keyboards, tooltips and Looking Glass. Normal text surfaces are opaque white; hover, focus, selection, attention and destructive actions retain distinct feedback. Checkboxes, radio buttons and toggles have distinct off/on glyphs; workspace actions, close controls and the hot corner use local SVGs. Looking Glass uses Google Sans Code.

Native style resolution was checked with Cinnamon 5.6.8 and with the stable 6.6.9 base stylesheet compiled from upstream SCSS. Both checks used the 5.6.8 St engine; a full Cinnamon desktop session, the 6.6 runtime, screen-locker integration and arbitrary third-party applets remain unverified. See [coverage](../COVERAGE.md) for the exact evidence boundary.

## KDE color scheme and Plasma style

The package also includes a [KDE application color scheme and Plasma desktop style](kde/README.md). Install them in KDE's color-scheme and Plasma-style directories as described in that guide; the GTK theme directory is not a KDE installation location. The [KDE checklist](kde/README.md#bundle-checklist) tracks Aurorae, Kvantum, global themes, cursors and SDDM separately.

## Window decorations

For Xfwm, the normal [decoration theme](xfwm4/themerc) is included when you copy this directory to `~/.themes/Fmind/`. Select Fmind under Xfce Settings → Window Manager → Style. Your button layout and title alignment remain configurable in Xfce. The menu button uses a consistent Fmind glyph instead of an application icon.

For a display requiring larger decorations, copy the entire `variants/Fmind-hdpi/` directory beside `~/.themes/Fmind/` as `~/.themes/Fmind-hdpi/`, or use `variants/Fmind-xhdpi/` as `~/.themes/Fmind-xhdpi/`. Select the corresponding name in Window Manager. The [HiDPI](variants/Fmind-hdpi/xfwm4/themerc) and [extra-HiDPI](variants/Fmind-xhdpi/xfwm4/themerc) variants use twice and three times the normal pixel dimensions. Text uses your desktop DPI with Google Sans Bold 10; choose the variant that matches that scale. Each variant includes all 24 frame pieces and 36 button assets: focused, unfocused, hover and pressed, with distinct toggled stick, shade and maximize controls. The XPM files are maintained directly and require no asset build step.

For Metacity 3.46+, copy this complete package to `~/.local/share/themes/Fmind/`, preserving the [theme XML](metacity-1/metacity-theme-3.xml) in its `metacity-1/` subdirectory. Metacity searches the XDG data locations instead of `~/.themes/`. If you set `XDG_DATA_HOME`, use its `themes/Fmind/` directory. Select the native Metacity theme type and name in your desktop's configuration UI, or run these commands after installing:

```sh
gsettings set org.gnome.metacity.theme name Fmind
gsettings set org.gnome.metacity.theme type metacity
```

The Metacity XML draws vector controls and covers normal, dialog, modal, utility, menu and border-only windows; focus, all resize permissions, maximize, shade, left/right tiling and their shaded combinations. Maximized windows use a distinct restore glyph. It defines menu, minimize, maximize, close, shade/unshade, above/unabove and stick/unstick controls for engines exposing them. Metacity 3.46's public renderer displays the first four controls; other engines and control layouts need separate runtime verification. Set the title font to Google Sans through your desktop's font settings. This is a Metacity XML theme, not a GNOME Shell or Mutter shell theme.

## Full bundle checklist

The [free Dracula GTK repository](https://github.com/dracula/gtk) also contains desktop-shell and window-manager themes. The catalog's GTK entry remains pending until those companions are implemented and checked.

- [x] [GTK 2 widgets](gtk-2.0/gtkrc), using the native drawing engine.
- [x] [GTK 3.20+ widgets](gtk-3.0/gtk.css).
- [x] [GTK 4 widgets](gtk-4.0/gtk.css).
- [ ] GTK 3 before 3.20.
- [ ] Application-specific widget refinements for the apps in the reference bundle.
- [x] [GNOME Shell](gnome-shell/gnome-shell.css), with [legacy image controls](gnome-shell/legacy.css).
- [x] [Cinnamon](cinnamon/cinnamon.css).
- [ ] [Complete KDE bundle](kde/README.md#bundle-checklist); color scheme and Plasma style are available, with other companions pending.
- [x] [Metacity](metacity-1/metacity-theme-3.xml).
- [x] [Xfwm](xfwm4/themerc), including HiDPI and extra-HiDPI decorations.
- [ ] Unity.

The shared color layer is maintained directly. The built-in base theme can evolve with GTK; the tested toolkit versions and validation limits are recorded in [coverage](../COVERAGE.md).
