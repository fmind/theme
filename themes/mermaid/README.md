# Fmind for Mermaid

Files: [fmind.json](fmind.json).

Format: [Mermaid theme configuration](https://mermaid.js.org/config/theming.html) · [Mermaid CLI](https://mermaid.js.org/config/mermaidCLI.html)

## Installation

Pass the configuration to Mermaid CLI:

```sh
mmdc --configFile fmind.json --input diagram.mmd --output diagram.svg
```

In a page, pass the same object to `mermaid.initialize()`. In Markdown that renders Mermaid itself, such as GitHub, copy the `theme` and `themeVariables` keys into the diagram frontmatter:

```mermaid
---
config:
  theme: base
  themeVariables:
    primaryColor: "#f1f3f4"
    primaryTextColor: "#202124"
    primaryBorderColor: "#174ea6"
    lineColor: "#174ea6"
---
flowchart LR
  Evidence --> Decision --> Outcome
```

The file customizes Mermaid's `base` theme, the only one that accepts `themeVariables`. Nodes are light gray with a dark blue border, flows are dark blue, notes are light yellow, and pie, mindmap, timeline and Git series follow the chart order of [DESIGN.md](../../DESIGN.md#components). Load Google Sans before rendering, or Mermaid falls back to a system sans-serif.

User journey actors and faces keep Mermaid's built-in colors, and timeline events use tints that Mermaid derives. Tested with Mermaid 12.3.0 and Mermaid CLI 12.2.0 on flowchart, sequence, state, class, entity, Gantt, pie, mindmap, timeline and Git diagrams.
