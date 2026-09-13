# fmind/theme

A light theme for everyday terminal work. One folder per app, native theme files, no generator.

## Palette

![Fmind colors and their roles](screenshots/palette.svg)

The complete palette contains 20 colors, including the supporting custom shades. Every color is listed below, whether it colors syntax, interface elements or backgrounds.

All currently appear in at least one integration; a dash means no assigned role in that column. Colors without any use should remain listed as **Unused**.

| Color | Hex | Syntax and text | Interface and backgrounds |
| --- | --- | --- | --- |
| White | `#FFFFFF` | Label text on dark fills | Main background |
| Light gray | `#F1F3F4` | — | Panels, cursor line, menus and neutral diff lines |
| Gray | `#9AA0A6` | bat gutter numbers | Borders, scrollbar accents and deprecated-code marks |
| Dark gray (custom) | `#595D62` | Comments, line numbers and secondary text | Inactive labels and muted indicators; ANSI bright black |
| Charcoal | `#202124` | Body text, variables, parameters, properties, operators and punctuation | Label text on bright fills; ANSI black and white slots |
| Dark blue | `#174EA6` | Keywords, functions, calls, escapes, configuration keys, inline code and primary headings | Navigation, links, focus indicators and staged-change signs; ANSI blue |
| Medium blue | `#4285F4` | — | Cursor, incremental search, blue labels, tabs and marked-file indicators |
| Light blue | `#D2E3FC` | — | Selections, selected rows and completion items |
| Dark red | `#A50E0E` | Errors, exceptions and deleted text | Failure indicators, deletion signs and error-badge fills; ANSI red |
| Medium red | `#EA4335` | — | Cut-file markers, spelling-error and diagnostic-error underlines |
| Light red | `#FAD2CF` | — | Deleted-line and deleted-word backgrounds |
| Dark orange (custom) | `#934900` | Numbers, constants, booleans and warning text | Modified-change signs and attention indicators; ANSI yellow |
| Orange | `#E37400` | — | Search and warning-label fills, selected-file markers and warning underlines |
| Yellow | `#FBBC04` | — | Active tabs, current search match, changed words and focused controls |
| Light yellow | `#FEEFC3` | — | Changed-line and marked-base-commit backgrounds |
| Dark green | `#0D652D` | Strings, characters, added text and secondary headings | Success indicators, addition signs and executable files; ANSI green |
| Medium green | `#34A853` | — | Insert/select-mode labels, copied-file markers and success underlines |
| Light green | `#CEEAD6` | — | Added-line, added-word and cherry-picked-commit backgrounds |
| Purple (custom) | `#681DA8` | Types, classes, builtins, decorators, attributes and emphasis | Secondary accents and type-related labels; ANSI magenta |
| Teal (custom) | `#00636D` | Informational diagnostics | Informational messages and cyan icons; ANSI cyan |

Dark shades carry text; bright shades carry fills and accents. Syntax and comments meet 4.5:1 on white, panels, selections and diff backgrounds. Filled labels use charcoal or white text according to their background. Staged Git signs keep the change’s color and add bold. Color is reinforced by labels, signs and typography.

Font recommendation: **GoogleSansCode Nerd Font Mono**. Font installation and selection belong to the terminal configuration. Text stays upright; bold marks structural emphasis.

## Screenshots

| Code, shell, search and selection | Markdown |
| --- | --- |
| ![Neovim and Fish in Zellij, including search and selected code](screenshots/zellij.png) | ![Markdown syntax in Neovim](screenshots/markdown.png) |

Two real application captures, using synthetic examples and VHS. [Validation and capture instructions](checks/README.md).

## Install

Use a truecolor terminal with a light background. Paths below use `~/.config`; respect each app’s configured directory or `XDG_CONFIG_HOME`. Merge fragments into existing configuration instead of replacing unrelated settings.

| Tool | Theme file | Installation |
| --- | --- | --- |
| Atuin | [fmind.toml](atuin/fmind.toml) | Copy to `atuin/themes/fmind.toml`; set `[theme] name = "fmind"` in `atuin/config.toml`. |
| bat | [fmind.tmTheme](bat/fmind.tmTheme) | Copy to the `themes/` directory under `bat --config-dir`; run `bat cache --build`, then select `--theme=fmind`. |
| bottom | [fmind.toml](bottom/fmind.toml) | Merge `[styles]` and its sections into `bottom/bottom.toml`. |
| delta | [fmind.gitconfig](delta/fmind.gitconfig) | Include from Git configuration; install the bat theme first. |
| Fastfetch | [fmind.json](fastfetch/fmind.json) | Merge `display.color` into `fastfetch/config.jsonc`. |
| Fish | [fmind.fish](fish/fmind.fish) | Copy to `fish/conf.d/fmind.fish`. |
| fzf | [fmind.conf](fzf/fmind.conf) | Set `FZF_DEFAULT_OPTS_FILE` to this file’s absolute path. |
| gh-dash | [fmind.yml](gh-dash/fmind.yml) | Merge `theme` into `gh-dash/config.yml`. |
| Ghostty | [fmind](ghostty/fmind) | Copy to `ghostty/themes/fmind`; set `theme = fmind`. |
| k9s | [fmind.yaml](k9s/fmind.yaml) | Copy to the skins directory shown by `k9s info`; select `k9s.ui.skin: fmind` in its config. |
| Lazydocker | [fmind.yml](lazydocker/fmind.yml) | Merge `gui.theme` into Lazydocker’s `config.yml`. |
| LazyGit | [fmind.yml](lazygit/fmind.yml) | Merge `gui.theme` into the config directory shown by `lazygit --print-config-dir`. |
| lsd | [fmind.yaml](lsd/fmind.yaml) | Copy to `lsd/colors.yaml`; set `color.theme: custom` in `lsd/config.yaml`. |
| lualine | [fmind.lua](lualine/fmind.lua) | Copy to `nvim/lua/lualine/themes/fmind.lua`; select `fmind` or `auto`. |
| Neovim | [fmind.lua](nvim/colors/fmind.lua) | Copy to `nvim/colors/fmind.lua`; use `colorscheme fmind`. |
| OpenCode | [fmind.json](opencode/fmind.json) | Copy to `opencode/themes/fmind.json`; select `fmind` through `/theme`. |
| ptpython | [fmind.py](ptpython/fmind.py) | Load `CODE` and `UI` in `config.py`; register and select them as shown below. |
| Starship | [fmind.toml](starship/fmind.toml) | Merge the palette and `palette = "fmind"` into `starship.toml`. Module styles select palette names. |
| Yazi | [fmind.toml](yazi/fmind.toml) | Merge into `yazi/theme.toml`; install the bat theme at the configured `mgr.syntect_theme` path. |
| Zellij | [fmind.kdl](zellij/fmind.kdl) | Copy to `zellij/themes/fmind.kdl`; set `theme "fmind"`. Uses named styles (0.41+). |

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

Named ANSI colors follow the terminal palette; use the matching Ghostty theme. Both normal and bright slots use readable dark foregrounds, including the slots named white. Apps that use ANSI colors as backgrounds or define their own colors may need app-specific settings; a terminal palette cannot control every rendered color.

Maintained alongside [fmind/dot](https://github.com/fmind/dot). [MIT license](LICENSE).
