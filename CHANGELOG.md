# Changelog

## Unreleased

### Breaking

- Remove ports for apps or pages that cannot load a custom theme, user stylesheet or theme file: Bear, Couscous, Dash, Docker Desktop, Dyalog APL, EverythingToolbar, Fedilab, ForkLift, FreeTube, Gemini, GitKraken (custom themes disabled since 11.8.0), GMK, Kurozora, New Tabs, NewTerm2, Node Console, Noir, Passky, Postman, Revolt (now Stoat), RunJS, Signal Desktop, Sketch, Stirling PDF, Subsonic, Thumb-Key, Trudido, Ueli and Visual Spigot.
- Remove ports whose files used an invented, undocumented or unverified format, or CSS variables and selectors the app never reads: ABAP, Ableton Live, AdiIRC, Anne Pro 2, Aseprite, Audacity, Bandcamp, BookWyrm, ChatGPT, Cider, CodePen, DeepSeek, Delphi, Directory Opus, Dirtywave M8, Discord Bot Maker, eM Client, Files (Windows; it reads `AppTheme*BackgroundColor` settings, not a theme file), FL Studio 21, FlorisBoard, Flowlab, fman (its `Theme.css` cannot recolor the file panes), Funkwhale, Gamepad Viewer, Gitroll, Google Calendar, Homepage, HyperX NGENUITY, IBM ACS, IDA Pro, ImageGlass, ITFY, jGRASP, Kali Browser, KanbanFlow, LCD Smartie, LeetCode, LibreNMS, Linear, LTspice, macOS Color Picker, MetaEditor, Minecraft, MiXplorer, mRemoteNG, MusicBee, OneCommander, Oracle SQL Developer, Scrivener, Snappy Driver Installer, Snappy Driver Installer Origin, SnippetsLab, SOLIDWORKS, StationView, Telegram iOS, Todoist, Ulysses, Vital, Vivado, WhatsApp Web, Xcode, Yakuake and YouTube Music Desktop (now Pear Desktop).
- Remove ports for discontinued, archived or shut-down apps: Arduino Pro IDE (use the VS Code theme in Arduino IDE 2.x), Caprine Messenger, cli-visualizer, Facebook Messenger (use the Facebook userstyle), LightPaper, Nitter, Nova Launcher, Sequel Pro (use Sequel Ace), spotify-tui and Visual Basic 6.
- Remove duplicate ports: WP (use WordPress) and xdbg (use x64dbg). The folders and raw download paths of every removed port no longer exist; each remaining port's README cites the upstream format it follows.
- Replace or retire superseded theme files so each port keeps only its native format: AlphaI TUI (`fmind.json` -> `fmind.toml`), Albert (`Fmind.qss` -> `Fmind.ini`), CadZinho (`fmind.json` -> `fmind.lua`), Color Slurp (`fmind.json` removed; import the GIMP palette), Drafts (`fmind.yml` -> `fmind.draftsTheme`), GameMaker (`fmind.json` -> `fmind.tmTheme`), GitHub Pages (`_config.yml` and `assets/css/style.css` -> `assets/css/style.scss`), Heroic Games Launcher (`fmind.json` -> `fmind.css`), Homer (`fmind.css` -> `fmind.yml`), Keybr (`fmind.css` -> `fmind.user.css`), Kristall (`fmind.ini` -> `fmind.kthm`), Krita and LabPlot (`Fmind.colors` and `fmind.xml` removed; both use `themes/gtk/kde/color-schemes/Fmind.colors`), Marta (`fmind.kana` -> `Fmind.theme`), Monkeytype (`fmind.json` removed; enter the ten colors in its README), Neiki's Page Editor (`fmind.json` -> `fmind.css`), Notesnook (`fmind.css` -> `fmind.json`), novelWriter (`fmind.conf` -> `fmind.toml`, novelWriter 26.2+), Omarchy (`hyprland.conf` -> `colors.toml`), Prompt (`fmind.json` removed; import the iTerm2 colors), SecureCRT (`fmind.ini` -> `fmind.py`, SecureCRT 8.7+), Spacemacs (`fmind-theme.el` removed; uses the Emacs theme), TeXstudio (`fmind.txsCol` -> `fmind.txsprofile`), Textastic (`fmind.tmTheme` removed; uses the TextMate theme), Vivaldi (`fmind.json` removed; set the colors in its README), Vortex Mod Manager (`fmind.scss` -> `variables.scss`), Wing (`fmind.py` -> `fmind.plt`), Wox (`Fmind.xaml` -> `fmind.json`, Wox 2.4.5+) and x64dbg (`fmind.ini` -> `style.ini`).

