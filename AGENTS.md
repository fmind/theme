# AGENTS.md

Fmind is a light theme and design system. README.md owns usage and is displayed directly on GitHub; DESIGN.md owns the design system in the [DESIGN.md format](https://github.com/google-labs-code/design.md); CHANGELOG.md records user-visible changes. Keep only these four root Markdown files.

## Guidelines

- **Edit native files directly**: each `themes/<app>/` directory holds native files and a README that owns installation. List every integration alphabetically in README, linking to its directory, without priority tiers. Experimental files do not establish native support. Follow README [Contribute](README.md#contribute) for ports, and keep README concise.
- **Treat removals and renames as breaking**: raw download URLs and [fmind/dot](https://github.com/fmind/dot), which pins and executes several theme files, depend on theme paths. Record a removal or rename under Breaking in CHANGELOG.md and release a major version.
- **Keep the palette aligned**: `checks/palette.yaml`, DESIGN.md, README, `screenshots/palette.svg` and fmind/www `tests/test_palette.py` (`FMIND_COLORS`) list the same colors. Text needs 4.5:1 contrast; essential controls need 3:1 and non-color state cues. Design roles, typography, layout and components change in DESIGN.md only; lint it with `npx @google/design.md@0.4.0 lint DESIGN.md`.
- **Regenerate visuals from their sources**: edit branding in `artworks/generate.py`, run `mise run artwork`, and preserve bundled source assets and their licenses. After changing the nvim, fish, bat, zellij or ghostty themes, refresh the two synthetic terminal captures with `mise run screenshots`. Capture uses Neovim's built-in syntax highlighting, and the captures do not prove GUI coverage.
- **Keep checks generic**: `checks/` covers shared repository invariants, not native app behavior. Do not add app-specific harnesses or parser downloads. Checks isolate app configuration and never modify installed themes or contact live app services; verify affected themes manually in their apps.
- **Release only when authorized**: follow [theme-release](.agents/skills/theme-release/SKILL.md). Local checks, hosted CI and releases are separate evidence.

## Maintenance

Install [mise](https://mise.jdx.dev/), then set up and validate:

```sh
mise trust
mise install
mise run install
mise run all
```

`mise tasks` lists every task and its purpose. `mise run all` is the read-only gate that GitHub Actions runs on pushes to `main`, pull requests and weekly.

- **Hooks delegate to mise tasks**: `mise run install` activates Lefthook. Pre-commit formats staged files in scope and runs `mise run check`; pre-push runs `mise run test`.
- **Formatting scope is explicit**: dprint formats only the paths in `dprint.json`, and Ruff formats only Python. Native files under `themes/`, screenshot fixtures, generated artwork and lockfiles stay unformatted. Preserve one-line Markdown paragraphs.
- **Network checks are separate evidence**: `check:security` needs network access and fails on reported vulnerabilities or registry errors. `mise run test` checks local links and anchors, not external URLs.
- **Dependabot opens security fixes only**: it groups fixes for root uv, GitHub Actions and JupyterLab npm; version updates stay off. Update artwork script locks, mise pins (including the workflow's mise version) and dprint plugins manually.
- **Capture screenshots on Linux**: mise locks ttyd for Linux only, and the Chromium fallback searches only the Linux Playwright cache. Elsewhere, put ttyd on `PATH` and set `VHS_CHROME_PATH` (untested).
- **Search lockfiles with Git**: `.ignore` hides lockfiles and generated SVGs from ripgrep and agent search tools; use `git grep` for them.
