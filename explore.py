#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml>=6.0.2"]
# ///
"""Explore variants of the Rain Split contract and write them to palettes/.

The Split contract, which is the part worth keeping: default text is a pale
green-white so prose recedes, and the saturated greens are spent only on syntax.

Rain Split's own ladder is the anchor every variant is measured against:

    comment 0.47 -> function 0.64 -> type 0.82 -> string 0.86 -> keyword 0.91
    -> text 0.97, with amber number at 0.83 and red error at 0.69

What this optimises is the thing a contrast check cannot see - which hue and
which rung carries which syntax role. Thresholds come from palette.py, so a
variant designed here is measured by exactly what render.py will refuse to ship.

The admissible hues are green, red for errors and amber for numbers; see
palette.py for what was tried and rejected.

    uv run explore.py            # write every policy to palettes/
    uv run explore.py --dry-run  # report only
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path

from palette import (
    AMBER,
    chroma as chroma_of,
    CHROMA_EXEMPT,
    ANSI,
    CONTRAST_BOUNDS,
    GREEN,
    PAIRS,
    RED,
    ROLES,
    SLOT_OF,
    chroma,
    contrast,
    hue,
    in_gamut,
    is_green,
    MIN_ROLE_CHROMA,
    oklch_hex,
    required_separation,
    separation,
)

ROOT = Path(__file__).parent
PALETTES = ROOT / "palettes"

# render.py measures the rounded hex, so this must too - optimising on the
# continuous OKLCh value silently passes variants that then fail the audit.
# The margin keeps a later rounding from flipping a pass into a failure.
SAFETY_MARGIN = 0.005

# The lightness the ladder is stretched around when a policy changes its spread.
LADDER_CENTRE = 0.78


def hex_separation(a: list[float], b: list[float]) -> float:
    return separation(oklch_hex(*a), oklch_hex(*b))


@dataclass(frozen=True, slots=True)
class Role:
    """The box in OKLCh that one syntax role is allowed to live in."""

    hue: tuple[float, float]
    L: tuple[float, float]
    C: tuple[float, float]


@dataclass(frozen=True, slots=True)
class Policy:
    slug: str
    name: str
    family: str
    idea: str
    ground: str
    roles: dict[str, Role]
    seed: int = 1


# Bands anchored on the film's own four-stop ramp, not on Rain Split's:
#
#   deep trail  #003b00  L 0.305  C 0.104   -> comment
#   mid trail   #008f11  L 0.564  C 0.187   -> function
#   body        #00ff41  L 0.869  C 0.278   -> variable, the neon default text
#   leading     #ccffcc  L 0.952  C 0.086   -> string, the bright head of the rain
#
# The pale near-white is kept, but spent on one accent role instead of on
# everything you read. That single move is the difference between a theme that
# measures as matrix and one that measures as white with a green note.
# Fourteen roles, laid out so the two axes do different work: lightness carries
# the ramp from dead code up to the live line, and chroma separates a role from
# its own relative at the same height. A parameter is a dimmer green at nearly
# the height of a local; a builtin is a dimmer green beside a keyword. That
# kinship is the semantics - related things look related without merging.
BASE_BANDS: dict[str, tuple[float, float, float, float]] = {
    # Ten greens spread over the full lightness range at high chroma. The solver
    # is free to place them anywhere in the green window, and with chroma pinned
    # near the top of the gamut, hue is the only slack it has left - so the roles
    # fan out across the window instead of washing out towards grey.
    "comment":   (0.40, 0.52, 0.080, 0.150),
    "function":  (0.54, 0.66, 0.180, 0.270),
    "parameter": (0.60, 0.72, 0.150, 0.230),
    "builtin":   (0.66, 0.77, 0.150, 0.230),
    "type":      (0.70, 0.81, 0.190, 0.280),
    "keyword":   (0.76, 0.87, 0.150, 0.240),
    "property":  (0.79, 0.89, 0.140, 0.220),
    "variable":  (0.85, 0.93, 0.220, 0.300),
    "escape":    (0.88, 0.95, 0.140, 0.220),
    "string":    (0.93, 0.975, 0.035, 0.095),
    # amber pair, as saturated as the gamut allows at each height
    "number":    (0.72, 0.82, 0.145, 0.200),
    "constant":  (0.84, 0.92, 0.140, 0.190),
    # red pair; warning runs warmer so it can stay saturated higher up
    "error":     (0.58, 0.70, 0.190, 0.265),
    "warning":   (0.71, 0.81, 0.150, 0.215),
}

WARNING_HUE = (28.0, 48.0)


def contract(
    *,
    green: tuple[float, float] = GREEN,
    number_hue: tuple[float, float] = AMBER,
    red_hue: tuple[float, float] = RED,
    chroma_scale: float = 1.0,
    spread: float = 1.0,
    bands: dict[str, tuple[float, float, float, float]] | None = None,
    role_hues: dict[str, tuple[float, float]] | None = None,
    text_neutral: bool = False,
) -> dict[str, Role]:
    """Build the role boxes for one variant of the Split contract.

    `spread` stretches the lightness ladder around its centre, so a variant can
    separate its rungs more or less aggressively without re-stating every band.
    """
    merged = BASE_BANDS | (bands or {})
    roles: dict[str, Role] = {}
    for role, (lo, hi, c_lo, c_hi) in merged.items():
        lo = LADDER_CENTRE + (lo - LADDER_CENTRE) * spread
        hi = LADDER_CENTRE + (hi - LADDER_CENTRE) * spread
        window = green
        if role in ("number", "constant"):
            window = number_hue
        elif role == "error":
            window = red_hue
        elif role == "warning":
            window = WARNING_HUE
        elif role == "variable" and text_neutral:
            window = (0.0, 360.0)
        if role_hues and role in role_hues:
            window = role_hues[role]
        roles[role] = Role(
            window,
            (min(0.975, max(0.30, lo)), min(0.975, max(0.32, hi))),
            (c_lo * chroma_scale, c_hi * chroma_scale),
        )
    return roles


DEFAULT = "default"

# Fmind is what shipped. It came from a shortlist that changed one thing at a
# time from a baseline called Prime; the three changes that were kept are the
# ones encoded below. The rejected candidates are recorded in the README rather
# than kept as code, since re-solving them would not reproduce their hexes
# anyway - the palettes under palettes/ are the source of truth, not this file.
LANES = {
    "variable": (141.0, 148.0), "string": (141.0, 149.0),
    "function": (141.0, 148.0), "keyword": (142.0, 149.0),
    "type": (142.0, 149.0), "comment": (141.0, 150.0),
    "parameter": (159.0, 168.0), "property": (159.0, 168.0),
    "builtin": (159.0, 168.0), "escape": (158.0, 167.0),
}
SIGNAL_REDS = {
    "error": (0.58, 0.68, 0.225, 0.280),
    "warning": (0.68, 0.78, 0.185, 0.245),
}

POLICIES = [
    Policy(
        "fmind", "Fmind", DEFAULT,
        "The default. Pure black ground, warm primaries with cool relatives, a hot "
        "red pair for errors and warnings, and amber kept on numbers and constants.",
        "#000000", contract(role_hues=LANES, bands=SIGNAL_REDS), seed=19,
    ),
]


def solve(policy: Policy) -> tuple[dict[str, list[float]], float]:
    """Hill-climb the roles until every pair keeps its required distance."""
    rng = random.Random(policy.seed)

    def start(role: str, box: Role) -> list[float]:
        return [
            (box.L[0] + box.L[1]) / 2,
            (box.C[0] + box.C[1]) / 2,
            (box.hue[0] + box.hue[1]) / 2,
        ]

    def cost(state: dict[str, list[float]]) -> float:
        total = 0.0
        for a, b in PAIRS:
            want = required_separation(a, b) + SAFETY_MARGIN
            deficit = want - hex_separation(state[a], state[b])
            if deficit > 0:
                total += 18 * deficit
        for role, (L, C, h) in state.items():
            box = policy.roles[role]
            for value, (lo, hi), weight in ((h, box.hue, 0.5), (L, box.L, 9.0), (C, box.C, 9.0)):
                if value < lo:
                    total += weight * (lo - value)
                if value > hi:
                    total += weight * (value - hi)
            if not in_gamut(L, C, h):
                total += 7
            if role not in CHROMA_EXEMPT and role != "variable":
                shipped = chroma_of(oklch_hex(L, C, h))
                want = MIN_ROLE_CHROMA + SAFETY_MARGIN
                if shipped < want:
                    total += 25 * (want - shipped)
            floor, ceiling = CONTRAST_BOUNDS[role]
            got = contrast(oklch_hex(L, C, h), policy.ground)
            if got < floor:
                total += 1.6 * (floor - got)
            if got > ceiling:
                total += 1.6 * (got - ceiling)
        return total

    best = {role: start(role, box) for role, box in policy.roles.items()}
    best_cost = cost(best)
    step = 0.05
    for i in range(90000):
        candidate = {k: v[:] for k, v in best.items()}
        role = rng.choice(ROLES)
        axis = rng.randrange(3)
        candidate[role][axis] += rng.uniform(-1, 1) * (step, step * 0.8, step * 50)[axis]
        candidate[role][0] = min(0.978, max(0.28, candidate[role][0]))
        candidate[role][1] = min(0.33, max(0.002, candidate[role][1]))
        c = cost(candidate)
        if c < best_cost:
            best, best_cost = candidate, c
        if i % 12000 == 11999:
            step *= 0.74
    return best, best_cost


def build(policy: Policy) -> dict:
    state, cost = solve(policy)
    role_hex = {role: oklch_hex(*values) for role, values in state.items()}

    # Every slot is a solved role. Nothing here is a lightened copy of anything.
    ansi = {
        "black": oklch_hex(0.33, 0.050, 150),
        "red": role_hex["error"],
        "green": role_hex["string"],
        "yellow": role_hex["number"],
        "blue": role_hex["function"],
        "magenta": role_hex["keyword"],
        "cyan": role_hex["type"],
        "white": oklch_hex(0.90, 0.020, 150),
        "bright_black": role_hex["comment"],
        "bright_red": role_hex["warning"],
        "bright_green": role_hex["escape"],
        "bright_yellow": role_hex["constant"],
        "bright_blue": role_hex["parameter"],
        "bright_magenta": role_hex["builtin"],
        "bright_cyan": role_hex["property"],
        "bright_white": oklch_hex(0.975, 0.010, 150),
    }

    chromatic = [ansi[k] for k in ANSI if k not in ("black", "white", "bright_black", "bright_white")]
    scored = [
        (a, b, hex_separation(state[a], state[b]) - required_separation(a, b)) for a, b in PAIRS
    ]
    a, b, slack = min(scored, key=lambda row: row[2])

    return {
        "policy": policy,
        "text": role_hex["variable"],
        "cursor": ansi["bright_green"],
        "ansi": ansi,
        "roles": role_hex,
        "green_share": round(sum(1 for c in chromatic if is_green(c)) / len(chromatic) * 100),
        "text_contrast": round(contrast(role_hex["variable"], policy.ground), 1),
        "accent_floor": round(min(
            contrast(role_hex[r], policy.ground) for r in ROLES if r != "comment"
        ), 1),
        "neon": round(chroma(role_hex["variable"]), 3),
        "min_chroma": round(min(
            chroma(role_hex[r]) for r in ROLES if r not in CHROMA_EXEMPT
        ), 3),
        "hue_spread": round(
            max(hue(role_hex[r]) for r in ROLES if is_green(role_hex[r]))
            - min(hue(role_hex[r]) for r in ROLES if is_green(role_hex[r])), 1
        ),
        "min_separation": round(min(hex_separation(state[x], state[y]) for x, y in PAIRS), 3),
        "tightest_pair": f"{a}/{b}",
        "slack": round(slack, 3),
        "cost": round(cost, 4),
        "hues": {role: round(hue(c)) for role, c in role_hex.items()},
        "chromas": {role: round(chroma(c), 3) for role, c in role_hex.items()},
    }


def to_yaml(result: dict) -> str:
    policy = result["policy"]
    lines = [
        "# Palette source of truth. Regenerate tool files with: uv run render.py",
        "# Designed by explore.py against the contract in palette.py.",
        f'name: "{policy.name}"',
        f'family: "{policy.family}"',
        "description: >-",
        f"  {' '.join(policy.idea.split())}",
        f'ground: "{policy.ground}"',
        f'text: "{result["text"]}"',
        f'cursor: "{result["cursor"]}"',
        "ansi:",
    ]
    lines += [f'  {key}: "{result["ansi"][key]}"' for key in ANSI]
    lines += ["", "# Which syntax role each slot carries, and where it landed.", "roles:"]
    for role in ROLES:
        lines.append(
            f'  {role}: "{result["roles"][role]}"'
            f"  # {SLOT_OF[role]}, hue {result['hues'][role]}, chroma {result['chromas'][role]}"
        )
    lines += [
        "",
        "measured:",
        f'  green_share: {result["green_share"]}',
        f'  text_contrast: {result["text_contrast"]}',
        f'  accent_floor: {result["accent_floor"]}',
        f'  neon: {result["neon"]}',
        f'  min_chroma: {result["min_chroma"]}',
        f'  min_separation: {result["min_separation"]}',
        f'  tightest_pair: "{result["tightest_pair"]}"',
        f'  slack: {result["slack"]}',
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = parser.parse_args()

    results = [build(p) for p in POLICIES]

    for family in (DEFAULT,):
        rows = sorted(
            (r for r in results if r["policy"].family == family), key=lambda r: -r["slack"]
        )
        print(f"\n{family}")
        print(f"  {'variant':<14} {'neon':>5} {'minC':>5} {'hues':>5} {'green':>6} {'minSep':>7} {'slack':>7}  tightest")
        for r in rows:
            mark = " " if r["slack"] >= 0 else "!"
            print(
                f"  {mark}{r['policy'].slug:<13} {r['neon']:>5.3f} {r['min_chroma']:>5.3f} "
                f"{r['hue_spread']:>5.1f} {r['green_share']:>5}% "
                f"{r['min_separation']:>7.3f} {r['slack']:>7.3f}  {r['tightest_pair']}"
            )

    rejected = [r for r in results if r["slack"] < 0]
    if rejected:
        print("\nCould not satisfy the contract (reported, not written):")
        for r in rejected:
            print(f"  {r['policy'].slug}: {r['tightest_pair']} short by {abs(r['slack']):.3f}")

    if args.dry_run:
        return 0

    written = 0
    for r in results:
        if r["slack"] < 0:
            continue
        (PALETTES / f"{r['policy'].slug}.yaml").write_text(to_yaml(r))
        written += 1
    print(f"\nwrote {written} palettes to palettes/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
