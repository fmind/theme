---
name: theme-release
description: Validate and publish a Fmind theme release, including catalog evidence, immutable version tags and the README Pages site.
---

# Theme release

1. Read `README.md`, `REVIEW.md`, `VALIDATION.md` and `TODO.md`. Describe directory coverage separately from native acceptance, including known incomplete drafts in release notes.
1. Inspect Git status and the intended version locally and remotely. Never reuse a published version; this repository already has historical v1 and v2 tags.
1. Run `mise install`, `mise run install` and `mise run all`. The build writes only `.cache/site/`; app configuration stays isolated. If unrelated global mise tools prevent setup, use `MISE_IGNORED_CONFIG_PATHS` with the actual global configuration path, without editing the workstation configuration.
1. Review the built README at desktop and mobile widths. Refresh the two terminal screenshots only when theme visuals change.
1. With publication authorized, update explicit package versions, generate release notes, commit the candidate and push `main`. Verify its CI and Pages deployment before tagging that exact commit.
1. Create an annotated, unused semantic-version tag and publish a GitHub release with the verified scope and outstanding native acceptance gaps. Automatic source archives are the release payload; no Python package or extension marketplace publication is implied.
1. Verify the remote peeled tag, public release state and the Pages URL. Remove only task-owned temporary outputs.
