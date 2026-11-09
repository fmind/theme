# Fmind for daisyUI

Files: [fmind.css](fmind.css).

Format: [daisyUI themes](https://daisyui.com/docs/themes/)

## Installation

Requires daisyUI 5 on Tailwind CSS v4. Copy `fmind.css` next to your stylesheet, disable the built-in themes and import it after the plugin:

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: false;
}
@import "./fmind.css";
```

The theme is the default, so no `data-theme` attribute is needed. Buttons take the 8px field radius; add `rounded-full` for the pill buttons of [DESIGN.md](../../DESIGN.md#components). Add the [Tailwind theme](../tailwind/) for the remaining tokens, such as `text-muted` and `bg-selection`. Tested with daisyUI 5.7.50.
