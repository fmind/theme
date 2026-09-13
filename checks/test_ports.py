"""Offline checks of shipped native ports, their selections and ANSI mappings."""

import configparser
import json
import plistlib
import re
import tomllib
import unittest

from test_theme import PALETTE, ROOT, contrast


def toml(app):
    return tomllib.loads((ROOT / app / "fmind.toml").read_text())


def ini(path):
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(path.read_text())
    return parser


def plist_color(value):
    return "#" + "".join(f"{round(value[channel + ' Component'] * 255):02x}" for channel in ("Red", "Green", "Blue"))


class PortTests(unittest.TestCase):
    def assert_readable(self, foreground, background, context=""):
        self.assertGreaterEqual(contrast(foreground, background), 4.5, context)

    def assert_slots(self, colors):
        self.assertEqual(colors, list(PALETTE["ansi"].values()))
        for foreground in colors:
            self.assert_readable(foreground, PALETTE["ground"])
            self.assert_readable(foreground, PALETTE["surfaces"]["selection"])

    def test_alacritty_slots_and_labels(self):
        colors = toml("alacritty")["colors"]
        self.assert_slots(list(colors["normal"].values()) + list(colors["bright"].values()))
        for name in ("cursor", "vi_mode_cursor", "selection"):
            value = colors[name]
            self.assert_readable(value["text"], value.get("cursor", value.get("background")), name)
        for name in ("search", "hints"):
            for value in colors[name].values():
                self.assert_readable(value["foreground"], value["background"], name)
        for value in colors["dim"].values():
            self.assert_readable(value, colors["primary"]["background"])

    def test_kitty_slots_and_labels(self):
        fields = dict(
            line.split(maxsplit=1)
            for line in (ROOT / "kitty/fmind.conf").read_text().splitlines()
            if line and not line.startswith("#")
        )
        self.assert_slots([fields[f"color{i}"] for i in range(16)])
        for prefix in ("selection", "active_tab", "inactive_tab", "mark1", "mark2", "mark3"):
            self.assert_readable(fields[prefix + "_foreground"], fields[prefix + "_background"], prefix)
        self.assert_readable(fields["cursor_text_color"], fields["cursor"])

    def test_wezterm_slots_and_tabs(self):
        theme = toml("wezterm")
        self.assertEqual(theme["metadata"]["name"], "fmind")
        colors = theme["colors"]
        self.assert_slots(colors["ansi"] + colors["brights"])
        self.assert_readable(colors["selection_fg"], colors["selection_bg"])
        self.assert_readable(colors["cursor_fg"], colors["cursor_bg"])
        for name, value in colors["tab_bar"].items():
            if isinstance(value, dict):
                self.assert_readable(value["fg_color"], value["bg_color"], name)

    def test_windows_terminal_slots(self):
        colors = json.loads((ROOT / "windows-terminal/fmind.json").read_text())
        names = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]
        self.assert_slots([colors[n] for n in names] + [colors["bright" + n.title()] for n in names])
        self.assert_readable(colors["foreground"], colors["background"])
        self.assert_readable(colors["foreground"], colors["selectionBackground"])

    def test_iterm_srgb_slots(self):
        theme = plistlib.loads((ROOT / "iterm2/fmind.itermcolors").read_bytes())
        for value in theme.values():
            self.assertEqual(value["Color Space"], "sRGB")
            for channel in ("Red", "Green", "Blue"):
                self.assertTrue(0 <= value[channel + " Component"] <= 1)
        colors = {k: plist_color(v) for k, v in theme.items()}
        self.assertLessEqual(set(colors.values()), set(PALETTE["official"] + PALETTE["custom"]))
        self.assert_slots([colors[f"Ansi {i} Color"] for i in range(16)])
        for fg, bg in (("Foreground", "Background"), ("Selected Text", "Selection"), ("Cursor Text", "Cursor")):
            self.assert_readable(colors[fg + " Color"], colors[bg + " Color"])

    def test_konsole_rgb_slots(self):
        theme = ini(ROOT / "konsole/fmind.colorscheme")
        colors = {}
        for section in theme.sections():
            if section != "General":
                rgb = [int(c) for c in theme[section]["Color"].split(",")]
                self.assertEqual(len(rgb), 3)
                self.assertTrue(all(0 <= c <= 255 for c in rgb))
                colors[section] = "#" + "".join(f"{c:02x}" for c in rgb)
        self.assertLessEqual(set(colors.values()), set(PALETTE["official"] + PALETTE["custom"]))
        self.assert_slots([colors[f"Color{i}{suffix}"] for suffix in ("", "Intense") for i in range(8)])
        for suffix in ("", "Intense", "Faint"):
            self.assert_readable(colors["Foreground" + suffix], colors["Background" + suffix])

    def test_foot_light_palette_and_labels(self):
        parser = configparser.ConfigParser(interpolation=None)
        parser.read_string("[main]\n" + (ROOT / "foot/fmind.ini").read_text())
        self.assertEqual(parser["main"]["initial-color-theme"], "light")
        colors = parser["colors-light"]
        self.assert_slots(["#" + colors[f"{prefix}{i}"] for prefix in ("regular", "bright") for i in range(8)])
        for name in ("cursor", "jump-labels", "scrollback-indicator", "search-box-no-match", "search-box-match"):
            fg, bg = colors[name].split()
            self.assert_readable("#" + fg, "#" + bg, name)
        self.assert_readable("#" + colors["selection-foreground"], "#" + colors["selection-background"])

    def test_rio_slots_and_titles(self):
        colors = toml("rio")["colors"]
        names = list(PALETTE["ansi"])[:8]
        self.assert_slots([colors[prefix + n] for prefix in ("", "light-") for n in names])
        for name in ("selection", "search-match", "search-focused-match"):
            self.assert_readable(colors[name + "-foreground"], colors[name + "-background"], name)
        for name in ("tabs", "tabs-active", "dim-foreground", "light-foreground"):
            self.assert_readable(colors[name], colors["background"], name)

    def test_helix_references_and_styles(self):
        theme = toml("helix")
        palette = theme.pop("palette")
        for name, value in theme.items():
            if isinstance(value, str):
                self.assertIn(value, palette, name)
            else:
                for key in ("fg", "bg"):
                    if key in value:
                        self.assertIn(value[key], palette, name)
                if "underline" in value:
                    self.assertIn(value["underline"]["color"], palette, name)
                if "fg" in value:
                    self.assert_readable(palette[value["fg"]], palette[value.get("bg", "white")], name)
        for name in ("comment", "string", "keyword", "function", "type", "constant"):
            value = theme[name]
            fg = palette[value if isinstance(value, str) else value["fg"]]
            for bg in ("white", "panel", "selection", "added", "deleted", "changed"):
                self.assert_readable(fg, palette[bg], name)

    def test_micro_and_tmux_filled_styles(self):
        for line in (ROOT / "micro/fmind.micro").read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            match = re.fullmatch(
                r'color-link ([\w.-]+) "(?:(?:bold|underline) )?(#[\da-f]{6})?(?:,(#[\da-f]{6}))?"', line
            )
            self.assertIsNotNone(match, line)
            if match[2] and match[3]:
                self.assert_readable(match[2], match[3], match[1])
        for line in (ROOT / "tmux/fmind.conf").read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            self.assertRegex(line, r"^set -g [\w-]+ '[^']+'$")
            pair = re.search(r"fg=(#[\da-f]{6}),bg=(#[\da-f]{6})", line)
            if pair:
                self.assert_readable(pair[1], pair[2], line)

    def test_btop_text_and_selection(self):
        colors = {}
        for line in (ROOT / "btop/fmind.theme").read_text().splitlines():
            if line and not line.startswith("#"):
                match = re.fullmatch(r'theme\[([\w]+)\]="(#[\da-f]{6})"', line)
                self.assertIsNotNone(match, line)
                self.assertNotIn(match[1], colors)
                colors[match[1]] = match[2]
        self.assert_readable(colors["selected_fg"], colors["selected_bg"])
        for key in ("main_fg", "title", "hi_fg", "inactive_fg", "graph_text", "proc_misc"):
            self.assert_readable(colors[key], colors["main_bg"], key)

    def test_vscode_extension_and_editor(self):
        manifest = json.loads((ROOT / "vscode/package.json").read_text())
        (contribution,) = manifest["contributes"]["themes"]
        self.assertEqual(contribution["uiTheme"], "vs")
        theme = json.loads((ROOT / "vscode" / contribution["path"]).read_text())
        self.assertEqual(theme["type"], "light")
        self.assertTrue(theme["semanticHighlighting"])
        colors = theme["colors"]
        names = [n.title() for n in list(PALETTE["ansi"])[:8]]
        self.assert_slots([colors["terminal.ansi" + p + n] for p in ("", "Bright") for n in names])
        for key, foreground in colors.items():
            if key.endswith("Foreground"):
                background = colors.get(key.removesuffix("Foreground") + "Background")
                if background:
                    self.assert_readable(foreground, background, key)
        for rule in [*theme["tokenColors"], *({"settings": s} for s in theme["semanticTokenColors"].values())]:
            for bg in (
                "editor.background",
                "editor.lineHighlightBackground",
                "editor.selectionBackground",
                "diffEditor.insertedLineBackground",
                "diffEditor.removedLineBackground",
            ):
                self.assert_readable(rule["settings"]["foreground"], colors[bg], str(rule))

    def test_sublime_syntax_and_selection(self):
        source = (ROOT / "sublime-text/fmind.sublime-color-scheme").read_text()
        theme = json.loads("\n".join(line for line in source.splitlines() if not line.startswith("//")))
        colors = theme["globals"]
        for prefix in ("selection", "inactive_selection", "find_highlight"):
            self.assert_readable(colors[prefix + "_foreground"], colors[prefix])
        self.assert_readable(colors["gutter_foreground"], colors["gutter"])
        for rule in theme["rules"]:
            for bg in ("background", "line_highlight", "selection"):
                self.assert_readable(rule["foreground"], colors[bg], rule["scope"])

    def test_zed_syntax_statuses_and_selection(self):
        family = json.loads((ROOT / "zed/fmind.json").read_text())
        (theme,) = family["themes"]
        self.assertEqual(theme["appearance"], "light")
        style = theme["style"]
        self.assert_slots([style["terminal.ansi." + name] for name in PALETTE["ansi"]])
        for name, background in style.items():
            if name.endswith(".background") and name.removesuffix(".background") in style:
                self.assert_readable(style[name.removesuffix(".background")], background, name)
        for name, rule in style["syntax"].items():
            for bg in (
                "editor.background",
                "editor.active_line.background",
                "search.match_background",
                "search.active_match_background",
                "version_control.word_added",
                "version_control.word_deleted",
            ):
                self.assert_readable(rule["color"], style[bg], name)
            for player in style["players"]:
                self.assert_readable(rule["color"], player["selection"], name)