### Added

- Distill Google UI/UX layout, progressive disclosure, interactive component (`button-secondary`, `input`, `chip`) and inline-state rules into `DESIGN.md`.

### Changed

- LaTeX: `fmindyellow` is now yellow `#FBBC04`, the former pale value moves to the new `fmindlightyellow` (`#FEEFC3`), and `fmindborder` is gray `#9AA0A6`.
- Mark the Blender preset experimental and partial.

### Fixed

- Rewrite files the app could not load in its native format: Aliucord (Themer), Amfora, Evidence (`theme.yaml`), Infinity for Reddit, JDownloader 2, MetaTrader 5, MindNode, Neiki's Editor (3.14 theme package), PeerTube (7.3+ plugin package), Pythonista, Replugged (theme folder), SideNotes, SpeedCrunch, T3 Code, TablePlus, Telegram macOS, Tower, Unigram, Wiremix and YunoHost.
- Set the variables and selectors the app actually reads in Beeper, GitLab, Jellyfin, Joplin, Keybr, Lichess, Mailspring, Miniflux, Misskey, MkDocs (Material), Nextcloud, omg.lol, Tridactyl, Tumblr, Unraid, Vesktop/Discord, Vimium and YouTube; scope the Advent of Code, AutoAO3App, Keybr and Tumblr userstyles to their sites.
- Correct ignored or invalid keys in bobthefish, GRUB (empty values made it reject the theme), Kakoune, LimeChat, Mako, NeoMutt, ncspot, Nyxt (`:action-color`, Nyxt 3.9+), Oh My Posh and Powerlevel10k (config version 4), Pandoc, PowerShell ISE, ptpython, qBittorrent, Qt (AlternateBase, LinkVisited), Qt Creator 21, Starship (`bright-green`), Tabletop Simulator, Telegram Desktop and Android, Thunderbird (add-on ID), TiddlyWiki, Visual Studio and Vortex Mod Manager.
- Fix unreadable or weak colors: Doom Emacs yellow, Eclipse CDT inactive code and brackets, Hacker News site name, highlight.js emphasis, Insomnia method and status labels, JetBrains error and warning cues, lsd tree edges and git status, MakeHuman and SDDM control borders, Spicetify surfaces and selected rows, The Lounge sidebar, Total Commander cursor, tym cursor text, xfce4-terminal selection, and medium-blue carets in Mousepad, NetBeans, RStudio, Sequel Ace and WindTerm.
- Complete or trim partial themes: add MakeHuman's missing `fmind.mht`, the GIMP palette's 20 named colors, Plymouth password prompts and boot messages, and every qBittorrent transfer and log state; reduce Stack Overflow to body colors; stop recoloring the Google Search sign-in button; drop settings Sumatra PDF, Uptime Kuma and Qt Creator never read, and DuckDuckGo's undocumented `k21` parameter.
- Correct installation steps for Arduino IDE (1.8 only), Cava, Cursor, Dev-C++, dircolors, Discourse (zip upload), Dwarf Fortress, Flarum, Forgejo, GIMP 3.2, GitHub Pages (keeps the site's `_config.yml`), Javadoc (JDK 21+), Keypirinha, Krita, LDoc, MacDown and MacDown CSS (MacDown 3000), Marp, MATLAB, Mattermost, Midnight Commander, Slack, SmartGit, Standard Notes (jsDelivr), Sumatra PDF, Telegram, The Lounge, tint2, tlrc, Unraid 7.2+, Uptime Kuma, VS Code (Install Extension from Location) and Wolfram Notebooks; state Zellij's 0.42 minimum and DankMaterialShell's new name, Dux Shell.
- Require JupyterLab 4.6.4+ and Notebook 7.6.3+ for the JupyterLab extension, the first releases that ship its `@jupyterlab/apputils` 4.7.4.
- Fix dead or wrong links for Beyond Compare 4, Cinnamon, Hyprland, Konsole, musikcube, Steam (Millennium) and Textual, and name NeoMutt, Proton Mail and Renoise correctly in the theme index.
- Align off-palette hex colors, Windows BGR integers, XML/plist structures and release versions across native theme files, and state explicit installation paths and palette color names across theme READMEs.

### Maintenance

- Expand `checks/test_repository.py` to validate XML/plist syntax, theme `#` hex colors against the palette, release versions, token references, KDE scheme copies, Markdown anchor targets and a `Format:` link in every theme README; AGENTS.md keeps a port only with a cited upstream format.
- Add `gitleaks` secret scanning of recent commits and the working tree (`check:leaks`) to `mise run check` and CI, pin `jdx/mise-action` to mise 2026.10.21 with a weekly schedule and 100-commit checkout depth, and override `glob` to 14.0.3 in the JupyterLab lockfile.
- Ignore the Thonny, NetBeans and qBittorrent build outputs, format only Python with Ruff, match `.python-version` to Python 3.14.10, and list every versioned file in the release skill.

## 4.0.0 — 2026-10-29

### Breaking

- Remove themes for discontinued or archived apps: Abricotine, Apollo, Atom, Coda, Cryptowatch, exa (use eza), Fig, Fluent Terminal, Harpy for Twitter, Light Table, MonoDevelop, Nylas N1 (use Mailspring), Postbox, Termite and XChat / HexChat. Their folders and raw download paths no longer exist.
- Remove the Rackula port: it targeted VCV Rack, and Rackula is now dark-only without custom themes.
- Move Libreddit to `themes/redlib/` as a native Redlib theme for self-hosted instances; Libreddit itself is no longer operational.

### Added

- Add `DESIGN.md`, the Fmind design system in the DESIGN.md format: color roles, typography, layout, shapes, diagram components and usage rules, with the tools that consume it. Checks keep its tokens equal to the palette and its component text at 4.5:1 contrast.

### Maintenance

- Update dprint 0.64.3 and its plugins, Lefthook, Neovim, Node.js 26.13.0, Python 3.14.10, Ruff 0.17.3, uv 0.13.6, zizmor 1.31.1, jdx/mise-action 5.2.4, Python and artwork dependencies and the JupyterLab builders; repository tasks stay on the workstation Python 3.14.
- Clear npm audit advisories in the JupyterLab build lock: override sanitize-html to 2.18.1 and update fast-uri to 3.1.9.
- Lint shipped shell scripts with ShellCheck in `mise run check`; declare the shell of sourced snippets and drop subshells from the man page colors.
- List the coding agents fmind/dot currently supports in the design system consumers.

### Fixed

- Correct native theme formats and settings for Git, aerc, lnav, Nova, Pi Coding Agent, Notepad++ and TeXworks; remove an unrecognized Sioyek setting.
- Rewrite files the app could not load in its native format: Alfred, Chatterino, Cutter, DankMaterialShell, FocusWriter, Hermes Agent, musikcube, OpenSCAD, Sequel Ace, Sequel Pro, SerenityOS, Sniffnet, Superset, tig, tut and Xournal++.
- Correct ignored or invalid keys and structure in Aseprite, Arduino IDE, Blender, castero, CopyQ, Ditto, Doom Emacs, eza, GitKraken, ghostwriter, GoAccess, KDiff3, KiCad, Logseq, MacDown, Mailspring, MySQL Workbench, NeoMutt, Nilesoft Shell, Nitter, PolyMC, presenterm, qBittorrent, spotify-tui, tint2, Ulauncher and wob; add the metadata FreshRSS, Discourse and Millennium (Steam) need to list the theme.
- Fix unreadable or wrong colors: base16 bright white and yellow slots, qutebrowser URL and match colors, Telegram hover buttons, Notepad++ VHDL comments and error lists, Total Commander cursor, CodeRunner caret and syntax, and Zed current search match.
- Restore GNOME Shell calendar event markers and close-button focus colors, and use a Qt 6 date format on the SDDM login screen.
- Correct installation steps for Home Assistant, LDoc, Monkeytype, Omarchy, Rio, Spacemacs and the apps above; remove a generic "merge fragments" note that contradicted whole-file installs.

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
