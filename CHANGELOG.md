# Changelog

## Unreleased

### Added

- Add `DESIGN.md`, the Fmind design system in the DESIGN.md format: color roles, typography, layout, shapes, diagram components and usage rules, with the tools that consume it. Checks keep its tokens equal to the palette and its component text at 4.5:1 contrast.

### Maintenance

- Update dprint, Lefthook, Neovim, Node.js, Ruff and uv to current stable releases.
- Update the locked artwork dependencies; repository tasks stay on the workstation Python 3.14.
- Update jdx/mise-action to 5.1.2 and refresh the JupyterLab build lock.
- Clear npm audit advisories in the JupyterLab build lock: override sanitize-html to 2.18.1 and update fast-uri to 3.1.9.
- List the coding agents fmind/dot currently supports in the design system consumers.
- Update dprint 0.64.3 and its Markdown plugin, Node.js 26.13.0, Python 3.14.10, Ruff 0.17.3, uv 0.13.6, zizmor 1.31.1, jdx/mise-action 5.2.4, Python dependencies, artwork dependencies and the JupyterLab builders.
- Lint shipped shell scripts with ShellCheck in `mise run check`; declare the shell of sourced snippets and drop subshells from the man page colors.

### Fixed

- Correct native theme formats and settings for Git, aerc, lnav, Nova, Pi Coding Agent, Notepad++ and TeXworks; remove an unrecognized Sioyek setting.
- Rewrite files the app could not load in its native format: Alfred, Chatterino, Cutter, DankMaterialShell, FocusWriter, Hermes Agent, musikcube, OpenSCAD, Sequel Ace, Sequel Pro, SerenityOS, Sniffnet, Superset, tig, tut and Xournal++.
- Correct ignored or invalid keys and structure in Aseprite, Arduino IDE, Blender, castero, CopyQ, Ditto, Doom Emacs, eza, GitKraken, ghostwriter, GoAccess, KDiff3, KiCad, Logseq, MacDown, Mailspring, MySQL Workbench, NeoMutt, Nilesoft Shell, Nitter, Libreddit, PolyMC, presenterm, qBittorrent, spotify-tui, tint2, Ulauncher and wob; add the metadata FreshRSS, Discourse and Millennium (Steam) need to list the theme.
- Fix unreadable or wrong colors: base16 bright white and yellow slots, qutebrowser URL and match colors, Telegram hover buttons, Notepad++ VHDL comments and error lists, Total Commander cursor, CodeRunner caret and syntax, and Zed current search match.
- Restore GNOME Shell calendar event markers and close-button focus colors, and use a Qt 6 date format on the SDDM login screen.
- Correct installation steps for Home Assistant, LDoc, Light Table, Monkeytype, Omarchy, Rio, Spacemacs and the apps above; remove a generic "merge fragments" note that contradicted whole-file installs.

## 3.0.2 — 2026-10-06

### Fixed

- Restore palette ANSI slots in Blink Shell, iSH, Prompt and pywal: black is charcoal and bright colors match the readable normal colors.
- Correct ConEmu slot order for Cmder by sharing the ConEmu scheme, and SecureCRT ANSI white.
- Correct miscomputed Windows BGR color integers in EditPlus, LTspice, MetaEditor, MetaTrader 5, PL/SQL Developer and SolidWorks, and ripgrep's blue.
- Fix unreadable text: Dwarf Fortress and dircolors palettes, Qt 5 placeholders, ncspot status bar, Newsboat focus and info bars, KDiff3 input colors and Taskwarrior overdue/active tasks.
- Use dark gray for line numbers, scrollbar thumbs, sliders and essential control borders across editors, terminals and launchers.
- Align syntax roles with the palette: purple types and builtins, orange numbers, constants and warnings, charcoal variables, properties and punctuation, upright comments and medium-blue text cursors and carets.
- Fix native formats: gitk preferences and diff colors, Emacs lexical binding, Rime scheme patching and BGR colors, suckless tabbed variables, colorls keys, HexChat color triplets, The Lounge package metadata, TiddlyWiki palette type, Midnight Commander true color, xfce4-terminal cursor, Delta +/- markers, Eclipse error and deprecation cues, Plymouth script and qBittorrent resource file.
- Correct installation steps for Astro Starlight, Atom, Django Admin, Papirus Folders, ripgrep, Thunderbird, vis and zsh, man page colors where groff emits SGR escapes, and upstream links for CadZinho, DankMaterialShell and Revolution IRC.
- Keep HexChat chat colors readable on white and ship them as the `colors.conf` HexChat reads.
- Remove non-color settings from the Sumatra PDF fragment.
- State explicit `~/.config` destinations in theme READMEs instead of a shared relative-path note.
- Use README color names in GIMP/Inkscape and macOS palettes, the release version in userstyles, and scope the Google Search userstyle to search pages.
- Clear npm audit advisories in the JupyterLab build lock (brace-expansion, fast-uri, source-map-js) and adopt JupyterLab 4.6.4 security releases.
- Correct the blue documented in the wallpaper and banner READMEs to the generated `#174EA6`.

### Maintenance

- Update dprint and its JSON, Markdown and TOML plugins, FFmpeg, Lefthook, Node.js, Python, Ruff, uv, jdx/mise-action 5.1.1, Python dependencies and the JupyterLab build lock; migrate `mise.lock` to lockfile version 3.
- Remove the obsolete GitHub Pages site and repository homepage left from 2.x.

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
