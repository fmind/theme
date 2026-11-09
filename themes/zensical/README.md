# Fmind for Zensical

Files: [fmind.css](fmind.css).

Format: [Zensical custom colors](https://zensical.org/docs/setup/colors/#custom-colors) · [Material for MkDocs custom colors](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/#custom-colors)

## Installation

Copy `fmind.css` to `docs/stylesheets/`, then select custom colors on the light scheme and load the file in `zensical.toml`:

```toml
[project]
extra_css = ["stylesheets/fmind.css"]

[project.theme]
font.text = "Google Sans"
font.code = "Google Sans Code"

[[project.theme.palette]]
scheme = "default"
primary = "custom"
accent = "custom"
```

The file styles the `default` scheme only: page, navigation, links, code blocks with syntax colors, highlighted lines, marks, keys and tables. A dark `slate` scheme, if you add one, keeps its stock colors. Admonition types keep Zensical's own colors. Tested with Zensical 0.1.0 in the modern and classic variants.

## Material for MkDocs

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) reads the same variables. Use the same file in `mkdocs.yml` (not tested in Material itself):

```yaml
theme:
  name: material
  palette:
    scheme: default
    primary: custom
    accent: custom
extra_css:
  - stylesheets/fmind.css
```
