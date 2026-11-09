---
name: theme-port
description: Add, fix or remove a Fmind theme port under themes/<app>/, map palette roles to the native format, and verify the result in the real tool.
---

# Theme port

1. **Decide the scope.** Apply "Keep the catalog focused" in `AGENTS.md`. An app that loads an existing port's file becomes a section of that port's README, not a new folder.
1. **Read the upstream format.** Open the primary documentation or the loader source, and check the installed version of the tool. Do not write keys from memory. The README `Format:` line links the pages you read.
1. **Map roles, not colors.** Take syntax, ANSI and surface roles from `checks/palette.yaml`, and interface roles, components and the chart series order from `DESIGN.md`. Reference ports: `themes/nvim/colors/fmind.lua` for syntax, `themes/ghostty/fmind` for the 16 ANSI slots, `themes/pygments/fmind.py` for token highlighters. Dark shades carry text. Medium blue, medium red, yellow and the other bright shades are fills, cursors and markers only. Gray `#9AA0A6` never carries text. Text stays upright; bold marks keywords, tags, headings and named constants (`True`, `None`), while numbers stay regular. When a tool accepts only ANSI color names, use them so the terminal theme supplies the palette, as `themes/duckdb/` does.
1. **Write native files only.** No dependencies, lockfiles or build steps. `themes/<app>/README.md` has the title `Fmind for <App>`, a `Files:` line, a `Format:` line, an `## Installation` section with the full destination path, and the tool version you tested. Add the app to its README category in alphabetical order, and an entry under `## Unreleased` in `CHANGELOG.md`.
1. **Verify in the real tool, with an isolated configuration.** Load the file with the tool and inspect what it draws: render diagrams and pages and look at the image; run terminal tools in a pseudo-terminal and confirm that each emitted color is a palette value or an intended ANSI slot. Never run mise with `HOME` overridden, because it reinstalls every tool there: resolve the binary with `mise which <tool>`, then run it with `env -i HOME=<scratch>`. Say in the README and in your report what the tool loaded and what was only parsed.
1. **Refresh derived files.** After a change to the nvim, fish, bat, zellij, ghostty or vhs themes, run `mise run screenshots`. After a change to `DESIGN.md` tokens, run `mise run tokens`.
1. **Run the gate.** `mise run format`, then `mise run all`.

## Remove or rename a port

Delete or move the folder, update its README category, and record the old path under Breaking in `CHANGELOG.md`. Replace links to a removed folder in older changelog entries with plain text; `git grep -n "themes/<app>"` finds them and any use in `screenshots/capture.py`.

fmind/dot pins the theme files it deploys by commit and checksum, in its `.chezmoiexternal.toml.tmpl` and `dot/dot_tasks/theme_pin.py`. Do not remove or rename one of those paths without telling the owner, who updates fmind/dot in the same effort.
