# Fmind for Astro Starlight

Custom CSS theme for [Astro Starlight](https://starlight.astro.build/).

Format: [Starlight custom properties](https://github.com/withastro/starlight/blob/main/packages/starlight/src/style/props.css) · [Starlight custom CSS](https://starlight.astro.build/guides/css-and-tailwind/)

## Installation

Import [fmind.css](fmind.css) into your Starlight custom CSS configuration:

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
