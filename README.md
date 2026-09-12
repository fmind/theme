# fmind/theme

A phosphor-green terminal theme, defined once and rendered into every tool that takes a palette.

The palettes are green-dominant on purpose: green carries the body and the syntax, while red and amber are held back so an error still looks like an error.
Nothing in Ghostty's 395 built-in themes occupies that space — they are either monochrome green (`HaX0R_GR33N`, `Retro`, where all six hue slots are the same green) or only incidentally green (`RetroLegends`, `Homebrew`, at 17%).

## Layout

- `palettes/*.yaml` — the source of truth, one file per variant. Edit these.
- `palette.py` — the readability contract and the colour maths. Imported by both scripts, so what gets designed and what gets shipped cannot drift apart.
- `explore.py` — designs new palettes by optimising role assignment under that contract.
- `render.py` — validates a palette, then renders it for each tool.
- `out/<tool>/<variant>` — generated. Never edit; re-run the renderer instead.

## Use it

```bash
uv run render.py             # validate and render every palette
uv run render.py --check     # validate only, write nothing
uv run render.py split-base  # just one variant
uv run explore.py            # design the variant set again
uv run explore.py --dry-run  # report the design pass without writing
```

`render.py` exits non-zero if a palette would ship an unreadable terminal, so it is safe in a pre-commit hook or in CI.

## Two ways a green theme fails

Both are silent until you are reading a diff at midnight, so the contract in `palette.py` checks both.

1. **Contrast** — a colour that cannot be seen against the ground. Default text ≥ 9.0:1, other roles ≥ 5.0:1, and comments are *capped* at 6.0:1 as well as floored at 2.6:1, because a dim colour as bright as body text is not dim.
1. **Separation** — a colour that can be seen but not told apart from its neighbour. Required per pair of syntax roles and weighted by how often the two sit side by side.

The second check is what a green theme needs and a normal theme gets for free.
When five of eight roles share a hue, contrast alone will happily approve a palette in which strings, functions and body text are one indistinguishable wash.

Weighting matters more than it sounds. A flat threshold over-constrains the rare pairs and under-constrains the ones you read on every line, so the requirement is `0.130 × weight`:

| pair | weight | needs |
| --- | --- | --- |
| `variable` / `function` | 1.00 | 0.130 |
| `variable` / `string` | 1.00 | 0.130 |
| `function` / `type` | 1.00 | 0.130 |
| `variable` / `type` | 0.90 | 0.117 |
| `string` / `number` | 0.80 | 0.104 |
| `comment` / `string` | 0.60 | 0.078 |

One trap worth recording: measure the **rounded hex**, not the continuous OKLCh value you optimised. Quantising to 8 bits per channel costs up to ~0.03 of distance, which is enough to flip a marginal palette from pass to fail between design and render. `explore.py` evaluates separation on the shipped hex and keeps a `SAFETY_MARGIN` on top.

## Fourteen roles, not six

A terminal has sixteen slots and most themes spend six of them, generating the bright half as mechanical lightenings of the normal half.
That wastes six addressable colours, and it produces a palette that cannot tell a parameter from a local or a builtin from a user function — which is why `contrast(fg, bg)` rendered as one undifferentiated green.

Under the old model those two roles measured **0.050 apart**. Designed as roles in their own right, the same sixteen slots carry fourteen meanings:

| primary | slot | its relative | slot |
| --- | --- | --- | --- |
| `variable` | fg | `parameter` | 12 |
| `string` | 2 | `escape` | 10 |
| `number` | 3 | `constant` | 11 |
| `function` | 4 | `property` | 14 |
| `keyword` | 5 | `builtin` | 13 |
| `error` | 1 | `warning` | 9 |
| `type` | 6 | | |
| `comment` | 8 | | |

A secondary role is a relative of its primary and may sit closer to it than to anything else — that kinship is information, not a defect. It may never be identical.

The two axes do different work: **lightness** carries the ramp from dead code up to the live line, and **chroma** separates a role from its own relative at the same height. A parameter is a dimmer green at nearly the height of a local; a builtin is a dimmer green beside a keyword.

## The matrix ramp

Every palette is anchored on the film's own four stops rather than on a designer's taste:

```text
deep trail  #003b00  L 0.305  C 0.104   -> comment
mid trail   #008f11  L 0.564  C 0.187   -> function
body        #00ff41  L 0.869  C 0.278   -> variable, the neon default text
leading     #ccffcc  L 0.952  C 0.086   -> string, the bright head of the rain
```

`MIN_BODY_CHROMA` in `palette.py` holds body text at 0.18 or above, so no future variant can drift back to the pale green-white that measured 0.031.

### Matrix core

| variant | neon | min chroma | green | separation | idea |
| --- | --- | --- | --- | --- | --- |
| `matrix-burn` | 0.295 | 0.148 | 67% | 0.115 | Prime driven to the edge of the gamut at every height - the most saturated fourteen-role palette that still separates. |
| `matrix-forge` | 0.279 | 0.145 | 67% | 0.102 | The secondary roles pushed hardest of all, so a parameter and a builtin carry as much colour as the primaries they belong to. |
| `matrix-prime` | 0.278 | 0.146 | 67% | 0.110 | Prime with the pastels gone. |
| `matrix-void` | 0.270 | 0.147 | 83% | 0.084 | Pure black, and no amber at all - numbers and constants are saturated greens too, leaving red as the only colour that is not green. |
| `matrix-strata` | 0.257 | 0.148 | 67% | 0.109 | The lightness ladder stretched as far as the gamut allows, so fourteen saturated roles read as one clean gradient from dead code to live line. |

### Matrix, balanced

