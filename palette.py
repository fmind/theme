"""The palette contract: what makes a phosphor palette readable, and the maths.

render.py imports this and refuses to render a palette that misses any of it,
so a source file and the theme files it produces are measured by one rule.

Readability here is several independent things, and a green theme needs each one
checked:

  contrast    can the colour be seen against the ground (WCAG 2.1)
  separation  can two colours that mean different things be told apart (OKLab)
  saturation  is the colour as vivid as its own hue allows (OKLab, gamut-relative)
  glare       is the colour quiet enough to read for eight hours (WCAG, ceilings)

The last one is the one every contrast check gets backwards. WCAG has a floor and
no ceiling, so "more contrast" always scores better and a palette optimised
against it walks straight to a maximum nobody can sit in front of all day: pure
black behind a saturated body green, five of fifteen roles above 13.7:1, and the
two roles carrying the most glyphs - `string` and `punctuation` - the loudest of
the lot. Legibility and fatigue are not the same measurement. CONTRAST_BOUNDS
therefore caps as well as floors, and the ground is required to sit off zero.

The second is the one a conventional theme gets for free and a green theme does
not. When five of eight roles share a hue, contrast alone will happily approve a
palette in which strings, functions and body text are one indistinguishable wash.
Separation is required per pair and weighted by how often the two roles actually
sit next to each other, because a flat threshold over-constrains the rare pairs
and under-constrains the ones you read on every line. On top of that weighting
sits SEPARATION_FLOOR, which every pair must clear whether or not it is named:
an earlier revision weighted 35 of the 105 pairs and left `parameter` 0.043 from
`builtin`, which is two colours the eye cannot separate at 13px sitting next to
each other on every call with arguments.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from pathlib import Path

import yaml

# ----------------------------------------------------------------- the contract

# Syntax role -> the ANSI slot tools actually paint it with. "text" is the
# default foreground; the numbers are the familiar 16-colour indices.
#
# The bright half is not decoration. Treating slots 9-14 as mechanical
# lightenings of 1-6 wastes six addressable colours and leaves a palette that
# cannot tell a parameter from a local, or a builtin from a user function - the
# reason `contrast(fg, bg)` came out as one undifferentiated green. Designed as
# roles in their own right, the same sixteen slots carry fifteen meanings.
#
# Slot 7 is the fifteenth. It used to hold an off-white that no syntax role
# reached, while brackets, commas and operators were painted with the body
# colour - putting the loudest colour in the palette on the most frequent glyphs
# on the line. It now carries `punctuation`, a bone white the delimiters recede
# into.
SLOT_OF: dict[str, str] = {
    # primary: the eight every tool paints
    "variable": "text",
    "error": "red",               # 1
    "string": "green",            # 2
    "number": "yellow",           # 3
    "function": "blue",           # 4
    "keyword": "magenta",         # 5
    "type": "cyan",               # 6
    "punctuation": "white",       # 7   brackets, commas, operators
    "comment": "bright_black",    # 8
    # secondary: the bright half, each a relative of one primary
    "warning": "bright_red",      # 9
    "escape": "bright_green",     # 10  escapes and f-string interpolation
    "constant": "bright_yellow",  # 11  UPPER_CASE, True, None
    "parameter": "bright_blue",   # 12  arguments, as distinct from locals
    "builtin": "bright_magenta",  # 13  builtins and decorators
    "property": "bright_cyan",    # 14  attributes and methods
}
ROLES: list[str] = list(SLOT_OF)

# Each secondary role is a relative of one primary - warning of error, escape of
# string, constant of number, parameter of variable, builtin of keyword, property
# of type. That kinship is information, so a relative may sit closer to its own
# primary than to anything else. It may never be identical to it.

# 1.0 means "adjacent on nearly every line, needs the full distance".
PAIR_WEIGHT: dict[tuple[str, str], float] = {
    ("variable", "function"): 1.00,
    ("variable", "string"): 1.00,
    ("variable", "comment"): 1.00,
    ("function", "keyword"): 1.00,
    ("function", "type"): 1.00,
    ("variable", "keyword"): 0.90,
    ("variable", "type"): 0.90,
    ("error", "variable"): 0.90,
    ("error", "number"): 0.90,
    ("keyword", "type"): 0.80,
    ("string", "number"): 0.80,
    ("string", "function"): 0.70,
    ("number", "function"): 0.70,
    ("type", "string"): 0.70,
    ("error", "string"): 0.70,
    ("comment", "string"): 0.60,
    ("keyword", "number"): 0.60,
    ("comment", "function"): 0.60,
    # the pairs that made `contrast(fg, bg)` unreadable: a call beside its own
    # arguments, and a local beside a parameter, happen on nearly every line
    ("function", "parameter"): 1.00,
    ("variable", "parameter"): 0.85,
    ("parameter", "type"): 0.80,
    ("parameter", "string"): 0.70,
    ("parameter", "property"): 0.70,
    # attribute access sits against both its object and the calls around it
    ("variable", "property"): 0.90,
    ("function", "property"): 0.85,
    ("type", "property"): 0.80,
    # a builtin beside a keyword, and beside a user function
    ("keyword", "builtin"): 0.85,
    ("function", "builtin"): 0.85,
    ("variable", "builtin"): 0.80,
    # literals against each other and against the code around them
    ("number", "constant"): 0.80,
    ("variable", "constant"): 0.85,
    ("string", "constant"): 0.70,
    ("string", "escape"): 0.85,
    ("error", "warning"): 0.80,
    ("comment", "parameter"): 0.60,
    # the delimiters sit against everything they enclose
    ("variable", "punctuation"): 0.90,
    ("punctuation", "string"): 0.80,
    ("punctuation", "function"): 0.75,
    ("punctuation", "property"): 0.70,
    ("punctuation", "keyword"): 0.70,
    ("punctuation", "number"): 0.70,
    ("punctuation", "parameter"): 0.70,
    ("punctuation", "comment"): 0.60,
}
PAIRS: list[tuple[str, str]] = list(PAIR_WEIGHT)
BASE_SEPARATION = 0.130

# What every pair must clear, named above or not. Roughly the distance the eye
# needs to call two colours different in 13px monospace.
SEPARATION_FLOOR = 0.085

# Body text must actually read as neon green, not as white with a green note.
#
# This is the lesson of the Split contract. Pulling default text to a pale
# green-white separated it cleanly from every other role and passed every check
# here - and produced a theme nobody would call matrix. Measured against the
# film's own ramp the gap is not subtle:
#
#   film body      #00ff41   chroma 0.278
#   Rain Split     #e9fbe8   chroma 0.031
#
# Nine times flatter. The pale near-white still has a place, but as the *leading
# character* of the rain rather than as the body, so it is spent on one accent
# role instead of on everything you read.
MIN_BODY_CHROMA = 0.18

# No role may go pastel to buy its separation.
#
# The first fourteen-role attempt separated each secondary from its primary by
# dropping the secondary's chroma - parameter 0.069, builtin 0.079, property
# 0.092. Low chroma *is* pastel, so that strategy manufactured exactly the
# washed-out colours it was meant to avoid. Separation has to come from
# lightness and hue instead, leaving chroma free to stay saturated.
#
# The threshold is a fraction of what sRGB has at that hue, not an absolute.
# A flat floor is a green-specific number wearing a general name: the gamut
# gives hue 145 a ceiling of 0.268 and hue 205 only 0.144, so "chroma >= 0.14"
# reads as "no hue but green" - which is how this palette came to have only one.
# Measured as a fraction of the ceiling, a teal at 0.13 is fully saturated teal
# while a green at 0.13 is a washed-out green, which is what the eye agrees with.
MIN_SATURATION = 0.78
CHROMA_FLOOR = 0.085

# Three roles are exempt, for reasons of physics rather than taste: `string`
# sits near L 0.95 where the green gamut has no chroma left, `comment` is
# deliberately recessive, and `punctuation` is a neutral on purpose.
CHROMA_EXEMPT: frozenset[str] = frozenset({"string", "comment", "punctuation"})

# Contrast bounds against the ground. Ceilings matter as much as floors, and for
# two different reasons.
#
# `comment` is capped because a "dim" colour as bright as body text is not dim.
# `string` and `punctuation` are capped because of glare. Contrast is the check
# that reads as free - more is always better - and it is not: the roles that
# carry the most glyphs are the ones whose loudness you pay for all day, and
# those two carry more than any other. An earlier revision put `string` at
# 19.7:1, the brightest role in the palette, on every docstring and every line of
# markdown prose; `punctuation` sat at L 0.873 against a body at L 0.879, so the
# brackets and commas - the densest glyphs on a Python line - were the same
# lightness as the identifiers they enclose and nothing receded.
#
# With both capped, three roles clear 14:1 instead of five, which is what gives
# the eye a brightness hierarchy to skim by instead of leaving hue to do all of
# the work.
CONTRAST_BOUNDS: dict[str, tuple[float, float]] = {
    "variable": (9.0, 21.0),
    "error": (5.0, 21.0),
    "string": (5.0, 15.0),
    "number": (5.0, 21.0),
    "function": (4.5, 21.0),
    "keyword": (5.0, 21.0),
    "type": (5.0, 21.0),
    "comment": (2.6, 6.0),
    "warning": (5.0, 21.0),
    "escape": (5.0, 21.0),
    "constant": (5.0, 21.0),
    "parameter": (4.5, 21.0),
    "builtin": (5.0, 21.0),
    "property": (5.0, 21.0),
    "punctuation": (6.0, 9.5),
}

# The ground is never pure black.
#
# WCAG says #000000 maximises every contrast ratio in the palette and stops
# there, because it models legibility and not fatigue. A saturated body green at
# L 0.88 against a zero ground blooms - the glyph edges halate, worse with
# astigmatism, and the eye re-accommodates on every saccade between the terminal
# and anything else on the screen. Lifting the ground by a few thousandths of a
# luminance costs about a point of contrast and removes the hard edge.
#
# It is also what makes the second grounds work. `line` sits 0.006 above the
# ground; against a ground of exactly zero there is nothing below it to pull
# from, and the whole ladder is squeezed into the bottom of the range.
MIN_GROUND_LUMINANCE = 0.0015
MAX_GROUND_LUMINANCE = 0.0120

# A theme ships more than one ground. A diff row, the current line, a panel and
# a selection are all the ground with a little of one slot pulled into it, and
# every one of them has text on top: delta paints full syntax onto a diff row,
# so checking body text alone is not enough.
#
# They are named by how far they sit *above the ground* rather than by mix
# weight, because the mix happens in linear light and the slots do not start from
# the same place. A 0.18 blend toward this palette's near-white `green` lands at
# luminance 0.161 - an added line brighter than most themes' body text, with body
# text at 3.7:1 on top of it - while the same 0.18 toward `red` lands at 0.041.
# One lift for every surface means a plus row and a minus row sit the same
# distance off the ground and only the hue tells them apart, which is the whole
# point of a diff.
#
# A lift, not an absolute luminance. These were absolute while the ground was
# #000000, where the two are the same number and the difference never showed.
# The moment the ground lifts off zero they stop being the same: `line` at an
# absolute 0.006 sits 0.003 above a lifted ground instead of 0.006, and the
# current line quietly halves. What the surface means is "this far off whatever
# the ground is", so that is what it stores.
SURFACE_LIFT: dict[str, float] = {
    "line": 0.006,       # the line the cursor is on; must not read as highlighted
    "panel": 0.010,      # sidebars, completion menus, toolbars
    "plus": 0.014,       # an added line
    "minus": 0.014,      # a removed line
    "change": 0.014,     # a changed line
    "selection": 0.022,  # selected text, and the row a picker is on
    "plus_emph": 0.022,  # the changed run inside an added line
    "minus_emph": 0.022,
    "change_emph": 0.022,
    # A markdown heading bar is a ground like any other, and it has the heading
    # sitting on it. Only the top two levels get one: below that the colour
    # ladder carries the level on its own, and a bar on every line is noise.
    "heading1": 0.022,
    "heading2": 0.013,
}

# What the slot is pulled from. `bright_white` is the neutral: a selection, a
# current line and a heading bar should not pick a side.
#
# The added row is pulled from `bright_green` rather than from `green`, because
# `green` is the slot `string` occupies and a palette is free to spend it on a
# near-white - a docstring that reads as prose is a legitimate choice. When it
# does, an added row pulled from that slot lands neutral and a diff loses the
# one thing it has to get right. `bright_green` carries `escape`, which is green
# in every palette this contract admits, so a plus row is green whatever slot 2
# is spent on.
SURFACE_SLOT: dict[str, str] = {
    "line": "bright_white",
    "panel": "green",
    "plus": "bright_green",
    "minus": "red",
    "change": "yellow",
    "selection": "green",
    "plus_emph": "bright_green",
    "minus_emph": "red",
    "change_emph": "yellow",
    "heading1": "bright_white",
    "heading2": "bright_white",
}

# Body text has to clear the same 9:1 it clears against the ground. The other
# roles drop to 3:1: a surface is where you read one line, not a whole file, and
# holding every role to 4.5:1 leaves a diff background too faint to see.
SURFACE_ROLE_FLOOR = 3.0

# The gutter: line numbers, listchars, indent guides. Every glyph that is not
# content and not a comment.
#
# This was the one foreground the renderers mixed by hand, and it drifted into
# exactly the collision the contract exists to catch: at a 0.22 blend it landed
# on #7a7e7b, 0.036 from `comment` at #7e8a7b. A line number the same colour as
# a comment is two kinds of information wearing one colour, and nothing measured
# it because the mix happened in render.py rather than here.
#
# Stored as a lift for the same reason the surfaces are: what it means is "this
# far off whatever the ground is", and pulling from `bright_white` keeps it
# neutral so it does not read as a dim comment of its own.
GUTTER_LIFT = 0.130
GUTTER_SLOT = "bright_white"

# The chrome accent quartet. A status bar labels four kinds of thing - a key to
# press, a count, a name, an overflow - and hands them to whatever the tool
# calls emphasis_0..3. They therefore need the same separation as two syntax
# roles sitting side by side, which the first quartet did not have: `type`,
# `escape` and `property` are all cool, and escape/property measured 0.175 while
# type/escape measured 0.127 and type/property 0.119. Two of the four accents
# were the same teal, so a bar that looked like it carried four kinds of
# information carried three.
#
# The green is last because that is the index a status bar spends on the key you
# actually press. Zellij's bottom bar reads emphasis_3 for `Ctrl g`, and before
# this the bar had no green anywhere in base mode: `ribbon_selected` is the only
# green entry and it never appears there.
EMPHASIS: tuple[str, ...] = ("number", "type", "builtin", "variable")

# What a tool means by "added", "ok", "modified" or "deleted".
#
# A palette is free to spend slot 2 on a near-white `string`, and this one does -
# a docstring that reads as prose is the point. The cost is that every consumer
# asking for "green" gets a white, and the ones that mean *added* or *ok* by it
# get a white too. The README states the fix, and four of this repo's own
# renderers still got it wrong: the Neovim `Added` group, opencode's `success`
# and `diffAdded`, and ptpython's `generic.inserted` all painted an added line
# in a chroma-0.003 white while the removed line stayed red. A diff whose plus
# row has no hue has lost the one thing it has to get right.
#
# Naming it here means a renderer asks for the meaning and cannot reach the
# wrong slot by remembering the rule wrongly.
SEMANTIC: dict[str, str] = {
    "added": "escape",     # green in any palette this contract admits
    "ok": "function",      # the green that is not the body colour
    "modified": "number",
    "deleted": "error",
}

# The six markdown heading levels.
#
# Markdown is the one filetype where the palette is the whole interface, and six
# levels need six colours rather than six weights of one. Which six is a
# contract question, not a render detail: the first ladder put `property` at
# level five, 0.119 from the `type` at level two and 0.121 from the
# `punctuation` at level six, and both went unmeasured because the ladder lived
# in render.py.
#
# Adjacent levels hold BASE_SEPARATION and every pair holds the floor, and
# prominence never rises as the level descends. `comment`, `warning` and `error`
# are not admissible: a heading must not borrow a recessive or a signal role.
HEADING_LADDER: tuple[str, ...] = (
    "variable",   # body green, with a bar
    "constant",   # amber, with a bar
    "type",       # cyan
    "number",     # orange
    "keyword",    # violet
    "function",   # the darker green
)

# `punctuation` is deliberately not in the ladder. Chalk carries the bullets,
# the quote bars and the table rules in the same buffer, so a level-six heading
# painted chalk was indistinguishable from a table row - and it collided with
# both of its neighbours besides, at 0.119 from `type` and 0.121 from itself one
# level down.

# Bold is the one axis that costs no colour, and FiraCode ships a real Bold
# face while shipping no italic at all - so bold carries what hue cannot.
# Applied to the roles you scan for rather than read through.
BOLD_ROLES: frozenset[str] = frozenset({"function", "keyword", "error"})

# Hue windows that still read as a phosphor tube.
#
# Green carries the body and the code you wrote. Three cool tiers carry what the
# language knows, and each is usable only where sRGB still has chroma for it:
#
#   teal   172-195   the only cool hue with chroma left above L 0.85
#   cyan   195-215   thinnest of the three; fine mid-ladder
#   ice    214-240   richer than cyan at L 0.70, gone by L 0.85
#
# Amber holds the literals, red and orange the signals, and one violet holds
# `keyword` alone. Violet is the exception that earned itself: with keyword,
# type and variable all green, the keyword sat 0.126 from the nearer of the
# other two and the three were routinely misread. Moving it out of green took
# that to 0.430 - a larger gain than any other single change measured.
#
# What was tried and rejected:
#   lime (108-136)      sour, and it drags the whole palette yellow
#   amber on keywords   makes `def` and `if` look like warnings
#   copper as an accent the warm side is already spent: error, warning and the
#                       two literals occupy 16-95, leaving room for two roles
#   violet on more than `keyword`  stops reading as a green theme
#
# Bone-white is admissible as a *lightness* move rather than a hue: the
# delimiters and the comment are neutrals, and carry no hue at all.
GREEN = (137.0, 170.0)
TEAL = (172.0, 195.0)
CYAN = (195.0, 215.0)
ICE = (214.0, 240.0)
VIOLET = (300.0, 322.0)
AMBER = (68.0, 95.0)
RED = (16.0, 34.0)
ORANGE = (34.0, 50.0)

ANSI: list[str] = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
]


def required_separation(a: str, b: str) -> float:
    """Distance this pair of roles must keep. Never below the floor."""
    weight = PAIR_WEIGHT.get((a, b)) or PAIR_WEIGHT.get((b, a))
    return max(SEPARATION_FLOOR, BASE_SEPARATION * weight if weight else 0.0)


class PaletteError(Exception):
    """A palette that would ship an unreadable terminal."""


# --------------------------------------------------------------- colour maths


def _channels(colour: str, where: str = "colour") -> tuple[float, float, float]:
    text = colour.strip()
    if not (text.startswith("#") and len(text) == 7):
        raise PaletteError(f"{where}: {colour!r} is not a #rrggbb hex colour")
    try:
        return tuple(int(text[i : i + 2], 16) / 255 for i in (1, 3, 5))
    except ValueError as exc:
        raise PaletteError(f"{where}: {colour!r} is not a #rrggbb hex colour") from exc


def _to_linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def _from_linear(channel: float) -> float:
    c = min(1.0, max(0.0, channel))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(colour: str) -> float:
    """Relative luminance per WCAG, which uses a slightly different cutoff."""
    r, g, b = (
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        for c in _channels(colour, "luminance")
    )
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    """WCAG 2.1 contrast ratio, 1.0 to 21.0."""
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def oklab(colour: str) -> tuple[float, float, float]:
    r, g, b = (_to_linear(c) for c in _channels(colour, "oklab"))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )


def separation(a: str, b: str) -> float:
    """Perceptual distance in OKLab, uniform enough to compare small text."""
    return math.dist(oklab(a), oklab(b))


def hue(colour: str) -> float:
    _, A, B = oklab(colour)
    return math.degrees(math.atan2(B, A)) % 360


def chroma(colour: str) -> float:
    _, A, B = oklab(colour)
    return math.hypot(A, B)


def lightness(colour: str) -> float:
    return oklab(colour)[0]


def is_green(colour: str) -> bool:
    """Does this read as green to a viewer?

    The lower bound is 118, not 70: amber sits near hue 78, and a band that
    started at 70 counted every amber slot as green and overstated green share
    by a sixth. Chartreuse at 120 is the warmest hue that still reads green.
    """
    return 118.0 <= hue(colour) <= 178.0 and chroma(colour) >= 0.04


def oklch_to_linear(L: float, C: float, h: float) -> tuple[float, float, float]:
    a = C * math.cos(math.radians(h))
    b = C * math.sin(math.radians(h))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def in_gamut(L: float, C: float, h: float) -> bool:
    return all(-0.0015 <= c <= 1.0015 for c in oklch_to_linear(L, C, h))


_CEILING: dict[tuple[int, int], float] = {}


def max_chroma(L: float, h: float) -> float:
    """The most chroma sRGB has at this lightness and hue.

    What "saturated" means depends entirely on where you are standing: this is
    0.268 at hue 145 and 0.144 at hue 205, which is why the contract measures a
    fraction of it rather than an absolute.
    """
    key = (round(L * 200), round(h) % 360)
    if key not in _CEILING:
        lo, hi = 0.0, 0.40
        for _ in range(18):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if in_gamut(L, mid, h) else (lo, mid)
        _CEILING[key] = lo
    return _CEILING[key]


def saturation(colour: str) -> float:
    """Chroma as a fraction of what this hue and lightness allow."""
    ceiling = max_chroma(lightness(colour), hue(colour))
    return chroma(colour) / ceiling if ceiling else 0.0


def oklch_hex(L: float, C: float, h: float) -> str:
    r, g, b = (round(_from_linear(c) * 255) for c in oklch_to_linear(L, C, h))
    return f"#{r:02x}{g:02x}{b:02x}"


def lab_point(L: float, C: float, h: float) -> tuple[float, float, float]:
    return (L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h)))


def lab_distance(p: tuple[float, float, float], q: tuple[float, float, float]) -> float:
    return math.dist(lab_point(*p), lab_point(*q))


def mix(a: str, b: str, weight: float) -> str:
    """Blend towards b in linear light, so dark diff grounds stay neutral."""
    ca, cb = _channels(a, "mix"), _channels(b, "mix")
    out = [
        round(_from_linear(_to_linear(x) * (1 - weight) + _to_linear(y) * weight) * 255)
        for x, y in zip(ca, cb, strict=True)
    ]
    return "#{:02x}{:02x}{:02x}".format(*out)


def surface(palette: Palette, name: str) -> str:
    """The named second ground, solved for its lift above the ground.

    mix() blends in linear light and luminance is linear in those channels, so
    the weight that lands a surface exactly SURFACE_LIFT[name] above the ground
    is computed rather than searched.
    """
    ground = luminance(palette.ground)
    slot = luminance(palette.ansi[SURFACE_SLOT[name]])
    weight = SURFACE_LIFT[name] / (slot - ground)
    return mix(palette.ground, palette.ansi[SURFACE_SLOT[name]], weight)


def recede(colour: str, ground: str, target: float) -> str:
    """Pull `colour` toward `ground` until it sits at exactly `target` contrast.

    A second tier of the same meaning - a staged hunk against an unstaged one -
    needs to keep its hue and lose its urgency, and the amount to lose is a
    contrast, not a blend weight. gitsigns makes exactly this mistake: it dims
    the three sign colours by a flat 30% to derive its staged tier, which landed
    staged-delete at 1.9:1 and staged-change at 2.4:1, under the floor every
    other role in this palette has to clear. Same glyph, same column, invisible.

    Solved rather than searched, because contrast is monotonic in the blend:
    luminance is linear in the channels mix() interpolates.
    """
    lo, hi = luminance(ground), luminance(colour)
    want = target * (lo + 0.05) - 0.05
    if not lo < want < hi:
        return colour
    return mix(ground, colour, (want - lo) / (hi - lo))


# What a second tier of the same meaning is held to.
#
# The number is decided by `deleted`, which is the tightest of the three: `error`
# already sits at 5.30:1, so there is very little room between it and the floor,
# and a target of 4.0 leaves its receded tier only 0.076 away - under the
# separation floor, which is to say invisible as a distinction. At 3.5 the three
# tiers sit 0.399, 0.201 and 0.110 from their first tiers and all still clear the
# 3:1 a surface gives a role.
RECEDED_CONTRAST = 3.5


def gutter(palette: Palette) -> str:
    """The non-content foreground: line numbers, listchars, indent guides.

    Solved for its lift like a surface, and audited like a role, because it is
    read against the ground and has to stay clear of `comment`.
    """
    ground = luminance(palette.ground)
    slot = luminance(palette.ansi[GUTTER_SLOT])
    return mix(palette.ground, palette.ansi[GUTTER_SLOT], GUTTER_LIFT / (slot - ground))


# ------------------------------------------------------------------- the object


@dataclass(frozen=True, slots=True)
class Palette:
    name: str
    description: str
    ground: str
    text: str
    cursor: str
    ansi: dict[str, str]
    source: Path

    @property
    def slug(self) -> str:
        return self.source.stem

    def slot(self, index: int) -> str:
        return self.ansi[ANSI[index]]

    def role(self, name: str) -> str:
        """The colour this syntax role is painted with."""
        slot = SLOT_OF[name]
        return self.text if slot == "text" else self.ansi[slot]

    def surface(self, name: str) -> str:
        """A second ground: a diff row, a panel, the current line, a selection."""
        return surface(self, name)

    @property
    def gutter(self) -> str:
        """Line numbers, listchars, indent guides: present but not content."""
        return gutter(self)

    def semantic(self, meaning: str) -> str:
        """The colour for `added`, `ok`, `modified` or `deleted`.

        Always this rather than a slot by name: slot 2 is a legitimate place for
        a near-white `string`, and reaching for it because it is called "green"
        is how four renderers came to paint an added line without hue.
        """
        return self.role(SEMANTIC[meaning])

    @property
    def emphasis(self) -> tuple[str, ...]:
        """The chrome accent quartet, in the order tools index it."""
        return tuple(self.role(role) for role in EMPHASIS)

    @property
    def headings(self) -> tuple[str, ...]:
        """The six markdown heading colours, level one first."""
        return tuple(self.role(role) for role in HEADING_LADDER)


def load(path: Path) -> Palette:
    raw = yaml.safe_load(path.read_text())
    missing = {"name", "ground", "text", "cursor", "ansi"} - raw.keys()
    if missing:
        raise PaletteError(f"{path.name}: missing {', '.join(sorted(missing))}")
    absent = [key for key in ANSI if key not in raw["ansi"]]
    if absent:
        raise PaletteError(f"{path.name}: ansi is missing {', '.join(absent)}")
    for key in ("ground", "text", "cursor"):
        _channels(raw[key], f"{path.name}:{key}")
    for key, value in raw["ansi"].items():
        _channels(value, f"{path.name}:ansi.{key}")
    return Palette(
        name=raw["name"],
        description=(raw.get("description") or "").strip(),
        ground=raw["ground"],
        text=raw["text"],
        cursor=raw["cursor"],
        ansi=dict(raw["ansi"]),
        source=path,
    )


def audit(palette: Palette) -> list[str]:
    """Every way this palette would be hard to read. Empty means it ships."""
    problems: list[str] = []

    ground = luminance(palette.ground)
    if ground < MIN_GROUND_LUMINANCE:
        problems.append(
            f"ground {palette.ground} has luminance {ground:.4f}, want at least "
            f"{MIN_GROUND_LUMINANCE} — a saturated body on a zero ground halates, and the "
            f"second grounds have nothing to sit above"
        )
    elif ground > MAX_GROUND_LUMINANCE:
        problems.append(
            f"ground {palette.ground} has luminance {ground:.4f}, want at most "
            f"{MAX_GROUND_LUMINANCE} — it stops reading as a phosphor tube"
        )

    for role, (floor, ceiling) in CONTRAST_BOUNDS.items():
        colour = palette.role(role)
        slot = SLOT_OF[role]
        best = contrast(colour, palette.ground)
        if best < floor:
            problems.append(
                f"{role} ({slot}) peaks at {best:.1f}:1 against the ground, want {floor}"
            )
        elif best > ceiling:
            problems.append(
                f"{role} ({slot}) is {best:.1f}:1 against the ground, want at most "
                f"{ceiling} so it stays recessive"
            )

    # Unconditional: a body text so pale that is_green() rejects it is exactly
    # the failure this check exists to catch, so it must not gate on that.
    body = palette.text
    if chroma(body) < MIN_BODY_CHROMA:
        problems.append(
            f"body text {body} has chroma {chroma(body):.3f}, want {MIN_BODY_CHROMA} — "
            f"it reads as white with a green note rather than as neon green"
        )

    for role in ROLES:
        if role in CHROMA_EXEMPT:
            continue
        colour = palette.role(role)
        want = max(CHROMA_FLOOR, MIN_SATURATION * max_chroma(lightness(colour), hue(colour)))
        if chroma(colour) < want:
            problems.append(
                f"{role} has chroma {chroma(colour):.3f}, which is {saturation(colour):.0%} of "
                f"what hue {hue(colour):.0f} allows — want {MIN_SATURATION:.0%}, or it reads pastel"
            )

    # The grounds that are not the ground. Unchecked, these are where a palette
    # that passes everything above still ships an unreadable added line.
    body_floor = CONTRAST_BOUNDS["variable"][0]
    for name in SURFACE_LIFT:
        ground = surface(palette, name)
        got = contrast(palette.text, ground)
        if got < body_floor:
            problems.append(
                f"body text is {got:.1f}:1 on the {name} surface {ground}, want {body_floor}"
            )
        for role in ROLES:
            got = contrast(palette.role(role), ground)
            if got < SURFACE_ROLE_FLOOR:
                problems.append(
                    f"{role} is {got:.1f}:1 on the {name} surface {ground}, "
                    f"want {SURFACE_ROLE_FLOOR}"
                )

    # Every pair, not only the ones PAIR_WEIGHT happens to name.
    for a, b in itertools.combinations(ROLES, 2):
        want = required_separation(a, b)
        got = separation(palette.role(a), palette.role(b))
        if got < want:
            problems.append(
                f"{a} and {b} are {got:.3f} apart, want {want:.3f} "
                f"(they sit side by side often)"
            )

    # The gutter is read against the ground like a role, and it is the one
    # foreground a renderer used to mix by hand - which is how it ended up
    # 0.036 from `comment`.
    edge = gutter(palette)
    got = contrast(edge, palette.ground)
    if got < SURFACE_ROLE_FLOOR:
        problems.append(
            f"the gutter {edge} is {got:.1f}:1 against the ground, want "
            f"{SURFACE_ROLE_FLOOR} — a line number you cannot read is not dim, it is gone"
        )
    got = separation(edge, palette.role("comment"))
    if got < SEPARATION_FLOOR:
        problems.append(
            f"the gutter {edge} is {got:.3f} from comment, want {SEPARATION_FLOOR} — "
            f"a line number the same colour as a comment is two meanings in one colour"
        )

    # A receded tier has to stay readable and stay distinguishable from the tier
    # it recedes from, or it is not a tier.
    for meaning in SEMANTIC:
        first = palette.semantic(meaning)
        second = recede(first, palette.ground, RECEDED_CONTRAST)
        got = contrast(second, palette.ground)
        if got < SURFACE_ROLE_FLOOR:
            problems.append(
                f"the receded {meaning} {second} is {got:.1f}:1 against the ground, "
                f"want {SURFACE_ROLE_FLOOR}"
            )
        got = separation(first, second)
        if got < SEPARATION_FLOOR:
            problems.append(
                f"{meaning} and its receded tier are {got:.3f} apart, want "
                f"{SEPARATION_FLOOR} — lower RECEDED_CONTRAST or the two tiers are one"
            )

    # The chrome accents and the heading ladder are sets of colours that appear
    # together, so they are held to the same distances as adjacent syntax roles.
    for a, b in itertools.combinations(EMPHASIS, 2):
        got = separation(palette.role(a), palette.role(b))
        if got < BASE_SEPARATION:
            problems.append(
                f"emphasis accents {a} and {b} are {got:.3f} apart, want "
                f"{BASE_SEPARATION} — a status bar shows all four at once"
            )

    for level, (a, b) in enumerate(itertools.pairwise(HEADING_LADDER), start=1):
        got = separation(palette.role(a), palette.role(b))
        if got < BASE_SEPARATION:
            problems.append(
                f"heading {level} ({a}) and {level + 1} ({b}) are {got:.3f} apart, "
                f"want {BASE_SEPARATION} — consecutive levels nest"
            )
        if lightness(palette.role(b)) > lightness(palette.role(a)) + 0.005:
            problems.append(
                f"heading {level + 1} ({b}) is lighter than heading {level} ({a}) — "
                f"prominence has to fall as the level descends"
            )
    for a, b in itertools.combinations(HEADING_LADDER, 2):
        got = separation(palette.role(a), palette.role(b))
        if got < SEPARATION_FLOOR:
            problems.append(
                f"headings {a} and {b} are {got:.3f} apart, want {SEPARATION_FLOOR}"
            )

    return problems


def hue_families(palette: Palette) -> int:
    """How many distinct hue clusters the palette spends. Neutrals do not count."""
    hues = sorted(hue(palette.role(r)) for r in ROLES if chroma(palette.role(r)) >= 0.045)
    return 1 + sum(1 for a, b in zip(hues, hues[1:], strict=False) if b - a > 18.0)


def measure(palette: Palette) -> dict[str, object]:
    """The numbers worth reporting for a palette that passed."""
    chromatic = [
        palette.ansi[key]
        for key in ("red", "green", "yellow", "blue", "magenta", "cyan")
        + ("bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan")
    ]
    scored = [
        (a, b, separation(palette.role(a), palette.role(b)) - required_separation(a, b))
        for a, b in itertools.combinations(ROLES, 2)
    ]
    a, b, slack = min(scored, key=lambda row: row[2])
    return {
        "green_share": round(sum(1 for c in chromatic if is_green(c)) / len(chromatic) * 100),
        "text_contrast": round(contrast(palette.text, palette.ground), 1),
        "accent_floor": round(min(
            max(contrast(palette.ansi[k], palette.ground),
                contrast(palette.ansi[f"bright_{k}"], palette.ground))
            for k in ("red", "green", "yellow", "blue", "magenta", "cyan")
        ), 1),
        "neon": round(chroma(palette.text), 3),
        "min_saturation": round(min(
            saturation(palette.role(r)) for r in ROLES if r not in CHROMA_EXEMPT
        ), 2),
        "hue_families": hue_families(palette),
        "min_separation": round(min(
            separation(palette.role(x), palette.role(y))
            for x, y in itertools.combinations(ROLES, 2)
        ), 3),
        "tightest_pair": f"{a}/{b}",
        "slack": round(slack, 3),
    }
