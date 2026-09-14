# Fmind KDE

A KDE color scheme and Plasma desktop style with white surfaces, pale selections and readable semantic text. The application color scheme and the Plasma style are separate choices. This package contains the first KDE components of the free Dracula GTK bundle; the remaining components are listed below.

## Color scheme

Copy [Fmind.colors](color-schemes/Fmind.colors) to `~/.local/share/color-schemes/Fmind.colors`, then select Fmind in System Settings → Colors. The scheme includes views, windows, buttons, selections, tooltips, complementary surfaces, headers, inactive headers and window-title colors. Alternate ordinary backgrounds remain white. Inactive selections retain their pale highlight, and disabled effects keep the background white and text readable.

Neutral feedback uses amber on ordinary surfaces. Inside selections it uses the main text color because KDE's derived neutral background otherwise falls below the required contrast. The native check includes these generated semantic backgrounds, not only the RGB entries in the file.

Colors do not select an application widget style, font or icon theme. Use Google Sans for general text and Google Sans Code for fixed-width text in System Settings → Fonts. Applications that override the system palette need their own theme integration.

## Plasma style

Copy the complete `plasma/desktoptheme/Fmind/` directory to `~/.local/share/plasma/desktoptheme/Fmind/`, preserving its [metadata](plasma/desktoptheme/Fmind/metadata.json), [colors](plasma/desktoptheme/Fmind/colors), [settings](plasma/desktoptheme/Fmind/plasmarc) and SVG subdirectories. Select Fmind in System Settings → Plasma Style. Keep the installed Breeze default style: Plasma supplies its remaining control geometry and assets through the native fallback mechanism.

Fmind supplies opaque backgrounds for panels, dialogs, widgets, tooltips, toolbars and headings. Its list-item and task-button SVGs provide explicit normal, hover, selected/focused, attention, minimized and progress states, including panel orientations. Those state assets avoid inherited Breeze fills that use dark focus colors behind dark text. Blur, background contrast adjustment and adaptive transparency are disabled for this opaque style. Remaining controls use the installed Breeze assets with Fmind's colors.

The package uses the current JSON metadata format and native FrameSvg format. KDE Frameworks 5.103 was used for native loading, color evaluation and rendering. A Plasma 6/KSvg runtime, a complete Plasma desktop session, third-party widgets and arbitrary widget-style combinations remain unverified. Installing the style does not apply a desktop layout, change wallpapers or configure authentication.

## Bundle checklist

The [free Dracula KDE directory](https://github.com/dracula/gtk/tree/master/kde) includes additional independent packages. Its blue/purple and translucent/solid variants are coverage references; Fmind uses one consistent light palette and opaque ordinary surfaces.

- [x] KDE application color scheme.
- [x] Plasma desktop style, including opaque backgrounds and state assets.
- [ ] Aurorae window decorations.
- [ ] Kvantum widget theme.
- [ ] Global themes and splash screens for Plasma 5 and 6.
- [ ] Plasma 5 lock-screen, logout and OSD components from the reference bundle.
- [ ] Cursor theme.
- [ ] SDDM login-screen theme.

The parent GTK catalog entry remains pending until its full bundle is implemented and checked. See [coverage](../../COVERAGE.md) for the exact native evidence and remaining runtime boundaries.

## Maintenance

Edit the native files directly. Keep the color groups in the application scheme and Plasma `colors` file aligned; the Plasma copy intentionally omits application color-effect groups. Update the package metadata version when changing SVGs so Plasma can invalidate its cached assets. Checks isolate their configuration and caches, and never install themes into a user profile.
