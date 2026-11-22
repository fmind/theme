#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["fonttools>=4.60", "uharfbuzz>=0.51"]
# ///
"""Generate faithful Fmind branding wallpapers and banners."""

import argparse
import base64
import hashlib
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypedDict
from xml.sax.saxutils import escape

import uharfbuzz
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

# uharfbuzz re-exports its Cython extension symbols dynamically without type stubs.
hb: Any = uharfbuzz

ROOT = Path(__file__).resolve().parents[1]
ARTWORK = ROOT / "artworks"
PREVIEWS = ARTWORK / "previews"

BLUE = "#174ea6"
INK = "#353b4e"
WHITE = "#fdfdfd"
WIDTH, HEIGHT = 1988, 536

VARIANTS: tuple[tuple[str, int, int, float], ...] = (
    ("wallpapers/fmind-desktop-16x9", 3840, 2160, 0.80),
    ("wallpapers/fmind-laptop-16x10", 2560, 1600, 0.80),
    ("wallpapers/fmind-ultrawide-21x9", 3360, 1440, 0.74),
    ("wallpapers/fmind-tablet-3x4", 1536, 2048, 0.92),
    ("wallpapers/fmind-phone-9x20", 1440, 3200, 0.94),
    ("wallpapers/fmind-square", 2048, 2048, 0.86),
    ("banners/youtube", 2560, 1440, 0.57),
    ("banners/social-1500x500", 1500, 500, 0.76),
    ("banners/linkedin", 1584, 396, 0.73),
    ("banners/reddit", 1920, 384, 0.39),
)
LEFT_OFFSET_BANNERS = {"banners/social-1500x500", "banners/linkedin"}


class ExportRecord(TypedDict):
    file: str
    svg: str
    width: int
    height: int
    panel: list[float]
    bytes: int
    sha256: str


def run_magick(*args: str | Path, timeout: int = 60) -> None:
    """Invoke ImageMagick with closed stdin and a hard timeout."""
    subprocess.run(
        ["magick", *(str(arg) for arg in args)],
        check=True,
        stdin=subprocess.DEVNULL,
        timeout=timeout,
    )


def lettering(text: str, x: float, y: float, width: float, color: str, font: TTFont, shaping_font: Any) -> str:
    """Shape Google Sans glyphs with kerning and export exact vector outlines."""
    glyphs = font.getGlyphSet()
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(shaping_font, buffer)
    outlines = SVGPathPen(glyphs)
    bounds = BoundsPen(glyphs)
    cursor = 0
    for info, position in zip(buffer.glyph_infos, buffer.glyph_positions, strict=True):
        transform = (1, 0, 0, 1, cursor + position.x_offset, position.y_offset)
        glyph = glyphs[font.getGlyphName(info.codepoint)]
        glyph.draw(TransformPen(outlines, transform))
        glyph.draw(TransformPen(bounds, transform))
        cursor += position.x_advance
    if bounds.bounds is None:
        raise ValueError(f"No glyph bounds produced for {text!r}")
    left, _bottom, right, top = bounds.bounds
    scale = width / (right - left)
    return (
        f'<g aria-label="{escape(text)}" fill="{color}" '
        f'transform="translate({x - left * scale} {y + top * scale}) scale({scale} {-scale})">'
        f'<path d="{outlines.getCommands()}"/></g>'
    )


def composition() -> str:
    """Build the faithful panel composition using the authentic logo and Google Sans outlines."""
    font_path = ARTWORK / "GoogleSans-Bold.ttf"
    shaping_font = hb.Font(hb.Face(font_path.read_bytes()))
    logo = base64.b64encode((ARTWORK / "logo.png").read_bytes()).decode()
    with TTFont(font_path) as font:
        return (
            f'<rect x="10" y="10" width="1968" height="516" rx="48" '
            f'fill="{WHITE}" stroke="{BLUE}" stroke-width="20"/>'
            f'<image x="71" y="29" width="480" height="480" '
            f'href="data:image/png;base64,{logo}"/>'
            + lettering("fmind.dev", 615, 96, 1280, BLUE, font, shaping_font)
            + lettering("AI Agents, MLOps & Security", 625, 366, 1225, INK, font, shaping_font)
        )


def svg_document(width: int, height: int, content: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f"<title>fmind.dev — AI Agents, MLOps &amp; Security</title>{content}</svg>"
    )


def render(source: Path, target: Path) -> None:
    run_magick(
        "-background",
        WHITE,
        source,
        "-alpha",
        "remove",
        "-alpha",
        "off",
        "-strip",
        f"PNG24:{target}",
    )


def generate() -> None:
    """Generate all 10 SVG sources, export exact PNGs, and create validation previews."""
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    art = composition()
    master = ARTWORK / "composition.svg"
    master.write_text(svg_document(WIDTH, HEIGHT, art), encoding="utf-8")
    render(master, PREVIEWS / "composition.png")

    records: list[ExportRecord] = []
    for name, width, height, fraction in VARIANTS:
        panel_width = round(width * fraction)
        scale = panel_width / WIDTH
        panel_height = HEIGHT * scale
        x = width - panel_width - width * 0.035 if name in LEFT_OFFSET_BANNERS else (width - panel_width) / 2
        y = (height - panel_height) / 2

        content = f'<rect width="{width}" height="{height}" fill="{WHITE}"/>'
        content += f'<g transform="translate({x} {y}) scale({scale})">{art}</g>'

        svg_path = ROOT / f"{name}.svg"
        png_path = ROOT / f"{name}.png"
        svg_path.write_text(svg_document(width, height, content), encoding="utf-8")
        render(svg_path, png_path)

        records.append(
            {
                "file": f"{name}.png",
                "svg": f"{name}.svg",
                "width": width,
                "height": height,
                "panel": [x, y, float(panel_width), panel_height],
                "bytes": png_path.stat().st_size,
                "sha256": hashlib.sha256(png_path.read_bytes()).hexdigest(),
            }
        )

    run_magick(
        "montage",
        *(ROOT / r["file"] for r in records),
        "-font",
        ARTWORK / "GoogleSans-Bold.ttf",
        "-pointsize",
        "16",
        "-label",
        "%f",
        "-geometry",
        "460x280+12+28",
        "-background",
        "#e8e8e8",
        "-tile",
        "2x",
        "-strip",
        PREVIEWS / "all-variants.png",
    )

    run_magick(
        ARTWORK / "reference-banner.png",
        "-background",
        WHITE,
        "-alpha",
        "remove",
        "-crop",
        "1988x536+34+114",
        "+repage",
        PREVIEWS / "composition.png",
        "-append",
        "-strip",
        PREVIEWS / "reference-comparison.png",
    )

    for name, geometry in (("youtube", "1543x422+508+509"), ("reddit", "1920x227+0+78")):
        run_magick(
            ROOT / f"banners/{name}.png",
            "-crop",
            geometry,
            "+repage",
            "-strip",
            PREVIEWS / f"{name}-mobile-crop.png",
        )

    inputs = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(ARTWORK.iterdir())
        if p.suffix in {".png", ".ttf"}
    }
    (ARTWORK / "manifest.json").write_text(
        json.dumps({"inputs": inputs, "exports": records}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(records)} SVGs and PNGs.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Fmind branding wallpapers, banners, previews, and manifest.")
    parser.parse_args(argv)
    try:
        generate()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError) as error:
        print(f"Artwork generation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
