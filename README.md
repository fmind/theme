# fmind/theme

A light theme for everyday terminal work. One folder per app, native theme files, no generator.

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

Use the matching Ghostty theme for ANSI colors. Normal and bright slots use dark foregrounds, including slots named white.

Apps with their own colors or ANSI backgrounds may need additional settings.

## Maintenance

Install [mise](https://mise.jdx.dev/) and a C compiler, then run:

```sh
mise trust
mise install
mise run install
mise run check
```

Tools are configured in `mise.toml`; Python dependencies and Ruff in `pyproject.toml`. Lockfiles record resolved versions. Use `mise run format` for Python formatting.

Setup downloads pinned parsers to `.cache/syntax/`. Checks cover file syntax, highlighting, palette consistency and contrast. CI uses the same commands with isolated app configuration. Live services and untested app states remain outside the checks.

Edit native themes directly; update the expectations in `checks/`, palette table and SVG together. To diagnose highlighting, use Neovim's `:Inspect` or `:InspectTree`. Known limits: bat leaves YAML fences plain and omits strikethrough; Tree-sitter treats quoted TOML keys as strings.

Refresh the two PNGs with `mise run screenshots`. This requires setup above, VHS, ttyd, FFmpeg, Zellij, Fontconfig, the recommended font and Chromium. Set `VHS_CHROME_PATH`, or use Playwright Chromium from its default cache.

Maintained alongside [fmind/dot](https://github.com/fmind/dot). [MIT license](LICENSE).
