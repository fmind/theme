# fmind/theme

A light theme for everyday code and terminal work, with 69 app integrations. One folder per app, native theme files, no generator.

## Palette

![Fmind colors and their roles](screenshots/palette.svg)

All 20 colors are used. A dash means no role in that column.

| Color | Hex | Syntax and text | Interface and backgrounds |
| --- | --- | --- | --- |
| White | `#FFFFFF` | Label text on dark fills | Main background |
| Light gray | `#F1F3F4` | — | Panels, cursor line and neutral diffs |
| Gray | `#9AA0A6` | bat gutter numbers | Borders and scrollbar |
| Dark gray (custom) | `#595D62` | Comments and secondary text | Muted labels; ANSI bright black |
| Charcoal | `#202124` | Body text, variables and punctuation | Labels on bright fills; ANSI black/white |
| Dark blue | `#174EA6` | Keywords, functions, keys and headings | Navigation and links; ANSI blue |
| Medium blue | `#4285F4` | — | Cursor, tabs and label fills |
| Light blue | `#D2E3FC` | — | Selections and completions |
| Dark red | `#A50E0E` | Errors and deleted text | Failures and deletions; ANSI red |
| Medium red | `#EA4335` | — | Cut markers and error underlines |
| Light red | `#FAD2CF` | — | Deletion backgrounds |
| Dark orange (custom) | `#934900` | Numbers, constants and warnings | Changes and attention; ANSI yellow |
| Orange | `#E37400` | — | Search and warning accents |
| Yellow | `#FBBC04` | — | Active tabs, search matches and changed words |
| Light yellow | `#FEEFC3` | — | Change backgrounds |
| Dark green | `#0D652D` | Strings and added text | Success, additions and executables; ANSI green |
| Medium green | `#34A853` | — | Mode labels, copy markers and success accents |
| Light green | `#CEEAD6` | — | Addition backgrounds |
| Purple (custom) | `#681DA8` | Types, builtins, decorators and emphasis | Secondary accents; ANSI magenta |
| Teal (custom) | `#00636D` | Informational diagnostics | Information and icons; ANSI cyan |

Dark shades carry text; bright shades carry fills and accents. Syntax and comments meet 4.5:1 on white, panels, selections and diffs. Bold distinguishes staged Git signs.

Recommended terminal font: **GoogleSansCode Nerd Font Mono**. Text stays upright; bold adds emphasis.

## Screenshots

| Code, shell, search and selection | Markdown |
| --- | --- |
| ![Neovim and Fish in Zellij, including search and selected code](screenshots/zellij.png) | ![Markdown syntax in Neovim](screenshots/markdown.png) |

Captured with VHS using synthetic examples.

## Install

Use a truecolor terminal with a light background. Paths are relative to `~/.config` or your app's configured directory. Merge fragments into existing settings.

