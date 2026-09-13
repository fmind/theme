# AGENTS.md

Fmind is a light theme. See [README.md](README.md) for installation and [checks/README.md](checks/README.md) for validation.

- Edit native theme files directly. Keep palette expectations, README and palette SVG aligned.
- Keep text contrast at least 4.5:1 on backgrounds, selections, diffs and filled labels.
- Run `mise install`, `mise run install`, then `mise run check`. Use `mise run format` for Python edits.
- Keep two synthetic screenshots; refresh with `mise run screenshots` after visual changes.
- Isolate app configuration. Never modify installed themes or contact live services during checks.
