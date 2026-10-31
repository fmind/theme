# Fmind for Redlib

Light theme for [Redlib](https://github.com/redlib-org/redlib), the successor of Libreddit.

Format: [Redlib bundled themes](https://github.com/redlib-org/redlib/tree/main/static/themes) · [Redlib theme loader](https://github.com/redlib-org/redlib/blob/main/src/utils.rs)

## Installation

Redlib compiles its themes into the binary from `static/themes/*.css`, so this applies to self-hosted instances. Copy [fmind.css](fmind.css) to `static/themes/fmind.css` in a Redlib checkout, build and run it, then select fmind under Settings → Theme, or set `REDLIB_DEFAULT_THEME=fmind` for every visitor.