| Tool | Theme file | Installation |
| --- | --- | --- |
| Alacritty | [fmind.toml](alacritty/fmind.toml) | Copy to `alacritty/themes/fmind.toml`; add it to `[general] import = ["~/.config/alacritty/themes/fmind.toml"]`. |
| Atuin | [fmind.toml](atuin/fmind.toml) | Copy to `atuin/themes/fmind.toml`; set `[theme] name = "fmind"` in `atuin/config.toml`. |
| bat | [fmind.tmTheme](bat/fmind.tmTheme) | Copy to the `themes/` directory under `bat --config-dir`; run `bat cache --build`, then select `--theme=fmind`. |
| bottom | [fmind.toml](bottom/fmind.toml) | Merge `[styles]` and its sections into `bottom/bottom.toml`. |
| btop | [fmind.theme](btop/fmind.theme) | Copy to `btop/themes/fmind.theme`; select `fmind` in Options or set `color_theme = "fmind"` in `btop/btop.conf`. |
| Chrome | [manifest.json](chrome/manifest.json) | Open `chrome://extensions`, enable Developer mode, choose Load unpacked, and select `chrome/`. Styles browser chrome and the new-tab page, not websites. |
| ConEmu | [fmind.xml](conemu/fmind.xml) | Save a custom Fmind scheme in Settings → Features → Colors, then close ConEmu. In `ConEmu.xml`, replace that saved `PaletteN` key’s values with this file’s values, retaining its `PaletteN` key name. Reopen and select Fmind. Slot 15 is reserved for the white canvas; ANSI bright-white text needs an app override. |
| delta | [fmind.gitconfig](delta/fmind.gitconfig) | Include from Git configuration; install the bat theme first. |
| Dunst | [fmind.conf](dunst/fmind.conf) | Merge into `dunst/dunstrc`, then reload Dunst. Includes all three urgency levels. |
| Emacs | [fmind-theme.el](emacs/fmind-theme.el) | Copy to `~/.emacs.d/themes/`, add that directory to `custom-theme-load-path`, then use `M-x load-theme` → `fmind`. |
| Fastfetch | [fmind.json](fastfetch/fmind.json) | Merge `display.color` into `fastfetch/config.jsonc`. |
| Firefox | [manifest.json](firefox/manifest.json) | For local testing, use `about:debugging` → This Firefox → Load Temporary Add-on and select the manifest. Lasts until restart; permanent installation requires Mozilla signing. Styles browser UI, not websites. |
| Fish | [fmind.fish](fish/fmind.fish) | Copy to `fish/conf.d/fmind.fish`. |
| foot | [fmind.ini](foot/fmind.ini) | For foot 1.28+, copy to `foot/themes/fmind.ini`; add `include=~/.config/foot/themes/fmind.ini` before any section in `foot/foot.ini`. The fragment selects the light palette. |
| fzf | [fmind.conf](fzf/fmind.conf) | Set `FZF_DEFAULT_OPTS_FILE` to this file’s absolute path. |
| Geany | [fmind.conf](geany/fmind.conf) | Copy to `geany/colorschemes/fmind.conf`; choose View → Change Color Scheme → Fmind. Covers shared language styles and editor decorations. |
| Gedit | [fmind.xml](gedit/fmind.xml) | Copy to `~/.local/share/gtksourceview-4/styles/` and select Fmind in Preferences → Font & Colors. GtkSourceView 5 apps use `gtksourceview-5/styles/`. |
| gh-dash | [fmind.yml](gh-dash/fmind.yml) | Merge `theme` into `gh-dash/config.yml`. |
| Ghostty | [fmind](ghostty/fmind) | Copy to `ghostty/themes/fmind`; set `theme = fmind`. |
| GNOME Terminal | [fmind.dconf](gnome-terminal/fmind.dconf) | Import into a chosen profile with the scoped command below. The fragment only changes colors. |
| Helix | [fmind.toml](helix/fmind.toml) | Copy to `helix/themes/fmind.toml`; set `theme = "fmind"` in `helix/config.toml`. |
| Hyper | [fmind.json](hyper/fmind.json) | Copy beside `.hyper.js`; merge `...require("./fmind.json")` into its `config` object. Use Hyper’s Edit → Preferences to locate the config. |
| i3 | [fmind.conf](i3/fmind.conf) | Copy to `i3/fmind.conf`; add `include ~/.config/i3/fmind.conf` to the i3 config, then reload. Styles window borders and titles; your bar configuration stays separate. |
| IDLE | [fmind.cfg](idle/fmind.cfg) | With IDLE closed, merge the `[Fmind]` section into `~/.idlerc/config-highlight.cfg`. Reopen, then Options → Configure IDLE → Highlights → Custom Theme → Fmind. Restart to update the cursor. |
| iTerm2 | [fmind.itermcolors](iterm2/fmind.itermcolors) | Import through Settings → Profiles → Colors → Color Presets, then select `fmind`. |
| JetBrains | [fmind.icls](jetbrains/fmind.icls) | Settings → Editor → Color Scheme → gear menu → Import Scheme. Select `fmind` and a light IDE appearance. Covers language defaults, editor and console; not a UI plugin. |
| k9s | [fmind.yaml](k9s/fmind.yaml) | Copy to the skins directory shown by `k9s info`; select `k9s.ui.skin: fmind` in its config. |
| Kate | [fmind.theme](kate/fmind.theme) | Settings → Configure Kate → Color Themes → Import. Select Fmind. Also usable by KSyntaxHighlighting applications. |
| Kitty | [fmind.conf](kitty/fmind.conf) | Copy to `kitty/themes/fmind.conf`; add `include themes/fmind.conf` to `kitty/kitty.conf`. |
| Konsole | [fmind.colorscheme](konsole/fmind.colorscheme) | Copy to `~/.local/share/konsole/fmind.colorscheme`; select `fmind` under Edit Profile → Appearance. Selection and cursor use Konsole’s profile behavior. |
| Lazydocker | [fmind.yml](lazydocker/fmind.yml) | Merge `gui.theme` into Lazydocker’s `config.yml`. |
| LazyGit | [fmind.yml](lazygit/fmind.yml) | Merge `gui.theme` into the config directory shown by `lazygit --print-config-dir`. |
| lsd | [fmind.yaml](lsd/fmind.yaml) | Copy to `lsd/colors.yaml`; set `color.theme: custom` in `lsd/config.yaml`. |
| lualine | [fmind.lua](lualine/fmind.lua) | Copy to `nvim/lua/lualine/themes/fmind.lua`; select `fmind` or `auto`. |
| Matplotlib | [fmind.mplstyle](matplotlib/fmind.mplstyle) | Use `plt.style.use("/path/to/fmind.mplstyle")`, or copy to `stylelib/` under `matplotlib.get_configdir()` and use `plt.style.use("fmind")`. |
| Micro | [fmind.micro](micro/fmind.micro) | Copy to `micro/colorschemes/fmind.micro`; run `set colorscheme fmind` in the Ctrl-E command prompt. Requires truecolor. |
| Mintty | [fmind.minttyrc](mintty/fmind.minttyrc) | Merge into `~/.minttyrc` or load the file with `mintty -C /path/to/fmind.minttyrc`. |
| MobaXterm | [fmind.ini](mobaxterm/fmind.ini) | Close MobaXterm; merge `[Colors]` into `MobaXterm.ini` (its location is shown in Settings → Configuration → General). Reopen. Per-session color settings can override global colors. |
| Neovim | [fmind.lua](nvim/colors/fmind.lua) | Copy to `nvim/colors/fmind.lua`; use `colorscheme fmind`. |
| Obsidian | [theme.css](obsidian/theme.css), [manifest.json](obsidian/manifest.json) | Copy both into your vault’s `.obsidian/themes/Fmind/`; select Fmind and the Light base color scheme in Appearance. |
| OpenCode | [fmind.json](opencode/fmind.json) | Copy to `opencode/themes/fmind.json`; select `fmind` through `/theme`. |
| PowerShell | [fmind.ps1](powershell/fmind.ps1) | Dot-source from `$PROFILE`: `. "/path/to/fmind.ps1"`. Requires PowerShell 7, PSReadLine 2.2+, and a matching truecolor terminal. Colors the interactive input line and suggestions. |
| ptpython | [fmind.py](ptpython/fmind.py) | Load `CODE` and `UI` in `config.py`; register and select them as shown below. |
| Pygments | [fmind.py](pygments/fmind.py) | Copy the module into your Python project and pass `FmindStyle` to `HtmlFormatter`, as shown below. Requires Pygments; no changes to installed Pygments files. |
| Rio | [fmind.toml](rio/fmind.toml) | Copy to `rio/themes/fmind.toml`; set `theme = "fmind"` in `rio/config.toml`. On macOS use `~/Library/Application Support/rio/`. |
| Rofi | [fmind.rasi](rofi/fmind.rasi) | Copy to `rofi/fmind.rasi`; use `rofi -show drun -theme ~/.config/rofi/fmind.rasi`. Colors inherit the standard layout. |
| Starship | [fmind.toml](starship/fmind.toml) | Merge the palette and `palette = "fmind"` into `starship.toml`. Module styles select palette names. |
| Streamlit | [fmind.toml](streamlit/fmind.toml) | Merge `[theme]` into your project’s `.streamlit/config.toml`. Uses current Streamlit theming, including chart colors. |
| Sublime Text | [fmind.sublime-color-scheme](sublime-text/fmind.sublime-color-scheme) | Use Preferences → Browse Packages; copy into `User/`, then choose `fmind` with Select Color Scheme. This styles editor content; the UI theme is separate. |
| Terminal.app | [fmind.terminal](terminal-app/fmind.terminal) | On macOS, Settings → Profiles → action menu → Import; select the file and choose Fmind. Set the profile as Default for new windows if desired. Font choice remains in the profile settings. |
| Terminator | [fmind.conf](terminator/fmind.conf) | Merge the `[[fmind]]` profile under `[profiles]` in `terminator/config`; select that profile in Preferences. |
| Termux | [colors.properties](termux/colors.properties) | Copy to `~/.termux/colors.properties`; run `termux-reload-settings`. |
| Tilix | [fmind.json](tilix/fmind.json) | Copy to `tilix/schemes/fmind.json`; restart Tilix and choose Fmind in the profile’s Color settings. |
| tmux | [fmind.conf](tmux/fmind.conf) | Copy to `tmux/fmind.conf`; add `source-file ~/.config/tmux/fmind.conf` to your tmux config. Reload the config to apply. |
| Typora | [fmind.css](typora/fmind.css) | Preferences → Appearance → Open Theme Folder; copy the CSS, restart Typora, and select Fmind. |
| Vim | [fmind.vim](vim/fmind.vim) | Copy to `~/.vim/colors/fmind.vim`; use `set termguicolors` and `colorscheme fmind` in `.vimrc`. Also works in GUI Vim. |
| VS Code | [theme](vscode/fmind-color-theme.json), [manifest](vscode/package.json) | Copy the whole `vscode/` folder to `~/.vscode/extensions/fmind-theme-1.0.0/`, reload VS Code, then select `fmind` in Preferences: Color Theme. |
| Warp | [fmind.yaml](warp/fmind.yaml) | Copy to `~/.warp/themes/` on macOS, `~/.local/share/warp-terminal/themes/` on Linux (`$XDG_DATA_HOME` if set), or `%APPDATA%\warp\Warp\data\themes\` on Windows. Restart if needed and select Fmind in Appearance → Themes. |
| Waybar | [fmind.css](waybar/fmind.css) | Copy to `waybar/fmind.css`; import with `@import "fmind.css";` in `waybar/style.css` before your layout rules. |
| WezTerm | [fmind.toml](wezterm/fmind.toml) | Copy to `wezterm/colors/fmind.toml`; set `config.color_scheme = "fmind"` in `wezterm.lua`. |
| Windows Terminal | [fmind.json](windows-terminal/fmind.json) | Append this object to the `schemes` array in Settings → Open JSON file; set `"colorScheme": "fmind"` on the desired profile. |
| Xcode | [fmind.xccolortheme](xcode/fmind.xccolortheme) | Copy to `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`; restart Xcode, then Settings → Themes → Fmind. Install Google Sans and Google Sans Code for the specified fonts. Covers editor, console and documentation markup; use a light macOS appearance for the remaining UI. |
| Xfce4 Terminal | [fmind.theme](xfce4-terminal/fmind.theme) | Copy to `~/.local/share/xfce4/terminal/colorschemes/fmind.theme`; choose Fmind under Preferences → Colors → Presets. |
| Xresources | [fmind.Xresources](xresources/fmind.Xresources) | Include from `~/.Xresources`, then run `xrdb -merge ~/.Xresources`. Wildcard terminal colors apply to Xresource-aware apps; this is not a GTK theme. |
| Yazi | [fmind.toml](yazi/fmind.toml) | Merge into `yazi/theme.toml`; install the bat theme at the configured `mgr.syntect_theme` path. |
| Zathura | [fmind.conf](zathura/fmind.conf) | Copy to `zathura/fmind.conf`; add `include fmind.conf` to `zathura/zathurarc`. UI colors only; document recoloring is opt-in. |
| Zed | [fmind.json](zed/fmind.json) | Copy to `zed/themes/fmind.json`; choose `fmind` with `theme selector: toggle`. |
| Zellij | [fmind.kdl](zellij/fmind.kdl) | Copy to `zellij/themes/fmind.kdl`; set `theme "fmind"`. Uses named styles (0.41+). |
| zsh-syntax-highlighting | [fmind.zsh](zsh-syntax-highlighting/fmind.zsh) | Source after the plugin in `.zshrc`. Use a truecolor terminal and the matching terminal palette. Does not replace your prompt. |

For GNOME Terminal, create or select a profile in Preferences and copy its UUID from the profile’s settings. Import only into that profile, replacing `<profile-uuid>` and the file path below:

```sh
dconf load /org/gnome/terminal/legacy/profiles:/:<profile-uuid>/ < /path/to/gnome-terminal/fmind.dconf
```

For ptpython, put `fmind.py` beside `config.py` and add this to `configure(repl)`:

```python
from pathlib import Path
from runpy import run_path

