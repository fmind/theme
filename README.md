# fmind/theme

A light theme for code, terminals and apps, and the Fmind design system. Native files live in one folder per app under `themes/`; [DESIGN.md](DESIGN.md) describes the design for agents and design tools.

[Previews](#previews) · [Design system](#design-system) · [Palette](#palette) · [Themes](#available-themes) · [Contribute](#contribute)

[Changelog](CHANGELOG.md) · [Previous releases](https://github.com/fmind/theme/releases)

<img src="artworks/logo.png" alt="Fmind theme logo" width="120" height="120">

## Previews

| Code, shell, search and selection                    | Markdown                                        |
| ---------------------------------------------------- | ----------------------------------------------- |
| ![Neovim and Fish in Zellij](screenshots/zellij.png) | ![Markdown in Neovim](screenshots/markdown.png) |

Synthetic terminal captures made with VHS. Download [wallpapers](wallpapers/README.md) and [social banners](banners/README.md), or [preview all artwork](artworks/previews/all-variants.png).

## Design system

[DESIGN.md](DESIGN.md) is the single source for Fmind's visual identity: color roles, typography, layout, shapes, diagram components and do's and don'ts. It follows the [DESIGN.md format](https://github.com/google-labs-code/design.md) (alpha): YAML design tokens followed by prose rationale. Edit it here; consumers read it or export it instead of copying values.

It is the default for Médéric Hurier's own work. Customer or employer work uses that organization's design system, and an existing project keeps its established identity.

| Consumer                                                                    | How it uses DESIGN.md                                                                                                                                       |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Coding agents (Antigravity, Claude Code, Copilot, OpenCode)                 | [fmind/dot](https://github.com/fmind/dot) deploys a checksummed copy to `~/.agents/DESIGN.md`, and its shared `AGENTS.md` persona points every agent to it. |
| A project repository                                                        | Copy DESIGN.md to the project root, where design-aware agents look for it, or link to `~/.agents/DESIGN.md` from the project's `AGENTS.md`.                 |
| [Google Stitch](https://stitch.withgoogle.com/docs/design-md/specification) | Provide DESIGN.md as the design system for generated UI; the format originates from Stitch.                                                                 |
| Tailwind CSS v4 or v3                                                       | `npx @google/design.md@0.4.0 export --format css-tailwind DESIGN.md` emits an `@theme` block; `--format json-tailwind` emits v3 `theme.extend` JSON.        |
| Figma variables, Style Dictionary, Tokens Studio                            | `npx @google/design.md@0.4.0 export --format dtcg DESIGN.md` emits [W3C Design Tokens](https://www.designtokens.org/) JSON.                                 |
| Plain CSS (Zensical, static sites)                                          | `npx @google/design.md@0.4.0 export --format css-vars --prefix fmind DESIGN.md` emits custom properties.                                                    |
| Diagrams, decks, illustrations and demos                                    | The `fmind-visuals` and `diagrams-as-code` skills in fmind/dot adapt the tokens to D2, Mermaid, SVG, Typst and VHS.                                         |
| Terminals, editors and apps                                                 | Use the native files under `themes/`; [palette.yaml](checks/palette.yaml) maps the same colors to syntax and ANSI roles.                                    |

Validate changes with `mise run check:design`, which lints structure, token references and WCAG contrast with the design.md version pinned in `mise.toml` and fails on any warning; pre-commit and CI run it. Compare revisions with `npx @google/design.md@0.4.0 diff old.md DESIGN.md`. `mise run test` checks offline that the tokens match the palette.

## Palette

![Fmind colors and their roles](screenshots/palette.svg)

The palette uses the 15 [Google News hex colors](https://partnermarketinghub.withgoogle.com/brands/google-news/visual-identity/color-palette/) plus five complementary colors. Dark shades carry text, pale shades provide surfaces, and bright shades identify active states. Text stays upright; bold adds emphasis.

| Color                | Hex       | Syntax and text                             | Interface and backgrounds                                         |
| -------------------- | --------- | ------------------------------------------- | ----------------------------------------------------------------- |
| White                | `#FFFFFF` | Label text on dark fills                    | Main background                                                   |
| Light gray           | `#F1F3F4` | —                                           | Panels, cursor line and neutral diffs                             |
| Gray                 | `#9AA0A6` | —                                           | Decorative borders and separators                                 |
| Dark gray (custom)   | `#595D62` | Comments, gutter numbers and secondary text | Essential control borders and scrollbar thumbs; ANSI bright black |
| Charcoal             | `#202124` | Body text, variables and punctuation        | Labels on bright fills; ANSI black/white                          |
| Dark blue            | `#174EA6` | Keywords, functions, keys and headings      | Navigation and links; ANSI blue                                   |
| Medium blue          | `#4285F4` | —                                           | Cursor and active label fills                                     |
| Light blue           | `#D2E3FC` | —                                           | Selections, completions and inactive ribbons                      |
| Dark red             | `#A50E0E` | Errors and deleted text                     | Failures and deletions; ANSI red                                  |
| Medium red           | `#EA4335` | —                                           | Cut markers and error underlines                                  |
| Light red            | `#FAD2CF` | —                                           | Deletion backgrounds                                              |
| Dark orange (custom) | `#934900` | Numbers, constants and warnings             | Changes and attention; ANSI yellow                                |
| Orange               | `#E37400` | —                                           | Warning accents                                                   |
| Yellow               | `#FBBC04` | —                                           | Active tabs, current search matches and changed words             |
| Light yellow         | `#FEEFC3` | —                                           | Change backgrounds and ordinary search matches                    |
| Dark green           | `#0D652D` | Strings and added text                      | Success, additions and executables; ANSI green                    |
| Medium green         | `#34A853` | —                                           | Mode labels, copy markers and success accents                     |
| Light green          | `#CEEAD6` | —                                           | Addition backgrounds                                              |
| Purple (custom)      | `#681DA8` | Types, builtins, decorators and hints       | Secondary accents; ANSI magenta                                   |
| Teal (custom)        | `#00636D` | Informational diagnostics                   | Information and icons; ANSI cyan                                  |

## Available themes

Choose a tool for installation instructions and theme files. Each tool's README cites the upstream format its files follow. Some ports are partial, and inclusion here does not certify native application support.

- [Alacritty](themes/alacritty/)
- [Alfred](themes/alfred/)
- [Atuin](themes/atuin/)
- [Base16](themes/base16/)
- [bat](themes/bat/)
- [Beamer](themes/beamer/)
- [BetterDiscord](themes/betterdiscord/)
- [Blender](themes/blender/)
- [btop](themes/btop/)
- [Chrome](themes/chrome/)
- [Claude Code](themes/claude-code/)
- [Cmder](themes/conemu/#cmder)
- [ColorSlurp](themes/gimp/#colorslurp)
- [ConEmu](themes/conemu/)
- [Cursor](themes/cursor/)
- [delta](themes/delta/)
- [dircolors](themes/dircolors/)
- [Django Admin](themes/django-admin/)
- [DuckDuckGo](themes/duckduckgo/)
- [Dunst](themes/dunst/)
- [Eclipse](themes/eclipse/)
- [Emacs](themes/emacs/)
- [eza](themes/eza/)
- [Fastfetch](themes/fastfetch/)
- [Figma](themes/figma/)
- [Firefox](themes/firefox/)
- [Fish](themes/fish/)
- [foot](themes/foot/)
- [fzf](themes/fzf/)
- [GameMaker Studio](themes/gamemaker-studio/)
- [ggplot2](themes/ggplot2/)
- [Ghostty](themes/ghostty/)
- [GIMP](themes/gimp/)
- [Git](themes/git/)
- [GitHub](themes/github/)
- [GitHub Pages](themes/gh-pages/)
- [Gitk](themes/gitk/)
- [GitLab](themes/gitlab/)
- [GNOME Terminal](themes/gnome-terminal/)
- [GNU grep](themes/grep/)
- [Godot](themes/godot/)
- [Google Search](themes/google-search/)
- [GRUB](themes/grub/)
- [GTK](themes/gtk/)
- [GtkSourceView](themes/gtksourceview/)
- [Helix](themes/helix/)
- [Hermes Agent](themes/hermes-agent/)
- [highlight.js](themes/highlightjs/)
- [Home Assistant](themes/home-assistant/)
- [Hyprland](themes/hyprland/)
- [i3](themes/i3/)
- [IDLE](themes/idle/)
- [Inkscape](themes/inkscape/)
- [Insomnia](themes/insomnia/)
- [iTerm2](themes/iterm2/)
- [JDownloader 2](themes/jdownloader2/)
- [Jellyfin](themes/jellyfin/)
- [JetBrains](themes/jetbrains/)
- [Joplin](themes/joplin/)
- [JupyterLab](themes/jupyterlab/)
- [k9s](themes/k9s/)
- [Kate](themes/kate/)
- [Kitty](themes/kitty/)
- [Konsole](themes/konsole/)
- [Krita](themes/gtk/kde/#krita)
- [LabPlot](themes/gtk/kde/#labplot)
- [LaTeX](themes/latex/)
- [Lazydocker](themes/lazydocker/)
- [LazyGit](themes/lazygit/)
- [LibreOffice](themes/libreoffice/)
- [Logseq](themes/logseq/)
- [lsd](themes/lsd/)
- [lualine](themes/lualine/)
- [man pages](themes/man-pages/)
- [Marp](themes/marp/)
- [MATLAB](themes/matlab/)
- [Matplotlib](themes/matplotlib/)
- [Micro](themes/micro/)
- [Microsoft Edge](themes/microsoft-edge/)
- [Midnight Commander](themes/midnight-commander/)
- [Mintty](themes/mintty/)
- [MkDocs](themes/mkdocs/)
- [MySQL Workbench](themes/mysql-workbench/)
- [Neovim](themes/nvim/)
- [NetBeans](themes/netbeans/)
- [Nextcloud](themes/nextcloud/)
- [nnn](themes/nnn/)
- [Notepad++](themes/notepad-plus-plus/)
- [Obsidian](themes/obsidian/)
- [Oh My Posh](themes/oh-my-posh/)
- [Omarchy](themes/omarchy/)
- [OpenCode](themes/opencode/)
- [Pandoc](themes/pandoc/)
- [Pi Coding Agent](themes/pi-coding-agent/)
- [Polybar](themes/polybar/)
- [Powerlevel10k](themes/powerlevel10k/)
- [PowerShell](themes/powershell/)
- [Prism](themes/prism/)
- [Prompt](themes/iterm2/#prompt)
- [Pygments](themes/pygments/)
- [qBittorrent](themes/qbittorrent/)
- [Qt Creator](themes/qtcreator/)
- [Qt5 / Qt6](themes/qt5/)
- [ranger](themes/ranger/)
- [Raycast](themes/raycast/)
- [Rio](themes/rio/)
- [ripgrep](themes/ripgrep/)
- [Rofi](themes/rofi/)
- [RStudio](themes/rstudio/)
- [Slack](themes/slack/)
- [Spacemacs](themes/emacs/#spacemacs)
- [Spicetify](themes/spicetify/)
- [Spyder](themes/spyder/)
- [Stack Overflow](themes/stackoverflow/)
- [Starlight](themes/astro-starlight/)
- [Starship](themes/starship/)
- [Steam](themes/steam/)
- [Streamlit](themes/streamlit/)
- [Sublime Text](themes/sublime-text/)
- [T3 Code](themes/t3code/)
- [Tailwind](themes/tailwind/)
- [Telegram](themes/telegram/)
- [Telegram Android](themes/telegram-android/)
- [Terminal.app](themes/terminal-app/)
- [Terminator](themes/terminator/)
- [Termux](themes/termux/)
- [Textual](themes/textual/)
- [Thunderbird](themes/thunderbird/)
- [tig](themes/tig/)
- [Tilix](themes/tilix/)
- [tmux](themes/tmux/)
- [Typora](themes/typora/)
- [Unreal Engine](themes/unreal-engine/)
- [Vesktop Discord](themes/vesktop-discord/)
- [Vim](themes/vim/)
- [Vimium](themes/vimium/)
- [Visual Studio](themes/visual-studio/)
- [Vivaldi](themes/vivaldi/)
- [VS Code](themes/vscode/)
- [Wallpaper](wallpapers/README.md)
- [Warp](themes/warp/)
- [Waybar](themes/waybar/)
- [WezTerm](themes/wezterm/)
- [Windows Terminal](themes/windows-terminal/)
- [Wofi](themes/wofi/)
- [WordPress](themes/wordpress/)
- [Xfce4 Terminal](themes/xfce4-terminal/)
- [Xresources](themes/xresources/)
- [Yazi](themes/yazi/)
- [YouTube](themes/youtube/)
- [Zathura](themes/zathura/)
- [Zed](themes/zed/)
- [Zellij](themes/zellij/)
- [Zsh](themes/zsh/)
- [zsh-syntax-highlighting](themes/zsh-syntax-highlighting/)

## Contribute

Edit native files under `themes/` directly. New ports target widely used apps or developer, data and AI tools; niche apps, variants of existing ports and ports that need dependencies or build steps are declined. For a new or corrected port, add a `Format:` line to its README that links the upstream format or loader, document installation in that README, add its directory to the alphabetical list above, and test its actual colors and representative states. Report the app version and platform used; distinguish parser checks from native loading and visual testing.

Use only palette colors and keep text upright. Compute `0x` hex, decimal and Windows BGR color values carefully, because checks read only `#` hex colors. Name palette swatches with the color names above, and state the full installation destination, such as `~/.config/<app>/`, in each README.

Validation checks the palette and its contrast, the syntax of JSON, TOML, YAML, XML and plist theme files, theme `#` hex colors against the palette, release versions, a `Format:` link in every theme README, local Markdown links and anchors, and artwork integrity. Verify changed themes manually in their native apps.

Run `mise install` and `mise run install` to install tools, validation dependencies and Git hooks. Use `mise run format` to format Python and repository documentation/configuration, then `mise run all` to validate. Lefthook formats staged files in scope and runs offline checks before commits, and runs the vulnerability audit and tests before pushes. See [maintenance](AGENTS.md#maintenance) for formatting scope and tasks.

## Releases

Releases use explicitly chosen versions and immutable annotated tags. Follow the [release procedure](.agents/skills/theme-release/SKILL.md); verify CI for the release commit before tagging. Source archives are the release payload.

Maintained alongside [fmind/dot](https://github.com/fmind/dot). [MIT license](LICENSE); bundled Google Sans retains its [OFL license](artworks/OFL.txt).