| variant | neon | min chroma | green | separation | idea |
| --- | --- | --- | --- | --- | --- |
| `matrix-amber` | 0.277 | 0.147 | 67% | 0.110 | The amber pair taken to the top of its gamut, so a number and a named constant burn like the greens instead of sitting behind them. |
| `matrix-deep` | 0.274 | 0.147 | 67% | 0.114 | A ground with real green in it, so the tube reads as lit from behind and the darker rungs have somewhere to sit. |
| `matrix-lanes` | 0.268 | 0.146 | 67% | 0.111 | Primaries run warm and their relatives run cool, so kinship reads as a shift in temperature rather than a loss of colour. |
| `matrix-signal` | 0.264 | 0.147 | 67% | 0.110 | The red pair taken neon: an error and a warning as saturated as the greens they interrupt, rather than the salmon pink they were. |
| `matrix-arc` | 0.251 | 0.148 | 67% | 0.109 | The roles sweep the whole green window in order, so hue itself becomes the gradient and two roles at the same height are never the same green. |

## No role may go pastel

The first fourteen-role attempt separated each secondary from its primary by dropping the secondary's chroma. It passed every check and produced exactly the washed-out colours it was meant to avoid:

| role | then | now |
| --- | --- | --- |
| `parameter` | `#73a07f` 0.069 | `#06b67b` 0.152 |
| `builtin` | `#76ac87` 0.079 | `#35bf79` 0.155 |
| `property` | `#9cdeb1` 0.092 | `#8af5a6` 0.148 |
| `constant` | `#fad48e` 0.098 | `#ffd448` 0.158 |
| `warning` | `#ff958c` 0.129 | `#f27c57` 0.154 |

Low chroma *is* pastel, so buying separation with it is self-defeating. `MIN_ROLE_CHROMA = 0.14` now forbids it, and separation has to come from lightness and hue instead — which is where it belonged. With chroma pinned near the top of the gamut, hue becomes the solver's only slack, so the ten green roles fan out across 17-22° of the window rather than collapsing towards grey.

`string` and `comment` are exempt for reasons of physics rather than taste: `string` sits near L 0.95 where the sRGB green gamut has no chroma left, and `comment` is deliberately recessive.

## Bold yes, italic no

This is the third axis, and with fourteen roles competing for one hue window it earns its place: bold distinguishes without spending a colour.

`BOLD_ROLES` in `palette.py` applies it to `function`, `keyword` and `error` — the roles you *scan* for rather than read through — and `render.py` emits it in the fish config.

Bold is safe and worth using. `FiraCode Nerd Font Mono` ships a real Bold face, and Ghostty's `bold-is-bright` defaults to `false`, so bold renders as weight rather than swapping to the bright palette — which matters here, because the bright swap would silently replace the chosen greens.

Italic should be avoided. FiraCode ships **no italic face at all** (only Light, Regular, Medium, Retina, SemiBold, Bold). Ghostty's `font-synthetic-style` defaults to on, so italics get synthesised by slanting the upright glyphs, which its own documentation notes "will generally not look as good". Slanted monospace at 13px, green on black, is where legibility goes to die.

To opt out of synthesis entirely:

```
font-synthetic-style = no-italic,no-bold-italic
```

To have real italics instead, point Ghostty at a face that has them and keep FiraCode for upright text:

```
font-family-italic = "Maple Mono"
```

Dim (SGR 2) is the third axis, is well supported everywhere, and is the better choice for comments and secondary text than italic.

## Wiring each tool

Generated files are meant to be referenced, not pasted, wherever the tool allows it.

| tool | file | how |
| --- | --- | --- |
| Ghostty | `out/ghostty/<variant>` | Copy into `~/.config/ghostty/themes/`, then `theme = <variant>` |
| Zellij | `out/zellij/<variant>.kdl` | Copy into `~/.config/zellij/themes/`, then `theme "<variant>"` |
| fish | `out/fish/<variant>.fish` | Source it from `~/.config/fish/conf.d/` |
| Starship | `out/starship/<variant>.toml` | Merge the `[palettes.*]` block into `~/.config/starship.toml` |
| delta | `out/delta/<variant>.gitconfig` | `[include] path = …`, or paste into the `[delta]` section |
| k9s | `out/k9s/<variant>.yaml` | Copy into `~/.config/k9s/skins/`, then set `skin:` |
| gh-dash | `out/gh-dash/<variant>.yml` | Merge the `theme:` block into `~/.config/gh-dash/config.yml` |

fish is where the role mapping becomes explicit rather than implied, since it names its own roles: `command` takes the function slot, `quote` takes strings, `redirection` and `option` take types.

Tools that read the terminal's own 16 ANSI colours need no file and pick the palette up for free: `bat` (`--theme=ansi`), `lsd`, lazygit, lazydocker, bottom, atuin, yazi, fzf, fastfetch.
Keeping them on ANSI is deliberate — it means one Ghostty line reskins them.

Neovim is the one holdout. A 16-colour palette under treesitter is materially worse than a real colorscheme, so it needs a Lua theme rather than a generated config; that is not built yet.

## Adding a tool

Write a function in `render.py` that takes a `Palette` and returns `(relative path, contents)`, then add it to `RENDERERS`.
`Palette` exposes `ground`, `text`, `cursor`, `slot(0..15)` and `role("function")`; `mix()` from `palette.py` blends toward the ground for diff backgrounds.

## Adding a variant

Add a `Policy` to `POLICIES` in `explore.py`. A policy is a ground plus a box in OKLCh for each role — hue window, lightness range, chroma range — and the optimiser finds a point in each box that satisfies every pairwise requirement.
If a policy cannot be satisfied it reports negative slack rather than shipping something unreadable, which usually means a role needs to leave the green window.
