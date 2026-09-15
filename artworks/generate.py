#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["fonttools>=4.60", "uharfbuzz>=0.51", "typer>=0.27", "rich>=15"]
# ///
"""Generate faithful Fmind branding wallpapers and banners."""

import base64
import hashlib
import json
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

import typer
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from rich.console import Console

ROOT = Path(__file__).resolve().parents[1]
ARTWORK = ROOT / "artworks"
PREVIEWS = ARTWORK / "previews"

BLUE = "#174ea6"
INK = "#353b4e"
WHITE = "#fdfdfd"
WIDTH, HEIGHT = 1988, 536

VARIANTS = [
    ("wallpapers/fmind-desktop-16x9", 3840, 2160, 0.80),
    ("wallpapers/fmind-laptop-16x10", 2560, 1600, 0.80),
    ("wallpapers/fmind-ultrawide-21x9", 3360, 1440, 0.74),
    ("wallpapers/fmind-tablet-3x4", 1536, 2048, 0.92),
    ("wallpapers/fmind-phone-9x20", 1440, 3200, 0.94),
    ("wallpapers/fmind-square", 2048, 2048, 0.86),
    ("banners/youtube", 2560, 1440, 0.57),
    ("banners/x", 1500, 500, 0.76),
    ("banners/linkedin", 1584, 396, 0.73),
    ("banners/reddit", 1920, 384, 0.39),
    ("banners/bluesky", 1500, 500, 0.76),
    ("banners/mastodon", 1500, 500, 0.76),
]

app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)


def lettering(text: str, x: float, y: float, width: float, color: str) -> str:
    """Shape Google Sans glyphs with kerning and export exact vector outlines."""
    font_path = ARTWORK / "GoogleSans-Bold.ttf"
    font = TTFont(font_path)
    glyphs = font.getGlyphSet()
    shaping_font = hb.Font(hb.Face(font_path.read_bytes()))
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
    left, _bottom, right, top = bounds.bounds
    scale = width / (right - left)
    return (
        f'<g aria-label="{escape(text)}" fill="{color}" '
        f'transform="translate({x - left * scale} {y + top * scale}) scale({scale} {-scale})">'
        f'<path d="{outlines.getCommands()}"/></g>'
    )


def composition() -> str:
    """Build the faithful panel composition using the authentic logo and Google Sans outlines."""
    logo = base64.b64encode((ARTWORK / "logo.png").read_bytes()).decode()
    return (
        f'<rect x="10" y="10" width="1968" height="516" rx="48" '
        f'fill="{WHITE}" stroke="{BLUE}" stroke-width="20"/>'
        f'<image x="71" y="29" width="480" height="480" '
        f'href="data:image/png;base64,{logo}" xlink:href="data:image/png;base64,{logo}"/>'
        + lettering("fmind.dev", 615, 96, 1280, BLUE)
        + lettering("AI Agents, MLOps & Security", 625, 366, 1225, INK)
    )


def svg_document(width: int, height: int, content: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f"<title>fmind.dev — AI Agents, MLOps &amp; Security</title>{content}</svg>"
    )


def render(source: Path, target: Path) -> None:
    subprocess.run(
        [
            "magick",
            "-background",
            WHITE,
            str(source),
            "-alpha",
            "remove",
            "-alpha",
            "off",
            "-strip",
            "PNG24:" + str(target),
        ],
        check=True,
    )


@app.command()
def main() -> None:
    """Generate all 12 SVG sources, export exact PNGs, and create validation previews."""
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    art = composition()
    master = ARTWORK / "composition.svg"
    master.write_text(svg_document(WIDTH, HEIGHT, art))
    render(master, PREVIEWS / "composition.png")

    records = []
    for name, width, height, fraction in VARIANTS:
        panel_width = round(width * fraction)
        scale = panel_width / WIDTH
        panel_height = HEIGHT * scale
        x = (width - panel_width) / 2
        y = (height - panel_height) / 2
        if name in {"banners/x", "banners/bluesky", "banners/mastodon", "banners/linkedin"}:
            x = width - panel_width - width * 0.035
            y = (height - panel_height) / 2

        content = f'<rect width="{width}" height="{height}" fill="{WHITE}"/>'
        content += f'<g transform="translate({x} {y}) scale({scale})">{art}</g>'

        svg_path = ROOT / f"{name}.svg"
        png_path = ROOT / f"{name}.png"
        svg_path.write_text(svg_document(width, height, content))
        render(svg_path, png_path)

        records.append(
            {
                "file": f"{name}.png",
                "svg": f"{name}.svg",
                "width": width,
                "height": height,
                "panel": [x, y, panel_width, panel_height],
                "bytes": png_path.stat().st_size,
                "sha256": hashlib.sha256(png_path.read_bytes()).hexdigest(),
            }
        )

    # Previews
    command = ["magick"]
    subprocess.run(
        command
        + [
            "montage",
            *[str(ROOT / r["file"]) for r in records],
            "-font",
            str(ARTWORK / "GoogleSans-Bold.ttf"),
            "-pointsize",
            "16",
            "-label",
            "%f",
            "-geometry",
            "460x280+12+28",
            "-background",
            "#e8e8e8",
            "-tile",
            "3x",
            str(PREVIEWS / "all-variants.png"),
        ],
        check=True,
    )

    subprocess.run(
        command
        + [
            str(ARTWORK / "reference-banner.png"),
            "-background",
            WHITE,
            "-alpha",
            "remove",
            "-crop",
            "1988x536+34+114",
            "+repage",
            str(PREVIEWS / "composition.png"),
            "-append",
            str(PREVIEWS / "reference-comparison.png"),
        ],
        check=True,
    )

    for name, geometry in [("youtube", "1543x422+508+509"), ("reddit", "1920x227+0+78")]:
        subprocess.run(
            command
            + [
                str(ROOT / f"banners/{name}.png"),
                "-crop",
                geometry,
                "+repage",
                str(PREVIEWS / f"{name}-mobile-crop.png"),
            ],
            check=True,
        )

    inputs = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ARTWORK.iterdir() if p.suffix in {".png", ".ttf"}
    }
    (ARTWORK / "manifest.json").write_text(json.dumps({"inputs": inputs, "exports": records}, indent=2) + "\n")
    Console().print(f"Successfully generated {len(records)} SVGs and PNGs.")


if __name__ == "__main__":
    app()
