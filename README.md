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
uv run render.py fmind       # just one variant
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

## The theme

**Fmind** is the default across every application. One palette, `palettes/fmind.yaml`, rendered into `out/<tool>/fmind` for each tool that takes one.

| | |
| --- | --- |
| ground | `#000000` — pure black |
| body text | `#56ff40` — neon green, OKLab chroma 0.264 |
| green share | 67% of the chromatic slots |
| body contrast | 15.8:1 |
| least saturated role | 0.148 |
| tightest role pair | `keyword/builtin` at 0.113, with 0.007 to spare |

### The fourteen roles

| role | colour | L | C | hue |
| --- | --- | --- | --- | --- |
| `variable` | `#56ff40` | 0.879 | 0.264 | 142 |
| `error` | `#fb002a` | 0.622 | 0.252 | 25 |
| `string` | `#d5fcd5` | 0.953 | 0.066 | 145 |
| `number` | `#e3a92a` | 0.769 | 0.148 | 82 |
| `function` | `#008b00` | 0.552 | 0.188 | 142 |
| `keyword` | `#83dd81` | 0.819 | 0.153 | 144 |
| `type` | `#00ca00` | 0.727 | 0.247 | 142 |
| `comment` | `#24682c` | 0.459 | 0.115 | 145 |
| `warning` | `#ff692e` | 0.701 | 0.196 | 40 |
| `escape` | `#3afdb5` | 0.885 | 0.180 | 162 |
| `constant` | `#ffd449` | 0.883 | 0.157 | 91 |
| `parameter` | `#00b470` | 0.678 | 0.159 | 158 |
| `builtin` | `#01c08b` | 0.716 | 0.151 | 165 |
| `property` | `#56ebb2` | 0.846 | 0.151 | 164 |

Green carries every syntax role. Red is reserved for errors and warnings, amber for numbers and constants — those four slots are the only colours in the palette that are not green.

### Why fourteen and not six

A terminal has sixteen slots and most themes spend six, generating the bright half as mechanical lightenings of the normal half. That wastes six addressable colours and leaves a palette that cannot tell a parameter from a local or a builtin from a user function. Measured under this contract, those two roles sat **0.050 apart** — indistinguishable.

Each secondary role is a relative of one primary: `parameter` of `variable`, `property` of `type`, `builtin` of `keyword`, `escape` of `string`, `constant` of `number`, `warning` of `error`. Kinship is information; identity is a defect.

The two axes do different work. **Lightness** carries the ramp from dead code up to the live line. **Hue** separates a role from its own relative — primaries run warm, relatives run cool. Chroma does neither, because using it for separation is what makes a palette pastel.

### How it was chosen

Fmind is `prime-max` from a five-candidate shortlist, renamed. The shortlist changed one thing at a time from a baseline, and the three changes that were kept are:

| change | kept | why |
| --- | --- | --- |
| pure black ground | yes | from a candidate that also dropped amber; the ground was wanted, the amber loss was not |
| warm primaries, cool relatives | yes | kinship reads as temperature rather than as washing out |
| hotter red and orange pair | yes | preferred over the softer reds of the alternative |
| deeper green ground | no | too green |
| gamut-edge chroma | no | contrast preferred at the baseline level |

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
| Neovim | `out/nvim/colors/<variant>.lua` | Copy into `~/.config/nvim/colors/`, then `colorscheme fmind` |

fish is where the role mapping becomes explicit rather than implied, since it names its own roles: `command` takes the function slot, `quote` takes strings, `redirection` and `option` take types.

Tools that read the terminal's own 16 ANSI colours need no file and pick the palette up for free: `bat` (`--theme=ansi`), `lsd`, lazygit, lazydocker, bottom, atuin, yazi, fzf, fastfetch.
Keeping them on ANSI is deliberate — it means one Ghostty line reskins them.

Neovim gets a real colorscheme rather than a sixteen-colour fallback, and it is where the fourteen roles pay off most: treesitter distinguishes captures a terminal never can — a call from its arguments, a builtin from a user function, an attribute from the object it hangs off. The generated file sets treesitter captures, LSP semantic tokens, diagnostics and diff groups, and never sets italic. It drops into `colors/` on the runtimepath, so no plugin is needed.

## Adding a tool

Write a function in `render.py` that takes a `Palette` and returns `(relative path, contents)`, then add it to `RENDERERS`.
`Palette` exposes `ground`, `text`, `cursor`, `slot(0..15)` and `role("function")`; `mix()` from `palette.py` blends toward the ground for diff backgrounds.

## Adding a variant

Add a `Policy` to `POLICIES` in `explore.py`. A policy is a ground plus a box in OKLCh for each role — hue window, lightness range, chroma range — and the optimiser finds a point in each box that satisfies every pairwise requirement.
If a policy cannot be satisfied it reports negative slack rather than shipping something unreadable, which usually means a role needs to leave the green window.
