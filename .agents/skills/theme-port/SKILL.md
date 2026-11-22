---
name: theme-port
description: "Add, fix, or remove a Fmind theme port under themes/<app>/, map palette roles to the native format, and verify in the real tool."
license: MIT
metadata:
  kind: task
  author: Médéric HURIER (Fmind)
  source: github.com/fmind/theme/tree/main/.agents/skills/theme-port
  created: "2026-11-09"
  updated: "2026-11-22"
---

# Theme Port

Add, fix, rename, or remove native ports under `themes/<app>/` while keeping palette roles, README structure, and isolated tool verification aligned with `AGENTS.md`.

## Workflow

1. **Decide scope**: apply "Keep the catalog focused" in `AGENTS.md`. An app that loads an existing port's file becomes a section of that port's README, not a new folder.
1. **Read the upstream format**: open primary documentation or loader source and check the installed tool version; never write keys from memory. Link the pages read on the README `Format:` line.
1. **Map roles, not colors**: take syntax and ANSI text roles from `checks/palette.yaml` and canonical colors, surfaces, components, and chart series order from `DESIGN.md`. Reference ports: `themes/nvim/colors/fmind.lua` (syntax), `themes/ghostty/fmind` (16 ANSI slots), and `themes/pygments/fmind.py` (token highlighters). Dark shades carry text; bright shades (`#4285F4`, `#EA4335`, `#FBBC04`, `#34A853`, `#E37400`) are fills, cursors, and markers only; `#9AA0A6` never carries text. Keep text upright; bold marks keywords, tags, headings, and named constants (`True`, `None`), while numbers stay regular. When a tool accepts only ANSI names, delegate to the terminal palette (as in `themes/duckdb/`).
1. **Write native files only**: ship zero dependencies, lockfiles, or build steps. `themes/<app>/README.md` starts with `# Fmind for <App>`, includes `Files:` (linking every shipped file), `Format:` (upstream docs URL), and `## Installation` with the full destination path (optionally adding a brief `Tested with <Tool> <version>` line). Add the app alphabetically to its category in `README.md` and log an entry under `## Unreleased` in `CHANGELOG.md`.
1. **Verify in an isolated config**: load the file in the real tool, inspect rendered output (images for diagrams/pages; PTY color checks for terminal tools), and report the tested tool version plus what the tool loaded vs only parsed. Never run `mise` with `HOME` overridden (it reinstalls every tool there): resolve the binary with `mise which <tool>`, then run with `env -i HOME=<scratch>`.
1. **Refresh derived files & gate**: on Linux, run `mise -C screenshots install && mise run screenshots` after edits to any screenshot-trigger theme listed in `AGENTS.md`; run `mise run tokens` after `DESIGN.md` token edits; finish with `mise run format && mise run all`.

## Remove or Rename a Port

1. Delete or move `themes/<app>/`, update its `README.md` category, and record the old path under `Breaking` in `CHANGELOG.md`.
1. Replace links to removed folders in older changelog entries with plain text; find references via `git grep -n "themes/<app>"` (including `screenshots/capture.py`).

## Gotchas

- **`fmind/dot` pins paths by commit and SHA-256**: `.chezmoiexternal.toml.tmpl` and `dot/dot_tasks/theme_pin.py` pin deployed theme files; tell the owner before removing or renaming any pinned path so `fmind/dot` updates together.
- **Keep native files unformatted**: `dprint` and `ruff` intentionally exclude `themes/`; format edits manually to match the upstream tool's style.
