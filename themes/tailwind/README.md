# Fmind for Tailwind CSS

Files: [fmind.css](fmind.css).

Format: [Tailwind CSS theme variables](https://tailwindcss.com/docs/theme)

## Installation

Requires Tailwind CSS v4. Copy `fmind.css` next to your stylesheet and import it after Tailwind:

```css
@import "tailwindcss";
@import "./fmind.css";
```

The `@theme` block adds the [DESIGN.md](../../DESIGN.md) tokens under their own names: colors (`bg-canvas`, `text-foreground`, `text-primary`, `border-border`, `bg-error-surface`), type (`font-body-md`, `text-headline-lg`), radii (`rounded-md` to `rounded-xl`) and spacing (`p-md`, `max-w-reading-width`, `max-w-page-width`). Add the [daisyUI theme](../daisyui/) for components.

`fmind.css` is generated from DESIGN.md; edit the tokens there and run `mise run tokens`. For Tailwind v3, generate a `theme.extend` object with `npx @google/design.md@0.4.0 export --format json-tailwind DESIGN.md`. Tested with Tailwind CSS 4.3.4.
