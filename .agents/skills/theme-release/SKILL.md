---
name: theme-release
description: "Validate, tag, and publish a Fmind theme release with shared gates, version sync, and immutable GitHub tags."
license: MIT
metadata:
  kind: task
  author: Médéric HURIER (Fmind)
  source: github.com/fmind/theme/tree/main/.agents/skills/theme-release
  created: "2026-11-09"
  updated: "2026-11-22"
---

# Theme Release

Validate a release candidate, bump synchronized versions, verify exact-head CI, and publish an immutable `vX.Y.Z` GitHub release.

## Workflow

1. **Pre-check state and version**: read `README.md`, `AGENTS.md`, and `CHANGELOG.md`; verify a clean tree and unused version/tag locally and remotely:
   ```sh
   git status --short
   git fetch --tags origin
   git tag -l "vX.Y.Z"
   gh release view "vX.Y.Z" -R fmind/theme # expect not found
   ```
1. **Run full local gates**: run `mise install && mise run install && mise run all`. Verify changed themes manually in their real apps (gates check invariants, tokens, links, and artwork, not native rendering). Refresh terminal screenshots on Linux only when `nvim`, `fish`, `bat`, `zellij`, or `vhs` visuals changed.
1. **Bump versions & prepare candidate** (once publication is authorized): find matching manifests via `git grep -l -F <previous> -- pyproject.toml themes`, review each match (native format versions can coincide), update `pyproject.toml` and matching theme manifests (`themes/chrome/manifest.json`, `themes/vscode/package.json`), and regenerate `uv.lock` with `uv lock` (never hand-edit `uv.lock`). Rename `## Unreleased` in `CHANGELOG.md` to `## X.Y.Z - YYYY-MM-DD`, re-run `mise run all`, commit `chore(release): X.Y.Z`, and push `main`.
1. **Gate exact-head CI before tagging**: wait for CI on the exact pushed SHA (`gh run list -R fmind/theme --limit 3` / `gh run watch <run-id> -R fmind/theme`). Never tag a commit whose CI has not passed.
1. **Tag & publish**: create and push the annotated tag, then publish the GitHub release (automatic source archives are the payload; no PyPI or extension marketplace publish):
   ```sh
   git tag -a "vX.Y.Z" -m "Release vX.Y.Z"
   git push origin "refs/tags/vX.Y.Z"
   gh release create "vX.Y.Z" -R fmind/theme --title "vX.Y.Z" --notes-file <notes.md>
   ```
1. **Verify published state & report consumers**: confirm the peeled remote tag matches `HEAD` (`git ls-remote --tags origin "vX.Y.Z^{}"` and `gh release view "vX.Y.Z" -R fmind/theme`). Report affected consumers without editing them: `fmind/dot` (pins theme files + `DESIGN.md`; `mise run upgrade` advances the pin), `fmind/pub` (`BRANDING.md`), and `fmind/www` (`tests/test_palette.py`).

## Gotchas

- **Immutable releases and tags**: `v*` tags and GitHub releases are immutable once published. If a defect escapes after tagging, never delete or move the tag; ship a forward-fix `vX.Y.(Z+1)` release instead.
- **Unrelated global mise conflicts**: if global mise tools block setup, scope `MISE_IGNORED_CONFIG_PATHS` to the global config path without editing workstation config.
- **State verified behavior only**: separate local/CI checks from native app verification and list remaining acceptance gaps in release notes.