from prompt_toolkit.styles import Style

styles = run_path(str(Path(__file__).with_name("fmind.py")))
repl.install_code_colorscheme("fmind", Style.from_dict(styles["CODE"]))
repl.install_ui_colorscheme("fmind", Style.from_dict(styles["UI"]))
repl.use_code_colorscheme("fmind")
repl.use_ui_colorscheme("fmind")
```

For Pygments, with `fmind.py` beside your script:

```python
from pathlib import Path

from fmind import FmindStyle
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

source = Path("example.py").read_text()
html = highlight(source, PythonLexer(), HtmlFormatter(style=FmindStyle, full=True))
Path("example.html").write_text(html)
```

Use one of the matching terminal themes for ANSI colors. Normal and bright slots use dark foregrounds, including slots named white, except ConEmu’s reserved bright-white canvas slot.

Apps with their own colors or ANSI backgrounds may need additional settings. Keep opacity at 100% for the documented contrast. The terminal palettes cover 16 ANSI slots; applications can still request their own 256-color or truecolor values.

Coverage prioritizes terminals, editors and everyday terminal tools, informed by the [free Dracula app catalog](https://draculatheme.com/). See [coverage and remaining gaps](COVERAGE.md) and the [complete catalog checklist](CATALOG.md); this is not full catalog parity. Ports use Fmind’s palette and each app’s native format. Format references are linked at the top of comment-capable files; see also the [VS Code theme guide](https://code.visualstudio.com/api/extension-guides/color-theme), [Windows Terminal scheme reference](https://learn.microsoft.com/en-us/windows/terminal/customize-settings/color-schemes), and the schema in the Zed file.

## Maintenance

Install [mise](https://mise.jdx.dev/) and a C compiler, then run:

```sh
mise trust
mise install
mise run install
mise run check
```

Tools are configured in `mise.toml`; Python dependencies and Ruff in `pyproject.toml`. Lockfiles record resolved versions. Use `mise run format` for Python formatting.

Setup downloads pinned parsers to `.cache/syntax/`. Checks cover file syntax, highlighting, palette consistency, terminal slot parity and contrast. New ports have offline document, color-role and contrast checks; these do not prove that every app or GUI state has been exercised. CI uses the same commands with isolated app configuration. Live services and untested app states remain outside the checks.

Edit native themes directly; update the expectations in `checks/`, palette table and SVG together. To diagnose highlighting, use Neovim's `:Inspect` or `:InspectTree`. Known limits: bat leaves YAML fences plain and omits strikethrough; Tree-sitter treats quoted TOML keys as strings.

Refresh the two PNGs with `mise run screenshots`. This requires setup above, VHS, ttyd, FFmpeg, Zellij, Fontconfig, the recommended font and Chromium. Set `VHS_CHROME_PATH`, or use Playwright Chromium from its default cache.

Maintained alongside [fmind/dot](https://github.com/fmind/dot). [MIT license](LICENSE).
