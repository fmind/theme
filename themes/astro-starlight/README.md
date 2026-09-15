# Fmind for Astro Starlight

Custom CSS theme for [Astro Starlight](https://starlight.astro.build/).

## Installation

Import [fmind.css](fmind.css) into your Starlight custom CSS configuration:

```js
// astro.config.mjs
export default defineConfig({
  integrations: [
    starlight({
      customCss: [./src/styles/fmind.css],
    }),
  ],
});
```
