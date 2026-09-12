"""The palette contract, shared by render.py and explore.py.

Colour maths plus the one definition of what makes a phosphor palette readable.
Both scripts import this so they cannot drift apart: explore.py designs against
these thresholds and render.py refuses to ship anything that misses them.

Readability here is two independent things, and a green theme needs both checked:

  contrast    can the colour be seen against the ground (WCAG 2.1)
  separation  can two colours that mean different things be told apart (OKLab)

The second is the one a conventional theme gets for free and a green theme does
not. When five of eight roles share a hue, contrast alone will happily approve a
palette in which strings, functions and body text are one indistinguishable wash.
Separation is required per pair and weighted by how often the two roles actually
sit next to each other, because a flat threshold over-constrains the rare pairs
and under-constrains the ones you read on every line.
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
# roles in their own right, the same sixteen slots carry fourteen meanings.
SLOT_OF: dict[str, str] = {
    # primary: the eight every tool paints
    "variable": "text",
    "error": "red",               # 1
    "string": "green",            # 2
    "number": "yellow",           # 3
    "function": "blue",           # 4
    "keyword": "magenta",         # 5
    "type": "cyan",               # 6
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

# A secondary role is a relative of its primary, so it may sit closer - that
# kinship is information, not a defect. It still may never be identical.
KIN: dict[str, str] = {
    "warning": "error",
    "escape": "string",
    "constant": "number",
    "parameter": "variable",
    "builtin": "keyword",
    "property": "type",
}

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
}
PAIRS: list[tuple[str, str]] = list(PAIR_WEIGHT)
BASE_SEPARATION = 0.130

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
# Two roles are exempt, for reasons of physics rather than taste: `string` sits
# near L 0.95 where the sRGB green gamut simply has no chroma left, and
# `comment` is deliberately dark and recessive.
MIN_ROLE_CHROMA = 0.14
CHROMA_EXEMPT: frozenset[str] = frozenset({"string", "comment"})

# Contrast bounds against the ground. Comments are capped as well as floored: a
# "dim" colour as bright as body text is not dim.
CONTRAST_BOUNDS: dict[str, tuple[float, float]] = {
    "variable": (9.0, 21.0),
    "error": (5.0, 21.0),
    "string": (5.0, 21.0),
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
}

# Bold is the one axis that costs no colour, and FiraCode ships a real Bold
# face while shipping no italic at all - so bold carries what hue cannot.
# Applied to the roles you scan for rather than read through.
BOLD_ROLES: frozenset[str] = frozenset({"function", "keyword", "error"})

# Hue windows that still read as a phosphor tube.
#
# The admissible set is narrow and was settled by trying the alternatives:
#   lime (108-132)   sour, and it drags the whole palette yellow
#   jade (172-196)   reads as teal and breaks the immersion
#   copper (40-62)   too close to amber to earn a slot of its own
#   amber on keywords   makes `def` and `if` look like warnings
#   cool blue        anachronistic beside green; a CRT never came in it
#
# What survives: green carries every syntax role, red is reserved for errors,
# and amber appears only on numbers. Bone-white is admissible as a *lightness*
# move rather than a hue - a green so pale it reads white.
# Floor raised from 136: at the chroma a matrix body text needs, hue 138
# renders as #6fff1a - visibly the lime that was already rejected.
GREEN = (141.0, 168.0)
AMBER = (68.0, 95.0)
RED = (16.0, 34.0)

ANSI: list[str] = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
]


def required_separation(a: str, b: str) -> float:
    """Distance this pair of roles must keep. 0.0 if they never collide."""
    weight = PAIR_WEIGHT.get((a, b)) or PAIR_WEIGHT.get((b, a))
    return BASE_SEPARATION * weight if weight else 0.0


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
    # A reference palette is kept for comparison and expected to fail the audit.
    # It is reported and skipped, and never fails a run.
    reference: bool = False

    @property
    def slug(self) -> str:
        return self.source.stem

    def slot(self, index: int) -> str:
        return self.ansi[ANSI[index]]

    def role(self, name: str) -> str:
        """The colour this syntax role is painted with."""
        slot = SLOT_OF[name]
        return self.text if slot == "text" else self.ansi[slot]


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
        reference=bool(raw.get("reference", False)),
    )


def audit(palette: Palette) -> list[str]:
    """Every way this palette would be hard to read. Empty means it ships."""
    problems: list[str] = []

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
        if role in CHROMA_EXEMPT or role == "variable":
            continue
        got = chroma(palette.role(role))
        if got < MIN_ROLE_CHROMA:
            problems.append(
                f"{role} has chroma {got:.3f}, want {MIN_ROLE_CHROMA} — it reads pastel, "
                f"which is what separating by chroma instead of lightness costs"
            )

    for a, b in itertools.combinations(ROLES, 2):
        want = required_separation(a, b)
        if not want:
            continue
        got = separation(palette.role(a), palette.role(b))
        if got < want:
            problems.append(
                f"{a} and {b} are {got:.3f} apart, want {want:.3f} "
                f"(they sit side by side often)"
            )

    return problems


def measure(palette: Palette) -> dict[str, object]:
    """The numbers worth reporting for a palette that passed."""
    chromatic = [
        palette.ansi[key]
        for key in ("red", "green", "yellow", "blue", "magenta", "cyan")
        + ("bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan")
    ]
    scored = [
        (a, b, separation(palette.role(a), palette.role(b)) - required_separation(a, b))
        for a, b in PAIRS
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
        "pastel_roles": sum(
            1 for r in ROLES
            if r not in CHROMA_EXEMPT and chroma(palette.role(r)) < MIN_ROLE_CHROMA
        ),
        "min_chroma": round(min(
            chroma(palette.role(r)) for r in ROLES if r not in CHROMA_EXEMPT
        ), 3),
        "green_chroma": round(
            sum(chroma(palette.role(r)) for r in ROLES if is_green(palette.role(r)))
            / max(1, sum(1 for r in ROLES if is_green(palette.role(r)))), 3
        ),
        "min_separation": round(min(
            separation(palette.role(x), palette.role(y)) for x, y in PAIRS
        ), 3),
        "tightest_pair": f"{a}/{b}",
        "slack": round(slack, 3),
    }
