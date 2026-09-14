# Fmind cursors

Native Xcursor files with dark shapes, white outlines and readable semantic accents. The package covers all 113 names in the [free Dracula KDE cursor bundle](https://github.com/dracula/gtk/tree/master/kde/cursors/Dracula-cursors/cursors), using 43 independent cursor designs and 70 aliases. The artwork is original Fmind geometry.

## Installation

Copy the complete [Fmind/](Fmind/) directory to `~/.local/share/icons/Fmind/`, preserving [index.theme](Fmind/index.theme), the `cursors` directory and its symbolic links. Select Fmind in KDE System Settings → Cursors, or your desktop's cursor theme chooser. Applications may need a restart to pick up the change. The Fmind global theme also selects this cursor package once it is installed.

The theme contains native sizes 24, 32, 36, 48, 64 and 96 pixels. Choose the size in your desktop settings. A single Xcursor-aware application can use `XCURSOR_THEME=Fmind XCURSOR_SIZE=32 application-command`; desktop/session settings may take precedence. Wayland compositors expose their own cursor theme controls. The format and installation layout follow [KDE's cursor documentation](https://develop.kde.org/docs/features/cursor/) and the [Xcursor library](https://xorg.freedesktop.org/archive/X11R6.9.0/doc/html/Xcursor.3.html).

Shapes include left/right/center arrows, pointing/open/closed hands, text and vertical text, crosshairs, every resize direction, splitters, movement, copy/link/help/context-menu badges, forbidden/no-drop states, pencil, color picker, zoom and a kill cursor. Wait and progress have twelve frames at 60 ms per frame; progress retains an arrow with a fixed hotspot. Common toolkit names and legacy hashed names resolve directly to the appropriate native file. Unlike the reference bundle, `size-hor`, `size-ver`, `size-fdiag` and `size-bdiag` select resize shapes; `move` uses the four-way arrow and `grabbing` uses the closed hand.

The native X11 checks use isolated Xvfb and libXcursor; Wayland compositor rendering, sandboxed application theme discovery and hardware-specific cursor limits remain unverified. Details are recorded in [coverage](../../../COVERAGE.md).

## Maintenance

Edit the standalone [SVG frames](src/) and native `.cursor` recipes directly. Each recipe lists nominal size, hotspot, raster frame path and delay. The `compile.py` helper only rasterizes those SVGs with `rsvg-convert` and compiles the recipes with `xcursorgen`; it does not generate a palette, theme design or user configuration. Install both native tools before rebuilding.

From the repository root:

```sh
uv run --locked gtk/kde/cursors/compile.py --output gtk/kde/cursors/Fmind/cursors
mise run format
mise run check
mise run screenshots
```

To verify compilation without modifying the package, pass a temporary output directory and compare its files with `Fmind/cursors/`. The helper compiles every input before copying any output and refuses to replace symbolic links. Aliases are maintained directly in the package. Keep the retained reference-name list in `checks/cursor_names.txt` aligned with the coverage baseline.
