---
version: alpha
name: Fmind
description: Calm, exact, spacious light design for Médéric Hurier's (Fmind) own work on AI agents, MLOps and security.
colors:
  canvas: "#FFFFFF"
  panel: "#F1F3F4"
  border: "#9AA0A6"
  muted: "#595D62"
  foreground: "#202124"
  primary: "#174EA6"
  focus: "#4285F4"
  selection: "#D2E3FC"
  error: "#A50E0E"
  error-accent: "#EA4335"
  error-surface: "#FAD2CF"
  warning: "#934900"
  warning-accent: "#E37400"
  highlight: "#FBBC04"
  warning-surface: "#FEEFC3"
  success: "#0D652D"
  success-accent: "#34A853"
  success-surface: "#CEEAD6"
  type: "#681DA8"
  information: "#00636D"
typography:
  display:
    fontFamily: Google Sans
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.25
  headline-lg:
    fontFamily: Google Sans
    fontSize: 36px
    fontWeight: 700
    lineHeight: 1.25
  headline-md:
    fontFamily: Google Sans
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.375
  headline-sm:
    fontFamily: Google Sans
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.375
  body-lg:
    fontFamily: Google Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.625
  body-md:
    fontFamily: Google Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.625
  body-sm:
    fontFamily: Google Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: Google Sans
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0.1em
  code-md:
    fontFamily: Google Sans Code
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
rounded:
  md: 8px
  lg: 12px
  xl: 16px
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  reading-width: 768px
  page-width: 1152px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.canvas}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.full}"
  button-secondary:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.full}"
  input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm}"
  chip:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
  code-inline:
    textColor: "{colors.primary}"
    typography: "{typography.code-md}"
  code-block:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.foreground}"
    typography: "{typography.code-md}"
    rounded: "{rounded.lg}"
  card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
  selection:
    backgroundColor: "{colors.selection}"
    textColor: "{colors.foreground}"
  cursor:
    backgroundColor: "{colors.focus}"
    width: 2px
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
  underline-error:
    backgroundColor: "{colors.error-accent}"
    height: 2px
  marker-warning:
    backgroundColor: "{colors.warning-accent}"
    size: 8px
  label-mode:
    backgroundColor: "{colors.success-accent}"
    textColor: "{colors.foreground}"
    typography: "{typography.label-md}"
  match:
    backgroundColor: "{colors.warning-surface}"
    textColor: "{colors.foreground}"
  match-current:
    backgroundColor: "{colors.highlight}"
    textColor: "{colors.foreground}"
  diff-added:
    backgroundColor: "{colors.success-surface}"
    textColor: "{colors.foreground}"
  diff-removed:
    backgroundColor: "{colors.error-surface}"
    textColor: "{colors.foreground}"
  badge-error:
    backgroundColor: "{colors.error}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.full}"
  badge-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.full}"
  badge-success:
    backgroundColor: "{colors.success}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.full}"
  badge-information:
    backgroundColor: "{colors.information}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.full}"
  badge-type:
    backgroundColor: "{colors.type}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.full}"
  diagram-group:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.muted}"
  diagram-container:
    backgroundColor: "{colors.selection}"
    textColor: "{colors.foreground}"
  diagram-component:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.foreground}"
  diagram-actor:
    backgroundColor: "{colors.success-surface}"
    textColor: "{colors.foreground}"
  diagram-external:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.muted}"
  diagram-step:
    backgroundColor: "{colors.warning-surface}"
    textColor: "{colors.foreground}"
  diagram-terminal:
    backgroundColor: "{colors.foreground}"
    textColor: "{colors.canvas}"
---

# Fmind Design

## Overview

Calm, exact, spacious and technically grounded. Inspired by Google's product design, interfaces focus on the user's immediate task and strip away cognitive load: one clear purpose per view, sensible defaults that work on the first click, and progressive disclosure for complexity. The reader or user is a peer who checks one claim before believing the rest, so every screen and visual carries evidence: crisp geometry, editable diagrams and real labels over decorative imagery or chrome.

**Scope.** This is the default design for Médéric Hurier's (Fmind) own work: fmind.dev, applications, articles, talks, courses, open-source repositories, documentation and media. When the work belongs to a customer or employer, use their design system, brand guide, templates, fonts and logo instead. Ask for their guide rather than inferring a palette, and never mix brands in one asset. An existing project's established identity also wins over this default.

The design is light only. Terminal and editor themes in this repository apply the same palette to syntax and ANSI roles.

## Colors

The palette is the 15 Google News colors plus five custom shades (white, dark gray, dark orange, purple and teal). Each hue has three jobs: dark shades carry text, bright shades mark active states and accents, and pale shades provide surfaces.

