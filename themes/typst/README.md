# Fmind for Typst

Files: [fmind.typ](fmind.typ).

Format: [Typst styling](https://typst.app/docs/reference/styling/) · [modules](https://typst.app/docs/reference/scripting/#modules) · [color](https://typst.app/docs/reference/visualize/color/) · [raw](https://typst.app/docs/reference/text/raw/#parameters-theme)

## Installation

Keep the master copy at `~/.agents/themes/typst/fmind.typ` (deployed by [fmind/dot](https://github.com/fmind/dot)), copy `fmind.typ` next to your `.typ` sources so Typst resolves it inside the project root, and import it with zero external packages:

```typst
#import "fmind.typ": *
#show: fmind-diagram

#frame[
  #grid(
    columns: (auto, 54pt, auto, 54pt, auto),
    align: horizon,
    diagram-actor[Developer],
    flow-arrow(step: 1, caption: "commit"),
    diagram-container[
      #tile("fmind.typ", "stdlib module · zero packages")
    ],
    flow-arrow(step: 2, caption: "compile"),
    diagram-external[2× PNG · SVG · PDF],
  )
]
```

Export composed illustrations to crisp Retina PNG or vector SVG:

```sh
typst compile --format png --ppi 192 diagram.typ diagram.png
typst compile --format svg diagram.typ diagram.svg
```

For paged reports and handouts, apply `#show: fmind-doc` instead of `#show: fmind-diagram`. Fenced `raw` code blocks default to monochrome charcoal `#202124` on light gray `#F1F3F4` so Typst's stock theme never introduces off-palette colors; copy [fmind.tmTheme](../bat/fmind.tmTheme) beside the document and pass `#show: fmind-doc.with(code-theme: "fmind.tmTheme")` for full Fmind syntax highlighting.

`fmind.typ` uses only the Typst standard library: it exports `colors` (all 20 tokens), `chart-series`, `sans-font` and `mono-fonts`, `fmind-doc` and `fmind-diagram`, the seven `diagram-*` components of [DESIGN.md](../../DESIGN.md#components) (`diagram-group`, `diagram-container`, `diagram-component`, `diagram-actor`, `diagram-external`, `diagram-step` and `diagram-terminal`), plus `frame`, `chip`, `tile`, `status-badge`, `step-badge`, `flow-arrow` and `loop-back`. Tested with Typst 0.15.1 on macOS (`arm64`), verifying `fmind-diagram` (PNG and SVG) and `fmind-doc` (PDF and PNG, with and without `fmind.tmTheme`) in an isolated environment.
