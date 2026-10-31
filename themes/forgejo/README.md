# Fmind for Forgejo

Light theme stylesheet for [Forgejo](https://forgejo.org/). It imports Forgejo's built-in `forgejo-light` theme and overrides its colors.

Format: [Forgejo theme loader](https://codeberg.org/forgejo/forgejo/src/branch/forgejo/templates/base/head_style.tmpl) · [forgejo-light variables](https://codeberg.org/forgejo/forgejo/src/branch/forgejo/web_src/css/themes/theme-forgejo-light.css)

## Installation

1. Copy [fmind.css](fmind.css) to `$FORGEJO_CUSTOM/public/assets/css/theme-fmind.css` on your Forgejo server.
2. In `app.ini`, add `fmind` to `THEMES` under `[ui]`. This setting replaces the built-in list, so keep the default themes you want from the [configuration cheat sheet](https://forgejo.org/docs/latest/admin/config-cheat-sheet/#ui-ui). Optionally set `DEFAULT_THEME = fmind`.
3. Restart Forgejo, then select `fmind` under Settings → Appearance.
