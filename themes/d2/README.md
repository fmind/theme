# Fmind for D2

Files: [fmind.d2](fmind.d2).

Format: [D2 theme overrides](https://d2lang.com/tour/themes/#customizing-themes) · [classes](https://d2lang.com/tour/classes/) · [imports](https://d2lang.com/tour/imports/)

## Installation

Copy `fmind.d2` next to your diagrams and spread-import it on the first line. The path is relative to the importing file and omits the extension:

```d2
...@fmind

user: User {class: actor}
platform: Platform {
  class: group
  api: API {class: container}
  queue: Queue {class: component}
}
model: Model API {class: external}
user -> platform.api -> model
```

The import sets the D2 theme overrides, a white canvas and dark blue connections, so shapes without a class also use palette colors. The seven classes implement the `diagram-*` components of [DESIGN.md](../../DESIGN.md#components): `group`, `container`, `component`, `actor`, `external`, `step` and `terminal`.

Render labels in Google Sans with the `--font-regular`, `--font-italic`, `--font-bold` and `--font-semibold` flags of `d2`. Tested with D2 0.9.0.
