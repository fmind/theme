# Fmind for VS Code

Files: [theme](fmind-color-theme.json), [manifest](package.json), [MIT license](LICENSE).

Format: [Color Theme guide](https://code.visualstudio.com/api/extension-guides/color-theme) · [Theme Color reference](https://code.visualstudio.com/api/references/theme-color)

## Installation

Keep this directory in place, for example in a clone of this repository. Run **Developer: Install Extension from Location...** from the Command Palette, select this directory, then select `fmind` in Preferences: Color Theme. Copying the directory into `~/.vscode/extensions/` does not work: VS Code loads only the extensions recorded in that folder's `extensions.json` and removes unrecorded folders.

## Cursor

[Cursor](https://cursor.com/docs/configuration/extensions) loads VS Code color themes. With Cursor running, copy this `vscode/` directory to `~/.cursor/extensions/fmind-theme` (`%USERPROFILE%\.cursor\extensions\fmind-theme` on Windows); Cursor registers a folder added there only while it runs. Reload the window (**Developer: Reload Window**), then select `fmind` in Preferences: Color Theme.

## Antigravity

Google Antigravity IDE loads VS Code color themes: run **Developer: Install Extension from Location...** from the Command Palette, select this directory, then select `fmind` in Preferences: Color Theme. In the Antigravity CLI (`agy`), keep `"colorScheme": "terminal"` in `~/.gemini/antigravity-cli/settings.json` alongside a Fmind terminal palette.
