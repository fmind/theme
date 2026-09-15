"""Decode native desktop formats and exercise available style consumers offline."""

import configparser
import json
import os
import plistlib
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

import yaml
from pygments.formatters import HtmlFormatter
from pygments.lexers import DiffLexer, PythonLexer
from pygments.token import Generic, Keyword, String
from test_theme import PALETTE, ROOT, contrast

from pygments import highlight

ANSI = list(PALETTE["ansi"].values())
COLORS = set(PALETTE["official"] + PALETTE["custom"])


def ini(path):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read(ROOT / path)
    return parser


def normalized_rgb(channels):
    values = [float(c) for c in channels]
    if len(values) != 3 or any(not 0 <= c <= 1 for c in values):
        raise ValueError("Expected three RGB channels between zero and one")
    return "#" + "".join(f"{round(c * 255):02x}" for c in values)


class DesktopPortTests(unittest.TestCase):
    def readable(self, fg, bg, label=""):
        self.assertIn(fg, COLORS, label)
        self.assertIn(bg, COLORS, label)
        self.assertGreaterEqual(contrast(fg, bg), 4.5, label)

    def test_warp_and_tilix(self):
        warp = yaml.safe_load((ROOT / "warp/fmind.yaml").read_text())
        names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        self.assertEqual(warp["details"], "lighter")
        self.assertEqual([warp["terminal_colors"][group][n] for group in ("normal", "bright") for n in names], ANSI)
        self.readable(warp["foreground"], warp["background"])
        self.readable("#ffffff", warp["accent"])
        tilix = json.loads((ROOT / "tilix/fmind.json").read_text())
        self.assertFalse(tilix["use-theme-colors"])
        self.assertTrue(tilix["use-highlight-color"])
        self.assertTrue(tilix["use-cursor-color"])
        self.assertEqual(tilix["palette"], ANSI)
        for prefix in ("", "highlight-", "cursor-"):
            self.readable(tilix[prefix + "foreground-color"], tilix[prefix + "background-color"])
        for fg in ANSI:
            self.readable(fg, tilix["highlight-background-color"])

    def test_mobaxterm(self):
        theme = ini("mobaxterm/fmind.ini")["Colors"]
        self.assertEqual(theme["DefaultColorScheme"], "4")
        colors = {
            k: normalized_rgb([int(c) / 255 for c in v.split(",")])
            for k, v in theme.items()
            if k != "DefaultColorScheme"
        }
        names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
        self.assertEqual([colors[p + n] for p in ("", "Bold") for n in names], ANSI)
        self.readable(colors["ForegroundColour"], colors["BackgroundColour"])

    def test_terminal_apple_color_archives(self):
        theme = plistlib.loads((ROOT / "terminal-app/fmind.terminal").read_bytes())
        self.assertEqual(theme["type"], "Window Settings")
        self.assertFalse(theme["UseBrightBold"])
        colors = {}
        for key, value in theme.items():
            if not key.endswith("Color"):
                continue
            archive = plistlib.loads(value)
            self.assertEqual(archive["$archiver"], "NSKeyedArchiver")
            objects = archive["$objects"]
            color = objects[archive["$top"]["root"].data]
            self.assertEqual(objects[color["$class"].data]["$classname"], "NSColor")
            self.assertEqual(color["NSColorSpace"], 1)
            self.assertTrue(color["NSRGB"].endswith(b"\0"))
            colors[key] = normalized_rgb(color["NSRGB"].rstrip(b"\0").split())
        names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
        self.assertEqual([colors["ANSI" + p + n + "Color"] for p in ("", "Bright") for n in names], ANSI)
        for fg in ANSI + [colors["TextColor"], colors["TextBoldColor"]]:
            for bg in ("BackgroundColor", "SelectionColor"):
                self.readable(fg, colors[bg])

    def test_conemu_bgr_and_windows_slot_order(self):
        root = ET.parse(ROOT / "conemu/fmind.xml").getroot()
        values = {v.attrib["name"]: v.attrib for v in root.findall("value")}
        self.assertEqual(len(values), len(root.findall("value")))
        colors = []
        for i in range(32):
            field = values[f"ColorTable{i:02}"]
            self.assertEqual(field["type"], "dword")
            raw = field["data"]
            self.assertRegex(raw, r"^00[0-9a-f]{6}$")
            colors.append("#" + raw[6:8] + raw[4:6] + raw[2:4])
        order = [0, 4, 2, 6, 1, 5, 3, 7, 8, 12, 10, 14, 9, 13, 11, 15]
        expected = [ANSI[i] for i in order]
        # Native console palettes choose the canvas from these same 16 slots.
        expected[15] = PALETTE["ground"]
        self.assertEqual(colors, expected * 2)
        for prefix in ("", "Pop"):
            foreground = colors[int(values[prefix + "TextColorIdx"]["data"], 16)]
            background = colors[int(values[prefix + "BackColorIdx"]["data"], 16)]
            self.assertEqual(background, PALETTE["ground"])
            self.readable(foreground, background)
        for fg in colors[:15]:
            self.readable(fg, colors[15])

    def test_xcode_syntax_console_and_markup(self):
        theme = plistlib.loads((ROOT / "xcode/fmind.xccolortheme").read_bytes())

        def color(value):
            *channels, alpha = value.split()
            self.assertEqual(alpha, "1")
            return normalized_rgb(channels)

        syntax = theme["DVTSourceTextSyntaxColors"]
        self.assertEqual(set(syntax), set(theme["DVTSourceTextSyntaxFonts"]))
        self.assertGreaterEqual(len(syntax), 27)
        for name, value in syntax.items():
            for bg in (
                "DVTSourceTextBackground",
                "DVTSourceTextCurrentLineHighlightColor",
                "DVTSourceTextSelectionColor",
            ):
                self.readable(color(value), color(theme[bg]), name)
        for key, value in theme.items():
            if key.startswith("DVTConsole") and key.endswith("TextColor"):
                for bg in ("DVTConsoleTextBackgroundColor", "DVTConsoleTextSelectionColor"):
                    self.readable(color(value), color(theme[bg]), key)
            if (
                key.startswith("DVTMarkupText")
                and key.endswith("Color")
                and "Background" not in key
                and "Border" not in key
            ):
                self.readable(color(value), color(theme["DVTMarkupTextBackgroundColor"]), key)

    def test_geany_complete_named_styles(self):
        styles = ini("geany/fmind.conf")["named_styles"]
        self.assertEqual(styles["selection"].split(";")[2:], ["true", "true"])
        self.assertEqual(styles["current_line"].split(";")[2], "true")
        decorations = {"caret", "indent_guide", "white_space", "fold_symbol_highlight"}
        for name, value in styles.items():
            fg, bg, bold, italic = value.split(";")
            self.assertIn(bold, ("true", "false"))
            self.assertIn(italic, ("true", "false"))
            fg, bg = fg.replace("0x", "#"), bg.replace("0x", "#")
            self.assertIn(fg, COLORS)
            if name not in decorations:
                self.readable(fg, bg, name)
                for surface in ("selection", "current_line"):
                    self.readable(fg, styles[surface].split(";")[1].replace("0x", "#"), name)

    def test_idle_native_parser_with_isolated_home(self):
        # Importing idlelib.config initializes its global config; isolate even that read.
        program = """
import json, sys
from idlelib.config import IdleConf, IdleConfParser
parser = IdleConfParser(sys.argv[1])
parser.Load()
conf = IdleConf(_utest=True)
conf.userCfg['highlight'] = parser
print(json.dumps(conf.GetThemeDict('user', 'Fmind')))
"""
        with tempfile.TemporaryDirectory(prefix="fmind-idle-") as home:
            result = subprocess.run(
                [sys.executable, "-c", program, str(ROOT / "idle/fmind.cfg")],
                env={**os.environ, "HOME": home, "USERPROFILE": home},
                capture_output=True,
                text=True,
                check=True,
                timeout=15,
            )
        self.assertEqual(result.stderr, "")
        theme = json.loads(result.stdout)
        self.assertEqual(theme, dict(ini("idle/fmind.cfg")["Fmind"]))
        for key, fg in theme.items():
            if key.endswith("-foreground"):
                self.readable(fg, theme.get(key.replace("foreground", "background"), theme["normal-background"]), key)

    def test_pygments_real_tokens_and_html(self):
        style = runpy.run_path(str(ROOT / "pygments/fmind.py"))["FmindStyle"]
        formatter = HtmlFormatter(style=style, full=True)
        source = 'def greet(name):\n    # A synthetic fixture\n    return "hello " + name\n'
        html = highlight(source, PythonLexer(), formatter)
        self.assertIn('class="k"', html)
        self.assertIn('class="s2"', html)
        self.assertIn("greet", html)
        self.assertEqual(style.style_for_token(Keyword)["color"], "174ea6")
        self.assertEqual(style.style_for_token(String)["color"], "0d652d")
        diff = highlight("--- old\n+++ new\n@@ -1 +1 @@\n-before\n+after\n", DiffLexer(), formatter)
        self.assertIn('class="gd"', diff)
        self.assertIn('class="gi"', diff)
        for token, definition in style:
            if definition["color"]:
                for bg in (style.background_color, style.highlight_color):
                    self.readable("#" + definition["color"], bg, str(token))
                if definition["bgcolor"]:
                    self.readable("#" + definition["color"], "#" + definition["bgcolor"], str(token))
        self.assertEqual(style.style_for_token(Generic.Deleted)["bgcolor"], "fad2cf")

    def test_catalog_scope_and_shipped_paths(self):
        from test_theme import APPS

        catalog = (ROOT / "CATALOG.md").read_text()
        readme = (ROOT / "README.md").read_text()
        rows = re.findall(
            r"^\| +([^|]+) +\| +(Core|Additional) +\| +\[([^]]+)\]\(([^)]+)/\) +\|$", catalog, re.MULTILINE
        )
        self.assertEqual(len(rows), len(APPS))
        self.assertEqual({path for _, _, _, path in rows}, {app.name for app in APPS})
        self.assertIn(f"{len(rows)} integration directories", readme)
        self.assertIn(f"{len(rows)} integration directories", catalog)
        for _, _, label, path in rows:
            self.assertEqual(label, path)
            self.assertTrue((ROOT / path).is_dir(), path)
            self.assertIn(f"]({path}/", readme, path)

        # Snapshot of native paths consumed by chezmoi. Keep CI independent of
        # private dotfiles while protecting the public installation contract.
        core_paths = (
            "atuin/fmind.toml",
            "bat/fmind.tmTheme",
            "bottom/fmind.toml",
            "delta/fmind.gitconfig",
            "fastfetch/fmind.json",
            "fish/fmind.fish",
            "fzf/fmind.conf",
            "gh-dash/fmind.yml",
            "ghostty/fmind",
            "k9s/fmind.yaml",
            "lazydocker/fmind.yml",
            "lazygit/fmind.yml",
            "lsd/fmind.yaml",
            "lualine/fmind.lua",
            "nvim/colors/fmind.lua",
            "opencode/fmind.json",
            "ptpython/fmind.py",
            "starship/fmind.toml",
            "yazi/fmind.toml",
            "zellij/fmind.kdl",
        )
        self.assertEqual(
            {path for _, priority, _, path in rows if priority == "Core"}, {path.split("/")[0] for path in core_paths}
        )
        for path in core_paths:
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertIn(f"]({path})", readme, path)
