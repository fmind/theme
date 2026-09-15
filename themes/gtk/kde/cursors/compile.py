#!/usr/bin/env python3
"""Compile editable SVG frames and native xcursorgen recipes into cursor files."""

import argparse
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

SOURCE = Path(__file__).resolve().parent / "src"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Directory for compiled cursor files")
    args = parser.parse_args()
    tools: dict[str, str] = {}
    for name in ("rsvg-convert", "xcursorgen"):
        binary = shutil.which(name)
        if not binary:
            parser.error(f"Install {name} before compiling cursor assets")
        tools[name] = binary
    recipes = sorted(SOURCE.glob("*.cursor"))
    frames: set[tuple[int, Path]] = set()
    for recipe in recipes:
        for line in recipe.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split()
            if len(fields) not in (4, 5):
                parser.error(f"Invalid xcursorgen row in {recipe.name}")
            try:
                size, x, y = map(int, fields[:3])
                delay = int(fields[4]) if len(fields) == 5 else 50
            except ValueError:
                parser.error(f"Expected integer size, hotspot and delay in {recipe.name}")
            image = Path(fields[3])
            if not 0 < size <= 1024 or not (0 <= x < size and 0 <= y < size):
                parser.error(f"Invalid size or hotspot in {recipe.name}")
            if image.parts != (str(size), image.name) or image.suffix != ".png":
                parser.error(f"Expected size/frame.png in {recipe.name}")
            if not (SOURCE / image.with_suffix(".svg").name).is_file():
                parser.error(f"Missing SVG frame for {image.name}")
            if not 0 < delay <= 60_000:
                parser.error(f"Invalid animation delay in {recipe.name}")
            frames.add((size, image))
    with TemporaryDirectory(prefix="fmind-cursor-build-") as directory:
        work = Path(directory)
        for size, image in sorted(frames):
            target = work / image
            target.parent.mkdir(exist_ok=True)
            subprocess.run(
                [
                    tools["rsvg-convert"],
                    "--width",
                    str(size),
                    "--height",
                    str(size),
                    "--output",
                    str(target),
                    str(SOURCE / image.with_suffix(".svg").name),
                ],
                check=True,
                timeout=30,
            )
        # Compile all inputs successfully before replacing any package assets.
        compiled = work / "compiled"
        compiled.mkdir()
        for recipe in recipes:
            subprocess.run(
                [tools["xcursorgen"], "-p", str(work), str(recipe), str(compiled / recipe.stem)],
                check=True,
                timeout=30,
            )
        args.output.mkdir(parents=True, exist_ok=True)
        for path in compiled.iterdir():
            target = args.output / path.name
            if target.is_symlink():
                parser.error(f"Refusing to overwrite symlink: {target}")
        for path in compiled.iterdir():
            shutil.copyfile(path, args.output / path.name)
    print(f"Compiled {len(recipes)} cursors from {len(frames)} raster frames")


if __name__ == "__main__":
    main()