- **White (#FFFFFF) — canvas:** the main background and label text on dark fills.
- **Light gray (#F1F3F4) — panel:** groups, panels, code blocks and neutral surfaces.
- **Gray (#9AA0A6) — border:** decorative boundaries and separators; never small text.
- **Dark gray (#595D62) — muted:** secondary text, comments and essential control borders.
- **Charcoal (#202124) — foreground:** body text, variables and punctuation.
- **Dark blue (#174EA6) — primary:** headings, links, keywords, calls and the logo frame. The single brand accent.
- **Medium blue (#4285F4) — focus:** cursors, active controls and focus rings.
- **Light blue (#D2E3FC) — selection:** selected rows and primary containers.
- **Dark red (#A50E0E), medium red (#EA4335), light red (#FAD2CF) — error:** error text, markers and underlines, removed or failed regions.
- **Dark orange (#934900), orange (#E37400), yellow (#FBBC04), light yellow (#FEEFC3) — warning:** warning text, numbers and constants; attention fills; active tabs and current matches; changed or caution regions.
- **Dark green (#0D652D), medium green (#34A853), light green (#CEEAD6) — success:** strings, success text and additions; success markers; added regions and actor nodes.
- **Purple (#681DA8) — type:** types, builtins and secondary emphasis.
- **Teal (#00636D) — information:** informational text and diagnostics.

## Typography

Google Sans carries headings and body text; Google Sans Code carries code, commands, paths and protocol fields. Terminals use GoogleSansCode Nerd Font Mono. Use only regular (400), semibold (600) and bold (700), with real bold and italic faces; never synthesize slanting or weight.

Headlines are bold dark charcoal or dark blue. Body text is regular charcoal with relaxed leading. Labels are small bold uppercase in dark gray with wide tracking. Bundle the static TTF faces with their OFL notices in standalone deliverables and verify they load before export: [Google Sans](https://github.com/googlefonts/googlesans) and [Google Sans Code](https://github.com/googlefonts/googlesans-code).

## Layout

Generous whitespace on a 4px unit, with 8px steps between items and 24–32px margins. Long-form reading and focused single-purpose tools stay within 768px; wider data or multi-pane pages stay within 1152px. One job per view, one idea per slide, one thesis per diagram, one concept per illustration.

Applications follow Google's canonical layouts and progressive disclosure instead of dense dashboards:

- **Single workspace (default):** one centered column (`768px`) with the primary input, action and inline result in a single vertical flow, like Google Search or a document canvas.
- **List-detail or supporting pane:** split up to `1152px` into at most two panes (a primary content area plus a list or contextual inspector) only when the task compares items or inspects selections; collapse to a single pane on narrow viewports.
- **Progressive disclosure:** keep only the 1–3 controls needed for the main run visible; tuck advanced parameters, filters and raw diagnostics behind an expansion panel (`<details>`) or overflow menu until requested.

## Elevation & Depth

Flat. Hierarchy comes from tonal layers (white canvas, light gray panels, light blue containers), 1–2px strokes and typography, not shadows or gradients. Separate related groups with whitespace or a single 1px divider rather than nesting bordered cards inside cards.

## Shapes

Softly rounded rectangles: 8px for small controls, 12px for code blocks and tiles, 16px for cards and illustration frames, pills for buttons and badges. Lines are solid for flows and dashed for anything outside the boundary being described.

## Components

Application components keep interaction direct, predictable and low-noise:

- **Buttons and actions:** limit each view to one `button-primary` pill (`#174EA6` fill, white text) for the main action. Subordinate secondary actions with `button-secondary` (`#F1F3F4` fill, charcoal text) or plain text links; never place competing primary buttons side by side.
- **Inputs and forms:** `input` fields sit on white canvas with a 1px `#595D62` control border, `8px` radius and a 2px `#4285F4` focus ring. Pair every field with a visible label, prefill sensible defaults so the form works immediately, and validate inline (`underline-error` and `#A50E0E` helper text) rather than with popups.
- **Cards, lists and chips:** `card` containers group related content with `16px` radius and `16–24px` padding; `chip` elements hold compact filters or attributes on `#F1F3F4`. Separate list rows with whitespace or a 1px `#9AA0A6` `divider`.
- **Inline states (empty, loading, error, result):** render feedback in place within the workspace. Empty states explain what to do next in one muted sentence or starter example; errors state the failure and recovery on `#FAD2CF` with `#A50E0E` text; reserve modal dialogs for destructive confirmations.

Diagram components carry fixed meanings; reinforce each with a label, shape or line style rather than color alone.

- **diagram-group:** a labelled boundary holding other shapes (platform, layer, zone); gray stroke, the quietest fill.
- **diagram-container:** a major building block the text names; dark blue 2px stroke.
- **diagram-component:** a leaf part inside a container; gray stroke, neutral on purpose.
- **diagram-actor:** a human or calling system where the flow enters; dark green 2px stroke.
- **diagram-external:** something outside the described boundary; gray dashed stroke. A rejected alternative is an external whose label says so.
- **diagram-step:** one numbered stage of a sequence; dark orange stroke.
- **diagram-terminal:** where a flow starts or stops; solid charcoal box with its label inside.

Flows and arrows use dark blue. Inline code uses dark blue; code blocks sit on light gray. Status badges put white text on the dark shade of their role. Medium blue and medium red never carry text: they mark cursors, focus and error underlines. Current matches and active tabs use yellow, ordinary matches light yellow, and diffs the pale surface of their role.

## Do's and Don'ts

- Do give each view one focal point and one primary action, revealing secondary controls progressively.
- Do handle empty, loading, error and result states inline with plain-language recovery.
- Do use dark shades for text and bright shades only for fills, markers and accents.
- Do keep text at 4.5:1 contrast or more on its actual surface, and essential controls at 3:1.
- Do choose charcoal or white label text on filled shapes by measured contrast.
- Do keep editable sources (D2, Mermaid, SVG, Typst, VHS tapes) beside every export.
- Do copy approved artwork (logo, banners, wallpapers) unchanged instead of recoloring it.
- Don't add unrequested application chrome (navigation bars, sidebars, tabs, KPI ribbons, settings drawers, fake user menus or toast spam).
- Don't nest bordered cards inside cards or place multiple primary buttons in the same view.
- Don't use gradients, drop shadows, neon, dark backgrounds or generic AI imagery.
- Don't put readable technical labels or data in generated imagery.
- Don't add colors outside this palette; extend a semantic role here first.
- Don't apply this design to customer work.
