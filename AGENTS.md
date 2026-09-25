# AGENTS.md

Fmind is a light theme. README.md owns usage and is displayed directly on GitHub; CHANGELOG.md records user-visible changes. Keep only these three root Markdown files.

## Guidelines

- Maintain native files directly under `themes/`; list every integration alphabetically in README, linking to its directory. Each directory owns installation in its README; do not introduce priority tiers. Experimental files do not establish native support.
- Keep palette expectations in `checks/palette.yaml`, README and `screenshots/palette.svg` aligned. Text needs 4.5:1 contrast; essential controls need 3:1 and non-color state cues.
- Refresh the two synthetic terminal captures with `mise run screenshots` after theme visual changes. They do not prove GUI coverage.
- Edit branding through `artworks/generate.py` and regenerate with `mise run artwork`; preserve bundled source assets and their licenses.
- Isolate app configuration. Never modify installed themes or contact live app services during checks.
- Keep validation in `checks/`, branding sources and generation in `artworks/`.
- Keep README concise and verify documentation links and image paths after changes.
- For authorized publication, follow [theme-release](.agents/skills/theme-release/SKILL.md). Local checks, hosted CI and releases are separate evidence.

## Maintenance

Install [mise](https://mise.jdx.dev/):

```sh
mise trust
mise install
mise run install
mise run all
```

| Task                   | Purpose                                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| `mise run format`      | Format Python with Ruff and repository documentation/configuration with dprint.                                |
| `mise run check`       | Lint Python and workflows, validate hooks, check formatting and audit locked dependencies.                     |
| `mise run test`        | Check shared palette, JSON/TOML/YAML syntax, documentation and artwork.                                        |
| `mise run screenshots` | Refresh the two terminal captures. Uses pinned FFmpeg; requires Fontconfig, Chromium and the recommended font. |
| `mise run artwork`     | Regenerate artwork from `artworks/generate.py` and bundled assets.                                             |

`mise run check:security` queries OSV and npm for known vulnerabilities in the root Python lock, artwork script lock and JupyterLab npm lock, including development dependencies. It requires network access, installs no npm packages and fails on reported vulnerabilities or registry errors. Update artwork script locks, mise pins and dprint plugins manually; Dependabot covers root uv, GitHub Actions and JupyterLab npm dependencies.

Checks cover shared repository invariants, not native app behavior; verify affected themes manually in their apps. Do not add app-specific test harnesses or parser downloads. Screenshot capture uses built-in Neovim syntax highlighting and accepts `VHS_CHROME_PATH` or cached Playwright Chromium.

`mise run install` activates Lefthook: pre-commit formats staged files in scope and runs `mise run check`; pre-push runs `mise run test`. Keep hook commands delegated to mise tasks. dprint uses the explicit scope in `dprint.json`; native files under `themes/`, screenshot fixtures, generated artwork and lockfiles are outside that scope. Preserve one-line Markdown paragraphs.

GitHub Actions runs the read-only `mise run all` gate. Dependencies and tools are pinned in lockfiles and `mise.toml`; Dependabot proposes dependency updates for review.
