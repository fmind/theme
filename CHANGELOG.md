# Changelog

## 3.0.0 — 2026-09-15

### Breaking

- Move integration files from `<app>/...` to `themes/<app>/...`. Update checkout paths, raw download URLs and chezmoi external-file sources. Application destinations and existing tags are unchanged.

### Changed

- Separate validation (`checks/`) from artwork sources and generation (`artworks/`).
- Display README directly on GitHub; remove the standalone site, browser checks and Pages deployment.

- Replace app-specific validation harnesses with shared palette, structured-file, documentation and artwork checks; remove Docker and parser installation from validation.

- Add branding wallpapers and social banners with bundled Google Sans attribution.
- Correct the Standard Notes download URL and APT truecolor output.
- Improve Plasma 5 session interfaces, keyboard access and control contrast.
- List every theme alphabetically and move tool installation instructions into each theme directory.
- Simplify project documentation and add README navigation and a theme-problem form.
- Add dependency-update automation and protect version tags against modification and deletion.

Previous versions are available in [GitHub releases](https://github.com/fmind/theme/releases) and [tags](https://github.com/fmind/theme/tags).
