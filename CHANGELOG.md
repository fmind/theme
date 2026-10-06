# Changelog

## Unreleased

### Fixed

- Restore palette ANSI slots in Blink Shell, iSH, Prompt and pywal: black is charcoal and bright colors match the readable normal colors.
- Correct ConEmu slot order for Cmder by sharing the ConEmu scheme, and SecureCRT ANSI white.
- Correct byte-swapped Windows color integers in EditPlus, LTspice, MetaEditor, MetaTrader 5, PL/SQL Developer and SolidWorks, and ripgrep's blue.
- Fix unreadable text: Dwarf Fortress and dircolors palettes, Qt 5 placeholders, ncspot status bar, Newsboat focus and info bars, KDiff3 input colors and Taskwarrior overdue/active tasks.
- Use dark gray for line numbers, scrollbar thumbs, sliders and essential control borders across editors, terminals and launchers.
- Align syntax roles with the palette: purple types and builtins, orange numbers, constants and warnings, charcoal variables, properties and punctuation, upright comments and medium-blue cursors.
- Fix native formats: gitk preferences and diff colors, Emacs lexical binding, Rime scheme patching and BGR colors, suckless tabbed variables, colorls keys, HexChat color triplets, The Lounge package metadata, TiddlyWiki palette type, Midnight Commander true color, xfce4-terminal cursor, Delta +/- markers, Eclipse error and deprecation cues, Plymouth script and qBittorrent resource file.
- Correct installation steps for Astro Starlight, Atom, Django Admin, Papirus Folders, ripgrep, Thunderbird, vis and zsh, man page colors on groff 1.23+, and upstream links for CadZinho, DankMaterialShell and Revolution IRC.
- Use README color names in GIMP/Inkscape and macOS palettes, the release version in userstyles, and scope the Google Search userstyle to search pages.
- Clear npm audit advisories in the JupyterLab build lock (brace-expansion, fast-uri, source-map-js) and adopt JupyterLab 4.6.4 security releases.
- Correct the blue documented in the wallpaper and banner READMEs to the generated `#174EA6`.

### Maintenance

- Update dprint, FFmpeg, Lefthook, Node.js, Python, Ruff, uv, the dprint JSON plugin and Python dependencies; migrate `mise.lock` to lockfile version 3.

## 3.0.1 — 2026-09-25

### Fixed

- Improve TTY bright-text, Light Table gutter, ptpython scrollbar and FreeCAD control contrast.
- Correct nnn palette indexes and document the matching terminal palette.
- Restore FreeCAD native dock close icons and keep Highlight.js, Prism and MacDown text upright.
- Include the MIT license in the Thonny distribution.
- Correct the ptpython installation example for its native config loader.
- Make artwork previews and manifest ordering deterministic.

### Maintenance

- Audit locked project, artwork and JupyterLab dependencies in the shared check gate; add JupyterLab Dependabot updates.
- Update Ruff, uv, VHS, the dprint JSON plugin and artwork dependencies; pin Node.js for npm audits.
- Pin FFmpeg for screenshot capture and refresh the synthetic terminal screenshots.

## 3.0.0 — 2026-09-15

### Breaking

- Move integration files from `<app>/...` to `themes/<app>/...`. Update checkout paths, raw download URLs and chezmoi external-file sources. Application destinations and existing tags are unchanged.

### Changed

- Separate validation (`checks/`) from artwork sources and generation (`artworks/`).
- Display README directly on GitHub; remove the standalone site, browser checks and Pages deployment.
- Replace app-specific validation harnesses with shared palette, structured-file, documentation and artwork checks; remove Docker and parser installation from validation.
- Add branding wallpapers and social banners with bundled Google Sans attribution.
- Correct the Standard Notes download URL and APT truecolor output.
- Improve Plasma 5 session interfaces, keyboard access and control contrast.
- List every theme alphabetically and move tool installation instructions into each theme directory.
- Simplify project documentation and add README navigation and a theme-problem form.
- Add dependency-update automation and protect version tags against modification and deletion.

Previous versions are available in [GitHub releases](https://github.com/fmind/theme/releases) and [tags](https://github.com/fmind/theme/tags).
