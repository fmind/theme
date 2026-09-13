# fmind/theme

A phosphor-green terminal theme, defined once and rendered into every tool that takes a palette.

![Syntax preview](preview/fmind-code.svg)

![Shell preview](preview/fmind-shell.svg)

## The palette

Green carries the body and the code you wrote. Three cool tiers — teal, cyan, ice — carry what the language knows. Amber holds the literals, red and orange the signals, and one violet holds the keyword. Comments are grey and delimiters bone, so the two things you do not read recede out of the green entirely.

![The fifteen roles](preview/fmind-roles.svg)

Sixteen ANSI slots, fifteen syntax roles. The bright half is not a mechanical lightening of the normal half: each secondary is a relative of one primary — `parameter` of `variable`, `property` of `type`, `builtin` of `keyword` — placed as a role in its own right. Kinship is information; identity is a defect.

Violet is the one colour that is not part of a phosphor tube, and it earned the slot. With `keyword`, `type` and `variable` all green, the keyword sat 0.126 from the nearer of the other two and the three were routinely misread. It now sits **0.431** from the body text. No other single change measured close to that.

## What makes it readable

`palette.py` holds the contract and both scripts import it, so what is designed and what is shipped are measured by the same rules.

| check | rule | this palette |
| --- | --- | --- |
| contrast | body ≥ 9:1, other roles ≥ 4.5:1, comments capped at 6:1 so dim stays dim | body 15.8:1, dimmest 4.5:1 |
| separation | every pair ≥ 0.085 in OKLab, and up to 0.130 for pairs that sit side by side | closest pair 0.118 |
| saturation | ≥ 78% of the chroma sRGB has at that hue and lightness | lowest 84% |

Separation is the check a green theme needs and a normal theme gets for free, and it has to cover **every** pair, not the ones you thought to name. An earlier revision weighted 35 of the 105 pairs and left `parameter` 0.043 from `builtin` — two indistinguishable colours sitting next to each other on every call with arguments.

Saturation is measured against the gamut rather than as a flat number, because a flat floor is a green-specific value wearing a general name. sRGB gives hue 145 a chroma ceiling of 0.268 and hue 205 only 0.146, so "chroma ≥ 0.14" reads as "no hue but green" — which is how this theme came to have only one.

## Bold yes, italic no

`FiraCode Nerd Font Mono` ships a real Bold face and **no italic face at all**, so bold carries what hue cannot. It goes on `function`, `keyword` and `error` — the roles you scan for rather than read through.

Ghostty's `bold-is-bright` must stay `false`, or bold silently swaps six semantic colours for six others. Set `font-synthetic-style = no-italic,no-bold-italic` to stop italics being faked by slanting upright glyphs.

## Use it

```bash
uv run render.py            # validate and render
uv run render.py --check    # validate only, write nothing
```

`render.py` exits non-zero rather than ship an unreadable terminal, so it is safe in a pre-commit hook or in CI.

- `palettes/fmind.yaml` — the source of truth. Edit this.
- `palette.py` — the contract and the colour maths.
- One folder per tool, generated. Never edit; re-run the renderer.

## The other grounds

A theme ships more than one background. A diff row, a completion menu, the line the cursor is on and a selection are each the ground with a little of one slot pulled into it — and each has text on top, so each is audited like the ground.

They are named by target luminance, not by blend weight, because the blend happens in linear light and the slots do not start from the same place. Pulling 18% toward this palette's near-white `green` lands at luminance 0.161 — an added line brighter than most themes' body text, with body text on it at **3.7:1** and `function` at 1.7:1. The same 18% toward `red` lands at 0.041, four times darker. One luminance per surface means an added row and a removed row sit the same distance off the ground and only the hue tells them apart, which is the entire job of a diff.

| surface | luminance | body text on it |
| --- | --- | --- |
| current line | 0.006 | 14.1:1 |
| panel, menu, toolbar | 0.010 | 13.2:1 |
| added, removed, changed row | 0.014 | 12.4:1 |
| selection, and the emphasised run | 0.022 | 11.0:1 |

Body text holds the same 9:1 it holds against the ground; the other roles drop to 3:1, because a surface is where you read one line rather than a whole file.

## Wiring each tool

| tool | file | how |
| --- | --- | --- |
| Ghostty | `ghostty/fmind` | Copy into `~/.config/ghostty/themes/`, then `theme = fmind` |
| Zellij | `zellij/fmind.kdl` | Copy into `~/.config/zellij/themes/`, then `theme "fmind"` |
| fish | `fish/fmind.fish` | Source it from `~/.config/fish/conf.d/` |
| fzf | `fzf/fmind.conf` | Point `FZF_DEFAULT_OPTS_FILE` at it |
| Starship | `starship/fmind.toml` | Merge the `[palettes.*]` block into `~/.config/starship.toml` |
| delta | `delta/fmind.gitconfig` | `[include] path = …`, or paste into the `[delta]` section |
| k9s | `k9s/fmind.yaml` | Copy into `~/.config/k9s/skins/`, then set `skin:` |
| gh-dash | `gh-dash/fmind.yml` | Merge the `theme:` block into `~/.config/gh-dash/config.yml` |
| opencode | `opencode/fmind.json` | Copy into `~/.config/opencode/themes/`, then `"theme": "fmind"` |
| ptpython | `ptpython/fmind.py` | Drop next to `config.py`, then install `CODE` and `UI` |
| Neovim | `nvim/colors/fmind.lua` | Copy into `~/.config/nvim/colors/`, then `colorscheme fmind` |

Everything else reads the terminal's own colours and is themed for free: `bat --theme=ansi`, lsd, lazygit, lazydocker, bottom, atuin, yazi, fastfetch, gh, ripgrep, jq. Keeping them on ANSI is deliberate — one Ghostty line reskins the lot. What that costs is the bright half: a tool reading slot 12 gets `parameter` whatever it meant by "bright blue".

For that to be true the Ghostty file also reissues the **greyscale ramp**, slots 232-255. A theme that stops at slot 15 leaves every tool that reaches into the 256-colour cube looking untouched — lsd asks for `243`, and it is not a colour the palette sets. The ramp is re-emitted at xterm's own luminance (drift under 0.005) with the theme's green cast, so those greys join in. The 6×6×6 colour cube is left alone, because tools compute gradients from its structure.

fzf is the one file here that carries slot numbers rather than colours. It draws over whatever is already on the screen, so hex would pin the finder to one palette while the terminal behind it followed Ghostty; `-1` leaves the ground and the body text exactly as they are.

Neovim gets a real colorscheme rather than a sixteen-colour fallback, because treesitter distinguishes captures a terminal never can: a call from its arguments, a builtin from a user function, an attribute from the object it hangs off. It drops into `colors/` on the runtimepath, so no plugin is needed.

Two tools cannot take a palette from anywhere and are left alone: **Grok** ships five built-in themes with no custom slot (`dark` is the one that survives quantization to sixteen colours), and **Claude Code** has `dark-ansi`, which is the terminal's own palette by another name.

## Adding a tool

Write a function in `render.py` that takes a `Palette` and returns `(path, contents)`, then add it to `TOOLS`. `Palette` exposes `ground`, `text`, `cursor`, `slot(0..15)`, `role(name)` and `surface(name)`; reach for `surface()` rather than mixing your own background, so the new one is audited with the rest.
