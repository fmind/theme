---
name: theme-release
description: Validate and publish a Fmind theme release, including shared validation and immutable version tags.
---

# Theme release

1. Read `README.md`, `AGENTS.md` and `CHANGELOG.md`. Review the release diff and state only verified behavior in release notes.
1. Inspect Git status and the intended version locally and remotely. Never reuse a published version or tag.
1. Run `mise install`, `mise run install` and `mise run all`. The gate checks shared files, generated token files, documentation links and artwork, not native app behavior. Verify changed themes manually in their applications. If unrelated global mise tools prevent setup, use `MISE_IGNORED_CONFIG_PATHS` with the actual global configuration path, without editing the workstation configuration.
1. Review README links and previews on GitHub. Refresh the two terminal screenshots only when theme visuals change.
1. With publication authorized, bump the version in every file listed by `git grep -l -F <previous> -- pyproject.toml uv.lock themes` and review each match, since a native format version can coincide. `test_release_versions_are_consistent` in `checks/test_repository.py` enforces the package, extension and browser-theme manifest versions, and `uv run --locked` enforces `uv.lock`. Rename `## Unreleased` in CHANGELOG.md to `## X.Y.Z — YYYY-MM-DD`, commit the candidate as `chore(release): X.Y.Z` and push `main`. Verify its CI before tagging that exact commit.
1. Create the annotated tag `vX.Y.Z` and publish a GitHub release with the verified scope and outstanding native acceptance gaps. Automatic source archives are the release payload; no Python package or extension marketplace publication is implied.
1. Verify the remote peeled tag and public release state. Remove only task-owned temporary outputs.
1. Report which consumers the release affects, without editing them: fmind/dot pins theme files and `DESIGN.md` by commit (`mise run upgrade` there advances the pin), fmind/pub records the theme revision in `BRANDING.md`, and fmind/www snapshots the palette in `tests/test_palette.py`.
