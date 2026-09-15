# AGENTS.md

Fmind is a light theme. [README.md](README.md) owns usage and the GitHub Pages content.

- Follow [CATALOG.md](CATALOG.md) and [TODO.md](TODO.md); preserve all 20 core consumers. Directory parity does not mean functional parity. Read [REVIEW.md](REVIEW.md) before making support claims.
- Edit native theme files directly. Keep palette expectations, README and palette SVG aligned; use colors only where they have a meaningful role.
- Text contrast must reach 4.5:1 on backgrounds, selections, diffs and filled labels. Essential controls need 3:1; retain non-color state cues.
- Run `mise install`, `mise run install`, then `mise run all`. Use `mise run format` for Python edits.
- Keep two synthetic terminal screenshots; refresh with `mise run screenshots` after theme visual changes. They do not prove GUI coverage.
- Isolate app configuration. Never modify installed themes or contact live app services during checks.
- For publication, use [theme-release](.agents/skills/theme-release/SKILL.md). Native acceptance and publication are separate evidence.
