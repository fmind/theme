# AGENTS.md

Fmind is the design system and light theme behind Médéric Hurier's (Fmind) tools and publications. The repository holds four things: DESIGN.md, the design system in the [DESIGN.md format](https://github.com/google-labs-code/design.md); native theme files under `themes/`; ready-made files for renderers (CSS, Tailwind, D2, Mermaid, VHS); and brand artwork. README.md owns usage and is displayed directly on GitHub; CHANGELOG.md records user-visible changes. Keep only these four root Markdown files.

Three repositories consume it: [fmind/dot](https://github.com/fmind/dot) pins theme files and DESIGN.md by commit and checksum, fmind/pub copies the artwork and follows DESIGN.md, and fmind/www snapshots the palette. Never edit them from here; report what a change means for them.

## Guidelines

- **Keep the palette fixed**: the 15 Google News colors plus five custom shades are the owner's choice. Do not add, remove or change a color without an explicit request. `checks/palette.yaml`, DESIGN.md, README, `screenshots/palette.svg` and fmind/www `tests/test_palette.py` (`FMIND_COLORS`) list the same colors. Text needs 4.5:1 contrast; essential controls need 3:1 and non-color state cues.
- **Change the design in DESIGN.md only**: roles, typography, layout, components and the chart series order live there; lint it with `mise run check:design`. `themes/css/fmind.css` and `themes/tailwind/fmind.css` are generated from it: run `mise run tokens` and never edit them by hand. Bump design.md in `mise.toml` and run `mise lock npm:@google/design.md` to refresh `.mise/locks/`; tests require README `npx` commands to match.
- **Edit native files directly**: each `themes/<app>/` directory holds native files and a README that owns installation and cites, on a `Format:` line, the upstream format or loader its files follow; remove a port that no longer follows one. Never add dependencies, lockfiles or build steps to a port. Follow the [theme-port](.agents/skills/theme-port/SKILL.md) skill to add, fix or remove a port, and keep README concise.
- **Keep the catalog focused**: keep or add a port only when fmind/dot deploys it, a Fmind project renders with it (sites, documentation, diagrams, charts, recordings), or it is a leading developer, data or AI tool on Linux or macOS that the owner could adopt. Decline or remove consumer, chat, media and game apps, desktop environments and window managers, website userstyles, Windows-only apps, variants of existing ports and discontinued apps.
- **Treat removals and renames as breaking**: raw download URLs and fmind/dot, which pins and executes several theme files, depend on theme paths. Record a removal or rename under Breaking in CHANGELOG.md and release a major version.
- **Regenerate visuals from their sources**: edit branding in `artworks/generate.py`, run `mise run artwork`, and preserve bundled source assets and their licenses. After changing the nvim, fish, bat, zellij, ghostty or vhs themes, refresh the two synthetic terminal captures with `mise run screenshots`. Capture uses Neovim's built-in syntax highlighting, and the captures do not prove GUI coverage.
- **Keep checks generic**: `checks/` covers shared repository invariants, not native app behavior. Do not add app-specific harnesses or parser downloads. Checks isolate app configuration and never modify installed themes or contact live app services; verify affected themes in their apps and report what the app loaded.
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

- **Hooks delegate to mise tasks**: `mise run install` activates Lefthook. Pre-commit formats staged files in scope and runs the offline `mise run check:local`; pre-push runs `mise run check:network` and `mise run test`.
- **Formatting scope is explicit**: dprint formats only the paths in `dprint.json`, and Ruff formats only Python. Native files under `themes/`, screenshot fixtures, generated artwork and lockfiles stay unformatted. Preserve one-line Markdown paragraphs.
- **Network checks are separate evidence**: `check:vuln` (in `check:network`) needs network access and fails on reported vulnerabilities or registry errors, so it runs on pre-push and in CI, not on commit. `mise run test` checks local links and anchors, not external URLs.
- **Dependabot opens security fixes only**: it groups fixes for root uv and GitHub Actions; version updates stay off. Update artwork script locks, mise pins (including the workflow's mise version) and dprint plugins manually.
- **Capture screenshots on Linux**: mise locks ttyd for Linux only, and the Chromium fallback searches only the Linux Playwright cache. Elsewhere, put ttyd on `PATH` and set `VHS_CHROME_PATH` (untested).
- **Search lockfiles with Git**: `.ignore` hides lockfiles and generated SVGs from ripgrep and agent search tools; use `git grep` for them.
