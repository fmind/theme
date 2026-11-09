# Fmind for CSS

Files: [fmind.css](fmind.css).

Format: [CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties) · [design.md export](https://github.com/google-labs-code/design.md)

## Installation

Copy `fmind.css` into your site or rendered page and load it before your own styles:

```html
<link rel="stylesheet" href="fmind.css">
```

```css
body {
  background: var(--fmind-color-canvas);
  color: var(--fmind-color-foreground);
}
a {
  color: var(--fmind-color-primary);
}
```

The file defines the [DESIGN.md](../../DESIGN.md) colors (`--fmind-color-*`), spacing (`--fmind-spacing-*`) and radii (`--fmind-rounded-*`) on `:root`. Fonts are not included: load [Google Sans](https://github.com/googlefonts/googlesans) and [Google Sans Code](https://github.com/googlefonts/googlesans-code) yourself and set the sizes from DESIGN.md.

`fmind.css` is generated from DESIGN.md; edit the tokens there and run `mise run tokens`.
