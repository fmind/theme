# AGENTS.md

Fmind light theme and design system: [DESIGN.md](DESIGN.md) ([DESIGN.md format](https://github.com/google-labs-code/design.md)), native ports under `themes/` and brand artwork. Keep only four root Markdown files: `AGENTS.md`, `CHANGELOG.md`, `DESIGN.md` and [README.md](README.md) (usage and catalog).

## Guidelines

- **Keep the palette fixed**: never add, remove or change any of the [15 Google News colors](https://partnermarketinghub.withgoogle.com/brands/google-news/visual-identity/color-palette/) or five custom shades without an explicit request. `DESIGN.md` owns the 20 canonical hex colors; keep `DESIGN.md`, `checks/palette.yaml` (syntax/ANSI contrast roles), `README.md`, `screenshots/palette.svg` and `fmind/www` `tests/test_palette.py` (`FMIND_COLORS`) in sync. Text needs 4.5:1 contrast; essential controls need 3:1 plus non-color cues.
- **Change the design in `DESIGN.md` only**: roles, typography, layout, components and chart series order live there (`mise run check:design`). Regenerate `themes/css/fmind.css` and `themes/tailwind/fmind.css` via `mise run tokens` (never hand-edit); if bumping `npm:@google/design.md` in `mise.toml`, run `mise lock npm:@google/design.md` and match `@google/design.md@<version>` references across Markdown docs (enforced by `mise run test`).
- **Ship native port files only**: follow [theme-port](.agents/skills/theme-port/SKILL.md) to add, fix, rename or remove `themes/<app>/` ports. Never add dependencies, lockfiles or build steps; remove any port whose `README.md` can no longer cite an upstream format or loader on `Format:`.
- **Keep the catalog focused**: keep or add a port only when `fmind/dot` deploys it, a Fmind project renders with it, or it is a leading Linux/macOS developer, data or AI tool.
- **Treat path removals and renames as breaking**: raw URLs and `fmind/dot` checksum pins depend on `themes/` paths; record changes under `Breaking` in `CHANGELOG.md` for a major release.
- **Regenerate visuals from source**: edit branding in `artworks/generate.py` and run `mise -C artworks install && mise run artwork`, preserving bundled assets and `artworks/OFL.txt`. After `nvim`, `fish`, `bat`, `zellij` or `vhs` theme edits, run `mise -C screenshots install && mise run screenshots` on Linux (uses Neovim built-in `:syntax`, not Treesitter or GUIs). Local media/screenshot tools live in `artworks/mise.toml` and `screenshots/mise.toml` so CI installs only validation tools.
- **Keep `checks/` generic and offline**: test shared repo invariants only, without app harnesses, parser downloads, host-config writes or live services. Verify changed ports in the isolated real app and report what loaded vs only parsed.

## Maintenance

Setup: `mise install && mise run install` (`mise tasks` lists all tasks). Iterate offline with `mise run format`, `mise run check:local` and `mise run test` (local links/anchors only); run `mise run all` (adds networked `check:vuln`, matching CI) to gate changes, and follow [theme-release](.agents/skills/theme-release/SKILL.md) for releases. Weekly `.github/workflows/security.yml` runs full-history `check:leaks:full`, `check:network` and `check:actions:online`.

- **Formatting and hooks**: Lefthook runs `format` + `check:local` on commit and `check:network` + `test` on push. Only `dprint.json` paths (one-line Markdown paragraphs) and non-excluded Python (`checks/`, `artworks/generate.py`, `screenshots/capture.py`) are formatted; never format native `themes/`, `screenshots/samples/`, generated artwork or lockfiles.
- **Upgrade pins manually**: Dependabot opens security fixes only (`uv` and GitHub Actions); update GitHub Actions, `mise.toml` (`artworks/mise.toml`, `screenshots/mise.toml` and `ci.yml`/`security.yml` `mise` versions), `dprint.json` plugins, `uv.lock` and `artworks/generate.py.lock` manually.
- **Search hidden files with Git**: `.ignore` hides `*.lock`, `.mise/locks/` and generated SVGs from `rg` and agent search; use `git grep`.
