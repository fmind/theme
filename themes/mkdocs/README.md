# MkDocs

Fmind theme for [MkDocs](https://www.mkdocs.org/) sites that use the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

Format: [Material custom colors](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/#custom-colors) · [Material color variables](https://github.com/squidfunk/mkdocs-material/blob/master/src/templates/assets/stylesheets/main/_colors.scss)

## Install

Copy `fmind.css` into your `docs/` directory, then select custom primary colors and add the file to `extra_css` in `mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    primary: custom
extra_css:
  - fmind.css
```
