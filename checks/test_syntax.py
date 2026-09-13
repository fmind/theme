"""Exercise real Neovim captures/legacy syntax and bat's emitted terminal styles."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml
from test_theme import PALETTE, ROOT

CASES = yaml.safe_load((ROOT / "checks/syntax.yaml").read_text())


def terminal_cells(output: str, foreground: int) -> tuple[str, list[dict]]:
    """Decode bat's SGR output to the style displayed at each character."""
    plain, cells = "", []
    style = {"fg": foreground}
    offset = 0
    for match in re.finditer(r"\x1b\[([\d;]*)m", output):
        segment = output[offset : match.start()]
        plain += segment
        cells.extend(dict(style) for _ in segment)
        codes = [int(n) for n in match[1].split(";") if n] or [0]
        index = 0
        while index < len(codes):
            code = codes[index]
            if code == 0:
                style = {"fg": foreground}
            elif code in (38, 48) and codes[index + 1] == 2:
                red, green, blue = codes[index + 2 : index + 5]
                style["fg" if code == 38 else "bg"] = red * 65536 + green * 256 + blue
                index += 4
            elif code in (1, 3, 4, 9):
                style[{1: "bold", 3: "italic", 4: "underline", 9: "strikethrough"}[code]] = True
            elif code in (22, 23, 24, 29):
                style.pop({22: "bold", 23: "italic", 24: "underline", 29: "strikethrough"}[code], None)
            elif code == 39:
                style["fg"] = foreground
            elif code == 49:
                style.pop("bg", None)
            else:
                raise AssertionError(f"Unrecognized bat SGR code: {codes}")
            index += 1
        offset = match.end()
    plain += output[offset:]
    cells.extend(dict(style) for _ in output[offset:])
    assert "\x1b" not in plain, "Unhandled terminal escape in bat output"
    return plain, cells


class SyntaxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.palette = PALETTE
        cls.work = tempfile.TemporaryDirectory(prefix="fmind-syntax-")
        cls.addClassCleanup(cls.work.cleanup)
        cls.directory = Path(cls.work.name)
        cls.env = {
            **os.environ,
            "FMIND_THEME_ROOT": str(ROOT),
            "HOME": cls.work.name,
            "TERM": "xterm-256color",
            "COLORTERM": "truecolor",
        }
        for kind in ("CONFIG", "DATA", "CACHE", "STATE"):
            cls.env[f"XDG_{kind}_HOME"] = str(cls.directory / kind.lower())
        theme = cls.directory / "config/bat/themes/fmind.tmTheme"
        theme.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "bat/fmind.tmTheme", theme)
        cls.env["BAT_CONFIG_PATH"] = os.devnull
        cls.env["BAT_CACHE_PATH"] = str(cls.directory / "bat-cache")
        subprocess.run(["bat", "cache", "--build"], env=cls.env, check=True, capture_output=True, timeout=30)

    def assert_style(self, case: dict, style: dict):
        expected = self.palette["roles"][case["role"]]
        self.assertEqual(style.get("fg"), int(expected[1:], 16), case)
        self.assertEqual(bool(style.get("bold")), case.get("bold", False), case)
        self.assertFalse(style.get("italic", False), "The theme keeps text upright")

    def check_neovim(self, engine: str):
        cases = [{**case, "engine": engine} for case in CASES if engine in case["engines"]]
        request, response = self.directory / "request.json", self.directory / "response.json"
        request.write_text(json.dumps(cases))
        result = subprocess.run(
            [
                "nvim",
                "--headless",
                "-u",
                "NONE",
                "-i",
                "NONE",
                "-n",
                "-l",
                str(ROOT / "checks/nvim.lua"),
                str(request),
                str(response),
            ],
            env=self.env,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "", "Neovim emitted diagnostics")
        styles = json.loads(response.read_text())
        self.assertEqual(len(styles), len(cases))
        for case, style in zip(cases, styles, strict=True):
            with self.subTest(file=case["file"], token=case["text"], engine=case["engine"]):
                self.assert_style(case, style)
                if case.get("capture") == "markup.strikethrough":
                    self.assertTrue(style.get("strikethrough"), case)

    def test_native_coverage(self):
        result = subprocess.run(
            ["nvim", "--headless", "-u", "NONE", "-i", "NONE", "-l", str(ROOT / "checks/coverage.lua")],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "", "Neovim emitted diagnostics")

    def test_neovim_treesitter(self):
        self.check_neovim("treesitter")

    def test_neovim_legacy(self):
        self.check_neovim("legacy")

    def test_missing_runtime_explains_setup(self):
        result = subprocess.run(
            ["nvim", "--headless", "-u", "NONE", "-i", "NONE", "-l", str(ROOT / "checks/runtime.lua")],
            env={**self.env, "FMIND_THEME_ROOT": str(self.directory)},
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run mise run install", result.stderr)

    def test_bat_tokens(self):
        rendered = {}
        for case in CASES:
            if "bat" not in case["engines"]:
                continue
            with self.subTest(file=case["file"], token=case["text"]):
                if case["file"] not in rendered:
                    result = subprocess.run(
                        [
                            "bat",
                            "--paging=never",
                            "--color=always",
                            "--style=plain",
                            "--theme=fmind",
                            str(ROOT / "checks/samples" / case["file"]),
                        ],
                        env=self.env,
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=15,
                    )
                    self.assertEqual(result.stderr, "", "bat emitted diagnostics")
                    rendered[case["file"]] = terminal_cells(result.stdout, int(self.palette["text"][1:], 16))
                plain, styles = rendered[case["file"]]
                start = sum(len(line) for line in plain.splitlines(keepends=True)[: case.get("line", 1) - 1])
                position = plain.index(case["text"], start)
                self.assert_style(case, styles[position])
