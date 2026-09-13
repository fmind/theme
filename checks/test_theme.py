"""Validate shipped files and native styles without generating application config."""

import json
import plistlib
import re
import runpy
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PALETTE = yaml.safe_load((ROOT / "checks/palette.yaml").read_text())


def contrast(a: str, b: str) -> float:
    def luminance(value):
        channels = [int(value[i : i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722), strict=True))

    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


class ThemeTests(unittest.TestCase):
    def test_native_documents_parse(self):
        for app in ("atuin", "bottom", "starship", "yazi"):
            with self.subTest(app=app):
                tomllib.loads((ROOT / app / "fmind.toml").read_text())
        for app, suffix in (
            ("gh-dash", "yml"),
            ("k9s", "yaml"),
            ("lazydocker", "yml"),
            ("lazygit", "yml"),
            ("lsd", "yaml"),
        ):
            with self.subTest(app=app):
                self.assertIsInstance(yaml.safe_load((ROOT / app / f"fmind.{suffix}").read_text()), dict)

        json.loads((ROOT / "fastfetch/fmind.json").read_text())

    def test_shipped_syntax_matches_selected_palette(self):
        theme = plistlib.loads((ROOT / "bat/fmind.tmTheme").read_bytes())
        self.assertEqual(theme["name"], "fmind")
        for rule in theme["settings"][1:]:
            color = rule["settings"]["foreground"]
            self.assertEqual(color, PALETTE["roles"][rule["name"]])

    def test_native_files_use_documented_palette(self):
        apps = [
            "atuin",
            "bat",
            "bottom",
            "delta",
            "fastfetch",
            "fish",
            "fzf",
            "gh-dash",
            "ghostty",
            "k9s",
            "lazydocker",
            "lazygit",
            "lsd",
            "lualine",
            "nvim",
            "opencode",
            "ptpython",
            "starship",
            "yazi",
            "zellij",
        ]
        for app in apps:
            for path in (ROOT / app).rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                colors = re.findall(r"(?i)(?<![\w])#?([0-9a-f]{6})(?![\w])", path.read_text())
                with self.subTest(path=path.relative_to(ROOT)):
                    self.assertLessEqual(
                        {f"#{c.lower()}" for c in colors}, set(PALETTE["official"] + PALETTE["custom"])
                    )

    def test_terminal_slots_and_navigation(self):
        content = (ROOT / "ghostty/fmind").read_text()
        slots = re.findall(r"^palette = (\d+)=(#[\da-f]{6})$", content, re.MULTILINE)
        self.assertEqual([int(i) for i, _ in slots], list(range(16)))
        self.assertEqual([color for _, color in slots], list(PALETTE["ansi"].values()))
        nvim = (ROOT / "nvim/colors/fmind.lua").read_text()
        self.assertEqual(
            re.findall(r'terminal_color_\d+ = "(#[\da-f]{6})"', nvim),
            [color for _, color in slots],
        )
        self.assertRegex(content, r"(?m)^minimum-contrast = 1$")
        self.assertGreaterEqual(contrast(PALETTE["text"], PALETTE["ground"]), 9)
        self.assertGreaterEqual(contrast(PALETTE["text"], PALETTE["surfaces"]["selection"]), 9)

    def test_syntax_contrast_on_highlighted_surfaces(self):
        surfaces = {"background": PALETTE["ground"], **PALETTE["surfaces"]}
        for role, foreground in PALETTE["roles"].items():
            for name in ("background", "line", "panel", "selection", "plus", "minus", "change"):
                with self.subTest(role=role, surface=name):
                    self.assertGreaterEqual(contrast(foreground, surfaces[name]), 4.5)

    def test_readme_palette_and_local_links(self):
        readme = (ROOT / "README.md").read_text()
        for color in PALETTE["official"] + PALETTE["custom"]:
            self.assertIn(color.lower(), readme.lower())
        for target in re.findall(r"\]\(([^)]+)\)", readme):
            if "://" not in target:
                self.assertTrue((ROOT / target).is_file(), target)

    def test_opencode_references_and_syntax(self):
        doc = json.loads((ROOT / "opencode/fmind.json").read_text())
        for key, value in doc["theme"].items():
            self.assertIn(value, doc["defs"], key)
            if key.startswith("syntax"):
                self.assertEqual(doc["defs"][value], PALETTE["roles"][value], key)
        for kind in ("Added", "Removed"):
            self.assertGreaterEqual(
                contrast(doc["defs"][doc["theme"][f"diff{kind}"]], doc["defs"][doc["theme"][f"diff{kind}Bg"]]),
                4.5,
            )

    def test_ptpython_native_style(self):
        from prompt_toolkit.styles import Style

        theme = runpy.run_path(str(ROOT / "ptpython/fmind.py"))
        for group in ("CODE", "UI"):
            Style.from_dict(theme[group])
        for key, style in theme["UI"].items():
            pair = re.search(r"(#[\da-f]{6}) bg:(#[\da-f]{6})", style)
            if pair and pair[2] not in ("#ffffff", "#f1f3f4"):
                self.assertGreaterEqual(contrast(pair[1], pair[2]), 4.5, key)

    def test_yazi_filled_labels(self):
        theme = tomllib.loads((ROOT / "yazi/fmind.toml").read_text())
        for section in ("tabs", "mode", "indicator"):
            for name, style in theme[section].items():
                self.assertGreaterEqual(contrast(style["fg"], style["bg"]), 4.5, name)
        for name in ("count_copied", "count_cut", "count_selected"):
            style = theme["mgr"][name]
            self.assertGreaterEqual(contrast(style["fg"], style["bg"]), 4.5, name)

    def test_zellij_tiles_remain_readable(self):
        content = (ROOT / "zellij/fmind.kdl").read_text()
        blocks = {}
        for name, body in re.findall(r"(\w+) \{([^{}]+)\}", content):
            blocks[name] = dict(re.findall(r'(\w+) "(#[0-9a-f]+)"', body))
        bar = blocks["text_unselected"]
        for name in ("ribbon_unselected", "ribbon_selected"):
            tile = blocks[name]
            self.assertNotEqual(tile["background"], bar["background"])
            for key, foreground in tile.items():
                if key == "background":
                    continue
                self.assertGreaterEqual(contrast(foreground, tile["background"]), 4.5)

        for name in (
            "text_unselected",
            "text_selected",
            "table_title",
            "table_cell_unselected",
            "table_cell_selected",
            "list_unselected",
            "list_selected",
        ):
            tile = blocks[name]
            for key, foreground in tile.items():
                if key != "background":
                    self.assertGreaterEqual(contrast(foreground, tile["background"]), 4.5, name)
