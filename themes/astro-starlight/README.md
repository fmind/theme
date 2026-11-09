# Fmind for Astro Starlight

Custom CSS theme for [Astro Starlight](https://starlight.astro.build/).

Files: [fmind.css](fmind.css).

Format: [Starlight custom properties](https://github.com/withastro/starlight/blob/main/packages/starlight/src/style/props.css) · [Starlight custom CSS](https://starlight.astro.build/guides/css-and-tailwind/)

## Installation

Copy [fmind.css](fmind.css) to `src/styles/fmind.css` in your project, then add it to Starlight's `customCss`:

```js
// astro.config.mjs
export default defineConfig({
  integrations: [
    starlight({
      customCss: ['./src/styles/fmind.css'],
    }),
  ],
});
```
