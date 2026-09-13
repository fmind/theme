# Validation

Install [mise](https://mise.jdx.dev/) and a C compiler, then run from the repository:

```sh
mise trust
mise install
mise run install
mise run check
```

`mise run install` syncs Python dependencies from `uv.lock` and prepares pinned Neovim parsers under `.cache/syntax/`; it needs network access. `mise run check` validates file syntax, rendered Neovim and bat styles, palette membership and text contrast. It includes all 15 regression tests without formatting source. CI runs the same commands; `mise run format` formats Python explicitly.

The four `.gitignore` entries cover generated files: `.cache/` for parsers, `.ruff_cache/` for lint results, `.venv/` for Python dependencies and `__pycache__/` for Python bytecode. App configurations and caches stay isolated from installed themes and live services.

Edit native app files directly. `palette.yaml` and `syntax.yaml` hold regression expectations; no application reads them. When changing colors, update the native files, expectations, README and palette SVG together. Foreground text must meet 4.5:1 on white, panels, selections and diff surfaces. Bright accents belong on fills, markers and decoration. Diff words must remain distinct from their lines.

The synthetic corpus in `samples/` covers Python, YAML, Markdown, JSON, TOML, shell, HTML, CSS and Lua. Standard Tree-sitter captures and LSP token types inherit theme roles. A theme cannot supply missing parsers or identify syntax a grammar does not expose.

Known boundaries in the pinned runtime:

- bat highlights Python fences in Markdown but leaves the sample YAML fence plain. Neovim highlights both.
- Tree-sitter classifies quoted TOML keys as strings. Bare keys are blue and bold; quoted keys stay green. Legacy Neovim and bat distinguish them.
- bat has no strikethrough attribute. Deleted Markdown retains its markers and gray text; Neovim draws the strike.

Use `:Inspect`, `:set filetype?` and `:InspectTree` in Neovim when diagnosing a token. The gate exercises Neovim, bat, Fish and prompt-toolkit; parsing other app files does not prove every runtime state. Live clusters, Docker services and authenticated dashboards are outside these checks.

## Screenshots

`mise run screenshots` refreshes exactly two PNGs from synthetic inputs: code/shell with search and selection, and Markdown. The palette SVG is a small hand-maintained reference. Capture requires `mise run install`, VHS, ttyd, FFmpeg, Zellij, Fontconfig, GoogleSansCode Nerd Font Mono, and Chromium. Set `VHS_CHROME_PATH` to Chromium, or install Playwright Chromium in its default cache. Capture uses a temporary home and its own Zellij session.

## Updates

Tools use `latest` in `mise.toml`, except Python 3.13, also recorded in `.python-version` and constrained in `pyproject.toml`. `mise.lock` records the tested tool versions. Review updates with `mise outdated python uv neovim bat tree-sitter ruff fish` and rerun the gate after upgrading. Python dependencies and Ruff settings live in `pyproject.toml`; `uv.lock` records resolved dependencies. The Tree-sitter runtime stays pinned in `setup.py` so grammar changes are reviewed deliberately. Refresh screenshots after visual changes.
