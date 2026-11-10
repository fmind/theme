# Changelog

## Unreleased

### Breaking

- Remove Termux (`themes/termux/colors.properties`): Termux is Android-only, outside the Linux and macOS catalog scope; version 9.0.0 keeps it.
- OpenCode: migrate [OpenCode](themes/opencode/) (`themes/opencode/fmind.json`) to the OpenCode 2.x V2 theme format (`base` and `light` palettes, configured in `~/.config/opencode/cli.json`); OpenCode 1.x is no longer supported.

### Added

- [GitHub Copilot CLI](themes/copilot/) (`"theme": "default"` terminal inheritance) and [Antigravity](themes/vscode/#antigravity) IDE and CLI instructions.
- [jq](themes/jq/) truecolor `JQ_COLORS` snippet matching the syntax roles, and [fd](themes/dircolors/#fd) `LS_COLORS` instructions under [dircolors](themes/dircolors/).

### Fixed

- DESIGN.md and generated CSS/Tailwind tokens: quote `lineHeight` values so `@google/design.md` exports all nine `--leading-*` variables, and document `@theme` font, border and `max-w-*` precedence details in the CSS and Tailwind READMEs.
- pgcli: replace `noreverse` (rejected by Pygments' color parser) with `noinherit` on current completions and selections, and set `scrollbar.background` and `scrollbar.button` next to dark gray `#595D62` thumbs.
- Django Admin: theme buttons, messages, errors and secondary surfaces with palette colors, set `--hairline-color` to `#9AA0A6` so borders stay visible on `#F1F3F4`, set the Google Sans font variables, and keep `.selector-chosen` and `.calendar` headers white on `#174EA6`.
- Zensical: map `--md-code-hl-constant-color` (used by Material's highlight stylesheet for Python builtins and `self`) to purple `#681DA8`, bold literal constants `.kc` and `.no` in `#934900`, bold keywords and tags in `#174EA6`, and keep inline code `#174EA6` and captions upright.
- Hermes Agent: set `voice_status_bg`, `shell_dollar` and all seven `status_bar_*` foreground keys so dark-skin yellow and silver defaults never appear on `#F1F3F4`.
- Starlight, JupyterLab and Streamlit: keep Starlight light-mode contrast order, Google Sans fonts, `#174EA6` inline code and `#595D62` control borders; remove black drop shadows and fix cell borders, code blocks and collaborator series order in JupyterLab; add fonts, radii, dataframe borders and semantic status colors in Streamlit.
- Mermaid and D2: set Mermaid's `dagre` layout, white flowchart nodes on `#F1F3F4` clusters, green `diagram-actor` fills, charcoal state terminals, ER zebra rows and `xyChart` categorical series; set 1px strokes on D2 `group`, `component`, `external` and `step` classes to match DESIGN.md.
- Shell and CLI tools: complete `eza` `multi_link_file`, group permissions, git and non-dimmed metadata; replace `yazi` `prepend_dirs` with all 14 preset `dirs` and add hovered `orphan`/`dummy` icon rules; align `fish` `fmind.fish` and `fmind.theme` twins; convert `grep` `GREP_COLORS` to palette truecolor SGR; complete `btop`, `delta`, `fzf`, `git`, `glamour`, `k9s`, `lsd`, `starship` and `zsh-syntax-highlighting` role colors.
- Editors and terminals: align Markdown headings (`H1`–`H3` dark blue, `H1`–`H6` bold), blue links, fenced code blocks and `@module` in Neovim; refine TextMate scopes and semi-transparent scrollbars in `bat` and VS Code; override inherited low-contrast and italic `Default` attributes in JetBrains; add Helix bufferline and bright diagnostic curls, Zed 6-player categorical colors and semi-transparent active search match, `lualine` muted inactive segments, Vim 9 highlight groups, Alacritty `footer_bar`, iTerm2 `Match Background Color`, tmux copy-mode and menu styles, WezTerm copy-mode and quick-select colors, and Zellij categorical player order.
- Documentation: update Pi Coding Agent, Chrome (Vivaldi URL), fzf, bat, k9s, LazyGit, Lazydocker, man-pages, Alacritty, tmux, Warp, WezTerm, Vim and Zellij READMEs with explicit paths and current links.

### Maintenance

- Guard truecolor ANSI SGR sequences (`38`, `48` and `58` RGB) and `.dircolors`, `LS_COLORS`, `GREP_COLORS` and `JQ_COLORS` SGR parameters against off-palette or malformed codes in `checks/test_repository.py`, enable fenced code highlighting in `screenshots/editor.lua` and refresh the terminal screenshots.
- Update `markdown` 3.11.3, the dprint JSON 0.26.0, Markdown 0.29.0 and TOML 0.10.0 plugins, and `jdx/mise-action` to mise 2026.11.6.

## 9.0.0 — 2026-11-09

### Breaking

- Focus the catalog on what Fmind uses: a port stays when fmind/dot deploys it, a Fmind project renders with it, or it is a leading developer, data or AI tool on Linux or macOS. 88 ports for consumer, chat, media and game apps, desktop environments, website userstyles, Windows-only apps and tools outside that stack are removed, and their `themes/<app>/` raw download paths no longer exist; version 8.0.1 keeps them. Removed: `alfred`, `beamer`, `betterdiscord`, `blender`, `conemu`, `duckduckgo`, `dunst`, `eclipse`, `emacs`, `figma`, `firefox`, `foot`, `gamemaker-studio`, `ggplot2`, `gh-pages`, `gimp`, `github`, `gitk`, `gitlab`, `gnome-terminal`, `godot`, `google-search`, `grub`, `gtk`, `gtksourceview`, `home-assistant`, `hyprland`, `i3`, `idle`, `insomnia`, `jdownloader2`, `jellyfin`, `joplin`, `kate`, `konsole`, `latex`, `libreoffice`, `logseq`, `marp`, `matlab`, `micro`, `midnight-commander`, `mintty`, `mysql-workbench`, `nextcloud`, `nnn`, `notepad-plus-plus`, `obsidian`, `oh-my-posh`, `omarchy`, `pandoc`, `polybar`, `powerlevel10k`, `powershell`, `qt5`, `qtcreator`, `ranger`, `raycast`, `rio`, `rofi`, `rstudio`, `slack`, `spicetify`, `spyder`, `stackoverflow`, `steam`, `sublime-text`, `telegram`, `telegram-android`, `terminator`, `textual`, `thunderbird`, `tig`, `tilix`, `typora`, `unreal-engine`, `vesktop-discord`, `vimium`, `visual-studio`, `waybar`, `windows-terminal`, `wofi`, `wordpress`, `xfce4-terminal`, `xresources`, `youtube`, `zathura`, `zsh`. Their README sections for Cmder, ColorSlurp, Inkscape, Krita, LabPlot and Spacemacs go with them.
- MkDocs is now [Zensical](themes/zensical/): `themes/mkdocs/fmind.css` moves to `themes/zensical/fmind.css`, which also serves [Material for MkDocs](themes/zensical/#material-for-mkdocs). The stylesheet now applies to the `default` (light) scheme only, so set `scheme: default` with `primary: custom` and `accent: custom`.
- Tailwind: the v3 preset `themes/tailwind/fmind.js` is replaced by `themes/tailwind/fmind.css`, a Tailwind CSS v4 `@theme` file generated from DESIGN.md. Colors use the DESIGN.md token names (`fmind-ground` becomes `canvas`, `fmind-text` becomes `foreground`, `fmind-accent` becomes `focus`), and the file adds the type, radius and spacing tokens.
- Fold duplicate ports into the port whose files they use; their folders and raw download paths no longer exist. Cursor is now a section of [VS Code](themes/vscode/#cursor) (its theme file was identical), and Microsoft Edge and Vivaldi of [Chrome](themes/chrome/#microsoft-edge).
- Remove NetBeans and qBittorrent: both needed a build step (`zip`, `rcc`) before the app could load them.

### Added

- [D2](themes/d2/): an import that sets theme overrides, a white canvas, dark blue connections and the seven `diagram-*` classes of DESIGN.md, so unclassed shapes use palette colors too.
- [Mermaid](themes/mermaid/): a configuration file for the `base` theme that covers flowchart, sequence, state, class, entity, Gantt, pie, mindmap, timeline and Git diagrams.
- [VHS](themes/vhs/): a theme tape with the Ghostty colors, cursor and selection; this repository's screenshots now record with it.
- [CSS](themes/css/) custom properties and a [daisyUI](themes/daisyui/) 5 theme, next to the Tailwind file. `mise run tokens` regenerates the CSS and Tailwind files from DESIGN.md, and `mise run check:design` fails when they are stale.
- [DuckDB](themes/duckdb/) CLI highlighting, [pgcli](themes/pgcli/) menus, toolbar and query syntax, and a [Glamour](themes/glamour/) style for Markdown in the [GitHub CLI](themes/glamour/#github-cli).
- DESIGN.md: the order of categorical chart series (dark blue, teal, dark orange, purple, dark green, dark red) and chart axis rules.

### Fixed

- Zensical: code blocks use the Fmind syntax colors, and marks, keys, tables and the classic footer use palette colors.
- Pygments: constants and `True`, `False` and `None` are bold dark orange, tags bold dark blue, and regular expressions and interpolations dark blue, as in Neovim.
- highlight.js and Prism: regular expressions are dark blue and booleans bold, as in Neovim; highlight.js links are dark blue, and Prism keywords and constants are bold.
- Matplotlib and Streamlit: chart series follow the DESIGN.md order, so red and green no longer sit next to each other in second and third place.
- Terminal.app: the cursor is medium blue `#4285F4`, as in the other terminals.
- Contrast: control borders use dark gray `#595D62` in Django Admin and Streamlit; gray `#9AA0A6` no longer carries text in Vim (`NonText`, `SpecialKey`).
- Semantics: hint diagnostics are purple in VS Code and Helix; Prism operators are charcoal, CSS strings green and namespaces fully opaque; highlight.js decorators are purple and interpolations charcoal; Vim conditionals, loops and labels are bold like other keywords, and exceptions are red.
- Vim, Helix and Zed: named constants and booleans are bold dark orange, and Zed tags are bold, as in Neovim, bat and VS Code.
- lsd and LazyGit use palette hex colors instead of ANSI color names, so they no longer depend on the terminal palette.
- tmux: drop `pane-border-format`, a layout setting.
- Installation: Claude Code (settings file) and Lazydocker (path).

### Maintenance

- README lists the catalog by category and maps each kind of output (page, documentation site, diagram, chart, recording) to its ready-made file.
- Add the `theme-port` skill for adding, fixing and removing ports; the release skill covers the generated token files.
- Checks require every port to appear once in its README category, in alphabetical order, and fail when two ports ship a byte-identical theme file; tests that matched no remaining file are removed.
- Artwork SVGs embed the logo once instead of twice (1.1 MB each instead of 2.2 MB; the PNG exports are byte-identical), and the generator no longer needs Typer and Rich (2 locked packages instead of 10).
- Remove the unused `check:leaks:full` task and the redundant CI install step, format `.github/jactionlint.yaml`, and capture screenshots with the data-only fish theme.
- Theme READMEs share one title (`Fmind for <app>`) and one `Installation` heading.
- Python stays at 3.14.10: PyYAML 6.0.3, the latest release, ships no Python 3.15 wheel.

## 8.0.1 — 2026-11-07

### Maintenance

- Enable cosign and GitHub attestation verification in `mise.toml` `[settings]`, matching CI's defaults, so a full `mise lock` works on machines that turn them off globally.

## 8.0.0 — 2026-11-07

### Breaking

- Focus the catalog on widely used apps and developer, data and AI tools: 206 niche, duplicate or discontinued ports are removed, and their `themes/<app>/` raw download paths no longer exist. Removed: `adminer`, `adobe`, `adventofcode`, `aerc`, `albert`, `aliucord`, `alphai-tui`, `amfora`, `anytype`, `apt`, `archive-of-our-own`, `arduino-ide`, `auto-ao3-app`, `bashtop`, `bbedit`, `beeper`, `bemenu`, `bettercanvas`, `beyond-compare-4`, `blink-shell`, `blockbench`, `bobthefish`, `bottom`, `brackets`, `bspwm`, `btcpay-server`, `cadzinho`, `calibre`, `campfire`, `castero`, `cava`, `chatterino`, `clone-hero`, `codeblocks`, `codeforces`, `coderunner`, `colorls`, `copyq`, `cosmic-terminal`, `coteditor`, `cutter`, `dankmaterialshell`, `dev-cpp`, `discourse`, `ditto`, `dmenu`, `doom-emacs`, `dracula-css`, `drafts`, `duolingo`, `dwarf-fortress`, `editplus`, `evidence`, `facebook`, `flarum`, `fluxbox`, `focuswriter`, `fontforge`, `forgejo`, `freecad`, `freshrss`, `fuzzel`, `gajim`, `geany`, `gedit`, `gh-dash`, `ghostwriter`, `go-access`, `hacker-news`, `heroic-games-launcher`, `homer`, `i3lock-color`, `infinity-for-reddit`, `ish`, `jabref`, `javadoc`, `jupyter-notebook`, `kagi`, `kakoune`, `kdiff3`, `keybr`, `keypirinha`, `kicad`, `kristall`, `ldoc`, `leftwm`, `lichess`, `limechat`, `liteide`, `lnav`, `lxterminal`, `macdown`, `macdown-css`, `mailspring`, `makehuman`, `mako`, `mantine`, `markdown-css`, `marta`, `mattermost`, `metatrader5`, `mindnode`, `miniflux`, `misskey`, `mobaxterm`, `monkeytype`, `mousepad`, `musikcube`, `mutt`, `ncspot`, `neiki-editor`, `neiki-page-editor`, `newsboat`, `nilesoft-shell`, `notesnook`, `nova`, `novel-writer`, `nyxt`, `omglol`, `openbox`, `openscad`, `p10k-oh-my-posh`, `pantheon-terminal`, `papirus-folders`, `peacock-extension`, `peertube`, `plank`, `plsql-developer`, `plymouth`, `polymc`, `powershell-ise`, `presenterm`, `protonmail`, `psychopy`, `ptpython`, `pythonista`, `pywal`, `qterminal`, `quassel`, `quiver`, `qutebrowser`, `r`, `readwise-reader`, `redlib`, `renoise`, `replugged`, `revolution-irc`, `rime`, `ripcord`, `roam-research`, `sandpack`, `securecrt`, `sequel-ace`, `serenityos`, `sidenotes`, `sioyek`, `smartgit`, `sniffnet`, `speedcrunch`, `st`, `standard-notes`, `starship-powerline-preset`, `suckless-tabbed`, `sumatra-pdf`, `superset`, `swaylock`, `swaync`, `swayosd`, `swiftui`, `tableplus`, `tabletop-simulator`, `taskwarrior`, `telegram-macos`, `telegram-x`, `texshop`, `texstudio`, `textmate`, `texworks`, `thelounge`, `thonny`, `tiddlywiki`, `tint2`, `tlrc`, `tofi`, `total-commander`, `tower`, `tridactyl`, `tty`, `tumblr`, `tut`, `tym`, `ulauncher`, `unigram`, `unraid`, `uptime-kuma`, `vis`, `vortex-mod-manager`, `windterm`, `wing`, `wiremix`, `wob`, `wolfram-notebooks`, `wox`, `x64dbg`, `xournalpp`, `yunohost`. The README Textastic entry, which pointed to the TextMate port, is removed too.
- Thonny is removed with its plugin package and build step; uninstall `thonny-fmind` from Tools → Manage plug-ins.

### Maintenance

- Lint DESIGN.md in `mise run check` (pre-commit and CI) with design.md 0.4.0 pinned in mise and its npm dependencies locked under `.mise/locks/`; any lint warning, such as low contrast, now fails the gate. Node.js, previously used only for the removed JupyterLab build, now runs the linter.

## 7.0.0 — 2026-11-07

### Breaking

- JupyterLab: the theme is now `themes/jupyterlab/custom.css`, a user stylesheet that restyles JupyterLab Light in JupyterLab (started with `--custom-css`) and Notebook 7, without an extension or build. The `jupyterlab-fmind` extension package, its npm lockfile and its build files are removed. Uninstall the extension with `python -m pip uninstall jupyterlab-fmind` and choose JupyterLab Light in Settings → Theme.
- Remove Hyper: its upstream repository, vercel/hyper, is archived, and its last release is 3.4.1 from January 2023. `themes/hyper/` and its raw download paths no longer exist.

## 6.0.2 — 2026-11-07

### Fixed

- Openbox: title labels, buttons, handles and grips no longer fall back to solid black, and inactive button glyphs and disabled menu items are visible.
- Unreal Engine: title bars, foldouts and the deepest panels use light surfaces instead of near-black under dark text; selection, hover, status and accent colors are now defined.
- WordPress: admin bar labels and icons, and admin menu icons, are readable on the light bar and menu.
- Partial themes now cover the rest of the app: the qutebrowser command, mode, prompt, download, hint and message bars; lnav's status bar, cursor line and popups; the remaining vis base styles; MySQL Workbench brace matching, placeholders and `/*! */` hidden commands; TiddlyWiki sidebar, tabs, tags and editor; and Astro Starlight body text, inline code and hairlines.
- Contrast: input and control borders use dark gray `#595D62` in neiki-editor, neiki-page-editor, Thonny, Vimium, WindTerm and wofi; Adminer table grid lines, bashtop dividers and gradients, and the first cava bar color are visible on white; MkDocs link hover uses dark blue.
- Semantics: Prism tags are blue and attribute values green; NetBeans XML and Tomcat errors use pale red; Qt Creator output pane toggles and flashes follow the palette; MySQL Workbench variables use the text color; WindTerm session color tags are distinct again; CotEditor invisibles and Newsboat backgrounds no longer inherit off-palette defaults.
- Installation: complete paths or steps for Chatterino, delta, GRUB (PF2 font), lnav, Nilesoft Shell, NeoMutt, Rime, sioyek, Starship, Tridactyl and Visual Studio, and note truecolor or Nerd Font needs for Zsh and the Starship powerline preset. The Anytype loader citation points to its current source.

## 6.0.1 — 2026-11-07

### Fixed

- bat: color diff file headers, hunk ranges and the `+`/`-` markers, which rendered as plain text.
- Git: `git status -sb` shows the local branch in blue and the remote in green, like the other branch views.
- OpenCode: hovered dialog items use pale blue, distinct from the panel, and `$schema` points to the current schema; the previous URL returned 404.

## 6.0.0 — 2026-11-07

### Breaking

- Remove the README-only folders `themes/cmder/`, `themes/color-slurp/`, `themes/krita/`, `themes/labplot/`, `themes/prompt/`, `themes/spacemacs/`, `themes/textastic/` and `themes/wallpaper/`. Their install steps move to a section of the theme they use: ConEmu, GIMP, KDE, [iTerm2](themes/iterm2/#prompt), Emacs, TextMate (removed in a later release) and [wallpapers](wallpapers/README.md). The theme index still lists every app.
- Ghostty: the theme sets `faint-opacity`, so it requires Ghostty 1.2.0 or later.

### Added

- Fish: `themes/fish/fmind.theme`, a data-only theme loaded with `fish_config theme choose fmind`, is now the recommended install. `fmind.fish` remains available.

### Changed

- `label-md` labels are semibold (600) sentence case with normal tracking, replacing bold all-caps with wide tracking, a common tell of generated designs.
- Neovim: hint diagnostics and the builtin variables, parameters and modules (`self`, `cls`) use purple, as the palette documents; the indent scope guide is dark blue and plain guides are gray.
- fzf and LazyGit: inactive borders and separators use dark gray `#595D62`, which meets 3:1 on white.

### Fixed

- Git: remove `color.diff.context`, which made delta print unchanged lines without syntax highlighting, and show whitespace errors as a solid red cell instead of pale red on gray.
- Ghostty: faint (SGR 2) text keeps 5:1 contrast on white.
- Neovim: make the Trouble cursor line, bufferline selection, Mason and Octo text readable, and stop Trouble from painting white strips in its panel.
- Zellij: hovered tabs and status-bar items show pale yellow behind readable text instead of dark text on a dark fill.
- LazyGit: set `gui.colorScheme: light`, so a terminal that does not report its background no longer gets dark defaults, and style the selected line in unfocused views.
- Yazi: fallback icons use Fmind colors that stay readable on white, and broken symlinks get a red row again.

## 5.0.0 — 2026-10-31

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
