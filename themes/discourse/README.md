# Discourse

Fmind theme component for [Discourse](https://www.discourse.org/).

Format: [Discourse theme structure](https://meta.discourse.org/t/structure-of-themes-and-theme-components/60848) · [color_definitions.scss](https://github.com/discourse/discourse/blob/main/app/assets/stylesheets/color_definitions.scss)

## Install

Discourse reads `about.json` from the root of a git repository, so this component installs from an archive rather than from this repository's URL.

1. From a clone of this repository, write the archive outside the checkout: `git archive --format=zip --output="$HOME/fmind-discourse.zip" HEAD:themes/discourse`.
2. In the Discourse admin, open `Appearance` → `Themes & components` → `Components`.
3. Click `Install` → `From your device` and upload `fmind-discourse.zip`.
4. On the component page, add your theme under `Include component on these themes`.
