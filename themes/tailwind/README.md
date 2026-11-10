# Fmind for Tailwind CSS

Files: [fmind.css](fmind.css).

Format: [Tailwind CSS theme variables](https://tailwindcss.com/docs/theme)

## Installation

Requires Tailwind CSS v4. Copy `fmind.css` next to your stylesheet and import it after Tailwind:

```css
@import "tailwindcss";
@import "./fmind.css";

@theme {
  --font-sans: var(--font-body-md), sans-serif;
  --font-mono: var(--font-code-md), ui-monospace, monospace;
}
```

The `@theme` block adds the [DESIGN.md](../../DESIGN.md) tokens under their own names: colors (`bg-canvas`, `text-foreground`, `text-primary`, `border-border`, `bg-error-surface`), type (`font-body-md`, `text-headline-lg`, `leading-body-md`), radii (`rounded-md` to `rounded-xl`) and spacing (`p-md`, `max-w-reading-width`, `max-w-page-width`). Use `border-muted` (`#595D62`) rather than decorative `border-border` (`#9AA0A6`) on form controls so borders meet 3:1 contrast, and note that `--spacing-xs` to `--spacing-xl` take precedence over Tailwind's t-shirt `max-w-xs` to `max-w-xl` utilities (prefer `max-w-reading-width`, `max-w-page-width` or explicit widths). Add the [daisyUI theme](../daisyui/) for components.

`fmind.css` is generated from DESIGN.md; edit the tokens there and run `mise run tokens`. For Tailwind v3, generate a `theme.extend` object with `npx @google/design.md@0.4.0 export --format json-tailwind DESIGN.md`. Tested with Tailwind CSS 4.3.4.
