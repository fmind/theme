"""Native terminal palettes, isolated Lua loading, and WindTerm UI/syntax pairs."""

import ast
import configparser
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import tinycss2
from test_theme import PALETTE, ROOT, contrast

ANSI = list(PALETTE["ansi"].values())
NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]


def ini(path):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read(ROOT / path)
    return parser


class TerminalBatchTests(unittest.TestCase):
    def readable(self, fg, bg, label=""):
        for color in (fg, bg):
            self.assertIn(color, PALETTE["official"] + PALETTE["custom"], label)
        self.assertGreaterEqual(contrast(fg, bg), 4.5, label)

    def test_qterminal_normal_bright_and_faint_groups(self):
        config = ini("qterminal/fmind.colorscheme")

        def color(group):
            rgb = [int(c) for c in config[group]["Color"].split(",")]
            self.assertEqual(len(rgb), 3)
            return "#" + "".join(f"{c:02x}" for c in rgb)

        self.assertEqual(config["General"]["Description"], "Fmind")
        self.assertEqual(config["General"]["Opacity"], "1")
        self.assertEqual([color(f"Color{i}{suffix}") for suffix in ("", "Intense") for i in range(8)], ANSI)
        for suffix in ("", "Intense", "Faint"):
            self.assertEqual(color("Background" + suffix), "#ffffff")
            for prefix in ("Foreground", *(f"Color{i}" for i in range(8))):
                self.readable(color(prefix + suffix), color("Background" + suffix), prefix + suffix)

    def test_termite_ansi_cursor_and_hint_labels(self):
        config = ini("termite/fmind.conf")
        colors = config["colors"]
        self.assertEqual([colors[f"color{i}"] for i in range(16)], ANSI)
        self.readable(colors["foreground"], colors["background"])
        self.readable(colors["foreground_bold"], colors["background"])
        self.readable(colors["cursor_foreground"], colors["cursor"])
        for color in ANSI:
            self.readable(color, colors["highlight"])
        self.readable(config["hints"]["foreground"], config["hints"]["background"])
        # Termite does not implement a highlight_foreground key.
        self.assertNotIn("highlight_foreground", colors)

    def test_lxterminal_custom_palette_and_bold_policy(self):
        config = ini("lxterminal/fmind.conf")["general"]
        self.assertEqual(config["color_preset"], "Custom")
        self.assertEqual(config["boldbright"], "false")
        self.assertEqual([config[f"palette_color_{i}"] for i in range(16)], ANSI)
        self.readable(config["fgcolor"], config["bgcolor"])
        self.assertEqual(
            set(config),
            {"bgcolor", "fgcolor", "color_preset", "boldbright"} | {f"palette_color_{i}" for i in range(16)},
        )

    def test_st_extended_slots_do_not_replace_ansi_white(self):
        source = (ROOT / "st/fmind.h").read_text()
        colors = re.findall(r'"(#[\da-f]{6})"', source)
        self.assertEqual(colors[:16], ANSI)
        extra = {int(i): c for i, c in re.findall(r'\[(\d+)\] = "(#[\da-f]{6})"', source)}
        self.assertEqual(set(extra), {256, 257, 258, 259})
        defaults = {name: int(i) for name, i in re.findall(r"unsigned int (default\w+) = (\d+);", source)}
        self.assertEqual(set(defaults), {"defaultfg", "defaultbg", "defaultcs", "defaultrcs"})
        self.readable(extra[defaults["defaultfg"]], extra[defaults["defaultbg"]])
        self.readable(extra[defaults["defaultrcs"]], extra[defaults["defaultcs"]])
        self.assertEqual(extra[defaults["defaultbg"]], "#ffffff")

    def test_fluent_native_color_fields(self):
        theme = json.loads((ROOT / "fluent-terminal/fmind.flutecolors").read_text())
        self.assertEqual(theme["Name"], "Fmind")
        colors = theme["Colors"]
        slots = NAMES + ["Bright" + name for name in NAMES]
        self.assertEqual([colors[name] for name in slots], ANSI)
        self.assertEqual(
            set(colors),
            set(slots)
            | {
                "Foreground",
                "Background",
                "Cursor",
                "CursorAccent",
                "Selection",
                "SelectionForeground",
                "SelectionBackground",
            },
        )
        for fg, bg in (
            ("Foreground", "Background"),
            ("CursorAccent", "Cursor"),
            ("SelectionForeground", "SelectionBackground"),
            ("Foreground", "Selection"),
        ):
            self.readable(colors[fg], colors[bg], fg)

    def test_cosmic_complete_exported_color_contract(self):
        # This file uses only RON's named fields, nested tuples and string literals.
        source = (ROOT / "cosmic-terminal/fmind.ron").read_text()
        source = re.sub(r"(?m)^//.*$", "", source)
        source = source.replace("(", "{").replace(")", "}")
        source = re.sub(r"\b([a-z_]+):", r'"\1":', source)
        source = re.sub(r",\s*}", "}", source)
        theme = json.loads(source)
        self.assertEqual(
            set(theme),
            {
                "name",
                "foreground",
                "background",
                "cursor",
                "bright_foreground",
                "dim_foreground",
                "normal",
                "bright",
                "dim",
            },
        )
        self.assertEqual(theme["name"], "Fmind")
        self.assertEqual([theme[group][name.lower()] for group in ("normal", "bright") for name in NAMES], ANSI)
        for group in ("normal", "bright", "dim"):
            self.assertEqual(set(theme[group]), {name.lower() for name in NAMES})
            for color in theme[group].values():
                self.readable(color, theme["background"], group)
        for key in ("foreground", "bright_foreground", "dim_foreground"):
            self.readable(theme[key], theme["background"], key)

    def test_pantheon_custom_scheme_is_not_overridden_by_system(self):
        config = ini("pantheon-terminal/fmind.dconf")["/"]
        self.assertEqual(config["theme"], "'custom'")
        self.assertEqual(config["follow-system-style"], "false")
        self.assertEqual(config["prefer-dark-style"], "false")
        palette = ast.literal_eval(config["palette"]).split(":")
        self.assertEqual(palette, ANSI)
        self.readable(ast.literal_eval(config["foreground"]), ast.literal_eval(config["background"]))
        self.assertEqual(
            set(config),
            {
                "theme",
                "follow-system-style",
                "prefer-dark-style",
                "background",
                "foreground",
                "cursor-color",
                "palette",
            },
        )

    def test_tym_theme_executes_as_an_isolated_lua_table(self):
        program = "local f = assert(loadfile(arg[1])); setfenv(f, {}); io.write(vim.json.encode(f()))\n"
        with tempfile.TemporaryDirectory(prefix="fmind-tym-") as home:
            script = Path(home) / "check.lua"
            script.write_text(program)
            result = subprocess.run(
                ["nvim", "--headless", "-u", "NONE", "-i", "NONE", "-l", str(script), str(ROOT / "tym/theme.lua")],
                env={
                    **os.environ,
                    "HOME": home,
                    "XDG_CONFIG_HOME": home,
                    "XDG_DATA_HOME": home,
                    "XDG_STATE_HOME": home,
                    "XDG_CACHE_HOME": home,
                },
                text=True,
                capture_output=True,
                check=True,
                timeout=15,
            )
        self.assertEqual(result.stderr, "")
        theme = json.loads(result.stdout)
        self.assertEqual([theme[f"color_{i}"] for i in range(16)], ANSI)
        for fg, bg in (
            ("color_foreground", "color_background"),
            ("color_foreground", "color_window_background"),
            ("color_cursor_foreground", "color_cursor"),
            ("color_highlight_foreground", "color_highlight"),
            ("color_bold", "color_background"),
        ):
            self.readable(theme[fg], theme[bg], fg)

    def test_windterm_all_styles_scopes_and_decorations(self):
        source = (ROOT / "windterm/scheme.theme").read_text()
        theme = json.loads(re.sub(r"(?m)^//.*$", "", source))
        styles = {item["name"]: item["style"] for item in theme["styles"]}
        self.assertEqual(len(styles), 55)
        self.assertEqual(len(theme["styles"]), len(styles))
        self.assertEqual(len(theme["scopes"]), 50)
        slots = NAMES + ["Bright" + name for name in NAMES]
        self.assertEqual([styles["terminal.ansi" + name]["foreground"] for name in slots], ANSI)
        self.assertEqual(styles["text.default"]["background"], "#ffffff")
        self.assertEqual(styles["terminal.text"]["fontFamily"], "GoogleSansCode Nerd Font Mono")
        for entry in theme["styles"] + theme["scopes"]:
            label = str(entry.get("name", entry.get("scope")))
            style = entry["style"]
            self.assertLessEqual(
                set(style),
                {
                    "foreground",
                    "background",
                    "decorationForeground",
                    "decorationBackground",
                    "decorationStyle",
                    "fontFamily",
                    "fontSize",
                    "fontStyle",
                },
            )
            for key in ("foreground", "decorationForeground"):
                if key in style:
                    for bg in ("#ffffff", "#f1f3f4", "#d2e3fc", "#ceead6", "#fad2cf", "#feefc3"):
                        self.readable(style[key], bg, label)
            if "foreground" in style:
                for key in ("background", "decorationBackground"):
                    for bg in style.get(key, "#ffffff").split(", "):
                        self.readable(style["foreground"], bg, label)
        scopes = {e.get("name"): e["style"] for e in theme["scopes"] if "name" in e}
        for name, color in (
            ("Comment", "#595d62"),
            ("String", "#0d652d"),
            ("Keyword", "#174ea6"),
            ("diff.deleted", "#a50e0e"),
            ("diff.inserted", "#0d652d"),
        ):
            self.assertEqual(scopes[name]["foreground"], color, name)

    def test_windterm_ui_and_icon_colors_are_opaque_and_readable(self):
        for filename in ("gui.theme", "icon.theme"):
            source = (ROOT / "windterm" / filename).read_text()
            self.assertNotIn("$(AppDir)", source)
            self.assertNotRegex(source, r"::(?:disabled|selected|first|last)\b")
            rules = tinycss2.parse_stylesheet(source, skip_comments=True, skip_whitespace=True)
            for rule in rules:
                self.assertEqual(rule.type, "qualified-rule")
                selector = tinycss2.serialize(rule.prelude).strip()
                declarations = tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
                values = {}
                for declaration in declarations:
                    self.assertEqual(declaration.type, "declaration", selector)
                    values[declaration.name] = tinycss2.serialize(declaration.value).strip()
                fg = values.get("color")
                if fg:
                    for bg in ("#ffffff", "#f1f3f4", "#d2e3fc"):
                        self.readable(fg, bg, selector)
                    bg = values.get("background-color", "#ffffff")
                    if bg not in ("transparent", "none"):
                        self.readable(fg, bg, selector)
                for name in ("selection-color", "fill", "stroke"):
                    if values.get(name, "none") not in ("none", "transparent"):
                        self.readable(values[name], "#ffffff", selector)
