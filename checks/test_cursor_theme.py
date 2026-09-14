"""Xcursor binary integrity, source recipes and full reference-name coverage."""

import struct
import unittest
import xml.etree.ElementTree as ET
from collections import defaultdict

from test_kde_theme import config
from test_theme import ROOT, contrast

BASE = ROOT / "gtk/kde/cursors"
THEME = BASE / "Fmind"
SIZES = {24, 32, 36, 48, 64, 96}


def images(path):
    """Decode the documented little-endian Xcursor image chunks, including TOC."""
    data = path.read_bytes()
    if len(data) < 16:
        raise ValueError("Truncated Xcursor header")
    magic, header, version, count = struct.unpack_from("<4sIII", data)
    if magic != b"Xcur" or header != 16 or version != 0x10000 or not 0 < count <= 4096:
        raise ValueError("Invalid Xcursor header")
    end = header + count * 12
    if end > len(data):
        raise ValueError("Truncated Xcursor table of contents")
    result = []
    for index in range(count):
        kind, size, offset = struct.unpack_from("<III", data, header + index * 12)
        if kind != 0xFFFD0002 or offset != end or offset + 36 > len(data):
            raise ValueError("Invalid Xcursor image location")
        length, actual_kind, actual_size, revision, width, height, x, y, delay = struct.unpack_from("<9I", data, offset)
        if (length, actual_kind, actual_size, revision) != (36, kind, size, 1):
            raise ValueError("Image chunk disagrees with its table entry")
        if not 0 < width <= 1024 or not 0 < height <= 1024 or x >= width or y >= height:
            raise ValueError("Invalid image dimensions or hotspot")
        end = offset + length + width * height * 4
        if end > len(data):
            raise ValueError("Truncated Xcursor pixels")
        pixels = struct.unpack_from(f"<{width * height}I", data, offset + length)
        result.append((size, width, height, x, y, delay, pixels))
    if end != len(data):
        raise ValueError("Unexpected trailing Xcursor data")
    return result


class CursorThemeTests(unittest.TestCase):
    def test_complete_reference_names_and_internal_aliases(self):
        names = set((ROOT / "checks/cursor_names.txt").read_text().splitlines())
        self.assertEqual({p.name for p in (THEME / "cursors").iterdir()}, names)
        self.assertEqual(config(THEME / "index.theme")["Icon Theme"]["Name"], THEME.name)
        for path in (THEME / "cursors").iterdir():
            self.assertTrue(path.resolve().is_relative_to((THEME / "cursors").resolve()), path.name)
            self.assertTrue(path.is_file(), path.name)
            if path.is_symlink():
                self.assertEqual(path.readlink().parts, (path.resolve().name,), path.name)
        for kind in ("hor", "ver", "fdiag", "bdiag"):
            self.assertEqual((THEME / "cursors" / f"size-{kind}").resolve().name, f"size_{kind}")
        self.assertEqual((THEME / "cursors/move").resolve().name, "fleur")
        self.assertEqual((THEME / "cursors/grabbing").resolve().name, "closedhand")

    def test_binary_images_match_native_recipes_and_visible_pixels(self):
        canonical = {p.name for p in (THEME / "cursors").iterdir() if not p.is_symlink()}
        self.assertEqual(canonical, {p.stem for p in (BASE / "src").glob("*.cursor")})
        for name in canonical:
            rows = [
                row.split()
                for row in (BASE / "src" / f"{name}.cursor").read_text().splitlines()
                if row.strip() and not row.startswith("#")
            ]
            decoded = images(THEME / "cursors" / name)
            self.assertEqual(len(decoded), len(rows), name)
            self.assertEqual({im[0] for im in decoded}, SIZES)
            for row, (size, width, height, x, y, delay, pixels) in zip(rows, decoded, strict=True):
                self.assertEqual(
                    (size, width, height, x, y), (int(row[0]), int(row[0]), int(row[0]), int(row[1]), int(row[2]))
                )
                self.assertEqual(delay, int(row[4]) if len(row) == 5 else 0)
                self.assertTrue((BASE / "src" / row[3].split("/")[-1].replace(".png", ".svg")).is_file())
                self.assertIn(0, pixels, name)
                # Small outlined shapes can have only antialiased white pixels.
                self.assertTrue(
                    any(
                        (px >> 24) >= 128 and all(((px >> shift) & 255) == (px >> 24) for shift in (16, 8, 0))
                        for px in pixels
                    ),
                    name,
                )
                # At small sizes, antialiasing blends thin strokes with the halo.
                opaque = [px & 0xFFFFFF for px in pixels if px >> 24 == 255]
                self.assertTrue(opaque, name)
                darkest = min(opaque, key=lambda px: sum((px >> shift) & 255 for shift in (16, 8, 0)))
                self.assertGreaterEqual(contrast(f"#{darkest:06x}", "#ffffff"), 4.5, name)
                for px in pixels:
                    alpha = px >> 24
                    self.assertTrue(all(((px >> shift) & 255) <= alpha for shift in (16, 8, 0)), name)

    def test_pointing_and_resize_hotspots_follow_the_action_point(self):
        spots = {
            "default": (4, 3),
            "right_ptr": (28, 3),
            "center_ptr": (16, 3),
            "up-arrow": (16, 3),
            "right-arrow": (29, 16),
            "down-arrow": (16, 29),
            "left-arrow": (3, 16),
            "top_side": (16, 4),
            "right_side": (28, 16),
            "bottom_side": (16, 28),
            "left_side": (4, 16),
            "top_left_corner": (5, 5),
            "top_right_corner": (27, 5),
            "bottom_left_corner": (5, 27),
            "bottom_right_corner": (27, 27),
            "pencil": (5, 27),
            "color-picker": (5, 27),
            "pointer": (15, 3),
        }
        for name, (x, y) in spots.items():
            for size, _, _, actual_x, actual_y, _, pixels in images(THEME / "cursors" / name):
                self.assertEqual((actual_x, actual_y), (round(x * size / 32), round(y * size / 32)), name)
                self.assertGreater(pixels[actual_y * size + actual_x] >> 24, 0, name)

    def test_animations_have_distinct_frames_and_stable_hotspots(self):
        for name in ("wait", "progress"):
            by_size = defaultdict(list)
            for frame in images(THEME / "cursors" / name):
                by_size[frame[0]].append(frame)
            for frames in by_size.values():
                self.assertEqual(len(frames), 12)
                self.assertEqual(len({frame[3:5] for frame in frames}), 1)
                self.assertEqual({frame[5] for frame in frames}, {60})
                self.assertEqual(len({frame[-1] for frame in frames}), 12)

    def test_svg_frames_are_self_contained_geometry(self):
        for path in (BASE / "src").glob("*.svg"):
            root = ET.parse(path).getroot()
            self.assertEqual(root.get("viewBox"), "0 0 32 32")
            for node in root.iter():
                self.assertIn(node.tag.split("}")[-1], {"svg", "g", "path", "circle"})
                for key in node.attrib:
                    self.assertNotIn(key, {"href", "style", "opacity", "filter"})
                for key in ("fill", "stroke"):
                    if key in node.attrib:
                        self.assertIn(node.get(key), {"none", "#ffffff", "#202124", "#174ea6", "#a50e0e", "#0d652d"})


if __name__ == "__main__":
    unittest.main()
